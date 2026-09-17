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
import hashlib
import json
import os
import re
import sys
import traceback

# thread hygiene (set before any numeric lib import; this module is stdlib
# plus experiments.planform_mining only)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp203_wetlab_scaffold.json")
BANK = os.path.join(ROOT, "results", "wetlab_companion_bank.json")
SMOKE_OUT = os.path.join(ROOT, "results", "exp203_wetlab_scaffold_smoke.json")
SMOKE_BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_smoke.json")

PROTOCOL = os.path.join(ROOT, "docs", "STAGE5_WETLAB_COMPANION_PROTOCOL.md")
EXP139 = os.path.join(ROOT, "results", "exp139_levin_voltage.json")
SERIES = os.path.join(ROOT, "research", "levin_voltage_series.json")
EXP39 = os.path.join(ROOT, "results", "exp39_levin_voltage.json")

N_ENTRIES = 119  # pre-registered: exp139's own entry count, asserted

from experiments.planform_mining import plane_of_manipulation  # noqa: E402

# ======================================================================
# THE SCHEMA — read from docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md, the
# ONLY schema source.  The W5 deposit schema (L334-336) names seven
# required row columns (L338-344) and four extended columns (L346-348),
# keyed to the planform_mining.py plane / drug taxonomy (L335).  Every
# bank field below traces to a protocol line via FIELD_PROVENANCE;
# zero improvised fields.
# ======================================================================

REQUIRED_FIELDS = [
    "species",                                    # L338
    "blocker", "vehicle",                         # L339
    "concentration_mM", "concentration_frac_c_full",  # L340
    "exposure_window_start_rel_amputation",       # L341
    "exposure_window_end_rel_amputation",         # L341
    "exposure_mode",                              # L341
    "amputation_plane",                           # L342
    "phenotype_score",                            # L343
    "n",                                          # L344
]
EXTENDED_FIELDS = [                              # L346-348
    "dye_coupling_fraction",
    "rig_calibration_constants",
    "blocker_batch",
    "blind_scoring_rubric_version",
]
PROVENANCE_FIELDS = ["source_deposit", "source_record", "source_key",
                     "source_record_sha256"]     # L335-336 (keyed/re-runnable)
ROW_FIELDS = REQUIRED_FIELDS + EXTENDED_FIELDS + ["provenance"]

# planform_mining.py plane taxonomy (pre-registered 2026-09-15; the
# protocol keys the deposit schema to it, L335)
PLANES = frozenset({"head", "tail", "head_tail", "trunk", "crosspiece",
                    "graft", "irr", "lateral", "generic", "none"})
EXPOSURE_MODES = frozenset({"sustained", "pulse"})

# the protocol's required-field census (GATE-S2): the seven schema
# bullets of L338-344, each of which must be populated for a row to be
# ACCEPTED; rows failing the census are deposited on the reject list
# (the reject count is a FINDING, not a gate failure).
CENSUS_RULE = [
    {"item": "species", "fields": ["species"],
     "rule": "non-null"},
    {"item": "blocker_or_vehicle", "fields": ["blocker", "vehicle"],
     "rule": "at least one non-null (L339 'blocker (and vehicle)')"},
    {"item": "concentration", "fields": ["concentration_mM",
                                         "concentration_frac_c_full"],
     "rule": "at least one non-null (L340 'mM, and fraction of C_full')"},
    {"item": "exposure_window",
     "fields": ["exposure_window_start_rel_amputation",
                "exposure_window_end_rel_amputation", "exposure_mode"],
     "rule": "(start AND end non-null) OR mode non-null (L341 offers "
             "start/end or the sustained-or-pulse mode encoding)"},
    {"item": "amputation_plane", "fields": ["amputation_plane"],
     "rule": "non-null"},
    {"item": "phenotype_score", "fields": ["phenotype_score"],
     "rule": "non-null (a Durant-rubric penetrance; structure layer "
             "constrains it to [0,1])"},
    {"item": "n", "fields": ["n"], "rule": "non-null"},
]

# ---- field-provenance table: bank field -> protocol line --------------
# quotes are verified against the protocol file at run time (GATE-S1).
_L334 = ("**The deposit schema.** Machine-readable (CSV + JSON), keyed to "
         "PlanformDB's")
_L335_336 = ("experiment schema (the `planform_mining.py` plane / drug "
             "taxonomy) so the exp92 row-level mapping can be re-run with "
             "measured doses:")
_L338_344 = ("- species - blocker (and vehicle) - concentration (mM, and "
             "fraction of C_full) - exposure window (start / end relative "
             "to amputation; sustained or pulse) - amputation plane "
             "(pre-pharyngeal / trunk / post-pharyngeal) - phenotype score "
             "(Durant-database rubric, plane-resolved penetrance) - n")
_L346_348 = ("Extended columns per row: measured dye-coupling fraction (the "
             "functional dial), the rig's intensity->mV calibration "
             "constants, blocker batch, and the blind-scoring rubric "
             "version. Deposited with the publication (supplementary")
_L11_13 = ("**Ledger discipline:** every section is a pre-registered "
           "prediction with an explicit pass/fail gate, registered before "
           "the first animal is dosed. A failed gate is REPORTED, not "
           "iterated past — the FALSIFICATION.md discipline applies")

