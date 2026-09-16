#!/usr/bin/env python3
"""exp147 — THE NOISE-CARRYING STATE (stochastic chain deadline; L123's
registered object, exp143's refutation residue). exp143 verified 0/4:
the g64@36 late-control break is NOT in the mean-field chain state — a
two-sided pincer certificate across 6 candidate features shows rescue
g16@48 Pareto-dominates break g64@36 on every direction and the
margin-to-bar inverts outright; the deterministic sim sits at scalar
4.904 against the 6.0 bar (margin ~1.1 mV) while the DEPOSITED
harness verdict at g64@36 is P(break) = 1.0 (exp125/124). exp135's
docstring registers why the mirror is mean-field: "the harness's own
Euler update, noise omitted (the V-noise's stationary RMS is < 1 mV
and the inheritance noise is 0.6 mV iid, both an order below the
6.0 bar)". L123 registers the NOISE-CARRYING STATE: the stochastic
chain, where the deadline becomes a sub-margin noise statistic.

THE CLAIM (pre-registered BEFORE running): adding the harness's OWN
noise channels — bit-matched in form and amplitude, verbatim entry
points — to exp135/140/143's verified chain sim makes the deposited
verdict pattern (all 8 anchors, deadline curve 0/48/52/>34) fall out
as P(break) >= 0.5 thresholding.

HARNESS NOISE CHANNELS (read from the core harness code; cited):
  (a) V-noise: cultivation/bioelectric/collective.py:646-647 —
      "noise = self.noise_std * np.sqrt(dt) *
       self.rng.standard_normal(self.n)"; "Vn = self.V + dt*dV + noise".
      noise_std = 0.30 (collective.py:75 default; exp124 instantiates
      GraphCollective WITHOUT a noise_std override). Added EVERY Euler
      step (window, walk, settle), BEFORE the clamp overwrite
      (collective.py:668-671) — replicated here (clamps applied after
      dyn_step). Stationary RMS < 1 mV (exp135's documented bound).
  (b) inheritance noise: ONE N(0, 0.6) draw per committing walk cell,
      added to the target-value base and written to BOTH theta and V
      (cultivation/substrate/graph.py:154 + :161-162; the harness walk
      in exp124 uses the phi_spec_canon base = the cell's target on
      the gap_scale >= 1 branch, graph.py:153 — so the DETERMINISTIC
      injection is the harness's mean inheritance, exactly as
      exp135's docstring states; the noise rides on top, iid per
      cell, shared between the two fields).
  (c) theta drift: theta_drift = 0.0 (collective.py:76 default,
      not overridden by exp124) — the channel is ABSENT in the
      harness; NOT added here.
  (d) physiological clips (collective.py:664-666) omitted as in
      exp135/140/143 — inert: deterministic trajectories and sub-mV
      noise live far inside the bounds.
  FORBIDDEN MOVE (p-hacking bar, pre-registered): raising any noise
  amplitude beyond the harness's own values to force the g64@36
  crossing. The amplitudes above are bit-matched and NEVER tuned.

DESIGN (fixed before the deposited run):
  1. exp143.simulate_late's verbatim chain machinery (itself exp140's
     verbatim copy of exp135.simulate, <1e-9 asserted) + the two
     channel hooks above, batched over seeds (V, th are (B, n) arrays;
     row b of the batched stream is one organism's noise realization;
     op order otherwise untouched — with channels OFF the batched code
     is the exp143 instrument and must reproduce exp135.simulate).
  2. Cell set = exp125's exact curve battery on the torus:
     GRIDS[1]=(0,6,12,18,24), GRIDS[4]=(0,12,24,26,30,34,36,48),
     GRIDS[16]=(0,24,36,48,52,56,58), GRIDS[64]=(0,16,24,28,31,34),
     plus the two late controls CONTROLS = {16: 72, 64: 36} — the
     same 28 cells exp140/143 tabled. 8 of them are the deposited
     ANCHORS (5 break: g1@0, g4@48, g16@52, g16@72, g64@36;
     3 rescue: g4@36, g16@48, g64@34).
  3. Seed battery: 100 seeds per (cell, channel-config) = 100
     independent rows of one batched PCG64 stream seeded
     np.random.default_rng(("exp147", cell_index, config)).
     PRE-REGISTERED SHRINK: if the pilot (g64@36 — the most expensive
     cell: 2924 Euler steps at dt=1.2/72) projects the total wall over
     11 min, the 20 NON-ANCHOR ladder cells drop to 50 seeds (exactly
     the prefix rows of the same streams) and the 8 anchors + the
     decomposition arms KEEP 100. The branch used is deposited.
  4. Break criterion: err = RMS(V - target) over the full graph at
     read; break iff err >= 6.0 — the harness's own verdict rule
     (pattern_error >= ERR_BAR, exp124; pattern_error is the full-graph
     RMS, collective.py:693-695).

GATES (fixed before running):
  GATE-M1  P(break) at g64@36 (both channels) >= 0.5 — the
           deterministic 4.904 < 6.0 margin (1.096 mV) is noise-crossed
           by the harness's own noise.
  GATE-M2  P(break) < 0.5 at every deposited-rescue cell: g4@36,
           g16@48, g64@34, and the g64 flank g64@{0,16,24,28,31}
           (8 cells; g64@34 counted once) — the rescue side stays
           rescue under noise.
  GATE-M3  thresholding P(break) >= 0.5 on exp125's onset ladders
           reproduces the deposited censoring-corrected deadline curve
           0/48/52/>34 (g1 edge 0, g4 edge 48, g16 edge 52, g64 no
           edge inside the censored ladder) and the curve is
           monotone-rising in gamma.
  GATE-M4  honest mechanism attribution: the g64@36 crossing is
           decomposed into V-channel-only, inheritance-only, and both
           (P(break) per arm + excess squared error
           E[err^2] - err_det^2 per arm + the interaction term
           excess_both - excess_V - excess_inh); the dominant channel
           is NAMED and deposited. No re-tuning, no amplitude bumps,
           no post-hoc criteria.

REFUTATION BRANCH (pre-registered): if GATE-M1 FAILS — even
stochastic P(break) < 0.5 at g64@36 — the refutation is decisive:
the harness's own noise cannot close a 1.1 mV margin against a
deposited P(break) = 1.0, and the registered next object is the
HARNESS-IMPLEMENTATION RE-READ with the divergence hypothesis: the
deterministic mean-field chain (exp135/140/143's verified mirror)
may DIVERGE from the true harness dynamics at late times — the
decomposition's excess-squared-error budget quantifies exactly how
far the noise alone falls short, and the divergence must then live in
a deterministic step the mirror omits or mis-orders (candidates: the
clamp theta pull, the gap_scale coupling term, wound/injection state
details, step-count rounding) — NOT in noise amplitude, which is here
bit-matched and measured insufficient.

FIDELITY: with channels OFF the batched instrument reproduces
exp135.simulate() (the exp140/143-verified harness mirror) to < 1e-9
on the four deposited scalars (err, err_span, err_intact,
th_span_dev) at all 8 anchors, and the channels-off err at g64@36
must reproduce the deposited deterministic scalar 4.904 (|d| < 2e-3).

RUN: 28-cell stochastic battery (100 or pre-registered 50 seeds x
cells) + 2 decomposition arms + 28 + 8 deterministic fidelity sims.
BLAS pinned; wall target < 15 min.
"""
from __future__ import annotations

