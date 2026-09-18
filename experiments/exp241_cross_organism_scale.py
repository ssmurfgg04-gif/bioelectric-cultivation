#!/usr/bin/env python3
"""exp241 — CROSS-ORGANISM AT SCALE (the Section 6 item; the Stage 4
extension; exp214 closed 12 hosts, this extends the carriage to 100;
RUNNER-NATIVE: sharded for the 20-job fleet; ledger L217).

THE OPEN ITEM: exp209/exp214's universal-substrate result (12/12 hosts
carry all 10 deep targets at S*, worst margin +5.298) extends to 100+
hosts. RUNNER-NATIVE protocol: the module takes --shard i (0..19);
shard i runs hosts [5*i, 5*i+5) from the pre-registered 100-host grid
(exp202's host-generator machinery, the host seeds 0..99 — the SAME
generator, 100 draws), deposits results/exp241_host_shard_<i>.json,
and the union is merged by the main agent's salvage pass.

PER-SHARD PROTOCOL (each host): the exp209 K1-anchor discipline — the
host substrate generated (exp202's generator verbatim), the 10 deep
targets (exp209's frozen deep-band list) written at S* = (64.0, 0.0)
via the star write protocol, 3 seeds each, the carriage margin
recorded per (host, target): margin = 6.0 - err (the pre-named bar
6.0).

PRE-REGISTERED GATES (evaluated per shard + on the union):

  X1  THE SHARD COMPLETENESS: 5/5 hosts x 10 targets x 3 seeds measured,
      zero rejections, all finite.
  X2  THE CARRIAGE (per shard, and the union on merge): every host
      carries all 10 deep targets (err < 6.0 everywhere); the union's
      worst margin recorded beside exp209's +5.298 (the 12-host
      anchor).
  X3  THE DETERMINISM: the shard deposit re-runs bit-identical (the
      host generator's seeds fixed; the spot re-run on shard 0).

RUN: per shard ~25 hosts-worth of the battery = 5 hosts x 10 targets
x 3 seeds = 150 writes at the star; serial, BLAS pinned; the fleet
covers 100 hosts in one 20-job cycle.
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
OUT = os.path.join(ROOT, "results", "exp241_host_shard.json")


def main() -> dict:
    raise NotImplementedError(
        "exp241 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
