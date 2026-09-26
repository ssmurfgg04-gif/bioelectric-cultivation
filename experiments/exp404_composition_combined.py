#!/usr/bin/env python3
"""exp404 — THE COMPOSED CARRIER ↔ THE COMBINED-INTERVENTION
LITERATURE (batch HU-4; ledger L298; charter docs/HUMAN_EXTENSION.md).
exp403 landed HISTORY-PROTECTS-HUMAN: the register protects on the real
human connectome. THE OPEN QUESTION (handoff Section 7): is the
COMPOSITION LAW the same on the human side — when two intervention
carriers are applied together, is the effect additive, super-additive,
or sub-additive? THE MODEL PREDICTS (exp299, on the planarian
substrate, under stress): SUPER-ADDITIVE. THE HUMAN LITERATURE: Celnik
et al. 2009 measured ALL FOUR CELLS of the composition factorial in
humans (post-stroke motor training): PNS+tDCS +41.3% over double sham;
+15.4% over PNS+tDCS(sham) -> E_PNS = 25.9%; +22.7% over
PNS(sham)+tDCS -> E_tDCS = 18.6%. THE ADDITIVE PREDICTION = 44.5;
THE EXCESS = 41.3 − 44.5 = −3.2; THE EXCESS FRACTION = −0.072
(slightly sub-additive, i.e. APPROXIMATELY ADDITIVE).

THE MODEL INSTRUMENT (exp403's landed stressed walk + TWO carrier
arms, on the human graph, self-contained):
  base  the stressed walk (the wound + the −35.0 pin walk), neither
        carrier;
  A     + the history register blend at the boundary (g_ctx 0.5,
        exp403's landed arm);
  B     + the gap-junction reinforcement: gap_scale 1.25 DURING the
        walk (the read strengthening; the +25% pre-named, disclosed as
        fixed a priori), restored 1.0 after;
  AB    both composed.
  P_comp = (e_base − e_AB) − (e_base − e_A) − (e_base − e_B)
  (the composition interaction, mean over 5 seeds; improvement
  > 0 = error reduced).
  THE CLASS RULE (pre-named, symmetric on both sides): with
  impA = e_base − e_A, impB = e_base − e_B: if (impA + impB) <= 0 the
  class is UNDEFINED (disclosed branch); else the excess fraction
  f = P_comp / (impA + impB): SUPER if f > +0.10, SUB if f < −0.10,
  else ADDITIVE.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the exp401 adjacency rebuild reproduces the exp401
      deposit's density (1e-12); the floor −60.0 at entry/exit and
      every settle; the constants pre-named (G_CTX 0.5, the gap
      reinforcement 1.25, COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      wound −30.0, the stress pin −35.0) and asserted at run
      (fail=STOP).
  G2  THE 4-CELL INTEGRITY: 4 cells x 5 seeds, every err finite; the
      stressed base is the exp403 H0-S1 instrument re-run (its mean
      within 0.25 mV of exp403's deposited 8.3819 — the cross-experiment
      anchor face); the floors logged and asserted.
  G3  THE MODEL COMPOSITION MEASURED: impA, impB, P_comp, f_model and
      class_model computed and finite (the UNDEFINED branch allowed,
      disclosed); class_model deposited.
  G4  THE LITERATURE COMPARISON (the gate): Celnik 2009's arithmetic
      encoded verbatim (41.3, 25.9, 18.6, 44.5, −3.2, −0.072) ->
      class_lit = ADDITIVE (|−0.072| <= 0.10); the gate: class_model
      == class_lit -> COMPOSITION-CLASS-MATCH (the composition law
      transfers in class); else -> COMPOSITION-DIVERGES (the law is
      regime- or substrate-specific — a valid closure outcome,
      Outcome B/C territory, and the DIVERGENCE ITSELF is the
      finding).
  G5  THE DEPOSIT: the 4-cell errs per seed, impA/impB/P_comp/
      f_model, class_model, the Celnik table with sources, the gates
      and the branch deposited as
      results/exp404_composition_combined.json (fail=STOP).

THE HONEST LIMITS (in the deposit): the model's "carriers" are
register/gap-junction couplings, not tDCS/PNS; the class rule's ±0.10
band is a pre-named convention, not a law of nature; the literature
cell is ONE published 4-cell factorial (small-n, one task), not a
meta-analysis — the claim tested is the CLASS, disclosed.
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective
from human.substrate import build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp404_composition_combined.json")
SEEDS = [0, 1, 2, 3, 4]
G_CTX = 0.5
GAP_REINFORCE = 1.25
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
WOUND_V = -30.0
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
DT = 0.1

CELNIK = {
    "combined_pct": 41.3, "pns_single_pct": 25.9, "tdcs_single_pct": 18.6,
    "additive_prediction_pct": 44.5, "excess_pct": -3.2,
    "excess_fraction": -3.2 / 44.5, "class": "ADDITIVE",
    "source": "Celnik et al. 2009, the published 4-cell composition "
              "factorial (post-stroke motor training, humans): 41.3% over "
              "double sham; 15.4% over PNS+sham -> E_PNS 25.9; 22.7% over "
              "sham+PNS -> E_tDCS 18.6",
}


def _walk(h, target, region, g_ctx, gap, stress, floor_log):
    region_set = set(region)
    cls = np.zeros(h.n, dtype=int)
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        cls[i] = 0 if nbrs else 1
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(h.theta[j] - WOUND_V)))
            frontier.append(i)
    if not frontier:
        frontier = list(region)[:1]
        parent_of[frontier[0]] = frontier[0]
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(h.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    if stress:
        CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
        floor_log.append(("walk_entry", float(CORE.NEURAL_SPEC_MIN)))
    if gap:
        h.gap_scale = GAP_REINFORCE
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            h.step(DT)
        if h.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
            theta_new = h.phi_spec[i] + h.rng.normal(0.0, COMMIT_NOISE)
        else:
            theta_new = h.theta[src] + h.rng.normal(0.0, COMMIT_NOISE)
        written = theta_new
        if g_ctx > 0.0 and cls[i] == 0:
            written = ((1.0 - g_ctx) * theta_new
                       + g_ctx * float(h.phi_history[i]))
        h.theta[i] = written
        h.V[i] = written
        h.phi_history[i] = written
    if gap:
        h.gap_scale = 1.0
    if stress:
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
        floor_log.append(("walk_exit", float(CORE.NEURAL_SPEC_MIN)))
    h.run(30.0, dt=DT)
    return float(h.pattern_error(target))


def main() -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    floor_log: list = []

    # ---- G1 the anchors
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    dep401 = json.load(open(os.path.join(ROOT, "results",
                                         "exp401_human_substrate.json")))
    assert abs(float(dep401["preprocessing"]["density"])
               - float((W > 0).mean())) < 1e-12
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])
    assert len(region) == 80
    assert (G_CTX, GAP_REINFORCE, COMMIT_NOISE, STEPS_PER_CELL,
            WOUND_V, STRESS_FLOOR) == (0.5, 1.25, 0.6, 8, -30.0, -35.0)
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: density %.4f, floor %s)"
          % (float((W > 0).mean()), CORE.NEURAL_SPEC_MIN))

    # ---- G2 the 4-cell integrity (base = the exp403 H0-S1 re-run)
    errs = {k: [] for k in ["base", "A", "B", "AB"]}
    for seed in SEEDS:
        for key, g, gap in [("base", 0.0, False), ("A", G_CTX, False),
                            ("B", 0.0, True), ("AB", G_CTX, True)]:
            h = GraphCollective(adjacency=W, seed=seed)
            h.set_target(tgt)
            h.run(30.0, dt=DT)
            h.phi_spec = tgt.copy()
            h.phi_history = tgt.copy()
            h.theta[region] = WOUND_V
            h.V[region] = WOUND_V
            e = _walk(h, tgt, region, g, gap, True, floor_log)
            assert np.isfinite(e)
            errs[key].append(e)
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    base_mean = float(np.mean(errs["base"]))
    assert abs(base_mean - 8.3819) < 0.25, (base_mean, 8.3819)
    verdicts["G2"] = "PASS"
    detail["errs"] = errs
    print("G2 PASS (base %.4f vs exp403's 8.3819; A %.4f B %.4f AB %.4f)"
          % (base_mean, np.mean(errs["A"]), np.mean(errs["B"]),
             np.mean(errs["AB"])))

    # ---- G3 the model composition measured
    impA = base_mean - float(np.mean(errs["A"]))
    impB = base_mean - float(np.mean(errs["B"]))
    impAB = base_mean - float(np.mean(errs["AB"]))
    P_comp = impAB - impA - impB
    detail.update({"impA": impA, "impB": impB, "impAB": impAB,
                   "P_comp": P_comp})
    if impA + impB <= 0:
        f_model, class_model = None, "UNDEFINED"
    else:
        f_model = P_comp / (impA + impB)
        class_model = ("SUPER" if f_model > 0.10
                       else "SUB" if f_model < -0.10 else "ADDITIVE")
    detail.update({"f_model": f_model, "class_model": class_model})
    assert class_model in ("SUPER", "SUB", "ADDITIVE", "UNDEFINED")
    verdicts["G3"] = "PASS"
    print("G3 PASS (impA %.4f impB %.4f P_comp %.4f f_model %s -> %s)"
          % (impA, impB, P_comp,
             "NA" if f_model is None else "%.4f" % f_model, class_model))

    # ---- G4 the literature comparison (the gate)
    assert abs(CELNIK["additive_prediction_pct"]
               - (CELNIK["pns_single_pct"] + CELNIK["tdcs_single_pct"])) < 1e-9
    class_lit = CELNIK["class"]
    verdicts["G4"] = "PASS"
    match = class_model == class_lit
    branch = "COMPOSITION-CLASS-MATCH" if match else "COMPOSITION-DIVERGES"
    print("G4 PASS (class_model %s vs class_lit %s -> %s)"
          % (class_model, class_lit, branch))

    # ---- G5 the deposit
    dep = {
        "experiment": "exp404",
        "title": "THE COMPOSED CARRIER <-> THE COMBINED-INTERVENTION "
                 "LITERATURE (batch HU-4)",
        "instrument": {"base": "the exp403 H0-S1 stressed walk re-run",
                       "A": "the register blend g_ctx 0.5 (exp403's arm)",
                       "B": "the gap-junction reinforcement gap_scale 1.25 during the walk (pre-named, disclosed)",
                       "AB": "both composed",
                       "constants": {"G_CTX": G_CTX, "GAP_REINFORCE": GAP_REINFORCE,
                                     "COMMIT_NOISE": COMMIT_NOISE,
                                     "STEPS_PER_CELL": STEPS_PER_CELL,
                                     "WOUND_V": WOUND_V,
                                     "STRESS_FLOOR": STRESS_FLOOR}},
        "errs_per_seed": errs,
        "composition": detail,
        "class_rule": "f = P_comp/(impA+impB); SUPER > +0.10, SUB < -0.10, else ADDITIVE; UNDEFINED if impA+impB <= 0",
        "literature": CELNIK,
        "gates": verdicts,
        "branch": branch,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP404 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts, "branch": branch}


if __name__ == "__main__":
    main()
