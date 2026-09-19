#!/usr/bin/env python3
"""exp276 — THE AUDIT'S OWN FACE (batch 34; batch-33's derived next
item — zero new simulation).

THE OPEN ITEM: exp275 named mia_prod_err the one-zone premium's
proximate carrier (MIA-UPSTREAM); exp273 named H3/H5 the outliers at
mia_prod_err 2.12/2.28 vs the ten-host cluster's [0.49, 0.52]. What
makes the audit's own read high on exactly those two hosts? The audit
IS a battery member: exp243's multi_identity_audit.prod_err is the
MULTI-target production read on the base medium (seed 1), and the
adversarial battery that surrounds it has three pre-named arms — P1
(the canon row on the mirrored medium), P2 (the canon row on the
boundary-double medium), P3 (the deep-band substitution: the base
medium read at the deep rows r-60i0/r-60i1). Decompose each host's
audit error across the arms' own battery errors and read where the
outliers' audit error lives: in ONE perturbation arm, or spread
uniformly?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the 12-host table from exp243's deposit: the audit error
    a_h = classes.<H>.multi_identity_audit.prod_err (12 values; the
    runtime_s field EXCLUDED by the no-wall-clock discipline); the
    per-arm masses from the candidates records' errs: P1 =
    P1_canon_zone_relabelings (the mirror-medium canon row), P2 =
    P2_boundary_double_frequency_rewiring (the boundary-double-medium
    canon row), P3 = P3_deep_band_substitution (BOTH pre-named deep
    rows r-60i0/r-60i1); each arm's per-seed WORST = its row's err at
    the seed (P1/P2, one row each) / the max over the two P3 rows
    (exp255's/exp256's arm-worst convention); each arm's mass =
    the mean of its per-seed worsts over the 3 seeds.
  - the cross-check: the per-arm per-seed worsts derived from
    exp243's candidates == exp256's deposited rows' worst_err (the
    canonical rows max(P1,P2), the substituted rows max(i0,i1)),
    72/72 bit-exact — exp256's rows are the same battery re-deposited.
  - THE DECOMPOSITION (the accounting identity): per host, the arm
    shares s_k = m_k / (m_P1 + m_P2 + m_P3) (sum(s) == 1 asserted,
    tolerance 1e-9); the audit error's per-arm contributions
    c_k = s_k * a_h — the arms' contributions SUM TO THE AUDIT ERROR
    (sum_k c_k == a_h asserted within 1e-9, 12/12 hosts; the max
    |residual| recorded).
  - THE BRANCH (the discriminant pre-named, the bars numeric): the
    outliers = exp273's deposited outliers (asserted ==
    exp272's descriptive.premium_hosts == ['H3', 'H5']); the dominant
    arm = argmax_k s_k; the outlier concentration = the min over the
    two outliers of the dominant share. ARM-CONCENTRATED iff both
    outliers' dominant arm is the SAME arm AND the concentration
    >= 0.60 (the supermajority bar — one arm carries >= 60% of the
    battery mass on BOTH outliers); UNIFORM otherwise. The cluster's
    per-host dominant shares reported alongside, never gating.
  - THE RANK REGRESSION (the exp274 convention VERBATIM): the
    response = the audit error a_h (12 hosts); the three mediators =
    the per-arm contributions (c_P1, c_P2, c_P3); the three
    single-mediator Spearmans (tied-average ranks, mediator vector
    first, exp272's _spearman); the OLS-on-ranks full model R2 (the
    response enters as its tied-average ranks, the mediators as the
    numeric contribution values — exp262's/exp274's convention) plus
    the three pairs; the shares by the two-order symmetric average on
    the pre-named entry order P1 -> P2 -> P3 and its reverse
    P3 -> P2 -> P1; shares + unexplained == 1 asserted (no clamping);
    the all-ranks variant AUDIT-ONLY, never gated.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  B1  THE GRIDS: the candidates grid complete — 48 records = 12 hosts
      x 4 (P1, P2, P3 x 2), each with 3 finite errs, zero rejections;
      the audit records complete 12/12 (prod_err finite,
      bit_identical true); the arm-worst cross-check vs exp256's
      deposited rows 72/72 bit-exact; exp273's field-table carry of
      mia_prod_err bit-exact vs the exp243 records; the outlier
      pre-name asserted (exp273's outliers == exp272's
      descriptive.premium_hosts == ['H3', 'H5']); the provenance
      chains sha-verified against the actual deposit bytes — exp273's
      recorded inputs 5/5, exp274's 6/6, exp275's 7/7; READ-ONLY.
  B2  THE IDENTITY: per host, sum(s_k) == 1 AND sum_k c_k == a_h
      within 1e-9, 12/12 hosts; all shares and contributions finite.
  B3  THE BRANCH: the discriminant resolved on the pre-named bars
      (the concentration >= 0.60 supermajority + the same dominant
      arm on both outliers -> ARM-CONCENTRATED; else UNIFORM).
  B4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): ARM-CONCENTRATED / UNIFORM.

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
OUT = os.path.join(ROOT, "results", "exp276_audit_own_face.json")


def main() -> dict:
    raise NotImplementedError(
        "exp276 body lands under the pre-registration commit")
