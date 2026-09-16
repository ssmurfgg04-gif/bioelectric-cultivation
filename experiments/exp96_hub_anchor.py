#!/usr/bin/env python3
"""exp96 — THE HUB ANCHOR (ledger L78; the exp75-77 slow-anchor
theorem applied to the reader — exp95's registered repair).

THE REGISTERED PREDICTION: exp95 showed the deg-99 star's refusal is
architectural — the hub integrates the whole disc during the settle.
The exp75-77 theorem (coherence requires an anchor slower than the
hijack) says the fix is an ANCHOR, not a dial: clamp the hub to its
canon identity through the settle, release 1h before the read. With
the anchor, the spokes relax to the canon hub and the pattern
survives. Prediction: the star verifies at the star point WITH the
anchor; the anchor is the difference (the unanchored control stays
at exp95's ~8.5 mV floor); the anchor is harmless on the working
substrates; and the anchor buys OPERATING-POINT FREEDOM (the
exp75-77 theorem: the dials were compensating for the missing
anchor — with it, (1, 0) should also verify).

PRE-REGISTERED GATES:

  HA-G1  (the anchor buys the star) the star's multi program with
         the hub anchor verifies at the star point (>= 2/3 seeds).
  HA-G2  (the anchor is load-bearing) the unanchored control fails
         (exp95's deposited floor) while the anchored arm passes —
         the clamp is the difference.
  HA-G3  (no harm) the anchored variant still verifies on tree and
         cycle (the anchor does not break the working topologies).
  HA-G4  (the theorem's price) with the anchor, the star also
         verifies at (gamma=1, mu=0) — the anchor replaces the dial
         requirement (the slow anchor IS the missing architecture).

RUN: star x {unanchored, anchored} x {(64,0), (1,0)} x 3 seeds +
tree/cycle anchored controls. Serial, BLAS pinned.
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
    execute_two_source_n, MULTI, star_adj, tree_adj, cycle_adj,
    labeling_bfs_n,
)
from experiments.exp91_dose_axis_wiring import SEEDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp96_hub_anchor.json")

STAR_PT = {"gamma": 64.0, "mu": 0.0}
LOW_PT = {"gamma": 1.0, "mu": 0.0}


def arm(adj, op, anchored, seeds=SEEDS):
    anchor = None
    if anchored:
        canon = labeling_bfs_n(adj)
        anchor = [(0, float(canon[0]))]
    res = [execute_two_source_n(MULTI, adj, s, op=op, anchor=anchor)
           for s in seeds]
    return {
        "rate": round(float(np.mean(
            [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2),
    }


def main() -> dict:
    print("=== exp96: the hub anchor ===\n")

    star = star_adj(100)
    out: dict[str, dict] = {}

    out["star_unanchored_star_pt"] = arm(star, STAR_PT, anchored=False)
    out["star_anchored_star_pt"] = arm(star, STAR_PT, anchored=True)
    out["star_anchored_low_pt"] = arm(star, LOW_PT, anchored=True)
    out["star_unanchored_low_pt"] = arm(star, LOW_PT, anchored=False)
    tree, cycle = tree_adj(100), cycle_adj(100)
    out["tree_anchored"] = arm(tree, STAR_PT, anchored=True)
    out["cycle_anchored"] = arm(cycle, STAR_PT, anchored=True)
    for k, v in out.items():
        print(f"    {k:28s} rate {v['rate']:.2f} err {v['err']}")

    ha_g1 = out["star_anchored_star_pt"]["rate"] >= 2 / 3
    ha_g2 = (out["star_unanchored_star_pt"]["rate"] <= 1 / 3
             and ha_g1)
    ha_g3 = (out["tree_anchored"]["rate"] >= 2 / 3
             and out["cycle_anchored"]["rate"] >= 2 / 3)
    ha_g4 = out["star_anchored_low_pt"]["rate"] >= 2 / 3
    print(f"\n  HA-G1 anchor buys the star: "
          f"{'PASS' if ha_g1 else 'REFUTED'}")
    print(f"  HA-G2 anchor load-bearing: "
          f"{'PASS' if ha_g2 else 'REFUTED'}")
    print(f"  HA-G3 no harm (tree/cycle): "
          f"{'PASS' if ha_g3 else 'REFUTED'}")
    print(f"  HA-G4 operating-point freedom: "
          f"{'PASS' if ha_g4 else 'REFUTED'}")

    npass = sum([ha_g1, ha_g2, ha_g3, ha_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    result = {
        "exp": "exp96_hub_anchor",
        "arms": out,
        "criteria": {
            "HA_G1_anchor_buys_star": bool(ha_g1),
            "HA_G2_anchor_load_bearing": bool(ha_g2),
            "HA_G3_no_harm": bool(ha_g3),
            "HA_G4_op_freedom": bool(ha_g4),
        },
        "notes": (
            "The exp75-77 slow-anchor theorem applied to the reader: "
            "the hub clamped to its canon identity through the 15h "
            "settle, released 1h before the read (the pattern must "
            "HOLD without the clamp). exp94's executor with the "
            "backward-compatible anchor parameter; 3 seeds."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
