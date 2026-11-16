"""exp456 — PRIMARY P6: memory threshold depends on eps x exposure time.

Gates frozen in docs/PRIMARIES_ROUND3.md (commit 3053b8c) before this ran.
Run: python -m experiments.exp456_p6_eps_time
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.stats import binomtest
from scipy.optimize import minimize

from experiments.exp448_p1_target_memory import DT, TAIL, _amputate_rounds
from experiments.exp453_p5_p1_robustness import _make, DEFAULTS

EPS_M = [0.5, 0.75, 1.0, 1.5]
TIMES = [6, 12, 16, 24, 32, 48]
SEEDS = list(range(700, 710))
PAIRS = [(0.5, 48), (0.75, 32), (1.0, 24), (1.5, 16)]


def _run(args):
    m, T, seed = args
    c = _make(seed, eps=DEFAULTS["eps"] * m)
    c.block_gap_junctions(0.05)
    c.clamp(TAIL, -20.0)
    c.run(T, dt=DT)
    c.restore_gap_junctions(1.0)
    c.release_clamps()
    c.run(20, dt=DT)
    return m, T, seed, float(_amputate_rounds(c, 2))


def main() -> dict:
    jobs = [(m, T, s) for m in EPS_M for T in TIMES for s in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_run, jobs))
    cnt = {(m, T): sum(r[3] > 0.7 for r in rows if r[0] == m and r[1] == T)
           for m in EPS_M for T in TIMES}
    d = [cnt[(1.0, T)] for T in TIMES]
    g6a = all(d[i + 1] >= d[i] - 1 for i in range(len(d) - 1)) and d[0] <= 2 and d[-1] >= 8
    g6b = all(cnt[p] >= 8 for p in PAIRS)
    g6c = cnt[(0.5, 24)] <= 2 and cnt[(1.5, 24)] >= 8
    succ = sum(cnt[p] for p in PAIRS)
    p = binomtest(succ, 40, 0.5, alternative="greater").pvalue

    # exploratory: logistic fit of success on log(eps*T)
    x = np.array([np.log(DEFAULTS["eps"] * r[0] * r[1]) for r in rows])
    y = np.array([r[3] > 0.7 for r in rows], float)

    def nll(b):
        z = b[0] + b[1] * x
        return np.sum(np.logaddexp(0, z) - y * z)
    b = minimize(nll, [0.0, 5.0], method="Nelder-Mead").x
    et50 = float(np.exp(-b[0] / b[1]))

    g = {"G6a": bool(g6a), "G6b": bool(g6b), "G6c": bool(g6c)}
    res = {"primary": "P6", "grid_rewritten_of_10": {f"{m}x@{T}h": v for (m, T), v in cnt.items()},
           "gates": g, "p_value": float(p), "PASS": all(g.values()),
           "exploratory_logistic": {"intercept": float(b[0]), "slope": float(b[1]),
                                    "epsT_50": et50}}
    print("rewritten/10   T(h): " + " ".join(f"{T:>4d}" for T in TIMES))
    for m in EPS_M:
        print(f"  eps x{m:<4}        " + " ".join(f"{cnt[(m, T)]:>4d}" for T in TIMES))
    print(f"matched pairs (eps*T=0.96): {[cnt[q] for q in PAIRS]}")
    print(f"logistic 50% point: eps*T = {et50:.3f}")
    for k, v in g.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print(f"p = {p:.3g} -> P6 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp456_p6_eps_time.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
