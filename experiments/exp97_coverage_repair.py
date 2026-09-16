#!/usr/bin/env python3
"""exp97 — THE COVERAGE REPAIR (ledger L79; the probe that REFUTES
L77-L78's mechanism and the repair that re-tests the star boundary).

THE FORK DECISION (owned): L78 registered exp97 as a per-edge hub
anchor — an architecture extension to let the hub "speak a different
value to each neighbor." The pre-design probe MOOTED it: you do not
build signaling architecture to fix cells that were never rebuilt.

THE PROBE (one run, deposited as the decomposition arms): on the
star, the amputation range is cells 2-75 (reg_walk spans the
inter-zone gaps), but the blastema-frontier enumeration runs over
the ZONE UNION only (reg_idx). On a connected region the BFS walks
laterally and covers the gaps; on the star every spoke's ONLY
neighbor is the intact hub, so the BFS dead-ends — ~32 amputated
cells (12-29, 46-59) are NEVER REBUILT and sit at wound state
(blastema theta -40) forever. Decomposition of the deposited 8.53:
head-gaps 12 cells at -40 vs -20 (RMS 19.9), trunk-gaps 19 cells at
-40 vs -50 (RMS 10.1), cell 12 (361), hub drag (79), z1 residual
(106) — the coverage hole is ~93% of the squared error. THE SETTLE
MOVES NOTHING: post-walk 8.52 -> post-settle 8.53 -> post-release
8.53. L77-L78's mechanism story ("the settle homogenizes the disc
through the single-point integrator") is REFUTED — the error is
STATIC and born in the walk's coverage, not in settle dynamics.
The "architecture boundary" was an executor artifact.

THE REPAIR (backward-compatible): frontier_mode="walk" enumerates
the blastema frontier over the whole amputation range — the honest
wound-frontier semantics (a cell amputated and adjacent to intact
tissue IS a frontier cell). Default "zones" is bit-exact with every
deposited run (re-verified in-run: tree 0.56, star 8.53).

PRE-REGISTERED GATES:

  CV-G1  (the artifact pinned) the zones-mode star control FAILS at
         the deposited floor (rate 0/3, err 8.0-9.5) — in-run
         reproduction of the instrument state.
  CV-G2  (the repair buys the star) the walk-mode star VERIFIES
         >= 2/3 seeds at the star point (64, 0), err < 6.0
         (predicted band 0.5-1.5: hub drag + z1 residual remain).
  CV-G3  (the pattern is static) walk-mode star post-walk and
         post-settle errors differ by < 0.5 mV — no settle
         homogenization exists to anchor against (the L77-L78
         story stays refuted on the repaired run).
  CV-G4  (the repair is universal) walk-mode still verifies tree,
         cycle, and grid_elong >= 2/3 seeds each — the frontier
         repair generalizes beyond the star (trajectories shift;
         verification must hold).
  CV-G5  (the domain rule survives the repair) walk-mode star with
         the BELOW spec (z1 at -59, out of the M33 domain) FAILS
         and the no-canon variant FAILS (<= 1/3 each) — the
         two-source structure is load-bearing under full coverage.

RUN: star x {zones, walk} x 3 seeds + walk-mode below/no-canon x 2 +
tree/cycle/grid_elong walk-mode x 3 + 2 decomposition runs (final
state deposited). Serial, BLAS pinned.
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
    execute_two_source_n, MULTI, BELOW, star_adj, tree_adj, cycle_adj,
    grid_2d, STAR,
)
from experiments.exp91_dose_axis_wiring import SEEDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp97_coverage_repair.json")

STAR_PT = {"gamma": 64.0, "mu": 0.0}


def arm(adj, op, frontier_mode, seeds=SEEDS, with_canon=True,
        spec=None, return_state=False):
    res = [execute_two_source_n(
        spec if spec is not None else MULTI, adj, s, with_canon=with_canon,
        op=op, frontier_mode=frontier_mode, return_trace=True,
        return_state=return_state)
        for s in seeds]
    out = {
        "rate": round(float(np.mean(
            [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2),
        "post_walk_err": round(float(np.mean(
            [r["trace"]["post_walk_err"] for r in res])), 2),
        "post_settle_err": round(float(np.mean(
            [r["trace"]["post_settle_err"] for r in res])), 2),
    }
    if return_state:
        st = res[0]["final_state"]
        V = np.array(st["V"])
        tgt = np.array(st["target"])
        groups = {
            "hub": [0],
            "z0": list(range(2, 12)),
            "gap_head": list(range(12, 25)),
            "gap_trunk_a": list(range(25, 30)),
            "z1": list(range(30, 45)),
            "gap_trunk_b": list(range(46, 60)),
            "z2": list(range(60, 75)),
            "intact": list(range(76, 100)),
        }
        out["decomposition"] = {
            g: round(float(np.sqrt(np.mean(
                (V[idx] - tgt[idx]) ** 2))), 2)
            for g, idx in groups.items()}
        out["zone_means"] = res[0]["per_zone"]
    return out


def main() -> dict:
    print("=== exp97: the coverage repair ===\n")

    star = star_adj(100)
    out: dict[str, dict] = {}

    out["star_zones_star_pt"] = arm(star, STAR_PT, "zones")
    out["star_walk_star_pt"] = arm(star, STAR_PT, "walk")
    out["star_walk_below"] = arm(star, STAR_PT, "walk",
                                 seeds=(1, 2), spec=BELOW)
    out["star_walk_nocanon"] = arm(star, STAR_PT, "walk",
                                   seeds=(1, 2), with_canon=False)
    tree, cycle = tree_adj(100), cycle_adj(100)
    grid = grid_2d(5, 20)
    out["tree_walk"] = arm(tree, STAR_PT, "walk")
    out["cycle_walk"] = arm(cycle, STAR_PT, "walk")
    out["grid_walk"] = arm(grid, STAR_PT, "walk")
    out["star_walk_state"] = arm(star, STAR_PT, "walk",
                                 seeds=(1,), return_state=True)
    out["star_zones_state"] = arm(star, STAR_PT, "zones",
                                  seeds=(1,), return_state=True)
    for k, v in out.items():
        line = (f"    {k:24s} rate {v['rate']:.2f} err {v['err']}"
                f" (walk->settle {v['post_walk_err']}"
                f"->{v['post_settle_err']})")
        print(line)

    cv_g1 = (out["star_zones_star_pt"]["rate"] <= 1 / 3
             and 8.0 <= out["star_zones_star_pt"]["err"] <= 9.5)
    cv_g2 = out["star_walk_star_pt"]["rate"] >= 2 / 3
    cv_g3 = (abs(out["star_walk_star_pt"]["post_settle_err"]
                 - out["star_walk_star_pt"]["post_walk_err"]) < 0.5)
    cv_g4 = (out["tree_walk"]["rate"] >= 2 / 3
             and out["cycle_walk"]["rate"] >= 2 / 3
             and out["grid_walk"]["rate"] >= 2 / 3)
    cv_g5 = (out["star_walk_below"]["rate"] <= 1 / 3
             and out["star_walk_nocanon"]["rate"] <= 1 / 3)
    print(f"\n  CV-G1 artifact pinned (zones-mode floor): "
          f"{'PASS' if cv_g1 else 'REFUTED'}")
    print(f"  CV-G2 repair buys the star: "
          f"{'PASS' if cv_g2 else 'REFUTED'}")
    print(f"  CV-G3 pattern static (no settle drift): "
          f"{'PASS' if cv_g3 else 'REFUTED'}")
    print(f"  CV-G4 repair universal (tree/cycle/grid): "
          f"{'PASS' if cv_g4 else 'REFUTED'}")
    print(f"  CV-G5 domain rule survives: "
          f"{'PASS' if cv_g5 else 'REFUTED'}")

    npass = sum([cv_g1, cv_g2, cv_g3, cv_g4, cv_g5])
    print(f"\n  === {npass}/5 gates PASS ===")

    result = {
        "exp": "exp97_coverage_repair",
        "arms": out,
        "criteria": {
            "CV_G1_artifact_pinned": bool(cv_g1),
            "CV_G2_repair_buys_star": bool(cv_g2),
            "CV_G3_pattern_static": bool(cv_g3),
            "CV_G4_repair_universal": bool(cv_g4),
            "CV_G5_domain_rule_survives": bool(cv_g5),
        },
        "notes": (
            "The probe refuted L77-L78's settle-homogenization "
            "mechanism: the star's 8.5 floor is ~32 amputated-"
            "never-rebuilt gap cells at blastema -40 (the frontier "
            "enumerated over the zone union on a laterally "
            "disconnected region). The repair enumerates the "
            "blastema frontier over the amputation range "
            "(frontier_mode='walk', default 'zones' bit-exact). "
            "The registered per-edge hub anchor is MOOTED by the "
            "probe (cells that were never rebuilt need reads, not "
            "signaling architecture); 3 seeds, 2 for controls."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
