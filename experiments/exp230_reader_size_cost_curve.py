#!/usr/bin/env python3
"""exp230 — THE READER SIZE-COST CURVE (L204's registered next).

The reader's worst-err profile is graded in n: 1.45 (random, n=100),
0.62 (structured, n=400), 3.42 (structured, n=1000). The registered
measurement: the size-cost curve as ONE deposited line — the worst-err
vs n profile at n = 100/200/400/700/1000 on the path constructor (the
A_CHAIN family), 5 target classes x 3 seeds per n, the 6.0 bar
unchanged; PLUS the E1 checker repair (the completeness predicate
rebuilt from the deposited grid definition, re-run as a hygiene-only
pass — no gate rewrite).

========================= pre-registration =========================
Committed BEFORE any run. Instruments: exp225/exp227's sweep machinery
verbatim (the production scoped read, the target classes, the 3
seeds); the ns (pre-named): 100, 200, 400, 700, 1000; the target
classes per exp225's pre-named list; the floor discipline per
exp218's exp169-import restore VERBATIM (disclosed).

GATES (each evaluated exactly once):
  GATE-N1 (the curve) 5 ns x 5 target classes x 3 seeds decode with
           zero rejections, every err finite; the curve (worst-err
           and mean-err vs n) deposited as one line.
  GATE-N2 (the bar) every err < 6.0 at every n (the reader holds
           across the whole measured size axis).
  GATE-N3 (the fit) the log-log slope of worst-err vs n deposited
           (the scaling exponent, zero fitting — one OLS line, the
           value disclosed); the branch named: SUB-LINEAR (slope
           < 1) / LINEAR (1 <= slope < 2) / SUPER-LINEAR (>= 2).
  GATE-N4 (hygiene) zero rejections; all finite; the floor
           discipline asserted and disclosed; the completeness
           predicate built from the grid definition (the exp227 E1
           repair — hygiene only).
NO post-hoc tuning. --smoke permitted (n=200, 1 target), discarded.
DEPOSIT: results/exp230_reader_size_cost_curve.json
RUN: python3 -m experiments.exp230_reader_size_cost_curve [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results",
                   "exp230_reader_size_cost_curve.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
