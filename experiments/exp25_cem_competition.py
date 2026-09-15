"""exp25 — does the century-hold policy survive COMPETITION?

THE USER'S QUESTION: run exp19's century-hold CEM policy against the
multi-pattern stack and see if the discovered policy survives when
three novel patterns + the birth pattern compete for one codec budget.

WHAT IS BEING TRANSPLANTED (exp19's discovered 8-dim policy, searched
on the SINGLE-pattern anchored stack, seeds 11-12; hold objective =
mean_t alive x I_recoverable, t in 30..100):
    write_age 14.5   start_age 31.5   period 2.5   budget 9
    k_anchor 0.326   boost_pv 0.0   boost_pu 0.369   boost_f 1.059
  vs HAND (exp17's protected arm): write 5, start 30, period 5,
  budget 6, k_anchor 0.25, no boost.
  exp19's verdict: discovered 0.582 vs HAND 0.575 held-out — H1 FAILED
  by 1.2% (no search win), but H2-H4 passed (weak-pull law rediscovered
  at 0.326, interior allocation, new landscape vs reach).

WHY COMPETITION IS THE STRESSOR exp19 NEVER TESTED: its search world
held ONE novel pattern; exp23 then showed the multi-pattern world has
its own economics (two-layer capacity: storage free, expression
budget-bound; competition cost visible only under scarcity; no
allocation policy beats cell order). A policy discovered in the
single-pattern world may have overfit its unconstrained channel: the
discovered budget 9 on 60 cells is RICHER than HAND's 6, and exp23's
E1 gradient says competition goes invisible as the channel richens —
so the naive prediction is the discovered policy sails through. The
informative stress is the CLAMPED budget (b2, where exp23 measured
real competition cost): does the searched SCHEDULE (period 2.5,
start 31.5 — 2x the checkup frequency) still pay when the budget is
starved, or does its advantage evaporate with the channel?

DESIGN (exp23's exact multi-pattern geometry — zones C/A/B/birth,
cluster-aligned, scrambled; seeds 21-23 — held-out for the discovered
policy (search used 11-12, exp19's eval used 31-33) AND matching
exp23's published runs so the status-quo arm is a bit-exact regression
anchor; K=200; hold integrates ages 30..100 = exp19's objective; the
RUN horizon is 120yr = exp23's censoring convention, so medians are
comparable and the status-quo anchor replicates — a 105yr horizon was
run first and rejected: identical trajectories (I_V@60 and restored
matched exp23 exactly) but survivor-censoring shifted the death-age
median 57.9 vs 71.8, an artifact, recorded here):

  Arms (all multi-pattern, h_proc 3e-5/write-event/yr exactly as
  exp19 applied it, unless noted):
    disc        the discovered policy as-is (budget 9, k_anchor 0.326,
                boost_pu 0.369 x 1.059 on unverified, writes A/B/C at
                age 14.5)
    hand        HAND_ANCHORED transplanted (write 5, start 30, period
                5, budget 6, k_anchor 0.25, no boost)
    disc_b2     discovered with budget clamped to 2 (the stress test)
    hand_b2     HAND with budget clamped to 2 (the matched control)
    disc_solo   discovered schedule on the physics-matched single-B
                stack (B zone alone; the no-competition reference)
    hand_solo   HAND schedule, single-B (its no-competition reference)
    none        write A/B/C, never maintain (the decay baseline)
    status_quo  exp23's default arm exactly — write 5 / start 30 /
                period 5 / budget 6 / cell-order / k_anchor 0.25, NO
                h_proc (the bit-exact regression anchor; the only arm
                without procedure risk)

  hold(t) = alive_fraction(t) x mean_pattern I_recoverable(t) at ages
  30..100 (the multi-pattern generalization of exp19's objective;
  per-pattern holds recorded alongside; solo arms score B alone —
  exp23's solo_B convention).

PRE-REGISTERED:
  S1 (TRANSFER): disc overall hold >= hand overall hold. exp19's H1
      failed by 1.2% single-pattern; if the ordering inverts under
      competition, even the searched policy's marginal edge does not
      transfer.
  S2 (COMPETITION-COST ASYMMETRY): cost(disc) = hold(disc_solo) -
      hold(disc)  <  cost(hand) = hold(hand_solo) - hold(hand).
      The discovered policy's richer channel should pay LESS for
      competition (exp23 E1's gradient). Failing => the searched
      policy is MORE competition-fragile than the hand policy.
  S3 (EQUILIBRIUM LAW INVARIANCE): under disc in competition,
      I_V(A)@60 > I_V(B)@60 and I_V(A)@60 > I_V(C)@60 — exp23's E3
      physics ordering is policy-invariant (k_anchor 0.326 is still
      weak-pull by exp16's law).
  S4 (STRESS): disc_b2 overall hold >= hand_b2 overall hold — the
      schedule's advantage survives the starved budget, or it was
      channel-richness all along.
  R (REGRESSION): status_quo replicates exp23's published default arm
      (b6): |I_V@60 delta| < 0.005 per pattern, median within 0.5yr
      (hooks-unused bit-exactness at experiment scale, from the
      transplant side).

Falsifies: S1+S4 both failing kills the century-hold policy's claim
to generalize beyond its single-pattern search world. S2 failing
inverts the richness-fragility reading. S3 failing means a WEAK-pull
policy reorders the zone physics (would demand a mechanism story the
stack does not currently have).
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.exp23_multi_pattern import (
    ZONES, JUMP_MULT, HAZARD_BOOST, MULTI_TARGET, ZONE_MASK,
    B_SOLO_TARGET, B_MASK, MultiPatternCohort, _per_individual,
    _zone_write,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp25_cem_competition.json"
EXP23 = "results/exp23_multi_pattern.json"

K, YEARS, SEEDS = 200, 120.0, (21, 22, 23)
LEDGER_AT = np.arange(30.0, 101.0, 10.0)   # exp19's hold window
H_PROC = 3e-5
SPECS = [(nm, MULTI_TARGET, ZONE_MASK[(ZONES[nm][0], ZONES[nm][1])])
         for nm in ("A", "B", "C")]

# exp19's discovered policy (results/exp19_anchored_cem.json) and HAND
DISC = {"write_age": 14.5, "start_age": 31.5, "period": 2.5, "budget": 9,
        "k_anchor": 0.32615456103626106, "boost_pv": 0.0,
        "boost_pu": 0.3686716946123514, "boost_f": 1.05936261826428,
        "h_proc": H_PROC}
HAND = {"write_age": 5.0, "start_age": 30.0, "period": 5.0, "budget": 6,
        "k_anchor": 0.25, "boost_pv": 0.0, "boost_pu": 0.0,
        "boost_f": 1.0, "h_proc": H_PROC}
STATUS_QUO = {"write_age": 5.0, "start_age": 30.0, "period": 5.0,
              "budget": 6, "k_anchor": 0.25, "boost_pv": 0.0,
              "boost_pu": 0.0, "boost_f": 1.0, "h_proc": 0.0}

ARMS = {
    "disc":       {"policy": DISC,   "solo": False},
    "hand":       {"policy": HAND,   "solo": False},
    "disc_b2":    {"policy": {**DISC, "budget": 2}, "solo": False},
    "hand_b2":    {"policy": {**HAND, "budget": 2}, "solo": False},
    "disc_solo":  {"policy": DISC,   "solo": True},
    "hand_solo":  {"policy": HAND,   "solo": True},
    "none":       {"policy": {**HAND, "start_age": 105.0}, "solo": False,
                   "no_maintain": True},
    "status_quo": {"policy": STATUS_QUO, "solo": False},
}


def _p(s):
    print(s, flush=True)


def build25(seed: int, k_anchor: float) -> MultiPatternCohort:
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


def run_arm(arm: str, seed: int) -> dict:
    spec = ARMS[arm]
    pol = spec["policy"]
    solo = spec["solo"]
    ch = build25(seed, pol["k_anchor"])
    codec = None if spec.get("no_maintain") else FidelityCodec(
        n_cells=N_CELLS, budget_per_cycle=pol["budget"], levels=7,
        target_source="anchored")
    rng_local = np.random.default_rng(1234567)
    written = {"done": False}
    seen = set()
    proc_events = np.zeros(K, float)
    rows = {"t": [], "alive": [], "hold": [],
            "IV": {"A": [], "B": [], "C": []},
            "IR": {"A": [], "B": [], "C": []}}
    iv60 = {}

    def intervene(t, cohort):
        nonlocal proc_events
        dt = 0.25
        if not written["done"] and t >= pol["write_age"] - 1e-9:
            written["done"] = True
            for name in (("B",) if solo else ("A", "B", "C")):
                _zone_write(cohort, name)
            proc_events += 15.0 if solo else 45.0   # the write is a
            # procedure (cells written; exp19 counted its 12-cell zone)
            cohort._tgt = (B_SOLO_TARGET if solo else MULTI_TARGET)
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
        if pol["h_proc"] > 0:
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
                if solo:
                    led = cohort.pattern_ledger(ref=B_SOLO_TARGET,
                                                zone=B_MASK)
                    ir_mean = float(led["I_recoverable"])
                    rows["IV"]["B"].append(float(led["I_V"]))
                    rows["IR"]["B"].append(ir_mean)
                    hold = alive_f * ir_mean
                else:
                    led = cohort.pattern_ledgers(SPECS)
                    ir_vals = [led[nm]["I_recoverable"]
                               for nm in ("A", "B", "C")]
                    for nm in ("A", "B", "C"):
                        rows["IV"][nm].append(float(led[nm]["I_V"]))
                        rows["IR"][nm].append(float(led[nm]["I_recoverable"]))
                    ir_mean = float(np.mean(ir_vals))
                    hold = alive_f * ir_mean
                rows["t"].append(float(a))
                rows["alive"].append(alive_f)
                rows["hold"].append(hold)
                if abs(a - 60.0) < 0.13 and not solo:
                    for nm, ref, zone in SPECS:
                        iv60[nm] = float(_per_individual(
                            cohort, zone, ref, "I_V").mean())

    s = ch.run(years=YEARS, dt=0.25, intervention=intervene)
    s["rows"] = {k: (v if isinstance(v, list) else {n: list(x)
                                                    for n, x in v.items()})
                 for k, v in rows.items()}
    s["hold_mean"] = float(np.mean(rows["hold"])) if rows["hold"] else 0.0
    s["median"] = float(s["median_lifespan"])
    s["restored"] = codec.restored if codec else 0
    s["IV60"] = iv60
    i60 = next((i for i, tt in enumerate(rows["t"]) if abs(tt - 60) < .2),
               None)
    s["alive_frac_60"] = (float(rows["alive"][i60]) if i60 is not None
                          else float("nan"))
    return s


def _agg(arm: str, rows: list) -> dict:
    hold = [r["hold_mean"] for r in rows]
    hold_curve = [float(np.mean(x)) for x in
                  zip(*[r["rows"]["hold"] for r in rows])]
    t = rows[0]["rows"]["t"]
    entry = {
        "hold_mean": float(np.mean(hold)),
        "hold_by_seed": [float(h) for h in hold],
        "hold_curve": hold_curve,
        "hold_t": t,
        "median": float(np.mean([r["median"] for r in rows])),
        "restored": float(np.mean([r["restored"] for r in rows])),
        "alive_frac_60": float(np.nanmean([r["alive_frac_60"]
                                           for r in rows])),
        "IV60": {nm: float(np.nanmean([r["IV60"][nm] for r in rows
                                        if nm in r["IV60"]]))
                 for nm in ("A", "B", "C")
                 if any(nm in r["IV60"] for r in rows)},
    }
    for nm in ("A", "B", "C"):
        curves = [r["rows"]["IV"][nm] for r in rows
                  if len(r["rows"]["IV"][nm])]
        if curves:
            entry[f"IV_curve_{nm}"] = [float(np.nanmean(x))
                                       for x in zip(*curves)]
    return entry


def main() -> dict:
    t0 = time.time()
    _p("exp25 — the century-hold policy vs competition (exp19's "
       "discovered 8-dim policy transplanted into exp23's stack)")
    _p(f"    K={K}, {YEARS:.0f}yr, seeds {SEEDS} (held-out for the "
       f"discovered policy; matches exp23's regression anchor)")
    out = {}
    for arm in ARMS:
        rows = [run_arm(arm, sd) for sd in SEEDS]
        out[arm] = _agg(arm, rows)
        e = out[arm]
        iv = "  ".join(f"{nm} {e['IV60'][nm]:5.3f}"
                       for nm in ("A", "B", "C") if nm in e["IV60"])
        _p(f"    {arm:11s}: hold {e['hold_mean']:.3f}  "
           f"median {e['median']:6.1f}  restored {e['restored']:6.0f}  "
           f"{iv}")

    disc, hand = out["disc"], out["hand"]
    cost_disc = out["disc_solo"]["hold_mean"] - disc["hold_mean"]
    cost_hand = out["hand_solo"]["hold_mean"] - hand["hold_mean"]
    with open(EXP23) as f:
        e23 = json.load(f)["arms"]["default"]["6"]
    sq = out["status_quo"]
    r_ok = all(abs(sq["IV60"][nm] - e23["I_V_at_60"][nm]) < 0.005
               for nm in ("A", "B", "C")) \
        and abs(sq["median"] - e23["median"]) < 0.5

    crit = {
        "S1_transfer": bool(disc["hold_mean"] >= hand["hold_mean"]),
        "S2_cost_asymmetry": bool(cost_disc < cost_hand),
        "S3_equilibrium_invariance": bool(
            disc["IV60"]["A"] > disc["IV60"]["B"]
            and disc["IV60"]["A"] > disc["IV60"]["C"]),
        "S4_stress_b2": bool(out["disc_b2"]["hold_mean"]
                             >= out["hand_b2"]["hold_mean"]),
        "R_regression_vs_exp23": bool(r_ok),
    }
    results = {
        "exp": "exp25_cem_competition",
        "transplanted_policy": DISC,
        "hand_policy": HAND,
        "arms": out,
        "criteria": crit,
        "competition_costs": {"disc": float(cost_disc),
                              "hand": float(cost_hand)},
        "exp19_reference": {"disc_hold": 0.582, "hand_hold": 0.575,
                            "note": "single-pattern held-out (seeds "
                                    "31-33); exp25 re-evaluates BOTH in "
                                    "the multi-pattern world on seeds "
                                    "21-23 (held-out for the policy, "
                                    "matched to exp23's anchor)"},
        "hold_definition": "alive_fraction x mean I_recoverable over "
                           "A/B/C at ages 30..100 (solo arms: B alone)",
        "S2_composition_caveat": "the solo-vs-multi delta crosses metric "
                                "compositions (solo scores the volatile "
                                "B alone; multi scores the mean over "
                                "A/B/C where 2/3 of the novel load sits "
                                "on easier physics) — the WITHIN-world "
                                "disc-vs-hand comparison is clean; the "
                                "cross-world cost has this composition "
                                "term recorded alongside it",
        "horizon_note": "120yr run horizon (exp23's convention) after a "
                        "105yr first pass showed pure censoring artifacts "
                        "in death-age medians; hold always integrates "
                        "30..100",
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    _p(f"    competition costs: disc {cost_disc:+.3f}  "
       f"hand {cost_hand:+.3f}")
    _figure(results)
    _p(f"exp25 complete in {time.time()-t0:.0f}s")
    return results


def _figure(results: dict) -> None:
    setup()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4),
                           constrained_layout=True)
    t = results["arms"]["disc"]["hold_t"]

    # (a) hold curves: the transplant world
    for nm, c in (("disc", PALETTE["good"]), ("hand", PALETTE["accent"]),
                  ("disc_b2", PALETTE["good"]), ("hand_b2",
                                                 PALETTE["accent"]),
                  ("none", "0.6")):
        ls = "-" if nm in ("disc", "hand", "none") else "--"
        ax[0].plot(t, results["arms"][nm]["hold_curve"], ls=ls, lw=2.2,
                   color=c if nm != "none" else "0.6",
                   label=nm + ("" if ls == "-" else " (b2)"))
    ax[0].set(xlabel="age (yr)", ylabel="hold = alive x mean I_rec",
              ylim=(0, 1.02),
              title="the century-hold policy under competition")
    ax[0].legend(fontsize=8)

    # (b) solo vs multi: the competition cost, per policy
    names = ["disc", "hand"]
    solo = [results["arms"][n + "_solo"]["hold_mean"] for n in names]
    multi = [results["arms"][n]["hold_mean"] for n in names]
    w = 0.32
    x = np.arange(2)
    ax[1].bar(x - w / 2, solo, width=w, color=PALETTE["good"],
              label="solo (no competition)")
    ax[1].bar(x + w / 2, multi, width=w, color=PALETTE["accent"],
              label="multi (3 + birth compete)")
    for i in range(2):
        ax[1].annotate(f"cost {solo[i]-multi[i]:+.3f}",
                       (i, max(solo[i], multi[i]) + 0.03),
                       ha="center", fontsize=8)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(names)
    ax[1].set(ylabel="hold (mean over 30..100)", ylim=(0, 1.0),
              title="the competition cost, per policy")
    ax[1].legend(fontsize=8)

    # (c) per-pattern I_V curves under disc (the equilibrium law check)
    for nm, c in (("A", PALETTE["good"]), ("B", PALETTE["accent"]),
                  ("C", PALETTE["warn"])):
        ax[2].plot(t, results["arms"]["disc"][f"IV_curve_{nm}"],
                   lw=2.0, color=c, label=nm)
    ax[2].set(xlabel="age (yr)", ylabel="I_V", ylim=(0, 1.0),
              title="per-pattern hold under the discovered policy")
    ax[2].legend(fontsize=8)

    fig.suptitle("exp25 — century-hold CEM policy vs the multi-pattern "
                 "stack", fontsize=12)
    fig.savefig(fig_path("fig22_cem_competition"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig22_cem_competition.png")


if __name__ == "__main__":
    main()
