#!/usr/bin/env python3
"""Batch-2 figures: fig97 (the coverage repair) + fig100 (the
reader's price map). House style: constrained_layout, Okabe-Ito,
200 dpi, no tight_layout/bbox_inches."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/home/z/my-project/bioelectric-cultivation"
FIG = os.path.join(ROOT, "docs", "figures")

OK = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]

with open(os.path.join(ROOT, "results", "exp97_coverage_repair.json")) as f:
    e97 = json.load(f)
with open(os.path.join(ROOT, "results", "exp100_reader_price_map.json")) as f:
    e100 = json.load(f)

# ---- fig97: the artifact, the repair, the staticity ------------------
dec_z = e97["arms"]["star_zones_state"]["decomposition"]
dec_w = e97["arms"]["star_walk_state"]["decomposition"]
groups = list(dec_z.keys())
x = range(len(groups))
w = 0.38
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2),
                               constrained_layout=True)
ax1.bar([i - w / 2 for i in x], [dec_z[g] for g in groups], w,
        color=OK[1], label="zones mode (the artifact)")
ax1.bar([i + w / 2 for i in x], [dec_w[g] for g in groups], w,
        color=OK[2], label="walk mode (repaired)")
ax1.axhline(6.0, ls="--", c="k", lw=0.8)
ax1.text(len(groups) - 0.5, 6.4, "verify bar 6.0 mV", fontsize=8)
ax1.set_xticks(list(x))
ax1.set_xticklabels(groups, rotation=40, ha="right", fontsize=8)
ax1.set_ylabel("per-group RMS vs target (mV)")
ax1.set_title("(a) the star's error: amputated-never-rebuilt\ngap "
              "cells at blastema -40 (exp97 probe)", fontsize=10)
ax1.legend(fontsize=8)

pairs = [("star_zones_star_pt", "star, zones"),
         ("star_walk_star_pt", "star, walk"),
         ("tree_walk", "tree, walk"),
         ("cycle_walk", "walk"),
         ("grid_walk", "grid, walk")]
for i, (k, lab) in enumerate(pairs):
    a = e97["arms"][k]
    ax2.plot([a["post_walk_err"], a["post_settle_err"]], [i, i],
             "-o", color=OK[i % len(OK)], ms=5, label=lab)
ax2.axvline(6.0, ls="--", c="k", lw=0.8)
ax2.set_yticks(range(len(pairs)))
ax2.set_yticklabels([p[1] for p in pairs], fontsize=8)
ax2.set_xlabel("pattern error (mV)  —  post-walk (dot) vs "
               "post-settle (dot)")
ax2.set_title("(b) the settle moves nothing:\n8.52->8.53 artifact, "
              "0.91->1.02 repaired", fontsize=10)
fig.suptitle("exp97 — the coverage repair: the star's 8.5 mV floor "
             "was an executor artifact", fontsize=11)
fig.savefig(os.path.join(FIG, "fig97_coverage_repair.png"), dpi=200)
plt.close(fig)

# ---- fig100: the reader's price map ----------------------------------
cls = e100["classes"]
order = sorted(cls, key=lambda n: ({"DEFAULT": 0, "V_PRICED": 1,
                                    "TWO_DIAL": 2}[cls[n]["call"]],
                                   e100["cells"][n]["default"]["err"]))
colors = {"DEFAULT": OK[2], "V_PRICED": OK[0], "TWO_DIAL": OK[1]}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4),
                               constrained_layout=True)
for i, n in enumerate(order):
    c = cls[n]["call"]
    ax1.barh(i, e100["cells"][n]["default"]["err"], color=colors[c])
    ax1.text(e100["cells"][n]["default"]["err"] + 0.12, i, c,
             va="center", fontsize=7)
ax1.axvline(6.0, ls="--", c="k", lw=0.8)
ax1.set_yticks(range(len(order)))
ax1.set_yticklabels(order, fontsize=8)
ax1.invert_yaxis()
ax1.set_xlabel("default-cell err (mV); all 19 verify at their "
               "mapped cell")
ax1.set_title("(a) the default cell (1, 0.015):\nthe class bands at "
              "the reader's own floor", fontsize=10)

v2 = json.load(open(os.path.join(ROOT, "results",
                                 "exp102_r5_price_oracle.json")))
rows = v2["rows"]
edges = {n: v2["rows"][n]["ratio"] for n in rows}
gridv2 = json.load(open(os.path.join(ROOT, "results",
                                     "exp106_drift_and_oracle_v2.json")))
nx = [100, 196, 400, 784]
ax2.plot(nx, gridv2["oracle_v2"]["grid2d_v2_by_n"], "-o",
         color=OK[0], label="grid2d (V_PRICED)")
ax2.plot(nx, gridv2["oracle_v2"]["torus_v2_by_n"], "-s",
         color=OK[1], label="torus (TWO_DIAL)")
ax2.plot(nx, gridv2["oracle_v2"]["path_v2_by_n"], "-^",
         color=OK[2], label="path (DEFAULT; 1D law)")
ax2.set_xscale("log")
ax2.set_xlabel("n")
ax2.set_ylabel("oracle v2 = crossing / sqrt(edges)")
ax2.set_title("(b) oracle v2 is size-stable on 2D\n(Spearman 0.81 "
              "across the 19 substrates)", fontsize=10)
ax2.legend(fontsize=8)
fig.suptitle("exp100/exp102/exp106 — the reader's dial budget: "
             "the boundary term names the price, the dials pay it",
             fontsize=11)
fig.savefig(os.path.join(FIG, "fig100_reader_price_map.png"), dpi=200)
plt.close(fig)

for f in ("fig97_coverage_repair.png", "fig100_reader_price_map.png"):
    p = os.path.join(FIG, f)
    sz = os.path.getsize(p)
    assert sz > 20000, f"trivial figure: {f} ({sz} B)"
    print(f"OK {f} {sz // 1024} KB")
