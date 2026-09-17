#!/usr/bin/env python3
"""exp185 — THE N-SCALING LADDER (the read's size law).

exp180's registered next (L159): the grid residual above N3's 0.60
bar is a GENERIC size effect at the deposited census — the read's
n-scaling is its own instrument question. THIS EXPERIMENT runs the
ladder: n = 100 / 200 / 300 / 400 / 500, 10 fresh instances per rung
(5 per schedule class), the scoped production arm, the residual-vs-n
curve and the coverage features per rung.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Ladder, curves, and gates are fixed now.

THE LADDER: FlipGridMedium(n, seed = GRID_BASE_SEED + 5000 + 100*rung_idx
+ i) for rung_idx 0..4 (n = 100/200/300/400/500), i = 0..9, classes
alternating by i parity (GRID_CLASSES order flip_per/flip_aper);
decode via exp178's scoped arm under the -35.0 pin, seeds (1, 2, 3),
per-instance median err; features: support coverage, density, BFS
reach (exp180's computable set), f_max.

GATES (each evaluated exactly once):
  GATE-Y1 (ladder integrity) 50 instances built and decoded, zero
           rejections, all errs finite; the n=100 rung's median
           within [0.55, 0.80] (the deposited n=100 scale).
  GATE-Y2 (the curve) the residual-vs-n curve (per-rung pooled
           medians) deposited with per-rung dispersions; the curve
           shape NAMED by pre-named branches: (i) MONOTONE rising
           (each rung's median > the previous, n=500 > n=100) — a
           scaling law to name; (ii) SATURATING (n >= 300 rungs'
           medians within 0.05 of each other) — a finite-size
           plateau; (iii) NON-MONOTONE otherwise — deposited as-is.
           All three branches complete the gate.
  GATE-Y3 (the features track) per-feature Spearman vs residual on
           the pooled 50, deposited; the n=100-vs-n=500 feature
           shift table (the mechanism side-data).
  GATE-Y4 (hygiene) pin save/restore asserted; zero cross-rung
           anomalies; the n=100 rung replays exp169's S4 scale
           (pooled median within the deposited grid band).

NO post-hoc tuning. --smoke (1 instance at n=100 and n=500)
permitted, discarded. Deposit: results/exp185_n_scaling.json
Jobs: rung0..rung4
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from experiments.exp148_temporal_read import (  # noqa: E402
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N3_BAR,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
)

import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP169_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}

LADDER_N = [100, 200, 300, 400, 500]
PER_RUNG = 10
SEEDS = (1, 2, 3)
SATURATION_TOL = 0.05

OUT = os.path.join(ROOT, "results", "exp185_n_scaling.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP169_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


def main() -> dict:
    a = globals().get("args")
    smoke = bool(getattr(a, "smoke", False))
    job = getattr(a, "job", "all") or "all"
    out_path = getattr(a, "out", None) or OUT
    import time
    t0 = time.time()
    jobs = [f"rung{r}" for r in range(len(LADDER_N))] \
        if job == "all" else [job]
    mode = ("SMOKE instrument check (1 instance at n=100 and n=500) "
            "- discarded" if smoke else
            "FULL jobs=" + ",".join(jobs))
    print(f"=== exp185: THE N-SCALING LADDER ({mode}) ===\n")

    # ---- exp180's build/decode/feature patterns (local copies) ---------
    def _bfs_order(A: np.ndarray, start: int = 0) -> list[int]:
        """exp73's bfs_order, exp180's local verbatim copy."""
        n_ = A.shape[0]
        seen = np.zeros(n_, dtype=bool)
        seen[start] = True
        order = [start]
        queue = [start]
        while queue:
            i = queue.pop(0)
            for j in np.nonzero(A[i])[0]:
                j = int(j)
                if not seen[j]:
                    seen[j] = True
                    order.append(j)
                    queue.append(j)
        return order

    def _scoped_errs(med, fmax: float, seeds=SEEDS):
        """Scoped-arm decode errs (exp178's production dispatch via
        exp169's scoped_read) under the active instrument pin; the
        instance's f_max is passed in (identical to exp180's
        recompute-per-seed value: the construction is deterministic);
        returns (errs, rejections, V_last)."""
        errs, rej, V = [], 0, None
        for s in seeds:
            out = scoped_read(med, s, fmax, return_state=True)
            if out.get("ok"):
                errs.append(float(out["err"]))
                V = np.asarray(out["state"]["V"])
            else:
                rej += 1
        return errs, rej, V

    def _features(med) -> dict:
        """exp180's computable feature set, verbatim (n derived from
        M's shape — FlipGridMedium carries .M and .T, NOT .n)."""
        frames = list(med.snapshots())
        n_ = int(np.asarray(med.M).shape[0])
        sup = [(np.abs(Wt) > 0) for Wt in frames]
        sup_any = sup[0]
        for s2 in sup[1:]:
            sup_any = sup_any | s2
        A_sup = sup_any.astype(float)
        order = _bfs_order(A_sup)
        reach = len(order) / float(n_)
        q1_depth = (order[n_ // 4] / float(n_)
                    if len(order) > n_ // 4 else 1.0)
        cov = float(np.mean([s2.sum() / float(n_) for s2 in sup]))
        a = np.abs(A_sup)
        asym = (float(np.abs(A_sup - A_sup.T).sum()) / max(a.sum(), 1.0))
        dens = float(a.sum() / float(n_ * n_))
        return {"a1_bfs_reach": reach, "a1b_bfs_q1_depth": q1_depth,
                "a2_support_coverage": cov, "a4_support_density": dens,
                "a4b_support_asymmetry": asym}

    def _spearman(xs, ys) -> float:
        xs = np.asarray(xs, dtype=float)
        ys = np.asarray(ys, dtype=float)
        if len(xs) < 3 or np.std(xs) == 0 or np.std(ys) == 0:
            return float("nan")
        rx = np.argsort(np.argsort(xs)).astype(float)
        ry = np.argsort(np.argsort(ys)).astype(float)
        rx = (rx - rx.mean()) / (rx.std() or 1.0)
        ry = (ry - ry.mean()) / (ry.std() or 1.0)
        return float((rx * ry).mean())

    FEATURE_KEYS = ["a1_bfs_reach", "a1b_bfs_q1_depth",
                    "a2_support_coverage", "a4_support_density",
                    "a4b_support_asymmetry", "f_max"]

    def _build(rung_idx: int, i: int) -> dict:
        """The pre-registered ladder member: FlipGridMedium(n, seed =
        GRID_BASE_SEED + 5000 + 100*rung_idx + i), classes alternating
        by i parity in GRID_CLASSES order (flip_per/flip_aper); n is
        derived from M's shape (the medium carries no .n)."""
        n_reg = LADDER_N[rung_idx]
        cls = "flip_per" if (i % 2 == 0) else "flip_aper"
        seed = GRID_BASE_SEED + 5000 + 100 * rung_idx + i
        med = FlipGridMedium(n_reg, seed=seed, sched=GRID_CLASSES[cls])
        return {"rung_idx": rung_idx, "n_registered": n_reg,
                "n": int(np.asarray(med.M).shape[0]), "cls": cls,
                "i": i, "gen_seed": seed, "med": med}

    def _run_rung(rung_idx: int) -> dict:
        ts = time.time()
        n_reg = LADDER_N[rung_idx]
        recs = []
        for i in range(PER_RUNG):
            b = _build(rung_idx, i)
            med = b["med"]
            fm = f_max_frames(list(med.snapshots()))
            pin_floor()
            errs, rej, _V = _scoped_errs(med, fm)
            restore_floor()
            rec = {"rung_idx": rung_idx, "n": b["n"],
                   "n_registered": b["n_registered"], "cls": b["cls"],
                   "i": i, "gen_seed": b["gen_seed"], "f_max": fm,
                   "errs_scoped": errs, "rejections": rej,
                   "err_scoped_median": (float(np.median(errs))
                                         if errs else None)}
            rec.update(_features(med))
            if rec["err_scoped_median"] is not None:
                rec["residual"] = round(
                    rec["err_scoped_median"] - N3_BAR, 4)
            recs.append(rec)
            print(f"  [rung{rung_idx}] n={b['n']} {b['cls']} i={i} "
                  f"seed={b['gen_seed']} err={rec['err_scoped_median']} "
                  f"residual={rec.get('residual')} f_max={fm}")
        m_errs = [r["err_scoped_median"] for r in recs
                  if r["err_scoped_median"] is not None]
        pooled_err = float(np.median(m_errs)) if m_errs else None
        pooled_res = (pooled_err - N3_BAR) if pooled_err is not None \
            else None
        res_list = [r["residual"] for r in recs
                    if r.get("residual") is not None]
        section = {"n": n_reg, "rung_idx": rung_idx, "instances": recs,
                   "n_instances": len(recs),
                   "rejections": sum(int(r["rejections"]) for r in recs),
                   "pooled_median_err": pooled_err,
                   "pooled_median_residual": pooled_res,
                   "dispersion": ({
                       "q25": round(float(np.percentile(res_list, 25)), 4),
                       "q75": round(float(np.percentile(res_list, 75)), 4),
                       "iqr": round(float(np.percentile(res_list, 75)
                                          - np.percentile(res_list, 25)),
                                    4),
                       "std": round(float(np.std(res_list)), 4)}
                       if res_list else None),
                   "runtime_s": round(time.time() - ts, 1)}
        return section

    _saved = dict(_PIN_SAVE)
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP169_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP169_FLOOR}\n")

    if smoke:
        for ri in (0, len(LADDER_N) - 1):
            b = _build(ri, 0)
            med = b["med"]
            f = _features(med)
            f["f_max"] = f_max_frames(list(med.snapshots()))
            assert all(np.isfinite(v) for v in f.values()), \
                f"non-finite feature in smoke: {f}"
            pin_floor()
            errs, rej, _ = _scoped_errs(med, f["f_max"], seeds=(1,))
            restore_floor()
            print(f"  [smoke] n={b['n']} {b['cls']} seed={b['gen_seed']} "
                  + " ".join(f"{k}={v:.4g}" for k, v in f.items())
                  + f" | decode seed1 err={errs} rej={rej}")
        restore_floor()
        assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                   == _saved[m.__name__] for m in PIN_MODULES), \
            "smoke pin restore failed"
        print("\n  SMOKE check OK - discarded.")
        return {"smoke": True, "discarded": True}

    result: dict = {}
    if job != "all" and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
        assert result.get("exp") == "exp185", "deposit file mismatch"
    result.setdefault("exp", "exp185")
    result.setdefault("sections", {}).setdefault("rungs", {})
    result.setdefault("gates", {})

    for rj in jobs:
        ri = int(rj[len("rung"):])
        sec = _run_rung(ri)
        result["sections"]["rungs"][str(LADDER_N[ri])] = sec
        print(f"  [rung{ri}] n={sec['n']} pooled median err "
              f"{sec['pooled_median_err']} residual "
              f"{sec['pooled_median_residual']} "
              f"({sec['runtime_s']} s)")

    rungs = result["sections"]["rungs"]
    rejections = sum(int(sec.get("rejections", 0))
                     for sec in rungs.values())
    complete = all(str(n) in rungs for n in LADDER_N)

    if complete:
        all_inst = [rec for n in LADDER_N
                    for rec in rungs[str(n)]["instances"]]

        # ---------------- GATE-Y1 (ladder integrity) --------------------
        decoded = [r for r in all_inst
                   if r.get("err_scoped_median") is not None]
        finite = (len(decoded) == len(all_inst)
                  and all(np.isfinite(e) for r in all_inst
                          for e in r["errs_scoped"]))
        med100_err = rungs["100"]["pooled_median_err"]
        y1_band = med100_err is not None and 0.55 <= med100_err <= 0.80
        result["gates"]["Y1_ladder_integrity"] = {
            "pass": bool(len(all_inst) == 50 and len(decoded) == 50
                         and rejections == 0 and finite and y1_band),
            "instances_built": len(all_inst),
            "instances_decoded": len(decoded),
            "rejections": rejections,
            "all_errs_finite": bool(finite),
            "rung_n100_pooled_median_err": med100_err,
            "n100_band_registered": [0.55, 0.80],
            "n100_median_in_band": bool(y1_band)}
        print(f"  [Y1] built {len(all_inst)} decoded {len(decoded)} "
              f"rej {rejections} n100 median err {med100_err} "
              f"in [0.55, 0.80]: {bool(y1_band)}")

        # ---------------- GATE-Y2 (the curve) ---------------------------
        curve = [{"n": n,
                  "pooled_median_residual":
                      rungs[str(n)]["pooled_median_residual"],
                  "pooled_median_err": rungs[str(n)]["pooled_median_err"],
                  "dispersion": rungs[str(n)]["dispersion"]}
                 for n in LADDER_N]
        meds = [c["pooled_median_residual"] for c in curve]
        curve_ok = all(m is not None and np.isfinite(m) for m in meds)
        monotone = bool(curve_ok
                        and all(meds[j] > meds[j - 1]
                                for j in range(1, len(meds))))
        tail = meds[2:]  # the n >= 300 rungs (300/400/500)
        saturating = bool(curve_ok and not monotone and tail
                          and (max(tail) - min(tail)) <= SATURATION_TOL)
        branch = ("MONOTONE" if monotone else
                  "SATURATING" if saturating else "NON-MONOTONE")
        result["gates"]["Y2_curve_branch"] = {
            "pass": bool(curve_ok), "branch": branch, "curve": curve,
            "monotone_clause": monotone,
            "saturating_clause": saturating,
            "saturation_tol": SATURATION_TOL,
            "n500_minus_n100": (round(meds[4] - meds[0], 4)
                                if curve_ok else None)}
        print(f"  [Y2] curve complete={curve_ok} branch={branch} "
              f"medians={[round(m, 4) for m in meds]}")

        # ---------------- GATE-Y3 (the features track) ------------------
        table = {}
        for k in FEATURE_KEYS:
            xs = [r[k] for r in all_inst if r.get(k) is not None
                  and r.get("residual") is not None]
            ys = [r["residual"] for r in all_inst if r.get(k) is not None
                  and r.get("residual") is not None]
            rho = _spearman(xs, ys) if len(xs) >= 3 else float("nan")
            table[k] = round(rho, 4) if np.isfinite(rho) else None
        shift = {}
        for k in FEATURE_KEYS:
            v100 = [r[k] for r in rungs["100"]["instances"]
                    if r.get(k) is not None]
            v500 = [r[k] for r in rungs["500"]["instances"]
                    if r.get(k) is not None]
            m100 = float(np.mean(v100)) if v100 else None
            m500 = float(np.mean(v500)) if v500 else None
            shift[k] = {
                "mean_n100": (round(m100, 6)
                              if m100 is not None else None),
                "mean_n500": (round(m500, 6)
                              if m500 is not None else None),
                "delta_n500_minus_n100":
                    (round(m500 - m100, 6)
                     if m100 is not None and m500 is not None else None)}
        feats_complete = all(
            r.get(k) is not None and np.isfinite(r[k])
            for r in all_inst for k in FEATURE_KEYS)
        result["gates"]["Y3_features_track"] = {
            "pass": bool(feats_complete),
            "feature_keys": FEATURE_KEYS,
            "spearman_vs_residual_pooled50": table,
            "shift_table_n100_vs_n500": shift,
            "all_features_finite_all_50": bool(feats_complete)}
        print(f"  [Y3] features complete={feats_complete} rho table "
              f"{table}")

        # ---------------- GATE-Y4 (hygiene) -----------------------------
        anomalies = []
        seeds_seen = [r["gen_seed"] for r in all_inst]
        if len(set(seeds_seen)) != len(seeds_seen):
            anomalies.append("gen_seed collision across rungs")
        for r in all_inst:
            if r["n"] != r["n_registered"]:
                anomalies.append(f"n mismatch seed={r['gen_seed']}")
            want = "flip_per" if (r["i"] % 2 == 0) else "flip_aper"
            if r["cls"] != want:
                anomalies.append(f"class parity seed={r['gen_seed']}")
        for n in LADDER_N:
            if sorted(r["i"] for r in rungs[str(n)]["instances"]) \
                    != list(range(PER_RUNG)):
                anomalies.append(f"rung {n} instance set incomplete")
        with open(DEP169) as f:
            dep = json.load(f)
        dep_res = [float(np.median(r["errs_scoped"])) - N3_BAR
                   for r in dep["sections"]["grid"]["instances"]
                   if r.get("n") == 100 and r.get("errs_scoped")]
        lo, hi = (min(dep_res), max(dep_res)) if dep_res \
            else (None, None)
        med100_res = rungs["100"]["pooled_median_residual"]
        replay_ok = bool(med100_res is not None and lo is not None
                         and lo - 1e-09 <= med100_res <= hi + 1e-09)
        restore_floor()
        pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None)
                     == _saved[m.__name__] for m in PIN_MODULES)
        result["gates"]["Y4_hygiene"] = {
            "pass": bool(pin_ok and not anomalies and replay_ok),
            "pin": {"floor": DEP169_FLOOR,
                    "save_restore_asserted": bool(pin_ok)},
            "cross_rung_anomalies": anomalies,
            "zero_cross_rung_anomalies": not anomalies,
            "n100_replay": {
                "pooled_median_residual": med100_res,
                "deposited_band_exp169_S4": [lo, hi],
                "in_band": replay_ok}}
        print(f"  [Y4] pin_ok={pin_ok} anomalies={anomalies} "
              f"n100 replay {med100_res} in [{lo}, {hi}]: {replay_ok}")

        gate_order = ["Y1_ladder_integrity", "Y2_curve_branch",
                      "Y3_features_track", "Y4_hygiene"]
        result["verdict"] = "/".join(
            "PASS" if result["gates"][g]["pass"] else "REFUTE"
            for g in gate_order) + " gates"
    else:
        result["partial"] = True
        result["verdict"] = (
            f"PARTIAL (rungs merged: {len(rungs)}/5; gates evaluate "
            "exactly once, when all 5 rungs are present)")

    result["claim"] = ("the read's n-scaling: the residual-vs-n curve "
                       "over n=100..500 (10 fresh instances per rung, "
                       "scoped production arm under the -35.0 pin), "
                       "branch MONOTONE/SATURATING/NON-MONOTONE named "
                       "by the pre-named branches")
    result["config"] = {
        "ladder_n": LADDER_N, "per_rung": PER_RUNG,
        "seed_formula": "GRID_BASE_SEED + 5000 + 100*rung_idx + i",
        "class_rule": "i even -> flip_per, i odd -> flip_aper",
        "decode_seeds": list(SEEDS), "pin_floor": DEP169_FLOOR,
        "n3_bar": N3_BAR, "saturation_tol": SATURATION_TOL,
        "jobs": jobs, "smoke": False}
    result["rejections"] = rejections
    result["runtime_s"] = round(time.time() - t0, 1)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    print(f"\n  deposit: {out_path} ({result['runtime_s']} s)")
    print(f"  verdict: {result['verdict']}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["rung0", "rung1", "rung2",
                                      "rung3", "rung4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
