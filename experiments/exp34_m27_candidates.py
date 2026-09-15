#!/usr/bin/env python3
"""exp34 — M27 candidates: whole-fragment positional fit + repertoire clip
(M27a) and chain-accumulating commitment diffusion (M27b).

Model state (collective.py regrow, additive + bit-exact at defaults,
verify_m26_bitexact.py green to 1e-9, full suite green BEFORE this run):

  M27a: `gradient_window=0` measures the positional trend as a
        WHOLE-FRAGMENT secant (theta[far end] vs theta[face]) instead of
        M26a's 5-cell face window — exp32's diagnosis was that the
        head-only fragment's face window sits on the plateau (slope ~0),
        making the extrapolation a no-op exactly where the refutation
        lives. `gradient_clip=True` saturates the extrapolated identity
        to the intact side's OWN identity repertoire [min, max] of theta
        (intrinsic fate-axis bounds, no external target knowledge).
  M27b: `commitment_diffusion` — identity noise that random-walks ALONG
        the chain (wander += N(0, diffusion) per committed cell, sd ~
        diffusion * sqrt(d)) so commitment error COMPOUNDS — exp32's
        diagnosis of why M26b's i.i.d. noise averaged out (0.00 rate vs
        recorded 0.45).

PRE-REGISTERED GATES (fixed BEFORE tonight's arms ran; recorded
references are exp31/exp32's published values only):

  M27A-G1  cross_a @(g=1, wfit, clip) pred_abn_rate <= 0.67 — at least
           one seed regenerates normally where M26a left all three
           abnormal (exp31/exp32: 1.00; recorded bin a 0.52)
  M27A-G2  no overshoot introduction: bins b/c/d each <= 0.34
  M27A-G3  plane collaterals: cutting_{tail,head,trunk} @(g=1, wfit,
           clip) all pred_abn_rate == 0.00 (they were 0.00 in exp32)
  M27B-G1  ion_channel_tail @(cns=3, diff=1.5) pred_abn_rate >= 0.34
           (exp32 @cns only: 0.00; recorded ion mean 0.45)
  M27B-G2  ion_channel_head @(cns=3, diff=1.5) pred_abn_rate > 0
  M27B-G3  default inertness: cutting_tail (all defaults) AND
           innexin_tail per-seed errors bit-exact vs exp31

RUN PROTOCOL: identical to exp31/exp32 (seeds (1,2,3); window 24h dt=0.1;
thresholds unchanged; bin cut positions = exp31's recorded medians;
metrics read IMMEDIATELY after regrow). Serial, BLAS threads pinned.
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

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    EXP31_BINS, HEAD, TAILP, TRUNK, POST_Q, ANT_Q, WT_HEAD_V, WT_TAIL_V,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp34_m27_candidates.json")


def run_arm(arm: str, seed: int, cut_f: float = 0.5,
            length_gradient: float = 0.0,
            commitment_noise_scale: float = 1.0,
            direction: str = "forward",
            gradient_window: int = 5,
            gradient_clip: bool = False,
            commitment_diffusion: float = 0.0,
            phi_readout: float = 0.0,
            spec_expression_p: float = 1.0,
            spec_reanchor_p: float = 1.0,
            anchor_from_history: float | None = None,
            spec_reanchor_isolated: float = 1.0,
            neural_readout: float = 0.0) -> dict:
    c = make_collective(seed)
    rg = dict(length_gradient=length_gradient,
              commitment_noise_scale=commitment_noise_scale,
              direction=direction,
              gradient_window=gradient_window,
              gradient_clip=gradient_clip,
              commitment_diffusion=commitment_diffusion,
              phi_readout=phi_readout,
              spec_expression_p=spec_expression_p,
              spec_reanchor_p=spec_reanchor_p,
              anchor_from_history=anchor_from_history,
              spec_reanchor_isolated=spec_reanchor_isolated,
              neural_readout=neural_readout)

    def plane_protocol(plane: str) -> None:
        if plane == "head":
            c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(HEAD, cell_period=0.8, dt=DT, noise=0.6,
                     direction="backward" if direction == "forward" else direction,
                     **{k: v for k, v in rg.items() if k != "direction"})
        elif plane == "tail":
            c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, **rg)
        elif plane == "trunk":
            c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(TRUNK, cell_period=0.8, dt=DT, noise=0.6, **rg)
        elif plane == "head_tail":
            c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
            c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6,
                     **{k: v for k, v in rg.items() if k != "direction"})
            c.regrow(HEAD, cell_period=0.8, dt=DT, noise=0.6,
                     direction="backward" if direction == "forward" else direction,
                     **{k: v for k, v in rg.items() if k != "direction"})
        elif plane == "crosspiece":
            ci = int(round(cut_f * N))
            ci = min(max(ci, 5), N - 1)
            c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(slice(ci, N), cell_period=0.8, dt=DT, noise=0.6, **rg)
        else:
            raise ValueError(plane)

    def strip(plane: str, *suffixes: str) -> str:
        for s in suffixes:
            if plane.endswith(s):
                return plane[: -len(s)]
        return plane

    SUF = ("_m27", "_g1", "_inert", "_m28", "_recheck", "_m30",
           "_p70", "_p75", "_p80", "_p85", "_p90",
           "_q55", "_q65", "_q72", "_q80", "_q90",
           "_r40", "_r45", "_r50", "_r55", "_r60",
           "_t10", "_t15", "_t20", "_t25", "_t30", "_t40", "_m31",
           "_m31a", "_i40", "_i45", "_i50", "_i55", "_i60",
           "_inerti", "_plain", "_armed",
           "_n00", "_n50", "_n100", "_m33")

    if arm.startswith("cutting_"):
        plane = strip(arm[len("cutting_"):], *SUF)
        if plane.startswith("cross_"):
            plane = "crosspiece"
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("innexin_") or arm.startswith("gjblock_"):
        plane = strip(arm.split("_", 1)[1], *SUF)
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("restored_tail"):
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        c.restore_gap_junctions(1.0)
        c.run(20, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, **rg)
        c.run(15, dt=DT)
    elif arm.startswith("ion_channel_"):
        plane = strip(arm[len("ion_channel_"):], *SUF)
        c.gamma *= 0.5
        c.noise_std *= 3.0
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("wnt_"):
        plane = strip(arm[len("wnt_"):], "_m27")
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("apc_"):
        plane = strip(arm[len("apc_"):], "_m27")
        c.corrupt_region(ANT_Q, theta_value=WT_TAIL_V)
        c.run(24, dt=DT)
        plane_protocol(plane)
    else:
        raise ValueError(arm)
    m = {
        "wt_pattern_error": c.pattern_error(wildtype_target(N)),
        "head_likeness_tail": head_likeness(c.V, TAIL),
        "head_likeness_head": head_likeness(c.V, slice(0, N // 4)),
        "seed": seed,
    }
    m["predicted_abnormal"] = bool(
        m["wt_pattern_error"] >= ABN_ERR_MV
        or m["head_likeness_tail"] >= ABN_HL)
    return m


def sim_arm(arm: str, cut_f: float = 0.5, **kw) -> dict:
    runs = [run_arm(arm, s, cut_f, **kw) for s in SEEDS]
    errs = [r["wt_pattern_error"] for r in runs]
    return {
        "err_mean": float(np.mean(errs)),
        "err_se": float(np.std(errs, ddof=1) / np.sqrt(len(errs))) if len(errs) > 1 else 0.0,
        "err_per_seed": errs,
        "pred_abn_rate": float(np.mean([r["predicted_abnormal"] for r in runs])),
    }


def main() -> dict:
    print("=== exp34: M27 candidates — whole-fragment fit + clip, "
          "chain commitment diffusion ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))
    exp32 = json.load(open(os.path.join(ROOT, "results",
                                        "exp32_m26_repairs.json")))

    m27a = dict(length_gradient=1.0, gradient_window=0, gradient_clip=True)
    m27b = dict(commitment_noise_scale=3.0, commitment_diffusion=1.5)

    arm_defs = [
        # M27a: saturated whole-fragment gradient on the crosspiece bins
        ("cutting_cross_a_m27", dict(cut_f=EXP31_BINS["a"], **m27a)),
        ("cutting_cross_b_m27", dict(cut_f=EXP31_BINS["b"], **m27a)),
        ("cutting_cross_c_m27", dict(cut_f=EXP31_BINS["c"], **m27a)),
        ("cutting_cross_d_m27", dict(cut_f=EXP31_BINS["d"], **m27a)),
        ("cutting_tail_m27", dict(**m27a)),
        ("cutting_head_m27", dict(**m27a)),
        ("cutting_trunk_m27", dict(**m27a)),
        # M27b: chain-accumulating commitment diffusion on ion arms
        ("ion_channel_tail_m27", dict(**m27b)),
        ("ion_channel_head_m27", dict(**m27b)),
        # M27b-G3 inertness references
        ("cutting_tail_inert", {}),
        ("innexin_tail_m27", {}),
    ]
    sim: dict[str, dict] = {}
    for arm, kw in arm_defs:
        sim[arm] = sim_arm(arm, **kw)
        s = sim[arm]
        print(f"  {arm:24s} err {s['err_mean']:5.2f} ± {s['err_se']:4.2f} mV"
              f"   pred-abn {s['pred_abn_rate']:.2f}")

    def rate(a: str) -> float:
        return sim[a]["pred_abn_rate"]

    m27a_g1 = bool(rate("cutting_cross_a_m27") <= 0.67)
    m27a_g2 = bool(all(rate(f"cutting_cross_{b}_m27") <= 0.34
                       for b in ("b", "c", "d")))
    m27a_g3 = bool(all(rate(a) == 0.0 for a in
                       ("cutting_tail_m27", "cutting_head_m27",
                        "cutting_trunk_m27")))
    m27b_g1 = bool(rate("ion_channel_tail_m27") >= 0.34)
    m27b_g2 = bool(rate("ion_channel_head_m27") > 0.0)
    strict = sim["cutting_tail_inert"]
    inx = sim["innexin_tail_m27"]
    m27b_g3 = bool(
        np.allclose(strict["err_per_seed"],
                    exp31["sim_arms"]["cutting_tail"]["err_per_seed"],
                    atol=1e-9, rtol=0.0)
        and np.allclose(inx["err_per_seed"],
                        exp31["sim_arms"]["innexin_tail"]["err_per_seed"],
                        atol=1e-9, rtol=0.0))

    print(f"\n  M27A-G1 cross_a @(wfit,clip) <= 0.67:    "
          f"{rate('cutting_cross_a_m27'):.2f}  {'PASS' if m27a_g1 else 'REFUTED'}")
    print(f"  M27A-G2 bins b/c/d <= 0.34:               "
          f"{'PASS' if m27a_g2 else 'REFUTED'}")
    print(f"  M27A-G3 plane collaterals 0.00:           "
          f"{'PASS' if m27a_g3 else 'REFUTED'}")
    print(f"  M27B-G1 ion_tail @(cns3,diff1.5) >= 0.34: "
          f"{rate('ion_channel_tail_m27'):.2f}  {'PASS' if m27b_g1 else 'REFUTED'}")
    print(f"  M27B-G2 ion_head > 0:                     "
          f"{rate('ion_channel_head_m27'):.2f}  {'PASS' if m27b_g2 else 'REFUTED'}")
    print(f"  M27B-G3 default inertness (bit-exact):    "
          f"{'PASS' if m27b_g3 else 'REFUTED'}")

    out = {
        "exp": "exp34_m27_candidates",
        "source": "sim-only candidate evaluation against exp31/exp32 records",
        "m27a_params": m27a,
        "m27b_params": m27b,
        "sim_arms": sim,
        "criteria": {
            "M27A_G1_cross_a_whole_fragment_clip": m27a_g1,
            "M27A_G2_no_new_overshoot": m27a_g2,
            "M27A_G3_plane_collaterals": m27a_g3,
            "M27B_G1_ion_chain_diffusion": m27b_g1,
            "M27B_G2_ion_head_direction": m27b_g2,
            "M27B_G3_default_inertness": m27b_g3,
        },
        "recorded_reference": {
            "cross_bins": exp32["recorded_bin_means"],
            "ion_mean": 0.45,
            "exp32_cross_a_g1": exp32["sim_arms"]["cutting_cross_a"]["pred_abn_rate"],
            "exp32_ion_tail_cns3": exp32["sim_arms"]["ion_channel_tail_cns3"]["pred_abn_rate"],
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "M27a redesign justification: exp32 showed the 5-cell face "
            "window is a no-op on head-only fragments (plateau slope); the "
            "whole-fragment secant carries the head->trunk depolarization "
            "trend; the clip bounds commitment by the fragment's own "
            "identity repertoire (intrinsic, no target knowledge). M27b: "
            "chain-accumulating wander compounds commitment error (sd ~ "
            "diffusion*sqrt(d)) — the mechanism junction loss already has "
            "coherently, and i.i.d. noise (M26b) lacks."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
