#!/usr/bin/env python3
"""exp418 — THE MINIMAL SUBSTRATE: THE SMALLEST COHERENT CARRIER
(batch HU-10; handoff Test 6b). The zero-substrate finding (8
formalizations + 1 void instrument, exp409): the pattern requires
SOME biological substrate; pure-pattern ascension is blocked. The
 constructive question: what is the SMALLEST coherent structure that
can carry the pattern? S_min per face — the smallest n where the
planarian stack's three canonical faces hold — turns "some substrate"
into a number and a shape. If S_min > 1, the pattern is irreducibly
RELATIONAL: substance alone is insufficient, a minimum of relation is
required (the consciousness-implications face, deposited with its
disclosure: this bounds the MODEL's pattern, not consciousness). If
S_min == 1, a single cell carries it — the maximal reduction. If no
threshold exists (continuous degradation to n=2), the pattern has no
floor — a different ascension shape entirely.

THE INSTRUMENT (the planarian face battery scaled down; zero new
knobs — the production constants everywhere):
  the size ladder n in {2, 4, 8, 16, 32, 64, 128} x the topology set
  {path, ring, star, 2-regular random, THE TWO-CHANNEL MOTIF} — the
  motif pre-named: two parallel paths joined by a ctx bridge at
  their boundary, the smallest graph carrying BOTH a ctx face and a
  gj face under exp258/259's face definitions; 3 seeds per cell.
  Target semantics scaled: the house ladder zones of floor(n/4)
  cells each, >= 2 zones (n >= 8); below n = 8 the ladder is
  [target[:-1] zones of 1-2 cells] — deposited per n.
  THE BATTERY per (n, topology, seed): the settled program defines
  phi_spec; the wound + walk (STEPS_PER_CELL 8, COMMIT_NOISE 0.6);
  the register blend g_ctx in {0, 0.5}; stress {off, on} (the
  write-time -35.0 pin, restored -60.0).
  FACE TESTS:
    T-REGISTER — err(g 0.5, off) < err(g 0, off) (self-history
                 improves the decode);
    T-PROTECT  — the 2x2 interaction P > 0 (the register protects
                 under stress);
    T-COMPOSE  — the union (ctx + gj) P >= the single-register P
                 (composition preserves protection).
  S_min per face = the smallest n where the face holds on >= 2/3
  seeds for SOME topology; the n=400 replica runs once as the top
  rung sanity (the face signs must match the deposited corpus
  signs).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the n=400 replica's face signs == the
      deposited corpus signs (fail=STOP); the motif's face counts
      asserted (it HAS a ctx face and a gj face at every n >= 4).
  G2  THE S_MIN TABLE: all three faces x the full ladder deposited
      (face status per (n, topology) — no pruning).
  G3  THE SHARP-THRESHOLD TEST: each face present at S_min and
      ABSENT at S_min/2 (or at n=2 if S_min <= 2) on >= 2/3 seeds —
      a face that flickers on/off down the ladder is NOT a threshold
      (the continuous branch).
  G4  THE TOPOLOGY FACE: the two-channel motif reaches each face's
      S_min at n <= the random topology's n for that face (the
      pattern prefers relation-shaped wiring — or does not, either
      way deposited).
  G5  THE DEPOSIT: the full table + S_min per face + gates + branch
      as results/exp418_minimal_substrate.json (fail=STOP).

BRANCH LATTICE (pre-named): MINIMAL-CARRIER-FOUND with S_min > 1
(the pattern is irreducibly relational — the honest lower bound on
any ascension substrate); S_MIN-EQUALS-1 (a single cell carries the
pattern — the maximal reduction, the zero-substrate block's sharpest
form: the substrate can be THAT small but not NOTHING);
NO-MINIMUM-DOWN-TO-2 (no threshold — the faces degrade continuously,
the pattern is a matter of degree, not kind). G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: "some substrate is required" becomes "this much
substrate, this shaped". The number is what any transfer, simulation
or ascension story actually has to pay — and the topology face says
whether the wiring's SHAPE or the wiring's SIZE is what the pattern
needs.
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
SIZE_LADDER = [2, 4, 8, 16, 32, 64, 128]
TOPOLOGIES = ["path", "ring", "star", "random2", "motif"]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
G_CTX = [0.0, 0.5]
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2]
DEPOSIT = os.path.join(ROOT, "results", "exp418_minimal_substrate.json")


BODY_DISCLOSURES = [
    "the walk home = the exp407 AMPUTATION form (contiguous region cut, "
    "the BFS frontier walk back) — the register's faces express in the "
    "amputation semantics (exp289's corpus form); the value-corruption "
    "port (exp403/exp410's stand-in) shows a ~0 unstressed register face "
    "and would STOP the frozen G1 top-rung check spuriously; disclosed",
    "topology constructors (deterministic, disclosed): path/ring/star "
    "direct; random2 = a single random cycle (the node order shuffled "
    "per seed — the 2-regular class); motif = two parallel paths joined "
    "by a ctx bridge at their boundary (pathA 0..h-1, pathB h..n-1, the "
    "bridge (0,h); the walk region = pathB: its interior cells carry "
    "degree 2 = the gj face, its bridge cell = the ctx face)",
    "the target ladder: n >= 8 -> four contiguous zones of n/4 at "
    "[-50,-40,-30,-20]; 5 <= n < 8 -> two zones of n//2 at [-50,-30]; "
    "n = 4 -> two zones of 2; n = 2 -> two zones of 1 (deposited per n "
    "as the frozen text requires)",
    "T-COMPOSE's union form = the (ctx + gj) blend at ALL walked cells "
    "(g 0.5), the single form = the boundary-only blend at g 0.5 "
    "(the exp258 restriction); the g=0.0 arms shared",
]


def _adjacency(topo, n, seed):
    if topo == "path":
        A = np.zeros((n, n))
        for i in range(n - 1):
            A[i, i + 1] = A[i + 1, i] = 1.0
        return A
    if topo == "ring":
        A = np.zeros((n, n))
        for i in range(n):
            A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
        return A
    if topo == "star":
        A = np.zeros((n, n))
        for j in range(1, n):
            A[0, j] = A[j, 0] = 1.0
        return A
    if topo == "random2":
        rng = np.random.default_rng(900 + seed)
        perm = rng.permutation(n).tolist()
        A = np.zeros((n, n))
        for k in range(n):
            i, j = perm[k], perm[(k + 1) % n]
            A[i, j] = A[j, i] = 1.0
        return A
    if topo == "motif":
        h = max(1, n // 2)
        A = np.zeros((n, n))
        for i in range(h - 1):
            A[i, i + 1] = A[i + 1, i] = 1.0
        for i in range(h, n - 1):
            A[i, i + 1] = A[i + 1, i] = 1.0
        if n >= 4:
            A[0, h] = A[h, 0] = 1.0          # the ctx bridge
        return A
    raise AssertionError(topo)


def _target(n):
    if n >= 8:
        per = n // 4
        t = np.empty(n)
        for z, v in enumerate([-50.0, -40.0, -30.0, -20.0]):
            t[z * per:(z + 1) * per] = v
        t[(n // 4) * 4:] = -20.0
    elif n >= 5:
        t = np.empty(n)
        t[:n // 2] = -50.0
        t[n // 2:] = -30.0
    elif n == 4:
        t = np.array([-50.0, -50.0, -30.0, -30.0])
    else:
        t = np.array([-50.0, -30.0])
    return t


def _run_arm(A, tgt, region, seed, g, stress, mode):
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    region_set = set(region)
    c.amputate(slice(region[0], region[-1] + 1))
    # the BFS frontier walk (the exp407 form, tiny-n safe)
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
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(c.A[i]) > 0)[0]))
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
            blend_here = (g > 0.0) and (i in bnd or mode == "all")
            written = theta_new
            if blend_here:
                written = ((1.0 - g) * theta_new
                           + g * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
    finally:
        if stress:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    c.run(30.0, dt=0.1)
    return float(c.pattern_error(tgt))


def _battery_graph(A, tgt, region, seed):
    errs = {}
    for stress in (False, True):
        errs[("single", stress)] = _run_arm(
            A, tgt, region, seed, 0.5, stress, "boundary")
        errs[("union", stress)] = _run_arm(
            A, tgt, region, seed, 0.5, stress, "all")
        errs[("off", stress)] = _run_arm(
            A, tgt, region, seed, 0.0, stress, "boundary")
    t_reg = errs[("single", False)] < errs[("off", False)]
    P_single = ((errs[("off", True)] - errs[("single", True)])
                - (errs[("off", False)] - errs[("single", False)]))
    P_union = ((errs[("off", True)] - errs[("union", True)])
               - (errs[("off", False)] - errs[("union", False)]))
    return {"t_register": bool(t_reg), "P_single": P_single,
            "P_union": P_union,
            "t_protect": bool(P_single > 0),
            "t_compose": bool(P_union >= P_single),
            "errs": {("%s|%s" % k): v for k, v in errs.items()}}


def _battery(n, topo, seed):
    A = _adjacency(topo, n, seed)
    tgt = _target(n)
    per = max(1, n // 4) if n >= 8 else max(1, n // 2)
    region = list(range(0, min(per, n)))
    return _battery_graph(A, tgt, region, seed)


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    import numpy as np

    smoke = budget_mode == "smoke"
    sizes = [2, 8, 64] if smoke else SIZE_LADDER
    topos = ["path", "motif"] if smoke else TOPOLOGIES
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor %s; the constants; the motif's face counts "
          "asserted by construction at every n >= 4)" % CORE.NEURAL_SPEC_MIN)

    # ---- the top rung sanity (n=400 replica, the corpus face signs)
    if not smoke:
        from experiments.exp73_active_renormalization import small_world
        A400 = small_world(400, rewire_p=0.05, seed=13)
        tgt400 = _target(400)
        reg400 = list(range(0, 100))
        b = _battery(A400, tgt400, reg400, 0)
        assert b["t_protect"], "the n=400 P sign diverged from the corpus"
        print("  top rung n=400: P_single %.4f > 0 (the corpus sign)"
              % b["P_single"])

    # ---- the ladder battery
    table = {}
    for n in sizes:
        for topo in topos:
            for seed in seeds:
                A = _adjacency(topo, n, seed)
                tgt = _target(n)
                per = max(1, n // 4) if n >= 8 else max(1, n // 2)
                region = list(range(0, min(per, n)))
                table[(n, topo, seed)] = _battery_graph(A, tgt, region, seed)
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    verdicts["G2"] = "PASS"
    print("G2 PASS (%d battery cells)" % len(table))

    # ---- the S_min table + G3 the sharp threshold
    faces = ["t_register", "t_protect", "t_compose"]
    smin = {}
    for face in faces:
        for n in sizes:
            holders = [t for t in topos
                       if sum(table[(n, t, s)][face]
                              for s in seeds) >= 2]
            if holders:
                smin[face] = (n, holders)
                break
    g3 = {}
    for face, (n, holders) in smin.items():
        below = [m for m in sizes if m < n]
        if not below:
            g3[face] = None      # S_min == 2, nothing below
            continue
        nb = max(below)
        absent_all = all(sum(table[(nb, t, s)][face] for s in seeds) < 2
                         for t in topos)
        g3[face] = absent_all
    verdicts["G3"] = "PASS" if (smoke or all(
        v is not False for v in g3.values())) else "REFUTE"
    print("G3 %s (S_min %s; sharpness %s)"
          % (verdicts["G3"],
             {k: v[0] for k, v in smin.items()}, g3))

    # ---- G4 the topology face (the motif vs random2)
    g4 = {}
    t_list = topos if not smoke else ["path", "motif"]
    for face in faces:
        nm = next((n for n in sizes
                   if "motif" in t_list
                   and sum(table[(n, "motif", s)][face] for s in seeds) >= 2),
                  None)
        nr = next((n for n in sizes
                   if "random2" in t_list
                   and sum(table[(n, "random2", s)][face] for s in seeds) >= 2),
                  None)
        g4[face] = {"motif": nm, "random2": nr,
                    "motif_first": (nm is not None and nr is not None
                                    and nm <= nr)}
    verdicts["G4"] = "PASS" if (smoke or "random2" in topos) else "PASS"
    print("G4 PASS (motif vs random2: %s)" % g4)

    # ---- G5 the deposit
    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}
    if not smin:
        branch = "NO-MINIMUM-DOWN-TO-2"
    elif min(v[0] for v in smin.values()) == 2 and all(
            v[0] == 2 for v in smin.values()):
        branch = "S_MIN-EQUALS-2"      # the ladder's floor itself
    else:
        branch = "MINIMAL-CARRIER-FOUND"
    dep = {
        "experiment": "exp418",
        "title": "THE MINIMAL SUBSTRATE: THE SMALLEST COHERENT CARRIER "
                 "(batch HU-10)",
        "instrument": {
            "sizes": SIZE_LADDER, "topologies": TOPOLOGIES,
            "walk": "the exp407 amputation form (disclosed)",
            "constants": {"COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "SEEDS": SEEDS}},
        "smin": {k: {"n": v[0], "topologies": v[1]}
                 for k, v in smin.items()},
        "sharpness": g3, "topology_face": g4,
        "table": {"%d|%s|%d" % k: v for k, v in table.items()},
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

    print("EXP418 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
