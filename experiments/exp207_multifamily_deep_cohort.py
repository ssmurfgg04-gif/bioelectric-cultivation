#!/usr/bin/env python3
"""exp207 — THE MULTI-FAMILY DEEP COHORT (L179's registered next).

exp194's T2 refute quantified the layout-family ceiling: within the
MULTI family (6 shifts x 3 width scales x 3 depth patterns) the
cohort's max nearest-other distance is 39.33 vs the bar 76.668, and
the frozen-72 counterfactual maxes at 73.98 < 82.288. The registered
test: deep constructions from OUTSIDE the MULTI family — a
multi-family cohort (zone counts 1-4 x independent layouts, the
corpus's own layout diversity as the construction source) — does ANY
constructible deep program clear the bar, or does the funnel's
novelty discipline refuse the deep band as a CLASS?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp194's machinery verbatim
(the extended-library build, the funnel, the disclosed self-excluded
reading, the exp189-format trace table — reuse exp194's module
functions where importable); the cohort source (pre-named, zero
fitting): 40 deep programs drawn from the exp182-style target
generator's OWN construction (rng default_rng(207207); zone count
k ~ {1: 10, 2: 12, 3: 10, 4: 8} across 40 draws; each zone
(start ~ U(0.02, 0.80), width ~ U(0.08, 0.16), value ~ U(-60, -15)
with >= 2 zones <= -40 — the deep-band constraint, regenerated on
violation), rounded 1 dp; every program's f = spec_target_n, canon
asserted per program) joined to the frozen 72 = a 112-member library;
bars RE-DERIVED before selection.

GATES (each evaluated exactly once):
  GATE-M1 (the build) 40 multi-family deep programs built outside
           the MULTI family (structurally asserted: none is a MULTI
           shift/width variant — its zone triples differ from every
           MULTI-family program's); canon asserted per program; the
           112-member library bars re-derived and deposited before
           selection.
  GATE-M2 (the class question) the per-program self-excluded
           nearest-other distances + the frozen-72 counterfactual
           deposited (the exp189 trace format); the branches:
           SOME-CLEAR (>= 1 program > N*_lib-112), CLASS-REFUSED
           (0/40 and the max counterfactual < the frozen bar — the
           funnel refuses the deep band as a class at any layout).
  GATE-M3 (if SOME-CLEAR) the survivors pushed through the funnel's
           splice stage and the clause walk at the deep targets
           (exp176's sections, checksummed): the delivered-10's
           deep-target prices deposited; zero rejections.
  GATE-M4 (hygiene) zero rejections in the census; the floor pin
           asserted; the manifest (40 triples + f_sha256) deposited
           FIRST.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp207_multifamily_deep_cohort.json
RUN: python3 -m experiments.exp207_multifamily_deep_cohort [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp207_multifamily_deep_cohort.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
