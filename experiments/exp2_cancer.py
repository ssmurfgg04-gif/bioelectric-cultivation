"""EXP2 — Cancer normalization by bioelectric state restoration.

Reproduces the result structure of Chernet & Levin 2013/2015 (Oncotarget 4;
Front Physiol 6:519):
  - oncogene-expressing cells are depolarized (initiation);
  - the tumoral state is voltage-gated: depolarization keeps the growth
    driver active, hyperpolarization silences it;
  - tumorigenesis proceeds in a gap-junction-compromised context (isolated
    cells cannot feel the hyperpolarizing pull of healthy tissue);
  - RESTORING GAP-JUNCTION CONNECTIVITY is itself a normalization vector:
    a hyperpolarization wave erodes the tumor from its boundaries (the
    long-range bioelectric signaling result);
  - a direct local clamp normalizes even without connectivity; a
    constitutive ("locked") driver is not normalizable at all; a
    depolarizing "trophic" intervention makes the tumor worse.

Falsification test T1.2.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import wildtype_target
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

N = 100
DT = 0.1
TUMOR = slice(45, 53)   # 8-cell mid-body oncogenic region
G_GAP = 0.35            # strong coupling so the normalization wave propagates
GATE = -18.0            # depolarization-permissive threshold for the driver


def add_oncogene(c: BioElectricCollective, locked: bool = False,
                 rate: float = 0.03, target: float = -10.0) -> None:
    idx = np.arange(N)[TUMOR]
    gate = -1000.0 if locked else GATE
    c.theta_drivers.append((idx, target, rate, gate))


def init_tumor(c: BioElectricCollective) -> None:
    """Oncogene-expressing cells arrive depolarized in BOTH V and theta
    (initiation: oncogene expression directly alters ion-channel profile)."""
    c.corrupt_region(TUMOR, theta_value=-15.0, V_value=-15.0)


def region_depolarized(c) -> float:
    return float((c.V[TUMOR] > -25).mean())


def region_theta(c) -> float:
    return float(c.theta[TUMOR].mean())


def run_case(seed: int, mode: str, locked: bool = False,
             establish: float = 15.0, post: float = 300.0) -> dict:
    """mode: 'none' | 'restore_gj' | 'direct' | 'weak' | (locked uses restore_gj)."""
    c = BioElectricCollective(n=N, seed=seed, noise_std=0.3, g_gap=G_GAP)
    c.set_target(wildtype_target(N))
    add_oncogene(c, locked=locked)
    init_tumor(c)
    c.block_gap_junctions(0.05)   # tumorigenic context: connectivity compromised
    c.run(establish, dt=DT)
    pre = {"V": float(c.V[TUMOR].mean()), "theta": region_theta(c),
           "dep_frac": region_depolarized(c)}

    theta_hist = [region_theta(c)]
    if mode == "restore_gj":
        c.restore_gap_junctions(1.0)
    elif mode == "direct":
        c.clamp(TUMOR, -45.0)
        c.run(48, dt=DT)
        c.release_clamps()
    elif mode == "weak":
        c.clamp(TUMOR, -15.0)     # depolarizing "trophic" intervention
        c.run(48, dt=DT)
        c.release_clamps()

    steps = int(post / DT)
    for _ in range(steps):
        c.step(DT)
        theta_hist.append(region_theta(c))

    return {
        "mode": mode,
        "locked": locked,
        "pre": pre,
        "post": {"V": float(c.V[TUMOR].mean()), "theta": region_theta(c),
                 "dep_frac": region_depolarized(c)},
        "normalized": region_depolarized(c) < 0.2,
        "theta_history": theta_hist,
    }


def main() -> dict:
    setup()
    results: dict = {"cases": []}

    cases = [
        ("untreated (GJ blocked)", run_case(12, mode="none")),
        ("gap-junction connectivity restored", run_case(13, mode="restore_gj")),
        ("direct hyperpolarization -45 mV (GJ still blocked)",
         run_case(14, mode="direct")),
        ("depolarizing 'trophic' clamp -15 mV", run_case(15, mode="weak")),
        ("locked (constitutive) driver + GJ restore",
         run_case(16, mode="restore_gj", locked=True)),
    ]
    for label, r in cases:
        r["label"] = label
        results["cases"].append(r)
        print(f"  {label:48s} dep-frac {r['pre']['dep_frac']:.2f} -> "
              f"{r['post']['dep_frac']:.2f}  normalized={r['normalized']}")

    results["untreated_tumor_persists"] = not cases[0][1]["normalized"]
    results["gj_restore_normalizes"] = cases[1][1]["normalized"]
    results["direct_works_without_gj"] = cases[2][1]["normalized"]
    results["depolarizing_fails_to_normalize"] = not cases[3][1]["normalized"]
    results["locked_not_normalizable"] = not cases[4][1]["normalized"]

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.9), constrained_layout=True)
    ax = axes[0]
    colors = [PALETTE["accent"], PALETTE["primary"], PALETTE["good"],
              PALETTE["warn"], PALETTE["muted"]]
    for (label, r), col in zip(cases, colors):
        t = np.arange(len(r["theta_history"])) * DT
        ax.plot(t, r["theta_history"], lw=1.2, color=col, label=label)
    ax.axhline(GATE, color=PALETTE["accent"], ls="--", lw=0.8, label="driver gate")
    ax.axhline(-50, color=PALETTE["good"], ls=":", lw=0.8)
    ax.set_title("(a) Tumor-region theta by intervention")
    ax.set_xlabel("time after establishment"); ax.set_ylabel("region mean theta (mV)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=7,
              frameon=False)

    ax = axes[1]
    labels = [c["label"] for c in results["cases"]]
    dep = [c["post"]["dep_frac"] for c in results["cases"]]
    ypos = np.arange(len(labels))[::-1]
    cols = [PALETTE["good"] if c["normalized"] else PALETTE["accent"] for c in results["cases"]]
    ax.barh(ypos, dep, color=cols, height=0.55)
    ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=7.5)
    ax.axvline(0.2, color=PALETTE["good"], ls="--", lw=1)
    ax.set_xlim(0, 1.05)
    ax.set_title("(b) Final depolarized fraction")
    ax.set_xlabel("fraction of tumor cells depolarized (> -25 mV)")

    fig.savefig(fig_path("fig2_cancer_normalization.png"))
    plt.close(fig)

    path = dump_json("exp2_cancer.json", results)
    print(f"[exp2] results -> {path}")
    for k in ["untreated_tumor_persists", "gj_restore_normalizes",
              "direct_works_without_gj", "depolarizing_fails_to_normalize",
              "locked_not_normalizable"]:
        print(f"  {k}: {results[k]}")
    return results


if __name__ == "__main__":
    main()
