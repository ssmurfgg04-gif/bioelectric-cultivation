#!/usr/bin/env python3
"""exp280 — THE CHAIN'S HEAD: THE DEEP-BAND READ vs THE HOSTS' OWN
ADJACENCY STRUCTURE (batch 38; batch-37's derived item, ledger L257 —
zero new simulation).

THE OPEN ITEM: exp273 named H3/H5 the outliers at mia_prod_err 2.12/
2.28 vs the ten-host cluster's [0.49, 0.52] — they are the two
boundary-richest hosts (47/48 of the 400 cells canon-boundary vs the
cluster's [31, 43]). exp276 located the outliers' audit error 94% in
the P3 deep-band arm; exp277 showed the deep-band break is class-blind
(the cluster-typical error mixture amplified ~7x, not shifted);
exp278 showed the amplification is mia-scaled (rho 0.7250) and NOT
canon-boundary-count-scaled (-0.0596); exp279 closed the aggregation
face (AUDIT-MAX — the audit error rides the worst arm). The one
instrument never pointed at the deep-band exposure: the hosts' OWN
base adjacency structure. The question this module asks: is the
deep-band read's per-host error carried by the deposited adjacency's
own topology — the degree spectrum, the clustering, the boundary
cells' own degree, the pair-support density — or is the exposure
ABSENT from that structure (named honestly)?

THE INSTRUMENT (pre-registered, zero-knob): a pure re-read + a
DETERMINISTIC REBUILD of the deposited base adjacencies — exp269's/
exp256's rebuild form (the exp243/exp225 construction), every rebuild
bit-asserted against exp243's own records; ZERO new simulation (no
read, no decode, no dynamics — the rebuild is a deterministic graph
construction whose shas are pinned by the deposit):

  1. THE REBUILD: the 12 base adjacencies at the deposited ns
     (exp243's classes records carry n per host): H0/H1 the chain/
     path constructor graph_path(n) (the H0 slot echoes H1 bit-
     exactly — exp243's own disclosure, asserted); H2-H11
     small_world(n, 0.10, int(rec["rewire_seed"])) at the deposited
     rewire seeds. Every rebuild asserted against exp243's records:
     sha256(|A| as float64) == rec["base_sha256"]; the upper-triangle
     edge count == rec["edges_base"]; the exp208 classify CANON-
     BOUNDARY count == rec["n_boundary_cells_base"] (dual-carried vs
     exp272's per-host records and exp278's table); the canon
     identity labeling_bfs_n(|A|) == labeling_bfs_n(A).

  2. THE STRUCTURAL FIELDS (zero-knob, per host, from the rebuilt
     base A and its canon labeling; the pair support = |A| > 0, the
     degree = the per-cell support degree, symmetric):
     F1 deg_mean   — the mean of the degree spectrum over the n cells;
     F2 deg_max    — the max of the degree spectrum;
     F3 deg_spread — the max minus the min of the degree spectrum;
     F4 clustering — the mean local Watts-Strogatz clustering
        coefficient (deg >= 2: 2*E(N_i)/(d_i*(d_i-1)) with E the
        support edges among the cell's neighbors; deg < 2: 0.0);
     F5 boundary_degree_mean — the mean degree over the CANON-
        BOUNDARY cells (exp208's classify instrument: the canon
        labeling's ring-backbone value transitions);
     F6 pair_support_density — the support pairs in the upper
        triangle over n*(n-1)/2.
     DISCLOSED DEGENERACY (fixed BEFORE the body, from the
     deterministic rebuild of the deposited seeds — the exp277
     deposit-read disclosure precedent): the deposited rewire seeds'
     chords form NO triangles on any of the 12 rebuilt bases, so F4
     is identically 0.0 on all 12 (ASSERTED at G2, fail = STOP — the
     pre-registration describes the deposited data; drift fails
     loudly, no tuning). A constant field has no rank variance: F4's
     Spearman is UNDEFINED (recorded null) and F4 is EXCLUDED from
     the branch max — forced by the degeneracy, never chosen. The
     other five fields enter the max regardless of outcome. The H0
     slot echoes H1 bit-exactly (the chain class's n=400 call site,
     exp243's own disclosure) — the field table carries both slots;
     the regressions run on the 12-slot frame (the house convention,
     exp278's ties-census precedent).

  3. THE RESPONSES (the 12-host table): R1 = the deep-band read err
     per host — the mean over the 3 substituted rows' worst_err in
     exp256's deposited 72 rows (the exp255/exp256 arm-worst
     convention; bit-exact vs exp276's m_P3, exp273's field-table
     worst_err_mean_substituted, and exp278's per-host m_P3);
     R2 = the amplification ratio per host, read from exp278's
     deposited per-host table (asserted == its m_P3/m_P12_pooled
     identity bit-exact, with m_P12_pooled == the pooled mean over
     the 6 canonical instance errs replicated from exp256's rows in
     exp278's exact (seed, P1, P2) convention).

  4. THE REGRESSIONS (the exp274/exp275 conventions VERBATIM): per
     (response, field) the Spearman rho = Pearson on the tied-average
     ranks (scipy rankdata); the single-predictor OLS rank R2 (the
     response enters as its tied-average ranks, the field as the
     numeric design column); the all-ranks variant (the field ranked
     too — single R2 == rho^2 within 1e-12) AUDIT-ONLY; the ties
     census per vector. R2's regressions are REPORTED, never gating.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY: READ-ONLY sha-verified — the 12 rebuilt
      bases bit-asserted against exp243's records (base_sha256 12/12,
      edges_base 12/12, the classify boundary count 12/12 dual-carried
      vs exp272 + exp278, the canon identity 12/12, H0 == H1);
      exp256's 72 rows complete (12 hosts x 2 arms x 3 seeds) with
      worst_err == the max of the instance errs 72/72 and the
      instance structure 72/72 (canonical = P1+P2; substituted =
      r-60i0/r-60i1); the R1 triple carry bit-exact (exp276's m_P3 ==
      exp273's field table == exp278's m_P3 == the recomputed mean,
      12/12 each); exp278's ratio identity bit-exact 12/12; the
      outlier pre-name asserted 4-way (exp273 == exp272.descriptive.
      premium_hosts == exp276 == exp278 == ['H3','H5']); the
      provenance chains sha-verified against the actual deposit bytes
      (exp278's recorded inputs 11/11, exp276's 8/8, exp273's 5/5);
      READ-ONLY (12 deposits sha-recorded before, byte-unchanged
      after).
  G2  THE FIELD TABLE'S COMPLETENESS: the 12 x 6 field table
      complete with every field value finite; the structural
      identities asserted per host (deg_mean == 2*edges/n within
      1e-12; pair_support_density == edges/(n*(n-1)/2) bit-exact;
      the boundary mask nonempty); the DISCLOSED F4 degeneracy
      asserted (F4 == 0.0 on all 12 — fail = STOP); every field's
      distinct-level census recorded; the rho table complete (the
      five non-degenerate fields numeric on both responses, F4 null
      on both — the disclosed undefined).
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      TOPOLOGY-CARRIED iff >= 1 of the FIVE non-degenerate structural
      fields (F1, F2, F3, F5, F6) reaches Spearman >= 0.5 (the house
      bar — the exp274/exp278 SIGNED convention: the pre-named
      richness->exposure direction) against the deep-band read err
      R1; else TOPOLOGY-ABSENT (the exposure is not in the deposited
      adjacency's structure — named honestly). THE ABS VARIANT,
      pre-named: max |rho| over the same five fields recorded
      audit-only alongside — a field crossing |rho| >= 0.5 with a
      NEGATIVE sign is the ANTI-ALIGNED face (the field runs OPPOSITE
      the pre-named direction); it is NAMED in the deposit and the
      verdict, never gating. R2's regressions, the all-ranks
      variants, and the outlier-vs-cluster field margins are
      audit-only, never gating.
  G4  THE DISCIPLINE: deterministic — two-pass bit-identical; no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the deposits READ-ONLY sha-recorded byte-unchanged; the
      docstring+header pinned to this pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted
      at exit.

THE BRANCHES (pre-named): TOPOLOGY-CARRIED / TOPOLOGY-ABSENT.

RUN: a deposit re-read + a deterministic adjacency rebuild + rank
arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp280_chain_head.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
