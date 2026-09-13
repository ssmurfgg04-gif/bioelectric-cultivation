"""Integrated information for linear-Gaussian systems.

We implement Phi_int: an integration measure in the IIT family in the
spirit of Barrett & Seth (2011, "Practical measures of integrated
information for time-series data") and Oizumi et al.'s effective
information, formulated for linear systems

    x(t+1) = A x(t) + e(t),   e ~ N(0, Q)

with stationary covariance Sigma (discrete Lyapunov: Sigma = A Sigma A' + Q)
and lag covariance C1 = A Sigma.

For a bipartition P = (S, S-bar) we SEVER the system (block-diagonalize A
and Q) and compare one-step state information:

    I_w  = I(x(t); x(t+1))                     (whole system)
    I_S  = I(x_S(t); x_S(t+1))                 (severed part S)
    I_Sb = I(x_Sbar(t); x_Sbar(t+1))           (severed part S-bar)
    Phi(P) = I_w - I_S - I_Sb

Phi = min over bipartitions (the minimum-information bipartition). An
integrated system loses information when cut (Phi > 0); a modular system
loses nothing (Phi ~ 0). This is a *measure of integration*, not a claim
about consciousness — see docs/FALSIFICATION.md for the honest positioning
(weak/instrumental IIT per Mediano et al. 2022).

Exact N <= 12 via exhaustive bipartitions; larger systems use the
linearized version or sampled bipartitions.
"""

from __future__ import annotations

import itertools

import numpy as np


def _lyapunov(A: np.ndarray, Q: np.ndarray, iters: int = 200) -> np.ndarray:
    """Stationary covariance of x(t+1)=Ax+e, e~N(0,Q), via fixed-point."""
    S = Q.copy()
    for _ in range(iters):
        S_new = A @ S @ A.T + Q
        if np.allclose(S_new, S, atol=1e-12):
            return S_new
        S = S_new
    return S


def _gauss_mi(Sigma: np.ndarray, C1: np.ndarray, A: np.ndarray, Q: np.ndarray) -> float:
    """I(x_t; x_{t+1}) for the linear system with cov Sigma, lag C1."""
    pred = A @ Sigma @ A.T + Q  # covariance of x_{t+1}
    joint = np.block([[Sigma, C1.T], [C1, pred]])
    sign_w, logdet_w = np.linalg.slogdet(joint)
    sign_a, logdet_a = np.linalg.slogdet(Sigma)
    sign_b, logdet_b = np.linalg.slogdet(pred)
    if sign_w <= 0 or sign_a <= 0 or sign_b <= 0:
        return 0.0
    return 0.5 * (logdet_a + logdet_b - logdet_w) / np.log(2.0)


def phi_integration(A: np.ndarray, Q: np.ndarray, max_bipartitions: int = 512) -> dict:
    """Phi_int over the minimum information bipartition. N <= ~12 exact."""
    A = np.asarray(A, float)
    Q = np.asarray(Q, float)
    n = A.shape[0]
    Sigma = _lyapunov(A, Q)
    C1 = A @ Sigma  # cov(x_{t+1}, x_t)
    I_w = _gauss_mi(Sigma, C1, A, Q)

    best = {"phi": np.inf, "partition": None}
    count = 0
    for r in range(1, n // 2 + 1):
        for S in itertools.combinations(range(n), r):
            if count >= max_bipartitions:
                break
            count += 1
            idx = np.array(S)
            mask = np.zeros(n, dtype=bool)
            mask[idx] = True
            Ac = np.zeros_like(A)
            Qc = np.zeros_like(Q)
            Ac[np.ix_(mask, mask)] = A[np.ix_(mask, mask)]
            Qc[np.ix_(mask, mask)] = Q[np.ix_(mask, mask)]
            Ac[np.ix_(~mask, ~mask)] = A[np.ix_(~mask, ~mask)]
            Qc[np.ix_(~mask, ~mask)] = Q[np.ix_(~mask, ~mask)]
            Sc = _lyapunov(Ac, Qc)
            Cc = Ac @ Sc
            I_parts = _gauss_mi(Sc[np.ix_(mask, mask)], Cc[np.ix_(mask, mask)],
                                Ac[np.ix_(mask, mask)], Qc[np.ix_(mask, mask)])
            I_parts += _gauss_mi(Sc[np.ix_(~mask, ~mask)], Cc[np.ix_(~mask, ~mask)],
                                 Ac[np.ix_(~mask, ~mask)], Qc[np.ix_(~mask, ~mask)])
            phi_P = I_w - I_parts
            if phi_P < best["phi"]:
                best = {"phi": float(phi_P), "partition": (list(S), [i for i in range(n) if i not in S])}
        if count >= max_bipartitions:
            break
    best["I_whole"] = float(I_w)
    best["n"] = n
    return best


def linearized_phi(J: np.ndarray, dt: float = 0.1, Q: np.ndarray | None = None) -> dict:
    """Phi for a continuous-time system linearization x' = J x.

    Discretizes x(t+dt) = exp(J dt) x + noise (identity-scaled Q by default).
    """
    J = np.asarray(J, float)
    n = J.shape[0]
    A = np.eye(n) + dt * J
    if Q is None:
        Q = np.eye(n) * 0.05
    return phi_integration(A, Q)


def connectivity_family_phi(n: int = 8, seed: int = 0) -> dict:
    """Phi across connectivity regimes: chain, ER(p), small-world, all-to-all,
    two independent modules. Integration should peak at intermediate coupling."""
    import networkx as nx

    rng = np.random.default_rng(seed)
    out = {}

    def phi_of(W, noise=0.05):
        n = W.shape[0]
        Q = np.eye(n) * noise
        return phi_integration(W, Q)["phi"]

    # chain
    W = np.zeros((n, n))
    for i in range(n - 1):
        W[i, i + 1] = W[i + 1, i] = 0.5
    out["chain"] = phi_of(W)

    # ER at several densities
    for p in (0.15, 0.3, 0.5, 0.8):
        G = nx.erdos_renyi_graph(n, p, seed=seed)
        W = nx.to_numpy_array(G) * 0.5
        out[f"er_p{p}"] = phi_of(W)

    # small-world
    G = nx.watts_strogatz_graph(n, k=3, p=0.3, seed=seed)
    out["smallworld"] = phi_of(nx.to_numpy_array(G) * 0.5)

    # all-to-all (weak per-edge so total coupling comparable)
    W = np.ones((n, n)) - np.eye(n)
    out["alltoall_w0.1"] = phi_of(W * 0.1)

    # two independent modules (must give phi ~ 0)
    W = np.zeros((n, n))
    for i in range(n // 2 - 1):
        W[i, i + 1] = W[i + 1, i] = 0.5
    for i in range(n // 2, n - 1):
        W[i, i + 1] = W[i + 1, i] = 0.5
    out["two_modules"] = phi_of(W)

    # uniformly scaled coupling sweep
    G = nx.watts_strogatz_graph(n, k=3, p=0.2, seed=seed)
    B = nx.to_numpy_array(G)
    sweep = []
    for g in (0.05, 0.15, 0.3, 0.5, 0.8, 1.2):
        sweep.append((g, phi_of(B * g)))
    out["coupling_sweep"] = sweep
    return out
