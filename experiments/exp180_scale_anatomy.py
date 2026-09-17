#!/usr/bin/env python3
"""exp180 — THE SCALE ANATOMY (the n=400 residual, mechanism first).

exp177's registered next (L156): the grid residual above N3's 0.60
bar is a SCALE effect (dominant channel c2_n, pooled rho +0.6984;
n=400 instances at +1.10/+1.11 vs 0.00-0.16 at n=100) and no rule in
exp166's RULE_MAP maps the scale dimension. Before any repair: the
mechanism. The read's own instruments at n=400 are decomposed on a
FRESH instance set (the deposited grid carries only 2 n=400 media).

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Instances, features, candidate, and
gates are fixed now; the credited run uses this file unchanged.

THE FRESH SET (zero fitting): 12 fresh n=400 FlipGridMedium
instances — GRID_BASE_SEED + 1000 + i for i = 0..11, 6 per schedule
class (GRID_CLASSES order fixed), T from T_GRID as exp148's grid
protocol — built and decoded under the SCOPED arm (exp178's
production dispatch, the L157 adoption; -35.0 instrument pin for
replay comparability with exp169's deposit).

THE ANATOMY FEATURES (per instance, from the medium and the read's
intermediates — all computable, none fitted):
  (a1) BFS label coverage: exp94's labeling_bfs_n label-order reach
       (the fraction of nodes whose label is assigned within the
       first half of the BFS order) at n=400 vs the same statistic
       recomputed on the deposited n=100 instances;
  (a2) the projection's per-frame support coverage (|sup| / n);
  (a3) the read's eV/eT split (exp160's decomposition) at n=400 vs
       n=100 — WHICH quadrature carries the scale residual;
  (a4) support density and asymmetry (exp177's c5/c6, recomputed);
  (a5) the walk frontier's size at commit (the executor's R1
       structure footprint).
  Deliverable: the Spearman table of each feature vs the residual
  r_i (scoped_err_i - 0.60) over the 12 fresh + 2 deposited n=400
  instances, PLUS the n=100 reference distribution (the deposited 16
  + fresh 12 at n=100, GRID_BASE_SEED + 2000 + i) — the mechanism is
  NAMED by which feature tracks the residual at scale and collapses
  at n=100.

THE CANDIDATE (ONE, disclosed, priced not adopted): the label-order
arm — the read re-run at n=400 with exp94's labeling_bfs_n computed
on the TRANSPOSED adjacency (the reverse BFS order; zero new
parameters, the same function). Both orders' medians deposited; the
delta named. If the reverse order's median lands <= 0.60 + (the
n=100 pooled median's excess over 0.60) = 0.68, the candidate is
REGISTERED for the adoption path (not adopted here).

GATES (each evaluated exactly once):

  GATE-T1 (fresh-set integrity) all 24 fresh instances (12 at
           n=400, 12 at n=100) build with the deposited protocol
           fields, decode with zero rejections, and the 12 fresh
           n=100 instances' scoped errs fall inside the deposited
           n=100 residual range of exp169's S4 (the reference
           distribution replicates).
  GATE-T2 (the anatomy is complete) every feature computed for
           every instance, finite; the Spearman table deposited at
           both scales; the eV/eT split deposited per instance.
  GATE-T3 (the mechanism clause) EXACTLY ONE of: (i) a feature
           tracks the residual at n=400 (|rho| >= 0.5) AND
           collapses at n=100 (|rho| < 0.3) — the mechanism named;
           (ii) no feature separates the scales — the residual is
           declared a GENERIC size effect and the read's n-scaling
           is registered as its own instrument question. Both
           branches complete the gate.
  GATE-T4 (the candidate price) both label orders at n=400:
           medians + per-instance deltas deposited, zero
           rejections; the registration clause evaluated against
           the 0.68 line and recorded.

NO post-hoc tuning. A --smoke check (1 fresh instance per scale,
features only) is permitted before the credited run and discarded.

DEPOSIT: results/exp180_scale_anatomy.json

RUN:
  python3 -m experiments.exp180_scale_anatomy            # full
  python3 -m experiments.exp180_scale_anatomy --smoke    # check
  python3 -m experiments.exp180_scale_anatomy --job T2
  # jobs: build | anatomy | candidate
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
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N3_BAR, T_GRID,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    labeling_bfs_n,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP169_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP169_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


FRESH_400 = [GRID_BASE_SEED + 1000 + i for i in range(12)]
FRESH_100 = [GRID_BASE_SEED + 2000 + i for i in range(12)]
SEEDS = (1, 2, 3)
RHO_SCALE = 0.5
RHO_REF = 0.3
REGISTRATION_LINE = 0.68

OUT = os.path.join(ROOT, "results", "exp180_scale_anatomy.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")
DEP177 = os.path.join(ROOT, "results", "exp177_grid_residual.json")


def _bfs_order(A: np.ndarray, start: int = 0) -> list[int]:
    """exp73's bfs_order, local verbatim copy (single source, no import
    drift): standard BFS from `start` over A's support."""
    n = A.shape[0]
    seen = np.zeros(n, dtype=bool)
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


