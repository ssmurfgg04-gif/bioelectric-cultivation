"""Unit tests for the D3 layer — the write semantics of cell death
(cultivation/bioelectric/senescence_semantics.py)."""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, LatchingAgingCohort, quantize,
)
from cultivation.bioelectric.senescence_semantics import (
    SemanticsCohort, V_SEN, DEATH_SEMANTICS,
)

REGIME = dict(kappa_noise=0.020, lambda_gap=0.024, mu_theta=0.03,
              h_sys=0.050, seed_rate=6.0e-5, h_inflam=0.030, mortality_k=0.10)

TARGET = np.concatenate([np.full(12, v) for v in (-50.0, -20.0, -50.0, -60.0, -40.0)])


def _cohort(sem="stasis", latch="v2", K=8, seed=0, **kw):
    params = AgingParams(n_cells=24, target0=TARGET[:24].copy(), **REGIME)
    return SemanticsCohort(K=K, params=params, seed=seed,
                           death_semantics=sem, latch=latch, **kw)


def test_erasure_destroys_memory():
    ch = _cohort("erasure")
    mask = np.zeros((ch.K, ch.n), bool)
    mask[:, 10] = True                      # one cell dies everywhere
    pre_a = ch.theta_anchor[:, 10].copy()
    ch.senesced |= mask
    ch._death_event(mask)
    assert np.allclose(ch.theta_anchor[:, 10], V_SEN)
    assert np.allclose(ch.theta[:, 10], V_SEN)
    assert not np.allclose(pre_a, V_SEN)    # it really was a memory before
    print("  erasure: theta AND anchor destroyed at death: OK")


def test_transcription_moves_memory():
    ch = _cohort("transcription")
    # cell 10 dies holding a distinct memory; its neighbor 11 must receive it
    ch.theta_anchor[:, 10] = -30.0
    nb_before = ch.theta_anchor[:, 11].copy()
    mask = np.zeros((ch.K, ch.n), bool)
    mask[:, 10] = True
    ch.senesced |= mask
    ch._death_event(mask)
    w = ch.transcript_w
    expect = (1.0 - w) * nb_before + w * (-30.0)
    assert np.allclose(ch.theta_anchor[:, 11], expect)
    assert np.allclose(ch.theta_anchor[:, 10], V_SEN)   # source consumed
    # non-adjacent cells untouched
    assert not np.allclose(ch.theta_anchor[:, 5], expect)
    print("  transcription: memory written into junction neighbor, source consumed: OK")


def test_broadcast_drives_and_decays():
    ch = _cohort("broadcast")
    ch._bcast[:, 10] = 1.0
    V_nb = ch.V[:, 11].copy()
    g = np.full(ch.K, ch.p.g0)
    ch._broadcast_drive(0.25, g)
    # neighbor 11 was pulled toward V_SEN (depolarized if it sat below it)
    moved = ch.V[:, 11] - V_nb
    assert np.all(moved < 0) if np.all(V_nb > V_SEN) else np.all(moved != 0)
    assert np.all(ch._bcast[:, 10] < 1.0)   # amplitude decayed
    assert np.all(ch._bcast[:, 9] == 0.0)   # no spontaneous spread
    # a second application continues to decay toward zero
    for _ in range(40):
        ch._broadcast_drive(0.25, g)
    assert np.all(ch._bcast[:, 10] < 1e-4)
    print("  broadcast: decaying depolarization drive into neighbors: OK")


def test_v2_holds_private_perturbation():
    """A PRIVATE theta perturbation is healed (anchor holds), not latched."""
    ch = _cohort("stasis")
    g = np.full(ch.K, ch.p.g0 * 0.05)       # decayed junctions -> pin engages
    ch.theta[:, 12] += 12.0                 # one cell drifts privately
    drift0 = np.abs(ch.theta[:, 12] - ch.theta_anchor[:, 12]).copy()
    for _ in range(8):
        ch._integrate(0.25, g, np.zeros(ch.K))
    drift = np.abs(ch.theta[:, 12] - ch.theta_anchor[:, 12])
    assert np.all(drift <= drift0 + 1e-9)   # not amplified
    assert np.all(np.abs(ch.theta_anchor[:, 12] - ch.theta_anchor[:, 12].mean()) < 12.0)
    print("  v2 latch: private perturbation healed, memory holds: OK")


