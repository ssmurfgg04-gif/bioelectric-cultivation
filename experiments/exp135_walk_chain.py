#!/usr/bin/env python3
"""exp135 — THE WALK-CHAIN ACCUMULATION (ledger L114's registered
object, the fourth candidate for the deadline's law after three
refutations: exp125's free homogenization (both readings), exp132's
clamp-anchored V-exposure, exp134's theta-exposure).

THE OPEN PROBLEM. The censoring-corrected torus deadline curve is
monotone-RISING in pinning gamma — the empirical edges (first onset
with P(break) >= 0.5, 8 seeds, exp125's censoring-free deposit) are

    gamma   1    4    16    64
    edge    0    48   52    >34 (censored: real window ends 34.3 h)

and the two late-onset controls (g16@72, g64@36 — the latch fires
only in the settle's final hours) break at P=1.0. Both refuted
linearized families share one bug-class: the exposure is a PER-STEP/
INSTANTANEOUS functional of the boundary trajectory —
D(gamma, t*) = int_0^T_pre |delta_i(t)| dt on the intact boundary —
and both are INFEASIBLE on the same violated pair (gamma-16@52-break
vs gamma-4@36-rescue): the boundary V/theta deviation falls with
gamma while the empirical deadline RISES, and the mu-channel's
marginal damage (~14 D-units/h at the gamma-16 transition) is ~14x
too small for the 4 h rescue-to-break bracket. exp134's closing
lesson: the walk reads THETA (exp116 placed the mu damage in theta
independently); the missing structure sits DOWNSTREAM of the
boundary — in the walk itself.

THE MODEL (pre-registered here, BEFORE running; free parameters =
ONE transfer coefficient kappa and ONE persistence timescale tau_p,
fitted ONCE as a single pair on the torus's censoring-corrected
constraint cells and used unchanged across all four anchors —
GATE-B3 forbids any per-gamma re-fit):

  1. WINDOW [0, 24 h]: the harness deviation dynamics on the full
     graph as a deterministic mean field — the harness's own Euler
     update, noise omitted (the V-noise's stationary RMS is < 1 mV
     and the inheritance noise is 0.6 mV iid, both an order below
     the 6.0 bar):
       dV     = gamma (theta - V) + G V - V deg_G,  G = 0.20 A
       dtheta = eps (V - theta) + mu(t) (A theta - theta deg_A)
     zones clamped at their target voltage (V forced; theta pulled
     at the clamp's extra eps rate); mu = 0.015 until t* then 0
     (exp124's latch, mirrored step-for-step, INCLUDING inside the
     walk and settle so the late controls silence mid-settle exactly
     as the harness does). dt = star_dt(gamma), the harness's own
     stability bound. This is exp132/134's window physics, kept.
  2. AMPUTATION at 24 h: the 73-cell span resets to the wound state
     (V = -30, theta = -40).
  3. THE WALK CHAIN: exp124's multi-source BFS order over the span
     (frontier = boundary-adjacent span cells first, then BFS
     discovery; the parent choice feeds only a dead branch); each
     cell takes 8 Euler sub-steps and is then INJECTED at its target
     value — in the harness every inheritance branch (phi_spec >=
     -35, phi_spec_canon, or the parent chain) delivers exactly the
     cell's target value, so the deterministic injection IS the
     harness's mean inheritance. The wound phase's own mismatch is
     ERASED by the injection reset (the harness overwrites both
     theta and V); it enters the debt only through the drag it
     exerts, while still wound, on already-injected chain cells and
     the intact reservoir — the non-resetting carry that both
     refuted families collapsed away.
  4. THE ACCUMULATED DEBT (the registered object): with m(s) =
     sum over INJECTED span cells of |theta_i(s) - target_i| (the
     chain's theta-mismatch rate — THETA, per the exp116/exp134
     localization; the intact reservoir is not a walk cell and
     enters only through coupling), the debt at the read is the
     persistence-kernel convolution of the walk history:

       D(t*) = int_{24h}^{T_read} exp(-(T_read - s)/tau_p) m(s) ds,

     computed online as a leaky accumulator: the debt carried into
     each walk step is the kernel-weighted integral of ALL earlier
     steps (state persists across steps — non-Markovian), not a
     per-step instantaneous exposure. tau_p -> infinity recovers
     full accumulation; tau_p -> 0 recovers the per-step (Markov)
     exposure class of exp132/134. predicted_error = kappa D / 73;
     break iff > 6.0 (the exp132 transfer convention, N_REGION=73).
  5. Deadline(gamma) = first deposited onset whose predicted error
     crosses the bar.

GATES (pre-registered; the distinctions from BOTH refuted families):

  GATE-B1  (the curve) with the single fitted (kappa, tau_p): every
           real deposited torus cell (exp125's censoring-corrected
           grids) reproduces its deposited break boolean AND both
           late controls (g16@72, g64@36) break — the 0/48/52/>34
           curve within tolerance (the DL-G2 exact-boolean
           convention at the deposited grid resolution). On failure
           the violated constraint pair is named (the exp132
           convention).
  GATE-B2  (the sign) the predicted deadline RISES with pinning:
           edge(g1) = 0 < edge(g4) <= edge(g16), and gamma 64
           rescues at 34 while its late control breaks — the sign
           BOTH refuted families got wrong.
  GATE-B3  (no per-gamma re-fit) ONE (kappa, tau_p) pair satisfies
           all four anchors simultaneously — the joint feasible
           region over the tau_p grid is non-empty. If only
           per-gamma parameter sets exist, REFUTE as curve-fitting
           (the per-gamma contrast is computed and reported either
           way; if even per-gamma sets fail for some gamma, that is
           the stronger structural refutation and is named).
  GATE-B4  (accumulation discriminator) the PER-STEP ablation —
           exp134's boundary exposure D_abl = int_0^{T_pre}
           sum_{bnd} |theta - target| dt (the boundary trajectory
           under the same mu latch, but NO chain and NO kernel —
           the walk collapsed away exactly as the refuted family
           collapsed it), computed in THIS machinery and fitted on
           the same cells — must stay INFEASIBLE. (A window-only
           [0, 24 h] variant is blind to every onset beyond the
           window by construction; reported as a footnote only.)
           If the ablation is feasible, the exp135 pass does not
           isolate accumulation (the exp132/134 refutations were
           machinery-specific): report and diagnose.

ROBUSTNESS (reported, not gated): R1 zero-free transfer of the
fitted pair to grid2d and path (their deposited curves are flat-zero
at every real cell — all must predict non-break); R2 the ZERO-
PARAMETER mechanism check — the raw deterministic simulation's final
RMS error at the same cells (does the plain walk-chain dynamics,
kappa = 1, no debt abstraction, cross the 6.0 bar between the same
brackets?); R3 the intact/span error decomposition at the binding
transitions (where the error lives); R4 the marginal debt rate
kappa (dD/dt*)/73 at the gamma-16 (48, 52] transition vs the 4 h
bracket demand (exp134's 14x shortfall, re-measured for the
accumulated object).

RUN: ~80 deterministic sims (torus constraint cells + grid2d/path
transfer cells), seconds, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp125_u_shape_generalization import (
    protocol_end, region_span, target_pattern, MU, EPS, G_GAP,
    WINDOW_H, SETTLE_H, GRIDS, TORUS_G1,
)
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp135_walk_chain.json")

GAMMAS = (1.0, 4.0, 16.0, 64.0)
ERR_BAR = 6.0
WALK_SUB = 8
WOUND_V, WOUND_TH = -30.0, -40.0
TAU_GRID = (2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 1.0e9)


def canon_pattern(adj: np.ndarray) -> np.ndarray:
    n = adj.shape[0]
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    return canon


def zone_clamps(n: int) -> list[tuple[np.ndarray, float]]:
    """compile_anatomy(MULTI, n)'s R1 clamp emission, verbatim."""
    out = []
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        out.append((np.arange(i0, i1), float(z.voltage)))
    return out


