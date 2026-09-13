"""Shared experiment utilities: deterministic output dirs, JSON dump, plot style."""

from __future__ import annotations

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

# one consistent, low-saturation scientific palette
PALETTE = {
    "primary": "#1a5276",
    "accent": "#c0392b",
    "good": "#1e8449",
    "warn": "#b7950b",
    "muted": "#7f8c8d",
    "line2": "#2874a6",
    "line3": "#9b59b6",
}


def setup() -> tuple[str, str]:
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plt.rcParams.update({
        "figure.dpi": 130,
        "savefig.dpi": 150,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.5,
    })
    return RESULTS_DIR, FIGURES_DIR


def dump_json(name: str, obj: dict) -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=float)
    return path


def fig_path(name: str) -> str:
    os.makedirs(FIGURES_DIR, exist_ok=True)
    return os.path.join(FIGURES_DIR, name)
