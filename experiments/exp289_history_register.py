#!/usr/bin/env python3
"""exp289 — THE HISTORY-REGISTER PORT: GIVING THE DORMANT CHANNELS A
STATE VARIABLE THAT SURVIVES THE WALK (batch 47; ledger L267's
registered next (b) — Sediqi 2026 (bioRxiv 2026-06-23.733978: ionic-
exposure HISTORY shapes voltage/chromatin responses) converges with
Blattner-TAS 2026 (bioRxiv 2026-04-03.715890, github.com/marcelbtec/
tasmorpho: regeneration = a HIDDEN bioelectric state invisible in the
current anatomy) on one architectural move: the programs' writes need
a persistent register. exp288 landed SPEC-UNIFORM — the spec layer's
face is class-blind like every other level — so the frontier is NOT
geometric; L267's (a): the five dormant channels (ctx / pair /
structure / ca2 / apop, exp258/259/260/261/263/264) are inert under
SCHEMA-ONLY activation — the schema carries them, no evolution rule
acts on them. THE MISSING VARIABLE this module ports: the commit
HISTORY — what the program wrote LAST time, carried across walks as
a state variable the dynamics can read.)

THE PORT (additive, zero-knob at defaults): a new per-cell register
`phi_history` on the collective (the 8-channel named array's history
face — the channel values as of the LAST write), populated AT EACH
commit write (the traced replica's disclosed addition (f) site: after
c.theta[i] = theta_new, phi_history[i] = theta_new), initialized to
the spec layer's own values at write_spec_layer time (the history
starts as the program's own target — the never-written cells' history
IS the spec's install). NOTHING reads phi_history at defaults — the
register is recorded, never consumed — so EVERY legacy call site is
bit-exact by construction. G1 PROVES it on the machinery's own anchor:
the full 72-row substituted battery (12 hosts x 3 seeds x r-60i0/r-60i1
at n=400, exp256's battery, the exp287/exp288 traced replica form at
the production budget 8) re-run with the port live reproduces exp256's
deposited substituted errs BIT-EXACT 72/72 (the verified flags 72/72)
— the same S0 anchor discipline as exp287/exp288, now proving the
PORT side-effect-free (plus the repo test suite green from the repo
root).

THE FIRST HISTORY-CARRYING ACTIVATION (ch3 ctx, exp258's registered
channel, its landed form's registered next): the ctx coupling term
re-run reading the HISTORY register — the cell pulled toward its OWN
last commit (the self-history face) instead of the interior context.
The grid is exp258's VERBATIM {0, 0.25, 0.5, 1.0} (g_ctx), zero new
knobs, on the same 72-row battery shape (the grid multiplies the
battery: 4 grid points x 72 rows = 288 decodes per arm-set; the
g=0.0 point IS the schema-only arm — the within-run control, asserted
bit-exact vs the G1 anchor's errs).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE PORT'S ZERO-DELTA AT DEFAULTS: the 72-row battery with the
      register live reproduces exp256's deposited substituted errs
      BIT-EXACT 72/72 (the verified flags 72/72) AND exp282's
      walk_end_rms bit-exact 72/72 (the trace sha256 72/72 — the same
      walk discipline); the register's PRESENCE asserted (the
      attribute exists, the values finite, the init == the spec's
      install bit-exact at the walk's start — asserted per row);
      the repo test suite green (python3 -m tests.run_tests from the
      repo root, the shadow path disclosed); exp142 NOT modified.
  G2  THE HISTORY POPULATED (zero-knob asserted, fail=STOP per row):
      at the walk's end phi_history[write_set] == the commit replay's
      values BIT-EXACT per row (the register IS the commit sequence
      stored incrementally — the same replay exp287/exp288 anchored,
      now read from the register); the register's non-write-set cells
      == the spec install (the never-written cells' history is the
      spec layer); the register finite 72/72.
  G3  THE ACTIVATION BRANCH (pre-named numeric bars): per grid point
      g in {0.25, 0.5, 1.0} the 72-row battery re-run with the ctx
      coupling reading phi_history; per host the 6-row mean err; the
      branch HISTORY-CARRIED iff EXISTS a grid point g > 0 with the
      mean err IMPROVED vs the g=0.0 within-run control on >= 10/12
      hosts (the improvement bar: the per-host mean delta < 0.0 —
      strict, disclosed); else HISTORY-INERT (the exp258 verdict's
      form: degradation or no improvement). Audit-only: the per-host
      per-grid delta table, the worst-err per grid point vs the 6.0
      bar (unchanged), the exp288 pooled-R_max face re-computed at
      the best grid point (the class-blindness re-read under the
      history — audit-only, never gating).
  G4  THE DISCIPLINE: deterministic one-pass per grid point (the
      port is a state register, not a second RNG consumer — the
      stream UNTOUCHED, asserted via G1's bit-exact errs); no
      wall-clock fields; the docstring + header pinned to this
      pre-registration commit, asserted at entry AND exit; the
      source deposits READ-ONLY (exp243/256/272/273/282/287/288);
      NEURAL_SPEC_MIN == -60.0 asserted at exit (the exp169-import
      discipline; the -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): HISTORY-CARRIED / HISTORY-INERT.

RUN: the G1 anchor pass (72 decodes ~ 60-90 s) + the G2 asserts
(free) + the G3 grid (3 x 72 decodes ~ 3-5 min) — one invocation,
~4-7 min, UNDER the 570 s cap only in the checkpoint-split form
EXP289_MODE=pass1 (G1+G2) | pass2 (G3) | merge; the default
in-process form runs the whole sequence and may exceed the cap —
the pre-named form for the sandbox is the checkpoint split; the
pre-named form for the GitHub runners (30-min) is the in-process
default. Both forms evaluate the SAME gates and assert the same
bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp289_history_register.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp289's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
