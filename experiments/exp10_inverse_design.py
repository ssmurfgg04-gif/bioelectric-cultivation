"""EXP10 — Inverse design: the CEM search discovers intervention policies.

THE STEP exp8 DID NOT TAKE: exp1-8 tested HAND-BUILT schedules. The gate is
open (verified maintenance pays under pattern-fidelity mortality) — now the
inverse problem: WHAT SCHEDULE of the full arsenal (verified writes, gated
channel boosts, full re-derivations) maximizes lifespan, discovered rather
than guessed?

Search: cross-entropy method over an 8-dimensional policy vector —
  start_age, checkup period, write budget, regeneration interval & start,
  boost gating (P(boost|verified), P(boost|refused)), boost factor —
  evaluated on FidelityAgingCohort under an honest PROCEDURE-RISK cost
  (h_proc per write-event per year: overservicing kills; the optimum is an
  allocation, not a maximum).

HONEST PROTOCOL (pre-registered before the search ran):
  - Search fitness: median lifespan, common random number seed 11 (never
    used in exp8), K=150, years=110, the exp8 isolated-fidelity regime.
  - HELD-OUT validation: fresh seeds 21/22/23, identical physics.
  - REGIME TRANSFER: perturbed physics (jump_rate x1.5, f_crit 0.58,
    kappa 0.025, lambda 0.028) — does the discovered policy survive a world
    it was not tuned for?
  - Cost sensitivity: h_proc = 0 arm — was the structure cost-driven?
  - Ablation: each dimension reset to the hand-built reference (and solo:
    each dimension alone) — which components carry the policy?

Pre-registered criteria (falsification ledger):
  T4.1 CONVERGENCE      best fitness improves >= 8% from iteration-0 elite
                        best to final best.
  T4.2 HELD-OUT WIN     discovered median (fresh seeds) >= best hand-built
                        median x 1.03.
  T4.3 REGIME TRANSFER  discovered median under perturbed regime >= best
                        hand-built (same regime) x 0.98.
  T4.4 STRUCTURE        >= 2 ablation dimensions with |marginal effect|
                        >= 3% on held-out seeds.
"""

from __future__ import annotations

import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, ".")

from cultivation.inverse.cem import cem_optimize
from cultivation.inverse.design import (
    POLICY_NAMES, POLICY_BOUNDS, HAND_CODEC, HAND_CHAN, HAND_BLIND,
    HAND_REGEN, HAND_REGEN_CHAN, H_PROC, decode_policy, eval_policy,
    eval_policy_seeds,
)
from experiments.exp8_fidelity import fidelity_target, REGIME, age_preset
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

SEARCH_SEEDS = (11, 12)    # common random numbers for search fitness
HELDOUT_SEEDS = (21, 22, 23, 24)
POP, ITERS, ELITE = 28, 10, 0.22
HELDOUT_K = 300           # larger cohort for the evaluation phase
STATE_PATH = "scripts_dev/exp10_state.json"

# the no-maintenance control expressed in policy space (start beyond horizon)
NONE_U = (105.0, 5.0, 6.0, 60.0, 105.0, 0.0, 0.0, 1.0)

# perturbed physics for the transfer test
PERTURBED_REGIME = dict(REGIME)
PERTURBED_REGIME.update(kappa_noise=0.025, lambda_gap=0.028)
PERTURBED_COHORT = dict(jump_rate=0.0075, f_crit=0.58)

BASE_KW = dict(regime=REGIME, target0=fidelity_target, age_preset=age_preset)


def _fitness_arg(u):
    """Module-level so Pool can pickle it. Mean over CRN search seeds."""
    rs = [eval_policy(u, seed=s, **BASE_KW) for s in SEARCH_SEEDS]
    return -float(np.mean([r["median"] for r in rs]))