FIELD_PROVENANCE = [
    # -- bank envelope -------------------------------------------------
    {"field": "bank", "protocol_line": "L334", "quote": _L334},
    {"field": "protocol", "protocol_line": "L313",
     "quote": "## 5. W5 — THE RECORD PROPERTY (what the dosing table adds "
              "back)"},
    {"field": "protocol_sha256", "protocol_line": "L334-L336",
     "quote": _L334 + " " + _L335_336},
    {"field": "schema_version", "protocol_line": "L334-L336",
     "quote": _L334 + " " + _L335_336},
    {"field": "field_provenance", "protocol_line": "L335",
     "quote": "experiment schema (the `planform_mining.py` plane / drug "
              "taxonomy) so the"},
    {"field": "required_fields", "protocol_line": "L338-L344",
     "quote": _L338_344},
    {"field": "extended_fields", "protocol_line": "L346-L348",
     "quote": _L346_348},
    {"field": "census_rule", "protocol_line": "L338-L344",
     "quote": _L338_344},
    {"field": "import_source", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "import_rules", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "entries", "protocol_line": "L329",
     "quote": "Every W1/W2/W3 animal contributes one row with the measured "
              "dose identity"},
    {"field": "rejects", "protocol_line": "L11-L13", "quote": _L11_13},
    {"field": "counts", "protocol_line": "L338-L344", "quote": _L338_344},
    # -- required row columns (the seven W5 schema bullets) -------------
    {"field": "species", "protocol_line": "L338", "quote": "- species"},
    {"field": "blocker", "protocol_line": "L339",
     "quote": "- blocker (and vehicle)"},
    {"field": "vehicle", "protocol_line": "L339",
     "quote": "- blocker (and vehicle)"},
    {"field": "concentration_mM", "protocol_line": "L340",
     "quote": "- concentration (mM, and fraction of C_full)"},
    {"field": "concentration_frac_c_full", "protocol_line": "L340",
     "quote": "- concentration (mM, and fraction of C_full)"},
    {"field": "exposure_window_start_rel_amputation", "protocol_line": "L341",
     "quote": "- exposure window (start / end relative to amputation; "
              "sustained or pulse)"},
    {"field": "exposure_window_end_rel_amputation", "protocol_line": "L341",
     "quote": "- exposure window (start / end relative to amputation; "
              "sustained or pulse)"},
    {"field": "exposure_mode", "protocol_line": "L341",
     "quote": "- exposure window (start / end relative to amputation; "
              "sustained or pulse)"},
    {"field": "amputation_plane", "protocol_line": "L342",
     "quote": "- amputation plane (pre-pharyngeal / trunk / "
              "post-pharyngeal)"},
    {"field": "phenotype_score", "protocol_line": "L343",
     "quote": "- phenotype score (Durant-database rubric, plane-resolved "
              "penetrance)"},
    {"field": "n", "protocol_line": "L344", "quote": "- n"},
    # -- extended columns (L346-348) ------------------------------------
    {"field": "dye_coupling_fraction", "protocol_line": "L346",
     "quote": "Extended columns per row: measured dye-coupling fraction "
              "(the functional"},
    {"field": "rig_calibration_constants", "protocol_line": "L346-L347",
     "quote": "Extended columns per row: measured dye-coupling fraction "
              "(the functional dial), the rig's intensity->mV calibration "
              "constants, blocker batch, and the"},
    {"field": "blocker_batch", "protocol_line": "L347",
     "quote": "dial), the rig's intensity->mV calibration constants, "
              "blocker batch, and the"},
    {"field": "blind_scoring_rubric_version", "protocol_line": "L347-L348",
     "quote": "dial), the rig's intensity->mV calibration constants, "
              "blocker batch, and the blind-scoring rubric version. "
              "Deposited with the publication (supplementary"},
    # -- per-entry provenance (L335-336: the keyed, re-runnable mapping) -
    {"field": "provenance", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "provenance.source_deposit", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "provenance.source_record", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "provenance.source_key", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "provenance.source_record_sha256", "protocol_line": "L335-L336",
     "quote": _L335_336},
    {"field": "census_missing", "protocol_line": "L338-L344",
     "quote": _L338_344},
]

# hard-coded expected protocol lines (GATE-S1 verifies the file still
# carries exactly these at the cited line numbers)
_EXPECTED_LINES = {
    11: "**Ledger discipline:** every section is a pre-registered prediction with an",
    12: "explicit pass/fail gate, registered before the first animal is dosed. A failed",
    13: "gate is REPORTED, not iterated past — the FALSIFICATION.md discipline applies",
    313: "## 5. W5 — THE RECORD PROPERTY (what the dosing table adds back)",
    329: "Every W1/W2/W3 animal contributes one row with the measured dose identity",
    334: "**The deposit schema.** Machine-readable (CSV + JSON), keyed to PlanformDB's",
    335: "experiment schema (the `planform_mining.py` plane / drug taxonomy) so the",
    336: "exp92 row-level mapping can be re-run with measured doses:",
    338: "- species",
    339: "- blocker (and vehicle)",
    340: "- concentration (mM, and fraction of C_full)",
    341: "- exposure window (start / end relative to amputation; sustained or pulse)",
    342: "- amputation plane (pre-pharyngeal / trunk / post-pharyngeal)",
    343: "- phenotype score (Durant-database rubric, plane-resolved penetrance)",
    344: "- n",
    346: "Extended columns per row: measured dye-coupling fraction (the functional",
    347: "dial), the rig's intensity->mV calibration constants, blocker batch, and the",
    348: "blind-scoring rubric version. Deposited with the publication (supplementary",
}

# ---- helpers -----------------------------------------------------------

def _norm(s: str) -> str:
    return " ".join(s.split())


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def ser(obj) -> str:
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False)


def _is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)

# ---- validators (jsonschema-style, in-module, no new dependency) -------

