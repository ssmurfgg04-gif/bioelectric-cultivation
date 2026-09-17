#!/usr/bin/env python3
"""exp185 — THE N-SCALING LADDER (the read's size law).

exp180's registered next (L159): the grid residual above N3's 0.60
bar is a GENERIC size effect at the deposited census — the read's
n-scaling is its own instrument question. THIS EXPERIMENT runs the
ladder: n = 100 / 200 / 300 / 400 / 500, 10 fresh instances per rung
(5 per schedule class), the scoped production arm, the residual-vs-n
curve and the coverage features per rung.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Ladder, curves, and gates are fixed now.

THE LADDER: FlipGridMedium(n, seed = GRID_BASE_SEED + 5000 + 100*rung_idx
+ i) for rung_idx 0..4 (n = 100/200/300/400/500), i = 0..9, classes
alternating by i parity (GRID_CLASSES order flip_per/flip_aper);
decode via exp178's scoped arm under the -35.0 pin, seeds (1, 2, 3),
per-instance median err; features: support coverage, density, BFS
reach (exp180's computable set), f_max.

GATES (each evaluated exactly once):
  GATE-Y1 (ladder integrity) 50 instances built and decoded, zero
           rejections, all errs finite; the n=100 rung's median
           within [0.55, 0.80] (the deposited n=100 scale).
  GATE-Y2 (the curve) the residual-vs-n curve (per-rung pooled
           medians) deposited with per-rung dispersions; the curve
           shape NAMED by pre-named branches: (i) MONOTONE rising
           (each rung's median > the previous, n=500 > n=100) — a
           scaling law to name; (ii) SATURATING (n >= 300 rungs'
           medians within 0.05 of each other) — a finite-size
           plateau; (iii) NON-MONOTONE otherwise — deposited as-is.
           All three branches complete the gate.
  GATE-Y3 (the features track) per-feature Spearman vs residual on
           the pooled 50, deposited; the n=100-vs-n=500 feature
           shift table (the mechanism side-data).
  GATE-Y4 (hygiene) pin save/restore asserted; zero cross-rung
           anomalies; the n=100 rung replays exp169's S4 scale
           (pooled median within the deposited grid band).

NO post-hoc tuning. --smoke (1 instance at n=100 and n=500)
permitted, discarded. Deposit: results/exp185_n_scaling.json
Jobs: rung0..rung4
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
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N3_BAR,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
)

import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP169_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}

LADDER_N = [100, 200, 300, 400, 500]
PER_RUNG = 10
SEEDS = (1, 2, 3)
SATURATION_TOL = 0.05

OUT = os.path.join(ROOT, "results", "exp185_n_scaling.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP169_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["rung0", "rung1", "rung2",
                                      "rung3", "rung4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
