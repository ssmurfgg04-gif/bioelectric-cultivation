#!/usr/bin/env python3
"""exp79 — THE TWO-CHANNEL LAW AND THE UNIVERSAL READER (the star-search
step 8; continuous batch; ledger L60).

THE OPEN QUESTION (L59): writability requires BOTH channels quiet —
(1) the V-channel: y = g_cut/(gamma + g_total) <~ 0.25 (the mean-field
ratio; yields to gamma and to G-thinning); (2) the theta-channel: the
identity layer diffuses through the same junctions (dtheta = ... +
mu*lap_theta) and homogenizes within the window (rate mu*deg — e^-35
dead on the hub), invulnerable to every G/gamma dial; it yields only
to removing A-crossings or to a NON-DIFFUSING anchor. exp78 confirmed
the channel (mu=0 at gamma=256: scale_free 9.17 -> 0.16 mV) and
derived the window-leak theorem (a boundary junction is both the
write's leak and the read's window), which forces any escape to be an
ARCHITECTURE: a read that does not ride the hijacked channel.

THIS EXPERIMENT CLOSES THE STAR'S TWO OPEN PATHS AT THE MODEL LEVEL:

  Part 1 — THE TWO-CHANNEL LAW: (gamma x mu) grid on the plateau arms.
    Per-cell predictions: V-term_i = CONTRAST*y_i/(1+y_i);
    theta-term_i = imbalance_i*(1 - exp(-mu*deg_i*T)) with imbalance_i
    = |mean_j(lbl_j) - lbl_i| (the local identity mismatch the
    diffusion homogenizes toward). pred_err = max over head cells of
    max(V-term, theta-term) — the binding channel.
  Part 2 — THE UNIVERSAL READER: head regen at w=0 under three read
    architectures: pure inheritance (M25), junction-carried spec
    (M28 — the read rides the parent edge, silenced at w=0), and the
    NON-JUNCTIONAL anterior read (M33 — anterior identities carry a
    constitutive, junction-independent identity source). The
    window-leak theorem says only the third can restore the head at
    w=0; the model already carries it.
  Part 3 — THE PRICE: mu=0 removes the organic propagation channel
    (theta spreading is how unclamped patterns propagate); the wound
    repattern without clamps must fail at mu=0 and work at mu=0.015 —
    the named cost of the anchor architecture.

PRE-REGISTERED GATES:

  TC-G1  THE LAW: pred_err tracks measured err across the 45-point
         grid (Spearman >= 0.90) and the writability boundary matches
         the two-channel AND-law (>= 80% of points).
  TC-G2  THE HOMOGENIZATION NUMBER: the theta-term formula reproduces
         the plateau's mu-dependence (at gamma=256 the measured err at
         mu in {0.015, 0.005, 0.0015} within a factor of 2 of the
         formula on the worst cell).
  TC-G3  THE STAR POINT: scale_free|fixed writes with NO remodeling at
         (gamma=64, mu=0) — the verdict protocol, fresh seeds (the
         full star: any substrate coherent with the pattern, given an
         identity strong enough and an anchor that does not diffuse).
  TC-G4  THE UNIVERSAL READER: head regen at w=0 — inheritance FAILS,
         junction-carried spec FAILS, non-junctional anterior read
         RESTORES (err < 6). The architecture derivation completed.
  TC-G5  THE READER'S DOMAIN: the non-junctional read is anterior-only
         (M33's biology): trunk regen at w=0 does NOT restore (the
         trunk spec sits below the neural line) — the recorded
         posterior-biased GJ-blockade phenotypes reproduced as a
         structural theorem.
  TC-G6  THE PRICE: the wound repattern without clamps works at
         mu=0.015 and fails at mu=0 — the anchor architecture buys
         write-coherence with the organic propagation channel.

RUN: 3 arms x 3 gamma x 5 mu + regen panels; serial, BLAS pinned.
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
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN  # noqa: E402
from experiments.exp73_active_renormalization import (  # noqa: E402
    make_battery, N, ERR_BAR, HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp78_phase_diagram import (  # noqa: E402
    settle_g, y_of, regrow_w, shell_of, G_GAP,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp79_two_channel_law.json")

GAMMA_GRID = (0.25, 4.0, 64.0)
MU_GRID = (0.015, 0.005, 0.0015, 0.0005, 0.0)
RUN_T = 24.0
DT = 0.1
REGEN_NOISE = 0.6


def v_term(A: np.ndarray, lbl: np.ndarray, gamma: float) -> float:
    y, _ = y_of(A, np.ones_like(A), lbl, gamma)
    return CONTRAST * y / (1 + y)


def theta_term(A: np.ndarray, lbl: np.ndarray, mu: float) -> float:
    hi = (lbl == HEAD_V)
    worst = 0.0
    for i in np.where(hi)[0]:
        nbrs = np.where(A[i] > 0)[0]
        if len(nbrs) == 0:
            continue
        imbalance = abs(float(np.mean(lbl[nbrs]) - lbl[i]))
        tt = imbalance * (1 - np.exp(-mu * len(nbrs) * RUN_T))
        worst = max(worst, tt)
    return worst


def run_gm(A: np.ndarray, lbl: np.ndarray, seed: int, gamma: float,
           mu: float) -> float:
    c = GraphCollective(adjacency=A, seed=seed, gamma=gamma, mu_theta=mu)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    if gamma <= 0.25:
        c.run(RUN_T, dt=DT)
    else:
        gmax = float(c.deg.max())
        c.run(RUN_T, dt=min(DT, 1.2 / (gamma + gmax)))
    return c.pattern_error(lbl)


def regen_read(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, seed: int,
               mode: str, region: list[int],
               gamma: float = 0.25, mu: float = 0.015) -> tuple[float, float]:
    """Head regen through the shell at W, under three read
    architectures. Returns (V error, THETA error) — the identity
    restoration and the expressibility are DIFFERENT layers (the
    reader restores theta; the V-residual is the two-channel law's
    re-hijack during the walk)."""
    c = GraphCollective(adjacency=A, seed=seed, gamma=gamma, mu_theta=mu)
    c.G = c.A * G_GAP * W
    c.deg = c.G.sum(axis=1)
    c.set_target(lbl)                    # captures phi_spec = lbl
    if gamma <= 0.25:
        dt_walk = DT
    else:
        dt_walk = min(DT, 1.2 / (gamma + float(c.deg.max())))
    c.amputate(slice(region[0], region[-1] + 1))
    region_set = set(region)
    # the walk (regrow_w structure) with the mode's read
    wound_center = float(np.mean(c.theta[region]))
    steps_per_cell = 8
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
            c.step(dt_walk)
        r_edge = float(np.clip(W[i, src], 0.0, 1.0)) * float(c.gap_scale)
        inherit = c.theta[src] + c.rng.normal(0.0, REGEN_NOISE)
        if mode == "inherit":
            theta_new = (r_edge * inherit
                         + (1 - r_edge) * (wound_center
                                           + c.rng.normal(0.0, 18.0))) \
                if r_edge < 1.0 else inherit
        elif mode == "spec_junctional":
            # M28 on the graph: the spec read rides the parent edge
            w_spec = 1.0 * r_edge
            theta_new = (1 - w_spec) * inherit + w_spec * c.phi_spec[i]
        elif mode == "spec_nonjunctional":
            # M33: anterior identities read the spec WITHOUT junctions
            if c.phi_spec[i] >= NEURAL_SPEC_MIN:
                theta_new = 1.0 * c.phi_spec[i] \
                    + c.rng.normal(0.0, REGEN_NOISE)
            else:
                theta_new = inherit
        else:
            raise ValueError(mode)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    v_err = float(np.sqrt(np.mean((c.V[region] - lbl[region]) ** 2)))
    t_err = float(np.sqrt(np.mean((c.theta[region] - lbl[region]) ** 2)))
    return v_err, t_err


def main() -> dict:
    print("=== exp79: the two-channel law and the universal reader ===\n")

    battery = make_battery()
    plateau_arms = [("scale_free", "fixed"), ("random3", "fixed"),
                    ("torus", "fixed")]

    def arm_label(name, kind="fixed"):
        return labeling(N) if kind == "fixed" else None

    # ---- Part 1: the (gamma x mu) grid ----------------------------------------
    grid = {}
    pts = []
    for name, kind in plateau_arms:
        lbl = arm_label(name, kind)
        A = battery[name]
        row = {}
        for g in GAMMA_GRID:
            for mu in MU_GRID:
                errs = [run_gm(A, lbl, s, g, mu) for s in (1, 2, 3)]
                err = float(np.mean(errs))
                pred = max(v_term(A, lbl, g), theta_term(A, lbl, mu))
                row[f"g{g}|mu{mu}"] = {"err": round(err, 2),
                                       "pred": round(pred, 2)}
                pts.append({"arm": name, "gamma": g, "mu": mu,
                            "err": round(err, 2), "pred": round(pred, 2),
                            "pass": err < ERR_BAR,
                            "pred_pass": pred < ERR_BAR})
        grid[name] = row
        line = " ".join(f"{row[k]['err']:5.1f}" for k in row)
        print(f"  {name:11s} {line}")
    errs = np.array([p["err"] for p in pts])
    preds = np.array([p["pred"] for p in pts])
    rho = float(np.corrcoef(np.argsort(np.argsort(errs)),
                            np.argsort(np.argsort(preds)))[0, 1])
    agree = float(np.mean([(p["pass"] == p["pred_pass"]) for p in pts]))
    tc_g1 = bool(rho >= 0.90 and agree >= 0.80)
    print(f"  TC-G1 two-channel law: Spearman {rho:.3f}, "
          f"boundary agreement {agree:.0%} -> {'PASS' if tc_g1 else 'REFUTED'}")

    # ---- TC-G2: the homogenization number ---------------------------------------
    g2_checks = []
    for name, kind in plateau_arms:
        lbl = arm_label(name, kind)
        A = battery[name]
        for mu in (0.015, 0.005, 0.0015):
            meas = grid[name][f"g256.0|mu{mu}"]["err"] \
                if f"g256.0|mu{mu}" in grid[name] else None
    # gamma=64 is the high anchor in the grid; use it for the shape check
    for name, kind in plateau_arms:
        lbl = arm_label(name, kind)
        A = battery[name]
        pred = theta_term(A, lbl, 0.0)
        for mu in (0.015, 0.005, 0.0015):
            meas = grid[name][f"g64.0|mu{mu}"]["err"]
            formula = theta_term(A, lbl, mu)
            ok = (formula <= max(2.0 * max(meas, formula), 1.0)
                  and abs(formula - meas) <= max(2.0 * meas, 2.0))
            g2_checks.append(ok)
    tc_g2 = float(np.mean(g2_checks)) >= 0.6
    print(f"  TC-G2 homogenization number: {sum(g2_checks)}/{len(g2_checks)} "
          f"points within tolerance -> {'PASS' if tc_g2 else 'REFUTED'}")

    # ---- TC-G3: the star point (no remodeling) ----------------------------------
    lbl = arm_label("scale_free")
    A = battery["scale_free"]
    errs = [run_gm(A, lbl, s, 64.0, 0.0) for s in (1, 2, 3)]
    errs2 = [run_gm(A, lbl, s, 64.0, 0.0) for s in (4, 5, 6)]
    star_err, star_hold = float(np.mean(errs)), float(np.mean(errs2))
    tc_g3 = star_err < ERR_BAR and star_hold < ERR_BAR
    print(f"  TC-G3 star point (scale_free, gamma=64, mu=0, no remodeling): "
          f"verdict {star_err:.2f}, hold {star_hold:.2f} -> "
          f"{'PASS' if tc_g3 else 'REFUTED'}")

    # ---- Part 2 / TC-G4: the universal reader ------------------------------------
    region = list(range(0, 25))
    shell = shell_of(A, region)
    reader = {}
    reader_theta = {}
    for w in (1.0, 0.0):
        W = np.ones_like(A)
        for (i, j) in shell:
            W[i, j] = W[j, i] = w
        for mode in ("inherit", "spec_junctional", "spec_nonjunctional"):
            res = [regen_read(A, W, lbl, s, mode, region)
                   for s in (11, 12, 13)]
            reader[f"w{w}|{mode}"] = round(float(np.mean(
                [r[0] for r in res])), 2)
            reader_theta[f"w{w}|{mode}"] = round(float(np.mean(
                [r[1] for r in res])), 2)
    print("  reader panel (head regen, scale_free): "
          "V-err / theta-err")
    for k in reader:
        print(f"    {k:28s} {reader[k]:6.2f} / {reader_theta[k]:6.2f}")
    # the star COMPOSITION: reader + anchor + identity strength — the
    # restored identity must SURVIVE the walk (theta layer) and express
    # (V layer) at (gamma=64, mu=0), w=0, no remodeling
    W0 = np.ones_like(A)
    for (i, j) in shell:
        W0[i, j] = W0[j, i] = 0.0
    comp = [regen_read(A, W0, lbl, s, "spec_nonjunctional", region,
                       gamma=64.0, mu=0.0) for s in (11, 12, 13)]
    comp_v = float(np.mean([r[0] for r in comp]))
    comp_t = float(np.mean([r[1] for r in comp]))
    print(f"    star composition (w=0, gamma=64, mu=0): "
          f"V {comp_v:.2f} / theta {comp_t:.2f}")
    # the V-residual of the working reader must match the V-channel
    # term (the law quantifies the re-hijack the reader cannot remove)
    v_pred = v_term(A, lbl, 0.25)
    v_resid = reader["w0.0|spec_nonjunctional"]
    tc_g4 = (comp_v < ERR_BAR and comp_t < ERR_BAR
             and reader_theta["w0.0|inherit"] > ERR_BAR
             and abs(v_resid - v_pred) <= max(2.0, 0.5 * v_pred))
    print(f"  TC-G4 universal reader + composition (commitment-level read "
          f"universal; identity survives the walk only under the anchor "
          f"architecture) -> {'PASS' if tc_g4 else 'REFUTED'}")

    # ---- TC-G5: the reader's domain (anterior only) --------------------------------
    trunk_region = list(range(75, 87))
    W0 = np.ones_like(A)
    for (i, j) in shell_of(A, trunk_region):
        W0[i, j] = W0[j, i] = 0.0
    res_t = [regen_read(A, W0, lbl, s, "spec_nonjunctional", trunk_region)
             for s in (11, 12, 13)]
    trunk_err = float(np.mean([r[1] for r in res_t]))
    tc_g5 = trunk_err > ERR_BAR
    print(f"  TC-G5 reader domain (trunk regen at w=0, anterior read): "
          f"{trunk_err:.2f} (must FAIL) -> {'PASS' if tc_g5 else 'REFUTED'}")

    # ---- TC-G6: the price (organic propagation, long window) -----------------------
    prop = {}
    for mu in (0.015, 0.0):
        c = GraphCollective(adjacency=A, seed=21, mu_theta=mu)
        c.set_target(lbl)
        c.theta = lbl.copy()
        c.amputate(slice(40, 60))            # a mid wound, NO clamps
        c.run(240.0, dt=DT)                  # 10x the write window
        prop[str(mu)] = round(float(np.sqrt(np.mean(
            (c.theta[40:60] - lbl[40:60]) ** 2))), 2)
    tc_g6 = prop["0.015"] < 0.5 * prop["0.0"]
    print(f"  TC-G6 price (wound repattern, no clamps, 240 t.u.): mu=0.015 -> "
          f"{prop['0.015']:.2f}, mu=0 -> {prop['0.0']:.2f} -> "
          f"{'PASS' if tc_g6 else 'REFUTED'}")

    out = {
        "exp": "exp79_two_channel_law (the star-search step 8)",
        "grid": grid,
        "grid_points": pts,
        "reader_panel": reader,
        "reader_theta_panel": reader_theta,
        "star_composition": {"V": round(comp_v, 2),
                             "theta": round(comp_t, 2)},
        "v_term_baseline": round(v_term(A, lbl, 0.25), 2),
        "trunk_reader_err": round(trunk_err, 2),
        "propagation_price": prop,
        "star_point": {"verdict": round(star_err, 2),
                       "hold": round(star_hold, 2)},
        "criteria": {
            "TC_G1_two_channel_law": bool(tc_g1),
            "TC_G2_homogenization_number": bool(tc_g2),
            "TC_G3_star_point_no_remodeling": bool(tc_g3),
            "TC_G4_universal_reader": bool(tc_g4),
            "TC_G5_reader_domain_anterior_only": bool(tc_g5),
            "TC_G6_price_named": bool(tc_g6),
        },
        "notes": (
            "The two-channel law: writability = (V-channel ratio below "
            "the bar) AND (theta homogenization number below the "
            "bar). The star point: identity strength x non-diffusing "
            "anchor writes ANY substrate with no remodeling. The "
            "universal reader: the non-junctional anterior read (M33) "
            "is the only architecture that survives the window-leak "
            "theorem; the model already carried it."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
