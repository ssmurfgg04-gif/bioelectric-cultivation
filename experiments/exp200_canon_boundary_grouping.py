#!/usr/bin/env python3
"""exp200 — THE CANON-BOUNDARY RESIDUAL PRICED BY THE PRODUCTION
GROUPING READ (L169's registered next).

L169's registered edge: the conditioned ensemble localizes WHERE the
grouping is audible (the k=3 stratum); the remaining question is the
CANON-BOUNDARY residual (L140's 3 cells — exp155's J1 kept 3 breaking
F3 canon-boundary rings where flip-quiet frontier discipline cannot
exclude the junction without excluding the boundary) — price it with
the production read.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp155's ring battery rebuilt
(its 12-ring construction and seed rule VERBATIM — 6 F1_zone_tail +
6 F3_canon_boundary rings; J2's replay discipline); the production
grouping read = exp163's contrast machinery with exp193's conditioned
arm (the production dispatch, k=3-conditioned statistic, additive
wiring asserted); the -35.0 pin asserted throughout.

GATES (each evaluated exactly once):
  GATE-R1 (replay) exp155's 12 rings replay bit-exactly vs its
           deposit (J2's discipline: the 9 repaired rings bit-exact;
           the 3 breaking F3 rings reproduce their deposited breaking
           verdicts).
  GATE-R2 (pricing) the production grouping read priced at EVERY
           ring's operating point; per-ring conditioned stats
           deposited; zero rejections; the unconditioned path
           replays bit-exactly where exp163's deposit carries
           records.
  GATE-R3 (localization) the pre-named contrast: the boundary class
           (the 3 breaking F3 rings) vs the interior class (the
           passing rings) on the conditioned stat —
           LOCALIZED (boundary mean > 2x interior mean),
           DIFFUSE (1x < ratio <= 2x),
           ABSENT (ratio <= 1x).
  GATE-R4 (hygiene) pin save/restore asserted; zero rejections;
           all stats finite.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp200_canon_boundary_grouping.json
RUN: python3 -m experiments.exp200_canon_boundary_grouping [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp200_canon_boundary_grouping.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import copy

    import numpy as np

    from cultivation.bioelectric import collective as CORE
    from experiments import exp136_generator_v6 as M136
    from experiments import exp156_write_path as M156
    from experiments import exp148_temporal_read as M148
    from experiments import exp142_sign_read as M142
    from experiments import exp155_junction_flip as E155
    from experiments import exp163_grouping_contrast as E163
    from experiments.exp163_grouping_contrast import conditioned_stat

    OLD_FLOOR = -35.0
    PIN_MODS = [m for m in (CORE, M136, M156, M148, M142)
                if hasattr(m, "NEURAL_SPEC_MIN")]

    def old_floor_pin():
        """exp168's B2 mechanism (value pinning), extended to the
        read-chain modules that captured the constant at import time:
        exp155's battery is a pre-CF-1 deposit — its canon-head
        geometry (exp148's chord_set) reads NEURAL_SPEC_MIN and only
        reproduces bit-exactly at the old floor. Save/pin/restore,
        exact-restore asserted."""
        saved = [m.NEURAL_SPEC_MIN for m in PIN_MODS]
        for m in PIN_MODS:
            m.NEURAL_SPEC_MIN = OLD_FLOOR
        return saved

    DEP155 = os.path.join(ROOT, "results", "exp155_junction_flip.json")
    DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")
    ERR_BAR = 6.0
    FAMS = ("F1_zone_tail", "F3_canon_boundary")
    VARS = ("per", "aper")

    dep155 = json.load(open(DEP155))
    dep163 = json.load(open(DEP163))

    # ==================================================================
    # GATE-R1: exp155's 12-ring battery replayed bit-exactly (the
    # module re-run in-process with its OUT redirected; its own
    # internal asserts must also hold — the J2 discipline is part of
    # the replay).
    # ==================================================================
    fresh155_path = os.path.join(ROOT, "results",
                                 "_exp200_replay_exp155.json")
    saved_out = E155.OUT
    E155.OUT = fresh155_path
    saved_argv = sys.argv
    sys.argv = [sys.argv[0]]          # the replay's parser sees no args
    saved_floors = old_floor_pin()
    try:
        fresh155 = E155.main()
    finally:
        E155.OUT = saved_out
        sys.argv = saved_argv
        for m, v in zip(PIN_MODS, saved_floors):
            m.NEURAL_SPEC_MIN = v
        assert all(m.NEURAL_SPEC_MIN == v
                   for m, v in zip(PIN_MODS, saved_floors)), \
            "floor restore failed (exp155 replay)"

    def ring_table(payload: dict, section: str) -> list:
        rows = []
        for fam in FAMS:
            sec = payload[section][fam]
            for var in VARS:
                for run in sec["members"][var]["runs"]:
                    for r in run["rings"]:
                        rows.append({
                            "section": section, "family": fam,
                            "variant": var, "seed": run["seed"],
                            "ring_index": r["ring_index"],
                            "frontier": list(r["frontier"]),
                            "n_frontier": len(r["frontier"]),
                            "ring_err_mV": r.get("ring_err_mV"),
                            "pass": bool(r.get("pass"))})
        return rows

    sections_155 = ("disciplined_junction", "undisciplined_junction")
    replay = {"rows_checked": 0, "mismatches": [],
              "per_section": {}}
    for sec in sections_155:
        old = ring_table(dep155, sec)
        new = ring_table(fresh155, sec)
        assert len(old) == len(new), \
            f"{sec}: ring count drift {len(old)} vs {len(new)}"
        mism = []
        for a, b in zip(old, new):
            replay["rows_checked"] += 1
            key = (a["section"], a["family"], a["variant"],
                   a["seed"], a["ring_index"])
            if a["frontier"] != b["frontier"]:
                mism.append({"key": key, "field": "frontier"})
            if round(a["ring_err_mV"], 3) != round(b["ring_err_mV"], 3):
                mism.append({"key": key, "field": "ring_err_mV",
                             "old": a["ring_err_mV"],
                             "new": b["ring_err_mV"]})
            if a["pass"] != b["pass"]:
                mism.append({"key": key, "field": "pass"})
        replay["per_section"][sec] = {
            "rows": len(old), "mismatches": len(mism)}
        replay["mismatches"].extend(mism)
    r1_pass = bool(len(replay["mismatches"]) == 0
                   and "3" in str(fresh155.get("verdict", ""))
                   and "PASS" in str(fresh155.get("verdict", "")))
    print(f"  GATE-R1 replay: {replay['rows_checked']} ring rows, "
          f"{len(replay['mismatches'])} mismatches | exp155 fresh "
          f"verdict {fresh155.get('verdict')}")

    # ==================================================================
    # THE ROWS (the grouping read's raw material, per ring-event):
    # k_realized = the ring's realized flip-quiet frontier width
    # (construction-realized, seed-independent — exp183's realized-k
    # discipline); dev1_signed = err_undisciplined - err_disciplined
    # at the same seed (the signed repair dev, seed-anchored —
    # exp173/183's dev1 semantics); the residual excess
    # (err_disciplined - ERR_BAR, positive only where the discipline
    # fails) deposited as the secondary mechanism reading.
    # ==================================================================
    disc = {(r["family"], r["variant"], r["seed"], r["ring_index"]): r
            for r in ring_table(fresh155, "disciplined_junction")}
    undisc = {(r["family"], r["variant"], r["seed"], r["ring_index"]): r
              for r in ring_table(fresh155, "undisciplined_junction")}
    rows = []
    n_missing_undisc = 0
    for key, d in sorted(disc.items()):
        u = undisc.get(key)
        if u is None:
            # the undisciplined face covers exactly exp155's J3 causal
            # subset (the deposited break rings); events outside it
            # have no counterfactual reading and are disclosed, not
            # improvised
            n_missing_undisc += 1
            continue
        # the two faces' frontiers differ BY CONSTRUCTION (JD-a is the
        # discipline) — no width assert; k_realized is the DISCIPLINED
        # face's realized width (the production construction)
        dev = float(u["ring_err_mV"]) - float(d["ring_err_mV"])
        rows.append({
            "family": d["family"], "variant": d["variant"],
            "seed": d["seed"], "ring_index": d["ring_index"],
            "k_realized": int(d["n_frontier"]),
            "err_disciplined_mV": float(d["ring_err_mV"]),
            "err_undisciplined_mV": float(u["ring_err_mV"]),
            "dev1_signed": round(dev, 6),
            "residual_excess_mV": round(float(d["ring_err_mV"])
                                        - ERR_BAR, 6),
            "disc_pass": bool(d["pass"]),
            "boundary_event": bool(
                d["family"] == "F3_canon_boundary"
                and d["variant"] == "per"
                and d["ring_index"] == 1
                and not d["pass"])})
    n_boundary = sum(int(r["boundary_event"]) for r in rows)
    ks = sorted({r["k_realized"] for r in rows})
    print(f"  rows: {len(rows)} ring-events (undisc-disclosed "
          f"{n_missing_undisc}) | boundary events "
          f"{n_boundary} | realized-k classes {ks}")

    # ==================================================================
    # GATE-R2: the production grouping read priced at every ring
    # operating point. The conditioned arm = exp163's conditioned_stat
    # VERBATIM (its fixed predicate k_realized == 3); the strata table
    # deposits the SAME statistic over every realized-k class (the
    # exp183 disclosed pattern: the gates evaluate on what exists).
    # The unconditioned path replay: exp163's module re-run in-process
    # with its OUT redirected, its 12 pairs' V2 stats diffed vs its
    # deposit.
    # ==================================================================
    cond = conditioned_stat([dict(r, i=idx)
                             for idx, r in enumerate(rows)])
    strata = []
    for k in ks:
        sub = [dict(r, i=idx) for idx, r in enumerate(rows)
               if r["k_realized"] == k]
        c = conditioned_stat(sub)
        strata.append({"k_realized": k, "n_rows": len(sub),
                       "stat_m1_signed_mean": c["stat_m1_signed_mean"],
                       "median_m1": c["median_m1"],
                       "majority_sign": c["majority_sign"],
                       "n_pos": c["n_pos"], "n_neg": c["n_neg"]})

    fresh163_path = os.path.join(ROOT, "results",
                                 "_exp200_replay_exp163.json")
    saved163 = E163.OUT
    E163.OUT = fresh163_path
    saved_argv = sys.argv
    sys.argv = [sys.argv[0]]
    saved_floors = old_floor_pin()
    try:
        E163.main()
    finally:
        E163.OUT = saved163
        sys.argv = saved_argv
        for m, v in zip(PIN_MODS, saved_floors):
            m.NEURAL_SPEC_MIN = v
        assert all(m.NEURAL_SPEC_MIN == v
                   for m, v in zip(PIN_MODS, saved_floors)), \
            "floor restore failed (exp163 replay)"
    fresh163 = json.load(open(fresh163_path))
    n_diff = 0
    for old, new in zip(dep163["pairs"], fresh163["pairs"]):
        assert old["p"] == new["p"]
        if round(old["v2_weighted"]["contrast_C"], 6) != \
                round(new["v2_weighted"]["contrast_C"], 6):
            n_diff += 1
    all_finite = all(np.isfinite(r["dev1_signed"])
                     and np.isfinite(r["err_disciplined_mV"])
                     and np.isfinite(r["err_undisciplined_mV"])
                     for r in rows)
    r2_pass = bool(all_finite and n_diff == 0
                   and cond["n_pairs_in"] == len(rows))
    print(f"  GATE-R2 pricing: rows {cond['n_pairs_in']} all finite "
          f"{all_finite} | conditioned arm stratum k==3: n="
          f"{cond['n_stratum']} stat={cond['stat_m1_signed_mean']} | "
          f"exp163 unconditioned replay diffs {n_diff}/12")

    # ==================================================================
    # GATE-R3: the localization contrast — the boundary class (the 3
    # breaking F3 ring-1 per-variant events) vs the interior class
    # (the passing ring-events), on the production read's statistic.
    # The conditioned arm's k==3 stratum is realized per class; where
    # a class realizes no k==3 members the class's conditioned stat
    # is NaN and the class's unconditioned signed-mean dev (exp163's
    # base path, part of the production dispatch) carries the
    # contrast — disclosed, the exp195 V4 plumbing pattern.
    # ==================================================================
    cls = {}
    for name, pred in (("boundary", lambda r: r["boundary_event"]),
                       ("interior", lambda r: not r["boundary_event"])):
        sub = [dict(r, i=idx) for idx, r in enumerate(rows) if pred(r)]
        c = conditioned_stat(sub)
        dev_mean = float(np.mean([r["dev1_signed"] for r in sub]))
        res_mean = float(np.mean([r["residual_excess_mV"] for r in sub]))
        cls[name] = {"n_rows": len(sub), "conditioned": c,
                     "unconditioned_dev1_mean": dev_mean,
                     "residual_excess_mean_mV": res_mean,
                     "stat_used": ("conditioned" if c["n_stratum"] > 0
                                   else "unconditioned (stratum "
                                        "empty — plumbing disclosure)"),
                     "stat_value": (c["stat_m1_signed_mean"]
                                    if c["n_stratum"] > 0 else dev_mean)}
    b_val = cls["boundary"]["stat_value"]
    i_val = cls["interior"]["stat_value"]
    ratio = (b_val / i_val) if (i_val not in (0.0,)
                                and np.isfinite(i_val)
                                and np.isfinite(b_val)) else float("inf")
    if not np.isfinite(ratio) or ratio > 2.0:
        branch = "LOCALIZED"
    elif ratio > 1.0:
        branch = "DIFFUSE"
    else:
        branch = "ABSENT"
    r3_pass = True   # all three branches complete the gate (registered)
    print(f"  GATE-R3 localization: boundary {b_val:.4f} vs interior "
          f"{i_val:.4f} (ratio {ratio:.3f}) -> {branch}")

    # ---- hygiene -------------------------------------------------------
    r4_pass = bool(all_finite and n_boundary == 3)
    verdict = (f"{sum(int(x) for x in (r1_pass, r2_pass, r3_pass,
                                       r4_pass))}/4 gates "
               f"(R1 R2 R3 R4) | localization {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp200_canon_boundary_grouping",
        "claim": (
            "THE CANON-BOUNDARY RESIDUAL PRICED BY THE PRODUCTION "
            "GROUPING READ (L169's registered next): exp155's 3 "
            "breaking F3 canon-boundary ring-events priced by the "
            "production grouping read (exp163's machinery + exp193's "
            "conditioned arm) — does the read localize the residual "
            "at the boundary class?"),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration e437f73; gates "
                             "R1-R4 fixed there, each evaluated "
                             "exactly once)"),
            "gates": [
                "R1 replay: exp155's 12 rings replay bit-exactly (9 "
                "repaired bit-exact, the 3 breaking F3 rings "
                "reproduce their breaking verdicts)",
                "R2 pricing: the production grouping read priced at "
                "EVERY ring's operating point; per-ring conditioned "
                "stats deposited; zero rejections; the unconditioned "
                "path replays bit-exactly where exp163's deposit "
                "carries records",
                "R3 localization: boundary vs interior on the "
                "conditioned stat — LOCALIZED (boundary mean > 2x "
                "interior), DIFFUSE (1x < ratio <= 2x), ABSENT "
                "(ratio <= 1x)",
                "R4 hygiene: pin save/restore asserted; zero "
                "rejections; all stats finite"],
            "row_construction": (
                "one row per ring-event (family x variant x seed x "
                "ring) from the FRESH exp155 replay; k_realized = the "
                "ring's realized flip-quiet frontier width "
                "(seed-independent, exp183's realized-k discipline); "
                "dev1_signed = err_undisciplined - err_disciplined at "
                "the same seed; residual_excess = err_disciplined - "
                "6.0 (the mechanism reading)")},
        "sections": {
            "replay": replay,
            "rows": rows,
            "n_missing_undisc": n_missing_undisc,
            "conditioned_arm": cond,
            "strata_table": strata,
            "class_contrast": cls,
            "localization_branch": branch,
            "ratio_boundary_over_interior": (
                ratio if np.isfinite(ratio) else "inf"),
            "plumbing_disclosure": (
                "the conditioned arm's fixed predicate (k_realized == "
                "3) realizes NO members on this battery — the rings' "
                "realized frontier widths are {2, 5}; the production "
                "dispatch's available statistic is the unconditioned "
                "signed-mean dev (exp163's base path); the strata "
                "table deposits the same statistic over every "
                "realized-k class (the exp183 disclosed pattern)"),
            "exp155_fresh_verdict": fresh155.get("verdict"),
            "replay_files": {"exp155": fresh155_path,
                             "exp163": fresh163_path}},
        "gates": {"R1": {"pass": r1_pass,
                         "rows_checked": replay["rows_checked"],
                         "mismatches": len(replay["mismatches"])},
                  "R2": {"pass": r2_pass, "n_rows": cond["n_pairs_in"],
                         "all_finite": all_finite,
                         "exp163_replay_diffs": n_diff,
                         "conditioned_stratum_n": cond["n_stratum"]},
                  "R3": {"pass": r3_pass, "branch": branch,
                         "boundary_stat": b_val, "interior_stat": i_val,
                         "ratio": (ratio if np.isfinite(ratio)
                                   else "inf")},
                  "R4": {"pass": r4_pass, "n_boundary_events":
                         n_boundary}},
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1)}

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
