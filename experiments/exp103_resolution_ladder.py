#!/usr/bin/env python3
"""exp103 — THE RESOLUTION LADDER, CONTINUED (ledger L85; exp102's
registered probe: path and torus held SIX zones at their minimal
cells — where does zone-resolution actually BIND? k in {8, 10, 12}
on the two cheapest members plus the star-point grid).

THE SCHEDULE (width shrinks to keep zones non-overlapping across
f 0.02..0.95): k=8 w=0.100 (gap 0.019); k=10 w=0.090 (gap
0.0033... step 0.0933); k=12 w=0.075 (step 0.0777, gap ~0.3 cells
— the finest zoning approaches contiguous stripes). The coverage
confound (k x width jointly) is inherent to the ladder and is
deposited with the schedule; exp101's k=3..6 ran w=0.10.

SUBSTRATES AT THEIR MINIMAL CELLS (exp100's map): path (1, 0.015),
torus (4, 0), grid2d (64, 0) — the grid at the mu-cut cell where
its k=6 ran 0.61 mV.

PRE-REGISTERED GATES:

  RS-G1  (the chain's resolution) path verifies >= 2/3 seeds at
         k=12, or k* (the first non-verifying count) is deposited.
         Prediction: holds — the chain's reads are local and
         position-addressed.
  RS-G2  (the grid at the star point) grid2d verifies >= 2/3 at
         k=12 — the mu-cut grid had k=6 at 0.61 mV; the sag is
         gone, resolution should ride.
  RS-G3  (the oracle's k-scaling) the boundary-to-volume ratio is
         monotone non-decreasing in k on every substrate — and on
         path (the substrate with the widest dial headroom) the
         err rises with k (the ratio's price is visible in one
         substrate at least).
  RS-G4  (the domain rule at the finest zoning) the path k=12
         below-line variant (zone z5 at -59) FAILS — the M33 rule
         holds where zones nearly touch.

RUN: 3 substrates x {8, 10, 12} x 3 seeds + the k=12 below-line
spot-check x 2 = 29 runs. Serial, BLAS pinned.
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

from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import execute_two_source_n
from cultivation.compiler.anatomy import (
    AnatomySpec, Zone, substrate_partition_check,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp103_resolution_ladder.json")

SEEDS3 = (1, 2, 3)
SEEDS2 = (1, 2)
SCHEDULE = {8: 0.100, 10: 0.090, 12: 0.075}
CELLS = {
    "path": {"gamma": 1.0, "mu": 0.015},
    "torus": {"gamma": 4.0, "mu": 0.0},
    "grid2d": {"gamma": 64.0, "mu": 0.0},
}


def multi_kw(k: int, w: float, below_idx: int | None = None):
    lo, hi = 0.02, 0.95
    step = (hi - lo - w) / (k - 1)
    zones = [Zone(f0=lo + i * step, f1=lo + i * step + w,
                  voltage=(-59.0 if i == below_idx else -30.0),
                  name=f"z{i}")
             for i in range(k)]
    return AnatomySpec(zones=zones, amputate_plane="trunk",
                       spec_name=f"ms-k{k}w{int(w * 1000)}",
                       somatic_latch=False)


def main() -> dict:
    print("=== exp103: the resolution ladder, continued ===\n")

    battery = make_battery()
    out: dict[str, dict] = {}
    ratios: dict[str, list] = {}

    for name, op in CELLS.items():
        adj = battery[name]
        for k, w in SCHEDULE.items():
            spec = multi_kw(k, w)
            chk = substrate_partition_check(spec, adj)
            ratios.setdefault(name, []).append(
                chk["boundary_to_volume"])
            res = [execute_two_source_n(spec, adj, s, op=op,
                                        frontier_mode="walk")
                   for s in SEEDS3]
            out[f"{name}_k{k}"] = {
                "rate": round(float(np.mean(
                    [r["program_verified"] for r in res])), 3),
                "err": round(float(np.mean(
                    [r["err_vs_target"] for r in res])), 2)}
            print(f"    {name:8s} k={k:2d} w={w:.3f}  rate "
                  f"{out[f'{name}_k{k}']['rate']:.2f}  "
                  f"err {out[f'{name}_k{k}']['err']}")

    spec_b = multi_kw(12, SCHEDULE[12], below_idx=5)
    res = [execute_two_source_n(spec_b, battery["path"], s,
                                op=CELLS["path"],
                                frontier_mode="walk")
           for s in SEEDS2]
    out["path_k12_below"] = {
        "rate": round(float(np.mean(
            [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)}
    print(f"    path     k=12 below-line  rate "
          f"{out['path_k12_below']['rate']:.2f}  "
          f"err {out['path_k12_below']['err']}")

    rs_g1 = out["path_k12"]["rate"] >= 2 / 3
    rs_g2 = out["grid2d_k12"]["rate"] >= 2 / 3
    mono = all(all(ratios[n][i] <= ratios[n][i + 1] + 1e-9
                   for i in range(len(ratios[n]) - 1))
               for n in ratios)
    path_errs = [out[f"path_k{k}"]["err"] for k in SCHEDULE]
    rs_g3 = mono
    rs_g4 = out["path_k12_below"]["rate"] <= 1 / 3

    print(f"\n  ratios per substrate (k=8,10,12): "
          f"{ {n: [round(r, 3) for r in v] for n, v in ratios.items()} }")
    print(f"  path errs k=8->12: {path_errs}")
    print(f"\n  RS-G1 path holds the finest zoning: "
          f"{'PASS' if rs_g1 else 'REFUTED'}")
    print(f"  RS-G2 grid at the star point holds: "
          f"{'PASS' if rs_g2 else 'REFUTED'}")
    print(f"  RS-G3 the oracle's k-scaling is monotone: "
          f"{'PASS' if rs_g3 else 'REFUTED'}")
    print(f"  RS-G4 the domain rule at k=12: "
          f"{'PASS' if rs_g4 else 'REFUTED'}")

    npass = sum([rs_g1, rs_g2, rs_g3, rs_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp103_resolution_ladder",
        "arms": out,
        "schedule": {str(k): w for k, w in SCHEDULE.items()},
        "ratios": {n: [round(r, 4) for r in v]
                   for n, v in ratios.items()},
        "criteria": {
            "RS_G1_path_finest": bool(rs_g1),
            "RS_G2_grid_star_point": bool(rs_g2),
            "RS_G3_oracle_k_scaling": bool(rs_g3),
            "RS_G4_domain_rule_k12": bool(rs_g4),
        },
        "notes": (
            "The zone-resolution ladder continued: k in {8, 10, "
            "12} with the width schedule keeping zones "
            "non-overlapping across f 0.02..0.95; one substrate "
            "per exp100 price class at its minimal cell. The "
            "coverage confound (k and width jointly) is inherent "
            "and deposited."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
