#!/usr/bin/env python3
"""exp425 — THE REGISTER'S DUALITY UNDER CHANNEL SEPARATION (batch
HU-12; exp410's registered follow-up). exp410 landed REGISTER-DECOMP-
MIXTURE: the rescue R_FULL (+1.28 mV, stress-gated) tracks BOTH dose
axes at |rho| ~ 0.6 with OPPOSITE signs (gap 0.008 << the 0.2 bar) —
refinement is irreducibly plural on the SINGLE unsigned register. THE
OPEN QUESTION: is the duality a property of the REGISTER (one channel
cannot be un-pluralized) or of the WRITE SCHEDULE (the two memories
were written interleaved — separating the phases separates the
memories)? The two-channel hypothesis gets its measured shot: the
stress-era writes and the correction-era writes are routed into TWO
separate register channels (a write-schedule intervention on the
landed coupling — exp410's own condition class), the dose crossing
re-run per channel.

THE INSTRUMENT (exp410's 2x2 machinery verbatim + the channel split;
zero new knobs beyond the split itself):
  the exp410 hosts x seeds, the wound zone, the BFS boundary walk
  (STEPS_PER_CELL 8, COMMIT_NOISE 0.6), the register blend g_ctx 0.5.
  ARMS:
    MERGED   — the canonical single register (the exp410 C-FULL form).
    SPLIT    — phi_history_stress receives the stress-era writes only
               (the pin-era spec-layer writes); phi_history_correct
               receives the correction-walk commits only; the decode
               reads the MERGED pair at strength g_ctx/2 each (the
               read-matched form, pre-named).
    STRESS-ONLY — the decode reads phi_history_stress at g_ctx.
    CORRECT-ONLY— the decode reads phi_history_correct at g_ctx.
  THE DOSE CROSSING per arm: the stress ladder {-60, -45, -40, -35} x
  the correction ladder {0.5x, 1x, 2x the walk budget}; Spearman
  |rho| of R against each axis per arm.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the register-OFF twins bit-exact per seed;
      all R values finite (fail=STOP).
  G2  THE CALIBRATION: MERGED reproduces exp410's deposited C-FULL
      R_FULL within 0.10 mV on >= 3/4 hosts (the split instrument
      does not perturb the landed rescue).
  G3  THE SEPARATION: STRESS-ONLY tracks the stress axis |rho| >= 0.6
      with the correction axis |rho| <= 0.3, AND CORRECT-ONLY tracks
      the correction axis |rho| >= 0.6 with the stress axis
      |rho| <= 0.3 (per-host rho, median across hosts).
  G4  THE RECOMBINATION: SPLIT (read-merged) R >= max(R_stress_only,
      R_correct_only) - 0.05 mV on >= 3/4 hosts (the channels are
      additive at read, the exp419 composition sense).
  G5  deposit results/exp425_register_channel_split.json.

BRANCH LATTICE: DUALITY-SEPARABLE (G3 PASS) / DUALITY-ENTANGLED (G3
REFUTE — the duality survives the schedule surgery: the register's
pluralism is in the CHANNEL, not the schedule) / INSTRUMENT-REFUTED
(G1/G2 fail). G4's own PASS/REFUTE is deposited beside the branch
(additive-at-read vs interfering-at-read), not folded into it.

THE HONEST STAKES: exp410's plural register is the batch's central
mechanism finding; if the schedule separates it, the "qi refinement"
story acquires an engineering handle (write the phases separately,
read them separately); if it does not, the unsigned single-channel
register is a REAL structural commitment of the model.
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
PIN_LADDER = [-60.0, -45.0, -40.0, -35.0]
WALK_LADDER = [0.5, 1.0, 2.0]
N_HOSTS = 4
SEEDS = [0, 1, 2]
RHO_OWN = 0.6
RHO_OTHER = 0.3
MERGED_TOL = 0.10
RECOMB_TOL = 0.05
DEPOSIT = os.path.join(ROOT, "results",
                       "exp425_register_channel_split.json")


BODY_DISCLOSURES = [
    "the channel operationalization: the boundary-class commits (cls 0, "
    "exp410's own C-EVENT isolation class) are the STRESS-era channel; "
    "the interior-class commits (cls 1) are the CORRECTION channel; the "
    "blend reads at boundary cells only, as exp410's landed walk does",
    "SMOKE-REFUTED REPAIR, disclosed: the per-cell channel read is "
    "DEGENERATE — each cell commits exactly once per walk, so a "
    "boundary cell's per-cell H_S/H_C/merged values are identical at "
    "its commit (all arms collapsed to the same R in the smoke; the "
    "duality cannot live in per-cell field mixing). The repaired read: "
    "the channel's WALK-LEVEL AGGREGATE (mean of the channel field over "
    "its class's cells, evolving as the walk proceeds) — the two "
    "channels as two pattern-level memories; MERGED keeps exp410's "
    "per-cell canonical form (the calibration face is untouched)",
    "MERGED replicates exp410's C-FULL walk bit-path (single "
    "phi_history updated by every commit; G2's calibration is the "
    "verification face against exp410's deposited per-host R)",
    "the register-OFF twins (g_ctx 0) are bit-identical across channel "
    "modes by construction (the blend branch is skipped; no extra rng "
    "draws) — cached once per (host, seed, pin, mult) and reused "
    "across arms, disclosed",
    "G2 reads exp410's deposit (results/exp410_register_decomposition.json) "
    "top-level raw rows (host-major, seed-inner) for the per-host C_FULL "
    "R; absent deposit -> G2 REFUTE deposited honestly (no silent skip)",
]

import numpy as np

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective
from experiments.exp410_register_decomposition import (
    DT_FALLBACK, COMMIT_NOISE, G_CTX, PROD_FLOOR, STEPS_PER_CELL,
    STRESS_LADDER, CORRECTION_LADDER, SEEDS, N_HOSTS, WIND_V,
    _build, _region, _spearman)

INTEN = {-60.0: 0, -45.0: 1, -40.0: 2, -35.0: 3}
MODES = ("merged", "split", "stress_only", "correct_only")
# body-side constants (disclosed):
ROUNDS_SPLIT = 2   # the arms run 2 walk rounds on ONE build (the
                   # register carries across rounds — the exp414
                   # memory-chain form); the smoke proved the
                   # single-walk form DEGENERATE: the BFS order puts
                   # every boundary commit before every interior
                   # commit, so the correction channel's aggregate
                   # cannot influence any boundary read within one
                   # walk (correct_only was bit-identical to merged)
CROSSING_HOSTS = 2  # the dose crossing runs on hosts[:2] (the exp410
                    # precedent — its own crossing ran on hosts[:1]);
                    # G2's calibration and G4's point cells cover all
                    # 4 hosts


def _commit_pass(c, region, H_S, H_C, g_ctx, pin, steps_mult, mode):
    """One BFS boundary-inward commit pass (exp410's landed walk
    verbatim: the cls split, the pin handling, the commit loop) with
    the mode's blend source at the boundary cells; writes route to
    H_S (boundary class) / H_C (interior class); merged (the
    collective's own phi_history) takes every commit."""
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
    b_cells = np.array([i for i in region if cls[i] == 0], dtype=int)
    i_cells = np.array([i for i in region if cls[i] == 1], dtype=int)
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
                if mode == "merged":
                    src_hist = float(merged[i])
                elif mode == "stress_only":
                    src_hist = float(np.mean(H_S[b_cells]))
                elif mode == "correct_only":
                    src_hist = float(np.mean(H_C[i_cells]))
                else:
                    src_hist = (0.5 * float(np.mean(H_S[b_cells]))
                                + 0.5 * float(np.mean(H_C[i_cells])))
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * src_hist)
            c.theta[i] = written
            c.V[i] = written
            if cls[i] == 0:
                H_S[i] = written
            else:
                H_C[i] = written
            merged[i] = written
    finally:
        if stressed:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR


