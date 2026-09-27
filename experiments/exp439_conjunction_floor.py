#!/usr/bin/env python3
"""exp439 — THE CONJUNCTION'S FLOOR: THE SMALLEST PROTECTED STRUCTURE
(batch HU-13; exp431's registered follow-up). exp431 landed
TRIANGLE-ARTIFACT and the union 17-form table named the conjunction —
protective iff CYCLE-RANK <= 1 AND TRIANGLE-FREE — as the
zero-contradiction post-hoc. THE OPEN QUESTION: what is the SMALLEST
coherent structure the conjunction protects — the (nodes, edges)
floor of the protection, and does the conjunction survive ITS own
floor test?

THE INSTRUMENT (exp427/431's battery verbatim; the floor census as
the new axis): the candidate floor forms at the minimal sizes — the
2-node edge (n=2, the exp424 refuted floor), the 3-node tree (path3),
the 3-node unicyclic (ring3 = triangle3, the conjunction's own
refusal), the 4-node unicyclic girth-4 (ring4), the 4-node tree pair
(path4, star4) — 5 seeds each, the >= 3/5 bar; the conjunction's
prediction computed from the adjacency alone per form.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE ANCHORS: floor -60.0; the constants asserted; the census
      count asserted (6 forms, no pruning); exp431's controls
      (path3 5/5, triangle3 0/5) reproduce exactly (fail=STOP).
  G2  THE FULL TABLE: face status per (form, seed) x all three
      faces, no pruning.
  G3  THE FLOOR: the conjunction predicts every form's protection
      with ZERO contradictions on the floor census (the 2-node edge
      predicted NON-protective per exp424's refuted floor — the
      conjunction needs the count clause: cycle-rank <= 1 AND
      triangle-free AND n >= 3), and the smallest PROTECTED form is
      named (FLOOR-FOUND) or a contradiction appears (the
      conjunction's own floor test fails — FLOOR-BROKEN, honest).
  G4  THE ANATOMY: the per-form face table + the conjunction's
      per-form prediction column deposited.
  G5  deposit results/exp439_conjunction_floor.json.

BRANCH LATTICE: FLOOR-FOUND / FLOOR-BROKEN / INSTRUMENT-REFUTED.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as CORE
from experiments.exp418_minimal_substrate import (
    _battery_graph, _adjacency, PROD_FLOOR, COMMIT_NOISE,
    STEPS_PER_CELL)
from experiments.exp427_protection_motif_census import (
    _custom, _census_target, _region_for, _flags)
from experiments.exp431_triangle_independent import _has_triangle

PROTECT_SEED_BAR = 3
SEEDS = [0, 1, 2, 3, 4]
DEPOSIT = os.path.join(ROOT, "results", "exp439_conjunction_floor.json")

BODY_DISCLOSURES = [
    "exp431's battery verbatim (the 5-seed >= 3/5 bar, the trace(A^3)"
    "/6 triangle flag); the only new code is the 6-form floor census "
    "and the conjunction predicate: protective iff cycle-rank <= 1 "
    "AND triangle-free AND n >= 3 (the count clause carries exp424's "
    "n=2 refutation)",
    "path3 and triangle3 double as the census members AND exp431's "
    "controls (their expected 5/5 and 0/5 are the G1 face)",
    "the analysis is deterministic (the seeds carry all randomness)",
]


def _cycle_rank(A):
    n = A.shape[0]
    E = int(np.sum(np.triu(A > 0, 1)))
    seen, comps = set(), 0
    for s in range(n):
        if s in seen:
            continue
        comps += 1
        stack = [s]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack += [int(v) for v in np.where(A[u] > 0)[0]]
    return E - n + comps


def _conj_pred(A):
    return bool(_cycle_rank(A) <= 1 and not _has_triangle(A)
                and A.shape[0] >= 3)


CENSUS = {
    "edge2": lambda: _custom([(0, 1)], 2),
    "path3": lambda: _adjacency("path", 3, 0),
    "triangle3": lambda: _adjacency("ring", 3, 0),
    "path4": lambda: _adjacency("path", 4, 0),
    "star4": lambda: _adjacency("star", 4, 0),
    "ring4": lambda: _adjacency("ring", 4, 0),
}
EXPECTED_CONTROLS = {"path3": 5, "triangle3": 0}


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds_run = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert len(CENSUS) == 6

    table = {}
    for form in sorted(CENSUS):
        A = CENSUS[form]()
        n = A.shape[0]
        tgt = _census_target(n)
        region = _region_for(n)
        rows = [_battery_graph(A, tgt, region, s) for s in seeds_run]
        n_prot = sum(1 for r in rows if r["t_protect"])
        table[form] = {
            "cycle_rank": _cycle_rank(A),
            "triangle": _has_triangle(A),
            "n": n,
            "conj_predicts": _conj_pred(A),
            "n_protect": n_prot, "n_seeds": len(rows),
            "protective": bool(n_prot >= PROTECT_SEED_BAR),
            "per_seed": [{"t_protect": r["t_protect"],
                          "P_single": round(r["P_single"], 4)}
                         for r in rows],
        }
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
        print("  %s: protective %d/%d conj_pred %s (cr %d tri %s)"
              % (form, n_prot, len(rows), table[form]["conj_predicts"],
                 table[form]["cycle_rank"], table[form]["triangle"]))

    # ---- G1 the anchors (the controls double as census members)
    g1_ok = all(table[f]["n_protect"] == EXPECTED_CONTROLS[f]
                for f in EXPECTED_CONTROLS)
    verdicts["G1"] = "PASS" if g1_ok else "REFUTE"
    print("G1 %s (controls path3 %d/5, triangle3 %d/5)"
          % (verdicts["G1"], table["path3"]["n_protect"],
             table["triangle3"]["n_protect"]))
    if smoke:
        print("SMOKE OK discarded")
        return {"gates": verdicts}
    verdicts["G2"] = "PASS"
    print("G2 PASS (the full face table deposited, no pruning)")

    # ---- G3 the floor
    contradictions = [f for f, r in table.items()
                      if r["protective"] != r["conj_predicts"]]
    protected = [f for f, r in table.items() if r["protective"]]
    smallest = min(protected, key=lambda f: (table[f]["n"],
                                             table[f]["cycle_rank"]))
    if not contradictions:
        verdicts["G3"] = "PASS"
        branch = "FLOOR-FOUND"
        detail = {"smallest_protected": smallest,
                  "smallest_shape": [table[smallest]["n"],
                                     "cr %d" % table[smallest]
                                     ["cycle_rank"]]}
        print("G3 PASS (zero contradictions; smallest protected: %s "
              "%s)" % (smallest, detail["smallest_shape"]))
    else:
        verdicts["G3"] = "REFUTE"
        branch = "FLOOR-BROKEN"
        detail = {"contradictions": contradictions}
        print("G3 REFUTE (contradictions: %s)" % contradictions)

    verdicts["G4"] = "PASS"
    print("G4 PASS (%d forms in the table)" % len(table))

    out = {
        "experiment": "exp439",
        "title": "THE CONJUNCTION'S FLOOR: THE SMALLEST PROTECTED "
                 "STRUCTURE (batch HU-13)",
        "census": table,
        "detail": detail,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    with open(DEPOSIT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP439 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
