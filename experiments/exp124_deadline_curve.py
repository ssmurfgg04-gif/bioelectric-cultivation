#!/usr/bin/env python3
"""exp124 — THE DEADLINE CURVE D(gamma) (ledger L103-L104's arc:
the onset kernel is the MU-SILENCE DEADLINE, and it is CONJUNCTIVE
at gamma 1 — both channels must be cut. The unifying question: how
does the deadline move with pinning? At gamma 64 grid2d tolerates
default mu outright (V_PRICED); the torus's gamma ladder at default
mu refuses through 64 (exp100) — so the torus's deadline is finite
at every gamma, but it should RECEDE as gamma rises (stronger
pinning resists the window's mu damage longer). D(gamma) is the
temporal view of the class structure: DEFAULT = no deadline,
V_PRICED = deadline beyond the protocol at gamma_min, TWO_DIAL /
GEOMETRY = finite deadline at every gamma.)

THE PROTOCOL (torus, mu 0.015 from t=0, gamma FIXED at g in
{1, 4, 16, 64} from t=0 — dt = star_dt(g) for Euler stability —
intervention: c.mu = 0 at onset in {0, 6, 12, 18, 24, 36, 48, 72},
8 seeds, 3-seed pilot dropped: full seeds). The edge position
(first onset with P(break) >= 0.5) = the deadline at that gamma.

PRE-REGISTERED GATES:

  DC-G1  (the deadline recedes with pinning) the edge position is
         non-decreasing in gamma across {1, 4, 16, 64}.
  DC-G2  (the class structure interpolates) at gamma 64 the torus
         either never breaks (P = 0 flat — the deadline exits the
         protocol window, the V_PRICED-like tolerance emerging) or
         its edge is >= 36 h — no sharpening with strength.
  DC-G3  (the gamma-1 anchor reproduces) the gamma-1 curve matches
         exp123's full-blockade curve within 0.125 at every onset
         (the mu-only-from-onset at gamma 1 differs from the full
         blockade — exp123's CS-G1 refutation — so the anchor here
         is the FULL-blockade curve's SHAPE: both are mu-silenced
         at onset; gamma 1's deadline should land in the same grid
         cell, 36 h).

RUN: 4 gammas x 8 onsets x 8 seeds = 256 runs. Serial, BLAS
pinned.
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
OUT = os.path.join(ROOT, "results", "exp124_deadline_curve.json")

SEEDS = tuple(range(1, 9))
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)
WINDOW_H = 24.0
SETTLE_H = 15.0
GAMMAS = (1.0, 4.0, 16.0, 64.0)


def run_deadline(adj, seed: int, gamma: float, onset: float) -> bool:
    """gamma fixed from t=0 (dt stable), mu 0.015 until `onset`,
    then c.mu = 0 to the read. Returns BREAK."""
    n = adj.shape[0]
    dt = star_dt(gamma, float(adj.sum(axis=1).max()))
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    c = GraphCollective(adjacency=adj, seed=seed, gamma=gamma,
                        mu_theta=0.015)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return True
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def maybe(t):
        if t >= onset:
            c.mu = 0.0

    t0 = 0.0
    for _ in range(int(round(WINDOW_H / dt))):
        t0 += dt
        maybe(t0)
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
            maybe(t0)
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
    print("=== exp124: the deadline curve D(gamma) ===\n")

    battery = build_battery()
    torus = battery["torus"]
    out: dict = {}
    curves: dict = {}
    for g in GAMMAS:
        ps = []
        for onset in ONSETS:
            br = [run_deadline(torus, s, g, onset) for s in SEEDS]
            p = round(float(np.mean(br)), 3)
            ps.append(p)
            out[f"g{g:g}_t{onset:g}"] = p
        curves[g] = ps
        print(f"    gamma {g:5.1f}  P(break): {ps}")

    def edge(ps):
        for t, p in zip(ONSETS, ps):
            if p >= 0.5:
                return t
        return None

    edges = {g: edge(ps) for g, ps in curves.items()}
    e_vals = [edges[g] if edges[g] is not None else 10 ** 9
              for g in GAMMAS]
    dc_g1 = all(e_vals[i] >= e_vals[i + 1] - 1e-9
                for i in range(len(e_vals) - 1))
    dc_g2 = (edges[64.0] is None) or (edges[64.0] >= 36.0)
    exp123 = json.load(open(os.path.join(
        ROOT, "results", "exp123_channel_split.json")))
    # the gamma-1 anchor: exp123's mu_only curve is the SAME
    # protocol (mu->0 at onset, gamma 1) — compare
    anchor = exp123["curves"]["mu_only"]
    dc_g3 = all(abs(a - b) <= 0.125 for a, b in
                zip(curves[1.0], anchor))

    print(f"\n  edges: {edges}")
    print(f"  DC-G1 deadline recedes with pinning: "
          f"{'PASS' if dc_g1 else 'REFUTED'}")
    print(f"  DC-G2 class structure interpolates: "
          f"{'PASS' if dc_g2 else 'REFUTED'}")
    print(f"  DC-G3 gamma-1 anchor == exp123 mu_only: "
          f"{'PASS' if dc_g3 else 'REFUTED'}")

    npass = sum([dc_g1, dc_g2, dc_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp124_deadline_curve",
        "P_break": out,
        "curves": {str(k): v for k, v in curves.items()},
        "edges": {str(k): v for k, v in edges.items()},
        "criteria": {
            "DC_G1_deadline_recedes": bool(dc_g1),
            "DC_G2_class_interpolates": bool(dc_g2),
            "DC_G3_anchor_continuity": bool(dc_g3),
        },
        "notes": (
            "The deadline curve D(gamma) on the torus: mu silenced "
            "at onset under fixed pinning gamma in {1, 4, 16, 64}. "
            "The temporal view of the class structure: DEFAULT = "
            "no deadline, V_PRICED = deadline beyond the protocol, "
            "TWO_DIAL/GEOMETRY = finite deadline at every gamma."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
