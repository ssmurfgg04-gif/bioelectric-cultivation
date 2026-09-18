#!/usr/bin/env python3
"""exp213 — THE BOUNDARY ARM AT n=400 (L185's registered next).

exp208's ablation NAMED the c6 tail's new rule class: the excess lives
at the CANON-BOUNDARY cells (+0.574 mV; interior 0.000 exactly) — the
boundary phenomenon independently reproducing exp200's n=100
localization. L185's registered next: the exp205/exp210 composed
machinery aimed at the corner battery's boundary cells — the
plane-resolved read face armed ONLY at the boundary cells of the 25
tail instances — the pre-named bar being the tail's 1.30 bar crossed
by a boundary-only arm with the interior bit-exact (exp205's identity
clause at n=400).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's battery verbatim (the
c6 cell's 25 instances, seeds (1,2,3), the scoped read); exp208's
decomposition machinery verbatim (the CANON-BOUNDARY classification,
the mV^2 accounting identity); the arm (pre-named, zero knobs): at
each tail instance the decoded V's boundary-cell values are replaced
by the plane-resolved read's emission (exp158's machinery at the
n=400 corner battery: the boundary cells read through the canon-plane
sub-window chain), every interior cell bit-unchanged.

GATES (each evaluated exactly once):
  GATE-B1 (replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 instances x 3 seeds) and exp208's per-class
           decomposition reproduces bit-exactly at the reference.
  GATE-B2 (the arm) the boundary-armed errs for all 25 instances x 3
           seeds; the branch named: REPAIR (median <= 1.30 — the
           tail's bar crossed), IMPROVED (median improved >= 20% vs
           1.40, bar not crossed), NONE.
  GATE-B3 (the identity clause) every interior cell's decoded value
           bit-unchanged by the arm (exp205's identity clause at
           n=400); the arm touches exactly the boundary cells.
  GATE-B4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp213_boundary_arm_n400.json
RUN: python3 -m experiments.exp213_boundary_arm_n400 [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp213_boundary_arm_n400.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
