#!/usr/bin/env python3
"""exp267 — THE READ-STAGE ATTRIBUTION (batch 26; L244's registered
next — the arm contrast localized INSIDE the read stack).

THE OPEN ITEM (the two-line convergence, L243+L244): the residual's
rank variance is 75.7% arm (exp262), the arm share is NOT the
target's geometry (exp265) and NOT closable by deposit-level
structural terms (exp266) — it is the READ's own response to the
deep-band substitution. Which STAGE of the read stack carries it?

THE INSTRUMENT (pre-registered, zero-knob; the exp208
c6-tail-ablation mold applied to the read's stages): re-run the
substituted rows' decodes (exp256's 12 hosts x 3 seeds x 2 deep
instances = 72 rows) with each read stage's output held at its
CANONICAL-row value in turn — the canonical value is the same
stage's output on the SAME host's canon row (the P1/P2 battery's
row), same seed. Four arms:

  S0  the baseline (no hold) — the substituted rows as exp256 ran
      them (the reproduction anchor: the errs must reproduce
      exp243's/exp256's deposited values bit-exact);
  S1  the PROJECTION held (PN1/PN2 phase projection computed on the
      canon row's medium, applied to the substituted decode);
  S2  the FLIP-CLOCK held (TC1's F matrix from the canon row);
  S3  the EXECUTOR held (exp142's execute_signed run on the canon
      row's A_ext, the substituted row's target swapped in at the
      error read — the walk itself canonicalized).

The arm contrast's carrier = the stage whose canonicalization
CHANGES the substituted rows' errs the most (the rank-variance share
of the (S0 - Sk) delta across rows, the exp229/exp262 convention on
the delta ranks).

PRE-REGISTERED GATES:

  R1  THE REPRODUCTION: S0 reproduces the deposited errs bit-exact
      (72/72; the machinery anchor).
  R2  THE ATTRIBUTION: the three stage deltas' rank-variance shares
      reported; the gate: ONE stage's share >= 0.5 (the carrier is
      single-stage — the residual localizes inside the stack).
  R3  THE HONESTY CLAUSE: if no stage reaches 0.5, the contrast is
      DISTRIBUTED (the read's stages interact — deposited honestly,
      the shares named).
  R4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the read stack's production
      fingerprint asserted pre/post (exp160's READ_CONFIG); the
      -60.0 floor restored and asserted at exit (the exp169 import
      chain pins -35.0 — the explicit restore); deterministic
      (S0/S1/S2/S3 re-run on 6 hosts, bit-identical); no
      wall-clock fields.

THE BRANCHES (pre-named): STAGE-CARRIES (R2) / DISTRIBUTED (R3).

RUN: 4 arms x 72 rows at n=400 (the scoped read ~1.3 s/row) —
foreground segments or a runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp267_read_stage_attribution.json")


def main() -> dict:
    raise NotImplementedError(
        "exp267 body pending — pre-registration commit only")
