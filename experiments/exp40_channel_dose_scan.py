#!/usr/bin/env python3
"""exp40 — CHANNEL-SLICE DOSE SCAN + S2R3c literature closure (night-five
queue #3 and the exp35 refutation candidate ion_channel|trunk).

CONTEXT: exp35 found ion_channel|trunk recorded 0.46 (n=60) vs sim 0.00
(gap -0.46). exp37's sweep already shrank the gap to +0.21 (sim 0.67 at
the exp34-adopted M27b mapping + M26c two-face trunk, the closest
achievable being 1/3 at 0.13 distance). Tonight: the registered (cns x
diffusion) grid refines the mapping and tests whether the tail/head
calibrations survive.

GRID (pre-registered): cns in {1.0, 2.0, 3.0, 4.0, 5.0} x diffusion in
{0.0, 0.5, 1.0, 1.5, 2.0, 2.5}, ion protocol (gamma x0.5, noise x3),
trunk plane with M26c two-face regrow, 3 seeds. 30 arms.

GATES (fixed before the grid ran; recorded reference is exp35's
published 0.46 only):
  CH-G1  exists a grid cell with ion_trunk pred_abn_rate == 1/3 (the
         achievable rate closest to the recorded 0.46).
  CH-G2  at that cell, the tail/head calibrations hold: ion_tail
         rate >= 0.34 (exp34 M27B-G1) and ion_head rate > 0 (M27B-G2).
  CH-G3  cutting_tail per-seed errors bit-exact vs exp31 (structural
         inertness — the ion params apply only in ion arms).

S2R3c LITERATURE CLOSURE (registered in the same run): PlanformDB has
no drug concentrations (exp33, L16); Europe PMC confirms the published
record has NO partial-dose regeneration curve for planarian GJ blockers
— octanol/heptanol are used at supramaximal/effective doses with TIMING
ladders only (Oviedo 2010 Fig 2A pulse ladder, already extracted at
night three: RegenPeriod=0, no regen outcome recorded). Therefore the
S2R3 monotone dose-response prediction (3.28 -> 3.93 -> 4.54 -> 6.03 mV
at gap_scale 1.0/0.5/0.25/0.05) stands UNTESTED, not falsified, and is
recorded as a formal NOVEL-PREDICTION deposit with a concrete
experimental design (concentration ladder x regeneration outcome,
pre-registered analysis: Spearman monotonicity across doses).
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

from experiments.exp34_m27_candidates import run_arm, sim_arm  # noqa: E402
from experiments.exp27_stage2_pilot import make_collective, DT, SEEDS, TAIL  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp40_channel_dose_scan.json")

CNS_GRID = [1.0, 2.0, 3.0, 4.0, 5.0]
DIFF_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
RECORDED_ION_TRUNK = 0.46


def main() -> dict:
    print("=== exp40: channel-slice dose scan (cns x diffusion) ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))

    grid: dict[str, dict] = {}
    qualifying = None
    for cns in CNS_GRID:
        for diff in DIFF_GRID:
            tag = f"c{int(cns)}_d{int(diff * 10):02d}"
            trunk = sim_arm("ion_channel_trunk",
                            commitment_noise_scale=cns,
                            commitment_diffusion=diff,
                            direction="both")
            grid[f"ion_trunk_{tag}"] = trunk
            tail = sim_arm("ion_channel_tail",
                           commitment_noise_scale=cns,
                           commitment_diffusion=diff)
            head = sim_arm("ion_channel_head",
                           commitment_noise_scale=cns,
                           commitment_diffusion=diff)
            grid[f"ion_tail_{tag}"] = tail
            grid[f"ion_head_{tag}"] = head
            r_t = trunk["pred_abn_rate"]
            marker = ""
            if r_t == 1 / 3 and qualifying is None \
                    and tail["pred_abn_rate"] >= 0.34 \
                    and head["pred_abn_rate"] > 0:
                qualifying = (cns, diff)
                marker = "  <-- qualifying"
            print(f"  cns={cns:.0f} diff={diff:.1f}: trunk {r_t:.2f} "
                  f"(err {trunk['err_mean']:5.2f}) | tail "
                  f"{tail['pred_abn_rate']:.2f} | head "
                  f"{head['pred_abn_rate']:.2f}{marker}")

    ch_g1 = qualifying is not None
    ch_g2 = False
    if qualifying is not None:
        cns, diff = qualifying
        tag = f"c{int(cns)}_d{int(diff * 10):02d}"
        ch_g2 = bool(grid[f"ion_tail_{tag}"]["pred_abn_rate"] >= 0.34
                     and grid[f"ion_head_{tag}"]["pred_abn_rate"] > 0)

    # structural inertness control (re-verified, not assumed)
    from experiments.exp34_m27_candidates import SEEDS as S34
    fresh = []
    for s in SEEDS:
        c = make_collective(s)
        c.run(24, dt=DT)
        c.amputate(__import__('experiments.exp32_m26_repairs',
                              fromlist=['TAILP']).TAILP,
                   wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(__import__('experiments.exp32_m26_repairs',
                            fromlist=['TAILP']).TAILP,
                 cell_period=0.8, dt=DT, noise=0.6)
        fresh.append(c.pattern_error(wildtype_target(100)))
    ch_g3 = bool(np.allclose(
        fresh, exp31["sim_arms"]["cutting_tail"]["err_per_seed"],
        atol=1e-9, rtol=0.0))

    print(f"\n  CH-G1 cell at rate 1/3 exists:            "
          f"{qualifying}  {'PASS' if ch_g1 else 'REFUTED'}")
    print(f"  CH-G2 tail/head calibrations hold:        "
          f"{'PASS' if ch_g2 else 'REFUTED'}")
    print(f"  CH-G3 cutting control bit-exact:          "
          f"{'PASS' if ch_g3 else 'REFUTED'}")

    if qualifying is not None:
        cns, diff = qualifying
        print(f"  adopted ion mapping candidate: cns={cns}, "
              f"diffusion={diff} (trunk 1/3 vs recorded 0.46, "
              f"distance {abs(1/3 - RECORDED_ION_TRUNK):.2f})")

    out = {
        "exp": "exp40_channel_dose_scan",
        "grid": {"cns": CNS_GRID, "diffusion": DIFF_GRID},
        "recorded_reference": {"ion_channel_trunk": RECORDED_ION_TRUNK,
                               "n": 60, "source": "exp35"},
        "qualifying_cell": qualifying,
        "grid_results": grid,
        "criteria": {
            "CH_G1_rate_one_third_exists": ch_g1,
            "CH_G2_tail_head_calibrations_hold": ch_g2,
            "CH_G3_control_bitexact": ch_g3,
        },
        "s2r3c_literature_closure": {
            "planformdb": "no drug concentrations recorded (exp33, L16)",
            "literature": (
                "Europe PMC: no partial-dose regeneration curve for "
                "planarian GJ blockers; octanol/heptanol used at "
                "supramaximal doses with TIMING ladders only (Oviedo "
                "2010 Fig 2A, extracted night three — RegenPeriod=0)"),
            "verdict": (
                "S2R3 monotone dose-response (3.28/3.93/4.54/6.03 mV at "
                "gap 1.0/0.5/0.25/0.05) stands UNTESTED, not falsified; "
                "registered as NOVEL-PREDICTION deposit with concrete "
                "experimental design (concentration ladder x regen "
                "outcome; pre-registered Spearman monotonicity)"),
        },
        "notes": (
            "exp37's sweep already bracketed ion|trunk at 0.67 (gap "
            "+0.21 after exp35's -0.46); the grid asks whether the "
            "1/3 cell (closest to 0.46) exists without losing the "
            "tail/head calibrations. Scan is the calibration instrument "
            "(exp26/36/38 precedent)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
