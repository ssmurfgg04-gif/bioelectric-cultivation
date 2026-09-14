"""Debug: trace the post-release collapse in exp11 physics."""
import sys
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.morpho_engineering import (
    LatchingCollective, ClampProtocol, target_wildtype, discrete_fidelity,
    target_third_eye)

u = np.array([52, 8, -20, 50, 5, -50, 50, 5, -50, 80, 0.1])
col = LatchingCollective(n=100, seed=1)
col.set_target(target_wildtype(100))
col.set_state(target_wildtype(100) + col.rng.normal(0, 2.0, 100))
proto = ClampProtocol(u)
proto.apply(col, dt=0.1)
print("protocol:", proto.sites, "dur", proto.duration, "gap", proto.gap_scale)
target = target_third_eye(100)
t_elapsed = 0
for T in (50, 100, 200, 300, 400, 500):
    col.run(T - t_elapsed, dt=0.1)
    t_elapsed = T
    print(f"T={T}: fid={discrete_fidelity(col.V, target):.3f} "
          f"Vmin={col.V.min():.1f} Vmax={col.V.max():.1f} "
          f"nan={np.isnan(col.V).any()} "
          f"theta_min={col.theta.min():.1f} "
          f"anchor_min={col.theta_anchor.min():.1f} "
          f"anchor_max={col.theta_anchor.max():.1f}")
