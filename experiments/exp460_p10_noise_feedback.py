"""exp460 — PRIMARY P10: with damage->noise feedback, does state repair alone escape?

Gates and calibration rule frozen in docs/PRIMARIES_ROUND6.md (commit a5d7f39).
Run: python -m experiments.exp460_p10_noise_feedback
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from cultivation.bioelectric.aging import AgingCohort, AgingParams
from experiments.exp457_p7_escape import _state_repair, _every

PHIS = [0.5, 0.9]
CAL_SEEDS = [1000, 1001, 1002]
SEEDS = [1010, 1011, 1012, 1013, 1014]
K, YEARS, DT = 200, 300.0, 0.25
BASE = AgingParams()


def _cal(args):
    phi, seed = args
    p = BASE.with_updates(kappa_noise=(1 - phi) * BASE.kappa_noise)
    c = AgingCohort(K=K, params=p, seed=seed)
    c.run(years=70.0, dt=DT, record=False)
    return float(c.damage_dose[c.alive].mean())


def _noise_reset(c):
    a = c.alive
    c.noise_offset[a] = (c.t - c.clock_offset[a]) - 25.0
    c.damage_dose[a] = 0.0


ARMS = {"none": None,
        "state_only": _every(10.0, _state_repair),
        "state_noise": _every(10.0, _state_repair, _noise_reset)}


def _job(args):
    phi, kdam, arm, seed = args
    p = BASE.with_updates(kappa_noise=(1 - phi) * BASE.kappa_noise, noise_kappa_damage=kdam)
    s = AgingCohort(K=K, params=p, seed=seed).run(years=YEARS, dt=DT,
                                                   intervention=ARMS[arm], record=False)
    return phi, arm, seed, s["survivors_at_end"] / K, s["median_lifespan_km"]


def main() -> dict:
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        cal = {phi: float(np.mean(list(ex.map(_cal, [(phi, s) for s in CAL_SEEDS]))))
               for phi in PHIS}
        kdam = {phi: phi * BASE.kappa_noise * 70.0 / cal[phi] for phi in PHIS}
        jobs = [(phi, kdam[phi], a, s) for phi in PHIS for a in ARMS for s in SEEDS]
        rows = list(ex.map(_job, jobs))
    tab = {f"phi{phi}_{a}": {"alive300": [r[3] for r in rows if r[0] == phi and r[1] == a],
                              "km_median": [r[4] for r in rows if r[0] == phi and r[1] == a]}
           for phi in PHIS for a in ARMS}
    esc = lambda k: sum(f > 0.5 for f in tab[k]["alive300"])
    g10a = esc("phi0.9_state_only") >= 4
    g10b = (5 - esc("phi0.5_state_only")) >= 4
    res = {"primary": "P10", "calibration_meanD70": cal, "kappa_damage": kdam,
           "table": tab, "gates": {"G10a": bool(g10a), "G10b": bool(g10b)},
           "PASS": bool(g10a and g10b)}
    print("calibration mean D(70):", {k: round(v, 3) for k, v in cal.items()},
          "-> kappa_dam:", {k: round(v, 4) for k, v in kdam.items()})
    for k, v in tab.items():
        med = ", ".join("inf" if not np.isfinite(m) else f"{m:.0f}" for m in v["km_median"])
        print(f"{k:20s} alive@300 {np.mean(v['alive300']):.2f}  KM median [{med}]")
    print(f"G10a {'PASS' if g10a else 'FAIL'} | G10b {'PASS' if g10b else 'FAIL'} "
          f"-> P10 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp460_p10_noise_feedback.json", "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    main()
