#!/usr/bin/env python3
"""exp108 — THE MEAN-FIELD DECOMPOSITION (ledger L89's registration:
noise DEAD (exp105), walk exposure DEAD (exp106), zone-band geometry
DEAD (exp107), window pinning HALVES the rise (gamma 16, delta +0.58,
level -2.7 mV) — "the residual lives in the window/settle mean-field
itself". This experiment decomposes that residual mechanically.

THE PHENOMENON: the torus's (4, 0) err rises with size — exp104
deposited 3.82 -> 4.86 (+1.04, seeds 1-3, the committed harness);
exp107's schedule variant read 3.73 -> 4.40 (+0.67). PROCESS NOTE
OWNED: exp107's script was never committed (results + ledger only) —
a discipline gap; this experiment re-grounds the base on the
COMMITTED harness (exp94's executor, exp105's call pattern: MULTI,
(4, 0), frontier_mode="walk", commit_noise 0.6, steps_per_cell 8,
seeds 1-3) and requires the in-run base delta >= +0.6 mV for the
arms to be comparable (MD-G0; both deposited trends clear it).

THE INSTRUMENT (a verbatim copy of exp94's execute_two_source_n,
exp97-repaired executor, with three additions and NO change to the
dynamics, RNG draw order, or step counts — the base arm is
step-for-step identical to the shared executor's 15 h settle):
  1. PHASE TRACES — err recorded at: post-window on the SURVIVOR
     set (cells outside the amputated span, vs their target — the
     window's shaping of the intact field), post-walk (full, right
     after the commit loop), and settle checkpoints {1, 3, 7, 15}
     h (segmented runs — identical step sequence to one 15 h call).
  2. CELL-CLASS DECOMPOSITION at the final read — RMS error by
     class: ZONE cells (the three -30 mV ranges), GAP cells (the
     amputated span between zones, committed to the canon field),
     INTACT cells (outside the span, window-shaped base field).
  3. ARMS that cut the candidate mechanisms apart:
       base         the phenomenon (checkpoints deposited)
       eps_freeze   c.eps = 0 from walk end: theta frozen, V
                    relaxes to the smoothed-theta fixed point —
                    a SIZE-INVARIANT kernel (gamma/g_gap only);
                    if the trend SURVIVES freeze, it is the
                    committed pattern's geometry (the canon
                    diamond vs node-id zone coarsening); if it
                    FLATTENS, the rise is the settle theta sag
                    (homeostatic drift under the mean-field V)
       long_settle  60 h settle (4x): transient vs fixed point —
                    delta(60 h) ~ delta(15 h) says the fixed
                    point itself is n-dependent; shrink says the
                    15 h read is a transient on the way down
       window48     48 h window (2x): if the n-scaling seeds in
                    the window's intact-field rewrite, doubling
                    the window DEEPENS the trend

PRE-REGISTERED GATES:

  MD-G0  (base reproduction) the in-run base verifies >= 2/3
         seeds at every size AND its delta (n=784 minus n=100)
         is >= +0.6 mV — the registered phenomenon reproduced on
         the committed harness; below that the arms say nothing
         about the registered trend (REFUTED = the trend was
         schedule-specific, itself a finding).
  MD-G1  (localization) the phase decomposition is deposited and
         the dominant carrier of the base trend is NAMED from
         the data: compare the post-walk delta to the final
         delta — post-walk carries it (seeded at commit/window)
         or the settle trace accrues it (drift). A measurement
         gate: it cannot fail, only name.
  MD-G2  (mechanism) at least one of {eps_freeze, long_settle}
         flattens the trend: delta <= +0.30 mV at the arm's own
         final read.
  MD-G3  (probe validity) every arm verifies >= 2/3 seeds at
         every size — a failing arm says nothing about trends.
  MD-G4  (arm level sanity) every arm's n=100 err within
         +/- 1.5 mV of the base n=100 err — flattening must be
         a TREND effect, not a level shift.

THE INTERPRETATION MATRIX (pre-registered):
  eps_freeze FLATTENS              -> exp109: the eps ladder +
                                      window-theta decomposition
  eps_freeze RISES, settle ~ flat  -> exp109: the canon-diamond
                                      arm (canon-flat gaps)
  long_settle FLATTENS             -> exp109: settle ladder to
                                      the fixed point
  window48 DEEPENS                 -> the window seeds it; the
                                      exp109 arm combines with
                                      whichever mechanism arm bit

RUN: 4 arms x 4 sizes x 3 seeds = 48 runs. Serial, BLAS pinned.
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
from experiments.exp94_multizone_scale import (
    ERR_BAR, MULTI, execute_two_source_n,
)
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp108_mean_field_decomposition.json")

SEEDS3 = (1, 2, 3)
SIZES = (100, 196, 400, 784)
OP = {"gamma": 4.0, "mu": 0.0}
CHECKPOINTS = (1.0, 3.0, 7.0, 15.0)
ARMS = {
    "base": dict(settle_h=15.0, freeze_eps=False, window_h=24.0,
                 checkpoints=CHECKPOINTS),
    "eps_freeze": dict(settle_h=15.0, freeze_eps=True, window_h=24.0,
                       checkpoints=CHECKPOINTS),
    "long_settle": dict(settle_h=60.0, freeze_eps=False, window_h=24.0,
                        checkpoints=(1.0, 3.0, 7.0, 15.0, 30.0, 60.0)),
    "window48": dict(settle_h=15.0, freeze_eps=False, window_h=48.0,
                     checkpoints=CHECKPOINTS),
}


def _rms(c, target, mask) -> float | None:
    if not bool(mask.any()):
        return None
    d = c.V[mask] - target[mask]
    return round(float(np.sqrt(np.mean(d * d))), 2)


def execute_instrumented(spec, adjacency, seed: int,
                         settle_h: float = 15.0,
                         freeze_eps: bool = False,
                         window_h: float = 24.0,
                         checkpoints: tuple = CHECKPOINTS) -> dict:
    """exp94's execute_two_source_n (exp97 frontier_mode="walk"
    branch) verbatim — same dynamics, same RNG draw order, same
    step counts — instrumented with phase traces, a cell-class
    decomposition, an eps freeze, a window-length dial, and a
    segmented settle (bit-identical step sequence). The anchor
    branch is dropped (unused at the (4, 0) cell)."""
    n = adjacency.shape[0]
    gamma, mu = OP["gamma"], OP["mu"]
    dt = star_dt(gamma, float(adjacency.sum(axis=1).max()))
    canon = _labeling_bfs_n(adjacency)
    target = _spec_target_n(spec, canon, n)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(spec, n=n)
    if prog.rejected:
        return {"program_verified": False, "rejected": prog.rejected,
                "err_vs_target": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(window_h, dt=dt)

    a0 = int(round(spec.zones[0].f0 * n))
    a1 = int(round(spec.zones[-1].f1 * n))
    surv = np.ones(n, bool)
    surv[a0:a1] = False
    survivor_err_post_window = _rms(c, target, surv)

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
    steps_per_cell = 8
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
    post_walk_err = round(c.pattern_error(target), 2)

    if freeze_eps:
        c.eps = 0.0
    done = 0.0
    settle_trace: dict[str, float] = {}
    for cp in sorted(checkpoints):
        if cp > settle_h:
            continue
        c.run(cp - done, dt=dt)
        done = cp
        settle_trace[f"t{cp:g}"] = round(c.pattern_error(target), 2)
    if done < settle_h:
        c.run(settle_h - done, dt=dt)
        settle_trace[f"t{settle_h:g}"] = round(c.pattern_error(target), 2)

    zone_mask = np.zeros(n, bool)
    per_zone = {}
    ok_all = True
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zone_mask[i0:i1] = True
        zmean = float(np.mean(c.V[i0:i1]))
        ok = abs(zmean - z.voltage) <= ERR_BAR
        per_zone[z.name] = {"mean": round(zmean, 1), "ok": bool(ok)}
        ok_all &= ok
    gap_mask = np.zeros(n, bool)
    gap_mask[a0:a1] = True
    gap_mask &= ~zone_mask
    intact_mask = ~(zone_mask | gap_mask)
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    classes = {
        "counts": {"zone": int(zone_mask.sum()),
                   "gap": int(gap_mask.sum()),
                   "intact": int(intact_mask.sum())},
        "zone_rms": _rms(c, target, zone_mask),
        "gap_rms": _rms(c, target, gap_mask),
        "intact_rms": _rms(c, target, intact_mask),
    }
    return {"program_verified": bool(ok_all), "per_zone": per_zone,
            "err_vs_target": round(err, 2),
            "post_walk_err": post_walk_err,
            "survivor_err_post_window": survivor_err_post_window,
            "settle_trace": settle_trace, "classes": classes}


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


def main() -> dict:
    print("=== exp108: the mean-field decomposition ===\n")

    out: dict[str, dict] = {}
    traces: dict[str, dict] = {}
    for arm, cfg in ARMS.items():
        for r in (10, 14, 20, 28):
            adj = torus(r, r)
            n = adj.shape[0]
            runs = [execute_instrumented(MULTI, adj, s, **cfg)
                    for s in SEEDS3]
            out[f"{arm}_n{n}"] = {
                "rate": round(float(np.mean(
                    [x["program_verified"] for x in runs])), 3),
                "err": round(float(np.mean(
                    [x["err_vs_target"] for x in runs])), 2),
                "post_walk_err": round(float(np.mean(
                    [x["post_walk_err"] for x in runs])), 2),
                "survivor_err_post_window": round(float(np.mean(
                    [x["survivor_err_post_window"] for x in runs])), 2),
            }
            traces[f"{arm}_n{n}"] = {
                "settle_trace": runs[0]["settle_trace"],
                "classes": runs[0]["classes"],
                "per_zone": runs[0]["per_zone"],
            }
            print(f"    {arm:12s} n={n:4d}  rate "
                  f"{out[f'{arm}_n{n}']['rate']:.2f}  err "
                  f"{out[f'{arm}_n{n}']['err']:5.2f}  "
                  f"(post-walk {out[f'{arm}_n{n}']['post_walk_err']:5.2f})")

    def delta(arm: str, field: str = "err") -> float:
        errs = [out[f"{arm}_n{n}"][field] for n in SIZES]
        return round(errs[-1] - errs[0], 2)

    base_delta = delta("base")
    arm_deltas = {a: delta(a) for a in ARMS}
    pw_delta = delta("base", "post_walk_err")

    md_g0 = (all(out[f"base_n{n}"]["rate"] >= 2 / 3 for n in SIZES)
             and base_delta >= 0.6)
    md_g2 = min(arm_deltas["eps_freeze"],
                arm_deltas["long_settle"]) <= 0.30
    md_g3 = all(out[k]["rate"] >= 2 / 3 for k in out)
    b100 = out["base_n100"]["err"]
    md_g4 = all(abs(out[f"{a}_n100"]["err"] - b100) <= 1.5
                for a in ARMS if a != "base")

    carrier = ("post-walk (seeded at commit/window — the settle "
               "preserves, not creates)" if abs(pw_delta) >= 0.5
               * abs(base_delta) else
               "settle accrual (the drift grows the trend)")
    md_g1 = True  # measurement gate: names, never fails

    print(f"\n  base delta {base_delta:+.2f} "
          f"(post-walk {pw_delta:+.2f}) — carrier: {carrier}")
    print(f"  arm deltas: {arm_deltas}")
    print(f"\n  MD-G0 base reproduction (>= +0.6, verify): "
          f"{'PASS' if md_g0 else 'REFUTED'}")
    print(f"  MD-G1 localization: {carrier}")
    print(f"  MD-G2 mechanism (a probe arm flattens <= +0.30): "
          f"{'PASS' if md_g2 else 'REFUTED'}")
    print(f"  MD-G3 probe validity: {'PASS' if md_g3 else 'REFUTED'}")
    print(f"  MD-G4 arm level sanity (+/- 1.5 of base {b100}): "
          f"{'PASS' if md_g4 else 'REFUTED'}")

    npass = sum([md_g0, md_g2, md_g3, md_g4])
    print(f"\n  === {npass}/4 decision gates PASS "
          f"(MD-G1 names the carrier) ===")

    result = {
        "exp": "exp108_mean_field_decomposition",
        "arms": out,
        "traces_seed1": traces,
        "deltas": {"base": base_delta, "post_walk": pw_delta,
                   **arm_deltas},
        "carrier": carrier,
        "criteria": {
            "MD_G0_base_reproduction": bool(md_g0),
            "MD_G1_localization": carrier,
            "MD_G2_mechanism": bool(md_g2),
            "MD_G3_probe_validity": bool(md_g3),
            "MD_G4_level_sanity": bool(md_g4),
        },
        "notes": (
            "The torus's (4, 0) size trend decomposed: phase "
            "traces (survivor post-window, post-walk, settle "
            "checkpoints), cell-class RMS (zone/gap/intact), and "
            "three mechanism arms (eps freeze, 60 h settle, 48 h "
            "window). eps_freeze separates pattern geometry "
            "(size-invariant smoothing kernel) from settle theta "
            "dynamics; long_settle separates transient from "
            "fixed point; window48 tests the window seed."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
