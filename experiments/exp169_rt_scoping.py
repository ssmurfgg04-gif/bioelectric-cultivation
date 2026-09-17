#!/usr/bin/env python3
"""exp169 — R_T SCOPED (the per-media diagnostic exp167 registered).

exp167's deposit (L147) falsified the BLANKET R_T adoption clause for
the temporal read: the flip-quiet window silences exactly the channel
(TC1's F) that carries exp148's schedule semantics — the corner's
excess and the battery's signal are the SAME channel, so one zero-knob
clause cannot buy both (A2 FAIL 0/12 separated; fidelity +0.005 only).
The deposit registered the scoping: "R_T per-media via a PRE-REGISTERED
diagnostic in the style of PN1's rho (threshold fixed from deposited
boundaries BEFORE decoding, zero per-instance tuning): the flip clock's
CONCENTRATION". THIS EXPERIMENT runs that diagnostic.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Gates, statistic, and threshold are fixed
now; the credited run uses this file unchanged.

THE DIAGNOSTIC (zero knobs, computable from the medium alone):
  f_max(medium) = max over directed edges (i, j) of the per-edge
  presence-transition count across the read window (the TC1 raw
  flip-clock matrix's max entry; FrameSeq/flip_clock_matrix machinery,
  exp148 verbatim). For PAIRED constructions (exp148's FlipPairMedium
  families) the unit of scoping is the PAIR: f_max(pair) = max over the
  two schedule members — a scoped read must use ONE arm per pair or the
  N2 contrast is an instrument artifact, not a schedule readout.
  THE RULE: apply R_T (exp167's adopted read) iff f_max < 32.0;
  otherwise keep exp148's RAW temporal read. One threshold, no
  per-instance tuning, no outcome feedback.

THE THRESHOLD — fixed from the DEPOSITED empty gap before this file
  was written (both bounds recomputed and asserted at run time):
  * diffuse class (R_T side): exp166's corner spot media (cell 7,
    j = 0..9) and clean media (cell 0, j = 0..9) — exp167's deposit
    records raw f_max in [5, 7] (scoping_candidate text).
  * concentrated class (raw side): exp148's 12 battery pairs —
    f_aper per chord edge up to ~1248, minimum member-max across the
    24 deposited members >= 1165 (results/exp167_rt_adopted.json
    battery.pairs f_per/f_aper lists; every f_per entry is 2 but the
    PAIR-JOINT max is the f_aper scale — the pair is the unit).
  * 32.0 sits in the deposited gap (7, 1165): >= 4x above the diffuse
    ceiling, >= 36x below the concentrated floor. The grid instances'
    f_max values are NOT part of the gap derivation — classifying them
    is the diagnostic's prediction work (gate S4).

INSTRUMENTS (zero new calibration):
  * exp148's module verbatim: FAMILIES, LADDER, SCHED_SEED,
    GRID_BASE_SEED, GRID_CLASSES, N_INSTANCES, N_INSTANCES_400,
    FlipPairMedium, FlipGridMedium, FrameSeq, flip_clock_matrix,
    read_temporal, exp148_decode, outcome_key, verdict_blind, and the
    constants N3_BAR 0.60 / N2_MIN_SEPARATION 10 / N1_MIN_BLIND 11;
    seeds (1, 2, 3).
  * exp167's module verbatim: RTMasked (the adopted medium wrapper),
    its decode dispatch, CORNER_CELL 7 / CLEAN_CELL 0 / SPOT_J / 
    SPOT_SEEDS.
  * Deposits read at run time: results/exp148_temporal_read.json,
    results/exp166_leading_edge.json, results/exp167_rt_adopted.json
    (errs at execute_signed's 2-dp precision; replay = exact float
    equality on the records).
  * INSTRUMENT PIN (exp167's mechanism, disclosed pre-run): both
    replay references predate CF-1, so NEURAL_SPEC_MIN is pinned to
    -35.0 in every module whose bound name the read chain consults
    (cultivation.bioelectric.collective, exp142, exp145, exp148,
    exp94) — restored-world semantics, save/restore asserted.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-S1 (threshold validity) recomputed f_max reproduces the
           deposited classes: all 20 corner/clean spot media
           f_max < 32.0; all 12 battery pair-joint f_max >= 32.0;
           the recomputed per-chord counts match the deposit's
           f_per/f_aper lists exactly (instrument replay); the
           corner spot raw projection errs replay exp167's A3
           inputs bit-exactly (the wrapper changes nothing raw).
           PASS = all clauses.
  GATE-S2 (raw where concentrated) the scoped read on the 12
           battery pairs IS exp148's raw temporal read bit-exactly:
           per-pair verdicts and errs identical to the deposited
           temporal records; N2 separation 12/12 and N1 blindness
           12/12 reproduced. (The diagnostic keeps the schedule
           channel wherever it lives.)
  GATE-S3 (R_T where diffuse) the scoped read on the corner spot
           set IS exp167's adopted read bit-exactly: corner
           (cell 7) errs == exp167's A3 errs_adopted (median 0.535,
           20/20 media replay), clean cell (cell 0) bit-identical
           to exp166's clean arm-A (the no-op clause).
  GATE-S4 (the grid prediction + no-regression) the schedule grid
           under the scoped read: per-instance f_max and class
           deposited BEFORE the pooled verdict; zero rejections;
           scoped pooled median <= 0.685 (exp148's deposited
           temporal median — no fidelity regression); the scoped
           cross-class outcome-identity count deposited and
           strictly below exp167's blanket 30/30 whenever at least
           one instance classifies concentrated (the schedule
           channel survives there). No bar on HOW many grid
           instances classify which way — that is the prediction.

NO post-hoc knob tuning; exactly ONE threshold. Whatever the outcome,
it is deposited. A --smoke instrument check (1 pair, 1 grid instance,
corner j=0, clean j=0) is permitted before the credited run and
discarded; the credited full run uses the committed script unchanged.

DEPOSIT: results/exp169_rt_scoping.json

RUN:
  python3 -m experiments.exp169_rt_scoping                 # full
  python3 -m experiments.exp169_rt_scoping --smoke         # check
  python3 -m experiments.exp169_rt_scoping --job battery   # runner split
  # jobs: threshold | battery | corner | grid
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

from experiments.exp148_temporal_read import (  # noqa: E402
    FAMILIES, FlipGridMedium, FlipPairMedium, FrameSeq, GRID_BASE_SEED,
    GRID_CLASSES, LADDER, N1_MIN_BLIND, N2_MIN_SEPARATION, N3_BAR,
    N_INSTANCES, N_INSTANCES_400, SCHED_SEED,
    decode as exp148_decode, flip_clock_matrix, outcome_key,
    read_temporal, verdict_blind,
)
from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE,
)
from experiments.exp167_rt_adopted import (  # noqa: E402
    RTMasked, CORNER_CELL, CLEAN_CELL, SPOT_J, SPOT_SEEDS,
    decode as exp167_decode,
)

# ---- INSTRUMENT PIN (see docstring) --------------------------------
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


# ---- THE DIAGNOSTIC (fixed) ----------------------------------------
THRESHOLD = 32.0            # the deposited gap (7, 1165)

OUT = os.path.join(ROOT, "results", "exp169_rt_scoping.json")
DEP148 = os.path.join(ROOT, "results", "exp148_temporal_read.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")
DEP167 = os.path.join(ROOT, "results", "exp167_rt_adopted.json")


def f_max_frames(frames: list[np.ndarray]) -> float:
    """Max per-edge presence-transition count across the window."""
    trans = np.zeros_like(frames[0], dtype=np.int64)
    for a, b in zip(frames[:-1], frames[1:]):
        trans += ((np.abs(b) > 0).astype(np.int64)
                  - (np.abs(a) > 0).astype(np.int64) != 0)
    return float(trans.max()) if trans.size else 0.0


def scoped_read(medium, seed: int, fmax: float, return_state: bool = False):
    """THE RULE: R_T iff f_max < THRESHOLD, else exp148's raw temporal."""
    if fmax < THRESHOLD:
        return exp167_decode("adopted", medium, seed,
                             return_state=return_state)
    return exp148_decode("temporal", medium, seed,
                         return_state=return_state)


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["threshold", "battery", "corner",
                                      "grid", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
