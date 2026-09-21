#!/usr/bin/env python3
"""exp306 — THE PREMIUM UNDER THE COMPOSED CARRIER: DOES THE UNION'S
COMMIT LAYER DISSOLVE THE STRUCTURAL RESIDUAL? (batch 60; ledger
L290c's promoted candidate (5) — exp294 landed PREMIUM-MIXED on the
SELF g=1.0 carrier's commits: the noise-carried fraction DISSOLVED
(rho(mean_cvt)~mia_prod_err +0.2679 vs exp287's deposited +0.8616,
under the 0.40 bar) while the structural residual STRADDLED
(rho(mean_cvt)~one_zone_premium +0.4175 — above the dissolved bar,
below the carried bar). exp302 then landed PROTECTED-PRESERVED on the
COMPOSED union (faces=(ctx, gj, apop) at the composed optimum g=1.0,
+13.13 mV, the stress decode-invisible) — the strongest carrier the
stack has, and exp294 never saw it. THE OPEN QUESTION: does the
composed carrier's commit layer dissolve the structural residual too
(UNION-DISSOLVED — the premium story closes entirely: the host
dependence of the committed pattern was the noise's structure all the
way down), does it CARRY THROUGH (UNION-CARRIED — the premium is
structural to the spec layer and survives the strongest carrier), or
does the honest middle hold (UNION-MIXED)?

THE INSTRUMENT (exp302's landed union walk machinery VERBATIM at arm
A0 — no stress pin anywhere, the floor at -60.0 throughout; the 72-row
substituted battery exp256's/exp300's, 12 hosts x 3 seeds x r-60i0/
r-60i1 at n=400, the production budget 8; the commit recording the
exp287 form) with exp294's landed rho reads on top:

  R1  THE COMMIT-LAYER REGRESSIONS: per row the commit-vs-target RMS
      cvt_rms on the union's commits; per host the 6-row mean_cvt; THE
      ANCHOR REGRESSIONS: rho(mean_cvt)~mia_prod_err and
      rho(mean_cvt)~one_zone_premium under the house conventions
      VERBATIM (Spearman = Pearson on the tied-average ranks, the
      12-slot frame with the H0==H1 echo carried; the CONVENTION
      SELF-CHECK first: fed exp287's OWN deposited carrier host-table
      mean_cvt + the same covariate carries, the machinery must
      reproduce exp287's deposited rhos BIT-EXACT 2/2). The branch
      reads the comparison vs exp287's deposited rhos (+0.8616 /
      +0.7790) AND vs exp294's fresh self-carrier rhos (+0.2679 /
      +0.4175, re-read READ-ONLY from exp294's deposit).
  R2  THE IMPROVEMENT'S ADDRESS (audit-only, never gating): the
      per-host mean err deltas vs the dormant control (exp256's
      deposited substituted errs) vs the per-host mean_cvt deltas vs
      exp287's deposited commit layer — the delta correlation; the
      worst-err vs the 6.0 bar (audit-only).

THE ANCHOR (G1, fail=STOP): the 72 union walks reproduce exp300's
deposited union g=1.0 rows BIT-EXACT — the errs 72/72 + the trace shas
72/72 + the per-row cvt_rms 72/72 + the per-host mean_cvt 12/12 (the
commit layer IS the deposited union's, not a new instrument).

THE BRANCHES (pre-named): UNION-DISSOLVED iff BOTH fresh |rho| < 0.40
(the structural residual dissolves too — the premium was the noise's
host structure all the way down); UNION-CARRIED iff BOTH fresh |rho|
>= 0.60 (the premium is structural to the spec layer); UNION-MIXED
otherwise (the honest middle). The bars PREMIUM_DISSOLVED 0.40 /
PREMIUM_CARRIED 0.60 are exp294's landed bars, re-fixed HERE at
pre-registration, never fit.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets 72/72; THE MARKS' VALIDITY: the
      rebuilt q10/q90 + target_part + bands reproduce exp300's
      deposited arm_inputs BIT-EXACT 24/24 + 12/12 (the union's
      armed-site plan pinned to the deposited one — the anchor's
      bit-exactness depends on them); THE EXP300 ANCHOR: the 72 union
      rows bit-exact (errs + trace shas + per-row cvt_rms 72/72 each;
      the per-host mean_cvt 12/12); the convention self-check vs
      exp287's deposited rhos BIT-EXACT 2/2; the covariate carries
      (mia_prod_err + one_zone_premium) bit-exact 12/12 + 12/12 via
      exp273's field table; 7 deposits READ-ONLY sha before/after
      (exp243/256/272/273/287/294/300); the port's provenance + the
      zero-reader scan (the allowlist = the port + the pre-named
      history instruments + this module); exp142 and the core NOT
      modified (sha at entry == exit); the test suite green.
  G2  THE COMMIT LAYER'S DEFINITION (zero-knob asserted, fail=STOP per
      row): the commit count == walk_steps == the trace length 72/72;
      the commit indices unique 72/72; the write-set coverage 72/72;
      the values finite 72/72; the digests recorded 72/72 (the full
      sequences NOT re-deposited); cvt_rms finite 72/72; the A3 state
      convention 72/72; the register's replay equality + complement
      face 72/72; the union's face-write bookkeeping (n_sigma_writes +
      n_blend_writes) constant across the seeds per (host, instance)
      24/24; the gj landed compensation assert re-run per row
      (exp259's conservation identity, exp300's G2 form).
  G3  THE BRANCH DISCRIMINANT (the bars pre-named above, numeric,
      never fit): the fresh rhos vs the bars, evaluated exactly once;
      UNION-DISSOLVED / UNION-CARRIED / UNION-MIXED; the audit faces
      recorded (R2's address reads, never gating).
  G4  THE DISCIPLINE: deterministic (one pass; the payload serialized
      twice, the shas asserted equal); no wall-clock fields; the
      docstring + header pinned to the pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at
      exit; the floor -60.0 asserted at the entry, after the battery,
      and at exit (NO pin anywhere in this experiment).

RUN: 72 union decodes, in-process one invocation, ~2-4 min, under the
570 s cap.

DEPOSIT: results/exp306_premium_under_union.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp306_premium_under_union.json")


def main() -> dict:
    raise SystemExit("the body is not written yet (pre-registration stub)")
