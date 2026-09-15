#!/usr/bin/env python3
"""exp74 — THE RENORMALIZATION LADDER (the star-search step 3; continuous
batch; ledger L55).

THE OPEN QUESTION (L54's registered next step): exp73 moved the
coherence boundary for the homogeneous-degree substrates (torus,
random3) by conflict-driven REWIRING, but scale_free is immovable —
the residual wall is the DEGREE BUDGET (hubs straddle the boundary and
cannot shed edges under conservation). exp73 also proved the trivial
escape is closed (shattering fails; hubs keep their edges). The ladder
asks: WHERE IS THE LAST WALL?

THE RUNGS (each adds one remodeling move; all rules local and
target-blind — they read only the V field):
  rung 1  REWIRE (exp73: degree-preserving double-edge swaps,
          Metropolis on conflict, connectivity hard)
  rung 2  + PRUNE (conflict-thresholded junction dissolution — connexin
          down-regulation: edges with sustained transjunctional drop
          above (0.3 x contrast)^2 are removed; connectivity hard).
          Degree conservation RELAXED downward.
  rung 3  + GROW (Hebbian: "cells that agree, wire together" — new
          junctions between the most-agreeing non-adjacent pairs;
          growth budget capped at the initial edge count). Degree
          budget fully negotiable; connectivity trivially preserved.

Every rung is scored with the same instruments: verdict (3 fresh
seeds), hold (seeds 4-6, no drive), b2v, surviving cut structure
(bridges = the readout capacity), degree shed, rounds-to-writable.

PRE-REGISTERED GATES:

  RL-G1  RUNG-1 ANCHOR: rewiring alone reproduces exp73 (torus/random3
         writable, scale_free not).
  RL-G2  THE LADDER CLIMBS: scale_free becomes writable at SOME rung.
         The lowest sufficient rung is the residual wall's position:
         rung 2 -> pruning was the missing move; rung 3 -> new
         junctions were also needed; never -> the wall is deeper than
         the degree budget (log what survives).
  RL-G3  THE RESIDUAL CUT (readout capacity): after the ladder, the
         surviving cross-boundary edge count per arm is deposited
         together with the head-induced component count (a connected
         substrate needs at least one bridge per head component).
         THE TRADE-OFF IS REGISTERED: remodeling buys write-coherence
         at the price of readout bandwidth (bridges carry the pattern;
         exp72's "reach bought with contrast" at the substrate level).
  RL-G4  HOLD SEMANTICS: every arm writable at its rung holds from
         fresh noise seeds with no drive (formation-only remodeling).
  RL-G5  METRIC TRACKING: (a) if b2v < 0.10 wherever the dynamics
         passes — the fraction metric tracks through the ladder;
         (b) if not, the ABSOLUTE crossing count (the exp68 label
         energy form) must still separate pass/fail across all arms
         and rungs — else M41 (metric re-derivation) fires honestly.
  RL-G6  THE PRICE CURVE: junction budget spent per arm per rung
         (edges before/after, degree shed distribution) — the full
         "coherence bought with remodeling" curve.
  RL-G7  NO REGRESSION: the ladder never breaks a passing arm (applied
         to path|fixed and grid2d|fixed as controls; the remodeling is
         need-driven: pass arms only lose conflict edges and stay
         passing).

RUN: 6 fail arms x rungs-to-writable + 2 pass controls, 40 rounds max
per rung; serial, BLAS pinned.
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

from experiments.exp73_active_renormalization import (  # noqa: E402
    make_battery, labeling_bfs, settle_err, verdict, b2v_of, connected,
    edge_conflicts, _cf, propose_swap, renormalize,
    N, ERR_BAR, B2V_LIMIT, ROUNDS, SWAPS_PER_ROUND, TEMP,
    HEAD_V, TRUNK_V, CONTRAST,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp74_renormalization_ladder.json")

PRUNE_THRESHOLD = (0.3 * CONTRAST) ** 2   # 81 mV^2 sustained drop
PRUNE_PER_ROUND = 20                       # max dissolutions per round
GROW_PER_ROUND = 20                        # max new junctions per round
GROW_BUDGET_MULT = 1.0                     # may at most double the edges


def cut_stats(A: np.ndarray, lbl: np.ndarray) -> dict:
    hi = (lbl == HEAD_V)
    cut_edges = []
    for i in range(A.shape[0]):
        for j in np.where(A[i] > 0)[0]:
            if j > i and hi[i] != hi[j]:
                cut_edges.append((i, int(j)))
    # head-induced components (union-find on head subgraph)
    parent = list(range(N))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in np.where(hi)[0]:
        for j in np.where(A[i] > 0)[0]:
            if hi[j]:
                ri, rj = find(int(i)), find(int(j))
                if ri != rj:
                    parent[ri] = rj
    head_roots = {find(int(i)) for i in np.where(hi)[0]}
    return {"cut_edges": len(cut_edges), "head_components": len(head_roots)}


def climb(A0: np.ndarray, lbl: np.ndarray, max_rung: int = 3,
          seed: int = 1, verbose: bool = False) -> tuple[np.ndarray, dict]:
    """Climb the ladder rung by rung until writable (or rung exhausted).
    Each rung continues from the previous rung's wiring."""
    A = A0.copy()
    e0 = int(np.triu(A0, 1).sum())
    deg0 = A.sum(axis=1)
    grown_total = 0
    grow_budget = int(GROW_BUDGET_MULT * e0)
    rng = np.random.default_rng(seed * 104729 + 7)
    trace = {"rungs": [], "final_rung": None, "writable": False,
             "edges_start": e0}
    for rung in range(1, max_rung + 1):
        ok, err = verdict(A, lbl)
        if ok and rung > 1:
            trace["final_rung"] = rung - 1
            trace["writable"] = True
            break
        if ok and rung == 1:
            trace["final_rung"] = 0   # writable without remodeling
            trace["writable"] = True
            break
        if verbose:
            print(f"    rung {rung} start (err {err:.2f}) ...")
        rung_trace = {"rung": rung, "err_trace": [], "accepted": 0,
                      "pruned": 0, "grown": 0}
        first_pass = None
        for r in range(ROUNDS):
            c_seed = seed * 31 + rung * 101 + r
            c = GraphCollectiveSeed(A, c_seed)
            c.set_target(lbl)
            c.theta = lbl.copy()
            c.V = c.theta + c.rng.normal(0.0, 2.0, N)
            rec = c.run(24.0, dt=0.1, record_every=10)
            err = c.pattern_error(lbl)
            rung_trace["err_trace"].append(round(err, 3))
            if first_pass is None and err < ERR_BAR:
                first_pass = r + 1
            conf = edge_conflicts(A, rec)
            edges = list(conf.keys())
            V = c.V
            # --- move 1: rewire (rungs >= 1) ---
            for _ in range(SWAPS_PER_ROUND):
                prop = propose_swap(A, V, edges, conf, rng)
                if prop is None:
                    continue
                (a, b), (c2, d), p1, p2, d_conf = prop
                A2 = A.copy()
                A2[a, b] = A2[b, a] = 0.0
                A2[c2, d] = A2[d, c2] = 0.0
                A2[p1[0], p1[1]] = A2[p1[1], p1[0]] = 1.0
                A2[p2[0], p2[1]] = A2[p2[1], p2[0]] = 1.0
                if not connected(A2):
                    continue
                if d_conf <= 0 or rng.random() < np.exp(-d_conf / TEMP):
                    A = A2
                    rung_trace["accepted"] += 1
                    for x, y in ((a, b), (c2, d)):
                        conf.pop((min(x, y), max(x, y)), None)
                    for x, y in (p1, p2):
                        conf[(min(x, y), max(x, y))] = _cf(V, x, y)
                    edges = list(conf.keys())
            # --- move 2: prune (rungs >= 2) ---
            if rung >= 2:
                hot = sorted((e for e in edges
                              if conf[e] > PRUNE_THRESHOLD),
                             key=lambda e: -conf[e])
                for (a, b) in hot[:PRUNE_PER_ROUND]:
                    A2 = A.copy()
                    A2[a, b] = A2[b, a] = 0.0
                    if connected(A2):
                        A = A2
                        conf.pop((a, b), None)
                        rung_trace["pruned"] += 1
                edges = list(conf.keys())
            # --- move 3: grow (rungs >= 3) ---
            if rung >= 3 and grown_total < grow_budget:
                for _ in range(GROW_PER_ROUND):
                    if grown_total >= grow_budget:
                        break
                    i = int(rng.integers(0, N))
                    js = [int(j) for j in np.where(A[i] == 0)[0] if j != i]
                    if not js:
                        continue
                    sample = rng.choice(len(js), size=min(6, len(js)),
                                        replace=False)
                    j = js[int(min(sample, key=lambda k: _cf(V, i, js[k])))]
                    if _cf(V, i, j) > PRUNE_THRESHOLD:
                        continue        # never wire across a fight
                    A[i, j] = A[j, i] = 1.0
                    conf[(min(i, j), max(i, j))] = _cf(V, i, j)
                    edges = list(conf.keys())
                    grown_total += 1
                    rung_trace["grown"] += 1
            if verbose and (r + 1) % 10 == 0:
                print(f"      round {r+1:3d} err {err:7.2f} "
                      f"rew {rung_trace['accepted']} "
                      f"pr {rung_trace['pruned']} "
                      f"gr {rung_trace['grown']}")
        rung_trace["first_pass"] = first_pass
        ok, err = verdict(A, lbl)
        rung_trace["rung_verdict"] = {"err": round(err, 2), "pass": bool(ok)}
        trace["rungs"].append(rung_trace)
        trace["final_rung"] = rung
        trace["writable"] = bool(ok)
        if ok:
            break
    trace["edges_final"] = int(np.triu(A, 1).sum())
    trace["grown_total"] = grown_total
    return A, trace


