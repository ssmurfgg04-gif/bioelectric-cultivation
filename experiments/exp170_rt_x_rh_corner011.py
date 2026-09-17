#!/usr/bin/env python3
"""exp170 — R_T x R_H CROSS-CHECK ON THE 011 CELL (L145's follow-up).

exp145's registered next (via L147): "R_T x R_H cross-check on the 011
corner cell (L145's registered follow-up)" — the h+t cell (o=0, h=1,
t=1, cell index c = 4o+2h+t = 3) where exp166's above-bar tail lives
(9/50 main-battery instances above the 1.30 bar; cell median 0.820 mV
vs clean 0.670). exp166's P4 spot battery ran the single-rule mapping
ONLY (temporal -> R_T on the 111 corner and clean cells). The composed
rule on the 011 cell is untested. THIS EXPERIMENT runs it.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Arms, composition order, and gates are
fixed now; the credited run uses this file unchanged.

THE TWO RULES (both zero-knob, both deposited):
  R_T = exp166's rule_temporal_core VERBATIM (L140's flip-quiet
        discipline at the medium level: mask every frame to the
        across-frame core support; membership frozen).
  R_H = exp166's rule_hyper_S VERBATIM (L142's deposit at the medium
        level: A += F * S with S = co-hyperedge adjacency, F = the
        pre-decode pooled median nonzero |W| — pooled_F over the spot
        instances, computed BEFORE any decode).

THE COMPOSITION — the two rules act on DIFFERENT channels (R_T on the
  frame support/temporal channel, R_H on the projection's augmentation
  via hyperedge co-membership) and compose NON-trivially. Order is
  fixed by the data flow and named BEFORE the run:
    PRIMARY (mask-then-augment): frames' = R_T(frames); then the read
      computes A = project(frames') and A_ext = A + F' * S where F' =
      pooled median nonzero |W| of the MASKED frames (R_H's F computed
      on the masked frames — the augmentation reads the window it
      will decode) and S = the medium's co-hyperedge adjacency.
    REVERSED (augment-then-mask): frames'' = R_H(frames) i.e. each
      frame Wt + F * S with F = pooled |W| of the RAW frames; then
      R_T masks the augmented frames. Recorded arm, not primary.
  Both orders are zero-knob compositions of the two deposited rules;
  no third rule, no interpolation, no tuning.

INSTRUMENTS (zero new calibration):
  * exp166's module verbatim: CornerMedium (SEED_BASE 166166),
    rule_hyper_S, rule_temporal_core, pooled_F, the exp160 read stack
    via exp166's own dispatch, cell_dims.
  * THE PIN (exp167's mechanism, disclosed pre-run): exp166's deposit
    predates CF-1, so NEURAL_SPEC_MIN is pinned to -35.0 in every
    module whose bound name the read chain consults
    (cultivation.bioelectric.collective, exp142, exp145, exp148,
    exp94) — save/restore asserted; exp166's arm-A/B records were
    produced at that floor.
  * Deposit read at run time: results/exp166_leading_edge.json (the
    011 cell's main-battery stats: median, above-bar count).
  * Spot set: CornerMedium(n=100, seed = 166166 + 1000*3 + j),
    j = 0..9 (cell c=3, the 011 h+t cell), seeds (1, 2, 3) — 30
    decodes per arm, exp166's spot protocol verbatim.

ARMS (each exactly once, same 30 decodes):
  A0 raw          — exp160's stack verbatim, no rule.
  A1 R_T alone    — rule_temporal_core on the frames.
  A2 R_H alone    — rule_hyper_S on the frames (F from raw pooled |W|).
  A3 COMPOSED     — mask-then-augment (PRIMARY, defined above).
  A4 reversed     — augment-then-mask (recorded).

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-C1 (raw replay + tail presence) A0: zero rejections, all errs
           finite; the 30 raw errs deposited with per-instance
           medians; >= 5/10 spot instances' medians above exp160's
           deposited pooled median 0.630 (the cell is a tail cell —
           if the spot set fails to reproduce tail character, the
           construction is flagged and everything else deposited
           honestly with the construction caveat).
  GATE-C2 (single-rule prices) A1 and A2 medians and per-instance
           deltas vs A0 deposited; no pass bar — this gate PRICES the
           two channels separately so the composition's effect is
           attributable (record = pass always, values are the
           deposit).
  GATE-C3 (the composed rule) A3 vs A0: median(A3) < median(A0)
           AND >= 8/10 spot instances improved (per-instance median
           A3 < A0) AND median(A3) <= 0.60 mV (exp160's clean-cell
           parity bar — the L145-style "lands at clean scale"
           clause). Partial outcomes deposited honestly (median
           improvement without the parity bar = 2/3 clauses).
  GATE-C4 (order sensitivity + hygiene) A4 median deposited; the
           sign of median(A4) - median(A3) recorded (no bar);
           zero rejections across all five arms; the pin save/
           restore asserted in the deposit.

NO post-hoc knob tuning anywhere; exactly ONE composed rule is
primary. A --smoke instrument check (j = 0 only, seeds (1,)) is
permitted before the credited run and discarded; the credited full
run uses the committed script unchanged.

DEPOSIT: results/exp170_rt_x_rh_corner011.json

RUN:
  python3 -m experiments.exp170_rt_x_rh_corner011              # full
  python3 -m experiments.exp170_rt_x_rh_corner011 --smoke      # check
  python3 -m experiments.exp170_rt_x_rh_corner011 --arm A3     # split
  # arms: A0 | A1 | A2 | A3 | A4
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

from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE,
    pooled_F, rule_hyper_S, rule_temporal_core,
)

# ---- INSTRUMENT PIN (see docstring) --------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP166_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP166_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


# ---- FIXED CONSTANTS ------------------------------------------------
CELL_011 = 3                                   # c = 4o + 2h + t = 3
SPOT_J = list(range(10))
SPOT_SEEDS = (1, 2, 3)
CLEAN_PARITY_BAR = 0.60                        # exp160's pooled median
IMPROVED_MIN = 8                               # of 10 instances

OUT = os.path.join(ROOT, "results", "exp170_rt_x_rh_corner011.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")


def frames_of(med: CornerMedium) -> list[np.ndarray]:
    return [Wt.copy() for Wt in med.snapshots()]


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--arm", choices=["A0", "A1", "A2", "A3", "A4",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--arm/--out)
