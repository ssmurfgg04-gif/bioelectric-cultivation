#!/usr/bin/env python3
"""exp179 — TARGET-AWARE DELIVERY (the clause exp176 registered).

exp176's registered next (L155): the search's selection machinery is
TARGET-FREE (proven by G1's bit-identity at seed 141) — the delivered
cohort carries deep rungs (9/10, G3) but fails deep-target delivery
(0/10 under the 6.0 bar, G2 REFUTE). The repair is a TARGET-AWARE
DELIVERY clause: rank the 96-eligible pool by price at the GIVEN
target set before the cap-10 selection. No new knobs — exp150's
price_rung machinery already computes decode prices.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Clause, gates, and bars are fixed now.

THE CLAUSE (one rule, zero knobs):
  Given the 96-eligible pool (exp168's B3 funnel at seed 141,
  bit-identical re-derivation) and a target set T:
    rank members ASCENDING by price(m, T) = the MEAN composed decode
    err over T's targets x seeds (1, 2, 3) via exp150's price_rung
    VERBATIM at the production cell (1.0, 0.0);
    walk the ranked order, keeping member m iff its min pairwise
    distance D(m, kept) > N*_pool (33.776, the deposited C4 bar) —
    the SAME diversity constraint exp150's delivery enforced, applied
    within the price-ranked order;
    stop at 10. Tie-break: member index ascending. That is the whole
    clause.

GATES (each evaluated exactly once):

  GATE-H1 (pipeline integrity) the 72-member library, splice family,
           and 96-eligible pool re-derive bit-identically to exp176's
           deposit (bars 82.288 / 20.140 / 33.776; funnel counts
           96/253 -> 96/96); the pool's price table at T is computed
           fresh and deposited (96 rows).
  GATE-H2 (the old operating point's quality bars hold at exp150's
           own targets) the clause delivered-10 scored against
           exp150's deposited targets: C1 (every member beyond
           N*_lib and N*_splice), C2 (emitted-rung quads < 6.0),
           C3 (decode < 6.0 AND hold < 6.0 on 3/3 seeds), C4 (min
           pairwise D > N*_pool) — ALL PASS (the member SET may
           differ from exp150's; the quality bars may not).
  GATE-H3 (deep-target delivery — the clause's purpose) the clause
           delivered-10 scored against exp176's deep target set
           (rungs -40/-50/-60, the deposited constructions):
           >= 9/10 members with decode < 6.0 AND hold < 6.0 on 3/3
           seeds at EVERY rung; zero rejections; emission mode
           repriced_full.
  GATE-H4 (discipline) the R_W production-floor set empty == the
           excluded set over the eligible pool (both target sets);
           zero rejections everywhere; the price table's rng
           consumption does not perturb the search's bit-identity
           (prices computed AFTER the funnel re-derivation, in a
           fresh process block, pin untouched — no instrument pin
           needed: this run is post-CF-1 production world).

NO post-hoc tuning. A --smoke check (the price table for 3 pool
members only) is permitted before the credited run and discarded.

DEPOSIT: results/exp179_target_aware_delivery.json

RUN:
  python3 -m experiments.exp179_target_aware_delivery          # full
  python3 -m experiments.exp179_target_aware_delivery --smoke  # check
  python3 -m experiments.exp179_target_aware_delivery --job H3
  # jobs: H1 | H2 | H3
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
BAR_LIB = 82.288
BAR_SPLICE = 20.140
BAR_POOL = 33.776
ERR_BAR = 6.0
AUDIT_SEEDS = (1, 2, 3)
N_DELIVER = 10
SEARCH_SEED = 141
DEEP_RUNGS = [-40.0, -50.0, -60.0]

OUT = os.path.join(ROOT, "results", "exp179_target_aware_delivery.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP176 = os.path.join(ROOT, "results", "exp176_deep_band_search.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["H1", "H2", "H3", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
