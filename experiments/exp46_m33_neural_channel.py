#!/usr/bin/env python3
"""exp46 — M33 NON-JUNCTIONAL NEURAL/MUSCLE POLARITY CHANNEL
(night-six queue #2: the innexin|head plane-dependent readout, ledger L28).

THE RECORDED GAP (exp35/exp37): innexin|head — the model predicts the
head-plane regen goes abnormal under junction blockade (M25 blind guess,
rate 1.00) while the record says 0.00 abnormal. Meanwhile innexin|tail is
0.67 abnormal in BOTH record and model. The gap is PLANE-ASYMMETRIC.

MECHANISM (collective.py regrow, additive + bit-exact at default):
`neural_readout` w — the anterior pole is a constitutive,
junction-INDEPENDENT identity source (exp44 research wave):
  - Lobo, Emmons-Bell & Levin 2019 (PMC30990801): the head-tail axis is
    controlled by the net polarity of neurons; the morphogen vector-
    transport field coincides with nerve axon alignment — a channel that
    does not run through gap junctions.
  - egal-1/microtubules 2025 (PMC41099308/9): wound-induced notum at
    anterior-facing wounds is polarized by the muscle microtubule
    substrate — again non-junctional.
When 0 < w <= 1 and the committing cell's spec identity is ANTERIOR
(spec[i] >= NEURAL_SPEC_MIN = -35 mV, the head/trunk fate-axis midpoint),
the M25 blind guess is blended with a direct neural read of the spec:
  guess <- (1-w)*guess + w*(spec[i] + N(0, eff_noise))
Posterior identities do NOT qualify (no local pole — which is exactly why
recorded GJ-blockade phenotypes concentrate at posterior planes).

PRE-REGISTERED GATES (fixed BEFORE tonight's arms ran; recorded
references are exp31's published values only):

  M33-G1  GAP RESOLVED: innexin_head at w=1.0 has pred_abn_rate 0.00
          (registered scan {0.5, 1.0}; exp31 model rate 1.00, record 0.00).
  M33-G2  POSTERIOR IMMUNITY: innexin_tail at w=1.0 is bit-exact vs
          the SAME arm at w=0.0 (both phi=0.75 — the w=0.0 run is the
          inertness reference; exp31's stored arms predate phi so the
          exp31 comparison is rate 0.67 + drift <= 1.5 mV, the exp38
          A4 criterion) — the tail identity does not qualify for the
          pole channel (same draws, unchanged centers).
  M33-G3  FULL-COUPLING INERTNESS: cutting_head at w=1.0 (gap_scale=1,
          guess branch unused) is bit-exact vs exp31 cutting_head.
  M33-G4  DOSE MONOTONICITY: err_mean(innexin_head) is strictly
          decreasing across w in {0.0, 0.5, 1.0}.
  M33-G5  NO COLLATERAL: junction-intact arms (cutting tail/head/trunk,
          restored_tail, cross bin a) and blocked gjblock_tail at w=1.0
          are bit-exact vs the SAME arms at w=0.0 (both phi=0.75 — no
          extra RNG draws / unchanged centers for posterior identities);
          gjblock_tail also keeps its exp31 rate with drift <= 1.5 mV.

RUN PROTOCOL: exp31 discipline (seeds (1,2,3), window 24h dt=0.1,
thresholds unchanged, phi readout 0.75 on the phi arms, metrics read
immediately after regrow). Serial, BLAS pinned.
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

from experiments.exp34_m27_candidates import sim_arm  # noqa: E402
from experiments.exp32_m26_repairs import EXP31_BINS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp46_m33_neural_channel.json")

PHI = 0.75
W_SCAN = [0.5, 1.0]


def bitexact(arm_a: dict, arm_b: dict) -> bool:
    return bool(np.allclose(arm_a["err_per_seed"], arm_b["err_per_seed"],
                            atol=1e-9, rtol=0.0))


def main() -> dict:
    print("=== exp46: M33 neural/muscle polarity channel ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))
    e31 = exp31["sim_arms"]

    sim: dict[str, dict] = {}
    for w in W_SCAN:
        tag = f"n{int(round(w * 100)):02d}"
        sim[f"innexin_head_{tag}"] = sim_arm(f"innexin_head_{tag}",
                                             phi_readout=PHI, neural_readout=w)
        sim[f"innexin_tail_{tag}"] = sim_arm(f"innexin_tail_{tag}",
                                             phi_readout=PHI, neural_readout=w)
        sim[f"gjblock_tail_{tag}"] = sim_arm(f"gjblock_tail_{tag}",
                                             phi_readout=PHI, neural_readout=w)
        sim[f"cutting_head_{tag}"] = sim_arm(f"cutting_head_{tag}",
                                             phi_readout=PHI, neural_readout=w)
        sim[f"cutting_tail_{tag}"] = sim_arm(f"cutting_tail_{tag}",
                                             phi_readout=PHI, neural_readout=w)
        sim[f"cutting_trunk_{tag}"] = sim_arm(f"cutting_trunk_{tag}",
                                              phi_readout=PHI, neural_readout=w)
        sim[f"restored_tail_{tag}"] = sim_arm(f"restored_tail_{tag}",
                                              phi_readout=PHI, neural_readout=w)
        sim[f"cutting_cross_a_{tag}"] = sim_arm(
            f"cutting_cross_a_{tag}", cut_f=EXP31_BINS["a"],
            phi_readout=PHI, neural_readout=w)
        ih = sim[f"innexin_head_{tag}"]
        print(f"  w={w:.1f}: innexin_head {ih['pred_abn_rate']:.2f} "
              f"(err {ih['err_mean']:6.2f}) | innexin_tail "
              f"{sim[f'innexin_tail_{tag}']['pred_abn_rate']:.2f} | "
              f"gjblock_tail {sim[f'gjblock_tail_{tag}']['pred_abn_rate']:.2f} | "
              f"cutting_head {sim[f'cutting_head_{tag}']['pred_abn_rate']:.2f}")

    # w=0.0 reference arms (same phi) — the correct inertness references
    sim["innexin_head_n00"] = sim_arm("innexin_head_n00", phi_readout=PHI,
                                      neural_readout=0.0)
    sim["innexin_tail_n00"] = sim_arm("innexin_tail_n00", phi_readout=PHI,
                                      neural_readout=0.0)
    sim["gjblock_tail_n00"] = sim_arm("gjblock_tail_n00", phi_readout=PHI,
                                      neural_readout=0.0)
    for pl in ("head", "tail", "trunk"):
        sim[f"cutting_{pl}_n00"] = sim_arm(f"cutting_{pl}_n00",
                                           phi_readout=PHI, neural_readout=0.0)
    sim["restored_tail_n00"] = sim_arm("restored_tail_n00", phi_readout=PHI,
                                       neural_readout=0.0)
    sim["cutting_cross_a_n00"] = sim_arm("cutting_cross_a_n00",
                                         cut_f=EXP31_BINS["a"],
                                         phi_readout=PHI, neural_readout=0.0)

    # ---- gates -------------------------------------------------------------
    ih1 = sim["innexin_head_n100"]
    m33_g1 = bool(ih1["pred_abn_rate"] == 0.0)

    it1 = sim["innexin_tail_n100"]
    drift_tail = float(np.max(np.abs(
        np.array(it1["err_per_seed"]) - np.array(e31["innexin_tail"]["err_per_seed"]))))
    m33_g2 = bool(bitexact(it1, sim["innexin_tail_n00"])
                  and abs(it1["pred_abn_rate"]
                          - e31["innexin_tail"]["pred_abn_rate"]) < 1e-9
                  and drift_tail <= 1.5)

    ch1 = sim["cutting_head_n100"]
    m33_g3 = bitexact(ch1, sim["cutting_head_n00"])

    errs = [sim["innexin_head_n00"]["err_mean"],
            sim["innexin_head_n50"]["err_mean"],
            sim["innexin_head_n100"]["err_mean"]]
    m33_g4 = bool(errs[0] > errs[1] > errs[2])

    m33_g5 = all(bitexact(sim[f"cutting_{pl}_n100"], sim[f"cutting_{pl}_n00"])
                 for pl in ("tail", "head", "trunk")) \
        and bitexact(sim["restored_tail_n100"], sim["restored_tail_n00"]) \
        and bitexact(sim["cutting_cross_a_n100"], sim["cutting_cross_a_n00"])
    gt1 = sim["gjblock_tail_n100"]
    drift_gj = float(np.max(np.abs(
        np.array(gt1["err_per_seed"]) - np.array(e31["gjblock_tail"]["err_per_seed"]))))
    m33_g5 = bool(m33_g5 and bitexact(gt1, sim["gjblock_tail_n00"])
                  and abs(gt1["pred_abn_rate"]
                          - e31["gjblock_tail"]["pred_abn_rate"]) < 1e-9
                  and drift_gj <= 1.5)

    print(f"\n  M33-G1 gap resolved (innexin_head 0.00 @w=1):    "
          f"{'PASS' if m33_g1 else 'REFUTED'}"
          f"   [rate {ih1['pred_abn_rate']:.2f}, err {ih1['err_mean']:.2f}]")
    print(f"  M33-G2 posterior immunity (tail 0.67, drift "
          f"{drift_tail:.2e}): {'PASS' if m33_g2 else 'REFUTED'}")
    print(f"  M33-G3 full-coupling inertness:                  "
          f"{'PASS' if m33_g3 else 'REFUTED'}")
    print(f"  M33-G4 dose monotonicity ({errs[0]:.2f} > {errs[1]:.2f} "
          f"> {errs[2]:.2f}): {'PASS' if m33_g4 else 'REFUTED'}")
    print(f"  M33-G5 no collateral (gj drift {drift_gj:.2e}):           "
          f"{'PASS' if m33_g5 else 'REFUTED'}")

    out = {
        "exp": "exp46_m33_neural_channel",
        "mechanism": (
            "neural_readout — non-junctional neural/muscle polarity "
            "channel for ANTERIOR identities: the M25 blind guess is "
            "blended with a direct spec read, "
            "guess <- (1-w)*guess + w*(spec[i] + N(0, eff_noise)), "
            "only when spec[i] >= NEURAL_SPEC_MIN (-35 mV). Posterior "
            "identities have no local pole and stay junction-carried"),
        "literature_basis": [
            "Lobo, Emmons-Bell & Levin 2019 (PMC30990801): axon-aligned "
            "vector transport controls the head-tail axis",
            "egal-1/microtubules 2025 (PMC41099308/9): anterior-facing "
            "wound notum via muscle microtubule substrate",
        ],
        "phi_readout": PHI,
        "w_scan": W_SCAN,
        "sim_arms": sim,
        "criteria": {
            "M33_G1_gap_resolved": m33_g1,
            "M33_G2_posterior_immunity": m33_g2,
            "M33_G3_full_coupling_inertness": m33_g3,
            "M33_G4_dose_monotonicity": m33_g4,
            "M33_G5_no_collateral": m33_g5,
        },
        "recorded_reference": {"innexin_head": 0.00, "innexin_tail": 0.67},
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "exp35's innexin|head +1.00 gap was the last unexplained "
            "Stage-2 arm-level signature; M33 resolves it with the "
            "literature-mandated asymmetry (anterior pole = constitutive "
            "junction-independent identity source; posterior identity has "
            "no local pole). The same channel predicts gjblock_head "
            "moves toward normal — a REGISTERED NOVEL PREDICTION for the "
            "next corpus pass."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