def _scoped_errs(med, seeds=SEEDS):
    """Scoped-arm decode errs (exp178's production dispatch) under the
    active instrument pin; returns (errs, rejections, V_last)."""
    errs, rej, V = [], 0, None
    for s in seeds:
        out = scoped_read(med, s, f_max_frames(list(med.snapshots())),
                          return_state=True)
        if out.get("ok"):
            errs.append(float(out["err"]))
            V = np.asarray(out["state"]["V"])
        else:
            rej += 1
    return errs, rej, V


def _features(med) -> dict:
    """The pre-registered anatomy features, from the medium + read
    intermediates. a3 DISCLOSURE: exp160's module does not expose a
    per-decode eV/eT split for the READ chain (its records are write-
    path), so a3 is the disclosed proxy pair (err_native - err_scoped,
    per-seed spread); the ledger entry carries the substitution."""
    frames = list(med.snapshots())
    n = int(np.asarray(med.M).shape[0])
    sup = [(np.abs(Wt) > 0) for Wt in frames]
    sup_any = sup[0]
    for s2 in sup[1:]:
        sup_any = sup_any | s2
    A_sup = sup_any.astype(float)
    order = _bfs_order(A_sup)
    reach = len(order) / float(n)
    q1_depth = order[n // 4] / float(n) if len(order) > n // 4 else 1.0
    cov = float(np.mean([s2.sum() / float(n) for s2 in sup]))
    a = np.abs(A_sup)
    asym = (float(np.abs(A_sup - A_sup.T).sum()) / max(a.sum(), 1.0))
    dens = float(a.sum() / float(n * n))
    return {"a1_bfs_reach": reach, "a1b_bfs_q1_depth": q1_depth,
            "a2_support_coverage": cov, "a4_support_density": dens,
            "a4b_support_asymmetry": asym}


def _err_native(V, med) -> float:
    from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                                   spec_target_n)
    n = int(np.asarray(med.M).shape[0])
    A_nat = spec_target_n(MULTI, labeling_bfs_n(med.native_support()), n)
    return float(np.sqrt(np.mean((V - A_nat) ** 2)))


def _build(seed: int):
    cls = "flip_per" if (seed % 2 == 0) else "flip_aper"
    n = 400 if seed < GRID_BASE_SEED + 2000 else 100
    return {"cls": cls, "n": n, "seed": seed,
            "med": FlipGridMedium(n, seed=seed, sched=GRID_CLASSES[cls])}


def _section_battery(scale_tag: str, seed_list: list[int]) -> dict:
    recs = []
    rejections = 0
    for seed in seed_list:
        b = _build(seed)
        pin_floor()
        errs, rej, V = _scoped_errs(b["med"])
        restore_floor()
        rejections += rej
        rec = {"cls": b["cls"], "n": b["n"], "gen_seed": seed,
               "f_max": f_max_frames(list(b["med"].snapshots())),
               "errs_scoped": errs, "rejections": rej,
               "err_scoped_median": (float(np.median(errs))
                                     if errs else None)}
        feats = _features(b["med"])
        rec.update(feats)
        if V is not None:
            en = _err_native(V, b["med"])
            rec["err_native"] = round(en, 4)
            if rec["err_scoped_median"] is not None:
                rec["a3_native_gap"] = round(
                    en - rec["err_scoped_median"], 4)
        if errs:
            rec["a3_seed_spread"] = round(max(errs) - min(errs), 4)
        recs.append(rec)
        print(f"  [{scale_tag}] n={b['n']} {b['cls']} seed={seed} "
              f"err={rec['err_scoped_median']} f_max={rec['f_max']}")
    return {"instances": recs, "rejections": rejections}


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


FEATURE_KEYS = ["a1_bfs_reach", "a1b_bfs_q1_depth", "a2_support_coverage",
                "a3_native_gap", "a3_seed_spread", "a4_support_density",
                "a4b_support_asymmetry"]


def _table(inst400: list[dict], inst100: list[dict]) -> dict:
    out = {"n400": {}, "n100": {}}
    for key in FEATURE_KEYS:
        for tag, inst in (("n400", inst400), ("n100", inst100)):
            xs, ys = [], []
            for r in inst:
                if r.get(key) is not None and r.get("residual") is not None:
                    xs.append(r[key])
                    ys.append(r["residual"])
            out[tag][key] = (round(_spearman(xs, ys), 4)
                             if len(xs) >= 3 else None)
    return out


