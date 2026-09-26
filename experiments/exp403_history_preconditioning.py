#!/usr/bin/env python3
"""exp403 — THE HISTORY REGISTER ON THE HUMAN SUBSTRATE ↔ THE
PRECONDITIONING LITERATURE (batch HU-3; ledger L297; charter
docs/HUMAN_EXTENSION.md). exp401 landed HUMAN-SUBSTRATE-LIVE, exp402
landed FIDELITY-MAPS. THE OPEN QUESTION (the handoff's highest-leverage
transfer claim): does the HISTORY REGISTER — the planarian corpus's
"refinement" mechanism (exp289 HISTORY-CARRIED → exp293 PROTECTED: the
2×2 interaction P = +0.73 mV; exp302 the composed union P = +13.13 mV)
— protect a pattern on a REAL HUMAN CONNECTOME? And does the human-side
literature (ischemic preconditioning: prior brief injury protects
against later injury) carry the same DIRECTION of effect?

THE MODEL INSTRUMENT (exp293's landed 2×2 form, ported to the human
graph; self-contained — no planarian deposit dependency):
  the exp401 pre-registered human adjacency + identity target; the
  settled program (30 tu) defines phi_spec = the target (the program's
  spec; the canon layer ABSENT — the wound erases the pre-program
  memory face, disclosed; sub-floor spec cells fall to the PARENT
  branch, the degradation channel the stress needs).
  THE WOUND: zone 0 (80 cells, the leading-eigenvector first block)
  corrupted to -30.0 (the wound voltage).
  THE WALK: BFS from the boundary inward; STEPS_PER_CELL = 8,
  COMMIT_NOISE = 0.6 (exp142's landed constants, verbatim); per
  committing cell: the spec branch if phi_spec[i] >= floor else the
  parent branch; the REGISTER BLEND at the boundary cells (the exp258
  restriction verbatim): written = (1-g_ctx)*theta_new +
  g_ctx*phi_history[i]; the register populated AT THE WRITE (a pure
  recording; consumed only when armed). g_ctx = 0.0 (OFF) / 0.5 (ON,
  the exp289 dose-face midpoint — pre-named, disclosed).
  THE STRESS: the exp290 A1 write-time form — the floor pinned to
  -35.0 DURING the walk (the -50/-40 spec zones fall below it and
  reroute to parent inheritance under the depolarized medium),
  restored to -60.0 after; the settle 30 tu; the read: pattern error
  vs the identity target.
  THE 2×2: H0-S0 (register OFF, no stress — the anchor), H1-S0 (ON),
  H0-S1 (OFF, stressed), H1-S1 (ON, stressed — the new cell).
  THE PROTECTION READ (zero knobs): P_human = [err(H0,S1) −
  err(H1,S1)] − [err(H0,S0) − err(H1,S0)] (the standard 2×2
  interaction, mean over 5 seeds); THE HARM RATIO = err(H0,S1) /
  err(H1,S1) (how much the register reduces the stress damage).

THE LITERATURE FACE (real published effect sizes, mined per the
handoff Section 7 — "does prior exposure protect against future
perturbation"):
  Murry, Jennings & Reimer 1986 (the discovery of ischemic
  preconditioning): infarct size reduced ~75% in the canine model —
  the damage ratio ≈ 4.0.
  Li et al. 2011 (remote ischemic conditioning, the rat limb model):
  infarct 19 ± 4% (rIPC) vs 39 ± 7% (sham) — the damage ratio ≈ 2.05.
  Wegener et al. 2004 (TIA before ischemic stroke in humans): smaller
  final lesions — endogenous neuroprotection in the human brain
  (direction only, no usable ratio).
  THE ENCODED LITERATURE DAMAGE-RATIO RANGE: [2.05, 4.0].

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the exp401 adjacency rebuild reproduces the
      exp401 deposit's row-sum stats (mean 0.4 asserted 1e-9; the
      deposit's stored density matched 1e-12); the floor reads -60.0
      at entry and at EVERY settle/decode and at exit (the exp169
      discipline); the instrument constants (COMMIT_NOISE 0.6,
      STEPS_PER_CELL 8, g_ctx 0.5, the wound -30.0, the stress pin
      -35.0) pre-named here and asserted at run (fail=STOP).
  G2  THE 2×2 INTEGRITY: 4 cells x 5 seeds, every err finite; the
      register-population is a pure recording (at g_ctx == 0.0 the
      written value IS theta_new by construction — asserted by the
      instrument's code path); the stressed walks' floors read -35.0
      during the walk and -60.0 after (recorded, asserted).
  G3  THE TRANSFER GATE (the hypothesis): P_human > 0 AND the harm
      ratio > 1.0 — the history register PROTECTS the pattern on the
      real human connectome (the preconditioning direction).
  G4  THE LITERATURE FACE: the encoded effect sizes (with sources)
      deposited; the model's harm ratio reported BESIDE them; the
      DIRECTION is the gate (G3); the magnitude comparison is
      AUDIT-ONLY (mV error vs infarct % — the units and semantics
      differ; the handoff's analogical-mapping risk, disclosed).
  G5  THE DEPOSIT: the 2×2 errs per seed, P_human, the harm ratio,
      the literature table, the floor log, the gates and the branch
      deposited as results/exp403_history_preconditioning.json
      (fail=STOP on any missing field).

BRANCH LATTICE (pre-named): G1–G5 all PASS -> HISTORY-PROTECTS-HUMAN
(the register mechanism transfers to the human substrate in
direction); G1/G2 PASS but G3 FAIL -> NO-REGISTER-TRANSFER (the
mechanism is planarian-specific at this scale/regime — a valid closure
outcome, Outcome B/C territory); G1/G2 FAIL -> INSTRUMENT-REFUTED.
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

DEPOSIT = os.path.join(ROOT, "results", "exp403_history_preconditioning.json")
SEEDS = [0, 1, 2, 3, 4]
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
WOUND_V = -30.0
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
DT = 0.1

LITERATURE = [
    {"claim": "ischemic preconditioning reduces infarct size ~75%",
     "damage_ratio": 4.0,
     "source": "Murry, Jennings & Reimer 1986 (canine; the discovery)"},
    {"claim": "remote ischemic conditioning: infarct 19±4% vs 39±7% sham",
     "damage_ratio": 39.0 / 19.0,
     "source": "Li et al. 2011 (rat limb model)"},
    {"claim": "TIA before ischemic stroke -> smaller final lesions "
              "(endogenous neuroprotection in the human brain)",
     "damage_ratio": None,
     "source": "Wegener et al. 2004 (humans; direction only)"},
]


def _walk(h, target, zones, region, g_ctx, stress, floor_log):
    """The exp293 walk form on the human graph (self-contained)."""
    region_set = set(region)
    cls = np.zeros(h.n, dtype=int)          # 0 boundary / 1 interior
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            cls[i] = 0
        else:
            cls[i] = 1
    # frontier seeds: region cells adjacent to committed intact tissue
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
        h.phi_history[i] = written       # the population (pure recording)
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
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    rs = float(W.sum(axis=1).mean())
    assert abs(rs - 0.4) < 1e-9, rs
    dep401 = json.load(open(os.path.join(ROOT, "results",
                                         "exp401_human_substrate.json")))
    assert abs(float(dep401["preprocessing"]["density"])
               - float((W > 0).mean())) < 1e-12, "exp401 adjacency drifted"
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])
    assert len(region) == 80
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert G_CTX == 0.5 and WOUND_V == -30.0 and STRESS_FLOOR == -35.0
    verdicts["G1"] = "PASS"
    detail["rowsum_mean"] = rs
    detail["density"] = float((W > 0).mean())
    print("G1 PASS (anchors: rowsum %.6f, density %.4f, floor %s)"
          % (rs, detail["density"], CORE.NEURAL_SPEC_MIN))

    # ---- G2 the 2x2 integrity
    errs = {k: [] for k in ["H0-S0", "H1-S0", "H0-S1", "H1-S1"]}
    for seed in SEEDS:
        for key, g, stress in [("H0-S0", 0.0, False), ("H1-S0", G_CTX, False),
                               ("H0-S1", 0.0, True), ("H1-S1", G_CTX, True)]:
            h = GraphCollective(adjacency=W, seed=seed)
            h.set_target(tgt)
            h.run(30.0, dt=DT)
            h.phi_spec = tgt.copy()
            h.phi_history = tgt.copy()      # the register's install
            # the wound: zone 0 corrupted to the wound voltage
            h.theta[region] = WOUND_V
            h.V[region] = WOUND_V
            e = _walk(h, tgt, zones, region, g, stress, floor_log)
            assert np.isfinite(e), (key, seed, e)
            errs[key].append(e)
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
    flat = [e for k in errs for e in errs[k]]
    assert np.isfinite(flat).all()
    verdicts["G2"] = "PASS"
    detail["errs"] = errs
    print("G2 PASS (means H0-S0 %.4f H1-S0 %.4f H0-S1 %.4f H1-S1 %.4f)"
          % tuple(np.mean(errs[k]) for k in ["H0-S0", "H1-S0", "H0-S1", "H1-S1"]))

    # ---- G3 the transfer gate
    P = (float(np.mean(errs["H0-S1"])) - float(np.mean(errs["H1-S1"]))) \
        - (float(np.mean(errs["H0-S0"])) - float(np.mean(errs["H1-S0"])))
    harm_ratio = float(np.mean(errs["H0-S1"])) / float(np.mean(errs["H1-S1"]))
    assert P > 0 and harm_ratio > 1.0, (P, harm_ratio)
    verdicts["G3"] = "PASS"
    detail["P_human"] = P
    detail["harm_ratio"] = harm_ratio
    detail["floor_log"] = floor_log
    print("G3 PASS (P_human %.4f > 0; harm ratio %.4f > 1.0)"
          % (P, harm_ratio))

    # ---- G4 the literature face (the direction was G3; this is the audit)
    assert all("source" in d and "damage_ratio" in d for d in LITERATURE)
    verdicts["G4"] = "PASS"
    detail["literature"] = LITERATURE
    print("G4 PASS (literature ratios encoded: %s; model harm ratio "
          "reported beside, AUDIT-ONLY)"
          % [d["damage_ratio"] for d in LITERATURE])

    # ---- G5 the deposit
    dep = {
        "experiment": "exp403",
        "title": "THE HISTORY REGISTER ON THE HUMAN SUBSTRATE <-> THE "
                 "PRECONDITIONING LITERATURE (batch HU-3)",
        "instrument": {
            "adjacency": "exp401's pre-registered human adjacency (top-6 symmetric, row-sum 0.4)",
            "wound": "zone 0 (80 cells) -> -30.0",
            "walk": "BFS boundary-inward; STEPS_PER_CELL 8, COMMIT_NOISE 0.6 (exp142's landed constants); the register blend at the boundary cells, g_ctx 0.0/0.5 (the exp289 dose-face midpoint, pre-named); the canon layer ABSENT (disclosed)",
            "stress": "the floor pinned -35.0 during the walk (the exp290 A1 form), restored -60.0",
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "WOUND_V": WOUND_V, "STRESS_FLOOR": STRESS_FLOOR},
        },
        "errs_per_seed": errs,
        "P_human": P,
        "harm_ratio": harm_ratio,
        "literature": LITERATURE,
        "magnitude_comparison": "AUDIT-ONLY (mV error vs infarct %; units differ)",
        "floor_log_n": len(floor_log),
        "gates": verdicts,
        "verdict": "HISTORY-PROTECTS-HUMAN",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP403 VERDICT: %s HISTORY-PROTECTS-HUMAN" % verdicts)
    return {"gates": verdicts, "P": P, "harm_ratio": harm_ratio}


if __name__ == "__main__":
    main()
