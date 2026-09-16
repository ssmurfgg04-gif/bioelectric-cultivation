#!/usr/bin/env python3
"""exp95 — THE STAR-BOUNDARY PRICING (ledger L77; exp94's named
boundary — the deg-99 hub — tested as an operating-point statement).

THE PREDICTION (registered before the run): exp94's only refusal is
the star graph (1 hub + 99 spokes; multi-program error 8.53 mV at
the star point (gamma=64, mu=0)). The two-channel law explains it:
during the settle the hub's g_total ~ 99*g makes it a V-SINK — the
rebuilt spokes' V relaxes toward the hub — and the ratio
g_cut/(gamma + g_total) SHRINKS as gamma rises. So:
  (a) LOWER gamma should DECUPLE the hub's grip (the ratio closer
      to 1) — the spokes hold their canon memory;
  (b) the MU dial must be at 0 regardless — at mu=0.015 the theta
      homogenization through the deg-99 hub is mu*deg = huge
      (exp78's hub arithmetic), the identity layer washes out.
The star's price is therefore predicted TWO-DIAL — class III of
exp93 — and the boundary is PRICED, not absolute (R5' again).

PRE-REGISTERED GATES:

  SB-G1  (the boundary is priced) exists an operating point at
         which the star's multi program verifies (>= 2/3 seeds).
         Registered candidates: gamma in {1, 4} at mu=0.
  SB-G2  (the channel attribution) the two-dial structure: gamma
         alone at default mu FAILS at every gamma <= 64 (the theta
         channel through the hub), and at least one (gamma, 0) cell
         verifies — the hub refusal is joint debt, exp93's class
         III extended to the deg->n limit.
  SB-G3  (the ratio law) at mu=0 the multi-program error is
         MONOTONE in gamma (Spearman >= +0.8: higher gamma -> worse
         — the hub-sink signature), the direction OPPOSITE to the
         exp73-79 arc where higher gamma bought writability on the
         hub substrates. The reversal IS the diagnosis: at the
         deg->n limit the V-ratio law flips the gamma dial's sign.

RUN: the star substrate x the operating grid {gamma} x {mu} x 3
seeds with exp94's multi program (the two-source read). Serial,
BLAS pinned.
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
    execute_two_source_n, MULTI, star_adj,
)
from experiments.exp91_dose_axis_wiring import spearman

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp95_star_boundary.json")

SEEDS = (1, 2, 3)
GAMMA_GRID = [1.0, 4.0, 16.0, 64.0]
MU_GRID = [0.015, 0.0]


def main() -> dict:
    print("=== exp95: the star-boundary pricing ===\n")

    adj = star_adj(100)
    grid: dict[str, dict] = {}
    for mu in MU_GRID:
        for g in GAMMA_GRID:
            res = [execute_two_source_n(MULTI, adj, s,
                                        op={"gamma": g, "mu": mu})
                   for s in SEEDS]
            # execute_two_source_n reads the STAR op internally in
            # exp94; here the op is passed explicitly (the generalized
            # executor honours op — see the op kwarg below).
            grid[f"g{int(g)}_mu{int(mu * 1000)}"] = {
                "rate": round(float(np.mean(
                    [r["program_verified"] for r in res])), 3),
                "err": round(float(np.mean(
                    [r["err_vs_target"] for r in res])), 2),
            }
            print(f"    gamma={g:6.1f} mu={mu:.3f}: "
                  f"rate {grid[f'g{int(g)}_mu{int(mu*1000)}']['rate']:.2f} "
                  f"err {grid[f'g{int(g)}_mu{int(mu*1000)}']['err']}")

    verify_cells = [k for k, v in grid.items() if v["rate"] >= 2 / 3]
    sb_g1 = bool(verify_cells)
    print(f"\n  SB-G1 boundary priced: verify cells {verify_cells} -> "
          f"{'PASS' if sb_g1 else 'REFUTED'}")

    mu_default_fail = all(grid[f"g{int(g)}_mu15"]["rate"] <= 1 / 3
                          for g in GAMMA_GRID)
    mu0_some = any(grid[f"g{int(g)}_mu0"]["rate"] >= 2 / 3
                   for g in GAMMA_GRID)
    sb_g2 = bool(mu_default_fail and mu0_some)
    print(f"  SB-G2 two-dial: mu=0.015 fails at all gamma "
          f"({mu_default_fail}); some (gamma, 0) verifies "
          f"({mu0_some}) -> {'PASS' if sb_g2 else 'REFUTED'}")

    errs_mu0 = [grid[f"g{int(g)}_mu0"]["err"] for g in GAMMA_GRID]
    rho = spearman(GAMMA_GRID, errs_mu0)
    sb_g3 = bool(rho is not None and rho >= 0.8)
    print(f"  SB-G3 ratio-law reversal: errs at mu=0 {errs_mu0}, "
          f"Spearman {'undefined' if rho is None else round(rho, 3)} "
          f"-> {'PASS' if sb_g3 else 'REFUTED'}")

    npass = sum([sb_g1, sb_g2, sb_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    out = {
        "exp": "exp95_star_boundary",
        "grid": grid,
        "verify_cells": verify_cells,
        "criteria": {
            "SB_G1_boundary_priced": sb_g1,
            "SB_G2_two_dial_attribution": sb_g2,
            "SB_G3_ratio_law_reversal": sb_g3,
        },
        "notes": (
            "The deg-99 hub boundary tested as an operating-point "
            "statement: the V-ratio law predicts the gamma dial's "
            "SIGN FLIPS at the deg->n limit (the hub sink grows with "
            "gamma) — the reversal of the exp73-79 arc. The mu dial "
            "must be at zero (the theta homogenization through the "
            "hub is mu*deg). exp94's multi program; 3 seeds."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
