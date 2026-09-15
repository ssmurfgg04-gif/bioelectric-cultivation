"""Gap-junction-coupled bioelectric cell collective with homeostatic target memory.

Physics
-------
Each cell i maintains a membrane voltage V_i (mV, typically -70..-10 in
non-neural tissue). Cells are electrically coupled through gap junctions of
conductance G_ij (direct cytoplasmic continuity — the same electrical
synapse machinery neurons use). The dynamics:

    dV_i/dt     = gamma * (theta_i - V_i) + sum_j G_ij (V_j - V_i) + eta_i(t)

theta_i is the slow *homeostatic target*: the intrinsic resting state the
cell's channel expression re-converges toward (real cells do adjust their
resting potential over hours via ion-channel transcription — this is the
mechanism behind Levin-lab stable reprogramming results). Its dynamics:

    dtheta_i/dt = eps  * (V_i - theta_i)          # homeostatic plasticity
                + mu   * sum_j A_ij (theta_j - theta_i)   # pattern propagation
                + xi_i(t)                          # slow drift (aging)

Two regimes of one mechanism: a 24h forced depolarization rewrites theta
(reprogramming / the two-headed planarian memory), while unforced noise makes
theta random-walk (aging drift). The morphological target is an attractor of
this coupled system, exactly as in the Levin-group modeling literature
(Pietak & Levin 2017, Cervera et al. 2019, Grodstein & Levin 2021).
"""

from __future__ import annotations

import hashlib

import numpy as np

# physiological bounds (Nernst/reversal limits) — see step()
V_PHYS_MIN = -85.0
V_PHYS_MAX = 5.0

# M33 neural/muscle polarity channel: the fate-axis midpoint between the
# WT head identity (-20 mV) and the WT trunk/tail identity (-50 mV). Only
# ANTERIOR identities (spec >= this line) qualify for the non-junctional
# readout — the literature asymmetry: the anterior pole is a constitutive,
# junction-independent identity source (notum+ wound response, axon-aligned
# vector transport, Egal-1/microtubule muscle substrate), while posterior
# identity has no local pole and stays junction-carried (which is exactly
# why recorded GJ-blockade phenotypes concentrate at posterior planes).
NEURAL_SPEC_MIN = -35.0
# M35-A: the ARZ's multi-lineage convergence — K independent lineage
# reads averaged into the blastema guess (the three planarian lineages:
# epidermal, neural, muscle; K derived from the published lineage count,
# MED42172041, not fitted).
ARZ_LINEAGES = 3
ARZ_WIDTH = 2


def line_adjacency(n: int, k: int = 1, ring: bool = False) -> np.ndarray:
    """Binary adjacency of a 1D chain (k neighbors each side), optionally ring."""
    A = np.zeros((n, n))
    for d in range(1, k + 1):
        A += np.diag(np.ones(n - d), d) + np.diag(np.ones(n - d), -d)
    if ring and n > 2 * k:
        A[0, n - 1] = A[n - 1, 0] = 1.0
    return A


