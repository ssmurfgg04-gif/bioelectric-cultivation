#!/usr/bin/env python3
"""exp222 — THE COUNTERFACTUAL FUNNEL (L196's registered next).

exp207 (the counterfactual max 84.464 beats the frozen bar 82.288)
and exp220 (the spread cohort's N*_spread 82.259, the P95 NOT
re-tightened at 15x spread) doubly qualify the funnel's refusal: the
block is the STATISTIC'S OWN DEFINITION — the P95 pool includes the
frozen-72 record whose members the statistic is priced against. The
registered test: re-derive the acceptance statistic with the frozen
record's contribution EXCLUDED from its own P95 pool (self-exclusion
made explicit AT THE STATISTIC LEVEL), re-price BOTH deposited cohorts
(exp207's single-regime 40, exp220's spread cohort) under it; the
pre-named branch: the funnel OPENS under self-exclusion, or the
self-tightening is proven at the deepest level.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp207's deposited machinery
verbatim (the N-body record, the 40 x 40 mutual-distance matrix, the
bars N*_lib-112 76.103 / N*_splice-112 16.021 / frozen 82.288);
exp220's deposited spread cohort + selection order verbatim (min pair
84.942, N*_spread 82.259); the COUNTERFACTUAL STATISTIC (pre-named,
zero knobs): the P95 re-computed over the pool with the frozen-72
record's members removed (the pool = the deposited 112-member library
minus the frozen 72's members; the statistic form, the k, and the
distance metric unchanged — exp179's deposited definitions).

GATES (each evaluated exactly once):
  GATE-C1 (the anchors) both deposited cohorts replay: exp207's
           N*_lib-112 76.103 and exp220's N*_spread 82.259 reproduce
           bit-exactly from the deposits before any re-pricing.
  GATE-C2 (the counterfactual bar) the self-excluded statistic's
           value deposited; the branch named: FUNNEL-OPENS (>= 1
           member of either cohort clears the counterfactual bar) /
           SELF-TIGHTENING (0 clear AND the counterfactual bar <=
           the frozen bar's effective threshold on the same pool —
           the exclusion changes nothing).
  GATE-C3 (the attribution) the refusing pairs deposited: for every
           cohort member, its nearest in-pool neighbor and the
           margin to the counterfactual bar — the N-body record's
           final form under the corrected statistic.
  GATE-C4 (hygiene) zero rejections; all finite; the -60.0
           production floor asserted; no per-program tuning.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp222_counterfactual_funnel.json
RUN: python3 -m experiments.exp222_counterfactual_funnel [--smoke] [--job ...] [--out ...]
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
                   "exp222_counterfactual_funnel.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
