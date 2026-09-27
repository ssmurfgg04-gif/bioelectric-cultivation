#!/usr/bin/env python3
"""exp413 — THE PATTERN IN THE WIRING: IDENTITY UNDER VALUE VS WIRING
CORRUPTION (batch HU-10; handoff Test 3a). The corpus's working
conclusion: the pattern lives in the WIRING-KEYED INDEXATION, not in
the transmitted values — what persists is the structure of
connections, not the content. exp409's void instrument left the
indexation question open at the transport level; THIS experiment
tests the claim at the IDENTITY level with a zero-knob asymmetry
design: corrupt the VALUES with the wiring intact, or corrupt the
WIRING with the values intact, and measure (a) the immediate pattern
integrity and (b) the RESTORATION — whether the standard correction
walk re-learns the pattern. The identity-continuity reading: if
value corruption is survivable and wiring permutation is not, then
identity (in this model) is continuity of connectivity, not of
content — the formal content behind the substrate-independence
discussion.

THE INSTRUMENT (the corpus replica discipline): the n=400
path-family host, the canonical identity target, the settled program
(30 tu) defines phi_spec; STEPS_PER_CELL 8, COMMIT_NOISE 0.6, floor
-60.0 restored everywhere; 3 seeds.
  A-VALUE   — corrupt ALL committed values: theta := theta + N(0,
              sigma) with sigma = the target's own std (the pre-named
              corruption scale — commensurate with the pattern's own
              dynamic range); the register corrupted identically
              (phi_history += N(0, sigma)); the wiring untouched.
  B-WIRING  — degree-preserving random rewiring of the adjacency (the
              configuration model, double-edge swaps), two sub-arms:
              B10 (10% of edges rewired) and B100 (full randomization
              to the same degree sequence); the values untouched.
  C-ANCHOR  — untouched (must reproduce the deposited corpus errs
              BIT-EXACT).
READS: pattern error vs the target at settle +10 tu for each arm;
the RESTORATION face: after the corruption, re-run the standard
correction walk (the landed battery walk) — A after 1x walk, B after
1x and after 10x walk (the indexation, if lost, should not return at
any budget a realistic substrate could spend); the register's rescue
re-measured on each restored form.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; C-ANCHOR == the deposited corpus errs
      BIT-EXACT per seed (fail=STOP); the rewiring preserves the
      degree sequence EXACTLY (asserted per arm).
  G2  THE CORRUPTION ASYMMETRY: err(B100) >= 3 x err(A) at the
      immediate read (or the normalized integrity gap >= 0.5 — the
      integrity = 1 - err/err(B100), deposited both ways).
  G3  THE RESTORATION ASYMMETRY: A restores to <= 1.5 x C-ANCHOR err
      after the 1x walk; B100 does NOT (err >= 3 x C-ANCHOR after the
      10x walk); B10's partial face deposited (between A and B100 or
      not — the dose of wiring destruction).
  G4  THE REGISTER FACE ON EACH FORM: the register rescue R re-runs
      after restoration — R survives value corruption (memory of the
      correction, if exp410 lands CORRECTION, predicts R intact on A)
      and collapses on B100 (the indexation gone); deposited per
      arm.
  G5  THE DEPOSIT: the full table + gates + branch as
      results/exp413_indexation_identity.json (fail=STOP).

BRANCH LATTICE (pre-named): G2+G3 PASS -> WIRING-DOMINANT (identity
= connectivity continuity, content-erasing; the consciousness-
implications face deposits the interpretation WITH its disclosure:
this is the MODEL's identity, an analogy for substrate-independence
claims, not a consciousness claim); G2 reversed -> VALUE-DOMINANT
(the working conclusion was wrong at the identity level — the values
carry more than the wiring); mixed -> MIXED (the asymmetry is
budget-dependent — deposited with the crossover point). G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: "the pattern lives in the wiring" has been a
summary phrase; this experiment makes it a measured asymmetry with a
restoration budget — and the restoration budget is what any transfer
story (morphic or mechanical) actually has to beat.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
REWIRE_FRACTIONS = [0.10, 1.00]
RESTORE_BUDGETS = [1, 10]
SEEDS = [0, 1, 2]
N = 400
DEPOSIT = os.path.join(ROOT, "results", "exp413_indexation_identity.json")


def main() -> dict:
    raise NotImplementedError(
        "exp413 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
