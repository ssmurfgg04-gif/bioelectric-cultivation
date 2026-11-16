"""exp449 — PRIMARY P2: sustained vs dose-matched one-shot maintenance.

Gates frozen in docs/PRIMARIES.md (commit 6d64990) before this file ran.
Run: python -m experiments.exp449_p2_maintenance
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams

SEEDS = list(range(200, 220))
K, YEARS, DT = 400, 130.0, 0.25
N_APPS = 13                     # sustained applications at 48, 52, ..., 96
ONE_PULL = 1.0 - 0.9 ** N_APPS  # ~0.746
ONE_CLEAR = 3 * N_APPS          # 39


def _apply(cohort, pull, clear):
    for i in range(cohort.K):
        if not cohort.alive[i]:
            continue
        cohort.theta[i] += pull * (cohort.theta0 - cohort.theta[i])
        sen = np.where(cohort.senesced[i])[0]
        if len(sen):
            take = sen[:clear]
            cohort.senesced[i, take] = False
            cohort.theta[i, take] = cohort.theta0[take]
            cohort.V[i, take] = cohort.theta0[take]


def sustained(t, cohort):
    if t > 47 and abs((t - 48.0) % 4.0) < 0.26 and t < 100.5:
        _apply(cohort, 0.10, 3)


def one_shot(t, cohort):
    if abs(t - 48.0) < 0.126:
        _apply(cohort, ONE_PULL, ONE_CLEAR)


def _median(seed, interv):
    ch = AgingCohort(K=K, params=AgingParams(), seed=seed)
    return float(ch.run(years=YEARS, dt=DT, intervention=interv)["median_lifespan"])


def _job(seed):
    return seed, _median(seed, None), _median(seed, sustained), _median(seed, one_shot)


def _boot_ci(x, rng, n=10000):
    idx = rng.integers(0, len(x), (n, len(x)))
    m = x[idx].mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main() -> dict:
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, SEEDS))
    none = np.array([r[1] for r in rows]); sus = np.array([r[2] for r in rows])
    one = np.array([r[3] for r in rows])
    Rs, Ro = sus / none, one / none
    d = Rs - Ro
    rng = np.random.default_rng(449)
    ci_s, ci_d, ci_o = _boot_ci(Rs, rng), _boot_ci(d, rng), _boot_ci(Ro, rng)
    flips = rng.choice([-1.0, 1.0], (10000, len(d)))
    p = float((((flips * d).mean(axis=1) >= d.mean()).sum() + 1) / (len(flips) + 1))
    g = {"G2a": bool(ci_s[0] > 1.0), "G2b": bool(ci_d[0] > 0.0)}
    res = {"primary": "P2", "seeds": SEEDS, "median_none": none.tolist(),
           "median_sustained": sus.tolist(), "median_oneshot": one.tolist(),
           "R_s_mean": float(Rs.mean()), "R_s_ci95": ci_s,
           "R_o_mean": float(Ro.mean()), "R_o_ci95": ci_o,
           "diff_mean": float(d.mean()), "diff_ci95": ci_d,
           "gates": g, "p_value": p, "PASS": all(g.values())}
    print(f"R_sustained = {Rs.mean():.4f} CI {ci_s[0]:.4f}-{ci_s[1]:.4f}")
    print(f"R_oneshot   = {Ro.mean():.4f} CI {ci_o[0]:.4f}-{ci_o[1]:.4f}")
    print(f"R_s - R_o   = {d.mean():.4f} CI {ci_d[0]:.4f}-{ci_d[1]:.4f}")
    for k, v in g.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print(f"p = {p:.4g} -> P2 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp449_p2_maintenance.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