def walk_order(adj: np.ndarray, lo: int, hi: int) -> list[int]:
    """exp124's run_deadline walk order: multi-source BFS over the
    span, frontier = span cells with an intact neighbor first (in
    index order), then BFS discovery. The parent choice (nearest to
    wound_center) feeds only the dead inheritance branch, not the
    order."""
    region = set(range(lo, hi + 1))
    frontier: list[int] = []
    for i in range(lo, hi + 1):
        if any(int(j) not in region for j in np.where(adj[i] > 0)[0]):
            frontier.append(i)
    visited = set(frontier)
    order = list(frontier)
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(adj[i] > 0)[0]:
            j = int(j)
            if j in region and j not in visited:
                visited.add(j)
                order.append(j)
                queue.append(j)
    assert sorted(order) == list(range(lo, hi + 1)), "walk order broken"
    return order


def simulate(adj: np.ndarray, gamma: float, t_star: float | None) -> dict:
    """Deterministic mean-field replay of exp124's run_deadline
    protocol (noise-free). t_star = None -> never silenced. Returns
    the final RMS error (with span/intact decomposition) and the
    theta-mismatch trajectories that feed the debt integrals."""
    n = adj.shape[0]
    dt = star_dt(gamma, float(adj.sum(axis=1).max()))
    A = adj.astype(float)
    degA = A.sum(axis=1)
    G = G_GAP * A
    degG = G.sum(axis=1)
    target = target_pattern(adj)
    canon = canon_pattern(adj)
    clamps = zone_clamps(n)
    zall = np.concatenate([idx for idx, _ in clamps])
    lo, hi = int(zall.min()), int(zall.max())
    span = np.arange(lo, hi + 1)
    intact = np.array([i for i in range(n) if i < lo or i > hi], dtype=int)
    bnd = np.array(sorted({int(j) for i in span
                           for j in np.where(adj[i] > 0)[0]
                           if j < lo or j > hi}), dtype=int)
    order2 = walk_order(adj, lo, hi)

    V = canon.astype(float).copy()
    th = canon.astype(float).copy()
    mu = MU
    t0 = 0.0
    n_win = int(round(WINDOW_H / dt))
    m_traj: list[float] = []   # chain mismatch, post-amputation only
    b_traj: list[float] = []   # boundary mismatch, whole run
    inj = np.zeros(n, dtype=bool)

    def chain_mismatch() -> float:
        msk = np.where(inj[span])[0]
        if len(msk) == 0:
            return 0.0
        idx = span[msk]
        return float(np.abs(th[idx] - target[idx]).sum())

    def bnd_mismatch() -> float:
        return float(np.abs(th[bnd] - target[bnd]).sum())

    def dyn_step() -> None:
        nonlocal V, th, t0, mu
        t0 += dt
        if t_star is not None and t0 >= t_star:
            mu = 0.0
        dV = gamma * (th - V) + G @ V - V * degG
        dth = EPS * (V - th) + mu * (A @ th - th * degA)
        V = V + dt * dV
        th = th + dt * dth

    # ---- window (clamps on)
    for _ in range(n_win):
        dyn_step()
        for idx, val in clamps:
            V[idx] = val
            th[idx] += dt * EPS * (val - th[idx])
        b_traj.append(bnd_mismatch())

    # ---- amputation + the walk chain
    V[span] = WOUND_V
    th[span] = WOUND_TH
    for i in order2:
        for _ in range(WALK_SUB):
            dyn_step()
            m_traj.append(chain_mismatch())
            b_traj.append(bnd_mismatch())
        # the injection: every harness branch delivers target[i]
        V[i] = target[i]
        th[i] = target[i]
        inj[i] = True

    # ---- settle
    for _ in range(int(round(SETTLE_H / dt))):
        dyn_step()
        m_traj.append(chain_mismatch())
        b_traj.append(bnd_mismatch())

    return {
        "dt": dt,
        "t_read": t0,
        "t_pre": protocol_end(adj, gamma),
        "err": float(np.sqrt(np.mean((V - target) ** 2))),
        "err_span": float(np.sqrt(np.mean((V[span] - target[span]) ** 2))),
        "err_intact": float(np.sqrt(np.mean((V[intact] - target[intact]) ** 2))),
        "th_span_dev": float(np.sqrt(np.mean((th[span] - target[span]) ** 2))),
        "m_traj": m_traj,
        "b_traj": b_traj,
        "n_win": n_win,
    }


