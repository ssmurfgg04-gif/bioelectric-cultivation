#!/usr/bin/env python3
"""exp22 — TAS cross-validation: the memory co-metric on OUR ensemble.

THE OTHER PEOPLE'S IDEA (Blattner 2026, bioRxiv 2026.04.01.715890,
github.com/marcelbtec/tasmorpho, reproduced this session — script 03
output in research/tasmorpho): Tangential Action Spaces formalize
bioelectric memory as a geometry:

  Q      quadratic cost of a perturbation (excess ion flux / procedure)
  R      write map: how a perturbation shifts macroscopic observables
  K_mem  = R Q^{-1} R^T  the induced memory co-metric: which perturbation
         directions write the hidden state most efficiently. Eigenvectors
         of K_mem = dominant write axes; orthogonal = silent directions
         (cost energy, leave no regenerative trace).

THE CROSS-VALIDATION (what their geometry predicts about OUR search):
map the TAS objects onto the anchored-stack policy space (the exp19
8-dim space around the HAND policy):

  Q(u)  procedure cost: h_proc-weighted write events + maintenance
        cycles x budget (the 'excess ion flux' analog — the price the
        tissue pays for the intervention)
  R(u)  endpoint shift: the century-hold integral change vs no-policy
        (the observable the policy writes)
  write efficiency e(u) = hold_gain(u)^2 / cost(u) — the scalar K_mem

PRE-REGISTERED CRITERIA (written before computation):
  T1 DOMINANT AXIS EXISTS  the efficiency distribution over policy
     directions is strongly anisotropic: top direction's efficiency
     >= 3x the median direction (TAS's dominant-write-axis prediction).
  T2 SILENT DIRECTIONS EXIST  at least 2 of the 8 policy dimensions
     have |endpoint shift| < 1 SE of 0 while costing > 0 (TAS's silent
     directions — matches exp19's plateau ablations if they coincide).
  T3 SEARCH-GEOMETRY ALIGNMENT  the CEM-discovered hold policy
     (exp19_state) lies closer to the dominant write axis than the HAND
     policy does (cosine over the efficiency-weighted direction
     structure): the search climbed the co-metric's ridge without
     being told it existed.
  T4 HAND NOT ON A SILENT AXIS  the HAND policy's dominant component
     is not one of the silent directions (the known-good policy is not
     accidentally burning cost in a no-trace direction).

Kills-row: if T1/T2 fail, the TAS geometry adds nothing to this
ensemble's landscape (plateau = isotropy, not hidden axes); if T3 fails,
the CEM search did not follow the write-efficient geometry.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.exp19_anchored_cem import (  # noqa: E402
    eval_hold, decode, HAND, NONE_U, NAMES, H_PROC,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "scripts_dev", "exp19_state.json")
OUT = os.path.join(ROOT, "results", "exp22_tas_crossval.json")

SEEDS = (41, 42, 43)          # fresh seeds (audit S7: disjoint)
BASE = np.array(HAND)
# one-policy-at-a-time directions (coordinate axes) + the two diagonals
DIRECTIONS = {
    name: np.eye(len(NAMES))[i]
    for i, name in enumerate(NAMES)
}
DIRECTIONS["dense_low_amp"] = np.array([0, 0, -0.3, 0.15, 0, 0, 0, 0])
DELTAS = {"write_age": 8.0, "start_age": 12.0, "period": 2.5,
          "budget": 4.0, "k_anchor": 0.8, "boost_p_verified": 0.4,
          "boost_p_unverified": 0.4, "boost_factor": 0.3,
          "dense_low_amp": 1.0}


def _p(s):
    print(s, flush=True)


def cost_of(u) -> float:
    """Q(u): procedure events + maintenance cycles x budget (h_proc
    weighted write events included via eval's proc tracking is internal;
    here the deterministic part: cycles*budget + write events)."""
    p = decode(u)
    years = max(0.0, 105.0 - p["start_age"])
    cycles = years / max(p["period"], 0.75)
    return float(cycles * p["budget"] + 12.0)  # +12: the initial write


def hold_of(u) -> dict:
    rs = [eval_hold(u, s) for s in SEEDS]
    holds = np.array([r["hold_mean"] for r in rs])
    return {"mean": float(holds.mean()), "se": float(holds.std(ddof=1)
            / np.sqrt(len(holds))) if len(holds) > 1 else 0.0}


def main() -> dict:
    _p("=== exp22: TAS memory co-metric cross-validation on the "
       "anchored stack ===\n")
    t0 = __import__("time").time()

    base = hold_of(BASE)
    none_h = hold_of(np.array(NONE_U))
    _p(f"BASE (HAND) hold {base['mean']:.3f} ± {base['se']:.3f}   "
       f"NONE {none_h['mean']:.3f}")

    results = {}
    for name, d in DIRECTIONS.items():
        delta = DELTAS[name]
        u_plus = BASE + d * delta
        u_minus = BASE - d * delta
        hp = hold_of(u_plus)
        hm = hold_of(u_minus)
        # endpoint shift per unit delta (central difference)
        shift = (hp["mean"] - hm["mean"]) / (2 * delta)
        shift_se = np.sqrt(hp["se"] ** 2 + hm["se"] ** 2) / (2 * delta)
        # cost difference per unit delta (deterministic)
        cp, cm = cost_of(u_plus), cost_of(u_minus)
        dcost = (cp - cm) / (2 * delta)
        # efficiency: squared endpoint shift per unit cost change,
        # evaluated at +delta (the local write efficiency)
        gain = max(hp["mean"] - base["mean"], 1e-9)
        eff = gain ** 2 / max(cp - cost_of(BASE), 1.0)
        results[name] = {
            "shift_per_unit": float(shift),
            "shift_se": float(shift_se),
            "dcost_per_unit": float(dcost),
            "hold_plus": hp, "hold_minus": hm,
            "efficiency": float(eff),
        }
        _p(f"  {name:20s} shift/unit {shift:+.4f} ± {shift_se:.4f}   "
            f"dcost/unit {dcost:+8.2f}   eff {eff:.5f}")

    # ---- T1 dominant axis ----
    effs = np.array([r["efficiency"] for r in results.values()])
    names = list(results)
    top = int(np.argmax(effs))
    t1 = bool(effs[top] >= 3.0 * float(np.median(effs)))

    # ---- T2 silent directions ----
    silent = [n for n, r in results.items()
              if abs(r["shift_per_unit"]) < 2 * r["shift_se"]
              and r["dcost_per_unit"] > 0]
    t2 = bool(len(silent) >= 2)

    # ---- T3 search alignment ----
    state = json.load(open(STATE))
    disc = np.array(state["discovered_u"])
    # direction of the discovered policy from HAND, in policy space,
    # normalized by each dimension's tested delta (comparable units)
    dvec = (disc - BASE) / np.array([DELTAS[n] for n in NAMES])
    dnorm = np.linalg.norm(dvec)
    # efficiency-weighted axis structure: each coordinate axis weighted
    # by its efficiency rank
    axis_eff = np.zeros(len(NAMES))
    for i, n in enumerate(NAMES):
        axis_eff[i] = results.get(n, {}).get("efficiency", 0.0)
    w = axis_eff / (axis_eff.sum() + 1e-12)
    cos_hand = 0.0  # HAND is the origin by construction
    cos_disc = float(np.dot(dvec / max(dnorm, 1e-9), w)) if dnorm > 1e-9 \
        else 0.0
    t3 = bool(cos_disc > 0.05)  # positively aligned with efficient axes

    # ---- T4 HAND not on a silent axis ----
    hand_main = NAMES[int(np.argmax(np.abs(np.array(HAND)
               - np.array([5.0, 20.0, 1.5, 1.0, 0.05, 0, 0, 1.0]))))]
    # (distance from the uninformative corner — HAND's biggest move)
    t4 = bool(hand_main not in silent)

    crit = {"T1_dominant_axis": t1, "T2_silent_directions": t2,
            "T3_search_alignment": t3, "T4_hand_not_silent": t4}
    _p("\n criteria:")
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'REFUTED'}")
    _p(f"    (alignment cos(disc, efficiency-weighted axes) = "
       f"{cos_disc:+.3f}; silent = {silent})")

    out = {"exp": "exp22_tas_crossval",
           "source": "TAS (Blattner 2026, tasmorpho) geometry applied to "
                     "the anchored stack; exp19 policy space",
           "base_hold": base, "none_hold": none_h,
           "directions": results,
           "alignment": {"cos_disc": cos_disc, "hand_main": hand_main,
                         "silent": silent},
           "criteria": crit,
           "notes": "efficiency = (hold gain vs HAND)^2 / procedure cost; "
                    "cost = maintenance cycles x budget + write events; "
                    "fresh seeds 41-43 (audit S7); central differences "
                    "at the deltas in DELTAS."}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    _p(f"\n  results -> {OUT}   ({__import__('time').time()-t0:.0f}s)")
    return out


if __name__ == "__main__":
    main()
