#!/usr/bin/env python3
"""exp214 — THE 110-TARGET UNION CARRIAGE (L186's registered next).

exp202 carried exp182's 100-target manifest across the 12 hosts
(worst margin +5.285); exp209 carried the 10 deep targets across the
same hosts (worst +5.298) — separately. L186's registered question:
does S* carry the UNION (a 110-target manifest) at the same margin
floor on the same 12 hosts — Stage 4's cross-organism axis closes at
the union or names the interference.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp202's carriage protocol
verbatim (the host-parameterized replica, K1-anchored twice —
exp182's and exp172's deposits); the host set rebuilt checksummed
from exp202's deposit (exp209's build, verified); the TARGET set
(pre-named, zero fitting): exp182's manifest (100, checksummed) +
exp209's 10 deep targets (exp172's construction) = 110.

GATES (each evaluated exactly once):
  GATE-U1 (the anchors) both replay clauses hold: exp182's manifest
           f_sha256 checksummed on H0; exp172's prices bit-exact (the
           exp209 K1 rows re-verified).
  GATE-U2 (the union bar) >= 99/110 targets writable_3seed at S* on
           EVERY host (the pre-named union bar: the full repertoire's
           90% floor and the deep band's floor composed — 90/100 and
           9/10 both lift to 99/110); per-host miss lists deposited.
  GATE-U3 (the interference question) the union's per-host worst-case
           margin vs the two separate runs' worst margins (+5.285 /
           +5.298): the branch named — NO-INTERFERENCE (union worst
           >= min(separate worsts) - 0.05) / INTERFERENCE-NAMED (the
           union degrades beyond the 0.05 bar; the (host, target)
           pairs carrying the degradation deposited).
  GATE-U4 (hygiene) all errs finite; the (host, rung, wiring-id)
           lock log at S*; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0 + 10 targets), discarded.
DEPOSIT: results/exp214_union_carriage.json
RUN: python3 -m experiments.exp214_union_carriage [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp214_union_carriage.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "corpus",
                                      "gates"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
