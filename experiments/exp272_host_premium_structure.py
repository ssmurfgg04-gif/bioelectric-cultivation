#!/usr/bin/env python3
"""exp272 — THE HOST PREMIUM STRUCTURE (batch 30; L249's registered
next (a) — zero new simulation).

THE OPEN ITEM (L249): the one-zone premium is systematic (+0.6561
mean, 36/36 rows positive) and its shelf height is a deterministic
HOST property (host share 0.8143). What prices the shelf? The
standing candidate: the host's own boundary geometry (exp255's
instrument — the canon-boundary count carried the CANONICAL cost at
rho 0.8574 across hosts).

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
per-host premium means (12 values, exp271's deposited premium grid)
regressed against the host's canon-boundary count (exp243's classes
records, the exp255 instrument) — Spearman + the OLS slope; the
second regressor the docstring pre-names: the host's deep-band
premium at the SATURATED dose (exp270's d>=3 rows mean per host —
exp270's deposit carries the per-dose means pooled; the per-host
saturated means need exp256's deposited i0 rows vs the canon rows,
both already in the deposits — the shelf-to-shelf regression: does
the one-zone shelf price predict the multi-zone shelf price?).

PRE-REGISTERED GATES:

  H1  THE GRIDS: exp271's 36-row premium grid complete (12 hosts x 3
      seeds), the per-host means computed; exp243's boundary counts
      byte-verified; exp256's rows complete.
  H2  THE BOUNDARY PRICE: Spearman(per-host premium mean, the host's
      canon-boundary count) >= 0.5 (the shelf's price is the host's
      boundary geometry — the exp255 law extends to the
      substitution's categorical face).
  H3  THE SHELF-TO-SHELF: Spearman(one-zone premium mean, the
      multi-zone premium mean) across the 12 hosts >= 0.5 (the two
      shelves are the same host property at different depths — the
      step is a host-fixed price with a depth offset).
  H4  THE DISCIPLINE: exp271's/exp256's/exp243's deposits READ-ONLY
      sha-recorded byte-unchanged; deterministic; no wall-clock
      fields; the -60.0 floor asserted at exit.

THE BRANCHES (pre-named): PRICE-GEOMETRIC (H2 passes) /
PRICE-HOST-OTHER (H2 fails — the shelf's price is a host property
OUTSIDE the boundary geometry, named honestly; H3 reported either
way).

RUN: a deposit re-read + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp272_host_premium_structure.json")


def main() -> dict:
    raise NotImplementedError(
        "exp272 body pending — pre-registration commit only")
