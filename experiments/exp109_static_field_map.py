#!/usr/bin/env python3
"""exp109 — THE STATIC FIELD MAP (ledger L90's registration: the
frozen-geometry term — the V-equilibrium of the committed pattern —
carries the torus's full +1.40 size trend, and the eps-sag transient
compresses it to +1.04 at the 15 h read. What remains is pure
electrostatics: WHY does the frozen field's error rise with n).

THE INSTRUMENT (no dynamics anywhere): the committed theta pattern
is CAPTURED from the real executor at walk end (window + amputate +
BFS commit, bit-identical step sequence to exp108's instrumented
executor), then the settle field is solved DIRECTLY:

    (gamma I + L_G) V* = gamma theta,   L_G = g_gap (D(A) - A)

— the exact fixed point of dV/dt with theta frozen (exp108's
eps_freeze arm measured this field's error as the post-walk error;
the solve replaces the relaxation with linear algebra). On the torus
the Laplacian is the 2-D periodic lattice: the DFT basis
diagonalizes it EXACTLY (eigenvalue lambda(k) = g_gap(4 - 2cos kx
- 2cos ky), k = 2 pi (p, q) / r) — so the error field e = V* - target
is eigen-decomposed by fft2 and its POWER deposited by |k| band:
  LOW   |k| <= pi/(2)   (wavelength ~ span — reservoir bleed)
  MID   pi/2 < |k| <= 2 (wavelength ~ rows — the canon diamond's
        wrap scatter)
  HIGH  |k| > 2         (wavelength ~ the 4.5-cell smoothing kernel —
        local smearing of the -30/-50/-20 discontinuities)

THE ARMS (per size; real-pattern arms over seeds 1-3):
  real        the CAPTURED walk-end theta (window rewrite + commit
              noise baked in) — validated against exp108's dynamic
              post-walk error
  idealized   theta = target EXACTLY (zones -30, gaps canon, intact
              base canon — no window rewrite, no noise) — the pure
              pattern geometry, deterministic
  canon_flat  the idealized pattern with the CANON GAPS FLATTENED to
              trunk (-50) — kills the BFS-diamond scatter; if the
              size trend collapses, the diamond's wrap scatter is
              named as the seed

PRE-REGISTERED GATES:

  SF-G1  (instrument validity) the static solve on the real pattern
         reproduces the dynamic post-walk error within 0.15 mV at
         every size — the walk's 8-steps-per-cell quasi-equilibrium
         assumption holds; a miss means the walk-end field is NOT
         equilibrated and the static map misreads (then the capture
         is re-examined, not the physics).
  SF-G2  (localization) the band-power fractions are deposited for
         the real pattern at every size and the dominant band is
         NAMED from the data (measurement gate — names, never
         fails).
  SF-G3  (mechanism) the canon_flat arm's size delta (n=784 minus
         n=100) shrinks by >= 40% versus the idealized arm's delta
         — the diamond scatter drives the rise; below 40% the
         scatter is refuted as the carrier and the surviving band
         structure (low-k bleed or high-k smearing) carries to
         exp110.
  SF-G4  (clean-pattern floor) the idealized pattern's static error
         at n=100 is <= 1.0 mV — a clean pattern is cheap under the
         kernel; the trend must come from the pattern's specific
         structure, not from smoothing per se.

RUN: 12 dynamic captures (4 sizes x 3 seeds) + 8 solves (4 sizes x
{idealized, canon_flat}) + 12 real solves. Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.compiler.anatomy import compile_anatomy
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import GraphCollective
from experiments.exp68_coherence_search import torus
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp109_static_field_map.json")

SEEDS3 = (1, 2, 3)
SIZES = (100, 196, 400, 784)
GAMMA = 4.0
G_GAP = 0.2


def _labeling_bfs_n(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    order = bfs_order(A)
    lbl = np.full(n, TRUNK_V)
    lbl[order[:n // 4]] = HEAD_V
    return lbl


def _spec_target_n(spec, canon: np.ndarray, n: int) -> np.ndarray:
    target = canon.copy()
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    return target


def capture_walk_end(spec, adjacency, seed: int) -> dict:
    """exp108's instrumented executor, verbatim through the commit
    loop, returning the walk-end theta/V and the target (no settle)."""
    n = adjacency.shape[0]
    dt = star_dt(GAMMA, float(adjacency.sum(axis=1).max()))
    canon = _labeling_bfs_n(adjacency)
    target = _spec_target_n(spec, canon, n)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=GAMMA,
                        mu_theta=0.0)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(spec, n=n)
    if prog.rejected:
        return {"rejected": prog.rejected}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(24.0, dt=dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
    region_set = set(reg_walk)
    c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
    wound_center = float(np.mean(c.theta[reg_walk]))
    parent_of: dict[int, int] = {}
    frontier: list[int] = []
    for i in reg_walk:
        nbrs = [j for j in np.where(c.A[i] > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(
                nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = reg_idx[:1]
        parent_of[frontier[0]] = frontier[0]
    visited = set(frontier)
    order = [(i, parent_of[i]) for i in frontier]
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                queue.append(int(j))
    for i, src in order:
        for _ in range(8):
            c.step(dt)
        canon_src = getattr(c, "phi_spec_canon", None)
        if c.phi_spec[i] >= NEURAL_SPEC_MIN:
            theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
        elif canon_src is not None:
            theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
        else:
            theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    post_walk_err = round(float(np.sqrt(np.mean(
        (c.V - target) ** 2))), 2)
    return {"theta_end": c.theta.copy(), "V_end": c.V.copy(),
            "target": target, "post_walk_err": post_walk_err,
            "canon": canon}


def solve_static(A: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """The frozen-theta settle fixed point: (gamma I + L_G) V = gamma
    theta with L_G = g_gap (D - A). Dense solve — n <= 784."""
    n = A.shape[0]
    deg = A.sum(axis=1)
    L = np.diag(G_GAP * deg) - G_GAP * A
    M = GAMMA * np.eye(n) + L
    return GAMMA * np.linalg.solve(M, theta)


def band_power(e_torus: np.ndarray) -> dict:
    """Torus eigen-decomposition by fft2; power fractions by |k|
    band (angular frequency, radians/cell)."""
    r = e_torus.shape[0]
    E = np.fft.fft2(e_torus) / (r * r)
    p = np.abs(E) ** 2
    kx = np.fft.fftfreq(r) * 2 * np.pi
    KX, KY = np.meshgrid(kx, kx)
    K = np.sqrt(KX ** 2 + KY ** 2)
    tot = float(p.sum())
    if tot <= 0:
        return {"low": 0.0, "mid": 0.0, "high": 0.0}
    low = float(p[K <= np.pi / 2].sum()) / tot
    mid = float(p[(K > np.pi / 2) & (K <= 2.0)].sum()) / tot
    high = float(p[K > 2.0].sum()) / tot
    return {"low": round(low, 3), "mid": round(mid, 3),
            "high": round(high, 3)}


def static_report(A: np.ndarray, theta: np.ndarray, target: np.ndarray,
                  spec) -> dict:
    n = A.shape[0]
    V = solve_static(A, theta)
    e = V - target
    err = round(float(np.sqrt(np.mean(e * e))), 2)
    zone_mask = np.zeros(n, bool)
    a0 = int(round(spec.zones[0].f0 * n))
    a1 = int(round(spec.zones[-1].f1 * n))
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zone_mask[i0:i1] = True
    gap_mask = np.zeros(n, bool)
    gap_mask[a0:a1] = True
    gap_mask &= ~zone_mask
    intact_mask = ~(zone_mask | gap_mask)

    def rms(mask):
        if not bool(mask.any()):
            return None
        return round(float(np.sqrt(np.mean(e[mask] ** 2))), 2)

    r = int(round(np.sqrt(n)))
    bands = band_power(e.reshape(r, r))
    return {"err": err,
            "zone_rms": rms(zone_mask), "gap_rms": rms(gap_mask),
            "intact_rms": rms(intact_mask), "bands": bands}


def main() -> dict:
    print("=== exp109: the static field map ===\n")

    out: dict = {"real": {}, "idealized": {}, "canon_flat": {}}
    dyn_post_walk = {}

    for r in (10, 14, 20, 28):
        adj = torus(r, r)
        n = adj.shape[0]
        for s in SEEDS3:
            cap = capture_walk_end(MULTI, adj, s)
            rep = static_report(adj, cap["theta_end"],
                                cap["target"], MULTI)
            out["real"][f"n{n}_s{s}"] = rep
            dyn_post_walk[f"n{n}_s{s}"] = cap["post_walk_err"]
            print(f"    real     n={n:4d} s={s}  static {rep['err']:5.2f}"
                  f"  (dynamic post-walk {cap['post_walk_err']:5.2f})"
                  f"  bands {rep['bands']}")
        # idealized: theta = target exactly (intact = base canon)
        canon = _labeling_bfs_n(adj)
        target = _spec_target_n(MULTI, canon, n)
        rep = static_report(adj, target.copy(), target, MULTI)
        out["idealized"][f"n{n}"] = rep
        print(f"    idealized n={n:4d}      static {rep['err']:5.2f}"
              f"  bands {rep['bands']}")
        # canon_flat: gaps flattened to trunk
        cf = target.copy()
        a0 = int(round(MULTI.zones[0].f0 * n))
        a1 = int(round(MULTI.zones[-1].f1 * n))
        zm = np.zeros(n, bool)
        for z in MULTI.zones:
            i0 = int(round(z.f0 * n))
            i1 = max(int(round(z.f1 * n)), i0 + 1)
            zm[i0:i1] = True
        gap = np.zeros(n, bool)
        gap[a0:a1] = True
        gap &= ~zm
        cf[gap] = TRUNK_V
        rep = static_report(adj, cf, target, MULTI)
        out["canon_flat"][f"n{n}"] = rep
        print(f"    canon_flat n={n:4d}    static {rep['err']:5.2f}"
              f"  bands {rep['bands']}")

    # gates
    g1_misses = []
    for k, dv in dyn_post_walk.items():
        n = k.split("_")[0][1:]
        st = float(out["real"][k]["err"])
        if abs(st - dv) > 0.15:
            g1_misses.append((k, st, dv))
    sf_g1 = not g1_misses

    dom_bands = {}
    for n in SIZES:
        b = out["real"][f"n{n}_s1"]["bands"]
        dom_bands[n] = max(b, key=b.get)
    sf_g2 = True  # measurement gate: names, never fails

    def delta(arm):
        errs = [out[arm][f"n{n}"]["err"] for n in SIZES]
        return round(errs[-1] - errs[0], 2)

    d_ideal, d_flat = delta("idealized"), delta("canon_flat")
    shrink = round(1.0 - d_flat / d_ideal, 2) if d_ideal != 0 else 0.0
    sf_g3 = d_flat <= d_ideal * 0.6

    ideal100 = out["idealized"]["n100"]["err"]
    sf_g4 = ideal100 <= 1.0

    print(f"\n  SF-G1 static==dynamic (<= 0.15 mV): "
          f"{'PASS' if sf_g1 else 'REFUTED ' + str(g1_misses)}")
    print(f"  SF-G2 dominant bands by size: {dom_bands}")
    print(f"  SF-G3 canon-flat shrink {shrink} "
          f"(idealized delta {d_ideal:+.2f} -> flat {d_flat:+.2f}): "
          f"{'PASS' if sf_g3 else 'REFUTED'}")
    print(f"  SF-G4 clean-pattern floor (n=100 idealized "
          f"{ideal100} <= 1.0): {'PASS' if sf_g4 else 'REFUTED'}")

    npass = sum([sf_g1, sf_g3, sf_g4])
    print(f"\n  === {npass}/3 decision gates PASS "
          f"(SF-G2 names the band) ===")

    result = {
        "exp": "exp109_static_field_map",
        "arms": out,
        "dynamic_post_walk": dyn_post_walk,
        "deltas": {"idealized": d_ideal, "canon_flat": d_flat,
                   "shrink_frac": shrink},
        "dominant_bands": dom_bands,
        "criteria": {
            "SF_G1_instrument_validity": bool(sf_g1),
            "SF_G2_localization": {str(k): v
                                   for k, v in dom_bands.items()},
            "SF_G3_canon_flat_mechanism": bool(sf_g3),
            "SF_G4_clean_pattern_floor": bool(sf_g4),
        },
        "notes": (
            "The frozen-theta settle fixed point solved directly "
            "(V* = gamma(gamma I + L_G)^-1 theta) on captured real "
            "patterns, idealized patterns, and canon-flattened "
            "patterns; the error field eigen-decomposed on the "
            "torus's exact DFT modes and deposited by |k| band. "
            "Low-k = reservoir bleed across the span; mid-k = the "
            "canon diamond's wrap scatter; high-k = local kernel "
            "smearing of the zone-boundary discontinuities."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
