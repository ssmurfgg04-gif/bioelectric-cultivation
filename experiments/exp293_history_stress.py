#!/usr/bin/env python3
"""exp293 — THE HISTORY x STRESS INTERACTION: DOES THE REGISTER
PROTECT THE DECODE UNDER WRITE-TIME IONIC STRESS? (batch 48; ledger
L270's registered next (ii) — exp290 landed STORAGE-SIDE: the
write-time depolarized stress (-35.0 pin during the walk) degrades
the decode by 13.13 mV mean on every host while the read-time stress
is bit-identical to the anchor. exp289 landed HISTORY-CARRIED: the
self-history register improves the decode on 12/12 hosts, monotone
in g. The interaction is the memory-protection face: if the commit
history is a state variable that carries the program's own pattern
across the walk, a history-carrying walk under write-time stress may
degrade LESS than the schema-only walk under the same stress — the
register as a PROTECTIVE variable (the Sediqi 2026 history face's
causal form). The null: the stress degradation is additive and the
register's improvement independent — the interaction delta == 0.)

THE INSTRUMENT (exp289's + exp290's landed forms COMPOSED VERBATIM):
the 72-row substituted battery (exp256's) under the 2x2 factorial
(the register state x the stress state, both the machinery's own
constants):
  H0-S0  register OFF (the g=0 schema-only form), floor -60.0
         (the anchor — the errs reproduce exp256's deposited errs
         BIT-EXACT 72/72);
  H1-S0  register ON (the self-history form at the exp289-deposited
         best dose g=1.0), floor -60.0 (the errs reproduce exp289's
         deposited g=1.0 errs BIT-EXACT 72/72);
  H0-S1  register OFF, the WRITE-TIME stress (the walk at the -35.0
         pin, exp290's A1 arm verbatim — the errs reproduce exp290's
         deposited A1 errs BIT-EXACT 72/72);
  H1-S1  register ON (g=1.0), the WRITE-TIME stress (the NEW cell).
THE PROTECTION READ (zero knobs): the protection delta
  P = [mean_err(H0-S1) - mean_err(H1-S1)]
      - [mean_err(H0-S0) - mean_err(H1-S0)]
(the standard 2x2 interaction: the stress degradation under the
register minus the stress degradation without it; P > 0 = the
register PROTECTS — the stress hurts less when the history is
carried; P = 0 = additive independence; P < 0 = the register
AMPLIFIES the stress harm).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: H0-S0 == exp256's deposited errs BIT-EXACT 72/72;
      H1-S0 == exp289's deposited g=1.0 errs BIT-EXACT 72/72 (the
      trace shas 72/72); H0-S1 == exp290's deposited A1 errs
      BIT-EXACT 72/72; the floor asserts (the -35.0 pin during the
      walk in the S1 cells 144/144, -60.0 at the encode in the S0
      cells 144/144, -60.0 at every settle/decode 288/288); 8
      deposits READ-ONLY (exp243/256/272/273/282/287/288/289/290 —
      9 deposits, sha before/after).
  G2  THE NEW CELL'S INTEGRITY (H1-S1, zero-knob asserted, fail=STOP
      per row): finite errs 72/72; the A3 convention 72/72; the
      trace lengths == walk_steps 72/72; the commit counts ==
      walk_steps 72/72; the register's replay equality (exp289's G2
      form) 72/72 (the register populates identically under stress —
      the population path is stress-independent by construction,
      asserted); the S* lock reads 288 (4 cells x 72).
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars): P vs the
      pre-named bar PROTECT_BAR 0.05 mV (the exp290 margin form):
      PROTECTED   iff P >= 0.05;
      AMPLIFIED   iff P <= -0.05;
      ADDITIVE    otherwise (the honest null: the two effects
          independent at the machinery's resolution).
      Per-host P recorded (the outliers H3/H5's P, audit-only); the
      worst-err per cell vs the 6.0 bar (unchanged); the commit
      censuses per cell (the stress's effect on the (e) branch,
      exp290's disclosed form).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified
      (the composition uses exp289's landed register + exp290's
      landed pin schedule — the module attributes set around the
      calls, disclosed); NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PROTECTED / AMPLIFIED / ADDITIVE at the
PROTECT_BAR 0.05 mV form.

RUN: 288 decodes ~ 4-6 min — the pre-named form is the CHECKPOINT-
SPLIT EXP293_MODE=pass1 (the S0 cells, 144 decodes) | pass2 (the S1
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
OUT = os.path.join(ROOT, "results", "exp293_history_stress.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp293's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
