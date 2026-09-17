#!/usr/bin/env python3
"""exp180 — THE SCALE ANATOMY (the n=400 residual, mechanism first).

exp177's registered next (L156): the grid residual above N3's 0.60
bar is a SCALE effect (dominant channel c2_n, pooled rho +0.6984;
n=400 instances at +1.10/+1.11 vs 0.00-0.16 at n=100) and no rule in
exp166's RULE_MAP maps the scale dimension. Before any repair: the
mechanism. The read's own instruments at n=400 are decomposed on a
FRESH instance set (the deposited grid carries only 2 n=400 media).

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Instances, features, candidate, and
gates are fixed now; the credited run uses this file unchanged.

THE FRESH SET (zero fitting): 12 fresh n=400 FlipGridMedium
instances — GRID_BASE_SEED + 1000 + i for i = 0..11, 6 per schedule
class (GRID_CLASSES order fixed), T from T_GRID as exp148's grid
protocol — built and decoded under the SCOPED arm (exp178's
production dispatch, the L157 adoption; -35.0 instrument pin for
replay comparability with exp169's deposit).

THE ANATOMY FEATURES (per instance, from the medium and the read's
intermediates — all computable, none fitted):
  (a1) BFS label coverage: exp94's labeling_bfs_n label-order reach
       (the fraction of nodes whose label is assigned within the
       first half of the BFS order) at n=400 vs the same statistic
       recomputed on the deposited n=100 instances;
  (a2) the projection's per-frame support coverage (|sup| / n);
  (a3) the read's eV/eT split (exp160's decomposition) at n=400 vs
       n=100 — WHICH quadrature carries the scale residual;
  (a4) support density and asymmetry (exp177's c5/c6, recomputed);
  (a5) the walk frontier's size at commit (the executor's R1
       structure footprint).
  Deliverable: the Spearman table of each feature vs the residual
  r_i (scoped_err_i - 0.60) over the 12 fresh + 2 deposited n=400
  instances, PLUS the n=100 reference distribution (the deposited 16
  + fresh 12 at n=100, GRID_BASE_SEED + 2000 + i) — the mechanism is
  NAMED by which feature tracks the residual at scale and collapses
  at n=100.

THE CANDIDATE (ONE, disclosed, priced not adopted): the label-order
arm — the read re-run at n=400 with exp94's labeling_bfs_n computed
on the TRANSPOSED adjacency (the reverse BFS order; zero new
parameters, the same function). Both orders' medians deposited; the
delta named. If the reverse order's median lands <= 0.60 + (the
n=100 pooled median's excess over 0.60) = 0.68, the candidate is
REGISTERED for the adoption path (not adopted here).

GATES (each evaluated exactly once):

  GATE-T1 (fresh-set integrity) all 24 fresh instances (12 at
           n=400, 12 at n=100) build with the deposited protocol
           fields, decode with zero rejections, and the 12 fresh
           n=100 instances' scoped errs fall inside the deposited
           n=100 residual range of exp169's S4 (the reference
           distribution replicates).
  GATE-T2 (the anatomy is complete) every feature computed for
           every instance, finite; the Spearman table deposited at
           both scales; the eV/eT split deposited per instance.
  GATE-T3 (the mechanism clause) EXACTLY ONE of: (i) a feature
           tracks the residual at n=400 (|rho| >= 0.5) AND
           collapses at n=100 (|rho| < 0.3) — the mechanism named;
           (ii) no feature separates the scales — the residual is
           declared a GENERIC size effect and the read's n-scaling
           is registered as its own instrument question. Both
           branches complete the gate.
  GATE-T4 (the candidate price) both label orders at n=400:
           medians + per-instance deltas deposited, zero
           rejections; the registration clause evaluated against
           the 0.68 line and recorded.

NO post-hoc tuning. A --smoke check (1 fresh instance per scale,
features only) is permitted before the credited run and discarded.

DEPOSIT: results/exp180_scale_anatomy.json

RUN:
  python3 -m experiments.exp180_scale_anatomy            # full
  python3 -m experiments.exp180_scale_anatomy --smoke    # check
  python3 -m experiments.exp180_scale_anatomy --job T2
  # jobs: build | anatomy | candidate
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from experiments.exp148_temporal_read import (  # noqa: E402
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, T_GRID,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    labeling_bfs_n,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP169_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP169_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


FRESH_400 = [GRID_BASE_SEED + 1000 + i for i in range(12)]
FRESH_100 = [GRID_BASE_SEED + 2000 + i for i in range(12)]
RHO_SCALE = 0.5
RHO_REF = 0.3
REGISTRATION_LINE = 0.68

OUT = os.path.join(ROOT, "results", "exp180_scale_anatomy.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")
DEP177 = os.path.join(ROOT, "results", "exp177_grid_residual.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "anatomy", "candidate",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
