#!/usr/bin/env python3
"""exp217 — THE NOT-IN-LITERATURE CENSUS (L191's registered next).

Three complete passes (protocol, widened, figure) prove the corpus
leg's missing W5 fields are METHOD-SECTION-DEPTH facts: 73/119 records
carry ZERO verbatim extracts across all three sources files. exp215's
deposited specification registered the honest acceptance state:
NOT-IN-LITERATURE — the absence carried with its own provenance
discipline instead of a silent reject. This run IMPLEMENTS the
specification and re-imports the 119 records under the extended
census: the corpus leg's acceptance question closes either way (the
W5 fields are in-literature, or their absence is itself the deposited
finding).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp215's deposited
not_in_literature_spec VERBATIM (the state, the provenance
discipline, the census extension); exp206's module machinery verbatim
(read_sources, w5_fills, validate_row, ser, sha256 helpers); the
THREE sources files (w5_pass_sources.json, w5_pass_sources2.json,
w5_pass_sources3.json) each sha256'd IN the deposit; the w5c bank the
frozen baseline; the new bank written =
results/wetlab_companion_bank_w5d.json. THE EXTENSION (additive,
disclosed, zero knobs): census_missing is extended IN THIS MODULE
(exp203's file untouched) by the not_in_literature clause — a record
whose missing FILL_FIELDS have ZERO extracts across all three passes
is admissible to the state census_state='NOT-IN-LITERATURE' with the
missing field list; every other acceptance rule unchanged.

GATES (each evaluated exactly once):
  GATE-N1 (the evidence check) 119/119 records carry a verdict; the
           three sources files complete (119 records each); each
           file's sha256 in the deposit.
  GATE-N2 (the zero-extract assertion) every record admitted to
           NOT-IN-LITERATURE has zero extracts in ALL THREE passes
           for EVERY missing field; any record with an extract for a
           missing field is NOT admissible (the discipline holds).
  GATE-N3 (the split) n_normal_accepted + n_not_in_literature +
           n_rejected = 119; ALL of exp215's 73 zero-extract records
           land NOT-IN-LITERATURE or better; the realized counts
           deposited; the branch named: CLOSED-NIL (>= 73 land in
           the state and zero integrity violations) / PARTIAL.
  GATE-N4 (hygiene) the w5b and w5c banks byte-unchanged; the new
           bank deterministic (merge re-run bit-identical); zero
           fields without provenance.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp217_not_in_literature_census.json
BANK: results/wetlab_companion_bank_w5d.json
RUN: python3 -m experiments.exp217_not_in_literature_census [--smoke] [--job ...] [--out ...]
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
                   "exp217_not_in_literature_census.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_w5d.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
