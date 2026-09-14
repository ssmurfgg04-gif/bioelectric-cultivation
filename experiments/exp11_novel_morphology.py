"""EXP11 — Phase A: engineering novel morphologies (body tempering).

THE CULTIVATION CLAIM UNDER TEST: the body's software can be REWRITTEN —
not restored to factory settings (exp1's domain), but given NEW body
plans: a third eye (a novel depolarized organ zone mid-trunk), a novel
cell state (level-4 zones absent from wild-type), segmented ladders,
reversed polarity. All via sparse voltage clamps — the real Levin-layer
intervention modality — with protocols DISCOVERED by CEM search.

THE HONEST STRUCTURE:
  - twoheaded (Durant et al. 2017) is the positive CONTROL: a known
    developmental outcome the machinery must reproduce before any novel
    claim is credited.
  - restorative (corrupted -> wild-type) is the difficulty BASELINE:
    pushing the system back to a known attractor.
  - four novel targets test genuine engineering: reachability (can CEM
    find clamps that get there?), stability (does the theta memory HOLD
    after clamps release — quantized persistence against boundary blur),
    regenerative memory (does the structure survive amputation — the
    local-memory prediction: partial yes, full no), and difficulty
    scaling (settled error vs novel-boundary count).

Pre-registered criteria (falsification ledger):
  A1 REACHABILITY   third_eye and dual_zone settled fidelity >= 0.90
                    (mean over 3 evaluation seeds, after 300 free units).
  A2 STABILITY      settled fidelity decays < 0.05 over the next 200
                    free units (the discrete code holds the novel plan).
  A3 LOCAL MEMORY   partial amputation: novel identity recovers >= 0.60
                    in the regrown region; FULL amputation: lost (<= 0.20)
                    — positional memory is LOCAL; internal novel
                    structures have no archival backup. (Pre-registered
                    as the expected DIRECTIONAL result; either outcome is
                    informative and recorded.)
  A4 SCALING        settled error increases with novel-boundary count
                    (Spearman rho > 0 across the 6-target family).
  A5 CONTROLS       twoheaded >= 0.90 (the Levin anchor) and restorative
                    >= 0.95 (restoration is easier than engineering).
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, ".")

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morpho_engineering import (
    NOVEL_TARGETS, ClampProtocol, LatchingCollective, anchor_corrupted,
    discrete_fidelity, discover_protocol, evaluate_protocol,
    novel_boundary_count, regeneration_test, target_wildtype,
    target_third_eye, LEVELS,
)
from cultivation.bioelectric.morphospace import twoheaded_target
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

STATE_PATH = "scripts_dev/exp11_state.json"
EVAL_SEEDS = (1, 2, 3)


def target_twoheaded(n: int = 100) -> np.ndarray:
    return twoheaded_target(n)


# each entry: (target_fn, start_anchor_fn or None)
TARGETS = {
    "restorative": (target_wildtype, anchor_corrupted),  # deep: memory itself diseased
    "twoheaded": (target_twoheaded, None),   # Levin anchor: known outcome
    "third_eye": (target_third_eye, None),   # novel organ zone
    "dual_zone": (NOVEL_TARGETS["dual_zone"], None),  # novel cell STATE
    "ladder": (NOVEL_TARGETS["ladder"], None),        # many boundaries
    "mirror": (NOVEL_TARGETS["mirror"], None),        # polarity inversion
}


def main(stage: str = "all") -> dict:
    setup()
    t0 = time.time()
    state = {}
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            state = json.load(f)

    wt = target_wildtype(100)

    # ------------------------------------------------- 1. per-target searches
    if stage in ("search", "all"):
        for name, (tfn, afn) in TARGETS.items():
            if name in state.get("discovered", {}):
                print(f"  [skip] {name} already discovered")
                continue
            target = tfn(100)
            start_anchor = afn(100) if afn else None
            print(f"  discovering protocol for '{name}' "
                  f"({novel_boundary_count(target, wt)} novel cells)...")
            t1 = time.time()
            best_u, best_fid, hist = discover_protocol(
                target, seed=0, start_anchor=start_anchor)
            fids = [evaluate_protocol(best_u, target, seed=s,
                                      start_anchor=start_anchor)["fid_settled"]
                    for s in EVAL_SEEDS]
            state.setdefault("discovered", {})[name] = {
                "u": [float(v) for v in best_u],
                "search_fid": float(best_fid),
                "val_fids": [float(f) for f in fids],
                "val_mean": float(np.mean(fids)),
                "novel_cells": novel_boundary_count(target, wt),
                "search_s": time.time() - t1,
            }
            with open(STATE_PATH, "w") as f:
                json.dump(state, f, default=float)
            print(f"    settled fidelity (seeds {EVAL_SEEDS}): "
                  f"{np.mean(fids):.3f}  ({time.time() - t1:.0f}s)")
        if stage == "search":
            return state

    # ------------------------------------------------ 2. stability trajectories
    print("  stability: fidelity trajectory after release (500 free units)...")
    for name, (tfn, afn) in TARGETS.items():
        if name in state.get("stability", {}):
            continue
        target = tfn(100)
        start_anchor = afn(100) if afn else None
        u = np.array(state["discovered"][name]["u"])
        r = evaluate_protocol(u, target, seed=1, settle=500.0,
                              start_anchor=start_anchor)
        traj = np.array(r["fid_traj"])  # one record per 10 free units
        state.setdefault("stability", {})[name] = {
            "fid_release": r["fid_release"],
            "fid_settled300": float(traj[30]),
            "fid_final500": float(traj[-1]),
            "decay": float(traj[30] - traj[-1]),
        }
        print(f"    {name:12s}: release {r['fid_release']:.2f} -> "
              f"settled {state['stability'][name]['fid_settled300']:.2f} -> "
              f"final {state['stability'][name]['fid_final500']:.2f} "
              f"(decay {state['stability'][name]['decay']:.3f})")
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, default=float)

    # --------------------------------------------------- 3. regeneration memory
    print("  regenerative memory: amputation of the novel zone...")
    for name in ("twoheaded", "third_eye", "dual_zone"):
        if name in state.get("regen", {}):
            continue
        target = TARGETS[name][0](100)
        u = np.array(state["discovered"][name]["u"])
        rep = regeneration_test(u, target, seed=1)
        state.setdefault("regen", {})[name] = rep
        for arm in ("partial", "full"):
            if arm in rep:
                print(f"    {name:12s} {arm:8s}: recovery "
                      f"{rep[arm]['novel_identity_fraction']}, overshoot "
                      f"{rep[arm]['overshoot_fraction']}")
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, default=float)

    # ---------------------------------------------------------- 4. criteria
    disc = state["discovered"]
    stab = state["stability"]
    regen = state.get("regen", {})
    names = list(TARGETS)

    nb = [disc[n]["novel_cells"] for n in names]
    err = [1.0 - disc[n]["val_mean"] for n in names]
    rho, p = spearmanr(nb, err)

    third_eye = disc["third_eye"]["val_mean"]
    dual_zone = disc["dual_zone"]["val_mean"]
    criteria = {
        "A1_reachability": bool(third_eye >= 0.90 and dual_zone >= 0.90),
        "A2_stability": bool(max(stab[n]["decay"] for n in names) < 0.05),
        "A3_local_memory": bool(
            regen.get("third_eye", {}).get("partial", {}).get(
                "novel_identity_fraction", 0) >= 0.60
            and regen.get("third_eye", {}).get("full", {}).get(
                "novel_identity_fraction", 1) <= 0.20),
        "A4_scaling": bool(rho > 0),
        "A5_controls": bool(
            disc["twoheaded"]["val_mean"] >= 0.90
            and disc["restorative"]["val_mean"] >= 0.95),
    }

    results = {
        "discovered": {n: disc[n] for n in names},
        "stability": stab,
        "regen": regen,
        "scaling": {"novel_cells": nb, "settled_error": err,
                    "spearman_rho": float(rho), "p": float(p)},
        "criteria": criteria,
        "eval_seeds": list(EVAL_SEEDS),
    }

    print(f"\n  scaling: rho={rho:.2f} (p={p:.3f}) "
          f"[novel cells {dict(zip(names, nb))}]")
    for k, v in criteria.items():
        print(f"  {k}: {'PASS' if v else 'NEGATIVE'}")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.6), constrained_layout=True)

    ax = axes[0]
    target = target_third_eye(100)
    u = np.array(disc["third_eye"]["u"])
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
    ax.set_title(f"(a) Third eye: engineered vs wild-type\n"
                 f"fidelity {disc['third_eye']['val_mean']:.2f}")
    ax.set_xlabel("position (cells)"); ax.set_ylabel("Vmem (mV)")
    ax.legend(frameon=False, fontsize=7)

    ax = axes[1]
    for name, (tfn, afn) in TARGETS.items():
        u = np.array(disc[name]["u"])
        r = evaluate_protocol(u, tfn(100), seed=1, settle=500.0,
                              start_anchor=afn(100) if afn else None)
        ax.plot(np.arange(len(r["fid_traj"])) * 1.0, r["fid_traj"], lw=1.4,
                label=f"{name} ({disc[name]['val_mean']:.2f})")
    ax.set_title("(b) Persistence after clamp release")
    ax.set_xlabel("free time after release"); ax.set_ylabel("discrete fidelity")
    ax.set_ylim(0, 1.02); ax.legend(frameon=False, fontsize=6.5)

    ax = axes[2]
    ax.scatter(nb, err, s=60, color=PALETTE["primary"])
    for n, x, y in zip(names, nb, err):
        ax.annotate(n, (x, y), fontsize=6.5, xytext=(4, 4),
                    textcoords="offset points")
    ax.set_title(f"(c) Difficulty scaling (rho={rho:.2f})")
    ax.set_xlabel("novel cells (level-different from wild-type)")
    ax.set_ylabel("settled error (1 - fidelity)")

    ax = axes[3]
    regen_names = [n for n in ("twoheaded", "third_eye", "dual_zone")
                   if n in regen and "partial" in regen[n]]
    x = np.arange(len(regen_names))
    w = 0.35
    part = [regen[n]["partial"]["novel_identity_fraction"] for n in regen_names]
    full = [regen[n]["full"]["novel_identity_fraction"] for n in regen_names]
    ax.bar(x - w / 2, part, w, color=PALETTE["good"], label="partial amputation")
    ax.bar(x + w / 2, full, w, color=PALETTE["accent"], label="full amputation")
    ax.set_xticks(x); ax.set_xticklabels(regen_names, fontsize=8)
    ax.set_title("(d) Regenerative memory of novel zones")
    ax.set_ylabel("novel identity recovered")
    ax.legend(frameon=False, fontsize=7)

    fig.savefig(fig_path("fig11_novel_morphology.png"))
    plt.close(fig)

    results["honest_notes"] = [
        "All protocols are DISCOVERED (CEM over clamp position/width/voltage/"
        "duration/junction-scaling), not hand-designed — the same inverse-"
        "design stance as exp10.",
        "The two-headed worm (Durant 2017) is the Levin-lab anchor: the "
        "machinery must reproduce a KNOWN reprogramming outcome before novel "
        "targets count as evidence.",
        "Stability mechanism: the novel plan persists in the DISCRETE code — "
        "theta-boundary blur below half a level-spacing is invisible to "
        "downstream decoding; blur accumulates as sqrt(mu t).",
        "Regenerative memory is LOCAL in the sequential-inheritance model: "
        "partial amputation re-extends the novel identity from surviving "
        "cells (with overshoot — the when-to-stop problem), full amputation "
        "loses it: no archival backup for internal novel structures. This is "
        "the body-teming bottleneck the codec archive (exp8) does not solve "
        "for NON-DEFAULT patterns — the target template is the missing piece.",
    ]

    path = dump_json("exp11_novel_morphology.json", results)
    print(f"[exp11] results -> {path}  ({time.time() - t0:.0f}s)")
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["search", "all"])
    args = ap.parse_args()
    main(stage=args.stage)
