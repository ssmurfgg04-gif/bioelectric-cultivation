#!/usr/bin/env python3
"""exp218 — THE AUTOCATALYTIC AXIS (L190's registered next).

Stage 4's remaining 101% target: the cone expands ITSELF. exp151's
self-expansion walk (seed_cone -> frontier_of -> expansion_step, 6
rings, the committed set feeding the next round) is re-armed at S* on
the 12 union hosts (exp214's build): the expansion must be
SELF-FUELED on every organism — each ring's emission becomes the next
round's substrate with no external re-seeding — and the expansion must
ADD carrying capacity, never re-price it: the already-committed
cells' values are bit-stable across subsequent rounds, and the union
carriage margin profile is non-decreasing within the 0.05 bar across
rounds.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp151's walk machinery
VERBATIM (seed_cone, frontier_of, expansion_step, RINGS = 6, the
window discipline; the production scoped read via exp178's wiring);
the host set = exp214's build_hosts verbatim (H0/H1/H2-H11
checksummed from exp202's deposit); S* = (64.0, 0.0) asserted on
every write (the lock log); the CF-1 production floor -60.0 asserted.
THE CAPACITY CLAUSE (pre-named, zero knobs): after each ring k >= 2,
the committed prefix's per-cell values from round k-1 are re-read —
the clause holds iff every previously committed cell's value is
bit-unchanged or within the 0.05 mV drift bar (exp202's no-regression
bar); the margin profile clause is priced on H0 and H4 ONLY (the
reference and the worst-margin host — pre-named, disclosed): the
union manifest (exp214's 110) re-priced writable_3seed at S* after
rings 2, 4, 6 — the profile NON-DECREASING within 0.05.

GATES (each evaluated exactly once):
  GATE-X1 (the walk) the self-expansion walk completes 6 rings with
           zero rejections on EVERY one of the 12 hosts at S* (the
           cone expands itself on every organism; ring errs under
           exp151's 6.0 bar).
  GATE-X2 (the capacity clause) every previously committed cell's
           value bit-stable (or <= 0.05 mV drift) across subsequent
           rounds, all hosts, all rings — the expansion ADDS
           capacity, never disturbs it.
  GATE-X3 (the margin profile) the union carriage on H0 and H4
           re-priced after rings 2, 4, 6: per-round worst-case
           margin non-decreasing within the 0.05 bar (ADD-CAPACITY)
           vs re-priced (REFUTE).
  GATE-X4 (hygiene) all errs finite; the (host, ring, wiring-id)
           lock log at S*; the -60.0 floor asserted; no per-target
           tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp218_autocatalytic_axis.json
RUN: python3 -m experiments.exp218_autocatalytic_axis [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp218_autocatalytic_axis.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
