#!/usr/bin/env python3
"""exp421 — THE UNION-BLEND STREAM'S WIRING RECONSTRUCTION: THE
SHARPENING LEVER (batch HU-11; ledger L310's named lever — exp414's
boundary-blend stream reached AUC 0.63-0.68 because the blend faces
cover only the walked cells' coupling; the UNION form blends at EVERY
walked cell, putting every cell's commit under the register's pull and
widening the co-movement coverage). HYPOTHESIS: the union stream's
fingerprint clears the 0.85 bar on >= 2/3 graphs.

THE INSTRUMENT (exp414's machinery verbatim except the blend form):
three graphs, 10 rounds under the stress pin, the commit trajectories'
cross-correlation, edges := top-k by |S|; the UNION stream = the blend
at all walked cells (g_ctx 0.5); the BOUNDARY stream re-run as the
paired control (exp414's form); the shuffled null + the decoy as
exp414's.
PRE-REGISTERED GATES:
  G1  floor discipline; the constants; the graph identities logged.
  G2  the union stream's AUC >= 0.85 on >= 2/3 graphs.
  G3  the union-over-boundary improvement >= 0.05 AUC on >= 2/3 graphs
      (the lever's measured effect, both streams deposited).
  G4  the null <= 0.60 and the decoy gap >= 0.2 on every graph where
      G2 fired.
  G5  deposit results/exp421_union_stream_reconstruction.json.
BRANCH: WIRING-RECOVERABLE (G2 PASS) / SHARPENED-PARTIAL (G3 PASS, G2
REFUTE) / LEVER-NULL (G3 REFUTE) / INSTRUMENT-REFUTED.
THE HONEST STAKES: substrate-independence's concrete test gets its
sharpest honest shot — the structure in the trace, measured under the
blend form the carrier itself uses.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
GRAPHS = ["path100", "planarian400", "human400"]
ROUNDS = 10
DEPOSIT = os.path.join(ROOT, "results",
                       "exp421_union_stream_reconstruction.json")


def main() -> dict:
    raise NotImplementedError(
        "exp421 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
