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

SMOKE_OUT = os.path.join(ROOT, "results", "exp206_w5_dose_pass_smoke.json")
SMOKE_BANK = os.path.join(ROOT, "results", "wetlab_companion_bank_w5_smoke.json")

# thread hygiene (before numeric imports; the scaffold module does the same)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

# ======================================================================
# INSTRUMENTS — the exp203 scaffold + validator VERBATIM (the acceptance
# predicate IS the scaffold's required-field census; zero new acceptance
# rules), the FROZEN baseline bank (read, never rewritten), the series
# records, and the sources file the sweep wrote.
# ======================================================================
from experiments.exp203_wetlab_scaffold import (  # noqa: E402
    BANK as BASELINE_BANK,
    CENSUS_RULE,
    EXTENDED_FIELDS,
    FIELD_PROVENANCE,
    N_ENTRIES,
    REQUIRED_FIELDS,
    SERIES,
    census_missing,
    map_entry,
    ser,
    sha256_file,
    sha256_obj,
    validate_bank,
    bank_field_coverage,
    validate_row,
)

# the pass's W5 columns (the census gaps the literature sweep fills; the
# docstring's "concentration / blocker / phenotype / n" plus the
# exposure-mode encoding the census's exposure_window bullet accepts)
FILL_FIELDS = ["concentration_mM", "blocker", "phenotype_score", "n",
               "exposure_mode"]

# ---- pre-named W5 fill rules (the merge is a pure function of the
# ---- baseline row + the record's sources-file extracts) ----------------
FILL_RULES = {
    "ordering":
        "extracts are tried in the deterministic order (source rank as "
        "returned, then statement order in the sources file); the first "
        "admissible extract wins; ties impossible",
    "fill_never_overwrite":
        "a field is filled ONLY when the baseline row's value is null "
        "(the exp203 import's own reading is never overwritten)",
    "concentration_mM":
        "first extract of kind 'concentration' whose value_mM is a "
        "number > 0; the extractor (scripts/exp206_w5_sources_sweep.mjs, "
        "deposited alongside) only emits a statement whose stated unit "
        "is the protocol's declared mM or convertible to it by factor "
        "arithmetic (uM/µM/μM -> 1e-3, nM -> 1e-6, M -> 1e3), only when "
        "the statement is not a range endpoint, and — when the record "
        "carries keyed drugs (drug_start_end) — only when one of the "
        "record's own drug tokens is stated in the same snippet "
        "(L335's keyed drug taxonomy); %-of-solution statements are NOT "
        "emitted (mM conversion would need molar mass: inference)",
    "blocker":
        "first extract of kind 'blocker' — the extractor emits a record "
        "candidate drug token (the record's own drug_start_end names "
        "plus capitalized tokens of its own manipulation string, minus "
        "a fixed stopword lexicon) only when that token is stated "
        "verbatim in a returned snippet; the value copied is the "
        "record's token itself",
    "phenotype_score":
        "first extract of kind 'phenotype' — a verbatim stated "
        "penetrance ('X% of animals/worms/planarians/...') mapped to "
        "the schema's [0,1] score by X/100; no other phenotype reading "
        "is taken",
    "n":
        "first extract of kind 'n' with an integer >= 1 — verbatim "
        "'n = k' or 'k <count-noun>' statements only",
    "exposure_mode":
        "first extract of kind 'exposure_mode' — the protocol's own "
        "encoding tokens ('sustained'/'pulse') stated verbatim; numeric "
        "literature exposure windows are NOT mapped (the schema carries "
        "no unit, and a unit conversion would be inference)",
    "provenance":
        "rows whose record has a sources-file entry carry "
        "provenance.source_deposit = results/w5_pass_sources.json, "
        "source_record = the per-record locator in it, source_key = the "
        "series record id, source_record_sha256 = sha256 of the "
        "canonical JSON of that exact sources-file record (the keyed, "
        "re-runnable chain of L335-336); records with no sources-file "
        "entry keep the scaffold import's original provenance; every "
        "literature-filled field's own provenance (url + host + "
        "retrieved date + verbatim quote) is deposited per record in "
        "the pass deposit's verdicts (the row schema of the protocol "
        "has no per-field slot)",
}

# ---- sources file reading ----------------------------------------------

