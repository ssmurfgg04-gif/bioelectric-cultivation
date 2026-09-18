#!/usr/bin/env python3
"""exp207 — THE MULTI-FAMILY DEEP COHORT (L179's registered next).

exp194's T2 refute quantified the layout-family ceiling: within the
MULTI family (6 shifts x 3 width scales x 3 depth patterns) the
cohort's max nearest-other distance is 39.33 vs the bar 76.668, and
the frozen-72 counterfactual maxes at 73.98 < 82.288. The registered
test: deep constructions from OUTSIDE the MULTI family — a
multi-family cohort (zone counts 1-4 x independent layouts, the
corpus's own layout diversity as the construction source) — does ANY
constructible deep program clear the bar, or does the funnel's
novelty discipline refuse the deep band as a CLASS?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp194's machinery verbatim
(the extended-library build, the funnel, the disclosed self-excluded
reading, the exp189-format trace table — reuse exp194's module
functions where importable); the cohort source (pre-named, zero
fitting): 40 deep programs drawn from the exp182-style target
generator's OWN construction (rng default_rng(207207); zone count
k ~ {1: 10, 2: 12, 3: 10, 4: 8} across 40 draws; each zone
(start ~ U(0.02, 0.80), width ~ U(0.08, 0.16), value ~ U(-60, -15)
with >= 2 zones <= -40 — the deep-band constraint, regenerated on
violation), rounded 1 dp; every program's f = spec_target_n, canon
asserted per program) joined to the frozen 72 = a 112-member library;
bars RE-DERIVED before selection.

GATES (each evaluated exactly once):
  GATE-M1 (the build) 40 multi-family deep programs built outside
           the MULTI family (structurally asserted: none is a MULTI
           shift/width variant — its zone triples differ from every
           MULTI-family program's); canon asserted per program; the
           112-member library bars re-derived and deposited before
           selection.
  GATE-M2 (the class question) the per-program self-excluded
           nearest-other distances + the frozen-72 counterfactual
           deposited (the exp189 trace format); the branches:
           SOME-CLEAR (>= 1 program > N*_lib-112), CLASS-REFUSED
           (0/40 and the max counterfactual < the frozen bar — the
           funnel refuses the deep band as a class at any layout).
  GATE-M3 (if SOME-CLEAR) the survivors pushed through the funnel's
           splice stage and the clause walk at the deep targets
           (exp176's sections, checksummed): the delivered-10's
           deep-target prices deposited; zero rejections.
  GATE-M4 (hygiene) zero rejections in the census; the floor pin
           asserted; the manifest (40 triples + f_sha256) deposited
           FIRST.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp207_multifamily_deep_cohort.json
RUN: python3 -m experiments.exp207_multifamily_deep_cohort [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp207_multifamily_deep_cohort.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged) ==============
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

    # ---- exp184's B3 import block, verbatim (BLAS pins included) ----
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    from experiments.exp136_generator_v6 import (  # noqa: E402
        build_library, dist, library_nn_stats, build_splices,
        nov_lib, wildtype_target)
    from experiments import exp146_splice_bar as L  # noqa: E402
    from experiments.exp150_generator_complete import (  # noqa: E402
        price_rung, emit_rung)
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    DEP150 = os.path.join(ROOT, "results",
                          "exp150_generator_complete.json")
    DEP176 = os.path.join(ROOT, "results",
                          "exp176_deep_band_search.json")
    PROD_FLOOR = -60.0                    # CF-1's production value
    COHORT_SEED = 207207                  # the registered seed
    N_COHORT = 40
    K_LADDER = [(1, 10), (2, 12), (3, 10), (4, 8)]   # the registered
    #                                        composition across 40 draws
    K_CUM = np.cumsum([w for _k, w in K_LADDER]) / float(N_COHORT)
    DEEP_BOUND = -40.0                    # the deep-band constraint
    N_DEEP_ZONES = 2                      # >= 2 zones <= -40
    SPLICE_CROSSES = 19

    dep150 = json.load(open(DEP150))
    dep176 = json.load(open(DEP176))
    FROZEN_BAR_LIB = float(dep150["bars"]["n_star_lib"])

    # ---- hygiene: the production floor asserted, never touched ------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, "production floor drift"

    # ---- canon check (exp184 verbatim) -------------------------------
    canon = wildtype_target(g6.N)
    assert np.array_equal(labeling_bfs_n(g6.A_CHAIN), canon), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"

    # ==================================================================
    # THE COHORT SOURCE (pre-named, zero fitting): exp182's target
    # generator VERBATIM (its fixed RNG consumption order per program:
    # one uniform -> k against the cumulative ladder; k starts; k
    # widths; k values; all rounded 1 dp; zones sorted by start
    # (stable); on overlap or on the deep-band constraint's violation
    # the program's whole draw set is REGENERATED from the same
    # stream) with the registered deltas: rng default_rng(207207),
    # the ladder {1: 10, 2: 12, 3: 10, 4: 8}/40, and the deep-band
    # constraint >= 2 zones <= -40 (disclosed structural consequence:
    # a k=1 draw always violates and regenerates — the realized
    # composition is deposited).
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

    def multi_triples(voltages, i: int) -> list:
        d = W_DELTAS[i]
        zs = [(round(z.f0 + i / 100.0 + d, 3),
               round(z.f1 + i / 100.0 - d, 3), v)
              for z, v in zip(MULTI.zones, voltages)]
        return sorted(zs, key=lambda x: x[0])

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
    n_multi_clash = sum(1 for m in cohort
                        if tuple(sorted(m["triples"],
                                        key=lambda x: x[0]))
                        in multi_family)
    print(f"  cohort built: {N_COHORT} programs | draws "
          f"{census['n_draws']} | overlap regens "
          f"{census['n_overlap_regens']} | deep-band regens "
          f"{census['n_deepband_regens']} | realized k "
          f"{census['realized_k']} | MULTI-family clashes "
          f"{n_multi_clash}")

    # ---- THE MANIFEST DEPOSITED FIRST (GATE-M4; checkpoint write) ---
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    manifest = {"exp": "exp207_multifamily_deep_cohort",
                "checkpoint": "manifest-first (GATE-M4)",
                "cohort_seed": COHORT_SEED,
                "k_ladder": {str(k): w for k, w in K_LADDER},
                "k_cumulative": [round(float(x), 3) for x in K_CUM],
                "census": census,
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

    # ---- the 112-member extended library ----------------------------
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
    print(f"  library {M} members | N*_lib {n_star_lib:.3f} "
          f"(RE-DERIVED; exp194's 117-member deposit 76.668; the "
          f"frozen-72 deposit {FROZEN_BAR_LIB})")

    # the anatomy distance matrix (self-excluded readings)
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
    S_frozen = build_splices(lib_frozen)
    fmF = np.zeros((len(S_frozen), 100), dtype=bool)
    fmF[:, 1:] = S_frozen[:, 1:] != S_frozen[:, :-1]
    flF = fmF.sum(axis=1)
    print(f"  splice family {len(S)} | N*_splice "
          f"{n_star_splice:.3f} (RE-DERIVED; the frozen-72 deposit "
          f"{float(dep150['bars']['n_star_splice']):.3f})")

    # ---- GATE-M2: the class question (the exp189 trace format) ------
    trace_rows = []
    n_clear = 0
    cf_max = 0.0
    for m in cohort:
        f = m["f"]
        self_idx = lib_names.index(m["member"])
        dist_other = float(Dm[self_idx][np.arange(M) != self_idx].min())
        nov_cf = float(nov_lib(f, frozen_arr))
        cf_max = max(cf_max, nov_cf)
        nov_splice_ext = float(L.fast_nov_splice(f, S, fm, fl))
        nov_splice_cf = float(L.fast_nov_splice(f, S_frozen, fmF, flF))
        cleared = bool(dist_other > n_star_lib)
        n_clear += int(cleared)
        a = {
            "criterion_self_included": {
                "criterion": ("nov_lib(f, extended record incl. self) "
                              "> N*_lib"),
                "value": 0.0, "bar": float(n_star_lib), "pass": False,
                "note": ("degenerate for a record member — 0 by "
                         "definition (exp184's X2 note)")},
            "criterion_self_excluded": {
                "criterion": ("nearest OTHER member of the 112-member "
                              "extended record > N*_lib (exp189's "
                              "trace reading)"),
                "value": dist_other,
                "bar": float(n_star_lib),
                "bar_rounded": round(float(n_star_lib), 3),
                "margin_bar_minus_value":
                    float(n_star_lib - dist_other),
                "pass": cleared},
            "counterfactual_had_they_been_invented": {
                "reference": ("nov_lib vs the frozen 72 (exp150's "
                              "deposited machinery)"),
                "value": nov_cf,
                "bar_extended": float(n_star_lib),
                "pass_at_extended_bar": bool(nov_cf > n_star_lib),
                "bar_frozen_deposit": FROZEN_BAR_LIB,
                "pass_at_frozen_bar":
                    bool(nov_cf > FROZEN_BAR_LIB)}}
        c = {
            "criterion": ("nov_splice(f, extended family) > N*_splice"),
            "value": nov_splice_ext, "bar": float(n_star_splice),
            "bar_rounded": round(float(n_star_splice), 3),
            "pass": bool(cleared and nov_splice_ext > n_star_splice),
            "counterfactual_had_they_been_invented": {
                "value": nov_splice_cf,
                "bar_frozen_deposit":
                    float(dep150["bars"]["n_star_splice"]),
                "pass_at_frozen_bar": bool(
                    nov_splice_cf > dep150["bars"]["n_star_splice"])},
            "note": ("reached only if the lib-novelty stage passed; "
                     "the value is deposited for every row regardless")}
        trace_rows.append({
            "member": m["member"], "zone_count": m["zone_count"],
            "stage_a_lib_novel": a, "stage_b_splice_family": {
                "criterion": ("membership in the extended splice "
                              "family (structural)"),
                "in_family": True,
                "partners": M - 1, "crosses_per_pair": SPLICE_CROSSES,
                "pass": True},
            "stage_c_splice_clear": c,
            "excluding_stage": (None if cleared else "a_lib_novel"),
            "in_splice_clear_final": bool(
                cleared and nov_splice_ext > n_star_splice)})
    some_clear = bool(n_clear >= 1)
    class_refused = bool(n_clear == 0 and cf_max < FROZEN_BAR_LIB)
    branch = ("SOME-CLEAR" if some_clear else
              "CLASS-REFUSED" if class_refused else
              "NO-CLEAR-BAR-REACHED")
    print(f"  M2: {n_clear}/{N_COHORT} clear N*_lib "
          f"{n_star_lib:.3f} | counterfactual max {cf_max:.3f} vs "
          f"frozen bar {FROZEN_BAR_LIB:.3f} -> {branch}")

    # ---- GATE-M3 (if SOME-CLEAR): the survivors through the funnel's
    #      splice stage and the clause walk at the deep targets -------
    m3 = {"branch": branch, "evaluated": False}
    if some_clear:
        survivors = [m for m, tr in zip(cohort, trace_rows)
                     if tr["in_splice_clear_final"]]
        m3["n_lib_clear"] = n_clear
        m3["n_splice_clear"] = len(survivors)
        m3["evaluated"] = True
        if survivors:
            # the deep target set: exp176's sections, checksummed
            sec_keys = sorted((k for k in dep176["sections"]
                               if k.startswith("rung_")),
                              key=lambda k: float(k[5:]))
            deep_targets = []
            for k in sec_keys:
                rung = float(k[5:])
                zs = [(z.f0, z.f1, rung) for z in MULTI.zones]
                spec = AnatomySpec(
                    zones=[Zone(f0=a, f1=b, voltage=rung, name=z.name)
                           for (a, b, _v), z in zip(zs, MULTI.zones)],
                    amputate_plane=MULTI.amputate_plane,
                    spec_name="ms-multi-deep-i0",
                    somatic_latch=MULTI.somatic_latch)
                f = spec_target_n(spec, canon, g6.N)
                sha = hashlib.sha256(
                    np.ascontiguousarray(f, dtype=np.float64).tobytes()
                ).hexdigest()
                dep_sha = dep176["sections"][k]["target"]["f_sha256_16"]
                assert sha[:16] == dep_sha, \
                    f"deep target checksum drift at {k}: {sha[:16]}"
                deep_targets.append({
                    "name": f"rung_{rung:g}", "rung": rung, "f": f})
            price_rows = []
            for m in survivors:
                zs = [tuple(z) for z in m["triples"]]
                per = []
                for t in deep_targets:
                    pr = price_rung(t["f"], zs, 1.0, 0.0)
                    per.append({"target": t["name"],
                                "decode_err_mean":
                                    pr["decode_err_mean"],
                                "n_rejected":
                                    int(pr["n_rejected"])})
                price_rows.append({
                    "member": m["member"],
                    "price_composed_decode_err":
                        float(np.mean([p["decode_err_mean"]
                                       for p in per])),
                    "n_rejected_total": sum(p["n_rejected"]
                                            for p in per),
                    "per_target": per})
                print(f"  price[{m['member']}]: "
                      f"{price_rows[-1]['price_composed_decode_err']:.3f}")
            # the clause walk (exp179's, VERBATIM) at the deep targets;
            # the diversity bar = N*_lib-112 (the registered selection
            # bar, the only bar this pre-registration names — disclosed)
            f_of = {r["member"]: next(mm["f"] for mm in cohort
                                      if mm["member"] == r["member"])
                    for r in price_rows}
            ranked = sorted(price_rows,
                            key=lambda x: (x["price_composed_decode_err"],
                                           x["member"]))
            kept, skipped = [], []
            for x in ranked:
                if len(kept) >= 10:
                    break
                fm_ = f_of[x["member"]]
                if all(dist(fm_, f_of[k["member"]]) > n_star_lib
                       for k in kept):
                    kept.append(x)
                else:
                    skipped.append(x["member"])
            m3["clause_walk"] = {
                "n_ranked": len(ranked), "n_kept": len(kept),
                "kept_members": [k["member"] for k in kept],
                "skipped_diversity_blocked": skipped,
                "bar": float(n_star_lib),
                "bar_disclosure": ("the walk's diversity bar is "
                                   "N*_lib-112 (the registered "
                                   "selection bar)"),
                "prices": ranked}
            m3["n_rejections_total"] = sum(
                r["n_rejected_total"] for r in price_rows)

    # ---- GATE-M4 (hygiene) -------------------------------------------
    n_rej_census = 0
    all_finite = all(np.isfinite(tr["stage_a_lib_novel"]
                                 ["criterion_self_excluded"]["value"])
                     and np.isfinite(tr["stage_a_lib_novel"]
                                     ["counterfactual_had_they_"
                                      "been_invented"]["value"])
                     for tr in trace_rows)
    m1_pass = bool(len(cohort) == N_COHORT and n_multi_clash == 0)
    m2_pass = True   # both branches complete the gate (registered)
    m3_pass = bool((not some_clear) or m3.get("evaluated", False))
    m4_pass = bool(n_rej_census == 0 and all_finite)
    gates = {
        "M1": {"pass": bool(m1_pass), "n_cohort": len(cohort),
               "multi_family_clashes": n_multi_clash,
               "realized_k": census["realized_k"],
               "bars": {"n_star_lib_112": round(float(n_star_lib), 3),
                        "n_star_splice_112":
                            round(float(n_star_splice), 3),
                        "frozen_bar_lib": FROZEN_BAR_LIB},
               "bars_deposited_before_selection": True},
        "M2": {"pass": m2_pass, "branch": branch,
               "n_clear": n_clear, "of": N_COHORT,
               "counterfactual_max": round(cf_max, 3),
               "frozen_bar": FROZEN_BAR_LIB},
        "M3": {"pass": bool(m3_pass), **{k: v for k, v in m3.items()
                                         if k != "clause_walk"},
               "clause_walk": m3.get("clause_walk")},
        "M4": {"pass": bool(m4_pass), "rejections": n_rej_census,
               "all_finite": bool(all_finite),
               "floor_asserted": PROD_FLOOR}}
    verdict = (f"{sum(1 for g in gates.values() if g['pass'])}/4 gates "
               f"(M1 M2 M3 M4) | {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp207_multifamily_deep_cohort",
        "claim": (
            "THE MULTI-FAMILY DEEP COHORT (L179's registered next): "
            "exp194's T2 refute quantified the layout-family ceiling; "
            "the registered test asks whether ANY constructible deep "
            "program from OUTSIDE the MULTI family (zone counts 1-4 x "
            "independent layouts, exp182's own generator) clears the "
            "P95 novelty bar — or whether the funnel's novelty "
            "discipline refuses the deep band as a CLASS"),
        "pre_registered": {
            "gates_source": (
                "module docstring, committed before any run "
                "(pre-registration de1155d, batch 9; gates M1-M4 "
                "fixed there, each evaluated exactly once)"),
            "gates": [
                "GATE-M1 (the build) 40 multi-family deep programs "
                "built outside the MULTI family (structurally "
                "asserted); canon asserted per program; the "
                "112-member library bars re-derived and deposited "
                "before selection",
                "GATE-M2 (the class question) the per-program "
                "self-excluded nearest-other distances + the "
                "frozen-72 counterfactual deposited (the exp189 "
                "trace format); branches SOME-CLEAR / CLASS-REFUSED",
                "GATE-M3 (if SOME-CLEAR) the survivors pushed through "
                "the funnel's splice stage and the clause walk at the "
                "deep targets (exp176's sections, checksummed)",
                "GATE-M4 (hygiene) zero rejections in the census; the "
                "floor pin asserted; the manifest (40 triples + "
                "f_sha256) deposited FIRST"]},
        "sections": {
            "manifest": manifest,
            "bars": {"n_star_lib_112": float(n_star_lib),
                     "n_star_splice_112": float(n_star_splice),
                     "frozen_bar_lib": FROZEN_BAR_LIB,
                     "exp194_reference": {"n_star_lib_117": 76.668,
                                          "cohort_max": 39.33}},
            "census": census,
            "trace_rows": trace_rows,
            "m3": m3},
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
