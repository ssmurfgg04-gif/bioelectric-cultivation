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

# physiological bounds (Nernst/reversal limits) — see step()
V_PHYS_MIN = -85.0
V_PHYS_MAX = 5.0


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
        blastema_readout_noise: float = 18.0,
    ):
        self.n = n
        self.gamma = gamma  # intrinsic relaxation rate toward theta
        self.eps = eps  # homeostatic plasticity rate of theta
        self.mu = mu_theta  # theta diffusion (pattern propagation) rate
        self.noise_std = noise_std
        self.theta_drift = theta_drift
        # Spread (mV) of a blastema cell's identity guess when it cannot read
        # the pattern field through gap junctions (M25 coupling-dependent
        # readout; see regrow). Physiological range: a blind cell can land
        # anywhere on the head-trunk fate axis (~-20 to ~-50 mV).
        self.blastema_readout_noise = blastema_readout_noise

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
               noise: float = 0.6, direction: str = "forward",
               length_gradient: float = 0.0,
               commitment_noise_scale: float = 1.0) -> None:
        """Regeneration: the blastema EXTENDS THE STORED PATTERN outward from
        the wound boundary, one committing cell at a time (tissue-growth
        abstraction of neoblast-driven regrowth). Each new cell inherits the
        identity of the last committed cell — so what regrows is whatever the
        remaining tissue REMEMBERS. This is the mechanism that makes
        reprogramming memory empirically testable (Durant et al. 2017).

        `direction` names which wound face the chain extends from:
        "forward" (default, historical behavior — blastema grows tail-ward
        from the anterior boundary cell) or "backward" (head-ward from the
        posterior boundary cell — a head amputation's blastema reads the
        trunk boundary BEHIND it). At gap_scale == 1.0 and direction ==
        "forward" the mechanism is bit-exact with the pre-M25 chain.

        M26 ADDITIVE PARAMETERS (night three; each bit-exact at default):

        `length_gradient` g in [0,1] — INTRINSIC positional-information
        readout (M26a): a committing cell at distance d past the wound face
        blends chain inheritance with a linear EXTRAPOLATION of the stored
        theta trend measured over the intact tissue adjacent to the face
        (Wolpert-style positional cue; no external target knowledge). g=0
        keeps pure chain inheritance (bit-exact pre-M26 walk). Fixes the
        crosspiece length-gradient refutation (S2W2's cross_a overshoot:
        sim 1.00 vs recorded 0.52 — a pure chain cannot know how MUCH was
        removed; a gradient readout can).

        `commitment_noise_scale` — Vmem-gated blastema COMMITMENT (M26b):
        multiplies the per-cell identity noise. Ion-channel dysfunction
        (impaired homeostatic relaxation, noisy Vmem) degrades the
        commitment signal itself, not the stored pattern — recorded
        ion_channel experiments are as abnormal as junction loss (0.45 vs
        0.41) while the sim's stored pattern stays intact (0.00). The arm
        chooses the scale; default 1.0 is bit-exact.

        `direction="both"` (M26c) — TWO-FACE trunk regeneration: splits the
        region at the midpoint; the anterior half regenerates forward from
        the anterior face, the posterior half backward from the posterior
        face (two independent blastemas — mid-body removals in the record
        heal both faces, producing the two-headed / two-tailed phenotypes
        the one-face topology cannot reach).

        M25 COUPLING-DEPENDENT READOUT (exp27 S2P1 repair): the inheritance
        read itself runs THROUGH the gap-junction network. At full coupling
        the readout is exactly the stored chain (bit-exact with the previous
        mechanism — no extra RNG draws when gap_scale == 1.0). Under
        blockade the blastema cannot read the pattern field and each
        committing cell falls back to the wound-state default plus a broad
        guess along the fate axis (spread blastema_readout_noise) — the
        graded, mixed-outcome phenomenology PlanformDB records for innexin
        RNAi. Restore junctions before regrowth and the readout recovers
        (T1.1c / exp27 S2C control)."""
        idx = list(np.arange(self.n)[region])
        if not idx:
            return
        steps_per_cell = max(1, int(round(cell_period / dt)))
        r = float(self.gap_scale)  # junction health at regen onset
        wound_center = float(np.mean(self.theta[idx]))
        eff_noise = float(noise) * float(commitment_noise_scale)
        g = float(length_gradient)

        def face_slope(face: int, sign: int) -> tuple[float, float]:
            """Anchor (theta at the face) + per-cell theta trend measured on
            the intact side of the face (sign -1: anterior tissue, +1:
            posterior tissue). Deterministic — no RNG contact."""
            if sign < 0:
                lo, hi = max(0, face - 5), face  # intact cells face-5..face-1
            else:
                lo, hi = face + 1, min(self.n, face + 6)
            if hi - lo < 1 or (sign < 0 and face - 1 < 0) \
                    or (sign > 0 and face + 1 > self.n - 1):
                return float(self.theta[face if 0 <= face < self.n
                                        else (idx[0] if sign < 0 else idx[-1])]), 0.0
            vals = self.theta[lo:hi]
            slope = float((vals[-1] - vals[0]) / max(1, len(vals) - 1)) \
                if len(vals) > 1 else 0.0
            return float(self.theta[face]), slope

        def walk(order: list[int], src: int, sign: int) -> None:
            anchor, slope = face_slope(src, sign)
            d = 0
            for i in order:
                for _ in range(steps_per_cell):
                    self.step(dt)
                d += 1
                chain_base = self.theta[src]
                if g > 0.0:
                    chain_base = (1.0 - g) * chain_base \
                        + g * (anchor + slope * d)
                theta_new = chain_base + self.rng.normal(0.0, eff_noise)
                if r < 1.0:
                    guess = wound_center + self.rng.normal(
                        0.0, self.blastema_readout_noise)
                    theta_new = r * theta_new + (1.0 - r) * guess
                self.theta[i] = theta_new
                self.V[i] = theta_new
                src = i

        if direction == "forward":
            boundary = idx[0] - 1
            src = boundary if boundary >= 0 else idx[0]
            walk(idx, src, -1)
        elif direction == "backward":
            boundary = idx[-1] + 1
            src = boundary if boundary < self.n else idx[-1]
            walk(list(reversed(idx)), src, +1)
        elif direction == "both":
            h = len(idx) // 2
            fwd_b = idx[0] - 1
            fwd_src = fwd_b if fwd_b >= 0 else idx[0]
            walk(idx[:h], fwd_src, -1)
            bwd_b = idx[-1] + 1
            bwd_src = bwd_b if bwd_b < self.n else idx[-1]
            walk(list(reversed(idx[h:])), bwd_src, +1)
        else:
            raise ValueError(direction)

    def corrupt_region(self, region: slice, theta_value: float,
                       V_value: float | None = None) -> None:
        """Force a region into an arbitrary bioelectric state (pathology)."""
        self.theta[region] = theta_value
        if V_value is not None:
            self.V[region] = V_value

    # ------------------------------------------------------------------ steps
    def step(self, dt: float = 0.1) -> None:
        """One Euler-Maruyama step of the coupled dynamics.

        V and theta are held inside physiological bounds (Nernst/reversal-
        potential limits: no real membrane sustains |V| beyond ~100 mV).
        The bounds are INERT for every established experiment (exp1-11
        dynamics live well inside [-70, -10]); they only clip the
        pathological excursions a sustained artificial efferent (exp12's
        mind-body interface) can otherwise integrate without limit.
        """
        coupling = self.G @ self.V - self.V * self.deg
        dV = self.gamma * (self.theta - self.V) + coupling
        noise = self.noise_std * np.sqrt(dt) * self.rng.standard_normal(self.n)
        Vn = self.V + dt * dV + noise

        lap_theta = self.A @ self.theta - self.theta * self.A.sum(axis=1)
        # M25: pattern propagation is ALSO junction-carried — theta diffusion
        # scales with gap-junction health (bit-exact at gap_scale == 1.0).
        # With junctions down the stored pattern can no longer spread, so a
        # blind-regenerated region stays whatever the blastema guessed.
        dtheta = self.eps * (self.V - self.theta) \
            + self.mu * self.gap_scale * lap_theta

        # oncogene-like drivers (voltage-gated theta pulls)
        for idx, target, rate, vgate in self.theta_drivers:
            active = idx[self.V[idx] > vgate]
            if len(active):
                dtheta[active] += rate * (target - self.theta[active])

        drift = self.theta_drift * np.sqrt(dt) * self.rng.standard_normal(self.n)
        self.theta = np.clip(self.theta + dt * dtheta + drift,
                             V_PHYS_MIN, V_PHYS_MAX)
        self.V = np.clip(Vn, V_PHYS_MIN - 5.0, V_PHYS_MAX + 5.0)

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
            return rec[:k]  # trim any unfilled tail rows
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
