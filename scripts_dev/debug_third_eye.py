"""Debug: where does the third_eye protocol leave errors, and why does
partial-amputation recovery fail?"""
import sys
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.morpho_engineering import (
    LatchingCollective, ClampProtocol, target_wildtype, target_third_eye,
    discrete_fidelity, LEVELS)
from cultivation.bioelectric.fidelity import quantize
import json

state = json.load(open("scripts_dev/exp11_state.json"))
u = np.array(state["discovered"]["third_eye"]["u"])
proto = ClampProtocol(u)
print("protocol:", proto.sites, "dur", proto.duration, "gap", proto.gap_scale)

col = LatchingCollective(n=100, seed=1)
col.set_target(target_wildtype(100))
col.set_state(target_wildtype(100) + col.rng.normal(0, 2.0, 100))
proto.apply(col, dt=0.1)
col.run(300.0, dt=0.1)
target = target_third_eye(100)
q_reg = quantize(col.V, LEVELS)
q_tar = quantize(target, LEVELS)
wrong = np.nonzero(q_reg != q_tar)[0]
print("wrong cells:", wrong.tolist())
print("anchor 40-65:", np.round(col.theta_anchor[40:65], 1))
print("theta  40-65:", np.round(col.theta[40:65], 1))
print("V      40-65:", np.round(col.V[40:65], 1))