def validate_row(row, allow_census_missing: bool = False) -> list:
    """Structure layer: all slots present, correct types/enums/ranges.
    Nulls are allowed on every value slot (an unpopulated slot is a
    census finding, not a structural violation)."""
    errs = []
    if not isinstance(row, dict):
        return ["row: not an object"]
    allowed = set(ROW_FIELDS) | ({"census_missing"} if allow_census_missing
                                 else set())
    for k in sorted(set(row) - allowed):
        errs.append(f"unexpected key: {k}")
    for k in ROW_FIELDS:
        if k not in row:
            errs.append(f"missing required key: {k}")
    if errs:
        return errs
    v = row["species"]
    if v is not None and (not isinstance(v, str) or not v.strip()):
        errs.append("species: must be a non-empty string or null")
    for k in ("blocker", "vehicle", "blocker_batch",
              "blind_scoring_rubric_version"):
        v = row[k]
        if v is not None and (not isinstance(v, str) or not v.strip()):
            errs.append(f"{k}: must be a non-empty string or null")
    v = row["concentration_mM"]
    if v is not None and (not _is_num(v) or v <= 0):
        errs.append("concentration_mM: must be a number > 0 or null")
    v = row["concentration_frac_c_full"]
    if v is not None and (not _is_num(v) or not (0.0 <= v <= 1.0)):
        errs.append("concentration_frac_c_full: must be a number in [0,1] "
                    "or null")
    for k in ("exposure_window_start_rel_amputation",
              "exposure_window_end_rel_amputation"):
        v = row[k]
        if v is not None and not _is_num(v):
            errs.append(f"{k}: must be a number or null")
    v = row["exposure_mode"]
    if v is not None and v not in EXPOSURE_MODES:
        errs.append("exposure_mode: must be 'sustained' or 'pulse' or null")
    v = row["amputation_plane"]
    if v is not None and v not in PLANES:
        errs.append(f"amputation_plane: {v!r} not in the planform_mining.py "
                    f"plane taxonomy")
    v = row["phenotype_score"]
    if v is not None and (not _is_num(v) or not (0.0 <= v <= 1.0)):
        errs.append("phenotype_score: must be a number in [0,1] or null")
    v = row["n"]
    if v is not None and (not isinstance(v, int) or isinstance(v, bool)
                          or v < 1):
        errs.append("n: must be an integer >= 1 or null")
    v = row["dye_coupling_fraction"]
    if v is not None and (not _is_num(v) or not (0.0 <= v <= 1.0)):
        errs.append("dye_coupling_fraction: must be a number in [0,1] or "
                    "null")
    v = row["rig_calibration_constants"]
    if v is not None and not isinstance(v, dict):
        errs.append("rig_calibration_constants: must be an object or null")
    p = row["provenance"]
    if not isinstance(p, dict):
        errs.append("provenance: must be an object")
    else:
        for k in PROVENANCE_FIELDS:
            if k not in p:
                errs.append(f"provenance: missing {k}")
        if "source_deposit" in p and (not isinstance(p["source_deposit"], str)
                                      or not p["source_deposit"].strip()):
            errs.append("provenance.source_deposit: must be a non-empty "
                        "string")
        if "source_record" in p and (not isinstance(p["source_record"], str)
                                     or not p["source_record"].strip()):
            errs.append("provenance.source_record: must be a non-empty "
                        "string")
        if "source_key" in p and (not isinstance(p["source_key"], str)
                                  or not p["source_key"].strip()):
            errs.append("provenance.source_key: must be a non-empty string")
        srsha = p.get("source_record_sha256")
        if not isinstance(srsha, str) or not re.fullmatch(r"[0-9a-f]{64}",
                                                         srsha):
            errs.append("provenance.source_record_sha256: must be a 64-hex "
                        "sha256")
    return errs


def census_missing(row) -> list:
    """The protocol's required-field census (L338-344): which of the
    seven schema bullets are unpopulated on this row."""
    missing = []
    for item in CENSUS_RULE:
        flds = item["fields"]
        vals = [row.get(f) for f in flds]
        if item["item"] == "exposure_window":
            ok = (vals[0] is not None and vals[1] is not None) \
                or vals[2] is not None
        else:
            ok = any(v is not None for v in vals)
        if not ok:
            missing.append(item["item"])
    return missing


def validate_bank(bank) -> list:
    errs = []
    if not isinstance(bank, dict):
        return ["bank: not an object"]
    envelope = ["bank", "protocol", "protocol_sha256", "schema_version",
                "field_provenance", "required_fields", "extended_fields",
                "census_rule", "import_source", "import_rules", "entries",
                "rejects", "counts"]
    for k in envelope:
        if k not in bank:
            errs.append(f"bank: missing envelope key {k}")
    if errs:
        return errs
    if bank["bank"] != "wetlab_companion":
        errs.append("bank: bad bank name")
    if not re.fullmatch(r"[0-9a-f]{64}", bank["protocol_sha256"]):
        errs.append("bank: protocol_sha256 not 64-hex")
    if bank["required_fields"] != REQUIRED_FIELDS:
        errs.append("bank: required_fields drift")
    if bank["extended_fields"] != EXTENDED_FIELDS:
        errs.append("bank: extended_fields drift")
    if bank["census_rule"] != CENSUS_RULE:
        errs.append("bank: census_rule drift")
    for i, e in enumerate(bank["entries"]):
        for err in validate_row(e, allow_census_missing=False):
            errs.append(f"entries[{i}]: {err}")
        if e.get("census_missing"):
            errs.append(f"entries[{i}]: accepted row carries census_missing")
    for i, r in enumerate(bank["rejects"]):
        for err in validate_row(r, allow_census_missing=True):
            errs.append(f"rejects[{i}]: {err}")
        if not r.get("census_missing"):
            errs.append(f"rejects[{i}]: census_missing empty on a reject")
    c = bank["counts"]
    if (c.get("imported") != len(bank["entries"]) + len(bank["rejects"])
            or c.get("accepted") != len(bank["entries"])
            or c.get("rejected") != len(bank["rejects"])):
        errs.append("bank: counts inconsistent with entries/rejects")
    return errs


