"""exp453 — PRIMARY P5: is P1 target memory robust to parameter change?

Gates frozen in docs/PRIMARIES_ROUND2.md (commit 6d2231c) before this ran.
Run: python -m experiments.exp453_p5_p1_robustness
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.stats import binomtest

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import wildtype_target
from experiments.exp448_p1_target_memory import N, DT, _protocol

DEFAULTS = {"gamma": 0.25, "g_gap": 0.20, "eps": 0.04, "mu_theta": 0.015,
            "noise_std": 0.30}
SCALES = [0.5, 2 ** -0.5, 2 ** 0.5, 2.0]
SEEDS = list(range(400, 410))
EPS_SCAN = [0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]


def _make(seed, **kw):
    params = dict(DEFAULTS); params.update(kw)
    c = BioElectricCollective(n=N, seed=seed, **params)
    c.set_target(wildtype_target(N))
    c.run(10, dt=DT)
    return c


def _cell(args):
    pname, sc, seed = args
    val = DEFAULTS[pname] * sc
    hA = _protocol(_make(seed, **{pname: val}), -20.0, 2)
    kwC = {pname: val}
    kwC["eps"] = 0.0
    hC = _protocol(_make(seed, **kwC), -20.0, 2)
    return pname, sc, seed, float(hA), float(hC)


def _eps_scan(args):
    m, seed = args
    return m, seed, float(_protocol(_make(seed, eps=DEFAULTS["eps"] * m), -20.0, 2))


def main() -> dict:
    jobs = [(p, sc, sd) for p in DEFAULTS for sc in SCALES for sd in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_cell, jobs))
        scan = list(ex.map(_eps_scan, [(m, sd) for m in EPS_SCAN for sd in SEEDS]))
    table = {}
    for p in DEFAULTS:
        for sc in SCALES:
            r = [x for x in rows if x[0] == p and x[1] == sc]
            table[f"{p}@{sc:.2f}"] = {"A_rewritten": sum(x[3] > 0.7 for x in r),
                                      "C_not": sum(x[4] < 0.35 for x in r),
                                      "A_mean_h": float(np.mean([x[3] for x in r]))}
    local = [v for k, v in table.items() if k.endswith("@0.71") or k.endswith("@1.41")]
    g5a = all(v["A_rewritten"] >= 8 for v in local)
    g5b = all(v["C_not"] >= 9 for v in table.values())
    succ = sum(v["A_rewritten"] for v in local)
    p = binomtest(succ, 10 * len(local), 0.5, alternative="greater").pvalue
    eps_curve = {m: float(np.mean([s[2] > 0.7 for s in scan if s[0] == m]))
                 for m in EPS_SCAN}
    res = {"primary": "P5", "table": table,
           "gates": {"G5a": bool(g5a), "G5b": bool(g5b)}, "p_value": float(p),
           "PASS": bool(g5a and g5b),
           "exploratory_eps_scan_rewrite_rate": {str(k): v for k, v in eps_curve.items()},
           "eps_over_gamma": {str(k): DEFAULTS["eps"] * k / DEFAULTS["gamma"] for k in EPS_SCAN}}
    print(f"{'cell':18s} A_rew  C_not  A_mean_h")
    for k, v in table.items():
        print(f"{k:18s} {v['A_rewritten']:>4d}  {v['C_not']:>5d}   {v['A_mean_h']:.2f}")
    print("eps multiplier -> rewrite rate:", {k: round(v, 2) for k, v in eps_curve.items()})
    print(f"G5a {'PASS' if g5a else 'FAIL'} | G5b {'PASS' if g5b else 'FAIL'} | p={p:.3g} "
          f"-> P5 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp453_p5_p1_robustness.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
