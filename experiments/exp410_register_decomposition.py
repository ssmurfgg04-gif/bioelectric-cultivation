#!/usr/bin/env python3
"""exp410 — THE REGISTER'S MEMORY CONTENT: WHAT ACCUMULATES? (batch
HU-10; handoff Test 1 — the history register as "qi refinement").
exp289 landed HISTORY-CARRIED, exp292 the dose/source faces, exp293
PROTECTED (P = +0.73 mV), exp408 REFINEMENT-REGIME-MAPPED (the register
is UNSIGNED — protection and corruption share the same carryover). THE
OPEN QUESTION: the register is self-dominant, dose-peaked, and
super-additive under stress — but memory OF WHAT? Three candidates,
all pre-named: (M-EVENT) memory of the stress event itself; (M-CORRECT)
memory of the correction walk's commits; (M-REGIME) memory of the
regime (the settled program's own writes). The register is a single
unsigned channel, so the candidates are decomposed COUNTERFACTUALLY,
not by reading a sign: run the landed 2×2 machinery with one candidate's
contributing writes REMOVED at a time and measure the rescue R each way.

THE INSTRUMENT (exp293's landed 2×2 form on the planarian replica;
zero new knobs — every condition is a write-schedule intervention on
the landed coupling):
  the corpus replica host (n=400, the exp256 battery discipline), the
  canonical identity target, the settled program (30 tu) defines
  phi_spec; the wound zone corrupted; the BFS boundary walk,
  STEPS_PER_CELL 8, COMMIT_NOISE 0.6; the register blend at the
  boundary cells g_ctx = 0.5 (the exp403 pre-named ON dose); the
  register populated AT THE WRITE. 4 pre-named hosts x 3 seeds
  (disclosed budget reduction from the 72-row battery: the
  decomposition adds 3 conditions x the dose crossing).
  C-FULL   — the canonical form: wound + register ON + correction walk
             (the rescue R_FULL = err(register OFF twin) − err(ON)).
  C-EVENT  — the correction walk NEVER RUNS: wound + register ON, the
             register holds only stress-era writes (M-EVENT isolated).
  C-CORRECT— the stress NEVER TOUCHES the medium: unstressed wound +
             register ON + correction walk (M-CORRECT isolated).
  C-REGIME — no wound, no stress: the settled program re-walked with
             the register ON (M-REGIME isolated).
  Each condition runs its own register-OFF twin at the same seed; R_X
  is the paired decode-error difference.
  THE DOSE CROSSING: R over the stress-dose ladder {-60, -45, -40,
  -35} (the pin values, exp290's A1 family) x the correction-dose
  ladder {0.5x, 1x, 2x the walk budget}; Spearman |rho| of R against
  each candidate's own dose axis.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, g_ctx
      0.5, the ladders as written); the OFF arms reproduce the
      register-OFF twin bit-exact per seed (same-walk identity); all
      R values finite (fail=STOP).
  G2  THE DECOMPOSITION TABLE: R_EVENT, R_CORRECT, R_REGIME deposited
      per (host, seed); consistency R_FULL >= max(R_*) - 0.05 mV (the
      isolated components cannot exceed the full rescue by more than
      the tolerance — a violation means the write-schedule surgery
      broke the instrument, fail=STOP).
  G3  THE ATTRIBUTION: the dominant component = the one whose dose
      axis R tracks: |rho| >= 0.6 AND >= 0.2 above BOTH runners-up.
  G4  THE PERSISTENCE FACE: R re-measured after {0, 30, 90} tu of
      post-walk drift; the regime candidate predicts the SLOWEST
      decay (R(90)/R(0) highest of the three); deposited per
      condition.
  G5  THE DEPOSIT: the full table + gates + branch as
      results/exp410_register_decomposition.json (fail=STOP).

BRANCH LATTICE (pre-named): G3 fires on C-CORRECT ->
REGISTER-DECOMP-CORRECTION (the register remembers the FIX — "qi
refinement" is memory of the correction); on C-EVENT ->
REGISTER-DECOMP-EVENT (memory of the insult); on C-REGIME ->
REGISTER-DECOMP-REGIME (memory of the regime — exp408's unsigned
carryover is regime memory); no component meets G3 -> REGISTER-DECOMP-
MIXTURE (refinement is irreducibly plural). G1/G2 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: "qi refinement" gets a mechanism name — the
register is memory OF something specific, which determines what it is
good for: correction memory = a tutor; event memory = a scar; regime
memory = an identity. exp408's no-sign finding says protection and
corruption share the carryover; this experiment says which WORLD that
carryover carries.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_LADDER = [-60.0, -45.0, -40.0, -35.0]
CORRECTION_LADDER = [0.5, 1.0, 2.0]
PERSISTENCE_LADDER = [0.0, 30.0, 90.0]
SEEDS = [0, 1, 2]
N_HOSTS = 4
PROD_FLOOR = -60.0
DEPOSIT = os.path.join(ROOT, "results", "exp410_register_decomposition.json")


def main() -> dict:
    raise NotImplementedError(
        "exp410 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
