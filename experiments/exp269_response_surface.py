#!/usr/bin/env python3
"""exp269 — THE RESPONSE-SURFACE SAMPLE (batch 27; L246's registered
next (a) — the read's err surface sampled over the substitution's own
parameter: the deep rung's voltage ladder).

THE OPEN ITEM (L246): the boundary residual is deterministic-per-
instance, arm-carried, and irreducible at every decomposition level
(substrate, target, law, stages, channels). The one measurement never
taken: the read's response SHAPE — how the err moves as the
substitution's own parameter (the deep rung's voltage) sweeps. The
battery sampled the rung at -60.0 only; the dose-response curve is
the direct measurement of the response surface the stage ablations
proved non-decomposable.

THE INSTRUMENT (pre-registered, zero-knob): the pre-named rung
ladder {-30, -40, -50, -55, -60, -65, -70} mV x the 12 hosts x 3
seeds x 2 instances (the exp172/exp214 deep construction at each
rung; the -60.0 rung is the battery's own anchor and must reproduce
exp256's deposited errs bit-exact). The per-host curve: worst err vs
rung; the pre-named shape reads:

  D1  the curve's monotonicity per host (Spearman |rung| vs err);
  D2  the curve's inflection (the rung where the err crosses the
      battery's own worst-canonical mean — the "the substitution
      starts to cost here" point);
  D3  the curve's end-behavior (does the err saturate at the
      extreme rungs or diverge — the response surface's face at the
      physiological boundary).

PRE-REGISTERED GATES:

  U1  THE ANCHOR: the -60.0 rung reproduces exp256's deposited
      substituted-row errs bit-exact (72 values; the machinery
      anchor; fail = STOP, no tuning).
  U2  THE SURFACE: all 7 rungs x 72 rows complete, finite, zero
      rejections; the per-host curves deposited.
  U3  THE SHAPE: the monotonicity/inflection/saturation reads
      reported per host and pooled; the gate: the pooled
      monotonicity Spearman >= 0.5 (the response has a directed
      shape — the surface is a curve, not a scatter) AND the
      extreme-rung behavior named (saturating or diverging).
  U4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (the -60.0 rung re-run IS the anchor; the
      -65.0 rung re-run on 6 hosts bit-identical); no wall-clock
      fields.

THE BRANCHES (pre-named): CURVE (U3 passes — the response surface
has a directed, nameable shape) / SCATTER (it does not).

RUN: 7 rungs x 72 rows at n=400 (~1.3 s/row ≈ 11 min) — checkpoint
segments per rung pair.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp269_response_surface.json")


def main() -> dict:
    raise NotImplementedError(
        "exp269 body pending — pre-registration commit only")
