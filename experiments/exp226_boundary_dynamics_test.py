#!/usr/bin/env python3
"""exp226 — THE BOUNDARY RESIDUAL'S DYNAMICS TEST (L198's registered
next).

The boundary excess (+0.574 mV at the canon-boundary cells, exp208)
survived every machinery suspect: the read face (three refutations,
L192/L194) and the canon-fallback (zero firings, zero value-changing
when forced, L198). The remaining hypothesis: the residual is the
SUBSTRATE'S OWN smoothing response to the plan's discontinuity — the
dynamics necessarily rounding a step the plan draws. The test: per
boundary cell, the plan's step magnitude vs the residual's magnitude,
against the substrate's local smoothing response priced on the same
battery.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt battery
verbatim (the c6 cell's 25 instances, seeds (1,2,3), the production
scoped read); exp208's classification + decomposition verbatim (the
CANON-BOUNDARY mask, the mV^2 accounting); the SMOOTHING RESPONSE
(pre-named, zero knobs): per boundary cell i, the local step S_i =
max |T_plan difference across i's lattice neighbors| and the
substrate's one-step diffusion response D_i = the ring-averaged
|W[i,.]|-weighted neighbor value spread (the first-order smoothing
kernel exp137's dynamics implements — no new machinery, the medium's
own weights); the clause: the per-cell residual r_i (the armed-vs-plan
deviation from exp208's decomposition rows) vs D_i scaled by S_i.

GATES (each evaluated exactly once):
  GATE-R1 (the replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 x 3) and exp208's decomposition reproduces
           bit-exactly at the reference (exp213's B1 verbatim).
  GATE-R2 (the correlation) Spearman(residual_i, S_i * D_i) across
           all boundary cells of the 25 instances x 3 seeds; the
           branch named: SMOOTHING-BOUND (rho >= 0.6) /
           PARTIAL-TRACKING (0.3 <= rho < 0.6) / EXCESS-NAMED
           (rho < 0.3 — a genuine boundary mechanism left).
  GATE-R3 (the magnitude clause) the residual's magnitude ratio:
           median(r_i / (S_i * D_i)) deposited; the clause holds iff
           the median <= 1.0 (the residual within the smoothing
           bound) — deposited alongside R2, disclosed as a reading
           aid.
  GATE-R4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp226_boundary_dynamics_test.json
RUN: python3 -m experiments.exp226_boundary_dynamics_test [--smoke] [--job ...] [--out ...]
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
                   "exp226_boundary_dynamics_test.json")


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

    import experiments.exp148_temporal_read as M148
    from cultivation.validation.stats import spearman_ties
    from experiments.exp145_phase_read import project_phase_native
    from experiments.exp160_any_medium import config_fingerprint
    from experiments.exp166_leading_edge import CornerMedium, cell_dims
    # exp169's import BEFORE exp199's (exp213's import order): the
    # exp169-import sets the production -35.0 floor across the pin
    # modules (the corpus's disclosed "exp169-import restore"), and
    # exp199's _PIN_SAVE must snapshot THAT state so restore_floor()
    # lands exactly at the pre-run floors (asserted in R4)
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp199_ro_n400_tail as M199
    from experiments.exp199_ro_n400_tail import (
        DEP160_FLOOR, N400, PER_CELL, SEEDS, pin_floor, restore_floor)

    # ---- R1's reference deposits ----------------------------------------
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

    # ---- the read stack, asserted before any decode (exp208 verbatim) ---
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

    # ---- THE SMOOTHING RESPONSE (pre-named, zero knobs) -----------------
    # S_i: the plan's local step at boundary cell i — the max absolute
    # T_plan difference from i to its lattice (ring-backbone i +/- 1)
    # neighbors (exp208's boundary lattice). DISCLOSED reading of
    # "max |T_plan difference across i's lattice neighbors|": the max
    # over the two lattice neighbors of |T[j] - T[i]| — the step the
    # plan draws AT i; never 0 on a CANON-BOUNDARY cell by
    # construction. The across-the-two-neighbors reading is computed
    # alongside and deposited as an audit-only alternate.
    # D_i: the substrate's one-step diffusion response — the
    # ring-averaged |W[i,.]|-weighted neighbor value spread: the
    # coupling row's weighted mean |T_j - T_i| over the support
    # neighbors (averaged over the neighbor ring). W = the projected
    # kernel the scoped read's dynamics implements (exp145's
    # project_phase_native front-end — the EXACT matrix exp142's
    # executor hands GraphCollective as G = A * g_gap): exp137's
    # first-order smoothing kernel, the medium's own weights, no new
    # machinery. On c6 (real, non-negative, T_eff = 1) the projected
    # row IS the symmetrized snapshot-magnitude row (asserted >= 0).
    # r_i: the per-cell residual — the mV^2 summand of exp208's
    # decomposition rows, (V - T)^2 at the cell (V = the armed
    # production scoped read's emission, T = the plan). Spearman on
    # r_i is rank-identical to Spearman on |V - T| (monotone).
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
        pooled_x: list = []          # S_i * D_i (the primary instruments)
        pooled_x_walt: list = []     # S_i * D_i(|Wbase| row) — audit only
        pooled_x_salt: list = []     # S_alt_i * D_i — audit only
        bnd_rms_all: list = []
        n_degenerate_D0 = 0          # D_i = 0 points (ratio -> inf,
        #                             beyond the bound by construction;
        #                             counted, kept, disclosed — NOT
        #                             dropped: dropping would be tuning)
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
                # R1a: bit-exact at the deposit's rounding (exp142's
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
                # R1b: exp208's decomposition reproduces bit-exactly
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
                x = S * D
                # D_i = 0 is a legitimate instrument reading: the
                # medium's own coupling need not span i's differing
                # ring neighbors (the lattice is the TARGET's canonical
                # neighborhood, not the medium's), so the plan's step
                # can be invisible to i's local smoothing. Such points
                # are KEPT (x = 0 ranks at the bottom of the pooled
                # correlation; r/x -> inf is beyond the smoothing
                # bound by construction) and counted for disclosure.
                n_degenerate_D0 += int(np.sum(x <= 0.0))
                pooled_r.extend(r.tolist())
                pooled_x.extend(x.tolist())
                pooled_x_walt.extend((S * Dwalt).tolist())
                pooled_x_salt.extend((Salt * D).tolist())
                ratio = r / x
                per_seed.append({
                    "seed": s, "n_bnd": int(len(idx)),
                    "S_mean_mV": float(S.mean()),
                    "S_median_mV": float(np.median(S)),
                    "D_mean_mV": float(D.mean()),
                    "D_median_mV": float(np.median(D)),
                    "r_median_mV2": float(np.median(r)),
                    "x_median_mV2": float(np.median(x)),
                    "ratio_median": float(np.median(ratio)),
                    "r": r.tolist(), "x": x.tolist()})
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
            print("  SMOKE instrument check complete - DISCARDED")
            return {"exp": "exp226_boundary_dynamics_test",
                    "smoke": True,
                    "n_points_smoke": len(pooled_r)}

        if args.job in SHARDS:
            shard = {"exp": "exp226_boundary_dynamics_test",
                     "shard": args.job, "instances": insts}
            with open(out_path, "w") as fh:
                json.dump(shard, fh, indent=1, default=float)
            print(f"  shard {args.job} deposited {out_path}")
            return shard

        # ---- R1 (the replay) — evaluated exactly once -------------------
        n_replay = sum(int(r["replay_bit_exact"]) for r in insts)
        n_decomp = sum(int(r["decomposition_bit_exact"]) for r in insts)
        n_total = len(insts)
        r1_pass = bool(n_replay == n_total and n_decomp == n_total)

        # ---- R2 (the correlation) — the branch, evaluated once ----------
        r_arr = np.asarray(pooled_r, dtype=float)
        x_arr = np.asarray(pooled_x, dtype=float)
        n_points = int(len(r_arr))
        assert n_points > 0 and len(x_arr) == n_points
        rho = float(spearman_ties(r_arr, x_arr))
        assert np.isfinite(rho), "non-finite Spearman"
        if rho >= 0.6:
            branch = "SMOOTHING-BOUND"
        elif rho >= 0.3:
            branch = "PARTIAL-TRACKING"
        else:
            branch = "EXCESS-NAMED"
        r2_pass = bool(branch in ("SMOOTHING-BOUND", "PARTIAL-TRACKING",
                                  "EXCESS-NAMED"))
        r2_pass = bool(r2_pass and n_points == (
            sum(ps["n_bnd"] for r_ in insts for ps in r_["per_seed"])))
        # audit-only alternates (never gated — the branch is named from
        # the pre-named primary instruments only)
        rho_w_alt = float(spearman_ties(
            r_arr, np.asarray(pooled_x_walt, dtype=float)))
        rho_s_alt = float(spearman_ties(
            r_arr, np.asarray(pooled_x_salt, dtype=float)))

        # ---- R3 (the magnitude clause) — evaluated once -----------------
        ratio_arr = r_arr / x_arr
        ratio_median = float(np.median(ratio_arr))
        r3_pass = bool(ratio_median <= 1.0)
        ratio_q = {f"q{q}": float(np.percentile(ratio_arr, q))
                   for q in (10, 25, 50, 75, 90)}

        # ---- R4 (hygiene) — evaluated once ------------------------------
        all_finite = bool(
            np.all(np.isfinite(r_arr)) and np.all(np.isfinite(x_arr))
            and all(np.isfinite(e) for r_ in insts for e in r_["errs"]))
        restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        pin_restored = bool(floors_post == floors_pre)
        assert pin_restored, "floor restore failed"
        r4_pass = bool(n_rejections == 0 and all_finite and pin_restored)

        gates = {
            "R1": {"pass": r1_pass, "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_instances": n_total,
                   "disclosure": ("errs + per-seed verified bit-exact vs "
                                  "exp199's deposit at the deposit's 2-dp "
                                  "err rounding (exp142's convention); "
                                  "exp208's per-class sum_sq + n_cells "
                                  "reproduced bit-exactly (float ==, the "
                                  "decode is deterministic) — exp213's "
                                  "B1 verbatim")},
            "R2": {"pass": r2_pass, "branch": branch, "rho": rho,
                   "n_points": n_points,
                   "n_degenerate_D0": n_degenerate_D0,
                   "point_set": ("all CANON-BOUNDARY cells of the c6 "
                                 "battery's 25 instances x 3 seeds, "
                                 "exp208's mask verbatim"),
                   "thresholds": {"SMOOTHING-BOUND": "rho >= 0.6",
                                  "PARTIAL-TRACKING": "0.3 <= rho < 0.6",
                                  "EXCESS-NAMED": "rho < 0.3"},
                   "sensitivity_audit_only": {
                       "rho_weight_row_Wbase": rho_w_alt,
                       "rho_step_across_neighbors": rho_s_alt,
                       "note": ("the branch is named from the pre-named "
                                "primary instruments only; the two "
                                "alternate readings are deposited for "
                                "audit, never gated")}},
            "R3": {"pass": r3_pass, "ratio_median": ratio_median,
                   "ratio_quantiles": ratio_q,
                   "n_degenerate_D0": n_degenerate_D0,
                   "degenerate_disclosure": (
                       "points with D_i = 0 (the medium's own coupling "
                       "does not span the cell's differing ring "
                       "neighbors) are KEPT, not dropped: their ratio "
                       "r_i / (S_i * D_i) is inf — beyond the "
                       "smoothing bound by construction — and they "
                       "rank at the bottom of R2's pooled "
                       "correlation; dropping them would be tuning"),
                   "clause": "median(r_i / (S_i * D_i)) <= 1.0",
                   "reading": ("r_i = the mV^2 summand of exp208's "
                               "decomposition rows; the residual within "
                               "the smoothing bound iff the median <= "
                               "1.0 — deposited alongside R2, a reading "
                               "aid")},
            "R4": {"pass": r4_pass, "rejections": n_rejections,
                   "rejection_records": rejection_records,
                   "all_finite": all_finite,
                   "pin": {"floors_pre": floors_pre,
                           "floors_post": floors_post,
                           "restored": pin_restored,
                           "modules": [m.__name__
                                       for m in pin_modules],
                           "disclosure": ("the exp169-import restore "
                                          "(exp225's disclosure): the "
                                          "import of exp169 sets the "
                                          "production -35.0 floor across "
                                          "the pin modules; exp199's "
                                          "_PIN_SAVE snapshots that "
                                          "state, so restore_floor() "
                                          "lands exactly at the pre-run "
                                          "floors (asserted)")}}}
        npass = sum(1 for g in gates.values() if g["pass"])
        verdict = f"{npass}/4 gates (R1 R2 R3 R4) | {branch}"
        print(f"  === {verdict} ===")
        print(f"  rho {rho:.4f} over {n_points} boundary points "
              f"({n_degenerate_D0} D_i=0 kept) | "
              f"ratio median {ratio_median:.4f} "
              f"(audit alternates: Wbase-row {rho_w_alt:.4f}, "
              f"across-step {rho_s_alt:.4f})")

        section = {"cell": 6, "n_instances": len(insts),
                   "seeds": list(SEEDS), "n_build": int(N400),
                   "n_replay_exact": n_replay,
                   "n_decomposition_exact": n_decomp,
                   "n_boundary_points": n_points,
                   "instances": insts}
        summary = {
            "S_mean_mV_pooled": float(np.mean(
                [ps["S_mean_mV"] for r_ in insts
                 for ps in r_["per_seed"]])),
            "D_mean_mV_pooled": float(np.mean(
                [ps["D_mean_mV"] for r_ in insts
                 for ps in r_["per_seed"]])),
            "r_median_mV2_pooled": float(np.median(r_arr)),
            "resid_rms_mV_pooled": float(np.sqrt(np.mean(r_arr))),
            "boundary_class_rms_contrib_mV_mean": float(
                np.mean(bnd_rms_all)),
            "note": ("the boundary class's rms contribution level, for "
                     "continuity with exp208's +0.574 mV excess (an "
                     "excess vs exp198's c3 baseline, not a level)")}

        deposit = {
            "exp": "exp226_boundary_dynamics_test",
            "claim": (
                "THE BOUNDARY RESIDUAL'S DYNAMICS TEST (L198's "
                "registered next): the boundary excess (+0.574 mV at "
                "the canon-boundary cells, exp208) survived every "
                "machinery suspect — the remaining hypothesis: the "
                "residual is the SUBSTRATE'S OWN smoothing response to "
                "the plan's discontinuity; per boundary cell, the "
                "plan's step magnitude vs the residual's magnitude, "
                "against the substrate's local smoothing response "
                "priced on the same battery"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 711bba0, batch 13; gates R1-R4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-R1 (the replay) the c6 battery replays "
                    "bit-exactly vs exp199's deposit (25 x 3) and "
                    "exp208's decomposition reproduces bit-exactly at "
                    "the reference (exp213's B1 verbatim)",
                    "GATE-R2 (the correlation) Spearman(residual_i, "
                    "S_i * D_i) across all boundary cells of the 25 "
                    "instances x 3 seeds; the branch named: "
                    "SMOOTHING-BOUND (rho >= 0.6) / PARTIAL-TRACKING "
                    "(0.3 <= rho < 0.6) / EXCESS-NAMED (rho < 0.3 — a "
                    "genuine boundary mechanism left)",
                    "GATE-R3 (the magnitude clause) the residual's "
                    "magnitude ratio: median(r_i / (S_i * D_i)) "
                    "deposited; the clause holds iff the median <= 1.0 "
                    "(the residual within the smoothing bound) — "
                    "deposited alongside R2, disclosed as a reading "
                    "aid",
                    "GATE-R4 (hygiene) zero rejections; all finite; "
                    "the -35.0 pin save/restore asserted (exp199's "
                    "semantics)"],
                "conventions": (
                    "S_i = max over i's lattice (ring-backbone i +/- 1, "
                    "exp208's boundary lattice) neighbors of "
                    "|T_plan[j] - T_plan[i]| (the step the plan draws "
                    "AT i; never 0 on a boundary cell); D_i = the "
                    "ring-averaged |W[i,.]|-weighted neighbor value "
                    "spread = the coupling row's weighted mean "
                    "|T_j - T_i| over the support neighbors, W = the "
                    "projected kernel the scoped read's dynamics "
                    "implements (exp145's project_phase_native — the "
                    "exact matrix exp142's executor hands "
                    "GraphCollective as G = A * g_gap; exp137's "
                    "first-order smoothing kernel, the medium's own "
                    "weights; asserted real non-negative on c6); "
                    "r_i = the mV^2 summand of exp208's decomposition "
                    "rows, (V_armed - T_plan)^2 at the cell (Spearman "
                    "on r_i is rank-identical to Spearman on |V - T|); "
                    "two alternate readings (the |Wbase| kernel row; "
                    "the across-neighbors step) computed and deposited "
                    "as audit-only sensitivities, never gated")},
            "sections": {"c6_tail": section,
                         "smoothing_response_summary": summary},
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
