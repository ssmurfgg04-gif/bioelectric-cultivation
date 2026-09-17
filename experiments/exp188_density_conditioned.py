#!/usr/bin/env python3
"""exp188 — THE DENSITY-CONDITIONED ENSEMBLE (the grouping read's
production form).

exp183's registered next (from its L160 finding, branch (i)): the
ensemble's sign structure is a DENSITY effect (k = 3 stratum holds,
k = 4 weakens) — the grouping read gains its first structural
covariate. THIS EXPERIMENT conditions the statistic on the covariate
and validates on a THIRD cohort: stat = the signed mean over the
k = 3 stratum ONLY (d_k-conditioned), tested on 36 fresh pairs
(ladder 188001..188036, exp183's protocol verbatim).

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Conditioning, cohort, and gates fixed.

THE CONDITIONED STATISTIC (zero new knobs): per pair, realized k and
d_k recorded; the conditioned stat = the signed mean over the k = 3
stratum ONLY. The unconditioned mean is computed for contrast
(recorded, not gated). Two-phase nulls per stratum (exp183's
protocol): bars frozen on disk before the stratum's real arm.

GATES (each evaluated exactly once):
  GATE-D1 (cohort integrity) 36 fresh pairs, construction asserts
           36/36, realized-k classification 36/36; independence from
           both prior cohorts (no projection bit-equal to any).
  GATE-D2 (null discipline) per-stratum bars frozen before their
           real arms (byte order); finite > 0.
  GATE-D3 (the conditioning claim) on the THIRD cohort: the k = 3
           stratum's conditioned stat > its bar with a majority
           sign (>= 5/6 if 6 pairs exist), AND the conditioned stat
           EXCEEDS the unconditioned stat in magnitude (conditioning
           buys power on independent draws); if the cohort's k = 3
           stratum has < 4 pairs, the gate evaluates on what exists
           (disclosed).
  GATE-D4 (attribution) the k = 4 stratum and the m2 side both
           silent (<= their bars) — the contrast stays attributable.

NO post-hoc tuning. --smoke (ladder pairs 0-1, features only)
permitted, discarded. Deposit: results/exp188_density_conditioned.json
Jobs: build | k3 | k4
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
    build_pair, co_membership, project, connected, T1, T2, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

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


LADDER = list(range(188001, 188037))

OUT = os.path.join(ROOT, "results", "exp188_density_conditioned.json")
DEP183 = os.path.join(ROOT, "results", "exp183_k_controlled_cohort.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "k3", "k4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
