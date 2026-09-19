#!/usr/bin/env python3
"""exp281 — THE ANTI-ALIGNED FACE TESTED AT THE SIGNED BAR: THE
BOUNDARY CELLS' OWN DEGREE MEAN vs THE PREMIUM'S THREE CARRIERS
(batch 39; batch-38's derived item, ledger L258 — zero new
simulation).

THE OPEN ITEM: exp280 named the ANTI-ALIGNED face — the boundary
cells' own degree mean (boundary_degree_mean, F5 of exp280's field
table; chord-poorest on the outliers: H3 1.5957 / H5 1.5625 vs the
ten-host cluster's [1.5, 1.8974]) ran OPPOSITE the pre-named
richness->exposure direction at rho -0.6081 against the deep-band
read err — a crossing of the 0.5 ABS bar with the 0.5 SIGNED bar
unmet (the branch TOPOLOGY-ABSENT; the face named, never gating).
The question exp281 asks: does that field carry the PREMIUM at the
SIGNED 0.5 house bar — the premium level itself, its amplification,
and the audit error that named the outliers — or does it clear
nothing, closing the chord line and placing the premium's origin
formally OUTSIDE the deposited host records?

THE INSTRUMENT (pre-registered, zero-knob): a pure re-read + a
DETERMINISTIC REBUILD — exp280's rebuild VERBATIM (the
exp269/exp256 form: graph_path for H0/H1, small_world(n, 0.10,
int(rec["rewire_seed"])) at exp243's deposited rewire seeds), every
rebuild bit-asserted against exp243's own records; ZERO new
simulation (no read, no decode, no dynamics — the rebuild is a
deterministic graph construction whose shas are pinned by the
deposit). ONE structural field computed per host, with exp280's
EXACT definition, never re-fit:

  F5 boundary_degree_mean — the mean pair-support degree over the
     CANON-BOUNDARY cells (exp208's classify instrument on the canon
     labeling, the ring backbone i±1; support = |A| > 0, symmetric;
     degree = the per-cell support degree); asserted BIT-EXACT vs
     exp280's deposited field table 12/12 (G2 — the definition is
     exp280's, bit-identical, fixed at this pre-registration).

THE THREE TARGETS (the 12-host table, exp272's per_host order — the
order the batch asserted exp273/exp276/exp278/exp279/exp280 against):

  T1 = exp272's per-host ONE-ZONE PREMIUM means (the premium level
     itself): per_host[*]["one_zone_premium_mean"]; the mean
     identity asserted bit-exact 12/12 (the recomputed mean over the
     deposited per-seed rows one_zone_premiums_by_seed == the
     deposited mean == exp273's field-table carry
     exp272.per_host.one_zone_premium_mean);
  T2 = exp278's per-host AMPLIFICATION RATIOS: per_host_table[
     *]["amplification_ratio"]; asserted == its own
     m_P3/m_P12_pooled identity bit-exact 12/12 (exp280's carry);
  T3 = the AUDIT ERROR mia_prod_err — the 4-way carry asserted
     bit-exact 12/12 each: exp243's
     classes[h]["multi_identity_audit"]["prod_err"] == exp276's
     decomposition_table audit_prod_err == exp279's origin_table
     audit_prod_err == exp273's field-table values
     (exp243.classes.multi_identity_audit.prod_err).

THE REGRESSIONS (the exp274/exp275 conventions VERBATIM): per
target, the Spearman rho = Pearson on the tied-average ranks (scipy
rankdata) of boundary_degree_mean vs the target on the 12-slot frame
(the H0 slot echoes H1 bit-exactly — the chain class's n=400 call
site, exp243's own disclosure, asserted; the house convention
carries both slots, exp278's ties-census precedent); the
single-predictor OLS rank R2 (the target enters as its tied-average
ranks, the field as the numeric design column); the all-ranks
variant (the field ranked too — single R2 == rho^2 within 1e-12)
AUDIT-ONLY; the ties census per vector.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY (the exp280 precedent): READ-ONLY
      sha-verified — the 12 rebuilt bases bit-asserted against
      exp243's records (sha256(|A| as float64) == rec["base_sha256"]
      12/12; the upper-triangle edge count == rec["edges_base"]
      12/12; the exp208 classify CANON-BOUNDARY count ==
      rec["n_boundary_cells_base"] 12/12, dual-carried vs exp272's
      per-host records + exp278's per-host table; labeling_bfs_n(
      |A|) == labeling_bfs_n(A) 12/12; H0 == H1 bit-exact);
      exp278's ratio identity bit-exact 12/12; the T1 mean identity
      bit-exact 12/12; the T3 4-way carry bit-exact 12/12 each; the
      outlier pre-name asserted (exp273 == exp272.descriptive.
      premium_hosts == exp276 == exp278 == exp279 == exp280 ==
      ['H3','H5']); the provenance chains sha-verified against the
      actual deposit bytes (exp280's recorded inputs 12/12, exp279's
      9/9, exp278's 11/11, exp276's 8/8, exp273's 5/5, exp272's
      4/4); READ-ONLY (the deposits sha-recorded before, byte-
      unchanged after).
  G2  THE FIELD DEFINITION BIT-IDENTICAL TO EXP280'S: the classify
      boundary masks nonempty 12/12; the recomputed
      boundary_degree_mean == exp280's deposited field-table values
      BIT-EXACT 12/12 (the boundary cells' own degree mean over the
      classify boundary set — exp280's code path, never re-fit);
      the field's distinct-level ties census recorded.
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      CHORD-CARRIED iff boundary_degree_mean reaches Spearman >=
      0.5 (the SIGNED house bar) against >= 1 of the three targets
      (T1 the premium level / T2 the amplification / T3 the audit
      error) — the mechanism line RE-OPENS at the chord level; else
      CHORD-ABSENT (it clears nothing — the line stands closed at
      mia and the premium's origin is formally OUTSIDE the deposited
      host records). THE ABS VARIANT, pre-named: a target crossing
      |rho| >= 0.5 with a NEGATIVE sign is the ANTI-ALIGNED face
      (the chord runs OPPOSITE the pre-named direction) — named in
      the deposit and the verdict per target, NEVER gating
      (exp280's precedent: the face named honestly, the SIGNED bar
      decides).
  G4  THE DISCIPLINE: deterministic — two-pass bit-identical; no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the deposits READ-ONLY sha-recorded byte-unchanged; the
      docstring+header pinned to this pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted
      at exit.

THE BRANCHES (pre-named): CHORD-CARRIED / CHORD-ABSENT.

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
OUT = os.path.join(ROOT, "results", "exp281_antialigned_face.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
