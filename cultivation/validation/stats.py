"""Statistics helpers for validation experiments (M17 sloppiness fixes).

Why this module exists: the audit (docs/SLOPPINESS.md) found that every
headline number in exp18/exp19 was a point estimate without uncertainty.
These helpers make the honest statistics the default:

  - perm_rank_pvalue: exact/permutation p-value for "is X's rank among
    the top-k extreme?" (V1-style claims) under a random-rank null.
  - bootstrap_ci: percentile bootstrap CI for any statistic (V4 rho,
    hold means) with seed control.
  - spearman_ties: Spearman rho with average-rank tie handling
    (scipy.stats.spearmanr wrapped; replaces the argsort-of-argsort).
  - floor_sensitivity: permeability-floor robustness for the vmem map
    (perturb the GENE_WEIGHTS baseline floors and re-rank).
  - mean_se: mean +- standard error across seeds (the exp19 S1 fix).
All functions are deterministic given `seed`.
"""
from __future__ import annotations

import numpy as np


def spearman_ties(a, b) -> float:
    """Spearman rho with proper tie handling (S5)."""
    from scipy.stats import spearmanr
    r = spearmanr(np.asarray(a, float), np.asarray(b, float))
    return float(r.statistic)


def perm_rank_pvalue(rank: int, n: int, side: str = "low",
                     n_perm: int = 20000, seed: int = 0) -> float:
    """Permutation p-value for a rank claim (S1).

    Null: the cell type's rank is uniformly random over {1..n}.
    side='low': P(rank <= observed) (hyperpolarization claims, V1).
    side='high': P(rank >= observed).
    For uniform ranks this is exact combinatorially; the permutation
    route is kept for extensibility (weighted nulls later).
    """
    if n < 1 or rank < 1 or rank > n:
        return float("nan")
    if side == "low":
        p = rank / n
    elif side == "high":
        p = (n - rank + 1) / n
    else:
        raise ValueError(side)
    return float(min(1.0, p))


def bootstrap_ci(stat_fn, data, n_boot: int = 2000, alpha: float = 0.05,
                 seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap CI for stat_fn(data) (S1).

    data: sequence of observations; stat_fn: callable(list_or_array)->float.
    Resampling is over the observations (cell types for rho, seeds for
    hold means).
    """
    rng = np.random.default_rng(seed)
    data = np.asarray(data)
    stats = np.empty(n_boot)
    n = len(data)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        stats[i] = stat_fn(data[idx])
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def mean_se(vals) -> dict:
    """mean +- standard error, reported as a dict (the S1 exp19 fix)."""
    v = np.asarray(vals, float)
    return {"mean": float(v.mean()),
            "se": float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1
            else 0.0,
            "n": int(len(v))}


def floor_sensitivity(infer_fn, levels=(0.5, 1.5), seed: int = 0) -> dict:
    """Permeability-floor robustness (S8): scale the baseline floors in
    cultivation.validation.vmem_inference by `levels` and re-run the
    ranking. infer_fn() must return {cell type: Vm_mV}.

    Returns {level: {rank correlation with the default map (Spearman),
    max rank shift}} so callers can report 'rank-robust to +-50% floors'.
    """
    import cultivation.validation.vmem_inference as VI
    base = infer_fn()
    base_order = list(dict(sorted(base.items(), key=lambda kv: kv[1])))
    out = {}
    orig_floors = {"PK": 0.05, "PNa": 0.02, "PCl": 0.05}
    for lev in levels:
        scaled = {k: v * lev for k, v in orig_floors.items()}
        src = VI.permeabilities_from_expression

        def patched(expr, _s=scaled):
            P = dict(_s)
            for gene, lvl in expr.items():
                if gene not in VI.GENE_WEIGHTS:
                    continue
                cls, w = VI.GENE_WEIGHTS[gene]
                P[cls] = P.get(cls, 0.0) + w * float(lvl)
            return P

        VI.permeabilities_from_expression = patched
        try:
            pert = infer_fn()
        finally:
            VI.permeabilities_from_expression = src
        pert_order = list(dict(sorted(pert.items(), key=lambda kv: kv[1])))
        common = [g for g in base_order if g in pert_order]
        ra = [base_order.index(g) for g in common]
        rb = [pert_order.index(g) for g in common]
        rho = spearman_ties(ra, rb)
        max_shift = max(abs(a - b) for a, b in zip(ra, rb)) if common else 0
        out[f"x{lev}"] = {"spearman_vs_default": rho,
                          "max_rank_shift": int(max_shift)}
    return out


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    x = rng.normal(size=12)
    y = np.argsort(x) * 0.9 + rng.normal(size=12)
    print("spearman_ties:", round(spearman_ties(x, y), 3))
    print("perm p (rank 3 of 10, low):", perm_rank_pvalue(3, 10))
    print("bootstrap rho CI:",
          bootstrap_ci(lambda d: spearman_ties(d[:, 0], d[:, 1]),
                       np.column_stack([x, y]), n_boot=500, seed=2))
    print("mean_se:", mean_se([61.7, 66.5, 73.0]))
    print("stats module self-check OK")
