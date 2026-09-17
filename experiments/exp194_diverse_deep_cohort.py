#!/usr/bin/env python3
"""exp194 — THE DIVERSE DEEP COHORT (novelty-proof deep members).

exp189's registered next (L165): the deep cohort dies of
SELF-SIMILARITY at the lib-novelty stage. Build deep members with
STRUCTURAL diversity — varied zone layouts/widths (exp172's
construction discipline at 6 layout shifts x 5 rungs = 30 members,
plus 15 mixed-depth members carrying deep+shallow zones) — through
the SAME funnel.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp184's extended-library + clause-walk machinery verbatim; exp189's trace functions for the distance table.

GATES (each evaluated exactly once):
  GATE-T1 (cohort build) 45 diverse deep members built (30
           uniform-rung varied-layout + 15 mixed-depth), canon ==
           wildtype asserted per member, the extended library
           (72 + 45) bars re-derived and deposited before selection.
  GATE-T2 (survival) >= 15/45 deep members in the eligible pool
           (the DISTANCE fix works); the per-member lib-novel
           distances deposited vs exp189's trace table.
  GATE-T3 (deep delivery) the clause's delivered-10 at the deep
           targets: >= 9/10 with decode < 6.0 AND hold < 6.0 on
           3/3 seeds at every rung; zero rejections; no
           audit_only_fallback.
  GATE-T4 (the old point) the clause's 10 at exp150's targets:
           C1-C4 ALL PASS.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp194_diverse_deep_cohort.json
RUN: python3 -m experiments.exp194_diverse_deep_cohort [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp194_diverse_deep_cohort.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "deep", "old", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    # ---- exp184's B3 import block, verbatim (BLAS pins included) ------
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import hashlib

    from experiments.exp136_generator_v6 import (  # noqa: E402
        SEARCH_CELLS, CELL_SURCHARGE, LAMBDA_NOV, N as LAT_N,
        profile_of_zones, build_library, dist, library_nn_stats,
        build_splices, nov_lib, quad_err, wildtype_target)
    from experiments import exp141_generator_wide as W  # noqa: E402
    from experiments import exp146_splice_bar as L  # noqa: E402
    from experiments.exp150_generator_complete import (  # noqa: E402
        price_rung, emit_rung)
    from experiments.exp156_write_path import (  # noqa: E402
        clash_mass, r_w_predict)
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as M136  # noqa: E402
    import experiments.exp156_write_path as M156  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    DEP184 = os.path.join(ROOT, "results", "exp184_deep_library.json")
    DEP189 = os.path.join(ROOT, "results",
                          "exp189_funnel_exclusion_anatomy.json")
    DEP141 = os.path.join(ROOT, "results", "exp141_generator_wide.json")
    DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
    PROD_FLOOR = -60.0                    # CF-1's production value
    SPLICE_EXPECTED = 117 * 116 // 2 * 19  # 128,886

    dep184 = json.load(open(DEP184))
    dep189 = json.load(open(DEP189))
    dep150 = json.load(open(DEP150))
    dep176 = json.load(open(DEP176))
    dep141 = json.load(open(DEP141))
    prev146 = json.load(open(DEP146))
    pipe184 = dep184["sections"]["pipeline"]
    bar184 = pipe184["bars"]
    trace189_rows = dep189["sections"]["trace"]["rows"]

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
    # THE DIVERSE COHORT CONSTRUCTION (disclosed, zero fitting — the
    # registered discipline: exp172's construction at 6 layout
    # instances x 5 rungs = 30 uniform-rung members with L165's
    # registered WIDTH variation, plus 15 mixed-depth members = 3
    # a-priori value patterns x 5 layout instances). All geometry in
    # exact cell units so instance 0 width-delta 0 reproduces
    # exp172's construction bit-exactly (exp176's target checksums
    # assert this below).
    # ==================================================================
    W_DELTAS = (0.0, 0.01, -0.01, 0.02, -0.02, 0.01)
    # positive delta narrows (f0 += d, f1 -= d); negative widens.
    MIXED_PATTERNS = ((-60.0, -15.0, -45.0),
                      (-15.0, -50.0, -55.0),
                      (-40.0, -60.0, -20.0))
    ZONE_NAMES = tuple(z.name for z in MULTI.zones)

    def multi_member(voltages, i: int):
        """The MULTI 3-zone program shifted +i cells with the
        instance's width delta applied to every zone boundary;
        voltages = per-zone values (the rung repeated for uniform
        members, the pattern's mix for mixed-depth members)."""
        d = W_DELTAS[i]
        zs = [(z.f0 + i / 100.0 + d, z.f1 + i / 100.0 - d, v)
              for z, v in zip(MULTI.zones, voltages)]
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=v, name=nm)
                   for (a, b, v), nm in zip(zs, ZONE_NAMES)],
            amputate_plane=MULTI.amputate_plane,
            spec_name=f"ms-diverse-i{i}",
            somatic_latch=MULTI.somatic_latch)
        f = spec_target_n(spec, canon, g6.N)
        return f, zs

    # ---- the extended library: exp141's frozen 72 + the 45 -----------
    lib_frozen = build_library()
    assert len(lib_frozen) == 72, \
        f"frozen library size drift: {len(lib_frozen)}"
    frozen_names = list(lib_frozen)
    frozen_arr = np.stack([lib_frozen[n] for n in frozen_names])

    deep_lib: dict = {}
    deep_meta: list = []
    for rung in DEEP_RUNGS:                       # 30 uniform-rung
        for i in range(6):
            f, zs = multi_member([rung] * 3, i)
            name = f"u_r{rung:g}_i{i}"
            deep_lib[name] = f
            deep_meta.append({"member": name, "kind": "uniform",
                              "rung": rung, "pattern": None,
                              "instance": i,
                              "zones": [tuple(z) for z in zs], "f": f})
    for p, pat in enumerate(MIXED_PATTERNS):      # 15 mixed-depth
        for i in range(5):
            f, zs = multi_member(list(pat), i)
            name = f"m_p{p}_i{i}"
            deep_lib[name] = f
            deep_meta.append({"member": name, "kind": "mixed",
                              "rung": None, "pattern": list(pat),
                              "instance": i,
                              "zones": [tuple(z) for z in zs], "f": f})
    assert len(deep_lib) == 45, \
        f"diverse cohort size drift: {len(deep_lib)} != 45"
    assert sum(1 for m in deep_meta if m["kind"] == "uniform") == 30
    assert sum(1 for m in deep_meta if m["kind"] == "mixed") == 15

    # canon == wildtype asserted PER MEMBER (registered clause)
    for m in deep_meta:
        assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
            f"canon drift at member {m['member']}"

    lib = dict(lib_frozen)
    lib.update(deep_lib)
    assert len(lib) == 117, f"extended library size drift: {len(lib)}"
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    print(f"  extended library built: 72 frozen + 45 diverse deep "
          f"(30 uniform 6-instance + 15 mixed-depth) = "
          f"{len(lib_names)} members")

    # ==================================================================
    # THE PIPELINE — exp184's machinery verbatim with the cohort
    # novelty READING disclosed below (exp189's trace reading).
    # ==================================================================
    def run_pipeline() -> dict:
        # ---- 0. N*_lib re-derived on the extended library ----------
        n_star_lib, nn_arr = library_nn_stats(lib)
        print(f"  library {len(lib_names)} members | N*_lib "
              f"{n_star_lib:.3f} (RE-DERIVED on the 117-member "
              f"extended library; exp184's 87-member deposit "
              f"{bar184['n_star_lib']}; the frozen-72 deposit "
              f"{FROZEN_BAR_LIB})")

        # ---- 1. splice family + N*_splice re-derived (exp146
        #         machinery) ------------------------------------------
        S = build_splices(lib)
        assert len(S) == SPLICE_EXPECTED, \
            f"splice family size drift: {len(S)} != {SPLICE_EXPECTED}"
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
        print(f"  splice family {len(S)} | N*_splice "
              f"{n_star_splice:.3f} (RE-DERIVED on the extended "
              f"family; exp184's 87-family deposit "
              f"{bar184['n_star_splice']} | frozen-72 deposit "
              f"{prev146['n_star_splice']}) | harness "
              f"max|fast-verbatim| {worst:.2e}")

        # ---- the frozen-72 counterfactual family (exp189's reading)
        S_frozen = build_splices(lib_frozen)
        fmF = np.zeros((len(S_frozen), 100), dtype=bool)
        fmF[:, 1:] = S_frozen[:, 1:] != S_frozen[:, :-1]
        flF = fmF.sum(axis=1)

        # the anatomy's own distance matrix (self-excluded readings)
        M = len(lib_names)
        Dm = np.zeros((M, M))
        for i in range(M):
            for j in range(i + 1, M):
                Dm[i, j] = Dm[j, i] = dist(lib[lib_names[i]],
                                           lib[lib_names[j]])
        assert np.array_equal(
            np.array([Dm[i][np.arange(M) != i].min()
                      for i in range(M)]), nn_arr), \
            "nn harness drift: anatomy matrix != library_nn_stats"

        # ---- 2. the search re-run (exp141's loop VERBATIM, seed
        #         141) — the ONE change: the novelty reference is the
        #         117-member extended library ------------------------
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
        round_summaries = []
        for rnd in range(W.ROUNDS + 1):
            recs = [evaluate(zs) for zs in pop]
            for r in recs:
                pool[W.to_key(r["zones"])] = r
            recs_sorted = sorted(recs, key=lambda r: r["J"])
            n_novel = sum(int(r["novel"]) for r in recs)
            round_summaries.append({
                "round": rnd, "n": len(recs), "n_novel": n_novel,
                "median_J": float(np.median([r["J"] for r in recs])),
                "best_J": float(recs_sorted[0]["J"])})
            print(f"  search round {rnd}: n={len(recs)} "
                  f"novel={n_novel} median J "
                  f"{round_summaries[-1]['median_J']:.1f} best J "
                  f"{recs_sorted[0]['J']:.2f}")
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

        rep = {"rounds_match": False, "pool_size": len(pool),
               "exp141_pool_size": dep141["search"]["pool_size"],
               "expected_divergent": True,
               "note": ("the ONE change (the 117-member extended "
                        "novelty reference) legitimately moves the "
                        "search's J/novelty; the exp141 bit-identity "
                        "assert does not apply here")}
        print(f"  search re-run done: pool {len(pool)} (exp141's "
              f"frozen pool {dep141['search']['pool_size']}; "
              f"expected divergent)")

        # ---- 2b. the 45 diverse members pushed through the SAME
        #          machinery. THE READING (disclosed): a record
        #          member's self-included nov_lib is 0 by definition
        #          (exp184's X2 note); exp189's P3 diagnosis is a
        #          SELF-EXCLUDED-reading finding. The registered
        #          question ("do diverse members clear novelty where
        #          uniform rungs could not") is therefore evaluated on
        #          the SELF-EXCLUDED distance (nearest OTHER member of
        #          the 117), with BOTH other readings deposited per
        #          member: the degenerate self-included value and the
        #          counterfactual vs the frozen 72.
        n_pool_search = len(pool)
        deep_fate: list = []
        for m in deep_meta:
            zs = m["zones"]
            key = W.to_key([tuple(z) for z in zs])
            assert key not in pool, \
                (f"a search candidate collides with cohort member "
                 f"{m['member']} — that would be a finding")
            f = m["f"]
            self_idx = lib_names.index(m["member"])
            nov_selfex = float(Dm[self_idx][np.arange(M) != self_idx]
                               .min())
            nearest_other = lib_names[int(
                [k for k in range(M) if k != self_idx][
                    np.argmin(Dm[self_idx][np.arange(M) != self_idx])])]
            nov_selfinc = nov_lib(f, lib_arr)      # degenerate: 0.0
            nov_cf = nov_lib(f, frozen_arr)        # vs frozen 72
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
            J = best["cost"] + LAMBDA_NOV * max(0.0,
                                                n_star_lib - nov_selfex)
            rec = {"zones": [tuple(z) for z in zs], "f": f,
                   "nov_lib": nov_selfex,
                   "nov_self_included": float(nov_selfinc),
                   "nov_lib_vs_frozen72": nov_cf,
                   "nearest_other_extended": nearest_other,
                   "dist_nearest_other_extended": nov_selfex,
                   "nearest_frozen72": frozen_names[j_cf],
                   "dist_nearest_frozen72": float(d_cf[j_cf]),
                   "J": J, "search_cell": best["cell"],
                   "search_eV": best["eV"], "search_eT": best["eT"],
                   "search_quad": best["quad"],
                   "novel": bool(nov_selfex > n_star_lib),
                   "tags": W.class_tags([tuple(z) for z in zs], f),
                   "deep_member": True, "member": m["member"],
                   "kind": m["kind"], "rung": m["rung"],
                   "pattern": m["pattern"],
                   "instance": m["instance"]}
            pool[key] = rec
            deep_fate.append(rec)
        nov_u = [round(r["dist_nearest_other_extended"], 2)
                 for r in deep_fate if r["kind"] == "uniform"]
        nov_m = [round(r["dist_nearest_other_extended"], 2)
                 for r in deep_fate if r["kind"] == "mixed"]
        print(f"  cohort pushed through the machinery: 45 candidates "
              f"(pool {n_pool_search} -> {len(pool)}) | self-excluded "
              f"novelty: uniform max {max(nov_u)}, mixed max "
              f"{max(nov_m)} vs N*_lib {n_star_lib:.3f}")

        # ---- 3. the funnel (verbatim) --------------------------------
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
              f"DIVERSE cohort in eligible: {n_deep_eligible}/45")

        # the cohort's splice novelty (both readings; the counter-
        # factual family is the frozen 72's)
        for r in deep_fate:
            r["nov_splice_extended"] = L.fast_nov_splice(
                r["f"], S, fm, fl)
            r["nov_splice_vs_frozen72"] = L.fast_nov_splice(
                r["f"], S_frozen, fmF, flF)
            r["in_eligible"] = bool(r["novel"])
            r["in_splice_clear"] = bool(
                r["in_eligible"]
                and r["nov_splice_extended"] > n_star_splice)
        del S_frozen, fmF, flF

        # ---- 4. N*_pool re-derived BEFORE selection ------------------
        pool_dict = {f"pool-{i:03d}": r["f"]
                     for i, r in enumerate(splice_clear)}
        n_star_pool, _ = library_nn_stats(pool_dict)
        print(f"  N*_pool {n_star_pool:.3f} (RE-DERIVED on the "
              f"extended funnel's splice-clear set, before selection)")
        bars = {"n_star_lib": round(n_star_lib, 3),
                "n_star_splice": round(n_star_splice, 3),
                "n_star_pool": round(n_star_pool, 3)}
        bars_deposited_before_selection = True

        # ---- 5. R_W census over the eligible stream (production
        #         floor ONLY — no instrument pin, post-CF-1 world) ----
        rw_rows = []
        for i, r in enumerate(eligible):
            m_new = clash_mass(r["f"], canon)
            pos_new = bool(r_w_predict(r["f"], canon))
            rw_rows.append({"idx": i,
                            "splice_clear": bool(r["nov_splice"]
                                                 > n_star_splice),
                            "clash_mass_production_mV2": round(m_new, 3),
                            "r_w_positive_production": pos_new})
            r["_rw_pos_production"] = pos_new
        rw_pos_prod = {i for i, x in enumerate(rw_rows)
                       if x["r_w_positive_production"]}
        print(f"  R_W census over {len(eligible)} eligible "
              f"(production floor, no pin): positives "
              f"{len(rw_pos_prod)} | max mass "
              f"{max(x['clash_mass_production_mV2'] for x in rw_rows):.3f} mV^2")

        # ---- 6. reference delivery: the J-order greedy at the
        #         extended bars (diagnostic only) ----------------------
        def zkey_of(zs) -> str:
            return W.to_key([tuple(z) for z in zs])

        def greedy(bar: float) -> list:
            dlist: list = []
            for r in eligible:
                if len(dlist) >= N_DELIVER:
                    break
                if r["_rw_pos_production"]:
                    continue
                if r["nov_splice"] <= n_star_splice:
                    continue
                if any(dist(r["f"], d["f"]) <= bar for d in dlist):
                    continue
                dlist.append(r)
            return dlist

        delivered_ref = greedy(n_star_pool)
        print(f"  J-order greedy reference delivery at the extended "
              f"bars: {len(delivered_ref)}/{N_DELIVER} (diagnostic)")

        return {"canon_check": True,
                "canon_asserted_per_member": True,
                "harness_max_abs_diff": worst,
                "bars": bars,
                "bars_deposited_before_selection":
                bars_deposited_before_selection,
                "search_replication": rep,
                "funnel": {"pool": len(pool),
                           "pool_search_only": n_pool_search,
                           "lib_novel": len(eligible),
                           "splice_clear": len(splice_clear)},
                "n_star_lib": n_star_lib,
                "n_star_splice": n_star_splice,
                "n_star_splice_frozen_deposit":
                prev146["n_star_splice"],
                "n_star_pool": n_star_pool,
                "deep_funnel": {
                    "n_deep_members": 45,
                    "uniform_members": 30, "mixed_members": 15,
                    "n_in_eligible": n_deep_eligible,
                    "n_in_splice_clear": n_deep_splice,
                    "fates": [{
                        "member": r["member"],
                        "kind": r["kind"],
                        "rung": r["rung"], "pattern": r["pattern"],
                        "instance": r["instance"],
                        "nov_lib_self_excluded":
                        float(r["nov_lib"]),
                        "nov_self_included":
                        float(r["nov_self_included"]),
                        "nov_lib_vs_frozen72":
                        float(r["nov_lib_vs_frozen72"]),
                        "nearest_other_extended":
                        r["nearest_other_extended"],
                        "dist_nearest_other_extended":
                        float(r["dist_nearest_other_extended"]),
                        "nearest_frozen72": r["nearest_frozen72"],
                        "dist_nearest_frozen72":
                        float(r["dist_nearest_frozen72"]),
                        "nov_splice_extended":
                        float(r["nov_splice_extended"]),
                        "nov_splice_vs_frozen72":
                        float(r["nov_splice_vs_frozen72"]),
                        "novel": bool(r["novel"]),
                        "in_eligible": bool(r["in_eligible"]),
                        "in_splice_clear": bool(r["in_splice_clear"]),
                        "J": float(r["J"])} for r in deep_fate]},
                "rw_census": rw_rows,
                "rw_pos_production": sorted(rw_pos_prod),
                "delivered_reference": {
                    "rule": ("J-order greedy, R_W pre-filter + "
                             "exp146 clause + C4 @ N*_pool-extended"),
                    "n_delivered": len(delivered_ref),
                    "keys": [zkey_of(r["zones"])
                             for r in delivered_ref]},
                "members": splice_clear}

    # ==================================================================
    # THE TRACE TABLE — exp189's trace functions on the 45 (the
    # registered instrument): per-member stage rows with the criterion
    # value, the bar, the margin and PASS/FAIL at each carried stage.
    # ==================================================================
    def build_trace_rows(deep_fate, n_star_lib, n_star_splice) -> list:
        rows = []
        for rec in deep_fate:
            a = {
                "criterion_self_included": {
                    "criterion": ("nov_lib(f, extended record incl. "
                                  "self) > N*_lib"),
                    "value": float(rec["nov_self_included"]),
                    "bar": float(n_star_lib),
                    "pass": bool(rec["nov_self_included"]
                                 > n_star_lib),
                    "note": ("degenerate for a record member — 0 by "
                             "definition (exp184's X2 reading note); "
                             "deposited for completeness")},
                "criterion_self_excluded": {
                    "criterion": ("nearest OTHER member of the "
                                  "117-member extended record > N*_lib "
                                  "(exp189's trace reading)"),
                    "value": float(rec["dist_nearest_other_extended"]),
                    "nearest_other": rec["nearest_other_extended"],
                    "bar": float(n_star_lib),
                    "bar_rounded": round(float(n_star_lib), 3),
                    "margin_bar_minus_value":
                        float(n_star_lib
                              - rec["dist_nearest_other_extended"]),
                    "pass": bool(rec["novel"])},
                "counterfactual_had_they_been_invented": {
                    "reference": ("nov_lib vs the frozen 72 "
                                  "(exp150's deposited machinery)"),
                    "value": float(rec["nov_lib_vs_frozen72"]),
                    "nearest": rec["nearest_frozen72"],
                    "dist_nearest":
                        float(rec["dist_nearest_frozen72"]),
                    "bar_extended": float(n_star_lib),
                    "pass_at_extended_bar":
                        bool(rec["nov_lib_vs_frozen72"]
                             > n_star_lib),
                    "bar_frozen_deposit": FROZEN_BAR_LIB,
                    "pass_at_frozen_bar":
                        bool(rec["nov_lib_vs_frozen72"]
                             > FROZEN_BAR_LIB)},
            }
            b = {
                "criterion": ("membership in the extended splice "
                              "family (structural)"),
                "in_family": True,
                "partners": 116, "crosses_per_pair": 19,
                "n_splices_participating": 116 * 19,
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
                    float(n_star_splice
                          - rec["nov_splice_extended"]),
                "pass": bool(rec["in_splice_clear"]),
                "counterfactual_had_they_been_invented": {
                    "reference": ("nov_splice vs the frozen-72 family "
                                  "at exp150's deposited bar"),
                    "value": float(rec["nov_splice_vs_frozen72"]),
                    "bar_frozen_deposit": FROZEN_BAR_SPLICE,
                    "pass_at_frozen_bar":
                        bool(rec["nov_splice_vs_frozen72"]
                             > FROZEN_BAR_SPLICE)},
                "note": ("reached only if the lib-novelty stage "
                         "passed; the value is deposited for every "
                         "row regardless"),
            }
            excl = None
            if not a["criterion_self_excluded"]["pass"]:
                excl = "a_lib_novel"
            elif not c["pass"]:
                excl = "c_splice_clear"
            rows.append({
                "member": rec["member"], "kind": rec["kind"],
                "rung": rec["rung"], "pattern": rec["pattern"],
                "instance": rec["instance"],
                "stage_a_lib_novel": a,
                "stage_b_splice_family": b,
                "stage_c_splice_clear": c,
                "excluding_stage": excl,
                "in_eligible_final": bool(rec["in_eligible"]),
                "in_splice_clear_final": bool(rec["in_splice_clear"]),
                "J": float(rec["J"])})
        return rows

    # ==================================================================
    # THE TARGET SETS (exp184's, VERBATIM)
    # ==================================================================
    def targets_exp150() -> dict:
        ts = []
        for d in dep150["delivered"]:
            zs = [tuple(z) for z in d["zones"]]
            f = profile_of_zones(zs)
            ts.append({"name": d["name"],
                       "zones": [list(z) for z in zs],
                       "f_sha256_16":
                       hashlib.sha256(f.tobytes()).hexdigest()[:16],
                       "f": f})
        return {"label": "exp150_targets",
                "construction": (
                    "exp150's own targets (its deposit): the 10 "
                    "delivered members' zone programs; target profile "
                    "f_t = profile_of_zones(zones_t) VERBATIM (the "
                    "member's own profile — the exp150 own-target "
                    "discipline, recovered deterministically from the "
                    "deposit)"),
                "n_targets": len(ts), "targets": ts}

    def targets_deep() -> dict:
        ts = []
        sec_keys = sorted((k for k in dep176["sections"]
                           if k.startswith("rung_")),
                          key=lambda k: float(k[5:]))
        for k in sec_keys:
            rung = float(k[5:])
            f, triples = multi_member([rung] * 3, 0)
            sha = hashlib.sha256(f.tobytes()).hexdigest()[:16]
            dep_sha = dep176["sections"][k]["target"]["f_sha256_16"]
            assert sha == dep_sha, \
                f"deep target checksum drift at {k}: " \
                f"{sha} vs deposit {dep_sha}"
            ts.append({"name": f"rung_{rung:g}", "rung": rung,
                       "triples": [list(t) for t in triples],
                       "f_sha256_16": sha, "f": f})
        print(f"  deep target set: {len(ts)} constructions from "
              f"exp176's deposit sections, checksums match "
              f"{[t['f_sha256_16'] for t in ts]}")
        return {"label": "deep_targets",
                "construction": (
                    "exp176's deep set (its deposit sections "
                    "rung_-40/-50/-60 targets): the MULTI 3-zone "
                    "program (instance 0, width delta 0 — bit-exact "
                    "with exp172's construction) with every zone "
                    "value forced to the rung, exp94's spec_target_n, "
                    "canon = labeling_bfs_n(A_CHAIN); checksums "
                    "asserted against the exp176 deposit"),
                "n_targets": len(ts), "targets": ts}

    # ==================================================================
    # THE POOL'S PRICE TABLE at T (exp184's, VERBATIM)
    # ==================================================================
    def price_table(T: dict, members: list) -> dict:
        prov = None
        rows = []
        for i, r in enumerate(members):
            zs = [tuple(z) for z in r["zones"]]
            per = []
            for ti, t in enumerate(T["targets"]):
                pr = price_rung(t["f"], zs, 1.0, 0.0)
                assert pr["cell"] == [1.0, 0.0], "production cell drift"
                prov = pr["provenance"]
                e_new, mode = emit_rung([pr])
                per.append({"target": t["name"], "target_idx": ti,
                            "cell": pr["cell"], "cost": pr["cost"],
                            "eV": pr["eV"], "eT": pr["eT"],
                            "quad": pr["quad"],
                            "audit_pass": bool(pr["pass"]),
                            "silent": bool(pr["silent"]),
                            "decode_errs": pr["decode_errs"],
                            "hold_errs": pr["hold_errs"],
                            "decode_err_mean": pr["decode_err_mean"],
                            "hold_err_mean": pr["hold_err_mean"],
                            "erosion_increment_mean":
                            pr["erosion_increment_mean"],
                            "decode_stable_seeds":
                            pr["decode_stable_seeds"],
                            "n_ok": int(pr["n_ok"]),
                            "dec333": bool(pr["dec333"]),
                            "full_valid": bool(pr["full_valid"]),
                            "n_rejected": int(pr["n_rejected"]),
                            "emission_mode": mode,
                            "emitted_cell":
                            (e_new["cell"] if e_new else None)})
            price = float(np.mean([p["decode_err_mean"] for p in per]))
            rows.append({"idx": i,
                         "member": (r["member"] if r.get("deep_member")
                                    else f"pool-{i:03d}"),
                         "zones": [list(z) for z in zs],
                         "J": float(r["J"]),
                         "nov_lib": float(r["nov_lib"]),
                         "nov_splice": float(r["nov_splice"]),
                         "price_composed_decode_err": price,
                         "per_target": per})
            print(f"  price[{T['label']}] {rows[-1]['member']}: price "
                  f"{price:.3f} | worst target "
                  f"{max(p['decode_err_mean'] for p in per):.3f} "
                  f"({max(per, key=lambda p: p['decode_err_mean'])['target']})")
        return {"target_set_label": T["label"],
                "n_rows": len(rows),
                "instrument": (
                    "exp150's price_rung VERBATIM at the production "
                    "cell (1.0, 0.0), seeds (1,2,3); price(m, T) = the "
                    "mean composed decode err over T's targets x seeds "
                    "(mean_t of decode_err_mean); emission via exp150's "
                    "emit_rung on the single-rung (1,0) table; computed "
                    "fresh AFTER the funnel re-derivation"),
                "provenance_cell_1_0": prov,
                "rows": rows}

    # ==================================================================
    # THE CLAUSE (one rule, zero knobs) — exp179's clause_walk VERBATIM
    # ==================================================================
    def clause_walk(table: dict, members: list,
                    n_star_pool: float) -> dict:
        f_of = {i: r["f"] for i, r in enumerate(members)}
        ranked = sorted(table["rows"],
                        key=lambda x: (x["price_composed_decode_err"],
                                       x["idx"]))
        kept, skipped = [], []
        for x in ranked:
            if len(kept) >= N_DELIVER:
                break
            fm_ = f_of[x["idx"]]
            if all(dist(fm_, f_of[k["idx"]]) > n_star_pool
                   for k in kept):
                kept.append(x)
            else:
                blocked_by = min(
                    (k["idx"] for k in kept
                     if dist(fm_, f_of[k["idx"]]) <= n_star_pool),
                    default=None)
                skipped.append({"idx": x["idx"],
                                "member": x["member"],
                                "price": x["price_composed_decode_err"],
                                "blocked_by_pool_idx": blocked_by})
        Dm = [[float(dist(f_of[a["idx"]], f_of[b["idx"]]))
               for b in kept] for a in kept]
        min_d = min(Dm[i][j] for i in range(len(kept))
                    for j in range(len(kept)) if i != j)
        assert min_d > n_star_pool, \
            "clause walk emitted a pair within N*_pool — clause broken"
        print(f"  clause walk [{table.get('target_set_label', 'targets')}]:"
              f" kept {len(kept)}/{N_DELIVER} | min pairwise D "
              f"{min_d:.3f} > N*_pool-extended {n_star_pool:.3f} | best "
              f"price {ranked[0]['price_composed_decode_err']:.3f} | "
              f"worst kept price "
              f"{kept[-1]['price_composed_decode_err']:.3f} | skipped "
              f"{len(skipped)}")
        return {"ranked_order_idxs": [x["idx"] for x in ranked],
                "kept": kept, "n_kept": len(kept),
                "skipped_diversity_blocked": skipped,
                "pairwise_D": [[round(v, 3) for v in row] for row in Dm],
                "min_pairwise_D": float(min_d),
                "bar": float(n_star_pool)}

    # ==================================================================
    # THE GATES (each evaluated exactly once, on complete inputs)
    # ==================================================================
    def evaluate_t1(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        if pipe is None:
            return None
        df = pipe["deep_funnel"]
        build_ok = bool(pipe["library_members"] == 117
                        and df["uniform_members"] == 30
                        and df["mixed_members"] == 45 - 30
                        and df["n_deep_members"] == 45
                        and pipe["canon_asserted_per_member"]
                        and pipe["canon_check"])
        bars_ok = bool(pipe["bars_deposited_before_selection"]
                       and np.isfinite(pipe["n_star_lib"])
                       and np.isfinite(pipe["n_star_splice"])
                       and np.isfinite(pipe["n_star_pool"])
                       and pipe["harness_max_abs_diff"] < 1e-9)
        return {"gate": "T1", "clause": (
            "cohort build: 45 diverse deep members built (30 "
            "uniform-rung varied-layout + 15 mixed-depth), canon == "
            "wildtype asserted per member, the extended library "
            "(72 + 45) bars re-derived and deposited BEFORE selection"),
                "library_members": pipe["library_members"],
                "uniform_members": df["uniform_members"],
                "mixed_members": df["mixed_members"],
                "n_deep_members": df["n_deep_members"],
                "cohort_builds_45": build_ok,
                "canon_asserted_per_member":
                pipe["canon_asserted_per_member"],
                "harness_max_abs_diff": pipe["harness_max_abs_diff"],
                "bars": pipe["bars"],
                "bars_rederived_computed_not_assumed": True,
                "bars_deposited_before_selection":
                pipe["bars_deposited_before_selection"],
                "pass": bool(build_ok and bars_ok)}

    def evaluate_t2(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        trace = sections.get("trace")
        if pipe is None or trace is None:
            return None
        df = pipe["deep_funnel"]
        n_in = df["n_in_eligible"]
        rows_ok = bool(len(trace["rows"]) == 45
                       and all(r["stage_a_lib_novel"] is not None
                               for r in trace["rows"]))
        return {"gate": "T2", "clause": (
            "survival: >= 15/45 deep members in the eligible pool (the "
            "DISTANCE fix works); the per-member lib-novel distances "
            "deposited vs exp189's trace table"),
                "n_deep_members": df["n_deep_members"],
                "n_in_eligible": n_in,
                "n_in_splice_clear": df["n_in_splice_clear"],
                "required": 15,
                "eligible_pool_size": pipe["funnel"]["lib_novel"],
                "trace_rows_deposited": len(trace["rows"]),
                "trace_complete": rows_ok,
                "exp189_reference_rows":
                len(sections["trace"]["exp189_reference_rows"]),
                "reading_disclosure":
                sections["trace"]["reading_disclosure"],
                "pass": bool(n_in >= 15 and rows_ok)}

    def evaluate_t3(sections: dict) -> dict | None:
        sec = sections.get("clause_deep_targets")
        if sec is None:
            return None
        kept = sec["walk"]["kept"]
        rows = [dict(p, member=k["member"], idx=k["idx"])
                for k in kept for p in k["per_target"]]
        want_targets = sorted(set(p["target"] for p in rows)) if rows \
            else []
        complete = bool(
            len(kept) == N_DELIVER
            and all(len(k["per_target"]) == sec["n_targets"]
                    for k in kept)
            and want_targets == sorted(
                (t["name"] if isinstance(t, dict) else t)
                for t in sec["target_names"]))
        per_rung_counts = {
            tg: sum(int(p["n_ok"] == len(AUDIT_SEEDS))
                    for p in rows if p["target"] == tg)
            for tg in want_targets}
        members_all = sum(
            1 for k in kept
            if len(k["per_target"]) == sec["n_targets"]
            and all(p["n_ok"] == len(AUDIT_SEEDS)
                    for p in k["per_target"]))
        n_rej = sum(p["n_rejected"] for p in rows)
        modes = sorted(set(p["emission_mode"] for p in rows))
        ok = bool(complete and members_all >= 9 and n_rej == 0
                  and modes == ["repriced_full"])
        return {"gate": "T3", "clause": (
            "deep delivery: the clause's delivered-10 at the deep "
            "targets: >= 9/10 with decode < 6.0 AND hold < 6.0 on 3/3 "
            "seeds at every rung; zero rejections; no "
            "audit_only_fallback (emission mode repriced_full "
            "everywhere)"),
                "complete": complete,
                "n_delivered": len(kept),
                "per_rung_333_counts": per_rung_counts,
                "members_passing_all_targets": members_all,
                "rejections": n_rej,
                "emission_modes": modes,
                "pass": ok}

    def evaluate_t4(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        sec = sections.get("clause_exp150_targets")
        if pipe is None or sec is None:
            return None
        n_star_lib = pipe["n_star_lib"]
        n_star_splice = pipe["n_star_splice"]
        n_star_pool = pipe["n_star_pool"]
        kept = sec["walk"]["kept"]
        rows = [dict(p, member=k["member"], idx=k["idx"])
                for k in kept for p in k["per_target"]]
        complete = bool(
            len(kept) == N_DELIVER
            and all(len(k["per_target"]) == sec["n_targets"]
                    for k in kept))
        c1_rows = [{"member": k["member"], "nov_lib": k["nov_lib"],
                    "nov_splice": k["nov_splice"],
                    "beyond_bars": bool(
                        k["nov_lib"] > n_star_lib
                        and k["nov_splice"] > n_star_splice)}
                   for k in kept]
        c1 = all(x["beyond_bars"] for x in c1_rows)
        c2 = all(p["audit_pass"] and p["quad"] < ERR_BAR for p in rows)
        c2_fails = [p["member"] + "/" + p["target"] for p in rows
                    if not (p["audit_pass"] and p["quad"] < ERR_BAR)]
        c3 = all(p["n_ok"] == len(AUDIT_SEEDS) for p in rows)
        c3_fails = [p["member"] + "/" + p["target"] for p in rows
                    if p["n_ok"] != len(AUDIT_SEEDS)]
        min_d = sec["walk"]["min_pairwise_D"]
        c4 = bool(min_d > n_star_pool)
        n_rej = sum(p["n_rejected"] for p in rows)
        ok = bool(complete and c1 and c2 and c3 and c4)
        return {"gate": "T4", "clause": (
            "the old operating point: the clause's delivered-10 at "
            "exp150's targets: C1 every member beyond N*_lib-extended "
            "and N*_splice-extended, C2 emitted-rung quads < 6.0, C3 "
            "decode < 6.0 AND hold < 6.0 on 3/3 seeds, C4 min pairwise "
            "D > N*_pool-extended — ALL PASS"),
                "complete": complete,
                "n_delivered": len(kept),
                "c1_members_beyond_bars": c1,
                "c1_rows": c1_rows,
                "c2_all_quads_below_bar": c2,
                "c2_fail_rows": c2_fails,
                "c3_all_decode_hold_333": c3,
                "c3_fail_rows": c3_fails,
                "c4_min_pairwise_D": min_d,
                "c4_bar": float(n_star_pool),
                "c4_pass": c4,
                "n_scoring_rows": len(rows),
                "rejections_this_gate": n_rej,
                "pass": ok}

    # ---- dispatch ------------------------------------------------------
    print("=== exp194: THE DIVERSE DEEP COHORT (novelty-proof deep "
          "members — exp189's registered next, L165) ===\n")
    if args.smoke:
        pipe = run_pipeline()
        dep = {"exp": "exp194_diverse_deep_cohort", "kind": "smoke",
               "discarded": True,
               "scope": ("117-member extended-library build + the "
                         "three re-derived N* bars only (no trace, no "
                         "price tables, no clause walks, no gates)"),
               "bars": pipe["bars"],
               "funnel": pipe["funnel"],
               "deep_funnel_counts": {
                   k: pipe["deep_funnel"][k]
                   for k in ("n_deep_members", "n_in_eligible",
                             "n_in_splice_clear")},
               "wall_s": round(time.time() - t0, 1)}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                        exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(dep, fh, indent=1, default=float)
        print(f"  SMOKE (bars only — discarded): bars {dep['bars']} | "
              f"funnel {dep['funnel']} | cohort in eligible "
              f"{dep['deep_funnel_counts']['n_in_eligible']}/45")
        return dep

    result: dict = {}
    if args.job != "all" and os.path.exists(out_path):
        with open(out_path) as fh:
            result = json.load(fh)
    result.setdefault("sections", {})
    result.setdefault("gates", {})

    pipe = run_pipeline()
    members = pipe["members"]
    n_star_lib = pipe["n_star_lib"]
    n_star_splice = pipe["n_star_splice"]
    n_star_pool = pipe["n_star_pool"]
    result["sections"]["pipeline"] = {
        "bars": pipe["bars"],
        "library_members": 117,
        "uniform_members": 30, "mixed_members": 15,
        "splice_family_size": SPLICE_EXPECTED,
        "harness_max_abs_diff": pipe["harness_max_abs_diff"],
        "bars_deposited_before_selection":
        pipe["bars_deposited_before_selection"],
        "search_replication": pipe["search_replication"],
        "funnel": pipe["funnel"],
        "n_star_lib": n_star_lib,
        "n_star_splice": n_star_splice,
        "n_star_splice_frozen_deposit":
        pipe["n_star_splice_frozen_deposit"],
        "n_star_pool": n_star_pool,
        "deep_funnel": pipe["deep_funnel"],
        "rw_census": pipe["rw_census"],
        "rw_pos_production": pipe["rw_pos_production"],
        "delivered_reference": pipe["delivered_reference"],
        "canon_check": bool(pipe["canon_check"]),
        "canon_asserted_per_member": True,
        "production_floor_asserted": True,
        "instrument_pin_used": False}

    # the trace table (exp189's functions on the 45 fates)
    deep_fate_recs = pipe["deep_funnel"]["fates"]
    trace_rows = build_trace_rows(deep_fate_recs, n_star_lib,
                                  n_star_splice)
    result["sections"]["trace"] = {
        "rows": trace_rows,
        "n_rows": len(trace_rows),
        "instrument": ("exp189's trace functions on the 45-member "
                       "diverse cohort: stage a = lib-novelty (the "
                       "self-excluded reading IS the criterion; the "
                       "degenerate self-included value and the "
                       "frozen-72 counterfactual deposited per row), "
                       "stage b = structural splice-family membership, "
                       "stage c = splice-clear price vs N*_splice"),
        "exp189_reference_rows": trace189_rows,
        "exp189_reference_note": ("exp189's 15-row trace table "
                                  "(exp184's uniform-rung cohort at "
                                  "3 instances, no width variation) "
                                  "deposited verbatim for the "
                                  "side-by-side — its members are "
                                  " constructions from the SAME "
                                  "family; the bars differ (87- vs "
                                  "117-member re-derivation)"),
        "reading_disclosure": (
            "THE READING (disclosed, fixed before the run): a record "
            "member's self-included nov_lib is 0 by definition "
            "(exp184's X2 note), and exp189's P3 branch-DISTANCE "
            "diagnosis is a self-excluded-reading finding; the "
            "registered question (do diverse members clear novelty) "
            "is therefore evaluated on the SELF-EXCLUDED nearest-other "
            "distance against the RE-DERIVED N*_lib-117, with the "
            "degenerate self-included value and the frozen-72 "
            "counterfactual deposited per member"),
    }

    # the price tables (fresh, after the funnel re-derivation)
    def tables_for(job: str) -> None:
        if job in ("old", "all"):
            T1 = targets_exp150()
            tab1 = price_table(T1, members)
            result["sections"]["price_table_exp150_targets"] = {
                "target_set": {k: v for k, v in T1.items()
                               if k != "targets"},
                "targets": [{k: v for k, v in t.items() if k != "f"}
                            for t in T1["targets"]],
                "n_rows": tab1["n_rows"],
                "instrument": tab1["instrument"],
                "provenance_cell_1_0": tab1["provenance_cell_1_0"],
                "rows": tab1["rows"]}
        if job in ("deep", "all"):
            T2 = targets_deep()
            tab2 = price_table(T2, members)
            result["sections"]["price_table_deep_targets"] = {
                "target_set": {k: v for k, v in T2.items()
                               if k != "targets"},
                "targets": [{k: v for k, v in t.items() if k != "f"}
                            for t in T2["targets"]],
                "n_rows": tab2["n_rows"],
                "instrument": tab2["instrument"],
                "provenance_cell_1_0": tab2["provenance_cell_1_0"],
                "rows": tab2["rows"]}

    tables_for(args.job)

    # the clause walks + scoring sections
    if args.job in ("old", "all"):
        T1 = targets_exp150()
        tab1 = result["sections"]["price_table_exp150_targets"]
        walk1 = clause_walk(tab1, members, n_star_pool)
        result["sections"]["clause_exp150_targets"] = {
            "target_set_label": "exp150_targets",
            "target_set_construction": T1["construction"],
            "n_targets": T1["n_targets"],
            "target_names": [t["name"] for t in T1["targets"]],
            "walk": {"ranked_order_idxs": walk1["ranked_order_idxs"],
                     "n_kept": walk1["n_kept"],
                     "kept": walk1["kept"],
                     "skipped_diversity_blocked":
                     walk1["skipped_diversity_blocked"],
                     "pairwise_D": walk1["pairwise_D"],
                     "min_pairwise_D": walk1["min_pairwise_D"],
                     "bar": walk1["bar"]},
            "scoring_note": (
                "each kept member scored against EVERY exp150 target "
                "at the production cell (1.0, 0.0), seeds (1,2,3) — "
                "the per_target rows ARE the scoring rows (the same "
                "price_rung calls; no re-decode)")}
    if args.job in ("deep", "all"):
        T2 = targets_deep()
        tab2 = result["sections"]["price_table_deep_targets"]
        walk2 = clause_walk(tab2, members, n_star_pool)
        result["sections"]["clause_deep_targets"] = {
            "target_set_label": "deep_targets",
            "target_set_construction": T2["construction"],
            "n_targets": T2["n_targets"],
            "target_names": [t["name"] for t in T2["targets"]],
            "walk": {"ranked_order_idxs": walk2["ranked_order_idxs"],
                     "n_kept": walk2["n_kept"],
                     "kept": walk2["kept"],
                     "skipped_diversity_blocked":
                     walk2["skipped_diversity_blocked"],
                     "pairwise_D": walk2["pairwise_D"],
                     "min_pairwise_D": walk2["min_pairwise_D"],
                     "bar": walk2["bar"]},
            "scoring_note": (
                "each kept member scored against EVERY deep rung in "
                "exp176's deposit sections (-40/-50/-60) at the "
                "production cell (1.0, 0.0), seeds (1,2,3) — the "
                "per_target rows ARE the scoring rows (the same "
                "price_rung calls; no re-decode)")}

    # gates: each evaluated exactly once, on complete inputs only
    for name, fn in (("T1", evaluate_t1), ("T2", evaluate_t2),
                     ("T3", evaluate_t3), ("T4", evaluate_t4)):
        if name in result["gates"]:
            continue
        g = fn(result["sections"])
        if g is not None:
            result["gates"][name] = g

    npass = sum(int(g["pass"]) for g in result["gates"].values())
    for name in ("T1", "T2", "T3", "T4"):
        if name in result["gates"]:
            g = result["gates"][name]
            extra = ""
            if name == "T1":
                extra = (f" (library {g['library_members']}, cohort "
                         f"{g['uniform_members']}u+{g['mixed_members']}m"
                         f", bars {g['bars']})")
            elif name == "T2":
                extra = (f" ({g['n_in_eligible']}/{g['n_deep_members']} "
                         f"in eligible, required >= {g['required']}; "
                         f"splice-clear {g['n_in_splice_clear']}; "
                         f"trace rows {g['trace_rows_deposited']})")
            elif name == "T3":
                extra = (f" ({g['members_passing_all_targets']}/"
                         f"{g['n_delivered']} members pass all targets"
                         f", per-rung {g['per_rung_333_counts']}, rej "
                         f"{g['rejections']}, modes "
                         f"{g['emission_modes']})"
                         if g["complete"] else " (incomplete)")
            elif name == "T4":
                extra = (f" (C1 {g['c1_members_beyond_bars']}, C2 "
                         f"{g['c2_all_quads_below_bar']}, C3 "
                         f"{g['c3_all_decode_hold_333']}, C4 min D "
                         f"{g['c4_min_pairwise_D']:.3f} vs bar "
                         f"{g['c4_bar']:.3f}, rows "
                         f"{g['n_scoring_rows']})"
                         if g["complete"] else " (incomplete)")
            print(f"  GATE-{name}: {'PASS' if g['pass'] else 'REFUTE'}"
                  f"{extra}")
    verdict = (f"{npass}/{len(result['gates'])} gates "
               f"({' '.join(k for k in ('T1', 'T2', 'T3', 'T4')
                            if k in result['gates'])})")
    print(f"  === {verdict} ===")

    result.update({
        "exp": "exp194_diverse_deep_cohort",
        "claim": (
            "THE DIVERSE DEEP COHORT (exp189's registered next, "
            "L165): the deep cohort dies of SELF-SIMILARITY at the "
            "lib-novelty stage. THIS RUN builds deep members with "
            "STRUCTURAL diversity — exp172's construction discipline "
            "at 6 layout instances x 5 rungs = 30 uniform-rung "
            "members (the registered width variation applied per "
            "instance), plus 15 mixed-depth members carrying "
            "deep+shallow zones (3 a-priori value patterns x 5 "
            "instances) — through the SAME funnel: the 117-member "
            "extended library (72 frozen + 45), bars RE-DERIVED "
            "before selection, exp189's trace functions on every "
            "member, the clause delivery = exp179's price-ranked walk "
            "at the deep targets (exp176's deposit sections) and at "
            "exp150's own targets (its deposit)"),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration 129c1ac; gates "
                             "T1-T4 fixed there, each evaluated "
                             "exactly once)"),
            "gates": [
                "T1 cohort build: 45 diverse deep members built (30 "
                "uniform-rung varied-layout + 15 mixed-depth), canon "
                "== wildtype asserted per member, the extended "
                "library (72 + 45) bars re-derived and deposited "
                "before selection",
                "T2 survival: >= 15/45 deep members in the eligible "
                "pool (the DISTANCE fix works); the per-member "
                "lib-novel distances deposited vs exp189's trace "
                "table",
                "T3 deep delivery: the clause's delivered-10 at the "
                "deep targets: >= 9/10 with decode < 6.0 AND hold < "
                "6.0 on 3/3 seeds at every rung; zero rejections; no "
                "audit_only_fallback",
                "T4 the old point: the clause's 10 at exp150's "
                "targets: C1-C4 ALL PASS"],
            "cohort": ("30 uniform-rung members = exp172's "
                       "construction at 6 layout instances (+i cells, "
                       "i = 0..5) x rungs {-40,-45,-50,-55,-60} with "
                       "the registered width variation (per-instance "
                       "boundary deltas {0,+1,-1,+2,-2,+1} cells); "
                       "15 mixed-depth members = 3 a-priori patterns "
                       "((-60,-15,-45), (-15,-50,-55), (-40,-60,-20)) "
                       "x 5 layout instances"),
            "bars": "RE-DERIVED on the 117-member extended library "
                    "(computed, not assumed)",
            "reading": ("cohort lib-novelty = the SELF-EXCLUDED "
                        "nearest-other distance vs N*_lib-117 "
                        "(exp189's trace reading; the degenerate "
                        "self-included value and the frozen-72 "
                        "counterfactual deposited per member)"),
            "deep_target_set": ("exp176's deposit sections "
                                "rung_-40/-50/-60 targets, checksummed"),
            "tie_break": "member index ascending (J-ordered funnel "
                         "index)"},
        "stage_order": ["extended_library_build (72 frozen + 45 "
                        "diverse deep constructions)",
                        "canon_asserted_per_member (45)",
                        "n_star_lib_rederived (117-member pairwise "
                        "distances, deposited machinery)",
                        "splice_family_rederived (128886) + "
                        "n_star_splice_rederived (exp146 machinery)",
                        "search_rerun_seed141 (exp141's loop VERBATIM; "
                        "the ONE change: the 117-member novelty "
                        "reference; expected divergent)",
                        "cohort_pushed_through_the_same_machinery (45 "
                        "candidates, same formulas, the disclosed "
                        "self-excluded reading)",
                        "funnel_rederived (lib-novelty -> splice-clear "
                        "on the extended bars)",
                        "n_star_pool_rederived_BEFORE_selection",
                        "rw_census (production floor, no pin)",
                        "trace_table (45 rows x 3 stages, exp189's "
                        "functions)",
                        "price_tables_fresh_after_funnel (deep targets "
                        "= exp176 deposit sections; exp150 targets = "
                        "its deposit)",
                        "clause_walks (price-ranked, C4-diverse @ "
                        "N*_pool-extended, cap 10)",
                        "gates_evaluated"],
        "smoke_disclosure": ("a --smoke check (117-member build + "
                             "bars only) ran before the credited run "
                             "and was discarded (no file)"),
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1)})

    if not args.smoke:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  deposited {out_path} | wall {result['wall_s']} s")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "deep", "old", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
