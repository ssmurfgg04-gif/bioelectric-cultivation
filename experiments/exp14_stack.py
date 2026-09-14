"""EXP14 — Phase D: the integrated stack, end-to-end on a HELD-OUT corpus.

THE TOWER (each layer discovered/validated in its own phase, none ever
tuned on the held-out regime):

  L5  consciousness-body interface   exp12   the noreward/bistable retention
      physics that makes the somatic-memory layer a TRUSTED write target
      (bistable, re-writable, hopping-bounded) + the passive-decay law
  L4  latching somatic memory        exp11   patterns persist indefinitely;
      written states latch in; corruption beyond the deadzone sticks
  L3  CEM-discovered policy          exp10   the intervention schedule
      (loaded from its results JSON — never re-searched here)
  L2  verified codec                 exp8    consensus-then-archive
      maintenance; THE GATE
  L1  fidelity-dependent mortality   exp8    aging = pattern information loss

THE HELD-OUT CORPUS (never seen by ANY phase):
  kappa 0.017, lambda_gap 0.026, jump_rate 0.006, f_crit 0.655,
  K=300, years=170, seeds 51/52/53 — no phase tuned, searched, or
  validated on this regime or seed family.

  D1 THE GATE HOLDS        hand+codec beats hand+local (the exp8 gate,
                           transferred).
  D2 THE POLICY WINS       the exp10 discovered policy (loaded, frozen —
                           natively noreward) beats the hand-built schedule.
  D3 THE LATCH COMPOSES    + LatchingAgingCohort beats the latch-less
                           stack (writes latch in; slow erosion absorbed).
  D4 NOREREWARD TOLERANCE  the stack under passive policy decay (the
                           exp12 hook): degrades gracefully, does not
                           collapse (the latch carries what was written).

  D5 CEM vs GA BENCHMARK   fresh head-to-head at EXACTLY MATCHED budget
                           (140 fitness evals each: GA pop 20 + 6 gens
                           x 20 = 140; CEM 7 iters x 20 = 140; CRN seeds
                           11/12, same bounds/fitness): Hazan & Levin's
                           GA as 'a first step'; the CEM as the next.
                           Metrics: final best,
                           area-under-convergence (sample efficiency),
                           evals to 95% of final.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, LatchingAgingCohort,
)
from cultivation.inverse.cem import cem_optimize
from cultivation.inverse.ga import ga_optimize
from cultivation.inverse.design import (
    POLICY_BOUNDS, HAND_CODEC, decode_policy, eval_policy,
)
from experiments.exp8_fidelity import (
    fidelity_target, REGIME, age_preset, run_condition,
)
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

STATE = "scripts_dev/exp14_state.json"

# the held-out corpus
HELDOUT_REGIME = dict(REGIME)
HELDOUT_REGIME.update(kappa_noise=0.017, lambda_gap=0.026)
HELDOUT_COHORT = dict(jump_rate=0.006, f_crit=0.655)
HELDOUT_SEEDS = (51, 52, 53)
HELDOUT_K = 300
HELDOUT_YEARS = 170.0
DECAY_TAU = 80.0

# matched-budget search settings (D5)
POP, ITERS = 20, 7
CRN_SEEDS = (11, 12)


def _p(s):
    print(s, flush=True)


# ------------------------------------------------------------------- D1-D4
def run_stack(results: dict) -> dict:
    _p("  D1-D4: the integrated stack on the HELD-OUT corpus...")
    exp10 = json.load(open("results/exp10_inverse_design.json"))
    u_disc = np.array(exp10["discovered_u"])

    arms = {}

    # ---- baseline arms via exp8's machinery (hand-built schedules)
    for cond in ("none", "local", "codec"):
        ms = [run_condition(cond, seed=s, regime=HELDOUT_REGIME,
                            K=HELDOUT_K, years=HELDOUT_YEARS,
                            cohort_kw=HELDOUT_COHORT)["median"]
              for s in HELDOUT_SEEDS]
        arms[f"hand_{cond}"] = {
            "medians_by_seed": [float(m) for m in ms],
            "median": float(np.mean(ms))}
        _p(f"    hand/{cond:6s}: median {np.mean(ms):6.1f} yr "
           f"(seeds {[round(m) for m in ms]})")

    # ---- the discovered policy (loaded, frozen — natively noreward)
    kw = dict(K=HELDOUT_K, years=HELDOUT_YEARS, regime=HELDOUT_REGIME,
              target0=fidelity_target, age_preset=age_preset,
              cohort_kw=HELDOUT_COHORT)

    def policy_arm(label, **extra):
        ms, det = [], []
        for s in HELDOUT_SEEDS:
            r = eval_policy(u_disc, seed=s, **kw, **extra)
            ms.append(r["median"])
            det.append({"writes": r["writes"], "regens": r["regens"],
                        "boost_apps": r["boost_apps"]})
        arms[label] = {"medians_by_seed": [float(m) for m in ms],
                       "median": float(np.mean(ms)),
                       "writes": float(np.mean([d["writes"] for d in det])),
                       "regens": float(np.mean([d["regens"] for d in det]))}
        _p(f"    {label:16s}: median {np.mean(ms):6.1f} yr "
           f"(seeds {[round(m) for m in ms]})")

    policy_arm("disc_codec")
    policy_arm("disc_decay", decay_tau=DECAY_TAU)   # the noreward arm

    # ---- L3/L4 DIAGNOSTIC TABLE (the honest negative, fully diagnosed):
    # the latch layer's integration attempts + the decisive ablation
    _p("  D3 diagnostics: the latch layer vs the aging stack...")

    def run_latch(u, latch_kw=None):
        ck = dict(HELDOUT_COHORT)
        ck.update(latch_kw or {})
        ms = []
        for s in HELDOUT_SEEDS:
            r = eval_policy(u, seed=s, K=HELDOUT_K, years=HELDOUT_YEARS,
                            regime=HELDOUT_REGIME, target0=fidelity_target,
                            age_preset=age_preset, cohort_kw=ck,
                            cohort_cls=LatchingAgingCohort)
            ms.append(r["median"])
        return float(np.mean(ms))

    latch_diag = {
        "hand_latch": run_latch(np.array(HAND_CODEC)),
        "disc_latch": run_latch(u_disc),
        "hand_latch_deadzone0": run_latch(np.array(HAND_CODEC),
                                           {"deadzone": 0.0}),
    }
    for k, v in latch_diag.items():
        _p(f"    {k:22s}: median {v:6.1f} yr")

    gate = arms["hand_codec"]["median"] / arms["hand_local"]["median"]
    policy_gain = arms["disc_codec"]["median"] / arms["hand_codec"]["median"]
    policy_vs_none = arms["disc_codec"]["median"] / arms["hand_none"]["median"]
    stack_gain = arms["disc_codec"]["median"] / arms["hand_local"]["median"]
    decay_cost = arms["disc_decay"]["median"] / arms["disc_codec"]["median"]
    latch_cost = latch_diag["hand_latch"] / arms["hand_codec"]["median"]
    latch_dz0 = latch_diag["hand_latch_deadzone0"] / arms["hand_codec"]["median"]

    _p(f"    GATE (hand codec/local)        x{gate:.3f}")
    _p(f"    POLICY vs none                 x{policy_vs_none:.3f}")
    _p(f"    POLICY vs hand (strict)        x{policy_gain:.3f}")
    _p(f"    STACK vs pre-gate              x{stack_gain:.3f}")
    _p(f"    DECAY cost (noreward)          x{decay_cost:.3f}")
    _p(f"    LATCH cost (naive)             x{latch_cost:.3f}  "
       f"(deadzone-0 ablation x{latch_dz0:.3f} — neutral)")

    c = results.setdefault("criteria", {})
    c["D1_gate_holds_heldout"] = bool(gate >= 1.03)
    c["D2_policy_beats_baseline"] = bool(policy_vs_none >= 1.3)
    c["D2b_policy_beats_hand_strict"] = bool(policy_gain >= 1.03)
    c["D3_latch_composes"] = bool(latch_cost >= 0.98)
    c["D4_noreward_tolerant"] = bool(decay_cost >= 0.80)

    out = {"arms": arms, "latch_diagnostics": latch_diag,
           "gains": {"gate": gate, "policy_vs_none": policy_vs_none,
                     "policy_vs_hand": policy_gain, "full_stack": stack_gain,
                     "decay_cost": decay_cost, "latch_cost": latch_cost,
                     "latch_deadzone0_ablation": latch_dz0},
           "heldout": {"regime": HELDOUT_REGIME, "cohort": HELDOUT_COHORT,
                       "seeds": list(HELDOUT_SEEDS), "K": HELDOUT_K,
                       "years": HELDOUT_YEARS, "decay_tau": DECAY_TAU}}
    results["stack"] = out
    dump_json("integrated_stack_heldout.json", out)
    return out


# ------------------------------------------------------------------- D5
def _fitness(u):
    """exp10's exact search fitness: mean median over CRN seeds."""
    rs = [eval_policy(u, seed=s, K=150, years=110.0, regime=REGIME,
                      target0=fidelity_target, age_preset=age_preset)
          for s in CRN_SEEDS]
    return -float(np.mean([r["median"] for r in rs]))


