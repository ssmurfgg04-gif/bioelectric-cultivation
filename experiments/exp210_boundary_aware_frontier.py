#!/usr/bin/env python3
"""exp210 — THE COMPOSED BOUNDARY-AWARE FRONTIER RULE (L178's
registered next).

exp205's pricing: the plane-resolved face halves the boundary residual
(21-48% improvements at exactly the localized site) yet 0/3 cross the
bar; exp155's discipline fails AT the boundary ("cannot exclude the
boundary cell without excluding the boundary itself", L140's exact
words). The registered composition: the two complementary mechanisms
at the one site both can see — the JD-a membership face gains a
BOUNDARY-AWARE exception (the fence yields exactly at canon-boundary
cells) and the boundary cells' read face is plane-resolved
(exp158's machinery, exp205's armed face). One composed rule, zero
knobs, aimed at the 3 breaking F3 ring-1 events.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp205's replay machinery
verbatim (the full-capture floor pin, the 141-row anchor, the 69-row
ring-event table); the composed rule (pre-registered here, zero
knobs): JD-a' = the flip-quiet reach F_q of exp155's JD-a, EXCEPT
that a node whose only committed-adjacency is a flip edge AND which
sits on a canon-value boundary in the target is ADMITTED to the
frontier with the plane-resolved read face (exp158's machinery)
instead of exclusion; everything else exp155's protocol verbatim.

GATES (each evaluated exactly once):
  GATE-F1 (anchor) exp205's replay reproduces (141/141 ring rows;
           the 3 boundary events at their disciplined errs).
  GATE-F2 (the composition) the composed rule at F3 ring-1: per-event
           errs for all 3 seeds; the branch named: REPAIR (all 3 <
           6.0), PARTIAL (>= 1 < 6.0 and none worse than the
           disciplined baseline), NONE.
  GATE-F3 (no-regression) every passing ring's err bit-exact vs the
           replay outside the F3 ring-1 site (the identity clause;
           the composed rule touches only the boundary site).
  GATE-F4 (hygiene) zero rejections; all finite; the pin
           save/restore asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp210_boundary_aware_frontier.json
RUN: python3 -m experiments.exp210_boundary_aware_frontier [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp210_boundary_aware_frontier.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
