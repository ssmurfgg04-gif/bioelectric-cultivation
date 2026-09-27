#!/usr/bin/env python3
"""exp414 — WIRING RECOVERABLE FROM THE COMMIT STREAM ALONE (batch
HU-10; handoff Test 3b). The pattern lives in the wiring-keyed
indexation (exp413 tests the identity face); the CONVERSE question is
forensic: does the commit history — the register's recorded stream,
values only, no wiring access — contain enough information to
RECONSTRUCT the wiring? If yes, "the wiring lives in the pattern's
history" becomes a measured statement, and substrate-independence
acquires a concrete meaning: the structure is recoverable from the
pattern's own trace, with no access to the substrate's anatomy. This
is the memory-forensics face of the indexation claim.

THE INSTRUMENT (zero knobs, pre-named): three graphs — path(100),
the planarian n=400 replica host, the human Schaefer-400 k=6
adjacency (sha-pinned); run the standard walk on each (the settled
program + the correction walk, STEPS_PER_CELL 8, COMMIT_NOISE 0.6,
the register blend g_ctx = 0.5 at the blend faces) and record EVERY
commit: (cell, order, value) — the stream is the ONLY input to the
reconstruction (the walk order is legitimately available — the
destination-donates-its-walk-order legality, the exp307 precedent).
RECONSTRUCTION (pre-named): the commit-time cross-correlation matrix
S_ij over the stream (the commits at coupled cells co-move through
the blend and gj faces); edges := the top-k pairs by |S_ij| with k =
the TRUE edge count (the oracle-k disclosure: the count, not the
identities, is assumed known); score AUC (the full |S| matrix as the
statistic vs the true adjacency) and precision@k.
CONTROLS: (a) the shuffled-stream null — the commit values randomly
permuted in time per cell (AUC must collapse to ~0.5: the structure
is in the CO-MOVEMENT, not the marginals); (b) the decoy — a
degree-matched different graph; the reconstruction scored against the
decoy must NOT approach its score against the true graph (the
fingerprint is graph-specific).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      three graphs' identities logged (the FC sha pinned; path(100)
      == the exp136 A_CHAIN form); the walk reproduces the anchor
      commit counts (STEPS_PER_CELL x the walked cells, asserted);
      all stream values finite (fail=STOP).
  G2  THE RECOVERY: AUC >= 0.85 on >= 2/3 graphs (the per-graph AUC +
      precision@k deposited).
  G3  THE NULL: the shuffled-stream AUC <= 0.60 on ALL three graphs.
  G4  THE DECOY: AUC(true) - AUC(scored against the decoy) >= 0.2 on
      the graphs where G2 fired.
  G5  THE DEPOSIT: the per-graph table (AUC, precision@k, null AUC,
      decoy AUC) + gates + branch as
      results/exp414_wiring_from_history.json (fail=STOP).

BRANCH LATTICE (pre-named): G2 PASS -> WIRING-RECOVERABLE (the
commit history is a wiring fingerprint — the register is enough to
rebuild the connectome's shape); AUC in [0.65, 0.85) on the best
graphs -> WIRING-PARTIAL (the fingerprint is blurred — WHICH graphs
blur it, deposited: the blend faces' coverage is the suspected
mechanism); AUC <= 0.65 everywhere -> NOT-RECOVERABLE (the stream
carries the content, not the key — the indexation claim loses its
converse). G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: exp409's void instrument and exp413's asymmetry
constrain what indexation IS; this experiment tests what it LEAVES
BEHIND. A positive answer is the strongest substrate-independence
result the stack can honestly produce without new data: the
structure survives in the trace.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
GRAPHS = ["path100", "planarian400", "human400"]
DEPOSIT = os.path.join(ROOT, "results", "exp414_wiring_from_history.json")


def main() -> dict:
    raise NotImplementedError(
        "exp414 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
