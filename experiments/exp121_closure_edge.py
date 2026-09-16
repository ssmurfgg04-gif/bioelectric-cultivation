#!/usr/bin/env python3
"""exp121 — THE CLOSURE EDGE (ledger L101's registration: exp120
found the stack's temporal vulnerability map is a per-substrate
STEP — grid2d/path invulnerable, the torus breaking only when the
sustained blockade lands at/after ~48 h (late walk) — with the
edge moving 48 -> 36 h under doubled commitment diffusion. Three
follow-ups, one experiment.)

PART A — THE BREAK MECHANISM: at the torus's onset-48 edge, WHAT
exceeds the 6.0 bar? Cell-class RMS decomposition (zone/gap/intact)
of the blockaded final read vs the unblocked control, plus the raw
err distribution over seeds — names whether the break is the
committed span drifting, the intact field, or the gap/canon cells.

PART B — THE CORRECTED REFIT: the record's decreasing kernel is
P(success | onset) = 1 - P(break); refit the decreasing logistic
L/(1+exp((t-tc)/kappa)) to 1 - P(break) per arm and deposit the
edge parameters honestly (the torus's step may fit poorly — the
Brier-ish residual is deposited; a step is a kappa -> 0 limit).

PART C — THE MU EDGE-SHIFT LADDER: torus only, mu in
{0.015, 0.03, 0.06}, 8 onsets x 8 seeds: is the edge position
monotone in mu? The edge is defined as the first onset (in the
sweep grid) where P(break) >= 0.5 — coarse but deposited with the
full curves.

PRE-REGISTERED GATES:

  CE-G1  (break localization) at the torus edge (onset 48), the
         blockaded read's error decomposition is deposited and the
         dominant class NAMED (measurement gate — names, never
         fails).
  CE-G2  (monotone edge shift) the torus edge position (first
         P(break) >= 0.5 onset) is non-increasing in mu across
         {0.015, 0.03, 0.06} — the commitment-diffusion dial moves
         closure monotonically.
  CE-G3  (the path/grid2d null holds at double resolution) the
         invulnerable substrates stay invulnerable at onsets
         {42, 54, 66} (finer around the torus edge): P(break) = 0
         at all three — the substrate specificity is not a grid
         artifact of the coarse onset sweep.

RUN: torus 3 mu arms x 8 onsets x 8 seeds + grid2d/path 3 onsets x
8 seeds + the edge decompositions. Serial, BLAS pinned.
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
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI, ERR_BAR
from experiments.exp112_walk_speed_ladder import build_battery
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp121_closure_edge.json")

SEEDS = tuple(range(1, 9))
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)
WINDOW_H = 24.0
SETTLE_H = 15.0
BLOCK_SCALE = 0.05


def run_err(adj, seed: int, onset: float, mu: float,
            block: bool = True) -> dict:
    """exp120's run_kernel returning the error + class decomposition
    instead of a boolean (the blockade semantic verbatim)."""
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
    from cultivation.substrate.graph import GraphCollective
    c = GraphCollective(adjacency=adj, seed=seed, gamma=1.0,
                        mu_theta=mu)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return {"err": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def maybe_block(t):
        if block and t >= onset:
            c.block_gap_junctions(BLOCK_SCALE)

    t0 = 0.0
    for _ in range(int(round(WINDOW_H / dt))):
        t0 += dt
        maybe_block(t0)
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
            maybe_block(t0)
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
    walk_hours = 0.8 * n * 0.73
    T_END = WINDOW_H + walk_hours + SETTLE_H
    if onset <= WINDOW_H + walk_hours:
        rest = SETTLE_H
    else:
        rest = max(0.0, T_END - onset)
    for _ in range(int(round(rest / dt))):
        t0 += dt
        maybe_block(t0)
        c.step(dt)
    err = float(c.pattern_error(target))
    zone = np.zeros(n, bool)
    a0 = int(round(MULTI.zones[0].f0 * n))
    a1 = int(round(MULTI.zones[-1].f1 * n))
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zone[i0:i1] = True
    gap = np.zeros(n, bool)
    gap[a0:a1] = True
    gap &= ~zone
    intact = ~(zone | gap)

    def rms(m):
        d = c.V[m] - target[m]
        return round(float(np.sqrt(np.mean(d * d))), 2)

    return {"err": round(err, 2), "zone_rms": rms(zone),
            "gap_rms": rms(gap), "intact_rms": rms(intact)}


def edge_position(ps, onsets):
    for t, p in zip(onsets, ps):
        if p >= 0.5:
            return t
    return None


def main() -> dict:
    print("=== exp121: the closure edge ===\n")

    battery = build_battery()
    torus = battery["torus"]
    out: dict = {"mu_ladder": {}, "fine_null": {},
                 "break_decomp": {}, "refit": {}}

    # PART C: the mu edge-shift ladder
    curves = {}
    for mu in (0.015, 0.03, 0.06):
        ps = []
        for onset in ONSETS:
            breaks = [run_err(torus, s, onset, mu)["err"] >= ERR_BAR
                      for s in SEEDS]
            p = float(np.mean(breaks))
            ps.append(p)
            out["mu_ladder"][f"mu{mu:g}_t{onset:g}"] = round(p, 3)
        curves[mu] = ps
        print(f"    torus mu={mu:g}  P(break): "
              f"{[round(x, 2) for x in ps]}")
    edges = {mu: edge_position(ps, ONSETS)
             for mu, ps in curves.items()}
    e_vals = [edges[m] if edges[m] is not None else 10 ** 9
              for m in (0.015, 0.03, 0.06)]
    ce_g2 = all(e_vals[i] >= e_vals[i + 1]
                for i in range(len(e_vals) - 1))
    print(f"    edges (first P>=0.5): {edges}")

    # PART A: the break mechanism at onset 48
    decomp = {"blocked": [], "control": []}
    for s in SEEDS:
        decomp["blocked"].append(run_err(torus, s, 48.0, 0.015))
        decomp["control"].append(run_err(torus, s, 10 ** 6, 0.015,
                                         block=False))

    def mean_class(runs, k):
        return round(float(np.mean([r[k] for r in runs])), 2)

    for label, runs in decomp.items():
        out["break_decomp"][label] = {
            "err": mean_class(runs, "err"),
            "zone_rms": mean_class(runs, "zone_rms"),
            "gap_rms": mean_class(runs, "gap_rms"),
            "intact_rms": mean_class(runs, "intact_rms"),
            "break_rate": round(float(np.mean(
                [r["err"] >= ERR_BAR for r in runs])), 3),
        }
        print(f"    {label:8s} err {out['break_decomp'][label]['err']}"
              f"  zone {out['break_decomp'][label]['zone_rms']}"
              f"  gap {out['break_decomp'][label]['gap_rms']}"
              f"  intact {out['break_decomp'][label]['intact_rms']}")
    b = out["break_decomp"]["blocked"]
    dom = max(("zone", b["zone_rms"]), ("gap", b["gap_rms"]),
              ("intact", b["intact_rms"]), key=lambda x: x[1])
    ce_g1 = True  # measurement gate
    print(f"    dominant class at the edge: {dom[0]} ({dom[1]})")

    # PART B: corrected refit (decreasing success kernel)
    from scipy.optimize import curve_fit
    for mu, ps in curves.items():
        succ = 1.0 - np.array(ps)
        try:
            popt, _ = curve_fit(
                lambda t, L, tc, k: L / (1.0 + np.exp((t - tc) / k)),
                np.array(ONSETS, float), succ,
                p0=[1.0, 60.0, 12.0], maxfev=20000,
                bounds=([0.1, -100.0, 0.1], [1.0, 300.0, 200.0]))
            out["refit"][f"mu{mu:g}"] = {
                "L": round(float(popt[0]), 3),
                "tc": round(float(popt[1]), 1),
                "kappa": round(float(popt[2]), 1)}
        except Exception as e:
            out["refit"][f"mu{mu:g}"] = {"fit_failed": str(e)[:60]}
        print(f"    refit mu={mu:g}: {out['refit'][f'mu{mu:g}']}")

    # CE-G3: the null substrates at fine onsets
    fine = (42.0, 54.0, 66.0)
    for name in ("grid2d", "path"):
        adj = battery[name]
        ps = []
        for onset in fine:
            br = [run_err(adj, s, onset, 0.015)["err"] >= ERR_BAR
                  for s in SEEDS]
            ps.append(round(float(np.mean(br)), 3))
        out["fine_null"][name] = ps
        print(f"    {name} fine P(break) {ps}")
    ce_g3 = all(max(v) == 0.0 for v in out["fine_null"].values())

    print(f"\n  CE-G1 break localization: dominant = {dom[0]} "
          f"({dom[1]} mV)")
    print(f"  CE-G2 monotone edge shift: "
          f"{'PASS' if ce_g2 else 'REFUTED'} ({edges})")
    print(f"  CE-G3 fine-grid null holds: "
          f"{'PASS' if ce_g3 else 'REFUTED'}")

    npass = sum([ce_g2, ce_g3])
    print(f"\n  === {npass}/2 decision gates PASS "
          f"(CE-G1 names the class) ===")

    result = {
        "exp": "exp121_closure_edge",
        "arms": out,
        "edges": {str(k): v for k, v in edges.items()},
        "dominant_class": {"name": dom[0], "rms": dom[1]},
        "criteria": {
            "CE_G1_break_localization": dom[0],
            "CE_G2_monotone_edge_shift": bool(ce_g2),
            "CE_G3_fine_null_holds": bool(ce_g3),
        },
        "notes": (
            "The torus's closure edge: class decomposition at "
            "onset 48 (blockade vs control), the corrected "
            "decreasing-kernel refit (1 - P(break)), and the mu "
            "edge-shift ladder {0.015, 0.03, 0.06}; the null "
            "substrates re-checked at fine onsets."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
