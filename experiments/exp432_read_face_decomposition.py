#!/usr/bin/env python3
"""exp432 — THE ENTANGLED REGISTER'S READ FACE (batch HU-13;
exp425's registered follow-up). exp425 landed DUALITY-ENTANGLED: the
dose correlations (rho_correct ~ -0.53, rho_stress ~ +0.58) are
INVARIANT across merged/split/stress_only/correct_only write
schedules — the register's channels are entangled at the READ, not
the write. THE OPEN QUESTION: WHICH CELLS' READS carry which
correlation? The blend reads at wound-facing boundary cells (exp425's
channel operationalization); the read face is the untested axis.

HYPOTHESIS: the read face, not the write schedule, is where the
entanglement lives — restricting the read to interior cells vs
boundary cells vs the union changes the correlations' magnitudes
(even if their signs survive, the exp425 lesson pre-named).

THE INSTRUMENT (exp425's landed form verbatim; the READ face as the
new axis): merged write schedule only (the calibration path), the
read restricted pre-named to three faces — BOUNDARY (exp425's own),
INTERIOR, UNION (every cell); the (pin x mult) crossing x hosts[:2]
x 3 seeds; R = the rescue read per face; rho per dose axis per face.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0 at entry/exit; constants asserted
      (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, G_CTX 0.5); the merged
      arm at the BOUNDARY face replicates exp425's deposited merged
      rho within 1e-3 (fail=STOP).
  G2  the discipline: the read face is fixed per arm BEFORE the
      walks; no face-dependent rng path; the register-OFF twins
      cached per (host, seed, pin, mult).
  G3  THE DECOMPOSITION: the read face changes either correlation's
      magnitude by >= 0.1 on >= 1 face (READ-FACE-CARRIES) or it
      does not (READ-INVARIANT — the entanglement survives every
      read face too; the register's pluralism is total at n<=400).
  G4  the anatomy: the full (face x axis x host) rho table deposited
      + the per-face R tables.
  G5  deposit results/exp432_read_face_decomposition.json.

BRANCH LATTICE: READ-FACE-CARRIES / READ-INVARIANT /
INSTRUMENT-REFUTED (G1 fail).
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration (re-asserted from exp425's landed constants)
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
STRESS_LADDER = [-60.0, -45.0, -40.0, -35.0]
CORRECTION_LADDER = [0.5, 1.0, 2.0]
SEEDS = [0, 1, 2]
N_HOSTS = 4
ANCHOR_TOL = 1e-3     # G1's exp425 replication bar
FACE_TOL = 0.1        # G3's read-face-carries bar
DEPOSIT = os.path.join(ROOT, "results",
                       "exp432_read_face_decomposition.json")
EXP425_DEPOSIT = os.path.join(ROOT, "results",
                              "exp425_register_channel_split.json")

BODY_DISCLOSURES = [
    "exp425's deposit (results/exp425_register_channel_split.json, runner "
    "artifact hu12-exp425 / run 36308174641 at fec154a, ledger L326) was "
    "ABSENT from the local workspace at body time; regenerated BEFORE this "
    "run by executing exp425's own landed module locally (the machinery "
    "files unchanged since the runner's base commit; deterministic hosts/"
    "seeds/ladders) and cross-checked against ledger L326's recorded "
    "merged medians (rho_correct ~ -0.53, rho_stress ~ +0.58, verdict "
    "DUALITY-ENTANGLED) before serving as G1's anchor; disclosed, not "
    "silent",
    "the face operationalization: the write schedule is exp425's MERGED "
    "arm bit-path in EVERY face (every commit writes the single "
    "phi_history; the blend applies at the cls-0 boundary commits only, "
    "the landed coupling); the READ FACE selects the blend's history "
    "source — BOUNDARY reads the committing cell's own register value "
    "(exp425's merged per-cell canonical form, the bit-identical path the "
    "G1 anchor rides on), INTERIOR reads the walk-level aggregate mean "
    "over the interior-class cells (cls 1), UNION reads the walk-level "
    "aggregate mean over every region cell (the walk-level aggregate is "
    "exp425's own channel-read form, its landed precedent); the face "
    "changes ONLY the blended source value — zero face-dependent "
    "branching in the walk",
    "G2's no-face-dependent-rng-path clause is verified operationally: "
    "the walk's rng draw count is face-independent by construction (the "
    "face enters one committed value; the blend consumes zero draws; "
    "every commit draws exactly one normal either way), so the "
    "collective's rng STATE after a cell must be bit-identical across "
    "all four cells of a key (three faces + the register-OFF twin) — "
    "asserted per key",
    "G1's fail=STOP reading: the floor/constants anchors are hard "
    "asserts (STOP); the exp425 replication clause is evaluated exactly "
    "once and a failure lands the pre-named INSTRUMENT-REFUTED branch "
    "with the anatomy still deposited (G4/G5 deposit beside the branch, "
    "exp425's G4 convention) — no silent continue-as-PASS; a G2 "
    "discipline failure (a face-dependent rng path) is likewise "
    "instrument breakage and lands INSTRUMENT-REFUTED (disclosed "
    "extension of the lattice's G1 clause)",
    "the smoke budget (1 host x 1 seed) skips the exp425 rho-anchor "
    "clause (budget mismatch vs the deposited full crossing) but "
    "bit-checks the boundary-face R table against exp425's deposited "
    "merged rows on the overlapping (host 0, seed 0) keys at 1e-4 (the "
    "deposit's own rounding) — hard assert",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from experiments.exp425_register_channel_split import (
    DT_FALLBACK, G_CTX, COMMIT_NOISE, PROD_FLOOR, STEPS_PER_CELL,
    STRESS_LADDER, CORRECTION_LADDER, SEEDS, N_HOSTS, WIND_V, INTEN,
    ROUNDS_SPLIT, CROSSING_HOSTS, _build, _region, _spearman)

FACES = ("boundary", "interior", "union")   # the pre-named read faces,
#                                             frozen before any walk


def _commit_pass(c, region, face, g_ctx, pin, steps_mult):
    """exp425's landed BFS boundary-inward commit pass verbatim (the
    cls split, the parent/frontier seeding, the pin handling, the
    commit loop, the blend at the boundary cells) with the mode
    dispatch replaced by the READ FACE dispatch — the blend's history
    source only; the write schedule is exp425's MERGED arm in every
    face (every commit writes the single phi_history). The H_S/H_C
    side registers are dropped: they are passive copies never read on
    the merged path (value- and rng-neutral, disclosed)."""
    region_set = set(region)
    cls = {}
    for i in region:
        nbrs = [j for j in np.where(c.A[i] > 0)[0] if j not in region_set]
        cls[i] = 0 if nbrs else 1
    parent_of, frontier = {}, []
    wound_center = float(np.mean(c.theta[region]))
    for i in region:
        nbrs = [j for j in np.where(c.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = list(region)[:1]
        parent_of[frontier[0]] = frontier[0]
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    from collections import deque
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    merged = c.phi_history
    i_cells = np.array([i for i in region if cls[i] == 1], dtype=int)
    all_cells = np.array(list(region), dtype=int)
    n_steps = max(1, int(round(STEPS_PER_CELL * steps_mult)))
    stressed = pin > PROD_FLOOR
    if stressed:
        CORE.NEURAL_SPEC_MIN = pin
    try:
        for i, src in order:
            for _ in range(n_steps):
                c.step(DT_FALLBACK)
            if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
            written = theta_new
            if g_ctx > 0.0 and cls[i] == 0:
                if face == "boundary":
                    src_hist = float(merged[i])
                elif face == "interior":
                    src_hist = float(np.mean(merged[i_cells]))
                else:
                    src_hist = float(np.mean(merged[all_cells]))
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * src_hist)
            c.theta[i] = written
            c.V[i] = written
            merged[i] = written
    finally:
        if stressed:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR


def _rng_tag(c):
    st = c.rng.bit_generator.state
    return (int(st["state"]["state"]), int(st["state"]["inc"]))


def _cell(host, seed, face, g_ctx, pin, mult, rounds=None):
    """exp425's _cell verbatim with the face axis; returns (err, the
    post-walk rng-state tag — the G2 no-face-dependent-rng-path
    witness). At g_ctx == 0.0 the blend branch is skipped by
    construction (the face argument is never read; exp425's own
    register-OFF twin caching form)."""
    if rounds is None:
        rounds = ROUNDS_SPLIT
    c, target, _ = _build(host, seed)
    region = _region(target)
    c.theta[region] = WIND_V
    c.V[region] = WIND_V
    for _ in range(rounds):
        _commit_pass(c, region, face, g_ctx, pin, mult)
        c.run(30.0, dt=DT_FALLBACK)
    err = float(c.pattern_error(target))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored in cell"
    return err, _rng_tag(c)


def _exp425_deposit():
    with open(EXP425_DEPOSIT) as f:
        return json.load(f)


def main(budget: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget == "smoke"
    hosts = range(1 if smoke else N_HOSTS)
    seeds = SEEDS[:1] if smoke else SEEDS

    # ---- G1 the anchors (entry)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and G_CTX == 0.5
    assert WIND_V == -30.0
    assert STRESS_LADDER == [-60.0, -45.0, -40.0, -35.0]
    assert CORRECTION_LADDER == [0.5, 1.0, 2.0]
    assert FACES == ("boundary", "interior", "union")
    print("G1 anchors asserted at entry (floor %s, the ladders as "
          "written%s)" % (CORE.NEURAL_SPEC_MIN, ", SMOKE" if smoke else ""))

    # ---- G2 the arm plan: the read face fixed per arm BEFORE the walks
    hosts_cross = list(hosts)[:CROSSING_HOSTS]
    plan = [(f, h, s, p, m)
            for h in hosts_cross
            for s in seeds
            for p in STRESS_LADDER
            for m in CORRECTION_LADDER
            for f in FACES]
    n_keys = len(hosts_cross) * len(seeds) * len(STRESS_LADDER) \
        * len(CORRECTION_LADDER)
    assert len(plan) == n_keys * len(FACES)
    assert {f for f, *_ in plan} == set(FACES)
    print("G2 plan fixed pre-walk (%d arms = %d keys x 3 faces; the OFF "
          "twins cached per (host, seed, pin, mult))" % (len(plan), n_keys))

    # ---- the crossing: one cached OFF twin per key, three face cells
    R: dict = {}
    tags: dict = {}
    off_cache: dict = {}
    key_tags: dict = {}
    key_counts: dict = {}
    g2_flags: list = []
    for f, h, s, p, m in plan:
        key = (h, s, p, m)
        if key not in off_cache:
            # the twin: g_ctx 0.0 — the blend branch skipped by
            # construction; the face argument never read (exp425's form)
            off_cache[key] = _cell(h, s, "boundary", 0.0, p, m)
            key_tags.setdefault(key, set()).add(off_cache[key][1])
            key_counts[key] = 1
        err, tag = _cell(h, s, f, G_CTX, p, m)
        R[(f, h, s, p, m)] = off_cache[key][0] - err
        tags[(f, h, s, p, m)] = tag
        key_tags.setdefault(key, set()).add(tag)
        key_counts[key] += 1
        if key_counts[key] == len(FACES) + 1:
            # the key is complete: 3 faces + the OFF twin must share ONE
            # rng trajectory (the same draw count -> the same final state)
            g2_flags.append(len(key_tags[key]) == 1)
    assert len(off_cache) == n_keys, "the OFF twin cache missed a key"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
    assert all(np.isfinite(v) for v in R.values())
    g2_ok = bool(g2_flags) and all(g2_flags) and len(g2_flags) == n_keys
    verdicts["G2"] = "PASS" if g2_ok else "REFUTE"
    print("G2 %s (rng-state bit-identity across the 4 cells of each of "
          "%d keys)" % (verdicts["G2"], n_keys))

    # ---- per-face per-host rho (exp425's convention: per-host Spearman
    # over that host's seeds x pins x mults, then the median across hosts)
    rho = {}
    for f in FACES:
        rs, rc = [], []
        for h in hosts_cross:
            rvals = [R[(f, h, s, p, m)]
                     for s in seeds
                     for p in STRESS_LADDER
                     for m in CORRECTION_LADDER]
            pins = [p for _ in seeds for p in STRESS_LADDER
                    for _ in CORRECTION_LADDER]
            mults = [m for _ in seeds for _ in STRESS_LADDER
                     for m in CORRECTION_LADDER]
            rs.append(_spearman([INTEN[p] for p in pins], rvals))
            rc.append(_spearman(mults, rvals))
        rho[f] = {"rho_stress_med": float(np.median(rs)),
                  "rho_correct_med": float(np.median(rc)),
                  "per_host_stress": rs, "per_host_correct": rc}
    detail["rho"] = rho
    for f in FACES:
        print("  %s: rho_stress %.3f rho_correct %.3f"
              % (f, rho[f]["rho_stress_med"], rho[f]["rho_correct_med"]))

    # ---- G1's anchor clause (evaluated exactly once, full budget):
    # the BOUNDARY face is exp425's MERGED arm bit-path, so its rho must
    # replicate exp425's deposited merged medians within 1e-3
    if smoke:
        d425 = _exp425_deposit()
        worst = 0.0
        for (h, s, p, m) in off_cache:
            k = "merged|%d|%d|%s|%s" % (h, s, p, m)
            worst = max(worst, abs(R[("boundary", h, s, p, m)]
                                   - d425["R_table"][k]))
        assert worst <= 1e-4, ("smoke bit-check vs exp425's merged rows "
                               "failed: %g" % worst)
        verdicts["G1"] = "PASS"
        print("G1 PASS (SMOKE: boundary-face R bit-checks exp425's merged "
              "rows on host 0 seed 0, worst %.2e)" % worst)
    else:
        try:
            d425 = _exp425_deposit()
            m425 = d425["rho"]["merged"]
            d_stress = abs(rho["boundary"]["rho_stress_med"]
                           - m425["rho_stress_med"])
            d_correct = abs(rho["boundary"]["rho_correct_med"]
                            - m425["rho_correct_med"])
            ok = d_stress <= ANCHOR_TOL and d_correct <= ANCHOR_TOL
            r_worst = max(abs(R[("boundary", h, s, p, m)]
                              - d425["R_table"]["merged|%d|%d|%s|%s"
                                                % (h, s, p, m)])
                          for (h, s, p, m) in off_cache)
            verdicts["G1"] = "PASS" if ok else "REFUTE"
            detail["exp425_anchor"] = {
                "exp425_merged": {"rho_stress_med": m425["rho_stress_med"],
                                  "rho_correct_med":
                                      m425["rho_correct_med"]},
                "boundary_face": {
                    "rho_stress_med": rho["boundary"]["rho_stress_med"],
                    "rho_correct_med":
                        rho["boundary"]["rho_correct_med"]},
                "delta_stress": round(d_stress, 6),
                "delta_correct": round(d_correct, 6),
                "tol": ANCHOR_TOL,
                "r_table_max_delta": round(float(r_worst), 6)}
            print("G1 %s (anchor deltas: stress %.2e correct %.2e, tol "
                  "%.0e; R-table worst %.2e)"
                  % (verdicts["G1"], d_stress, d_correct, ANCHOR_TOL,
                     r_worst))
        except (OSError, KeyError) as e:
            verdicts["G1"] = "REFUTE"
            detail["exp425_anchor"] = {"error": repr(e)}
            print("G1 REFUTE (exp425's deposit unreadable: %r)" % e)

    # ---- G3 the decomposition (evaluated exactly once)
    deltas = {}
    carry = False
    for f in ("interior", "union"):
        for ax in ("rho_stress_med", "rho_correct_med"):
            d = abs(abs(rho[f][ax]) - abs(rho["boundary"][ax]))
            deltas["%s|%s" % (f, ax)] = round(d, 4)
            if d >= FACE_TOL:
                carry = True
    verdicts["G3"] = "PASS" if carry else "REFUTE"
    print("G3 %s (magnitude deltas vs BOUNDARY: %s; bar %.2f)"
          % (verdicts["G3"], deltas, FACE_TOL))

    # ---- the branch
    branch = ("READ-FACE-CARRIES" if verdicts["G3"] == "PASS"
              else "READ-INVARIANT")
    if verdicts["G1"] != "PASS" or verdicts["G2"] != "PASS":
        branch = "INSTRUMENT-REFUTED"

    # ---- G4 the anatomy: the (face x axis x host) rho table + the
    # per-face R tables ride in the deposit (rho above + R_table below)

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    dep = {
        "experiment": "exp432",
        "title": "THE ENTANGLED REGISTER'S READ FACE (batch HU-13)",
        "instrument": {
            "faces": list(FACES),
            "face_definitions": {
                "boundary": "the blend reads the committing boundary "
                            "cell's own register value (exp425's MERGED "
                            "per-cell canonical form, the bit-identical "
                            "path)",
                "interior": "the blend reads the walk-level aggregate "
                            "mean of the register over the interior-class "
                            "cells (cls 1)",
                "union": "the blend reads the walk-level aggregate mean "
                         "of the register over every region cell"},
            "write_schedule": "exp425's MERGED arm bit-path in every "
                              "face (the calibration path; every commit "
                              "writes the single phi_history)",
            "rounds_per_arm": ROUNDS_SPLIT,
            "crossing_hosts": CROSSING_HOSTS,
            "crossing": {"pins": STRESS_LADDER,
                         "mults": CORRECTION_LADDER},
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "hosts": N_HOSTS, "seeds": SEEDS},
            "exp425_deposit": "results/exp425_register_channel_split.json "
                              "(regenerated locally from exp425's landed "
                              "module; ledger L326 cross-check; "
                              "disclosed)"},
        "R_table": {"%s|%d|%d|%s|%s" % k: round(v, 4)
                    for k, v in R.items()},
        "rho": rho,
        "g3_magnitude_deltas": deltas,
        "exp425_anchor": detail.get("exp425_anchor"),
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
    print("EXP432 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget="smoke" if "--smoke" in _argv else "full")
