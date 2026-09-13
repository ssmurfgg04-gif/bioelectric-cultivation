"""Gaussian belief propagation on the gap-junction graph.

Gap-junction-coupled cell collectives are literally running loopy Gaussian
belief propagation: each cell averages its neighbors' states weighted by
conductance, iteratively, converging toward the collective consensus (the
local optimum of a smoothness + fidelity objective). This module is the
explicit decoder form of that computation — used to denoise observed
voltage patterns before RS decoding (the bioelectric analogue of
helix-codec's consensus layer).

Objective: minimize  sum_i m_i (x_i - y_i)^2 / (2 s_n^2) + sum_ij a_ij (x_i - x_j)^2
Jacobi / BP iterations converge to the exact solution on trees, and to a
good approximation on loopy (lattice-like) graphs.
"""

from __future__ import annotations

import numpy as np


def bp_smooth(y: np.ndarray, A: np.ndarray, observed: np.ndarray,
              noise_var: float = 4.0, iters: int = 25) -> np.ndarray:
    """Denoise/complete a voltage pattern using the coupling graph.

    y: (..., n) observed voltages (values at unobserved positions ignored)
    A: (n, n) structural adjacency (conductance weights)
    observed: boolean mask of which positions carry measurements
    Returns x: (..., n) the smoothed/completed pattern.

    Missing cells are reconstructed from neighbors — the bioelectric
    analogue of consensus recovery from redundant reads.
    """
    y = np.asarray(y, dtype=float)
    A = np.asarray(A, dtype=float)
    deg = A.sum(axis=1)  # (n,)
    lam = 1.0 / noise_var  # observation precision

    x = np.where(observed, y, np.broadcast_to((y * observed).sum(-1, keepdims=True)
                                              / np.maximum(observed.sum(-1, keepdims=True), 1),
                                              y.shape))
    w = np.broadcast_to(lam * observed.astype(float), y.shape)  # per-unit weight
    denom = w + deg  # (..., n) + (n,) broadcast
    for _ in range(iters):
        neighbor_sum = np.einsum("...j,ij->...i", x, A)
        x = (w * np.where(observed, y, 0.0) + neighbor_sum) / np.maximum(denom, 1e-9)
    return x


def bp_mse(x_est: np.ndarray, x_true: np.ndarray) -> float:
    return float(np.mean((x_est - x_true) ** 2))
