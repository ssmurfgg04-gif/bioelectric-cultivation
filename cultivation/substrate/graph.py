"""Stage 5 (Ascension) — substrate independence.

THE CLAIM
---------
Everything the map does — target-memory attractors, junction-carried
readout (M25), regeneration through the collective (M26c/M28) — is a
property of the COUPLED DYNAMICS on a graph, not of the 1-D chain. The
chain was always one adjacency among many; the cultivation roadmap's
last phase is to show the machinery survives the death of the line:
same ODEs, arbitrary topology, same regeneration semantics.

WHAT TRANSFERS UNCHANGED
------------------------
* The dynamics: BioElectricCollective already takes an arbitrary
  `adjacency` — step() is graph-native (Laplacian + degrees).
* The target-memory attractor: a region labeling (identity zones) is
  an attractor on any connected substrate.
* M25's readout rule generalizes: a committing cell inherits from an
  ALREADY-COMMITTED GRAPH NEIGHBOR (the chain walk is just BFS on a
  path); under blockade the blind-guess fallback is identical.

WHAT IS NEW HERE
----------------
`regrow_graph` — the regeneration walk on an arbitrary graph: BFS from
the wound boundary inward, each cell inheriting theta (+ identity
noise, + M25 guess under blockade) from its committed neighbor. On the
path topology this reduces to the chain walk's inheritance structure
(not bit-exact — different RNG draw order — but the same mechanism).
"""
from __future__ import annotations

import numpy as np

from cultivation.bioelectric.collective import (
    BioElectricCollective, line_adjacency,
)


# ---------------------------------------------------------------- topologies
def path(n: int) -> np.ndarray:
    return line_adjacency(n, k=1, ring=False)


def grid_2d(rows: int, cols: int) -> np.ndarray:
    """rows x cols 2D lattice, row-major node ids."""
    n = rows * cols
    A = np.zeros((n, n))
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if c + 1 < cols:
                A[i, i + 1] = A[i + 1, i] = 1.0
            if r + 1 < rows:
                A[i, i + cols] = A[i + cols, i] = 1.0
    return A


def random_regular(n: int, k: int = 3, seed: int = 7) -> np.ndarray:
    """Random k-regular graph (pairing model with retries)."""
    rng = np.random.default_rng(seed)
    for _ in range(200):
        stubs = np.repeat(np.arange(n), k)
        rng.shuffle(stubs)
        A = np.zeros((n, n))
        ok = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            if u == v or A[u, v]:
                ok = False
                break
            A[u, v] = A[v, u] = 1.0
        if ok:
            return A
    raise RuntimeError("pairing model failed; increase retries")


def scale_free(n: int, seed: int = 11, m: int = 2) -> np.ndarray:
    """Preferential-attachment (Barabasi-Albert) graph."""
    rng = np.random.default_rng(seed)
    A = np.zeros((n, n))
    deg = np.zeros(n)
    # seed clique of m+1
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            A[i, j] = A[j, i] = 1.0
            deg[i] += 1
            deg[j] += 1
    for i in range(m + 1, n):
        p = deg[:i] / deg[:i].sum()
        targets = rng.choice(i, size=m, replace=False, p=p)
        for t in targets:
            A[i, t] = A[t, i] = 1.0
            deg[i] += 1
            deg[t] += 1
    return A


# ----------------------------------------------------------------- collective
class GraphCollective(BioElectricCollective):
    """The collective on an arbitrary substrate + graph-native regen."""

    def __init__(self, adjacency: np.ndarray, seed: int | None = 0, **kw):
        n = adjacency.shape[0]
        super().__init__(n=n, adjacency=adjacency, seed=seed, **kw)

    def regrow_graph(self, region: list[int], cell_period: float = 0.8,
                     dt: float = 0.1, noise: float = 0.6) -> None:
        """BFS regeneration through the graph (M25-consistent).

        Walk order: BFS from the boundary (committed intact neighbors of
        the region) inward; each committing cell inherits from the
        committed neighbor it was discovered THROUGH. Under blockade the
        M25 blind-guess replaces the inheritance read, exactly as in the
        chain."""
        region_set = set(region)
        idx = list(np.arange(self.n)[region]) if not region_set \
            else list(region)
        if not idx:
            return
        r = float(self.gap_scale)
        wound_center = float(np.mean(self.theta[idx]))
        steps_per_cell = max(1, int(round(cell_period / dt)))

        # frontier seeds: region cells adjacent to committed intact tissue
        parent_of: dict[int, int] = {}
        frontier: list[int] = []
        for i in idx:
            nbrs = [j for j in np.where(self.A[i] > 0)[0]
                    if j not in region_set]
            if nbrs:
                parent_of[i] = int(max(
                    nbrs, key=lambda j: -abs(self.theta[j] - wound_center)))
                frontier.append(i)
        if not frontier:            # interior region: seed from wound state
            frontier = idx[:1]
            parent_of[frontier[0]] = frontier[0]

        visited = set(frontier)
        order: list[tuple[int, int]] = [(i, parent_of[i]) for i in frontier]
        queue = list(frontier)
        while queue:
            i = queue.pop(0)
            for j in np.where(self.A[i] > 0)[0]:
                if int(j) in region_set and int(j) not in visited:
                    visited.add(int(j))
                    parent_of[int(j)] = int(i)
                    order.append((int(j), int(i)))
                    queue.append(int(j))

        for i, src in order:
            for _ in range(steps_per_cell):
                self.step(dt)
            if r >= 1.0:
                theta_new = self.theta[src] + self.rng.normal(0.0, noise)
            else:
                guess = wound_center + self.rng.normal(
                    0.0, self.blastema_readout_noise)
                theta_new = r * (self.theta[src]
                                 + self.rng.normal(0.0, noise)) \
                    + (1.0 - r) * guess
            self.theta[i] = theta_new
            self.V[i] = theta_new


# ---------------------------------------------------------------------------
# PERF (final-session review, bit-exact): the vectorized form of exp208's
# classify — the house classifier duplicated across the landed experiment
# bodies. The landed bodies stay byte-frozen (their pins assert the
# docstring/header shas and their deposits assert bit-exactness); this
# helper is the single shared implementation for all FUTURE consumers.
# Bit-equality with the reference loop form is asserted by
# tests/test_deposits_and_safety.py over a fixed battery of graphs.
def classify_vectorized(T, W):
    """exp208's classes, vectorized. Returns the same dict of masks as
    the reference loop form: boundary (the cells whose label differs
    from a ring neighbor), junction (degree >= 2 off the boundary),
    interior, and the integer class array (0 boundary / 1 junction /
    2 interior). W's support (|W| > 0) defines degree, exactly as the
    reference."""
    Td = np.asarray(T, dtype=float)
    n = len(Td)
    bnd = (Td != np.roll(Td, 1)) | (Td != np.roll(Td, -1))
    support = np.abs(W) > 0
    iu = np.triu_indices(n, 1)
    keep = support[iu]
    deg = np.zeros(n, dtype=int)
    np.add.at(deg, iu[0][keep], 1)
    np.add.at(deg, iu[1][keep], 1)
    pj = deg >= 2
    cls = np.zeros(n, dtype=int)
    cls[pj] = 1
    cls[bnd] = 0
    return {"boundary": bnd, "junction": pj & ~bnd,
            "interior": ~(bnd | pj), "class": cls}
