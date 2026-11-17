"""exp463 — PRIMARY P12: with harm per repair, is the optimal repair interval interior?
Frozen in docs/PRIMARIES_ROUND7.md (b1d2c1b + amendment A 371b2c7). Uses P13' best fit."""
from __future__ import annotations
import json, os
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from cultivation.bioelectric.reliability import ReliabilityParams, simulate

BEST = dict(n_blocks=2, lam=3000, k=0.10, k_cv=0.1)
PERIODS = [5, 10, 20, 30, 40]
HARMS = [0.0, 1e-3]
SEEDS = [1130, 1131, 1132]
HORIZON = 600.0


def _job(args):
    R, h, seed = args
    p = ReliabilityParams(**BEST, mu_ext=5e-4, harm=h)
    d = simulate(p, 4000, HORIZON, seed, repair_every=R, repair_c=1.0)
    return R, h, seed, float(np.minimum(d, HORIZON).mean())


def main():
    with ProcessPoolExecutor(os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, [(R, h, s) for R in PERIODS for h in HARMS for s in SEEDS]))
    rm = {(R, h): float(np.mean([r[3] for r in rows if r[0] == R and r[1] == h])) for R in PERIODS for h in HARMS}
    z = [rm[(R, 0.0)] for R in PERIODS]
    g12a = all(z[i + 1] <= z[i] * 1.01 for i in range(len(z) - 1))
    best_R = max(PERIODS, key=lambda R: rm[(R, 1e-3)])
    g12b = best_R not in (PERIODS[0], PERIODS[-1])
    print("RMST to 600 yr     harm=0     harm=1e-3")
    for R in PERIODS:
        print(f"  every {R:>2} yr   {rm[(R,0.0)]:8.1f}   {rm[(R,1e-3)]:8.1f}")
    print(f"optimal R with harm: {best_R} yr")
    g = {"G12a": bool(g12a), "G12b": bool(g12b)}
    res = {"primary": "P12", "rmst": {f"R{R}_h{h}": v for (R, h), v in rm.items()},
           "optimal_R_with_harm": best_R, "gates": g, "PASS": all(g.values())}
    print(f"G12a {'PASS' if g12a else 'FAIL'} | G12b {'PASS' if g12b else 'FAIL'} -> P12 {'PASS' if res['PASS'] else 'FAIL'}")
    json.dump(res, open("results/exp463_p12_costly_repair.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
