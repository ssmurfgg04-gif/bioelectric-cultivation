#!/usr/bin/env python3
"""exp101 — THE ZONE-COUNT LADDER (ledger L83; exp100's registered
map: the compiler's zone-resolution limit — MULTI carries 3 zones;
how many can the two-source read hold at n=100?).

THE FAMILY: k-zone MULTI variants, all zones at -30 (above the M33
line), width 0.10 each, spread evenly over f 0.02..0.95:
  k=3  the deposited MULTI verbatim (the control column);
  k=4  [0.02-0.12][0.297-0.397][0.573-0.673][0.85-0.95];
  k=5  step 0.2075; k=6  step 0.166 (gaps ~6-7 cells).
The substrate set: path, grid2d, torus — one per exp100 class
(DEFAULT (1, 0.015) / V_PRICED (64, 0.015) / TWO_DIAL (4, 0)) —
each at its OWN minimal cell from the reader's price map.

PRE-REGISTERED GATES:

  ZC-G1  (the resolution) k=6 verifies >= 2/3 seeds on ALL THREE
         substrates at their minimal cells — the reader holds six
         zones at n=100.
  ZC-G2  (the compiler agrees) substrate_partition_check passes
         every (substrate, k) pair — the compiler neither over-
         promises nor under-promises at these counts.
  ZC-G3  (the domain rule scales) the k=6 below-line variant (zone
         z2 at -59) FAILS on path — pushing more zones does not
         sneak past the M33 line.
  ZC-G4  (the price of resolution) the k=6 err stays within 2x of
         the k=3 err on the same substrate — resolution does not
         blow the budget.

RUN: 3 substrates x {3, 4, 5, 6} x 3 seeds + the k=6 below-line
spot-check x 2 = 38 runs. Serial, BLAS pinned.
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
from experiments.exp94_multizone_scale import (
    execute_two_source_n, MULTI,
)
from experiments.exp100_reader_price_map import run_cell
from cultivation.compiler.anatomy import (
    AnatomySpec, Zone, substrate_partition_check,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp101_zone_count_ladder.json")

SEEDS3 = (1, 2, 3)
SEEDS2 = (1, 2)

# each substrate's minimal cell from exp100's reader price map
CELLS = {
    "path": {"gamma": 1.0, "mu": 0.015},
    "grid2d": {"gamma": 64.0, "mu": 0.015},
    "torus": {"gamma": 4.0, "mu": 0.0},
}


def multi_k(k: int, below: bool = False) -> AnatomySpec:
    if k == 3:
        if not below:
            return MULTI
        fr = [(0.02, 0.12), (0.30, 0.45), (0.60, 0.75)]
    else:
        width, lo, hi = 0.10, 0.02, 0.95
        step = (hi - lo - width) / (k - 1)
        fr = [(lo + i * step, lo + i * step + width)
              for i in range(k)]
    zones = [Zone(f0=a, f1=b,
                  voltage=(-59.0 if (below and i == 2) else -30.0),
                  name=f"z{i}")
             for i, (a, b) in enumerate(fr)]
    return AnatomySpec(zones=zones, amputate_plane="trunk",
                       spec_name=f"ms-k{k}{'-below' if below else ''}",
                       somatic_latch=False)


def main() -> dict:
    print("=== exp101: the zone-count ladder ===\n")

    battery = make_battery()
    out: dict[str, dict] = {}
    partition = {}

    for name, op in CELLS.items():
        adj = battery[name]
        for k in (3, 4, 5, 6):
            spec = multi_k(k)
            chk = substrate_partition_check(spec, adj)
            partition[f"{name}_k{k}"] = bool(chk["substrate_compilable"])
            res = [execute_two_source_n(spec, adj, s, op=op,
                                        frontier_mode="walk")
                   for s in SEEDS3]
            out[f"{name}_k{k}"] = {
                "rate": round(float(np.mean(
                    [r["program_verified"] for r in res])), 3),
                "err": round(float(np.mean(
                    [r["err_vs_target"] for r in res])), 2)}
            print(f"    {name:8s} k={k}  rate "
                  f"{out[f'{name}_k{k}']['rate']:.2f}  "
                  f"err {out[f'{name}_k{k}']['err']}")

    spec_b = multi_k(6, below=True)
    res = [execute_two_source_n(spec_b, battery["path"], s,
                                op=CELLS["path"], frontier_mode="walk")
           for s in SEEDS2]
    out["path_k6_below"] = {
        "rate": round(float(np.mean(
            [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)}
    print(f"    path     k=6 below-line  rate "
          f"{out['path_k6_below']['rate']:.2f}  "
          f"err {out['path_k6_below']['err']}")

    zc_g1 = all(out[f"{n}_k6"]["rate"] >= 2 / 3 for n in CELLS)
    zc_g2 = all(partition.values())
    zc_g3 = out["path_k6_below"]["rate"] <= 1 / 3
    zc_g4 = all(out[f"{n}_k6"]["err"] <= 2 * out[f"{n}_k3"]["err"]
                for n in CELLS)
    print(f"\n  ZC-G1 six zones hold (all substrates): "
          f"{'PASS' if zc_g1 else 'REFUTED'}")
    print(f"  ZC-G2 the compiler agrees: "
          f"{'PASS' if zc_g2 else 'REFUTED'}")
    print(f"  ZC-G3 domain rule scales: "
          f"{'PASS' if zc_g3 else 'REFUTED'}")
    print(f"  ZC-G4 resolution within budget: "
          f"{'PASS' if zc_g4 else 'REFUTED'}")

    npass = sum([zc_g1, zc_g2, zc_g3, zc_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp101_zone_count_ladder",
        "arms": out,
        "partition": partition,
        "criteria": {
            "ZC_G1_six_zones_hold": bool(zc_g1),
            "ZC_G2_compiler_agrees": bool(zc_g2),
            "ZC_G3_domain_rule_scales": bool(zc_g3),
            "ZC_G4_within_budget": bool(zc_g4),
        },
        "notes": (
            "The compiler's zone-resolution limit: k in {3,4,5,6} "
            "all-at--30 zone specs on one substrate per exp100 "
            "reader-price class, each at its own minimal operating "
            "cell (path DEFAULT, grid2d V(64), torus TWO(4,0)). "
            "k=3 is the deposited MULTI verbatim."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
