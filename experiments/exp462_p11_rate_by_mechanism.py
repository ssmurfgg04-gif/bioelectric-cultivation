"""exp462 — PRIMARY P11: is the Gompertz rate set by mechanism (element failure rate k)?
Frozen in docs/PRIMARIES_ROUND7.md (b1d2c1b + amendment A 371b2c7). Uses P13' best fit."""
from __future__ import annotations
import json, os
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy import stats
from cultivation.bioelectric.reliability import ReliabilityParams, simulate, gompertz_beta

BEST = dict(n_blocks=2, lam=3000, k=0.10, k_cv=0.1)
SCALES = [0.5, 2 ** -0.5, 1.0, 2 ** 0.5, 2.0]
SEEDS = [1120, 1121, 1122]


def _job(args):
    sc, seed = args
    p = ReliabilityParams(**{**BEST, "k": BEST["k"] * sc})
    d = simulate(p, 10000, 140.0 / sc + 60, seed)
    M = float(np.median(d))
    b, fit = gompertz_beta(d, 0.45 * M, 1.25 * M)
    return sc, seed, b, fit["fits"]["gompertz"]["aic"], fit["fits"]["weibull"]["aic"], M


def main():
    with ProcessPoolExecutor(os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, [(sc, s) for sc in SCALES for s in SEEDS]))
    x = np.log([BEST["k"] * r[0] for r in rows]); y = np.log([r[2] for r in rows])
    lr = stats.linregress(x, y)
    aic_ok = {sc: sum(r[3] for r in rows if r[0] == sc) < sum(r[4] for r in rows if r[0] == sc) for sc in SCALES}
    g = {"G11a": bool(lr.slope >= 0.5), "G11b": bool(all(aic_ok.values()))}
    p = float(lr.pvalue / 2 if lr.slope > 0 else 1 - lr.pvalue / 2)
    for sc in SCALES:
        r = [q for q in rows if q[0] == sc]
        print(f"k={BEST['k']*sc:.3f} beta={np.mean([q[2] for q in r]):.4f} median={np.mean([q[5] for q in r]):.1f} gompertz_beats_weibull={aic_ok[sc]}")
    print(f"elasticity {lr.slope:.3f} ± {lr.stderr:.3f}  p={p:.2g}")
    res = {"primary": "P11", "rows": rows, "elasticity": float(lr.slope), "se": float(lr.stderr),
           "p_value": p, "gates": g, "PASS": all(g.values())}
    print(f"G11a {'PASS' if g['G11a'] else 'FAIL'} | G11b {'PASS' if g['G11b'] else 'FAIL'} -> P11 {'PASS' if res['PASS'] else 'FAIL'}")
    json.dump(res, open("results/exp462_p11_rate_by_mechanism.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
