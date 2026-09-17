#!/usr/bin/env python3
"""exp200 — THE CANON-BOUNDARY RESIDUAL PRICED BY THE PRODUCTION
GROUPING READ (L169's registered next).

L169's registered edge: the conditioned ensemble localizes WHERE the
grouping is audible (the k=3 stratum); the remaining question is the
CANON-BOUNDARY residual (L140's 3 cells — exp155's J1 kept 3 breaking
F3 canon-boundary rings where flip-quiet frontier discipline cannot
exclude the junction without excluding the boundary) — price it with
the production read.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp155's ring battery rebuilt
(its 12-ring construction and seed rule VERBATIM — 6 F1_zone_tail +
6 F3_canon_boundary rings; J2's replay discipline); the production
grouping read = exp163's contrast machinery with exp193's conditioned
arm (the production dispatch, k=3-conditioned statistic, additive
wiring asserted); the -35.0 pin asserted throughout.

GATES (each evaluated exactly once):
  GATE-R1 (replay) exp155's 12 rings replay bit-exactly vs its
           deposit (J2's discipline: the 9 repaired rings bit-exact;
           the 3 breaking F3 rings reproduce their deposited breaking
           verdicts).
  GATE-R2 (pricing) the production grouping read priced at EVERY
           ring's operating point; per-ring conditioned stats
           deposited; zero rejections; the unconditioned path
           replays bit-exactly where exp163's deposit carries
           records.
  GATE-R3 (localization) the pre-named contrast: the boundary class
           (the 3 breaking F3 rings) vs the interior class (the
           passing rings) on the conditioned stat —
           LOCALIZED (boundary mean > 2x interior mean),
           DIFFUSE (1x < ratio <= 2x),
           ABSENT (ratio <= 1x).
  GATE-R4 (hygiene) pin save/restore asserted; zero rejections;
           all stats finite.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp200_canon_boundary_grouping.json
RUN: python3 -m experiments.exp200_canon_boundary_grouping [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp200_canon_boundary_grouping.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