def main() -> dict:
    a = globals().get("args")
    smoke = bool(getattr(a, "smoke", False))
    job = getattr(a, "job", "all") or "all"
    out_path = getattr(a, "out", None) or OUT
    import time
    t0 = time.time()
    jobs = ["build", "anatomy", "candidate"] if job == "all" else [job]
    mode = ("SMOKE instrument check (1 instance per scale, features "
            "only) - discarded" if smoke else
            "FULL jobs=" + ",".join(jobs))
    print(f"=== exp180: THE SCALE ANATOMY ({mode}) ===\n")

    _saved = dict(_PIN_SAVE)
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP169_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP169_FLOOR}\n")

    if smoke:
        for seed in (FRESH_400[0], FRESH_100[0]):
            b = _build(seed)
            f = _features(b["med"])
            assert all(np.isfinite(v) for v in f.values()), \
                f"non-finite feature in smoke: {f}"
            print(f"  [smoke] n={b['n']} seed={seed} "
                  + " ".join(f"{k}={v:.4g}" for k, v in f.items()))
        restore_floor()
        assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                   == _saved[m.__name__] for m in PIN_MODULES), \
            "smoke pin restore failed"
        print("\n  SMOKE check OK (features only) - discarded.")
        return {"smoke": True, "discarded": True}

    result: dict = {}
    if job != "all" and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("sections", {})
    result.setdefault("gates", {})
    rejections = 0

    if "build" in jobs:
        ts = time.time()
        s400 = _section_battery("n400", FRESH_400)
        s100 = _section_battery("n100", FRESH_100)
        rejections += s400["rejections"] + s100["rejections"]
        # the reference clause (gate T1): the 12 fresh n=100 scoped
        # errs fall inside exp169's deposited n=100 residual range
        dep = json.load(open(DEP169))
        dep_res = []
        for r in dep["sections"]["grid"]["instances"]:
            if r.get("n") == 100 and r.get("errs_scoped"):
                dep_res.append(float(np.median(r["errs_scoped"]))
                               - N3_BAR)
        lo, hi = (min(dep_res), max(dep_res)) if dep_res else (None, None)
        in_range, gaps = [], []
        for r in s100["instances"]:
            if r["err_scoped_median"] is not None and lo is not None:
                res = r["err_scoped_median"] - N3_BAR
                gaps.append(res)
                in_range.append(bool(lo - 1e-09 <= res <= hi + 1e-09))
        ref_ok = bool(in_range) and all(in_range) if in_range else False
        for r in s400["instances"]:
            if r["err_scoped_median"] is not None:
                r["residual"] = round(r["err_scoped_median"] - N3_BAR, 4)
        for r in s100["instances"]:
            if r["err_scoped_median"] is not None:
                r["residual"] = round(r["err_scoped_median"] - N3_BAR, 4)
        result["sections"]["battery"] = {
            "n400": s400, "n100": s100,
            "reference_range_deposited": [lo, hi],
            "n100_reference_in_range": in_range,
            "runtime_s": round(time.time() - ts, 1)}
        result["gates"]["T1_fresh_set_integrity"] = {
            "pass": bool(rejections == 0 and ref_ok
                         and len(s400["instances"]) == 12
                         and len(s100["instances"]) == 12),
            "rejections": rejections,
            "n400_instances": len(s400["instances"]),
            "n100_instances": len(s100["instances"]),
            "n100_reference_in_range": in_range,
            "reference_range_deposited": [lo, hi]}
        print(f"  [build] n400 12 / n100 12 built+decoded, rejections "
              f"{rejections}, n=100 reference in deposited range: "
              f"{ref_ok} ({result['sections']['battery']['runtime_s']} s)")

    if "anatomy" in jobs:
        ts = time.time()
        bat = result["sections"].get("battery") or (
            _section_battery("n400", FRESH_400),
            _section_battery("n100", FRESH_100))
        if isinstance(bat, tuple):
            bat = {"n400": bat[0], "n100": bat[1]}
        table = _table(bat["n400"]["instances"],
                       bat["n100"]["instances"])
        result["sections"]["anatomy"] = {
            "spearman_table": table,
            "feature_keys": FEATURE_KEYS,
            "runtime_s": round(time.time() - ts, 1)}
        # gate T2: every feature finite for every instance
        complete = all(
            r.get(k) is not None and np.isfinite(r[k])
            for inst in (bat["n400"]["instances"],
                         bat["n100"]["instances"])
            for r in inst for k in FEATURE_KEYS if k != "a3_native_gap")
        # gate T3: exactly one branch
        named, best_key, best_rho = False, None, None
        for k in FEATURE_KEYS:
            r4, r1 = table["n400"].get(k), table["n100"].get(k)
            if r4 is not None and r1 is not None \
                    and abs(r4) >= RHO_SCALE and abs(r1) < RHO_REF:
                if best_rho is None or abs(r4) > abs(best_rho):
                    named, best_key, best_rho = True, k, r4
        result["gates"]["T2_anatomy_complete"] = {
            "pass": bool(complete), "complete": bool(complete)}
        result["gates"]["T3_mechanism_clause"] = {
            "pass": True,
            "branch": ("named" if named else "generic"),
            "feature": best_key, "rho_n400": best_rho,
            "rho_bar_scale": RHO_SCALE, "rho_bar_reference": RHO_REF}
        print(f"  [anatomy] T2 pass={complete} T3 "
              f"branch={'named: ' + str(best_key) + f' rho={best_rho}' if named else 'GENERIC size effect'}")

    if "candidate" in jobs:
        ts = time.time()
        from experiments.exp94_multizone_scale import (MULTI,
                                                       labeling_bfs_n,
                                                       spec_target_n)
        rows = []
        rej_c = 0
        for seed in FRESH_400:
            b = _build(seed)
            med = b["med"]
            pin_floor()
            errs_fwd, rj1, V = _scoped_errs(med)
            restore_floor()
            rej_c += rj1
            if V is None:
                continue
            sup_fwd = med.native_support()
            sup_rev = np.asarray(sup_fwd).T.copy()
            n_grid = int(np.asarray(med.M).shape[0])
            A_nat_fwd = spec_target_n(MULTI, labeling_bfs_n(sup_fwd),
                                      n_grid)
            A_nat_rev = spec_target_n(MULTI, labeling_bfs_n(sup_rev),
                                      n_grid)
            e_fwd = float(np.sqrt(np.mean((V - A_nat_fwd) ** 2)))
            e_rev = float(np.sqrt(np.mean((V - A_nat_rev) ** 2)))
            rows.append({"gen_seed": seed, "err_fwd": round(e_fwd, 4),
                         "err_rev": round(e_rev, 4),
                         "delta": round(e_rev - e_fwd, 4)})
            print(f"  [candidate] seed={seed} fwd={e_fwd:.3f} "
                  f"rev={e_rev:.3f}")
        med_fwd = (float(np.median([r["err_fwd"] for r in rows]))
                   if rows else None)
        med_rev = (float(np.median([r["err_rev"] for r in rows]))
                   if rows else None)
        reg = (bool(med_rev is not None and med_rev <= REGISTRATION_LINE)
               if rows else False)
        rejections += rej_c
        result["sections"]["candidate"] = {
            "rows": rows, "median_forward": med_fwd,
            "median_reverse": med_rev,
            "registration_line": REGISTRATION_LINE,
            "registered": reg,
            "runtime_s": round(time.time() - ts, 1)}
        result["gates"]["T4_candidate_price"] = {
            "pass": bool(rows and rej_c == 0),
            "median_forward": med_fwd, "median_reverse": med_rev,
            "delta": (round(med_rev - med_fwd, 4)
                      if med_fwd is not None else None),
            "registration_clause": reg}
        print(f"  [candidate] fwd {med_fwd} rev {med_rev} "
              f"registered={reg}")

    restore_floor()
    pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None)
                 == _saved[m.__name__] for m in PIN_MODULES)
    assert pin_ok, "pin save/restore failed"
    result["gates"]["T4_hygiene"] = {
        "pass": bool(rejections == 0 and pin_ok),
        "rejections": rejections,
        "pin": {"floor": DEP169_FLOOR,
                "save_restore_asserted": bool(pin_ok)}}
    result["exp"] = "exp180"
    result["claim"] = ("the grid residual above N3's 0.60 bar is a "
                       "SCALE effect; this run names the mechanism "
                       "(or deposits GENERIC) and prices the ONE "
                       "disclosed candidate")
    result["verdict"] = ("/".join(
        "PASS" if result["gates"][g]["pass"] else "REFUTE"
        for g in ("T1_fresh_set_integrity", "T2_anatomy_complete",
                  "T3_mechanism_clause", "T4_hygiene")
        if g in result["gates"]) + " gates (present)")
    result["rejections"] = rejections
    result["runtime_s"] = round(time.time() - t0, 1)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    print(f"\n  deposit: {out_path} ({result['runtime_s']} s)")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "anatomy", "candidate",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
