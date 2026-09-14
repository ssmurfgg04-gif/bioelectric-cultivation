"""Phase B — the consciousness-body interface (qi circulation / autonomic
transcendence).

THE CLAIM UNDER TEST (cultivation Tier A)
------------------------------------------
Can a trained neural state influence non-neural tissue bioelectricity
BEYOND the autonomic ceiling? The novels call it qi circulation; the
biology calls it (the established part) autonomic efference — and the
established mechanism already crosses the mind-body line: the cholinergic
anti-inflammatory pathway (Borovikova et al. 2000; Tracey 2002 — vagus
stimulation suppresses macrophage TNF through nicotinic receptors: neural
activity changing immune-cell state), heart-rate-variability biofeedback
(Lehrer & Gevirtz 2014 — trained vagal control beyond naive range), and
meditation's measurable autonomic effects (Thayer & Lane's
neurovisceral-integration framework).

THE MODEL
---------
Neural layer: CTRNN (small-world, n=40) — the autonomic OS. A COHERENT
drive (sustained uniform input on an attention subset — the meditation
stand-in) pushes the network toward a coherent attractor; a RANDOM drive
of equal power is the control.

Efferent interface, two paths onto the non-neural collective's theta:
  - REFLEX path: fixed diffuse projection W_fixed, output CLIPPED at the
    autonomic ceiling (±2 mV — the hard-wired range real autonomic
    reflexes modulate slowly-variable tissue state within).
  - PLASTIC path: W_plastic, trained by three-factor (reward-modulated
    Hebbian) learning — activity x tissue-response x neuromodulatory
    reward. Subject to an L2 metabolic cost (synapses decay without use:
    nothing is free). NOT clipped at the reflex ceiling: its limit is the
    learned synaptic structure, not a hard clip — the question the model
    answers is how far training can actually push it.

Reward: the improvement of the tissue's DISCRETE pattern toward a target
(one adjacent-level zone shift — the smallest meaningful morphological
change; band width 10 mV means a useful pull must be ~5+ mV, far beyond
the 2 mV reflex ceiling).

WHAT WOULD FALSIFY THE TIER-A STORY: if training never pushes effective
tissue influence past the ceiling, or if RANDOM drive trains equally well
(coherence is not the carrier), or if the learned effect cannot flip
discrete states — then "trained mind influences body software beyond
autonomic reflex" is dead AT THIS MODELING LEVEL, and the honest
conclusion is that the ceiling is a training limit only in the novels.
"""

from __future__ import annotations

import numpy as np

from .ctrnn import CTRNN, make_small_world

# ------------------------------------------------------------------ constants
N_NEURAL = 40
N_TISSUE = 60
REFLEX_CEILING_MV = 2.0      # the hard-wired autonomic range
PLASTIC_L2 = 0.002           # metabolic decay of unused synapses
ETA_HEBB = 0.05              # three-factor learning rate
W_SAT = 3.0                  # synaptic saturation (mV/unit per synapse) —
                             # real synapses have finite strength; the cap
                             # bounds the plastic path's max output
POST_SAT_U = 2.0             # postsynaptic-tag saturation (mV/unit of
                             # efferent — the tag lives in u-space so the
                             # loop gain is duration-invariant)
ATTENTION_SIZE = 15          # the attention subset size (meditation stand-in)


