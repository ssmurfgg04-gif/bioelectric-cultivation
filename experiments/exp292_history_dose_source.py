#!/usr/bin/env python3
"""exp292 — THE HISTORY DOSE AND SOURCE: WHERE THE CARRIER BREAKS, AND
WHOSE COMMITS PROTECT THE BOUNDARY (batch 48; ledger L269's registered
nexts (i)+(ii) — exp289 landed HISTORY-CARRIED: the ctx coupling
reading the SELF-history improves the decode on 12/12 hosts at every
grid point of exp258's grid, MONOTONE in g, total -0.3100 mV at
g=1.0. Two structural questions follow, zero new knobs: (1) THE DOSE
— the improvement is monotone over exp258's grid {0, 0.25, 0.5, 1.0};
where does it saturate or break? The ladder extends to the
pre-named {1.0, 2.0, 4.0} (the same instrument, the dose axis
exp270/exp286's form). (2) THE SOURCE — exp289 read the cell's OWN
last commit (the self-history face). The alternative source: the
NEIGHBOR-history face (the cell pulled toward the mean last-commit of
its graph neighbors — the social form: the boundary cells' neighbors
are the unwound tissue whose history is the spec install). The two
forms are crossed with the dose ladder in ONE battery.)

THE INSTRUMENT (exp289's landed form REUSED VERBATIM): the additive
phi_history register (initialized to the spec install, populated at
each commit write, nothing reads it at defaults); the ctx coupling
term at the register; the 72-row substituted battery (exp256's,
12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, the traced replica at
the production budget 8). The arms:
  SELF  — the exp289 form verbatim, g in {1.0, 2.0, 4.0} (the dose
          ladder; the g=1.0 point reproduces exp289's deposited
          g=1.0 errs BIT-EXACT — the anchor);
  NBOR  — the coupling source switched to the neighbor mean of
          phi_history (the graph neighbors of the projected adjacency
          A_ext, the mean over the support; the same grid {1.0, 2.0,
          4.0}).
The g=0.0 control is exp289's/exp288's anchor errs (the deposited
form, bit-exact — no re-run, the anchor read from the deposits).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR + THE ARMS' INTEGRITY: the SELF g=1.0 errs reproduce
      exp289's deposited g=1.0 errs BIT-EXACT 72/72 (the same-walk
      discipline: the trace shas 72/72); per arm-cell the finite/A3/
      trace-length/commit-count asserts 72/72; the S* lock reads
      432 (2 sources x 3 doses x 72); the floor -35.0-pin discipline
      N/A (no stress here — the floor -60.0 throughout, asserted);
      the source deposits READ-ONLY (exp243/256/272/273/282/287/288/
      289 — 8 deposits, sha before/after).
  G2  THE SOURCE FORMS' DEFINITION (zero-knob asserted, fail=STOP):
      the SELF form's coupling reads phi_history[i] (exp289's form,
      asserted == the deposited instrument by G1's bit-exactness);
      the NBOR form's coupling reads mean(phi_history[nbrs(i)]) over
      the adjacency support (the neighbors' last commits — the
      register itself UNTOUCHED: the read is a pure projection, the
      population path identical to exp289's); the register's replay
      equality (exp289's G2 form) re-asserted per arm 72/72.
  G3  THE DOSE + SOURCE BRANCH (pre-named numeric bars): per arm-cell
      the 72-row mean err and the mean paired delta vs the g=0.0
      anchor; the branches:
      DOSE-SATURATING  iff the SELF deltas improve monotonically
          through g=2.0 and the g=4.0 delta >= the g=2.0 delta
          (no reversal) on >= 10/12 hosts;
      DOSE-REVERSAL    iff the SELF delta at g=4.0 < the g=2.0 delta
          (a degradation past the peak) on >= 10/12 hosts;
      SELF-DOMINANT    iff the SELF mean delta < the NBOR mean delta
          at the best shared dose by more than 0.05 mV (the
          exp290 margin form);
      NBOR-DOMINANT    iff the reverse by the same margin;
      SOURCE-SYMMETRIC otherwise.
      Audit-only: the per-host per-arm delta table, the worst-err per
      arm vs the 6.0 bar (unchanged), the exp288 pooled-R_max face at
      the best arm (audit-only), the H3/H5 outlier deltas.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified
      (the port is exp289's landed form — the module attribute the
      coupling reads is the ONLY difference between the arms);
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): DOSE-SATURATING / DOSE-REVERSAL x
SELF-DOMINANT / NBOR-DOMINANT / SOURCE-SYMMETRIC (the dose face and
the source face recorded independently).

RUN: 432 decodes ~ 6-9 min — the pre-named form is the CHECKPOINT-
SPLIT EXP292_MODE=pass1 (SELF ladder, 216 decodes) | pass2 (NBOR
ladder, 216 decodes) | merge, each pass under the 570 s cap; the
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
OUT = os.path.join(ROOT, "results", "exp292_history_dose_source.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp292's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
