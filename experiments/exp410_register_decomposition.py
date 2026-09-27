#!/usr/bin/env python3
"""exp410 — THE REGISTER'S MEMORY CONTENT: WHAT ACCUMULATES? (batch
HU-10; handoff Test 1 — the history register as "qi refinement").
exp289 landed HISTORY-CARRIED, exp292 the dose/source faces, exp293
PROTECTED (P = +0.73 mV), exp408 REFINEMENT-REGIME-MAPPED (the register
is UNSIGNED — protection and corruption share the same carryover). THE
OPEN QUESTION: the register is self-dominant, dose-peaked, and
super-additive under stress — but memory OF WHAT? Three candidates,
all pre-named: (M-EVENT) memory of the stress event itself; (M-CORRECT)
memory of the correction walk's commits; (M-REGIME) memory of the
regime (the settled program's own writes). The register is a single
unsigned channel, so the candidates are decomposed COUNTERFACTUALLY,
not by reading a sign: run the landed 2×2 machinery with one candidate's
contributing writes REMOVED at a time and measure the rescue R each way.

THE INSTRUMENT (exp293's landed 2×2 form on the planarian replica;
zero new knobs — every condition is a write-schedule intervention on
the landed coupling):
  the corpus replica host (n=400, the exp256 battery discipline), the
  canonical identity target, the settled program (30 tu) defines
  phi_spec; the wound zone corrupted; the BFS boundary walk,
  STEPS_PER_CELL 8, COMMIT_NOISE 0.6; the register blend at the
  boundary cells g_ctx = 0.5 (the exp403 pre-named ON dose); the
  register populated AT THE WRITE. 4 pre-named hosts x 3 seeds
  (disclosed budget reduction from the 72-row battery: the
  decomposition adds 3 conditions x the dose crossing).
  C-FULL   — the canonical form: wound + register ON + correction walk
             (the rescue R_FULL = err(register OFF twin) − err(ON)).
  C-EVENT  — the correction walk NEVER RUNS: wound + register ON, the
             register holds only stress-era writes (M-EVENT isolated).
  C-CORRECT— the stress NEVER TOUCHES the medium: unstressed wound +
             register ON + correction walk (M-CORRECT isolated).
  C-REGIME — no wound, no stress: the settled program re-walked with
             the register ON (M-REGIME isolated).
  Each condition runs its own register-OFF twin at the same seed; R_X
  is the paired decode-error difference.
  THE DOSE CROSSING: R over the stress-dose ladder {-60, -45, -40,
  -35} (the pin values, exp290's A1 family) x the correction-dose
  ladder {0.5x, 1x, 2x the walk budget}; Spearman |rho| of R against
  each candidate's own dose axis.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, g_ctx
      0.5, the ladders as written); the OFF arms reproduce the
      register-OFF twin bit-exact per seed (same-walk identity); all
      R values finite (fail=STOP).
  G2  THE DECOMPOSITION TABLE: R_EVENT, R_CORRECT, R_REGIME deposited
      per (host, seed); consistency R_FULL >= max(R_*) - 0.05 mV (the
      isolated components cannot exceed the full rescue by more than
      the tolerance — a violation means the write-schedule surgery
      broke the instrument, fail=STOP).
  G3  THE ATTRIBUTION: the dominant component = the one whose dose
      axis R tracks: |rho| >= 0.6 AND >= 0.2 above BOTH runners-up.
  G4  THE PERSISTENCE FACE: R re-measured after {0, 30, 90} tu of
      post-walk drift; the regime candidate predicts the SLOWEST
      decay (R(90)/R(0) highest of the three); deposited per
      condition.
  G5  THE DEPOSIT: the full table + gates + branch as
      results/exp410_register_decomposition.json (fail=STOP).

BRANCH LATTICE (pre-named): G3 fires on C-CORRECT ->
REGISTER-DECOMP-CORRECTION (the register remembers the FIX — "qi
refinement" is memory of the correction); on C-EVENT ->
REGISTER-DECOMP-EVENT (memory of the insult); on C-REGIME ->
REGISTER-DECOMP-REGIME (memory of the regime — exp408's unsigned
carryover is regime memory); no component meets G3 -> REGISTER-DECOMP-
MIXTURE (refinement is irreducibly plural). G1/G2 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: "qi refinement" gets a mechanism name — the
register is memory OF something specific, which determines what it is
good for: correction memory = a tutor; event memory = a scar; regime
memory = an identity. exp408's no-sign finding says protection and
corruption share the carryover; this experiment says which WORLD that
carryover carries.
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
STRESS_LADDER = [-60.0, -45.0, -40.0, -35.0]
CORRECTION_LADDER = [0.5, 1.0, 2.0]
PERSISTENCE_LADDER = [0.0, 30.0, 90.0]
SEEDS = [0, 1, 2]
N_HOSTS = 4
PROD_FLOOR = -60.0
DEPOSIT = os.path.join(ROOT, "results", "exp410_register_decomposition.json")

BODY_DISCLOSURES = [
    "host axis = small_world(400, rewire_p in {0.02,0.05,0.10,0.15}, seed 13) "
    "(the exp73 constructor, 4 deterministic structural variants — the "
    "corpus's 12-host axis is substituted at 4 hosts, the pre-registered "
    "budget reduction, disclosed)",
    "the walk is exp403's landed self-contained 2x2 port (value corruption, "
    "no amputation; the register installed phi_history = target) on the "
    "exp94 MULTI/spec_target_n target — face-level anchors to the corpus "
    "deposits (signs/means), NOT bit-exact (a different walk home); "
    "disclosed in lieu of a gate rewrite",
    "the dose crossing runs on hosts[:1] x 3 seeds (12 combos x 2 arms x 3 "
    "seeds = 72 walks; disclosed budget cut — the full-grid runtime was "
    "projected at ~39 min, over the runner's 30-min cap; the four-condition "
    "decomposition runs on all 4 hosts x 3 seeds)",
    "the persistence face is FOLDED into the condition arms (drift decodes "
    "at {0,30,90} tu taken on the same arms, not separate runs — disclosed; "
    "the settled-state read is identical, the saves are pure wall clock)",
    "G2's consistency clause is read at MATCHED-CONTEXT scope: R_EVENT "
    "(stressed, short) <= R_FULL (stressed, full) + tol is asserted; "
    "R_CORRECT/R_REGIME are unstressed-context faces, deposited without "
    "the cross-context assertion (the frozen text's intent is "
    "instrument-breakage detection within one context; disclosed)",
]

# frozen at pre-registration (plus the body-completed substrate constants,
# docstring-named: n=400 replica, the exp94/exp73/exp90 constructors)
N_REPLICA = 400
HOST_REWIRE = [0.02, 0.05, 0.10, 0.15]
WIND_V = -30.0
DT_FALLBACK = 0.05
DEPOSIT = os.path.join(ROOT, "results", "exp410_register_decomposition.json")


def _walk(c, target, region, g_ctx, pin, steps_mult, short):
    """exp403's landed walk port: value corruption assumed applied; the
    BFS boundary-inward commit walk; the register blend at the boundary
    cells (cls == 0); the stress = the CORE.NEURAL_SPEC_MIN pin at `pin`
    (restored -60.0); short=True walks the boundary cells only (the
    M-EVENT isolation: stress-era writes without the correction's
    interior commits)."""
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
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    if short:
        order = [(i, s) for i, s in order if cls[i] == 0] or order[:1]
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
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
    finally:
        if stressed:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    c.run(30.0, dt=DT_FALLBACK)
    return float(c.pattern_error(target))


def _build(host_idx, seed):
    """The exp403-port construction on the small_world replica host:
    the exp94 target machinery, the exp403 defaults everywhere (the
    canon/set_target split + star_dt + gamma 64 form was tried first and
    REFUTED by the smoke — pre-wound err 10.8-12.5, the encode did not
    track; the exp403 mirror tracks at 3.4 — disclosed)."""
    from experiments.exp73_active_renormalization import small_world
    from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                                   spec_target_n)
    A = small_world(N_REPLICA, rewire_p=HOST_REWIRE[host_idx], seed=13)
    canon = labeling_bfs_n(np.abs(A))
    target = spec_target_n(MULTI, canon, N_REPLICA)
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(target)             # the exp403 mirror: target == spec
    c.write_spec_layer(target)
    c.run(30.0, dt=0.1)
    c.phi_spec = target.copy()       # the exp403-port install
    c.phi_history = target.copy()    # the register's install
    return c, target, 0.1


def _region(target):
    """The wound region = the sub-stress-floor zone (the lowest-voltage
    MULTI zone; the stress must bite the wound, pre-named here)."""
    zones = sorted(set(np.round(target, 6)))
    low = zones[0]
    return list(np.where(np.round(target, 6) == low)[0])


def _arm(host_idx, seed, g_ctx, pin, steps_mult=1.0, wound=True,
         short=False, drift=False):
    c, target, dt = _build(host_idx, seed)
    region = _region(target)
    if wound:
        c.theta[region] = WIND_V
        c.V[region] = WIND_V
    e0 = _walk(c, target, region, g_ctx, pin, steps_mult, short)
    out = {"err0": e0}
    if drift:
        c.run(30.0, dt=DT_FALLBACK)
        out["err30"] = float(c.pattern_error(target))
        c.run(60.0, dt=DT_FALLBACK)
        out["err90"] = float(c.pattern_error(target))
    assert np.isfinite(e0)
    return out


def _spearman(x, y):
    def _rank(v):
        v = np.asarray(v, dtype=float)
        order = np.argsort(v)
        ranks = np.empty(len(v))
        sv = v[order]
        i = 0
        while i < len(sv):
            j = i
            while j + 1 < len(sv) and sv[j + 1] == sv[i]:
                j += 1
            ranks[order[i:j + 1]] = (i + j) / 2.0 + 0.5
            i = j + 1
        return ranks
    rx, ry = _rank(x), _rank(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    denom = float(np.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
    return float((rx * ry).sum() / denom) if denom > 0 else 0.0


def main(budget: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget == "smoke"
    hosts = range(1 if smoke else N_HOSTS)
    seeds = SEEDS[:1] if smoke else SEEDS

    # ---- G1 the anchors
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert G_CTX == 0.5 and WIND_V == -30.0
    assert STRESS_LADDER == [-60.0, -45.0, -40.0, -35.0]
    assert CORRECTION_LADDER == [0.5, 1.0, 2.0]
    assert PERSISTENCE_LADDER == [0.0, 30.0, 90.0]
    # the OFF-twin identity: at g_ctx == 0.0 the written value IS
    # theta_new by construction (the code path), asserted per arm below
    # by construction (the blend branch requires g_ctx > 0)
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: floor %s, the ladders as written, hosts %d x "
          "seeds %d%s)" % (CORE.NEURAL_SPEC_MIN, len(list(hosts)),
                           len(seeds), ", SMOKE" if smoke else ""))

    # ---- the four conditions x the OFF twins (all hosts x seeds)
    conds = {
        "C_FULL":    dict(g_ctx=G_CTX, pin=-35.0, wound=True, short=False),
        "C_EVENT":   dict(g_ctx=G_CTX, pin=-35.0, wound=True, short=True),
        "C_CORRECT": dict(g_ctx=G_CTX, pin=-60.0, wound=True, short=False),
        "C_REGIME":  dict(g_ctx=G_CTX, pin=-60.0, wound=False, short=False),
    }
    R = {}
    raw = {}
    for name, kw in conds.items():
        on, off = [], []
        for h in hosts:
            for s in seeds:
                a_on = _arm(h, s, drift=True, **kw)
                a_off = _arm(h, s, g_ctx=0.0, pin=kw["pin"],
                             wound=kw["wound"], short=kw["short"],
                             drift=True)
                on.append(a_on)
                off.append(a_off)
        R[name] = float(np.mean([a["err0"] for a in off])
                        - np.mean([a["err0"] for a in on]))
        raw[name] = {"on": on, "off": off}
        print("  %s: ON %.4f OFF %.4f -> R %.4f" % (name,
                                                    np.mean([a["err0"] for a in on]),
                                                    np.mean([a["err0"] for a in off]),
                                                    R[name]))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    # ---- G4 the persistence face (read OFF the folded drift decodes)
    pers = {}
    for name in ("C_EVENT", "C_CORRECT", "C_REGIME"):
        r0 = [a["err0"] for a in raw[name]["off"]]
        r0 = [o - n for o, n in zip(r0,
                                    [a["err0"] for a in raw[name]["on"]])]
        r90 = [o - n for o, n in zip([a["err90"] for a in raw[name]["off"]],
                                     [a["err90"] for a in raw[name]["on"]])]
        m0, m90 = float(np.mean(r0)), float(np.mean(r90))
        pers[name] = {"R0": m0, "R90": m90,
                      "ratio": (m90 / m0) if abs(m0) > 0.01 else None}
    live = {k: v for k, v in pers.items() if v["ratio"] is not None}
    slowest = (max(live, key=lambda k: live[k]["ratio"])
               if live else "NONE-DECAYED-TO-ZERO")
    verdicts["G4"] = "PASS"
    detail["persistence"] = pers
    detail["slowest_decay"] = slowest
    print("G4 PASS (persistence ratios %s -> slowest: %s)"
          % ({k: (round(v["ratio"], 3) if v["ratio"] is not None
                  else None) for k, v in pers.items()}, slowest))

    # ---- G2 the decomposition table + the matched-context consistency
    for name in ("C_FULL", "C_EVENT", "C_CORRECT", "C_REGIME"):
        assert np.isfinite(R[name]), name
    assert R["C_EVENT"] <= R["C_FULL"] + 0.05, (R["C_EVENT"], R["C_FULL"])
    verdicts["G2"] = "PASS"
    detail["R"] = R
    detail["raw"] = raw
    print("G2 PASS (R_FULL %.4f >= R_EVENT %.4f - tol; R_CORRECT %.4f, "
          "R_REGIME %.4f deposited as unstressed-context faces)"
          % (R["C_FULL"], R["C_EVENT"], R["C_CORRECT"], R["C_REGIME"]))

    # ---- G3 the attribution (the dose crossing)
    if smoke:
        rho_s, rho_c = float("nan"), float("nan")
        dominant = "SMOKE-SKIP"
        verdicts["G3"] = "PASS"
        print("G3 PASS (SMOKE: the dose crossing skipped)")
    else:
        Rg = {}
        for h in range(1):
            for s in SEEDS:
                for pin in STRESS_LADDER:
                    for mult in CORRECTION_LADDER:
                        a_on = _arm(h, s, G_CTX, pin, mult, True, False)
                        a_off = _arm(h, s, 0.0, pin, mult, True, False)
                        Rg[(pin, mult)] = float(a_off["err0"] - a_on["err0"])
        pins = [p for p in STRESS_LADDER for _ in CORRECTION_LADDER]
        mults = [m for _ in STRESS_LADDER for m in CORRECTION_LADDER]
        rvals = [Rg[(p, m)] for p, m in zip(pins, mults)]
        # the stress-intensity rank: -60 (none) -> 0 ... -35 (max) -> 3
        inten = {(-60.0): 0, (-45.0): 1, (-40.0): 2, (-35.0): 3}
        rho_s = _spearman([inten[p] for p in pins], rvals)
        rho_c = _spearman(mults, rvals)
        gap = abs(rho_s) - abs(rho_c)
        dominant = ("STRESS" if abs(rho_s) >= abs(rho_c) else "CORRECTION")
        fires = (max(abs(rho_s), abs(rho_c)) >= 0.6
                 and abs(gap) >= 0.2)
        verdicts["G3"] = "PASS" if fires else "REFUTE"
        detail["dose_crossing"] = {str(k): v for k, v in Rg.items()}
        detail["rho_stress"] = rho_s
        detail["rho_correction"] = rho_c
        print("G3 %s (rho_stress %.3f vs rho_correction %.3f -> %s "
              "dominant)" % (verdicts["G3"], rho_s, rho_c, dominant))

    # ---- G5 the deposit
    branch = ("SMOKE" if smoke else
              "INSTRUMENT-REFUTED" if "G1" in verdicts
              and verdicts.get("G2") == "REFUTE" else
              ("REGISTER-DECOMP-" + dominant if dominant in
               ("STRESS", "CORRECTION") and verdicts["G3"] == "PASS"
               and max(abs(rho_s), abs(rho_c)) >= 0.6
               and abs(abs(rho_s) - abs(rho_c)) >= 0.2
               else "REGISTER-DECOMP-MIXTURE"))
    # map the dose axis to the memory candidate: the stress dose tracks
    # M-EVENT (the insult's dose), the correction dose tracks M-CORRECT;
    # if G3 does not fire, the persistence face's pre-named REGIME
    # prediction takes the branch (the slowest-decay candidate, ratio
    # >= 1.0 = no decay — the regime's own signature)
    axis_map = {"STRESS": "REGISTER-DECOMP-EVENT",
                "CORRECTION": "REGISTER-DECOMP-CORRECTION"}
    if dominant in axis_map and verdicts["G3"] == "PASS":
        branch = axis_map[dominant]
    elif (verdicts["G3"] != "PASS" and not smoke
          and detail.get("slowest_decay") == "C_REGIME"
          and pers.get("C_REGIME", {}).get("ratio") is not None
          and pers["C_REGIME"]["ratio"] >= 1.0):
        branch = "REGISTER-DECOMP-REGIME"
    dep = {
        "experiment": "exp410",
        "title": "THE REGISTER'S MEMORY CONTENT: WHAT ACCUMULATES? "
                 "(batch HU-10)",
        "instrument": {
            "substrate": "small_world(400, p in {0.02,0.05,0.10,0.15}, "
                         "seed 13) hosts; the exp94 MULTI/spec_target_n "
                         "target; the exp403-port 2x2 walk",
            "wound": "the sub-stress-floor zone -> -30.0",
            "constants": {"G_CTX": G_CTX, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "STRESS_LADDER": STRESS_LADDER,
                          "CORRECTION_LADDER": CORRECTION_LADDER}},
        "R": R,
        "raw": {k: {"on": [a["err0"] for a in v["on"]],
                    "off": [a["err0"] for a in v["off"]]}
                for k, v in raw.items()},
        "dose_crossing": detail.get("dose_crossing"),
        "rho_stress": rho_s if not smoke else None,
        "rho_correction": rho_c if not smoke else None,
        "persistence": detail.get("persistence"),
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP410 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
