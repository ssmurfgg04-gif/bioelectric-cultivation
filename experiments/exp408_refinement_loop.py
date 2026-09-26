#!/usr/bin/env python3
"""exp408 — THE REFINEMENT LOOP: DOES THE REGISTER'S MEMORY KEEP THE
PATTERN THROUGH SUCCESSIVE WOUND/REPAIR CYCLES? (batch HU-8; ledger
L303; charter docs/HUMAN_EXTENSION.md §8; the user's "history register
→ refinement" angle: the system gets better at maintaining its pattern
BECAUSE of its history — the computational analog of the cultivation
traditions' refinement). exp403 landed HISTORY-PROTECTS-HUMAN (one
cycle); exp407 landed BYPASS-EXPLAINED. THE OPEN QUESTION: across k
successive wound/repair cycles, does the register's carryover keep the
committed pattern CLEAN (the refinement claim — the stored memory is
better than the raw write channel and STAYS better), or does the noise
compound cycle-over-cycle (the corruption claim)?

THE THEORY FACE (pre-registered, derived BEFORE the run): at the
blended boundary cells the deviation from the spec obeys
d_k = (1-g)·noise_k + g·d_{k-1} (the register carries the previous
committed value). At g=0.5 with the commit sigma 0.6: RMS_1 = 0.30
(the register starts AT the spec install — the cleanest possible
memory), RMS_∞ = σ·sqrt(g/(1+g))·... = σ·sqrt((1-g)/... ) — the
fixed-point variance (1-g)²σ²/(1−g²) → RMS_∞ = σ·sqrt((1−g)/(1+g))
= 0.6·sqrt(0.5/1.5) = 0.346. THE PREDICTION: the ON arm's committed
RMS is bounded in [0.30, 0.35] across all cycles (the memory holds the
pattern ~1.7× cleaner than the raw write channel) and SATURATES (the
convergence face), while the OFF arm's committed RMS stays at σ = 0.6
(no carryover: every cycle re-rolls the full noise).

THE INSTRUMENT (exp403's landed walk form, cycled; on the human
graph): k = 8 cycles; each cycle = the wound (zone 0 → −30.0) → the
wait 20 tu → the corrective BFS walk (STEPS_PER_CELL 8,
COMMIT_NOISE 0.6, the register blend at the boundary g_ctx = 0.5 ON /
0.0 OFF; the register populated at the write) → the settle 30 tu; the
register persists ACROSS cycles (the carryover channel under test);
5 seeds; two arms (ON g=0.5, OFF g=0.0).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the exp401 adjacency rebuild (density 1e-12); the
      floor −60.0 at entry/exit; the constants pre-named (g 0.5, the
      commit sigma 0.6, STEPS_PER_CELL 8, the wound −30.0, the wait
      20, k 8) and asserted (fail=STOP).
  G2  THE SINGLE-CYCLE ANCHOR: e_1(ON) < e_1(OFF) at the 5-seed mean
      (the exp403 protection reproduces on the cycled instrument).
  G3  THE REFINEMENT FACE (the committed layer, the boundary cells):
      the committed-value RMS deviation from the spec, per cycle —
      (a) ON < OFF at EVERY cycle, 8/8; (b) ON bounded by the theory
      band [0.25, 0.40] at every cycle (the pre-named bar around the
      derived [0.30, 0.346]); (c) OFF's RMS within [0.54, 0.66]
      (the σ = 0.6 channel, no carryover).
  G4  THE SATURATION FACE: ON's committed RMS converges —
      |RMS_8 − RMS_6| <= 0.02 (the pre-named bar; the refinement
      SATURATES at the memory's fixed point, it does not compound to
      zero — the honest shape the theory face derives).
  G5  THE PATTERN FACE: the settled pattern error e_k(ON) < e_k(OFF)
      at EVERY cycle, 8/8 (the protection persists across the loop).
  G6  THE DEPOSIT: the per-cycle tables (the committed RMS per arm,
      the pattern errs per arm per seed), the theory face, the gates
      and the branch deposited as results/exp408_refinement_loop.json
      (fail=STOP).

BRANCH LATTICE (pre-named): G1–G6 all PASS -> REFINEMENT-SUSTAINED
(the register's memory keeps the pattern cleaner than the raw write
channel across the whole loop, saturating at the derived fixed point
— the "refinement" is real and bounded); any of G3–G5 FAIL ->
REFINEMENT-REFUTED (the carryover corrupts or fades — the honest
negative); G1/G2 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: REFINEMENT-SUSTAINED would ground the cultivation
narrative computationally — the memory channel is cleaner than the
write channel and the gap is SUSTAINED by the carryover — while ALSO
bounding it honestly (the saturation face: practice does not make the
pattern perfect; it holds it at the memory's fixed point).
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cultivation.substrate.graph import GraphCollective
from human.substrate import build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp408_refinement_loop.json")
K = 8
SEEDS = [0, 1, 2, 3, 4]
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
WOUND_V = -30.0
WAIT_TU = 20.0
SETTLE_TU = 30.0
DT = 0.1


def _corrective_walk(h, region):
    region_set = set(region)
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(h.theta[j] - WOUND_V)))
            frontier.append(i)
    if not frontier:
        return {}, set()
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
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(h.A[i]) > 0)[0]))
    commits = {}
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            h.step(DT)
        if h.phi_spec[i] >= -60.0:
            commit_base = h.phi_spec[i]
        else:
            commit_base = h.theta[src]
        theta_new = commit_base + h.rng.normal(0.0, COMMIT_NOISE)
        written = theta_new
        if G_CTX > 0.0 and i in bnd:
            written = ((1.0 - G_CTX) * theta_new
                       + G_CTX * float(h.phi_history[i]))
        h.theta[i] = written
        h.V[i] = written
        h.phi_history[i] = written
        if i in bnd:
            commits[i] = float(written)
    return commits, bnd


def main() -> dict:
    """THE BODY IS WRITTEN AT THE BODY COMMIT (pre-registration)."""
    raise NotImplementedError("exp408 body lands at the body commit")


    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 the anchors
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    dep401 = json.load(open(os.path.join(ROOT, "results",
                                         "exp401_human_substrate.json")))
    assert abs(float(dep401["preprocessing"]["density"])
               - float((W > 0).mean())) < 1e-12
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])
    assert len(region) == 80
    assert (G_CTX, COMMIT_NOISE, STEPS_PER_CELL, WOUND_V, WAIT_TU,
            SETTLE_TU, K) == (0.5, 0.6, 8, -30.0, 20.0, 30.0, 8)
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: density %.4f, k=%d)" % (float((W > 0).mean()), K))

    # ---- the loop battery
    rms_on = {k: [] for k in range(1, K + 1)}
    rms_off = {k: [] for k in range(1, K + 1)}
    e_on = {k: [] for k in range(1, K + 1)}
    e_off = {k: [] for k in range(1, K + 1)}
    for seed in SEEDS:
        for arm, g in [("ON", G_CTX), ("OFF", 0.0)]:
            h = GraphCollective(adjacency=W, seed=seed)
            h.set_target(tgt)
            h.run(30.0, dt=DT)
            h.phi_spec = tgt.copy()
            h.phi_history = tgt.copy()   # the register's clean install
            for k in range(1, K + 1):
                h.theta[region] = WOUND_V
                h.V[region] = WOUND_V
                h.run(WAIT_TU, dt=DT)
                commits, bnd = _corrective_walk(h, region)
                if g == 0.0:
                    # re-apply the OFF semantics: the walk above blended
                    # at G_CTX; rebuild the OFF arm by redoing the cycle
                    # with the blend disabled is cleaner — see the second
                    # pass below (the arm loop is split for clarity)
                    pass
                h.run(SETTLE_TU, dt=DT)
                e = float(h.pattern_error(tgt))
                if bnd:
                    devs = [commits[i] - float(tgt[i]) for i in bnd]
                    rms = float(np.sqrt(np.mean(np.square(devs))))
                else:
                    rms = float("nan")
                assert np.isfinite(e) and np.isfinite(rms)
                if arm == "ON":
                    rms_on[k].append(rms)
                    e_on[k].append(e)
                else:
                    rms_off[k].append(rms)
                    e_off[k].append(e)
    verdicts["G2"] = "PASS"
    print("G2 deferred to the split-arm pass")

    # NOTE: the single-pass structure above cannot express both arms
    # cleanly (the OFF arm must skip the blend INSIDE the walk); the
    # split-arm pass below is the real battery (the first pass's OFF
    # rows are DISCARDED as instrument scaffolding — disclosed).
    rms_on = {k: [] for k in range(1, K + 1)}
    rms_off = {k: [] for k in range(1, K + 1)}
    e_on = {k: [] for k in range(1, K + 1)}
    e_off = {k: [] for k in range(1, K + 1)}
    blend_flag = {"ON": True, "OFF": False}
    for seed in SEEDS:
        for arm in ("ON", "OFF"):
            h = GraphCollective(adjacency=W, seed=seed)
            h.set_target(tgt)
            h.run(30.0, dt=DT)
            h.phi_spec = tgt.copy()
            h.phi_history = tgt.copy()
            for k in range(1, K + 1):
                h.theta[region] = WOUND_V
                h.V[region] = WOUND_V
                h.run(WAIT_TU, dt=DT)
                # the walk with the arm's blend flag (inline; the exp403
                # form with blend_flag controlling the blend)
                region_set = set(region)
                parent_of, frontier = {}, []
                for i in region:
                    nbrs = [j for j in np.where(h.A[i] > 0)[0]
                            if j not in region_set]
                    if nbrs:
                        parent_of[i] = int(max(
                            nbrs, key=lambda j: -abs(h.theta[j] - WOUND_V)))
                        frontier.append(i)
                if not frontier:
                    frontier = region[:1]
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
                bnd = set(i for i in region
                          if any(j not in region_set
                                 for j in np.where(np.abs(h.A[i]) > 0)[0]))
                commits = {}
                for i, src in order:
                    for _ in range(STEPS_PER_CELL):
                        h.step(DT)
                    if h.phi_spec[i] >= -60.0:
                        commit_base = h.phi_spec[i]
                    else:
                        commit_base = h.theta[src]
                    theta_new = commit_base + h.rng.normal(0.0, COMMIT_NOISE)
                    written = theta_new
                    if blend_flag[arm] and i in bnd:
                        written = ((1.0 - G_CTX) * theta_new
                                   + G_CTX * float(h.phi_history[i]))
                    h.theta[i] = written
                    h.V[i] = written
                    h.phi_history[i] = written
                    if i in bnd:
                        commits[i] = float(written)
                h.run(SETTLE_TU, dt=DT)
                e = float(h.pattern_error(tgt))
                devs = [commits[i] - float(tgt[i]) for i in bnd]
                rms = float(np.sqrt(np.mean(np.square(devs))))
                assert np.isfinite(e) and np.isfinite(rms)
                (rms_on if arm == "ON" else rms_off)[k].append(rms)
                (e_on if arm == "ON" else e_off)[k].append(e)

    # ---- G2 the single-cycle anchor
    assert float(np.mean(e_on[1])) < float(np.mean(e_off[1])), \
        (np.mean(e_on[1]), np.mean(e_off[1]))
    verdicts["G2"] = "PASS"
    detail["e1_on_mean"] = float(np.mean(e_on[1]))
    detail["e1_off_mean"] = float(np.mean(e_off[1]))
    print("G2 PASS (e1: ON %.4f < OFF %.4f)"
          % (detail["e1_on_mean"], detail["e1_off_mean"]))

    # ---- G3 the refinement face (the committed RMS)
    rmson = {k: float(np.mean(rms_on[k])) for k in range(1, K + 1)}
    rmsoff = {k: float(np.mean(rms_off[k])) for k in range(1, K + 1)}
    cond_a = all(rmson[k] < rmsoff[k] for k in range(1, K + 1))
    cond_b = all(0.25 <= rmson[k] <= 0.40 for k in range(1, K + 1))
    cond_c = all(0.54 <= rmsoff[k] <= 0.66 for k in range(1, K + 1))
    assert cond_a and cond_b and cond_c, (rmson, rmsoff)
    verdicts["G3"] = "PASS"
    detail["rms_on_mean"] = rmson
    detail["rms_off_mean"] = rmsoff
    print("G3 PASS (ON %s..%.3f bounded [0.25,0.40]; OFF ~%.3f; ON<OFF 8/8)"
          % ("%.3f" % rmson[1], rmson[K], rmsoff[K]))

    # ---- G4 the saturation face
    conv = abs(rmson[K] - rmson[K - 2])
    assert conv <= 0.02, conv
    verdicts["G4"] = "PASS"
    detail["rms_on_convergence"] = conv
    print("G4 PASS (|RMS_8 - RMS_6| = %.4f <= 0.02 — the refinement "
          "saturates at the memory's fixed point)" % conv)

    # ---- G5 the pattern face
    cond5 = all(float(np.mean(e_on[k])) < float(np.mean(e_off[k]))
                for k in range(1, K + 1))
    assert cond5, [(k, np.mean(e_on[k]), np.mean(e_off[k]))
                   for k in range(1, K + 1)]
    verdicts["G5"] = "PASS"
    detail["e_on_mean"] = {k: float(np.mean(e_on[k]))
                           for k in range(1, K + 1)}
    detail["e_off_mean"] = {k: float(np.mean(e_off[k]))
                            for k in range(1, K + 1)}
    print("G5 PASS (e_k: ON < OFF at every cycle, 8/8)")

    # ---- G6 the deposit
    dep = {
        "experiment": "exp408",
        "title": "THE REFINEMENT LOOP (batch HU-8)",
        "theory_face": "d_k = (1-g)*noise_k + g*d_{k-1}; at g=0.5, sigma=0.6: RMS_1=0.30, RMS_inf=0.6*sqrt(0.5/1.5)=0.346",
        "instrument": {"cycles": K, "wait_tu": WAIT_TU, "settle_tu": SETTLE_TU,
                       "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                                     "STEPS_PER_CELL": STEPS_PER_CELL,
                                     "WOUND_V": WOUND_V}},
        "rms_committed": {"ON": rmson, "OFF": rmsoff},
        "pattern_err": {"ON": detail["e_on_mean"],
                        "OFF": detail["e_off_mean"]},
        "rms_on_convergence": conv,
        "disclosures": ["the first single-pass battery's OFF rows were "
                        "discarded as instrument scaffolding (the OFF "
                        "arm's blend flag needs to live inside the walk); "
                        "the deposited battery is the split-arm pass"],
        "gates": verdicts,
        "verdict": "REFINEMENT-SUSTAINED",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G6"] = "PASS"
    print("G6 PASS (deposit %s)" % DEPOSIT)

    print("EXP408 VERDICT: %s REFINEMENT-SUSTAINED" % verdicts)
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
