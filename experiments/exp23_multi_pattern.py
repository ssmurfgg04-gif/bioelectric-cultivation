"""exp23 — multi-pattern allocation: competing bioelectric memories.

THE AI-SCIENTIST'S BEST IDEA (trial 426f320, idea #1 'multi_pattern_
maintenance', Interestingness 9 / Novelty 9), unblocked by the multi-zone
pattern_ledgers API (c2c7754). Every prior maintenance result (exp17,
exp19) held exactly ONE novel pattern in ONE zone; real planarian tissue
carries several simultaneous bioelectric memories (head / pre-pharyngeal
/ tail; Pezzulo & Levin 2021's re-writable memories). Whether pattern
hold capacity is PER-PATTERN or a SHARED resource — and whether the
allocation policy for a fixed maintenance budget matters — is the open
question. The AI-Scientist's premise is 'under resource constraints';
the in-session design probes showed the constraint must be made to BIND
(budget 6, exp17's single-pattern calibration, leaves the channel rich
enough that competition is invisible), so the budget is the experimental
scarcity dial: 1, 2, 4, 6 cells/cycle.

DESIGN (the AI-Scientist's, adapted to the stack's actual machinery;
three small-scale probes fixed the geometry and metric before any full
run — recorded in the module history):

  Three novel patterns + the birth pattern, four CLUSTER-ALIGNED zones
  of 15 cells each (3 pure codec clusters per zone; positions SCRAMBLED
  — C, A, B, birth — so the codec's default cell-order priority is not
  accidentally identical to any tested policy). All patterns written at
  t=5, maintained by the SAME anchored+protected codec from age 30:

    C  cells  0:15, value -70 (level 0, in-archive-nowhere) — HIGH
       TURNOVER: senescence hazard 2x (per cell, exact)
    A  cells 15:30, value -30 (level 4, in-archive-nowhere) — STABLE:
       jump susceptibility 0.5x (clusters 3-5)
    B  cells 30:45, value -10 (level 6, exp17's novel value) — VOLATILE:
       jump susceptibility 2.0x (clusters 6-8)
    birth pattern  cells 45:60 — the fourth budget group

  TWO-LAYER CAPACITY (the first probe's finding): the protected memory
  tier stores every written pattern for free — frozen per-cell anchors,
  I_anchor ~ 1.0 even with NO maintenance. STORAGE is per-pattern and
  free; EXPRESSION is not. The working state (I_V) decays under jumps,
  noise, and death, and only the codec's budgeted writes restore it.
  The competing-resource question is an I_V question; the criteria are
  pre-registered on I_V (I_anchor / I_recoverable recorded as the
  memory-layer integrity; ledger convention = exp17's: all K
  individuals, dead included — alive-only means recorded alongside).

  MORTALITY TIMING (recorded deviation from exp17): exp17 scored
  mortality against the novel target from t=0 — harmless with one small
  zone. Four zones covering the whole animal make the not-yet-written
  target lethal from birth, so: the birth pattern is the target UNTIL
  the deliberate write; the written pattern(s) are the target after.
  solo17 keeps exp17's original convention for exact replication.

  Arms (identical except WHERE the budget goes) x budget {1, 2, 4, 6}:
    none        no codec (the decay baseline; budget-free)
    solo17      hooks OFF, exp17's zone (24:36, -10), cell-order, budget
                6 — the anchored_protected arm re-run in-session (same
                seeds 21-23, K=200, 120yr: regression against exp17's
                published I_rec@60 = 0.907)
    solo_B      hooks ON, B only (30:45), cell-order — the PHYSICS-
                MATCHED single-pattern control (volatile B alone; the
                competition cost is measured against this, per budget)
    default     all three, cell-order priority (the status quo)
    balanced    round-robin: equal shares to C, A, B, birth
    fixed       static priority A > B > C > birth (favor the stable)
    severity    per-cycle shares track each group's DETECTED demand —
                the dynamic allocation
    critical    all-in on any group whose detected-need fraction tops
                0.5, else balanced

PRE-REGISTERED (fixed after the probes, before the full run):
  E1 (competition is real UNDER SCARCITY — expression capacity shared):
      at budget 1: default I_V(B)@60 < solo_B I_V(B)@60 - 0.05
      AND at budget 6: |default - solo_B| I_V(B)@60 < 0.05 (the channel
      is rich enough that competition is invisible — the scarcity
      gradient itself is the finding).
  E2 (allocation matters — the AI-Scientist's hypothesis):
      at budget 1: best policy (balanced/fixed/severity/critical)
      min-I_V@60 >= default's + 0.05
      AND mean(severity, critical) overall-I_V@60 > fixed's (dynamic
      beats static priority under constraint).
  E3 (physics dominates policy — the two-bottleneck law generalizes):
      at budget 1, balanced: I_V(A)@60 > I_V(B)@60 AND I_V(A)@60 >
      I_V(C)@60. Mechanistic reading: the high-turnover pattern's
      deficit is a death-restoration EQUILIBRIUM set by its own hazard
      rate, not a budget-starvation effect — allocation shifts
      restoration lag, not the equilibrium.
  E4 (maintenance still pays at every scarcity level):
      every codec arm at every budget: median lifespan >= none's.
  R (regression, recorded not gated): solo17 I_rec@60 within 0.05 of
      exp17's published 0.907 — the hooks-unused bit-exactness claim at
      experiment scale.

Falsifies: E1 failing at budget 1 kills the shared-capacity story (the
channel scales for free even at scarcity). E2 failing kills the
allocation-policy question (the bottleneck is physics — E3's reading).
E4 failing means multi-pattern maintenance is a net mortality hazard.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec, quantize
from cultivation.bioelectric.senescence_semantics import SemanticsCohort
from cultivation.validation.stats import bootstrap_ci
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp23_multi_pattern.json"

K, YEARS, SEEDS = 200, 120.0, (21, 22, 23)
CHECKUP, FROM_AGE = 5.0, 30.0
BUDGETS = (1, 2, 4, 6)                    # the scarcity dial
COHORT_KW = dict(jump_rate=0.006, f_crit=0.655)

# ---- the three competing patterns (CLUSTER-ALIGNED, SCRAMBLED) ---------
ZONES = {                      # name -> (start, stop, value, label)
    "A": (15, 30, -30.0, "stable (0.5x jumps)"),
    "B": (30, 45, -10.0, "volatile (2x jumps)"),
    "C": (0, 15, -70.0, "high-turnover (2x death hazard)"),
}
MULTI_TARGET = fidelity_target()
B_SOLO_TARGET = fidelity_target()          # solo_B: B zone alone
for s, e, v, _ in ZONES.values():
    MULTI_TARGET[s:e] = v
B_SOLO_TARGET[30:45] = -10.0
# solo17 = exp17's exact setup: region zone 24:36, novel target from t=0
EXP17_TARGET = fidelity_target()
EXP17_TARGET[24:36] = -10.0
ZONE_MASK = {}
for s, e, v, _ in ZONES.values():
    z = np.zeros(N_CELLS, bool)
    z[s:e] = True
    ZONE_MASK[(s, e)] = z
B_MASK = ZONE_MASK[(30, 45)]
EXP17_MASK = np.zeros(N_CELLS, bool)
EXP17_MASK[24:36] = True

# per-cluster jump susceptibility — EXACT under cluster alignment
# (C = clusters 0-2, A = 3-5, B = 6-8, birth pattern = 9-11)
JUMP_MULT = np.array([1.0, 1.0, 1.0, 0.5, 0.5, 0.5,
                      2.0, 2.0, 2.0, 1.0, 1.0, 1.0])

# per-cell senescence boost: C's elevated turnover (exact per cell)
HAZARD_BOOST = np.ones(N_CELLS)
HAZARD_BOOST[0:15] = 2.0

# budget-allocation groups: 0 = birth pattern, 1..3 = the novel patterns
# (four EQUAL groups of 15 cells)
GROUPS = np.zeros(N_CELLS, int)
GROUPS[0:15] = 3                 # C
GROUPS[15:30] = 1                # A
GROUPS[30:45] = 2                # B

MAIN_ARMS = ("solo_B", "default", "balanced", "fixed", "severity",
             "critical")
ARMS = ("none", "solo17") + MAIN_ARMS
POLICY_ARMS = ("balanced", "fixed", "severity", "critical")
WRITE_SETS = {"solo17": ("B17",), "solo_B": ("B",)}   # else: all three
ALLOC = {
    "none": None, "solo17": None, "solo_B": None, "default": None,
    "balanced": {"groups": GROUPS, "policy": "balanced"},
    "fixed": {"groups": GROUPS, "policy": "fixed", "order": [1, 2, 3, 0]},
    "severity": {"groups": GROUPS, "policy": "severity"},
    "critical": {"groups": GROUPS, "policy": "critical",
                 "critical_frac": 0.5},
}
LEDGER_AT = np.arange(10.0, YEARS + 1, 10.0)
METRICS = ("I_V", "I_anchor", "I_recoverable")


def _p(s):
    print(s, flush=True)


class MultiPatternCohort(SemanticsCohort):
    """Three competing novel patterns with heterogeneous zone physics.
    Mortality scored against the CURRENT target (birth pattern until the
    deliberate write; the written pattern after — see module docstring).
    on_write carries a side-effect-free budget audit (where the codec's
    writes landed, by group) — no RNG consumption, dynamics untouched."""

    def _correct_mask(self) -> np.ndarray:
        ok = (quantize(self.V, self.levels)
              == quantize(np.broadcast_to(self._tgt, (self.K, self.n)),
                          self.levels))
        ok[:, ~self._fid_keep] = True
        return ok

    def on_write(self, do: np.ndarray) -> None:
        if getattr(self, "_audit_on", False):
            g = self._audit_groups
            self._write_audit += np.array(
                [int(do[:, g == gid].sum()) for gid in range(4)], int)
        super().on_write(do)


def build(seed: int, hooks: bool = True) -> MultiPatternCohort:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **REGIME)
    ch = MultiPatternCohort(K=K, params=params, seed=seed,
                            death_semantics="broadcast", latch="v2",
                            protect_written=True, **COHORT_KW)
    ch._tgt = fidelity_target()            # birth pattern until the write
    ch._audit_groups = GROUPS
    ch._write_audit = np.zeros(4, int)
    ch._audit_on = False
    if hooks:
        ch.jump_mult = JUMP_MULT
        ch.hazard_boost = HAZARD_BOOST
    return ch


def _per_individual(ch, zone: np.ndarray, ref: np.ndarray,
                    metric: str, alive_only: bool = False) -> np.ndarray:
    """Per-individual ledger metric for a zone (bootstrap input; the
    same quantized-match semantics as pattern_ledger)."""
    r = np.broadcast_to(ref, (ch.K, ch.n))
    okV = (quantize(ch.V[:, zone], ch.levels)
           == quantize(r[:, zone], ch.levels))
    if metric == "I_V":
        vals = okV.mean(axis=1)
    elif metric == "I_anchor":
        okA = (quantize(ch.theta_anchor[:, zone], ch.levels)
               == quantize(r[:, zone], ch.levels))
        vals = okA.mean(axis=1)
    else:
        okA = (quantize(ch.theta_anchor[:, zone], ch.levels)
               == quantize(r[:, zone], ch.levels))
        vals = (okV | okA).mean(axis=1)
    if alive_only:
        vals = vals[ch.alive]
    return vals


def _zone_write(cohort, name: str) -> None:
    """The deliberate write of one zone (its own value; exp17 semantics:
    theta, V, then on_write -> the protected tier)."""
    if name == "B17":                      # exp17's zone, hooks-off arm
        s, e, v = 24, 36, -10.0
    else:
        s, e, v, _ = ZONES[name]
    zd = np.zeros((cohort.K, cohort.n), bool)
    zd[:, s:e] = True
    cohort.theta = np.where(zd, v, cohort.theta)
    cohort.V = np.where(zd, v, cohort.V)
    cohort.on_write(zd)


def run_arm(arm: str, seed: int, budget: int = 6) -> dict:
    writes = WRITE_SETS.get(arm, ("A", "B", "C"))
    hooks = arm != "solo17"
    ch = build(seed, hooks)
    if arm == "solo17":
        ch._tgt = EXP17_TARGET             # exp17's from-t=0 convention
        led_spec = [("B", EXP17_TARGET, EXP17_MASK)]
    elif arm == "solo_B":
        led_spec = [("B", B_SOLO_TARGET, B_MASK)]
    else:
        led_spec = [(nm, MULTI_TARGET, ZONE_MASK[(ZONES[nm][0],
                                                  ZONES[nm][1])])
                    for nm in ("A", "B", "C")]
    tgt_after = {"solo17": EXP17_TARGET, "solo_B": B_SOLO_TARGET}.get(
        arm, MULTI_TARGET)
    codec = None
    if arm != "none":
        codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=budget,
                              levels=7, target_source="anchored")
    written = {"done": False}
    seen = set()
    series = {m: {p: [] for p in ("A", "B", "C")} for m in METRICS}
    boot60 = {}
    alive60 = {}

    def maintain(t, cohort):
        if not written["done"] and t >= 5.0:
            written["done"] = True
            for name in writes:
                _zone_write(cohort, name)
            if arm != "solo17":
                cohort._tgt = tgt_after     # the write makes it the target
            cohort._audit_on = True         # audit codec writes only
        if codec is not None and t >= FROM_AGE - 1e-9 \
                and abs((t - FROM_AGE) % CHECKUP) <= 0.26:
            codec.maintain(cohort, age_preset(t), mode="codec",
                           alloc=ALLOC[arm])
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                if arm in ("solo17", "solo_B"):
                    led = cohort.pattern_ledger(
                        ref=led_spec[0][1], zone=led_spec[0][2])
                    for m in METRICS:
                        series[m]["B"].append(led[m])
                        series[m]["A"].append(float("nan"))
                        series[m]["C"].append(float("nan"))
                else:
                    specs = [(nm, MULTI_TARGET,
                              ZONE_MASK[(ZONES[nm][0], ZONES[nm][1])])
                             for nm in ("A", "B", "C")]
                    led = cohort.pattern_ledgers(specs)
                    for nm in ("A", "B", "C"):
                        for m in METRICS:
                            series[m][nm].append(led[nm][m])
                if abs(a - 60.0) < 0.13:
                    for nm, ref, zone in led_spec:
                        boot60[nm] = _per_individual(
                            cohort, zone, ref, "I_V").tolist()
                        alive60[nm] = float(_per_individual(
                            cohort, zone, ref, "I_V",
                            alive_only=True).mean()) \
                            if cohort.alive.any() else float("nan")

    s = ch.run(years=YEARS, dt=0.25, intervention=maintain)
    s["series"] = {
        m: {p: list(v) for p, v in d.items()} for m, d in series.items()}
    s["boot60"] = boot60
    s["alive60_IV"] = alive60
    s["restored"] = codec.restored if codec else 0
    s["by_group"] = ch._write_audit.tolist()
    # survival fractions at 60/100 (defuses the median-of-dead bias)
    ht = np.asarray(s["hist_t"], float)
    ha = np.asarray(s["hist_alive"], float)
    s["alive_frac_60"] = float(ha[np.argmin(np.abs(ht - 60.0))])
    s["alive_frac_100"] = float(ha[np.argmin(np.abs(ht - 100.0))])
    return s


def _at(rows, metric, key, age=60.0) -> float:
    vals = []
    for r in rows:
        s = r["series"][metric][key]
        if s:
            # series recorded in order; a fully-dead seed stops early and
            # has fewer entries than LEDGER_AT
            la = np.asarray(LEDGER_AT[:len(s)], float)
            m = np.abs(la - age) < 0.2
            v = np.asarray(s, float)[m]
            v = v[~np.isnan(v)]
            if len(v):
                vals.append(float(np.mean(v)))
    return float(np.mean(vals)) if vals else float("nan")


def _aggregate(arm: str, budget: int, rows: list) -> dict:
    entry = {
        "budget": budget,
        "median": float(np.mean([r["median_lifespan"] for r in rows])),
        "median_by_seed": [float(r["median_lifespan"]) for r in rows],
        "alive_frac_60": float(np.mean([r["alive_frac_60"] for r in rows])),
        "alive_frac_100": float(np.mean([r["alive_frac_100"]
                                         for r in rows])),
        "restored": float(np.mean([r["restored"] for r in rows])),
        "writes_by_group": np.mean(
            [np.asarray(r["by_group"], float) for r in rows],
            axis=0).tolist(),
        "alive60_IV": {nm: float(np.nanmean([r["alive60_IV"][nm]
                                              for r in rows
                                              if nm in r["alive60_IV"]]))
                       for nm in ("A", "B", "C")
                       if any(nm in r["alive60_IV"] for r in rows)},
    }
    for m in METRICS:
        entry[f"{m}_at_60"] = {nm: _at(rows, m, nm) for nm in ("A", "B", "C")}
        entry[f"{m}_at_100"] = {nm: _at(rows, m, nm, 100.0)
                                for nm in ("A", "B", "C")}
    entry["min_IV_at_60"] = float(np.nanmin(
        [entry["I_V_at_60"][nm] for nm in ("A", "B", "C")]))
    entry["overall_IV_at_60"] = float(np.nanmean(
        [entry["I_V_at_60"][nm] for nm in ("A", "B", "C")]))
    entry["min_IR_at_60"] = float(np.nanmin(
        [entry["I_recoverable_at_60"][nm] for nm in ("A", "B", "C")]))
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # solo arms' NaNs
        entry["curves"] = {
            m: {nm: [float(np.nanmean(x)) for x in zip(
                *[r["series"][m][nm] for r in rows])]
                for nm in ("A", "B", "C")}
            for m in METRICS}
    if rows[0]["boot60"]:
        entry["ci95_IV_at_60"] = {
            nm: bootstrap_ci(np.mean, np.concatenate(
                [r["boot60"][nm] for r in rows if nm in r["boot60"]]))
            for nm in ("A", "B", "C")
            if any(nm in r["boot60"] for r in rows)}
    return entry


def main() -> dict:
    t0 = time.time()
    _p("exp23 — multi-pattern allocation (the AI-Scientist's best idea)")
    _p(f"    scarcity dial: budget {BUDGETS} cells/cycle; "
       f"K={K}, {YEARS:.0f}yr, seeds {SEEDS}")
    out = {}
    # budget-free arms
    for arm in ("none", "solo17"):
        rows = [run_arm(arm, sd, 6) for sd in SEEDS]
        out[arm] = _aggregate(arm, 6, rows)
        e = out[arm]
        _p(f"    {arm:9s}: median {e['median']:6.1f} yr  "
           f"alive@60 {e['alive_frac_60']:.2f}  "
           f"IV B {e['I_V_at_60']['B']:5.3f}  "
           f"IR B {e['I_recoverable_at_60']['B']:5.3f}  "
           f"restored {e['restored']:.0f}")
    # budget-swept arms
    for arm in MAIN_ARMS:
        out[arm] = {}
        for b in BUDGETS:
            rows = [run_arm(arm, sd, b) for sd in SEEDS]
            out[arm][b] = _aggregate(arm, b, rows)
            e = out[arm][b]
            _p(f"    {arm:9s} b={b}: median {e['median']:6.1f} yr  "
               f"alive@60 {e['alive_frac_60']:.2f}  "
               f"minIV {e['min_IV_at_60']:5.3f}  "
               f"A {e['I_V_at_60']['A']:5.3f}  "
               f"B {e['I_V_at_60']['B']:5.3f}  "
               f"C {e['I_V_at_60']['C']:5.3f}  "
               f"restored {e['restored']:.0f}  "
               f"bygrp {np.round(e['writes_by_group']).astype(int).tolist()}")

    d1 = out["default"][1]
    s1 = out["solo_B"][1]
    d6 = out["default"][6]
    s6 = out["solo_B"][6]
    dyn1 = 0.5 * (out["severity"][1]["overall_IV_at_60"]
                  + out["critical"][1]["overall_IV_at_60"])
    crit = {
        "E1_competition_under_scarcity": bool(
            d1["I_V_at_60"]["B"] < s1["I_V_at_60"]["B"] - 0.05
            and abs(d6["I_V_at_60"]["B"] - s6["I_V_at_60"]["B"]) < 0.05),
        "E2_allocation_matters": bool(
            max(out[p][1]["min_IV_at_60"] for p in POLICY_ARMS)
            >= d1["min_IV_at_60"] + 0.05
            and dyn1 > out["fixed"][1]["overall_IV_at_60"]),
        "E3_physics_dominates_policy": bool(
            out["balanced"][1]["I_V_at_60"]["A"]
            > out["balanced"][1]["I_V_at_60"]["B"]
            and out["balanced"][1]["I_V_at_60"]["A"]
            > out["balanced"][1]["I_V_at_60"]["C"]),
        "E4_maintenance_still_pays": bool(
            min(min(out[a][b]["median"] for b in BUDGETS)
                for a in MAIN_ARMS)
            >= out["none"]["median"]),
        "R_solo17_regression": bool(
            abs(out["solo17"]["I_recoverable_at_60"]["B"] - 0.907) < 0.05),
    }
    results = {
        "exp": "exp23_multi_pattern",
        "source_idea": "AI-Scientist trial idea #1 multi_pattern_maintenance"
                       " (426f320); unblocked by pattern_ledgers (c2c7754)",
        "budgets": list(BUDGETS),
        "arms": out,
        "criteria": crit,
        "exp17_reference": {"I_rec_at_60": 0.907,
                            "note": "solo17 re-runs exp17's "
                                    "anchored_protected arm (same seeds "
                                    "21-23, K=200, budget 6, 120yr)"},
        "zones": {nm: {"cells": f"{s}:{e}", "value": v, "physics": lab}
                  for nm, (s, e, v, lab) in ZONES.items()},
        "primary_metric": "I_V (working-state hold) — storage is free "
                          "(I_anchor ~ 1.0 unmaintained); the scarce "
                          "resource is EXPRESSION (codec budget)",
        "ledger_convention": "exp17's: all K individuals (dead included); "
                             "alive-only I_V@60 recorded as alive60_IV",
        "mortality_timing": "birth pattern is the target until the t=5 "
                            "deliberate write, the written pattern after "
                            "(recorded deviation from exp17's from-t=0 "
                            "convention, necessitated by whole-animal "
                            "zone coverage)",
        "cluster_alignment": "zones = 3 pure codec clusters each, "
                             "positions scrambled (C,A,B,birth) so "
                             "cell-order priority != any tested policy",
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    _figure(results)
    _p(f"exp23 complete in {time.time()-t0:.0f}s")
    return results


def _figure(results: dict) -> None:
    setup()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4),
                           constrained_layout=True)
    tvec = list(LEDGER_AT)
    pcol = {"A": PALETTE["good"], "B": PALETTE["accent"],
            "C": PALETTE["warn"]}
    none = results["arms"]["none"]

    # (a) the scarcity gradient: B's hold, alone vs competing, per budget
    xs = np.arange(len(BUDGETS))
    solo = [results["arms"]["solo_B"][b]["I_V_at_60"]["B"] for b in BUDGETS]
    comp = [results["arms"]["default"][b]["I_V_at_60"]["B"] for b in BUDGETS]
    ax[0].plot(xs, solo, "o-", color=PALETTE["good"], lw=2.4,
               label="B alone (solo_B)")
    ax[0].plot(xs, comp, "s-", color=PALETTE["accent"], lw=2.4,
               label="B under default (3 compete)")
    ax[0].axhline(none["curves"]["I_V"]["B"][-1], color="0.5", lw=1.0,
                  ls=":", label="B, no maintenance")
    ax[0].set_xticks(xs)
    ax[0].set_xticklabels([str(b) for b in BUDGETS])
    ax[0].set(xlabel="maintenance budget (cells/cycle)",
              ylabel="I_V @ 60 (working state)", ylim=(0, 1.0),
              title="the scarcity gradient (competition cost)")
    ax[0].legend(fontsize=8)

    # (b) min-I_V@60 vs budget by policy — does allocation matter?
    for p, c in zip(("default", "balanced", "fixed", "severity",
                     "critical"),
                    ("0.3", PALETTE["accent"], PALETTE["warn"],
                     PALETTE["good"], "0.6")):
        ys = [results["arms"][p][b]["min_IV_at_60"] for b in BUDGETS]
        ax[1].plot(xs, ys, "o-", color=c, lw=1.8, label=p)
    ax[1].set_xticks(xs)
    ax[1].set_xticklabels([str(b) for b in BUDGETS])
    ax[1].set(xlabel="maintenance budget (cells/cycle)",
              ylabel="min I_V @ 60", ylim=(0, 1.0),
              title="the worst-held pattern (policies vs default)")
    ax[1].legend(fontsize=8)

    # (c) per-pattern I_V@60 at the tightest budget — physics vs policy
    names = [a for a in MAIN_ARMS]
    w = 0.26
    xpos = np.arange(len(names))
    for i, nm in enumerate(("A", "B", "C")):
        vals = [results["arms"][a][1]["I_V_at_60"][nm] for a in names]
        ax[2].bar(xpos + (i - 1) * w, vals, width=w, color=pcol[nm],
                  label=f"{nm} ({ZONES[nm][3]})")
    ax[2].set_xticks(xpos)
    ax[2].set_xticklabels(names, rotation=25, fontsize=8)
    ax[2].set(ylabel="I_V @ 60", ylim=(0, 1.0),
              title="per-pattern hold at budget 1 (tightest)")
    ax[2].legend(fontsize=7, loc="upper right")

    fig.suptitle("exp23 — multi-pattern allocation: competing bioelectric "
                 "memories", fontsize=12)
    fig.savefig(fig_path("fig20_multi_pattern"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig20_multi_pattern.png")


if __name__ == "__main__":
    main()
