"""Smoke test: the fixed three-factor rule converges (no divergence)."""
import sys, time
sys.path.insert(0, ".")
import numpy as np
from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.neural.interface import MindBodyInterface

N = 60
ZONE = slice(20, 30)
WANTED = 10.0

def fresh_tissue(seed=0):
    t = BioElectricCollective(n=N, seed=seed)
    base = np.full(N, -50.0)
    base[: N // 4] = -20.0
    t.set_target(base)
    t.set_state(base + t.rng.normal(0, 1.5, N))
    t.run(10.0, dt=0.1)
    return t

for arm in ("coherent", "random", "tonic"):
    ifc = MindBodyInterface(seed=7)
    t0 = time.time()
    curve = []
    for ep in range(60):
        tissue = fresh_tissue(0)
        mode = "coherent" if arm != "random" else "random"
        rep = ifc.train_epoch(tissue, ZONE, WANTED, mode, 1.2,
                              reward_mode="tonic" if arm == "tonic" else "feedback")
        tissue = fresh_tissue(0)
        infl = ifc.effective_influence(tissue, ZONE, "coherent", 1.2)
        curve.append(infl["shift_mV"])
    c = np.array(curve)
    finite = np.isfinite(c).all()
    print(f"{arm:9s}: final {curve[-1]:+8.2f} mV  peak {np.max(np.abs(curve)):6.2f}  "
          f"|W| {np.linalg.norm(ifc.W_plastic):7.2f}  finite={finite}  ({time.time()-t0:.0f}s)")
    print(f"           curve[0:60:6] = {np.round(c[::6], 1)}")
    print(f"           zone_shift last epoch: {rep['zone_shift']:+.2f} (wanted {WANTED})")

# coherence check with the attention subset
ifc = MindBodyInterface(seed=7)
I_coh = ifc.drive("coherent", 1.2)
I_rnd = ifc.drive("random", 1.2)
print(f"\ncoherence: coherent-drive {ifc.coherence(I_coh):+.3f} vs random-drive {ifc.coherence(I_rnd):+.3f}")

# policy save/load roundtrip
p = ifc.save_policy()
ifc2 = MindBodyInterface.load_policy(p)
t = fresh_tissue(0)
a = ifc.effective_influence(t, ZONE, "coherent", 1.2)["shift_mV"]
t = fresh_tissue(0)
b = ifc2.effective_influence(t, ZONE, "coherent", 1.2)["shift_mV"]
print(f"save/load roundtrip: {a:+.3f} vs {b:+.3f} (identical={np.isclose(a,b)})")
