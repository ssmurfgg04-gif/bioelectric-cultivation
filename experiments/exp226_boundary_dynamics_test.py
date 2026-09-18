#!/usr/bin/env python3
"""exp226 — THE BOUNDARY RESIDUAL'S DYNAMICS TEST (L198's registered
next).

The boundary excess (+0.574 mV at the canon-boundary cells, exp208)
survived every machinery suspect: the read face (three refutations,
L192/L194) and the canon-fallback (zero firings, zero value-changing
when forced, L198). The remaining hypothesis: the residual is the
SUBSTRATE'S OWN smoothing response to the plan's discontinuity — the
dynamics necessarily rounding a step the plan draws. The test: per
boundary cell, the plan's step magnitude vs the residual's magnitude,
against the substrate's local smoothing response priced on the same
battery.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt battery
verbatim (the c6 cell's 25 instances, seeds (1,2,3), the production
scoped read); exp208's classification + decomposition verbatim (the
CANON-BOUNDARY mask, the mV^2 accounting); the SMOOTHING RESPONSE
(pre-named, zero knobs): per boundary cell i, the local step S_i =
max |T_plan difference across i's lattice neighbors| and the
substrate's one-step diffusion response D_i = the ring-averaged
|W[i,.]|-weighted neighbor value spread (the first-order smoothing
kernel exp137's dynamics implements — no new machinery, the medium's
own weights); the clause: the per-cell residual r_i (the armed-vs-plan
deviation from exp208's decomposition rows) vs D_i scaled by S_i.

GATES (each evaluated exactly once):
  GATE-R1 (the replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 x 3) and exp208's decomposition reproduces
           bit-exactly at the reference (exp213's B1 verbatim).
  GATE-R2 (the correlation) Spearman(residual_i, S_i * D_i) across
           all boundary cells of the 25 instances x 3 seeds; the
           branch named: SMOOTHING-BOUND (rho >= 0.6) /
           PARTIAL-TRACKING (0.3 <= rho < 0.6) / EXCESS-NAMED
           (rho < 0.3 — a genuine boundary mechanism left).
  GATE-R3 (the magnitude clause) the residual's magnitude ratio:
           median(r_i / (S_i * D_i)) deposited; the clause holds iff
           the median <= 1.0 (the residual within the smoothing
           bound) — deposited alongside R2, disclosed as a reading
           aid.
  GATE-R4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp226_boundary_dynamics_test.json
RUN: python3 -m experiments.exp226_boundary_dynamics_test [--smoke] [--job ...] [--out ...]
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
                   "exp226_boundary_dynamics_test.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
