#!/usr/bin/env python3
"""exp255 — THE PAIR-COUNT COST REGRESSION (exp254's registered next;
the pair-structure's causal face; ledger L233).

THE OPEN ITEM (L232): the deep-band substitution's cost is the pair
geometry's. THE CAUSAL TEST (zero new simulation): across exp243's
12 candidate hosts, the per-host pair-junction share (the deposits'
own class-count records: the argmax-class P3 rows' decompositions per
host) vs the per-host worst err (the deposits' candidate records) —
one regression, the pair-share as the cost predictor.

PRE-REGISTERED GATES:

  G1  THE REGRESSION: Spearman(pair-share, worst-err) across the 12
      hosts >= 0.5 (the pair structure carries the cost across hosts).
  G2  THE SPECIFICITY: the pair share predicts the P3 (substituted)
      rows' worsts BETTER than it predicts the P1/P2 (canonical) rows'
      worsts (the specificity clause — the cost predictor is specific
      to the substitution).
  G3  THE DISCIPLINE: exp243's deposit READ-ONLY sha-recorded
      byte-unchanged, deterministic.

THE BRANCH (pre-named): G1 PASS -> PAIR-COUNT-PREDICTS (the causal
face lands — the reader's cost is a function of the pair structure);
G1 REFUTE -> the host-level cost is not pair-count-determined
(deposited honestly).

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
OUT = os.path.join(ROOT, "results", "exp255.json")


def main() -> dict:
    raise NotImplementedError(
        "exp255 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
