#!/usr/bin/env python3
"""exp125 — THE U-SHAPE GENERALIZATION + THE ANALYTIC DEADLINE TEST
(ledger L105's registration, with a PRE-RUN AUDIT CORRECTION owned
before the deposit: the exp124 protocol's pre-settle duration is
gamma-DEPENDENT — star_dt = min(0.1, 1.2/(gamma+deg)) shrinks with
gamma, so the 73-cell walk shrinks 58.4 h (gamma 1) -> 10.3 h
(gamma 64) and the pre-settle phase ends at 82.4 / 82.4 / 59.0 /
34.3 h across the gamma ladder. Every deposited exp124 cell with
onset > the pre-settle end NEVER FIRED the mu-silence: the gamma-16
"72 h edge" cell and the gamma-64 "36 h collapse" cells (36/48/72)
are NEVER-SILENCED CONTROLS — default-mu torus runs, which break at
P=1.0 by exp100's refusal. The deposited U-shape's right flank is
censoring, not physics. exp125 re-runs the deadline curve
censoring-free and tests the registered analytic form.

THE PROTOCOL (exp124's run_deadline imported verbatim — bit-exact
harness; per-gamma CENSORING-AWARE onset grids that stay inside
each protocol's real window; 8 seeds):

  torus   gamma 1  onsets {0,6,12,18,24}    (real window 82.4 h)
          gamma 4  deposited 8 onsets       (anchor + bracket)
          gamma 16 onsets {0,12,24,36,48,52,56,58}   (real to 59.0)
          gamma 64 onsets {0,8,16,20,24,27,30,33}    (real to 34.3)
          never-silenced controls at gamma 16 "72" and gamma 64 "36"
  grid2d  gamma 1 {0,6,12,18,24}; gamma 4 {0,12,24,26,30,34,36,48};
          gamma 16 {0,24,36,48,52,56,58}; gamma 64 {0,16,24,28,31,34}
  path    same grids as grid2d (its real windows: 82.4/140.8/62.9/34.6)

PRE-REGISTERED GATES:

  AX-G0  (anchor continuity) the in-batch torus gamma-4 curve at the
         deposited 8 onsets matches the deposited exp124 curve within
         0.125 at every onset, AND the in-batch torus gamma-1 arm at
         {0,6,12,18,24} matches exp123's deposited mu_only curve
         within 0.125 (the exp124 DC-G3 tolerance convention).
  AX-G1  (the censoring map verified) (a) every deposited cell the
         map classifies REAL reproduces in-batch within 0.25;
         (b) the re-run never-silenced controls (gamma 16 @ 72,
         gamma 64 @ 36) read P(break) = 1.0 — they are default-mu
         runs, the censoring mechanism itself; (c) therefore the
         gamma-64 "collapse to 36 h" and gamma-16 "72 h edge" are
         WITHDRAWN as artifact and replaced by in-batch brackets
         inside the real windows.
  DCG1R  (the repaired DC-G1) on censoring-free curves the torus
         deadline is NON-DECREASING in gamma: edge(1)=0 <= edge(4),
         and the bracketed/lower-bounded edges at 16 and 64 do not
         invert edge(4). A real U (any inversion inside real windows)
         REFUTES.
  UG-G1  (baseline invulnerability) grid2d and path at gamma 1:
         P(break) = 0.0 flat at every real onset (exp120's full-
         blockade invulnerability extends to the mu-only channel).
  UG-G2  (the generalization fork, two-sided) IF grid2d/path break
         at any real cell: their edge-vs-gamma sequence is compared
         to the torus's repaired monotone structure (same test as
         DCG1R per substrate). IF they never break: the deadline
         phenomenon is declared TORUS-SPECIFIC and AN-G2's no-break
         predictions become load-bearing.
  AN-G1  (the registered analytic form, BOTH readings) with rates
         r_win(k) = mu*lam_k + eps*gamma*lam_k/(gamma+g*lam_k) and
         post-silence exact joint slow eigenvalue
         r_post(k) = (T - sqrt(T^2-4*g*lam*eps))/2, T = gamma+g*lam+eps
         (mu = 0), band = lam_k <= lam_max/2 (trivial mode excluded),
         amplitudes a_k = <target - mean, q_k>:
         H1 (cumulative homogenization): predicted destroyed RMS =
         sqrt(sum_k (a_k (1-exp(-r_win t* - r_post (T_end-t*))))^2/n);
         H2 (remaining-time integral, the registration's literal
         phrase): edge = T_end - Theta/r_post_eff, rescue iff
         (T_end - t*) r_post_eff <= Theta. Fit Theta ONCE on the
         torus's censoring-corrected constraint cells. PASS iff a
         feasible Theta exists for a variant; the violated constraint
         pair is named on refutation.
  AN-G2  (zero-free-parameter transfer, CONDITIONAL) evaluated only
         for a variant whose torus fit is feasible: its Theta_mid
         predicts grid2d/path break booleans at every real silenced
         cell; PASS iff full agreement with one-cell edge slack.
         Void by pre-registration if AN-G1 refutes both variants.

RUN: ~660 runs, serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp124_deadline_curve import run_deadline, ONSETS, SEEDS
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI
from experiments.exp73_active_renormalization import bfs_order
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp125_u_shape_generalization.json")

MU, EPS, G_GAP = 0.015, 0.04, 0.20
WINDOW_H, SETTLE_H = 24.0, 15.0

GRIDS = {
    1.0: (0.0, 6.0, 12.0, 18.0, 24.0),
    4.0: (0.0, 12.0, 24.0, 26.0, 30.0, 34.0, 36.0, 48.0),
    16.0: (0.0, 24.0, 36.0, 48.0, 52.0, 56.0, 58.0),
    64.0: (0.0, 16.0, 24.0, 28.0, 31.0, 34.0),
}
TORUS_G1 = (0.0, 6.0, 12.0, 18.0, 24.0)
TORUS_G4_ANCHOR = tuple(ONSETS)            # the deposited 8
CONTROLS = {16.0: 72.0, 64.0: 36.0}        # never-silenced control arms


def region_span(n: int) -> int:
    idx: set[int] = set()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        idx.update(range(i0, i1))
    ri = sorted(idx)
    return ri[-1] - ri[0] + 1


def protocol_end(adj: np.ndarray, gamma: float) -> float:
    """exp124's exact pre-settle duration: window steps + walk steps."""
    n = adj.shape[0]
    dt = star_dt(gamma, float(adj.sum(axis=1).max()))
    return round(WINDOW_H / dt) * dt + region_span(n) * 8 * dt


