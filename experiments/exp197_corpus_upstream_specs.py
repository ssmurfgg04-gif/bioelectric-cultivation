#!/usr/bin/env python3
"""exp197 — THE UPSTREAM SPECS EXPORT (the corpus leg's last resort).

exp192's registered next (L168): the loader/mapping INPUTS that fed
the decode — the per-record zone specs the simulator consumed. If
they also do not persist per record, the corpus leg closes
STRUCTURALLY BLOCKED.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp192's stage-census machinery verbatim; exp161's S* protocol.

GATES (each evaluated exactly once):
  GATE-X1 (the trace) the mining pipeline's loader/mapping
           stage traced (planform_mining.py + the exp118 machinery):
           do per-record zone specs exist upstream (deposited
           intermediates or re-derivable from the raw records)?
           The stage census deposited either way.
  GATE-X2 (the export or the closure) IF the specs exist: export
           results/corpus_zone_specs.json (tracked), build 100
           targets (seed 187187), price at S* via exp161's
           machinery (the exp187/192 gate set); IF NOT: deposit
           STRUCTURALLY BLOCKED with the census (a completed
           finding — the corpus leg moves to the wetlab companion
           protocol's deposit format, registered).
  GATE-X3 (the empirical bar, conditional) if the battery ran:
           >= 90/100 writable at the 6.0 bar on 3/3 seeds.
  GATE-X4 (hygiene) manifest-first discipline where a battery ran;
           zero improvised decoders anywhere.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp197_corpus_upstream_specs.json
RUN: python3 -m experiments.exp197_corpus_upstream_specs [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp197_corpus_upstream_specs.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
