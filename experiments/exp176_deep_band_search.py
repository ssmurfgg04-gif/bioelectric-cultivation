#!/usr/bin/env python3
"""exp176 — DEEP-BAND GENERATOR SEARCH (the search sent to the band).

exp172's registered next (L151): "the band is writable but the
GENERATOR has never BEEN SENT there — the search's own target
families have never carried a deep-band target; next: the
fresh-search end-to-end with deep-band target families (the exp168
B3 pipeline verbatim, targets at the deep rungs, bars re-derived),
which tests whether the search's selection machinery VALUES the
widened band or the band's writability stays dormant until targets
ask for it".

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Pipeline, targets, and gates are fixed now.

THE PIPELINE (exp168's B3, verbatim, ONE swapped input):
  exp150's pipeline VERBATIM — the 72-member library with N*_lib
  re-derived (bar 82.288), the splice family 48,564 with N*_splice
  re-derived via exp146's splice_family_bar (bar 20.140), exp141's
  search loop at seed 141, the funnel (lib-novel -> splice-clear),
  N*_pool re-derived before selection (bar 33.776), exp165's R_W
  pre-emission exclusion clause, cap 10, ERR_BAR 6.0, audit seeds
  (1, 2, 3). THE ONE SWAPPED INPUT: the TARGET FAMILIES — the
  delivered cohort's decode/hold targets are exp172's deep-band
  constructions (MULTI 3-zone programs with zone values at the DEEP
  rungs {-40, -50, -60}, 3 targets x 10 translated instances... the
  target SET = 3 programs, one per rung, instance 0 translations —
  the same construction exp172 deposited; the search scores members
  against the deep targets where exp150's scored against its own).
  Library/splice/pool bars are TARGET-INDEPENDENT (structure bars) —
  they are re-derived and asserted at the deposited values.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-G1 (pipeline integrity at the swapped targets) the bars
           re-derive at the deposited values: N*_lib 82.288,
           N*_splice 20.140, N*_pool 33.776 (float equality at the
           deposited precision); the search loop at seed 141 is
           BIT-IDENTICAL to exp141's deposit through the funnel
           (the search's selection does not consult the targets —
           if it does, the divergence is the finding, deposited).
  GATE-G2 (delivery at the band) the delivered cohort (up to 10)
           decodes the DEEP targets: decode < 6.0 AND hold < 6.0 on
           3/3 seeds for >= 9/10 delivered members (the C3 clause
           at the deep targets); zero rejections; emission mode
           repriced_full (audit_only_fallback never fires).
  GATE-G3 (the band is VALUED, not just writable) the delivered
           members' emitted rungs reach the deep band: >= 1
           delivered member carries >= 1 emitted rung value in
           [-60, -35) (the search USES the widened repertoire when
           the targets ask for it — the dormancy question answered
           NO); the count of delivered members with deep rungs
           deposited.
  GATE-G4 (R_W discipline at the band) the production-floor R_W-
           positive set over the eligible pool is empty and equals
           the excluded set (exp168's B4 at the swapped targets);
           zero false exclusions.

NO post-hoc tuning. A --smoke check (library bar re-derivation only,
no search) is permitted before the credited run and discarded.
Wall budget: the exp168 B3 credited run took 178.1 s locally; the
runner split carries the per-rung jobs.

DEPOSIT: results/exp176_deep_band_search.json

RUN:
  python3 -m experiments.exp176_deep_band_search            # full
  python3 -m experiments.exp176_deep_band_search --smoke    # check
  python3 -m experiments.exp176_deep_band_search --rung -50.0
  # jobs: bars | d40 | d50 | d60
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
DEEP_RUNGS = [-40.0, -50.0, -60.0]
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141
BAR_LIB = 82.288
BAR_SPLICE = 20.140
BAR_POOL = 33.776

OUT = os.path.join(ROOT, "results", "exp176_deep_band_search.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP168 = os.path.join(ROOT, "results", "exp168_cf1_production.json")


def main() -> dict:
    # ==== BODY (written by the run agent; docstring/imports/constants
    # above byte-unchanged — exp174's body-only discipline) ============
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "d40", "d50", "d60",
                                      "all"], default="all")
    ap.add_argument("--rung", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    # ---- exp168's B3 import block, verbatim (BLAS pin included) ------
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import contextlib
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
    PROD_FLOOR = -60.0                    # CF-1's production value
    OLD_FLOOR = -35.0                     # the pre-CF-1 pin (census only)

    # ---- instrument check: the production core in situ ---------------
    floors = {"CORE": CORE.NEURAL_SPEC_MIN,
              "M136": M136.NEURAL_SPEC_MIN,
              "M156": M156.NEURAL_SPEC_MIN}
    assert all(v == PROD_FLOOR for v in floors.values()), \
        f"production floor drift: {floors}"

    @contextlib.contextmanager
    def old_floor_pin():
        """exp168's value-pinning mechanism, verbatim semantics (used
        ONLY for the B4 census rows; save/restore asserted)."""
        mods = (CORE, M136, M156)
        saved = [m.NEURAL_SPEC_MIN for m in mods]
        assert all(v == PROD_FLOOR for v in saved), \
            "core is not at the patched floor when pinning"
        for m in mods:
            m.NEURAL_SPEC_MIN = OLD_FLOOR
        try:
            yield
        finally:
            for m, v in zip(mods, saved):
                m.NEURAL_SPEC_MIN = v
            assert all(m.NEURAL_SPEC_MIN == PROD_FLOOR
                       for m in mods), "floor restore failed"

    def deep_target(rung: float):
        """THE ONE SWAPPED INPUT: exp172's deep-band construction at
        `rung`, instance 0 (the MULTI 3-zone program verbatim — every
        MULTI zone value forced to the rung), built by exp94's
        spec_target_n machinery. Returns f (the decode/hold target),
        the program triples, canon."""
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
    # THE B3 PIPELINE (exp168's fresh_search sections 0-6, verbatim;
    # target-independent by construction — G1's clause)
    # ==================================================================
    def run_pipeline() -> dict:
        canon = wildtype_target(LAT_N)

        # ---- 0. frozen library + N*_lib (verbatim) ------------------
        lib = build_library()
        lib_names = list(lib)
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
        dep150 = json.load(open(DEP150))
        funnel_identity = {
            "pool": len(pool) == dep150["funnel"]["pool"],
            "lib_novel":
                len(eligible) == dep150["funnel"]["lib_novel"],
            "splice_clear":
                len(splice_clear) == dep150["funnel"]["splice_clear"]}
        assert all(funnel_identity.values()), \
            "funnel counts drifted from the deposited funnel"

        # ---- 5. R_W census over the eligible stream (G4 data) --------
        rw_rows = []
        for i, r in enumerate(eligible):
            with old_floor_pin():
                m_old = clash_mass(r["f"], canon)
                pos_old = bool(r_w_predict(r["f"], canon))
            m_new = clash_mass(r["f"], canon)    # production floor
            pos_new = bool(r_w_predict(r["f"], canon))
            rw_rows.append({"splice_clear": bool(r["nov_splice"]
                                                 > n_star_splice),
                            "clash_mass_production_mV2": round(m_new, 3),
                            "r_w_positive_production": pos_new,
                            "clash_mass_old_floor_mV2": round(m_old, 3),
                            "r_w_positive_old_floor": pos_old})
            r["_rw_pos_production"] = pos_new
        rw_pos_prod = {i for i, x in enumerate(rw_rows)
                       if x["r_w_positive_production"]}
        rw_pos_old = {i for i, x in enumerate(rw_rows)
                      if x["r_w_positive_old_floor"]}
        print(f"  R_W census over {len(eligible)} eligible: "
              f"production-floor positives {len(rw_pos_prod)} | "
              f"old-floor positives {len(rw_pos_old)} (max mass "
              f"old-floor {max(x['clash_mass_old_floor_mV2'] for x in rw_rows):.3f} mV^2)")

        # ---- 6. delivery: greedy with the R_W pre-emission clause ----
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
                    continue                   # R_W pre-emission filter
                if r["nov_splice"] <= n_star_splice:
                    continue                   # exp146's clause, kept
                if any(dist(r["f"], d["f"]) <= bar for d in dlist):
                    continue                   # C4 filter at `bar`
                dlist.append(r)
            return dlist, excluded_rw

        delivered, excluded_rw = greedy(n_star_pool)  # C4@N*_pool + R_W
        old_rule, _ = greedy(n_star_lib)              # cross-check
        old_keys = [zkey_of(r["zones"]) for r in old_rule]
        exp146_keys = [zkey_of(d["zones"]) for d in prev146["delivered"]]
        assert old_keys == exp146_keys, \
            "old-rule re-delivery does not reproduce exp146's 7 — " \
            "pipeline drift"
        print(f"  delivery (C4 @ N*_pool + R_W pre-filter): "
              f"{len(delivered)}/{N_DELIVER} | old-rule cross-check "
              f"reproduces exp146's 7: True")

        # ---- 9. funnel census vs exp150's delivered-10 + exp168 B3 ---
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
                  "note": ("the search's selection never consulted the "
                           "targets — the delivered cohort is the "
                           "deposited B3 cohort bit-identically"
                           if fresh_keys == exp150_keys == b3_keys else
                           "the delivery diverged from the deposited "
                           "cohort — see keys")}

        # ---- B4/G4: R_W pre-filter discipline ------------------------
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
                "rw_pos_old_floor": sorted(rw_pos_old),
                "delivered": delivered,
                "excluded_by_rw": excluded_rw,
                "excluded_names": excluded_names,
                "delivered_rw_negative": delivered_rw_negative,
                "shadow_pricing": shadow,
                "false_exclusions": false_exclusions,
                "census_vs_exp150": census}

    # ==================================================================
    # THE SWAPPED STAGE: pricing the delivered cohort AGAINST THE DEEP
    # TARGETS (exp150's price_rung + emit_rung VERBATIM at the
    # production cell; the ONLY changed argument is the target profile
    # f — the member's own program zones stay; exp150 scored members
    # against their own profile).
    # ==================================================================
    def price_rung_deep(rung: float, delivered: list) -> dict:
        f_deep, triples, _canon = deep_target(rung)
        checksum = hashlib.sha256(f_deep.tobytes()).hexdigest()[:16]
        print(f"  deep target rung {rung}: zones {triples} | f sha256 "
              f"{checksum} | n_below_-35 cells "
              f"{int((f_deep < -35.0).sum())}")
        rows = []
        for k, r in enumerate(delivered):
            tbl = [price_rung(f_deep, r["zones"], 1.0, 0.0)]
            e_new, mode = emit_rung(tbl)
            t = tbl[0]
            assert t["cell"] == [1.0, 0.0]
            rows.append({
                "member": f"d-{k + 1:02d}", "rung": rung,
                "cell": [1.0, 0.0], "seeds": list(AUDIT_SEEDS),
                "zones": [list(z) for z in r["zones"]],
                "audit_pass": bool(t["pass"]), "quad": t["quad"],
                "eV": t["eV"], "eT": t["eT"], "silent": t["silent"],
                "decode_errs": t["decode_errs"],
                "hold_errs": t["hold_errs"],
                "decode_err_mean": t["decode_err_mean"],
                "hold_err_mean": t["hold_err_mean"],
                "decode_stable_seeds": t["decode_stable_seeds"],
                "n_ok": int(t["n_ok"]), "dec333": bool(t["dec333"]),
                "full_valid": bool(t["full_valid"]),
                "n_rejected": int(t["n_rejected"]),
                "emission_mode": mode,
                "emitted_cell": (e_new["cell"] if e_new else None),
                "c3_at_deep_target": bool(t["n_ok"] == len(AUDIT_SEEDS))})
            print(f"  deep-price[{rung:g}] d-{k + 1:02d}: audit "
                  f"{t['pass']} quad {t['quad']} decode "
                  f"{t['decode_errs']} hold {t['hold_errs']} "
                  f"({t['decode_stable_seeds']}) mode {mode} "
                  f"rej {t['n_rejected']}")
        return {"rung": rung,
                "target": {
                    "construction": ("exp172's deep-band construction, "
                                     "instance 0: the MULTI 3-zone "
                                     "program (exp94), every zone value "
                                     "forced to the rung; "
                                     "f = spec_target_n(spec, canon, "
                                     "100), canon = labeling_bfs_n("
                                     "A_CHAIN) == wildtype_target(100) "
                                     "asserted"),
                    "triples": [list(t) for t in triples],
                    "f_sha256_16": checksum},
                "decode_instrument": (
                    "exp136_generator_v6.decode VERBATIM via exp150's "
                    "price_rung at the production cell (1.0, 0.0), "
                    "seeds (1,2,3); the ONE swapped input is the "
                    "target profile f (the deep construction) — the "
                    "member's own program zones stay"),
                "rows": rows}

    def evaluate_g2(sections: dict) -> dict:
        """G2 on the merged per-rung sections. Reading (fixed here,
        disclosed in the clause): the C3 clause per member AT THE DEEP
        TARGETS = decode < 6.0 AND hold < 6.0 on 3/3 seeds at EVERY
        deep rung of the target set {3 programs, one per rung}; the
        gate asks for >= 9/10 such members, zero rejections, and every
        (member, rung) emission mode repriced_full."""
        rung_secs = [sections.get(f"rung_{r:g}") for r in DEEP_RUNGS]
        present = [s for s in rung_secs if s is not None]
        rows = [row for s in present for row in s["rows"]]
        per_rung_counts = {f"{s['rung']:g}":
                           sum(int(r["c3_at_deep_target"])
                               for r in s["rows"])
                           for s in present}
        members = sorted(set(r["member"] for r in rows))
        members_all = sum(
            1 for m in members
            if all(r["c3_at_deep_target"] for r in rows
                   if r["member"] == m) and
            len([r for r in rows if r["member"] == m])
            == len(DEEP_RUNGS))
        n_rej = sum(r["n_rejected"] for r in rows)
        modes = sorted(set(r["emission_mode"] for r in rows))
        complete = len(present) == len(DEEP_RUNGS)
        ok = bool(complete and members_all >= 9 and n_rej == 0
                  and modes == ["repriced_full"])
        return {"gate": "G2", "clause": (
            "the delivered cohort (up to 10) decodes the DEEP targets: "
            ">= 9/10 delivered members with decode < 6.0 AND hold < "
            "6.0 on 3/3 seeds at EVERY deep rung {-40,-50,-60} (the "
            "C3 clause at the deep targets, member-level over the "
            "target set); zero rejections; emission mode "
            "repriced_full (audit_only_fallback never fires)"),
                "complete": complete,
                "per_rung_c3_counts": per_rung_counts,
                "members_passing_all_targets": members_all,
                "n_delivered": len(members),
                "rejections": n_rej,
                "emission_modes": modes,
                "rows_note": ("per-(member, rung) rows in "
                              "sections.rung_-40/-50/-60"),
                "pass": ok}

    # ---- dispatch ------------------------------------------------------
    print("=== exp176: THE DEEP-BAND GENERATOR SEARCH (the exp168 B3 "
          "pipeline verbatim, targets at the deep rungs) ===\n")
    if args.smoke:
        lib = build_library()
        n_star_lib, _ = library_nn_stats(lib)
        ok = round(n_star_lib, 3) == BAR_LIB
        print(f"  SMOKE (library bar re-derivation only, no search — "
              f"discarded): library {len(lib)} members | N*_lib "
              f"{n_star_lib:.3f} vs bar {BAR_LIB} -> "
              f"{'OK' if ok else 'DRIFT'}")
        dep = {"exp": "exp176_deep_band_search", "kind": "smoke",
               "discarded": True, "n_star_lib": n_star_lib,
               "bar": BAR_LIB, "ok": bool(ok)}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                        exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(dep, fh, indent=1, default=float)
        return dep

    rung_of = {"d40": -40.0, "d50": -50.0, "d60": -60.0}
    if args.rung is not None:
        jobs = [("rung", float(args.rung))]
    elif args.job == "all":
        jobs = [("bars", None)] + [("rung", r) for r in DEEP_RUNGS]
    elif args.job == "bars":
        jobs = [("bars", None)]
    else:
        jobs = [("rung", rung_of[args.job])]

    # merged deposit: split runs accumulate sections across invocations
    result: dict = {}
    if args.job != "all" and os.path.exists(out_path):
        with open(out_path) as fh:
            result = json.load(fh)
    result.setdefault("sections", {})
    result.setdefault("gates", {})

    pipe = None
    for kind, rung in jobs:
        if pipe is None:
            pipe = run_pipeline()
        if kind == "bars":
            delivered = pipe["delivered"]
            deep_flags = []
            for k, r in enumerate(delivered):
                deep_flags.append({
                    "member": f"d-{k + 1:02d}",
                    "zones": [list(z) for z in r["zones"]],
                    "carries_deep_rung": bool(any(
                        -60.0 <= v < -35.0 for (a, b, v) in r["zones"]))})
            n_deep = sum(int(x["carries_deep_rung"])
                         for x in deep_flags)
            result["sections"]["pipeline"] = {
                "bars": pipe["bars"],
                "bars_deposited_before_selection":
                pipe["bars_deposited_before_selection"],
                "search_replication": pipe["search_replication"],
                "harness_max_abs_diff": pipe["harness_max_abs_diff"],
                "funnel": pipe["funnel"],
                "funnel_identity": pipe["funnel_identity"],
                "rw_census": pipe["rw_census"],
                "rw_pos_production": pipe["rw_pos_production"],
                "rw_pos_old_floor": pipe["rw_pos_old_floor"],
                "excluded_by_rw": pipe["excluded_by_rw"],
                "shadow_pricing": pipe["shadow_pricing"],
                "census_vs_exp150": pipe["census_vs_exp150"],
                "delivered_deep_rung_flags": deep_flags,
                "n_delivered_with_deep_rungs": n_deep}
            # G1 (bars re-derive + search bit-identical through the
            # funnel), G3 (the band is VALUED), G4 (R_W discipline)
            result["gates"]["G1"] = {
                "gate": "G1", "clause": (
                    "the bars re-derive at the deposited values: N*_lib "
                    "82.288, N*_splice 20.140, N*_pool 33.776 (float "
                    "equality at the deposited precision); the search "
                    "loop at seed 141 is BIT-IDENTICAL to exp141's "
                    "deposit through the funnel (the search's selection "
                    "does not consult the targets — a divergence would "
                    "be the finding, deposited)"),
                "bars": pipe["bars"],
                "bars_float_equal": bool(
                    pipe["bars"]["n_star_lib"] == BAR_LIB
                    and pipe["bars"]["n_star_splice"] == BAR_SPLICE
                    and pipe["bars"]["n_star_pool"] == BAR_POOL),
                "rounds_match":
                    pipe["search_replication"]["rounds_match"],
                "pool_size_match":
                    pipe["search_replication"]["pool_size_match"],
                "funnel_identity": pipe["funnel_identity"],
                "pass": bool(
                    pipe["bars"]["n_star_lib"] == BAR_LIB
                    and pipe["bars"]["n_star_splice"] == BAR_SPLICE
                    and pipe["bars"]["n_star_pool"] == BAR_POOL
                    and pipe["search_replication"]["rounds_match"]
                    and pipe["search_replication"]["pool_size_match"]
                    and all(pipe["funnel_identity"].values()))}
            result["gates"]["G3"] = {
                "gate": "G3", "clause": (
                    "the delivered members' emitted rungs reach the "
                    "deep band: >= 1 delivered member carries >= 1 "
                    "emitted rung value in [-60, -35) (emitted rung "
                    "values = the delivered programs' zone voltages — "
                    "the search USES the widened repertoire when the "
                    "targets ask for it); the count of delivered "
                    "members with deep rungs deposited"),
                "n_members_with_deep_rungs": n_deep,
                "n_delivered": len(delivered),
                "flags": deep_flags,
                "pass": bool(n_deep >= 1)}
            excluded_names = pipe["excluded_names"]
            rw_pos_prod = pipe["rw_pos_production"]
            eligible_keys_note = ("set identity checked against the "
                                  "census indices")
            result["gates"]["G4"] = {
                "gate": "G4", "clause": (
                    "the production-floor R_W-positive set over the "
                    "eligible pool is empty and equals the excluded "
                    "set (exp168's B4 at the swapped targets); zero "
                    "false exclusions"),
                "n_rw_pos_production": len(rw_pos_prod),
                "n_excluded": len(excluded_names),
                "delivered_all_rw_negative":
                    pipe["delivered_rw_negative"],
                "false_exclusions": pipe["false_exclusions"],
                "census_note": eligible_keys_note,
                "pass": bool(
                    len(rw_pos_prod) == 0
                    and len(excluded_names) == 0
                    and pipe["delivered_rw_negative"]
                    and not pipe["false_exclusions"])}
        else:
            sec = price_rung_deep(rung, pipe["delivered"])
            result["sections"][f"rung_{rung:g}"] = sec
            if "G2" not in result["gates"]:
                g2 = evaluate_g2(result["sections"])
                if g2["complete"]:
                    result["gates"]["G2"] = g2

    npass = sum(int(g["pass"]) for g in result["gates"].values())
    for name in ("G1", "G2", "G3", "G4"):
        if name in result["gates"]:
            g = result["gates"][name]
            extra = ""
            if name == "G1":
                extra = (f" (bars {g['bars']}, rounds "
                         f"{g['rounds_match']}, pool "
                         f"{g['pool_size_match']})")
            elif name == "G2":
                extra = (f" ({g['members_passing_all_targets']}/"
                         f"{g['n_delivered']} members pass all targets"
                         f", per-rung {g['per_rung_c3_counts']}, rej "
                         f"{g['rejections']}, modes "
                         f"{g['emission_modes']})"
                         if g["complete"] else " (incomplete)")
            elif name == "G3":
                extra = f" ({g['n_members_with_deep_rungs']}/" \
                        f"{g['n_delivered']} carry deep rungs)"
            elif name == "G4":
                extra = (f" (R_W-positive {g['n_rw_pos_production']}, "
                         f"excluded {g['n_excluded']}, false "
                         f"{len(g['false_exclusions'])})")
            print(f"  GATE-{name}: {'PASS' if g['pass'] else 'REFUTE'}"
                  f"{extra}")
    verdict = (f"{npass}/{len(result['gates'])} gates "
               f"({' '.join(k for k in ('G1', 'G2', 'G3', 'G4')
                            if k in result['gates'])})")
    print(f"  === {verdict} ===")

    result.update({
        "exp": "exp176_deep_band_search",
        "claim": ("THE DEEP-BAND GENERATOR SEARCH (exp172's registered "
                  "next, L151): the fresh-search end-to-end (exp168's "
                  "B3 pipeline VERBATIM — library/splice/pool bars "
                  "re-derived, exp141's loop at seed 141, the funnel, "
                  "the R_W pre-emission clause, cap 10) with the ONE "
                  "swapped input — the delivered cohort's decode/hold "
                  "targets are exp172's deep-band constructions (MULTI "
                  "3-zone programs at the deep rungs {-40,-50,-60}, "
                  "instance 0, exp94's spec_target_n), decoded via "
                  "exp136.decode at the production cell (1.0, 0.0), "
                  "seeds (1,2,3) — which tests whether the search's "
                  "selection machinery VALUES the widened band or the "
                  "band's writability stays dormant until targets ask "
                  "for it"),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration; gates G1-G4 fixed "
                             "there, each evaluated exactly once)"),
            "gates": ["G1 bars re-derive (82.288 / 20.140 / 33.776, "
                      "float equality at deposited precision) + the "
                      "search bit-identical to exp141 through the "
                      "funnel",
                      "G2 the delivered cohort decodes the DEEP "
                      "targets (C3 clause: decode<6 AND hold<6 on 3/3 "
                      "seeds, >= 9/10 members; zero rejections; "
                      "emission repriced_full)",
                      "G3 >= 1 delivered member carries >= 1 emitted "
                      "rung value in [-60, -35); the count deposited",
                      "G4 the production-floor R_W-positive set empty "
                      "and equal to the excluded set; zero false "
                      "exclusions"],
            "swapped_input": ("the target families only: exp172's "
                              "deep-band constructions, target SET = "
                              "3 programs (one per rung, instance 0 "
                              "translations)"),
            "structure": ("exp168's B3 pipeline verbatim: its imports, "
                          "search loop and bars; the pricing stage "
                          "reuses exp150's price_rung/emit_rung "
                          "VERBATIM with the swapped target profile f "
                          "at the single production cell (1.0, 0.0)")},
        "smoke_disclosure": ("a --smoke check (library bar "
                             "re-derivation only, no search) ran "
                             "before the credited run and was "
                             "discarded (no file)"),
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
    ap.add_argument("--job", choices=["bars", "d40", "d50", "d60",
                                      "all"], default="all")
    ap.add_argument("--rung", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--rung/--out)
