#!/usr/bin/env python3
"""exp275 — THE AUDIT'S DIRECTION (batch 33; L252's registered next
(a) — zero new simulation).

THE OPEN ITEM (L252): the one-zone rewrite premium's carrier IS
mia_prod_err (Spearman 0.8905, share 0.5634 — exp274). Is the
hosts' multi-identity audit error mechanistically UPSTREAM of the
premium, or are premium and audit error parallel faces of one
deeper host defect? mia's own conditioning proposes the test: if
mia is the proximate carrier, the premium's OTHER correlates (the
boundary count, the pair deficit) carry no premium rank variance
once mia is held fixed; if the two are downstream of the same
defect, the geometry survives mia's conditioning.

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
exp229 partial-correlation form VERBATIM — the standard
partial-rank identity on the tied-average Spearman rhos (scipy
rankdata both sides, exp272's _spearman convention;
partial(Y,X|Z) = (rho_YX - rho_YZ*rho_XZ) /
sqrt((1-rho_YZ^2)(1-rho_XZ^2))) — on the 12-host table (the
one-zone premium means from exp272's deposit as the response; the
three mediators from exp273's deposited field table by exact
field name; the multi-zone premium means from exp272's deposit).
Three partials pre-named:
  (i)   partial(one-zone premium, n_boundary_cells_base |
        mia_prod_err)
  (ii)  partial(one-zone premium, pair deficit | mia_prod_err)
        [the canonical pair-junction mean — LOWER is the deficit
        side]
  (iii) partial(one-zone premium, multi-zone premium |
        mia_prod_err) — the depth-offset re-read: does exp272's
        rho 0.9912 shelf-to-shelf identity survive mia's
        conditioning?

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  A1  THE GRIDS: the 12-host table complete (5 columns, finite):
      the one-zone AND multi-zone premium means re-derived from
      exp272's deposited 36-row grids bit-exact (sum/3, the
      arithmetic recompute clean); exp273's field-table carry of
      the means bit-exact; the duplicate boundary-count carrier
      identical to the exp243 record; exp273's provenance chain
      sha-verified 5/5 AND exp274's recorded input shas 6/6
      against the actual deposit bytes; READ-ONLY.
  A2  THE FORM: the three partials computed by the exp229
      identity, each finite (the identity's denominator > 0); the
      anchors reproduce bit-exact: the three unconditioned
      Spearmans against the one-zone premium == exp274's
      deposited m2 spearman_rho values, the unconditioned shelf
      rho == exp272's deposited H3 spearman_rho (0.9912).
  A3  THE BRANCH (the discriminant pre-named, the bars numeric):
      a geometric partial COLLAPSES iff |partial| < 0.5, SURVIVES
      iff |partial| >= 0.5 (the house bar). MIA-UPSTREAM = both
      (i) and (ii) collapse — mia absorbs everything the geometry
      set can see, the audit error is the proximate carrier.
      MIA-COLLINEAR = both survive — the geometry carries premium
      variance beyond mia: same defect, parallel faces. MIXED =
      exactly one survives. The shelf re-read (iii) is reported
      at its pre-named 0.9 bar — SHELF-SURVIVES (>= 0.9: the
      depth-offset identity is mia-independent) / SHELF-ABSORBED
      (< 0.9) — alongside the branch, NEVER read by it.
  A4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): MIA-UPSTREAM / MIA-COLLINEAR / MIXED
(A3's bars read the two geometric partials (i) and (ii) only;
(iii) is reported, never gating).

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
OUT = os.path.join(ROOT, "results", "exp275_audit_direction.json")


def main() -> dict:
    raise NotImplementedError(
        "exp275 body pending — pre-registration commit only")
