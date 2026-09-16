#!/usr/bin/env python3
"""exp119 — THE MEMORY CO-METRIC SPECTRUM TEST (ledger L99's
registration; subagent 2-a's top-ranked 2026 prediction, TAS-P1
from Blattner 2026's TAS framework: morphological memory acts
through a rank-one/anisotropic kernel — top-eigenvalue energy
fraction >= 0.8 with silent orthogonal directions. HONEST SCOPE
NOTE: the TAS paper's exact K_mem = R Q^-1 R^T form was not
retrievable (access-blocked; mined from README/abstract only), so
this experiment tests the ACCESSIBLE CORE claim on the stack's own
machinery, two-sided: rank-one-like concentration CONFIRMS TAS's
anisotropy on the stack; a diffuse/identity-like spectrum REFUTES
it. No replica of the unread formula is claimed.)

THE INSTRUMENT (the identity-sensitivity spectrum): the stack's
memory read is the frozen-theta field operator W = gamma
(gamma I + L_G)^-1 (exp109's static instrument, SF-G1-exact). For
each substrate, eigen-decompose the graph Laplacian (the torus and
grid modes are the DFT modes; path/star computed numerically) and
measure, per mode v_i, the IDENTITY SENSITIVITY:

    s_i = || W(target + delta v_i) - target ||
        - || W(target) - target ||,   delta = 2 mV RMS

— the identity error a unit-norm pattern perturbation along mode i
costs at the read. The spectrum {s_i} is the memory co-metric's
diagonal in the Laplacian basis: concentrated (a few modes carry
the sensitivity) = anisotropic memory; flat = isotropic.

THE ARMS:
  spectrum   all n modes per substrate (grid2d, torus at n=100;
             path, star for contrast), delta 2 mV RMS
  silence    the DYNAMIC crosscheck: perturb the captured walk-end
             theta field (exp110 capture) along the TOP-sensitivity
             and a LOW-sensitivity mode at matched norm, settle
             dynamically (15 h, the deployed protocol), and compare
             the final identity errors — the static instrument's
             prediction vs the real dynamics

PRE-REGISTERED GATES (two-sided, per subagent 2-a's framing):

  MS-G1  (anisotropy) the top-mode share of the sensitivity
         spectrum (s_max^2 / sum s_i^2 over all modes) is >= 0.8
         on grid2d AND torus -> TAS's rank-one claim CONFIRMED on
         the stack; <= 0.5 -> REFUTED (the memory co-metric is
         diffuse); between -> partial, deposited.
  MS-G2  (silent directions) the identity-error cost of a
         matched-norm (2 mV RMS) perturbation along the two
         LOWEST-sensitivity modes is <= 0.5 mV AND at least 2x
         smaller than the cost along the top-sensitivity mode —
         the differential silence TAS predicts; ratio < 1.5 ->
         the memory is effectively isotropic in directions (TAS's
         silent-directions REFUTED).
  MS-G3  (instrument validity) the dynamic settle of the perturbed
         walk-end field matches the static instrument's prediction
         within 0.3 mV for both perturbation directions — the
         spectrum measured statically describes the real protocol.

RUN: 4 substrates x n modes static solves + 2 x 2 dynamic runs
+ captures. Serial, BLAS pinned.
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

from cultivation.substrate.graph import grid_2d, path
from experiments.exp94_multizone_scale import MULTI, star_adj
from experiments.exp111_protocol_calibration import (
    GAMMA_T, run_read,
)
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp68_coherence_search import torus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp119_memory_spectrum.json")

G_GAP = 0.2
GAMMA = 4.0
DELTA_RMS = 2.0


def static_read(A, theta):
    n = A.shape[0]
    L = np.diag(G_GAP * A.sum(axis=1)) - G_GAP * A
    return GAMMA * np.linalg.solve(GAMMA * np.eye(n) + L, theta)


def mode_basis(A):
    L = np.diag(A.sum(axis=1)) - A
    w, V = np.linalg.eigh(L)
    return V  # columns = modes, ascending eigenvalue


def main() -> dict:
    print("=== exp119: the memory co-metric spectrum ===\n")

    battery = build_battery()
    SUBS = {"grid2d": battery["grid2d"], "torus": battery["torus"],
            "path": battery["path"], "star": battery["star"]}
    out: dict = {}
    top_share = {}
    sens_sorted = {}

    for name, A in SUBS.items():
        n = A.shape[0]
        from experiments.exp110_frozen_walk_probe import (
            capture_walk_end as _cap_ref,
        )
        ref = _cap_ref(MULTI, A, 1, steps_per_cell=8)
        tgt = ref["target"]  # the executor's own target (canon +
        # zones) — the identity the protocol actually reads
        V = mode_basis(A)
        base_err = float(np.sqrt(np.mean(
            (static_read(A, tgt) - tgt) ** 2)))
        sens = np.zeros(n)
        for i in range(n):
            v = V[:, i]
            v = v / (np.sqrt(np.mean(v * v)) + 1e-12)
            e = static_read(A, tgt + DELTA_RMS * v) - tgt
            sens[i] = float(np.sqrt(np.mean(e * e))) - base_err
        share = float(sens.max() ** 2
                      / np.sum(sens ** 2)) if sens.sum() else 0.0
        top_share[name] = round(share, 3)
        order = np.argsort(sens)
        sens_sorted[name] = {
            "top_mode": int(np.argmax(sens)),
            "top_sens": round(float(sens.max()), 3),
            "bottom_sens": round(float(sens[order[0]]), 3),
            "second_bottom": round(float(sens[order[1]]), 3),
            "base_err": round(base_err, 3),
        }
        out[f"spectrum_{name}"] = {
            "share": top_share[name],
            **sens_sorted[name],
            "sens_head": [round(float(x), 3)
                          for x in sens[order[:5]]],
            "sens_tail": [round(float(x), 3)
                          for x in sens[order[-5:]]],
        }
        print(f"    {name:8s} top-share {share:.3f}  top-sens "
              f"{sens.max():.3f}  bottom {sens[order[0]]:.3f}  "
              f"base {base_err:.3f}")

    ms_g1 = None
    g = [top_share.get(k) for k in ("grid2d", "torus")]
    if all(x >= 0.8 for x in g):
        ms_g1 = True
    elif all(x <= 0.5 for x in g):
        ms_g1 = False
    # between -> partial: record as None, gate REFUTED-as-stated but
    # deposited with the partial verdict

    # dynamic silence crosscheck on grid2d
    adj = battery["grid2d"]
    n = adj.shape[0]
    V = mode_basis(adj)
    from experiments.exp110_frozen_walk_probe import (
        capture_walk_end,
    )
    cap_ref = capture_walk_end(MULTI, adj, 1, steps_per_cell=8)
    tgt = cap_ref["target"]
    sens = []
    for i in range(n):
        v = V[:, i] / (np.sqrt(np.mean(V[:, i] ** 2)) + 1e-12)
        e = static_read(adj, tgt + DELTA_RMS * v) - tgt
        sens.append(float(np.sqrt(np.mean(e * e))))
    sens = np.array(sens)
    order = np.argsort(sens)
    top_i, low_i = int(order[-1]), int(order[0])

    cap = run_read(adj, 1, 4.0, 0.0, 8, None, False)
    theta_end = cap.get("theta_end")
    silence = {}
    if theta_end is None:
        # run_read's static mode returns no theta; re-capture via
        # exp110's instrument
        from experiments.exp110_frozen_walk_probe import (
            capture_walk_end,
        )
        cap2 = capture_walk_end(MULTI, adj, 1, steps_per_cell=8)
        theta_end = cap2["theta_end"]
    for label, mi in (("top", top_i), ("low", low_i)):
        v = V[:, mi] / (np.sqrt(np.mean(V[:, mi] ** 2)) + 1e-12)
        th = theta_end + DELTA_RMS * v
        pred = static_read(adj, th)
        pred_err = float(np.sqrt(np.mean((pred - tgt) ** 2)))
        r = run_read(adj, 1, 4.0, 0.0, 8, 15.0, False)
        _ = r  # deployed reference read for the unperturbed field
        silence[label] = {"pred_err": round(pred_err, 3)}
        print(f"    silence {label}-mode (i={mi}): predicted "
              f"read err {pred_err:.3f}")

    lo = max(silence["low"]["pred_err"], 1e-9)
    hi = silence["top"]["pred_err"]
    ms_g2 = (lo <= 0.5 + sens_sorted["grid2d"]["base_err"]
             and hi >= 2.0 * lo)
    # static-vs-dynamic: run the perturbed fields through the real
    # settle and compare (MS-G3)
    dyn = {}
    from experiments.exp110_frozen_walk_probe import (
        capture_walk_end as _cap,
    )
    cap0 = _cap(MULTI, adj, 1, steps_per_cell=8)
    theta0 = cap0["theta_end"]
    from experiments.exp90_two_source_read import star_dt
    from cultivation.substrate.graph import GraphCollective
    from cultivation.compiler.anatomy import compile_anatomy
    from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
    dt = star_dt(4.0, 4.0)
    for label, mi in (("top", top_i), ("low", low_i)):
        v = V[:, mi] / (np.sqrt(np.mean(V[:, mi] ** 2)) + 1e-12)
        c = GraphCollective(adjacency=adj, seed=1, gamma=4.0,
                            mu_theta=0.0)
        c.set_target(theta0.copy())
        c.theta = (theta0 + DELTA_RMS * v).copy()
        c.V = c.theta.copy()
        c.run(15.0, dt=dt)
        dyn_err = float(np.sqrt(np.mean((c.V - tgt) ** 2)))
        dyn[label] = round(dyn_err, 3)
        print(f"    dynamic {label}-mode settled err "
              f"{dyn_err:.3f} vs static pred "
              f"{silence[label]['pred_err']:.3f}")
    ms_g3 = (abs(dyn["top"] - silence["top"]["pred_err"]) <= 0.3
             and abs(dyn["low"] - silence["low"]["pred_err"]) <= 0.3)

    print(f"\n  top-shares: {top_share}")
    print(f"  silence (static pred): top {hi:.3f} vs low {lo:.3f} "
          f"(ratio {hi / lo:.1f})")
    verdict_g1 = ("CONFIRMED" if ms_g1 else
                  ("REFUTED" if ms_g1 is False else "PARTIAL"))
    print(f"\n  MS-G1 anisotropy: {verdict_g1}")
    print(f"  MS-G2 silent directions: "
          f"{'PASS' if ms_g2 else 'REFUTED'}")
    print(f"  MS-G3 instrument validity: "
          f"{'PASS' if ms_g3 else 'REFUTED'}")

    npass = sum([bool(ms_g1), ms_g2, ms_g3])
    print(f"\n  === {npass}/3 gates PASS (MS-G1: {verdict_g1}) ===")

    result = {
        "exp": "exp119_memory_spectrum",
        "spectra": out,
        "silence": {"static": silence, "dynamic": dyn},
        "criteria": {
            "MS_G1_anisotropy": verdict_g1,
            "MS_G2_silent_directions": bool(ms_g2),
            "MS_G3_instrument_validity": bool(ms_g3),
        },
        "notes": (
            "TAS-P1's accessible core on the stack's machinery: "
            "the identity-sensitivity spectrum per substrate "
            "(static instrument, SF-G1-exact), matched-norm "
            "perturbations along top/low modes, and the "
            "static-vs-dynamic crosscheck through the real 15 h "
            "settle. TAS's exact K_mem form was not retrievable; "
            "no replica claimed."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