def read_sources(path: str) -> dict:
    """The sources file the sweep wrote; absent/empty file => the
    registered empty-sources mode (0 accepted, negative sweep)."""
    if not os.path.exists(path):
        return {"mode": "empty", "doc": None,
                "by_id": {}, "n_records": 0}
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    recs = doc.get("records") or []
    mode = ("empty" if not recs else
            ("full" if len(recs) >= N_ENTRIES else "partial"))
    return {"mode": mode, "doc": doc,
            "by_id": {r["id"]: r for r in recs}, "n_records": len(recs)}


def _extract_order(src_rec: dict, kind: str) -> list:
    """All extracts of a kind, in the pre-named deterministic order:
    source rank as returned (unknown rank last), then statement order."""
    out = []
    for ex in src_rec.get("extracts", []):
        if ex.get("kind") == kind:
            out.append(ex)
    ranked = [e for e in out if isinstance(e.get("rank"), int)]
    unranked = [e for e in out if not isinstance(e.get("rank"), int)]
    ranked.sort(key=lambda e: e["rank"])
    return ranked + unranked


def w5_fills(row: dict, series_entry: dict, src_rec: dict) -> dict:
    """The pre-named fill rules applied to one record.  Returns
    {field: value}; pure."""
    has_keyed_drugs = bool(series_entry.get("drug_start_end"))
    fills = {}
    for field in FILL_FIELDS:
        if row.get(field) is not None:
            continue  # fill, never overwrite
        if field == "concentration_mM":
            for ex in _extract_order(src_rec, "concentration"):
                v = ex.get("value_mM")
                if isinstance(v, (int, float)) and not isinstance(v, bool) \
                        and v > 0 and (ex.get("drug") or not has_keyed_drugs):
                    fills[field] = float(v)
                    break
        elif field == "blocker":
            for ex in _extract_order(src_rec, "blocker"):
                d = ex.get("drug")
                if isinstance(d, str) and d.strip():
                    fills[field] = d
                    break
        elif field == "phenotype_score":
            for ex in _extract_order(src_rec, "phenotype"):
                v = ex.get("value")
                if isinstance(v, (int, float)) and not isinstance(v, bool) \
                        and 0.0 <= v <= 1.0:
                    fills[field] = float(v)
                    break
        elif field == "n":
            for ex in _extract_order(src_rec, "n"):
                v = ex.get("value")
                if isinstance(v, int) and not isinstance(v, bool) and v >= 1:
                    fills[field] = int(v)
                    break
        elif field == "exposure_mode":
            for ex in _extract_order(src_rec, "exposure_mode"):
                v = ex.get("value")
                if v in ("sustained", "pulse"):
                    fills[field] = v
                    break
    return fills


_KIND_OF = {"concentration_mM": "concentration", "blocker": "blocker",
            "phenotype_score": "phenotype", "n": "n",
            "exposure_mode": "exposure_mode"}


def _fill_provenance(field: str, value, src_rec: dict) -> dict:
    """The provenance of the winning extract for one filled field:
    url + retrieved date + the verbatim quote (GATE-D2)."""
    kind = _KIND_OF[field]
    for ex in _extract_order(src_rec, kind):
        if kind == "concentration":
            v = ex.get("value_mM")
            ok = isinstance(v, (int, float)) and not isinstance(v, bool) \
                and v > 0
        elif kind == "blocker":
            v = ex.get("drug")
            ok = isinstance(v, str) and bool(v.strip())
        elif kind == "phenotype":
            v = ex.get("value")
            ok = isinstance(v, (int, float)) and not isinstance(v, bool) \
                and 0.0 <= v <= 1.0
        elif kind == "n":
            v = ex.get("value")
            ok = isinstance(v, int) and not isinstance(v, bool) and v >= 1
        else:
            v = ex.get("value")
            ok = v in ("sustained", "pulse")
        if ok and value == v:
            return {"url": ex.get("url"), "host_name": ex.get("host"),
                    "source_name": ex.get("name"), "rank": ex.get("rank"),
                    "retrieved": src_rec.get("retrieved"),
                    "verbatim_quote": ex.get("quote"),
                    "stated": {k: ex.get(k) for k in
                               ("value_stated", "unit_stated", "pct_stated",
                                "token_stated", "drug") if k in ex}}
    raise AssertionError(f"no extract backs the filled field {field}")


# ---- the pass pipeline (pure; no clock, no randomness) -----------------

