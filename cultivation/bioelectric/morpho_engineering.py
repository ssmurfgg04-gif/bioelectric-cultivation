"""Phase A — engineering NOVEL morphologies (body tempering / vessel rewriting).

THE QUESTION exp1 never asked
-----------------------------
exp1 reproduced Levin's RESTORATIVE results (two-headed reprogramming,
cancer normalization): pushing the collective back to a KNOWN attractor,
with persistence measured over short horizons (~20 time units). Cultivation
Tier B claims more — writing body plans that do not exist in nature: a
third eye (a novel depolarized organ zone mid-trunk), a novel cell state
(level-4 zones absent from wild-type), segmented ladders, reversed
polarity — via sparse voltage clamps, with protocols DISCOVERED by CEM.

THE PHYSICS UPGRADE THIS MODULE INTRODUCES: the latching somatic memory
---------------------------------------------------------------
The base collective (exp1-9) has theta as a slave of V with spatial
smoothing — patterns erode on ~100-unit timescales, which exp1's short
horizons never exposed. Real planarian reprogramming persists for the
animal's LIFE (Durant et al. 2017: two-headed animals keep the target
across months and repeated amputations). The established model (Pezzulo &
Levin 2021, bistable somatic memory; Nuzzo et al. for the biochemical
latch) has each cell's stored target held by a cell-autonomous LATCH:

    d(anchor_i)/dt = alpha * (V_i - anchor_i)   ONLY while
                     |V_i - anchor_i| > deadzone

Below the deadzone the memory is FROZEN (latched); above it, SUSTAINED
forcing integrates the memory toward the forced voltage. This single
mechanism gives: (a) indefinite pattern persistence (the anchor pins
theta against Laplacian erosion), (b) the 24h-sustained-perturbation
requirement (transient forcing barely moves the latch), (c) the
sub-threshold dose-response (perturbations inside the deadzone never
rewrite — exp1's T1.3), and (d) the two-headed permanence across
amputations (the anchor survives in remaining cells and is inherited
by regrowth).

LatchingCollective subclasses BioElectricCollective; exp1-9 physics is
unchanged (they never test long horizons).

TESTS (each pre-registered in exp11):
  1. REACHABILITY — CEM finds clamp protocols that LATCH novel targets.
  2. STABILITY — the latched pattern holds over long free dynamics.
  3. REGENERATIVE MEMORY — local positional memory: partial amputation
     re-extends the novel identity; full amputation loses it (no archival
     backup for internal novel structures).
  4. DIFFICULTY SCALING — engineering cost vs novel-boundary count.
  5. CONTROLS — twoheaded (Levin anchor) and deep-restorative baseline.
"""

from __future__ import annotations

import numpy as np

from ..inverse.cem import cem_optimize
from .collective import V_PHYS_MIN, V_PHYS_MAX
from .collective import BioElectricCollective
from .fidelity import quantize

N_CELLS = 100
LEVELS = 7

# latch parameters (Levin-layer calibrated: sustained forcing integrates
# the memory; the anchor pins theta hard enough that boundary Laplacian
# pull cannot re-open the latch after release)
ALPHA_LATCH = 0.042     # 1/unit — latch integration rate
DEADZONE_MV = 5.0       # below this deviation the memory is frozen
K_ANCHOR = 0.25         # theta's relaxation rate toward its anchor


