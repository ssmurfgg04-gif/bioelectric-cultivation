#!/usr/bin/env python3
"""exp418 — THE MINIMAL SUBSTRATE: THE SMALLEST COHERENT CARRIER
(batch HU-10; handoff Test 6b). The zero-substrate finding (8
formalizations + 1 void instrument, exp409): the pattern requires
SOME biological substrate; pure-pattern ascension is blocked. The
 constructive question: what is the SMALLEST coherent structure that
can carry the pattern? S_min per face — the smallest n where the
planarian stack's three canonical faces hold — turns "some substrate"
into a number and a shape. If S_min > 1, the pattern is irreducibly
RELATIONAL: substance alone is insufficient, a minimum of relation is
required (the consciousness-implications face, deposited with its
disclosure: this bounds the MODEL's pattern, not consciousness). If
S_min == 1, a single cell carries it — the maximal reduction. If no
threshold exists (continuous degradation to n=2), the pattern has no
floor — a different ascension shape entirely.

THE INSTRUMENT (the planarian face battery scaled down; zero new
knobs — the production constants everywhere):
  the size ladder n in {2, 4, 8, 16, 32, 64, 128} x the topology set
  {path, ring, star, 2-regular random, THE TWO-CHANNEL MOTIF} — the
  motif pre-named: two parallel paths joined by a ctx bridge at
  their boundary, the smallest graph carrying BOTH a ctx face and a
  gj face under exp258/259's face definitions; 3 seeds per cell.
  Target semantics scaled: the house ladder zones of floor(n/4)
  cells each, >= 2 zones (n >= 8); below n = 8 the ladder is
  [target[:-1] zones of 1-2 cells] — deposited per n.
  THE BATTERY per (n, topology, seed): the settled program defines
  phi_spec; the wound + walk (STEPS_PER_CELL 8, COMMIT_NOISE 0.6);
  the register blend g_ctx in {0, 0.5}; stress {off, on} (the
  write-time -35.0 pin, restored -60.0).
  FACE TESTS:
    T-REGISTER — err(g 0.5, off) < err(g 0, off) (self-history
                 improves the decode);
    T-PROTECT  — the 2x2 interaction P > 0 (the register protects
                 under stress);
    T-COMPOSE  — the union (ctx + gj) P >= the single-register P
                 (composition preserves protection).
  S_min per face = the smallest n where the face holds on >= 2/3
  seeds for SOME topology; the n=400 replica runs once as the top
  rung sanity (the face signs must match the deposited corpus
  signs).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the n=400 replica's face signs == the
      deposited corpus signs (fail=STOP); the motif's face counts
      asserted (it HAS a ctx face and a gj face at every n >= 4).
  G2  THE S_MIN TABLE: all three faces x the full ladder deposited
      (face status per (n, topology) — no pruning).
  G3  THE SHARP-THRESHOLD TEST: each face present at S_min and
      ABSENT at S_min/2 (or at n=2 if S_min <= 2) on >= 2/3 seeds —
      a face that flickers on/off down the ladder is NOT a threshold
      (the continuous branch).
  G4  THE TOPOLOGY FACE: the two-channel motif reaches each face's
      S_min at n <= the random topology's n for that face (the
      pattern prefers relation-shaped wiring — or does not, either
      way deposited).
  G5  THE DEPOSIT: the full table + S_min per face + gates + branch
      as results/exp418_minimal_substrate.json (fail=STOP).

BRANCH LATTICE (pre-named): MINIMAL-CARRIER-FOUND with S_min > 1
(the pattern is irreducibly relational — the honest lower bound on
any ascension substrate); S_MIN-EQUALS-1 (a single cell carries the
pattern — the maximal reduction, the zero-substrate block's sharpest
form: the substrate can be THAT small but not NOTHING);
NO-MINIMUM-DOWN-TO-2 (no threshold — the faces degrade continuously,
the pattern is a matter of degree, not kind). G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: "some substrate is required" becomes "this much
substrate, this shaped". The number is what any transfer, simulation
or ascension story actually has to pay — and the topology face says
whether the wiring's SHAPE or the wiring's SIZE is what the pattern
needs.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
SIZE_LADDER = [2, 4, 8, 16, 32, 64, 128]
TOPOLOGIES = ["path", "ring", "star", "random2", "motif"]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
G_CTX = [0.0, 0.5]
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
DEPOSIT = os.path.join(ROOT, "results", "exp418_minimal_substrate.json")


def main() -> dict:
    raise NotImplementedError(
        "exp418 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