def run_ga(state: dict) -> dict:
    _p("  D5a: GA baseline (fresh, exactly matched budget)...")
    t0 = time.time()
    # GA burns POP evals on its initial random population, so it gets
    # ITERS-1 generations to land on the SAME total budget: 20 + 6*20 = 140
    # fitness evals, identical to the CEM's 7 x 20 = 140.
    # ckpt: exact resume across wall-clock slices (sandboxed execution)
    with mp.Pool(2) as pool:
        u, f, hist = ga_optimize(_fitness, POLICY_BOUNDS, pop=POP,
                                 gens=ITERS - 1, seed=7, verbose=True,
                                 pool=pool,
                                 checkpoint="scripts_dev/exp14_ga.ckpt")
    state["ga"] = {"u": [float(x) for x in u], "best": float(-f),
                   "history": hist, "wall_s": time.time() - t0}
    json.dump(state, open(STATE, "w"), indent=1)
    _p(f"    GA final best median {-f:.1f} yr ({time.time() - t0:.0f}s)")
    return state["ga"]


def run_cem(state: dict) -> dict:
    _p("  D5b: CEM (fresh, exactly matched budget)...")
    t0 = time.time()
    with mp.Pool(2) as pool:
        u, f, hist = cem_optimize(_fitness, POLICY_BOUNDS, pop=POP,
                                  iters=ITERS, seed=7, verbose=True,
                                  pool=pool,
                                  checkpoint="scripts_dev/exp14_cem.ckpt")
    curve = [(POP * (it + 1), -float(bestf)) for it, bestf, _mu in hist]
    state["cem"] = {"u": [float(x) for x in u], "best": float(-f),
                    "curve": curve, "wall_s": time.time() - t0}
    json.dump(state, open(STATE, "w"), indent=1)
    _p(f"    CEM final best median {-f:.1f} yr ({time.time() - t0:.0f}s)")
    return state["cem"]


