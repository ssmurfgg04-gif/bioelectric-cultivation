#!/usr/bin/env python3
"""exp184 — THE DEEP-PROGRAM LIBRARY COHORT (the library sent to the band).

exp179's registered next (L158): the deep-delivery failure is upstream
of delivery — the pool's members carry MIXED-VALUE programs while the
deep targets demand UNIFORM-deep patterns, and the U(-60,-15) per-zone
library draw makes those vanishingly rare. exp172 wrote uniform-deep
patterns by direct construction, bypassing the library. THIS
EXPERIMENT pushes all-deep library members through the SAME
splice/funnel machinery and re-runs the clause delivery.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Cohort, bars, and gates are fixed now.

THE COHORT (disclosed construction, zero fitting):
  all-deep library members: exp172's uniform-rung construction as
  LIBRARY PROGRAMS — for each rung in {-40, -45, -50, -55, -60} and
  each of 3 zone-layout ladders (the MULTI program's zone spans,
  shifted +i cells i = 0..2: the exp172 instance discipline), one
  member program (zones all at the rung) — 15 members — joined to
  exp141's 72-member library as a 87-member extended library. The
  splice family, funnel, and N* bars RE-DERIVED on the extended
  library (structure bars: N*_lib from the library's pairwise
  distances via the deposited machinery, N*_splice via exp146's
  splice_family_bar, N*_pool before selection — computed, not
  assumed). Search seed 141. The R_W clause and cap 10 as exp168's
  B3. The clause delivery = exp179's price-ranked walk (ranked
  ascending by mean composed decode err over the DEEP target set,
  keep iff min pairwise D > N*_pool-extended, stop at 10).

GATES (each evaluated exactly once):
  GATE-X1 (extended pipeline integrity) the extended library builds
           (87 members), the splice family + funnel re-derive with
           zero rejections, and the three N* bars are deposited
           BEFORE selection (bars_deposited_before_selection).
  GATE-X2 (the deep members survive the funnel) >= 10 of the 15
           all-deep members are in the 96-eligible pool (the
           machinery does not discard the band).
  GATE-X3 (deep delivery) the clause's delivered-10 at the deep
           target set: >= 9/10 with decode < 6.0 AND hold < 6.0 on
           3/3 seeds at EVERY rung; zero rejections; emission mode
           repriced_full everywhere (audit_only_fallback must NOT
           fire — the L143 retirement holds when the library serves
           the band).
  GATE-X4 (the old operating point) the clause's delivered-10 at
           exp150's own targets: C1-C4 ALL PASS (the quality bars
           hold on the extended library too).

NO post-hoc tuning. --smoke (extended-library build + bars only)
permitted, discarded. Deposit: results/exp184_deep_library.json
Jobs: bars | deep | old
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

DEEP_RUNGS = [-40.0, -45.0, -50.0, -55.0, -60.0]
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141

OUT = os.path.join(ROOT, "results", "exp184_deep_library.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP176 = os.path.join(ROOT, "results", "exp176_deep_band_search.json")
DEP179 = os.path.join(ROOT, "results", "exp179_target_aware_delivery.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "deep", "old", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
