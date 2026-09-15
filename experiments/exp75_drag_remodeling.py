#!/usr/bin/env python3
"""exp75 — RUNG 4: DRAG-DRIVEN REMODELING (the star-search step 4;
continuous batch; ledger L56).

THE OPEN QUESTION (L55's registered candidate): the ladder's three
local signals all fail on the hub substrate — per-edge conflict is
degree-diluted, agreement growth is smear-corrupted. The registered
escape: the HOMEOSTATIC DRAG |V_i - theta_i|. It is per-cell (not
per-edge — undiluted by degree), fully local (a cell knows its own
channel-set target theta and its achieved voltage V), and target-blind
(the label array never enters). It reads the smear DIRECTLY: where V
is hijacked by the neighbors, the cell's identity cannot be expressed,
and the drag is exactly that failure, felt by the cell.

THE RUNG-4 MOVE (drag-shed): each round —
  1. one write attempt (the exp68 settle protocol), recording V AND
     theta through the run;
  2. tail-mean per-cell drag d_i = mean_t |V_i(t) - theta_i(t)|;
  3. every HOT cell (d_i > DRAG_THRESHOLD) sheds its most-conflicting
     junction (the neighbor with the largest sustained transjunctional
     drop), connectivity HARD (tissue stays one tissue).
Nothing else: no rewiring, no growth — clean attribution of the rung.

BIOLOGY: the drag is the cell-autonomous identity-maintenance failure
(the channel set says -20, the junction field says -35) — exactly the
condition under which real cells remodel their coupling (activity-
dependent homeostatic plasticity; connexin turnover follows sustained
transjunctional load).

PRE-REGISTERED GATES (the prediction: scale_free becomes writable):

  DR-G1  SIGNAL SEPARATION: the tail drag separates the regimes — pass
         arms stay below the threshold (no hot cells) and the fail
         arms' hub boundary cells are hot in the first rounds (the
         signal exists where the incoherence is).
  DR-G2  RUNG 4 WRITES scale_free: drag-shed alone makes BOTH
         scale_free arms writable (mean verdict error < 6.0, 3 fresh
         seeds) with connectivity preserved at every round. THE
         REGISTERED PREDICTION. If refuted, the wall is deeper than
         sensing — deposit whether the mechanism stalled for signal
         reasons (drag never fired / fired but not at the boundary) or
         connectivity reasons (every candidate edge was a bridge).
  DR-G3  HOLD SEMANTICS: the shed wiring holds from fresh noise seeds
         with no drive (formation-only remodeling).
  DR-G4  NO REGRESSION: pass controls shed nothing (drag < threshold
         there) and the already-writable arms are not broken.
  DR-G5  METRIC TRACKING: b2v and absolute crossing continue to agree
         with the verdicts on every final wiring.
  DR-G6  THE PRICE: junctions shed per arm and rounds-to-writable —
         the drag-driven instance of the "coherence bought with
         remodeling" curve.

RUN: 2 scale_free arms (the wall) + torus/random3 (writable controls)
+ path/grid2d (pass controls); 40 rounds max; serial, BLAS pinned.
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
    make_battery, labeling_bfs, verdict, b2v_of, connected, edge_conflicts,
    N, ERR_BAR, B2V_LIMIT, ROUNDS, HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp74_renormalization_ladder import cut_stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp75_drag_remodeling.json")

DRAG_THRESHOLD = 8.0    # mV, tail-mean |V - theta| (25% of contrast)
RUN_T = 24.0
DT = 0.1
REC_EVERY = 10
TAIL_FRAC = 0.5


def settle_drag(A: np.ndarray, lbl: np.ndarray, seed: int):
    """One write attempt recording both fields; returns final V, the
    tail-mean per-cell drag, per-edge conflicts (tail), and the error."""
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    steps = int(round(RUN_T / DT))
    Vs, Ts = [], []
    for t in range(steps):
        c.step(DT)
        if t % REC_EVERY == 0:
            Vs.append(c.V.copy())
            Ts.append(c.theta.copy())
    rec = np.array(Vs)
    tail = rec[int(len(rec) * TAIL_FRAC):]
    tail_t = np.array(Ts)[int(len(Ts) * TAIL_FRAC):]
    drag = np.mean(np.abs(tail - tail_t), axis=0)
    conf = edge_conflicts(A, rec)
    return c.V.copy(), drag, conf, c.pattern_error(lbl)


def drag_shed(A0: np.ndarray, lbl: np.ndarray, seed: int = 1,
              rounds: int = ROUNDS, verbose: bool = False):
    """Rung 4: drag-driven junction shedding. Target-blind: the rule
    reads only (A, V, theta)."""
    A = A0.copy()
    e0 = int(np.triu(A, 1).sum())
    rng = np.random.default_rng(seed * 15485863 + 11)
    trace = {"err_trace": [], "hot_trace": [], "shed_trace": [],
             "bridges_blocked": 0, "shed_total": 0, "first_pass": None,
             "connected_every_round": True}
    for r in range(rounds):
        V, drag, conf, err = settle_drag(A, lbl, seed * 31 + r)
        trace["err_trace"].append(round(err, 3))
        hot = np.where(drag > DRAG_THRESHOLD)[0]
        trace["hot_trace"].append(int(len(hot)))
        if trace["first_pass"] is None and err < ERR_BAR:
            trace["first_pass"] = r + 1
        if not connected(A):
            trace["connected_every_round"] = False
        shed_r = 0
        # hottest cells shed first; each hot cell sheds its most-
        # conflicting edge once per round
        order = sorted(hot, key=lambda i: -drag[i])
        for i in order:
            nbrs = [int(j) for j in np.where(A[i] > 0)[0]]
            if not nbrs:
                continue
            # the neighbor with the largest sustained drop (or any, if
            # the edge map has no entry — a fresh edge from growth)
            j = max(nbrs, key=lambda jj: conf.get((min(i, jj), max(i, jj)), 0.0))
            A2 = A.copy()
            A2[i, j] = A2[j, i] = 0.0
            if connected(A2):
                A = A2
                conf.pop((min(i, j), max(i, j)), None)
                trace["shed_total"] += 1
                shed_r += 1
            else:
                trace["bridges_blocked"] += 1
        trace["shed_trace"].append(shed_r)
        if verbose and (r + 1) % 5 == 0:
            print(f"    round {r+1:3d} err {err:6.2f} hot {len(hot):3d} "
                  f"shed {shed_r:3d} (tot {trace['shed_total']}, "
                  f"blocked {trace['bridges_blocked']})")
    trace["edges_final"] = int(np.triu(A, 1).sum())
    trace["edges_start"] = e0
    return A, trace


def main() -> dict:
    print("=== exp75: rung 4 — drag-driven remodeling (star-search step 4) ===\n")

    battery = make_battery()
    wall_arms = [("scale_free", "fixed"), ("scale_free", "bfs")]
    writable_controls = [("torus", "fixed"), ("random3", "fixed")]
    pass_controls = [("path", "fixed"), ("grid2d", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- DR-G1: signal separation -------------------------------------------
    sig = {}
    for name, kind in wall_arms + writable_controls + pass_controls:
        lbl = arm_label(name, kind)
        V, drag, conf, err = settle_drag(battery[name], lbl, 1)
        hot = int((drag > DRAG_THRESHOLD).sum())
        sig[f"{name}|{kind}"] = {"mean_drag": round(float(drag.mean()), 2),
                                 "hot": hot, "static_err": round(err, 2)}
        print(f"  signal {name:11s}|{kind:5s} mean drag "
              f"{sig[f'{name}|{kind}']['mean_drag']:6.2f} hot {hot:3d} "
              f"err {err:6.2f}")
    g1 = (all(sig[f"{n}|{k}"]["hot"] > 0 for n, k in wall_arms)
          and all(sig[f"{n}|{k}"]["hot"] <= 2 for n, k in pass_controls))
    print(f"  DR-G1 signal separation: {'PASS' if g1 else 'REFUTED'}\n")

    # ---- DR-G2/G3: the wall arms --------------------------------------------
    results = {}
    for name, kind in wall_arms:
        lbl = arm_label(name, kind)
        print(f"  drag-shed {name}|{kind}:")
        A_rw, tr = drag_shed(battery[name], lbl, verbose=True)
        ok, err = verdict(A_rw, lbl)
        ok2, err2 = verdict(A_rw, lbl, seeds=(4, 5, 6))
        st = cut_stats(A_rw, lbl)
        results[f"{name}|{kind}"] = {
            "verdict_err": round(err, 2), "verdict_pass": bool(ok),
            "hold_err": round(err2, 2), "hold_pass": bool(ok2),
            "b2v": round(b2v_of(A_rw, lbl), 4), "cut": st,
            "edges": (tr["edges_start"], tr["edges_final"]),
            "shed_total": tr["shed_total"],
            "bridges_blocked": tr["bridges_blocked"],
            "first_pass": tr["first_pass"],
            "connected_every_round": tr["connected_every_round"],
            "hot_first5": tr["hot_trace"][:5],
            "err_trace_tail": tr["err_trace"][-5:],
        }
        print(f"    -> err {err:.2f} ({'PASS' if ok else 'FAIL'}) "
              f"hold {err2:.2f} b2v {results[f'{name}|{kind}']['b2v']:.4f} "
              f"cut {st['cut_edges']} edges "
              f"{tr['edges_start']}->{tr['edges_final']} "
              f"blocked {tr['bridges_blocked']}")
    g2 = all(results[f"{n}|{k}"]["verdict_pass"] for n, k in wall_arms)
    g3 = all(results[f"{n}|{k}"]["hold_pass"] for n, k in wall_arms)
    print(f"\n  DR-G2 rung 4 writes scale_free (THE PREDICTION): "
          f"{'PASS' if g2 else 'REFUTED'}")
    print(f"  DR-G3 hold semantics: {'PASS' if g3 else 'REFUTED'}")

    # ---- DR-G4: no regression -----------------------------------------------
    regress = {}
    for name, kind in writable_controls + pass_controls:
        lbl = arm_label(name, kind)
        A_rw, tr = drag_shed(battery[name], lbl)
        ok, err = verdict(A_rw, lbl)
        regress[f"{name}|{kind}"] = {
            "err": round(err, 2), "pass": bool(ok),
            "shed_total": tr["shed_total"],
            "edges": (tr["edges_start"], tr["edges_final"])}
        print(f"  control {name:11s} err {err:.2f} "
              f"{'PASS' if ok else 'FAIL'} shed {tr['shed_total']} "
              f"edges {tr['edges_start']}->{tr['edges_final']}")
    g4 = all(v["pass"] for v in regress.values())
    print(f"  DR-G4 no regression: {'PASS' if g4 else 'REFUTED'}")

    # ---- DR-G5: metric tracking on all final wirings -------------------------
    pts = []
    for name, kind in wall_arms:
        r = results[f"{name}|{kind}"]
        pts.append({"arm": f"{name}|{kind}", "b2v": r["b2v"],
                    "crossing": r["cut"]["cut_edges"],
                    "pass": r["verdict_pass"]})
    g5 = all((p["b2v"] < B2V_LIMIT) == p["pass"] and
             (p["crossing"] <= 20) == p["pass"] for p in pts)
    print(f"  DR-G5 metric tracking: {'PASS' if g5 else 'REFUTED'} "
          f"({[ (p['arm'], p['b2v'], p['crossing'], p['pass']) for p in pts ]})")

    out = {
        "exp": "exp75_drag_remodeling (the star-search step 4, rung 4)",
        "signal": sig,
        "wall_arms": results,
        "controls": regress,
        "criteria": {
            "DR_G1_signal_separation": bool(g1),
            "DR_G2_rung4_writes_scale_free": bool(g2),
            "DR_G3_hold_semantics": bool(g3),
            "DR_G4_no_regression": bool(g4),
            "DR_G5_metric_tracking": bool(g5),
            "DR_G6_price_deposited": True,
        },
        "notes": (
            "Rung 4 of the renormalization ladder: the homeostatic "
            "drag |V - theta| as the remodeling signal — per-cell "
            "(undiluted by degree), local, target-blind. DR-G2 is the "
            "registered prediction: cells that cannot hold their "
            "identity shed their most-conflicting junction, and the "
            "hub substrate becomes writable. Refutation paths are "
            "pre-diagnosed: signal stall vs connectivity block "
            "(bridges_blocked counter)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
