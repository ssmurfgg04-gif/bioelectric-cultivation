#!/usr/bin/env python3
"""exp231 — THE CHINESE-TARGETS GATES DEPOSIT (L201's registered
next; the Section 5 item).

The last open deposit leg: the Chinese literature targets — the
scaffold exists (experiments/scaffold_chinese_targets.py, gates
drafted) and the deposit converts it to the wetlab companion's final
form: the drafted gates exported as a self-contained, provenance-
carrying deposit the wetlab side can execute without the stack.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: experiments/
scaffold_chinese_targets.py's deposited machinery VERBATIM (its gate
definitions, its target fields); exp224's final-form discipline
VERBATIM (the projection gates: per-entry identity, split integrity,
self-containment, determinism); the artifact written =
results/chinese_targets_gates_deposit.json.

GATES (each evaluated exactly once):
  GATE-C1 (the projection) every drafted target exported with its
           gate fields verbatim from the scaffold's definitions;
           zero fields without provenance (the scaffold's own
           source references inline).
  GATE-C2 (the split integrity) the exported counts == the
           scaffold's deposited counts exactly; any drift raises.
  GATE-C3 (the self-containment) the artifact parses standalone;
           every entry carries its identity fields; the sha256 of
           the artifact + of the scaffold's own deposit (if any)
           recorded in the export's meta.
  GATE-C4 (hygiene) the scaffold's files byte-unchanged during the
           export; the export deterministic (re-run bit-identical).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp231_chinese_targets_deposit.json
ARTIFACT: results/chinese_targets_gates_deposit.json
RUN: python3 -m experiments.exp231_chinese_targets_deposit [--smoke] [--job ...] [--out ...]
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
                   "exp231_chinese_targets_deposit.json")
ARTIFACT = os.path.join(ROOT, "results",
                        "chinese_targets_gates_deposit.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import hashlib
    import inspect
    import re
    import time

    # exp224's final-form discipline VERBATIM: the same ser/sha256_file
    # helpers (exp203's, via exp206's re-export), the same gate wrapper,
    # the same deposit shape.
    import experiments.exp206_w5_dose_pass as E206  # noqa: E402
    import experiments.scaffold_chinese_targets as SCAF  # noqa: E402

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

    SCAF_PATH = os.path.join(ROOT, "experiments",
                             "scaffold_chinese_targets.py")
    GATES_DOC = os.path.join(ROOT, "research",
                             "chinese_targets_gates.md")
    EXP129 = os.path.join(ROOT, "results",
                          "exp129_chinese_targets.json")
    EXP118_FULL = SCAF.EXP118_FULL   # the scaffold's own reference path
    for _p in (SCAF_PATH, GATES_DOC, EXP129, EXP118_FULL):
        assert os.path.exists(_p), f"instrument file missing: {_p}"

    # hygiene hashes BEFORE any export work (GATE-C4 re-checks after)
    sha0 = {p: E206.sha256_file(p)
            for p in (SCAF_PATH, GATES_DOC, EXP129, EXP118_FULL)}
    with open(SCAF_PATH, encoding="utf-8") as f:
        scaf_lines = f.read().splitlines()

    # ---- the instruments: the scaffold's machinery VERBATIM ------------
    # imported live; the gate definitions, target fields, grids, pins
    # are read from the module object — never re-typed, never re-derived.
    scaf_doc = SCAF.__doc__
    gate_fns = dict(SCAF.GATES)
    constants = {
        "D_PAR": SCAF.D_PAR,
        "GEN_BIAS": SCAF.GEN_BIAS,
        "SEEDS": list(SCAF.SEEDS),
        "DOSE_GRID_COARSE": list(SCAF.DOSE_GRID_COARSE),
        "FINE_DOSES": list(SCAF.FINE_DOSES),
        "FINE_SEEDS": list(SCAF.FINE_SEEDS),
        "ONSETS": list(SCAF.ONSETS),
        "TIMING_GAMMA": SCAF.TIMING_GAMMA,
        "TIMING_SEEDS": list(SCAF.TIMING_SEEDS),
        "T1_COARSENING": dict(SCAF.T1_COARSENING),
    }
    pin_names = ("PIN_T1_METFORMIN", "PIN_T2_USP7", "PIN_T3_OPA1")
    pins = {n: getattr(SCAF, n) for n in pin_names}
    TID_PIN = {"T1": "PIN_T1_METFORMIN", "T2": "PIN_T2_USP7",
               "T3": "PIN_T3_OPA1"}

    def line_of(pat: str) -> int:
        for i, l in enumerate(scaf_lines, 1):
            if re.match(pat, l):
                return i
        raise AssertionError(f"scaffold line not found: {pat}")

    def pin_todo(name: str) -> str:
        i = line_of(rf"^{name}\s*=") - 1
        got = [scaf_lines[i]]
        for l in scaf_lines[i + 1:]:
            if re.match(r"^\s+#", l):
                got.append(l)
            else:
                break
        return "\n".join(got)

    # the scaffold's target fields: the three paragraphs of its module
    # docstring's THE THREE TARGETS block, verbatim
    doc_lines = scaf_doc.splitlines()
    tgt_starts = {}
    for i, l in enumerate(doc_lines):
        m = re.match(r"^  (T[123])  ", l)
        if m:
            tgt_starts[m.group(1)] = i
    assert sorted(tgt_starts) == ["T1", "T2", "T3"], \
        f"the scaffold's THE THREE TARGETS block drifted: {tgt_starts}"
    target_para = {}
    for tid, i in tgt_starts.items():
        j = i + 1
        while j < len(doc_lines) and doc_lines[j].startswith("      "):
            j += 1
        target_para[tid] = "\n".join(doc_lines[i:j]).rstrip()

    def section_refs(doc: str) -> list:
        return re.findall(r"Gates\s+(§[A-Za-z0-9]+)", doc)

    with open(GATES_DOC, encoding="utf-8") as f:
        doc_text = f.read()
    doc_headings = [l for l in doc_text.splitlines() if l.startswith("#")]

    def section_live(ref: str) -> bool:
        label = ref.lstrip("§")
        return any(label in h for h in doc_headings)

    def import_block() -> list:
        got, i = [], 0
        while i < len(scaf_lines):
            l = scaf_lines[i]
            if re.match(r"^from experiments\.", l):
                chunk = [l]
                if l.rstrip().endswith("("):
                    for l2 in scaf_lines[i + 1:]:
                        chunk.append(l2)
                        if ")" in l2:
                            break
                got.append("\n".join(chunk))
                i += len(chunk)
            else:
                i += 1
        return got

    def scaf_counts() -> dict:
        """The scaffold's deposited counts, computed live from the
        imported module each call (GATE-C2's comparison base)."""
        n_anchor = sum(1 for g in gate_fns if g.startswith("A_"))
        return {
            "targets": len(pin_names),
            "gates": len(gate_fns),
            "anchor_gates": n_anchor,
            "target_gates": len(gate_fns) - n_anchor,
            "dose_grid_coarse": len(SCAF.DOSE_GRID_COARSE),
            "fine_doses": len(SCAF.FINE_DOSES),
            "fine_seeds": len(SCAF.FINE_SEEDS),
            "onsets": len(SCAF.ONSETS),
            "timing_seeds": len(SCAF.TIMING_SEEDS),
            "mapping_seeds": len(SCAF.SEEDS),
            "coarsening_bands": len(SCAF.T1_COARSENING),
            "to_pin_constants": len(pin_names),
        }

    with open(EXP129, encoding="utf-8") as f:
        e129 = json.load(f)
    assert e129.get("exp") == "exp129_chinese_targets", \
        "the finalized-run deposit is not exp129's"

    SCAF_REL = os.path.relpath(SCAF_PATH, ROOT)
    GDOC_REL = os.path.relpath(GATES_DOC, ROOT)
    E129_REL = os.path.relpath(EXP129, ROOT)
    E118_REL = os.path.relpath(EXP118_FULL, ROOT)

    # the pre-registered quotes (the docstring's own clauses, verbatim)
    _FINAL_FORM_QUOTE = ("the drafted gates exported as a "
                         "self-contained, provenance-carrying deposit "
                         "the wetlab side can execute without the stack")
    _C1_QUOTE = ("GATE-C1 (the projection) every drafted target exported "
                 "with its gate fields verbatim from the scaffold's "
                 "definitions; zero fields without provenance (the "
                 "scaffold's own source references inline).")
    _C2_QUOTE = ("GATE-C2 (the split integrity) the exported counts == "
                 "the scaffold's deposited counts exactly; any drift "
                 "raises.")
    _C3_QUOTE = ("GATE-C3 (the self-containment) the artifact parses "
                 "standalone; every entry carries its identity fields; "
                 "the sha256 of the artifact + of the scaffold's own "
                 "deposit (if any) recorded in the export's meta.")
    _C4_QUOTE = ("GATE-C4 (hygiene) the scaffold's files byte-unchanged "
                 "during the export; the export deterministic (re-run "
                 "bit-identical).")
    _E129_QUOTE = ("the finalized-run block is copied VERBATIM from "
                   "exp129's deposit (the scaffold's gates' deposited "
                   "run): the pinned-record state, the pin provenance, "
                   "the provenance corrections and the gate outcomes")
    PR_REF = "exp231 docstring (pre-registered, batch 14)"
    E129_REF = (f"{E129_REL} (copied verbatim; sha256 in "
                f"meta.finalized_run_deposit_sha256)")
    HYG_REF = ("computed at export (E206.sha256_file, exp224's "
               "discipline verbatim)")
    IDX_REF = "computed at export (source line index into the scaffold)"

    # ==== the projection ===============================================
    def build_export(n_take=None) -> tuple:
        """The export is a projection, ZERO re-derivation: every gate
        definition, target field, pre-registered grid, coarsening map
        and TO-PIN constant is copied from the imported scaffold
        VERBATIM; the finalized-run block from exp129's deposit
        VERBATIM; nothing is re-adjudicated, re-pinned or re-derived."""
        take_ids = (["T1", "T2", "T3"][:n_take] if n_take
                    else ["T1", "T2", "T3"])
        targets = []
        for tid in take_ids:
            targets.append({
                "target_id": tid,
                "docstring_verbatim": target_para[tid],
                "pin_constant": TID_PIN[tid],
                "pin_value_scaffold": pins[TID_PIN[tid]],
                "pin_todo_verbatim": pin_todo(TID_PIN[tid]),
                "pin_def_line": line_of(rf"^{TID_PIN[tid]}\s*="),
                "para_def_line": line_of(rf"^  {tid}  "),
                "gates": [g for g in gate_fns
                          if g.startswith(tid + "_")],
            })
        take_gates = (list(gate_fns)[:n_take] if n_take
                      else list(gate_fns))
        gates_entries = []
        for gid in take_gates:
            fn = gate_fns[gid]
            refs = section_refs(fn.__doc__)
            kind = "anchor" if gid.startswith("A_") else "target"
            tid = None if kind == "anchor" else gid.split("_")[0]
            gates_entries.append({
                "gate_id": gid,
                "order": list(gate_fns).index(gid),
                "kind": kind,
                "target_id": tid,
                "docstring_verbatim": fn.__doc__,
                "gates_doc_section": refs[0] if refs else None,
                "gates_doc_sections_all": refs,
                "scaffold_stub": ("NotImplementedError"
                                  in inspect.getsource(fn)),
                "def_line": fn.__code__.co_firstlineno,
                "finalized_run_outcome": e129["gate_outcomes"][gid],
            })

        scaffold_block = {
            "file": SCAF_REL,
            "sha256": sha0[SCAF_PATH],
            "module_docstring_verbatim": scaf_doc,
            "status_line": scaf_lines[line_of(r"^STATUS:") - 1],
            "machinery_imports": import_block(),
            "exp_num": SCAF.EXP_NUM,
            "own_deposit": {
                "path": os.path.relpath(SCAF.OUT, ROOT),
                "present": os.path.exists(SCAF.OUT),
                "note": ("the scaffold never ran (SCAFFOLD, EXP_NUM "
                         "None): no deposit exists at its OUT path — "
                         "the 'if any' clause of GATE-C3; the drafted "
                         "gates' finalized+run deposit is carried in "
                         "the finalized_run block")},
            "constants": constants,
            "pins": pins,
            "pin_todo_verbatim": {n: pin_todo(n) for n in pin_names},
            "pin_def_line": {n: line_of(rf"^{n}\s*=")
                             for n in pin_names},
        }
        registration_block = {
            "file": GDOC_REL,
            "sha256": sha0[GATES_DOC],
            "note": ("the gates document is the registration; the "
                     "scaffold is its carriage — the scaffold's own "
                     "docstring line below says exactly this"),
            "sections_live": {ref: section_live(ref) for ref in
                              sorted({r for row in gates_entries
                                      for r in
                                      row["gates_doc_sections_all"]})},
        }
        finalized_run = {
            "note": ("the scaffold's gates were assigned exp number 129 "
                     "and finalized+run by Task 5-f "
                     "(experiments/exp129_chinese_targets.py); this "
                     "block is the deposited run of the drafted gates, "
                     "carried VERBATIM so the wetlab side sees both the "
                     "drafted state (the scaffold stubs) and the "
                     "stack-side outcome of the same gates"),
            "deposit": E129_REL,
            "deposit_sha256": sha0[EXP129],
            "pins_detail": json.loads(json.dumps(
                e129["preflight"]["record_pins_detail"])),
            "pin_provenance": json.loads(json.dumps(
                e129["pin_provenance"])),
            "provenance_corrections": json.loads(json.dumps(
                e129["provenance_corrections"])),
            "gate_outcomes": json.loads(json.dumps(
                e129["gate_outcomes"])),
            "notes": e129.get("notes"),
        }
        counts = scaf_counts()
        artifact = {
            "artifact": "chinese_targets_gates_deposit",
            "artifact_file":
                "results/chinese_targets_gates_deposit.json",
            "exp": "exp231_chinese_targets_deposit",
            "title": ("THE CHINESE-TARGETS GATES DEPOSIT — the wetlab "
                      "companion's final form of the drafted gates"),
            "counts": counts,
            "scaffold": scaffold_block,
            "registration": registration_block,
            "finalized_run": finalized_run,
            "targets": targets,
            "gates": gates_entries,
            "meta": {
                "row_base": (f"{SCAF_REL} (the scaffold's machinery "
                             "VERBATIM: gate definitions, target "
                             "fields, pre-registered grids, pins)"),
                "row_base_sha256": sha0[SCAF_PATH],
                "registration": GDOC_REL,
                "registration_sha256": sha0[GATES_DOC],
                "scaffold_own_deposit": scaffold_block["own_deposit"],
                "finalized_run_deposit": finalized_run["deposit"],
                "finalized_run_deposit_sha256": sha0[EXP129],
                "anchor_reference": E118_REL,
                "anchor_reference_sha256": sha0[EXP118_FULL],
                "n_targets": len(targets),
                "n_gates": len(gates_entries),
                "export_clause": (
                    "the export is a projection, zero re-derivation: "
                    "every gate definition, target field, pre-registered "
                    "grid, coarsening map and TO-PIN constant is copied "
                    "from experiments/scaffold_chinese_targets.py "
                    "VERBATIM (imported live); the finalized-run block "
                    "from results/exp129_chinese_targets.json VERBATIM; "
                    "nothing is re-adjudicated, re-pinned or re-derived "
                    "here"),
                "hash_discipline": (
                    "meta.artifact_sha256_canonical_payload = sha256 of "
                    "this artifact serialized canonically (indent=1, "
                    "sort_keys) WITHOUT the "
                    "artifact_sha256_canonical_payload slot; the run "
                    "deposit (results/exp231_chinese_targets_deposit."
                    "json) records the sha256 of the artifact file "
                    "bytes"),
            },
        }

        # ---- the field-provenance table: zero fields without provenance
        # every observed path gets a row naming its scaffold line (with
        # the source line quoted), its copied-from deposit, or the
        # pre-registered docstring clause it implements.
        BLOCKS = ("counts", "finalized_run", "scaffold.own_deposit",
                  "meta.scaffold_own_deposit",
                  "scaffold.constants.T1_COARSENING",
                  "registration.sections_live", "meta.field_provenance")

        def prefix_covered(path: str) -> bool:
            """True for paths UNDER a registered block (the block's
            row itself still gets a table row — every field carries
            provenance, block roots included)."""
            return any(path.startswith(b + ".")
                       or path.startswith(b + "[") for b in BLOCKS)

        def collect_paths(o, p, acc):
            if isinstance(o, dict):
                for k, v in o.items():
                    np_ = f"{p}.{k}" if p else k
                    acc.append(np_)
                    collect_paths(v, np_, acc)
            elif isinstance(o, list):
                for v in o:
                    if isinstance(v, (dict, list)):
                        collect_paths(v, f"{p}[]", acc)

        paths: list = []
        collect_paths(artifact, "", paths)

        L_DOC = line_of(r'^"""SCAFFOLD')
        L_STATUS = line_of(r"^STATUS:")
        L_EXPNUM = line_of(r"^EXP_NUM = None")
        L_E118 = line_of(r"^EXP118_FULL = ")
        L_GATES = line_of(r"^GATES = \{")
        L_PIN1 = line_of(r"^PIN_T1_METFORMIN\s*=")
        pin1_line = scaf_lines[L_PIN1 - 1]
        todo1 = pin_todo("PIN_T1_METFORMIN").splitlines()
        FM = {"artifact": (PR_REF, _FINAL_FORM_QUOTE),
              "artifact_file": (PR_REF, _FINAL_FORM_QUOTE),
              "exp": (PR_REF, _FINAL_FORM_QUOTE),
              "title": (PR_REF, _FINAL_FORM_QUOTE),
              "counts": (PR_REF, _C2_QUOTE),
              "scaffold": (f"{SCAF_REL} (the deposited machinery, "
                           "verbatim)", _C1_QUOTE),
              "registration": (f"{GDOC_REL} (the registration; the "
                               "scaffold is its carriage)", _C1_QUOTE),
              "finalized_run": (E129_REF, _E129_QUOTE),
              "targets": (f"{SCAF_REL} module docstring, THE THREE "
                          "TARGETS block", _C1_QUOTE),
              "gates": (f"{SCAF_REL} GATES dict + gate docstrings, "
                        "verbatim", _C1_QUOTE),
              "meta": (PR_REF, _FINAL_FORM_QUOTE),
              "scaffold.file": (PR_REF, _FINAL_FORM_QUOTE),
              "scaffold.sha256": (HYG_REF, _C4_QUOTE),
              "scaffold.module_docstring_verbatim":
                  (f"{SCAF_REL}:{L_DOC} (verbatim)", scaf_lines[L_DOC - 1]),
              "scaffold.status_line":
                  (f"{SCAF_REL}:{L_STATUS} (verbatim)",
                   scaf_lines[L_STATUS - 1]),
              "scaffold.machinery_imports":
                  (f"{SCAF_REL} import block (verbatim)",
                   scaf_lines[line_of(r"^from experiments\.") - 1]),
              "scaffold.exp_num": (f"{SCAF_REL}:{L_EXPNUM} (verbatim)",
                                   scaf_lines[L_EXPNUM - 1]),
              "scaffold.own_deposit": (PR_REF, _C3_QUOTE),
              "scaffold.constants":
                  (f"{SCAF_REL} pre-registered grids/constants block "
                   "(verbatim)",
                   scaf_lines[line_of(r"^# ---- pre-registered grids")
                              - 1]),
              "scaffold.pins": (f"{SCAF_REL}:{L_PIN1} (verbatim)",
                                pin1_line),
              "scaffold.pin_todo_verbatim":
                  (f"{SCAF_REL}:{L_PIN1} (verbatim)", pin1_line),
              "scaffold.pin_def_line": (IDX_REF, _C1_QUOTE),
              "registration.file": (PR_REF, _FINAL_FORM_QUOTE),
              "registration.sha256": (HYG_REF, _C4_QUOTE),
              "registration.note":
                  (f"{SCAF_REL}:{L_DOC} (verbatim)",
                   scaf_lines[L_DOC - 1]),
              "registration.sections_live":
                  ("computed at export (the scaffold's own 'Gates §...' "
                   "references vs the registration's headings)",
                   _C1_QUOTE),
              "targets[].target_id":
                  (f"{SCAF_REL} (the T1/T2/T3 paragraph labels)",
                   _C1_QUOTE),
              "targets[].docstring_verbatim":
                  (f"{SCAF_REL} module docstring (verbatim)",
                   scaf_lines[line_of(r"^  T1  ") - 1]),
              "targets[].pin_constant":
                  (f"{SCAF_REL}:{L_PIN1} (verbatim)", pin1_line),
              "targets[].pin_value_scaffold":
                  (f"{SCAF_REL}:{L_PIN1} (verbatim)", pin1_line),
              "targets[].pin_todo_verbatim":
                  (f"{SCAF_REL}:{L_PIN1} (verbatim)", todo1[1]),
              "targets[].pin_def_line": (IDX_REF, _C1_QUOTE),
              "targets[].para_def_line": (IDX_REF, _C1_QUOTE),
              "targets[].gates":
                  ("derived at export from the scaffold's gate-id "
                   "prefixes (T#_*)", _C1_QUOTE),
              "gates[].gate_id":
                  (f"{SCAF_REL}:{L_GATES} (verbatim order)",
                   scaf_lines[L_GATES - 1]),
              "gates[].order":
                  (f"{SCAF_REL}:{L_GATES} (verbatim order)",
                   scaf_lines[L_GATES - 1]),
              "gates[].kind":
                  ("derived at export from the scaffold's gate-id "
                   "prefixes (A_/T#_)", _C1_QUOTE),
              "gates[].target_id":
                  ("derived at export from the scaffold's gate-id "
                   "prefixes (A_/T#_)", _C1_QUOTE),
              "gates[].docstring_verbatim":
                  (f"{SCAF_REL} gate docstrings (verbatim)",
                   scaf_lines[line_of(r"^def anchor_gate") - 1]),
              "gates[].gates_doc_section":
                  ("parsed from each gate docstring's own 'Gates §...' "
                   "reference (the scaffold's inline source reference)",
                   _C1_QUOTE),
              "gates[].gates_doc_sections_all":
                  ("parsed from each gate docstring's own 'Gates §...' "
                   "reference (the scaffold's inline source reference)",
                   _C1_QUOTE),
              "gates[].scaffold_stub":
                  ("computed at export (the scaffold's gate bodies "
                   "raise NotImplementedError)", _C1_QUOTE),
              "gates[].def_line": (IDX_REF, _C1_QUOTE),
              "gates[].finalized_run_outcome": (E129_REF, _E129_QUOTE),
              "meta.row_base": (PR_REF, _FINAL_FORM_QUOTE),
              "meta.row_base_sha256": (HYG_REF, _C4_QUOTE),
              "meta.registration": (PR_REF, _FINAL_FORM_QUOTE),
              "meta.registration_sha256": (HYG_REF, _C4_QUOTE),
              "meta.scaffold_own_deposit": (PR_REF, _C3_QUOTE),
              "meta.finalized_run_deposit": (E129_REF, _E129_QUOTE),
              "meta.finalized_run_deposit_sha256": (HYG_REF, _C3_QUOTE),
              "meta.anchor_reference":
                  (f"{SCAF_REL}:{L_E118} (the scaffold's own reference "
                   "path)", scaf_lines[L_E118 - 1]),
              "meta.anchor_reference_sha256": (HYG_REF, _C4_QUOTE),
              "meta.n_targets": (PR_REF, _C1_QUOTE),
              "meta.n_gates": (PR_REF, _C1_QUOTE),
              "meta.export_clause": (PR_REF, _FINAL_FORM_QUOTE),
              "meta.hash_discipline":
                  (PR_REF, "exp224's hash discipline, verbatim"),
              "meta.field_provenance": (PR_REF, _C1_QUOTE)}
        def const_line(name: str) -> tuple:
            """The scaffold's own line for a constant: its assignment
            line, or — for the constants the scaffold carries by import
            (D_PAR/GEN_BIAS/SEEDS come from exp118_corpus_full_mine) —
            the scaffold's import line naming it."""
            for i, l in enumerate(scaf_lines, 1):
                if re.match(rf"^{name}\s*=", l):
                    return i, l, "verbatim"
            for i, l in enumerate(scaf_lines, 1):
                if re.match(rf"^\s+{name},\s*$", l):
                    return (i, l, "imported into the scaffold verbatim "
                            "from exp118_corpus_full_mine")
            raise AssertionError(f"scaffold line not found for {name}")

        for name in constants:
            ln, line_txt, how = const_line(name)
            FM[f"scaffold.constants.{name}"] = (
                f"{SCAF_REL}:{ln} ({how})", line_txt)
        for name in pin_names:
            ln = line_of(rf"^{name}\s*=")
            FM[f"scaffold.pins.{name}"] = (
                f"{SCAF_REL}:{ln} (verbatim)", scaf_lines[ln - 1])
            FM[f"scaffold.pin_todo_verbatim.{name}"] = (
                f"{SCAF_REL}:{ln} (verbatim)",
                pin_todo(name).splitlines()[1])
            FM[f"scaffold.pin_def_line.{name}"] = (IDX_REF, _C1_QUOTE)

        fp_table = []
        for path in sorted(set(paths)):
            if prefix_covered(path):
                continue
            assert path in FM, f"field without provenance: {path}"
            pl, q = FM[path]
            fp_table.append({"field": path, "protocol_line": pl,
                             "quote": q})
        # the canonical self-hash slot is inserted AFTER the payload
        # hash below, and the table's own root path is not observable
        # at collect time (the table is attached below) — both get
        # their rows registered here so the table is complete in the
        # hashed state (C3's recompute reproduces it)
        for extra_path, extra_pl in (
                ("meta.field_provenance", PR_REF),
                ("meta.artifact_sha256_canonical_payload",
                 "computed at export (the canonical self-hash)")):
            fp_table.append(
                {"field": extra_path, "protocol_line": extra_pl,
                 "quote": ("exp224's hash discipline, verbatim"
                           if extra_path.endswith("_payload")
                           else _C1_QUOTE)})
        fp_table.sort(key=lambda r: r["field"])
        artifact["meta"]["field_provenance"] = fp_table
        # payload hash over the COMPLETE artifact WITHOUT the slot
        # (exp224's hash discipline, verbatim)
        payload_sha = hashlib.sha256(
            E206.ser(artifact).encode("utf-8")).hexdigest()
        artifact["meta"]["artifact_sha256_canonical_payload"] = (
            payload_sha)
        return artifact, {"counts": counts,
                          "target_ids": [r["target_id"]
                                         for r in targets],
                          "gate_ids": [r["gate_id"]
                                       for r in gates_entries]}

    artifact, parts = build_export(n_take=2 if args.smoke else None)

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
            """Zero fields without provenance: every path in the
            artifact is either in the meta.field_provenance table or
            under a table-registered block."""
            known = {r["field"]
                     for r in art["meta"]["field_provenance"]}
            blocks = ("counts", "finalized_run",
                      "scaffold.own_deposit",
                      "meta.scaffold_own_deposit",
                      "scaffold.constants.T1_COARSENING",
                      "registration.sections_live",
                      "meta.field_provenance")

            def cov(path: str) -> bool:
                return (path in known
                        or any(path == b or path.startswith(b + ".")
                               or path.startswith(b + "[")
                               for b in blocks))

            gaps = []

            def walk(o, p):
                if isinstance(o, dict):
                    for k, v in o.items():
                        np_ = f"{p}.{k}" if p else k
                        if not cov(np_):
                            gaps.append(np_)
                        walk(v, np_)
                elif isinstance(o, list):
                    for v in o:
                        if isinstance(v, (dict, list)):
                            walk(v, f"{p}[]")

            walk(art, "")
            return sorted(set(gaps))

        def _c1():
            # ---- GATE-C1 (the projection) ---------------------------
            ids_t = [r["target_id"] for r in artifact["targets"]]
            ids_g = [r["gate_id"] for r in artifact["gates"]]
            want_g = list(gate_fns)
            verb_ok, kind_ok, ref_ok, stub_ok, named_ok = \
                [], [], [], [], []
            for row in artifact["gates"]:
                gid = row["gate_id"]
                fn = gate_fns[gid]
                verb_ok.append(
                    row["docstring_verbatim"] == fn.__doc__)
                kind = "anchor" if gid.startswith("A_") else "target"
                tid = None if kind == "anchor" else gid.split("_")[0]
                kind_ok.append(row["kind"] == kind
                               and row["target_id"] == tid)
                refs = section_refs(fn.__doc__)
                ref_ok.append(bool(refs)
                              and row["gates_doc_sections_all"] == refs
                              and row["gates_doc_section"] == refs[0]
                              and all(section_live(r) for r in refs))
                stub_ok.append(row["scaffold_stub"] is True
                               and "NotImplementedError"
                                   in inspect.getsource(fn))
                named_ok.append(re.search(rf"{fn.__name__}\(\)",
                                          scaf_doc) is not None)
            para_ok = all(
                row["docstring_verbatim"]
                == target_para[row["target_id"]]
                for row in artifact["targets"])
            pin_ok = all(
                row["pin_constant"] == TID_PIN[row["target_id"]]
                and row["pin_value_scaffold"]
                is pins[row["pin_constant"]] is None
                for row in artifact["targets"])
            tgt_gates_ok = all(
                row["gates"] == [g for g in want_g
                                 if g.startswith(row["target_id"]
                                                 + "_")]
                for row in artifact["targets"]) and sorted(
                g for row in artifact["targets"] for g in row["gates"]) \
                == sorted(g for g in want_g
                          if not g.startswith("A_"))
            sections_live = artifact["registration"]["sections_live"]
            live_ok = all(sections_live.values())
            gaps = field_coverage(artifact)
            ok = (ids_t == ["T1", "T2", "T3"] and ids_g == want_g
                  and len(artifact["gates"]) == 7
                  and all(verb_ok) and all(kind_ok) and all(ref_ok)
                  and all(stub_ok) and all(named_ok) and para_ok
                  and pin_ok and tgt_gates_ok and live_ok and not gaps)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "targets_exported": ids_t,
                "gates_exported_in_scaffold_order": ids_g == want_g,
                "gate_docstrings_verbatim": all(verb_ok),
                "kind_target_mapping": all(kind_ok),
                "scaffold_section_refs_live_vs_registration":
                    all(ref_ok) and live_ok,
                "all_gates_scaffold_stubs": all(stub_ok),
                "all_gates_named_in_scaffold_docstring": all(named_ok),
                "target_docstrings_verbatim": para_ok,
                "pin_fields_verbatim": pin_ok,
                "target_gate_membership": tgt_gates_ok,
                "zero_fields_without_provenance": not gaps,
                "provenance_gaps": gaps,
                "field_provenance_rows":
                    len(artifact["meta"]["field_provenance"])}

        def _c2():
            # ---- GATE-C2 (the split integrity) ----------------------
            want = scaf_counts()
            got = artifact["counts"]
            # any drift raises (the registered clause)
            assert got == want, \
                (f"split drift: exported {got} != the scaffold's "
                 f"deposited counts {want}")
            assert got["targets"] == len(pin_names) \
                == len(target_para) == 3
            assert got["gates"] == len(gate_fns) == 7
            assert (got["anchor_gates"], got["target_gates"]) == (1, 6)
            assert got["anchor_gates"] + got["target_gates"] \
                == got["gates"]
            stubs = [g for g, fn in gate_fns.items()
                     if "NotImplementedError" in inspect.getsource(fn)]
            assert sorted(stubs) == sorted(gate_fns), \
                ("the scaffold's drafted-gate state drifted (a stub "
                 "outside GATES or vice versa)")
            assert got["to_pin_constants"] == 3 and all(
                v is None for v in pins.values()), \
                ("the scaffold's TO-PIN state drifted (a pin filled in "
                 "the scaffold)")
            assert (got["dose_grid_coarse"], got["fine_doses"],
                    got["fine_seeds"], got["onsets"],
                    got["timing_seeds"], got["mapping_seeds"],
                    got["coarsening_bands"]) == (5, 6, 7, 8, 8, 3, 5), \
                f"grid-length drift vs the registered grids: {got}"
            return {
                "verdict": "PASS",
                "scaffold_counts_deposited": want,
                "exported_counts": got,
                "split_matches_exactly": True,
                "n_targets": got["targets"],
                "n_gates": got["gates"],
                "grid_lengths": {k: got[k] for k in
                                 ("dose_grid_coarse", "fine_doses",
                                  "fine_seeds", "onsets",
                                  "timing_seeds", "mapping_seeds",
                                  "coarsening_bands")}}

        def _c3():
            # ---- GATE-C3 (the self-containment) ---------------------
            blob = E206.ser(artifact)
            reparsed = json.loads(blob)     # parses standalone
            IDF_G = ("gate_id", "order", "kind", "docstring_verbatim",
                     "gates_doc_section")
            IDF_T = ("target_id", "pin_constant", "docstring_verbatim")
            ident_bad = []
            for row in reparsed["gates"]:
                if not (all(k in row for k in IDF_G)
                        and all(row.get(k) is not None for k in IDF_G)
                        and row.get("target_id")
                        in (None, "T1", "T2", "T3")):
                    ident_bad.append(row.get("gate_id"))
            for row in reparsed["targets"]:
                if not (all(k in row for k in IDF_T)
                        and all(row.get(k) for k in IDF_T)):
                    ident_bad.append(row.get("target_id"))
            claimed = reparsed["meta"].pop(
                "artifact_sha256_canonical_payload")
            recomputed = hashlib.sha256(
                E206.ser(reparsed).encode("utf-8")).hexdigest()
            sha_ok = (claimed == recomputed
                      and isinstance(claimed, str) and len(claimed) == 64)
            own = reparsed["meta"]["scaffold_own_deposit"]
            own_ok = (own["present"] is False
                      and not os.path.exists(SCAF.OUT)
                      and own["path"] == os.path.relpath(SCAF.OUT, ROOT)
                      and isinstance(own["note"], str))
            e129_live = E206.sha256_file(EXP129)
            dep_ok = (reparsed["meta"]["finalized_run_deposit_sha256"]
                      == e129_live == sha0[EXP129]
                      and len(e129_live) == 64)
            ok = (not ident_bad and sha_ok and own_ok and dep_ok
                  and reparsed["meta"]["n_gates"] == 7
                  and reparsed["meta"]["n_targets"] == 3)
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "parses_standalone": True,
                "gate_identity_fields": list(IDF_G),
                "target_identity_fields": list(IDF_T),
                "identity_violations": ident_bad,
                "artifact_sha256_canonical_payload": claimed,
                "artifact_payload_sha_ok": sha_ok,
                "scaffold_own_deposit": own,
                "scaffold_own_deposit_ok": own_ok,
                "finalized_run_deposit_sha256": e129_live,
                "finalized_run_deposit_sha_ok": dep_ok,
                "n_gates_meta": reparsed["meta"]["n_gates"],
                "n_targets_meta": reparsed["meta"]["n_targets"]}

        def _c4():
            # ---- GATE-C4 (hygiene) ----------------------------------
            os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
            blob = E206.ser(artifact)
            with open(ARTIFACT, "w", encoding="utf-8") as f:
                f.write(blob)
            artifact_rerun, _parts2 = build_export()
            determinism = E206.ser(artifact_rerun) == blob
            sha1 = {p: E206.sha256_file(p) for p in sha0}
            unchanged = all(sha1[p] == sha0[p] for p in sha0)
            ok = unchanged and determinism
            return {
                "verdict": "PASS" if ok else "REFUTE",
                "scaffold_files_byte_unchanged": unchanged,
                "export_deterministic": determinism,
                "artifact_file": os.path.relpath(ARTIFACT, ROOT),
                "artifact_sha256_file": E206.sha256_file(ARTIFACT),
                "artifact_bytes": len(blob.encode("utf-8")),
                "file_sha256": {os.path.relpath(p, ROOT): sha0[p]
                                for p in sha0}}

        # ---- evaluate each gate exactly once ---------------------------
        _gate("GATE-C1", _c1)
        _gate("GATE-C2", _c2)
        _gate("GATE-C3", _c3)
        _gate("GATE-C4", _c4)

        n_pass = sum(1 for v in gates.values()
                     if v["verdict"] == "PASS")
        n_ref = sum(1 for v in gates.values()
                    if v["verdict"] == "REFUTE")
        sp = artifact["counts"]
        n_refuted = ", ".join(k for k, v in gates.items()
                              if v["verdict"] == "REFUTE")
        verdict = (
            f"{n_pass}/{len(gates)} gates PASS | the drafted "
            f"{sp['targets']}-target/{sp['gates']}-gate "
            f"Chinese-targets scaffold exported as the wetlab "
            f"companion's final form ({sp['anchor_gates']} anchor + "
            f"{sp['target_gates']} target gates, all scaffold stubs, "
            f"machinery verbatim; the scaffold's own deposit absent "
            f"per the C3 'if any' clause — the finalized run exp129's "
            f"outcomes carried beside them) | artifact "
            f"results/chinese_targets_gates_deposit.json deposited"
            if n_ref == 0 else
            f"REFUTE {n_ref} gate(s) ({n_refuted}) "
            f"| counts {sp['targets']}/{sp['gates']}")

        pre_block_lines, in_pre = [], False
        for l in __doc__.splitlines():
            if "PRE-REGISTRATION" in l:
                in_pre = True
            if in_pre:
                pre_block_lines.append(l)
            if in_pre and l.startswith("RUN:"):
                break
        gates_block_lines, in_g = [], False
        for l in __doc__.splitlines():
            if l.startswith("GATES (each evaluated exactly once):"):
                in_g = True
            if in_g:
                gates_block_lines.append(l)
            if in_g and l.startswith("NO post-hoc tuning"):
                break

        deposit_sections = {
            "scaffold_counts_deposited": parts["counts"],
            "exported_target_ids": parts["target_ids"],
            "exported_gate_ids": parts["gate_ids"],
            "gates_doc_section_refs":
                {row["gate_id"]: row["gates_doc_sections_all"]
                 for row in artifact["gates"]},
            "sections_live":
                artifact["registration"]["sections_live"],
            "scaffold_stub_all": all(r["scaffold_stub"]
                                     for r in artifact["gates"]),
            "finalized_run_outcomes": e129["gate_outcomes"],
            "own_deposit_present":
                artifact["scaffold"]["own_deposit"]["present"],
            "field_provenance_rows":
                len(artifact["meta"]["field_provenance"]),
            "artifact": {
                "file": os.path.relpath(ARTIFACT, ROOT),
                "sha256": E206.sha256_file(ARTIFACT),
                "sha256_canonical_payload":
                    artifact["meta"][
                        "artifact_sha256_canonical_payload"],
                "bytes": len(E206.ser(artifact).encode("utf-8")),
                "n_targets": len(artifact["targets"]),
                "n_gates": len(artifact["gates"]),
                "parses_standalone": True}}
        deposit = {
            "exp": "exp231_chinese_targets_deposit",
            "claim": (
                "THE CHINESE-TARGETS GATES DEPOSIT (L201's registered "
                "next; the Section 5 item; the last open deposit leg): "
                "the scaffold's drafted gates "
                "(experiments/scaffold_chinese_targets.py — 3 targets "
                "x 7 gates: the anchor + the T1 metformin dose-axis/"
                "biphasic pair, the T2 Usp7 penetrance/timing pair, "
                "the T3 opa1 impairment/rescue pair) exported as the "
                "wetlab companion's final form — a self-contained, "
                "provenance-carrying artifact "
                "(results/chinese_targets_gates_deposit.json) the "
                "wetlab side can execute without the stack: every gate "
                "definition, target field, pre-registered grid, "
                "coarsening map and TO-PIN constant copied from the "
                "scaffold VERBATIM (imported live, zero re-derivation, "
                "every field provenance-tagged to its scaffold line), "
                "the scaffold's own §-references verified live against "
                "the registration (research/chinese_targets_gates.md), "
                "and the drafted gates' deposited run (exp129: pins "
                "detail, pin provenance, provenance corrections, gate "
                "outcomes) carried verbatim beside them; the scaffold's "
                "own OUT deposit does not exist (the scaffold never "
                "ran — the C3 'if any' clause, disclosed)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 799a35c, batch 14; gates C1-C4 "
                    "fixed there, each evaluated exactly once)"),
                "pre_registration_block_verbatim":
                    "\n".join(pre_block_lines),
                "gates_block_verbatim":
                    "\n".join(gates_block_lines)},
            "instruments": {
                "scaffold": {"file": SCAF_REL,
                             "sha256": sha0[SCAF_PATH]},
                "registration": {"file": GDOC_REL,
                                 "sha256": sha0[GATES_DOC]},
                "finalized_run_deposit": {"file": E129_REL,
                                          "sha256": sha0[EXP129]},
                "anchor_reference": {"file": E118_REL,
                                     "sha256": sha0[EXP118_FULL]},
                "machinery": (
                    "experiments/exp203_wetlab_scaffold.py's ser/"
                    "sha256_file helpers via exp206's re-export "
                    "(exp224's final-form discipline verbatim)"),
                "exp224_discipline": (
                    "per-entry identity, split integrity, "
                    "self-containment, determinism")},
            "sections": deposit_sections,
            "gates": gates,
            "artifact": os.path.relpath(ARTIFACT, ROOT),
            "registration": GDOC_REL,
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
    print(f"  SMOKE: {sp['targets']} targets / {sp['gates']} gates on "
          f"the first {len(artifact['targets'])} target and "
          f"{len(artifact['gates'])} gate entries; the artifact "
          f"serializes ({len(blob)} chars) and parses standalone "
          f"- DISCARDED (no artifact write, no deposit, no gates)")
    return {"exp": "exp231_chinese_targets_deposit", "smoke": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
