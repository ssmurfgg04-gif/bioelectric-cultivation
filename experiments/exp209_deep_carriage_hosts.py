#!/usr/bin/env python3
"""exp209 — THE DEEP-BAND CARRIAGE ACROSS THE 12 HOSTS (L181's
registered next).

exp202 closed the carriage on exp182's deposited manifest (the full
widened repertoire). L181's registered axis: the TARGET class — the
deep-band targets the library cannot represent (exp194's T2) carried
at S* across the same 12 hosts. The substrate's organism-independence
is asked INSIDE the band.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp202's carriage protocol
verbatim (exp161's probe_margin + writable_3seed at S* = (64.0, 0.0),
seeds (1,2,3), the host set H0/H1/H2-H11 from exp202's deposit — the
same 12 hosts, their build records reused checksummed); the TARGET
set (pre-named, zero fitting): exp172's uniform-rung constructions at
rungs {-40, -45, -50, -55, -60} x instances {0, 1} = 10 deep targets,
f = spec_target_n, canon asserted per target (the exp176-verified
construction discipline).

GATES (each evaluated exactly once):
  GATE-K1 (the anchor) H0's deep-target margins replay exp172's
           deposited prices bit-exactly at the reference organism
           (the deposit's counterfactual engine produced them
           bit-exactly at CF-1 — exp172's discipline).
  GATE-K2 (the carriage bar) >= 9/10 deep targets writable_3seed at
           S* on EVERY host (the deep band is harder than the full
           repertoire's 90/100 — the pre-named 9/10 bar); the
           per-host miss lists deposited.
  GATE-K3 (the margin profile) per-host worst-case deep margin
           deposited; the worst host named; the margin-vs-rung
           profile (the deep rungs as bins) deposited; exp202's
           worst-host line (+5.285) recorded as the reference.
  GATE-K4 (hygiene) all errs finite; the lock log carries every
           (host, rung, wiring-id) triple at S*; no per-target
           tuning.
NO post-hoc tuning. --smoke permitted (H0 + targets 0-1), discarded.
DEPOSIT: results/exp209_deep_carriage_hosts.json
RUN: python3 -m experiments.exp209_deep_carriage_hosts [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp209_deep_carriage_hosts.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