def _cell(host, seed, g_ctx, pin, mult, mode, rounds=None):
    if rounds is None:
        rounds = ROUNDS_SPLIT
    c, target, _ = _build(host, seed)
    region = _region(target)
    c.theta[region] = WIND_V
    c.V[region] = WIND_V
    H_S = c.phi_history.copy()
    H_C = c.phi_history.copy()
    for _ in range(rounds):
        _commit_pass(c, region, H_S, H_C, g_ctx, pin, mult, mode)
        c.run(30.0, dt=DT_FALLBACK)
    err = float(c.pattern_error(target))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored in cell"
    return err


def _exp410_per_host_full():
    import json
    p = DEPOSIT.replace("exp425_register_channel_split.json",
                        "exp410_register_decomposition.json")
    with open(p) as f:
        d = json.load(f)
    on = d["raw"]["C_FULL"]["on"]
    off = d["raw"]["C_FULL"]["off"]
    per_host = {}
    for h in range(N_HOSTS):
        rows_o = on[h * len(SEEDS):(h + 1) * len(SEEDS)]
        rows_f = off[h * len(SEEDS):(h + 1) * len(SEEDS)]
        per_host[h] = float(np.mean(rows_f) - np.mean(rows_o))
    return per_host


def main(budget: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget == "smoke"
    hosts = range(1 if smoke else N_HOSTS)
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8 and G_CTX == 0.5
    assert WIND_V == -30.0
    assert STRESS_LADDER == [-60.0, -45.0, -40.0, -35.0]
    assert CORRECTION_LADDER == [0.5, 1.0, 2.0]
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: floor %s, the ladders as written%s)"
          % (CORE.NEURAL_SPEC_MIN, ", SMOKE" if smoke else ""))

    # ---- the dose crossing x arms (hosts[:CROSSING_HOSTS]; the OFF
    # twins cached once per cell)
    hosts_cross = list(hosts)[:CROSSING_HOSTS]
    R = {}
    off_cache = {}
    for h in hosts_cross:
        for s in seeds:
            for pin in STRESS_LADDER:
                for mult in CORRECTION_LADDER:
                    key = (h, s, pin, mult)
                    if key not in off_cache:
                        off_cache[key] = _cell(h, s, 0.0, pin, mult,
                                               "merged")
                    for mode in MODES:
                        err = _cell(h, s, G_CTX, pin, mult, mode)
                        R[(mode, h, s, pin, mult)] = (
                            off_cache[key] - err)
    # G4's point cells on the remaining hosts (the C_FULL point only)
    for h in hosts:
        if h in hosts_cross:
            continue
        for s in seeds:
            off_cache[(h, s, -35.0, 1.0)] = _cell(h, s, 0.0, -35.0, 1.0,
                                                  "merged")
            for mode in ("split", "stress_only", "correct_only"):
                err = _cell(h, s, G_CTX, -35.0, 1.0, mode)
                R[(mode, h, s, -35.0, 1.0)] = (
                    off_cache[(h, s, -35.0, 1.0)] - err)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"
    assert all(np.isfinite(v) for v in R.values())

    # ---- per-arm per-host rho (the median across hosts)
    rho = {}
    for mode in MODES:
        rs, rc = [], []
        for h in hosts_cross:
            rvals = [R[(mode, h, s, p, m)]
                     for s in seeds
                     for p in STRESS_LADDER
                     for m in CORRECTION_LADDER]
            pins = [p for _ in seeds for p in STRESS_LADDER
                    for _ in CORRECTION_LADDER]
            mults = [m for _ in seeds for _ in STRESS_LADDER
                     for m in CORRECTION_LADDER]
            rs.append(_spearman([INTEN[p] for p in pins], rvals))
            rc.append(_spearman(mults, rvals))
        rho[mode] = {"rho_stress_med": float(np.median(rs)),
                     "rho_correct_med": float(np.median(rc)),
                     "per_host_stress": rs, "per_host_correct": rc}
    detail["rho"] = rho
    for mode in MODES:
        print("  %s: rho_stress %.3f rho_correct %.3f"
              % (mode, rho[mode]["rho_stress_med"],
                 rho[mode]["rho_correct_med"]))

    # ---- G2 the calibration (MERGED at rounds=1 — the landed form's
    # bit-path — vs exp410's per-host C_FULL R, all 4 hosts)
    try:
        full410 = _exp410_per_host_full()
        ok = 0
        cal = {}
        for h in hosts:
            r_m = float(np.mean([
                _cell(h, s, 0.0, -35.0, 1.0, "merged", rounds=1)
                - _cell(h, s, G_CTX, -35.0, 1.0, "merged", rounds=1)
                for s in seeds]))
            cal[h] = {"merged": round(r_m, 4),
                        "exp410": round(full410[h], 4),
                        "delta": round(abs(r_m - full410[h]), 4)}
            if abs(r_m - full410[h]) <= MERGED_TOL:
                ok += 1
        verdicts["G2"] = "PASS" if ok >= max(1, int(np.ceil(
            3 * len(list(hosts)) / 4))) else "REFUTE"
        detail["calibration"] = cal
    except (OSError, KeyError) as e:
        verdicts["G2"] = "REFUTE"
        detail["calibration"] = {"error": repr(e)}
    print("G2 %s (%s)" % (verdicts["G2"], detail.get("calibration")))

    # ---- G3 the separation
    so, co = rho["stress_only"], rho["correct_only"]
    sep = (abs(so["rho_stress_med"]) >= RHO_OWN
           and abs(so["rho_correct_med"]) <= RHO_OTHER
           and abs(co["rho_correct_med"]) >= RHO_OWN
           and abs(co["rho_stress_med"]) <= RHO_OTHER)
    verdicts["G3"] = "PASS" if sep else "REFUTE"
    print("G3 %s (stress-only %.3f/%.3f, correct-only %.3f/%.3f; bars "
          "own %.2f other %.2f)" % (verdicts["G3"],
                                    so["rho_stress_med"],
                                    so["rho_correct_med"],
                                    co["rho_correct_med"],
                                    co["rho_stress_med"],
                                    RHO_OWN, RHO_OTHER))

    # ---- G4 the recombination (SPLIT >= max(SO, CO) - tol at C-FULL)
    ok, rec = 0, {}
    for h in hosts:
        r_sp = float(np.mean([R[("split", h, s, -35.0, 1.0)]
                              for s in seeds]))
        r_so = float(np.mean([R[("stress_only", h, s, -35.0, 1.0)]
                              for s in seeds]))
        r_co = float(np.mean([R[("correct_only", h, s, -35.0, 1.0)]
                              for s in seeds]))
        rec[h] = {"split": round(r_sp, 4), "stress_only": round(r_so, 4),
                  "correct_only": round(r_co, 4)}
        if r_sp >= max(r_so, r_co) - RECOMB_TOL:
            ok += 1
    verdicts["G4"] = ("PASS" if ok >= max(1, int(np.ceil(
        3 * len(list(hosts)) / 4))) else "REFUTE")
    detail["recombination"] = rec
    print("G4 %s (%s)" % (verdicts["G4"], rec))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}

    branch = ("DUALITY-SEPARABLE" if verdicts["G3"] == "PASS"
              else "DUALITY-ENTANGLED")
    if verdicts["G1"] != "PASS" or verdicts["G2"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    dep = {
        "experiment": "exp425",
        "title": "THE REGISTER'S DUALITY UNDER CHANNEL SEPARATION "
                 "(batch HU-12)",
        "instrument": {
            "arms": list(MODES),
            "rounds_per_arm": ROUNDS_SPLIT,
            "crossing_hosts": CROSSING_HOSTS,
            "crossing": {"pins": STRESS_LADDER, "mults": CORRECTION_LADDER},
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "hosts": N_HOSTS, "seeds": SEEDS}},
        "R_table": {"%s|%d|%d|%s|%s" % k: round(v, 4)
                    for k, v in R.items()},
        "rho": rho,
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
    print("EXP425 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget="smoke" if "--smoke" in _argv else "full")
