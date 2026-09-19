#!/usr/bin/env python3
"""exp270 — THE STRUCTURAL DOSE (batch 28; L247's registered next —
the substitution's event size as the parameter the voltage ladder
could not see).

THE OPEN ITEM (L247): the read's response to the deep-band
substitution is CATEGORICAL — flat in the rung voltage inside the
identity repertoire, hard-refused beyond it. The unmeasured dose
face: the substitution's EVENT SIZE — how many of MULTI's zones the
rewrite touches. The battery's substitution rewrites ONE zone (the
deep band's single-zone form at -60.0, the exp256 anchor). The
structural dose curve: the zone count scaled.

THE INSTRUMENT (pre-registered, zero-knob): the pre-named zone-count
ladder {1, 2, 4, 8, 16} — at each dose d, the substituted target
rewrites the FIRST d zones of MULTI's zone skeleton to the -60.0
rung (the exp256 construction's own form, the zone subset the
pre-named first-d rule, deterministic); x the 12 hosts x 3 seeds
(one instance per dose — the instance axis is pre-named i0, the
battery's own first instance); the -60.0/d=1 form is the exp256
anchor (the i0 rows) and must reproduce bit-exact.

PRE-REGISTERED GATES:

  Z1  THE ANCHOR: d=1 reproduces exp256's deposited i0 substituted
      errs bit-exact (24 values; fail = STOP, no tuning).
  Z2  THE CURVE: all 5 doses x 24 rows complete, finite, zero
      rejections (rows that hit the compiler's repertoire floor are
      RECORDED refusals, never patched — the dose at which the
      refusal fires is itself the measurement).
  Z3  THE DOSE FACE: the pooled monotonicity (Spearman d vs err) and
      the per-dose means reported; the gate: monotonicity >= 0.5
      (the categorical response HAS a structural dose curve) or the
      honest flat refusal branch.
  Z4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (the d=2 form re-run on 6 hosts bit-identical);
      no wall-clock fields.

THE BRANCHES (pre-named): DOSE-CURVE (Z3 passes) / FLAT-REFUSAL.

RUN: 5 doses x 24 rows (~1.3 s/row ≈ 2.6 min) — one segment.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp270_structural_dose.json")


def main() -> dict:
    raise NotImplementedError(
        "exp270 body pending — pre-registration commit only")
