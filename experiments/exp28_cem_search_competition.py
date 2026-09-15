"""exp28 — CEM SEARCH UNDER COMPETITION: search where the search found
something.

THE USER'S MOVE (Option 3): exp25 transplanted exp19's century-hold
policy (discovered on the SINGLE-pattern stack) into the multi-pattern
world and it WON decisively (hold 0.625 vs HAND 0.500, +14.4yr median).
Now re-run the CEM SEARCH ITSELF with the fitness evaluated in the
competitive world — if the solo-optimal policy was found to under-
estimate itself by 1.2% in exp19's world, maybe the competitive-optimal
policy is better still. If re-searching adds nothing, the solo-
discovered policy sits at (or near) the competitive optimum — a
robustness property of the search, not a coincidence of its world.

DESIGN (exp25's world exactly — the eval is a faithful port of
exp25.run_arm so the transplant reference reproduces):

  SEARCH: 8-dim policy space (exp19's bounds verbatim — write_age,
  start_age, period, budget, k_anchor, boost_p_verified,
  boost_p_unverified, boost_factor), CEM pop 24 / iters 10 / elite 0.25
  / seed 27, fitness = -(mean hold) over search seeds (41, 42) — NEW
  seeds, disjoint from exp19's search (11-12), exp19's eval (31-33),
  and exp25's eval (21-23). Search-world cohorts K=150, 105yr (exp19's
  search convention — relative fitness, censoring irrelevant).

  hold(t) = alive_fraction(t) x mean I_recoverable(A,B,C)(t),
  t in 30..100 — exp25's objective verbatim (the multi-pattern
  generalization; the composition caveat recorded there applies here).

  HELD-OUT EVAL (seeds 21-23, K=200, 120yr, exp25's convention —
  directly comparable with exp25's published table):
    disc28     the newly discovered policy
    disc19     exp19's transplanted policy (exp25's DISC) — doubles as
               the harness-equivalence regression anchor (R)
    hand       HAND_ANCHORED (exp17's protected arm)
    none       write, never maintain (decay baseline)
    disc28_b2  disc28 with budget clamped to 2 (the starvation stress)
    disc19_b2  disc19 with budget clamped 2 (exp25's S4 pair)

PRE-REGISTERED:
  C1 (RE-SEARCH PAYS): hold(disc28) >= hold(disc19) + 0.02 on the
      held-out competitive world. Failing => the solo-discovered policy
      is already within 0.02 of the competitive optimum — search-world
      mismatch costs almost nothing (the robustness reading).
  C2 (POLICY DIVERGENCE): >= 1 of write_age/start_age/period/budget
      shifted by >= 25% between disc28 and disc19. Recorded either way:
      divergence without C1 = a rugged neutral landscape; convergence
      = the same optimum from both worlds.
  C3 (LAW REDISCOVERED, 3rd independent test): k_anchor(disc28) <= 1.0
      — the matched-channel weak-pull law, now under competition.
  C4 (INTERIORITY): 1 < budget < 12 AND period > 1.5 — procedure risk
      still forbids maximum-therapy-forever under competition.
  C5 (EQUILIBRIUM INVARIANCE): under disc28, I_V(A)@60 > I_V(B)@60 and
      I_V(A)@60 > I_V(C)@60 — exp23's zone-physics ordering survives
      whatever the search found (cross-link to exp26: if the search
      reorders zones it has found a corruption-side lever exp26 says
      does not exist at these elasticities).
  C6 (STRESS): hold(disc28_b2) >= hold(disc19_b2) — the competitively
      searched policy under the starved budget.
  R (HARNESS EQUIVALENCE): disc19 through this module's eval path
      reproduces exp25's published disc arm (|dhold| < 0.005; exact
      delta recorded — the port is trajectory-faithful by construction,
      so this is the bit-level claim at experiment scale).

Falsifies: C1 passing + C2 passing kills the 'search world does not
matter' null — the competitive optimum is a different policy AND better,
so single-pattern benchmarks under-estimate more than exp25 showed. C1
failing validates exp25's robustness reading (the transplant was near-
optimal). C3 failing would be the first policy family to violate the
matched-channel law. C5 failing would contradict exp26's elasticity map
and demand a mechanism story.
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
from experiments.exp23_multi_pattern import (
    ZONES, JUMP_MULT, HAZARD_BOOST, MULTI_TARGET, ZONE_MASK,
    MultiPatternCohort, _per_individual, _zone_write,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp28_cem_competition_search.json"
CKPT = "scripts_dev/exp28_cem.ckpt"
STATE = "scripts_dev/exp28_state.json"
EXP25 = "results/exp25_cem_competition.json"

SEARCH_SEEDS = (41, 42)          # NEW — disjoint from 11/12, 31-33, 21-23
EVAL_SEEDS = (21, 22, 23)        # exp25's eval seeds (comparability)
POP, ITERS, ELITE = 24, 10, 0.25
K_SEARCH, YEARS_SEARCH = 150, 105.0
K_EVAL, YEARS_EVAL = 200, 120.0
LEDGER_AT = np.arange(30.0, 101.0, 10.0)   # exp19/exp25 hold window
H_PROC = 3e-5
SPECS = [(nm, MULTI_TARGET, ZONE_MASK[(ZONES[nm][0], ZONES[nm][1])])
         for nm in ("A", "B", "C")]

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

# exp19's discovered policy (exp25's DISC) and HAND — verbatim
DISC19 = {"write_age": 14.5, "start_age": 31.5, "period": 2.5, "budget": 9,
          "k_anchor": 0.32615456103626106, "boost_pv": 0.0,
          "boost_pu": 0.3686716946123514, "boost_f": 1.05936261826428,
          "h_proc": H_PROC}
HAND = {"write_age": 5.0, "start_age": 30.0, "period": 5.0, "budget": 6,
        "k_anchor": 0.25, "boost_pv": 0.0, "boost_pu": 0.0,
        "boost_f": 1.0, "h_proc": H_PROC}
NONE_U = {**HAND, "start_age": 105.0}


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


def _build(seed: int, k_anchor: float, K: int) -> MultiPatternCohort:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **REGIME)
    ch = MultiPatternCohort(K=K, params=params, seed=seed,
                            death_semantics="broadcast", latch="v2",
                            protect_written=True, jump_rate=0.006,
                            f_crit=0.655, k_anchor=k_anchor)
    ch._tgt = fidelity_target()
    ch.jump_mult = JUMP_MULT
    ch.hazard_boost = HAZARD_BOOST
    return ch


def run_policy(pol: dict, seed: int, K: int = K_EVAL,
               years: float = YEARS_EVAL,
               maintain_on: bool = True) -> dict:
    """One policy on one multi-pattern cohort — a faithful port of
    exp25.run_arm (same intervention order, same RNG usage), with K and
    horizon parameterized so the SEARCH can run cheap."""
    ch = _build(seed, pol["k_anchor"], K)
    codec = (FidelityCodec(n_cells=N_CELLS, budget_per_cycle=pol["budget"],
                           levels=7, target_source="anchored")
             if maintain_on else None)
    rng_local = np.random.default_rng(1234567)
    written = {"done": False}
    seen: set = set()
    proc_events = np.zeros(K, float)
    rows = {"t": [], "alive": [], "hold": [],
            "IV": {"A": [], "B": [], "C": []}}
    iv60 = {}

    def intervene(t, cohort):
        nonlocal proc_events
        dt = 0.25
        if not written["done"] and t >= pol["write_age"] - 1e-9:
            written["done"] = True
            for name in ("A", "B", "C"):
                _zone_write(cohort, name)
            proc_events += 45.0           # the write is a procedure
            cohort._tgt = MULTI_TARGET
        if codec is not None and t >= pol["start_age"] - 1e-9 \
                and abs((t - pol["start_age"]) % pol["period"]) <= 0.26:
            rep = codec.maintain(cohort, age_preset(t), mode="codec")
            per_i = np.asarray(rep["restored_per_i"], float)
            proc_events += per_i
            pv, pu, bf = pol["boost_pv"], pol["boost_pu"], pol["boost_f"]
            if (pv > 0 or pu > 0) and bf > 1.0:
                verified = np.asarray(rep["verified_mask"], bool)
                draw = rng_local.random(cohort.K)
                mask = (verified & (draw < pv)) | (~verified & (draw < pu))
                if mask.any():
                    cohort.boost_channel(mask, bf, 8.0)
        if pol.get("h_proc", H_PROC) > 0:
            hazard = pol["h_proc"] * proc_events
            dd = cohort.rng.random(cohort.K)
            died = cohort.alive & (dd < dt * hazard)
            if died.any():
                cohort.death_age[died] = cohort.t
                cohort.alive &= ~died
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                alive_f = float(cohort.alive.mean())
                led = cohort.pattern_ledgers(SPECS)
                ir_vals = [led[nm]["I_recoverable"] for nm in ("A", "B", "C")]
                for nm in ("A", "B", "C"):
                    rows["IV"][nm].append(float(led[nm]["I_V"]))
                rows["t"].append(float(a))
                rows["alive"].append(alive_f)
                rows["hold"].append(alive_f * float(np.mean(ir_vals)))
                if abs(a - 60.0) < 0.13:
                    for nm, ref, zone in SPECS:
                        iv60[nm] = float(_per_individual(
                            cohort, zone, ref, "I_V").mean())

    s = ch.run(years=years, dt=0.25, intervention=intervene)
    return {
        "hold_mean": float(np.mean(rows["hold"])) if rows["hold"] else 0.0,
        "hold_curve": rows["hold"], "hold_t": rows["t"],
        "median": float(s["median_lifespan"]),
        "restored": codec.restored if codec else 0,
        "IV60": iv60,
        "alive": rows["alive"],
        "alive_frac_60": (float(rows["alive"][next(
            (i for i, tt in enumerate(rows["t"]) if abs(tt - 60) < .2), 0)])
            if rows["t"] else float("nan")),
    }


def _fitness(u):
    pol = decode(u)
    pol["h_proc"] = H_PROC
    rs = [run_policy(pol, s, K=K_SEARCH, years=YEARS_SEARCH)
          for s in SEARCH_SEEDS]
    return -float(np.mean([r["hold_mean"] for r in rs]))


def _agg(pol: dict, seeds=EVAL_SEEDS, **kw) -> dict:
    rs = [run_policy(pol, s, **kw) for s in seeds]
    return {
        "hold_mean": float(np.mean([r["hold_mean"] for r in rs])),
        "hold_by_seed": [r["hold_mean"] for r in rs],
        "hold_curve": [float(np.mean(x)) for x in
                       zip(*[r["hold_curve"] for r in rs])],
        "hold_t": rs[0]["hold_t"],
        "median": float(np.mean([r["median"] for r in rs])),
        "restored": float(np.mean([r["restored"] for r in rs])),
        "IV60": {nm: float(np.nanmean([r["IV60"][nm] for r in rs]))
                 for nm in ("A", "B", "C")},
        "alive_frac_60": float(np.nanmean([r["alive_frac_60"]
                                           for r in rs])),
    }


def main() -> dict:
    setup()
    t0 = time.time()
    state = {}
    if os.path.exists(STATE):
        with open(STATE) as f:
            state = json.load(f)

    # ---------------- search ----------------
    if "discovered_u" not in state:
        _p("[exp28] CEM search UNDER COMPETITION (pop=%d, iters=%d, "
           "seeds %s, K=%d, %.0fyr)" % (POP, ITERS, SEARCH_SEEDS,
                                        K_SEARCH, YEARS_SEARCH))
        best_u, best_f, hist = cem_optimize(
            _fitness, BOUNDS, pop=POP, elite_frac=ELITE, iters=ITERS,
            seed=27, verbose=True, checkpoint=CKPT)
        pol28 = decode(best_u)
        pol28["h_proc"] = H_PROC
        # report keys = decode()'s keys (boost_pv/pu/f), not the NAMES
        # spelling of the bounds list
        _p("  discovered policy: "
           + "  ".join(f"{k}={pol28[k]:.3f}" for k in
                      ("write_age", "start_age", "period", "budget",
                       "k_anchor", "boost_pv", "boost_pu",
                       "boost_f")))
        _p(f"  search hold (K={K_SEARCH}, {YEARS_SEARCH:.0f}yr) = "
           f"{-best_f:.3f}")
        state["discovered_u"] = [float(x) for x in best_u]
        state["search_hold"] = -float(best_f)
        state["history"] = [(int(i), float(f)) for i, f, _mu in hist]
        with open(STATE, "w") as f:
            json.dump(state, f, indent=1)
    pol28 = decode(state["discovered_u"])
    pol28["h_proc"] = H_PROC

    # ---------------- held-out eval ----------------
    _p(f"\n[exp28] held-out evaluation (seeds {EVAL_SEEDS}, K={K_EVAL}, "
       f"{YEARS_EVAL:.0f}yr — exp25's convention)")
    arms = {
        "disc28": _agg(pol28),
        "disc19": _agg(DISC19),
        "hand": _agg(HAND),
        "none": _agg(NONE_U, maintain_on=False),
        "disc28_b2": _agg({**pol28, "budget": 2}),
        "disc19_b2": _agg({**DISC19, "budget": 2}),
    }
    for nm, e in arms.items():
        iv = "  ".join(f"{z} {e['IV60'][z]:5.3f}" for z in ("A", "B", "C"))
        _p(f"    {nm:10s}: hold {e['hold_mean']:.3f}  median "
           f"{e['median']:6.1f}  restored {e['restored']:6.0f}  {iv}")

    # ---------------- criteria ----------------
    with open(EXP25) as f:
        e25 = json.load(f)
    r_delta = abs(arms["disc19"]["hold_mean"]
                  - e25["arms"]["disc"]["hold_mean"])

    def div(a, b):
        return abs(a - b) / max(abs(b), 1e-9)

    crit = {
        "C1_research_pays": bool(
            arms["disc28"]["hold_mean"]
            >= arms["disc19"]["hold_mean"] + 0.02),
        "C2_policy_divergence": bool(any(
            div(pol28[k], DISC19[k]) >= 0.25
            for k in ("write_age", "start_age", "period", "budget"))),
        "C3_law_rediscovered": bool(pol28["k_anchor"] <= 1.0),
        "C4_interiority": bool(1 < pol28["budget"] < 12
                               and pol28["period"] > 1.5),
        "C5_equilibrium_invariance": bool(
            arms["disc28"]["IV60"]["A"] > arms["disc28"]["IV60"]["B"]
            and arms["disc28"]["IV60"]["A"] > arms["disc28"]["IV60"]["C"]),
        "C6_stress_b2": bool(arms["disc28_b2"]["hold_mean"]
                             >= arms["disc19_b2"]["hold_mean"]),
        "R_harness_vs_exp25": bool(r_delta < 0.005),
    }
    results = {
        "exp": "exp28_cem_competition_search",
        "discovered_policy": {k: pol28[k] for k in
                             ("write_age", "start_age", "period",
                              "budget", "k_anchor", "boost_pv",
                              "boost_pu", "boost_f")},
        "transplanted_policy": DISC19,
        "hand_policy": HAND,
        "search": {"seeds": list(SEARCH_SEEDS), "K": K_SEARCH,
                   "years": YEARS_SEARCH, "pop": POP, "iters": ITERS,
                   "history": state.get("history", []),
                   "search_hold": state.get("search_hold")},
        "arms": arms,
        "criteria": crit,
        "harness_regression_delta": float(r_delta),
        "exp25_reference": {
            "disc_hold": e25["arms"]["disc"]["hold_mean"],
            "hand_hold": e25["arms"]["hand"]["hold_mean"],
        },
        "hold_definition": "alive_fraction x mean I_recoverable over "
                           "A/B/C at ages 30..100 (exp25's objective)",
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    _p(f"    harness regression |disc19 - exp25.disc| = {r_delta:.2e}")
    _figure(results)
    _p(f"exp28 complete in {time.time()-t0:.0f}s")
    return results


def _figure(results: dict) -> None:
    setup()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4),
                           constrained_layout=True)
    t = results["arms"]["disc28"]["hold_t"]
    styles = {"disc28": (PALETTE["good"], "-"),
              "disc19": ("#b58900", "-"),
              "hand": (PALETTE["accent"], "-"),
              "none": ("0.6", "-"),
              "disc28_b2": (PALETTE["good"], "--"),
              "disc19_b2": ("#b58900", "--")}
    for nm, (c, ls) in styles.items():
        ax[0].plot(t, results["arms"][nm]["hold_curve"], ls=ls, lw=2.2,
                   color=c, label=nm)
    ax[0].set(xlabel="age (yr)", ylabel="hold = alive x mean I_rec",
              ylim=(0, 1.02),
              title="searched-under-competition vs transplanted")
    ax[0].legend(fontsize=8)

    names = ["disc28", "disc19", "hand"]
    vals = [results["arms"][n]["hold_mean"] for n in names]
    ax[1].bar(range(3), vals,
              color=[PALETTE["good"], "#b58900", PALETTE["accent"]])
    ax[1].set_xticks(range(3))
    ax[1].set_xticklabels(names)
    ax[1].set(ylabel="hold (mean 30..100)", ylim=(0, 1.0),
              title="held-out, competitive world")

    # search convergence
    h = results["search"]["history"]
    if h:
        its = [i for i, f in h]
        fs = [-f for i, f in h]
        ax[2].plot(its, fs, "o-", color=PALETTE["accent"], lw=2)
        ax[2].set(xlabel="CEM iteration", ylabel="population best hold",
                  title="search convergence (competitive fitness)")
    fig.savefig(fig_path("fig27_cem_competition_search"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
