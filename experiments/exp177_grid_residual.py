#!/usr/bin/env python3
"""exp177 — THE GRID RESIDUAL DECOMPOSITION (what R_T cannot reach).

exp169's registered next (L148 (ii)): the schedule grid classifies
ALL-DIFFUSE at T=32, so the scoped read is exp167's adopted read
everywhere on the grid and the pooled median stands at 0.68 mV —
N3's 0.60 bar is never reached by R_T there. "The temporal channel's
remaining excess is NOT flip-clock: price it." THIS EXPERIMENT
decomposes the grid's residual.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Channels, decomposition, and gates are
fixed now; the credited run uses this file unchanged.

THE RESIDUAL (defined once): per grid instance i (exp148's schedule
grid, 20 instances = 8 x n=100 + 2 x n=400 per class x 2 classes...
the deposited instance set of exp169's S4), residual
  r_i = scoped_err_i - N3_BAR (0.60),
where scoped_err_i = the instance's median decode err under the
scoped read (exp169's deposited per-instance records — replayed
bit-exactly first, then decomposed; NO new decodes for the replay).

THE CHANNEL CENSUS (zero knobs, pre-registered channel list): per
instance, the structural features computable from the medium ALONE:
  (c1) schedule class (per | aper) — one-hot;
  (c2) n (100 | 400);
  (c3) T (the window length, T_GRID);
  (c4) flip mass m_i = total presence transitions across the window;
  (c5) support size |sup_i| and its DENSITY (edges / n^2);
  (c6) support ASYMMETRY a_i = ||sup - sup^T||_0 / |sup|_0 (the
       oriented dimension's footprint — exp160's A-SYM class);
  (c7) the frame-diversity d_i = mean pairwise Jaccard distance
       between frame supports (temporal dimension's footprint).
  THE DECOMPOSITION: Spearman rank correlation of each feature with
  r_i across the instance set, deposited per class and pooled; the
  DOMINANT channel = the feature with the largest |rho| at
  |rho| >= 0.5 (a pre-named threshold, not a fit); if no feature
  reaches 0.5, the residual is declared UNATTRIBUTED at this census
  and the deposit says so (that is a completed answer, not a
  failure — it registers the next instrument).

CANDIDATE REPAIR (priced ONLY IF a dominant channel fires, zero
  knobs): the mapped rule from exp166's RULE_MAP for the dominant
  feature's dimension (asymmetry -> R_O one-way restore; density ->
  R_H cancellation-weighted S; frame-diversity -> R_T is already
  active, so frame-diversity dominance registers the gap instead of
  pricing a rule). The mapped rule runs on the instances in the
  dominant feature's TOP TERcile (the pre-registered slice), spot
  scale (3 seeds), and the delta median deposited. No adoption
  claim — pricing only.

INSTRUMENTS (zero new calibration):
  * exp148's module verbatim (the grid constructors, T_GRID,
    GRID_CLASSES, GRID_BASE_SEED, N_INSTANCES, N_INSTANCES_400);
  * exp169's deposit results/exp169_rt_scoping.json (the per-
    instance scoped records — the replay source);
  * the -35.0 instrument pin (exp167's mechanism) for any decode;
  * seeds (1, 2, 3) for the candidate-repair spot runs.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-R1 (replay) the grid scoped errs replay exp169's S4 records
           bit-exactly (per instance, per seed) — the decomposition
           runs on the deposited errs, zero new decodes for this
           gate.
  GATE-R2 (the census is complete) all seven features computed for
           all instances, no NaN, the Spearman table deposited per
           class and pooled (the table IS the deliverable).
  GATE-R3 (the verdict clause) a dominant channel is NAMED at
           |rho| >= 0.5, OR the residual is deposited UNATTRIBUTED
           at this census. Both branches complete the gate; the
           branch taken is the finding.
  GATE-R4 (hygiene) zero rejections in any decode performed; pin
           save/restore asserted.

NO post-hoc knob tuning; the census is fixed. A --smoke check (1
instance per class, features only) is permitted before the credited
run and discarded.

DEPOSIT: results/exp177_grid_residual.json

RUN:
  python3 -m experiments.exp177_grid_residual            # full
  python3 -m experiments.exp177_grid_residual --smoke    # check
  python3 -m experiments.exp177_grid_residual --job census
  # jobs: replay | census | repair
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
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N_INSTANCES,
    N_INSTANCES_400, T_GRID,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
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


RHO_BAR = 0.5                   # the pre-named dominance threshold
OUT = os.path.join(ROOT, "results", "exp177_grid_residual.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["replay", "census", "repair",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
