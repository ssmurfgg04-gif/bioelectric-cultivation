#!/usr/bin/env python3
"""exp259 — PAIR-CELL GEOMETRY COMPENSATION (batch 22 item 4; the SECOND
channel activation under the exp257 schema — activates ch2 "gj", the
per-cell gap-junction state).

THE OPEN ITEM (exp254/exp255): the deep-band substitution re-wires the
pair-junction structure and the reader's price follows it (pair share
70.1% -> 83.5%, the substituted medium's pair cells' RMS err 3.706 vs
the rest's 3.520); the cost decouples from the host-level boundary
geometry (rho 0.137) and lives at the ROW level (exp256's test). The
compensation: local junction-weight re-scaling targeted specifically
at the substituted pair cells.

THE MECHANISM (pre-registered, zero free parameters): the per-cell gj
channel (ch2) carries each cell's junction-weight multiplier; the
compensation pass renormalizes each PAIR-JUNCTION cell's multiplier so
the cell's effective pair-participation (sum of working conductances
to its pair-junction neighbors) matches the CANONICAL medium's mean
pair-participation over its own pair cells (the canonical-match rule —
the canonical medium is the target of record, no new constants; the
non-pair cells' multipliers stay 1.0; the total conductance
conservation is asserted: the compensation redistributes, it does not
amplify — sum(G) post == sum(G) pre within 1e-9).

PRE-REGISTERED GATES:

  P1  THE DORMANT IDENTITY: gj at defaults (all multipliers 1.0)
      reproduces the exp257 schema's own battery bit-exactly.
  P2  THE COMPENSATION: applying the canonical-match renormalization
      to the substituted medium's pair cells REDUCES the reader's
      worst err on the substituted rows (exp243's 12 candidate hosts x
      the P3 medium x 3 seeds) — pooled worst-err reduction >= 10%
      (the pre-named bar; all rows reported, zero post-hoc selection).
  P3  THE SPECIFICITY / NON-INTERFERENCE: the SAME compensation
      applied to the canonical media does NOT degrade them (worst-err
      change <= +5% on the P1/P2 rows) — the lever is specific to the
      substitution's pair re-wiring.
  P4  THE DISCIPLINE: exp243's/exp254's deposits READ-ONLY
      sha-recorded byte-unchanged; conductance conservation asserted;
      the -60.0 floor restored and asserted; deterministic re-run.

THE BRANCHES (pre-named): P2 PASS -> PAIR-COMPENSATED (the pair
geometry's causal face lands — the row-level driver is compensated at
its own scale); P2 REFUTE -> COMPENSATION-INERT (the pair re-wiring is
not the row-level driver's lever, deposited honestly).

RUN: 12 hosts x 2 media x 3 seeds x {on, off} (48 scoped reads) + the
dormant identity battery; runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp259_pair_geometry_compensation.json")


def main() -> dict:
    raise NotImplementedError(
        "exp259 body pending — pre-registration commit only")
