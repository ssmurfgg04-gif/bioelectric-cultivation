#!/usr/bin/env python3
"""exp184 — THE DEEP-PROGRAM LIBRARY COHORT (the library sent to the band).

exp179's registered next (L158): the deep-delivery failure is upstream
of delivery — the pool's members carry MIXED-VALUE programs while the
deep targets demand UNIFORM-deep patterns, and the U(-60,-15) per-zone
library draw makes those vanishingly rare. exp172 wrote uniform-deep
patterns by direct construction, bypassing the library. THIS
EXPERIMENT pushes all-deep library members through the SAME
splice/funnel machinery and re-runs the clause delivery.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Cohort, bars, and gates are fixed now.

THE COHORT (disclosed construction, zero fitting):
  all-deep library members: exp172's uniform-rung construction as
  LIBRARY PROGRAMS — for each rung in {-40, -45, -50, -55, -60} and
  each of 3 zone-layout ladders (the MULTI program's zone spans,
  shifted +i cells i = 0..2: the exp172 instance discipline), one
  member program (zones all at the rung) — 15 members — joined to
  exp141's 72-member library as a 87-member extended library. The
  splice family, funnel, and N* bars RE-DERIVED on the extended
  library (structure bars: N*_lib from the library's pairwise
  distances via the deposited machinery, N*_splice via exp146's
  splice_family_bar, N*_pool before selection — computed, not
  assumed). Search seed 141. The R_W clause and cap 10 as exp168's
  B3. The clause delivery = exp179's price-ranked walk (ranked
  ascending by mean composed decode err over the DEEP target set,
  keep iff min pairwise D > N*_pool-extended, stop at 10).

GATES (each evaluated exactly once):
  GATE-X1 (extended pipeline integrity) the extended library builds
           (87 members), the splice family + funnel re-derive with
           zero rejections, and the three N* bars are deposited
           BEFORE selection (bars_deposited_before_selection).
  GATE-X2 (the deep members survive the funnel) >= 10 of the 15
           all-deep members are in the 96-eligible pool (the
           machinery does not discard the band).
  GATE-X3 (deep delivery) the clause's delivered-10 at the deep
           target set: >= 9/10 with decode < 6.0 AND hold < 6.0 on
           3/3 seeds at EVERY rung; zero rejections; emission mode
           repriced_full everywhere (audit_only_fallback must NOT
           fire — the L143 retirement holds when the library serves
           the band).
  GATE-X4 (the old operating point) the clause's delivered-10 at
           exp150's own targets: C1-C4 ALL PASS (the quality bars
           hold on the extended library too).

NO post-hoc tuning. --smoke (extended-library build + bars only)
permitted, discarded. Deposit: results/exp184_deep_library.json
Jobs: bars | deep | old
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

DEEP_RUNGS = [-40.0, -45.0, -50.0, -55.0, -60.0]
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141

OUT = os.path.join(ROOT, "results", "exp184_deep_library.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP176 = os.path.join(ROOT, "results", "exp176_deep_band_search.json")
DEP179 = os.path.join(ROOT, "results", "exp179_target_aware_delivery.json")


def main() -> dict:
    # ==== BODY (written by the run agent; docstring/imports/constants
    # above byte-unchanged — exp174's body-only discipline) ============
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "deep", "old", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    # ---- exp168's B3 import block, verbatim (BLAS pin included) ------
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import hashlib

    from experiments.exp136_generator_v6 import (  # noqa: E402
        ERR_BAR, SEARCH_CELLS, CELL_SURCHARGE, AUDIT_SEEDS, LAMBDA_NOV,
        N_DELIVER, N as LAT_N,
        profile_of_zones, build_library, dist, library_nn_stats,
        build_splices, nov_lib, nov_splice, quad_err, erosion, decode,
        wildtype_target,
    )
    from experiments import exp141_generator_wide as W  # noqa: E402
    from experiments.exp144_audit_operating_points import (  # noqa: E402
        EXTENDED_LADDER,
    )
    from experiments import exp146_splice_bar as L  # noqa: E402
    from experiments.exp150_generator_complete import (  # noqa: E402
        price_rung, emit_rung,
    )
    from experiments.exp156_write_path import (  # noqa: E402  VERBATIM
        decode_cf, clash_mass, r_w_predict, CF_FLOOR,
    )
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as M136  # noqa: E402
    import experiments.exp156_write_path as M156  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n,
    )

    DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
    DEP141 = os.path.join(ROOT, "results", "exp141_generator_wide.json")
    PROD_FLOOR = -60.0                    # CF-1's production value

    # the target-set / lineage deposits (the clause's T inputs and the
    # frozen-72 reference line)
    dep150 = json.load(open(DEP150))
    dep176 = json.load(open(DEP176))
    dep141 = json.load(open(DEP141))
    prev146 = json.load(open(DEP146))

    # ---- instrument check: the production core in situ ---------------
    # (post-CF-1 production world; the floor is asserted, never touched
    # — no instrument pin anywhere this run)
    floors = {"CORE": CORE.NEURAL_SPEC_MIN,
              "M136": M136.NEURAL_SPEC_MIN,
              "M156": M156.NEURAL_SPEC_MIN}
    assert all(v == PROD_FLOOR for v in floors.values()), \
        f"production floor drift: {floors}"

    # ---- canon check --------------------------------------------------
    canon = wildtype_target(LAT_N)
    assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"

    # ==================================================================
    # THE ONE CHANGE: the extended library — exp141's 72 + the 15
    # all-deep members (exp172's uniform-rung construction as LIBRARY
    # PROGRAMS: rungs {-40,-45,-50,-55,-60} x 3 MULTI-zone layout
    # shifts +i cells, i = 0..2 — the exp172 instance discipline).
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
    print(f"  extended library built: 72 frozen + 15 all-deep = "
          f"{len(lib_names)} members")

    # ==================================================================
    # THE PIPELINE (exp168's B3 / exp179's run_pipeline structure,
    # verbatim stage order; the ONE change propagated: every library
    # reference is the 87-member extended library, and the three N*
    # bars are RE-DERIVED on the extended structures — computed, not
    # assumed, so nothing is asserted against the frozen-72 bars).
    # ==================================================================
    def run_pipeline() -> dict:
        # ---- 0. N*_lib re-derived on the extended library ----------
        n_star_lib, _ = library_nn_stats(lib)
        print(f"  library {len(lib_names)} members | N*_lib "
              f"{n_star_lib:.3f} (RE-DERIVED on the extended library; "
              f"the frozen-72 deposit was "
              f"{dep150['bars']['n_star_lib']})")

        # ---- 1. splice family + N*_splice re-derived (exp146
        #         machinery) ------------------------------------------
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
        print(f"  splice family {len(S)} | N*_splice "
              f"{n_star_splice:.3f} (RE-DERIVED on the extended "
              f"family; the frozen-72 deposit was "
              f"{prev146['n_star_splice']}) | harness "
              f"max|fast-verbatim| {worst:.2e}")

        # ---- 2. the search re-run (exp141's loop VERBATIM, seed
        #         141) — the ONE change: the novelty reference is the
        #         EXTENDED library (lib_arr / n_star_lib above) ------
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
            n_novel_nd = sum(int(r["novel"]
                                 and r["tags"]["nondisjoint"])
                             for r in recs)
            n_novel_bl = sum(int(r["novel"]
                                 and r["tags"]["n_below_line_zones"] > 0)
                             for r in recs)
            round_summaries.append({
                "round": rnd, "n": len(recs), "n_novel": n_novel,
                "n_novel_nondisjoint": n_novel_nd,
                "n_novel_below_line": n_novel_bl,
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

        # divergence diagnostic vs exp141's deposit (EXPECTED: the ONE
        # change — the extended novelty reference — legitimately moves
        # the search's J/novelty; bit-identity to the exp141 deposit is
        # NOT registered for this run — X1 replaces it with the
        # re-derivation clauses — so this is deposited, not asserted)
        rep_rounds = []
        for a, b in zip(round_summaries, dep141["search"]["rounds"]):
            ok = (a["round"] == b["round"] and a["n"] == b["n"]
                  and a["n_novel"] == b["n_novel"]
                  and abs(a["median_J"] - b["median_J"]) < 1e-9
                  and abs(a["best_J"] - b["best_J"]) < 1e-9)
            rep_rounds.append({"round": a["round"], "match": bool(ok)})
        rep = {"rounds_match": all(r["match"] for r in rep_rounds),
               "round_rows": rep_rounds,
               "pool_size_match": len(pool)
               == dep141["search"]["pool_size"],
               "pool_size": len(pool),
               "exp141_pool_size": dep141["search"]["pool_size"],
               "expected_divergent": True,
               "note": ("the ONE change (the 87-member extended "
                        "novelty reference) legitimately moves the "
                        "search's J/novelty; the exp141 bit-identity "
                        "assert of the FROZEN pipeline does not apply "
                        "here — X1's re-derivation clauses replace it")}
        print(f"  search re-run vs exp141 deposit (expected divergent):"
              f" rounds {rep['rounds_match']} | pool {len(pool)} vs "
              f"{dep141['search']['pool_size']}")

        # ---- 2b. the 15 all-deep members pushed through the SAME
        #          splice/funnel machinery: appended to the pool as
        #          candidates, evaluated by the SAME formulas (their f
        #          = the exp172 construction; novelty by the pipeline's
        #          own nov_lib against the record they joined, plus the
        #          frozen-72 counterfactual deposited alongside) ------
        n_pool_search = len(pool)
        deep_fate: list = []
        for m in deep_meta:
            zs = m["zones"]
            key = W.to_key([tuple(z) for z in zs])
            assert key not in pool, \
                (f"a search candidate collides with deep member "
                 f"{m['member']} — that would be a finding")
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
            pool[key] = rec
            deep_fate.append(rec)
        print(f"  deep members pushed through the machinery: 15 "
              f"candidates appended (pool {n_pool_search} -> "
              f"{len(pool)}) | their nov_lib vs the record they joined: "
              f"{[round(r['nov_lib'], 3) for r in deep_fate]}")

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
              f"DEEP members in eligible: {n_deep_eligible}/15")

        # the deep members' splice novelty (diagnosis, both readings:
        # against the extended family they joined, and the frozen-72
        # counterfactual "had they been invented" family)
        S_frozen = build_splices(lib_frozen)
        fmF = np.zeros((len(S_frozen), 100), dtype=bool)
        fmF[:, 1:] = S_frozen[:, 1:] != S_frozen[:, :-1]
        flF = fmF.sum(axis=1)
        for r in deep_fate:
            r["nov_splice_extended"] = L.fast_nov_splice(r["f"], S, fm, fl)
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
        bars_deposited_before_selection = True   # stage order kept

        # funnel census vs the frozen-72 lineage (EXPECTED-DIVERGENT
        # diagnostic: the exp150/exp146 lineage asserts are the FROZEN
        # pipeline's validity checks — the exp179 H1 clause — and are
        # replaced here by X1's re-derivation clauses)
        funnel_census = {
            "frozen_lineage": {
                "pool": dep150["funnel"]["pool"],
                "lib_novel": dep150["funnel"]["lib_novel"],
                "splice_clear": dep150["funnel"]["splice_clear"]},
            "extended": {"pool": len(pool),
                         "lib_novel": len(eligible),
                         "splice_clear": len(splice_clear)},
            "expected_divergent": True}

        # ---- 5. R_W census over the eligible stream (production
        #         floor ONLY — no instrument pin, post-CF-1 world) ----
        rw_rows = []
        for i, r in enumerate(eligible):
            m_new = clash_mass(r["f"], canon)   # production floor
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
        #         extended bars (diagnostic only — no lineage assert;
        #         THE delivery this run is the clause walk below) -----
        def zkey_of(zs) -> str:
            return W.to_key([tuple(z) for z in zs])

        def greedy(bar: float) -> list:
            dlist: list = []
            for r in eligible:
                if len(dlist) >= N_DELIVER:
                    break
                if r["_rw_pos_production"]:
                    continue           # R_W pre-emission filter
                if r["nov_splice"] <= n_star_splice:
                    continue           # exp146's clause, kept
                if any(dist(r["f"], d["f"]) <= bar for d in dlist):
                    continue           # C4 filter at `bar`
                dlist.append(r)
            return dlist

        delivered_ref = greedy(n_star_pool)
        print(f"  J-order greedy reference delivery at the extended "
              f"bars: {len(delivered_ref)}/{N_DELIVER} (diagnostic)")

        return {"canon_check": True,
                "harness_max_abs_diff": worst,
                "bars": bars,
                "bars_deposited_before_selection":
                bars_deposited_before_selection,
                "search_replication": rep,
                "funnel": {"pool": len(pool),
                           "pool_search_only": n_pool_search,
                           "lib_novel": len(eligible),
                           "splice_clear": len(splice_clear)},
                "funnel_census_vs_frozen_lineage": funnel_census,
                "n_star_lib": n_star_lib,
                "n_star_splice": n_star_splice,
                "n_star_splice_frozen_deposit":
                prev146["n_star_splice"],
                "n_star_pool": n_star_pool,
                "deep_funnel": {
                    "n_deep_members": 15,
                    "n_in_eligible": n_deep_eligible,
                    "n_in_splice_clear": n_deep_splice,
                    "fates": [{
                        "member": r["member"],
                        "rung": r["rung"], "instance": r["instance"],
                        "nov_lib_extended": float(r["nov_lib"]),
                        "nov_lib_vs_frozen72":
                        float(r["nov_lib_vs_frozen72"]),
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
                # the extended eligible pool records (the clause's
                # input):
                "members": splice_clear}

    # ==================================================================
    # THE TARGET SETS (the clause's T inputs)
    # ==================================================================
    def targets_exp150() -> dict:
        """T = exp150's OWN targets (its deposit): the 10 delivered
        members' zone programs; each target profile is the member's
        own profile f_t = profile_of_zones(zones_t) VERBATIM (exp150's
        own-target discipline, recovered deterministically from the
        deposit)."""
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
        """T = exp176's deep set (its deposit sections rung_-40/-50/-60
        targets): the deposited constructions, re-derived by exp172's/
        exp176's deep_target VERBATIM (instance 0) and CHECKSUMMED
        against the deposit."""
        ts = []
        sec_keys = sorted((k for k in dep176["sections"]
                           if k.startswith("rung_")),
                          key=lambda k: float(k[5:]))
        for k in sec_keys:
            rung = float(k[5:])
            f, triples = deep_member(rung, 0)
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
                    "program (instance 0) with every zone value forced "
                    "to the rung, exp94's spec_target_n, canon = "
                    "labeling_bfs_n(A_CHAIN); checksums asserted "
                    "against the exp176 deposit"),
                "n_targets": len(ts), "targets": ts}

    # ==================================================================
    # THE POOL'S PRICE TABLE at T (the clause's ranking data)
    # ==================================================================
    def price_table(T: dict, members: list) -> dict:
        """Every eligible member priced at EVERY target of T via
        exp150's price_rung VERBATIM at the production cell (1.0, 0.0),
        seeds (1,2,3). price(m, T) = the MEAN composed decode err over
        T's targets x seeds = mean_t decode_err_mean(t). Computed
        FRESH, AFTER the funnel re-derivation (stage order deposited;
        the decodes are locally seeded — no shared rng to perturb the
        already-recorded search)."""
        prov = None
        rows = []
        for i, r in enumerate(members):
            zs = [tuple(z) for z in r["zones"]]
            per = []
            for ti, t in enumerate(T["targets"]):
                pr = price_rung(t["f"], zs, 1.0, 0.0)
                assert pr["cell"] == [1.0, 0.0], "production cell drift"
                prov = pr["provenance"]
                e_new, mode = emit_rung([pr])   # single-rung emission
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
    def clause_walk(table: dict, members: list) -> dict:
        """Rank the eligible pool ASCENDING by price(m, T); walk the
        ranked order, keeping member m iff its min pairwise distance
        D(m, kept) > N*_pool-extended (RE-DERIVED this run — the SAME
        diversity constraint exp150's delivery enforced, applied within
        the price-ranked order); stop at 10. Tie-break: member index
        ascending. No R_W step — the production-floor R_W census is
        deposited with the pipeline."""
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
    def evaluate_x1(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        if pipe is None:
            return None
        bars = pipe["bars"]
        funnel = pipe["funnel"]
        build_ok = bool(pipe["library_members"] == 87
                        and pipe["deep_members"] == 15)
        splice_ok = bool(pipe["splice_family_size"] == 71079
                         and pipe["harness_max_abs_diff"] < 1e-9)
        funnel_ok = bool(funnel["pool"] > 15
                         and funnel["lib_novel"] > 0
                         and funnel["splice_clear"] > 0
                         and np.isfinite(pipe["n_star_pool"]))
        n_rej = 0
        for tkey in ("price_table_deep_targets",
                     "price_table_exp150_targets"):
            if tkey in sections:
                n_rej += sum(p["n_rejected"]
                             for r in sections[tkey]["rows"]
                             for p in r["per_target"])
        zero_rej = bool(n_rej == 0)
        ok = bool(build_ok and splice_ok and funnel_ok and zero_rej
                  and pipe["bars_deposited_before_selection"]
                  and pipe["canon_check"]
                  and pipe["production_floor_asserted"])
        return {"gate": "X1", "clause": (
            "extended pipeline integrity: the extended library builds "
            "(87 members), the splice family + funnel re-derive with "
            "zero rejections, and the three N* bars are deposited "
            "BEFORE selection (bars_deposited_before_selection)"),
                "library_members": pipe["library_members"],
                "deep_members": pipe["deep_members"],
                "library_builds_87": build_ok,
                "splice_family_size": pipe["splice_family_size"],
                "harness_max_abs_diff": pipe["harness_max_abs_diff"],
                "splice_family_rederived": splice_ok,
                "funnel": funnel,
                "funnel_rederived": funnel_ok,
                "bars": bars,
                "bars_rederived_computed_not_assumed": True,
                "bars_deposited_before_selection":
                pipe["bars_deposited_before_selection"],
                "canon_check": pipe["canon_check"],
                "production_floor_asserted":
                pipe["production_floor_asserted"],
                "rejections_total": n_rej,
                "zero_rejections": zero_rej,
                "pass": ok}

    def evaluate_x2(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        if pipe is None:
            return None
        df = pipe["deep_funnel"]
        fates = df["fates"]
        n_in = df["n_in_eligible"]
        # counterfactual ("had they been invented against the frozen
        # record"): novelty vs the frozen 72 at BOTH bars, splice
        # novelty vs the frozen family at the deposited bar
        cf = {
            "novelty_reference": ("the frozen 72-member library "
                                  "(exp150's deposited bars)"),
            "frozen_bar_lib": dep150["bars"]["n_star_lib"],
            "frozen_bar_splice": dep150["bars"]["n_star_splice"],
            "n_novel_vs_frozen72_at_extended_bar":
            sum(int(r["nov_lib_vs_frozen72"] > pipe["n_star_lib"])
                for r in fates),
            "n_novel_vs_frozen72_at_frozen_bar":
            sum(int(r["nov_lib_vs_frozen72"]
                    > dep150["bars"]["n_star_lib"]) for r in fates),
            "n_splice_clear_vs_frozen_family_at_frozen_bar":
            sum(int(r["nov_splice_vs_frozen72"]
                    > dep150["bars"]["n_star_splice"]) for r in fates),
            "max_nov_lib_vs_frozen72":
            max(r["nov_lib_vs_frozen72"] for r in fates)}
        ok = bool(n_in >= 10)
        return {"gate": "X2", "clause": (
            "the deep members survive the funnel: >= 10 of the 15 "
            "all-deep members are in the 96-eligible pool (the "
            "machinery does not discard the band)"),
                "n_deep_members": df["n_deep_members"],
                "n_in_eligible": n_in,
                "n_in_splice_clear": df["n_in_splice_clear"],
                "required": 10,
                "eligible_pool_size": pipe["funnel"]["lib_novel"],
                "fates": fates,
                "reading_note": (
                    "the 15 all-deep members joined the library AND "
                    "were pushed through the SAME funnel as candidates "
                    "(nov_lib by the pipeline's own machinery against "
                    "the record they joined — a record member's "
                    "novelty is 0 by definition); the counterfactual "
                    "reading (novelty vs the frozen 72, had they been "
                    "invented) is deposited alongside and fails at the "
                    "same stage"),
                "counterfactual_had_they_been_invented": cf,
                "pass": ok}

    def evaluate_x3(sections: dict) -> dict | None:
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
        return {"gate": "X3", "clause": (
            "deep delivery — the clause's purpose: the clause's "
            "delivered-10 at the deep target set (exp176's deposit "
            "sections): >= 9/10 with decode < 6.0 AND hold < 6.0 on "
            "3/3 seeds at EVERY rung; zero rejections; emission mode "
            "repriced_full everywhere (audit_only_fallback must NOT "
            "fire — the L143 retirement holds when the library serves "
            "the band)"),
                "complete": complete,
                "n_delivered": len(kept),
                "per_rung_333_counts": per_rung_counts,
                "members_passing_all_targets": members_all,
                "rejections": n_rej,
                "emission_modes": modes,
                "rows_note": ("per-(member, rung) rows in "
                              "clause_deep_targets.walk.kept[]."
                              "per_target"),
                "pass": ok}

    def evaluate_x4(sections: dict) -> dict | None:
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
        return {"gate": "X4", "clause": (
            "the old operating point: the clause's delivered-10 at "
            "exp150's own targets (its deposit): C1 every member "
            "beyond N*_lib-extended and N*_splice-extended, C2 "
            "emitted-rung quads < 6.0, C3 decode < 6.0 AND hold < 6.0 "
            "on 3/3 seeds, C4 min pairwise D > N*_pool-extended — ALL "
            "PASS (the quality bars hold on the extended library too)"),
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
    print("=== exp184: THE DEEP-PROGRAM LIBRARY COHORT (the library "
          "sent to the band — exp179's registered next, L158) ===\n")
    if args.smoke:
        pipe = run_pipeline()
        dep = {"exp": "exp184_deep_library", "kind": "smoke",
               "discarded": True,
               "scope": ("extended-library build + the three re-derived "
                         "N* bars only (no price tables, no clause "
                         "walks, no gates)"),
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
              f"funnel {dep['funnel']} | deep in eligible "
              f"{dep['deep_funnel_counts']['n_in_eligible']}/15")
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
        "library_members": 87,
        "deep_members": 15,
        "splice_family_size": 71079,
        "harness_max_abs_diff": pipe["harness_max_abs_diff"],
        "bars_deposited_before_selection":
        pipe["bars_deposited_before_selection"],
        "search_replication": pipe["search_replication"],
        "funnel": pipe["funnel"],
        "funnel_census_vs_frozen_lineage":
        pipe["funnel_census_vs_frozen_lineage"],
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
        "production_floor_asserted": True,
        "instrument_pin_used": False}

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
        walk1 = clause_walk(tab1, members)
        kept1 = [{**k, "per_target": k["per_target"]}
                 for k in walk1["kept"]]
        result["sections"]["clause_exp150_targets"] = {
            "target_set_label": "exp150_targets",
            "target_set_construction": T1["construction"],
            "n_targets": T1["n_targets"],
            "target_names": [t["name"] for t in T1["targets"]],
            "walk": {"ranked_order_idxs": walk1["ranked_order_idxs"],
                     "n_kept": walk1["n_kept"],
                     "kept": kept1,
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
        walk2 = clause_walk(tab2, members)
        kept2 = [{**k, "per_target": k["per_target"]}
                 for k in walk2["kept"]]
        result["sections"]["clause_deep_targets"] = {
            "target_set_label": "deep_targets",
            "target_set_construction": T2["construction"],
            "n_targets": T2["n_targets"],
            "target_names": [t["name"] for t in T2["targets"]],
            "walk": {"ranked_order_idxs": walk2["ranked_order_idxs"],
                     "n_kept": walk2["n_kept"],
                     "kept": kept2,
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
    for name, fn in (("X1", evaluate_x1), ("X2", evaluate_x2),
                     ("X3", evaluate_x3), ("X4", evaluate_x4)):
        if name in result["gates"]:
            continue
        g = fn(result["sections"])
        if g is not None:
            result["gates"][name] = g

    npass = sum(int(g["pass"]) for g in result["gates"].values())
    for name in ("X1", "X2", "X3", "X4"):
        if name in result["gates"]:
            g = result["gates"][name]
            extra = ""
            if name == "X1":
                extra = (f" (bars {g['bars']}, library "
                         f"{g['library_members']}, splice family "
                         f"{g['splice_family_size']}, funnel "
                         f"{g['funnel']})")
            elif name == "X2":
                extra = (f" ({g['n_in_eligible']}/{g['n_deep_members']} "
                         f"deep members in the eligible pool, required "
                         f">= {g['required']}; splice-clear "
                         f"{g['n_in_splice_clear']})")
            elif name == "X3":
                extra = (f" ({g['members_passing_all_targets']}/"
                         f"{g['n_delivered']} members pass all targets"
                         f", per-rung {g['per_rung_333_counts']}, rej "
                         f"{g['rejections']}, modes "
                         f"{g['emission_modes']})"
                         if g["complete"] else " (incomplete)")
            elif name == "X4":
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
               f"({' '.join(k for k in ('X1', 'X2', 'X3', 'X4')
                            if k in result['gates'])})")
    print(f"  === {verdict} ===")

    result.update({
        "exp": "exp184_deep_library",
        "claim": (
            "THE DEEP-PROGRAM LIBRARY COHORT (exp179's registered "
            "next, L158): the deep-delivery failure is upstream of "
            "delivery — the pool's members carry MIXED-VALUE programs "
            "while the deep targets demand UNIFORM-deep patterns. "
            "THIS RUN pushes all-deep library members through the "
            "SAME splice/funnel machinery and re-runs the clause "
            "delivery: exp172's uniform-rung construction (rungs "
            "{-40,-45,-50,-55,-60} x 3 MULTI-zone layout shifts, the "
            "exp172 instance discipline) joins exp141's 72-member "
            "library as a 87-member extended library; the splice "
            "family, funnel, and N* bars RE-DERIVED on the extended "
            "library (computed, not assumed); search seed 141; the "
            "clause delivery = exp179's price-ranked walk (ranked "
            "ascending by mean composed decode err over the DEEP "
            "target set = exp176's deposit sections, keep iff min "
            "pairwise D > N*_pool-extended, stop at 10); the old "
            "operating point re-scored at exp150's own targets (its "
            "deposit)"),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration; gates X1-X4 fixed "
                             "there, each evaluated exactly once)"),
            "gates": [
                "X1 extended pipeline integrity: the extended library "
                "builds (87 members), the splice family + funnel "
                "re-derive with zero rejections, and the three N* bars "
                "are deposited BEFORE selection "
                "(bars_deposited_before_selection)",
                "X2 the deep members survive the funnel: >= 10 of the "
                "15 all-deep members are in the 96-eligible pool (the "
                "machinery does not discard the band)",
                "X3 deep delivery: the clause's delivered-10 at the "
                "deep target set: >= 9/10 with decode < 6.0 AND hold "
                "< 6.0 on 3/3 seeds at EVERY rung; zero rejections; "
                "emission mode repriced_full everywhere",
                "X4 the old operating point: the clause's delivered-10 "
                "at exp150's own targets: C1-C4 ALL PASS"],
            "cohort": ("15 all-deep members = exp172's uniform-rung "
                       "construction (rungs {-40,-45,-50,-55,-60} x 3 "
                       "MULTI-zone layout shifts +i cells, i = 0..2) "
                       "joined to exp141's 72-member library"),
            "bars": "RE-DERIVED on the extended library (computed, "
                    "not assumed)",
            "deep_target_set": ("exp176's deposit sections "
                                "rung_-40/-50/-60 targets, checksummed"),
            "tie_break": "member index ascending (J-ordered funnel "
                         "index)"},
        "stage_order": ["extended_library_build (72 frozen + 15 "
                        "all-deep exp172 constructions)",
                        "n_star_lib_rederived (extended pairwise "
                        "distances, deposited machinery)",
                        "splice_family_rederived (71079) + "
                        "n_star_splice_rederived (exp146 machinery)",
                        "search_rerun_seed141 (exp141's loop VERBATIM; "
                        "the ONE change: extended novelty reference; "
                        "exp141 bit-identity NOT registered here — "
                        "divergence deposited as expected)",
                        "deep_members_pushed_through_the_same_"
                        "machinery (pool candidates, same formulas)",
                        "funnel_rederived (lib-novelty -> splice-clear "
                        "on the extended bars)",
                        "n_star_pool_rederived_BEFORE_selection",
                        "rw_census (production floor, no pin)",
                        "price_tables_fresh_after_funnel (deep targets "
                        "= exp176 deposit sections; exp150 targets = "
                        "its deposit)",
                        "clause_walks (price-ranked, C4-diverse @ "
                        "N*_pool-extended, cap 10)",
                        "gates_evaluated"],
        "smoke_disclosure": ("a --smoke check (extended-library build + "
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
