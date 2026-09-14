"""Pattern-fidelity-dependent mortality — the Level-3 gate.

WHY THIS MODULE EXISTS (the documented negative result it fixes)
-----------------------------------------------------------------
exp6 showed codec maintenance ~= local maintenance and recorded the cause:
the mortality model was INSENSITIVE TO WRITTEN-VALUE CORRECTNESS — death
depended on senescence burden and tracking error (distance from the cell's
own drifting target), never on whether the pattern was RIGHT. Verification
against an archive cannot pay off in a model that never asks "correct?".

THE BIOLOGY THAT WAS MISSING
----------------------------
1. Vmem states are functionally DISCRETE. Cells occupy resting-potential
   bands whose IDENTITY — not proximity — gates downstream behavior
   (proliferation vs differentiation, neoblast activation, tumor-like
   growth). Morphology is decoded from discrete symbols, so mortality is a
   function of SYMBOL ERRORS, not Euclidean distance.

2. Bioelectric corruption is REGIONAL. Because cells are gap-junction
   coupled, reprogramming events flip whole DOMAINS together — this is how
   the two-headed planarian memory works and how tumor-like depolarized
   regions form. We model corruption as cluster "jumps". Correlated domain
   errors are exactly what averaging cannot fix — and exactly what an
   archive-referenced decoder uniquely can.

3. Organ function fails when pattern fidelity (fraction of cells in the
   correct discrete state) drops below critical — a wrong-state tissue that
   is perfectly healthy by local tracking metrics is doing the wrong JOB.

THE TWO BOTTLENECKS (the structural discovery this module enables)
-------------------------------------------------------------------
- The PATTERN (discrete code) can be repaired by verified writes — but only
  while the CHANNEL can still hold discrete states. Noise growth
  sigma(t)=sigma0*exp(kappa*t) eventually pushes the OU voltage spread past
  the level spacing: the Shannon capacity cliff. Pattern-only interventions
  plateau there.
- The CHANNEL (gap-junction coupling) can be restored (connexin
  upregulation) — but opening junctions in CORRUPTED tissue propagates the
  corruption (Chernet & Levin 2015: gap junctions spread tumor-like states).
  Channel repair is therefore DANGEROUS without prior verification: the
  codec's verify-then-write is what makes combined repair safe.

THE CODEC DISTINCTION THIS MAKES MEASURABLE
-------------------------------------------
- LOCAL maintenance (no archive): maintains whatever the local consensus
  says — it would faithfully maintain a two-headed worm.
- CODEC maintenance: consensus-read VERIFICATION (two independent reads
  must agree — helix-codec's consensus layer), THEN archive comparison to
  find wrong domains, refuse-unverified, write archived values.
- REGENERATION: full re-derivation from the archive (Dai et al. 2025:
  repeated amputation-regeneration cycles rejuvenate planarians). Resets
  the pattern; does NOT reset the channel engines — cycles must repeat.
- CHANNEL THERAPY: restore coupling toward youthful levels, optionally
  GATED on verification (safe) or ungated (propagates corruption).

The aging clock: per-individual pattern fidelity at a snapshot age
predicts remaining lifespan — the model's version of a readable bioelectric
biomarker (what voltage dyes measure in real tissue).
"""

from __future__ import annotations

import numpy as np

from .aging import AgingCohort, AgingParams
from ..coding.belief_prop import bp_smooth

V_MIN, V_MAX = -70.0, -10.0


# --------------------------------------------------------------------- symbols
def quantize(V, levels: int = 7, v_min: float = V_MIN, v_max: float = V_MAX):
    """Map voltages to discrete level indices (centers at v_min + k*span)."""
    span = (v_max - v_min) / (levels - 1)
    q = np.round((np.asarray(V, float) - v_min) / span)
    return np.clip(q, 0, levels - 1).astype(int)


def level_span(levels: int = 7, v_min: float = V_MIN, v_max: float = V_MAX) -> float:
    return (v_max - v_min) / (levels - 1)


def pattern_fidelity(V, theta0, levels: int = 7,
                     v_min: float = V_MIN, v_max: float = V_MAX) -> float:
    """Fraction of cells whose quantized state equals the archived target's."""
    ok = quantize(V, levels, v_min, v_max) == quantize(theta0, levels, v_min, v_max)
    return float(np.mean(ok))


