#!/usr/bin/env python3
"""exp283 — THE EARLY-COMMIT FACE: exp282's AUDIT-ONLY LEAD PROMOTED TO
A GATE (batch 41; ledger L260's registered next (a) — zero new
simulation, a pure re-read, seconds).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED (the walk's end RMS
the strongest carrier yet named: walk_end_rms~mia +0.8826 /
~premium +0.8807, the SIGNED house bar) — but its audit-only lead is
the CONVERGENCE POINT (TA3 conv_step): the cluster's per-step RMS
curve first falls below 2x its final value only at the walk's very
END (~289/292 steps) while the outliers H3/H5 cross EARLIER
(219.67/239.17 mean steps) — the outlier walks commit into their
wrong pattern early. TWO QUESTIONS, pre-registered:
  (Q1) Is the early-commit property CATEGORICAL — a GAP between the
       cluster's ~289/292 and the outliers' 220/239 — not a
       continuum?
  (Q2) Does the early-commit summary (TA3 conv_step) predict the
       premium (exp272's per-host means) and mia (exp273's field
       table) BETTER than the end RMS (TA1 walk_end_rms, exp282's
       own strongest)?

THE INSTRUMENT (pre-registered, zero-knob): a PURE RE-READ of three
deposits — exp282's trajectory deposit (its 72 per-row traces, the
three per-row summaries, the 12-host means table, the six deposited
regressions), exp272's per-host one-zone premium means, exp273's
field table (the mia field 'exp243.classes.multi_identity_audit.
prod_err'). NO new simulation, NO rebuild, NO re-run: every number
recomputed from the deposited bytes; seconds, foreground.

  (Q1) THE ZERO-KNOB TESTS: the 12-host conv_step means' ORDERING
       (recorded in full, ascending; the PRE-NAMED ASSERTION — the
       two outliers H3/H5 hold the TWO SMALLEST conv_step means);
       the GAP RATIO = the cluster min / the outlier max (the
       pre-named form); the PRE-NAMED CATEGORICAL BAR: the gap ratio
       >= 1.2 (fixed from ledger L260's disclosed rounding ~289/239;
       the exact deposit re-read decides). Outcome: CATEGORICAL-GAP /
       CONTINUUM-GAP, recorded; the per-row conv_step values
       audit-only.
  (Q2) THE SIGNED-BAR COMPARISON, under the exp274/exp275/exp282
       conventions VERBATIM (Spearman = Pearson on the tied-average
       ranks, scipy rankdata; the 12-slot frame, the H0==H1 echo
       carried; the ties census per vector): the EARLY-COMMIT
       ORIENTATION PRE-NAMED — earliness = -conv_step_mean per host
       (exp282's disclosed face runs NEGATIVE, conv_step~mia -0.3432
       / ~premium -0.1565: the lead's direction is earliness WITH the
       exposure; the orientation is fixed HERE at pre-registration,
       never fit) — so the CARRY bar is e_t = Spearman(earliness,
       target) >= 0.5 (the SIGNED house bar) on >= 1 of the two
       targets (T_mia, T_prem). The STRICT-POSITIVE reading
       (conv_step as-deposited reaching >= +0.5) recorded audit-only.
       THE COMPARISON per target (audit-only, never gating):
       EARLY-COMMIT-DOMINATES iff |e_t| > |rho_end,t| where
       rho_end,t = walk_end_rms~target (exp282's own strongest),
       else END-RMS-DOMINATES. The six exp282 rhos recomputed from
       the re-read and asserted BIT-EXACT vs exp282's deposited
       regressions 6/6. The single-predictor rank R2s audit-only.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE GRIDS' INTEGRITY (READ-ONLY sha-verified): the three source
      deposits (exp282, exp272, exp273) sha-recorded BEFORE any
      parse, byte-unchanged after the work; THE PROVENANCE CHAINS
      sha-verified — every input sha recorded inside exp282 (4),
      exp273 (5), exp272 (4) asserted against the CURRENT file bytes
      (hashing only, never parsed); the host frame asserted 3-way
      (exp272's per_host order == exp273's hosts == exp282's hosts,
      12 unique); the outlier pre-name asserted ['H3','H5'] 3-way
      (exp273.outliers == exp272.descriptive.premium_hosts ==
      exp282.outliers) and the ten-host complement == exp282.cluster;
      the carries BIT-EXACT: mia (exp273's field-table field) ==
      exp282's targets.mia_prod_err.values 12/12; the premium
      (exp272's per_host one_zone_premium_mean) == exp273's
      field-table carry 'exp272.per_host.one_zone_premium_mean' ==
      exp282's targets.one_zone_premium.values (12/12 x 2); AND
      EXP282'S TRACES COMPLETE PER ROW (the deposit's internal
      integrity, re-derived bit-exact): 72/72 rows with
      len(trace) == walk_steps >= 1, every entry finite, final > 0,
      the convergence point existing (0 <= conv_step < walk_steps);
      trace_sha256 recomputed == deposited 72/72; the THREE
      SUMMARIES re-derived from the deposited traces BIT-EXACT 72/72
      each (walk_end_rms == trace[-1]; last10_slope == the
      least-squares slope over the last W = max(2, ceil(0.10*S))
      entries, numpy.polyfit degree 1 — exp282's exact form;
      conv_step == the first index strictly below 2x final); the
      per-host means recomputed == exp282's host_table BIT-EXACT
      12/12 x 3 summaries; the S0 anchor carried (err ==
      err_deposited 72/72, as exp282 landed it); the six deposited
      rhos reproduced BIT-EXACT 6/6.
  G2  THE CATEGORICAL BAR (pre-named): the 12-host conv_step means'
      ordering evaluated exactly as pre-named (the two-smallest
      assertion is HARD — a violation REFUTES the gate); the gap
      ratio computed in the pre-named form (cluster min / outlier
      max); the bar >= 1.2 applied exactly as pre-named; the outcome
      (CATEGORICAL-GAP / CONTINUUM-GAP) recorded in the deposit and
      the verdict.
  G3  THE BRANCH DISCRIMINANT (numeric, pre-named): EARLY-COMMIT-
      CATEGORICAL iff the gap holds (the gap ratio >= 1.2) AND the
      carry holds (max over the two targets of e_t >= 0.5, the
      SIGNED house bar in the pre-named early-commit orientation);
      else CONTINUUM, with the failed component(s) NAMED (the gap /
      the carry / both). The strict-positive reading, the per-target
      comparison vs the end RMS, and the R2s recorded audit-only,
      never gating.
  G4  THE DISCIPLINE: deterministic — the full re-read +
      recomputation executes TWICE, the two passes' payloads
      BIT-IDENTICAL; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring + header pinned to this
      pre-registration commit, asserted at entry AND exit; the
      source deposits byte-unchanged; NEURAL_SPEC_MIN == -60.0
      asserted at exit (the floor restored post-import — exp218's
      disclosed discipline).

THE BRANCHES (pre-named): EARLY-COMMIT-CATEGORICAL / CONTINUUM.

RUN: a pure re-read of three deposits + rank arithmetic; seconds,
foreground, two passes (G4). No checkpoint-split (nothing heavy).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp283_early_commit_face.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
