#!/usr/bin/env python3
"""exp89 — THE UNIVERSAL COMPILER (the substrate-conditioned
operating point; continuous batch; ledger L71).

THE ARC: exp43 measured that the mechanism is universal but the FORM
is substrate-conditioned (the head|trunk partition exists on
path/grid, fails on random3/scale_free). exp47 compiled that into
R5 (the partition's boundary-to-volume refusal). exp79 crossed the
star: (gamma=64, mu=0) writes ANY substrate with zero remodeling —
and exp81 wired the escape into the compiler for WRITE programs
(35/35 scale_free refusals verify at the star point). exp87
connected the REGEN reader (the R1 memory write + the M33-gated read
+ the star point) on the chain and grid.

THE OPEN QUESTION: is the R5 refusal OPERATING-POINT-CONDITIONAL for
the full program INCLUDING regeneration? The two-channel law says
yes: the refusal is a writability statement, and the star point
buys writability on any substrate. If the regen path verifies at the
star point on the refused substrates and FAILS at the default
operating point exactly where R5 says it must, then the compiler's
refusal is not a wall but a PRICE TAG — R5' (the conditional rule):
"this partition is not writable at your operating point; the star
point buys it."

THE DESIGN: exp87's v5 program semantics (the R1 memory write, the
M33-gated reader at w=1.0, the star operating point) executed across
the full 7-substrate battery (exp73's battery, verbatim), with the
per-substrate canon (the BFS-order labeling — exp43's framing: the
body coordinates ARE the BFS order) and the BFS regen walk with the
per-cell domain gate.

PRE-REGISTERED GATES:

  UC-G1  THE R5 SIGNATURE AT DEFAULT: at the default operating
         point (gamma=1, mu=0.015), the in-domain single-zone
         program's verification agrees with the compiler's own R5
         partition check on >= 90% of the battery (the refused
         substrates fail, the passing ones verify — the law's
         necessity side).
  UC-G2  THE STAR LIFT: at the star point, the same program
         verifies on >= 6/7 substrates — the refusal lifts; R5' is
         born (a refusal becomes operating-point-conditional).
  UC-G3  THE DOMAIN IS SUBSTRATE-INDEPENDENT: the below-line zone
         fails on >= 6/7 substrates EVEN at the star point (the M33
         gate is identity-based, not connectivity-based — the read's
         domain does not move with the substrate).
  UC-G4  STABILITY ON THE REFUSED SUBSTRATES: the star-point
         programs hold 100 generations on the R5-refused substrates,
         >= 3/4.
  UC-G5  THE MULTI-REGION READER GENERALIZES: the multi-zone
         program verifies on >= 5/7 substrates at the star point.

RUN: 7 substrates x (2 operating points x 3 seeds) + the domain arm
+ stability + multi-region; serial, BLAS pinned.
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

from cultivation.compiler.anatomy import (
    AnatomySpec, Zone, compile_anatomy, substrate_partition_check,
    WINDOW_H,
)
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import GraphCollective
from experiments.exp73_active_renormalization import make_battery, N
from experiments.exp73_active_renormalization import labeling_bfs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp89_universal_compiler.json")

ERR_BAR = 6.0
STAR = {"gamma": 64.0, "mu": 0.0}
DEFAULT = {"gamma": 1.0, "mu": 0.015}


def star_dt(gamma: float, deg_max: float) -> float:
    return min(0.1, 1.2 / (gamma + deg_max))


def spec_target(spec: AnatomySpec, canon: np.ndarray) -> np.ndarray:
    target = canon.copy()
    for z in spec.zones:
        i0 = int(round(z.f0 * N))
        i1 = max(int(round(z.f1 * N)), i0 + 1)
        target[i0:i1] = z.voltage
    return target


def execute_universal(spec: AnatomySpec, adjacency: np.ndarray,
                      seed: int, op: dict) -> dict:
    """The v5 program semantics on an arbitrary substrate: the R1
    memory write, the clamps, the amputation of the zone-bearing
    region, the BFS regen walk with the per-cell M33 gate at w=1.0,
    at the given operating point."""
    gamma, mu = op["gamma"], op["mu"]
    dt = star_dt(gamma, float(adjacency.sum(axis=1).max()))
    canon = labeling_bfs(adjacency)
    target = spec_target(spec, canon)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(spec, n=N)
    if prog.rejected:
        return {"program_verified": False, "rejected": prog.rejected}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=dt)
    c.release_clamps()
    # amputate the union of the ZONE regions (the program's regen
    # target) — ALL zones regardless of domain: the amputation is the
    # trigger, not a domain statement (F1, in-run: filtering the
    # regen region by domain turned the below-line program into a
    # write-only program — the clamps verified without any regen).
    reg_idx: list[int] = []
    for z in spec.zones:
        i0 = int(round(z.f0 * N))
        i1 = max(int(round(z.f1 * N)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    if reg_idx:
        region_set = set(reg_idx)
        c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
        # BFS walk (regrow_graph structure) with the per-cell gate
        wound_center = float(np.mean(c.theta[reg_idx]))
        steps_per_cell = 8
        parent_of: dict[int, int] = {}
        frontier: list[int] = []
        for i in reg_idx:
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
            if c.phi_spec[i] >= NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
            c.theta[i] = theta_new
            c.V[i] = theta_new
    c.run(15.0, dt=dt)
    per_zone = {}
    ok_all = True
    for z in spec.zones:
        i0 = int(round(z.f0 * N))
        i1 = max(int(round(z.f1 * N)), i0 + 1)
        zmean = float(np.mean(c.V[i0:i1]))
        ok = abs(zmean - z.voltage) <= ERR_BAR
        per_zone[z.name] = {"mean": round(zmean, 1), "ok": bool(ok),
                            "in_domain": bool(z.voltage >= NEURAL_SPEC_MIN)}
        ok_all &= ok
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    return {"program_verified": bool(ok_all), "per_zone": per_zone,
            "err_vs_target": round(err, 2)}


def main() -> dict:
    print("=== exp89: the universal compiler ===\n")

    battery = make_battery()
    substrates = ["path", "grid2d", "torus", "random3", "random6",
                  "scale_free", "small_world"]

    in_dom = AnatomySpec(
        zones=[Zone(f0=0.05, f1=0.20, voltage=-30.0, name="z0")],
        amputate_plane="head", spec_name="uc-in", somatic_latch=False)
    out_dom = AnatomySpec(
        zones=[Zone(f0=0.05, f1=0.20, voltage=-59.0, name="z0")],
        amputate_plane="head", spec_name="uc-out", somatic_latch=False)
    multi = AnatomySpec(
        zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
               Zone(f0=0.30, f1=0.45, voltage=-30.0, name="z1"),
               Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
        amputate_plane="trunk", spec_name="uc-multi", somatic_latch=False)

    # the compiler's own R5 classification per substrate
    r5 = {}
    for name in substrates:
        chk = substrate_partition_check(in_dom, battery[name])
        r5[name] = chk["substrate_compilable"]
    print(f"  R5 partition check: "
          f"{ {k: v for k, v in r5.items()} }")

    # ---- UC-G1: the R5 signature at the default operating point -----------
    agree = 0
    default_res = {}
    for name in substrates:
        res = [execute_universal(in_dom, battery[name], s, DEFAULT)
               for s in (1, 2, 3)]
        ok = float(np.mean([r["program_verified"] for r in res])) > 0.5
        default_res[name] = round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)
        agree += int(ok == r5[name])
    uc_g1 = bool(agree / len(substrates) >= 0.9)
    print(f"  UC-G1 R5 signature at default: {agree}/7 agree -> "
          f"{'PASS' if uc_g1 else 'REFUTED'}; errs {default_res}")

    # ---- UC-G2: the star lift ---------------------------------------------
    star_res = {}
    star_ok = 0
    for name in substrates:
        res = [execute_universal(in_dom, battery[name], s, STAR)
               for s in (1, 2, 3)]
        star_res[name] = round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)
        star_ok += int(np.mean([r["program_verified"]
                                for r in res]) > 0.5)
    uc_g2 = bool(star_ok >= 6)
    print(f"  UC-G2 star lift: {star_ok}/7 verify at the star point -> "
          f"{'PASS' if uc_g2 else 'REFUTED'}; errs {star_res}")

    # ---- UC-G3: the domain is substrate-independent --------------------------
    dom_fail = 0
    for name in substrates:
        res = [execute_universal(out_dom, battery[name], s, STAR)
               for s in (1, 2)]
        dom_fail += int(np.mean([r["program_verified"]
                                 for r in res]) < 0.5)
    uc_g3 = bool(dom_fail >= 6)
    print(f"  UC-G3 domain independence: the below-line program fails "
          f"on {dom_fail}/7 substrates at the star point -> "
          f"{'PASS' if uc_g3 else 'REFUTED'}")

    # ---- UC-G5: the multi-region reader generalizes --------------------------
    multi_ok = 0
    multi_errs = {}
    for name in substrates:
        res = [execute_universal(multi, battery[name], s, STAR)
               for s in (1, 2)]
        multi_errs[name] = round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)
        multi_ok += int(np.mean([r["program_verified"]
                                 for r in res]) > 0.5)
    uc_g5 = bool(multi_ok >= 5)
    print(f"  UC-G5 multi-region: {multi_ok}/7 substrates verify -> "
          f"{'PASS' if uc_g5 else 'REFUTED'}; errs {multi_errs}")

    # ---- UC-G4: stability on the refused substrates ---------------------------
    refused = [n for n in substrates if not r5[n]][:4]
    hold_ok = 0
    for name in refused:
        canon = labeling_bfs(battery[name])
        target = spec_target(in_dom, canon)
        gamma, mu = STAR["gamma"], STAR["mu"]
        dt = star_dt(gamma, float(battery[name].sum(axis=1).max()))
        c = GraphCollective(adjacency=battery[name], seed=2, gamma=gamma,
                            mu_theta=mu)
        c.set_target(canon)
        c.write_spec_layer(target)
        c.set_state(target.copy())
        c.theta = target.copy()
        c.run(100.0, dt=dt)
        e = float(c.pattern_error(target))
        hold_ok += int(e < ERR_BAR)
    uc_g4 = bool(refused and hold_ok >= 3)
    print(f"  UC-G4 stability on refused substrates: {hold_ok}/"
          f"{len(refused)} hold 100 generations -> "
          f"{'PASS' if uc_g4 else 'REFUTED'}")

    out = {
        "exp": "exp89_universal_compiler",
        "r5_classification": r5,
        "default_errs": default_res,
        "star_errs": star_res,
        "multi_errs": multi_errs,
        "criteria": {
            "UC_G1_r5_signature_at_default": uc_g1,
            "UC_G2_star_lift": uc_g2,
            "UC_G3_domain_substrate_independent": uc_g3,
            "UC_G4_stability_refused": uc_g4,
            "UC_G5_multi_region_generalizes": uc_g5,
        },
        "notes": (
            "R5' (the conditional rule, if the gates hold): the "
            "partition refusal is an OPERATING-POINT statement — the "
            "default operating point reproduces the exp43 signature, "
            "the star point lifts it on every substrate. The "
            "compiler's refusal output becomes a price tag: 'not "
            "writable at your operating point; the star architecture "
            "buys it.' The M33 read's domain (the neural line) is "
            "identity-based and does NOT move with the substrate — "
            "the domain rule and the operating-point rule are "
            "orthogonal."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/5 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
