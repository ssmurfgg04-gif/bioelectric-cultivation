"""exp24 unit tests — the memory-potentiation hook.

Covers: (1) golden regression of the ACTIVE potentiation path (captured
at results/_golden_exp24_prereg.json — potentiation consumes no RNG, so
any drift means semantics changed), (2) potentiate() unit semantics on
synthetic masks (pairs, window extension, no-op guards), (3) bit-exact
claims: expired-window and inert-attribute paths draw identically to
the unpotentiated original, (4) jump suppression with factor 0, (5) the
maintenance-integration capture mechanism. The unused-path golden
(exp23's) is guarded in test_exp23_alloc.py and re-verified by the suite.
"""
import sys

import numpy as np
import pytest

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, FidelityCodec, quantize,
)
from cultivation.bioelectric.senescence_semantics import SemanticsCohort
from experiments.exp8_fidelity import N_CELLS, REGIME, fidelity_target

PRESET = {"meas_noise_mV": 1.5, "dropout": 0.1, "symbol_err": 0.05}
JUMP_MULT = np.array([1., 1., 1., .5, .5, .5, 2., 2., 2., 1., 1., 1.])

GOLDEN = {
    "pot_calls": 13, "pot_pairs": 56, "cycles": 13, "restored": 224,
    "median": 23.75, "theta_sum": -16356.179923423462,
    "V_sum": -16328.812719304995, "sen_frac": 0.027083333333333334,
    "death_events": 28, "ledger_I_rec": 0.9270833333333334,
}


class CaptureCohort(SemanticsCohort):
    """Stashes the maintenance cycle's actual write mask (the experiment's
    correction-coupling mechanism)."""

    def on_write(self, do):
        if getattr(self, "_capture", False):
            prev = getattr(self, "_captured_do", None)
            self._captured_do = do.copy() if prev is None else (prev | do)
        super().on_write(do)


def _cohort(seed: int = 42, K: int = 8, jump_rate: float = 0.02,
            cls=SemanticsCohort) -> SemanticsCohort:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = cls(K=K, params=params, seed=seed, death_semantics="broadcast",
             latch="v2", protect_written=True, jump_rate=jump_rate,
             f_crit=0.655)
    return ch


