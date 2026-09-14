"""Inverse design of intervention POLICIES — let the search find the protocol.

MOTIVATION (the step exp8 did not take)
---------------------------------------
exp1-8 tested HAND-BUILT interventions: fixed schedules chosen by intuition
(codec from age 30, checkup every 5 yr, budget 6, boost 1.25). The gate is
open — verified maintenance pays under pattern-fidelity mortality — but
nobody searched the POLICY SPACE. The inverse question is the one that
matters for intervention discovery:

    Given the arsenal (verified writes, channel restoration, full
    re-derivation), WHAT SCHEDULE maximizes lifespan — and is it anything a
    human would have guessed?

This module defines the policy vector u (8 dimensions covering the full
exp8 arsenal), decodes it into an intervention schedule, and evaluates it
on a FidelityAgingCohort under an honest COST MODEL:

PROCEDURE RISK (the anti-cheat term)
------------------------------------
Therapies are not free. Every cell-write is an invasive procedure (targeted
drug delivery / optogenetic actuation / surgical reprogramming) with a small
permanent iatrogenic hazard h_proc per write-event per year, and every full
re-derivation writes the whole organism (60 events). Without this term the
search trivially discovers "maximum therapy forever"; with it, overservicing
kills and the optimum is a nontrivial ALLOCATION — start age, checkup
density, write budget, regeneration timing, and channel-boost gating all
trade against each other.

The cost is applied IDENTICALLY to hand-built baselines and discovered
policies (fair comparison), and a no-procedure-risk sensitivity arm reports
whether the discovered structure was cost-driven.
"""

from __future__ import annotations

import numpy as np

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec

# ------------------------------------------------------------------ policy space
POLICY_NAMES = [
    "start_age",        # when verified maintenance begins
    "period",           # checkup interval (yr)
    "budget",           # cell-writes per checkup cycle
    "regen_period",     # full re-derivation interval (yr)
    "regen_start",      # age of first re-derivation (>=100: never)
    "boost_p_verified",  # P(channel boost | read verified)
    "boost_p_unverified",  # P(channel boost | read refused) — the gating knob
    "boost_factor",     # connexin boost multiplier per application
]

POLICY_BOUNDS = [
    (20.0, 60.0),
    (1.5, 10.0),
    (1.0, 12.0),
    (8.0, 60.0),
    (25.0, 105.0),
    (0.0, 1.0),
    (0.0, 1.0),
    (1.0, 1.6),
]

# hand-built exp8 reference policy (codec + fully-gated boost), expressed in
# the same 8-dim space — the baseline the search must beat
HAND_CODEC = (30.0, 5.0, 6.0, 60.0, 105.0, 0.0, 0.0, 1.0)
HAND_CHAN = (30.0, 5.0, 6.0, 60.0, 105.0, 1.0, 0.0, 1.25)
HAND_BLIND = (30.0, 5.0, 6.0, 60.0, 105.0, 1.0, 1.0, 1.25)
HAND_REGEN = (30.0, 5.0, 6.0, 20.0, 30.0, 0.0, 0.0, 1.0)
HAND_REGEN_CHAN = (30.0, 5.0, 6.0, 20.0, 30.0, 1.0, 0.0, 1.25)

H_PROC = 3e-5  # 1/yr per write-event — the procedure-risk coefficient


def decode_policy(u) -> dict:
    """Round the continuous vector onto implementable schedules."""
    u = np.clip(np.asarray(u, float), [b[0] for b in POLICY_BOUNDS],
                [b[1] for b in POLICY_BOUNDS])
    start = round(u[0] * 4) / 4
    period = max(0.75, round(u[1] * 4) / 4)
    budget = int(round(u[2]))
    regen_period = max(2.0, round(u[3] * 4) / 4)
    regen_start = round(float(u[4]) * 4) / 4
    return {
        "start_age": start,
        "period": period,
        "budget": budget,
        "regen_period": regen_period,
        "regen_start": regen_start,
        "regen_never": bool(regen_start >= 100.0),
        "boost_p_verified": float(u[5]),
        "boost_p_unverified": float(u[6]),
        "boost_factor": float(u[7]),
    }


