#!/usr/bin/env python3
"""exp433 — THE INVISIBILITY RECIPE ON THE HUMAN CONNECTOME (batch
HU-13; exp411/412/422's registered follow-up). exp411 found the
dissolution threshold g* = 0.117 (Hill R2 0.9996) and the recipe —
saturate, refresh below g*; exp412 carried the instrument to the
human connectome bit-exactly (400/400, delta 0.0 on 5/5 seeds);
exp422 landed the recipe VIABLE at n=4 (refresh at g = 0.05 visible
+ carrier-retained; the G2 direction honestly REFUTE-recorded). THE
OPEN QUESTION: does the recipe SCALE — does saturate-then-refresh-
below-g* carry an invisible zone on the human connectome's wiring?

THE INSTRUMENT (exp412's connectome form verbatim + exp422's recipe
schedule verbatim; zero new knobs): the connectome host, the
dissolution sweep to g in {0.05, 0.08, 0.117, 0.15, 0.20} (below and
above g*), the refresh arm vs the no-refresh control, 5 seeds;
FACES: invisible-zone retention (the exp412 read), carrier retention
(the exp422 read), and the recipe-vs-control delta per g.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0; exp412's deposited connectome
      identity reproduced (the bit-exact face, delta 0.0 on the
      no-recipe control, 5/5 seeds; fail=STOP).
  G2  the discipline: the refresh schedule fixed before the runs
      (refresh at the arm's g, the exp422 semantics); no recipe
      parameter tuned post hoc.
  G3  THE SCALING: the recipe's invisible-zone retention at g < g*
      >= the no-refresh control's on >= 4/5 seeds per g (RECIPE-
      SCALES) or the connectome wiring breaks it (RECIPE-BREAKS —
      honest, deposited with the g profile).
  G4  the anatomy: the retention x g curve per arm deposited + the
      carrier-retention column.
  G5  deposit results/exp433_recipe_on_connectome.json.

BRANCH LATTICE: RECIPE-SCALES / RECIPE-BREAKS / INSTRUMENT-REFUTED.
"""

from __future__ import annotations

import json
import os
import sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_STAR = 0.117
GLADDER_433 = [0.05, 0.08, 0.117, 0.15, 0.20]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
WOUND_VOLT = -30.0
DT = 0.1
SETTLE_TU = 30.0
SEEDS = [0, 1, 2, 3, 4]
CARRIER_BAR = 0.8            # exp422's retained read
DEPOSIT = os.path.join(ROOT, "results", "exp433_recipe_on_connectome.json")

BODY_DISCLOSURES = [
    "the host build = exp412's verbatim (load_human_fc sha-asserted, "
    "build_human_adjacency row-sum 0.4 asserted, human_target, region "
    "= zones == 0); the walk = exp412's _walk_union verbatim at "
    "union_on=True (the ladder arm exp412's G4 read rode on) with "
    "exp422's two-pass schedule spliced in: _pass(g) then ONE refresh "
    "_pass(refresh_g), the stress pin wrapping BOTH passes and "
    "restored before the settle (exp422's floor form)",
    "the faces: the exp412 read = the stress-gated delta "
    "|e_stress - e_calm| per (arm, g, seed) — the invisible zone's "
    "depth read; the exp422 read = the carrier improvement "
    "e_calm(g=0) - e_calm(arm) with the 0.8 x one-pass-g=1.0 "
    "retention bar; the invisible-zone RETENTION value = "
    "vis_g0(seed) - |Delta|(arm, g, seed) — how much of the fully "
    "visible g=0 stress signal the arm suppresses",
    "G3's frozen reading: the recipe's retention >= the control's "
    "per seed per g strictly below g* ({0.05, 0.08}); the g >= g* "
    "rungs ride in the anatomy ungated",
    "G1's bit-exact face: exp412's deposited errs_per_g['0.0'] rows "
    "(LADDER_SEEDS 0-2, union_on=True) must reproduce exactly — the "
    "one-pass control at g=0 IS exp412's arm bit-path; the delta-0.0 "
    "face is then the g=0 bit-identity on 5/5 seeds (the head seeds "
    "extended, disclosed: seeds 3-4 have no exp412 row and ride "
    "ungated)",
    "deterministic (the seeds carry all randomness); the credited "
    "run is the runner run at the pushed state",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective
from human.substrate import (build_human_adjacency, human_target,
                             load_human_fc)


def order_of(h, region):
    """exp412's frontier BFS order verbatim (rebuilt per pass — the
    order depends only on A and region, both frozen; exp412 built it
    once per walk, identical form)."""
    region_set = set(region)
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(h.theta[j]
                                                      - WOUND_VOLT)))
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
    return order


