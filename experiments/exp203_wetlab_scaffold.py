#!/usr/bin/env python3
"""exp203 — THE WETLAB COMPANION DEPOSIT SCAFFOLD (L170's registered
next).

L170's two-sided closure: the corpus leg is STRUCTURALLY BLOCKED (the
bank carries no programs, the decode emits none, the upstream holds
none) — Stage 5's EMPIRICAL transfer leg moves to the wetlab
companion protocol's deposit format (docs/
STAGE5_WETLAB_COMPANION_PROTOCOL.md). This run builds the scaffold:
the schema read from the protocol, the bank format implemented, and
the FIRST deposit imported — the Levin voltage series (exp139's
119-entry deposit) — validated end to end.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: the protocol doc is the ONLY
schema source (zero improvised fields — every bank field traces to a
protocol line, the field-provenance table deposited); the import
source is results/exp139_levin_voltage.json (its own entry count
asserted == 119); jsonschema-style validation implemented in-module
(no new dependency).

GATES (each evaluated exactly once):
  GATE-S1 (schema) the protocol read; the bank scaffold built with
           the field-provenance table (bank field -> protocol line)
           deposited; zero fields without provenance; the schema
           validates the scaffold's empty bank.
  GATE-S2 (import) the Levin series imported: 119/119 entries, each
           with its protocol-required fields populated and per-entry
           provenance (source deposit key + sha256 of the source
           record); entries failing the protocol's required-field
           census are deposited on the reject list (the reject count
           is a FINDING, not a gate failure — the gate is that every
           accepted entry validates).
  GATE-S3 (round-trip) write/read-back byte-identical on the full
           bank; the validator accepts every round-tripped entry and
           rejects a mutated probe (one field corrupted per probe x
           every required field — the negative controls all fail).
  GATE-S4 (hygiene) no source deposit mutated; the bank written
           under results/ with a deterministic filename; the run is
           idempotent (re-run reproduces the bank byte-identically).
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp203_wetlab_scaffold.json
BANK: results/wetlab_companion_bank.json
RUN: python3 -m experiments.exp203_wetlab_scaffold [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp203_wetlab_scaffold.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
