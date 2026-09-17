#!/usr/bin/env python3
"""exp202 — CROSS-ORGANISM CARRIAGE (Stage 4's cross-organism edge).

Stage 4's cross-substrate leg closed 100/100 (exp182: S* = (64.0,
0.0) carries 100 fresh targets at worst-case margin +5.404 on the
REFERENCE organism, the n=100 A_CHAIN lattice). The registered
cross-organism question: does the SAME substrate carriage hold on
DIFFERENT HOST GEOMETRIES — the size law's scale (n=400) and the
corpus's rewired organism structures?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp182's protocol VERBATIM
(probe_margin + writable_3seed at the locked substrate rung
S* = (64.0, 0.0), seeds (1, 2, 3), exp161's _lock_substrate asserted
per write); TARGETS = exp182's DEPOSITED 100-target manifest reused
checksummed (zero new fitting — the manifest IS the pre-registration
artifact); HOSTS (the pre-named set, zero fitting):
  H0 the reference organism (n=100, A_CHAIN — exp182's own host; the
     replay anchor),
  H1 the size-law organism (n=400, labeling_bfs_n(A_CHAIN-400) —
     exp198's scale),
  H2-H11 TEN corpus-rewired organisms: exp88's rewire machinery
     applied to the first 10 PlanformDB records (seed = 202200 + i,
     disclosed), each yielding a host adjacency with its own canon
     labeling asserted == its engine canon.

GATES (each evaluated exactly once):
  GATE-H1 (anchors) H0 replays exp182's verdicts bit-exactly (the
           writability set and margins at deposit rounding); every
           host's canon == its engine canon asserted.
  GATE-H2 (the carriage bar) >= 90/100 targets writable_3seed at S*
           on EVERY host H1-H11; the per-host miss lists deposited;
           zero rejections.
  GATE-H3 (the margin profile — the deliverable) per-host worst-case
           margin deposited; the worst host NAMED; the per-host
           margin-vs-depth profile (exp182's four bins) deposited;
           exp182's +5.404 recorded as the reference line.
  GATE-H4 (hygiene) all errs finite; no per-target or per-host
           tuning anywhere; the substrate lock log carries every
           (host, rung, wiring-id) triple at S*.
NO post-hoc tuning. --smoke permitted (H0 + targets 0-2), discarded.
DEPOSIT: results/exp202_cross_organism_carriage.json
RUN: python3 -m experiments.exp202_cross_organism_carriage [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp202_cross_organism_carriage.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
