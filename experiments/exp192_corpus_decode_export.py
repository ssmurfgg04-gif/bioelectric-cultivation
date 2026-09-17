#!/usr/bin/env python3
"""exp192 — THE CORPUS DECODE EXPORT (the empirical bank built, then
S* re-runs).

exp187's registered next (L163): the corpus's decoded programs live
in the mining pipeline's decode stage, not the comparison bank. Export
them, then price the exported class at S*.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. If the mining pipeline cannot re-run in this environment, deposit the BLOCKED finding with the exact failing stage (a completed S1 REFUTE) — do not improvise a decoder.

GATES (each evaluated exactly once):
  GATE-S1 (the export) planform_mining.py's decode path re-run
           (or its deposited intermediates re-read, disclosed) to
           produce results/corpus_decoded_programs.json: per record
           the decoder's own zone/identity program + provenance; the
           bank tracked and force-added; the decode MAE consistency
           spot-checked vs the deposited 0.290 machinery (>= 20
           records re-scored within tolerance, recorded).
  GATE-S2 (the battery) 100 programs sampled (seed 187187) from the
           export, built via exp94's spec_target_n (canon ==
           wildtype asserted), writability at S* = (64.0, 0.0) via
           exp161's writable_3seed + _lock_substrate.
  GATE-S3 (the empirical bar) >= 90/100 writable at the 6.0 bar on
           3/3 seeds; the miss list deposited; zero rejections.
  GATE-S4 (hygiene) manifest-first byte-offset assertion; all errs
           finite; no per-target tuning.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp192_corpus_decode_export.json
RUN: python3 -m experiments.exp192_corpus_decode_export [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp192_corpus_decode_export.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
