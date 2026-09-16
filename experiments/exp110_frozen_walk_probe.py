#!/usr/bin/env python3
"""exp110 — THE FROZEN-WALK PROBE (ledger L91's registration:
exp109's static instrument localized the torus's rising price to a
LOW-K component growing ~8x while clean geometry DECAYS with n —
the seed is the difference between the real committed field and the
clean one, and the only things in that difference are the EVOLVED
states of the cells. Commits are exact; the two evolution channels:
the 24 h window on the intact field (survivor err DECAYS with n —
2.79 -> 1.71, exonerated as the carrier) and the walk's inter-commit
steps (0.8n time units of wound-field (-30) exposure on the intact
reservoir — saturating at large n, nominally reconcilable with
exp106's spc-invariance only if the sag saturates by the spc=2
duration). This probe CUTS the two channels apart).

THE ARMS (static instrument throughout — solve, no settle):
  real        the exp109 capture verbatim (spc=8, seeds 1-3)
  frozen      the walk with the inter-commit steps REMOVED (spc=0:
              the intact field stays at its window output through
              the whole walk; commits still exact) — if the frozen
              arm's size delta flips to the idealized DECAY and its
              level drops >= 40%, the walk's wound-field exposure is
              NAMED as the seed carrier; if the trend survives
              (delta >= +0.6), the walk evolution is REFUTED and the
              class-split spectra point to the carrier
  idealized   theta = target exactly (exp109's decay reference,
              recomputed)

THE INSTRUMENT ADDITIONS:
  1. WALK-DRIFT EVIDENCE: RMS(theta_end - theta_start) on the INTACT
     cells per size per arm — the direct measurement of how much the
     intact reservoir moved during the walk (the frozen arm's is 0
     by construction; the real arm's n-scaling is the wound-exposure
     signature).
  2. CLASS-SPLIT SPECTRA: fft2 band fractions of (theta_end - target)
     computed SEPARATELY on the committed-span mask and the intact
     mask (zero-padded outside the mask — the mask leaks power
     between bands comparably across sizes; localization instrument,
     not an energy identity). The rising carrier is named by which
     mask's low-band power grows faster with n.

PRE-REGISTERED GATES:

  FW-G1  (localization) the frozen arm's static delta is <= 0 AND
         its mean level drops >= 40% below the real arm's mean ->
         the walk's wound-field exposure is the seed carrier
         (PASS = named). Frozen delta >= +0.6 -> the walk evolution
         is REFUTED as the carrier (the gate records the refutation
         and the class spectra carry to exp111).
  FW-G2  (class localization) the class-split low-band growth factor
         (n=784 / n=100) is deposited for both masks and the LARGER
         names the carrier (measurement gate — names, never fails).
  FW-G3  (probe sanity) every static error in the battery stays
         inside the 6.0 mV bar — probes that refuse say nothing
         about trends.

RUN: 4 sizes x {real, frozen} x 3 seeds captures + solves + 4
idealized solves. Serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp110_frozen_walk_probe.json")

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


def capture_walk_end(spec, adjacency, seed: int,
                     steps_per_cell: int = 8) -> dict:
    """exp109's capture with a steps_per_cell dial: 8 = the real
    walk, 0 = frozen (no inter-commit steps — the intact field is
    the window output for the whole walk)."""
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
    theta_start = c.theta.copy()
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
        for _ in range(steps_per_cell):
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
    zm = np.zeros(n, bool)
    a0 = int(round(spec.zones[0].f0 * n))
    a1 = int(round(spec.zones[-1].f1 * n))
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zm[i0:i1] = True
    gm = np.zeros(n, bool)
    gm[a0:a1] = True
    gm &= ~zm
    intact = ~(zm | gm)
    committed = zm | gm
    d_theta = c.theta - target
    intact_drift = round(float(np.sqrt(np.mean(
        (c.theta[intact] - theta_start[intact]) ** 2))), 2)
    return {"theta_end": c.theta.copy(), "target": target,
            "post_walk_err": round(float(np.sqrt(np.mean(
                (c.V - target) ** 2))), 2),
            "intact_drift": intact_drift,
            "masks": {"committed": committed, "intact": intact},
            "d_theta": d_theta}


def solve_static(A: np.ndarray, theta: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    deg = A.sum(axis=1)
    L = np.diag(G_GAP * deg) - G_GAP * A
    return GAMMA * np.linalg.solve(GAMMA * np.eye(n) + L, theta)


def band_fractions(field: np.ndarray, r: int) -> dict:
    E = np.fft.fft2(field.reshape(r, r)) / (r * r)
    p = np.abs(E) ** 2
    kx = np.fft.fftfreq(r) * 2 * np.pi
    KX, KY = np.meshgrid(kx, kx)
    K = np.sqrt(KX ** 2 + KY ** 2)
    tot = float(p.sum())
    if tot <= 0:
        return {"low": 0.0, "mid": 0.0, "high": 0.0, "abs_low": 0.0}
    low = float(p[K <= np.pi / 2].sum()) / tot
    mid = float(p[(K > np.pi / 2) & (K <= 2.0)].sum()) / tot
    high = float(p[K > 2.0].sum()) / tot
    return {"low": round(low, 3), "mid": round(mid, 3),
            "high": round(high, 3),
            "abs_low": round(float(p[K <= np.pi / 2].sum()), 2)}


def static_err(A, theta, target) -> float:
    V = solve_static(A, theta)
    return round(float(np.sqrt(np.mean((V - target) ** 2))), 2)


def main() -> dict:
    print("=== exp110: the frozen-walk probe ===\n")

    out: dict = {"real": {}, "frozen": {}, "idealized": {},
                 "spectra": {}, "walk_drift": {}}

    for r in (10, 14, 20, 28):
        adj = torus(r, r)
        n = adj.shape[0]
        for arm, spc in (("real", 8), ("frozen", 0)):
            errs = []
            for s in SEEDS3:
                cap = capture_walk_end(MULTI, adj, s,
                                       steps_per_cell=spc)
                e = static_err(adj, cap["theta_end"], cap["target"])
                errs.append(e)
                out["walk_drift"][f"{arm}_n{n}_s{s}"] = \
                    cap["intact_drift"]
                if s == 1:
                    dm = cap["masks"]
                    dt_f = cap["d_theta"]
                    spec_c = band_fractions(
                        np.where(dm["committed"], dt_f, 0.0), r)
                    spec_i = band_fractions(
                        np.where(dm["intact"], dt_f, 0.0), r)
                    out["spectra"][f"{arm}_n{n}"] = {
                        "committed": spec_c, "intact": spec_i}
            out[arm][f"n{n}"] = round(float(np.mean(errs)), 2)
            print(f"    {arm:8s} n={n:4d}  static {out[arm][f'n{n}']:5.2f}"
                  f"  intact-walk-drift "
                  f"{out['walk_drift'][f'{arm}_n{n}_s1']:5.2f}")
        canon = _labeling_bfs_n(adj)
        target = _spec_target_n(MULTI, canon, n)
        out["idealized"][f"n{n}"] = static_err(adj, target.copy(),
                                               target)
        print(f"    idealized n={n:4d}  static "
              f"{out['idealized'][f'n{n}']:5.2f}")

    def delta(arm):
        errs = [out[arm][f"n{n}"] for n in SIZES]
        return round(errs[-1] - errs[0], 2)

    d_real, d_frozen, d_ideal = (delta("real"), delta("frozen"),
                                 delta("idealized"))
    lvl_real = float(np.mean([out["real"][f"n{n}"] for n in SIZES]))
    lvl_frozen = float(np.mean([out["frozen"][f"n{n}"]
                                for n in SIZES]))
    drop = round(1.0 - lvl_frozen / lvl_real, 2)

    named = None
    if d_frozen <= 0 and drop >= 0.40:
        named = ("the walk's wound-field exposure IS the seed "
                 "carrier (frozen walk collapses the trend and the "
                 "level)")
    elif d_frozen >= 0.6:
        named = ("the walk evolution is REFUTED as the carrier — "
                 "the window output / committed cells carry; "
                 "exp111 reads the class-split spectra")
    else:
        named = ("MIXED — partial contribution; the class-split "
                 "spectra arbitrate in exp111")
    fw_g1 = d_frozen <= 0 and drop >= 0.40

    def low_growth(arm):
        sp = out["spectra"]
        a = sp[f"{arm}_n100"], sp[f"{arm}_n784"]
        return {
            "committed": round(a[1]["committed"]["abs_low"]
                               / max(a[0]["committed"]["abs_low"],
                                     1e-9), 2),
            "intact": round(a[1]["intact"]["abs_low"]
                            / max(a[0]["intact"]["abs_low"], 1e-9),
                            2),
        }

    growth = {"real": low_growth("real"), "frozen": low_growth("frozen")}
    fw_g2 = True  # measurement gate
    all_errs = ([out[a][f"n{n}"] for a in ("real", "frozen",
                                           "idealized")
                 for n in SIZES])
    fw_g3 = all(e < 6.0 for e in all_errs)

    print(f"\n  deltas: real {d_real:+.2f} | frozen {d_frozen:+.2f} "
          f"| idealized {d_ideal:+.2f}")
    print(f"  levels: real {lvl_real:.2f} -> frozen {lvl_frozen:.2f} "
          f"(drop {drop})")
    print(f"  low-band growth (n784/n100): {growth}")
    print(f"\n  FW-G1 localization: {named}")
    print(f"  FW-G2 class spectra: deposited (see growth above)")
    print(f"  FW-G3 probe sanity (< 6.0 bar): "
          f"{'PASS' if fw_g3 else 'REFUTED'}")

    npass = sum([fw_g1, fw_g3])
    print(f"\n  === {npass}/2 decision gates PASS ===")

    result = {
        "exp": "exp110_frozen_walk_probe",
        "arms": out,
        "deltas": {"real": d_real, "frozen": d_frozen,
                   "idealized": d_ideal},
        "levels": {"real": round(lvl_real, 2),
                   "frozen": round(lvl_frozen, 2), "drop": drop},
        "low_band_growth": growth,
        "criteria": {"FW_G1_localization": named,
                     "FW_G2_class_spectra": "deposited",
                     "FW_G3_probe_sanity": bool(fw_g3)},
        "notes": (
            "The walk's inter-commit steps cut (spc=0) with the "
            "static instrument: separates the wound-field exposure "
            "channel from the window-output channel; class-split "
            "spectra of (theta_end - target) deposited per arm per "
            "size with absolute low-band power for the growth "
            "comparison."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
