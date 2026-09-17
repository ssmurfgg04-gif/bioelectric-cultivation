#!/usr/bin/env python3
"""exp189 — THE FUNNEL EXCLUSION ANATOMY (which stage kills the deep
programs?).

exp184's registered next (L160): the funnel excludes ALL 15 all-deep
members (0/15 eligible) even when the library contains them. Trace
each through every stage and name the excluding criterion.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp184's extended-library machinery verbatim (import from its module or copy its build block); exp141/exp146/exp150's funnel functions.

GATES (each evaluated exactly once):
  GATE-P1 (per-member trace) each of the 15 deep members traced
           through: (a) lib-novel distance vs N*_lib (the member's
           nearest-library distance, the criterion value, PASS/FAIL);
           (b) splice-family membership (in/out, the splice count);
           (c) splice-clear price vs N*_splice. The full trace table
           deposited (15 rows x 3 stages).
  GATE-P2 (the excluding stage NAMED) exactly one stage carries the
           exclusion for the majority (>= 8/15): the deposit names
           it and the criterion's per-member margin distribution.
  GATE-P3 (the mechanism clause) the pre-named branches: (i) DISTANCE
           failure — deep programs too similar to each other (the
           15 members' pairwise distances concentrated below the
           novelty bar); (ii) OUT-COMPETED — the 72 outrank them at
           a rank-cut; (iii) SPLICE-PRICED — their splices price
           above N*_splice. All branches complete the gate.
  GATE-P4 (hygiene) zero rejections in any price computed; the bars
           re-derive bit-identically to exp184's deposit.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp189_funnel_exclusion_anatomy.json
RUN: python3 -m experiments.exp189_funnel_exclusion_anatomy [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp189_funnel_exclusion_anatomy.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