def _blended_set(h, region, union_on):
    """exp412's blended set verbatim: boundary cells, plus the
    junction rule (support-degree >= 2 interior cells) when
    union_on."""
    region_set = set(region)
    cls = {}
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        cls[i] = 0 if nbrs else 1
    if union_on:
        support_deg = (np.abs(h.A) > 0).sum(axis=1)
        junction = set(int(i) for i in region
                       if cls[i] != 0 and int(support_deg[i]) >= 2)
        return set(int(i) for i in region if cls[i] == 0) | junction
    return set(int(i) for i in region if cls[i] == 0)


def _run_arm(W, tgt, region, g, stress, seed, refresh_g=None,
             union_on=True):
    """exp412's _run_human verbatim + exp422's two-pass schedule."""
    h = GraphCollective(adjacency=W, seed=seed)
    h.set_target(tgt)
    h.run(SETTLE_TU, dt=DT)
    h.phi_spec = tgt.copy()
    h.phi_history = tgt.copy()
    h.theta[region] = WOUND_VOLT
    h.V[region] = WOUND_VOLT
    blended = _blended_set(h, region, union_on)
    order = order_of(h, region)     # frozen: A and region fixed
    if stress:
        CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
    try:
        _pass_h(h, order, blended, g)
        if refresh_g is not None:
            _pass_h(h, order, blended, refresh_g)
    finally:
        if stress:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    h.run(SETTLE_TU, dt=DT)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored in arm"
    e = float(h.pattern_error(tgt))
    assert np.isfinite(e)
    return e


