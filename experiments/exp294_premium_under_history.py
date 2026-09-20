#!/usr/bin/env python3
"""exp294 — THE PREMIUM UNDER THE HISTORY CARRIER: DOES THE SPEC-LAYER
PREMIUM SURVIVE THE REGISTER'S IMPROVEMENT? (batch 48; ledger L269's
registered next (iv) == L273's registered next (iii) — exp289 landed
HISTORY-CARRIED (the self-history coupling improves the decode 12/12,
monotone to g=1.0), exp292 landed DOSE-REVERSAL x SELF-DOMINANT (the
carrier is self-sourced, dose-peaked at g ~ 1.0), exp293 landed
PROTECTED (the register protects under write-time stress,
super-additively, P +0.7285). The chain's standing finding (exp287,
L265): the premium lives in WHAT the program commits —
rho(mean_cvt)~mia +0.8616 / ~premium +0.7790, and exp288 (L267)
showed the commit-error face is class-blind. THE OPEN QUESTION: the
carrier improves the decode by re-coupling the commits to the
cells' own history — does that improvement DISSOLVE the spec-layer
premium (the host-dependence of the committed pattern collapses as
the errs converge — the premium was the noise's host structure) or
CARRY THROUGH it (the committed pattern stays host-dependent — the
premium is structural to the spec layer, not to the un-coupled
noise)?)

THE INSTRUMENT (exp289's landed form REUSED VERBATIM at its landed
best dose): the SELF form at g=1.0 on the 72-row substituted battery
(exp256's, 12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, the traced
replica at the production budget 8) with the commit recording (the
(f) addition) — the SAME walk exp289's g=1.0 arm ran (the errs + the
trace shas reproduce exp289's deposited g=1.0 records BIT-EXACT
72/72 — the anchor, fail=STOP; NO new decodes needed beyond the one
anchor battery re-run that produces them).

THE READS (zero new knobs, all on the fresh carrier-walk commits):

  R1  THE COMMIT LAYER UNDER THE CARRIER: per row the commit-vs-target
      RMS cvt_rms (the exp287 form) on the carrier's commits; per host
      the 6-row mean_cvt; THE ANCHOR REGRESSIONS: rho(mean_cvt)~mia
      and ~premium under the house conventions (exp274/exp275/exp282
      VERBATIM) — the branch reads the comparison vs exp287's
      deposited rhos (+0.8616 / +0.7790):
      PREMIUM-DISSOLVED  iff BOTH fresh |rho| < 0.40 (the carrier's
          improvement flattened the committed pattern's host
          dependence — the premium was the un-coupled noise);
      PREMIUM-CARRIED    iff BOTH fresh |rho| >= 0.60 (the committed
          pattern stays host-dependent under the carrier — the
          premium is structural to the spec layer);
      PREMIUM-MIXED      otherwise (the honest middle).
  R2  THE IMPROVEMENT'S ADDRESS (audit-only): the per-host mean err
      deltas vs the g=0.0 anchor (the exp289 deposited form) vs the
      per-host mean_cvt deltas — does the improvement track the
      commit-layer change (the delta correlation, the house
      conventions, audit-only)? The exp288 pooled-R_max face on the
      carrier's commits (audit-only). The worst-err vs the 6.0 bar
      (unchanged, audit-only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: the carrier battery's errs == exp289's deposited
      g=1.0 errs BIT-EXACT 72/72 (the verified flags 72/72) + the
      trace shas 72/72 (the SAME walk — the commit layer is the
      carrier's, not a new instrument); the 12 bases rebuilt
      sha-asserted vs exp243 (the exp269/exp280 form); the deep
      targets 72/72; the carries mia + premium bit-exact 12/12 +
      12/12; the provenance chains sha-verified (9 deposits:
      exp243/256/272/273/282/287/288/289/292 — the pre-named 29
      records: exp243 4 + exp256 3 + exp272 4 + exp273 5 + exp282 4
      + exp287 5 + exp288 1 + exp289 2 + exp292 1); the source
      deposits READ-ONLY byte-unchanged.
  G2  THE COMMIT LAYER'S DEFINITION (zero-knob asserted, fail=STOP
      per row): the commit count == walk_steps == the trace length
      72/72; the commit indices unique 72/72; the write-set coverage
      72/72; the values finite 72/72; the digests recorded 72/72
      (the full sequences NOT re-deposited); cvt_rms finite 72/72;
      the A3 convention 72/72; the S* lock reads 72; the register's
      replay equality (exp289's G2 form, the PER-ARM scope) 72/72.
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars above): the
      fresh rhos vs the PREMIUM_DISSOLVED 0.40 / PREMIUM_CARRIED 0.60
      bars (fixed HERE at pre-registration, never fit); the
      regressions under the house conventions verbatim (Spearman =
      Pearson on the tied-average ranks; the 12-slot frame with the
      H0==H1 echo carried); audit-only: R2's address reads.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PREMIUM-DISSOLVED / PREMIUM-CARRIED /
PREMIUM-MIXED.

RUN: 72 decodes ~ 60-90 s foreground, one pass + the asserts. Under
the 570 s cap in-process.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp294_premium_under_history.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp294's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
