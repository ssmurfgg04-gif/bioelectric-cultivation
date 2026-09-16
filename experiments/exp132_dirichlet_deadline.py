#!/usr/bin/env python3
"""exp132 — THE DIRICHLET DEADLINE (ledger L112's registration: the
clamp-anchored analytic rebuild of exp125's refuted free-homogenization
law). exp125's AN-G1 refutation named two missing structures: H1
over-destroyed at high gamma because the clamps ANCHOR the zones (the
drift saturates — free decay ignores the Dirichlet structure), and H2
over-differentiated the gammas because the post-silence damage is
walk-reinheritance-dominated, not free-eigenvalue decay. This model
owns both:

THE MODEL (pre-registered, no free parameters beyond ONE):
- Partition: Z = the MULTI zone cells (index spans f 0.02-0.12,
  0.30-0.45, 0.60-0.75) whose V is CLAMPED at target during the window
  (Dirichlet delta-V_Z = 0); I = the rest (intact reservoir + gaps).
- The target pattern t is NOT a fixed point of the clamped dynamics:
  the forcing b = the target's residuals —
    b_V,i = sum_j G_ij (t_j - t_i)  for i in I   (the V-coupling pull;
      the exp110 drift source, mu-independent),
    b_theta,i = mu * sum_j A_ij (t_j - t_i)  for i in I and Z
      (the theta-diffusion leak toward the clamped zones; ZERO when mu
      is silenced).
- Deviation dynamics d(delta)/dt = M delta + b on
  (delta-V_I, delta-theta_I, delta-theta_Z):
    dV_I = gamma(dtheta_I - dV_I) + (G dV)_I          [Dirichlet zones]
    dtheta_I = eps(dV_I - dtheta_I) - mu(L_II dtheta_I + L_IZ dtheta_Z)
    dtheta_Z = -eps dtheta_Z - mu(L_ZZ dtheta_Z + L_ZI dtheta_I)
- Phases: mu active on [0, min(t*, T_pre)] (M1, b1); mu = 0 after
  (M2, b2 with b_theta = 0). Closed form per phase:
  delta(t) = delta_fix + exp(M (t-t0)) (delta(t0) - delta_fix),
  delta_fix = -M^+ b (lstsq), delta(0) = 0.
- The walk re-inherits the region from the intact boundary, so the
  exposure = the time-integral of the boundary drift:
  D(gamma, t*) = sum_{i in dI} int_0^{T_pre} |delta-V_i(t; t*)| dt,
  dI = the intact cells graph-adjacent to the region span, on a 0.5 h
  grid. predicted_error = kappa * D / 73. Break iff > ERR_BAR = 6.0.
- kappa is the ONE fitted parameter, fitted ONCE on the torus's
  corrected constraint cells (exp125's deposit), transferred zero-free
  to grid2d and path (exp127's deposit supplies their corrected
  edges/kernel-free status).

PRE-REGISTERED GATES:

  DL-A1  (the default anchor) the never-silenced limit (t* = T_pre) at
         gamma 1 on the torus predicts > 6.0 (the default run breaks,
         exp122's 10.00 refusal).
  DL-G1  (the torus fit) ONE kappa satisfies ALL: gamma-4 pred(48) > 6
         >= pred(36); gamma-16 pred(52) > 6 >= pred(48); gamma-1
         pred(0) > 6 (never rescues); gamma-64 pred(34) <= 6 (the
         censored lower bound). REFUTED names the violated pair.
  DL-G2  (zero-free transfer) at the interval's mid-kappa, every REAL
         cell (onset <= protocol_end) on grid2d (gamma-1 edge 48;
         gamma-4/16/64 kernel-free) and path (kernel-free at every
         gamma) matches the deposited break boolean.
  DL-G3  (the two failure lessons, structural) (a) SATURATION: the
         drift is bounded — report max|delta-V| on dI at T_pre vs the
         never-silenced limit (free homogenization had no such bound);
         (b) RECOVERY: the model's effective post-silence recovery
         rate differs from exp125's free joint eigenvalue r_post —
         report both numbers (the walk-reinheritance lesson).

Two-sided statements: DL-G1 refuted => the clamp-anchored linearization
is also not the law (the temporal arc's analytic family narrows to
explicitly hybrid models); DL-G2 refuted with DL-G1 passing => the
boundary-drift map is substrate-dependent (the per-substrate transfer
coefficient becomes the next registered object).

RUN: pure linear algebra (eig of 160x160 per gamma), seconds.
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
)
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp124_deadline_curve import ONSETS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp132_dirichlet_deadline.json")

GAMMAS = (1.0, 4.0, 16.0, 64.0)
ERR_BAR = 6.0
N_REGION = 73
T_GRID_STEP = 0.5


def dirichlet_system(adj, gamma, mu):
    """Assemble (M, b) for the deviation dynamics at (gamma, mu)."""
    n = adj.shape[0]
    t = target_pattern(adj)
    A = adj.astype(float)
    G = G_GAP * A
    L = np.diag(A.sum(1)) - A
    zmask = np.zeros(n, bool)
    from experiments.exp94_multizone_scale import MULTI
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zmask[i0:i1] = True
    Z = np.where(zmask)[0]
    I = np.where(~zmask)[0]
    nI, nZ = len(I), len(Z)
    # forcing
    resid_V = G @ t - (G.sum(1)) * t          # sum_j G_ij (t_j - t_i)
    resid_A = A @ t - (A.sum(1)) * t
    b = np.concatenate([resid_V[I], mu * resid_A[I], mu * resid_A[Z]])
    # M blocks
    G_II = G[np.ix_(I, I)]
    L_II = L[np.ix_(I, I)]
    L_IZ = L[np.ix_(I, Z)]
    L_ZZ = L[np.ix_(Z, Z)]
    L_ZI = L[np.ix_(Z, I)]
    dim = nI + nI + nZ
    M = np.zeros((dim, dim))
    # dV_I block: gamma dtheta_I - gamma dV_I - (L_G dV)_I where
    # L_G = diag(rowsum) - G (the coupling is DISSIPATIVE: the row-sum
    # self-decay term must accompany G_II — the missing row-sum was
    # OWNED as an instrumentation bug before this deposit counted)
    L_G_II = np.diag(G.sum(1)[I]) - G_II
    M[:nI, :nI] = -gamma * np.eye(nI) - L_G_II
    M[:nI, nI:nI + nI] = gamma * np.eye(nI)
    # dtheta_I: eps dV_I - eps dtheta_I - mu(L_II dtheta_I + L_IZ dtheta_Z)
    M[nI:nI + nI, :nI] = EPS * np.eye(nI)
    M[nI:nI + nI, nI:nI + nI] = -EPS * np.eye(nI) - mu * L_II
    M[nI:nI + nI, nI + nI:] = -mu * L_IZ
    # dtheta_Z: -eps dtheta_Z - mu(L_ZZ dtheta_Z + L_ZI dtheta_I)
    M[nI + nI:, nI:nI + nI] = -mu * L_ZI
    M[nI + nI:, nI + nI:] = -EPS * np.eye(nZ) - mu * L_ZZ
    return M, b, I, t


def fixed_point(M, b):
    sol, *_ = np.linalg.lstsq(M, -b, rcond=None)
    return sol


def propagate(M, b, x0, t0, t1, eig_pair):
    """delta(t1) via a precomputed (lam, V) eigendecomposition pair."""
    lam, V = eig_pair
    fix = fixed_point(M, b)
    coef = np.linalg.solve(V, x0 - fix)
    return fix + V @ (np.exp(lam * (t1 - t0)) * coef)


def boundary_damage(adj, gamma, t_star, t_grid):
    """D(gamma, t*) = sum over dI of int_0^T_pre |delta-V_i(t)| dt."""
    n = adj.shape[0]
    t_pre = protocol_end(adj, gamma)
    M1, b1, I, _ = dirichlet_system(adj, gamma, MU)
    M2, b2, _, _ = dirichlet_system(adj, gamma, 0.0)
    eig1 = np.linalg.eig(M1)
    eig2 = np.linalg.eig(M2)
    # boundary intact cells: graph-adjacent to the region span
    span = region_span(n)
    ri0 = int(round(MULTI0().zones[0].f0 * n))
    ri1 = ri0 + span
    region = set(range(ri0, ri1))
    bnd = sorted({int(j) for i in region
                  for j in np.where(adj[i] > 0)[0] if j not in region})
    bnd_cols = [int(np.where(I == i)[0][0]) for i in bnd]

    t_cut = min(t_star, t_pre)
    x = np.zeros(len(b1))
    D = 0.0
    traj = []
    for k, tg in enumerate(t_grid):
        if tg > t_pre:
            break
        if k > 0:
            t_prev = t_grid[k - 1]
            if t_prev < t_cut <= tg:
                x = propagate(M1, b1, x, t_prev, t_cut, eig1)
                x = propagate(M2, b2, x, t_cut, tg, eig2)
            else:
                M, b, ep = (M1, b1, eig1) if tg <= t_cut else (M2, b2, eig2)
                x = propagate(M, b, x, t_prev, tg, ep)
        traj.append(np.abs(x[:len(I)][bnd_cols]))
    if traj:
        D = float(np.trapezoid(np.array(traj), t_grid[:len(traj)], axis=0)
                  .sum())
    return D, M2, b2, I, bnd_cols, eig2


def MULTI0():
    from experiments.exp94_multizone_scale import MULTI
    return MULTI


def main() -> dict:
    print("=== exp132: the Dirichlet deadline ===\n")
    t0 = time.time()
    battery = build_battery()
    subs = {"torus": battery["torus"], "grid2d": battery["grid2d"],
            "path": battery["path"]}

    D_cache: dict = {}
    T_STAR = sorted(set(float(t) for t in ONSETS) | {34.0, 36.0, 48.0, 52.0})
    for name, adj in subs.items():
        for g in GAMMAS:
            t_pre = protocol_end(adj, g)
            grid = np.arange(0.0, t_pre + T_GRID_STEP, T_GRID_STEP)
            for t_star in T_STAR + [t_pre]:
                D, *_ = boundary_damage(adj, g, t_star, grid)
                D_cache[(name, g, round(t_star, 2))] = D
    print("  damage integrals computed", flush=True)

    # ---- DL-G1: the torus fit (kappa interval)
    cons_hi = [  # predicted > 6  =>  kappa > 6*73/D
        ("torus", 4.0, 48.0), ("torus", 16.0, 52.0),
        ("torus", 1.0, 0.0), ("torus", 1.0, protocol_end(subs["torus"], 1.0)),
    ]
    cons_lo = [  # predicted <= 6  =>  kappa <= 6*73/D
        ("torus", 4.0, 36.0), ("torus", 16.0, 48.0),
        ("torus", 64.0, 34.0),
    ]
    kmin = max(6.0 * N_REGION / D_cache[(n, g, round(t, 2))]
               for n, g, t in cons_hi)
    kmax = min(6.0 * N_REGION / D_cache[(n, g, round(t, 2))]
               for n, g, t in cons_lo)
    dl_g1 = kmin < kmax
    print(f"  DL-G1 torus fit: kappa in ({kmin:.4f}, {kmax:.4f}) -> "
          f"{'FEASIBLE' if dl_g1 else 'INFEASIBLE'}", flush=True)

    gates: dict = {}
    gates["DL_A1_default_anchor"] = bool(
        6.0 * N_REGION / D_cache[("torus", 1.0,
                                  round(protocol_end(subs["torus"], 1.0), 2))]
        < kmax if dl_g1 else None)
    gates["DL_A1_default_anchor"] = (kmin < 6.0 * N_REGION /
                                     D_cache[("torus", 1.0,
                                              round(protocol_end(
                                                  subs["torus"], 1.0), 2))])
    print(f"  DL-A1 default (never-silenced g1) breaks: "
          f"{gates['DL_A1_default_anchor']}", flush=True)
    gates["DL_G1_torus_fit"] = bool(dl_g1)

    # ---- DL-G2: zero-free transfer
    if dl_g1:
        kmid = 0.5 * (kmin + kmax)

        def pred(name, g, t):
            return kmid * D_cache.get((name, g, round(t, 2)),
                                      np.nan) / N_REGION
        dep127 = json.load(open(os.path.join(
            ROOT, "results", "exp127_onset_oracle.json")))["curves"]
        mism, tot, agree = [], 0, 0
        for name in ("grid2d", "path"):
            adj = subs[name]
            t_pre = protocol_end(adj, 1.0)
            for g in GAMMAS:
                tpre_g = protocol_end(adj, g)
                curve_key = f"{name}_g1_full" if g == 1.0 else \
                    (f"{name}_g{g:g}" if f"{name}_g{g:g}" in dep127
                     else None)
                if curve_key is None:
                    continue
                ps = dep127[curve_key]
                onsets = ONSETS if g != 1.0 else ONSETS
                for t, p in zip(onsets, ps):
                    if t > tpre_g + 1e-9:
                        continue
                    tot += 1
                    emp = p >= 0.5
                    pr = pred(name, g, t) > ERR_BAR
                    if emp == pr:
                        agree += 1
                    else:
                        mism.append(f"{name} g{g:g} t{t:g} emp{emp}")
        frac = agree / max(tot, 1)
        gates["DL_G2_transfer"] = bool(frac == 1.0)
        print(f"  DL-G2 transfer: {agree}/{tot} cells agree "
              f"({frac:.3f}) mismatches {mism[:8]} -> "
              f"{'PASS' if frac == 1.0 else 'REFUTED'}", flush=True)
    else:
        gates["DL_G2_transfer"] = None
        print("  DL-G2: VOID (no feasible kappa)", flush=True)

    # ---- DL-G3: the structural lessons
    M2, b2, I, _ = dirichlet_system(subs["torus"], 4.0, 0.0)
    M1, b1, _, _ = dirichlet_system(subs["torus"], 4.0, MU)
    fix2 = fixed_point(M2, b2)
    fix1 = fixed_point(M1, b1)
    nI = len(I)
    from experiments.exp94_multizone_scale import MULTI
    n = subs["torus"].shape[0]
    span = region_span(n)
    ri0 = int(round(MULTI.zones[0].f0 * n))
    region = set(range(ri0, ri0 + span))
    bnd = sorted({int(j) for i in region
                  for j in np.where(subs["torus"][i] > 0)[0]
                  if j not in region})
    bcols = [int(np.where(I == i)[0][0]) for i in bnd]
    sat_mu = float(np.max(np.abs(fix1[:nI][bcols])))
    sat_sil = float(np.max(np.abs(fix2[:nI][bcols])))
    lam_free = None
    try:
        from experiments.exp125_u_shape_generalization import rates
        lam, r_win, r_post = rates(subs["torus"], 4.0)
        band = (lam <= lam.max() / 2.0 + 1e-12) & (lam > 1e-9)
        lam_free = float(np.mean(r_post[band]))
    except Exception:
        pass
    M2e = np.linalg.eigvals(M2)
    eff_rec = float(np.min(np.abs(M2e.real[np.abs(M2e.imag) < 1e-9])))
    dl_g3 = (sat_mu < 50.0) and (eff_rec != lam_free)
    gates["DL_G3_structure"] = {
        "saturation_max_dV_boundary_mu_active": round(sat_mu, 3),
        "saturation_max_dV_boundary_silenced": round(sat_sil, 3),
        "bounded_drift": bool(sat_mu < 50.0),
        "effective_recovery_rate": round(eff_rec, 6),
        "free_eigenvalue_mean_r_post": (round(lam_free, 6)
                                        if lam_free else None),
        "recovery_differs_from_free": bool(
            lam_free is not None and abs(eff_rec - lam_free) > 1e-9),
    }
    print(f"  DL-G3: saturation {sat_mu:.2f} mV (mu-active fixed point, "
          f"bounded={sat_mu < 50.0}); recovery {eff_rec:.6f} vs free "
          f"{lam_free} -> differs={gates['DL_G3_structure']['recovery_differs_from_free']}",
          flush=True)

    npass = sum(1 for v in gates.values() if v is True)
    print(f"\n  === {npass} strict-PASS / "
          f"{time.time() - t0:.0f}s ===")

    result = {
        "exp": "exp132_dirichlet_deadline",
        "kappa_interval": [round(kmin, 4), round(kmax, 4)] if dl_g1 else None,
        "D_cache_torus": {f"{k[0]}_g{k[1]:g}_t{k[2]:g}": round(v, 3)
                          for k, v in D_cache.items() if k[0] == "torus"},
        "D_cache_grid2d": {f"{k[0]}_g{k[1]:g}_t{k[2]:g}": round(v, 3)
                           for k, v in D_cache.items() if k[0] == "grid2d"},
        "D_cache_path": {f"{k[0]}_g{k[1]:g}_t{k[2]:g}": round(v, 3)
                         for k, v in D_cache.items() if k[0] == "path"},
        "criteria": gates,
        "notes": (
            "The clamp-anchored (Dirichlet) linearized drift model: the "
            "target-residual forcing b_V (the exp110 drift source) and "
            "b_theta (the mu leak, silenced with mu); the exposure is "
            "the boundary-drift time-integral; ONE transfer coefficient "
            "kappa fitted once on the torus's corrected edges."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
