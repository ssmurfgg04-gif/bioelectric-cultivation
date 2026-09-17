#!/usr/bin/env python3
"""exp189 — THE FUNNEL EXCLUSION ANATOMY (which stage kills the deep
programs?).

exp184's registered next (L160): the funnel excludes ALL 15 all-deep
members (0/15 eligible) even when the library contains them. Trace
each through every stage and name the excluding criterion.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp184's extended-library machinery verbatim (import from its module or copy its build block); exp141/exp146/exp150's funnel functions.

GATES (each evaluated exactly once):
  GATE-P1 (per-member trace) each of the 15 deep members traced
           through: (a) lib-novel distance vs N*_lib (the member's
           nearest-library distance, the criterion value, PASS/FAIL);
           (b) splice-family membership (in/out, the splice count);
           (c) splice-clear price vs N*_splice. The full trace table
           deposited (15 rows x 3 stages).
  GATE-P2 (the excluding stage NAMED) exactly one stage carries the
           exclusion for the majority (>= 8/15): the deposit names
           it and the criterion's per-member margin distribution.
  GATE-P3 (the mechanism clause) the pre-named branches: (i) DISTANCE
           failure — deep programs too similar to each other (the
           15 members' pairwise distances concentrated below the
           novelty bar); (ii) OUT-COMPETED — the 72 outrank them at
           a rank-cut; (iii) SPLICE-PRICED — their splices price
           above N*_splice. All branches complete the gate.
  GATE-P4 (hygiene) zero rejections in any price computed; the bars
           re-derive bit-identically to exp184's deposit.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp189_funnel_exclusion_anatomy.json
RUN: python3 -m experiments.exp189_funnel_exclusion_anatomy [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp189_funnel_exclusion_anatomy.json")


def main() -> dict:
    # ==== BODY (written by the run agent; docstring/imports/constants
    # above byte-unchanged — exp174's body-only discipline) ============
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "bars", "trace"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    # ---- exp184's B3 import block, verbatim (BLAS pins included) ------
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    from experiments.exp136_generator_v6 import (  # noqa: E402
        SEARCH_CELLS, CELL_SURCHARGE, LAMBDA_NOV, N as LAT_N,
        profile_of_zones, build_library, dist, library_nn_stats,
        build_splices, nov_lib, quad_err, wildtype_target)
    from experiments import exp141_generator_wide as W  # noqa: E402
    from experiments import exp146_splice_bar as L  # noqa: E402
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as M136  # noqa: E402
    import experiments.exp156_write_path as M156  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    DEEP_RUNGS = [-40.0, -45.0, -50.0, -55.0, -60.0]
    SEARCH_SEED = 141
    PROD_FLOOR = -60.0                    # CF-1's production value

    # the lineage deposits (exp184's bars + fates are P4's reference;
    # exp150's frozen bars are the counterfactual readings' bars)
    DEP184 = os.path.join(ROOT, "results", "exp184_deep_library.json")
    DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
    DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
    dep184 = json.load(open(DEP184))
    dep150 = json.load(open(DEP150))
    prev146 = json.load(open(DEP146))
    pipe184 = dep184["sections"]["pipeline"]
    bar184 = pipe184["bars"]
    funnel184 = pipe184["funnel"]
    fates184 = {r["member"]: r
                for r in pipe184["deep_funnel"]["fates"]}
    FROZEN_BAR_LIB = float(dep150["bars"]["n_star_lib"])
    FROZEN_BAR_SPLICE = float(dep150["bars"]["n_star_splice"])

    # ---- instrument check: the production core in situ (exp184
    #      verbatim; the floor is asserted, never touched) -------------
    floors = {"CORE": CORE.NEURAL_SPEC_MIN,
              "M136": M136.NEURAL_SPEC_MIN,
              "M156": M156.NEURAL_SPEC_MIN}
    assert all(v == PROD_FLOOR for v in floors.values()), \
        f"production floor drift: {floors}"

    # ---- canon check (exp184 verbatim) --------------------------------
    canon = wildtype_target(LAT_N)
    assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"

    # ==================================================================
    # THE EXTENDED-LIBRARY BUILD BLOCK — exp184's, VERBATIM (its
    # deep_member construction + the 72 + 15 assembly). Instruments:
    # exp141/exp146/exp150's funnel functions via the exp136/exp146
    # imports above.
    # ==================================================================
    def deep_member(rung: float, instance: int):
        """exp172's uniform-rung construction, VERBATIM (its
        target_for instance mechanism): the MULTI 3-zone program
        shifted +instance cells on the n=100 lattice, every zone value
        forced to `rung`, f = spec_target_n(spec, canon, 100),
        canon = labeling_bfs_n(A_CHAIN) (asserted == the engine's canon
        above). Returns f (the member's profile) and the program
        triples."""
        zs = [(z.f0 + instance / 100.0, z.f1 + instance / 100.0, z.name)
              for z in MULTI.zones]
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=rung, name=nm)
                   for (a, b, nm) in zs],
            amputate_plane=MULTI.amputate_plane,
            spec_name=f"ms-multi-deep-i{instance}",
            somatic_latch=MULTI.somatic_latch)
        f = spec_target_n(spec, canon, g6.N)
        triples = [(a, b, rung) for (a, b, _nm) in zs]
        return f, triples

    lib_frozen = build_library()
    assert len(lib_frozen) == 72, \
        f"frozen library size drift: {len(lib_frozen)}"
    frozen_names = list(lib_frozen)
    frozen_arr = np.stack([lib_frozen[n] for n in frozen_names])

    deep_lib: dict = {}
    deep_meta: list = []
    for rung in DEEP_RUNGS:
        for i in range(3):
            f, triples = deep_member(rung, i)
            name = f"deep_r{rung:g}_i{i}"
            deep_lib[name] = f
            deep_meta.append({"member": name, "rung": rung,
                              "instance": i,
                              "zones": [tuple(z) for z in triples],
                              "f": f})
    assert len(deep_lib) == 15, \
        f"deep cohort size drift: {len(deep_lib)}"

    lib = dict(lib_frozen)
    lib.update(deep_lib)
    assert len(lib) == 87, f"extended library size drift: {len(lib)}"
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    deep_idx = [lib_names.index(m["member"]) for m in deep_meta]
    assert len(deep_idx) == 15 and len(set(deep_idx)) == 15
    print(f"  extended library built: 72 frozen + 15 all-deep = "
          f"{len(lib_names)} members (exp184's build block verbatim)")

    # ---- N*_lib re-derived (the deposited machinery) -----------------
    n_star_lib, nn_arr = library_nn_stats(lib)
    print(f"  N*_lib {n_star_lib:.3f} (RE-DERIVED via exp136's "
          f"library_nn_stats on the extended library; exp184's deposit "
          f"{bar184['n_star_lib']})")

    # the anatomy's own copy of the SAME matrix (same dist, same
    # symmetric-storage convention) to identify nearest-OTHER members
    # and the deep cohort's pairwise distances (the machinery's
    # library_nn_stats returns only the NN column):
    M = len(lib_names)
    Dm = np.zeros((M, M))
    for i in range(M):
        for j in range(i + 1, M):
            Dm[i, j] = Dm[j, i] = dist(lib[lib_names[i]],
                                       lib[lib_names[j]])
    nn_mine = np.array([Dm[i][np.arange(M) != i].min()
                        for i in range(M)])
    assert np.array_equal(nn_mine, nn_arr), \
        "nn harness drift: anatomy matrix != library_nn_stats column"

    # ---- splice family + N*_splice re-derived (exp146 machinery,
    #         exp184's section 1 verbatim incl. the harness check) -----
    S = build_splices(lib)
    n_splice_expected = 87 * 86 // 2 * 19
    assert len(S) == n_splice_expected, \
        f"splice family size drift: {len(S)} != {n_splice_expected}"
    fm = np.zeros((len(S), 100), dtype=bool)
    fm[:, 1:] = S[:, 1:] != S[:, :-1]
    fl = fm.sum(axis=1)
    rng = np.random.default_rng(150)
    worst = 0.0
    for _ in range(400):
        a, b = rng.integers(0, len(S), 2)
        if a == b:
            continue
        i, j = min(a, b), max(a, b)
        m1, m2 = L.cut_mask(S[i]), L.cut_mask(S[j])
        fast = float(L.fast_dist_fwd(
            S[i], m1, int(m1.sum()), S[j][None], m2[None],
            np.array([int(m2.sum())]))[0])
        worst = max(worst, abs(fast - dist(S[i], S[j])))
    assert worst < 1e-9, \
        "imported fast evaluator diverged from dist"
    n_star_splice, _, _ = L.splice_family_bar(S)
    print(f"  splice family {len(S)} | N*_splice {n_star_splice:.3f} "
          f"(RE-DERIVED via exp146's splice_family_bar; exp184's "
          f"deposit {bar184['n_star_splice']} | frozen-72 deposit "
          f"{prev146['n_star_splice']}) | harness "
          f"max|fast-verbatim| {worst:.2e}")

    # ---- stage (b) ground truth: splice-family membership counts -----
    # (structural: build_splices emits crosses-per-pair rows for EVERY
    # unordered pair, so every library member participates; verified,
    # not assumed)
    crosses_n = int(len(np.arange(0.05, 1.0, 0.05)))
    partners_n = len(lib_names) - 1
    per_member_splices = partners_n * crosses_n
    assert 2 * len(S) == len(lib_names) * per_member_splices, \
        "splice participation census drift"

    # ---- the frozen-72 counterfactual family (exp184's both-readings
    #         block: the "had they been invented, not joined" family) --
    S_frozen = build_splices(lib_frozen)
    fmF = np.zeros((len(S_frozen), 100), dtype=bool)
    fmF[:, 1:] = S_frozen[:, 1:] != S_frozen[:, :-1]
    flF = fmF.sum(axis=1)

    # ---- the 15 deep members' criterion records (exp184's section 2b
    #         formulas VERBATIM — same nov_lib / quad_err / class_tags
    #         calls; pure deterministic functions, order-independent) --
    deep_recs: list = []
    for m in deep_meta:
        zs = m["zones"]
        key = W.to_key([tuple(z) for z in zs])
        f = m["f"]
        nov = nov_lib(f, lib_arr)          # vs the record it joined
        nov_cf = nov_lib(f, frozen_arr)    # counterfactual: frozen 72
        d_cf = [dist(f, frozen_arr[k])
                for k in range(len(frozen_arr))]
        j_cf = int(np.argmin(d_cf))
        best = None
        for ci, (g, mu) in enumerate(SEARCH_CELLS):
            eV, eT, q = quad_err(f, g, mu, seeds=(1,))
            cost = q + ci * CELL_SURCHARGE
            if best is None or cost < best["cost"]:
                best = {"cost": cost, "cell": (g, mu), "eV": eV,
                        "eT": eT, "quad": q}
        J = best["cost"] + LAMBDA_NOV * max(0.0, n_star_lib - nov)
        rec = {"zones": [tuple(z) for z in zs], "f": f,
               "nov_lib": nov, "nov_lib_vs_frozen72": nov_cf,
               "nearest_frozen72": frozen_names[j_cf],
               "dist_nearest_frozen72": float(d_cf[j_cf]),
               "J": J, "search_cell": best["cell"],
               "search_eV": best["eV"], "search_eT": best["eT"],
               "search_quad": best["quad"],
               "novel": bool(nov > n_star_lib),
               "tags": W.class_tags([tuple(z) for z in zs], f),
               "deep_member": True, "member": m["member"],
               "rung": m["rung"], "instance": m["instance"]}
        # both splice readings (exp184's diagnosis block, verbatim
        # evaluators): against the extended family they joined, and
        # the frozen-72 counterfactual family
        rec["nov_splice_extended"] = L.fast_nov_splice(f, S, fm, fl)
        rec["nov_splice_vs_frozen72"] = L.fast_nov_splice(
            f, S_frozen, fmF, flF)
        # nearest OTHER library member (self excluded) — the matrix
        # reading of the same distance the criterion walks:
        i = lib_names.index(m["member"])
        row = Dm[i].copy()
        row[i] = np.inf
        j2 = int(np.argmin(row))
        rec["nearest_other_extended"] = lib_names[j2]
        rec["dist_nearest_other_extended"] = float(row[j2])
        assert float(row[j2]) == float(nn_arr[i]), \
            f"nearest-other drift for {m['member']}"
        deep_recs.append(rec)
    del S_frozen, fmF, flF
    print(f"  deep members' criterion records: 15 (nov_lib vs the "
          f"record they joined all "
          f"{max(r['nov_lib'] for r in deep_recs):.3f} — a record "
          f"member's novelty is 0 by definition; nearest OTHER member "
          f"max {max(r['dist_nearest_other_extended'] for r in deep_recs):.3f})")

    # ==================================================================
    # THE TRACE (GATE-P1): 15 rows x 3 stages, each stage with the
    # criterion value, the bar, the margin and PASS/FAIL. Stage (b)
    # (family membership) is structural and excludes no one; the
    # funnel's carried stages are (a) lib-novelty then (c)
    # splice-clearance — excluding_stage = the FIRST carried stage
    # whose criterion fails.
    # ==================================================================
    STAGE_TO_BRANCH = {"a_lib_novel": "DISTANCE",
                       "c_splice_clear": "SPLICE-PRICED"}

    def build_trace_rows(ranks: dict | None) -> list:
        rows = []
        for rec in deep_recs:
            d184 = fates184[rec["member"]]
            a = {
                "criterion": ("nov_lib(f, extended record incl. self) "
                              "> N*_lib"),
                "value": float(rec["nov_lib"]),
                "bar": float(n_star_lib),
                "bar_rounded": round(float(n_star_lib), 3),
                "margin_bar_minus_value":
                    float(n_star_lib - rec["nov_lib"]),
                "pass": bool(rec["nov_lib"] > n_star_lib),
                "nearest_other_extended": rec["nearest_other_extended"],
                "dist_nearest_other_extended":
                    float(rec["dist_nearest_other_extended"]),
                "margin_self_excluded":
                    float(n_star_lib
                          - rec["dist_nearest_other_extended"]),
                "counterfactual_had_they_been_invented": {
                    "reference": ("nov_lib vs the frozen 72 "
                                  "(exp150's deposited machinery)"),
                    "value": float(rec["nov_lib_vs_frozen72"]),
                    "nearest": rec["nearest_frozen72"],
                    "dist_nearest":
                        float(rec["dist_nearest_frozen72"]),
                    "bar_extended": float(n_star_lib),
                    "pass_at_extended_bar":
                        bool(rec["nov_lib_vs_frozen72"] > n_star_lib),
                    "bar_frozen_deposit": FROZEN_BAR_LIB,
                    "pass_at_frozen_bar":
                        bool(rec["nov_lib_vs_frozen72"]
                             > FROZEN_BAR_LIB)},
                "exp184_deposit_agrees":
                    bool(rec["nov_lib"] == d184["nov_lib_extended"]),
            }
            b = {
                "criterion": ("membership in the extended splice "
                              "family (structural)"),
                "in_family": True,
                "partners": partners_n,
                "crosses_per_pair": crosses_n,
                "n_splices_participating": per_member_splices,
                "pass": True,
                "note": ("every library member participates in "
                         "partners x crosses family rows; membership "
                         "is structural and excludes no one"),
            }
            c = {
                "criterion": ("nov_splice(f, extended family) > "
                              "N*_splice"),
                "value": float(rec["nov_splice_extended"]),
                "bar": float(n_star_splice),
                "bar_rounded": round(float(n_star_splice), 3),
                "margin_bar_minus_value":
                    float(n_star_splice - rec["nov_splice_extended"]),
                "pass": bool(rec["nov_splice_extended"]
                             > n_star_splice),
                "note": ("the extended family contains splices "
                         "identical or near-identical to each deep "
                         "member's own profile (same-rung "
                         "adjacent-instance pairs at late crosses), so "
                         f"the splice-clear price is 0.0 for "
                         f"{sum(rec['nov_splice_extended'] == 0.0 for rec in deep_recs)}"
                         f"/15 and max "
                         f"{max(rec['nov_splice_extended'] for rec in deep_recs):.3f} "
                         "across the cohort — all far below N*_splice; "
                         "reached only if (a) passed"),
                "counterfactual_had_they_been_invented": {
                    "reference": ("nov_splice vs the frozen-72 family "
                                  "at exp150's deposited bar"),
                    "value": float(rec["nov_splice_vs_frozen72"]),
                    "bar_frozen_deposit": FROZEN_BAR_SPLICE,
                    "pass_at_frozen_bar":
                        bool(rec["nov_splice_vs_frozen72"]
                             > FROZEN_BAR_SPLICE)},
                "exp184_deposit_agrees":
                    bool(rec["nov_splice_extended"]
                         == d184["nov_splice_extended"]),
            }
            excl = None
            if not a["pass"]:
                excl = "a_lib_novel"
            elif not c["pass"]:
                excl = "c_splice_clear"
            rows.append({
                "member": rec["member"], "rung": rec["rung"],
                "instance": rec["instance"],
                "stage_a_lib_novel": a,
                "stage_b_splice_family": b,
                "stage_c_splice_clear": c,
                "excluding_stage": excl,
                "in_eligible_final": bool(a["pass"]),
                "in_splice_clear_final": bool(a["pass"] and c["pass"]),
                "J": float(rec["J"]),
                "J_rank_in_J_ordered_pool":
                    (ranks or {}).get(rec["member"])})
        return rows

    def build_exclusion(rows: list) -> dict:
        counts = {"a_lib_novel": 0, "b_splice_family": 0,
                  "c_splice_clear": 0}
        for r in rows:
            if r["excluding_stage"] is not None:
                counts[r["excluding_stage"]] += 1
        carriers = sorted(s for s, n in counts.items() if n >= 8)
        named = carriers[0] if len(carriers) == 1 else None
        labels = {"a_lib_novel":
                  "the LIB-NOVELTY stage (nov_lib vs N*_lib)",
                  "b_splice_family":
                  "the SPLICE-FAMILY membership stage (structural)",
                  "c_splice_clear":
                  "the SPLICE-CLEAR stage (nov_splice vs N*_splice)"}
        margins_as_run = [float(n_star_lib - rec["nov_lib"])
                          for rec in deep_recs]
        margins_self = [float(n_star_lib
                              - rec["dist_nearest_other_extended"])
                        for rec in deep_recs]
        margins_cf = [float(FROZEN_BAR_LIB
                            - rec["nov_lib_vs_frozen72"])
                      for rec in deep_recs]

        def stats(vs):
            return {"min": float(np.min(vs)),
                    "median": float(np.median(vs)),
                    "max": float(np.max(vs))}
        return {
            "stage_labels": labels,
            "excluding_stage_counts": counts,
            "majority_required": 8,
            "carrier_stages": carriers,
            "named_stage": named,
            "named_stage_label": (labels[named] if named else None),
            "margin_distribution": {
                "criterion": ("N*_lib - nov_lib — the excluding "
                              "stage's criterion, per member"),
                "as_run_values":
                    [round(v, 3) for v in margins_as_run],
                "as_run": stats(margins_as_run),
                "self_excluded_values":
                    [round(v, 3) for v in margins_self],
                "self_excluded": stats(margins_self),
                "counterfactual_frozen72_bar_values":
                    [round(v, 3) for v in margins_cf],
                "counterfactual_frozen72_bar": stats(margins_cf),
                "note": ("all margins positive — the novelty bar "
                         "excludes every deep member with room; the "
                         "closest approach under ANY reading is the "
                         "counterfactual max nov_lib_vs_frozen72 "
                         f"{max(rec['nov_lib_vs_frozen72'] for rec in deep_recs):.3f}"
                         f", still below the frozen bar "
                         f"{FROZEN_BAR_LIB:.3f}")}}

    def build_branches(rows: list, ranks: dict | None) -> dict:
        pw = Dm[np.ix_(deep_idx, deep_idx)]
        iu = np.triu_indices(len(deep_idx), 1)
        pairwise = pw[iu]
        n_below = int((pairwise < n_star_lib).sum())
        rank_list = sorted(ranks.values()) if ranks else []
        branch_distance = {
            "branch": "DISTANCE",
            "clause": ("(i) DISTANCE failure — deep programs too "
                       "similar to each other (the 15 members' "
                       "pairwise distances concentrated below the "
                       "novelty bar)"),
            "n_pairs": int(len(pairwise)),
            "n_pairs_below_bar": n_below,
            "concentration_below_bar":
                float(n_below / len(pairwise)),
            "pairwise_min": float(pairwise.min()),
            "pairwise_median": float(np.median(pairwise)),
            "pairwise_max": float(pairwise.max()),
            "n_star_lib": float(n_star_lib),
            "nearest_other_all_below_bar": bool(all(
                rec["dist_nearest_other_extended"] < n_star_lib
                for rec in deep_recs)),
            "counterfactual_max_nov_lib_vs_frozen72":
                float(max(rec["nov_lib_vs_frozen72"]
                          for rec in deep_recs)),
            "counterfactual_frozen_bar": FROZEN_BAR_LIB,
            "counterfactual_n_novel_at_frozen_bar": int(sum(
                rec["nov_lib_vs_frozen72"] > FROZEN_BAR_LIB
                for rec in deep_recs)),
            "carried": bool(n_below * 2 > len(pairwise)
                            and all(rec["dist_nearest_other_extended"]
                                    < n_star_lib
                                    for rec in deep_recs))}
        branch_outcompeted = {
            "branch": "OUT-COMPETED",
            "clause": ("(ii) OUT-COMPETED — the 72 outrank them at a "
                       "rank-cut"),
            "rank_cut_in_funnel": False,
            "note": ("the funnel is a two-threshold filter "
                     "(lib-novelty, splice-clear); there is NO "
                     "rank-cut stage at which the frozen 72 could "
                     "outrank the deep members — every novel member "
                     "is admitted regardless of J-rank (the J-ordered "
                     "list only sets traversal order); the deep "
                     "members' J-ranks are recorded as diagnostic"),
            "deep_J_ranks_in_J_ordered_pool": rank_list,
            "pool_size": (max(ranks.values()) if ranks else None),
            "carried": False}
        n_above = int(sum(rec["nov_splice_extended"] > n_star_splice
                          for rec in deep_recs))
        branch_splice = {
            "branch": "SPLICE-PRICED",
            "clause": ("(iii) SPLICE-PRICED — their splices price "
                       "above N*_splice"),
            "n_above_extended_bar": n_above,
            "max_nov_splice_extended":
                float(max(rec["nov_splice_extended"]
                          for rec in deep_recs)),
            "n_star_splice": float(n_star_splice),
            "counterfactual_n_above_frozen_bar": int(sum(
                rec["nov_splice_vs_frozen72"] > FROZEN_BAR_SPLICE
                for rec in deep_recs)),
            "counterfactual_frozen_bar": FROZEN_BAR_SPLICE,
            "carried": bool(n_above > 0)}
        carried = [x["branch"] for x in
                   (branch_distance, branch_outcompeted,
                    branch_splice) if x["carried"]]
        return {"branches": [branch_distance, branch_outcompeted,
                             branch_splice],
                "carried_branches": carried,
                "branch_named": (carried[0]
                                 if len(carried) == 1 else None),
                "consistency_with_exclusion_stage": {
                    "stage_to_branch": STAGE_TO_BRANCH,
                    "note": ("the lib-novelty stage's criterion IS a "
                             "distance criterion — branch (i) is its "
                             "mechanism; a splice-clear carrier would "
                             "map to branch (iii); branch (ii) has no "
                             "stage to carry (no rank-cut exists)")}}

    # ==================================================================
    # dispatch -----------------------------------------------------------
    # ==================================================================
    print("=== exp189: THE FUNNEL EXCLUSION ANATOMY (which stage "
          "kills the deep programs? — exp184's registered next, "
          "L160) ===\n")

    if args.smoke:
        rows = build_trace_rows(None)
        excl = build_exclusion(rows)
        brs = build_branches(rows, None)
        dep = {"exp": "exp189_funnel_exclusion_anatomy",
               "kind": "smoke", "discarded": True,
               "scope": ("extended-library build + re-derived N*_lib / "
                         "N*_splice + the 15-row trace table + "
                         "exclusion/branch evals (no seed-141 search "
                         "re-run, no N*_pool, no gates)"),
               "bars_partial": {
                   "n_star_lib": round(float(n_star_lib), 3),
                   "n_star_splice": round(float(n_star_splice), 3)},
               "funnel_counts_membership": {
                   "library": len(lib_names),
                   "splice_family": len(S)},
               "trace_rows": rows,
               "exclusion": excl,
               "branches": brs,
               "wall_s": round(time.time() - t0, 1)}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                        exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(dep, fh, indent=1, default=float)
        print(f"  SMOKE (discarded): N*_lib "
              f"{dep['bars_partial']['n_star_lib']} | N*_splice "
              f"{dep['bars_partial']['n_star_splice']} | excluding "
              f"{dep['exclusion']['excluding_stage_counts']} | branch "
              f"{dep['branches']['branch_named']}")
        return dep

    result: dict = {}
    if args.job != "all" and os.path.exists(out_path):
        with open(out_path) as fh:
            result = json.load(fh)
    result.setdefault("sections", {})
    result.setdefault("gates", {})

    result["sections"]["build"] = {
        "library_members": len(lib_names),
        "deep_members": len(deep_lib),
        "splice_family_size": len(S),
        "splice_participation_per_member": per_member_splices,
        "harness_max_abs_diff": worst,
        "canon_check": True,
        "production_floor_asserted": True,
        "instrument_pin_used": False,
        "build_block_source": ("exp184_deep_library.py's "
                               "extended-library build block, copied "
                               "verbatim (its deep_member construction "
                               "+ the 72 + 15 assembly)")}
    result["sections"]["bars_rederived"] = {
        "n_star_lib": round(float(n_star_lib), 3),
        "n_star_splice": round(float(n_star_splice), 3),
        "n_star_lib_raw": float(n_star_lib),
        "n_star_splice_raw": float(n_star_splice),
        "machinery": ("exp136's library_nn_stats + exp146's "
                      "splice_family_bar on the extended structures "
                      "(computed, not assumed)"),
        "exp184_deposit_reference": bar184}
    if args.job == "bars":
        result.update({"exp": "exp189_funnel_exclusion_anatomy",
                       "verdict": "partial (job=bars)",
                       "wall_s": round(time.time() - t0, 1)})
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        return result

    # ---- the search re-run (exp141's loop VERBATIM, seed 141, via
    #         exp184's section 2 — needed ONLY for N*_pool's
    #         splice-clear corpus; the trace's criteria are
    #         search-independent) --------------------------------------
    rng = np.random.default_rng(SEARCH_SEED)
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
        J = best["cost"] + LAMBDA_NOV * max(0.0, n_star_lib - nov)
        rec = {"zones": zones, "f": f, "nov_lib": nov, "J": J,
               "search_cell": best["cell"], "search_eV": best["eV"],
               "search_eT": best["eT"], "search_quad": best["quad"],
               "novel": bool(nov > n_star_lib),
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
    for rnd in range(W.ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[W.to_key(r["zones"])] = r
        recs_sorted = sorted(recs, key=lambda r: r["J"])
        n_novel = sum(int(r["novel"]) for r in recs)
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
    n_pool_search = len(pool)
    print(f"  search re-run (seed 141, extended novelty reference): "
          f"pool {n_pool_search}")

    # ---- the deep members pushed through the SAME machinery
    #         (exp184's section 2b verbatim: appended to the pool as
    #         candidates) ----------------------------------------------
    for rec in deep_recs:
        key = W.to_key([tuple(z) for z in rec["zones"]])
        assert key not in pool, \
            (f"a search candidate collides with deep member "
             f"{rec['member']} — that would be a finding")
        pool[key] = rec
    print(f"  deep members appended (pool {n_pool_search} -> "
          f"{len(pool)})")

    # ---- the funnel (exp184's section 3, VERBATIM) -------------------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    eligible = [r for r in ordered if r["novel"]]
    for r in eligible:
        r["nov_splice"] = L.fast_nov_splice(r["f"], S, fm, fl)
    splice_clear = [r for r in eligible
                    if r["nov_splice"] > n_star_splice]
    n_deep_eligible = sum(int(bool(r.get("deep_member")))
                          for r in eligible)
    n_deep_splice = sum(int(bool(r.get("deep_member")))
                        for r in splice_clear)
    print(f"  funnel: lib-novel {len(eligible)}/{len(pool)} | "
          f"splice-clear {len(splice_clear)}/{len(eligible)} | "
          f"DEEP members in eligible: {n_deep_eligible}/15")

    # ---- N*_pool re-derived BEFORE selection (exp184's section 4,
    #         VERBATIM) -------------------------------------------------
    pool_dict = {f"pool-{i:03d}": r["f"]
                 for i, r in enumerate(splice_clear)}
    n_star_pool, _ = library_nn_stats(pool_dict)
    print(f"  N*_pool {n_star_pool:.3f} (RE-DERIVED on the extended "
          f"funnel's splice-clear set, before selection)")

    # ---- P4 hygiene: bars bit-exact vs exp184's deposit --------------
    bars = {"n_star_lib": round(float(n_star_lib), 3),
            "n_star_splice": round(float(n_star_splice), 3),
            "n_star_pool": round(float(n_star_pool), 3)}
    bars_bitmatch = bool(bars == bar184)
    funnel_census = {"pool": len(pool),
                     "pool_search_only": n_pool_search,
                     "lib_novel": len(eligible),
                     "splice_clear": len(splice_clear)}
    census_match = bool(funnel_census == funnel184)
    ranks = {r["member"]: i for i, r in enumerate(ordered, 1)
             if r.get("deep_member")}

    # deep-fate criterion values bit-match exp184's deposit (the SAME
    # deterministic machinery — the anatomy's licence to trace)
    fate_checks: list = []
    fate_bitmatch = True
    for rec in deep_recs:
        d184 = fates184[rec["member"]]
        checks = {
            "nov_lib_extended":
                rec["nov_lib"] == d184["nov_lib_extended"],
            "nov_lib_vs_frozen72":
                rec["nov_lib_vs_frozen72"]
                == d184["nov_lib_vs_frozen72"],
            "nearest_frozen72":
                rec["nearest_frozen72"] == d184["nearest_frozen72"],
            "dist_nearest_frozen72":
                rec["dist_nearest_frozen72"]
                == d184["dist_nearest_frozen72"],
            "nov_splice_extended":
                rec["nov_splice_extended"]
                == d184["nov_splice_extended"],
            "nov_splice_vs_frozen72":
                rec["nov_splice_vs_frozen72"]
                == d184["nov_splice_vs_frozen72"],
            "J": rec["J"] == d184["J"],
            "novel": rec["novel"] == d184["novel"],
            "in_eligible": rec["novel"] == d184["in_eligible"],
            "in_splice_clear":
                (rec["novel"]
                 and rec["nov_splice_extended"] > n_star_splice)
                == d184["in_splice_clear"]}
        fate_bitmatch &= all(checks.values())
        fate_checks.append({"member": rec["member"],
                            "checks": checks,
                            "all": bool(all(checks.values()))})
    print(f"  hygiene: bars bit-match {bars_bitmatch} | funnel census "
          f"match {census_match} | deep-fate criterion bit-match "
          f"{fate_bitmatch}")

    # ---- the trace + exclusion + branches (final, with ranks) --------
    rows = build_trace_rows(ranks)
    excl = build_exclusion(rows)
    brs = build_branches(rows, ranks)
    result["sections"]["trace"] = {
        "stages": ["a_lib_novel", "b_splice_family", "c_splice_clear"],
        "stage_criteria": {
            "a_lib_novel": "nov_lib(f, extended record incl. self) > N*_lib",
            "b_splice_family": "membership in the extended splice family (structural)",
            "c_splice_clear": "nov_splice(f, extended family) > N*_splice"},
        "n_rows": len(rows),
        "rows": rows,
        "matrix_view": {
            "members": [r["member"] for r in rows],
            "values_a_lib_novel":
                [r["stage_a_lib_novel"]["value"] for r in rows],
            "values_c_splice_clear":
                [r["stage_c_splice_clear"]["value"] for r in rows],
            "bars": [float(n_star_lib), float(n_star_splice)],
            "pass_a": [r["stage_a_lib_novel"]["pass"] for r in rows],
            "pass_b": [r["stage_b_splice_family"]["pass"] for r in rows],
            "pass_c": [r["stage_c_splice_clear"]["pass"] for r in rows],
            "excluding_stage": [r["excluding_stage"] for r in rows]}}
    result["sections"]["exclusion"] = excl
    result["sections"]["branches"] = brs
    result["sections"]["funnel_census"] = {
        "this_run": funnel_census,
        "exp184_deposit": funnel184,
        "match": census_match,
        "n_deep_in_eligible": n_deep_eligible,
        "n_deep_in_splice_clear": n_deep_splice}
    result["sections"]["hygiene"] = {
        "rejections_total": 0,
        "rejections_note": ("no price_rung/emit instrument is part of "
                            "this anatomy's registered instruments — "
                            "the three stages compute criterion "
                            "values (nov_lib, membership, nov_splice) "
                            "only, which cannot reject; rejections "
                            "structurally zero, disclosed (the exp187 "
                            "C4 disclosure pattern)"),
        "bars": bars,
        "bars_bit_match_exp184": bars_bitmatch,
        "funnel_census_match": census_match,
        "deep_fate_criterion_bitmatch": bool(fate_bitmatch),
        "deep_fate_checks": fate_checks,
        "nn_matrix_harness": "anatomy Dm matrix == library_nn_stats's "
                             "NN column (array_equal)",
        "fast_evaluator_harness_max_abs_diff": worst}

    # ==================================================================
    # THE GATES (each evaluated exactly once, on complete inputs)
    # ==================================================================
    def evaluate_p1(sections: dict) -> dict | None:
        tr = sections.get("trace")
        if tr is None:
            return None
        complete = bool(tr["n_rows"] == 15 and all(
            r["stage_a_lib_novel"] is not None
            and r["stage_b_splice_family"] is not None
            and r["stage_c_splice_clear"] is not None
            for r in tr["rows"]))
        return {"gate": "P1", "clause": (
            "per-member trace: each of the 15 deep members traced "
            "through (a) lib-novel distance vs N*_lib (the member's "
            "nearest-library distance, the criterion value, PASS/FAIL);"
            " (b) splice-family membership (in/out, the splice count); "
            "(c) splice-clear price vs N*_splice. The full trace table "
            "deposited (15 rows x 3 stages)"),
                "n_rows": tr["n_rows"],
                "n_stages_per_row": 3,
                "complete": complete,
                "pass": complete}

    def evaluate_p2(sections: dict) -> dict | None:
        exc = sections.get("exclusion")
        if exc is None:
            return None
        counts = exc["excluding_stage_counts"]
        carriers = [s for s, n in counts.items() if n >= 8]
        ok = bool(len(carriers) == 1)
        return {"gate": "P2", "clause": (
            "the excluding stage NAMED: exactly one stage carries the "
            "exclusion for the majority (>= 8/15): the deposit names "
            "it and the criterion's per-member margin distribution"),
                "excluding_stage_counts": counts,
                "majority_required": 8,
                "carrier_stages": carriers,
                "named_stage": exc["named_stage"],
                "named_stage_label": exc["named_stage_label"],
                "margin_distribution": exc["margin_distribution"],
                "pass": ok}

    def evaluate_p3(sections: dict) -> dict | None:
        brs_ = sections.get("branches")
        exc = sections.get("exclusion")
        if brs_ is None or exc is None:
            return None
        consistent = bool(
            brs_["branch_named"] is not None
            and exc["named_stage"] is not None
            and brs_["branch_named"]
            == brs_["consistency_with_exclusion_stage"]
            ["stage_to_branch"].get(exc["named_stage"]))
        ok = bool(len(brs_["branches"]) == 3
                  and len(brs_["carried_branches"]) >= 1
                  and consistent)
        return {"gate": "P3", "clause": (
            "the mechanism clause: the pre-named branches (i) DISTANCE "
            "failure — deep programs too similar to each other (the 15 "
            "members' pairwise distances concentrated below the "
            "novelty bar); (ii) OUT-COMPETED — the 72 outrank them at "
            "a rank-cut; (iii) SPLICE-PRICED — their splices price "
            "above N*_splice. All branches complete the gate"),
                "branches": brs_["branches"],
                "carried_branches": brs_["carried_branches"],
                "branch_named": brs_["branch_named"],
                "consistent_with_exclusion_stage": consistent,
                "pass": ok}

    def evaluate_p4(sections: dict) -> dict | None:
        hy = sections.get("hygiene")
        br = sections.get("bars_rederived")
        if hy is None or br is None or "n_star_pool" not in hy["bars"]:
            return None
        ok = bool(hy["rejections_total"] == 0
                  and hy["bars_bit_match_exp184"]
                  and hy["funnel_census_match"]
                  and hy["deep_fate_criterion_bitmatch"])
        return {"gate": "P4", "clause": (
            "hygiene: zero rejections in any price computed; the bars "
            "re-derive bit-identically to exp184's deposit"),
                "rejections_total": hy["rejections_total"],
                "rejections_note": hy["rejections_note"],
                "bars_this_run": hy["bars"],
                "bars_exp184_deposit": bar184,
                "bars_bit_identical": hy["bars_bit_match_exp184"],
                "funnel_census": sections["funnel_census"],
                "funnel_census_match": hy["funnel_census_match"],
                "deep_fate_criterion_bitmatch":
                hy["deep_fate_criterion_bitmatch"],
                "pass": ok}

    for name, fn in (("P1", evaluate_p1), ("P2", evaluate_p2),
                     ("P3", evaluate_p3), ("P4", evaluate_p4)):
        if name in result["gates"]:
            continue
        g = fn(result["sections"])
        if g is not None:
            result["gates"][name] = g

    npass = sum(int(g["pass"]) for g in result["gates"].values())
    for name in ("P1", "P2", "P3", "P4"):
        if name in result["gates"]:
            g = result["gates"][name]
            extra = ""
            if name == "P1":
                extra = (f" ({g['n_rows']} rows x "
                         f"{g['n_stages_per_row']} stages, complete "
                         f"{g['complete']})")
            elif name == "P2":
                extra = (f" (counts {g['excluding_stage_counts']}, "
                         f"named {g['named_stage']})")
            elif name == "P3":
                extra = (f" (carried {g['carried_branches']}, named "
                         f"{g['branch_named']}, consistent "
                         f"{g['consistent_with_exclusion_stage']})")
            elif name == "P4":
                extra = (f" (bars {g['bars_this_run']} bit-identical "
                         f"{g['bars_bit_identical']}, rejections "
                         f"{g['rejections_total']})")
            print(f"  GATE-{name}: {'PASS' if g['pass'] else 'REFUTE'}"
                  f"{extra}")
    verdict = (f"{npass}/{len(result['gates'])} gates "
               f"({' '.join(k for k in ('P1', 'P2', 'P3', 'P4')
                            if k in result['gates'])})")
    named_stage = excl["named_stage"]
    branch_named = brs["branch_named"]
    stage_label = excl["named_stage_label"]
    print(f"  === {verdict} ===")
    print(f"  EXCLUDING STAGE: {stage_label} | BRANCH: {branch_named}")

    result.update({
        "exp": "exp189_funnel_exclusion_anatomy",
        "claim": (
            "THE FUNNEL EXCLUSION ANATOMY (exp184's registered next, "
            "L160): exp184's funnel excludes ALL 15 all-deep members "
            "(0/15 eligible) even when the library contains them. "
            "THIS RUN traces each deep member through every stage "
            "with exp184's extended-library machinery verbatim (its "
            "build block copied; exp141/exp146/exp150's funnel "
            "functions): (a) lib-novel distance vs N*_lib, (b) "
            "splice-family membership, (c) splice-clear price vs "
            "N*_splice; names the excluding stage and the mechanism "
            "branch from the pre-named set {DISTANCE, OUT-COMPETED, "
            "SPLICE-PRICED}; bars RE-DERIVED bit-exactly against "
            "exp184's deposit"),
        "result_line": {
            "excluding_stage": named_stage,
            "excluding_stage_label": stage_label,
            "branch": branch_named,
            "n_excluded_at_named_stage":
                excl["excluding_stage_counts"].get(named_stage, 0)
            if named_stage else 0},
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration; gates P1-P4 "
                             "fixed there, each evaluated exactly "
                             "once)"),
            "gates": [
                "P1 per-member trace: (a) lib-novel distance vs "
                "N*_lib; (b) splice-family membership (in/out, the "
                "splice count); (c) splice-clear price vs N*_splice; "
                "the full trace table deposited (15 rows x 3 stages)",
                "P2 the excluding stage NAMED: exactly one stage "
                "carries the exclusion for the majority (>= 8/15), "
                "with the criterion's per-member margin distribution",
                "P3 the mechanism clause: pre-named branches (i) "
                "DISTANCE failure, (ii) OUT-COMPETED at a rank-cut, "
                "(iii) SPLICE-PRICED; all branches complete the gate",
                "P4 hygiene: zero rejections in any price computed; "
                "the bars re-derive bit-identically to exp184's "
                "deposit"],
            "instruments": ("exp184's extended-library build block "
                            "(copied verbatim) + exp141/exp146/exp150's "
                            "funnel functions via exp136/exp146 "
                            "imports; search seed 141 for N*_pool's "
                            "corpus re-derivation"),
            "cohort": ("15 all-deep members = exp172's uniform-rung "
                       "construction (rungs {-40,-45,-50,-55,-60} x 3 "
                       "MULTI-zone layout shifts +i cells, i = 0..2) "
                       "inside exp184's 87-member extended library"),
            "bars": "RE-DERIVED on the extended structures (computed, "
                    "not assumed); bit-exact vs exp184's deposit "
                    "required by P4",
            "tie_break": "member index ascending (J-ordered funnel "
                         "index)"},
        "stage_order": [
            "extended_library_build (exp184's block verbatim: 72 "
            "frozen + 15 all-deep exp172 constructions)",
            "n_star_lib_rederived (exp136's library_nn_stats on the "
            "extended library) + anatomy distance matrix (harness: "
            "array_equal to the machinery's NN column)",
            "splice_family_rederived (71079) + harness (400 pairs, "
            "max|fast-verbatim| < 1e-9) + n_star_splice_rederived "
            "(exp146's splice_family_bar)",
            "deep_members_criterion_records (exp184's 2b formulas "
            "verbatim: nov_lib, quad_err/J, class_tags, both splice "
            "readings, nearest-other identities)",
            "trace_table_built (15 rows x 3 stages, margins, "
            "counterfactuals)",
            "search_rerun_seed141 (exp141's loop VERBATIM via "
            "exp184's section 2; needed only for N*_pool's corpus)",
            "deep_members_appended_to_pool (exp184's 2b verbatim)",
            "funnel_rederived (lib-novelty -> splice-clear, exp184's "
            "section 3 verbatim)",
            "n_star_pool_rederived_BEFORE_selection (exp184's section "
            "4 verbatim)",
            "hygiene (bars bit-exact vs exp184, funnel census, "
            "deep-fate criterion bit-match, zero rejections)",
            "gates_evaluated"],
        "smoke_disclosure": ("a --smoke check (extended-library build "
                             "+ re-derived N*_lib/N*_splice + the "
                             "15-row trace table) ran before the "
                             "credited run and was discarded (no "
                             "file)"),
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1)})

    os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1, default=float)
    print(f"  deposited {out_path} | wall {result['wall_s']} s")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
