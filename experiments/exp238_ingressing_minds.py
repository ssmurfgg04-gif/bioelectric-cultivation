#!/usr/bin/env python3
"""exp238 — THE INGRESSING MINDS TEST (the Section 6 item; "Ingressing
Minds", MDPI 2409-9287/11/5/161; ledger L214).

THE CLAIM TESTED: a single body can host MULTIPLE, simultaneously
retrievable morphological memories — "multiple memories in the same
body" — and which memory surfaces is decided by the READ, not by
competitive storage. The stack already carries the two-layer substrate
for the claim: theta (the expression memory) and phi_spec (the spec/
identity memory, set_target's write-once layer) — two addressable
stores on ONE substrate at S* = (64.0, 0.0).

THE DESIGN (zero-knob): pattern A = the canonical labeling (exp43's
head/trunk); pattern B = a CONFLICTING zone map on the same cells
(the mirror labeling: the head zone relocated to the posterior third —
the two patterns disagree on >= 60% of cells, pre-named). The write
sequence: A into theta via the star write protocol (exp79's run_gm
verbatim), B into phi_spec via write_spec_layer (exp87's frozen
machinery, the R1 memory write). Then the retrieval battery.

PRE-REGISTERED GATES:

  M1  THE CO-EXISTENCE: both memories retrievable after the write
      sequence at S* on all 3 arms x 3 seeds — the expression read
      reports A (theta vs A: err < 6.0) AND the spec read reports B
      (phi_spec == B bit-exact) simultaneously.
  M2  THE NON-INTERFERENCE: running under A's expression (the star
      maintenance window T=24 x 3 rounds) does not corrupt B (phi_spec
      bit-exact before/after, sha-compared) and B's presence does not
      degrade A's maintenance (err within 0.5 mV of the B-free
      control).
  M3  THE CONFLICT (the claim's core): A and B disagree on >= 60% of
      cells AND both remain retrievable — "multiple memories in the
      same body" realized computationally at S*.
  M4  THE ADDRESSING (the ingress claim): which memory surfaces is
      decided by the READ PROTOCOL alone — the window read surfaces A,
      the spec read surfaces B, with ZERO re-writes between
      retrievals (the memory is addressed, not re-expressed); the
      switching is lossless (A's err identical before/after a B
      retrieval round, bit-exact theta).

THE BRANCH (pre-named): M1-M4 PASS -> MULTI-MEMORY-CONFIRMED (S*
reproduces the "multiple memories in the same body" claim — the
Ingressing Minds parallel grounded in the stack); M1 or M2 REFUTE ->
SINGLE-MEMORY (the two-layer substrate does not host independent
memories — the expression erases the spec, deposited honestly).

RUN: the write sequence + 4 retrieval panels x 3 arms x 3 seeds;
serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp238_ingressing_minds.json")


def main() -> dict:
    raise NotImplementedError(
        "exp238 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
