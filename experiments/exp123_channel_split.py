#!/usr/bin/env python3
"""exp123 — THE CHANNEL SPLIT (ledger L103's registration: exp122
reinterpreted the onset kernel as the MU-SILENCE DEADLINE — the
blockade rescues the default-cell torus because gap_scale scales
the theta-diffusion term. This experiment splits the two channels
causally: the theta channel (mu) vs the V-coupling channel (G).)

THE ARMS (torus, default cell gamma 1 mu 0.015, onsets {0, 6, 12,
18, 24, 36, 48, 72}, 8 seeds):
  full    block_gap_junctions(0.05) from onset (both channels:
          G/deg scaled AND gap_scale -> theta diffusion cut) —
          the exp120 default arm reproduced in-batch
  mu_only c.mu = 0.0 from onset (theta diffusion cut directly,
          V-coupling INTACT)
  g_only  G/deg scaled to 0.05 from onset with gap_scale HELD AT
          1.0 (V-coupling cut, theta diffusion INTACT)
  control no intervention (the exp122 column: P(break) = 1.0)

PRE-REGISTERED GATES:

  CS-G1  (the deadline is the theta channel) the mu_only arm's
         P(break) matches the full arm within 0.125 at every
         onset — cutting mu alone rescues exactly like the
         blockade.
  CS-G2  (the V channel is not the carrier) the g_only arm's
         P(break) matches the no-intervention control within
         0.125 at every onset — cutting V-coupling alone changes
         nothing.
  CS-G3  (harness continuity) the full arm's curve matches
         exp120's deposited default arm within 0.125 at every
         onset.

RUN: 4 arms x 8 onsets x 8 seeds = 256 runs. Serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp123_channel_split.json")

SEEDS = tuple(range(1, 9))
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)
WINDOW_H = 24.0
SETTLE_H = 15.0
BLOCK_SCALE = 0.05


def run_arm_mode(adj, seed: int, onset: float, mode: str) -> bool:
    """mode: 'full' | 'mu_only' | 'g_only' | 'control'. The
    intervention switches at `onset` protocol-hours and holds."""
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
        return True
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def apply(t):
        if t < onset or mode == "control":
            return
        if mode in ("full", "g_only"):
            c.G = c.G0 * BLOCK_SCALE
            c.deg = c.G.sum(axis=1)
        if mode == "full":
            c.gap_scale = BLOCK_SCALE
        if mode == "mu_only":
            c.mu = 0.0

    t0 = 0.0
    for _ in range(int(round(WINDOW_H / dt))):
        t0 += dt
        apply(t0)
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
            apply(t0)
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
    c.run(SETTLE_H, dt=dt)
    return bool(float(c.pattern_error(target)) >= ERR_BAR)


def main() -> dict:
    print("=== exp123: the channel split ===\n")

    battery = build_battery()
    torus = battery["torus"]
    exp120 = json.load(open(os.path.join(
        ROOT, "results", "exp120_kernel_shape.json")))

    out: dict = {}
    curves: dict = {}
    for mode in ("full", "mu_only", "g_only", "control"):
        ps = []
        for onset in ONSETS:
            br = [run_arm_mode(torus, s, onset, mode)
                  for s in SEEDS]
            p = round(float(np.mean(br)), 3)
            ps.append(p)
            out[f"{mode}_t{onset:g}"] = p
        curves[mode] = ps
        print(f"    {mode:8s} P(break): {ps}")

    cs_g1 = all(abs(a - b) <= 0.125 for a, b in
                zip(curves["mu_only"], curves["full"]))
    cs_g2 = all(abs(a - b) <= 0.125 for a, b in
                zip(curves["g_only"], curves["control"]))
    dep = exp120["curves"]["torus"]["default"]
    cs_g3 = all(abs(a - b) <= 0.125 for a, b in
                zip(curves["full"], dep))

    print(f"\n  CS-G1 mu-only == full (theta channel): "
          f"{'PASS' if cs_g1 else 'REFUTED'}")
    print(f"  CS-G2 g-only == control (V channel inert): "
          f"{'PASS' if cs_g2 else 'REFUTED'}")
    print(f"  CS-G3 full == exp120 default (harness): "
          f"{'PASS' if cs_g3 else 'REFUTED'}")

    npass = sum([cs_g1, cs_g2, cs_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp123_channel_split",
        "P_break": out,
        "curves": curves,
        "criteria": {
            "CS_G1_theta_channel": bool(cs_g1),
            "CS_G2_v_channel_inert": bool(cs_g2),
            "CS_G3_harness_continuity": bool(cs_g3),
        },
        "notes": (
            "The causal split of the mu-silence deadline: mu-only "
            "(c.mu = 0 from onset, coupling intact) vs g-only "
            "(G/deg scaled, gap_scale held at 1.0 — theta "
            "diffusion intact) vs the full blockade vs control. "
            "The record's drug mapping is exact iff CS-G1 and "
            "CS-G2 both hold."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
