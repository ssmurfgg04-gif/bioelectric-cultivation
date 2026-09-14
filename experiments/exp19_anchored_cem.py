"""exp19 — CEM on the ANCHORED STACK: hold the target over a century.

THE STEP exp10 DID NOT TAKE: the reach-objective search (maximize median
lifespan toward the BIRTH pattern) predates the anchored stack. Now that
novel target forms can be written and maintained (exp17: protected tier,
0.90 recoverable at age 100), the inverse problem changes shape: not
'reach the target' but 'HOLD the target over a century' — a different
fitness landscape (the written pattern must exist AND the animal must stay
alive; death is ultimate pattern loss).

OBJECTIVE (pre-registered):
  hold(t) = alive_fraction(t) x I_recoverable(t)  at ages 30,40,...,100
  fitness = -mean_t hold(t)   (the century-hold integral)
  Scored against the CURRENT (novel) target — the exp17 semantics.

SEARCH SPACE (8 dims — the anchored-stack policy):
  write_age      when the novel pattern is written (5..30)
  start_age      when anchored maintenance begins (20..60)
  period         checkup interval (1.5..10)
  budget         cell-writes per cycle (1..12)
  k_anchor       the anchor pull strength (0.05..3.0) — the matched-channel
                 law axis: exp16 found composition only works with WEAK pull
                 (k=0.25); does the SEARCH rediscover it?
  boost_p_verified / boost_p_unverified / boost_factor  (exp10 semantics)
Procedure risk h_proc = 3e-5/write-event/yr applies identically to all arms.

BASELINES:
  HAND_ANCHORED  (5, 30, 5, 6, 0.25, 0, 0, 1) — the exp17 protected arm
  NONE           write but never maintain (the decay baseline)

Pre-registered criteria:
  H1 SEARCH WIN     held-out hold(discovered) >= 1.05 x hold(HAND_ANCHORED)
  H2 LAW REDISCOVERED  discovered k_anchor <= 1.0 (weak pull emerges from
                    search — the exp16 matched-channel law, now found
                    instead of calibrated)
  H3 ALLOCATION     budget and period interior (1 < budget < 12, period > 1.5)
                    — procedure risk forbids maximum-therapy-forever
  H4 NEW LANDSCAPE  the discovered schedule differs materially from exp10's
                    reach-optimum (start_age 20.5, period 2.45, budget 9.0):
                    >= 1 dim shifted by >= 25% — hold is not reach.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.inverse.cem import cem_optimize
from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.exp17_anchored_target import (
    NovelTargetCohort, NOVEL_TARGET, ZONE, NOVEL_VAL, COHORT_KW,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp19_anchored_cem.json"
CKPT = "scripts_dev/exp19_cem.ckpt"
STATE = "scripts_dev/exp19_state.json"

SEARCH_SEEDS = (11, 12)
HELDOUT_SEEDS = (31, 32, 33)
POP, ITERS, ELITE = 24, 10, 0.25
YEARS = 105.0
LEDGER_AT = np.arange(30.0, 101.0, 10.0)
H_PROC = 3e-5

BOUNDS = [
    (5.0, 30.0),     # write_age
    (20.0, 60.0),    # start_age
    (1.5, 10.0),     # period
    (1.0, 12.0),     # budget
    (0.05, 3.0),     # k_anchor
    (0.0, 1.0),      # boost_p_verified
    (0.0, 1.0),      # boost_p_unverified
    (1.0, 1.6),      # boost_factor
]
NAMES = ["write_age", "start_age", "period", "budget", "k_anchor",
         "boost_p_verified", "boost_p_unverified", "boost_factor"]

HAND = (5.0, 30.0, 5.0, 6.0, 0.25, 0.0, 0.0, 1.0)       # exp17 protected arm
NONE_U = (5.0, 105.0, 5.0, 6.0, 0.25, 0.0, 0.0, 1.0)    # write, never maintain

EXP10_REACH = (20.5, 2.45, 9.0)   # start_age, period, budget (reach-optimum)

PERTURBED_REGIME = dict(REGIME)
PERTURBED_REGIME.update(kappa_noise=0.025, lambda_gap=0.028)
PERTURBED_COHORT = dict(COHORT_KW)
PERTURBED_COHORT.update(jump_rate=0.0075, f_crit=0.58)


def _p(s):
    print(s, flush=True)


def decode(u) -> dict:
    u = np.clip(np.asarray(u, float), [b[0] for b in BOUNDS],
                [b[1] for b in BOUNDS])
    return {
        "write_age": round(float(u[0]) * 4) / 4,
        "start_age": round(float(u[1]) * 4) / 4,
        "period": max(0.75, round(float(u[2]) * 4) / 4),
        "budget": int(round(float(u[3]))),
        "k_anchor": float(u[4]),
        "boost_pv": float(u[5]),
        "boost_pu": float(u[6]),
        "boost_f": float(u[7]),
    }


def eval_hold(u, seed: int, K: int = 150, years: float = YEARS,
              regime: dict | None = None, cohort_kw: dict | None = None,
              h_proc: float = H_PROC, maintain_on: bool = True) -> dict:
    """One policy on one anchored-stack cohort. Top-level for pickling."""
    policy = decode(u)
    kw = dict(COHORT_KW)
    kw.update(cohort_kw or {})
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **(regime or REGIME))
    ch = NovelTargetCohort(K=K, params=params, seed=seed,
                           death_semantics="broadcast", latch="v2",
                           protect_written=True, k_anchor=policy["k_anchor"],
                           **kw)
    ch._tgt = NOVEL_TARGET
    codec = (FidelityCodec(n_cells=N_CELLS, budget_per_cycle=policy["budget"],
                           levels=7, target_source="anchored")
             if maintain_on else None)
    rng_local = np.random.default_rng(1234567)
    written = {"done": False}
    proc_events = np.zeros(K, float)
    seen: set = set()
    rows = {"t": [], "hold": [], "I_rec": [], "alive": []}
    stats = {"writes": 0, "boost_apps": 0, "refused": 0}

    def intervene(t, cohort):
        nonlocal proc_events
        dt = 0.25
        if not written["done"] and t >= policy["write_age"] - 1e-9:
            written["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, ZONE] = True
            cohort.theta = np.where(do, NOVEL_VAL, cohort.theta)
            cohort.V = np.where(do, NOVEL_VAL, cohort.V)
            cohort.on_write(do)
            proc_events += float(ZONE.sum())      # the write is a procedure

        if codec is not None and t >= policy["start_age"] - 1e-9 \
                and abs((t - policy["start_age"]) % policy["period"]) <= 0.26:
            rep = codec.maintain(cohort, age_preset(t), mode="codec")
            per_i = np.asarray(rep["restored_per_i"], float)
            proc_events += per_i
            stats["writes"] += int(per_i.sum())
            stats["refused"] += rep["refused"]
            pv, pu, bf = policy["boost_pv"], policy["boost_pu"], policy["boost_f"]
            if (pv > 0 or pu > 0) and bf > 1.0:
                verified = np.asarray(rep["verified_mask"], bool)
                draw = rng_local.random(cohort.K)
                mask = (verified & (draw < pv)) | (~verified & (draw < pu))
                if mask.any():
                    cohort.boost_channel(mask, bf, 8.0)
                    stats["boost_apps"] += int(mask.sum())

        if h_proc > 0:
            hazard = h_proc * proc_events
            dd = cohort.rng.random(cohort.K)
            died = cohort.alive & (dd < dt * hazard)
            if died.any():
                cohort.death_age[died] = cohort.t
                cohort.alive &= ~died

        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                led = cohort.pattern_ledger(ref=NOVEL_TARGET, zone=ZONE)
                alive_f = float(cohort.alive.mean())
                rows["t"].append(float(a))
                rows["alive"].append(alive_f)
                rows["I_rec"].append(float(led["I_recoverable"]))
                rows["hold"].append(alive_f * float(led["I_recoverable"]))

    s = ch.run(years=years, dt=0.25, intervention=intervene)
    hold_mean = float(np.mean(rows["hold"])) if rows["hold"] else 0.0
    return {"median": s["median_lifespan"], "hold_mean": hold_mean,
            "hold_t": rows["t"], "hold": rows["hold"], "I_rec": rows["I_rec"],
            "alive": rows["alive"], **stats}


def _fitness(u):
    rs = [eval_hold(u, s) for s in SEARCH_SEEDS]
    return -float(np.mean([r["hold_mean"] for r in rs]))


def run_search(stage_checkpoints=True):
    _p("[exp19] CEM search — the century-hold objective "
       "(pop=%d, iters=%d, CRN %s)" % (POP, ITERS, SEARCH_SEEDS))
    best_u, best_f, hist = cem_optimize(
        _fitness, BOUNDS, pop=POP, elite_frac=ELITE, iters=ITERS, seed=19,
        verbose=True, checkpoint=CKPT)
    _p(f"  discovered u = {np.round(best_u, 3)}  hold = {-best_f:.3f}")
    return best_u, best_f, hist


def mean_hold(u, seeds, K=200, **kw):
    rs = [eval_hold(u, s, K=K, **kw) for s in seeds]
    return {
        "hold_mean": float(np.mean([r["hold_mean"] for r in rs])),
        "median": float(np.mean([r["median"] for r in rs])),
        "hold_curve": [float(np.mean(x)) for x in zip(*[r["hold"] for r in rs])],
        "hold_t": rs[0]["hold_t"],
        "writes": float(np.mean([r["writes"] for r in rs])),
        "boost_apps": float(np.mean([r["boost_apps"] for r in rs])),
    }


def main(stage: str = "all") -> dict:
    setup()
    t0 = time.time()
    state = {}
    if os.path.exists(STATE):
        with open(STATE) as f:
            state = json.load(f)

    if stage in ("search", "all") or "discovered_u" not in state:
        best_u, best_f, hist = run_search()
        state["discovered_u"] = [float(x) for x in best_u]
        state["search_hold"] = -float(best_f)
        state["history"] = [(int(i), float(f)) for i, f, _mu in hist]
        state["elite_k"] = [float(np.mean([u[4] for u in []])) for u in []]
        with open(STATE, "w") as f:
            json.dump(state, f, indent=1)

    disc = np.array(state["discovered_u"])

    if stage in ("eval", "all") or "heldout" not in state:
        _p("\n[exp19] held-out evaluation (seeds %s, K=200)" % (HELDOUT_SEEDS,))
        held_disc = mean_hold(disc, HELDOUT_SEEDS)
        held_hand = mean_hold(HAND, HELDOUT_SEEDS)
        held_none = mean_hold(NONE_U, HELDOUT_SEEDS, maintain_on=False)
        _p(f"  discovered : hold {held_disc['hold_mean']:.3f}  "
           f"median {held_disc['median']:.1f}  "
           f"writes {held_disc['writes']:.0f}")
        _p(f"  HAND       : hold {held_hand['hold_mean']:.3f}  "
           f"median {held_hand['median']:.1f}")
        _p(f"  NONE       : hold {held_none['hold_mean']:.3f}  "
           f"median {held_none['median']:.1f}")
        state["heldout"] = {"discovered": held_disc, "hand": held_hand,
                            "none": held_none}

        _p("\n  regime transfer (perturbed physics):")
        tr_disc = mean_hold(disc, HELDOUT_SEEDS, regime=PERTURBED_REGIME,
                            cohort_kw=PERTURBED_COHORT)
        tr_hand = mean_hold(HAND, HELDOUT_SEEDS, regime=PERTURBED_REGIME,
                            cohort_kw=PERTURBED_COHORT)
        _p(f"  discovered : hold {tr_disc['hold_mean']:.3f}   "
           f"HAND: {tr_hand['hold_mean']:.3f}")
        state["transfer"] = {"discovered": tr_disc, "hand": tr_hand}

        _p("\n  no-procedure-risk sensitivity (h_proc = 0):")
        nr_disc = mean_hold(disc, HELDOUT_SEEDS, h_proc=0.0)
        nr_hand = mean_hold(HAND, HELDOUT_SEEDS, h_proc=0.0)
        _p(f"  discovered : hold {nr_disc['hold_mean']:.3f}   "
           f"HAND: {nr_hand['hold_mean']:.3f}")
        state["norisk"] = {"discovered": nr_disc, "hand": nr_hand}

        _p("\n  ablations (each dim reset to HAND, held-out):")
        ab = {}
        for i, nm in enumerate(NAMES):
            u_ab = disc.copy()
            u_ab[i] = HAND[i]
            r = mean_hold(u_ab, HELDOUT_SEEDS)
            ab[nm] = r["hold_mean"]
            _p(f"    {nm:18s} -> hold {r['hold_mean']:.3f} "
               f"({r['hold_mean'] - held_disc['hold_mean']:+.3f})")
        state["ablations"] = ab
        with open(STATE, "w") as f:
            json.dump(state, f, indent=1)

    # ---------------- criteria ----------------
    disc_u = state["discovered_u"]
    pol = decode(disc_u)
    hd, hh = (state["heldout"]["discovered"]["hold_mean"],
              state["heldout"]["hand"]["hold_mean"])
    crit = {
        "H1_search_win": bool(hd >= 1.05 * hh),
        "H2_law_rediscovered": bool(pol["k_anchor"] <= 1.0),
        "H3_allocation": bool(1 < pol["budget"] < 12 and pol["period"] > 1.5),
        "H4_new_landscape": bool(
            abs(pol["start_age"] - EXP10_REACH[0]) / EXP10_REACH[0] >= 0.25
            or abs(pol["period"] - EXP10_REACH[1]) / EXP10_REACH[1] >= 0.25
            or abs(pol["budget"] - EXP10_REACH[2]) / EXP10_REACH[2] >= 0.25),
    }
    out = {"exp": "exp19_anchored_cem",
           "objective": "century-hold: mean_t alive_frac(t) x I_rec(t), "
                        "t in 30..100",
           "discovered_u": disc_u, "discovered_policy": pol,
           "search_hold": state["search_hold"],
           "heldout": state["heldout"], "transfer": state["transfer"],
           "norisk": state["norisk"], "ablations": state["ablations"],
           "criteria": crit}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    _p("\n criteria:")
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    try:
        _figure(out)
    except Exception as e:  # noqa: BLE001
        _p(f"  (figure failed non-fatally: {e})")
    _p(f"exp19 complete in {time.time()-t0:.0f}s")
    return out


def _figure(res):
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2), constrained_layout=True)
    hd = res["heldout"]
    t = hd["discovered"]["hold_t"]
    ax[0].plot(t, hd["discovered"]["hold_curve"], lw=2.4,
               color=PALETTE["good"], label="discovered")
    ax[0].plot(t, hd["hand"]["hold_curve"], lw=2.2, color=PALETTE["accent"],
               label="HAND (exp17)")
    ax[0].plot(t, hd["none"]["hold_curve"], lw=2.0, color="0.6",
               label="none (decay)")
    ax[0].set(xlabel="age (yr)", ylabel="hold = alive x I_recoverable",
              ylim=(0, 1.02), title="the century-hold integral (held-out)")
    ax[0].legend(fontsize=9)

    hist = res.get("_history") or []
    ax[1].axis("off")

    names = list(res["ablations"])
    vals = [res["ablations"][n] - hd["discovered"]["hold_mean"]
            for n in names]
    ax[2].barh(range(len(names)), vals, color=PALETTE["accent"])
    ax[2].set_yticks(range(len(names)))
    ax[2].set_yticklabels(names, fontsize=8)
    ax[2].axvline(0, color="k", lw=0.6)
    ax[2].set(xlabel="hold delta vs discovered (ablation)",
              title="what carries the policy")
    fig.suptitle("exp19 — CEM on the anchored stack: hold, not reach",
                 fontsize=12)
    fig.savefig(fig_path("fig19_anchored_cem"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig19_anchored_cem.png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
