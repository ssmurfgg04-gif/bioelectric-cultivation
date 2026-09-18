#!/usr/bin/env python3
"""exp262 — THE RESIDUAL VARIANCE COMPONENTS (batch 24 item 1; L239's
registered next (a) — zero new simulation).

THE OPEN ITEM: the boundary residual's rank variance splits
step 0.241 / curvature 0.058 / unexplained 0.701 (exp229), the
unexplained share 0.686 under exp245's gauge-free form; every
instrument family since has REFUTED (read-face x4, write-context
exp258, pair-weights exp259, pair-structure exp260, ca2-readout
exp261). Where does the 68.6% live at the DESIGN level? The exp256
battery's 72 deposited rows (12 hosts x 2 arms x 3 seeds, worst errs)
carry the answer's factors: host identity, arm (canonical vs
substituted), seed.

THE INSTRUMENT (pre-registered, zero-knob): the three-way
rank-variance attribution by the exp229 OLS-on-tied-average-ranks
method generalized to three factors — the response is the row's worst
err rank over the 72 rows; the factors enter in the pre-named order
host, then arm, then seed; the shares are the symmetric average of
the two order-of-entry decompositions (exp229's exact convention,
the split sums to 1 exactly, no clamping); the SEED share is the
pre-named discriminant.

PRE-REGISTERED GATES:

  V1  THE REPRODUCTION: the 72 deposited worsts re-read from
      exp256's deposit are complete (12 x 2 x 3, no gaps), finite,
      and the battery's own anchors hold (the deposit's exp243
      reproduction records byte-unchanged, sha-verified).
  V2  THE ATTRIBUTION: the three shares computed as pre-named; the
      deposit reports all three plus the residual.
  V3  THE DISCRIMINANT (the gate): seed-share <= 0.10 -> the residual
      is DETERMINISTIC-PER-INSTANCE (structural — it replicates
      across seeds; the next instruments must be structure-level);
      seed-share >= 0.30 -> NOISE-LIKE (the residual is mostly
      seed-level variance — the search shifts to the noise path);
      between -> MIXED. The gate reads the seed share ONLY; the
      branch is pre-named.
  V4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; deterministic; no wall-clock
      fields; the -60.0 floor asserted (no exp169 import needed —
      the battery is a pure re-read).

THE BRANCHES (pre-named): DETERMINISTIC-PER-INSTANCE / NOISE-LIKE /
MIXED — each names the next instrument family honestly.

RUN: a pure deposit re-read + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp262_variance_components.json")


def main() -> dict:
    raise NotImplementedError(
        "exp262 body pending — pre-registration commit only")