def run_pipeline(sources_path: str) -> tuple:
    with open(SERIES, "r", encoding="utf-8") as f:
        series = json.load(f)["series"]
    assert len(series) == N_ENTRIES, len(series)
    baseline_sha = sha256_file(BASELINE_BANK)
    with open(BASELINE_BANK, "r", encoding="utf-8") as f:
        baseline = json.load(f)
    src = read_sources(sources_path)
    entries, rejects, verdicts = [], [], []
    for i, e in enumerate(series):
        row = map_entry(e)  # the scaffold's import, VERBATIM
        baseline_row = dict(row)
        src_rec = src["by_id"].get(e["id"])
        lit_prov = {}
        if src_rec is not None:
            fills = w5_fills(row, e, src_rec)
            for field, value in fills.items():
                row[field] = value
                lit_prov[field] = _fill_provenance(field, value, src_rec)
            row["provenance"] = {
                "source_deposit": "results/w5_pass_sources.json",
                "source_record":
                    f"results/w5_pass_sources.json#records.{e['id']}",
                "source_key": e["id"],
                "source_record_sha256": sha256_obj(src_rec),
            }
        cm = census_missing(row)
        struct_ok = not validate_row(row, allow_census_missing=bool(cm))
        accepted = not cm and struct_ok and not validate_row(row)
        reasons = _reasons(row, e, src_rec, cm)
        verdict = {
            "index": i,
            "id": e["id"],
            "status": "accepted" if accepted else "still-rejected",
            "census_missing": cm,
            "reasons": reasons,
            "sources_tried": (len(src_rec.get("sources_tried", []))
                              if src_rec else 0),
            "extracts_considered": {
                k: sum(1 for ex in (src_rec or {}).get("extracts", [])
                       if ex.get("kind") == k)
                for k in ("concentration", "blocker", "phenotype", "n",
                          "exposure_mode")},
            "literature_filled": {
                f: lit_prov[f] for f in FILL_FIELDS if f in lit_prov},
            "baseline_row_sha256": sha256_obj(baseline_row),
        }
        if accepted:
            entries.append(row)
        else:
            rejects.append(dict(row, census_missing=cm))
        verdicts.append(verdict)
    counts = {"imported": len(series), "accepted": len(entries),
              "rejected": len(rejects)}
    bank = {
        "bank": "wetlab_companion",
        "protocol": "docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md",
        "protocol_sha256": sha256_file(
            os.path.join(ROOT, "docs",
                         "STAGE5_WETLAB_COMPANION_PROTOCOL.md")),
        "schema_version": "1.0",
        "field_provenance": FIELD_PROVENANCE,
        "required_fields": list(REQUIRED_FIELDS),
        "extended_fields": list(EXTENDED_FIELDS),
        "census_rule": CENSUS_RULE,
        # exp203's validator requires every import_rules KEY to be a
        # field in the provenance table; the procedural rules are
        # payload (import_source is a known envelope container whose
        # sub-keys are data), not schema fields
        "import_source": {
            "baseline": "results/wetlab_companion_bank.json (the frozen "
                        "0/119 baseline; read, never rewritten)",
            "series_records": "research/levin_voltage_series.json#series",
            "w5_sources": os.path.relpath(sources_path, ROOT),
            "w5_sources_records": src["n_records"],
            "w5_sources_mode": src["mode"],
            "pass_rules": {
                "ordering": FILL_RULES["ordering"],
                "fill_never_overwrite":
                FILL_RULES["fill_never_overwrite"],
                "base_rows": "the exp203 scaffold's map_entry, VERBATIM "
                             "(the acceptance predicate is the "
                             "scaffold's required-field census; zero "
                             "new acceptance rules)"}},
        "import_rules": {k: v for k, v in FILL_RULES.items()
                         if k not in ("ordering", "fill_never_overwrite")},
        "entries": entries,
        "rejects": rejects,
        "counts": counts,
    }
    fill_rates = {}
    for f in FILL_FIELDS:
        lit = sum(1 for v in verdicts if f in v["literature_filled"])
        base = sum(1 for e2 in series
                   if map_entry(e2)[f] is not None)
        total = sum(1 for r in entries + rejects if r.get(f) is not None)
        fill_rates[f] = {"baseline_derived": base, "literature_filled": lit,
                         "total_nonnull": total, "of": N_ENTRIES}
    ctx = {"series": series, "baseline": baseline,
           "baseline_sha": baseline_sha, "src": src, "verdicts": verdicts,
           "fill_rates": fill_rates, "counts": counts}
    return bank, ctx


