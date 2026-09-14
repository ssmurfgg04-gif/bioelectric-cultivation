"""Debug the batched maintain on the failing test scenario."""
import sys
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec

REGIME = dict(kappa_noise=0.020, lambda_gap=0.024, mu_theta=0.03,
              h_sys=0.050, seed_rate=6.0e-5, h_inflam=0.030, mortality_k=0.10)
TARGET = np.concatenate([np.full(12, v) for v in (-50.0, -20.0, -50.0, -60.0, -40.0)])

ch = FidelityAgingCohort(K=1, params=AgingParams(n_cells=60, target0=TARGET,
                                                 **REGIME), seed=2)
ch.jump_rate = 0.0
ch.theta[0, 15:20] = -60.0
ch.V[0, 15:20] = -60.0

codec = FidelityCodec(n_cells=60, budget_per_cycle=6)
preset = {"meas_noise_mV": 1.0, "dropout": 0.02, "symbol_err": 0.005}

theta_before = ch.theta.copy()
rep = codec.maintain(ch, preset, mode="codec")
print("rep:", {k: v for k, v in rep.items() if k != "verified_mask"})
changed = np.nonzero(theta_before != ch.theta)[1]
print("changed cells:", changed)
print("new theta at changed:", ch.theta[0, changed])
print("old theta at changed:", theta_before[0, changed])
print("archive cluster means:", codec._cluster_means(ch.theta0))
print("fidelity:", float(ch.global_fidelity()[0]))
