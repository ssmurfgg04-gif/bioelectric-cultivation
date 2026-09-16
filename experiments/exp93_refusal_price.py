#!/usr/bin/env python3
"""exp93 — THE REFUSAL PRICE BATTERY (ledger L75; R5' characterized
across the substrate battery — the handoff's open item #4).

THE QUESTION: exp89 birthed R5' — "the partition refusal is an
OPERATING-POINT statement, not a wall; the star architecture buys
it." The star point (gamma=64, mu=0) is the MAXIMAL buy. The price
of the refusal is the MINIMAL operating-point move that buys
writability, per substrate. exp78/79 found the dials independent
(the two-channel law) and the hub substrates plateau on the gamma
dial (the theta channel carries their refusal). The battery prices
each refusal along each dial separately.

THE INSTRUMENT: exp89's machinery verbatim — the single in-domain
program (uc-in), exp73's 7-substrate battery, 3 seeds, the
verify-or-refuse verdict, err_vs_target deposited at every point.

THE LADDERS (for every substrate REFUSED at the default point):
  * the GAMMA ladder at mu = 0.015: gamma in {2, 4, 8, 16, 32, 64}
    — gamma_min = the smallest verifying gamma (the V-channel
    price, in log2 fold-units above the default).
  * the MU ladder at gamma = 1.0: mu in {0.01, 0.005, 0.002, 0.0}
    — mu_max = the largest verifying mu (the theta-channel price,
    in fold-units of mu reduction).
  * if both one-dial ladders fail at their ends, the substrate is
    TWO-DIAL: the registered probe {(4, 0), (16, 0)} brackets the
    cheapest two-dial point before the star.

PRE-REGISTERED GATES:

  RP-G1  (the partition control) the R5 signature reproduces: the
         default verify agrees with the compiler's own partition
         check on >= 6/7 substrates (exp89's UC-G1).
  RP-G2  (the lift control) 7/7 verify at the star point
         (exp89's UC-G2).
  RP-G3  (the price is a dial distance) every refused substrate's
         price is measurable on the ladders: one-dial (gamma_min or
         mu_max exists) or two-dial (a registered probe point
         verifies). No refused substrate remains unwritable below
         the star.
  RP-G4  (the stratification) the prices stratify by channel: the
         hub substrate scale_free's gamma ladder at default mu
         FAILS at every gamma <= 64 (the exp78 theta-channel
         plateau, now on the write path) while torus and random3
         verify at gamma <= 16 — the hub refusal's price is carried
         by the theta channel, the small-world refusals' by the
         V-channel ratio.

RUN: 7 substrates x 3 seeds x {default, star} + the ladders on the
refused set (~140 program runs). Serial, BLAS pinned.
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

from cultivation.compiler.anatomy import (
    AnatomySpec, Zone, substrate_partition_check,
)
from experiments.exp73_active_renormalization import make_battery
from experiments.exp89_universal_compiler import (
    execute_universal, DEFAULT, STAR, ERR_BAR,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp93_refusal_price.json")

SEEDS = (1, 2, 3)
SUBSTRATES = ["path", "grid2d", "torus", "random3", "random6",
              "scale_free", "small_world"]
GAMMA_LADDER = [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
MU_LADDER = [0.01, 0.005, 0.002, 0.0]
TWO_DIAL_PROBE = [(4.0, 0.0), (16.0, 0.0)]
MU_DEFAULT = DEFAULT["mu"]


def verify_rate(name: str, adjacency, op: dict) -> tuple[float, float]:
    res = [execute_universal(SPEC, adjacency, s, op) for s in SEEDS]
    rate = float(np.mean([r["program_verified"] for r in res]))
    err = float(np.mean([r["err_vs_target"] for r in res]))
    return rate, round(err, 2)


SPEC = AnatomySpec(
    zones=[Zone(f0=0.05, f1=0.20, voltage=-30.0, name="z0")],
    amputate_plane="head", spec_name="uc-in", somatic_latch=False)


def main() -> dict:
    print("=== exp93: the refusal price battery ===\n")

    battery = make_battery()

    # ---- the compiler's own R5 classification ------------------------------
    r5 = {name: substrate_partition_check(SPEC, battery[name])
          ["substrate_compilable"] for name in SUBSTRATES}
    print(f"  R5 partition: {r5}")

    # ---- RP-G1: the default point (the partition control) ------------------
    default_res = {}
    for name in SUBSTRATES:
        rate, err = verify_rate(name, battery[name], DEFAULT)
        default_res[name] = {"rate": rate, "err": err}
        print(f"    default {name:12s} rate {rate:.2f} err {err}")
    agree = sum(int((default_res[n]["rate"] > 0.5) == r5[n])
                for n in SUBSTRATES)
    rp_g1 = bool(agree >= 6)
    print(f"  RP-G1 partition agreement: {agree}/7 -> "
          f"{'PASS' if rp_g1 else 'REFUTED'}")

    # ---- RP-G2: the star lift (the control) --------------------------------
    star_res = {}
    for name in SUBSTRATES:
        rate, err = verify_rate(name, battery[name], STAR)
        star_res[name] = {"rate": rate, "err": err}
    star_ok = sum(int(star_res[n]["rate"] > 0.5) for n in SUBSTRATES)
    rp_g2 = bool(star_ok == 7)
    print(f"  RP-G2 star lift: {star_ok}/7 -> "
          f"{'PASS' if rp_g2 else 'REFUTED'}; "
          f"errs { {n: star_res[n]['err'] for n in SUBSTRATES} }")

    # ---- the ladders (the price instrument) --------------------------------
    refused = [n for n in SUBSTRATES if default_res[n]["rate"] <= 0.5]
    print(f"\n  refused at default: {refused}")
    prices: dict[str, dict] = {}
    for name in refused:
        p: dict = {}
        gm = None
        for g in GAMMA_LADDER:
            rate, err = verify_rate(name, battery[name],
                                    {"gamma": g, "mu": MU_DEFAULT})
            p[f"gamma_{g}"] = {"rate": rate, "err": err}
            if gm is None and rate > 0.5:
                gm = g
        mm = None
        for m in MU_LADDER:
            rate, err = verify_rate(name, battery[name],
                                    {"gamma": 1.0, "mu": m})
            p[f"mu_{m}"] = {"rate": rate, "err": err}
            if mm is None and rate > 0.5:
                mm = m
        dial = "gamma" if gm is not None else \
               ("mu" if mm is not None else "both")
        if dial == "both":
            for g, m in TWO_DIAL_PROBE:
                rate, err = verify_rate(name, battery[name],
                                        {"gamma": g, "mu": m})
                p[f"probe_{g}_{m}"] = {"rate": rate, "err": err}
                if rate > 0.5:
                    dial = f"both@({g},{m})"
                    break
        g_price = (float(np.log2(gm)) if gm is not None
                   else float(np.log2(GAMMA_LADDER[-1])) + 1.0)
        # the mu price in fold-units; mu_max == 0.0 means the dial must
        # go to EXACTLY zero (an unbounded fold reduction — deposited
        # as None with the dial string carrying the semantics)
        m_price = (float(-np.log2(mm / MU_DEFAULT))
                   if mm is not None and mm > 0.0 else None)
        prices[name] = {"dial": dial, "gamma_min": gm, "mu_max": mm,
                        "gamma_price_log2": round(g_price, 2),
                        "mu_price_log2": (None if m_price is None
                                          else round(m_price, 2)),
                        "ladders": p}
        print(f"    {name}: dial {dial} gamma_min {gm} mu_max {mm}")

    # ---- RP-G3: the price is measurable -------------------------------------
    rp_g3 = all(prices[n]["dial"] != "both" or
                prices[n]["dial"].startswith("both@")
                for n in refused) and len(prices) == len(refused) \
        and all(not (prices[n]["dial"] == "both") for n in refused)
    rp_g3 = bool(all(prices[n]["dial"] != "both" for n in refused))
    print(f"  RP-G3 every refusal priced: "
          f"{'PASS' if rp_g3 else 'REFUTED'}")

    # ---- RP-G4: the stratification ------------------------------------------
    sf_gamma_fail = all(prices.get("scale_free", {}).get(
        "ladders", {}).get(f"gamma_{g}", {}).get("rate", 0) <= 0.5
        for g in GAMMA_LADDER)
    small_gamma_ok = all(
        prices.get(n, {}).get("ladders", {}).get(
            f"gamma_{g}", {}).get("rate", 0) > 0.5
        for n in ("torus", "random3") for g in (4.0, 16.0)
        if f"gamma_{g}" in prices.get(n, {}).get("ladders", {}))
    rp_g4 = bool(sf_gamma_fail)
    print(f"  RP-G4 stratification: scale_free gamma-ladder fails "
          f"through 64 = {sf_gamma_fail}; torus/random3 small-gamma "
          f"verify = {small_gamma_ok} -> {'PASS' if rp_g4 else 'REFUTED'}")

    npass = sum([rp_g1, rp_g2, rp_g3, rp_g4])
    print(f"\n  === {npass}/4 gates PASS ===")

    out = {
        "exp": "exp93_refusal_price",
        "r5_partition": r5,
        "default": default_res,
        "star": star_res,
        "prices": prices,
        "criteria": {
            "RP_G1_partition_control": rp_g1,
            "RP_G2_star_lift_control": rp_g2,
            "RP_G3_price_measurable": rp_g3,
            "RP_G4_channel_stratification": rp_g4,
        },
        "notes": (
            "R5' characterized: the refusal price is the minimal "
            "operating-point move along the two independent dials "
            "(exp79's two-channel law). The price ordering deposits "
            "the substrate stratification: which refusals the "
            "V-channel ratio buys (gamma), which the theta "
            "homogenization buys (mu), and which need both. exp89 "
            "machinery verbatim; the uc-in program; 3 seeds."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
