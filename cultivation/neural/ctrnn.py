"""Continuous-time recurrent neural network (the neural-side bioelectric sheet).

tau_i dV_i/dt = -V_i + sum_j W_ij tanh(V_j) + I_i + noise

Same mathematics as the non-neural collective (coupled ODEs with sigmoidal
nonlinearities), faster time constant — the "OS layer" of the body-software
stack. Used in exp5 to study how coherent drive (a crude computational stand-in
for meditative states) changes linearized integration Phi.
"""

from __future__ import annotations

import numpy as np
import networkx as nx


def make_small_world(n: int, k: int = 3, p: float = 0.3, w: float = 0.8,
                     seed: int = 0) -> np.ndarray:
    G = nx.watts_strogatz_graph(n, k, p, seed=seed)
    return nx.to_numpy_array(G) * w


class CTRNN:
    def __init__(self, W: np.ndarray, tau: float = 1.0, noise: float = 0.02,
                 seed: int = 0):
        self.W = np.asarray(W, float)
        self.n = self.W.shape[0]
        self.tau = tau
        self.noise = noise
        self.rng = np.random.default_rng(seed)
        self.V = self.rng.normal(0, 0.1, self.n)

    def set_state(self, V: np.ndarray) -> None:
        self.V = np.asarray(V, float).copy()

    def step(self, dt: float, I: np.ndarray | None = None) -> np.ndarray:
        I = np.zeros(self.n) if I is None else I
        dV = (-self.V + self.W @ np.tanh(self.V) + I) / self.tau
        self.V = self.V + dt * dV + self.noise * np.sqrt(dt) * self.rng.standard_normal(self.n)
        return self.V

    def run(self, duration: float, dt: float = 0.05,
            I: np.ndarray | None = None) -> np.ndarray:
        steps = int(duration / dt)
        for _ in range(steps):
            self.step(dt, I)
        return self.V

    def jacobian(self, V: np.ndarray | None = None) -> np.ndarray:
        """Jacobian of the continuous dynamics at state V."""
        V = self.V if V is None else V
        D = (1 - np.tanh(V) ** 2) / self.tau  # diagonal of d(activation)/dV
        return (-np.eye(self.n) + self.W * D[None, :]) / self.tau

    def coherent_drive(self, strength: float, subset: np.ndarray | None = None) -> np.ndarray:
        """A coherent input pattern (stand-in for an attention/meditation regime)."""
        I = np.zeros(self.n)
        idx = np.arange(self.n) if subset is None else subset
        I[idx] = strength
        return I
