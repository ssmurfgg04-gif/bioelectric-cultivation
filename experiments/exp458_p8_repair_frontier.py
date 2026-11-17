"""exp458 — PRIMARY P8: repair-budget frontier.

Gates frozen in docs/PRIMARIES_ROUND5.md (commit 3111615) before this ran.
Run: python -m experiments.exp458_p8_repair_frontier
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams

PERIODS = [10, 20, 30, 40, 60]
COMPLETE = [0.25, 0.5, 0.75, 1.0]
SEEDS = [900, 901, 902]
K, YEARS, DT, START = 200, 300.0, 0.25, 48.0


def make_repair(R, c):
    def f(t, ch):
        if t < START - 1e-9 or abs((t - START) % R) >= DT / 2:
            return
        a = ch.alive
        ch.theta[a] += c * (ch.theta0 - ch.theta[a])
        clear = ch.senesced & a[:, None] & (ch.rng.random(ch.senesced.shape) < c)
        ch.senesced[clear] = False
        rows, cols = np.where(clear)
        ch.theta[rows, cols] = ch.theta0[cols]
        ch.V[rows, cols] = ch.theta0[cols]
        bio = t - ch.clock_offset
        ch.clock_offset[a] += c * np.maximum(bio[a] - 25.0, 0.0)
    return f


def _job(args):
    R, c, seed = args
    ch = AgingCohort(K=K, params=AgingParams(), seed=seed)
    s = ch.run(years=YEARS, dt=DT, intervention=make_repair(R, c), record=False)
    return R, c, seed, s["survivors_at_end"] / K, s["median_lifespan_km"]


def main() -> dict:
    jobs = [(R, c, s) for R in PERIODS for c in COMPLETE for s in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, jobs))
    A = {(R, c): float(np.mean([r[3] for r in rows if r[0] == R and r[1] == c]))
         for R in PERIODS for c in COMPLETE}
    M = {(R, c): [r[4] for r in rows if r[0] == R and r[1] == c] for R in PERIODS for c in COMPLETE}
    tol = 0.05
    mono_R = all(A[(PERIODS[i + 1], c)] <= A[(PERIODS[i], c)] + tol
                 for c in COMPLETE for i in range(len(PERIODS) - 1))
    mono_c = all(A[(R, COMPLETE[i + 1])] >= A[(R, COMPLETE[i])] - tol
                 for R in PERIODS for i in range(len(COMPLETE) - 1))
    g8a = mono_R and mono_c
    g8b = A[(10, 0.5)] < 0.5 * A[(10, 1.0)]
    frontier = {R: next((c for c in COMPLETE if A[(R, c)] > 0.5), None) for R in PERIODS}
    res = {"primary": "P8", "alive300": {f"R{R}_c{c}": v for (R, c), v in A.items()},
           "km_median": {f"R{R}_c{c}": v for (R, c), v in M.items()},
           "frontier_min_completeness_for_escape": {str(k): v for k, v in frontier.items()},
           "gates": {"G8a": bool(g8a), "G8b": bool(g8b)}, "PASS": bool(g8a and g8b)}
    print("alive@300   c: " + " ".join(f"{c:>6}" for c in COMPLETE))
    for R in PERIODS:
        print(f"  every {R:>2} yr   " + " ".join(f"{A[(R, c)]:>6.2f}" for c in COMPLETE))
    print("median KM (c=1.0):", {R: M[(R, 1.0)] for R in PERIODS})
    print("frontier (min c for escape):", frontier)
    print(f"G8a {'PASS' if g8a else 'FAIL'} (mono_R={mono_R}, mono_c={mono_c}) | "
          f"G8b {'PASS' if g8b else 'FAIL'} -> P8 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp458_p8_repair_frontier.json", "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    main()
