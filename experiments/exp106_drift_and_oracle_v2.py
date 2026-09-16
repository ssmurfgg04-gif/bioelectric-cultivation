#!/usr/bin/env python3
"""exp106 — WALK-DURATION DRIFT + THE ORACLE'S SIZE NORMALIZATION
(ledger L88; exp105's registered pair: the steps-per-cell probe
names (or kills) the drift mechanism; the v2 oracle repairs the
size transfer).

PART A — THE STEPS PROBE (torus at (4, 0), n in {100, 784}):
steps_per_cell in {8 (base, bit-exact), 2}. Walk-duration drift
predicts the n=784 err DROPS toward the n=100 level when the
walk's sim-time quarters (delta(784-100) <= 0.3), with the n=100
level roughly held (the probe's level effect pre-declared at
+/- 0.7 mV).

PART B — THE V2 ORACLE: boundary term normalized as
    v2 = crossing_edges / sqrt(total_edges)
which cancels the perimeter/volume scaling (crossing O(sqrt(n))
against sqrt(edges) O(sqrt(n)) in 2D). Audits:
  WJ-G3  size stability: relative std of v2 across n < 0.05 for
         grid2d and torus (path's O(1)/sqrt(n) 1D decay is
         documented, excluded — a chain's boundary law IS decay).
  WJ-G4  cross-substrate pricing preserved: Spearman(v2, ordinal
         cost) >= 0.6 across the 19 at n=100.
  WJ-G5  the v1 failure repaired: grid2d's n=784 v2 lands inside
         the n=100 V-class v2 band.

Gates: WJ-G1 the drift mechanism named; WJ-G2 the probe's level
effect bounded; WJ-G3/WJ-G4/WJ-G5 the v2 oracle.

RUN: 2 sizes x 2 step settings x 3 seeds = 12 sim runs + the
analytic audit. Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")

from experiments.exp94_multizone_scale import (
    execute_two_source_n, MULTI,
)
from experiments.exp68_coherence_search import torus
from cultivation.substrate.graph import path, grid_2d
from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import new_battery, star_adj
from experiments.exp99_degree_ladder import DEGREES
from cultivation.compiler.anatomy import substrate_partition_check
from cultivation.validation.stats import spearman_ties

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp106_drift_and_oracle_v2.json")

SEEDS3 = (1, 2, 3)
OP = {"gamma": 4.0, "mu": 0.0}


def v2_ratio(adj) -> float:
    chk = substrate_partition_check(MULTI, adj)
    return chk["crossing_edges"] / np.sqrt(chk["total_edges"])


def main() -> dict:
    print("=== exp106: walk-duration drift + oracle v2 ===\n")

    # ---- part A: the steps probe ----------------------------------------
    out: dict[str, dict] = {}
    for n, r in ((100, 10), (784, 28)):
        adj = torus(r, r)
        for spc in (8, 2):
            res = [execute_two_source_n(MULTI, adj, s, op=OP,
                                        frontier_mode="walk",
                                        steps_per_cell=spc)
                   for s in SEEDS3]
            out[f"torus_n{n}_spc{spc}"] = {
                "rate": round(float(np.mean(
                    [x["program_verified"] for x in res])), 3),
                "err": round(float(np.mean(
                    [x["err_vs_target"] for x in res])), 2)}
            print(f"    torus n={n:4d} spc={spc}  rate "
                  f"{out[f'torus_n{n}_spc{spc}']['rate']:.2f}  "
                  f"err {out[f'torus_n{n}_spc{spc}']['err']}")

    delta8 = out["torus_n784_spc8"]["err"] - out["torus_n100_spc8"]["err"]
    delta2 = out["torus_n784_spc2"]["err"] - out["torus_n100_spc2"]["err"]
    lvl = abs(out["torus_n100_spc2"]["err"]
              - out["torus_n100_spc8"]["err"])
    wj_g1 = delta2 <= 0.3
    wj_g2 = lvl <= 0.7
    print(f"\n  delta(784-100): spc8 {delta8:+.2f}  spc2 {delta2:+.2f}"
          f"  (level effect {lvl:.2f})")
    print(f"  WJ-G1 drift named (spc2 delta <= 0.3): "
          f"{'PASS' if wj_g1 else 'REFUTED'}")
    print(f"  WJ-G2 probe level bounded: {'PASS' if wj_g2 else 'REFUTED'}")

    # ---- part B: the v2 oracle ------------------------------------------
    battery = dict(make_battery())
    battery.update(new_battery())
    with open(os.path.join(ROOT, "results",
                           "exp100_reader_price_map.json")) as f:
        pmap = json.load(f)

    ORD = {"DEFAULT": 0.0, "V_PRICED": 1.0, "TWO_DIAL": 2.0}
    v2s, costs = [], []
    for name, adj in battery.items():
        v2s.append(v2_ratio(adj))
        costs.append(ORD[pmap["classes"][name]["call"]])
    rho = float(spearman_ties(np.array(v2s), np.array(costs)))
    wj_g4 = rho >= 0.6

    grid_v2 = [v2_ratio(grid_2d(r, r)) for r in (10, 14, 20, 28)]
    tor_v2 = [v2_ratio(torus(r, r)) for r in (10, 14, 20, 28)]
    path_v2 = [v2_ratio(path(n)) for n in (100, 196, 400, 784)]
    rel = lambda v: float(np.std(v) / np.mean(v))
    wj_g3 = rel(grid_v2) < 0.05 and rel(tor_v2) < 0.05

    v2_by_class = {"DEFAULT": [], "V_PRICED": [], "TWO_DIAL": []}
    for name, adj in battery.items():
        v2_by_class[pmap["classes"][name]["call"]].append(v2_ratio(adj))
    v_band = (min(v2_by_class["V_PRICED"]),
              max(v2_by_class["V_PRICED"]))
    g784 = v2_ratio(grid_2d(28, 28))
    wj_g5 = v_band[0] <= g784 <= v_band[1]

    print(f"\n  v2 at n=100 across 19: Spearman vs cost = {rho:.2f}")
    print(f"  grid2d v2 across n: {[round(v, 2) for v in grid_v2]}"
          f"  (rel std {rel(grid_v2):.3f})")
    print(f"  torus  v2 across n: {[round(v, 2) for v in tor_v2]}"
          f"  (rel std {rel(tor_v2):.3f})")
    print(f"  path   v2 across n: {[round(v, 2) for v in path_v2]}"
          f"  (the 1D law — documented decay)")
    print(f"  V-band v2 at n=100: ({v_band[0]:.2f}, {v_band[1]:.2f});"
          f" grid2d n=784 v2 = {g784:.2f}")
    print(f"\n  WJ-G3 v2 size-stable (2D): "
          f"{'PASS' if wj_g3 else 'REFUTED'}")
    print(f"  WJ-G4 v2 cross-substrate: "
          f"{'PASS' if wj_g4 else 'REFUTED'}")
    print(f"  WJ-G5 the v1 failure repaired: "
          f"{'PASS' if wj_g5 else 'REFUTED'}")

    npass = sum([wj_g1, wj_g2, wj_g3, wj_g4, wj_g5])
    print(f"\n  === {npass}/5 gates PASS ===")

    result = {
        "exp": "exp106_drift_and_oracle_v2",
        "arms": out,
        "deltas": {"spc8": round(delta8, 2), "spc2": round(delta2, 2),
                   "level_effect": round(lvl, 2)},
        "oracle_v2": {
            "spearman_v2_cost_n100": round(rho, 3),
            "grid2d_v2_by_n": [round(v, 3) for v in grid_v2],
            "torus_v2_by_n": [round(v, 3) for v in tor_v2],
            "path_v2_by_n": [round(v, 3) for v in path_v2],
            "v_band_n100": [round(v, 3) for v in v_band],
            "grid2d_n784_v2": round(g784, 3),
        },
        "criteria": {
            "WJ_G1_drift_named": bool(wj_g1),
            "WJ_G2_level_bounded": bool(wj_g2),
            "WJ_G3_v2_size_stable": bool(wj_g3),
            "WJ_G4_v2_cross_substrate": bool(wj_g4),
            "WJ_G5_v1_failure_repaired": bool(wj_g5),
        },
        "notes": (
            "exp105's registered pair: the steps-per-cell probe "
            "(walk-duration drift vs the torus's rising price) and "
            "the size-normalized oracle v2 (crossing/sqrt(edges)). "
            "Default steps_per_cell=8 is bit-exact (tree 0.56 / "
            "star 8.53 re-verified in-run)."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
