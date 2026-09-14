"""D3 — the write semantics of cell death (the tower's last open joint).

FALSIFICATION.md T4/D3: the latch layer composed onto the aging stack at
x0.800 — 'anchor-pinning fights the codec's writes on senesced cells'.
This module resolves the joint the way the biology says it should be
resolved: by making the death event itself a first-class WRITE with
competing, testable semantics.

THE BIOLOGY (research sweep 2026-09; full citations in docs/RESEARCH_MAP.md
section 7):

  1. Injury/death is an INSTANT tissue-scale depolarization (Zhao 2022:
     wound fields arise instantaneously and persist until the barrier
     recovers; 2025 injury-induced electrochemical coupling: organ injury
     -> immediate tissue depolarization gradient -> calcium wave).
  2. The depolarization is WRITTEN into neighbors through gap junctions —
     the bystander effect: senescent cells induce DNA-damage/senescence
     markers in junction-coupled neighbors (Nelson et al. 2012; Decrock
     2009 'to live or let die'; Cusato 2003 retinal bystander killing;
     Spray 2012 'Good Samaritans and dark side'); SASP paracrine
     spreading is cell-type-specific and directional (2026).
  3. The broadcast CORRUPTS; it does not transcribe: what propagates is
     the death signal (depolarization + SASP), not the dying cell's
     pattern. Senescence is contagious.
  4. The PATTERN survives death DISTRIBUTEDLY, not by transcription:
     the collective bioelectric state + bistable somatic memories
     (Pezzulo & Levin 2021: bioelectric pattern memories persist in
     planarian tissue > 1 week) + the genomic archive (the per-cell
     positional identity regenerate() re-derives from). Death is a
     transition for the pattern exactly because the pattern is stored
     redundantly in carriers the death of one cell cannot erase.
  5. The coupling is bidirectional: bioelectric state controls the death
     program (Beane et al. 2013: H+,K+-ATPase regulates apoptosis-driven
     remodeling in planarian regeneration).
  6. The junction channel itself ages (connexin/innexin decline is an
     integral indicator of aging across tissues; planarian innexins are
     load-bearing for regeneration — Oviedo 2009, Peiris 2013, Nogi 2007).

COMPETING WRITE SEMANTICS at the moment a cell senesces
(the discriminating experiment is experiments/exp16_d3_semantics.py):

  S0 "stasis"        Nothing is written. The cell's own memory freezes
                     wherever it was; V pins depolarized; theta creeps.
                     (The v1 default, minus the anchor corruption.)
  S1 "erasure"       The death event destroys the local memory outright:
                     theta AND the anchor snap to the senescent value.
                     Death is erasure.
  S2 "transcription" The dying cell's pre-death memory is WRITTEN INTO
                     the junction-connected neighbors' anchors — 'death
                     is a transcription event; the pattern moves'. The
                     star's naive form. Prediction: the novel-pattern
                     ledger decays slowest and the pattern MIGRATES
                     spatially on death.
  S3 "broadcast"     The dying cell drives a sustained depolarization
                     into its junction-connected neighbors (amplitude ~
                     conductance, decay tau_b) — the bystander effect.
                     Senescence spreads through the STATE, not just the
                     hazard. Own anchor freezes (recoverable stasis).
                     Prediction: dose-dependent spatial clustering and
                     g-dependent spread — separable from the statistical
                     contagion of h_inflam.

THE LATCH v2 — consensus anchoring (the composition fix):

  v1's anchor tracked the cell's OWN theta: any private drift beyond the
  deadzone re-programmed the memory, so at the boundary of a codec-repaired
  region the anchor learned the corrupted neighborhood and the write was
  outvoted. v2 tracks the LOCAL CONSENSUS (junction-masked mean of theta
  over self + non-senesced neighbors):

    - private deviations (single-cell noise, one neighbor's death
      broadcast) do not move the anchor; the pin restores theta —
      the pattern SURVIVES its neighbors' deaths;
    - collective shifts (regional jumps, whole-cluster codec writes,
      sustained region-wide depolarization) move the consensus; the
      anchor follows — novel morphologies latch, and a collectively
      sustained depolarized state latches as a stable attractor (cancer
      as a COLLECTIVE memory, not a single-cell one);
    - senesced cells' anchors FREEZE (recoverable stasis — the codec
      can restore the pattern the cell died holding);
    - the pin is junction-gated as in v1: with junctions alive the latch
      is transparent (propagation carries the pattern); as junctions die
      the memory channel takes over — graceful-degradation REDUNDANCY
      instead of antagonist. This is the dissolution of the D3 conflict.
"""
from __future__ import annotations

