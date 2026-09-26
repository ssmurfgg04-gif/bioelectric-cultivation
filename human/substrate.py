"""The human substrate ingestion layer (real HCP data, zero knobs).

THE PRE-REGISTERED PREPROCESSING RULE (frozen at the exp401
pre-registration commit; every step deterministic, nothing tuned to
the outcome):
  1. W = fc.copy(); diagonal -> 0 (the raw matrix carries 1.0 self-
     coupling; the model's adjacency is strictly off-diagonal);
  2. negatives -> 0 (2.08% of edges; the model's conductance matrix is
     non-negative — an inhibitory edge is out of scope, disclosed);
  3. per-node symmetric top-6: each node keeps its 6 strongest FC
     neighbors; the kept edge set is symmetrized by max (the pre-named
     connectivity ladder {6, 8, 10, 12, 16}: the FIRST k on the ladder
     that yields a fully connected 400-node graph — k=6 connects all
     400, disclosed in the deposit);
  4. global scale: W *= 0.4 / mean(row-sum) — the planarian path-
     regime comparability rule (the validated 1-D machinery runs at
     interior degree 2 x g_gap 0.20 = 0.4 total conductance per cell;
     putting the human graph's per-node coupling in the SAME regime is
     the disclosed, untuned comparability choice).
The dynamical parameters (gamma .25, g_gap .20, eps .04, mu .015,
noise .30, blastema_readout_noise 18.0) keep the planarian defaults
EVERYWHERE — no parameter was fitted on human data.
"""
from __future__ import annotations

import hashlib
import os

import numpy as np

_FC_PATH = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "data", "human_fc_schaefer400.npy")

# sha256 of the committed real-data file (pinned at ingestion; exp401's
# H1 asserts the working tree's copy against this digest).
FC_SHA256 = "9c8cc9155c2f96e680db9730e25c0c9d56f643949378afb28250a462d9b12243"

LADDER = (6, 8, 10, 12, 16)
TARGET_MEAN_ROW_SUM = 0.4


def load_human_fc(path: str | None = None) -> np.ndarray:
    """Load the committed real HCP group-average FC (Schaefer-400)."""
    p = path or _FC_PATH
    with open(p, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    if digest != FC_SHA256:
        raise AssertionError("human FC sha mismatch: %s" % digest)
    fc = np.load(p)
    assert fc.shape == (400, 400), fc.shape
    assert np.allclose(fc, fc.T, atol=1e-12), "FC not symmetric"
    return fc


def build_human_adjacency(fc: np.ndarray, k: int | None = None) -> np.ndarray:
    """The pre-registered preprocessing rule (see the module docstring).

    k=None walks the pre-named ladder and returns the first k that
    connects all 400 nodes; an explicit k must also connect fully
    (fail=STOP either way)."""
    W0 = np.clip(np.asarray(fc, dtype=float).copy(), 0.0, None)
    np.fill_diagonal(W0, 0.0)
    ladder = (k,) if k is not None else LADDER
    for kk in ladder:
        Wk = np.zeros_like(W0)
        for i in range(W0.shape[0]):
            idx = np.argsort(W0[i])[::-1][:kk]
            Wk[i, idx] = W0[i, idx]
        W = np.maximum(Wk, Wk.T)          # symmetric keep set
        if _connected(W):
            W = W * (TARGET_MEAN_ROW_SUM / W.sum(axis=1).mean())
            assert np.allclose(W, W.T, atol=1e-12)
            assert abs(W.diagonal()).max() == 0.0
            return W
    raise AssertionError("no ladder k connects the graph")


def _connected(W: np.ndarray) -> bool:
    A = (W > 0).astype(np.int8)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v in np.where(A[u])[0]:
            if int(v) not in seen:
                seen.add(int(v))
                stack.append(int(v))
    return len(seen) == W.shape[0]


def human_target(W: np.ndarray, n_zones: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """The deterministic data-shaped identity target: order the nodes by
    the leading eigenvector of the human adjacency (Fiedler-style
    ordering, deterministic), partition into n_zones equal blocks, and
    assign the house voltage ladder centers ([-50, -40, -30, -20, -10]
    for 5 zones — the same synthetic-target semantics as the planarian
    corpus: the target is an identity map, not a fitted quantity)."""
    vals, vecs = np.linalg.eigh(W)
    order = np.argsort(vecs[:, -1])
    n = W.shape[0]
    assert n % n_zones == 0
    zones = np.zeros(n, dtype=int)
    per = n // n_zones
    centers = np.linspace(-50.0, -10.0, n_zones)
    for z in range(n_zones):
        zones[order[z * per:(z + 1) * per]] = z
    return centers[zones], zones
