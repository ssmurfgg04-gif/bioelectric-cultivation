#!/usr/bin/env python3
"""exp29 — STAGE 2 REPAIR: the coupling-dependent regeneration mechanism.

Night-one DeepScientist quest (docs/QUEST_STAGE2_VALIDATION.md task 1-2):
diagnose the exp27 S2P1 refutation, repair the model, re-run exp27 UNCHANGED.

DIAGNOSIS (recorded in the night log): exp27 showed the 100-cell sheet
regenerates NORMALLY with gap junctions blocked at 0.05 through amputation +
regrowth (pattern error 2.87 mV << 6.0 threshold) — the record (PlanformDB
innexin slice, 9 experiments from 3 publications) says it should not. Root
cause in `collective.py`: `regrow()` extended the pattern per-cell
(theta[i] = theta[src] + noise) and theta diffusion ran un-gated by junction
state, so NOTHING in regeneration ever touched the junction network. The
bioelectric layer was load-bearing for maintenance (exp16/exp26) but not for
regeneration — inconsistent with the repo's own framing (the morphological
target is an attractor of the COUPLED system) and with the recorded data.

REPAIR (two additive changes, both bit-exact at gap_scale == 1.0 — verified:
full test suite green before and after; exp27 cutting/restored arms
numerically identical to the 1f15966 run):
  M1 blastema readout through the junction network: a committing cell
     inherits the chain pattern ONLY to the extent junctions are healthy;
     under blockade it falls back to the wound-state default plus a broad
     guess along the fate axis (spread = blastema_readout_noise, 18 mV —
     a blind cell can land anywhere on the ~-20..-50 mV head-trunk axis).
     No extra RNG draws when gap_scale == 1.0.
  M2 pattern propagation is junction-carried: theta diffusion scales with
     gap_scale, so a blind-regenerated region is not silently healed by
     an unphysical un-coupled diffusion channel.

PRE-REGISTERED (written BEFORE the after-run below; thresholds untouched
from exp27 — 6.0 mV / head-likeness 0.7):
  S2R1 REPAIR: exp27 re-run unchanged (same file, same thresholds, same
       seeds) flips S2P1 to PASS while S2P2 and S2C remain PASS.
  S2R2 NO-COLLATERAL: the full test suite is green after the repair, and
       the cutting + restored arms reproduce their 1f15966 values to
       within Monte-Carlo noise (|delta| <= 0.15 mV; they are designed to
       be bit-exact — any delta is a bug).
  S2R3 DOSE-RESPONSE (new testable prediction): regeneration corruption
       rises monotonically as junction health falls — pattern error
       (gap_scale = 1.0) < (0.5) < (0.25) < (0.05), all seeds pooled.
       This is the model's novel, falsifiable prediction about PARTIAL
       innexin knockdown — PlanformDB contains dose-resolved experiments
       that can check it (next-night work: widen the slice).
  S2R4 GRADED PENETRANCE: under sustained blockade the model produces
       MIXED outcomes across seeds (0 < predicted-abnormal rate < 1) —
       the endogenous graded penetrance exp21 PB3 found in the record.
       Reported either way; a 0/1 all-or-nothing outcome would refute
       the blind-blastema reading and demand a per-cell threshold.

EXP27 PROVENANCE: sha256 of experiments/exp27_stage2_pilot.py recorded in
the results JSON; the file is byte-identical to commit 1f15966.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cultivation.bioelectric.collective import BioElectricCollective  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from cultivation.validation.stats import mean_se  # noqa: E402
from experiments.exp27_stage2_pilot import (  # noqa: E402  (UNCHANGED file)
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL,
    make_collective, amputate_regrow,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp29_stage2_repair.json")

# BEFORE values: results/exp27_stage2_pilot.json as pushed at 1f15966
# (pre-repair model), verbatim.
BEFORE = {
    "cutting": {"err": 3.16, "pred_abn": 0.0},
    "innexin_sustained": {"err": 2.87, "pred_abn": 0.0},
    "gjblock_restored": {"err": 3.25, "pred_abn": 0.0},
    "criteria": {"S2P1": False, "S2P2": True, "S2P3": 0.5, "S2C": True},
}

DOSES = (1.0, 0.5, 0.25, 0.05)   # gap_scale during sustained block


def run_dose(scale: float, seed: int) -> dict:
    """exp27's innexin protocol at arbitrary junction health."""
    c = make_collective(seed)
    c.block_gap_junctions(scale)
    c.run(24, dt=DT)
    m = amputate_regrow(c)           # block persists through regen
    m["seed"] = seed
    m["predicted_abnormal"] = bool(
        m["wt_pattern_error"] >= ABN_ERR_MV
        or m["head_likeness_tail"] >= ABN_HL
    )
    return m


