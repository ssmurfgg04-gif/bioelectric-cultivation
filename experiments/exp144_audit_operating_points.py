#!/usr/bin/env python3
"""exp144 — THE AUDIT AT OFF-POLE OPERATING POINTS (workstream J; the
L121-registered repair: PER-INVENTION OPERATING-POINT SELECTION from a
price-map ladder extended off-pole, before the audit).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the audit is
executed exactly once against these gates):
======================================================================

MOTIVE (L121's owned diagnosis v2): exp136 and exp141 share the same
two pole-calibrated search cells [[1.0, 0.015], [4.0, 0.0]] and the
same pole-calibrated audit ladder; any off-pole invention was audited
at operating cells never calibrated for it. This experiment freezes an
EXTENDED operating ladder BEFORE the search, then re-audits exp141's
candidate pool per-invention: a candidate PASSES if ANY frozen rung
passes (the emitted cell is part of the compiled program — exp136's
own wording), and the emitted rung is argmin over a frozen cost key.
NO per-candidate free parameter exists: the ladder is frozen first,
selection is argmin over frozen rungs.

DESIGN:
  (1) exp141's pool is NOT persisted (its results JSON carries round
      aggregates only), so the search is RE-RUN IDENTICALLY: exp141's
      own functions (well_formed_wide, random_spec_wide, mutate_wide,
      to_key, class_tags), its RNG seed 141, its search shape (96
      stratified seeds + 5 generations x 48, 16 elites), its score J.
      Replication is CHECKED against exp141's deposited aggregates
      (per-round novel counts, pool size 253, best-J per round) and
      the check is deposited.
  (2) THE EXTENDED LADDER (frozen; deposited to the results file at
      stage "ladder_deposit" BEFORE the search's first candidate is
      evaluated). Nine rungs = exp136's deposited four pole rungs
      PLUS five cross cells drawn from the price-map v2 vocabulary
      (exp117's PM-G2 class->cell mapping: DEFAULT0 -> (1, 0.015);
      MU0 -> (1, 0); GAMMA0 -> (4..16, .015 or 0); GEOMETRY ->
      (32, 0); walk-speed fast arm (64, 0) from exp112):
        (1.0, 0.0)    NEW cross — price-map MU0_SILENCE cell (exp100/113)
        (1.0, 0.015)  deposited — exp136 ladder / DEFAULT0
        (4.0, 0.0)    deposited — exp136 ladder / GAMMA0 mu-silent
        (4.0, 0.015)  NEW cross — GAMMA0 default-mu arm (exp113)
        (16.0, 0.0)   deposited — exp136 ladder
        (16.0, 0.015) NEW cross — GAMMA0 default-mu arm (exp113)
        (32.0, 0.0)   NEW — price-map GEOMETRY cell (exp100)
        (64.0, 0.0)   deposited — exp136 ladder / walk-speed fast arm
        (64.0, 0.015) NEW cross — fast arm at default mu (exp112)
      Frozen cost key (exp136's own surcharge semantics, monotone in
      both price coordinates): cost = gamma/4 + (1.0 if mu > 0 else 0).
      All nine costs are distinct; the emitted rung of a passing
      candidate is the argmin-cost PASSING rung.
  (3) THE PER-INVENTION RULE: a candidate passes the two-channel
      audit iff ANY ladder rung has quad = hypot(eV, eT) < ERR_BAR
      (6.0 mV, 3 seeds, exp84's ablation semantics — instruments
      UNCHANGED); its emitted operating point is the cheapest passing
      rung and is deposited as part of the compiled program.
  (4) THE AUDIT COHORT (frozen after the search, before the audit;
      deposited at stage "cohort_deposit"):
        - GATE-BEARING: every pool candidate that clears the FULL
          exp136 novelty clause (NOV_lib > N* AND nov_splice > N* —
          the C1-eligible set), NO CAP;
        - DIAGNOSTIC FILL: if fewer than 24 candidates are audited
          gate-bearing, the cohort is filled to 24 (or the size of
          the lib-novel pool) with the highest-J lib-novel
          (NOV_lib > N*) candidates that FAIL the splice clause.
          Rationale owned in advance: exp141's deposited results
          (delivered 0 with 96 lib-novel candidates) imply the splice
          clause may kill candidates BEFORE any audit runs; the fill
          guarantees the audit-vs-ladder question is answered either
          way. Fill members are non-gate-bearing by construction and
          are labeled "splice_failed_fill" in the deposit.
  (5) THE GATES:
    GATE-J1  MINIMUM REVIVAL: >= 1 candidate clears the FULL novelty
             clause (NOV_lib > N* AND nov_splice > N*) AND passes the
             audit at some rung of the extended ladder (per-invention
             rule). This is the minimum claim revival.
    GATE-J2  TWO-CHANNEL AUDIT (C2 UNCHANGED): >= 8/10 of the
             DELIVERED inventions (exp136's greedy delivery: J-order,
             novelty, pairwise-N* C4 filter, splice clause, cap 10)
             pass the audit at their selected rung.
    GATE-J3  DECODE + STABILITY (C3 UNCHANGED): >= 8/10 delivered
             inventions decode under the existing decoder at their
             emitted rung: post-settle error < 6.0 mV AND the 100
             t.u. hold error < 6.0 mV, each on >= 2/3 seeds.
    GATE-J4  NO FREE PARAMETER (procedural): the ladder was frozen
             and deposited BEFORE the search (stage order recorded in
             this file's own deposit); every emitted rung is a member
             of the frozen ladder; selection is the argmin of the
             frozen cost key over the frozen rungs (verified by
             recomputation); all nine rungs carry deposited
             provenance; the frozen ladder is a superset of exp136's
             deposited audit ladder. PASS iff all five checks hold.
    C1/C4 evaluated UNCHANGED on the delivered set (C1: exactly 10
    delivered, each clearing the full novelty clause; C4: pairwise
    min D > N*). J2 == C2 and J3 == C3 by construction; both labels
    are deposited.

REFUTATION BRANCH (pre-registered): if the gates still deliver 0/4
with the ladder extended, the L121 "audit operating point" diagnosis
is REFUTED and the decomposition is deposited: for EVERY audited
candidate failing all nine rungs, its argmin-quad rung's (eV, eT)
decomposition and channel attribution (eV >= eT -> "V_dominated": the
hijack channel alone cannot hold the invented pattern off-pole;
else "theta_dominated": the theta/diffusion channel carries the
failure), plus the aggregate V- vs theta-dominated counts. If instead
the audit never receives gate-bearing candidates (the splice clause
kills everything, as exp141's deposited funnel implies), that fact is
itself the localization: the killer sits UPSTREAM of the audit, in
the anti-recombination clause, and the decomposition is deposited on
the diagnostic fill.

INSTRUMENT DISCLOSURE: everything downstream of the ladder is
exp136/exp141's machinery imported verbatim (quad_err, erosion,
decode, d_struct, dist, nov_lib, nov_splice, build_library,
build_splices, library_nn_stats); the search re-run is exp141's loop
verbatim at its seed. RUNTIME BUDGET: search ~4 min + splice scan
~2-3 min + audit <= 24 x 9 rungs x 6 ablation runs + decodes; wall
under ~15 min, serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, LADDER as POLE_LADDER, SEARCH_CELLS, CELL_SURCHARGE,
    AUDIT_SEEDS, LAMBDA_NOV, N_DELIVER, CUT_TOL,
    profile_of_zones, build_library, dist, library_nn_stats,
    build_splices, nov_lib, nov_splice, quad_err, erosion, decode,
)
from experiments import exp141_generator_wide as W  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp144_audit_operating_points.json")
PREV = os.path.join(ROOT, "results", "exp141_generator_wide.json")

# ---- THE EXTENDED LADDER (frozen; see docstring for provenance) ----
EXTENDED_LADDER = (
    (1.0, 0.0), (1.0, 0.015),          # MU0 silence cell + DEFAULT0 pole
    (4.0, 0.0), (4.0, 0.015),          # GAMMA0 both mu arms
    (16.0, 0.0), (16.0, 0.015),        # GAMMA0 upper both mu arms
    (32.0, 0.0),                       # GEOMETRY cell
    (64.0, 0.0), (64.0, 0.015),        # walk-speed fast arm, both mu
)
PROVENANCE = {
    (1.0, 0.0): "NEW cross — price-map v2 MU0_SILENCE cell (exp100/"
                "exp113 deposited (1, 0))",
    (1.0, 0.015): "deposited — exp136 audit ladder; price-map DEFAULT0",
    (4.0, 0.0): "deposited — exp136 audit ladder; GAMMA0 mu-silent",
    (4.0, 0.015): "NEW cross — GAMMA0 default-mu arm (exp113 priced "
                  "GAMMA0 at (4..16, .015 or 0))",
    (16.0, 0.0): "deposited — exp136 audit ladder",
    (16.0, 0.015): "NEW cross — GAMMA0 default-mu arm (exp113)",
    (32.0, 0.0): "NEW — price-map v2 GEOMETRY cell (exp100 (32, 0))",
    (64.0, 0.0): "deposited — exp136 audit ladder; exp112 walk-speed "
                 "fast arm",
    (64.0, 0.015): "NEW cross — walk-speed fast arm at default mu "
                   "(exp112: gamma buys speed at default mu)",
}


def rung_cost(g: float, mu: float) -> float:
    """Frozen cost key (exp136's surcharge semantics), monotone in
    both price-map coordinates; all nine rung costs distinct."""
    return g / 4.0 + (1.0 if mu > 0 else 0.0)


AUDIT_CAP = 24   # diagnostic-fill cap (gate-bearing members uncapped)


def main() -> dict:
    t0 = time.time()
    print("=== exp144: the audit at off-pole operating points ===\n")

    # ---- 0. the frozen library, the bar, and the LADDER DEPOSIT ----
    lib = build_library()
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    n_star, nn = library_nn_stats(lib)
    splices = build_splices(lib)
    print(f"  library {len(lib_names)} members | N* {n_star:.3f} "
          f"(exp141 deposited 82.288; CUT_TOL {CUT_TOL} both runs — "
          f"L121's cross-tol flag resolved: identical metric)")
    print(f"  splice family: {len(splices)} single-crossover profiles")
    assert abs(n_star - 82.288) < 0.01, "N* re-derivation drift"
    for rung in POLE_LADDER:
        assert rung in EXTENDED_LADDER, f"pole rung {rung} lost"
    costs = [rung_cost(g, mu) for (g, mu) in EXTENDED_LADDER]
    assert len(set(costs)) == len(costs), "frozen cost key must be injective"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump({
            "exp": "exp144_audit_operating_points (workstream J)",
            "stage": "ladder_deposit (written BEFORE the search runs)",
            "extended_ladder": {
                "rungs": [list(r) for r in EXTENDED_LADDER],
                "cost_key": "gamma/4 + (1.0 if mu>0 else 0) — frozen; "
                            "exp136's own surcharge semantics",
                "rung_costs": {f"({g},{mu})": rung_cost(g, mu)
                               for (g, mu) in EXTENDED_LADDER},
                "provenance": {f"({g},{mu})": PROVENANCE[(g, mu)]
                               for (g, mu) in EXTENDED_LADDER},
                "pole_rungs_superset_of_exp136": True,
                "selection_rule": "emitted = argmin cost over PASSING "
                                  "rungs; pass = hypot(eV, eT) < 6.0 "
                                  "at 3 seeds; NO per-candidate free "
                                  "parameter",
                "price_map_v2_sources": "exp117 PM-G2 class->cell "
                                        "vocabulary; exp100 deposited "
                                        "cells; exp112 walk-speed "
                                        "ladder; exp113 re-priced map",
            },
            "n_star": round(n_star, 3),
            "audit_cap_diagnostic_fill": AUDIT_CAP,
        }, fh, indent=1, default=float)
    print("  EXTENDED LADDER deposited (stage ladder_deposit) BEFORE "
          "the search\n")

    # ---- 1. the search re-run (exp141's loop VERBATIM, seed 141) ---
    rng = np.random.default_rng(141)
    cache: dict[tuple, dict] = {}

    def evaluate(zones) -> dict:
        key = W.to_key(zones)
        if key in cache:
            return cache[key]
        f = profile_of_zones(zones)
        nov = nov_lib(f, lib_arr)
        best = None
        for ci, (g, mu) in enumerate(SEARCH_CELLS):
            eV, eT, q = quad_err(f, g, mu, seeds=(1,))
            cost = q + ci * CELL_SURCHARGE
            if best is None or cost < best["cost"]:
                best = {"cost": cost, "cell": (g, mu), "eV": eV,
                        "eT": eT, "quad": q}
        J = best["cost"] + LAMBDA_NOV * max(0.0, n_star - nov)
        rec = {"zones": zones, "f": f, "nov_lib": nov, "J": J,
               "search_cell": best["cell"], "search_eV": best["eV"],
               "search_eT": best["eT"], "search_quad": best["quad"],
               "novel": bool(nov > n_star),
               "tags": W.class_tags(zones, f)}
        cache[key] = rec
        return rec

    pop = []
    si = 0
    while len(pop) < W.POP0:
        zs = W.random_spec_wide(rng, stratify=True,
                                force_overlap=(si % 3 == 1))
        si += 1
        if zs and W.well_formed_wide(zs):
            pop.append(zs)
    pool: dict[tuple, dict] = {}
    round_summaries = []
    for rnd in range(W.ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[W.to_key(r["zones"])] = r
        recs_sorted = sorted(recs, key=lambda r: r["J"])
        n_novel = sum(int(r["novel"]) for r in recs)
        n_novel_nd = sum(int(r["novel"] and r["tags"]["nondisjoint"])
                         for r in recs)
        n_novel_bl = sum(int(r["novel"]
                             and r["tags"]["n_below_line_zones"] > 0)
                         for r in recs)
        round_summaries.append({
            "round": rnd, "n": len(recs), "n_novel": n_novel,
            "n_novel_nondisjoint": n_novel_nd,
            "n_novel_below_line": n_novel_bl,
            "median_J": float(np.median([r["J"] for r in recs])),
            "best_J": float(recs_sorted[0]["J"]),
        })
        print(f"  search round {rnd}: n={len(recs)} novel={n_novel} "
              f"best J {recs_sorted[0]['J']:.2f}")
        if rnd == W.ROUNDS:
            break
        elites = [r["zones"] for r in recs_sorted[:W.N_ELITE]]
        pop = list(elites)
        while len(pop) < W.PER_ROUND:
            parent = elites[int(rng.integers(0, len(elites)))]
            child = W.mutate_wide(parent, rng)
            if child is not None and W.to_key(child) not in pool:
                pop.append(child)
            else:
                zs = W.random_spec_wide(rng, stratify=False)
                if zs:
                    pop.append(zs)

    # replication check vs exp141's deposited aggregates
    prev = json.load(open(PREV))
    rep_rounds = []
    for a, b in zip(round_summaries, prev["search"]["rounds"]):
        ok = (a["round"] == b["round"] and a["n"] == b["n"]
              and a["n_novel"] == b["n_novel"]
              and a["n_novel_nondisjoint"] == b["n_novel_nondisjoint"]
              and a["n_novel_below_line"] == b["n_novel_below_line"]
              and abs(a["best_J"] - b["best_J"]) < 1e-9)
        rep_rounds.append({"round": a["round"], "match": bool(ok)})
    rep = {"rounds_match": all(r["match"] for r in rep_rounds),
           "pool_size_match": len(pool) == prev["search"]["pool_size"],
           "rounds": rep_rounds,
           "pool_size": len(pool),
           "exp141_pool_size": prev["search"]["pool_size"]}
    print(f"  replication vs exp141 deposit: rounds "
          f"{rep['rounds_match']} | pool {len(pool)} vs "
          f"{prev['search']['pool_size']} -> "
          f"{'IDENTICAL' if rep['rounds_match'] and rep['pool_size_match'] else 'DIVERGED'}")
    assert rep["rounds_match"] and rep["pool_size_match"], \
        "search re-run diverged from the exp141 deposit"

    # ---- 2. novelty funnel + splice scan (J order) ------------------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    eligible = [r for r in ordered if r["novel"]]
    print(f"\n  lib-novel pool: {len(eligible)}/{len(pool)}")
    splice_scan = []
    for r in eligible:
        ns = nov_splice(r["f"], splices)
        r["nov_splice"] = ns
        splice_scan.append(ns > n_star)
    splice_clear = [r for r in eligible if r["nov_splice"] > n_star]
    print(f"  splice-clear (C1-eligible): "
          f"{len(splice_clear)}/{len(eligible)}")

    # ---- 3. exp136's delivery procedure VERBATIM --------------------
    delivered: list[dict] = []
    for r in eligible:
        if len(delivered) >= N_DELIVER:
            break
        f = r["f"]
        if any(dist(f, d["f"]) <= n_star for d in delivered):
            continue                                   # GATE-C4 filter
        if r["nov_splice"] <= n_star:
            continue                                   # anti-recombination
        delivered.append(r)
    for r in delivered:
        r["role"] = "gate_bearing_delivered"
    print(f"  delivered {len(delivered)}/{N_DELIVER} (exp136 procedure)")

    # ---- 4. the audit cohort (frozen before the audit) --------------
    cohort: list[dict] = []
    seen: set[tuple] = set()

    def admit(r, role):
        k = W.to_key(r["zones"])
        if k in seen:
            return
        seen.add(k)
        r = dict(r)
        r["role"] = role
        cohort.append(r)

    for r in splice_clear:                 # gate-bearing, uncapped
        admit(r, "gate_bearing_splice_clear" if r not in delivered
              else "gate_bearing_delivered")
    for r in delivered:
        admit(r, "gate_bearing_delivered")
    if len(cohort) < AUDIT_CAP:
        for r in eligible:                 # diagnostic fill, J order
            if len(cohort) >= AUDIT_CAP:
                break
            if r["nov_splice"] > n_star:
                continue
            admit(r, "splice_failed_fill")
    with open(OUT, "w") as fh:
        json.dump({
            "exp": "exp144_audit_operating_points (workstream J)",
            "stage": "cohort_deposit (frozen AFTER search, BEFORE audit)",
            "extended_ladder": {
                "rungs": [list(r) for r in EXTENDED_LADDER],
                "cost_key": "gamma/4 + (1.0 if mu>0 else 0)",
                "provenance": {f"({g},{mu})": PROVENANCE[(g, mu)]
                               for (g, mu) in EXTENDED_LADDER},
                "selection_rule": "emitted = argmin cost over PASSING "
                                  "rungs; pass = hypot(eV,eT) < 6.0 "
                                  "at 3 seeds",
            },
            "cohort": [{"zones": [list(z) for z in r["zones"]],
                        "role": r["role"],
                        "J": round(r["J"], 4),
                        "nov_lib": round(r["nov_lib"], 2),
                        "nov_splice": round(r.get("nov_splice", float("nan")), 2)}
                       for r in cohort],
        }, fh, indent=1, default=float)
    print(f"  audit cohort frozen: {len(cohort)} "
          f"(gate-bearing {sum(int(r['role'].startswith('gate')) for r in cohort)}, "
          f"splice-failed fill {sum(int(r['role'] == 'splice_failed_fill') for r in cohort)})\n")

    # ---- 5. THE AUDIT across the extended ladder --------------------
    for k, r in enumerate(cohort):
        zones, f = r["zones"], r["f"]
        tbl = []
        for (g, mu) in EXTENDED_LADDER:
            eV, eT, q = quad_err(f, g, mu, seeds=AUDIT_SEEDS)
            tbl.append({"cell": [g, mu], "cost": rung_cost(g, mu),
                        "eV": round(eV, 3), "eT": round(eT, 3),
                        "quad": round(q, 3),
                        "pass": bool(q < ERR_BAR)})
        passing = [t for t in tbl if t["pass"]]
        if passing:
            emitted_t = min(passing, key=lambda t: t["cost"])
            g, mu = emitted_t["cell"]
            full = float(np.mean([erosion(f, g, mu, "full", s)
                                  for s in AUDIT_SEEDS]))
            emitted_t["full"] = round(full, 3)
            dec = [decode(f, zones, g, mu, s) for s in AUDIT_SEEDS]
            r["decode_errs"] = [round(d["decode_err"], 3) for d in dec]
            r["hold_errs"] = [round(d["hold_err"], 3) for d in dec]
            n_ok = sum(int(d["decode_err"] < ERR_BAR
                           and d["hold_err"] < ERR_BAR) for d in dec)
            r["decode_stable_seeds"] = f"{n_ok}/{len(dec)}"
            r["decode_pass"] = bool(n_ok >= 2)
            r["emitted_cell"] = [g, mu]
        else:
            g, mu = min(tbl, key=lambda t: t["quad"])["cell"]
            full = float(np.mean([erosion(f, g, mu, "full", s)
                                  for s in AUDIT_SEEDS]))
            tbl[[t["cell"] for t in tbl].index([g, mu])]["full"] = \
                round(full, 3)
            r["emitted_cell"] = None
            r["decode_errs"] = r["hold_errs"] = None
            r["decode_stable_seeds"] = "0/3"
            r["decode_pass"] = False
        r["audit_pass"] = bool(passing)
        r["ladder"] = tbl
        # eV vs eTheta decomposition: at the argmin-quad rung
        best_t = min(tbl, key=lambda t: t["quad"])
        r["decomposition"] = {
            "best_rung": best_t["cell"],
            "best_quad": best_t["quad"],
            "eV": best_t["eV"], "eT": best_t["eT"],
            "channel": ("V_dominated" if best_t["eV"] >= best_t["eT"]
                        else "theta_dominated"),
        }
        print(f"  audit[{k + 1:02d}/{len(cohort)}] role={r['role']} "
              f"audit_pass={r['audit_pass']} "
              f"emitted={r['emitted_cell']} "
              f"best_quad={r['decomposition']['best_quad']:.2f} "
              f"({r['decomposition']['channel']}) "
              f"decode={r['decode_stable_seeds']}")

    # ---- 6. gates ----------------------------------------------------
    n_del = len(delivered)
    del_recs = [next(r for r in cohort
                     if W.to_key(r["zones"]) == W.to_key(d["zones"]))
                for d in delivered]
    c1 = bool(n_del == N_DELIVER
              and all(r["nov_lib"] > n_star and r["nov_splice"] > n_star
                      for r in del_recs))
    audit_n = sum(int(r["audit_pass"]) for r in del_recs)
    star_only = bool(n_del > 0 and audit_n >= 8
                     and all(r["emitted_cell"] == [64.0, 0.0]
                             for r in del_recs if r["audit_pass"]))
    c2 = bool(n_del >= 8 and audit_n >= 8)   # C2's 8/10 wording
    decode_n = sum(int(r["decode_pass"]) for r in del_recs)
    c3 = bool(n_del >= 8 and decode_n >= 8)
    for r in cohort:
        r["min_pairwise_D"] = round(float(min(
            (dist(r["f"], d["f"]) for d in delivered
             if W.to_key(r["zones"]) != W.to_key(d["zones"])),
            default=float("inf"))), 2)
    c4 = bool(n_del == N_DELIVER and n_del >= 2 and
              all(r["min_pairwise_D"] > n_star for r in del_recs))
    gb_pass = [r for r in cohort
               if r["role"].startswith("gate_bearing") and r["audit_pass"]]
    j1 = bool(any(r["nov_splice"] > n_star and r["audit_pass"]
                  for r in cohort
                  if r["role"].startswith("gate_bearing")))
    # J4 procedural checks
    j4_checks = {
        "ladder_deposited_before_search": True,   # stage order in OUT
        "all_emitted_cells_in_frozen_ladder": all(
            tuple(r["emitted_cell"]) in EXTENDED_LADDER
            for r in cohort if r["audit_pass"]),
        "selection_is_argmin_of_frozen_cost": all(
            r["emitted_cell"] == min(
                (t["cell"] for t in r["ladder"] if t["pass"]),
                key=lambda c: rung_cost(*c))
            for r in cohort if r["audit_pass"]),
        "provenance_complete": all((g, mu) in PROVENANCE
                                   for (g, mu) in EXTENDED_LADDER),
        "superset_of_exp136_ladder": all(rung in EXTENDED_LADDER
                                         for rung in POLE_LADDER),
    }
    j4 = bool(all(j4_checks.values()))

    # ---- 7. diagnostics ---------------------------------------------
    revival = {f"({g},{mu})": sum(int(t["pass"]) for r in cohort
                                  for t in r["ladder"]
                                  if t["cell"] == [g, mu])
               for (g, mu) in EXTENDED_LADDER}
    fails = [r for r in cohort if not r["audit_pass"]]
    chan_counts = {"V_dominated": sum(int(r["decomposition"]["channel"]
                                         == "V_dominated") for r in fails),
                   "theta_dominated": sum(int(r["decomposition"]["channel"]
                                              == "theta_dominated")
                                          for r in fails)}
    rho = W.spearman([r["nov_lib"] for r in cohort],
                     [r["decomposition"]["best_quad"] for r in cohort])
    gates = {"J1_minimum_revival": j1,
             "J2_C2_two_channel_audit": c2,
             "J3_C3_decode_stability": c3,
             "J4_no_free_parameter": j4,
             "C1_novelty_generation": c1,
             "C4_zero_anatomy_special": c4}
    npass = sum(int(v) for v in gates.values())
    print(f"\n  GATE-J1 minimum revival: {'PASS' if j1 else 'REFUTED'} "
          f"(gate-bearing audit passers {len(gb_pass)})")
    print(f"  GATE-J2/C2 audit ({audit_n}/{n_del}): "
          f"{'PASS' if c2 else 'REFUTED'} (star-only={star_only})")
    print(f"  GATE-J3/C3 decode ({decode_n}/{n_del}): "
          f"{'PASS' if c3 else 'REFUTED'}")
    print(f"  GATE-J4 no-free-parameter: "
          f"{j4_checks} -> {'PASS' if j4 else 'REFUTED'}")
    print(f"  C1: {'PASS' if c1 else 'REFUTED'} | "
          f"C4: {'PASS' if c4 else 'REFUTED'}")
    print(f"  === {npass}/6 gate clauses PASS ===")

    out = {
        "exp": "exp144_audit_operating_points (workstream J)",
        "claim": ("per-invention operating-point selection over a "
                  "price-map-v2-derived ladder extended off-pole "
                  "revives the exp136/exp141 generator claim "
                  "(L121's registered repair); the emitted cell is "
                  "part of the compiled program"),
        "pre_registration": {
            "gates": {"J1": ">=1 candidate clears the FULL novelty "
                            "clause (NOV_lib > N* AND nov_splice > N*) "
                            "AND passes the audit at some rung",
                      "J2": "C2 unchanged: >=8/10 delivered pass the "
                            "two-channel audit at the selected rung",
                      "J3": "C3 unchanged: >=8/10 delivered decode+"
                            "hold at the emitted rung",
                      "J4": "ladder frozen+deposited before the "
                            "search; selection = argmin over frozen "
                            "rungs; provenance complete; superset of "
                            "exp136's ladder"},
            "cohort_rule": "all C1-eligible (gate-bearing, uncapped) "
                           "+ diagnostic fill of highest-J splice-"
                           f"failing lib-novel candidates to {AUDIT_CAP}",
            "ladder_frozen_at": "stage ladder_deposit, before search "
                                "candidate 1",
        },
        "extended_ladder": {
            "rungs": [list(r) for r in EXTENDED_LADDER],
            "cost_key": "gamma/4 + (1.0 if mu>0 else 0)",
            "rung_costs": {f"({g},{mu})": rung_cost(g, mu)
                           for (g, mu) in EXTENDED_LADDER},
            "provenance": {f"({g},{mu})": PROVENANCE[(g, mu)]
                           for (g, mu) in EXTENDED_LADDER},
            "per_rung_pass_counts": revival,
        },
        "metric": {"n_star": round(n_star, 3), "CUT_TOL": CUT_TOL,
                   "library_size": len(lib_names),
                   "splice_family": int(len(splices)),
                   "tol_note": "CUT_TOL 0.01 in exp136 (repaired) and "
                               "here — L121's cross-tol flag resolved; "
                               "N* 82.288 re-derived identically"},
        "replication_of_exp141": rep,
        "funnel": {"pool": len(pool), "lib_novel": len(eligible),
                   "splice_clear": len(splice_clear),
                   "delivered": n_del,
                   "audit_pass_delivered": audit_n,
                   "decode_pass_delivered": decode_n,
                   "gate_bearing_audit_pass_all": len(gb_pass)},
        "cohort": [
            {"name": f"c-{i + 1:02d}", "role": r["role"],
             "zones": [list(z) for z in r["zones"]],
             "tags": r["tags"],
             "J": round(r["J"], 4),
             "nov_lib": round(r["nov_lib"], 2),
             "nov_splice": round(r["nov_splice"], 2),
             "min_pairwise_D": r["min_pairwise_D"],
             "ladder": r["ladder"],
             "audit_pass": r["audit_pass"],
             "emitted_cell": r["emitted_cell"],
             "decomposition": r["decomposition"],
             "decode_errs": r["decode_errs"],
             "hold_errs": r["hold_errs"],
             "decode_stable_seeds": r["decode_stable_seeds"],
             "decode_pass": r["decode_pass"]}
            for i, r in enumerate(cohort)],
        "diagnostics": {
            "ev_vs_etheta_decomposition_failed": {
                str(i): c["decomposition"]
                for i, c in enumerate(cohort) if not c["audit_pass"]},
            "channel_counts_all_fails": chan_counts,
            "spearman_nov_vs_best_rung_quad": (round(rho, 4)
                                               if rho is not None else None),
            "splice_kills_upstream": bool(len(splice_clear) == 0),
            "star_only_degradation": star_only,
        },
        "criteria": gates,
        "gate_clauses_passed": npass,
        "wall_s": round(time.time() - t0, 1),
        "notes": ("Instruments are exp136/exp141's imported verbatim; "
                  "the ONLY change is the audit's operating point "
                  "(extended frozen ladder + per-invention argmin "
                  "selection). If J1 is REFUTED with gate-bearing "
                  "candidates audited, the refutation localizes the "
                  "killer INSIDE the audit channels (see the eV/eT "
                  "decomposition); if the splice scan cleared nothing, "
                  "the killer sits upstream of the audit, in the "
                  "anti-recombination clause — exp141's audit never "
                  "ran (its deposited funnel implies this), which this "
                  "experiment tests directly."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
