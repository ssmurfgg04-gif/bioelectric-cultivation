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
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
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

    W5B_BANK = os.path.join(ROOT, "results",
                            "wetlab_companion_bank_w5b.json")
    W5_SOURCES = E206.SOURCES           # pass 1 (frozen)
    W5B_SOURCES = os.path.join(ROOT, "results",
                               "w5_pass_sources2.json")  # pass 2 (frozen)
    SMOKE_BANK = os.path.join(ROOT, "results",
                              "wetlab_companion_bank_w5c_smoke.json")
    bank_path = SMOKE_BANK if args.smoke else BANK
    n_take = 3 if args.smoke else E206.N_ENTRIES

    assert os.path.exists(W5B_BANK), \
        "the w5b bank (pass-2 baseline) missing"
    assert os.path.exists(sources_path), (
        "sources file 3 missing — run "
        "scripts/exp215_w5_sources_sweep3.mjs first (from "
        "/home/z/my-project/zai-proxy so the SDK resolves)")
    w5b_sha0 = E206.sha256_file(W5B_BANK)

    with open(W5_SOURCES, encoding="utf-8") as f:
        pass1 = json.load(f)
    with open(W5B_SOURCES, encoding="utf-8") as f:
        pass2 = json.load(f)
    src3 = E206.read_sources(sources_path)

    with open(E206.SERIES, encoding="utf-8") as f:
        series = json.load(f)["series"]
    with open(W5B_BANK, encoding="utf-8") as f:
        w5b = json.load(f)

    # ---- the merge: baseline row = the W5B BANK's row (pass-2's
    #      product, the frozen baseline for THIS pass); fills from
    #      sources 3 via E206's w5_fills (fill, never overwrite) ------
    w5b_rows: dict = {}
    for r in list(w5b.get("entries", [])) + list(w5b.get("rejects", [])):
        key = (r.get("provenance") or {}).get("source_key")
        if key is not None:
            w5b_rows[key] = r

    def merge() -> tuple:
        entries, rejects, verdicts = [], [], []
        for i, e in enumerate(series[:n_take]):
            base = w5b_rows.get(e["id"])
            assert base is not None, \
                f"the w5b bank has no row for {e['id']}"
            row = json.loads(json.dumps(base))   # pure copy
            prior_fields = {f for f in E206.FILL_FIELDS
                            if row.get(f) is not None}
            src_rec = src3["by_id"].get(e["id"])
            fills_prov = {}
            fig_swept = (src_rec is not None
                         and not src_rec.get("figure_identity_absent",
                                             False))
            if src_rec is not None:
                fills = E206.w5_fills(row, e, src_rec)
                for field, value in fills.items():
                    row[field] = value
                    fills_prov[field] = E206._fill_provenance(
                        field, value, src_rec)
                row["provenance"] = {
                    "source_deposit":
                        "results/w5_pass_sources3.json",
                    "source_record":
                        f"results/w5_pass_sources3.json#records.{e['id']}",
                    "source_key": e["id"],
                    "source_record_sha256":
                        E206.sha256_obj(src_rec),
                    "pass2_source_record_sha256":
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
                "figure_swept": fig_swept,
                "figure_identity_absent": bool(
                    src_rec is not None
                    and src_rec.get("figure_identity_absent", False)),
                "figure_query_pass": (src_rec or {}).get("query_pass")})
            (entries if accepted else rejects).append(row)
        counts = {"imported": len(series[:n_take]),
                  "accepted": len(entries),
                  "rejected": len(rejects)}
        bank3 = {
            "bank": "wetlab_companion",       # the validator's name rule
            "bank_file": "results/wetlab_companion_bank_w5c.json",
            "pass": 3,
            "baseline": {
                "bank": "results/wetlab_companion_bank_w5b.json",
                "sha256": w5b_sha0,
                "disclosure": ("the w5b bank is the frozen baseline for "
                               "THIS pass; its rows are the merge's "
                               "base")},
            "schema_version": w5b.get("schema_version"),
            "census_rule": w5b.get("census_rule"),
            "required_fields": w5b.get("required_fields"),
            "extended_fields": w5b.get("extended_fields"),
            "protocol": w5b.get("protocol"),
            "protocol_sha256": w5b.get("protocol_sha256"),
            "import_source": {
                "sources_file": os.path.relpath(sources_path, ROOT),
                "sources_records": src3["n_records"],
                "sources_mode": src3["mode"],
                "figure_pass_disclosure": (
                    "STRUCTURE-DRIVEN, not query-driven: the figure "
                    "queries pre-named per record ({source} "
                    "{db_figure_panel} {species} + {db_experiment_id} "
                    "{db_figure_panel}); 20 records without db identity "
                    "fields carry figure_identity_absent verdicts"),
                "pass_rules": {
                    "ordering": E206.FILL_RULES["ordering"],
                    "fill_never_overwrite":
                        E206.FILL_RULES["fill_never_overwrite"],
                    "base_rows": ("the W5B BANK's rows (pass-2's "
                                  "product), not the scaffold rows — "
                                  "the w5b bank is the frozen baseline "
                                  "for this pass; the acceptance "
                                  "predicate is UNCHANGED (the exp203 "
                                  "scaffold's required-field census)")}},
            "import_rules": {k: v for k, v in E206.FILL_RULES.items()
                             if k not in ("ordering",
                                          "fill_never_overwrite")},
            "field_provenance": list(w5b.get("field_provenance", [])),
            "entries": entries,
            "rejects": rejects,
            "counts": counts,
        }
        return bank3, verdicts

    bank3, verdicts = merge()

    # ---- the fill-rate deltas vs the w5b bank (GATE-F3) --------------
    def fill_rates(rows) -> dict:
        out = {}
        for f in E206.FILL_FIELDS:
            out[f] = sum(1 for r in rows if r.get(f) is not None)
        return out

    w5b_all_rows = list(w5b.get("entries", []))
    w5b_all_rows += list(w5b.get("rejects", []))
    rates_w5b = fill_rates(w5b_all_rows)
    rates_w5c = fill_rates(list(bank3["entries"]) + list(bank3["rejects"]))
    deltas = {f: {"w5b": rates_w5b[f], "w5c": rates_w5c[f],
                  "delta": rates_w5c[f] - rates_w5b[f]}
              for f in E206.FILL_FIELDS}

    # ---- the zero-extract census across ALL THREE passes (the
    #      REGISTERED branch's evidence base) ---------------------------
    def zero_extract_ids() -> list:
        ex1 = {r["id"]: len(r.get("extracts", []))
               for r in pass1["records"]}
        ex2 = {r["id"]: len(r.get("extracts", []))
               for r in pass2["records"]}
        ex3 = {r["id"]: len(r.get("extracts", []))
               for r in src3["doc"]["records"]}
        return sorted(e["id"] for e in series
                      if ex1.get(e["id"], 0) == 0
                      and ex2.get(e["id"], 0) == 0
                      and ex3.get(e["id"], 0) == 0)

    not_in_literature_spec = {
        "state": "NOT-IN-LITERATURE",
        "registered_repair": (
            "the exp203 census extended with an explicit "
            "absent-from-literature verdict: a record whose W5 fields "
            "are stated nowhere in the surfaced literature is "
            "DEPOSITED as NOT-IN-LITERATURE rather than rejected — "
            "the absence is the finding, carried with its own "
            "provenance discipline"),
        "provenance_discipline": (
            "a NOT-IN-LITERATURE verdict requires: the three passes' "
            "complete sweep evidence (119 records x the protocol, "
            "widened, and figure queries at the deposited sources "
            "files), zero verbatim extracts for the missing fields "
            "across all three passes, and the per-field absence "
            "asserted against the pass-1/2/3 sources records by "
            "sha256; the verdict's provenance names ALL THREE sources "
            "files"),
        "census_extension": (
            "census_missing(row) gains the not_in_literature clause: "
            "a row admitted to the new state carries "
            "'census_state': 'NOT-IN-LITERATURE' with the field list "
            "that is absent-from-literature; every other acceptance "
            "rule unchanged; the extension is implemented by the "
            "REGISTERED NEXT, not here"),
        "zero_extract_records_all_3_passes": zero_extract_ids(),
        "n_zero_extract_records": len(zero_extract_ids())}

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

        def _f1():
            # ---- GATE-F1 (the sweep): 119/119 covered ---------------
            ids3 = ([r.get("id") for r in src3["doc"]["records"]]
                    if src3["doc"] else [])
            want = [e["id"] for e in series]
            n_fig = sum(1 for v in verdicts if v["figure_swept"])
            n_abs = sum(1 for v in verdicts
                        if v["figure_identity_absent"])
            return {
                "verdict": "PASS"
                if (sorted(ids3) == sorted(want)
                    and n_fig + n_abs == len(want))
                else "REFUTE",
                "n_records_sources3": len(ids3),
                "n_series": len(want),
                "complete_not_sampled": sorted(ids3) == sorted(want),
                "n_figure_swept": n_fig,
                "n_figure_identity_absent": n_abs,
                "absent_disclosure": (
                    "the 20 model-quantity records carry no db "
                    "identity fields — the figure pass is vacuous "
                    "for them, disclosed per record")}

        def _f2():
            # ---- GATE-F2 (acceptance integrity; exp211's E2
            #      mechanism verbatim, baseline = the w5b rows) -------
            bad = []
            for r in bank3["entries"]:
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
                        # pass-2-derived: must equal the w5b row's value
                        base = w5b_rows[key]
                        if r[f] != base.get(f):
                            bad.append({"id": key, "field": f,
                                        "why": "baseline drift"})
                    else:
                        if not (prov.get("url") and prov.get("retrieved")
                                and prov.get("verbatim_quote")):
                            bad.append({"id": key, "field": f,
                                        "why": "incomplete provenance"})
            for r in bank3["rejects"]:
                assert r["census_missing"], \
                    r["provenance"]["source_key"]
                assert not E206.validate_row(
                    r, allow_census_missing=True)
            vb = (E206.validate_bank(bank3)
                  if hasattr(E206, "validate_bank") else [])
            return {
                "verdict": "PASS" if not bad and not vb else "REFUTE",
                "n_accepted": len(bank3["entries"]),
                "integrity_violations": bad,
                "bank_validator_errors": vb,
                "import_rules": bank3["import_rules"]}

        def _f3():
            # ---- GATE-F3 (the yield; the branch NAMED, each clause
            #      evaluated once) ------------------------------------
            acc = bank3["counts"]["accepted"]
            branch = "ACCEPTED" if acc >= 1 else "REGISTERED"
            return {
                "verdict": "PASS",
                "branch": branch,
                "accepted": acc,
                "baseline_accepted_exp211": 0,
                "fill_rate_deltas_vs_w5b": deltas,
                "not_in_literature_spec": (
                    not_in_literature_spec if branch == "REGISTERED"
                    else None),
                "branch_disclosure": (
                    "the pre-registered branch: ACCEPTED (>= 1) / the "
                    "validator extension REGISTERED (0 full censuses "
                    "across three passes -> the NOT-IN-LITERATURE "
                    "state's specification deposited as the registered "
                    "repair); the branch NAMED is the gate, the "
                    "specification is the deposit — the census itself "
                    "is extended by the REGISTERED NEXT")}

        def _f4():
            # ---- GATE-F4 (hygiene) ----------------------------------
            os.makedirs(os.path.dirname(bank_path), exist_ok=True)
            with open(bank_path, "w", encoding="utf-8") as f:
                f.write(E206.ser(bank3))
            bank3_rerun, _v2 = merge()
            determinism = (E206.ser(bank3_rerun) == E206.ser(bank3))
            w5b_sha1 = E206.sha256_file(W5B_BANK)
            return {
                "verdict": "PASS" if (determinism
                                      and w5b_sha1 == w5b_sha0
                                      and os.path.exists(sources_path))
                else "REFUTE",
                "w5b_bank_byte_unchanged": w5b_sha1 == w5b_sha0,
                "w5b_sha256": w5b_sha0,
                "new_bank_deterministic": determinism,
                "sources_file": os.path.relpath(sources_path, ROOT),
                "sources_file_sha256":
                    E206.sha256_file(sources_path)}

        # ---- evaluate each gate exactly once, asserts recorded as
        #      REFUTE with the failing line (exp206's gate discipline)
        _gate("GATE-F1", _f1)
        _gate("GATE-F2", _f2)
        _gate("GATE-F3", _f3)
        _gate("GATE-F4", _f4)

        n_pass = sum(1 for v in gates.values()
                     if v["verdict"] == "PASS")
        n_ref = sum(1 for v in gates.values()
                    if v["verdict"] == "REFUTE")
        acc = bank3["counts"]["accepted"]
        branch = gates["GATE-F3"].get("branch", "—")
        verdict = (
            f"{n_pass}/{len(gates)} gates PASS | branch {branch} | "
            f"accepted {acc}/{E206.N_ENTRIES} vs exp211's 0/119"
            if n_ref == 0 else
            f"REFUTE {n_ref} gate(s) "
            f"({', '.join(k for k, v in gates.items() if v['verdict'] == 'REFUTE')}) "
            f"| accepted {acc}/{E206.N_ENTRIES}")

        deposit = {
            "exp": "exp215_w5_figure_pass",
            "claim": ("THE W5 FIGURE-PASS (L184's registered next): "
                      "STRUCTURE-DRIVEN, not query-driven — the "
                      "figure queries pre-named per record ({source} "
                      "{db_figure_panel} {species} + "
                      "{db_experiment_id} {db_figure_panel}); if the "
                      "figure-pass also yields zero full censuses, "
                      "the honest alternative registers: a record "
                      "whose W5 fields are stated NOWHERE becomes an "
                      "explicit NOT-IN-LITERATURE deposit (the "
                      "registered validator extension)"),
            "pre_registered": {
                "gates_source": ("module docstring, committed before "
                                 "any run (pre-registration 08b1cfc, "
                                 "batch 10; gates F1-F4 fixed there, "
                                 "each evaluated exactly once)"),
                "gates": [
                    "GATE-F1 (the sweep) 119/119 covered by the "
                    "figure-pass; per-record verdicts deposited; "
                    "complete, not sampled",
                    "GATE-F2 (acceptance integrity) every accepted "
                    "entry validates; the L182/L184 import rules "
                    "verbatim; zero fields without provenance",
                    "GATE-F3 (the yield) the accepted count vs "
                    "exp211's 0/119; the per-field fill-rate deltas "
                    "vs the w5b bank; the branch: ACCEPTED (>= 1) / "
                    "the validator extension REGISTERED",
                    "GATE-F4 (hygiene) the w5b bank byte-unchanged; "
                    "the new bank deterministic; the sources file "
                    "deposited"]},
            "sections": {
                "verdicts": verdicts,
                "fill_rate_deltas": deltas,
                "not_in_literature_spec":
                    (not_in_literature_spec
                     if gates["GATE-F3"].get("branch") == "REGISTERED"
                     else None),
                "sources3_mode": src3.get("mode")},
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
    print(f"  SMOKE: merged {len(bank3['entries'])} accepted / "
          f"{len(bank3['rejects'])} rejected on the first {n_take} "
          f"records - DISCARDED (no deposit, no gates)")
    return {"exp": "exp215_w5_figure_pass", "smoke": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--sources", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
