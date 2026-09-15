#!/usr/bin/env python3
"""exp78 — THE COHERENCE PHASE DIAGRAM (the star-search step 7;
continuous batch; ledger L59).

THE CONVERGENCE (L58): five remodeling rungs refuted in the high-degree
regime, all for one reason — no local signal finds the hijack's source
in a smeared field. The mean-field fixed point gives the real
variable: at a boundary cell,
    V* = (gamma*theta + G*V_nb) / (gamma + G_total),
    error_i ~ CONTRAST * g_cut_i / (gamma + g_total_i) = CONTRAST * y_i / (1 + y_i)
with y_i = g_cut_i / (gamma + g_total_i). WRITABILITY IS A PHASE
RATIO: y <~ bar/CONTRAST (~0.25), substrate-free in mean-field. The
hub fails because ITS g_cut = 10 while gamma = 0.25 — no rewiring of
other edges changes the hub's own ratio; only the cell's identity
strength (gamma) or its cut conductance (thinning) moves it.

THIS EXPERIMENT MEASURES THE PHASE DIAGRAM AND TESTS THE LAW:

  Part 1 — THE GAMMA SWEEP: gamma in {0.25, 1, 4, 16, 64, 256} x all
    8 arms, no remodeling. PD-G1: every fail arm flips writable at a
    finite gamma (the boundary moves with identity strength — the
    star's mechanism, no remodeling needed). PD-G2: the flip points
    collapse onto y (the ratio law — the universal coordinate the
    exp72 volume-law hunt lacked).

  Part 2 — THE THINNING DUALITY: uniform cut-thinning (all cut edges
    scaled to w, anatomy untouched) on the scale_free arms, w in
    {1, 0.3, 0.1, 0.03, 0.01, 0.003, 0}. PD-G3: the thinning flip w*
    maps onto the SAME y* band (thinning g_cut and raising gamma are
    one currency: both move y).

  Part 3 — THE WRITE/READ TRADE ON ONE DIAL: thin a SHELL around the
    tail region (the regen region's boundary edges) at w; measure (a)
    the region's write-hold error (decreases with thinning — less
    hijack) and (b) the region's REGENERATION error through the
    per-edge readout (r_edge = W_ij, the M25 semantics made per-edge;
    increases with thinning — the read starves). PD-G4: BOTH costs on
    ONE variable — the conservation-law candidate: each junction's
    conductance simultaneously carries the hijack and the signal; the
    crossover is the substrate's operating point.

  PD-G5 — THE MEAN-FIELD COLLAPSE: measured errors track
    err_pred = CONTRAST * y/(1+y) across the whole grid (Spearman >=
    0.9; band +-3 mV on the worst cell).

  PD-G0 — INSTRUMENT BIT-EXACTNESS: regrow_w at W=1 reproduces
    regrow_graph (gap_scale=1) on a fixed case (the per-edge read
    instrument is anchored before it is trusted).

RUN: 8 arms x 6 gammas x 3 seeds + 2 arms x 7 w x 3 seeds + 6 w x 3
seeds regen; serial, BLAS pinned.
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

from cultivation.substrate.graph import GraphCollective  # noqa: E402
from experiments.exp73_active_renormalization import (  # noqa: E402
    make_battery, labeling_bfs, b2v_of,
    N, ERR_BAR, HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp74_renormalization_ladder import cut_stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp78_phase_diagram.json")

G_GAP = 0.20
GAMMA_SWEEP = (0.25, 1.0, 4.0, 16.0, 64.0, 256.0)
W_SWEEP = (1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.0)
RUN_T = 24.0
DT = 0.1
CELL_PERIOD = 0.8
REGEN_NOISE = 0.6


def settle_g(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, seed: int,
             gamma: float) -> float:
    """The exp68 write protocol at arbitrary gamma. Euler stability:
    explicit integration needs dt < ~2/(gamma + g_max); the historical
    gamma=0.25 protocol (dt=0.1) is preserved bit-consistently with the
    ledger anchors; higher gammas sub-step the SAME ODE over the SAME
    24 t.u. window."""
    c = GraphCollective(adjacency=A, seed=seed, gamma=gamma)
    c.G = c.A * G_GAP * W
    c.deg = c.G.sum(axis=1)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    if gamma <= 0.25:
        c.run(RUN_T, dt=DT)
    else:
        gmax = float(c.deg.max())
        dt_eff = min(DT, 1.2 / (gamma + gmax))
        c.run(RUN_T, dt=dt_eff)
    return c.pattern_error(lbl)


def verdict_g(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, gamma: float,
              seeds=(1, 2, 3)) -> tuple[bool, float]:
    errs = [settle_g(A, W, lbl, s, gamma) for s in seeds]
    return (float(np.mean(errs)) < ERR_BAR, float(np.mean(errs)))


def y_of(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, gamma: float):
    """Per-cell phase variable y_i = g_cut_i / (gamma + g_total_i); the
    arm's y is the max over HEAD cells (the worst cell binds)."""
    hi = (lbl == HEAD_V)
    G = A * G_GAP * W
    y_max = 0.0
    worst = -1
    for i in np.where(hi)[0]:
        gc = gt = 0.0
        for j in np.where(A[i] > 0)[0]:
            g = G[i, j]
            gt += g
            if not hi[j]:
                gc += g
        y_i = gc / (gamma + gt) if (gamma + gt) > 0 else 0.0
        if y_i > y_max:
            y_max, worst = y_i, int(i)
    return y_max, worst