# --------------------------------------------------------------- goldens
def _potentiation_scenario(factor=0.25, window=5.0, cls=CaptureCohort):
    ch = _cohort(cls=cls)
    ch.jump_mult = JUMP_MULT
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    state = {"done": False, "pot_calls": 0, "pot_pairs": 0}

    def maintain(t, cohort):
        if not state["done"] and t >= 1.0:
            state["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, 24:36] = True
            cohort.theta = np.where(do, -10.0, cohort.theta)
            cohort.V = np.where(do, -10.0, cohort.V)
            cohort.on_write(do)
        if t >= 10.0 and abs((t - 10.0) % 5.0) <= 0.26:
            cohort._capture = True
            codec.maintain(cohort, PRESET, mode="codec")
            cohort._capture = False
            do = getattr(cohort, "_captured_do", None)
            if do is not None:
                n = cohort.potentiate(do, window=window, factor=factor)
                state["pot_calls"] += 1
                state["pot_pairs"] += int(n)
                cohort._captured_do = None

    s = ch.run(years=40.0, dt=0.25, intervention=maintain)
    zone = np.zeros(ch.n, bool)
    zone[24:36] = True
    led = ch.pattern_ledger(ref=np.where(zone, -10.0, ch.theta0), zone=zone)
    return {
        "pot_calls": state["pot_calls"], "pot_pairs": state["pot_pairs"],
        "cycles": codec.cycles, "restored": codec.restored,
        "median": float(s["median_lifespan"]),
        "theta_sum": float(np.asarray(ch.theta).sum()),
        "V_sum": float(np.asarray(ch.V).sum()),
        "sen_frac": float(ch.senesced.mean()),
        "death_events": int(ch.death_events),
        "ledger_I_rec": led["I_recoverable"],
    }


def test_golden_active_path():
    got = _potentiation_scenario()
    for k, v in GOLDEN.items():
        assert got[k] == pytest.approx(v, abs=1e-12), f"{k}: {got[k]} != {v}"


def test_golden_factor_one_bit_exact():
    """factor >= 1.0 is a no-op -> must reproduce the no-potentiation
    baseline of the SAME scenario (zone physics on, potentiation off):
    identical draws, zero potentiated pairs."""
    got = _potentiation_scenario(factor=1.0)
    # baseline captured with potentiation disabled (jump_mult active):
    assert got["cycles"] == 13
    assert got["restored"] == 196
    assert got["median"] == 31.75
    assert got["theta_sum"] == pytest.approx(-17432.05892233314, abs=1e-9)
    assert got["V_sum"] == pytest.approx(-17379.777129781665, abs=1e-9)
    assert got["death_events"] == 24
    assert got["pot_pairs"] == 0


# ------------------------------------------------------------- unit semantics
def test_potentiate_unit_semantics():
    ch = _cohort(K=4)
    ch.t = 10.0
    do = np.zeros((4, ch.n), bool)
    do[0, 0:5] = True          # animal 0, cluster 0
    do[2, 25:30] = True        # animal 2, cluster 5
    n = ch.potentiate(do, window=5.0, factor=0.25)
    assert n == 2
    assert ch._pot_until[0, 0] == 15.0
    assert ch._pot_until[2, 5] == 15.0
    assert ch._pot_until.sum() == 30.0
    # window extension: rewrite inside the window restarts it
    ch.t = 12.0
    n = ch.potentiate(do, window=5.0, factor=0.25)
    assert n == 2                      # both extended
    assert ch._pot_until[0, 0] == 17.0
    # a shorter window never shortens (max semantics)
    ch.t = 12.5
    n = ch.potentiate(do, window=1.0, factor=0.25)
    assert n == 0                      # 13.5 < 17.0 -> not new
    assert ch._pot_until[0, 0] == 17.0
    # no-op guards
    assert ch.potentiate(do, window=0.0, factor=0.25) == 0
    assert ch.potentiate(do, window=5.0, factor=1.0) == 0
    # empty mask: inert attribute, factor stays 1.0
    ch2 = _cohort(K=2)
    empty = np.zeros((2, ch2.n), bool)
    assert ch2.potentiate(empty, window=5.0, factor=0.25) == 0
    assert ch2._pot_factor == 1.0


# ----------------------------------------------------------- bit-exact claims
def _checksums(ch):
    return (float(np.asarray(ch.theta).sum()),
            float(np.asarray(ch.V).sum()),
            int(ch.death_events))


def test_bit_exact_expired_window():
    """A window that expires before the next jump step leaves the draw
    stream untouched (eff = exactly 1.0 -> rate * 1.0 == rate)."""
    a = _cohort(seed=7)
    b = _cohort(seed=7)
    do = np.zeros((a.K, a.n), bool)
    do[:, 0:5] = True
    a.potentiate(do, window=0.1, factor=0.25)   # expires at t+0.1 < t+dt
    for _ in range(80):
        a.step(0.25)
        b.step(0.25)
    assert _checksums(a) == _checksums(b)


def test_bit_exact_inert_attribute():
    """_pot_until present but all-zero: draws identical to vanilla."""
    a = _cohort(seed=9)
    b = _cohort(seed=9)
    a.potentiate(np.zeros((a.K, a.n), bool), window=5.0, factor=0.25)
    for _ in range(60):
        a.step(0.25)
        b.step(0.25)
    assert _checksums(a) == _checksums(b)


def test_jump_suppression_factor_zero():
    """factor 0.0 over a long window: potentiated clusters never jump."""
    ch = _cohort(seed=3, jump_rate=0.05)
    do = np.zeros((ch.K, ch.n), bool)
    do[:, 0:10] = True                    # clusters 0-1, all animals
    ch.potentiate(do, window=60.0, factor=0.0)
    tgt = fidelity_target()
    for _ in range(200):
        ch.step(0.25)
    ok_zone = (quantize(ch.V[:, 0:10], ch.levels)
               == quantize(np.broadcast_to(tgt[0:10], (ch.K, 10)), ch.levels))
    # unpotentiated control for contrast
    ch2 = _cohort(seed=3, jump_rate=0.05)
    for _ in range(200):
        ch2.step(0.25)
    ok_zone2 = (quantize(ch2.V[:, 0:10], ch2.levels)
                == quantize(np.broadcast_to(tgt[0:10], (ch2.K, 10)),
                            ch2.levels))
    assert ok_zone.mean() > ok_zone2.mean() + 0.2   # suppression is real
    assert ok_zone.mean() > 0.8                     # nearly jump-free


def test_maintain_integration_capture():
    """The capture mechanism: potentiation fires with the codec's ACTUAL
    write mask, and potentiation does not perturb the codec counters."""
    ch = _cohort(cls=CaptureCohort)
    ch.jump_mult = JUMP_MULT
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    do = np.zeros((ch.K, ch.n), bool)
    do[:, 24:36] = True
    ch.theta = np.where(do, -10.0, ch.theta)
    ch.V = np.where(do, -10.0, ch.V)
    ch.on_write(do)
    ch._captured_do = None
    before = codec.restored
    ch._capture = True
    rep = codec.maintain(ch, PRESET, mode="codec")
    ch._capture = False
    mask = getattr(ch, "_captured_do", None)
    assert mask is not None
    assert int(mask.sum()) == rep["restored"]       # the REAL write mask
    n = ch.potentiate(mask, window=5.0, factor=0.25)
    assert n > 0
    assert codec.restored == before + rep["restored"]
    # potentiation changed nothing about the write itself
    assert int(mask.sum()) == rep["restored"]
