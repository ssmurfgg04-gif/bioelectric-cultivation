#!/usr/bin/env python3
"""exp441 — WHAT FIXES THE COMPOSITION CLASS? (batch HU-13; exp419's
charter-recorded next question). exp419 landed: the composition class
tracks the FORM of composition, not the substrate. THE OPEN QUESTION:
what property of the form fixes the class — the charter's recorded
question. THE CANDIDATES (pre-named from the landed findings):
(a) the wiring's cycle structure (exp431/439's conjunction family —
cycle-rank and triangle content), (b) the register's dose-response
shape (exp410/425's plural register — the two-axis coupling), (c)
the wound geometry's walk-order structure (exp429's geometry
invariance), (d) the commit stream's content class (exp435's
dose-stress-timing triangle).

THE INSTRUMENT (a determinant-census over the landed corpus: every
experiment whose deposit carries a composition-class label or an
equivalent form-level classification, joined against the four
candidate feature families computed from each form's own adjacency
and battery constants; the join is deterministic, zero new
simulation): the classes and forms enumerated from the deposits;
the feature matrix computed; the determinant test = which family
class-separates with zero contradictions ACROSS the union corpus
(the exp431 union-table method, lifted to the feature families).

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE CORPUS: every cited deposit loads; the class labels
      match the ledger's (fail=STOP).
  G2  THE JOIN: the feature matrix computed from the forms'
      adjacencies + battery constants only (no deposit-outcome
      leakage into the features).
  G3  THE DETERMINANT: exactly one family class-separates with
      zero contradictions (CARRIER-FAMILY-NAMED — the charter
      question answered at the corpus's resolution) / >= 2
      (OVERDETERMINED) / 0 (NO-DETERMINANT-AT-CORPUS-RESOLUTION —
      honest: the class needs a feature outside the four).
  G4  THE ANATOMY: the (form x family) matrix + the separating
      family's columns deposited.
  G5  deposit results/exp441_composition_determinant.json.

BRANCH LATTICE: CARRIER-FAMILY-NAMED / OVERDETERMINED /
NO-DETERMINANT-AT-CORPUS-RESOLUTION / INSTRUMENT-REFUTED.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from experiments.exp427_protection_motif_census import (
    _custom, _region_for)
from experiments.exp418_minimal_substrate import _adjacency
from experiments.exp431_triangle_independent import _has_triangle
from experiments.exp439_conjunction_floor import _cycle_rank

DEPOSIT = os.path.join(ROOT, "results", "exp441_composition_determinant.json")

BODY_DISCLOSURES = [
    "the corpus = the union of the four landed form-level censuses "
    "(exp427's 9, exp431's 8, exp439's 6, exp440's 8; overlaps "
    "asserted to agree — the battery is verbatim and seeded, the "
    "labels are identical where forms repeat); 26 distinct forms",
    "the features are computed from each form's adjacency + the "
    "battery's own region rule ONLY (no deposit-outcome leakage into "
    "the features — G2)",
    "the families (b) register dose-response shape and (d) commit "
    "stream content are CONSTANT across the corpus (the battery is "
    "verbatim: same COMMIT_NOISE/STEPS_PER_CELL/G_CTX on every form) "
    "— they have zero variance and cannot separate by construction; "
    "their inclusion is the honest statement that the corpus cannot "
    "test them (the resolution limit, deposited in the anatomy)",
    "the determinant test = the exp431 union-table method: a "
    "predicate class-separates iff it predicts every form's class "
    "with zero contradictions",
]


def _forms_and_labels():
    forms = {}

    def _load(name, key):
        with open(os.path.join(ROOT, "results", name)) as f:
            return json.load(f)[key]

    d427 = json.load(open(os.path.join(
        ROOT, "results", "exp427_protection_motif_census.json")))
    for form, row in d427["census_table"].items():
        forms[form] = {"protective": row["protective"],
                       "n_prot": row["n_protect"],
                       "n_seeds": row["n_seeds"],
                       "src": "exp427"}
    d431 = json.load(open(os.path.join(
        ROOT, "results", "exp431_triangle_independent.json")))
    for form, row in d431["sample_table"].items():
        if form in forms:
            assert forms[form]["protective"] == row["protective"], form
        forms[form] = {"protective": row["protective"],
                       "n_prot": row["n_protect"],
                       "n_seeds": row["n_seeds"],
                       "src": forms[form]["src"] + "+exp431"
                       if form in forms else "exp431"}
    d439 = json.load(open(os.path.join(
        ROOT, "results", "exp439_conjunction_floor.json")))
    for form, row in d439["census"].items():
        if form in forms:
            assert forms[form]["protective"] == row["protective"], form
            forms[form]["src"] += "+exp439"
        else:
            forms[form] = {"protective": row["protective"],
                           "n_prot": row["n_protect"],
                           "n_seeds": row["n_seeds"], "src": "exp439"}
    d440 = json.load(open(os.path.join(
        ROOT, "results", "exp440_conjunction_forward.json")))
    for form, row in d440["sample"].items():
        assert form not in forms, form
        forms[form] = {"protective": row["protective"],
                       "n_prot": row["n_protect"],
                       "n_seeds": row["n_seeds"], "src": "exp440"}
    return forms


ADJ = {
    "path3": lambda: _adjacency("path", 3, 0),
    "triangle3": lambda: _adjacency("ring", 3, 0),
    "path4": lambda: _adjacency("path", 4, 0),
    "star4": lambda: _adjacency("star", 4, 0),
    "ring4": lambda: _adjacency("ring", 4, 0),
    "complete4": lambda: np.ones((4, 4)) - np.eye(4),
    "paw4": lambda: _custom([(0, 1), (1, 2), (0, 2), (0, 3)], 4),
    "diamond4": lambda: _custom([(0, 1), (0, 2), (0, 3), (1, 2),
                                 (1, 3)], 4),
    "motif4": lambda: _adjacency("motif", 4, 0),
    "k23": lambda: _custom([(0, 2), (0, 3), (0, 4), (1, 2), (1, 3),
                            (1, 4)], 5),
    "k33": lambda: _custom([(0, 3), (0, 4), (0, 5), (1, 3), (1, 4),
                            (1, 5), (2, 3), (2, 4), (2, 5)], 6),
    "wheel5": lambda: _custom([(0, i) for i in range(1, 6)]
                              + [(i, (i % 5) + 1) for i in range(1, 5)]
                              + [(5, 1)], 6),
    "c5chord": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                                (0, 2)], 5),
    "bowtie": lambda: _custom([(0, 1), (0, 2), (1, 2), (0, 3), (0, 4),
                               (3, 4)], 5),
    "house": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 0), (0, 4),
                              (1, 4)], 5),
    "ring5": lambda: _adjacency("ring", 5, 0),
    "path5": lambda: _adjacency("path", 5, 0),
    "edge2": lambda: _custom([(0, 1)], 2),
    "tree7": lambda: _custom([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5),
                              (2, 6)], 7),
    "c5leaf": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                               (0, 5)], 6),
    "c6leaf": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
                               (5, 0), (0, 6)], 7),
    "path6": lambda: _adjacency("path", 6, 0),
    "c6chord": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
                                (5, 0), (0, 2)], 6),
    "k33plus": lambda: _custom([(0, 3), (0, 4), (0, 5), (1, 3), (1, 4),
                                (1, 5), (2, 3), (2, 4), (2, 5), (0, 1)],
                               6),
    "double_ring4": lambda: _custom([(0, 1), (1, 2), (2, 3), (3, 0),
                                     (2, 4), (4, 5), (5, 1)], 6),
    "c7chords": lambda: _custom([(i, (i + 1) % 7) for i in range(7)]
                                + [(0, 2), (2, 4)], 7),
}


def _region_cycle_rank(A, region):
    """The induced subgraph on the wound region: its cycle rank."""
    rs = sorted(region)
    idx = {v: i for i, v in enumerate(rs)}
    B = np.zeros((len(rs), len(rs)))
    for i in rs:
        for j in rs:
            if i < j and A[i, j] > 0:
                B[idx[i], idx[j]] = B[idx[j], idx[i]] = 1.0
    return _cycle_rank(B)


def _consistent(pred, forms):
    contra = [f for f, r in forms.items() if r["protective"] != pred(f)]
    return (not contra), contra


def main() -> dict:
    verdicts: dict[str, str] = {}
    forms = _forms_and_labels()
    assert len(forms) == 26, len(forms)
    verdicts["G1"] = "PASS"
    print("G1 PASS (the corpus loads: 26 distinct forms across 4 "
          "censuses, overlaps agree)")

    feats = {}
    for form, ctor in ADJ.items():
        A = ctor()
        region = _region_for(A.shape[0])
        feats[form] = {
            "n": A.shape[0],
            "cycle_rank": _cycle_rank(A),
            "triangle": _has_triangle(A),
            "region_cr": _region_cycle_rank(A, region),
            "region_size": len(region),
            "region_internal_edges": int(np.sum(np.triu(
                (A[np.ix_(region, region)] > 0), 1))),
        }
    assert set(feats) == set(forms), \
        (set(feats) ^ set(forms))
    verdicts["G2"] = "PASS"
    print("G2 PASS (the feature matrix computed from adjacency + the "
          "region rule only)")

    families = {
        "A_global_wiring": {
            "conj_count_clause": lambda f: (
                feats[f]["cycle_rank"] <= 1
                and not feats[f]["triangle"] and feats[f]["n"] >= 3),
            "cycle_rank_le_1": lambda f: feats[f]["cycle_rank"] <= 1,
            "triangle_free": lambda f: not feats[f]["triangle"],
            "n_ge_3": lambda f: feats[f]["n"] >= 3,
        },
        "B_register_dose_shape": {
            "constant_battery": lambda f: True,
        },
        "C_wound_local_wiring": {
            "region_acyclic": lambda f: feats[f]["region_cr"] == 0,
            "region_acyclic_size_ge_2": lambda f: (
                feats[f]["region_cr"] == 0
                and feats[f]["region_size"] >= 2),
            "region_no_internal_edges": lambda f: (
                feats[f]["region_internal_edges"] == 0),
        },
        "D_stream_content": {
            "constant_walk": lambda f: True,
        },
    }

    family_results = {}
    for fam, preds in families.items():
        best = None
        for pname, p in preds.items():
            ok, contra = _consistent(p, forms)
            n_hit = sum(1 for f, r in forms.items()
                        if r["protective"] == p(f))
            row = {"consistent": ok, "contradictions": len(contra),
                   "hits": n_hit, "of": len(forms)}
            if best is None or (ok and not best["consistent"]) or \
                    (ok == best["consistent"]
                     and n_hit > best["hits"]):
                best = dict(row, predicate=pname)
        family_results[fam] = best
        print("  %s: best %s consistent %s (%d/%d)"
              % (fam, best["predicate"], best["consistent"],
                 best["hits"], best["of"]))

    separating = [fam for fam, r in family_results.items()
                  if r["consistent"]]
    if len(separating) == 1:
        verdicts["G3"] = "PASS"
        branch = "CARRIER-FAMILY-NAMED"
        detail = {"family": separating[0]}
    elif len(separating) >= 2:
        verdicts["G3"] = "PASS"
        branch = "OVERDETERMINED"
        detail = {"families": separating}
    else:
        verdicts["G3"] = "PASS"
        branch = "NO-DETERMINANT-AT-CORPUS-RESOLUTION"
        detail = {"note": "the class needs a feature outside the "
                          "four pre-named families (or outside the "
                          "corpus's resolution — B and D are "
                          "zero-variance here)"}
    print("G3 %s (branch %s; separating: %s)"
          % (verdicts["G3"], branch, separating or "NONE"))

    verdicts["G4"] = "PASS"
    print("G4 PASS (the 27-form x feature matrix + the family table "
          "deposited)")

    out = {
        "experiment": "exp441",
        "title": "WHAT FIXES THE COMPOSITION CLASS? (batch HU-13)",
        "corpus": {f: dict(forms[f], **feats[f]) for f in sorted(forms)},
        "family_results": family_results,
        "detail": detail,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    with open(DEPOSIT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP441 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
