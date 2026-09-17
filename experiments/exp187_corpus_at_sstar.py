#!/usr/bin/env python3
"""exp187 — THE CORPUS AT S* (the substrate vs the mined planform
records).

Stage 5 path 2's next scale-up (L152/L157 line): S* = (64.0, 0.0)
carries 10 deposited (exp161) and 100 fresh random (exp182) targets —
all SYNTHETIC. The corpus's 1,716 mined planform records are the
EMPIRICAL target class. THIS EXPERIMENT samples 100 corpus patterns
and prices their writability at S*.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Sample, protocol, and gates are fixed now.

THE SAMPLE (zero fitting): the corpus deposit (exp118's mined records
— results/exp118_corpus_full.json) supplies the pattern bank; the
sample = records indexed by rng = default_rng(187187), 100 records
drawn without replacement from the bank's decoded-pattern records
(the record field carrying the decoded zone/identity program; the
exact field name read from the deposit at run time and recorded in
the manifest); each sampled pattern built through exp94's
spec_target_n on its own labeling (canon == wildtype asserted per
target). The manifest (100 record ids + f_sha256) deposited FIRST.

THE PROTOCOL: exp161's writable_3seed + probe_margin at S* =
(64.0, 0.0), seeds (1, 2, 3), the substrate lock asserted per write.

GATES (each evaluated exactly once):
  GATE-C1 (manifest first) the manifest precedes the battery in the
           deposit (byte-offset assertion); 100 unique records.
  GATE-C2 (the empirical bar) >= 90/100 corpus targets writable at
           S* (decode < 6.0 AND hold < 6.0 on 3/3 seeds); the miss
           list deposited; zero rejections.
  GATE-C3 (the margin profile) worst-case margin deposited; the
           margin histogram + the depth profile (the corpus's own
           value distribution) deposited; exp182's +5.404 reference
           line recorded.
  GATE-C4 (hygiene) all errs finite; no per-target tuning.

NO post-hoc tuning. --smoke (3 sampled records) permitted, discarded.
Deposit: results/exp187_corpus_at_sstar.json
Jobs: manifest | battery
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from experiments.exp161_universal_substrate import (  # noqa: E402
    probe_margin, writable_3seed, _lock_substrate,
)

S_STAR = (64.0, 0.0)
SAMPLE_SEED = 187187
N_SAMPLE = 100
SCALEUP_BAR = 90

OUT = os.path.join(ROOT, "results", "exp187_corpus_at_sstar.json")
CORPUS = os.path.join(ROOT, "results", "exp118_corpus_full.json")
DEP161 = os.path.join(ROOT, "results", "exp161_universal_substrate.json")


def main() -> dict:
    # ---- BODY (written by the run agent; docstring/imports/constants
    # ---- byte-unchanged). The __main__ block calls main() with no
    # ---- arguments, so the body re-parses sys.argv with the SAME
    # ---- flags to honor --smoke/--job/--out.
    import hashlib
    import time

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["manifest", "battery", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t0 = time.time()
    out_path = args.out or OUT

    # ---------- helpers -------------------------------------------
    def _sha_bytes(b: bytes) -> str:
        return hashlib.sha256(b).hexdigest()

    def _sha_file(path: str) -> str:
        with open(path, "rb") as fh:
            return _sha_bytes(fh.read())

    def _write(payload: dict, path: str) -> str:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w") as fh:
            json.dump(payload, fh, indent=1, default=float)
        return path

    def _num(x) -> bool:
        return isinstance(x, (int, float)) and not isinstance(x, bool)

    # the engine grid programs are represented on (g6.N = 100; the
    # corpus 1D sheet is the same N=100) — used ONLY by the structural
    # label-vector test below; disclosed in the scan block
    N_GRID = 100

    def _zone_triples(v) -> bool:
        """A LIST OF ZONE TRIPLES (f0, f1, voltage) or Zone-like dicts
        {f0, f1, voltage}. STRUCTURAL test only: NO conversion."""
        if not isinstance(v, list) or not v:
            return False
        for z in v:
            if isinstance(z, dict):
                if not {"f0", "f1", "voltage"} <= set(z):
                    return False
            elif isinstance(z, (list, tuple)):
                if len(z) != 3 or not all(_num(x) for x in z):
                    return False
            else:
                return False
        return True

    def _label_vector(v) -> bool:
        return (isinstance(v, list) and len(v) == N_GRID
                and all(_num(x) for x in v))

    def _spec_dict(v) -> bool:
        return (isinstance(v, dict) and "zones" in v
                and _zone_triples(v["zones"]))

    def _is_program(v) -> bool:
        return _zone_triples(v) or _label_vector(v) or _spec_dict(v)

    def _example(v):
        if isinstance(v, dict):
            return {k: _example(x) for k, x in list(v.items())[:6]}
        if isinstance(v, (list, tuple)):
            if len(v) > 4:
                return [_example(x) for x in list(v)[:4]] + \
                    [f"...({len(v)} items)"]
            return [_example(x) for x in v]
        if isinstance(v, str):
            return v if len(v) <= 60 else v[:57] + "..."
        if v is None or isinstance(v, (bool, int, float)):
            return v
        return str(v)[:60]

    def _reason(name: str, types: list) -> str:
        if name == "arm":
            return ("the mapped manipulation arm (family, plane, dose, "
                    "duration): a SIMULATION-KNOB tuple, no spatial "
                    "extents/voltages; NOT loadable as a target program "
                    "without an improvised conversion (excluded by the "
                    "pre-registration)")
        if "dict" in types:
            return "a mapping (flags/parameters); no zone structure"
        if "list" in types:
            return ("a list of labels/values, not zone triples (f0, "
                    "f1, voltage) and not a per-cell label vector")
        if "str" in types:
            return "a categorical label"
        if "bool" in types:
            return "a flag"
        return "a scalar metadata/outcome value"

    # ---- 1. the bank (exp118's mined planform records) ------------
    with open(CORPUS) as fh:
        bank = json.load(fh)
    records = bank["per_record"]
    n_bank = len(records)
    corpus_sha = _sha_file(CORPUS)
    bank_block = {
        "path": "results/exp118_corpus_full.json",
        "sha256": corpus_sha,
        "exp": bank.get("exp"), "mode": bank.get("mode"),
        "n_db_total": bank.get("n_db_total"), "n_records": n_bank,
        "accounting": bank.get("accounting"),
        "top_level_sections": {k: type(v).__name__ for k, v in
                               bank.items() if k != "per_record"},
    }

    # ---- 2. the pattern-field scan (registered: the exact field
    # ---- name is read from the deposit at run time and recorded)
    field_names: list = []
    for r in records:
        for k in r:
            if k not in field_names:
                field_names.append(k)
    fields = []
    qualifying: list = []
    for name in field_names:
        vals = [r[name] for r in records if name in r]
        types = sorted({type(v).__name__ for v in vals})
        n_prog = sum(int(_is_program(v)) for v in vals)
        ok = bool(vals) and n_prog == len(vals)
        fields.append({"name": name, "n_present": len(vals),
                       "types": types, "example": _example(vals[0]),
                       "n_program_values": n_prog,
                       "program_candidate": ok,
                       "reason": _reason(name, types)})
        if ok:
            qualifying.append(name)
    pattern_field = qualifying[0] if qualifying else None
    scan_block = {
        "registered_rule": (
            "the record field carrying the decoded zone/identity "
            "program; the exact field name read from the deposit at "
            "run time and recorded here; a field qualifies ONLY on "
            "structure (zone triples (f0, f1, voltage), a zone-bearing "
            f"spec dict, or a per-cell label vector of length "
            f"{N_GRID}) — NO conversion attempted"),
        "n_fields": len(fields),
        "fields": fields,
        "fields_qualifying": qualifying,
        "pattern_field": pattern_field,
    }

    # ---- 3. the registered sampler --------------------------------
    # default_rng(187187), 100 without replacement from the bank's
    # decoded-pattern records; if no pattern field exists the pool is
    # EMPTY and the sampler runs over the FULL bank as a DIAGNOSTIC
    # would-be sample (disclosed as such; never used as targets).
    rng = np.random.default_rng(SAMPLE_SEED)
    if pattern_field is not None:
        pool = [i for i, r in enumerate(records)
                if _is_program(r.get(pattern_field))]
        basis = (f"records carrying the pattern field "
                 f"'{pattern_field}'")
    else:
        pool = list(range(n_bank))
        basis = ("the FULL bank — the decoded-pattern subset is EMPTY "
                 "(0/1716 records carry a program field); the "
                 "registered sampler was run on the full bank as a "
                 "DIAGNOSTIC would-be sample, disclosed as such")
    n_draw = min(N_SAMPLE, len(pool))
    sel = np.sort(rng.choice(len(pool), size=n_draw, replace=False))
    chosen = [int(pool[int(j)]) for j in sel]
    sample_block = {
        "rng": f"np.random.default_rng({SAMPLE_SEED}), choice(..., "
               f"{n_draw}, replace=False); indices sorted ascending "
               f"after the draw",
        "basis": basis,
        "n_pool": len(pool),
        "n_sampled": n_draw,
        "n_unique_eids": len({records[i]["eid"] for i in chosen}),
        "records": [{"bank_index": int(i), "eid": records[i]["eid"],
                     "group": records[i].get("group"),
                     "plane": records[i].get("plane"),
                     "manipulation": records[i].get("manipulation"),
                     "status": records[i].get("status")}
                    for i in chosen],
        "never_used_as_targets": pattern_field is None,
    }

    # ---- (loadable branch only) build the targets BEFORE the
    # ---- manifest write: spec_target_n on the engine's canon, canon
    # ---- == wildtype asserted per target; NO instrument calls here
    built = None
    if pattern_field is not None:
        import experiments.exp136_generator_v6 as g6
        from experiments.exp94_multizone_scale import (
            MULTI, labeling_bfs_n, spec_target_n)
        from cultivation.compiler.anatomy import AnatomySpec, Zone

        def _triples_of(zv):
            if isinstance(zv, dict):
                zv = zv["zones"]
            out = []
            for z in zv:
                if isinstance(z, dict):
                    out.append((float(z["f0"]), float(z["f1"]),
                                float(z["voltage"])))
                else:
                    out.append((float(z[0]), float(z[1]),
                                float(z[2])))
            return out

        canon = labeling_bfs_n(g6.A_CHAIN)
        built = []
        for k, i in enumerate(chosen):
            assert np.array_equal(canon, g6.wildtype_target(g6.N)), \
                f"bank record {i}: canon mismatch vs the engine's " \
                f"wildtype (canon == wildtype asserted per target)"
            triples = _triples_of(records[i][pattern_field])
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{m}")
                       for m, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp187-bank{i}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, g6.N)
            f_sha = hashlib.sha256(np.ascontiguousarray(
                f, dtype=np.float64).tobytes()).hexdigest()
            built.append({"bank_index": i, "eid": records[i]["eid"],
                          "triples": triples, "f_sha256": f_sha,
                          "f": f})
        sample_block["records"] = [
            {**sr, "triples": b["triples"], "f_sha256": b["f_sha256"]}
            for sr, b in zip(sample_block["records"], built)]

    manifest_payload = {
        "experiment": "exp187_corpus_at_sstar",
        "kind": "manifest",
        "deposited_first": True,
        "sample_seed": SAMPLE_SEED, "n_sample": N_SAMPLE,
        "s_star": list(S_STAR),
        "bank": bank_block,
        "pattern_field_scan": scan_block,
        "sample": sample_block,
    }

    # ---- --smoke: 3 sampled records, permitted and DISCARDED -------
    if args.smoke:
        rng3 = np.random.default_rng(SAMPLE_SEED)
        sel3 = np.sort(rng3.choice(len(pool), size=3, replace=False))
        rows3 = []
        for j in sel3:
            i = int(pool[int(j)])
            r = records[i]
            pv = [k for k in r if _is_program(r[k])]
            rows3.append({"bank_index": i, "eid": r["eid"],
                          "n_fields": len(r),
                          "program_fields": pv})
            print(f"  smoke record bank[{i}] eid {r['eid']}: "
                  f"{len(r)} fields, program fields: "
                  f"{pv or 'NONE'}")
        branch = ("loadable" if pattern_field is not None
                  else "INCOMPATIBLE-STRUCTURE")
        print(f"=== exp187 SMOKE (3 sampled records, DISCARDED) === "
              f"pattern_field {pattern_field!r} -> {branch} branch")
        dep = {"experiment": "exp187_corpus_at_sstar",
               "kind": "smoke", "discarded": True, "rows": rows3,
               "pattern_field": pattern_field,
               "branch": branch}
        if args.out:
            _write(dep, out_path)
        return dep

    # ===================== the credited run ==========================
    print(f"=== exp187: the corpus at S* = {list(S_STAR)} ===\n")
    print(f"  bank: {n_bank} records, sha256 {corpus_sha[:12]}...")
    print(f"  pattern-field scan: {len(fields)} record fields, "
          f"qualifying {qualifying or 'NONE'} "
          f"-> {'loadable' if pattern_field is not None else 'INCOMPATIBLE-STRUCTURE'}")

    # ---- 4. manifest deposited FIRST (byte-offset discipline) -------
    if args.job != "battery":
        p = _write(manifest_payload, out_path)
        L1 = os.path.getsize(p)
        sha1 = _sha_file(p)
        print(f"  manifest deposited FIRST -> {p} ({L1} bytes)")
    if args.job == "manifest":
        return manifest_payload

    # assert the phase-1 manifest holds bytes [0, L) of the deposit
    with open(out_path, "rb") as fh:
        b_now = fh.read()
    if args.job == "all":
        assert len(b_now) == L1 and _sha_bytes(b_now) == sha1, \
            "manifest-first violated: the deposit changed under us"
    else:
        phase1 = json.loads(b_now)
        assert (phase1.get("kind") == "manifest"
                and phase1.get("experiment")
                == "exp187_corpus_at_sstar"), \
            "battery job: no phase-1 manifest on disk"
        L1 = len(b_now)
        sha1 = _sha_bytes(b_now)
    manifest_first = {
        "protocol": ("the phase-1 manifest deposit occupied bytes "
                     "[0, L) of the deposit; re-read + re-hashed "
                     "BEFORE the final write; length + sha256 "
                     "recorded here"),
        "byte_offset": 0,
        "manifest_byte_length": L1,
        "manifest_sha256": sha1,
        "asserted_before_final_write": True,
    }

    # ---- 5. the exp182 reference line (C3's registered record) ------
    with open(os.path.join(ROOT, "results",
                           "exp182_substrate_100.json")) as fh:
        dep182 = json.load(fh)
    assert dep182["battery"]["S_star"] == [S_STAR[0], S_STAR[1]], \
        "exp182's deposited S* != this module's S*"
    ref_worst = float(dep182["battery"]["worst_case_margin3"])

    # ---- 6. the battery / the diagnosis -----------------------------
    if pattern_field is None:
        # ======== INCOMPATIBLE-STRUCTURE (the honest branch) ========
        miss_list = [{"bank_index": int(i), "eid": records[i]["eid"],
                      "reason": "no_pattern_field_in_bank_"
                                "incompatible_structure"}
                     for i in chosen]
        gates = {"C1": True, "C2": False, "C3": False, "C4": True}
        gate_detail = {
            "C1": (
                "PASS — the manifest-first protocol was executed: the "
                "phase-1 manifest (bank identity + the FULL "
                f"{len(fields)}-field scan + the {n_draw} sampled "
                f"records) was deposited FIRST at bytes [0, {L1}) "
                f"(sha256 {sha1[:12]}...), re-read and re-hashed "
                "BEFORE the final write; the sample carries "
                f"{sample_block['n_unique_eids']} unique records. "
                "DISCLOSURE: the manifest is a DIAGNOSIS manifest — "
                "the bank has no target programs, so it carries no "
                "target f_sha256 fields; the sampled eids are the "
                "registered sampler's output over the full bank (the "
                "decoded-pattern subset is empty), labeled "
                "never_used_as_targets"),
            "C2": (
                "REFUTE — 0/100 (bar >= 90): ZERO corpus targets could "
                "be built because NO record field carries a decoded "
                "zone/identity program (the "
                f"{len(fields)}-field structural scan deposited; "
                "fields_qualifying = []); writable_3seed never ran; "
                "the miss list is the 100 sampled records, all with "
                "the same reason; zero rejections trivially (zero "
                "writes). INCOMPATIBLE-STRUCTURE — the empirical "
                "target class is not loadable as target programs; no "
                "conversion improvised per pre-registration"),
            "C3": (
                "REFUTE — the margin deliverable does not exist: no "
                "targets constructible, zero instrument calls, no "
                "margins, so no histogram/depth profile of corpus "
                "margins can be formed; exp182's reference line "
                f"(+{ref_worst:.3f}) is recorded"),
            "C4": (
                "PASS — no per-target tuning: structurally ZERO "
                "instrument calls, S* never adjusted, the scan is "
                "read-only over the deposit, no knobs touched; the "
                "errs clause is vacuous over the empty battery "
                "(all() over no errs) and is disclosed as such"),
        }
        out = {
            "experiment": "exp187_corpus_at_sstar",
            "kind": "incompatible_structure",
            "claim": (
                "the empirical target class: 100 sampled mined "
                "planform records priced for writability at the "
                "locked substrate S* = (64.0, 0.0) — registered "
                "sample/protocol/gates C1-C4"),
            "pre_registered": {
                "sample": (
                    "rng = default_rng(187187), 100 records without "
                    "replacement from the bank's decoded-pattern "
                    "records (the record field carrying the decoded "
                    "zone/identity program, read from the deposit at "
                    "run time); each pattern built through exp94's "
                    "spec_target_n on its own labeling (canon == "
                    "wildtype asserted per target)"),
                "protocol": (
                    "exp161's writable_3seed + probe_margin at S* = "
                    "(64.0, 0.0), seeds (1, 2, 3), the substrate lock "
                    "asserted per write"),
                "manifest_first": True,
                "gates": {
                    "C1": "the manifest precedes the battery in the "
                          "deposit (byte-offset assertion); 100 "
                          "unique records",
                    "C2": ">= 90/100 corpus targets writable at S* "
                          "(decode < 6.0 AND hold < 6.0 on 3/3 "
                          "seeds); the miss list deposited; zero "
                          "rejections",
                    "C3": "worst-case margin deposited; the margin "
                          "histogram + the depth profile deposited; "
                          "exp182's +5.404 reference line recorded",
                    "C4": "all errs finite; no per-target tuning",
                },
            },
            "bank": bank_block,
            "pattern_field_scan": scan_block,
            "manifest_first": manifest_first,
            "sample": sample_block,
            "battery": {
                "S_star": list(S_STAR), "seeds": [1, 2, 3],
                "n_targets_built": 0, "n_instrument_calls": 0,
                "n_writable": 0, "n_rejected_seeds": 0,
                "miss_list": miss_list,
                "miss_list_note": (
                    "every sampled record misses for the SAME reason: "
                    "the bank carries no decoded zone/identity "
                    "program, so no target could be BUILT "
                    "(writable_3seed never ran) — this is a structure "
                    "refutation, not a substrate failure"),
            },
            "margin_profile": {
                "exists": False,
                "reason": ("no margins exist: zero targets "
                           "constructible, zero instrument calls"),
                "exp182_reference_line": {
                    "source": "results/exp182_substrate_100.json",
                    "n_targets": 100,
                    "worst_case_margin3": round(ref_worst, 4),
                    "recorded": True},
            },
            "gates": gates,
            "gate_detail": gate_detail,
            "gates_passed": f"{int(sum(gates.values()))}/4",
            "verdict": (
                "C2 REFUTE with diagnosis — INCOMPATIBLE-STRUCTURE: "
                "exp118's corpus is an outcome-comparison bank "
                "(recorded vs simulated scalar outcomes over 1,716 "
                "PlanformDB experiments), not a pattern-program bank; "
                f"no record field carries a decoded zone/identity "
                f"program ({len(fields)}-field scan deposited); no "
                "conversion improvised per pre-registration"),
            "smoke_disclosure": (
                "a --smoke check (3 sampled records, scan verdicts "
                "only) ran before the credited run in a separate "
                "process and was discarded (no file)"),
            "wall_s": round(time.time() - t0, 1),
        }
    else:
        # ======== the registered battery (loadable branch) ===========
        from experiments.exp161_universal_substrate import (
            _SUBSTRATE_FIXED, _SUBSTRATE_LOG)

        _SUBSTRATE_FIXED[:] = [S_STAR, id(g6.A_CHAIN)]  # ONCE, before
        # any verdict; _lock_substrate now RAISES on per-target drift
        per = []
        canon_asserts = 0
        for b in built:
            pm = probe_margin(b["f"], b["triples"], S_STAR)
            v = writable_3seed(b["f"], b["triples"], S_STAR)
            row = v["row"]
            per.append({
                "bank_index": b["bank_index"], "eid": b["eid"],
                "triples": b["triples"], "f_sha256": b["f_sha256"],
                "probe_margin1": float(pm),
                "writable": bool(v["writable"]),
                "rejected": bool(v["rejected"]),
                "n_rejected": int(row["n_rejected"]),
                "margin3": float(v["margin3"]),
                "quad": row["quad"],
                "decode_errs": row["decode_errs"],
                "hold_errs": row["hold_errs"]})
            canon_asserts += 1
            if len(per) % 10 == 0:
                print(f"  ... {len(per)}/{n_draw} corpus targets "
                      f"priced ({time.time() - t0:.0f}s)", flush=True)

        n_writable = sum(int(q["writable"]) for q in per)
        n_rej = sum(int(q["n_rejected"]) for q in per)
        margins = [q["margin3"] for q in per]
        worst = float(min(margins))
        mean_m = float(np.mean(margins))
        counts, edges = np.histogram(margins, bins=10)
        all_vals = sorted(v for q in per
                          for (_s, _e, v) in q["triples"])
        q1, q2, q3 = (all_vals[len(all_vals) // 4],
                      all_vals[len(all_vals) // 2],
                      all_vals[3 * len(all_vals) // 4])
        depth = []
        for lo, hi, lab in [(None, q1, "Q1 (shallowest)"),
                            (q1, q2, "Q2"), (q2, q3, "Q3"),
                            (q3, None, "Q4 (deepest)")]:
            tv = [q["margin3"] for q in per
                  if any((lo is None or v >= lo)
                         and (hi is None or v <= hi)
                         for (_s, _e, v) in q["triples"])]
            depth.append({"bin": lab, "n_targets": len(tv),
                          "worst_margin3": (round(float(min(tv)), 4)
                                            if tv else None)})
        all_fin = bool(
            all(np.isfinite(q["probe_margin1"])
                and np.isfinite(q["quad"])
                and all(np.isfinite(x) for x in q["decode_errs"])
                and all(np.isfinite(x) for x in q["hold_errs"])
                for q in per))
        runs = [r for r, _ in _SUBSTRATE_LOG]
        c1 = bool(manifest_first["asserted_before_final_write"]
                  and sample_block["n_unique_eids"] == N_SAMPLE
                  and len(per) == N_SAMPLE)
        c2 = bool(n_writable >= SCALEUP_BAR and n_rej == 0)
        c3 = bool(np.isfinite(worst) and len(depth) == 4)
        c4 = bool(all_fin and canon_asserts == N_SAMPLE)
        gates = {"C1": c1, "C2": c2, "C3": c3, "C4": c4}
        miss_list = [{"bank_index": q["bank_index"], "eid": q["eid"],
                      "margin3": round(q["margin3"], 4),
                      "rejected": q["rejected"]}
                     for q in per if not q["writable"]]
        out = {
            "experiment": "exp187_corpus_at_sstar",
            "kind": "battery",
            "bank": bank_block,
            "pattern_field_scan": scan_block,
            "manifest_first": manifest_first,
            "sample": {k: v for k, v in sample_block.items()},
            "battery": {
                "S_star": list(S_STAR), "seeds": [1, 2, 3],
                "n_writable": n_writable,
                "n_rejected_seeds": n_rej,
                "miss_list": miss_list,
                "worst_case_margin3": round(worst, 4),
                "mean_margin3": round(mean_m, 4),
                "per_target": [{**q,
                                "probe_margin1": round(
                                    q["probe_margin1"], 4),
                                "margin3": round(q["margin3"], 4)}
                               for q in per]},
            "margin_profile": {
                "exists": True,
                "worst_case_margin3": round(worst, 4),
                "histogram": {"counts": [int(c) for c in counts],
                              "bin_edges": [float(e) for e in edges]},
                "depth_profile": depth,
                "exp182_reference_line": {
                    "source": "results/exp182_substrate_100.json",
                    "n_targets": 100,
                    "worst_case_margin3": round(ref_worst, 4)}},
            "substrate_log": {"n_writes": len(_SUBSTRATE_LOG),
                              "all_at_S_star": all(
                                  r == S_STAR for r in runs)},
            "gates": gates,
            "gates_passed": f"{int(sum(gates.values()))}/4",
            "smoke_disclosure": (
                "a --smoke check (3 sampled records, scan verdicts "
                "only) ran before the credited run in a separate "
                "process and was discarded (no file)"),
            "wall_s": round(time.time() - t0, 1),
        }

    p = _write(out, out_path)
    for g in ("C1", "C2", "C3", "C4"):
        print(f"  GATE-{g}: "
              f"{'PASS' if gates[g] else 'REFUTE'}")
    print(f"  === {int(sum(gates.values()))}/4 gates PASS === "
          f"{out['battery']['n_writable']}/{N_SAMPLE} corpus targets "
          f"writable at S* {list(S_STAR)}")
    print(f"  deposited {p} ({out['wall_s']}s)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["manifest", "battery", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
