"""Real-coded genetic algorithm — the inverse-design BASELINE.

Hazan & Levin (2022) used genetic algorithms as 'a first step toward the
design of machine learning tools for improved bioelectric control of
growth and form'. The project's CEM (exp10) claims to be the NEXT step —
more sample-efficient on the same landscape. This module is the honest
benchmark: a standard, well-tuned real-coded GA (tournament selection,
BLX-alpha crossover, gaussian mutation, elitism) evaluated under the
identical fitness, bounds, and common-random-number seeds, at the same
evaluation budget, so the comparison measures the SEARCH ALGORITHM, not
the tuning effort.
"""
from __future__ import annotations

import os
import pickle

import numpy as np


def ga_optimize(fitness, bounds, pop: int = 28, gens: int = 10,
                seed: int = 0, tournament_k: int = 3, blx_alpha: float = 0.5,
                mut_prob: float = 0.2, mut_sigma_frac: float = 0.15,
                elite: int = 2, verbose: bool = False, pool=None,
                checkpoint: str | None = None):
    """Maximize -fitness... (same sign convention as cem_optimize: the
    callable returns a COST to MINIMIZE). Returns (best_u, best_f,
    history) where history[k] = {'gen': k, 'best': ..., 'mean': ...,
    'evals': cumulative evaluations so far}.

    checkpoint: pickle file updated after EVERY generation holding the
    full optimizer state (population, fitnesses, rng bit-generator
    state, best-so-far). If the process is killed mid-search, re-running
    with the same arguments resumes EXACTLY where it left off — required
    for sandboxed execution where wall-clock budget comes in slices.
    """
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in bounds], float)
    hi = np.array([b[1] for b in bounds], float)
    span = hi - lo

    def eval_batch(U):
        if pool is not None:
            return np.array(pool.map(fitness, [u for u in U]))
        return np.array([fitness(u) for u in U])

    # ---- exact resume from a checkpoint (population + rng state) ----
    gen0 = 0
    if checkpoint and os.path.exists(checkpoint):
        with open(checkpoint, "rb") as f:
            st = pickle.load(f)
        P, F, evals = st["P"], st["F"], st["evals"]
        best_u, best_f = st["best_u"], st["best_f"]
        history = st["history"]
        gen0 = st["gen"]
        rng.bit_generator.state = st["rng_state"]
        if verbose:
            print(f"  GA resume from gen {gen0} (evals {evals})", flush=True)
    else:
        P = rng.uniform(lo, hi, (pop, len(lo)))
        F = eval_batch(P)
        evals = pop
        best_i = int(np.argmin(F))
        best_u, best_f = P[best_i].copy(), float(F[best_i])
        history = [{"gen": 0, "best": best_f, "mean": float(F.mean()),
                    "evals": evals}]
        gen0 = 0
        if checkpoint:
            _dump_ckpt(checkpoint, P, F, evals, best_u, best_f, history,
                       0, rng)

    def tournament():
        idx = rng.integers(0, pop, tournament_k)
        return P[idx[np.argmin(F[idx])]].copy()

    for gen in range(gen0 + 1, gens + 1):
        children = []
        # elitism: carry the top-E unchanged
        for i in np.argsort(F)[:elite]:
            children.append(P[i].copy())
        while len(children) < pop:
            p1, p2 = tournament(), tournament()
            if rng.random() < 0.9:  # BLX-alpha crossover
                cmin = np.minimum(p1, p2)
                cmax = np.maximum(p1, p2)
                rng_ = blx_alpha * (cmax - cmin)
                child = rng.uniform(cmin - rng_, cmax + rng_)
            else:
                child = p1.copy()
            # gaussian mutation per gene
            m = rng.random(len(child)) < mut_prob
            child[m] += rng.normal(0.0, mut_sigma_frac * span[m])
            children.append(np.clip(child, lo, hi))
        P = np.array(children)
        F = eval_batch(P)
        evals += pop
        best_i = int(np.argmin(F))
        if F[best_i] < best_f:
            best_u, best_f = P[best_i].copy(), float(F[best_i])
        history.append({"gen": gen, "best": best_f,
                        "mean": float(F.mean()), "evals": evals})
        if checkpoint:
            _dump_ckpt(checkpoint, P, F, evals, best_u, best_f, history,
                       gen, rng)
        if verbose:
            print(f"  GA gen {gen}: best {best_f:.3f} mean {F.mean():.3f}",
                  flush=True)

    return best_u, best_f, history


def _dump_ckpt(path, P, F, evals, best_u, best_f, history, gen, rng):
    st = {"P": np.asarray(P), "F": np.asarray(F), "evals": int(evals),
          "best_u": np.asarray(best_u), "best_f": float(best_f),
          "history": history, "gen": int(gen),
          "rng_state": rng.bit_generator.state}
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(st, f)
    os.replace(tmp, path)  # atomic: never a torn checkpoint
