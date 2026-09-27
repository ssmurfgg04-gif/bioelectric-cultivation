#!/usr/bin/env python3
"""exp425 — THE REGISTER'S DUALITY UNDER CHANNEL SEPARATION (batch
HU-12; exp410's registered follow-up). exp410 landed REGISTER-DECOMP-
MIXTURE: the rescue R_FULL (+1.28 mV, stress-gated) tracks BOTH dose
axes at |rho| ~ 0.6 with OPPOSITE signs (gap 0.008 << the 0.2 bar) —
refinement is irreducibly plural on the SINGLE unsigned register. THE
OPEN QUESTION: is the duality a property of the REGISTER (one channel
cannot be un-pluralized) or of the WRITE SCHEDULE (the two memories
were written interleaved — separating the phases separates the
memories)? The two-channel hypothesis gets its measured shot: the
stress-era writes and the correction-era writes are routed into TWO
separate register channels (a write-schedule intervention on the
landed coupling — exp410's own condition class), the dose crossing
re-run per channel.

THE INSTRUMENT (exp410's 2x2 machinery verbatim + the channel split;
zero new knobs beyond the split itself):
  the exp410 hosts x seeds, the wound zone, the BFS boundary walk
  (STEPS_PER_CELL 8, COMMIT_NOISE 0.6), the register blend g_ctx 0.5.
  ARMS:
    MERGED   — the canonical single register (the exp410 C-FULL form).
    SPLIT    — phi_history_stress receives the stress-era writes only
               (the pin-era spec-layer writes); phi_history_correct
               receives the correction-walk commits only; the decode
               reads the MERGED pair at strength g_ctx/2 each (the
               read-matched form, pre-named).
    STRESS-ONLY — the decode reads phi_history_stress at g_ctx.
    CORRECT-ONLY— the decode reads phi_history_correct at g_ctx.
  THE DOSE CROSSING per arm: the stress ladder {-60, -45, -40, -35} x
  the correction ladder {0.5x, 1x, 2x the walk budget}; Spearman
  |rho| of R against each axis per arm.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the register-OFF twins bit-exact per seed;
      all R values finite (fail=STOP).
  G2  THE CALIBRATION: MERGED reproduces exp410's deposited C-FULL
      R_FULL within 0.10 mV on >= 3/4 hosts (the split instrument
      does not perturb the landed rescue).
  G3  THE SEPARATION: STRESS-ONLY tracks the stress axis |rho| >= 0.6
      with the correction axis |rho| <= 0.3, AND CORRECT-ONLY tracks
      the correction axis |rho| >= 0.6 with the stress axis
      |rho| <= 0.3 (per-host rho, median across hosts).
  G4  THE RECOMBINATION: SPLIT (read-merged) R >= max(R_stress_only,
      R_correct_only) - 0.05 mV on >= 3/4 hosts (the channels are
      additive at read, the exp419 composition sense).
  G5  deposit results/exp425_register_channel_split.json.

BRANCH LATTICE: DUALITY-SEPARABLE (G3 PASS) / DUALITY-ENTANGLED (G3
REFUTE — the duality survives the schedule surgery: the register's
pluralism is in the CHANNEL, not the schedule) / INSTRUMENT-REFUTED
(G1/G2 fail). G4's own PASS/REFUTE is deposited beside the branch
(additive-at-read vs interfering-at-read), not folded into it.

THE HONEST STAKES: exp410's plural register is the batch's central
mechanism finding; if the schedule separates it, the "qi refinement"
story acquires an engineering handle (write the phases separately,
read them separately); if it does not, the unsigned single-channel
register is a REAL structural commitment of the model.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
PIN_LADDER = [-60.0, -45.0, -40.0, -35.0]
WALK_LADDER = [0.5, 1.0, 2.0]
N_HOSTS = 4
SEEDS = [0, 1, 2]
RHO_OWN = 0.6
RHO_OTHER = 0.3
MERGED_TOL = 0.10
RECOMB_TOL = 0.05
DEPOSIT = os.path.join(ROOT, "results",
                       "exp425_register_channel_split.json")


def main() -> dict:
    raise NotImplementedError(
        "exp425 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
