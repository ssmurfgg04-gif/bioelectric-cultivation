"""Quick timing probe for the CEM search budget."""
import sys, time
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec
from experiments.exp8_fidelity import fidelity_target, REGIME, age_preset

def one_run(K=150, years=110.0, seed=0):
    codec = FidelityCodec(n_cells=60, budget_per_cycle=6)
    params = AgingParams(n_cells=60, target0=fidelity_target(), **REGIME)
    ch = FidelityAgingCohort(K=K, params=params, seed=seed)
    def maintain(t, cohort):
        if t < 30.0 - 1e-9 or abs((t - 30.0) % 5.0) > 0.26:
            return
        codec.maintain(cohort, age_preset(t), mode="codec")
    s = ch.run(years=years, dt=0.25, intervention=maintain, record=False)
    return s["median_lifespan"]

t0 = time.time()
m = one_run()
t1 = time.time()
print(f"K=150 years=110 codec-maintained run: median={m:.1f}, wall={t1-t0:.2f}s")

t0 = time.time()
m = one_run(years=130.0)
t1 = time.time()
print(f"K=150 years=130 codec-maintained run: median={m:.1f}, wall={t1-t0:.2f}s")

params = AgingParams(n_cells=60, target0=fidelity_target(), **REGIME)
ch = FidelityAgingCohort(K=150, params=params, seed=1)
t0 = time.time(); s = ch.run(years=130.0, dt=0.25, record=False); t1 = time.time()
print(f"K=150 years=130 none run: median={s['median_lifespan']:.1f}, wall={t1-t0:.2f}s")
