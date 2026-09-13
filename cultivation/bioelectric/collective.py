"""Gap-junction-coupled bioelectric cell collective with homeostatic target memory.

Physics
-------
Each cell i maintains a membrane voltage V_i (mV, typically -70..-10 in
non-neural tissue). Cells are electrically coupled through gap junctions of
conductance G_ij (direct cytoplasmic continuity — the same electrical
synapse machinery neurons use). The dynamics:

    dV_i/dt     = gamma * (theta_i - V_i) + sum_j G_ij (V_j - V_i) + eta_i(t)

theta_i is the slow *homeostatic target*: the intrinsic resting state the
cell's channel expression re-converges toward (real cells do adjust their
resting potential over hours via ion-channel transcription — this is the
mechanism behind Levin-lab stable reprogramming results). Its dynamics:

    dtheta_i/dt = eps  * (V_i - theta_i)          # homeostatic plasticity
                + mu   * sum_j A_ij (theta_j - theta_i)   # pattern propagation
                + xi_i(t)                          # slow drift (aging)

Two regimes of one mechanism: a 24h forced depolarization rewrites theta
(reprogramming / the two-headed planarian memory), while unforced noise makes
theta random-walk (aging drift). The morphological target is an attractor of
this coupled system, exactly as in the Levin-group modeling literature
(Pietak & Levin 2017, Cervera et al. 2019, Grodstein & Levin 2021).
"""

from __future__ import annotations

import numpy as np


def line_adjacency(n: int, k: int = 1, ring: bool = False) -> np.ndarray:
    """Binary adjacency of a 1D chain (k neighbors each side), optionally ring."""
    A = np.zeros((n, n))
    for d in range(1, k + 1):
        A += np.diag(np.ones(n - d), d) + np.diag(np.ones(n - d), -d)
    if ring and n > 2 * k:
        A[0, n - 1] = A[n - 1, 0] = 1.0
    return A


