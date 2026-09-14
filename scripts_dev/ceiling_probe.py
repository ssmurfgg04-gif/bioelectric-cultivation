"""Find the physical ceiling for third_eye with hand-designed protocols."""
import sys
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.morpho_engineering import evaluate_protocol, target_third_eye

target = target_third_eye(100)
protos = {
    "clean narrow (52,7,-20)x100,gap0.1": np.array([52, 7, -20, 10, 1, -50, 90, 1, -50, 100, 0.1]),
    "clean wide (52,10,-20)x100,gap0.1": np.array([52, 10, -20, 10, 1, -50, 90, 1, -50, 100, 0.1]),
    "exact (52,7,-20)x150,gap0.05": np.array([52, 7, -20, 10, 1, -50, 90, 1, -50, 150, 0.05]),
    "exact volt -18 x150 gap0.05": np.array([52, 7, -18, 10, 1, -50, 90, 1, -50, 150, 0.05]),
    "two-site edges (46,3,-20)+(58,3,-20)": np.array([46, 3, -20, 58, 3, -20, 90, 1, -50, 150, 0.05]),
}
for name, u in protos.items():
    r = evaluate_protocol(u, target, seed=1)
    print(f"{name}: settled {r['fid_settled']:.3f} anchor {r['anchor_latched']:.3f}")
