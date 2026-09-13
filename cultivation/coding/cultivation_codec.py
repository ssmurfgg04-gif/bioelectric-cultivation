"""The cultivation codec: read -> denoise -> verify -> write -> repeat.

The computational form of "cultivation as ongoing maintenance of the
morphogenetic code".

Architecture (informed by the helix-codec stress findings AND by a
documented negative result of our own):

  - STORING RS PARITY AS VOLTAGE SETPOINTS FAILS: engineered parity clusters
    hold sharp, non-natural values that the sheet's smoothing dynamics
    (homeostatic plasticity + pattern interdiffusion) actively erode within
    decades. Distributing redundancy as tissue setpoints is fought by the
    physics. (Negative result, kept in the record.)

  - THE VIABLE DESIGN: parity lives OUT-OF-BAND — the genomic archive
    (theta0: DNA stores the youthful target and does not drift like
    tissue). The living tissue is the noisy CHANNEL carrying a copy of
    that target. Maintenance reads the tissue through the aging channel
    (measurement noise, dropout, corrupted clusters), DENOISES with
    gap-junction belief propagation (the coupling graph is the consensus
    decoder), VERIFIES against the archive with a strict agreement
    threshold (no silent writes — the F3 lesson), and writes back a
    bounded budget of cells toward the archived youthful values (the F5
    lesson: intervene before capacity is exhausted).

The long-chain cascade architecture (outer RS + inner BP + consensus +
digest) from helix-codec is preserved conceptually; the RS layer runs at
the archive-integrity level (unit-tested in tests/test_units.py) while the
tissue-level decoder is BP + archive verification.
"""

from __future__ import annotations

import numpy as np

from .reed_solomon import ClusterRSCodec
from .belief_prop import bp_smooth


class CultivationCodec:
    def __init__(self, n_clusters: int = 12, k_clusters: int = 8,
                 n_cells: int = 60, budget_per_cycle: int = 4, levels: int = 8,
                 agreement_threshold: float = 0.70):
        self.n_clusters = n_clusters
        self.k_clusters = k_clusters
        self.n_cells = n_cells
        self.budget = budget_per_cycle
        self.levels = levels
        self.agreement_threshold = agreement_threshold
        self.codec = ClusterRSCodec(n_clusters, k_clusters, levels=levels)
        self.cluster_len = n_cells // n_clusters
        # cluster adjacency (1D chain of clusters)
        A = np.zeros((n_clusters, n_clusters))
        for i in range(n_clusters - 1):
            A[i, i + 1] = A[i + 1, i] = 1.0
        self.A_cluster = A
        # ledger
        self.cycles = 0
        self.decode_failures = 0
        self.restored_cells = 0

    # ------------------------------------------------------------------ utils
    def _cluster_means(self, theta: np.ndarray) -> np.ndarray:
        return theta.reshape(self.n_clusters, self.cluster_len).mean(axis=1)

    def _cluster_dead(self, senesced: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        frac = senesced.reshape(self.n_clusters, self.cluster_len).mean(axis=1)
        return frac > threshold

    # ------------------------------------------------------------- maintenance
    def maintain(self, cohort, preset: dict, mode: str = "codec") -> dict:
        """One maintenance cycle over an AgingCohort.

        mode='codec' : read -> BP denoise -> verify vs archive -> budgeted
                       write-back (the cultivation codec).
        mode='local' : local information only — no archive, no BP; a fully
                       dead cluster's target is simply gone.
        """
        self.cycles += 1
        K = cohort.K
        rng = cohort.rng
        restored = 0
        verified = 0
        failures = 0

        archive_means = self._cluster_means(cohort.theta0)

        for i in range(K):
            if not cohort.alive[i]:
                continue
            theta_i = cohort.theta[i]
            sen_i = cohort.senesced[i]
            dead_clusters = self._cluster_dead(sen_i)
            cluster_frac = sen_i.reshape(
                self.n_clusters, self.cluster_len).mean(axis=1)
            if sen_i.sum() == 0:
                continue

            if mode == "codec":
                # 1. READ: noisy cluster-level observation with dropout
                obs = self._cluster_means(theta_i) + rng.normal(
                    0, preset["meas_noise_mV"], self.n_clusters)
                readable = ~dead_clusters & (
                    rng.random(self.n_clusters) > preset["dropout"])
                # 2. DENOISE: BP smoothing fills unreadable/dead clusters
                #    from the coupling graph (the consensus decoder)
                denoised = bp_smooth(
                    obs[None, :], self.A_cluster, readable[None, :],
                    noise_var=preset["meas_noise_mV"] ** 2, iters=20,
                )[0]
                # 3. VERIFY: strict agreement with the genomic archive —
                #    refuse to write if the read is not trustworthy
                lv_span = (self.codec.V_MAX - self.codec.V_MIN) / (self.levels - 1)
                agreement = float(np.mean(
                    np.abs(denoised[readable] - archive_means[readable])
                    <= 1.5 * lv_span)) if readable.any() else 0.0
                if agreement < self.agreement_threshold:
                    failures += 1
                    continue  # unverified read — REFUSE to write
                verified += 1
                target_v = archive_means  # the archived youthful values
            else:
                target_v = None  # local mode: reconstruct lazily below

            # 4. WRITE: restore up to budget senesced cells, worst first
            order = np.argsort(cluster_frac)[::-1]
            remaining = self.budget
            for c in order:
                if remaining <= 0:
                    break
                if cluster_frac[c] <= 0:
                    continue
                if mode == "codec":
                    tgt_v = float(target_v[c])
                else:
                    nb = [c - 1, c + 1]
                    nb = [x for x in nb
                          if 0 <= x < self.n_clusters and cluster_frac[x] <= 0.3]
                    if not nb:
                        continue  # no local information — cannot restore
                    tgt_v = float(np.mean(self._cluster_means(theta_i)[nb]))
                cells_in = np.arange(c * self.cluster_len, (c + 1) * self.cluster_len)
                dead_cells = cells_in[sen_i[cells_in]]
                if len(dead_cells) == 0:
                    continue
                take = dead_cells[:remaining]
                cohort.senesced[i, take] = False
                cohort.theta[i, take] = tgt_v
                cohort.V[i, take] = tgt_v
                restored += len(take)
                remaining -= len(take)

        self.decode_failures += failures
        self.restored_cells += restored
        return {
            "cycle": self.cycles,
            "verified_reads": verified,
            "refused_reads": failures,
            "cells_restored": restored,
            "parity_budget": self.codec.nsym,
        }
