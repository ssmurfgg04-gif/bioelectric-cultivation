#!/usr/bin/env python3
"""exp206 — THE W5 DOSE-IDENTITY LITERATURE PASS (L176's registered
next).

L176's census: the wetlab companion bank's first candidate deposit
(the 119-entry Levin voltage series) is 0/119 accepted — the
protocol's W5 dose-identity columns (concentration, blocker,
phenotype, n) are the missing material, quantified per row. The
registered pass: a targeted literature sweep that fills W5 per
record, one entry at a time, the exp203 scaffold validating on
acceptance.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: results/exp203_wetlab_scaffold
's scaffold + validator VERBATIM (the acceptance predicate IS the
scaffold's required-field census — zero new acceptance rules);
results/wetlab_companion_bank.json is the bank (read, never
rewritten — the pass writes to a NEW bank file, the original is the
frozen baseline); the search protocol per record (pre-named, zero
knobs): the record's own title/authors/year/name fields form the
query; each candidate source's fields are copied ONLY when the source
states them verbatim (no inference, no unit conversion beyond the
protocol's declared units); every accepted field carries source
provenance (url + retrieved date); unresolvable records stay
rejected with their census reasons.

GATES (each evaluated exactly once):
  GATE-D1 (the pass runs) all 119 records swept; per-record verdicts
           (accepted / still-rejected + reasons + sources-tried)
           deposited; the sweep is complete, not sampled.
  GATE-D2 (acceptance integrity) every accepted entry validates
           through the exp203 scaffold's validator; every accepted
           W5 field carries source provenance; zero fields without
           provenance.
  GATE-D3 (the yield — the finding) the accepted count deposited
           against the 0/119 baseline; the per-field fill rates
           (concentration / blocker / phenotype / n) deposited; the
           still-rejected list carries the reasons.
  GATE-D4 (hygiene) the frozen baseline bank byte-unchanged; the new
           bank deterministic (re-run reproduces it byte-identically
           given the same sources file); the sources file (per-record
           raw extracts) deposited alongside.
NO post-hoc tuning. --smoke permitted (records 0-4), discarded.
DEPOSIT: results/exp206_w5_dose_pass.json
BANK: results/wetlab_companion_bank_w5.json
SOURCES: results/w5_pass_sources.json
RUN: python3 -m experiments.exp206_w5_dose_pass [--smoke] [--job ...] [--out ...] [--sources ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp206_w5_dose_pass.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_w5.json")
SOURCES = os.path.join(ROOT, "results", "w5_pass_sources.json")


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
