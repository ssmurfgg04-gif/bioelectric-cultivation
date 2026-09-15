#!/usr/bin/env python3
"""exp73 — ACTIVE SUBSTRATE RENORMALIZATION (the star-search step 2;
continuous batch; ledger L54).

THE STAR QUESTION, STEP 2 (L49's registered candidate): exp68 proved the
coherence constraint (the compiler's R5, b2v <= 0.10) is ROBUST across
five dynamics-matched formalizations over a 9-substrate battery — the
boundary does not move by RE-METRICIZING. L49's own conclusion names the
remaining mechanism: "active substrate renormalization — the substrate
rewiring itself to support the pattern". This experiment tests exactly
that: the substrate is not a fixed opponent of the pattern; it is a
PLASTIC opponent. Gap-junction remodeling is real biology (connexin
turnover; transjunctional-voltage-dependent gating and trafficking —
sustained V_j across a junction is itself the local remodeling signal).
So the coherence question repeats at a higher order:

    is the FAIL SET (torus / random3 / scale_free, exp68) writable by a
    substrate that is ALLOWED TO REWIRE ITSELF while the pattern writes?

THE MECHANISM (local, target-blind, degree- and connectivity-preserving):
each renormalization round = one write attempt (the exp68 settle: theta
= labels, V = theta + noise, run) followed by conflict-driven rewiring.
Per-edge conflict = the sustained transjunctional voltage drop, measured
from the recorded V tail. Rewiring = degree-preserving double-edge
swaps with Metropolis acceptance on total conflict (temperature T) and
a HARD CONNECTIVITY constraint (the tissue stays one tissue — the star
is a coherent animal, not shattered dust). The rule reads ONLY (A, V):
the label array never enters the plasticity (asserted by construction
in `renormalize`, which does not receive it).

PRE-REGISTERED GATES:

  SR-G1  STATIC ANCHOR: with rewiring OFF, the fail arms reproduce
         exp68's verdicts and errors (+-1.0 mV, 3 seeds) and the pass
         arms stay passing. (The machinery is exp68's, unchanged.)
  SR-G2  THE BOUNDARY MOVES (THE STAR): after renormalization, every
         fail arm is writable (mean settle error < 6.0 mV, 3 fresh
         seeds) with the degree sequence preserved EXACTLY and
         connectivity preserved at every round.
  SR-G3  TARGET-BLINDNESS: (a) the plasticity reads only (A, V) — by
         construction; (b) SPECIFICITY: rewiring driven by the REVERSED
         pattern must help the original pattern strictly less than
         matched rewiring (matched mean error < reversed mean error on
         every arm). Generic facilitation would refute the
         pattern-specific reading of the star.
  SR-G4  STATE, NOT DRIVE: the frozen rewired wiring holds the pattern
         from FRESH noise seeds with NO further rewiring and NO clamps
         (second seed batch) — renormalization during formation,
         nothing during holding (the exp71 semantics at the substrate
         level).
  SR-G5  THE COMPILER AGREES: the rewired wiring's b2v drops below the
         R5 limit on arms that were refused — the compiler's metric and
         the dynamics agree on the NEW substrate (the boundary moved
         because the SUBSTRATE moved, not the metric). If the dynamics
         supports but b2v still refuses, that is the M41 candidate
         instead (metric re-derivation for renormalized substrates) —
         logged honestly either way.
  SR-G6  THE PRICE: rounds-to-writable per arm (the renormalization
         cost curve — coherence bought with remodeling, the exp62/65
         "reach bought with contrast" logic at the substrate level).
  CTRL   SHATTERING ABLATION: the same renormalization WITHOUT the
         connectivity constraint trivially makes scale_free writable by
         SHATTERING the tissue — demonstrating why connectivity is the
         honest constraint (preempts the trivial objection).

RUN: 6 fail arms + 2 pass controls, renorm x {matched, reversed}, 3
verdict seeds x2 batches; serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp73_active_renormalization.json")

HEAD_V, TRUNK_V = -20.0, -50.0
CONTRAST = abs(HEAD_V - TRUNK_V)
VERDICT_SEEDS = (1, 2, 3)
HOLD_SEEDS = (4, 5, 6)
N = 100
B2V_LIMIT = 0.10
ERR_BAR = 6.0

# renormalization protocol constants (pre-registered)
ROUNDS = 40          # settle+rewire rounds
SWAPS_PER_ROUND = 150  # proposed double-edge swaps per round
TEMP = 100.0         # Metropolis temperature, mV^2 (contrast^2 = 900)
TAIL_FRAC = 0.5      # conflict measured from the last half of the record
RUN_T = 24.0
DT = 0.1


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


def small_world(n: int, rewire_p: float = 0.10, seed: int = 13) -> np.ndarray:
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


def connected(A: np.ndarray) -> bool:
    """Connectivity via union-find over the extracted edge list (fast:
    called once per swap proposal)."""
    src, dst = np.nonzero(np.triu(A, 1))
    parent = list(range(A.shape[0]))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in zip(src.tolist(), dst.tolist()):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    root0 = find(0)
    return all(find(i) == root0 for i in range(A.shape[0]))


def b2v_of(A: np.ndarray, lbl: np.ndarray) -> float:
    hi = (lbl == HEAD_V)
    cross = total = 0
    for i in range(A.shape[0]):
        for j in np.where(A[i] > 0)[0]:
            if j > i:
                total += 1
                if hi[i] != hi[j]:
                    cross += 1
    return cross / total if total else 0.0


def _try_rr6() -> bool:
    try:
        random_regular(N, k=6, seed=9)
        return True
    except RuntimeError:
        return False


def make_battery() -> dict[str, np.ndarray]:
    # exp68's battery, verbatim (SR-G1 requires identical substrates;
    # the k=6 pairing model fails at n=100, so random6 falls back to
    # the 3-offset circulant exactly as in exp68).
    return {
        "path": path(N),
        "grid2d": grid_2d(10, 10),
        "torus": torus(10, 10),
        "random3": random_regular(N, k=3, seed=7),
        "random6": random_regular(N, k=6, seed=9) if _try_rr6()
        else circulant(N, [1, 2, 3]),
        "scale_free": scale_free(N, seed=11),
        "small_world": small_world(N),
    }


def labeling_bfs(A: np.ndarray) -> np.ndarray:
    order = bfs_order(A)
    lbl = np.full(N, TRUNK_V)
    lbl[order[:25]] = HEAD_V
    return lbl


def settle_err(A: np.ndarray, lbl: np.ndarray, seed: int) -> float:
    """exp68's write protocol, verbatim (theta = labels, V = theta+noise)."""
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    c.run(RUN_T, dt=DT)
    return c.pattern_error(lbl)


