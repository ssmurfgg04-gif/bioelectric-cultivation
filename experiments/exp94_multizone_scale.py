#!/usr/bin/env python3
"""exp94 — THE MULTI-ZONE REGEN SCALE-UP (ledger L76; the handoff's
open item #5 — exp90's two-source read verified on 7/7 substrates;
the battery now grows to 12 NEW topologies including size-scaled
variants).

THE QUESTION: the multi-zone novel-anatomy regeneration (exp90's
two-source read: the pole read above the M33 line, the canon
coordinate memory below it) verified on exp73's 7-substrate battery
at the star point (errors 0.49-0.70 mV). Does it generalize to
topologies the law has never touched — trees, hubs, cycles, ladders,
barbells, complete and bipartite graphs, elongated grids — and to
LARGER substrates (n=200)?

THE NEW BATTERY (12 substrates, N=100 unless stated):
  tree          balanced binary tree (degree stress: parent hubs of 3)
  star          one hub, 99 spokes (the deg=99 extreme)
  cycle         the ring (degree 2 everywhere, no boundary)
  ladder        the 2x50 prism
  barbell       two K25 cliques + a path bridge (community stress)
  complete      K60 (the deg=59 dense extreme)
  bipartite     K50,50 (no within-class edges)
  grid_elong    grid_2d(5, 20) (the aspect-ratio stress)
  torus_elong   torus(5, 20)
  random8       random_regular(100, k=8)
  path200       path(200) — the size scale
  scale_free200 scale_free(200, seed=13) — the size + hub scale

The executor is exp90's execute_two_source generalized over
n = adjacency.shape[0] (the zone fractions map to any n; the
compiler runs at that n). The multi program: 3 in-domain zones
(-30.0 mV at f 0.02-0.12 / 0.30-0.45 / 0.60-0.75), trunk amputation
— exp90's uc-multi spec verbatim.

PRE-REGISTERED GATES:

  MS-G1  (the scale-up) the multi two-source program verifies
         (>= 2/3 seeds) on >= 9/12 new substrates at the star
         point; errors deposited per substrate (exp90's reference
         band 0.49-0.70 mV on the 7-battery).
  MS-G2  (no backdoor) the below-line variant (the same program
         with the zone voltage at -59.0, out of the M33 domain)
         FAILS on >= 8/12 new substrates — the domain rule survives
         the scale.
  MS-G3  (the canon source is load-bearing) the stripped-canon
         variant fails on >= 8/12 — the two-source structure
         survives the scale (the exp90 TS-G4 pattern).
  MS-G4  (the size scale) the n=200 variants verify on >= 1/2 —
         the reader scales in n.

RUN: 12 substrates x {multi, below-line, no-canon} x 2-3 seeds at
the star point; the R5 partition check per new substrate deposited.
Serial, BLAS pinned.
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

from cultivation.compiler.anatomy import (
    AnatomySpec, Zone, compile_anatomy, substrate_partition_check,
)
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import (
    GraphCollective, path, grid_2d, random_regular, scale_free,
)
from experiments.exp68_coherence_search import torus
from experiments.exp73_active_renormalization import (
    labeling_bfs, circulant, bfs_order, N,
)
from experiments.exp90_two_source_read import star_dt, spec_target
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp94_multizone_scale.json")

ERR_BAR = 6.0
STAR = {"gamma": 64.0, "mu": 0.0}
WINDOW_H = 24.0


def tree_adj(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(1, n):
        p = (i - 1) // 2
        A[i, p] = A[p, i] = 1.0
    return A


def star_adj(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(1, n):
        A[i, 0] = A[0, i] = 1.0
    return A


def cycle_adj(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
    return A


def ladder_adj(n: int) -> np.ndarray:
    h = n // 2
    A = np.zeros((n, n))
    for i in range(h):
        A[i, i + h] = A[i + h, i] = 1.0
        if i + 1 < h:
            A[i, i + 1] = A[i + 1, i] = 1.0
            A[i + h, i + 1 + h] = A[i + 1 + h, i + h] = 1.0
    return A


def barbell_adj(n: int) -> np.ndarray:
    k = 25
    A = np.zeros((n, n))
    for c in (0, k + 25):
        for i in range(c, c + k):
            for j in range(i + 1, c + k):
                A[i, j] = A[j, i] = 1.0
    b0, b1 = k - 1, k          # clique1 end -> bridge start
    cur = b1
    chain = [b0]
    for _ in range(n - 2 * k + 1):
        chain.append(cur)
        cur += 1
    chain.append(2 * k + 24)
    for a, b in zip(chain, chain[1:]):
        A[a, b] = A[b, a] = 1.0
    return A


def complete_adj(n: int) -> np.ndarray:
    A = np.ones((n, n)) - np.eye(n)
    return A


def bipartite_adj(n: int) -> np.ndarray:
    h = n // 2
    A = np.zeros((n, n))
    A[:h, h:] = 1.0
    A[h:, :h] = 1.0
    return A


def new_battery() -> dict[str, np.ndarray]:
    return {
        "tree": tree_adj(100),
        "star": star_adj(100),
        "cycle": cycle_adj(100),
        "ladder": ladder_adj(100),
        "barbell": barbell_adj(100),
        "complete": complete_adj(60),
        "bipartite": bipartite_adj(100),
        "grid_elong": grid_2d(5, 20),
        "torus_elong": torus(5, 20),
        "random8": circulant(100, [1, 2, 3, 4]),   # degree 8; the
        # pairing model fails at k>=6, n=100 (exp73's note) — the
        # deterministic degree-8 circulant is the dense case
        "path200": path(200),
        "scale_free200": scale_free(200, seed=13),
    }


MULTI = AnatomySpec(
    zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
           Zone(f0=0.30, f1=0.45, voltage=-30.0, name="z1"),
           Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
    amputate_plane="trunk", spec_name="ms-multi", somatic_latch=False)
BELOW = AnatomySpec(
    zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
           Zone(f0=0.30, f1=0.45, voltage=-59.0, name="z1"),
           Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
    amputate_plane="trunk", spec_name="ms-below", somatic_latch=False)


def execute_two_source_n(spec: AnatomySpec, adjacency: np.ndarray,
                         seed: int, with_canon: bool = True,
                         op: dict | None = None,
                         anchor: list | None = None,
                         frontier_mode: str = "zones",
                         return_trace: bool = False,
                         return_state: bool = False) -> dict:
    """exp90's execute_two_source generalized over n (and, since
    exp95, over the operating point — default STAR, which is what
    exp94's deposited results used; since exp96, an optional
    settle-anchor: [(cell, voltage), ...] clamped through the 15h
    settle and released 1h before the read — the exp75-77 slow-anchor
    theorem applied to the reader; since exp97, the blastema-frontier
    enumeration mode).

    frontier_mode="zones" (default — BIT-EXACT with every deposited
    run) enumerates wound-frontier candidates over the zone union
    only. frontier_mode="walk" enumerates over the whole amputation
    range: on topologies whose amputated region is laterally
    DISCONNECTED (the star — every spoke's only neighbor is the
    intact hub), every amputated cell borders intact tissue and is a
    wound-frontier cell; the zones mode leaves the inter-zone gaps
    amputated and NEVER rebuilt (the exp97 probe: ~32 wound cells at
    blastema -40 carry ~93% of the star's 8.5 mV floor — an executor
    coverage artifact, not an architecture boundary)."""
    n = adjacency.shape[0]
    _op = op if op is not None else STAR
    gamma, mu = _op["gamma"], _op["mu"]
    dt = star_dt(gamma, float(adjacency.sum(axis=1).max()))
    canon = labeling_bfs_n(adjacency)
    target = spec_target_n(spec, canon, n)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(canon)
    c.write_spec_layer(target)
    if not with_canon and hasattr(c, "phi_spec_canon"):
        del c.phi_spec_canon
    prog = compile_anatomy(spec, n=n)
    if prog.rejected:
        return {"program_verified": False, "rejected": prog.rejected,
                "err_vs_target": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    if reg_idx:
        reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
        region_set = set(reg_walk)
        c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
        wound_center = float(np.mean(c.theta[reg_walk]))
        steps_per_cell = 8
        parent_of: dict[int, int] = {}
        frontier: list[int] = []
        # exp97: the blastema frontier is the amputated cells ADJACENT
        # TO INTACT TISSUE — on a connected region that is the zone
        # union's boundary cells (the old enumeration, bit-exact); on
        # a disconnected region it is every amputated cell.
        frontier_domain = (reg_idx if frontier_mode == "zones"
                           else reg_walk)
        for i in frontier_domain:
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
        order = [(i, parent_of[i]) for i in frontier]
        queue = list(frontier)
        while queue:
            i = queue.pop(0)
            for j in np.where(c.A[i] > 0)[0]:
                if int(j) in region_set and int(j) not in visited:
                    visited.add(int(j))
                    parent_of[int(j)] = int(i)
                    order.append((int(j), int(i)))
                    queue.append(int(j))
        for i, src in order:
            for _ in range(steps_per_cell):
                c.step(dt)
            canon_src = getattr(c, "phi_spec_canon", None) \
                if with_canon else None
            if c.phi_spec[i] >= NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
            elif canon_src is not None:
                # the canon read's gate is the SOURCE's existence (the
                # attribute), never the value's sign — phi_spec_canon
                # holds NEGATIVE voltages; a value>0 guard silently
                # degrades every below-line cell to the wound-state
                # chain read (the exp89 UC-G5 failure mode, owned
                # in-run)
                theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
            c.theta[i] = theta_new
            c.V[i] = theta_new
    trace: dict = {}
    if return_trace:
        trace["post_walk_err"] = round(c.pattern_error(target), 2)
    if anchor:
        for cell_i, v in anchor:
            c.clamp(slice(cell_i, cell_i + 1), v)
    c.run(15.0, dt=dt)
    if anchor:
        c.release_clamps()
        c.run(1.0, dt=dt)
    per_zone = {}
    ok_all = True
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zmean = float(np.mean(c.V[i0:i1]))
        ok = abs(zmean - z.voltage) <= ERR_BAR
        per_zone[z.name] = {"mean": round(zmean, 1), "ok": bool(ok)}
        ok_all &= ok
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    out = {"program_verified": bool(ok_all), "per_zone": per_zone,
           "err_vs_target": round(err, 2)}
    if return_trace:
        trace["post_settle_err"] = round(c.pattern_error(target), 2)
        out["trace"] = trace
    if return_state:
        out["final_state"] = {"V": c.V.tolist(),
                              "target": target.tolist()}
    return out


def labeling_bfs_n(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    order = bfs_order(A)
    lbl = np.full(n, TRUNK_V)
    lbl[order[:n // 4]] = HEAD_V
    return lbl


def spec_target_n(spec: AnatomySpec, canon: np.ndarray,
                  n: int) -> np.ndarray:
    target = canon.copy()
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    return target


def main() -> dict:
    print("=== exp94: the multi-zone regen scale-up ===\n")

    battery = new_battery()
    r5 = {}
    for name, adj in battery.items():
        chk = substrate_partition_check(MULTI, adj)
        r5[name] = chk["substrate_compilable"]
    print(f"  R5 partition on the new battery: {r5}\n")

    results: dict[str, dict] = {}
    for name, adj in battery.items():
        multi = [execute_two_source_n(MULTI, adj, s) for s in (1, 2, 3)]
        below = [execute_two_source_n(BELOW, adj, s) for s in (1, 2)]
        nocanon = [execute_two_source_n(MULTI, adj, s, with_canon=False)
                   for s in (1, 2)]
        results[name] = {
            "multi_rate": round(float(np.mean(
                [r["program_verified"] for r in multi])), 3),
            "multi_err": round(float(np.nanmean(
                [r["err_vs_target"] for r in multi])), 2),
            "below_rate": round(float(np.mean(
                [r["program_verified"] for r in below])), 3),
            "nocanon_rate": round(float(np.mean(
                [r["program_verified"] for r in nocanon])), 3),
        }
        print(f"    {name:14s} multi {results[name]['multi_rate']:.2f} "
              f"(err {results[name]['multi_err']}) | below "
              f"{results[name]['below_rate']:.2f} | no-canon "
              f"{results[name]['nocanon_rate']:.2f}")

    n_names = list(battery)
    ms_g1 = sum(int(results[n]["multi_rate"] >= 2 / 3)
                for n in n_names) >= 9
    ms_g2 = sum(int(results[n]["below_rate"] <= 1 / 3)
                for n in n_names) >= 8
    ms_g3 = sum(int(results[n]["nocanon_rate"] <= 1 / 3)
                for n in n_names) >= 8
    ms_g4 = (results["path200"]["multi_rate"] >= 2 / 3
             or results["scale_free200"]["multi_rate"] >= 2 / 3)
    print(f"\n  MS-G1 scale-up: "
          f"{sum(int(results[n]['multi_rate'] >= 2/3) for n in n_names)}"
          f"/12 verify -> {'PASS' if ms_g1 else 'REFUTED'}")
    print(f"  MS-G2 no backdoor: "
          f"{sum(int(results[n]['below_rate'] <= 1/3) for n in n_names)}"
          f"/12 below-line fail -> {'PASS' if ms_g2 else 'REFUTED'}")
    print(f"  MS-G3 canon load-bearing: "
          f"{sum(int(results[n]['nocanon_rate'] <= 1/3) for n in n_names)}"
          f"/12 no-canon fail -> {'PASS' if ms_g3 else 'REFUTED'}")
    print(f"  MS-G4 size scale: path200 "
          f"{results['path200']['multi_rate']:.2f}, scale_free200 "
          f"{results['scale_free200']['multi_rate']:.2f} -> "
          f"{'PASS' if ms_g4 else 'REFUTED'}")

    npass = sum([ms_g1, ms_g2, ms_g3, ms_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    out = {
        "exp": "exp94_multizone_scale",
        "r5_partition": r5,
        "results": results,
        "criteria": {
            "MS_G1_scale_up": bool(ms_g1),
            "MS_G2_no_backdoor": bool(ms_g2),
            "MS_G3_canon_load_bearing": bool(ms_g3),
            "MS_G4_size_scale": bool(ms_g4),
        },
        "notes": (
            "exp90's two-source read scaled to 12 new topologies "
            "(trees, hub, cycle, ladder, barbell, complete, "
            "bipartite, elongated grids, k=8 random, n=200 size "
            "scale). The executor is exp90's generalized over n; "
            "the multi program verbatim; the star operating point; "
            "3 seeds multi / 2 seeds controls."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
