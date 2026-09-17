#!/usr/bin/env python3
"""exp172 — DEEP-BAND INVENTION SWEEP (the widened repertoire's frontier).

exp168's registered next (L146): "the widened floor makes deep-zone
writes FIRST-CLASS (the search's own deep voltage band down to -60 is
now fully readable — the class the old floor effectively refused at
decode is writable, so a deep-band invention sweep prices the widened
repertoire's own frontier)". CF-1 (NEURAL_SPEC_MIN -35 -> -60, L146)
made the compiler's full repertoire [-60, -15] (exp141's WIDE_LO/HI =
REPERTOIRE_LO/HI, compiler/anatomy.py) readable at decode: before,
any committed spec below -35 fell back to canon at exp136.decode's
adoption branch; now it adopts. THIS EXPERIMENT prices the newly
readable band directly.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Ladder, bars, and gates are fixed now.

THE DESIGN:
  * Target patterns: piecewise-constant zone patterns f on n=100
    engines, built by exp94's spec_target_n machinery (MULTI zones,
    labeling_bfs_n) with the zone values forced to the rung ladder —
    DEEP rungs {-40.0, -45.0, -50.0, -55.0, -60.0} (5 rungs x 10
    instances) and SHALLOW controls {-20.0, -25.0, -30.0} (3 rungs x
    10 instances); seeds (1, 2, 3) per (rung, instance) — the same
    3-seed protocol as exp168's B2/B3.
  * THE TWO ARMS (the audit IS the design, exp168's mechanism):
      PATCHED — the working tree's CF-1 floor (-60.0): decode adopts.
      PINNED  — OLD_FLOOR_PIN rebinding the ONE constant to -35.0
                (save/restore asserted) in the modules that captured
                it at import time: the pre-CF-1 engine.
  * Readout: exp136's decode VERBATIM (the consumer CF-1 targets) —
    e_decode = pattern_error(f) after the adoption walk, then the
    stability hold; errs at 2-dp precision, replay comparisons exact.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-D1 (shallow audit) SHALLOW controls: patched errs == pinned
           errs BIT-EXACTLY per (rung, instance, seed) — 90/90
           records (float equality). The adoption branch consumed
           one normal draw on EITHER side pre-patch (adopted or
           canon), so the rng streams align; any mismatch is an
           instrument bug, not a finding.
  GATE-D2 (the deep regime is live) DEEP rungs: pinned err >
           patched err on >= 80% of (rung, instance, seed) records;
           the pinned arm's errs sit at the canon-refusal scale
           (deposited: err_pinned vs err(canon projection of f),
           the "write did not take" reference, recorded per rung).
  GATE-D3 (the frontier price) the patched err profile vs depth
           deposited per rung; the frontier rung NAMED = the deepest
           rung whose median decode err <= 6.0 AND median hold err
           <= 6.0 (the production ERR_BAR, exp150's C3 clause) on
           the 3-seed medians. PASS iff at least one deep rung
           reaches the bar (the widened repertoire's frontier is
           real); the named rung is the deposit either way.
  GATE-D4 (hygiene) zero rejections; all errs finite; the pin's
           save/restore asserted between arms; the shallow arm run
           FIRST so any pin leakage fails D1 loudly.

NO post-hoc knob tuning; the ladder is fixed above. A --smoke
instrument check (rungs -40 and -20, instance 0, seed 1) is permitted
before the credited run and discarded; the credited full run uses the
committed script unchanged.

DEPOSIT: results/exp172_deep_band_sweep.json

RUN:
  python3 -m experiments.exp172_deep_band_sweep            # full
  python3 -m experiments.exp172_deep_band_sweep --smoke    # check
  python3 -m experiments.exp172_deep_band_sweep --rung -50.0
  # jobs: shallow | d40 | d45 | d50 | d55 | d60
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

from experiments.exp136_generator_v6 import (  # noqa: E402
    decode as exp136_decode,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
DEEP_RUNGS = [-40.0, -45.0, -50.0, -55.0, -60.0]
SHALLOW_RUNGS = [-20.0, -25.0, -30.0]
N_INST = 10
SEEDS = (1, 2, 3)
ERR_BAR = 6.0                   # exp150's production bar
OLD_FLOOR = -35.0
NEW_FLOOR = -60.0

OUT = os.path.join(ROOT, "results", "exp172_deep_band_sweep.json")


class OldFloorPin:
    """exp168's OLD_FLOOR_PIN mechanism, verbatim semantics."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


def run_rung(rung: float, instance: int, seed: int, arm: str) -> dict:
    """One (rung, instance, seed) record. Body written by the run
    agent (gates fixed above)."""
    raise NotImplementedError


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["shallow", "d40", "d45", "d50",
                                      "d55", "d60", "all"],
                    default="all")
    ap.add_argument("--rung", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--rung/--out)