def _reasons(row, e, src_rec, cm) -> list:
    """Per-record reasons for staying rejected (census items named, with
    the record-specific blocking detail)."""
    if not cm:
        return []
    n_tried = len(src_rec.get("sources_tried", [])) if src_rec else 0
    if src_rec is None:
        return [f"{'all census items'}: no sources-file entry for this "
                f"record (search not run or failed) — sources_tried=0"]
    reasons = []
    for item in cm:
        if item == "concentration":
            got = sum(1 for ex in src_rec.get("extracts", [])
                      if ex.get("kind") == "concentration")
            reasons.append(
                f"concentration: no admissible verbatim-stated "
                f"concentration (mM/uM/nM/M tied to the record's keyed "
                f"drug, non-range) in {n_tried} tried sources "
                f"({got} raw candidate statements rejected by the "
                f"verbatim rules)")
        elif item == "blocker_or_vehicle":
            reasons.append(
                "blocker_or_vehicle: the record states no drug_start_end "
                "and no candidate blocker token of the record was stated "
                f"verbatim in {n_tried} tried sources")
        elif item == "exposure_window":
            reasons.append(
                "exposure_window: the record states no drug_start_end "
                "window and no verbatim 'sustained'/'pulse' token was "
                f"stated in {n_tried} tried sources")
        elif item == "phenotype_score":
            reasons.append(
                "phenotype_score: no verbatim stated penetrance "
                f"('X% of animals/...') in {n_tried} tried sources")
        elif item == "n":
            reasons.append(
                f"n: no verbatim 'n = k' / 'k <count-noun>' statement "
                f"in {n_tried} tried sources")
        else:
            reasons.append(f"{item}: unpopulated")
    return reasons

# ======================================================================
# GATES — each evaluated exactly once, as pre-registered.
# ======================================================================

def gate_d1(ctx, bank) -> dict:
    """GATE-D1 (the pass runs): all 119 records swept; per-record
    verdicts (accepted / still-rejected + reasons + sources-tried)
    deposited; the sweep is complete, not sampled."""
    assert len(ctx["series"]) == N_ENTRIES == 119
    assert len(ctx["verdicts"]) == N_ENTRIES
    ids = [v["id"] for v in ctx["verdicts"]]
    assert len(set(ids)) == N_ENTRIES
    assert set(ids) == {e["id"] for e in ctx["series"]}
    for v in ctx["verdicts"]:
        assert v["status"] in ("accepted", "still-rejected"), v
        assert isinstance(v["reasons"], list) and v["reasons"] or \
            v["status"] == "accepted", v["id"]
        assert isinstance(v["sources_tried"], int), v["id"]
        assert set(v["census_missing"]) <= {
            it["item"] for it in CENSUS_RULE} or v["status"] == "accepted"
    n_acc = sum(1 for v in ctx["verdicts"] if v["status"] == "accepted")
    assert n_acc == len(bank["entries"])
    return {
        "verdict": "PASS",
        "asserts": {
            "all_119_records_swept": True,
            "per_record_verdicts_deposited": len(ctx["verdicts"]),
            "every_verdict_carries_status_reasons_sources_tried": True,
            "accepted_matches_bank_entries": True,
        },
        "detail": {
            "sources_mode": ctx["src"]["mode"],
            "sources_records": ctx["src"]["n_records"],
            "records_with_search_results": sum(
                1 for v in ctx["verdicts"] if v["sources_tried"] > 0),
            "accepted": n_acc,
        },
    }