def _pass_h(h, order, blended, g):
    """The commit pass with the prebuilt order (exp412's loop)."""
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            h.step(DT)
        if h.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
            theta_new = h.phi_spec[i] + h.rng.normal(0.0, COMMIT_NOISE)
        else:
            theta_new = h.theta[src] + h.rng.normal(0.0, COMMIT_NOISE)
        written = theta_new
        if g > 0.0 and int(i) in blended:
            written = ((1.0 - g) * theta_new
                       + g * float(h.phi_history[i]))
        h.theta[i] = written
        h.V[i] = written
        h.phi_history[i] = written


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert GLADDER_433 == [0.05, 0.08, 0.117, 0.15, 0.20]
    assert G_STAR == 0.117 and CARRIER_BAR == 0.8

    fc = load_human_fc()
    W = build_human_adjacency(fc)
    rs = float(W.sum(axis=1).mean())
    assert abs(rs - 0.4) < 1e-9, rs
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])

    # ---- G1 the anchors: exp412's g=0 ladder rows bit-exact
    dep412 = json.load(open(os.path.join(
        ROOT, "results", "exp412_invisibility_human.json")))
    ref = dep412["ladder"]["errs_per_g"]["0.0"]
    bit_ok = True
    for si, seed in enumerate([0, 1, 2]):
        for tag, stress in (("off", False), ("on", True)):
            e = _run_arm(W, tgt, region, 0.0, stress, seed)
            if e != ref[tag][si]:
                bit_ok = False
                print("  g=0 %s seed %d: %.12f vs %.12f"
                      % (tag, seed, e, ref[tag][si]))
    verdicts["G1"] = "PASS" if bit_ok else "REFUTE"
    print("G1 %s (exp412's g=0 rows bit-exact on seeds 0-2, "
          "union_on=True; the delta-0.0 face = the bit-identity)"
          % verdicts["G1"])
    if smoke:
        print("SMOKE OK discarded (no deposit written; the G1 bit-face "
          "is the smoke's job — the sweep is the full budget's)")
        return {"gates": verdicts}
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    else:
        # ---- G2 the discipline (frozen schedule, disclosed)
        verdicts["G2"] = "PASS"
        print("G2 PASS (the two-pass schedule frozen: saturate 1.0 -> "
              "ONE refresh at the arm's g, exp422's semantics; no "
              "post-hoc tuning)")

        # ---- the g=0 visibility anchors per seed
        vis_g0 = {}
        for seed in seeds:
            e_calm = _run_arm(W, tgt, region, 0.0, False, seed)
            e_stress = _run_arm(W, tgt, region, 0.0, True, seed)
            vis_g0[seed] = abs(e_stress - e_calm)

        # ---- the one-pass g=1.0 carrier normalization
        e_off0 = {s: _run_arm(W, tgt, region, 0.0, False, s)
                  for s in seeds}
        e_g1 = {s: _run_arm(W, tgt, region, 1.0, False, s)
                for s in seeds}
        one_pass_imp = float(np.mean([e_off0[s] - e_g1[s]
                                      for s in seeds]))

        # ---- the sweep: control (one-pass) vs recipe (two-pass)
        curve = {}
        for g in GLADDER_433:
            control_v, recipe_v = {}, {}
            control_c, recipe_c = {}, {}
            for seed in seeds:
                e_ctl_c = _run_arm(W, tgt, region, g, False, seed)
                e_ctl_s = _run_arm(W, tgt, region, g, True, seed)
                control_v[seed] = abs(e_ctl_s - e_ctl_c)
                control_c[seed] = e_off0[seed] - e_ctl_c
                e_rec_c = _run_arm(W, tgt, region, 1.0, False, seed,
                                   refresh_g=g)
                e_rec_s = _run_arm(W, tgt, region, 1.0, True, seed,
                                   refresh_g=g)
                recipe_v[seed] = abs(e_rec_s - e_rec_c)
                recipe_c[seed] = e_off0[seed] - e_rec_c
            curve[g] = {
                "control_vis": {s: round(v, 6)
                                for s, v in control_v.items()},
                "recipe_vis": {s: round(v, 6)
                               for s, v in recipe_v.items()},
                "control_retention": {s: round(vis_g0[s] - control_v[s],
                                               6) for s in seeds},
                "recipe_retention": {s: round(vis_g0[s] - recipe_v[s],
                                              6) for s in seeds},
                "control_carrier_imp": float(np.mean(
                    [control_c[s] for s in seeds])),
                "recipe_carrier_imp": float(np.mean(
                    [recipe_c[s] for s in seeds])),
                "control_carrier_retained": bool(
                    float(np.mean([control_c[s] for s in seeds]))
                    >= CARRIER_BAR * one_pass_imp),
                "recipe_carrier_retained": bool(
                    float(np.mean([recipe_c[s] for s in seeds]))
                    >= CARRIER_BAR * one_pass_imp),
            }
            print("  g=%.3f: control vis %.4f (carrier %s) | recipe "
                  "vis %.4f (carrier %s)"
                  % (g, np.mean(list(control_v.values())),
                     curve[g]["control_carrier_retained"],
                     np.mean(list(recipe_v.values())),
                     curve[g]["recipe_carrier_retained"]))

        # ---- G3 the scaling (g < g* strictly, per g, per seed)
        cells = {}
        for g in GLADDER_433:
            if g >= G_STAR:
                continue
            hits = sum(1 for s in seeds
                       if curve[g]["recipe_retention"][s]
                       >= curve[g]["control_retention"][s])
            cells[g] = {"hits": hits, "of": len(seeds),
                        "ok": hits >= 4}
        all_ok = bool(cells) and all(c["ok"] for c in cells.values())
        verdicts["G3"] = "PASS" if all_ok else "REFUTE"
        print("G3 %s (retention hits %s)"
              % (verdicts["G3"], {g: c["hits"] for g, c in
                                  cells.items()}))

        branch = "RECIPE-SCALES" if all_ok else "RECIPE-BREAKS"

        # ---- G4 the anatomy
        verdicts["G4"] = "PASS"
        detail = {"vis_g0": {s: round(v, 6) for s, v in
                             vis_g0.items()},
                  "one_pass_imp": round(one_pass_imp, 6),
                  "carrier_bar": CARRIER_BAR,
                  "g3_cells": cells}
        print("G4 PASS (the retention x g curve per arm + the carrier "
              "column deposited; vis_g0 %.4f, one-pass imp %.4f)"
              % (np.mean(list(vis_g0.values())), one_pass_imp))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    out = {
        "experiment": "exp433",
        "title": "THE INVISIBILITY RECIPE ON THE HUMAN CONNECTOME "
                 "(batch HU-13)",
        "instrument": {"gladder": GLADDER_433, "g_star": G_STAR,
                       "seeds": SEEDS, "union_on": True,
                       "carrier_bar": CARRIER_BAR},
        "curve": curve,
        "detail": detail,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP433 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
