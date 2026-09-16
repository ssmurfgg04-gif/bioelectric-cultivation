#!/usr/bin/env python3
"""exp105 — THE TORUS'S RISING PRICE (ledger L87; exp104's
registered mechanism probe: the two-dial cell (4, 0) verified the
torus at every size but its err ROSE 3.82 -> 4.86 across
n=100..784. Two live candidates; whichever arm FLATTENS the trend
names the mechanism).

THE PROBES (torus(r, r), r in {10, 14, 20, 28}; the base arm is
exp104's deposit, not re-run):
  (a) PINNING: the (16, 0) cell — stronger gamma; if the rise is
      the gamma-4 window pinning losing ground on longer walks,
      gamma 16 flattens it.
  (b) COMMITMENT NOISE: (4, 0) with commit_noise=0.2 — the walk's
      per-cell identity noise (0.6 mV sd, hardcoded since exp90);
      if the rise is exp32's sqrt(d) commitment-noise compounding
      along the BFS order, noise 0.2 flattens it.
  (c) the COMBO (16, 0 + noise 0.2) — the mixed case.

PRE-REGISTERED GATES:

  TP-G1  (the mechanism named) at least one probe arm flattens the
         trend: err(n=784) - err(n=100) <= 0.3 mV (the base trend
         is +1.04). Both flatten -> mixed; neither -> a third
         mechanism (registered deeper, no claim).
  TP-G2  (probe validity) every probe arm verifies >= 2/3 seeds at
         every size — a failing probe says nothing about trends.
  TP-G3  (noise sanity) the low-noise arm at n=100 sits within
         +/- 0.5 mV of the base 3.82 — the noise scale's
         base-level effect is small, so any flattening is a trend
         effect, not a level shift.

RUN: 3 probe arms x 4 sizes x 3 seeds = 36 runs. Serial, BLAS
pinned.
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

from experiments.exp94_multizone_scale import execute_two_source_n, MULTI
from experiments.exp68_coherence_search import torus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp105_torus_rising_price.json")

SEEDS3 = (1, 2, 3)
SIZES = (100, 196, 400, 784)
BASE_DELTA = 1.04   # exp104: 4.86 - 3.82
ARMS = {
    "pin_16_0": {"gamma": 16.0, "mu": 0.0, "commit_noise": 0.6},
    "noise02_4_0": {"gamma": 4.0, "mu": 0.0, "commit_noise": 0.2},
    "combo_16_0_noise02": {"gamma": 16.0, "mu": 0.0,
                           "commit_noise": 0.2},
}


def main() -> dict:
    print("=== exp105: the torus's rising price ===\n")

    out: dict[str, dict] = {}
    for arm, cfg in ARMS.items():
        for r in (10, 14, 20, 28):
            adj = torus(r, r)
            n = adj.shape[0]
            res = [execute_two_source_n(MULTI, adj, s, op=cfg,
                                        frontier_mode="walk",
                                        commit_noise=cfg["commit_noise"])
                   for s in SEEDS3]
            out[f"{arm}_n{n}"] = {
                "rate": round(float(np.mean(
                    [x["program_verified"] for x in res])), 3),
                "err": round(float(np.mean(
                    [x["err_vs_target"] for x in res])), 2)}
            print(f"    {arm:20s} n={n:4d}  rate "
                  f"{out[f'{arm}_n{n}']['rate']:.2f}  "
                  f"err {out[f'{arm}_n{n}']['err']}")

    deltas = {}
    for arm in ARMS:
        errs = [out[f"{arm}_n{n}"]["err"] for n in SIZES]
        deltas[arm] = round(errs[-1] - errs[0], 2)
    flatteners = [a for a, d in deltas.items() if d <= 0.3]
    tp_g1 = len(flatteners) >= 1
    tp_g2 = all(out[k]["rate"] >= 2 / 3 for k in out)
    noise_base = out["noise02_4_0_n100"]["err"]
    tp_g3 = abs(noise_base - 3.82) <= 0.5

    print(f"\n  trend deltas (n=784 minus n=100; base +{BASE_DELTA}):"
          f" {deltas}")
    print(f"  flatteners: {flatteners or 'NONE — a third mechanism'}")
    print(f"\n  TP-G1 the mechanism named: "
          f"{'PASS' if tp_g1 else 'REFUTED'}")
    print(f"  TP-G2 probe validity: {'PASS' if tp_g2 else 'REFUTED'}")
    print(f"  TP-G3 noise sanity (base {noise_base} vs 3.82): "
          f"{'PASS' if tp_g3 else 'REFUTED'}")

    npass = sum([tp_g1, tp_g2, tp_g3])
    print(f"\n  === {npass}/3 gates PASS ===")

    result = {
        "exp": "exp105_torus_rising_price",
        "arms": out,
        "trend_deltas": deltas,
        "flatteners": flatteners,
        "criteria": {
            "TP_G1_mechanism_named": bool(tp_g1),
            "TP_G2_probe_validity": bool(tp_g2),
            "TP_G3_noise_sanity": bool(tp_g3),
        },
        "notes": (
            "The torus's two-dial price rises with size (exp104: "
            "+1.04 mV from n=100 to 784). The probe arms: stronger "
            "gamma (16, 0), reduced walk commitment noise (0.2), "
            "and the combo. Whichever flattens the trend names the "
            "mechanism (pinning vs commitment-noise compounding)."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
