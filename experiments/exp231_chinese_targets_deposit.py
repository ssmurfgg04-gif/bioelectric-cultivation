#!/usr/bin/env python3
"""exp231 — THE CHINESE-TARGETS GATES DEPOSIT (L201's registered
next; the Section 5 item).

The last open deposit leg: the Chinese literature targets — the
scaffold exists (experiments/scaffold_chinese_targets.py, gates
drafted) and the deposit converts it to the wetlab companion's final
form: the drafted gates exported as a self-contained, provenance-
carrying deposit the wetlab side can execute without the stack.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: experiments/
scaffold_chinese_targets.py's deposited machinery VERBATIM (its gate
definitions, its target fields); exp224's final-form discipline
VERBATIM (the projection gates: per-entry identity, split integrity,
self-containment, determinism); the artifact written =
results/chinese_targets_gates_deposit.json.

GATES (each evaluated exactly once):
  GATE-C1 (the projection) every drafted target exported with its
           gate fields verbatim from the scaffold's definitions;
           zero fields without provenance (the scaffold's own
           source references inline).
  GATE-C2 (the split integrity) the exported counts == the
           scaffold's deposited counts exactly; any drift raises.
  GATE-C3 (the self-containment) the artifact parses standalone;
           every entry carries its identity fields; the sha256 of
           the artifact + of the scaffold's own deposit (if any)
           recorded in the export's meta.
  GATE-C4 (hygiene) the scaffold's files byte-unchanged during the
           export; the export deterministic (re-run bit-identical).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp231_chinese_targets_deposit.json
ARTIFACT: results/chinese_targets_gates_deposit.json
RUN: python3 -m experiments.exp231_chinese_targets_deposit [--smoke] [--job ...] [--out ...]
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
                   "exp231_chinese_targets_deposit.json")
ARTIFACT = os.path.join(ROOT, "results",
                        "chinese_targets_gates_deposit.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