import numpy as np

from .aging import AgingParams
from .fidelity import FidelityAgingCohort, LatchingAgingCohort, quantize

V_SEN = -25.0          # the senescent pinned value (aging.py's convention)

DEATH_SEMANTICS = ("stasis", "erasure", "transcription", "broadcast")
LATCH_MODES = ("none", "v1", "v2")


class SemanticsCohort(LatchingAgingCohort):
    """FidelityAgingCohort + selectable death write-semantics + latch v2.

    Parameters
    ----------
    death_semantics : one of DEATH_SEMANTICS (default "stasis").
    latch : "v1" — LatchingAgingCohort's original anchor semantics;
            "v2" — consensus anchoring (the D3 fix);
            "none" — no anchor layer at all (plain Fidelity physics;
              only "broadcast" does anything at death events).
    broadcast_gain : mV-scale strength of the death depolarization drive
      per unit junction conductance (calibrated so one event transiently
      depolarizes each junction neighbor by ~gain*2 mV before healing).
    broadcast_tau : decay time of the death broadcast (yr; the wound
      field persists until the local state recovers).
    transcript_w : weight of the anchor write into neighbors at a
      transcription death event.
    """

    def __init__(self, *a, death_semantics: str = "stasis",
                 latch: str = "v2", broadcast_gain: float = 3.0,
                 broadcast_tau: float = 0.06, transcript_w: float = 1.0,
                 k_anchor: float | None = None, **kw):
        if death_semantics not in DEATH_SEMANTICS:
            raise ValueError(f"death_semantics must be one of {DEATH_SEMANTICS}")
        if latch not in LATCH_MODES:
            raise ValueError(f"latch must be one of {LATCH_MODES}")
        self._sem_ready = False
        self.death_semantics = death_semantics
        self.latch_mode = latch
        self.broadcast_gain = broadcast_gain
        self.broadcast_tau = broadcast_tau
        self.transcript_w = transcript_w
        # FULL-COPY transcription (the exp16 iteration-1 finding: a 0.6-blend
        # write lands BETWEEN discrete levels and accidentally ERASES the
        # pattern it was supposed to move — transcription must copy the
        # whole memory state or it is just a slower erasure)
        # v1 defaults live in LatchingAgingCohort; for v2 the deadzone keeps
        # the same calibration (junction-gated) but the PIN is matched-channel
        # (see below).
        self._bcast = None
        self._latch_ready = False
        if k_anchor is not None:
            kw["k_anchor"] = k_anchor      # explicit override flows to v1 base
        super().__init__(*a, **kw)
        # MATCHED-CHANNEL MEMORY (the exp16 iteration-1 finding): v1's
        # k_anchor=50/yr pin is ~100x the bandwidth of the junction channel
        # it backs up (~g0*deg ~ 0.4/yr) — a dominant 'backup' that fights
        # the primary channel, decouples theta from V, and chronically
        # inflates the |V-theta| senescence hazard. The v2 default matches
        # the memory's pull to the order of the channel it replaces: a
        # redundancy, not a replacement. (alpha_latch stays 20/yr — memory
        # FORMATION is fast; the PULL is matched.)
        if k_anchor is None and self.latch_mode == "v2":
            self.k_anchor = 0.25   # calibrated: composition x1.000 (exp16 C2)
        self._bcast = np.zeros((self.K, self.n))
        self._sem_ready = True
        # ledger bookkeeping (information carried by memory vs state)
        self.death_events = 0
        self.hist_ledger: list[dict] = []

    # ------------------------------------------------------------- dynamics
    def _integrate(self, dt: float, g: np.ndarray, sigma: np.ndarray) -> None:
        if self.latch_mode == "v1":
            # exactly the original layer (the comparison arm)
            LatchingAgingCohort._integrate(self, dt, g, sigma)
            self._broadcast_drive(dt, g)
            return
        # latch "none" or "v2": plain Fidelity physics first
        FidelityAgingCohort._integrate(self, dt, g, sigma)
        if not self._sem_ready:
            return
        self._broadcast_drive(dt, g)
        if self.latch_mode != "v2" or not self._latch_ready:
            return
        # ---- latch v2: CONSENSUS anchoring -------------------------------
        # consensus = junction-masked mean of theta over self + non-senesced
        # neighbors (the collective positional judgment). With junctions
        # alive dz_eff ~ 0 and k_eff ~ 0: the anchor tracks the consensus
        # (transparent) and propagation carries the pattern. As junctions
        # die: within-dz consensus moves are absorbed (memory holds) and
        # the pin restores private deviations toward the latched pattern
        # (the memory channel replaces the junction channel).
        avail = self.A[None, :, :] * (~self.senesced)[:, None, :].astype(float)
        deg = avail.sum(axis=2)                                    # (K, n)
        cons = (np.einsum("kij,kj->ki", avail, self.theta) + self.theta) \
            / (deg + 1.0)
        gap_frac = np.clip(g / self.p.g0, 0.0, 1.0)[:, None]
        dz_eff = self.deadzone * (1.0 - gap_frac)
        k_eff = self.k_anchor * (1.0 - gap_frac)
        healthy = ~self.senesced
        dev = cons - self.theta_anchor                            # collective
        far = (np.abs(dev) > dz_eff) & healthy
        decay_a = np.exp(-self.alpha_latch * dt)
        new_dev = np.where(far, dev * decay_a, dev)
        # frozen anchors for senesced cells: the anchor they died holding
        self.theta_anchor = np.where(
            healthy, cons - new_dev, self.theta_anchor)
        # pin: PRIVATE deviation from the (possibly updated) anchor shrinks
        decay_k = np.exp(-k_eff * dt)
        self.theta = np.where(
            healthy,
            self.theta_anchor + (self.theta - self.theta_anchor) * decay_k,
            self.theta)

    def _broadcast_drive(self, dt: float, g: np.ndarray) -> None:
        """S3: the death broadcast — a decaying depolarization drive into
        junction-connected neighbors (the bystander effect, made state-
        level rather than hazard-level)."""
        if self._bcast is None or not self._bcast.any():
            return
        nb = self._bcast @ self.A.T                                # (K, n)
        drive = self.broadcast_gain * g[:, None] * np.minimum(nb, 2.0) \
            * (V_SEN - self.V)
        # senesced cells are already pinned; only living tissue is driven
        self.V = np.where(self.senesced, self.V, self.V + dt * drive)
        self._bcast = self._bcast * np.exp(-dt / self.broadcast_tau)

    # ---------------------------------------------------------- death events
    def step(self, dt: float, g_override: np.ndarray | None = None,
             theta_pull: np.ndarray | None = None) -> None:
        super().step(dt, g_override, theta_pull)
        newly = getattr(self, "_newly_senesced", None)
        if newly is not None and newly.any():
            self._death_event(newly)

    def _death_event(self, newly: np.ndarray) -> None:
        """The write-on-death hook — where the four semantics differ."""
        self.death_events += int(newly.sum())
        if self.death_semantics == "erasure":
            # death destroys the local memory outright
            self.theta = np.where(newly, V_SEN, self.theta)
            if self._latch_ready and self.latch_mode != "none":
                self.theta_anchor = np.where(newly, V_SEN, self.theta_anchor)
        elif self.death_semantics == "transcription":
            # the dying cell's pre-death memory is written into the anchors
            # of its junction-connected surviving neighbors
            if self._latch_ready and self.latch_mode != "none":
                src = newly.astype(float) * self.theta_anchor      # (K, n)
                nb_cnt = newly.astype(float) @ self.A             # (K, n)
                nb_val = src @ self.A
                has = nb_cnt > 0
                nb_mean = nb_val / np.maximum(nb_cnt, 1.0)
                w = self.transcript_w
                self.theta_anchor = np.where(
                    has & ~self.senesced,
                    (1.0 - w) * self.theta_anchor + w * nb_mean,
                    self.theta_anchor)
                # the writer's own memory is consumed by the transcription
                # (moved, not copied — the pattern leaves the dying cell)
                self.theta_anchor = np.where(newly, V_SEN, self.theta_anchor)
        elif self.death_semantics == "broadcast":
            # the bystander effect: a decaying depolarization drive into
            # junction-connected neighbors (applied in _broadcast_drive)
            if self._bcast is not None:
                self._bcast = np.where(newly, 1.0, self._bcast)
        # "stasis": nothing is written — the anchor freezes wherever it was

    # ------------------------------------------------------------- ledger
    def pattern_ledger(self, ref: np.ndarray | None = None,
                       zone: np.ndarray | None = None) -> dict:
        """Where the pattern lives — the star question, quantified.

        I_V          : fraction of cells whose WORKING state (V) encodes
                       the reference pattern (quantized level match).
        I_anchor     : fraction whose SOMATIC MEMORY (anchor) encodes it.
        I_recoverable: either carrier holds it — the information survives
                       the deaths that occurred, because a repair channel
                       (codec writing from anchors, or the collective) can
                       re-derive the working state from either carrier.
                       For a NOVEL pattern (not in the genomic archive)
                       this is the whole story: lose both carriers and the
                       pattern is gone — erasure; hold either and death
                       was a transition, not an ending.

        zone restricts the metric to a cell subset (the novel-morphology
        zone); default: all cells.
        """
        if self.latch_mode == "none":
            raise RuntimeError("ledger requires an anchor layer (latch v1/v2)")
        r = self.theta0 if ref is None else np.asarray(ref, float)
        keep = np.ones(self.n, bool) if zone is None else np.asarray(zone, bool)
        okV = (quantize(self.V[:, keep], self.levels)
               == quantize(np.broadcast_to(r, (self.K, self.n))[:, keep],
                           self.levels))
        okA = (quantize(self.theta_anchor[:, keep], self.levels)
               == quantize(np.broadcast_to(r, (self.K, self.n))[:, keep],
                           self.levels))
        return {
            "I_V": float(okV.mean()),
            "I_anchor": float(okA.mean()),
            "I_recoverable": float((okV | okA).mean()),
            "n_cells": int(keep.sum()),
        }

    def pattern_centroid(self, level: int, zone: np.ndarray) -> float:
        """Mean distance of ALL anchor-carriers of the given novel level
        from the zone center — the spatial-migration signature of
        transcription-on-death (the pattern literally moves outward when
        death is a transcription event; it stays put otherwise)."""
        zone = np.asarray(zone, bool)
        pos = np.broadcast_to(np.arange(self.n)[None, :], (self.K, self.n))
        carry = (quantize(self.theta_anchor, self.levels) == level) \
            & self.alive[:, None]
        if not carry.any():
            return float("nan")
        zc = pos[:, zone].mean(axis=1, keepdims=True)
        d = np.abs(pos - zc)
        return float(d[carry].mean())
