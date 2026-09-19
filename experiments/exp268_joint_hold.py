#!/usr/bin/env python3
"""exp268 — THE JOINT HOLD (batch 26 item 2; L245's registered next —
the S1 x S3 stages canonicalized SIMULTANEOUSLY).

THE OPEN ITEM (L245): the arm contrast's stage shares are the
projection 0.4406 and the executor 0.1990 (jointly 0.64) with 0.3604
unexplained by any single stage. The joint hold decides between:
(a) the INTERACTION is the carrier — holding both stages closes the
contrast beyond the sum of the singles; (b) the 0.36 is the joint's
irreducible face.

THE INSTRUMENT (pre-registered, zero-knob; exp267's machinery
verbatim): the J arm — both the projection (PN1/PN2 from the canon
row's medium) and the executor (the canon row's A_ext walk with the
substituted row's target at the error read) held simultaneously, on
the same 72 rows (12 hosts x 3 seeds x 2 deep instances). The
comparison set: exp267's deposited S0/S1/S3 rows (the singles) and
the fresh J rows.

PRE-REGISTERED GATES:

  J1  THE ANCHORS: S0 and the singles re-read from exp267's deposit
      (byte-verified); the J arm's canon-row reference decodes
      reproduce exp256's/exp267's canon anchors bit-exact.
  J2  THE JOINT CLOSURE: the joint hold's delta share (S0 - J)
      computed by the exp262 convention; the gate: the joint share
      >= 0.5 AND exceeds max(single shares) + 0.10 (the interaction
      adds beyond the dominant single — the carrier is the JOINT).
  J3  THE IRREDUCIBLE FACE: the residual after the joint hold (the
      share of (S0 - J) NOT explained — i.e. 1 - joint share)
      reported; if J2 fails, the branch names the honest reading:
      either the singles' sum already saturates (joint ~ max single)
      or the contrast survives both stages (the read's response is
      not stage-decomposable at all).
  J4  THE DISCIPLINE: exp267's/exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (J re-run on 6 hosts, bit-identical); no
      wall-clock fields.

THE BRANCHES (pre-named): JOINT-CARRIES (J2) / SATURATED / NOT-
STAGE-DECOMPOSABLE — each names the residual's final disposition at
the read-stack level honestly.

RUN: 72 J rows at n=400 (~1.3 s/row); foreground segment.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp268_joint_hold.json")


def main() -> dict:
    raise NotImplementedError(
        "exp268 body pending — pre-registration commit only")
