#!/usr/bin/env python3
"""exp229 — THE CURVATURE TEST (L202's registered next).

exp226's PARTIAL-TRACKING left a genuine boundary structure: ~150x
inside the smoothing bound in magnitude, tracking the step response
only partially (rho 0.545). The registered identity test: the
residual's structure decomposed against the plan's SECOND difference
(the curvature, not the step). If the residual tracks the plan's
curvature, the excess is the pattern's own geometry read through the
substrate; the branch: CURVATURE-TRACKED / GENUINE-EXCESS.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp226's machinery verbatim
(the battery, the replay anchors, the residual rows r_i, the
disclosures — the D_i = 0 points kept, the alternates audit-only);
the CURVATURE INSTRUMENT (pre-named, zero knobs): K_i = |T_plan[i-1]
- 2*T_plan[i] + T_plan[i+1]| on the ring backbone (the plan's second
difference at cell i); the clause: Spearman(r_i, K_i) across the same
10,047 canon-boundary points.

GATES (each evaluated exactly once):
  GATE-K1 (the replay) exp226's anchors reproduce (exp199 bit-exact
           25/25 + exp208's decomposition bit-exact).
  GATE-K2 (the curvature clause) the branch named: CURVATURE-TRACKED
           (rho >= 0.6) / MIXED (0.3 <= rho < 0.6) / GENUINE-EXCESS
           (rho < 0.3).
  GATE-K3 (the joint reading) the partial-correlation of r_i with
           K_i controlling for S_i * D_i (exp226's instrument)
           deposited; the three-way attribution (step, curvature,
           unexplained) deposited as shares of rank variance.
  GATE-K4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp229_curvature_test.json
RUN: python3 -m experiments.exp229_curvature_test [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp229_curvature_test.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
