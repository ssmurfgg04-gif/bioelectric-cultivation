"""Bioelectric pattern-fidelity maintenance: an AI-Scientist experiment template.

Grounded in the bioelectric-cultivation framework: a cohort of coupled
bioelectric cell-state attractors is driven through a century of aging
(quantization noise, state jumps, cell death with bystander broadcast).
A novel morphology (a body-part voltage pattern that exists only in somatic
memory, not the genomic archive) is written in early life, then a
maintenance codec tries to HOLD it against decay. Mortality is scored
against the CURRENT (novel) target: an animal is not sick for differing
from its birth pattern.

Arms:
  none                no maintenance (the decay baseline)
  archive             codec referenced to the genomic archive (the erasure
                      hazard: repairs novel tissue back to factory default)
  anchored_protected  codec referenced to somatic memory + protected tier
                      (the known-good hand policy)
  adaptive_policy     THE EXPLORATION ARM: configurable maintenance policy
                      (cadence schedule, budget, write timing) — edit the
                      POLICY knobs below to test ideas.

Metrics: median lifespan, I_recoverable at age 60 and 100 (how much of the
written pattern is recoverable), codec restoration counts.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.environ.get("CULTIVATION_ROOT",
                      "/home/z/my-project/bioelectric-cultivation")
sys.path.insert(0, REPO)

from cultivation.bioelectric.fidelity import FidelityCodec  # noqa: E402
from experiments import exp17_anchored_target as E17        # noqa: E402

# ---------------------------------------------------------------- knobs ----
SEEDS = [21, 22, 23]
YEARS = 120.0

# The write event (early-life reprogramming of the novel zone)
WRITE_AGE = 5.0
WRITE_VAL = -10.0

# The maintenance policy (edit these to explore)
POLICY = {
    "from_age": 30.0,     # age when maintenance starts
    "checkup": 5.0,       # base maintenance cadence (yr)
    "budget": 6,          # cells restored per maintenance cycle
    "schedule": "fixed",  # "fixed" | "adaptive" (cadence relaxes with age)
    "adaptive_growth": 1.6,  # interval multiplier per 50 yr of age
}

ARMS = ("none", "archive", "anchored_protected", "adaptive_policy")

LEDGER_AT = np.arange(10.0, YEARS + 1, 10.0)


def _next_check(t: float, pol: dict) -> float:
    if pol["schedule"] == "adaptive":
        interval = pol["checkup"] * (1.0 + pol["adaptive_growth"]
                                     * max(t - pol["from_age"], 0.0) / 50.0)
        return interval
    return pol["checkup"]


def run_one(arm: str, seed: int) -> dict:
    protect = arm in ("anchored_protected", "adaptive_policy")
    ch = E17.build(seed, WRITE_VAL, protect=protect)
    codec = None
    if arm != "none":
        codec = FidelityCodec(
            n_cells=E17.N_CELLS, budget_per_cycle=POLICY["budget"],
            levels=7,
            target_source=("archive" if arm == "archive" else "anchored"))

    written = {"done": False}
    seen = set()
    series = {"t": [], "I_rec": []}
    next_check = {"t": POLICY["from_age"]}

    def maintain(t, cohort):
        if not written["done"] and t >= WRITE_AGE:
            written["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, E17.ZONE] = True
            cohort.theta = np.where(do, WRITE_VAL, cohort.theta)
            cohort.V = np.where(do, WRITE_VAL, cohort.V)
            if hasattr(cohort, "on_write"):
                cohort.on_write(do)
        if codec is not None and t >= next_check["t"] - 1e-9:
            next_check["t"] = t + _next_check(t, POLICY)
            codec.maintain(cohort, E17.age_preset(t), mode="codec")
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                led = cohort.pattern_ledger(ref=E17.NOVEL_TARGET,
                                            zone=E17.ZONE)
                series["t"].append(float(a))
                series["I_rec"].append(led["I_recoverable"])

    s = ch.run(years=YEARS, dt=0.25, intervention=maintain)
    s["I_rec_t"] = series["t"]
    s["I_rec"] = series["I_rec"]
    s["ledger"] = ({"cycles": codec.cycles, "restored": codec.restored}
                   if codec else None)
    return s


def _at(rows, age) -> float:
    vals = []
    for r in rows:
        if r["I_rec_t"]:
            m = np.asarray(r["I_rec_t"]) if isinstance(r["I_rec_t"], list) else r["I_rec_t"]
            m = np.abs(np.asarray(r["I_rec_t"]) - age) < 0.2
            if m.any():
                vals.append(float(np.mean(np.asarray(r["I_rec"])[m])))
    return float(np.mean(vals)) if vals else float("nan")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=str, default="run_0")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    final_infos = {}
    for arm in ARMS:
        rows = [run_one(arm, s) for s in SEEDS]
        final_info_dict = {
            "median_lifespan": [float(r["median_lifespan"]) for r in rows],
            "I_recoverable_at_60": [_at([r], 60.0) for r in rows],
            "I_recoverable_at_100": [_at([r], 100.0) for r in rows],
            "restored": ([float(r["ledger"]["restored"]) for r in rows]
                         if rows[0]["ledger"] else [0.0] * len(rows)),
        }
        means = {f"{k}_mean": float(np.mean(v))
                 for k, v in final_info_dict.items()}
        stderrs = {f"{k}_stderr": float(np.std(v) / np.sqrt(len(v)))
                   for k, v in final_info_dict.items()}
        final_infos[arm] = {"means": means, "stderrs": stderrs,
                            "final_info_dict": final_info_dict}
        # survival curve of the median seed for the figure
        final_infos[arm]["hist"] = {
            "t": [float(x) for x in rows[0]["hist_t"]],
            "alive": [float(x) for x in rows[0]["hist_alive"]],
            "I_rec_t": [float(x) for x in rows[0]["I_rec_t"]],
            "I_rec": [float(x) for x in rows[0]["I_rec"]],
        }
        print(f"{arm:20s} median={means['median_lifespan_mean']:6.1f} "
              f"I_rec@60={means['I_recoverable_at_60_mean']:5.3f} "
              f"I_rec@100={means['I_recoverable_at_100_mean']:5.3f} "
              f"restored={means['restored_mean']:6.0f}")

    with open(os.path.join(args.out_dir, "final_info.json"), "w") as f:
        json.dump(final_infos, f, indent=1)

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    colors = {"none": "0.6", "archive": "#c44e52",
              "anchored_protected": "#55a868", "adaptive_policy": "#4c72b0"}
    for arm in ARMS:
        d = final_infos[arm]["hist"]
        ax[0].plot(d["I_rec_t"], d["I_rec"], color=colors[arm], lw=2.0,
                   label=arm)
    ax[0].set(xlabel="age (yr)", ylabel="I_recoverable (novel pattern)",
              ylim=(0, 1.05), title="written-pattern recoverability")
    ax[0].legend(fontsize=8)
    meds = [final_infos[a]["means"]["median_lifespan_mean"] for a in ARMS]
    errs = [final_infos[a]["stderrs"]["median_lifespan_stderr"]
            for a in ARMS]
    ax[1].bar(range(len(ARMS)), meds, yerr=errs,
              color=[colors[a] for a in ARMS], capsize=3)
    ax[1].set_xticks(range(len(ARMS)))
    ax[1].set_xticklabels(ARMS, rotation=20, fontsize=8)
    ax[1].set(ylabel="median lifespan (yr)",
              title="mortality vs the current target")
    fig.suptitle("bioelectric pattern-fidelity maintenance", fontsize=12)
    fig.savefig(os.path.join(args.out_dir, "figure.png"), dpi=150)
    plt.close(fig)

    with open(os.path.join(args.out_dir, "notes.txt"), "w") as f:
        f.write(
            "figure.png, left panel: I_recoverable (fraction of the written "
            "novel pattern recoverable from somatic memory) vs age for each "
            "arm. 'archive' shows the erasure hazard — archive-referenced "
            "repair actively erases the novel pattern. 'none' is pure decay. "
            "'anchored_protected' is the known-good hand policy. "
            "'adaptive_policy' is the configurable exploration arm.\n"
            "figure.png, right panel: median lifespan per arm (error bars = "
            "SE over seeds), mortality scored against the CURRENT (novel) "
            "target, so an animal is not sick for differing from its birth "
            "pattern.\n")


if __name__ == "__main__":
    main()
