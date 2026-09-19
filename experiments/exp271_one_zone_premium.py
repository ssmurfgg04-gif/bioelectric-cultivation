#!/usr/bin/env python3
"""exp271 — THE ONE-ZONE PREMIUM (batch 29; L248's registered next —
zero new simulation).

THE OPEN ITEM (L248): the structural dose is a STEP — the one-zone
rewrite's mean err 0.7939 vs the multi-zone saturation 1.0131, and
the canon baseline's own worst-errs ~0.55-0.62 (exp256's canonical
rows). The one-zone regime carries a PREMIUM over canon (the single
deep zone already costs more than the canon program) that the
multi-zone regime saturates past. Decompose the premium the exp262
way: per row, premium = d1_err - canon_err (both from the deposits:
exp270's d=1 rows, exp256's canonical rows on the same host/seed);
the premium's own structure: its mean, its host/seed rank shares
(the exp229/exp262 tied-average-rank OLS convention), and its
sign consistency (does EVERY host carry a positive premium, or do
some hosts find the one-zone rewrite cheaper than canon?).

PRE-REGISTERED GATES:

  P1  THE RECONSTRUCTION: the d=1 errs (36 rows) re-read from
      exp270's deposit; the canon worst-errs (36 rows) re-read from
      exp256's canonical rows (the same host/seed keys); both grids
      complete, finite, sha-verified.
  P2  THE PREMIUM: the mean premium > 0 (the one-zone rewrite costs
      more than canon — the step's lower shelf is still above the
      canon floor) AND the sign consistency >= 30/36 rows positive
      (the premium is systematic, not host-noise).
  P3  THE STRUCTURE: the premium's host/seed rank shares reported
      (the exp262 convention); the gate reads the SEED share only:
      seed share <= 0.10 -> the premium is deterministic-per-host
      (structural — the step's shelf height is a host property);
      else MIXED/NOISE-LIKE honestly named.
  P4  THE DISCIPLINE: exp270's/exp256's deposits READ-ONLY
      sha-recorded byte-unchanged; deterministic; no wall-clock
      fields; the -60.0 floor asserted at exit (no exp169 import).

THE BRANCHES (pre-named): PREMIUM-STRUCTURAL (P2 + P3's structural
branch) / PREMIUM-MIXED / PREMIUM-ABSENT (P2 fails — the one-zone
rewrite is canon-equivalent, the step's lower shelf IS the floor).

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
OUT = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")


def main() -> dict:
    raise NotImplementedError(
        "exp271 body pending — pre-registration commit only")