def benchmark_report(results: dict, state: dict) -> dict:
    _p("  D5c: CEM vs GA benchmark report...")
    ga, cem = state["ga"], state["cem"]
    ga_curve = [(h["evals"], -h["best"]) for h in ga["history"]]
    cem_curve = cem["curve"]

    def auc(curve, n_evals=POP * ITERS):
        """Area under the best-so-far curve (sample efficiency).

        Convention: the first observed best is extended back to x=0, so
        the ENTIRE budget is integrated (the old version integrated only
        from the first eval point but divided by the full budget,
        undercounting both algorithms by the first batch's width)."""
        xs = [0] + [x for x, _ in curve]
        ys = [curve[0][1]] + [y for _, y in curve]
        if xs[-1] < n_evals:  # extend to the full budget
            xs.append(n_evals)
            ys.append(curve[-1][1])
        return float(np.trapezoid(ys, xs) / n_evals)

    def evals_to(curve, target):
        for x, y in curve:
            if y >= target:
                return int(x)
        return None

    target95 = 0.95 * max(cem["best"], ga["best"])
    out = {
        "budget_evals": POP * ITERS, "crn_seeds": list(CRN_SEEDS),
        "ga": {"best_median": ga["best"], "auc": auc(ga_curve),
               "evals_to_95pct": evals_to(ga_curve, target95),
               "final_mean_pop": -ga["history"][-1]["mean"],
               "wall_s": ga["wall_s"]},
        "cem": {"best_median": cem["best"], "auc": auc(cem_curve),
                "evals_to_95pct": evals_to(cem_curve, target95),
                "wall_s": cem["wall_s"]},
        "ga_curve": ga_curve, "cem_curve": cem_curve,
    }
    _p(f"    GA : best {ga['best']:.1f}  AUC {out['ga']['auc']:.1f}  "
       f"evals->95% {out['ga']['evals_to_95pct']}")
    _p(f"    CEM: best {cem['best']:.1f}  AUC {out['cem']['auc']:.1f}  "
       f"evals->95% {out['cem']['evals_to_95pct']}")
    c = results.setdefault("criteria", {})
    c["D5_cem_sample_efficiency"] = bool(
        out["cem"]["auc"] > out["ga"]["auc"])
    c["D5_cem_final_not_worse"] = bool(
        cem["best"] >= 0.98 * ga["best"])
    results["benchmark"] = out
    dump_json("cem_vs_ga_benchmark.json", out)
    return out


