#!/usr/bin/env python3
"""exp228 — THE WINDOW-IMPLIED SELF-FED WALK (L200's registered next).

exp223's refutation localized the value channel's limit: the read is
STRUCTURE-driven — the committed VALUES are invisible to the window,
so value-carrying breaks exactly at the host's structure
discontinuities (sub-mV between them). The structure-honest form: the
plan propagated by the WINDOW'S OWN IMPLIED VALUES — the emission the
structure dictates at each frontier cell (the ring's own read output)
becomes the NEXT round's plan at those cells; the walk's target is
then fully self-referential (round k's plan = round k-1's emissions),
no external plan beyond the seed round. The pre-named bar: 6 rings
under the 6.0 bar on H0 and H4.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp223's walk machinery
verbatim (the window construction, the exp178 production scoped read,
the S* lock, the floor-restore discipline, the P6 frozen-commit
discipline — Y2's bit-exact checks reused verbatim); the
WINDOW-IMPLIED PLAN (pre-named, zero knobs): round k's target at the
frontier = round k-1's EMITTED values at the previously-frontier
cells propagated by exp94's spec_target_n over the canon base (the
emission, not the committed frozen value, is what propagates — the
exp223 refutation's own diagnosis); the pre-named hosts: H0 and H4.

GATES (each evaluated exactly once):
  GATE-F1 (the walk) 6 window-implied rings complete with zero
           rejections on H0 and H4 (3 seeds each); ring errs under
           the 6.0 bar throughout.
  GATE-F2 (the frozen-commit clause) the committed values bit-stable
           (P6 verbatim, exp223's Y2 checks reused) — the emissions
           feed the PLAN, never the committed record retroactively.
  GATE-F3 (the self-reference profile) per-round the
           emitted-vs-implied-plan err deposited; the branch named:
           SELF-CARRYING (all 6 rings under the bar) / DEGRADES
           (any ring over).
  GATE-F4 (hygiene) all finite; the S* lock per write; the -60.0
           floor post-restore asserted; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp228_window_implied_walk.json
RUN: python3 -m experiments.exp228_window_implied_walk [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp228_window_implied_walk.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
