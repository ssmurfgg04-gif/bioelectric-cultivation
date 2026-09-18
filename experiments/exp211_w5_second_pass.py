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
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged) ==============
    import hashlib
    import time

    import experiments.exp206_w5_dose_pass as E206  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--sources", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    sources_path = args.sources or SOURCES

    W5_BANK = os.path.join(ROOT, "results",
                           "wetlab_companion_bank_w5.json")
    W5_SOURCES = E206.SOURCES          # pass 1's sources (frozen here)
    SMOKE_BANK = os.path.join(ROOT, "results",
                              "wetlab_companion_bank_w5b_smoke.json")
    bank_path = SMOKE_BANK if args.smoke else BANK
    n_take = 3 if args.smoke else E206.N_ENTRIES

    assert os.path.exists(W5_BANK), "the w5 bank (pass-1 baseline) missing"
    assert os.path.exists(sources_path), (
        "sources file 2 missing — run "
        "scripts/exp211_w5_sources_sweep2.mjs first (from "
        "/home/z/my-project/zai-proxy so the SDK resolves)")
    w5_sha0 = E206.sha256_file(W5_BANK)

    with open(W5_SOURCES, encoding="utf-8") as f:
        pass1 = json.load(f)
    src2 = E206.read_sources(sources_path)
    failed1 = [r["id"] for r in pass1["records"]
               if r.get("search_error") or r.get("n_results") == 0]

    with open(E206.SERIES, encoding="utf-8") as f:
        series = json.load(f)["series"]
    with open(W5_BANK, encoding="utf-8") as f:
        w5 = json.load(f)

    # ---- the merge: baseline row = the W5 BANK's row (pass-1's
    #      product, the frozen baseline for THIS pass); fills from
    #      sources 2 via E206's w5_fills (fill, never overwrite — the
    #      pass-1 fills are in the w5 rows and are preserved) --------
    w5_rows: dict = {}
    for r in list(w5.get("entries", [])) + list(w5.get("rejects", [])):
        key = (r.get("provenance") or {}).get("source_key")
        if key is not None:
            w5_rows[key] = r

    def merge() -> tuple:
        entries, rejects, verdicts = [], [], []
        for i, e in enumerate(series[:n_take]):
            base = w5_rows.get(e["id"])
            assert base is not None, \
                f"the w5 bank has no row for {e['id']}"
            row = json.loads(json.dumps(base))   # pure copy
            prior_fields = {f for f in E206.FILL_FIELDS
                            if row.get(f) is not None}
            src_rec = src2["by_id"].get(e["id"])
            fills_prov = {}
            if src_rec is not None:
                fills = E206.w5_fills(row, e, src_rec)
                for field, value in fills.items():
                    row[field] = value
                    fills_prov[field] = E206._fill_provenance(
                        field, value, src_rec)
                row["provenance"] = {
                    "source_deposit":
                        "results/w5_pass_sources2.json",
                    "source_record":
                        f"results/w5_pass_sources2.json#records.{e['id']}",
                    "source_key": e["id"],
                    "source_record_sha256":
                        E206.sha256_obj(src_rec),
                    "pass1_source_record_sha256":
                        (row.get("provenance") or {}).get(
                            "source_record_sha256")}
            cm = E206.census_missing(row)
            struct_ok = not E206.validate_row(
                row, allow_census_missing=bool(cm))
            accepted = (not cm and struct_ok
                        and not E206.validate_row(row))
            reasons = E206._reasons(row, e, src_rec, cm)
            verdicts.append({
                "index": i, "id": e["id"], "accepted": accepted,
                "census_missing": cm,
                "literature_filled": fills_prov,
                "prior_filled_fields": sorted(prior_fields),
                "reasons": reasons,
                "swept_pass2": src_rec is not None
                and not src_rec.get("carried_from_pass1", False)})
            (entries if accepted else rejects).append(row)
        counts = {"imported": len(series[:n_take]),
                  "accepted": len(entries),
                  "rejected": len(rejects)}
        bank2 = {
            "bank": "wetlab_companion",       # the validator's name rule
            "bank_file": "results/wetlab_companion_bank_w5b.json",
            "pass": 2,
            "baseline": {"bank": "results/wetlab_companion_bank_w5.json",
                         "sha256": w5_sha0,
                         "disclosure": ("the w5 bank is the frozen "
                                        "baseline for THIS pass; its "
                                        "rows are the merge's base")},
            "schema_version": w5.get("schema_version"),
            "census_rule": w5.get("census_rule"),
            "required_fields": w5.get("required_fields"),
            "extended_fields": w5.get("extended_fields"),
            "protocol": w5.get("protocol"),
            "protocol_sha256": w5.get("protocol_sha256"),
            "import_source": {
                "sources_file": os.path.relpath(sources_path, ROOT),
                "sources_records": src2["n_records"],
                "sources_mode": src2["mode"],
                "pass1_failed_ids": failed1,
                "pass_rules": {
                    "ordering": E206.FILL_RULES["ordering"],
                    "fill_never_overwrite":
                        E206.FILL_RULES["fill_never_overwrite"],
                    "base_rows": ("the W5 BANK's rows (pass-1's "
                                  "product), not the scaffold rows — "
                                  "the w5 bank is the frozen baseline "
                                  "for this pass; the acceptance "
                                  "predicate is UNCHANGED (the exp203 "
                                  "scaffold's required-field census)")}},
            "import_rules": {k: v for k, v in E206.FILL_RULES.items()
                             if k not in ("ordering",
                                          "fill_never_overwrite")},
            "field_provenance": list(w5.get("field_provenance", [])),
            "entries": entries,
            "rejects": rejects,
            "counts": counts,
        }
        return bank2, verdicts

    bank2, verdicts = merge()

    # ---- the fill-rate deltas vs the w5 bank (GATE-E3) --------------
    def fill_rates(rows) -> dict:
        out = {}
        for f in E206.FILL_FIELDS:
            out[f] = sum(1 for r in rows if r.get(f) is not None)
        return out

    w5_all_rows = list(w5.get("entries", [])) + list(w5.get("rejects", []))
    rates_w5 = fill_rates(w5_all_rows)
    rates_w5b = fill_rates(list(bank2["entries"]) + list(bank2["rejects"]))
    deltas = {f: {"w5": rates_w5[f], "w5b": rates_w5b[f],
                  "delta": rates_w5b[f] - rates_w5[f]}
              for f in E206.FILL_FIELDS}

    gates = {}
    gate_errs = {}
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
                gate_errs[name] = tb[-1] if tb else "AssertionError"

        def _e1():
            # ---- GATE-E1 (the sweep): 119/119 covered; the 12
            #      re-swept ------------------------------------------
            ids2 = [r.get("id") for r in src2["records"]] \
                if isinstance(src2.get("records"), list) else \
                sorted(src2.get("by_id", {}).keys())
            want = [e["id"] for e in series]
            n_reswept = sum(1 for v in verdicts if v["swept_pass2"])
            return {
                "verdict": "PASS"
                if (sorted(ids2) == sorted(want)
                    and n_reswept >= len(failed1))
                else "REFUTE",
                "n_records_sources2": len(ids2),
                "n_series": len(want),
                "complete_not_sampled": sorted(ids2) == sorted(want),
                "pass1_failed_ids": failed1,
                "n_reswept_in_pass2": n_reswept}

        def _e2():
            # ---- GATE-E2 (acceptance integrity; exp206's gate_d2
            #      mechanism verbatim, the baseline line now the w5
            #      bank's rows — pass-1's provenance) ----------------
            bad = []
            for r in bank2["entries"]:
                key = r["provenance"]["source_key"]
                assert not E206.census_missing(r), key
                assert not E206.validate_row(r), \
                    (key, E206.validate_row(r))
                v = next(x for x in verdicts if x["id"] == key)
                for f in E206.FILL_FIELDS:
                    if r[f] is None:
                        continue
                    prov = v["literature_filled"].get(f)
                    if prov is None:
                        # pass-1-derived: must equal the w5 row's value
                        base = w5_rows[key]
                        if r[f] != base.get(f):
                            bad.append({"id": key, "field": f,
                                        "why": "baseline drift"})
                    else:
                        if not (prov.get("url") and prov.get("retrieved")
                                and prov.get("verbatim_quote")):
                            bad.append({"id": key, "field": f,
                                        "why": "incomplete provenance"})
            for r in bank2["rejects"]:
                assert r["census_missing"], \
                    r["provenance"]["source_key"]
                assert not E206.validate_row(
                    r, allow_census_missing=True)
            vb = (E206.validate_bank(bank2)
                  if hasattr(E206, "validate_bank") else [])
            return {
                "verdict": "PASS" if not bad and not vb else "REFUTE",
                "n_accepted": len(bank2["entries"]),
                "integrity_violations": bad,
                "bank_validator_errors": vb,
                "import_rules": bank2["import_rules"]}

        def _e3():
            # ---- GATE-E3 (the yield) ------------------------------
            acc = bank2["counts"]["accepted"]
            return {
                "verdict": "PASS" if acc >= 1 else "REFUTE",
                "accepted": acc,
                "baseline_accepted":
                    w5.get("counts", {}).get("accepted", 0),
                "goal_state": ">= 1 accepted entry",
                "goal_met": acc >= 1,
                "fill_rate_deltas_vs_w5": deltas}

        def _e4():
            # ---- GATE-E4 (hygiene) --------------------------------
            os.makedirs(os.path.dirname(bank_path), exist_ok=True)
            with open(bank_path, "w", encoding="utf-8") as f:
                f.write(E206.ser(bank2))
            bank2_rerun, _v2 = merge()
            determinism = (E206.ser(bank2_rerun) == E206.ser(bank2))
            w5_sha1 = E206.sha256_file(W5_BANK)
            return {
                "verdict": "PASS" if (determinism and w5_sha1 == w5_sha0
                                      and os.path.exists(sources_path))
                else "REFUTE",
                "w5_bank_byte_unchanged": w5_sha1 == w5_sha0,
                "w5_sha256": w5_sha0,
                "new_bank_deterministic": determinism,
                "sources_file": os.path.relpath(sources_path, ROOT),
                "sources_file_sha256":
                    E206.sha256_file(sources_path)}

        # ---- evaluate each gate exactly once, asserts recorded as
        #      REFUTE with the failing line (exp206's gate discipline)
        _gate("GATE-E1", _e1)
        _gate("GATE-E2", _e2)
        _gate("GATE-E3", _e3)
        _gate("GATE-E4", _e4)

        n_pass = sum(1 for v in gates.values()
                     if v["verdict"] == "PASS")
        n_ref = sum(1 for v in gates.values()
                    if v["verdict"] == "REFUTE")
        acc = bank2["counts"]["accepted"]
        verdict = (
            f"{n_pass}/{len(gates)} gates PASS | accepted {acc}/"
            f"{E206.N_ENTRIES} vs the w5 pass's 0/119"
            if n_ref == 0 else
            f"REFUTE {n_ref} gate(s) "
            f"({', '.join(k for k, v in gates.items() if v['verdict'] == 'REFUTE')}) "
            f"| accepted {acc}/{E206.N_ENTRIES}")

        deposit = {
            "exp": "exp211_w5_second_pass",
            "claim": ("THE W5 SECOND PASS (L182's registered next): "
                      "the 12 429'd/failed records re-swept at "
                      "pacing, then the pre-named widened queries "
                      "(drug + species + phenotype terms from the "
                      "record's own fields); the acceptance predicate "
                      "UNCHANGED (the exp203 scaffold's required-field "
                      "census); the w5 bank is the frozen baseline for "
                      "this pass"),
            "pre_registered": {
                "gates_source": ("module docstring, committed before "
                                 "any run (pre-registration de1155d, "
                                 "batch 9; gates E1-E4 fixed there, "
                                 "each evaluated exactly once)"),
                "gates": [
                    "GATE-E1 the sweep: 119/119 records covered (12 "
                    "re-sweeps + the widened queries); per-record "
                    "verdicts deposited; complete, not sampled",
                    "GATE-E2 acceptance integrity: every accepted "
                    "entry validates; the L182 import rules verbatim; "
                    "zero fields without provenance",
                    "GATE-E3 the yield: the accepted count vs 0/119; "
                    "per-field fill-rate deltas vs the w5 bank; the "
                    "goal state >= 1 accepted entry",
                    "GATE-E4 hygiene: the w5 bank byte-unchanged; the "
                    "new bank deterministic; the sources file "
                    "deposited"]},
            "sections": {
                "verdicts": verdicts,
                "fill_rate_deltas": deltas,
                "pass1_failed_ids": failed1,
                "sources2_mode": src2.get("mode")},
            "gates": gates,
            "bank": os.path.relpath(bank_path, ROOT),
            "sources": os.path.relpath(sources_path, ROOT),
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(deposit, f, indent=1, default=float)
        print(f"  === {verdict} ===")
        print(f"  deposited {out_path} | bank {bank_path}")
        return deposit

    # smoke: pipeline check only, discarded
    print(f"  SMOKE: merged {len(bank2['entries'])} accepted / "
          f"{len(bank2['rejects'])} rejected on the first {n_take} "
          f"records - DISCARDED (no deposit, no gates)")
    return {"exp": "exp211_w5_second_pass", "smoke": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--sources", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
