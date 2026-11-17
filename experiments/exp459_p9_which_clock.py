"""exp459 — PRIMARY P9: which clock (junction loss vs noise growth) carries the synergy?

Gates frozen in docs/PRIMARIES_ROUND5.md (commit 3111615) before this ran.
Run: python -m experiments.exp459_p9_which_clock
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams
from experiments.exp457_p7_escape import _state_repair, _every

SEEDS = [950, 951, 952, 953, 954]
K, YEARS, DT = 200, 300.0, 0.25


def _gap_clock(c):
    a = c.alive
    c.gap_offset[a] = (c.t - c.clock_offset[a]) - 25.0


def _noise_clock(c):
    a = c.alive
    c.noise_offset[a] = (c.t - c.clock_offset[a]) - 25.0


ARMS = {
    "S+G": _every(10.0, _state_repair, _gap_clock),
    "S+N": _every(10.0, _state_repair, _noise_clock),
    "S+GN": _every(10.0, _state_repair, _gap_clock, _noise_clock),
    "G_only": _every(10.0, _gap_clock),
    "N_only": _every(10.0, _noise_clock),
}


def _job(args):
    arm, seed = args
    ch = AgingCohort(K=K, params=AgingParams(), seed=seed)
    s = ch.run(years=YEARS, dt=DT, intervention=ARMS[arm], record=False)
    return arm, seed, s["survivors_at_end"] / K, s["median_lifespan_km"]


def main() -> dict:
    jobs = [(a, s) for a in ARMS for s in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, jobs))
    tab = {a: {"alive300": [r[2] for r in rows if r[0] == a],
               "km_median": [r[3] for r in rows if r[0] == a]} for a in ARMS}
    g9a = all(f > 0.5 for f in tab["S+N"]["alive300"])
    g9b = all(f <= 0.5 for f in tab["S+G"]["alive300"])
    res = {"primary": "P9", "table": tab, "gates": {"G9a": bool(g9a), "G9b": bool(g9b)},
           "PASS": bool(g9a and g9b)}
    for a, v in tab.items():
        med = ", ".join("inf" if not np.isfinite(m) else f"{m:.0f}" for m in v["km_median"])
        print(f"{a:7s} alive@300 mean {np.mean(v['alive300']):.2f}  KM median [{med}]")
    print(f"G9a {'PASS' if g9a else 'FAIL'} | G9b {'PASS' if g9b else 'FAIL'} "
          f"-> P9 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp459_p9_which_clock.json", "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    main()