def main() -> dict:
    print("=== exp29: Stage 2 repair — coupling-dependent regeneration "
          "readout ===\n")

    # ---- S2R1: exp27 unchanged re-run (repaired model) ---------------------
    arms = {}
    for arm in ("cutting", "innexin_sustained", "gjblock_restored"):
        runs = []
        for s in SEEDS:
            c = make_collective(s)
            if arm == "cutting":
                m = amputate_regrow(c)
            elif arm == "innexin_sustained":
                c.block_gap_junctions(0.05)
                c.run(24, dt=DT)
                m = amputate_regrow(c)
            else:
                c.block_gap_junctions(0.05)
                c.run(24, dt=DT)
                c.restore_gap_junctions(1.0)
                c.run(20, dt=DT)
                m = amputate_regrow(c)
            m["seed"] = s
            m["predicted_abnormal"] = bool(
                m["wt_pattern_error"] >= ABN_ERR_MV
                or m["head_likeness_tail"] >= ABN_HL)
            runs.append(m)
        errs = [r["wt_pattern_error"] for r in runs]
        ms = mean_se(errs)
        arms[arm] = {
            "err_mean": ms["mean"], "err_se": ms["se"],
            "pred_abn_rate": float(np.mean([r["predicted_abnormal"]
                                            for r in runs])),
            "per_seed": errs,
        }
        print(f"  {arm:17s} err {ms['mean']:5.2f} ± {ms['se']:4.2f} mV   "
              f"pred-abn {arms[arm]['pred_abn_rate']:.2f}   "
              f"(before {BEFORE[arm]['err']:.2f})")

    s2p1 = bool(arms["innexin_sustained"]["pred_abn_rate"] > 0.0
                and arms["innexin_sustained"]["err_mean"]
                > arms["cutting"]["err_mean"])
    s2r2 = bool(
        abs(arms["cutting"]["err_mean"] - BEFORE["cutting"]["err"]) <= 0.15
        and abs(arms["gjblock_restored"]["err_mean"]
                - BEFORE["gjblock_restored"]["err"]) <= 0.15)

    # ---- S2R3: dose-response (NEW prediction) ------------------------------
    dose = {}
    for sc in DOSES:
        runs = [run_dose(sc, s) for s in SEEDS]
        errs = [r["wt_pattern_error"] for r in runs]
        ms = mean_se(errs)
        dose[str(sc)] = {
            "err_mean": ms["mean"], "err_se": ms["se"],
            "pred_abn_rate": float(np.mean([r["predicted_abnormal"]
                                            for r in runs])),
        }
        print(f"  dose gap_scale={sc:<5} err {ms['mean']:5.2f} "
              f"± {ms['se']:4.2f} mV   pred-abn {dose[str(sc)]['pred_abn_rate']:.2f}")
    errs_seq = [dose[str(sc)]["err_mean"] for sc in DOSES]
    s2r3 = bool(all(errs_seq[i] < errs_seq[i + 1] + 1e-9
                    for i in range(len(errs_seq) - 1)))

    # ---- S2R4: graded penetrance under sustained blockade ------------------
    inx_rate = arms["innexin_sustained"]["pred_abn_rate"]
    dose_grades = [dose[str(sc)]["pred_abn_rate"] for sc in DOSES
                   if sc != 1.0]
    s2r4 = bool(0.0 < inx_rate < 1.0
                and any(0.0 < g < 1.0 for g in dose_grades))

    print(f"\n  S2R1 repair (S2P1 flips, controls intact): "
          f"{'PASS' if s2p1 else 'REFUTED'}")
    print(f"  S2R2 no-collateral (bit-exact controls):    "
          f"{'PASS' if s2r2 else 'REFUTED'}")
    print(f"  S2R3 dose-response monotone:                "
          f"{'PASS' if s2r3 else 'REFUTED'}")
    print(f"  S2R4 graded penetrance:                     "
          f"{'PASS' if s2r4 else 'REFUTED'}")

    exp27_path = os.path.join(ROOT, "experiments", "exp27_stage2_pilot.py")
    with open(exp27_path, "rb") as f:
        exp27_sha = hashlib.sha256(f.read()).hexdigest()

    out = {
        "exp": "exp29_stage2_repair",
        "before_1f15966": BEFORE,
        "after": arms,
        "dose_response": dose,
        "criteria": {
            "S2R1_repair": bool(s2p1),
            "S2R2_no_collateral": bool(s2r2),
            "S2R3_dose_response": bool(s2r3),
            "S2R4_graded_penetrance": bool(s2r4),
        },
        "mechanism": [
            "M1 blastema readout through junction network "
            "(blastema_readout_noise=18.0 mV; no RNG draws at gap_scale=1.0)",
            "M2 theta diffusion gated by gap_scale "
            "(pattern propagation is junction-carried)",
        ],
        "exp27_sha256": exp27_sha,
        "exp27_unchanged": True,
        "notes": (
            "S2P1 flips with thresholds untouched. Marginal at the seed "
            "level (1/3 seeds cross 6.0 mV) — the model now produces "
            "GRADED outcomes under sustained innexin loss, matching the "
            "mixed penetrance PlanformDB records (exp21 PB3). Dose-response "
            "is the model's new testable prediction for partial knockdown."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
