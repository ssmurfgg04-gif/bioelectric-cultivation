#!/usr/bin/env python3
"""exp98 — THE STAR'S TRUE PRICE LADDER (ledger L80; exp97's
registered follow-up: exp95's (gamma, mu) grid measured the coverage
ARTIFACT and is invalidated — under the repaired executor, where in
the dial plane does the deg-99 star actually verify?).

THE INSTRUMENT (exp93's ladder convention verbatim): the default
operating point is (gamma=1, mu=0.015); the star point is (64, 0).
For the star topology under frontier_mode="walk":
  * the DEFAULT cell (1, 0.015) x 3 seeds;
  * the GAMMA ladder at default mu: {2, 4, 8, 16, 32, 64} x 3
    (the V-channel price, log2 fold-units above the default);
  * the MU ladder at gamma=1: {0.01, 0.005, 0.002, 0} x 3
    (the theta-channel price, fold-units of mu reduction);
  * the TWO-DIAL probe {(4, 0), (16, 0)} x 3 (unconditional —
    deposited either way, the exp93 bracket);
  * the DEFAULT-POINT SANITY: path(100) at (1, 0.015) x 3 — the
    two-source read has only ever run at (64, 0); if path verifies
    at the default the reader's own default cell is real, and any
    star refusal at default is a PRICE, not a reader-wide gap.

THE MECHANISTIC STAKES: the hub's single-point integration is REAL
on the theta channel (each spoke's only theta-neighbor is the hub;
the hub integrates 99 thetas at 99*mu) — L77-L78 had the right
suspect on the wrong channel (the V-side settle is inert, exp97
CV-G3). Theta-priced (the torus class) is the live prediction: the
gamma ladder fails through 64 at default mu, the mu ladder buys it.

PRE-REGISTERED GATES:

  SL-G1  (writable somewhere) >= 1 star ladder cell verifies
         >= 2/3 seeds — the repaired star is writable at some
         operating point.
  SL-G2  (the class call) the minimal verifying cell by exp93's
         dial distance: DEFAULT if (1, 0.015) verifies; V-PRICED
         if some (g, 0.015) verifies with gamma_min deposited;
         THETA-PRICED if some (1, mu) verifies with mu_max
         deposited; TWO-DIAL if {(4,0), (16,0)} verifies; else
         REFUSED-EVERYWHERE (the architecture boundary RETURNS).
  SL-G3  (the channel signature) IF theta-priced: the gamma ladder
         at default mu fails 0/3 at every gamma including 64 while
         the mu ladder verifies — the priced channel is theta, the
         V channel never buys it. Otherwise deposit the failing
         ladder's monotonicity as the signature.
  SL-G4  (default-point sanity) path(100) verifies at (1, 0.015)
         >= 2/3 — the reader's default cell is real on a known
         default-class substrate.

RUN: 13 star cells x 3 seeds + path sanity x 3 = 42 runs. Serial,
BLAS pinned.
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

from experiments.exp94_multizone_scale import (
    execute_two_source_n, MULTI, star_adj,
)
from cultivation.substrate.graph import path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp98_star_price_ladder.json")

SEEDS = (1, 2, 3)
MU_DEFAULT = 0.015
GAMMA_LADDER = (2.0, 4.0, 8.0, 16.0, 32.0, 64.0)
MU_LADDER = (0.01, 0.005, 0.002, 0.0)
TWO_DIAL = ((4.0, 0.0), (16.0, 0.0))


def cell(adj, gamma, mu, frontier_mode="walk"):
    res = [execute_two_source_n(MULTI, adj, s, op={"gamma": gamma,
                                                   "mu": mu},
                                frontier_mode=frontier_mode)
           for s in SEEDS]
    return {"rate": round(float(np.mean(
        [r["program_verified"] for r in res])), 3),
        "err": round(float(np.mean(
            [r["err_vs_target"] for r in res])), 2)}


def main() -> dict:
    print("=== exp98: the star's true price ladder ===\n")

    star = star_adj(100)
    out: dict[str, dict] = {}

    out["star_default_1_0.015"] = cell(star, 1.0, MU_DEFAULT)
    for g in GAMMA_LADDER:
        out[f"star_gamma_{g:g}_mu_default"] = cell(star, g, MU_DEFAULT)
    for m in MU_LADDER:
        out[f"star_mu_{m:g}_gamma1"] = cell(star, 1.0, m)
    for g, m in TWO_DIAL:
        out[f"star_twodial_{g:g}_{m:g}"] = cell(star, g, m)
    out["path_default_sanity"] = cell(path(100), 1.0, MU_DEFAULT)
    for k, v in out.items():
        print(f"    {k:28s} rate {v['rate']:.2f} err {v['err']}")

    def rate_of(key):
        return out[key]["rate"]

    verifies = [k for k in out if k.startswith("star_")
                and rate_of(k) >= 2 / 3]
    sl_g1 = len(verifies) >= 1

    if rate_of("star_default_1_0.015") >= 2 / 3:
        cls, cls_key = "DEFAULT", "star_default_1_0.015"
    else:
        g_ver = [g for g in GAMMA_LADDER
                 if rate_of(f"star_gamma_{g:g}_mu_default") >= 2 / 3]
        m_ver = [m for m in MU_LADDER
                 if rate_of(f"star_mu_{m:g}_gamma1") >= 2 / 3]
        td_ver = [f"star_twodial_{g:g}_{m:g}" for g, m in TWO_DIAL
                  if rate_of(f"star_twodial_{g:g}_{m:g}") >= 2 / 3]
        if g_ver:
            cls, cls_key = "V_PRICED", g_ver[0]
        elif m_ver:
            cls, cls_key = "THETA_PRICED", m_ver[0]
        elif td_ver:
            cls, cls_key = "TWO_DIAL", td_ver[0]
        else:
            cls, cls_key = "REFUSED_EVERYWHERE", None

    gamma_ladder_rates = [rate_of(f"star_gamma_{g:g}_mu_default")
                          for g in GAMMA_LADDER]
    mu_ladder_rates = [rate_of(f"star_mu_{m:g}_gamma1")
                       for m in MU_LADDER]
    if cls == "THETA_PRICED":
        sl_g3 = all(r <= 1 / 3 for r in gamma_ladder_rates)
    else:
        fails = [r for r in gamma_ladder_rates if r <= 1 / 3]
        sl_g3 = (len(fails) == len(gamma_ladder_rates)
                 or all(gamma_ladder_rates[i] <= gamma_ladder_rates[i + 1]
                        + 1e-9
                        for i in range(len(gamma_ladder_rates) - 1)))

    sl_g4 = rate_of("path_default_sanity") >= 2 / 3
    print(f"\n  SL-G1 writable somewhere: {'PASS' if sl_g1 else 'REFUTED'}")
    print(f"  SL-G2 the class call: {cls}"
          f"{'' if cls_key is None else f' (cheapest: {cls_key})'}")
    print(f"  SL-G3 channel signature: {'PASS' if sl_g3 else 'REFUTED'}")
    print(f"  SL-G4 default-point sanity (path): "
          f"{'PASS' if sl_g4 else 'REFUTED'}")

    npass = sum([sl_g1, sl_g3, sl_g4])
    print(f"\n  === {npass}/3 boolean gates PASS; class = {cls} ===")

    result = {
        "exp": "exp98_star_price_ladder",
        "arms": out,
        "class": {"call": cls, "cheapest_verifying_cell": cls_key,
                  "gamma_ladder_rates": gamma_ladder_rates,
                  "mu_ladder_rates": mu_ladder_rates},
        "criteria": {
            "SL_G1_writable_somewhere": bool(sl_g1),
            "SL_G3_channel_signature": bool(sl_g3),
            "SL_G4_default_point_sanity": bool(sl_g4),
        },
        "notes": (
            "exp95's grid measured the coverage artifact and is "
            "invalidated; this is the star's price ladder under the "
            "repaired executor (frontier_mode='walk'). exp93's "
            "ladder convention verbatim; the two-source read's "
            "first run at the DEFAULT operating point (the reader "
            "has only ever run at the (64, 0) star point); 3 seeds."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
