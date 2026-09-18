#!/usr/bin/env python3
"""exp237 — THE NCA CLONE BOUND (Hansali 2025, IEEE TMBMC — the direct
computational parallel; the Section 6 item; ledger L213).

THE OPEN QUESTION: Neural Cellular Automata (per-cell local updates with
a perception vector and a residual rule) regenerate target patterns from
local information alone — Hansali 2025's NCA is the literature's
computational parallel of the stack. The test: is the stack's
regeneration competence reproducible by a purely LOCAL rule (the NCA
claim), or does the stack's memory layer (theta — the homeostatic
target, D3's distributed property) carry information a local rule
cannot capture?

THE INSTRUMENT (zero-knob, a behavioral clone, no training loop beyond
least squares): on the torus arm (the NCA-native topology), record the
stack's own transitions (V, theta) over the regeneration window after
the standard amputation (exp73's protocol) — the dataset D = {(x_t, x_
t+1)} of per-cell states with the canonical neighborhood. The CLONE: a
linear local rule x'_t+1 = W @ phi(x_t) with the perception vector
phi = the NCA standard: (self, neighbor-mean, neighbor-std) per layer
(V and theta), fitted by ridge least squares on D. TWO clones: the
CLONE-WITH-MEMORY (phi includes theta; 9 features) and the CLONE-WITHOUT
(phi includes V only; 5 features — the pure-NCA perception). The bound
test: each clone runs ITS OWN closed-loop regeneration from the wound
state; the stack's regen is the reference.

PRE-REGISTERED GATES:

  H1  THE ONE-STEP FIDELITY: the clone-with-memory's one-step prediction
      R^2 >= 0.95 on held-out transitions (the stack's local update IS
      locally predictable); the clone-without's R^2 reported beside it
      (pre-named expectation: strictly lower — V alone does not predict
      the update because dV depends on theta).
  H2  THE CLOSED-LOOP REGEN BOUND: the clone-with-memory completes the
      regeneration (final err < 6.0, exp79's bar) on the torus at 3
      seeds; the clone-without FAILS (err >= 2x the bar) — the memory
      layer's information is NECESSARY for the regen competence: the
      stack is NOT reducible to a memoryless NCA.
  H3  THE HANSALI PARALLEL (the convergence claim): the clone-with-
      memory's closed-loop trajectory stays within the stack's own
      trajectory tube (the max per-cell deviation <= 2x the stack's
      seed-to-seed spread at every checkpoint) — the LOCAL rule
      reproduces the COMPETENCE (the NCA parallel is real: a local
      perceptron suffices WHEN the perception includes the memory).

THE BRANCH (pre-named): H2 PASS (with-memory completes, without fails)
-> MEMORY-NECESSARY (the stack's regen is NOT a memoryless-NCA
phenomenon; the theta layer is the irreducible difference — the
Hansali/Levin memory claim grounded computationally); H2 REFUTE ->
REDUCIBLE (a memoryless local rule regenerates the pattern — the
memory's information is dispensable, deposited honestly).

RUN: the transition recording + 2 ridge fits + the closed-loop panels;
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
OUT = os.path.join(ROOT, "results", "exp237_nca_clone_bound.json")


def main() -> dict:
    raise NotImplementedError(
        "exp237 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
