#!/usr/bin/env python3
"""exp221 — THE WRITE-PATH BOUNDARY ARM AT n=400 (L194's registered
next).

Three pre-registered read arms (exp213 boundary-only, exp216
context-shell, exp219 F1-composition) refuted the read-face repair
line with bit-exact instruments — the boundary excess is a WRITE-side
phenomenon. The write-side dual: the writer's canon-fallback identity
overwrite (the ~9 mV floor exp156 measured at the write path, CF-1's
removal patch exp165/168) re-examined AT the boundary cells of the
n=400 corner battery — where does the write path's boundary signature
live, and does a boundary-localized write arm (the same zero-knob
discipline, on the write face) move the c6 tail's 1.30 bar?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt battery
verbatim (the c6 cell's 25 instances, seeds (1,2,3), the production
scoped arm for the read side); exp208's classification verbatim (the
CANON-BOUNDARY mask); the WRITE arm (pre-named, zero knobs): at each
instance the write pass re-runs with the canon-fallback identity map
DISABLED exactly at the boundary cells (the fallback's identity
overwrite skipped for the boundary class, applied everywhere else —
CF-1's removal generalized one class further), every interior cell's
write path bit-unchanged; the -60.0 CF-1 production floor asserted
(the write side); the decode/replay chain identical to exp213's (the
floor pin -35.0 semantics on the READ modules only).

GATES (each evaluated exactly once):
  GATE-W1 (the replay) the unmodified battery replays bit-exactly vs
           exp199's deposit (25 x 3) — the write arm's baseline.
  GATE-W2 (the write arm) the boundary-write-armed errs for all 25
           instances x 3 seeds; the branch named: REPAIR (median
           <= 1.30 — the tail's bar crossed), IMPROVED (median
           improved >= 20% vs 1.40, bar not crossed — the nesting
           disclosed), NONE.
  GATE-W3 (the identity clause) the interior cells' written values
           bit-unchanged by the arm (the arm touches exactly the
           boundary class's write path); the canon-fallback's skip
           asserted per boundary cell.
  GATE-W4 (hygiene) zero rejections; all finite; both floors
           asserted (-60.0 write side, -35.0 read-side pin
           save/restore).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp221_write_path_boundary_arm.json
RUN: python3 -m experiments.exp221_write_path_boundary_arm [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results",
                   "exp221_write_path_boundary_arm.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