def GraphCollectiveSeed(A, s):
    from cultivation.substrate.graph import GraphCollective
    return GraphCollective(adjacency=A, seed=s)


def main() -> dict:
    print("=== exp74: the renormalization ladder (star-search step 3) ===\n")

    battery = make_battery()
    fail_arms = [("torus", "fixed"), ("torus", "bfs"),
                 ("random3", "fixed"), ("random3", "bfs"),
                 ("scale_free", "fixed"), ("scale_free", "bfs")]
    controls = [("path", "fixed"), ("grid2d", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- RL-G1: rung-1 anchor (rewire only) ---------------------------------
    g1_checks = {}
    for name, kind in [("torus", "fixed"), ("random3", "fixed"),
                       ("scale_free", "fixed")]:
        lbl = arm_label(name, kind)
        A1, _ = renormalize(battery[name], lbl, rounds=ROUNDS)
        ok, err = verdict(A1, lbl)
        g1_checks[f"{name}|{kind}"] = {"err": round(err, 2), "pass": bool(ok)}
        print(f"  rung1 anchor {name:11s} err {err:6.2f} "
              f"{'PASS' if ok else 'FAIL'}")
    g1 = (g1_checks["torus|fixed"]["pass"] and g1_checks["random3|fixed"]["pass"]
          and not g1_checks["scale_free|fixed"]["pass"])
    print(f"  RL-G1 rung-1 anchor: {'PASS' if g1 else 'REFUTED'}\n")

    # ---- RL-G2..G6: the climb ------------------------------------------------
    results = {}
    for name, kind in fail_arms:
        lbl = arm_label(name, kind)
        print(f"  climb {name}|{kind}:")
        A_rw, tr = climb(battery[name], lbl, verbose=True)
        ok, err = verdict(A_rw, lbl)
        ok2, err2 = verdict(A_rw, lbl, seeds=(4, 5, 6))
        st = cut_stats(A_rw, lbl)
        results[f"{name}|{kind}"] = {
            "final_rung": tr["final_rung"], "writable": bool(ok),
            "verdict_err": round(err, 2), "hold_err": round(err2, 2),
            "hold_pass": bool(ok2),
            "b2v": round(b2v_of(A_rw, lbl), 4), "cut": st,
            "edges_start": tr["edges_start"], "edges_final": tr["edges_final"],
            "rung_verdicts": [r.get("rung_verdict") for r in tr["rungs"]],
        }
        print(f"    -> rung {tr['final_rung']} err {err:.2f} "
              f"({'PASS' if ok else 'FAIL'}) hold {err2:.2f} "
              f"b2v {results[f'{name}|{kind}']['b2v']:.4f} "
              f"cut {st['cut_edges']} (head comps {st['head_components']}) "
              f"edges {tr['edges_start']}->{tr['edges_final']}")

    g2 = all(results[f"{n}|{k}"]["writable"] for n, k in fail_arms)
    g4 = all(results[f"{n}|{k}"]["hold_pass"] for n, k in fail_arms)
    moved = [k for k in results if results[k]["writable"]]
    g5a = all(results[k]["b2v"] < B2V_LIMIT for k in moved)
    print(f"\n  RL-G2 the ladder climbs (scale_free writable): "
          f"{'PASS' if g2 else 'REFUTED'}")
    print(f"  RL-G4 hold semantics: {'PASS' if g4 else 'REFUTED'}")
    print(f"  RL-G5a fraction metric tracks on moved arms: "
          f"{'PASS' if g5a else 'FAIL -> check absolute form'}")

    # ---- RL-G7: no regression on pass arms ----------------------------------
    regress = {}
    for name, kind in controls:
        lbl = arm_label(name, kind)
        A_rw, tr = climb(battery[name], lbl)
        ok, err = verdict(A_rw, lbl)
        regress[f"{name}|{kind}"] = {"err": round(err, 2), "pass": bool(ok),
                                     "edges": (tr["edges_start"],
                                               tr["edges_final"])}
        print(f"  control {name:8s} err {err:.2f} "
              f"{'PASS' if ok else 'FAIL'} "
              f"edges {tr['edges_start']}->{tr['edges_final']}")
    g7 = all(v["pass"] for v in regress.values())
    print(f"  RL-G7 no regression: {'PASS' if g7 else 'REFUTED'}")

    # ---- RL-G5b: absolute-crossing separator across all rungs ---------------
    # collected from every arm's final wiring + verdict
    all_points = []
    for name, kind in fail_arms:
        lbl = arm_label(name, kind)
        r = results[f"{name}|{kind}"]
        all_points.append({"arm": f"{name}|{kind}",
                           "crossing": r["cut"]["cut_edges"],
                           "b2v": r["b2v"], "pass": r["writable"]})
    pass_c = sorted(p["crossing"] for p in all_points if p["pass"])
    fail_c = sorted(p["crossing"] for p in not_pass(all_points))
    sep_abs = bool(pass_c and fail_c and max(pass_c) < min(fail_c)) \
        if fail_c else bool(pass_c)
    print(f"  RL-G5b absolute crossing: pass {pass_c} fail {fail_c} "
          f"{'SEPARATES' if sep_abs else 'overlaps'}")

    out = {
        "exp": "exp74_renormalization_ladder (the star-search step 3)",
        "rung1_anchor": g1_checks,
        "climb": results,
        "controls": regress,
        "criteria": {
            "RL_G1_rung1_anchor": bool(g1),
            "RL_G2_ladder_climbs": bool(g2),
            "RL_G4_hold_semantics": bool(g4),
            "RL_G5a_fraction_tracks": bool(g5a),
            "RL_G5b_absolute_separates": bool(sep_abs),
            "RL_G7_no_regression": bool(g7),
        },
        "notes": (
            "The star-search step 3: the ladder relaxes the degree "
            "budget rung by rung (rewire -> +prune -> +grow). RL-G2's "
            "lowest sufficient rung is the last wall's position; RL-G3 "
            "deposits the residual cut as the readout capacity (the "
            "write-coherence vs readout-bandwidth trade-off; the "
            "substrate-level instance of the 'everything is bought' "
            "law)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


def not_pass(points):
    return [p for p in points if not p["pass"]]


if __name__ == "__main__":
    main()
