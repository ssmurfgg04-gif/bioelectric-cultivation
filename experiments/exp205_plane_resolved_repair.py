#!/usr/bin/env python3
"""exp205 — THE PLANE-RESOLVED REPAIR AT THE CANON-BOUNDARY RING
(L175's registered next).

L175 localized the canon-boundary residual: the production read's
statistic concentrates at exactly the 3 breaking F3 ring-1 events
(ratio 2.973). L140's named repair candidate is the exp158-class
plane-resolved readout — the read that can SEE the boundary is the
read that can REPAIR it. This run arms a plane-resolved face at the
F3 ring-1 window and prices the repair.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp200's replay machinery
verbatim (exp155's battery re-run in-process under the FULL floor pin
— CORE/M136/M156/M148/M142 — the exp200-deposited pin set; the 141-row
replay + the 69-row ring-event table are the R1 anchor); the
plane-resolved readout = exp158's plane machinery VERBATIM (its
plane-resolved reading of the window, zero knobs) applied at the F3
ring-1 window ONLY; the -35.0 pin asserted throughout.

THE REPAIR RULE (pre-registered, zero knobs): at the F3 ring-1
operating point, the read window's boundary-plane cells are read
plane-resolved (exp158's machinery) while everything else keeps
exp155's JD protocol verbatim — one face added at the exact site the
localization named, nothing else touched.

GATES (each evaluated exactly once):
  GATE-C1 (anchor) exp200's replay reproduces (141/141 ring rows, 0
           mismatches; the 3 boundary events reproduce their breaking
           errs at deposit rounding).
  GATE-C2 (the repair) the plane-resolved arm at F3 ring-1: per-event
           errs deposited for all 3 seeds; the branch named:
           REPAIR (all 3 events < 6.0 mV), PARTIAL (>= 1 event < 6.0
           and none worse than the disciplined baseline), NONE
           (otherwise).
  GATE-C3 (no-regression) every passing ring's err under the armed
           protocol is bit-exact vs exp200's replay (the arm touches
           ONLY the boundary ring's window — the identity clause).
  GATE-C4 (hygiene) zero rejections; all errs finite; the pin
           save/restore asserted.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp205_plane_resolved_repair.json
RUN: python3 -m experiments.exp205_plane_resolved_repair [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp205_plane_resolved_repair.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
