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


def regen_lightcone(seed: int, n: int = 100,
                    regen_slice: slice | None = None,
                    pulse_cell: int | None = None,
                    pulse_hours: float = 2.0,
                    pulse_v: float = 0.0,
                    pulse_during_regen: bool = True,
                    gap_scale: float = 1.0,
                    settle_hours: float = 24.0,
                    post_hours: float = 15.0,
                    cell_period: float = 0.8,
                    dt: float = 0.1,
                    noise: float = 0.6) -> dict:
    """Paired-trajectory light cone of a pulse delivered DURING the
    regeneration window (exp49; the LC-G4 resolution).

    Pezzulo/Levin 2017 (PMC28538159): a *temporary* bioelectric
    modulation of AMPUTATED trunk fragments permanently rewrites the
    regenerative pattern — the published rewrite regime is the REGEN
    WINDOW, not the homeostatic state. This instrument pairs two
    identical collectives (same seed => identical RNG streams), gives
    both the same amputation, and clamps one cell of B while the
    regeneration walk is committing cells. The per-cell theta divergence
    after the walk IS the causal influence of the pulse through the
    commitment chain: each committing cell reads theta[src] (M25), so a
    perturbed wound face propagates into EVERY subsequently committed
    identity — the regen-window cone spans the whole regenerate.

    The walk below mirrors BioElectricCollective.regrow's forward
    formula VERBATIM — chain draw, M25 r-mix with the blind guess under
    blockade (guess = wound_center + N(0, blastema_readout_noise)),
    identical RNG draw order — so that the pulse_hours=0 arm at full
    coupling is bit-identical to a plain c.regrow and the blocked
    condition carries the model's exact guess-mix semantics (exp49's
    LC5-G0 equivalence gate).
    """
    a = BioElectricCollective(n=n, seed=seed)
    b = BioElectricCollective(n=n, seed=seed)
    for c in (a, b):
        c.gap_scale = float(gap_scale)
        c.G = c.G0 * float(gap_scale)
        c.deg = c.G.sum(axis=1)
        c.run(settle_hours, dt=dt)          # settle both identically
    if regen_slice is None:
        regen_slice = slice(int(n * 0.85), n)
    idx = list(np.arange(n)[regen_slice])
    if pulse_cell is None:
        pulse_cell = idx[0] - 1             # the wound face (intact side)
    steps_per_cell = max(1, int(round(cell_period / dt)))
    steps_pulse = int(round(pulse_hours / dt)) if pulse_during_regen else 0

    a.amputate(regen_slice, wound_voltage=-30.0, blastema_theta=-40.0)
    b.amputate(regen_slice, wound_voltage=-30.0, blastema_theta=-40.0)
    if pulse_during_regen and pulse_hours > 0:
        b.clamp(np.array([pulse_cell]), pulse_v)

    # regrow's walk preamble (wound state for the M25 blind guess)
    r = float(a.gap_scale)                 # identical in A and B
    wound_center_a = float(np.mean(a.theta[idx]))
    wound_center_b = float(np.mean(b.theta[idx]))
    src = idx[0] - 1 if idx[0] - 1 >= 0 else idx[0]
    steps_done = 0
    diverging: list[int] = []
    for i in idx:
        for _ in range(steps_per_cell):
            a.step(dt)
            b.step(dt)
            steps_done += 1
            if steps_done == steps_pulse:
                b.release_clamps()          # pulse ends mid-walk
        # the model's forward-walk commitment (regrow formula verbatim,
        # including the M25 r-mix and its draw order)
        theta_a = a.theta[src] + a.rng.normal(0.0, noise)
        theta_b = b.theta[src] + b.rng.normal(0.0, noise)
        if r < 1.0:
            guess_a = wound_center_a + a.rng.normal(
                0.0, a.blastema_readout_noise)
            guess_b = wound_center_b + b.rng.normal(
                0.0, b.blastema_readout_noise)
            theta_a = r * theta_a + (1.0 - r) * guess_a
            theta_b = r * theta_b + (1.0 - r) * guess_b
        a.theta[i] = theta_a
        a.V[i] = theta_a
        b.theta[i] = theta_b
        b.V[i] = theta_b
        diverging.append(int(abs(theta_b - theta_a) > 0.5))
        src = i
    b.release_clamps()
    a.run(post_hours, dt=dt)
    b.run(post_hours, dt=dt)

    residue = np.abs(b.theta - a.theta)
    far_end = idx[-1]
    return {
        "seed": seed,
        "pulse_cell": int(pulse_cell),
        "pulse_hours": float(pulse_hours),
        "pulse_during_regen": bool(pulse_during_regen),
        "gap_scale": float(gap_scale),
        "regen_cells": len(idx),
        "far_end_cell": int(far_end),
        "far_end_residue_mv": float(residue[far_end]),
        "max_residue_in_regen_mv": float(np.max(residue[idx])),
        "cells_committed_while_pulse_active": (
            min(len(idx), steps_pulse // steps_per_cell + 1)
            if pulse_during_regen and pulse_hours > 0 else 0),
        "residue_profile": [round(float(residue[i]), 3) for i in idx],
    }
