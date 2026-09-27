#!/usr/bin/env python3
"""exp446 — THE DOSE-AXIS COVERAGE INSTRUMENT (batch HU-14; exp438's
no-op disclosure). exp438: the pharmacological lattice is anchored
but INEXPRESSIBLE in the realizability predicate — the predicate has
no dose column. HYPOTHESIS: a dose-coverage column (whether the
anatomy's intervention classes have corpus-realized dose ranges
sufficient to reach the anatomy's required contrast) makes the
lattice expressible and re-scores the 10 anatomies honestly.

THE INSTRUMENT (exp438's machinery verbatim + the dose-coverage
column): per anatomy, the required contrast (its max_contrast) vs
the reachable contrast under the corpus's realized dose ranges for
its intervention classes (the exp118 class table's dose ranges, the
exp410 dose-axis mapping); the column deposited; the 10-anatomy
re-scoring with the column active.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: exp438's deposited feasible set + union-open set
      reproduced (fail=STOP).
  G2  the discipline: the dose column computed from the corpus's
      OWN realized dose ranges (no invented doses).
  G3  THE RE-SCORE: the dose column flips >= 1 anatomy's
      realizability (DOSE-BINDING — the lattice earns its column)
      or flips none (DOSE-UNBINDING — the geometry columns were the
      only bindings; the lattice stays out of the spec).
  G4  the anatomy: the (anatomy x required-vs-reachable contrast)
      table deposited.
  G5  deposit results/exp446_dose_coverage_instrument.json.

BRANCH LATTICE: DOSE-BINDING / DOSE-UNBINDING / INSTRUMENT-REFUTED.
"""
