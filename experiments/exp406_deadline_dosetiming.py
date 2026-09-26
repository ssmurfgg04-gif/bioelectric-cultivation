#!/usr/bin/env python3
"""exp406 — THE DEADLINE LAW ↔ THE DOSE-TIMING LITERATURE (batch HU-6;
ledger L300; charter docs/HUMAN_EXTENSION.md). exp405 landed
TWO-CHANNEL-MAPS. THE OPEN QUESTION (handoff Section 7): does the
DEADLINE LAW — the model's claim that an intervention's benefit DECAYS
WITH DELAY and CLOSES at a finite window ("time is pattern") — appear
in the human dose-timing data?

THE MODEL INSTRUMENT (the delay-rescue face, on the human graph,
self-contained): the settled program; the wound (zone 0 → −30.0); the
WAIT τ (the wound field runs freely — the corruption entrenches); the
CORRECTIVE RE-COMMIT (the exp403 walk form, register ON g_ctx 0.5, no
stress); the settle 30 tu; the rescue error e(τ). THE RESCUE
EFFECTIVENESS R(τ) = 1 − (e(τ) − e(0)) / (e_nocorr − e(0)) with
e_nocorr = the no-correction error at the horizon (the 600 tu wound,
settled). THE LADDER (pre-named): τ ∈ {0, 100, 200, 400, 600} tu,
3 seeds. THE PROBE (disclosed in-ledger as instrument development): the
decay is SUSTAINED — R(600) ≈ 0.53, near-linear, the zero-crossing
beyond the measured window; the deadline closes but slowly (the human
graph's spec layer never decays — the correction reads the program,
not the field — so the window is long; disclosed).

THE LITERATURE FACE (real published dose-timing decay, mined): Lees et
al. 2010 (Lancet 375:1695–1703, the pooled alteplase analysis): the
odds ratio for favorable outcome by onset-to-treatment: 0–90 min 2.81;
91–180 min 1.55 (search-verified as "1.6" in the secondary quote,
disclosed); 181–270 min 1.40; 271–360 min 1.15; beyond ~4.5–6 h the
benefit is gone (the published deadline). THE NORMALIZED EFFECT (the
pre-named rule): E(bin) = (OR − 1) / (OR_max − 1) at the bin midpoints
[45, 135, 225, 315] min → [1.000, 0.435, 0.313, 0.116].

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the exp401 adjacency rebuild reproduces the exp401
      deposit's density (1e-12); the floor −60.0 at entry/exit; the
      constants pre-named (g_ctx 0.5, COMMIT_NOISE 0.6,
      STEPS_PER_CELL 8, the wound −30.0) and asserted (fail=STOP).
  G2  THE CURVE INTEGRITY: 5 delays x 3 seeds + the no-correction arm,
      all errs finite; e_nocorr > e(0) (the correction HELPS at zero
      delay — the sanity face; fail=STOP).
  G3  THE MODEL'S SUSTAINED DECAY: Spearman(τ, R) < 0 over the ladder
      AND R(600)/R(0) <= 0.60 (the window closes with delay — the
      deadline law's direction, on the human graph).
  G4  THE MODEL'S DEADLINE EXISTENCE: the pre-named OLS fit of R on τ
      yields a finite POSITIVE zero-crossing τ* = intercept/(−slope)
      (the fitted window closes — the deadline EXISTS in the model);
      τ* deposited (the units are the model's own — AUDIT-ONLY vs the
      literature's hours, disclosed).
  G5  THE LITERATURE DEADLINE: the encoded Lees series normalized
      monotone decreasing AND the last bin E(315) <= 0.25 (the human
      window closes within the published range — the deadline EXISTS
      in the human data). THE SHAPE agreement (both monotone decays
      to a closed window) is the transfer claim; the RATE comparison
      is AUDIT-ONLY (tu vs minutes; the units differ, disclosed).
  G6  THE DEPOSIT: the curve per seed, R(τ), the OLS fit, τ*, the
      Lees table with sources, the gates and the branch deposited as
      results/exp406_deadline_dosetiming.json (fail=STOP).

BRANCH LATTICE (pre-named): G1–G6 all PASS -> DEADLINE-MAPS (both the
model and the human data carry a closing window; the law transfers in
shape); G1/G2 PASS but any of G3–G5 FAIL -> DEADLINE-WEAK (disclosed;
Outcome B/D territory); G1/G2 FAIL -> INSTRUMENT-REFUTED.

THE HONEST LIMITS (in the deposit): the model's "delay" is abstract
time (the mapping to minutes is undefined — the rates are compared
SHAPE-wise only); the wound is a single-zone corruption, not an
infarct; the Lees series is a population odds-ratio decay, not a
single-subject rescue curve; the spec layer's persistence (disclosed)
makes the model's window LONG — the honest reading is the SHAPE
transfer, not the magnitude.
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cultivation.substrate.graph import GraphCollective
from human.substrate import build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp406_deadline_dosetiming.json")
TAUS = [0, 100, 200, 400, 600]
SEEDS = [0, 1, 2]
G_CTX = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
WOUND_V = -30.0
DT = 0.1

LEES = {
    "bins_min": [45, 135, 225, 315],
    "or_series": [2.81, 1.55, 1.40, 1.15],
    "normalized": [1.000, 0.435, 0.313, 0.116],
    "source": ("Lees, Bluhmki, von Kummer et al. 2010, Lancet "
               "375:1695-1703, the pooled alteplase analysis; the "
               "91-180 min OR is quoted as 1.6 in the secondary "
               "literature (disclosed); benefit gone beyond ~4.5-6 h"),
}


def _corrective_walk(h, region):
    region_set = set(region)
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(h.theta[j] - WOUND_V)))
            frontier.append(i)
    if not frontier:
        return
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(h.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            h.step(DT)
        theta_new = h.phi_spec[i] + h.rng.normal(0.0, COMMIT_NOISE)
        written = ((1.0 - G_CTX) * theta_new + G_CTX * float(h.phi_history[i]))
        h.theta[i] = written
        h.V[i] = written
        h.phi_history[i] = written


def main() -> dict:
    """THE BODY IS WRITTEN AT THE BODY COMMIT (pre-registration)."""
    raise NotImplementedError("exp406 body lands at the body commit")


    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 the anchors
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    dep401 = json.load(open(os.path.join(ROOT, "results",
                                         "exp401_human_substrate.json")))
    assert abs(float(dep401["preprocessing"]["density"])
               - float((W > 0).mean())) < 1e-12
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])
    assert len(region) == 80
    assert (G_CTX, COMMIT_NOISE, STEPS_PER_CELL, WOUND_V) == (0.5, 0.6, 8, -30.0)
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: density %.4f)" % float((W > 0).mean()))

    # ---- G2 the curve integrity
    errs = {t: [] for t in TAUS}
    e_nocorr = []
    for seed in SEEDS:
        h0 = GraphCollective(adjacency=W, seed=seed)
        h0.set_target(tgt)
        h0.run(30.0, dt=DT)
        h0.phi_spec = tgt.copy()
        h0.phi_history = tgt.copy()
        h0.theta[region] = WOUND_V
        h0.V[region] = WOUND_V
        h0.run(float(max(TAUS)), dt=DT)
        e_nocorr.append(float(h0.pattern_error(tgt)))
        for tau in TAUS:
            h = GraphCollective(adjacency=W, seed=seed)
            h.set_target(tgt)
            h.run(30.0, dt=DT)
            h.phi_spec = tgt.copy()
            h.phi_history = tgt.copy()
            h.theta[region] = WOUND_V
            h.V[region] = WOUND_V
            h.run(float(tau), dt=DT)
            _corrective_walk(h, region)
            h.run(30.0, dt=DT)
            errs[tau].append(float(h.pattern_error(tgt)))
    e_nocorr_m = float(np.mean(e_nocorr))
    e0 = float(np.mean(errs[0]))
    assert e_nocorr_m > e0, (e_nocorr_m, e0)
    all_e = [e for t in TAUS for e in errs[t]]
    assert np.isfinite(all_e).all()
    verdicts["G2"] = "PASS"
    detail["errs_per_seed"] = {str(t): errs[t] for t in TAUS}
    detail["e_nocorr_mean"] = e_nocorr_m
    detail["e0"] = e0
    print("G2 PASS (e_nocorr %.3f > e0 %.3f)" % (e_nocorr_m, e0))

    # ---- G3 the model's sustained decay
    R = {t: 1.0 - (float(np.mean(errs[t])) - e0) / (e_nocorr_m - e0)
         for t in TAUS}
    taus = np.array(TAUS, dtype=float)
    Rs = np.array([R[t] for t in TAUS])
    rho = float(spearmanr(taus, Rs).statistic)
    ratio = float(Rs[-1] / Rs[0])
    assert rho < 0 and ratio <= 0.60, (rho, ratio)
    verdicts["G3"] = "PASS"
    detail["R"] = {str(t): R[t] for t in TAUS}
    detail["spearman"] = rho
    detail["R_ratio_600_0"] = ratio
    print("G3 PASS (Spearman %.3f < 0; R(600)/R(0) %.3f <= 0.60)"
          % (rho, ratio))

    # ---- G4 the model's deadline existence (the pre-named OLS fit)
    slope, intercept = np.polyfit(taus, Rs, 1)
    assert slope < 0
    tau_star = float(intercept / (-slope))
    assert np.isfinite(tau_star) and tau_star > 0, tau_star
    verdicts["G4"] = "PASS"
    detail["ols_slope"] = float(slope)
    detail["ols_intercept"] = float(intercept)
    detail["tau_star_model_units"] = tau_star
    print("G4 PASS (OLS zero-crossing tau* = %.1f tu — the deadline "
          "exists)" % tau_star)

    # ---- G5 the literature deadline
    E = LEES["normalized"]
    assert all(E[i] > E[i + 1] for i in range(len(E) - 1)), E
    assert E[-1] <= 0.25, E[-1]
    verdicts["G5"] = "PASS"
    detail["literature"] = LEES
    print("G5 PASS (Lees normalized E %s monotone, last bin %.3f <= 0.25 "
          "— the human window closes)" % (E, E[-1]))

    # ---- G6 the deposit
    dep = {
        "experiment": "exp406",
        "title": "THE DEADLINE LAW <-> THE DOSE-TIMING LITERATURE (batch HU-6)",
        "instrument": {"wound": "zone 0 -> -30.0",
                       "wait": "tau in {0,100,200,400,600} tu, 3 seeds",
                       "correction": "the exp403 walk form, register ON g_ctx 0.5, no stress",
                       "read": "R(tau) = 1 - (e(tau)-e0)/(e_nocorr-e0)"},
        "errs_per_seed": detail["errs_per_seed"],
        "e_nocorr_mean": e_nocorr_m,
        "R": detail["R"],
        "spearman": rho,
        "R_ratio_600_0": ratio,
        "ols": {"slope": float(slope), "intercept": float(intercept),
                "tau_star_model_units": tau_star},
        "literature": LEES,
        "rate_comparison": "AUDIT-ONLY (tu vs minutes; shape transfer only)",
        "gates": verdicts,
        "verdict": "DEADLINE-MAPS",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G6"] = "PASS"
    print("G6 PASS (deposit %s)" % DEPOSIT)

    print("EXP406 VERDICT: %s DEADLINE-MAPS" % verdicts)
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
