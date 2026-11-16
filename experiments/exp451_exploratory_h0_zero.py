"""exp451 — EXPLORATORY (not a primary): P3 failed; does removing the
error-driven senescence term entirely (h0 = 0) let h_sys set beta?
Post-hoc follow-up to exp450, labelled exploratory per docs/PRIMARIES.md.
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy import stats

from cultivation.bioelectric.aging import AgingCohort, AgingParams, hazard_and_fits

HSYS = [0.05, 0.07, 0.10, 0.14, 0.20]
SEEDS = [300, 301, 302, 303]
K, ENTRY = 400, 35.0


def _job(args):
    h, seed = args
    base = AgingParams()
    p = base.with_updates(h0=0.0, h_sys=h)
    s = AgingCohort(K=K, params=p, seed=seed).run(years=130.0, dt=0.25)
    ages = np.asarray(s["death_ages"], float)
    end = 100.0
    adult = ages[ages >= ENTRY].copy()
    if np.sum(np.isfinite(adult) & (adult <= end)) < 30:
        end = 130.0
    adult[adult > end] = np.inf
    fit = hazard_and_fits(adult, end, entry=ENTRY)
    b = float(np.exp(fit["fits"]["gompertz"]["params"][1]))
    return h, seed, b, end, float(s["median_lifespan"]), int(np.isfinite(adult).sum())


def main() -> dict:
    jobs = [(h, s) for h in HSYS for s in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, jobs))
    x = np.log([r[0] for r in rows]); y = np.log([r[2] for r in rows])
    lr = stats.linregress(x, y)
    p = float(lr.pvalue / 2 if lr.slope > 0 else 1 - lr.pvalue / 2)
    ratios = {h: float(np.mean([r[2] for r in rows if r[0] == h]) / h) for h in HSYS}
    g = {"G3a": bool(lr.slope >= 0.5),
         "G3b": bool(all(0.5 <= v <= 1.5 for v in ratios.values()))}
    res = {"primary": "P3", "variant": "h0 = 0 (EXPLORATORY)", "rows": rows,
           "elasticity": float(lr.slope), "elasticity_se": float(lr.stderr),
           "beta_over_hsys": {str(k): v for k, v in ratios.items()},
           "gates": g, "p_value": p, "PASS": all(g.values())}
    for h in HSYS:
        bs = [r[2] for r in rows if r[0] == h]
        med = np.mean([r[4] for r in rows if r[0] == h])
        print(f"h_sys={h:.2f}  beta={np.mean(bs):.4f}  beta/h={ratios[h]:.2f}  median={med:.1f}")
    print(f"elasticity = {lr.slope:.3f} ± {lr.stderr:.3f}")
    for k, v in g.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print(f"p = {p:.3g} -> P3 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp451_exploratory_h0_zero.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
