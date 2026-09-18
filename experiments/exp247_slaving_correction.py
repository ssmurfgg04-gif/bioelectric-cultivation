#!/usr/bin/env python3
"""exp247 — THE THETA-TERM'S SLAVING CORRECTION (exp246's registered
next; the two-channel law's missing coupled-mode term; ledger L225).

THE OPEN ITEM (L224): the quadrature law's 6 boundary misses are ALL the
theta-term over-predicting on the torus at gamma>=4 (pred 11.45 vs
measured 4.80-5.92): the homogenization number assumes the identity
layer homogenizes at the UNCOPLED rate mu*deg — but theta's dynamics
are SLAVED to the coupled (V,theta) system, whose homogenization mode
decays at the COUPLED slow eigenvalue, not mu*deg. THE ZERO-KNOB
CORRECTION: for a theta-mode with Laplacian eigenvalue lambda (= deg,
exp79's own per-cell proxy), the coupled 2x2 block on the mode
amplitudes (v, w) is [[-(gamma+lambda_G), gamma], [eps, -(eps+mu*lambda)]]
with lambda_G = lambda*G_GAP — the homogenization rate = |slow
eigenvalue| of this block, EXACT from the linear algebra, no fitting.
exp79's raw form is the limiting case and is recovered as a sanity
anchor.

PRE-REGISTERED GATES:

  C1  THE ANCHOR: the corrected theta-term reproduces exp79's deposited
      grid errs bit-consistently on the gamma=0.25 column (the
      plateau's own regime) within the deposit's 2dp rounding.
  C2  THE BOUNDARY CLOSES: exp233's 27-point grid re-read under the
      corrected quadrature pred — the writability boundary agreement
      rises from 21/27 (77.8%) to >= 24/27.
  C3  THE RANK HOLDS: the corrected quadrature pred keeps Spearman
      >= 0.90 (the Q1 result must survive the correction).
  C4  THE DISCIPLINE: exp233's and exp79's deposits consumed READ-ONLY
      (sha-recorded, byte-unchanged), the arithmetic deterministic,
      re-run bit-identical.

THE BRANCH (pre-named): C2 PASS -> SLAVING-CORRECTED (the law's
theta-term gains its coupled-mode form; the composition names with the
boundary closed); C2 REFUTE -> RESIDUAL-NAMED (the torus face is not
the slaving — the misses' driver named for the next instrument).

RUN: the deposit re-reads + the 2x2 eigensolves; seconds.
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
OUT = os.path.join(ROOT, "results", "exp247.json")


def main() -> dict:
    raise NotImplementedError(
        "exp247 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
