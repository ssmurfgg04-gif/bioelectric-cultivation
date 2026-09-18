#!/usr/bin/env python3
"""exp252 — THE DEEP-BAND SUBSTITUTION'S COST (exp243's registered
next; the conjunction's price decomposed; ledger L230).

THE OPEN ITEM (L221): exp243's A2 named the conjunction's price — the
deep-band substitution (P3) triples the reader's worst cell (3.68 vs
the structured-only 0.62 and the random 1.45). THE DECOMPOSITION: where
the 3.68 lives — the boundary vs the interior — via exp208's
machinery on the substituted rows (exp243's deposit carries the
argmax's decomposition records; this experiment re-reads them and
EXTENDS with the per-rung split: the substituted deep-band rows' errs
vs the canonical rows' errs, each decomposed into the canon-boundary
and interior shares).

PRE-REGISTERED GATES:

  B1  THE COST'S ADDRESS: the 3.68's decomposition deposited (the
      boundary share vs the interior share of the substituted rows'
      sum-of-squares) — the gate is the record (zero silence).
  B2  THE RUNG SPLIT: the substituted deep-band rows' worst err vs the
      canonical rows' worst err (both from exp243's deposit, re-read)
      — the gate: the deep-band rows' worst exceeds the canonical
      rows' worst (the substitution IS the cost's carrier, pre-named
      expectation).
  B3  THE DISCIPLINE: exp243's deposit READ-ONLY (sha-recorded,
      byte-unchanged), deterministic.

THE BRANCH (pre-named): the cost is boundary-dominant (the boundary
share >= 0.5) -> BOUNDARY-CARRIED (the conjunction's price is the
boundary signature amplified by the substitution — consistent with
exp226/exp229/exp245's boundary frontier); interior-dominant ->
INTERIOR-CARRIED (the deep band's geometry itself costs — the honest
surprise).

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
OUT = os.path.join(ROOT, "results", "exp252.json")


def main() -> dict:
    raise NotImplementedError(
        "exp252 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
