#!/usr/bin/env python3
"""exp419 — WHAT FIXES THE COMPOSITION CLASS? (batch HU-10; the
charter's recorded next question — docs/HUMAN_EXTENSION.md's closing
paragraph: "what fixes the composition class (the substrate's coupling
regime? the wound's stress context? the spec layer's persistence?)" —
recorded, not pursued, because the closure rule fired; THIS batch
pursues it). exp404 landed the sharpest species difference: the
planarian stack composes SUPER-ADDITIVELY (P_union = +13.13 mV) where
the human substrate composes ADDITIVELY (f = -0.025, Celnik-
consistent). exp412 tests the same split through the invisibility
face; THIS experiment tests the three pre-named determinant
candidates DIRECTLY — each one swapped on each substrate, the
composition class re-measured, the flip located.

THE INSTRUMENT (the exp293 / exp403 2x2 forms VERBATIM on their
respective substrates — the planarian replica and the Schaefer-400
human adjacency; 3 seeds; the composed union (ctx, gj) at g=1.0, the
apop sigma face excluded as exp407 excluded it; the P read = the
standard 2x2 interaction on the decode error):
  D1  THE COUPLING REGIME (the wiring statistics): the planarian
      replica's P re-measured on a degree-matched FC-style top-k
      graph (the planarian walk on human-SHAPED wiring); the human
      graph's P re-measured on a path-style degree-matched graph
      (the human walk on planarian-SHAPED wiring). A class flip on
      either substrate with the wiring alone = D1.
  D2  THE STRESS CONTEXT: the composed 2x2 measured with NO
      write-time stress (all four cells unstressed; the composition
      improvement vs the protection dissociated — the rest-context
      composition face). A class flip between the stressed and
      rest-context forms on either substrate = D2.
  D3  THE SPEC PERSISTENCE: the canon layer present vs absent on
      both substrates (the human instrument's canon-ABSENT default
      per exp403's disclosure; the planarian replica's canon present
      — crossed both ways). A class flip with the canon alone = D3.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      FC sha pinned; the constants asserted; each substrate's
      canonical P reproduces its deposited class at the shared
      seeds — the planarian P_union > 0 (super-additive, the exp302
      face) and the human P in the additive band (|f| <= 0.10, the
      exp404 face) — bit-exact where the deposits store per-seed
      values, sign-exact at the fresh additive seeds (disclosed).
  G2  THE D1 SWAP TABLE: P measured on both swapped wirings, both
      substrates; the class (super-additive / additive / amplifying)
      deposited per cell.
  G3  THE D2 REST-CONTEXT TABLE: P_rest per substrate, the
      stressed-vs-rest class change deposited.
  G4  THE D3 CANON TABLE: P with the canon crossed per substrate.
  G5  THE VERDICT ARITHMETIC + DEPOSIT: the determinant = the
      candidate whose swap flips the composition class on >= 1
      substrate; multiple flippers -> the one with the LARGER flip
      magnitude (the deposited P delta); NO candidate flips anything
      -> NO-SINGLE-DETERMINANT (the class is multi-causal or
      intrinsic — deposited with the full 3-candidate table). All
      tables + gates + branch as
      results/exp419_composition_determinant.json (fail=STOP).

BRANCH LATTICE (pre-named): DETERMINANT-COUPLING (the wiring's shape
fixes the class — exp404's additivity is a GRAPH property, portable
by rewiring); DETERMINANT-STRESS-CONTEXT (the class is a CONTEXT
property — composition composes differently under threat);
DETERMINANT-SPEC-PERSISTENCE (the class is a MEMORY property — the
canon layer's persistence is what super-additivity needs);
NO-SINGLE-DETERMINANT. G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: the bridge's sharpest species difference gets its
cause. A determinant means the composition class is ENGINEERABLE
(pick the wiring, the context, or the memory); no determinant means
the planarian super-additivity is sui generis — deposited as such,
no forcing.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
G_UNION = 1.0
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
STRESS_FLOOR = -35.0
ADDITIVE_BAND = 0.10
SEEDS = [0, 1, 2]
DEPOSIT = os.path.join(ROOT, "results", "exp419_composition_determinant.json")


def main() -> dict:
    raise NotImplementedError(
        "exp419 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
