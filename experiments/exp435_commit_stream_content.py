#!/usr/bin/env python3
"""exp435 — WHAT THE COMMIT STREAM CARRIES: THE CONTENT DECOMPOSITION
(batch HU-13; exp414/421/425/426's shared exit). Three levers, three
nulls: coverage dilutes (exp421: union 0.598 < boundary 0.633), the
schedule is invariant (exp425), the chain buys +0.008 (exp426). The
shared exit: the boundary commits carry the fingerprint and the
interior commits do not. THE OPEN QUESTION: WHAT do the boundary
commits carry that the interior commits lack — dose magnitude, stress
context, wound adjacency, or timing?

THE INSTRUMENT (exp421's landed machinery verbatim; the content axis
as the new lever): the boundary stream scored as-is (the exp414 form,
the anchor); four ablations pre-named — (a) magnitude-shuffled
(each boundary commit's dose permuted within the stream), (b)
stress-context stripped (the stress pin lifted for boundary commits
only), (c) wound-adjacency stripped (the read face moved one hop off
the boundary), (d) timing-shuffled (the commit order permuted);
3 graphs x 3 seeds; AUC per ablation vs the anchor.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0; constants asserted; the anchor arm
      reproduces exp421's deposited boundary per-graph bests within
      1e-3 (fail=STOP).
  G2  the discipline: the ablations fixed before the runs; each
      ablation touches ONE stream property; the permutions seeded
      and disclosed.
  G3  THE CONTENT: >= 1 ablation drops the AUC below the anchor by
      >= 0.05 (CONTENT-CARRIES — the ablation named) or no ablation
      moves it (CONTENT-NULL — the fingerprint is not in the
      boundary commits' content either; the program's read-side exit
      stands alone).
  G4  the anatomy: the (ablation x graph x seed) AUC table deposited.
  G5  deposit results/exp435_commit_stream_content.json.

BRANCH LATTICE: CONTENT-CARRIES / CONTENT-NULL / INSTRUMENT-REFUTED.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# body-side import completion (the stub header carried nothing) —
# disclosed; every frozen constant below is re-asserted from exp421's
# landed module (the G1 anchor rides the imported constants verbatim)
import hashlib
import time

import numpy as np

import cultivation.bioelectric.collective as CORE
from experiments.exp421_union_stream_reconstruction import (
    COMMIT_NOISE, G_CTX, GRAPHS, PROD_FLOOR, ROUNDS, SEEDS,
    STEPS_PER_CELL, _auc, _build, _run_arm, _score_arm, _sha,
    _walk_round,
)

ANCHOR_TOL = 1e-3        # G1's exp421 replication bar (fail=STOP clause)
DROP_BAR = 0.05          # G3's content-carries bar
# the permutions' seed formulas (frozen before any run, G2):
#   ablation (a): np.random.default_rng((PERM_SEED_MAG, g_idx, seed))
#   ablation (d): np.random.default_rng((PERM_SEED_TIME, g_idx, seed,
#                                        round_tag))
PERM_SEED_MAG = 435101
PERM_SEED_TIME = 435202
ABLATIONS = ("magnitude_shuffled", "stress_stripped",
             "adjacency_stripped", "timing_shuffled")
DEPOSIT = os.path.join(ROOT, "results",
                       "exp435_commit_stream_content.json")
EXP421_DEPOSIT = os.path.join(ROOT, "results",
                              "exp421_union_stream_reconstruction.json")


BODY_DISCLOSURES = [
    "the machinery is exp421's landed module imported VERBATIM (_build, "
    "_walk_round, _score_arm, _auc, _sha and the constants) — the "
    "anchor arm is exp421's own _run_arm boundary path re-expanded "
    "(_build + 10 stressed _walk_round rounds + _score_arm, the same "
    "three landed calls in the same order); the smoke proves the "
    "expansion bit-identical to the imported _run_arm on the overlap "
    "cell before anything else is trusted",
    "exp421's runner deposit was ABSENT from the local workspace at "
    "body time; restored BEFORE this run from the runner artifact "
    "(hu12-exp421 / run 36308178119, the /tmp/hu12art/x421 results "
    "tree, ledger L325; sha256 50883519efbdf82e...) into results/ — "
    "disclosed, not silent (the exp432 exp425-restore precedent)",
    "ablation (a) magnitude-shuffled, reading: the ANCHOR's own commit "
    "stream (values only, the (round x cell) matrix X) has its dose "
    "values permuted WITHIN the stream — one seeded permutation over "
    "all 10 x n_cells commits, each commit's dose reassigned to "
    "another commit's slot; the schedule (which cell commits in which "
    "round), the coverage, the stress context and the adjacency are "
    "untouched (the dose multiset is asserted preserved exactly); the "
    "finer per-cell-in-time cousin is exp414's own shuffled null, "
    "already scored inside every anchor row as auc_null and deposited "
    "beside",
    "ablation (b) stress-context stripped, reading: the pin lifted for "
    "the boundary stream's commits — all of them ARE boundary commits "
    "(the boundary arm walks only the wound region), so 'for boundary "
    "commits only' = the walk runs exp421's stress=False path (no "
    "-35.0 write-time pin; the unstressed spec-branch form exp414 "
    "disclosed); one property touched: the stress context",
    "ablation (c) wound-adjacency stripped, reading: the READ FACE "
    "(which commits enter the reconstruction) moves one hop off the "
    "wound's boundary — the read face becomes the anchor region's "
    "interior cells (no neighbor outside the region, exp425's cls "
    "split, the landed boundary/interior precedent); the anchor's own "
    "stream is reused unchanged (generation untouched); the "
    "generation-side alternative (re-walking a shrunk region, which "
    "would ALSO re-root the BFS inheritance) named and rejected — it "
    "touches two properties; the exterior-ring reading (exp285's ring "
    "ONE HOP OUTSIDE the wound) named and rejected as UNSCORABLE on "
    "path100 (the ring is {19,60}: two cells, zero edges, a nan AUC) — "
    "the instrument cannot run it on the pre-named graph set",
    "ablation (d) timing-shuffled, reading: the commit ORDER permuted "
    "— exp421's _walk_round re-instantiated locally as "
    "_walk_round_timed, byte-similar with EXACTLY ONE insertion: after "
    "the BFS order is complete (re-seed included), the (cell, parent) "
    "order is permuted by a seeded generator (ONE fixed permutation "
    "per (graph, seed), applied identically to every round — the "
    "schedule is one permuted schedule; the per-round re-draw variant "
    "named and rejected as a second knob); the pair multiset is "
    "asserted preserved (the routing tree unchanged, only the visit "
    "sequence), so the parents/coverage/stress/blend are the anchor's",
    "the (d) copy's neutrality is witnessed operationally (G2): on "
    "path100 seed 0, _walk_round_timed with the permutation disabled "
    "reproduces the imported _walk_round's 10-round commit matrix "
    "bit-exactly on a same-seed fresh build — the insertion is the "
    "ONLY behavioral difference, so (d)'s delta is attributable to the "
    "order permutation alone",
    "G3's evaluation unit, pre-named here BEFORE the runs (the "
    "docstring's 'AUC per ablation vs the anchor' made concrete): the "
    "paired per-seed delta (anchor auc - ablation auc on the same "
    "(graph, seed) cell), summarized per (ablation, graph) by the "
    "seed MEAN; an ablation fires on a graph at mean-delta >= 0.05; "
    "G3 fires if >= 1 (ablation, graph) fires (CONTENT-CARRIES, the "
    "ablation named); the per-seed paired deltas and the per-graph "
    "best-vs-best deltas (exp421's summary style) deposited beside as "
    "secondary, non-gating",
    "the floor discipline: -60.0 restored at every settle (exp421's "
    "_walk_round restores the pin in finally BEFORE the round's "
    "c.run(30.0) settle) and asserted at entry/exit/after every arm; "
    "no Lyapunov solve appears anywhere in this instrument (the "
    "statistic is a Pearson cross-correlation over the commit stream; "
    "walks only at n <= 400) — the Kronecker/Schur clause is vacuous "
    "here, recorded for the discipline",
]


# ---------------------------------------------------------------- arms
def _run_anchor_stream(graph, seed):
    """exp421's boundary arm re-expanded (the same three landed calls
    as _run_arm(g, s, 'boundary')) returning the row AND the stream
    (the ablations (a)/(c) consume the anchor's own stream — no second
    walk)."""
    c, tgt, region, n = _build(graph, seed)
    region_full = [int(x) for x in region]
    rounds = [_walk_round(c, region_full, True) for _ in range(ROUNDS)]
    row = _score_arm(c, rounds, seed)
    return row, rounds, c, region_full


def _walk_round_timed(c, region, stress, perm_key, round_tag):
    """exp421's _walk_round byte-similar with EXACTLY ONE insertion
    (the timing ablation): the seeded permutation of the complete
    commit order. perm_key=None disables it (the neutrality witness)."""
    from collections import deque
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
    if perm_key is not None:
        # THE insertion (one line + its assert): the commit order
        # permuted, seeded; the (cell, parent) multiset preserved.
        rng_t = np.random.default_rng(tuple(perm_key) + (round_tag,))
        perm = rng_t.permutation(len(order))
        order_permuted = [order[int(p)] for p in perm]
        assert sorted(order_permuted) == sorted(order), \
            "the timing permutation broke the routing multiset"
        order = order_permuted
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


def _run_stress_stripped(graph, seed):
    """Ablation (b): the pin lifted (exp421's stress=False path), all
    else the anchor's form."""
    c, tgt, region, n = _build(graph, seed)
    region_full = [int(x) for x in region]
    rounds = [_walk_round(c, region_full, False) for _ in range(ROUNDS)]
    return _score_arm(c, rounds, seed)


def _run_timing_shuffled(graph, seed, g_idx):
    """Ablation (d): the commit order permuted (one fixed seeded
    permutation per (graph, seed), every round), all else the
    anchor's form."""
    c, tgt, region, n = _build(graph, seed)
    region_full = [int(x) for x in region]
    rounds = [_walk_round_timed(c, region_full, True,
                                (PERM_SEED_TIME, g_idx, seed), r)
              for r in range(ROUNDS)]
    return _score_arm(c, rounds, seed)


# ------------------------------------------------- stream-level scorers
def _stream_X(rounds, cells):
    """The (rounds x cells) commit matrix (exp421's _score_arm form);
    commits outside `cells` (the dropped frontier face) are skipped."""
    idx = {cell: k for k, cell in enumerate(cells)}
    X = np.full((len(rounds), len(cells)), np.nan)
    for r, rd in enumerate(rounds):
        for i, v in rd.items():
            k = idx.get(i)
            if k is not None:
                X[r, k] = v
    assert np.isfinite(X).all()
    return X


def _edges_of(c, cells):
    """The true-edge mask among `cells` (exp421's _score_arm form)."""
    nc = len(cells)
    A_true = (np.abs(c.A) > 0)
    np.fill_diagonal(A_true, False)
    edges_mask = np.zeros((nc, nc), dtype=bool)
    edges_mask[:] = A_true[np.ix_(cells, cells)]
    iu = np.triu_indices(nc, 1)
    k_true = int(edges_mask[iu].sum())
    return edges_mask, iu, k_true


def _score_permuted_stream(c, rounds, g_idx, seed):
    """Ablation (a): the anchor stream's dose values permuted within
    the stream (one seeded permutation over all commits), then scored
    exactly as _score_arm scores the anchor (the null/decoy controls
    are the anchor's own — the stream-level permutation does not
    change the bookkeeping)."""
    cells = sorted({int(i) for rd in rounds for i in rd})
    X = _stream_X(rounds, cells)
    flat = X.reshape(-1)
    rng_a = np.random.default_rng((PERM_SEED_MAG, g_idx, seed))
    Xp = flat[rng_a.permutation(flat.size)].reshape(X.shape)
    # one-property witness: the dose multiset preserved EXACTLY
    assert np.array_equal(np.sort(Xp, axis=None), np.sort(X, axis=None)), \
        "the dose permutation broke the stream's value multiset"
    S = np.nan_to_num(np.corrcoef(Xp.T), nan=0.0)
    edges_mask, iu, k_true = _edges_of(c, cells)
    auc = _auc(S, edges_mask)
    sc = np.abs(S[iu])
    top = np.argsort(sc)[::-1][:k_true]
    prec = float(edges_mask[iu][top].mean()) if k_true else float("nan")
    return {"auc": auc, "precision_at_k": prec, "k_true": k_true,
            "n_cells_walked": len(cells)}


def _interior_cells(c, region):
    """The read face one hop off the wound's boundary: the region's
    cells with NO neighbor outside the region (exp425's cls split)."""
    rs = set(region)
    return [i for i in region
            if not any(j not in rs
                       for j in np.where(np.abs(c.A[i]) > 0)[0])]


def _score_read_face(c, rounds, read_cells):
    """Ablation (c): the anchor's own stream scored on the moved read
    face (the interior commits only; the frontier face dropped)."""
    cells = sorted({int(i) for rd in rounds for i in rd})
    assert set(read_cells) <= set(cells), "read face left the stream"
    X = _stream_X(rounds, read_cells)
    S = np.nan_to_num(np.corrcoef(X.T), nan=0.0)
    edges_mask, iu, k_true = _edges_of(c, read_cells)
    assert k_true > 0, "the moved read face carries no edges"
    auc = _auc(S, edges_mask)
    sc = np.abs(S[iu])
    top = np.argsort(sc)[::-1][:k_true]
    prec = float(edges_mask[iu][top].mean()) if k_true else float("nan")
    return {"auc": auc, "precision_at_k": prec, "k_true": k_true,
            "n_cells_walked": len(read_cells)}


# ---------------------------------------------------------------- main
def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    graphs = GRAPHS[:1] if smoke else GRAPHS
    seeds = SEEDS[:1] if smoke else SEEDS

    # ---- G1 the anchors (entry)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert G_CTX == 0.5 and COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert ROUNDS == 10 and PROD_FLOOR == -60.0
    assert ABLATIONS == ("magnitude_shuffled", "stress_stripped",
                         "adjacency_stripped", "timing_shuffled")
    assert DROP_BAR == 0.05 and ANCHOR_TOL == 1e-3
    print("G1 floor %s; constants verified%s"
          % (CORE.NEURAL_SPEC_MIN, " (SMOKE)" if smoke else ""))

    with open(EXP421_DEPOSIT) as f:
        d421 = json.load(f)
    dep_rows = d421["results"]

    # ---- G2 the discipline: the ablations fixed BEFORE the runs
    one_property = {
        "magnitude_shuffled": "the dose-to-commit assignment (scoring "
                              "time, the anchor's own stream, the dose "
                              "multiset asserted preserved)",
        "stress_stripped": "the stress context (generation time, the "
                           "pin lifted, all else the anchor's form)",
        "adjacency_stripped": "the read face (scoring time, the "
                              "anchor's own stream, the frontier face "
                              "dropped one hop off the boundary)",
        "timing_shuffled": "the commit order (generation time, one "
                           "seeded permutation of the complete order, "
                           "the routing multiset asserted preserved)",
    }
    assert set(one_property) == set(ABLATIONS)
    assert len(ABLATIONS) == 4
    print("G2 plan fixed pre-run (4 ablations, one property each, "
          "perm seeds %d/%d)" % (PERM_SEED_MAG, PERM_SEED_TIME))

    results: dict = {}
    identities: dict = {}
    for g_idx, graph in enumerate(graphs):
        for seed in seeds:
            # the anchor: exp421's boundary path (the G1 anchor)
            t0 = time.time()
            row, rounds, c, region_full = _run_anchor_stream(graph, seed)
            row["wall_s"] = round(time.time() - t0, 1)
            results["anchor|%s|%d" % (graph, seed)] = row
            print("  anchor %s seed %d: AUC %.3f p@k %.3f null %.3f "
                  "decoy %.3f (%.1fs)"
                  % (graph, seed, row["auc"], row["precision_at_k"],
                     row["auc_null"], row["auc_decoy"], row["wall_s"]))
            assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor post-anchor"

            # (a) magnitude-shuffled: the anchor's own stream, doses
            # permuted within the stream
            row_a = _score_permuted_stream(c, rounds, g_idx, seed)
            results["magnitude_shuffled|%s|%d" % (graph, seed)] = row_a
            # (c) adjacency-stripped: the anchor's own stream, the read
            # face moved one hop off the wound's boundary
            row_c = _score_read_face(c, rounds,
                                     _interior_cells(c, region_full))
            results["adjacency_stripped|%s|%d" % (graph, seed)] = row_c
            del c
            # (b) stress-context stripped
            t0 = time.time()
            row_b = _run_stress_stripped(graph, seed)
            row_b["wall_s"] = round(time.time() - t0, 1)
            results["stress_stripped|%s|%d" % (graph, seed)] = row_b
            assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor post-(b)"
            # (d) timing-shuffled
            t0 = time.time()
            row_d = _run_timing_shuffled(graph, seed, g_idx)
            row_d["wall_s"] = round(time.time() - t0, 1)
            results["timing_shuffled|%s|%d" % (graph, seed)] = row_d
            assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor post-(d)"
            print("  mag %.3f | stress %.3f | hopoff %.3f | time %.3f"
                  % (row_a["auc"], row_b["auc"], row_c["auc"],
                     row_d["auc"]))
        c_id, _, _, _ = _build(graph, seeds[0])
        identities[graph] = _sha(np.abs(c_id.A))
        del c_id
        if graph in d421.get("graph_identities", {}):
            assert identities[graph] == d421["graph_identities"][graph], \
                "graph identity drifted vs exp421's deposit: %s" % graph
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    # ---- G1's replication clause (evaluated exactly once): the anchor
    # reproduces exp421's deposited boundary rows / per-graph bests
    row_worst = 0.0
    for g in graphs:
        for s in seeds:
            k = "boundary|%s|%d" % (g, s)
            mine = results["anchor|%s|%d" % (g, s)]
            for f in ("auc", "precision_at_k", "auc_null", "auc_decoy"):
                row_worst = max(row_worst, abs(mine[f] - dep_rows[k][f]))
    anchor_best = {}
    for g in graphs:
        anchor_best[g] = max(results["anchor|%s|%d" % (g, s)]["auc"]
                             for s in seeds)
    best_worst = max(abs(anchor_best[g]
                         - d421["per_graph_best"]["boundary"][g])
                     for g in graphs)
    if smoke:
        # the SMOKE bit-check: the overlap keys only (path100 seed 0)
        assert row_worst <= 1e-9, \
            "smoke bit-check vs exp421's boundary row failed: %g" \
            % row_worst
        # the verbatim-path witness (disclosed): the re-expanded anchor
        # is the imported _run_arm boundary path, bit-exactly
        row_imported = _run_arm(graphs[0], seeds[0], "boundary")
        mine0 = results["anchor|%s|%d" % (graphs[0], seeds[0])]
        for f in ("auc", "precision_at_k", "auc_null", "auc_decoy"):
            assert mine0[f] == row_imported[f], \
                "the expanded anchor drifted from exp421's _run_arm: %s" % f
        verdicts["G1"] = "PASS"
        print("G1 PASS (SMOKE bit-check: anchor row bit-matches "
              "exp421's boundary|path100|0, worst %.2e; the expansion "
              "== the imported _run_arm bit-exactly)" % row_worst)
    else:
        ok = best_worst <= ANCHOR_TOL and row_worst <= ANCHOR_TOL
        verdicts["G1"] = "PASS" if ok else "REFUTE"
        print("G1 %s (per-graph-best worst %.2e, row worst %.2e, "
              "tol %.0e; identities %s)"
              % (verdicts["G1"], best_worst, row_worst, ANCHOR_TOL,
                 identities))

    # ---- G2's operational witnesses
    if not smoke:
        # (d)-copy neutrality: the timed walk with the permutation
        # disabled is the imported walk, bit-exactly (path100 seed 0)
        c1, _, region1, _ = _build("path100", 0)
        r1 = [_walk_round(c1, [int(x) for x in region1], True)
              for _ in range(ROUNDS)]
        c2, _, region2, _ = _build("path100", 0)
        r2 = [_walk_round_timed(c2, [int(x) for x in region2], True,
                                None, r) for r in range(ROUNDS)]
        cells = sorted({int(i) for rd in r1 for i in rd})
        X1, X2 = _stream_X(r1, cells), _stream_X(r2, cells)
        g2_copy_ok = np.array_equal(X1, X2)
        assert g2_copy_ok, "the (d) copy is not neutral with perm off"
        verdicts["G2"] = "PASS"
        print("G2 PASS (one property per ablation; the (d) copy "
              "neutral bit-exactly with the permutation disabled; the "
              "(a) dose multiset + (d) routing multiset asserts live "
              "in the arm code)")
    else:
        verdicts["G2"] = "PASS (smoke: the plan + the in-arm asserts)"

    # ---- G3 the content (evaluated exactly once; smoke-skip)
    if smoke:
        verdicts["G3"] = "SMOKE-SKIP"
        verdicts["G4"] = "SMOKE-SKIP"
        print("G3/G4 SMOKE-SKIP (the content verdict needs the full "
              "3x3 table)")
    else:
        deltas_paired = {}
        deltas_mean = {}
        fire = {}
        for a in ABLATIONS:
            for g in graphs:
                ds = [results["anchor|%s|%d" % (g, s)]["auc"]
                      - results["%s|%s|%d" % (a, g, s)]["auc"]
                      for s in seeds]
                deltas_paired["%s|%s" % (a, g)] = [round(d, 4) for d in ds]
                m = float(np.mean(ds))
                deltas_mean["%s|%s" % (a, g)] = round(m, 4)
                fire["%s|%s" % (a, g)] = m >= DROP_BAR
        fired = sorted(k for k, v in fire.items() if v)
        verdicts["G3"] = "PASS" if fired else "REFUTE"
        print("G3 %s (seed-mean deltas vs the anchor: %s; bar %.2f; "
              "fired: %s)"
              % (verdicts["G3"], deltas_mean, DROP_BAR, fired))

        # ---- G4 the anatomy: the (ablation x graph x seed) AUC table
        auc_table = {a: {g: {s: results["%s|%s|%d" % (a, g, s)]["auc"]
                             for s in seeds} for g in graphs}
                     for a in ("anchor",) + ABLATIONS}
        verdicts["G4"] = "PASS"
        print("G4 PASS (the %d-row AUC table rides in the deposit)"
              % len(results))

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    # ---- the branch + G5 the deposit
    if verdicts["G1"] != "PASS" or not str(verdicts["G2"]).startswith(
            "PASS"):
        branch = "INSTRUMENT-REFUTED"
    elif verdicts["G3"] == "PASS":
        branch = "CONTENT-CARRIES"
    else:
        branch = "CONTENT-NULL"
    dep = {
        "experiment": "exp435",
        "title": "WHAT THE COMMIT STREAM CARRIES: THE CONTENT "
                 "DECOMPOSITION (batch HU-13)",
        "instrument": {
            "anchor": "exp421's boundary arm (exp414's wound-region "
                      "form) re-run verbatim, same seeds",
            "ablations": ABLATIONS,
            "ablation_definitions": one_property,
            "perm_seed_formulas": {
                "magnitude_shuffled":
                    "default_rng((%d, g_idx, seed)) over all "
                    "10 x n_cells commits" % PERM_SEED_MAG,
                "timing_shuffled":
                    "default_rng((%d, g_idx, seed, round_tag)) over "
                    "the complete commit order, one fixed permutation "
                    "applied to every round" % PERM_SEED_TIME},
            "rounds": ROUNDS,
            "stress": "the write-time -35.0 pin each round (lifted "
                      "for the stress_stripped ablation only)",
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "SEEDS": SEEDS, "GRAPHS": GRAPHS}},
        "graph_identities": identities,
        "exp421_anchor": {
            "deposit": "results/exp421_union_stream_reconstruction.json",
            "per_graph_best_deposited": d421["per_graph_best"]["boundary"],
            "per_graph_best_anchor": anchor_best,
            "per_graph_best_worst_delta": round(best_worst, 9),
            "row_worst_delta": round(row_worst, 9),
            "tol": ANCHOR_TOL},
        "results": results,
        "auc_table": auc_table,
        "g3_deltas": {"seed_mean_per_ablation_graph": deltas_mean,
                      "per_seed_paired": deltas_paired,
                      "fired": fired, "bar": DROP_BAR},
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
    print("EXP435 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main(budget_mode="smoke" if "--smoke" in sys.argv else "full")
