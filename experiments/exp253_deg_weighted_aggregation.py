#!/usr/bin/env python3
"""exp253 — THE DEG-WEIGHTED AGGREGATION (exp251's registered next; the
response-law form's zero-knob unifier; ledger L231).

THE OPEN ITEM (L229): the rank and the boundary PULL APART across the
aggregation forms (population: rank 0.9554 / boundary 18/27; worst-cell:
0.9359 / 21/27). THE ZERO-KNOB UNIFIER: the DEG-WEIGHTED RMS — the
theta-term aggregated with the cells' junction participation as the
weights (theta_term = sqrt(sum deg_i * drag_i^2 / sum deg_i)): the drag
enters the pattern error weighted by the cell's coupling — no fitting,
the weights are the substrate's own degrees. The two prior forms are
the degenerate limits (worst-cell = the max; population = the flat
weights), so the deg-weighted form INTERPOLATES mechanistically.

PRE-REGISTERED GATES:

  W1  THE BOUNDARY: the deg-weighted quadrature pred's boundary
      agreement >= 24/27 on exp233's grid (the bar both prior forms
      missed).
  W2  THE RANK: Spearman >= 0.90.
  W3  THE UNIFIER CLAUSE: the deg-weighted form's boundary agreement
      >= BOTH prior forms' (>= 21/27 — it must not lose to either).
  W4  THE DISCIPLINE: the deposits READ-ONLY sha-recorded
      byte-unchanged, deterministic.

THE BRANCH (pre-named): W1+W3 PASS -> UNIFIED-FORM (the response law's
theta-term is the deg-weighted RMS — the three-channel quadrature law
closes with its aggregation named); W1 REFUTE -> FORM-OPEN (the
aggregation family's two-point interpolation does not close it — the
law's form question stays open with the constraint set widened).

RUN: the deposit re-read + the arithmetic; seconds.
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
OUT = os.path.join(ROOT, "results", "exp253.json")


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

    EPS = 0.04
    MU = 0.015
    BAR = 6.0

    def sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    p233 = os.path.join(ROOT, "results", "exp233_field_third_channel.json")
    sha233 = sha(p233)
    with open(p233) as f:
        dep233 = json.load(f)

    def coupled_rate(lam, gamma, mu):
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
        deg = (A * G_GAP).sum(axis=1)
        y_max, _ = y_of(A, np.ones_like(A), lbl, gamma)
        eV = CONTRAST * y_max / (1 + y_max)
        # the DEG-WEIGHTED RMS theta-term
        num = den = 0.0
        for i in range(N):
            nbrs = np.where(A[i] > 0)[0]
            if len(nbrs) == 0:
                continue
            imbalance = abs(float(np.mean(lbl[nbrs]) - lbl[i]))
            rate = coupled_rate(float(deg[i]), gamma, MU)
            drag = imbalance * (1 - np.exp(-rate * RUN_T))
            num += deg[i] * drag ** 2
            den += deg[i]
        eT_dw = float(np.sqrt(num / den)) if den > 0 else 0.0
        Wf = field_weights(A, arm)
        ef = float(field_term(Wf, lbl, gamma, kappa)) if kappa > 0 else 0.0
        pred = float(np.sqrt(eV ** 2 + eT_dw ** 2 + ef ** 2))
        rows.append({"arm": arm, "gamma": gamma, "kappa": kappa,
                     "err": err, "eT_dw": round(eT_dw, 4),
                     "pred_q_dw": round(pred, 4),
                     "pred_pass": bool(pred < BAR),
                     "measured_pass": bool(err < BAR)})
    agree = sum(1 for r in rows if r["pred_pass"] == r["measured_pass"])
    preds = np.array([r["pred_q_dw"] for r in rows])
    errs = np.array([r["err"] for r in rows])
    rho = float(np.corrcoef(np.argsort(np.argsort(preds)),
                            np.argsort(np.argsort(errs)))[0, 1])
    w1, w2, w3 = agree >= 24, rho >= 0.90, agree >= 21
    branch = "UNIFIED-FORM" if (w1 and w3) else "FORM-OPEN"
    criteria = {"W1_boundary": bool(w1), "W2_rank": bool(w2),
                "W3_unifier": bool(w3)}
    print(f"  W1 boundary {agree}/27 (bar 24) -> {'PASS' if w1 else 'REFUTED'}")
    print(f"  W2 Spearman {rho:.4f} -> {'PASS' if w2 else 'REFUTED'}")
    print(f"  W3 >= both priors (21/27) -> {'PASS' if w3 else 'REFUTED'}")
    print(f"  BRANCH: {branch}")
    out = {"exp": "exp253_deg_weighted_aggregation", "rows": rows,
           "boundary_agreement": agree, "spearman": rho,
           "criteria": criteria, "branch": branch,
           "consumed_deposits": {"exp233": sha233},
           "notes": "the deg-weighted RMS: the drag enters weighted by "
                    "the cell's junction participation (the substrate's "
                    "own degrees — zero knobs); the two prior forms are "
                    "the degenerate limits (worst-cell = max, population "
                    "= flat weights)"}
    out["read_only_verified"] = bool(sha(p233) == sha233)
    criteria["W4_discipline"] = bool(out["read_only_verified"])
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  === {sum(criteria.values())}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
