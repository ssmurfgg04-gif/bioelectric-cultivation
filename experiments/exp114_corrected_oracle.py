#!/usr/bin/env python3
"""exp114 — THE CORRECTED ORACLE REPLICA (ledger L94's registration:
exp113's rho test was an instrument mismatch — the exp102/106 oracle
claims CLASS-LEVEL pricing (Spearman 0.73 raw / 0.81 v2 against the
dial-class ordinal over the 19 battery), not within-expensive-set
cell errors. This experiment re-tests the oracle under ITS OWN
instrument on the walk-tax-free re-priced map. Assembly only —
every number comes from deposited results.)

THE INSTRUMENT (exp102/106 semantics, exactly):
  ordinal dial cost per member, lexicographic on the ladder
  positions the re-priced map landed on:
    gamma ladder [1, 2, 4, 8, 16, 32, 64]  (idx 0..6)
    mu ladder    [0.015, 0.01, 0.005, 0.002, 0]  (idx 0..4)
    cost = gamma_idx * 10 + mu_idx
  classes (exp113's table):
    DEFAULT0  (1, 0.015): path, path200, cycle, small_world, star
    MU0       (1, 0):     torus, torus_elong, random3, random8,
                          scale_free, scale_free200
    GAMMA0    (16, .015): tree, grid2d, grid_elong
              (8, .015):  ladder, random6
              (4, 0):     barbell
    GEOMETRY  (32, 0):   bipartite, complete
  the v2 ratios: exp113's deposit (computed by exp106's v2_ratio).

PRE-REGISTERED GATES:

  OR-G1  (the oracle survives the corrected re-test) Spearman(v2,
         ordinal cost) over the 19 re-priced members is >= 0.60 —
         weakened survival is admissible (the 0.73/0.81 references
         were measured on walk-taxed cells, an unknown confound at
         the time); below 0.60 the class-level claim is refuted on
         the honest map.
  OR-G2  (class-mean monotonicity) the mean v2 is monotone
         non-decreasing across the re-priced classes ordered by
         mean cost: DEFAULT0 < MU0 < GAMMA0 < GEOMETRY — exp102's
         class structure on the honest map.
  OR-G3  (the geometry pair dominates) every member whose v2 is
         below the pair's minimum (25.03) sits at a STRICTLY
         cheaper cell (cost < 54) — no v2-lower substrate needs a
         costlier cell than the pair; the top tail's semantics
         hold without the walk tax propping them up.

THE DEPOSIT: the corrected Spearman (vs the 0.73/0.81 references),
the class-mean v2 table, the domination check — the oracle's final
form on the walk-tax-free map. exp115 derives from the outcome: PASS
-> the R5' price oracle is a geometry instrument and the compiler's
price map re-issues with walk_speed as a standard dial column;
REFUTED -> the ratio's class pricing was itself a walk-tax artifact
and the oracle's domain shrinks to the geometry pair.

RUN: assembly only (no dynamics). BLAS pinned.
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

from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp114_corrected_oracle.json")

GAMMA_LADDER = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
MU_LADDER = [0.015, 0.01, 0.005, 0.002, 0.0]

CLASSES = {
    "DEFAULT0": ["path", "path200", "cycle", "small_world", "star"],
    "MU0": ["torus", "torus_elong", "random3", "random8",
            "scale_free", "scale_free200"],
    "GAMMA0": ["tree", "grid2d", "grid_elong", "ladder", "random6",
               "barbell"],
    "GEOMETRY": ["bipartite", "complete"],
}
CELLS = {
    "path": [1.0, 0.015], "path200": [1.0, 0.015],
    "cycle": [1.0, 0.015], "small_world": [1.0, 0.015],
    "star": [1.0, 0.015],
    "torus": [1.0, 0.0], "torus_elong": [1.0, 0.0],
    "random3": [1.0, 0.0], "random8": [1.0, 0.0],
    "scale_free": [1.0, 0.0], "scale_free200": [1.0, 0.0],
    "tree": [16.0, 0.015], "grid2d": [16.0, 0.015],
    "grid_elong": [16.0, 0.015], "ladder": [8.0, 0.015],
    "random6": [8.0, 0.015], "barbell": [4.0, 0.0],
    "bipartite": [32.0, 0.0], "complete": [32.0, 0.0],
}


def ordinal_cost(cell):
    g, m = cell
    return GAMMA_LADDER.index(g) * 10 + MU_LADDER.index(m)


def main() -> dict:
    print("=== exp114: the corrected oracle replica ===\n")

    exp113 = json.load(open(os.path.join(
        ROOT, "results", "exp113_repriced_map.json")))
    v2 = {name: rec["v2"] for name, rec in
          exp113["map_spc0"].items() if rec.get("v2") is not None}
    # the 4 DEFAULT members' v2 not in exp113's map_spc0 (they were
    # run fresh there) — compute from exp106's instrument
    from experiments.exp106_drift_and_oracle_v2 import v2_ratio
    from experiments.exp112_walk_speed_ladder import build_battery
    battery = build_battery()
    for name in ("path", "path200", "cycle", "small_world"):
        v2[name] = round(float(v2_ratio(battery[name])), 4)

    costs = {name: ordinal_cost(CELLS[name]) for name in CELLS}
    names = list(CELLS)
    rho = round(float(spearmanr([v2[n] for n in names],
                                [costs[n] for n in names]).statistic),
                3)
    print(f"    v2: {v2}")
    print(f"    costs: {costs}")
    print(f"\n    Spearman(v2, ordinal cost) over 19: {rho} "
          f"(references: 0.73 raw / 0.81 v2, walk-taxed)")

    class_means = {}
    for cls, members in CLASSES.items():
        cm = round(float(np.mean([v2[n] for n in members])), 3)
        cc = round(float(np.mean([costs[n] for n in members])), 1)
        class_means[cls] = {"v2_mean": cm, "cost_mean": cc,
                            "members": members}
        print(f"    {cls:9s} v2_mean {cm:7.3f}  cost_mean {cc:5.1f}")

    order = sorted(CLASSES, key=lambda c: class_means[c]["cost_mean"])
    v2_seq = [class_means[c]["v2_mean"] for c in order]
    or_g2 = all(v2_seq[i] <= v2_seq[i + 1] + 1e-9
                for i in range(len(v2_seq) - 1))

    or_g1 = rho >= 0.60
    pair_min = min(v2["bipartite"], v2["complete"])
    worse = [n for n in names if v2[n] < pair_min
             and costs[n] >= costs["bipartite"]]
    or_g3 = not worse

    print(f"\n  class order by cost: {order}")
    print(f"  OR-G1 oracle survives (rho {rho} >= 0.60): "
          f"{'PASS' if or_g1 else 'REFUTED'}")
    print(f"  OR-G2 class-mean monotonicity: "
          f"{'PASS' if or_g2 else 'REFUTED'}")
    print(f"  OR-G3 geometry pair dominates (violations {worse}): "
          f"{'PASS' if or_g3 else 'REFUTED'}")

    npass = sum([or_g1, or_g2, or_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp114_corrected_oracle",
        "spearman_class_ordinal": rho,
        "references": {"exp102_raw_class": 0.73,
                       "exp106_v2": 0.811},
        "class_means": class_means,
        "criteria": {
            "OR_G1_oracle_survives": bool(or_g1),
            "OR_G2_class_monotonicity": bool(or_g2),
            "OR_G3_pair_dominates": bool(or_g3),
        },
        "notes": (
            "The v2 oracle re-tested under its own class-ordinal "
            "instrument on the walk-tax-free re-priced map (19 "
            "members, lexicographic gamma/mu ladder costs). The "
            "geometry pair's domination is the semantic check."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