class BioElectricCollective:
    """A 1D bioelectric cell collective (anatomical axis). Vectorized in numpy."""

    def __init__(
        self,
        n: int = 100,
        gamma: float = 0.25,
        g_gap: float = 0.20,
        eps: float = 0.04,
        mu_theta: float = 0.015,
        noise_std: float = 0.30,
        theta_drift: float = 0.0,
        adjacency: np.ndarray | None = None,
        seed: int | None = 0,
    ):
        self.n = n
        self.gamma = gamma  # intrinsic relaxation rate toward theta
        self.eps = eps  # homeostatic plasticity rate of theta
        self.mu = mu_theta  # theta diffusion (pattern propagation) rate
        self.noise_std = noise_std
        self.theta_drift = theta_drift

        self.rng = np.random.default_rng(seed)
        self.A = adjacency if adjacency is not None else line_adjacency(n)
        self.G = 0.0 + self.A * g_gap  # working conductance matrix
        self.G0 = self.G.copy()  # youthful reference
        self.gap_scale = 1.0  # global gap-junction health multiplier
        self.deg = (self.A * g_gap).sum(axis=1)

        self.theta = np.full(n, -50.0)
        self.V = self.theta + self.rng.normal(0.0, 2.0, n)

        # clamps: cell index -> voltage (interventions applied each step)
        self.clamps: dict[int, float] = {}
        # theta drivers: (region_indices, target_voltage, rate, voltage_gate)
        # A driver pulls theta toward target at `rate`, but ONLY where the
        # cell's voltage is above voltage_gate (depolarization-gated). This
        # is the oncogene model: tumoral growth signaling is permissive in
        # depolarized tissue (Chernet & Levin 2015) and is silenced by
        # hyperpolarization — which is why restoring Vmem can normalize
        # oncogene-expressing cells.
        self.theta_drivers: list[tuple[np.ndarray, float, float, float]] = []

    # ------------------------------------------------------------------ state
    def set_target(self, theta: np.ndarray) -> None:
        self.theta = np.asarray(theta, dtype=float).copy()

    def set_state(self, V: np.ndarray) -> None:
        self.V = np.asarray(V, dtype=float).copy()

    def clone_state(self) -> tuple[np.ndarray, np.ndarray]:
        return self.V.copy(), self.theta.copy()

    def restore_state(self, state: tuple[np.ndarray, np.ndarray]) -> None:
        self.V, self.theta = state[0].copy(), state[1].copy()

    # ------------------------------------------------------------ interventions
    def clamp(self, region: slice | np.ndarray, voltage: float) -> None:
        """Hold a region's voltage (drug / electrode / optogenetic forcing)."""
        idx = np.arange(self.n)[region] if isinstance(region, slice) else np.asarray(region)
        for i in idx:
            self.clamps[int(i)] = voltage

    def release_clamps(self) -> None:
        self.clamps.clear()

    def block_gap_junctions(self, scale: float) -> None:
        """Scale all gap-junction conductances (heptanol/octanol-like blockade)."""
        self.gap_scale = float(scale)
        self.G = self.G0 * scale
        self.deg = self.G.sum(axis=1)

    def restore_gap_junctions(self, scale: float = 1.0) -> None:
        self.block_gap_junctions(scale)

    def scale_gap_junctions(self, factor: float) -> None:
        self.block_gap_junctions(self.gap_scale * factor)

    def amputate(self, region: slice, wound_voltage: float = -30.0,
                 blastema_theta: float = -40.0) -> None:
        """Remove structure: cells reset to wound state, pattern re-derives."""
        self.V[region] = wound_voltage
        self.theta[region] = blastema_theta

    def regrow(self, region: slice, cell_period: float = 0.8, dt: float = 0.1,
               noise: float = 0.6) -> None:
        """Regeneration: the blastema EXTENDS THE STORED PATTERN outward from
        the wound boundary, one committing cell at a time (tissue-growth
        abstraction of neoblast-driven regrowth). Each new cell inherits the
        identity of the last committed cell — so what regrows is whatever the
        remaining tissue REMEMBERS. This is the mechanism that makes
        reprogramming memory empirically testable (Durant et al. 2017)."""
        idx = list(np.arange(self.n)[region])
        if not idx:
            return
        boundary = idx[0] - 1
        src = boundary if boundary >= 0 else idx[0]
        steps_per_cell = max(1, int(round(cell_period / dt)))
        for i in idx:
            for _ in range(steps_per_cell):
                self.step(dt)
            self.theta[i] = self.theta[src] + self.rng.normal(0.0, noise)
            self.V[i] = self.theta[i]
            src = i

    def corrupt_region(self, region: slice, theta_value: float,
                       V_value: float | None = None) -> None:
        """Force a region into an arbitrary bioelectric state (pathology)."""
        self.theta[region] = theta_value
        if V_value is not None:
            self.V[region] = V_value

    # ------------------------------------------------------------------ steps
    def step(self, dt: float = 0.1) -> None:
        """One Euler-Maruyama step of the coupled dynamics."""
        coupling = self.G @ self.V - self.V * self.deg
        dV = self.gamma * (self.theta - self.V) + coupling
        noise = self.noise_std * np.sqrt(dt) * self.rng.standard_normal(self.n)
        Vn = self.V + dt * dV + noise

        lap_theta = self.A @ self.theta - self.theta * self.A.sum(axis=1)
        dtheta = self.eps * (self.V - self.theta) + self.mu * lap_theta

        # oncogene-like drivers (voltage-gated theta pulls)
        for idx, target, rate, vgate in self.theta_drivers:
            active = idx[self.V[idx] > vgate]
            if len(active):
                dtheta[active] += rate * (target - self.theta[active])

        drift = self.theta_drift * np.sqrt(dt) * self.rng.standard_normal(self.n)
        self.theta = self.theta + dt * dtheta + drift
        self.V = Vn

        if self.clamps:
            idx = np.fromiter(self.clamps.keys(), dtype=int)
            vals = np.fromiter(self.clamps.values(), dtype=float)
            self.V[idx] = vals
            # clamped cells' plasticity sees the forced voltage
            self.theta[idx] += dt * self.eps * (vals - self.theta[idx])

    def run(self, duration: float, dt: float = 0.1, record_every: int = 0) -> np.ndarray | None:
        """Integrate for `duration` time units. Optionally record trajectories."""
        steps = int(round(duration / dt))
        if record_every > 0:
            n_rec = steps // record_every + 1
            rec = np.empty((n_rec, self.n))
            k = 0
            for t in range(steps):
                self.step(dt)
                if t % record_every == 0 and k < n_rec:
                    rec[k] = self.V
                    k += 1
            return rec
        for _ in range(steps):
            self.step(dt)
        return None

    # ----------------------------------------------------------------- metrics
    def pattern_error(self, target: np.ndarray) -> float:
        """RMS deviation of the voltage pattern from a target pattern (mV)."""
        return float(np.sqrt(np.mean((self.V - target) ** 2)))

    def target_drift(self, theta0: np.ndarray) -> float:
        """RMS drift of the stored target memory from its original value."""
        return float(np.sqrt(np.mean((self.theta - theta0) ** 2)))
