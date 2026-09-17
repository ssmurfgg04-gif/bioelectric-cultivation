#!/usr/bin/env python3
"""exp162 — THE ZERO-SUBSTRATE PROBE (the blocked path, one new mechanism;
Stage 5; the exp68 blocker re-attacked at the temporal level).

THE BLOCKER (L49, exp68): the naive floating-pattern star — write a
2-zone target the substrate's label structure cannot support and have
it PERSIST — is blocked by the DYNAMICS, robustly across five
formalizations (b2v, label energy, mean per-node force, algebraic
connectivity lambda2, conductance: all five separate the pass/fail
sets, CF-G3). L49's own honest report: the 101% path needs a NEW
MECHANISM, not a re-metricization.

THE ONE CANDIDATE MECHANISM (this probe's object):
  TEMPORAL COHERENCE WITHOUT SPATIAL SUPPORT. The deadline law
  (L128/L133, exp149/exp154) established that WHEN mu fires matters as
  much as WHERE V is — the same spatial content breaks or rescues
  depending on the mu-latch timing alone (the half-plane
  0.2930*x + 0.3650*y - 4.6258 > 0 is a statement about trajectory
  timing, not endpoint support). TRANSPLANTED TO THE WRITE PROBLEM:
  the pattern may be carried in the TIMING of the interventions
  themselves — a schedule, not a substrate. The medium is MEMORYLESS:
  every node's identity (V AND theta) is reset bit-exactly to ground
  between intervention rounds; nothing persists but the schedule.

THE TEST: write exp68's canonical REFUSED 2-zone target (the
fixed-index labeling on the 10x10 torus, b2v = 0.110 > 0.10, the
star's fail case) using ONLY scheduled interventions — one clamp
window (the target's non-ground zone, the minimal spatial content any
write must have) plus the deadline protocol's own mu-latch — on the
memoryless medium, then ask whether the written pattern PERSISTS
>= 1 read window after the schedule ends.

=====================================================================
PRE-REGISTRATION (deposited BEFORE running; nothing below the RUN
marker was executed when this docstring was committed; all constants
inherited from the record — zero new knobs):
=====================================================================

MEDIUM (memoryless): exp68's torus(10,10) verbatim (100 nodes,
4-regular). GROUND = TRUNK_V = -50.0 mV (the constructor's native
ground). Memoryless protocol: BEFORE every intervention round (and
before round 0, overwriting the constructor's noisy init) the state
is reset bit-exactly: release_clamps(); V[:] = GROUND; theta[:] =
GROUND; each reset is asserted np.array_equal on both arrays. R = 3
identical rounds; round-independence is ASSERTED (below), which makes
the verdict R-invariant (R is provably not a knob).

TARGET (the blocked star, inherited verbatim): exp43/exp68's
fixed-index labeling(n=100): first 25 nodes HEAD_V = -20.0, the rest
GROUND. exp68's own metrics() is run on (torus, labeling) and the
full 5-formalization separator values are deposited — this is WHICH
static formalizations refuse the target. exp68's deposited verdict:
torus|fixed err 8.47, b2v 0.110 — refused.

THE SCHEDULE RULE (zero-knob; the deadline protocol's own shape,
transplanted to the write): per round of W = 48.0 t.u.
(WINDOW 24.0 = exp124's WINDOW_H, then a TAIL 24.0 at clamp-release —
the regime where exp124's late latches acted), dt = 0.1:
  - EVENT C (the spatial content, minimal): clamp the target's
    non-ground zone (head indices) at HEAD_V for the WINDOW [0, 24)
    only; released for the TAIL. Zone B is ground and
    reset-guaranteed; the write intervenes ONLY where the target
    leaves ground.
  - EVENT M (the temporal lever — the deadline move): mu = MU_FULL
    (0.015, exp124's full-mu level) from round start until the latch
    onset t_s, then mu = 0.0 exactly (exp124's maybe() semantics:
    latched once, silenced for the rest of the round AND the read).
  - THE SCHEDULE (a priori) = t_s = 24.0: the latch at the
    WINDOW/TAIL boundary — the deadline law's canonical edge form.
  - THE BATTERY (the mechanism's fairness arm, zero new constants):
    t_s over exp124's deposited ONSETS that lie in [0, W]:
    (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0) — 7 candidates, all run.
  - READ: after the final round, a free run of 24.0 t.u. (exp68's
    settle duration; exp68's own measurement conditions), mu left as
    the schedule left it (0.0 for every candidate), trajectory
    sampled at read t = 0, 6, 12, 18, 24.
  - SEEDS (1, 2, 3) = exp68's; noise_std = 0.0 (exp149's
    stream-preserving determinism delta) so the bit-exactness gates
    below are exact.

GATES (scored exactly as written; either verdict is a win — this
probe exists to close the question honestly):

  Z1  PERSISTENCE: THE schedule's mean-over-seeds pattern_error at
      READ-END (t = 24 of the read) < 6.0 (exp68's own ERR_BAR and
      statistic). PASS = the written pattern persisted one full read
      window after the schedule ended — the blocked path reopens at
      stage 1. The full battery is reported alongside; a BATTERY
      member passing the same cell criterion while THE schedule fails
      is pre-registered as a success variant ("battery-member
      rescue", the member's timing named as the operating point).

  Z2  TIMING LOAD-BEARING: the same schedule content with SHUFFLED
      timing does NOT write the pattern. Shuffle pool: 5 fixed-seed
      latch onsets u_s ~ U[0, W] (np.random.default_rng(s), s in
      1..5, rounded to the dt grid; drawn values deposited), clamp
      content identical, seeds 1-3 each. PASS iff NO shuffle cell's
      mean-over-seeds read-end err < 6.0. (If Z1 fails, Z2 is
      consistent-but-moot; both are deposited. If a SHUFFLE writes
      while THE schedule does not, that is a writer cell under Z4's
      census and is reported as such — timing would then be
      load-bearing with the a priori latch mis-placed.)

  Z3  RESET HONESTY (prerequisite for ANY verdict to be scorable):
      (a) bit-exact reset asserts: 0 violations across every reset in
      every run (V and theta array_equal to ground each time);
      (b) ROUND-INDEPENDENCE: for THE schedule, seed 1, the R = 3
      run's (V, theta) at read-start AND its read trajectory are
      bit-identical (np.array_equal) to the R = 1 run's — the direct
      proof that nothing persists but the schedule; (c) the
      prerequisite instrument anchor: exp68's sim_supports protocol
      verbatim (default noise_std, seeds 1-3, theta = labeling,
      V = theta + N(0,2), run(24)) reproduces the deposited
      torus|fixed mean err 8.47 within +-1.0 (exp73's fidelity bar).
      If any Z3 member fails: deposit and STOP — no verdict scored.
      BOUNDEDNESS + CARRIER DISSECTION (deposited for every cell):
      the read trajectory (bounded measurement, no single-endpoint
      claim), theta's deviation from ground at read-end
      (RMSE + max), max|V - theta|, and zone-A mean theta — naming
      the carrier if persistence occurs (theta-carried = the schedule
      installed a theta memory; V-carried = flagged for immediate
      re-examination as the stronger claim).

  Z4  PRE-REGISTERED VERDICT (both ways, decided by the writer census
      over the 12 timing cells = 7 battery + 5 shuffles):
      - SUCCESS (the blocked path reopens) iff at least one timing
        cell writes AND not all do (1 <= |WRITERS| <= 11) AND Z3
        passes. Mechanism name deposited: TEMPORAL COHERENCE — the
        write's persistence is carried by the schedule's timing
        structure, with the carrier (theta vs V) named by the Z3
        dissection and the writing timing(s) named.
      - FAILURE (the constraint's 6th formalization CONFIRMED) iff
        NO timing cell writes AND Z3 passes. Deposit WHICH class:
        the TEMPORAL-SCHEDULE formalization class (6th) — the
        deadline law's own mu-latch family transplanted from the
        break/rescue question to the write/persist question, swept
        over its entire deposited onset space at fixed minimal clamp
        content on a bit-exact-reset memoryless medium — AGREES with
        the five static formalizations: the refused labeling is
        unwritable-persistently at every deposited timing; the
        temporal-coherence escape route is CLOSED at this probe's
        scope. The scope statement and falsification conditions are
        deposited with the verdict.
      - DEGENERATE (all 12 cells write, or Z3 fails): deposit, own,
        no mechanism claim either way.

RUN: 1 anchor arm + 7 battery x 3 seeds x 3 rounds + 5 shuffles x
3 seeds x 3 rounds + round-independence arms. Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.substrate.graph import GraphCollective  # noqa: E402
from experiments.exp43_substrate_independence import (  # noqa: E402
    HEAD_N, HEAD_V, TRUNK_V, labeling,
)
from experiments.exp68_coherence_search import metrics, sim_supports, torus  # noqa: E402

OUT = os.path.join(ROOT, "results", "exp162_zero_substrate.json")

# ---- inherited constants (the record's own; zero new knobs) -------------
N = 100
DT = 0.1
WINDOW_H = 24.0          # exp124's WINDOW_H — the clamp window
TAIL_H = 24.0            # the deadline tail (clamp released, latch regime)
ROUND_H = WINDOW_H + TAIL_H
READ_H = 24.0            # exp68's settle duration — one read window
ERR_BAR = 6.0            # exp68's ERR_BAR and statistic (mean over seeds)
MU_FULL = 0.015          # exp124's full-mu level (the stack default)
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0)  # exp124's ONSETS n [0,W]
THE_SCHEDULE_ONSET = 24.0  # a priori: latch at the WINDOW/TAIL boundary
SEEDS = (1, 2, 3)        # exp68's seeds
ROUNDS = 3               # provably inert (round-independence assert)
SHUFFLE_SEEDS = (1, 2, 3, 4, 5)
ANCHOR_DEPOSIT = 8.47    # exp68's deposited torus|fixed mean err
ANCHOR_TOL = 1.0         # exp73's fidelity bar
GROUND = TRUNK_V

# ============================ RUN ========================================


def ground_reset(c: GraphCollective) -> None:
    """The memoryless reset: bit-exact identity wipe (V and theta)."""
    c.release_clamps()
    c.V[:] = GROUND
    c.theta[:] = GROUND


def run_round(c: GraphCollective, onset: float) -> None:
    """One schedule round: clamp window + mu-latch, exp124's semantics."""
    c.mu = MU_FULL
    c.clamp(slice(0, HEAD_N), HEAD_V)
    t0 = 0.0
    for _ in range(int(round(ROUND_H / DT))):
        t0 += DT
        if t0 >= onset:          # exp124's maybe(): latch once, mu -> 0
            c.mu = 0.0
        c.step(DT)
    c.release_clamps()


