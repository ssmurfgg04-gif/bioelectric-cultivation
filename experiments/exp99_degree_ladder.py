#!/usr/bin/env python3
"""exp99 — THE DEGREE LADDER (ledger L81; exp98's registered map:
the price-vs-degree boundary — beyond deg-99, does the hub's
one-dial price RISE with degree, and is there a degree where one
dial stops buying?).

THE FAMILY: stars with n in {50, 75, 100, 150, 200} (degree n-1 in
{49, 74, 99, 149, 199}; n >= 50 keeps the 3-zone fraction layout
non-degenerate — the hub stays outside every zone). The cells (the
exp97/98 map's load-bearing columns):
  * the DEFAULT (1, 0.015) — the marginal refusal at deg 99;
  * the ONE-DIAL tags (2, 0.015) and (1, 0.01);
  * the TWO-DIAL (4, 0) and the MAX-FORCING anchor (64, 0).

THE REGISTERED PREDICTION (flat): the per-spoke coupling rates are
degree-INDEPENDENT (each spoke feels the hub at g=0.2 on the V
channel and mu on the theta channel, one edge either way); the hub
integrates faster with degree but nothing on the spoke side speeds
up. So the default sag and the one-dial tags should be FLAT in
degree — R5' closes degree-invariant. A rising map (the tag dying
at some degree) would be the FIRST real boundary, with its degree
and the (64, 0) probe bracketing it.

PRE-REGISTERED GATES:

  DL-G1  (the map's shape) the default-cell err is FLAT in degree
         (|Spearman| < 0.6 across the 5 degrees) — the flat
         prediction; a positive rho >= 0.6 deposits the rising map
         instead (informative either way, the rule pre-set).
  DL-G2  (one-dial survival) BOTH one-dial cells verify >= 2/3 at
         EVERY degree — the tag is degree-invariant.
  DL-G3  (no boundary through 199) at deg 199 at least one of the
         four non-default cells verifies >= 2/3.
  DL-G4  (the anchor) (64, 0) verifies >= 2/3 at EVERY degree with
         mean err < 2.0 (exp97's 1.02 at deg 99 anchors mid-ladder).

RUN: 5 degrees x 5 cells x 3 seeds = 75 runs. Serial, BLAS pinned.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp99_degree_ladder.json")

SEEDS = (1, 2, 3)
DEGREES = (49, 74, 99, 149, 199)   # n = degree + 1
CELLS = {
    "default_1_0.015": {"gamma": 1.0, "mu": 0.015},
    "onedial_gamma2": {"gamma": 2.0, "mu": 0.015},
    "onedial_mu0.01": {"gamma": 1.0, "mu": 0.01},
    "twodial_4_0": {"gamma": 4.0, "mu": 0.0},
    "anchor_64_0": {"gamma": 64.0, "mu": 0.0},
}


def cell(adj, op):
    res = [execute_two_source_n(MULTI, adj, s, op=op,
                                frontier_mode="walk")
           for s in SEEDS]
    return {"rate": round(float(np.mean(
        [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)}


def main() -> dict:
    print("=== exp99: the degree ladder ===\n")

    out: dict[str, dict] = {}
    for d in DEGREES:
        adj = star_adj(d + 1)
        for cname, op in CELLS.items():
            key = f"deg{d}_{cname}"
            out[key] = cell(adj, op)
            print(f"    {key:26s} rate {out[key]['rate']:.2f} "
                  f"err {out[key]['err']}")

    degs = np.array(DEGREES, dtype=float)
    default_errs = np.array(
        [out[f"deg{d}_default_1_0.015"]["err"] for d in DEGREES])
    from cultivation.validation.stats import spearman_ties
    rho = spearman_ties(degs, default_errs)
    dl_g1 = abs(rho) < 0.6
    dl_g2 = all(out[f"deg{d}_{c}"]["rate"] >= 2 / 3
                for d in DEGREES
                for c in ("onedial_gamma2", "onedial_mu0.01"))
    dl_g3 = any(out[f"deg199_{c}"]["rate"] >= 2 / 3
                for c in ("onedial_gamma2", "onedial_mu0.01",
                          "twodial_4_0", "anchor_64_0"))
    anchor_errs = [out[f"deg{d}_anchor_64_0"]["err"] for d in DEGREES]
    dl_g4 = (all(out[f"deg{d}_anchor_64_0"]["rate"] >= 2 / 3
                 for d in DEGREES)
             and max(anchor_errs) < 2.0)

    print(f"\n  default errs vs degree: "
          f"{dict(zip([int(d) for d in DEGREES], default_errs))}")
    print(f"  Spearman(degree, default err) = {rho:.2f}")
    print(f"  anchor (64,0) errs: {dict(zip([int(d) for d in DEGREES], anchor_errs))}")
    print(f"\n  DL-G1 flat map (|rho| < 0.6): "
          f"{'PASS' if dl_g1 else 'REFUTED (rising map deposited)'}")
    print(f"  DL-G2 one-dial survival: {'PASS' if dl_g2 else 'REFUTED'}")
    print(f"  DL-G3 no boundary through 199: "
          f"{'PASS' if dl_g3 else 'REFUTED'}")
    print(f"  DL-G4 the anchor holds: {'PASS' if dl_g4 else 'REFUTED'}")

    npass = sum([dl_g1, dl_g2, dl_g3, dl_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp99_degree_ladder",
        "arms": out,
        "map": {
            "default_errs": dict(zip([int(d) for d in DEGREES],
                                     default_errs.tolist())),
            "spearman_degree_default_err": round(float(rho), 3),
            "anchor_errs": dict(zip([int(d) for d in DEGREES],
                                    anchor_errs)),
        },
        "criteria": {
            "DL_G1_flat_map": bool(dl_g1),
            "DL_G2_one_dial_survival": bool(dl_g2),
            "DL_G3_no_boundary_through_199": bool(dl_g3),
            "DL_G4_anchor_holds": bool(dl_g4),
        },
        "notes": (
            "The price-vs-degree map: 5 star degrees x 5 operating "
            "cells under the repaired executor. The registered "
            "prediction is FLAT (per-spoke coupling rates are "
            "degree-independent; the hub's faster integration does "
            "not propagate to the spoke side). A rising map would "
            "be the first real reader boundary, degree deposited."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
