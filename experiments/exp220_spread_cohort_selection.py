#!/usr/bin/env python3
"""exp220 — THE SPREAD-COHORT SELECTION ORDER (L188's registered next).

exp207's N-body finding: the funnel's refusal is the cohort's OWN
DENSITY (each program's nearest sibling sits inside the bar and the
P95 statistic re-tightens around every admission). The registered
question: can a DELIBERATELY SPREAD cohort — max-min selection over
the generator's space (exp179's greedy discipline at the generator's
own bars) — land even ONE member above the moving bar? If the bar
rises to meet every cohort, the funnel's novelty stage is PROVEN
self-tightening and the delivery question moves from construction to
SELECTION ORDER.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp207's build VERBATIM
(exp182's generator at the registered seed 207207, the ladder
{1:10, 2:12, 3:10, 4:8}/40, the deep-band constraint >= 2 zones
<= -40, canon asserted per program, the manifest deposited FIRST);
the bars re-derived BEFORE selection (N*_lib-112 76.103, N*_splice-112
16.021, the frozen bar 82.288 — asserted vs exp207's deposit);
exp179's greedy VERBATIM as the max-min selector: the spread cohort of
40 = the greedy max-min ordering over the 40 programs' pairwise
distances (the exp207 mutual-distance matrix machinery), the selection
order deposited.

GATES (each evaluated exactly once):
  GATE-D1 (the manifest) 40 multi-family deep programs built and
           canon-asserted (exp207's build verbatim, seed 207207);
           the manifest + f_sha256s deposited FIRST; 0 MULTI-family
           clashes.
  GATE-D2 (the spread) the max-min selection order deposited; the
           cohort's min pairwise distance STRICTLY GREATER than
           exp207's single-regime cohort's (the spread is real, not
           nominal); the distance matrices both deposited.
  GATE-D3 (the funnel) the spread cohort priced through the SAME
           funnel (the self-excluded bar N*_lib-112 76.103, the
           counterfactual max vs the frozen 72 82.288); the branch
           named: SOME-CLEAR (>= 1 member clears the self-excluded
           bar) / BAR-RISES (0 clear AND the P95 re-tightened around
           the spread cohort — the self-tightening proof) /
           NEITHER.
  GATE-D4 (hygiene) zero rejections; all finite; the -60.0
           production floor asserted; no per-program tuning.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp220_spread_cohort_selection.json
RUN: python3 -m experiments.exp220_spread_cohort_selection [--smoke] [--job ...] [--out ...]
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
                   "exp220_spread_cohort_selection.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged; gates D1-D4
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
        out_path = "/tmp/exp220_smoke_discarded.json"   # smoke: discarded

    # ---- exp184's B3 import block, verbatim (BLAS pins included) ----
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    from experiments.exp136_generator_v6 import (  # noqa: E402
        build_library, dist, library_nn_stats, build_splices,
        nov_lib, wildtype_target)
    from experiments import exp146_splice_bar as L  # noqa: E402
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    DEP207 = os.path.join(ROOT, "results",
                          "exp207_multifamily_deep_cohort.json")
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
    SPLICE_CROSSES = 19

    dep207 = json.load(open(DEP207))
    dep150 = json.load(open(DEP150))
    FROZEN_BAR_LIB = float(dep150["bars"]["n_star_lib"])
    dep207_bars = dep207["sections"]["bars"]
    assert FROZEN_BAR_LIB == float(dep207_bars["frozen_bar_lib"]), \
        "frozen bar drift vs exp207's deposit"

    # ---- hygiene: the production floor asserted, never touched ------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, "production floor drift"

    # ---- canon check (exp184 verbatim) -------------------------------
    canon = wildtype_target(g6.N)
    assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"

    # ==================================================================
    # THE BUILD (GATE-D1): exp207's generator VERBATIM (its fixed RNG
    # consumption order per program: one uniform -> k against the
    # cumulative ladder; k starts; k widths; k values; all rounded 1 dp;
    # zones sorted by start (stable); on overlap or on the deep-band
    # constraint's violation the program's whole draw set is REGENERATED
    # from the same stream) at the registered seed 207207 and ladder
    # {1: 10, 2: 12, 3: 10, 4: 8}/40 with the deep-band constraint
    # >= 2 zones <= -40. The build is then cross-validated BIT-EXACT
    # against exp207's deposited manifest (f_sha256 per program) —
    # the "VERBATIM" clause is asserted, not narrated.
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

    # ---- the MULTI-family program set (exp194's registered
    #      constants, reconstructed for the structural assertion) -----
    W_DELTAS = (0.0, 0.01, -0.01, 0.02, -0.02, 0.01)
    MIXED_PATTERNS = ((-60.0, -15.0, -45.0),
                      (-15.0, -50.0, -55.0),
                      (-40.0, -60.0, -20.0))
    DEEP_RUNGS = (-40.0, -45.0, -50.0, -55.0, -60.0)

    def multi_triples(voltages, i: int) -> tuple:
        d = W_DELTAS[i]
        zs = [(round(z.f0 + i / 100.0 + d, 3),
               round(z.f1 + i / 100.0 - d, 3), v)
              for z, v in zip(MULTI.zones, voltages)]
        return tuple(sorted(zs, key=lambda x: x[0]))

    multi_family: set = set()
    for rung in DEEP_RUNGS:
        for i in range(6):
            multi_family.add(multi_triples([rung] * 3, i))
    for pat in MIXED_PATTERNS:
        for i in range(5):
            multi_family.add(multi_triples(list(pat), i))
    assert len(multi_family) == 45, \
        f"MULTI-family reconstruction drift: {len(multi_family)}"

    cohort, census = gen_cohort()
    assert len(cohort) == N_COHORT
    # bit-exact cross-validation vs exp207's deposited manifest
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
    n_multi_clash = sum(1 for m in cohort
                        if tuple(sorted(m["triples"],
                                        key=lambda x: x[0]))
                        in multi_family)
    print(f"  cohort built: {N_COHORT} programs | f_sha256 matches vs "
          f"exp207's deposit {n_sha_match}/{N_COHORT} | draws "
          f"{census['n_draws']} | overlap regens "
          f"{census['n_overlap_regens']} | deep-band regens "
          f"{census['n_deepband_regens']} | realized k "
          f"{census['realized_k']} | MULTI-family clashes "
          f"{n_multi_clash}")

    # ---- THE MANIFEST DEPOSITED FIRST (GATE-D1; checkpoint write) ----
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    manifest = {"exp": "exp220_spread_cohort_selection",
                "checkpoint": "manifest-first (GATE-D1)",
                "cohort_seed": COHORT_SEED,
                "k_ladder": {str(k): w for k, w in K_LADDER},
                "k_cumulative": [round(float(x), 3) for x in K_CUM],
                "census": census,
                "f_sha256_matches_vs_exp207": n_sha_match,
                "multi_family_clashes": n_multi_clash,
                "manifest": [{"member": m["member"],
                              "zone_count": m["zone_count"],
                              "triples": [list(t) for t in m["triples"]],
                              "vmin": m["vmin"],
                              "f_sha256": m["f_sha256"]}
                             for m in cohort]}
    with open(out_path, "w") as fh:
        json.dump(manifest, fh, indent=1, default=float)
    print(f"  manifest deposited FIRST -> {out_path}")

    # ---- the 112-member extended library + the bars re-derived
    #      BEFORE selection (asserted vs exp207's deposit) -------------
    lib_frozen = build_library()
    assert len(lib_frozen) == 72, "frozen library size drift"
    frozen_names = list(lib_frozen)
    frozen_arr = np.stack([lib_frozen[n] for n in frozen_names])
    deep_lib = {m["member"]: m["f"] for m in cohort}
    lib = dict(lib_frozen)
    lib.update(deep_lib)
    assert len(lib) == 112, f"extended library drift: {len(lib)}"
    lib_names = list(lib)
    M = len(lib_names)

    n_star_lib, nn_arr = library_nn_stats(lib)
    assert round(n_star_lib, 3) == 76.103, \
        f"N*_lib-112 re-derivation drift: {n_star_lib}"
    assert abs(n_star_lib
               - float(dep207_bars["n_star_lib_112"])) < 1e-9, \
        "N*_lib-112 drift vs exp207's deposit"
    print(f"  library {M} members | N*_lib-112 {n_star_lib:.3f} "
          f"(RE-DERIVED before selection; asserted == exp207's deposit)")

    # the anatomy distance matrix (exp207's machinery, verbatim)
    Dm = np.zeros((M, M))
    for i in range(M):
        for j in range(i + 1, M):
            Dm[i, j] = Dm[j, i] = dist(lib[lib_names[i]],
                                       lib[lib_names[j]])
    assert np.array_equal(
        np.array([Dm[i][np.arange(M) != i].min() for i in range(M)]),
        nn_arr), "nn harness drift"

    # ---- the splice family + N*_splice (exp146 machinery) -----------
    SPLICE_EXPECTED = M * (M - 1) // 2 * SPLICE_CROSSES
    S = build_splices(lib)
    assert len(S) == SPLICE_EXPECTED, \
        f"splice family drift: {len(S)} != {SPLICE_EXPECTED}"
    fm = np.zeros((len(S), 100), dtype=bool)
    fm[:, 1:] = S[:, 1:] != S[:, :-1]
    fl = fm.sum(axis=1)
    n_star_splice, _, _ = L.splice_family_bar(S)
    assert round(n_star_splice, 3) == 16.021, \
        f"N*_splice-112 re-derivation drift: {n_star_splice}"
    assert abs(n_star_splice
               - float(dep207_bars["n_star_splice_112"])) < 1e-9, \
        "N*_splice-112 drift vs exp207's deposit"
    S_frozen = build_splices(lib_frozen)
    fmF = np.zeros((len(S_frozen), 100), dtype=bool)
    fmF[:, 1:] = S_frozen[:, 1:] != S_frozen[:, :-1]
    flF = fmF.sum(axis=1)
    print(f"  splice family {len(S)} | N*_splice-112 "
          f"{n_star_splice:.3f} (RE-DERIVED before selection; asserted "
          f"== exp207's deposit) | frozen bar {FROZEN_BAR_LIB:.3f}")

    # the frozen record's own P95 (the moving bar's starting level)
    n_star_frozen, nn_frozen = library_nn_stats(lib_frozen)
    assert round(n_star_frozen, 3) == 82.288, \
        f"frozen-72 P95 drift: {n_star_frozen}"

    dep207_trace = {t["member"]: t for t in dep207["sections"]["trace_rows"]}

    # ==================================================================
    # THE SPREAD (GATE-D2): exp179's greedy VERBATIM as the max-min
    # selector. The 40 programs' pairwise distances (the exp207
    # mutual-distance matrix machinery) feed a greedy max-min
    # (farthest-first) ordering: the seed is the most isolated program
    # (max nearest-other within the 40; ties -> member index ascending),
    # each next slot takes the remaining program MAXIMIZING its min
    # distance to the already-selected (ties -> member index ascending)
    # — that ordering is the selection order, deposited in full.
    # exp179's keep-discipline is then applied at the generator's OWN
    # bar (N*_lib-112, re-derived above BEFORE selection): walk the
    # selection order, keep iff min distance to the KEPT set > bar.
    # The kept members, in selection order, are THE SPREAD COHORT.
    # ==================================================================
    cohort_pos = [lib_names.index(m["member"]) for m in cohort]
    C40 = Dm[np.ix_(cohort_pos, cohort_pos)]
    off = ~np.eye(N_COHORT, dtype=bool)
    min_pair_single = float(C40[off].min())
    max_pair_single = float(C40[off].max())

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
            if best_v is None or v > best_v:   # strict: ties -> lowest idx
                best_i, best_v = i, v
        sel_order.append(best_i)
        step_values.append(best_v)
        remaining.discard(best_i)
    assert len(sel_order) == N_COHORT and len(set(sel_order)) == N_COHORT

    spread_bar = float(n_star_lib)   # the generator's own bar, BEFORE
    kept: list[int] = []
    keep_margin_at: dict[int, float | None] = {}
    for i in sel_order:
        d_kept = min((float(C40[i, j]) for j in kept), default=np.inf)
        if d_kept > spread_bar:
            # the first keep faces an empty kept set — no margin exists
            keep_margin_at[i] = (None if not kept
                                 else d_kept - spread_bar)
            kept.append(i)
    keep_margins = [keep_margin_at[i] for i in kept]
    K = len(kept)
    print(f"  max-min selection order deposited ({N_COHORT} slots) | "
          f"spread cohort kept {K} at the generator's own bar "
          f"{spread_bar:.3f}")

    min_pair_spread = (float(C40[np.ix_(kept, kept)][
        ~np.eye(K, dtype=bool)].min()) if K >= 2 else None)
    spread_real = bool(K >= 2 and min_pair_spread > min_pair_single)
    mps_txt = (f"{min_pair_spread:.3f}" if min_pair_spread is not None
               else "undefined (<2 kept)")
    print(f"  D2: spread cohort min pairwise {mps_txt} vs "
          f"single-regime cohort's {min_pair_single:.3f} -> "
          f"{'REAL' if spread_real else 'NOMINAL/ABSENT'}")

    # ==================================================================
    # THE FUNNEL (GATE-D3): the spread cohort priced through the SAME
    # funnel. Two records deposited:
    #   (i) the fixed 112-record (exp207's M2 funnel VERBATIM, the
    #       cross-validation: the values must reproduce exp207's trace
    #       bit-level for every spread member);
    #   (ii) the spread record (frozen 72 + the spread cohort) — the
    #       N-body record the spread cohort actually faces — with the
    #       P95 RE-DERIVED AROUND THE SPREAD COHORT, plus the
    #       moving-bar admission walk (the bar re-derived at every
    #       admission; exp207's single-regime generation order walked
    #       as the control).
    # Branch (disclosed reading): SOME-CLEAR iff >= 1 spread member's
    # self-excluded nearest-other distance in the spread record clears
    # the registered self-excluded bar N*_lib-112 76.103; else
    # BAR-RISES iff the P95 re-tightened around the spread cohort
    # (N*_spread <= 76.103 — the bar returned to the single-regime
    # tightened level); else NEITHER.
    # ==================================================================
    trace_rows = []
    for rank, i in enumerate(sel_order):
        if i not in kept:
            continue
        m = cohort[i]
        pos = cohort_pos[i]
        dist_other_112 = float(Dm[pos][np.arange(M) != pos].min())
        nov_cf = float(nov_lib(m["f"], frozen_arr))
        nov_splice_ext = float(L.fast_nov_splice(m["f"], S, fm, fl))
        nov_splice_cf = float(L.fast_nov_splice(m["f"], S_frozen, fmF,
                                                flF))
        # bit-level cross-validation vs exp207's trace (same funnel)
        dt = dep207_trace[m["member"]]
        assert abs(dist_other_112
                   - dt["stage_a_lib_novel"]["criterion_self_excluded"]
                   ["value"]) < 1e-9, \
            f"{m['member']}: 112-record NN drift vs exp207"
        assert abs(nov_cf
                   - dt["stage_a_lib_novel"]
                   ["counterfactual_had_they_been_invented"]
                   ["value"]) < 1e-9, \
            f"{m['member']}: counterfactual drift vs exp207"
        assert abs(nov_splice_ext
                   - dt["stage_c_splice_clear"]["value"]) < 1e-9 and \
            abs(nov_splice_cf
                - dt["stage_c_splice_clear"]
                ["counterfactual_had_they_been_invented"]
                ["value"]) < 1e-9, \
            f"{m['member']}: splice reading drift vs exp207"
        sp_pos = [cohort_pos[j] for j in kept]
        others = [p for p in sp_pos if p != pos]
        nn_spread = float(min([Dm[pos, p] for p in others]
                              + [float(Dm[pos, :len(frozen_names)].min())]))
        cleared_fixed = bool(dist_other_112 > n_star_lib)
        cleared_spread = bool(nn_spread > n_star_lib)
        trace_rows.append({
            "member": m["member"], "zone_count": m["zone_count"],
            "selection_rank": rank,
            "keep_margin_at_keep": keep_margin_at[i],
            "stage_a_lib_novel": {
                "criterion_self_included": {
                    "criterion": ("nov_lib(f, extended record incl. "
                                  "self) > N*_lib"),
                    "value": 0.0, "bar": float(n_star_lib),
                    "pass": False,
                    "note": ("degenerate for a record member — 0 by "
                             "definition (exp184's X2 note)")},
                "criterion_self_excluded": {
                    "criterion": ("nearest OTHER member of the 112-"
                                  "member extended record > N*_lib "
                                  "(exp189's trace reading; the fixed "
                                  "record — cross-validated == exp207)"),
                    "value": dist_other_112,
                    "bar": float(n_star_lib),
                    "bar_rounded": round(float(n_star_lib), 3),
                    "margin_bar_minus_value":
                        float(n_star_lib - dist_other_112),
                    "pass": cleared_fixed},
                "counterfactual_had_they_been_invented": {
                    "reference": ("nov_lib vs the frozen 72 (exp150's "
                                  "deposited machinery)"),
                    "value": nov_cf,
                    "bar_extended": float(n_star_lib),
                    "pass_at_extended_bar": bool(nov_cf > n_star_lib),
                    "bar_frozen_deposit": FROZEN_BAR_LIB,
                    "pass_at_frozen_bar":
                        bool(nov_cf > FROZEN_BAR_LIB)}},
            "stage_b_splice_family": {
                "criterion": ("membership in the extended splice family "
                              "(structural)"),
                "in_family": True,
                "partners": M - 1, "crosses_per_pair": SPLICE_CROSSES,
                "pass": True},
            "stage_c_splice_clear": {
                "criterion": ("nov_splice(f, extended family) > "
                              "N*_splice"),
                "value": nov_splice_ext, "bar": float(n_star_splice),
                "bar_rounded": round(float(n_star_splice), 3),
                "pass": bool(cleared_fixed
                             and nov_splice_ext > n_star_splice),
                "counterfactual_had_they_been_invented": {
                    "value": nov_splice_cf,
                    "bar_frozen_deposit":
                        float(dep150["bars"]["n_star_splice"]),
                    "pass_at_frozen_bar": bool(
                        nov_splice_cf
                        > dep150["bars"]["n_star_splice"])},
                "note": ("reached only if the lib-novelty stage passed; "
                         "the value is deposited for every row "
                         "regardless")},
            "spread_record_reading": {
                "record": "frozen 72 + the spread cohort",
                "nn_self_excluded": nn_spread,
                "bar_fixed_n_star_lib_112": float(n_star_lib),
                "clears_at_fixed_bar": cleared_spread,
                "clears_at_own_p95": None,   # finalized after N*_spread
                "note": ("the N-body record the spread cohort actually "
                         "faces; the own-p95 column is finalized after "
                         "N*_spread is derived below")},
            "excluding_stage": (None if cleared_fixed
                                else "a_lib_novel"),
            "in_splice_clear_final": bool(
                cleared_fixed and nov_splice_ext > n_star_splice)})

    # ---- the spread record + the P95 RE-DERIVED AROUND IT -----------
    lib_spread = dict(lib_frozen)
    lib_spread.update({cohort[i]["member"]: cohort[i]["f"] for i in kept})
    assert len(lib_spread) == 72 + K
    n_star_spread, nn_spread_arr = library_nn_stats(lib_spread)
    for tr in trace_rows:   # finalize the own-p95 column
        tr["spread_record_reading"]["bar_own_p95"] = float(n_star_spread)
        tr["spread_record_reading"]["clears_at_own_p95"] = bool(
            tr["spread_record_reading"]["nn_self_excluded"]
            > n_star_spread)
    n_clear_fixed = sum(1 for tr in trace_rows
                        if tr["stage_a_lib_novel"]
                        ["criterion_self_excluded"]["pass"])
    n_clear_spread = sum(1 for tr in trace_rows
                         if tr["spread_record_reading"]
                         ["clears_at_fixed_bar"])
    n_clear_own_p95 = sum(1 for tr in trace_rows
                          if tr["spread_record_reading"]
                          ["clears_at_own_p95"])

    # ---- the moving-bar admission walks ------------------------------
    def walk(order_idx: list[int], label: str) -> dict:
        cur_names = list(frozen_names)
        cur_nn = nn_frozen.copy()
        steps = []
        n_clear = 0
        for i in order_idx:
            pos = cohort_pos[i]
            d_all = Dm[pos, [lib_names.index(n) for n in cur_names]]
            nn_new = float(d_all.min())
            bar_before = float(np.percentile(cur_nn, 95))
            cleared = bool(nn_new > bar_before)
            n_clear += int(cleared)
            cur_nn = np.minimum(cur_nn, d_all)
            cur_nn = np.append(cur_nn, nn_new)
            cur_names.append(cohort[i]["member"])
            bar_after = float(np.percentile(cur_nn, 95))
            steps.append({"member": cohort[i]["member"],
                          "nn_self_excluded": nn_new,
                          "bar_before": bar_before,
                          "clears_the_move": cleared,
                          "bar_after": bar_after})
        # the incremental machinery must reproduce the direct statistic
        if len(order_idx) == N_COHORT:
            assert np.array_equal(np.sort(cur_nn), np.sort(nn_arr)), \
                f"{label}: walk nn spectrum drift vs library_nn_stats"
            assert abs(float(np.percentile(cur_nn, 95)) - n_star_lib) \
                < 1e-12, f"{label}: walk final bar drift"
        else:
            assert np.array_equal(np.sort(cur_nn),
                                  np.sort(nn_spread_arr)), \
                f"{label}: walk nn spectrum drift vs library_nn_stats"
            assert abs(float(np.percentile(cur_nn, 95))
                       - n_star_spread) < 1e-12, \
                f"{label}: walk final bar drift"
        print(f"  walk[{label}]: {len(steps)} admissions | "
              f"bar {FROZEN_BAR_LIB:.3f} -> "
              f"{steps[-1]['bar_after']:.3f} | moving-bar clears "
              f"{n_clear}")
        return {"label": label, "order": [cohort[i]["member"]
                                          for i in order_idx],
                "n_admissions": len(steps), "n_clears": n_clear,
                "bar_start": float(np.percentile(nn_frozen, 95)),
                "bar_final": steps[-1]["bar_after"],
                "steps": steps}

    walk_spread = walk(list(kept), "spread-cohort (selection order)")
    # the control is a measurement, not an assert: exp207's N-body
    # finding (0 clears, the P95 re-tightens around every admission)
    # is REPRODUCED here or the deviation is deposited honestly
    walk_control = walk(list(range(N_COHORT)),
                        "single-regime control (generation order)")

    # ---- the branch (each evaluated exactly once) --------------------
    some_clear = bool(n_clear_spread >= 1)
    bar_rises = bool((not some_clear) and n_clear_spread == 0
                     and n_star_spread <= n_star_lib + 1e-9)
    branch = ("SOME-CLEAR" if some_clear else
              "BAR-RISES" if bar_rises else "NEITHER")
    print(f"  D3: fixed-112 clears {n_clear_fixed}/{K} (cross-validated "
          f"== exp207) | spread-record clears at the fixed bar "
          f"{n_clear_spread}/{K} | at the record's own P95 "
          f"{n_clear_own_p95}/{K} | N*_spread {n_star_spread:.3f} vs "
          f"N*_lib-112 {n_star_lib:.3f} -> {branch}")

    # ---- GATE-D4 (hygiene) -------------------------------------------
    n_rej = 0   # no rejection machinery fires in the registered readings
    numeric_vals = [tr["stage_a_lib_novel"]["criterion_self_excluded"]
                    ["value"] for tr in trace_rows] + \
                   [tr["stage_a_lib_novel"]
                    ["counterfactual_had_they_been_invented"]["value"]
                    for tr in trace_rows] + \
                   [tr["spread_record_reading"]["nn_self_excluded"]
                    for tr in trace_rows] + \
                   [s["nn_self_excluded"] for s in
                    walk_spread["steps"] + walk_control["steps"]] + \
                   [min_pair_single, max_pair_single] + \
                   ([min_pair_spread] if min_pair_spread is not None
                    else [])
    all_finite = bool(np.all(np.isfinite(numeric_vals)))
    d1_pass = bool(len(cohort) == N_COHORT
                   and n_sha_match == N_COHORT and n_multi_clash == 0)
    d2_pass = spread_real
    d3_pass = True   # every registered branch completes the gate
    d4_pass = bool(n_rej == 0 and all_finite)
    gates = {
        "D1": {"pass": bool(d1_pass), "n_cohort": len(cohort),
               "f_sha256_matches_vs_exp207": n_sha_match,
               "multi_family_clashes": n_multi_clash,
               "canon_asserted_per_program": True,
               "realized_k": census["realized_k"],
               "bars": {"n_star_lib_112": round(float(n_star_lib), 3),
                        "n_star_splice_112":
                            round(float(n_star_splice), 3),
                        "frozen_bar_lib": FROZEN_BAR_LIB},
               "bars_deposited_before_selection": True},
        "D2": {"pass": bool(d2_pass), "n_kept": K,
               "spread_bar": float(spread_bar),
               "min_pair_spread": min_pair_spread,
               "min_pair_single_regime": min_pair_single,
               "strictly_greater": bool(
                   min_pair_spread is not None
                   and min_pair_spread > min_pair_single),
               "selection_order": [cohort[i]["member"]
                                   for i in sel_order],
               "step_values": [round(v, 3) for v in step_values],
               "kept_members": [cohort[i]["member"] for i in kept],
               "keep_margins_at_keep": keep_margins},
        "D3": {"pass": bool(d3_pass), "branch": branch,
               "n_clear_fixed_112": n_clear_fixed,
               "n_clear_spread_record_at_fixed_bar": n_clear_spread,
               "n_clear_spread_record_at_own_p95": n_clear_own_p95,
               "n_star_spread": round(float(n_star_spread), 3),
               "n_star_lib_112": round(float(n_star_lib), 3),
               "p95_re_tightened_around_spread_cohort": bool(
                   n_star_spread <= n_star_lib + 1e-9),
               "walk_spread_clears": walk_spread["n_clears"],
               "walk_control_clears": walk_control["n_clears"],
               "reading_disclosure": (
                   "SOME-CLEAR is evaluated on the spread record (the "
                   "N-body record the spread cohort faces: frozen 72 + "
                   "the spread cohort) at the registered self-excluded "
                   "bar N*_lib-112 76.103; the fixed-112-record reading "
                   "is deposited as the same-funnel cross-validation "
                   "(bit-level == exp207's trace). BAR-RISES = 0 clear "
                   "AND N*_spread <= 76.103 (the P95 re-tightened "
                   "around the spread cohort).")},
        "D4": {"pass": bool(d4_pass), "rejections": n_rej,
               "all_finite": all_finite,
               "floor_asserted": PROD_FLOOR,
               "no_per_program_tuning": True}}
    n_pass = sum(1 for g in gates.values() if g["pass"])
    verdict = (f"{n_pass}/4 gates (D1 D2 D3 D4) | {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp220_spread_cohort_selection",
        "claim": (
            "THE SPREAD-COHORT SELECTION ORDER (L188's registered "
            "next): exp207's N-body finding — the funnel's refusal is "
            "the cohort's OWN DENSITY, the P95 statistic re-tightens "
            "around every admission — is tested with a DELIBERATELY "
            "SPREAD cohort: exp179's greedy discipline as a max-min "
            "(farthest-first) selector over the generator's own 40 "
            "programs (exp207's build verbatim at seed 207207), kept "
            "at the generator's own bar (N*_lib-112). Can the spread "
            "cohort land even ONE member above the moving bar — or "
            "does the bar rise to meet every cohort (the self-"
            "tightening proof)?"),
        "pre_registered": {
            "gates_source": (
                "module docstring, committed before any run "
                "(pre-registration d52addd, batch 11; gates D1-D4 "
                "fixed there, each evaluated exactly once)"),
            "gates": [
                "GATE-D1 (the manifest) 40 multi-family deep programs "
                "built and canon-asserted (exp207's build verbatim, "
                "seed 207207); the manifest + f_sha256s deposited "
                "FIRST; 0 MULTI-family clashes",
                "GATE-D2 (the spread) the max-min selection order "
                "deposited; the cohort's min pairwise distance "
                "STRICTLY GREATER than exp207's single-regime "
                "cohort's (the spread is real, not nominal); the "
                "distance matrices both deposited",
                "GATE-D3 (the funnel) the spread cohort priced "
                "through the SAME funnel (the self-excluded bar "
                "N*_lib-112 76.103, the counterfactual max vs the "
                "frozen 72 82.288); the branch named: SOME-CLEAR / "
                "BAR-RISES / NEITHER",
                "GATE-D4 (hygiene) zero rejections; all finite; the "
                "-60.0 production floor asserted; no per-program "
                "tuning"]},
        "sections": {
            "manifest": manifest,
            "bars": {"n_star_lib_112": float(n_star_lib),
                     "n_star_splice_112": float(n_star_splice),
                     "frozen_bar_lib": FROZEN_BAR_LIB,
                     "n_star_frozen_72": float(n_star_frozen),
                     "n_star_spread_record": float(n_star_spread),
                     "re_derived_before_selection": True,
                     "asserted_vs_exp207_deposit": True},
            "census": census,
            "selection": {
                "selector": ("exp179's greedy discipline as the max-min "
                             "(farthest-first) selector: seed = the most "
                             "isolated program (max nearest-other within "
                             "the 40, ties -> member index ascending); "
                             "each next slot maximizes min distance to "
                             "the already-selected (ties -> lowest "
                             "index); keep-discipline at the generator's "
                             "own bar N*_lib-112"),
                "bar": float(spread_bar),
                "selection_order": [cohort[i]["member"]
                                    for i in sel_order],
                "step_values": [float(v) for v in step_values],
                "kept_members": [cohort[i]["member"] for i in kept],
                "keep_margins_at_keep": keep_margins},
            "distance_matrices": {
                "single_regime_40x40":
                    [[round(float(x), 6) for x in row] for row in C40],
                "spread_kxk": ([[round(float(x), 6) for x in row]
                                for row in C40[np.ix_(kept, kept)]]
                               if K >= 2 else []),
                "min_pair_single_regime": min_pair_single,
                "min_pair_spread": min_pair_spread,
                "max_pair_single_regime": max_pair_single},
            "trace_rows": trace_rows,
            "funnel": {
                "spread_record": {
                    "record": "frozen 72 + the spread cohort",
                    "n_members": 72 + K,
                    "n_star_spread": float(n_star_spread),
                    "n_star_lib_112": float(n_star_lib),
                    "p95_re_tightened_around_spread_cohort": bool(
                        n_star_spread <= n_star_lib + 1e-9),
                    "n_clear_fixed_112": n_clear_fixed,
                    "n_clear_spread_at_fixed_bar": n_clear_spread,
                    "n_clear_spread_at_own_p95": n_clear_own_p95},
                "walk_spread": walk_spread,
                "walk_control_single_regime": walk_control,
                "branch": branch}},
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
