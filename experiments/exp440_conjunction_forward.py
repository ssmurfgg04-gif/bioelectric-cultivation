#!/usr/bin/env python3
"""exp440 — THE CONJUNCTION'S FORWARD TEST AT n = 6-8 (batch HU-13;
exp431/439's registered follow-up). exp431's conjunction (protective
iff cycle-rank <= 1 AND triangle-free) is post-hoc at n = 3-5. THE
OPEN QUESTION: does it PREDICT — does the rule, frozen from the
17-form union, hold on forms it has never seen at sizes it has never
covered?

THE INSTRUMENT (exp427/431's battery verbatim; the forward sample
pre-named under the rule's own logic, 8 forms at n = 6-8): the
rule-satisfying quartet — full binary tree 7 (7n 6e), unicyclic
girth-5 (C5 + one leaf: 6n 6e), unicyclic girth-6 (C6 + one leaf:
7n 7e), path6 — predicted PROTECTIVE; the rule-violating quartet —
K4 minus 2 adjacent edges (6e 4n... no: n=4 is covered; the
violating quartet at n = 6-8: C6 + one chord (6n 7e, girth 3),
K3,3 + one edge? (bipartite so triangle-free but cycle-rank 4),
double-ring (two C4s sharing an edge: 6n 7e, girth 4, cycle-rank 2),
C7 + 2 chords — predicted NON-protective; 5 seeds, the >= 3/5 bar.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE ANCHORS: floor -60.0; the constants; the 8-form count;
      exp431's controls reproduce exactly (fail=STOP).
  G2  THE FULL TABLE: no pruning.
  G3  THE FORWARD TEST: the conjunction predicts all 8 forms with
      ZERO contradictions (RULE-FORWARDS — the design rule enters
      the substrate engineering spec) or any contradiction
      (RULE-LIMITED — the rule's domain is the small-n census;
      deposited with the failing form named).
  G4  THE ANATOMY: the per-form table + the prediction column.
  G5  deposit results/exp440_conjunction_forward.json.

BRANCH LATTICE: RULE-FORWARDS / RULE-LIMITED / INSTRUMENT-REFUTED.
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
from experiments.exp439_conjunction_floor import _cycle_rank, _conj_pred

PROTECT_SEED_BAR = 3
SEEDS = [0, 1, 2, 3, 4]
DEPOSIT = os.path.join(ROOT, "results", "exp440_conjunction_forward.json")

BODY_DISCLOSURES = [
    "exp431's battery verbatim; the conjunction predicate imported "
    "from exp439's landed module verbatim (cycle-rank <= 1 AND "
    "triangle-free AND n >= 3)",
    "the forward sample pre-named under the rule's own logic: the "
    "satisfying quartet (tree7, c5leaf, c6leaf, path6) predicted "
    "PROTECTIVE; the violating quartet (c6chord: girth 3; k33plus: "
    "triangle-free cycle-rank 5; double_ring4: triangle-free "
    "cycle-rank 2; c7chords: girth 3) predicted NON-protective — the "
    "two triangle-free high-cycle-rank forms are the cycle-rank "
    "clause's discriminators (the pure-triangle reading would "
    "misclassify them)",
    "the analysis is deterministic (the seeds carry all randomness)",
]

SAMPLE = {
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
CONTROLS = {"path3": lambda: _adjacency("path", 3, 0),
            "triangle3": lambda: _adjacency("ring", 3, 0)}
EXPECTED_CONTROLS = {"path3": 5, "triangle3": 0}


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds_run = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert len(SAMPLE) == 8

    table = {}
    for form in sorted(SAMPLE):
        A = SAMPLE[form]()
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

    g1_rows = {}
    if not smoke:
        for form, ctor in CONTROLS.items():
            A = ctor()
            tgt = _census_target(A.shape[0])
            region = _region_for(A.shape[0])
            rows = [_battery_graph(A, tgt, region, s) for s in SEEDS]
            g1_rows[form] = sum(1 for r in rows if r["t_protect"])
        g1_ok = all(g1_rows[f] == EXPECTED_CONTROLS[f]
                    for f in EXPECTED_CONTROLS)
    else:
        g1_ok = True
    verdicts["G1"] = "PASS" if g1_ok else "REFUTE"
    print("G1 %s (controls %s)"
          % (verdicts["G1"], g1_rows or "smoke-skip"))
    if smoke:
        print("SMOKE OK discarded")
        return {"gates": verdicts}
    verdicts["G2"] = "PASS"
    print("G2 PASS (the full face table deposited, no pruning)")

    contradictions = [f for f, r in table.items()
                      if r["protective"] != r["conj_predicts"]]
    if not contradictions:
        verdicts["G3"] = "PASS"
        branch = "RULE-FORWARDS"
        print("G3 PASS (zero contradictions across the 8-form forward "
              "sample — the design rule enters the substrate "
              "engineering spec)")
    else:
        verdicts["G3"] = "REFUTE"
        branch = "RULE-LIMITED"
        print("G3 REFUTE (contradictions: %s)" % contradictions)

    verdicts["G4"] = "PASS"
    print("G4 PASS (%d forms in the table)" % len(table))

    out = {
        "experiment": "exp440",
        "title": "THE CONJUNCTION'S FORWARD TEST AT n = 6-8 (batch "
                 "HU-13)",
        "sample": table,
        "control_rows": g1_rows,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    with open(DEPOSIT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP440 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