class LatchingCollective(BioElectricCollective):
    """BioElectricCollective + cell-autonomous latching target memory.

    theta is pinned to a per-cell anchor (the morphogenetic memory);
    the anchor moves only under SUSTAINED voltage deviation beyond the
    deadzone. All base-class interventions (clamp, amputate, regrow,
    gap-junction blockade) work unchanged; regrow additionally inherits
    the anchor (positional memory carried by surviving neighbor cells).
    """

    def __init__(self, *a, alpha_latch: float = ALPHA_LATCH,
                 deadzone: float = DEADZONE_MV, k_anchor: float = K_ANCHOR,
                 **kw):
        super().__init__(*a, **kw)
        self.alpha_latch = alpha_latch
        self.deadzone = deadzone
        self.k_anchor = k_anchor
        self.theta_anchor = self.theta.copy()

    def set_anchor(self, anchor: np.ndarray) -> None:
        self.theta_anchor = np.asarray(anchor, float).copy()

    def set_target(self, theta: np.ndarray, sync_anchor: bool = True) -> None:
        """Set the stored target; by default the latch memory follows (the
        natural semantics: the target IS the latched memory)."""
        super().set_target(theta)
        if sync_anchor:
            self.theta_anchor = self.theta.copy()

    def step(self, dt: float = 0.1) -> None:
        # latch dynamics: integrate the anchor toward V only under
        # sustained beyond-deadzone deviation
        dev = self.V - self.theta_anchor
        move = np.where(np.abs(dev) > self.deadzone,
                        self.alpha_latch * dev, 0.0)
        self.theta_anchor = self.theta_anchor + dt * move
        # theta relaxes toward the anchor (memory pinning) — injected as an
        # extra pull on top of the base dynamics by temporarily biasing
        # theta's target: we re-use the base step, then apply the pull.
        super().step(dt)
        # base step already moved theta via eps(V-theta)+mu*lap; add the
        # anchor pull (explicit Euler on the pinning term)
        self.theta = np.clip(
            self.theta + dt * self.k_anchor * (self.theta_anchor - self.theta),
            V_PHYS_MIN, V_PHYS_MAX)
        # clamps pin V; the anchor latches to clamped values through dev

    def amputate(self, region: slice, wound_voltage: float = -30.0,
                 blastema_theta: float = -40.0) -> None:
        super().amputate(region, wound_voltage, blastema_theta)
        self.theta_anchor[region] = blastema_theta

    def regrow(self, region: slice, cell_period: float = 0.8, dt: float = 0.1,
               noise: float = 0.6) -> None:
        """Regrowth inherits BOTH theta and the anchor from the boundary
        cell — positional memory is carried by surviving tissue."""
        idx = list(np.arange(self.n)[region])
        if not idx:
            return
        boundary = idx[0] - 1
        src = boundary if boundary >= 0 else idx[0]
        steps_per_cell = max(1, int(round(cell_period / dt)))
        for i in idx:
            for _ in range(steps_per_cell):
                self.step(dt)
            self.theta[i] = self.theta[src] + self.rng.normal(0.0, noise)
            self.theta_anchor[i] = self.theta_anchor[src] \
                + self.rng.normal(0.0, noise)
            self.V[i] = self.theta[i]
            src = i


