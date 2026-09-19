#!/usr/bin/env python3
"""exp284 — THE ENDPOINT COMPOSITION: THE END-RMS CARRIER DECOMPOSED BY
CELL CLASS AT THE WALK LEVEL (batch 42; batch-41's derived item, ledger
L261 — exp283's verdict put the exposure in WHERE THE WALK ENDS, not in
where it settles; this module opens that endpoint).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED — the walk's end RMS
(TA1 walk_end_rms, the per-step RMS-to-target curve's final value) is
the strongest carrier yet named (signed Spearman +0.8826 against
mia_prod_err, +0.8807 against exp272's one-zone premium means; the 0.5
SIGNED house bar). exp277 asked the same WHERE question at the DECODE
level — exp256's deposited per-row decompositions through exp208's
cell-class machinery — and found the decode-level break CLASS-BLIND
(branch NEITHER: the outliers' cb shares 0.1513/0.2265 vs the cluster
max 0.1767, both margins NEGATIVE). THE NEW SURFACE: the WALK level —
the end-RMS carrier's own per-cell composition. The question: does the
outlier hosts' end-RMS mass concentrate in CANON-BOUNDARY cells at the
walk level, in PAIR-JUNCTION cells, or is the walk-level break ALSO
class-blind (matching exp277)?

THE INSTRUMENT (pre-registered, zero-knob): the pure re-reads where
possible + THE MINIMAL FRESH STATE-CARRYING RE-RUN where the per-cell
end state is needed.

  THE PURE RE-READS (no new simulation): exp282's trajectory deposit —
  the 72 per-row traces + the three summaries + the 12-host means
  table; the carrier (walk_end_rms per row) carried BIT-EXACT.
  exp256's 72-row battery — the deposited substituted instance errs
  (the S0 anchor's targets), the row/instance shas, the row-level
  class_counts. exp272's per-host one-zone premium means + exp273's
  field table (the mia field + the premium carry). exp277's per-host
  decode-level shares (the walk-vs-decode face, audit-only).

  THE FRESH RE-RUN (the minimal form): exp282's _execute_signed_traced
  replica REUSED VERBATIM (landed at 8ca252e — exp142's walk
  byte-similar + exactly the disclosed recording additions: the
  per-step RMS read after each commit, the trace + step-count fields,
  the final state always carried; the RNG stream / dt / canon / walk
  order / commits untouched; exp142 NOT modified), called through
  exp256's _scoped_row_read_state form (the projection chain PN1/PN2 +
  TC1 + TC2 + the traced TC3), on the SAME 72 substituted rows
  (12 hosts x 3 seeds (1,2,3) x the two deep instances r-60i0/r-60i1
  at n=400 — exp256's battery, ONE FRESH RUN).

  THE PER-CELL END ERRORS: from the state-carrying read's final_state
  (the replica's disclosed addition (c)): e_i = V_i - T_i over the
  n=400 frame. THE END-RMS (the decomposition's object):
  err_exact = sqrt(mean(e^2)) — the A3-checked state convention.
  DISCLOSED (pre-body): exp282's walk_end_rms carrier is the PRE-settle
  trace[-1]; the final_state end state is POST-settle (exp142's fixed
  15.0 settle tail runs between the walk's last commit and the state
  return — a fixed part of the executor, not a knob); the trace stores
  scalars, not the frame, so the end state is the ONLY per-cell end
  record the landed machinery provides. The per-row settle gap
  |err_exact - walk_end_rms_carried| is recorded per row (audit-only;
  exp282's deposited rows put it at ~1e-3 mV — e.g. H3 s1 i0: 3.6759
  vs 3.6748).

  THE CLASSIFICATION (exp208's classify VERBATIM on the row target +
  medium): CANON-BOUNDARY (the cell sits on a canon-value boundary in
  the target — a ring neighbor's target value differs), PAIR-JUNCTION
  (endpoint of >= 2 chords in the medium's pair support |A_base| > 0),
  INTERIOR (neither); precedence the registered listing order (the
  boundary wins, then the junction). Applied per INSTANCE
  (classify(T_instance, A_host) — the two deep targets differ by the
  instance shift). THE MASK SEMANTICS (exp277's disclosure, carried):
  exp208's decompose reads the cls array — cls 1 = PAIR-JUNCTION (the
  junctions off the boundary ring), cls 0 = otherwise (the boundary
  ring + the interior ride the same mask; cls is never 2) — so the
  per-class CANON-BOUNDARY record is the NON-PAIR-JUNCTION complement
  of the squared error and the INTERIOR record is empty; the branch
  reads the labels at face value (exp277's convention) for
  walk-vs-decode comparability, and THE PURE-MASK SPLIT (the boundary
  ring's own share vs the interior's own share, computed directly from
  the masks — recoverable in the fresh run, unlike exp277's deposit
  re-read) is recorded alongside, audit-only.

  THE DECOMPOSITION (exp208's decompose conventions VERBATIM): per
  class c — sum_sq_c = sum_{i in c} e_i^2; frac_of_sq = sum_sq_c /
  total; rms_contrib_mV = sqrt(sum_sq_c / n). THE ACCOUNTING IDENTITY
  (G2): sum_c sum_sq_c / n == err_exact^2 — the mean-squared scale the
  RMS actually decomposes (an mV-linear split would be a fake
  identity) — and the fracs sum to 1.0.

  THE PER-HOST TABLE: per-host means over the host's 6 rows (3 seeds x
  2 instances) of frac_cb / frac_pj / frac_int (the exp208-label
  shares), the pure-mask shares, the rms_contrib means, the mean class
  counts, the err_exact and walk_end_rms_carried means.

  THE BRANCH (the discriminant pre-named, the bars numeric, the
  exp277 form): the outliers = exp273's deposited outliers (asserted
  == exp272's descriptive.premium_hosts == ['H3', 'H5']); the cluster
  = the other ten. margin_cb = min(frac_cb_mean over {H3, H5}) -
  max(frac_cb_mean over the cluster); margin_pj likewise.
  WALK-BOUNDARY iff margin_cb >= 0.05 AND margin_cb >= margin_pj;
  WALK-PAIR iff margin_pj >= 0.05 AND margin_pj > margin_cb;
  WALK-CLASS-BLIND otherwise — the exhaustive residual, INCLUDING the
  weak-ordering face (an ordering that holds below the 0.05 bar is
  recorded honestly; the branch stays class-blind). The 0.05
  CONCENTRATION BAR = 5 percentage points of the squared-error share
  (fixed HERE at pre-registration, never fit; exp277's decode-level
  margins were NEGATIVE — -0.0255 cb / -0.1792 pj — so any positive
  walk-level ordering is already new information, recorded in full).
  The both-exceed case: the LARGER margin names the branch; exact
  float equality of the margins (never expected) resolves
  WALK-BOUNDARY (the pre-named order).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280 precedent (graph_path at the chain
      class's n=400 call site for H0/H1 — H0 echoes H1 bit-exactly,
      asserted; small_world(n, 0.10, deposited rewire_seed) for
      H2-H11), bit-asserted against exp243's records: sha256(|A| as
      float64) == base_sha256 12/12; the upper-triangle edge count ==
      edges_base 12/12; the classify boundary-ring count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity
      labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12; f_max recomputed
      == f_max_base 12/12. The two deep-row targets rebuilt per
      exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited instance medium_sha256 72/72. exp256's 72 rows
      with the substituted structure 36/36 + worst == max 36/36. THE
      RE-READS: exp282's 72 traces complete per row (len ==
      walk_steps >= 1, all finite, final > 0, the convergence point
      existing, trace_sha256 recomputed 72/72) + the three summaries
      re-derived from the deposited traces BIT-EXACT 72/72 x 3 + the
      per-host means bit-exact vs exp282's host_table 12/12 x 3; the
      mia carry bit-exact 12/12 (exp273's field table == exp243's own
      class records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS sha-verified
      against the current file bytes — exp243 (4) + exp256 (3) +
      exp272 (4) + exp273 (5) + exp282 (4) + exp277 (8) = 28 records.
      The source deposits READ-ONLY: sha-recorded BEFORE any read,
      byte-unchanged after the work.
  G2  THE RE-RUN'S ANCHORS + THE ACCOUNTING IDENTITY: the fresh
      state-carrying re-run of the 72 rows through exp282's traced
      replica REUSED VERBATIM — THE S0 ANCHOR: every row's final err
      reproduces exp256's DEPOSITED substituted instance err BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags 72/72) and exp282's deposited walk reproduced BIT-EXACTLY
      (the re-run's per-row trace_sha256 == exp282's deposited
      trace_sha256 72/72 — the decomposition is of the SAME walk
      exp282 traced; the fresh walk_end_rms == exp282's deposited
      walk_end_rms 72/72, float-identical). THE A3 STATE-CONVENTION
      ASSERT 72/72 (round(err_exact, 2) == the reported err — the end
      state's own RMS is the reported err's exact form). THE
      CLASSIFICATION ANCHOR: the fresh classify's pure mask counts on
      each row's WORST instance == exp256's deposited row-level
      class_counts 36/36 (the classification machinery reproduces
      exp256's deposited classify). THE ACCOUNTING IDENTITY per row
      (all 72): sum_c sum_sq_c / n == err_exact^2 within 1e-6 *
      max(1.0, err_exact^2) (exp208's identity form, asserted
      fail=STOP); the fracs sum to 1.0 within 1e-9; the pure masks
      partition n=400 (the counts sum to 400, the masks pairwise
      disjoint, 72/72); the per-row identity residual + the settle gap
      recorded (the max of each, audit-only).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): the
      branch resolved on the pre-named margins (the exp277 min-vs-max
      form + the 0.05 concentration bar + the pre-named precedence):
      WALK-BOUNDARY / WALK-PAIR / WALK-CLASS-BLIND. Audit-only, never
      gating: the full 12-host ordering by frac_cb_mean and
      frac_pj_mean; exp277's decode-level margins re-read from its
      deposit and recomputed from its per-host table (asserted equal)
      beside the walk-level margins (the walk-vs-decode face); the
      pure-mask split (the boundary ring's own share vs the
      interior's own share) per host; the per-host shares' Spearman
      against mia_prod_err and the one-zone premium (the
      exp274/exp275/exp282 conventions VERBATIM — Spearman = Pearson
      on scipy's tied-average ranks, the 12-slot frame with the
      H0==H1 echo carried, the ties census per vector, the
      single-predictor rank R2; the interior share's degeneracy —
      identically 0.0 on the exp208-label reading — excluded from the
      regressions, disclosed, exp280's F4 precedent).
  G4  THE DISCIPLINE: deterministic — the fresh re-run executes TWICE,
      the two passes' row payloads (errs, decompositions, tables,
      margins) BIT-IDENTICAL; no wall-clock fields (recursive key scan
      + serialized-blob scan); the docstring + header pinned to this
      pre-registration commit, asserted at entry AND exit; the source
      deposits byte-unchanged; NEURAL_SPEC_MIN == -60.0 asserted at
      exit (exp218's disclosed exp169-import discipline — the whole
      reader chain imported FIRST, the floor restored after; the
      -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): WALK-BOUNDARY / WALK-PAIR / WALK-CLASS-BLIND.

RUN: the deterministic sha-asserted rebuild (seconds) + the pure
re-reads + the fresh 72-row state-carrying battery run TWICE (72
decodes per pass), foreground ~2-3 min. If a pass cannot finish inside
the 570 s foreground cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE pass
per invocation (env EXP284_PASS=pass1|pass2 caches that pass's row
payload) and the PRE-NAMED MERGE (env EXP284_MERGE=1) compares the two
cached payloads BIT-EXACT and writes the deposit — the merge never
recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp284_endpoint_composition.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
