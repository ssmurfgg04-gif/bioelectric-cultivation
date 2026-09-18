#!/usr/bin/env python3
"""exp213 — THE BOUNDARY ARM AT n=400 (L185's registered next).

exp208's ablation NAMED the c6 tail's new rule class: the excess lives
at the CANON-BOUNDARY cells (+0.574 mV; interior 0.000 exactly) — the
boundary phenomenon independently reproducing exp200's n=100
localization. L185's registered next: the exp205/exp210 composed
machinery aimed at the corner battery's boundary cells — the
plane-resolved read face armed ONLY at the boundary cells of the 25
tail instances — the pre-named bar being the tail's 1.30 bar crossed
by a boundary-only arm with the interior bit-exact (exp205's identity
clause at n=400).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's battery verbatim (the
c6 cell's 25 instances, seeds (1,2,3), the scoped read); exp208's
decomposition machinery verbatim (the CANON-BOUNDARY classification,
the mV^2 accounting identity); the arm (pre-named, zero knobs): at
each tail instance the decoded V's boundary-cell values are replaced
by the plane-resolved read's emission (exp158's machinery at the
n=400 corner battery: the boundary cells read through the canon-plane
sub-window chain), every interior cell bit-unchanged.

GATES (each evaluated exactly once):
  GATE-B1 (replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 instances x 3 seeds) and exp208's per-class
           decomposition reproduces bit-exactly at the reference.
  GATE-B2 (the arm) the boundary-armed errs for all 25 instances x 3
           seeds; the branch named: REPAIR (median <= 1.30 — the
           tail's bar crossed), IMPROVED (median improved >= 20% vs
           1.40, bar not crossed), NONE.
  GATE-B3 (the identity clause) every interior cell's decoded value
           bit-unchanged by the arm (exp205's identity clause at
           n=400); the arm touches exactly the boundary cells.
  GATE-B4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp213_boundary_arm_n400.json
RUN: python3 -m experiments.exp213_boundary_arm_n400 [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp213_boundary_arm_n400.json")


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

    import numpy as np

    import cultivation.bioelectric.collective as _core
    import experiments.exp148_temporal_read as M148
    from experiments import exp155_junction_flip as E155
    from experiments.exp160_any_medium import config_fingerprint
    from experiments.exp166_leading_edge import CornerMedium, cell_dims
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    from experiments.exp199_ro_n400_tail import (
        DEP160_FLOOR, N400, PER_CELL, REPAIR_PCT, SEEDS, pin_floor,
        restore_floor)
    from experiments.exp94_multizone_scale import labeling_bfs_n

    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    DEP208 = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")
    for _p in (DEP199, DEP208):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    with open(DEP199) as f:
        dep199 = json.load(f)
    with open(DEP208) as f:
        dep208 = json.load(f)
    dep_by_cell = {r["j"]: r
                   for r in dep199["cells"]["c6"]["instances"]}
    dep208_by_j = {r["j"]: r
                   for r in dep208["sections"]["c6_tail"]["instances"]}

    # ---- the read stack, asserted before any decode -----------------
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    # ---- instrument pin (exp199's save/restore semantics) -----------
    floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                  for m in (_core, M148)]
    pin_floor()
    try:
        assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
                   for m in (_core, M148)), "instrument pin failed"

        OLD_FLOOR = DEP160_FLOOR

        class BatteryMember:
            """Interface adapter (disclosed, zero knobs — no rule
            lives here): the corner battery already satisfies the read
            chain (.snapshots()); E155.WindowQuietMedium additionally
            reads .A (the n x n base) and .T (the frame count) —
            exposed verbatim from the medium (A = Wbase, T = T_eff).
            The c6 battery is real and single-frame (cell_dims(6):
            temporal inactive), so the flip clock is identically zero
            on this battery — disclosed, not assumed: TC1 runs and
            returns zero the same as on any static medium."""

            def __init__(self, med):
                self.A = med.Wbase
                self.T = med.T_eff
                self._med = med

            def snapshots(self):
                return self._med.snapshots()

        # ---- exp208's classification VERBATIM (the pre-named classes,
        #      zero knobs; disclosed conventions) ----------------------
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
            ident = abs(sum(p["sum_sq"] for p in per) / n
                        - err_recomputed ** 2)
            assert ident < 1e-6 * max(1.0, err_recomputed ** 2), \
                f"accounting identity violated: {ident}"
            assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
            return {"per_class": per, "identity_residual": ident}

        # ---- THE CANON-PLANE MAP + THE FACE (exp205/exp210's
        #      machinery VERBATIM; the canon planes are the medium's
        #      OWN labeling — labeling_bfs_n on the battery's base
        #      support, head = canon >= the pinned NEURAL_SPEC_MIN) --
        def plane_of_map(W: np.ndarray) -> dict:
            canon = labeling_bfs_n(W)
            return {j: ("head" if canon[j] >= OLD_FLOOR else "tail")
                    for j in range(W.shape[0])}

        def plane_resolved_read(member, win: set, crossing: list,
                                s: int, plane_of: dict,
                                planes=("head", "tail"),
                                sweep: bool = False):
            """THE FACE. Returns (V_stitched, meta). exp205/exp210's
            face VERBATIM with ONE disclosed no-op guard: a canon
            plane with ZERO window cells is skipped (an empty
            sub-window reads nothing — the emission assignment on an
            empty pw would be a no-op; recorded in meta)."""
            n = member.A.shape[0]
            V = np.zeros(n)
            meta = {"planes": {}, "sweep_ok": None}
            outs = []
            for p in planes:
                pw = sorted(j for j in win if plane_of[j] == p)
                if not pw:
                    meta["planes"][p] = {
                        "n_nodes": 0, "nodes": [],
                        "n_crossing_zeroed": 0, "n_flip_entries": 0,
                        "program_verified": None,
                        "empty_window_noop": True}
                    continue
                pcross = [(i, j) for (i, j) in crossing
                          if i in pw and j in pw]
                wm = E155.WindowQuietMedium(member, pw, pcross)
                if sweep:
                    sw = wm.sweep_assert()
                    assert sw["ok"], f"plane window sweep failed ({p})"
                    if meta["sweep_ok"] is None:
                        meta["sweep_ok"] = True
                with E155.warnings_as_errors():
                    A0 = E155.project_phase_native(wm)[0]
                Fc = E155.flip_clock_matrix(wm)
                A_ext = A0 + Fc                # TC2 (verbatim)
                with E155.warnings_as_errors():
                    out = E155.execute_signed(E155.MULTI, A_ext, s,
                                              op=E155.STAR_OP,
                                              return_state=True)
                Vp = np.asarray(out["final_state"]["V"], dtype=float)
                V[pw] = Vp[pw]
                outs.append(bool(out.get("program_verified", False)))
                meta["planes"][p] = {
                    "n_nodes": len(pw),
                    "nodes": [int(x) for x in pw],
                    "n_crossing_zeroed": len(pcross),
                    "n_flip_entries": int(np.count_nonzero(Fc)),
                    "program_verified":
                        bool(out.get("program_verified", False))}
            meta["program_verified_all_planes"] = bool(all(outs))
            return V, meta

        seeds = list(SEEDS)
        smoke = args.smoke
        job = args.job
        SHARDS = {f"b{k}": list(range(k * 5, (k + 1) * 5))
                  for k in range(5)}
        js_all = list(range(PER_CELL))
        if smoke:
            js_all, seeds = [0], [1]

        def run_instance(j: int) -> dict:
            gen_seed = dep_by_cell[j]["gen_seed"]
            med = CornerMedium(N400, gen_seed, cell_dims(6))
            assert med.n == N400
            member = BatteryMember(med)
            fmax = float(f_max_frames(list(med.snapshots())))
            plane_of = plane_of_map(med.Wbase)
            dep_rec = dep_by_cell[j]
            ref = dep208_by_j[j]
            errs, armed_errs, per_inst, faces = [], [], [], []
            armed_bnd_rms = []
            replay_flags, ref_flags, ident_flags = [], [], []
            n_bnd = None
            for s_idx, (s, dep_err) in enumerate(
                    zip(seeds, dep_rec["errs"])):
                out = M148.decode("scoped", med, s, return_state=True,
                                  f_max=fmax)
                assert out["ok"], \
                    f"rejection at j{j} s{s}: {out['rejection']}"
                err = float(out["err"])
                assert np.isfinite(err)
                errs.append(err)
                # B1a: bit-exact at the deposit's rounding (exp142's
                # convention, exp208's replay discipline)
                replay_flags.append(
                    round(err, 2) == float(dep_err)
                    and bool(out["verified"])
                    == bool(dep_rec["verified"]))
                V = np.asarray(out["state"]["V"], dtype=float)
                T = np.asarray(out["state"]["target"], dtype=float)
                err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
                assert round(err_exact, 2) == round(err, 2), \
                    "state err vs reported err drift"
                cinfo = classify(T, med.Wbase)
                cls = cinfo["class"]
                bnd = cls == 0
                if n_bnd is None:
                    n_bnd = int(bnd.sum())
                # B1b: exp208's decomposition reproduces bit-exactly
                dec = decompose(V, T, cls, err_exact)
                ref_dec = ref["decompositions"][s_idx]
                ref_flags.append(all(
                    pc["sum_sq"] == rc["sum_sq"]
                    and pc["n_cells"] == rc["n_cells"]
                    for pc, rc in zip(dec["per_class"],
                                      ref_dec["per_class"])))
                per_inst.append(dec)
                # THE ARM (pre-named, zero knobs): the decoded V's
                # boundary-cell values replaced by the plane-resolved
                # read's emission; every interior cell bit-unchanged.
                win = {int(i) for i in np.where(bnd)[0]}
                V_face, face_meta = plane_resolved_read(
                    member, win, [], s, plane_of,
                    sweep=(s == seeds[0]))
                emitted_nodes = sorted(sum(
                    (face_meta["planes"][p]["nodes"]
                     for p in face_meta["planes"]), []))
                assert emitted_nodes == sorted(win), \
                    "the face's emission is not exactly the boundary set"
                win_arr = np.array(sorted(win), dtype=int)
                V_arm = V.copy()
                V_arm[win_arr] = V_face[win_arr]
                # B3: the identity clause — every non-boundary cell
                # bit-unchanged by the arm (exp205's identity clause
                # at n=400)
                ident_flags.append(
                    bool(np.array_equal(V_arm[~bnd], V[~bnd])))
                err_armed = float(np.sqrt(np.mean((V_arm - T) ** 2)))
                assert np.isfinite(err_armed)
                armed_errs.append(err_armed)
                # the boundary class's own residual under the arm
                # (deposited, not gated — the class the excess lives in)
                e2_arm = (V_arm - T) ** 2
                armed_bnd_rms.append(
                    float(np.sqrt(e2_arm[bnd].sum() / len(T))))
                faces.append({"seed": s, "face": face_meta})
            return {"j": j, "gen_seed": gen_seed,
                    "tail": bool(dep_rec["tail"]),
                    "dep199_median_err": dep_rec["median_err"],
                    "errs": errs,
                    "armed_errs": armed_errs,
                    "replay_bit_exact": bool(all(replay_flags)),
                    "decomposition_bit_exact": bool(all(ref_flags)),
                    "identity_bit_exact": bool(all(ident_flags)),
                    "median_err": float(np.median(errs))
                    if len(errs) == len(seeds) else None,
                    "armed_median_err": float(np.median(armed_errs))
                    if len(armed_errs) == len(seeds) else None,
                    "n_boundary_cells": n_bnd,
                    "armed_boundary_rms": armed_bnd_rms,
                    "decompositions": per_inst,
                    "faces": faces}

        # ---- --smoke: instrument subset only, discarded --------------
        if smoke:
            rec = run_instance(0)
            restore_floor()
            assert [getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in (_core, M148)] == floors_pre, \
                "floor restore failed (smoke)"
            print("  SMOKE instrument check complete - DISCARDED")
            return {"exp": "exp213_boundary_arm_n400", "smoke": True}

        # ---- the battery: c6 (the tail, 25 instances) -----------------
        js = SHARDS[job] if job in SHARDS else js_all
        insts: list = []
        for j in js:
            rec = run_instance(j)
            insts.append(rec)
            print(f"  [c6 j{j:2d}] med {rec['median_err']} -> armed "
                  f"{rec['armed_median_err']} "
                  f"(replay "
                  f"{'exact' if rec['replay_bit_exact'] else 'DRIFT'}, "
                  f"identity "
                  f"{'exact' if rec['identity_bit_exact'] else 'BROKEN'})")
        if job in SHARDS:
            shard = {"exp": "exp213_boundary_arm_n400",
                     "shard": job, "instances": insts}
            with open(out_path, "w") as fh:
                json.dump(shard, fh, indent=1, default=float)
            print(f"  shard {job} deposited {out_path}")
            return shard

        section = {"cell": 6, "n_instances": len(insts),
                   "seeds": list(SEEDS), "n_build": int(N400),
                   "n_replay_exact": sum(int(r["replay_bit_exact"])
                                         for r in insts),
                   "n_decomp_exact": sum(int(r["decomposition_bit_exact"])
                                         for r in insts),
                   "n_identity_exact": sum(int(r["identity_bit_exact"])
                                           for r in insts),
                   "instances": insts}
        print(f"  [c6] replay exact {section['n_replay_exact']}/"
              f"{len(insts)} | decomposition exact "
              f"{section['n_decomp_exact']}/{len(insts)} | identity "
              f"exact {section['n_identity_exact']}/{len(insts)}")

        # ---- B2: the branch (each clause evaluated exactly once) ------
        baseline_median = float(np.median(
            [dep_by_cell[j]["median_err"] for j in range(PER_CELL)]))
        BAR = 1.30                       # the tail's pre-named bar
        armed_medians = [r["armed_median_err"] for r in insts]
        armed_median = float(np.median(armed_medians))
        flat75 = float(np.median([e for r in insts
                                  for e in r["armed_errs"]]))
        improvement_pct = (100.0 * (baseline_median - armed_median)
                           / baseline_median)
        # The branch EXACTLY as pre-registered: REPAIR (median <= 1.30),
        # IMPROVED (median improved >= 20% vs 1.40, bar not crossed),
        # NONE. DISCLOSED: the pre-registered thresholds nest —
        # (1 - REPAIR_PCT/100) * 1.40 = 1.12 < 1.30 — so IMPROVED is
        # formally unreachable as written; implemented verbatim (no
        # post-hoc reinterpretation), the disclosure carries it.
        improved_bar = (1.0 - REPAIR_PCT / 100.0) * baseline_median
        if armed_median <= BAR:
            branch = "REPAIR"
        elif armed_median <= improved_bar:
            branch = "IMPROVED"
        else:
            branch = "NONE"
        # the boundary class's own residual shift (deposited, not gated):
        bnd_before = float(np.mean(
            [p["rms_contrib_mV"] for r in insts
             for d in r["decompositions"]
             for p in d["per_class"] if p["class"] == "CANON-BOUNDARY"]))
        bnd_armed = float(np.mean(
            [x for r in insts for x in r["armed_boundary_rms"]]))
        dep208_bnd = float(np.mean(
            [p["rms_contrib_mV"] for r in dep208_by_j.values()
             for d in r["decompositions"]
             for p in d["per_class"] if p["class"] == "CANON-BOUNDARY"]))

        n_replay = section["n_replay_exact"]
        n_total = len(insts)
        all_finite = all(np.isfinite(e) for r in insts
                         for e in (r["errs"] + r["armed_errs"]))
        b1_pass = bool(n_replay == n_total
                       and section["n_decomp_exact"] == n_total)
        b2_pass = bool(branch in ("REPAIR", "IMPROVED", "NONE"))
        b3_pass = bool(section["n_identity_exact"] == n_total)
        b4_pass = bool(all_finite)

        gates = {
            "B1": {"pass": b1_pass, "n_replay_exact": n_replay,
                   "n_decomposition_exact": section["n_decomp_exact"],
                   "n_instances": n_total,
                   "disclosure": ("errs bit-exact vs exp199's deposit at "
                                  "the deposit's 2-dp rounding (exp142's "
                                  "convention); exp208's per-class "
                                  "sum_sq reproduced bit-exactly "
                                  "(float ==, the decode is "
                                  "deterministic)")},
            "B2": {"pass": b2_pass, "branch": branch,
                   "baseline_median_dep199_c6": baseline_median,
                   "bar": BAR,
                   "armed_median_instance": armed_median,
                   "armed_median_flat75": flat75,
                   "improvement_pct": round(improvement_pct, 2),
                   "improved_bar_disclosed": improved_bar,
                   "nesting_disclosure": (
                       "IMPROVED's pre-registered clause (median <= "
                       "(1-0.20)*1.40 = 1.12) is nested under REPAIR's "
                       "1.30 bar as written; implemented verbatim, no "
                       "post-hoc reinterpretation"),
                   "boundary_class_rms_contrib_mV": {
                       "exp208_reference": dep208_bnd,
                       "exp213_replay_unarmed": bnd_before,
                       "armed": bnd_armed}},
            "B3": {"pass": b3_pass,
                   "n_identity_exact": section["n_identity_exact"],
                   "clause": ("every non-boundary cell's decoded value "
                              "bit-unchanged (np.array_equal); the "
                              "face's emission asserted == the boundary "
                              "set per decode")},
            "B4": {"pass": b4_pass, "rejections": 0,
                   "all_finite": bool(all_finite),
                   "pin_restore_asserted": True}}
        npass = sum(1 for g in gates.values() if g["pass"])
        verdict = (f"{npass}/4 gates (B1 B2 B3 B4) | {branch}")
        print(f"  === {verdict} ===")
        print(f"  armed median {armed_median} vs baseline "
              f"{baseline_median} (bar {BAR}, improvement "
              f"{improvement_pct:.1f}%)")

        restore_floor()
        assert [getattr(m, "NEURAL_SPEC_MIN", None)
                for m in (_core, M148)] == floors_pre, \
            "floor restore failed"

        deposit = {
            "exp": "exp213_boundary_arm_n400",
            "claim": (
                "THE BOUNDARY ARM AT n=400 (L185's registered next): "
                "exp208's ablation NAMED the c6 tail's new rule class "
                "(the excess lives at the CANON-BOUNDARY cells, "
                "interior 0.000 exactly) — the exp205/exp210 composed "
                "machinery aimed at the corner battery's boundary "
                "cells: the plane-resolved read face armed ONLY at the "
                "boundary cells of the 25 tail instances, the "
                "pre-named bar being the tail's 1.30 bar crossed by a "
                "boundary-only arm with the interior bit-exact "
                "(exp205's identity clause at n=400)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 08b1cfc, batch 10; gates B1-B4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-B1 (replay) the c6 battery replays bit-exactly "
                    "vs exp199's deposit (25 instances x 3 seeds) and "
                    "exp208's per-class decomposition reproduces "
                    "bit-exactly at the reference",
                    "GATE-B2 (the arm) the boundary-armed errs for all "
                    "25 instances x 3 seeds; the branch named: REPAIR "
                    "(median <= 1.30 — the tail's bar crossed), "
                    "IMPROVED (median improved >= 20% vs 1.40, bar not "
                    "crossed), NONE",
                    "GATE-B3 (the identity clause) every interior "
                    "cell's decoded value bit-unchanged by the arm "
                    "(exp205's identity clause at n=400); the arm "
                    "touches exactly the boundary cells",
                    "GATE-B4 (hygiene) zero rejections; all finite; "
                    "the -35.0 pin save/restore asserted (exp199's "
                    "semantics)"],
                "conventions": (
                    "the arm's window = the instance's CANON-BOUNDARY "
                    "cell set (exp208's classification verbatim); each "
                    "canon plane's induced sub-window (the plane's "
                    "boundary cells) decoded by the verbatim TC1/TC2/TC3 "
                    "chain, emission stitched per plane; crossing = [] "
                    "(no committed cone exists in the battery decode — "
                    "disclosed); the canon planes are the medium's OWN "
                    "labeling (labeling_bfs_n on the battery's base "
                    "support); empty plane windows are recorded no-ops "
                    "(disclosed)")},
            "sections": {"c6_tail": section},
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
