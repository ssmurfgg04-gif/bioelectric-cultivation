#!/usr/bin/env python3
"""exp173 — THE POOLED GROUPING STATISTIC (L144's registered repair (b)).

exp163's registered next (L144): the grouping contrast's per-pair
err-level channel is exhausted at the deposited floor (max response
0.32 mV vs theta 0.27, 10/12 pairs sub-threshold) — the contrast needs
"(b) a pooled/ensemble statistic across pairs (sum/median of signed
dev asymmetries)". Pooling buys power: the deposited per-pair noise
floor is 0.09 mV, and a SIGNED ensemble mean over the 12 adversarial
pairs accumulates a consistent cancellation-attributable response
while averaging the floor down. exp163's devs were compared per pair
and ABSOLUTE-VALUED (C = |err1 - err2|); the sign structure across
pairs was never read. THIS EXPERIMENT reads it.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Statistic, null, and gates are fixed
now; the credited run uses this file unchanged.

CONSTRUCTION (exp163 VERBATIM, replayed for integrity):
  exp159's build_pair / project / co_membership imported verbatim,
  the same 12 adversarial pairs, construction seed 159, bit-identical
  projections (A1 == A2 per pair, asserted), S_1 != S_2, S_2 ==
  support(A), connectivity re-asserted per pair. V2 weighting from
  exp163's cancel_mass_matrix VERBATIM (W peaks on the sign-
  cancellation entries; member 2 has W == 0 -> augmented == A
  bit-exactly). Readout: STAR_OP verbatim (gamma 64, mu 0), seeds
  (1,) per decode as exp163's credited run, err_vs_target.

THE SIGNED STATISTIC (new, fixed now):
  dev1_signed(p) = err(A + F*S_v(m1), T1) - err(A, T1)   [signed]
  dev2_signed(p) = err(A + F*S_v(m2), T2) - err(A, T2)   [signed]
  with A the SHARED bit-identical projection and err(A, T) the arm-1
  null decode (exp163's null protocol verbatim).
  POOLED STATISTIC: stat = mean over the 12 pairs of dev_signed.
  Reported separately for the sign-cancellation side (m1) and the
  clique side (m2). The SIGNED mean is the primary; the median is
  recorded (not gated).

TWO-PHASE NULL DISCIPLINE (exp163's pre-decode deposit, verbatim):
  PHASE-A (null deposit, written to the deposit file BEFORE any
  real-arm decode): the pooled null distribution from the SHARED
  arm-1 null — per pair, the signed dev of a PLACEHOLDER member
  whose augmentation is exp163's deposited null augmentation
  (the arm-1 null errs are exp163's DEPOSITED null_err values,
  replayed bit-exactly); the null bar = max |pooled null stat|
  over the deposited null protocol's seeds. The bar is frozen in
  the phase-A record before the phase-B execute_signed calls.
  PHASE-B (real arm): dev1_signed/dev2_signed per pair, the pooled
  stats, the verdict.

INSTRUMENT PIN (exp167's mechanism, disclosed pre-run): exp163's
  deposit predates CF-1, so NEURAL_SPEC_MIN is pinned to -35.0 in
  every module whose bound name the chain consults
  (cultivation.bioelectric.collective, exp142, exp145, exp148,
  exp94) — save/restore asserted.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-E1 (construction replay) projections bit-identical per pair
           (A1 == A2, 12/12); the unsigned |dev| values recomputed
           from the fresh decode match exp163's deposited
           v2_weighted devs within the 2-dp rounding (|diff| <=
           0.005 mV, 12/12 on both sides); the m2 side augmented ==
           A bit-exactly (W == 0, 12/12).
  GATE-E2 (null deposit first) the phase-A record exists in the
           deposit with the frozen null bar BEFORE the phase-B
           decode (byte-offset assertion, exp168's discipline);
           the pooled null bar is finite and > 0.
  GATE-E3 (the ensemble verdict) PASS iff |stat_m1| > null bar
           AND >= 9/12 pairs share the majority sign of dev1_signed
           (the ensemble reads a consistent cancellation-side
           response, not 12 independent coin flips). Failure
           deposited with the per-pair signed table.
  GATE-E4 (attribution at ensemble level) |stat_m2| <= null bar
           (the clique side stays silent when pooled — the contrast
           is attributable to the sign-cancellation member at the
           ensemble level, exp163's G3 discipline carried over).

NO post-hoc knob tuning; exactly ONE statistic. A --smoke instrument
check (pairs 0-1 only) is permitted before the credited run and
discarded; the credited full run uses the committed script unchanged.

DEPOSIT: results/exp173_pooled_grouping.json

RUN:
  python3 -m experiments.exp173_pooled_grouping            # full
  python3 -m experiments.exp173_pooled_grouping --smoke    # check
  python3 -m experiments.exp173_pooled_grouping --phase A  # runner split
  # jobs: phaseA | phaseB
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

from experiments.exp159_hyperedge_walk import (  # noqa: E402
    build_pair, co_membership, project, connected, GADGET_SIZE,
    T1, T2, SEED_CONSTRUCT, SEED_EXEC, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix, NOISE_MULTIPLE,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

# ---- INSTRUMENT PIN (see docstring) --------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP163_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP163_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


OUT = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")
DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")
N_PAIRS = 12
MAJORITY_MIN = 9               # of 12 pairs share the majority sign


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--phase", choices=["A", "B", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--phase/--out)
