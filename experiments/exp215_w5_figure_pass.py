#!/usr/bin/env python3
"""exp215 — THE W5 FIGURE-PASS (L184's registered next).

exp211's second pass completed the sweep (119/119) and moved the
yield (concentration_mM 2 -> 5) but acceptance stands 0/119 — the
census needs fields no title/widened query surfaces. L184's registered
third pass is STRUCTURE-DRIVEN, not query-driven: (a) query by the
record's FIGURE/PANEL identity (db_experiment_id + db_figure_panel
name the exact experiment the literature describes); (b) if the
figure-pass also yields zero full censuses, the honest alternative
registers: a record whose W5 fields are stated NOWHERE becomes an
explicit NOT-IN-LITERATURE deposit (a new acceptance state the exp203
census does not yet have — the registered validator extension,
evaluated ONLY if the figure-pass yields zero full censuses).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp206/exp211's module
machinery verbatim (the merge, the validator, the import rules as
repaired at L182/L184); sources file 3 = results/w5_pass_sources3.json
(the figure-pass's extractions, same schema); the bank written =
results/wetlab_companion_bank_w5c.json (the w5b bank is the frozen
baseline for THIS pass); the figure queries pre-named: per record,
"{source} {db_figure_panel} {species}" + "{db_experiment_id}
{figure_panel}" variants.

GATES (each evaluated exactly once):
  GATE-F1 (the sweep) 119/119 covered by the figure-pass; per-record
           verdicts deposited; complete, not sampled.
  GATE-F2 (acceptance integrity) every accepted entry validates; the
           L182/L184 import rules verbatim; zero fields without
           provenance.
  GATE-F3 (the yield) the accepted count vs exp211's 0/119; the
           per-field fill-rate deltas vs the w5b bank; the branch:
           ACCEPTED (>= 1) / the validator extension REGISTERED (0
           full censuses across three passes -> the NOT-IN-LITERATURE
           state's specification deposited as the registered repair,
           the exp203 census extended with an explicit
           absent-from-literature verdict carrying its own provenance
           discipline).
  GATE-F4 (hygiene) the w5b bank byte-unchanged; the new bank
           deterministic; the sources file deposited.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp215_w5_figure_pass.json
BANK: results/wetlab_companion_bank_w5c.json
SOURCES: results/w5_pass_sources3.json
RUN: python3 -m experiments.exp215_w5_figure_pass [--smoke] [--job ...] [--out ...] [--sources ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp215_w5_figure_pass.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_w5c.json")
SOURCES = os.path.join(ROOT, "results", "w5_pass_sources3.json")


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
