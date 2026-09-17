#!/usr/bin/env python3
"""exp175 — THE M33 SPLIT (one constant, one gate branch, to production).

exp171's registered next (L150): "the SPLIT — M33 needs its OWN
anterior line constant (M33_LINE = -35.0, the literature midpoint)
distinct from the S-REL adoption floor (NEURAL_SPEC_MIN = -60.0)".
exp171 priced the collapse (asymmetry ratio 0.1550 < 0.5 under CF-1's
one-constant widening); this experiment LANDS the repair in the core,
with the same bit-exact-at-old-operating-points discipline exp168 set.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Patch, audits, and gates are fixed now.

THE PATCH (ONE new constant + ONE gate-branch change, cited file:line):
  cultivation/bioelectric/collective.py
    - NEW: M33_LINE = -35.0   (the anterior/posterior literature
      midpoint: WT head -20 vs WT trunk/tail -50; the line M33's
      docstring has always described)
    - the M33 gate branch (collective.py:582) reads
      `float(spec[i]) >= M33_LINE` where it read
      `float(spec[i]) >= NEURAL_SPEC_MIN`.
  NEURAL_SPEC_MIN stays -60.0: the S-REL spec-adoption floor (the
  decode consumer exp136.decode:394) is UNCHANGED — CF-1's widened
  repertoire is untouched by this patch. Exactly one behavioral
  consumer changes (the M33 branch); the M36 misanchor branch
  (collective.py:588+) shares the anterior-eligibility question and
  is INACTIVE at defaults (mis_w = 0) — its floor is NOT changed in
  this patch and that asymmetry is disclosed (M36 keeps reading
  NEURAL_SPEC_MIN; no deposited experiment exercises M36-active).

GATES (each evaluated exactly once):

  GATE-P1 (tests green) `python3 -m tests.run_tests` from the repo
           root POST-patch exits 0 with zero failures (checked
           beforehand: no test references M33_LINE; the -35.0 in
           test_d3_semantics is a theta anchor value, unrelated).

  GATE-P2 (M33 restored to the literature line, bit-exact) exp171's
           four families re-run at neural_w = 0.5, r = 0.05, seeds
           (1, 2, 3): TRUNK/DEEP qualifying-cell counts return to 0
           and the engines' full draw logs are BIT-IDENTICAL to
           exp171's PINNED arm per (family, seed); HEAD/LINE remain
           bit-identical to both of exp171's arms (they never
           diverged); the asymmetry ratio A_patched/A_pinned under
           the SPLIT is 1.0 within float equality (the collapse is
           repaired — branch (a) of exp171's pre-named verdicts,
           now by construction).

  GATE-P3 (adoption untouched — CF-1 stands) the deep band still
           decodes: exp172's frontier rung (-60.0, instance 0,
           seeds (1,2,3)) replayed bit-exactly under the split core
           (exp136.decode reads NEURAL_SPEC_MIN, which did not
           move); exp172's shallow controls bit-exact as well.

  GATE-P4 (hygiene) pin save/restore asserted where used; zero
           non-finite values; the patch diff is exactly the two
           cited lines (git diff --stat asserted in the deposit).

NO post-hoc tuning. A --smoke instrument check (TRUNK family, seed 1)
is permitted before the credited run and discarded. The credited run
uses the committed script unchanged.

DEPOSIT: results/exp175_m33_split.json

RUN:
  python3 -m experiments.exp175_m33_split            # full
  python3 -m experiments.exp175_m33_split --smoke    # check
  python3 -m experiments.exp175_m33_split --job P2   # runner split
  # jobs: P2 | P3
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
OLD_FLOOR_PIN = -35.0          # exp171's pinned floor (the pinned arm)
NEW_FLOOR = -60.0              # CF-1, unchanged by this patch
M33_LINE = -35.0               # the NEW constant the patch introduces
NEURAL_W = 0.5
N_CELLS = 100
SEEDS = (1, 2, 3)
FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}

OUT = os.path.join(ROOT, "results", "exp175_m33_split.json")
DEP171 = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")
DEP172 = os.path.join(ROOT, "results", "exp172_deep_band_sweep.json")


class OldFloorPin:
    """exp168's mechanism, for the pinned-arm replay comparisons."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR_PIN
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["P2", "P3", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