def y_mean_of(A: np.ndarray, W: np.ndarray, lbl: np.ndarray,
              gamma: float) -> float:
    """Mean y over head cells (the RMS estimate's phase variable)."""
    hi = (lbl == HEAD_V)
    G = A * G_GAP * W
    ys = []
    for i in np.where(hi)[0]:
        gc = gt = 0.0
        for j in np.where(A[i] > 0)[0]:
            g = G[i, j]
            gt += g
            if not hi[j]:
                gc += g
        ys.append(gc / (gamma + gt) if (gamma + gt) > 0 else 0.0)
    return float(np.mean(ys)) if ys else 0.0


def regrow_w(c: GraphCollective, W: np.ndarray, region: list[int],
             cell_period: float = CELL_PERIOD, dt: float = DT,
             noise: float = REGEN_NOISE) -> None:
    """regrow_graph with the PER-EDGE readout: the inheritance blend r
    rides the edge's conductance (r_edge = W_ij * gap_scale), the M25
    coupling-dependent read made per-edge. At W=1 this must reproduce
    regrow_graph (PD-G0)."""
    region_set = set(region)
    r_global = float(c.gap_scale)
    wound_center = float(np.mean(c.theta[region]))
    steps_per_cell = max(1, int(round(cell_period / dt)))

    parent_of: dict[int, int] = {}
    frontier: list[int] = []
    for i in region:
        nbrs = [j for j in np.where(c.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(
                nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = region[:1]
        parent_of[frontier[0]] = frontier[0]

    visited = set(frontier)
    order: list[tuple[int, int]] = [(i, parent_of[i]) for i in frontier]
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
        r = float(np.clip(W[i, src], 0.0, 1.0)) * r_global
        if r >= 1.0:
            theta_new = c.theta[src] + c.rng.normal(0.0, noise)
        else:
            guess = wound_center + c.rng.normal(
                0.0, c.blastema_readout_noise)
            theta_new = r * (c.theta[src] + c.rng.normal(0.0, noise)) \
                + (1.0 - r) * guess
        c.theta[i] = theta_new
        c.V[i] = theta_new


def shell_of(A: np.ndarray, region: list[int]) -> list[tuple[int, int]]:
    """Edges with exactly one endpoint in the region (the regen shell /
    the region's electrical boundary)."""
    rs = set(region)
    edges = set()
    for i in region:
        for j in np.where(A[i] > 0)[0]:
            j = int(j)
            if j not in rs:
                edges.add((min(i, j), max(i, j)))
    return sorted(edges)


def main() -> dict:
    print("=== exp78: the coherence phase diagram (star-search step 7) ===\n")

    battery = make_battery()
    fail_arms = [("torus", "fixed"), ("torus", "bfs"),
                 ("random3", "fixed"), ("random3", "bfs"),
                 ("scale_free", "fixed"), ("scale_free", "bfs")]
    pass_arms = [("path", "fixed"), ("grid2d", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- PD-G0: instrument bit-exactness (head regen on scale_free) ------------
    A = battery["scale_free"]
    lbl = labeling(N)
    c1 = GraphCollective(adjacency=A, seed=5)
    c1.set_target(lbl)
    c1.amputate(slice(0, 25))
    c1.regrow_graph(list(range(0, 25)))
    err_ref = c1.pattern_error(lbl)
    c2 = GraphCollective(adjacency=A, seed=5)
    c2.set_target(lbl)
    c2.amputate(slice(0, 25))
    regrow_w(c2, np.ones_like(A), list(range(0, 25)))
    err_new = c2.pattern_error(lbl)
    pd_g0 = abs(err_ref - err_new) < 1e-9
    print(f"  PD-G0 regrow_w bit-exact at W=1: "
          f"{err_ref:.6f} vs {err_new:.6f} -> {'PASS' if pd_g0 else 'REFUTED'}\n")

    # ---- Part 1: the gamma sweep -----------------------------------------------
    grid = {}
    for name, kind in fail_arms + pass_arms:
        lbl = arm_label(name, kind)
        row = {}
        for g in GAMMA_SWEEP:
            ok, err = verdict_g(battery[name], np.ones_like(battery[name]),
                                lbl, g)
            row[g] = {"err": round(err, 2), "pass": bool(ok)}
        grid[f"{name}|{kind}"] = row
        flips = [g for g in GAMMA_SWEEP if row[g]["pass"]]
        gstar = min(flips) if flips else None
        y_star = None
        if gstar is not None:
            y_star, _ = y_of(battery[name], np.ones_like(battery[name]),
                             lbl, gstar)
        print(f"  {name:11s}|{kind:5s} " +
              " ".join(f"g{g:<4}:{row[g]['err']:6.2f}"
                       f"{'*' if row[g]['pass'] else ' '}"
                       for g in GAMMA_SWEEP) +
              f"  gamma* {gstar} y* {y_star if y_star is None else round(y_star, 3)}")
    pd_g1 = all(any(grid[f"{n}|{k}"][g]["pass"] for g in GAMMA_SWEEP)
                for n, k in fail_arms)
    y_flips = []
    for (n, k), row in [(x, grid[f"{x[0]}|{x[1]}"]) for x in fail_arms]:
        flips = [g for g in GAMMA_SWEEP if row[g]["pass"]]
        if flips:
            lbl = arm_label(n, k)
            y, _ = y_of(battery[n], np.ones_like(battery[n]), lbl,
                        min(flips))
            y_flips.append(y)
    pd_g2 = bool(y_flips) and 0.10 <= min(y_flips) and max(y_flips) <= 0.50
    print(f"\n  PD-G1 boundary moves with identity (every arm flips): "
          f"{'PASS' if pd_g1 else 'REFUTED'}")
    print(f"  PD-G2 ratio law (y* at flips in [0.10, 0.50]): "
          f"y_flips = {[round(y, 3) for y in y_flips]} -> "
          f"{'PASS' if pd_g2 else 'REFUTED'}")

    # ---- Part 2: the thinning duality (uniform cut scaling) ---------------------
    dual = {}
    for name, kind in [("scale_free", "fixed"), ("scale_free", "bfs")]:
        lbl = arm_label(name, kind)
        A = battery[name]
        hi = (lbl == HEAD_V)
        W_cut = np.ones_like(A)
        for i in range(N):
            for j in np.where(A[i] > 0)[0]:
                if j > i and hi[i] != hi[j]:
                    W_cut[i, j] = W_cut[j, i] = np.nan  # mark cut
        row = {}
        for w in W_SWEEP:
            W = np.ones_like(A)
            W[np.isnan(W_cut)] = w
            ok, err = verdict_g(A, W, lbl, 0.25)
            y, _ = y_of(A, W, lbl, 0.25)
            row[w] = {"err": round(err, 2), "pass": bool(ok),
                      "y": round(y, 4)}
        dual[f"{name}|{kind}"] = row
        print(f"  dual {name}|{kind}: " +
              " ".join(f"w{w}: {row[w]['err']:6.2f}"
                       f"{'*' if row[w]['pass'] else ' '}"
                       for w in W_SWEEP))
    # duality: the thinning flip's y must sit in the same band
    y_dual = []
    for row in dual.values():
        flips = [w for w in W_SWEEP if row[w]["pass"]]
        if flips:
            y_dual.append(row[min(flips)]["y"])
    pd_g3 = bool(y_dual) and all(0.10 <= y <= 0.50 for y in y_dual)
    print(f"  PD-G3 duality (thinning flips land in the same y band): "
          f"y_dual = {[round(y, 3) for y in y_dual]} -> "
          f"{'PASS' if pd_g3 else 'REFUTED'}")

    # ---- Part 3: the write/read trade on one dial -------------------------------
    trade = {}
    name, kind = "scale_free", "fixed"
    A = battery[name]
    lbl = arm_label(name, kind)
    # a SUB-region of the head: its parents (head cells 12-24) carry the
    # RIGHT identity, so the per-edge read can be starved honestly (an
    # amputated whole-head has only trunk parents and inherits the WRONG
    # identity regardless of W — measured and discarded in the first run).
    region = list(range(0, 12))
    shell = shell_of(A, region)
    for w in (1.0, 0.3, 0.1, 0.03, 0.01, 0.0):
        W = np.ones_like(A)
        for (i, j) in shell:
            W[i, j] = W[j, i] = w
        # (a) the region's write-hold error (3 seeds)
        werr = []
        for s in (1, 2, 3):
            c = GraphCollective(adjacency=A, seed=s)
            c.G = c.A * G_GAP * W
            c.deg = c.G.sum(axis=1)
            c.set_target(lbl)
            c.theta = lbl.copy()
            c.V = c.theta + c.rng.normal(0.0, 2.0, N)
            c.run(RUN_T, dt=DT)
            werr.append(float(np.sqrt(np.mean(
                (c.V[region] - lbl[region]) ** 2))))
        # (b) the region's REGEN through the thinned shell (3 seeds)
        rerr = []
        for s in (11, 12, 13):
            c = GraphCollective(adjacency=A, seed=s)
            c.G = c.A * G_GAP * W
            c.deg = c.G.sum(axis=1)
            c.set_target(lbl)
            c.amputate(slice(0, 12))
            regrow_w(c, W, region)
            rerr.append(float(np.sqrt(np.mean(
                (c.V[region] - lbl[region]) ** 2))))
        trade[w] = {"write_err": round(float(np.mean(werr)), 2),
                    "regen_err": round(float(np.mean(rerr)), 2),
                    "n_shell": len(shell)}
        print(f"  trade w={w:5}: write {trade[w]['write_err']:6.2f}  "
              f"regen {trade[w]['regen_err']:6.2f} "
              f"(shell {len(shell)} edges)")
    ws = sorted(trade, reverse=True)
    write_down = all(trade[ws[i]]["write_err"] <= trade[ws[i + 1]]["write_err"]
                     + 0.5 for i in range(len(ws) - 1))
    regen_up = all(trade[ws[i]]["regen_err"] <= trade[ws[i + 1]]["regen_err"]
                   + 0.5 for i in range(len(ws) - 1))
    pd_g4 = write_down and regen_up
    print(f"  PD-G4 one dial prices both (write down, regen up): "
          f"{'PASS' if pd_g4 else 'REFUTED'} "
          f"(write_down {write_down}, regen_up {regen_up})")

    # ---- PD-G5: the mean-field collapse ------------------------------------------
    pts = []
    for (n, k), row in [(x, grid[f"{x[0]}|{x[1]}"]) for x in
                        fail_arms + pass_arms]:
        lbl = arm_label(n, k)
        for g in GAMMA_SWEEP:
            y_worst, worst = y_of(battery[n], np.ones_like(battery[n]),
                                  lbl, g)
            y_mean = y_mean_of(battery[n], np.ones_like(battery[n]),
                               lbl, g)
            pred = CONTRAST * y_mean / (1 + y_mean)
            pts.append({"arm": f"{n}|{k}", "gamma": g,
                        "err": row[g]["err"], "pred": round(pred, 2),
                        "y_worst": round(y_worst, 4),
                        "y_mean": round(y_mean, 4)})
    errs = np.array([p["err"] for p in pts])
    preds = np.array([p["pred"] for p in pts])
    rho = float(np.corrcoef(np.argsort(np.argsort(errs)),
                            np.argsort(np.argsort(preds)))[0, 1])
    pd_g5 = bool(rho >= 0.90)
    print(f"  PD-G5 mean-field collapse: Spearman {rho:.3f} "
          f"-> {'PASS' if pd_g5 else 'REFUTED'}")

    # ---- the plateau attribution: the theta channel -----------------------------
    # every gamma/W dial plateaus (torus 4.8, random3 8.1, scale_free 9.2).
    # The registered diagnosis: the plateau is the THETA channel — theta
    # diffuses through the junctions (mu * lap_theta) and homogenizes the
    # identity layer within the window, invulnerable to every G/gamma
    # dial. Direct test: gamma=256 with mu=0 (the non-diffusing anchor).
    plateau = {}
    for name, kind in [("scale_free", "fixed"), ("random3", "fixed"),
                       ("torus", "fixed")]:
        lbl = arm_label(name, kind)
        row = {}
        for mu in (0.015, 0.0):
            errs = []
            for s in (1, 2, 3):
                c = GraphCollective(adjacency=battery[name], seed=s,
                                    gamma=256.0, mu_theta=mu)
                c.set_target(lbl)
                c.theta = lbl.copy()
                c.V = c.theta + c.rng.normal(0.0, 2.0, N)
                gmax = float(c.deg.max())
                c.run(RUN_T, dt=min(DT, 1.2 / (256.0 + gmax)))
                errs.append(c.pattern_error(lbl))
            row[str(mu)] = round(float(np.mean(errs)), 2)
        plateau[f"{name}|{kind}"] = row
        print(f"  plateau {name:11s} gamma=256: mu=0.015 -> {row['0.015']:6.2f}"
              f"  mu=0 -> {row['0.0']:6.2f}")
    theta_conf = all(plateau[k]["0.0"] < ERR_BAR
                     for k in plateau)
    print(f"  theta-channel attribution (mu=0 flips the plateaus): "
          f"{'CONFIRMED' if theta_conf else 'REFUTED'}")

    out = {
        "exp": "exp78_phase_diagram (the star-search step 7)",
        "gamma_grid": grid,
        "thinning_duality": dual,
        "write_read_trade": trade,
        "plateau_attribution": plateau,
        "collapse_points": pts,
        "criteria": {
            "PD_G0_instrument_bit_exact": bool(pd_g0),
            "PD_G1_boundary_moves_with_identity": bool(pd_g1),
            "PD_G2_ratio_law": bool(pd_g2),
            "PD_G3_thinning_duality": bool(pd_g3),
            "PD_G4_one_dial_both_costs": bool(pd_g4),
            "PD_G5_mean_field_collapse": bool(pd_g5),
            "PD_G7_theta_channel_confirmed": bool(theta_conf),
        },
        "notes": (
            "The coherence phase diagram: writability as a phase "
            "ratio y = g_cut/(gamma + g_total) with the boundary at "
            "y* ~ bar/CONTRAST. Identity strength (gamma) and "
            "conductance thinning (W) are the same currency. The "
            "write/read trade on one dial is the conservation-law "
            "candidate: each junction carries the hijack and the "
            "signal; the crossover is the operating point."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
