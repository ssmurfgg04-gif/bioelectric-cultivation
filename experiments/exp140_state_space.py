#!/usr/bin/env python3
"""exp140 — THE STATE-SPACE DEADLINE (joint-threshold reduction; ledger
L118's registered object). exp135 closed the scalar-reduction family
(per-step exp132, theta-swapped exp134, persistence-kernel exp135 —
kappa interval EMPTY at every tau_p, per-gamma refits pairwise
disjoint) while its DEPOSIT reproduced the deadline curve for the
first time: the chain's DIRECT simulation (harness-verbatim walk,
multi-source BFS, non-resetting state) hits the deposited edges
0/48/52/null. So the law LIVES in the chain's full state, not any
scalar integral of the boundary. REGISTERED NEXT (L118): state-space
reduction — the deadline as a JOINT threshold.

THE CLAIM (pre-registered BEFORE running): the deadline is a
half-plane in the 2D state projection

    x = span-theta-dev = RMS(th[span] - target[span])  at the read
    y = intact-V-dev   = RMS(V[intact] - target[intact]) at the read

— exp135's OWN decomposition fields (th_span_dev, err_intact),
verbatim; read = end of the harness-verbatim protocol sim (window +
amputation + walk chain + settle). Break iff w1*x + w2*y + b > 0.
No new physics: exp135.simulate() is reused untouched for the
cross-check; an instrumented VERBATIM copy (dynamics, walk order,
injection, mu latch, clamps untouched — asserted equal to
exp135.simulate() to <1e-9 on all four deposited scalars at every
anchor) adds only the per-cell read-state snapshot and a subsampled
(x_t, y_t) readout trajectory.

THE EIGHT DEPOSITED ANCHOR CELLS (the censoring-corrected bracket
set + both late controls, exp125's deposit via exp135):

    break : (g1,t0) (g4,t48) (g16,t52) (g16,t72) (g64,t36)
    rescue: (g4,t36) (g16,t48) (g64,t34)

g64@34/36 is the CENSORED bracket: the in-window flank rescues
through the window end 34.3 h (deposited edge ">34") while the
beyond-window late control breaks at P=1.0.

GATES (pre-registered):

  GATE-F1  (joint separability) a single linear separator fit on the
           eight anchors — exact 2D max-margin (perpendicular
           bisector of the closest convex-hull pair; hulls
           intersecting or zero gap => infeasible) — misclassifies
           ZERO deposited cells. If infeasible: best min-violation
           line by deterministic candidate enumeration, F1 FAIL
           logged with the violating cells.

  GATE-F2  (joint, not the refuted scalar family returning)
           (a) BOTH coordinates materially weight the normal: each
               |w_i|*sigma_i >= 10% of sum_j |w_j|*sigma_j (sigma_j =
               anchor-cloud std of coordinate j), evaluated on the
               F1 separator (or the min-violation basis, reported);
           (b) BOTH single-axis ablations — the best x-only and
               y-only thresholds on the same eight cells, either
               orientation — FAIL to zero-misclassify. If either
               single axis suffices, F2 FAILS and the result is
               reported as the scalar family returning in
               state-space clothing.

  GATE-F3  (out-of-sample prediction of the censored/un-tested
           cells) refit on the six NON-control anchors (break
           g1@0/g4@48/g16@52; rescue g4@36/g16@48/g64@34 — no g64
           break information in the fit); the frozen refit separator
           must place (a) g16@72 BREAK, (b) g64@36 BREAK, and (c)
           EVERY in-window g64 flank cell (t in 0,16,24,28,31,34)
           RESCUE — i.e. predict the deposited ">34" censoring
           verdict (in-window rescue + late-control break) from
           cells that never saw a g64 break.

  GATE-F4  (transfer — the bounded repair of exp135's NaN leg) the
           FROZEN F1 separator places EVERY deposited grid2d/path
           cell (flat-zero curves: all rescue; exp135 R1's 26+26
           cells) on the RESCUE side. Scope, honestly: flat-zero
           substrates carry no break class, so this gate verifies
           non-contradiction at the torus orientation, not local
           separation; the state readouts exist there because the
           span's own walk exists on every substrate (the readout
           needs no boundary chain and no kappa — the exact object
           exp135's transfer leg lacked). Reported alongside, not
           gated: the direct-sim scalar err at every transfer cell
           and the score/err rank agreement (orientation consistency).

ROBUSTNESS (reported, not gated): R1 the full 28-cell torus
censoring-corrected curve under the frozen separator + predicted
edges vs deposited 0/48/52/>34; R2 per-anchor margins; R3 the (x,y)
readout trajectories along the walk for the eight anchors; R4
max-abs readout variants (single-axis and joint, reported only);
R5 the violation geometry if F1 fails (which anchor pierces the
opposite hull, with the direct sim's own scalar at that cell).

RUN: 88 deterministic sims (28 torus + 26 grid2d + 26 path + 8
cross-checks), the exp135 wall-time class; BLAS pinned.
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

from experiments.exp125_u_shape_generalization import (
    protocol_end, region_span, target_pattern, GRIDS, TORUS_G1,
    WINDOW_H, SETTLE_H,
)
from experiments.exp112_walk_speed_ladder import build_battery
import experiments.exp135_walk_chain as e135
from experiments.exp90_two_source_read import star_dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp140_state_space.json")

GAMMAS = (1.0, 4.0, 16.0, 64.0)
ERR_BAR = 6.0

# ---- the eight deposited anchor cells (exp125 deposit via exp135) ----
BREAK_CELLS = ((1.0, 0.0), (4.0, 48.0), (16.0, 52.0), (16.0, 72.0),
               (64.0, 36.0))
RESCUE_CELLS = ((4.0, 36.0), (16.0, 48.0), (64.0, 34.0))
ANCHORS = BREAK_CELLS + RESCUE_CELLS
F3_CONTROLS = ((16.0, 72.0), (64.0, 36.0))          # held out of the refit
G64_FLANK = ((64.0, 0.0), (64.0, 16.0), (64.0, 24.0),
             (64.0, 28.0), (64.0, 31.0), (64.0, 34.0))
F3_FIT = tuple(c for c in ANCHORS if c not in F3_CONTROLS)

W_SHARE = 0.10   # F2(a) materiality bar per standardized coordinate


def fmt(c) -> str:
    return f"g{c[0]:g}_t{c[1]:g}"


def deposited_verdict(c) -> str:
    """exp125's censoring-corrected torus deposit (via exp135's
    break_cells/rescue_cells): g1 breaks everywhere (edge 0); g4 edge
    48; g16 edge 52 with late control 72; g64 censored >34 (all
    in-window rescue) with late control 36 breaking."""
    g, t = c
    if g == 1.0:
        return "break"
    if g == 4.0:
        return "break" if t >= 48.0 else "rescue"
    if g == 16.0:
        return "rescue" if t <= 48.0 else "break"
    return "break" if t >= 36.0 else "rescue"


# ------------------------------------------------------------------
# instrumented verbatim copy of exp135.simulate()
# ------------------------------------------------------------------
def simulate_instrumented(adj: np.ndarray, gamma: float,
                          t_star: float | None, want_traj: bool = True,
                          want_snapshot: bool = False) -> dict:
    """VERBATIM copy of exp135.simulate(): same Euler dynamics, same
    zone clamps, same multi-source BFS walk order, same 8 sub-steps +
    injection at target, same mu latch (incl. inside walk/settle),
    same non-resetting state. Instrumentation ONLY: subsampled
    (x_t, y_t) readout trajectory, per-cell (V, th) snapshot at the
    read, max-abs readout variants. Fidelity asserted in main()."""
    n = adj.shape[0]
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

    V = canon.astype(float).copy()
    th = canon.astype(float).copy()
    mu = e135.MU
    t0 = 0.0
    n_win = int(round(WINDOW_H / dt))
    n_settle = int(round(SETTLE_H / dt))
    inj = np.zeros(n, dtype=bool)

    def x_read() -> float:
        return float(np.sqrt(np.mean((th[span] - target[span]) ** 2)))

    def y_read() -> float:
        return float(np.sqrt(np.mean((V[intact] - target[intact]) ** 2)))

    def dyn_step() -> None:
        nonlocal V, th, t0, mu
        t0 += dt
        if t_star is not None and t0 >= t_star:
            mu = 0.0
        dV = gamma * (th - V) + G @ V - V * degG
        dth = e135.EPS * (V - th) + mu * (A @ th - th * degA)
        V = V + dt * dV
        th = th + dt * dth

    n_total = n_win + e135.WALK_SUB * len(order2) + n_settle
    stride = max(1, n_total // 240)
    step = 0
    traj: list[tuple[float, float, float]] = []

    # ---- window (clamps on) — verbatim phase structure
    for _ in range(n_win):
        dyn_step()
        for idx, val in clamps:
            V[idx] = val
            th[idx] += dt * e135.EPS * (val - th[idx])
        step += 1
        if want_traj and step % stride == 0:
            traj.append((round(t0, 4), round(x_read(), 4), round(y_read(), 4)))

    # ---- amputation + the walk chain — verbatim
    V[span] = e135.WOUND_V
    th[span] = e135.WOUND_TH
    for i in order2:
        for _ in range(e135.WALK_SUB):
            dyn_step()
            step += 1
            if want_traj and step % stride == 0:
                traj.append((round(t0, 4), round(x_read(), 4),
                             round(y_read(), 4)))
        # the injection: every harness branch delivers target[i]
        V[i] = target[i]
        th[i] = target[i]
        inj[i] = True

    # ---- settle — verbatim
    for _ in range(n_settle):
        dyn_step()
        step += 1
        if want_traj and step % stride == 0:
            traj.append((round(t0, 4), round(x_read(), 4), round(y_read(), 4)))

    out = {
        "dt": dt,
        "t_read": t0,
        "t_pre": protocol_end(adj, gamma),
        "err": float(np.sqrt(np.mean((V - target) ** 2))),
        "err_span": float(np.sqrt(np.mean((V[span] - target[span]) ** 2))),
        "err_intact": float(np.sqrt(np.mean((V[intact] - target[intact]) ** 2))),
        "th_span_dev": float(np.sqrt(np.mean((th[span] - target[span]) ** 2))),
        "x": float(np.sqrt(np.mean((th[span] - target[span]) ** 2))),
        "y": float(np.sqrt(np.mean((V[intact] - target[intact]) ** 2))),
        "x_max": float(np.max(np.abs(th[span] - target[span]))),
        "y_max": float(np.max(np.abs(V[intact] - target[intact]))),
        "n_span": int(len(span)),
        "n_intact": int(len(intact)),
    }
    if want_traj:
        out["traj"] = traj
    if want_snapshot:
        out["span_idx"] = [int(i) for i in span]
        out["intact_idx"] = [int(i) for i in intact]
        out["target_span"] = [round(float(v), 3) for v in target[span]]
        out["target_intact"] = [round(float(v), 3) for v in target[intact]]
        out["V_read"] = [round(float(v), 3) for v in V]
        out["th_read"] = [round(float(v), 3) for v in th]
    return out


# ------------------------------------------------------------------
# 2D linear-separator geometry (exact, deterministic)
# ------------------------------------------------------------------
def _cross(o, a, b) -> float:
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def convex_hull(pts) -> list[tuple[float, float]]:
    pts = sorted(set((round(float(x), 12), round(float(y), 12))
                     for x, y in pts))
    if len(pts) <= 2:
        return pts
    lower: list = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _on_seg(p, a, b) -> bool:
    return (min(a[0], b[0]) - 1e-12 <= p[0] <= max(a[0], b[0]) + 1e-12
            and min(a[1], b[1]) - 1e-12 <= p[1] <= max(a[1], b[1]) + 1e-12)


def point_in_hull(p, hull_pts) -> bool:
    h = hull_pts if len(hull_pts) >= 3 else hull_pts
    if len(h) == 1:
        return abs(p[0] - h[0][0]) < 1e-12 and abs(p[1] - h[0][1]) < 1e-12
    if len(h) == 2:
        return _on_seg(p, h[0], h[1])
    signs = [_cross(h[i], h[(i + 1) % len(h)], p) for i in range(len(h))]
    return (all(s >= -1e-9 for s in signs)
            or all(s <= 1e-9 for s in signs))


def _seg_intersect(p1, p2, p3, p4) -> bool:
    d1 = _cross(p3, p4, p1)
    d2 = _cross(p3, p4, p2)
    d3 = _cross(p1, p2, p3)
    d4 = _cross(p1, p2, p4)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True
    return (abs(d1) < 1e-12 and _on_seg(p1, p3, p4)) \
        or (abs(d2) < 1e-12 and _on_seg(p2, p3, p4)) \
        or (abs(d3) < 1e-12 and _on_seg(p3, p1, p2)) \
        or (abs(d4) < 1e-12 and _on_seg(p4, p1, p2))


def hulls_intersect(h1, h2) -> bool:
    if any(point_in_hull(p, h2) for p in h1):
        return True
    if any(point_in_hull(p, h1) for p in h2):
        return True
    if len(h1) >= 2 and len(h2) >= 2:
        e1 = [(h1[i], h1[(i + 1) % len(h1)]) for i in range(len(h1))]
        e2 = [(h2[i], h2[(i + 1) % len(h2)]) for i in range(len(h2))]
        if len(h1) == 2:
            e1 = [(h1[0], h1[1])]
        if len(h2) == 2:
            e2 = [(h2[0], h2[1])]
        for a, b in e1:
            for c, d in e2:
                if _seg_intersect(a, b, c, d):
                    return True
    return False


def _closest_on_seg(p, a, b) -> tuple[float, float]:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 < 1e-24:
        return a
    t = ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2
    t = max(0.0, min(1.0, t))
    return (ax + t * dx, ay + t * dy)


def _closest_on_hull(p, h) -> tuple[float, float]:
    if len(h) == 1:
        return h[0]
    segs = [(h[i], h[(i + 1) % len(h)]) for i in range(len(h))] \
        if len(h) > 2 else [(h[0], h[1])]
    best, bd = None, float("inf")
    for a, b in segs:
        c = _closest_on_seg(p, a, b)
        d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2
        if d < bd:
            best, bd = c, d
    return best


def max_margin(pb, pr):
    """Exact 2D hard-margin separator. Returns (w, b, margin_distance)
    with break iff score > 0, or None if the hulls intersect / touch."""
    hB = convex_hull(pb)
    hR = convex_hull(pr)
    if hulls_intersect(hB, hR):
        return None
    best = None
    for a in hB:
        c = _closest_on_hull(a, hR)
        d2 = (a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2
        if best is None or d2 < best[0]:
            best = (d2, a, c)
    for c in hR:
        a = _closest_on_hull(c, hB)
        d2 = (a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2
        if d2 < best[0]:
            best = (d2, a, c)
    d2, a, c = best
    dist = float(np.sqrt(d2))
    if dist < 1e-9:
        return None
    w = np.array([a[0] - c[0], a[1] - c[1]])
    b = -float(w @ ((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0))
    return w, b, dist / 2.0


def _minmax_margin(w, b, pts, labels) -> float:
    nw = float(np.linalg.norm(w))
    return min(((s if lab else -s) / nw)
               for (x, y), lab, s in
               ((p, l, w[0] * p[0] + w[1] * p[1] + b)
                for p, l in zip(pts, labels)))


def min_violation_line(pb, pr):
    """Deterministic min-violation line (max-min-margin tie-break)."""
    pts = list(pb) + list(pr)
    labels = [True] * len(pb) + [False] * len(pr)
    cands = []
    for i in range(len(pb)):
        for j in range(len(pr)):
            w = np.array([pb[i][0] - pr[j][0], pb[i][1] - pr[j][1]])
            bb = -float(w @ pb[i])
            cands += [(w, bb), (-w, -bb)]
    for group in (pb, pr):
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                d = np.array([group[j][0] - group[i][0],
                              group[j][1] - group[i][1]])
                w = np.array([-d[1], d[0]])
                bb = -float(w @ group[i])
                cands += [(w, bb), (-w, -bb)]
    for ax in (0, 1):
        vals = sorted({p[ax] for p in pts})
        units = ((1.0, 0.0),) if ax == 0 else ((0.0, 1.0),)
        for v0, v1 in zip(vals, vals[1:]):
            thr = (v0 + v1) / 2.0
            for u in units:
                w = np.array(u)
                cands += [(w, -thr), (-w, thr)]
    best = None
    for w, bb in cands:
        viol = sum(1 for (x, y), l in zip(pts, labels)
                   if (w[0] * x + w[1] * y + bb > 0) != l)
        mm = _minmax_margin(w, bb, pts, labels)
        key = (-viol, mm)
        if best is None or key > best[0]:
            best = (key, w, bb, viol, mm)
    _, w, bb, viol, mm = best
    return w, bb, viol, mm


def single_axis_feasible(pb, pr, coord: int) -> dict:
    """Best threshold on one axis, either orientation. Zero
    misclassification possible iff the label intervals disjoint."""
    vb = sorted(p[coord] for p in pb)
    vr = sorted(p[coord] for p in pr)
    hi_break = (max(vb) < min(vr) - 1e-12) if vb and vr else False
    lo_break = (max(vr) < min(vb) - 1e-12) if vb and vr else False
    return {"feasible": bool(hi_break or lo_break),
            "orientation": ("break_high" if hi_break
                            else "break_low" if lo_break else None),
            "break_range": [min(vb), max(vb)] if vb else None,
            "rescue_range": [min(vr), max(vr)] if vr else None}


def spearman(a, b) -> float:
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    ra, rb = ranks(list(a)), ranks(list(b))
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = float(np.sqrt(sum((x - ma) ** 2 for x in ra)
                        * sum((y - mb) ** 2 for y in rb)))
    return num / den if den > 0 else float("nan")


# ------------------------------------------------------------------
def main() -> dict:
    print("=== exp140: the state-space deadline (joint threshold) ===\n")
    t_start = time.time()
    battery = build_battery()
    torus = battery["torus"]
    n_region = region_span(torus.shape[0])
    assert n_region == 73

    # ---- torus cell set: the deposited grid + the two late controls
    cells: list[tuple[float, float]] = []
    for g in GAMMAS:
        for t in (TORUS_G1 if g == 1.0 else GRIDS[g]):
            cells.append((g, float(t)))
    for c in ANCHORS:
        if c not in cells:
            cells.append(c)
    cells = sorted(set(cells))
    assert len(cells) == 28, len(cells)

    sim: dict = {}
    for c in cells:
        sim[c] = simulate_instrumented(torus, c[0], c[1],
                                       want_traj=c in ANCHORS,
                                       want_snapshot=c in ANCHORS)
    print(f"  torus sims: {len(sim)} ({time.time() - t_start:.0f}s)",
          flush=True)

    # ---- fidelity: the instrumented copy vs exp135's own simulate()
    fidelity = []
    for c in ANCHORS:
        ref = e135.simulate(torus, c[0], c[1])
        dmax = max(abs(ref[k] - sim[c][k]) for k in
                   ("err", "err_span", "err_intact", "th_span_dev"))
        fidelity.append({"cell": fmt(c),
                         "max_abs_scalar_diff": round(float(dmax), 15)})
        assert dmax < 1e-9, f"instrumentation drift at {fmt(c)}: {dmax}"
    print(f"  fidelity vs exp135.simulate() at 8 anchors: "
          f"max|d| = {max(f['max_abs_scalar_diff'] for f in fidelity):.2e}",
          flush=True)

    xy = {c: (sim[c]["x"], sim[c]["y"]) for c in cells}
    pb = [xy[c] for c in BREAK_CELLS]
    pr = [xy[c] for c in RESCUE_CELLS]

    def anchor_table(w, b) -> list[dict]:
        nw = float(np.linalg.norm(w))
        rows = []
        for c in ANCHORS:
            x, y = xy[c]
            s = w[0] * x + w[1] * y + b
            dep = "break" if c in BREAK_CELLS else "rescue"
            rows.append({"cell": fmt(c), "x": round(x, 4),
                         "y": round(y, 4), "deposited": dep,
                         "score": round(float(s), 4),
                         "signed_margin": round(float(s / nw), 4),
                         "placed": "break" if s > 0 else "rescue"})
        return rows

    # ---- GATE-F1: the joint separator on the eight anchors
    sep = max_margin(pb, pr)
    if sep is not None:
        w, b, margin = sep
        method = "hard-margin hull bisector (exact)"
        f1 = True
        viol_cells = []
    else:
        w, b, viol, _mm = min_violation_line(pb, pr)
        margin = _minmax_margin(w, b, pb + pr,
                                [True] * len(pb) + [False] * len(pr))
        method = "min-violation line (hulls intersect)"
        f1 = viol == 0
        viol_cells = [fmt(c) for c in ANCHORS
                      if (w[0] * xy[c][0] + w[1] * xy[c][1] + b > 0)
                      != (c in BREAK_CELLS)]
    print(f"  F1: w=({w[0]:.4f}, {w[1]:.4f}) b={b:.4f} margin="
          f"{margin:.4f} -> {'PASS' if f1 else 'FAIL'} {viol_cells}",
          flush=True)

    # ---- GATE-F2: joint, not scalar
    sig = [float(np.std([p[i] for p in pb + pr])) for i in (0, 1)]
    contrib = [abs(float(w[i])) * sig[i] for i in (0, 1)]
    tot = sum(contrib)
    shares = [c / tot if tot > 0 else 0.0 for c in contrib]
    xonly = single_axis_feasible(pb, pr, 0)
    yonly = single_axis_feasible(pb, pr, 1)
    f2 = (all(s >= W_SHARE for s in shares)
          and not xonly["feasible"] and not yonly["feasible"])
    print(f"  F2: weight shares ({shares[0]:.3f}, {shares[1]:.3f}) "
          f"x-only feasible {xonly['feasible']} y-only "
          f"{yonly['feasible']} -> {'PASS' if f2 else 'FAIL'}", flush=True)

    # ---- GATE-F3: out-of-sample prediction of the censored cells
    pb3 = [xy[c] for c in F3_FIT if c in BREAK_CELLS]
    pr3 = [xy[c] for c in F3_FIT if c in RESCUE_CELLS]
    sep3 = max_margin(pb3, pr3)
    if sep3 is not None:
        w3, b3, m3 = sep3
        method3 = "hard-margin hull bisector (6-cell refit)"
        viol3 = 0
    else:
        w3, b3, viol3, _mm = min_violation_line(pb3, pr3)
        m3 = _minmax_margin(w3, b3, pb3 + pr3,
                            [True] * len(pb3) + [False] * len(pr3))
        method3 = "min-violation line (6-cell refit)"
    s72 = w3[0] * xy[(16.0, 72.0)][0] + w3[1] * xy[(16.0, 72.0)][1] + b3
    s6436 = w3[0] * xy[(64.0, 36.0)][0] + w3[1] * xy[(64.0, 36.0)][1] + b3
    flank = {fmt(c): {"x": round(xy[c][0], 4), "y": round(xy[c][1], 4),
                      "score": round(float(w3[0] * xy[c][0]
                                          + w3[1] * xy[c][1] + b3), 4),
                      "placed": "break"
                      if w3[0] * xy[c][0] + w3[1] * xy[c][1] + b3 > 0
                      else "rescue"}
             for c in G64_FLANK}
    f3 = (viol3 == 0 and s72 > 0 and s6436 > 0
          and all(v["placed"] == "rescue" for v in flank.values()))
    print(f"  F3: refit w=({w3[0]:.4f}, {w3[1]:.4f}) b={b3:.4f}; "
          f"g16@72 score {s72:.3f} (want break), g64@36 score "
          f"{s6436:.3f} (want break), flank all rescue "
          f"{all(v['placed'] == 'rescue' for v in flank.values())} "
          f"-> {'PASS' if f3 else 'FAIL'}", flush=True)

    # ---- GATE-F4: transfer with the frozen F1 separator (bounded repair)
    transfer = {}
    f4 = True
    for name in ("grid2d", "path"):
        adj = battery[name]
        tcells = []
        for g in GAMMAS:
            grid = TORUS_G1 if g == 1.0 else GRIDS[g]
            tpre = protocol_end(adj, g)
            for t in grid:
                if t > tpre + 1e-9:
                    continue
                tcells.append((g, float(t)))
        tsim = {c: simulate_instrumented(adj, c[0], c[1], want_traj=False)
                for c in tcells}
        rows, scs, errs = [], [], []
        false_break = 0
        for c in tcells:
            x, y = tsim[c]["x"], tsim[c]["y"]
            sc = w[0] * x + w[1] * y + b
            scs.append(sc)
            errs.append(tsim[c]["err"])
            if sc > 0:
                false_break += 1
            rows.append({"cell": fmt(c), "x": round(x, 4),
                         "y": round(y, 4), "score": round(float(sc), 4),
                         "direct_err": round(float(tsim[c]["err"]), 3),
                         "placed": "break" if sc > 0 else "rescue"})
        nw = float(np.linalg.norm(w))
        worst = min(rows, key=lambda r: r["score"])
        ok = false_break == 0
        f4 = f4 and ok
        transfer[name] = {
            "n_cells": len(tcells), "false_breaks": false_break,
            "agree_with_flat_zero_deposit": ok,
            "worst_rescue_margin": round(float(worst["score"] / nw), 4),
            "worst_cell": worst["cell"],
            "direct_err_max": round(float(max(errs)), 3),
            "direct_err_breaks": int(sum(1 for e in errs if e > ERR_BAR)),
            "spearman_score_vs_direct_err":
                round(float(spearman(scs, errs)), 4),
            "cells": rows,
        }
        print(f"  F4 {name}: false breaks {false_break}/{len(tcells)} "
              f"direct-err breaks {transfer[name]['direct_err_breaks']} "
              f"worst margin {transfer[name]['worst_rescue_margin']:.3f} "
              f"({worst['cell']}) rho(score,err) "
              f"{transfer[name]['spearman_score_vs_direct_err']:.3f}",
              flush=True)

    # ---- R1: the full torus curve under the frozen separator
    curve = []
    for c in cells:
        x, y = xy[c]
        sc = w[0] * x + w[1] * y + b
        dep = deposited_verdict(c)
        curve.append({"cell": fmt(c), "x": round(x, 4), "y": round(y, 4),
                      "deposited": dep, "score": round(float(sc), 4),
                      "direct_err": round(float(sim[c]["err"]), 3),
                      "placed": "break" if sc > 0 else "rescue"})
    mism = [r["cell"] for r in curve if r["deposited"] != r["placed"]]
    edges = {}
    for g in GAMMAS:
        grid = TORUS_G1 if g == 1.0 else GRIDS[g]
        e = None
        for t in grid:
            if (g, float(t)) == (16.0, 72.0):
                continue
            sc = w[0] * xy[(g, float(t))][0] + w[1] * xy[(g, float(t))][1] + b
            if sc > 0:
                e = float(t)
                break
        edges[f"g{g:g}"] = e
    print(f"  R1: curve mismatches {mism}; predicted edges {edges} "
          f"(deposited 0/48/52/>34)", flush=True)

    # ---- R4: max-abs readout variants (reported only)
    pbm = [(sim[c]["x_max"], sim[c]["y_max"]) for c in BREAK_CELLS]
    prm = [(sim[c]["x_max"], sim[c]["y_max"]) for c in RESCUE_CELLS]
    r4 = {
        "single_axis": {
            "x_max_only": single_axis_feasible(pbm, prm, 0),
            "y_max_only": single_axis_feasible(pbm, prm, 1)},
        "joint": None,
    }
    sep_m = max_margin(pbm, prm)
    if sep_m is not None:
        r4["joint"] = {"feasible": True,
                       "w": [round(float(v), 4) for v in sep_m[0]],
                       "b": round(float(sep_m[1]), 4),
                       "margin": round(float(sep_m[2]), 4)}
    else:
        wm, bm, viom, _ = min_violation_line(pbm, prm)
        r4["joint"] = {"feasible": False, "min_violations": int(viom),
                       "w": [round(float(v), 4) for v in wm],
                       "b": round(float(bm), 4)}

    # ---- R5 (pre-registered): the violation geometry if F1 fails
    piercing = []
    for cb in BREAK_CELLS:
        dom = [fmt(cr) for cr in RESCUE_CELLS
               if xy[cr][0] >= xy[cb][0] and xy[cr][1] >= xy[cb][1]]
        if dom:
            piercing.append({"break_cell": fmt(cb),
                             "x": round(xy[cb][0], 4),
                             "y": round(xy[cb][1], 4),
                             "dominated_by_rescue": dom,
                             "direct_err": round(float(sim[cb]["err"]), 3)})
    scan_best = -float("inf")
    scan_theta = None
    for th in np.linspace(0.0, np.pi, 36001):
        wq = (float(np.cos(th)), float(np.sin(th)))
        bs = [wq[0] * p[0] + wq[1] * p[1] for p in pb]
        rs = [wq[0] * p[0] + wq[1] * p[1] for p in pr]
        gap = max(min(bs) - max(rs), min(rs) - max(bs))
        if gap > scan_best:
            scan_best, scan_theta = gap, float(np.degrees(th))
    r5 = {
        "linear_separability_certificate": {
            "method": "exhaustive 36001-direction projection scan",
            "best_gap": round(float(scan_best), 4),
            "best_theta_deg": round(float(scan_theta), 2),
            "separable": bool(scan_best > 0)},
        "piercing_anchors": piercing,
        "g64_bracket_displacement_34_to_36": {
            "dx": round(float(xy[(64.0, 36.0)][0] - xy[(64.0, 34.0)][0]), 4),
            "dy": round(float(xy[(64.0, 36.0)][1] - xy[(64.0, 34.0)][1]), 4),
            "x_shortfall_to_clear_rescue_hull": round(
                float(xy[(16.0, 48.0)][0] - xy[(64.0, 36.0)][0]), 4)},
    }

    # ---- R6/R7 (post-run robustness, NOT pre-registered gates): the
    # feasible 6-cell refit separator's own transfer and curve behavior
    def edges_under(wq, bq):
        out = {}
        for g in GAMMAS:
            grid = TORUS_G1 if g == 1.0 else GRIDS[g]
            e = None
            for t in grid:
                sc = wq[0] * xy[(g, float(t))][0] \
                    + wq[1] * xy[(g, float(t))][1] + bq
                if sc > 0:
                    e = float(t)
                    break
            out[f"g{g:g}"] = e
        return out

    curve3_mism = [fmt(c) for c in cells
                   if (w3[0] * xy[c][0] + w3[1] * xy[c][1] + b3 > 0)
                   != (deposited_verdict(c) == "break")]
    r67 = {
        "added": "post-run; not pre-registered gates; gates untouched",
        "refit_separator_on_transfer": {
            name: {
                "false_breaks": int(sum(
                    1 for row in
                    transfer[name]["cells"]
                    if w3[0] * row["x"] + w3[1] * row["y"] + b3 > 0)),
                "n_cells": transfer[name]["n_cells"]}
            for name in ("grid2d", "path")},
        "refit_separator_curve": {
            "mismatches": curve3_mism,
            "predicted_edges": edges_under(w3, b3)},
    }

    npass = sum([f1, f2, f3, f4])
    print(f"\n  === {npass}/4 gates PASS ({time.time() - t_start:.0f}s) ===")

    result = {
        "exp": "exp140_state_space",
        "claim": ("the torus deadline is a joint threshold: a half-plane "
                  "in (span-theta-dev, intact-V-dev) — exp135's own "
                  "th_span_dev / err_intact fields at the protocol read "
                  "— separates all break cells from all rescue cells, "
                  "with both coordinates load-bearing (no single-axis "
                  "threshold survives)"),
        "pre_registered": {
            "anchors": {"break": [fmt(c) for c in BREAK_CELLS],
                        "rescue": [fmt(c) for c in RESCUE_CELLS]},
            "readouts": {"x": "RMS(th[span]-target[span]) at read "
                              "(exp135 th_span_dev, verbatim)",
                         "y": "RMS(V[intact]-target[intact]) at read "
                              "(exp135 err_intact, verbatim)"},
            "f3_fit": [fmt(c) for c in F3_FIT],
            "f3_controls": [fmt(c) for c in F3_CONTROLS],
            "f3_flank": [fmt(c) for c in G64_FLANK],
            "f2_materiality_bar": W_SHARE,
        },
        "fidelity_check": fidelity,
        "anchors": anchor_table(w, b),
        "separator": {"w": [round(float(w[0]), 6), round(float(w[1]), 6)],
                      "b": round(float(b), 6),
                      "margin_distance": round(float(margin), 4),
                      "method": method,
                      "w_share": [round(s, 4) for s in shares],
                      "sigma": [round(s, 4) for s in sig]},
        "gates": {
            "F1_joint_separable": {"pass": bool(f1),
                                   "violations": viol_cells},
            "F2_joint_not_scalar": {
                "pass": bool(f2),
                "w_share": [round(s, 4) for s in shares],
                "x_only": xonly, "y_only": yonly},
            "F3_censored_prediction": {
                "pass": bool(f3),
                "refit_method": method3,
                "refit_violations": int(viol3),
                "refit_margin": round(float(m3), 4),
                "w": [round(float(v), 6) for v in w3],
                "b": round(float(b3), 6),
                "g16_t72_score": round(float(s72), 4),
                "g64_t36_score": round(float(s6436), 4),
                "g64_flank": flank},
            "F4_transfer_bounded_repair": {
                "pass": bool(f4), "substrates": transfer},
        },
        "full_curve": curve,
        "curve_mismatches": mism,
        "predicted_edges": edges,
        "violation_geometry_R5": r5,
        "post_run_robustness_R6_R7": r67,
        "alt_readouts_max_abs": r4,
        "trajectories": {fmt(c): sim[c].get("traj", [])
                         for c in ANCHORS if "traj" in sim[c]},
        "state_snapshots": {
            fmt(c): {"span_idx": sim[c]["span_idx"],
                     "intact_idx": sim[c]["intact_idx"],
                     "V_read": sim[c]["V_read"],
                     "th_read": sim[c]["th_read"]}
            for c in ANCHORS},
        "criteria": {
            "F1_joint_separable": bool(f1),
            "F2_joint_not_scalar": bool(f2),
            "F3_censored_prediction": bool(f3),
            "F4_transfer_bounded_repair": bool(f4),
        },
        "diagnosis": (
            "F1/F3 fail on ONE anchor: the g64@36 late control. Its "
            "(span-theta-dev, intact-V-dev) = (2.777, 8.203) is "
            "Pareto-dominated by rescue g16@48 (3.537, 9.535), so NO "
            "linear separator exists on the eight anchors (exhaustive "
            "36001-direction scan: best gap -0.446) — the min-violation "
            "line must invert the intact-V weight (w2 = -1.352) to keep "
            "g64@36 break-ward, which then false-breaks every flat-zero "
            "transfer cell (F4's failure is inherited from F1, not a "
            "transfer-readout failure: under the FEASIBLE 6-cell refit "
            "separator the same 52 transfer cells are 0/26 + 0/26 "
            "false breaks, deep rescue-side). The six "
            "censoring-corrected bracket cells alone ARE separable "
            "with an interpretable BOTH-POSITIVE normal (w = (+0.293, "
            "+0.365), hard margin 0.234), and that refit predicts "
            "g16@72 break and the whole g64 in-window flank rescue — "
            "7/8 predictions correct, failing only g64@36 (score "
            "-0.818 vs deposited P=1.0 break). The bracket displacement "
            "34->36 moves break-ward (+0.592, +0.236) but falls 0.760 "
            "x-units short of clearing the rescue hull — the mu-latch's "
            "marginal state damage is again too small (exp134's "
            "14x-shortfall bug-class, now measured in state units). "
            "Consistent with the deposit: the direct sim's own scalar "
            "at g64@36 is 4.904 < 6.0 — the deterministic mean-field "
            "state at read does not encode the late-control break, and "
            "no functional of it (this projection included) can "
            "recover what the state does not contain. REGISTERED "
            "NEXT: the state-space reduction survives only as a "
            "curve-law (the 0/48/52/>34 edges live in the "
            "(span-theta, intact-V) plane, both coordinates "
            "load-bearing, single-axis thresholds dead); the late "
            "controls need a state direction the mean-field read "
            "collapses — candidates: a third coordinate (residual "
            "mu exposure at read / wound-front theta PROFILE shape "
            "rather than its RMS), a pre-settle read, or noise-carrying "
            "state (the harness breaks g64@36 at P=1.0 where the "
            "mean-field sits 1.1 mV under the bar)."),
        "notes": (
            "Instrumentation-only reuse of exp135's chain simulation: "
            "the walk machinery is exp135.simulate()'s verbatim copy, "
            "asserted equal to exp135.simulate() to <1e-9 on all four "
            "deposited scalars at every anchor. The separator lives on "
            "the model's own state readouts at the protocol read; no "
            "new physics, no kappa, no tau_p."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
