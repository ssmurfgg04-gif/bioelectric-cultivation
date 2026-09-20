#!/usr/bin/env python3
"""exp295 — THE DOSE CURVE REFINED AND THE NBOR LEAK REPAIR (batch 48;
ledger L273's registered nexts (i)+(ii) — exp292 landed DOSE-REVERSAL
x SELF-DOMINANT: the self-history carrier peaks at g ~ 1.0 (the
reversal past the peak 12/12) and the neighbor-mean form degrades
12/12 (+1.8385 mV at g=1.0 — the register of the unwound neighbors
holds the SPEC INSTALL, so the naive neighbor mean re-injects the
spec's own values as a false history: THE LEAK). Two pre-named
follow-ups, one battery: (1) THE DOSE CURVE refined around the peak —
the pre-named {0.75, 1.0, 1.25, 1.5} SELF ladder (the reversal's
sharpness: is the peak flat or sharp?); (2) THE LEAK REPAIR — the
WRITE-SET-WEIGHTED neighbor form: the neighbor mean weighted by each
neighbor's write-set membership (nbrs that the program ACTUALLY
wrote contribute their true commit history; unwritten nbrs — whose
register holds the spec install — contribute ZERO weight): the leak
face isolated. The repaired NBOR arm re-runs the source face: does
the social form turn from poison to neutral/protection once the leak
is removed?)

THE INSTRUMENT (exp292's landed form REUSED VERBATIM): the additive
phi_history register, the traced replica, the 72-row substituted
battery. The arms:
  SELF-R  — the self form at g in {0.75, 1.0, 1.25, 1.5} (the
            refined curve; the g=1.0 point anchors bit-exact vs
            exp289's deposited g=1.0 errs 72/72);
  NBW     — the write-set-weighted neighbor form at g in {0.25, 0.5,
            1.0} (exp292's NBOR grid, now leak-repaired; the weight
            w_j = 1 if the neighbor j is in the row's write set (the
            commit sequence's support) else 0; the mean over the
            weighted support; a row with NO written neighbors falls
            back to the self value — disclosed, the fallback count
            recorded).
The g=0.0 control is exp289's/exp288's anchor errs (the deposits,
bit-exact — read, never re-run).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR + THE ARMS' INTEGRITY: the SELF g=1.0 errs ==
      exp289's deposited g=1.0 errs BIT-EXACT 72/72 (the trace shas
      72/72); per arm-cell the finite/A3/trace-length/commit-count
      asserts 72/72; the S* lock reads 504 (7 arm-cells x 72); the
      floor -60.0 throughout (no stress); 9 deposits READ-ONLY
      (exp243/256/272/273/282/287/288/289/292), sha before/after.
  G2  THE FORMS' DEFINITION (zero-knob asserted, fail=STOP per row):
      the NBW weights derived ONLY from the commit sequence's support
      (the write set — no new knobs); the fallback-to-self count
      recorded per row (audit); the register replay equality per arm
      at the PER-ARM scope (exp292's diagnosis honored): 72/72 per
      arm-cell; the complement 72/72 per arm-cell.
  G3  THE TWO BRANCH FACES (pre-named numeric bars):
      THE DOSE FACE (SELF-R): the curve's shape at the refined grid —
      PEAK-FLAT  iff the |delta| differences among {0.75, 1.0, 1.25}
          are all < 0.01 mV on >= 10/12 hosts (a plateau);
      PEAK-SHARP otherwise (a distinct optimum — the reversal's
          sharpness recorded by the argbest host-wise, audit-only).
      THE LEAK FACE (NBW vs exp292's NBOR deposited deltas): the
      repaired form's mean paired delta vs the leaky form's +1.8385
      at g=1.0:
      LEAK-CONFIRMED  iff the NBW delta at g=1.0 improves vs the NBOR
          deposited delta by > 0.05 mV on >= 10/12 hosts (the leak
          WAS the failure mode);
      LEAK-NOT-SUFFICIENT otherwise (the social form's failure is
          deeper than the leak — recorded honestly).
      Audit-only: the per-host per-arm delta table, the fallback
      counts, the worst-err vs the 6.0 bar, the R_max face (audit).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PEAK-FLAT / PEAK-SHARP x LEAK-CONFIRMED /
LEAK-NOT-SUFFICIENT (the two faces recorded independently).

RUN: 504 decodes ~ 7-10 min — the pre-named form is the CHECKPOINT-
SPLIT EXP295_MODE=pass1 (SELF-R, 288 decodes) | pass2 (NBW, 216
decodes) | merge; the in-process default for the GitHub runners.
Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp295_dose_curve_leak_repair.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp295's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
