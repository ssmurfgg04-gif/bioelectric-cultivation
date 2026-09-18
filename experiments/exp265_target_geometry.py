#!/usr/bin/env python3
"""exp265 — THE TARGET-GEOMETRY REGRESSION (batch 25 item 1; L242's
registered next (a) — zero new simulation).

THE OPEN ITEM (exp262's arm share 0.757): 75.7% of the explainable
rank variance of the 72 battery rows' worst errs sits on the
canonical-vs-substituted arm contrast. The substitution changes the
ROW (the read program's target), not the medium (exp243's P3 keeps
the base medium). So the arm contrast IS a target-geometry contrast:
the deep band's -60.0 rung rows vs the canon row. What property of
the deep targets carries it?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
substituted rows' worst errs (exp256's deposited 36 rows) regressed
against the deep targets' OWN structural properties, computed from
the exp256 deposit's row records + the deep target construction
(exp172's/exp214's pre-named construction, rebuilt deterministically
at n=400 and bit-asserted against the deposited row_target_sha256):

  T1  the target's OWN canon-boundary cell count (exp208's
      classify on the target itself — the boundary the TARGET
      draws, not the medium's);
  T2  the target's zone count (the deep band is one zone at -60.0
      over MULTI's zone skeleton — the construction's own count);
  T3  the target's value range (max - min).

The regression: Spearman + the OLS slope on (property, worst err)
across the 36 substituted rows, per property; plus the canon rows'
(36 rows) same regressions as the specificity mirror.

PRE-REGISTERED GATES:

  G1  THE REBUILD: the deep targets rebuilt at n=400 bit-match the
      exp256 deposit's row_target_sha256 records (the construction
      is deterministic; any drift stops the experiment).
  G2  THE ARM CONTRAST DECOMPOSED: at least ONE pre-named target
      property reaches Spearman >= 0.5 against the substituted
      rows' worst errs (the arm share's geometry carrier exists at
      the target level).
  G3  THE SPECIFICITY MIRROR: the same property's regression
      against the CANON rows' worst errs is reported (the canon
      rows share one target — the host canon — so the mirror is
      the HOST-LEVEL canon-boundary count, the exp255 instrument;
      the pre-named expectation: the mirror stays the strong
      host-level carrier rho 0.857, the target-level carrier is
      the substituted rows' own).
  G4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; deterministic; no wall-clock
      fields; the -60.0 floor asserted at exit (no exp169 import).

THE BRANCHES (pre-named): G2 PASS -> TARGET-GEOMETRY-CARRIES (the
arm share has a named geometric carrier — the residual's next
instrument is the target's own boundary structure); G2 REFUTE ->
TARGET-GEOMETRY-ABSENT (the arm share is not the target's geometry —
the interaction is the read's OWN response to the substitution,
deposited honestly).

RUN: a deposit re-read + target rebuilds + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp265_target_geometry.json")


def main() -> dict:
    raise NotImplementedError(
        "exp265 body pending — pre-registration commit only")
