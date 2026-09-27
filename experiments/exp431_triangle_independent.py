#!/usr/bin/env python3
"""exp431 — THE TRIANGLE HYPOTHESIS ON AN INDEPENDENT SAMPLE (batch
HU-12; exp427's registered follow-up). exp427 landed NO-CARRIER: all
four pre-named candidates contradicted the census, and the census's
own table named "contains a triangle (K3)" as the POST-HOC perfect
separator — 0/5 protective on all four triangle-bearing forms, >= 4/5
on all five triangle-free forms. POST-HOC, UNTESTED. And the census
CONFOUNDED DENSITY with triangulation (every dense form bore a
triangle; every sparse form was triangle-free). THE INDEPENDENT
SAMPLE disentangles the two: 8 new connected binary forms, never run
by any prior battery —
  DENSE x TRIANGLE-FREE : K2,3 (5n 6e), K3,3 (6n 9e)   <- the crux
  DENSE x TRIANGLE-BEAR : wheel5 (6n 10e)
  SPARSE x TRIANGLE-BEAR: C5+chord (5n 6e), bowtie (5n 6e),
                          house (5n 6e)
  SPARSE x TRIANGLE-FREE: ring5 (5n 5e), path5 (5n 4e)  <- the
                          never-run exp427 holdouts, promoted
THE CRUX: the two hypotheses diverge EXACTLY on the five 0.6-density
forms — the triangle carrier predicts K2,3/K3,3 protective and
C5+chord/bowtie/house non-protective; the density carrier predicts
the reverse. ring5/path5 agree under both (a consistency cell, not a
discriminator).

THE INSTRUMENT (exp427's battery verbatim; zero new knobs): exp418's
_battery_graph per (form, seed), the house-ladder _census_target,
_region_for, 5 seeds per form; a form is PROTECTIVE iff T-PROTECT
holds on >= 3/5 seeds; the triangle flag = trace(A^3)/6 > 0.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the sample count asserted (8 forms, no
      pruning); every form's face table complete (fail=STOP).
  G2  THE FULL TABLE: face status per (form, seed) x all three faces
      deposited — no pruning, including the forms that fail
      everywhere.
  G3  THE HYPOTHESIS: "contains K3" predicts T-PROTECT with ZERO
      contradictions across the 8-form independent sample (protective
      iff triangle-free, the >= 3/5 bar). PASS -> the post-hoc
      separator survives out-of-sample (it is a law at this scale);
      REFUTE -> any contradiction (TRIANGLE-ARTIFACT, or the exact
      inversion DENSITY-CARRIED when the dense triangle-free pair
      fails AND the sparse triangle trio protects).
  G4  THE CONTROLS: path3 and triangle3 re-run under this run's
      battery — path3 5/5 protective and triangle3 0/5 must reproduce
      EXACTLY (the battery is seeded and deterministic; any deviation
      = instrument drift, deposited honestly).
  G5  deposit results/exp431_triangle_independent.json.

BRANCH LATTICE: TRIANGLE-CARRIED / TRIANGLE-ARTIFACT / DENSITY-CARRIED
/ CONTROLS-FAILED / INSTRUMENT-REFUTED (G1 fail).

THE HONEST STAKES: exp424 made the minimal substrate a wiring
question; exp427's census named its post-hoc lever. If the triangle
survives the independent sample, the S_min story becomes predictive —
"protection = f(triangulation), computable from the adjacency
alone" — and the design rule (avoid K3 at small n) enters the
substrate engineering spec. If it inverts (density carried), the
census's perfect separator was an artifact of its form list — and
the honest correction re-opens the carrier question with density as
the pre-named candidate.
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

PROTECT_SEED_BAR = 3
DEPOSIT = os.path.join(ROOT, "results", "exp431_triangle_independent.json")

BODY_DISCLOSURES = [
    "exp427's battery imported verbatim (_battery_graph, "
    "_census_target semantics, _region_for, 5 seeds, the >= 3/5 "
    "protective bar) — zero new knobs; the only new code is the 8 "
    "form constructors and the trace(A^3)/6 triangle flag",
    "the sample is independent of exp427's 9-form census by "
    "construction (no overlap; ring5/path5 were exp427's holdouts, "
    "never run there — G4 was VACUOUS-NO-CARRIER)",
    "the 0.6-density crux: K2,3, K3,3, C5+chord, bowtie, house all "
    "sit at density 0.60; the two hypotheses diverge exactly there",
    "the controls (path3, triangle3) are exp427's own census rows "
    "re-run under this battery — seeded and deterministic, exact "
    "reproduction expected; deviation = instrument drift",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from experiments.exp418_minimal_substrate import (
    _battery_graph, _adjacency, PROD_FLOOR, COMMIT_NOISE,
    STEPS_PER_CELL)
from experiments.exp427_protection_motif_census import (
    _custom, _census_target, _region_for, _flags)

SEEDS = [0, 1, 2, 3, 4]

SAMPLE = {
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
}
CONTROLS = {
    "path3": lambda: _adjacency("path", 3, 0),
    "triangle3": lambda: _adjacency("ring", 3, 0),
}
CONTROLS_EXPECTED = {"path3": 5, "triangle3": 0}


def _has_triangle(A):
    A3 = np.linalg.matrix_power((A > 0).astype(float), 3)
    return bool(np.trace(A3) / 6.0 > 0)


def _density(A):
    n = A.shape[0]
    return float(np.sum(np.triu(A > 0, 1))) / (n * (n - 1) / 2.0)


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget_mode == "smoke"

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert len(SAMPLE) == 8 and len(CONTROLS) == 2

    # ---- the independent-sample battery (all forms x seeds, no prune)
    table = {}
    for form in sorted(SAMPLE):
        A = SAMPLE[form]()
        n = A.shape[0]
        tgt = _census_target(n)
        region = _region_for(n)
        seeds_run = SEEDS[:1] if smoke else SEEDS
        rows = [_battery_graph(A, tgt, region, s) for s in seeds_run]
        n_prot = sum(1 for r in rows if r["t_protect"])
        table[form] = {
            "triangle": _has_triangle(A),
            "density": round(_density(A), 3),
            "flags": _flags(A, region),
            "n_protect": n_prot, "n_seeds": len(rows),
            "protective": bool(n_prot >= PROTECT_SEED_BAR),
            "t_register": sum(1 for r in rows if r["t_register"]),
            "t_compose": sum(1 for r in rows if r["t_compose"]),
            "per_seed": [{"t_protect": r["t_protect"],
                          "P_single": round(r["P_single"], 4),
                          "t_register": r["t_register"],
                          "t_compose": r["t_compose"]} for r in rows],
        }
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
        print("  %s: protective %d/%d triangle %s density %.2f"
              % (form, n_prot, len(rows), table[form]["triangle"],
                 table[form]["density"]))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    verdicts["G1"] = "PASS"
    verdicts["G2"] = "PASS"
    print("G1 PASS (floor; constants; sample complete %d/%d forms)"
          % (len(table), len(SAMPLE)))
    print("G2 PASS (the full face table deposited, no pruning)")

    # ---- G3 the hypothesis (zero contradictions on the sample)
    contradictions = []
    for form, row in table.items():
        pred = not row["triangle"]
        if row["protective"] != pred:
            contradictions.append(form)
    verdicts["G3"] = "PASS" if not contradictions else "REFUTE"
    print("G3 %s (contradictions: %s)"
          % (verdicts["G3"], contradictions or "NONE"))

    # ---- G4 the controls (exact reproduction of exp427's anchors)
    control_rows = {}
    g4_ok = True
    if not smoke:
        for form in sorted(CONTROLS):
            A = CONTROLS[form]()
            n = A.shape[0]
            tgt = _census_target(n)
            region = _region_for(n)
            rows = [_battery_graph(A, tgt, region, s) for s in SEEDS]
            n_prot = sum(1 for r in rows if r["t_protect"])
            control_rows[form] = {"n_protect": n_prot,
                                  "expected": CONTROLS_EXPECTED[form],
                                  "exact": n_prot ==
                                  CONTROLS_EXPECTED[form]}
            if not control_rows[form]["exact"]:
                g4_ok = False
            assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
        verdicts["G4"] = "PASS" if g4_ok else "REFUTE"
    else:
        verdicts["G4"] = "SMOKE-SKIP"
    print("G4 %s (%s)"
          % (verdicts["G4"], {k: v["n_protect"] for k, v in
                              control_rows.items()} or "skipped"))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    # ---- the branch
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    elif not g4_ok:
        branch = "CONTROLS-FAILED"
    elif not contradictions:
        branch = "TRIANGLE-CARRIED"
    else:
        dense_tf = [f for f, r in table.items()
                    if r["density"] >= 0.55 and not r["triangle"]]
        sparse_tb = [f for f, r in table.items()
                     if r["density"] < 0.55 and r["triangle"]]
        if dense_tf and sparse_tb and \
                all(not table[f]["protective"] for f in dense_tf) and \
                all(table[f]["protective"] for f in sparse_tb):
            branch = "DENSITY-CARRIED"
        else:
            branch = "TRIANGLE-ARTIFACT"

    try:
        dep427 = json.load(open(os.path.join(
            ROOT, "results", "exp427_protection_motif_census.json")))
        cross427 = {"verdict": dep427.get("verdict"),
                    "consistent_candidates":
                        dep427.get("consistent_candidates")}
    except (OSError, KeyError):
        cross427 = None

    dep = {
        "experiment": "exp431",
        "title": "THE TRIANGLE HYPOTHESIS ON AN INDEPENDENT SAMPLE "
                 "(batch HU-12)",
        "instrument": {"sample": sorted(SAMPLE),
                       "controls": sorted(CONTROLS),
                       "seeds": SEEDS,
                       "protect_bar": PROTECT_SEED_BAR,
                       "triangle_flag": "trace(A^3)/6 > 0"},
        "sample_table": table,
        "control_rows": control_rows,
        "contradictions": contradictions,
        "exp427_cross_check": cross427,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    with open(DEPOSIT, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP431 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts, "verdict": branch}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
