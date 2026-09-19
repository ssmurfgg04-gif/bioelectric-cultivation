#!/usr/bin/env python3
"""exp279 — THE AUDIT ERROR'S ORIGIN (batch 37; batch-36's derived next
item, ledger L256 — zero new simulation).

THE OPEN ITEM: exp273 named H3/H5 the outliers at mia_prod_err 2.12/
2.28 vs the ten-host cluster's [0.49, 0.52] — the ~4x. exp276
decomposed the battery's error MASS (94% P3 on the outliers) but never
asked the numeric question this module asks: what makes the AUDIT err
when the single-target reads err ~equal? The audit IS a battery
member — exp243's multi_identity_audit.prod_err is the MULTI-target
production read on the base medium (seed 1) — and the battery around
it has three pre-named single-target arms (P1 the canon row on the
mirrored medium, P2 the canon row on the boundary-double medium, P3
the deep-band substitution rows r-60i0/r-60i1). Per host, compare the
audit's prod_err against the battery's own per-arm errs: (a) is the
audit error the MAX of the battery errs (the multi-target aggregation
re-reads the worst arm and adds nothing beyond it), (b) does it
EXCEED any single arm (a SUM-style aggregation — the audit's
simultaneous multi-target read costs MORE than any single-target
read: the interference face), or (c) is it independent of the battery
errs (the audit's own construction)?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the 12-host table from exp243's deposit: the audit error
    a_h = classes.<H>.multi_identity_audit.prod_err (12 values; the
    records read AS DEPOSITED — see G2); the battery's per-arm errs
    from the candidates records: P1/P2 one row each x 3 seed errs,
    P3 the two pre-named deep rows r-60i0/r-60i1 x 3 seed errs.
  - THE GATING GRAIN (the audit's own operating point): the audit
    record is the seed-1 read (the deposited seed == 1 asserted
    12/12), so the battery's per-arm SEED-1 errs: p1 = P1.errs[0],
    p2 = P2.errs[0], p3 = max(P3 i0.errs[0], P3 i1.errs[0])
    (exp255's/exp256's arm-worst convention); max_arm_err(h) =
    max(p1, p2, p3); the argmax arm named (ties to the FIRST arm in
    the pre-named order P1 -> P2 -> P3). The grain is MATCHED — the
    audit's err and the arms' errs at the SAME seed, zero grain
    mixing.
  - THE ROBUSTNESS GRAIN (audit-only, never gating): exp276's arm
    masses m_P1/m_P2/m_P3 (the mean over the 3 seeds of the per-seed
    arm worsts), recomputed from exp243's candidates and cross-
    checked BIT-EXACT vs exp276's deposited decomposition_table
    12 x 3; max_mass(h) = max of the three masses.
  - THE DECOMPOSITION (per host, both grains): the gap = a_h -
    max_arm; the excess ratio = a_h / max_arm; the per-host class,
    the precedence FIXED: MAX-host iff |a_h - max_arm| <= 0.10 * a_h
    (the 10% bar); else EXCESS-host iff a_h > 1.1 * max_arm (the
    1.1x bar); else INDEPENDENT-host (fails both bars — DISCLOSED:
    this class includes the below-worst face a_h < 0.9 * max_arm,
    the audit erring LESS than the worst single-target arm).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE GRIDS: integrity READ-ONLY sha-verified — the candidates
      grid complete (48 records = 12 hosts x 4: P1, P2, P3 x 2; 3
      finite errs each; zero rejections; verified all-True); the
      audit records complete 12/12 (prod_err finite, bit_identical
      True, seed == 1); the P3 arm's two pre-named deep rows exactly
      r-60i0/r-60i1 on every host; exp256's 72 rows re-read complete
      (12 hosts x 2 arms x 3 seeds) with every row's worst_err == the
      max of its instance errs AND bit-exact vs the arm worsts
      derived from exp243's candidates; exp273's field-table carry of
      mia_prod_err bit-exact vs the exp243 audit records 12/12; the
      outlier pre-name asserted (exp273's outliers == exp272's
      descriptive.premium_hosts == ['H3', 'H5']); the provenance
      chains sha-verified against the actual deposit bytes —
      exp276's recorded inputs 8/8, exp273's recorded inputs 5/5;
      READ-ONLY (the deposits sha-recorded before, byte-unchanged
      after).
  G2  THE IDENTITY: the aggregation form asserted AS THE DATA DEFINES
      IT — the 12 audit records enumerated; a record carrying
      per-target component fields would be verified
      sum(components) == prod_err within 1e-9; the deposited records
      carry NONE (asserted 12/12: the key set is exactly {seed,
      bit_identical, prod_err, f_max}) — the record is ATOMIC as
      deposited, the identity clause VACUOUS-AS-DEPOSITED, the audit
      error read as deposited and NEVER repaired or reconstructed
      (the aggregation form is inferred only through G3's
      discriminant); the battery's own aggregation identities
      asserted where the data defines them: the deposited worst_err
      == max(errs) 48/48 candidates and 72/72 exp256 rows; the
      recomputed masses == exp276's deposited masses bit-exact
      12 x 3.
  G3  THE BRANCH: the discriminant pre-named with the numeric bars,
      the precedence fixed, evaluated on the GATING grain:
      AUDIT-MAX iff the MAX-hosts >= 10 of 12; else AUDIT-EXCESS iff
      the EXCESS-hosts >= 10 of 12; else AUDIT-INDEPENDENT. The
      per-host table (both grains' gaps, ratios, argmax arms,
      classes) recorded regardless; the robustness grain's
      classification recorded audit-only, never gating.
  G4  THE DISCIPLINE: deterministic — two-pass bit-identical; no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the deposits READ-ONLY sha-recorded byte-unchanged; the
      docstring+header pinned to this pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted
      at exit.

THE BRANCHES (pre-named): AUDIT-MAX / AUDIT-EXCESS / AUDIT-INDEPENDENT.

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
OUT = os.path.join(ROOT, "results", "exp279_audit_error_origin.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
