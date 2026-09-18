#!/usr/bin/env python3
"""exp220 — THE SPREAD-COHORT SELECTION ORDER (L188's registered next).

exp207's N-body finding: the funnel's refusal is the cohort's OWN
DENSITY (each program's nearest sibling sits inside the bar and the
P95 statistic re-tightens around every admission). The registered
question: can a DELIBERATELY SPREAD cohort — max-min selection over
the generator's space (exp179's greedy discipline at the generator's
own bars) — land even ONE member above the moving bar? If the bar
rises to meet every cohort, the funnel's novelty stage is PROVEN
self-tightening and the delivery question moves from construction to
SELECTION ORDER.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp207's build VERBATIM
(exp182's generator at the registered seed 207207, the ladder
{1:10, 2:12, 3:10, 4:8}/40, the deep-band constraint >= 2 zones
<= -40, canon asserted per program, the manifest deposited FIRST);
the bars re-derived BEFORE selection (N*_lib-112 76.103, N*_splice-112
16.021, the frozen bar 82.288 — asserted vs exp207's deposit);
exp179's greedy VERBATIM as the max-min selector: the spread cohort of
40 = the greedy max-min ordering over the 40 programs' pairwise
distances (the exp207 mutual-distance matrix machinery), the selection
order deposited.

GATES (each evaluated exactly once):
  GATE-D1 (the manifest) 40 multi-family deep programs built and
           canon-asserted (exp207's build verbatim, seed 207207);
           the manifest + f_sha256s deposited FIRST; 0 MULTI-family
           clashes.
  GATE-D2 (the spread) the max-min selection order deposited; the
           cohort's min pairwise distance STRICTLY GREATER than
           exp207's single-regime cohort's (the spread is real, not
           nominal); the distance matrices both deposited.
  GATE-D3 (the funnel) the spread cohort priced through the SAME
           funnel (the self-excluded bar N*_lib-112 76.103, the
           counterfactual max vs the frozen 72 82.288); the branch
           named: SOME-CLEAR (>= 1 member clears the self-excluded
           bar) / BAR-RISES (0 clear AND the P95 re-tightened around
           the spread cohort — the self-tightening proof) /
           NEITHER.
  GATE-D4 (hygiene) zero rejections; all finite; the -60.0
           production floor asserted; no per-program tuning.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp220_spread_cohort_selection.json
RUN: python3 -m experiments.exp220_spread_cohort_selection [--smoke] [--job ...] [--out ...]
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
                   "exp220_spread_cohort_selection.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
