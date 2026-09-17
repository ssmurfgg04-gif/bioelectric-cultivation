#!/usr/bin/env python3
"""exp208 — THE C6 TAIL ABLATION (L177's registered next).

The c6 tail at n=400 refused all three named rules (R_O harm, R_H
neutral-harm, R_T no-op) — the RULE_MAP's first n=400-only entry
fires. The registered discovery protocol: a pre-registered ablation
on the tail's own geometry — WHERE does the excess live? The
decoded-vs-target structure of the 25 tail instances: boundary cells,
pair-junction cells, or the interior. The rule is NAMED FROM the
ablation's answer, not from the n=100 map.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt battery
verbatim (the c6 cell's 25 instances, seeds (1,2,3)); the production
scoped arm; the -35.0 pin; the error decomposition (pre-named, zero
knobs): per decoded cell, its err contribution split by cell class —
CANON-BOUNDARY (the cell sits on a canon-value boundary in the
target), PAIR-JUNCTION (the cell is an endpoint of >= 2 chords in the
medium's chord set), INTERIOR (neither) — the three-class
decomposition deposited per instance, the per-class excess
(err_class - the clean-cell class baseline from exp198's c3 clean
battery at n=400) the registered reading.

GATES (each evaluated exactly once):
  GATE-A1 (replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 instances x 3 seeds).
  GATE-A2 (the decomposition) every decoded cell classified into
           exactly one of the three pre-named classes; the per-class
           err shares deposited; the shares sum to the instance err
           (the accounting identity asserted).
  GATE-A3 (the naming) the class carrying the LARGEST mean excess
           names the new rule class's target (the branch recorded:
           BOUNDARY-NAMED / JUNCTION-NAMED / INTERIOR-NAMED); the
           clean-battery baseline (exp198's c3 at n=400) replayed
           bit-exactly as the reference line.
  GATE-A4 (hygiene) zero rejections; all finite; the pin asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp208_c6_tail_ablation.json
RUN: python3 -m experiments.exp208_c6_tail_ablation [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