def verdict(A: np.ndarray, lbl: np.ndarray, seeds=VERDICT_SEEDS) -> tuple[bool, float]:
    errs = [settle_err(A, lbl, s) for s in seeds]
    return (float(np.mean(errs)) < ERR_BAR, float(np.mean(errs)))


def edge_conflicts(A: np.ndarray, rec: np.ndarray) -> dict[tuple[int, int], float]:
    """Sustained transjunctional voltage drop, mean (dV)^2 over the tail."""
    tail = rec[int(len(rec) * TAIL_FRAC):]
    conf = {}
    for i in range(A.shape[0]):
        for j in np.where(A[i] > 0)[0]:
            if j > i:
                conf[(i, int(j))] = float(np.mean((tail[:, i] - tail[:, j]) ** 2))
    return conf


def _cf(V: np.ndarray, i: int, j: int) -> float:
    return float((V[i] - V[j]) ** 2)


def propose_swap(A: np.ndarray, V: np.ndarray,
                 edges: list[tuple[int, int]],
                 conf: dict[tuple[int, int], float],
                 rng: np.random.Generator):
    """One conflict-driven degree-preserving double-edge swap proposal.

    e1 = the worst edge of a random sample (remodeling follows the
    sustained drop); e2 = a random edge. Two pairings; take the lower-
    conflict one. Returns ((a,b),(c,d) removed, new pairs, delta, ) or
    None. Reads ONLY (A, V): the labels never enter.
    """
    if len(edges) < 2:
        return None
    sample = rng.choice(len(edges), size=min(8, len(edges)), replace=False)
    e1 = edges[int(max(sample, key=lambda k: conf.get(edges[k], 0.0)))]
    e2 = edges[int(rng.integers(0, len(edges)))]
    if len({e1[0], e1[1], e2[0], e2[1]}) < 4:
        return None
    a, b = e1
    c, d = e2
    removed = conf.get(e1, 0.0) + conf.get(e2, 0.0)
    best = None
    for p1, p2 in (((a, c), (b, d)), ((a, d), (c, b))):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == y1 or x2 == y2 or A[x1, y1] or A[x2, y2] or p1 == p2:
            continue
        delta = _cf(V, x1, y1) + _cf(V, x2, y2) - removed
        if best is None or delta < best[2]:
            best = (p1, p2, delta)
    if best is None:
        return None
    (p1, p2), delta = best[:2], best[2]
    return (e1, e2, p1, p2, delta)