def free_read(c: GraphCollective) -> tuple[list[float], np.ndarray, np.ndarray]:
    """One read window (24 t.u. free run); trajectory at 0/6/12/18/24."""
    traj = []
    sample = int(round(6.0 / DT))
    for k in range(int(round(READ_H / DT))):
        if k % sample == 0:
            traj.append(float(c.pattern_error(c.phi_read_target)))
        c.step(DT)
    traj.append(float(c.pattern_error(c.phi_read_target)))
    return traj, c.V.copy(), c.theta.copy()


def run_cell(adj: np.ndarray, seed: int, onset: float, rounds: int,
             ground_vec: np.ndarray, target: np.ndarray,
             reset_violations: list[int]) -> dict:
    """One full probe cell: R memoryless rounds + one read window."""
    c = GraphCollective(adjacency=adj, seed=seed, noise_std=0.0)
    c.phi_read_target = target
    for _ in range(rounds):
        ground_reset(c)
        if not (np.array_equal(c.V, ground_vec)
                and np.array_equal(c.theta, ground_vec)):
            reset_violations.append(seed)
        run_round(c, onset)
    mu_at_read = float(c.mu)
    traj, V_end, th_end = free_read(c)
    zone_a = np.where(target == HEAD_V)[0]
    return {
        "traj": [round(x, 4) for x in traj],
        "err_read_end": round(traj[-1], 4),
        "mu_at_read": mu_at_read,
        "theta_rmse_from_ground": round(
            float(np.sqrt(np.mean((th_end - GROUND) ** 2))), 4),
        "theta_max_dev": round(float(np.max(np.abs(th_end - GROUND))), 4),
        "v_theta_gap_max": round(float(np.max(np.abs(V_end - th_end))), 4),
        "zoneA_theta_mean": round(float(np.mean(th_end[zone_a])), 4),
        "V_end": V_end, "theta_end": th_end,
    }


