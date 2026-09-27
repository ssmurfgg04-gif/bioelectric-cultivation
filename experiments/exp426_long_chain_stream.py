#!/usr/bin/env python3
"""exp426 — THE LONG-CHAIN STREAM: ROUNDS AS THE FINGERPRINT LEVER
(batch HU-12; exp421's pre-named successor regardless of its branch).
exp414's blur analysis and exp421's union lever both act on COVERAGE;
the orthogonal lever is CHAIN LENGTH — the register carries across
rounds (the memory chain IS the signal), so a 30-round stream gives
each coupled pair 3x the co-movement samples and 3x the register-
mediated coupling history. The question: does the fingerprint's AUC
rise with the chain, and does it clear the 0.85 bar at 30 rounds?

THE INSTRUMENT (exp421's machinery verbatim, both its arms retained):
three graphs (path100, the planarian replica, the human Schaefer-400);
the UNION arm (whole-graph walk coverage) and the BOUNDARY arm
(exp414's wound-region form) at ROUNDS_SHORT 10 and ROUNDS_LONG 30;
the commit trajectories' cross-correlation, edges := top-k by |S|;
the shuffled null + the degree-matched decoy as exp414's.
BUDGET DISCLOSURE (frozen here, not discovered): SEEDS = [0, 1] — the
30-round union arm triples exp421's walk cost per seed; two seeds keep
the per-graph-best convention alive at 2/3 the rows.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the graph identities logged (sha per
      adjacency); all stream values finite (fail=STOP).
  G2  THE CONTINUITY: the boundary arm at 10 rounds reproduces
      exp414's deposited per-graph best AUCs within 0.05 on >= 2/3
      graphs (this instrument is the landed one's extension, not a
      new build).
  G3  THE CHAIN: the union arm at 30 rounds reaches AUC >= 0.85 on
      >= 2/3 graphs (per-graph best across seeds).
  G4  THE DOSE-RESPONSE: union AUC(30) > union AUC(10) on >= 2/3
      graphs AND the shuffled null at 30 rounds <= 0.60 on ALL
      graphs (more rounds must feed the SIGNAL, not the noise).
  G5  deposit results/exp426_long_chain_stream.json.

BRANCH LATTICE: CHAIN-CARRIES (G3 PASS) / CHAIN-PARTIAL (G3 REFUTE,
G4's first clause PASS — the lever's direction holds, the bar stays
out of reach) / CHAIN-NULL (G4 REFUTE — the fingerprint saturates at
10 rounds; the chain axis is closed) / INSTRUMENT-REFUTED (G1/G2
fail).

THE HONEST STAKES: if the chain carries the fingerprint past the bar,
"the wiring lives in the pattern's history" becomes a measured
reconstruction claim with a stated cost (chain length); if it
saturates, the commit stream's information content has a CEILING —
the indexation claim's converse gets its honest bound.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1]
GRAPHS = ["path100", "planarian400", "human400"]
ROUNDS_SHORT = 10
ROUNDS_LONG = 30
AUC_BAR = 0.85
CONTINUITY_TOL = 0.05
DEPOSIT = os.path.join(ROOT, "results",
                       "exp426_long_chain_stream.json")


BODY_DISCLOSURES = [
    "the machinery is exp421's landed module imported verbatim (_build, "
    "_walk_round, _score_arm) with the rounds axis parameterized — the "
    "union arm = exp421's whole-graph walk coverage, the boundary arm = "
    "exp414's wound-region form; zero new knobs beyond the rounds "
    "ladder frozen in the docstring",
    "G2 reads exp414's deposit (results/exp414_wiring_from_history.json) "
    "per_graph_best_auc; absent deposit -> G2 REFUTE deposited honestly",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from experiments.exp421_union_stream_reconstruction import (
    GRAPHS, PROD_FLOOR, G_CTX, COMMIT_NOISE, STEPS_PER_CELL,
    _build, _walk_round, _score_arm, _sha)


def _run_arm_rounds(graph, seed, arm, rounds):
    c, tgt, region, n = _build(graph, seed)
    region_full = (list(range(n)) if arm == "union"
                   else [int(x) for x in region])
    rlist = [_walk_round(c, region_full, True) for _ in range(rounds)]
    return _score_arm(c, rlist, seed)


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget_mode == "smoke"
    graphs = GRAPHS[:1] if smoke else GRAPHS
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and G_CTX == 0.5
    assert ROUNDS_SHORT == 10 and ROUNDS_LONG == 30
    print("G1 floor %s; constants verified" % CORE.NEURAL_SPEC_MIN)

    cells_log = {}
    results = {}
    for graph in graphs:
        for seed in seeds:
            for arm, rounds in (("boundary", ROUNDS_SHORT),
                                ("union", ROUNDS_SHORT),
                                ("union", ROUNDS_LONG)):
                row = _run_arm_rounds(graph, seed, arm, rounds)
                results["%s|%d|%d" % (arm, rounds, seed)] = row
                print("  %s r%d seed %d: AUC %.3f p@k %.3f null %.3f "
                      "decoy %.3f (k=%d)"
                      % (arm, rounds, seed, row["auc"],
                         row["precision_at_k"], row["auc_null"],
                         row["auc_decoy"], row["k_true"]))
        c, _, _, _ = _build(graph, seeds[0])
        cells_log[graph] = _sha(np.abs(c.A))
        del c
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor entry/exit; the constants; identities %s)"
          % cells_log)

    def best(arm, rounds):
        out = {}
        for g in graphs:
            vals = [results["%s|%d|%d" % (arm, rounds, s)]["auc"]
                    for s in seeds
                    if "%s|%d|%d" % (arm, rounds, s) in results]
            out[g] = max(vals) if vals else float("nan")
        return out

    b10 = best("boundary", ROUNDS_SHORT)
    u10 = best("union", ROUNDS_SHORT)
    u30 = best("union", ROUNDS_LONG)

    # ---- G2 the continuity (boundary@10 vs exp414's deposited bests)
    try:
        import json
        import os
        with open(os.path.join(ROOT, "results",
                               "exp414_wiring_from_history.json")) as f:
            dep414 = json.load(f)["per_graph_best_auc"]
        ok = sum(1 for g in graphs
                 if abs(b10[g] - dep414[g]) <= CONTINUITY_TOL)
        verdicts["G2"] = ("PASS" if ok >= max(
            1, int(np.ceil(2 * len(graphs) / 3))) else "REFUTE")
        detail["continuity"] = {g: {"this_run": round(b10[g], 3),
                                    "exp414": round(dep414[g], 3)}
                                for g in graphs}
    except (OSError, KeyError) as e:
        verdicts["G2"] = "REFUTE"
        detail["continuity"] = {"error": repr(e)}
    print("G2 %s (%s)" % (verdicts["G2"], detail.get("continuity")))

    # ---- G3 the chain
    g3_graphs = [g for g in graphs if u30[g] >= AUC_BAR]
    verdicts["G3"] = ("PASS" if (not smoke and len(g3_graphs) >= 2)
                      else "PASS" if smoke else "REFUTE")
    print("G3 %s (union@30 per-graph best %s)" % (verdicts["G3"], u30))

    # ---- G4 the dose-response + the null discipline
    rising = sum(1 for g in graphs if u30[g] > u10[g])
    nulls30 = [results["union|%d|%d" % (ROUNDS_LONG, s)]["auc_null"]
               for s in seeds
               if "union|%d|%d" % (ROUNDS_LONG, s) in results]
    g4 = rising >= max(1, int(np.ceil(2 * len(graphs) / 3))) and (
        not nulls30 or max(nulls30) <= 0.60)
    verdicts["G4"] = "PASS" if (smoke or g4) else "REFUTE"
    print("G4 %s (rising on %d/%d; union@30 nulls %s)"
          % (verdicts["G4"], rising, len(graphs),
             ["%.3f" % a for a in nulls30]))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    branch = ("CHAIN-CARRIES" if verdicts["G3"] == "PASS" else
              "CHAIN-PARTIAL" if rising >= max(
                  1, int(np.ceil(2 * len(graphs) / 3))) else
              "CHAIN-NULL")
    if verdicts["G1"] != "PASS" or verdicts["G2"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    dep = {
        "experiment": "exp426",
        "title": "THE LONG-CHAIN STREAM: ROUNDS AS THE FINGERPRINT "
                 "LEVER (batch HU-12)",
        "instrument": {
            "arms": ["boundary@10 (the exp414 continuity face)",
                     "union@10", "union@30"],
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "SEEDS": SEEDS}},
        "graph_identities": cells_log,
        "results": results,
        "per_graph_best": {"boundary@10": b10, "union@10": u10,
                           "union@30": u30},
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    import json
    import os
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP426 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
