#!/usr/bin/env python3
"""exp239 — THE COUPLING-PLASTICITY FAILURE MODE (the Section 6 item;
Zenodo 21459264's symbol-grounding parallel; ledger L215).

THE CLAIM TESTED: under coupling plasticity (the junction weights
themselves remodel — exp77's drag remodeling, exp78's G-thinning), a
GLOBAL ENERGY FUNCTION may cease to exist for the coupled dynamics —
the "coupling plasticity" failure mode of symbol grounding. The stack's
dynamics at fixed G are a linear coupled system (dV = gamma*(theta-V) +
G-coupling; dtheta = eps*(V-theta) + mu*lap(theta)) — at fixed G a
quadratic Lyapunov function EXISTS (the standard Lyapunov equation).
The question: does the fixed-G Lyapunov certificate survive G's
remodeling, and does the coherence constraint (the maintained pattern's
zone structure) protect it?

THE INSTRUMENT (zero-knob): E(x) = x^T P x with x = (V - theta, theta
- lbl) the deviation state and P the Lyapunov solution of the fixed-G
block system at the star point (P from the discrete Lyapunov equation
on the linearized update operator M: M^T P M - P = -Q, Q = I — solved
exactly by numpy on the stacked operator, no fitting). The test walks
sampled trajectories and checks dE <= 0 at every step.

PRE-REGISTERED GATES:

  E1  THE FIXED-G BASELINE: E decreases along every sampled trajectory
      at the star (gamma=64, mu=0, fixed G; 3 arms x 3 seeds x 200
      steps, zero violations within float tolerance) — the certificate
      exists on the frozen dynamics.
  E2  THE REMODELING BREAK: under G-remodeling (exp77's drag remodeling
      protocol verbatim — the junction weights updated every pre-named
      10 steps by the drag rule), the fixed-G certificate's dE computed
      WITH THE STALE P turns positive on a pre-named fraction of
      remodel steps (>= 1 violation per trajectory on >= 1/3 of
      trajectories): the fixed-G energy is NOT a global energy under
      plasticity — the failure mode fires.
  E3  THE COHERENCE PROTECTION: with the coherence clamp on (the
      pattern maintained at the star: the write held, no wound), the
      remodeling trajectories show dE <= 0 throughout (the maintained
      pattern's neighborhood keeps the certificate locally valid) —
      the constraint's protective effect, the grounding's price
      structure named.
  E4  THE TIME-VARYING CERTIFICATE (the honest extension): the
      pointwise-fresh Lyapunov solution P_t (re-solved at each remodel
      step for the CURRENT G) restores dE <= 0 everywhere — the system
      is not gradient-free, it is gradient-MOVING: a global energy
      exists only piecewise-in-time under plasticity; the failure mode
      is the single fixed E, not the dynamics.

THE BRANCH (pre-named): E2 fires + E4 restores -> PLASTICITY-BOUNDED
(the failure mode is real and LOCALIZED: coupling plasticity breaks
any FIXED global energy while a time-varying certificate persists —
the symbol-grounding parallel grounded computationally); E2 does not
fire -> REMODEL-SAFE (the stack's remodeling preserves the fixed
certificate — deposited honestly).

RUN: the trajectory panels + the Lyapunov solves (the 100x100 stacked
operator, eigen-free solve); serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp239_coupling_plasticity.json")


def main() -> dict:
    raise NotImplementedError(
        "exp239 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
