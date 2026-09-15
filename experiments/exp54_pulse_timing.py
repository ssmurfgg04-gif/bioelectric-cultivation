#!/usr/bin/env python3
"""exp54 — PULSE-TIMING CRITICAL WINDOW (night-eight queue #1; ledger L35).

LITERATURE BASIS (exp53 wave, research/NIGHT_EIGHT_SYNTHESIS.md):

  Durant et al. 2019 (MED30799071, Biophys J — the directive's "3h window"
  paper; its PMID was mis-cited, the record is verified): depolarizing the
  injured tissue during the FIRST 3 h of regeneration alters gene
  expression by 6 h and produces a double-headed phenotype DESPITE
  confirmed washout — "resting membrane potential taking place within the
  first 3 h after injury kick-starts the downstream pattern". The
  transcriptional faces are demarcated BY 6 h.

  ZENODO:18358611 (coupling response geometry): response curves across
  perturbation strength / exposure time / fragment position share a
  fixed structural form — saturation plateau, onset/closure point, finite
  transition width — and LATE perturbations fail regardless of strength.

MODEL MAPPING. The model's decision medium is the commitment walk: each
committing cell reads theta[src] (the last committed cell), and the wound
face's state reaches the chain only at the walk's start (direct chain
read) plus a diffusive leak thereafter (the face is clamped, the last
committed cell sits adjacent in the lattice). Prediction: the stored
identity shift DECAYS with pulse start time — early pulses ride the
chain, late pulses meet a chain that has already moved past the face.

PRE-REGISTERED GATES (fixed BEFORE the arms ran):

  PT-G1  FIXED-SHAPE CURVE (structural form, ZENODO:18358611):
         (a) shift(start) is monotone NON-INCREASING in start time
             (seed means);
         (b) an early SATURATION PLATEAU exists: shift(0) >= 0.90 x
             max over the scan;
         (c) LATE FAILURE: shift at the latest start still inside the
             walk (start = walk_span - 3h) < 25% of shift(0);
         (d) FINITE transition width: the 90%-to-10% drop span is
             > 0 and < the full walk span (a measured width, not a step
             and not a flat curve).
  PT-G2  3H SUFFICIENCY (MED30799071): a pulse covering the first 3 h
         writes >= 80% of what a 6 h pulse writes (start = 0 both).
  PT-G3  6H DEADLINE: a 3h pulse STARTING at 6h writes < 50% of the
         start-0 3h pulse; a pulse starting AT/after the walk end is
         cone-bounded like the intact case (< 10% of start-0).
  PT-G4  PERSISTENCE + BLOCKADE (exp49 contrasts re-checked at the new
         timing): the start-0 3h write persists >= 1.0 mV mean after the
         15h post-settle, and collapses under gap_scale=0.05 to < 10%
         of the coupled value.
  PT-G5  SIZE COLLAPSE (fixed-shape across the fragment axis): with
         start and duration normalized by each fragment's own walk span,
         the normalized curves at n in {60, 100, 140} correlate
         Spearman rho >= 0.9 pairwise.

RUN PROTOCOL: seeds (1,2,3); n=100 primary; regen slice 0.85..1.0
(15 cells, tail; walk span 12h); wound face = cell 84; pulse_v = 0.0;
settle 24h; cell_period 0.8; dt 0.1; post 15h. Primary scan: start in
{0, 1, 2, 3, 4, 6, 8, 10, 12} h, dur 3h. Duration arms: dur in {3, 6}
at start 0. Blocked arm: gap_scale 0.05, start 0, dur 3h. Size axis:
n in {60, 100, 140} with regen slice 0.85..1.0 (9/15/21 cells), dur =
25% of walk span, starts on a normalized grid mapped to hours. Serial,
BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.cognitive.lightcone import (  # noqa: E402
    regen_pulse_timing,
    measure_lightcone,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp54_pulse_timing.json")

SEEDS = (1, 2, 3)


def main() -> None:
    print("=== exp54: pulse-timing critical window ===\n")
    res: dict = {"exp": "exp54_pulse_timing", "arms": {}}

    # ---- primary start-time scan (n=100, dur=3h) -----------------------
    starts = [0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0]
    scan: dict[float, list[float]] = {}
    far: dict[float, list[float]] = {}
    for s in starts:
        vals, fars = [], []
        for seed in SEEDS:
            r = regen_pulse_timing(seed, start_hours=s, pulse_hours=3.0)
            vals.append(r["mean_shift_in_regen_mv"])
            fars.append(r["far_end_residue_mv"])
        scan[s] = vals
        far[s] = fars
        print(f"  start={s:5.1f}h  mean_shift={np.mean(vals):6.3f} mV "
              f"(seeds {[round(v,2) for v in vals]})")
    res["arms"]["scan_dur3h"] = {
        str(s): {"mean_shift_seeds": scan[s],
                 "mean_shift": float(np.mean(scan[s])),
                 "far_end_seeds": far[s]} for s in starts}
    curve = [float(np.mean(scan[s])) for s in starts]

    # ---- duration comparison at start=0 (PT-G2) ------------------------
    dur_vals = {}
    for d in (3.0, 6.0):
        vals = [regen_pulse_timing(seed, start_hours=0.0, pulse_hours=d)
                ["mean_shift_in_regen_mv"] for seed in SEEDS]
        dur_vals[d] = float(np.mean(vals))
        print(f"  dur={d:.0f}h @ start 0  mean_shift={dur_vals[d]:.3f} mV")
    res["arms"]["dur_comparison"] = {
        str(d): {"mean_shift": v, "seeds": None}
        for d, v in dur_vals.items()}

    # ---- blocked arm (PT-G4) -------------------------------------------
    blocked = [regen_pulse_timing(seed, start_hours=0.0, pulse_hours=3.0,
                                  gap_scale=0.05)["mean_shift_in_regen_mv"]
               for seed in SEEDS]
    print(f"  blocked (gap 0.05) start 0: {np.mean(blocked):.3f} mV")
    res["arms"]["blocked"] = {
        "mean_shift": float(np.mean(blocked)),
        "seeds": blocked}

    # ---- size collapse axis (PT-G5) ------------------------------------
    # normalized grid: dur = 25% of walk span; starts at fractions.
    frac_grid = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
    size_curves: dict[int, list[float]] = {}
    size_walk: dict[int, float] = {}
    for n in (60, 100, 140):
        L = n - int(n * 0.85)                       # regen cells
        walk_span = L * 0.8
        dur = 0.25 * walk_span
        curve_n: list[float] = []
        for f in frac_grid:
            s = f * walk_span
            # for n=100 keep continuity with the primary scan where f maps
            # onto the same hours (not required; independent arm)
            vals = [regen_pulse_timing(seed, n=n, start_hours=s,
                                       pulse_hours=dur)
                    ["mean_shift_in_regen_mv"] for seed in SEEDS]
            curve_n.append(float(np.mean(vals)))
        size_curves[n] = curve_n
        size_walk[n] = walk_span
        print(f"  n={n} (walk {walk_span:.1f}h, dur {dur:.2f}h): "
              f"{[round(v, 2) for v in curve_n]}")
    res["arms"]["size_collapse"] = {
        str(n): {"walk_span_hours": size_walk[n],
                 "frac_grid": frac_grid,
                 "curve": size_curves[n]} for n in size_curves}

    # ================= GATES =================
    gates: dict[str, dict] = {}

    # PT-G1 fixed-shape curve
    mx = max(curve)
    drops = [(s, c) for s, c in zip(starts, curve)]
    monotone_ok = all(curve[i] >= curve[i + 1] - 0.05
                      for i in range(len(curve) - 1))
    plateau_ok = curve[0] >= 0.90 * mx
    # latest grid start whose 3h pulse still ends inside the 12h walk
    late_start = max(s for s in starts if s + 3.0 <= 12.0)
    late_idx = starts.index(late_start)
    late_ok = curve[late_idx] < 0.25 * curve[0]
    # 90%->10% width in hours (linear interp on the descending curve)
    hi = 0.9 * mx
    lo = 0.1 * mx
    s90 = s10 = None
    for i in range(len(curve) - 1):
        a0, a1 = curve[i], curve[i + 1]
        if s90 is None and a0 >= hi >= a1:
            s90 = starts[i] + (a0 - hi) / max(a0 - a1, 1e-9) \
                * (starts[i + 1] - starts[i])
        if s90 is not None and a0 >= lo >= a1:
            s10 = starts[i] + (a0 - lo) / max(a0 - a1, 1e-9) \
                * (starts[i + 1] - starts[i])
            break
    width = (s10 - s90) if (s90 is not None and s10 is not None) else None
    width_ok = width is not None and 0.0 < width < 12.0
    gates["PT-G1"] = {
        "verdict": "PASS" if (monotone_ok and plateau_ok and late_ok
                              and width_ok) else "REFUTED",
        "monotone_nonincreasing": monotone_ok,
        "early_plateau_shift0_ge_0.9max": plateau_ok,
        "late_failure_lt_0.25x": late_ok,
        "late_value_mv": curve[late_idx],
        "finite_width_hours": width,
        "width_ok": width_ok,
        "curve": {str(s): c for s, c in drops},
    }

    # PT-G2 3h sufficiency
    ratio = dur_vals[3.0] / max(dur_vals[6.0], 1e-9)
    gates["PT-G2"] = {
        "verdict": "PASS" if ratio >= 0.80 else "REFUTED",
        "shift_3h": dur_vals[3.0], "shift_6h": dur_vals[6.0],
        "ratio": ratio,
    }

    # PT-G3 6h deadline
    shift0 = curve[0]
    shift6 = curve[starts.index(6.0)]
    post_walk_start = 12.0                       # pulse begins at walk end
    shift12 = curve[starts.index(12.0)]
    g3a = shift6 < 0.5 * shift0
    g3b = shift12 < 0.10 * shift0
    gates["PT-G3"] = {
        "verdict": "PASS" if (g3a and g3b) else "REFUTED",
        "shift_start6_mv": shift6, "lt_50pct_of_start0": g3a,
        "shift_start12_mv": shift12, "lt_10pct_of_start0": g3b,
    }

    # PT-G4 persistence + blockade
    persist = curve[0] >= 1.0                    # post-settled mean shift
    blocked_mean = float(np.mean(blocked))
    collapse = blocked_mean < 0.10 * shift0
    gates["PT-G4"] = {
        "verdict": "PASS" if (persist and collapse) else "REFUTED",
        "settled_shift_start0_mv": shift0, "persists_ge_1mv": persist,
        "blocked_mean_mv": blocked_mean,
        "blocked_lt_10pct": collapse,
    }

    # PT-G5 size collapse
    rhos = {}
    ns = sorted(size_curves)
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            r, _ = spearmanr(size_curves[ns[i]], size_curves[ns[j]])
            rhos[f"{ns[i]}v{ns[j]}"] = float(r)
    g5 = all(v >= 0.9 for v in rhos.values())
    gates["PT-G5"] = {
        "verdict": "PASS" if g5 else "REFUTED",
        "pairwise_spearman": rhos,
    }

    res["gates"] = gates
    n_pass = sum(1 for g in gates.values() if g["verdict"] == "PASS")
    res["summary"] = f"{n_pass}/{len(gates)} gates PASS"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"\nGATES: {res['summary']}")
    for k, g in gates.items():
        print(f"  {k}: {g['verdict']}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
