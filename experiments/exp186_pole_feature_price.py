#!/usr/bin/env python3
"""exp186 — THE POLE-FEATURE PRICE (does any substrate WANT the deep
pole readout?).

exp175's registered next (L154): with the M33 split in production
(M33_LINE = -35.0), the disclosed open question stands — "whether any
substrate WANTS pole-eligible deep identities (the -60 pole readout as
a feature)". THIS EXPERIMENT prices it as a counterfactual: substrates
at deep identities under blockade, M33 armed at the DEEP line (the
pre-split CF-1 world) vs the production line (the split world) — does
arming the pole readout at -60 HELP or HURT the substrate's identity
read?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Arms, weights, and gates are fixed now.

THE ARMS (the engine-variant mechanism, exp156's decode_cf discipline
— one constant rebound per arm, save/restore asserted):
  ARM-PROD — the production split core (M33_LINE = -35.0): deep
             identities get NO pole readout.
  ARM-DEEP — M33_LINE rebound to -60.0 in the one module that binds
             it: deep identities GET the pole readout (the CF-1-world
             M33 behavior, exp171's measured collapse world).
  THE SUBSTRATES: exp171's four identity families (HEAD -20, LINE
  -35, TRUNK -50, DEEP -60) at neural_w = 0.5, r = 0.05, seeds
  (1, 2, 3) — exp171's protocol verbatim, now with the SPLIT core.
  THE PRICE: per family, err = |guess - spec| at the blocked plane
  pooled over seeds, arm-PROD vs arm-DEEP; the FEATURE question is
  the SIGN of (err_DEEP - err_PROD) on the TRUNK/DEEP families:
  negative = the deep pole readout HELPS (a feature worth arming);
  positive = it HURTS (the split is not just literature-faithful,
  it is substrate-correct).

GATES (each evaluated exactly once):
  GATE-Z1 (production replay) ARM-PROD reproduces exp175's P2
           records bit-exactly (the four families, seeds (1,2,3):
           TRUNK/DEEP == exp171's pinned arm, HEAD/LINE unchanged).
  GATE-Z2 (the counterfactual is live) ARM-DEEP differs from
           ARM-PROD on TRUNK/DEEP (the pole branch fires; the
           first divergent step reproduces the M33 blend exactly,
           exp171's M2 discipline) and is BIT-IDENTICAL on
           HEAD/LINE (the line only moved below -35).
  GATE-Z3 (the price) per family the signed delta deposited; the
           verdict branch pre-named: HELP iff BOTH TRUNK and DEEP
           deltas < 0; HURT iff BOTH > 0; MIXED otherwise. All
           three branches complete the gate.
  GATE-Z4 (hygiene) rebind save/restore asserted both arms; zero
           non-finite values.

NO post-hoc tuning. --smoke (TRUNK, seed 1, both arms) permitted,
discarded. Deposit: results/exp186_pole_feature_price.json
Jobs: prod | deep
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

import cultivation.bioelectric.collective as core  # noqa: E402

FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}
NEURAL_W = 0.5
N_CELLS = 100
SEEDS = (1, 2, 3)
PROD_LINE = -35.0
DEEP_LINE = -60.0

OUT = os.path.join(ROOT, "results", "exp186_pole_feature_price.json")
DEP171 = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")
DEP175 = os.path.join(ROOT, "results", "exp175_m33_split.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["prod", "deep", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
