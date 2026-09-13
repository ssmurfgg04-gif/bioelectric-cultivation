"""EXP1 — Planarian reprogramming and stable morphological memory.

Reproduces, in silico, the Levin-lab result structure (Durant et al. 2017;
Pezzulo & Levin 2021):
  1. a 24h gap-junction-blocked + tail-depolarization perturbation stably
     rewrites the regeneration target (two-headed morphology);
  2. the rewrite PERSISTS across subsequent amputations (memory);
  3. sub-threshold perturbation does NOT rewrite (dose-response);
  4. gap-junction blockade alone does NOT rewrite (negative control —
     guards against "any perturbation works" overfitting).

Falsification test T1.1 in tests/test_falsification.py.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import (
    wildtype_target, twoheaded_target, head_likeness, pattern_error,
)
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt


N = 100
DT = 0.1


def make_collective(seed: int) -> BioElectricCollective:
    c = BioElectricCollective(n=N, seed=seed, noise_std=0.3)
    c.set_target(wildtype_target(N))
    c.run(10, dt=DT)
    return c


def reprogram(c: BioElectricCollective, voltage: float, duration: float = 24.0,
              gj_block: float = 0.05) -> None:
    c.block_gap_junctions(gj_block)
    c.clamp(slice(3 * N // 4, N), voltage)
    c.run(duration, dt=DT)
    c.restore_gap_junctions(1.0)
    c.release_clamps()


def amputate_and_regrow(c: BioElectricCollective, rounds: int = 2,
                        region: slice | None = None) -> list[dict]:
    """Cut the tail zone; the blastema regrows by extending the stored pattern
    from the wound boundary (see BioElectricCollective.regrow)."""
    out = []
    reg = region if region is not None else slice(85, 100)
    for r in range(rounds):
        c.amputate(reg, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(reg, cell_period=0.8, dt=DT, noise=0.6)
        c.run(15, dt=DT)
        out.append({
            "round": r + 1,
            "head_likeness_head": head_likeness(c.V, slice(0, N // 4)),
            "head_likeness_tail": head_likeness(c.V, slice(3 * N // 4, N)),
            "tail_theta_mean": float(c.theta[3 * N // 4:].mean()),
        })
    return out


def main() -> dict:
    setup()
    results: dict = {}

    # ---- 1. wild-type stability ------------------------------------------------
    c = make_collective(seed=1)
    wt_err = [c.pattern_error(wildtype_target(N))]
    for _ in range(20):
        c.run(1, dt=DT)
        wt_err.append(c.pattern_error(wildtype_target(N)))
    results["wt_pattern_error_final"] = wt_err[-1]
    results["wt_stable"] = wt_err[-1] < 3.0

    # ---- 2. reprogramming + memory across amputations ---------------------------
    c = make_collective(seed=2)
    theta_before = c.theta.copy()
    V_traces = []
    # record trajectory through the protocol
    c.block_gap_junctions(0.05)
    c.clamp(slice(3 * N // 4, N), -20.0)
    for _ in range(240):  # 24 time units at dt=0.1
        c.step(DT)
        if len(V_traces) % 4 == 0 or not V_traces:
            V_traces.append(c.V.copy())
        if len(V_traces) >= 60:
            break
    V_traces = np.array(V_traces)
    c.restore_gap_junctions(1.0)
    c.release_clamps()
    c.run(20, dt=DT)
    theta_after = c.theta.copy()
    twohead_err = c.pattern_error(twoheaded_target(N))
    results["twoheaded_pattern_error"] = twohead_err
    results["twoheaded_achieved"] = twohead_err < 6.0
    results["tail_theta_before"] = float(theta_before[3 * N // 4:].mean())
    results["tail_theta_after"] = float(theta_after[3 * N // 4:].mean())

    rounds = amputate_and_regrow(c, rounds=2)
    results["amputation_rounds"] = rounds
    results["memory_persists"] = rounds[-1]["head_likeness_tail"] > 0.7

    # ---- 3. negative control: GJ blockade alone ----------------------------------
    c2 = make_collective(seed=3)
    c2.block_gap_junctions(0.05)
    c2.run(24, dt=DT)
    c2.restore_gap_junctions(1.0)
    c2.run(20, dt=DT)
    rounds_ctl = amputate_and_regrow(c2, rounds=1)
    results["control_gjblock_tail_headlikeness"] = rounds_ctl[0]["head_likeness_tail"]
    results["control_gjblock_no_reprogram"] = rounds_ctl[0]["head_likeness_tail"] < 0.35

    # ---- 4. dose-response --------------------------------------------------------
    doses = [-35.0, -32.5, -30.0, -27.5, -25.0, -22.5, -20.0, -17.5, -15.0]
    dose_curve = []
    for v in doses:
        c3 = make_collective(seed=4)
        reprogram(c3, v)
        c3.run(20, dt=DT)
        r = amputate_and_regrow(c3, rounds=1)[0]
        dose_curve.append({"clamp_voltage": v, "tail_headlikeness": r["head_likeness_tail"],
                           "tail_theta": r["tail_theta_mean"]})
    results["dose_response"] = dose_curve
    v15 = dose_curve[0]["tail_headlikeness"]
    v20 = dose_curve[-2]["tail_headlikeness"]
    results["dose_response_present"] = v20 > 0.7 and v15 < 0.4

    # ---- figure -------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.0), constrained_layout=True)
    ax = axes[0, 0]
    im = ax.imshow(V_traces, aspect="auto", cmap="RdYlBu_r",
                   extent=[0, N, 24, 0], vmin=-60, vmax=-15)
    ax.set_title("(a) Reprogramming: V(x,t) during 24h perturbation")
    ax.set_xlabel("cell index (anterior -> posterior)")
    ax.set_ylabel("time (h)")
    fig.colorbar(im, ax=ax, label="Vmem (mV)", shrink=0.85)

    ax = axes[0, 1]
    x = np.arange(N)
    ax.plot(x, theta_before, color=PALETTE["muted"], lw=1.2, label="theta before")
    ax.plot(x, theta_after, color=PALETTE["accent"], lw=1.6, label="theta after (memory)")
    ax.plot(x, twoheaded_target(N), "--", color=PALETTE["primary"], lw=1.0,
            label="two-headed target")
    ax.set_title("(b) Target memory rewrite (theta)")
    ax.set_xlabel("cell index"); ax.set_ylabel("theta (mV)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)

    ax = axes[1, 0]
    rounds_lab = [r["round"] for r in rounds]
    tail_h = [r["head_likeness_tail"] for r in rounds]
    ctl_h = rounds_ctl[0]["head_likeness_tail"]
    w = 0.35
    ax.bar(rounds_lab, tail_h, width=w, color=PALETTE["accent"], label="reprogrammed + amputation")
    ax.bar([rounds_lab[-1] + w], [ctl_h], width=w, color=PALETTE["muted"], label="GJ-block control")
    ax.axhline(0.7, color=PALETTE["good"], ls="--", lw=1, label="two-headed threshold")
    ax.set_ylim(0, 1.05)
    ax.set_title("(c) Memory across amputations")
    ax.set_xlabel("amputation round"); ax.set_ylabel("tail head-likeness")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)

    ax = axes[1, 1]
    ax.plot([d["clamp_voltage"] for d in dose_curve],
            [d["tail_headlikeness"] for d in dose_curve], "o-", color=PALETTE["primary"])
    ax.axhline(0.7, color=PALETTE["good"], ls="--", lw=1)
    ax.invert_xaxis()
    ax.set_title("(d) Dose-response of reprogramming")
    ax.set_xlabel("clamp voltage (mV, depolarizing ->)")
    ax.set_ylabel("tail head-likeness after amputation")

    fig.savefig(fig_path("fig1_regeneration_memory.png"))
    plt.close(fig)

    path = dump_json("exp1_regeneration.json", results)
    print(f"[exp1] results -> {path}")
    print(f"  two-headed achieved: {results['twoheaded_achieved']} "
          f"(pattern error {twohead_err:.2f} mV)")
    print(f"  memory across 2 amputations: {results['memory_persists']}")
    print(f"  GJ-block control (no reprogram): {results['control_gjblock_no_reprogram']}")
    print(f"  dose response present: {results['dose_response_present']}")
    return results


if __name__ == "__main__":
    main()
