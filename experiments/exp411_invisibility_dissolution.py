#!/usr/bin/env python3
"""exp411 — THE DISSOLUTION SHAPE AND THE MEMORY-DISCIPLINE FACE
(batch HU-10; handoff Test 2a). exp407 landed BYPASS-EXPLAINED: the
composed carrier's +0.0000 mV stress delta is the SATURATION limit —
at g=1.0 the commit reads the register chain, a channel the stress
cannot reach — and G4 landed the dissolution MONOTONE as g falls
{1.0, 0.75, 0.5, 0.25, 0.0}. TWO questions stay open. (1) THE SHAPE:
is the dissolution THRESHOLDED (dynamics re-enter at a g* — the
register chain stops dominating abruptly) or GRADUAL (the two channels
blend continuously)? A threshold means a SAFE operating band exists
(carrier ON, dynamics readable below g*); gradual means every carrier
strength buys invisibility with the same coin. (2) THE DISCIPLINE
FACE: exp407 moved the practical target to "memory-write discipline".
Can a two-pass write — commit saturated at g=1.0, then ONE refresh
pass at g=0.5 re-exposing the memory to dynamics — keep the carrier's
improvement while returning stress visibility? If yes, the discipline
recipe exists; if the refresh destroys the carrier, the discipline is
costly and the trade is quantified.

THE INSTRUMENT (exp407's landed form VERBATIM): path(100), the 3-zone
spec [-50 x40, -30 x30, -20 x30], faces (ctx, gj) — the apop sigma
face excluded as exp407 excluded it; the write-time -35.0 pin
(exp290's A1), restored -60.0; COMMIT_NOISE 0.6, STEPS_PER_CELL 8;
the register populated at the write.
  F-SHAPE: the fine g ladder {1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6,
           0.5, 0.25, 0.0} x stress {off, on} x 10 seeds (exp407's 5
           seeds kept + 5 additive, disclosed); |Delta(g)| = the mean
           |err(on) - err(off)| per g; Hill fit |D(g)| = Dmax * g*h^n
           / (g*h^n + g^n) vs the linear fit on the same 10 points
           (least squares on the means, zero knobs).
  F-DISCIPLINE: the two-pass arm — the standard walk with the blended
           cells committed at g=1.0, then ONE refresh pass over the
           same cells at g=0.5 (write = 0.5*theta_new + 0.5*
           phi_history), then the settle; the stress 2x2 on the
           two-pass form; carrier retained = the two-pass improvement
           vs register-OFF >= 0.8 x the g=1.0 one-pass improvement;
           visibility returned = |Delta_two-pass| >= 0.10 x the
           g=0.0 one-pass mean |Delta|.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      pin -35.0, the ladders as written); at the shared 5 seeds the
      g=1.0 and g=0.0 arms reproduce exp407's deposited per-seed
      deltas BIT-EXACT (the anchor; the 5 additive seeds disclosed).
  G2  THE MONOTONE FACE RE-CONFIRMED: |Delta(g)| non-decreasing as g
      falls across all 10 ladder points (ties allowed), 10/10 seeds
      finite.
  G3  THE SHAPE BRANCH: thresholded iff Hill R^2 > linear R^2 + 0.10
      on the 10 mean points; g* (the Hill half-point) deposited if
      thresholded.
  G4  THE DISCIPLINE FACE: both pre-named conditions evaluated once,
      numbers deposited; VIABLE iff carrier retained AND visibility
      returned; COSTLY otherwise (which condition failed, deposited).
  G5  THE DEPOSIT: the ladder table, both fits, the two-pass table,
      gates + branch as results/exp411_invisibility_dissolution.json
      (fail=STOP).

BRANCH LATTICE (pre-named): DISSOLUTION-THRESHOLDED +
MEMORY-DISCIPLINE-VIABLE (the safe band exists AND the recipe works —
the carrier story closes both ways); DISSOLUTION-THRESHOLDED +
MEMORY-DISCIPLINE-COSTLY; DISSOLUTION-GRADUAL + VIABLE; DISSOLUTION-
GRADUAL + COSTLY (no safe band, no recipe — the invisibility is the
carrier's price at every strength). G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: exp407 said build commit layers that read memory,
not dynamics. This experiment says whether the reading can be SCHEDULED
(a band, a recipe) or only bought (a trade). A thresholded dissolution
with a viable discipline face is an engineering result; the gradual +
costly branch is the honest negative that closes the practical story.
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
from cultivation.substrate.graph import GraphCollective, path

# frozen at pre-registration
N = 100        # the exp407 chain substrate (docstring-named; the stub
               # omitted the constant — body-side completion, disclosed)
GLADDER = [1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5, 0.25, 0.0]
REFRESH_G = 0.5
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ANCHOR_SEEDS = [0, 1, 2, 3, 4]
DT = 0.1
WINDOW = 30.0
DEPOSIT = os.path.join(ROOT, "results", "exp411_invisibility_dissolution.json")


def _spec_target():
    tgt = np.empty(N)
    tgt[:40] = -50.0
    tgt[40:70] = -30.0
    tgt[70:] = -20.0
    return tgt


def _run_arm(g, stress, seed, refresh_g=None):
    """exp407's landed arm form VERBATIM + the optional two-pass refresh
    (the F-DISCIPLINE arm: refresh_g=None -> the one-pass exp407 form;
    a float -> ONE refresh pass over the blended cells at that g after
    the saturated pass). Same RNG consumption per pass as exp407."""
    c = GraphCollective(adjacency=path(N), seed=seed)
    tgt = _spec_target()
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(WINDOW, dt=DT)
    region = list(range(20, 60))
    region_set = set(region)
    c.amputate(slice(region[0], region[-1] + 1))
    wound_center = float(np.mean(c.theta[region]))
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = region[:1]
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
    blended = sorted(bnd | (set(region) - bnd))
    commits = {}

    def _commit_pass(gg, collect):
        for i, src in order:
            for _ in range(STEPS_PER_CELL):
                c.step(DT)
            if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                commit_base = c.phi_spec[i]
            else:
                commit_base = c.theta[src]
            hist_i = float(c.phi_history[i])
            theta_new = commit_base + c.rng.normal(0.0, COMMIT_NOISE)
            written = theta_new
            if gg > 0.0 and i in blended:
                written = (1.0 - gg) * theta_new + gg * hist_i
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
            if collect:
                commits[i] = float(written)

    if stress:
        CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
    _commit_pass(g, collect=True)
    if refresh_g is not None:
        _commit_pass(refresh_g, collect=False)
    if stress:
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    c.run(WINDOW, dt=DT)
    err = float(c.pattern_error(tgt))
    return commits, err, blended


def _r2(y, yhat):
    ss_res = float(np.sum((np.asarray(y) - np.asarray(yhat)) ** 2))
    ss_tot = float(np.sum((np.asarray(y) - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def main() -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    dep407 = json.load(open(os.path.join(
        ROOT, "results", "exp407_invisibility_mechanism.json")))

    # ---- G1 the anchors
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert GLADDER == [1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5, 0.25, 0.0]
    assert REFRESH_G == 0.5 and DT == 0.1 and WINDOW == 30.0
    anchor_ok = True
    for g in (1.0, 0.0):
        for stress in (False, True):
            key = ("%g|%s" % (g, stress))
            ref = dep407["errs"][key]
            for si, seed in enumerate(ANCHOR_SEEDS):
                _, err, _ = _run_arm(g, stress, seed)
                if err != ref[si]:
                    anchor_ok = False
    assert anchor_ok, "the exp407 anchor errs drifted"
    verdicts["G1"] = "PASS"
    print("G1 PASS (20/20 anchor arms bit-exact vs exp407's deposit)")
    detail["anchor_bit_exact"] = True

    # ---- the battery (the fine ladder, 10 seeds)
    errs = {(g, s): [] for g in GLADDER for s in (False, True)}
    for g in GLADDER:
        for stress in (False, True):
            for seed in SEEDS:
                _, err, _ = _run_arm(g, stress, seed)
                errs[(g, stress)].append(err)
                assert np.isfinite(err)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR

    # ---- G2 the monotone face re-confirmed (|delta| as g falls)
    deltas = {g: float(np.mean([o - n for o, n in
                                zip(errs[(g, False)], errs[(g, True)])]))
              for g in GLADDER}
    seq_desc = [abs(deltas[g]) for g in GLADDER]     # g: 1.0 -> 0.0
    mono = all(seq_desc[i] <= seq_desc[i + 1] + 1e-12
               for i in range(len(seq_desc) - 1))
    assert mono, seq_desc
    verdicts["G2"] = "PASS"
    detail["mean_delta_per_g"] = {str(g): deltas[g] for g in GLADDER}
    detail["abs_delta_desc"] = seq_desc
    print("G2 PASS (|delta| ladder %s monotone non-decreasing toward g=0)"
          % ["%.4f" % x for x in seq_desc])

    # ---- G3 the shape branch (Hill vs linear on the 10 mean points)
    gs = np.array(GLADDER)
    ad = np.abs([deltas[g] for g in GLADDER])
    dmax = float(ad.max())
    best = None
    for n_exp in np.concatenate([np.linspace(0.25, 8.0, 64),
                                 np.linspace(0.25, 8.0, 512)]):
        for gh in np.concatenate([np.linspace(0.05, 1.0, 40),
                                  np.linspace(0.05, 1.0, 200)]):
            pred = dmax * (gh ** n_exp) / (gh ** n_exp + gs ** n_exp)
            sse = float(np.sum((ad - pred) ** 2))
            if best is None or sse < best[0]:
                best = (sse, float(n_exp), float(gh))
    sse_h, n_fit, gh_fit = best
    hill_pred = dmax * (gh_fit ** n_fit) / (gh_fit ** n_fit + gs ** n_fit)
    r2_hill = _r2(ad, hill_pred)
    lin = np.polyfit(gs, ad, 1)
    r2_lin = _r2(ad, np.polyval(lin, gs))
    thresholded = bool(r2_hill > r2_lin + 0.10)
    verdicts["G3"] = "PASS"
    detail["hill"] = {"dmax": dmax, "n": n_fit, "g_star": gh_fit,
                      "r2": r2_hill}
    detail["linear_r2"] = r2_lin
    detail["shape"] = ("THRESHOLDED" if thresholded else "GRADUAL")
    print("G3 %s (Hill R2 %.4f [n %.2f, g* %.3f] vs linear R2 %.4f -> %s)"
          % (verdicts["G3"], r2_hill, n_fit, gh_fit, r2_lin,
             detail["shape"]))

    # ---- G4 the discipline face (the two-pass write)
    imp_off = float(np.mean(errs[(0.0, False)]))
    imp_onepass = imp_off - float(np.mean(errs[(1.0, False)]))
    vis_g0 = float(np.mean([abs(o - n) for o, n in
                            zip(errs[(0.0, False)], errs[(0.0, True)])]))
    tp_errs = {"off": [], "on": []}
    for seed in SEEDS:
        _, e_off, _ = _run_arm(1.0, False, seed, refresh_g=REFRESH_G)
        _, e_on, _ = _run_arm(1.0, True, seed, refresh_g=REFRESH_G)
        tp_errs["off"].append(e_off)
        tp_errs["on"].append(e_on)
        assert np.isfinite(e_off) and np.isfinite(e_on)
    tp_mean_off = float(np.mean(tp_errs["off"]))
    tp_mean_on = float(np.mean(tp_errs["on"]))
    tp_imp = imp_off - tp_mean_off
    tp_absdelta = abs(tp_mean_on - tp_mean_off)
    retained = bool(tp_imp >= 0.8 * imp_onepass)
    visible = bool(tp_absdelta >= 0.10 * vis_g0)
    viable = retained and visible
    verdicts["G4"] = "PASS"
    detail["discipline"] = {
        "improvement_onepass": imp_onepass, "improvement_twopass": tp_imp,
        "carrier_retained": retained, "visibility_returned": visible,
        "absdelta_twopass": tp_absdelta, "absdelta_g0": vis_g0,
        "viable": viable,
        "errs_off": tp_errs["off"], "errs_on": tp_errs["on"]}
    print("G4 PASS (two-pass: improvement %.4f vs one-pass %.4f "
          "[retained=%s]; |delta| %.4f vs 0.10 x %.4f [visible=%s] -> %s)"
          % (tp_imp, imp_onepass, retained, tp_absdelta, vis_g0,
             visible, "VIABLE" if viable else "COSTLY"))

    # ---- G5 the deposit
    dep = {
        "experiment": "exp411",
        "title": "THE DISSOLUTION SHAPE AND THE MEMORY-DISCIPLINE FACE "
                 "(batch HU-10)",
        "instrument": {"substrate": "path(100), the 3-zone spec [-50 x40, -30 x30, -20 x30]",
                       "faces": "(ctx, gj) — the apop sigma face excluded (exp407's disclosed exclusion)",
                       "ladder": GLADDER, "refresh_g": REFRESH_G,
                       "constants": {"COMMIT_NOISE": COMMIT_NOISE,
                                     "STEPS_PER_CELL": STEPS_PER_CELL,
                                     "SEEDS": SEEDS,
                                     "ANCHOR_SEEDS": ANCHOR_SEEDS}},
        "errs": {("%g|%s" % (g, s)): errs[(g, s)]
                 for g in GLADDER for s in (False, True)},
        "shape": detail["shape"], "hill": detail["hill"],
        "linear_r2": r2_lin,
        "discipline": detail["discipline"],
        "anchor_bit_exact": True,
        "gates": verdicts,
        "verdict": "%s+%s" % (detail["shape"],
                              "MEMORY-DISCIPLINE-VIABLE" if viable
                              else "MEMORY-DISCIPLINE-COSTLY"),
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP411 VERDICT: %s %s+%s" % (verdicts, detail["shape"],
                                        "MEMORY-DISCIPLINE-VIABLE" if viable
                                        else "MEMORY-DISCIPLINE-COSTLY"))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
