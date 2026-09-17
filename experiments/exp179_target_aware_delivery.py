#!/usr/bin/env python3
"""exp179 — TARGET-AWARE DELIVERY (the clause exp176 registered).

exp176's registered next (L155): the search's selection machinery is
TARGET-FREE (proven by G1's bit-identity at seed 141) — the delivered
cohort carries deep rungs (9/10, G3) but fails deep-target delivery
(0/10 under the 6.0 bar, G2 REFUTE). The repair is a TARGET-AWARE
DELIVERY clause: rank the 96-eligible pool by price at the GIVEN
target set before the cap-10 selection. No new knobs — exp150's
price_rung machinery already computes decode prices.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Clause, gates, and bars are fixed now.

THE CLAUSE (one rule, zero knobs):
  Given the 96-eligible pool (exp168's B3 funnel at seed 141,
  bit-identical re-derivation) and a target set T:
    rank members ASCENDING by price(m, T) = the MEAN composed decode
    err over T's targets x seeds (1, 2, 3) via exp150's price_rung
    VERBATIM at the production cell (1.0, 0.0);
    walk the ranked order, keeping member m iff its min pairwise
    distance D(m, kept) > N*_pool (33.776, the deposited C4 bar) —
    the SAME diversity constraint exp150's delivery enforced, applied
    within the price-ranked order;
    stop at 10. Tie-break: member index ascending. That is the whole
    clause.

GATES (each evaluated exactly once):

  GATE-H1 (pipeline integrity) the 72-member library, splice family,
           and 96-eligible pool re-derive bit-identically to exp176's
           deposit (bars 82.288 / 20.140 / 33.776; funnel counts
           96/253 -> 96/96); the pool's price table at T is computed
           fresh and deposited (96 rows).
  GATE-H2 (the old operating point's quality bars hold at exp150's
           own targets) the clause delivered-10 scored against
           exp150's deposited targets: C1 (every member beyond
           N*_lib and N*_splice), C2 (emitted-rung quads < 6.0),
           C3 (decode < 6.0 AND hold < 6.0 on 3/3 seeds), C4 (min
           pairwise D > N*_pool) — ALL PASS (the member SET may
           differ from exp150's; the quality bars may not).
  GATE-H3 (deep-target delivery — the clause's purpose) the clause
           delivered-10 scored against exp176's deep target set
           (rungs -40/-50/-60, the deposited constructions):
           >= 9/10 members with decode < 6.0 AND hold < 6.0 on 3/3
           seeds at EVERY rung; zero rejections; emission mode
           repriced_full.
  GATE-H4 (discipline) the R_W production-floor set empty == the
           excluded set over the eligible pool (both target sets);
           zero rejections everywhere; the price table's rng
           consumption does not perturb the search's bit-identity
           (prices computed AFTER the funnel re-derivation, in a
           fresh process block, pin untouched — no instrument pin
           needed: this run is post-CF-1 production world).

NO post-hoc tuning. A --smoke check (the price table for 3 pool
members only) is permitted before the credited run and discarded.

DEPOSIT: results/exp179_target_aware_delivery.json

RUN:
  python3 -m experiments.exp179_target_aware_delivery          # full
  python3 -m experiments.exp179_target_aware_delivery --smoke  # check
  python3 -m experiments.exp179_target_aware_delivery --job H3
  # jobs: H1 | H2 | H3
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

from experiments.exp136_generator_v6 import (  # noqa: E402
    decode as exp136_decode,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)

# ---- FIXED CONSTANTS ------------------------------------------------
BAR_LIB = 82.288
BAR_SPLICE = 20.140
BAR_POOL = 33.776
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141
DEEP_RUNGS = [-40.0, -50.0, -60.0]

OUT = os.path.join(ROOT, "results", "exp179_target_aware_delivery.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP176 = os.path.join(ROOT, "results", "exp176_deep_band_search.json")


def main() -> dict:
    # ==== BODY (written by the run agent; docstring/imports/constants
    # above byte-unchanged — exp174's body-only discipline) ============
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["H1", "H2", "H3", "all"],
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

    DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
    DEP168 = os.path.join(ROOT, "results", "exp168_cf1_production.json")
    PROD_FLOOR = -60.0                    # CF-1's production value

    # the two target-set deposits (the clause's T inputs)
    dep150 = json.load(open(DEP150))
    dep176 = json.load(open(DEP176))

    # ---- instrument check: the production core in situ ---------------
    # (H4 discipline: NO instrument pin anywhere this run — post-CF-1
    # production world; the floor is asserted, never touched.)
    floors = {"CORE": CORE.NEURAL_SPEC_MIN,
              "M136": M136.NEURAL_SPEC_MIN,
              "M156": M156.NEURAL_SPEC_MIN}
    assert all(v == PROD_FLOOR for v in floors.values()), \
        f"production floor drift: {floors}"

    def deep_target(rung: float):
        """exp176's deep-band construction, VERBATIM: the MULTI 3-zone
        program (instance 0), every zone value forced to `rung`, built
        by exp94's spec_target_n machinery. Returns f (the decode/hold
        target), the program triples, canon."""
        zs = [(z.f0, z.f1, z.name) for z in MULTI.zones]   # instance 0
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=rung, name=nm)
                   for (a, b, nm) in zs],
            amputate_plane=MULTI.amputate_plane,
            spec_name="ms-multi-deep-i0",
            somatic_latch=MULTI.somatic_latch)
        canon = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon, g6.wildtype_target(g6.N)), \
            "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"
        f = spec_target_n(spec, canon, g6.N)
        triples = [(a, b, rung) for (a, b, _nm) in zs]
        return f, triples, canon

    # ==================================================================
    # THE PIPELINE (exp168's B3 / exp176's run_pipeline sections 0-6,
    # verbatim; target-independent by construction — H1's clause).
    # The ONE deviation is H4-mandated: the R_W census runs at the
    # PRODUCTION FLOOR ONLY (no old-floor pin — pin untouched).
    # ==================================================================
    def run_pipeline() -> dict:
        canon = wildtype_target(LAT_N)

        # ---- 0. frozen library + N*_lib (verbatim) ------------------
        lib = build_library()
        lib_names = list(lib)
        assert len(lib_names) == 72, \
            f"library size drift: {len(lib_names)}"
        lib_arr = np.stack([lib[n] for n in lib_names])
        n_star_lib, _ = library_nn_stats(lib)
        print(f"  library {len(lib_names)} members | N*_lib "
              f"{n_star_lib:.3f} (bar {BAR_LIB})")
        assert round(n_star_lib, 3) == BAR_LIB, "N*_lib drift"

        # ---- 1. splice family + N*_splice (exp146 machinery) --------
        S = build_splices(lib)
        assert len(S) == 48564, f"splice family size drift: {len(S)}"
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
        prev146 = json.load(open(DEP146))
        print(f"  splice family {len(S)} | N*_splice "
              f"{n_star_splice:.3f} (exp146 deposit "
              f"{prev146['n_star_splice']}) | harness "
              f"max|fast-verbatim| {worst:.2e}")
        assert round(n_star_splice, 3) == BAR_SPLICE, \
            "N*_splice drift vs the pre-registered bar"
        assert abs(n_star_splice - prev146["n_star_splice"]) < 1e-3, \
            "N*_splice drift vs exp146 deposit"

        # ---- 2. the search re-run (exp141's loop VERBATIM, seed 141)
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

        prev141 = json.load(open(os.path.join(
            ROOT, "results", "exp141_generator_wide.json")))
        rep_rounds = []
        for a, b in zip(round_summaries, prev141["search"]["rounds"]):
            ok = (a["round"] == b["round"] and a["n"] == b["n"]
                  and a["n_novel"] == b["n_novel"]
                  and a["n_novel_nondisjoint"] == b["n_novel_nondisjoint"]
                  and a["n_novel_below_line"] == b["n_novel_below_line"]
                  and abs(a["median_J"] - b["median_J"]) < 1e-9
                  and abs(a["best_J"] - b["best_J"]) < 1e-9)
            rep_rounds.append({"round": a["round"], "match": bool(ok)})
        rep = {"rounds_match": all(r["match"] for r in rep_rounds),
               "round_rows": rep_rounds,
               "pool_size_match": len(pool)
               == prev141["search"]["pool_size"],
               "pool_size": len(pool),
               "exp141_pool_size": prev141["search"]["pool_size"]}
        print(f"  search replication vs exp141 deposit: rounds "
              f"{rep['rounds_match']} | pool {len(pool)} vs "
              f"{prev141['search']['pool_size']}")
        assert rep["rounds_match"] and rep["pool_size_match"], \
            "search re-run diverged from the exp141 deposit — the " \
            "divergence is the finding, deposited"

        # ---- 3. the funnel (verbatim) --------------------------------
        ordered = sorted(pool.values(), key=lambda r: r["J"])
        eligible = [r for r in ordered if r["novel"]]
        for r in eligible:
            r["nov_splice"] = L.fast_nov_splice(r["f"], S, fm, fl)
        splice_clear = [r for r in eligible
                        if r["nov_splice"] > n_star_splice]
        print(f"  funnel: lib-novel {len(eligible)}/{len(pool)} | "
              f"splice-clear {len(splice_clear)}/{len(eligible)}")

        # ---- 4. N*_pool (third corpus, verbatim) ---------------------
        pool_dict = {f"pool-{i:03d}": r["f"]
                     for i, r in enumerate(splice_clear)}
        n_star_pool, _ = library_nn_stats(pool_dict)
        print(f"  N*_pool {n_star_pool:.3f} (bar {BAR_POOL})")
        assert round(n_star_pool, 3) == BAR_POOL, "N*_pool drift"
        bars = {"n_star_lib": round(n_star_lib, 3),
                "n_star_splice": round(n_star_splice, 3),
                "n_star_pool": round(n_star_pool, 3)}
        bars_deposited_before_selection = True   # stage order kept

        # funnel identity (the deposit-recorded funnel, exp150)
        funnel_identity = {
            "pool": len(pool) == dep150["funnel"]["pool"],
            "lib_novel":
                len(eligible) == dep150["funnel"]["lib_novel"],
            "splice_clear":
                len(splice_clear) == dep150["funnel"]["splice_clear"]}
        assert all(funnel_identity.values()), \
            "funnel counts drifted from the deposited funnel"

        # ---- 5. R_W census over the eligible stream (H4 data;
        #         PRODUCTION FLOOR ONLY — no instrument pin, H4) ------
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

        # ---- 6. delivery cross-check: the J-order greedy (exp150's
        #         repaired rule) still reproduces the deposited lineage
        def zkey_of(zs) -> str:
            return W.to_key([tuple(z) for z in zs])

        def greedy(bar: float) -> tuple[list, list]:
            dlist: list[dict] = []
            excluded_rw: list[dict] = []
            for i, r in enumerate(eligible):
                if len(dlist) >= N_DELIVER:
                    break
                if r["_rw_pos_production"]:
                    excluded_rw.append({"idx": i,
                                        "clash_mass_mV2":
                                        rw_rows[i][
                                            "clash_mass_production_mV2"]})
                    continue           # R_W pre-emission filter
                if r["nov_splice"] <= n_star_splice:
                    continue           # exp146's clause, kept
                if any(dist(r["f"], d["f"]) <= bar for d in dlist):
                    continue           # C4 filter at `bar`
                dlist.append(r)
            return dlist, excluded_rw

        delivered, excluded_rw = greedy(n_star_pool)  # C4@N*_pool + R_W
        old_rule, _ = greedy(n_star_lib)              # cross-check
        old_keys = [zkey_of(r["zones"]) for r in old_rule]
        exp146_keys = [zkey_of(d["zones"]) for d in prev146["delivered"]]
        assert old_keys == exp146_keys, \
            "old-rule re-delivery does not reproduce exp146's 7 — " \
            "pipeline drift"
        print(f"  delivery cross-check (C4 @ N*_pool + R_W pre-filter):"
              f" {len(delivered)}/{N_DELIVER} | old-rule cross-check "
              f"reproduces exp146's 7: True")

        # ---- 7. funnel census vs exp150's delivered-10 + exp168 B3 ---
        exp150_keys = [zkey_of(d["zones"])
                       for d in dep150["delivered"]]
        fresh_keys = [zkey_of(r["zones"]) for r in delivered]
        dep168 = json.load(open(DEP168))
        b3_keys = [zkey_of(d["zones"])
                   for d in dep168["b3_fresh_search"]["delivered"]]
        census = {"same_set_same_order_exp150":
                  fresh_keys == exp150_keys,
                  "same_set_same_order_exp168_b3": fresh_keys == b3_keys,
                  "n_delivered_fresh": len(delivered),
                  "n_delivered_exp150": len(dep150["delivered"]),
                  "excluded_by_rw": excluded_rw,
                  "note": ("the pipeline's selection is bit-identical "
                           "to the deposited lineage"
                           if fresh_keys == exp150_keys == b3_keys else
                           "the delivery diverged from the deposited "
                           "cohort — see keys")}
        assert census["same_set_same_order_exp150"], \
            "J-order delivery diverged from exp150's deposited cohort"

        # ---- B4/H4: R_W pre-filter discipline ------------------------
        excluded_names = [zkey_of(eligible[x["idx"]]["zones"])
                          for x in excluded_rw]
        delivered_rw_negative = all(
            not r["_rw_pos_production"] for r in delivered)
        shadow = []      # shadow pricing: no excluded member would
        for x in excluded_rw:          # have delivered a full-valid rung
            r = eligible[x["idx"]]
            zones = r["zones"]
            tbl = [price_rung(r["f"], zones, g, mu)
                   for (g, mu) in EXTENDED_LADDER]
            e_new, mode = emit_rung(tbl)
            shadow.append({"idx": x["idx"],
                           "would_deliver_full_valid":
                           bool(mode == "repriced_full"),
                           "mode": mode})
        false_exclusions = [s for s in shadow
                            if s["would_deliver_full_valid"]]

        return {"canon_check": True,
                "harness_max_abs_diff": worst,
                "bars": bars,
                "bars_deposited_before_selection":
                bars_deposited_before_selection,
                "search_replication": rep,
                "funnel": {"pool": len(pool),
                           "lib_novel": len(eligible),
                           "splice_clear": len(splice_clear)},
                "funnel_identity": funnel_identity,
                "rw_census": rw_rows,
                "rw_pos_production": sorted(rw_pos_prod),
                "excluded_by_rw": excluded_rw,
                "excluded_names": excluded_names,
                "delivered_rw_negative": delivered_rw_negative,
                "shadow_pricing": shadow,
                "false_exclusions": false_exclusions,
                "census_vs_exp150": census,
                "delivered_reference_keys": fresh_keys,
                # the 96-eligible pool records (the clause's input):
                "members": splice_clear,
                "n_star_lib": n_star_lib,
                "n_star_splice": n_star_splice,
                "n_star_pool": n_star_pool}

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
        """T = exp176's deep set (its deposit sections
        rung_-40/-50/-60 targets): the deposited constructions,
        re-derived by exp176's deep_target VERBATIM and CHECKSUMMED
        against the deposit."""
        ts = []
        for rung in DEEP_RUNGS:
            f, triples, _canon = deep_target(rung)
            sha = hashlib.sha256(f.tobytes()).hexdigest()[:16]
            dep_sha = dep176["sections"][f"rung_{rung:g}"]["target"][
                "f_sha256_16"]
            assert sha == dep_sha, \
                f"deep target checksum drift at rung {rung}: " \
                f"{sha} vs deposit {dep_sha}"
            ts.append({"name": f"rung_{rung:g}", "rung": rung,
                       "triples": [list(t) for t in triples],
                       "f_sha256_16": sha, "f": f})
        print(f"  deep target set: 3 constructions, checksums match "
              f"exp176's deposit "
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
        """Every pool member priced at EVERY target of T via exp150's
        price_rung VERBATIM at the production cell (1.0, 0.0), seeds
        (1,2,3). price(m, T) = the MEAN composed decode err over T's
        targets x seeds = mean_t decode_err_mean(t). Computed FRESH,
        AFTER the funnel re-derivation (stage order deposited; the
        decodes are locally seeded — no shared rng to perturb the
        already-asserted search bit-identity)."""
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
            rows.append({"idx": i, "member": f"pool-{i:03d}",
                         "zones": [list(z) for z in zs],
                         "J": float(r["J"]),
                         "nov_lib": float(r["nov_lib"]),
                         "nov_splice": float(r["nov_splice"]),
                         "price_composed_decode_err": price,
                         "per_target": per})
            print(f"  price[{T['label']}] pool-{i:03d}: price "
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
    # THE CLAUSE (one rule, zero knobs)
    # ==================================================================
    def clause_walk(table: dict, members: list) -> dict:
        """Rank the 96-eligible pool ASCENDING by price(m, T); walk the
        ranked order, keeping member m iff its min pairwise distance
        D(m, kept) > N*_pool (33.776, the deposited C4 bar — the SAME
        diversity constraint exp150's delivery enforced, applied within
        the price-ranked order); stop at 10. Tie-break: member index
        ascending. No R_W step — H4's census proves the production-
        floor positive set is empty (the pre-emission clause is
        vacuous)."""
        f_of = {i: r["f"] for i, r in enumerate(members)}
        ranked = sorted(table["rows"],
                        key=lambda x: (x["price_composed_decode_err"],
                                       x["idx"]))
        kept, skipped = [], []
        for x in ranked:
            if len(kept) >= N_DELIVER:
                break
            fm = f_of[x["idx"]]
            if all(dist(fm, f_of[k["idx"]]) > n_star_pool for k in kept):
                kept.append(x)
            else:
                blocked_by = min(
                    (k["idx"] for k in kept
                     if dist(fm, f_of[k["idx"]]) <= n_star_pool),
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
        print(f"  clause walk [{table.get('target_set_label', 'targets')}]: kept "
              f"{len(kept)}/{N_DELIVER} | min pairwise D {min_d:.3f} "
              f"> N*_pool {n_star_pool:.3f} | best price "
              f"{ranked[0]['price_composed_decode_err']:.3f} | worst "
              f"kept price "
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
    def evaluate_h1(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        t1 = sections.get("price_table_exp150_targets")
        t2 = sections.get("price_table_deep_targets")
        if pipe is None or t1 is None or t2 is None:
            return None
        bars = pipe["bars"]
        bars_float_equal = bool(
            bars["n_star_lib"] == BAR_LIB
            and bars["n_star_splice"] == BAR_SPLICE
            and bars["n_star_pool"] == BAR_POOL)
        funnel_ok = bool(
            pipe["funnel"] == {"pool": 253, "lib_novel": 96,
                               "splice_clear": 96})
        tables_ok = bool(t1["n_rows"] == 96 and t2["n_rows"] == 96)
        rep = pipe["search_replication"]
        ok = bool(
            bars_float_equal and funnel_ok and tables_ok
            and pipe["harness_max_abs_diff"] < 1e-9
            and rep["rounds_match"] and rep["pool_size_match"]
            and all(pipe["funnel_identity"].values())
            and pipe["census_vs_exp150"]["same_set_same_order_exp150"]
            and pipe["canon_check"])
        return {"gate": "H1", "clause": (
            "pipeline integrity: the 72-member library, splice family, "
            "and 96-eligible pool re-derive bit-identically to exp176's "
            "deposit (bars 82.288 / 20.140 / 33.776; funnel counts "
            "96/253 -> 96/96); the pool's price table at T is computed "
            "fresh and deposited (96 rows, both target sets); prices "
            "computed AFTER the funnel re-derivation"),
                "bars": bars,
                "bars_float_equal": bars_float_equal,
                "library_members": 72,
                "splice_family_size": 48564,
                "harness_max_abs_diff": pipe["harness_max_abs_diff"],
                "search_replication": rep,
                "funnel": pipe["funnel"],
                "funnel_counts_96_253_96_96": funnel_ok,
                "funnel_identity": pipe["funnel_identity"],
                "census_same_set_same_order_exp150":
                    pipe["census_vs_exp150"][
                        "same_set_same_order_exp150"],
                "price_tables_rows": {
                    "exp150_targets": t1["n_rows"],
                    "deep_targets": t2["n_rows"]},
                "price_tables_96_rows_each": tables_ok,
                "price_tables_fresh_after_funnel": True,
                "deep_target_checksums_vs_deposit": "asserted (3/3)",
                "pass": ok}

    def evaluate_h2(sections: dict) -> dict | None:
        sec = sections.get("clause_exp150_targets")
        if sec is None:
            return None
        kept = sec["walk"]["kept"]
        rows = [dict(p, member=k["member"], idx=k["idx"])
                for k in kept for p in k["per_target"]]
        complete = bool(
            len(kept) == N_DELIVER
            and all(len(k["per_target"]) == dep150["funnel"][
                "delivered_repaired"] for k in kept))
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
        return {"gate": "H2", "clause": (
            "the old operating point's quality bars hold at exp150's "
            "own targets: the clause delivered-10 (ranked by price at "
            "exp150's deposited targets) scored against exp150's "
            "deposited targets — C1 every member beyond N*_lib and "
            "N*_splice, C2 emitted-rung quads < 6.0, C3 decode < 6.0 "
            "AND hold < 6.0 on 3/3 seeds, C4 min pairwise D > N*_pool "
            "— ALL PASS (the member SET may differ from exp150's; the "
            "quality bars may not)"),
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

    def evaluate_h3(sections: dict) -> dict | None:
        sec = sections.get("clause_deep_targets")
        if sec is None:
            return None
        kept = sec["walk"]["kept"]
        rows = [dict(p, member=k["member"], idx=k["idx"])
                for k in kept for p in k["per_target"]]
        want_targets = sorted(f"rung_{r:g}" for r in DEEP_RUNGS)
        complete = bool(
            len(kept) == N_DELIVER
            and all(len(k["per_target"]) == len(DEEP_RUNGS)
                    for k in kept)
            and sorted(set(p["target"] for p in rows)) == want_targets)
        per_rung_counts = {
            f"{r:g}": sum(int(p["n_ok"] == len(AUDIT_SEEDS))
                          for p in rows if p["target"] == f"rung_{r:g}")
            for r in DEEP_RUNGS}
        members_all = sum(
            1 for k in kept
            if len(k["per_target"]) == len(DEEP_RUNGS)
            and all(p["n_ok"] == len(AUDIT_SEEDS)
                    for p in k["per_target"]))
        n_rej = sum(p["n_rejected"] for p in rows)
        modes = sorted(set(p["emission_mode"] for p in rows))
        ok = bool(complete and members_all >= 9 and n_rej == 0
                  and modes == ["repriced_full"])
        return {"gate": "H3", "clause": (
            "deep-target delivery — the clause's purpose: the clause "
            "delivered-10 (ranked by price at exp176's deep set) "
            "scored against exp176's deep target set (rungs "
            "-40/-50/-60, the deposited constructions): >= 9/10 "
            "members with decode < 6.0 AND hold < 6.0 on 3/3 seeds at "
            "EVERY rung; zero rejections; emission mode "
            "repriced_full"),
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

    def evaluate_h4(sections: dict) -> dict | None:
        pipe = sections.get("pipeline")
        t1 = sections.get("price_table_exp150_targets")
        t2 = sections.get("price_table_deep_targets")
        c150 = sections.get("clause_exp150_targets")
        cdeep = sections.get("clause_deep_targets")
        if any(s is None for s in (pipe, t1, t2, c150, cdeep)):
            return None
        rw_pos = pipe["rw_pos_production"]
        excluded = pipe["excluded_by_rw"]
        identity = bool(sorted(rw_pos)
                        == sorted(x["idx"] for x in excluded))
        walks_idxs = ([k["idx"] for k in c150["walk"]["kept"]]
                      + [k["idx"] for k in cdeep["walk"]["kept"]])
        walks_rw_negative = all(
            not pipe["rw_census"][i]["r_w_positive_production"]
            for i in walks_idxs)
        all_rows = [p for t in (t1, t2) for r in t["rows"]
                    for p in r["per_target"]]
        n_rej = sum(p["n_rejected"] for p in all_rows)
        ok = bool(
            len(rw_pos) == 0 and len(excluded) == 0 and identity
            and walks_rw_negative and not pipe["false_exclusions"]
            and pipe["delivered_rw_negative"]
            and n_rej == 0)
        return {"gate": "H4", "clause": (
            "discipline: the R_W production-floor set empty == the "
            "excluded set over the eligible pool (both target sets); "
            "zero rejections everywhere; the price table's rng "
            "consumption does not perturb the search's bit-identity "
            "(prices computed AFTER the funnel re-derivation, in a "
            "fresh process block, pin untouched — no instrument pin "
            "needed: this run is post-CF-1 production world)"),
                "n_rw_pos_production": len(rw_pos),
                "rw_pos_production": rw_pos,
                "n_excluded": len(excluded),
                "excluded_by_rw": excluded,
                "rw_set_identity": identity,
                "clause_walks_apply_no_rw_exclusions": True,
                "clause_walk_members_all_rw_negative":
                    walks_rw_negative,
                "delivered_rw_negative": pipe["delivered_rw_negative"],
                "false_exclusions": pipe["false_exclusions"],
                "zero_rejections_everywhere": bool(n_rej == 0),
                "n_price_rows_checked": len(all_rows),
                "rejections_total": n_rej,
                "instrument_pin_used": False,
                "production_floor_asserted": True,
                "prices_after_funnel_rederivation": True,
                "search_bitidentity_asserted_before_pricing": True,
                "pass": ok}

    # ---- dispatch ------------------------------------------------------
    print("=== exp179: TARGET-AWARE DELIVERY (the clause exp176 "
          "registered — price-ranked delivery within the C4 diversity "
          "constraint) ===\n")
    if args.smoke:
        pipe = run_pipeline()
        T1, T2 = targets_exp150(), targets_deep()
        sub = pipe["members"][:3]
        tab1 = price_table(T1, sub)
        tab2 = price_table(T2, sub)
        print(f"  SMOKE (the price table for 3 pool members only — "
              f"discarded): T1 rows {tab1['n_rows']} x "
              f"{T1['n_targets']} targets | T2 rows {tab2['n_rows']} x "
              f"{T2['n_targets']} targets | prices T1 "
              f"{[round(r['price_composed_decode_err'], 3) for r in tab1['rows']]} "
              f"| prices T2 "
              f"{[round(r['price_composed_decode_err'], 3) for r in tab2['rows']]}")
        dep = {"exp": "exp179_target_aware_delivery", "kind": "smoke",
               "discarded": True,
               "pipeline_funnel": pipe["funnel"],
               "bars": pipe["bars"],
               "smoke_price_table_T1":
               {r["member"]: r["price_composed_decode_err"]
                for r in tab1["rows"]},
               "smoke_price_table_T2":
               {r["member"]: r["price_composed_decode_err"]
                for r in tab2["rows"]},
               "wall_s": round(time.time() - t0, 1)}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                        exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(dep, fh, indent=1, default=float)
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
        "library_members": 72,
        "splice_family_size": 48564,
        "harness_max_abs_diff": pipe["harness_max_abs_diff"],
        "bars_deposited_before_selection":
        pipe["bars_deposited_before_selection"],
        "search_replication": pipe["search_replication"],
        "funnel": pipe["funnel"],
        "funnel_identity": pipe["funnel_identity"],
        "rw_census": pipe["rw_census"],
        "rw_pos_production": pipe["rw_pos_production"],
        "excluded_by_rw": pipe["excluded_by_rw"],
        "delivered_rw_negative": pipe["delivered_rw_negative"],
        "shadow_pricing": pipe["shadow_pricing"],
        "false_exclusions": pipe["false_exclusions"],
        "census_vs_exp150": pipe["census_vs_exp150"],
        "delivered_reference_keys": pipe["delivered_reference_keys"],
        "canon_check": bool(pipe.get("canon_check", True))}

    # the price tables (fresh, after the funnel re-derivation)
    def tables_for(job: str) -> None:
        if job in ("H1", "H2", "all"):
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
        if job in ("H1", "H3", "all"):
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
    if args.job in ("H2", "all"):
        T1 = targets_exp150()
        tab1 = result["sections"]["price_table_exp150_targets"]
        walk1 = clause_walk(tab1, members)
        kept1 = [{**k, "per_target": k["per_target"]}
                 for k in walk1["kept"]]
        result["sections"]["clause_exp150_targets"] = {
            "target_set_label": "exp150_targets",
            "target_set_construction": T1["construction"],
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
    if args.job in ("H3", "all"):
        T2 = targets_deep()
        tab2 = result["sections"]["price_table_deep_targets"]
        walk2 = clause_walk(tab2, members)
        kept2 = [{**k, "per_target": k["per_target"]}
                 for k in walk2["kept"]]
        result["sections"]["clause_deep_targets"] = {
            "target_set_label": "deep_targets",
            "target_set_construction": T2["construction"],
            "walk": {"ranked_order_idxs": walk2["ranked_order_idxs"],
                     "n_kept": walk2["n_kept"],
                     "kept": kept2,
                     "skipped_diversity_blocked":
                     walk2["skipped_diversity_blocked"],
                     "pairwise_D": walk2["pairwise_D"],
                     "min_pairwise_D": walk2["min_pairwise_D"],
                     "bar": walk2["bar"]},
            "scoring_note": (
                "each kept member scored against EVERY deep rung "
                "(-40/-50/-60) at the production cell (1.0, 0.0), "
                "seeds (1,2,3) — the per_target rows ARE the scoring "
                "rows (the same price_rung calls; no re-decode)")}

    # gates: each evaluated exactly once, on complete inputs only
    for name, fn in (("H1", evaluate_h1), ("H2", evaluate_h2),
                     ("H3", evaluate_h3), ("H4", evaluate_h4)):
        if name in result["gates"]:
            continue
        g = fn(result["sections"])
        if g is not None:
            result["gates"][name] = g

    npass = sum(int(g["pass"]) for g in result["gates"].values())
    for name in ("H1", "H2", "H3", "H4"):
        if name in result["gates"]:
            g = result["gates"][name]
            extra = ""
            if name == "H1":
                extra = (f" (bars {g['bars']}, funnel "
                         f"{g['funnel_counts_96_253_96_96']}, tables "
                         f"{g['price_tables_rows']})")
            elif name == "H2":
                extra = (f" (C1 {g['c1_members_beyond_bars']}, C2 "
                         f"{g['c2_all_quads_below_bar']}, C3 "
                         f"{g['c3_all_decode_hold_333']}, C4 min D "
                         f"{g['c4_min_pairwise_D']:.3f} > "
                         f"{g['c4_bar']:.3f}, rows "
                         f"{g['n_scoring_rows']})")
            elif name == "H3":
                extra = (f" ({g['members_passing_all_targets']}/"
                         f"{g['n_delivered']} members pass all targets"
                         f", per-rung {g['per_rung_333_counts']}, rej "
                         f"{g['rejections']}, modes "
                         f"{g['emission_modes']})"
                         if g["complete"] else " (incomplete)")
            elif name == "H4":
                extra = (f" (R_W-positive {g['n_rw_pos_production']}, "
                         f"excluded {g['n_excluded']}, false "
                         f"{len(g['false_exclusions'])}, rej "
                         f"{g['rejections_total']}/{g['n_price_rows_checked']} rows)")
            print(f"  GATE-{name}: {'PASS' if g['pass'] else 'REFUTE'}"
                  f"{extra}")
    verdict = (f"{npass}/{len(result['gates'])} gates "
               f"({' '.join(k for k in ('H1', 'H2', 'H3', 'H4')
                            if k in result['gates'])})")
    print(f"  === {verdict} ===")

    result.update({
        "exp": "exp179_target_aware_delivery",
        "claim": (
            "TARGET-AWARE DELIVERY (the clause exp176 registered, "
            "L155's repair): the search's selection machinery is "
            "TARGET-FREE (exp176 G1 bit-identity at seed 141) and its "
            "delivered cohort fails deep-target delivery (exp176 G2 "
            "REFUTE). THE CLAUSE (one rule, zero knobs): given the "
            "96-eligible pool (exp168's B3 funnel at seed 141, "
            "bit-identical re-derivation) and a target set T, rank "
            "members ASCENDING by price(m, T) = the MEAN composed "
            "decode err over T's targets x seeds (1,2,3) via exp150's "
            "price_rung VERBATIM at the production cell (1.0, 0.0); "
            "walk the ranked order, keeping member m iff its min "
            "pairwise distance D(m, kept) > N*_pool (33.776, the "
            "deposited C4 bar); stop at 10; tie-break member index "
            "ascending. Run at BOTH target sets: exp150's own targets "
            "(its deposit) and exp176's deep set (its deposit sections "
            "rung_-40/-50/-60 targets)"),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration; gates H1-H4 fixed "
                             "there, each evaluated exactly once)"),
            "gates": [
                "H1 pipeline integrity: the 72-member library, splice "
                "family, and 96-eligible pool re-derive bit-identically "
                "to exp176's deposit (bars 82.288 / 20.140 / 33.776; "
                "funnel counts 96/253 -> 96/96); the pool's price "
                "table at T computed fresh and deposited (96 rows)",
                "H2 the old operating point's quality bars hold at "
                "exp150's own targets: C1 beyond N*_lib and N*_splice, "
                "C2 emitted-rung quads < 6.0, C3 decode < 6.0 AND hold "
                "< 6.0 on 3/3 seeds, C4 min pairwise D > N*_pool — "
                "ALL PASS (member set may differ; bars may not)",
                "H3 deep-target delivery: >= 9/10 members with decode "
                "< 6.0 AND hold < 6.0 on 3/3 seeds at EVERY deep rung; "
                "zero rejections; emission mode repriced_full",
                "H4 discipline: R_W production-floor set empty == the "
                "excluded set (both target sets); zero rejections "
                "everywhere; prices computed AFTER the funnel "
                "re-derivation, pin untouched"],
            "tie_break": "member index ascending (J-ordered funnel "
                         "index)",
            "structure": ("exp168's B3 pipeline re-derivation verbatim "
                          "(exp176's run_pipeline minus the old-floor "
                          "pin, per H4); the pricing stage reuses "
                          "exp150's price_rung/emit_rung VERBATIM with "
                          "the target profile f swapped to the target "
                          "set's constructions")},
        "stage_order": ["pipeline_rederivation (library -> splice -> "
                        "search seed 141 -> funnel -> N*_pool -> R_W "
                        "census)",
                        "search_bitidentity_asserted (exp141 deposit)",
                        "price_tables_fresh_after_funnel",
                        "clause_walks (price-ranked, C4-diverse, cap "
                        "10)",
                        "gates_evaluated"],
        "smoke_disclosure": ("a --smoke check (the price table for 3 "
                             "pool members only) ran before the "
                             "credited run and was discarded (no "
                             "file)"),
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
    ap.add_argument("--job", choices=["H1", "H2", "H3", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
