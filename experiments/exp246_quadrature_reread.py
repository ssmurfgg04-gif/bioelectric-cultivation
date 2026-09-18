#!/usr/bin/env python3
"""exp246 — THE QUADRATURE THREE-CHANNEL RE-READ (exp233's registered
next; the law's composition form; ledger L222).

THE OPEN ITEM: exp233's F3 REFUTE — the max-form three-channel
prediction pred3 = max(V-term, theta-term, field-term) pooled at
Spearman 0.700 over the (gamma x kappa) grid — while its NON-GATING
quadrature composition pooled at 0.933. exp233's registered next: the
grid re-read under the quadrature form err ~ sqrt(eV^2 + etheta^2 +
efield^2) — the two-channel boundary work's own quadrature precedent —
as the law's correct composition.

THE INSTRUMENTS (frozen, verbatim): exp233's deposited grid (27 points
x 3 seeds x 3 arms — re-read from the deposit, ZERO re-simulation for
the gate arithmetic; the field-term machinery from exp233's body for
the per-point efield term), exp79's V-term and theta-term (the frozen
forms), the quadrature pred: pred_q = sqrt(eV^2 + eT^2 + ef^2) with the
three terms the per-point exp233/exp79 quantities (the V-term
CONTRAST*y/(1+y), the theta-term the homogenization number, the
field-term exp233's field-drag quantity — each the PREDICTED mV
contribution, composed in quadrature).

PRE-REGISTERED GATES:

  Q1  THE QUADRATURE LAW: pred_q tracks the measured errs across the
      deposited grid with Spearman >= 0.90 (exp79 TC-G1's bar) — the
      gate the max-form failed (0.700) and the non-gating quadrature
      preview passed (0.933, now GATED).
  Q2  THE BOUNDARY AGREEMENT: pred_q's writability boundary (pred_q <
      6.0 iff err < 6.0) agrees on >= 80% of the grid points (exp79
      TC-G1's second clause).
  Q3  THE THREE-CHANNEL VERDICT (the composition named): if Q1+Q2 PASS,
      the stack's channel composition is QUADRATURE — the three
      channels' contributions compose as independent RMS terms, not as
      a binding max; the law's form is updated to the quadrature
      three-channel form and the exp233 F3 verdict is REFINED (the
      field channel is real but non-binding: it composes, it does not
      dominate). If Q1 REFUTEs, the composition form stays open — the
      deposited honestly.
  Q4  THE DISCIPLINE: the re-read consumes exp233's deposit read-only
      (byte-unchanged through the re-read, sha-recorded), the
      arithmetic deterministic, re-run bit-identical.

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
OUT = os.path.join(ROOT, "results", "exp246_quadrature_reread.json")


def main() -> dict:
    raise NotImplementedError(
        "exp246 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