def bank_field_coverage(bank) -> list:
    """Zero fields without provenance: every SCHEMA field position in the
    bank — the envelope keys, each row's slots and provenance sub-fields,
    the provenance-table row keys, the census-rule keys, and the
    import-rule keys — must appear in the field-provenance table.
    Deposited payload data (the import anchor's own metadata, counts
    sub-keys, values inside source-derived content) is data, not schema
    fields; the protocol cannot name the task's import source."""
    known = {r["field"] for r in bank["field_provenance"]}
    missing = []
    for k in bank:
        if k not in known:
            missing.append(f"envelope:{k}")
    for label, rows in (("entry", bank.get("entries", [])),
                        ("reject", bank.get("rejects", []))):
        for i, r in enumerate(rows):
            for k in r:
                if k not in known:
                    missing.append(f"{label}[{i}]:{k}")
            p = r.get("provenance", {})
            if isinstance(p, dict):
                for k in p:
                    if f"provenance.{k}" not in known:
                        missing.append(f"{label}[{i}]:provenance.{k}")
    for i, row in enumerate(bank.get("field_provenance", [])):
        for k in row:
            if k not in ("field", "protocol_line", "quote"):
                missing.append(f"field_provenance[{i}]:{k}")
    for i, row in enumerate(bank.get("census_rule", [])):
        for k in row:
            if k not in ("item", "fields", "rule"):
                missing.append(f"census_rule[{i}]:{k}")
    for k in bank.get("import_rules", {}):
        if k not in known:
            missing.append(f"import_rules:{k}")
    return sorted(set(missing))

# ======================================================================
# THE IMPORT — the first deposit: exp139's 119-entry Levin voltage
# series.  Import anchor: results/exp139_levin_voltage.json (its own
# entry count asserted == 119); the series records live at the deposit
# its sources.record line points to:
# research/levin_voltage_series.json#series.
# ======================================================================

IMPORT_RULES = {
    "species": "verbatim source record 'species' (119/119 non-null in the "
               "series)",
    "blocker": "'; '-joined drug names from the record's drug_start_end "
               "tuples (PlanformDB ExperimentDrug names via the series; "
               "the protocol's keyed drug taxonomy, L335); null when the "
               "record states no drugs (no drug_start_end field, an "
               "empty list, or RNAi-only/cutting-only rows)",
    "vehicle": "null — no structured vehicle field exists in the source "
               "deposit",
    "concentration_mM": "null — the source deposit carries no concentration "
                        "anywhere (exp33/L16: PlanformDB has no drug "
                        "concentrations; re-verified by exp197). This "
                        "column is the record hole the wetlab companion "
                        "exists to fill",
    "concentration_frac_c_full": "null — same absence as concentration_mM",
    "exposure_window_start_rel_amputation":
        "min over the record's drug_start_end tuples of position 1 "
        "(StartTime), verbatim uninterpreted",
    "exposure_window_end_rel_amputation":
        "max over the record's drug_start_end tuples of position 2 "
        "(EndTime), verbatim uninterpreted (StartTime/EndTime semantics "
        "are the source deposit's own; e.g. EndTime 0.0 is deposited "
        "as recorded)",
    "exposure_mode": "null — not stated per-row in the structured source",
    "amputation_plane":
        "plane_of_manipulation(record['region_or_tissue'])['plane'] — the "
        "protocol's keyed plane taxonomy (L335; rules pre-registered "
        "2026-09-15 in experiments/planform_mining.py), applied verbatim",
    "phenotype_score":
        "1 - sum(frequency for outcome_frequencies entries whose outcome "
        "== 'Wild type') — the record's pre-registered abnormal rule "
        "(exp21: abnormal(E) = 1 - freq(Wild type); exp139's deposited "
        "reading of the same rows); null when the record states no "
        "outcome frequencies",
    "n": "n_if_stated verbatim when it is an integer >= 1, else null "
         "(non-integer or non-positive source values are unmappable to "
         "the schema's n and are left unpopulated; the exact source "
         "record is recoverable via provenance.source_record_sha256)",
    "dye_coupling_fraction": "null — not stated in the source deposit "
                             "(extended column, L346)",
    "rig_calibration_constants": "null — not stated in the source deposit "
                                 "(extended column, L346-347)",
    "blocker_batch": "null — not stated in the source deposit (extended "
                     "column, L347)",
    "blind_scoring_rubric_version": "null — not stated in the source "
                                    "deposit (extended column, L347-348)",
    "provenance": "source_deposit = the task's named import source "
                  "(results/exp139_levin_voltage.json); source_record = "
                  "the series deposit its sources.record line points to "
                  "(research/levin_voltage_series.json#series); "
                  "source_key = the record's own id; "
                  "source_record_sha256 = sha256 of the canonical JSON of "
                  "the exact source record",
}


def map_entry(e: dict) -> dict:
    dse = e.get("drug_start_end") or []
    if dse:
        blocker = "; ".join(t[0] for t in dse)
        w_start = min(t[1] for t in dse)
        w_end = max(t[2] for t in dse)
    else:
        blocker = w_start = w_end = None
    of = e.get("outcome_frequencies")
    if of:
        score = 1.0 - sum(f["frequency"] for f in of
                          if f["outcome"] == "Wild type")
        if not (_is_num(score) and 0.0 <= score <= 1.0):
            score = None
    else:
        score = None
    nsrc = e.get("n_if_stated")
    n = nsrc if (isinstance(nsrc, int) and not isinstance(nsrc, bool)
                 and nsrc >= 1) else None
    row = {
        "species": e.get("species"),
        "blocker": blocker,
        "vehicle": None,
        "concentration_mM": None,
        "concentration_frac_c_full": None,
        "exposure_window_start_rel_amputation": w_start,
        "exposure_window_end_rel_amputation": w_end,
        "exposure_mode": None,
        "amputation_plane": plane_of_manipulation(
            e.get("region_or_tissue"))["plane"],
        "phenotype_score": score,
        "n": n,
        "dye_coupling_fraction": None,
        "rig_calibration_constants": None,
        "blocker_batch": None,
        "blind_scoring_rubric_version": None,
        "provenance": {
            "source_deposit": "results/exp139_levin_voltage.json",
            "source_record": "research/levin_voltage_series.json#series",
            "source_key": e["id"],
            "source_record_sha256": sha256_obj(e),
        },
    }
    assert not validate_row(row), validate_row(row)
    return row


