#!/usr/bin/env python3
"""exp277 — THE DEEP-BAND BREAK FACE (batch 35; batch-34's derived next
item (a), ledger L254 — zero new simulation).

THE OPEN ITEM: exp276 closed the mechanism line at the deposits'
bottom — the outlier hosts' audit error is 94% P3 deep-band-space
(ARM-CONCENTRATED), and exp273 named H3/H5 the boundary-richest hosts
(47/48 canon-boundary cells vs the ten-host cluster's [4, 43]). WHY do
the deep-band programs break on exactly the boundary-richest hosts?
exp256's deposited rows carry the answer's raw material: each row (the
WORST instance per host x arm x seed) is decomposed by exp208's
cell-class machinery into CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR
with frac_of_sq and rms_contrib_mV. Decompose the P3 arm's OWN error
per host and read the face: is the outlier hosts' deep-band error
boundary-class (the CANON-BOUNDARY share) or pair-class (the
PAIR-JUNCTION share)?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the source: exp256's deposited 72 rows = 12 hosts x 2 arms
    (canonical, substituted) x 3 seeds; the SUBSTITUTED arm (P3's own
    face: the deep rows r-60i0/r-60i1 on the base medium) is the 36
    rows read here (12 hosts x 3 seeds); each row's decomposition =
    exp208's classify(T_row, W_row) + decompose on the row's WORST
    instance's own state-carrying read (exp243's A3 path), deposited
    as per_class with frac_of_sq / sum_sq / rms_contrib_mV.
  - THE MASK SEMANTICS (disclosed, read AS DEPOSITED): exp208's
    classify assigns cls 1 = PAIR-JUNCTION and 0 = otherwise (the
    boundary ring wins precedence; the interior cells ride the 0
    mask — cls is never set to 2), so the deposited per_class
    CANON-BOUNDARY record is the NON-PAIR-JUNCTION complement of the
    squared error (boundary ring + interior) and the deposited
    INTERIOR record is empty. Verified here in-deposit 72/72
    (per_class PAIR-JUNCTION n_cells == class_counts PAIR-JUNCTION;
    per_class INTERIOR n_cells == 0; per_class CANON-BOUNDARY
    n_cells == 400 - that count; class_counts sum to n = 400). The
    branch therefore reads the deposited labels at face value:
    "boundary-class" == the non-pair-junction share, "pair-class" ==
    the PAIR-JUNCTION share. (The pure boundary-only share is NOT
    recoverable from the deposits — the decomposition's frac does not
    split the complement; disclosed, never repaired, zero new
    simulation.)
  - the 12-host table: per-host mean CANON-BOUNDARY frac and mean
    PAIR-JUNCTION frac over the substituted rows (3 seeds each),
    alongside the mean worst_err (the P3 arm's own error, exp276's
    m_P3), the mean rms_contrib_mV, and the mean pair-junction count.
  - THE BRANCH (the discriminant pre-named, the bars numeric): the
    outliers = exp273's deposited outliers (asserted == exp272's
    descriptive.premium_hosts == ['H3', 'H5']); the cluster = exp273's
    other ten. BOUNDARY-CLASS iff min(cb share on H3, H5) > max(cb
    share over the cluster); PAIR-CLASS iff min(pj share on H3, H5) >
    max(pj share over the cluster); SPLIT iff both exceed; NEITHER
    (the exhaustive residual) otherwise. Both margins recorded.
  - THE PREMIUM'S MEDIATOR (the exp274/exp275 conventions, REPORTED
    not gated): the response = mia_prod_err (exp273's deposited field
    table, exact field exp243.classes.multi_identity_audit.prod_err,
    carried bit-exact vs exp243's records); the two mediators = the
    two per-host mean shares; the single-mediator Spearmans
    (tied-average ranks, mediator vector first, exp272's _spearman);
    the OLS-on-ranks single R2s + the full-model R2 (the response
    enters as its tied-average ranks, the mediators as the numeric
    mean shares — exp262's/exp274's convention) plus the pair; the
    shares by the two-order symmetric average on the pre-named entry
    order cb -> pj and its reverse pj -> cb; shares + unexplained == 1
    asserted (no clamping); the ties census; the all-ranks variant
    AUDIT-ONLY, never gating.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  D1  THE GRIDS: exp256's 72 rows re-read COMPLETE — 12 hosts x 2
      arms x 3 seeds, every row's decomposition carrying the three
      pre-named per_class records with finite frac_of_sq / sum_sq /
      rms_contrib_mV; the mask semantics verified in-deposit (72/72
      as disclosed above); the 36 substituted rows complete 12 x 3;
      all worst_err finite; the outlier pre-name asserted (exp273's
      outliers == exp272's descriptive.premium_hosts == ['H3', 'H5']);
      exp273's field-table mia_prod_err carry bit-exact vs exp243's
      records; the provenance chains sha-verified against the actual
      deposit bytes — exp273's recorded inputs 5/5, exp274's 6/6,
      exp275's 7/7; READ-ONLY.
  D2  THE ACCOUNTING IDENTITY (per row, all 72): the per-class
      frac_of_sq sums to 1 within 1e-9 (72/72); the deposited
      identity_residual <= 1e-9 (72/72); the RMS-reconstruction face:
      |sqrt(sum_k sum_sq_k / 400) - worst_err| <= 0.0051 in every row
      (worst_err is exp256's 2-decimal rounding — the 0.005 bound +
      margin; the max deviation recorded).
  D3  THE BRANCH: the discriminant resolved on the pre-named numeric
      bars (the min-over-outliers vs max-over-cluster comparisons;
      both margins recorded); the mediator rank regression REPORTED
      alongside under the exp274 conventions — audit-only, never
      gating.
  D4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): BOUNDARY-CLASS / PAIR-CLASS / SPLIT /
NEITHER (the exhaustive residual; the first three are the registered
question's named outcomes).

RUN: a deposit re-read + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp277_deep_band_break_face.json")


def main() -> dict:
    raise NotImplementedError(
        "exp277 body lands under the pre-registration commit")