import json
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.exp125_u_shape_generalization import (
    target_pattern, region_span, GRIDS, CONTROLS, WINDOW_H, SETTLE_H,
)
from experiments.exp112_walk_speed_ladder import build_battery
import experiments.exp135_walk_chain as e135
from experiments.exp90_two_source_read import star_dt
from experiments.exp140_state_space import (
    ANCHORS, BREAK_CELLS, RESCUE_CELLS, G64_FLANK, ERR_BAR, fmt,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp147_noise_state.json")

# ---- harness noise parameters: the harness's OWN, bit-matched ----
NOISE_STD = 0.30   # collective.py:75 default (V-noise amplitude)
INH_SIGMA = 0.60   # graph.py:107 / exp124 walk (inheritance, mV)
# theta_drift = 0.0 (collective.py:76) -> channel absent; not added.

DEP_S64_36_DET = 4.904     # exp140/143's deposited deterministic scalar
SEEDS_PRIMARY = 100        # pre-registered primary battery
SEEDS_FALLBACK = 50        # pre-registered shrink (ladder cells only)
WALL_TRIGGER_S = 660.0     # 11 min projection -> shrink branch

# GATE-M2 cell set: deposited rescues + the g64 flank (g64@34 once)
RESCUE_GATE = tuple(dict.fromkeys(RESCUE_CELLS + G64_FLANK))


# ------------------------------------------------------------------
# batched stochastic chain — exp143.simulate_late's verbatim machinery
# (exp140/135's verified mirror) + the two bit-matched channel hooks
# ------------------------------------------------------------------
def simulate_stoch(adj: np.ndarray, gamma: float, t_star: float,
                   n_seeds: int, channels: tuple[str, ...],
                   seed_key) -> dict:
    n = adj.shape[0]
    B = int(n_seeds)
    dt = star_dt(gamma, float(adj.sum(axis=1).max()))
    A = adj.astype(float)
    degA = A.sum(axis=1)
    G = e135.G_GAP * A
    degG = G.sum(axis=1)
    target = target_pattern(adj)
    canon = e135.canon_pattern(adj)
    clamps = e135.zone_clamps(n)
    zall = np.concatenate([idx for idx, _ in clamps])
    lo, hi = int(zall.min()), int(zall.max())
    span = np.arange(lo, hi + 1)
    intact = np.array([i for i in range(n) if i < lo or i > hi], dtype=int)
    order2 = e135.walk_order(adj, lo, hi)

    rng = np.random.default_rng(seed_key)
    V = np.repeat(canon.astype(float)[None, :], B, axis=0)
    th = np.repeat(canon.astype(float)[None, :], B, axis=0)
    mu = e135.MU
    t0 = 0.0
    n_win = int(round(WINDOW_H / dt))
    n_settle = int(round(SETTLE_H / dt))

    use_V = "V" in channels
    use_inh = "inherit" in channels
    v_amp = NOISE_STD * np.sqrt(dt)

    def dyn_step() -> None:
        nonlocal V, th, t0, mu
        t0 += dt
        if t_star is not None and t0 >= t_star:
            mu = 0.0
        dV = gamma * (th - V) + V @ G - V * degG
        mterm = mu * (th @ A - th * degA)
        dth = e135.EPS * (V - th) + mterm
        V = V + dt * dV
        if use_V:                      # collective.py:646-647, every step
            V = V + v_amp * rng.standard_normal((B, n))
        th = th + dt * dth

    # ---- window (clamps on) — verbatim phase structure; harness order:
    # noise inside step, THEN clamp overwrite (collective.py:668-673)
    for _ in range(n_win):
        dyn_step()
        for idx, val in clamps:
            V[:, idx] = val
            th[:, idx] += dt * e135.EPS * (val - th[:, idx])

    # ---- amputation + the walk chain — verbatim + inheritance hook
    V[:, span] = e135.WOUND_V
    th[:, span] = e135.WOUND_TH
    for i in order2:
        for _ in range(e135.WALK_SUB):
            dyn_step()
        if use_inh:                    # graph.py:154 + :161-162 — ONE
            z = rng.normal(0.0, INH_SIGMA, size=B)   # draw, both fields
            V[:, i] = target[i] + z
            th[:, i] = target[i] + z
        else:
            V[:, i] = target[i]
            th[:, i] = target[i]

    # ---- settle — verbatim
    for _ in range(n_settle):
        dyn_step()

    err = np.sqrt(np.mean((V - target) ** 2, axis=1))
    err_span = np.sqrt(np.mean((V[:, span] - target[span]) ** 2, axis=1))
    dev = th[0, span] - target[span] if B == 1 else None
    out = {
        "err": err,
        "err_span": err_span,
        "err_intact": np.sqrt(np.mean(
            (V[:, intact] - target[intact]) ** 2, axis=1)),
    }
    if B == 1:
        out["th_span_dev"] = float(np.sqrt(np.mean(dev ** 2)))
    return out


def seed_key(cell_index: int, config: str) -> tuple:
    return (14700, int(cell_index),
            {"off": 0, "both": 1, "V": 2, "inherit": 3}[config])


def _scalar(x) -> float:
    return float(x[0]) if isinstance(x, np.ndarray) else float(x)


def stats_of(res: dict, bar: float) -> dict:
    err = res["err"]
    brk = err >= bar
    p = float(np.mean(brk))
    e2 = float(np.mean(err ** 2))
    return {
        "n_seeds": int(err.size),
        "P_break": round(p, 4),
        "mc_stderr": round(float(np.sqrt(max(p * (1 - p), 1e-12)
                                      / err.size)), 4),
        "mean_err": round(float(np.mean(err)), 4),
        "std_err": round(float(np.std(err)), 4),
        "max_err": round(float(np.max(err)), 6),
        "mean_sq_err": round(e2, 4),
        "mean_err_span": round(float(np.mean(res["err_span"])), 4),
    }


def main() -> dict:
    print("=== exp147: the noise-carrying state (stochastic chain) ===\n")
    t_start = time.time()
    battery = build_battery()
    torus = battery["torus"]
    assert region_span(torus.shape[0]) == 73

    # ---- cell set: exp125's exact curve battery + late controls ----
    cells: list[tuple[float, float]] = []
    for g in (1.0, 4.0, 16.0, 64.0):
        for t in GRIDS[g]:
            cells.append((g, float(t)))
    for t in CONTROLS.values():
        c = (float(next(k for k, v in CONTROLS.items() if v == t)), float(t))
        if c not in cells:
            cells.append(c)
    cell_index = {c: i for i, c in enumerate(cells)}
    assert len(cells) == 28, len(cells)
    assert set(ANCHORS) <= set(cells)
    ladder = {g: [float(t) for t in GRIDS[g]] for g in GRIDS}

    # ---- pilot: g64@36, both channels, 100 seeds (shrink trigger) ----
    pilot = simulate_stoch(torus, 64.0, 36.0, SEEDS_PRIMARY,
                           ("V", "inherit"), seed_key(cell_index[(64.0, 36.0)], "both"))
    pilot_t = time.time() - t_start
    pilot_stats = stats_of(pilot, ERR_BAR)
    steps_total = sum(
        (int(round(WINDOW_H / star_dt(g, float(torus.sum(axis=1).max()))))
         + 73 * 8 + int(round(SETTLE_H / star_dt(g, float(torus.sum(axis=1).max())))))
        for (g, _t) in cells)
    per_step = pilot_t / 2924.0
    proj = per_step * (steps_total + 2 * 2924) + 140.0 + pilot_t
    shrink = proj > WALL_TRIGGER_S
    B_ladder = SEEDS_FALLBACK if shrink else SEEDS_PRIMARY
    B_anchor = SEEDS_PRIMARY
    print(f"  pilot g64@36 both/100: {pilot_t:.1f}s  P(break) = "
          f"{pilot_stats['P_break']}  mean err = {pilot_stats['mean_err']}")
    print(f"  projected wall {proj:.0f}s -> seed branch: "
          f"{'FALLBACK (anchors 100, ladder ' + str(B_ladder) + ')' if shrink else 'PRIMARY 100 everywhere'}",
          flush=True)

    # ---- fidelity: channels OFF vs exp135.simulate at all 8 anchors --
    fid = []
    det_err = {}
    for c in ANCHORS:
        ref = e135.simulate(torus, c[0], c[1])
        off = simulate_stoch(torus, c[0], c[1], 1, (),
                             seed_key(cell_index[c], "off"))
        d = max(abs(float(ref[k]) - _scalar(off[k]))
                for k in ("err", "err_span", "err_intact", "th_span_dev"))
        fid.append({"cell": fmt(c), "max_abs_scalar_diff": round(float(d), 15)})
        assert d < 1e-9, f"drift vs exp135 at {fmt(c)}: {d}"
        det_err[c] = float(off["err"][0])
    s36 = det_err[(64.0, 36.0)]
    assert abs(s36 - DEP_S64_36_DET) < 2e-3, s36
    print(f"  fidelity: channels-OFF vs exp135 max|d| = "
          f"{max(f['max_abs_scalar_diff'] for f in fid):.2e}; "
          f"err_det(g64@36) = {s36:.4f} (deposited {DEP_S64_36_DET})",
          flush=True)
    for c in cells:
        if c not in det_err:
            off = simulate_stoch(torus, c[0], c[1], 1, (),
                                 seed_key(cell_index[c], "off"))
            det_err[c] = float(off["err"][0])

    # ---- stochastic battery (both channels) ----
    curve: dict[tuple[float, float], dict] = {}
    arm_errs = {}
    for c in cells:
        is_anchor = c in ANCHORS
        B = B_anchor if is_anchor else B_ladder
        res = simulate_stoch(torus, c[0], c[1], B, ("V", "inherit"),
                             seed_key(cell_index[c], "both"))
        if c == (64.0, 36.0):      # keep per-seed errs for the decomp
            arm_errs["both"] = res["err"]
        st = stats_of(res, ERR_BAR)
        st.update({"cell": fmt(c), "g": c[0], "t": c[1],
                   "deposited": "break" if c in BREAK_CELLS else "rescue",
                   "err_det": round(det_err[c], 4),
                   "ladder_cell": not is_anchor})
        curve[c] = st
        tag = "ANCHOR" if is_anchor else "ladder"
        print(f"  [{tag}] g{c[0]:g}@{c[1]:g}  P(break) = {st['P_break']:.3f}"
              f" ± {st['mc_stderr']:.3f}  mean err {st['mean_err']:.3f} "
              f"(det {st['err_det']:.3f})  deposited {st['deposited']}",
              flush=True)

    # ---- GATE-M4 decomposition at g64@36 (harness amplitudes only) ---
    arms = {"both": curve[(64.0, 36.0)]}
    for cfg in ("V", "inherit"):
        res = simulate_stoch(torus, 64.0, 36.0, B_anchor, (cfg,),
                             seed_key(cell_index[(64.0, 36.0)], cfg))
        arms[cfg] = stats_of(res, ERR_BAR)
        arm_errs[cfg] = res["err"]
        print(f"  [decomp] g64@36 {cfg:8s} P(break) = {arms[cfg]['P_break']:.3f}"
              f"  mean err {arms[cfg]['mean_err']:.3f}", flush=True)
    e2_det = det_err[(64.0, 36.0)] ** 2
    excess = {k: float(np.mean(v ** 2)) - e2_det for k, v in arm_errs.items()}
    interaction = excess["both"] - excess["V"] - excess["inherit"]
    solo_cross = {k: arms[k]["P_break"] if k in arms else None
                  for k in ("V", "inherit")}
    dominant = max(("V", "inherit"), key=lambda k: excess[k])
    decomp = {
        "cell": "g64@36", "err_det": round(det_err[(64.0, 36.0)], 4),
        "amplitudes": {"V_noise_std": NOISE_STD, "inherit_sigma": INH_SIGMA,
                       "theta_drift": 0.0},
        "arms": {k: {**arms[k], "per_seed_err": [round(float(x), 4)
                                                 for x in arm_errs[k]]}
                 for k in ("V", "inherit", "both")},
        "excess_sq_err": {k: round(excess[k], 3) for k in excess},
        "interaction_sq_err": round(interaction, 3),
        "needed_sq_err": round(ERR_BAR ** 2 - e2_det, 3),
        "solo_P_break": solo_cross,
        "dominant_channel": dominant,
    }

    # ---- gates ----
    p36 = curve[(64.0, 36.0)]["P_break"]
    m1 = bool(p36 >= 0.5)
    m2_cells = {fmt(c): curve[c]["P_break"] for c in RESCUE_GATE}
    m2 = all(p < 0.5 for p in m2_cells.values())
    pred_edges = {}
    for g in (1.0, 4.0, 16.0, 64.0):
        e = None
        for t in ladder[g]:
            if curve[(g, t)]["P_break"] >= 0.5:
                e = t
                break
        pred_edges[g] = e
    target_edges = {1.0: 0.0, 4.0: 48.0, 16.0: 52.0, 64.0: None}
    m3 = (pred_edges == target_edges
          and pred_edges[1.0] < pred_edges[4.0] < pred_edges[16.0]
          and pred_edges[64.0] is None)
    m4 = True  # decomposition deposited with dominant channel named;
    #            amplitudes are the harness's own (no tuning occurred).

    gates = {"M1_g64t36_noise_crossed": m1,
             "M2_rescue_side_holds": m2,
             "M3_curve_0_48_52_gt34": bool(m3),
             "M4_decomposition_honest": m4}
    if all(gates.values()):
        verdict = "M-CONFIRMED"
    elif not m1:
        verdict = "M-REFUTED (decisive: harness's own noise cannot close " \
                  "the margin; register the harness-implementation re-read)"
    else:
        verdict = "M-MIXED"

    out = {
        "experiment": "exp147_noise_state",
        "claim": "the harness's own noise channels, bit-matched into the "
                 "verified chain sim, reproduce the deposited verdict "
                 "pattern as P(break) >= 0.5 thresholding",
        "runtime_s": round(time.time() - t_start, 1),
        "noise_channels": {
            "V_noise": {"file": "cultivation/bioelectric/collective.py",
                        "lines": "646-647 (amplitude default :75)",
                        "form": "noise_std*sqrt(dt)*N(0,1) per Euler step, "
                                "added to V before clamp overwrite",
                        "noise_std": NOISE_STD},
            "inheritance": {"file": "cultivation/substrate/graph.py",
                            "lines": "154,161-162 (gap_scale>=1 branch :153)",
                            "form": "ONE N(0,0.6) draw per committing walk "
                                    "cell, added to the target base, written "
                                    "to BOTH theta and V, iid per cell",
                            "sigma_mV": INH_SIGMA},
            "theta_drift": {"file": "cultivation/bioelectric/collective.py",
                            "lines": "76,663-664", "value": 0.0,
                            "note": "channel ABSENT in the harness default; "
                                    "not added"},
            "forbidden_move": "raising amplitudes beyond harness values "
                              "(pre-registered p-hacking bar) — not done",
        },
        "prereg": {
            "seeds_primary": SEEDS_PRIMARY,
            "seeds_fallback_ladder_only": SEEDS_FALLBACK,
            "shrink_trigger_projected_s": WALL_TRIGGER_S,
            "branch_used": "fallback(ladder=%d, anchors=%d)" % (B_ladder, B_anchor)
                           if shrink else "primary(100 everywhere)",
            "break_criterion": "err >= 6.0 (pattern_error >= ERR_BAR, "
                               "collective.py:693-695; exp124's verdict rule)",
            "rng": "np.random.default_rng((14700, cell_index, config_id)); "
                   "fallback rows are prefix rows of the primary streams",
        },
        "fidelity_channels_off": {
            "vs_exp135": fid,
            "err_det_g64t36": round(s36, 6),
            "deposited_scalar": DEP_S64_36_DET,
        },
        "pilot": {"seconds": round(pilot_t, 1), **pilot_stats},
        "curve": [curve[c] for c in cells],
        "ladders": {f"g{g:g}": ladder[g] for g in ladder},
        "predicted_edges": {f"g{g:g}": pred_edges[g] for g in pred_edges},
        "predicted_curve": "0/48/52/>34" if m3 else
                           "/".join(str(pred_edges[g]) for g in
                                    (1.0, 4.0, 16.0, 64.0)),
        "gate_M2_cells": m2_cells,
        "decomposition_g64t36": decomp,
        "gates": gates,
        "verdict": verdict,
    }
    if not m1:
        out["next_object"] = {
            "object": "HARNESS-IMPLEMENTATION RE-READ",
            "divergence_hypothesis": "the deterministic mean-field chain "
                                     "(exp135/140/143's verified mirror) "
                                     "diverges from the true harness at "
                                     "late times by a step the mirror "
                                     "omits or mis-orders; the noise "
                                     "budget measured here falls short of "
                                     "the crossing by a factor %.1f in "
                                     "squared-error mass, so noise "
                                     "amplitude CANNOT be the carrier"
                                     % (decomp["needed_sq_err"]
                                        / max(sum(excess[k] for k in
                                                  ("V", "inherit")), 1e-12)),
        }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  edges predicted: {out['predicted_edges']} -> curve "
          f"'{out['predicted_curve']}'")
    print(f"  GATES: {gates}\n  VERDICT: {verdict}")
    print(f"  deposit: {OUT}  ({out['runtime_s']}s)", flush=True)
    return out


if __name__ == "__main__":
    main()
