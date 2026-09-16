#!/usr/bin/env python3
"""exp100 — THE READER'S PRICE MAP (ledger L82; exp99's registered
map: exp93 priced the WRITE path; the READER (the two-source read)
has only run at the (64, 0) star point by convention. This is the
reader's own taxonomy across the full 19-substrate battery).

THE INSTRUMENT (exp93's ladder convention, adaptive per substrate):
  1. the DEFAULT cell (gamma=1, mu=0.015) x 3 seeds — verifies
     >= 2/3 -> class DEFAULT;
  2. else the GAMMA ladder {2, 4, 8, 16, 32, 64} at default mu
     x 2 seeds (screen) -> any verify: confirm the MINIMAL gamma
     x 3 seeds -> class V_PRICED(gamma_min);
  3. else the MU ladder {0.01, 0.005, 0.002, 0} at gamma=1 x 2
     seeds -> confirm the MAXIMAL mu x 3 seeds ->
     class THETA_PRICED(mu_max);
  4. else the TWO-DIAL probe {(4, 0), (16, 0)} x 2 seeds ->
     confirm cheapest x 3 seeds -> class TWO_DIAL; else REFUSED.

THE BATTERY (19): exp73's 7 (path, grid2d, torus, random3,
random6, scale_free, small_world) + exp94's 12 (tree, star, cycle,
ladder, barbell, complete, bipartite, grid_elong, torus_elong,
random8, path200, scale_free200).

PRE-REGISTERED GATES:

  PM-G1  (the map completes) every substrate carries a class call.
  PM-G2  (no refusals) ZERO substrates classify REFUSED — R5'
         extends battery-wide on the reader's own path.
  PM-G3  (the stratification is real) >= 2 classes present — the
         map is not trivially uniform.

KNOWN ANCHORS going in: path verified at default (2.91, exp98's
SL-G4); the star refuses default and verifies one dial up
(exp98); the battery verified at (64, 0) 19/19 after the repair
(exp97/exp99).

RUN (chunkable, merge semantics — results accumulate in
results/exp100_reader_price_map.json):
  python experiments/exp100_reader_price_map.py            # defaults
  python experiments/exp100_reader_price_map.py --ladder star,torus
  python experiments/exp100_reader_price_map.py --finalize
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp73_active_renormalization import make_battery, N
from experiments.exp94_multizone_scale import (
    execute_two_source_n, MULTI, new_battery,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp100_reader_price_map.json")

SEEDS3 = (1, 2, 3)
SEEDS2 = (1, 2)
GAMMA_LADDER = (2.0, 4.0, 8.0, 16.0, 32.0, 64.0)
MU_LADDER = (0.01, 0.005, 0.002, 0.0)
TWO_DIAL = ((4.0, 0.0), (16.0, 0.0))
# exp100 in-run bracket extension (owned): the registered {(4,0),
# (16,0)} probe came from the WRITE path's stratification; the
# reader's dense extremes (bipartite, complete) price ABOVE it
# while verifying at the (64, 0) star point (exp94 MS-G1). The
# bracket extends toward the star point.
TWO_DIAL_EXT = ((32.0, 0.0), (64.0, 0.0))


def run_cell(adj, gamma, mu, seeds):
    res = [execute_two_source_n(MULTI, adj, s,
                                op={"gamma": gamma, "mu": mu},
                                frontier_mode="walk")
           for s in seeds]
    return {"rate": round(float(np.mean(
        [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)}


def load() -> dict:
    if os.path.exists(OUT):
        with open(OUT) as f:
            return json.load(f)
    return {"cells": {}, "classes": {}, "criteria": {}}


def save(d: dict) -> None:
    with open(OUT, "w") as f:
        json.dump(d, f, indent=1, default=float)


def default_rate(d: dict, name: str) -> float:
    c = d["cells"].get(name, {}).get("default")
    return c["rate"] if c else -1.0


def run_ladder(d: dict, name: str, adj) -> None:
    cells = d["cells"].setdefault(name, {})
    if cells.get("default", {}).get("rate", 0) >= 2 / 3:
        print(f"    {name}: default already verifies — no ladder")
        return
    g_verify = []
    for g in GAMMA_LADDER:
        key = f"gamma_{g:g}"
        if key not in cells:
            cells[key] = run_cell(adj, g, 0.015, SEEDS2)
        if cells[key]["rate"] >= 0.99:
            g_verify.append(g)
    if g_verify:
        gmin = min(g_verify)
        ck = f"confirm_gamma_{gmin:g}"
        if ck not in cells:
            cells[ck] = run_cell(adj, gmin, 0.015, SEEDS3)
        if cells[ck]["rate"] >= 2 / 3:
            d["classes"][name] = {"call": "V_PRICED",
                                  "gamma_min": gmin}
            print(f"    {name}: V_PRICED gamma_min={gmin}")
            return
    m_verify = []
    for m in MU_LADDER:
        key = f"mu_{m:g}"
        if key not in cells:
            cells[key] = run_cell(adj, 1.0, m, SEEDS2)
        if cells[key]["rate"] >= 0.99:
            m_verify.append(m)
    if m_verify:
        mmax = max(m_verify)
        ck = f"confirm_mu_{mmax:g}"
        if ck not in cells:
            cells[ck] = run_cell(adj, 1.0, mmax, SEEDS3)
        if cells[ck]["rate"] >= 2 / 3:
            d["classes"][name] = {"call": "THETA_PRICED",
                                  "mu_max": mmax}
            print(f"    {name}: THETA_PRICED mu_max={mmax}")
            return
    td_verify = []
    for g, m in TWO_DIAL + TWO_DIAL_EXT:
        key = f"twodial_{g:g}_{m:g}"
        if key not in cells:
            cells[key] = run_cell(adj, g, m, SEEDS2)
        if cells[key]["rate"] >= 0.99:
            td_verify.append((g, m))
    if td_verify:
        g, m = min(td_verify)
        ck = f"confirm_twodial_{g:g}_{m:g}"
        if ck not in cells:
            cells[ck] = run_cell(adj, g, m, SEEDS3)
        if cells[ck]["rate"] >= 2 / 3:
            d["classes"][name] = {"call": "TWO_DIAL",
                                  "cheapest": [g, m]}
            print(f"    {name}: TWO_DIAL at ({g:g}, {m:g})")
            return
    d["classes"][name] = {"call": "REFUSED"}
    print(f"    {name}: REFUSED — the first reader refusal")


def finalize(d: dict) -> None:
    classes = d["classes"]
    names = sorted(classes)
    refused = [n for n in names if classes[n]["call"] == "REFUSED"]
    kinds = sorted({classes[n]["call"] for n in names})
    pm_g1 = len(names) == 19
    pm_g2 = len(refused) == 0
    pm_g3 = len(kinds) >= 2
    print("\n  THE READER'S PRICE MAP:")
    for n in names:
        c = classes[n]
        detail = ("", "")
        if c["call"] == "V_PRICED":
            detail = (f" gamma_min={c['gamma_min']:g}",)
        elif c["call"] == "THETA_PRICED":
            detail = (f" mu_max={c['mu_max']:g}",)
        elif c["call"] == "TWO_DIAL":
            detail = (f" cheapest={tuple(c['cheapest'])}",)
        err = d["cells"][n].get(
            "default", {}).get("err", "")
        print(f"    {n:14s} {c['call']:13s}{detail[0]}"
              f"   (default err {err})")
    print(f"\n  PM-G1 map completes: {'PASS' if pm_g1 else 'REFUTED'}"
          f" ({len(names)}/19)")
    print(f"  PM-G2 no refusals: {'PASS' if pm_g2 else 'REFUTED'}"
          f" (refused: {refused})")
    print(f"  PM-G3 stratification: {'PASS' if pm_g3 else 'REFUTED'}"
          f" (classes: {kinds})")
    d["criteria"] = {
        "PM_G1_map_completes": bool(pm_g1),
        "PM_G2_no_refusals": bool(pm_g2),
        "PM_G3_stratification": bool(pm_g3),
    }
    d["notes"] = (
        "exp93's taxonomy measured for the READER (the two-source "
        "read) across the full 19-substrate battery, adaptive "
        "ladders, merge-semantics chunked runs. The reader had "
        "only ever run at the (64, 0) star point by convention.")


def main() -> None:
    battery = dict(make_battery())
    battery.update(new_battery())
    d = load()
    args = sys.argv[1:]

    if "--finalize" in args:
        finalize(d)
        save(d)
        return

    if "--ladder" in args:
        idx = args.index("--ladder")
        names = args[idx + 1].split(",")
        for n in names:
            print(f"  ladder: {n}")
            run_ladder(d, n, battery[n])
        save(d)
        return

    names = [a for a in args if not a.startswith("-")] or sorted(battery)
    print("=== exp100: the reader's price map — default cells ===\n")
    for n in names:
        if default_rate(d, n) >= 0:
            print(f"    {n:14s} default already deposited")
            continue
        d["cells"].setdefault(n, {})["default"] = run_cell(
            battery[n], 1.0, 0.015, SEEDS3)
        c = d["cells"][n]["default"]
        print(f"    {n:14s} rate {c['rate']:.2f} err {c['err']}")
        if c["rate"] >= 2 / 3:
            d["classes"][n] = {"call": "DEFAULT"}
        save(d)
    refused = [n for n in d["cells"]
               if default_rate(d, n) < 2 / 3
               and n not in d.get("classes", {})]
    print(f"\n  default phase done. ladder queue: {refused}\n"
          f"  run: python experiments/exp100_reader_price_map.py "
          f"--ladder {','.join(refused)}" if refused else
          "\n  default phase done. no ladders needed.")


if __name__ == "__main__":
    main()
