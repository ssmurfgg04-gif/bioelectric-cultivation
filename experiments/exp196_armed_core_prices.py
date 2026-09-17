#!/usr/bin/env python3
"""exp196 — THE ARMED-CORE GENERATOR PRICES (the feature's value in
the generator's currency).

exp191's registered next (L167): the exp168 B3 pipeline re-run at
ARM-DEEP (core.M33_LINE rebound -60.0) vs the production split — the
search is target-free so selection is bit-identical; the decode/hold
prices shift where deep identities exist.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp179's pipeline + price-table machinery verbatim; exp186's ARM-DEEP rebinding.

GATES (each evaluated exactly once):
  GATE-W1 (selection identity) the funnel + delivery at seed 141
           BIT-IDENTICAL between arms (the search consults no pole
           channel — proven, not assumed).
  GATE-W2 (the price shift) the delivered cohort's decode/hold
           prices at the deposited targets, ARM-DEEP vs ARM-PROD,
           3 seeds: per-member deltas deposited; the members with
           nonzero deltas counted (the armed feature's footprint).
  GATE-W3 (the direction) the pre-named branch: NET-POSITIVE iff
           the mean delta < 0 (armed helps the generator's own
           targets), NET-NEGATIVE if > 0, NEUTRAL if all |delta|
           < 0.005 (float noise). All complete.
  GATE-W4 (hygiene) rebind asserted per arm; zero rejections both
           arms.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp196_armed_core_prices.json
RUN: python3 -m experiments.exp196_armed_core_prices [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp196_armed_core_prices.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