def policy_intervention(policy: dict, n_cells: int = 60,
                        age_preset=None, h_proc: float = H_PROC,
                        K: int | None = None, boost_cap: float = 8.0):
    """Build the intervention callback that EXECUTES a decoded policy.

    Returns (callback, stats-dict) — stats filled during the run."""
    codec = FidelityCodec(n_cells=n_cells, budget_per_cycle=policy["budget"])
    proc_events = None  # allocated on first call (needs K)
    stats = {"writes": 0, "regens": 0, "boost_apps": 0, "refused": 0}
    rng_local = np.random.default_rng(1234567)

    def intervene(t, cohort):
        nonlocal proc_events
        dt = 0.25
        if proc_events is None:
            proc_events = np.zeros(cohort.K, float)

        # ---------- scheduled verified maintenance ----------
        if t >= policy["start_age"] - 1e-9 and \
                abs((t - policy["start_age"]) % policy["period"]) <= 0.26:
            preset = age_preset(t)
            rep = codec.maintain(cohort, preset, mode="codec")
            per_i = np.asarray(rep["restored_per_i"], float)
            proc_events += per_i
            stats["writes"] += int(per_i.sum())
            stats["refused"] += rep["refused"]
            # ---------- channel boost with learned gating ----------
            pv, pu = policy["boost_p_verified"], policy["boost_p_unverified"]
            if pv > 0 or pu > 0:
                verified = np.asarray(rep["verified_mask"], bool)
                draw = rng_local.random(cohort.K)
                mask = (verified & (draw < pv)) | (~verified & (draw < pu))
                if mask.any():
                    cohort.boost_channel(mask, policy["boost_factor"], boost_cap)
                    stats["boost_apps"] += int(mask.sum())

        # ---------- scheduled full re-derivation ----------
        if not policy["regen_never"] and t >= policy["regen_start"] - 1e-9 and \
                abs((t - policy["regen_start"]) % policy["regen_period"]) <= 0.26:
            before = int(cohort.alive.sum())
            cohort.regenerate()
            proc_events += 60.0 * cohort.alive  # whole-body re-derivation writes
            stats["regens"] += before

        # ---------- procedure risk (the anti-cheat hazard) ----------
        if h_proc > 0 and proc_events is not None:
            hazard = h_proc * proc_events
            dd = cohort.rng.random(cohort.K)
            died = cohort.alive & (dd < dt * hazard)
            if died.any():
                cohort.death_age[died] = cohort.t
                cohort.alive &= ~died

    return intervene, stats


def eval_policy(u, seed: int, K: int = 150, years: float = 110.0,
                regime: dict | None = None, target0=None, h_proc: float = H_PROC,
                age_preset=None, boost_cap: float = 8.0,
                cohort_kw: dict | None = None) -> dict:
    """Evaluate one policy vector on one cohort. Top-level (picklable).

    cohort_kw: constructor overrides for FidelityAgingCohort (jump_rate,
    f_crit, k_fail) — the landscape axes of the robustness tests."""
    policy = decode_policy(u)
    params = AgingParams(n_cells=60, target0=target0(), **(regime or {}))
    ch = FidelityAgingCohort(K=K, params=params, seed=seed, **(cohort_kw or {}))
    intervene, stats = policy_intervention(
        policy, age_preset=age_preset, h_proc=h_proc, boost_cap=boost_cap)
    s = ch.run(years=years, dt=0.25, intervention=intervene, record=False)
    return {
        "median": s["median_lifespan"],
        "max": s["max_lifespan"],
        "survivors": s["survivors_at_end"],
        "writes": stats["writes"],
        "regens": stats["regens"],
        "boost_apps": stats["boost_apps"],
        "refused": stats["refused"],
        "policy": policy,
    }


def eval_policy_seeds(u, seeds, **kw) -> dict:
    """Mean over seeds — the held-out evaluation used after the search."""
    rs = [eval_policy(u, seed=s, **kw) for s in seeds]
    out = {k: float(np.mean([r[k] for r in rs])) for k in ("median", "max", "writes",
                                                           "regens", "boost_apps")}
    out["medians_by_seed"] = [r["median"] for r in rs]
    out["policy"] = rs[0]["policy"]
    return out
