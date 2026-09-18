#!/usr/bin/env python3
"""exp264 — THE APOP CHANNEL ACTIVATION (batch 24 item 3; L239's
registered next (c) — the FIFTH activation under the exp257 schema,
ch6 "apop", the paper's apoptosis-as-morphogenetic-signal face).

THE OPEN ITEM: the paper's census names apoptosis as a morphogenetic
signal — ABSENT from the stack; the exp257 schema gave it native
state (ch6, dormant). The stack-native pre-named instrument: the
apop channel MARKS the cells at the extreme band of the theta
distribution (the death-competent state: sustained extreme
depolarization or the wound's blastema state — the pre-named rule:
a cell is marked iff its theta sits in the battery-wide extreme
decile at settle time [both tails, the zero-knob quantile rule] OR
the cell sits in the amputation's blastema band); the mark is
state (carried in ch6), the readout tests whether the marked set
localizes the boundary excess, the coupling (gated on the readout)
lets the mark modulate the cell's identity commitment noise (the
M26b face: the death signal's morphogenetic role is to RELAX the
marked cell's commitment toward the local mean — the pre-named
form: the marked cells' commitment noise multiplied by
(1 - g_apop) at the grid {0, 0.25, 0.5, 1.0}).

PRE-REGISTERED GATES (the exp258/exp261/exp263 mold):

  A1  THE DORMANT IDENTITY: g_apop = 0 reproduces the production
      decode bit-exactly on the c6 battery (75/75, the X1 form
      verbatim).
  A2  THE READOUT (zero-risk, read-only): the marked set's boundary
      enrichment — the marked cells' CANON-BOUNDARY membership rate
      vs the unmarked cells' (the pre-named enrichment ratio >= 2.0
      gates the coupling; Fisher-type count comparison recorded,
      the ratio is the gate).
  A3  THE COUPLING (only if A2 passes; else SKIPPED-A2-FAIL): the
      marked cells' commitment-noise relaxation at the pre-named
      grid; the gates: the best cell reduces the worst boundary-row
      err >= 10% AND the non-boundary rows' worst-err change <= +5%.
  A4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded; collective.py untouched sha-recorded; the -60.0
      floor restored and asserted; deterministic re-run; no
      wall-clock fields.

THE BRANCHES (pre-named): APOP-CARRIES / APOP-READOUT-ONLY /
APOP-INERT — deposited honestly.

RUN: the c6 battery x the grid; foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp264_apop_activation.json")


def main() -> dict:
    raise NotImplementedError(
        "exp264 body pending — pre-registration commit only")
