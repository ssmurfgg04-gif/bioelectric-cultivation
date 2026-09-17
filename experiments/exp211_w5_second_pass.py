#!/usr/bin/env python3
"""exp211 — THE W5 SECOND PASS (L182's registered next).

exp206's yield is rate-limited, not knowledge-limited: 12 records
429'd at 5 retries, and the title-query protocol misses the records
whose dose identity lives in methods sections the title cannot
surface. The registered second pass: (a) the 12 429'd records
re-swept at the protocol's pacing; (b) for records still rejected,
the pre-named widened query (drug + species + phenotype terms from
the record's own fields); the acceptance predicate UNCHANGED (the
exp203 scaffold's required-field census — zero new acceptance rules).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp206's module machinery
verbatim (the merge is a pure function of the baseline row + the
sources-file extracts; the import rules as repaired at L182);
sources file 2 = results/w5_pass_sources2.json (same schema, the
second pass's extractions, provenance per field); the bank written =
results/wetlab_companion_bank_w5b.json (the w5 bank is the frozen
baseline for THIS pass).

GATES (each evaluated exactly once):
  GATE-E1 (the sweep) 119/119 records covered by the second pass
           (12 re-sweeps + the widened queries); per-record verdicts
           deposited; complete, not sampled.
  GATE-E2 (acceptance integrity) every accepted entry validates; the
           import rules from L182 enforced verbatim; zero fields
           without provenance.
  GATE-E3 (the yield) the accepted count deposited against exp206's
           0/119; the per-field fill-rate DELTAS vs the w5 bank
           deposited; the goal state named: >= 1 accepted entry.
  GATE-E4 (hygiene) the w5 bank byte-unchanged; the new bank
           deterministic; the sources file deposited.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp211_w5_second_pass.json
BANK: results/wetlab_companion_bank_w5b.json
SOURCES: results/w5_pass_sources2.json
RUN: python3 -m experiments.exp211_w5_second_pass [--smoke] [--job ...] [--out ...] [--sources ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp211_w5_second_pass.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_w5b.json")
SOURCES = os.path.join(ROOT, "results", "w5_pass_sources2.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--sources", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
