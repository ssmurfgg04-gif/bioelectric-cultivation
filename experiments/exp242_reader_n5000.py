#!/usr/bin/env python3
"""exp242 — THE READER AT n=5000+ (the Section 6 item; the Stage 5
extension; exp230 closed n=100->1000 flat, this pushes to n=5000;
RUNNER-NATIVE: sharded for the 20-job fleet; ledger L218).

THE OPEN ITEM: the reader's size-cost curve is n-INVARIANT on
n=100..1000 (exp230: flat 0.54-0.59 mV, slope -0.029). The extreme-n
extension: n=5000 on the path constructor (exp198's scale constructor,
the A_CHAIN family — path(5000), bit-asserted against the same
construction rule). RUNNER-NATIVE: the module takes --shard i (0..14
measured rows: 5 target classes x 3 seeds; 15..19 the redundancy
re-runs for the fleet's 20 slots), runs ONE (class, seed) decode at
n=5000, deposits results/exp242_reader_n5000_shard_<i>.json; the
union merged by the main agent's salvage pass.

PER-ROW PROTOCOL (exp230's machinery verbatim at n=5000): the
production scoped read, the deep band's -60.0 rung carrying both
pre-named instances, the 6.0 bar unchanged, the floors discipline
(-35.0 pins disclosed, -60.0 restored and asserted at exit).

PRE-REGISTERED GATES (evaluated per row + on the union):

  N1  THE COMPLETENESS: 15/15 (class, seed) rows measured, zero
      rejections, all finite.
  N2  THE FLAT PROFILE HOLDS: every row's err < 6.0; the union's worst
      err <= 1.5x exp230's n=1000 worst (0.54) — the sub-linear band
      (pre-named: the reader's cost does not grow into the extreme-n
      regime; the slope check on (log n, log worst) across exp230's
      deposited points + the n=5000 point recorded).
  N3  THE MEMORY DISCIPLINE: the n=5000 substrate constructed without
      densification (the path's banded adjacency handled as a band —
      no 5000x5000 dense array where a band suffices; the peak
      allocation recorded in the deposit).

RUN: per row one decode at n=5000; the fleet covers 15 rows + 5
redundancy re-runs in one 20-job cycle; serial per job, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp242_reader_n5000_shard.json")


def main() -> dict:
    raise NotImplementedError(
        "exp242 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
