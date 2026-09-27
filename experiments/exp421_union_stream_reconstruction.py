#!/usr/bin/env python3
"""exp421 — THE UNION-BLEND STREAM'S WIRING RECONSTRUCTION: THE
SHARPENING LEVER (batch HU-11; ledger L310's named lever — exp414's
boundary-blend stream reached AUC 0.63-0.68 because the blend faces
cover only the walked cells' coupling; the UNION form blends at EVERY
walked cell, putting every cell's commit under the register's pull and
widening the co-movement coverage). HYPOTHESIS: the union stream's
fingerprint clears the 0.85 bar on >= 2/3 graphs.

THE INSTRUMENT (exp414's machinery verbatim except the blend form):
three graphs, 10 rounds under the stress pin, the commit trajectories'
cross-correlation, edges := top-k by |S|; the UNION stream = the blend
at all walked cells (g_ctx 0.5); the BOUNDARY stream re-run as the
paired control (exp414's form); the shuffled null + the decoy as
exp414's.
PRE-REGISTERED GATES:
  G1  floor discipline; the constants; the graph identities logged.
  G2  the union stream's AUC >= 0.85 on >= 2/3 graphs.
  G3  the union-over-boundary improvement >= 0.05 AUC on >= 2/3 graphs
      (the lever's measured effect, both streams deposited).
  G4  the null <= 0.60 and the decoy gap >= 0.2 on every graph where
      G2 fired.
  G5  deposit results/exp421_union_stream_reconstruction.json.
BRANCH: WIRING-RECOVERABLE (G2 PASS) / SHARPENED-PARTIAL (G3 PASS, G2
REFUTE) / LEVER-NULL (G3 REFUTE) / INSTRUMENT-REFUTED.
THE HONEST STAKES: substrate-independence's concrete test gets its
sharpest honest shot — the structure in the trace, measured under the
blend form the carrier itself uses.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# body-side import completion (the stub header carried os/sys only) —
# disclosed; the frozen constants below are byte-unchanged
import hashlib
import time
from collections import deque

import numpy as np

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective

G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
GRAPHS = ["path100", "planarian400", "human400"]
ROUNDS = 10
DEPOSIT = os.path.join(ROOT, "results",
                       "exp421_union_stream_reconstruction.json")


BODY_DISCLOSURES = [
    "the union/boundary distinction implemented as the COVERAGE reading of "
    "the pre-registered blend-form sentence: the union stream walks the "
    "WHOLE graph every round (every cell's commit under the register's "
    "pull; the reconstruction covers all n cells; k = the FULL edge "
    "count) while the boundary control is exp414's single wound-region "
    "form re-run verbatim on same-seed fresh builds; the blend-scope "
    "reading (blend at wound-facing cells only) named and rejected — "
    "L310's named blur mechanism is coverage, and exp414's landed form "
    "already blended at every walked cell in its region",
    "the build-time wound stays the exp414 form (the walk region is the "
    "whole graph while the wound is the exp414 region — the exp413 "
    "rest-context disclosure precedent: the stress-routed parent "
    "inheritance is what the reconstruction reads)",
    "the union walk's BFS: when the region is the whole graph no cell has "
    "an outside parent, so the walk seeds at the first region cell (the "
    "exp307 walk-order legality) and re-seeds a fresh BFS tree at any "
    "unvisited cell (a forest order is still a valid walk order); the "
    "re-seed never fires on exp414's connected regions",
    "G4's evaluation convention: on every graph whose best union AUC "
    ">= 0.85, all of that graph's shuffled-null AUCs must be <= 0.60 and "
    "its best row's (auc - auc_decoy) >= 0.2 (exp414's row-level "
    "convention); no fired graph -> vacuous PASS (exp414's convention)",
    "the boundary arm is also the instrument cross-check: same seeds as "
    "exp414, its per-graph bests are deposited beside exp414's landed "
    "numbers (non-gating field exp414_cross_check)",
]


def _build(graph, seed):
    """exp414's build verbatim."""
    from experiments.exp73_active_renormalization import small_world
    from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                                   spec_target_n)
    if graph == "path100":
        from cultivation.substrate.graph import path
        A = path(100)
        n = 100
        tgt = np.empty(n)
        tgt[:40] = -50.0
        tgt[40:70] = -30.0
        tgt[70:] = -20.0
        region = list(range(20, 60))
    elif graph == "planarian400":
        A = small_world(400, rewire_p=0.05, seed=13)
        n = 400
        canon = labeling_bfs_n(np.abs(A))
        tgt = spec_target_n(MULTI, canon, n)
        region = list(range(0, 100))
    else:
        from human.substrate import (build_human_adjacency, human_target,
                                     load_human_fc)
        A = build_human_adjacency(load_human_fc())
        n = 400
        tgt, zones = human_target(A)
        region = list(np.where(zones == 0)[0])
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    if graph != "human400":
        c.amputate(slice(region[0], region[-1] + 1))
    else:
        c.theta[region] = -30.0
        c.V[region] = -30.0
    return c, tgt, region, n


