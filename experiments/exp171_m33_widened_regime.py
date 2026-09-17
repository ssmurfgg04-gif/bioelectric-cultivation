#!/usr/bin/env python3
"""exp171 — M33'S NEW [-60, -35) REGIME (first exercise + audit).

exp168's registered next (L146): "the M33 gate's new [-60, -35) regime
(collective.py:366/584) is unexercised by any deposited experiment —
its first use should carry its own bit-exact-at-old-operating-points
audit". CF-1 widened NEURAL_SPEC_MIN from -35.0 to -60.0 for the
S-REL spec-adoption floor; the SAME constant gates the core's M33
non-junctional neural/muscle polarity readout (neural_readout > 0.0,
junction blockade r < 1.0, spec[i] >= NEURAL_SPEC_MIN). No deposited
experiment has ever set neural_readout > 0 — this is the FIRST.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Arms, weights, and gates are fixed now.

WHAT CHANGED SEMANTICALLY (named before the run): M33's comment fixes
the old line at "the fate-axis midpoint between the WT head identity
(-20 mV) and the WT trunk/tail identity (-50 mV)" — i.e. -35.0 was the
ANTERIOR/POSTERIOR literature line (posterior identities have no local
pole; recorded GJ-blockade phenotypes concentrate at posterior planes,
innexin|tail 0.67 vs innexin|head 0.00). The widened floor RECLASSIFIES
every identity in [-60, -35) — including the -50 trunk/tail identity —
as ANTERIOR-ELIGIBLE for the pole readout. This may be exactly right
(deeper anterior identities exist) or exactly wrong (the trunk plane's
junction-carried phenomenology is the literature asymmetry M33
encodes). The experiment does not presuppose either: it prices the
reclassification and deposits the asymmetry ratio.

INSTRUMENTS (zero new calibration):
  * The core engine VERBATIM: the M33 branch at collective.py:582
    (`neural_w > 0.0 and spec is not None and 0 <= i < n and
    float(spec[i]) >= NEURAL_SPEC_MIN`), the constructor's
    neural_readout / neural_misanchor parameters (line 199), and the
    junction-blockade coupling parameter that drives r < 1.0 (the
    guess branch's precondition; read from the engine's constructor —
    M33 is inert at full coupling r >= 1.0 and at neural_w = 0).
  * Substrates: four identity families, values from the WT/literature
    ladder — HEAD -20.0, LINE -35.0 (the old boundary), TRUNK -50.0,
    DEEP -60.0 — as uniform per-plane spec identities on n=100
    engines, seeds (1, 2, 3) per family.
  * THE TWO ARMS (the audit IS the design):
      PATCHED — the working tree's CF-1 floor NEURAL_SPEC_MIN = -60.0.
      PINNED  — exp168's OLD_FLOOR_PIN mechanism rebinding the ONE
                constant to -35.0 (save/restore asserted) in every
                module that captured it at import time.
    neural_w = 0.5 (pre-registered, the blend midpoint — zero
    fitting), one blockade setting (the engine's default reduced-
    coupling configuration, recorded in the deposit), no other knobs.
  * The sweep ladder over neural_w is FORBIDDEN (one weight only).

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-M1 (bit-exact audit above the old line) HEAD/LINE families
           (identities >= -35.0): patched vs pinned are BIT-IDENTICAL
           per (family, seed) — final V, committed phi_spec, and the
           guess stream at the blocked plane (float equality). The
           patch must be invisible where it was already active.
  GATE-M2 (the new regime is live) TRUNK/DEEP families (identities
           in [-60, -35)): patched differs from pinned under the
           same settings — qualifying-cell count > 0 (cells whose
           spec >= -60 and < -35 that now take the pole branch);
           the FIRST divergent step reproduces the M33 blend exactly:
           guess_patched = (1 - w) * guess_base + w * (spec + draw)
           with guess_base and draw taken from the pinned arm's
           shared stream (the divergence point is the branch itself).
  GATE-M3 (the asymmetry price — the literature clause) the head/tail
           blockade asymmetry under the pole readout:
             A(arm) = | mean_err(TRUNK planes, arm) -
                       mean_err(HEAD planes, arm) |
           where err = |guess - spec| at the blocked plane, pooled
           over seeds. Deposited: A_pinned, A_patched, and the ratio
           A_patched / A_pinned. The gate RECORDS the ratio with two
           pre-named verdict branches (no post-hoc reading):
             (a) ratio >= 0.5 — the asymmetry SURVIVES the widened
                 floor; CF-1 stands as ONE constant (the pole readout
                 is identity-anchored, not line-anchored, at this
                 weight).
             (b) ratio < 0.5 — the asymmetry COLLAPSES toward the
                 patched floor's eligibility; the split is REGISTERED
                 (M33 needs its own anterior line, distinct from the
                 S-REL adoption floor) as the experiment's registered
                 next.
           Either branch is a completed deposit; the gate passes on
           the RECORD being complete, not on which branch fires.
  GATE-M4 (inertia + hygiene) neural_readout = 0.0 runs: patched ==
           pinned bit-identically on ALL four families (the inert-at-
           default clause, whole-sweep); pin save/restore asserted;
           zero non-finite values anywhere.

NO post-hoc knob tuning; exactly ONE neural_w. A --smoke instrument
check (HEAD + TRUNK families, seed 1 only) is permitted before the
credited run and discarded; the credited full run uses the committed
script unchanged.

DEPOSIT: results/exp171_m33_widened_regime.json

RUN:
  python3 -m experiments.exp171_m33_widened_regime           # full
  python3 -m experiments.exp171_m33_widened_regime --smoke   # check
  python3 -m experiments.exp171_m33_widened_regime --family TRUNK
  # jobs: HEAD | LINE | TRUNK | DEEP | inertia
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

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}
NEURAL_W = 0.5                 # the ONE weight, pre-registered
N_CELLS = 100
SEEDS = (1, 2, 3)
OLD_FLOOR = -35.0              # exp168's pre-patch value
NEW_FLOOR = -60.0              # exp168's CF-1 value (the working tree)
ASYM_RATIO_SPLIT = 0.5         # the pre-named verdict branch point

OUT = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")


class OldFloorPin:
    """exp168's OLD_FLOOR_PIN mechanism, verbatim semantics."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


def run_engine(spec_val: float, seed: int, neural_w: float):
    """Build the n=100 plane engine, run under blockade, return the
    record. Body written by the run agent (gates fixed above)."""
    raise NotImplementedError


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["HEAD", "LINE", "TRUNK", "DEEP",
                                      "inertia", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
