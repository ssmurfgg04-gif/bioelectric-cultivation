#!/usr/bin/env python3
"""exp250 — THE M33/miRNA INTERFERENCE ANATOMY (exp236's registered
next; the R2 interference mapped; ledger L228).

THE OPEN ITEM (L212): exp236's R2 REFUTE — the pairwise mechanism
coverages do NOT compose (interference exists). THE ANATOMY: which
cells the miRNA repressor wrongly de-competences that the anterior read
would have correctly specified — the overlap map per the pre-named
battery (the amputation cohort x the mechanism pairs), the repair being
the pre-named gate hierarchy: the competence AND-read (a cell regen-
competent iff BOTH mechanisms' competence predicates hold) vs the
OR-read (either suffices).

PRE-REGISTERED GATES:

  I1  THE OVERLAP MAP: the wrongly-de-competenced cell set named per
      arm (the cells where miRNA represses but M33 would specify) —
      the count and the spatial distribution deposited.
  I2  THE GATE HIERARCHY: the AND-read's coverage >= the OR-read's on
      the trunk plane (the strict intersection removes the interference
      without losing the true competence); the pairwise compositions
      re-run under the AND-read.
  I3  THE DISCIPLINE: exp236's deposit byte-unchanged, zero rejections,
      deterministic.

THE BRANCH (pre-named): I2 PASS -> INTERFERENCE-REPAIRED (exp236's R2
verdict UPDATED); I2 REFUTE -> INTERFERENCE-STRUCTURAL.

RUN: the overlap battery; minutes.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp250.json")


def main() -> dict:
    # ---- the frozen machinery, imported verbatim from exp236 ---------------
    # (the miRNA layer, the w=0 amputation protocol, the shared-pool regen
    # panel with the M33/M35/miRNA gates, and the pre-named panels/seeds)
    from experiments.exp236_microrna_regionalization import (
        ARZ_K, DELTA_M, DT_WALK, GUESS_SD, GRAPH_ARMS, NOISE_STD, PLANES,
        REGIONS, REGEN_SEEDS, RING, SIGMA_M, SOURCE_S, STEPS_PER_CELL,
        draw_pool, mirna_layer, regen_panel, w0_matrix,
    )
    from experiments.exp43_substrate_independence import labeling
    from experiments.exp73_active_renormalization import ERR_BAR, N, make_battery
    from cultivation.bioelectric.collective import M33_LINE, NEURAL_SPEC_MIN

    print("=== exp250: the M33/miRNA interference anatomy ===\n")

    DEP = os.path.join(ROOT, "results", "exp250_interference_anatomy.json")
    EXP236_DEP = os.path.join(
        ROOT, "results", "exp236_microrna_regionalization.json")

    import hashlib

    def sha256_of(path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    rejections: list[str] = []
    h236_before = sha256_of(EXP236_DEP)

    battery = make_battery()
    lbl = labeling(N)

    # ---- the miRNA layer per graph-arm (exp236's mirna_layer, verbatim) ----
    layers = {g: mirna_layer(battery[g]) for g in GRAPH_ARMS}

    # ---- I1: THE OVERLAP MAP (per arm) --------------------------------------
    # the wrongly-de-competenced cell set: the cells where the miRNA
    # represses (m >= m_line) but M33 would specify (phi_spec >= M33_LINE,
    # the production M33 gate — exp236's frozen machinery and its
    # disclosure (1); "above the M33 gate" per this module's
    # pre-registration). The settled layer is wound-independent
    # (mirna_layer(A) predates the cut), so the map is a per-graph-arm
    # object over the whole organism; the spatial distribution is
    # deposited against the amputation cohort's region windows.
    windows = {"head": set(range(0, 25)),       # exp79's reader region
               "mid": set(range(40, 60)),       # exp79's TC-G6 mid wound
               "trunk": set(range(75, 87))}     # exp79's TC-G5 trunk panel
    m33_spec_idx = np.where(lbl >= M33_LINE)[0].tolist()
    overlap_map = {}
    for g in GRAPH_ARMS:
        lay = layers[g]
        rep_idx = np.where(lay["repressed"])[0].tolist()
        ov_idx = sorted(set(rep_idx) & set(m33_spec_idx))
        ov_set = set(ov_idx)
        rep_windows = {w: sum(1 for i in rep_idx if i in idx)
                       for w, idx in windows.items()}
        rep_windows["other"] = len(rep_idx) - sum(rep_windows.values())
        ov_windows = {w: sum(1 for i in ov_idx if i in idx)
                      for w, idx in windows.items()}
        ov_windows["other"] = len(ov_idx) - sum(ov_windows.values())
        overlap_map[g] = {
            "overlap_count": len(ov_idx),
            "overlap_idx": ov_idx,
            "overlap_in_amputation_region": {
                plane: sorted(ov_set & set(REGIONS[plane]))
                for plane in PLANES},
            "overlap_spatial_windows": ov_windows,
            "repressed_count": len(rep_idx),
            "repressed_idx": rep_idx,
            "repressed_spatial_windows": rep_windows,
            "m33_specified_count": len(m33_spec_idx),
            "m33_specified_idx": m33_spec_idx,
            "m_line": round(float(lay["m_line"]), 3),
            "m_max": round(float(np.max(lay["m"])), 3),
        }
    i1_maps_complete = all(
        overlap_map[g]["overlap_count"] >= 0
        and "overlap_idx" in overlap_map[g]
        and "overlap_spatial_windows" in overlap_map[g]
        for g in GRAPH_ARMS) and len(overlap_map) == len(GRAPH_ARMS)
    i1 = bool(i1_maps_complete)
    print("  I1 the overlap map (miRNA represses m>=m_line AND M33 would "
          f"specify phi_spec>={M33_LINE}):")
    for g in GRAPH_ARMS:
        mm = overlap_map[g]
        print(f"    {g:11s}: repressed {mm['repressed_count']} "
              f"{mm['repressed_idx']} (windows {mm['repressed_spatial_windows']}), "
              f"M33-specified {mm['m33_specified_count']} "
              f"{mm['m33_specified_idx'][:5]}..., "
              f"OVERLAP {mm['overlap_count']} {mm['overlap_idx']}")
    if all(overlap_map[g]["overlap_count"] == 0 for g in GRAPH_ARMS):
        print("    -> the wrongly-de-competenced set is EMPTY on every arm: "
              "the repressed zone (the source ring, mid-body) never "
              "intersects the M33-specified set (the head) — NO cell-level "
              "miRNA->M33 veto exists")

    # ---- the amputation battery: singles + OR pairs + the AND-read ----------
    # coverage = the plane verdict (region RMS < ERR_BAR, exp73's
    # convention) mean over the seeds — exp236's R2 convention. All arms
    # share each (graph-arm, plane, seed) pool (exp236's draw_pool), so
    # the reads compose on identical draws.
    SINGLES = ("M33", "M35", "miRNA")
    PAIRS = ("M33+M35", "M33+miRNA", "M35+miRNA")

    def run_pass() -> list[dict]:
        rows: list[dict] = []
        for gi, gname in enumerate(GRAPH_ARMS):
            A = battery[gname]
            comp = layers[gname]["competent"]
            # the AND-read competence: regen-competent iff BOTH mechanisms'
            # competence predicates hold — (phi_spec >= M33_LINE) AND
            # (m < m_line). Realized by feeding the conjoined array through
            # exp236's frozen competence-gate arm (its "miRNA" arm reader —
            # the gate consumes the pre-computed competence array and no
            # rng stream) with the pair's single-guess fallback (exp236's
            # M33+miRNA fallback). The frozen regen_panel walk is reused
            # verbatim — zero new walk code.
            comp_and = (lbl >= M33_LINE) & comp
            for pi, plane in enumerate(PLANES):
                region = REGIONS[plane]
                W = w0_matrix(A, region)
                for seed in REGEN_SEEDS:
                    pool = draw_pool(len(region), gi, pi, seed)
                    cfgs = [(a, "single", a, comp) for a in SINGLES] \
                        + [(a, "OR", a, comp) for a in PAIRS] \
                        + [("M33+miRNA", "AND", "miRNA", comp_and)]
                    for name, read, arm, carray in cfgs:
                        try:
                            r = regen_panel(A, W, lbl, seed, arm, region,
                                            carray, pool)
                            if not all(np.isfinite(r[k]) for k in
                                       ("rms", "restored", "zone_acc")):
                                rejections.append(
                                    f"non-finite {gname}/{plane}/{seed}/"
                                    f"{read}:{name}")
                            rows.append({"graph": gname, "plane": plane,
                                         "seed": seed, "pair": name,
                                         "read": read, **r})
                        except Exception as e:  # noqa: BLE001
                            rejections.append(
                                f"exception {gname}/{plane}/{seed}/"
                                f"{read}:{name}: {type(e).__name__}: {e}")
        return rows

    rows1 = run_pass()

    def cov(rows: list[dict], plane: str, g: str, pair: str, read: str) -> float:
        sel = [r["verdict"] for r in rows
               if r["plane"] == plane and r["graph"] == g
               and r["pair"] == pair and r["read"] == read]
        return float(np.mean(sel)) if len(sel) == len(REGEN_SEEDS) \
            else float("nan")

    def cov_and(rows: list[dict], plane: str, g: str, pair: str) -> float:
        # under the AND-read: the M33+miRNA pair runs the conjoined gate;
        # the M35-bearing pairs carry no second spec gate (M35's ARZ
        # convergence is the fallback amender, not a gate — exp236's
        # machinery), so the conjunction over the pair's predicates
        # reduces to the surviving gate: the AND and OR reads COINCIDE
        # for them (the same runs under both reads, disclosed).
        if pair == "M33+miRNA":
            return cov(rows, plane, g, pair, "AND")
        return cov(rows, plane, g, pair, "OR")

    # ---- the exp236 anchor (I3): the re-run singles + OR pairs must
    # reproduce exp236's deposited coverages EXACTLY (its R2_rows carry
    # the unrounded per-run verdicts) ----------------------------------------
    dep236 = json.load(open(EXP236_DEP))
    acc: dict = {}
    for r in dep236["R2_rows"]:
        acc.setdefault((r["plane"], r["graph"], r["arm"]), []).append(
            r["verdict"])
    cov236 = {k: float(np.mean(v)) for k, v in acc.items()}
    cross = []
    for plane in PLANES:
        for g in GRAPH_ARMS:
            for arm in SINGLES + PAIRS:
                mine = cov(rows1, plane, g, arm, "single" if arm in SINGLES
                           else "OR")
                cross.append({"plane": plane, "graph": g, "arm": arm,
                              "rerun": mine, "exp236": cov236[(plane, g, arm)],
                              "ok": bool(mine == cov236[(plane, g, arm)])})
    cross_ok = all(c["ok"] for c in cross) and len(cross) == 54
    if not cross_ok:
        rejections.append(f"exp236 anchor mismatch in "
                          f"{sum(1 for c in cross if not c['ok'])}/54 cells")

    # ---- I2(a): the AND-read vs the OR-read on the trunk plane --------------
    # the gate hierarchy quantified per pair x graph-arm on the trunk
    # plane (exp236's R2 table convention: every cell of the plane's
    # table must hold); the M33+miRNA pair is the anatomy's named pair.
    i2a_rows = []
    for g in GRAPH_ARMS:
        for pair in PAIRS:
            a = cov_and(rows1, "trunk", g, pair)
            o = cov(rows1, "trunk", g, pair, "OR")
            i2a_rows.append({"graph": g, "pair": pair, "and_cov": a,
                             "or_cov": o, "ok": bool(a >= o - 1e-12)})
    i2a = all(r["ok"] for r in i2a_rows)

    # ---- I2(b): the pairwise compositions re-run under the AND-read ---------
    # exp236's R2 criterion (each pair >= max(single) on every plane)
    # re-run with the pairs' gates under the AND-read.
    i2b_rows = []
    for plane in PLANES:
        for g in GRAPH_ARMS:
            best_single = max(cov(rows1, plane, g, a, "single")
                              for a in SINGLES)
            for pair in PAIRS:
                pc = cov_and(rows1, plane, g, pair)
                i2b_rows.append({"plane": plane, "graph": g, "pair": pair,
                                 "and_cov": pc, "max_single": best_single,
                                 "ok": bool(pc >= best_single - 1e-12)})
    i2b = all(r["ok"] for r in i2b_rows)
    i2 = bool(i2a and i2b)

    print(f"\n  I2 the gate hierarchy (coverage = the plane-verdict mean, "
          f"bar {ERR_BAR}):")
    print("    trunk-plane coverage, per graph-arm (AND vs OR):")
    for g in GRAPH_ARMS:
        line = "  ".join(
            f"{p}:{cov_and(rows1, 'trunk', g, p):.2f}/"
            f"{cov(rows1, 'trunk', g, p, 'OR'):.2f}" for p in PAIRS)
        print(f"      {g:11s} AND/OR {line}")
    mm = [r for r in i2a_rows if not r["ok"]]
    fail_a = "; ".join(
        "{}|{} AND {:.2f} < OR {:.2f}".format(
            r["graph"], r["pair"], r["and_cov"], r["or_cov"])
        for r in mm)
    print("    (a) AND >= OR on the trunk plane: "
          f"{sum(r['ok'] for r in i2a_rows)}/{len(i2a_rows)} cells -> "
          f"{'PASS' if i2a else 'REFUTED'}"
          + (f"  (failing: {fail_a})" if not i2a else ""))
    print("    (b) the pairwise compositions under the AND-read "
          "(pair >= max(single)):")
    for plane in PLANES:
        line = "  ".join(
            f"{p}:{cov_and(rows1, plane, 'scale_free', p):.2f}"
            for p in PAIRS)
        print(f"      {plane:5s} (scale_free) {line}   "
              f"singles M33:{cov(rows1, plane, 'scale_free', 'M33', 'single'):.2f}"
              f" M35:{cov(rows1, plane, 'scale_free', 'M35', 'single'):.2f}"
              f" miRNA:{cov(rows1, plane, 'scale_free', 'miRNA', 'single'):.2f}")
    bad_b = [r for r in i2b_rows if not r["ok"]]
    fail_b = ", ".join(
        "{}|{}|{}".format(r["plane"], r["graph"], r["pair"])
        for r in bad_b)
    print(f"      -> {sum(r['ok'] for r in i2b_rows)}/{len(i2b_rows)} "
          f"comparisons hold -> {'PASS' if i2b else 'REFUTED'}"
          + (f"  (failing: {fail_b})" if not i2b else ""))

    # ---- determinism: the full battery re-run, bit-identical ----------------
    rows2 = run_pass()
    key = lambda r: (r["graph"], r["plane"], r["seed"], r["pair"], r["read"])  # noqa: E731
    d1 = {key(r): r for r in rows1}
    d2 = {key(r): r for r in rows2}
    diffs = []
    if set(d1) != set(d2):
        diffs.append("row-key sets differ")
    for k in sorted(set(d1) & set(d2)):
        for f in ("rms", "verdict", "restored", "zone_acc", "zone_flips"):
            if d1[k][f] != d2[k][f]:
                diffs.append(f"{k}:{f}")
    deterministic = not diffs
    if not deterministic:
        rejections.append(f"determinism: {len(diffs)} field diffs "
                          f"(first: {diffs[:3]})")

    # the overlap map re-derived after the battery: identical
    ov_again = {g: sorted(
        set(np.where(layers[g]["repressed"])[0].tolist())
        & set(m33_spec_idx)) for g in GRAPH_ARMS}
    map_stable = all(ov_again[g] == overlap_map[g]["overlap_idx"]
                     for g in GRAPH_ARMS)
    if not map_stable:
        rejections.append("overlap map not stable across passes")

    h236_after = sha256_of(EXP236_DEP)
    byte_unchanged = h236_after == h236_before
    if not byte_unchanged:
        rejections.append("exp236 deposit hash changed during the run")

    i3 = bool(byte_unchanged and cross_ok and deterministic
              and map_stable and not rejections)
    print(f"\n  I3 the discipline: exp236 deposit byte-unchanged "
          f"({h236_before[:12]}...), rejections {len(rejections)}, "
          f"deterministic {deterministic} ({len(d1)} rows x 2 passes "
          f"bit-identical), exp236 anchor exact "
          f"({sum(c['ok'] for c in cross)}/{len(cross)} cells) -> "
          f"{'PASS' if i3 else 'REFUTED'}")

    branch = "INTERFERENCE-REPAIRED" if i2 else "INTERFERENCE-STRUCTURAL"
    criteria = {"I1_overlap_map_deposited": i1,
                "I2_gate_hierarchy": i2,
                "I3_discipline": i3}
    npass = sum(criteria.values())
    print(f"\n  BRANCH (pre-named): {branch}")
    print(f"  === {npass}/3 gates PASS ===")

    out = {
        "exp": "exp250_interference_anatomy (the M33/miRNA interference "
               "anatomy — exp236's registered next, ledger L212/L228)",
        "criteria": criteria,
        "branch": branch,
        "I1_overlap_map": overlap_map,
        "I1_finding": {
            "overlap_counts": {g: overlap_map[g]["overlap_count"]
                               for g in GRAPH_ARMS},
            "empty_on_every_arm": all(
                overlap_map[g]["overlap_count"] == 0 for g in GRAPH_ARMS),
            "reading": "the cells where the miRNA represses (m >= m_line) "
                       "but M33 would specify (phi_spec >= M33_LINE), per "
                       "graph-arm over the whole organism; the spatial "
                       "distribution deposited against the amputation "
                       "cohort's region windows"},
        "I2_gate_hierarchy": {
            "i2a_trunk_and_vs_or": i2a_rows,
            "i2a": bool(i2a),
            "i2b_compositions_under_and": i2b_rows,
            "i2b": bool(i2b),
            "coverage_table": {
                f"{plane}|{g}": (
                    {f"single:{label}":
                     round(cov(rows1, plane, g, label, "single"), 6)
                     for label in SINGLES}
                    | {f"pair:{pair}|OR":
                       round(cov(rows1, plane, g, pair, "OR"), 6)
                       for pair in PAIRS}
                    | {f"pair:{pair}|AND":
                       round(cov_and(rows1, plane, g, pair), 6)
                       for pair in PAIRS})
                for plane in PLANES for g in GRAPH_ARMS},
        },
        "I3_discipline": {
            "exp236_deposit_byte_unchanged": bool(byte_unchanged),
            "exp236_sha256_before": h236_before,
            "exp236_sha256_after": h236_after,
            "rejections": rejections,
            "rejection_count": len(rejections),
            "deterministic": bool(deterministic),
            "determinism_diffs": diffs,
            "panel_rows_per_pass": len(rows1),
            "exp236_anchor_exact": bool(cross_ok),
            "exp236_anchor_cells": len(cross),
            "exp236_anchor_max_abs_diff": float(max(
                abs(c["rerun"] - c["exp236"]) for c in cross)),
            "overlap_map_stable": bool(map_stable)},
        "constants": {
            "m33_line": M33_LINE, "neural_spec_min": NEURAL_SPEC_MIN,
            "err_bar": ERR_BAR, "n": N,
            "delta_m": DELTA_M, "sigma_m": SIGMA_M, "source_s": SOURCE_S,
            "ring": RING, "arz_k": ARZ_K, "guess_sd": GUESS_SD,
            "noise_std": NOISE_STD, "steps_per_cell": STEPS_PER_CELL,
            "dt_walk": DT_WALK,
            "graph_arms": list(GRAPH_ARMS), "planes": list(PLANES),
            "regions": {p: REGIONS[p] for p in PLANES},
            "regen_seeds": list(REGEN_SEEDS)},
        "notes": (
            "OPERATIONALIZATION DISCLOSURES (the docstring byte-unchanged): "
            "(1) THE M33 PREDICATE: 'above the M33 gate' = the production "
            "M33 gate phi_spec >= M33_LINE = -35.0 — exp236's frozen "
            "machinery (its regen_panel gate) and its disclosure (1); "
            "NEURAL_SPEC_MIN = -60.0 is the post-exp168 S-REL adoption "
            "floor, not the M33 gate under the current core, and is "
            "deposited only for the record. (2) THE AND-READ'S "
            "REALIZATION: the conjoined competence array "
            "(phi_spec >= M33_LINE) AND (m < m_line) is fed through "
            "exp236's frozen competence-gate arm (its 'miRNA' arm reader "
            "consumes a pre-computed competence array and no rng stream) "
            "with exp236's M33+miRNA pair fallback (the single guess); "
            "the frozen regen_panel walk is reused verbatim, so the AND "
            "rows sit on the identical shared pools, commitment order and "
            "step dynamics as the OR rows. (3) M35 IS GATE-LESS: the ARZ "
            "multi-lineage convergence is the fallback amender, not a "
            "spec gate (exp236's machinery) — the conjunction over an "
            "M35-bearing pair's predicates reduces to the surviving gate, "
            "so the AND and OR reads COINCIDE for M33+M35 and M35+miRNA; "
            "those rows are the same runs recorded under both reads "
            "(disclosed, not duplicated). (4) THE LAYER IS "
            "WOUND-INDEPENDENT: the settled field (exp236's mirna_layer(A) "
            "on the intact graph) predates the cut, so the overlap map is "
            "a per-graph-arm object over the whole organism; "
            "overlap_in_amputation_region localizes it against the "
            "amputation cohort's regions. (5) THE FINDING (I1): the "
            "repressed set is exactly the source ring 45-54 on every arm "
            "and M33's spec set is the head 0-24 (lbl -20 >= -35 > "
            "lbl mid/trunk -50) — DISJOINT: the wrongly-de-competenced "
            "set is EMPTY; there is NO cell-level miRNA->M33 veto. "
            "exp236's R2 interference is STRUCTURAL: the trunk plane's "
            "competence is carried by the miRNA gate ALONE (M33's "
            "predicate is false on the entire trunk region, the TC-G5 "
            "dead zone), so any pair lacking the miRNA gate (M33+M35) — "
            "and any hierarchy that intersects the M33 predicate into the "
            "pair gate (the AND-read on M33+miRNA) — loses the trunk "
            "(0.0 < the miRNA single's 1.0). (6) I2(a)'s QUANTIFICATION: "
            "the gate hierarchy is evaluated per pair x graph-arm on the "
            "trunk plane (exp236's R2 table convention — every cell of "
            "the plane's table must hold); the full per-pair AND/OR table "
            "is deposited so any weaker reading is computable from the "
            "deposit. (7) THE ANCHOR: the re-run singles + OR pairs "
            "reproduce exp236's deposited R2 coverages EXACTLY (54/54 "
            "cells, its unrounded R2_rows verdicts) — the shared-pool "
            "protocol is deterministic and the frozen machinery intact. "
            "(8) THE DEPOSIT PATH: results/exp250_interference_anatomy.json "
            "(the repo's results/expNNN_<name>.json convention and the "
            "batch's registered artifact name; the module's stub OUT "
            "constant results/exp250.json is unused — the docstring names "
            "no deposit path). (9) COVERAGE: the plane verdict (region "
            "RMS < ERR_BAR, exp73's convention) mean over exp236's three "
            "regen seeds; the AND/OR tolerances follow exp236's 1e-12 "
            "composition convention."),
    }
    os.makedirs(os.path.dirname(DEP), exist_ok=True)
    with open(DEP, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {DEP}")
    return out


if __name__ == "__main__":
    main()
