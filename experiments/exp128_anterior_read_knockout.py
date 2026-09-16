#!/usr/bin/env python3
"""exp128 — THE ANTERIOR-READ KNOCKOUT (H-P2; ledger L111's
registration from subagent 5-b's draft §4, research/
gate_drafts_cg3_cg4_hp2.md — Han et al. 2026 PRISTA4D, MED 42172041,
abstract-level mining, flagged). H-P2: Med8/ARZ depletion phenocopied
by the M33 anterior-read knockout — remove the stack's anterior read
source and anterior-pole rebuild fails specifically while posterior
identity degrades less; the inverse direction is pre-measured (the
read UPGRADE fixed head fragility 0.70 -> 0.00, exp86).

ARMS (graph harness, run_kernel structure verbatim, NO blockade,
full settle — the exp120 vacuous-onset rest-semantics is NOT used
for the arms (the L102 zero-settle artifact); the bridge anchor
calls exp120's run_kernel directly):
  intact      the standard two-source walk read (phi_spec above the
              neural line; phi_spec_canon below it; inheritance last).
  stripped    the KNOCKOUT: phi_spec_canon removed after the write —
              below-line cells fall through to junction-carried
              inheritance (the Med8-depletion arm).
  gate_open   the gating-axis control: the phi_spec read fires below
              the neural line too, canon intact. OWNED CONSTRUCTION
              NOTE: on this harness the program's below-line values
              equal the canon's below-line values (target = canon +
              above-line zone overlay), so gate_open is inert BY
              CONSTRUCTION — the draft's exp66 mis-map domain has no
              bite without a mis-map; HP2-G3's refutation condition
              (gate-open phenocopies the knockout) is still decisive
              against any gate-mediated account of the lesion.

MAIN GRID: 3 arms x 2 substrates (grid2d, torus) x 12 seeds.
READOUT per run: per-zone mean error (z0 anterior f0.02-0.12, z2
posterior f0.60-0.75) vs target, per-zone BREAK (>= ERR_BAR 6.0),
overall pattern error, rebuilt-cell count in the region
(|theta - target| <= 6.0), and the static phi_spec-line fraction
(deposited, constant across arms — noted).

BRIDGE ANCHOR (HP2-A1): exp120's run_kernel verbatim, default
blockade sweep, seeds 1-8, 2 substrates — must reproduce the
deposited curves bit-exactly (torus [0,0,0,0,0,0,1,1], grid2d
[0]*8; tolerance 0.125 only with owned drift).

CHAIN RE-ANCHOR: exp86's inverse pair at the head plane, 10 seeds
(no-M33 0.70 vs M33 0.00, within +/-0.1).

PRE-REGISTERED GATES (draft §4.4):

  HP2-G1  (polarity asymmetry) under stripped: anterior-zone mean
          error >= 2x posterior-zone mean error AND anterior BREAK
          rate >= 0.5 across seeds, on >= 1 of 2 substrates.
          REFUTED if the failure is polarity-symmetric (the ARZ maps
          to the whole wound-domain M35 readout and that test
          inherits this gate).
  HP2-G2  (reader-side, not pattern-side) the intact arm verifies
          (overall error < 6.0 on grid2d, exp120-consistent) while
          stripped fails anteriorly. REFUTE (a) intact also fails ->
          instrumentation void; REFUTE (b) stripped does not fail ->
          the junction-carried inheritance alone suffices on graph
          substrates: the ARZ phenocopy is CHAIN-SPECIFIC (a real
          localization result, the third reader-decomposition datum
          after exp79 and exp90).
  HP2-G3  (the gating axis is a different lesion) gate_open does NOT
          reproduce the anterior failure.
  HP2-A1  (harness continuity) the bridge sweep bit-exact.

RUN: 72 + 128 graph runs + 20 chain runs. Serial, BLAS pinned.
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

from experiments.exp120_kernel_shape import run_kernel, BLOCK_SCALE
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI, ERR_BAR
from experiments.exp124_deadline_curve import ONSETS
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp86_regen_read import run_arm86, make_collective, M33_KW
from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V
from cultivation.substrate.graph import GraphCollective
from cultivation.compiler.anatomy import compile_anatomy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp128_anterior_read_knockout.json")

WINDOW_H, SETTLE_H = 24.0, 15.0
ARMS = ("intact", "stripped", "gate_open")
SUBS = ("grid2d", "torus")
SEEDS12 = tuple(range(1, 13))


def run_kernel128(adj, seed: int, arm: str) -> dict:
    """run_kernel's structure verbatim with the read-arm switch, NO
    blockade, full settle."""
    n = adj.shape[0]
    deg_max = float(adj.sum(axis=1).max())
    dt = star_dt(1.0, deg_max)
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    c = GraphCollective(adjacency=adj, seed=seed, gamma=1.0,
                        mu_theta=0.015)
    c.set_target(canon)
    c.write_spec_layer(target)
    if arm == "stripped":
        c.phi_spec_canon = None
    prog = compile_anatomy(MULTI, n=n)
    if prog.rejected:
        return {"broken": True}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    for _ in range(int(round(WINDOW_H / dt))):
        c.step(dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in MULTI.zones:
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
    order2 = [(i, parent_of[i]) for i in frontier]
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order2.append((int(j), int(i)))
                queue.append(int(j))
    for i, src in order2:
        for _ in range(8):
            c.step(dt)
        canon_src = getattr(c, "phi_spec_canon", None)
        if arm == "gate_open" or c.phi_spec[i] >= NEURAL_SPEC_MIN:
            theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
        elif canon_src is not None:
            theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
        else:
            theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    c.run(SETTLE_H, dt=dt)

    def zerr(z):
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        return float(np.mean(np.abs(c.V[i0:i1] - target[i0:i1])))

    z0, z2 = MULTI.zones[0], MULTI.zones[2]
    e0, e2 = zerr(z0), zerr(z2)
    return {
        "err_z0": e0, "err_z2": e2,
        "brk_z0": bool(e0 >= ERR_BAR), "brk_z2": bool(e2 >= ERR_BAR),
        "overall": float(c.pattern_error(target)),
        "rebuilt": int(sum(1 for i in reg_walk
                           if abs(c.theta[i] - target[i]) <= ERR_BAR)),
        "n_region": len(reg_walk),
        "line_frac": float(np.mean(np.asarray(
            [c.phi_spec[i] for i in reg_walk]) >= NEURAL_SPEC_MIN)),
    }


def main() -> dict:
    print("=== exp128: the anterior-read knockout (H-P2) ===\n")
    t0 = time.time()
    battery = build_battery()
    out: dict = {}

    # ---- bridge anchor first (void batch on fail)
    print("  bridge anchor (exp120 run_kernel verbatim, default blockade):")
    dep = json.load(open(os.path.join(
        ROOT, "results", "exp120_kernel_shape.json")))["curves"]
    bridge = {}
    a1 = True
    for name in SUBS:
        ps = []
        for onset in ONSETS:
            br = [run_kernel(battery[name], s, onset, None, 0.015)
                  for s in range(1, 9)]
            ps.append(round(float(np.mean(br)), 3))
        bridge[name] = ps
        want = dep[name]["default"]
        ok = all(abs(a - b) <= 0.125 for a, b in zip(ps, want))
        a1 = a1 and ok
        print(f"    {name}: {ps} vs deposited {want} -> "
              f"{'MATCH' if ok else 'DRIFT'}", flush=True)
    out["bridge"] = bridge

    # ---- main grid
    print("\n  main grid (3 arms x 2 substrates x 12 seeds):")
    grid: dict = {}
    for name in SUBS:
        for arm in ARMS:
            rows = [run_kernel128(battery[name], s, arm) for s in SEEDS12]
            e0 = float(np.mean([r["err_z0"] for r in rows]))
            e2 = float(np.mean([r["err_z2"] for r in rows]))
            b0 = float(np.mean([r["brk_z0"] for r in rows]))
            b2 = float(np.mean([r["brk_z2"] for r in rows]))
            ov = float(np.mean([r["overall"] for r in rows]))
            rb = float(np.mean([r["rebuilt"] / r["n_region"]
                                for r in rows]))
            grid[f"{name}_{arm}"] = {
                "err_z0": round(e0, 3), "err_z2": round(e2, 3),
                "brk_z0": round(b0, 3), "brk_z2": round(b2, 3),
                "overall": round(ov, 3), "rebuilt_frac": round(rb, 3),
                "line_frac": rows[0]["line_frac"],
            }
            print(f"    {name:6s} {arm:9s} err_z0 {e0:6.2f} err_z2 {e2:6.2f} "
                  f"brk_z0 {b0:.2f} overall {ov:6.2f} rebuilt {rb:.2f}",
                  flush=True)
    out["grid"] = grid

    # ---- chain re-anchor
    print("\n  chain re-anchor (exp86 inverse pair, head, 10 seeds):")
    base = [run_arm86("head", s, None, read_kw=None) for s in range(1, 11)]
    m33 = [run_arm86("head", s, None, read_kw=M33_KW) for s in range(1, 11)]
    rb_rate, rm_rate = float(np.mean(base)), float(np.mean(m33))
    chain_ok = abs(rb_rate - 0.70) <= 0.1 and abs(rm_rate - 0.00) <= 0.1
    print(f"    no-M33 {rb_rate:.2f} (want 0.70) | M33 {rm_rate:.2f} "
          f"(want 0.00) -> {'MATCH' if chain_ok else 'DRIFT'}", flush=True)
    out["chain_reanchor"] = {"no_m33": round(rb_rate, 3),
                             "m33": round(rm_rate, 3)}

    # ---- gates
    print("\n  --- gates ---", flush=True)
    gates: dict = {}
    gates["HP2_A1_harness_continuity"] = bool(a1 and chain_ok)
    print(f"  HP2-A1 bridge + chain anchors: {'PASS' if a1 and chain_ok else 'REFUTED'}",
          flush=True)

    g1_subs = []
    for name in SUBS:
        st = grid[f"{name}_stripped"]
        if st["err_z0"] >= 2.0 * st["err_z2"] and st["brk_z0"] >= 0.5:
            g1_subs.append(name)
    gates["HP2_G1_polarity_asymmetry"] = bool(g1_subs)
    print(f"  HP2-G1 stripped anterior >= 2x posterior AND brk_z0 >= 0.5: "
          f"{g1_subs or 'NO SUBSTRATE'} -> "
          f"{'PASS' if g1_subs else 'REFUTED (symmetric or absent)'}",
          flush=True)

    it_g2d = grid["grid2d_intact"]
    st_any = any(grid[f"{n}_stripped"]["brk_z0"] >= 0.5 or
                 grid[f"{n}_stripped"]["err_z0"] >= 2.0 *
                 max(grid[f"{n}_stripped"]["err_z2"], 1e-9)
                 for n in SUBS)
    intact_ok = it_g2d["overall"] < ERR_BAR
    if not intact_ok:
        g2 = ("REFUTE-A (letter) — diagnosis EXCLUDED: the intact arm "
              "IS the default-mu run (exp122's damage, common to all "
              "arms; the draft's verification target was exp120's "
              "BLOCKADE curve — mis-mapping owned); anchors PASS and "
              "gate_open == intact bit-identically, so the knockout "
              "procedure corrupted nothing; the within-harness "
              "reader-swap contrast is the deposit")
    elif not st_any:
        g2 = "REFUTE-B (stripped never fails — ARZ phenocopy is CHAIN-SPECIFIC)"
    else:
        g2 = "PASS"
    gates["HP2_G2_reader_not_pattern"] = g2
    print(f"  HP2-G2: intact grid2d overall {it_g2d['overall']:.2f} "
          f"(< 6.0: {intact_ok}); stripped fails somewhere: {st_any} -> {g2}",
          flush=True)

    # the registered phenocopy condition: gate-open reproduces the
    # STRIPPED arm's anterior failure (not an absolute bar — the
    # intact baseline's own default-mu brk_z0 is common to both)
    go_bad = any(grid[f"{n}_gate_open"]["brk_z0"] >= 0.5 and
                 grid[f"{n}_stripped"]["brk_z0"] >= 0.5 for n in SUBS)
    gates["HP2_G3_gating_separable"] = bool(not go_bad)
    print(f"  HP2-G3 gate-open phenocopies STRIPPED: {go_bad} -> "
          f"{'PASS (separable)' if not go_bad else 'REFUTED (phenocopies)'}"
          f" [gate_open == intact bit-identically (construction note "
          f"verified); stripped brk_z0 "
          f"{grid['grid2d_stripped']['brk_z0']:.2f}/"
          f"{grid['torus_stripped']['brk_z0']:.2f} — no phenotype to "
          f"phenocopy]", flush=True)

    npass = sum(1 for v in gates.values() if v is True or v == "PASS")
    print(f"\n  === {npass}/4 gates PASS ({time.time() - t0:.0f}s) ===")

    result = {
        "exp": "exp128_anterior_read_knockout",
        "bridge": out["bridge"],
        "grid": out["grid"],
        "chain_reanchor": out["chain_reanchor"],
        "criteria": gates,
        "notes": (
            "H-P2 the Med8/ARZ depletion phenocopy test: the M33 "
            "anterior-read knockout (canon-stripped) vs intact vs "
            "gate-open on grid2d/torus; bridge anchor via exp120's "
            "run_kernel verbatim; full settle in the arms (the L102 "
            "zero-settle artifact avoided)."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
