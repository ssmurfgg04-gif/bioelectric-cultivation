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
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import subprocess
    import time

    import experiments.exp206_w5_dose_pass as E206  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    W5B_BANK = os.path.join(ROOT, "results",
                            "wetlab_companion_bank_w5b.json")
    W5C_BANK = os.path.join(ROOT, "results",
                            "wetlab_companion_bank_w5c.json")
    W5_SOURCES = E206.SOURCES             # pass 1 (frozen)
    W5B_SOURCES = os.path.join(ROOT, "results",
                               "w5_pass_sources2.json")  # pass 2 (frozen)
    W5C_SOURCES = os.path.join(ROOT, "results",
                               "w5_pass_sources3.json")  # pass 3 (frozen)
    SPEC_DEPOSIT = os.path.join(ROOT, "results",
                                "exp215_w5_figure_pass.json")
    EXP203_PATH = os.path.join(ROOT, "experiments",
                               "exp203_wetlab_scaffold.py")
    SMOKE_BANK = os.path.join(ROOT, "results",
                              "wetlab_companion_bank_w5d_smoke.json")
    bank_path = SMOKE_BANK if args.smoke else BANK
    n_take = 3 if args.smoke else E206.N_ENTRIES

    assert os.path.exists(W5B_BANK), "the w5b bank (hygiene) missing"
    assert os.path.exists(W5C_BANK), \
        "the w5c bank (the frozen baseline for this pass) missing"
    assert os.path.exists(SPEC_DEPOSIT), \
        "exp215's deposit (the not_in_literature_spec) missing"
    for _p in (W5_SOURCES, W5B_SOURCES, W5C_SOURCES):
        assert os.path.exists(_p), f"sources file missing: {_p}"

    # ---- the instruments -------------------------------------------------
    with open(SPEC_DEPOSIT, encoding="utf-8") as f:
        spec_doc = json.load(f)
    spec = spec_doc["sections"]["not_in_literature_spec"]
    assert spec is not None and spec.get("state") == "NOT-IN-LITERATURE", \
        "exp215's deposited not_in_literature_spec missing"
    assert spec_doc["gates"]["GATE-F3"].get("branch") == "REGISTERED", \
        "exp215's REGISTERED branch is the instrument's precondition"
    assert spec["n_zero_extract_records"] == 73, \
        spec["n_zero_extract_records"]
    spec_zero = list(spec["zero_extract_records_all_3_passes"])

    src1 = E206.read_sources(W5_SOURCES)
    src2 = E206.read_sources(W5B_SOURCES)
    src3 = E206.read_sources(W5C_SOURCES)
    by_pass = {1: src1["by_id"], 2: src2["by_id"], 3: src3["by_id"]}
    sources_sha = {os.path.relpath(p, ROOT): E206.sha256_file(p)
                   for p in (W5_SOURCES, W5B_SOURCES, W5C_SOURCES)}
    src_sha0 = dict(sources_sha)

    with open(E206.SERIES, encoding="utf-8") as f:
        series = json.load(f)["series"]
    with open(W5C_BANK, encoding="utf-8") as f:
        w5c = json.load(f)
    w5c_sha0 = E206.sha256_file(W5C_BANK)
    w5b_sha0 = E206.sha256_file(W5B_BANK)
    exp203_sha0 = E206.sha256_file(EXP203_PATH)

    w5c_rows: dict = {}
    for r in list(w5c.get("entries", [])) + list(w5c.get("rejects", [])):
        key = (r.get("provenance") or {}).get("source_key")
        if key is not None:
            w5c_rows[key] = r

    # ==== THE EXTENSION (additive, disclosed, zero knobs) ==============
    # census_missing is extended IN THIS MODULE (exp203's file untouched)
    # by the not_in_literature clause; every other acceptance rule
    # unchanged.

    _KINDS = ("concentration", "blocker", "phenotype", "n",
              "exposure_mode")

    def extract_counts(rec) -> dict:
        """Raw per-kind extract counts of one pass's sources record
        (the zero-extract assertion reads the sources files, not the
        merge)."""
        c = {k: 0 for k in _KINDS}
        for ex in (rec or {}).get("extracts", []):
            if ex.get("kind") in c:
                c[ex.get("kind")] += 1
        return c

    def nil_missing_fill_fields(row) -> list:
        """The record's missing FILL_FIELDS (the null W5 columns the
        three passes swept for)."""
        return [f for f in E206.FILL_FIELDS if row.get(f) is None]

    def nil_admissible(row, cm, recs) -> tuple:
        """THE not_in_literature CLAUSE: a record whose missing
        FILL_FIELDS have ZERO extracts across all three passes is
        admissible to census_state='NOT-IN-LITERATURE'.  Returns
        (admissible, missing_fill_fields, per-pass kind counts)."""
        assert cm, "the clause applies to census-missing records only"
        miss = nil_missing_fill_fields(row)
        counts = {p: extract_counts(recs[p]) for p in (1, 2, 3)}
        zero = all(counts[p][E206._KIND_OF[f]] == 0
                   for f in miss for p in (1, 2, 3))
        return zero, miss, counts

    def validate_nil_row(row) -> list:
        """exp203's validate_row (structure layer, census-missing
        allowed) + the census_state slot the not_in_literature clause
        adds; every other rule unchanged."""
        body = {k: v for k, v in row.items() if k != "census_state"}
        errs = list(E206.validate_row(body, allow_census_missing=True))
        if row.get("census_state") != "NOT-IN-LITERATURE":
            errs.append("census_state: must be 'NOT-IN-LITERATURE'")
        if not row.get("census_missing"):
            errs.append("census_missing: the missing field list must "
                        "be non-empty on a NOT-IN-LITERATURE row")
        return errs

    def validate_bank_ext(bank) -> list:
        """exp203's validate_bank, extended additively for the
        three-state partition (entries / not_in_literature / rejects):
        the entries and rejects rules are exp203's, UNCHANGED; the NIL
        rows validate through validate_nil_row."""
        errs = []
        envelope = ["bank", "bank_file", "pass", "baseline", "protocol",
                    "protocol_sha256", "schema_version",
                    "field_provenance", "required_fields",
                    "extended_fields", "census_rule", "census_extension",
                    "import_source", "import_rules", "entries",
                    "not_in_literature", "rejects", "counts"]
        for k in envelope:
            if k not in bank:
                errs.append(f"bank: missing envelope key {k}")
        if errs:
            return errs
        if bank["bank"] != "wetlab_companion":
            errs.append("bank: bad bank name")
        if bank["required_fields"] != E206.REQUIRED_FIELDS:
            errs.append("bank: required_fields drift")
        if bank["extended_fields"] != E206.EXTENDED_FIELDS:
            errs.append("bank: extended_fields drift")
        if bank["census_rule"] != E206.CENSUS_RULE:
            errs.append("bank: census_rule drift (the census is "
                        "exp203's, UNCHANGED; the extension lives in "
                        "census_extension)")
        for i, e in enumerate(bank["entries"]):
            for err in E206.validate_row(e, allow_census_missing=False):
                errs.append(f"entries[{i}]: {err}")
            if e.get("census_missing"):
                errs.append(f"entries[{i}]: accepted row carries "
                            "census_missing")
        for i, r in enumerate(bank["not_in_literature"]):
            for err in validate_nil_row(r):
                errs.append(f"not_in_literature[{i}]: {err}")
        for i, r in enumerate(bank["rejects"]):
            for err in E206.validate_row(r, allow_census_missing=True):
                errs.append(f"rejects[{i}]: {err}")
            if not r.get("census_missing"):
                errs.append(f"rejects[{i}]: census_missing empty on a "
                            "reject")
        c = bank["counts"]
        n = (c.get("normal_accepted", 0) + c.get("not_in_literature", 0)
             + c.get("rejected", 0))
        if (c.get("imported") != n
                or c.get("normal_accepted") != len(bank["entries"])
                or c.get("not_in_literature")
                != len(bank["not_in_literature"])
                or c.get("rejected") != len(bank["rejects"])):
            errs.append("bank: counts inconsistent with the three-state "
                        "partition")
        return errs

    def field_coverage(bank) -> list:
        """Zero fields without provenance: exp203's bank_field_coverage
        VERBATIM (envelope, entries, rejects, import_rules) + the
        not_in_literature list's rows and their provenance sub-keys."""
        missing = list(E206.bank_field_coverage(bank))
        known = {r["field"] for r in bank["field_provenance"]}
        for i, r in enumerate(bank.get("not_in_literature", [])):
            for k in r:
                if k not in known:
                    missing.append(f"not_in_literature[{i}]:{k}")
            p = r.get("provenance", {})
            if isinstance(p, dict):
                for k in p:
                    if f"provenance.{k}" not in known:
                        missing.append(
                            f"not_in_literature[{i}]:provenance.{k}")
        return sorted(set(missing))

    # ---- the field-provenance rows the extension adds (the w5c file
    #      is untouched; the TABLE is extended here, disclosed) --------
    _NIL_QUOTE = ("census_missing is extended IN THIS MODULE (exp203's "
                  "file untouched) by the not_in_literature clause — a "
                  "record whose missing FILL_FIELDS have ZERO extracts "
                  "across all three passes is admissible to the state "
                  "census_state='NOT-IN-LITERATURE' with the missing "
                  "field list; every other acceptance rule unchanged")
    NEW_FP = [
        {"field": "bank_file",
         "protocol_line": "exp206/exp215/exp217 bank lineage",
         "quote": "the new bank written = "
                  "results/wetlab_companion_bank_w5d.json"},
        {"field": "pass",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": "This run IMPLEMENTS the specification and re-imports "
                  "the 119 records under the extended census"},
        {"field": "baseline",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": "the w5c bank the frozen baseline"},
        {"field": "census_extension",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec"),
         "quote": spec["registered_repair"]},
        {"field": "not_in_literature",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": _NIL_QUOTE},
        {"field": "census_state",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": "admissible to the state "
                  "census_state='NOT-IN-LITERATURE' with the missing "
                  "field list"},
        {"field": "provenance.pass2_source_record_sha256",
         "protocol_line": ("results/wetlab_companion_bank_w5c.json#"
                           "import_rules.provenance"),
         "quote": w5c.get("import_rules", {}).get("provenance", "")},
        {"field": "provenance.census_state",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec.provenance_discipline"),
         "quote": spec["provenance_discipline"]},
        {"field": "provenance.pass1_source_record_sha256",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec.provenance_discipline"),
         "quote": spec["provenance_discipline"]},
        {"field": "provenance.pass3_source_record_sha256",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec.provenance_discipline"),
         "quote": spec["provenance_discipline"]},
        {"field": "provenance.sources_files",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec.provenance_discipline"),
         "quote": ("the verdict's provenance names ALL THREE sources "
                   "files")},
        {"field": "provenance.sources_files_sha256",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": ("the THREE sources files ... each sha256'd IN the "
                   "deposit")},
        {"field": "provenance.missing_fill_fields",
         "protocol_line": "exp217 docstring (pre-registered, batch 11)",
         "quote": _NIL_QUOTE},
        {"field": "provenance.absence_discipline",
         "protocol_line": ("results/exp215_w5_figure_pass.json#sections."
                           "not_in_literature_spec.provenance_discipline"),
         "quote": spec["provenance_discipline"]},
    ]

    # ---- the census (merge): base rows = the W5C BANK's rows (the
    #      frozen baseline for THIS pass); the re-import re-runs
    #      E206's w5_fills per pass ONLY to assert it adds nothing
    #      (fill-complete baseline), re-computes the census FRESH
    #      (16 w5c rows carry pass-2-stale inherited census_missing
    #      keys — overwritten here), and adjudicates the three-state
    #      partition through the unchanged rules + the NIL clause ----
    def merge() -> tuple:
        entries, nil_rows, rejects, verdicts = [], [], [], []
        refill_added: dict = {}
        for i, e in enumerate(series[:n_take]):
            base = w5c_rows.get(e["id"])
            assert base is not None, \
                f"the w5c bank has no row for {e['id']}"
            row = json.loads(json.dumps(base))   # pure copy
            inherited_cm = base.get("census_missing")
            refill = {}
            recs = {p: by_pass[p].get(e["id"]) for p in (1, 2, 3)}
            for p in (1, 2, 3):
                if recs[p] is not None:
                    rf = E206.w5_fills(row, e, recs[p])
                    if rf:
                        refill[str(p)] = sorted(rf)
            refill_added[e["id"]] = refill
            cm = E206.census_missing(row)   # FRESH census (authoritative)
            struct_ok = not E206.validate_row(
                row, allow_census_missing=bool(cm))
            normal_ok = ((not cm) and struct_ok
                         and not E206.validate_row(row))
            adm, miss, counts = nil_admissible(row, cm, recs)
            total_ex = sum(
                len((recs[p] or {}).get("extracts", []))
                for p in (1, 2, 3))
            if normal_ok:
                state = "accepted"
            elif cm and adm:
                state = "not_in_literature"
            else:
                state = "rejected"
            reasons: list = []
            if state == "not_in_literature":
                row["census_state"] = "NOT-IN-LITERATURE"
                row["census_missing"] = list(cm)
                row["provenance"] = {
                    "source_deposit":
                        "results/exp217_not_in_literature_census.json",
                    "source_record": (
                        "results/exp217_not_in_literature_census.json"
                        f"#sections.verdicts.{e['id']}"),
                    "source_key": e["id"],
                    # the three-pass evidence chain, keyed + re-runnable
                    "source_record_sha256":
                        E206.sha256_obj([recs[1], recs[2], recs[3]]),
                    "pass1_source_record_sha256":
                        E206.sha256_obj(recs[1]),
                    "pass2_source_record_sha256":
                        E206.sha256_obj(recs[2]),
                    "pass3_source_record_sha256":
                        E206.sha256_obj(recs[3]),
                    "sources_files": [
                        "results/w5_pass_sources.json",
                        "results/w5_pass_sources2.json",
                        "results/w5_pass_sources3.json"],
                    "sources_files_sha256": [
                        sources_sha["results/w5_pass_sources.json"],
                        sources_sha["results/w5_pass_sources2.json"],
                        sources_sha["results/w5_pass_sources3.json"]],
                    "census_state": "NOT-IN-LITERATURE",
                    "missing_fill_fields": list(miss),
                    "absence_discipline":
                        spec["provenance_discipline"]}
                nil_rows.append(row)
            elif state == "rejected":
                if cm:
                    reasons = E206._reasons(
                        row, e, recs[3] or recs[2] or recs[1], cm)
                    blocking = sorted({
                        f for f in miss
                        if any(counts[p][E206._KIND_OF[f]] > 0
                               for p in (1, 2, 3))})
                    if blocking:
                        reasons.append(
                            "not_in_literature clause: extract(s) "
                            f"present for missing field(s) {blocking} "
                            "across the three passes — the NIL "
                            "discipline excludes admission (GATE-N2)")
                    else:
                        reasons.append(
                            "not_in_literature clause inapplicable: "
                            "no missing FILL_FIELDS cover the census "
                            "items (uncovered census item)")
                else:
                    reasons = list(E206.validate_row(row))
                row = dict(row, census_missing=cm)
                rejects.append(row)
            else:
                entries.append(row)
            verdicts.append({
                "index": i, "id": e["id"], "state": state,
                "census_missing": cm,
                "missing_fill_fields": miss,
                "extract_counts_by_pass": {str(p): counts[p]
                                           for p in (1, 2, 3)},
                "total_extracts_all_passes": total_ex,
                "zero_extract_all_passes": total_ex == 0,
                "in_exp215_zero_extract_set": e["id"] in set(spec_zero),
                "nil_admissible": bool(cm) and adm,
                "census_missing_matches_baseline":
                    sorted(inherited_cm or []) == sorted(cm),
                "refill_added": refill,
                "sources_tried_by_pass": {
                    str(p): len((recs[p] or {}).get("sources_tried", []))
                    for p in (1, 2, 3)},
                "reasons": reasons})
        counts = {"imported": len(series[:n_take]),
                  "normal_accepted": len(entries),
                  "not_in_literature": len(nil_rows),
                  "rejected": len(rejects)}
        bank4 = {
            "bank": "wetlab_companion",       # the validator's name rule
            "bank_file": "results/wetlab_companion_bank_w5d.json",
            "pass": 4,
            "baseline": {
                "bank": "results/wetlab_companion_bank_w5c.json",
                "sha256": w5c_sha0,
                "disclosure": ("the w5c bank is the frozen baseline for "
                               "THIS pass; its rows are the census's "
                               "re-adjudicated base")},
            "protocol": w5c.get("protocol"),
            "protocol_sha256": w5c.get("protocol_sha256"),
            "schema_version": w5c.get("schema_version"),
            "census_rule": w5c.get("census_rule"),
            "required_fields": w5c.get("required_fields"),
            "extended_fields": w5c.get("extended_fields"),
            "census_extension": {
                "state": "NOT-IN-LITERATURE",
                "implemented_in":
                    "experiments/exp217_not_in_literature_census.py "
                    "(exp203's file untouched)",
                "clause": _NIL_QUOTE,
                "source_spec": (
                    "results/exp215_w5_figure_pass.json#sections."
                    "not_in_literature_spec"),
                "source_spec_sha256": E206.sha256_file(SPEC_DEPOSIT),
                "spec": spec},
            "import_source": {
                "baseline": ("results/wetlab_companion_bank_w5c.json "
                             "(the frozen 0/119 baseline; read, never "
                             "rewritten)"),
                "series_records":
                    "research/levin_voltage_series.json#series",
                "sources_files": [
                    "results/w5_pass_sources.json",
                    "results/w5_pass_sources2.json",
                    "results/w5_pass_sources3.json"],
                "sources_files_sha256": sources_sha,
                "sources_records": [src1["n_records"], src2["n_records"],
                                    src3["n_records"]],
                "sources_mode": [src1["mode"], src2["mode"],
                                 src3["mode"]],
                "pass_rules": {
                    "ordering": E206.FILL_RULES["ordering"],
                    "fill_never_overwrite":
                        E206.FILL_RULES["fill_never_overwrite"],
                    "base_rows": ("the W5C BANK's rows (pass-3's "
                                  "product), not the scaffold rows — "
                                  "the re-import's w5_fills re-run "
                                  "adds NOTHING (fill-complete "
                                  "baseline; asserted per record) and "
                                  "the acceptance predicate is "
                                  "UNCHANGED except the deposited "
                                  "not_in_literature clause; "
                                  "census_missing is recomputed FRESH "
                                  "(inherited pass-2-stale keys "
                                  "overwritten)")}},
            "import_rules": dict(
                list((w5c.get("import_rules") or {}).items())
                + [("not_in_literature", _NIL_QUOTE)]),
            "field_provenance": list(w5c.get("field_provenance", []))
            + NEW_FP,
            "entries": entries,
            "not_in_literature": nil_rows,
            "rejects": rejects,
            "counts": counts}
        return bank4, verdicts, refill_added

    bank4, verdicts, refill_added = merge()

    recomputed_zero = sorted(
        e["id"] for e in series
        if sum(len((by_pass[p].get(e["id"]) or {}).get("extracts", []))
               for p in (1, 2, 3)) == 0)

    # ---- the deposit's evidence sections (assembled BEFORE the gates
    #      so GATE-N1's "each file's sha256 in the deposit" reads the
    #      payload that is actually written) ----------------------------
    deposit_sections = {
        "verdicts": verdicts,
        "sources": [
            {"file": os.path.relpath(p, ROOT),
             "sha256": sources_sha[os.path.relpath(p, ROOT)],
             "n_records": s["n_records"], "mode": s["mode"]}
            for p, s in ((W5_SOURCES, src1), (W5B_SOURCES, src2),
                         (W5C_SOURCES, src3))],
        "not_in_literature_spec": spec,   # the instrument, VERBATIM
        "zero_extract_recomputed": recomputed_zero,
        "counts_split": {
            "n_normal_accepted": len(bank4["entries"]),
            "n_not_in_literature": len(bank4["not_in_literature"]),
            "n_rejected": len(bank4["rejects"]),
            "imported": len(series[:n_take])},
        "refill_added_nothing": all(
            not v for v in refill_added.values()),
        "exp203_file": "experiments/exp203_wetlab_scaffold.py",
        "exp203_file_sha256": exp203_sha0}

    gates = {}
    if not args.smoke:
        def _gate(name, fn):
            try:
                gates[name] = fn()
            except AssertionError:
                import traceback as _tb
                tb = _tb.format_exc().strip().splitlines()
                gates[name] = {"verdict": "REFUTE",
                               "assert_failure": tb[-1] if tb
                               else "AssertionError"}

        def _exp203_untouched() -> bool:
            try:
                for extra in (["HEAD"], ["--cached"]):
                    r = subprocess.run(
                        ["git", "diff", "--quiet"] + extra + ["--",
                         "experiments/exp203_wetlab_scaffold.py"],
                        cwd=ROOT, capture_output=True, timeout=30)
                    if r.returncode != 0:
                        return False
                return True
            except Exception:
                return False

        def _n1():
            # ---- GATE-N1 (the evidence check) -----------------------
            ids_v = [v["id"] for v in verdicts]
            want = [e["id"] for e in series[:n_take]]
            per_file = []
            for entry in deposit_sections["sources"]:
                sha_now = E206.sha256_file(
                    os.path.join(ROOT, entry["file"]))
                sha = entry["sha256"]
                per_file.append({
                    "file": entry["file"],
                    "n_records": entry["n_records"],
                    "sha256_is_64hex_in_deposit":
                        isinstance(sha, str) and len(sha) == 64
                        and all(c in "0123456789abcdef" for c in sha),
                    "sha256_matches_file": sha_now == sha,
                    "complete_119": entry["n_records"] == E206.N_ENTRIES})
            ids_ok = []
            for s in (src1, src2, src3):
                ids_p = sorted(r.get("id")
                               for r in s["doc"]["records"])
                ids_ok.append(ids_p == sorted(want))
            ok = (len(verdicts) == len(want)
                  and sorted(ids_v) == sorted(want)
                  and all(f["sha256_is_64hex_in_deposit"]
                          and f["sha256_matches_file"]
                          and f["complete_119"] for f in per_file)
                  and all(ids_ok))
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "n_verdicts": len(verdicts),
                "n_series": len(want),
                "verdict_ids_complete": sorted(ids_v) == sorted(want),
                "sources_files": per_file,
                "ids_match_series_by_pass": ids_ok}

        def _n2():
            # ---- GATE-N2 (the zero-extract assertion; the discipline
            #      holds) ----------------------------------------------
            bad_nil = []
            for v in verdicts:
                if v["state"] != "not_in_literature":
                    continue
                for f in v["missing_fill_fields"]:
                    kind = E206._KIND_OF[f]
                    for p in (1, 2, 3):
                        rec = by_pass[p].get(v["id"])
                        n_ex = sum(1 for ex in
                                   (rec or {}).get("extracts", [])
                                   if ex.get("kind") == kind)
                        if n_ex:
                            bad_nil.append({"id": v["id"], "field": f,
                                            "pass": p,
                                            "kind_extracts": n_ex})
            # completeness: no record with a non-empty census and zero
            # extracts for every missing field sits in rejects
            # (recounted from the sources docs, independent of the
            # merge's flags)
            missed, uncovered = [], []
            for v in verdicts:
                if v["state"] != "rejected" or not v["census_missing"]:
                    continue
                if not v["missing_fill_fields"]:
                    uncovered.append(v["id"])
                    continue
                zero_all = True
                for f in v["missing_fill_fields"]:
                    kind = E206._KIND_OF[f]
                    for p in (1, 2, 3):
                        rec = by_pass[p].get(v["id"])
                        if any(ex.get("kind") == kind for ex in
                               (rec or {}).get("extracts", [])):
                            zero_all = False
                if zero_all:
                    missed.append(v["id"])
            refill_clean = all(not v for v in refill_added.values())
            bank_errs = validate_bank_ext(bank4)
            untouched = _exp203_untouched()
            ok = (not bad_nil and not missed and refill_clean
                  and not bank_errs and untouched)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "nil_zero_extract_violations": bad_nil,
                "clause_misses": missed,
                "uncovered_census_records": uncovered,
                "refill_added_nothing": refill_clean,
                "refill_drift": {k: v
                                 for k, v in refill_added.items() if v},
                "bank_validator_errors": bank_errs,
                "exp203_file_untouched_git": untouched,
                "exp203_file_sha256": exp203_sha0,
                "n_not_in_literature":
                    len(bank4["not_in_literature"])}

        def _n3():
            # ---- GATE-N3 (the split; the branch NAMED, each clause
            #      evaluated once) ------------------------------------
            na = len(bank4["entries"])
            nn = len(bank4["not_in_literature"])
            nr = len(bank4["rejects"])
            split_ok = na + nn + nr == len(series[:n_take])
            states = {v["id"]: v["state"] for v in verdicts}
            landed = {
                "all_73_not_in_literature_or_better": all(
                    states.get(i) in ("accepted", "not_in_literature")
                    for i in spec_zero),
                "n_landed_in_state": sum(
                    1 for i in spec_zero
                    if states.get(i) == "not_in_literature"),
                "n_landed_accepted": sum(
                    1 for i in spec_zero
                    if states.get(i) == "accepted")}
            g2 = gates.get("GATE-N2") or {}
            zero_integrity = (
                g2.get("verdict") == "PASS"
                and not g2.get("nil_zero_extract_violations")
                and not g2.get("clause_misses")
                and not g2.get("bank_validator_errors"))
            branch = ("CLOSED-NIL" if (nn >= 73 and zero_integrity)
                      else "PARTIAL")
            set_ok = recomputed_zero == sorted(spec_zero)
            ok = (split_ok
                  and landed["all_73_not_in_literature_or_better"]
                  and set_ok)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "n_normal_accepted": na,
                "n_not_in_literature": nn,
                "n_rejected": nr,
                "split_sum": na + nn + nr,
                "split_ok": split_ok,
                "exp215_zero_extract_landing": landed,
                "zero_extract_set_matches_exp215": set_ok,
                "branch": branch,
                "realized_counts_deposited":
                    deposit_sections["counts_split"]}

        def _n4():
            # ---- GATE-N4 (hygiene) ----------------------------------
            os.makedirs(os.path.dirname(bank_path), exist_ok=True)
            with open(bank_path, "w", encoding="utf-8") as f:
                f.write(E206.ser(bank4))
            bank4_rerun, _v2, _r3 = merge()
            determinism = (E206.ser(bank4_rerun) == E206.ser(bank4))
            w5b_sha1 = E206.sha256_file(W5B_BANK)
            w5c_sha1 = E206.sha256_file(W5C_BANK)
            src_unchanged = all(
                E206.sha256_file(p) == src_sha0[os.path.relpath(p, ROOT)]
                for p in (W5_SOURCES, W5B_SOURCES, W5C_SOURCES))
            gaps = field_coverage(bank4)
            ok = (determinism and w5b_sha1 == w5b_sha0
                  and w5c_sha1 == w5c_sha0 and src_unchanged
                  and not gaps)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "w5b_bank_byte_unchanged": w5b_sha1 == w5b_sha0,
                "w5c_bank_byte_unchanged": w5c_sha1 == w5c_sha0,
                "w5c_sha256": w5c_sha0,
                "sources_files_byte_unchanged": src_unchanged,
                "new_bank_deterministic": determinism,
                "zero_fields_without_provenance": not gaps,
                "provenance_gaps": gaps,
                "field_provenance_rows":
                    len(bank4["field_provenance"])}

        # ---- evaluate each gate exactly once, asserts recorded as
        #      REFUTE with the failing line (exp206's gate discipline)
        _gate("GATE-N1", _n1)
        _gate("GATE-N2", _n2)
        _gate("GATE-N3", _n3)
        _gate("GATE-N4", _n4)

        n_pass = sum(1 for v in gates.values()
                     if v["verdict"] == "PASS")
        n_ref = sum(1 for v in gates.values()
                    if v["verdict"] == "REFUTE")
        na = len(bank4["entries"])
        nn = len(bank4["not_in_literature"])
        nr = len(bank4["rejects"])
        branch = gates["GATE-N3"].get("branch", "—")
        verdict = (
            f"{n_pass}/{len(gates)} gates PASS | branch {branch} | "
            f"split {na} accepted / {nn} NOT-IN-LITERATURE / {nr} "
            f"rejected of {E206.N_ENTRIES}"
            if n_ref == 0 else
            f"REFUTE {n_ref} gate(s) "
            f"({', '.join(k for k, v in gates.items() if v['verdict'] == 'REFUTE')}) "
            f"| split {na}/{nn}/{nr}")

        deposit_sections["exp203_file_untouched_git"] = (
            gates["GATE-N2"].get("exp203_file_untouched_git"))
        deposit = {
            "exp": "exp217_not_in_literature_census",
            "claim": ("THE NOT-IN-LITERATURE CENSUS (L191's registered "
                      "next): the corpus leg's missing W5 fields are "
                      "METHOD-SECTION-DEPTH facts (73/119 records carry "
                      "zero verbatim extracts across all three passes); "
                      "this run IMPLEMENTS exp215's deposited "
                      "specification and re-imports the 119 records "
                      "under the extended census — a record whose "
                      "missing FILL_FIELDS have ZERO extracts across "
                      "all three passes is admitted to "
                      "census_state='NOT-IN-LITERATURE' with the "
                      "missing field list; every other acceptance rule "
                      "unchanged"),
            "pre_registered": {
                "gates_source": ("module docstring, committed before "
                                 "any run (pre-registration d52addd, "
                                 "batch 11; gates N1-N4 fixed there, "
                                 "each evaluated exactly once)"),
                "gates": [
                    "GATE-N1 (the evidence check) 119/119 records "
                    "carry a verdict; the three sources files complete "
                    "(119 records each); each file's sha256 in the "
                    "deposit",
                    "GATE-N2 (the zero-extract assertion) every record "
                    "admitted to NOT-IN-LITERATURE has zero extracts "
                    "in ALL THREE passes for EVERY missing field; any "
                    "record with an extract for a missing field is "
                    "NOT admissible (the discipline holds)",
                    "GATE-N3 (the split) n_normal_accepted + "
                    "n_not_in_literature + n_rejected = 119; ALL of "
                    "exp215's 73 zero-extract records land "
                    "NOT-IN-LITERATURE or better; the realized counts "
                    "deposited; the branch named: CLOSED-NIL (>= 73 "
                    "land in the state and zero integrity violations) "
                    "/ PARTIAL",
                    "GATE-N4 (hygiene) the w5b and w5c banks "
                    "byte-unchanged; the new bank deterministic "
                    "(merge re-run bit-identical); zero fields "
                    "without provenance"]},
            "instruments": {
                "spec_deposit": "results/exp215_w5_figure_pass.json",
                "spec_deposit_sha256":
                    E206.sha256_file(SPEC_DEPOSIT),
                "machinery": ("experiments/exp206_w5_dose_pass.py "
                              "VERBATIM (read_sources, w5_fills, "
                              "validate_row, ser, sha256 helpers)"),
                "machinery_sha256": E206.sha256_file(
                    os.path.join(ROOT, "experiments",
                                 "exp206_w5_dose_pass.py")),
                "exp203_file_sha256": exp203_sha0,
                "census_extension": _NIL_QUOTE},
            "sections": deposit_sections,
            "gates": gates,
            "bank": os.path.relpath(bank_path, ROOT),
            "sources": [os.path.relpath(p, ROOT)
                        for p in (W5_SOURCES, W5B_SOURCES, W5C_SOURCES)],
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(deposit, f, indent=1, default=float)
        print(f"  === {verdict} ===")
        print(f"  deposited {out_path} | bank {bank_path}")
        return deposit

    # smoke: pipeline check only, discarded
    print(f"  SMOKE: {len(bank4['entries'])} accepted / "
          f"{len(bank4['not_in_literature'])} NOT-IN-LITERATURE / "
          f"{len(bank4['rejects'])} rejected on the first {n_take} "
          f"records - DISCARDED (no deposit, no gates)")
    return {"exp": "exp217_not_in_literature_census", "smoke": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
