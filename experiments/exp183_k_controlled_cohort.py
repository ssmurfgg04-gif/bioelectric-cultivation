#!/usr/bin/env python3
"""exp183 — THE K-CONTROLLED COHORT (is the ensemble's sign a density
effect?).

exp174's registered next (L153): all three minority-sign pairs across
both cohorts are k = 4 gadgets (original p4/p6, fresh p5) — "if the
k = 4 stratum flips sign while k = 3 holds, the ensemble's sign
structure is a DENSITY effect and the grouping read gains its first
structural covariate".

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Stratification, statistic, and gates are
fixed now.

THE STRATIFICATION (zero fitting): exp159's construction VERBATIM,
seed ladder 183001..183036 (SEED_CONSTRUCT rebound per pair, the
exp174 mechanism, restore asserted) — 36 fresh pairs; each pair's
REALIZED k recorded from the construction; the cohort is THEN split
into the k = 3 stratum and the k = 4 stratum, taking the FIRST 6 of
each by ladder order (the pre-registered selection rule; if either
stratum has fewer than 6 among the 36, the stratum sizes are
deposited as-is and the gates evaluate on what exists — disclosed).

THE STATISTIC (exp173/exp174's, verbatim): dev_signed per pair,
stat = mean over the stratum's pairs, V2 weighting via exp163's
cancel_mass_matrix, STAR_OP readout, seed (1,); m2 side identical.

TWO-PHASE NULL DISCIPLINE: per stratum, the null bar frozen on disk
BEFORE the stratum's real-arm decode (exp173's protocol: the shared
arm-1 null, bar = max |pooled null stat| over exp142's deposited
seeds x own-targets); byte-offset assertion per stratum.

GATES (each evaluated exactly once):

  GATE-W1 (strata integrity) both strata built; per-pair
           construction asserts hold (A1 == A2, S_2 == support(A),
           connectivity); the realized-k classification matches the
           construction's own k field 36/36 (or as built).
  GATE-W2 (null discipline) both strata's bars frozen before their
           real arms; byte order asserted; bars finite and > 0.
  GATE-W3 (the density clause) per stratum: |stat| vs its bar and
           the majority-sign count deposited; the DENSITY question
           answered by the pre-named pattern: (i) k=4 stratum
           flips/weakens while k=3 holds — density effect CONFIRMED;
           (ii) both strata hold — density NOT the covariate;
           (iii) both flip — the sign is construction-generic.
           ALL THREE branches complete the gate; the branch taken
           is the finding.
  GATE-W4 (attribution) |stat_m2| <= its bar in BOTH strata.

NO post-hoc tuning. A --smoke check (ladder pairs 0-1, features
only) is permitted before the credited run and discarded.

DEPOSIT: results/exp183_k_controlled_cohort.json

RUN:
  python3 -m experiments.exp183_k_controlled_cohort          # full
  python3 -m experiments.exp183_k_controlled_cohort --smoke  # check
  python3 -m experiments.exp183_k_controlled_cohort --stratum 4
  # jobs: build | k3 | k4
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


LADDER = list(range(183001, 183037))
STRATUM_SIZES = (6, 6)

OUT = os.path.join(ROOT, "results", "exp183_k_controlled_cohort.json")
DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "k3", "k4", "all"],
                    default="all")
    ap.add_argument("--stratum", type=int, choices=[3, 4], default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--stratum/--out)