# ----------------------------------------------------------------- figure
def make_figure(results: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0),
                             constrained_layout=True)
    ax = axes[0]
    arms = results["stack"]["arms"]
    order = ["hand_none", "hand_local", "hand_codec", "disc_codec",
             "disc_decay"]
    labels = ["none", "hand+local\n(pre-gate)", "hand+codec\n(exp8 gate)",
              "disc policy\n(exp10, frozen)", "+ passive decay\n(noreward)"]
    vals = [arms[a]["median"] for a in order]
    colors = [PALETTE["muted"], PALETTE["muted"], PALETTE["primary"],
              PALETTE["line2"], PALETTE["warn"]]
    ax.bar(range(len(order)), vals, color=colors)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("median lifespan (yr)")
    ax.set_title(f"The tower on the held-out corpus\n"
                 f"(full stack x{results['stack']['gains']['full_stack']:.2f} "
                 f"vs pre-gate)")
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=7)

    ax = axes[1]
    b = results["benchmark"]
    gx = [x for x, _ in b["ga_curve"]]
    gy = [y for _, y in b["ga_curve"]]
    cx = [x for x, _ in b["cem_curve"]]
    cy = [y for _, y in b["cem_curve"]]
    ax.step(gx, gy, where="post", color=PALETTE["accent"], label="GA")
    ax.step(cx, cy, where="post", color=PALETTE["primary"], label="CEM")
    ax.set_xlabel("policy evaluations (common random numbers)")
    ax.set_ylabel("best median lifespan found (yr)")
    ax.set_title("CEM vs GA — matched budget (140 evals)")
    ax.legend(frameon=False, fontsize=8)

    fig.savefig(fig_path("fig14_stack.png"))
    plt.close(fig)