# ------------------------------------------------------------------- cohort
class FidelityAgingCohort(AgingCohort):
    """AgingCohort + discrete-symbol corruption + fidelity-dependent mortality
    + a per-individual channel-boost state (connexin restoration therapy).

    Additional dynamics:
      - cluster jumps: each coupled domain flips to a uniformly-chosen WRONG
        level at rate jump_rate/cluster/yr (regional bioelectric
        reprogramming). Jumps set theta AND V (Vmem reprogramming is fast).
      - organ failure: contiguous quarters each have fidelity F_j(t); death
        hazard gains k_fail * mean_j(max(0, f_crit - F_j)).
      - channel_boost: per-individual multiplier on gap-junction conductance
        (capped at youthful g0). Boosting is the model of connexin-
        upregulation therapy; on corrupted tissue it propagates errors
        through the newly-opened junctions — the reason channel repair
        should be gated on verification.
    """

    def __init__(self, K: int = 300, params: AgingParams | None = None, seed: int = 0,
                 levels: int = 7, jump_rate: float = 0.005,
                 f_crit: float = 0.62, k_fail: float = 0.30,
                 snapshot_ages: tuple = (30.0, 40.0, 50.0, 60.0)):
        super().__init__(K=K, params=params, seed=seed)
        self.levels = levels
        self.span = level_span(levels)
        self.jump_rate = jump_rate
        self.f_crit = f_crit
        self.k_fail = k_fail
        self.snapshot_ages = list(snapshot_ages)
        self.n_clusters = 12
        self.cluster_len = self.n // self.n_clusters
        self.channel_boost = np.ones(K)

        # pattern-edge guard: cells at a discontinuity of the archived target
        # drift to intermediate levels via the theta-laplacian — their correct
        # state is genuinely AMBIGUOUS (real morphological boundaries are
        # graded zones), so they are excluded from the fidelity metric.
        d = np.abs(np.diff(self.theta0))
        edge = np.zeros(self.n, bool)
        edge[:-1] |= d > 0.5 * self.span
        edge[1:] |= d > 0.5 * self.span
        self._fid_keep = ~edge

        # healthy fidelity baseline (same warmup discipline as base_err)
        Vb, thb, senb = self.V.copy(), self.theta.copy(), self.senesced.copy()
        Fs = []
        for _ in range(24):
            self._integrate(0.25, np.full(K, self.p.g0), np.full(K, self.p.sigma0))
            Fs.append(self.global_fidelity())
        self.F0 = float(np.mean(Fs))
        self.V, self.theta, self.senesced = Vb, thb, senb

        self.snapshots: dict[float, np.ndarray] = {}
        self._snapped = set()
        self.hist_fid: list[float] = []

        self._organ_slices = [slice(j * self.org_len, (j + 1) * self.org_len)
                               for j in range(self.n_org)]

    # ---------------------------------------------------------------- metrics
    def _correct_mask(self) -> np.ndarray:
        """(K, n) bool: quantized V equals quantized archived target
        (pattern-edge cells excluded — see the guard note in __init__)."""
        ok = quantize(self.V, self.levels) == quantize(self.theta0[None, :], self.levels)
        ok[:, ~self._fid_keep] = True
        return ok

    def global_fidelity(self) -> np.ndarray:
        """(K,) per-individual fraction of cells in the correct discrete state."""
        ok = quantize(self.V, self.levels) == quantize(self.theta0[None, :], self.levels)
        return ok[:, self._fid_keep].mean(axis=1)

    def organ_fidelities(self) -> np.ndarray:
        """(K, n_org) per-organ pattern fidelity."""
        ok = self._correct_mask()
        return np.stack([ok[:, sl].mean(axis=1) for sl in self._organ_slices], axis=1)

    # ------------------------------------------------------------------ steps
    def _integrate(self, dt: float, g: np.ndarray, sigma: np.ndarray) -> None:
        """One Euler-Maruyama step; theta-diffusion is JUNCTION-SCALED.

        Real gap junctions share cytoplasm (ions, IP3, small molecules), so
        pattern propagation between cells scales with conductance. Two
        consequences:
          - as G decays with age, corrupted domains get QUARANTINED (frozen
            in place) — a hidden benefit of decoupling;
          - restoring coupling (connexin therapy) on corrupted tissue
            RE-OPENS propagation for the corruption — the reason channel
            repair must be gated on verification.
        """
        p = self.p
        avail = self.A[None, :, :] * (~self.senesced)[:, None, :].astype(float)
        deg = avail.sum(axis=2)
        coupling = g[:, None] * (np.einsum("kij,kj->ki", avail, self.V) - self.V * deg)
        dV = p.gamma * (self.theta - self.V) + coupling
        noise = sigma[:, None] * np.sqrt(dt) * self.rng.standard_normal((self.K, self.n))
        Vn = self.V + dt * dV + noise
        Vn[self.senesced] = -25.0

        lap = self.theta @ self.A.T - self.theta * self.degA
        gap_frac = np.clip(g / p.g0, 0.0, 1.0)[:, None]
        dtheta = p.eps * (self.V - self.theta) + p.mu_theta * gap_frac * lap
        drift = p.theta_drift * np.sqrt(dt) * self.rng.standard_normal((self.K, self.n))
        self.theta = self.theta + dt * dtheta + drift
        self.V = Vn

    def _apply_jumps(self, dt: float) -> None:
        """Regional reprogramming events: whole clusters flip to a wrong level."""
        if self.jump_rate <= 0.0:
            return
        K, C, cl = self.K, self.n_clusters, self.cluster_len
        draws = self.rng.random((K, C)) < self.jump_rate * dt
        if not draws.any():
            return
        rows, cols = np.nonzero(draws)
        for k, c in zip(rows, cols):
            if not self.alive[k]:
                continue
            cells = slice(c * cl, (c + 1) * cl)
            cur = int(quantize(self.theta[k, cells], self.levels)[0])
            wrong = self.rng.choice([l for l in range(self.levels) if l != cur])
            target = V_MIN + wrong * self.span + self.rng.normal(0.0, 1.0)
            self.theta[k, cells] = target
            self.V[k, cells] = target + self.rng.normal(0.0, 1.0, cl)

    def step(self, dt: float, g_override: np.ndarray | None = None,
             theta_pull: np.ndarray | None = None) -> None:
        if g_override is None and self.channel_boost is not None:
            g_nat = np.exp(-self.lam * self.t) * self.p.g0
            g_override = np.minimum(g_nat * self.channel_boost, self.p.g0)
        super().step(dt, g_override, theta_pull)
        self._apply_jumps(dt)

        # organ-failure hazard from pattern-fidelity deficit
        F = self.organ_fidelities()
        deficit = np.clip(self.f_crit - F, 0.0, None).sum(axis=1)
        death_hazard = self.k_fail * deficit / self.n_org
        dd = self.rng.random(self.K)
        died = self.alive & (dd < dt * death_hazard)
        if died.any():
            self.death_age[died] = self.t
            self.alive &= ~died

        for age in self.snapshot_ages:
            if age not in self._snapped and self.t >= age - 1e-9:
                self._snapped.add(age)
                self.snapshots[age] = self.global_fidelity()

    # ---------------------------------------------------------------- therapy
    def boost_channel(self, mask: np.ndarray, factor: float = 1.15,
                      cap: float = 6.0) -> None:
        """Connexin-restoration therapy: raise the gap-junction conductance
        multiplier for the masked individuals (effective conductance is still
        capped at youthful g0). UNGATED boosting on corrupted tissue
        propagates errors through the newly-opened junctions — the hazard
        that motivates verification-gated channel repair."""
        self.channel_boost = np.where(mask,
                                      np.minimum(self.channel_boost * factor, cap),
                                      self.channel_boost)

    def regenerate(self, jitter: float = 1.0, hazard: float = 0.01) -> None:
        """Full re-derivation of the pattern from the genomic archive.

        The planarian cycle: theta and V rebuilt from theta0, senesced cells
        replaced, jumps erased. The AGING ENGINES (lambda, kappa) are NOT
        reset — the rebuilt pattern degrades faster each cycle, so cycles
        must be repeated (Dai et al. 2025). Channel boost persists.
        """
        alive = self.alive
        if not alive.any():
            return
        ka = int(alive.sum())
        self.theta[alive] = np.tile(self.theta0, (ka, 1)) \
            + self.rng.normal(0.0, jitter, (ka, self.n))
        self.V[alive] = self.theta[alive] + self.rng.normal(0.0, jitter, (ka, self.n))
        self.senesced[alive] = False
        dd = self.rng.random(self.K)
        died = self.alive & (dd < hazard)
        self.death_age[died] = self.t
        self.alive &= ~died

    # ------------------------------------------------------------------- run
    def run(self, years: float = 130.0, dt: float = 0.25,
            intervention=None, record: bool = True) -> dict:
        steps = int(round(years / dt))
        for _ in range(steps):
            if self.alive.sum() == 0:
                break
            self.step(dt)
            if intervention is not None:
                intervention(self.t, self)
            if record:
                self.hist_t.append(self.t)
                self.hist_alive.append(float(self.alive.mean()))
                err = np.abs(self.V - self.theta)[self.alive]
                self.hist_error.append(float(err.mean()) if err.size else np.nan)
                sen_frac = self.senesced[self.alive].mean() if self.alive.any() else np.nan
                self.hist_sen.append(float(sen_frac))
                fid = self.global_fidelity()[self.alive]
                self.hist_fid.append(float(fid.mean()) if fid.size else np.nan)
        s = self.summary()
        s["F0_healthy"] = self.F0
        s["hist_fid"] = self.hist_fid
        s["snapshots"] = {str(a): v.tolist() for a, v in self.snapshots.items()}
        return s


