"""EXP7 — Sharded stress sweep over the aging-parameter space.

Grid: lambda_gap x kappa_noise x h_sys x seeds x {none, codec}.
Each run: a full aging cohort with maintenance, recording median lifespan,
Gompertz fit, and maintenance gain. Designed to be SHARDED:

    python -m experiments.exp7_stress --shard 3/24 --out results/sweep/shard_3.json

Runners execute one shard each (24 shards via GitHub Actions matrix);
aggregate.py merges the shards into the landscape figures.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingCohort, AgingParams, hazard_and_fits
from cultivation.coding.cultivation_codec import CultivationCodec
from experiments.exp6_error_correction import age_preset
from experiments.viz import dump_json

LAMBDAS = [0.02, 0.03, 0.04]
KAPPAS = [0.03, 0.05, 0.07]
HSYS = [0.07, 0.10, 0.13]
SEEDS = [0, 1, 2]
CONDS = ["none", "codec"]
CHECKUP = 5.0
FROM_AGE = 30.0


def make_grid() -> list[dict]:
    grid = []
    for lam in LAMBDAS:
        for kap in KAPPAS:
            for h in HSYS:
                for seed in SEEDS:
                    for cond in CONDS:
                        grid.append({"lambda_gap": lam, "kappa_noise": kap,
                                     "h_sys": h, "seed": seed, "cond": cond})
    return grid


def run_one(cfg: dict, K: int = 150, years: float = 130.0) -> dict:
    codec = CultivationCodec(12, 8, 60, budget_per_cycle=4)
    params = AgingParams(n_cells=60, lambda_gap=cfg["lambda_gap"],
                         kappa_noise=cfg["kappa_noise"], h_sys=cfg["h_sys"])
    ch = AgingCohort(K=K, params=params, seed=cfg["seed"])

    def maintain(t, cohort):
        if t < FROM_AGE or abs((t - FROM_AGE) % CHECKUP) > 0.26:
            return
        if cfg["cond"] != "codec":
            return
        codec.maintain(cohort, age_preset(t), mode="codec")

    s = ch.run(years=years, dt=0.25, intervention=maintain)
    ages = np.array(s["death_ages"])
    adult = ages[(ages >= 35) & (ages <= 100)].copy()
    adult[adult == np.inf] = 100.0
    fits = hazard_and_fits(adult, years=100)
    g = fits["fits"]["gompertz"]
    return {
        **cfg,
        "median": s["median_lifespan"],
        "max": s["max_lifespan"],
        "survivors": s["survivors_at_end"],
        "best_model": fits["best"],
        "beta_adult": float(np.exp(g["params"][1])),
        "gompertz_aic_gap": float(
            g["aic"] - min(v["aic"] for v in fits["fits"].values())),
        "cells_restored": codec.restored_cells,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", default="0/1", help="i/N shard selector")
    ap.add_argument("--out", default="results/sweep/shard_0.json")
    ap.add_argument("--K", type=int, default=150)
    ap.add_argument("--years", type=float, default=130.0)
    args = ap.parse_args()

    i, n = (int(x) for x in args.shard.split("/"))
    grid = make_grid()
    mine = [g for idx, g in enumerate(grid) if idx % n == i]
    print(f"[exp7] shard {i}/{n}: {len(mine)} of {len(grid)} runs")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    import json as _json
    results = []
    for k, cfg in enumerate(mine):
        r = run_one(cfg, K=args.K, years=args.years)
        results.append(r)
        print(f"  [{k+1}/{len(mine)}] lam={cfg['lambda_gap']} kap={cfg['kappa_noise']} "
              f"h={cfg['h_sys']} seed={cfg['seed']} {cfg['cond']:5s} "
              f"median={r['median']:.1f} beta={r['beta_adult']:.3f} best={r['best_model']}")
        with open(args.out, "w") as f:  # incremental flush to the requested path
            _json.dump({"shard": args.shard, "results": results}, f, indent=2)
    with open(args.out, "w") as f:
        _json.dump({"shard": args.shard, "results": results}, f, indent=2)
    print(f"[exp7] wrote {args.out}")


if __name__ == "__main__":
    main()
