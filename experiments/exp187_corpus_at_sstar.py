#!/usr/bin/env python3
"""exp187 — THE CORPUS AT S* (the substrate vs the mined planform
records).

Stage 5 path 2's next scale-up (L152/L157 line): S* = (64.0, 0.0)
carries 10 deposited (exp161) and 100 fresh random (exp182) targets —
all SYNTHETIC. The corpus's 1,716 mined planform records are the
EMPIRICAL target class. THIS EXPERIMENT samples 100 corpus patterns
and prices their writability at S*.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Sample, protocol, and gates are fixed now.

THE SAMPLE (zero fitting): the corpus deposit (exp118's mined records
— results/exp118_corpus_full.json) supplies the pattern bank; the
sample = records indexed by rng = default_rng(187187), 100 records
drawn without replacement from the bank's decoded-pattern records
(the record field carrying the decoded zone/identity program; the
exact field name read from the deposit at run time and recorded in
the manifest); each sampled pattern built through exp94's
spec_target_n on its own labeling (canon == wildtype asserted per
target). The manifest (100 record ids + f_sha256) deposited FIRST.

THE PROTOCOL: exp161's writable_3seed + probe_margin at S* =
(64.0, 0.0), seeds (1, 2, 3), the substrate lock asserted per write.

GATES (each evaluated exactly once):
  GATE-C1 (manifest first) the manifest precedes the battery in the
           deposit (byte-offset assertion); 100 unique records.
  GATE-C2 (the empirical bar) >= 90/100 corpus targets writable at
           S* (decode < 6.0 AND hold < 6.0 on 3/3 seeds); the miss
           list deposited; zero rejections.
  GATE-C3 (the margin profile) worst-case margin deposited; the
           margin histogram + the depth profile (the corpus's own
           value distribution) deposited; exp182's +5.404 reference
           line recorded.
  GATE-C4 (hygiene) all errs finite; no per-target tuning.

NO post-hoc tuning. --smoke (3 sampled records) permitted, discarded.
Deposit: results/exp187_corpus_at_sstar.json
Jobs: manifest | battery
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

from experiments.exp161_universal_substrate import (  # noqa: E402
    probe_margin, writable_3seed, _lock_substrate,
)

S_STAR = (64.0, 0.0)
SAMPLE_SEED = 187187
N_SAMPLE = 100
SCALEUP_BAR = 90

OUT = os.path.join(ROOT, "results", "exp187_corpus_at_sstar.json")
CORPUS = os.path.join(ROOT, "results", "exp118_corpus_full.json")
DEP161 = os.path.join(ROOT, "results", "exp161_universal_substrate.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["manifest", "battery", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
