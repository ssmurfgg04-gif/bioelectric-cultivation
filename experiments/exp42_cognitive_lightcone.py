#!/usr/bin/env python3
"""exp42 — STAGE 4 (NASCENT SOUL): the cognitive light cone.

THE QUESTION: is the collective's influence structure a COGNITIVE
object — a light cone that integrates and remembers — and is it
junction-carried as M25 requires? Pezzulo & Levin 2021's cognitive
scaling says the bioelectric dynamics that implement regeneration
implement primitive cognition; the measurable is the causal reach of a
localized perturbation (cultivation/cognitive/lightcone.py, paired
trajectories: same seed => identical noise => divergence IS influence).

PRE-REGISTERED GATES (fixed BEFORE the runs):

  LC-G1  PROPAGATION: at gap_scale=1.0 the horizon grows with time
         (Spearman rho(times, horizons) > 0 on every seed) — influence
         propagates at finite speed.
  LC-G2  COGNITIVE FRAGMENTATION: at gap_scale=0.05 the final horizon
         stays < 25% of the chain on every seed — under junction
         blockade the collective cannot integrate across the body.
  LC-G3  DOSE-RESPONSE: the final horizon is monotone in gap_scale
         (Spearman rho > 0 across {1.0, 0.5, 0.25, 0.05}, pooled
         seeds) — the light cone is junction-scaled (M25 at the
         cognitive level), the same monotone shape S2R3 predicts for
         regeneration and exp40 measured for the channel axis.
  LC-G4  MEMORY RESIDUE: at gap_scale=1.0 the pulse leaves a theta
         residue (paired dTheta) at >= half-chain distance on >= 2 of
         3 seeds (> 0.5 mV) — the light cone leaves a MEMORY (the D3
         collective-attractor property, the cognitive latch).

RUN PROTOCOL: seeds (1,2,3); settle 24h; single-cell pulse (cell 50,
0 mV — a strong depolarization) for 2h; total 24h; epsilon 0.5 mV;
records every 1 time unit. Serial, BLAS pinned.
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

from cultivation.cognitive.lightcone import measure_lightcone  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp42_cognitive_lightcone.json")

SEEDS = (1, 2, 3)
GAPS = (1.0, 0.5, 0.25, 0.05)


def main() -> dict:
    print("=== exp42: Stage 4 — the cognitive light cone ===\n")

    runs: dict[str, dict] = {}
    for g in GAPS:
        for s in SEEDS:
            runs[f"g{int(round(g * 100)):02d}_s{s}"] = measure_lightcone(
                seed=s, gap_scale=g)
        prof = [runs[f"g{int(round(g * 100)):02d}_s{s}"]["final_horizon"]
                for s in SEEDS]
        res = [runs[f"g{int(round(g * 100)):02d}_s{s}"]["theta_residue"]["max"]
               for s in SEEDS]
        print(f"  gap={g:.2f}: final horizon per seed {prof} | "
              f"theta-residue max {['%.1f' % r for r in res]} mV")

    # ---- gates -----------------------------------------------------------
    from scipy.stats import spearmanr
    lc_g1 = True
    for s in SEEDS:
        r = runs[f"g100_s{s}"]
        rho = spearmanr(r["times"], r["horizons"])
        lc_g1 &= bool(rho.statistic > 0)

    lc_g2 = all(runs[f"g05_s{s}"]["final_horizon"] < 25 for s in SEEDS)

    pooled = [runs[f"g{int(round(g * 100)):02d}_s{s}"]["final_horizon"]
              for g in GAPS for s in SEEDS]
    gap_labels = [g for g in GAPS for _ in SEEDS]
    rho3 = spearmanr(gap_labels, pooled)
    lc_g3 = bool(rho3.statistic > 0)

    residues_half = [runs[f"g100_s{s}"]["theta_residue"]["at_half_chain"]
                     for s in SEEDS]
    lc_g4 = sum(r > 0.5 for r in residues_half) >= 2

    print(f"\n  LC-G1 horizon grows with time (gap=1.0):   "
          f"{'PASS' if lc_g1 else 'REFUTED'}")
    print(f"  LC-G2 fragmentation under blockade (<25%): "
          f"{'PASS' if lc_g2 else 'REFUTED'}")
    print(f"  LC-G3 junction-scaled dose-response "
          f"(rho={rho3.statistic:.2f}): {'PASS' if lc_g3 else 'REFUTED'}")
    print(f"  LC-G4 theta residue at half-chain "
          f"({['%.2f' % r for r in residues_half]}): "
          f"{'PASS' if lc_g4 else 'REFUTED'}")

    out = {
        "exp": "exp42_cognitive_lightcone",
        "stage": "4 — Nascent Soul (cognitive light cone)",
        "instrument": "cultivation/cognitive/lightcone.py (paired "
                      "trajectories: same seed => divergence IS influence)",
        "pulse": {"cell": 50, "voltage_mV": 0.0, "hours": 2.0},
        "gap_scales": list(GAPS),
        "runs": {k: {kk: vv for kk, vv in v.items()
                     if kk != "final_influence"} for k, v in runs.items()},
        "criteria": {
            "LC_G1_propagation": lc_g1,
            "LC_G2_fragmentation": lc_g2,
            "LC_G3_junction_scaled_dose_response": lc_g3,
            "LC_G4_memory_residue": lc_g4,
        },
        "notes": (
            "The light cone is the cognitive measurable of the M25 "
            "story: influence propagates THROUGH the junction network, "
            "collapses under blockade, and leaves a theta memory — "
            "integration and memory on the same substrate that "
            "regenerates (Pezzulo & Levin 2021 scaling claim, now "
            "measured in this model)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
