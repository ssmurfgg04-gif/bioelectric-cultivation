#!/usr/bin/env python3
"""exp266 — THE LAW'S STRUCTURAL TERM (batch 25 item 2; L242's
registered next (b) — the exp251/exp253 aggregation line's honest
close; zero new simulation).

THE OPEN ITEM: the two-channel law's response-domain form needs a
STRUCTURAL term (L231: three aggregation forms, one monotone rank
ordering 0.936 -> 0.955 -> 0.960, the boundary pinned at 24). The
batteries since named the structural candidates: the arm indicator
(the substitution, exp262's 0.757 share) and the host boundary count
(exp255's rho_canon 0.857). exp265 tests the target-geometry
decomposition of the arm share; exp266 closes the LAW line: the
response form err ~ f(two-channel pred, arm indicator, host boundary
count) evaluated on the deposited battery, the rank the structural
terms reach vs the pre-named 0.90 bar and the boundary pin.

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): on
exp256's 72 deposited rows (worst errs + the row records), the OLS
rank regression (tied average ranks, the exp229 convention):

  M0  the baseline: the two-channel law's pred alone (exp232's S3
      battery carried the law at 0.620 pooled — the pred values for
      these rows come from the same formula run_gm-side; where the
      deposit carries no per-row pred, the law term is the battery's
      own op-level prediction: gamma=64, mu=0 -> the pre-named
      star-point prediction recorded in exp232's deposit);
  M1  M0 + the arm indicator (0/1);
  M2  M1 + the host boundary count (exp243's classes records);
  M3  M2 + the interaction (arm x boundary count).

The gates read the RANK (Spearman between the full-model fitted
ranks and the observed worst-err ranks) and the BOUNDARY (the
model's own boundary prediction — predicted-err >= 24 vs the
observed boundary pin — the agreement rate).

PRE-REGISTERED GATES:

  W1  THE REPRODUCTION: exp256's 72 rows complete, finite,
      sha-verified; exp243's classes records byte-unchanged.
  W2  THE RANK LADDER: the ranks reported for M0..M3; the gate:
      M3's rank >= 0.90 (the structural terms close the law's rank
      gap — the response form is complete at the battery's level).
  W3  THE BOUNDARY: M3's boundary agreement >= the exp251 pop-RMS
      form's 21/27 (the structural terms do not regress the
      boundary face).
  W4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded;
      deterministic; no wall-clock fields; the -60.0 floor
      asserted at exit.

THE BRANCHES (pre-named): W2 PASS -> LAW-STRUCTURALLY-CLOSED (the
response form is complete at the battery level — the residual's rank
gap was the missing structural terms, the boundary face carries the
rest); W2 REFUTE -> LAW-OPEN (the rank gap survives the structural
terms — the form needs the read's own response surface, deposited
honestly).

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
OUT = os.path.join(ROOT, "results", "exp266_law_structural_term.json")


def main() -> dict:
    raise NotImplementedError(
        "exp266 body pending — pre-registration commit only")
