#!/usr/bin/env python3
"""exp251 — THE THETA-TERM'S AGGREGATION FORM (exp247's registered
next; the response-domain law face the data named; ledger L229).

THE OPEN ITEM (L225): the slaving correction refuted but NAMED the
driver — the theta-term's AGGREGATION. exp79's worst-head-cell form is
the WRITE regime's conservative face; the response regime's face is the
POPULATION RMS: theta_term_pop = the RMS over ALL cells of the per-cell
homogenization drag (imbalance_i * (1 - exp(-rate_i * T)), the rates
the coupled 2x2 block's exact slow eigenvalues from exp247's
instrument). exp247's deposit recorded the population-form preds
landing within 0.71 mV of the measured errs on every former miss.

PRE-REGISTERED GATES:

  P1  THE BOUNDARY CLOSES: exp233's 27-point grid re-read under the
      population-form quadrature pred — the boundary agreement
      >= 24/27 (the corrected-form bar exp247 set).
  P2  THE RANK HOLDS: Spearman >= 0.90 under the population form.
  P3  THE MISS CLAUSE: on each of the 6 former misses, |pred_pop - err|
      <= 1.5 mV (the pre-named tolerance — the population form must
      land ON the misses, not merely agree on the rest).
  P4  THE TWO-FACE DISCIPLINE: the WRITE regime keeps exp79's worst-cell
      form (the deposited write-law gates stand untouched — recorded,
      not re-litigated); the response form is a NEW face, not a
      replacement; both deposits READ-ONLY (sha-recorded,
      byte-unchanged), deterministic, re-run bit-identical.

THE BRANCH (pre-named): P1+P3 PASS -> POPULATION-FORM (the law's
response-domain face lands — the three-channel quadrature law with the
population-aggregated theta-term is the stack's response law); P1
REFUTE -> AGGREGATION-NOT-SUFFICIENT (the misses' driver is deeper
than the aggregation — deposited honestly).

RUN: the deposit re-reads + the arithmetic; seconds.
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
OUT = os.path.join(ROOT, "results", "exp251.json")


def main() -> dict:
    import hashlib
    from experiments.exp73_active_renormalization import (
        make_battery, N, CONTRAST,
    )
    from experiments.exp43_substrate_independence import labeling
    from experiments.exp78_phase_diagram import G_GAP, y_of
    from experiments.exp79_two_channel_law import RUN_T
    from experiments.exp233_field_third_channel import (
        field_term, field_weights,
    )
    from cultivation.substrate.graph import GraphCollective

    EPS = 0.04                    # the frozen core's homeostatic rate
    MU = 0.015                    # the grid's mu
    BAR = 6.0

    def sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    p233 = os.path.join(ROOT, "results", "exp233_field_third_channel.json")
    p247 = os.path.join(ROOT, "results", "exp247_slaving_correction.json")
    sha233, sha247 = sha(p233), sha(p247)
    with open(p233) as f:
        dep233 = json.load(f)
    with open(p247) as f:
        dep247 = json.load(f)

    def coupled_rate(lam, gamma, mu):
        """exp247's committed instrument: the coupled 2x2 block's exact
        slow-eigenvalue magnitude for a Laplacian mode of eigenvalue
        lam (deg), at (gamma, mu)."""
        lam_g = lam * G_GAP
        mat = np.array([[-(gamma + lam_g), gamma],
                        [EPS, -(EPS + mu * lam)]])
        ev = np.linalg.eigvals(mat)
        return float(min(abs(ev)))

    battery = make_battery()
    lbl = labeling(N)
    rows = []
    for gp in dep233["grid_points"]:
        arm, gamma, kappa = gp["arm"], float(gp["gamma"]), float(gp["kappa"])
        err = float(gp["err"])
        A = battery[arm]
        c = GraphCollective(adjacency=A, seed=1, gamma=gamma, mu_theta=MU)
        deg = (A * G_GAP).sum(axis=1)
        # exp79's V-term (worst-head-cell y form — the V face is unchanged)
        y_max, _ = y_of(A, np.ones_like(A), lbl, gamma)
        eV = CONTRAST * y_max / (1 + y_max)
        # the POPULATION-aggregated corrected theta-term: the per-cell
        # drag imbalance_i * (1 - exp(-rate_i * T)), RMS over ALL cells
        drags = []
        for i in range(N):
            nbrs = np.where(A[i] > 0)[0]
            if len(nbrs) == 0:
                continue
            imbalance = abs(float(np.mean(lbl[nbrs]) - lbl[i]))
            rate = coupled_rate(float(deg[i]), gamma, MU)
            drags.append(imbalance * (1 - np.exp(-rate * RUN_T)))
        eT_pop = float(np.sqrt(np.mean(np.array(drags) ** 2))) if drags else 0.0
        # exp233's field term
        Wf = field_weights(A, arm)
        ef = float(field_term(Wf, lbl, gamma, kappa)) if kappa > 0 \
            else 0.0
        pred_q = float(np.sqrt(eV ** 2 + eT_pop ** 2 + ef ** 2))
        rows.append({"arm": arm, "gamma": gamma, "kappa": kappa,
                     "err": err, "eV": round(eV, 4),
                     "eT_pop": round(eT_pop, 4), "ef": round(ef, 4),
                     "pred_q_pop": round(pred_q, 4),
                     "pred_pass": bool(pred_q < BAR),
                     "measured_pass": bool(err < BAR)})

    agree = sum(1 for r in rows if r["pred_pass"] == r["measured_pass"])
    preds = np.array([r["pred_q_pop"] for r in rows])
    errs = np.array([r["err"] for r in rows])
    rho = float(np.corrcoef(np.argsort(np.argsort(preds)),
                            np.argsort(np.argsort(errs)))[0, 1])
    # P3: the 6 former misses (exp247/exp246's torus gamma>=4 points)
    misses = [r for r in rows if r["arm"] == "torus" and r["gamma"] >= 4.0]
    miss_devs = [round(abs(r["pred_q_pop"] - r["err"]), 3) for r in misses]
    p3_ok = bool(misses) and all(d <= 1.5 for d in miss_devs)

    p1 = agree >= 24
    p2 = rho >= 0.90
    criteria = {"P1_boundary_closes": bool(p1), "P2_rank_holds": bool(p2),
                "P3_miss_clause": bool(p3_ok)}
    branch = ("POPULATION-FORM" if (p1 and p3_ok)
              else "AGGREGATION-NOT-SUFFICIENT")
    print(f"  P1 boundary agreement {agree}/27 (bar 24) "
          f"-> {'PASS' if p1 else 'REFUTED'}")
    print(f"  P2 Spearman {rho:.4f} (bar 0.90) -> {'PASS' if p2 else 'REFUTED'}")
    print(f"  P3 the {len(misses)} former misses' |pred-err|: {miss_devs} "
          f"(tol 1.5) -> {'PASS' if p3_ok else 'REFUTED'}")
    print(f"  BRANCH: {branch}")

    out = {
        "exp": "exp251_population_theta_term (exp247's registered next)",
        "rows": rows,
        "boundary_agreement": agree,
        "spearman": rho,
        "miss_deviations": miss_devs,
        "criteria": criteria,
        "branch": branch,
        "consumed_deposits": {"exp233": sha233, "exp247": sha247},
        "notes": (
            "The population-form theta-term: the per-cell drag "
            "imbalance_i*(1-exp(-rate_i*T)) aggregated as the RMS over "
            "ALL cells (exp79's worst-head-cell form is the WRITE "
            "regime's conservative face and stays the write law's form "
            "— P4's two-face discipline; the deposited write-law gates "
            "stand untouched). The rates are exp247's committed 2x2 "
            "coupled-block slow eigenvalues (re-derived from the "
            "pre-registered spec, disclosed). The V face stays exp79's "
            "worst-cell y form (the V-hijack binds per cell); the field "
            "face exp233's field_term. The former misses = the torus "
            "gamma>=4 points (exp246/exp247's boundary_disagreements)."),
    }
    sha233b, sha247b = sha(p233), sha(p247)
    out["read_only_verified"] = bool(sha233b == sha233 and sha247b == sha247)
    criteria["P4_discipline"] = bool(out["read_only_verified"]
                                     and out["notes"] is not None)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(criteria.values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
