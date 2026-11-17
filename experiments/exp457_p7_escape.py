"""exp457 — PRIMARY P7: what must be repaired for negligible senescence?

Gates frozen in docs/PRIMARIES_ROUND4.md (commit 09bcd48) before this ran.
Run: python -m experiments.exp457_p7_escape
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams

SEEDS = [800, 801, 802, 803, 804]
K, YEARS, DT, START = 200, 300.0, 0.25, 48.0


def _state_repair(c):
    a = c.alive
    c.theta[a] = c.theta0
    c.V[a] = c.theta0
    c.senesced[a] = False


def _clock_repair(c):
    a = c.alive
    c.clock_offset[a] = c.t - 25.0


def _every(period, *actions):
    def f(t, c):
        if t >= START - 1e-9 and abs(((t - START) % period)) < DT / 2:
            for act in actions:
                act(c)
    return f


ARMS = {
    "none": None,
    "M1_state_1yr": _every(1.0, _state_repair),
    "M2_clock_10yr": _every(10.0, _clock_repair),
    "M3_full_10yr": _every(10.0, _state_repair, _clock_repair),
    "M4_full_20yr": _every(20.0, _state_repair, _clock_repair),
}


def _job(args):
    arm, seed = args
    c = AgingCohort(K=K, params=AgingParams(), seed=seed)
    s = c.run(years=YEARS, dt=DT, intervention=ARMS[arm], record=False)
    return arm, seed, s["median_lifespan_km"], s["survivors_at_end"] / K


def main() -> dict:
    jobs = [(a, s) for a in ARMS for s in SEEDS]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, jobs))
    tab = {a: {"km_median": [r[2] for r in rows if r[0] == a],
               "alive_300": [r[3] for r in rows if r[0] == a]} for a in ARMS}
    g7a = all(m < 200 for m in tab["M1_state_1yr"]["km_median"])
    g7b = all(f > 0.5 for f in tab["M3_full_10yr"]["alive_300"])
    res = {"primary": "P7", "table": tab,
           "gates": {"G7a": bool(g7a), "G7b": bool(g7b)},
           "p_value_per_gate": 0.5 ** 5, "PASS": bool(g7a and g7b)}
    for a, v in tab.items():
        med = ", ".join("inf" if not np.isfinite(m) else f"{m:.0f}" for m in v["km_median"])
        print(f"{a:15s} KM median [{med}]  alive@300 mean {np.mean(v['alive_300']):.2f}")
    print(f"G7a {'PASS' if g7a else 'FAIL'} | G7b {'PASS' if g7b else 'FAIL'} "
          f"-> P7 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp457_p7_escape.json", "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    main()
