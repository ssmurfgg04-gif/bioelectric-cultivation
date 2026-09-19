#!/usr/bin/env python3
"""exp278 — THE AMPLIFICATION FACTOR (batch 36; batch-35's derived item,
ledger L255 — zero new simulation).

THE OPEN ITEM: exp277 closed the face question — the deep-band break is
CLASS-BLIND: the outliers' deep-band error carries the cluster-typical
class mixture, amplified ~7x (P3's own error H3 3.68 / H5 3.36 mV vs
the cluster's ~0.50-0.54). The amplification is itself the measurement:
per host, the deep-band substitution's cost stands against the
canon-space arms' cost on the SAME host x seed grid — exp256's
deposited 72 rows carry both faces. THE AMPLIFICATION RATIO per host =
the P3 arm's mean err / the P1+P2 arms' mean err (zero-knob: one
closed-form for all 12 hosts, no parameters). THE QUESTION: does the
per-host amplification track the audit error mia_prod_err (exp273's
external discriminator), or the canon-boundary count (exp255's
zero-knob instrument — exp272 refuted it for the PREMIUM level at
Spearman 0.0526 < 0.5; here it is tested for the AMPLIFICATION level)?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the numerator: the P3 arm's mean err = the mean over the 3
    substituted rows' deposited worst_err per host (the per-seed arm
    worst = the max over the two pre-named deep instances r-60i0/
    r-60i1 — exp255's/exp256's arm-worst convention; == exp276's
    m_P3 == exp277's mean_worst_err, bit-exact asserted).
  - THE DENOMINATOR'S DEFINITION (the gate, zero-knob): the P1+P2
    arms' mean err = the POOLED mean over the 6 canonical instance
    errs (P1_canon_zone_relabelings x 3 seeds +
    P2_boundary_double_frequency_rewiring x 3 seeds) — NOT the mean
    of the per-seed maxima (the deposited worst_err_mean_canonical
    IS the max variant; it is recorded alongside as audit-only and
    never enters the ratio; asserted in G2).
  - the regressors: mia_prod_err (exp273's deposited field table,
    exact field exp243.classes.multi_identity_audit.prod_err,
    selection external, bit-exact vs exp243's records) and the
    canon-boundary count (the exp255 instrument: exp243's classes
    records' n_boundary_cells_base — carried bit-exact from exp273's
    field table, cross-checked vs exp243's classes, exp272's
    per_host records, and exp255's deposited rows).
  - THE REGRESSIONS (the exp274/exp275 conventions verbatim): the
    response = the amplification ratio (12 hosts, tied-average
    ranks); two single-regressor Spearmans (regressor vector first,
    scipy rankdata both sides); the OLS-on-ranks single R2s (the
    response enters as its tied-average ranks, the regressor as its
    numeric values — exp262's/exp274's convention) + the full model
    (both regressors; with two regressors the pair IS the full
    model); the shares by the two-order symmetric average on the
    pre-named entry order mia -> bc and its reverse bc -> mia;
    shares + unexplained == 1 asserted (no clamping); the ties
    census; the all-ranks variant AUDIT-ONLY, never gating.
  - THE BRANCH (the discriminant pre-named, the bars numeric):
    MIA-SCALED iff Spearman(ratio, mia_prod_err) >= 0.5 (the house
    bar); else GEOMETRY-SCALED iff Spearman(ratio, boundary count)
    >= 0.5; else UNATTACHED (the exhaustive residual). The mia test
    is pre-named FIRST — the precedence is part of this
    registration; both rhos recorded regardless.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE GRIDS: exp256's 72 rows re-read COMPLETE — 12 hosts x 2
      arms x 3 seeds, every canonical row carrying exactly the two
      pre-named P1/P2 instances and every substituted row exactly the
      two pre-named deep instances r-60i0/r-60i1, each row's
      worst_err finite AND == the max of its instance errs (the
      deposited arm-worst convention, verified 72/72); the per-host
      means recomputed from the rows bit-exact vs EVERY deposited
      record where present — exp273's field table
      (worst_err_mean_substituted / _canonical / _all_arms),
      exp276's decomposition_table (m_P1 / m_P2 / m_P3), exp277's
      per_host_table (mean_worst_err), exp272's deposited records
      where present (per_host n_boundary_cells_base; both grids'
      canon_worst_err columns == exp256's canonical row worst_err
      36/36 each at the (host, seed) grain), exp243's classes
      records (multi_identity_audit.prod_err + n_boundary_cells_base),
      exp255's deposited rows (n_boundary_cells, 24 rows, each host
      single-valued); the outlier pre-name asserted (exp273's
      outliers == exp272's descriptive.premium_hosts == ['H3', 'H5']);
      the provenance chains sha-verified against the actual deposit
      bytes — exp273's recorded inputs 5/5, exp274's 6/6, exp275's
      7/7, exp276's 8/8, exp277's 8/8; READ-ONLY.
  G2  THE RATIO'S DEFINITION (zero-knob): one closed-form for all 12
      hosts — R_h = m_P3(h) / m_P12(h), m_P12 = the POOLED mean over
      the 6 canonical instance errs (identified by the deposited pert
      names, 3 seeds each), asserted computed from the instances and
      NOT from the per-seed maxima; the max variant (the mean of the
      canonical rows' worst_err) computed alongside, bit-exact vs
      exp273's deposited worst_err_mean_canonical, recorded
      audit-only — never entering the ratio; the pooled-vs-max gap
      recorded per host; all 12 ratios finite and > 0; the definition
      carries no parameters and no per-host cases (the ratio map
      carries exactly the 12 host keys, one formula).
  G3  THE BRANCH: the discriminant resolved on the pre-named numeric
      bars (MIA-SCALED / GEOMETRY-SCALED / UNATTACHED above; both
      rhos recorded); the regressions REPORTED alongside under the
      exp274/exp275 conventions — audit-only, never gating.
  G4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): MIA-SCALED / GEOMETRY-SCALED / UNATTACHED
(the exhaustive residual; the first two are the registered question's
named outcomes).

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
OUT = os.path.join(ROOT, "results", "exp278_amplification_factor.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")
