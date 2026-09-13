"""C. elegans connectome loader — REAL data.

Sources (downloaded by the research phase, see research/data/):
- herm_full_edgelist.csv — Cook et al. 2019, Nature 571 (whole-animal
  connectomes of both C. elegans sexes), hermaphrodite, 7,378 edges:
  4,681 chemical + 2,698 electrical (gap junctions) over 1,308 cells.
- CElegansNeuronTables.xls / celegans_connectome.csv — OpenWorm
  (White et al. 1986 lineage): 3,362 neuron-neuron edges
  (1,084 electrical + 2,278 chemical).

The GAP-JUNCTION (electrical) connectome is the biologically relevant one
for this project: innexin-based electrical synapses — the same coupling
machinery as non-neural cell collectives.
"""

from __future__ import annotations

import csv
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "research", "data")


def load_celegans_gap_junctions(prefer: str = "cook2019") -> tuple[np.ndarray, list[str]]:
    """Load the neuron-neuron gap-junction adjacency (weighted, symmetric).

    Returns (adjacency, names). Falls back cook2019 -> openworm.
    """
    path = os.path.join(DATA_DIR, "herm_full_edgelist.csv")
    if prefer == "cook2019" and os.path.exists(path):
        edges: dict[tuple[str, str], int] = {}
        names: set[str] = set()
        with open(path, newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) < 4:
                    continue
                src, trg, typ = row[0], row[1], row[2]
                w = row[3] if len(row) > 3 else "1"
                if "electrical" in typ.lower() or "gap" in typ.lower():
                    try:
                        weight = int(float(w))
                    except ValueError:
                        weight = 1
                    edges[(src, trg)] = edges.get((src, trg), 0) + weight
                    names.update((src, trg))
        if edges:
            names = sorted(names)
            idx = {nm: i for i, nm in enumerate(names)}
            A = np.zeros((len(names), len(names)))
            for (s, t), w in edges.items():
                if s == t:
                    continue
                A[idx[s], idx[t]] += w
                A[idx[t], idx[s]] += w  # gap junctions are bidirectional
            return A, names

    path = os.path.join(DATA_DIR, "celegans_connectome.csv")
    if os.path.exists(path):
        edges = {}
        names = set()
        with open(path, newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            cols = [h.strip().lower() for h in header] if header else []
            def col(cands):
                for c in cands:
                    if c in cols:
                        return cols.index(c)
                return None
            i_src = col(["source", "origin", "from", "pre"])
            i_trg = col(["target", "destination", "to", "post"])
            i_typ = col(["type", "connection type", "kind"])
            i_w = col(["weight", "synapses", "count"])
            for row in reader:
                if len(row) <= max(x for x in (i_src, i_trg, i_typ or 0) if x is not None):
                    continue
                typ = (row[i_typ].lower() if i_typ is not None else "electrical")
                if "elec" in typ or "gap" in typ:
                    s, t = row[i_src], row[i_trg]
                    w = 1
                    if i_w is not None:
                        try:
                            w = int(float(row[i_w]))
                        except (ValueError, IndexError):
                            w = 1
                    edges[(s, t)] = edges.get((s, t), 0) + w
                    names.update((s, t))
        names = sorted(names)
        idx = {nm: i for i, nm in enumerate(names)}
        A = np.zeros((len(names), len(names)))
        for (s, t), w in edges.items():
            if s == t:
                continue
            A[idx[s], idx[t]] += w
            A[idx[t], idx[s]] += w
        return A, names

    raise FileNotFoundError("no connectome data found in research/data/")


def motif_samples(A: np.ndarray, size: int = 8, n_samples: int = 30,
                  seed: int = 0) -> list[np.ndarray]:
    """Sample connected `size`-node subgraphs (induced motifs) for exact Phi."""
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    deg = (A > 0).sum(axis=1)
    pool = np.where(deg > 0)[0]
    motifs = []
    tries = 0
    while len(motifs) < n_samples and tries < n_samples * 40:
        tries += 1
        seed_node = rng.choice(pool)
        # BFS growth
        chosen = {int(seed_node)}
        frontier = [int(seed_node)]
        while len(chosen) < size and frontier:
            u = frontier.pop(rng.integers(len(frontier)) if len(frontier) else 0)
            nbrs = np.where(A[u] > 0)[0]
            rng.shuffle(nbrs)
            for v in nbrs:
                if int(v) not in chosen:
                    chosen.add(int(v))
                    frontier.append(int(v))
                if len(chosen) == size:
                    break
        if len(chosen) == size:
            idx = sorted(chosen)
            motifs.append(A[np.ix_(idx, idx)])
    return motifs
