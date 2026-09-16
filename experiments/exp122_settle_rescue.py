#!/usr/bin/env python3
"""exp122 — THE SETTLE-RESCUE TEST (ledger L102's registration:
exp121 localized the torus's closure-edge break in the INTACT field
— the walk-time wound-exposure drift (exp110) frozen in when the
blockade cuts the coupling whose settle would re-smooth it. The
dual-phase claim: the walk-time exposure SEEDS the drift and the
settle's coupling RE-SMOOTHS it; breaking requires both the seed
and the freeze. This experiment runs the 2x2 phase structure.)

THE ARMS (torus, onset 48 h — the edge, mu 0.015, 8 seeds):
  walk_only    blockade applied at onset 48, RESTORED (scale 1.0)
               at the settle start — the walk-time exposure with a
               rescuing settle
  settle_only  no blockade until the walk ends, then blocked
               through the settle — the freeze without the
               walk-time seed (the settle-start blockade at 82.4 h
               protocol time)
  sustained    blockade from onset 48 to the read (exp121's
               breaking arm, re-run in-batch)
  control      never blocked, full settle (the exp111 default
               column re-derived in-batch)

PRE-REGISTERED GATES:

  SR-G1  (the walk-time seed is survivable) walk_only's P(break)
         <= 0.125 (<= 1/8 seeds) while sustained's P(break) >= 0.5
         — restoring the settle rescues the edge.
  SR-G2  (the phase structure is named) the full 2x2 (plus
         control) is deposited and the rescue ordering satisfies
         walk_only < sustained - 0.25 — the settle's coupling is
         the rescuing phase, completing the exp108-121 chain: the
         walk tax seeds (exp110), the mu silence protects
         (exp115-116), the settle coupling re-smooths (this), and
         the closure edge is where the seed meets the freeze.

RUN: 4 arms x 8 seeds. Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.compiler.anatomy import compile_anatomy
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import GraphCollective
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI, ERR_BAR
from experiments.exp112_walk_speed_ladder import build_battery
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp122_settle_rescue.json")

SEEDS = tuple(range(1, 9))
WINDOW_H = 24.0
SETTLE_H = 15.0
BLOCK_SCALE = 0.05
ONSET = 48.0


def run_phase(adj, seed: int, block_from: float | None,
              block_until: float | None) -> dict:
    """The standard regeneration with the blockade applied from
    `block_from` until `block_until` protocol-hours (None until =
    to the read; None from = never). Returns the final err."""
    n = adj.shape[0]
    dt = star_dt(1.0, float(adj.sum(axis=1).max()))
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    c = GraphCollective(adjacency=adj, seed=seed, gamma=1.0,
                        mu_theta=0.015)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return {"err": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def gate(t):
        if block_from is None or t < block_from:
            return
        if block_until is not None and t >= block_until:
            if not c.gap_scale == 1.0:
                c.block_gap_junctions(1.0)
            return
        if c.gap_scale != BLOCK_SCALE:
            c.block_gap_junctions(BLOCK_SCALE)

    t0 = 0.0
    for _ in range(int(round(WINDOW_H / dt))):
        t0 += dt
        gate(t0)
        c.step(dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
    region_set = set(reg_walk)
    c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
    wound_center = float(np.mean(c.theta[reg_walk]))
    parent_of: dict[int, int] = {}
    frontier: list[int] = []
    for i in reg_walk:
        nbrs = [j for j in np.where(c.A[i] > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(
                nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = reg_idx[:1]
        parent_of[frontier[0]] = frontier[0]
    visited = set(frontier)
    order2 = [(i, parent_of[i]) for i in frontier]
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order2.append((int(j), int(i)))
                queue.append(int(j))
    for i, src in order2:
        for _ in range(8):
            t0 += dt
            gate(t0)
            c.step(dt)
        canon_src = getattr(c, "phi_spec_canon", None)
        if c.phi_spec[i] >= NEURAL_SPEC_MIN:
            theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
        elif canon_src is not None:
            theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
        else:
            theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    walk_end = WINDOW_H + 0.8 * n * 0.73
    for _ in range(int(round(SETTLE_H / dt))):
        t0 += dt
        gate(t0)
        c.step(dt)
    return {"err": round(float(c.pattern_error(target)), 2),
            "walk_end": round(walk_end, 1)}


def main() -> dict:
    print("=== exp122: the settle-rescue test ===\n")

    battery = build_battery()
    torus = battery["torus"]
    walk_end = WINDOW_H + 0.8 * torus.shape[0] * 0.73

    ARMS = {
        "walk_only": (ONSET, walk_end),
        "settle_only": (walk_end, None),
        "sustained": (ONSET, None),
        "control": (None, None),
    }
    out: dict = {}
    rates: dict = {}
    for arm, (bf, bu) in ARMS.items():
        errs = []
        for s in SEEDS:
            r = run_phase(torus, s, bf, bu)
            errs.append(r["err"])
        errs_a = np.array(errs)
        rates[arm] = round(float(np.mean(
            errs_a >= ERR_BAR)), 3)
        out[arm] = {"errs": [round(e, 2) for e in errs],
                    "mean_err": round(float(errs_a.mean()), 2),
                    "P_break": rates[arm]}
        print(f"    {arm:12s} mean {out[arm]['mean_err']:5.2f}  "
              f"P(break) {rates[arm]:.3f}  errs {out[arm]['errs']}")

    sr_g1 = rates["walk_only"] <= 0.125 and rates["sustained"] >= 0.5
    sr_g2 = rates["walk_only"] <= rates["sustained"] - 0.25

    print(f"\n  SR-G1 walk-time seed survivable: "
          f"{'PASS' if sr_g1 else 'REFUTED'}")
    print(f"  SR-G2 rescue ordering (walk_only <= "
          f"sustained - 0.25): {'PASS' if sr_g2 else 'REFUTED'}")

    npass = sum([sr_g1, sr_g2])
    print(f"\n  === {npass}/2 gates PASS ===")

    result = {
        "exp": "exp122_settle_rescue",
        "arms": out,
        "P_break": rates,
        "walk_end_h": round(walk_end, 1),
        "criteria": {
            "SR_G1_seed_survivable": bool(sr_g1),
            "SR_G2_rescue_ordering": bool(sr_g2),
        },
        "notes": (
            "The 2x2 phase structure at the torus's closure edge "
            "(onset 48 h): walk-only blockade with a rescuing "
            "settle, settle-only blockade, sustained, and the "
            "unblocked control. Completes the exp108-122 chain: "
            "walk tax seeds, mu silence protects, settle coupling "
            "re-smooths, the closure edge is where the seed meets "
            "the freeze."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
