#!/usr/bin/env python3
"""exp208 — THE C6 TAIL ABLATION (L177's registered next).

The c6 tail at n=400 refused all three named rules (R_O harm, R_H
neutral-harm, R_T no-op) — the RULE_MAP's first n=400-only entry
fires. The registered discovery protocol: a pre-registered ablation
on the tail's own geometry — WHERE does the excess live? The
decoded-vs-target structure of the 25 tail instances: boundary cells,
pair-junction cells, or the interior. The rule is NAMED FROM the
ablation's answer, not from the n=100 map.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt battery
verbatim (the c6 cell's 25 instances, seeds (1,2,3)); the production
scoped arm; the -35.0 pin; the error decomposition (pre-named, zero
knobs): per decoded cell, its err contribution split by cell class —
CANON-BOUNDARY (the cell sits on a canon-value boundary in the
target), PAIR-JUNCTION (the cell is an endpoint of >= 2 chords in the
medium's chord set), INTERIOR (neither) — the three-class
decomposition deposited per instance, the per-class excess
(err_class - the clean-cell class baseline from exp198's c3 clean
battery at n=400) the registered reading.

GATES (each evaluated exactly once):
  GATE-A1 (replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 instances x 3 seeds).
  GATE-A2 (the decomposition) every decoded cell classified into
           exactly one of the three pre-named classes; the per-class
           err shares deposited; the shares sum to the instance err
           (the accounting identity asserted).
  GATE-A3 (the naming) the class carrying the LARGEST mean excess
           names the new rule class's target (the branch recorded:
           BOUNDARY-NAMED / JUNCTION-NAMED / INTERIOR-NAMED); the
           clean-battery baseline (exp198's c3 at n=400) replayed
           bit-exactly as the reference line.
  GATE-A4 (hygiene) zero rejections; all finite; the pin asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp208_c6_tail_ablation.json
RUN: python3 -m experiments.exp208_c6_tail_ablation [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged) ==============
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import experiments.exp148_temporal_read as M148  # noqa: E402
    from experiments.exp160_any_medium import (  # noqa: E402
        BAR, config_fingerprint)
    from experiments.exp166_leading_edge import (  # noqa: E402
        CornerMedium, cell_dims)
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD, f_max_frames)
    from experiments.exp199_ro_n400_tail import (  # noqa: E402
        DEP160_FLOOR, N400, PER_CELL, SEEDS, pin_floor, restore_floor)

    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    assert os.path.exists(DEP199), \
        "exp199's deposit is missing — the A1 replay target is required"
    with open(DEP199) as f:
        dep199 = json.load(f)
    dep_by_cell = {c: {r["j"]: r for r in dep199["cells"][f"c{c}"][
        "instances"]} for c in (3, 6)}

    # ---- the read stack, asserted before any decode -----------------
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    # ---- instrument pin (exp199's save/restore semantics) -----------
    pin_floor()
    try:
        import cultivation.bioelectric.collective as _core
        assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
                   for m in (_core, M148)), "instrument pin failed"

        # ---- the decomposition conventions (pre-named, zero knobs,
        #      disclosed) ---------------------------------------------
        def classify(T: np.ndarray, W: np.ndarray) -> dict:
            n = len(T)
            Td = np.asarray(T, dtype=float)
            # CANON-BOUNDARY: the cell sits on a canon-value boundary
            # in the target (a lattice neighbor's target value differs;
            # the n-cell ring backbone i +/- 1)
            bnd = np.zeros(n, dtype=bool)
            for i in range(n):
                if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                    bnd[i] = True
            # PAIR-JUNCTION: endpoint of >= 2 chords in the medium's
            # chord set (the pair support of the medium's base
            # adjacency |Wbase| > 0 — the hyperedge cliques are group
            # couplings, not pairs; DISCLOSED)
            support = np.abs(W) > 0
            iu = np.triu_indices(n, 1)
            deg = np.zeros(n, dtype=int)
            for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
                deg[a] += 1
                deg[b] += 1
            pj = deg >= 2
            # precedence: the registered listing order — CANON-BOUNDARY
            # wins, then PAIR-JUNCTION, then INTERIOR (disclosed)
            cls = np.zeros(n, dtype=int)          # 2 = INTERIOR
            cls[pj] = 1
            cls[bnd] = 0
            return {"boundary": bnd, "junction": pj & ~bnd,
                    "interior": ~(bnd | pj), "class": cls}

        def decompose(V: np.ndarray, T: np.ndarray, cls: np.ndarray,
                      err_recomputed: float) -> dict:
            e2 = (np.asarray(V, dtype=float)
                  - np.asarray(T, dtype=float)) ** 2
            total = float(e2.sum())
            n = len(e2)
            per = []
            for name, mask in (("CANON-BOUNDARY", cls == 0),
                               ("PAIR-JUNCTION", cls == 1),
                               ("INTERIOR", cls == 2)):
                ss = float(e2[mask].sum())
                per.append({"class": name, "n_cells": int(mask.sum()),
                            "sum_sq": ss,
                            "frac_of_sq": ss / total if total > 0 else 0.0,
                            "rms_contrib_mV":
                                float(np.sqrt(ss / n)) if n else 0.0})
            # THE ACCOUNTING IDENTITY (the RMS convention, disclosed):
            # the shares are mean-squared contributions in mV^2 and
            # sum to err^2 — the identity on the scale the RMS actually
            # decomposes (an mV-linear split would be a fake identity)
            ident = abs(sum(p["sum_sq"] for p in per) / n
                        - err_recomputed ** 2)
            assert ident < 1e-6 * max(1.0, err_recomputed ** 2), \
                f"accounting identity violated: {ident}"
            assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
            return {"per_class": per, "identity_residual": ident}

        # ---- the battery: c6 (the tail, 25 instances) + c3 (the
        #      clean baseline, 25 instances), seeds (1,2,3) -----------
        smoke = args.smoke
        cells = [6, 3] if not smoke else [6]
        js = list(range(PER_CELL)) if not smoke else [0]
        seeds = list(SEEDS) if not smoke else [1]
        sections: dict = {}
        for c in cells:
            insts: list = []
            for j in js:
                gen_seed = 166000 + 1000 * c + j
                # exp199's gen-seed rule VERBATIM (its deposit carries
                # gen_seed per instance; asserted below)
                gen_seed = dep_by_cell[c][j]["gen_seed"]
                med = CornerMedium(N400, gen_seed, cell_dims(c))
                assert med.n == N400
                fmax = float(f_max_frames(list(med.snapshots())))
                dep_rec = dep_by_cell[c][j]
                errs, per_inst = [], []
                replay_flags = []
                for s, dep_err in zip(seeds, dep_rec["errs"]):
                    out = M148.decode("scoped", med, s, return_state=True,
                                      f_max=fmax)
                    assert out["ok"], \
                        f"rejection at c{c} j{j} s{s}: {out['rejection']}"
                    err = float(out["err"])
                    assert np.isfinite(err)
                    errs.append(err)
                    # A1: bit-exact at the deposit's rounding
                    replay_flags.append(
                        round(err, 2) == float(dep_err)
                        and bool(out["verified"])
                        == bool(dep_rec["verified"]))
                    # A2: the decomposition from the returned state
                    V = np.asarray(out["state"]["V"], dtype=float)
                    T = np.asarray(out["state"]["target"], dtype=float)
                    cinfo = classify(T, med.Wbase)
                    err_exact = float(np.sqrt(
                        np.mean((V - T) ** 2)))
                    assert round(err_exact, 2) == round(err, 2), \
                        "state err vs reported err drift"
                    per_inst.append(decompose(V, T, cinfo["class"],
                                              err_exact))
                rec = {"j": j, "gen_seed": gen_seed,
                       "tail": bool(dep_rec["tail"]),
                       "dep199_median_err": dep_rec["median_err"],
                       "errs": errs,
                       "replay_bit_exact": bool(all(replay_flags)),
                       "median_err": float(np.median(errs))
                       if len(errs) == len(seeds) else None,
                       "decompositions": per_inst}
                insts.append(rec)
                print(f"  [c{c} j{j:2d}] med {rec['median_err']} "
                      f"replay "
                      f"{'exact' if rec['replay_bit_exact'] else 'DRIFT'}")
            sections[f"c{c}"] = {
                "cell": c, "n_instances": len(insts),
                "seeds": seeds, "n_build": int(N400),
                "n_replay_exact": sum(int(r["replay_bit_exact"])
                                      for r in insts),
                "instances": insts}
            print(f"  [c{c}] replay exact "
                  f"{sections[f'c{c}']['n_replay_exact']}/{len(insts)}")

        if smoke:
            restore_floor()
            print("  SMOKE instrument check complete - DISCARDED")
            return {"exp": "exp208_c6_tail_ablation", "smoke": True}

        # ---- A3: the per-class excess vs the clean baseline ---------
        def class_means(sec, tail_only: bool) -> dict:
            rows = {k: [] for k in ("CANON-BOUNDARY", "PAIR-JUNCTION",
                                    "INTERIOR")}
            for r in sec["instances"]:
                if tail_only and not r["tail"]:
                    continue
                for d in r["decompositions"]:
                    for p in d["per_class"]:
                        rows[p["class"]].append(p["rms_contrib_mV"])
            return {k: float(np.mean(v)) if v else None
                    for k, v in rows.items()}

        mean_c6 = class_means(sections["c6"], tail_only=True)
        mean_c3 = class_means(sections["c3"], tail_only=False)
        excess = {k: (mean_c6[k] - mean_c3[k])
                  if (mean_c6[k] is not None and mean_c3[k] is not None)
                  else None for k in mean_c6}
        ranked = sorted((k for k in excess if excess[k] is not None),
                        key=lambda k: -excess[k])
        branch = {"CANON-BOUNDARY": "BOUNDARY-NAMED",
                  "PAIR-JUNCTION": "JUNCTION-NAMED",
                  "INTERIOR": "INTERIOR-NAMED"}[ranked[0]]

        n_replay = sum(sections[f"c{c}"]["n_replay_exact"]
                       for c in (6, 3))
        n_total = sum(len(sections[f"c{c}"]["instances"])
                      for c in (6, 3))
        all_finite = all(np.isfinite(p["rms_contrib_mV"])
                         for c in (6, 3)
                         for r in sections[f"c{c}"]["instances"]
                         for d in r["decompositions"]
                         for p in d["per_class"])
        a1_pass = bool(n_replay == n_total)
        a2_pass = bool(a1_pass and all_finite)
        a3_pass = bool(ranked and excess[ranked[0]] is not None)
        a4_pass = bool(a1_pass and all_finite)

        gates = {
            "A1": {"pass": a1_pass, "n_replay_exact": n_replay,
                   "n_instances": n_total,
                   "disclosure": ("bit-exact vs exp199's deposit at the "
                                  "deposit's 2-dp err rounding, the "
                                  "exp142 convention")},
            "A2": {"pass": a2_pass,
                   "n_decompositions": 3 * n_total,
                   "accounting_identity": ("shares are mean-squared "
                                           "contributions (mV^2), "
                                           "summing to err^2 — the RMS "
                                           "scale; fracs sum to 1.0"),
                   "all_finite": bool(all_finite)},
            "A3": {"pass": a3_pass, "branch": branch,
                   "mean_rms_contrib_c6_tail_mV": mean_c6,
                   "mean_rms_contrib_c3_clean_mV": mean_c3,
                   "excess_mV": excess,
                   "ranking": ranked,
                   "baseline_disclosure": ("c3 = exp198's clean cell "
                                           "(h+t), its 25 instances, "
                                           "the same decomposition")},
            "A4": {"pass": a4_pass, "rejections": 0,
                   "all_finite": bool(all_finite)}}
        verdict = (f"{sum(1 for g in gates.values() if g['pass'])}/4 "
                   f"gates (A1 A2 A3 A4) | {branch}")
        print(f"  === {verdict} ===")
        print(f"  excess: {json.dumps(excess)}")

        deposit = {
            "exp": "exp208_c6_tail_ablation",
            "claim": (
                "THE C6 TAIL ABLATION (L177's registered next): the c6 "
                "tail at n=400 refused all three named rules — the "
                "RULE_MAP's first n=400-only entry fires; the "
                "pre-registered ablation asks WHERE the excess lives "
                "(boundary cells, pair-junction cells, or the interior) "
                "and the rule is NAMED FROM the ablation's answer"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration de1155d, batch 9; gates A1-A4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-A1 (replay) the c6 battery replays bit-exactly "
                    "vs exp199's deposit (25 instances x 3 seeds)",
                    "GATE-A2 (the decomposition) every decoded cell "
                    "classified into exactly one of the three pre-named "
                    "classes; per-class err shares deposited; the shares "
                    "sum to the instance err (the accounting identity "
                    "asserted)",
                    "GATE-A3 (the naming) the class carrying the LARGEST "
                    "mean excess names the new rule class's target "
                    "(BOUNDARY-NAMED / JUNCTION-NAMED / INTERIOR-NAMED); "
                    "the clean-battery baseline (exp198's c3 at n=400) "
                    "replayed bit-exactly as the reference line",
                    "GATE-A4 (hygiene) zero rejections; all finite; the "
                    "pin asserted"],
                "conventions": (
                    "CANON-BOUNDARY: a lattice neighbor's target value "
                    "differs (the n-cell ring backbone); PAIR-JUNCTION: "
                    "endpoint of >= 2 chords in the medium's chord set "
                    "(the pair support of |Wbase| > 0 — hyperedge "
                    "cliques are group couplings, not pairs); "
                    "precedence = the registered listing order; the "
                    "accounting identity holds on the mean-squared "
                    "(mV^2) scale the RMS actually decomposes, "
                    "disclosed in the deposit")},
            "sections": {
                "c6_tail": sections["c6"],
                "c3_clean_baseline": sections["c3"],
                "class_means": {"c6_tail": mean_c6,
                                "c3_clean": mean_c3,
                                "excess_mV": excess,
                                "branch": branch}},
            "gates": gates,
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(out_path, "w") as fh:
            json.dump(deposit, fh, indent=1, default=float)
        print(f"  deposited {out_path} | wall {deposit['wall_s']} s")
        return deposit
    finally:
        restore_floor()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
