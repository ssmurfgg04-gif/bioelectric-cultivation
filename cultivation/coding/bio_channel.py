"""Bioelectric channel presets — the ageing analogue of helix-codec's
sequencing-channel presets (simulate.ts: PRESET_ILLUMINA / NANOPORE / ...).

A "channel" here is measurement + maintenance access to the bioelectric
state, whose fidelity degrades with organismal age: voltage readout noise,
cluster dropout (senesced cells are unreadable), and symbol corruption
(noise-driven quantization flips).
"""

from __future__ import annotations

import numpy as np

CHANNEL_PRESETS: dict[str, dict] = {
    "young":   {"meas_noise_mV": 1.0, "dropout": 0.02, "symbol_err": 0.005},
    "mature":  {"meas_noise_mV": 1.8, "dropout": 0.06, "symbol_err": 0.012},
    "old":     {"meas_noise_mV": 3.0, "dropout": 0.12, "symbol_err": 0.025},
    "aged":    {"meas_noise_mV": 5.0, "dropout": 0.20, "symbol_err": 0.045},
    "ancient": {"meas_noise_mV": 8.0, "dropout": 0.30, "symbol_err": 0.08},
}


def corrupt_symbols(symbols: np.ndarray, preset: dict,
                    rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Apply a bioelectric channel to a symbol array.

    symbols: (n,) ints in [0, 255]
    Returns (observed, dead_mask): values at dead positions are garbage;
    live values flip with probability `symbol_err`.
    """
    n = len(symbols)
    dead = rng.random(n) < preset["dropout"]
    observed = symbols.copy()
    flips = rng.random(n) < preset["symbol_err"]
    mag = rng.integers(1, 8, size=n)
    observed = np.where(flips, observed ^ mag, observed)
    observed[dead] = rng.integers(0, 256, size=n)
    return observed, dead
