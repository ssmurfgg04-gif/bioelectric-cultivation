#!/usr/bin/env python3
"""exp426 — THE LONG-CHAIN STREAM: ROUNDS AS THE FINGERPRINT LEVER
(batch HU-12; exp421's pre-named successor regardless of its branch).
exp414's blur analysis and exp421's union lever both act on COVERAGE;
the orthogonal lever is CHAIN LENGTH — the register carries across
rounds (the memory chain IS the signal), so a 30-round stream gives
each coupled pair 3x the co-movement samples and 3x the register-
mediated coupling history. The question: does the fingerprint's AUC
rise with the chain, and does it clear the 0.85 bar at 30 rounds?

THE INSTRUMENT (exp421's machinery verbatim, both its arms retained):
three graphs (path100, the planarian replica, the human Schaefer-400);
the UNION arm (whole-graph walk coverage) and the BOUNDARY arm
(exp414's wound-region form) at ROUNDS_SHORT 10 and ROUNDS_LONG 30;
the commit trajectories' cross-correlation, edges := top-k by |S|;
the shuffled null + the degree-matched decoy as exp414's.
BUDGET DISCLOSURE (frozen here, not discovered): SEEDS = [0, 1] — the
30-round union arm triples exp421's walk cost per seed; two seeds keep
the per-graph-best convention alive at 2/3 the rows.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the graph identities logged (sha per
      adjacency); all stream values finite (fail=STOP).
  G2  THE CONTINUITY: the boundary arm at 10 rounds reproduces
      exp414's deposited per-graph best AUCs within 0.05 on >= 2/3
      graphs (this instrument is the landed one's extension, not a
      new build).
  G3  THE CHAIN: the union arm at 30 rounds reaches AUC >= 0.85 on
      >= 2/3 graphs (per-graph best across seeds).
  G4  THE DOSE-RESPONSE: union AUC(30) > union AUC(10) on >= 2/3
      graphs AND the shuffled null at 30 rounds <= 0.60 on ALL
      graphs (more rounds must feed the SIGNAL, not the noise).
  G5  deposit results/exp426_long_chain_stream.json.

BRANCH LATTICE: CHAIN-CARRIES (G3 PASS) / CHAIN-PARTIAL (G3 REFUTE,
G4's first clause PASS — the lever's direction holds, the bar stays
out of reach) / CHAIN-NULL (G4 REFUTE — the fingerprint saturates at
10 rounds; the chain axis is closed) / INSTRUMENT-REFUTED (G1/G2
fail).

THE HONEST STAKES: if the chain carries the fingerprint past the bar,
"the wiring lives in the pattern's history" becomes a measured
reconstruction claim with a stated cost (chain length); if it
saturates, the commit stream's information content has a CEILING —
the indexation claim's converse gets its honest bound.
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
SEEDS = [0, 1]
GRAPHS = ["path100", "planarian400", "human400"]
ROUNDS_SHORT = 10
ROUNDS_LONG = 30
AUC_BAR = 0.85
CONTINUITY_TOL = 0.05
DEPOSIT = os.path.join(ROOT, "results",
                       "exp426_long_chain_stream.json")


def main() -> dict:
    raise NotImplementedError(
        "exp426 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
