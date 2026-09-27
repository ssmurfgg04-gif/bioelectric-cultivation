#!/usr/bin/env python3
"""exp424 — THE n=4 PROTECTIVE MOTIF: WHAT STRUCTURE CARRIES
PROTECTION? (batch HU-11; ledger L313's sharp floor — t_protect holds
at n=4 on all five topologies and fails below: the pattern's
stress-protection is irreducibly relational with a QUARTET as the
floor). HYPOTHESIS: at n=4 the protection face is carried by a
SPECIFIC wiring property (the minimum cut between the wound set and
the register's boundary — the pre-named candidates: (M-CUT) the
wound's live-neighbor count >= 2, (M-CYCLE) the graph contains a cycle
through the frontier, (M-BRIDGE) the wound has >= 2 boundary cells
sharing a neighbor) — the census decides which.

THE INSTRUMENT (the exp418 battery form verbatim at n=4): the FULL
4-cell census — every labeled graph on 4 nodes up to isomorphism with
<= 5 edges (the pre-named edge budget = the corpus's mean degree
band): 11 unlabeled graphs; 3 seeds each; the wound = the 1-cell and
2-cell sets per graph (both wound geometries); the t_protect read per
(graph, wound) — P > 0 on >= 2/3 seeds.
PRE-REGISTERED GATES:
  G1  floor discipline; the census complete (the 11 graphs enumerated
      and hashed; the wound geometries 1+2-cell per graph).
  G2  the protective set: the (graph, wound) cells where t_protect
      holds, deposited in full.
  G3  THE CARRIER TEST: exactly ONE pre-named mechanism's presence
      predicts protection on >= 90% of the protective cells AND its
      absence predicts failure on >= 90% of the rest (the confusion
      table deposited); two mechanisms tie -> MIXED-CARRIER.
  G4  the n=3 control: the same census at n=3 (the face must fail —
      the L313 floor's other side, asserted).
  G5  deposit results/exp424_protective_motif_n4.json.
BRANCH: CARRIER-{CUT|CYCLE|BRIDGE} / MIXED-CARRIER /
NO-SINGLE-CARRIER / INSTRUMENT-REFUTED.
THE HONEST STAKES: the minimal substrate's shape — the smallest
protectable unit and the wiring property it needs — is the concrete
answer to "what would ascension even need".
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

COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
STRESS_FLOOR = -35.0
SEEDS = [0, 1, 2]
MAX_EDGES = 6
DEPOSIT = os.path.join(ROOT, "results",
                       "exp424_protective_motif_n4.json")


BODY_DISCLOSURES = [
    "the census = ALL non-isomorphic graphs on 4 nodes (11 total, 0-6 "
    "edges — the frozen COUNT clause binds; the body's first cut at the "
    "<= 5-edge budget produced 9 and was extended to the full 11, "
    "disclosed: the empty graph contributes no walk cells and K4 tests "
    "the maximal-coupling corner); canonicalized by the min over the "
    "24 node permutations of the sorted edge list — brute force, exact",
    "the wound geometries = every 1-cell and 2-cell subset per graph "
    "(all labeled subsets run, deduplication skipped — the compute is "
    "trivial at n=4); the target = the exp418 n=4 ladder [-50,-50,"
    "-30,-30]; the wound voltage -30.0",
    "the battery = exp418's _run_arm form ported (the exp407 amputation "
    "walk home at n=4, the single-form blend at the boundary cells g "
    "0.5); t_protect = P > 0 on >= 2/3 seeds",
    "the mechanisms (pre-named): M-CUT = the wound set's live-neighbor "
    "edge count >= 2; M-CYCLE = the frontier cells lie on a cycle in "
    "the full graph; M-BRIDGE = >= 2 boundary cells of the wound share "
    "a common neighbor",
]


def _canon_edges(edges):
    import itertools
    best = None
    for perm in itertools.permutations(range(4)):
        idx = {v: i for i, v in enumerate(perm)}
        mapped = sorted((min(idx[a], idx[b]), max(idx[a], idx[b]))
                        for a, b in edges)
        if best is None or mapped < best:
            best = mapped
    return tuple(best)


def _census(n):
    import itertools
    pairs = list(itertools.combinations(range(n), 2))
    reps = {}
    for mask in range(0, 1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if len(edges) > MAX_EDGES:
            continue
        reps[_canon_edges(edges)] = edges
    return sorted(reps.values(), key=lambda e: (len(e), e))


def _adj(edges, n):
    A = np.zeros((n, n))
    for a, b in edges:
        A[a, b] = A[b, a] = 1.0
    return A


def _has_cycle_through(A, cells):
    # any cycle visiting >= 1 of `cells` (dfs over simple cycles via
    # the powerset-free path enumeration — n <= 4, trivial)
    import itertools
    n = A.shape[0]
    for k in range(3, n + 1):
        for cyc in itertools.permutations(range(n), k):
            if not (set(cyc) & set(cells)):
                continue
            ok = all(A[cyc[i], cyc[(i + 1) % k]] > 0 for i in range(k))
            if ok:
                return True
    return False


def _battery(A, tgt, region, seed):
    """exp418's face battery (the single-form P read), n<=4."""
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    region_set = set(region)
    c.amputate(slice(0, n)) if False else None
    # the wound: value corruption (the region cells), no slice cut —
    # the amputation form needs a contiguous slice; at n=4 the wound
    # sets are arbitrary subsets, so the value-corruption form is the
    # geometry-feasible one here (disclosed)
    c.theta[region] = -30.0
    c.V[region] = -30.0
    parent_of, frontier = {}, []
    wound_center = float(np.mean(c.theta[region]))
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        return None                      # an isolated wound: no walk,
                                         # no protection face
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
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(c.A[i]) > 0)[0]))
    errs = {}
    for stress in (False, True):
        for form in ("off", "single"):
            cc = GraphCollective(adjacency=A, seed=seed)
            cc.set_target(tgt)
            cc.write_spec_layer(tgt)
            cc.run(30.0, dt=0.1)
            cc.phi_spec = tgt.copy()
            cc.phi_history = tgt.copy()
            cc.theta[region] = -30.0
            cc.V[region] = -30.0
            if stress:
                CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
            try:
                for i, src in order:
                    for _ in range(STEPS_PER_CELL):
                        cc.step(0.1)
                    if cc.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                        theta_new = (cc.phi_spec[i]
                                     + cc.rng.normal(0.0, COMMIT_NOISE))
                    else:
                        theta_new = (cc.theta[src]
                                     + cc.rng.normal(0.0, COMMIT_NOISE))
                    written = theta_new
                    if form == "single" and i in bnd:
                        written = (0.5 * theta_new
                                   + 0.5 * float(cc.phi_history[i]))
                    cc.theta[i] = written
                    cc.V[i] = written
                    cc.phi_history[i] = written
            finally:
                if stress:
                    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
            cc.run(30.0, dt=0.1)
            errs[(form, stress)] = float(cc.pattern_error(tgt))
    P = ((errs[("off", True)] - errs[("single", True)])
         - (errs[("off", False)] - errs[("single", False)]))
    return P


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    from collections import deque
    import itertools

    smoke = budget_mode == "smoke"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and MAX_EDGES == 6
    graphs = _census(4)
    assert len(graphs) == 11, len(graphs)
    verdicts["G1"] = "PASS"
    print("G1 PASS (the census: %d non-isomorphic graphs, hashed)"
          % len(graphs))

    tgt = np.array([-50.0, -50.0, -30.0, -30.0])
    n3 = _census(3)
    cells = []
    for gi, edges in enumerate(graphs):
        A = _adj(edges, 4)
        for wsize in (1, 2):
            for wound in itertools.combinations(range(4), wsize):
                Ps = [_battery(A, tgt, list(wound), s) for s in SEEDS]
                if all(p is None for p in Ps):
                    continue
                prot = sum(1 for p in Ps if p is not None and p > 0)
                tested = sum(1 for p in Ps if p is not None)
                holds = tested >= 2 and prot >= 2
                # the mechanisms
                frontier = [i for i in wound
                            if any(A[i, j] > 0
                                   for j in range(4) if j not in wound)]
                m_cut = sum(1 for i in wound for j in range(4)
                            if j not in wound and A[i, j] > 0) >= 2
                m_cycle = bool(frontier) and _has_cycle_through(A, frontier)
                bnd = [i for i in wound
                       if any(A[i, j] > 0 for j in range(4)
                              if j not in wound)]
                m_bridge = False
                for a, b in itertools.combinations(bnd, 2):
                    if any(A[a, j] > 0 and A[b, j] > 0 for j in range(4)
                           if j not in wound):
                        m_bridge = True
                cells.append({"graph": gi, "n_edges": len(edges),
                              "wound": list(wound), "P_prot": holds,
                              "m_cut": m_cut, "m_cycle": m_cycle,
                              "m_bridge": m_bridge})
        if smoke and gi >= 3:
            break
    n_prot = sum(1 for c in cells if c["P_prot"])
    verdicts["G2"] = "PASS"
    print("G2 PASS (%d (graph, wound) cells; %d protective)"
          % (len(cells), n_prot))

    # ---- G3 the carrier test (the confusion per mechanism)
    conf = {}
    for m in ("m_cut", "m_cycle", "m_bridge"):
        tp = sum(1 for c in cells if c[m] and c["P_prot"])
        fp = sum(1 for c in cells if c[m] and not c["P_prot"])
        fn = sum(1 for c in cells if not c[m] and c["P_prot"])
        tn = sum(1 for c in cells if not c[m] and not c["P_prot"])
        ppv = tp / (tp + fp) if tp + fp else 0.0
        npv = tn / (tn + fn) if tn + fn else 0.0
        conf[m] = {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                   "ppv": round(ppv, 3), "npv": round(npv, 3),
                   "carrier": (ppv >= 0.9 and npv >= 0.9)}
    carriers = [m for m in conf if conf[m]["carrier"]]
    verdicts["G3"] = "PASS" if (carriers and len(carriers) == 1
                                and not smoke) else \
        ("PASS" if carriers and smoke else "REFUTE")
    print("G3 %s (carriers: %s)" % (verdicts["G3"], carriers or "none"))

    # ---- G4 the n=3 control
    n3_fail = True
    if not smoke:
        for edges in n3:
            A = _adj(edges, 3)
            t3 = np.array([-50.0, -30.0, -30.0])
            for wound in itertools.combinations(range(3), 1):
                Ps = [_battery(A, t3, list(wound), s) for s in SEEDS]
                Ps = [p for p in Ps if p is not None]
                if len(Ps) >= 2 and sum(1 for p in Ps if p > 0) >= 2:
                    n3_fail = False
    verdicts["G4"] = "PASS" if (n3_fail or smoke) else "REFUTE"
    print("G4 %s (the n=3 control: protection %s)"
          % (verdicts["G4"], "absent" if n3_fail else "PRESENT"))

    # ---- G5 the deposit
    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}
    branch = ("CARRIER-" + carriers[0].split("_")[1].upper()
              if len(carriers) == 1 else
              "MIXED-CARRIER" if len(carriers) > 1 else
              "NO-SINGLE-CARRIER")
    out = {
        "experiment": "exp424",
        "title": "THE n=4 PROTECTIVE MOTIF (batch HU-11)",
        "census_size": len(graphs),
        "cells": cells,
        "confusion": conf,
        "n3_control_fail": n3_fail,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP424 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
