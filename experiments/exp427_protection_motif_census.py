#!/usr/bin/env python3
"""exp427 — WHAT WIRING CARRIES THE PROTECTION? THE MOTIF CENSUS
(batch HU-12; exp424's registered follow-up). exp424 corrected exp418:
protection holds at n=3 on protective graphs — the floor is
WIRING-DEPENDENT, not a universal count. The open question is the
shape of that dependence: WHICH wiring feature separates protective
graphs from non-protective ones at small n? Four pre-named candidates,
fixed before the census runs:
  (a) CYCLE      — the graph contains a cycle (cycle rank >= 1);
  (b) DEGREE     — min degree >= 2 (every cell has a second neighbor);
  (c) HUB        — max degree >= 3 (a concentration point exists);
  (d) TWOKCHANNEL— the exp418 two-channel motif structure (a ctx face
                   AND a gj face both present).

THE INSTRUMENT (exp418's battery verbatim at the census scale; zero
new knobs):
  the census forms — every connected simple graph on 3 nodes (path3,
  triangle3) and on 4 nodes (path4, star4, ring4, complete4, paw4,
  diamond4) + the exp418 two-channel motif (motif4): 9 forms total,
  binary unweighted (the census question is WIRING; exp424's
  precedent), each form's adjacency built by the corpus's own
  constructors.
  THE BATTERY per (form, seed): the settled program defines phi_spec
  (the house-ladder zones, exp418's scaled semantics); the wound +
  walk (STEPS_PER_CELL 8, COMMIT_NOISE 0.6); the register blend
  g_ctx in {0, 0.5}; stress {off, on} (the write-time -35.0 pin,
  restored -60.0); 5 seeds per form.
  FACES per (form, seed): T-REGISTER, T-PROTECT (the 2x2 interaction
  P), T-COMPOSE — exp418's definitions verbatim.
  A form is PROTECTIVE iff T-PROTECT holds on >= 3/5 seeds.
  The holdout probes (ring5, path5) are built and held aside; their
  battery runs ONLY after the carrier verdict is fixed from the
  census (the pre-named prediction test).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the census count asserted (9 forms, no
      pruning); every form's face table complete (fail=STOP).
  G2  THE FULL TABLE: face status per (form, seed) x all three faces
      deposited — no pruning, including the forms that fail
      everywhere.
  G3  THE CARRIER: a candidate is CONSISTENT iff every protective
      form has it AND every non-protective form lacks it (zero
      contradictions across the 9-form census). THE GATE: exactly
      one candidate is consistent.
  G4  THE HOLDOUT: the winning candidate predicts T-PROTECT on
      ring5 (has-cycle) and path5 (no-cycle) — both predictions
      correct (fail of either = REFUTE, deposited honestly).
  G5  deposit results/exp427_protection_motif_census.json.

BRANCH LATTICE: CYCLE-CARRIED / DEGREE-CARRIED / HUB-CARRIED /
MOTIF-CARRIED (the consistent winner) / MULTI-CARRIER (>= 2
consistent — the protection is over-determined) / NO-CARRIER (none —
the protection is not a single-feature property at this scale) /
INSTRUMENT-REFUTED (G1 fail).

THE HONEST STAKES: exp424's correction made the minimal substrate a
WIRING question; the census either names the feature (the S_min
curve becomes predictive — "protection = f(wiring), computable
before the battery runs") or honestly dissolves the single-feature
hypothesis.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_CTX_GRID = [0.0, 0.5]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2, 3, 4]
CENSUS_FORMS = ["path3", "triangle3", "path4", "star4", "ring4",
                "complete4", "paw4", "diamond4", "motif4"]
HOLDOUT_FORMS = ["ring5", "path5"]
PROTECT_SEED_BAR = 3
DEPOSIT = os.path.join(ROOT, "results",
                       "exp427_protection_motif_census.json")


BODY_DISCLOSURES = [
    "the battery is exp418's landed machinery imported verbatim "
    "(_battery_graph, _target, _adjacency for the path/ring/star/motif "
    "forms); the census constructors (triangle3, complete4, paw4, "
    "diamond4) are the corpus's own adjacency style, deterministic, "
    "zero new knobs",
    "the region rule is exp418's own (_battery: per = max(1, n//4) if "
    "n >= 8 else max(1, n//2)) — the face semantics are the battery's, "
    "not redefined",
    "the candidate flags are computed from the BUILT adjacency + region: "
    "cycle = cycle rank > 0 (E - V + components); degree = the graph's "
    "min/max degree; TWOKCHANNEL = the battery's own two faces present "
    "(an internal region edge AND a boundary cell) — the operational "
    "form of 'a ctx face AND a gj face both present'",
    "G4's holdout runs ONLY when exactly one candidate is consistent; "
    "with NONE or >= 2 consistent, G4 deposits VACUOUS with the reason "
    "(nothing was predicted; the branch lattice carries the verdict)",
    "exp424's landed census (NO-SINGLE-CARRIER at the (form, wound)-cell "
    "granularity, bridge/cut/cycle candidates) is deposited beside this "
    "run as the cross-experiment continuity field; this census's "
    "granularity is the FORM (exp418's region rule fixes the wound), "
    "its candidate set adds min-degree, hub, and the two-channel face "
    "pair",
    "the target ladder extended to n=3 body-side: exp418's _target jumps "
    "from n=2 to n=4 (its ladder never ran n=3); the census uses the "
    "n>=5 rule's own formula at n=3 (t[:n//2] = -50, rest = -30 — one "
    "low cell, two high), disclosed; no gate touches the target ladder",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from experiments.exp418_minimal_substrate import (
    _battery_graph, _target, _adjacency, PROD_FLOOR, COMMIT_NOISE,
    STEPS_PER_CELL)


def _complete(n):
    A = np.ones((n, n)) - np.eye(n)
    return A


def _custom(edges, n):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    return A


CENSUS = {
    "path3": lambda: _adjacency("path", 3, 0),
    "triangle3": lambda: _adjacency("ring", 3, 0),
    "path4": lambda: _adjacency("path", 4, 0),
    "star4": lambda: _adjacency("star", 4, 0),
    "ring4": lambda: _adjacency("ring", 4, 0),
    "complete4": lambda: _complete(4),
    "paw4": lambda: _custom([(0, 1), (1, 2), (0, 2), (0, 3)], 4),
    "diamond4": lambda: _custom([(0, 1), (0, 2), (0, 3), (1, 2),
                                 (1, 3)], 4),
    "motif4": lambda: _adjacency("motif", 4, 0),
}
HOLDOUT = {
    "ring5": lambda: _adjacency("ring", 5, 0),
    "path5": lambda: _adjacency("path", 5, 0),
}


def _region_for(n):
    per = max(1, n // 4) if n >= 8 else max(1, n // 2)
    return list(range(0, min(per, n)))


def _census_target(n):
    if n == 3:
        t = np.empty(3)
        t[:1] = -50.0
        t[1:] = -30.0
        return t
    return _target(n)


def _flags(A, region):
    n = A.shape[0]
    E = int(np.sum(np.triu(A > 0, 1)))
    deg = (np.abs(A) > 0).sum(axis=1)
    # components via BFS
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
    cycle = (E - n + comps) > 0
    # the battery's own faces: an internal region edge + a boundary cell
    rset = set(region)
    internal_edge = any(A[i, j] > 0 for i in region for j in region
                        if i < j)
    boundary = any(any(j not in rset for j in np.where(A[i] > 0)[0])
                   for i in region)
    return {"m_cycle": bool(cycle), "m_mindeg2": bool(deg.min() >= 2),
            "m_hub3": bool(deg.max() >= 3),
            "m_twochannel": bool(internal_edge and boundary),
            "n_edges": E, "min_deg": int(deg.min()),
            "max_deg": int(deg.max())}


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget_mode == "smoke"

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert len(CENSUS_FORMS) == 9 and len(HOLDOUT_FORMS) == 2
    assert sorted(CENSUS_FORMS) == sorted(CENSUS)

    # ---- the census battery (all forms x seeds, no pruning)
    table = {}
    for form in CENSUS_FORMS:
        A = CENSUS[form]()
        n = A.shape[0]
        tgt = _census_target(n)
        region = _region_for(n)
        seeds_run = SEEDS[:1] if smoke else SEEDS
        rows = [_battery_graph(A, tgt, region, s) for s in seeds_run]
        n_prot = sum(1 for r in rows if r["t_protect"])
        table[form] = {
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
        print("  %s: protective %d/%d flags %s"
              % (form, n_prot, len(rows),
                 {k: v for k, v in table[form]["flags"].items()
                  if k.startswith("m_")}))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    verdicts["G1"] = "PASS"
    verdicts["G2"] = "PASS"
    print("G1 PASS (floor; constants; census complete %d/%d forms)"
          % (len(table), len(CENSUS_FORMS)))
    print("G2 PASS (the full face table deposited, no pruning)")

    # ---- G3 the carrier (zero contradictions across the census)
    consistent = []
    for cand in ("m_cycle", "m_mindeg2", "m_hub3", "m_twochannel"):
        ok = all(table[f]["protective"] == bool(table[f]["flags"][cand])
                 for f in CENSUS_FORMS)
        if ok:
            consistent.append(cand)
    verdicts["G3"] = "PASS" if len(consistent) == 1 else "REFUTE"
    print("G3 %s (consistent candidates: %s)"
          % (verdicts["G3"], consistent or "NONE"))

    # ---- G4 the holdout (only with exactly one consistent candidate)
    g4 = "VACUOUS"
    holdout_rows = {}
    if len(consistent) == 1 and not smoke:
        winner = consistent[0]
        preds = {}
        for form in HOLDOUT_FORMS:
            A = HOLDOUT[form]()
            n = A.shape[0]
            tgt = _census_target(n)
            region = _region_for(n)
            rows = [_battery_graph(A, tgt, region, s) for s in SEEDS]
            n_prot = sum(1 for r in rows if r["t_protect"])
            prot = n_prot >= PROTECT_SEED_BAR
            fl = _flags(A, region)
            preds[form] = {"predicted": bool(fl[winner]),
                           "measured": prot, "correct": prot == bool(fl[winner])}
            holdout_rows[form] = {"flags": fl,
                                  "n_protect": n_prot,
                                  "protective": prot}
        g4 = "PASS" if all(p["correct"] for p in preds.values()) \
            else "REFUTE"
        detail["holdout_predictions"] = preds
    elif smoke:
        g4 = "SMOKE-SKIP"
    else:
        g4 = ("VACUOUS-NO-CARRIER" if not consistent
              else "VACUOUS-MULTI-CARRIER")
    verdicts["G4"] = g4
    print("G4 %s" % g4)

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    if len(consistent) == 1:
        branch = {"m_cycle": "CYCLE-CARRIED",
                  "m_mindeg2": "DEGREE-CARRIED",
                  "m_hub3": "HUB-CARRIED",
                  "m_twochannel": "MOTIF-CARRIED"}[consistent[0]]
    elif len(consistent) >= 2:
        branch = "MULTI-CARRIER"
    else:
        branch = "NO-CARRIER"
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"

    try:
        dep424 = json.load(open(os.path.join(
            ROOT, "results", "exp424_protective_motif_n4.json")))
        cross424 = {"verdict": dep424.get("verdict"),
                    "gates": dep424.get("gates"),
                    "census_size": dep424.get("census_size")}
    except (OSError, KeyError):
        cross424 = None

    dep = {
        "experiment": "exp427",
        "title": "WHAT WIRING CARRIES THE PROTECTION? THE MOTIF CENSUS "
                 "(batch HU-12)",
        "instrument": {"forms": CENSUS_FORMS, "holdout": HOLDOUT_FORMS,
                       "seeds": SEEDS,
                       "candidates": ["m_cycle", "m_mindeg2", "m_hub3",
                                      "m_twochannel"]},
        "census_table": table,
        "holdout": holdout_rows,
        "consistent_candidates": consistent,
        "exp424_cross_check": cross424,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP427 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
