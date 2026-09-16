#!/usr/bin/env python3
"""exp102 — R5 RECALIBRATED: FROM BOOLEAN GATE TO PRICE ORACLE
(ledger L84; exp101's registered audit — the chain-era partition
boolean is refused by its own executor; the boundary-to-volume
RATIO it measures may still be the right number, read as a PRICE).

THE CLAIM UNDER TEST: the partition's boundary-to-volume ratio
(crossing edges / total edges) predicts the READER's dial cost —
how far up the (gamma, mu) plane a substrate's minimal verifying
cell sits — instead of a boolean compilable/refuse.

COST SCALES (from exp100's deposited map):
  ordinal    DEFAULT=0, V_PRICED=1, TWO_DIAL=2;
  sub-order  within V_PRICED: gamma_min; within TWO_DIAL: the
             bracket ((4,0) < (16,0) < (32,0)) as 2.0/2.33/2.67.

PRE-REGISTERED GATES:

  RO-G1  (the boolean is dead) the check's boolean verdict at the
         default R5_MAX contradicts the executor's mapped-cell
         verdict (verified, all 19 by exp100's construction) on
         >= 8 of the 19 substrates.
  RO-G2  (the oracle rises) Spearman(ratio, ordinal cost) >= 0.6
         across the 19 substrates. The star's deviation is
         pre-declared: its unzoned hub inflates the ratio (every
         zone-spoke edge crosses) while its post-repair price is
         the cheapest — deposited as the named outlier either way.
  RO-G3  (the oracle resolves) (a) the class-mean ratios are
         monotone DEFAULT < V_PRICED < TWO_DIAL; (b) within
         TWO_DIAL the bracket means are monotone (4,0) < (16,0) <
         (32,0).
  RO-G4  (the oracle is degree-flat on stars) the ratio is
         constant (std < 0.01) across the exp99 degree ladder
         {49, 74, 99, 149, 199} — matching exp99's degree-invariant
         map (the zone fractions scale; every measured edge
         structure is self-similar).

RUN: analytic — no sim runs. Ratios computed from the adjacency
structures; costs parsed from results/exp100_reader_price_map.json.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")

from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import (
    MULTI, new_battery, star_adj,
)
from experiments.exp99_degree_ladder import DEGREES
from cultivation.compiler.anatomy import substrate_partition_check
from cultivation.validation.stats import spearman_ties

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp102_r5_price_oracle.json")

BRACKET_COST = {(4.0, 0.0): 2.0, (16.0, 0.0): 2.33, (32.0, 0.0): 2.67}


def main() -> dict:
    print("=== exp102: R5 recalibrated — the price oracle ===\n")

    battery = dict(make_battery())
    battery.update(new_battery())

    with open(os.path.join(ROOT, "results",
                           "exp100_reader_price_map.json")) as f:
        pmap = json.load(f)

    rows = {}
    for name, adj in battery.items():
        chk = substrate_partition_check(MULTI, adj)
        cls = pmap["classes"][name]
        call = cls["call"]
        if call == "DEFAULT":
            cost, sub = 0.0, 0.0
        elif call == "V_PRICED":
            cost, sub = 1.0, float(cls["gamma_min"])
        else:
            cost = 2.0
            sub = BRACKET_COST[tuple(cls["cheapest"])]
        rows[name] = {
            "ratio": chk["boundary_to_volume"],
            "boolean": chk["substrate_compilable"],
            "class": call,
            "ordinal_cost": cost,
            "sub_cost": sub,
        }
        print(f"    {name:14s} ratio {chk['boundary_to_volume']:.3f}"
              f"  bool {int(chk['substrate_compilable'])}"
              f"  {call:9s} cost {cost} (sub {sub})")

    ratios = np.array([rows[n]["ratio"] for n in rows])
    costs = np.array([rows[n]["ordinal_cost"] for n in rows])
    bools = [rows[n]["boolean"] for n in rows]

    ro_g1 = sum(1 for b in bools if not b) >= 8

    rho = float(spearman_ties(ratios, costs))
    ro_g2 = rho >= 0.6

    groups = {c: [rows[n]["ratio"] for n in rows
                  if rows[n]["class"] == c]
              for c in ("DEFAULT", "V_PRICED", "TWO_DIAL")}
    means = {c: float(np.mean(v)) for c, v in groups.items() if v}
    g3a = (means["DEFAULT"] < means["V_PRICED"] < means["TWO_DIAL"])

    td = [(rows[n]["sub_cost"], rows[n]["ratio"]) for n in rows
          if rows[n]["class"] == "TWO_DIAL"]
    brackets = sorted({sc for sc, _ in td})
    bmeans = {sc: float(np.mean([r for sc2, r in td if sc2 == sc]))
              for sc in brackets}
    g3b = all(bmeans[brackets[i]] < bmeans[brackets[i + 1]]
              for i in range(len(brackets) - 1))
    ro_g3 = g3a and g3b

    star_ratios = []
    for d in DEGREES:
        chk = substrate_partition_check(MULTI, star_adj(d + 1))
        star_ratios.append(chk["boundary_to_volume"])
    star_std = float(np.std(star_ratios))
    ro_g4 = star_std < 0.01

    print(f"\n  class-mean ratios: "
          f"{ {c: round(m, 3) for c, m in means.items()} }")
    print(f"  two-dial bracket means: "
          f"{ {b: round(m, 3) for b, m in bmeans.items()} }")
    print(f"  star-family ratios: "
          f"{[round(r, 3) for r in star_ratios]} (std {star_std:.4f})")
    print(f"\n  RO-G1 the boolean is dead: "
          f"{'PASS' if ro_g1 else 'REFUTED'} "
          f"({sum(1 for b in bools if not b)}/19 refused)")
    print(f"  RO-G2 the oracle rises (rho): "
          f"{'PASS' if ro_g2 else 'REFUTED'} (rho = {rho:.2f})")
    print(f"  RO-G3 the oracle resolves: "
          f"{'PASS' if ro_g3 else 'REFUTED'}")
    print(f"  RO-G4 degree-flat on stars: "
          f"{'PASS' if ro_g4 else 'REFUTED'}")

    npass = sum([ro_g1, ro_g2, ro_g3, ro_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp102_r5_price_oracle",
        "rows": rows,
        "stats": {
            "spearman_ratio_ordinal_cost": round(rho, 3),
            "class_mean_ratios": {c: round(m, 4)
                                  for c, m in means.items()},
            "bracket_mean_ratios": {str(b): round(m, 4)
                                    for b, m in bmeans.items()},
            "star_family_ratios": [round(r, 4) for r in star_ratios],
            "star_family_std": round(star_std, 4),
        },
        "criteria": {
            "RO_G1_boolean_dead": bool(ro_g1),
            "RO_G2_oracle_rises": bool(ro_g2),
            "RO_G3_oracle_resolves": bool(ro_g3),
            "RO_G4_degree_flat_stars": bool(ro_g4),
        },
        "notes": (
            "The chain-era R5 boolean refused 10/12 executor-"
            "verified (substrate, k) pairs (exp101). This audit "
            "tests the ratio as a PRICE ORACLE for the reader's "
            "dial cost across the 19-substrate battery (exp100's "
            "deposited map). Analytic — no sim runs."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
