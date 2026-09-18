#!/usr/bin/env python3
"""exp256 — THE ROW-LEVEL PAIR REGRESSION (exp255's registered next, L233;
batch 22 item 1).

THE OPEN ITEM (L233): the boundary geometry drives the CANONICAL rows'
cost across hosts (rho 0.8574) but the deep-band substitution BREAKS
that dependence (rho 0.1374) — exp254's pair-structure mechanism
operating at the ROW level, not the host level. The per-host records
carry only the argmax decompositions; the row-level regression needs
per-seed rows for MANY hosts.

THE INSTRUMENT (exp243's machinery verbatim, zero new knobs): run the
per-seed decomposition battery — the 12 candidate hosts x the two media
(the canonical P1/P2 battery medium vs the P3 deep-band substituted
medium) x 3 seeds (exp142's seeds) — recording each row's per-class
decomposition (exp208's classify: CANON-BOUNDARY / PAIR-JUNCTION /
INTERIOR, precedence intact) and the row's worst err. 72 rows.

PRE-REGISTERED GATES:

  R1  THE ROW-LEVEL REGRESSION: Spearman(per-row PAIR-JUNCTION count,
      per-row worst err) across the 72 rows >= 0.5 (the pair structure
      carries the cost AT THE ROW LEVEL, where exp255 located it).
  R2  THE SPECIFICITY: the row-level pair count predicts the
      substituted (P3-medium) rows' errs BETTER than the canonical
      rows' (rho_P3 > rho_canon on the same 36-row halves) — the
      row-level mirror of exp255's host-level inversion.
  R3  THE HOST-LEVEL NULL SHARPENED: within-host rank correlation
      (Spearman computed per host over its own 6 rows, pooled via the
      tied average-rank OLS on within-host ranks) — the row-level
      driver must survive CONTROLLING for host identity (the null:
      the host-level boundary count alone explains the rows).
  R4  THE DISCIPLINE: exp243's deposit READ-ONLY sha-recorded
      byte-unchanged; deterministic (re-run bit-identical); the
      -60.0 floor restored and asserted at exit after any exp169
      import.

THE BRANCHES (pre-named): R1 PASS -> ROW-PAIR-CARRIES (the pair
geometry is the row-level driver — exp254's mechanism measured at its
own scale); R1 REFUTE -> ROW-DRIVER-ABSENT (the row-level cost has a
different structure than pair counts — deposited honestly).

RUN: 72 scoped reads + decompositions (exp243's battery ran 138.5 s for
48 candidates; this is comparable), foreground or runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp256_row_pair_regression.json")


def main() -> dict:
    raise NotImplementedError(
        "exp256 body pending — pre-registration commit only")
