#!/usr/bin/env python3
"""exp191 — THE DEEP POLE READOUT'S OPERATING ENVELOPE (blockade
depth).

exp186's registered next (L162): the feature HELPS at r = 0.05. The
disclosed sweep r in {0.05, 0.2, 0.5} (TRUNK/DEEP families, ARM-DEEP
vs ARM-PROD, exp186's protocol verbatim): is the deep pole readout a
BLOCKADE-REGIME feature?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp171/exp186's run_engine protocol verbatim; core.M33_LINE rebinding (exp174's mechanism).

GATES (each evaluated exactly once):
  GATE-R1 (replay) the r = 0.05 cell reproduces exp186's Z3
           deltas bit-exactly (TRUNK -4.3523, DEEP -5.8913).
  GATE-R2 (the sweep) per r in {0.2, 0.5}: ARM-PROD vs ARM-DEEP on
           TRUNK/DEEP, seeds (1,2,3), the signed deltas deposited;
           HEAD/LINE bit-identical across arms at every r.
  GATE-R3 (the envelope clause) pre-named: REGIME-FEATURE iff the
           deltas shrink monotonically toward 0 as r grows (help at
           deep blockade, vanishing at shallow); PERSISTENT if they
           hold across r; INVERTED if any r flips sign. All
           complete.
  GATE-R4 (hygiene) rebind save/restore asserted per arm per r;
           zero non-finite.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp191_pole_envelope.json
RUN: python3 -m experiments.exp191_pole_envelope [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp191_pole_envelope.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