def read_import_anchor() -> dict:
    """exp139's own entry count asserted == 119, then the series deposit
    its sources.record line points to read and its length asserted."""
    with open(EXP139, "r", encoding="utf-8") as f:
        d139 = json.load(f)
    assert d139["exp"] == "exp139_levin_voltage"
    assert d139["gates"]["LV_A1"]["partition_total"] == N_ENTRIES, \
        d139["gates"]["LV_A1"]["partition_total"]
    counts = d139["partition"]["counts"]
    assert sum(counts.values()) == N_ENTRIES, counts
    m = re.match(r"^([^\s(]+)\s*\((\d+) entries\)$", d139["sources"]["record"])
    assert m, d139["sources"]["record"]
    assert int(m.group(2)) == N_ENTRIES, m.group(2)
    assert m.group(1) == "research/levin_voltage_series.json", m.group(1)
    with open(SERIES, "r", encoding="utf-8") as f:
        sdoc = json.load(f)
    series = sdoc["series"]
    assert len(series) == N_ENTRIES, len(series)
    assert sdoc["counts"]["total_entries"] == N_ENTRIES
    return {
        "deposit": "results/exp139_levin_voltage.json",
        "deposit_sha256": sha256_file(EXP139),
        "exp139_partition_total": d139["gates"]["LV_A1"]["partition_total"],
        "exp139_partition_counts": counts,
        "exp139_sources_record": d139["sources"]["record"],
        "series_file": "research/levin_voltage_series.json",
        "series_sha256": sha256_file(SERIES),
        "series_len": len(series),
        "series_counts": sdoc["counts"],
        "exp39_reference": ("the series protocol names "
                            "results/exp39_levin_voltage.json among its "
                            "mining sources (the V1-V6 direction-match "
                            "pairs); the file is untracked in git, hashed "
                            "for hygiene when present"),
    }


def run_pipeline() -> tuple:
    """Pure: reads the sources, imports the series, returns the full bank
    plus the run context.  No writes, no clock, no randomness."""
    protocol_lines = None
    hashes = {}
    for label, path in (("protocol", PROTOCOL), ("exp139", EXP139),
                        ("series", SERIES)):
        hashes[label] = {"path": os.path.relpath(path, ROOT),
                         "sha256": sha256_file(path), "present": True}
    hashes["exp39"] = (
        {"path": "results/exp39_levin_voltage.json",
         "sha256": sha256_file(EXP39), "present": True}
        if os.path.exists(EXP39) else
        {"path": "results/exp39_levin_voltage.json", "sha256": None,
         "present": False})
    with open(PROTOCOL, "r", encoding="utf-8") as f:
        protocol_lines = f.read().splitlines()
    anchor = read_import_anchor()
    with open(SERIES, "r", encoding="utf-8") as f:
        series = json.load(f)["series"]
    rows = [map_entry(e) for e in series]
    entries, rejects = [], []
    for row in rows:
        cm = census_missing(row)
        if cm:
            rejects.append(dict(row, census_missing=cm))
        else:
            entries.append(row)
    bank = {
        "bank": "wetlab_companion",
        "protocol": "docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md",
        "protocol_sha256": hashes["protocol"]["sha256"],
        "schema_version": "1.0",
        "field_provenance": FIELD_PROVENANCE,
        "required_fields": list(REQUIRED_FIELDS),
        "extended_fields": list(EXTENDED_FIELDS),
        "census_rule": CENSUS_RULE,
        "import_source": anchor,
        "import_rules": IMPORT_RULES,
        "entries": entries,
        "rejects": rejects,
        "counts": {"imported": len(rows), "accepted": len(entries),
                   "rejected": len(rejects)},
    }
    ctx = {"hashes": hashes, "protocol_lines": protocol_lines,
           "anchor": anchor, "rows": rows, "series": series}
    return bank, ctx

# ======================================================================
# G3 probe fixture — a SYNTHETIC census-valid row (a W5-shaped wetlab
# row), NOT a bank row and not derived from any source deposit.  It
# exists so the validator's accept path and the negative controls
# (one field corrupted per probe x every required field) are
# non-vacuous regardless of the import's accepted count.
# ======================================================================

_FIXTURE_VALUES = {
    "species": "Schmidtea mediterranea",
    "blocker": "Octanol",
    "vehicle": None,
    "concentration_mM": 1.0,
    "concentration_frac_c_full": 0.5,
    "exposure_window_start_rel_amputation": 0.0,
    "exposure_window_end_rel_amputation": 14.0,
    "exposure_mode": "sustained",
    "amputation_plane": "tail",
    "phenotype_score": 0.5,
    "n": 30,
    "dye_coupling_fraction": None,
    "rig_calibration_constants": None,
    "blocker_batch": None,
    "blind_scoring_rubric_version": None,
}
_FIXTURE = dict(_FIXTURE_VALUES,
                provenance={
                    "source_deposit":
                        "synthetic G3 probe fixture — not a source deposit",
                    "source_record":
                        "experiments/exp203_wetlab_scaffold.py#_FIXTURE",
                    "source_key": "fixture-001",
                    "source_record_sha256":
                        sha256_obj(_FIXTURE_VALUES)})

