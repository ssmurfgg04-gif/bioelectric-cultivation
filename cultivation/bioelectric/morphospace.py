"""Morphospace utilities: target patterns, polarity and head-identity metrics.

Planarian bioelectric anatomy (Levin lab): the anterior (head) region is
depolarized relative to the trunk; bioelectric reprogramming that forces a
tail region depolarized for ~24h stably rewrites the regeneration target
(two-headed morphology persisting across subsequent amputations — Durant et
al. 2017; Pezzulo & Levin 2021 modeled it as bistable somatic memory).
"""

from __future__ import annotations

import numpy as np


def wildtype_target(n: int, head_v: float = -20.0, trunk_v: float = -50.0,
                    head_fraction: float = 0.25) -> np.ndarray:
    """Wild-type planarian-like axis: depolarized head, hyperpolarized trunk."""
    t = np.full(n, trunk_v)
    t[: int(n * head_fraction)] = head_v
    return t


def twoheaded_target(n: int, head_v: float = -20.0, trunk_v: float = -50.0,
                     head_fraction: float = 0.25) -> np.ndarray:
    """Reprogrammed axis: depolarized zones at BOTH ends (two-headed worm)."""
    t = np.full(n, trunk_v)
    h = int(n * head_fraction)
    t[:h] = head_v
    t[-h:] = head_v
    return t


def pattern_error(V: np.ndarray, target: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(V) - np.asarray(target)) ** 2)))


def head_likeness(V: np.ndarray, region: slice) -> float:
    """Head-identity score of a region in [0, 1].

    0 = fully trunk-like (hyperpolarized, <= -40 mV); 1 = fully head-like
    (depolarized, >= -25 mV). Linear in between; threshold at -32.5 mV.
    """
    seg = np.asarray(V)[region]
    return float(np.clip((seg.mean() + 40.0) / 15.0, 0.0, 1.0))


def polarity_error(V: np.ndarray, target: np.ndarray) -> float:
    """Signed pattern error along the axis: >0 means anterior is too hyperpolarized."""
    diff = np.asarray(V) - np.asarray(target)
    return float(np.mean(diff))


def basin_escape(V: np.ndarray, target: np.ndarray, tol: float = 8.0) -> bool:
    """True if the state has left the target's basin (rough check)."""
    return pattern_error(V, target) > tol
