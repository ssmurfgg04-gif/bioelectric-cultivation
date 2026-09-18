#!/usr/bin/env python3
"""exp245 — THE BOUNDARY RESIDUAL'S GAUGE-AWARE RE-DECOMPOSITION (the
Section 6 item; exp229's ~70% unexplained boundary structure; ledger
L221).

THE OPEN ITEM: exp226/exp229's three-way rank-variance attribution of
the boundary residual (step 0.241 / curvature 0.058 / unexplained
0.701) left ~70% of the rank variance unexplained. THIS BATCH'S
discovery re-opens the decomposition: exp234 proved the pattern layer
carries an EXACT GAUGE MODE (the uniform offset — zero information,
conserved), and exp239 carried the gauge quotient into the certificate
machinery. The residual r_i (exp208's decomposition-row mV^2 summands)
is an ABSOLUTE-RMS object — it contains the gauge share. The zero-knob
refinement: re-decompose exp226's residual on the GAUGE QUOTIENT and
re-run the three-way attribution (step / curvature / unexplained) on
the gauge-aware residual.

THE INSTRUMENTS (all frozen, verbatim): exp226's machinery (the c6
battery, the replay anchors, the residual rows, the D_i = 0 points
kept), exp226's step instrument S_i, exp229's curvature instrument
K_i; the NEW element is the residual's gauge projection: r_i^gauge =
r_i computed on the gauge-quotiented fields (the (V, theta) fields
projected: x = y - (y.g)g with g the uniform direction — the mV^2
summands recomputed from the projected fields; the summand is
quadratic so the projection's cross-terms are carried exactly, no
approximation). The attribution: the same OLS-on-tied-ranks method
exp229 fixed in its body, re-run on (r_i^gauge, S_i, K_i).

PRE-REGISTERED GATES:

  G1  THE CONTINUITY: exp226's machinery verbatim reproduces exp226's
      deposit bit-exactly (the replay anchors — exp229's K1 class).
  G2  THE GAUGE SHARE: the gauge share of the residual's rank variance
      recorded (the R^2 of the gauge direction alone on the tied
      ranks); the gate is the RECORD (zero-tolerance on silence), the
      pre-named expectation: the share is small (the gauge is uniform,
      the residual is boundary-concentrated — but the absolute-RMS
      summand carries SOME gauge).
  G3  THE RE-ATTRIBUTION: the three-way split on the gauge-aware
      residual (step / curvature / unexplained — shares sum to 1,
      exp229's method); the gate: the split recomputed and deposited;
      the FINDING names whether the unexplained share DROPS (the gauge
      was eating attribution) or STANDS (~70% confirmed gauge-free).
  G4  THE DISCIPLINE: zero rejections, all finite, the -35.0 pin
      save/restore asserted (the exp169-import restore disclosed).

THE BRANCH (pre-named): the unexplained share drops below 0.6 ->
GAUGE-EATS (the 70% was partly the gauge — the boundary frontier's
standing measure UPDATED); the share stands >= 0.65 ->
GAUGE-FREE-70 (the unexplained structure is genuinely not-gauge — the
frontier's hardest core confirmed).

RUN: exp226's battery verbatim + the projected recomputation; serial,
BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp245_boundary_gauge.json")


def main() -> dict:
    raise NotImplementedError(
        "exp245 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