# ------------------------------------------------------------------- main
def main(stage: str = "all") -> dict:
    setup()
    t0 = time.time()
    print("[exp14] Phase D — the integrated stack on held-out physics")
    results: dict = {}
    try:
        state = json.load(open(STATE))
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}

    if stage in ("all", "stack"):
        run_stack(results)
    elif stage in ("ga", "cem", "report"):
        # the D1-D4 held-out arms were already computed and dumped by the
        # 'stack' stage; load them instead of re-running the expensive arms
        try:
            results["stack"] = json.load(
                open("results/integrated_stack_heldout.json"))
            g = results["stack"]["gains"]
            c = results.setdefault("criteria", {})
            c["D1_gate_holds_heldout"] = bool(g["gate"] >= 1.03)
            c["D2_policy_beats_baseline"] = bool(g["policy_vs_none"] >= 1.3)
            c["D2b_policy_beats_hand_strict"] = bool(g["policy_vs_hand"] >= 1.03)
            c["D3_latch_composes"] = bool(g["latch_cost"] >= 0.98)
            c["D4_noreward_tolerant"] = bool(g["decay_cost"] >= 0.80)
        except FileNotFoundError:
            _p("  [report] no cached held-out stack — run stage 'stack' first")
    if stage in ("all", "ga"):
        if "ga" not in state:
            run_ga(state)
        results["_ga_loaded"] = True
    if stage in ("all", "cem"):
        if "cem" not in state:
            run_cem(state)
    if stage in ("all", "report"):
        if "ga" not in state or "cem" not in state:
            _p("  [report] missing search state — run stages ga/cem first")
        else:
            benchmark_report(results, state)

    if "stack" in results and "benchmark" in results:
        for k, v in results["criteria"].items():
            _p(f"  {k}: {'PASS' if v else 'NEGATIVE'}")
        results["honest_notes"] = [
            "The held-out corpus (kappa 0.017, lambda 0.026, jump 0.006, "
            "f_crit 0.655, seeds 51-53) was never used by any phase: not "
            "exp8's validation, not exp10's search/heldout/perturbed "
            "regimes, not exp13's sweeps.",
            "The discovered policy is LOADED from exp10's results JSON and "
            "run FROZEN — the stack is natively noreward (a fixed schedule "
            "executing on latch-backed tissue; no runtime adaptation "
            "anywhere).",
            "The exp12 layer enters as physics, not machinery: the latch's "
            "bistability/rewritability laws (B6) are what make the "
            "LatchingAgingCohort's writes trustworthy, and the D4 decay "
            "arm is exp12's passive-decay law applied to the policy's "
            "amplitude.",
            "D5 runs BOTH algorithms fresh at exactly matched budget "
            "(140 evals each, CRN seeds 11/12, identical fitness/bounds) "
            "— the comparison measures the search algorithm, not tuning "
            "effort.",
            "D5 honest reading: on THIS landscape the sample-efficiency "
            "criterion is NEGATIVE — the GA's initial uniform draw already "
            "contains a ~93.5-yr policy (the attainable plateau is broad), "
            "so its best-so-far curve is flat from eval 20 (AUC 93.6 vs "
            "CEM 91.0). The CEM still lands slightly higher on final best "
            "(94.1 vs 93.9) and exp10's own 280-eval CEM search plateaued "
            "at 93.1 — the landscape saturates near ~94 for BOTH "
            "algorithms, ~+19% above the best hand-built policy (81.9). "
            "The honest claim is NOT 'CEM is more sample-efficient than "
            "GA'; it is 'inverse design (either algorithm) beats hand "
            "design by ~19%, and on broad-plateau landscapes adaptive "
            "sampling gains little over uniform sampling at small "
            "budgets.'",
            "D2b honest reading: the discovered policy LOSES to the "
            "hand-built codec arm on the held-out corpus (111 vs 124) "
            "while WINNING on its search regime (93 vs 82). The "
            "hand-policy has no regeneration (regen_start 105 = never); "
            "the discovered one regenerates from age 74 — on the milder "
            "held-out physics the pure-maintenance arm simply outlives "
            "any regen schedule's procedure hazard. The search found the "
            "optimum of ITS regime; regimes differ; transfer is real but "
            "imperfect (exp10 T4.3: +3.4% perturbed-regime gain).",
            "D3 honest reading: grafting the latch layer onto the aging "
            "stack COSTS ~20% of lifespan (99.4 vs 124.3 under the "
            "hand-codec policy; deadzone-0 ablation recovers only to "
            "106.7). The latch's anchor-pinning fights the codec's "
            "maintenance writes on senesced cells (a stably-depolarized "
            "senesced cell re-latches its OWN wrong anchor within weeks "
            "unless the write hook fires first) — the two layers are not "
            "yet semantically aligned. The stack reported in D1/D2/D4 is "
            "the latch-LESS composition (exp8 cohort + exp10 policy + "
            "exp12 decay law); the latch composes cleanly in the "
            "morphology domain (exp11) but not yet in the aging domain. "
            "Recorded as the tower's open joint.",
        ]
        make_figure(results)
        path = dump_json("exp14_stack.json", results)
        _p(f"[exp14] results -> {path}  ({time.time() - t0:.0f}s)")
    return results


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
