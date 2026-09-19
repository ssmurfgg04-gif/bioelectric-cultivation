#!/usr/bin/env python3
"""exp288 — THE SPEC LAYER'S FACE: WHAT MAKES THE COMPILER'S SPEC-LAYER
COMMITS DEEP-BAND-HOST-DEPENDENT? (batch 46; ledger L265's registered
next (a) — the decomposition of exp287's commit layer, the premium's
structural address: batch 45 closed the mechanism line at the compiler
with the committed pattern itself carrying the exposure
(rho(mean_cvt)~mia +0.8616 / ~premium +0.7790) while every grain
screened so far is class-blind (exp277's decode NEITHER, exp284's walk
CLASS-BLIND, exp285's ring ABSENT). Before the chain rests, the commit
layer's OWN face gets its decomposition: the commit error by cell
class, and the commit values against the spec's own named voltages.)

THE OPEN ITEM: exp287 landed SELF-DRIFT with the exposure carried by
the COMMITTED PATTERN (mean_cvt spread 0.587059-0.631465 across the 12
hosts, the rank carriage +0.8616/+0.7790) and recorded the commits'
source census: every one of the 20802 commits drew from the SPEC layer
(spec 20802 / canon 0 / parent 0). The landed write path fixes WHAT the
spec layer contains: set_target(canon) installs phi_spec = canon,
write_spec_layer(target) then re-installs phi_spec = target BIT-EXACTLY
(a plain array copy) and preserves the pre-program memory as
phi_spec_canon; the dynamics (step/run/clamp/amputate) never touch
phi_spec — so at the write, phi_spec[i] == target[i] bit-exact and each
commit is phi_spec[i] + ONE commit-noise draw (exp142's COMMIT_NOISE
0.6, the machinery's own constant). The commit values' bases are
therefore the target values themselves: the spec's PRE-NAMED deep-rung
voltage -60.0 on the deep-zone cells, the canon's gap values (-50.0
trunk / -20.0 head) on the un-named gap cells the write inherits. THE
STRUCTURAL QUESTION (this module, zero new knobs): with the per-cell
commit error being exactly one commit-noise draw, WHAT makes the
committed pattern deep-band-host-dependent? Candidate carriers: the
commit error's CLASS structure — the squared commit error concentrates
in a classify class beyond that class's cell share (SPEC-GEOMETRIC) —
or NOTHING in the spec layer's content, the host-dependence entering
only through the noise DRAWS' stream positions and the walked count
(SPEC-UNIFORM — class-blind like every other level screened). The
draw-stream reading (disclosed, asserted as its observable
consequence): the walk's dt = star_dt at the S* operating point, scaled
by the projected adjacency's max degree (host-dependent), sets how much
rng the encode window + the per-cell interludes consume before each
commit — hosts sharing dt share the commit-draw sequence, hosts sharing
dt AND the per-row walked counts share the commit-value multisets
BIT-EXACT, and the commit-vs-target RMS — the RMS of pure draws —
cannot see the walk ORDER at all.

THE INSTRUMENT (pre-named, zero knobs): exp287's landed body REUSED
VERBATIM — the state-carrying traced replica with the commit recording
(_execute_signed_traced with the disclosed recording addition (f), the
RNG stream / dt / canon / walk order / commits untouched; exp142 NOT
modified) at the production budget 8 == exp142's STEPS_PER_CELL, the
host rebuild (exp269's/exp280's form), exp256's _scoped_row_read_state
form (the projection chain PN1/PN2 + TC1 + TC2 + the traced TC3) — ONE
FRESH RUN of the SAME 72 substituted rows (12 hosts x 3 seeds (1,2,3) x
r-60i0/r-60i1 at n=400, exp256's battery). The decomposition (pure
rebuild + arithmetic, ZERO new knobs):

  (1) THE COMMITTED PATTERN REBUILT per row: the commit sequence
      re-read (the recorded committed theta per cell in walk order —
      exp287's replay form verbatim; the replay built ONLY from the
      recorded commits — no re-simulation, no parameters, no external
      target enters it); the per-cell commit error
      e_i = commit_i - T_i against the row's deep target, on the
      program's write set (the replay's support: exactly the cells
      the executed program wrote, each exactly once).
  (2) THE CLASS DECOMPOSITION (exp208's classify VERBATIM, applied
      per instance — classify(T_instance, A_host) — the CLEAN masks:
      CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR, disjoint, covering;
      the exp208-label cls-array records carried audit-only
      alongside, exp284's disclosure repeated: cls 1 = the
      pair-junctions off the boundary ring, cls 0 = the boundary ring
      AND the interior riding the same mask, cls 2 never occurs —
      asserted): per row and per class c on the write set —
      n_c = |c intersect write|, cell_share_c = n_c / n_write,
      sum_sq_c = sum e_i^2 over c, frac_of_sq_c = sum_sq_c / total,
      rms_contrib_mV = sqrt(sum_sq_c / n_write), and the
      concentration ratio R_c = frac_of_sq_c / cell_share_c (a class
      with n_c == 0 on a row is recorded with zero shares and R
      null, disclosed — the branch reads the POOLED form below).
  (3) THE COMMIT-VALUE DISTRIBUTION'S OWN STRUCTURE: the base census
      (the distinct target values at the committed cells, with
      counts — the spec's pre-named voltage -60.0 vs the canon gap
      values), THE NAMED-BASE FRACTION (#{s_i == -60.0} / n_write —
      the histogram's mass whose base IS the spec layer's named
      voltage), THE EXACT-LANDING COUNT (#{commit_i == -60.0}
      bit-exact — what fraction of commits land EXACTLY on the spec
      layer's named voltage: the noise-vanished face; and
      #{commit_i == s_i} — the noise-vanished face on any base),
      and the error moments (mean/std/min/max of e_i — the population
      std — and the fraction |e_i| <= COMMIT_NOISE, the machinery's
      own sigma).

THE PRE-NAMED BRANCH (the bars numeric, fixed HERE at
pre-registration, never fit): per host, the 6 rows POOLED per class
(the sums and counts added over the host's rows — the pooling kills
the small-class single-row variance, the probe-level fluctuation of
R on ~12-27-cell classes reaching ~0.5, disclosed); the host's
concentration R_max = max over non-empty classes of the pooled R_c;
CONC_BAR = 1.50 (a class holding >= 1.5x its committed-cell share of
the squared commit error);
  SPEC-GEOMETRIC iff #{hosts with R_max >= CONC_BAR} >=
      CONC_MIN_HOSTS (10) — the commit error's class decomposition
      concentrates in a class;
  else SPEC-UNIFORM — class-blind like every other level.
Audit-only, never gating: the per-row R table; the exp284-style
outlier-vs-cluster margins on the pooled clean-mask fracs (margin_c =
min over {H3,H5} - max over the cluster, the 0.05 bar form, recorded
honestly); the mean_cvt~mia / ~premium regressions under the
exp274/exp275/exp282 conventions VERBATIM (asserted == exp287's
deposited rhos BIT-EXACT — the anchor); THE DRAW-STREAM FACE (the
mechanism audit, deterministic arithmetic on the rows, asserted
fail=STOP): the hosts grouped by (dt, the 6-row walked-count vector)
must carry BIT-IDENTICAL per-row cvt_rms within a group, and cvt_rms
must be BIT-IDENTICAL across the two instances of every (host, seed)
pair — the commit values are the spec's bases + draw-stream positions
and cannot see the walk order; the per-host dt + the projected
adjacency's max degree recorded (the dt recomputed OUTSIDE the replica
by the same pure projection calls — project_phase_native +
flip_clock_matrix on the base medium: no rng, no state, a pure read).

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285/exp286/exp287
      precedent (graph_path at the chain class's n=400 call site for
      H0/H1 — H0 echoes H1 bit-exactly, asserted; small_world(n, 0.10,
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
      TRAJECTORY-CARRIED asserted; exp282's host_table
      walk_end_rms_mean present for the 12 hosts. THE EXP287 RE-READ:
      the 72 row records present with commit_seq_sha256 + cvt_rms +
      n_commits + sc_rms; the 12-host mean_cvt present. THE S0 ANCHOR
      (the production-budget battery): the re-run's reported errs
      reproduce exp256's DEPOSITED substituted errs BIT-EXACT (72/72,
      the machinery's native 2-dp convention; the verified flags
      72/72), exp282's walk_end_rms reproduces BIT-EXACT (the fresh
      walk_end_rms == exp282's deposited walk_end_rms 72/72; the
      fresh trace sha256 == exp282's deposited trace_sha256 72/72;
      err_exact 72/72; the fresh per-host end-RMS means == exp282's
      deposited host_table means 12/12), AND exp287's COMMIT LAYER
      reproduces BIT-EXACT (the fresh commit sequence digests ==
      exp287's deposited commit_seq_sha256 72/72 — the SAME commits
      exp287 recorded; the fresh per-row cvt_rms == exp287's 72/72;
      the fresh n_commits == exp287's 72/72; the fresh sc_rms ==
      exp287's 72/72; the fresh per-host mean_cvt == exp287's
      deposited mean_cvt 12/12). The carries: the mia carry bit-exact
      12/12 (exp273's field table == exp243's own class records) +
      the premium carry bit-exact 12/12 (exp272 == exp273's
      field-table carry). THE PROVENANCE CHAINS sha-verified against
      the current file bytes — exp243 (4) + exp256 (3) + exp272 (4) +
      exp273 (5) + exp282 (4) + exp287 (5) = 25 records. The source
      deposits READ-ONLY: sha-recorded BEFORE any read, byte-unchanged
      after the work (6 deposits: exp243, exp256, exp272, exp273,
      exp282, exp287).
  G2  THE COMMIT REPLAY + THE DECOMPOSITION'S ACCOUNTING IDENTITY
      (zero-knob asserted, fail=STOP per row): the commit recording
      bookkeeping (the exp287 form: the commit count == walk_steps ==
      the trace length 72/72; the commit indices UNIQUE — each
      committed cell exactly once 72/72; the replica-side write-set
      coverage — the commit sequence elementwise == the walked order
      72/72; the commit values finite 72/72; the source census sane
      72/72; the commit sequence digest sha256 recorded 72/72 — the
      full sequences NOT re-deposited, bit-reproduced via the digests
      + G1's anchors). THE DECOMPOSITION: per row the three clean
      classes partition the write set (the class counts sum to
      n_write 72/72; the masks disjoint and covering by construction,
      asserted via the classify source); the exp208-label cls-2
      count == 0 72/72 (the exp277/exp284 disclosure, asserted);
      THE ACCOUNTING IDENTITY on the scale the RMS actually
      decomposes: sum_c sum_sq_c / n_write == cvt_rms^2 within
      1e-6 * max(1.0, cvt_rms^2) (exp208's/exp284's identity form on
      the write-set support, disclosed) 72/72, and the fracs sum to
      1.0 within 1e-9 72/72. THE HISTOGRAM's sanity: the base census
      sums to n_write 72/72; the named-base + gap-base partition
      72/72; the exact-landing count within [0, n_write] 72/72; the
      error moments finite 72/72. The per-row decode integrity: the
      A3 state convention (round(err_exact, 2) == the reported err)
      asserted fail=STOP 72/72; the trace finite + trace[-1] > 0 +
      the trace length == walk_steps 72/72; the convergence point
      exists (TA3) 72/72; the S* lock reads 72; the exp284-style
      settle gap recorded audit-only.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): per host
      the pooled decomposition; R_max vs CONC_BAR 1.50; N_conc >=
      CONC_MIN_HOSTS 10 -> SPEC-GEOMETRIC; else SPEC-UNIFORM. The
      mean_cvt~mia / ~premium regressions asserted == exp287's
      deposited rhos BIT-EXACT (the anchor, fail=STOP; the house
      conventions verbatim: Spearman = Pearson on the tied-average
      ranks, the single-predictor OLS rank R2, the ties census per
      vector, the 12-slot frame with the H0==H1 echo carried).
      Audit-only, never gating: the per-row R table; the exp284-style
      margins (the 0.05 bar form); the draw-stream face's cvt-tie
      groups + the per-host dt record; the orderings by R_max; the
      outlier-vs-cluster faces; the pooled base censuses; the pooled
      named-base + exact-landing totals; the error moments vs
      COMMIT_NOISE.
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, 72 decodes per pass; or
      the pre-named checkpoint-split EXP288_MODE=pass1|pass2 + merge
      with each pass a separate process; the two passes' payloads
      BIT-IDENTICAL, asserted at the merge/assembly); no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): SPEC-GEOMETRIC / SPEC-UNIFORM.

RUN: the deterministic sha-asserted rebuild (seconds) + 72 decodes per
pass ~ 60-90 s foreground per pass, TWO passes (G4) ~ 2-4 min total,
far under the 570 s cap per invocation. THE DEFAULT TWO-PASS
IN-PROCESS FORM (no env): the full battery computed twice in one
invocation. THE PRE-NAMED CHECKPOINT-SPLIT ALTERNATIVE:
EXP288_MODE=pass1|pass2 computes and caches ONE pass's payload per
invocation; EXP288_MODE=merge compares the two cached payloads
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
OUT = os.path.join(ROOT, "results", "exp288_spec_layer_face.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp288's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
