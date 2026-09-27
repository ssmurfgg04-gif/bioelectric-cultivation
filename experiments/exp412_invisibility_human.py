#!/usr/bin/env python3
"""exp412 — THE STRESS-INVISIBILITY ON THE HUMAN CONNECTOME (batch
HU-10; handoff Test 2b). exp407 explained the composed carrier's
+0.0000 mV stress delta as the SATURATION bypass on the planarian
chain; exp404 landed COMPOSITION-CLASS-MATCH — the human graph's
composition is ADDITIVE (f = -0.025, Celnik-consistent) where the
planarian's is SUPER-ADDITIVE (P_union = +13.13 mV). THE OPEN
QUESTION: does the saturation bypass itself transfer — is the g=1.0
committed layer on the REAL HUMAN CONNECTOME equally unreached by
stress — or does the human substrate keep the dynamics readable under
composition (a second, mechanistic face of the composition-class
split)? If the bypass transfers, invisibility is a property of the
commit ARCHITECTURE (substrate-general); if it breaks, it is a
property of the substrate's coupling (and shares a mechanism with
exp404's additivity — the charter's recorded question advances).

THE INSTRUMENT (exp403's ported human walk VERBATIM, composed with
exp407's 2-arm face): the exp401 pre-registered human adjacency (the
Schaefer-400 k=6 form, sha-pinned), the identity target, the zone-0
wound corrupted to -30.0, the BFS boundary walk, STEPS_PER_CELL 8,
COMMIT_NOISE 0.6; the register blend at the boundary cells; the
exp290 write-time -35.0 pin, restored -60.0. The composed union here
is (ctx, gj) at g=1.0 — the apop sigma face excluded as exp407
excluded it (it scales the noise, not the blend; disclosed); the gj
face on the human graph = the junction cells (degree >= 2 off the
wound boundary, the exp407 junction rule ported verbatim).
  ARMS: {union OFF, union ON} x {stress OFF, stress ON} x 5 seeds
  (the union-OFF arms ARE exp403's H0/H1 arms at the shared seeds —
  the anchor reuse is disclosed, no re-derivation);
  THE LADDER: g in {1.0, 0.75, 0.5, 0.25, 0.0} x stress x 3 seeds
  (disclosed budget: 3 seeds on the ladder, 5 on the g=1.0 head).
READS: (a) at g=1.0 every blended cell's committed value across the
stress arms — bit-equality; (b) the settled decode error deltas per
g; (c) the cross-species table: the human |Delta(g)| against the
planarian chain's deposited exp407 table and a fresh n=100 chain
replica at the same seeds (the shared-seed comparison, disclosed).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      human FC sha asserted against human/substrate.py's pin; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      pin -35.0, the ladders); the union-OFF arms reproduce exp403's
      deposited per-seed errs BIT-EXACT at the shared seeds
      (fail=STOP).
  G2  THE BYPASS FACE ON HUMAN: at g=1.0, EVERY blended cell's
      committed value is BIT-IDENTICAL across the stress arms in 5/5
      seeds AND the settled stress delta == 0.0 exactly.
  G3  THE DISSOLUTION LADDER: |Delta(g)| monotone non-decreasing as g
      falls 1.0 -> 0.0 on the human graph (the mean over the 3 ladder
      seeds; ties allowed at 0.0).
  G4  THE CROSS-SPECIES TABLE: the human vs planarian-chain |Delta|
      per g deposited side by side; the class comparison stated
      (same-ladder / human-raises / human-lowers) with the ratio at
      g=0.5.
  G5  THE DEPOSIT: the bit-equality flags, the ladder table, the
      cross-species table, gates + branch as
      results/exp412_invisibility_human.json (fail=STOP).

BRANCH LATTICE (pre-named): G2 PASS -> INVISIBLE-TRANSFERS (the
bypass is commit-architecture, substrate-general — the "memory-write
discipline" target from exp407 carries to human-scale design); G2
FAIL with the human delta >= 1.0 mV at g=1.0 -> INVISIBLE-BREAKS-
HUMAN (a species difference mechanistically consistent with exp404's
additivity: an additive substrate keeps the dynamics readable under
composition); G2 FAIL with the delta in (0, 1.0) mV mixed across
seeds -> INCONCLUSIVE (the table localizes it either way). G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: the second discriminator for the composition-class
question — architecture vs substrate. Either answer sharpens what
"strengthening the carrier" would even mean on a human-scale
neuromodulation target.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
GLADDER = [1.0, 0.75, 0.5, 0.25, 0.0]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
HEAD_SEEDS = [0, 1, 2, 3, 4]
LADDER_SEEDS = [0, 1, 2]
WOUND_VOLT = -30.0
DEPOSIT = os.path.join(ROOT, "results", "exp412_invisibility_human.json")


def main() -> dict:
    raise NotImplementedError(
        "exp412 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
