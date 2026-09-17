#!/usr/bin/env python3
"""exp193 — THE CONDITIONED ENSEMBLE TO PRODUCTION (the adoption).

exp188's registered next (L164): the k=3-conditioned statistic as the
production grouping read — the exp178-pattern additive arm, bit-exact
at every old operating point.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp163/exp183/exp188's modules and deposits verbatim; the -35.0 pin.

GATES (each evaluated exactly once):
  GATE-F1 (the wiring) exp163's module gains the additive
           function conditioned_stat(pairs) (the k=3-stratum signed
           mean, realized-k from the construction); the existing
           unconditioned path untouched; tests green post-wiring.
  GATE-F2 (old operating points bit-exact) exp163's and exp174's
           deposited verdicts replay bit-exactly through the
           UNCHANGED unconditioned path (per-pair devs + stats, both
           cohorts); exp183's and exp188's stratum stats replay
           bit-exactly through the conditioned arm (third+second
           cohorts).
  GATE-F3 (the production property) the conditioned arm's
           classification rule (stat > bar AND majority sign)
           reproduces exp188's D3 verdict on the third cohort and
           exp183's W3 branch (i) on the second — the production
           rule agrees with every deposited verdict.
  GATE-F4 (hygiene) zero rejections; pin save/restore asserted.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp193_conditioned_ensemble_production.json
RUN: python3 -m experiments.exp193_conditioned_ensemble_production [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp193_conditioned_ensemble_production.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
