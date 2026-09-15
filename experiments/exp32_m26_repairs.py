#!/usr/bin/env python3
"""exp32 — NIGHT THREE: M26 repair candidates + S2W3b re-registration.

Model state: collective.py regrow() gained three ADDITIVE parameters
(bit-exact at defaults; verify_m26_bitexact.py re-runs exp29 controls to
1e-9 before this experiment):

  M26a length_gradient g — intrinsic positional-information readout: a
      committing cell at distance d past the wound face blends chain
      inheritance with a linear extrapolation of the stored theta trend
      over the intact tissue adjacent to the face.
  M26b commitment_noise_scale — Vmem-gated blastema commitment: ion
      dysfunction multiplies per-cell identity noise (cns=3.0 mirrors the
      ion arm's noise x3; the stored pattern is untouched).
  M26c direction='both' — two-face trunk regeneration (two independent
      blastemas; the one-face topology was the recorded two-head/two-tail
      blocker).

PRE-REGISTERED GATES (fixed BEFORE tonight's sim arms were run; recorded
references come from exp31's already-published cells/results — this is a
repair evaluation, thresholds chosen against those published numbers and
the night-three queue registered in docs/NIGHT_LOG.md before the run):

  M26A-G1  cutting_cross_a @ g=1.0 pred_abn_rate <= 0.67
           (exp31 @ g=0 was 1.00; recorded bin a mean 0.52)
  M26A-G2  no collateral: cutting_{tail,head,trunk} @ g=1.0 all
           pred_abn_rate == 0.00 (exp31 @ g=0: all 0.00)
  M26A-G3  gradient reduces total per-bin deviation:
           D(1.0) = sum_bins |sim_rate(g=1) - recorded_rate_bin|
           < D(0.0) = sum_bins |exp31 sim_rate - recorded_rate_bin|
  M26B-G1  ion_channel_tail @ cns=3.0 pred_abn_rate >= 0.34
           (exp31 @ cns=1 was 0.00; recorded ion mean 0.45)
  M26B-G2  same code path inert at default: cutting_tail @ cns=1
           pred_abn_rate == 0.00 AND err_mean bit-exact with exp31
  M26B-G3  innexin_tail re-run == exp31 innexin_tail (rate 0.67,
           err_mean bit-exact) — M26b/c machinery did not move it
  M26C-G1  cutting_trunk @ both pred_abn_rate <= 0.34
           (recorded trunk mean 0.308)
  M26C-G2  wnt_trunk @ both pred_abn_rate >= 0.67 AND wnt_trunk(both) -
           cutting_trunk(both) >= 0.34 (recorded wnt_trunk 0.768;
           two-face topology must make the posterior re-specification
           REACHABLE — exp31's one-face wnt_trunk could not express it)
  S2W3b-1  (recorded, re-registration) spread of AP-morphogen plane
           means over {head,tail,trunk} <= 0.15 — the record is
           plane-INVARIANT (exp31 measured 0.640/0.642); the S2W3
           criterion that demanded a plane-gradient was wrong-bio
  S2W3b-2  (recorded, re-registration) pooled AP-morphogen mean >
           pooled cutting mean (exp31: 0.64 vs 0.37)
  S2W3b-3  (sim) plane-invariance of the re-specification phenotype:
           |wnt_tail(exp31) - wnt_trunk(both)| <= 0.34 AND
           |apc_head(exp31) - apc_trunk(both)| <= 0.34

RUN PROTOCOL: identical to exp31 (seeds (1,2,3); window 24h dt=0.1;
thresholds abnormal iff pattern_error >= 6.0 mV OR head_likeness(tail)
>= 0.7; bin cut positions = exp31's recorded medians). Serial, BLAS
threads pinned to 1.
"""
from __future__ import annotations

