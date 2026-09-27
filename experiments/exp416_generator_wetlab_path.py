#!/usr/bin/env python3
"""exp416 — THE GENERATOR'S WET-LAB PATH: WHICH NOVEL ANATOMY IS
REALIZABLE FIRST? (batch HU-10; handoff Test 5, analysis-only — no
new data, no wet lab). The generator stack landed 10/10 novel
anatomies computationally validated and ZERO wet-lab confirmation —
the honest gap the corpus has carried since the generator batch. This
experiment converts the gap into a ranked, costed menu: which of the
10 anatomies is closest to physically realizable with PlanformDB's
EXISTING intervention classes (the corpus's drug/ligand classes and
their observed dose ranges), and what is the MINIMAL wet-lab test
that would confirm or refute ONE of them. The output is a spec a
lab could execute with nothing the corpus has not already used.

THE INSTRUMENT (analysis over landed deposits; fail=STOP if the
generator's novel-anatomy deposit is absent):
  the generator's novel-anatomy deposit (the 10/10 set — located at
  run time from the generator batch's deposit index under results/),
  each anatomy's required edge/flip pattern; PlanformDB's
  intervention classes as deposited (the class -> drug/ligand table
  + each class's observed dose range).
SCORING per anatomy (zero knobs, binary + count):
  (a) COVERAGE — every required intervention inducible by an
      existing class (partial coverage = the fraction, deposited);
  (b) FEASIBILITY — every required dose within the class's observed
      corpus range (the out-of-range list deposited per anatomy);
  (c) COST — the count of distinct interventions (fewer = cheaper).
  RANK = (full coverage, full feasibility, -cost) lexicographic.
THE MINIMAL SPEC (for the top-ranked anatomy): N worms = the corpus's
minimum powered n for the target morphology readout; the intervention
list (class, drug, dose, timing); the predicted morphology readout
per the model's target semantics; the falsification threshold = the
model's prediction +/- the corpus's own measurement noise for that
readout (the honest bar: the test must be able to FAIL).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE LOAD: the generator deposit + the PlanformDB class table
      located, loaded, shas logged (fail=STOP if either is absent —
      INSTRUMENT-VOID, no fabricating a deposit).
  G2  THE SCORING TABLE: all 10 anatomies scored on (a)(b)(c), the
      table deposited in full (no pruning to the winner).
  G3  THE PATH: >= 1 anatomy with FULL coverage AND FULL feasibility
      -> the minimal wet-lab spec deposited per the pre-named form;
      else NO-PATH (the blocking classes per anatomy deposited).
  G4  THE RANKING: the top-3 by the pre-named lexicographic rank
      deposited with their cost counts.
  G5  THE DEPOSIT: the table, the spec or the blockers, gates +
      branch as results/exp416_generator_wetlab_path.json
      (fail=STOP).

BRANCH LATTICE (pre-named): WETLAB-PATH-OPEN (a spec exists a lab
could run with the corpus's own toolbox — the zero-confirmation gap
has a price tag); NO-PATH-WITHOUT-NEW-EQUIPMENT (the blocking
classes ARE the discovery: what the corpus lacks is named — the gap
becomes a shopping list, not a shrug). G1 FAIL -> INSTRUMENT-VOID.

THE HONEST STAKES: "10/10 computationally validated, zero wet-lab
confirmation" is either a fatal gap or a queue. This experiment
makes it a queue — ordered, costed, falsifiable — or names exactly
which tool is missing.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
DEPOSIT = os.path.join(ROOT, "results", "exp416_generator_wetlab_path.json")


def main() -> dict:
    raise NotImplementedError(
        "exp416 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
