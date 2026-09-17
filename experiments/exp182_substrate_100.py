#!/usr/bin/env python3
"""exp182 — UNIVERSAL SUBSTRATE: 100 MORE TARGETS (path 2's scale-up).

Stage 5 path 2 (the handoff ledger's LANDED status): S* = (64.0, 0.0)
carries the 10 deposited diverse targets at worst-case margin +5.391
(exp161). The registered scale-up: 100 FRESH targets. With CF-1 the
writable repertoire runs to -60, and exp172 priced the deep band
writable at the production cell — so the fresh targets span the FULL
widened repertoire, including the deep band S* has never been asked
to carry.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Targets, protocol, and gates are fixed now.

THE TARGET SET (100 fresh programs, zero fitting):
  built by ONE pre-registered generator: rng = default_rng(182182);
  for t = 0..99: zone count k ~ {1: 3, 2: 4, 3: 2, 4: 1} (the
  exp161 diversity ladder, 1-4 zones); each zone a triple
  (start, end, value): start ~ U(0.02, 0.80), width ~ U(0.08, 0.16),
  value ~ U(-60.0, -15.0) — the FULL repertoire, deep band included,
  rounded to 1 dp; non-overlap enforced by construction (sorted
  starts, regenerated on collision — the generator is deterministic
  at the seed); values below -35 are EXPLICITLY WELCOME (that is the
  scale-up's point: S* vs the deep band). Target f built by exp94's
  spec_target_n on the MULTI 3-zone program's labeling (canon ==
  wildtype asserted per target, exp172's construction discipline).
  The 100 triples + f_sha256 deposited FIRST (the target manifest is
  the pre-registration artifact).

THE PROTOCOL (exp161's, verbatim): probe_margin and writable_3seed
at the locked substrate rung S* = (64.0, 0.0), seeds (1, 2, 3), the
substrate lock asserted per write (exp161's _lock_substrate).

GATES (each evaluated exactly once):

  GATE-V1 (the substrate lock) exp161's _lock_substrate fires on
           every write; the log carries 100 (rung, wiring-id) pairs
           all at S*.
  GATE-V2 (the scale-up bar) >= 90/100 targets writable at S*
           (writable_3seed: decode < 6.0 AND hold < 6.0 on 3/3
           seeds); the miss list deposited with per-target margins;
           zero rejections.
  GATE-V3 (the margin profile — the deliverable) worst-case margin
           over the 100 deposited; the margin-vs-depth profile
           (values binned at [-60,-50), [-50,-40), [-40,-30),
           [-30,-15]) deposited; the deposited 10-target margin
           (+5.391 worst) recorded as the reference line.
  GATE-V4 (hygiene) all errs finite; the canon == wildtype assert
           holds per target; no per-target tuning anywhere.

NO post-hoc tuning. A --smoke check (targets 0-2) is permitted
before the credited run and discarded.

DEPOSIT: results/exp182_substrate_100.json

RUN:
  python3 -m experiments.exp182_substrate_100            # full
  python3 -m experiments.exp182_substrate_100 --smoke    # check
  python3 -m experiments.exp182_substrate_100 --job V2
  # jobs: manifest | battery
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

from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)
from experiments.exp161_universal_substrate import (  # noqa: E402
    probe_margin, writable_3seed, _lock_substrate, _SUBSTRATE_LOG,
)

# ---- FIXED CONSTANTS ------------------------------------------------
S_STAR = (64.0, 0.0)
TARGET_SEED = 182182
N_TARGETS = 100
ZONE_COUNT_LADDER = {1: 3, 2: 4, 3: 2, 4: 1}
WIDE_LO = -60.0
WIDE_HI = -15.0
SCALEUP_BAR = 90                 # of 100

OUT = os.path.join(ROOT, "results", "exp182_substrate_100.json")
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
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
