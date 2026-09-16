#!/usr/bin/env python3
"""exp104 — THE SIZE AXIS (ledger L86; exp103's registered probe:
the price's n-scaling — exp94's 2-substrate n-scale at (64, 0)
becomes a map at the mapped minimal cells).

THE FAMILY: path(n), grid2d(r x r), torus(r x r) at n in
{100, 196, 400, 784} (grid/torus refined 10->14->20->28; the exact
cell counts deposited). k=3 MULTI verbatim, frontier_mode="walk".

THE CELLS (exp100's map verbatim): path (1, 0.015) DEFAULT,
grid2d (64, 0.015) V_PRICED, torus (4, 0) TWO_DIAL. The grid at
its MAPPED cell carries the theta sag — its err trend in n is the
mean-field question.

PRE-REGISTERED GATES:

  SZ-G1  (DEFAULT scales) path verifies >= 2/3 seeds at EVERY n,
         with err non-increasing from n=100 (exp94's hint:
         path200's 2.38 beat path100's 2.91 — the sag is a
         mean-field effect and bigger discs dilute it).
  SZ-G2  (the grid's price at scale) grid2d at its mapped cell
         verifies at EVERY n (deposit the err trend).
  SZ-G3  (torus holds) torus verifies at EVERY n.
  SZ-G4  (the oracle is size-stable) the boundary-to-volume ratio
         is ~n-invariant per family (std across n < 0.02) — the
         ratio is a SHAPE number, not a size number, so the
         exp100 class calls transfer across the size axis.

RUN: 3 families x 4 sizes x 3 seeds = 36 runs. Serial, BLAS
pinned.
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

from experiments.exp94_multizone_scale import (
    execute_two_source_n, MULTI,
)
from experiments.exp68_coherence_search import torus
from cultivation.substrate.graph import path, grid_2d
from cultivation.compiler.anatomy import substrate_partition_check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp104_size_axis.json")

SEEDS3 = (1, 2, 3)
SIZES = (100, 196, 400, 784)
CELLS = {
    "path": {"gamma": 1.0, "mu": 0.015},
    "grid2d": {"gamma": 64.0, "mu": 0.015},
    "torus": {"gamma": 4.0, "mu": 0.0},
}


def family_adj(name: str, n: int) -> np.ndarray:
    if name == "path":
        return path(n)
    r = int(round(n ** 0.5))
    if name == "grid2d":
        return grid_2d(r, r)
    return torus(r, r)


def main() -> dict:
    print("=== exp104: the size axis ===\n")

    out: dict[str, dict] = {}
    ratios: dict[str, list] = {}
    sizes_used: dict[str, list] = {}

    for name, op in CELLS.items():
        for n in SIZES:
            adj = family_adj(name, n)
            chk = substrate_partition_check(MULTI, adj)
            ratios.setdefault(name, []).append(
                chk["boundary_to_volume"])
            sizes_used.setdefault(name, []).append(adj.shape[0])
            res = [execute_two_source_n(MULTI, adj, s, op=op,
                                        frontier_mode="walk")
                   for s in SEEDS3]
            out[f"{name}_n{adj.shape[0]}"] = {
                "rate": round(float(np.mean(
                    [r["program_verified"] for r in res])), 3),
                "err": round(float(np.mean(
                    [r["err_vs_target"] for r in res])), 2)}
            print(f"    {name:8s} n={adj.shape[0]:4d}  rate "
                  f"{out[f'{name}_n{adj.shape[0]}']['rate']:.2f}  "
                  f"err {out[f'{name}_n{adj.shape[0]}']['err']}")

    def rates(fam):
        return [out[f"{fam}_n{v}"]["rate"]
                for v in sizes_used[fam]]

    path_errs = [out[f"path_n{v}"]["err"] for v in sizes_used["path"]]
    sz_g1 = (all(r >= 2 / 3 for r in rates("path"))
             and path_errs[1] <= path_errs[0])
    sz_g2 = all(r >= 2 / 3 for r in rates("grid2d"))
    sz_g3 = all(r >= 2 / 3 for r in rates("torus"))
    ratio_stds = {n: float(np.std(v)) for n, v in ratios.items()}
    sz_g4 = all(s < 0.02 for s in ratio_stds.values())

    print(f"\n  path errs vs n: {dict(zip(sizes_used['path'], path_errs))}")
    print(f"  ratio stds per family: "
          f"{ {n: round(s, 4) for n, s in ratio_stds.items()} }")
    print(f"\n  SZ-G1 DEFAULT scales (path): "
          f"{'PASS' if sz_g1 else 'REFUTED'}")
    print(f"  SZ-G2 the grid's price at scale: "
          f"{'PASS' if sz_g2 else 'REFUTED'}")
    print(f"  SZ-G3 torus holds: {'PASS' if sz_g3 else 'REFUTED'}")
    print(f"  SZ-G4 the oracle is size-stable: "
          f"{'PASS' if sz_g4 else 'REFUTED'}")

    npass = sum([sz_g1, sz_g2, sz_g3, sz_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp104_size_axis",
        "arms": out,
        "sizes_used": sizes_used,
        "ratios": {n: [round(r, 4) for r in v]
                   for n, v in ratios.items()},
        "criteria": {
            "SZ_G1_default_scales": bool(sz_g1),
            "SZ_G2_grid_at_scale": bool(sz_g2),
            "SZ_G3_torus_holds": bool(sz_g3),
            "SZ_G4_oracle_size_stable": bool(sz_g4),
        },
        "notes": (
            "The price's n-scaling: 3 substrate families x 4 sizes "
            "x 3 seeds at their exp100 mapped minimal cells "
            "(path DEFAULT, grid2d V(64, 0.015), torus TWO(4, 0)). "
            "k=3 MULTI verbatim; the sag is the mean-field "
            "question."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
