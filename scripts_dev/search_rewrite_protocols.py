"""Discover REWRITE protocols (A->B and B->A transitions) via CEM.

The rewritability test (Pezzulo & Levin 2021: re-writable memory medium)
needs protocols that overwrite an ESTABLISHED novel pattern with another —
a different inverse-design problem than exp11's (which always started from
wildtype). Hand-built composites plateau at 0.8 fidelity (the post-release
sag physics needs search-discovered overshoot compensation — exactly what
exp11's CEM found for the initial writes).

Search fitness: -(settled fidelity to DESTINATION - do-nothing baseline),
evaluated from a genuinely SOURCE-latched state (apply exp11's discovered
source protocol, settle, then apply the candidate). The baseline
subtraction is the anti-deception term (an A-latched tissue already scores
~0.7 against B — both share the wildtype background).

Saves: results/rewrite_protocols.json  (loaded by exp12's B6b — no re-search)
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.morpho_engineering import (
    LatchingCollective, ClampProtocol, target_wildtype, target_third_eye,
    target_dual_zone, discrete_fidelity,
)
from cultivation.inverse.cem import cem_optimize

N = 100
A = target_third_eye(N)
B = target_dual_zone(N)
WT = target_wildtype(N)

EXP11 = json.load(open("results/exp11_novel_morphology.json"))
U_THIRD = np.array(EXP11["discovered"]["third_eye"]["u"])


def make_source_state(seed: int, source_protocol=None) -> LatchingCollective:
    """A genuinely SOURCE-latched tissue. Default source = third_eye (via
    exp11's discovered protocol); pass a (u, n_sites) tuple to build a
    different source (e.g. dual_zone via the discovered A->B protocol —
    the B->A search MUST start from a genuinely B-latched state: the
    first version of this script got that wrong and 'discovered' a
    trivial A->A rewrite)."""
    col = LatchingCollective(n=N, seed=seed)
    col.set_target(WT)
    col.set_state(WT + col.rng.normal(0, 2.0, N))
    if source_protocol is None:
        ClampProtocol(U_THIRD, n_sites=3).apply(col, dt=0.1)
    else:
        u, ns = source_protocol
        ClampProtocol(np.asarray(u, float), n_sites=ns).apply(col, dt=0.1)
    col.run(250.0, dt=0.1)
    return col


def eval_transition(u, target, seed: int, n_sites: int = 4,
                    source_protocol=None) -> float:
    col = make_source_state(seed, source_protocol)
    ClampProtocol(np.asarray(u, float), n_sites=n_sites).apply(col, dt=0.1)
    col.run(300.0, dt=0.1)
    return discrete_fidelity(col.V, target)


def search(target, label: str, seeds=(5,), n_sites: int = 4,
           pop: int = 30, iters: int = 10, restarts: int = 2,
           source_protocol=None) -> dict:
    bounds = []
    for _ in range(n_sites):
        bounds += [(0, N - 1), (1, 25), (-70.0, -10.0)]
    bounds += [(20.0, 150.0), (0.05, 0.8)]

    u_null = np.array([30, 1, -50.0, 70, 1, -50.0, 5, 1, -20.0,
                       90, 1, -50.0, 40.0, 1.0])
    base = float(np.mean([eval_transition(u_null, target, s, n_sites,
                                          source_protocol)
                          for s in seeds]))
    print(f"[{label}] do-nothing baseline: {base:.3f}", flush=True)

    def fitness(u):
        fids = [eval_transition(u, target, s, n_sites, source_protocol)
                for s in seeds]
        return -(float(np.mean(fids)) - base)

    best_u, best_f, hist = None, np.inf, None
    for r in range(restarts):
        u, f, hist = cem_optimize(fitness, bounds, pop=pop, iters=iters,
                                  seed=200 * r + 7, verbose=False)
        if f < best_f:
            best_u, best_f, best_hist = u, f, hist
    fid_search = -best_f + base
    # validation on unseen seeds
    val = [eval_transition(best_u, target, s, n_sites, source_protocol)
           for s in (6, 7, 8)]
    print(f"[{label}] search fid {fid_search:.3f}  val {[round(v,3) for v in val]}"
          f"  mean {np.mean(val):.3f}", flush=True)
    return {"u": [float(x) for x in best_u], "n_sites": n_sites,
            "search_fid": fid_search, "val_fids": [float(v) for v in val],
            "val_mean": float(np.mean(val)), "baseline": base}


def main() -> dict:
    t0 = time.time()
    out = {}
    print("[rewrite-search] A (third_eye) -> B (dual_zone)...", flush=True)
    out["A_to_B"] = search(B, "B")
    print("[rewrite-search] B (dual_zone) -> A (third_eye)...", flush=True)
    # the B->A search starts from a GENUINELY B-latched state (apply the
    # discovered A->B protocol first)
    src_B = (np.array(out["A_to_B"]["u"]), out["A_to_B"]["n_sites"])
    out["B_to_A"] = search(A, "A", source_protocol=src_B)
    out["source_protocol"] = "exp11 discovered third_eye (loaded); B-source " \
                              "built via the discovered A->B protocol"
    out["search_wall_s"] = time.time() - t0
    path = "results/rewrite_protocols.json"
    json.dump(out, open(path, "w"), indent=1)
    print(f"[rewrite-search] -> {path} ({time.time() - t0:.0f}s)")
    return out


if __name__ == "__main__":
    main()