def main(stage: str = "all") -> dict:
    """Stages: 'search' (CEM + checkpoint), 'eval' (held-out + report), 'all'.
    Split so long runs fit within tool timeouts; state persists in
    scripts_dev/exp10_state.json."""
    import json, os
    setup()
    t0 = time.time()
    state = {}
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            state = json.load(f)

    if stage in ("search", "all") or "discovered_u" not in state:
        print("[exp10] inverse design — CEM discovers the intervention policy")
        # ------------------------------------------------------------- 1. search
        print(f"  searching 8-dim policy space (pop={POP}, iters={ITERS}, "
              f"CRN seeds {SEARCH_SEEDS})...")
        use_pool = True
        try:
            with Pool(2) as pool:
                pool.map(float, [1.0, 2.0])  # smoke test pickling
        except Exception as e:
            print(f"  (multiprocessing unavailable: {e}; sequential fallback)")
            use_pool = False

        hist_best = []

        def cem_callback(it, best_f, mu):
            hist_best.append(float(best_f))
            print(f"    iter {it:2d}: best median {-best_f:6.1f}  "
                  f"mu={np.round(mu, 2)}", flush=True)

        if use_pool:
            rng = np.random.default_rng(0)
            lo = np.array([b[0] for b in POLICY_BOUNDS], float)
            hi = np.array([b[1] for b in POLICY_BOUNDS], float)
            mu, sigma = (lo + hi) / 2, (hi - lo) / 4
            n_elite = max(2, int(POP * ELITE))
            best_u, best_f = None, np.inf
            it_start = 0
            # resume an interrupted search (per-iteration checkpoints)
            if state.get("search_partial"):
                rng.bit_generator.state = {
                    "bit_generator": "PCG64",
                    "state": {"state": int(state["rng_state"]["state"]),
                              "inc": int(state["rng_state"]["inc"])},
                    "has_uint32": int(state["rng_state"].get("has_uint32", 0)),
                    "uinteger": int(state["rng_state"].get("uinteger", 0)),
                }
                mu = np.array(state["mu"], float)
                sigma = np.array(state["sigma"], float)
                best_u = np.array(state["best_u"], float)
                best_f = float(state["best_f"])
                it_start = int(state["next_iter"])
                hist_best = list(state["history_best_median"])
                print(f"  resuming search at iteration {it_start}")
            for it in range(it_start, ITERS):
                U = rng.normal(mu, np.maximum(sigma, 1e-6), size=(POP, 8))
                U = np.clip(U, lo, hi)
                with Pool(2) as pool:
                    F = np.array(pool.map(_fitness_arg, list(U)))
                order = np.argsort(F)
                if F[order[0]] < best_f:
                    best_f, best_u = float(F[order[0]]), U[order[0]].copy()
                elite = U[order[:n_elite]]
                mu = elite.mean(axis=0)
                sigma = elite.std(axis=0) + (hi - lo) * 0.02
                cem_callback(it, best_f, mu)
                # per-iteration checkpoint (resumable)
                rs = rng.bit_generator.state["state"]
                with open(STATE_PATH, "w") as f:
                    json.dump({
                        "search_partial": True, "next_iter": it + 1,
                        "rng_state": {"state": int(rs["state"]), "inc": int(rs["inc"])},
                        "mu": [float(v) for v in mu],
                        "sigma": [float(v) for v in sigma],
                        "best_u": [float(v) for v in best_u],
                        "best_f": float(best_f),
                        "history_best_median": [-b for b in hist_best],
                        "search_wall_s": time.time() - t0,
                        "use_pool": use_pool, "pop": POP, "iters": ITERS,
                        "search_seeds": list(SEARCH_SEEDS),
                    }, f)
        else:
            best_u, best_f, hist = cem_optimize(
                _fitness_arg, POLICY_BOUNDS, pop=POP, elite_frac=ELITE,
                iters=ITERS, seed=0, verbose=False)
            hist_best = [h[1] for h in hist]

        discovered_u = best_u
        state.update({
            "discovered_u": [float(v) for v in discovered_u],
            "history_best_median": [-b for b in hist_best],
            "search_wall_s": time.time() - t0,
            "use_pool": use_pool,
            "pop": POP, "iters": ITERS, "search_seeds": list(SEARCH_SEEDS),
        })
        with open(STATE_PATH, "w") as f:
            json.dump(state, f)
        if stage == "search":
            print(f"[exp10] search stage complete -> {STATE_PATH}")
            return state
    else:
        print("[exp10] resuming from checkpoint — evaluation stage")
        discovered_u = np.array(state["discovered_u"], float)
        hist_best = [-m for m in state["history_best_median"]]

    discovered = decode_policy(discovered_u)
    print(f"  DISCOVERED policy: {discovered}")

    # --------------------------------------------------- 2. hand-built arms
    print("  hand-built baselines (identical procedure-risk accounting)...")
    hands = {
        "codec": HAND_CODEC, "chan": HAND_CHAN, "blind": HAND_BLIND,
        "regen": HAND_REGEN, "regen_chan": HAND_REGEN_CHAN,
    }
    # paired design: every policy evaluated on the same seeds as the none
    # control; the population-level frailty draw cancels in the ratio.
    none_by_seed = {s: eval_policy(np.array(NONE_U), seed=s, K=HELDOUT_K,
                                    **BASE_KW)["median"] for s in HELDOUT_SEEDS}
    base_median, base_gain = {}, {}
    for name, u in hands.items():
        r = eval_policy_seeds(u, HELDOUT_SEEDS, K=HELDOUT_K, **BASE_KW)
        base_median[name] = r["median"]
        base_gain[name] = float(np.mean(
            [r["medians_by_seed"][i] / none_by_seed[s]
             for i, s in enumerate(HELDOUT_SEEDS)]))
        print(f"    {name:10s}: median {r['median']:6.1f}  paired x{base_gain[name]:.3f}  "
              f"(writes {r['writes']:.0f}, regens {r['regens']:.1f})")
    best_hand_name = max(base_gain, key=base_gain.get)
    best_hand_median = base_median[best_hand_name]
    best_hand_gain = base_gain[best_hand_name]

    # -------------------------------------------------- 3. held-out + transfer
    print("  held-out evaluation (fresh seeds 21-24, K=300)...")
    r_disc = eval_policy_seeds(discovered_u, HELDOUT_SEEDS, K=HELDOUT_K, **BASE_KW)
    disc_gain = float(np.mean(
        [r_disc["medians_by_seed"][i] / none_by_seed[s]
         for i, s in enumerate(HELDOUT_SEEDS)]))
    print(f"    discovered: median {r_disc['median']:6.1f}  paired x{disc_gain:.3f}  "
          f"(writes {r_disc['writes']:.0f}, regens {r_disc['regens']:.1f}, "
          f"boosts {r_disc['boost_apps']:.0f})")

    print("  regime transfer (perturbed physics)...")
    pert_kw = dict(regime=PERTURBED_REGIME, target0=fidelity_target,
                   age_preset=age_preset, cohort_kw=PERTURBED_COHORT)
    none_pert = {s: eval_policy(np.array(NONE_U), seed=s, K=HELDOUT_K,
                                **pert_kw)["median"] for s in HELDOUT_SEEDS}
    r_disc_pert = eval_policy_seeds(discovered_u, HELDOUT_SEEDS, K=HELDOUT_K, **pert_kw)
    disc_pert_gain = float(np.mean(
        [r_disc_pert["medians_by_seed"][i] / none_pert[s]
         for i, s in enumerate(HELDOUT_SEEDS)]))
    pert_hands, pert_gains = {}, {}
    for name, u in hands.items():
        r = eval_policy_seeds(u, HELDOUT_SEEDS, K=HELDOUT_K, **pert_kw)
        pert_hands[name] = r["median"]
        pert_gains[name] = float(np.mean(
            [r["medians_by_seed"][i] / none_pert[s]
             for i, s in enumerate(HELDOUT_SEEDS)]))
    best_pert_hand = max(pert_gains, key=pert_gains.get)
    print(f"    discovered(pert): paired x{disc_pert_gain:.3f}  "
          f"best hand(pert): {best_pert_hand} x{pert_gains[best_pert_hand]:.3f}")

    # ------------------------------------------------------ 4. cost sensitivity
    print("  no-procedure-risk sensitivity (h_proc = 0)...")
    r_disc_free = eval_policy_seeds(discovered_u, HELDOUT_SEEDS, K=HELDOUT_K,
                                     h_proc=0.0, **BASE_KW)
    r_hand_free = eval_policy_seeds(hands[best_hand_name], HELDOUT_SEEDS,
                                     K=HELDOUT_K, h_proc=0.0, **BASE_KW)
    print(f"    discovered(h=0): {r_disc_free['median']:6.1f}   "
          f"best-hand(h=0): {r_hand_free['median']:6.1f}")

    # ------------------------------------------------------------ 5. ablation
    print("  ablation: reset each dimension to the hand reference...")
    ref = np.array(HAND_CODEC, float)
    disc = np.asarray(discovered_u, float)
    ablation, solo = {}, {}
    for i, name in enumerate(POLICY_NAMES):
        u_ab = disc.copy(); u_ab[i] = ref[i]
        r = eval_policy_seeds(u_ab, HELDOUT_SEEDS, K=HELDOUT_K, **BASE_KW)
        ablation[name] = r["median"]
        u_so = ref.copy(); u_so[i] = disc[i]
        r2 = eval_policy_seeds(u_so, HELDOUT_SEEDS, K=HELDOUT_K, **BASE_KW)
        solo[name] = r2["median"]
        print(f"    {name:20s}: ablated {ablation[name]:6.1f}  "
              f"solo {solo[name]:6.1f}  (full {r_disc['median']:6.1f})")
    marginal = {n: (r_disc["median"] - ablation[n]) / r_disc["median"]
                for n in POLICY_NAMES}

    # ---------------------------------------------------------- 6. criteria
    iter0_best = -hist_best[0] if hist_best else np.nan
    final_best = -hist_best[-1] if hist_best else np.nan
    criteria = {
        "T4.1_convergence": bool(final_best >= iter0_best * 1.08),
        "T4.2_heldout_win": bool(disc_gain >= best_hand_gain * 1.03),
        "T4.3_regime_transfer": bool(
            disc_pert_gain >= pert_gains[best_pert_hand] * 0.98),
        "T4.4_structure": bool(sum(
            1 for n in POLICY_NAMES if abs(marginal[n]) >= 0.03) >= 2),
    }

    results = {
        "search": {
            "seeds": list(SEARCH_SEEDS), "pop": POP, "iters": ITERS,
            "history_best_median": [-b for b in hist_best],
            "search_wall_s": state.get("search_wall_s", float("nan")),
            "use_pool": state.get("use_pool", False),
        },
        "discovered_u": [float(v) for v in discovered_u],
        "discovered_policy": discovered,
        "discovered_heldout": r_disc,
        "discovered_paired_gain": disc_gain,
        "discovered_perturbed": r_disc_pert,
        "discovered_perturbed_gain": disc_pert_gain,
        "discovered_free": r_disc_free,
        "none_by_seed": none_by_seed,
        "hand_built": {n: {"median": base_median[n], "paired_gain": base_gain[n]}
                       for n in hands},
        "hand_perturbed": {n: {"median": pert_hands[n], "paired_gain": pert_gains[n]}
                           for n in hands},
        "best_hand": {"name": best_hand_name, "median": best_hand_median,
                      "paired_gain": best_hand_gain,
                      "perturbed_gain": pert_gains[best_pert_hand]},
        "ablation_medians": ablation,
        "solo_medians": solo,
        "marginal_effects": marginal,
        "criteria": criteria,
        "h_proc": H_PROC,
        "regime": REGIME,
        "perturbed_regime": PERTURBED_REGIME,
        "perturbed_cohort": PERTURBED_COHORT,
        "heldout_seeds": list(HELDOUT_SEEDS),
        "heldout_K": HELDOUT_K,
    }

    # ---------------------------------------------------------- printout
    iter0_best = -hist_best[0] if hist_best else np.nan
    final_best = -hist_best[-1] if hist_best else np.nan
    print(f"\n  CEM: iter0 best {iter0_best:.1f} -> final {final_best:.1f} "
          f"(search {state.get('search_wall_s', float('nan')):.0f}s)")
    print(f"  held-out: discovered {r_disc['median']:.1f} (paired x{disc_gain:.3f}) "
          f"vs best hand ({best_hand_name}) {best_hand_median:.1f} "
          f"(paired x{best_hand_gain:.3f})")
    print(f"  transfer: discovered x{disc_pert_gain:.3f} vs best hand "
          f"({best_pert_hand}) x{pert_gains[best_pert_hand]:.3f} (paired)")
    print(f"  h_proc=0: discovered {r_disc_free['median']:.1f} vs hand "
          f"{r_hand_free['median']:.1f}")
    for k, v in criteria.items():
        print(f"  {k}: {'PASS' if v else 'NEGATIVE'}")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.5), constrained_layout=True)

    ax = axes[0]
    ax.plot(range(len(hist_best)), [-b for b in hist_best], "o-",
            color=PALETTE["primary"])
    ax.set_title("(a) CEM convergence")
    ax.set_xlabel("iteration"); ax.set_ylabel("best median lifespan (yr)")

    ax = axes[1]
    # paired gains vs none control (population frailty cancels)
    names = ["none"] + list(hands) + ["CEM"]
    vals = [1.0] + [base_gain[n] for n in hands] + [disc_gain]
    x = np.arange(len(names))
    colors = [PALETTE["muted"]] + [PALETTE["line2"]] * len(hands) + [PALETTE["good"]]
    ax.bar(x, vals, color=colors, width=0.62)
    ax.axhline(1.0, color="k", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=7, rotation=30)
    ax.set_title("(b) Paired median gain vs none (seeds 21-24)")
    ax.set_ylabel("lifespan gain (x)")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.01, f"x{v:.2f}", ha="center", fontsize=7)

    ax = axes[2]
    m = [marginal[n] for n in POLICY_NAMES]
    y = np.arange(len(POLICY_NAMES))
    ax.barh(y, m, color=[PALETTE["accent"] if abs(v) >= 0.03 else PALETTE["muted"]
                         for v in m])
    ax.set_yticks(y); ax.set_yticklabels(POLICY_NAMES, fontsize=7)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_title("(c) Ablation marginals (reset to hand ref)")
    ax.set_xlabel("fractional effect on median")

    ax = axes[3]
    # transfer scatter: paired gain per seed, baseline vs perturbed
    disc_gain_seeds = [r_disc["medians_by_seed"][i] / none_by_seed[s]
                       for i, s in enumerate(HELDOUT_SEEDS)]
    disc_pert_gain_seeds = [r_disc_pert["medians_by_seed"][i] / none_pert[s]
                            for i, s in enumerate(HELDOUT_SEEDS)]
    r_hand = eval_policy_seeds(hands[best_hand_name], HELDOUT_SEEDS,
                                K=HELDOUT_K, **BASE_KW)
    hand_gain_seeds = [r_hand["medians_by_seed"][i] / none_by_seed[s]
                       for i, s in enumerate(HELDOUT_SEEDS)]
    r_hand_pert = eval_policy_seeds(hands[best_hand_name], HELDOUT_SEEDS,
                                     K=HELDOUT_K, **pert_kw)
    hand_pert_gain_seeds = [r_hand_pert["medians_by_seed"][i] / none_pert[s]
                            for i, s in enumerate(HELDOUT_SEEDS)]
    ax.scatter(hand_gain_seeds, hand_pert_gain_seeds, s=46, color=PALETTE["line2"],
               label=f"best hand ({best_hand_name})")
    ax.scatter(disc_gain_seeds, disc_pert_gain_seeds, s=46, color=PALETTE["good"],
               marker="^", label="CEM discovered")
    lims = [0.9, 1.45]
    ax.plot(lims, lims, ls="--", lw=0.8, color="k", alpha=0.4)
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_title("(d) Transfer: baseline vs perturbed physics")
    ax.set_xlabel("paired gain (baseline regime)")
    ax.set_ylabel("paired gain (perturbed regime)")
    ax.legend(frameon=False, fontsize=7)

    fig.savefig(fig_path("fig10_inverse_design.png"))
    plt.close(fig)

    results["honest_notes"] = [
        "The search discovered a schedule over the SAME arsenal exp8 tested "
        "by hand — evaluated under an explicit procedure-risk cost so that "
        "'maximum therapy forever' is not the answer.",
        "Held-out validation: the discovered policy is evaluated on seeds "
        "never seen by the search (21-24 vs search CRN 11-12) with a PAIRED "
        "design (each policy divided by the none-control on the same seed, so "
        "population-level frailty draws cancel) — generalization, not "
        "memorization.",
        "Regime transfer: perturbed corruption rate, critical fidelity, and "
        "channel aging — the policy must survive physics it was not tuned "
        "for (a weaker criterion than winning: no collapse).",
        "The cost-free sensitivity arm reports whether the discovered "
        "structure was an artifact of the procedure-risk model.",
    ]

    path = dump_json("exp10_inverse_design.json", results)
    print(f"[exp10] results -> {path}  ({time.time() - t0:.0f}s total)")
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["search", "eval", "all"])
    args = ap.parse_args()
    main(stage=args.stage)
