#!/usr/bin/env python3
"""exp41 — STAGE 3 (GOLDEN CORE): the anatomical compiler, first run.

THE QUESTION (the Golden Core threshold): the model has stopped being a
simulator and become a COMPILER — declarative anatomy in, verified
bioelectric prescription out. Phase A (exp11) searched protocols with
CEM; the adopted Stage-2 mechanisms (M28 phi positional layer + M25
junction-carried readout + M26c two-face regrow) make the inverse map
analytic: cultivation/compiler/anatomy.py compiles an AnatomySpec to an
InterventionProgram with NO search, executes it, and verifies its own
criteria.

PRE-REGISTERED GATES (fixed BEFORE the programs ran):

  CP-G1  RESTORATIVE COMPILE: spec {head@0..0.25, trunk@0.25..1.0} with
         a tail amputation trigger verifies (program_verified == True)
         on all 3 seeds — the compiler restores the WT anatomy from the
         prescribed clamps + spec-reading regrow.
  CP-G2  TWO-HEAD COMPILE (the Levin anchor, reached by compilation not
         search): spec {head@0..0.25, head@0.75..1.0} with a tail
         amputation trigger verifies on all 3 seeds — depolarized zones
         at BOTH ends hold within 6.0 mV and the regen reads the spec.
  CP-G3  NOVEL-ANATOMY COMPILE: spec with an ECTOPIC head zone at
         mid-trunk {head@0.45..0.60, trunk elsewhere} verifies — a body
         plan that does not exist in nature, prescribed and reached.
  CP-G4  SAFETY REFUSAL: a spec with identity voltage outside the fate
         repertoire (e.g., +10 mV) is REJECTED at compile time (no
         program emitted) — the compiler refuses what the substrate
         cannot express.
  CP-G5  COUPLING NECESSITY: CP-G1's program, executed with
         gap_scale=0.05 during regen, FAILS its verification — the
         compiler's coupling precondition (R3) is load-bearing, not
         decorative (M25/M28 consistency at the compiled level).

PROCESS NOTE (verifier bug, caught in the first run): the first
execution's verifier matched the pattern-error criterion by the
substring "pattern error" while the criterion string reads
"wt_pattern_error" — the whole-spec error gate was silently skipped
and every program's verification rested on zone checks alone (blocked
runs therefore showed spurious verified=True at err 6.83/6.72/10.21).
Fixed to "pattern_error"; every verdict below comes from the FIXED
verifier. Same species as exp36's float-literal gate bug: verification
criteria must be executed, not parsed by substring.

REGISTERED AMENDMENT (exploratory, exp36 precedent): CP-G3' — the
ectopic mid-trunk zone is surrounded by trunk tissue on BOTH sides, so
after clamp release the boundary Laplacian erodes it ~4-6 mV toward
trunk (first run: -26.2 vs the -26.0 bar — a 0.22 mV miss). The
morpho_engineering latch (exp11) pins theta against exactly this
erosion; the amendment compiles the same spec with the latching
substrate (compiler rule R1': zones without anatomical support require
the somatic latch — a NEW emitted precondition), executed unchanged.
If it verifies, R1' is the compiler's first learned rule and the
ectopic-anatomy gate flips.

RUN PROTOCOL: seeds (1,2,3); window 24h; thresholds 6.0 mV; programs
executed via execute_and_verify (clamps -> window -> release -> amputate
-> spec-reading regrow -> settle). Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
OPENBLAS_NUM_THREADS = os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
MKL_NUM_THREADS = os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.compiler.anatomy import (  # noqa: E402
    AnatomySpec, Zone, compile_anatomy, execute_and_verify,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp41_anatomical_compiler.json")
SEEDS = (1, 2, 3)

HEAD_V, TRUNK_V = -20.0, -50.0

SPECS: dict[str, AnatomySpec] = {
    "CP-G1_restore": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head"),
               Zone(0.25, 1.0, TRUNK_V, "trunk")],
        amputate_plane="tail", spec_name="restore_wt"),
    "CP-G2_twohead": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head_anterior"),
               Zone(0.75, 1.0, HEAD_V, "head_posterior"),
               Zone(0.25, 0.75, TRUNK_V, "trunk")],
        amputate_plane="tail", spec_name="two_headed"),
    "CP-G3_ectopic": AnatomySpec(
        zones=[Zone(0.0, 0.25, HEAD_V, "head_native"),
               Zone(0.45, 0.60, HEAD_V, "head_ectopic_midtrunk"),
               Zone(0.25, 0.45, TRUNK_V, "trunk_a"),
               Zone(0.60, 1.0, TRUNK_V, "trunk_b")],
        amputate_plane="tail", spec_name="third_head"),
    "CP-G4_refusal": AnatomySpec(
        zones=[Zone(0.0, 0.25, +10.0, "impossible_identity")],
        amputate_plane="tail", spec_name="out_of_repertoire"),
}


def main() -> dict:
    print("=== exp41: Stage 3 — the anatomical compiler ===\n")

    programs: dict[str, dict] = {}
    runs: dict[str, list[dict]] = {}

    for name, spec in SPECS.items():
        prog = compile_anatomy(spec)
        programs[name] = json.loads(json.dumps({
            "rejected": prog.rejected,
            "clamps": prog.clamps,
            "regen": prog.regen,
            "preconditions": prog.preconditions,
            "description": prog.describe(),
        }))
        if prog.rejected:
            print(f"  {name}: REJECTED at compile time "
                  f"({len(prog.rejected)} reason(s))")
            continue
        runs[name] = [execute_and_verify(prog, spec, seed=s)
                      for s in SEEDS]
        ok = all(r["program_verified"] for r in runs[name])
        errs = [round(r["err_vs_spec_target"], 2) for r in runs[name]]
        print(f"  {name}: verified {'3/3' if ok else 'FAIL'} "
              f"(spec-err per seed {errs})")
        for k, v in runs[name][0].items():
            if isinstance(v, dict) and "ok" in v:
                print(f"      {k}: {v}")

    # CP-G5: coupling necessity — CP-G1's program with blocked junctions
    spec = SPECS["CP-G1_restore"]
    prog = compile_anatomy(spec)
    blocked = [execute_and_verify(prog, spec, seed=s, gap_scale=0.05)
               for s in SEEDS]
    blocked_ok = [r["program_verified"] for r in blocked]
    cp_g5 = not all(blocked_ok)
    print(f"  CP-G5 (coupling necessity, gap_scale=0.05): verified "
          f"{sum(blocked_ok)}/3 -> precondition is "
          f"{'LOAD-BEARING (PASS)' if cp_g5 else 'DECORATIVE (REFUTED)'}")

    # CP-G3' amendment (exploratory): latching substrate for the
    # unsupported ectopic zone (compiler rule R1' — latch emission)
    from cultivation.bioelectric.morpho_engineering import (
        LatchingCollective,
    )
    spec3 = SPECS["CP-G3_ectopic"]
    prog3 = compile_anatomy(spec3)
    prog3.preconditions["somatic_latch"] = True
    prog3.preconditions["latch_rationale"] = (
        "R1': ectopic zone lacks anatomical support; the somatic latch "
        "pins theta against boundary erosion (exp11)")
    amend3 = [execute_and_verify(prog3, spec3, seed=s,
                                 collective_cls=LatchingCollective)
              for s in SEEDS]
    amend_ok = all(r["program_verified"] for r in amend3)
    print(f"  CP-G3' (latch amendment, exploratory): verified "
          f"{'3/3' if amend_ok else 'FAIL'} "
          f"(errs {[round(r['err_vs_spec_target'], 2) for r in amend3]})")

    cp_g1 = all(r["program_verified"] for r in runs["CP-G1_restore"])
    cp_g2 = all(r["program_verified"] for r in runs["CP-G2_twohead"])
    cp_g3 = all(r["program_verified"] for r in runs["CP-G3_ectopic"])
    cp_g4 = bool(programs["CP-G4_refusal"]["rejected"])

    print(f"\n  CP-G1 restorative compile:            "
          f"{'PASS' if cp_g1 else 'REFUTED'}")
    print(f"  CP-G2 two-head compile (Levin anchor):"
          f" {'PASS' if cp_g2 else 'REFUTED'}")
    print(f"  CP-G3 novel-anatomy compile:          "
          f"{'PASS' if cp_g3 else 'REFUTED'}")
    print(f"  CP-G3' latch amendment (exploratory): "
          f"{'PASS' if amend_ok else 'REFUTED'}")
    print(f"  CP-G4 safety refusal:                 "
          f"{'PASS' if cp_g4 else 'REFUTED'}")
    print(f"  CP-G5 coupling necessity:             "
          f"{'PASS' if cp_g5 else 'REFUTED'}")

    out = {
        "exp": "exp41_anatomical_compiler",
        "stage": "3 — Golden Core (anatomical compiler v0)",
        "compiler": "cultivation/compiler/anatomy.py",
        "rules": {
            "R1": "identity zones -> sustained clamps over the 24h window",
            "R2": "trigger plane -> amputate + phi_readout=0.75 spec read",
            "R3": "junction-health precondition (gap_scale >= 1.0)",
            "R4": "repertoire check at compile time (safety refusal)",
        },
        "programs": programs,
        "runs": runs,
        "cp_g3_amendment": {
            "status": "exploratory (exp36 precedent)",
            "rule": "R1': zones without anatomical support require the "
                    "somatic latch",
            "runs": amend3,
            "verified": amend_ok,
        },
        "cp_g5_blocked_runs": blocked,
        "verifier_bug_note": (
            "first run's verifier skipped the whole-spec pattern-error "
            "gate (substring 'pattern error' vs 'wt_pattern_error'); "
            "all verdicts here come from the fixed verifier"),
        "criteria": {
            "CP_G1_restorative": cp_g1,
            "CP_G2_two_head": cp_g2,
            "CP_G3_novel_anatomy": cp_g3,
            "CP_G4_safety_refusal": cp_g4,
            "CP_G5_coupling_necessity": cp_g5,
        },
        "notes": (
            "Compilation, not search: zero CEM iterations. The M28 phi "
            "layer is the target representation — write the spec, "
            "trigger a regen that reads it. The prescription is the "
            "lab-executable deliverable: regions, voltages, durations, "
            "coupling preconditions, verification criteria."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
