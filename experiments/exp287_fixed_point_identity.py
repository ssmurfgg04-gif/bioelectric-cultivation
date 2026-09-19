#!/usr/bin/env python3
"""exp287 — THE FIXED POINT'S IDENTITY: IS THE WALK'S ERROR THE EXECUTED
PROGRAM'S OWN SELF-CONSISTENCY LIMIT? (batch 45; ledger L264's derived
item — batch 44 closed the budget question: the end-RMS carrier is the
walk's FIXED POINT, BUDGET-INVARIANT on 12/12 hosts with no
outlier/cluster separation, so the last structural question the
walk-level surface could ask is WHAT the fixed point IS. This module
asks for its identity: re-read the executed program's OWN writes as
the target.)

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED on walk_end_rms (the
PRE-settle trace[-1]; signed Spearman +0.8826151316282213 against
mia_prod_err, +0.8807017543859651 against exp272's one-zone premium
means) and exp286 landed the endpoint BUDGET-INVARIANT — the premium
is the walk's fixed point, carried by the host structure at every
step budget. But a fixed point is not yet an IDENTITY: is the walk's
final error vs the deep target the executed program's OWN
self-consistency limit — the walk lands exactly where it commits and
the error is IN the commit values (the program's imperfect
self-knowledge: the committed pattern differs from the deep target —
the chain closes at the compiler's program) — or does the walk's
final state differ from its own commits (the between-commit dynamics
and the settle MOVE it — SELF-DRIFT, the exp284 disclosed settle
gap's amplified form: exp284's |err_exact - trace[-1]| is an
RMS-DIFFERENCE that cancels drift orthogonal to the residual; the
per-cell committed read below is the drift's proper norm)?

THE TEST (pre-named): re-read the executed program's OWN writes as
the target. The state-carrying traced replica (exp286's landed form
REUSED VERBATIM — _execute_signed_traced with the budget
parameterization at the production budget 8 == exp142's
STEPS_PER_CELL, the host rebuild, exp256's _scoped_row_read_state
form: the projection chain PN1/PN2 + TC1 + TC2 + the traced TC3) runs
the substituted rows (12 hosts x 3 seeds (1,2,3) x the two deep
instances r-60i0/r-60i1 at n=400 — exp256's battery; budget 8). ONE
DISCLOSED RECORDING ADDITION (zero knobs): the replica already walks
cell-by-cell with the commit values in hand — the inherited/
committed theta per cell (theta_new, whatever its source: the spec
layer, the canon, or the parent) is RECORDED AT THE WRITE, after the
write, with the source tag; the recording draws NOTHING from the RNG
stream and touches no state — proven by the S0 anchor's bit-exact
trace sha256 + walk_end_rms (the SAME walk exp282 deposited). At the
walk's end the target for the self-consistency read is the COMMITTED
PATTERN itself (the final theta/V the walk wrote — the program's own
output read as its target).

THE PRE-NAMED QUANTITIES (fixed HERE at pre-registration):
  (1) THE SELF-CONSISTENCY ERROR — sc_rms = the RMS over the
      committed cells (the replay's support: exactly the cells the
      executed program wrote, each exactly once) between the walk's
      final state (the post-settle final_state read) and a REPLAY of
      its own commits (the commit sequence re-read: the recorded
      committed theta per cell, re-read in walk order). ZERO KNOBS:
      the replay is built ONLY from the recorded commits — no
      re-simulation, no parameters, no external target enters the
      replay; the definition has no free parameters.
  (2) THE PROGRAM-VS-TARGET GAP — the production err vs the deep
      target: err_exact (the A3-checked full-frame RMS between the
      final state and the deep target), ANCHORED by the S0 anchor
      (the reported errs reproduce exp256's deposited substituted
      errs BIT-EXACT 72/72; err_exact reproduces exp282's 72/72).
      (The supports differ by construction — the replay lives on the
      program's write set, the gap on the full frame; the ratio below
      is the pre-named read, the supports disclosed.)
  (3) THE BRANCH (the bars numeric, fixed HERE, never fit):
      SC_FRAC_BAR = 0.01, SC_MIN_HOSTS = 10 — per host the mean
      sc_rms over its 6 rows vs the mean err_exact over its 6 rows;
      the host is self-consistent iff mean_sc < SC_FRAC_BAR *
      mean_gap; N_sc = #{hosts self-consistent}:
        SELF-CONSISTENT iff N_sc >= SC_MIN_HOSTS (the walk lands
        exactly where it commits — the premium is the program's
        imperfect self-knowledge: the committed pattern differs from
        the deep target, the error is IN the commit values, the
        chain closes at the compiler's program);
        else SELF-DRIFT (the walk's final state differs from its own
        commits — the between-commit dynamics + the settle move it;
        the exp284 disclosed settle gap's amplified form).

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285/exp286 precedent
      (graph_path at the chain class's n=400 call site for H0/H1 —
      H0 echoes H1 bit-exactly, asserted; small_world(n, 0.10,
      deposited rewire_seed) for H2-H11), bit-asserted against
      exp243's records: sha256(|A| as float64) == base_sha256 12/12;
      the upper-triangle edge count == edges_base 12/12; the classify
      boundary count == n_boundary_cells_base 12/12, dual-carried vs
      exp272's per_host AND exp273's field table; the canon identity
      labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12; f_max
      recomputed == f_max_base 12/12; the bases NON-NEGATIVE
      asserted per host. The two deep-row targets rebuilt per
      exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited medium_sha256 72/72. exp256's 72 rows with
      the substituted structure 36/36 + worst == max 36/36. THE
      EXP282 RE-READ: the 72 row records present with trace_sha256 +
      walk_end_rms + err_deposited + walk_steps; exp282's deposited
      err_deposited == exp256's deposited substituted err 72/72 (the
      two deposits' chain anchor); exp282's deposited branch ==
      TRAJECTORY-CARRIED asserted (the pre-registered context);
      exp282's host_table walk_end_rms_mean present for the 12
      hosts. THE S0 ANCHOR (the production-budget battery): the
      re-run's reported errs reproduce exp256's DEPOSITED substituted
      errs BIT-EXACT (72/72, the machinery's native 2-dp convention;
      the verified flags 72/72), AND exp282's walk_end_rms reproduces
      BIT-EXACT (the fresh walk_end_rms == exp282's deposited
      walk_end_rms 72/72; the fresh trace sha256 == exp282's
      deposited trace_sha256 72/72 — the SAME walk exp282 deposited,
      which also proves the commit recording side-effect-free;
      err_exact 72/72; the fresh per-host end-RMS means == exp282's
      deposited host_table means 12/12). The carries: the mia carry
      bit-exact 12/12 (exp273's field table == exp243's own class
      records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS
      sha-verified against the current file bytes — exp243 (4) +
      exp256 (3) + exp272 (4) + exp273 (5) + exp282 (4) = 20 records.
      The source deposits READ-ONLY: sha-recorded BEFORE any read,
      byte-unchanged after the work (5 deposits: exp243, exp256,
      exp272, exp273, exp282).
  G2  THE COMMIT RECORDING + THE SELF-CONSISTENCY QUANTITY'S
      DEFINITION (zero-knob asserted, fail=STOP per row): the
      disclosed recording addition — the committed theta per cell
      recorded AT THE WRITE (after the write; the inherited/
      committed value whatever its source, with the source tag
      spec/canon/parent recorded audit-only) — draws nothing from
      the RNG stream and touches no state (proven by G1's bit-exact
      trace shas). Per row: the commit count == walk_steps == the
      trace length 72/72 (the write set fully recorded); the commit
      indices UNIQUE — each committed cell exactly once (the commit
      sequence re-read is a clean replay) 72/72; the replica-side
      write-set coverage: the commit sequence elementwise == the
      walked order (asserted inside the replica where the region is
      in scope) 72/72; the commit values finite 72/72; the commit
      sequence digest sha256 recorded per row (the full commit
      sequences NOT re-deposited — bit-reproduced via the digest +
      G1's trace shas, the exp284/exp285/exp286 precedent); THE
      REPLAY built ONLY from the recorded commits (the construction
      reads the commit list + the final state and nothing else — no
      re-simulation, no parameters, no external target enters the
      replay); sc_rms finite 72/72; the denominators err_exact > 0
      72/72. The per-row decode integrity: the A3 state convention
      (round(err_exact, 2) == the reported err) asserted fail=STOP
      72/72; the trace finite + trace[-1] > 0 + the trace length ==
      walk_steps 72/72; the convergence point exists (TA3, exp282's
      assert form) 72/72; the S* lock reads 72 (the lock log
      asserted); the exp284-style settle gap |err_exact -
      walk_end_rms| recorded audit-only.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): per host
      mean_sc (the 6-row mean of sc_rms) vs mean_gap (the 6-row mean
      of err_exact); the host self-consistent iff mean_sc <
      SC_FRAC_BAR * mean_gap (SC_FRAC_BAR 0.01); N_sc >= SC_MIN_HOSTS
      (10) -> SELF-CONSISTENT; else SELF-DRIFT. Audit-only, never
      gating: the per-row sc fractions sc_rms/err_exact; the
      commit-vs-target RMS on the committed cells (cvt_rms — where
      the error lives: the committed pattern vs the deep target on
      the program's own write set); the per-row + per-host source
      censuses (how many commits drew from the spec layer vs the
      canon vs the parent — the program's self-knowledge face); the
      exp284-style settle gaps; the max/min per-row sc per host; the
      audit-only regressions of mean_sc and mean_cvt against
      mia_prod_err (exp273's field table, asserted == exp243's own
      class records) and exp272's one-zone premium means (asserted
      == exp273's field-table carry) under the exp274/exp275/exp282
      conventions VERBATIM (Pearson on the tied-average ranks, the
      12-slot frame with the H0==H1 echo carried, the ties census
      per vector, the single-predictor rank R2) — does the
      self-consistency drift track the exposure (named honestly,
      never gating).
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, 72 decodes per pass; or
      the pre-named checkpoint-split EXP287_MODE=pass1|pass2 + merge
      with each pass a separate process; the two passes' payloads
      BIT-IDENTICAL, asserted at the merge/assembly); no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): SELF-CONSISTENT / SELF-DRIFT.

RUN: the deterministic sha-asserted rebuild (seconds) + 72 decodes per
pass ~ 60-90 s foreground per pass, TWO passes (G4) ~ 2-4 min total,
far under the 570 s cap per invocation. THE DEFAULT TWO-PASS
IN-PROCESS FORM (no env): the full battery computed twice in one
invocation. THE PRE-NAMED CHECKPOINT-SPLIT ALTERNATIVE:
EXP287_MODE=pass1|pass2 computes and caches ONE pass's payload per
invocation; EXP287_MODE=merge compares the two cached payloads
BIT-EXACT, assembles, evaluates the gates once, writes the deposit —
the merge NEVER re-decodes — and removes the caches. Both forms
evaluate the SAME gates and assert the same bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp287_fixed_point_identity.json")


def main() -> dict:
    raise NotImplementedError(
        "exp287 body — written by the run agent under the body-only "
        "discipline; the docstring/imports/constants above are the "
        "pre-registration and stay byte-unchanged")


if __name__ == "__main__":
    main()
