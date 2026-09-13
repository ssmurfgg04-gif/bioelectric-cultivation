"""Aggregate sharded sweep results into landscape figures + report.

    python -m experiments.aggregate --dir results/sweep
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")

from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt


def main() -> None:
    setup()
    d = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else "results/sweep"
    rows = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        with open(f) as fh:
            rows.extend(json.load(fh).get("results", []))
    if not rows:
        print("no shard results found")
        return
    print(f"[aggregate] {len(rows)} runs from {d}")

    lam = sorted({r["lambda_gap"] for r in rows})
    kap = sorted({r["kappa_noise"] for r in rows})
    hsys = sorted({r["h_sys"] for r in rows})
    h_mid = hsys[len(hsys) // 2]

    def cell(field, cond, h, agg=np.median):
        M = np.full((len(lam), len(kap)), np.nan)
        for r in rows:
            if r["cond"] == cond and r["h_sys"] == h:
                M[lam.index(r["lambda_gap"]), kap.index(r["kappa_noise"])] = r[field]
        return agg(M, axis=...) if False else M

    # median over seeds per cell
    def grid_of(field, cond, h):
        M = np.full((len(lam), len(kap)), np.nan)
        for i, l_ in enumerate(lam):
            for j, k_ in enumerate(kap):
                vals = [r[field] for r in rows
                        if r["cond"] == cond and r["h_sys"] == h
                        and r["lambda_gap"] == l_ and r["kappa_noise"] == k_]
                if vals:
                    M[i, j] = float(np.median(vals))
        return M

    M_life = grid_of("median", "none", h_mid)
    M_gain = np.full((len(lam), len(kap)), np.nan)
    for i, l_ in enumerate(lam):
        for j, k_ in enumerate(kap):
            base = [r["median"] for r in rows if r["cond"] == "none" and r["h_sys"] == h_mid
                    and r["lambda_gap"] == l_ and r["kappa_noise"] == k_]
            cod = [r["median"] for r in rows if r["cond"] == "codec" and r["h_sys"] == h_mid
                   and r["lambda_gap"] == l_ and r["kappa_noise"] == k_]
            if base and cod:
                M_gain[i, j] = float(np.median(cod) / np.median(base))
    M_beta = grid_of("beta_adult", "none", h_mid)

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8), constrained_layout=True)
    for ax, M, title, cmap, fmt in [
        (axes[0], M_life, "(a) Median lifespan (no maintenance)",
         "viridis", "{:.0f}"),
        (axes[1], M_beta, "(b) Gompertz beta (adult window)",
         "magma", "{:.3f}"),
        (axes[2], M_gain, "(c) Maintenance gain (codec / none)",
         "RdYlGn", "x{:.2f}"),
    ]:
        im = ax.imshow(M.T, origin="lower", cmap=cmap, aspect="auto")
        ax.set_xticks(range(len(lam))); ax.set_xticklabels([str(x) for x in lam])
        ax.set_yticks(range(len(kap))); ax.set_yticklabels([str(x) for x in kap])
        ax.set_xlabel("lambda_gap (junction decay)")
        ax.set_ylabel("kappa_noise (noise growth)")
        ax.set_title(f"{title}\nh_sys={h_mid}")
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if np.isfinite(M[i, j]):
                    ax.text(i, j, fmt.format(M[i, j]), ha="center", va="center",
                            fontsize=7.5, color="white" if cmap != "RdYlGn" else "black")
        fig.colorbar(im, ax=ax, shrink=0.85)

    fig.savefig(fig_path("fig9_sweep_landscape.png"))
    plt.close(fig)

    best_models = {}
    for r in rows:
        best_models[r["best_model"]] = best_models.get(r["best_model"], 0) + 1
    summary = {
        "runs": len(rows),
        "shards": len(glob.glob(os.path.join(d, "*.json"))),
        "best_model_counts": best_models,
        "mean_beta": float(np.mean([r["beta_adult"] for r in rows])),
        "mean_gain_codec_vs_none": float(np.mean([
            r["median"] for r in rows if r["cond"] == "codec"]) /
            np.mean([r["median"] for r in rows if r["cond"] == "none"])),
    }
    dump_json("sweep_summary.json", summary)
    print(f"[aggregate] summary: {summary}")

    # markdown report
    lines = ["# Sweep aggregate report", "",
             f"- runs: {summary['runs']} across {summary['shards']} shards",
             f"- best-model counts (adult window): {best_models}",
             f"- mean Gompertz beta: {summary['mean_beta']:.4f} /yr",
             f"- mean maintenance gain: x{summary['mean_gain_codec_vs_none']:.2f}",
             "", "## Median lifespan grid (none, h_sys="
             f"{h_mid})", "",
             "| lambda \\ kappa | " + " | ".join(str(k) for k in kap) + " |",
             "|---" * (len(kap) + 1) + "|"]
    for i, l_ in enumerate(lam):
        lines.append(f"| {l_} | " + " | ".join(
            f"{M_life[i, j]:.1f}" if np.isfinite(M_life[i, j]) else "-"
            for j in range(len(kap))) + " |")
    lines += ["", "## Maintenance gain grid (codec/none)", "",
              "| lambda \\ kappa | " + " | ".join(str(k) for k in kap) + " |",
              "|---" * (len(kap) + 1) + "|"]
    for i, l_ in enumerate(lam):
        lines.append(f"| {l_} | " + " | ".join(
            f"x{M_gain[i, j]:.2f}" if np.isfinite(M_gain[i, j]) else "-"
            for j in range(len(kap))) + " |")
    with open(os.path.join("results", "SWEEP_REPORT.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("[aggregate] wrote results/SWEEP_REPORT.md and fig9")


if __name__ == "__main__":
    main()
