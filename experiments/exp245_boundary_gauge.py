#!/usr/bin/env python3
"""exp245 — THE BOUNDARY RESIDUAL'S GAUGE-AWARE RE-DECOMPOSITION (the
Section 6 item; exp229's ~70% unexplained boundary structure; ledger
L221).

THE OPEN ITEM: exp226/exp229's three-way rank-variance attribution of
the boundary residual (step 0.241 / curvature 0.058 / unexplained
0.701) left ~70% of the rank variance unexplained. THIS BATCH'S
discovery re-opens the decomposition: exp234 proved the pattern layer
carries an EXACT GAUGE MODE (the uniform offset — zero information,
conserved), and exp239 carried the gauge quotient into the certificate
machinery. The residual r_i (exp208's decomposition-row mV^2 summands)
is an ABSOLUTE-RMS object — it contains the gauge share. The zero-knob
refinement: re-decompose exp226's residual on the GAUGE QUOTIENT and
re-run the three-way attribution (step / curvature / unexplained) on
the gauge-aware residual.

THE INSTRUMENTS (all frozen, verbatim): exp226's machinery (the c6
battery, the replay anchors, the residual rows, the D_i = 0 points
kept), exp226's step instrument S_i, exp229's curvature instrument
K_i; the NEW element is the residual's gauge projection: r_i^gauge =
r_i computed on the gauge-quotiented fields (the (V, theta) fields
projected: x = y - (y.g)g with g the uniform direction — the mV^2
summands recomputed from the projected fields; the summand is
quadratic so the projection's cross-terms are carried exactly, no
approximation). The attribution: the same OLS-on-tied-ranks method
exp229 fixed in its body, re-run on (r_i^gauge, S_i, K_i).

PRE-REGISTERED GATES:

  G1  THE CONTINUITY: exp226's machinery verbatim reproduces exp226's
      deposit bit-exactly (the replay anchors — exp229's K1 class).
  G2  THE GAUGE SHARE: the gauge share of the residual's rank variance
      recorded (the R^2 of the gauge direction alone on the tied
      ranks); the gate is the RECORD (zero-tolerance on silence), the
      pre-named expectation: the share is small (the gauge is uniform,
      the residual is boundary-concentrated — but the absolute-RMS
      summand carries SOME gauge).
  G3  THE RE-ATTRIBUTION: the three-way split on the gauge-aware
      residual (step / curvature / unexplained — shares sum to 1,
      exp229's method); the gate: the split recomputed and deposited;
      the FINDING names whether the unexplained share DROPS (the gauge
      was eating attribution) or STANDS (~70% confirmed gauge-free).
  G4  THE DISCIPLINE: zero rejections, all finite, the -35.0 pin
      save/restore asserted (the exp169-import restore disclosed).

THE BRANCH (pre-named): the unexplained share drops below 0.6 ->
GAUGE-EATS (the 70% was partly the gauge — the boundary frontier's
standing measure UPDATED); the share stands >= 0.65 ->
GAUGE-FREE-70 (the unexplained structure is genuinely not-gauge — the
frontier's hardest core confirmed).

RUN: exp226's battery verbatim + the projected recomputation; serial,
BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp245_boundary_gauge.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only
    # discipline; docstring/imports/constants above byte-unchanged —
    # the gates below are the docstring's, each evaluated exactly
    # once) ==============================================================
    import time

    t0 = time.time()

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
    # lands exactly at the pre-run floors (asserted in G4)
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp199_ro_n400_tail as M199
    from experiments.exp199_ro_n400_tail import (
        DEP160_FLOOR, N400, PER_CELL, SEEDS, pin_floor, restore_floor)

    # ---- G1's reference deposits (exp226's anchors) + exp229's
    #      deposit (the point-set and original-split continuity
    #      audits; read-only, never modified) ---------------------------
    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    DEP208 = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")
    DEP229 = os.path.join(ROOT, "results", "exp229_curvature_test.json")
    for _p in (DEP199, DEP208, DEP229):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    with open(DEP199) as f:
        dep199 = json.load(f)
    with open(DEP208) as f:
        dep208 = json.load(f)
    with open(DEP229) as f:
        dep229 = json.load(f)
    dep_by_cell = {r["j"]: r
                   for r in dep199["cells"]["c6"]["instances"]}
    dep208_by_j = {r["j"]: r
                   for r in dep208["sections"]["c6_tail"]["instances"]}
    n_points_exp229 = int(dep229["gates"]["K2"]["n_points"])
    shares_exp229 = dep229["gates"]["K3"][
        "three_way_shares_of_rank_variance"]

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
    #      response; exp245 adds NO new substrate machinery) --------------
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
    # tuning; exp226's disclosure).
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

    # ---- exp229's curvature instrument VERBATIM (zero knobs) ------------
    # K_i = |T_plan[i-1] - 2*T_plan[i] + T_plan[i+1]| on the ring
    # backbone (the plan's SECOND difference at cell i). Zero is a
    # legitimate reading — a locally linear plan segment has no
    # curvature; such points are KEPT, Spearman's tie handling ranks
    # them together, dropping them would be tuning (exp229's
    # disclosure).
    def curvature(T: np.ndarray, i: int) -> float:
        n = len(T)
        return abs(float(T[(i - 1) % n]) - 2.0 * float(T[i])
                   + float(T[(i + 1) % n]))

    # ---- THE GAUGE PROJECTION (the NEW element; exp234's gauge mode,
    #      exp239's quotient form) ----------------------------------------
    # r_i^gauge = r_i computed on the gauge-quotiented fields:
    # x = y - (y.g)g with g the uniform direction, the mV^2 summands
    # recomputed from the projected field exactly (the summand is
    # quadratic so the projection's cross-terms are carried exactly,
    # no approximation).
    # OPERATIONALIZATION (disclosed, zero knobs): the residual's field
    # is the deviation d = V - T_plan over the WHOLE decoded field —
    # the field exp208's mV^2 summands are built from, i.e. the
    # pattern layer's state as the read delivers it (the frozen
    # machinery's state exposes (V, target); the raw (V,theta) stack's
    # theta channel is not exposed by the decode, and projecting the
    # ABSOLUTE stack would re-center both fields by the plan-level
    # constant (~-37.6 mV on c6), reducing the summands to
    # signed-deviation reads and destroying the residual's own
    # structure). The projection is EXACTLY gauge-invariant: under the
    # substrate's uniform shift (V+c, theta+c) (exp234's zero mode, M
    # @ ones = 0) the deviation's uniform component (y.g) tracks the
    # shift one-for-one, so x is invariant — this IS the residual on
    # the gauge quotient. g = the uniform direction on the field
    # (ones/sqrt(n)); the gauge coordinate (y.g) is the per-
    # instance-seed scalar broadcast to the instance's boundary points
    # (the gauge is global — exp234's own words), and it is G2's
    # gauge-direction instrument. Audit-only alternate: the
    # boundary-restricted gauge scope (the uniform component over the
    # boundary cells only), computed alongside, never gated.
    def gauge_project(d: np.ndarray) -> tuple[np.ndarray, float]:
        n = len(d)
        g = np.ones(n) / np.sqrt(n)
        proj = float(d @ g)                  # the gauge coordinate
        x = d - proj * g                     # x = y - (y.g)g, literally
        return x, proj

    def gauge_project_scope(d: np.ndarray) -> tuple[np.ndarray, float]:
        # audit-only alternate: the uniform direction over the SAME
        # vector (the boundary rows here); scope disclosed, never gated
        n = len(d)
        g = np.ones(n) / np.sqrt(n)
        proj = float(d @ g)
        x = d - proj * g
        return x, proj

    # ---- exp229's OLS-on-tied-ranks R^2 (the attribution method,
    #      verbatim) -------------------------------------------------------
    def _r2(y: np.ndarray, cols: list) -> float:
        Xd = np.column_stack([np.ones(len(y))] + list(cols))
        beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
        resid = y - Xd @ beta
        sstot = float(((y - y.mean()) ** 2).sum())
        return float(1.0 - float((resid ** 2).sum()) / sstot)

    # ---- the battery: c6 (the tail, 25 instances), seeds (1,2,3) --------
    seeds = list(SEEDS)

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
        pooled_x: list = []          # S_i * D_i (exp226's instrument)
        pooled_k: list = []          # K_i (exp229's instrument)
        pooled_rg: list = []         # r_i^gauge (the gauge-aware
        #                            residual — the gated object)
        pooled_g: list = []          # the gauge coordinate (y.g),
        #                            broadcast within the instance-seed
        pooled_rgb: list = []        # r_i^gauge, boundary-restricted
        #                            gauge scope — audit only
        pooled_x_walt: list = []     # S_i * D_i(|Wbase| row) — audit only
        pooled_x_salt: list = []     # S_alt_i * D_i — audit only
        bnd_rms_all: list = []
        n_degenerate_D0 = 0          # D_i = 0 points (x = S*D = 0;
        #                             kept, counted, disclosed — NOT
        #                             dropped: dropping would be
        #                             tuning; exp226's disclosure)
        n_zero_curv = 0              # K_i = 0 points (locally linear
        #                             plan segments; kept, ties ranked
        #                             together; exp229's disclosure)
        for j in range(PER_CELL):
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
                # G1a: bit-exact at the deposit's rounding (exp142's
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
                # G1b: exp208's decomposition reproduces bit-exactly
                dec = decompose(V, T, cls, err_exact)
                ref_dec = ref["decompositions"][s_idx]
                ref_flags.append(all(
                    pc["sum_sq"] == rc["sum_sq"]
                    and pc["n_cells"] == rc["n_cells"]
                    for pc, rc in zip(dec["per_class"],
                                      ref_dec["per_class"])))
                bnd_rms_all.append(
                    [p["rms_contrib_mV"] for p in dec["per_class"]
                     if p["class"] == "CANON-BOUNDARY"][0])
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
                # ---- THE GAUGE PROJECTION (the new element) --------
                # the whole deviation field d = V - T_plan (the
                # residual's field), projected on the uniform
                # direction's orthogonal complement; the mV^2
                # summands recomputed from the projected field
                # EXACTLY (cross-terms carried — the plain square)
                d_perp, gcoord = gauge_project(V - T)
                rg = d_perp[idx] ** 2
                # audit-only alternate: the boundary-restricted scope
                d_bnd = (V - T)[idx]
                rg_bnd, _ = gauge_project_scope(d_bnd)
                rg_bnd = rg_bnd ** 2
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
                pooled_rg.extend(rg.tolist())
                pooled_rgb.extend(rg_bnd.tolist())
                pooled_g.extend([gcoord] * len(idx))
                pooled_x_walt.extend((S * Dwalt).tolist())
                pooled_x_salt.extend((Salt * D).tolist())
                ratio = r / x
                per_seed.append({
                    "seed": s, "n_bnd": int(len(idx)),
                    "gauge_coordinate_mV": gcoord,
                    "S_mean_mV": float(S.mean()),
                    "S_median_mV": float(np.median(S)),
                    "D_mean_mV": float(D.mean()),
                    "D_median_mV": float(np.median(D)),
                    "K_mean_mV": float(K.mean()),
                    "K_median_mV": float(np.median(K)),
                    "r_median_mV2": float(np.median(r)),
                    "rg_median_mV2": float(np.median(rg)),
                    "x_median_mV2": float(np.median(x)),
                    "k_median_mV": float(np.median(K)),
                    "ratio_median": float(np.median(ratio)),
                    "r": r.tolist(), "x": x.tolist(), "k": K.tolist(),
                    "r_gauge": rg.tolist()})
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

        # ---- G1 (the replay) — evaluated exactly once (exp229's K1
        #      class verbatim) --------------------------------------------
        n_replay = sum(int(r["replay_bit_exact"]) for r in insts)
        n_decomp = sum(int(r["decomposition_bit_exact"]) for r in insts)
        n_total = len(insts)
        g1_pass = bool(n_replay == n_total and n_decomp == n_total
                       and n_total == PER_CELL)

        # ---- the pooled point set (exp226/exp229's, asserted) ------------
        r_arr = np.asarray(pooled_r, dtype=float)
        k_arr = np.asarray(pooled_k, dtype=float)
        x_arr = np.asarray(pooled_x, dtype=float)
        rg_arr = np.asarray(pooled_rg, dtype=float)
        g_arr = np.asarray(pooled_g, dtype=float)
        n_points = int(len(r_arr))
        assert n_points > 0 and len(k_arr) == n_points \
            and len(x_arr) == n_points \
            and len(rg_arr) == n_points and len(g_arr) == n_points
        assert n_points == (
            sum(ps["n_bnd"] for r_ in insts for ps in r_["per_seed"]))
        # the machinery is exp226's verbatim and the decode is
        # deterministic, so the point set MUST be exp229's 10,047
        assert n_points == n_points_exp229, \
            f"boundary point set drifted vs exp229's deposit: {n_points}"

        # ---- G2 (the gauge share) — evaluated exactly once ---------------
        # the R^2 of the gauge direction alone on the tied ranks: OLS
        # of rankdata(r_i) on [1, rankdata(gauge coordinate)] —
        # exp229's _r2 form with the gauge direction as the sole
        # regressor. The gate is the RECORD (zero-tolerance on
        # silence); the pre-named expectation is that the share is
        # small (the gauge is uniform, the residual is
        # boundary-concentrated — but the absolute-RMS summand
        # carries SOME gauge).
        Rk_orig = np.asarray(rankdata(r_arr), dtype=float)
        Gk = np.asarray(rankdata(g_arr), dtype=float)
        share_gauge = _r2(Rk_orig, [Gk])
        # the gate is the RECORD: pass = the share recorded and finite
        g2_pass = bool(np.isfinite(share_gauge))
        # audit-only alternates (never gated): the rank correlation
        # and the unranked-regressor R^2
        rho_rG = float(spearman_ties(r_arr, g_arr))
        share_gauge_unranked = _r2(Rk_orig, [g_arr])

        # ---- G3 (the re-attribution) — evaluated exactly once ------------
        # exp229's method verbatim on the gauge-aware residual: the
        # partial correlation + the three-way OLS-on-tied-ranks split
        # (the symmetric average-of-orderings form, shares sum to 1,
        # no clamping), with r_i -> r_i^gauge.
        rho_rK = float(spearman_ties(rg_arr, k_arr))
        rho_rX = float(spearman_ties(rg_arr, x_arr))
        rho_KX = float(spearman_ties(k_arr, x_arr))
        den = float(np.sqrt(max(0.0, 1.0 - rho_rX ** 2)
                            * max(0.0, 1.0 - rho_KX ** 2)))
        partial = float((rho_rK - rho_rX * rho_KX) / den) if den > 0.0 \
            else float("nan")
        Rk = np.asarray(rankdata(rg_arr), dtype=float)
        Ck = np.asarray(rankdata(k_arr), dtype=float)
        Xk = np.asarray(rankdata(x_arr), dtype=float)

        r2_full = _r2(Rk, [Ck, Xk])
        r2_step = _r2(Rk, [Xk])
        r2_curv = _r2(Rk, [Ck])
        share_step = 0.5 * (r2_step + r2_full - r2_curv)
        share_curv = 0.5 * (r2_curv + r2_full - r2_step)
        share_unexplained = 1.0 - r2_full
        shares_sum = share_step + share_curv + share_unexplained
        shares_ok = bool(abs(shares_sum - 1.0) < 1e-9)
        assert shares_ok, "three-way shares do not sum to 1"
        # THE BRANCH (pre-named): the unexplained share drops below
        # 0.6 -> GAUGE-EATS; the share stands >= 0.65 -> GAUGE-FREE-70
        if share_unexplained < 0.6:
            branch = "GAUGE-EATS"
        elif share_unexplained >= 0.65:
            branch = "GAUGE-FREE-70"
        else:
            # the pre-registration named two branches; an
            # in-between landing is deposited honestly, never forced
            branch = "NO-PRE-NAMED-BRANCH"
        g3_pass = bool(np.isfinite(partial) and shares_ok
                       and all(np.isfinite(v) for v in
                               (share_step, share_curv,
                                share_unexplained)))
        delta_unexplained = share_unexplained - float(
            shares_exp229["unexplained"])
        finding = ("DROPS" if share_unexplained
                   < float(shares_exp229["unexplained"])
                   else "STANDS")
        # audit-only continuity vs exp229's deposit (never gated):
        # the SAME method on the ORIGINAL (absolute-RMS) residual must
        # reproduce exp229's deposited shares bit-exactly (the decode
        # is deterministic, the method verbatim)
        Rk0 = Rk_orig
        r2_full_orig = _r2(Rk0, [Ck, Xk])
        r2_step_orig = _r2(Rk0, [Xk])
        r2_curv_orig = _r2(Rk0, [Ck])
        shares_orig = {
            "step": 0.5 * (r2_step_orig + r2_full_orig - r2_curv_orig),
            "curvature": 0.5 * (r2_curv_orig + r2_full_orig
                                - r2_step_orig),
            "unexplained": 1.0 - r2_full_orig}
        orig_bit_equal = bool(
            shares_orig["step"] == float(shares_exp229["step"])
            and shares_orig["curvature"]
            == float(shares_exp229["curvature"])
            and shares_orig["unexplained"]
            == float(shares_exp229["unexplained"]))
        # audit-only alternate: the boundary-restricted gauge scope
        # (the split on the boundary-scope-projected residual), never
        # gated
        rg_b_arr = np.asarray(pooled_rgb, dtype=float)
        Rkb = np.asarray(rankdata(rg_b_arr), dtype=float)
        r2_full_b = _r2(Rkb, [Ck, Xk])
        r2_step_b = _r2(Rkb, [Xk])
        r2_curv_b = _r2(Rkb, [Ck])
        shares_bnd_scope = {
            "step": 0.5 * (r2_step_b + r2_full_b - r2_curv_b),
            "curvature": 0.5 * (r2_curv_b + r2_full_b - r2_step_b),
            "unexplained": 1.0 - r2_full_b}

        # ---- G4 (hygiene) — evaluated once (exp229's K4 verbatim) --------
        all_finite = bool(
            np.all(np.isfinite(r_arr)) and np.all(np.isfinite(k_arr))
            and np.all(np.isfinite(x_arr))
            and np.all(np.isfinite(rg_arr))
            and np.all(np.isfinite(g_arr))
            and all(np.isfinite(e) for r_ in insts for e in r_["errs"]))
        restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        pin_restored = bool(floors_post == floors_pre)
        assert pin_restored, "floor restore failed"
        g4_pass = bool(n_rejections == 0 and all_finite and pin_restored)

        gates = {
            "G1": {"pass": g1_pass, "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_instances": n_total,
                   "disclosure": ("errs + per-seed verified bit-exact vs "
                                  "exp199's deposit at the deposit's 2-dp "
                                  "err rounding (exp142's convention); "
                                  "exp208's per-class sum_sq + n_cells "
                                  "reproduced bit-exactly (float ==, the "
                                  "decode is deterministic) — exp213's "
                                  "B1 verbatim; exp226's anchors, "
                                  "exp226's machinery verbatim "
                                  "(exp229's K1 class)")},
            "G2": {"pass": g2_pass,
                   "gauge_share_of_residual_rank_variance": share_gauge,
                   "response": "the tied ranks of exp226's residual "
                               "r_i = (V - T_plan)^2 at the boundary "
                               "cells (the ABSOLUTE-RMS object)",
                   "regressor": "the tied ranks of the gauge direction's "
                                "reading — the projection scalar (y.g) "
                                "per instance-seed (the field's uniform "
                                "component; broadcast to the instance's "
                                "boundary points, the gauge is global — "
                                "exp234), the sole regressor (the "
                                "exp229 _r2 form + intercept)",
                   "gate_semantics": ("the gate is the RECORD "
                                      "(zero-tolerance on silence): "
                                      "pass = the share recorded and "
                                      "finite"),
                   "pre_named_expectation": (
                       "the share is small (the gauge is uniform, the "
                       "residual is boundary-concentrated — but the "
                       "absolute-RMS summand carries SOME gauge)"),
                   "n_points": n_points,
                   "n_distinct_gauge_values": int(
                       len(np.unique(g_arr))),
                   "gauge_coordinate_range_mV":
                       [float(g_arr.min()), float(g_arr.max())],
                   "audit_only": {
                       "spearman_r_vs_gauge_coordinate": rho_rG,
                       "r2_unranked_regressor": share_gauge_unranked,
                       "note": ("alternates deposited for audit, "
                                "never gated")}},
            "G3": {"pass": g3_pass, "branch": branch, "finding": finding,
                   "unexplained_share": share_unexplained,
                   "delta_unexplained_vs_exp229": delta_unexplained,
                   "three_way_shares_of_rank_variance": {
                       "step": share_step, "curvature": share_curv,
                       "unexplained": share_unexplained},
                   "shares_sum": shares_sum,
                   "r2_rank": {"full": r2_full, "step_only": r2_step,
                               "curvature_only": r2_curv},
                   "components": {"rho_rK": rho_rK, "rho_rX": rho_rX,
                                  "rho_KX": rho_KX},
                   "partial_rho_rK_given_X": partial,
                   "response": "the gauge-aware residual "
                               "r_i^gauge = (V - T_plan - (y.g))^2 at "
                               "the boundary cells (the mV^2 summands "
                               "recomputed from the projected field "
                               "exactly)",
                   "branch_rule": {"GAUGE-EATS": "unexplained < 0.6",
                                   "GAUGE-FREE-70":
                                       "unexplained >= 0.65"},
                   "exp229_deposit_reference": {
                       "step": float(shares_exp229["step"]),
                       "curvature": float(shares_exp229["curvature"]),
                       "unexplained": float(
                           shares_exp229["unexplained"])},
                   "method_disclosure": (
                       "exp229's method verbatim: partial correlation "
                       "(rho_rK - rho_rX*rho_KX) / sqrt((1-rho_rX^2)"
                       "(1-rho_KX^2)) on the Spearman rhos; "
                       "attribution: OLS on the tied average ranks, "
                       "the step/curvature split the AVERAGE of the "
                       "two order-of-entry decompositions — "
                       "symmetric, zero knobs, shares sum to 1 "
                       "exactly, no clamping (a negative share is a "
                       "real suppression reading)"),
                   "exp229_continuity_audit_only": {
                       "split_on_original_residual": shares_orig,
                       "bit_equal_to_exp229_deposit": orig_bit_equal,
                       "note": ("the same method on the ORIGINAL "
                                "absolute-RMS residual; deterministic "
                                "decode + verbatim method, so it must "
                                "equal exp229's deposited split; "
                                "disclosed, never gated")},
                   "gauge_scope_audit_only": {
                       "split_boundary_restricted_scope":
                           shares_bnd_scope,
                       "note": ("the gauge projection with the "
                                "uniform component taken over the "
                                "boundary cells only (the global-field "
                                "scope is the gated reading — the "
                                "gauge is global); deposited for "
                                "audit, never gated")}},
            "G4": {"pass": g4_pass, "rejections": n_rejections,
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
        verdict = f"{npass}/4 gates (G1 G2 G3 G4) | {branch}"
        print(f"  === {verdict} ===")
        print(f"  gauge share {share_gauge:.4f} "
              f"(gauge coordinate range "
              f"[{g_arr.min():+.4f}, {g_arr.max():+.4f}] mV) | "
              f"gauge-aware split over {n_points} points "
              f"({n_degenerate_D0} D_i=0 kept, {n_zero_curv} K_i=0 "
              f"kept): step {share_step:.4f} / curvature "
              f"{share_curv:.4f} / unexplained {share_unexplained:.4f} "
              f"(exp229: {float(shares_exp229['unexplained']):.4f}) | "
              f"the unexplained share {finding}")

        section = {"cell": 6, "n_instances": len(insts),
                   "seeds": list(SEEDS), "n_build": int(N400),
                   "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_boundary_points": n_points,
                   "instances": insts}
        summary = {
            "gauge_coordinate_mean_mV": float(np.mean(g_arr)),
            "gauge_coordinate_std_mV": float(np.std(g_arr)),
            "r_median_mV2_pooled": float(np.median(r_arr)),
            "rg_median_mV2_pooled": float(np.median(rg_arr)),
            "resid_rms_mV_pooled": float(np.sqrt(np.mean(r_arr))),
            "resid_gauge_rms_mV_pooled": float(np.sqrt(np.mean(rg_arr))),
            "gauge_share_of_residual_rank_variance": share_gauge,
            "shares": {"step": share_step, "curvature": share_curv,
                       "unexplained": share_unexplained},
            "note": ("r_i in mV^2, the gauge coordinate in mV (the "
                     "field's uniform component), r_i^gauge the "
                     "projected summands — exp226's instruments "
                     "verbatim, the gauge projection added")}

        deposit = {
            "exp": "exp245_boundary_gauge",
            "claim": (
                "THE BOUNDARY RESIDUAL'S GAUGE-AWARE RE-DECOMPOSITION "
                "(the Section 6 item; exp229's ~70% unexplained "
                "boundary structure; ledger L221): exp226/exp229's "
                "three-way rank-variance attribution of the boundary "
                "residual (step 0.241 / curvature 0.058 / unexplained "
                "0.701) left ~70% unexplained; the residual is an "
                "ABSOLUTE-RMS object so it contains the gauge share — "
                "the zero-knob refinement: re-decompose exp226's "
                "residual on the GAUGE QUOTIENT (exp234's exact gauge "
                "mode, exp239's projector form) and re-run the "
                "three-way attribution on the gauge-aware residual"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 1b98432, batch 17; gates G1-G4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "G1  THE CONTINUITY: exp226's machinery verbatim "
                    "reproduces exp226's deposit bit-exactly (the "
                    "replay anchors — exp229's K1 class).",
                    "G2  THE GAUGE SHARE: the gauge share of the "
                    "residual's rank variance recorded (the R^2 of "
                    "the gauge direction alone on the tied ranks); "
                    "the gate is the RECORD (zero-tolerance on "
                    "silence), the pre-named expectation: the share "
                    "is small (the gauge is uniform, the residual is "
                    "boundary-concentrated — but the absolute-RMS "
                    "summand carries SOME gauge).",
                    "G3  THE RE-ATTRIBUTION: the three-way split on "
                    "the gauge-aware residual (step / curvature / "
                    "unexplained — shares sum to 1, exp229's method); "
                    "the gate: the split recomputed and deposited; "
                    "the FINDING names whether the unexplained share "
                    "DROPS (the gauge was eating attribution) or "
                    "STANDS (~70% confirmed gauge-free).",
                    "G4  THE DISCIPLINE: zero rejections, all finite, "
                    "the -35.0 pin save/restore asserted (the "
                    "exp169-import restore disclosed)."],
                "conventions": (
                    "exp226's machinery verbatim: the c6 battery "
                    "(exp199's rebuilt battery, 25 instances x 3 "
                    "seeds, the production scoped read), the replay "
                    "anchors, exp208's classification + decomposition "
                    "rows, the D_i = 0 points kept, the step "
                    "instrument S_i; exp229's curvature instrument "
                    "K_i verbatim (K_i = 0 kept, ties ranked "
                    "together); X = S_i * D_i. THE GAUGE PROJECTION "
                    "(the new element, operationalized in the body): "
                    "the residual's field is the deviation d = V - "
                    "T_plan over the WHOLE decoded field (the field "
                    "the mV^2 summands are built from; the frozen "
                    "machinery's state exposes (V, target) — the raw "
                    "(V,theta) stack's theta channel is not exposed "
                    "by the decode, and projecting the ABSOLUTE "
                    "stack would re-center both fields by the "
                    "plan-level constant (~-37.6 mV on c6), reducing "
                    "the summands to signed-deviation reads and "
                    "destroying the residual's structure); the "
                    "projection g = the uniform direction "
                    "(ones/sqrt(n)), x = y - (y.g)g computed "
                    "literally, the mV^2 summands recomputed from "
                    "the projected field exactly (the square's "
                    "cross-terms carried, no approximation); the "
                    "projection is EXACTLY gauge-invariant (under "
                    "the substrate's uniform shift (V+c, theta+c) — "
                    "exp234's zero mode, M @ ones(2n) = 0 — the "
                    "deviation's uniform component tracks the shift "
                    "one-for-one, so x is invariant): this IS the "
                    "residual on the gauge quotient; the gauge "
                    "coordinate (y.g) is the per-instance-seed "
                    "scalar broadcast to the instance's boundary "
                    "points (the gauge is global — exp234's own "
                    "words) and is G2's gauge-direction instrument; "
                    "audit-only alternates (the boundary-restricted "
                    "gauge scope; the unranked-regressor R^2; the "
                    "original-residual split) deposited, never "
                    "gated")},
            "sections": {"c6_tail": section,
                         "gauge_redecomposition_summary": summary},
            "gates": gates,
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(OUT, "w") as fh:
            json.dump(deposit, fh, indent=1, default=float)
        print(f"  deposited {OUT} | wall {deposit['wall_s']} s")
        return deposit
    finally:
        restore_floor()


if __name__ == "__main__":
    main()