def gate_d2(ctx, bank) -> dict:
    """GATE-D2 (acceptance integrity): every accepted entry validates
    through the exp203 scaffold's validator; every accepted W5 field
    carries source provenance; zero fields without provenance."""
    for r in bank["entries"]:
        assert not census_missing(r), r["provenance"]["source_key"]
        assert not validate_row(r), (r["provenance"]["source_key"],
                                     validate_row(r))
        # every non-null W5 field on an accepted row is either the
        # baseline import's own reading (scaffold IMPORT_RULES chain) or
        # literature-filled with url+retrieved provenance in the verdict
        v = next(x for x in ctx["verdicts"]
                 if x["id"] == r["provenance"]["source_key"])
        for f in FILL_FIELDS:
            if r[f] is None:
                continue
            prov = v["literature_filled"].get(f)
            if prov is None:
                # baseline-derived: must equal the scaffold import's value
                base = next(e2 for e2 in ctx["series"]
                            if e2["id"] == r["provenance"]["source_key"])
                assert r[f] == map_entry(base)[f], (r["provenance"][
                    "source_key"], f)
            else:
                assert prov.get("url"), (r["provenance"]["source_key"], f)
                assert prov.get("retrieved"), (
                    r["provenance"]["source_key"], f)
                assert prov.get("verbatim_quote"), (
                    r["provenance"]["source_key"], f)
    for r in bank["rejects"]:
        assert r["census_missing"], r["provenance"]["source_key"]
        assert not validate_row(r, allow_census_missing=True), \
            (r["provenance"]["source_key"], validate_row(r, True))
    assert validate_bank(bank) == [], validate_bank(bank)
    unprov = bank_field_coverage(bank)
    assert not unprov, unprov
    # the validator's accept path exercised non-vacuously regardless of
    # the accepted count: the scaffold's own G3 fixture must validate
    from experiments.exp203_wetlab_scaffold import _FIXTURE  # noqa: E402
    assert not validate_row(_FIXTURE) and not census_missing(_FIXTURE)
    return {
        "verdict": "PASS",
        "asserts": {
            "every_accepted_entry_validates_exp203": True,
            "every_accepted_w5_field_provenanced": True,
            "zero_fields_without_provenance": True,
            "every_reject_structure_clean_census_named": True,
            "bank_validates_exp203": True,
            "validator_accept_path_nonvacuous_fixture": True,
        },
        "detail": {
            "accepted": len(bank["entries"]),
            "accepted_ids": [r["provenance"]["source_key"]
                             for r in bank["entries"]],
            "literature_filled_fields_total": sum(
                len(v["literature_filled"]) for v in ctx["verdicts"]),
        },
    }


def gate_d3(ctx, bank) -> dict:
    """GATE-D3 (the yield — the finding): the accepted count deposited
    against the 0/119 baseline; the per-field fill rates deposited; the
    still-rejected list carries the reasons."""
    bc = ctx["baseline"]["counts"]
    assert bc == {"imported": N_ENTRIES, "accepted": 0,
                  "rejected": N_ENTRIES}, bc
    c = bank["counts"]
    assert c["imported"] == N_ENTRIES
    assert c["accepted"] == len(bank["entries"]) == sum(
        1 for v in ctx["verdicts"] if v["status"] == "accepted")
    assert c["rejected"] == len(bank["rejects"])
    assert c["accepted"] + c["rejected"] == N_ENTRIES
    for f, fr in ctx["fill_rates"].items():
        assert fr["of"] == N_ENTRIES
        assert fr["total_nonnull"] == sum(
            1 for r in bank["entries"] + bank["rejects"]
            if r.get(f) is not None), f
    for v in ctx["verdicts"]:
        if v["status"] == "still-rejected":
            assert v["reasons"], v["id"]
    return {
        "verdict": "PASS",
        "verdict_note": "the yield is a FINDING (pre-registered), not a "
                        "gate failure: the gate is that the accepted "
                        "count, the per-field fill rates and the "
                        "still-rejected reasons are deposited and "
                        "reconcile with the 0/119 baseline",
        "asserts": {
            "baseline_is_0_of_119": True,
            "accepted_count_deposited_against_baseline": True,
            "per_field_fill_rates_reconcile": True,
            "every_still_rejected_carries_reasons": True,
        },
        "detail": {
            "baseline_counts": bc,
            "accepted": c["accepted"],
            "fill_rates": ctx["fill_rates"],
            "still_rejected": c["rejected"],
        },
    }


