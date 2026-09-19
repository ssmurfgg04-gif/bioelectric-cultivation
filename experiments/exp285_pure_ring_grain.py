#!/usr/bin/env python3
"""exp285 — THE PURE RING GRAIN: THE END-RMS CARRIER'S MASS IN THE RING
AROUND THE CLASSIFY BOUNDARY SET (batch 43; exp284's audit-only sub-bar
live lead — on the boundary's own share the outliers H3/H5 hold the two
highest values (0.1501/0.1601 vs the ten-host cluster's [0.0489,
0.1094], margin +0.0406) but the pre-named 0.05 bar was not crossed and
exp284's branch stayed WALK-CLASS-BLIND; this module widens the grain
by one hop: the ring of cells IMMEDIATELY AROUND the classify boundary
set).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED — the walk's end RMS
(TA1 walk_end_rms) is the strongest carrier yet named (signed Spearman
+0.8826 against mia_prod_err, +0.8807 against exp272's one-zone premium
means; the 0.5 SIGNED house bar). exp284 decomposed the carrier's
endpoint by cell class at the walk level and found it CLASS-BLIND on
the exp208-label reading (the margins NEGATIVE), while its audit-only
PURE-MASK SPLIT showed the boundary ring's OWN share carrying a clean
but sub-bar ordering — the one live lead. exp285 asks the grain
question that lead points at: does the end-RMS mass in the RING AROUND
the classify boundary set — the immediate non-boundary neighbors —
carry the exposure at the 0.5 signed bar?

THE RING (the zero-knob definition, fixed HERE at pre-registration):
per row, exp208's classify VERBATIM on the row target + medium
(classify(T_instance, A_host)) yields the boundary set B; the
RING = {j not in B : exists i in B with A[i,j] > 0} — the immediate
non-boundary neighbors of the classify boundary set on the medium's
pair support. The rebuilt bases are non-negative (asserted per host in
the rebuild), so the read A[i,j] > 0 IS the |A| > 0 support convention
exp208's classify itself uses. No thresholds, no weights, no degree
bars, no distance bands — zero knobs.

THE INSTRUMENT (pre-registered, zero new simulation beyond the one
battery): exp284's landed body REUSED VERBATIM — the traced replica
(_execute_signed_traced, landed at 8ca252e, reused verbatim since
f3ca053: exp142's walk byte-similar + exactly the disclosed recording
additions; the RNG stream / dt / canon / walk order / commits
untouched; exp142 NOT modified), the host rebuild (exp269's/exp280's
form), exp256's _scoped_row_read_state form (the projection chain
PN1/PN2 + TC1 + TC2 + the traced TC3), and the end-state decomposition
(exp208's classify + decompose conventions VERBATIM) — ONE FRESH RUN
of the SAME 72 substituted rows (12 hosts x 3 seeds (1,2,3) x the two
deep instances r-60i0/r-60i1 at n=400 — exp256's battery). THE ONLY
ADDITION: the ring mask + the per-row THREE-WAY end-RMS split boundary
/ RING / rest (exp208's decompose conventions VERBATIM on the
mean-squared scale: sum_sq / frac_of_sq / rms_contrib_mV; the identity
asserted fail=STOP). The per-cell end errors from the state-carrying
read's final_state (e_i = V_i - T_i over the n=400 frame); the
END-RMS = err_exact (the A3-checked state convention; the PRE-settle
trace[-1] carrier vs the POST-settle end state disclosed pre-body in
exp284 — carried; the settle gap recorded audit-only).

THE PER-HOST TABLE: per-host means over the host's 6 rows (3 seeds x 2
instances) of the ring share (frac_ring), the boundary's own share
(frac_boundary — exp284's pure boundary-ring share), the rest share
(frac_rest), the mean ring count, the mean boundary count, the
err_exact and walk_end_rms_carried means, the settle-gap mean.

THE REGRESSIONS: the per-host ring-share means against mia_prod_err
(exp273's field table, asserted == exp243's own class records) and
exp272's one-zone premium means (asserted == exp273's field-table
carry), Spearman under the exp274/exp275/exp282 conventions VERBATIM
(Pearson on the tied-average ranks, the 12-slot frame with the H0==H1
echo carried, the ties census per vector, the single-predictor rank
R2). Audit-only, never gating: the boundary-share and rest-share
regressions; the full 12-host ordering by the ring share; exp284's
audit-only face recomputed beside (the fresh per-host boundary shares
asserted == exp284's deposited pure_boundary_ring_share means
BIT-EXACT 12/12, and the outliers-vs-cluster pure-share margin
recomputed from the fresh means == the margin from exp284's deposited
means bit-exact).

THE BRANCH (pre-named, the bar numeric, fixed HERE at
pre-registration, never fit): RING-CARRIED iff the ring share's signed
Spearman reaches >= 0.5 — the SIGNED house bar, positive — against
>= 1 of the two targets; RING-ABSENT otherwise (named honestly). The
abs variant pre-named: a NEGATIVE rho <= -0.5 crossing = the
ANTI-ALIGNED face, named per target in the deposit + verdict, never
gating (exp280/exp281's precedent).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284 precedent (graph_path at the
      chain class's n=400 call site for H0/H1 — H0 echoes H1 bit-
      exactly, asserted; small_world(n, 0.10, deposited rewire_seed)
      for H2-H11), bit-asserted against exp243's records: sha256(|A| as
      float64) == base_sha256 12/12; the upper-triangle edge count ==
      edges_base 12/12; the classify boundary-ring count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity labeling_bfs_n(|A|)
      == labeling_bfs_n(A) 12/12; f_max recomputed == f_max_base 12/12;
      the bases NON-NEGATIVE asserted per host (the 0/1 support form —
      the ring's read A[i,j] > 0 is then literally the |A| > 0 pair
      support exp208's classify uses). The two deep-row targets rebuilt
      per exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited medium_sha256 72/72. exp256's 72 rows with the
      substituted structure 36/36 + worst == max 36/36. THE EXP284
      RE-READ: the 72 row records present with the per_class records +
      trace_sha256 + err_exact + err_deposited + pure_shares;
      exp284's deposited err_deposited == exp256's deposited
      substituted err 72/72 (the two deposits' chain anchor);
      exp284's deposited branch == WALK-CLASS-BLIND asserted (the
      pre-registered context). THE S0 ANCHOR (both halves, from the
      fresh battery): the re-run's final errs reproduce exp256's
      DEPOSITED substituted errs BIT-EXACT (72/72, the machinery's
      native 2-dp convention; the verified flags 72/72), AND exp284's
      deposited per-class shares reproduce BIT-EXACT (the fresh
      per_class frac_of_sq x 3 == exp284's deposited x 3, 72/72 x 3 —
      with sum_sq and n_cells asserted beside; the fresh err_exact ==
      exp284's err_exact 72/72; the fresh trace_sha256 == exp284's
      trace_sha256 72/72 — the decomposition is of the SAME walk
      exp284 deposited; the fresh boundary's own share == exp284's
      deposited pure boundary-ring share 72/72). The carries: the mia
      carry bit-exact 12/12 (exp273's field table == exp243's own
      class records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS sha-verified
      against the current file bytes — exp243 (4) + exp256 (3) +
      exp272 (4) + exp273 (5) + exp284 (6) = 22 records. The source
      deposits READ-ONLY: sha-recorded BEFORE any read, byte-unchanged
      after the work (5 deposits).
  G2  THE RING DEFINITION (zero knobs, asserted per row, all 72): the
      ring = {j not in boundary : exists i in boundary with
      A[i,j] > 0} on exp208's classify boundary set
      (classify(T_instance, A_host) VERBATIM) + the medium's pair
      support; asserted (a) DISJOINT from the boundary set — the
      constructed ring index set shares no element with the boundary
      index set, and (b) COVERING NO boundary cells — the boolean
      ring & boundary masks all-False; the three-way partition
      boundary / ring / rest covers n=400 (the counts sum to 400, the
      masks pairwise disjoint, 72/72); the ring NONEMPTY 72/72 (a
      degenerate empty ring STOPs honestly — fail=STOP); the per-row
      THREE-WAY identity sum_{parts} sum_sq / n == err_exact^2 within
      1e-6 * max(1.0, err_exact^2) (exp208's identity form, asserted
      fail=STOP) + the ring-split fracs sum to 1.0 within 1e-9; the
      A3 state-convention assert 72/72; the ring split's BOUNDARY part
      == exp284's deposited pure boundary-ring share BIT-EXACT 72/72
      (the new instrument tied to exp284's lead by construction, then
      asserted); the classification anchor — the fresh worst-instance
      mask counts == exp256's deposited row class_counts 36/36; the
      per-row ring count + the identity residual + the settle gap
      recorded (the maxima, audit-only).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): the
      branch resolved on the pre-named 0.5 SIGNED house bar —
      RING-CARRIED iff max(rho_ring~mia, rho_ring~premium) >= 0.5
      (positive), RING-ABSENT otherwise. Audit-only, never gating: the
      full 12-host ordering by frac_ring_mean; the boundary-share +
      rest-share regressions; the ANTI-ALIGNED variant named per
      target (rho <= -0.5); exp284's audit-only face recomputed beside
      (the fresh per-host boundary shares == exp284's deposited
      pure_boundary_ring_share means BIT-EXACT 12/12; the
      outliers-vs-cluster pure-share margin recomputed from the fresh
      means == the margin from exp284's deposited means bit-exact; the
      fresh ordering by the boundary share beside exp284's); exp284's
      WALK-CLASS-BLIND label margins re-read beside (the exp208-label
      shares stay the registered face — the ring is the NEW grain,
      additive, never a replacement).
  G4  THE DISCIPLINE: deterministic — the fresh re-run executes TWICE,
      the two passes' row payloads (errs, ring splits,
      decompositions, tables, rhos) BIT-IDENTICAL; no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): RING-CARRIED / RING-ABSENT.

RUN: the deterministic sha-asserted rebuild (seconds) + the fresh
72-row state-carrying battery run TWICE (72 decodes per pass),
foreground ~2 min total, far under the 570 s cap. If a pass cannot
finish inside the 570 s cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE
pass per invocation (env EXP285_MODE=pass1|pass2 caches that pass's
row payload) and the PRE-NAMED MERGE (env EXP285_MODE=merge) compares
the two cached payloads BIT-EXACT and writes the deposit — the merge
never recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp285_pure_ring_grain.json")


def main() -> dict:
    raise NotImplementedError(
        "exp285 body lands under the batch-43 pre-registration — the "
        "gates above are fixed before any body (the body-only "
        "discipline; exp174's precedent)")


if __name__ == "__main__":
    main()