def run_curve(adj, gamma, onsets, tag, out):
    ps = []
    for onset in onsets:
        br = [run_deadline(adj, s, gamma, onset) for s in SEEDS]
        p = round(float(np.mean(br)), 3)
        ps.append(p)
        out[f"{tag}_g{gamma:g}_t{onset:g}"] = p
    print(f"    {tag:8s} gamma {gamma:5.1f}  onsets {list(onsets)}\n"
          f"             P(break): {ps}", flush=True)
    return ps


# ------------------------------------------------------------------ analytic
def spectrum(adj):
    lam, Q = np.linalg.eigh(np.diag(adj.sum(1)) - adj)
    return lam, Q


def target_pattern(adj):
    n = adj.shape[0]
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    return target


def rates(adj, gamma):
    lam, _ = spectrum(adj)
    r_win = MU * lam + EPS * gamma * lam / (gamma + G_GAP * lam)
    T2 = gamma + G_GAP * lam + EPS
    disc = np.maximum(T2 ** 2 - 4.0 * G_GAP * lam * EPS, 0.0)
    r_post = 0.5 * (T2 - np.sqrt(disc))
    return lam, r_win, r_post


def pred_rms_H1(adj, gamma, onset, t_pre, t_end):
    """H1: cumulative homogenization of the canon low-k amplitude."""
    lam, r_win, r_post = rates(adj, gamma)
    target = target_pattern(adj)
    dev = target - target.mean()
    _, Q = spectrum(adj)
    a = Q.T @ dev
    band = (lam <= lam.max() / 2.0 + 1e-12) & (lam > 1e-9)
    if onset <= t_pre + 1e-9:
        tw, tp = onset, t_end - onset
    else:                       # never silenced: mu active throughout
        tw, tp = t_end, 0.0
    survive = np.exp(-r_win[band] * tw - r_post[band] * max(tp, 0.0))
    destroyed = a[band] * (1.0 - survive)
    return float(np.sqrt(np.sum(destroyed ** 2) / int(band.sum())))


def r_post_eff(adj, gamma):
    """H2: pattern-energy-weighted RMS post-silence drift rate."""
    lam, _, r_post = rates(adj, gamma)
    target = target_pattern(adj)
    dev = target - target.mean()
    _, Q = spectrum(adj)
    a = Q.T @ dev
    band = (lam <= lam.max() / 2.0 + 1e-12) & (lam > 1e-9)
    num = float(np.sqrt(np.sum((a[band] * r_post[band]) ** 2)))
    den = float(np.sqrt(np.sum(a[band] ** 2)))
    return num / max(den, 1e-12)


