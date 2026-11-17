"""exp464 — PRIMARY P14: does target memory persist in 2D tissue?
Frozen in docs/PRIMARIES_ROUND7.md (commit b1d2c1b)."""
from __future__ import annotations
import json, os
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import head_likeness

S = 20
N = S * S
SEEDS = list(range(1140, 1160))
TAIL = np.arange(15 * S, N)


def grid_adjacency(s):
    A = np.zeros((s * s, s * s))
    for r in range(s):
        for c in range(s):
            i = r * s + c
            if r + 1 < s: A[i, i + s] = A[i + s, i] = 1
            if c + 1 < s: A[i, i + 1] = A[i + 1, i] = 1
    return A


A2 = grid_adjacency(S)
TARGET = np.full(N, -50.0); TARGET[: 5 * S] = -20.0


def _arm(seed, clamp, eps):
    c = BioElectricCollective(n=N, seed=seed, noise_std=0.3, eps=eps, adjacency=A2)
    c.set_target(TARGET); c.run(10, dt=0.1)
    c.block_gap_junctions(0.05)
    if clamp: c.clamp(TAIL, -20.0)
    c.run(24, dt=0.1)
    c.restore_gap_junctions(1.0); c.release_clamps()
    c.run(200, dt=0.1)
    return float(head_likeness(c.V, TAIL))


def _job(seed):
    return seed, _arm(seed, True, 0.04), _arm(seed, False, 0.04), _arm(seed, True, 0.0)


def main():
    with ProcessPoolExecutor(os.cpu_count() or 1) as ex:
        rows = list(ex.map(_job, SEEDS))
    A = np.array([r[1] for r in rows]); B = np.array([r[2] for r in rows]); C = np.array([r[3] for r in rows])
    g = {"G14a": bool((A > 0.7).sum() >= 18), "G14b": bool((B < 0.35).sum() >= 18), "G14c": bool((C < 0.35).sum() >= 18)}
    print(f"A rewritten {(A>0.7).sum()}/20 (mean h {A.mean():.2f}) | B not {(B<0.35).sum()}/20 (mean {B.mean():.2f}) | C(eps=0) not {(C<0.35).sum()}/20 (mean {C.mean():.2f})")
    res = {"primary": "P14", "A": A.tolist(), "B": B.tolist(), "C": C.tolist(), "gates": g, "PASS": all(g.values())}
    print(" | ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in g.items()), f"-> P14 {'PASS' if res['PASS'] else 'FAIL'}")
    json.dump(res, open("results/exp464_p14_2d_memory.json", "w"), indent=1)


if __name__ == "__main__":
    main()
