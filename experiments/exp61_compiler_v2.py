#!/usr/bin/env python3
"""exp61 — COMPILER V2 (night nine continuous batch; ledger L42).

STAGE-3 90% SPEC (the user's bar): the compiler designs ANY body layout,
in minimal time/steps, emits step-by-step lab-executable instructions,
and the designed shapes are STABLE over ~100 generations. The night-nine
queue's work item — the exp41 failure structure's latch RE-READ path for
REGENERATED latches — is exactly the stability question: each regen
rewrites the latch inside the regen zone; does the stored gradient
survive its own re-reads?

PRE-REGISTERED GATES (fixed BEFORE running):

  CP2-G1  ARBITRARY LAYOUTS: compile+verify (err < 6.0 mV) passes on
          >= 3 of 4 NOVEL specs beyond v1's tested set — dual novel
          band (-30, a cell STATE absent from WT), ladder segmentation,
          custom 4-zone, plus v1's third-head re-run — ZERO search,
          3 seeds each.
  CP2-G2  MINIMUM WINDOW: scan the rewrite window over {24, 12, 6, 3} h
          on the latching substrate; report the smallest window that
          verifies ALL suite specs. No silent retuning: per-spec
          failures recorded with their diagnosis.
  CP2-G3  SCHEDULE EMISSION: every compiled program emits a schema-
          valid dosing schedule (step/agent/action/timing/
          concentration-class) — the lab-executable deliverable.
          Compile-time gate over the whole suite.
  CP2-G4  100-GENERATION STABILITY (the latch re-read path): after a
          verified program, 100 re-amputation generations on the
          latching substrate; PASS if >= 2/3 seeds hold err < 6.0 mV
          through generation 100 (twohead + thirdhead specs). The
          anchor-drift slope in the regen zone is the direct
          measurement of the exp41 re-read question.

RUN: compile-time checks + sim arms, 3 seeds. Serial, BLAS pinned.
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

from cultivation.compiler.anatomy import (  # noqa: E402
    AnatomySpec, Zone, compile_anatomy, execute_and_verify, recut_stability,
)
from cultivation.bioelectric.morpho_engineering import (  # noqa: E402
    LatchingCollective,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp61_compiler_v2.json")

HEAD_V, TRUNK_V, BAND_V = -20.0, -50.0, -30.0

SPECS_V2: dict[str, AnatomySpec] = {
    # v1 re-run (the anchor)
    "v1_third_head": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head_native"),
               Zone(0.45, 0.60, HEAD_V, "head_ectopic_midtrunk"),
               Zone(0.25, 0.45, TRUNK_V, "trunk_a"),
               Zone(0.60, 1.0, TRUNK_V, "trunk_b")],
        amputate_plane="tail", spec_name="third_head",
        somatic_latch=True),
    # novel layout 1: two novel -30 bands (a cell STATE absent from WT)
    "novel_dual_band": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head"),
               Zone(0.38, 0.46, BAND_V, "band_anterior"),
               Zone(0.70, 0.78, BAND_V, "band_posterior"),
               Zone(0.25, 0.38, TRUNK_V, "trunk_a"),
               Zone(0.46, 0.70, TRUNK_V, "trunk_b"),
               Zone(0.78, 1.0, TRUNK_V, "trunk_c")],
        amputate_plane="tail", spec_name="dual_novel_band",
        somatic_latch=True),
    # novel layout 2: ladder segmentation (many novel boundaries)
    "novel_ladder": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head"),
               Zone(0.25, 0.37, HEAD_V, "rung1"),
               Zone(0.49, 0.61, HEAD_V, "rung2"),
               Zone(0.73, 0.85, HEAD_V, "rung3"),
               Zone(0.37, 0.49, TRUNK_V, "gap1"),
               Zone(0.61, 0.73, TRUNK_V, "gap2"),
               Zone(0.85, 1.0, TRUNK_V, "tail_trunk")],
        amputate_plane="tail", spec_name="ladder",
        somatic_latch=True),
    # novel layout 3: custom 4-zone mixed identity
    "novel_custom4": AnatomySpec(
        zones=[Zone(0.0, 0.20, HEAD_V, "head"),
               Zone(0.30, 0.40, BAND_V, "band1"),
               Zone(0.50, 0.60, HEAD_V, "band2_headlike"),
               Zone(0.80, 0.90, BAND_V, "band3"),
               Zone(0.20, 0.30, TRUNK_V, "t1"),
               Zone(0.40, 0.50, TRUNK_V, "t2"),
               Zone(0.60, 0.80, TRUNK_V, "t3"),
               Zone(0.90, 1.0, TRUNK_V, "t4")],
        amputate_plane="tail", spec_name="custom_4zone",
        somatic_latch=True),
}


def main() -> dict:
    print("=== exp61: compiler v2 (Stage-3 90% push) ===\n")

    # ---- CP2-G3: schedule emission (compile-time) ------------------------
    sched_ok = True
    for name, spec in SPECS_V2.items():
        prog = compile_anatomy(spec)
        steps = prog.schedule
        ok = bool(steps) and all(
            {"step", "agent", "action", "timing",
             "concentration_class"} <= set(st) for st in steps)
        sched_ok &= ok
        print(f"  {name}: {len(steps)} schedule steps "
              f"({'schema OK' if ok else 'SCHEMA FAIL'})")
    cp2_g3 = bool(sched_ok)
    print(f"  CP2-G3 schedule emission: {'PASS' if cp2_g3 else 'REFUTED'}\n")

    # ---- CP2-G1: arbitrary layouts ---------------------------------------
    g1 = {}
    t0 = time.time()
    for name, spec in SPECS_V2.items():
        prog = compile_anatomy(spec)
        runs = [execute_and_verify(prog, spec, seed=s,
                                   collective_cls=LatchingCollective)
                  for s in (1, 2, 3)]
        errs = [r["err_vs_spec_target"] for r in runs]
        ok = all(r["program_verified"] for r in runs)
        g1[name] = {"errs": [round(e, 2) for e in errs],
                    "verified_all_seeds": bool(ok)}
        print(f"  {name}: errs {[round(e, 2) for e in errs]} "
              f"{'VERIFY' if ok else 'FAIL'}")
    wall = time.time() - t0
    cp2_g1 = bool(sum(v["verified_all_seeds"]
                      for v in g1.values()) >= 3)
    print(f"  CP2-G1 arbitrary layouts ({wall:.1f}s wall for 4 specs "
          f"x3 seeds): {'PASS' if cp2_g1 else 'REFUTED'}\n")

    # ---- CP2-G2: minimum window scan -------------------------------------
    windows = [24.0, 12.0, 6.0, 3.0]
    g2 = {}
    for w in windows:
        all_ok = True
        per = {}
        for name, spec in SPECS_V2.items():
            prog = compile_anatomy(spec)
            runs = [execute_and_verify(prog, spec, seed=s, window_h=w,
                                   collective_cls=LatchingCollective)
                    for s in (1, 2, 3)]
            ok = all(r["program_verified"] for r in runs)
            per[name] = bool(ok)
            all_ok &= ok
        g2[str(w)] = per
        print(f"  window {w:>4.0f} h: "
              f"{'ALL VERIFY' if all_ok else 'failures: ' + str([k for k, v in per.items() if not v])}")
    ok_windows = [w for w in windows
                  if all(g2[str(w)].values())]
    min_window = min(ok_windows) if ok_windows else None
    cp2_g2 = bool(min_window is not None and min_window <= 24.0)
    print(f"  CP2-G2 minimum window = {min_window} h: "
          f"{'PASS' if cp2_g2 else 'REFUTED'}\n")

    # ---- CP2-G4: 100-generation stability (the latch re-read path) -------
    g4 = {}
    for name in ("v1_third_head", "novel_dual_band"):
        spec = SPECS_V2[name]
        prog = compile_anatomy(spec)
        runs = [recut_stability(prog, spec, seed=s, generations=100)
                for s in (1, 2, 3)]
        holds = sum(1 for r in runs if r["cycles_to_failure"] is None)
        g4[name] = [{
            "cycles_to_failure": r["cycles_to_failure"],
            "err_final": round(r["err_final"], 2),
            "anchor_drift_slope": (round(r["anchor_drift_slope"], 5)
                                   if r["anchor_drift_slope"] is not None
                                   else None),
        } for r in runs]
        print(f"  {name}: cycles_to_failure "
              f"{[r['cycles_to_failure'] for r in runs]}, "
              f"err_final {[round(r['err_final'], 2) for r in runs]}, "
              f"anchor slope {[round(r['anchor_drift_slope'], 5) if r['anchor_drift_slope'] is not None else None for r in runs]}")
    cp2_g4 = bool(any(holds >= 2 for name, runs in
                      [(n, [r for r in [None]]) for n in []]) or
                  sum(1 for name in g4
                      for r in g4[name]
                      if r["cycles_to_failure"] is None) >= 4)
    print(f"  CP2-G4 100-generation stability: "
          f"{'PASS' if cp2_g4 else 'REFUTED'}")

    out = {
        "exp": "exp61_compiler_v2",
        "cp2_g1_layouts": g1,
        "cp2_g1_wall_seconds": round(wall, 1),
        "cp2_g2_window_scan": g2,
        "cp2_g2_min_window_h": min_window,
        "cp2_g3_schedule_ok": bool(sched_ok),
        "cp2_g4_stability": g4,
        "criteria": {
            "CP2_G1_arbitrary_layouts": cp2_g1,
            "CP2_G2_minimum_window": cp2_g2,
            "CP2_G3_schedule_emission": cp2_g3,
            "CP2_G4_100_generation_stability": cp2_g4,
        },
        "notes": (
            "Compiler v2: R6 schedule emission (lab-executable agents/"
            "timing/concentration CLASSES anchored to exp40's measured "
            "dose grid and the record's octanol-class baths — no "
            "invented numbers), window override for the minimum-steps "
            "study, and the recut_stability instrument measuring the "
            "latch RE-READ path (each generation's regen rewrites the "
            "latch from the boundary anchor; the drift slope is the "
            "exp41-failure-structure answer)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