# one field corrupted per probe x every required field; each corruption
# makes the probe invalid at the structure layer or (for uniquely
# load-bearing slots corrupted to null) at the census layer
_CORRUPTIONS = {
    "species": None,                                  # census fail
    "blocker": None,                                  # census fail (vehicle null)
    "vehicle": 123,                                   # type fail
    "concentration_mM": -1.0,                         # range fail
    "concentration_frac_c_full": 1.5,                 # range fail
    "exposure_window_start_rel_amputation": "t0",     # type fail
    "exposure_window_end_rel_amputation": "t1",       # type fail
    "exposure_mode": "fortnight",                     # enum fail
    "amputation_plane": "brain",                      # taxonomy fail
    "phenotype_score": 1.5,                           # range fail
    "n": 0,                                           # domain fail
    "provenance": "DELETE",                           # missing object
}

# ======================================================================
# THE GATES — each evaluated exactly once, as pre-registered.
# ======================================================================

def _quote_of(lines, spec: str) -> str:
    """Resolve a citation like 'L334' or 'L346-L348' to the normalized
    joined text of those protocol lines."""
    m = re.fullmatch(r"L(\d+)(?:-L(\d+))?", spec)
    assert m, spec
    a = int(m.group(1))
    b = int(m.group(2) or m.group(1))
    return _norm(" ".join(lines[a - 1:b]))


def gate_s1(ctx, bank) -> dict:
    """GATE-S1 (schema): the protocol read; the bank scaffold built with
    the field-provenance table deposited; zero fields without
    provenance; the schema validates the scaffold's empty bank."""
    lines = ctx["protocol_lines"]
    # the protocol carries exactly the cited lines (no drift since the read)
    for ln, expected in _EXPECTED_LINES.items():
        assert lines[ln - 1] == expected, \
            f"protocol L{ln} drifted: {lines[ln-1]!r}"
    for row in FIELD_PROVENANCE:
        assert _quote_of(lines, row["protocol_line"]) == _norm(row["quote"]), \
            f"provenance quote mismatch for {row['field']} " \
            f"({row['protocol_line']})"
    scaffold = dict(bank, entries=[], rejects=[],
                    counts={"imported": 0, "accepted": 0, "rejected": 0})
    errs = validate_bank(scaffold)
    assert not errs, errs
    unprovenanced = bank_field_coverage(scaffold)
    assert not unprovenanced, unprovenanced
    return {
        "verdict": "PASS",
        "asserts": {
            "protocol_lines_unchanged": True,
            "field_provenance_quotes_verified": len(FIELD_PROVENANCE),
            "scaffold_validates_empty_bank": True,
            "zero_fields_without_provenance": True,
        },
        "detail": {
            "protocol_sha256": sha256_file(PROTOCOL),
            "provenance_rows": len(FIELD_PROVENANCE),
            "required_fields": REQUIRED_FIELDS,
            "extended_fields": EXTENDED_FIELDS,
        },
    }


def gate_s2(ctx, bank) -> dict:
    """GATE-S2 (import): the Levin series imported — 119/119 entries, each
    with per-entry provenance (source deposit key + sha256 of the source
    record); entries failing the protocol's required-field census are
    deposited on the reject list (the reject count is a FINDING, not a
    gate failure — the gate is that every accepted entry validates)."""
    anchor = ctx["anchor"]
    assert anchor["exp139_partition_total"] == N_ENTRIES
    assert sum(anchor["exp139_partition_counts"].values()) == N_ENTRIES
    assert anchor["series_len"] == N_ENTRIES
    assert bank["counts"]["imported"] == N_ENTRIES
    assert len(ctx["rows"]) == N_ENTRIES
    # 119/119 accounted, ids unique, nothing silently dropped
    ids = [r["provenance"]["source_key"] for r in bank["entries"]] + \
          [r["provenance"]["source_key"] for r in bank["rejects"]]
    assert len(ids) == N_ENTRIES and len(set(ids)) == N_ENTRIES, \
        "imported ids not 119 unique"
    assert set(ids) == {e["id"] for e in ctx["series"]}
    # per-entry provenance: source key + sha256 of the exact source record
    by_key = {e["id"]: e for e in ctx["series"]}
    for r in bank["entries"] + bank["rejects"]:
        p = r["provenance"]
        src = by_key[p["source_key"]]
        assert p["source_record_sha256"] == sha256_obj(src), p["source_key"]
        assert p["source_deposit"] == "results/exp139_levin_voltage.json"
        assert p["source_record"] == \
            "research/levin_voltage_series.json#series"
    # the gate: every accepted entry validates (census-clean + structure-
    # clean); every reject is structure-clean with a non-empty census
    for r in bank["entries"]:
        assert not census_missing(r), r["provenance"]["source_key"]
        assert not validate_row(r), (r["provenance"]["source_key"],
                                     validate_row(r))
    for r in bank["rejects"]:
        assert r["census_missing"], r["provenance"]["source_key"]
        assert not validate_row(r, allow_census_missing=True), \
            (r["provenance"]["source_key"], validate_row(r, True))
    assert validate_bank(bank) == [], validate_bank(bank)
    # per-slot population census (how much of the protocol schema the
    # record's own rows could populate)
    pop = {}
    for f in REQUIRED_FIELDS + EXTENDED_FIELDS:
        pop[f] = sum(1 for r in ctx["rows"] if r[f] is not None)
    rc = {}
    for r in bank["rejects"]:
        for item in r["census_missing"]:
            rc[item] = rc.get(item, 0) + 1
    return {
        "verdict": "PASS",
        "asserts": {
            "exp139_entry_count_119": True,
            "series_len_119": True,
            "imported_119_of_119": True,
            "ids_unique_complete": True,
            "per_entry_provenance_sha_verified": True,
            "every_accepted_entry_validates": True,
            "every_reject_structure_clean_census_named": True,
            "bank_validates": True,
        },
        "detail": {
            "counts": dict(bank["counts"]),
            "population_census": pop,
            "reject_census_summary": rc,
            "finding": "reject count is a FINDING (pre-registered), not a "
                       "gate failure",
        },
    }


