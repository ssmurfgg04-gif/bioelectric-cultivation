#!/usr/bin/env python3
"""exp260 — THE PAIR-STRUCTURE LEVER (batch 23 item 1; exp259's
structural dual — L237's registered next (a)).

THE OPEN ITEM (L237): the pair-geometry correlation is real (exp254's
J2, exp256's within-host 0.5888) but participation WEIGHTS are not the
lever — the renormalization was inert on the substituted medium and
harmful on the canonical ones. exp254's shift was STRUCTURAL: the
deep-band substitution re-wires WHICH cells carry >= 2 chords (the
pair share 70.1% -> 83.5%). The structural dual: operate on the chord
SET, not the weights.

THE MECHANISM (pre-registered, zero free parameters): the DE-PAIRING
operation — on each substituted row's medium, for every PAIR-JUNCTION
cell that is NOT a pair cell of the host's canonical reference (the
base medium's canon-row classification, the same reference exp259
used), remove chords (lowest-index-first, minimal count) until the
cell's chord degree < 2, i.e. until it leaves the PAIR-JUNCTION class
under the row's own target; removals preserve the medium's canon-value
boundary set (the CANON-BOUNDARY class wins precedence and is never
touched: a chord is removed only if BOTH endpoints stay non-boundary
under the row's target); the operation is deterministic given the
classification, no knobs.

PRE-REGISTERED GATES:

  Q1  THE IDENTITY: on the canonical rows the operation is a NO-OP by
      construction (the reference IS the canonical classification) —
      asserted array-equal on all 12 hosts; and the machinery anchor:
      the un-operated substituted rows reproduce exp243's deposited
      worsts bit-exact (exp256's verification).
  Q2  THE STRUCTURE LEVER: the de-pairing REDUCES the substituted
      rows' pooled worst-err (the same pooled form as exp259: the mean
      over the 36 rows of the arm's worst err) by >= 10%.
  Q3  THE SPECIFICITY: the canonical rows' worst-errs are unchanged
      bit-exactly (the operation's no-op face verified live on the
      canonical media, not assumed).
  Q4  THE DISCIPLINE: exp243's/exp254's deposits READ-ONLY
      sha-recorded byte-unchanged; every removal recorded (the
      per-row removed-chord lists in the deposit); the -60.0 floor
      restored and asserted; deterministic re-run (the substituted
      battery re-run on 6 hosts, bit-identical).

THE BRANCHES (pre-named): Q2 PASS -> PAIR-STRUCTURE-CARRIES (the pair
cost is structural — the exp254 shift's causal face lands); Q2 REFUTE
-> STRUCTURE-INERT (neither weights nor structure move it — the pair
correlation is diagnostic, not causal, deposited honestly).

RUN: exp243's machinery verbatim (exp259's body is the precedent), 12
hosts x 2 arms x 3 seeds x 2 instances; foreground.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp260_pair_structure_lever.json")


def main() -> dict:
    raise NotImplementedError(
        "exp260 body pending — pre-registration commit only")
