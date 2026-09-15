"""Capture golden values BEFORE the exp23 hooks land, for bit-exact
regression (the S2/S3 backdoor discipline: additive hooks must not change
a single draw when unused).

Scenario: 8 individuals, broadcast/v2/protected cohort, zone 24:36 written
to -10 at t=1, anchored codec budget 4 from age 10 every 5yr, 40yr horizon.
Records codec counters + state checksums.
"""
import json
import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec
from cultivation.bioelectric.senescence_semantics import SemanticsCohort
from experiments.exp8_fidelity import N_CELLS, REGIME, fidelity_target

PRESET = {"meas_noise_mV": 1.5, "dropout": 0.1, "symbol_err": 0.05}


def scenario() -> dict:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = SemanticsCohort(K=8, params=params, seed=42,
                         death_semantics="broadcast", latch="v2",
                         protect_written=True, jump_rate=0.02, f_crit=0.655)
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    state = {"done": False}

    def maintain(t, cohort):
        if not state["done"] and t >= 1.0:
            state["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, 24:36] = True
            cohort.theta = np.where(do, -10.0, cohort.theta)
            cohort.V = np.where(do, -10.0, cohort.V)
            cohort.on_write(do)
        if t >= 10.0 and abs((t - 10.0) % 5.0) <= 0.26:
            codec.maintain(cohort, PRESET, mode="codec")

    s = ch.run(years=40.0, dt=0.25, intervention=maintain)
    zone = np.zeros(ch.n, bool)
    zone[24:36] = True
    led = ch.pattern_ledger(ref=np.where(zone, -10.0, ch.theta0), zone=zone)
    return {
        "cycles": codec.cycles, "verified": codec.verified,
        "refused": codec.refused, "restored": codec.restored,
        "median": float(s["median_lifespan"]),
        "theta_sum": float(np.asarray(ch.theta).sum()),
        "theta_anchor_sum": float(np.asarray(ch.theta_anchor).sum()),
        "V_sum": float(np.asarray(ch.V).sum()),
        "sen_frac": float(ch.senesced.mean()),
        "death_events": int(ch.death_events),
        "ledger_I_rec": led["I_recoverable"],
    }


if __name__ == "__main__":
    gold = scenario()
    out = "results/_golden_exp23_prereg.json"
    with open(out, "w") as f:
        json.dump(gold, f, indent=1, sort_keys=True)
    print(json.dumps(gold, indent=1, sort_keys=True))
    print(f"golden written: {out}")
