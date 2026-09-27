#!/usr/bin/env python3
"""exp428 — THE TWO-KEY DECODE BIAS: GROUP x PLANE (batch HU-12;
exp423's registered follow-up). exp423 landed BIAS-PARTIAL: the
per-block bias cuts the test MAE 0.2989 -> 0.2552 (the material cut
landed) but the runs test's |z| = 6.72 persists — the residual sign
structure has a NON-BLOCK component. The next key is pre-named by the
corpus's own anatomy: the per-record `plane` field (the anatomical
region of the recording — the corpus rows carry it; the decode's
errors should key on WHERE the tissue was read, not only on WHAT was
done to it). The lever: a two-key bias, the (group, plane) cell's
median residual, fitted train-only, applied test-only, nested inside
exp423's frozen discipline.

THE INSTRUMENT (exp423's machinery verbatim, the key extended; zero
new knobs):
  the L74 per-row corpus (the scored rows, exp118's per_record with
  per-row errors), the same train/test split (the rows' corpus order,
  even = train, odd = test); the key = the (group, plane) pair from
  the corpus's own fields (no invention; a test row whose cell was
  unseen or train-thin carries bias 0 — the pre-named fallback).
  The ladder's entry point: exp423's corrected test MAE 0.2552
  reproduced first, then the two-key bias applied.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the raw anchor (0.3705/0.2900/0.6928) bit-tight
      within 0.005; exp423's per-block corrected test MAE 0.2552
      reproduced within 0.005 (the ladder's entry point).
  G2  THE DISCIPLINE: train/test disjoint; the two-key bias fitted
      train-only; the fallback rule applied as pre-named; the cell
      support table (train n per (group, plane)) deposited.
  G3  THE GATE: the test-half MAE after the two-key bias <= 0.2402
      (0.2552 - 0.015, a material further cut, pre-named) AND the
      runs test's |z| on the test-half residuals <= 2 (the sign
      structure absorbed, two-sided — the exp415 lesson).
  G4  THE ANATOMY: the two-key bias table deposited (WHICH (group,
      plane) cells over/under-predict, with n each) + the residual
      runs-z ladder (raw / block-corrected / two-key-corrected).
  G5  deposit results/exp428_two_key_bias.json.

BRANCH LATTICE: BIAS-CLOSED (G3 PASS — the model-side gap is the
decode's group x plane bias, repaired with zero new data) /
BIAS-STRUCTURAL (the MAE cut lands, |z| > 2 persists — the sign
structure survives BOTH keys; the gap is not a bias at this
granularity) / BIAS-REFUTED (neither — the plane key adds nothing)
/ INSTRUMENT-REFUTED (G1/G2 fail).

THE HONEST STAKES: the MAE 0.290 story has been decomposed
(exp415: model-side dominant) and partially repaired (exp423: the
block bias); this is the third and finest pre-named key the corpus's
own fields support. If |z| survives it, the residual is STRUCTURAL —
the decode's next repair is a model change, not a bias term.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

ENTRY_MAE = 0.2552
MAE_TARGET = 0.2402
RUNS_Z = 2.0
ANCHOR_TOL = 0.005
MIN_SUPPORT = 3
DEPOSIT = os.path.join(ROOT, "results", "exp428_two_key_bias.json")


def main() -> dict:
    raise NotImplementedError(
        "exp428 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
