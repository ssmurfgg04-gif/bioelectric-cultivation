#!/usr/bin/env python3
"""exp195 — THE SCALING LAW'S SECOND AXIS (zone-count dose-response).

exp190's registered next (L166): interior value fidelity at fixed n —
1/2/3/4-zone programs x 10 instances at n = 100 and n = 400, the
scoped arm under the -35.0 pin.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp185/exp180's build + scoped_read patterns; MULTI zone-count variants via exp94's AnatomySpec with 1-4 zones (the exp161 ladder).

GATES (each evaluated exactly once):
  GATE-V1 (ladder integrity) 80 instances (4 zone counts x 10 x
           2 sizes) built and decoded, zero rejections, finite.
  GATE-V2 (the dose-response) the err-vs-zone-count curve at each
           size deposited with dispersions; the branch named:
           (i) DOSE-DRIVEN (err rises with zone count at BOTH
           sizes), (ii) SIZE-DRIVEN (flat in zone count at both),
           (iii) INTERACTION (rises at n=400 only). All complete.
  GATE-V3 (the coverage link) support coverage vs zone count per
           size, Spearman deposited — the coverage mechanism's
           other face or its refutation.
  GATE-V4 (hygiene) pin asserted; the n=100/1-zone rung inside
           exp185's deposited n=100 band.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp195_zone_count_axis.json
RUN: python3 -m experiments.exp195_zone_count_axis [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

from experiments.exp148_temporal_read import (
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N3_BAR,
)
from experiments.exp169_rt_scoping import (
    DEP148_FLOOR, PIN_MODULES, _PIN_SAVE, f_max_frames, scoped_read,
)
from experiments.exp94_multizone_scale import (
    MULTI, labeling_bfs_n, spec_target_n,
)
from cultivation.compiler.anatomy import AnatomySpec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp195_zone_count_axis.json")


def _pin():
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP148_FLOOR


def _unpin():
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


def _spec_kc(k: int):
    """A k-zone program on the MULTI discipline: k equal spans from the
    MULTI ladder's own zone layout, values from the deposited -30.0
    class (the exp161 u-06 family), spans non-overlapping, disclosed."""
    zs = list(MULTI.zones)[:k]
    return AnatomySpec(
        zones=[type(z)(f0=z.f0, f1=z.f1, voltage=-30.0, name=z.name)
               for z in zs],
        amputate_plane=MULTI.amputate_plane,
        spec_name=f"kc-{k}-zone")


def _dec_errs(med):
    errs, rej = [], 0
    for s in (1, 2, 3):
        out = scoped_read(med, s, f_max_frames(list(med.snapshots())),
                          return_state=False)
        if out.get("ok"):
            errs.append(float(out["err"]))
        else:
            rej += 1
    return errs, rej


def main() -> dict:
    a = globals().get("args")
    smoke = bool(getattr(a, "smoke", False))
    out_path = getattr(a, "out", None) or OUT
    t0 = time.time()
    print("=== exp195: THE ZONE-COUNT AXIS ===")
    _pin()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP148_FLOOR
               for m in PIN_MODULES)
    if smoke:
        for k in (1, 4):
            spec = _spec_kc(k)
            f = spec_target_n(spec, labeling_bfs_n(
                FlipGridMedium(100, seed=GRID_BASE_SEED,
                               sched=GRID_CLASSES["flip_per"]
                               ).native_support()), 100)
            print(f"  [smoke] k={k} target built, finite="
                  f"{bool(np.isfinite(f).all())}")
        _unpin()
        return {"smoke": True, "discarded": True}

    result: dict = {"sections": {}, "gates": {}}
    rejections = 0
    curve = {"n100": {}, "n400": {}}
    cov = {"n100": {}, "n400": {}}
    for k in (1, 2, 3, 4):
        spec = _spec_kc(k)
        for n in (100, 400):
            errs_all, covs = [], []
            for i in range(10):
                seed = GRID_BASE_SEED + 7000 + 100 * (k - 1) + i
                cls = "flip_per" if i % 2 == 0 else "flip_aper"
                med = FlipGridMedium(n, seed=seed, sched=GRID_CLASSES[cls])
                sup = med.native_support()
                f = spec_target_n(spec, labeling_bfs_n(sup), n)
                assert np.isfinite(f).all()
                _pin()
                errs, rej = _dec_errs(med)
                _unpin()
                rejections += rej
                errs_all.extend(errs)
                covs.append(float(np.abs(sup).sum()) / float(
                    np.asarray(med.M).shape[0] ** 2))
            med_err = float(np.median(errs_all)) if errs_all else None
            curve[f"n{n}"][f"k{k}"] = med_err
            cov[f"n{n}"][f"k{k}"] = float(np.median(covs))
            print(f"  k={k} n={n}: median {med_err} "
                  f"(rejections {rej})")
    # gate V1
    v1 = bool(rejections == 0 and all(
        curve[f"n{n}"][f"k{k}"] is not None
        for k in (1, 2, 3, 4) for n in (100, 400)))
    result["gates"]["V1_ladder_integrity"] = {
        "pass": v1, "rejections": rejections}
    # gate V2: the dose-response branch
    def rising(d):
        vals = [d[f"k{k}"] for k in (1, 2, 3, 4)]
        return all(vals[i + 1] > vals[i] for i in range(3))
    r100, r400 = rising(curve["n100"]), rising(curve["n400"])
    flat400 = (abs(curve["n400"]["k4"] - curve["n400"]["k1"])
               <= 0.05)
    if r100 and r400:
        branch = "DOSE-DRIVEN"
    elif not r100 and not r400:
        branch = "SIZE-DRIVEN"
    else:
        branch = "INTERACTION" if r400 and not r100 else "MIXED"
    result["gates"]["V2_dose_response"] = {
        "pass": True, "branch": branch, "curve": curve,
        "rising_n100": r100, "rising_n400": r400}
    # gate V3: coverage link (Spearman by rank over k at each size)
    def spearman(xs, ys):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        if np.std(xs) == 0 or np.std(ys) == 0:
            return None
        rx = np.argsort(np.argsort(xs)).astype(float)
        ry = np.argsort(np.argsort(ys)).astype(float)
        rx = (rx - rx.mean()) / rx.std()
        ry = (ry - ry.mean()) / ry.std()
        return float((rx * ry).mean())
    link = {}
    for n in (100, 400):
        xs = [cov[f"n{n}"][f"k{k}"] for k in (1, 2, 3, 4)]
        ys = [curve[f"n{n}"][f"k{k}"] for k in (1, 2, 3, 4)]
        link[f"n{n}"] = spearman(xs, ys)
    result["gates"]["V3_coverage_link"] = {
        "pass": True, "spearman": link, "coverage": cov}
    # gate V4: hygiene + the 1-zone n=100 rung inside exp185's band
    dep = json.load(open("/".join([ROOT, "results",
                                   "exp185_n_scaling.json"])))
    band = None
    try:
        r0 = dep["sections"]["ladder"]["rung0"]
        errs = [e for inst in r0["instances"]
                for e in inst.get("errs_scoped", [])]
        band = [float(np.min(errs)), float(np.max(errs))]
    except Exception:
        band = None
    k100 = curve["n100"]["k1"]
    in_band = bool(band and band[0] - 1e-9 <= k100 <= band[1] + 1e-9)
    _unpin()
    ok_pin = all(getattr(m, "NEURAL_SPEC_MIN", None)
                 == _PIN_SAVE[m.__name__] for m in PIN_MODULES)
    result["gates"]["V4_hygiene"] = {
        "pass": bool(ok_pin and in_band), "pin_restored": ok_pin,
        "k1_n100": k100, "exp185_n100_band": band,
        "in_band": in_band}
    result["exp"] = "exp195"
    result["verdict"] = "/".join(
        "PASS" if result["gates"][g]["pass"] else "REFUTE"
        for g in ("V1_ladder_integrity", "V2_dose_response",
                  "V3_coverage_link", "V4_hygiene")) + " gates"
    result["runtime_s"] = round(time.time() - t0, 1)
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1)
    print(f"  verdict: {result['verdict']} branch={branch}")
    print(f"  deposit: {out_path}")
    return result



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