def main() -> dict:
    t_start = time.time()
    print("=== exp162: the zero-substrate probe ===\n")

    adj = torus(10, 10)
    target = labeling(N)
    ground_vec = np.full(N, GROUND)
    zone_a = np.where(target == HEAD_V)[0]
    m = metrics(adj, target)
    print(f"  target: exp43 fixed labeling on exp68 torus; "
          f"b2v={m['b2v']:.3f} E={m['label_energy']:.0f} "
          f"lam2={m['lambda2']:.3f} cond={m['conductance']:.3f}")

    # ---- Z3(c): the instrument anchor (exp68's protocol verbatim) --------
    ok_anchor, mean_err_anchor = sim_supports(adj, target)
    anchor_delta = mean_err_anchor - ANCHOR_DEPOSIT
    anchor_ok = abs(anchor_delta) <= ANCHOR_TOL
    print(f"  anchor: exp68 sim_supports torus|fixed err {mean_err_anchor:.2f} "
          f"(deposit {ANCHOR_DEPOSIT}, delta {anchor_delta:+.2f}) "
          f"{'OK' if anchor_ok else 'BROKEN'}\n")

    # ---- the battery + shuffle pool --------------------------------------
    reset_violations: list[int] = []
    battery: dict[str, dict] = {}
    for onset in ONSETS:
        cells = [run_cell(adj, s, onset, ROUNDS, ground_vec, target,
                          reset_violations) for s in SEEDS]
        mean_err = float(np.mean([x["err_read_end"] for x in cells]))
        battery[f"onset_{onset:.0f}"] = {
            "per_seed_err_read_end": [x["err_read_end"] for x in cells],
            "mean_err_read_end": round(mean_err, 4),
            "mean_traj": [round(float(np.mean([x["traj"][k] for x in cells])), 4)
                          for k in range(len(cells[0]["traj"]))],
            "dissection": {k: cells[0][k] for k in
                           ("theta_rmse_from_ground", "theta_max_dev",
                            "v_theta_gap_max", "zoneA_theta_mean",
                            "mu_at_read")},
            "writes": bool(mean_err < ERR_BAR),
            "cells": [{k: v for k, v in x.items()
                       if k not in ("V_end", "theta_end")} for x in cells],
        }
        tag = " WRITER" if mean_err < ERR_BAR else ""
        print(f"  battery t_s={onset:4.1f}  read-end err mean "
              f"{mean_err:6.3f}  traj {battery[f'onset_{onset:.0f}']['mean_traj']}"
              f"{tag}")

    shuffle_onsets = {}
    shuffles: dict[str, dict] = {}
    for s in SHUFFLE_SEEDS:
        u = round(float(np.random.default_rng(s).uniform(0.0, ROUND_H)), 1)
        shuffle_onsets[str(s)] = u
    for s in SHUFFLE_SEEDS:
        onset = shuffle_onsets[str(s)]
        cells = [run_cell(adj, seed, onset, ROUNDS, ground_vec, target,
                          reset_violations) for seed in SEEDS]
        mean_err = float(np.mean([x["err_read_end"] for x in cells]))
        shuffles[f"shuffle_seed_{s}"] = {
            "onset": onset,
            "per_seed_err_read_end": [x["err_read_end"] for x in cells],
            "mean_err_read_end": round(mean_err, 4),
            "mean_traj": [round(float(np.mean([x["traj"][k] for x in cells])), 4)
                          for k in range(len(cells[0]["traj"]))],
            "writes": bool(mean_err < ERR_BAR),
        }
        print(f"  shuffle s={s} t_s={onset:4.1f}  read-end err mean "
              f"{mean_err:6.3f}{' WRITER' if mean_err < ERR_BAR else ''}")

    # ---- Z3(b): round-independence (nothing persists but the schedule) ---
    c3 = run_cell(adj, 1, THE_SCHEDULE_ONSET, ROUNDS, ground_vec, target,
                  reset_violations)
    c1 = run_cell(adj, 1, THE_SCHEDULE_ONSET, 1, ground_vec, target,
                  reset_violations)
    dv = float(np.max(np.abs(c3["V_end"] - c1["V_end"])))
    dth = float(np.max(np.abs(c3["theta_end"] - c1["theta_end"])))
    dt_traj = float(np.max(np.abs(np.array(c3["traj"])
                                  - np.array(c1["traj"]))))
    round_indep = bool(dv == 0.0 and dth == 0.0 and dt_traj == 0.0)
    print(f"\n  round-independence (R=3 vs R=1, THE schedule, seed 1): "
          f"max|dV|={dv:.3e} max|dtheta|={dth:.3e} max|dtraj|={dt_traj:.3e} "
          f"{'BIT-EXACT' if round_indep else 'VIOLATED'}")
    print(f"  reset asserts: violations = {len(reset_violations)} "
          f"(every reset in every run, V and theta array_equal to ground)")

    # ---- gate scoring -----------------------------------------------------
    the_cell = battery["onset_24"]
    z1 = bool(the_cell["writes"])
    battery_writers = [k for k, v in battery.items() if v["writes"]]
    battery_rescue = bool(battery_writers)  # success variant
    shuffle_writers = [k for k, v in shuffles.items() if v["writes"]]
    z2 = bool(not shuffle_writers)
    z3 = bool(anchor_ok and round_indep and len(reset_violations) == 0)

    writers = sorted(battery_writers + shuffle_writers)
    n_cells = len(battery) + len(shuffles)
    if not z3:
        verdict = ("INSTRUMENT FAILURE — deposit and STOP; no verdict "
                   "scored (Z3 prerequisite failed)")
        mechanism = None
        fclass = None
    elif not writers:
        verdict = ("FAILURE — the coherence constraint's 6th formalization "
                   "CONFIRMED at the temporal level")
        mechanism = None
        fclass = ("TEMPORAL-SCHEDULE class (6th): the deadline law's "
                  "mu-latch family transplanted to the write/persist "
                  "question, swept over its entire deposited onset space "
                  "{0,6,12,18,24,36,48} + 5 shuffled timings at fixed "
                  "minimal clamp content on a bit-exact-reset memoryless "
                  "torus — the class AGREES with the five static "
                  "formalizations (b2v, label energy, mean force, lambda2, "
                  "conductance): the refused labeling is "
                  "unwritable-persistently at every deposited timing; the "
                  "temporal-coherence escape route is CLOSED at this "
                  "probe's scope")
    elif len(writers) >= n_cells:
        verdict = ("DEGENERATE — every timing cell writes; timing is not "
                   "load-bearing; owned, no mechanism claim either way")
        mechanism = None
        fclass = None
    else:
        verdict = ("SUCCESS — the blocked path reopens: "
                   "TEMPORAL COHERENCE WITHOUT SPATIAL SUPPORT")
        mechanism = ("TEMPORAL COHERENCE — the write's persistence is "
                     "carried by the schedule's timing structure; writing "
                     f"timings: {writers}; carrier per Z3 dissection")
        fclass = None

    # carrier attribution for the record (theta- vs V-carried)
    best = min(battery.values(), key=lambda v: v["mean_err_read_end"])
    carrier = {
        "theta_rmse_from_ground_at_best_cell":
            best["dissection"]["theta_rmse_from_ground"],
        "theta_max_dev_at_best_cell":
            best["dissection"]["theta_max_dev"],
        "v_theta_gap_max_at_best_cell":
            best["dissection"]["v_theta_gap_max"],
        "zoneA_theta_mean_at_best_cell":
            best["dissection"]["zoneA_theta_mean"],
        "reading": (
            "theta-carried if theta deviates from ground in the target's "
            "direction at read-end (the schedule installed a theta memory "
            "— support CREATED by the schedule, not pre-existing); "
            "V-carried impossible-looking after 24 t.u. of gamma "
            "relaxation — would be flagged for immediate re-examination"),
    }

    out = {
        "exp": "exp162_zero_substrate (the zero-substrate probe)",
        "pre_registration": "see the module docstring (deposited before "
                            "running; zero new knobs — every constant "
                            "inherited from exp43/exp68/exp124/exp149)",
        "medium": {
            "adjacency": "exp68 torus(10,10) verbatim",
            "ground_mV": GROUND,
            "memoryless_protocol": "bit-exact reset (V and theta) to "
                                   "ground before every round incl. "
                                   "round 0; R=3 rounds; "
                                   "round-independence asserted",
            "noise_std": 0.0,
            "determinism_note": "exp149's stream-preserving delta; "
                                "bit-exact gates are exact",
        },
        "target": {
            "labeling": "exp43 fixed-index (first 25 = -20.0, rest -50.0)",
            "static_formalization_values": m,
            "exp68_deposit": {"torus|fixed_err": 8.47, "b2v": 0.110,
                              "verdict": "refused (5/5 formalizations)"},
        },
        "schedule_rule": {
            "window_clamp": f"head zone clamped at {HEAD_V} for "
                            f"[0, {WINDOW_H})",
            "tail": f"clamp released for [{WINDOW_H}, {ROUND_H})",
            "mu_latch": f"mu={MU_FULL} until t_s (exp124 maybe() "
                        "semantics), then 0.0",
            "THE_schedule_onset": THE_SCHEDULE_ONSET,
            "battery_onsets": list(ONSETS),
            "rounds": ROUNDS,
            "read_window": READ_H,
            "seeds": list(SEEDS),
        },
        "anchor": {"mean_err": round(mean_err_anchor, 4),
                   "deposit": ANCHOR_DEPOSIT,
                   "delta": round(anchor_delta, 4),
                   "tol": ANCHOR_TOL, "ok": bool(anchor_ok)},
        "schedule_battery": battery,
        "shuffle_pool": {"drawn_onsets": shuffle_onsets, "cells": shuffles},
        "reset_asserts": {"violations": len(reset_violations),
                          "scope": "every reset in every run"},
        "round_independence": {"max_abs_dV": dv, "max_abs_dtheta": dth,
                               "max_abs_dtraj": dt_traj,
                               "bit_exact": round_indep},
        "gates": {
            "Z1_persistence_THE_schedule": bool(z1),
            "Z1_variant_battery_rescue": battery_rescue,
            "battery_writers": battery_writers,
            "Z2_timing_load_bearing": bool(z2),
            "shuffle_writers": shuffle_writers,
            "Z3_reset_honesty": bool(z3),
        },
        "writer_census": {"writers": writers, "n_cells": n_cells},
        "carrier_dissection": carrier,
        "verdict": verdict,
        "mechanism": mechanism,
        "formalization_class": fclass,
        "wall_seconds": round(time.time() - t_start, 1),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    scored = sum([z1 or battery_rescue, z2, z3])
    print(f"  gates: Z1={z1} (battery-rescue variant: {battery_rescue}) "
          f"Z2={z2} Z3={z3}")
    print(f"  VERDICT: {verdict}")
    print(f"  === wall {out['wall_seconds']} s ===")
    return out


if __name__ == "__main__":
    main()
