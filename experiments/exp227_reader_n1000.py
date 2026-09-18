#!/usr/bin/env python3
"""exp227 — THE READER AT n=1000 (L199's registered next).

The structured-media adversarial reader held at 0.62 mV worst (L199)
— under the random baseline. The size axis's terminal point for the
reader line: the same structured-media sweep at n=1000 — path(1000)
as host + the corner battery at n=1000, 5 target classes x 3 seeds,
the 6.0 bar unchanged. If the reader holds at n=1000, the media-
independence claim carries to the scale where the n=400 corner
battery's boundary phenomenon (exp208) can be re-examined at a second
large n.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp225's sweep machinery
verbatim (the production scoped read, the target classes, the 3
seeds); the hosts: path(1000) (exp198's scale constructor — the SAME
constructor that builds A_CHAIN and H1) + the n=1000 corner battery
(exp166's CornerMedium at n=1000, 5 instances, gen-seed rule
166000 + j); the floors asserted post-restore (exp218's exp169-import
discipline VERBATIM — the body MUST restore CORE.NEURAL_SPEC_MIN =
-60.0 after the import chain and disclose it).

GATES (each evaluated exactly once):
  GATE-E1 (the n=1000 sweep) path(1000): 5 target classes x 3 seeds
           decode with zero rejections under the 6.0 bar; the corner
           battery at n=1000: 5 instances x 3 seeds decode with zero
           rejections; complete, not sampled.
  GATE-E2 (the reader bar) every err finite and < 6.0; the per-host
           worst-case deposited; the n=1000 worst vs the n=400
           structured worst (0.62, L199) and the random worst (1.45)
           deposited as the contrast reading.
  GATE-E3 (the boundary signature at n=1000) the corner battery's
           decomposition at n=1000 (exp208's three-class machinery
           verbatim): the CANON-BOUNDARY excess vs the interior
           (the interior-0.000 identity exp208 named, re-tested at
           the second large n) — the branch named: REPRODUCED
           (interior excess 0.000 exactly at 2-dp) / DRIFTED.
  GATE-E4 (hygiene) zero rejections; all finite; the floor
           discipline asserted and disclosed.
NO post-hoc tuning. --smoke permitted (path(1000), 1 target), discarded.
DEPOSIT: results/exp227_reader_n1000.json
RUN: python3 -m experiments.exp227_reader_n1000 [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp227_reader_n1000.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
