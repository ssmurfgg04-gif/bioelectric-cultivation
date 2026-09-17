#!/usr/bin/env python3
"""exp176 — DEEP-BAND GENERATOR SEARCH (the search sent to the band).

exp172's registered next (L151): "the band is writable but the
GENERATOR has never BEEN SENT there — the search's own target
families have never carried a deep-band target; next: the
fresh-search end-to-end with deep-band target families (the exp168
B3 pipeline verbatim, targets at the deep rungs, bars re-derived),
which tests whether the search's selection machinery VALUES the
widened band or the band's writability stays dormant until targets
ask for it".

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Pipeline, targets, and gates are fixed now.

THE PIPELINE (exp168's B3, verbatim, ONE swapped input):
  exp150's pipeline VERBATIM — the 72-member library with N*_lib
  re-derived (bar 82.288), the splice family 48,564 with N*_splice
  re-derived via exp146's splice_family_bar (bar 20.140), exp141's
  search loop at seed 141, the funnel (lib-novel -> splice-clear),
  N*_pool re-derived before selection (bar 33.776), exp165's R_W
  pre-emission exclusion clause, cap 10, ERR_BAR 6.0, audit seeds
  (1, 2, 3). THE ONE SWAPPED INPUT: the TARGET FAMILIES — the
  delivered cohort's decode/hold targets are exp172's deep-band
  constructions (MULTI 3-zone programs with zone values at the DEEP
  rungs {-40, -50, -60}, 3 targets x 10 translated instances... the
  target SET = 3 programs, one per rung, instance 0 translations —
  the same construction exp172 deposited; the search scores members
  against the deep targets where exp150's scored against its own).
  Library/splice/pool bars are TARGET-INDEPENDENT (structure bars) —
  they are re-derived and asserted at the deposited values.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-G1 (pipeline integrity at the swapped targets) the bars
           re-derive at the deposited values: N*_lib 82.288,
           N*_splice 20.140, N*_pool 33.776 (float equality at the
           deposited precision); the search loop at seed 141 is
           BIT-IDENTICAL to exp141's deposit through the funnel
           (the search's selection does not consult the targets —
           if it does, the divergence is the finding, deposited).
  GATE-G2 (delivery at the band) the delivered cohort (up to 10)
           decodes the DEEP targets: decode < 6.0 AND hold < 6.0 on
           3/3 seeds for >= 9/10 delivered members (the C3 clause
           at the deep targets); zero rejections; emission mode
           repriced_full (audit_only_fallback never fires).
  GATE-G3 (the band is VALUED, not just writable) the delivered
           members' emitted rungs reach the deep band: >= 1
           delivered member carries >= 1 emitted rung value in
           [-60, -35) (the search USES the widened repertoire when
           the targets ask for it — the dormancy question answered
           NO); the count of delivered members with deep rungs
           deposited.
  GATE-G4 (R_W discipline at the band) the production-floor R_W-
           positive set over the eligible pool is empty and equals
           the excluded set (exp168's B4 at the swapped targets);
           zero false exclusions.

NO post-hoc tuning. A --smoke check (library bar re-derivation only,
no search) is permitted before the credited run and discarded.
Wall budget: the exp168 B3 credited run took 178.1 s locally; the
runner split carries the per-rung jobs.

DEPOSIT: results/exp176_deep_band_search.json

RUN:
  python3 -m experiments.exp176_deep_band_search            # full
  python3 -m experiments.exp176_deep_band_search --smoke    # check
  python3 -m experiments.exp176_deep_band_search --rung -50.0
  # jobs: bars | d40 | d50 | d60
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

from experiments.exp136_generator_v6 import (  # noqa: E402
    decode as exp136_decode,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)

# ---- FIXED CONSTANTS ------------------------------------------------
DEEP_RUNGS = [-40.0, -50.0, -60.0]
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141
BAR_LIB = 82.288
BAR_SPLICE = 20.140
BAR_POOL = 33.776

OUT = os.path.join(ROOT, "results", "exp176_deep_band_search.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP168 = os.path.join(ROOT, "results", "exp168_cf1_production.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["bars", "d40", "d50", "d60",
                                      "all"], default="all")
    ap.add_argument("--rung", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--rung/--out)
