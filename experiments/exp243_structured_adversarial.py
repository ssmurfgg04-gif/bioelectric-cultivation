#!/usr/bin/env python3
"""exp243 — STRUCTURED ADVERSARIAL MEDIA (the Section 6 item; the Stage 5
extension; exp225 held 0.62 mV on structured media, exp198's n=400
random worst 1.45; ledger L219).

THE OPEN ITEM: the reader held on structured media and on random media
separately; the UNTESTED cell is the conjunction — media that are BOTH
structured AND adversarial: the adversary designs the medium INSIDE the
structured class to maximize the reader's decode error. The honest
adversary (zero-knob): the structured family is exp225's (the pre-named
structured constructors); the adversary = the WORST member of the
family by the reader's own error — found by a bounded search the
docstring pre-names (the grid over the family's discrete parameters:
exp225's structured classes x the pre-named perturbation set {the
canon/zone relabelings, the boundary-double-frequency rewiring, the
deep-band substitution} — the adversary picks the argmax over the
PRE-NAMED candidate list, no continuous optimization, no fitting).

PRE-REGISTERED GATES:

  A1  THE ADVERSARIAL-STRUCTURED HOLD: the reader's worst err over the
      full adversarial candidate list x 3 seeds < 6.0 at n=400 (the
      production read, exp225's machinery verbatim).
  A2  THE CONJUNCTION COST: the adversarial-structured worst err vs the
      structured-only worst (exp225's deposited 0.62) and the random
      worst (exp198's 1.45) — the conjunction's price recorded; the
      gate: the adversarial-structured worst < 2x the random worst
      (the structured class does not hide a 2x worse cell).
  A3  THE ADVERSARY'S ANATOMY: the argmax candidate named (which
      pre-named perturbation class wins) and its error decomposition
      (the canon-boundary share via exp208's machinery — the boundary
      signature's presence under adversarial design).
  A4  THE DISCIPLINE: the floors save/restore asserted, the MULTI
      identity audits bit-identical, zero rejections, all finite.

THE BRANCH (pre-named): A1 PASS -> ADVERSARIAL-HOLD (the reader holds
on the conjunction — the Stage 5 media axis closes); A1 REFUTE ->
ADVERSARIAL-BREAK (the conjunction breaks the reader — the honest
limit and the read architecture's named cost).

RUN: the candidate list x 3 seeds at n=400; serial, BLAS pinned;
minutes.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp243_structured_adversarial.json")


def main() -> dict:
    raise NotImplementedError(
        "exp243 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
