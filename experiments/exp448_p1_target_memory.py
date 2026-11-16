"""exp448 — PRIMARY P1: bioelectric target memory (docs/PRIMARIES.md).

Gates frozen in docs/PRIMARIES.md (commit 6d64990) before this file ran.
Run: python -m experiments.exp448_p1_target_memory
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.stats import binomtest

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import head_likeness, wildtype_target

N, DT = 100, 0.1
SEEDS = list(range(100, 120))
DOSES = [-35.0, -30.0, -25.0, -20.0, -15.0]
TAIL = slice(3 * N // 4, N)


def _make(seed: int, eps: float = 0.04) -> BioElectricCollective:
    c = BioElectricCollective(n=N, seed=seed, noise_std=0.3, eps=eps)
    c.set_target(wildtype_target(N))
    c.run(10, dt=DT)
    return c


def _amputate_rounds(c, rounds):
    h = None
    for _ in range(rounds):
        c.amputate(slice(85, 100), wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(slice(85, 100), cell_period=0.8, dt=DT, noise=0.6)
        c.run(15, dt=DT)
        h = head_likeness(c.V, TAIL)
    return h


def _protocol(c, clamp_v, rounds):
    c.block_gap_junctions(0.05)
    if clamp_v is not None:
        c.clamp(TAIL, clamp_v)
    c.run(24, dt=DT)
    c.restore_gap_junctions(1.0)
    c.release_clamps()
    c.run(20, dt=DT)
    return _amputate_rounds(c, rounds)


def _seed_job(seed):
    out = {"seed": seed,
           "A": _protocol(_make(seed), -20.0, 2),
           "B": _protocol(_make(seed), None, 1),
           "C": _protocol(_make(seed, eps=0.0), -20.0, 2),
           "D": {v: _protocol(_make(seed), v, 1) for v in DOSES}}
    return out


def main() -> dict:
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as ex:
        rows = list(ex.map(_seed_job, SEEDS))
    A = np.array([r["A"] for r in rows]); B = np.array([r["B"] for r in rows])
    C = np.array([r["C"] for r in rows])
    D = {v: float(np.mean([r["D"][v] for r in rows])) for v in DOSES}
    nA, nB, nC = int((A > 0.7).sum()), int((B < 0.35).sum()), int((C < 0.35).sum())
    dvals = [D[v] for v in DOSES]
    mono = all(dvals[i + 1] >= dvals[i] - 0.02 for i in range(len(dvals) - 1))
    g = {"G1a": nA >= 18, "G1b": nB >= 18, "G1c": nC >= 18,
         "G1d": mono and D[-35.0] < 0.35 and D[-20.0] > 0.7}
    p = binomtest(nA, 20, 0.5, alternative="greater").pvalue
    res = {"primary": "P1", "seeds": SEEDS, "A_h": A.tolist(), "B_h": B.tolist(),
           "C_h": C.tolist(), "dose_mean_h": {str(k): v for k, v in D.items()},
           "counts": {"A_rewritten": nA, "B_not": nB, "C_not": nC},
           "gates": g, "p_value": float(p), "PASS": all(g.values())}
    for k, v in g.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print(f"A rewritten {nA}/20 | B not {nB}/20 | C(eps=0) not {nC}/20")
    print("dose mean h:", {k: round(v, 3) for k, v in D.items()})
    print(f"p = {p:.3g}  -> P1 {'PASS' if res['PASS'] else 'FAIL'}")
    os.makedirs("results", exist_ok=True)
    json.dump(res, open("results/exp448_p1_target_memory.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
