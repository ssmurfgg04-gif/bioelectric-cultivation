"""Debug the regeneration_test novel-identity failure."""
import sys
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.morpho_engineering import (
    LatchingCollective, ClampProtocol, target_wildtype, target_third_eye,
    discrete_fidelity, LEVELS)
from cultivation.bioelectric.fidelity import quantize

col = LatchingCollective(n=100, seed=1)
col.set_target(target_wildtype(100))
col.set_state(target_wildtype(100) + col.rng.normal(0, 2.0, 100))
u = np.array([52, 8, -20, 50, 5, -50, 50, 5, -50, 80, 0.1])
ClampProtocol(u).apply(col, dt=0.1)
col.run(100.0, dt=0.1)
target = target_third_eye(100)
print("pre-amputation fidelity:", discrete_fidelity(col.V, target))
print("pre-amputation anchor zone 45-60:", np.round(col.theta_anchor[45:60], 1))

c2 = LatchingCollective(n=100, seed=101)
c2.set_target(col.theta.copy())
c2.set_state(col.V.copy())
c2.set_anchor(col.theta_anchor.copy())
sl = slice(49, 64)
c2.amputate(sl)
print("boundary cell 48: theta", round(c2.theta[48], 1),
      "anchor", round(c2.theta_anchor[48], 1))
c2.regrow(sl)
print("post-regrow theta 49-64:", np.round(c2.theta[49:64], 1))
print("post-regrow anchor 49-64:", np.round(c2.theta_anchor[49:64], 1))
c2.run(150.0, dt=0.1)
q_reg = quantize(c2.V, LEVELS)
q_tar = quantize(target, LEVELS)
q_wt = quantize(target_wildtype(100), LEVELS)
regrown = np.zeros(100, bool); regrown[sl] = True
novel = [i for i in range(100) if regrown[i] and q_tar[i] != q_wt[i]]
trunk = [i for i in range(100) if regrown[i] and q_tar[i] == q_wt[i]]
print("post-settle V 49-64:", np.round(c2.V[49:64], 1))
print("novel cells in region:", novel)
print("q_reg at novel:", [int(q_reg[i]) for i in novel])
print("q_tar at novel:", [int(q_tar[i]) for i in novel])
