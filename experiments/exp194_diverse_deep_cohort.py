#!/usr/bin/env python3
"""exp194 — THE DIVERSE DEEP COHORT (novelty-proof deep members).

exp189's registered next (L165): the deep cohort dies of
SELF-SIMILARITY at the lib-novelty stage. Build deep members with
STRUCTURAL diversity — varied zone layouts/widths (exp172's
construction discipline at 6 layout shifts x 5 rungs = 30 members,
plus 15 mixed-depth members carrying deep+shallow zones) — through
the SAME funnel.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp184's extended-library + clause-walk machinery verbatim; exp189's trace functions for the distance table.

GATES (each evaluated exactly once):
  GATE-T1 (cohort build) 45 diverse deep members built (30
           uniform-rung varied-layout + 15 mixed-depth), canon ==
           wildtype asserted per member, the extended library
           (72 + 45) bars re-derived and deposited before selection.
  GATE-T2 (survival) >= 15/45 deep members in the eligible pool
           (the DISTANCE fix works); the per-member lib-novel
           distances deposited vs exp189's trace table.
  GATE-T3 (deep delivery) the clause's delivered-10 at the deep
           targets: >= 9/10 with decode < 6.0 AND hold < 6.0 on
           3/3 seeds at every rung; zero rejections; no
           audit_only_fallback.
  GATE-T4 (the old point) the clause's 10 at exp150's targets:
           C1-C4 ALL PASS.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp194_diverse_deep_cohort.json
RUN: python3 -m experiments.exp194_diverse_deep_cohort [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp194_diverse_deep_cohort.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