def gate_s3(ctx, bank, bank_path: str) -> dict:
    """GATE-S3 (round-trip): write/read-back byte-identical on the full
    bank; the validator accepts every round-tripped entry and rejects a
    mutated probe (one field corrupted per probe x every required field
    — the negative controls all fail)."""
    out_bytes = ser(bank).encode("utf-8")
    with open(bank_path, "wb") as f:
        f.write(out_bytes)
    with open(bank_path, "rb") as f:
        raw = f.read()
    assert raw == out_bytes, "write/read-back not byte-identical"
    rb = json.loads(raw.decode("utf-8"))
    errs = validate_bank(rb)
    assert not errs, errs
    for r in rb["entries"]:
        assert not validate_row(r) and not census_missing(r)
    for r in rb["rejects"]:
        assert not validate_row(r, allow_census_missing=True)
        assert r["census_missing"]
    assert not bank_field_coverage(rb), bank_field_coverage(rb)
    # the validator's accept path on a well-formed row (non-vacuous even
    # when the import's accepted set is empty)
    assert not census_missing(_FIXTURE), census_missing(_FIXTURE)
    assert not validate_row(_FIXTURE), validate_row(_FIXTURE)
    # negative controls: one field corrupted per probe x every required
    # field — all must be rejected
    probes = []
    for slot, bad in _CORRUPTIONS.items():
        probe = dict(_FIXTURE)
        if bad == "DELETE":
            probe = {k: v for k, v in probe.items() if k != slot}
        else:
            probe[slot] = bad
        rejected = bool(census_missing(probe)) or bool(validate_row(probe))
        probes.append({"corrupted_field": slot,
                       "corruption": "DELETE" if bad == "DELETE" else bad,
                       "rejected": rejected})
    assert len(probes) == len(REQUIRED_FIELDS) + 1  # 11 value slots + provenance
    assert all(p["rejected"] for p in probes), \
        [p for p in probes if not p["rejected"]]
    return {
        "verdict": "PASS",
        "asserts": {
            "round_trip_byte_identical": True,
            "bank_revalidates_after_round_trip": True,
            "every_round_tripped_entry_accepted": True,
            "field_coverage_zero_unprovenanced": True,
            "fixture_accepted": True,
            "negative_controls_all_fail": True,
        },
        "detail": {"bank_path": os.path.relpath(bank_path, ROOT),
                   "bank_bytes": len(out_bytes),
                   "negative_controls": probes},
    }


def gate_s4(ctx, bank, bank_path: str) -> dict:
    """GATE-S4 (hygiene): no source deposit mutated; the bank written
    under results/ with a deterministic filename; the run is idempotent
    (re-run reproduces the bank byte-identically)."""
    for label, h in ctx["hashes"].items():
        if not h["present"]:
            continue
        assert sha256_file(os.path.join(ROOT, h["path"])) == h["sha256"], \
            f"source mutated: {label}"
    assert os.path.basename(BANK) == "wetlab_companion_bank.json"
    assert os.path.relpath(BANK, ROOT) == \
        os.path.join("results", "wetlab_companion_bank.json")
    bank2, _ = run_pipeline()
    b1, b2 = ser(bank), ser(bank2)
    assert b1 == b2, "re-run not byte-identical"
    with open(bank_path, "rb") as f:
        raw = f.read()
    assert raw == b2.encode("utf-8"), "written bank != re-run bank"
    return {
        "verdict": "PASS",
        "asserts": {
            "no_source_deposit_mutated": True,
            "deterministic_bank_filename": True,
            "rerun_byte_identical": True,
            "written_bank_equals_rerun": True,
        },
        "detail": {"source_hashes": ctx["hashes"]},
    }

# ======================================================================
# main
# ======================================================================

