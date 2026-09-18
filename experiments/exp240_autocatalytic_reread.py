#!/usr/bin/env python3
"""exp240 — THE AUTOCATALYTIC RE-READ FIX (the Section 6 item; exp218's
mis-operationalized re-read clause repaired; ledger L216).

THE OPEN ITEM: exp218 landed the cone's self-expansion (self-fueled +
ADD-CAPACITY confirmed, X1+X3) but its re-read clause was
mis-operationalized — the registered intent: after ADD-CAPACITY, the
cone's OWN READ must absorb the added capacity (the read's SUPPORT SET
grows: the new cells' values enter the read's inputs and the read's
coverage grows monotonically); exp218's implementation instead re-
decoded the values (a value-level check, not a support-level one). The
repair is instrument-level: the support-set criterion replaces the
re-decode criterion; exp218's battery re-runs under the repaired
instrument.

THE INSTRUMENT (zero-knob): the cone's read support = the set of cells
whose values the cone's read consumes (exp178's scoped read support
discipline); after each ADD-CAPACITY round (the expansion writes new
cells from the cone's own carried state — exp218's self-fueled
protocol verbatim), support(new) must strictly contain support(old)
and the new cells' read-back must match their written values (the
absorption check).

PRE-REGISTERED GATES:

  A1  THE ABSORPTION: after every ADD-CAPACITY round, the read's
      support strictly grows and the new cells read back their written
      values (support monotone across all rounds x 3 arms x 3 seeds).
  A2  THE SELF-FUEL: the expansion continues for the pre-named 6
      rounds WITHOUT external writes (each round's plan sourced from
      the cone's own carried state, exp218's protocol) with the
      interior errs sub-mV (the 6.0 bar only at the boundary per
      exp223/exp228's structural finding).
  A3  THE REPAIR DISCLOSURE (the mis-operationalization named): exp218's
      re-decode criterion and this support criterion are compared on
      the SAME battery — the cases where they disagree are counted and
      deposited (the repair's bite made explicit; the gate records the
      disagreement rate, zero-tolerance on silence).
  A4  THE DISCIPLINE: the P6 provenance locks (exp223's Y2 class) hold
      through the repaired instrument (zero drift), the floor
      save/restore asserted.

THE BRANCH (pre-named): A1+A2 PASS -> AUTOCATALYTIC-CLOSED (the
cone's self-expansion axis CLOSES with the repaired clause — the
Stage 4 autocatalytic item lands); A1 REFUTE -> NOT-ABSORBED (the
added capacity stays outside the read's support — the cone cannot
read its own additions, the honest limit).

RUN: 6 rounds x 3 arms x 3 seeds + the A3 comparison; serial, BLAS
pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp240_autocatalytic_reread.json")


def main() -> dict:
    raise NotImplementedError(
        "exp240 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
