"""The TOWER summary figure — one image, four phases.

  (a) exp10  the CEM-discovered intervention policy vs the hand-built
             baseline (the 8-dim policy space — what the search chose)
  (b) exp13  the jump-rate scaling law of the codec gate (quadratic fit,
             R2) — how the gate's value scales with corruption pressure
  (c) exp11  the engineered novel morphology (third eye: target vs
             achieved settled Vmem vs wild-type)
  (d) exp12  the consciousness-body interface retention curves (reward /
             noreward / no-latch / baseline) — the latch as trusted,
             decay-tolerant write medium

Everything is LOADED from the committed results JSONs (nothing re-run
except panel (c)'s 300-unit settle, which is deterministic given the
stored protocol vector).
"""
from __future__ import annotations

import json
import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.morpho_engineering import (
    ALPHA_LATCH, ClampProtocol, LatchingCollective, discrete_fidelity,
    target_third_eye, target_wildtype,
)
from cultivation.inverse.design import HAND_CODEC, POLICY_NAMES
from experiments.viz import PALETTE, fig_path, setup

import matplotlib.pyplot as plt


def main() -> None:
    setup()
    exp10 = json.load(open("results/exp10_inverse_design.json"))
    exp13 = json.load(open("results/exp13_scaling.json"))
    exp11 = json.load(open("scripts_dev/exp11_state.json"))
    norew = json.load(open("results/noreward_fidelity.json"))
    exp14 = json.load(open("results/integrated_stack_heldout.json"))

    fig, axes = plt.subplots(1, 4, figsize=(16.0, 4.2),
                             constrained_layout=True)

    # ---------------------------------------------- (a) exp10 policy
    ax = axes[0]
    u_disc = exp10["discovered_u"]
    x = np.arange(len(POLICY_NAMES))
    w = 0.38
    ax.bar(x - w / 2, u_disc, w, color=PALETTE["line2"],
           label="CEM-discovered")
    ax.bar(x + w / 2, HAND_CODEC, w, color=PALETTE["muted"],
           label="hand-built (exp8)")
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace("_", "\n") for n in POLICY_NAMES],
                       fontsize=5.6)
    ax.set_ylabel("value (policy units)")
    ax.set_title("(a) exp10: the discovered policy\n"
                 f"(held-out stack x{exp14['gains']['full_stack']:.2f} "
                 f"vs pre-gate)")
    ax.legend(frameon=False, fontsize=7)

    # ------------------------------------------- (b) exp13 scaling law
    ax = axes[1]
    rows = exp13["C1"]["jump_axis"]
    jr = np.array([r["jump_rate"] for r in rows])
    gate = np.array([r["gate_codec_none"] for r in rows])
    c = np.polyfit(jr, gate, 2)
    fit = np.polyval(c, jr)
    ss_res = float(((gate - fit) ** 2).sum())
    ss_tot = float(((gate - gate.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    xs = np.linspace(jr.min(), jr.max(), 120)
    ax.plot(jr, gate, "o", ms=7, color=PALETTE["primary"],
            label="gate (codec / none)")
    ax.plot(xs, np.polyval(c, xs), "-", lw=1.4, color=PALETTE["accent"],
            label=f"quadratic fit (R2={r2:.3f})")
    ax.axhline(1.0, color=PALETTE["muted"], ls=":", lw=1.0)
    ax.set_xlabel("regional jump rate (corruption pressure)")
    ax.set_ylabel("lifespan gain of verified maintenance")
    ax.set_title("(b) exp13: gate vs corruption\n(the scaling law)")
    ax.legend(frameon=False, fontsize=7)

    # ---------------------------------------- (c) exp11 novel morphology
    ax = axes[2]
    target = target_third_eye(100)
    u = np.array(exp11["discovered"]["third_eye"]["u"])
    col = LatchingCollective(n=100, seed=1)
    col.set_target(target_wildtype(100))
    col.set_state(target_wildtype(100) + col.rng.normal(0, 2, 100))
    proto = ClampProtocol(u)
    proto.apply(col)
    col.run(300.0, dt=0.1)
    ax.plot(target, lw=2.2, color=PALETTE["muted"], label="novel target")
    ax.plot(col.V, lw=1.2, color=PALETTE["good"], label="achieved (settled)")
    ax.plot(target_wildtype(100), lw=1.0, ls="--", color=PALETTE["accent"],
            alpha=0.6, label="wild-type")
    fid = exp11["discovered"]["third_eye"]["val_mean"]
    ax.set_title(f"(c) exp11: third eye\nfidelity {fid:.2f}, "
                 f"alpha_latch={ALPHA_LATCH}")
    ax.set_xlabel("position (cells)")
    ax.set_ylabel("Vmem (mV)")
    ax.legend(frameon=False, fontsize=7)

    # ------------------------------------- (d) exp12 retention curves
    ax = axes[3]
    styles = {
        "reward": (PALETTE["good"], "-", "reward loop (learning intact)"),
        "noreward": (PALETTE["line2"], "-", "no reward (latch only)"),
        "no-latch": (PALETTE["warn"], "--", "no latch (control)"),
        "baseline": (PALETTE["muted"], ":", "no interface (baseline)"),
    }
    for arm, (c_, ls, lab) in styles.items():
        a = norew["arms"][arm]
        ax.plot(a["times"], a["fidelity_mean"], ls, lw=1.6, color=c_,
                label=lab)
    ax.set_xlabel("time (interface units)")
    ax.set_ylabel("target fidelity")
    ax.set_ylim(0, 1.05)
    ax.set_title("(d) exp12: retention without reward\n"
                 "(the latch as decay-tolerant medium)")
    ax.legend(frameon=False, fontsize=6.5, loc="lower left")

    fig.savefig(fig_path("fig16_tower_summary.png"))
    plt.close(fig)
    print("saved ->", fig_path("fig16_tower_summary.png"))


if __name__ == "__main__":
    main()
