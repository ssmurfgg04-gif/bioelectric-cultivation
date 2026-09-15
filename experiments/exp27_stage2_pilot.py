#!/usr/bin/env python3
"""exp27 — STAGE 2 PILOT: first per-experiment SIMULATION validation against
PlanformDB. exp21 tested the DATABASE against the model's signatures without
running the simulator; this runs the actual stack and compares predicted
regeneration outcome classes against recorded outcomes.

DATA (already in-repo):
  PlanformDB 2.5.0 (Lobo et al. 2013, Bioinformatics 29:608; Lobo Lab UMBC)
  data/planform/planformDB_2.5.0.edb — 1,716 experiments / 119 publications.
  Download source http://lobolab.umbc.edu/planform/downloads/planformDB_2.5.0.edb
  (re-verified live this session).

PILOT SLICE (the two classes where this repo's mechanisms speak directly):
  cutting       amputation-only experiments (no RNAi)
  innexin       RNAi against innexins (Dj-inx, Smed-inx): gap-junction loss

SIMULATION ARMS (3 seeds each, exp1 machinery, N=100 sheet):
  cutting           make_collective -> amputate tail -> regrow (GJs intact)
  innexin_sustained make_collective -> block GJs (0.05) -> 24h window ->
                    amputate + regrow WHILE BLOCKED (RNAi persists through
                    regeneration; this is the RNAi-realistic protocol)
  gjblock_restored  block -> 24h -> RESTORE -> 20h -> amputate + regrow
                    (T1.1c negative-control semantics: transient block that
                    clears before regeneration must NOT corrupt the outcome)

PRE-REGISTERED CRITERIA (fixed BEFORE any outcome query, anchored to exp1's
existing in-repo calibration: wt_stable < 3.0 mV, two-headed threshold
head-likeness 0.7 / pattern error 6.0 mV — no threshold was tuned for this
experiment):
  S2P1 ORDERING  sim predicted-abnormal rate(innexin_sustained) >
                 sim predicted-abnormal rate(cutting), AND recorded
                 abnormal(innexin) > recorded abnormal(cutting) in the same
                 slice — the model reproduces the recorded ordering.
  S2P2 CUTTING MAPPING  sim predicts WT-dominant for cutting AND recorded
                 cutting mean abnormal < 0.5 (WT-dominant majority).
                 Caveat carried from exp21: publication bias inflates the
                 recorded cutting baseline; a REFUTATION here bounds the
                 naive mapping, it does not invalidate the model.
  S2P3 CLASS MATCH (exploratory, no threshold) fraction of class-level
                 pairs where sim-predicted dominant outcome == recorded
                 dominant outcome. Reported, not gated.
  S2C  CONTROL   gjblock_restored predicted WT-dominant (consistency with
                 T1.1c). If REFUTED, the sustained-vs-transient distinction
                 is not load-bearing in the model and S2P1 must be
                 reinterpreted.

PREDICTION RULE (sim -> class, pre-registered):
  predicted_abnormal  iff  pattern_error(final V, wildtype_target) >= 6.0 mV
                           OR head_likeness(tail region) >= 0.7 (ectopic head)
  else predicted_wt_dominant

RECORDED CLASS (DB -> class):
  abnormal_dominant  iff Num-weighted mean over post-regeneration result
                     sets of (1 - freq(Wild type)) >= 0.5   [exp21 metric]

LIMITATIONS (stated up front): class-level mapping (one protocol per class,
no per-experiment dose/amputation-plane variation yet — that per-experiment
variation is exactly the overnight DeepScientist work); morphologies lumped
into WT vs abnormal; 100-cell species-agnostic sheet vs multi-species DB.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cultivation.bioelectric.collective import BioElectricCollective  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from cultivation.validation.stats import mean_se  # noqa: E402
from experiments.exp21_planform_benchmark import (  # noqa: E402
    DB, load_experiments,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp27_stage2_pilot.json")

N = 100
DT = 0.1
SEEDS = (1, 2, 3)

# pre-registered thresholds (exp1 calibration, untouched)
ABN_ERR_MV = 6.0
ABN_HL = 0.7
TAIL = slice(3 * N // 4, N)


def make_collective(seed: int) -> BioElectricCollective:
    c = BioElectricCollective(n=N, seed=seed, noise_std=0.3)
    c.set_target(wildtype_target(N))
    c.run(10, dt=DT)
    return c


def amputate_regrow(c: BioElectricCollective) -> dict:
    c.amputate(slice(85, 100), wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(slice(85, 100), cell_period=0.8, dt=DT, noise=0.6)
    c.run(15, dt=DT)
    return {
        "wt_pattern_error": c.pattern_error(wildtype_target(N)),
        "head_likeness_tail": head_likeness(c.V, TAIL),
        "head_likeness_head": head_likeness(c.V, slice(0, N // 4)),
    }


def run_arm(arm: str, seed: int) -> dict:
    c = make_collective(seed)
    if arm == "cutting":
        m = amputate_regrow(c)
    elif arm == "innexin_sustained":
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        m = amputate_regrow(c)          # block persists through regen
    elif arm == "gjblock_restored":
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        c.restore_gap_junctions(1.0)
        c.run(20, dt=DT)
        m = amputate_regrow(c)
    else:
        raise ValueError(arm)
    m["seed"] = seed
    m["predicted_abnormal"] = bool(
        m["wt_pattern_error"] >= ABN_ERR_MV
        or m["head_likeness_tail"] >= ABN_HL
    )
    return m


def sim_arm(arm: str) -> dict:
    runs = [run_arm(arm, s) for s in SEEDS]
    errs = [r["wt_pattern_error"] for r in runs]
    hls = [r["head_likeness_tail"] for r in runs]
    ms_e, ms_h = mean_se(errs), mean_se(hls)
    return {
        "runs": runs,
        "wt_pattern_error_mean": ms_e["mean"],
        "wt_pattern_error_se": ms_e["se"],
        "head_likeness_tail_mean": ms_h["mean"],
        "head_likeness_tail_se": ms_h["se"],
        "predicted_abn_rate": float(np.mean([r["predicted_abnormal"]
                                             for r in runs])),
    }


def main() -> dict:
    print("=== exp27: Stage 2 pilot — per-experiment sim validation vs "
          "PlanformDB (cutting + innexin slice) ===\n")

    con = sqlite3.connect(DB)
    exps = load_experiments(con)
    slice_exps = {eid: e for eid, e in exps.items()
                  if e["group"] in ("cutting", "innexin")}
    for grp in ("cutting", "innexin"):
        vals = [e["abnormal"] for e in slice_exps.values()
                if e["group"] == grp]
        ms = mean_se(vals)
        print(f"  recorded {grp:9s} n={len(vals):4d}  "
              f"abnormal {ms['mean']:.3f} ± {ms['se']:.3f}")

    print()
    sim = {arm: sim_arm(arm) for arm in
           ("cutting", "innexin_sustained", "gjblock_restored")}
    for arm, s in sim.items():
        print(f"  sim {arm:17s} err {s['wt_pattern_error_mean']:5.2f} "
              f"± {s['wt_pattern_error_se']:4.2f} mV   "
              f"hl_tail {s['head_likeness_tail_mean']:.2f}   "
              f"pred-abn {s['predicted_abn_rate']:.2f}")

    rec_cut = [e["abnormal"] for e in slice_exps.values()
               if e["group"] == "cutting"]
    rec_inx = [e["abnormal"] for e in slice_exps.values()
               if e["group"] == "innexin"]

    # ---- pre-registered criteria ------------------------------------------
    s2p1 = bool(sim["innexin_sustained"]["predicted_abn_rate"]
                > sim["cutting"]["predicted_abn_rate"]
                and np.mean(rec_inx) > np.mean(rec_cut))
    s2p2 = bool(sim["cutting"]["predicted_abn_rate"] == 0.0
                and np.mean(rec_cut) < 0.5)
    pairs = [("cutting", "cutting"), ("innexin_sustained", "innexin")]
    matches = 0
    for sim_arm_name, db_grp in pairs:
        sim_dom = ("abnormal_dominant"
                   if sim[sim_arm_name]["predicted_abn_rate"] >= 0.5
                   else "wt_dominant")
        rec_abn = rec_inx if db_grp == "innexin" else rec_cut
        rec_dom = ("abnormal_dominant" if np.mean(rec_abn) >= 0.5
                   else "wt_dominant")
        if sim_dom == rec_dom:
            matches += 1
    s2p3 = matches / len(pairs)
    s2c = bool(sim["gjblock_restored"]["predicted_abn_rate"] == 0.0)

    print(f"\n  S2P1 ordering (sim + recorded): "
          f"{'PASS' if s2p1 else 'REFUTED'}")
    print(f"  S2P2 cutting mapping:           "
          f"{'PASS' if s2p2 else 'REFUTED'}")
    print(f"  S2P3 class match rate:          {s2p3:.2f} (exploratory)")
    print(f"  S2C  restored-block control:    "
          f"{'PASS' if s2c else 'REFUTED'}")

    detail = {grp: [{"exp": eid, "rnais": e["rnais"],
                     "abnormal": round(e["abnormal"], 3),
                     "n_rs": e["n_rs"]}
                    for eid, e in sorted(slice_exps.items())
                    if e["group"] == grp]
               for grp in ("cutting", "innexin")}

    out = {
        "exp": "exp27_stage2_pilot",
        "source": "PlanformDB 2.5.0 (Lobo 2013), in-repo .edb",
        "n_slice_experiments": len(slice_exps),
        "n_cutting": len(rec_cut),
        "n_innexin": len(rec_inx),
        "sim_arms": sim,
        "recorded": {
            "cutting_mean_abnormal": float(np.mean(rec_cut)) if rec_cut else None,
            "innexin_mean_abnormal": float(np.mean(rec_inx)) if rec_inx else None,
        },
        "criteria": {
            "S2P1_ordering": bool(s2p1),
            "S2P2_cutting_mapping": bool(s2p2),
            "S2P3_class_match_rate": s2p3,
            "S2C_restored_control": bool(s2c),
        },
        "prediction_rule": (
            "predicted_abnormal iff wt_pattern_error >= 6.0 mV OR "
            "head_likeness_tail >= 0.7 (exp1 calibration, pre-registered)"),
        "slice_detail": detail,
        "notes": (
            "First per-experiment-class sim-vs-DB validation (exp21 was "
            "DB-only). Class-level mapping; per-experiment dose/plane "
            "variation is the overnight DeepScientist quest "
            "(docs/QUEST_STAGE2_VALIDATION.md)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
