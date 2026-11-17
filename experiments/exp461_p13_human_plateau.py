"""exp461 — PRIMARY P13: fit reliability model to human median + Gompertz beta,
predict the held-out late-life mortality plateau (Barbi et al. 2018, ~0.7/yr).

Frozen in docs/PRIMARIES_ROUND7.md (commit b1d2c1b).
"""
from __future__ import annotations

import itertools
import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.reliability import (ReliabilityParams, simulate,
                                                 gompertz_beta, late_hazard)

NS = [2, 4, 8, 16, 32]
LAMS = [300, 1000, 3000, 10000, 30000]
KS = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08]
TEST_SEEDS = [1110, 1111, 1112, 1113, 1114]
OBS_PLATEAU = 0.7


def _cal(args):
    n, lam, k = args
    d = simulate(ReliabilityParams(n_blocks=n, lam=lam, k=k), 4000, 140, 1100)
    M = float(np.median(d))
    try:
        b, _ = gompertz_beta(d, 35.0, 100.0)
    except Exception:
        b = float("nan")
    return n, lam, k, M, b


def _test(args):
    n, lam, k, seed = args
    d = simulate(ReliabilityParams(n_blocks=n, lam=lam, k=k), 20000, 140, seed)
    return (n, lam, k, seed, late_hazard(d, 105, 110), late_hazard(d, 110, 115),
            late_hazard(d, 105, 115), int((d >= 105).sum()))


def main():
    grid = list(itertools.product(NS, LAMS, KS))
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        cal = list(ex.map(_cal, grid))
        acc = [c for c in cal if 77 <= c[3] <= 83 and np.isfinite(c[4]) and 0.075 <= c[4] <= 0.095]
        print(f"accepted {len(acc)}/{len(grid)}")
        for c in acc:
            print(f"  n={c[0]:>2} lam={c[1]:>5} k={c[2]}  median={c[3]:.1f} beta={c[4]:.4f}")
        if not acc:
            res = {"primary": "P13", "accepted": [], "gates": {"G13a": False, "G13b": False}, "PASS": False}
            print("P13 FAIL: nothing accepted")
        else:
            best = min(acc, key=lambda c: ((c[3] - 80) / 3) ** 2 + ((c[4] - 0.085) / 0.01) ** 2)
            tests = list(ex.map(_test, [(c[0], c[1], c[2], s) for c in acc for s in TEST_SEEDS]))
            per = {}
            for c in acc:
                r = [t for t in tests if t[:3] == c[:3]]
                per[c[:3]] = {"h105_115": float(np.nanmean([t[6] for t in r])),
                              "h105_110": float(np.nanmean([t[4] for t in r])),
                              "h110_115": float(np.nanmean([t[5] for t in r])),
                              "n_at_105": int(np.mean([t[7] for t in r]))}
            med_pred = float(np.median([v["h105_115"] for v in per.values()]))
            bb = per[best[:3]]
            ratio = bb["h110_115"] / bb["h105_110"]
            g = {"G13a": bool(0.40 <= med_pred <= 1.20), "G13b": bool(ratio < 1.3)}
            res = {"primary": "P13", "accepted": [list(c) for c in acc], "best": list(best),
                   "per_set": {str(k): v for k, v in per.items()},
                   "median_pred_plateau": med_pred, "observed_plateau_barbi2018": OBS_PLATEAU,
                   "best_ratio_110_115_over_105_110": ratio,
                   "gates": g, "PASS": all(g.values())}
            for k_, v in per.items():
                print(f"  {k_}: h[105,115)={v['h105_115']:.3f}  ({v['h105_110']:.3f} -> {v['h110_115']:.3f})  n@105~{v['n_at_105']}")
            print(f"best fit n,lam,k = {best[:3]}  median pred plateau {med_pred:.3f} (obs ~0.7)  ratio {ratio:.2f}")
            print(f"G13a {'PASS' if g['G13a'] else 'FAIL'} | G13b {'PASS' if g['G13b'] else 'FAIL'} -> P13 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp461_p13_human_plateau.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
