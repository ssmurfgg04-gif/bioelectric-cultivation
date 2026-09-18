#!/usr/bin/env python3
"""exp224 — THE LEVIN VOLTAGE SERIES FINAL-FORM DEPOSIT (L193's
registered next).

The corpus leg's acceptance question is CLOSED (exp217: 111
NOT-IN-LITERATURE + 8 extract-carrying rejects). The Stage 2 deposit
leg completes: the 119-entry series (research/levin_voltage_series.json)
re-exported AS the wetlab companion's final form — 111 NOT-IN-LITERATURE
rows (the absence carried with its three-pass provenance), the 8
partial rows with their per-field extracts, the census states +
provenance inline, the whole artifact self-contained for wetlab use
(the structurally-blocked corpus leg converts to a deposit, the
Section 5 registered item).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp217's deposited census
VERBATIM (the w5d bank's rows: census states, census_missing lists,
the NIL provenance naming sources 1/2/3); the series
(research/levin_voltage_series.json, 119 entries) the row base; the
FINAL FORM (pre-named, zero knobs): one JSON artifact
results/levin_voltage_series_wetlab_final.json with per-entry:
{series fields verbatim, census_state (accepted/NOT-IN-LITERATURE/
rejected-extract-carrying), census_missing list, provenance block
(exp217's, inline), the 8 partial rows' extracts verbatim}; the
counts MUST equal exp217's deposited split (0/111/8) — the export is
a projection, zero re-derivation.

GATES (each evaluated exactly once):
  GATE-Z1 (the projection) 119/119 entries exported; per-entry
           census_state == exp217's deposited verdict for that id;
           zero fields without provenance (the NIL rows carry the
           three-file provenance inline).
  GATE-Z2 (the split integrity) the exported counts == exp217's
           deposited split exactly (0 accepted / 111
           NOT-IN-LITERATURE / 8 rejected); any drift raises.
  GATE-Z3 (the wetlab self-containment) the artifact parses
           standalone; every entry carries its series identity (id,
           source, pmid_or_doi, species, region_or_tissue); the
           sha256 of the artifact + of exp217's deposit recorded in
           the export's meta.
  GATE-Z4 (hygiene) exp217's deposit byte-unchanged during the
           export; the export deterministic (re-run bit-identical).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp224_series_final_form.json
ARTIFACT: results/levin_voltage_series_wetlab_final.json
RUN: python3 -m experiments.exp224_series_final_form [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp224_series_final_form.json")
ARTIFACT = os.path.join(ROOT, "results",
                        "levin_voltage_series_wetlab_final.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