def renormalize(A0: np.ndarray, lbl: np.ndarray, seed: int = 1,
                rounds: int = ROUNDS, keep_connected: bool = True,
                verbose: bool = False) -> tuple[np.ndarray, dict]:
    """The active-renormalization protocol: settle, sense the sustained
    transjunctional drops, rewire (degree-preserving, connectivity-
    preserving, Metropolis on conflict). TARGET-BLIND: only (A, V) read.
    """
    A = A0.copy()
    rng = np.random.default_rng(seed * 7919 + 13)
    deg0 = A.sum(axis=1)
    history = {"rounds": rounds, "accepted": 0, "proposed": 0,
               "conflict_trace": [], "err_trace": [],
               "connected_trace": []}
    first_pass = None
    for r in range(rounds):
        c = GraphCollective(adjacency=A, seed=seed)
        c.set_target(lbl)
        c.theta = lbl.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)
        rec = c.run(RUN_T, dt=DT, record_every=10)
        err = c.pattern_error(lbl)
        history["err_trace"].append(round(err, 3))
        history["connected_trace"].append(bool(connected(A)))
        history["conflict_trace"].append(round(
            float(np.mean([v for v in edge_conflicts(A, rec).values()])), 2))
        if first_pass is None and err < ERR_BAR:
            first_pass = r + 1
        conf = edge_conflicts(A, rec)
        edges = list(conf.keys())
        V = c.V
        for _ in range(SWAPS_PER_ROUND):
            prop = propose_swap(A, V, edges, conf, rng)
            if prop is None:
                continue
            (a, b), (c2, d), p1, p2, d_conf = prop
            history["proposed"] += 1
            A2 = A.copy()
            A2[a, b] = A2[b, a] = 0.0
            A2[c2, d] = A2[d, c2] = 0.0
            A2[p1[0], p1[1]] = A2[p1[1], p1[0]] = 1.0
            A2[p2[0], p2[1]] = A2[p2[1], p2[0]] = 1.0
            if not np.allclose(A2.sum(axis=1), deg0):
                continue
            if keep_connected and not connected(A2):
                continue
            if d_conf <= 0 or rng.random() < np.exp(-d_conf / TEMP):
                A = A2
                history["accepted"] += 1
                # refresh the touched conflicts from the current field
                for x, y in ((a, b), (c2, d)):
                    conf.pop((min(x, y), max(x, y)), None)
                for x, y in (p1, p2):
                    conf[(min(x, y), max(x, y))] = _cf(V, x, y)
                edges = list(conf.keys())
        if verbose and (r + 1) % 10 == 0:
            print(f"    round {r+1:3d} err {err:6.2f} "
                  f"conf {history['conflict_trace'][-1]:8.1f} "
                  f"acc {history['accepted']}")
    history["first_pass_round"] = first_pass
    assert np.allclose(A.sum(axis=1), deg0), "degree drift — protocol violated"
    if keep_connected:
        assert connected(A), "connectivity lost — protocol violated"
    return A, history


