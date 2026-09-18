#!/usr/bin/env python3
"""exp254 — THE PAIR-JUNCTION GEOMETRY UNDER SUBSTITUTION (exp252's
registered next; the interior cost's mechanism; ledger L232).

THE OPEN ITEM (L230): the deep-band substitution's cost is
INTERIOR-carried (85% PAIR-JUNCTION — exp208's structure-coupled
class). THE MECHANISM: the substituted medium's pair structure — the
deep-band swap (-60.0 rung) changes which cells are PAIR-JUNCTION
(cells whose pair partner's junction differs) and what their errs are.

PRE-REGISTERED GATES:

  J1  THE PAIR SHIFT: the pair-junction cell count on the substituted
      medium vs the canonical medium at the argmax host (exp243's
      machinery verbatim: exp208's classify on both media) — the shift
      recorded.
  J2  THE ERR LOCATION: the substituted medium's errs on its pair
      cells vs its canon-boundary cells vs the rest (the three-way err
      split on the substituted medium) — the gate: the pair cells'
      mean err exceeds the rest's (the cost lives where the geometry
      changed).
  J3  THE DISCIPLINE: exp243's deposit READ-ONLY sha-recorded
      byte-unchanged, deterministic, zero rejections.

THE BRANCH (pre-named): J2 PASS -> PAIR-GEOMETRY-CARRIED (the interior
cost is the pair geometry's — the deep band's swap re-wires the pair
structure and the reader's price follows it); J2 REFUTE -> the cost is
diffuse (deposited honestly).

RUN: the classify battery + the arithmetic; minutes.
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
OUT = os.path.join(ROOT, "results", "exp254.json")


def main() -> dict:
    raise NotImplementedError(
        "exp254 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
