#!/usr/bin/env python3
"""exp273 — THE OUTLIER HOSTS (batch 31; L250's registered next (a) —
zero new simulation).

THE OPEN ITEM (L250): the rewrite premium's shelf price is a
host-fixed property outside the boundary geometry (H2 refuted), and
the host structure is TWO OUTLIERS against a tight cluster: H3/H5
carry 1.95/2.10 one-zone and 3.51/3.17 multi-zone premiums vs the
ten-host cluster's 0.34-0.49/0.33-0.49. What distinguishes H3/H5?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
discriminant search across the deposited host records — for every
host-level field in the deposits (exp243's classes records: rewire
seed, edges_base, n_boundary_cells_base, f_max_base; exp256's
per-host row records; exp182's margin profiles; exp241's margin
data where present), compute the field for all 12 hosts and test
the pre-named separation: the field value separates {H3, H5} from
the other ten hosts iff the two outliers' values both sit outside
the ten-host cluster's [min, max] range ON THE SAME SIDE. Every
candidate field is reported; the gate reads the COUNT of separating
fields.

PRE-REGISTERED GATES:

  X1  THE GRIDS: the 12-host field table assembled from the
      deposits (every field provenance-tagged); exp271's/exp272's
      premium grids byte-verified.
  X2  THE SEPARATION: at least ONE deposited field separates {H3,
      H5} from the ten-host cluster on the same side (the gate) —
      the count and the fields named; ZERO separating fields ->
      OUTLIER-DEPOSIT-ABSENT (the discriminator lives outside the
      deposited records — a new instrument required, named
      honestly).
  X3  THE HONESTY CLAUSE: fields that separate ONE outlier but not
      the other are reported as one-sided (never counted as
      separating).
  X4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged; deterministic; no wall-clock fields; the
      -60.0 floor asserted at exit.

THE BRANCHES (pre-named): OUTLIER-DEPOSIT-CARRIED (X2 passes) /
OUTLIER-DEPOSIT-ABSENT.

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
OUT = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")


def main() -> dict:
    raise NotImplementedError(
        "exp273 body pending — pre-registration commit only")