# --------------------------------------------------------------------- targets
def target_wildtype(n: int = N_CELLS) -> np.ndarray:
    t = np.full(n, -50.0)
    t[: n // 4] = -20.0
    return t


def target_third_eye(n: int = N_CELLS) -> np.ndarray:
    """A novel depolarized organ zone mid-trunk — structure that does not
    exist in the wild-type pattern (the 1D 'third eye')."""
    t = target_wildtype(n)
    t[45:60] = -20.0
    return t


def target_dual_zone(n: int = N_CELLS) -> np.ndarray:
    """Two novel symmetric zones at level 4 (-30 mV) — a cell STATE absent
    from the wild-type pattern (which uses levels 5 and 2): a novel type."""
    t = target_wildtype(n)
    t[38:46] = -30.0
    t[70:78] = -30.0
    return t


def target_ladder(n: int = N_CELLS) -> np.ndarray:
    """Alternating segmentation — many novel boundaries, far from wild-type."""
    t = np.full(n, -50.0)
    t[: n // 4] = -20.0
    for start in range(n // 4, n, 24):
        t[start: start + 12] = -20.0
    return t


def target_mirror(n: int = N_CELLS) -> np.ndarray:
    """Reversed polarity: head identity at the posterior end."""
    return target_wildtype(n)[::-1].copy()


def anchor_corrupted(n: int = N_CELLS) -> np.ndarray:
    """The deep-restorative start state: the MEMORY itself is corrupted
    (entrenched pathology — the bioelectric disease state), not just V.
    Reprogramming back to wild-type must rewrite the latch."""
    t = target_wildtype(n)
    t[20:40] = -20.0      # ectopic depolarized domain (tumor-like)
    t[70:80] = -30.0      # second corrupted domain
    return t


NOVEL_TARGETS = {
    "third_eye": target_third_eye,
    "dual_zone": target_dual_zone,
    "ladder": target_ladder,
    "mirror": target_mirror,
}


def novel_boundary_count(target: np.ndarray, wildtype: np.ndarray) -> int:
    q_t = quantize(target, LEVELS)
    q_w = quantize(wildtype, LEVELS)
    return int(np.sum(q_t != q_w))


def _edge_keep(target: np.ndarray, levels: int = LEVELS) -> np.ndarray:
    """Edge guard (same discipline as exp8's fidelity metric): cells at a
    level-discontinuity of the TARGET sit on genuinely graded boundaries —
    their correct discrete state is ambiguous, so they are excluded."""
    q = quantize(target, levels)
    d = np.abs(np.diff(q)) > 0
    keep = np.ones(len(q), bool)
    keep[:-1] &= ~d
    keep[1:] &= ~d
    return keep


def discrete_fidelity(V, target, levels: int = LEVELS) -> float:
    """Fraction of non-boundary cells in the target's discrete Vmem band."""
    keep = _edge_keep(target, levels)
    if keep.sum() == 0:
        return 1.0
    ok = quantize(V, levels) == quantize(target, levels)
    return float(ok[keep].mean())


# ------------------------------------------------------------------ protocols
class ClampProtocol:
    """Reprogramming protocol: M clamp sites + duration + junction scaling.

    u = [pos_1, halfwidth_1, volt_1, ..., pos_M, halfwidth_M, volt_M,
         duration, gap_scale]
    """

    def __init__(self, u, n_sites: int = 3):
        self.n_sites = n_sites
        u = np.asarray(u, float)
        self.sites = []
        for i in range(n_sites):
            pos = int(np.clip(round(u[3 * i]), 0, N_CELLS - 1))
            hw = int(np.clip(round(u[3 * i + 1]), 1, 25))
            volt = float(np.clip(u[3 * i + 2], -70.0, -10.0))
            self.sites.append((pos, hw, volt))
        self.duration = float(np.clip(u[3 * n_sites], 2.0, 150.0))
        self.gap_scale = float(np.clip(u[3 * n_sites + 1], 0.05, 2.0))

    def apply(self, col: BioElectricCollective, dt: float = 0.1):
        """Apply the sites FIRST-WINS: cells claimed by an earlier site are
        not re-clamped by later ones (real electrode arrays cannot stack
        conflicting commands — and the decoder must not create last-write
        pathologies the search can fall into)."""
        if self.gap_scale != 1.0:
            col.block_gap_junctions(self.gap_scale)
        claimed: set[int] = set()
        for pos, hw, volt in self.sites:
            idx = [i for i in range(max(0, pos - hw), min(col.n, pos + hw + 1))
                   if i not in claimed]
            for i in idx:
                col.clamps[int(i)] = volt
                claimed.add(int(i))
        col.run(self.duration, dt=dt)
        col.release_clamps()
        if self.gap_scale != 1.0:
            col.restore_gap_junctions(1.0)


def evaluate_protocol(u, target, seed: int = 0, n: int = N_CELLS,
                      settle: float = 300.0, dt: float = 0.1,
                      start_anchor=None) -> dict:
    """Force -> release -> settle -> score. The full Phase-A pipeline."""
    col = LatchingCollective(n=n, seed=seed)
    col.set_target(target_wildtype(n))
    col.set_state(target_wildtype(n) + col.rng.normal(0, 2.0, n))
    if start_anchor is not None:
        col.set_anchor(np.asarray(start_anchor, float))
    proto = ClampProtocol(u)
    proto.apply(col, dt=dt)

    fid_release = discrete_fidelity(col.V, target)
    hist_every = max(1, int(10.0 / dt))
    rec = col.run(settle, dt=dt, record_every=hist_every)
    if rec is None:
        rec = np.zeros((1, n))
    fids = [discrete_fidelity(rec[k], target) for k in range(len(rec))]
    return {
        "fid_release": fid_release,
        "fid_settled": discrete_fidelity(col.V, target),
        "fid_traj": fids,
        "anchor_latched": float(np.mean(
            quantize(col.theta_anchor, LEVELS) == quantize(target, LEVELS))),
        "rms": float(np.sqrt(np.mean((col.V - target) ** 2))),
        "protocol": {"sites": proto.sites, "duration": proto.duration,
                     "gap_scale": proto.gap_scale},
    }


# ---------------------------------------------------------------- the search
def null_protocol_u(n: int = N_CELLS):
    """The do-nothing protocol: three 1-cell clamps at wild-type-consistent
    trunk values, minimal duration, normal junctions — no latch changes."""
    return np.array([10, 1, -50.0, n // 2, 1, -50.0, n - 10, 1, -50.0,
                     2.0, 1.0])


def discover_protocol(target, seed: int = 0, n: int = N_CELLS,
                      pop: int = 50, iters: int = 15, start_anchor=None,
                      restarts: int = 2, verbose: bool = False):
    """CEM search (with restarts) for the clamp protocol that engineers
    `target`.

    Fitness = -(settled fidelity - DO-NOTHING BASELINE), two seeds.
    The baseline subtraction is the anti-deception term: an un-manipulated
    collective already scores ~0.85 against a novel target (everything
    except the novel zone matches). Without subtracting it, the search can
    converge to 'don't try' — clamping the novel zone to WILD-TYPE values
    and harvesting the free score (a deception the first search fell into;
    protocol history recorded in the results JSON). Restarts counter the
    sharp-peak-in-a-plateau structure of builder protocols."""
    bounds = []
    for _ in range(3):
        bounds += [(0, n - 1), (1, 25), (-70.0, -10.0)]
    bounds += [(2.0, 150.0), (0.05, 2.0)]

    u_null = null_protocol_u(n)
    base = float(np.mean([
        evaluate_protocol(u_null, target, seed=s, n=n,
                         start_anchor=start_anchor)["fid_settled"]
        for s in (seed, seed + 1)]))

    def fitness(u):
        fids = [evaluate_protocol(u, target, seed=s, n=n,
                                  start_anchor=start_anchor)["fid_settled"]
                for s in (seed, seed + 1)]
        return -(float(np.mean(fids)) - base)

    best_u, best_f, best_hist = None, np.inf, None
    for r in range(restarts):
        u, f, hist = cem_optimize(fitness, bounds, pop=pop, iters=iters,
                                  seed=1000 * r, verbose=verbose)
        if f < best_f:
            best_u, best_f, best_hist = u, f, hist
    return best_u, -best_f, best_hist


# -------------------------------------------------------------- regeneration
def regeneration_test(u, target, seed: int = 0, n: int = N_CELLS,
                      dt: float = 0.1,
                      latch_kw: dict | None = None) -> dict:
    """Establish the novel pattern, then amputate the region carrying it.

    latch_kw: optional overrides (k_anchor, alpha_latch, deadzone, mu_theta)
    passed to BOTH collectives — the exp13 C4 sweep hooks.

    Target-aware arms:
      partial — the distal part of the novel zone removed; novel cells
                remain at the boundary: regrowth re-extends the novel
                identity (latch inherited from surviving cells), possibly
                with OVERSHOOT (the when-to-stop problem).
      full    — the whole novel zone + margins removed: sequential
                inheritance has no remaining source of novel identity ->
                the structure is lost. LOCAL positional memory: no
                archival backup for internal novel structures.
    """
    kw = latch_kw or {}
    col = LatchingCollective(n=n, seed=seed, **kw)
    col.set_target(target_wildtype(n))
    col.set_state(target_wildtype(n) + col.rng.normal(0, 2.0, n))
    proto = ClampProtocol(u)
    proto.apply(col, dt=dt)
    col.run(100.0, dt=dt)

    novel_zone = quantize(target, LEVELS) != quantize(target_wildtype(n), LEVELS)
    zone_idx = np.arange(n)[novel_zone]
    if len(zone_idx) == 0:
        return {"error": "target has no novel zone"}
    z0, z1 = int(zone_idx[0]), int(zone_idx[-1])

    q_tar = quantize(target, LEVELS)
    q_wt = quantize(target_wildtype(n), LEVELS)

    arms = {
        "partial": slice(z0 + max(3, (z1 - z0) // 3), min(z1 + 5, n)),
        "full": slice(max(0, z0 - 5), min(z1 + 5, n)),
    }
    out = {"zone": [z0, z1]}
    for arm, sl in arms.items():
        c2 = LatchingCollective(n=n, seed=seed + 100, **kw)
        c2.set_target(col.theta.copy())
        c2.set_state(col.V.copy())
        c2.set_anchor(col.theta_anchor.copy())
        c2.amputate(sl)
        c2.regrow(sl)
        c2.run(150.0, dt=dt)
        regrown = np.zeros(n, bool)
        regrown[sl] = True
        q_reg = quantize(c2.V, LEVELS)
        novel_cells = [i for i in range(n) if regrown[i] and q_tar[i] != q_wt[i]]
        trunk_cells = [i for i in range(n) if regrown[i] and q_tar[i] == q_wt[i]]
        out[arm] = {
            "novel_identity_fraction": (
                float(np.mean([q_reg[i] == q_tar[i] for i in novel_cells]))
                if novel_cells else None),
            "overshoot_fraction": (
                float(np.mean([q_reg[i] != q_wt[i] for i in trunk_cells]))
                if trunk_cells else None),
            "fidelity": discrete_fidelity(c2.V, target),
        }
    return out
