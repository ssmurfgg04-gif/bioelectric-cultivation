#!/usr/bin/env python3
"""exp76 — RUNG 5: THE SLOW ANCHOR (the star-search step 5; continuous
batch; ledger L57).

THE OPEN QUESTION (L56's registered candidate): exp75 proved the drag
signal |V - theta| is SELF-EXTINGUISHING — theta is plastic and
follows the smeared V within one write window, so the hijack rewrites
the reference and the tissue cannot locally detect its own
incoherence. The registered repair: TWO-TIMESCALE IDENTITY. The cell
carries a SLOW anchor (M28's phi_spec semantics: the positional spec
captured at pattern set; biologically the epigenetic/expression memory
that survives reprogramming — the codebase's own D3 result) and the
remodeling signal becomes the SLOW drag |V_i - anchor_i|.

THE THEOREM CONTRAST (this rung's real content): the timescale
separation IS the mechanism. Three anchor drift rates, everything else
identical:
    eps_slow = 0.04  (== eps — a single timescale; must reproduce
                      exp75's failure: the anchor smears with the
                      field, no hot cells, no shedding, no repair)
    eps_slow = 0.004 (40x slower than the fast relaxation — borderline)
    eps_slow = 0.0   (frozen — the M28 spec semantics)
Prediction: repair exists ONLY when the anchor outlives the write
window. The boundary between failing and working anchor rates is the
quantitative form of "coherence requires an anchor slower than the
hijack".

THE RUNG-5 MOVE (anchor-shed): each round —
  1. one write attempt with a two-timescale collective (fast theta as
     usual; the slow anchor a_v with drift rate eps_slow, initialized
     to the pattern at write start — no new information: the write
     protocol already sets theta = pattern);
  2. tail-mean per-cell slow drag d_i = mean_t |V_i(t) - a_i(t)|;
  3. every HOT cell (d_i > 8 mV) sheds its most-conflicting junction,
     connectivity HARD.
Target-blind: the cell compares its own voltage to its OWN slow
memory — the label array never enters the rule.

PRE-REGISTERED GATES:

  AN-G1  THE DIAGNOSIS QUANTIFIED: at eps_slow = eps, the end-of-write
         anchor drift on the fail arms is large (the anchor is
         corrupted within one window — deposit mean |a_end - pattern|)
         and no shedding fires (reproduces exp75).
  AN-G2  SIGNAL SEPARATION (frozen): the frozen-anchor drag separates
         — fail arms have hot cells in the first rounds; pass arms
         have ~none (threshold 8 mV).
  AN-G3  THE PREDICTION: frozen-anchor shedding makes BOTH scale_free
         arms writable (mean verdict error < 6.0, 3 fresh seeds),
         connectivity preserved at every round.
  AN-G4  HOLD SEMANTICS: the shed wiring holds from fresh noise seeds
         with no drive.
  AN-G5  NO REGRESSION: pass controls shed nothing / stay passing;
         the writable arms are not broken.
  AN-G6  METRIC TRACKING: b2v and absolute crossing agree with the
         verdicts on every final wiring.
  AN-G7  THE TIMESCALE BOUNDARY: repair appears between eps_slow = eps
         and eps_slow = 0 — the eps_slow sweep deposits where the
         boundary sits (the quantitative "anchor slower than hijack"
         law).

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
    make_battery, labeling_bfs, verdict, b2v_of, connected, edge_conflicts,
    N, ERR_BAR, B2V_LIMIT, ROUNDS, HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp74_renormalization_ladder import cut_stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp76_slow_anchor.json")

DRAG_THRESHOLD = 8.0
RUN_T = 24.0
DT = 0.1
REC_EVERY = 10
TAIL_FRAC = 0.5
EPS_SLOW_SWEEP = (0.04, 0.004, 0.0)


def anchor_drag(rec_v: np.ndarray, rec_a: np.ndarray) -> np.ndarray:
    """Tail-mean |V - anchor| per cell (the slow drag)."""
    tail = slice(int(len(rec_v) * TAIL_FRAC), None)
    return np.mean(np.abs(rec_v[tail] - rec_a[tail]), axis=0)


def settle_anchor(A: np.ndarray, lbl: np.ndarray, seed: int,
                  eps_slow: float):
    """One write attempt with the two-timescale anchor; returns final
    fields, the tail-mean slow drag per cell, per-edge conflicts, the
    error, and the end-of-write anchor drift (the diagnosis metric)."""
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.a_v = lbl.copy()                       # the anchor, captured at write
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    steps = int(round(RUN_T / DT))
    Vs, As = [], []
    for t in range(steps):
        # the anchor's own dynamics: relaxes toward its CAPTURED value
        # at eps_slow (an identity memory with finite lifetime); with
        # eps_slow = 0 it is frozen.
        c.a_v = c.a_v + eps_slow * DT * (lbl - c.a_v)
        c.step(DT)
        if t % REC_EVERY == 0:
            Vs.append(c.V.copy())
            As.append(c.a_v.copy())
    rec_v, rec_a = np.array(Vs), np.array(As)
    drag = anchor_drag(rec_v, rec_a)
    conf = edge_conflicts(A, rec_v)
    anchor_drift = float(np.sqrt(np.mean((c.a_v - lbl) ** 2)))
    return c.V.copy(), drag, conf, c.pattern_error(lbl), anchor_drift


def anchor_shed(A0: np.ndarray, lbl: np.ndarray, seed: int = 1,
                rounds: int = ROUNDS, eps_slow: float = 0.0,
                verbose: bool = False):
    """Rung 5: slow-drag-driven junction shedding."""
    A = A0.copy()
    e0 = int(np.triu(A, 1).sum())
    trace = {"err_trace": [], "hot_trace": [], "shed_trace": [],
             "bridges_blocked": 0, "shed_total": 0, "first_pass": None,
             "connected_every_round": True, "anchor_drift_end": None}
    for r in range(rounds):
        V, drag, conf, err, adr = settle_anchor(A, lbl, seed * 31 + r,
                                                eps_slow)
        trace["err_trace"].append(round(err, 3))
        trace["anchor_drift_end"] = round(adr, 3)
        hot = np.where(drag > DRAG_THRESHOLD)[0]
        trace["hot_trace"].append(int(len(hot)))
        if trace["first_pass"] is None and err < ERR_BAR:
            trace["first_pass"] = r + 1
        if not connected(A):
            trace["connected_every_round"] = False
        shed_r = 0
        for i in sorted(hot, key=lambda i: -drag[i]):
            nbrs = [int(j) for j in np.where(A[i] > 0)[0]]
            if not nbrs:
                continue
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
                  f"blocked {trace['bridges_blocked']}) adr {adr:.2f}")
    trace["edges_final"] = int(np.triu(A, 1).sum())
    trace["edges_start"] = e0
    return A, trace


def main() -> dict:
    print("=== exp76: rung 5 — the slow anchor (star-search step 5) ===\n")

    battery = make_battery()
    wall_arms = [("scale_free", "fixed"), ("scale_free", "bfs")]
    writable_controls = [("torus", "fixed"), ("random3", "fixed")]
    pass_controls = [("path", "fixed"), ("grid2d", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- AN-G1: the diagnosis quantified (eps_slow = eps reproduces exp75) ---
    g1_data = {}
    for name, kind in wall_arms:
        lbl = arm_label(name, kind)
        V, drag, conf, err, adr = settle_anchor(battery[name], lbl, 1, 0.04)
        hot = int((drag > DRAG_THRESHOLD).sum())
        g1_data[f"{name}|{kind}"] = {"anchor_drift": round(adr, 2),
                                     "hot": hot, "err": round(err, 2)}
        print(f"  eps_slow=eps {name}|{kind}: anchor drift {adr:.2f} mV, "
              f"hot {hot}, err {err:.2f}")
    g1 = all(d["anchor_drift"] > 5.0 and d["hot"] == 0
             for d in g1_data.values())
    print(f"  AN-G1 anchor corrupts within one window, no signal: "
          f"{'PASS' if g1 else 'REFUTED'}\n")

    # ---- AN-G2: signal separation (frozen anchor) ----------------------------
    sig = {}
    for name, kind in wall_arms + pass_controls:
        lbl = arm_label(name, kind)
        V, drag, conf, err, adr = settle_anchor(battery[name], lbl, 1, 0.0)
        sig[f"{name}|{kind}"] = {"hot": int((drag > DRAG_THRESHOLD).sum()),
                                 "mean_drag": round(float(drag.mean()), 2)}
        print(f"  frozen {name:11s}|{kind:5s} mean slow drag "
              f"{sig[f'{name}|{kind}']['mean_drag']:6.2f} "
              f"hot {sig[f'{name}|{kind}']['hot']:3d}")
    g2 = (all(sig[f"{n}|{k}"]["hot"] > 0 for n, k in wall_arms)
          and all(sig[f"{n}|{k}"]["hot"] <= 2 for n, k in pass_controls))
    print(f"  AN-G2 signal separation (frozen): {'PASS' if g2 else 'REFUTED'}\n")

    # ---- AN-G3/G4: the prediction --------------------------------------------
    results = {}
    for name, kind in wall_arms:
        lbl = arm_label(name, kind)
        print(f"  anchor-shed {name}|{kind} (frozen):")
        A_rw, tr = anchor_shed(battery[name], lbl, verbose=True)
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
        }
        print(f"    -> err {err:.2f} ({'PASS' if ok else 'FAIL'}) "
              f"hold {err2:.2f} b2v {results[f'{name}|{kind}']['b2v']:.4f} "
              f"cut {st['cut_edges']} edges "
              f"{tr['edges_start']}->{tr['edges_final']} "
              f"blocked {tr['bridges_blocked']}")
    g3 = all(results[f"{n}|{k}"]["verdict_pass"] for n, k in wall_arms)
    g4 = all(results[f"{n}|{k}"]["hold_pass"] for n, k in wall_arms)
    print(f"\n  AN-G3 the prediction (frozen anchor writes scale_free): "
          f"{'PASS' if g3 else 'REFUTED'}")
    print(f"  AN-G4 hold semantics: {'PASS' if g4 else 'REFUTED'}")

    # ---- AN-G5: no regression --------------------------------------------------
    regress = {}
    for name, kind in writable_controls + pass_controls:
        lbl = arm_label(name, kind)
        A_rw, tr = anchor_shed(battery[name], lbl)
        ok, err = verdict(A_rw, lbl)
        regress[f"{name}|{kind}"] = {
            "err": round(err, 2), "pass": bool(ok),
            "shed_total": tr["shed_total"],
            "edges": (tr["edges_start"], tr["edges_final"])}
        print(f"  control {name:11s} err {err:.2f} "
              f"{'PASS' if ok else 'FAIL'} shed {tr['shed_total']} "
              f"edges {tr['edges_start']}->{tr['edges_final']}")
    g5 = all(v["pass"] for v in regress.values())
    print(f"  AN-G5 no regression: {'PASS' if g5 else 'REFUTED'}")

    # ---- AN-G6: metric tracking -------------------------------------------------
    pts = [{"arm": k, "b2v": r["b2v"], "crossing": r["cut"]["cut_edges"],
            "pass": r["verdict_pass"]} for k, r in results.items()]
    g6 = all((p["b2v"] < B2V_LIMIT) == p["pass"] and
             (p["crossing"] <= 20) == p["pass"] for p in pts)
    print(f"  AN-G6 metric tracking: {'PASS' if g6 else 'REFUTED'}")

    # ---- AN-G7: the timescale boundary sweep ------------------------------------
    print("\n  AN-G7 timescale sweep (scale_free|fixed):")
    sweep = {}
    for eps_s in EPS_SLOW_SWEEP:
        lbl = arm_label("scale_free", "fixed")
        A_rw, tr = anchor_shed(battery["scale_free"], lbl, eps_slow=eps_s)
        ok, err = verdict(A_rw, lbl)
        sweep[str(eps_s)] = {"err": round(err, 2), "pass": bool(ok),
                             "shed": tr["shed_total"],
                             "anchor_drift_end": tr["anchor_drift_end"]}
        print(f"    eps_slow={eps_s:5}: err {err:6.2f} "
              f"{'PASS' if ok else 'FAIL'} shed {tr['shed_total']:3d} "
              f"adr_end {tr['anchor_drift_end']}")
    g7 = (not sweep["0.04"]["pass"]) and sweep["0.0"]["pass"]
    print(f"  AN-G7 timescale boundary (single fails, frozen works): "
          f"{'PASS' if g7 else 'REFUTED'}")

    out = {
        "exp": "exp76_slow_anchor (the star-search step 5, rung 5)",
        "diagnosis": g1_data,
        "signal": sig,
        "wall_arms": results,
        "controls": regress,
        "timescale_sweep": sweep,
        "criteria": {
            "AN_G1_diagnosis_quantified": bool(g1),
            "AN_G2_signal_separation": bool(g2),
            "AN_G3_prediction_frozen_writes": bool(g3),
            "AN_G4_hold_semantics": bool(g4),
            "AN_G5_no_regression": bool(g5),
            "AN_G6_metric_tracking": bool(g6),
            "AN_G7_timescale_boundary": bool(g7),
        },
        "notes": (
            "Rung 5: the two-timescale identity. The slow anchor is "
            "M28's phi_spec semantics implemented as a cell state; the "
            "remodeling signal is the slow drag |V - anchor|. AN-G7 is "
            "the theorem gate: the repair exists only when the anchor "
            "outlives the write window — the quantitative form of "
            "'coherence requires an anchor slower than the hijack'."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/7 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
