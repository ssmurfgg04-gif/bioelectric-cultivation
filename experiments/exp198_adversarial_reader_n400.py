#!/usr/bin/env python3
"""exp198 — THE UNIVERSAL READER AT SCALE (adversarial media x the
size law).

The universal reader's last open class: adversarial media at n=400 —
exp181's four-cell adversarial cohort rebuilt at n=400 (the size law's
class), 4 cells x 25 instances x seeds (1,2,3).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp181's cohort machinery verbatim (CornerMedium at n=400), exp178's scoped arm, the -35.0 pin.

GATES (each evaluated exactly once):
  GATE-A1 (build + decode) 100 adversarial instances at n=400
           decode with zero rejections through the production
           scoped arm (the CornerMedium construction at n=400,
           exp166's generator verbatim with n=400).
  GATE-A2 (the scale bar) the pooled adversarial median <= 1.30
           (the U2 bar); the size law's prediction priced: the
           n=400 adversarial median vs exp181's n=100 median 0.545
           — the ratio deposited against exp185's monotone law
           (predicted ratio ~ the n-law's, recorded not gated).
  GATE-A3 (the tail) above-bar instances tabulated per cell; the
           tail's ownership deposited (characterization gate).
  GATE-A4 (hygiene) per-cell f_max classifications deposited; pin
           asserted; zero cross-arm anomalies.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp198_adversarial_reader_n400.json
RUN: python3 -m experiments.exp198_adversarial_reader_n400 [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp198_adversarial_reader_n400.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