GATE_FUNCS = {"s1": gate_s1, "s2": gate_s2, "s3": gate_s3, "s4": gate_s4}


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args, _ = ap.parse_known_args()
    if args.job == "all":
        jobs = ["s1", "s2", "s3", "s4"]
    else:
        jobs = [j.strip().lower() for j in args.job.split(",") if j.strip()]
        unknown = [j for j in jobs if j not in GATE_FUNCS]
        assert not unknown, f"unknown --job gates: {unknown}"
    bank, ctx = run_pipeline()
    bank_path = SMOKE_BANK if args.smoke else BANK
    gates = {}
    for j in jobs:
        try:
            if j in ("s1", "s2"):
                gates[f"GATE-{j.upper()}"] = GATE_FUNCS[j](ctx, bank)
            else:
                gates[f"GATE-{j.upper()}"] = GATE_FUNCS[j](ctx, bank,
                                                           bank_path)
        except AssertionError:
            tb = traceback.format_exc().strip().splitlines()
            gates[f"GATE-{j.upper()}"] = {
                "verdict": "REFUTE",
                "traceback_one_liner": tb[-1] if tb else "AssertionError",
            }
    for j in GATE_FUNCS:
        gates.setdefault(f"GATE-{j.upper()}", {"verdict": "NOT_EVALUATED"})
    evaluated = {k: v for k, v in gates.items()
                 if v["verdict"] != "NOT_EVALUATED"}
    n_pass = sum(1 for v in evaluated.values() if v["verdict"] == "PASS")
    n_ref = sum(1 for v in evaluated.values() if v["verdict"] == "REFUTE")
    all_pass = n_ref == 0 and n_pass > 0
    counts = bank["counts"]
    verdict = (
        f"PASS {n_pass}/{len(evaluated)} gates — the wetlab companion bank "
        f"scaffolded from the protocol (every field line-traced), first "
        f"deposit imported: {counts['imported']}/{N_ENTRIES} accounted, "
        f"{counts['accepted']} accepted / {counts['rejected']} "
        f"census-rejected (the record's missing dose axis, quantified per "
        f"row); round-trip byte-identical, negative controls all fail, "
        f"hygiene clean"
        if all_pass else
        f"REFUTE {n_ref}/{len(evaluated)} gates failed "
        f"({', '.join(k for k, v in evaluated.items() if v['verdict'] == 'REFUTE')})")
    rejected = counts["rejected"]
    deposit = {
        "exp": "exp203_wetlab_scaffold",
        "task": "THE WETLAB COMPANION DEPOSIT SCAFFOLD (L170's registered "
                "next): the Stage-5 wetlab companion protocol's schema "
                "read, the bank format implemented, and the FIRST deposit "
                "imported — exp139's 119-entry Levin voltage series — "
                "validated end to end",
        "protocol": {
            "path": "docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md",
            "sha256": ctx["hashes"]["protocol"]["sha256"],
            "role": "the ONLY schema source; every bank field traces to a "
                    "protocol line via field_provenance",
        },
        "import_anchor": ctx["anchor"],
        "field_provenance": FIELD_PROVENANCE,
        "required_fields": REQUIRED_FIELDS,
        "extended_fields": EXTENDED_FIELDS,
        "census_rule": CENSUS_RULE,
        "import_rules": IMPORT_RULES,
        "bank_pointer": os.path.relpath(bank_path, ROOT),
        "counts": counts,
        "population_census": gates["GATE-S2"].get("detail", {}).get(
            "population_census"),
        "reject_census_summary": gates["GATE-S2"].get("detail", {}).get(
            "reject_census_summary"),
        "negative_controls": gates["GATE-S3"].get("detail", {}).get(
            "negative_controls"),
        "gates": gates,
        "criteria": {
            "GATE-S1": "protocol read; bank scaffold built with the "
                       "field-provenance table deposited; zero fields "
                       "without provenance; schema validates the empty "
                       "bank",
            "GATE-S2": "Levin series imported 119/119, per-entry "
                       "provenance (source deposit key + sha256 of the "
                       "source record); census-failing entries on the "
                       "reject list (reject count a FINDING); every "
                       "accepted entry validates",
            "GATE-S3": "write/read-back byte-identical on the full bank; "
                       "validator accepts every round-tripped entry and "
                       "rejects a mutated probe (one field corrupted per "
                       "probe x every required field)",
            "GATE-S4": "no source deposit mutated; deterministic bank "
                       "filename under results/; re-run reproduces the "
                       "bank byte-identically",
        },
        "verdict": verdict,
        "notes": (
            "Census reading (disclosed): the protocol's W5 schema has "
            "exactly two column classes — the seven bullets (L338-344, "
            "required) and the extended columns (L346-348) — so the "
            "required-field census checks all seven bullets. The record's "
            "rows carry NO concentrations anywhere (exp33/L16; "
            "re-verified exp197), so the census rejects every record row "
            "on the dose-identity column: the reject count IS the "
            "quantified record hole this bank exists to fill, deposited "
            "per row with reasons. At accepted=0 the accepted-validate "
            "clause is vacuous by this pre-registered design; the "
            "validator's accept path is exercised non-vacuously by the "
            "G3 fixture, and its reject path by the 12 negative "
            "controls. StartTime/EndTime are deposited verbatim "
            "uninterpreted (the source deposit's own semantics). "
            "results/exp39_levin_voltage.json is a series mining source "
            "but untracked in git; hashed for hygiene when present. "
            "Smoke runs (permitted, discarded) write "
            "results/exp203_wetlab_scaffold_smoke.json and "
            "results/wetlab_companion_bank_smoke.json only."),
        "sources": {
            "protocol": "docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md (the "
                        "ONLY schema source; W5 deposit schema L334-348)",
            "import_source": "results/exp139_levin_voltage.json (its own "
                             "entry count asserted == 119)",
            "series_records": "research/levin_voltage_series.json#series "
                              "(the deposit exp139's sources.record points "
                              "to; 119 entries)",
            "plane_drug_taxonomy": "experiments/planform_mining.py "
                                   "(pre-registered 2026-09-15; the "
                                   "protocol keys the schema to it, "
                                   "L335)",
            "phenotype_rule": "experiments/exp21_planform_benchmark.py "
                              "(abnormal(E) = 1 - freq(Wild type), "
                              "pre-registered) via exp139's deposited "
                              "reading",
            "series_mining_source": "results/exp39_levin_voltage.json "
                                    "(untracked; hashed when present)",
        },
        "smoke": bool(args.smoke),
        "job": args.job,
        "gates_all_pass": bool(all_pass),
    }
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    _args = ap.parse_args()
    _res = main()
    _out_path = _args.out or (SMOKE_OUT if _args.smoke else OUT)
    _dep = dict(_res)
    _dep["deposit_path"] = os.path.relpath(_out_path, ROOT)
    with open(_out_path, "w", encoding="utf-8") as _f:
        _f.write(ser(_dep))
    print(f"exp203 deposit -> {_out_path}")
    print(f"exp203 verdict: {_res['verdict']}")
    sys.exit(0 if _res["gates_all_pass"] else 1)
