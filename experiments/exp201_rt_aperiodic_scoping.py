#!/usr/bin/env python3
"""exp201 — R_T APERIODIC SCOPING (L147's registered next).

exp167 adopted R_T (flip-quiet core-support windowing) for
time-varying media; exp169 scoped it by the f_max diagnostic
(THRESHOLD 32.0, pair-joint for paired constructions) and exp178
landed the scoped arm in production. The registered open edge: R_T's
scoping on APERIODIC media — presence schedules with no periodic
flip clock, the class the 32.0 threshold has never been asked to
classify.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp169's f_max_frames
VERBATIM with the DEPOSITED THRESHOLD 32.0 (never re-fit); exp148's
temporal battery construction VERBATIM with the flip-clock's
presence intervals replaced by the pre-named APERIODIC schedule
(intervals = ceil(8 * U(0.5, 4.0)^k), drawn per edge from
default_rng(201201) — disclosed, zero fitting); exp160's decode stack
VERBATIM (fingerprint asserted) with exp178's scoped arm; the -35.0
pin asserted.

THE BATTERY (40 aperiodic media, two pre-named subfamilies):
  mild-aperiodic (k mean ~1, schedules near-regular) and
  strong-aperiodic (k mean ~4, schedules bursty) — 20 each,
  generator seeds deposited FIRST (seed = 201200 + i).

GATES (each evaluated exactly once):
  GATE-P1 (census) the f_max census over the 40; the classification
           deposited per medium; the gap structure vs the deposited
           32.0 threshold RECORDED (the threshold stands; a bimodal
           census with an empty gap crossing 32.0 confirms the
           scoping's transfer; an interior census does not refute —
           it prices the aperiodic class's position).
  GATE-P2 (scoped read) every aperiodic medium read under the
           production scoped arm; per-media arm selection and errs
           deposited; zero rejections; all errs finite.
  GATE-P3 (the scoping question) on the f_max < 32 side the scoped
           read IS exp167's adopted path bit-exactly; on the
           >= 32 side it IS exp148's raw temporal bit-exactly; the
           per-subfamily median deltas vs the raw temporal arm
           deposited, with the pre-named branches:
           REPAIR (mild-aperiodic median drops >= 20%),
           PARTIAL (0 < drop < 20%), NEUTRAL-HARM (<= 0).
  GATE-P4 (hygiene) pin save/restore asserted; fingerprints
           asserted; zero rejections.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp201_rt_aperiodic_scoping.json
RUN: python3 -m experiments.exp201_rt_aperiodic_scoping [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp201_rt_aperiodic_scoping.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
