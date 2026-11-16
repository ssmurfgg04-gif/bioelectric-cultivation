"""exp454 — PRIMARY P4: does aging lose information beyond added noise?

Gates frozen in docs/PRIMARIES_ROUND2.md (commit 6d2231c) before this ran.
Re-implements the exp5 MI pipeline with sigma and g set independently.
Run: python -m experiments.exp454_p4_information_loss
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.information.mutual_info import estimate_mi_joint
from experiments.exp5_information import N, TARGETS, features, outcome_class

SEEDS = list(range(500, 520))
N_SAMPLES = 360


def sigma_of(a): return 3.0 + 25.0 * a
def g_of(a): return 0.2 * (1.0 - 0.9 * a)


def mi(sigma: float, g: float, seed: int) -> float:
    rng = np.random.default_rng(seed)
    X, y = [], []
    for i in range(N_SAMPLES):
        target = TARGETS[["wt", "twohead", "midcorrupt"][i % 3]]
        c = BioElectricCollective(n=N, seed=int(rng.integers(1 << 30)),
                                  noise_std=sigma, g_gap=g)
        c.set_target(target)
        c.set_state(target + rng.normal(0, sigma, N))
        c.run(2, dt=0.1)
        Vm = c.V.copy()
        c.run(13, dt=0.1)
        X.append(features(Vm)); y.append(outcome_class(c.V))
    return float(estimate_mi_joint(np.array(X), np.array(y), bins=4))


def _job(seed):
    young = mi(sigma_of(0), g_of(0), seed)
    full = mi(sigma_of(1), g_of(1), seed)
    noise = mi(sigma_of(1), g_of(0), seed)
    gj = mi(sigma_of(0), g_of(1), seed)
    return seed, young, full, noise, gj


def _ci(x, rng, n=10000):
    m = x[rng.integers(0, len(x), (n, len(x)))].mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main() -> dict:
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, SEEDS))
    a = np.array(rows)[:, 1:]
    young, full, noise, gj = a.T
    d_full, d_noise, d_gj = young - full, young - noise, young - gj
    extra = d_full - d_noise
    rng = np.random.default_rng(454)
    ci_extra, ci_full = _ci(extra, rng), _ci(d_full, rng)
    flips = rng.choice([-1.0, 1.0], (10000, len(extra)))
    p = float((((flips * extra).mean(axis=1) >= extra.mean()).sum() + 1) / 10001)
    g = {"G4a": bool(ci_extra[0] > 0), "G4b": bool(ci_full[0] > 0)}
    res = {"primary": "P4", "rows": [list(r) for r in rows],
           "mean_MI": {"young": float(young.mean()), "full": float(full.mean()),
                       "noise_only": float(noise.mean()), "gj_only": float(gj.mean())},
           "drop_full_ci95": ci_full, "drop_noise_ci95": _ci(d_noise, rng),
           "drop_gj_ci95": _ci(d_gj, rng),
           "extra_drop_mean": float(extra.mean()), "extra_drop_ci95": ci_extra,
           "gates": g, "p_value": p, "PASS": all(g.values())}
    for k, v in res["mean_MI"].items():
        print(f"MI {k:10s} {v:.3f} bits")
    print(f"drop full {d_full.mean():.3f} CI {ci_full} | noise-only {d_noise.mean():.3f} "
          f"| GJ-only {d_gj.mean():.3f}")
    print(f"extra (full - noise) {extra.mean():.3f} CI {ci_extra}")
    print(f"G4a {'PASS' if g['G4a'] else 'FAIL'} | G4b {'PASS' if g['G4b'] else 'FAIL'} | "
          f"p={p:.3g} -> P4 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp454_p4_information_loss.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
