#!/usr/bin/env python3
"""exp174 — THE REPLICATION COHORT (the ensemble's second 12).

exp173's registered next (L152): the signed-mean signature is a power
claim, and "a power claim is only as good as its second cohort" — 12
FRESH adversarial pairs (same construction protocol, new construction
seed) to test whether stat_m1 > null bar with a >= 9/12 majority sign
REPLICATES; plus the minority-pair anatomy (the 2 minority-sign pairs
of the original cohort) recorded.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Cohort, statistic, and gates are fixed
now; the credited run uses this file unchanged.

THE FRESH COHORT:
  exp159's construction VERBATIM with the ONE changed input disclosed
  here: exp159.SEED_CONSTRUCT rebound 159 -> 174174 for the cohort
  build (the OLD_FLOOR_PIN rebinding mechanism — save, rebind, build
  all 12 pairs via build_pair(p) p = 0..11, restore asserted). The
  construction protocol is otherwise untouched: same GADGET_SIZE,
  same T1/T2 targets, same OP, same adversarial family structure —
  the 12 fresh pairs are the same CLASS of object with independent
  draws, not a re-run of the original 12.

THE STATISTIC (exp173's, verbatim — zero new choices):
  dev_signed(p) = err(A + F*S_v(m1), T1) - err(A, T1)   [signed]
  stat = mean over the 12 pairs; V2 weighting via exp163's
  cancel_mass_matrix VERBATIM; STAR_OP readout, seed (1,); m2 side
  computed identically for attribution.

TWO-PHASE NULL DISCIPLINE (exp173's, verbatim):
  PHASE-A: the fresh cohort's null bar frozen on disk BEFORE any
  real-arm decode — per-pair null = the shared arm-1 null decode of
  the bit-identical projection (exp163/exp173's null protocol); bar =
  max |pooled null stat| over exp142's deposited seeds (1, 2, 3) x
  own-targets. Byte-offset assertion in the deposit.
  PHASE-B: the real arm.

INSTRUMENT PIN: the chain predates CF-1; NEURAL_SPEC_MIN pinned to
  -35.0 (exp167's mechanism, save/restore asserted).

MINORITY ANATOMY (recorded, no bar): exp173's deposit lists the
  per-pair signed devs of the ORIGINAL cohort; the minority-sign
  pairs' structural features (density d_k, cancel_entries_S1,
  gadget size, sw1 mass) are tabulated against the majority pairs'
  — the deposit carries the table; any structural split is the
  registered question, not a gate.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-F1 (fresh construction integrity) per pair: A1 == A2
           bit-identical, S_1 != S_2, S_2 == support(A), connectivity
           holds — 12/12 (exp163's G3/A1 discipline on the new
           cohort); the fresh projections differ from the original
           cohort's (independence check: no pair's projection
           bit-equal to any original pair's).
  GATE-F2 (null discipline) the phase-A record precedes the phase-B
           decode (byte offsets in the deposit); the fresh null bar
           is finite and > 0.
  GATE-F3 (REPLICATION — the gate) |stat_m1_fresh| > fresh null bar
           AND >= 9/12 pairs share the majority sign of dev1_signed.
           PASS = the signature replicates on independent draws.
           Failure = the original cohort's 4/4 was cohort luck —
           deposited honestly and the ensemble claim DOWNGRADED to
           cohort-specific in the ledger.
  GATE-F4 (attribution replicates) |stat_m2_fresh| <= fresh null
           bar (the clique side silent on the fresh cohort too).

NO post-hoc knob tuning. A --smoke check (fresh pairs 0-1) is
permitted before the credited run and discarded.

DEPOSIT: results/exp174_replication_cohort.json

RUN:
  python3 -m experiments.exp174_replication_cohort          # full
  python3 -m experiments.exp174_replication_cohort --smoke  # check
  python3 -m experiments.exp174_replication_cohort --phase A
  # jobs: phaseA | phaseB | anatomy
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

import experiments.exp159_hyperedge_walk as exp159  # noqa: E402
from experiments.exp159_hyperedge_walk import (  # noqa: E402
    build_pair, co_membership, project, connected, GADGET_SIZE,
    T1, T2, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

# ---- INSTRUMENT PIN -------------------------------------------------
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


# ---- FIXED CONSTANTS ------------------------------------------------
FRESH_SEED_CONSTRUCT = 174174    # the ONE changed input, disclosed
N_PAIRS = 12
MAJORITY_MIN = 9

OUT = os.path.join(ROOT, "results", "exp174_replication_cohort.json")
DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")
DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--phase", choices=["A", "B", "anatomy", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--phase/--out)
