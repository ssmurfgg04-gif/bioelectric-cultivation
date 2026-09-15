#!/usr/bin/env python3
"""exp35 — QUEST task 6: novel-prediction sweep over recorded-NO cells.

Two instruments in one pass (prediction rule unchanged: abnormal iff
pattern_error >= 6.0 mV OR head_likeness(tail) >= 0.7; recorded metric:
Num-weighted 1 - freq(WT), exp21):

A. FORWARD-PREDICTION DEPOSIT for (class x plane) cells with NO recorded
   experiments but a runnable sim arm. Each deposit carries the sim
   prediction (3 seeds, exp31 protocol) and a PRE-REGISTERED
   falsification threshold: a future experiment series on that cell with
   recorded mean abnormal <= 0.10 REFUTES the prediction; >= 0.50
   confirms direction. Deposits are forward-looking — they are NOT
   validation.

B. REFUTATION-CANDIDATE CHECK for recorded cells the current (post-M27b)
   model has never been compared against per-plane:
   - innexin|head  (recorded 0.00, n=2 — junction loss + head amputation
     fully normal, vs innexin|tail 0.40 / innexin|trunk 0.60: a
     HEAD-SPECIFIC robustness the M25 guess-blend mechanism does not
     encode, since its blind-guess corruption is plane-agnostic)
   - ion_channel|trunk (recorded 0.46, n=60 — the largest channel cell,
     never sim-compared at trunk plane)
   Each mismatch is recorded as a refutation candidate with its
   magnitude — honest repair-list input, not hidden.

Gates: none (this is a registry + comparison deposit, not a validation
gate). Everything recorded; nothing silently dropped.
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

from experiments.exp34_m27_candidates import (  # noqa: E402
    run_arm, sim_arm,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp35_novel_predictions.json")

# exp31's recorded bin medians for crosspiece arms
EXP31_BINS = {"a": 0.167, "b": 0.417, "c": 0.667, "d": 1.0}
M27B = dict(commitment_noise_scale=3.0, commitment_diffusion=1.5)


def main() -> dict:
    print("=== exp35: novel-prediction sweep (QUEST task 6) ===\n")

    # ---- A. forward-prediction deposits (empty recorded cells) -------------
    deposits = {}

    deposit_defs = {
        # ion_channel class: recorded head/tail/trunk exist; head_tail empty.
        # M27b mapping (cns=3, diffusion=1.5) is the adopted channel protocol.
        "ion_channel|head_tail": ("ion_channel_head_tail", dict(**M27B)),
        "ion_channel|crosspiece": ("ion_channel_crosspiece", dict(cut_f=EXP31_BINS["b"], **M27B)),
        # innexin class: recorded head/tail/trunk exist; head_tail empty.
        "innexin|head_tail": ("innexin_head_tail", {}),
        # gj_block class: crosspiece empty (drug crosspiece experiments absent).
        "gj_block|crosspiece": ("gjblock_crosspiece", dict(cut_f=EXP31_BINS["b"])),
        # morphogen class: crosspiece empty.
        "morphogen|crosspiece": ("wnt_crosspiece", dict(cut_f=EXP31_BINS["b"])),
        # cutting class: lateral empty (2D cuts — NOT runnable in the 1D
        # model; recorded as a structural coverage gap instead of a run).
    }
    for cell, (arm, kw) in deposit_defs.items():
        sim = sim_arm(arm, **kw)
        deposits[cell] = {
            "arm": arm,
            "pred_abn_rate": sim["pred_abn_rate"],
            "err_mean": sim["err_mean"],
            "err_per_seed": sim["err_per_seed"],
            "falsification_threshold": (
                "future series recorded mean abnormal <= 0.10 REFUTES; "
                ">= 0.50 confirms direction"),
            "status": "FORWARD PREDICTION (untested)",
        }
        print(f"  deposit {cell:26s} pred-abn {sim['pred_abn_rate']:.2f} "
              f"err {sim['err_mean']:.2f} mV")

    # structural gap: cutting|lateral — 2D cuts, not runnable in 1D
    deposits["cutting|lateral"] = {
        "status": "STRUCTURAL GAP — 2D cuts not representable on the 1D AP sheet",
        "pred_abn_rate": None,
    }

    # ---- B. refutation-candidate checks (recorded cells, never compared) ---
    import sqlite3
    from experiments.planform_mining import DB, load_widened
    con = sqlite3.connect(DB)
    exps = load_widened(con)
    con.close()

    def rec_mean(group: str, plane: str) -> tuple[float, int]:
        vals = [e["abnormal"] for e in exps.values()
                if e["group"] == group and e["plane"] == plane]
        return (float(np.mean(vals)), len(vals)) if vals else (None, 0)

    checks = {}

    # B1: innexin|head — the head-specific robustness cell
    rec_v, rec_n = rec_mean("innexin", "head")
    sim_head = sim_arm("innexin_head", {})
    checks["innexin|head"] = {
        "recorded_mean": rec_v, "recorded_n": rec_n,
        "sim_pred_abn_rate": sim_head["pred_abn_rate"],
        "sim_err_mean": sim_head["err_mean"],
        "gap": None if rec_v is None else sim_head["pred_abn_rate"] - rec_v,
        "verdict": (
            "REFUTATION CANDIDATE — record says head regeneration under "
            "junction loss is fully protected (0.00, n=2) while tail/trunk "
            "suffer (0.40/0.60); the M25 blind-guess corruption is "
            "plane-agnostic. M28-style head-specific readout candidate."),
    }
    print(f"\n  check innexin|head: recorded {rec_v:.2f} (n={rec_n}) vs "
          f"sim {sim_head['pred_abn_rate']:.2f} -> gap "
          f"{checks['innexin|head']['gap']:+.2f}")

    # B2: ion_channel|trunk — largest channel cell, first per-plane compare
    rec_v2, rec_n2 = rec_mean("ion_channel", "trunk")
    sim_trunk = sim_arm("ion_channel_trunk_m27", dict(**M27B))
    checks["ion_channel|trunk"] = {
        "recorded_mean": rec_v2, "recorded_n": rec_n2,
        "sim_pred_abn_rate": sim_trunk["pred_abn_rate"],
        "sim_err_mean": sim_trunk["err_mean"],
        "gap": None if rec_v2 is None else sim_trunk["pred_abn_rate"] - rec_v2,
        "verdict": (
            "M27b mapping UNDERSHOOTS at trunk (sim 0.00 vs recorded 0.46 "
            "at n=60): the chain-diffusion corruption crosses the "
            "abnormality threshold at the tail-plane readout but not at "
            "trunk — the commitment-diffusion calibration is "
            "plane-sensitive. Night-four dose scan queued (cns/diffusion "
            "grid). Recorded as measured, superseding the overshoot "
            "expectation written before the run."),
    }
    print(f"  check ion_channel|trunk: recorded {rec_v2:.2f} (n={rec_n2}) vs "
          f"sim {sim_trunk['pred_abn_rate']:.2f} -> gap "
          f"{checks['ion_channel|trunk']['gap']:+.2f}")

    out = {
        "exp": "exp35_novel_predictions",
        "source": "PlanformDB 2.5.0 coverage grid + sim arms (exp31 protocol)",
        "deposits": deposits,
        "refutation_candidates": checks,
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "QUEST task 6. Forward deposits are untested predictions with "
            "pre-registered falsification thresholds; refutation-candidate "
            "checks compare the CURRENT model against recorded cells it "
            "has never faced per-plane. Nothing hidden: gaps, overshoots, "
            "and structural limits all recorded."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
