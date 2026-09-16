#!/usr/bin/env python3
"""exp90 — THE TWO-SOURCE READ (the canon-source repair for the exp89
chain-carry contamination; continuous batch; ledger L72).

THE REGISTERED REPAIR (L71/exp89 UC-G5): the multi-zone program's
below-line GAP cells (canon -50) inherit from the last committed
cell — which is the NOVEL zone (-30) — the M25 inheritance chain
carries THROUGH the novel zone and contaminates the canon gaps
(errs 5.77-8.5 mV on every substrate, bar 6.0). Root: the program's
write_spec_layer OVERWRITES the distributed memory (phi_spec := the
novel target), so the below-line cells' correct source — the canon
memory, the D3 distributed property — is gone; the chain is all
they have, and the chain is contaminated.

THE REPAIR, two pieces:
  1. write_spec_layer preserves the pre-program memory as
     phi_spec_canon (the core edit; additive — inert when no spec
     layer existed before).
  2. The walk's below-line commit reads the CANON memory:
       above-line cell -> the pole read (phi_spec[i], w=1.0)
       below-line cell -> the canon read (phi_spec_canon[i]) when
                          present; the inheritance chain otherwise.
     The canon read is the graph-native analog of the chain walk's
     face anchor (the face cell's expression IS the canon at the
     boundary). It is NOT the pole read — the M33 domain gate still
     refuses to write below-line NOVEL identities; the canon read
     restores the cell's own coordinate identity, nothing else.

PRE-REGISTERED GATES:

  TS-G1  THE CONTAMINATION CLOSES: the multi-zone program under the
         two-source read verifies on >= 6/7 substrates at the star
         point (the exp89 refutation flips), with the per-substrate
         errors deposited.
  TS-G2  THE POLE READ UNAFFECTED: the single-zone in-domain program
         still verifies on >= 6/7 substrates (the repair must not
         degrade the above-line path).
  TS-G3  NO BACKDOOR: the below-line NOVEL zone program STILL fails
         on >= 6/7 substrates — the canon read gives the cell its
         own coordinate identity (canon), never the novel spec; the
         M33 domain rule survives the repair intact.
  TS-G4  THE CANON SOURCE IS LOAD-BEARING: with the canon memory
         absent (no set_target before the write — the fallback
         path), the contamination RETURNS on the multi-zone program
         (>= 5/7 substrates fail) — the mechanism attribution: the
         canon source, not some other side effect of the repair.

RUN: 7 substrates x {multi, in-domain, out-of-domain, no-canon} x
2-3 seeds at the star point; serial, BLAS pinned.
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
    AnatomySpec, Zone, compile_anatomy, WINDOW_H,
)
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.substrate.graph import GraphCollective
from experiments.exp73_active_renormalization import make_battery, N
from experiments.exp73_active_renormalization import labeling_bfs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp90_two_source_read.json")

ERR_BAR = 6.0
STAR = {"gamma": 64.0, "mu": 0.0}


def star_dt(gamma: float, deg_max: float) -> float:
    return min(0.1, 1.2 / (gamma + deg_max))


def spec_target(spec: AnatomySpec, canon: np.ndarray) -> np.ndarray:
    target = canon.copy()
    for z in spec.zones:
        i0 = int(round(z.f0 * N))
        i1 = max(int(round(z.f1 * N)), i0 + 1)
        target[i0:i1] = z.voltage
    return target


def execute_two_source(spec: AnatomySpec, adjacency: np.ndarray,
                       seed: int, with_canon: bool = True) -> dict:
    gamma, mu = STAR["gamma"], STAR["mu"]
    dt = star_dt(gamma, float(adjacency.sum(axis=1).max()))
    canon = labeling_bfs(adjacency)
    target = spec_target(spec, canon)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(canon)              # the D3 memory (canon source)
    c.write_spec_layer(target)
    if not with_canon:
        # TS-G4's clean instrument: strip the canon SOURCE only (the
        # establishment, the clamps, the walk, and the dynamics are
        # identical) — the walk falls back to the inheritance chain
        if hasattr(c, "phi_spec_canon"):
            del c.phi_spec_canon
    prog = compile_anatomy(spec, n=N)
    if prog.rejected:
        return {"program_verified": False, "rejected": prog.rejected}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in spec.zones:
        i0 = int(round(z.f0 * N))
        i1 = max(int(round(z.f1 * N)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    canon_src = getattr(c, "phi_spec_canon", None) if with_canon else None
    if reg_idx:
        # the amputation removes the WHOLE range [first zone, last
        # zone] (a physical cut is contiguous); the walk rebuilds the
        # WHOLE range — F1 (in-run, correcting exp89's UC-G5
        # diagnosis): the multi program's errors were the amputated
        # but NEVER-REBUILT gap cells sitting at wound state, not
        # chain-carry contamination. The gap cells between zones are
        # amputated tissue and the regen walk must visit them; the
        # per-cell source gate (pole read above the line, canon read
        # below) then decides each identity.
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
            frontier = reg_walk[:1]
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
            elif canon_src is not None:
                theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
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
    print("=== exp90: the two-source read ===\n")

    battery = make_battery()
    substrates = ["path", "grid2d", "torus", "random3", "random6",
                  "scale_free", "small_world"]

    multi = AnatomySpec(
        zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
               Zone(f0=0.30, f1=0.45, voltage=-30.0, name="z1"),
               Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
        amputate_plane="trunk", spec_name="ts-multi", somatic_latch=False)
    in_dom = AnatomySpec(
        zones=[Zone(f0=0.05, f1=0.20, voltage=-30.0, name="z0")],
        amputate_plane="head", spec_name="ts-in", somatic_latch=False)
    out_dom = AnatomySpec(
        zones=[Zone(f0=0.05, f1=0.20, voltage=-59.0, name="z0")],
        amputate_plane="head", spec_name="ts-out", somatic_latch=False)

    # ---- TS-G1: the contamination closes ------------------------------------
    multi_res = {}
    multi_ok = 0
    for name in substrates:
        res = [execute_two_source(multi, battery[name], s)
               for s in (1, 2)]
        multi_res[name] = round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)
        multi_ok += int(np.mean([r["program_verified"]
                                 for r in res]) > 0.5)
    ts_g1 = bool(multi_ok >= 6)
    print(f"  TS-G1 multi-zone two-source: {multi_ok}/7 verify "
          f"(exp89: 1/7) -> {'PASS' if ts_g1 else 'REFUTED'}; "
          f"errors {multi_res}")

    # ---- TS-G2: the pole read unaffected -------------------------------------
    in_ok = 0
    for name in substrates:
        res = [execute_two_source(in_dom, battery[name], s)
               for s in (1, 2)]
        in_ok += int(np.mean([r["program_verified"]
                              for r in res]) > 0.5)
    ts_g2 = bool(in_ok >= 6)
    print(f"  TS-G2 in-domain pole read: {in_ok}/7 still verify -> "
          f"{'PASS' if ts_g2 else 'REFUTED'}")

    # ---- TS-G3: no backdoor -----------------------------------------------------
    out_fail = 0
    for name in substrates:
        res = [execute_two_source(out_dom, battery[name], s)
               for s in (1, 2)]
        out_fail += int(np.mean([r["program_verified"]
                                 for r in res]) < 0.5)
    ts_g3 = bool(out_fail >= 6)
    print(f"  TS-G3 below-line novel zone: fails on {out_fail}/7 "
          f"substrates (the canon read is not a backdoor) -> "
          f"{'PASS' if ts_g3 else 'REFUTED'}")

    # ---- TS-G4: the canon source is load-bearing ---------------------------------
    no_canon = {}
    nc_fail = 0
    for name in substrates:
        res = [execute_two_source(multi, battery[name], s,
                                  with_canon=False) for s in (1, 2)]
        no_canon[name] = round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)
        nc_fail += int(np.mean([r["program_verified"]
                                for r in res]) < 0.5)
    ts_g4 = bool(nc_fail >= 5)
    print(f"  TS-G4 no-canon fallback: the multi-zone program fails "
          f"on {nc_fail}/7 substrates -> "
          f"{'PASS' if ts_g4 else 'REFUTED'}; errors {no_canon}")

    out = {
        "exp": "exp90_two_source_read",
        "multi_errs": multi_res,
        "no_canon_errs": no_canon,
        "criteria": {
            "TS_G1_contamination_closes": ts_g1,
            "TS_G2_pole_read_unaffected": ts_g2,
            "TS_G3_no_backdoor": ts_g3,
            "TS_G4_canon_load_bearing": ts_g4,
        },
        "notes": (
            "The two-source read: the pole read (above-line, "
            "constitutive, w=1.0) + the canon read (below-line, the "
            "pre-program D3 memory preserved by write_spec_layer as "
            "phi_spec_canon). The canon read restores the cell's own "
            "coordinate identity — it is not a backdoor for "
            "below-line novel specs (the M33 domain rule survives "
            "intact). The graph-native analog of the chain walk's "
            "face anchor."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
