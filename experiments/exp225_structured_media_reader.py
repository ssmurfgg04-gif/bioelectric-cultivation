#!/usr/bin/env python3
"""exp225 — THE STRUCTURED-MEDIA ADVERSARIAL READER (L189/L194's
Stage 5 path-1 push).

The universal reader closed on random media (200 random media, zero
rejections; the corner battery at n=400) — the registered Stage 5
extension: STRUCTURED adversarial media, the hardest class the stack
can name. The 12 union hosts' own graph structures (small-world
corpus rewires + the n=400 path) used AS decode media — the reader
decoding each host's own W under the production scoped arm against
the host's own canon target and against the union's carried targets:
if the reader holds on the media the WRITER itself built from, the
"any medium" claim extends from random to structured.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp214's build_hosts verbatim
(the 12 hosts, checksummed from exp202's deposit); the production
scoped read (exp178's wiring — exp148.decode("scoped", ...) with
exp169's f_max); exp169's THRESHOLD asserted; the floors asserted
post-restore (exp218's disclosed exp169-import discipline: restore
CORE.NEURAL_SPEC_MIN = -60.0 after the import chain); the targets
per host: the host's own canon (wildtype) + 3 union targets
(manifest indices 0, 49, 99 — pre-named) + the deep band's -60.0
rung both instances (pre-named).

GATES (each evaluated exactly once):
  GATE-M1 (the structured sweep) all 12 hosts x 5 targets x 3 seeds
           decode with ZERO rejections under the production scoped
           arm (structured media, complete, not sampled).
  GATE-M2 (the reader bar) every decode's err under the 6.0 bar
           (exp151/155's verify bar); the per-host worst-case
           deposited; zero non-finite.
  GATE-M3 (the structured-vs-random contrast) the structured media's
           worst err vs the corner battery's deposited worst (exp198/
           exp199's n=400 line): the branch named — HELD (structured
           worst <= the random worst + 0.5 mV) / DEGRADES (beyond).
  GATE-M4 (hygiene) the -60.0/-35.0 floor discipline asserted
           (exp218's restore, disclosed); zero rejections; all
           finite; no per-media tuning.
NO post-hoc tuning. --smoke permitted (H0 only), discarded.
DEPOSIT: results/exp225_structured_media_reader.json
RUN: python3 -m experiments.exp225_structured_media_reader [--smoke] [--job ...] [--out ...]
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
                   "exp225_structured_media_reader.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