def _walk_round(c, region, stress):
    """exp414's round verbatim (the blend at every walked cell, g_ctx
    0.5) + the forest re-seed for whole-graph regions."""
    region_set = set(region)
    parent_of, frontier = {}, []
    wound_center = float(np.mean(c.theta[region]))
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = [int(region[0])]
        parent_of[frontier[0]] = frontier[0]
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(np.abs(c.A[i]) > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    for i in region:
        if int(i) not in visited:
            visited.add(int(i))
            parent_of[int(i)] = int(i)
            order.append((int(i), int(i)))
            q2 = deque([int(i)])
            while q2:
                u = q2.popleft()
                for j in np.where(np.abs(c.A[u]) > 0)[0]:
                    if int(j) in region_set and int(j) not in visited:
                        visited.add(int(j))
                        parent_of[int(j)] = int(u)
                        order.append((int(j), int(u)))
                        q2.append(int(j))
    commits = {}
    if stress:
        CORE.NEURAL_SPEC_MIN = -35.0
    try:
        for i, src in order:
            for _ in range(STEPS_PER_CELL):
                c.step(0.1)
            if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                theta_new = (c.phi_spec[i]
                             + c.rng.normal(0.0, COMMIT_NOISE))
            else:
                theta_new = (c.theta[src]
                             + c.rng.normal(0.0, COMMIT_NOISE))
            written = theta_new
            if G_CTX > 0.0:
                written = ((1.0 - G_CTX) * theta_new
                           + G_CTX * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
            commits[i] = written
    finally:
        if stress:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    c.run(30.0, dt=0.1)
    return commits


def _auc(S, edges_mask):
    """Rank AUC of |S| against a boolean edge mask (exp414's verbatim)."""
    iu = np.triu_indices_from(S, 1)
    scores = np.abs(S[iu])
    labels = edges_mask[iu].astype(int)
    order = np.argsort(scores)
    ranks = np.empty(len(scores))
    ranks[order] = np.arange(1, len(scores) + 1)
    s_sorted = scores[order]
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        ranks[order[i:j + 1]] = np.arange(i, j + 1) + 1.0
        i = j + 1
    n_pos = labels.sum()
    n_neg = len(labels) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    return float((ranks[labels == 1].sum()
                  - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def _score_arm(c, rounds, seed):
    """The stream's reconstruction + null + decoy (exp414's machinery,
    scoped to the arm's walked cells)."""
    from experiments.exp413_indexation_identity import \
        _degree_preserving_rewire
    cells = sorted({int(i) for rd in rounds for i in rd})
    idx = {cell: k for k, cell in enumerate(cells)}
    X = np.full((len(rounds), len(cells)), np.nan)
    for r, rd in enumerate(rounds):
        for i, v in rd.items():
            X[r, idx[i]] = v
    assert np.isfinite(X).all()
    S = np.nan_to_num(np.corrcoef(X.T), nan=0.0)
    nc = len(cells)
    A_true = (np.abs(c.A) > 0)
    np.fill_diagonal(A_true, False)
    edges_mask = np.zeros((nc, nc), dtype=bool)
    edges_mask[:] = A_true[np.ix_(cells, cells)]
    iu = np.triu_indices(nc, 1)
    k_true = int(edges_mask[iu].sum())
    auc = _auc(S, edges_mask)
    sc = np.abs(S[iu])
    top = np.argsort(sc)[::-1][:k_true]
    prec = float(edges_mask[iu][top].mean()) if k_true else float("nan")
    Xn = X.copy()
    rng = np.random.default_rng(500 + seed)
    for j in range(Xn.shape[1]):
        rng.shuffle(Xn[:, j])
    Sn = np.nan_to_num(np.corrcoef(Xn.T), nan=0.0)
    auc_null = _auc(Sn, edges_mask)
    A_bin = (np.abs(c.A) > 0).astype(float)
    A_dec, _ = _degree_preserving_rewire(A_bin, 1.0, seed)
    dec_full = (np.abs(A_dec) > 0)
    np.fill_diagonal(dec_full, False)
    dec_mask = dec_full[np.ix_(cells, cells)]
    auc_decoy = _auc(S, dec_mask)
    return {"auc": auc, "precision_at_k": prec, "auc_null": auc_null,
            "auc_decoy": auc_decoy, "k_true": k_true,
            "n_cells_walked": nc}


def _run_arm(graph, seed, arm):
    c, tgt, region, n = _build(graph, seed)
    region_full = (list(range(n)) if arm == "union"
                   else [int(x) for x in region])
    rounds = [_walk_round(c, region_full, True) for _ in range(ROUNDS)]
    return _score_arm(c, rounds, seed)


def _sha(A):
    return hashlib.sha256(np.ascontiguousarray(A).tobytes()).hexdigest()[:16]


def main(budget_mode: str = "full", arm: str = None,
         assemble: bool = False) -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    graphs = GRAPHS[:1] if smoke else GRAPHS
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and G_CTX == 0.5
    assert ROUNDS == 10
    print("G1 floor %s; constants verified" % CORE.NEURAL_SPEC_MIN)

    if assemble:
        return _assemble()

    if arm is not None:
        # the arm-split contingency: one arm only, partial deposit, no
        # gates (the assembler evaluates the gates exactly once)
        assert arm in ("union", "boundary")
        rows = {"%s|%s|%d" % (arm, g, s):
                _run_arm(g, s, arm)
                for g in (GRAPHS[:1] if smoke else GRAPHS)
                for s in (SEEDS[:1] if smoke else SEEDS)}
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
        dep = {"experiment": "exp421", "arm_partial": arm,
               "results": rows, "disclosures": BODY_DISCLOSURES}
        path = DEPOSIT.replace(".json", "_partial_%s.json" % arm)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path + ".tmp", "w") as f:
            json.dump(dep, f, indent=1, sort_keys=True)
        os.replace(path + ".tmp", path)
        print("EXP421 PARTIAL (%s) written: %s" % (arm, path))
        return {"gates": {}}

    identities = {}
    results = {}
    for graph in graphs:
        for seed in seeds:
            for a in ("union", "boundary"):
                t0 = time.time()
                row = _run_arm(graph, seed, a)
                row["wall_s"] = round(time.time() - t0, 1)
                results["%s|%s|%d" % (a, graph, seed)] = row
                print("  %s %s seed %d: AUC %.3f p@k %.3f null %.3f "
                      "decoy %.3f (k=%d, %.1fs)"
                      % (a, graph, seed, row["auc"], row["precision_at_k"],
                         row["auc_null"], row["auc_decoy"], row["k_true"],
                         row["wall_s"]))
        c, _, _, _ = _build(graph, seeds[0])
        identities[graph] = _sha(np.abs(c.A))
        del c
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor entry/exit; the constants; identities %s)"
          % identities)

    union_best, bound_best = {}, {}
    for g in graphs:
        ua = [results["union|%s|%d" % (g, s)]["auc"] for s in seeds
              if "union|%s|%d" % (g, s) in results]
        ba = [results["boundary|%s|%d" % (g, s)]["auc"] for s in seeds
              if "boundary|%s|%d" % (g, s) in results]
        union_best[g] = max(ua) if ua else float("nan")
        bound_best[g] = max(ba) if ba else float("nan")

    g2_graphs = [g for g in graphs if union_best[g] >= 0.85]
    verdicts["G2"] = ("PASS" if (smoke or len(g2_graphs) >= 2)
                      else "REFUTE")
    print("G2 %s (union per-graph best %s)"
          % (verdicts["G2"], union_best))

    improved = [g for g in graphs
                if union_best[g] - bound_best[g] >= 0.05]
    verdicts["G3"] = ("PASS" if (smoke or len(improved) >= 2)
                      else "REFUTE")
    print("G3 %s (union-over-boundary %s; improved on %s)"
          % (verdicts["G3"],
             {g: round(union_best[g] - bound_best[g], 3) for g in graphs},
             improved))

    g4_details, g4_ok = {}, True
    for g in g2_graphs:
        rows = [results["union|%s|%d" % (g, s)] for s in seeds
                if "union|%s|%d" % (g, s) in results]
        nulls_ok = all(r["auc_null"] <= 0.60 for r in rows)
        best_row = max(rows, key=lambda r: r["auc"])
        gap = best_row["auc"] - best_row["auc_decoy"]
        g4_details[g] = {"nulls_ok": nulls_ok, "decoy_gap": round(gap, 3)}
        g4_ok = g4_ok and nulls_ok and gap >= 0.2
    verdicts["G4"] = ("PASS" if (smoke or not g2_graphs or g4_ok)
                      else "REFUTE")
    print("G4 %s (%s)" % (verdicts["G4"], g4_details))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    exp414_cross = None
    try:
        with open(os.path.join(ROOT, "results",
                               "exp414_wiring_from_history.json")) as f:
            exp414_cross = json.load(f).get("per_graph_best_auc")
    except OSError:
        pass
    branch = ("WIRING-RECOVERABLE" if verdicts["G2"] == "PASS" else
              "SHARPENED-PARTIAL" if verdicts["G3"] == "PASS" else
              "LEVER-NULL")
    dep = {
        "experiment": "exp421",
        "title": "THE UNION-BLEND STREAM'S WIRING RECONSTRUCTION: THE "
                 "SHARPENING LEVER (batch HU-11)",
        "instrument": {
            "arms": ["union (whole-graph walk coverage)",
                     "boundary (exp414's wound-region form, paired "
                     "control)"],
            "rounds": ROUNDS,
            "stress": "the write-time -35.0 pin each round",
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "SEEDS": SEEDS}},
        "graph_identities": identities,
        "results": results,
        "per_graph_best": {"union": union_best, "boundary": bound_best},
        "exp414_cross_check": exp414_cross,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP421 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


def _assemble() -> dict:
    """Post-salvage gate evaluation from the two arm partials (the
    arm-split contingency; gates evaluated exactly once here)."""
    parts = {}
    for a in ("union", "boundary"):
        p = DEPOSIT.replace(".json", "_partial_%s.json" % a)
        with open(p) as f:
            parts[a] = json.load(f)["results"]
    results = dict(parts["union"])
    results.update(parts["boundary"])
    graphs = sorted({k.split("|")[1] for k in results})
    seeds = sorted({int(k.split("|")[2]) for k in results})
    union_best, bound_best = {}, {}
    for g in graphs:
        ua = [results["union|%s|%d" % (g, s)]["auc"] for s in seeds
              if "union|%s|%d" % (g, s) in results]
        ba = [results["boundary|%s|%d" % (g, s)]["auc"] for s in seeds
              if "boundary|%s|%d" % (g, s) in results]
        union_best[g] = max(ua) if ua else float("nan")
        bound_best[g] = max(ba) if ba else float("nan")
    g2_graphs = [g for g in graphs if union_best[g] >= 0.85]
    verdicts = {
        "G2": "PASS" if len(g2_graphs) >= 2 else "REFUTE",
        "G3": "PASS" if sum(1 for g in graphs
                            if union_best[g] - bound_best[g] >= 0.05) >= 2
        else "REFUTE",
    }
    g4_ok = True
    for g in g2_graphs:
        rows = [results["union|%s|%d" % (g, s)] for s in seeds
                if "union|%s|%d" % (g, s) in results]
        best_row = max(rows, key=lambda r: r["auc"])
        g4_ok = (g4_ok
                 and all(r["auc_null"] <= 0.60 for r in rows)
                 and best_row["auc"] - best_row["auc_decoy"] >= 0.2)
    verdicts["G4"] = "PASS" if (not g2_graphs or g4_ok) else "REFUTE"
    branch = ("WIRING-RECOVERABLE" if verdicts["G2"] == "PASS" else
              "SHARPENED-PARTIAL" if verdicts["G3"] == "PASS" else
              "LEVER-NULL")
    dep = {"experiment": "exp421", "assembled_from":
           ["exp421_partial_union.json", "exp421_partial_boundary.json"],
           "results": results,
           "per_graph_best": {"union": union_best,
                              "boundary": bound_best},
           "disclosures": BODY_DISCLOSURES, "gates": verdicts,
           "verdict": branch}
    with open(DEPOSIT + ".tmp", "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(DEPOSIT + ".tmp", DEPOSIT)
    print("EXP421 ASSEMBLED VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    _smoke = "--smoke" in _argv
    _arm = None
    if "--arm" in _argv:
        _arm = _argv[_argv.index("--arm") + 1]
    if "--assemble" in _argv:
        main(assemble=True)
    elif _smoke:
        main(budget_mode="smoke")
    elif _arm:
        main(arm=_arm)
    else:
        main()
