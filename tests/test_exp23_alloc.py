"""exp23 unit tests — the multi-pattern allocation hooks.

Covers: (1) bit-exact regression of the additive hooks (golden captured
BEFORE the edit, the S2/S3 backdoor discipline), (2) the four allocation
policies' rank semantics on synthetic writable masks, (3) an integration
test through FidelityCodec.maintain with alloc, (4) the jump_mult and
hazard_boost zone-heterogeneity hooks.
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


# --------------------------------------------------------------- goldens
GOLDEN = {
    "cycles": 13, "verified": 83, "refused": 0, "restored": 252,
    "median": 26.875,
    "theta_sum": -17210.23268499173,
    "theta_anchor_sum": -17128.749503003877,
    "V_sum": -17032.959879892584,
    "sen_frac": 0.0375,
    "death_events": 29,
    "ledger_I_rec": 0.9270833333333334,
}


def _golden_scenario():
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=8, params=params, seed=42,
                         death_semantics="broadcast", latch="v2",
                         protect_written=True, jump_rate=0.02, f_crit=0.655)
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    state = {"done": False}

    def maintain(t, cohort):
        if not state["done"] and t >= 1.0:
            state["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, 24:36] = True
            cohort.theta = np.where(do, -10.0, cohort.theta)
            cohort.V = np.where(do, -10.0, cohort.V)
            cohort.on_write(do)
        if t >= 10.0 and abs((t - 10.0) % 5.0) <= 0.26:
            codec.maintain(cohort, PRESET, mode="codec")

    s = ch.run(years=40.0, dt=0.25, intervention=maintain)
    zone = np.zeros(ch.n, bool)
    zone[24:36] = True
    led = ch.pattern_ledger(ref=np.where(zone, -10.0, ch.theta0), zone=zone)
    return {
        "cycles": codec.cycles, "verified": codec.verified,
        "refused": codec.refused, "restored": codec.restored,
        "median": float(s["median_lifespan"]),
        "theta_sum": float(np.asarray(ch.theta).sum()),
        "theta_anchor_sum": float(np.asarray(ch.theta_anchor).sum()),
        "V_sum": float(np.asarray(ch.V).sum()),
        "sen_frac": float(ch.senesced.mean()),
        "death_events": int(ch.death_events),
        "ledger_I_rec": led["I_recoverable"],
    }


def test_golden_bitexact():
    """The additive hooks (jump_mult / hazard_boost / alloc) changed
    NOTHING when unused — every counter and state checksum identical."""
    got = _golden_scenario()
    for k, v in GOLDEN.items():
        assert got[k] == pytest.approx(v, abs=1e-12), (k, got[k], v)
    print("  golden bit-exact regression: OK")


def test_alloc_none_kwarg_equivalent():
    """maintain(..., alloc=None) == maintain(...) — same call semantics."""
    got = _golden_scenario()          # uses alloc=None explicitly? no —
    # the golden scenario calls maintain WITHOUT the kwarg; run again
    # WITH alloc=None and require identical results.
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=8, params=params, seed=42,
                         death_semantics="broadcast", latch="v2",
                         protect_written=True, jump_rate=0.02, f_crit=0.655)
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    state = {"done": False}

    def maintain(t, cohort):
        if not state["done"] and t >= 1.0:
            state["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, 24:36] = True
            cohort.theta = np.where(do, -10.0, cohort.theta)
            cohort.V = np.where(do, -10.0, cohort.V)
            cohort.on_write(do)
        if t >= 10.0 and abs((t - 10.0) % 5.0) <= 0.26:
            codec.maintain(cohort, PRESET, mode="codec", alloc=None)

    ch.run(years=40.0, dt=0.25, intervention=maintain)
    assert codec.restored == GOLDEN["restored"]
    assert float(np.asarray(ch.theta).sum()) == pytest.approx(
        GOLDEN["theta_sum"], abs=1e-9)
    print("  alloc=None kwarg equivalence: OK")


# ------------------------------------------------------- policy semantics
def _synth():
    """4 groups x 3 cells; W marks 2 writable cells in groups 0-2, 1 in
    group 3 (demand 2,2,2,1; total 7)."""
    n = 12
    groups = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
    W = np.zeros((1, n), bool)
    W[0, [0, 1, 3, 4, 6, 7, 9]] = True
    return groups, W


def test_alloc_fixed_priority():
    groups, W = _synth()
    codec = FidelityCodec(n_cells=12, n_clusters=4, budget_per_cycle=4)
    ranks = codec._alloc_ranks(W, {"groups": groups, "policy": "fixed",
                                   "order": [1, 2, 3, 0]})
    written = W & (ranks <= 4)
    # budget 4 -> ALL of group 1's writable cells (2), then group 2's
    # first two writable cells; group 0 (lowest priority) gets nothing
    assert written[0, 3] and written[0, 4]
    assert written[0, 6] and written[0, 7]
    assert not written[0, 0] and not written[0, 1]
    assert written.sum() == 4
    print("  fixed priority order respected: OK")


def test_alloc_balanced_roundrobin():
    groups, W = _synth()
    codec = FidelityCodec(n_cells=12, n_clusters=4, budget_per_cycle=4)
    ranks = codec._alloc_ranks(W, {"groups": groups, "policy": "balanced"})
    written = W & (ranks <= 4)
    # one cell from each of the 4 groups
    per_group = [written[0, groups == g].sum() for g in range(4)]
    assert per_group == [1, 1, 1, 1], per_group
    print("  balanced round-robin split: OK")


def test_alloc_severity_follows_demand():
    n = 12
    groups = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
    W = np.zeros((1, n), bool)
    W[0, [0, 1, 2, 3, 4, 5, 6]] = True     # demand 3,3,1,0 — group 0 worst
    codec = FidelityCodec(n_cells=12, n_clusters=4, budget_per_cycle=4)
    ranks = codec._alloc_ranks(W, {"groups": groups, "policy": "severity"})
    written = W & (ranks <= 4)
    per_group = [written[0, groups == g].sum() for g in range(4)]
    # weighted round-robin at budget 4 over demand (3,3,1,0): ideal shares
    # (1.7, 1.7, 0.6, 0) -> integer pacing (2, 1, 1, 0) — the two
    # high-demand groups dominate, the zero-demand group gets NOTHING
    assert per_group == [2, 1, 1, 0], per_group
    assert written.sum() == 4
    print("  severity shares track demand: OK")


def test_alloc_critical_allin():
    groups, W = _synth()                    # demand 2,2,2,1 over 3-cell groups
    codec = FidelityCodec(n_cells=12, n_clusters=4, budget_per_cycle=4)
    # frac 2/3 < 0.9 -> not critical -> balanced
    ranks = codec._alloc_ranks(W, {"groups": groups, "policy": "critical",
                                   "critical_frac": 0.9})
    written = W & (ranks <= 4)
    assert [written[0, groups == g].sum() for g in range(4)] == [1, 1, 1, 1]
    # critical_frac 0.5 -> every group with 2/3 writable is critical;
    # the WORST (argmax tie -> group 0) takes priority; its 2 writable
    # cells saturate first, the leftover budget spills to the next group
    ranks = codec._alloc_ranks(W, {"groups": groups, "policy": "critical",
                                   "critical_frac": 0.5})
    written = W & (ranks <= 4)
    assert written[0, 0] and written[0, 1]      # the critical group first
    assert written.sum() == 4                    # budget fully used
    per_group = [written[0, groups == g].sum() for g in range(4)]
    assert per_group[0] == 2 and per_group[1] == 2, per_group
    print("  critical all-in switch (with spill): OK")


def test_alloc_budget_never_exceeded():
    """Whatever the policy, writes never exceed the per-cycle budget."""
    rng = np.random.default_rng(7)
    for _ in range(20):
        n = 12
        groups = rng.permutation([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
        W = rng.random((3, n)) < 0.6
        codec = FidelityCodec(n_cells=12, n_clusters=4, budget_per_cycle=5)
        for policy in ("balanced", "fixed", "severity", "critical"):
            alloc = {"groups": groups, "policy": policy, "order": [2, 0, 3, 1]}
            ranks = codec._alloc_ranks(W, alloc)
            written = W & (ranks <= 5)
            assert written.sum(axis=1).max() <= 5, (policy, groups)
    print("  budget cap respected under random masks: OK")


# ------------------------------------------------------- through maintain
def test_maintain_with_alloc_integration():
    """maintain(..., alloc=fixed[zone first]) concentrates writes on the
    priority group and reports restored_by_group."""
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=40, params=params, seed=11,
                         death_semantics="stasis", latch="v2",
                         protect_written=True, jump_rate=0.0, f_crit=0.655)
    groups = np.zeros(ch.n, int)
    groups[24:36] = 1                       # the novel zone = group 1
    groups[36:48] = 2                       # a second zone = group 2
    # write both zones so the anchored codec has memories to defend
    do = np.zeros((ch.K, ch.n), bool)
    do[:, 24:36] = True
    ch.theta = np.where(do, -10.0, ch.theta)
    ch.V = np.where(do, -10.0, ch.V)
    do2 = np.zeros((ch.K, ch.n), bool)
    do2[:, 36:48] = True
    ch.theta = np.where(do2, -30.0, ch.theta)
    ch.V = np.where(do2, -30.0, ch.V)
    ch.on_write(do | do2)
    # corrupt both zones equally (jump-like): flip to a wrong level
    ch.theta[:, 24:36] = -40.0
    ch.V[:, 24:36] = -40.0
    ch.theta[:, 36:48] = -40.0
    ch.V[:, 36:48] = -40.0
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=6, levels=7,
                          target_source="anchored")
    out = codec.maintain(ch, PRESET, mode="codec",
                         alloc={"groups": groups, "policy": "fixed",
                                "order": [1, 2, 0]})
    rbg = out["restored_by_group"]
    # both zones fully wrong -> zone 1 (priority) saturates the ENTIRE
    # budget for every verified individual; zone 2 and background get
    # zero writes (rbg sums over the 40 individuals)
    assert rbg[1] == out["restored"], rbg
    assert rbg[2] == 0 and rbg[0] == 0, rbg
    assert rbg[1] <= 6 * 40
    # and the restored cells sit in zone 1 (written to ~-10)
    fixed = np.abs(ch.theta[:, 24:36] + 10.0) < 6.0
    assert fixed.mean() > 0.4, fixed.mean()
    print("  maintain+alloc integration (fixed zone-first): OK")


# ------------------------------------------------------ zone heterogeneity
def test_jump_mult_contrast():
    """A 0.1x-susceptibility cluster region jumps far less than a 5x one."""
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=60, params=params, seed=13,
                         death_semantics="stasis", latch="none",
                         jump_rate=0.25, f_crit=0.9)
    ch.jump_mult = np.ones(12)
    ch.jump_mult[2:5] = 0.1                 # clusters covering cells 10:25
    ch.jump_mult[6:9] = 5.0                 # clusters covering cells 30:45
    t0 = ch.theta.copy()
    ch.run(years=10.0, dt=0.25)
    dev = np.abs(ch.theta - t0).mean(axis=0)   # (n,) mean deviation
    # 5x vs 0.1x susceptibility: >2x deviation contrast (neighbor-cluster
    # Laplacian spillover blurs the ratio; the ordering is unambiguous)
    assert dev[30:45].mean() > 2.0 * dev[10:25].mean(), \
        (dev[30:45].mean(), dev[10:25].mean())
    print(f"  jump_mult contrast (5x vs 0.1x dev "
          f"{dev[30:45].mean():.1f} vs {dev[10:25].mean():.2f} mV): OK")


def test_hazard_boost_contrast():
    """A 4x hazard zone senesces several times faster than baseline."""
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=60, params=params, seed=17,
                         death_semantics="stasis", latch="none",
                         jump_rate=0.0, f_crit=0.9)
    ch.hazard_boost = np.ones(ch.n)
    ch.hazard_boost[36:48] = 4.0
    ch.run(years=25.0, dt=0.25)
    hi = ch.senesced[:, 36:48].mean()
    lo = ch.senesced[:, 0:12].mean()
    assert hi > 2.0 * max(lo, 1e-3), (hi, lo)
    print(f"  hazard_boost contrast (sen {hi:.3f} vs {lo:.3f}): OK")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "-s"]))
