"""Capture golden values for the exp24 POTENTIATION path (locks the
active-path semantics for all future edits).

Scenario: 8 individuals, exp23-style zone physics (jump_mult 0.5/2.0),
zone 24:36 written to -10 at t=1, anchored codec budget 4 from age 10
every 5yr, POTENTIATION factor 0.25 window 5yr on every maintenance
write (the write mask captured through on_write — the same mechanism
the experiment uses). 40yr horizon.

Any future _apply_jumps/potentiate edit must reproduce these values
exactly (same seeds, same draws: potentiation consumes no RNG).
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
JUMP_MULT = np.array([1., 1., 1., .5, .5, .5, 2., 2., 2., 1., 1., 1.])


class CaptureCohort(SemanticsCohort):
    """Stashes the maintenance cycle's actual write mask (exp24's
    mechanism: potentiation is correction-coupled by construction)."""

    def on_write(self, do):
        if getattr(self, "_capture", False):
            prev = getattr(self, "_captured_do", None)
            self._captured_do = do.copy() if prev is None else (prev | do)
        super().on_write(do)


def scenario(factor: float = 0.25, window: float = 5.0,
             cls=CaptureCohort) -> dict:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(), **REGIME)
    ch = cls(K=8, params=params, seed=42,
             death_semantics="broadcast", latch="v2",
             protect_written=True, jump_rate=0.02, f_crit=0.655)
    ch.jump_mult = JUMP_MULT
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=4, levels=7,
                          target_source="anchored")
    state = {"done": False, "pot_calls": 0, "pot_pairs": 0}

    def maintain(t, cohort):
        if not state["done"] and t >= 1.0:
            state["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, 24:36] = True
            cohort.theta = np.where(do, -10.0, cohort.theta)
            cohort.V = np.where(do, -10.0, cohort.V)
            cohort.on_write(do)
        if t >= 10.0 and abs((t - 10.0) % 5.0) <= 0.26:
            cohort._capture = True
            codec.maintain(cohort, PRESET, mode="codec")
            cohort._capture = False
            do = getattr(cohort, "_captured_do", None)
            if do is not None:
                n = cohort.potentiate(do, window=window, factor=factor)
                state["pot_calls"] += 1
                state["pot_pairs"] += int(n)
                cohort._captured_do = None

    s = ch.run(years=40.0, dt=0.25, intervention=maintain)
    zone = np.zeros(ch.n, bool)
    zone[24:36] = True
    led = ch.pattern_ledger(ref=np.where(zone, -10.0, ch.theta0), zone=zone)
    return {
        "pot_calls": state["pot_calls"],
        "pot_pairs": state["pot_pairs"],
        "cycles": codec.cycles, "restored": codec.restored,
        "median": float(s["median_lifespan"]),
        "theta_sum": float(np.asarray(ch.theta).sum()),
        "V_sum": float(np.asarray(ch.V).sum()),
        "sen_frac": float(ch.senesced.mean()),
        "death_events": int(ch.death_events),
        "ledger_I_rec": led["I_recoverable"],
    }


if __name__ == "__main__":
    gold = scenario()
    out = "results/_golden_exp24_prereg.json"
    with open(out, "w") as f:
        json.dump(gold, f, indent=1, sort_keys=True)
    print(json.dumps(gold, indent=1, sort_keys=True))
    print(f"golden written: {out}")
