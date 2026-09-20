#!/usr/bin/env python3
"""exp296 — THE CROSS-CHANNEL HISTORY SWEEP: DOES THE CARRIER
GENERALIZE BEYOND CTX? (batch 49; ledger L277's registered next (i)
== L269's registered next (iii) — exp289 landed HISTORY-CARRIED on
the ctx channel (the interior-context coupling reading the
self-history: 12/12 improved, monotone to the g ~ 1.0 plateau),
exp292/295 mapped the carrier's geometry (self-sourced,
plateau-robust, the social form poisoned), exp293 landed PROTECTED
(super-additive stress protection), exp294 landed PREMIUM-MIXED (the
noise-carried premium fraction dissolves). THE OPEN ARCHITECTURAL
QUESTION: the schema carries EIGHT channels; the history carrier
worked on ONE (ctx). Do the OTHER FOUR dormant channels'
history-reading forms also carry — or was ctx the only channel whose
dynamics had a history-shaped hole? The sweep: each dormant channel's
landed activation form re-run with its coupling term reading
phi_history (the self form at the plateau dose g=1.0) instead of its
landed source.)

THE ARMS (each channel's landed form + the history source swap, zero
new knobs — the dose is the landed plateau g=1.0 for all four):
  GJ-HIST   — ch2 (the pair-cell canonical-match compensation,
              exp259's landed form) reading phi_history;
  STR-HIST  — the de-pairing structural form (exp260's landed form)
              reading phi_history;
  CA2-HIST  — the BETSE-grounded calcium channel (exp261's landed
              form) reading phi_history;
  AP(OP)-HIST — the apoptosis channel (exp263's/exp264's landed
              form) reading phi_history.
Each arm's control is its own landed no-history arm (the channel's
deposited errs from its own ledger deposit — the bit-exact anchor).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each arm's no-history control reproduces its
      channel's deposited errs BIT-EXACT 72/72 (the four deposits:
      exp259/exp260/exp261/exp263-264's battery records — the
      specific deposit paths read from the ledger's L-numbers at the
      body's build); the ctx-HIST arm (exp289's form, the positive
      control) reproduces exp289's deposited g=1.0 errs BIT-EXACT
      72/72; the S* lock reads 360 (5 arms x 72); the floor -60.0
      throughout; the deposits READ-ONLY (the pre-named 11:
      exp243/256/272/273/282/287/288/289/292/293/295), sha
      before/after.
  G2  THE FORMS' DEFINITION (zero-knob asserted, fail=STOP per row):
      each arm's coupling reads phi_history[i] (the self form —
      exp295's plateau verdict fixed the source); the register's
      replay equality per arm at the PER-ARM 72/72 scope; the
      complement 72/72 per arm; the coupling's non-history path
      (each channel's landed term) UNCHANGED (the landed form's own
      asserts re-run per arm).
  G3  THE SWEEP BRANCH (pre-named numeric bars): per channel the
      72-row mean paired delta vs its own control (the
      anchor-minus-arm improvement form); the channel CARRIES iff
      its mean delta < -0.05 mV (the house margin) AND the
      per-host improvement clause >= 10/12; the sweep:
      CARRIER-GENERAL  iff >= 3 of the 4 channels carry;
      CARRIER-PARTIAL  iff 1-2 carry (the carried channels named);
      CARRIER-CTX-ONLY iff 0 carry (ctx was the only hole — the
          honest null, the channel-specificity face).
      Audit-only: the per-host per-channel delta table, the
      worst-err per arm vs the 6.0 bar (unchanged), the R_max face
      per arm (audit), the H3/H5 deltas.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): CARRIER-GENERAL / CARRIER-PARTIAL /
CARRIER-CTX-ONLY.

RUN: 360 decodes ~ 5-8 min — the pre-named form is the CHECKPOINT-
SPLIT EXP296_MODE=pass1 (GJ-HIST + STR-HIST, 144) | pass2 (CA2-HIST
+ AP-HIST + the ctx-HIST positive control, 216) | merge; the
in-process default for the GitHub runners. Both forms evaluate the
SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp296_channel_sweep.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp296's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
