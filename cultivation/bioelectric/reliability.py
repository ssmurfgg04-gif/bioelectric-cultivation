"""Reliability-theory aging model (Gavrilov & Gavrilova 2001), vectorised.

Structure: an organism is `n_blocks` vital blocks in SERIES (any block
failing = death). Each block holds redundant elements in PARALLEL. At
birth each block starts with a Poisson(lam) number of functional
elements (developmental defects = high initial damage load). Elements
fail independently at rate k per year. Death occurs when any block has
zero functional elements, or from extrinsic hazard mu_ext.

Why this exists (round 7): the bioelectric AgingCohort produces a
Gompertz-shaped hazard but no parameter controls its slope (exp447,
P3, P3'), because death there is a single stochastic onset. In the
reliability model the Gompertz slope is set by the element failure rate
k (analytically beta ~ k for highly damaged initial states), and the
hazard decelerates to a late-life plateau ~ n_blocks*k as surviving
blocks are each down to their last element.

Repair (round 7, P12): restores failed elements toward each block's
initial count with completeness c. Each repair event adds a permanent
hazard increment `harm` (e.g. oncogenic risk of reprogramming).

State is an integer array (K, n_blocks); one step is a binomial thinning,
so a 10k-individual, 300-yr cohort runs in well under a second.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class ReliabilityParams:
    n_blocks: int = 8
    lam: float = 6.0       # mean initial functional elements per block
    k: float = 0.085       # 1/yr element failure rate
    mu_ext: float = 0.0    # 1/yr extrinsic (age-independent) hazard
    harm: float = 0.0      # 1/yr permanent hazard added per repair event
    k_cv: float = 0.0      # gamma-frailty CV of the per-individual failure rate

    def with_updates(self, **kw) -> "ReliabilityParams":
        return replace(self, **kw)


def simulate(p: ReliabilityParams, K: int, years: float, seed: int,
             dt: float = 0.25, repair_every: float | None = None,
             repair_c: float = 1.0, repair_start: float = 48.0) -> np.ndarray:
    """Return death ages (np.inf = alive at end)."""
    rng = np.random.default_rng(seed)
    init = rng.poisson(p.lam, size=(K, p.n_blocks))
    cur = init.copy()
    death = np.full(K, np.inf)
    alive = (cur > 0).all(axis=1)
    death[~alive] = 0.0
    extra = np.zeros(K)
    if p.k_cv > 0:
        ki = p.k * rng.gamma(1.0 / p.k_cv ** 2, p.k_cv ** 2, size=K)
    else:
        ki = np.full(K, p.k)
    q = 1.0 - np.exp(-ki * dt)
    steps = int(round(years / dt))
    next_rep = repair_start
    for i in range(1, steps + 1):
        t = i * dt
        idx = np.where(alive)[0]
        if idx.size == 0:
            break
        cur[idx] -= rng.binomial(cur[idx], q[idx][:, None])
        dead_blk = (cur[idx] == 0).any(axis=1)
        haz = p.mu_ext + extra[idx]
        dead_ext = rng.random(idx.size) < 1.0 - np.exp(-haz * dt)
        d = idx[dead_blk | dead_ext]
        death[d] = t
        alive[d] = False
        if repair_every is not None and t >= next_rep - 1e-9:
            next_rep += repair_every
            a = np.where(alive)[0]
            if a.size:
                missing = np.maximum(init[a] - cur[a], 0)
                cur[a] += rng.binomial(missing, repair_c)
                extra[a] += p.harm
    return death


def gompertz_beta(death: np.ndarray, entry: float, end: float) -> float:
    from cultivation.bioelectric.aging import hazard_and_fits
    ad = death[death >= entry].copy()
    ad[ad > end] = np.inf
    fit = hazard_and_fits(ad, end, entry=entry)
    return float(np.exp(fit["fits"]["gompertz"]["params"][1])), fit


def late_hazard(death: np.ndarray, a0: float, a1: float) -> float:
    """Occurrence/exposure hazard on [a0, a1): deaths / person-years."""
    at = death[death >= a0]
    if at.size == 0:
        return float("nan")
    exposure = np.clip(np.minimum(at, a1) - a0, 0, None).sum()
    deaths = ((at >= a0) & (at < a1)).sum()
    return float(deaths / exposure) if exposure > 0 else float("nan")
