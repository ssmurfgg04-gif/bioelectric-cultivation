#!/usr/bin/env python3
"""exp33 — S2R3a: drug-TIMING response (the dose axis PlanformDB actually has).

BACKGROUND: exp29's S2R3 predicted a monotone dose-response for junction
loss (3.28 -> 3.93 -> 4.54 -> 6.03 mV at gap_scale 1.0/0.5/0.25/0.05).
PlanformDB 2.5.0 carries NO concentrations (ExperimentDrug has only
StartTime/EndTime) — the concentration axis is a literature task (S2R3b).
But 45 GJ-blocker rows (octanol/heptanol/hexanol) carry EXPOSURE TIMING,
and 13 carry nonzero timing. Timing semantics (recorded as an assumption
BEFORE the outcome query): StartTime = hours of pre-treatment BEFORE the
cut; EndTime = hours AFTER the cut the drug is washed out; (0,0) =
timing unspecified; (t,0) t>0 = pre-treatment pulse, junctions RESTORED
during regeneration; (0,t) t>0 = applied at/after the cut, junctions
BLOCKED during regeneration.

PRE-REGISTERED PREDICTIONS (from the M25 mechanism, i.e. from exp27's
S2C restoration control extended per-experiment — fixed BEFORE the
outcome query below):

  S2R3a-1  WASHOUT-BEFORE-REGEN IS RECOVERY: experiments whose GJ-blocker
           exposure ENDED at/ before the cut ((t,0), t>0) are LESS
           abnormal than experiments whose exposure COVERED regeneration
           ((0,t), t>0). Direction gate on pooled means.
  S2R3a-2  The sim counterpart is already recorded: restored control 0.00
           abnormal vs sustained blockade 0.67 (exp29/exp31) — cited, no
           new sim runs.
  S2R3a-3  POWER HONESTY: with n ~= 13 usable rows the test is
           exploratory; verdicts are DIRECTIONAL (means ordered as
           predicted), with exact n recorded per arm. A direction miss
           against the mechanism is a REAL refutation signal (it would
           mean restoration timing does not matter, contradicting S2C).

  S2R3b (concentration monotonicity) is recorded as NOT YET CHECKABLE
  against this corpus — instrumentation gap, prediction stands untested.
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

from experiments.planform_mining import DB, load_widened  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp33_s2r3_timing.json")

GJ_DRUGS = ("Octanol", "Heptanol", "Hexanol")


def main() -> dict:
    print("=== exp33: S2R3a — GJ-blocker exposure-timing response ===\n")

    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT ed.Experiment, d.Name, ed.StartTime, ed.EndTime "
        "FROM ExperimentDrug ed JOIN Drug d ON d.Id = ed.Drug "
        f"WHERE d.Name IN {GJ_DRUGS}"
    ).fetchall()
    con.close()

    exps = load_widened(sqlite3.connect(DB))
    print(f"  corpus: {len(exps)} experiments with outcomes; "
          f"{len(rows)} GJ-blocker drug rows")

    arms: dict[str, list[dict]] = {
        "washout_before_regen": [],   # (t>0, 0): pulse, restored at regen
        "regen_covered": [],          # (0, t>0): blocked through regen
        "timing_unspecified": [],     # (0,0): excluded from the test
        "other": [],                  # any other pattern (record)
    }
    for eid, drug, t0, t1 in rows:
        e = exps.get(str(eid)) or exps.get(eid)
        rec = {
            "exp": eid, "drug": drug, "start": t0, "end": t1,
            "abnormal": None if e is None else round(e["abnormal"], 3),
            "plane": None if e is None else e["plane"],
            "group": None if e is None else e["group"],
        }
        if t0 == 0.0 and t1 == 0.0:
            arms["timing_unspecified"].append(rec)
        elif t0 > 0.0 and t1 == 0.0:
            arms["washout_before_regen"].append(rec)
        elif t0 == 0.0 and t1 > 0.0:
            arms["regen_covered"].append(rec)
        else:
            arms["other"].append(rec)

    for name, lst in arms.items():
        vals = [r["abnormal"] for r in lst if r["abnormal"] is not None]
        mean = float(np.mean(vals)) if vals else None
        print(f"  {name:22s} n={len(lst):2d} (with outcome {len(vals):2d})"
              + (f"  mean abnormal {mean:.3f}" if mean is not None else ""))
        for r in lst:
            print(f"      exp {r['exp']:>5} {r['drug']:9s} "
                  f"({r['start']:.2f},{r['end']:.2f}) "
                  f"abn={r['abnormal']} plane={r['plane']} group={r['group']}")

    wash = [r["abnormal"] for r in arms["washout_before_regen"]
            if r["abnormal"] is not None]
    cov = [r["abnormal"] for r in arms["regen_covered"]
           if r["abnormal"] is not None]
    mean_wash = float(np.mean(wash)) if wash else None
    mean_cov = float(np.mean(cov)) if cov else None

    s2r3a_1 = bool(mean_wash is not None and mean_cov is not None
                   and mean_wash < mean_cov)
    print(f"\n  S2R3a-1 washout ({mean_wash:.3f}, n={len(wash)}) < "
          f"regen-covered ({mean_cov:.3f}, n={len(cov)}): "
          f"{'PASS' if s2r3a_1 else 'REFUTED'}")

    out = {
        "exp": "exp33_s2r3_timing",
        "source": "PlanformDB 2.5.0 ExperimentDrug timing (no concentrations)",
        "timing_semantics_assumption": (
            "StartTime = hours pre-treatment before the cut; EndTime = hours "
            "post-cut washout; (0,0) = unspecified — recorded BEFORE the "
            "outcome query"),
        "arms": arms,
        "washout_mean": mean_wash,
        "regen_covered_mean": mean_cov,
        "criteria": {
            "S2R3a_1_washout_recovers": s2r3a_1,
            "S2R3a_2_sim_counterpart": True,  # exp29/exp31 recorded: 0.00 vs 0.67
            "S2R3a_3_power_flag": "exploratory, n=13 usable rows",
            "S2R3b_concentration_axis": (
                "NOT CHECKABLE against PlanformDB 2.5.0 (no dose column) — "
                "literature task; prediction stands untested, not falsified"),
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7 (sim side); recorded abnormality "
            "is Num-weighted 1 - freq(WT) (exp21 metric)"),
        "notes": (
            "The M25 mechanism predicts restoration timing matters: a pulse "
            "that ends at the cut leaves junctions readable during "
            "regeneration (S2C control logic, per experiment). Directional "
            "test only — n is small; a direction miss is a real refutation "
            "signal for the restoration mechanism."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
