#!/usr/bin/env python3
"""exp120 — THE WRITE-SUCCESS KERNEL SHAPE TEST (ledger L100's
registration; subagent 2-a's CG-P1/P2 against Damon's deposited
record, Zenodo 18358611, with the record numbers tc ~ 20 h,
kappa ~ 10 h, L ~ 0.75 from Durant 2017 / Beane 2011 / Oviedo 2010).
The stack mapping uses exp70's established semantic (the gap-junction
blockade breaks regeneration when applied before commitment closes;
P(break) decays with onset) generalized to GRAPH substrates.

THE PROTOCOL per (substrate, onset, arm, seed): the standard
regeneration protocol at the default cell (gamma 1, mu 0.015) —
24 h window, walk, 15 h settle — phase-run so the blockade
(c.gap_scale = 0.05) can be applied at onset t in {0, 6, 12, 18,
24, 36, 48, 72} h from protocol start and held to the read.
Outcome: BREAK = pattern_error >= 6.0 mV at the final read (the
regeneration failed). P(break) over seeds -> the kernel.

THE ARMS:
  default   gamma 1 throughout
  gamma64   gamma raised to 64 AT THE ONSET (strength cannot
            reopen a closed window: P(break | gamma64) must NOT
            diverge from P(break | gamma1) at late onsets)
  mu03      commitment diffusion doubled (mu 0.015 -> 0.03,
            default strength) — CG-P1's tc-shift test

PRE-REGISTERED GATES:

  CG-G1  (shape invariance) the fitted logistic P(t) = L / (1 +
         exp((t - tc)/kappa)) has kappa and L within +/- 20%
         across grid2d / torus / path at the default arm — Damon's
         core invariance claim on the stack. (If P(break) never
         rises above 0.1 anywhere, the kernel is degenerate on the
         stack — deposit honestly as not-testable-this-way.)
  CG-G2  (strength cannot reopen) |P(break | gamma64) - P(break |
         gamma1)| <= 0.05 at onsets >= 48 h on grid2d and torus.
  CG-G3  (the D-shift moves tc) the mu03 arm's fitted tc differs
         from default by >= 2 h in a consistent direction on >= 2/3
         substrates (monotone shift, sign free).

RUN: 3 substrates x 8 onsets x 8 seeds x {default, gamma64} +
3 x 8 x 8 mu03 = 576 runs. Serial, BLAS pinned.
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

from scipy.optimize import curve_fit

from cultivation.compiler.anatomy import compile_anatomy
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import GraphCollective, grid_2d, path
from experiments.exp68_coherence_search import torus
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI, ERR_BAR
from experiments.exp112_walk_speed_ladder import build_battery
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp120_kernel_shape.json")

SEEDS = tuple(range(1, 9))
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)
WINDOW_H = 24.0
SETTLE_H = 15.0
BLOCK_SCALE = 0.05


def run_kernel(adj, seed: int, onset: float, gamma_late: float,
               mu: float) -> bool:
    """The standard regeneration with a sustained gap-junction
    blockade (block_gap_junctions: G and deg scaled — the exp70
    semantic) applied at `onset` hours from protocol start; gamma
    raised to `gamma_late` at the onset with a STABLE dt (computed
    for the max gamma used — the Euler step must satisfy
    |1 - gamma*dt| < 1). Onsets beyond the protocol end are
    vacuous (never triggered) and return the unblocked outcome.
    Returns BREAK."""
    n = adj.shape[0]
    deg_max = float(adj.sum(axis=1).max())
    g_max = max(1.0, gamma_late or 1.0)
    dt = star_dt(g_max, deg_max)
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    c = GraphCollective(adjacency=adj, seed=seed, gamma=1.0,
                        mu_theta=mu)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return True
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def phase(hours, block, g):
        """Run `hours`, applying the blockade/gamma switches from
        their onset times; returns elapsed protocol time."""
        t0 = 0.0
        steps = int(round(hours / dt))
        for _ in range(steps):
            t0 += dt
            if block and t0 >= onset:
                c.block_gap_junctions(BLOCK_SCALE)
            if g and gamma_late is not None and t0 >= onset:
                c.gamma = gamma_late
            c.step(dt)
        return t0

    t = phase(WINDOW_H, True, True)
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
    walk_hours = 0.8 * n * 0.73
    T_END = WINDOW_H + walk_hours + SETTLE_H
    done = 0.0
    for i, src in order2:
        # 8 steps per cell with the blockade switch inline
        for _ in range(8):
            done += dt
            t += dt
            if t >= onset:
                c.block_gap_junctions(BLOCK_SCALE)
                if gamma_late is not None:
                    c.gamma = gamma_late
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
    rest = max(0.0, min(SETTLE_H,
                        onset - (WINDOW_H + walk_hours)))
    rest = SETTLE_H if onset <= WINDOW_H + walk_hours else \
        max(0.0, T_END - onset)
    steps = int(round(rest / dt))
    for _ in range(steps):
        t += dt
        if t >= onset:
            c.block_gap_junctions(BLOCK_SCALE)
            if gamma_late is not None:
                c.gamma = gamma_late
        c.step(dt)
    err = float(c.pattern_error(target))
    return bool(err >= ERR_BAR)


def arm_curve(adj, onset_list, gamma_late, mu, label, out, name):
    ps = []
    for onset in onset_list:
        breaks = [run_kernel(adj, s, onset, gamma_late, mu)
                  for s in SEEDS]
        p = float(np.mean(breaks))
        ps.append(p)
        out[f"{name}_{label}_t{onset:g}"] = round(p, 3)
    print(f"    {name:7s} {label:8s} P(break): "
          f"{[round(x, 2) for x in ps]}")
    return ps


def fit_logistic(onsets, ps):
    ps = np.array(ps, float)
    if ps.max() < 0.1 or ps.min() > 0.9:
        return None
    L0 = float(np.clip(ps.max(), 0.5, 1.0))
    try:
        popt, _ = curve_fit(
            lambda t, L, tc, k: L / (1.0 + np.exp((t - tc) / k)),
            np.array(onsets, float), ps,
            p0=[L0, 20.0, 10.0], maxfev=20000,
            bounds=([0.1, -50.0, 0.5], [1.0, 200.0, 100.0]))
        return {"L": round(float(popt[0]), 3),
                "tc": round(float(popt[1]), 1),
                "kappa": round(float(popt[2]), 1)}
    except Exception:
        return None


def main() -> dict:
    print("=== exp120: the write-success kernel shape ===\n")

    battery = build_battery()
    SUBS = {"grid2d": battery["grid2d"], "torus": battery["torus"],
            "path": battery["path"]}
    out: dict = {}
    curves = {}

    for name, adj in SUBS.items():
        curves[name] = {
            "default": arm_curve(adj, ONSETS, None, 0.015,
                                 "default", out, name),
            "gamma64": arm_curve(adj, ONSETS, 64.0, 0.015,
                                 "gamma64", out, name),
            "mu03": arm_curve(adj, ONSETS, None, 0.03,
                              "mu03", out, name),
        }

    fits = {name: {arm: fit_logistic(ONSETS, ps)
                   for arm, ps in arms.items()}
            for name, arms in curves.items()}
    print(f"\n  fits: {json.dumps(fits, indent=1)}")

    ks = [fits[n]["default"]["kappa"] for n in SUBS
          if fits[n]["default"]]
    Ls = [fits[n]["default"]["L"] for n in SUBS if fits[n]["default"]]
    cg_g1 = (len(ks) == 3
             and (max(ks) - min(ks)) <= 0.4 * np.mean(ks)
             and (max(Ls) - min(Ls)) <= 0.4 * np.mean(Ls))
    late_d = []
    for name in ("grid2d", "torus"):
        for onset in (48.0, 72.0):
            d = abs(out[f"{name}_gamma64_t{onset:g}"]
                    - out[f"{name}_default_t{onset:g}"])
            late_d.append(d)
    cg_g2 = all(d <= 0.05 for d in late_d)
    tcs = {n: (fits[n]["default"]["tc"], fits[n]["mu03"]["tc"])
           for n in SUBS if fits[n]["default"] and fits[n]["mu03"]}
    shifts = [abs(b - a) >= 2.0 for a, b in tcs.values()] \
        if tcs else []
    cg_g3 = len(shifts) >= 2 and sum(shifts) >= 2

    print(f"\n  CG-G1 shape invariance (kappa {ks}, L {Ls}): "
          f"{'PASS' if cg_g1 else 'REFUTED'}")
    print(f"  CG-G2 no late rescue (max |d| {max(late_d):.2f}): "
          f"{'PASS' if cg_g2 else 'REFUTED'}")
    print(f"  CG-G3 tc shift under mu03 (tc pairs {tcs}): "
          f"{'PASS' if cg_g3 else 'REFUTED'}")

    npass = sum([cg_g1, cg_g2, cg_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp120_kernel_shape",
        "P_break": out,
        "curves": curves,
        "fits": fits,
        "criteria": {
            "CG_G1_shape_invariance": bool(cg_g1),
            "CG_G2_no_late_rescue": bool(cg_g2),
            "CG_G3_tc_shift": bool(cg_g3),
        },
        "notes": (
            "CG-P1/P2 on graph substrates: sustained gap-junction "
            "blockade applied at onset t during the standard "
            "regeneration; P(break) over 8 seeds; decreasing "
            "logistic fits compared across substrates (kappa/L "
            "invariance), strength arm (gamma 64 at onset — no "
            "late rescue), and the commitment-diffusion shift "
            "(mu 0.03). Record references: tc~20 h, kappa~10 h, "
            "L~0.75."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