def gate_d4(ctx, bank, bank_path: str, sources_path: str) -> dict:
    """GATE-D4 (hygiene): the frozen baseline bank byte-unchanged; the
    new bank deterministic (re-run reproduces it byte-identically given
    the same sources file); the sources file deposited alongside."""
    assert sha256_file(BASELINE_BANK) == ctx["baseline_sha"], \
        "frozen baseline bank mutated"
    bank2, _ = run_pipeline(sources_path)
    b1, b2 = ser(bank), ser(bank2)
    assert b1 == b2, "re-run not byte-identical given the same sources file"
    with open(bank_path, "rb") as f:
        raw = f.read()
    assert raw == b2.encode("utf-8"), "written bank != re-run bank"
    for label, path in (("protocol", os.path.join(
            ROOT, "docs", "STAGE5_WETLAB_COMPANION_PROTOCOL.md")),
            ("series", SERIES), ("scaffold", os.path.join(
                ROOT, "experiments", "exp203_wetlab_scaffold.py"))):
        assert os.path.exists(path), label
    assert os.path.exists(sources_path), "sources file not deposited"
    return {
        "verdict": "PASS",
        "asserts": {
            "frozen_baseline_bank_byte_unchanged": True,
            "new_bank_deterministic_rerun_byte_identical": True,
            "written_bank_equals_rerun": True,
            "sources_file_deposited": True,
        },
        "detail": {
            "baseline_bank_sha256": ctx["baseline_sha"],
            "sources_file_sha256": sha256_file(sources_path),
            "bank_bytes": len(raw),
        },
    }

# ======================================================================
# main
# ======================================================================

