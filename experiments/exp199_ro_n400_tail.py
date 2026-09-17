#!/usr/bin/env python3
"""exp199 — R_O AT n=400 ON THE C6 TAIL (the reader's residual map).

exp198's registered next (L171): the universal reader's residual map
is fully named — random 0.630, adversarial n=100 0.545, adversarial
n=400 0.705 with the tail 25/100 owned by cell c6 (A-SYM+A-PAIR) —
and the remaining edge is the c6 tail's mechanism: price R_O
(exp166's rule_oriented_restore, the oriented one-way support
restore) at n=400 on the c6 tail.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp198's n=400 adversarial
battery rebuilt (its seed rule and cell definitions VERBATIM, n=400
via the CornerMedium constructor's first parameter); exp160's decode
stack VERBATIM (fingerprint asserted == exp160's deposit) with the
temporal dispatch = exp178's scoped arm under the -35.0 pin; R_O =
exp166's rule_oriented_restore VERBATIM applied at the frames level.

GATES (each evaluated exactly once):
  GATE-A1 (replay) the 100-instance n=400 battery replays
           BIT-EXACTLY vs exp198's deposit under the production
           scoped arm (all errs + verdicts equal at the deposit's
           rounding, seeds (1,2,3)).
  GATE-A2 (R_O on the oriented cells) R_O armed on every
           oriented-active instance (the cells carrying A-SYM per
           exp181's definitions); per-instance deltas deposited;
           the c6 tail's median delta names the branch:
           REPAIR (median drops >= 20%), PARTIAL (0 < drop < 20%),
           NEUTRAL-HARM (median <= 0).
  GATE-A3 (no-regression) on oriented-INACTIVE instances R_O is a
           no-op by construction — bit-exact replay; on
           oriented-active NON-tail instances no instance degrades
           by more than +0.05 mV (the pre-named no-regression bar).
  GATE-A4 (hygiene) zero rejections; all errs finite; the -35.0
           instrument pin asserted; the fingerprint asserted.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp199_ro_n400_tail.json
RUN: python3 -m experiments.exp199_ro_n400_tail [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
