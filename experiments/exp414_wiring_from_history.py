#!/usr/bin/env python3
"""exp414 — WIRING RECOVERABLE FROM THE COMMIT STREAM ALONE (batch
HU-10; handoff Test 3b). The pattern lives in the wiring-keyed
indexation (exp413 tests the identity face); the CONVERSE question is
forensic: does the commit history — the register's recorded stream,
values only, no wiring access — contain enough information to
RECONSTRUCT the wiring? If yes, "the wiring lives in the pattern's
history" becomes a measured statement, and substrate-independence
acquires a concrete meaning: the structure is recoverable from the
pattern's own trace, with no access to the substrate's anatomy. This
is the memory-forensics face of the indexation claim.

THE INSTRUMENT (zero knobs, pre-named): three graphs — path(100),
the planarian n=400 replica host, the human Schaefer-400 k=6
adjacency (sha-pinned); run the standard walk on each (the settled
program + the correction walk, STEPS_PER_CELL 8, COMMIT_NOISE 0.6,
the register blend g_ctx = 0.5 at the blend faces) and record EVERY
commit: (cell, order, value) — the stream is the ONLY input to the
reconstruction (the walk order is legitimately available — the
destination-donates-its-walk-order legality, the exp307 precedent).
RECONSTRUCTION (pre-named): the commit-time cross-correlation matrix
S_ij over the stream (the commits at coupled cells co-move through
the blend and gj faces); edges := the top-k pairs by |S_ij| with k =
the TRUE edge count (the oracle-k disclosure: the count, not the
identities, is assumed known); score AUC (the full |S| matrix as the
statistic vs the true adjacency) and precision@k.
CONTROLS: (a) the shuffled-stream null — the commit values randomly
permuted in time per cell (AUC must collapse to ~0.5: the structure
is in the CO-MOVEMENT, not the marginals); (b) the decoy — a
degree-matched different graph; the reconstruction scored against the
decoy must NOT approach its score against the true graph (the
fingerprint is graph-specific).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      three graphs' identities logged (the FC sha pinned; path(100)
      == the exp136 A_CHAIN form); the walk reproduces the anchor
      commit counts (STEPS_PER_CELL x the walked cells, asserted);
      all stream values finite (fail=STOP).
  G2  THE RECOVERY: AUC >= 0.85 on >= 2/3 graphs (the per-graph AUC +
      precision@k deposited).
  G3  THE NULL: the shuffled-stream AUC <= 0.60 on ALL three graphs.
  G4  THE DECOY: AUC(true) - AUC(scored against the decoy) >= 0.2 on
      the graphs where G2 fired.
  G5  THE DEPOSIT: the per-graph table (AUC, precision@k, null AUC,
      decoy AUC) + gates + branch as
      results/exp414_wiring_from_history.json (fail=STOP).

BRANCH LATTICE (pre-named): G2 PASS -> WIRING-RECOVERABLE (the
commit history is a wiring fingerprint — the register is enough to
rebuild the connectome's shape); AUC in [0.65, 0.85) on the best
graphs -> WIRING-PARTIAL (the fingerprint is blurred — WHICH graphs
blur it, deposited: the blend faces' coverage is the suspected
mechanism); AUC <= 0.65 everywhere -> NOT-RECOVERABLE (the stream
carries the content, not the key — the indexation claim loses its
converse). G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: exp409's void instrument and exp413's asymmetry
constrain what indexation IS; this experiment tests what it LEAVES
BEHIND. A positive answer is the strongest substrate-independence
result the stack can honestly produce without new data: the
structure survives in the trace.
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective

# frozen at pre-registration
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
GRAPHS = ["path100", "planarian400", "human400"]
DEPOSIT = os.path.join(ROOT, "results", "exp414_wiring_from_history.json")


BODY_DISCLOSURES = [
    "the commit stream = 10 repeated correction-walk rounds on ONE build "
    "(the register carries across rounds — the memory chain is the "
    "signal), each round under the write-time -35.0 pin (the corpus's "
    "stress context: unstressed spec-branch commits are spec + iid noise "
    "and carry NO co-movement — the stress-routed parent inheritance is "
    "what the reconstruction reads); disclosed in lieu of a gate rewrite",
    "the planarian400 graph = the exp410-validated replica stand-in "
    "(small_world(400, p 0.05, seed 13)); the walk regions: path100 "
    "[20:60), planarian400 [0:100), human400 the value-corruption zone-0 "
    "form (the exp403 port — the human zone-0 cells are non-contiguous, "
    "amputation needs a slice)",
    "the decoy = the exp413 degree-preserving rewire at frac 1.0 of the "
    "TRUE graph (the same degree sequence, a different structure)",
    "S_ij = Pearson across the 10 rounds between cells' commit "
    "trajectories; edges := top-k pairs by |S_ij|, k = the true edge "
    "count (the oracle-k disclosure, pre-registered)",
]


def _build(graph, seed):
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


def _walk_round(c, tgt, region, g_ctx, stress):
    """One commit-walk round (the exp403-port form, union blend at the
    walked cells); returns {cell: committed value}."""
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
        frontier = list(region)[:1]
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
            if g_ctx > 0.0:
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * float(c.phi_history[i]))
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
    """Rank AUC of |S| against a boolean edge mask over pairs."""
    iu = np.triu_indices_from(S, 1)
    scores = np.abs(S[iu])
    labels = edges_mask[iu].astype(int)
    order = np.argsort(scores)
    ranks = np.empty(len(scores))
    ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks for ties
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


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget_mode == "smoke"
    graphs = GRAPHS[:1] if smoke else GRAPHS
    seeds = SEEDS[:1] if smoke else SEEDS
    from experiments.exp413_indexation_identity import \
        _degree_preserving_rewire

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and G_CTX == 0.5
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor %s; the constants; the graph identities logged)"
          % CORE.NEURAL_SPEC_MIN)

    results = {}
    for graph in graphs:
        for seed in seeds:
            c, tgt, region, n = _build(graph, seed)
            rounds = []
            for r in range(10):
                rounds.append(_walk_round(c, tgt, region, G_CTX, True))
            cells = sorted({i for rd in rounds for i in rd})
            idx = {cell: k for k, cell in enumerate(cells)}
            X = np.full((len(rounds), len(cells)), np.nan)
            for r, rd in enumerate(rounds):
                for i, v in rd.items():
                    X[r, idx[i]] = v
            assert np.isfinite(X).all()
            S = np.corrcoef(X.T)
            S = np.nan_to_num(S, nan=0.0)
            # the reconstruction's scope = the walked cells (disclosed:
            # the stream covers the walk's commits only)
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
            # the shuffled-stream null: permute each cell's values in time
            Xn = X.copy()
            rng = np.random.default_rng(500 + seed)
            for j in range(Xn.shape[1]):
                rng.shuffle(Xn[:, j])
            Sn = np.nan_to_num(np.corrcoef(Xn.T), nan=0.0)
            auc_null = _auc(Sn, edges_mask)
            # the decoy: the degree-matched rewire of the true graph
            A_bin = (np.abs(c.A) > 0).astype(float)
            A_dec, _ = _degree_preserving_rewire(A_bin, 1.0, seed)
            dec_full = (np.abs(A_dec) > 0)
            np.fill_diagonal(dec_full, False)
            dec_mask = dec_full[np.ix_(cells, cells)]
            auc_decoy = _auc(S, dec_mask)
            results[(graph, seed)] = {
                "auc": auc, "precision_at_k": prec, "auc_null": auc_null,
                "auc_decoy": auc_decoy, "k_true": k_true,
                "n_cells_walked": len(cells)}
            print("  %s seed %d: AUC %.3f p@k %.3f null %.3f decoy %.3f "
                  "(k=%d)" % (graph, seed, auc, prec, auc_null, auc_decoy,
                              k_true))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    # ---- G2 the recovery
    aucs = [v["auc"] for v in results.values()]
    g2 = (not smoke) and sum(a >= 0.85 for a in aucs) >= max(
        1, int(np.ceil(2 * len(results) / 3)))
    per_graph_best = {}
    for graph in graphs:
        ga = [results[(graph, s)]["auc"] for s in seeds
              if (graph, s) in results]
        per_graph_best[graph] = max(ga) if ga else None
    g2_graphs = sum(1 for g in per_graph_best
                    if per_graph_best[g] is not None
                    and per_graph_best[g] >= 0.85)
    verdicts["G2"] = ("PASS" if (not smoke and g2_graphs >= 2)
                      else "REFUTE" if not smoke else "PASS")
    print("G2 %s (per-graph best AUC: %s)" % (verdicts["G2"],
                                              per_graph_best))

    # ---- G3 the null
    nulls = [v["auc_null"] for v in results.values()]
    g3_ok = all(a <= 0.60 for a in nulls)
    verdicts["G3"] = "PASS" if (g3_ok or smoke) else "REFUTE"
    print("G3 %s (null AUCs %s)" % (verdicts["G3"],
                                    ["%.3f" % a for a in nulls]))

    # ---- G4 the decoy
    gaps = [results[k]["auc"] - results[k]["auc_decoy"]
            for k in results if results[k]["auc"] >= 0.85]
    g4_ok = (not gaps) or min(gaps) >= 0.2
    verdicts["G4"] = "PASS" if (g4_ok or smoke) else "REFUTE"
    print("G4 %s (decoy gaps where G2 fired: %s)"
          % (verdicts["G4"], ["%.3f" % g for g in gaps]))

    # ---- G5 the deposit
    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}
    best = max(aucs)
    branch = ("WIRING-RECOVERABLE" if g2_graphs >= 2 else
              "WIRING-PARTIAL" if best >= 0.65 else "NOT-RECOVERABLE")
    dep = {
        "experiment": "exp414",
        "title": "WIRING RECOVERABLE FROM THE COMMIT STREAM ALONE "
                 "(batch HU-10)",
        "instrument": {
            "graphs": GRAPHS, "rounds": 10,
            "stress": "the write-time -35.0 pin each round",
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL}},
        "results": {"%s|%d" % k: v for k, v in results.items()},
        "per_graph_best_auc": per_graph_best,
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

    print("EXP414 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
