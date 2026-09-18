#!/usr/bin/env python3
"""exp258 — INTERIOR-CONTEXT BOUNDARY WRITE COUPLING (batch 22 item 3;
the FIRST channel activation under the exp257 schema — activates ch3
"ctx", the interior-context channel).

THE OPEN ITEM (exp229/exp245): ~0.686 of the boundary residual's rank
variance is unexplained by step or curvature; the four read-face
repairs (exp213 read-only boundary, exp216/exp219 context shells,
exp221 composed rules) all REFUTED — the boundary excess lives in the
channel truncation, not in the read face. The override's causal
prediction: a native interior-context channel, WRITTEN from the
boundary cell's local interior neighborhood during boundary write
passes, gives the boundary cell's write the context the truncation
destroyed — read-face changes failed because the context was never IN
the state to read.

THE MECHANISM (pre-registered, zero free parameters): during the
boundary write pass, each boundary cell's ctx channel is written with
the local interior context — the distance-weighted mean of the
interior neighbors' (theta - V) mismatch over the cell's junction
neighbors (the exp208 pair-geometry instrument's own neighborhood
definition; weights = the working conductances G_ij, normalized; no
new constants). During the write, the boundary cell's effective target
blends its chain-inherited identity with the ctx channel's read: the
blend is the pre-named ctx-gain dial g_ctx in {0, 0.25, 0.5, 1.0} —
g_ctx = 0 IS the bit-exact dormant default (the migration contract's
own face).

PRE-REGISTERED GATES:

  X1  THE DORMANT IDENTITY: g_ctx = 0 reproduces the exp257 schema's
      own battery bit-exactly (the activation's bit-exact gate — the
      dormant default is the legacy behavior).
  X2  THE COUPLING: at g_ctx > 0 the boundary rows' errs (the
      exp226/exp229 canon-boundary row class) DROP below the dormant
      baseline on the pre-named battery (exp226's c6 battery instances
      x 3 seeds) — worst boundary-row err reduction >= 10% at SOME
      pre-named g_ctx (the grid is the test, not a fit: report all
      four g_ctx values, the gate reads the best cell of the grid,
      zero post-hoc tuning).
  X3  THE SPECIFICITY: the interior rows' errs are NOT degraded at the
      same g_ctx (the coupling targets the boundary; non-interference
      on the interior) — worst interior-row err change <= +5%.
  X4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the -60.0 floor restored and
      asserted; deterministic re-run.

THE BRANCHES (pre-named): X2 PASS -> CONTEXT-CARRIED (the truncation
diagnosis CONFIRMED causally — the boundary excess was the missing
channel); X2 REFUTE -> CONTEXT-INERT (the interior context in the
state does not close the boundary — the ~70% structure has another
carrier, deposited honestly).

RUN: exp226's c6 battery x 4 g_ctx values x 3 seeds (12 battery runs +
the dormant identity re-runs); runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp258_interior_context_coupling.json")


def main() -> dict:
    raise NotImplementedError(
        "exp258 body pending — pre-registration commit only")