class BioElectricCollective:
    """A 1D bioelectric cell collective (anatomical axis). Vectorized in numpy."""

    def __init__(
        self,
        n: int = 100,
        gamma: float = 0.25,
        g_gap: float = 0.20,
        eps: float = 0.04,
        mu_theta: float = 0.015,
        noise_std: float = 0.30,
        theta_drift: float = 0.0,
        adjacency: np.ndarray | None = None,
        seed: int | None = 0,
        blastema_readout_noise: float = 18.0,
    ):
        self.n = n
        self.gamma = gamma  # intrinsic relaxation rate toward theta
        self.eps = eps  # homeostatic plasticity rate of theta
        self.mu = mu_theta  # theta diffusion (pattern propagation) rate
        self.noise_std = noise_std
        self.theta_drift = theta_drift
        # Spread (mV) of a blastema cell's identity guess when it cannot read
        # the pattern field through gap junctions (M25 coupling-dependent
        # readout; see regrow). Physiological range: a blind cell can land
        # anywhere on the head-trunk fate axis (~-20 to ~-50 mV).
        self.blastema_readout_noise = blastema_readout_noise

        self.rng = np.random.default_rng(seed)
        self.A = adjacency if adjacency is not None else line_adjacency(n)
        self.G = 0.0 + self.A * g_gap  # working conductance matrix
        self.G0 = self.G.copy()  # youthful reference
        self.gap_scale = 1.0  # global gap-junction health multiplier
        self.deg = (self.A * g_gap).sum(axis=1)

        self.theta = np.full(n, -50.0)
        self.V = self.theta + self.rng.normal(0.0, 2.0, n)

        # clamps: cell index -> voltage (interventions applied each step)
        self.clamps: dict[int, float] = {}
        # theta drivers: (region_indices, target_voltage, rate, voltage_gate)
        # A driver pulls theta toward target at `rate`, but ONLY where the
        # cell's voltage is above voltage_gate (depolarization-gated). This
        # is the oncogene model: tumoral growth signaling is permissive in
        # depolarized tissue (Chernet & Levin 2015) and is silenced by
        # hyperpolarization — which is why restoring Vmem can normalize
        # oncogene-expressing cells.
        self.theta_drivers: list[tuple[np.ndarray, float, float, float]] = []

    # ------------------------------------------------------------------ state
    def set_target(self, theta: np.ndarray) -> None:
        self.theta = np.asarray(theta, dtype=float).copy()
        # M28: the identity-at-coordinate SPEC is captured when the animal's
        # pattern is first set — a distributed collective property (D3: the
        # pattern survives cell death as a distributed property, not a cell
        # property). theta is the expression layer; phi_spec is what belongs
        # at each body coordinate. Only read when regrow(phi_readout > 0).
        if getattr(self, "phi_spec", None) is None:
            self.phi_spec = self.theta.copy()

    def set_state(self, V: np.ndarray) -> None:
        self.V = np.asarray(V, dtype=float).copy()

    def clone_state(self) -> tuple[np.ndarray, np.ndarray]:
        return self.V.copy(), self.theta.copy()

    def restore_state(self, state: tuple[np.ndarray, np.ndarray]) -> None:
        self.V, self.theta = state[0].copy(), state[1].copy()

    # ------------------------------------------------------------ interventions
    def clamp(self, region: slice | np.ndarray, voltage: float) -> None:
        """Hold a region's voltage (drug / electrode / optogenetic forcing)."""
        idx = np.arange(self.n)[region] if isinstance(region, slice) else np.asarray(region)
        for i in idx:
            self.clamps[int(i)] = voltage

    def release_clamps(self) -> None:
        self.clamps.clear()

    def block_gap_junctions(self, scale: float) -> None:
        """Scale all gap-junction conductances (heptanol/octanol-like blockade)."""
        self.gap_scale = float(scale)
        self.G = self.G0 * scale
        self.deg = self.G.sum(axis=1)

    def restore_gap_junctions(self, scale: float = 1.0) -> None:
        self.block_gap_junctions(scale)

    def scale_gap_junctions(self, factor: float) -> None:
        self.block_gap_junctions(self.gap_scale * factor)

    def amputate(self, region: slice, wound_voltage: float = -30.0,
                 blastema_theta: float = -40.0) -> None:
        """Remove structure: cells reset to wound state, pattern re-derives."""
        self.V[region] = wound_voltage
        self.theta[region] = blastema_theta

    def regrow(self, region: slice, cell_period: float = 0.8, dt: float = 0.1,
               noise: float = 0.6, direction: str = "forward",
               length_gradient: float = 0.0,
               commitment_noise_scale: float = 1.0,
               gradient_window: int = 5,
               gradient_clip: bool = False,
               commitment_diffusion: float = 0.0,
               phi_readout: float = 0.0,
               spec_expression_p: float = 1.0,
               spec_reanchor_p: float = 1.0,
               anchor_from_history: float | None = None,
               spec_reanchor_isolated: float = 1.0,
               neural_readout: float = 0.0,
               neural_misanchor: float = 0.0,
               arz_readout: float = 0.0,
               arz_width: int = 2,
               neoblast_depleted: float = 0.0) -> None:
        """Regeneration: the blastema EXTENDS THE STORED PATTERN outward from
        the wound boundary, one committing cell at a time (tissue-growth
        abstraction of neoblast-driven regrowth). Each new cell inherits the
        identity of the last committed cell — so what regrows is whatever the
        remaining tissue REMEMBERS. This is the mechanism that makes
        reprogramming memory empirically testable (Durant et al. 2017).

        `direction` names which wound face the chain extends from:
        "forward" (default, historical behavior — blastema grows tail-ward
        from the anterior boundary cell) or "backward" (head-ward from the
        posterior boundary cell — a head amputation's blastema reads the
        trunk boundary BEHIND it). At gap_scale == 1.0 and direction ==
        "forward" the mechanism is bit-exact with the pre-M25 chain.

        M26 ADDITIVE PARAMETERS (night three; each bit-exact at default):

        `length_gradient` g in [0,1] — INTRINSIC positional-information
        readout (M26a): a committing cell at distance d past the wound face
        blends chain inheritance with a linear EXTRAPOLATION of the stored
        theta trend measured over the intact tissue adjacent to the face
        (Wolpert-style positional cue; no external target knowledge). g=0
        keeps pure chain inheritance (bit-exact pre-M26 walk). Fixes the
        crosspiece length-gradient refutation (S2W2's cross_a overshoot:
        sim 1.00 vs recorded 0.52 — a pure chain cannot know how MUCH was
        removed; a gradient readout can).

        `commitment_noise_scale` — Vmem-gated blastema COMMITMENT (M26b):
        multiplies the per-cell identity noise. Ion-channel dysfunction
        (impaired homeostatic relaxation, noisy Vmem) degrades the
        commitment signal itself, not the stored pattern — recorded
        ion_channel experiments are as abnormal as junction loss (0.45 vs
        0.41) while the sim's stored pattern stays intact (0.00). The arm
        chooses the scale; default 1.0 is bit-exact.

        `direction="both"` (M26c) — TWO-FACE trunk regeneration: splits the
        region at the midpoint; the anterior half regenerates forward from
        the anterior face, the posterior half backward from the posterior
        face (two independent blastemas — mid-body removals in the record
        heal both faces, producing the two-headed / two-tailed phenotypes
        the one-face topology cannot reach).

        M27 ADDITIVE PARAMETERS (night three, second wave; each bit-exact
        at default):

        `gradient_window` — the positional-trend measurement span for the
        length-gradient readout: 5 (default) = the M26a five-cell window
        adjacent to the wound face; 0 = WHOLE-FRAGMENT secant (theta at
        the far end of the intact side vs theta at the face). exp32's
        refutation diagnosis: a head-only fragment's 5-cell face window
        sits on the head plateau (slope ~0) so the extrapolation is a
        no-op exactly where the recorded refutation lives; the secant
        over the WHOLE fragment carries the head->trunk depolarization
        trend instead.
        `gradient_clip` — saturate the extrapolated identity to the
        intact side's own identity repertoire [min(theta), max(theta)]
        (intrinsic fate-axis bounds: the fragment cannot commit a cell
        OUTSIDE the identity range it actually stores). No external
        target knowledge.
        `commitment_diffusion` — CHAIN-ACCUMULATING commitment error
        (M27 candidate #2): per-cell identity noise that random-walks
        ALONG the chain (wander += N(0, diffusion) each committed cell),
        so commitment error COMPOUNDS through sequential inheritance
        (sd ~ diffusion * sqrt(d)) instead of averaging out — the
        exp32 diagnosis of why i.i.d. commitment noise (M26b) left the
        ion arms at 0.00 while the record shows 0.45. Zero new RNG draws
        when 0.0.

        `phi_readout` (M28 DUAL-FIELD) — identity-at-coordinate spec
        readout: the committing cell at body coordinate i blends its chain
        inheritance with phi_spec[i], the identity that BELONGS at that
        coordinate (the distributed collective spec captured at pattern
        set — D3: the pattern survives fragmentation as a distributed
        property; theta is the expression layer, phi_spec the positional
        layer). The read is junction-carried: w = phi_readout *
        gap_scale, so junction blockade silences the spec read exactly
        like the chain read (M25). Deterministic — no new RNG draws;
        0.0 default is bit-exact.

        `spec_expression_p` (M30 STOCHASTIC SPEC EXPRESSION) — per-cell
        expression probability of the spec read: when 0 < p < 1 and the
        phi read is active, EACH committing cell draws u ~ U(0,1) and
        reads phi_spec only if u < p (cells that fail to re-express the
        positional spec fall back to pure chain inheritance for that
        cell). Rationale: exp36 found the deterministic spec read gives
        SHARP binary penetrance (chain->spec transition between weight 0
        and 0.2) while the record is graded (cross_a 0.52) — neoblast
        spec re-expression is stochastic at the cell level, so the
        effective per-seed spec fraction is Binomial(L, p): larger
        regenerates concentrate near the mean, small ones are
        all-or-nothing, and the binary 6 mV outcome threshold then
        splits seeds. The draw is GATED (no RNG contact at p == 1.0 or
        when the phi read is inactive) so every existing trajectory is
        bit-exact at the default.

        `spec_reanchor_p` (M30 AMENDED — regenerate-level stochastic
        re-anchoring) — exp38's per-cell version was REFUTED as
        registered: silencing individual cells does not grade the
        pattern because the chain RE-CARRIES the spec blend (each
        committed cell writes its blended value, so the next cell
        inherits it — expression failures do not accumulate; the error
        stayed ~3 mV at every p and no seed split). The stochastic unit
        must therefore be the regenerate, not the cell: the wound-face
        re-anchoring of the positional read (M28) is a ONE-TIME event
        per blastema, drawn ~ Bernoulli(spec_reanchor_p) at the start of
        each walk. A blastema that fails to re-anchor reads NO spec for
        its whole regenerate (pure chain inheritance). One parameter;
        no RNG contact at the default 1.0 or when the phi read is
        inactive (bit-exact).

        `anchor_from_history` (M31 STORED-HISTORY ANCHOR) — replaces the
        regrow-time re-anchoring coin flip with a property of the
        fragment's STORAGE HISTORY: the wound-face anchor is AVAILABLE
        iff the intact face cell's expressed identity still agrees with
        the identity that BELONGS at that coordinate,
        |theta[face] - phi_spec[face]| <= anchor_from_history (mV).
        Literature basis (exp44 research wave): positional information is
        CONSTITUTIVELY expressed from muscle and reset by wound signaling
        (Ross et al. 2022) — the read draws on a material state stored in
        the fragment (Egal-1/microtubule polarity substrate, 2025), not a
        fresh stochastic event at wound time. Deterministic — ZERO RNG
        contact; seed-splitting emerges from the seeds' genuinely
        different noise histories during the settle (real fragments
        differ the same way), not from regrow-time draws. The two faces
        of a direction="both" regen each evaluate their own history.
        Rule order: when anchor_from_history is not None it REPLACES the
        spec_reanchor_p draw; a face with no intact tissue (or out-of-
        range coordinate) has NO stored history at the wound face and
        the spec read stays OFF for that blastema. None default is
        bit-exact.

        `spec_reanchor_isolated` (M31-A — ISOLATED re-anchoring, exp45
        amendment) — exp45 REFUTED the registered M31: the model's
        settle history is seed-INVARIANT at macro scale (face drifts
        4.14/4.21/4.26 mV across seeds — deterministic deformation
        dominates), so no stored-state threshold can split seeds; the
        detrended fine structure does differ per seed but only at
        ~0.03 mV (micro-scale, un-fittable). The stochastic unit is
        therefore kept at the regenerate level (exp38's amendment) but
        its draw is MINTED FROM THE FRAGMENT'S OWN STORED STATE instead
        of the shared RNG stream: a per-blastema Bernoulli drawn from a
        dedicated Generator seeded by a blake2b digest of the quantized
        theta window at the wound face. Deterministic given the stored
        state (the coin IS a property of the fragment's history — the
        M31 goal), yet never touches self.rng, so arms that do not use
        the spec read stay BIT-EXACT (removes exp38's exact blocker:
        the re-anchor draw shifted the shared stream and flipped the
        marginal innexin seed). Zero RNG contact of either kind at the
        default 1.0 or when the phi read is inactive. Priority:
        anchor_from_history (if armed) > spec_reanchor_isolated (if
        armed) > spec_reanchor_p (legacy exp38 form).

        `neural_readout` (M33 — NON-JUNCTIONAL NEURAL/MUSCLE POLARITY
        CHANNEL, exp46) — the anterior pole is a constitutive,
        junction-INDEPENDENT identity source: wound-induced notum at
        anterior-facing wounds via the Egal-1/microtubule muscle
        substrate (2025), axon-aligned morphogen vector transport whose
        field coincides with nerve alignment (Lobo et al. 2019). When
        0 < w < 1 and the committing cell's spec identity is ANTERIOR
        (spec[i] >= NEURAL_SPEC_MIN), the M25 blind-guess fallback is
        blended with a direct neural read of the spec,
        guess <- (1-w)*guess + w*(spec[i] + N(0, eff_noise)) — the cell
        is no longer blind even with junctions down. Posterior
        identities do NOT qualify (no local pole — the recorded
        GJ-blockade phenomenology concentrates at posterior planes,
        innexin|tail 0.67 abnormal while innexin|head 0.00). Inert at
        full coupling (the guess branch is unused when r >= 1.0) and at
        the default 0.0 (bit-exact; no extra draws).

        `neural_misanchor` (M36 — MIS-ANCHORED POLE, exp57 egal-1 analog):
        the polarity substrate that CONFINES the anterior pole channel to
        anterior identities (Egal-1/microtubule longitudinal-muscle
        asymmetry, MED41099308: egal-1 RNAi or microtubule
        destabilization -> ECTOPIC notum at POSTERIOR-facing wounds ->
        posterior heads) is broken. When 0 < neural_misanchor <= 1, the
        pole channel's read at EVERY committing cell blends the guess
        with the ANTERIOR POLE's spec value (spec[0], the head program)
        instead of the cell's own identity: a posterior-facing wound
        under blockade ACTS LIKE an anterior wound — the two-headed
        direction. The weight multiplies neural_readout's (w =
        neural_readout * neural_misanchor semantics: misanchor REPLACES
        the identity test, the pole read itself draws spec[0]). Inert at
        the default 0.0 (bit-exact) and at full coupling (the guess
        branch is unused when r >= 1.0).

        M25 COUPLING-DEPENDENT READOUT (exp27 S2P1 repair): the inheritance
        read itself runs THROUGH the gap-junction network. At full coupling
        the readout is exactly the stored chain (bit-exact with the previous
        mechanism — no extra RNG draws when gap_scale == 1.0). Under
        blockade the blastema cannot read the pattern field and each
        committing cell falls back to the wound-state default plus a broad
        guess along the fate axis (spread blastema_readout_noise) — the
        graded, mixed-outcome phenomenology PlanformDB records for innexin
        RNAi. Restore junctions before regrowth and the readout recovers
        (T1.1c / exp27 S2C control)."""
        idx = list(np.arange(self.n)[region])
        if not idx:
            return
        steps_per_cell = max(1, int(round(cell_period / dt)))
        r = float(self.gap_scale)  # junction health at regen onset
        wound_center = float(np.mean(self.theta[idx]))
        eff_noise = float(noise) * float(commitment_noise_scale)
        g = float(length_gradient)
        # M30: expression draw only when the spec read is active AND the
        # probability is genuinely stochastic — zero RNG contact otherwise.
        expr_draw = 0.0 < float(spec_expression_p) < 1.0 \
            and phi_readout > 0.0
        expr_p = float(spec_expression_p)
        reanchor_draw = 0.0 < float(spec_reanchor_p) < 1.0 \
            and phi_readout > 0.0
        reanchor_p = float(spec_reanchor_p)
        # M31: history rule, when armed, replaces the regrow-time draw.
        hist_t = None if anchor_from_history is None else float(anchor_from_history)
        hist_spec = getattr(self, 'phi_spec', None)
        # M31-A: isolated re-anchoring draw (minted from stored state).
        iso_p = float(spec_reanchor_isolated)
        iso_draw = 0.0 < iso_p < 1.0 and phi_readout > 0.0
        neural_w = float(neural_readout)
        mis_w = float(neural_misanchor)
        arz_w = float(arz_readout)
        # M37 GENE LAYER: neoblast depletion — the regenerating tissue
        # cannot re-express identity (the planarian neoblast requirement,
        # smedwi-1/piwi-family RNAi: wound closes, blastema absent or
        # uncommitted — scar semantics). Blend the committed identity
        # toward the wound baseline; nb=0 bit-exact, nb=1 pure scar.
        nb_w = float(neoblast_depleted)

        def face_slope(face: int, sign: int) -> tuple[float, float, float, float]:
            """Anchor (theta at the face), per-cell theta trend on the intact
            side of the face, and the intact side's identity-repertoire
            [lo, hi] for gradient clipping. sign -1: anterior tissue,
            +1: posterior tissue. Deterministic — no RNG contact.
            gradient_window 0 => whole-fragment secant; window w => w-cell
            window adjacent to the face (M26a behavior when w == 5)."""
            if sign < 0:
                lo = max(0, face - gradient_window) if gradient_window > 0 else 0
                hi = face  # intact cells lo..face-1
            else:
                lo = face + 1
                hi = min(self.n, face + 1 + gradient_window) if gradient_window > 0 else self.n
            no_tissue = (hi - lo < 1) or (sign < 0 and face - 1 < 0) \
                or (sign > 0 and face + 1 > self.n - 1)
            fallback = float(self.theta[face if 0 <= face < self.n
                                        else (idx[0] if sign < 0 else idx[-1])])
            if no_tissue:
                return fallback, 0.0, fallback, fallback
            vals = self.theta[lo:hi]
            if len(vals) > 1:
                slope = float((vals[-1] - vals[0]) / (len(vals) - 1))
            else:
                slope = 0.0
            anchor = float(self.theta[face])
            return anchor, slope, float(np.min(vals)), float(np.max(vals))

        def walk(order: list[int], src: int, sign: int) -> None:
            anchor, slope, rep_lo, rep_hi = face_slope(src, sign)
            wander = 0.0
            d = 0
            # M30 amended: one-time per-blastema spec re-anchoring —
            # either the M31 stored-history rule (deterministic, zero RNG)
            # or the regrow-time Bernoulli draw (exp38 registered form).
            spec_on = True
            if hist_t is not None and phi_readout > 0.0:
                if hist_spec is None or not (0 <= src < self.n):
                    spec_on = False        # no stored history at this face
                else:
                    spec_on = abs(self.theta[src] - float(hist_spec[src])) \
                        <= hist_t
            elif iso_draw:
                # M31-A: the coin is minted from the fragment's own stored
                # state (quantized face window) — deterministic per stored
                # state, ZERO self.rng contact (other arms stay bit-exact).
                lo = max(0, src - 2)
                hi = min(self.n, src + 3)
                win = np.round(self.theta[lo:hi], 6)
                digest = hashlib.blake2b(
                    win.tobytes() + bytes([src & 0xFF]),
                    digest_size=8).digest()
                g_iso = np.random.default_rng(
                    int.from_bytes(digest, 'little'))
                spec_on = bool(g_iso.random() < iso_p)
            elif reanchor_draw:
                spec_on = self.rng.random() < reanchor_p
            for i in order:
                for _ in range(steps_per_cell):
                    self.step(dt)
                d += 1
                chain_base = self.theta[src]
                if g > 0.0:
                    extrap = anchor + slope * d
                    if gradient_clip and rep_lo < rep_hi:
                        extrap = min(max(extrap, rep_lo), rep_hi)
                    chain_base = (1.0 - g) * chain_base + g * extrap
                spec = getattr(self, 'phi_spec', None)
                if phi_readout > 0.0 and spec is not None and spec_on:
                    expressed = True
                    if expr_draw:
                        expressed = self.rng.random() < expr_p
                    if expressed:
                        w = phi_readout * r
                        chain_base = (1.0 - w) * chain_base \
                            + w * float(spec[i])
                if commitment_diffusion > 0.0:
                    wander += self.rng.normal(0.0, commitment_diffusion)
                theta_new = chain_base + self.rng.normal(0.0, eff_noise) \
                    + wander
                if r < 1.0:
                    # M35-A ARZ READOUT (night nine, amended): the 4D
                    # atlas's wound-proximal domain CONVERGES multi-lineage
                    # identity signals (MED42172041). The M25 guess base
                    # (wound_center) is ALREADY the wound region's stored
                    # repertoire mean — the first-registered base blend is
                    # a no-op (recorded as the M35 redundancy discovery).
                    # The convergence content is VARIANCE REDUCTION: the
                    # guess averages the ARZ_LINEAGES independent lineage
                    # reads (epidermal/neural/muscle — the three planarian
                    # lineages; K derived from the published lineage
                    # count, not fitted). arz_readout=0.0 is bit-exact
                    # (single draw, unchanged stream).
                    guess_base = wound_center
                    draw = self.rng.normal(0.0, self.blastema_readout_noise)
                    if arz_w > 0.0:
                        conv = float(np.mean([
                            self.rng.normal(0.0,
                                            self.blastema_readout_noise)
                            for _ in range(ARZ_LINEAGES)]))
                        draw = (1.0 - arz_w) * draw + arz_w * conv
                    guess = guess_base + draw
                    # M33: non-junctional neural/muscle readout for
                    # anterior identities — the pole channel bypasses the
                    # junction network entirely.
                    if neural_w > 0.0 and spec is not None \
                            and 0 <= i < self.n \
                            and float(spec[i]) >= NEURAL_SPEC_MIN:
                        nread = float(spec[i]) \
                            + self.rng.normal(0.0, eff_noise)
                        guess = (1.0 - neural_w) * guess + neural_w * nread
                    elif neural_w > 0.0 and mis_w > 0.0 and spec is not None:
                        # M36: mis-anchored pole — the confinement is
                        # broken; the wound reads the head program
                        # regardless of position (egal-1 direction).
                        nread = float(spec[0]) \
                            + self.rng.normal(0.0, eff_noise)
                        guess = (1.0 - neural_w * mis_w) * guess \
                            + neural_w * mis_w * nread
                    theta_new = r * theta_new + (1.0 - r) * guess
                if nb_w > 0.0:
                    # M37: neoblast-depleted commitment — the wound seals
                    # WITHOUT identity restoration (deterministic blend,
                    # no stream change; the identity information is
                    # simply absent, which is the biological claim).
                    theta_new = (1.0 - nb_w) * theta_new + nb_w * wound_center
                self.theta[i] = theta_new
                self.V[i] = theta_new
                src = i

        if direction == "forward":
            boundary = idx[0] - 1
            src = boundary if boundary >= 0 else idx[0]
            walk(idx, src, -1)
        elif direction == "backward":
            boundary = idx[-1] + 1
            src = boundary if boundary < self.n else idx[-1]
            walk(list(reversed(idx)), src, +1)
        elif direction == "both":
            h = len(idx) // 2
            fwd_b = idx[0] - 1
            fwd_src = fwd_b if fwd_b >= 0 else idx[0]
            walk(idx[:h], fwd_src, -1)
            bwd_b = idx[-1] + 1
            bwd_src = bwd_b if bwd_b < self.n else idx[-1]
            walk(list(reversed(idx[h:])), bwd_src, +1)
        else:
            raise ValueError(direction)

    def corrupt_region(self, region: slice, theta_value: float,
                       V_value: float | None = None) -> None:
        """Force a region into an arbitrary bioelectric state (pathology)."""
        self.theta[region] = theta_value
        if V_value is not None:
            self.V[region] = V_value

    # ------------------------------------------------------------------ steps
    def step(self, dt: float = 0.1) -> None:
        """One Euler-Maruyama step of the coupled dynamics.

        V and theta are held inside physiological bounds (Nernst/reversal-
        potential limits: no real membrane sustains |V| beyond ~100 mV).
        The bounds are INERT for every established experiment (exp1-11
        dynamics live well inside [-70, -10]); they only clip the
        pathological excursions a sustained artificial efferent (exp12's
        mind-body interface) can otherwise integrate without limit.
        """
        coupling = self.G @ self.V - self.V * self.deg
        dV = self.gamma * (self.theta - self.V) + coupling
        noise = self.noise_std * np.sqrt(dt) * self.rng.standard_normal(self.n)
        Vn = self.V + dt * dV + noise

        lap_theta = self.A @ self.theta - self.theta * self.A.sum(axis=1)
        # M25: pattern propagation is ALSO junction-carried — theta diffusion
        # scales with gap-junction health (bit-exact at gap_scale == 1.0).
        # With junctions down the stored pattern can no longer spread, so a
        # blind-regenerated region stays whatever the blastema guessed.
        dtheta = self.eps * (self.V - self.theta) \
            + self.mu * self.gap_scale * lap_theta

        # oncogene-like drivers (voltage-gated theta pulls)
        for idx, target, rate, vgate in self.theta_drivers:
            active = idx[self.V[idx] > vgate]
            if len(active):
                dtheta[active] += rate * (target - self.theta[active])

        drift = self.theta_drift * np.sqrt(dt) * self.rng.standard_normal(self.n)
        self.theta = np.clip(self.theta + dt * dtheta + drift,
                             V_PHYS_MIN, V_PHYS_MAX)
        self.V = np.clip(Vn, V_PHYS_MIN - 5.0, V_PHYS_MAX + 5.0)

        if self.clamps:
            idx = np.fromiter(self.clamps.keys(), dtype=int)
            vals = np.fromiter(self.clamps.values(), dtype=float)
            self.V[idx] = vals
            # clamped cells' plasticity sees the forced voltage
            self.theta[idx] += dt * self.eps * (vals - self.theta[idx])

    def run(self, duration: float, dt: float = 0.1, record_every: int = 0) -> np.ndarray | None:
        """Integrate for `duration` time units. Optionally record trajectories."""
        steps = int(round(duration / dt))
        if record_every > 0:
            n_rec = steps // record_every + 1
            rec = np.empty((n_rec, self.n))
            k = 0
            for t in range(steps):
                self.step(dt)
                if t % record_every == 0 and k < n_rec:
                    rec[k] = self.V
                    k += 1
            return rec[:k]  # trim any unfilled tail rows
        for _ in range(steps):
            self.step(dt)
        return None

    # ----------------------------------------------------------------- metrics
    def pattern_error(self, target: np.ndarray) -> float:
        """RMS deviation of the voltage pattern from a target pattern (mV)."""
        return float(np.sqrt(np.mean((self.V - target) ** 2)))

    def target_drift(self, theta0: np.ndarray) -> float:
        """RMS drift of the stored target memory from its original value."""
        return float(np.sqrt(np.mean((self.theta - theta0) ** 2)))