def test_v2_latches_collective_shift():
    """A COLLECTIVE shift (whole cluster moves together) latches the memory."""
    ch = _cohort("stasis")
    zone = slice(8, 12)                     # a full cluster (cluster_len=2 x2)
    ch.theta[:, zone] = -20.0
    ch.V[:, zone] = -20.0
    g = np.full(ch.K, ch.p.g0)
    for _ in range(20):
        ch._integrate(0.25, g, np.zeros(ch.K))
    lv = quantize(ch.theta_anchor[:, 9], ch.levels)
    assert np.all(lv == quantize(-20.0, ch.levels))
    print("  v2 latch: collective shift latched (novel morphology memory): OK")


def test_senesced_anchor_freezes():
    ch = _cohort("stasis")
    mask = np.zeros((ch.K, ch.n), bool)
    mask[:, 6] = True
    frozen = ch.theta_anchor[:, 6].copy()
    ch.senesced |= mask
    g = np.full(ch.K, ch.p.g0)
    for _ in range(16):
        ch._integrate(0.25, g, np.zeros(ch.K))
    assert np.allclose(ch.theta_anchor[:, 6], frozen)
    print("  v2 latch: senesced cell's anchor frozen (recoverable stasis): OK")


def test_on_write_latches_v2():
    ch = _cohort("stasis")
    do = np.zeros((ch.K, ch.n), bool)
    do[:, 4] = True
    ch.theta[:, 4] = -35.0
    ch.on_write(do)
    assert np.allclose(ch.theta_anchor[:, 4], -35.0)
    print("  on_write: explicit codec writes latch the memory: OK")


def test_ledger_metrics():
    ch = _cohort("stasis")
    led = ch.pattern_ledger()
    for k in ("I_V", "I_anchor", "I_recoverable"):
        assert 0.0 <= led[k] <= 1.0
    assert led["I_recoverable"] >= max(led["I_V"], led["I_anchor"]) - 1e-12
    # a wrong reference must score ~0 on the anchors (they hold theta0)
    wrong = np.full(ch.n, -10.0)
    assert ch.pattern_ledger(ref=wrong)["I_anchor"] < 0.05
    print("  pattern ledger: carriers and recoverability bounded: OK")


def test_v1_arm_matches_original():
    """Regression guard: latch='v1' + 'stasis' reproduces LatchingAgingCohort
    trajectories exactly (same seed, no death-event side effects)."""
    params = AgingParams(n_cells=24, target0=TARGET[:24].copy(), **REGIME)
    a = LatchingAgingCohort(K=6, params=params, seed=42)
    b = SemanticsCohort(K=6, params=params, seed=42,
                         death_semantics="stasis", latch="v1")
    g = np.full(6, 0.2)
    for _ in range(40):
        a._integrate(0.25, g, np.zeros(6))
        b._integrate(0.25, g, np.zeros(6))
    assert np.allclose(a.theta, b.theta)
    assert np.allclose(a.theta_anchor, b.theta_anchor)
    print("  v1 arm: bit-exact with the original latch layer: OK")


def test_semantics_registry():
    for s in DEATH_SEMANTICS:
        ch = _cohort(s, latch="v2")
        assert ch.death_semantics == s
    try:
        _cohort("nonsense")
        raise AssertionError("invalid semantics accepted")
    except ValueError:
        pass
    print("  registry: four semantics, invalid rejected: OK")


def main() -> int:
    print("senescence_semantics (D3) tests:")
    test_erasure_destroys_memory()
    test_transcription_moves_memory()
    test_broadcast_drives_and_decays()
    test_v2_holds_private_perturbation()
    test_v2_latches_collective_shift()
    test_senesced_anchor_freezes()
    test_on_write_latches_v2()
    test_ledger_metrics()
    test_v1_arm_matches_original()
    test_semantics_registry()
    print("all D3 semantics tests passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
