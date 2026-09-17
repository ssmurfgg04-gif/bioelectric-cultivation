#!/usr/bin/env python3
"""exp204 — R_H AND R_T AT n=400 ON THE C6 TAIL (L174's registered next).

exp199 falsified R_O as the c6 tail's mechanism (NEUTRAL-HARM, the
no-regression clause refuted). The tail class is c6 = A-SYM+A-PAIR —
the pre-named suspect is the A-PAIR (hyper) dimension, whose rule is
R_H (exp166's rule_hyper_S, L142's cancellation-density weighting);
R_T (exp166's rule_temporal_core) is the temporal rule and must be a
bit-exact no-op on this non-temporal battery — the control clause.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt n=400 battery
(its construction, seed rule and cell definitions VERBATIM); the base
arm = exp199's deposit replayed (its baseline errs are the replay
target — no re-decode of the base arm is needed beyond the replay
assert); R_H and R_T = exp166's rules VERBATIM armed at the frames
level under the -35.0 pin; exp160's decode stack VERBATIM (fingerprint
asserted), the temporal dispatch = exp178's scoped arm.

GATES (each evaluated exactly once):
  GATE-B1 (replay) exp199's base-arm errs replay bit-exactly vs its
           deposit at the deposit's rounding (the battery is the SAME
           construction; spot-assert on the c6 tail + one clean cell,
           all seeds).
  GATE-B2 (R_H on the tail) R_H armed on the hyper-active instances;
           per-instance deltas deposited; the c6 tail's median delta
           names the branch: REPAIR (median drops >= 20%),
           PARTIAL (0 < drop < 20%), NEUTRAL-HARM (median <= 0).
  GATE-B3 (the R_T control + composition) R_T on this battery is a
           bit-exact no-op (T=1 frames — exp166's rule_temporal_core
           identity); the R_H x R_T composition equals R_H alone
           bit-exactly (the exp170 dominated-composition lesson:
           deposited, pre-named, not an adoption candidate unless
           R_H itself repairs).
  GATE-B4 (hygiene + no-regression) zero rejections; all errs
           finite; the pin asserted; on hyper-INACTIVE instances
           R_H is a no-op bit-exact; on hyper-active non-tail
           instances no degradation beyond +0.05 mV.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp204_rh_rt_n400_tail.json
RUN: python3 -m experiments.exp204_rh_rt_n400_tail [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp204_rh_rt_n400_tail.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
