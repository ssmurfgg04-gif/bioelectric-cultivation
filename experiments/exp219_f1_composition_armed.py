#!/usr/bin/env python3
"""exp219 — THE F1 COMPOSITION ARMED (L187's registered next).

exp212's census sweep named the site where the composed rule's
membership face can act for the first time: the JD-a fence bites at
F1_zone_tail rings 2-6 (11 excluded cell-ring pairs, 5 of them
canon-value boundary cells — the admission clause WOULD fire). This
run ARMS the exp210 composed rule (the fence's boundary-aware
exception + the plane-resolved read face) at F1: the boundary cells
in the fence's exclusions are ADMITTED with the plane-resolved read
face; everything else is exp155's disciplined protocol verbatim.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp210's composed machinery
VERBATIM (the JD-a' admission clause, the plane-resolved face, the
full-capture floor pin, the ring_table replay); the arm scope
PRE-NAMED from exp212's deposited census (zero re-derivation): the
F1_zone_tail family's exclusion sites (excl [74] at ring 2, [74] at
ring 3, [66, 74] at ring 4, [63, 66, 74] at ring 5, [61, 63, 66, 74]
at ring 6 — the canon-value boundary cells among them admitted, the
non-boundary exclusions KEEP the fence (the composition admits ONLY
boundary cells)); exp155's disciplined junction battery (the F1
family, members per/aper, seeds (1,2,3)) the replay baseline.

GATES (each evaluated exactly once):
  GATE-P1 (the replay) exp155's F1 rows reproduce bit-exactly
           outside the armed sites (the disciplined battery's ring
           errs at the deposit's rounding; the walk's committed SET
           identical).
  GATE-P2 (the composition) per-ring errs for the armed F1 events,
           all seeds; the branch named: REPAIR (every armed ring
           err < 6.0 mV), PARTIAL (>= 1 < 6.0 and none worse than
           the disciplined baseline at that ring), NONE.
  GATE-P3 (the identity clause) every NON-armed ring's err bit-exact
           vs the replay (the composition touches only the census-
           named boundary admissions; the aper member's rings
           included).
  GATE-P4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted; the admission sets asserted ==
           exp212's deposited census (the boundary cells only).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp219_f1_composition_armed.json
RUN: python3 -m experiments.exp219_f1_composition_armed [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp219_f1_composition_armed.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