def debt(sim: dict, tau_p: float) -> float:
    """D(t*) = sum_j dt m_j exp(-(T_read - t_j)/tau_p) — the leaky
    accumulator evaluated at the read."""
    m = np.asarray(sim["m_traj"])
    if len(m) == 0:
        return 0.0
    dt = sim["dt"]
    t_rel = np.arange(1, len(m) + 1) * dt
    T = len(m) * dt
    with np.errstate(under="ignore"):
        w = np.exp(-(T - t_rel) / tau_p)
    return float(np.sum(m * dt * w))


def debt_ablation(sim: dict, n_region: int) -> float:
    """exp134's per-step exposure in THIS machinery: the boundary
    time-integral over [0, T_pre] (window + walk steps, same mu
    latch), no chain, no kernel."""
    n_pre = sim["n_win"] + WALK_SUB * n_region
    b = np.asarray(sim["b_traj"][:n_pre])
    return float(b.sum() * sim["dt"])


def fit_interval(d_break: list[float], d_rescue: list[float],
                 n_region: int) -> tuple[float, float, bool]:
    """kmin = max over break cells of BAR*n_region/D (D=0 -> inf);
    kmax = min over rescue cells. Feasible iff kmin < kmax."""
    kmin = max((ERR_BAR * n_region / d if d > 0 else float("inf"))
               for d in d_break)
    kmax = min((ERR_BAR * n_region / d if d > 0 else float("inf"))
               for d in d_rescue)
    return kmin, kmax, bool(kmin < kmax)


