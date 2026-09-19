#!/usr/bin/env python3
"""exp286 — THE ENDPOINT'S DOSE: THE END-RMS CARRIER'S OWN PARAMETER,
THE WALK'S STEP BUDGET (batch 44; ledger L263's derived item — batch 43
closed the grain screen at three levels, all exposure-blind at the 0.5
SIGNED bar: the exp208-label classes (exp277 decode NEITHER + exp284
walk CLASS-BLIND), the boundary's own share (exp284's audit-only
sub-bar lead), the ring around it (exp285 RING-ABSENT) — so the
carrier's exposure stays in the walk's ENDPOINT MAGNITUDE (exp282's
+0.88). This module turns to the carrier's OWN parameter: the walk's
step budget).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED on walk_end_rms
(the walk's trace[-1]; signed Spearman +0.8826151316282213 against
mia_prod_err, +0.8807017543859651 against exp272's one-zone premium
means; the 0.5 SIGNED house bar). The production budget is exp142's
STEPS_PER_CELL == 8 — the number of integration steps the walk takes
per committed cell before the commit draw. Is the endpoint magnitude a
FIXED POINT of the walk — invariant to the budget — or an artifact of
the production dose? If the endpoint is budget-invariant, the premium
is the walk's fixed point; if the outlier hosts' (H3/H5's) budget
response differs from the ten-host cluster's, the premium is a BUDGET
artifact — the excess endpoint magnitude produced by the production
dose rather than carried by the host structure.

THE LADDER (pre-named, fixed HERE at pre-registration): budgets
{4, 8, 16} — 4 HALVES the production budget, 8 IS the production
default (asserted == exp142's STEPS_PER_CELL), 16 DOUBLES it. The dose
is delivered as integration steps per committed cell; the walk ORDER
is untouched (asserted per row: walk_steps IDENTICAL across the three
budgets — the budget scales the steps per cell, never the visit order;
the delivered dose per row = budget * walk_steps, the {4x, 8x, 16x}
ladder per cell).

THE INSTRUMENT (pre-registered, zero new simulation beyond the one
battery x the three budgets): exp284/exp285's landed traced replica
REUSED VERBATIM (_execute_signed_traced, landed 8ca252e, reused since
f3ca053: exp142's walk byte-similar + exactly the disclosed recording
additions; the RNG stream / dt / canon / walk order / commits
untouched; exp142 NOT modified) with ONE DISCLOSED PARAMETERIZATION:
the per-cell loop bound is read from an explicit budget argument
instead of the module constant — at budget 8 the code path IS the
landed replica's, and it is ANCHORED BIT-EXACT against exp282's
deposited walks (G1: the trace sha256 + walk_end_rms reproduce 72/72).
Plus the host rebuild (exp269's/exp280's/exp284's/exp285's form) and
exp256's _scoped_row_read_state form (the projection chain PN1/PN2 +
TC1 + TC2 + the traced TC3). ONE FRESH RUN of the SAME 72 substituted
rows (12 hosts x 3 seeds (1,2,3) x the two deep instances
r-60i0/r-60i1 at n=400 — exp256's battery) DECODED AT EACH BUDGET —
216 decodes per pass. NO classify / decompose / mask work on the rows
— the dose question is budget-level, not grain-level (the grain screen
is closed; exp285's ring machinery is deliberately absent). The
per-cell end errors are NOT re-decomposed — the endpoint magnitude is
the read.

THE PER-ROW READS: per row and per budget — the end RMS (the walk's
trace[-1], the PRE-settle carrier; the POST-settle err_exact + the
settle gap recorded audit-only), the reported err, the A3-checked
state convention, the trace sha256 (recorded at EVERY budget; asserted
== exp282's deposit at budget 8; the 4/16 shas recorded for any future
re-verification), walk_steps, the convergence point (TA3), the
delivered step count. THE PER-HOST MEANS: over the host's 6 rows
(3 seeds x 2 instances) of the end RMS at each budget.

THE PRE-NAMED READS: (1) THE BUDGET SENSITIVITY — per host the ratios
r4 = mean_end_RMS(4) / mean_end_RMS(8) and r16 = mean_end_RMS(16) /
mean_end_RMS(8); if ~1.0 the endpoint is budget-invariant — the walk's
fixed point; the outliers' ratios vs the cluster's decide the artifact
question. (2) THE EXP282 ANCHOR AT THE DEFAULT — the regressions of
the end_RMS(8) carrier (the per-host means) against mia_prod_err
(exp273's field table, asserted == exp243's own class records) and
exp272's one-zone premium means (asserted == exp273's field-table
carry) under the exp274/exp275/exp282 conventions VERBATIM (Pearson on
the tied-average ranks, the 12-slot frame with the H0==H1 echo
carried, the ties census per vector, the single-predictor rank R2),
ASSERTED BIT-EXACT == exp282's deposited rhos — the default-budget
carrier reproduced, not re-fit. (3) THE BRANCH (below).

THE BRANCH (pre-named, the bars numeric, fixed HERE at
pre-registration, never fit): with INV_BAND = 0.10, INV_MIN_HOSTS =
10, SEP_MARGIN = 0.10 — N_inv = #{hosts : |r4 - 1| <= INV_BAND AND
|r16 - 1| <= INV_BAND}; BUDGET-INVARIANT iff N_inv >= INV_MIN_HOSTS
(both ratios within 1.0 +/- 0.1 on >= 10/12 hosts — the premium is the
walk's fixed point); else BUDGET-ARTIFACT iff the outliers' ratios
SEPARATE from the cluster's: min(r | outliers) - max(r | cluster) >
SEP_MARGIN or min(r | cluster) - max(r | outliers) > SEP_MARGIN, on r4
or r16, either direction (the premium tracks the budget — a BUDGET
artifact); else MIXED (named honestly). The full orderings + the
outlier margins recorded audit-only, never gating.

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285 precedent (graph_path
      at the chain class's n=400 call site for H0/H1 — H0 echoes H1
      bit-exactly, asserted; small_world(n, 0.10, deposited
      rewire_seed) for H2-H11), bit-asserted against exp243's records:
      sha256(|A| as float64) == base_sha256 12/12; the upper-triangle
      edge count == edges_base 12/12; the classify boundary count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity labeling_bfs_n(|A|)
      == labeling_bfs_n(A) 12/12; f_max recomputed == f_max_base
      12/12; the bases NON-NEGATIVE asserted per host. The two
      deep-row targets rebuilt per exp256's build_rows deep
      construction (exp214's deep form VERBATIM): row_target_sha256
      == exp256's deposited instance records 72/72, and the base
      medium sha == exp243's base_sha256 == the deposited
      medium_sha256 72/72. exp256's 72 rows with the substituted
      structure 36/36 + worst == max 36/36. THE EXP282 RE-READ: the
      72 row records present with trace_sha256 + walk_end_rms +
      err_deposited + walk_steps; exp282's deposited err_deposited ==
      exp256's deposited substituted err 72/72 (the two deposits'
      chain anchor); exp282's deposited branch == TRAJECTORY-CARRIED
      asserted (the pre-registered context); exp282's host_table
      walk_end_rms_mean present for the 12 hosts. THE S0 ANCHOR (the
      budget-8 half of the fresh battery): the re-run's final errs at
      budget 8 reproduce exp256's DEPOSITED substituted errs BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags 72/72), AND exp282's walk_end_rms reproduces BIT-EXACT at
      budget 8 (the fresh walk_end_rms(8) == exp282's deposited
      walk_end_rms 72/72; the fresh trace sha256(8) == exp282's
      deposited trace_sha256 72/72 — the SAME walk exp282 deposited;
      the fresh per-host end_RMS(8) means == exp282's deposited
      host_table means 12/12). The carries: the mia carry bit-exact
      12/12 (exp273's field table == exp243's own class records) + the
      premium carry bit-exact 12/12 (exp272 == exp273's field-table
      carry). THE PROVENANCE CHAINS sha-verified against the current
      file bytes — exp243 (4) + exp256 (3) + exp272 (4) + exp273 (5) +
      exp282 (4) = 20 records. The source deposits READ-ONLY:
      sha-recorded BEFORE any read, byte-unchanged after the work
      (5 deposits: exp243, exp256, exp272, exp273, exp282).
  G2  THE LADDER (pre-named, per-row dose integrity, all 72 rows x 3
      budgets = 216 decodes per pass): the ladder (4, 8, 16) fixed at
      pre-registration; 8 == exp142's STEPS_PER_CELL asserted (the
      production default — 4 halves the budget, 16 doubles it); the
      replica's one disclosed parameterization: the per-cell loop
      bound from the budget argument (at 8 the landed replica's code
      path — anchored bit-exact in G1); per row: walk_steps IDENTICAL
      across the three budgets (the visit order untouched — the dose
      scales the steps per cell, never the order) + the delivered dose
      budget * walk_steps recorded (the {4x, 8x, 16x} ladder per
      cell); per row per budget: the A3 state convention
      (round(err_exact, 2) == the reported err; asserted fail=STOP);
      the trace finite + trace[-1] > 0; the trace length ==
      walk_steps; the convergence point exists (TA3, exp282's assert
      form); the settle gap recorded (audit-only); the S* read lock
      count == 216 (the lock log asserted); the per-host denominators
      mean_end_RMS(8) > 0 asserted 12/12 and the ratios r4/r16
      computed 12/12.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): (a) THE
      EXP282 ANCHOR AT THE DEFAULT — the fresh per-host end_RMS(8)
      means regressed against mia_prod_err and the one-zone premium
      under the exp274/exp275/exp282 conventions VERBATIM must
      reproduce exp282's deposited rhos BIT-EXACT
      (+0.8826151316282213 against mia_prod_err, +0.8807017543859651
      against the premium) — the default-budget carrier reproduced,
      not re-fit; a drift REFUTEs. (b) THE BRANCH on the pre-named
      bars — INV_BAND 0.10, INV_MIN_HOSTS 10, SEP_MARGIN 0.10:
      BUDGET-INVARIANT iff N_inv >= 10 (both ratios within 1.0 +/- 0.1
      on >= 10/12 hosts — the premium is the walk's fixed point);
      else BUDGET-ARTIFACT iff the outliers' ratios separate from the
      cluster's by > 0.10 on r4 or r16 (either direction — the premium
      is a BUDGET artifact); else MIXED (named honestly). Audit-only,
      never gating: the budget-4 and budget-16 carrier regressions
      against both targets (does the dose change the carrier's
      strength); the full 12-host orderings by r4 and by r16 with the
      outliers' positions; the outlier-vs-cluster ratio margins; the
      per-host end-RMS means at all three budgets; the delivered-dose
      face.
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, or the pre-named
      checkpoint-split per budget + merge with each budget computed
      twice as separate processes; the two passes' payloads
      BIT-IDENTICAL per budget, asserted at the merge/assembly); no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): BUDGET-INVARIANT / BUDGET-ARTIFACT / MIXED.

RUN: the deterministic sha-asserted rebuild (seconds) + 216 decodes per
full pass (3 budgets x 72 rows) ~ 4-6 min foreground per full pass,
far under the 570 s cap per invocation. THE PRE-NAMED CHECKPOINT-SPLIT
PER BUDGET + MERGE (the expected form): EXP286_MODE=budget4|budget8|
budget16 computes and caches ONE budget's 72-row payload per
invocation (each budget computed TWICE as separate processes — the
cross-process form doubles as the byte-identity check, exp284's
precedent; the checkpoint holds at most two payloads per budget);
EXP286_MODE=merge compares the two cached payloads PER BUDGET
BIT-EXACT, assembles, evaluates the gates once, writes the deposit —
the merge NEVER re-decodes — and removes the caches. THE TWO-PASS
IN-PROCESS ALTERNATIVE (no env): the full 3-budget battery computed
twice in one invocation (under the 570 s cap per the probe). Both
forms evaluate the SAME gates and assert the same bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp286_endpoint_dose.json")


def main() -> dict:
    raise NotImplementedError(
        "exp286 body — written by the run agent under the body-only "
        "discipline; the docstring/imports/constants above are the "
        "pre-registration and stay byte-unchanged")


if __name__ == "__main__":
    main()
