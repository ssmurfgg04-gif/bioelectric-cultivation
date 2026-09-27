#!/usr/bin/env python3
"""exp442 — THE WOUND-COUPLED GLOBAL INVARIANT (batch HU-14;
exp441/440's shared exit). exp441: no single family fixes the
composition class — the nearest (global wiring, 24/26) fails exactly
on the chord-rings; exp440: what separates chord-rings (protective)
from double-rings (non) at equal cycle-rank and edge budget is WHERE
the redundancy sits relative to the wound region. HYPOTHESIS: the
protection is a function of the WOUND-COUPLED global invariant — a
global graph quantity evaluated on the wound-anchored decomposition
(e.g., the cycle-rank of the graph MINUS the region-induced
subgraph, the outside-the-wound redundancy).

THE INSTRUMENT (exp427/431/439/440's battery verbatim; the
decomposition as the new feature): for every form in the 26-form
union corpus (exp441's corpus verbatim), compute the
outside-the-wound cycle-rank (the full graph's cycle-rank minus the
region-induced subgraph's) and the inside/outside split of the
triangle content; the predicate candidates pre-named: (i) protective
iff outside-cr <= 1 AND triangle-free-outside; (ii) protective iff
inside-cr == 0; (iii) the two-sided conjunction. Zero-contradiction
test on all 26 forms (the union-table method).

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the corpus: exp441's 26-form union loads with agreeing
      overlaps (fail=STOP).
  G2  the features: the decomposition computed from the adjacency +
      the region rule only (no outcome leakage).
  G3  THE INVARIANT: >= 1 pre-named wound-coupled predicate
      separates all 26 forms with zero contradictions
      (INVARIANT-NAMED — the class-fixing feature is found) or none
      does (NO-INVARIANT — the honest close of the wiring family at
      this corpus).
  G4  the anatomy: the (form x decomposition-feature) matrix +
      the predicate table deposited.
  G5  deposit results/exp442_wound_coupled_invariant.json.

BRANCH LATTICE: INVARIANT-NAMED / NO-INVARIANT / INSTRUMENT-REFUTED.
"""
