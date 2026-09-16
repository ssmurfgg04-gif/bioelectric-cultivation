#!/usr/bin/env python3
"""exp116 — THE MU-PHASE LOCALIZATION (ledger L96's registration:
the middle band's mu cut is BINARY-DEEP — theta diffusion must be
fully off or identity does not hold — and walk speed buys gamma,
never mu. The mu channel is a contamination channel (the intact/
wound field's identity bleeding into the rebuilt span through
theta diffusion); WHICH PHASE the contamination lives in is this
experiment's question. At spc=0 the walk has no steps, so the
mu-active phases are the WINDOW (24 h, pre-amputation) and the
SETTLE (15 h, post-commit).)

THE DESIGN (a phase 2x2 at the default gamma, on the six MU0
members, spc=0, 3 seeds — the frozen-walk protocol):
  oo   mu = 0 in window AND settle          (the (1, 0) control —
                                             verifies 6/6 per
                                             exp115)
  w1s1 mu = 0.015 in window AND settle      (the (1, 0.015) full
                                             default — the failing
                                             cell)
  w1s0 mu = 0.015 in WINDOW only            (window contamination
                                             only)
  w0s1 mu = 0.015 in SETTLE only            (settle contamination
                                             only)

PRE-REGISTERED GATES:

  MP-G1  (clean phase attribution) ONE single-phase arm refuses
         (rate < 2/3) across >= 5/6 members while the OTHER
         single-phase arm verifies (rate >= 2/3) across >= 5/6 —
         the sensitive phase is NAMED. If both refuse or both
         verify, the contamination is not phase-localized (honest
         deposit, the 2x2 says "both" or "neither").
  MP-G2  (corner anchoring) oo verifies >= 5/6 and w1s1 refuses
         >= 5/6 — the 2x2's corners reproduce the deposited cells
         so the attribution stands on something.
  MP-G3  (no runaway) every arm's mean err < 10 mV — sanity.

THE PREDICTION SPACE (pre-registered): settle-sensitive (w0s1
refuses, w1s0 verifies) — the post-commit diffusion bleeds the
committed -30 zones into the intact field and the intact -50/-20
back into the span; window-sensitive (w1s0 refuses, w0s1 verifies)
— the pre-amputation diffusion homogenizes the canon field the
intact cells carry into the settle; both (each phase contributes)
— the gate says so.

RUN: 6 members x 4 arms x 3 seeds = 72 runs. Serial, BLAS pinned.
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
from cultivation.substrate.graph import GraphCollective, grid_2d, path
from experiments.exp68_coherence_search import torus
from experiments.exp73_active_renormalization import (
    bfs_order, circulant,
)
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import (
    MULTI, barbell_adj, bipartite_adj, complete_adj, cycle_adj,
    ladder_adj, scale_free, star_adj, tree_adj,
)
from experiments.exp100_reader_price_map import make_battery
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp116_mu_phase_localization.json")

SEEDS3 = (1, 2, 3)
ERR_BAR = 6.0
DEFAULT_MU = 0.015
MU0_MEMBERS = ("torus", "torus_elong", "random3", "random8",
               "scale_free", "scale_free200")


def build_battery() -> dict:
    battery = dict(make_battery())
    battery.update({
        "tree": tree_adj(100), "star": star_adj(100),
        "cycle": cycle_adj(100),
        "ladder": ladder_adj(100), "barbell": barbell_adj(100),
        "complete": complete_adj(60), "bipartite": bipartite_adj(100),
        "grid_elong": grid_2d(5, 20), "torus_elong": torus(5, 20),
        "random8": circulant(100, [1, 2, 3, 4]),
        "grid2d": grid_2d(10, 10), "torus": torus(10, 10),
        "scale_free": scale_free(100, seed=11),
        "scale_free200": scale_free(200, seed=13),
        "path200": path(200),
    })
    return battery


def run_phased(adj, seed: int, mu_window: float,
               mu_settle: float) -> dict:
    """The spc=0 walk executor (exp110/111 instrument) with the mu
    rate set independently for the window and the settle. gamma 1,
    default mu as the ON value."""
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
                        mu_theta=mu_window)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return {"program_verified": False, "err": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(24.0, dt=dt)
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
    for i, src in order2:      # spc = 0: no inter-commit steps
        canon_src = getattr(c, "phi_spec_canon", None)
        if c.phi_spec[i] >= NEURAL_SPEC_MIN:
            theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
        elif canon_src is not None:
            theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
        else:
            theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    c.mu = mu_settle
    c.run(15.0, dt=dt)
    ok_all = True
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        ok_all &= abs(float(np.mean(c.V[i0:i1])) - z.voltage) <= ERR_BAR
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    return {"program_verified": bool(ok_all), "err": round(err, 2)}


def arm_stats(adj, mw, ms) -> dict:
    runs = [run_phased(adj, s, mw, ms) for s in SEEDS3]
    return {"rate": round(float(np.mean(
        [x["program_verified"] for x in runs])), 3),
        "err": round(float(np.mean([x["err"] for x in runs])), 2)}


def main() -> dict:
    print("=== exp116: the mu-phase localization ===\n")

    battery = build_battery()
    ARMS = {"oo": (0.0, 0.0), "w1s1": (DEFAULT_MU, DEFAULT_MU),
            "w1s0": (DEFAULT_MU, 0.0), "w0s1": (0.0, DEFAULT_MU)}
    out: dict = {}
    for name in MU0_MEMBERS:
        adj = battery[name]
        for arm, (mw, ms) in ARMS.items():
            st = arm_stats(adj, mw, ms)
            out[f"{name}_{arm}"] = st
            print(f"    {name:13s} {arm:5s}  {st['rate']:.2f}"
                  f"/{st['err']:5.2f}")

    def refused(arm):
        return sum(out[f"{n}_{arm}"]["rate"] < 2 / 3
                   for n in MU0_MEMBERS)

    def verified(arm):
        return sum(out[f"{n}_{arm}"]["rate"] >= 2 / 3
                   for n in MU0_MEMBERS)

    verdict = ("both phases contribute (no clean attribution)")
    mp_g1 = False
    if (refused("w0s1") >= 5 and verified("w1s0") >= 5):
        verdict = "SETTLE-sensitive (settle mu alone kills identity)"
        mp_g1 = True
    elif (refused("w1s0") >= 5 and verified("w0s1") >= 5):
        verdict = "WINDOW-sensitive (window mu alone kills identity)"
        mp_g1 = True
    mp_g2 = (verified("oo") >= 5 and refused("w1s1") >= 5)
    mp_g3 = all(out[k]["err"] < 10 for k in out)

    print(f"\n  refused: oo {refused('oo')}/6, w1s1 "
          f"{refused('w1s1')}/6, w1s0 {refused('w1s0')}/6, w0s1 "
          f"{refused('w0s1')}/6")
    print(f"\n  MP-G1 clean phase attribution: "
          f"{'PASS' if mp_g1 else 'REFUTED'} — {verdict}")
    print(f"  MP-G2 corner anchoring: "
          f"{'PASS' if mp_g2 else 'REFUTED'}")
    print(f"  MP-G3 no runaway: {'PASS' if mp_g3 else 'REFUTED'}")

    npass = sum([mp_g1, mp_g2, mp_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp116_mu_phase_localization",
        "arms": out,
        "verdict": verdict,
        "criteria": {
            "MP_G1_phase_attribution": bool(mp_g1),
            "MP_G2_corner_anchoring": bool(mp_g2),
            "MP_G3_no_runaway": bool(mp_g3),
        },
        "notes": (
            "The mu channel's contamination phase localized by a "
            "2x2 (window-mu x settle-mu) at default gamma on the "
            "six MU0 members under the frozen walk."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
