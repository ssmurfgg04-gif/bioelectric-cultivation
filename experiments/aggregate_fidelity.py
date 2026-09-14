"""Aggregate the 24 exp8-sweep shard artifacts into the gate-robustness map.

Reads results/sweep/cell_*.json (one per runner shard), builds:

  - results/fidelity_sweep_summary.json  (the landscape table)
  - results/FIDELITY_SWEEP_REPORT.md     (human report + verdicts)
  - results/figures/fig10_gate_landscape.png (3 panels: gate gain heatmaps
    across jump_rate x f_crit for each kappa; probe bar chart)
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")

from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

SWEEP_DIR = "results/sweep"
RESULTS_DIR = "results"

JUMP_RATES = (0.003, 0.005, 0.008)
F_CRITS = (0.55, 0.62, 0.70)
KAPPAS = (0.020, 0.030)


def main() -> dict:
    global SWEEP_DIR
    if "--dir" in sys.argv:
        SWEEP_DIR = sys.argv[sys.argv.index("--dir") + 1]
    setup()
    paths = sorted(glob.glob(os.path.join(SWEEP_DIR, "cell_*.json")))
    print(f"[aggregate-fidelity] {len(paths)} shard artifacts from {SWEEP_DIR}")
    cells = []
    for p in paths:
        with open(p) as f:
            cells.append(json.load(f))

    landscape = [c for c in cells if c["kind"] == "landscape"]
    probes = [c for c in cells if c["kind"].startswith("probe_")]

    n_cells = len(cells)
    n_gate = sum(1 for c in cells if c.get("gate_holds"))
    gate_ratio = n_gate / max(n_cells, 1)

    # landscape arrays: gate gain (codec/local) per (kappa, f_crit, jump)
    grid = {}
    for kappa in KAPPAS:
        M = np.full((len(F_CRITS), len(JUMP_RATES)), np.nan)
        for c in landscape:
            if abs(c["kappa"] - kappa) < 1e-9:
                i = F_CRITS.index(c["f_crit"])
                j = JUMP_RATES.index(c["jump_rate"])
                M[i, j] = c["gains"]["codec_vs_local"]
        grid[kappa] = M

    # aggregates over all cells
    def agg(key):
        vals = [c["gains"][key] for c in cells if key in c.get("gains", {})]
        return float(np.mean(vals)) if vals else float("nan")

    summary = {
        "n_cells": n_cells,
        "n_landscape": len(landscape),
        "n_probes": len(probes),
        "gate_holds_cells": n_gate,
        "gate_hold_fraction": gate_ratio,
        "mean_gains": {k: agg(k) for k in (
            "codec_vs_none", "local_vs_none", "codec_vs_local",
            "regen_vs_none", "chan_vs_codec", "chan_vs_blind")},
        "cells": [{k: c[k] for k in ("kind", "jump_rate", "f_crit", "kappa",
                                     "channel_factor", "levels", "medians",
                                     "gains", "gate_holds")} for c in cells],
    }

    # ------------------------------------------------------------ verdicts
    mean_gate = summary["mean_gains"]["codec_vs_local"]
    verdicts = {
        "gate_robustness": (
            f"the Level-3 gate (codec/local >= 1.03) holds in {n_gate}/{n_cells} "
            f"cells ({gate_ratio:.0%}) across the physics landscape; mean "
            f"codec/local x{mean_gate:.3f}"),
        "regen": (f"regeneration rejuvenates in "
                  f"{sum(1 for c in cells if c['gains']['regen_vs_none'] >= 1.15)}/{n_cells} "
                  f"cells (mean x{agg('regen_vs_none'):.2f})"),
        "gating_pays": (f"verification-gated channel therapy beats blind boosting in "
                        f"{sum(1 for c in cells if c['gains']['chan_vs_blind'] > 1.0)}/{n_cells} "
                        f"cells (mean x{agg('chan_vs_blind'):.3f})"),
        "worst_cell": min(cells, key=lambda c: c["gains"]["codec_vs_local"])["kind"],
        "best_cell": max(cells, key=lambda c: c["gains"]["codec_vs_local"])["kind"],
    }
    summary["verdicts"] = verdicts

    # ------------------------------------------------------------ report
    lines = [
        "# Fidelity Sweep Report — Level-3 gate robustness",
        "",
        f"- Shards aggregated: **{n_cells}/24**",
        f"- Gate holds (codec/local >= 1.03): **{n_gate}/{n_cells}** "
        f"({gate_ratio:.0%})",
        f"- Mean codec/local: **x{mean_gate:.3f}**  |  "
        f"mean codec/none: x{agg('codec_vs_none'):.3f}  |  "
        f"mean regen/none: x{agg('regen_vs_none'):.3f}",
        "",
        "## Landscape cells (kappa x f_crit x jump_rate)",
        "",
        "| kappa | f_crit | jump | none | local | codec | regen | chan | blind | codec/local | gate |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in landscape:
        m, g = c["medians"], c["gains"]
        lines.append(
            f"| {c['kappa']:.3f} | {c['f_crit']} | {c['jump_rate']} "
            f"| {m['none']:.0f} | {m['local']:.0f} | {m['codec']:.0f} "
            f"| {m['regen']:.0f} | {m['chan']:.0f} | {m['blind']:.0f} "
            f"| x{g['codec_vs_local']:.3f} | {'HOLDS' if c['gate_holds'] else 'FAILS'} |")
    lines += ["", "## Probe cells", "",
              "| probe | none | local | codec | regen | chan | blind | codec/local | gate |",
              "|---|---|---|---|---|---|---|---|---|"]
    for c in probes:
        m, g = c["medians"], c["gains"]
        lines.append(
            f"| {c['kind']} | {m['none']:.0f} | {m['local']:.0f} | {m['codec']:.0f} "
            f"| {m['regen']:.0f} | {m['chan']:.0f} | {m['blind']:.0f} "
            f"| x{g['codec_vs_local']:.3f} | {'HOLDS' if c['gate_holds'] else 'FAILS'} |")
    lines += ["", "## Verdicts", ""]
    for k, v in verdicts.items():
        lines.append(f"- **{k}**: {v}")
    lines += [
        "",
        "Codec architecture note: this sweep runs the FIXED codec (consensus-read",
        "detection + per-cell archive writes) — the batched rewrite that repaired",
        "two latent bugs (boundary destruction by cluster-mean writes; BP-smear",
        "false-positive detection). Gate gains are therefore directly comparable",
        "across cells but slightly stronger than the original exp8 single-regime",
        "run (documented in FALSIFICATION.md).",
    ]
    report = "\n".join(lines) + "\n"
    with open(os.path.join(RESULTS_DIR, "FIDELITY_SWEEP_REPORT.md"), "w") as f:
        f.write(report)
    with open(os.path.join(RESULTS_DIR, "fidelity_sweep_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 3.9), constrained_layout=True)
    for ax, kappa in zip(axes[:2], KAPPAS):
        M = grid.get(kappa)
        if M is None or np.all(np.isnan(M)):
            continue
        im = ax.imshow(M, cmap="RdYlGn", vmin=0.95, vmax=1.25, aspect="auto")
        ax.set_xticks(range(len(JUMP_RATES)))
        ax.set_xticklabels([f"{j:.3f}" for j in JUMP_RATES])
        ax.set_yticks(range(len(F_CRITS)))
        ax.set_yticklabels([f"{f}" for f in F_CRITS])
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if np.isfinite(M[i, j]):
                    ax.text(j, i, f"x{M[i, j]:.2f}", ha="center", va="center",
                            fontsize=8)
        ax.set_title(f"kappa = {kappa:.3f}")
        ax.set_xlabel("jump_rate")
        ax.set_ylabel("f_crit")
        ax.grid(False)
    fig.colorbar(im, ax=axes[:2], shrink=0.85, label="codec/local gain")

    ax = axes[2]
    kinds = [c["kind"].replace("probe_", "") for c in probes]
    gate_vals = [c["gains"]["codec_vs_local"] for c in probes]
    y = np.arange(len(kinds))
    ax.barh(y, gate_vals, color=[PALETTE["good"] if v >= 1.03 else PALETTE["accent"]
                                 for v in gate_vals])
    ax.axvline(1.03, color="k", ls="--", lw=1)
    ax.set_yticks(y); ax.set_yticklabels(kinds, fontsize=7)
    ax.set_xlabel("codec/local gain (x)")
    ax.set_title("probe cells")
    for i, v in enumerate(gate_vals):
        ax.text(v, i, f" x{v:.2f}", va="center", fontsize=7)

    fig.savefig(fig_path("fig10_gate_landscape.png"))
    plt.close(fig)

    print(f"  gate holds: {n_gate}/{n_cells} ({gate_ratio:.0%}); "
          f"mean codec/local x{mean_gate:.3f}")
    print(f"  regen/none x{agg('regen_vs_none'):.2f}; "
          f"chan/blind x{agg('chan_vs_blind'):.3f}")
    print(f"[aggregate-fidelity] -> {RESULTS_DIR}/fidelity_sweep_summary.json, "
          f"{RESULTS_DIR}/FIDELITY_SWEEP_REPORT.md, "
          f"results/figures/fig10_gate_landscape.png")
    return summary


if __name__ == "__main__":
    main()
