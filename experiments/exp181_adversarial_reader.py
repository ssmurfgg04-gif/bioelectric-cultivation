#!/usr/bin/env python3
"""exp181 — UNIVERSAL READER: ADVERSARIAL MEDIA (path 1's closer).

Stage 5 path 1 (the handoff ledger's ~85%): exp160's 200 RANDOM media
decode with ZERO rejections (median 0.630 mV); the adversarial class
is untested at scale. The corner cells, the flip battery, and the
grouping pairs were all decoded in this session's experiments — but
never as a UNIVERSAL-READER battery. THIS EXPERIMENT runs 200
STRUCTURED adversarial media through the production read.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Cohort, read, and gates are fixed now.

THE COHORT (200 structured adversarial media, zero fitting):
  exp166's CornerMedium generator at the four ADVERSARIAL cells —
  c = 3 (h+t), c = 5 (o+t), c = 6 (o+h), c = 7 (o+h+t) — 50
  instances each, seed = 166166 + 1000*c + j, j = 0..49, n = 100
  (exp166's construction VERBATIM; its main batteries used the same
  cells at n=100). This is the class the random-media sweep only
  samples in the tail: every medium carries at least two ACTIVE
  violation dimensions by construction.

THE READ (production, exactly as deposited):
  exp160's READ_CONFIG VERBATIM (fingerprint 8e11e88c1c2f1518
  asserted at run time) with the ONE adoption from L157: the
  temporal dispatch is exp178's SCOPED arm (the diagnostic clause,
  zero knobs) — the production read this session installed. Seeds
  (1, 2, 3). -35.0 instrument pin for comparability with the
  deposited random-media records (exp160's 200 ran pre-CF-1).

GATES (each evaluated exactly once):

  GATE-U1 (zero rejections — the universal claim) 600 decodes
           (200 media x 3 seeds): zero rejections, all errs finite,
           verify recorded per decode.
  GATE-U2 (the adversarial median at the deposited bar) the pooled
           adversarial median <= 1.30 mV (exp160's U2 bar = 2.0x
           the OOD anchor 0.65); the per-cell medians deposited;
           the random-media comparison (0.630) recorded as context,
           NOT a bar (adversarial media are ALLOWED to be harder —
           the bar is the U2 ceiling).
  GATE-U3 (the tail is corner-owned, characterized) the above-bar
           instances (err > 1.30) tabulated per cell with their
           violation classes; the deposit names which cell owns the
           tail; no bar on the tail SIZE (characterization gate).
  GATE-U4 (the scoped arm's discipline holds) per-cell f_max
           classifications deposited; wherever the diagnostic
           selects the raw path (f_max >= 32), the decode is the
           temporal arm's (recorded); zero cross-arm anomalies.

NO post-hoc tuning. A --smoke check (cell 3, j = 0, seeds (1,)) is
permitted before the credited run and discarded.

DEPOSIT: results/exp181_adversarial_reader.json

RUN:
  python3 -m experiments.exp181_adversarial_reader            # full
  python3 -m experiments.exp181_adversarial_reader --smoke    # check
  python3 -m experiments.exp181_adversarial_reader --cell 3
  # jobs: c3 | c5 | c6 | c7
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
)
from experiments.exp160_any_medium import (  # noqa: E402
    BAR, OOD_ANCHOR, READ_CONFIG, config_fingerprint,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP160_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP160_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


ADVERSARIAL_CELLS = [3, 5, 6, 7]     # h+t, o+t, o+h, o+h+t
PER_CELL = 50
SEEDS = (1, 2, 3)

OUT = os.path.join(ROOT, "results", "exp181_adversarial_reader.json")
DEP160 = os.path.join(ROOT, "results", "exp160_any_medium.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cell", type=int, choices=ADVERSARIAL_CELLS,
                    default=None)
    ap.add_argument("--job", choices=["c3", "c5", "c6", "c7", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--cell/--job/--out)