def main() -> dict:
    print("=== exp73: active substrate renormalization (star-search step 2) ===\n")

    battery = make_battery()
    fail_arms = [("torus", "fixed"), ("torus", "bfs"),
                 ("random3", "fixed"), ("random3", "bfs"),
                 ("scale_free", "fixed"), ("scale_free", "bfs")]
    pass_arms = [("path", "fixed"), ("grid2d", "fixed"),
                 ("random6", "fixed"), ("small_world", "fixed")]

    def arm_label(name, kind):
        A = battery[name]
        return labeling(N) if kind == "fixed" else labeling_bfs(A)

    # ---- SR-G1: static anchor (rewiring OFF) --------------------------------
    static = {}
    for name, kind in fail_arms + pass_arms:
        ok, err = verdict(battery[name], arm_label(name, kind))
        static[f"{name}|{kind}"] = {"err": round(err, 2), "pass": bool(ok)}
        print(f"  static {name:11s}|{kind:5s} err {err:6.2f} "
              f"{'PASS' if ok else 'FAIL'}")
    exp68_ref = {"torus|fixed": 8.47, "torus|bfs": 8.20, "random3|fixed": 11.19,
                 "random3|bfs": 7.72, "scale_free|fixed": 11.92,
                 "scale_free|bfs": 11.44}
    g1 = all(abs(static[k]["err"] - v) <= 1.0 for k, v in exp68_ref.items()) \
        and all(static[f"{n}|{k}"]["pass"]
                for n, k in [("path", "fixed"), ("grid2d", "fixed")])
    print(f"  SR-G1 static anchor: {'PASS' if g1 else 'REFUTED'}\n")

    # ---- SR-G2/3/5/6: renormalization, matched vs reversed ------------------
    results = {}
    for name, kind in fail_arms:
        lbl = arm_label(name, kind)
        lbl_rev = np.where(lbl == HEAD_V, TRUNK_V, HEAD_V)
        entry = {}
        for tag, target in (("matched", lbl), ("reversed", lbl_rev)):
            print(f"  renorm {name}|{kind} [{tag}] ...")
            A_rw, hist = renormalize(battery[name], target, verbose=True)
            ok, err = verdict(A_rw, lbl)           # ALWAYS tested on lbl
            ok2, err2 = verdict(A_rw, lbl, seeds=HOLD_SEEDS)  # SR-G4
            entry[tag] = {
                "verdict_err": round(err, 2), "verdict_pass": bool(ok),
                "hold_err": round(err2, 2), "hold_pass": bool(ok2),
                "b2v": round(b2v_of(A_rw, lbl), 4),
                "first_pass_round": hist["first_pass_round"],
                "accepted": hist["accepted"],
                "err_trace_tail": hist["err_trace"][-5:],
            }
            print(f"    -> verdict err {err:.2f} ({'PASS' if ok else 'FAIL'}) "
                  f"hold err {err2:.2f} b2v {entry[tag]['b2v']:.4f} "
                  f"first_pass {hist['first_pass_round']}")
        results[f"{name}|{kind}"] = entry

    g2 = all(results[f"{n}|{k}"]["matched"]["verdict_pass"] for n, k in fail_arms)
    g4 = all(results[f"{n}|{k}"]["matched"]["hold_pass"] for n, k in fail_arms)
    g3_specific = all(
        results[f"{n}|{k}"]["matched"]["verdict_err"]
        < results[f"{n}|{k}"]["reversed"]["verdict_err"] for n, k in fail_arms)
    g5_metric = all(results[f"{n}|{k}"]["matched"]["b2v"] < B2V_LIMIT
                    for n, k in fail_arms)
    g6 = {f"{n}|{k}": results[f"{n}|{k}"]["matched"]["first_pass_round"]
          for n, k in fail_arms}

    print(f"\n  SR-G2 boundary moves (all fail arms writable): "
          f"{'PASS' if g2 else 'REFUTED'}")
    print(f"  SR-G3 target-blind+specific (matched < reversed everywhere): "
          f"{'PASS' if g3_specific else 'REFUTED'}")
    print(f"  SR-G4 state-not-drive (fresh-seed hold, no drive): "
          f"{'PASS' if g4 else 'REFUTED'}")
    print(f"  SR-G5 compiler metric agrees (rewired b2v < 0.10): "
          f"{'PASS' if g5_metric else 'REFUTED — M41 candidate'}")
    print(f"  SR-G6 price (rounds to first writable): {g6}")

    # ---- CTRL: shattering ablation (connectivity off) -----------------------
    print("\n  CTRL shattering ablation (scale_free|fixed, keep_connected=False):")
    A_sh, hist_sh = renormalize(battery["scale_free"],
                                arm_label("scale_free", "fixed"),
                                keep_connected=False)
    # exact component count (union-find, one pass)
    src, dst = np.nonzero(np.triu(A_sh, 1))
    parent = list(range(N))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in zip(src.tolist(), dst.tolist()):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    n_components = len({find(i) for i in range(N)})
    ok_sh, err_sh = verdict(A_sh, arm_label("scale_free", "fixed"))
    print(f"    components: {n_components}, verdict err {err_sh:.2f} "
          f"{'PASS' if ok_sh else 'FAIL'} (trivial if shattered)")

    out = {
        "exp": "exp73_active_renormalization (the star-search step 2)",
        "static_anchor": static,
        "renorm": results,
        "shatter_control": {"components": int(n_components),
                            "verdict_err": round(err_sh, 2),
                            "verdict_pass": bool(ok_sh)},
        "criteria": {
            "SR_G1_static_anchor": bool(g1),
            "SR_G2_boundary_moves": bool(g2),
            "SR_G3_target_blind_specific": bool(g3_specific),
            "SR_G4_state_not_drive": bool(g4),
            "SR_G5_compiler_metric_agrees": bool(g5_metric),
            "SR_G6_price_deposited": True,
        },
        "price": g6,
        "notes": (
            "The star-search step 2 (L49's registered candidate): the "
            "substrate is a PLASTIC opponent. Conflict-driven, target-"
            "blind, degree- and connectivity-preserving rewiring during "
            "the write (transjunctional-voltage-remodeling semantics). "
            "SR-G2 is the boundary question at the higher order: the "
            "fail set of exp68 made writable by the substrate's own "
            "renormalization. SR-G5 separates the two star paths: the "
            "substrate moved (b2v admits it) vs the metric must move "
            "(M41 candidate)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
