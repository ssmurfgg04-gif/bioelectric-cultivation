#!/usr/bin/env python3
"""exp178 — THE SCOPED READ TO PRODUCTION (the adoption, closed).

exp169's registered next (L148 (i)): "the scoped read as the ADOPTION
candidate for exp148's production temporal read (the diagnostic
clause is one function, zero knobs)". exp167 adopted R_T blanket and
was falsified (A2 0/12); exp169 scoped it and reconciled both
channels (4/4). This experiment wires the scoped read into the
PRODUCTION dispatch — exp148's decode gains the arm "scoped" — with
the bit-exact-at-every-old-operating-point audit exp168's CF-1
adoption set as the standard.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Wiring, audits, and gates are fixed now.

THE WIRING (one arm, one function, cited file):
  experiments/exp148_temporal_read.py — the decode dispatch gains
  arm "scoped": f_max from the medium's frames (exp169's
  f_max_frames VERBATIM, PAIR-JOINT max for paired constructions),
  then R_T (exp167's adopted path) iff f_max < 32.0 else the
  existing "temporal" arm's code path UNCHANGED. The existing arms
  ("temporal", "phase", "mag", "sign") are untouched — the scoped
  arm is ADDITIVE. No existing caller changes behavior (the default
  arm is whatever it was; "scoped" must be requested).

GATES (each evaluated exactly once):

  GATE-A1 (T=1 static bit-exactness — the automatic safety) on
           exp148's static N4 controls (the exp73 torus battery,
           exp142's signed/complex_phase 4-instance subsets,
           exp145's reactive subset): f_max == 0 < 32 at T = 1 ->
           the rule selects R_T, and rule_temporal_core at T = 1 is
           the no-op identity (core = the frame's own support), so
           the scoped arm's final V is BIT-IDENTICAL to the temporal
           arm's per seed, verify preserved, errs bit-identical to
           exp148's deposited static records.
  GATE-A2 (concentrated side unchanged) the 12 flip-clock battery
           pairs under the scoped arm: pair-joint f_max >= 32 ->
           the raw temporal path — errs and verdicts BIT-IDENTICAL
           to exp148's deposited temporal records (12/12 separation,
           12/12 blindness).
  GATE-A3 (diffuse side = the adopted read) the corner spot set
           under the scoped arm: BIT-IDENTICAL to exp167's A3
           adopted errs (median 0.535 replayed, 20/20 media; clean
           cell no-op bit-exact vs exp166's arm-A).
  GATE-A4 (grid no-regression + hygiene) the schedule grid under
           the scoped arm: zero rejections, pooled median <= 0.685
           (exp148's deposited temporal median), per-instance
           classification identical to exp169's S4 (all diffuse);
           the tests suite green POST-wiring (`python3 -m
           tests.run_tests` exits 0 — the additive arm touches no
           existing test).

INSTRUMENTS: exp148's module (post-wiring), exp169's f_max_frames +
THRESHOLD imported VERBATIM (one source of truth for the diagnostic),
exp167's adopted path, the -35.0 instrument pin for every replay
against pre-CF-1 deposits (save/restore asserted), seeds (1, 2, 3).

NO post-hoc tuning. A --smoke check (1 torus instance + 1 battery
pair) is permitted before the credited run and discarded.

DEPOSIT: results/exp178_scoped_production.json

RUN:
  python3 -m experiments.exp178_scoped_production            # full
  python3 -m experiments.exp178_scoped_production --smoke    # check
  python3 -m experiments.exp178_scoped_production --job A2   # split
  # jobs: A1 | A2 | A3 | A4
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

from experiments.exp148_temporal_read import (  # noqa: E402
    FAMILIES, FlipGridMedium, FlipPairMedium, GRID_BASE_SEED,
    GRID_CLASSES, LADDER, N1_MIN_BLIND, N2_MIN_SEPARATION, N3_BAR,
    N_INSTANCES, N_INSTANCES_400, SCHED_SEED,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames,
)
from experiments.exp167_rt_adopted import (  # noqa: E402
    RTMasked, CORNER_CELL, CLEAN_CELL, SPOT_J, SPOT_SEEDS,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP148_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP148_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


OUT = os.path.join(ROOT, "results", "exp178_scoped_production.json")
DEP148 = os.path.join(ROOT, "results", "exp148_temporal_read.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")
DEP167 = os.path.join(ROOT, "results", "exp167_rt_adopted.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["A1", "A2", "A3", "A4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
