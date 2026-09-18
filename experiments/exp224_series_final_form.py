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
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import hashlib
    import time

    import experiments.exp206_w5_dose_pass as E206  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    # --job accepted for batch CLI parity; the registered run is the
    # single full export ("all"); --smoke is a pipeline check,
    # discarded (no artifact write, no deposit, no gates).

    CENSUS = os.path.join(ROOT, "results",
                          "exp217_not_in_literature_census.json")
    W5D = os.path.join(ROOT, "results",
                       "wetlab_companion_bank_w5d.json")
    W5_SOURCES = E206.SOURCES                     # pass 1 (frozen)
    W5B_SOURCES = os.path.join(ROOT, "results",
                               "w5_pass_sources2.json")  # pass 2
    W5C_SOURCES = os.path.join(ROOT, "results",
                               "w5_pass_sources3.json")  # pass 3
    E206_PATH = os.path.join(ROOT, "experiments",
                             "exp206_w5_dose_pass.py")

    assert os.path.exists(CENSUS), \
        "exp217's deposited census (the instrument) missing"
    assert os.path.exists(W5D), \
        "the w5d bank (the census's rows) missing"
    for _p in (W5_SOURCES, W5B_SOURCES, W5C_SOURCES):
        assert os.path.exists(_p), f"sources file missing: {_p}"

    # ---- the instruments --------------------------------------------------
    with open(CENSUS, encoding="utf-8") as f:
        census = json.load(f)
    census_sha0 = E206.sha256_file(CENSUS)
    with open(W5D, encoding="utf-8") as f:
        w5d = json.load(f)
    w5d_sha0 = E206.sha256_file(W5D)
    with open(E206.SERIES, encoding="utf-8") as f:
        series_doc = json.load(f)
    series = series_doc["series"]
    series_sha0 = E206.sha256_file(E206.SERIES)
    machinery_sha0 = E206.sha256_file(E206_PATH)

    assert census.get("exp") == "exp217_not_in_literature_census", \
        "the census deposit is not exp217's"
    verdicts = census["sections"]["verdicts"]
    dep_split = census["sections"]["counts_split"]
    dep_sources = {s["file"]: s
                   for s in census["sections"]["sources"]}
    spec = census["sections"]["not_in_literature_spec"]
    assert isinstance(spec, dict) and \
        spec.get("state") == "NOT-IN-LITERATURE", \
        "exp217's deposited not_in_literature_spec missing"
    assert len(verdicts) == len(series) == E206.N_ENTRIES == 119, \
        (len(verdicts), len(series), E206.N_ENTRIES)
    by_id = {v["id"]: v for v in verdicts}
    assert len(by_id) == 119, "exp217's verdict ids are not unique/complete"
    bank_rows: dict = {}
    for r in (list(w5d.get("entries", []))
              + list(w5d.get("not_in_literature", []))
              + list(w5d.get("rejects", []))):
        bank_rows[(r.get("provenance") or {}).get("source_key")] = r
    assert len(bank_rows) == 119, \
        f"the w5d bank's rows are not 119 unique ids ({len(bank_rows)})"

    sources_paths = (W5_SOURCES, W5B_SOURCES, W5C_SOURCES)
    sources_rel = [os.path.relpath(p, ROOT) for p in sources_paths]
    sources_sha = {rel: E206.sha256_file(p)
                   for p, rel in zip(sources_paths, sources_rel)}

    # the FINAL FORM's census_state names (pre-registered, zero knobs)
    DISPLAY = {"accepted": "accepted",
               "not_in_literature": "NOT-IN-LITERATURE",
               "rejected": "rejected-extract-carrying"}

    _SERIES_FIELDS_QUOTE = ("{series fields verbatim, census_state "
                            "(accepted/NOT-IN-LITERATURE/"
                            "rejected-extract-carrying), census_missing "
                            "list, provenance block (exp217's, inline), "
                            "the 8 partial rows' extracts verbatim}")
    _EXTRACTS_QUOTE = ("the 8 partial rows with their per-field "
                       "extracts, verbatim")

    # ==== the projection ===============================================
    def build_export(n_take=None) -> tuple:
        """The export is a projection, ZERO re-derivation: no
        acceptance predicate re-runs here — census_state, census_missing
        and the provenance block are copied from exp217's deposited
        census VERBATIM (cross-checked against the w5d bank's rows),
        the series fields from the row base VERBATIM, the 8 partial
        rows' extracts from the three sources files VERBATIM."""
        paths_by_pass = {1: W5_SOURCES, 2: W5B_SOURCES, 3: W5C_SOURCES}
        src, src_meta = {}, []
        for p in (1, 2, 3):
            s = E206.read_sources(paths_by_pass[p])
            assert s["n_records"] == E206.N_ENTRIES, \
                f"sources pass {p}: {s['n_records']} records"
            src[p] = s["by_id"]
            src_meta.append({"pass": p,
                             "file": sources_rel[p - 1],
                             "sha256": sources_sha[sources_rel[p - 1]],
                             "n_records": s["n_records"],
                             "mode": s["mode"]})

        entries, acc_ids, nil_ids, rej_ids = [], [], [], []
        for e in (series[:n_take] if n_take else series):
            vid = e["id"]
            assert vid in by_id, \
                f"exp217's deposit has no verdict for {vid}"
            assert vid in bank_rows, \
                f"the w5d bank has no row for {vid}"
            v = by_id[vid]          # the deposited verdict — copied,
            brow = bank_rows[vid]   # never re-adjudicated
            row = json.loads(json.dumps(e))   # series fields VERBATIM
            row["census_state"] = DISPLAY[v["state"]]
            row["census_missing"] = list(v["census_missing"])
            if v["state"] == "not_in_literature":
                row["provenance"] = json.loads(
                    json.dumps(brow["provenance"]))  # exp217's, inline
                nil_ids.append(vid)
            elif v["state"] == "rejected":
                row["provenance"] = json.loads(
                    json.dumps(brow["provenance"]))  # exp217's, inline
                row["extracts_by_pass"] = {
                    str(p): json.loads(json.dumps(
                        (src[p].get(vid) or {}).get("extracts", [])))
                    for p in (1, 2, 3)}
                rej_ids.append(vid)
            else:
                row["provenance"] = json.loads(
                    json.dumps(brow.get("provenance") or {}))
                acc_ids.append(vid)
            entries.append(row)

        # the carried extracts are the ones the deposit counted
        # (per-kind counts == exp217's deposited extract_counts)
        for row in entries:
            if "extracts_by_pass" not in row:
                continue
            v = by_id[row["id"]]
            for p in (1, 2, 3):
                got: dict = {}
                for ex in row["extracts_by_pass"][str(p)]:
                    got[ex.get("kind")] = got.get(ex.get("kind"), 0) + 1
                want = {k: n for k, n in
                        v["extract_counts_by_pass"][str(p)].items() if n}
                assert got == want, \
                    (f"{row['id']}: carried extracts drift vs exp217's "
                     f"deposited counts (pass {p}: {got} != {want})")

        # the field-provenance table: the w5d bank's rows VERBATIM +
        # the export's new fields (disclosed, added in this module).
        # The table's universe is derived from the OBSERVED content:
        # the series rows are not uniform (the 99 PlanformDB
        # recorded-outcome rows carry db_experiment_id, db_figure_panel,
        # drug_start_end, outcome_frequencies; 102 rows carry
        # vmem_mv_note) — every carried series field is registered
        # content ("series fields verbatim") and gets its exp224 row.
        # The census keys (census_state, census_missing, provenance +
        # the provenance.* sub-keys) are the w5d table's own rows
        # (exp203's + exp217's NEW_FP describe exactly these fields).
        # 'species' collides with the w5d table's W5-column row; the
        # series field gets its own exp224 row (duplicate field name,
        # disclosed).
        w5d_fields = {r["field"]
                      for r in w5d.get("field_provenance", [])}
        observed = {k for row in entries for k in row}
        _CENSUS_KEYS = {"census_state", "census_missing", "provenance"}
        new_names = sorted(observed - _CENSUS_KEYS - w5d_fields)
        if "species" in observed:
            new_names = ["species"] + new_names
        extract_keys = sorted(
            {k for row in entries
             for exl in (row.get("extracts_by_pass") or {}).values()
             for ex in exl for k in ex})
        new_fields = (new_names
                      + [f"extracts_by_pass.{k}" for k in extract_keys])
        fp_table = (list(w5d.get("field_provenance", []))
                    + [{"field": f,
                        "protocol_line":
                            "exp224 docstring (pre-registered, batch 12)",
                        "quote": (_EXTRACTS_QUOTE
                                  if f.startswith("extracts_by_pass")
                                  else _SERIES_FIELDS_QUOTE)}
                       for f in new_fields])

        split = {"accepted": len(acc_ids),
                 "not_in_literature": len(nil_ids),
                 "rejected": len(rej_ids)}
        artifact = {
            "artifact": "levin_voltage_series_wetlab_final",
            "artifact_file":
                "results/levin_voltage_series_wetlab_final.json",
            "exp": "exp224_series_final_form",
            "title": series_doc.get("title"),
            "counts": dict(split, imported=len(entries)),
            "entries": entries,
            "meta": {
                "row_base": ("research/levin_voltage_series.json#series "
                             "(119 entries; the series fields VERBATIM, "
                             "the row base)"),
                "row_base_sha256": series_sha0,
                "census_deposit":
                    "results/exp217_not_in_literature_census.json",
                "census_deposit_sha256": census_sha0,
                "census_verdict": census.get("verdict"),
                "census_branch":
                    (census.get("gates", {}).get("GATE-N3") or {})
                    .get("branch"),
                "bank": "results/wetlab_companion_bank_w5d.json",
                "bank_sha256": w5d_sha0,
                "sources_files": list(sources_rel),
                "sources_files_sha256": [sources_sha[r]
                                         for r in sources_rel],
                "n_entries": len(entries),
                "split": split,
                "census_spec": spec,   # exp217's spec, VERBATIM inline
                "export_clause": (
                    "the export is a projection, zero re-derivation: "
                    "census_state, census_missing and the provenance "
                    "block are copied from exp217's deposited census "
                    "VERBATIM; the series fields from the row base "
                    "VERBATIM; the 8 partial rows' extracts from the "
                    "three sources files VERBATIM"),
                "hash_discipline": (
                    "meta.artifact_sha256_canonical_payload = sha256 of "
                    "this artifact serialized canonically (indent=1, "
                    "sort_keys) WITHOUT the "
                    "artifact_sha256_canonical_payload slot; the run "
                    "deposit (results/exp224_series_final_form.json) "
                    "records the sha256 of the artifact file bytes"),
                "field_provenance": fp_table,
                "honest_scope": series_doc.get("honest_scope"),
                "protocol": series_doc.get("protocol"),
                "series_created": series_doc.get("created"),
                "series_agent": series_doc.get("agent")}}
        payload_sha = hashlib.sha256(
            E206.ser(artifact).encode("utf-8")).hexdigest()
        artifact["meta"]["artifact_sha256_canonical_payload"] = payload_sha
        return artifact, {"acc": acc_ids, "nil": nil_ids, "rej": rej_ids,
                          "src_meta": src_meta, "new_fields": new_fields}

    artifact, parts = build_export(n_take=3 if args.smoke else None)

    gates = {}
    if not args.smoke:
        def _gate(name, fn):
            # each gate evaluated exactly once; asserts recorded as
            # REFUTE with the failing line (exp206's gate discipline)
            try:
                gates[name] = fn()
            except AssertionError:
                import traceback as _tb
                tb = _tb.format_exc().strip().splitlines()
                gates[name] = {"verdict": "REFUTE",
                               "assert_failure": tb[-1] if tb
                               else "AssertionError"}

        def field_coverage(art) -> list:
            """Zero fields without provenance: every entry's top-level
            key, provenance sub-key and extract sub-key is in the
            artifact's field_provenance table."""
            known = {r["field"]
                     for r in art["meta"]["field_provenance"]}
            missing = []
            for i, row in enumerate(art["entries"]):
                for k in row:
                    if k not in known:
                        missing.append(f"entries[{i}]:{k}")
                p = row.get("provenance") or {}
                if isinstance(p, dict):
                    for k in p:
                        if f"provenance.{k}" not in known:
                            missing.append(f"entries[{i}]:provenance.{k}")
                for exl in (row.get("extracts_by_pass") or {}).values():
                    for ex in exl:
                        for k in ex:
                            if f"extracts_by_pass.{k}" not in known:
                                missing.append(
                                    f"entries[{i}]:extracts_by_pass.{k}")
            return sorted(set(missing))

        def _z1():
            # ---- GATE-Z1 (the projection) ---------------------------
            ids = [r["id"] for r in artifact["entries"]]
            want = [e["id"] for e in series]
            state_ok, missing_ok, prov_ok, nil_live = [], [], [], []
            for row in artifact["entries"]:
                v = by_id[row["id"]]
                brow = bank_rows[row["id"]]
                state_ok.append(
                    row["census_state"] == DISPLAY[v["state"]])
                missing_ok.append(
                    sorted(row["census_missing"])
                    == sorted(v["census_missing"])
                    == sorted(brow.get("census_missing") or []))
                if v["state"] != "accepted":
                    prov_ok.append(bool(row.get("provenance")))
                else:
                    prov_ok.append(True)
                if v["state"] == "not_in_literature":
                    p = row.get("provenance") or {}
                    nil_live.append(
                        brow.get("census_state") == "NOT-IN-LITERATURE"
                        and p.get("sources_files") == list(sources_rel)
                        and p.get("sources_files_sha256")
                        == [sources_sha[r] for r in sources_rel]
                        and p.get("census_state") == "NOT-IN-LITERATURE"
                        and list(p.get("missing_fill_fields") or [])
                        == list(v["missing_fill_fields"])
                        and all(isinstance(p.get(k), str)
                                and len(p.get(k)) == 64
                                for k in
                                ("source_record_sha256",
                                 "pass1_source_record_sha256",
                                 "pass2_source_record_sha256",
                                 "pass3_source_record_sha256")))
            # the three files the NIL provenance names are LIVE: the
            # current hashes == the inline provenance == exp217's
            # deposit-recorded hashes
            dep_live = [
                sources_sha[s["file"]] == s["sha256"]
                and dep_sources.get(s["file"], {}).get("sha256")
                == s["sha256"]
                for s in parts["src_meta"]]
            gaps = field_coverage(artifact)
            ok = (len(artifact["entries"]) == 119
                  and ids == want
                  and all(state_ok) and all(missing_ok)
                  and all(prov_ok) and all(nil_live)
                  and all(dep_live) and not gaps)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "n_exported": len(artifact["entries"]),
                "ids_match_series_order": ids == want,
                "census_state_matches_verdict_per_entry":
                    all(state_ok),
                "census_missing_matches_deposit_and_bank":
                    all(missing_ok),
                "every_non_accepted_row_carries_provenance":
                    all(prov_ok),
                "nil_provenance_inline_live": all(nil_live),
                "sources_files_hash_live_vs_deposit": all(dep_live),
                "zero_fields_without_provenance": not gaps,
                "provenance_gaps": gaps,
                "field_provenance_rows":
                    len(artifact["meta"]["field_provenance"])}

        def _z2():
            # ---- GATE-Z2 (the split integrity) ----------------------
            # compared on the deposit's full key set (the deposited
            # split carries imported=119 beside the 0/111/8 triple)
            got = {"n_normal_accepted": artifact["counts"]["accepted"],
                   "n_not_in_literature":
                       artifact["counts"]["not_in_literature"],
                   "n_rejected": artifact["counts"]["rejected"],
                   "imported": artifact["counts"]["imported"]}
            # any drift raises (the registered clause)
            assert got == dep_split, \
                (f"split drift: exported {got} != exp217's deposited "
                 f"{dep_split}")
            assert (got["n_normal_accepted"],
                    got["n_not_in_literature"],
                    got["n_rejected"]) == (0, 111, 8), \
                f"split drift vs the registered 0/111/8: {got}"
            assert got["n_normal_accepted"] \
                + got["n_not_in_literature"] \
                + got["n_rejected"] == 119
            assert w5d.get("counts") == {"imported": 119,
                                         "normal_accepted": 0,
                                         "not_in_literature": 111,
                                         "rejected": 8}, w5d.get("counts")
            dep_state = {v["id"]: v["state"] for v in verdicts}
            assert sorted(parts["acc"] + parts["nil"] + parts["rej"]) \
                == sorted(dep_state), "id partition drift"
            assert sorted(
                i for i, s in dep_state.items()
                if s == "not_in_literature") == sorted(parts["nil"]), \
                "NOT-IN-LITERATURE id set drift vs exp217's deposit"
            assert sorted(
                i for i, s in dep_state.items()
                if s == "rejected") == sorted(parts["rej"]), \
                "rejected id set drift vs exp217's deposit"
            return {
                "verdict": "PASS",
                "exported_split": artifact["counts"],
                "exp217_deposited_split": dep_split,
                "bank_counts": w5d.get("counts"),
                "id_partition_matches_deposit": True,
                "n_accepted": got["n_normal_accepted"],
                "n_not_in_literature": got["n_not_in_literature"],
                "n_rejected": got["n_rejected"]}

        def _z3():
            # ---- GATE-Z3 (the wetlab self-containment) --------------
            blob = E206.ser(artifact)
            reparsed = json.loads(blob)     # parses standalone
            IDF = ("id", "source", "pmid_or_doi", "species",
                   "region_or_tissue")
            ser_by_id = {e["id"]: e for e in series}
            ident_bad = []
            for row in reparsed["entries"]:
                src_e = ser_by_id[row["id"]]
                ok_i = (all(k in row for k in IDF)
                        and all(row[k] == src_e.get(k) for k in IDF)
                        and all(row.get(k) for k in
                                ("id", "source", "species",
                                 "region_or_tissue")))
                if not ok_i:
                    ident_bad.append(row.get("id"))
            dep_sha_now = E206.sha256_file(CENSUS)
            meta = reparsed["meta"]
            payload = json.loads(blob)
            claimed = payload["meta"].pop(
                "artifact_sha256_canonical_payload")
            recomputed = hashlib.sha256(
                E206.ser(payload).encode("utf-8")).hexdigest()
            sha_ok = (claimed == recomputed
                      and isinstance(claimed, str) and len(claimed) == 64)
            dep_ok = (meta.get("census_deposit_sha256") == dep_sha_now
                      and isinstance(dep_sha_now, str)
                      and len(dep_sha_now) == 64)
            ok = (not ident_bad and sha_ok and dep_ok
                  and meta.get("n_entries") == 119)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "parses_standalone": True,
                "identity_fields": list(IDF),
                "identity_violations": ident_bad,
                "artifact_sha256_canonical_payload": claimed,
                "artifact_payload_sha_ok": sha_ok,
                "census_deposit_sha256": dep_sha_now,
                "census_deposit_sha_ok": dep_ok,
                "n_entries_meta": meta.get("n_entries")}

        def _z4():
            # ---- GATE-Z4 (hygiene) ----------------------------------
            os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
            blob = E206.ser(artifact)
            with open(ARTIFACT, "w", encoding="utf-8") as f:
                f.write(blob)
            artifact_rerun, _parts2 = build_export()
            determinism = E206.ser(artifact_rerun) == blob
            census_sha1 = E206.sha256_file(CENSUS)
            w5d_sha1 = E206.sha256_file(W5D)
            series_sha1 = E206.sha256_file(E206.SERIES)
            ok = (census_sha1 == census_sha0 and determinism)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "exp217_deposit_byte_unchanged":
                    census_sha1 == census_sha0,
                "exp217_deposit_sha256": census_sha0,
                "export_deterministic": determinism,
                "artifact_file": os.path.relpath(ARTIFACT, ROOT),
                "artifact_sha256_file": E206.sha256_file(ARTIFACT),
                "artifact_bytes": len(blob.encode("utf-8")),
                "evidence_bank_series_byte_unchanged":
                    (w5d_sha1 == w5d_sha0
                     and series_sha1 == series_sha0)}

        # ---- evaluate each gate exactly once ---------------------------
        _gate("GATE-Z1", _z1)
        _gate("GATE-Z2", _z2)
        _gate("GATE-Z3", _z3)
        _gate("GATE-Z4", _z4)

        n_pass = sum(1 for v in gates.values()
                     if v["verdict"] == "PASS")
        n_ref = sum(1 for v in gates.values()
                    if v["verdict"] == "REFUTE")
        sp = artifact["counts"]
        verdict = (
            f"{n_pass}/{len(gates)} gates PASS | split "
            f"{sp['accepted']} accepted / {sp['not_in_literature']} "
            f"NOT-IN-LITERATURE / {sp['rejected']} rejected of "
            f"{artifact['meta']['n_entries']} | artifact "
            f"results/levin_voltage_series_wetlab_final.json deposited"
            if n_ref == 0 else
            f"REFUTE {n_ref} gate(s) "
            f"({', '.join(k for k, v in gates.items() if v['verdict'] == 'REFUTE')}) "
            f"| split {sp['accepted']}/{sp['not_in_literature']}"
            f"/{sp['rejected']}")

        extracts_carried = {
            row["id"]: {
                "pass1": len(row["extracts_by_pass"]["1"]),
                "pass2": len(row["extracts_by_pass"]["2"]),
                "pass3": len(row["extracts_by_pass"]["3"]),
                "total": sum(len(v) for v in
                             row["extracts_by_pass"].values())}
            for row in artifact["entries"]
            if "extracts_by_pass" in row}
        deposit_sections = {
            "exp217_split_deposited": dep_split,
            "export_split_realized": artifact["counts"],
            "id_partition": {"accepted": parts["acc"],
                             "not_in_literature": parts["nil"],
                             "rejected": parts["rej"]},
            "sources_files": parts["src_meta"],
            "extracts_carried": extracts_carried,
            "field_provenance_rows":
                len(artifact["meta"]["field_provenance"]),
            "new_field_provenance_fields": parts["new_fields"],
            "artifact": {
                "file": os.path.relpath(ARTIFACT, ROOT),
                "sha256": E206.sha256_file(ARTIFACT),
                "sha256_canonical_payload":
                    artifact["meta"][
                        "artifact_sha256_canonical_payload"],
                "bytes": len(E206.ser(artifact).encode("utf-8")),
                "entries": len(artifact["entries"]),
                "parses_standalone": True}}
        deposit = {
            "exp": "exp224_series_final_form",
            "claim": (
                "THE SERIES FINAL-FORM DEPOSIT (L193's registered "
                "next): the corpus leg's acceptance question is CLOSED "
                "(exp217: 111 NOT-IN-LITERATURE + 8 extract-carrying "
                "rejects); the Stage 2 deposit leg completes — the "
                "119-entry series (research/levin_voltage_series.json) "
                "re-exported AS the wetlab companion's final form: 111 "
                "NOT-IN-LITERATURE rows carrying their absence with the "
                "three-pass provenance inline, the 8 partial rows with "
                "their per-field extracts verbatim, census states + "
                "provenance inline, the whole artifact self-contained "
                "for wetlab use; the export is a projection, zero "
                "re-derivation (the structurally-blocked corpus leg "
                "converts to a deposit, the Section 5 registered item)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 94e15cb, batch 12; gates Z1-Z4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-Z1 (the projection) 119/119 entries exported; "
                    "per-entry census_state == exp217's deposited "
                    "verdict for that id; zero fields without "
                    "provenance (the NIL rows carry the three-file "
                    "provenance inline).",
                    "GATE-Z2 (the split integrity) the exported counts "
                    "== exp217's deposited split exactly (0 accepted / "
                    "111 NOT-IN-LITERATURE / 8 rejected); any drift "
                    "raises.",
                    "GATE-Z3 (the wetlab self-containment) the artifact "
                    "parses standalone; every entry carries its series "
                    "identity (id, source, pmid_or_doi, species, "
                    "region_or_tissue); the sha256 of the artifact + "
                    "of exp217's deposit recorded in the export's "
                    "meta.",
                    "GATE-Z4 (hygiene) exp217's deposit byte-unchanged "
                    "during the export; the export deterministic "
                    "(re-run bit-identical)."]},
            "instruments": {
                "census_deposit": os.path.relpath(CENSUS, ROOT),
                "census_deposit_sha256": census_sha0,
                "census_scope": (
                    "exp217's deposited census VERBATIM (sections."
                    "verdicts, sections.counts_split, sections."
                    "not_in_literature_spec) + the w5d bank's rows "
                    "(census states, census_missing lists, the NIL "
                    "provenance naming sources 1/2/3)"),
                "row_base": "research/levin_voltage_series.json#series",
                "row_base_sha256": series_sha0,
                "machinery": (
                    "experiments/exp206_w5_dose_pass.py VERBATIM "
                    "(read_sources, ser, sha256 helpers)"),
                "machinery_sha256": machinery_sha0,
                "sources_files": list(sources_rel),
                "sources_files_sha256": [sources_sha[r]
                                         for r in sources_rel],
                "state_display": DISPLAY},
            "sections": deposit_sections,
            "gates": gates,
            "artifact": os.path.relpath(ARTIFACT, ROOT),
            "census": os.path.relpath(CENSUS, ROOT),
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(deposit, f, indent=1, default=float)
        print(f"  === {verdict} ===")
        print(f"  deposited {out_path} | artifact {ARTIFACT}")
        return deposit

    # smoke: pipeline check only, discarded
    blob = E206.ser(artifact)
    json.loads(blob)
    sp = artifact["counts"]
    print(f"  SMOKE: {sp['accepted']} accepted / "
          f"{sp['not_in_literature']} NOT-IN-LITERATURE / "
          f"{sp['rejected']} rejected on the first "
          f"{len(artifact['entries'])} records; the artifact "
          f"serializes ({len(blob)} chars) and parses standalone "
          f"- DISCARDED (no artifact write, no deposit, no gates)")
    return {"exp": "exp224_series_final_form", "smoke": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
