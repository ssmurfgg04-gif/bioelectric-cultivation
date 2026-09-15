"""Stage 4 (Nascent Soul) — the cognitive light cone.

THE CONCEPT
-----------
The "cognitive light cone" of a bioelectric perturbation is the causal
reach of its influence through the collective: how far, in cells, and
how fast, in time, a localized change of state propagates. This is the
measurable behind the cognitive-scaling claim (Pezzulo & Levin 2021):
the same coupled dynamics that implement regeneration implement
primitive cognition — integration, memory, goal-maintenance — and the
LIGHT CONE is how much body one cell's state can inform, and how much
pattern the collective can integrate on behalf of a part.

THE INSTRUMENT (paired-trajectory, zero averaging)
--------------------------------------------------
Two collectives with the SAME seed have IDENTICAL RNG streams: run them
side by side, pulse one cell of B (a brief clamp) while A runs free,
and the per-cell divergence |V_B - V_A| at distance d and time t IS the
causal influence of the pulse — exact, paired, no Monte Carlo noise.
The horizon at time t is the largest d with influence > epsilon.

M25 predicts the cone is JUNCTION-CARRIED: under gap-junction blockade
the cone collapses (the collective becomes cognitively fragmented —
cells can neither inform nor integrate). The theta residue after the
pulse (the light cone leaves a memory) is the D3 collective-attractor
property at the cognitive level.
"""
from __future__ import annotations

import numpy as np

from cultivation.bioelectric.collective import BioElectricCollective


def measure_lightcone(seed: int, n: int = 100,
                      pulse_cell: int | None = None,
                      pulse_v: float = 0.0,
                      pulse_hours: float = 2.0,
                      total_hours: float = 24.0,
                      dt: float = 0.1,
                      gap_scale: float = 1.0,
                      epsilon_mv: float = 0.5) -> dict:
    """Paired-trajectory light cone of a single-cell pulse.

    Returns horizon(t) profile, final influence profile, and the theta
    residue (memory) after the pulse.
    """
    a = BioElectricCollective(n=n, seed=seed)
    b = BioElectricCollective(n=n, seed=seed)
    for c in (a, b):
        c.gap_scale = float(gap_scale)
        c.G = c.G0 * float(gap_scale)
        c.deg = c.G.sum(axis=1)
        c.run(24, dt=dt)                    # settle both identically
    if pulse_cell is None:
        pulse_cell = n // 2
    steps_pulse = int(round(pulse_hours / dt))
    steps_total = int(round(total_hours / dt))
    b.clamp(np.array([pulse_cell]), pulse_v)

    horizons: list[float] = []              # horizon per record step
    times: list[float] = []
    influence: np.ndarray | None = None
    for t in range(steps_total):
        a.step(dt)
        b.step(dt)
        dV = np.abs(b.V - a.V)
        if t < steps_pulse:
            pass
        else:
            dV[pulse_cell] = 0.0            # exclude the pulse site itself
        if t % 10 == 0:                     # record every 1 time unit
            far = np.where(dV > epsilon_mv)[0]
            h = int(np.max(np.abs(far - pulse_cell))) if len(far) else 0
            horizons.append(h)
            times.append(t * dt)
        if t == steps_total - 1:
            influence = dV
    b.release_clamps()

    residue = np.abs(b.theta - a.theta)     # theta memory the pulse left
    return {
        "seed": seed,
        "pulse_cell": pulse_cell,
        "gap_scale": gap_scale,
        "times": times,
        "horizons": horizons,
        "final_influence": influence.tolist(),
        "final_horizon": int(horizons[-1]),
        "theta_residue": {
            "max": float(np.max(residue)),
            "mean": float(np.mean(residue)),
            "at_half_chain": float(residue[min(n // 2 + n // 4, n - 1)]),
            "cells_above_1mv": int(np.sum(residue > 1.0)),
        },
    }
