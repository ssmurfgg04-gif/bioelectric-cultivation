#!/usr/bin/env python3
"""exp229 — THE CURVATURE TEST (L202's registered next).

exp226's PARTIAL-TRACKING left a genuine boundary structure: ~150x
inside the smoothing bound in magnitude, tracking the step response
only partially (rho 0.545). The registered identity test: the
residual's structure decomposed against the plan's SECOND difference
(the curvature, not the step). If the residual tracks the plan's
curvature, the excess is the pattern's own geometry read through the
substrate; the branch: CURVATURE-TRACKED / GENUINE-EXCESS.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp226's machinery verbatim
(the battery, the replay anchors, the residual rows r_i, the
disclosures — the D_i = 0 points kept, the alternates audit-only);
the CURVATURE INSTRUMENT (pre-named, zero knobs): K_i = |T_plan[i-1]
- 2*T_plan[i] + T_plan[i+1]| on the ring backbone (the plan's second
difference at cell i); the clause: Spearman(r_i, K_i) across the same
10,047 canon-boundary points.

GATES (each evaluated exactly once):
  GATE-K1 (the replay) exp226's anchors reproduce (exp199 bit-exact
           25/25 + exp208's decomposition bit-exact).
  GATE-K2 (the curvature clause) the branch named: CURVATURE-TRACKED
           (rho >= 0.6) / MIXED (0.3 <= rho < 0.6) / GENUINE-EXCESS
           (rho < 0.3).
  GATE-K3 (the joint reading) the partial-correlation of r_i with
           K_i controlling for S_i * D_i (exp226's instrument)
           deposited; the three-way attribution (step, curvature,
           unexplained) deposited as shares of rank variance.
  GATE-K4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp229_curvature_test.json
RUN: python3 -m experiments.exp229_curvature_test [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp229_curvature_test.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only
    # discipline; docstring/imports/constants above byte-unchanged —
    # the gates below are the docstring's, each evaluated exactly
    # once) ==============================================================
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
    from scipy.stats import rankdata

    import experiments.exp148_temporal_read as M148
    from cultivation.validation.stats import spearman_ties
    from experiments.exp145_phase_read import project_phase_native
    from experiments.exp160_any_medium import config_fingerprint
    from experiments.exp166_leading_edge import CornerMedium, cell_dims
    # exp169's import BEFORE exp199's (exp213's import order): the
    # exp169-import sets the production -35.0 floor across the pin
    # modules (the corpus's disclosed "exp169-import restore"), and
    # exp199's _PIN_SAVE must snapshot THAT state so restore_floor()
    # lands exactly at the pre-run floors (asserted in K4)
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp199_ro_n400_tail as M199
    from experiments.exp199_ro_n400_tail import (
        DEP160_FLOOR, N400, PER_CELL, SEEDS, pin_floor, restore_floor)

    # ---- K1's reference deposits (exp226's anchors) ----------------------
    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    DEP208 = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")
    DEP226 = os.path.join(ROOT, "results",
                          "exp226_boundary_dynamics_test.json")
    for _p in (DEP199, DEP208, DEP226):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    with open(DEP199) as f:
        dep199 = json.load(f)
    with open(DEP208) as f:
        dep208 = json.load(f)
    with open(DEP226) as f:
        dep226 = json.load(f)
    dep_by_cell = {r["j"]: r
                   for r in dep199["cells"]["c6"]["instances"]}
    dep208_by_j = {r["j"]: r
                   for r in dep208["sections"]["c6_tail"]["instances"]}
    # exp226's deposited rho (audit-only continuity for K3, never gated)
    rho_rX_exp226 = float(dep226["gates"]["R2"]["rho"])
    n_points_exp226 = int(dep226["gates"]["R2"]["n_points"])

    # ---- the read stack, asserted before any decode (exp226 verbatim) ---
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    # ---- exp208's classification + decomposition VERBATIM (the
    #      pre-named classes, zero knobs; disclosed conventions) ---------
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

    # ---- exp226's instruments VERBATIM (the step + the smoothing
    #      response; exp229 adds NO new substrate machinery) --------------
    # S_i: the plan's local step at boundary cell i — the max absolute
    # T_plan difference from i to its lattice (ring-backbone i +/- 1)
    # neighbors (exp208's boundary lattice). The across-the-two-
    # neighbors reading is computed alongside as an audit-only
    # alternate (never gated).
    # D_i: the substrate's one-step diffusion response — the
    # ring-averaged |W[i,.]|-weighted neighbor value spread; W = the
    # projected kernel the scoped read's dynamics implements (exp145's
    # project_phase_native — the exact matrix exp142's executor hands
    # GraphCollective as G = A * g_gap; asserted real non-negative on
    # c6). D_i = 0 points are KEPT, not dropped (dropping would be
    # tuning; disclosed as in exp226).
    # r_i: the per-cell residual — the mV^2 summand of exp208's
    # decomposition rows, (V - T)^2 at the cell.
    def local_step(T: np.ndarray, i: int) -> float:
        n = len(T)
        return max(abs(float(T[i]) - float(T[(i - 1) % n])),
                   abs(float(T[i]) - float(T[(i + 1) % n])))

    def alt_step(T: np.ndarray, i: int) -> float:
        # audit-only alternate reading (never gated)
        n = len(T)
        return abs(float(T[(i - 1) % n]) - float(T[(i + 1) % n]))

    def smoothing_rows(T: np.ndarray, Wmat: np.ndarray,
                       idx: np.ndarray) -> np.ndarray:
        Ws = np.abs(Wmat[idx, :].astype(float))
        dT = np.abs(T[None, :] - T[idx][:, None])
        den = Ws.sum(axis=1)
        assert np.all(den > 0.0), "empty coupling row"
        return (Ws * dT).sum(axis=1) / den

    # ---- THE CURVATURE INSTRUMENT (pre-named, zero knobs) ---------------
    # K_i = |T_plan[i-1] - 2*T_plan[i] + T_plan[i+1]| on the ring
    # backbone (the plan's SECOND difference at cell i). Zero is a
    # legitimate reading — a locally linear plan segment has no
    # curvature (e.g. a monotone ramp's middle cell is on a
    # canon-boundary with K_i = 0); such points are KEPT, Spearman's
    # tie handling ranks them together, dropping them would be tuning.
    def curvature(T: np.ndarray, i: int) -> float:
        n = len(T)
        return abs(float(T[(i - 1) % n]) - 2.0 * float(T[i])
                   + float(T[(i + 1) % n]))

    # ---- the battery: c6 (the tail, 25 instances), seeds (1,2,3) --------
    smoke = args.smoke
    seeds = list(SEEDS) if not smoke else [1]
    SHARDS = {f"b{k}": list(range(k * 5, (k + 1) * 5))
              for k in range(5)}
    js_run = ([0] if smoke else
              (SHARDS[args.job] if args.job in SHARDS
               else list(range(PER_CELL))))

    # ---- instrument pin (exp199's semantics, save/restore asserted) -----
    pin_modules = list(M199.PIN_MODULES)
    floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                  for m in pin_modules]
    pin_floor()
    n_rejections = 0
    rejection_records: list = []
    try:
        assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
                   for m in pin_modules), "instrument pin failed"

        insts: list = []
        pooled_r: list = []
        pooled_x: list = []          # S_i * D_i (exp226's instrument,
        #                             K3's control)
        pooled_k: list = []          # K_i (the curvature instrument)
        pooled_x_walt: list = []     # S_i * D_i(|Wbase| row) — audit only
        pooled_x_salt: list = []     # S_alt_i * D_i — audit only
        n_degenerate_D0 = 0          # D_i = 0 points (x = S*D = 0;
        #                             kept, counted, disclosed — NOT
        #                             dropped: dropping would be
        #                             tuning; exp226's disclosure)
        n_zero_curv = 0              # K_i = 0 points (locally linear
        #                             plan segments; kept, ties ranked
        #                             together, disclosed)
        for j in js_run:
            dep_rec = dep_by_cell[j]
            # exp199's gen-seed rule via its own deposit (exp208's
            # replay discipline, disclosed)
            gen_seed = dep_rec["gen_seed"]
            med = CornerMedium(N400, gen_seed, cell_dims(6))
            assert med.n == N400
            fmax = float(f_max_frames(list(med.snapshots())))
            # the dynamics' own kernel row (the medium's own weights
            # as the read's projection delivers them to the executor)
            A_dyn, rho_pn, branch_pn = project_phase_native(med)
            assert not np.iscomplexobj(A_dyn)
            assert float(A_dyn.min()) >= 0.0, \
                "c6 kernel row expected real non-negative"
            Wb = np.abs(np.asarray(med.Wbase))   # magnitude row (audit only)
            ref = dep208_by_j[j]
            errs, per_seed = [], []
            replay_flags, ref_flags = [], []
            n_bnd = None
            for s_idx, (s, dep_err) in enumerate(
                    zip(seeds, dep_rec["errs"])):
                out = M148.decode("scoped", med, s, return_state=True,
                                  f_max=fmax)
                if not out["ok"]:
                    n_rejections += 1
                    rejection_records.append(
                        {"j": j, "seed": s,
                         "rejection": out["rejection"]})
                    replay_flags.append(False)
                    ref_flags.append(False)
                    continue
                err = float(out["err"])
                assert np.isfinite(err)
                errs.append(err)
                # K1a: bit-exact at the deposit's rounding (exp142's
                # convention), per seed (errs + verified)
                replay_flags.append(
                    round(err, 2) == float(dep_err)
                    and bool(out["verified"])
                    == bool(dep_rec["verified"][s_idx]))
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
                # K1b: exp208's decomposition reproduces bit-exactly
                dec = decompose(V, T, cls, err_exact)
                ref_dec = ref["decompositions"][s_idx]
                ref_flags.append(all(
                    pc["sum_sq"] == rc["sum_sq"]
                    and pc["n_cells"] == rc["n_cells"]
                    for pc, rc in zip(dec["per_class"],
                                      ref_dec["per_class"])))
                # ---- the clause's data: per boundary cell ----------
                idx = np.where(bnd)[0]
                assert len(idx) > 0, f"no boundary cells at j{j}"
                e2 = (V - T) ** 2
                r = e2[idx]
                S = np.array([local_step(T, int(i)) for i in idx])
                Salt = np.array([alt_step(T, int(i)) for i in idx])
                D = smoothing_rows(T, A_dyn, idx)
                Dwalt = smoothing_rows(T, Wb, idx)
                K = np.array([curvature(T, int(i)) for i in idx])
                x = S * D
                # the D_i = 0 disclosure (exp226 verbatim): a
                # legitimate instrument reading — the medium's own
                # coupling need not span i's differing ring neighbors
                # (the lattice is the TARGET's canonical neighborhood,
                # not the medium's). KEPT: x = 0 ranks at the bottom
                # of the pooled correlations; dropping would be tuning.
                n_degenerate_D0 += int(np.sum(x <= 0.0))
                n_zero_curv += int(np.sum(K == 0.0))
                pooled_r.extend(r.tolist())
                pooled_x.extend(x.tolist())
                pooled_k.extend(K.tolist())
                pooled_x_walt.extend((S * Dwalt).tolist())
                pooled_x_salt.extend((Salt * D).tolist())
                ratio = r / x
                per_seed.append({
                    "seed": s, "n_bnd": int(len(idx)),
                    "S_mean_mV": float(S.mean()),
                    "S_median_mV": float(np.median(S)),
                    "D_mean_mV": float(D.mean()),
                    "D_median_mV": float(np.median(D)),
                    "K_mean_mV": float(K.mean()),
                    "K_median_mV": float(np.median(K)),
                    "r_median_mV2": float(np.median(r)),
                    "x_median_mV2": float(np.median(x)),
                    "k_median_mV": float(np.median(K)),
                    "ratio_median": float(np.median(ratio)),
                    "r": r.tolist(), "x": x.tolist(), "k": K.tolist()})
            rec = {"j": j, "gen_seed": gen_seed,
                   "tail": bool(dep_rec["tail"]),
                   "dep199_median_err": dep_rec["median_err"],
                   "errs": errs,
                   "replay_bit_exact":
                       bool(all(replay_flags))
                       and len(replay_flags) == len(seeds),
                   "decomposition_bit_exact":
                       bool(all(ref_flags))
                       and len(ref_flags) == len(seeds),
                   "n_boundary_cells": n_bnd,
                   "per_seed": per_seed}
            insts.append(rec)
            print(f"  [c6 j{j:2d}] med {rec['dep199_median_err']} "
                  f"bnd {n_bnd} "
                  f"replay "
                  f"{'exact' if rec['replay_bit_exact'] else 'DRIFT'} "
                  f"decomp "
                  f"{'exact' if rec['decomposition_bit_exact'] else 'DRIFT'}")

        if smoke:
            restore_floor()
            assert [getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in pin_modules] == floors_pre, \
                "floor restore failed (smoke)"
            r_s = np.asarray(pooled_r, dtype=float)
            k_s = np.asarray(pooled_k, dtype=float)
            x_s = np.asarray(pooled_x, dtype=float)
            print(f"  SMOKE instrument check complete - DISCARDED "
                  f"(smoke rho(r,K) {spearman_ties(r_s, k_s):.4f}, "
                  f"smoke rho(r,X) {spearman_ties(r_s, x_s):.4f})")
            return {"exp": "exp229_curvature_test",
                    "smoke": True,
                    "n_points_smoke": len(pooled_r)}

        if args.job in SHARDS:
            shard = {"exp": "exp229_curvature_test",
                     "shard": args.job, "instances": insts}
            with open(out_path, "w") as fh:
                json.dump(shard, fh, indent=1, default=float)
            print(f"  shard {args.job} deposited {out_path}")
            return shard

        # ---- K1 (the replay) — evaluated exactly once -------------------
        n_replay = sum(int(r["replay_bit_exact"]) for r in insts)
        n_decomp = sum(int(r["decomposition_bit_exact"]) for r in insts)
        n_total = len(insts)
        k1_pass = bool(n_replay == n_total and n_decomp == n_total
                       and n_total == PER_CELL)

        # ---- K2 (the curvature clause) — the branch, evaluated once -----
        r_arr = np.asarray(pooled_r, dtype=float)
        k_arr = np.asarray(pooled_k, dtype=float)
        x_arr = np.asarray(pooled_x, dtype=float)
        n_points = int(len(r_arr))
        assert n_points > 0 and len(k_arr) == n_points \
            and len(x_arr) == n_points
        rho = float(spearman_ties(r_arr, k_arr))
        assert np.isfinite(rho), "non-finite Spearman"
        if rho >= 0.6:
            branch = "CURVATURE-TRACKED"
        elif rho >= 0.3:
            branch = "MIXED"
        else:
            branch = "GENUINE-EXCESS"
        k2_pass = bool(branch in ("CURVATURE-TRACKED", "MIXED",
                                  "GENUINE-EXCESS"))
        k2_pass = bool(k2_pass and n_points == (
            sum(ps["n_bnd"] for r_ in insts for ps in r_["per_seed"]))
            and n_points == n_points_exp226)
        # audit-only alternates (never gated — the branch is named from
        # the pre-named primary instruments only): exp226's two
        # alternate readings, recomputed on the same point set
        rho_w_alt = float(spearman_ties(
            r_arr, np.asarray(pooled_x_walt, dtype=float)))
        rho_s_alt = float(spearman_ties(
            r_arr, np.asarray(pooled_x_salt, dtype=float)))

        # ---- K3 (the joint reading) — evaluated once --------------------
        # the partial correlation of r_i with K_i controlling for
        # S_i * D_i: the standard partial-correlation identity on the
        # Spearman rhos (Kendall's partial-rank form; the ranks come
        # from spearmanr's own tied-average ranking via spearman_ties).
        # The three-way attribution (step, curvature, unexplained) as
        # shares of RANK variance: OLS on the tied average ranks, the
        # step/curvature split taken as the AVERAGE of the two
        # sequential (order-of-entry) decompositions — symmetric, zero
        # knobs, the three shares sum to 1 exactly. No share is
        # clamped (a negative share is a real suppression reading;
        # clamping would be tuning).
        rho_rX = float(spearman_ties(r_arr, x_arr))
        rho_KX = float(spearman_ties(k_arr, x_arr))
        den = float(np.sqrt(max(0.0, 1.0 - rho_rX ** 2)
                            * max(0.0, 1.0 - rho_KX ** 2)))
        partial = float((rho - rho_rX * rho_KX) / den) if den > 0.0 \
            else float("nan")
        Rk = np.asarray(rankdata(r_arr), dtype=float)
        Ck = np.asarray(rankdata(k_arr), dtype=float)
        Xk = np.asarray(rankdata(x_arr), dtype=float)

        def _r2(y: np.ndarray, cols: list) -> float:
            Xd = np.column_stack([np.ones(len(y))] + list(cols))
            beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
            resid = y - Xd @ beta
            sstot = float(((y - y.mean()) ** 2).sum())
            return float(1.0 - float((resid ** 2).sum()) / sstot)

        r2_full = _r2(Rk, [Ck, Xk])
        r2_step = _r2(Rk, [Xk])
        r2_curv = _r2(Rk, [Ck])
        share_step = 0.5 * (r2_step + r2_full - r2_curv)
        share_curv = 0.5 * (r2_curv + r2_full - r2_step)
        share_unexplained = 1.0 - r2_full
        shares_sum = share_step + share_curv + share_unexplained
        shares_ok = bool(abs(shares_sum - 1.0) < 1e-9)
        assert shares_ok, "three-way shares do not sum to 1"
        k3_pass = bool(np.isfinite(partial) and shares_ok
                       and all(np.isfinite(v) for v in
                               (share_step, share_curv,
                                share_unexplained)))
        # audit-only continuity vs exp226's deposit (never gated): the
        # machinery is exp226's verbatim and the decode deterministic,
        # so the recomputed step rho should equal exp226's deposited
        # 0.5449887249912534
        rho_rX_matches_exp226 = bool(rho_rX == rho_rX_exp226)

        # ---- K4 (hygiene) — evaluated once ------------------------------
        all_finite = bool(
            np.all(np.isfinite(r_arr)) and np.all(np.isfinite(k_arr))
            and np.all(np.isfinite(x_arr))
            and all(np.isfinite(e) for r_ in insts for e in r_["errs"]))
        restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        pin_restored = bool(floors_post == floors_pre)
        assert pin_restored, "floor restore failed"
        k4_pass = bool(n_rejections == 0 and all_finite and pin_restored)

        gates = {
            "K1": {"pass": k1_pass, "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_instances": n_total,
                   "disclosure": ("errs + per-seed verified bit-exact vs "
                                  "exp199's deposit at the deposit's 2-dp "
                                  "err rounding (exp142's convention); "
                                  "exp208's per-class sum_sq + n_cells "
                                  "reproduced bit-exactly (float ==, the "
                                  "decode is deterministic) — exp213's "
                                  "B1 verbatim; exp226's anchors, "
                                  "exp226's machinery verbatim")},
            "K2": {"pass": k2_pass, "branch": branch, "rho": rho,
                   "n_points": n_points,
                   "n_degenerate_D0": n_degenerate_D0,
                   "n_zero_curvature": n_zero_curv,
                   "point_set": ("all CANON-BOUNDARY cells of the c6 "
                                 "battery's 25 instances x 3 seeds, "
                                 "exp208's mask verbatim — the SAME "
                                 "10,047 points as exp226's R2"),
                   "point_set_matches_exp226":
                       bool(n_points == n_points_exp226),
                   "thresholds": {"CURVATURE-TRACKED": "rho >= 0.6",
                                  "MIXED": "0.3 <= rho < 0.6",
                                  "GENUINE-EXCESS": "rho < 0.3"},
                   "zero_curvature_disclosure": (
                       "K_i = 0 is a legitimate reading (a locally "
                       "linear plan segment has no curvature); those "
                       "points are KEPT, Spearman's tie handling ranks "
                       "them together — dropping them would be tuning"),
                   "sensitivity_audit_only": {
                       "rho_weight_row_Wbase": rho_w_alt,
                       "rho_step_across_neighbors": rho_s_alt,
                       "note": ("the branch is named from the pre-named "
                                "primary instruments only; exp226's two "
                                "alternate readings recomputed on the "
                                "same point set for audit, never "
                                "gated")}},
            "K3": {"pass": k3_pass,
                   "partial_rho_rK_given_X": partial,
                   "components": {"rho_rK": rho, "rho_rX": rho_rX,
                                  "rho_KX": rho_KX},
                   "r2_rank": {"full": r2_full, "step_only": r2_step,
                               "curvature_only": r2_curv},
                   "three_way_shares_of_rank_variance": {
                       "step": share_step, "curvature": share_curv,
                       "unexplained": share_unexplained},
                   "method_disclosure": (
                       "partial correlation: the standard identity "
                       "(rho_rK - rho_rX*rho_KX) / sqrt((1-rho_rX^2)"
                       "(1-rho_KX^2)) on the Spearman rhos (Kendall's "
                       "partial-rank form); attribution: OLS on the "
                       "tied average ranks, the step/curvature split "
                       "the AVERAGE of the two order-of-entry "
                       "decompositions — symmetric, zero knobs, "
                       "shares sum to 1 exactly, no clamping (a "
                       "negative share is a real suppression "
                       "reading)"),
                   "exp226_continuity_audit_only": {
                       "rho_rX_recomputed": rho_rX,
                       "rho_rX_exp226_deposited": rho_rX_exp226,
                       "bit_equal": rho_rX_matches_exp226,
                       "note": ("exp226's machinery verbatim + "
                                "deterministic decode, so the "
                                "recomputed step rho should equal "
                                "exp226's deposited value; disclosed, "
                                "never gated")}},
            "K4": {"pass": k4_pass, "rejections": n_rejections,
                   "rejection_records": rejection_records,
                   "all_finite": all_finite,
                   "pin": {"floors_pre": floors_pre,
                           "floors_post": floors_post,
                           "restored": pin_restored,
                           "modules": [m.__name__
                                       for m in pin_modules],
                           "disclosure": ("the exp169-import restore "
                                          "(exp226's disclosure): the "
                                          "import of exp169 sets the "
                                          "production -35.0 floor across "
                                          "the pin modules; exp199's "
                                          "_PIN_SAVE snapshots that "
                                          "state, so restore_floor() "
                                          "lands exactly at the pre-run "
                                          "floors (asserted)")}}}
        npass = sum(1 for g in gates.values() if g["pass"])
        verdict = f"{npass}/4 gates (K1 K2 K3 K4) | {branch}"
        print(f"  === {verdict} ===")
        print(f"  rho(r,K) {rho:.4f} over {n_points} boundary points "
              f"({n_zero_curv} K_i=0 kept, {n_degenerate_D0} D_i=0 "
              f"kept) | partial(r,K|X) {partial:.4f} | shares "
              f"step {share_step:.4f} / curvature {share_curv:.4f} / "
              f"unexplained {share_unexplained:.4f} | "
              f"(audit alternates: Wbase-row {rho_w_alt:.4f}, "
              f"across-step {rho_s_alt:.4f})")

        section = {"cell": 6, "n_instances": len(insts),
                   "seeds": list(SEEDS), "n_build": int(N400),
                   "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_boundary_points": n_points,
                   "instances": insts}
        summary = {
            "K_mean_mV_pooled": float(np.mean(k_arr)),
            "K_median_mV_pooled": float(np.median(k_arr)),
            "r_median_mV2_pooled": float(np.median(r_arr)),
            "resid_rms_mV_pooled": float(np.sqrt(np.mean(r_arr))),
            "rho_rK": rho, "rho_rX": rho_rX, "rho_KX": rho_KX,
            "partial_rho_rK_given_X": partial,
            "shares": {"step": share_step, "curvature": share_curv,
                       "unexplained": share_unexplained},
            "note": ("K_i in mV (the plan's second difference), "
                     "r_i in mV^2, X = S_i * D_i in mV^2 — exp226's "
                     "instruments verbatim, the curvature added")}

        deposit = {
            "exp": "exp229_curvature_test",
            "claim": (
                "THE CURVATURE TEST (L202's registered next): exp226's "
                "PARTIAL-TRACKING left a genuine boundary structure — "
                "~150x inside the smoothing bound in magnitude, "
                "tracking the step response only partially (rho "
                "0.545); the identity test: the residual's structure "
                "decomposed against the plan's SECOND difference (the "
                "curvature, not the step) — if the residual tracks the "
                "plan's curvature, the excess is the pattern's own "
                "geometry read through the substrate"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 799a35c, batch 14; gates K1-K4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-K1 (the replay) exp226's anchors reproduce "
                    "(exp199 bit-exact 25/25 + exp208's decomposition "
                    "bit-exact)",
                    "GATE-K2 (the curvature clause) the branch named: "
                    "CURVATURE-TRACKED (rho >= 0.6) / MIXED (0.3 <= "
                    "rho < 0.6) / GENUINE-EXCESS (rho < 0.3) — "
                    "Spearman(r_i, K_i) across the same 10,047 "
                    "canon-boundary points",
                    "GATE-K3 (the joint reading) the partial-"
                    "correlation of r_i with K_i controlling for "
                    "S_i * D_i (exp226's instrument) deposited; the "
                    "three-way attribution (step, curvature, "
                    "unexplained) deposited as shares of rank "
                    "variance",
                    "GATE-K4 (hygiene) zero rejections; all finite; "
                    "the -35.0 pin save/restore asserted (exp199's "
                    "semantics)"],
                "conventions": (
                    "K_i = |T_plan[i-1] - 2*T_plan[i] + T_plan[i+1]| "
                    "on the ring backbone (the plan's second difference "
                    "at cell i; zero is a legitimate reading — kept, "
                    "ties ranked together); r_i = the mV^2 summand of "
                    "exp208's decomposition rows; X = S_i * D_i = "
                    "exp226's smoothing instrument verbatim; the D_i=0 "
                    "points kept (exp226's disclosure); exp226's two "
                    "alternate readings recomputed audit-only, never "
                    "gated; the K3 method (partial-rank identity + the "
                    "symmetric average-of-orderings OLS split on "
                    "ranks, shares sum to 1, no clamping) fixed here, "
                    "zero knobs")},
            "sections": {"c6_tail": section,
                         "curvature_joint_summary": summary},
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
