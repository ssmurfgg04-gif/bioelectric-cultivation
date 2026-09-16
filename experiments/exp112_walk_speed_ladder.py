#!/usr/bin/env python3
"""exp112 — THE WALK-SPEED LADDER (ledger L92's registration: the
frozen-walk operating point priced the torus's trend away and
INVERTED it — walk_speed enters the compiler's price map as a
candidate dial. The open question: how much of the dial BUDGET does
walk speed buy back across the price map's expensive members? If
slower walks (spc 8 -> 2 -> 0) let substrates verify at strictly
cheaper cells, the two-dial price tags were partly WALK TAX —
identity erasure during the rebuild — not coupling geometry.)

THE INSTRUMENT (exp100's classes table is the adopted map; the
exp110/111 executor with a steps_per_cell dial):
  adopted8    each expensive member at its exp100 adopted cell,
              spc=8, 3 seeds — the reference (must reproduce the
              exp100 deposit within seed noise)
  adopted0    the SAME cell at spc=0, 3 seeds — the no-harm check
  down0       the ONE-DIAL-DOWN descent at spc=0, 3 seeds per rung:
              V_PRICED members (adopted (G, 0.015)): gamma in
              {G/4, G/2} at mu 0.015;
              TWO_DIAL members (adopted (G, 0)): (G/4, 0), (G/2, 0)

THE MEMBERS (15, from exp100's classes): star (2, .015); tree,
grid2d, grid_elong (64, .015); ladder, random6 (32, .015); torus,
torus_elong, random3, random8, scale_free, scale_free200 (4, 0);
barbell (16, 0); bipartite, complete (32, 0). The four DEFAULT
members are controls-by-omission (nothing to buy back).

PRE-REGISTERED GATES:

  WS-G1  (buy-back) at least 3 of the 15 expensive members VERIFY
         (rate >= 2/3, err < 6.0) at a strictly cheaper cell under
         spc=0 — the dial budget releases.
  WS-G2  (reference reproduction) every member verifies at its
         adopted cell under spc=8 with err within +/- 0.75 mV of
         the exp100 deposit — the harness is the same one that
         built the map.
  WS-G3  (no harm) no member that verifies at its adopted cell
         under spc=8 loses verification at that cell under spc=0 —
         speed is a free dial at the adopted cell.

THE DEPOSIT: per member, the minimal verifying cell under spc=0 and
the dial saved (gamma ratio or the (G, 0) -> (G/2, 0) step) — the
walk_speed-repriced top of the price map. exp113 derives from the
buy-back pattern: if the two-dial members drop to one-dial or
default cells, the R5' price oracle gains walk_speed as a third
predictor; if the dense extremes hold their price, the boundary
term was measuring coupling geometry after all and the walk tax was
torus-specific.

RUN: 15 members x (3 + 3 + 6) runs = 180. Serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp112_walk_speed_ladder.json")

SEEDS3 = (1, 2, 3)
ERR_BAR = 6.0
DEFAULT_MU = 0.015

# member -> (adopted (gamma, mu), down-rungs [(g, mu), ...])
MEMBERS = {
    "star": ((2.0, DEFAULT_MU), [(0.5, DEFAULT_MU),
                                 (1.0, DEFAULT_MU)]),
    "tree": ((64.0, DEFAULT_MU), [(16.0, DEFAULT_MU),
                                  (32.0, DEFAULT_MU)]),
    "grid2d": ((64.0, DEFAULT_MU), [(16.0, DEFAULT_MU),
                                    (32.0, DEFAULT_MU)]),
    "grid_elong": ((64.0, DEFAULT_MU), [(16.0, DEFAULT_MU),
                                        (32.0, DEFAULT_MU)]),
    "ladder": ((32.0, DEFAULT_MU), [(8.0, DEFAULT_MU),
                                    (16.0, DEFAULT_MU)]),
    "random6": ((32.0, DEFAULT_MU), [(8.0, DEFAULT_MU),
                                     (16.0, DEFAULT_MU)]),
    "torus": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "torus_elong": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "random3": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "random8": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "scale_free": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "scale_free200": ((4.0, 0.0), [(1.0, 0.0), (2.0, 0.0)]),
    "barbell": ((16.0, 0.0), [(4.0, 0.0), (8.0, 0.0)]),
    "bipartite": ((32.0, 0.0), [(8.0, 0.0), (16.0, 0.0)]),
    "complete": ((32.0, 0.0), [(8.0, 0.0), (16.0, 0.0)]),
}

# exp100 deposit keys for the adopted cells (reference errs)
DEP_KEY = {
    "star": "gamma_2", "tree": "gamma_64", "grid2d": "gamma_64",
    "grid_elong": "gamma_64", "ladder": "gamma_32",
    "random6": "gamma_32", "torus": "twodial_4_0",
    "torus_elong": "twodial_4_0", "random3": "twodial_4_0",
    "random8": "twodial_4_0", "scale_free": "twodial_4_0",
    "scale_free200": "twodial_4_0", "barbell": "twodial_16_0",
    "bipartite": "twodial_32_0", "complete": "twodial_32_0",
}


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


def run_cell(adj, seed: int, gamma: float, mu: float,
             steps_per_cell: int) -> dict:
    """The exp100 cell run (execute_two_source_n semantics) with a
    steps_per_cell dial; spc=8 is bit-identical to the deployed
    executor."""
    n = adjacency_n = adj.shape[0]
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
                        mu_theta=mu)
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
    for i, src in order2:
        for _ in range(steps_per_cell):
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
    c.run(15.0, dt=dt)
    ok_all = True
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        ok_all &= abs(float(np.mean(c.V[i0:i1])) - z.voltage) <= ERR_BAR
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    return {"program_verified": bool(ok_all),
            "err": round(err, 2)}


def cell_stats(adj, gamma, mu, spc) -> dict:
    runs = [run_cell(adj, s, gamma, mu, spc) for s in SEEDS3]
    return {"rate": round(float(np.mean(
        [x["program_verified"] for x in runs])), 3),
        "err": round(float(np.mean([x["err"] for x in runs])), 2)}


def main() -> dict:
    print("=== exp112: the walk-speed ladder ===\n")

    battery = build_battery()
    exp100 = json.load(open(os.path.join(
        ROOT, "results", "exp100_reader_price_map.json")))

    out: dict = {}
    buy_backs: dict = {}
    for name, (cell, rungs) in MEMBERS.items():
        adj = battery[name]
        g, m = cell
        a8 = cell_stats(adj, g, m, 8)
        a0 = cell_stats(adj, g, m, 0)
        ref = exp100["cells"][name][DEP_KEY[name]]
        out[f"{name}_adopted8"] = a8
        out[f"{name}_adopted0"] = a0
        print(f"    {name:13s} adopted{g:g}{'/' if m == 0.0 else '.'}"
              f"{m:g}  spc8 {a8['rate']:.2f}/{a8['err']:5.2f} "
              f"(exp100 {ref['rate']:.2f}/{ref['err']:5.2f})  "
              f"spc0 {a0['rate']:.2f}/{a0['err']:5.2f}")
        best = None
        for rg, rm in rungs:
            st = cell_stats(adj, rg, rm, 0)
            out[f"{name}_down0_{rg:g}_{rm:g}"] = st
            print(f"        down spc0 ({rg:g}, {rm:g})  "
                  f"{st['rate']:.2f}/{st['err']:5.2f}")
            if st["rate"] >= 2 / 3 and st["err"] < ERR_BAR:
                best = {"cell": [rg, rm],
                        "saves": round(g / rg, 2)}
                break
        if best:
            buy_backs[name] = best
            print(f"        -> BUY-BACK at ({best['cell'][0]:g}, "
                  f"{best['cell'][1]:g}), saves "
                  f"{best['saves']}x gamma")

    g2_ok = all(out[f"{n}_adopted8"]["rate"] >= 2 / 3
                and abs(out[f"{n}_adopted8"]["err"]
                        - exp100["cells"][n][DEP_KEY[n]]["err"])
                <= 0.75 for n in MEMBERS)
    g3_ok = all(out[f"{n}_adopted0"]["rate"] >= 2 / 3
                for n in MEMBERS
                if out[f"{n}_adopted8"]["rate"] >= 2 / 3)
    ws_g1 = len(buy_backs) >= 3
    ws_g2 = g2_ok
    ws_g3 = g3_ok

    print(f"\n  buy-backs: {len(buy_backs)}/15 -> "
          f"{ {k: v['cell'] for k, v in buy_backs.items()} }")
    print(f"\n  WS-G1 buy-back (>= 3 members): "
          f"{'PASS' if ws_g1 else 'REFUTED'}")
    print(f"  WS-G2 reference reproduction (+/- 0.75): "
          f"{'PASS' if ws_g2 else 'REFUTED'}")
    print(f"  WS-G3 no harm at the adopted cell: "
          f"{'PASS' if ws_g3 else 'REFUTED'}")

    npass = sum([ws_g1, ws_g2, ws_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp112_walk_speed_ladder",
        "arms": out,
        "buy_backs": buy_backs,
        "criteria": {
            "WS_G1_buy_back": bool(ws_g1),
            "WS_G2_reference_reproduction": bool(ws_g2),
            "WS_G3_no_harm": bool(ws_g3),
        },
        "notes": (
            "walk_speed (steps_per_cell 8 -> 0) as a candidate "
            "price-map dial: adopted-cell references at spc=8 "
            "reproduced, the same cells at spc=0 (no harm), and a "
            "two-rung one-dial-down descent at spc=0 per member. "
            "Buy-back = verification at a strictly cheaper cell."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