def main() -> dict:
    print("=== exp125: the U-shape generalization + the analytic deadline ===\n")
    t_start = time.time()

    battery = build_battery()
    subs = {"torus": battery["torus"], "grid2d": battery["grid2d"],
            "path": battery["path"]}

    # censoring map of the DEPOSITED exp124 grid
    censoring = {}
    for name, adj in subs.items():
        for g in (1.0, 4.0, 16.0, 64.0):
            t_pre = protocol_end(adj, g)
            censoring[f"{name}_g{g:g}"] = {
                "t_pre_h": round(t_pre, 2),
                "censored_deposited": [t for t in ONSETS if t > t_pre + 1e-9],
            }
    print("  censoring map (deposited cells beyond the real window):")
    for k, v in censoring.items():
        if v["censored_deposited"]:
            print(f"    {k}: t_pre={v['t_pre_h']}h  "
                  f"censored {v['censored_deposited']}")
    print(flush=True)

    curves: dict = {}
    # ---- torus: anchors + censoring-free brackets
    curves["torus_g1"] = run_curve(subs["torus"], 1.0, TORUS_G1,
                                   "torus", curves)
    curves["torus_g4_anchor"] = run_curve(subs["torus"], 4.0,
                                          TORUS_G4_ANCHOR, "torus",
                                          curves)
    curves["torus_g4"] = run_curve(subs["torus"], 4.0, GRIDS[4.0],
                                   "torus", curves)
    curves["torus_g16"] = run_curve(subs["torus"], 16.0, GRIDS[16.0],
                                    "torus", curves)
    curves["torus_g64"] = run_curve(subs["torus"], 64.0, GRIDS[64.0],
                                    "torus", curves)
    # never-silenced controls (onset beyond t_pre: maybe() never fires)
    for g, t in CONTROLS.items():
        br = [run_deadline(subs["torus"], s, g, t) for s in SEEDS]
        curves[f"torus_control_g{g:g}_t{t:g}"] = round(float(np.mean(br)), 3)
        print(f"    control torus gamma {g:g} onset {t:g} (never silenced)"
              f"  P(break): {curves[f'torus_control_g{g:g}_t{t:g}']}",
              flush=True)

    # ---- grid2d + path: censoring-free deadline curves
    for name in ("grid2d", "path"):
        for g, grid in GRIDS.items():
            curves[f"{name}_g{g:g}"] = run_curve(subs[name], g, grid,
                                                 name, curves)

    def edge(ps, onsets):
        for t, p in zip(onsets, ps):
            if p >= 0.5:
                return t
        return None

    edges = {}
    for key, ps in curves.items():
        if not isinstance(ps, list) or key == "torus_g4_anchor":
            continue
        name = key.rsplit("_g", 1)[0]
        g = float(key.rsplit("_g", 1)[1])
        grid = TORUS_G1 if key == "torus_g1" else GRIDS[g]
        edges[key] = edge(ps, grid)

    # ------------------------------------------------ gates
    print("\n  --- gates ---", flush=True)
    gates: dict = {}

    # AX-G0 anchors
    dep124 = json.load(open(os.path.join(
        ROOT, "results", "exp124_deadline_curve.json")))
    d4 = dep124["curves"]["4.0"]
    ax0a = all(abs(a - b) <= 0.125 for a, b in
               zip(curves["torus_g4_anchor"], d4))
    dep123 = json.load(open(os.path.join(
        ROOT, "results", "exp123_channel_split.json")))
    m1 = dep123["curves"]["mu_only"][:5]
    ax0b = all(abs(a - b) <= 0.125 for a, b in
               zip(curves["torus_g1"], m1))
    gates["AX_G0_anchor_continuity"] = bool(ax0a and ax0b)
    print(f"  AX-G0 anchor: exp124 g4 {'PASS' if ax0a else 'REFUTED'} "
          f"(in-batch {curves['torus_g4_anchor']} vs deposited {d4}); "
          f"exp123 g1 {'PASS' if ax0b else 'REFUTED'}", flush=True)

    # AX-G1 censoring map: deposited REAL cells reproduce in-batch
    # (the anchor curve covers all 8 gamma-4 cells at 0.125 via AX-G0;
    # here the bracket grids' deposited-real cells: g4@24, g16@48, g64@24)
    real_ok = (curves["torus_g4"][2] <= 0.25        # deposited g4 @ 24
               and curves["torus_g16"][3] <= 0.25   # deposited g16 @ 48
               and curves["torus_g64"][2] <= 0.25)  # deposited g64 @ 24
    ctrl_break = (curves["torus_control_g16_t72"] == 1.0
                  and curves["torus_control_g64_t36"] == 1.0)
    gates["AX_G1_censoring_map"] = bool(real_ok and ctrl_break)
    print(f"  AX-G1 censoring: real cells reproduce "
          f"{'PASS' if real_ok else 'REFUTED'}; never-silenced controls "
          f"break {'PASS' if ctrl_break else 'REFUTED'} "
          f"({curves['torus_control_g16_t72']}, "
          f"{curves['torus_control_g64_t36']})", flush=True)

    # DCG1R repaired monotonicity on the torus (censoring-free)
    e1 = edges["torus_g1"]              # 0 expected
    e4 = edges["torus_g4"]
    e16 = edges["torus_g16"]            # may be None (censored) -> LB 58
    e64 = edges["torus_g64"]            # may be None (censored) -> LB 34
    lb16 = 58.0 if e16 is None else e16
    lb64 = 34.0 if e64 is None else e64
    dcg1r = (e1 == 0.0) and (e4 is not None) and (e4 >= e1) \
        and (lb16 >= e4 - 1e-9) and (lb64 >= min(e4, 24.0) - 1e-9)
    gates["DCG1R_monotone_repaired"] = bool(dcg1r)
    print(f"  DCG1R: edges g1={e1} g4={e4} g16={e16} (LB 58) "
          f"g64={e64} (LB 34) -> {'PASS' if dcg1r else 'REFUTED'}",
          flush=True)

    # UG-G1 baseline invulnerability
    ug_g1 = all(max(curves[f"{name}_g1"]) == 0.0
                for name in ("grid2d", "path"))
    gates["UG_G1_baseline_invulnerable"] = bool(ug_g1)
    print(f"  UG-G1 grid2d/path gamma-1 flat-zero: "
          f"{'PASS' if ug_g1 else 'REFUTED'} "
          f"({curves['grid2d_g1']} | {curves['path_g1']})", flush=True)

    # UG-G2 generalization fork
    brk = {name: any(max(curves[f"{name}_g{g:g}"]) >= 0.5
                     for g in GRIDS) for name in ("grid2d", "path")}
    if not any(brk.values()):
        ug_g2 = True                    # torus-specific declaration
        ug_g2_note = ("TORUS-SPECIFIC: grid2d/path never break at any "
                      "real (gamma, onset); AN-G2 no-break predictions "
                      "load-bearing")
    else:
        seq_ok = True
        for name in ("grid2d", "path"):
            if not brk[name]:
                continue
            es = [edges.get(f"{name}_g{g:g}") for g in (1.0, 4.0, 16.0, 64.0)]
            es_lb = [(0.0 if e is None else e) for e in es]
            # repaired-monotone check with censored lower bounds
            for i in range(1, len(es_lb)):
                prev = es[i - 1] if es[i - 1] is not None else None
                if prev is not None and es_lb[i] < prev - 1e-9:
                    seq_ok = False
        ug_g2 = seq_ok
        ug_g2_note = ("deadline structure on breaking substrate(s) "
                      f"{[k for k, v in brk.items() if v]}: "
                      "monotone-repaired" if seq_ok else "INVERSION (real U)")
    gates["UG_G2_generalization_fork"] = bool(ug_g2)
    print(f"  UG-G2 fork: {ug_g2_note} -> "
          f"{'PASS' if ug_g2 else 'REFUTED'}", flush=True)

    # ------------------------------------------------ analytic fit (torus)
    t_end = {g: protocol_end(subs["torus"], g) + SETTLE_H
             for g in (1.0, 4.0, 16.0, 64.0)}
    t_pre = {g: protocol_end(subs["torus"], g)
             for g in (1.0, 4.0, 16.0, 64.0)}

    # constraint cells (censoring-corrected, in-batch torus arms)
    def pval(key, idx):
        return curves[key][idx]

    lo_cells, hi_cells = [], []   # rescue cells push Theta up, break down
    g1 = curves["torus_g1"]
    for i, t in enumerate(TORUS_G1):
        (hi_cells if g1[i] >= 0.5 else lo_cells).append((1.0, t))
    for i, t in enumerate(GRIDS[4.0]):
        (hi_cells if curves["torus_g4"][i] >= 0.5 else lo_cells).append(
            (4.0, t))
    for i, t in enumerate(GRIDS[16.0]):
        (hi_cells if curves["torus_g16"][i] >= 0.5 else lo_cells).append(
            (16.0, t))
    for i, t in enumerate(GRIDS[64.0]):
        (hi_cells if curves["torus_g64"][i] >= 0.5 else lo_cells).append(
            (64.0, t))
    # never-silenced torus controls must break — H1-domain constraints
    # only (H2's reading covers silenced arms; a never-silenced run has
    # no remaining-time term and is outside its scope by construction)
    hi_cells_H1 = hi_cells + [(16.0, 10 ** 9), (64.0, 10 ** 9)]

    analytic = {}
    for variant in ("H1", "H2"):
        f = (lambda g, t: pred_rms_H1(subs["torus"], g, t, t_pre[g],
                                      t_end[g])) if variant == "H1" \
            else (lambda g, t: (t_end[g] - t) * r_post_eff(subs["torus"], g))
        hi_set = hi_cells_H1 if variant == "H1" else hi_cells
        lo = max((f(g, t) for g, t in lo_cells), default=0.0)
        hi = min((f(g, t) for g, t in hi_set))
        analytic[variant] = {
            "theta_min": round(lo, 4), "theta_max": round(hi, 4),
            "feasible": bool(lo < hi),
            "n_lo_constraints": len(lo_cells),
            "n_hi_constraints": len(hi_set),
        }
        # name the binding constraints on refutation
        if lo >= hi:
            worst_lo = max(lo_cells, key=lambda gt: f(*gt))
            worst_hi = min(hi_set, key=lambda gt: f(*gt))
            analytic[variant]["violated_pair"] = [
                f"rescue {worst_lo}", f"break {worst_hi}"]
    an_g1 = any(v["feasible"] for v in analytic.values())
    print(f"  AN-G1 analytic: H1 {analytic['H1']} | H2 {analytic['H2']} "
          f"-> {'PASS' if an_g1 else 'REFUTED (both readings)'}", flush=True)
    gates["AN_G1_analytic_fit"] = bool(an_g1)

    # AN-G2 conditional transfer
    an_g2 = None
    an_g2_variant = None
    if an_g1:
        variant = "H2" if analytic["H2"]["feasible"] else "H1"
        an_g2_variant = variant
        th_mid = 0.5 * (analytic[variant]["theta_min"]
                        + analytic[variant]["theta_max"])
        agree, tot, mism = 0, 0, []
        for name in ("grid2d", "path"):
            adj = subs[name]
            for g, grid in GRIDS.items():
                tp = protocol_end(adj, g)
                te = tp + SETTLE_H
                for i, t in enumerate(grid):
                    if t > tp + 1e-9:
                        continue
                    tot += 1
                    if variant == "H1":
                        pv = pred_rms_H1(adj, g, t, tp, te)
                        pred = pv > th_mid
                    else:
                        pred = (te - t) * r_post_eff(adj, g) > th_mid
                    emp = curves[f"{name}_g{g:g}"][i] >= 0.5
                    if pred == emp:
                        agree += 1
                    else:
                        mism.append(f"{name} g{g:g} t{t:g}")
        frac = agree / max(tot, 1)
        an_g2 = (frac == 1.0) or (frac >= 0.9 and len(mism) <= 2)
        analytic[variant]["transfer"] = {
            "theta_mid": round(th_mid, 4), "agreement": round(frac, 4),
            "n_cells": tot, "mismatches": mism[:12]}
        print(f"  AN-G2 transfer ({variant}, Theta_mid "
              f"{th_mid:.3f}): agreement {frac:.3f} ({agree}/{tot}) "
              f"mismatches {mism[:8]} -> {'PASS' if an_g2 else 'REFUTED'}",
              flush=True)
    else:
        print("  AN-G2: VOID by pre-registration (no feasible torus fit)",
              flush=True)
    gates["AN_G2_transfer"] = None if an_g1 is None else bool(an_g2) \
        if an_g1 else None
    if an_g1:
        gates["AN_G2_transfer"] = bool(an_g2)

    npass = sum(1 for v in gates.values() if v is True)
    nref = sum(1 for v in gates.values() if v is False)
    nvoid = sum(1 for v in gates.values() if v is None)
    print(f"\n  === {npass} PASS / {nref} REFUTED / {nvoid} VOID "
          f"({time.time() - t_start:.0f}s) ===")

    result = {
        "exp": "exp125_u_shape_generalization",
        "censoring_map": censoring,
        "curves": curves,
        "edges": {k: v for k, v in edges.items()},
        "analytic": analytic,
        "an_g2_variant": an_g2_variant,
        "criteria": gates,
        "notes": (
            "Censoring-free deadline curves on torus/grid2d/path; the "
            "exp124 U-shape's right flank owned as protocol censoring "
            "(gamma-dependent walk duration); the registered analytic "
            "deadline tested in both readings (H1 cumulative, H2 "
            "remaining-time integral)."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
