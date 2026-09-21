#!/usr/bin/env python3
"""exp302 — THE COMPOSED STRESS FACE: IS THE ~29x PROTECTION
PRESERVED UNDER COMPOSITION? (batch 56; ledger L286's registered
next (a) — exp293 landed PROTECTED: the ctx register's 2x2
interaction P = +0.73 mV, the write-time stress hurting ~29x LESS
when the history is carried than the register's own rest
improvement would suggest; exp300 landed MONOTONE-TO-1.0: the
composed carrier's optimum IS the saturated face g=1.0 of the union
faces=(ctx, gj, apop) on ONE walk; exp301 landed WRITE-SIDE-CARRIED:
the carrier changes WHAT the program commits, not the structure of
how it commits. THE OPEN QUESTION: does the PROTECTION face survive
composition — is the composed union (the strongest carrier the stack
has) under write-time ionic stress degraded LESS than the schema-only
walk by more than the pre-named margin, and how does the composed
protection compare to the single register's (the audit face — does
protection COMPOSE like the improvement did below saturation)? The
null: the stress degradation is additive under the union too and the
composed interaction == the single register's (P_union == P_ctx).)

THE INSTRUMENT (exp293's landed 2x2 factorial form COMPOSED VERBATIM
with exp300's landed union coupling + exp290's landed stress-pin
schedule; the 72-row substituted battery, exp256's):
  U0-S0  union OFF (the g=0 schema-only form), floor -60.0
         (the anchor — the errs reproduce exp256's deposited errs
         BIT-EXACT 72/72, the walk anchors exp282's 72/72);
  U1-S0  union ON (the faces=(ctx, gj, apop) union at the composed
         optimum g=1.0, exp300's landed arm VERBATIM), floor -60.0
         (the anchor — the errs + the trace shas reproduce exp300's
         deposited union g=1.0 rows BIT-EXACT 72/72);
  U0-S1  union OFF, the WRITE-TIME stress (the walk at the -35.0
         pin, exp290's A1 arm verbatim — the errs reproduce exp290's
         deposited A1 errs BIT-EXACT 72/72);
  U1-S1  union ON (g=1.0), the WRITE-TIME stress (THE NEW CELL).
THE PROTECTION READ (zero knobs): the composed protection delta
  P_union = [mean_err(U0-S1) - mean_err(U1-S1)]
            - [mean_err(U0-S0) - mean_err(U1-S0)]
(the standard 2x2 interaction on the union: P > 0 = the union
PROTECTS under composition; P = 0 = additive independence; P < 0 =
the union AMPLIFIES the stress harm).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: U0-S0 == exp256's deposited errs BIT-EXACT 72/72
      (the verified flags 72/72; exp282's walk_end_rms + trace shas +
      err_exact 72/72 — the SAME walk exp282 deposited; the
      commit-layer digests vs exp287/exp288 recorded AUDIT-ONLY);
      U1-S0 == exp300's deposited union g=1.0 rows BIT-EXACT 72/72
      (the errs + the trace shas; the face write-count + register
      digest faces AUDIT-ONLY); U0-S1 == exp290's deposited A1 errs
      BIT-EXACT 72/72 (the fresh trace shas + floor schedules
      AUDIT-ONLY); the MARKS' VALIDITY: the rebuilt q10/q90 +
      target_part + bands reproduce exp300's deposited arm_inputs
      BIT-EXACT (fail=STOP — the union's armed-site plan is pinned
      to the deposited one); the floor asserts (the -35.0 pin during
      the walk in the S1 cells 144/144, the -60.0 encode in the S0
      cells 144/144, -60.0 at every settle/decode 288/288); 11
      deposits READ-ONLY (exp243/256/272/273/282/287/288/289/290/
      293/300 — sha before/after); the rebuild chain sha-asserted.
  G2  THE NEW CELL'S INTEGRITY (U1-S1, zero-knob asserted, fail=STOP
      per row): finite errs 72/72; the A3 convention 72/72; the
      trace lengths == walk_steps 72/72; the commit counts ==
      walk_steps 72/72; the register's replay equality (exp289's G2
      form) 72/72; the STREAM face (the commit-index digests +
      walk_steps + n_commits identical across ALL FOUR cells) 72/72;
      the PLAN face (the union's armed-site counts n_arm_writes +
      n_sigma_writes + n_blend_writes identical across U1-S0/U1-S1 —
      the plan is (target, A)-determined, stress-independent) 72/72;
      the S* lock reads 288 (4 cells x 72).
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars): P_union vs
      the pre-named bar PROTECT_BAR 0.05 mV (the exp293 margin form):
      PROTECTED-PRESERVED  iff P_union >= 0.05;
      AMPLIFIED             iff P_union <= -0.05;
      ADDITIVE              otherwise (the honest null).
      AUDIT-ONLY, never gating: the composition's protection
      comparison (P_union vs exp293's deposited P_ctx — does
      protection compose?); the ratio face (P_union / the union's
      rest improvement) vs exp293's ~29x; the per-host P (the
      outliers H3/H5 disclosed); the worst-err per cell vs the 6.0
      bar; the commit src censuses per cell (the floor's effect on
      the (e) branch); the gj landed compensation assert re-run per
      U1 row (exp259's conservation identity — exp300's G2 form).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified
      (the composition uses exp300's landed union coupling + exp290's
      landed pin schedule — the module attributes set around the
      calls, disclosed); NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PROTECTED-PRESERVED / AMPLIFIED / ADDITIVE
at the PROTECT_BAR 0.05 mV form.

RUN: 288 decodes ~ 5-8 min — the pre-named form is the CHECKPOINT-
SPLIT EXP302_MODE=pass1 (the S0 cells, 144 decodes) | pass2 (the S1
cells, 144 decodes) | merge; the in-process default for the GitHub
runners. Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp302_composed_stress_face.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to this file's pre-registration commit; gates G1-G4
    #      evaluated exactly once) ========================================
    raise NotImplementedError(
        "exp302's body lands per the pre-registration (the stub holds "
        "the plan; the body is the next commit)")
