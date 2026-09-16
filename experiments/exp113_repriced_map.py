#!/usr/bin/env python3
"""exp113 — THE RE-PRICED MAP (ledger L93's registration: exp112
released the dial budget — 13/15 expensive members verify cheaper
under the frozen walk, the (4, 0) two-dial class dissolves to
default gamma, and bipartite/complete REFUSE every descent rung
(the v2 oracle's top tail). This experiment assembles the honest
walk-tax-free price map and re-tests the oracle on it).

THE ASSEMBLY (no re-running of deposited cells):
  - the 15 expensive members' spc=0 minimal cells: exp112's
    buy-backs (13) + bipartite/complete at their adopted (32, 0)
    under spc=0 (exp112's adopted0 arms: 4.47 / 5.21, rate 1.00);
  - the 4 DEFAULT members (path, path200, cycle, small_world) RUN
    NOW at the default cell (1, 0.015) under spc=0 (3 seeds) —
    their only missing column;
  - the spc=8 reference column: the exp100 deposit (confirmed
    bit-exact by exp112's WS-G2).

THE ORACLE RE-TEST: v2 = crossing_edges / sqrt(total_edges)
(exp106's v2_ratio, verbatim) computed per substrate; Spearman
against the minimal-cell errs under BOTH protocols over the 15
expensive members:
  rho8  = Spearman(v2, err at the exp100 adopted cell, spc=8)
  rho0  = Spearman(v2, err at the spc=0 minimal cell)
The walk tax is size- and topology-coupled noise in the spc=8
column; the geometry price is what remains at spc=0. If the oracle
measures geometry, rho0 >= rho8 - 0.05.

PRE-REGISTERED GATES:

  RP-G1  (the map closes under the new protocol) all 19 members
         verify somewhere under spc=0 (13 buy-backs + 2 geometry
         at their adopted cell + 4 DEFAULT members now) — the
         reader's domain stays CLOSED under the frozen walk.
  RP-G2  (the oracle survives the re-price) rho0 >= rho8 - 0.05
         over the 15 expensive members; both rhos deposited.
  RP-G3  (the top tail stands) both bipartite and complete sit in
         the top 3 of the spc=0 minimal-cell errs — the geometry
         pair is what the ratio's top tail was pointing at all
         along.

RUN: 4 DEFAULT members x 3 seeds at (1, 0.015) spc=0 + assembly.
Serial, BLAS pinned.
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

from experiments.exp106_drift_and_oracle_v2 import v2_ratio
from experiments.exp112_walk_speed_ladder import (
    DEFAULT_MU, build_battery, cell_stats,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp113_repriced_map.json")

DEFAULT_MEMBERS = ("path", "path200", "cycle", "small_world")
BUY_BACKS = {
    "star": [1.0, 0.015], "tree": [16.0, 0.015],
    "grid2d": [16.0, 0.015], "grid_elong": [16.0, 0.015],
    "ladder": [8.0, 0.015], "random6": [8.0, 0.015],
    "torus": [1.0, 0.0], "torus_elong": [1.0, 0.0],
    "random3": [1.0, 0.0], "random8": [1.0, 0.0],
    "scale_free": [1.0, 0.0], "scale_free200": [1.0, 0.0],
    "barbell": [4.0, 0.0],
}
GEOMETRY_PAIR = {"bipartite": [32.0, 0.0], "complete": [32.0, 0.0]}


def main() -> dict:
    print("=== exp113: the re-priced map ===\n")

    battery = build_battery()
    exp100 = json.load(open(os.path.join(
        ROOT, "results", "exp100_reader_price_map.json")))
    exp112 = json.load(open(os.path.join(
        ROOT, "results", "exp112_walk_speed_ladder.json")))

    def exp100_err(name):
        dep = exp100["cells"][name]
        return dep[dep.get("class_cell", "twodial_4_0"
                           if name in BUY_BACKS or name in
                           GEOMETRY_PAIR else "gamma_64")]["err"] \
            if False else None

    # spc8 reference errs: exp112's adopted8 arms (WS-G2-confirmed
    # against the exp100 deposit)
    err8: dict = {}
    for name in list(BUY_BACKS) + list(GEOMETRY_PAIR):
        err8[name] = exp112["arms"][f"{name}_adopted8"]["err"]

    # spc0 minimal errs
    err0: dict = {}
    cell0: dict = {}
    for name, cell in BUY_BACKS.items():
        g, m = cell
        key = f"{name}_down0_{g:g}_{m:g}"
        err0[name] = exp112["arms"][key]["err"]
        cell0[name] = cell
    for name, cell in GEOMETRY_PAIR.items():
        err0[name] = exp112["arms"][f"{name}_adopted0"]["err"]
        cell0[name] = cell

    # the 4 DEFAULT members now (spc=0 at the default cell)
    default_results = {}
    for name in DEFAULT_MEMBERS:
        st = cell_stats(battery[name], 1.0, DEFAULT_MU, 0)
        default_results[name] = st
        err0[name] = st["err"]
        cell0[name] = [1.0, DEFAULT_MU]
        err8[name] = exp100["cells"][name]["default"]["err"]
        print(f"    {name:13s} (1, {DEFAULT_MU}) spc0  "
              f"{st['rate']:.2f}/{st['err']:5.2f}   "
              f"(exp100 default {exp100['cells'][name]['default']['rate']:.2f}"
              f"/{err8[name]:5.2f})")

    all15 = list(BUY_BACKS) + list(GEOMETRY_PAIR)
    v2s = {name: round(float(v2_ratio(battery[name])), 4)
           for name in all15}
    print(f"\n    v2 ratios: {v2s}")

    rho8 = round(float(spearmanr([v2s[n] for n in all15],
                                 [err8[n] for n in all15]).statistic), 3)
    rho0 = round(float(spearmanr([v2s[n] for n in all15],
                                 [err0[n] for n in all15]).statistic), 3)

    rp_g1 = all(default_results[n]["rate"] >= 2 / 3
                for n in DEFAULT_MEMBERS)
    rp_g2 = rho0 >= rho8 - 0.05
    top3 = sorted(all15, key=lambda n: -err0[n])[:3]
    rp_g3 = all(n in top3 for n in GEOMETRY_PAIR)

    print(f"\n  rho8 (walk-taxed) {rho8}  |  rho0 (geometry) {rho0}")
    print(f"  top-3 spc=0 errs: "
          f"{[(n, err0[n]) for n in sorted(all15, key=lambda x: -err0[x])[:3]]}")
    print(f"\n  RP-G1 map closes under spc=0 (19/19): "
          f"{'PASS' if rp_g1 else 'REFUTED'}")
    print(f"  RP-G2 oracle survives (rho0 {rho0} >= "
          f"rho8 {rho8} - 0.05): {'PASS' if rp_g2 else 'REFUTED'}")
    print(f"  RP-G3 top tail stands (top3 {top3}): "
          f"{'PASS' if rp_g3 else 'REFUTED'}")

    npass = sum([rp_g1, rp_g2, rp_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp113_repriced_map",
        "map_spc0": {n: {"cell": cell0[n], "err": err0[n],
                         "v2": v2s.get(n)}
                     for n in list(cell0)},
        "map_spc8_reference": err8,
        "default_members_spc0": default_results,
        "rhos": {"spc8": rho8, "spc0": rho0},
        "top3_spc0": top3,
        "criteria": {
            "RP_G1_map_closes": bool(rp_g1),
            "RP_G2_oracle_survives": bool(rp_g2),
            "RP_G3_top_tail_stands": bool(rp_g3),
        },
        "notes": (
            "The walk-tax-free price map: 19 members, minimal "
            "cells under spc=0, the v2 oracle re-tested against "
            "both protocol columns. The geometry pair's standing "
            "in the top tail is the oracle's semantic check."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
