#!/usr/bin/env python3
"""exp216 — THE CONTEXT-SHELL ARM AT n=400 (L189's registered next).

exp213's refutation localized the face's failure mode: the plane-
resolved read is CONTEXT-HUNGRY — armed only at the ~130 scattered
canon-boundary cells the sub-window carries almost no neighborhood and
the emission lands 7.7x off plan, while the same face at exp205's
full-window site HALVED the boundary residual. The registered repair:
the same face at the boundary cells' CONTEXT WINDOW — win = the
boundary cells PLUS their lattice-neighbor shell (i +/- 1 for each
boundary cell), the smallest window that restores exp205's geometry.
The pre-named bars are UNCHANGED: the tail's 1.30 bar and the
interior-bit-exact identity clause (now bound to the shell window's
complement).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp213's body machinery
verbatim (the replay battery vs exp199's deposit + exp208's
decomposition reference; exp208's classification; the canon-plane map
on the battery's base support; the TC1/TC2/TC3 face) with ONE
pre-named delta: the arm's window = {bnd} u {neighbors(bnd)} on the
ring backbone; the face reads the shell window plane-resolved and the
ARMED cells' values are replaced ONLY at the boundary cells (the
shell's interior members provide context and are NOT written — the
decoded V is kept bit-exactly there).

GATES (each evaluated exactly once):
  GATE-S1 (replay) the c6 battery replays bit-exactly vs exp199's
           deposit (25 x 3) and exp208's decomposition reproduces
           bit-exactly at the reference (exp213's B1 verbatim).
  GATE-S2 (the shell arm) the shell-armed errs for all 25 instances
           x 3 seeds; the branch named: REPAIR (median <= 1.30 — the
           tail's bar crossed), IMPROVED (median improved >= 20% vs
           1.40, bar not crossed — the pre-registered nesting
           disclosed), NONE.
  GATE-S3 (the identity clause) every cell OUTSIDE the shell window
           bit-unchanged by the arm; the face's emission asserted ==
           the shell window; the boundary cells are the only cells
           whose values change vs the decoded V.
  GATE-S4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted (exp199's semantics).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp216_context_shell_arm.json
RUN: python3 -m experiments.exp216_context_shell_arm [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp216_context_shell_arm.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
