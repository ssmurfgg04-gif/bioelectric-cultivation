#!/usr/bin/env python3
"""exp196 — THE ARMED-CORE GENERATOR PRICES (the feature's value in
the generator's currency).

exp191's registered next (L167): the exp168 B3 pipeline re-run at
ARM-DEEP (core.M33_LINE rebound -60.0) vs the production split — the
search is target-free so selection is bit-identical; the decode/hold
prices shift where deep identities exist.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp179's pipeline + price-table machinery verbatim; exp186's ARM-DEEP rebinding.

GATES (each evaluated exactly once):
  GATE-W1 (selection identity) the funnel + delivery at seed 141
           BIT-IDENTICAL between arms (the search consults no pole
           channel — proven, not assumed).
  GATE-W2 (the price shift) the delivered cohort's decode/hold
           prices at the deposited targets, ARM-DEEP vs ARM-PROD,
           3 seeds: per-member deltas deposited; the members with
           nonzero deltas counted (the armed feature's footprint).
  GATE-W3 (the direction) the pre-named branch: NET-POSITIVE iff
           the mean delta < 0 (armed helps the generator's own
           targets), NET-NEGATIVE if > 0, NEUTRAL if all |delta|
           < 0.005 (float noise). All complete.
  GATE-W4 (hygiene) rebind asserted per arm; zero rejections both
           arms.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp196_armed_core_prices.json
RUN: python3 -m experiments.exp196_armed_core_prices [--smoke] [--job ...] [--out ...]
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

BAR_LIB = 82.288
BAR_SPLICE = 20.140
BAR_POOL = 33.776

OUT = os.path.join(ROOT, "results", "exp196_armed_core_prices.json")


def main() -> dict:
    # ==== BODY (written by the run agent; docstring/imports/constants
    # above byte-unchanged — exp174's body-only discipline) ============
    import time
    import traceback

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all"], default="all",
                    help="only the credited both-arms run is registered: "
                         "W1's bit-identity is a CROSS-ARM comparison "
                         "(exp191's one-job pattern)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()  # sys.argv — the pre-registered __main__ CLI
    out_path = args.out if args.out is not None else OUT

    # ---- exp179's import block, verbatim (BLAS pins included) --------
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
    from experiments.exp136_generator_v6 import (  # noqa: E402
        decode as exp136_decode,
    )
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n,
    )

    DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
    DEP168 = os.path.join(ROOT, "results", "exp168_cf1_production.json")
    DEP150 = os.path.join(ROOT, "results",
                          "exp150_generator_complete.json")
    DEP176 = os.path.join(ROOT, "results",
                          "exp176_deep_band_search.json")
    PROD_FLOOR = -60.0                    # CF-1's production value
    PROD_LINE = -35.0                     # exp175's production split
    DEEP_LINE = -60.0                     # the ARM-DEEP counterfactual
    SEARCH_SEED = 141
    DEEP_RUNGS = [-40.0, -50.0, -60.0]
    NOISE_BAR = 0.005                     # W3's float-noise bar

    # the two target-set deposits (the price tables' T inputs, exp179's)
    dep150 = json.load(open(DEP150))
    dep176 = json.load(open(DEP176))

    # ---- instrument check: the production core in situ ---------------
    # (exp179's floors check verbatim + exp186's ARM precondition: the
    # production split core M33_LINE = -35.0 must be in the tree.)
    floors = {"CORE": CORE.NEURAL_SPEC_MIN,
              "M136": M136.NEURAL_SPEC_MIN,
              "M156": M156.NEURAL_SPEC_MIN}
    assert all(v == PROD_FLOOR for v in floors.values()), \
        f"production floor drift: {floors}"
    assert CORE.M33_LINE == PROD_LINE, \
        "precondition: the production split core (M33_LINE = -35.0, " \
        "exp175) must be in the tree"

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
                # exp196's ONE disclosed deviation: the return dict
                # gains the delivered records (W2's cohort); every
                # other line of this machinery is verbatim exp179.
                "delivered": delivered,
                # the 96-eligible pool records (the clause's input):
                "members": splice_clear,
                "n_star_lib": n_star_lib,
                "n_star_splice": n_star_splice,
                "n_star_pool": n_star_pool}

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
    # W1's ARM FINGERPRINTS (the bit-identity evidence, auditable
    # in-deposit: everything W1 calls "the funnel + delivery at seed
    # 141", canonically serialized with full-precision floats)
    # ==================================================================
    def _f_sha(f: np.ndarray) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()) \
            .hexdigest()

    def _canon(x):
        if isinstance(x, dict):
            return {str(k): _canon(x[k]) for k in sorted(x, key=str)}
        if isinstance(x, (list, tuple)):
            return [_canon(v) for v in x]
        if isinstance(x, bool) or x is None or isinstance(x, str):
            return x
        if isinstance(x, (int, np.integer)):
            return int(x)
        if isinstance(x, (float, np.floating)):
            return float(x).hex()
        if isinstance(x, np.ndarray):
            return {"__ndarray__": str(x.dtype), "shape": list(x.shape),
                    "sha256": hashlib.sha256(
                        np.ascontiguousarray(x).tobytes()).hexdigest()}
        return repr(x)

    def _digest(obj) -> str:
        return hashlib.sha256(json.dumps(_canon(obj), sort_keys=True,
                                         separators=(",", ":"))
                              .encode()).hexdigest()

    def member_fp(r: dict) -> dict:
        return {"key": W.to_key([tuple(z) for z in r["zones"]]),
                "zones": [[float(x).hex() for x in z]
                          for z in r["zones"]],
                "J": float(r["J"]).hex(),
                "nov_lib": float(r["nov_lib"]).hex(),
                "nov_splice": (float(r["nov_splice"]).hex()
                               if "nov_splice" in r else None),
                "novel": bool(r["novel"]),
                "search_cell": [float(r["search_cell"][0]),
                                float(r["search_cell"][1])],
                "search_eV": float(r["search_eV"]).hex(),
                "search_eT": float(r["search_eT"]).hex(),
                "search_quad": float(r["search_quad"]).hex(),
                "tags": _canon(r["tags"]),
                "f_sha256": _f_sha(r["f"])}

    def funnel_fingerprint(pipe: dict) -> dict:
        return {"round_rows": pipe["search_replication"]["round_rows"],
                "pool_size": pipe["search_replication"]["pool_size"],
                "funnel": pipe["funnel"],
                "bars": {k: float(v).hex()
                         for k, v in pipe["bars"].items()},
                "n_stars_full_precision": {
                    "n_star_lib": float(pipe["n_star_lib"]).hex(),
                    "n_star_splice":
                        float(pipe["n_star_splice"]).hex(),
                    "n_star_pool": float(pipe["n_star_pool"]).hex()},
                "harness_max_abs_diff":
                    float(pipe["harness_max_abs_diff"]).hex(),
                "members_J_order": [member_fp(r)
                                    for r in pipe["members"]],
                "rw_rows": pipe["rw_census"],
                "rw_pos_production": pipe["rw_pos_production"],
                "excluded_by_rw": pipe["excluded_by_rw"],
                "excluded_names": pipe["excluded_names"],
                "shadow_pricing": pipe["shadow_pricing"],
                "false_exclusions": pipe["false_exclusions"],
                "census_vs_exp150": pipe["census_vs_exp150"],
                "delivered_reference_keys":
                    pipe["delivered_reference_keys"]}

    # ==================================================================
    # ONE ARM: the pipeline + price-table machinery under the arm's core
    # ==================================================================
    def tab_dep(tab: dict, T: dict) -> dict:
        return {"target_set_label": tab["target_set_label"],
                "target_set_construction": T["construction"],
                "targets": [{k: v for k, v in t.items() if k != "f"}
                            for t in T["targets"]],
                "n_rows": tab["n_rows"],
                "instrument": tab["instrument"],
                "provenance_cell_1_0": tab["provenance_cell_1_0"],
                "rows": tab["rows"]}

    def run_arm(deep: bool) -> dict:
        """ONE arm of exp196: exp179's pipeline + price-table machinery
        VERBATIM, under the arm's core. ARM-PROD (deep=False): the tree
        as-is — no rebind, the line asserted unchanged pre/post the arm.
        ARM-DEEP (deep=True): exp186's counterfactual — the ONE constant
        core.M33_LINE rebound to -60.0 via exp174's save/rebind/restore
        mechanism, asserted per arm; the CF-1-world M33 behavior."""
        arm_label = "deep" if deep else "prod"
        if deep:
            saved = CORE.M33_LINE
            assert saved == PROD_LINE, \
                f"pre-rebind drift: M33_LINE = {saved} != {PROD_LINE}"
            CORE.M33_LINE = DEEP_LINE
            assert CORE.M33_LINE == DEEP_LINE, "rebind to -60.0 failed"
        else:
            assert CORE.M33_LINE == PROD_LINE, \
                "ARM-PROD precondition: the tree's core as-is"
        try:
            pipe = run_pipeline()
            T1 = targets_exp150()
            T2 = targets_deep()
            delivered = pipe["delivered"]
            assert len(delivered) == N_DELIVER, \
                f"delivered cohort size drift: {len(delivered)}"
            print(f"  [{arm_label}] pricing the delivered cohort at "
                  f"both deposited target sets ...")
            tab1 = price_table(T1, delivered)
            tab2 = price_table(T2, delivered)
        finally:
            if deep:
                CORE.M33_LINE = saved
                assert CORE.M33_LINE == PROD_LINE, \
                    "restore to -35.0 failed"
            else:
                assert CORE.M33_LINE == PROD_LINE, \
                    "ARM-PROD: the production line drifted during the arm"
        fp = funnel_fingerprint(pipe)
        fdig = _digest(fp)
        ddig = _digest({"keys": pipe["delivered_reference_keys"],
                        "members": [member_fp(r) for r in delivered]})
        total_rej = sum(p["n_rejected"]
                        for tab in (tab1, tab2)
                        for r in tab["rows"]
                        for p in r["per_target"])
        print(f"  [{arm_label}] funnel digest {fdig[:16]}... | delivered "
              f"digest {ddig[:16]}... | price rejections {total_rej}")
        if deep:
            rebind_rec = {
                "mechanism": ("exp174's rebinding mechanism via exp186's "
                              "protocol: save, assert, rebind, run, "
                              "restore, assert — the ONE constant "
                              "core.M33_LINE, the one module that "
                              "binds it"),
                "saved_line": saved, "rebound_line": DEEP_LINE,
                "restore_assert_passed": True,
                "post_restore_line": CORE.M33_LINE}
        else:
            rebind_rec = {
                "mechanism": ("none — the tree's production core as-is "
                              "(exp186's ARM-PROD); the line asserted "
                              "unchanged pre and post the whole arm"),
                "rebound": False,
                "line_pre": PROD_LINE, "line_post": PROD_LINE}
        return {"arm": arm_label, "crashed": False,
                "m33_line_effective": (DEEP_LINE if deep else PROD_LINE),
                "rebind": rebind_rec,
                "funnel_digest": fdig,
                "delivered_digest": ddig,
                "pipe": {"bars": pipe["bars"],
                         "funnel": pipe["funnel"],
                         "funnel_identity": pipe["funnel_identity"],
                         "search_replication":
                             pipe["search_replication"],
                         "harness_max_abs_diff":
                             pipe["harness_max_abs_diff"],
                         "rw_census": pipe["rw_census"],
                         "rw_pos_production": pipe["rw_pos_production"],
                         "excluded_by_rw": pipe["excluded_by_rw"],
                         "excluded_names": pipe["excluded_names"],
                         "delivered_rw_negative":
                             pipe["delivered_rw_negative"],
                         "shadow_pricing": pipe["shadow_pricing"],
                         "false_exclusions": pipe["false_exclusions"],
                         "census_vs_exp150": pipe["census_vs_exp150"],
                         "delivered_reference_keys":
                             pipe["delivered_reference_keys"],
                         "fingerprint": fp},
                "delivered": [{"idx": i,
                               "name": dep150["delivered"][i]["name"],
                               "key": W.to_key([tuple(z)
                                                for z in r["zones"]]),
                               "J": float(r["J"]),
                               "nov_lib": float(r["nov_lib"]),
                               "nov_splice": float(r["nov_splice"]),
                               "zones": [list(z) for z in r["zones"]]}
                              for i, r in enumerate(delivered)],
                "price_tables": {"exp150_targets": tab_dep(tab1, T1),
                                 "deep_targets": tab_dep(tab2, T2)},
                "price_rows_rejections": total_rej}

    def _jdefault(o):
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(f"unserializable: {type(o)}")

    # ---- --smoke: the pipeline only, ONE arm (permitted, discarded) ---
    print("=== exp196: THE ARMED-CORE GENERATOR PRICES (the feature's "
          "value in the generator's currency) ===\n")
    if args.smoke:
        assert CORE.M33_LINE == PROD_LINE, \
            "smoke precondition: the tree's production core as-is"
        pipe = run_pipeline()          # ONE arm (ARM-PROD), pipeline only
        dep = {"exp": "exp196_armed_core_prices", "kind": "smoke",
               "discarded": True,
               "funnel": pipe["funnel"], "bars": pipe["bars"],
               "n_delivered": len(pipe["delivered"]),
               "delivered_keys": pipe["delivered_reference_keys"],
               "wall_s": round(time.time() - t0, 1)}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                        exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(dep, fh, indent=1, default=_jdefault)
        print(f"  SMOKE (pipeline only, ONE arm — discarded): funnel "
              f"{pipe['funnel']} | bars {pipe['bars']}")
        return dep

    # ---- the credited BOTH-ARMS run (ARM-PROD first, tree as-is;
    #      then ARM-DEEP under the rebound line) ------------------------
    arms: dict = {}
    for deep in (False, True):
        label = "arm_deep" if deep else "arm_prod"
        arm_desc = ("(core.M33_LINE rebound to -60.0)" if deep
                    else "(the tree as-is, M33_LINE = -35.0)")
        print(f"\n--- ARM-{'DEEP' if deep else 'PROD'} {arm_desc} ---")
        try:
            arms[label] = run_arm(deep)
        except Exception as exc:  # noqa: BLE001 — a crashed arm IS
            #            W1's REFUTE evidence; deposit it, do not die.
            arms[label] = {"arm": ("deep" if deep else "prod"),
                           "crashed": True, "error": repr(exc),
                           "traceback": traceback.format_exc()}
            print(f"  ARM CRASHED: {exc!r}")

    sections: dict = {"arm_prod": arms["arm_prod"],
                      "arm_deep": arms["arm_deep"]}
    both_alive = not (sections["arm_prod"].get("crashed")
                      or sections["arm_deep"].get("crashed"))

    # ==================================================================
    # W2's PER-MEMBER DELTA TABLES (both deposited target sets)
    # ==================================================================
    def deltas_for(set_label: str, prod_arm: dict,
                   deep_arm: dict) -> dict:
        """Per-member decode/hold price deltas, ARM-DEEP vs ARM-PROD
        (delta = deep − prod), per target, per seed — the SAME
        exp150 price_rung calls both arms (exp179's price_table
        machinery, verbatim, on the delivered cohort)."""
        prows = {r["member"]: r
                 for r in prod_arm["price_tables"][set_label]["rows"]}
        drows = {r["member"]: r
                 for r in deep_arm["price_tables"][set_label]["rows"]}
        assert set(prows) == set(drows) and len(prows) == N_DELIVER, \
            "delivered cohort membership drift between arms"
        n_t = len(prod_arm["price_tables"][set_label]["targets"])
        rows, pooled = [], []
        for i in range(N_DELIVER):
            m = f"pool-{i:03d}"
            p, q = prows[m], drows[m]
            assert p["zones"] == q["zones"], \
                f"{set_label}/{m}: member program drift between arms"
            per, mdeltas = [], []
            for pi, pr in enumerate(p["per_target"]):
                qr = q["per_target"][pi]
                assert qr["target"] == pr["target"], \
                    f"{set_label}/{m}: target order drift"
                d_dec = [b - a for a, b in zip(pr["decode_errs"],
                                               qr["decode_errs"])]
                d_hold = [b - a for a, b in zip(pr["hold_errs"],
                                                qr["hold_errs"])]
                d_dm = qr["decode_err_mean"] - pr["decode_err_mean"]
                d_hm = qr["hold_err_mean"] - pr["hold_err_mean"]
                per.append({"target": pr["target"],
                            "prod": {"decode_errs": pr["decode_errs"],
                                     "hold_errs": pr["hold_errs"],
                                     "decode_err_mean":
                                         pr["decode_err_mean"],
                                     "hold_err_mean": pr["hold_err_mean"],
                                     "n_ok": pr["n_ok"],
                                     "n_rejected": pr["n_rejected"],
                                     "emission_mode":
                                         pr["emission_mode"]},
                            "deep": {"decode_errs": qr["decode_errs"],
                                     "hold_errs": qr["hold_errs"],
                                     "decode_err_mean":
                                         qr["decode_err_mean"],
                                     "hold_err_mean": qr["hold_err_mean"],
                                     "n_ok": qr["n_ok"],
                                     "n_rejected": qr["n_rejected"],
                                     "emission_mode":
                                         qr["emission_mode"]},
                            "delta_decode_errs": d_dec,
                            "delta_hold_errs": d_hold,
                            "delta_decode_err_mean": d_dm,
                            "delta_hold_err_mean": d_hm})
                mdeltas.extend(d_dec + d_hold + [d_dm, d_hm])
            rows.append({"member": m,
                         "name": prod_arm["delivered"][i]["name"],
                         "price_prod": p["price_composed_decode_err"],
                         "price_deep": q["price_composed_decode_err"],
                         "delta_price":
                             q["price_composed_decode_err"]
                             - p["price_composed_decode_err"],
                         "delta_decode_err_mean_member":
                             float(np.mean([x["delta_decode_err_mean"]
                                            for x in per])),
                         "delta_hold_err_mean_member":
                             float(np.mean([x["delta_hold_err_mean"]
                                            for x in per])),
                         "n_deltas": len(mdeltas),
                         "member_nonzero_any":
                             bool(any(x != 0.0 for x in mdeltas)),
                         "member_max_abs_delta":
                             float(max(abs(x) for x in mdeltas)),
                         "per_target": per})
            pooled.extend(mdeltas)
        return {"target_set_label": set_label,
                "n_members": len(rows), "n_targets": n_t,
                "n_deltas": len(pooled),
                "n_members_nonzero":
                    sum(int(r["member_nonzero_any"]) for r in rows),
                "n_deltas_nonzero": sum(1 for x in pooled if x != 0.0),
                "n_deltas_at_or_above_noise_bar":
                    sum(1 for x in pooled if abs(x) >= NOISE_BAR),
                "max_abs_delta":
                    float(max((abs(x) for x in pooled), default=0.0)),
                "mean_delta":
                    float(np.mean(pooled)) if pooled else 0.0,
                "rows": rows, "pooled_deltas": pooled}

    delta_secs: dict = {}
    if both_alive:
        for sl in ("exp150_targets", "deep_targets"):
            delta_secs[sl] = deltas_for(sl, sections["arm_prod"],
                                        sections["arm_deep"])
    sections["price_deltas"] = delta_secs

    # ==================================================================
    # THE GATES (each evaluated exactly once, on complete inputs)
    # ==================================================================
    W1_CLAUSE = ("selection identity: the funnel + delivery at seed 141 "
                 "BIT-IDENTICAL between arms (the search consults no "
                 "pole channel — proven, not assumed).")
    W2_CLAUSE = ("the price shift: the delivered cohort's decode/hold "
                 "prices at the deposited targets, ARM-DEEP vs ARM-PROD, "
                 "3 seeds: per-member deltas deposited; the members with "
                 "nonzero deltas counted (the armed feature's footprint).")
    W3_CLAUSE = ("the direction: the pre-named branch: NET-POSITIVE iff "
                 "the mean delta < 0 (armed helps the generator's own "
                 "targets), NET-NEGATIVE if > 0, NEUTRAL if all |delta| "
                 "< 0.005 (float noise). All complete.")
    W4_CLAUSE = ("hygiene: rebind asserted per arm; zero rejections "
                 "both arms.")

    def evaluate_w1(sections, _delta) -> dict:
        p, d = sections["arm_prod"], sections["arm_deep"]
        if p.get("crashed") or d.get("crashed"):
            return {"gate": "W1", "clause": W1_CLAUSE, "pass": False,
                    "arm_crash": True,
                    "crash_prod": p.get("error"),
                    "crash_deep": d.get("error")}
        same_fd = p["funnel_digest"] == d["funnel_digest"]
        same_dd = p["delivered_digest"] == d["delivered_digest"]
        bars_equal = all(p["pipe"]["bars"][k] == d["pipe"]["bars"][k]
                         for k in p["pipe"]["bars"])
        funnel_equal = p["pipe"]["funnel"] == d["pipe"]["funnel"]
        keys_equal = (p["pipe"]["delivered_reference_keys"]
                      == d["pipe"]["delivered_reference_keys"])
        rw_equal = (p["pipe"]["rw_pos_production"]
                    == d["pipe"]["rw_pos_production"])
        census_ok = all(a["pipe"]["census_vs_exp150"][
            "same_set_same_order_exp150"] for a in (p, d))
        fp_keys = sorted(p["pipe"]["fingerprint"].keys())
        assert fp_keys == sorted(d["pipe"]["fingerprint"].keys()), \
            "fingerprint field drift between arms"
        ok = bool(same_fd and same_dd and bars_equal and funnel_equal
                  and keys_equal and rw_equal and census_ok)
        return {"gate": "W1", "clause": W1_CLAUSE,
                "funnel_digest_prod": p["funnel_digest"],
                "funnel_digest_deep": d["funnel_digest"],
                "delivered_digest_prod": p["delivered_digest"],
                "delivered_digest_deep": d["delivered_digest"],
                "funnel_digests_bit_identical": bool(same_fd),
                "delivered_digests_bit_identical": bool(same_dd),
                "bars_float_equal": bool(bars_equal),
                "funnel_counts_equal": bool(funnel_equal),
                "delivered_keys_bit_identical": bool(keys_equal),
                "rw_census_equal": bool(rw_equal),
                "both_arms_reproduce_exp150s_cohort": bool(census_ok),
                "arm_crash": False,
                "fingerprint_fields": fp_keys,
                "proof_note": (
                    "the FULL exp168-B3 pipeline (library -> splice "
                    "harness -> search seed 141 -> funnel -> N*_pool -> "
                    "R_W census -> J-order delivery) was RE-RUN under "
                    "the rebound core (ARM-DEEP) and compared field-by-"
                    "field against the ARM-PROD arm via the deposited "
                    "per-arm fingerprints (full-precision float hexes + "
                    "f-profile sha256s); bit-identity is proven by "
                    "execution, not assumed"),
                "pass": ok}

    def evaluate_w2(sections, _delta) -> dict:
        p, d = sections["arm_prod"], sections["arm_deep"]
        if p.get("crashed") or d.get("crashed") or not _delta:
            return {"gate": "W2", "clause": W2_CLAUSE, "pass": False,
                    "arm_crash": bool(p.get("crashed")
                                      or d.get("crashed"))}
        pooled = (_delta["exp150_targets"]["pooled_deltas"]
                  + _delta["deep_targets"]["pooled_deltas"])
        complete = all(s["n_members"] == N_DELIVER
                       and s["n_targets"] in (10, 3)
                       for s in _delta.values())
        finite = bool(np.all(np.isfinite(np.asarray(pooled,
                                                    dtype=float)))) \
            if pooled else True
        nz_members = sorted({r["name"] for s in _delta.values()
                             for r in s["rows"]
                             if r["member_nonzero_any"]})
        ok = bool(complete and finite)
        return {"gate": "W2", "clause": W2_CLAUSE,
                "complete": complete, "all_deltas_finite": finite,
                "n_members_scored": 2 * N_DELIVER,
                "n_deltas": len(pooled),
                "n_deltas_nonzero":
                    sum(s["n_deltas_nonzero"]
                        for s in _delta.values()),
                "n_members_nonzero_per_set":
                    {sl: s["n_members_nonzero"]
                     for sl, s in _delta.items()},
                "n_members_nonzero_pooled": len(nz_members),
                "members_nonzero": nz_members,
                "n_deltas_at_or_above_noise_bar":
                    sum(s["n_deltas_at_or_above_noise_bar"]
                        for s in _delta.values()),
                "max_abs_delta":
                    float(max((abs(x) for x in pooled), default=0.0)),
                "footprint_note": (
                    "the members with nonzero deltas are the armed "
                    "feature's footprint in the generator's currency "
                    "(delta = ARM-DEEP − ARM-PROD, per target, per "
                    "seed, decode AND hold; rows in sections."
                    "price_deltas.<set>.rows)"),
                "pass": ok}

    def evaluate_w3(_sections, delta) -> dict:
        if not delta:
            return {"gate": "W3", "clause": W3_CLAUSE, "pass": False,
                    "arm_crash": True}
        own, dep_set = delta["exp150_targets"], delta["deep_targets"]
        pooled = own["pooled_deltas"] + dep_set["pooled_deltas"]
        mean_own = float(np.mean([r["delta_price"]
                                  for r in own["rows"]]))
        mean_own_grand = float(np.mean(own["pooled_deltas"]))
        mean_deep_set = float(np.mean([r["delta_price"]
                                       for r in dep_set["rows"]]))
        mean_hold_own = float(np.mean(
            [r["delta_hold_err_mean_member"] for r in own["rows"]]))
        neutral = bool(all(abs(x) < NOISE_BAR for x in pooled))
        netpos = bool(mean_own < 0.0)
        netneg = bool(mean_own > 0.0)
        n_branches = int(neutral) + int(netpos) + int(netneg)
        assert n_branches == 1, \
            ("pre-named W3 branches not uniquely determined: "
             f"neutral={neutral} netpos={netpos} netneg={netneg}")
        branch = ("NET-POSITIVE" if netpos else
                  "NET-NEGATIVE" if netneg else "NEUTRAL")
        return {"gate": "W3", "clause": W3_CLAUSE,
                "primary_read": ("the mean delta at the generator's own "
                                 "targets (exp150's own-target set); "
                                 "delta = ARM-DEEP − ARM-PROD"),
                "mean_delta_price_own_targets": mean_own,
                "mean_delta_own_targets_grand_pooled":
                    mean_own_grand,
                "mean_delta_price_deep_targets": mean_deep_set,
                "mean_delta_hold_own_targets": mean_hold_own,
                "mean_delta_pooled_both_sets":
                    float(np.mean(pooled)),
                "noise_bar": NOISE_BAR,
                "neutral_condition_all_below_bar": neutral,
                "net_positive_condition_mean_lt_0": netpos,
                "net_negative_condition_mean_gt_0": netneg,
                "branches_triggered": n_branches,
                "branch": branch,
                "pass": bool(n_branches == 1)}

    def evaluate_w4(sections, _delta) -> dict:
        p, d = sections["arm_prod"], sections["arm_deep"]
        if p.get("crashed") or d.get("crashed"):
            return {"gate": "W4", "clause": W4_CLAUSE, "pass": False,
                    "arm_crash": True,
                    "crash_prod": p.get("error"),
                    "crash_deep": d.get("error")}
        rebind_ok = bool(
            d["rebind"]["saved_line"] == PROD_LINE
            and d["rebind"]["rebound_line"] == DEEP_LINE
            and d["rebind"]["restore_assert_passed"]
            and d["rebind"]["post_restore_line"] == PROD_LINE
            and p["rebind"]["rebound"] is False
            and p["rebind"]["line_pre"] == PROD_LINE
            and p["rebind"]["line_post"] == PROD_LINE
            and CORE.M33_LINE == PROD_LINE)
        rej = p["price_rows_rejections"] + d["price_rows_rejections"]
        ok = bool(rebind_ok and rej == 0)
        return {"gate": "W4", "clause": W4_CLAUSE,
                "rebind_prod": p["rebind"], "rebind_deep": d["rebind"],
                "rebind_asserted_per_arm": rebind_ok,
                "rejections_total": rej,
                "rejections_per_arm": {
                    "prod": p["price_rows_rejections"],
                    "deep": d["price_rows_rejections"]},
                "zero_rejections_both_arms": bool(rej == 0),
                "post_run_line": CORE.M33_LINE,
                "pass": ok}

    gates: dict = {}
    for name, fn in (("W1", evaluate_w1), ("W2", evaluate_w2),
                     ("W3", evaluate_w3), ("W4", evaluate_w4)):
        g = fn(sections, delta_secs)
        gates[name] = g
    npass = sum(int(g["pass"]) for g in gates.values())
    for name in ("W1", "W2", "W3", "W4"):
        g = gates[name]
        extra = ""
        if name == "W1":
            extra = (f" (funnel digest "
                     f"{g.get('funnel_digests_bit_identical')}, delivered "
                     f"digest {g.get('delivered_digests_bit_identical')}, "
                     f"bars {g.get('bars_float_equal')}, keys "
                     f"{g.get('delivered_keys_bit_identical')})")
        elif name == "W2":
            extra = (f" (deltas {g.get('n_deltas')}, nonzero "
                     f"{g.get('n_deltas_nonzero')}, members nonzero "
                     f"{g.get('n_members_nonzero_per_set')} pooled "
                     f"{g.get('n_members_nonzero_pooled')}, max |d| "
                     f"{g.get('max_abs_delta')})")
        elif name == "W3":
            extra = (f" (mean delta own-targets "
                     f"{g.get('mean_delta_price_own_targets')}, "
                     f"deep-targets "
                     f"{g.get('mean_delta_price_deep_targets')}, "
                     f"branch {g.get('branch')})")
        elif name == "W4":
            extra = (f" (rebind asserted "
                     f"{g.get('rebind_asserted_per_arm')}, rejections "
                     f"{g.get('rejections_total')})")
        print(f"  GATE-{name}: {'PASS' if g['pass'] else 'REFUTE'}"
              f"{extra}")
    verdict = f"{npass}/{len(gates)} gates (W1 W2 W3 W4)"
    print(f"  === {verdict} | branch "
          f"{gates['W3'].get('branch', 'UNEVALUATED')} ===")

    result = {"exp": "exp196_armed_core_prices",
              "claim": (
                  "THE ARMED-CORE GENERATOR PRICES (the feature's value "
                  "in the generator's currency): exp179's pipeline + "
                  "price-table machinery run TWICE — ARM-PROD (the "
                  "tree's production split core as-is, M33_LINE = "
                  "-35.0) and ARM-DEEP (core.M33_LINE rebound to "
                  "-60.0, exp186's save/rebind/restore asserted) — the "
                  "funnel + delivery at seed 141 re-derived under BOTH "
                  "arms (W1: bit-identity proven by execution, the "
                  "search consults no pole channel), then the delivered "
                  "cohort (exp150's deposited lineage d-01..d-10, "
                  "reproduced and asserted by both arms' census) priced "
                  "at BOTH deposited target sets (exp150's own targets; "
                  "exp176's deep rungs -40/-50/-60) via exp150's "
                  "price_rung VERBATIM at the production cell (1.0, "
                  "0.0), seeds (1,2,3); per-member decode/hold deltas "
                  "deposited (delta = ARM-DEEP − ARM-PROD); W3's "
                  "pre-named direction branch classifies the armed "
                  "feature's value in the generator's currency"),
              "pre_registered": {
                  "gates_source": ("module docstring, committed before "
                                   "any run (pre-registration; gates "
                                   "W1-W4 fixed there, each evaluated "
                                   "exactly once)"),
                  "gates": [W1_CLAUSE, W2_CLAUSE, W3_CLAUSE, W4_CLAUSE],
                  "instruments": ("exp179's pipeline + price-table "
                                  "machinery verbatim; exp186's ARM-DEEP "
                                  "rebinding (exp174's mechanism)")},
              "stage_order": [
                  "instrument_check (production floors + M33_LINE "
                  "-35.0 asserted in the tree)",
                  "arm_prod: pipeline (library -> splice harness -> "
                  "search seed 141 -> funnel -> N*_pool -> R_W census "
                  "-> J-order delivery) then the delivered cohort "
                  "priced at both deposited target sets",
                  "arm_deep: save/rebind core.M33_LINE -60.0 (asserted) "
                  "-> the SAME machinery -> restore (asserted)",
                  "W1 cross-arm fingerprint comparison (full-precision "
                  "digests)",
                  "W2 per-member delta tables (both target sets)",
                  "W3 direction branch (pre-named)",
                  "W4 hygiene census",
                  "deposit"],
              "deviations_disclosed": [
                  "run_pipeline's return dict gains the delivered "
                  "records ('delivered') — the ONE addition to the "
                  "verbatim exp179 machinery (W2 needs the cohort "
                  "records; the census inside run_pipeline already "
                  "asserts the cohort == exp150's deposited lineage "
                  "set+order)",
                  "the clause walks are NOT part of this "
                  "pre-registration and are not run; W1's 'delivery' "
                  "is the exp168-B3 pipeline's own J-order greedy "
                  "delivery (target-free by construction)"],
              "smoke_disclosure": (
                  "a --smoke check (the pipeline only, ONE arm — no "
                  "pricing, no gates) ran before the credited run and "
                  "was discarded"),
              "sections": sections,
              "gates": gates,
              "verdict": verdict,
              "wall_s": round(time.time() - t0, 1)}

    os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1, default=_jdefault,
                  allow_nan=False)
    print(f"  deposited {out_path} | wall {result['wall_s']} s")
    return result
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
