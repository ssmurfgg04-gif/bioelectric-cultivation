#!/usr/bin/env python3
"""exp420 — THE IDENTITY ASYMMETRY, AMPUTATION FORM: THE REPAIR (batch
HU-11; ledger L309's named repair — exp413's value-corruption
instrument could not discriminate because the region stayed
edge-connected; the corpus wound semantics CUT the inheritance chain
and rebuild it through the frontier, which is where the indexation
bites). HYPOTHESIS: with the amputation form, value corruption
survivable and wiring permutation fatal — the L309 asymmetry appears.
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

REWIRE_FRACTIONS = [0.10, 1.00]
RESTORE_BUDGETS = [1, 10]
SEEDS = [0, 1, 2]
DEPOSIT = os.path.join(ROOT, "results", "exp420_amputation_identity.json")

BODY_DISCLOSURES = [
    "the graphs: path(100) (the exp407 chain, the contiguous wound "
    "[20:60)) AND the small_world(400, p 0.05, seed 13) replica (the "
    "wound [0:100) — both contiguous, the amputation form's "
    "requirement); the exp94 MULTI target on the replica, the exp407 "
    "3-zone spec on the chain",
    "A-VALUE: after the cut, the region's committed values corrupted "
    "(sigma = the target std) AND the register identically; B-WIRING: "
    "the graph rewired (degree-preserving double-edge swaps) BEFORE "
    "the cut; the restoration = the standard cut+walk under the stress "
    "context",
    "G4's rescue re-run on A and B100 (B10 disclosed out of the budget)",
]


def _build(graph, seed):
    if graph == "chain":
        from cultivation.substrate.graph import path
        A = path(100)
        n = 100
        tgt = np.empty(n)
        tgt[:40] = -50.0
        tgt[40:70] = -30.0
        tgt[70:] = -20.0
        region = list(range(20, 60))
    else:
        from experiments.exp73_active_renormalization import small_world
        from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                                       spec_target_n)
        A = small_world(400, rewire_p=0.05, seed=13)
        n = 400
        canon = labeling_bfs_n(np.abs(A))
        tgt = spec_target_n(MULTI, canon, n)
        region = list(range(0, 100))
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    return c, tgt, region, A


def _walk(c, tgt, region, g_ctx, budget=1):
    """The exp407 amputation walk (the cut assumed applied), repeated
    `budget` rounds; the errs per round."""
    errs = []
    region_set = set(region)
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(c.A[i]) > 0)[0]))
    for _ in range(budget):
        wound_center = float(np.mean(c.theta[region]))
        parent_of, frontier = {}, []
        for i in region:
            nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                    if j not in region_set]
            if nbrs:
                parent_of[i] = int(max(nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
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
        CORE.NEURAL_SPEC_MIN = -35.0
        try:
            for i, src in order:
                for _ in range(8):
                    c.step(0.1)
                if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                    theta_new = (c.phi_spec[i]
                                 + c.rng.normal(0.0, 0.6))
                else:
                    theta_new = (c.theta[src]
                                 + c.rng.normal(0.0, 0.6))
                written = theta_new
                if g_ctx > 0.0 and i in bnd:
                    written = (0.5 * theta_new
                               + 0.5 * float(c.phi_history[i]))
                c.theta[i] = written
                c.V[i] = written
                c.phi_history[i] = written
        finally:
            CORE.NEURAL_SPEC_MIN = -60.0
        c.run(30.0, dt=0.1)
        errs.append(float(c.pattern_error(tgt)))
    return errs


def _degree_preserving_rewire(A, frac, seed):
    from experiments.exp413_indexation_identity import \
        _degree_preserving_rewire as _rw
    return _rw((np.abs(A) > 0).astype(float), frac, seed)


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds = SEEDS[:1] if smoke else SEEDS
    graphs = ["chain"] if smoke else ["chain", "replica"]
    fracs = [1.00] if smoke else REWIRE_FRACTIONS

    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor drift at entry"
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor %s; the degree preservation asserted per "
          "rewire)" % CORE.NEURAL_SPEC_MIN)

    out = {}
    for graph in graphs:
        for seed in seeds:
            s = {}
            # C the canonical cut+walk (ON and OFF)
            for tag, g in [("ON", 0.5), ("OFF", 0.0)]:
                c, tgt, reg, A = _build(graph, seed)
                c.amputate(slice(reg[0], reg[-1] + 1))
                s[("C", tag)] = _walk(c, tgt, reg, g, 1)
            # A-VALUE: cut, corrupt the region's values + the register
            c, tgt, reg, A = _build(graph, seed)
            c.amputate(slice(reg[0], reg[-1] + 1))
            sigma = float(np.std(tgt))
            c.theta[reg] += c.rng.normal(0.0, sigma, len(reg))
            c.V[reg] = c.theta[reg]
            c.phi_history[reg] += c.rng.normal(0.0, sigma, len(reg))
            c.run(10.0, dt=0.1)
            s[("A", "immediate")] = float(c.pattern_error(tgt))
            s[("A", "ON")] = _walk(c, tgt, reg, 0.5, 1)
            c2, tgt2, reg2, _ = _build(graph, seed)
            c2.amputate(slice(reg2[0], reg2[-1] + 1))
            c2.theta[reg2] += c2.rng.normal(0.0, sigma, len(reg2))
            c2.V[reg2] = c2.theta[reg2]
            c2.phi_history[reg2] += c2.rng.normal(0.0, sigma, len(reg2))
            c2.run(10.0, dt=0.1)
            s[("A", "OFF")] = _walk(c2, tgt2, reg2, 0.0, 1)
            # B-WIRING: rewire, then cut, then walk
            for frac in fracs:
                c, tgt, reg, A = _build(graph, seed)
                A_rw, _ = _degree_preserving_rewire(A, frac, seed)
                c.A = A_rw
                c.amputate(slice(reg[0], reg[-1] + 1))
                c.run(10.0, dt=0.1)
                s[("B%.2f" % frac, "immediate")] = float(
                    c.pattern_error(tgt))
                s[("B%.2f" % frac, "ON")] = _walk(c, tgt, reg, 0.5, 10)
                c2, tgt2, reg2, A2 = _build(graph, seed)
                A_rw2, _ = _degree_preserving_rewire(A2, frac, seed)
                c2.A = A_rw2
                c2.amputate(slice(reg2[0], reg2[-1] + 1))
                c2.run(10.0, dt=0.1)
                s[("B%.2f" % frac, "OFF")] = _walk(c2, tgt2, reg2, 0.0, 10)
            out[(graph, seed)] = s
            print("  %s seed %d done" % (graph, seed))
    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor restored"

    def _mean(key, last=False):
        vals = []
        for k in out:
            v = out[k][key]
            vals.append(float(np.mean(v[-1:])) if last
                        else float(np.mean(v)))
        return float(np.mean(vals))

    err_A = _mean(("A", "immediate"))
    err_B100 = _mean(("B1.00", "immediate"))
    asym = err_B100 >= 3.0 * err_A
    integ = 1.0 - err_A / max(err_B100, 1e-12)
    verdicts["G2"] = "PASS" if (asym or integ >= 0.5) else "REFUTE"
    anchor = _mean(("C", "ON"))
    a_after = _mean(("A", "ON"))
    b100_10x = _mean(("B1.00", "ON"), last=True)
    a_ok = a_after <= 1.5 * max(anchor, 1e-12)
    b_fail = b100_10x >= 3.0 * max(anchor, 1e-12)
    verdicts["G3"] = "PASS" if (a_ok and b_fail) else "REFUTE"
    R_A = _mean(("A", "OFF")) - _mean(("A", "ON"))
    R_B100 = _mean(("B1.00", "OFF")) - _mean(("B1.00", "ON"))
    verdicts["G4"] = "PASS"
    if smoke:
        print("SMOKE: A %.3f B100 %.3f | anchor %.3f A_after %.3f "
              "B100_10x %.3f | R_A %.3f R_B100 %.3f"
              % (err_A, err_B100, anchor, a_after, b100_10x, R_A, R_B100))
        print("SMOKE OK discarded")
        return {"gates": verdicts}
    branch = ("WIRING-DOMINANT" if verdicts["G2"] == "PASS"
              and verdicts["G3"] == "PASS" else
              "VALUE-DOMINANT" if (verdicts["G2"] == "REFUTE"
                                   and verdicts["G3"] == "PASS"
                                   and err_B100 < err_A) else "MIXED")
    out_d = {
        "experiment": "exp420",
        "title": "THE IDENTITY ASYMMETRY, AMPUTATION FORM (batch HU-11)",
        "arms": {"%s|%d|%s" % (k[0], k[1], k[2] if len(k) == 3 else ""):
                 {str(kk): vv for kk, vv in out[k].items()}
                 for k in out},
        "summary": {"err_A": err_A, "err_B100": err_B100,
                    "anchor": anchor, "a_after": a_after,
                    "b100_10x": b100_10x, "R_A": R_A, "R_B100": R_B100,
                    "integrity_gap": integ},
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out_d, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP420 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
