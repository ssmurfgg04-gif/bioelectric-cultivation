#!/usr/bin/env python3
"""exp411 — THE DISSOLUTION SHAPE AND THE MEMORY-DISCIPLINE FACE
(batch HU-10; handoff Test 2a). exp407 landed BYPASS-EXPLAINED: the
composed carrier's +0.0000 mV stress delta is the SATURATION limit —
at g=1.0 the commit reads the register chain, a channel the stress
cannot reach — and G4 landed the dissolution MONOTONE as g falls
{1.0, 0.75, 0.5, 0.25, 0.0}. TWO questions stay open. (1) THE SHAPE:
is the dissolution THRESHOLDED (dynamics re-enter at a g* — the
register chain stops dominating abruptly) or GRADUAL (the two channels
blend continuously)? A threshold means a SAFE operating band exists
(carrier ON, dynamics readable below g*); gradual means every carrier
strength buys invisibility with the same coin. (2) THE DISCIPLINE
FACE: exp407 moved the practical target to "memory-write discipline".
Can a two-pass write — commit saturated at g=1.0, then ONE refresh
pass at g=0.5 re-exposing the memory to dynamics — keep the carrier's
improvement while returning stress visibility? If yes, the discipline
recipe exists; if the refresh destroys the carrier, the discipline is
costly and the trade is quantified.

THE INSTRUMENT (exp407's landed form VERBATIM): path(100), the 3-zone
spec [-50 x40, -30 x30, -20 x30], faces (ctx, gj) — the apop sigma
face excluded as exp407 excluded it; the write-time -35.0 pin
(exp290's A1), restored -60.0; COMMIT_NOISE 0.6, STEPS_PER_CELL 8;
the register populated at the write.
  F-SHAPE: the fine g ladder {1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6,
           0.5, 0.25, 0.0} x stress {off, on} x 10 seeds (exp407's 5
           seeds kept + 5 additive, disclosed); |Delta(g)| = the mean
           |err(on) - err(off)| per g; Hill fit |D(g)| = Dmax * g*h^n
           / (g*h^n + g^n) vs the linear fit on the same 10 points
           (least squares on the means, zero knobs).
  F-DISCIPLINE: the two-pass arm — the standard walk with the blended
           cells committed at g=1.0, then ONE refresh pass over the
           same cells at g=0.5 (write = 0.5*theta_new + 0.5*
           phi_history), then the settle; the stress 2x2 on the
           two-pass form; carrier retained = the two-pass improvement
           vs register-OFF >= 0.8 x the g=1.0 one-pass improvement;
           visibility returned = |Delta_two-pass| >= 0.10 x the
           g=0.0 one-pass mean |Delta|.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      pin -35.0, the ladders as written); at the shared 5 seeds the
      g=1.0 and g=0.0 arms reproduce exp407's deposited per-seed
      deltas BIT-EXACT (the anchor; the 5 additive seeds disclosed).
  G2  THE MONOTONE FACE RE-CONFIRMED: |Delta(g)| non-decreasing as g
      falls across all 10 ladder points (ties allowed), 10/10 seeds
      finite.
  G3  THE SHAPE BRANCH: thresholded iff Hill R^2 > linear R^2 + 0.10
      on the 10 mean points; g* (the Hill half-point) deposited if
      thresholded.
  G4  THE DISCIPLINE FACE: both pre-named conditions evaluated once,
      numbers deposited; VIABLE iff carrier retained AND visibility
      returned; COSTLY otherwise (which condition failed, deposited).
  G5  THE DEPOSIT: the ladder table, both fits, the two-pass table,
      gates + branch as results/exp411_invisibility_dissolution.json
      (fail=STOP).

BRANCH LATTICE (pre-named): DISSOLUTION-THRESHOLDED +
MEMORY-DISCIPLINE-VIABLE (the safe band exists AND the recipe works —
the carrier story closes both ways); DISSOLUTION-THRESHOLDED +
MEMORY-DISCIPLINE-COSTLY; DISSOLUTION-GRADUAL + VIABLE; DISSOLUTION-
GRADUAL + COSTLY (no safe band, no recipe — the invisibility is the
carrier's price at every strength). G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: exp407 said build commit layers that read memory,
not dynamics. This experiment says whether the reading can be SCHEDULED
(a band, a recipe) or only bought (a trade). A thresholded dissolution
with a viable discipline face is an engineering result; the gradual +
costly branch is the honest negative that closes the practical story.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
GLADDER = [1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5, 0.25, 0.0]
REFRESH_G = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ANCHOR_SEEDS = [0, 1, 2, 3, 4]
DT = 0.1
WINDOW = 30.0
DEPOSIT = os.path.join(ROOT, "results", "exp411_invisibility_dissolution.json")


def main() -> dict:
    raise NotImplementedError(
        "exp411 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
