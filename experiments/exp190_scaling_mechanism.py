#!/usr/bin/env python3
"""exp190 — THE SCALING LAW'S MECHANISM (boundary vs interior).

exp185's registered next (L161): the residual-vs-n curve is MONOTONE
(0.075 -> 1.480) with coverage rho +0.974. Name WHERE the error
lives: zone-boundary cells (labeling resolution) vs zone-interior
cells (value fidelity).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp185's ladder instances (GRID_BASE_SEED + 5000 + 100*r + i), exp94's spec_target_n/labeling_bfs_n, the scoped arm under the -35.0 pin.

GATES (each evaluated exactly once):
  GATE-Q1 (states replay) the n=400/500 read states from
           exp185's deposit (or fresh decodes if states were not
           deposited — disclosed either way), zero rejections.
  GATE-Q2 (the split) per instance: err_boundary (cells within the
           zone-boundary band, width = the labeling resolution exp94
           uses, disclosed) vs err_interior (the rest); the ratio
           deposited per rung.
  GATE-Q3 (the mechanism clause) pre-named: BOUNDARY if
           err_boundary > 2x err_interior pooled at n >= 400;
           INTERIOR if the reverse; MIXED otherwise. All complete.
  GATE-Q4 (the resolution test) the boundary band width scaled 2x
           as a disclosed probe: if err_boundary collapses into the
           band, the law is labeling resolution (registered); else
           interior-dominated. Recorded, no bar.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp190_scaling_mechanism.json
RUN: python3 -m experiments.exp190_scaling_mechanism [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp190_scaling_mechanism.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
