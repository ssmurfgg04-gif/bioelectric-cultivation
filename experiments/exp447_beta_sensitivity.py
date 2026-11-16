"""exp447 — WHAT SETS THE GOMPERTZ SLOPE? (review fix C2 / Phase-2 sensitivity)

Motivation (external review, 2026-11-16): exp3 recorded C2 = False — the
fitted adult Gompertz slope beta does not track h_sys, the parameter the
code labelled "the Gompertz engine". The README nevertheless reported the
fitted beta (~0.09/yr) as landing in "the empirical human range". If no
mechanism parameter controls beta, that agreement is a coincidence of
calibration, not an emergent prediction.

PRE-REGISTERED QUESTION (written before the run, not edited after):
  One-at-a-time sensitivity: scale each aging parameter by
  {0.5, 0.71, 1, 1.41, 2} (log-symmetric), 3 seeds each, K=400, and fit
  beta on the adult window [35, 100] with the LEFT-TRUNCATION-CORRECTED
  likelihood (hazard_and_fits(entry=35)). Report the elasticity
      e_p = d ln(beta) / d ln(p)
  (OLS slope over the 5 levels, seed-averaged).

  Interpretation rule (fixed in advance):
   - |e_p| >= 0.5  -> p CONTROLS beta
   - 0.1 <= |e_p| < 0.5 -> p WEAKLY influences beta
   - |e_p| < 0.1   -> p is INERT for beta
  If every |e_p| < 0.5, the model has no parameter that sets the
  Gompertz rate, and the "human-range beta" claim is withdrawn.

Run: python -m experiments.exp447_beta_sensitivity [--quick]
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams, hazard_and_fits

PARAMS = ["h_sys", "soft", "margin", "h0", "kappa_noise", "lambda_gap",
          "mortality_k", "seed_rate", "sigma0"]
SCALES = [0.5, 2 ** -0.5, 1.0, 2 ** 0.5, 2.0]
ENTRY, END = 35.0, 100.0


def _beta(args):
    pname, scale, seed, K = args
    base = AgingParams()
    p = base.with_updates(**{pname: getattr(base, pname) * scale})
    ch = AgingCohort(K=K, params=p, seed=seed)
    s = ch.run(years=130.0, dt=0.25)
    ages = np.asarray(s["death_ages"], float)
    adult = ages[ages >= ENTRY].copy()
    adult[adult > END] = np.inf
    if np.isfinite(adult).sum() < 30:
        return pname, scale, seed, float("nan"), float(s["median_lifespan"])
    fit = hazard_and_fits(adult, END, entry=ENTRY)
    b = float(np.exp(fit["fits"]["gompertz"]["params"][1]))
    return pname, scale, seed, b, float(s["median_lifespan"])


def main(quick: bool = False) -> dict:
    seeds = [0] if quick else [0, 1, 2]
    K = 200 if quick else 400
    jobs = [(p, sc, sd, K) for p in PARAMS for sc in SCALES for sd in seeds]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_beta, jobs))

    out = {"design": {"params": PARAMS, "scales": SCALES, "seeds": seeds,
                      "K": K, "window": [ENTRY, END],
                      "fit": "Gompertz MLE, left-truncated at 35"},
           "elasticity": {}, "rows": rows}
    print(f"{'param':12s} {'elast':>7s}  verdict    beta@x0.5 -> beta@x2")
    for p in PARAMS:
        xs, ys, med = [], [], {}
        for sc in SCALES:
            bs = [r[3] for r in rows if r[0] == p and r[1] == sc and np.isfinite(r[3])]
            if bs:
                xs.append(np.log(sc)); ys.append(np.log(np.mean(bs)))
                med[sc] = float(np.mean(bs))
        e = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 3 else float("nan")
        v = ("CONTROLS" if abs(e) >= 0.5 else "WEAK" if abs(e) >= 0.1 else "INERT")
        out["elasticity"][p] = {"e": e, "verdict": v, "beta_by_scale": med}
        print(f"{p:12s} {e:7.3f}  {v:9s}  {med.get(0.5, float('nan')):.4f} -> "
              f"{med.get(2.0, float('nan')):.4f}")

    base_b = [r[3] for r in rows if r[1] == 1.0 and np.isfinite(r[3])]
    out["baseline_beta_mean"] = float(np.mean(base_b))
    out["baseline_beta_sd"] = float(np.std(base_b, ddof=1)) if len(base_b) > 1 else 0.0
    controllers = [p for p, d in out["elasticity"].items() if d["verdict"] == "CONTROLS"]
    out["controllers"] = controllers
    out["verdict"] = ("BETA HAS A CONTROLLING PARAMETER: " + ", ".join(controllers)
                      if controllers else
                      "NO PARAMETER CONTROLS BETA — human-range claim withdrawn")
    print(f"\nbaseline beta = {out['baseline_beta_mean']:.4f} "
          f"± {out['baseline_beta_sd']:.4f} (SD over all baseline runs)")
    print("VERDICT:", out["verdict"])
    if not quick:
        os.makedirs("results", exist_ok=True)
        with open("results/exp447_beta_sensitivity.json", "w") as f:
            json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    main(ap.parse_args().quick)
