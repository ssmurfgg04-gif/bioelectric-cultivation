"""Cross-entropy-method search: the inverse problem solver.

Given a forward simulator whose outcome depends on an intervention vector
u (which cells to clamp, to what voltage, for how long), find the u that
minimizes the outcome error. Derivative-free, population-based, robust on
the low-dimensional intervention spaces that matter biologically — the
computational equivalent of searching for the cultivation technique.
"""

from __future__ import annotations

import numpy as np


def cem_optimize(fitness, bounds: list[tuple[float, float]], pop: int = 50,
                 elite_frac: float = 0.2, iters: int = 12,
                 seed: int = 0, verbose: bool = False):
    """Minimize fitness(u) over the box bounds. Returns (best_u, best_f, history)."""
    rng = np.random.default_rng(seed)
    d = len(bounds)
    lo = np.array([b[0] for b in bounds], float)
    hi = np.array([b[1] for b in bounds], float)
    mu = (lo + hi) / 2
    sigma = (hi - lo) / 4
    n_elite = max(2, int(pop * elite_frac))
    best_u, best_f = None, np.inf
    history = []
    for it in range(iters):
        U = rng.normal(mu, np.maximum(sigma, 1e-6), size=(pop, d))
        U = np.clip(U, lo, hi)
        F = np.array([fitness(u) for u in U])
        order = np.argsort(F)
        if F[order[0]] < best_f:
            best_f = float(F[order[0]])
            best_u = U[order[0]].copy()
        elite = U[order[:n_elite]]
        mu = elite.mean(axis=0)
        sigma = elite.std(axis=0) + (hi - lo) * 0.02
        history.append((it, best_f, mu.copy()))
        if verbose:
            print(f"  cem[{it}] best={best_f:.4f} mu={np.round(mu, 2)}")
    return best_u, best_f, history