# ---------------------------------------------------------------- maintenance
class FidelityCodec:
    """Consensus-verified, archive-referenced maintenance of the pattern code.

    Verification architecture (fixed per helix-codec's separation of
    consensus from correction — the exp6 gate conflated them):

      1. READ twice through the aging channel (independent noise/dropout).
      2. VERIFY the READ: the two reads must agree on commonly-readable
         clusters (measurement reliability). A jumped domain reads
         CONSISTENTLY wrong — it passes verification and is then DETECTED
         by archive comparison. Genuine channel garbage fails consistency
         and the write is REFUSED. (exp6's gate used agreement-with-archive
         as the trust measure — backwards: it refused to repair exactly
         when repair was most needed.)
      3. DETECT wrong domains: the consensus read (mean of the two
         verified reads; single-read fill for asymmetric dropouts) vs the
         genomic archive at cluster granularity. NOT the BP-smoothed read —
         smoothing smears genuine sharp jumps into adjacent clusters and
         false-positives them (a bug the batched rewrite exposed: adjacent
         clusters got flagged wrong and the write budget was wasted on
         healthy boundary-spanning domains).
      4. WRITE archived values into senesced or verified-wrong domains,
         budget-limited, PER-CELL (the genomic archive specifies per-cell
         positional identity — same source regenerate() re-derives from;
         writing cluster MEANS would destroy pattern boundaries).

    local mode: no archive, no verification. Repairs senesced cells in the
    worst clusters with the noisy BP consensus value — a jumped domain IS
    the consensus, invisible from inside; channel noise flows into writes.
    """

    def __init__(self, n_clusters: int = 12, n_cells: int = 60,
                 budget_per_cycle: int = 6, levels: int = 7,
                 consistency_threshold: float = 0.70):
        self.C = n_clusters
        self.n = n_cells
        self.budget = budget_per_cycle
        self.levels = levels
        self.span = level_span(levels)
        self.threshold = consistency_threshold
        self.cluster_len = n_cells // n_clusters
        A = np.zeros((n_clusters, n_clusters))
        for i in range(n_clusters - 1):
            A[i, i + 1] = A[i + 1, i] = 1.0
        self.A_cluster = A
        self.cycles = 0
        self.verified = 0
        self.refused = 0
        self.restored = 0

    def _cluster_means(self, x: np.ndarray) -> np.ndarray:
        return x.reshape(self.C, self.cluster_len).mean(axis=1)

    def maintain(self, cohort: FidelityAgingCohort, preset: dict,
                 mode: str = "codec") -> dict:
        """One maintenance cycle, VECTORIZED across all individuals.

        (Rewritten batch-mode: identical semantics to the original
        per-individual loop — per-cluster actuation noise, budget in cells,
        refusal per individual — but evaluated as (K, C) array operations.
        RNG draw order differs from the loop version, so exact trajectories
        differ; distributions do not.)
        """
        self.cycles += 1
        rng = cohort.rng
        K, C, cl = cohort.K, self.C, self.cluster_len
        alive = cohort.alive

        theta = cohort.theta                      # (K, n)
        sen = cohort.senesced                     # (K, n)
        cluster_of = np.arange(cohort.n) // cl    # (n,) cluster index of cell

        # ---- READ twice through the aging channel (K, C)
        cm = theta.reshape(K, C, cl).mean(axis=2)  # (K, C) cluster means
        dead = sen.reshape(K, C, cl).mean(axis=2) > 0.5
        obs_a = cm + rng.normal(0.0, preset["meas_noise_mV"], (K, C))
        obs_b = cm + rng.normal(0.0, preset["meas_noise_mV"], (K, C))
        read_a = ~dead & (rng.random((K, C)) > preset["dropout"])
        read_b = ~dead & (rng.random((K, C)) > preset["dropout"])
        both = read_a & read_b
        obs = np.where(read_a, obs_a, np.where(read_b, obs_b, 0.0))
        readable = read_a | read_b
        # actuation noise: writing (targeted drug/opto) is more precise
        # than reading (dye imaging) — 0.5x the read noise
        act_mV = 0.5 * preset["meas_noise_mV"]

        # per-cluster noise draw (one actuation value per written cluster,
        # shared by the cells of that cluster — as in the loop version)
        act_noise = rng.normal(0.0, act_mV, (K, C))

        if mode == "codec":
            # ---- VERIFY the read (consensus of two independent reads)
            tol = 2.0 * preset["meas_noise_mV"] + 1.0
            consistent = np.abs(obs_a - obs_b) <= tol
            n_both = both.sum(axis=1)
            cons_frac = np.where(n_both > 0,
                                 consistent.sum(axis=1) / np.maximum(n_both, 1),
                                 0.0)
            # ---- WRITE-PRECISION GATE: refuse when actuation cannot
            # reliably place symbols (the F3/F5 lessons — no silent
            # writes, no reckless ones either).
            fail = (cons_frac < self.threshold) | (act_mV > 0.35 * self.span)
            refused_mask = alive & fail     # only alive individuals counted
            verified_mask = alive & ~fail
            # ---- DETECT wrong domains: consensus read vs the genomic
            # archive (regional). The consensus read = mean of the two
            # verified reads where both are readable, single-read fill
            # otherwise; unreadable clusters cannot be flagged.
            archive = self._cluster_means(cohort.theta0)             # (C,)
            read_cons = np.where(both, 0.5 * (obs_a + obs_b),
                                 np.where(read_a, obs_a,
                                          np.where(read_b, obs_b, archive[None, :])))
            wrong = readable & (np.abs(read_cons - archive[None, :]) > 0.5 * self.span)
            writable = dead | wrong                                  # (K, C)
            W = writable[:, cluster_of]                              # (K, n)
            # per-cell archive write values (boundaries preserved)
            write_cells = np.broadcast_to(cohort.theta0[None, :], (K, cohort.n))
        else:
            refused_mask = np.zeros(K, bool)   # local mode: no verification, no refusal
            verified_mask = np.zeros(K, bool)
            denoised = bp_smooth(
                obs, self.A_cluster, readable,
                noise_var=preset["meas_noise_mV"] ** 2, iters=20)  # (K, C)
            writable = dead                                          # (K, C)
            W = writable[:, cluster_of] & sen                        # (K, n)
            # local: only the consensus value per cluster is available
            write_cells = denoised[:, cluster_of]                      # (K, n)

        # ---- budget allocation: cells in priority order (writable clusters
        # in cluster order, cells within cluster), first `budget` cells
        # (deterministic stable order — the loop version's argsort was
        # quicksort-unstable at ties)
        W = W & verified_mask[:, None] if mode == "codec" else W & alive[:, None]
        ranks = np.cumsum(W, axis=1)                                  # 1-based rank
        write_mask = W & (ranks <= self.budget)                      # (K, n)

        # ---- WRITE: per-cluster actuation value + per-cell archive target
        vals = write_cells + act_noise[:, cluster_of]                 # (K, n)
        do = write_mask
        if do.any():
            cohort.theta = np.where(do, vals, cohort.theta)
            cohort.V = np.where(do, vals, cohort.V)
            cohort.senesced = np.where(do, False, cohort.senesced)

        restored_per_i = do.sum(axis=1)
        restored = int(restored_per_i.sum())
        refused = int(refused_mask.sum())
        verified = int(verified_mask.sum())

        self.verified += verified
        self.refused += refused
        self.restored += restored
        return {"cycle": self.cycles, "verified": verified, "refused": refused,
                "restored": restored, "verified_mask": verified_mask.tolist(),
                "restored_per_i": restored_per_i.tolist()}
