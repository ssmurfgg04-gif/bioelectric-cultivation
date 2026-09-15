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
        # exp23 hook: optional PER-CLUSTER susceptibility multiplier (zone
        # heterogeneity — a stable vs a volatile region). Scalar when the
        # attribute is absent -> bit-exact with the original draw.
        mult = getattr(self, "jump_mult", None)
        rate = (self.jump_rate if mult is None
                else self.jump_rate * np.asarray(mult, float))
        draws = self.rng.random((K, C)) < rate * dt
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
                 consistency_threshold: float = 0.70,
                 per_cell_archive: bool = True,
                 target_source: str = "archive"):
        self.C = n_clusters
        self.n = n_cells
        self.budget = budget_per_cycle
        self.levels = levels
        self.span = level_span(levels)
        self.threshold = consistency_threshold
        # ABLATION SWITCH (exp13 C2): False -> write CLUSTER MEANS instead
        # of per-cell archive values (destroys boundary-preserving write
        # precision — the hypothesized source of the cliff safety margin).
        self.per_cell_archive = per_cell_archive
        # D3b (exp17): "archive" — the genomic archive is the reference and
        # write source (the tower's verified semantics); "anchored" — the
        # SOMATIC MEMORY (theta_anchor) is the reference and write source
        # wherever the cluster's memory is internally coherent, with the
        # genomic archive as fallback for incoherent memories. This is the
        # biological target-morphology semantics: the remembered pattern IS
        # the target unless the memory itself is corrupted. Without it,
        # verified maintenance actively ERASES novel morphologies (they
        # read 'wrong' against the archive and get repaired to factory
        # default) — the off-target hazard exp17 measures.
        if target_source not in ("archive", "anchored"):
            raise ValueError("target_source must be 'archive' or 'anchored'")
        self.target_source = target_source
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
                 mode: str = "codec", alloc: dict | None = None) -> dict:
        """One maintenance cycle, VECTORIZED across all individuals.

        (Rewritten batch-mode: identical semantics to the original
        per-individual loop — per-cluster actuation noise, budget in cells,
        refusal per individual — but evaluated as (K, C) array operations.
        RNG draw order differs from the loop version, so exact trajectories
        differ; distributions do not.)

        alloc (exp23, optional): multi-pattern budget allocation. When
        given, the budget's priority order over writable cells follows the
        POLICY instead of plain cell order — see _alloc_ranks. None (the
        default, all prior experiments) is bit-exact unchanged.
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
            # ---- DETECT wrong domains: consensus read vs the reference
            # (regional). The consensus read = mean of the two verified
            # reads where both are readable, single-read fill otherwise;
            # unreadable clusters cannot be flagged.
            archive = self._cluster_means(cohort.theta0)             # (C,)
            anchored = (self.target_source == "anchored"
                        and hasattr(cohort, "theta_anchor"))
            if anchored:
                # D3b: the reference is the somatic memory wherever the
                # cluster's memory is internally coherent (spread <= half
                # a level); incoherent memories fall back to the archive.
                anc = cohort.theta_anchor                       # (K, n)
                anchor_cm = anc.reshape(K, C, cl).mean(axis=2)  # (K, C)
                anchor_sd = anc.reshape(K, C, cl).std(axis=2)   # (K, C)
                mem_ok = anchor_sd <= 0.5 * self.span           # (K, C)
                ref = np.where(mem_ok, anchor_cm, archive[None, :])
            else:
                ref = np.broadcast_to(archive, (K, C))
            read_cons = np.where(both, 0.5 * (obs_a + obs_b),
                                 np.where(read_a, obs_a,
                                          np.where(read_b, obs_b, ref)))
            wrong = readable & (np.abs(read_cons - ref) > 0.5 * self.span)
            writable = dead | wrong                                  # (K, C)
            W = writable[:, cluster_of]                              # (K, n)
            # per-cell write values (boundaries preserved); ablated mode:
            # cluster-mean values (boundaries smeared); anchored mode:
            # per-cell MEMORY values in coherent clusters, archive elsewhere
            if anchored:
                write_cells = np.where(
                    mem_ok[:, cluster_of],
                    np.broadcast_to(anc, (K, cohort.n)),
                    np.broadcast_to(cohort.theta0[None, :], (K, cohort.n)))
            elif self.per_cell_archive:
                write_cells = np.broadcast_to(cohort.theta0[None, :], (K, cohort.n))
            else:
                write_cells = np.broadcast_to(
                    archive[None, :][:, cluster_of], (K, cohort.n))
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
        if alloc is None:
            ranks = np.cumsum(W, axis=1)                              # 1-based rank
        else:
            ranks = self._alloc_ranks(W, alloc)                       # exp23
        write_mask = W & (ranks <= self.budget)                      # (K, n)

        # ---- WRITE: per-cluster actuation value + per-cell archive target
        vals = write_cells + act_noise[:, cluster_of]                 # (K, n)
        do = write_mask
        if do.any():
            cohort.theta = np.where(do, vals, cohort.theta)
            cohort.V = np.where(do, vals, cohort.V)
            cohort.senesced = np.where(do, False, cohort.senesced)
            # latch-integration hook (LatchingAgingCohort): a write is a
            # reprogramming event — the somatic anchor latches to it
            if hasattr(cohort, "on_write"):
                cohort.on_write(do)

        restored_per_i = do.sum(axis=1)
        restored = int(restored_per_i.sum())
        refused = int(refused_mask.sum())
        verified = int(verified_mask.sum())

        self.verified += verified
        self.refused += refused
        self.restored += restored
        out = {"cycle": self.cycles, "verified": verified, "refused": refused,
               "restored": restored, "verified_mask": verified_mask.tolist(),
               "restored_per_i": restored_per_i.tolist()}
        if alloc is not None:
            # exp23: where the budget went (allocation bookkeeping)
            g = np.asarray(alloc["groups"], int)
            out["restored_by_group"] = [
                int(do[:, g == gid].sum()) for gid in range(int(g.max()) + 1)]
        return out

    def _alloc_ranks(self, W: np.ndarray, alloc: dict) -> np.ndarray:
        """exp23 — policy-driven budget priority over writable cells.

        alloc = {"groups": (n,) int group id per cell (the competing
        patterns; e.g. 0=background, 1..3 = novel zones),
        "policy": one of:

          "balanced"  round-robin interleave — equal shares per group;
          "fixed"     static priority, "order" = group ids best-first
                      (all of group 1's writable cells outrank group 2's);
          "severity"  weighted round-robin: per-individual budget shares
                      track each group's DETECTED demand (writable count) —
                      shares proportional to need, per cycle;
          "critical"  if any group's detected-need FRACTION exceeds
                      "critical_frac" (default 0.5), ALL budget goes to the
                      worst such group this cycle; otherwise balanced.

        Returns (K, n) 1-based priority rank among writable cells
        (rank 1 = written first), ties broken deterministically by cell
        index. The alloc=None path (cell order) is untouched and
        bit-exact with every prior experiment.
        """
        K, n = W.shape
        g = np.asarray(alloc["groups"], int)
        G = int(g.max()) + 1
        policy = alloc.get("policy", "balanced")
        if policy not in ("balanced", "fixed", "severity", "critical"):
            raise ValueError(f"unknown alloc policy: {policy}")
        # in-group position of each cell (by cell index) + group sizes
        ingrp = np.zeros(n, int)
        gsize = np.zeros(G, int)
        for gid in range(G):
            m = g == gid
            ingrp[m] = np.arange(int(m.sum()))
            gsize[gid] = int(m.sum())
        # per-individual detected demand (writable cells) per group (K, G)
        demand = np.stack([W[:, g == gid].sum(axis=1)
                           for gid in range(G)], axis=1)
        if policy == "fixed":
            order = list(alloc.get("order", range(G)))
            orank = np.empty(G)
            for i, gid in enumerate(order):
                orank[gid] = i
            prio = np.broadcast_to(
                orank[g][None, :] * n + ingrp[None, :], (K, n)).astype(float)
        elif policy == "severity":
            # weighted round-robin: a group with demand d gets shares ~ d
            # (step = total/demand -> smaller step = tighter spacing =
            # more of that group's cells fall under any budget cutoff)
            tot = demand.sum(axis=1, keepdims=True)                # (K, 1)
            # finite stand-in for inf (inf*0 = nan would break ranks);
            # 1e9 is unreachable by any real step (= tot/demand <= n)
            step = np.where(demand > 0,
                            tot / np.maximum(demand, 1e-9), 1e9)
            prio = (step[:, g] * ingrp[None, :]
                    + g[None, :] * 1e-6
                    + np.arange(n)[None, :] * 1e-9)               # (K, n)
        elif policy == "critical":
            frac = demand / np.maximum(gsize[None, :], 1)          # (K, G)
            worst = frac.argmax(axis=1)                            # (K,)
            crit = frac.max(axis=1) >= alloc.get("critical_frac", 0.5)
            BIG = float(G * n + 1)
            bal = (ingrp[None, :] * G + g[None, :]).astype(float)
            fix = ((g[None, :] != worst[:, None]).astype(float) * BIG
                   + g[None, :] * n + ingrp[None, :])
            prio = np.where(crit[:, None], fix, bal)
        else:  # balanced — round-robin interleave across groups
            prio = (ingrp[None, :] * G + g[None, :]).astype(float)
        # rank of cell j = 1 + #writable cells with strictly higher
        # priority (vectorized pairwise; n=60 -> (K, n, n) is small)
        lt = prio[:, None, :] < prio[:, :, None]   # [k, j, i]: i outranks j
        ranks = 1 + (W[:, None, :] & lt).sum(axis=2)
        return ranks.astype(np.int64)


# ------------------------------------------------------------- latch layer
class LatchingAgingCohort(FidelityAgingCohort):
    """FidelityAgingCohort + exp11's cell-autonomous latching memory.

    The Phase-D integration layer: every theta now carries an ANCHOR (the
    somatic pattern memory). TIME-SCALE NOTE (the first integration
    attempt's bug, recorded): exp11's latch rates were calibrated in
    simulation TIME UNITS (protocols ran 24-150 units); this cohort's t is
    in YEARS. With unit-scale rates the writes latched over ~24 yr and the
    k_anchor pull half-healed exp8's permanent jumps (semantics violated
    at both seams). The defaults here are YEAR-calibrated to the real
    biophysics: latch dynamics run at DAYS (alpha ~ 20/yr, pinning
    ~ 50/yr), so:

      - cluster jumps (full-band, 8.57 mV > deadzone 5) latch in within
        weeks: exp8's 'regional reprogramming is permanent' semantics
        PRESERVED;
      - codec writes latch in within weeks (plus the explicit on_write
        sync hook — exp11's 'written patterns persist' semantics);
      - sub-deadzone slow erosion (theta drift + Laplacian) is ABSORBED:
        the layer's gift (exp11's stability semantics);
      - senesced cells (V pinned at -25) corrupt their own anchors over
        weeks — biologically honest (a stably-depolarized cell IS
        reprogrammed; that is why cancers persist) — and the codec's
        write-hook re-latches the anchor when it repairs them;
      - regenerate() re-derives theta AND the anchor from the genomic
        archive (the re-derivation resets the memory too).
    """

    def __init__(self, *a, alpha_latch: float = 20.0,
                 deadzone: float = 5.0, k_anchor: float = 50.0, **kw):
        # the parent constructor runs warmup _integrate calls BEFORE the
        # anchor exists — gate the latch layer until initialization ends
        self._latch_ready = False
        self.alpha_latch = alpha_latch
        self.deadzone = deadzone
        self.k_anchor = k_anchor
        super().__init__(*a, **kw)
        self.theta_anchor = np.tile(self.theta0, (self.K, 1))
        self._latch_ready = True

    def _integrate(self, dt: float, g: np.ndarray, sigma: np.ndarray) -> None:
        super()._integrate(dt, g, sigma)
        if not self._latch_ready:
            return
        # EXACT-EXPONENTIAL updates (unconditionally stable at any rate —
        # the explicit-Euler version diverged at k_anchor*dt ~ 12.5, which
        # is exactly what the second integration attempt hit).
        #
        # JUNCTION-GATED LATCH (the third-attempt design, pre-registered):
        # the ablations showed the naive latch's deadzone absorption
        # suppresses the theta-Laplacian — the gap-junction-mediated
        # PATTERN PROPAGATION exp8's maintenance relied on for post-write
        # healing (deadzone=0 restored exp8 exactly; full deadzone cost
        # 15 yr). The principled composition: the latch engages AS THE
        # SHARING NETWORK DIES. Healthy junctions (gap_frac -> 1): the
        # anchor tracks theta continuously (deadzone -> 0, pin -> 0 — the
        # latch is TRANSPARENT; pure exp8 propagation semantics). Decayed
        # junctions (gap_frac -> 0, exp8's quarantine regime): the
        # deadzone and pin engage — the somatic memory freezes the
        # pattern exactly when propagation can no longer hold it. The two
        # memory mechanisms become graceful-degradation redundancies
        # instead of antagonists.
        dev = self.theta - self.theta_anchor
        gap_frac = np.clip(g / self.p.g0, 0.0, 1.0)[:, None]
        dz_eff = self.deadzone * (1.0 - gap_frac)
        k_eff = self.k_anchor * (1.0 - gap_frac)
        # anchor follows beyond-effective-deadzone deviation
        far = np.abs(dev) > dz_eff
        decay_a = np.exp(-self.alpha_latch * dt)
        new_dev = np.where(far, dev * decay_a, dev)
        self.theta_anchor = self.theta - new_dev
        # theta pinned toward the anchor (only where junctions have decayed)
        decay_k = np.exp(-k_eff * dt)
        self.theta = self.theta_anchor + dev * decay_k

    def on_write(self, do: np.ndarray) -> None:
        """Codec-write hook: a maintenance write is a reprogramming event —
        the anchor latches to the written value (exp11 semantics; the
        biophysics of a sustained forced Vmem rewrite)."""
        if do.any():
            self.theta_anchor = np.where(do, self.theta, self.theta_anchor)

    def regenerate(self, jitter: float = 1.0, hazard: float = 0.01) -> None:
        was_alive = self.alive.copy()
        super().regenerate(jitter, hazard)
        ka = int(was_alive.sum())
        if ka:
            self.theta_anchor[was_alive] = np.tile(self.theta0, (ka, 1))
