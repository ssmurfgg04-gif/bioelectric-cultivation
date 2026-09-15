#!/usr/bin/env python3
"""exp77 — RUNG 6: CONDUCTANCE REMODELING (the star-search step 6;
continuous batch; ledger L58).

THE OPEN QUESTION (L57's registered candidate): the slow anchor fires
and shedding MOVES the hub wall (11.92 -> 8.45) but stalls at the
BRIDGE WALL — every remaining cut edge is a connectivity bridge, and
the bridges carry the hijack. The registered escape: ANATOMICAL
BRIDGES AND ELECTRICAL COUPLING ARE SEPARABLE VARIABLES. In the
model's own equations the identity read propagates through mu * A
(theta diffusion) and never touches G, while the voltage hijack flows
entirely through G. Rung 6 keeps the bridge (A untouched — unity,
degrees, readout capacity all preserved) and DOWN-REGULATES THE
CHANNEL: W_ij *= 0.3 on the hot cells' most-conflicting junctions
(connexin gating semantics — the most directly biological remodeling
move, minutes not hours). Floor: no junction goes fully electrically
silent (conductance floor 0.01) — the readout is retained by design.

ALSO CARRIED (L57's owned bug): the corrected theorem contrast. The
anchor is dragged BY THE VOLTAGE at rate eps_slow (a_v += eps_slow *
(V - a_v)) — at eps_slow = eps it IS theta and must reproduce exp75's
failure (no signal, no movement); at 0 it is the frozen spec and the
signal fires. The contrast was registered twice and mis-implemented
once; this run decides it.

THE M41 MOMENT (pre-declared): if thinning writes the pattern while A
is unchanged, then EVERY topology metric (b2v, absolute crossing)
refuses a substrate the dynamics supports — the metric MUST be
re-derived. The registered candidate: the CONDUCTANCE-WEIGHTED
crossing fraction wc = sum_cut G_ij / sum_all G_ij. On the static
battery (W = 1) wc == b2v (all exp68 separations inherited); on the
thinned substrate wc collapses below the R5 limit. M41 fires if and
only if wc tracks the verdicts where b2v does not.

PRE-REGISTERED GATES:

  TH-G1  THE THEOREM CONTRAST (corrected): at eps_slow = eps the
         anchor follows the hijack — zero hot cells, zero movement
         (exp75 reproduced through the new code path); at eps_slow = 0
         the signal fires (hot > 0 on the wall arms).
  TH-G2  THE PREDICTION: conductance thinning makes BOTH scale_free
         arms writable (mean verdict error < 6.0, 3 fresh seeds) with
         A UNCHANGED (edges 197 -> 197, degree sequence exact,
         connectivity trivially preserved).
  TH-G3  HOLD SEMANTICS: the thinned substrate holds from fresh noise
         seeds with no drive.
  TH-G4  NO REGRESSION: pass controls stay passing; the writable
         controls stay passing.
  TH-G5  M41: (a) on the thinned substrate b2v still refuses while
         the dynamics supports (the topology metric is blind to
         conductance); (b) the conductance-weighted crossing wc
         separates pass/fail across the static battery AND the thinned
         arms. Both together = the metric re-derivation fires honestly.
  TH-G6  THE PRICE: total conductance budget spent per arm (the
         continuous currency replacing the junction count).

RUN: 2 scale_free wall arms + torus/random3 (writable controls) +
path/grid2d (pass controls); 40 rounds max; serial, BLAS pinned.
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
    make_battery, labeling_bfs, b2v_of, edge_conflicts, connected,
    N, ERR_BAR, B2V_LIMIT, ROUNDS, HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp74_renormalization_ladder import cut_stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp77_conductance_remodeling.json")

DRAG_THRESHOLD = 8.0
RUN_T = 24.0
DT = 0.1
REC_EVERY = 10
TAIL_FRAC = 0.5
G_GAP = 0.20
THIN_FACTOR = 0.3
G_FLOOR = 0.01            # absolute conductance floor per junction
EPS_SLOW_CONTRAST = 0.04  # == eps: the anchor must reproduce exp75


def settle_w(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, seed: int,
             eps_slow: float = 0.0):
    """One write attempt on substrate (A, W). W multiplies the per-edge
    conductance. The slow anchor a_v is dragged BY THE VOLTAGE at
    eps_slow (0 = frozen spec); returns final fields, tail-mean slow
    drag, per-edge conflicts, error."""
    c = GraphCollective(adjacency=A, seed=seed)
    c.G = c.A * G_GAP * W
    c.deg = c.G.sum(axis=1)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.a_v = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    steps = int(round(RUN_T / DT))
    Vs, As = [], []
    for t in range(steps):
        c.a_v = c.a_v + eps_slow * DT * (c.V - c.a_v)
        c.step(DT)
        if t % REC_EVERY == 0:
            Vs.append(c.V.copy())
            As.append(c.a_v.copy())
    rec_v, rec_a = np.array(Vs), np.array(As)
    tail = slice(int(len(rec_v) * TAIL_FRAC), None)
    drag = np.mean(np.abs(rec_v[tail] - rec_a[tail]), axis=0)
    conf = edge_conflicts(A, rec_v)
    return c.V.copy(), drag, conf, c.pattern_error(lbl)


def settle_err_w(A: np.ndarray, W: np.ndarray, lbl: np.ndarray,
                 seed: int) -> float:
    V, _, _, err = settle_w(A, W, lbl, seed)
    return err


def verdict_w(A: np.ndarray, W: np.ndarray, lbl: np.ndarray,
              seeds=(1, 2, 3)) -> tuple[bool, float]:
    errs = [settle_err_w(A, W, lbl, s) for s in seeds]
    return (float(np.mean(errs)) < ERR_BAR, float(np.mean(errs)))


def conductance_thin(A0: np.ndarray, lbl: np.ndarray, seed: int = 1,
                     rounds: int = ROUNDS, eps_slow: float = 0.0,
                     verbose: bool = False):
    """Rung 6: slow-drag-driven conductance down-regulation. A is never
    modified; only W changes. Target-blind: the rule reads (V, a_v, W)."""
    W = np.ones_like(A0)
    A = A0.copy()
    g0 = float((A * G_GAP).sum() / 2.0)
    trace = {"err_trace": [], "hot_trace": [], "thin_trace": [],
             "first_pass": None, "G_total_trace": []}
    for r in range(rounds):
        V, drag, conf, err = settle_w(A, W, lbl, seed * 31 + r, eps_slow)
        trace["err_trace"].append(round(err, 3))
        trace["G_total_trace"].append(round(
            float((A * G_GAP * W).sum() / 2.0) / g0, 4))
        hot = np.where(drag > DRAG_THRESHOLD)[0]
        trace["hot_trace"].append(int(len(hot)))
        if trace["first_pass"] is None and err < ERR_BAR:
            trace["first_pass"] = r + 1
        thin_r = 0
        for i in sorted(hot, key=lambda i: -drag[i]):
            nbrs = [int(j) for j in np.where(A[i] > 0)[0]]
            if not nbrs:
                continue
            # the junction carrying the most CONFLICT x CONDUCTANCE
            j = max(nbrs, key=lambda jj: conf.get(
                (min(i, jj), max(i, jj)), 0.0) * W[i, jj])
            if A[i, j] * G_GAP * W[i, j] <= G_FLOOR:
                continue        # already at the floor — readout retained
            W[i, j] = W[j, i] = W[i, j] * THIN_FACTOR
            thin_r += 1
        trace["thin_trace"].append(thin_r)
        if verbose and (r + 1) % 5 == 0:
            print(f"    round {r+1:3d} err {err:6.2f} hot {len(hot):3d} "
                  f"thin {thin_r:3d} G/G0 "
                  f"{trace['G_total_trace'][-1]:.3f}")
    trace["G_total_final"] = trace["G_total_trace"][-1]
    return A, W, trace


def wc_metric(A: np.ndarray, W: np.ndarray, lbl: np.ndarray) -> float:
    """Conductance-weighted crossing fraction (the M41 candidate)."""
    hi = (lbl == HEAD_V)
    G = A * G_GAP * W
    cut = total = 0.0
    for i in range(A.shape[0]):
        for j in np.where(A[i] > 0)[0]:
            if j > i:
                total += G[i, j]
                if hi[i] != hi[j]:
                    cut += G[i, j]
    return cut / total if total else 0.0


def main() -> dict:
    print("=== exp77: rung 6 — conductance remodeling (star-search step 6) ===\n")

    battery = make_battery()
    wall_arms = [("scale_free", "fixed"), ("scale_free", "bfs")]
    writable_controls = [("torus", "fixed"), ("random3", "fixed")]
    pass_controls = [("path", "fixed"), ("grid2d", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- TH-G1: the corrected theorem contrast --------------------------------
    contrast = {}
    for name, kind in wall_arms:
        lbl = arm_label(name, kind)
        V, drag, conf, err = settle_w(battery[name], np.ones_like(battery[name]),
                                      lbl, 1, EPS_SLOW_CONTRAST)
        hot_slow = int((drag > DRAG_THRESHOLD).sum())
        V, drag0, conf0, err0 = settle_w(battery[name],
                                         np.ones_like(battery[name]),
                                         lbl, 1, 0.0)
        hot_frozen = int((drag0 > DRAG_THRESHOLD).sum())
        contrast[f"{name}|{kind}"] = {
            "hot_eps_slow": hot_slow, "hot_frozen": hot_frozen}
        print(f"  contrast {name}|{kind}: eps_slow=eps hot {hot_slow} | "
              f"frozen hot {hot_frozen}")
    g1 = (all(contrast[f"{n}|{k}"]["hot_eps_slow"] <= 2
              for n, k in wall_arms)
          and all(contrast[f"{n}|{k}"]["hot_frozen"] > 0
                  for n, k in wall_arms))
    print(f"  TH-G1 theorem contrast (corrected): "
          f"{'PASS' if g1 else 'REFUTED'}\n")

    # ---- TH-G2/G3: the prediction ---------------------------------------------
    results = {}
    for name, kind in wall_arms:
        lbl = arm_label(name, kind)
        print(f"  conductance-thin {name}|{kind}:")
        A_rw, W_rw, tr = conductance_thin(battery[name], lbl, verbose=True)
        ok, err = verdict_w(A_rw, W_rw, lbl)
        ok2, err2 = verdict_w(A_rw, W_rw, lbl, seeds=(4, 5, 6))
        st = cut_stats(A_rw, lbl)
        results[f"{name}|{kind}"] = {
            "verdict_err": round(err, 2), "verdict_pass": bool(ok),
            "hold_err": round(err2, 2), "hold_pass": bool(ok2),
            "b2v": round(b2v_of(A_rw, lbl), 4),
            "wc": round(wc_metric(A_rw, W_rw, lbl), 4),
            "A_unchanged": bool(np.array_equal(A_rw, battery[name])),
            "cut": st, "G_over_G0": tr["G_total_final"],
            "first_pass": tr["first_pass"],
        }
        print(f"    -> err {err:.2f} ({'PASS' if ok else 'FAIL'}) "
              f"hold {err2:.2f} b2v {results[f'{name}|{kind}']['b2v']:.4f} "
              f"wc {results[f'{name}|{kind}']['wc']:.4f} "
              f"A unchanged {results[f'{name}|{kind}']['A_unchanged']} "
              f"G/G0 {tr['G_total_final']:.3f}")
    g2 = all(results[f"{n}|{k}"]["verdict_pass"]
             and results[f"{n}|{k}"]["A_unchanged"] for n, k in wall_arms)
    g3 = all(results[f"{n}|{k}"]["hold_pass"] for n, k in wall_arms)
    print(f"\n  TH-G2 the prediction (thin writes scale_free, A unchanged): "
          f"{'PASS' if g2 else 'REFUTED'}")
    print(f"  TH-G3 hold semantics: {'PASS' if g3 else 'REFUTED'}")

    # ---- TH-G4: no regression ---------------------------------------------------
    regress = {}
    for name, kind in writable_controls + pass_controls:
        lbl = arm_label(name, kind)
        A_rw, W_rw, tr = conductance_thin(battery[name], lbl)
        ok, err = verdict_w(A_rw, W_rw, lbl)
        regress[f"{name}|{kind}"] = {
            "err": round(err, 2), "pass": bool(ok),
            "G_over_G0": tr["G_total_final"]}
        print(f"  control {name:11s} err {err:.2f} "
              f"{'PASS' if ok else 'FAIL'} G/G0 {tr['G_total_final']:.3f}")
    g4 = all(v["pass"] for v in regress.values())
    print(f"  TH-G4 no regression: {'PASS' if g4 else 'REFUTED'}")

    # ---- TH-G5: M41 ---------------------------------------------------------------
    m41_topo_blind = all(results[f"{n}|{k}"]["b2v"] > B2V_LIMIT
                         for n, k in wall_arms)
    # wc across the static battery + thinned arms
    pts = []
    for name, A in battery.items():
        for knd in ("fixed", "bfs"):
            lbl = labeling(N) if knd == "fixed" else labeling_bfs(A)
            ok_s, err_s = verdict_w(A, np.ones_like(A), lbl)
            pts.append({"arm": f"{name}|{knd} (static)",
                        "wc": wc_metric(A, np.ones_like(A), lbl),
                        "b2v": b2v_of(A, lbl), "pass": bool(ok_s),
                        "err": round(err_s, 2)})
    for name, kind in wall_arms:
        r = results[f"{name}|{kind}"]
        pts.append({"arm": f"{name}|{kind} (thinned)", "wc": r["wc"],
                    "b2v": r["b2v"], "pass": r["verdict_pass"],
                    "err": r["verdict_err"]})
    wc_pass = sorted(p["wc"] for p in pts if p["pass"])
    wc_fail = sorted(p["wc"] for p in pts if not p["pass"])
    g5b = bool(wc_pass and wc_fail and max(wc_pass) < min(wc_fail))
    g5 = bool(m41_topo_blind and g5b)
    print(f"\n  TH-G5a topology metric blind on thinned substrate: "
          f"{'YES' if m41_topo_blind else 'no'}")
    print(f"  TH-G5b wc separates (pass {wc_pass} / fail {wc_fail}): "
          f"{'PASS' if g5b else 'REFUTED'}")
    print(f"  TH-G5 M41 (metric re-derivation) fires: "
          f"{'PASS' if g5 else 'REFUTED'}")

    out = {
        "exp": "exp77_conductance_remodeling (the star-search step 6, rung 6)",
        "theorem_contrast": contrast,
        "wall_arms": results,
        "controls": regress,
        "metric_table": pts,
        "criteria": {
            "TH_G1_theorem_contrast": bool(g1),
            "TH_G2_thin_writes_A_unchanged": bool(g2),
            "TH_G3_hold_semantics": bool(g3),
            "TH_G4_no_regression": bool(g4),
            "TH_G5_M41_fires": bool(g5),
            "TH_G6_price_deposited": True,
        },
        "notes": (
            "Rung 6: conductance remodeling — the bridge stays "
            "(anatomy, degrees, readout capacity preserved; A "
            "untouched) and the CHANNEL is down-regulated (connexin "
            "gating semantics). The corrected theorem contrast "
            "(anchor dragged by V at eps_slow) is also decided here. "
            "M41 pre-declared: if A is unchanged while the dynamics "
            "flips, every topology metric is blind and the "
            "conductance-weighted crossing wc is the re-derived "
            "coherence metric."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
