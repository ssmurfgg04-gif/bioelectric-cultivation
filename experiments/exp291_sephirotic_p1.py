#!/usr/bin/env python3
"""exp291 — THE P1 SEPHIROTIC TEST: THE RECORD'S OWN ARITHMETIC
REPRODUCED LOCALLY AND THE 8-MODE MAPPING RECONCILED AGAINST THE
STACK'S 8-CHANNEL SCHEMA (batch 47; ledger L267's registered next
(d) — the search wave (S-3, research/2026-09-20_sephirotic_compiler.md)
fetched Zenodo 19042388's own deposits: research/sephirotic/
paper25_results.json (the record's results: 8 internal modes at
indices [0,1,2,4,5,7,8,9], channels_mapped 8, knockout_confirmed 7 +
knockout_partial 1, lambda_6 1.2, lambda_distance 0.0, the spatial
spectrum [0.9077855614887613, 1.2, 1.5422144385112373], the internal
spectrum 8 values, null_lambda_hits 3011 / null_total 100000 /
p_null 0.00039) + paper25_computation.py (the record's own code,
19,367 bytes) + paper25.pdf. The pre-registered P1 test — named in
the ledger's standing frontiers since the Sephirotic deposit — is
now UNBLOCKED: the record's deterministic arithmetic reproduces
locally, and the record's 8-mode spec reconciles against exp257's
8-channel native schema.)

THE TWO READS (zero new simulation; the record's own code run as-is):

  R1  THE LOCAL REPRODUCTION (the deterministic face): run the
      record's own paper25_computation.py (imported or subprocess'd
      AS-IS — no edits; the file byte-sha recorded in the deposit)
      and assert its deterministic outputs reproduce the deposited
      paper25_results.json: lambda_6 == 1.2 EXACTLY, the spatial
      spectrum 3/3 bit-exact (within 1e-12 — the floats are the
      record's own serialization), the internal spectrum 8/8 within
      1e-12, the indices [3,6,10] / [0,1,2,4,5,7,8,9] exact, the
      graph identity "Paper 24 canonical (5 principles, 24 edges)"
      exact. The STOCHASTIC face (the 100,000-draw null) is NOT
      re-run — the deposit's p_null 3.9e-4 is recorded as deposited,
      disclosed (the null's seed is the record's own; the
      deterministic spectrum is the reproduction target).
  R2  THE MAPPING RECONCILIATION: the record's 8 internal modes
      against exp257's 8-channel native schema (the Sephirotic
      spec's own mapping — Zenodo 19042388 defines the 8 modes;
      exp257 named the stack's channels from the same spec):
      Vmem-bistability, GJ-morphogenesis, Ca2+, Vmem-propagation,
      epigenetic-proliferation, ion-channel-expression, 5-HT,
      apoptosis. Per channel the stack's honest state from the
      ledger (zero new runs): CONFIRMED (a landed causal test)
      {Vmem-bistability, GJ-morphogenesis, Vmem-propagation},
      PARTIAL (dynamics ported, the association below the bar)
      {Ca2+ — exp261 CA2-INERT, association 0.1738 < 0.5, the port
      clean}, INERT (schema-only, no dynamics) {ctx-form
      epigenetic-proliferation (exp258 CONTEXT-INERT), pair-form
      ion-channel-expression (exp259/260 COMPENSATION/STRUCTURE-
      INERT), 5-HT (exp263 SHT-INERT), apoptosis (exp264 APOP-INERT
      with inversion)}. The trichotomy counts 3 / 1 / 4 recorded
      against the record's own 7 confirmed + 1 partial (the record's
      knockout test is IN-SILICO on the record's model; the stack's
      tests are the ledger's causal record — the two scorecards are
      RECONCILED, not equated, disclosed).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE DEPOSIT INTEGRITY: research/sephirotic/paper25_results.json
      + paper25_computation.py + paper25.pdf exist, byte-sha recorded
      before and after (READ-ONLY); the results JSON parses; the
      pre-named fields present (the 12 named above).
  G2  THE LOCAL REPRODUCTION (R1): the record's own computation run
      as-is reproduces the deterministic face (the bars above);
      fail=STOP on any drift — the record's own arithmetic is the
      anchor.
  G3  THE MAPPING RECONCILIATION (R2): the 8-channel mapping
      recorded per channel with the ledger citation (the L-numbers);
      the trichotomy counts 3/1/4 recorded; the branch pre-named:
      P1-ALIGNED iff G2 passes AND the mapping is total (8/8 —
      every stack channel carries a record mode and every record
      mode carries a stack channel, the exp257 naming) / P1-DRIFTED
      otherwise.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the core NOT imported (this module
      touches no stack state — the floor discipline N/A, disclosed).

THE BRANCHES (pre-named): P1-ALIGNED / P1-DRIFTED.

RUN: seconds (the record's own computation + the reconciliation
table). One pass, foreground.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp291_sephirotic_p1.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp291's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
