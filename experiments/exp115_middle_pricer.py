#!/usr/bin/env python3
"""exp115 — WHAT PRICES THE MIDDLE (ledger L95's registration: the
v2 oracle prices the ENDS — the cheap band and the geometry pair —
and the middle band's cells are set by the mu channel and walk
speed instead. Two questions: is the middle's mu price shallow,
and does ANY deposited quantity price the middle?).

PART A — THE MU LADDER AT BOTH WALK SPEEDS (new runs): the six MU0
members (torus, torus_elong, random3, random8, scale_free,
scale_free200 — all verify at (1, 0) under spc=0) run the mu rungs
{0.01, 0} at BOTH spc=0 and spc=8, 3 seeds:
  (1, 0.01) @ spc=0 — is the full mu cut load-bearing, or does the
            first mu rung already buy the middle?
  (1, 0.01) @ spc=8 — is the mu requirement itself
            walk-speed-dependent (the exp110 mechanism acting on
            the mu channel: the slow walk's wound-field exposure
            needs the theta diffusion off to hold identity)?

PART B — MIDDLE-BAND PREDICTORS (assembly): for the 13 middle
members (19 minus 5 DEFAULT0 minus 2 GEOMETRY), Spearman against
the exp114 ordinal costs for three deposited quantities:
  mean degree, spectral gap lambda_2 (algebraic connectivity), and
  the v2 ratio (known disordered — the reference).

PRE-REGISTERED GATES:

  MB-G1  (the mu price is shallow) >= 4/6 MU0 members verify
         (rate >= 2/3) at (1, 0.01) under spc=0 — the first mu
         rung buys most of the middle; below 4/6 the full cut is
         load-bearing and the middle is mu-deep.
  MB-G2  (the mu price is walk-speed-dependent) for >= 4/6 MU0
         members, (1, 0.01) verifies at spc=0 while (1, 0.01) at
         spc=8 REFUSES (rate < 2/3) — the mu channel's price
         collapses when the walk is fast (the two dials interact
         through the rebuild).
  MB-G3  (a middle predictor exists) the best of {mean degree,
         lambda_2, v2} reaches Spearman >= 0.5 against the middle
         ordinal costs; if none does, the middle is genuinely
         multi-channel and the map deposits that honestly.

RUN: 6 members x 2 mu rungs x 2 speeds x 3 seeds = 72 runs +
assembly. Serial, BLAS pinned.
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

from experiments.exp112_walk_speed_ladder import build_battery, cell_stats
from experiments.exp114_corrected_oracle import CELLS, ordinal_cost

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp115_middle_pricer.json")

MU0_MEMBERS = ("torus", "torus_elong", "random3", "random8",
               "scale_free", "scale_free200")
MIDAll = ["torus", "torus_elong", "random3", "random8", "scale_free",
          "scale_free200", "barbell", "ladder", "random6", "tree",
          "grid2d", "grid_elong"]


def main() -> dict:
    print("=== exp115: what prices the middle ===\n")

    battery = build_battery()
    out: dict = {"mu_ladder": {}, "predictors": {}}

    # PART A
    for name in MU0_MEMBERS:
        adj = battery[name]
        for mu in (0.01, 0.0):
            for spc in (0, 8):
                st = cell_stats(adj, 1.0, mu, spc)
                key = f"{name}_mu{mu:g}_spc{spc}"
                out["mu_ladder"][key] = st
                print(f"    {name:13s} (1, {mu:g}) spc={spc}  "
                      f"{st['rate']:.2f}/{st['err']:5.2f}")

    mu01_spc0 = [out["mu_ladder"][f"{n}_mu0.01_spc0"]["rate"] >= 2 / 3
                 for n in MU0_MEMBERS]
    mb_g1 = sum(mu01_spc0) >= 4
    mb_g2 = sum(
        out["mu_ladder"][f"{n}_mu0.01_spc0"]["rate"] >= 2 / 3
        and out["mu_ladder"][f"{n}_mu0.01_spc8"]["rate"] < 2 / 3
        for n in MU0_MEMBERS) >= 4

    # PART B
    exp113 = json.load(open(os.path.join(
        ROOT, "results", "exp113_repriced_map.json")))
    costs = {n: ordinal_cost(CELLS[n]) for n in MIDAll}
    deg = {n: round(float(battery[n].sum(axis=1).mean()), 3)
           for n in MIDAll}
    lam2 = {}
    for n in MIDAll:
        A = battery[n]
        L = np.diag(A.sum(axis=1)) - A
        lam2[n] = round(float(np.linalg.eigvalsh(L)[1]), 4)
    v2 = {n: exp113["map_spc0"][n]["v2"] for n in MIDAll
          if exp113["map_spc0"][n].get("v2") is not None}
    # barbell's v2 was in exp114's map? (barbell in map_spc0 with
    # v2) — fill any missing from exp114's arms via recompute
    from experiments.exp106_drift_and_oracle_v2 import v2_ratio
    for n in MIDAll:
        if n not in v2 or v2[n] is None:
            v2[n] = round(float(v2_ratio(battery[n])), 4)

    names = list(costs)
    rhos = {
        "mean_degree": round(float(spearmanr(
            [deg[n] for n in names],
            [costs[n] for n in names]).statistic), 3),
        "lambda2": round(float(spearmanr(
            [lam2[n] for n in names],
            [costs[n] for n in names]).statistic), 3),
        "v2": round(float(spearmanr(
            [v2[n] for n in names],
            [costs[n] for n in names]).statistic), 3),
    }
    out["predictors"] = {"rhos": rhos, "mean_degree": deg,
                         "lambda2": lam2, "v2": v2, "costs": costs}
    best = max(rhos, key=rhos.get)
    mb_g3 = rhos[best] >= 0.5

    print(f"\n  mu ladder: (1, 0.01) @ spc0 verifies "
          f"{sum(mu01_spc0)}/6")
    print(f"  predictors vs middle cost: {rhos} (best {best})")
    print(f"\n  MB-G1 mu price shallow (>= 4/6): "
          f"{'PASS' if mb_g1 else 'REFUTED'}")
    print(f"  MB-G2 mu price walk-speed-dependent (>= 4/6): "
          f"{'PASS' if mb_g2 else 'REFUTED'}")
    print(f"  MB-G3 middle predictor exists ({best} "
          f"{rhos[best]} >= 0.5): {'PASS' if mb_g3 else 'REFUTED'}")

    npass = sum([mb_g1, mb_g2, mb_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp115_middle_pricer",
        "arms": out,
        "criteria": {
            "MB_G1_mu_price_shallow": bool(mb_g1),
            "MB_G2_mu_price_speed_dependent": bool(mb_g2),
            "MB_G3_middle_predictor": {"best": best,
                                       "rho": rhos[best],
                                       "pass": bool(mb_g3)},
        },
        "notes": (
            "The middle band's pricer: the mu ladder at both walk "
            "speeds on the six MU0 members (shallow? "
            "speed-dependent?) and three candidate predictors "
            "(mean degree, lambda_2, v2) against the ordinal "
            "middle costs."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
