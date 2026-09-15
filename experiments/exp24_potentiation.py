"""exp24 — memory POTENTIATION: attacking the corruption side of the
death-restoration equilibrium.

THE AI-SCIENTIST'S #2 IDEA (trial 426f320, 'memory_enhancement_
protocols', Interestingness 9 / Novelty 9), strategy 3 of 3: "after each
maintenance cycle, increase the stability of corrected cells by
reducing their jump probability for 5 years". Of its three enhancement
strategies only this one maps onto the stack's actual corruption
physics — the pattern is DISCRETE SYMBOLS (quantized levels), so
'amplitude consolidation / reinforcement' (strategies 1-2) has no
corruption axis to act on; jump susceptibility is that axis.

WHY THIS IS THE QUESTION NOW (the user's framing): exp23 showed
maintenance is EQUILIBRIUM-BOUND — the working-state deficit is a
death-restoration equilibrium set by per-zone PHYSICS (jump
susceptibility, senescence hazard); allocation policy, which
redistributes the RESTORATION side of that equilibrium, moved outcomes
by ~0.023 max while physics moved them ~0.4 (E3, 20x). Potentiation
attacks the CORRUPTION side: it reduces the jump probability itself,
but only where correction just happened (correction-coupled by
construction). If the equilibrium is really physics-set, potentiation
should move it — with a catch: its reach scales with maintenance
coverage (you can only potentiate what you write), so the benefit
should grow with budget.

DESIGN (exp23's exact multi-pattern geometry — zones C/A/B/birth,
cluster-aligned, scrambled; seeds 21-23, K=200, 120yr; the plain arm is
exp23's default cell-order arm and doubles as the regression anchor):

  Arms at budgets {1, 6}:
    plain     no potentiation (== exp23 default; R anchor)
    pot05     factor 0.5,  window 5yr, on corrected clusters
    pot025    factor 0.25, window 5yr
    pot_rand  factor 0.25, window 5yr, SAME per-cycle pair count but
              RANDOM placement (the AI-Scientist's own control:
              'enhancement applied to a random pattern' — the gating
              test; random placement can stabilize wrong-state
              clusters, the ungated-boost hazard of exp8)
    pot_perm  factor 0.25, window infinite (the physics ceiling: what
              the equilibrium becomes if the reduction never wears off
              — decomposes transient-coupling benefit from blanket
              physics change)
  Window sweep at budget 6, factor 0.25: w2 / w5(=pot025) / w10
  (cadence is 5yr: w5 covers exactly one cycle, w10 two, w2 expires
  mid-cycle — the coverage-geometry dial).

PRE-REGISTERED (fixed before the full run; the one in-session design
probe — machinery validation, 1 seed, b6, pot025 vs plain — is recorded
in the module history below):

  P1 (EQUILIBRIUM SHIFT — the headline): pot025's B I_V@60 at budget 6
      beats plain's by > 0.046 = 2x exp23's measured allocation-effect
      ceiling (0.023, the b1 competition cost; the policy-vs-default
      spread was smaller still). Failing => potentiation is another
      lag-shifter, not an equilibrium-breaker.
  P2 (GATING): pot_rand's B I_V@60 <= plain's + 0.01 at BOTH budgets.
      Failing => the benefit is placement-agnostic (a blanket jump-rate
      cut, not correction-coupled enhancement).
  P3 (DISSOCIATION — the two-bottleneck structure): at b6, delta_B >
      delta_C AND delta_B > delta_A. Potentiation acts on the jump
      axis, so the jump-volatile pattern must gain most; C's
      hazard-driven deficit and A's already-free hold must gain less.
      Failing => the corruption-side structure is not jump-dominated.
  P4 (BUDGET COUPLING): delta_B at b6 > delta_B at b1 (coverage scales
      with maintenance reach).
  P5 (DOSE-RESPONSE): at b6, pot025 >= pot05 - 0.01 AND pot05 > plain
      (monotone-or-plateau; a reversal kills).
  P6 (LIFESPAN): median(pot025) > median(plain) at BOTH budgets —
      equilibrium-breaking must reach mortality.
  P7 (CEILING — the decomposition added after the design probe, before
      the full run): pot_perm's B I_V@60 at b6 beats plain's by >
      0.046. Separates 'the idea fails at its literal spec (5yr window)'
      from 'the mechanism cannot move the equilibrium at all'. P1
      failing while P7 passes localizes the failure to the transient
      coverage geometry, not the corruption-side mechanism.
  W (window sweep, recorded not gated): prediction w10 >= w5 >= w2 -
      0.01 (longer protection, diminishing returns — exp22's plateau
      law says plateaus are the norm).
  R (REGRESSION): plain@b replicates exp23's published default arm:
      |I_V@60 delta| < 0.005 per pattern, median within 0.5yr, at both
      budgets (bit-exact hooks claim at experiment scale).

Falsifies: P1 failing kills the potentiation-breaks-the-equilibrium
story (and with it the AI-Scientist's enhancement premise in this
stack). P2 failing kills the correction-coupling claim. P3 failing
kills the jump-axis attribution of B's deficit. P6 failing means the
equilibrium's mortality side is untouchable from the corruption side.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec, quantize
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.exp23_multi_pattern import (
    ZONES, JUMP_MULT, HAZARD_BOOST, GROUPS, MULTI_TARGET, ZONE_MASK,
    MultiPatternCohort, _per_individual, _zone_write,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp24_potentiation.json"
EXP23 = "results/exp23_multi_pattern.json"

K, YEARS, SEEDS = 200, 120.0, (21, 22, 23)
CHECKUP, FROM_AGE = 5.0, 30.0
BUDGETS = (1, 6)

ARMS = {                      # name -> potentiation spec
    "plain":    {"factor": None},
    "pot05":    {"factor": 0.5,  "window": 5.0},
    "pot025":   {"factor": 0.25, "window": 5.0},
    "pot_rand": {"factor": 0.25, "window": 5.0, "random": True},
    "pot_perm": {"factor": 0.25, "window": float("inf")},
    "w2":       {"factor": 0.25, "window": 2.0},
    "w10":      {"factor": 0.25, "window": 10.0},
}
SWEEP_BUDGETS = {"w2": (6,), "w10": (6,)}     # window arms at b6 only
LEDGER_AT = np.arange(10.0, YEARS + 1, 10.0)
METRICS = ("I_V", "I_anchor", "I_recoverable")


def _p(s):
    print(s, flush=True)


class PotentiationCohort(MultiPatternCohort):
    """exp23's multi-pattern cohort + the maintenance write-mask capture
    that makes potentiation correction-coupled (no RNG consumption)."""

    def on_write(self, do: np.ndarray) -> None:
        if getattr(self, "_capture", False):
            prev = getattr(self, "_captured_do", None)
            self._captured_do = do.copy() if prev is None else (prev | do)
        super().on_write(do)


def build24(seed: int) -> PotentiationCohort:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **REGIME)
    ch = PotentiationCohort(K=K, params=params, seed=seed,
                            death_semantics="broadcast", latch="v2",
                            protect_written=True, jump_rate=0.006,
                            f_crit=0.655)
    ch._tgt = fidelity_target()
    ch.jump_mult = JUMP_MULT
    ch.hazard_boost = HAZARD_BOOST
    return ch


def _random_mask_like(cohort, do: np.ndarray, rng: np.random.Generator):
    """The AI-Scientist's random-pattern control: same number of
    (animal, cluster) pairs as the real write, uniformly random
    placement among alive animals (a separate RNG stream — the cohort's
    draws are untouched)."""
    cl = cohort.cluster_len
    C = cohort.n_clusters
    rows, cols = np.nonzero(do)
    pairs = list(zip(rows.tolist(), (cols // cl).tolist()))
    n = len(pairs)
    if n == 0:
        return None
    alive = np.nonzero(cohort.alive)[0]
    if len(alive) == 0:
        return None
    space = len(alive) * C
    idx = rng.choice(space, size=min(n, space), replace=False)
    out = np.zeros_like(do)
    for j in idx:
        k = int(alive[j // C])
        c = int(j % C)
        out[k, c * cl:(c + 1) * cl] = True
    return out


def run_arm(arm: str, seed: int, budget: int) -> dict:
    spec = ARMS[arm]
    ch = build24(seed)
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=budget,
                          levels=7, target_source="anchored")
    rng_local = np.random.default_rng(10000 + 7919 * seed)
    written = {"done": False}
    seen = set()
    series = {m: {p: [] for p in ("A", "B", "C")} for m in METRICS}
    cov_series = []
    pot_pairs = {"n": 0, "calls": 0}
    boot60, alive60 = {}, {}

    def maintain(t, cohort):
        if not written["done"] and t >= 5.0:
            written["done"] = True
            for name in ("A", "B", "C"):
                _zone_write(cohort, name)
            cohort._tgt = MULTI_TARGET
        if t >= FROM_AGE - 1e-9 and abs((t - FROM_AGE) % CHECKUP) <= 0.26:
            if spec["factor"] is None:
                codec.maintain(cohort, age_preset(t), mode="codec")
            else:
                cohort._capture = True
                codec.maintain(cohort, age_preset(t), mode="codec")
                cohort._capture = False
                do = getattr(cohort, "_captured_do", None)
                cohort._captured_do = None
                if do is not None and do.any():
                    if spec.get("random"):
                        do = _random_mask_like(cohort, do, rng_local)
                    if do is not None and do.any():
                        n = cohort.potentiate(
                            do, window=spec["window"],
                            factor=spec["factor"])
                        pot_pairs["n"] += int(n)
                        pot_pairs["calls"] += 1
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                specs = [(nm, MULTI_TARGET,
                          ZONE_MASK[(ZONES[nm][0], ZONES[nm][1])])
                         for nm in ("A", "B", "C")]
                led = cohort.pattern_ledgers(specs)
                for nm in ("A", "B", "C"):
                    for m in METRICS:
                        series[m][nm].append(led[nm][m])
                until = getattr(cohort, "_pot_until", None)
                if until is None:
                    cov_series.append(0.0)
                else:
                    active = (cohort.t < until)
                    alive = cohort.alive
                    cov = float(active[alive].mean()) if alive.any() else 0.0
                    cov_series.append(cov)
                if abs(a - 60.0) < 0.13:
                    for nm, ref, zone in specs:
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
    s["restored"] = codec.restored
    s["pot_pairs"] = pot_pairs["n"]
    s["pot_calls"] = pot_pairs["calls"]
    s["coverage"] = cov_series
    ht = np.asarray(s["hist_t"], float)
    ha = np.asarray(s["hist_alive"], float)
    s["alive_frac_60"] = float(ha[np.argmin(np.abs(ht - 60.0))])
    s["alive_frac_100"] = float(ha[np.argmin(np.abs(ht - 100.0))])
    return s


def _at(rows, metric, key, age=60.0) -> float:
    vals = []
    for r in rows:
        s_ = r["series"][metric][key]
        if s_:
            la = np.asarray(LEDGER_AT[:len(s_)], float)
            m = np.abs(la - age) < 0.2
            v = np.asarray(s_, float)[m]
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
        "pot_pairs": float(np.mean([r["pot_pairs"] for r in rows])),
        "coverage_mean": float(np.mean(
            [np.mean(r["coverage"]) for r in rows])),
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
    entry["curves"] = {
        m: {nm: [float(np.nanmean(x)) for x in zip(
            *[r["series"][m][nm] for r in rows])]
            for nm in ("A", "B", "C")}
        for m in METRICS}
    if rows[0]["boot60"]:
        from cultivation.validation.stats import bootstrap_ci
        entry["ci95_IV_at_60"] = {
            nm: bootstrap_ci(np.mean, np.concatenate(
                [r["boot60"][nm] for r in rows if nm in r["boot60"]]))
            for nm in ("A", "B", "C")
            if any(nm in r["boot60"] for r in rows)}
    return entry


def _budgets_for(arm: str):
    return SWEEP_BUDGETS.get(arm, BUDGETS)


def main() -> dict:
    t0 = time.time()
    _p("exp24 — memory POTENTIATION (the AI-Scientist's idea #2, "
       "strategy 3)")
    _p(f"    budgets {BUDGETS} (+window sweep w2/w10 at b6); "
       f"K={K}, {YEARS:.0f}yr, seeds {SEEDS}")
    out = {}
    for arm in ARMS:
        out[arm] = {}
        for b in _budgets_for(arm):
            rows = [run_arm(arm, sd, b) for sd in SEEDS]
            out[arm][b] = _aggregate(arm, b, rows)
            e = out[arm][b]
            _p(f"    {arm:9s} b={b}: median {e['median']:6.1f}  "
               f"A {e['I_V_at_60']['A']:5.3f}  "
               f"B {e['I_V_at_60']['B']:5.3f}  "
               f"C {e['I_V_at_60']['C']:5.3f}  "
               f"restored {e['restored']:.0f}  "
               f"pot {e['pot_pairs']:.0f}  "
               f"cov {e['coverage_mean']:.2f}")

    pl1, pl6 = out["plain"][1], out["plain"][6]
    d_b = {b: out["pot025"][b]["I_V_at_60"]["B"] - pl["I_V_at_60"]["B"]
           for b, pl in ((1, pl1), (6, pl6))}
    d_a = out["pot025"][6]["I_V_at_60"]["A"] - pl6["I_V_at_60"]["A"]
    d_c = out["pot025"][6]["I_V_at_60"]["C"] - pl6["I_V_at_60"]["C"]
    # R: exp23's published default arm
    with open(EXP23) as f:
        e23 = json.load(f)["arms"]["default"]
    r_ok, r_detail = True, []
    for b in BUDGETS:
        for nm in ("A", "B", "C"):
            d = abs(out["plain"][b]["I_V_at_60"][nm]
                    - e23[str(b)]["I_V_at_60"][nm])
            r_detail.append(round(d, 6))
            r_ok &= d < 0.005
        r_ok &= abs(out["plain"][b]["median"]
                    - e23[str(b)]["median"]) < 0.5

    crit = {
        "P1_equilibrium_shift": bool(d_b[6] > 0.046),
        "P2_gating": bool(
            out["pot_rand"][1]["I_V_at_60"]["B"]
            <= pl1["I_V_at_60"]["B"] + 0.01
            and out["pot_rand"][6]["I_V_at_60"]["B"]
            <= pl6["I_V_at_60"]["B"] + 0.01),
        "P3_dissociation": bool(d_b[6] > d_c and d_b[6] > d_a),
        "P4_budget_coupling": bool(d_b[6] > d_b[1]),
        "P5_dose_response": bool(
            out["pot025"][6]["I_V_at_60"]["B"]
            >= out["pot05"][6]["I_V_at_60"]["B"] - 0.01
            and out["pot05"][6]["I_V_at_60"]["B"]
            > pl6["I_V_at_60"]["B"]),
        "P6_lifespan": bool(
            out["pot025"][1]["median"] > pl1["median"]
            and out["pot025"][6]["median"] > pl6["median"]),
        "P7_ceiling_perm": bool(
            out["pot_perm"][6]["I_V_at_60"]["B"]
            - pl6["I_V_at_60"]["B"] > 0.046),
        "R_regression_vs_exp23": bool(r_ok),
    }
    w_order = (out["w10"][6]["I_V_at_60"]["B"]
               >= out["pot025"][6]["I_V_at_60"]["B"] - 0.01
               and out["pot025"][6]["I_V_at_60"]["B"]
               >= out["w2"][6]["I_V_at_60"]["B"] - 0.01)

    results = {
        "exp": "exp24_potentiation",
        "source_idea": "AI-Scientist trial idea #2 memory_enhancement_"
                       "protocols strategy 3 (426f320); stack hook: "
                       "FidelityAgingCohort.potentiate / _pot_until",
        "arms": out,
        "criteria": crit,
        "window_ordering_holds": bool(w_order),
        "deltas_vs_plain": {"B_b1": d_b[1], "B_b6": d_b[6],
                            "A_b6": d_a, "C_b6": d_c},
        "r_detail_max_iv_delta": max(r_detail),
        "exp23_reference": "plain arm must replicate exp23's default "
                           "(same seeds/geometry; potentiation hooks "
                           "unused)",
        "adaptation_note": "strategies 1-2 of the idea (amplitude "
                           "consolidation / reinforcement) not "
                           "implemented: the pattern is discrete "
                           "symbols — amplitude is not a corruption "
                           "axis in this stack; strategy 3 (jump-"
                           "probability reduction) is the only one "
                           "that maps onto the corruption physics",
        "module_history": "design probe (machinery validation, recorded "
                          "before pre-registration): 1 seed, b6, pot025 "
                          "vs plain — delta_B +0.003, delta_C +0.004, "
                          "delta_A +0.002, coverage@60 0.131: the "
                          "transient effect is REAL but coverage-capped "
                          "(window = cadence protects only last-cycle "
                          "corrections, ~13% of clusters). The probe "
                          "motivated P7 (the permanent-potentiation "
                          "ceiling criterion) BEFORE the full run; the "
                          "window sweep w2/w5/w10 was already in the "
                          "design to decompose exactly this coverage "
                          "geometry",
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    _p(f"    W window ordering (w10>=w5>=w2-0.01): "
       f"{'holds' if w_order else 'violated'}")
    _p(f"    deltas B: b1 {d_b[1]:+.3f}  b6 {d_b[6]:+.3f}   "
       f"A b6 {d_a:+.3f}  C b6 {d_c:+.3f}")
    _figure(results)
    _p(f"exp24 complete in {time.time()-t0:.0f}s")
    return results


def _figure(results: dict) -> None:
    setup()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4),
                           constrained_layout=True)
    pcol = {"A": PALETTE["good"], "B": PALETTE["accent"],
            "C": PALETTE["warn"]}

    # (a) dose-response + controls: B's I_V@60 at b6
    names = ["plain", "pot05", "pot025", "pot_rand", "pot_perm"]
    vals = [results["arms"][n][6]["I_V_at_60"]["B"] for n in names]
    cols = ["0.5", PALETTE["accent"], PALETTE["good"], PALETTE["warn"],
            "0.3"]
    ax[0].bar(range(len(names)), vals, color=cols, width=0.62)
    ax[0].set_xticks(range(len(names)))
    ax[0].set_xticklabels(names, rotation=25, fontsize=8)
    ax[0].set(ylabel="B I_V @ 60", ylim=(0, 1.0),
              title="dose-response + gating (budget 6)")
    for i, v in enumerate(vals):
        ax[0].text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=7)

    # (b) window sweep at b6 (factor 0.25)
    wn = ["w2", "pot025", "w10"]
    wv = [results["arms"][n][6]["I_V_at_60"]["B"] for n in wn]
    ax[1].plot(range(3), wv, "o-", color=PALETTE["good"], lw=2.2)
    for i, v in enumerate(wv):
        ax[1].annotate(f"{v:.3f}", (i, v), textcoords="offset points",
                       xytext=(0, 8), ha="center", fontsize=8)
    ax[1].set_xticks(range(3))
    ax[1].set_xticklabels(["2yr", "5yr", "10yr"])
    ax[1].set(xlabel="potentiation window (cadence = 5yr)",
              ylabel="B I_V @ 60", ylim=(0, 1.0),
              title="the coverage-geometry dial")

    # (c) delta by pattern at b6 + budget coupling
    d = results["deltas_vs_plain"]
    bars = [("B b1", d["B_b1"]), ("B b6", d["B_b6"]),
            ("A b6", d["A_b6"]), ("C b6", d["C_b6"])]
    ax[2].bar([b[0] for b in bars], [b[1] for b in bars],
              color=[PALETTE["accent"], PALETTE["accent"],
                     PALETTE["good"], PALETTE["warn"]], width=0.55)
    ax[2].axhline(0, color="k", lw=0.6)
    ax[2].axhline(0.046, color="r", lw=1.0, ls="--",
                  label="P1 threshold (2x allocation ceiling)")
    ax[2].set(ylabel="delta I_V@60 vs plain",
              title="pattern dissociation + budget coupling")
    ax[2].legend(fontsize=8)

    fig.suptitle("exp24 — memory potentiation vs the death-restoration "
                 "equilibrium", fontsize=12)
    fig.savefig(fig_path("fig21_potentiation"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig21_potentiation.png")


if __name__ == "__main__":
    main()
