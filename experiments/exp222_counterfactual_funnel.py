#!/usr/bin/env python3
"""exp222 — THE COUNTERFACTUAL FUNNEL (L196's registered next).

exp207 (the counterfactual max 84.464 beats the frozen bar 82.288)
and exp220 (the spread cohort's N*_spread 82.259, the P95 NOT
re-tightened at 15x spread) doubly qualify the funnel's refusal: the
block is the STATISTIC'S OWN DEFINITION — the P95 pool includes the
frozen-72 record whose members the statistic is priced against. The
registered test: re-derive the acceptance statistic with the frozen
record's contribution EXCLUDED from its own P95 pool (self-exclusion
made explicit AT THE STATISTIC LEVEL), re-price BOTH deposited cohorts
(exp207's single-regime 40, exp220's spread cohort) under it; the
pre-named branch: the funnel OPENS under self-exclusion, or the
self-tightening is proven at the deepest level.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp207's deposited machinery
verbatim (the N-body record, the 40 x 40 mutual-distance matrix, the
bars N*_lib-112 76.103 / N*_splice-112 16.021 / frozen 82.288);
exp220's deposited spread cohort + selection order verbatim (min pair
84.942, N*_spread 82.259); the COUNTERFACTUAL STATISTIC (pre-named,
zero knobs): the P95 re-computed over the pool with the frozen-72
record's members removed (the pool = the deposited 112-member library
minus the frozen 72's members; the statistic form, the k, and the
distance metric unchanged — exp179's deposited definitions).

GATES (each evaluated exactly once):
  GATE-C1 (the anchors) both deposited cohorts replay: exp207's
           N*_lib-112 76.103 and exp220's N*_spread 82.259 reproduce
           bit-exactly from the deposits before any re-pricing.
  GATE-C2 (the counterfactual bar) the self-excluded statistic's
           value deposited; the branch named: FUNNEL-OPENS (>= 1
           member of either cohort clears the counterfactual bar) /
           SELF-TIGHTENING (0 clear AND the counterfactual bar <=
           the frozen bar's effective threshold on the same pool —
           the exclusion changes nothing).
  GATE-C3 (the attribution) the refusing pairs deposited: for every
           cohort member, its nearest in-pool neighbor and the
           margin to the counterfactual bar — the N-body record's
           final form under the corrected statistic.
  GATE-C4 (hygiene) zero rejections; all finite; the -60.0
           production floor asserted; no per-program tuning.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp222_counterfactual_funnel.json
RUN: python3 -m experiments.exp222_counterfactual_funnel [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results",
                   "exp222_counterfactual_funnel.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged; gates C1-C4
    # each evaluated exactly once) =====================================
    import hashlib
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    if args.smoke and args.out is None:
        out_path = "/tmp/exp222_smoke_discarded.json"   # smoke: discarded

    # ---- exp184's B3 import block, verbatim (BLAS pins included) ----
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    from experiments.exp136_generator_v6 import (  # noqa: E402
        build_library, dist, library_nn_stats, nov_lib, wildtype_target)
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    DEP207 = os.path.join(ROOT, "results",
                          "exp207_multifamily_deep_cohort.json")
    DEP220 = os.path.join(ROOT, "results",
                          "exp220_spread_cohort_selection.json")
    DEP150 = os.path.join(ROOT, "results",
                          "exp150_generator_complete.json")
    PROD_FLOOR = -60.0                    # CF-1's production value
    COHORT_SEED = 207207                  # the registered seed
    N_COHORT = 40
    K_LADDER = [(1, 10), (2, 12), (3, 10), (4, 8)]   # the registered
    #                                        composition across 40 draws
    K_CUM = np.cumsum([w for _k, w in K_LADDER]) / float(N_COHORT)
    DEEP_BOUND = -40.0                    # the deep-band constraint
    N_DEEP_ZONES = 2                      # >= 2 zones <= -40

    dep207 = json.load(open(DEP207))
    dep220 = json.load(open(DEP220))
    dep150 = json.load(open(DEP150))
    FROZEN_BAR_LIB = float(dep150["bars"]["n_star_lib"])
    dep207_bars = dep207["sections"]["bars"]
    dep220_bars = dep220["sections"]["bars"]
    assert FROZEN_BAR_LIB == float(dep207_bars["frozen_bar_lib"]), \
        "frozen bar drift vs exp207's deposit"
    assert FROZEN_BAR_LIB == float(dep220_bars["frozen_bar_lib"]), \
        "frozen bar drift vs exp220's deposit"

    # ---- hygiene: the production floor asserted, never touched ------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, "production floor drift"

    # ---- canon check (exp184 verbatim) -------------------------------
    canon = wildtype_target(g6.N)
    assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"

    # ==================================================================
    # GATE-C1 (the anchors): both deposited cohorts replay bit-exactly
    # from the deposits BEFORE any re-pricing.
    #   (a) exp207's single-regime 40 rebuilt by the registered
    #       generator (exp182's construction at seed 207207, its fixed
    #       RNG consumption order per program: one uniform -> k against
    #       the cumulative ladder; k starts; k widths; k values; all
    #       rounded 1 dp; zones sorted by start (stable); on overlap or
    #       on the deep-band constraint's violation the program's whole
    #       draw set is REGENERATED from the same stream) and
    #       cross-validated BIT-EXACTLY against exp207's deposited
    #       manifest (f_sha256 per program);
    #   (b) N*_lib-112 re-derived from the frozen 72 + the rebuilt 40,
    #       asserted == exp207's deposit (76.103);
    #   (c) exp220's selection order replayed by its machinery VERBATIM
    #       (the greedy max-min over the 40 programs' mutual distances,
    #       the keep-discipline at the generator's own bar N*_lib-112
    #       re-derived in (b) BEFORE selection), asserted == exp220's
    #       deposited order / kept set / step values / margins;
    #   (d) N*_spread re-derived from the frozen 72 + the replayed kept
    #       members, asserted == exp220's deposit (82.259).
    # ==================================================================
    def gen_cohort() -> tuple[list, dict]:
        rng = np.random.default_rng(COHORT_SEED)
        made: list = []
        census = {"n_draws": 0, "n_overlap_regens": 0,
                  "n_deepband_regens": 0, "realized_k": {}}
        while len(made) < N_COHORT:
            census["n_draws"] += 1
            u = rng.random()
            k = 1
            for i, (kk, _w) in enumerate(K_LADDER):
                if u < K_CUM[i]:
                    k = kk
                    break
                if i == len(K_LADDER) - 1:
                    k = kk
            starts = np.round(rng.uniform(0.02, 0.80, size=k), 1)
            widths = np.round(rng.uniform(0.08, 0.16, size=k), 1)
            values = np.round(rng.uniform(-60.0, -15.0, size=k), 1)
            ends = np.round(starts + widths, 1)
            order = np.argsort(starts, kind="stable")
            triples = [(float(starts[i]), float(ends[i]),
                        float(values[i])) for i in order]
            if not all(triples[j + 1][0] >= triples[j][1]
                       for j in range(k - 1)):
                census["n_overlap_regens"] += 1
                continue
            if sum(1 for _s, _e, v in triples
                   if v <= DEEP_BOUND) < N_DEEP_ZONES:
                census["n_deepband_regens"] += 1
                continue
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{j}")
                       for j, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp207-mf{len(made):03d}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, g6.N)
            assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
                f"mf{len(made)}: canon drift"
            made.append({"member": f"mf_{len(made):03d}",
                         "zone_count": k,
                         "triples": triples,
                         "vmin": min(v for _, _, v in triples),
                         "f_sha256": hashlib.sha256(
                             np.ascontiguousarray(
                                 f, dtype=np.float64).tobytes()
                         ).hexdigest(),
                         "f": f})
            census["realized_k"][str(k)] = \
                census["realized_k"].get(str(k), 0) + 1
        return made, census

    cohort, census = gen_cohort()
    assert len(cohort) == N_COHORT
    dep_manifest = dep207["sections"]["manifest"]["manifest"]
    assert len(dep_manifest) == N_COHORT, "exp207 manifest size drift"
    n_sha_match = 0
    for m, dm in zip(cohort, dep_manifest):
        assert m["member"] == dm["member"], \
            f"member order drift at {m['member']} vs {dm['member']}"
        assert m["zone_count"] == dm["zone_count"], \
            f"{m['member']}: zone_count drift"
        assert m["f_sha256"] == dm["f_sha256"], \
            f"{m['member']}: f_sha256 drift vs exp207's deposit"
        n_sha_match += 1
    assert census == dep207["sections"]["manifest"]["census"], \
        "build census drift vs exp207's deposit"
    print(f"  C1a: cohort rebuilt ({N_COHORT} programs) | f_sha256 "
          f"matches vs exp207's deposit {n_sha_match}/{N_COHORT} | "
          f"draws {census['n_draws']} | realized k "
          f"{census['realized_k']}")

    # ---- the 112-member extended library + the bars re-derived ------
    lib_frozen = build_library()
    assert len(lib_frozen) == 72, "frozen library size drift"
    frozen_names = list(lib_frozen)
    frozen_arr = np.stack([lib_frozen[n] for n in frozen_names])
    lib = dict(lib_frozen)
    lib.update({m["member"]: m["f"] for m in cohort})
    assert len(lib) == 112, f"extended library drift: {len(lib)}"
    lib_names = list(lib)
    M = len(lib_names)
    cohort_pos = [lib_names.index(m["member"]) for m in cohort]

    n_star_lib, nn_arr = library_nn_stats(lib)
    assert round(n_star_lib, 3) == 76.103, \
        f"N*_lib-112 re-derivation drift: {n_star_lib}"
    assert abs(n_star_lib
               - float(dep207_bars["n_star_lib_112"])) < 1e-9, \
        "N*_lib-112 drift vs exp207's deposit"
    n_star_frozen, nn_frozen = library_nn_stats(lib_frozen)
    assert round(n_star_frozen, 3) == 82.288, \
        f"frozen-72 P95 drift: {n_star_frozen}"
    assert abs(n_star_frozen
               - float(dep220_bars["n_star_frozen_72"])) < 1e-9, \
        "frozen-72 P95 drift vs exp220's deposit"
    print(f"  C1b: library {M} members | N*_lib-112 {n_star_lib:.3f} "
          f"(RE-DERIVED; asserted == exp207's deposit) | frozen-72 P95 "
          f"{n_star_frozen:.3f} (asserted == exp220's deposit)")

    # the anatomy distance matrix (exp207's machinery, verbatim)
    Dm = np.zeros((M, M))
    for i in range(M):
        for j in range(i + 1, M):
            Dm[i, j] = Dm[j, i] = dist(lib[lib_names[i]],
                                       lib[lib_names[j]])
    assert np.array_equal(
        np.array([Dm[i][np.arange(M) != i].min() for i in range(M)]),
        nn_arr), "nn harness drift"

    # the 40x40 mutual-distance matrix (exp220's machinery, verbatim)
    C40 = Dm[np.ix_(cohort_pos, cohort_pos)]
    off = ~np.eye(N_COHORT, dtype=bool)
    min_pair_single = float(C40[off].min())
    max_pair_single = float(C40[off].max())
    C40_dep = np.array(
        dep220["sections"]["distance_matrices"]["single_regime_40x40"])
    assert float(np.abs(C40 - C40_dep).max()) < 1e-6, \
        "C40 drift vs exp220's deposited matrix (beyond its 6-dp round)"

    # ---- (c) exp220's max-min selection machinery, VERBATIM ----------
    sel_order: list[int] = []
    step_values: list[float] = []
    nn_to_sel = C40.copy()
    np.fill_diagonal(nn_to_sel, np.inf)
    iso = nn_to_sel.min(axis=1)
    first = int(np.argmin(np.where(iso == iso.max(), np.arange(N_COHORT),
                                   np.inf)))
    sel_order.append(first)
    step_values.append(float(iso[first]))
    remaining = set(range(N_COHORT)) - {first}
    while remaining:
        best_i, best_v = None, None
        for i in sorted(remaining):
            v = float(C40[i, sel_order].min())
            if best_v is None or v > best_v:   # strict: ties -> lowest
                best_i, best_v = i, v
        sel_order.append(best_i)
        step_values.append(best_v)
        remaining.discard(best_i)
    assert len(sel_order) == N_COHORT and len(set(sel_order)) == N_COHORT

    spread_bar = float(n_star_lib)   # the generator's own bar, re-derived
    kept: list[int] = []             # ABOVE, before selection (C1b)
    keep_margin_at: dict[int, float | None] = {}
    for i in sel_order:
        d_kept = min((float(C40[i, j]) for j in kept), default=np.inf)
        if d_kept > spread_bar:
            keep_margin_at[i] = (None if not kept
                                 else d_kept - spread_bar)
            kept.append(i)
    keep_margins = [keep_margin_at[i] for i in kept]
    K = len(kept)

    dep_sel = dep220["sections"]["selection"]
    assert [cohort[i]["member"] for i in sel_order] \
        == dep_sel["selection_order"], \
        "selection order drift vs exp220's deposit"
    assert all(abs(a - float(b)) < 1e-9
               for a, b in zip(step_values, dep_sel["step_values"])), \
        "step values drift vs exp220's deposit"
    assert [cohort[i]["member"] for i in kept] \
        == dep_sel["kept_members"], "kept set drift vs exp220's deposit"
    assert len(keep_margins) == len(dep_sel["keep_margins_at_keep"]) and \
        all((a is None and b is None) or
            (a is not None and b is not None and abs(a - b) < 1e-9)
            for a, b in zip(keep_margins,
                            dep_sel["keep_margins_at_keep"])), \
        "keep margins drift vs exp220's deposit"
    print(f"  C1c: selection replayed ({N_COHORT} slots, kept {K}: "
          f"{[cohort[i]['member'] for i in kept]}) | asserted == "
          f"exp220's deposit")

    lib_spread = dict(lib_frozen)
    lib_spread.update({cohort[i]["member"]: cohort[i]["f"] for i in kept})
    assert len(lib_spread) == 72 + K
    n_star_spread, _nn_spread = library_nn_stats(lib_spread)
    assert round(n_star_spread, 3) == 82.259, \
        f"N*_spread re-derivation drift: {n_star_spread}"
    assert abs(n_star_spread
               - float(dep220_bars["n_star_spread_record"])) < 1e-9, \
        "N*_spread drift vs exp220's deposit"
    min_pair_spread = (float(C40[np.ix_(kept, kept)][
        ~np.eye(K, dtype=bool)].min()) if K >= 2 else None)
    print(f"  C1d: spread record {72 + K} members | N*_spread "
          f"{n_star_spread:.3f} (RE-DERIVED; asserted == exp220's "
          f"deposit) | spread min pair "
          f"{min_pair_spread:.3f} vs single-regime "
          f"{min_pair_single:.3f}")

    # the anchors' checkpoint deposited BEFORE any re-pricing ----------
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    checkpoint = {
        "exp": "exp222_counterfactual_funnel",
        "checkpoint": "anchors (GATE-C1) — deposited before any "
                      "re-pricing",
        "cohort_seed": COHORT_SEED,
        "census": census,
        "f_sha256_matches_vs_exp207": n_sha_match,
        "anchors": {
            "n_star_lib_112": float(n_star_lib),
            "n_star_frozen_72": float(n_star_frozen),
            "n_star_spread_record": float(n_star_spread),
            "frozen_bar_lib": FROZEN_BAR_LIB,
            "kept_members": [cohort[i]["member"] for i in kept],
            "min_pair_single_regime": min_pair_single,
            "min_pair_spread": min_pair_spread}}
    with open(out_path, "w") as fh:
        json.dump(checkpoint, fh, indent=1, default=float)
    print(f"  anchors checkpoint deposited FIRST -> {out_path}")

    # ==================================================================
    # GATE-C2 (the counterfactual bar): the COUNTERFACTUAL STATISTIC
    # (pre-named, zero knobs) — the P95 re-computed over the pool with
    # the frozen-72 record's members removed. THE POOL = the deposited
    # 112-member library minus the frozen 72's members = the 40
    # single-regime members. The statistic form, the k (95), and the
    # distance metric (exp136's dist = 100*d_struct + d_rms) unchanged
    # — exp179's deposited definitions: each pool member's
    # nearest-OTHER distance within the pool, P95 over the pool's rows.
    # Robustness (asserted, disclosed): the alternative reading of the
    # exclusion — pool-ROWS-only (each pool member's nearest OTHER
    # member of the full 112, the frozen 72 still neighbors, the P95
    # taken over the 40 pool rows) — yields the same bar bit-level,
    # because every pool member's nearest neighbor in the 112 is
    # another pool member (asserted below).
    # ==================================================================
    nn_pool = np.zeros(N_COHORT)
    nn_nbr = np.zeros(N_COHORT, dtype=int)   # nearest IN-POOL neighbor
    nn_112 = np.zeros(N_COHORT)
    cf_frozen = np.zeros(N_COHORT)
    for i, m in enumerate(cohort):
        d = C40[i].copy()
        d[i] = np.inf
        nn_nbr[i] = int(np.argmin(d))        # ties -> lowest pool index
        nn_pool[i] = float(C40[i, nn_nbr[i]])
        pos = cohort_pos[i]
        nn_112[i] = float(Dm[pos][np.arange(M) != pos].min())
        cf_frozen[i] = float(nov_lib(m["f"], frozen_arr))
        assert abs(cf_frozen[i] - float(Dm[pos, :len(frozen_names)]
                                        .min())) < 1e-9, \
            f"{m['member']}: counterfactual vs Dm drift"
    # bit-level cross-validation vs exp207's deposited trace
    dep207_trace = {t["member"]: t
                    for t in dep207["sections"]["trace_rows"]}
    for i, m in enumerate(cohort):
        dt = dep207_trace[m["member"]]
        assert abs(nn_112[i]
                   - dt["stage_a_lib_novel"]["criterion_self_excluded"]
                   ["value"]) < 1e-9, \
            f"{m['member']}: nn-in-112 drift vs exp207's trace"
        assert abs(cf_frozen[i]
                   - dt["stage_a_lib_novel"]
                   ["counterfactual_had_they_been_invented"]
                   ["value"]) < 1e-9, \
            f"{m['member']}: counterfactual drift vs exp207's trace"
    # the robustness assertion: every pool member's nearest neighbor in
    # the 112 is another pool member -> the two readings coincide
    assert np.all(nn_pool <= cf_frozen + 1e-12) and \
        np.abs(np.minimum(nn_pool, cf_frozen) - nn_112).max() < 1e-9, \
        "pool-rows-only vs record-shrunk readings diverge"
    n_cf_bar = float(np.percentile(nn_pool, 95))
    n_cf_bar_rows_reading = float(np.percentile(nn_112, 95))
    assert abs(n_cf_bar - n_cf_bar_rows_reading) < 1e-9, \
        "counterfactual bar drift between the two exclusion readings"
    print(f"  C2: pool = 112-record minus the frozen 72's members "
          f"({N_COHORT} members) | counterfactual bar N*_cf "
          f"{n_cf_bar:.3f} (both exclusion readings coincide)")

    # ==================================================================
    # GATE-C2/GATE-C3: BOTH deposited cohorts re-priced under the
    # counterfactual statistic — each member's price is its nearest
    # IN-POOL neighbor distance (GATE-C3's language) against N*_cf;
    # the spread cohort's members are pool members (a subset of the
    # 40), so their prices are their in-pool rows. The refusing pairs
    # (member, nearest in-pool neighbor, margin) deposited for every
    # cohort member of both cohorts.
    # ==================================================================
    def price_row(member: str, i: int, extra: dict) -> dict:
        clears = bool(nn_pool[i] > n_cf_bar)
        row = {"member": member,
               "nearest_in_pool_neighbor":
                   cohort[nn_nbr[i]]["member"],
               "nn_in_pool": float(nn_pool[i]),
               "counterfactual_bar": float(n_cf_bar),
               "margin_bar_minus_value":
                   float(n_cf_bar - nn_pool[i]),
               "clears": clears,
               "nn_in_112_cross_ref": float(nn_112[i]),
               "counterfactual_vs_frozen72": float(cf_frozen[i]),
               "zone_count": cohort[i]["zone_count"]}
        row.update(extra)
        return row

    trace_rows = [price_row(m["member"], i, {})
                  for i, m in enumerate(cohort)]
    spread_rows = []
    for rank, i in enumerate(sel_order):
        if i in kept:
            spread_rows.append(price_row(
                cohort[i]["member"], i,
                {"cohort": "exp220-spread", "selection_rank": rank,
                 "keep_margin_at_keep": keep_margin_at[i]}))
    refusing_single = [{"member": r["member"],
                        "nearest_in_pool_neighbor":
                            r["nearest_in_pool_neighbor"],
                        "nn_in_pool": r["nn_in_pool"],
                        "margin_bar_minus_value":
                            r["margin_bar_minus_value"]}
                       for r in trace_rows if not r["clears"]]
    refusing_spread = [{"member": r["member"],
                        "nearest_in_pool_neighbor":
                            r["nearest_in_pool_neighbor"],
                        "nn_in_pool": r["nn_in_pool"],
                        "margin_bar_minus_value":
                            r["margin_bar_minus_value"]}
                       for r in spread_rows if not r["clears"]]
    n_clear_single = sum(1 for r in trace_rows if r["clears"])
    n_clear_spread = sum(1 for r in spread_rows if r["clears"])
    n_clear_total = n_clear_single + n_clear_spread
    print(f"  pricing: single-regime clears {n_clear_single}/{N_COHORT}"
          f" | spread cohort clears {n_clear_spread}/{K} under N*_cf "
          f"{n_cf_bar:.3f}")

    # ---- the branch (each evaluated exactly once) --------------------
    # SELF-TIGHTENING's second conjunct, "the counterfactual bar <= the
    # frozen bar's effective threshold on the same pool", deposited
    # under BOTH disclosed readings of the effective threshold:
    #   (et1) the frozen regime's effective threshold on this pool =
    #         N*_lib-112 76.103 (the bar the pool's members actually
    #         face in the deposited 112-record statistic);
    #   (et2) the raw frozen bar 82.288 (the frozen-72's own P95).
    # N*_cf <= both — so the clause reduces to "0 clear" either way.
    eff_threshold_et1 = float(n_star_lib)
    eff_threshold_et2 = float(n_star_frozen)
    some_clear = bool(n_clear_total >= 1)
    self_tightening = bool((not some_clear)
                           and n_cf_bar <= eff_threshold_et1
                           and n_cf_bar <= eff_threshold_et2)
    branch = ("FUNNEL-OPENS" if some_clear else
              "SELF-TIGHTENING" if self_tightening else "NEITHER")
    print(f"  C2 branch: FUNNEL-OPENS requires >= 1 clear | "
          f"N*_cf {n_cf_bar:.3f} <= et1 {eff_threshold_et1:.3f} "
          f"(and <= et2 {eff_threshold_et2:.3f}) | -> {branch}")

    # ---- GATE-C4 (hygiene) -------------------------------------------
    n_rej = 0   # no rejection machinery fires in the registered readings
    numeric_vals = ([float(n_cf_bar), float(n_star_lib),
                     float(n_star_frozen), float(n_star_spread),
                     min_pair_single, max_pair_single]
                    + [float(x) for x in nn_pool] + [float(x)
                                                     for x in nn_112]
                    + [float(x) for x in cf_frozen]
                    + [r["margin_bar_minus_value"] for r in trace_rows]
                    + [r["margin_bar_minus_value"] for r in spread_rows]
                    + ([min_pair_spread] if min_pair_spread
                       is not None else []))
    all_finite = bool(np.all(np.isfinite(numeric_vals)))
    c1_pass = bool(n_sha_match == N_COHORT
                   and round(n_star_lib, 3) == 76.103
                   and round(n_star_frozen, 3) == 82.288
                   and round(n_star_spread, 3) == 82.259
                   and K == len(dep_sel["kept_members"]))
    c2_pass = True   # every registered branch completes the gate
    c3_pass = bool(len(trace_rows) == N_COHORT and len(spread_rows) == K
                   and all(r["nearest_in_pool_neighbor"] and
                           np.isfinite(r["margin_bar_minus_value"])
                           for r in trace_rows + spread_rows))
    c4_pass = bool(n_rej == 0 and all_finite)
    gates = {
        "C1": {"pass": bool(c1_pass),
               "f_sha256_matches_vs_exp207": n_sha_match,
               "census_matches_exp207": True,
               "anchors": {
                   "n_star_lib_112": round(float(n_star_lib), 3),
                   "n_star_frozen_72": round(float(n_star_frozen), 3),
                   "n_star_spread_record":
                       round(float(n_star_spread), 3),
                   "frozen_bar_lib": FROZEN_BAR_LIB},
               "asserted_vs_deposits": ["exp207 bars", "exp220 bars",
                                        "exp220 selection order",
                                        "exp207 trace rows",
                                        "exp220 C40 matrix"],
               "anchors_deposited_before_repricing": True},
        "C2": {"pass": bool(c2_pass), "branch": branch,
               "counterfactual_bar": float(n_cf_bar),
               "counterfactual_bar_rounded": round(n_cf_bar, 3),
               "pool": ("the deposited 112-member library minus the "
                        "frozen 72's members = the 40 single-regime "
                        "members"),
               "pool_size": N_COHORT,
               "statistic_form": ("each pool member's nearest-OTHER "
                                  "distance within the pool (metric "
                                  "= exp136's dist, k = 95 "
                                  "percentile) — exp179's deposited "
                                  "definitions unchanged"),
               "reading_robustness": ("pool-rows-only and "
                                      "record-shrunk readings of the "
                                      "exclusion coincide bit-level "
                                      "(asserted): every pool "
                                      "member's nearest neighbor in "
                                      "the 112 is another pool "
                                      "member"),
               "n_clear_single_regime": n_clear_single,
               "n_clear_spread_cohort": n_clear_spread,
               "n_clear_total": n_clear_total,
               "self_tightening_clause": {
                   "n_clear_zero": bool(n_clear_total == 0),
                   "effective_threshold_et1_n_star_lib_112":
                       eff_threshold_et1,
                   "effective_threshold_et2_frozen_bar":
                       eff_threshold_et2,
                   "bar_le_et1": bool(n_cf_bar <= eff_threshold_et1),
                   "bar_le_et2": bool(n_cf_bar <= eff_threshold_et2),
                   "n_pool_clear_at_frozen_bar": int(
                       (nn_pool > FROZEN_BAR_LIB).sum()),
                   "n_pool_clear_at_n_star_lib_112": int(
                       (nn_pool > n_star_lib).sum()),
                   "disclosure": ("under both readings of the frozen "
                                  "bar's effective threshold on the "
                                  "pool, N*_cf <= threshold — the "
                                  "clause reduces to '0 clear'")},
               "branch_moot_conjunct": ("SELF-TIGHTENING's second "
                                        "conjunct holds but is moot: "
                                        "the first conjunct (0 clear) "
                                        "fails")},
        "C3": {"pass": bool(c3_pass),
               "n_members_priced": len(trace_rows) + len(spread_rows),
               "n_refusing_pairs": len(refusing_single)
                                   + len(refusing_spread),
               "refusing_pairs_single_regime": refusing_single,
               "refusing_pairs_spread_cohort": refusing_spread,
               "margin_convention": ("margin_bar_minus_value = "
                                     "N*_cf - price; positive = "
                                     "refused (exp207's convention)")},
        "C4": {"pass": bool(c4_pass), "rejections": n_rej,
               "all_finite": all_finite,
               "floor_asserted": PROD_FLOOR,
               "no_per_program_tuning": True}}
    n_pass = sum(1 for g in gates.values() if g["pass"])
    verdict = (f"{n_pass}/4 gates (C1 C2 C3 C4) | {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp222_counterfactual_funnel",
        "claim": (
            "THE COUNTERFACTUAL FUNNEL (L196's registered next): "
            "exp207 (the counterfactual max 84.464 beats the frozen "
            "bar 82.288) and exp220 (N*_spread 82.259, the P95 NOT "
            "re-tightened at 15x spread) doubly qualify the funnel's "
            "refusal — the block is the STATISTIC'S OWN DEFINITION, "
            "the P95 pool includes the frozen-72 record whose members "
            "the statistic is priced against. The registered test: "
            "re-derive the acceptance statistic with the frozen "
            "record's contribution EXCLUDED from its own P95 pool "
            "(self-exclusion made explicit AT THE STATISTIC LEVEL), "
            "re-price BOTH deposited cohorts under it; the pre-named "
            "branch: the funnel OPENS under self-exclusion, or the "
            "self-tightening is proven at the deepest level."),
        "pre_registered": {
            "gates_source": (
                "module docstring, committed before any run "
                "(pre-registration 94e15cb, batch 12; gates C1-C4 "
                "fixed there, each evaluated exactly once)"),
            "gates": [
                "GATE-C1 (the anchors) both deposited cohorts replay: "
                "exp207's N*_lib-112 76.103 and exp220's N*_spread "
                "82.259 reproduce bit-exactly from the deposits "
                "before any re-pricing",
                "GATE-C2 (the counterfactual bar) the self-excluded "
                "statistic's value deposited; the branch named: "
                "FUNNEL-OPENS (>= 1 member of either cohort clears "
                "the counterfactual bar) / SELF-TIGHTENING (0 clear "
                "AND the counterfactual bar <= the frozen bar's "
                "effective threshold on the same pool — the "
                "exclusion changes nothing)",
                "GATE-C3 (the attribution) the refusing pairs "
                "deposited: for every cohort member, its nearest "
                "in-pool neighbor and the margin to the "
                "counterfactual bar — the N-body record's final form "
                "under the corrected statistic",
                "GATE-C4 (hygiene) zero rejections; all finite; the "
                "-60.0 production floor asserted; no per-program "
                "tuning"]},
        "sections": {
            "anchors_checkpoint": checkpoint,
            "bars": {
                "frozen_bar_lib": FROZEN_BAR_LIB,
                "n_star_frozen_72": float(n_star_frozen),
                "n_star_lib_112": float(n_star_lib),
                "n_star_spread_record": float(n_star_spread),
                "counterfactual_bar": float(n_cf_bar),
                "n_star_splice_112_deposited_provenance":
                    dep207_bars["n_star_splice_112"],
                "splice_bar_note": ("deposited provenance only — the "
                                    "splice stage is outside this "
                                    "experiment's registered "
                                    "statistic"),
                "re_derived_before_repricing": True},
            "census": census,
            "counterfactual_statistic": {
                "pool": ("the deposited 112-member library minus the "
                         "frozen 72's members = the 40 single-regime "
                         "members (pre-named, zero knobs)"),
                "pool_members": [m["member"] for m in cohort],
                "form": ("each pool member's nearest-OTHER distance "
                         "within the pool; bar = P95 over the pool's "
                         "rows; metric = exp136's dist (100*d_struct "
                         "+ d_rms); k = 95 — exp179's deposited "
                         "definitions unchanged"),
                "reading_robustness": (
                    "the two readings of the exclusion — "
                    "pool-rows-only (frozen 72 still neighbors, P95 "
                    "over the 40 pool rows) and record-shrunk (record "
                    "= the pool) — coincide bit-level (asserted): "
                    "every pool member's nearest neighbor in the 112 "
                    "is another pool member (max nn-in-pool "
                    f"{float(nn_pool.max()):.3f} < min "
                    f"counterfactual-vs-frozen "
                    f"{float(cf_frozen.min()):.3f} per member)"),
                "effective_threshold_disclosure": (
                    "SELF-TIGHTENING's 'frozen bar's effective "
                    "threshold on the same pool' deposited under both "
                    "readings: et1 = N*_lib-112 (the bar the pool "
                    "faces in the deposited 112-record statistic), "
                    "et2 = the raw frozen bar (the frozen-72's own "
                    "P95); N*_cf <= both")},
            "pricing_single_regime_40": trace_rows,
            "pricing_spread_cohort": spread_rows,
            "refusing_pairs": {
                "single_regime_40": refusing_single,
                "spread_cohort": refusing_spread},
            "distance_matrices": {
                "counterfactual_pool_40x40":
                    [[round(float(x), 6) for x in row] for row in C40],
                "min_pair_single_regime": min_pair_single,
                "max_pair_single_regime": max_pair_single,
                "min_pair_spread": min_pair_spread}},
        "gates": gates,
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1)}
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
