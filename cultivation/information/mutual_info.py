"""Mutual information between bioelectric state and morphological outcome.

I(V; M): if the bioelectric layer genuinely controls morphogenesis, the
state V must carry high mutual information with the outcome M. We estimate
it on simulator data: sample initial states across attractor basins, run
the dynamics, classify the outcome, and measure MI between state features
and outcome class. The cultivation question — can I(V; M) be *increased*
(by reprogramming) or *lost* (by aging noise)? — becomes directly measurable.
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import mutual_info_score


def _discretize(x: np.ndarray, bins: int) -> np.ndarray:
    """Quantile binning to integer codes (robust to non-uniform features)."""
    if bins <= 1:
        return np.zeros_like(x, dtype=int)
    qs = np.quantile(x, np.linspace(0, 1, bins + 1)[1:-1])
    return np.searchsorted(qs, x, side="right")


def estimate_mi_joint(X: np.ndarray, y: np.ndarray, bins: int = 4) -> float:
    """Joint MI between a vector of continuous features and a discrete class.

    Discretizes each feature into `bins` levels, forms a joint code
    (product space), and computes I(joint_code; class) in bits. Exact for
    the binned approximation; report bin count alongside.
    """
    codes = np.zeros(len(X), dtype=np.int64)
    for j in range(X.shape[1]):
        codes = codes * bins + _discretize(X[:, j], bins)
    return float(mutual_info_score(codes, y)) / np.log(2.0)


def estimate_mi_features(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Per-feature MI (bits) via sklearn's KBNS estimator."""
    return mutual_info_classif(X, y, discrete_features=False) / np.log(2.0)