GATE_FUNCS = {"d1": gate_d1, "d2": gate_d2, "d3": gate_d3, "d4": gate_d4}


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--sources", default=None)
    args, _ = ap.parse_known_args()
    sources_path = args.sources or SOURCES
    if args.job == "all":
        jobs = ["d1", "d2", "d3", "d4"]
    else:
        jobs = [j.strip().lower() for j in args.job.split(",") if j.strip()]
        unknown = [j for j in jobs if j not in GATE_FUNCS]
        assert not unknown, f"unknown --job gates: {unknown}"
    bank_path = SMOKE_BANK if args.smoke else BANK
    bank, ctx = run_pipeline(sources_path)
    # the pass's product: the NEW bank file (deterministic serialization;
    # D4 re-runs the pipeline and asserts byte-identity against this)
    os.makedirs(os.path.dirname(bank_path), exist_ok=True)
    with open(bank_path, "w", encoding="utf-8") as f:
        f.write(ser(bank))
    gates = {}
    for j in jobs:
        try:
            if j == "d4":
                gates["GATE-D4"] = gate_d4(ctx, bank, bank_path,
                                           sources_path)
            else:
                gates[f"GATE-{j.upper()}"] = GATE_FUNCS[j](ctx, bank)
        except AssertionError:
            import traceback as _tb
            tb = _tb.format_exc().strip().splitlines()
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
    acc = bank["counts"]["accepted"]
    verdict = (
        f"PASS {n_pass}/{len(evaluated)} gates — the W5 dose-identity "
        f"literature pass swept all 119 records and moved the bank to "
        f"{acc}/{N_ENTRIES} accepted (baseline 0/119; "
        f"{bank['counts']['rejected']} still rejected with per-record "
        f"reasons); every accepted entry validates through the exp203 "
        f"scaffold's validator with per-field source provenance; "
        f"frozen baseline byte-unchanged, new bank deterministic"
        if all_pass else
        f"REFUTE {n_ref}/{len(evaluated)} gates failed "
        f"({', '.join(k for k, v in evaluated.items() if v['verdict'] == 'REFUTE')}); "
        f"accepted {acc}/{N_ENTRIES} vs baseline 0/119")
    deposit = {
        "exp": "exp206_w5_dose_pass",
        "task": "THE W5 DOSE-IDENTITY LITERATURE PASS (L176's registered "
                "next): a targeted literature sweep filling the wetlab "
                "companion bank's W5 dose-identity columns per record on "
                "the 119-entry Levin voltage series, the exp203 scaffold "
                "validating on acceptance, against the frozen 0/119 "
                "baseline",
        "instruments": {
            "scaffold": "experiments/exp203_wetlab_scaffold.py "
                        "(validator + required-field census VERBATIM; "
                        "zero new acceptance rules)",
            "scaffold_sha256": sha256_file(os.path.join(
                ROOT, "experiments", "exp203_wetlab_scaffold.py")),
            "baseline_bank": "results/wetlab_companion_bank.json (frozen; "
                             "read, never rewritten)",
            "baseline_bank_sha256": ctx["baseline_sha"],
            "baseline_counts": ctx["baseline"]["counts"],
            "series_records": "research/levin_voltage_series.json#series",
            "series_sha256": sha256_file(SERIES),
            "sweep_script": "scripts/exp206_w5_sources_sweep.mjs",
            "sources_file": os.path.relpath(sources_path, ROOT),
            "sources_mode": ctx["src"]["mode"],
            "search_protocol": "per record: one z-ai web_search whose "
                               "query is the record's own "
                               "title/authors/year/name fields (source, "
                               "pmid_or_doi, species, region_or_tissue, "
                               "manipulation, id) joined verbatim — zero "
                               "knobs; fields copied ONLY when a source "
                               "states them verbatim; every accepted "
                               "field carries source provenance (url + "
                               "retrieved date)",
        },
        "field_provenance": FIELD_PROVENANCE,
        "required_fields": REQUIRED_FIELDS,
        "extended_fields": EXTENDED_FIELDS,
        "census_rule": CENSUS_RULE,
        "w5_fill_rules": FILL_RULES,
        "bank_pointer": os.path.relpath(bank_path, ROOT),
        "counts": dict(bank["counts"], baseline_accepted=0),
        "fill_rates": ctx["fill_rates"],
        "verdicts": ctx["verdicts"],
        "gates": gates,
        "criteria": {
            "GATE-D1": "all 119 records swept; per-record verdicts "
                       "(accepted / still-rejected + reasons + "
                       "sources-tried) deposited; the sweep is complete, "
                       "not sampled",
            "GATE-D2": "every accepted entry validates through the exp203 "
                       "scaffold's validator; every accepted W5 field "
                       "carries source provenance; zero fields without "
                       "provenance",
            "GATE-D3": "the accepted count deposited against the 0/119 "
                       "baseline; the per-field fill rates (concentration "
                       "/ blocker / phenotype / n) deposited; the "
                       "still-rejected list carries the reasons",
            "GATE-D4": "the frozen baseline bank byte-unchanged; the new "
                       "bank deterministic (re-run reproduces it "
                       "byte-identically given the same sources file); "
                       "the sources file (per-record raw extracts) "
                       "deposited alongside",
        },
        "verdict": verdict,
        "notes": (
            "The acceptance predicate is the exp203 scaffold's "
            "required-field census and validator VERBATIM: a record is "
            "accepted only when all seven protocol bullets (species, "
            "blocker/vehicle, concentration, exposure window, "
            "amputation plane, phenotype score, n) are populated and the "
            "row is structure-clean. The baseline rows already carry "
            "species/planes/exposure windows (from the series' "
            "drug_start_end), phenotype scores (1 - freq(Wild type)) and "
            "n where stated; the pass fills ONLY null fields, never "
            "overwrites. Concentration is the census item all 119 "
            "records miss; the sweep's verbatim rules (stated "
            "mM/uM/nM/M tied to the record's own keyed drug, ranges "
            "excluded, %-of-solution statements not convertible without "
            "molar mass) copy what the returned snippets state and no "
            "more. The search endpoint returns host-level URLs; they are "
            "deposited as returned, with the verbatim snippet as the "
            "quote. In the registered empty-sources mode (proxy "
            "unrecoverable) every record stays rejected with its "
            "reason and the gates still evaluate honestly. Smoke runs "
            "(records 0-4, permitted, discarded) write only the "
            "_smoke paths."),
        "sources": {
            "protocol": "docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md (the "
                        "W5 deposit schema, L334-348; the ONLY schema "
                        "source)",
            "scaffold": "experiments/exp203_wetlab_scaffold.py (the "
                        "validator/census instrument)",
            "baseline_bank": "results/wetlab_companion_bank.json (the "
                             "frozen 0/119 baseline)",
            "series_records": "research/levin_voltage_series.json#series "
                              "(119 records)",
            "sources_file": os.path.relpath(sources_path, ROOT) +
                            " (the sweep's per-record raw extracts, "
                            "written by "
                            "scripts/exp206_w5_sources_sweep.mjs)",
            "search_backend": "z-ai web_search "
                              "(z-ai-web-dev-sdk functions.invoke), the "
                              "backend fronted by the OpenAI-compatible "
                              "proxy at http://localhost:8787/v1",
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
    ap.add_argument("--sources", default=None)
    _args = ap.parse_args()
    _res = main()
    _out_path = _args.out or (SMOKE_OUT if _args.smoke else OUT)
    _dep = dict(_res)
    _dep["deposit_path"] = os.path.relpath(_out_path, ROOT)
    with open(_out_path, "w", encoding="utf-8") as _f:
        _f.write(ser(_dep))
    print(f"exp206 deposit -> {_out_path}")
    print(f"exp206 verdict: {_res['verdict']}")
    sys.exit(0 if _res["gates_all_pass"] else 1)
