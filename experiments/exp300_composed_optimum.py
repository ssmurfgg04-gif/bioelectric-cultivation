#!/usr/bin/env python3
"""exp300 — THE COMPOSED OPTIMUM: WHERE IS THE UNION'S DOSE PEAK?
(batch 54; ledger L283's registered next (a) — exp299 landed
SUPER-ADDITIVE: at g=0.5 the union of the three carrying faces beats
the best single by 0.093 mV (the noise shrink + the value
re-assertion compose below saturation); exp298 landed ADDITIVE at
g=1.0 (the sigma face saturates and subsumes the blends). THE OPEN
QUESTION: where is the COMPOSED carrier's optimum? The sub-saturation
compounding predicts the union's improvement grows as long as BOTH
mechanisms contribute — the sigma face's noise-shrink weakens toward
g=1.0 (its saturation) while the blend face's re-assertion is
dose-full from g>0. The pre-named ladder {0.25, 0.5, 0.75, 1.0}
spans the composition's live range: if the union's delta peaks
BELOW 1.0 the composition has its own optimum (the two mechanisms'
trade-off); if it rises monotonically to 1.0 the saturation face
dominates and the composed optimum IS the saturated face.)

THE ARMS (the exp298/exp299 landed composition VERBATIM — the union
faces=(ctx, gj, apop) on ONE walk — at each ladder point; the
single-face anchors at every ladder point come from the deposited
ladders: ctx from exp289's grid rows {0.25, 0.5} + exp296's g=1.0
rows; gj/apop from exp297's ladder rows {0.25, 0.5, 1.0}):
  faces=("ctx",)   the anchor ladder: MUST reproduce the deposited
                   ctx rows BIT-EXACT 72/72 at each of {0.25, 0.5,
                   1.0};
  faces=("gj",)    MUST reproduce the deposited gj rows BIT-EXACT
                   72/72 at each of {0.25, 0.5, 1.0};
  faces=("apop",)  MUST reproduce the deposited apop rows BIT-EXACT
                   72/72 at each of {0.25, 0.5, 1.0};
  faces=UNION      72 fresh rows at EACH of {0.25, 0.5, 0.75, 1.0}
                   — 288 union decodes.
Total: 3 x 3 x 72 (the anchors) + 4 x 72 (the union ladder) = 936
decodes on the shared deep-row battery.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each single-face arm reproduces its deposited rows
      BIT-EXACT 72/72 at each of its ladder points (the errs + the
      trace shas; the sources: exp289's grid rows + exp296's/exp297's
      deposits); the rebuild chain asserted; the S* lock reads 936;
      the floor -60.0; the deposits READ-ONLY (the pre-named 12 + the
      4 control deposits), sha before/after; the test suite green.
  G2  THE FORMS: the register faces 72/72 per (arm, dose); the stream
      faces 72/72 per (arm, dose) vs exp282's/exp287's deposited
      records; the site-write counts constant across seeds per
      (host, instance) and dose-invariant for the union (the site
      does not move with the dose); the gj landed assert re-run per
      row.
  G3  THE COMPOSED-OPTIMUM BRANCH (pre-named): the union's mean
      paired delta vs exp256's dormant baseline at each ladder point;
      the branch:
      PEAKED-BELOW-1.0  iff delta(0.75) < delta(0.5) AND delta(1.0) >
                        delta(0.75) (the composition's own optimum —
                        the two mechanisms' trade-off is real);
      MONOTONE-TO-1.0   iff delta(1.0) < delta(0.75) < delta(0.5) <
                        delta(0.25) (the saturation face dominates —
                        the composed optimum IS the saturated face);
      PLATEAU           iff the |delta| spread among {0.5, 0.75,
                        1.0} <= 0.01 mV;
      else MIXED (recorded, the honest leftover).
      Audit-only: the per-host per-dose delta tables; the
      composition's gain face (the union's delta minus the best
      single's delta at each dose — where the compounding lives); the
      worst-err per dose vs the 6.0 bar; the H3/H5 deltas; the R_max
      face at g=0.5 and g=1.0.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PEAKED-BELOW-1.0 / MONOTONE-TO-1.0 /
PLATEAU / MIXED.

RUN: 936 decodes ~ 10-14 min — the pre-named form is the CHECKPOINT-
SPLIT EXP300_MODE=pass1 (the anchor ladder: the three singles at
their deposited doses, 648) | pass2 (the union ladder, 288) | merge;
the in-process default runs the whole sequence.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp300_composed_optimum.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp300's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
