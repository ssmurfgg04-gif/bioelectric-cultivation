#!/usr/bin/env python3
"""exp239 — THE COUPLING-PLASTICITY FAILURE MODE (the Section 6 item;
Zenodo 21459264's symbol-grounding parallel; ledger L215).

THE CLAIM TESTED: under coupling plasticity (the junction weights
themselves remodel — exp77's drag remodeling, exp78's G-thinning), a
GLOBAL ENERGY FUNCTION may cease to exist for the coupled dynamics —
the "coupling plasticity" failure mode of symbol grounding. The stack's
dynamics at fixed G are a linear coupled system (dV = gamma*(theta-V) +
G-coupling; dtheta = eps*(V-theta) + mu*lap(theta)) — at fixed G a
quadratic Lyapunov function EXISTS (the standard Lyapunov equation).
The question: does the fixed-G Lyapunov certificate survive G's
remodeling, and does the coherence constraint (the maintained pattern's
zone structure) protect it?

THE INSTRUMENT (zero-knob): E(x) = x^T P x with x = (V - theta, theta
- lbl) the deviation state and P the Lyapunov solution of the fixed-G
block system at the star point (P from the discrete Lyapunov equation
on the linearized update operator M: M^T P M - P = -Q, Q = I — solved
exactly by numpy on the stacked operator, no fitting). The test walks
sampled trajectories and checks dE <= 0 at every step.

PRE-REGISTERED GATES:

  E1  THE FIXED-G BASELINE: E decreases along every sampled trajectory
      at the star (gamma=64, mu=0, fixed G; 3 arms x 3 seeds x 200
      steps, zero violations within float tolerance) — the certificate
      exists on the frozen dynamics.
  E2  THE REMODELING BREAK: under G-remodeling (exp77's drag remodeling
      protocol verbatim — the junction weights updated every pre-named
      10 steps by the drag rule), the fixed-G certificate's dE computed
      WITH THE STALE P turns positive on a pre-named fraction of
      remodel steps (>= 1 violation per trajectory on >= 1/3 of
      trajectories): the fixed-G energy is NOT a global energy under
      plasticity — the failure mode fires.
  E3  THE COHERENCE PROTECTION: with the coherence clamp on (the
      pattern maintained at the star: the write held, no wound), the
      remodeling trajectories show dE <= 0 throughout (the maintained
      pattern's neighborhood keeps the certificate locally valid) —
      the constraint's protective effect, the grounding's price
      structure named.
  E4  THE TIME-VARYING CERTIFICATE (the honest extension): the
      pointwise-fresh Lyapunov solution P_t (re-solved at each remodel
      step for the CURRENT G) restores dE <= 0 everywhere — the system
      is not gradient-free, it is gradient-MOVING: a global energy
      exists only piecewise-in-time under plasticity; the failure mode
      is the single fixed E, not the dynamics.

THE BRANCH (pre-named): E2 fires + E4 restores -> PLASTICITY-BOUNDED
(the failure mode is real and LOCALIZED: coupling plasticity breaks
any FIXED global energy while a time-varying certificate persists —
the symbol-grounding parallel grounded computationally); E2 does not
fire -> REMODEL-SAFE (the stack's remodeling preserves the fixed
certificate — deposited honestly).

RUN: the trajectory panels + the Lyapunov solves (the 100x100 stacked
operator, eigen-free solve); serial, BLAS pinned; minutes.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp239_coupling_plasticity.json")


def main() -> dict:
    from experiments.exp73_active_renormalization import (
        make_battery, N, edge_conflicts,
    )
    from experiments.exp43_substrate_independence import labeling
    from experiments.exp77_conductance_remodeling import (
        DRAG_THRESHOLD, THIN_FACTOR, G_GAP, G_FLOOR, EPS_SLOW_CONTRAST,
    )
    from cultivation.substrate.graph import GraphCollective

    STAR_GAMMA, STAR_MU = 64.0, 0.0
    WRITE_GAMMA, WRITE_MU = 0.25, 0.015   # exp77's own write regime
    DT_MAX = 0.1
    N_STEPS = 200
    REMODEL_EVERY = 10          # exp77's REC_EVERY discipline, step-level
    TOL = 1e-8                  # dE <= TOL * max(1, |E|) counts as <= 0
    SEEDS = (1, 2, 3)
    ARMS = ("scale_free", "random3", "torus")
    WOUND = slice(40, 60)       # exp79 TC-G6's mid wound
    N2 = 2 * N

    # the gauge direction: the uniform (V, theta) shift is an EXACT
    # conserved mode of the coupled dynamics at ANY (gamma, mu) (the
    # cancellation G@1 == deg and lap(1) == 0) — exp234's gauge mode
    # reappearing inside the certificate. The Lyapunov certificate lives
    # on the quotient: project it out everywhere (zero-knob, disclosed).
    g_hat = np.concatenate([np.zeros(N), np.ones(N)])
    g_hat /= np.linalg.norm(g_hat)
    P_g = np.eye(N2) - np.outer(g_hat, g_hat)

    def new_collective(A, seed, gamma, mu):
        c = GraphCollective(adjacency=A, seed=seed, gamma=gamma,
                            mu_theta=mu)
        c.noise_std = 0.0       # the certificate's condition: noise-free
        c.set_target(lbl)
        return c

    def dt_rule(c, gamma):
        return min(DT_MAX, 1.2 / (gamma + float(c.deg.max())))

    def lyapunov_P(M):
        from scipy.linalg import solve_discrete_lyapunov
        P = solve_discrete_lyapunov(M.T, np.eye(M.shape[0]),
                                    method="bilinear")
        return 0.5 * (P + P.T)

    def one_step_map(c, dt, gamma, mu):
        """The exact affine one-step map on the deviation y = (V-theta,
        theta-lbl): f(y) = M y + b, recovered exactly (linear dynamics)."""

        def f(y):
            c.V = y[:N] + y[N:] + lbl
            c.theta = y[N:] + lbl
            c.step(dt)
            return np.concatenate([c.V - c.theta, c.theta - lbl])

        b = f(np.zeros(N2))
        M = np.zeros((N2, N2))
        for k in range(N2):
            e = np.zeros(N2)
            e[k] = 1.0
            M[:, k] = f(e) - b
        return M, b

    def certificate(c, dt, gamma, mu):
        """The gauge-projected fixed-G certificate: (M_perp, P, y*)."""
        M, b = one_step_map(c, dt, gamma, mu)
        M_perp = P_g @ M @ P_g
        # the affine fixed point in y, projected
        y_star = np.linalg.solve(np.eye(N2) - M, b)
        y_star = y_star - float(y_star @ g_hat) * g_hat
        return M_perp, lyapunov_P(M_perp), y_star

    def E_of(y, P, y_star):
        x = y - y_star
        x = x - float(x @ g_hat) * g_hat
        return float(x @ P @ x)

    print("=== exp239: the coupling-plasticity failure mode ===\n")
    battery = make_battery()
    lbl = labeling(N)
    results = {"E1": [], "E2": [], "E3": [], "E4": [], "audit": []}

    for arm in ARMS:
        A = battery[arm]
        for seed in SEEDS:
            # ---- E1: the fixed-G baseline AT THE STAR (pre-named) ------
            c_dt = new_collective(A, seed, STAR_GAMMA, STAR_MU)
            c_dt.G = c_dt.A * G_GAP
            c_dt.deg = c_dt.G.sum(axis=1)
            dt_star = dt_rule(c_dt, STAR_GAMMA)
            cM = new_collective(A, seed, STAR_GAMMA, STAR_MU)
            cM.G = cM.A * G_GAP
            cM.deg = cM.G.sum(axis=1)
            M_s, b_s = one_step_map(cM, dt_star, STAR_GAMMA, STAR_MU)
            # the EXACT affine fixed point by the linear solve (the
            # epsilon-slaved relaxation has rho ~ 0.998 — iterating to
            # 1e-12 would need ~10^4 steps; the solve is exact)
            y_star_s = np.linalg.solve(np.eye(N2) - M_s, b_s)
            M_perp = P_g @ M_s @ P_g
            P_s = lyapunov_P(M_perp)
            specrad = float(max(abs(np.linalg.eigvals(M_perp))))

            rng = np.random.default_rng(seed * 97 + 5)
            y_start = y_star_s + rng.normal(0.0, 2.0, N2)
            c1 = new_collective(A, seed, STAR_GAMMA, STAR_MU)
            c1.G = c1.A * G_GAP
            c1.deg = c1.G.sum(axis=1)
            c1.V = y_start[:N] + y_start[N:] + lbl
            c1.theta = y_start[N:] + lbl
            E1s = []
            for _t in range(N_STEPS):
                c1.step(dt_star)
                E1s.append(E_of(np.concatenate([c1.V - c1.theta,
                                                c1.theta - lbl]),
                                P_s, y_star_s))
            viol1 = sum(1 for i in range(1, len(E1s))
                        if E1s[i] > E1s[i - 1]
                        + TOL * max(1.0, abs(E1s[i - 1])))
            results["E1"].append({"arm": arm, "seed": seed,
                                  "spectral_radius": specrad,
                                  "n_violations": int(viol1),
                                  "E_first": round(E1s[0], 6),
                                  "E_last": round(E1s[-1], 12),
                                  "monotone": bool(viol1 == 0)})

            # ---- E2/E4: exp77's write regime (the drag lives there) ----
            c_w = new_collective(A, seed, WRITE_GAMMA, WRITE_MU)
            c_w.G = c_w.A * G_GAP
            c_w.deg = c_w.G.sum(axis=1)
            dt_w = dt_rule(c_w, WRITE_GAMMA)
            M_w, b_w = one_step_map(c_w, dt_w, WRITE_GAMMA, WRITE_MU)
            y_star_w = np.linalg.solve(np.eye(N2) - M_w, b_w)
            P_w = lyapunov_P(P_g @ M_w @ P_g)

            def make_remodel(log):
                def remodel(cc, a_v, drag_win):
                    drag = np.mean(np.abs(drag_win), axis=0)
                    hot = np.where(drag > DRAG_THRESHOLD)[0]
                    if len(hot) == 0:
                        return
                    conf = edge_conflicts(A, np.array([cc.V]))
                    for i in sorted(hot, key=lambda i: -drag[i]):
                        nbrs = [int(j) for j in np.where(A[i] > 0)[0]]
                        if not nbrs:
                            continue
                        j = max(nbrs, key=lambda jj: conf.get(
                            (min(i, jj), max(i, jj)), 0.0)
                            * (cc.G[i, jj] / G_GAP))
                        if cc.G[i, j] <= G_FLOOR:
                            continue
                        cc.G[i, j] *= THIN_FACTOR
                        cc.G[j, i] *= THIN_FACTOR
                        cc.deg = cc.G.sum(axis=1)
                        log["thinned"] += 1
                    log["rounds"] += 1
                return remodel

            def wound_traj(gamma, mu, dt, remodel_hook, n_steps=N_STEPS):
                """Settled start -> wound -> relax, the slow anchor a_v
                dragged at exp77's eps_slow, the drag rule every
                REMODEL_EVERY steps. Returns (E-list with the STALE
                (P_w, y_star_w) certificate, remodel log, final c)."""
                c = new_collective(A, seed, gamma, mu)
                c.G = c.A * G_GAP
                c.deg = c.G.sum(axis=1)
                c.theta = y_star_w[N:] + lbl
                c.V = y_star_w[:N] + y_star_w[N:] + lbl
                c.amputate(WOUND)
                a_v = lbl.copy()
                log = {"rounds": 0, "thinned": 0}
                remodel = make_remodel(log)
                drag_win = []
                Es = []
                for t in range(n_steps):
                    a_v = a_v + EPS_SLOW_CONTRAST * dt * (c.V - a_v)
                    c.step(dt)
                    drag_win.append(c.V - a_v)
                    Es.append(E_of(np.concatenate([c.V - c.theta,
                                                   c.theta - lbl]),
                                   P_w, y_star_w))
                    if (t + 1) % REMODEL_EVERY == 0:
                        if remodel_hook is not None:
                            remodel(c, a_v, np.array(drag_win))
                        drag_win = []
                return Es, log, c

            E2s, log2, _ = wound_traj(WRITE_GAMMA, WRITE_MU, dt_w,
                                      "drag")
            viol2 = sum(1 for i in range(1, len(E2s))
                        if E2s[i] > E2s[i - 1]
                        + TOL * max(1.0, abs(E2s[i - 1])))
            results["E2"].append({"arm": arm, "seed": seed,
                                  "n_violations": int(viol2),
                                  "remodel_rounds": log2["rounds"],
                                  "edges_thinned": log2["thinned"],
                                  "E_first": round(E2s[0], 3),
                                  "E_last": round(E2s[-1], 6)})

            # ---- E3: the coherence clamp AT THE STAR (pre-named) -------
            c3 = new_collective(A, seed, STAR_GAMMA, STAR_MU)
            c3.G = c3.A * G_GAP
            c3.deg = c3.G.sum(axis=1)
            c3.V = y_star_s[:N] + y_star_s[N:] + lbl
            c3.theta = y_star_s[N:] + lbl
            log3 = {"rounds": 0, "thinned": 0}
            remodel3 = make_remodel(log3)
            E3s = []
            for t in range(N_STEPS):
                c3.step(dt_star)
                E3s.append(E_of(np.concatenate([c3.V - c3.theta,
                                                c3.theta - lbl]),
                                P_s, y_star_s))
                if (t + 1) % REMODEL_EVERY == 0:
                    if float(np.max(np.abs(c3.V - c3.theta)))                             > DRAG_THRESHOLD:
                        remodel3(c3, None, np.array([c3.V - c3.theta]))
            viol3 = sum(1 for i in range(1, len(E3s))
                        if E3s[i] > E3s[i - 1]
                        + TOL * max(1.0, abs(E3s[i - 1])))
            results["E3"].append({
                "arm": arm, "seed": seed, "n_violations": int(viol3),
                "remodel_rounds": log3["rounds"],
                "max_drag": round(float(np.max(np.abs(c3.V - c3.theta))), 4),
                "E_last": round(E3s[-1], 12)})

            # the audit arm (non-gating): FORCED thinning at the star —
            # the adversarial probe: thin the top-conflict edge every
            # REMODEL_EVERY steps REGARDLESS of drag.
            c3f = new_collective(A, seed, STAR_GAMMA, STAR_MU)
            c3f.G = c3.A * G_GAP
            c3f.deg = c3f.G.sum(axis=1)
            c3f.V = y_star_s[:N] + y_star_s[N:] + lbl
            c3f.theta = y_star_s[N:] + lbl
            E3f = []
            forced = 0
            for t in range(N_STEPS):
                c3f.step(dt_star)
                E3f.append(E_of(np.concatenate([c3f.V - c3f.theta,
                                                c3f.theta - lbl]),
                                P_s, y_star_s))
                if (t + 1) % REMODEL_EVERY == 0 and forced < 5:
                    conf = edge_conflicts(A, np.array([c3f.V]))
                    (i, j) = max(conf, key=lambda e: conf[e])
                    if c3f.G[i, j] > G_FLOOR:
                        c3f.G[i, j] *= THIN_FACTOR
                        c3f.G[j, i] *= THIN_FACTOR
                        c3f.deg = c3f.G.sum(axis=1)
                        forced += 1
            fviol = sum(1 for i in range(1, len(E3f))
                        if E3f[i] > E3f[i - 1]
                        + TOL * max(1.0, abs(E3f[i - 1])))
            results["audit"].append({"arm": arm, "seed": seed,
                                     "forced_thinnings": forced,
                                     "n_violations": int(fviol)})

            # ---- E4: the time-varying certificate (the write regime) ---
            c4 = new_collective(A, seed, WRITE_GAMMA, WRITE_MU)
            c4.G = c4.A * G_GAP
            c4.deg = c4.G.sum(axis=1)
            c4.theta = y_star_w[N:] + lbl
            c4.V = y_star_w[:N] + y_star_w[N:] + lbl
            c4.amputate(WOUND)
            a_v = lbl.copy()
            viol4 = 0
            cur_P, cur_ystar = P_w, y_star_w
            seg_prev = None
            drag_win = []
            for t in range(N_STEPS):
                a_v = a_v + EPS_SLOW_CONTRAST * dt_w * (c4.V - a_v)
                c4.step(dt_w)
                drag_win.append(c4.V - a_v)
                if (t + 1) % REMODEL_EVERY == 0:
                    cM_t = new_collective(A, seed, WRITE_GAMMA, WRITE_MU)
                    cM_t.G = c4.G.copy()
                    cM_t.deg = c4.deg.copy()
                    cur_M, cur_b = one_step_map(cM_t, dt_w, WRITE_GAMMA,
                                                WRITE_MU)
                    cur_ystar = np.linalg.solve(np.eye(N2) - cur_M, cur_b)
                    cur_ystar = cur_ystar                         - float(cur_ystar @ g_hat) * g_hat
                    cur_P = lyapunov_P(P_g @ cur_M @ P_g)
                    cur_M_perp = None
                    seg_prev = None
                    remodel4 = make_remodel({"rounds": 0, "thinned": 0})
                    remodel4(c4, a_v, np.array(drag_win))
                    drag_win = []
                E4_t = E_of(np.concatenate([c4.V - c4.theta,
                                            c4.theta - lbl]),
                            cur_P, cur_ystar)
                if seg_prev is not None:
                    if E4_t > seg_prev + TOL * max(1.0, abs(seg_prev)):
                        viol4 += 1
                seg_prev = E4_t
            results["E4"].append({"arm": arm, "seed": seed,
                                  "n_violations": int(viol4)})

    # ---- gate evaluation -------------------------------------------------
    e1_ok = all(r["monotone"] for r in results["E1"]) and         all(r["spectral_radius"] < 1.0 - 1e-9 for r in results["E1"])
    n_traj_with_viol = sum(1 for r in results["E2"]
                           if r["n_violations"] >= 1)
    n_remodeling = sum(1 for r in results["E2"] if r["remodel_rounds"] >= 1)
    e2_fires = bool(n_traj_with_viol >= len(results["E2"]) / 3.0
                    and n_remodeling >= len(results["E2"]) / 3.0)
    e3_ok = all(r["n_violations"] == 0 for r in results["E3"])
    e4_ok = all(r["n_violations"] == 0 for r in results["E4"])

    branch = ("PLASTICITY-BOUNDED" if (e2_fires and e4_ok)
              else "REMODEL-SAFE" if not e2_fires else "MIXED")
    criteria = {"E1_fixed_g_baseline": bool(e1_ok),
                "E2_remodeling_break_fires": e2_fires,
                "E3_coherence_protection": bool(e3_ok),
                "E4_time_varying_certificate_restores": bool(e4_ok)}
    print(f"  E1 fixed-G baseline: "
          f"{sum(r['monotone'] for r in results['E1'])}/9 monotone, "
          f"projected spectral radius "
          f"{max(r['spectral_radius'] for r in results['E1']):.10f} "
          f"-> {'PASS' if e1_ok else 'REFUTED'}")
    print(f"  E2 remodeling break: {n_traj_with_viol}/9 trajectories with "
          f">=1 stale-P violation ({n_remodeling}/9 remodeled, "
          f"{sum(r['edges_thinned'] for r in results['E2'])} edges thinned) "
          f"-> {'FIRES' if e2_fires else 'does not fire'}")
    print(f"  E3 coherence protection: "
          f"{sum(r['n_violations'] == 0 for r in results['E3'])}/9 clean, "
          f"max drag {max(r['max_drag'] for r in results['E3']):.3f} "
          f"(threshold {DRAG_THRESHOLD}) "
          f"-> {'PASS' if e3_ok else 'REFUTED'}")
    print(f"  E4 time-varying certificate: "
          f"{sum(r['n_violations'] == 0 for r in results['E4'])}/9 clean "
          f"-> {'PASS' if e4_ok else 'REFUTED'}")
    faudit = sum(r["n_violations"] for r in results["audit"])
    print(f"  audit (non-gating): the forced-thinning arm at the star "
          f"violates on {faudit} steps across 9 trajectories")
    print(f"  BRANCH: {branch}")

    out = {
        "exp": "exp239_coupling_plasticity (the Section 6 item)",
        "results": results,
        "criteria": criteria,
        "branch": branch,
        "notes": (
            "OPERATIONALIZATIONS (the docstring byte-unchanged): (1) the "
            "certificate trajectories are noise-free (noise_std=0.0 — the "
            "Lyapunov theorem's condition; the randomness lives in the "
            "sampled starts via fresh seeds). (2) THE GAUGE QUOTIENT: the "
            "uniform (V,theta) shift is an EXACT conserved mode of the "
            "coupled dynamics at any (gamma, mu) (exp234's gauge mode — "
            "the raw stacked map carries rho=1 and the raw Lyapunov solve "
            "is singular); the certificate lives on the gauge-orthogonal "
            "quotient (the projector P_g = I - g g^T, g the uniform "
            "direction), zero-knob, applied to every E. (3) The deviation "
            "state is the docstring's (V-theta, theta-lbl); the fixed "
            "point is the affine map's own (projected) fixed point by the "
            "exact linear solve. (4) The one-step map M recovered EXACTLY "
            "by finite differences (the dynamics are linear). (5) The "
            "discrete Lyapunov solve is scipy's Schur-form "
            "solve_discrete_lyapunov(method='bilinear') — the Kronecker "
            "direct form is memory-fatal at n2=200. (6) E2/E4 run at "
            "exp77's OWN write regime (gamma=0.25, mu=0.015 — the "
            "protocol-verbatim reading: the drag rule lives there; at the "
            "star's gamma=64 the V-theta drag decays below the threshold "
            "within one remodel window and the rule never fires — 0/9 "
            "remodels, disclosed), with exp77's slow anchor a_v dragged "
            "at eps_slow and the drag = the trailing-window mean |V - a_v| "
            "> 8.0, THIN_FACTOR 0.3, floor 0.01; the E2 certificate is "
            "built for the trajectory's OWN operator (the stale-P "
            "violations then isolate the REMODELING, not the gamma). (7) "
            "E3's protective effect has a mechanism face: at the coherent "
            "star the drag is ~0 and the remodeler never fires (the "
            "max-drag datum recorded); the audit arm forces the thinning "
            "adversarially (non-gating, disclosed)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(criteria.values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
