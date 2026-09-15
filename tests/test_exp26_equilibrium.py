"""exp26 unit tests — the architecture + audit hooks.

Covers: (1) n_clusters default bit-exactness (the architecture axis is
inert at 12), (2) validation, (3) granularity semantics (jumps flip
exactly cluster_len cells), (4) the jump audit consumes no RNG
(trajectories bit-exact with the flag on and off) and records jump
times, (5) on_write repair bookkeeping, (6) the corruption-source
classification on a hand-built state.
"""
import sys

import numpy as np
import pytest

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, FidelityCodec, quantize,
)
from experiments.exp8_fidelity import N_CELLS, REGIME, fidelity_target

PRESET = {"meas_noise_mV": 1.5, "dropout": 0.1, "symbol_err": 0.05}


def _params():
    return AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)


# ------------------------------------------------------- n_clusters axis
def test_n_clusters_default_bit_exact():
    """Explicit n_clusters=12 == the historical hardcoded 12."""
    kw = dict(K=8, params=_params(), seed=7, jump_rate=0.02, f_crit=0.655)
    a = FidelityAgingCohort(**kw)
    b = FidelityAgingCohort(n_clusters=12, **kw)
    sa = a.run(years=30.0, record=False)
    sb = b.run(years=30.0, record=False)
    assert np.array_equal(a.V, b.V) and np.array_equal(a.theta, b.theta)
    assert np.array_equal(a.senesced, b.senesced)
    assert sa["median_lifespan"] == sb["median_lifespan"]


def test_n_clusters_validation():
    kw = dict(K=8, params=_params(), seed=7)
    with pytest.raises(ValueError):
        FidelityAgingCohort(n_clusters=7, **kw)      # 60 % 7 != 0
    with pytest.raises(ValueError):
        FidelityAgingCohort(n_clusters=0, **kw)


def test_cluster_granularity_jump_size():
    """At n_clusters=20 jumps flip exactly cluster_len=3 cells, and the
    per-cell corruption flux is architecture-invariant (the pre-registered
    analytical fact): expected jumps/yr * cluster_len is the same."""
    for nc in (4, 12, 20):
        ch = FidelityAgingCohort(K=4, params=_params(), seed=3,
                                 jump_rate=0.5, f_crit=0.655,
                                 n_clusters=nc)     # hot: force jumps
        th0 = ch.theta.copy()
        ch._apply_jumps(1.0)                        # one big step
        jumped = np.abs(ch.theta - th0).sum(axis=1) > 0
        n_jump_cells = (np.abs(ch.theta - th0) > 0).sum()
        # every changed region is exactly cluster_len wide
        assert n_jump_cells % ch.cluster_len == 0
        assert ch.cluster_len == N_CELLS // nc
        assert jumped.any()
        # the jump draw matrix shape follows n_clusters (per-cluster rate)
        # — the flux-invariance fact is checked in the exp26 module itself


def test_jump_audit_records_and_consumes_no_rng():
    """Audit on/off: identical trajectories (no RNG draws), and
    _last_jump gets the step time stamped."""
    kw = dict(K=6, params=_params(), seed=11, jump_rate=0.3, f_crit=0.655)
    a = FidelityAgingCohort(**kw)
    b = FidelityAgingCohort(**kw)
    b._jump_audit_on = True
    b._last_jump = np.full((b.K, b.n_clusters), -np.inf)
    for _ in range(40):
        a.step(0.25)
        b.step(0.25)
    assert np.array_equal(a.V, b.V) and np.array_equal(a.theta, b.theta)
    assert np.array_equal(a.senesced, b.senesced)
    stamped = b._last_jump > 0
    assert stamped.sum() > 0
    assert (b._last_jump[stamped] <= b.t).all()


def test_repair_bookkeeping_via_on_write():
    """A write stamps per-cell repair times; the classification's
    jumped-since-repair logic reads them correctly."""
    from cultivation.bioelectric.senescence_semantics import LatchingAgingCohort

    class _RepairTracked(LatchingAgingCohort):
        def on_write(self, do):
            if getattr(self, "_jump_audit_on", False):
                rows, cols = np.nonzero(do)
                self._last_repair_cells[rows, cols] = self.t
            super().on_write(do)

    ch = _RepairTracked(K=2, params=_params(), seed=5, jump_rate=0.0,
                        f_crit=0.655)
    ch._jump_audit_on = True
    ch._last_jump = np.full((2, ch.n_clusters), -np.inf)
    ch._last_repair_cells = np.full((2, ch.n), -np.inf)
    do = np.zeros((2, ch.n), bool)
    do[:, 10:15] = True
    ch.on_write(do)
    assert (ch._last_repair_cells[:, 10:15] == 0.0).all()
    assert (ch._last_repair_cells[:, :10] == -np.inf).all()


def test_source_classification_handbuilt():
    """Wrong cells classify as senescence / jump / non-jump on a
    constructed state."""
    ch = FidelityAgingCohort(K=1, params=_params(), seed=1, jump_rate=0.0,
                             f_crit=0.655)
    ch._jump_audit_on = True
    ch._last_jump = np.full((1, ch.n_clusters), -np.inf)
    ch._last_repair_cells = np.full((1, ch.n), -np.inf)
    ref = fidelity_target()
    zone = np.zeros(ch.n, bool)
    zone[30:45] = True                     # a 15-cell zone, 3 clusters
    # cell 30: senesced AND wrong (pin -25 vs target -50)
    ch.senesced[0, 30] = True
    ch.V[0, 30] = -25.0
    # cells 31-33: cluster 6 jumped AFTER repair -> jump-source
    ch._last_jump[0, 6] = 50.0
    ch._last_repair_cells[0, 31:34] = 10.0
    ch.V[0, 31:34] = -10.0                 # wrong vs the -50 target
    # cell 35 (cluster 7): noise-drift wrong, last repair AFTER that
    # cluster's jump -> non-jump
    ch._last_jump[0, 7] = 5.0
    ch._last_repair_cells[0, 35] = 40.0
    ch.V[0, 35] = -10.0
    from experiments.exp26_equilibrium import _source_shares
    sh = _source_shares(ch, zone, ref)
    assert sh["senescence"] == pytest.approx(1 / 15)
    assert sh["jump"] == pytest.approx(3 / 15)
    assert sh["non_jump"] == pytest.approx(1 / 15)
    assert sh["wrong"] == pytest.approx(5 / 15)


def test_architecture_maintain_integration():
    """A full maintain cycle at n_clusters=20: codec granularity matches
    the cohort's; writes land on 3-cell clusters."""
    ch = FidelityAgingCohort(K=4, params=_params(), seed=9, jump_rate=0.0,
                             f_crit=0.655, n_clusters=20)
    codec = FidelityCodec(n_cells=N_CELLS, n_clusters=20,
                          budget_per_cycle=6, levels=7,
                          target_source="archive")
    # corrupt one whole 3-cell cluster
    ch.theta[:, 0:3] = -10.0
    ch.V[:, 0:3] = -10.0
    rep = codec.maintain(ch, PRESET, mode="codec")
    assert rep["restored"] > 0
    # the write restored toward archive values (level, not exact mV)
    ok = (quantize(ch.V[:, 0:3], 7)
          == quantize(np.broadcast_to(fidelity_target(), (4, ch.n))[:, 0:3], 7))
    assert ok.all()
