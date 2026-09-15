#!/usr/bin/env python3
"""exp68 — THE COHERENCE-FORMALIZATION SEARCH (the star-search step 1;
night nine continuous batch; ledger L49).

THE STAR QUESTION (the handoff's Section 13): is the exp43 coherence
constraint — the compiler's R5 refusal, b2v <= 0.10 — a FACT OF THE
DYNAMICS or an artifact of the metric's normalization? "When false
becomes true, the false is true": if a different, DYNAMICS-MATCHED
formalization predicts a substrate the b2v metric refuses and the SIM
SUPPORTS, the constraint's boundary moves — the 101% path is
formalization-dependent. If no such substrate exists across the
battery, the constraint is robust under formalization variation and
the honest report is "not yet formalization-dependent".

WHY b2v MAY BE THE WRONG NORMALIZATION: the dynamics' Laplacian is
UNNORMALIZED (lap = deg*v - G*v) — its pull at a boundary node scales
with DEGREE, not with the total-edge fraction. The dynamics-matched
quantity is the LABEL ENERGY E = sum over cut edges of (delta label)^2
= crossing * contrast^2 (the Laplacian quadratic form of the label
profile), or the per-node mean force; b2v divides crossing by TOTAL
edges (a density normalization the dynamics never applies).

BATTERY (n=100): path, ring, circulant-4 (ring + 2-step chords),
grid_2d(10,10), torus(10,10), random-3, random-6, scale-free,
small-world (ring + 10% rewired). TWO labelings: the fixed-index
(exp43's original anchors) and BFS-coherent communities (exp43's
amendment).

PRE-REGISTERED GATES:

  CF-G1  ANCHORS REPRODUCED: with the fixed-index labeling, the
         battery reproduces exp43's calibration (path PASS, grid PASS,
         random-3 FAIL, scale-free FAIL; errors on the same side of
         6.0 mV, 3 seeds).
  CF-G2  THE STAR QUESTION: across battery x labelings, exists a
         (substrate, labeling) where b2v REFUSES (b2v > 0.10) but the
         sim SUPPORTS (mean settle error < 6.0)? YES -> the boundary
         moves (M41 registered: the dynamics-matched metric replaces
         b2v in the compiler's R5); NO -> the constraint is robust
         (step-1 honest report).
  CF-G3  SEPARATOR TABLE: for each formalization (b2v, label energy
         E, mean per-node force, algebraic connectivity lambda2,
         conductance), the margin between the measured PASS and FAIL
         sets; the count of separating metrics deposited.

RUN: 10 substrates x 2 labelings x 3 seeds settle runs + metric
computation. Serial, BLAS pinned.
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

from cultivation.substrate.graph import (  # noqa: E402
    path, grid_2d, random_regular, scale_free, GraphCollective,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp68_coherence_search.json")

HEAD_V, TRUNK_V = -20.0, -50.0
CONTRAST = abs(HEAD_V - TRUNK_V)
SEEDS = (1, 2, 3)
N = 100
B2V_LIMIT = 0.10
ERR_BAR = 6.0


def circulant(n: int, offsets: list[int]) -> np.ndarray:
    A = np.zeros((n, n))
    for d in offsets:
        A += np.diag(np.ones(n - d), d) + np.diag(np.ones(n - d), -d)
    A[0, n - 1] = A[n - 1, 0] = 1.0
    return A


def torus(rows: int, cols: int) -> np.ndarray:
    A = np.zeros((rows * cols, rows * cols))
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            A[i, r * cols + (c + 1) % cols] = 1
            A[i, ((r + 1) % rows) * cols + c] = 1
    return np.maximum(A, A.T)


def small_world(n: int, rewire_p: float = 0.10,
                seed: int = 13) -> np.ndarray:
    A = circulant(n, [1]).copy()
    rng = np.random.default_rng(seed)
    edges = [(i, (i + 1) % n) for i in range(n)]
    for i, j in edges:
        if rng.random() < rewire_p:
            A[i, j] = A[j, i] = 0
            while True:
                k = int(rng.integers(0, n))
                if k != i and A[i, k] == 0:
                    A[i, k] = A[k, i] = 1
                    break
    return A


def bfs_order(A: np.ndarray, start: int = 0) -> list[int]:
    seen = {start}
    order = [start]
    q = [start]
    while q:
        i = q.pop(0)
        for j in np.where(A[i] > 0)[0]:
            if int(j) not in seen:
                seen.add(int(j))
                order.append(int(j))
                q.append(int(j))
    return order


def _try_rr6():
    try:
        random_regular(N, k=6, seed=9)
        return True
    except RuntimeError:
        return False


def make_battery() -> dict[str, np.ndarray]:
    return {
        "path": path(N),
        "ring": circulant(N, [1]),
        "circulant4": circulant(N, [1, 2]),
        "grid2d": grid_2d(10, 10),
        "torus": torus(10, 10),
        "random3": random_regular(N, k=3, seed=7),
        "random6": random_regular(N, k=6, seed=9) if _try_rr6() else circulant(N, [1, 2, 3]),
        "scale_free": scale_free(N, seed=11),
        "small_world": small_world(N),
    }


def metrics(A: np.ndarray, lbl: np.ndarray) -> dict:
    lab_hi = (lbl == HEAD_V).astype(int)
    crossing = 0
    total = 0
    for i in range(N):
        for j in np.where(A[i] > 0)[0]:
            if j > i:
                total += 1
                if lab_hi[i] != lab_hi[j]:
                    crossing += 1
    deg = A.sum(axis=1)
    L = np.diag(deg) - A
    lam2 = float(np.linalg.eigvalsh(L)[1]) if total else 0.0
    vol_hi = float(deg[lab_hi == 1].sum())
    vol_lo = float(deg[lab_hi == 0].sum())
    conductance = crossing / max(min(vol_hi, vol_lo), 1.0)
    return {
        "b2v": crossing / total if total else 0.0,
        "label_energy": crossing * CONTRAST ** 2,
        "mean_force": crossing * CONTRAST ** 2 / N,
        "lambda2": round(lam2, 4),
        "conductance": round(conductance, 4),
        "crossing": crossing,
    }


def sim_supports(A: np.ndarray, lbl: np.ndarray) -> tuple[bool, float]:
    errs = []
    for s in SEEDS:
        c = GraphCollective(adjacency=A, seed=s)
        c.set_target(lbl)
        c.theta = lbl.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)
        c.run(24, dt=0.1)
        errs.append(c.pattern_error(lbl))
    return (float(np.mean(errs)) < ERR_BAR, float(np.mean(errs)))


def main() -> dict:
    print("=== exp68: the coherence-formalization search ===\n")

    battery = make_battery()

    # ---- CF-G1: anchors reproduced (fixed-index labeling) -------------------
    anchors = {}
    for name in ("path", "grid2d", "random3", "scale_free"):
        A = battery[name]
        lbl = labeling(N)
        ok, mean_err = sim_supports(A, lbl)
        anchors[name] = {"mean_err": round(mean_err, 2), "pass": ok}
        print(f"  anchor {name:12s} err {mean_err:.2f} "
              f"{'PASS' if ok else 'FAIL'}")
    cf_g1 = bool(anchors["path"]["pass"] and anchors["grid2d"]["pass"]
                 and not anchors["random3"]["pass"]
                 and not anchors["scale_free"]["pass"])
    print(f"  CF-G1 anchors reproduced: {'PASS' if cf_g1 else 'REFUTED'}\n")

    # ---- the full battery: metrics + sim verdicts ---------------------------
    table = {}
    star_hits = []
    for name, A in battery.items():
        for lbl_kind in ("fixed", "bfs"):
            if lbl_kind == "fixed":
                lbl = labeling(N)
            else:
                order = bfs_order(A)
                lbl = np.full(N, TRUNK_V)
                lbl[order[:25]] = HEAD_V
            m = metrics(A, lbl)
            ok, mean_err = sim_supports(A, lbl)
            key = f"{name}|{lbl_kind}"
            table[key] = {**m, "sim_err": round(mean_err, 2),
                          "sim_pass": bool(ok)}
            refused_but_supported = (m["b2v"] > B2V_LIMIT and ok)
            if refused_but_supported:
                star_hits.append(key)
            print(f"  {key:24s} b2v={m['b2v']:.3f} E={m['label_energy']:.0f} "
                  f"lam2={m['lambda2']:.3f} cond={m['conductance']:.3f} "
                  f"err={mean_err:.2f} {'PASS' if ok else 'FAIL'}"
                  f"{'  <== STAR HIT' if refused_but_supported else ''}")

    cf_g2 = bool(star_hits)
    print(f"\n  CF-G2 star question (b2v refuses but sim supports): "
          f"{star_hits if star_hits else 'none'} -> "
          f"{'BOUNDARY MOVES (M41 registered)' if cf_g2 else 'CONSTRAINT ROBUST (step-1 honest report)'}")

    # ---- CF-G3: separator table ----------------------------------------------
    pass_set = [v for v in table.values() if v["sim_pass"]]
    fail_set = [v for v in table.values() if not v["sim_pass"]]
    separators = {}
    for metric in ("b2v", "label_energy", "mean_force", "lambda2",
                   "conductance"):
        if not pass_set or not fail_set:
            continue
        lo = min(v[metric] for v in pass_set)
        hi = max(v[metric] for v in fail_set)
        # a metric separates if some THRESHOLD splits the sets: the
        # sets must not overlap on the metric
        p_vals = sorted(v[metric] for v in pass_set)
        f_vals = sorted(v[metric] for v in fail_set)
        sep = (max(p_vals) < min(f_vals)) or (max(f_vals) < min(p_vals))
        direction = ("pass_low" if max(p_vals) < min(f_vals)
                     else "pass_high" if sep else "overlap")
        separators[metric] = {
            "pass_range": [round(min(p_vals), 3), round(max(p_vals), 3)],
            "fail_range": [round(min(f_vals), 3), round(max(f_vals), 3)],
            "separates": bool(sep), "direction": direction,
        }
        print(f"  {metric:14s} pass {separators[metric]['pass_range']} "
              f"fail {separators[metric]['fail_range']} "
              f"{'SEPARATES' if sep else 'overlaps'} ({direction})")
    n_sep = sum(1 for v in separators.values() if v["separates"])
    cf_g3 = bool(n_sep >= 1)
    print(f"  CF-G3 separator count {n_sep}: "
          f"{'PASS' if cf_g3 else 'REFUTED'}")

    out = {
        "exp": "exp68_coherence_search (the star-search step 1)",
        "anchors": anchors,
        "battery_table": table,
        "star_hits": star_hits,
        "separators": separators,
        "criteria": {
            "CF_G1_anchors_reproduced": bool(cf_g1),
            "CF_G2_boundary_moves": bool(cf_g2),
            "CF_G3_separator_table": bool(cf_g3),
        },
        "notes": (
            "The star-search step 1: the exp43 coherence constraint "
            "tested against the DYNAMICS-MATCHED formalizations (the "
            "unnormalized Laplacian's label energy and per-node force "
            "vs b2v's density normalization). CF-G2 is the boundary "
            "question: a substrate the b2v metric refuses but the "
            "dynamics supports MOVES the coherence boundary (the "
            "compiler's R5 would adopt the better metric as M41); "
            "none found -> the constraint is robust across the "
            "battery and the honest report is 'not yet "
            "formalization-dependent' — the naive floating-pattern "
            "star stays blocked by the dynamics, not by the metric."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/3 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