def main() -> dict:
    print("=== exp135: the walk-chain accumulation ===\n")
    t_start = time.time()
    battery = build_battery()
    torus = battery["torus"]
    n_region = region_span(torus.shape[0])
    assert n_region == 73

    # ---- the censoring-corrected constraint cells (exp125 deposit)
    break_cells = [(1.0, float(t)) for t in TORUS_G1] \
        + [(4.0, 48.0), (16.0, 52.0), (16.0, 56.0), (16.0, 58.0)] \
        + [(16.0, 72.0), (64.0, 36.0)]          # the two late controls
    rescue_cells = [(4.0, float(t)) for t in GRIDS[4.0] if t <= 36.0] \
        + [(16.0, float(t)) for t in (0.0, 24.0, 36.0, 48.0)] \
        + [(64.0, float(t)) for t in GRIDS[64.0]]

    all_cells = sorted(set(break_cells) | set(rescue_cells))
    sim: dict = {}
    for g, t in all_cells:
        sim[(g, t)] = simulate(torus, g, t)
    print(f"  torus constraint sims: {len(sim)} "
          f"({time.time() - t_start:.0f}s)", flush=True)

    # ---- GATE-B3: the joint (kappa, tau_p) fit over the tau grid
    d_break = {(c, tau): debt(sim[c], tau)
               for c in break_cells for tau in TAU_GRID}
    d_rescue = {(c, tau): debt(sim[c], tau)
                for c in rescue_cells for tau in TAU_GRID}
    d_abl_break = {c: debt_ablation(sim[c], n_region) for c in break_cells}
    d_abl_rescue = {c: debt_ablation(sim[c], n_region)
                    for c in rescue_cells}

    rows = []
    for tau in TAU_GRID:
        db = [d_break[(c, tau)] for c in break_cells]
        dr = [d_rescue[(c, tau)] for c in rescue_cells]
        kmin, kmax, ok = fit_interval(db, dr, n_region)
        bb = max(break_cells, key=lambda c: d_break[(c, tau)]
                 if d_break[(c, tau)] > 0 else -1.0)
        br = min(rescue_cells, key=lambda c: d_rescue[(c, tau)]
                 if d_rescue[(c, tau)] > 0 else float("inf"))
        rows.append({"tau_p": tau, "kmin": kmin, "kmax": kmax,
                     "feasible": ok,
                     "binding_break": f"g{bb[0]:g}_t{bb[1]:g}",
                     "binding_rescue": f"g{br[0]:g}_t{br[1]:g}",
                     "D_break": {f"g{c[0]:g}_t{c[1]:g}":
                                 round(d_break[(c, tau)], 2)
                                 for c in break_cells},
                     "D_rescue": {f"g{c[0]:g}_t{c[1]:g}":
                                  round(d_rescue[(c, tau)], 2)
                                  for c in rescue_cells}})
    feas = [r for r in rows if r["feasible"]]
    b3 = bool(feas)
    if feas:
        best = max(feas, key=lambda r: r["kmax"] - r["kmin"])
        tau_star, kmin, kmax = best["tau_p"], best["kmin"], best["kmax"]
        kappa = 0.5 * (kmin + kmax)
    else:
        best = max(rows, key=lambda r: r["kmax"] - r["kmin"])
        tau_star, kmin, kmax = best["tau_p"], best["kmin"], best["kmax"]
        kappa = float("nan")
    print(f"  B3 joint fit: feasible tau_p = "
          f"{[r['tau_p'] for r in feas] if feas else 'NONE'}",
          flush=True)
    if feas:
        print(f"  fitted pair: tau_p*={tau_star:g} h, "
              f"kappa* in ({kmin:.4f}, {kmax:.4f}), mid {kappa:.4f}",
              flush=True)

    # ---- GATE-B1: the curve at the fitted pair
    def pred(g, t, kap=None, tau=None):
        kap = kappa if kap is None else kap
        tau = tau_star if tau is None else tau
        return kap * debt(sim[(g, t)], tau) / n_region

    b1, curve_rows, mism = True, [], []
    for g, t in all_cells:
        p = pred(g, t)
        want_break = (g, t) in break_cells
        got = p > ERR_BAR
        curve_rows.append({"cell": f"g{g:g}_t{t:g}",
                           "D": round(debt(sim[(g, t)], tau_star), 2),
                           "pred_err": round(p, 3),
                           "direct_err": round(sim[(g, t)]["err"], 3),
                           "deposited": "break" if want_break else "rescue",
                           "predicted": "break" if got else "rescue"})
        if want_break != got:
            b1 = False
            mism.append(f"g{g:g}_t{t:g}")
    print(f"  B1 curve: {'PASS' if b1 else 'REFUTED'} "
          f"mismatches {mism}", flush=True)

    # ---- GATE-B2: the sign (edges rising with gamma)
    def edge(g, grid):
        for t in grid:
            if pred(g, float(t)) > ERR_BAR:
                return float(t)
        return None

    e = {g: edge(g, GRIDS[g] if g != 1.0 else TORUS_G1) for g in GAMMAS}
    ctrl_ok = (pred(16.0, 72.0) > ERR_BAR) and (pred(64.0, 36.0) > ERR_BAR)
    lb64 = 34.0 if e[64.0] is None else e[64.0]
    b2 = (e[1.0] == 0.0) and (e[4.0] is not None) and (e[4.0] > 0.0) \
        and (e[16.0] is not None) and (e[16.0] >= e[4.0] - 1e-9) \
        and (lb64 >= min(e[4.0], 24.0) - 1e-9) and ctrl_ok
    print(f"  B2 sign: edges {e} (g64 LB 34), controls break "
          f"{ctrl_ok} -> {'PASS' if b2 else 'REFUTED'}", flush=True)

    # ---- the per-gamma contrast (the curve-fitting signature)
    per_gamma = {}
    for g in GAMMAS:
        gb = [d_break[(c, tau_star)] for c in break_cells if c[0] == g]
        gr = [d_rescue[(c, tau_star)] for c in rescue_cells if c[0] == g]
        if gb and gr:
            k1, k2, ok = fit_interval(gb, gr, n_region)
            per_gamma[f"g{g:g}"] = {"kmin": k1, "kmax": k2, "feasible": ok}
        elif gb:
            k1, _, _ = fit_interval(gb, [1e18], n_region)
            per_gamma[f"g{g:g}"] = {"kmin": k1, "kmax": None,
                                    "feasible": True,
                                    "note": "break-only (no rescue cell)"}
        else:
            _, k2, _ = fit_interval([0.0], gr, n_region)
            per_gamma[f"g{g:g}"] = {"kmin": None, "kmax": k2,
                                    "feasible": True,
                                    "note": "rescue-only (no break cell)"}
    print(f"  per-gamma (no-refit contrast): {json.dumps(per_gamma)}",
          flush=True)

    # ---- GATE-B4: the per-step ablation (exp134's functional here)
    amin, amax, aok = fit_interval(list(d_abl_break.values()),
                                   list(d_abl_rescue.values()), n_region)
    b4 = not aok
    abl_bb = max(break_cells, key=lambda c: d_abl_break[c]
                 if d_abl_break[c] > 0 else -1.0)
    abl_br = min(rescue_cells, key=lambda c: d_abl_rescue[c]
                 if d_abl_rescue[c] > 0 else float("inf"))
    print(f"  B4 ablation (per-step boundary exposure): kappa in "
          f"({amin:.4f}, {amax:.4f}) -> "
          f"{'INFEASIBLE (PASS)' if b4 else 'FEASIBLE (REFUTED)'}; "
          f"binding pair g{abl_bb[0]:g}_t{abl_bb[1]:g} vs "
          f"g{abl_br[0]:g}_t{abl_br[1]:g}", flush=True)

    # ---- R1: zero-free transfer to grid2d / path (flat-zero deposits)
    transfer = {}
    for name in ("grid2d", "path"):
        adj = battery[name]
        tot, agree, mism2 = 0, 0, []
        for g in GAMMAS:
            grid = TORUS_G1 if g == 1.0 else GRIDS[g]
            tpre = protocol_end(adj, g)
            for t in grid:
                if t > tpre + 1e-9:
                    continue
                tot += 1
                s = simulate(adj, g, float(t))
                p = kappa * debt(s, tau_star) / n_region
                if p <= ERR_BAR:
                    agree += 1
                else:
                    mism2.append(f"g{g:g}_t{t:g} pred {p:.2f}")
        transfer[name] = {"n_cells": tot, "agree": agree,
                          "mismatches": mism2[:8]}
        print(f"  R1 transfer {name}: {agree}/{tot} non-break agree "
              f"mismatches {mism2[:8]}", flush=True)

    # ---- R2: the zero-parameter mechanism check (direct sim edges)
    direct = {}
    for g in GAMMAS:
        grid = TORUS_G1 if g == 1.0 else GRIDS[g]
        de = None
        for t in grid:
            key = (g, float(t))
            if key in sim and sim[key]["err"] > ERR_BAR:
                de = float(t)
                break
        direct[f"g{g:g}"] = de
    print(f"  R2 direct-sim edges (kappa=1, no debt): {direct}",
          flush=True)

    # ---- R3: where the error lives at the binding transitions
    r3 = {}
    for key in ((16.0, 48.0), (16.0, 52.0), (4.0, 36.0), (4.0, 48.0),
                (1.0, 0.0), (64.0, 34.0)):
        s = sim[key]
        r3[f"g{key[0]:g}_t{key[1]:g}"] = {
            "err": round(s["err"], 3), "err_span": round(s["err_span"], 3),
            "err_intact": round(s["err_intact"], 3),
            "th_span_dev": round(s["th_span_dev"], 3)}
    print(f"  R3 decomposition: {json.dumps(r3)}", flush=True)

    # ---- R4: the marginal debt rate at the g16 transition
    if (16.0, 52.0) in sim:
        d48 = debt(sim[(16.0, 48.0)], tau_star)
        d52 = debt(sim[(16.0, 52.0)], tau_star)
        rate_d = (d52 - d48) / 4.0
        rate_err = kappa * rate_d / n_region
        d48a = debt(sim[(4.0, 36.0)], tau_star)
        d48b = debt(sim[(4.0, 48.0)], tau_star)
        rate_d4 = (d48b - d48a) / 12.0
        r4 = {"dD_dt_g16_transition": round(rate_d, 2),
              "kappa_rate_mV_per_h_g16": round(rate_err, 4),
              "dD_dt_g4_transition": round(rate_d4, 2),
              "kappa_rate_mV_per_h_g4":
                  round(kappa * rate_d4 / n_region, 4),
              "empirical_demand_mV_per_h": ERR_BAR / 4.0}
        print(f"  R4 marginal rates: {json.dumps(r4)}", flush=True)
    else:
        r4 = None

    npass = sum([b1, b2, b3, b4])
    print(f"\n  === {npass}/4 gates PASS ({time.time() - t_start:.0f}s) ===")

    result = {
        "exp": "exp135_walk_chain",
        "model": {
            "form": ("accumulated chain debt D(t*) = int_{24h}^{T_read} "
                     "exp(-(T_read-s)/tau_p) m(s) ds, m(s) = sum over "
                     "injected span cells of |theta_i - target_i|; "
                     "predicted_error = kappa D / 73; break iff > 6.0; "
                     "deterministic mean-field walk chain (harness Euler "
                     "update, multi-source BFS order, 8 sub-steps/cell, "
                     "injection at target), non-resetting state"),
            "free_params": ["kappa (transfer)", "tau_p (persistence, h)"],
            "tau_grid": list(TAU_GRID),
        },
        "fit": {
            "per_tau": [{k: r[k] for k in
                         ("tau_p", "kmin", "kmax", "feasible",
                          "binding_break", "binding_rescue")} for r in rows],
            "feasible": b3,
            "tau_p_star": tau_star,
            "kappa_interval": [kmin, kmax] if feas else None,
            "kappa_star": kappa if feas else None,
        },
        "torus_curve": curve_rows,
        "predicted_edges": {f"g{g:g}": e[g] for g in GAMMAS},
        "per_gamma_fits": per_gamma,
        "ablation": {"kmin": amin, "kmax": amax, "feasible": aok,
                     "binding_break": f"g{abl_bb[0]:g}_t{abl_bb[1]:g}",
                     "binding_rescue": f"g{abl_br[0]:g}_t{abl_br[1]:g}"},
        "transfer": transfer,
        "direct_sim_edges": direct,
        "decomposition": r3,
        "marginal_rates": r4,
        "criteria": {
            "B1_curve_reproduced": bool(b1),
            "B2_sign_rising": bool(b2),
            "B3_single_fit_no_refit": bool(b3),
            "B4_ablation_discriminates": bool(b4),
        },
        "notes": (
            "The walk-chain accumulation model (L114's registered "
            "object): the deadline as a threshold crossing of the "
            "persistence-kernel integral of the chain's theta-mismatch, "
            "the chain simulated as the harness's own deterministic "
            "walk with non-resetting state."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