class MindBodyInterface:
    """The trainable bridge: CTRNN (neural) -> theta pull (non-neural tissue).

    The tissue model is any object with `.theta`, `.V`, `.step(dt)` and a
    Laplacian-coupled theta dynamics (we use BioElectricCollective /
    LatchingCollective). The interface adds a theta bias each step:

        u_tissue = clip(W_fixed^T r, +-ceiling) + W_plastic^T r
        theta += dt * gain_eff * u_tissue

    r = tanh(V_neural) (firing rates in [-1, 1]).
    """

    def __init__(self, n_neural: int = N_NEURAL, n_tissue: int = N_TISSUE,
                 seed: int = 0, ceiling: float = REFLEX_CEILING_MV,
                 plastic_l2: float = PLASTIC_L2):
        rng = np.random.default_rng(seed)
        self.n_neural, self.n_tissue = n_neural, n_tissue
        self.ceiling = ceiling
        self.l2 = plastic_l2
        self.seed = seed
        # the attention subset (meditation acts on a subnetwork, not the
        # whole brain); both drive modes use the SAME subset at equal power
        self.attention = np.arange(min(ATTENTION_SIZE, n_neural))

        # neural layer: small-world CTRNN (the autonomic OS)
        W_net = make_small_world(n_neural, k=3, p=0.3, w=0.8, seed=seed)
        self.net = CTRNN(W_net, tau=1.0, noise=0.02, seed=seed + 1)

        # reflex path: diffuse fixed projection (weak, clipped)
        self.W_fixed = rng.normal(0, 0.3, (n_neural, n_tissue))
        # plastic path: starts at zero — the interface must be TRAINED
        self.W_plastic = np.zeros((n_neural, n_tissue))
        self.rng = rng

    # ---------------------------------------------------------------- neural
    def drive(self, mode: str, strength: float, subset=None) -> np.ndarray:
        """Build the input current. 'coherent' = sustained uniform on the
        attention subset (meditation); 'random' = equal-power noise on the
        SAME subset (the anti-qigong control: same power, no coherence)."""
        I = np.zeros(self.n_neural)
        idx = self.attention if subset is None else subset
        if mode == "coherent":
            I[idx] = strength
        elif mode == "random":
            I[idx] = strength * self.rng.choice(
                [-1.0, 1.0], size=len(idx))
        return I

    def rates(self, I: np.ndarray, settle: float = 6.0, dt: float = 0.05,
              window: float = 2.0) -> np.ndarray:
        """Run the neural layer under drive; return time-averaged rates."""
        self.net.run(settle, dt=dt, I=I)
        acc = np.zeros(self.n_neural)
        steps = int(window / dt)
        for _ in range(steps):
            self.net.step(dt, I)
            acc += np.tanh(self.net.V)
        return acc / steps

    def coherence(self, I: np.ndarray, settle: float = 6.0, dt: float = 0.05,
                  window: float = 4.0) -> float:
        """Mean pairwise correlation of neural voltages under drive —
        the coherence measure (order-parameter surrogate)."""
        self.net.run(settle, dt=dt, I=I)
        rec = []
        for _ in range(int(window / dt)):
            self.net.step(dt, I)
            rec.append(self.net.V.copy())
        X = np.array(rec)
        C = np.corrcoef(X.T)
        n = C.shape[0]
        return float(np.mean(C[np.triu_indices(n, 1)]))

    # -------------------------------------------------------------- interface
    def efferent(self, r: np.ndarray) -> np.ndarray:
        """Total theta-bias delivered to tissue (mV). Reflex path clipped;
        plastic path unclipped (its limit is learned structure + L2 cost)."""
        reflex = np.clip(self.W_fixed.T @ r, -self.ceiling, self.ceiling)
        plastic = self.W_plastic.T @ r
        return reflex + plastic

    def apply(self, tissue, r: np.ndarray, dt: float, duration: float,
              gain_eff: float = 1.0) -> None:
        """Drive the tissue with the current efferent pattern."""
        u = gain_eff * self.efferent(r)
        steps = int(duration / dt)
        for _ in range(steps):
            tissue.theta = tissue.theta + dt * u
            tissue.step(dt)

    def train_epoch(self, tissue, target_zone: slice, target_shift: float,
                    mode: str, strength: float, drive_dt: float = 0.05,
                    tissue_dt: float = 0.1, duration: float = 20.0,
                    eta: float = ETA_HEBB, subset=None,
                    reward_mode: str = "feedback") -> dict:
        """One training epoch: drive -> apply -> three-factor update.

        reward_mode:
          "feedback" — the target-seeking rule (reward-gated delta rule).
             The neuromodulator GATES plasticity (learning happens only
             under the feedback regime); the teaching tag is the per-cell
             REMAINING ERROR expressed in u-space: (wanted - got_j)/
             duration — the efferent correction needed, so the loop gain
             is duration-invariant (the first implementation tagged in
             got-space: one epoch's weight change moved the achieved
             shift by ~duration x eta x r, the loop gain exploded, and
             the weights pinned at saturation with +1000 mV overshoot).
             Potentiates while the target is unmet, depresses on
             overshoot, stops at the target.
          "tonic"    — the unguided control (Hansali et al. 2025's
             SSRI-mimic: incentive loop abrogated, neuromodulator pinned
             on, no error knowledge). Tag = the per-cell ACHIEVED ramp
             rate got_j/duration: plain correlation learning that
             reinforces whatever happened — expected to potentiate to the
             Oja ceiling (systematic overshoot), not acquire the target.
          "frozen"   — no weight update (the noreward retention arm: the
             policy runs, the learning does not).

        Every updating mode carries the Oja-style homeostatic term
        (activity-dependent synaptic scaling, Turrigiano 1999) + L2
        metabolic decay + hard synaptic saturation at +-W_SAT — three
        separate bounds on Hebbian positive feedback.
        """
        I = self.drive(mode, strength, subset)
        r = self.rates(I, dt=drive_dt)

        theta_before = tissue.theta[target_zone].copy()
        baseline_pull = float(np.mean(self.efferent(r)[target_zone]))
        self.apply(tissue, r, dt=tissue_dt, duration=duration)
        theta_after = tissue.theta[target_zone]

        wanted = target_shift
        got = theta_after - theta_before              # per-cell achieved shift
        got_mean = float(np.mean(got))
        # reported neuromodulator (saturating fraction of target achieved)
        rho = float(np.clip(got_mean / (wanted + 1e-9), -1.0, 1.0))

        if reward_mode == "feedback":
            post = np.clip((wanted - got) / duration, -POST_SAT_U, POST_SAT_U)
        elif reward_mode == "tonic":
            post = np.clip(got / duration, -POST_SAT_U, POST_SAT_U)
        else:  # frozen
            post = np.zeros_like(got)

        if reward_mode != "frozen" and np.any(post != 0.0):
            zone_mask = np.zeros(self.n_tissue, bool)
            zone_mask[target_zone] = True
            post_full = np.zeros(self.n_tissue)
            post_full[target_zone] = post
            dW = eta * (np.outer(r, post_full)
                        - (post_full ** 2)[None, :] * self.W_plastic)
            self.W_plastic += dW
            # metabolic cost: unused synapses decay
            self.W_plastic -= self.l2 * self.W_plastic
            # synaptic saturation (finite strength)
            np.clip(self.W_plastic, -W_SAT, W_SAT, out=self.W_plastic)

        return {"reward": rho, "zone_shift": got_mean,
                "theta_before": float(theta_before.mean()),
                "theta_after": float(theta_after.mean()),
                "plastic_norm": float(np.linalg.norm(self.W_plastic)),
                "baseline_pull_mV": baseline_pull}

    def learn_from_error(self, r: np.ndarray, target_zone: slice,
                         residual: np.ndarray, duration: float,
                         eta: float = ETA_HEBB) -> None:
        """Weight update from a maintenance session's residual error (the
        reward arm's within-retention refresh: tag = signed residual in
        u-space — always corrective, never runaway)."""
        post_full = np.zeros(self.n_tissue)
        post_full[target_zone] = np.clip(residual / duration,
                                         -POST_SAT_U, POST_SAT_U)
        if np.any(post_full != 0.0):
            dW = eta * (np.outer(r, post_full)
                        - (post_full ** 2)[None, :] * self.W_plastic)
            self.W_plastic += dW
            self.W_plastic -= self.l2 * self.W_plastic
            np.clip(self.W_plastic, -W_SAT, W_SAT, out=self.W_plastic)

    # ------------------------------------------------------------- metrics
    def passive_decay(self, units: float, tau: float = 40.0) -> None:
        """Exponential decay of synaptic strength during non-practice.

        tau in epoch-equivalent units. The tissue-side memory (the somatic
        latch) has its OWN persistence physics (frozen below the deadzone —
        Shomrat & Levin 2013: planarian memory persists >= 14 days); this
        decay applies to the NEURAL side only.
        """
        self.W_plastic *= np.exp(-units / tau)

    # ------------------------------------------------------------ persistence
    def save_policy(self) -> dict:
        """The discovered policy: everything needed to rebuild the trained
        interface open-loop (weights + wiring seeds). NOTE: the neural
        layer carries intrinsic noise (0.02), so a loaded policy reproduces
        the trained behavior DISTRIBUTION, not trajectory-exact values —
        the weights themselves are bit-exact."""
        return {"n_neural": self.n_neural, "n_tissue": self.n_tissue,
                "seed": self.seed, "ceiling": self.ceiling, "l2": self.l2,
                "attention": self.attention.tolist(),
                "W_plastic": self.W_plastic.tolist()}

    @classmethod
    def load_policy(cls, policy: dict) -> "MindBodyInterface":
        """Rebuild the EXACT trained interface (no re-training, no
        re-search) — the noreward arm's entry point."""
        ifc = cls(n_neural=policy["n_neural"], n_tissue=policy["n_tissue"],
                  seed=policy["seed"], ceiling=policy["ceiling"],
                  plastic_l2=policy["l2"])
        ifc.attention = np.asarray(policy["attention"], int)
        ifc.W_plastic = np.asarray(policy["W_plastic"], float)
        return ifc

    def effective_influence(self, tissue, target_zone: slice, mode: str,
                            strength: float, duration: float = 20.0,
                            dt: float = 0.1, subset=None) -> dict:
        """Sustained theta shift achievable in the target zone (mV)."""
        I = self.drive(mode, strength, subset)
        r = self.rates(I)
        theta0 = tissue.theta[target_zone].mean()
        self.apply(tissue, r, dt=dt, duration=duration)
        theta1 = tissue.theta[target_zone].mean()
        return {"shift_mV": float(theta1 - theta0),
                "efferent_rms_mV": float(np.sqrt(np.mean(
                    self.efferent(r)[target_zone] ** 2)))}

    def apply_corrective(self, tissue, r: np.ndarray, target: np.ndarray,
                         zone: slice, dt: float = 0.1, duration: float = 10.0,
                         closed_loop: bool = True, span: float = 10.0) -> dict:
        """A maintenance practice session: apply the learned efferent to the
        zone, either OPEN-LOOP (fixed magnitude — the frozen policy) or
        CLOSED-LOOP (per-cell scaling by the signed error toward target —
        the reward-shaped feedback path). Returns the zone error before and
        after the session."""
        u = self.efferent(r).copy()
        u_zone = u[zone]
        if closed_loop:
            err = target[zone] - tissue.V[zone]
            u_zone = u_zone * np.clip(err / span, -1.0, 1.0)
        else:
            u_zone = u_zone * 1.0
        u = np.zeros_like(u)
        u[zone] = u_zone
        err_before = float(np.mean(np.abs(target[zone] - tissue.V[zone])))
        steps = int(duration / dt)
        for _ in range(steps):
            tissue.theta = tissue.theta + dt * u
            tissue.step(dt)
        err_after = float(np.mean(np.abs(target[zone] - tissue.V[zone])))
        return {"err_before_mV": err_before, "err_after_mV": err_after}
