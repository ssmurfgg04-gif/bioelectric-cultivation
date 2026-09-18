#!/usr/bin/env python3
"""exp253 — THE DEG-WEIGHTED AGGREGATION (exp251's registered next; the
response-law form's zero-knob unifier; ledger L231).

THE OPEN ITEM (L229): the rank and the boundary PULL APART across the
aggregation forms (population: rank 0.9554 / boundary 18/27; worst-cell:
0.9359 / 21/27). THE ZERO-KNOB UNIFIER: the DEG-WEIGHTED RMS — the
theta-term aggregated with the cells' junction participation as the
weights (theta_term = sqrt(sum deg_i * drag_i^2 / sum deg_i)): the drag
enters the pattern error weighted by the cell's coupling — no fitting,
the weights are the substrate's own degrees. The two prior forms are
the degenerate limits (worst-cell = the max; population = the flat
weights), so the deg-weighted form INTERPOLATES mechanistically.

PRE-REGISTERED GATES:

  W1  THE BOUNDARY: the deg-weighted quadrature pred's boundary
      agreement >= 24/27 on exp233's grid (the bar both prior forms
      missed).
  W2  THE RANK: Spearman >= 0.90.
  W3  THE UNIFIER CLAUSE: the deg-weighted form's boundary agreement
      >= BOTH prior forms' (>= 21/27 — it must not lose to either).
  W4  THE DISCIPLINE: the deposits READ-ONLY sha-recorded
      byte-unchanged, deterministic.

THE BRANCH (pre-named): W1+W3 PASS -> UNIFIED-FORM (the response law's
theta-term is the deg-weighted RMS — the three-channel quadrature law
closes with its aggregation named); W1 REFUTE -> FORM-OPEN (the
aggregation family's two-point interpolation does not close it — the
law's form question stays open with the constraint set widened).

RUN: the deposit re-read + the arithmetic; seconds.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp253.json")


def main() -> dict:
    raise NotImplementedError(
        "exp253 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
