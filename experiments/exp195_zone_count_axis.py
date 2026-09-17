#!/usr/bin/env python3
"""exp195 — THE SCALING LAW'S SECOND AXIS (zone-count dose-response).

exp190's registered next (L166): interior value fidelity at fixed n —
1/2/3/4-zone programs x 10 instances at n = 100 and n = 400, the
scoped arm under the -35.0 pin.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp185/exp180's build + scoped_read patterns; MULTI zone-count variants via exp94's AnatomySpec with 1-4 zones (the exp161 ladder).

GATES (each evaluated exactly once):
  GATE-V1 (ladder integrity) 80 instances (4 zone counts x 10 x
           2 sizes) built and decoded, zero rejections, finite.
  GATE-V2 (the dose-response) the err-vs-zone-count curve at each
           size deposited with dispersions; the branch named:
           (i) DOSE-DRIVEN (err rises with zone count at BOTH
           sizes), (ii) SIZE-DRIVEN (flat in zone count at both),
           (iii) INTERACTION (rises at n=400 only). All complete.
  GATE-V3 (the coverage link) support coverage vs zone count per
           size, Spearman deposited — the coverage mechanism's
           other face or its refutation.
  GATE-V4 (hygiene) pin asserted; the n=100/1-zone rung inside
           exp185's deposited n=100 band.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp195_zone_count_axis.json
RUN: python3 -m experiments.exp195_zone_count_axis [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp195_zone_count_axis.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
