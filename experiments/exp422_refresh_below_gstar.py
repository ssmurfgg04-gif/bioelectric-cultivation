#!/usr/bin/env python3
"""exp422 — THE REFRESH BELOW g*: THE DISCIPLINE RECIPE TESTED (batch
HU-11; ledger L306's deposited constraint — exp411's two-pass refresh
at g=0.5 retained the carrier but sat deep inside the invisible band
(g* = 0.117); the recipe needs a refresh BELOW g*). HYPOTHESIS: a
refresh pass at g < g* returns stress visibility while the carrier's
improvement survives the second pass.

THE INSTRUMENT (exp411's landed form verbatim: path(100), the 3-zone
spec, faces (ctx,gj), the -35.0 pin restored -60.0): the two-pass
write — commit saturated at g=1.0, ONE refresh pass at the ladder
{0.10, 0.08, 0.05} (all below g* = 0.117) — then the stress 2x2, 10
seeds; the carrier-retained and visibility-returned faces as exp411's
frozen definitions.
PRE-REGISTERED GATES:
  G1  floor discipline; the constants; exp407/exp411's anchor arms
      bit-exact at the shared seeds.
  G2  the refresh ladder's |Delta| monotone NON-INCREASING as the
      refresh g falls toward 0 (the visibility dial works).
  G3  THE VIABLE WINDOW: exists a refresh g in the ladder with BOTH
      carrier retained (>= 0.8 x the one-pass improvement) AND
      visibility returned (>= 0.10 x the g=0 delta) on >= 7/10 seeds;
      the window's edges deposited.
  G4  the trade curve: the improvement-vs-visibility frontier per
      refresh g, deposited (the recipe's price list).
  G5  deposit results/exp422_refresh_below_gstar.json.
BRANCH: MEMORY-DISCIPLINE-VIABLE (G3 PASS — the recipe exists, the
window deposited) / VIABILITY-COSTLY (the frontier deposited, no
window — every visibility gain spends carrier) / INSTRUMENT-REFUTED.
THE HONEST STAKES: exp407 moved the practical target to memory-write
discipline; exp411 bounded the band; THIS experiment either hands over
the recipe or prices every point on the frontier.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

REFRESH_LADDER = [0.10, 0.08, 0.05]
G_STAR = 0.117
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
DEPOSIT = os.path.join(ROOT, "results", "exp422_refresh_below_gstar.json")


def main() -> dict:
    raise NotImplementedError(
        "exp422 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
