#!/usr/bin/env python3
"""exp48 — M32 RECORD-CALIBRATED THRESHOLD FIT (night-six queue #4,
ledger L30).

LITERATURE BASIS (exp44): Pezzulo/Levin 2017 — the graded population
rate is "a constant ratio ... due NOT to partial penetrance of treatment"
but to "a multistable, epigenetic anatomical switch". The per-animal
binary outcome rule is CORRECT (each animal is all-or-nothing); the
population ratio comes from the switch. M32 therefore fits the model's
single outcome threshold to the corpus — it does NOT add graded
per-animal probabilities.

DATA: exp37's stored per-seed errors (36 arms, 1,029 mapped experiments,
weights = experiment counts). Per-class rate at threshold c:
    rate_class(c) = sum_rows(n_i * mean(err_per_seed[arm_i] >= c)) /
                    sum_rows(n_i)

PRE-REGISTERED FIT PROTOCOL:
  TRAIN   = {morphogen, innexin, gj_block}  (threshold-sensitive,
            mechanism-covered classes)
  HELD-OUT= {ion_channel}                   (predicted, not fitted)
  STRUCT. = {cutting, other_rnai}           (sim rate 0.0 at EVERY c —
            no mechanism layer; threshold-insensitive, excluded from the
            fit by pre-registration, reported as structural residuals)
  GRID    = 6.0 .. 14.0 mV step 0.5 (fixed before fitting)
  OBJECTIVE: weighted MAE over TRAIN classes (weights = class n)

GATES (fixed BEFORE the fit ran):
  M32-G1  UNIQUE INTERIOR OPTIMUM: the argmin is strictly inside the
          grid (a grid-edge optimum refutes M32 as unconstrained) and
          strictly better than both neighbours.
  M32-G2  TRAIN IMPROVEMENT: train MAE at the fitted c < train MAE at
          the legacy 6.0 mV.
  M32-G3  HELD-OUT IMPROVEMENT: ion_channel MAE at the fitted c < its
          MAE at 6.0 (the fit generalizes to an unfitted class).
  M32-G4  CROSS-COMPATIBILITY WITH THE STAGE-2 SLICE: exp45's M31-A
          qualifying cross_a per-seed errors must STRADDLE the fitted
          threshold (split rate in {1/3, 2/3} at the fitted c) — the
          corpus calibration must not kill the Stage-2 penetrance
          mechanism. Failure here means absolute-mV thresholds are NOT
          jointly identified (the exp39 scoping note), and the per-class
          shift is structural (the missing gene layer), not a threshold
          artifact.

RUN: pure re-analysis of stored results (no simulation; deterministic).
Serial, BLAS pinned.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp48_m32_threshold_fit.json")

GRID = [6.0 + 0.5 * k for k in range(17)]          # 6.0 .. 14.0
TRAIN = ["morphogen", "innexin", "gj_block"]
HELDOUT = ["ion_channel"]
STRUCTURAL = ["cutting", "other_rnai"]


def main() -> dict:
    print("=== exp48: M32 record-calibrated threshold fit ===\n")

    exp37 = json.load(open(os.path.join(ROOT, "results",
                                        "exp37_full_sweep.json")))
    exp45 = json.load(open(os.path.join(ROOT, "results",
                                        "exp45_m31_anchor_history.json")))
    rows = exp37["rows"]
    arms = exp37["sim_arms"]

    def class_rate(cls: str, c: float) -> tuple[float, int]:
        num = den = 0.0
        for r in rows:
            if r.get("group") != cls or r.get("sim_arm") not in arms:
                continue
            errs = arms[r["sim_arm"]]["err_per_seed"]
            n_i = int(r.get("n") or 1)
            num += n_i * float(np.mean([e >= c for e in errs]))
            den += n_i
        return (num / den if den else 0.0), int(den)

    recorded = {k: v["recorded"] for k, v in exp37["per_class"].items()}
    weights = {k: v["n"] for k, v in exp37["per_class"].items()}

    curve: dict[str, list[float]] = {}
    for cls in TRAIN + HELDOUT + STRUCTURAL:
        curve[cls] = [class_rate(cls, c)[0] for c in GRID]
        den = class_rate(cls, GRID[0])[1]
        print(f"  {cls:12s} n={den:4d} rec={recorded.get(cls, float('nan')):.3f} "
              + " ".join(f"{v:.2f}" for v in curve[cls]))

    def mae(classes, c_idx):
        tot = w = 0.0
        for cls in classes:
            n_w = weights.get(cls, 1)
            tot += n_w * abs(curve[cls][c_idx] - recorded.get(cls, 0.0))
            w += n_w
        return tot / w if w else float("nan")

    train_mae = [mae(TRAIN, k) for k in range(len(GRID))]
    k_best = int(np.argmin(train_mae))
    interior = 0 < k_best < len(GRID) - 1
    unique_strict = interior and \
        train_mae[k_best] < train_mae[k_best - 1] and \
        train_mae[k_best] < train_mae[k_best + 1]
    m32_g1 = bool(unique_strict)
    c_fit = GRID[k_best]
    m32_g2 = bool(train_mae[k_best] < train_mae[0])
    ho_mae = [abs(curve["ion_channel"][k] - recorded["ion_channel"])
              for k in range(len(GRID))]
    m32_g3 = bool(ho_mae[k_best] < ho_mae[0])

    # G4: M31-A cross-compatibility
    ca = exp45["sim_arms"].get("cutting_cross_a_i50")
    straddle = None
    if ca:
        errs = ca["err_per_seed"]
        rate_at_fit = float(np.mean([e >= c_fit for e in errs]))
        straddle = rate_at_fit in (1 / 3, 2 / 3)
    m32_g4 = bool(straddle) if straddle is not None else None

    print(f"\n  train MAE curve: " + " ".join(f"{v:.3f}" for v in train_mae))
    print(f"  fitted c = {c_fit:.1f} mV (grid index {k_best})")
    print(f"  M32-G1 unique interior optimum:      "
          f"{'PASS' if m32_g1 else 'REFUTED'}")
    print(f"  M32-G2 train improvement ({train_mae[0]:.3f} -> "
          f"{train_mae[k_best]:.3f}):          "
          f"{'PASS' if m32_g2 else 'REFUTED'}")
    print(f"  M32-G3 held-out ion_channel improvement "
          f"({ho_mae[0]:.3f} -> {ho_mae[k_best]:.3f}): "
          f"{'PASS' if m32_g3 else 'REFUTED'}")
    print(f"  M32-G4 M31-A straddle at fitted c "
          f"(rate {rate_at_fit if ca else 'n/a'}): "
          f"{'n/a' if m32_g4 is None else ('PASS' if m32_g4 else 'REFUTED')}")

    struct_mae = {cls: abs(curve[cls][k_best] - recorded[cls])
                  for cls in STRUCTURAL}
    out = {
        "exp": "exp48_m32_threshold_fit",
        "mechanism": (
            "M32: single record-calibrated outcome threshold fitted to "
            "the corpus under a pre-registered train/held-out split; "
            "per-animal binary rule retained (Pezzulo/Levin 2017: the "
            "graded population rate is a multistable-switch constant "
            "ratio, not partial treatment penetrance)"),
        "grid_mV": GRID,
        "train_classes": TRAIN,
        "held_out_classes": HELDOUT,
        "structural_classes": STRUCTURAL,
        "fitted_threshold_mV": c_fit,
        "rate_curves": {cls: {"grid": GRID, "rates": curve[cls],
                              "recorded": recorded.get(cls)}
                        for cls in curve},
        "train_mae_curve": train_mae,
        "structural_residual_mae_at_fit": struct_mae,
        "criteria": {
            "M32_G1_unique_interior_optimum": m32_g1,
            "M32_G2_train_improvement": m32_g2,
            "M32_G3_heldout_improvement": m32_g3,
            "M32_G4_m31a_cross_compatibility": m32_g4,
        },
        "notes": (
            "The 2017 paper's constant-ratio finding predicts the binary "
            "per-animal rule is correct — the fit tests only WHERE the "
            "all-or-nothing line sits. G4 checks joint identification "
            "with the Stage-2 slice calibration (exp45's M31-A split)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
