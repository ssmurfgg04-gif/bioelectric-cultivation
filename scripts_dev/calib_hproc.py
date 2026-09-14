"""Calibration probe: paired-gain evaluation of procedure risk across seeds."""
import sys
sys.path.insert(0, ".")
from cultivation.inverse.design import eval_policy, HAND_CODEC
from experiments.exp8_fidelity import fidelity_target, REGIME, age_preset
import numpy as np

kw = dict(regime=REGIME, target0=fidelity_target, age_preset=age_preset)
u_none = np.array([105.0, 5.0, 6.0, 60.0, 105.0, 0.0, 0.0, 1.0])
for seed in (21, 22, 23):
    rn = eval_policy(u_none, seed=seed, **kw)["median"]
    rc = eval_policy(np.array(HAND_CODEC), seed=seed, **kw)["median"]
    rf = eval_policy(np.array(HAND_CODEC), seed=seed, h_proc=0.0, **kw)["median"]
    print(f"seed {seed}: none={rn:.1f} codec_cost={rc:.1f} (paired x{rc/rn:.3f}) "
          f"codec_free={rf:.1f} (paired x{rf/rn:.3f})")