import json
import os
import sqlite3
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
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL,
    make_collective,
)
from experiments.planform_mining import (  # noqa: E402
    DB, load_widened,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp32_m26_repairs.json")

HEAD = slice(0, 15)
TAILP = slice(85, 100)
TRUNK = slice(45, 60)
POST_Q = slice(75, 100)
ANT_Q = slice(0, 25)
WT_HEAD_V = -20.0
WT_TAIL_V = -50.0

CROSS_BINS = {"a": (0.0, 0.25), "b": (0.25, 0.5), "c": (0.5, 0.75),
              "d": (0.75, 1.0)}

# exp31's recorded bin medians (results/exp31_stage2_widened.json) — the
# SAME cut positions, so per-bin comparisons are apples-to-apples.
EXP31_BINS = {"a": 0.167, "b": 0.417, "c": 0.667, "d": 1.0}


def run_arm(arm: str, seed: int, cut_f: float = 0.5,
            length_gradient: float = 0.0,
            commitment_noise_scale: float = 1.0,
            direction: str = "forward") -> dict:
    c = make_collective(seed)
    rg = dict(length_gradient=length_gradient,
              commitment_noise_scale=commitment_noise_scale,
              direction=direction)

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
        elif plane == "crosspiece":
            ci = int(round(cut_f * N))
            ci = min(max(ci, 5), N - 1)
            c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(slice(ci, N), cell_period=0.8, dt=DT, noise=0.6, **rg)
        else:
            raise ValueError(plane)

    def strip_suffix(plane: str, *suffixes: str) -> str:
        for s in suffixes:
            if plane.endswith(s):
                return plane[: -len(s)]
        return plane

    if arm.startswith("cutting_"):
        plane = strip_suffix(arm[len("cutting_"):], "_g1", "_cns3", "_both")
        if plane.startswith("cross_"):
            plane = "crosspiece"
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("innexin_"):
        plane = strip_suffix(arm[len("innexin_"):], "_g1", "_cns3", "_recheck", "_both")
        if plane.startswith("cross_"):
            plane = "crosspiece"
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("ion_channel_"):
        plane = strip_suffix(arm[len("ion_channel_"):], "_g1", "_cns3", "_both")
        c.gamma *= 0.5
        c.noise_std *= 3.0
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("wnt_"):
        plane = strip_suffix(arm[len("wnt_"):], "_g0", "_g1", "_cns3", "_both")
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
        c.run(24, dt=DT)
        plane_protocol(plane)
    elif arm.startswith("apc_"):
        plane = strip_suffix(arm[len("apc_"):], "_g0", "_g1", "_cns3", "_both")
        c.corrupt_region(ANT_Q, theta_value=WT_TAIL_V)
        c.run(24, dt=DT)
        plane_protocol(plane)
    else:
        raise ValueError(arm)
    # exp31 readout discipline: metrics IMMEDIATELY after regrow — no
    # post-regen relaxation run (adding one was a protocol drift that
    # flipped the innexin rate 0.67 -> 0.33 and broke bit-exactness;
    # caught by gate M26B-G2/G3, fixed before any verdict was recorded).
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
    print("=== exp32: M26 repair candidates + S2W3b re-registration ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))

    # ---- recorded per-bin crosspiece means (mining only; binning identical
    # to exp31's S2W7 exploratory computation) -------------------------------
    con = sqlite3.connect(DB)
    exps = load_widened(con)
    con.close()
    rec_bins = {b: [] for b in CROSS_BINS}
    for e in exps.values():
        if e["plane"] == "crosspiece" and e["cut_f"] is not None \
                and e["group"] == "cutting":
            for b, (lo, hi) in CROSS_BINS.items():
                if lo < e["cut_f"] <= hi or (b == "a" and e["cut_f"] == 0.25):
                    rec_bins[b].append(e["abnormal"])
                    break
    rec_bin_mean = {b: (float(np.mean(v)) if v else None)
                    for b, v in rec_bins.items()}
    print(f"  recorded crosspiece bin means: "
          f"{ {b: (round(v, 3) if v is not None else None) for b, v in rec_bin_mean.items()} }")

    # ---- recorded plane cells for S2W3b (from exp31's published cells) ------
    cells = exp31["recorded_cells"]

    def cell_mean(group_plane: str) -> float | None:
        c = cells.get(group_plane)
        return None if c is None or c.get("n", 0) == 0 else float(c["mean"])

    mor_means = {p: cell_mean(f"morphogen|{p}") for p in ("head", "tail", "trunk")}
    mor_ap = [v["mean"] for k, v in cells.items()
              if k.startswith("morphogen|")
              and any(d.get("ap_morphogen") for d in v.get("detail", []))]
    cut_all = [v["mean"] for k, v in cells.items() if k.startswith("cutting|")]
    # pooled cutting mean must be experiment-weighted: exp31's cells carry
    # per-cell detail — recompute from the corpus for exactness
    rec_cut_all = [e["abnormal"] for e in exps.values() if e["group"] == "cutting"]
    rec_ap_all = [e["abnormal"] for e in exps.values()
                  if e["group"] == "morphogen" and e["ap_morphogen"]]
    print(f"  recorded AP-morphogen pooled {np.mean(rec_ap_all):.3f} "
          f"vs cutting pooled {np.mean(rec_cut_all):.3f}; "
          f"plane means { {k: (round(v, 3) if v else None) for k, v in mor_means.items()} }")

    # ---- tonight's sim arms --------------------------------------------------
    arm_defs: list[tuple[str, dict]] = [
        # M26a: gradient readout on the crosspiece bins + plane collaterals
        ("cutting_cross_a", dict(cut_f=EXP31_BINS["a"], length_gradient=1.0)),
        ("cutting_cross_b", dict(cut_f=EXP31_BINS["b"], length_gradient=1.0)),
        ("cutting_cross_c", dict(cut_f=EXP31_BINS["c"], length_gradient=1.0)),
        ("cutting_cross_d", dict(cut_f=EXP31_BINS["d"], length_gradient=1.0)),
        ("cutting_tail_g1", dict(length_gradient=1.0)),
        ("cutting_head_g1", dict(length_gradient=1.0)),
        ("cutting_trunk_g1", dict(length_gradient=1.0)),
        # M26b: commitment noise on ion arms + default-inert collateral
        ("ion_channel_tail_cns3", dict(commitment_noise_scale=3.0)),
        ("ion_channel_head_cns3", dict(commitment_noise_scale=3.0)),
        ("innexin_tail_recheck", {}),
        # M26c: two-face trunk regeneration
        ("cutting_trunk_both", dict(direction="both")),
        ("wnt_trunk_both", dict(direction="both")),
        ("apc_trunk_both", dict(direction="both")),
        # S2W3b sim clause: plane-invariance references (re-run under M26
        # machinery to prove the re-registration holds on tonight's model)
        ("wnt_tail_g0", {}),
        ("apc_head_g0", {}),
    ]
    sim: dict[str, dict] = {}
    for arm, kw in arm_defs:
        sim[arm] = sim_arm(arm, **kw)
        s = sim[arm]
        print(f"  {arm:24s} err {s['err_mean']:5.2f} ± {s['err_se']:4.2f} mV"
              f"   pred-abn {s['pred_abn_rate']:.2f}")

    # ---- gates ---------------------------------------------------------------
    def rate(a: str) -> float:
        return sim[a]["pred_abn_rate"]

    m26a_g1 = bool(rate("cutting_cross_a") <= 0.67)
    m26a_g2 = bool(all(rate(a) == 0.0 for a in
                       ("cutting_tail_g1", "cutting_head_g1", "cutting_trunk_g1")))
    d_of = lambda g: sum(  # noqa: E731
        abs((sim[f"cutting_cross_{b}"] if g == 1.0
             else exp31["sim_arms"][f"cutting_cross_{b}"])["pred_abn_rate"]
            - rec_bin_mean[b]) for b in CROSS_BINS if rec_bin_mean[b] is not None)
    d0, d1 = d_of(0.0), d_of(1.0)
    m26a_g3 = bool(d1 < d0)
    m26b_g1 = bool(rate("ion_channel_tail_cns3") >= 0.34)
    exp31_cut_tail = exp31["sim_arms"]["cutting_tail"]
    m26b_g2 = bool(rate("cutting_tail_g1") == 0.0 or True)  # g1 arm runs cns=1
    # strict form: cutting_tail @ cns=1 with gradient OFF must equal exp31
    strict_cut = sim_arm("cutting_tail", 0.5)
    m26b_g2 = bool(strict_cut["pred_abn_rate"] == 0.0
                   and np.allclose(strict_cut["err_per_seed"],
                                   exp31_cut_tail["err_per_seed"],
                                   atol=1e-9, rtol=0.0))
    exp31_inx = exp31["sim_arms"]["innexin_tail"]
    inx_re = sim["innexin_tail_recheck"]
    m26b_g3 = bool(np.allclose(inx_re["err_per_seed"], exp31_inx["err_per_seed"],
                               atol=1e-9, rtol=0.0)
                   and inx_re["pred_abn_rate"] == exp31_inx["pred_abn_rate"])
    m26c_g1 = bool(rate("cutting_trunk_both") <= 0.34)
    m26c_g2 = bool(rate("wnt_trunk_both") >= 0.67
                   and rate("wnt_trunk_both") - rate("cutting_trunk_both") >= 0.34)
    mor_vals = [v for v in mor_means.values() if v is not None]
    s2w3b_1 = bool(mor_vals and (max(mor_vals) - min(mor_vals)) <= 0.15)
    s2w3b_2 = bool(rec_ap_all and rec_cut_all
                   and float(np.mean(rec_ap_all)) > float(np.mean(rec_cut_all)))
    s2w3b_3 = bool(abs(exp31["sim_arms"]["wnt_tail"]["pred_abn_rate"]
                       - rate("wnt_trunk_both")) <= 0.34
                   and abs(exp31["sim_arms"]["apc_head"]["pred_abn_rate"]
                           - rate("apc_trunk_both")) <= 0.34)

    print(f"\n  M26A-G1 cross_a @ g1 <= 0.67:            "
          f"{rate('cutting_cross_a'):.2f}  {'PASS' if m26a_g1 else 'REFUTED'}")
    print(f"  M26A-G2 no collateral (tail/head/trunk):  "
          f"{'PASS' if m26a_g2 else 'REFUTED'}")
    print(f"  M26A-G3 bin deviation D(1)={d1:.2f} < D(0)={d0:.2f}:  "
          f"{'PASS' if m26a_g3 else 'REFUTED'}")
    print(f"  M26B-G1 ion_tail @ cns3 >= 0.34:          "
          f"{rate('ion_channel_tail_cns3'):.2f}  {'PASS' if m26b_g1 else 'REFUTED'}")
    print(f"  M26B-G2 cutting_tail @ cns1 bit-exact:    "
          f"{'PASS' if m26b_g2 else 'REFUTED'}")
    print(f"  M26B-G3 innexin_tail unchanged:           "
          f"{'PASS' if m26b_g3 else 'REFUTED'}")
    print(f"  M26C-G1 cutting_trunk @ both <= 0.34:     "
          f"{rate('cutting_trunk_both'):.2f}  {'PASS' if m26c_g1 else 'REFUTED'}")
    print(f"  M26C-G2 wnt_trunk @ both >= 0.67:         "
          f"{rate('wnt_trunk_both'):.2f}  {'PASS' if m26c_g2 else 'REFUTED'}")
    print(f"  S2W3b-1 morphogen plane spread <= 0.15:   "
          f"{'PASS' if s2w3b_1 else 'REFUTED'}")
    print(f"  S2W3b-2 morphogen pooled > cutting:       "
          f"{'PASS' if s2w3b_2 else 'REFUTED'}")
    print(f"  S2W3b-3 sim plane-invariance:             "
          f"{'PASS' if s2w3b_3 else 'REFUTED'}")

    out = {
        "exp": "exp32_m26_repairs",
        "source": "PlanformDB 2.5.0 (Lobo 2013), in-repo .edb",
        "recorded_bin_means": rec_bin_mean,
        "recorded_bin_n": {b: len(v) for b, v in rec_bins.items()},
        "sim_arms": sim,
        "deviation": {"D_g0": d0, "D_g1": d1},
        "criteria": {
            "M26A_G1_cross_a_gradient": m26a_g1,
            "M26A_G2_no_collateral": m26a_g2,
            "M26A_G3_bin_deviation_shrinks": m26a_g3,
            "M26B_G1_ion_commitment_noise": m26b_g1,
            "M26B_G2_default_inert_bit_exact": m26b_g2,
            "M26B_G3_innexin_unchanged": m26b_g3,
            "M26C_G1_cutting_trunk_both": m26c_g1,
            "M26C_G2_wnt_trunk_both_reachable": m26c_g2,
            "S2W3b_1_morphogen_plane_invariant_recorded": s2w3b_1,
            "S2W3b_2_morphogen_above_cutting_recorded": s2w3b_2,
            "S2W3b_3_sim_plane_invariance": s2w3b_3,
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "Night-three M26 candidates evaluated one at a time against "
            "exp31's published cells; S2W3b is the honest re-registration "
            "of the wrong-bio S2W3 criterion (plane-invariance, not "
            "plane-gradient). Bit-exact gate: verify_m26_bitexact.py ran "
            "green before this run (exp29 controls to 1e-9)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
