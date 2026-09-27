#!/usr/bin/env python3
"""exp424 — THE n=4 PROTECTIVE MOTIF: WHAT STRUCTURE CARRIES
PROTECTION? (batch HU-11; ledger L313's sharp floor — t_protect holds
at n=4 on all five topologies and fails below: the pattern's
stress-protection is irreducibly relational with a QUARTET as the
floor). HYPOTHESIS: at n=4 the protection face is carried by a
SPECIFIC wiring property (the minimum cut between the wound set and
the register's boundary — the pre-named candidates: (M-CUT) the
wound's live-neighbor count >= 2, (M-CYCLE) the graph contains a cycle
through the frontier, (M-BRIDGE) the wound has >= 2 boundary cells
sharing a neighbor) — the census decides which.

THE INSTRUMENT (the exp418 battery form verbatim at n=4): the FULL
4-cell census — every labeled graph on 4 nodes up to isomorphism with
<= 5 edges (the pre-named edge budget = the corpus's mean degree
band): 11 unlabeled graphs; 3 seeds each; the wound = the 1-cell and
2-cell sets per graph (both wound geometries); the t_protect read per
(graph, wound) — P > 0 on >= 2/3 seeds.
PRE-REGISTERED GATES:
  G1  floor discipline; the census complete (the 11 graphs enumerated
      and hashed; the wound geometries 1+2-cell per graph).
  G2  the protective set: the (graph, wound) cells where t_protect
      holds, deposited in full.
  G3  THE CARRIER TEST: exactly ONE pre-named mechanism's presence
      predicts protection on >= 90% of the protective cells AND its
      absence predicts failure on >= 90% of the rest (the confusion
      table deposited); two mechanisms tie -> MIXED-CARRIER.
  G4  the n=3 control: the same census at n=3 (the face must fail —
      the L313 floor's other side, asserted).
  G5  deposit results/exp424_protective_motif_n4.json.
BRANCH: CARRIER-{CUT|CYCLE|BRIDGE} / MIXED-CARRIER /
NO-SINGLE-CARRIER / INSTRUMENT-REFUTED.
THE HONEST STAKES: the minimal substrate's shape — the smallest
protectable unit and the wiring property it needs — is the concrete
answer to "what would ascension even need".
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
STRESS_FLOOR = -35.0
SEEDS = [0, 1, 2]
MAX_EDGES = 5
DEPOSIT = os.path.join(ROOT, "results",
                       "exp424_protective_motif_n4.json")


def main() -> dict:
    raise NotImplementedError(
        "exp424 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
