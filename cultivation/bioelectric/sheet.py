"""2D bioelectric sheet — the graft/lateral representation (night-eight).

THE PROBLEM (night-eight queue #3): the 1D chain model has no lateral
axis, so graft and lateral-cut protocols (the largest remaining H gap in
exp51's decomposition) cannot be represented. The published solution shape
is the SYMMETRY HYPOTHESIS (Saito et al. 2003, Dev Dyn, DOI
10.1002/dvdy.10246 — verified via Crossref): planarian tissues carry
SYMMETRIC positional values across the left-right axis; mediolateral (M-L)
intercalation generates positional values along that axis; and midline
tissues implanted into a lateral region induce a COMPLETE ECTOPIC HEAD.
The midline is not a wall — it is a SOURCE of the axis.

THE MODEL (new module, additive — touches nothing in collective.py):

  A 2D lattice (h x w) with TWO INDEPENDENT position fields:
    theta_ap  — the A-P identity field (head = -20 mV depolarized top,
                trunk = -50 mV; the morphospace conventions)
    theta_ml  — the M-L positional field, sign-reversing across the
                midline column (negative left / positive right), with the
                midline column PINNED to zero: the axis source boundary.

  Grafts transplant a donor block's STORED fields (both layers) into the
  host. A donor block that contains the midline column KEEPS ITS ACTIVE
  SOURCE: the transplanted zero column stays pinned after grafting (the
  published organizer property of midline tissue).

  INTERCALATION RULE (the model's instantiation of M-L intercalation):
  wherever two horizontally adjacent cells carry OPPOSITE-SIGN ML values
  (opposing positional values brought into contact — Saito's condition),
  both contact cells' AP identity is driven toward the pole value for the
  duration of the contact. The M-L geometry is static during the
  intercalation phase (the mismatch is set by the graft geometry; AP
  re-specification runs to steady state under the sustained contact
  drive). This is deliberately parameter-light: one drive gain, one
  diffusion coefficient, the morphospace thresholds.
"""
from __future__ import annotations

import numpy as np

HEAD_V = -20.0          # depolarized pole identity (morphospace convention)
TRUNK_V = -50.0
HEAD_THRESH = -32.5     # head-likeness threshold (morphospace convention)
HEAD_FRACTION = 0.25    # native head zone = top quarter of the sheet


class BioelectricSheet:
    """A 2D AP x ML sheet with two independent position fields."""

    def __init__(self, h: int = 40, w: int = 24, seed: int = 0):
        self.h = int(h)
        self.w = int(w)
        self.rng = np.random.default_rng(seed)
        self.midline = self.w // 2
        # AP field: wild-type axis (head top quarter, trunk below)
        ap = np.full((self.h, self.w), TRUNK_V)
        ap[: int(self.h * HEAD_FRACTION), :] = HEAD_V
        self.theta_ap = ap
        # ML field: sign-reversing across the midline (symmetry hypothesis)
        cols = np.arange(self.w) - self.midline
        self.theta_ml = np.tile(cols / max(self.midline, 1),
                                (self.h, 1)).astype(float)
        # boundary conditions: the native sources
        self._ap_pins = {(0, j): HEAD_V for j in range(self.w)}
        self._ml_pins = {(i, self.midline): 0.0 for i in range(self.h)}
        # transplanted active sources (midline donors keep their axis):
        # list of (row0, row1, col0, col1, frozen_ml_values) — a grafted
        # midline MAINTAINS ITS OWN INTERNAL AXIS against host diffusion
        # (the published organizer property); a non-source graft's ML
        # values blend into the host by diffusion instead.
        self._graft_sources: list[tuple[int, int, int, int, np.ndarray]] = []

    # ------------------------------------------------------------- dynamics
    def _lap(self, f: np.ndarray) -> np.ndarray:
        out = np.zeros_like(f)
        out[1:-1, :] += f[:-2, :] + f[2:, :]
        out[:, 1:-1] += f[:, :-2] + f[:, 2:]
        deg = np.full_like(f, 2.0)
        deg[:, 1:-1] = 4.0
        deg[0, :] = deg[-1, :] = (2.0 if self.h <= 2 else 3.0)
        deg[:, 0] = deg[:, -1] = np.minimum(deg[:, 0], 3.0)
        # corners: degree 2
        deg[0, 0] = deg[0, -1] = deg[-1, 0] = deg[-1, -1] = 2.0
        return out - deg * f

    def settle(self, steps: int = 240, diffusion: float = 0.05,
               noise: float = 0.02) -> None:
        """Relax both fields toward the sourced equilibrium (with noise)."""
        for _ in range(steps):
            lap_ap = self._lap(self.theta_ap)
            lap_ml = self._lap(self.theta_ml)
            self.theta_ap += diffusion * lap_ap \
                + self.rng.normal(0.0, noise, self.theta_ap.shape)
            self.theta_ml += diffusion * lap_ml
            self._apply_pins()

    def _apply_pins(self) -> None:
        for (i, j), v in self._ap_pins.items():
            self.theta_ap[i, j] = v
        for (i, j), v in self._ml_pins.items():
            self.theta_ml[i, j] = v

    # ---------------------------------------------------------------- graft
    def take_block(self, r0: int, c0: int, bh: int, bw: int) -> dict:
        """Harvest a donor block (both stored fields, deep copy)."""
        r1, c1 = r0 + bh, c0 + bw
        contains_midline = (c0 <= self.midline < c1)
        return {
            "ap": self.theta_ap[r0:r1, c0:c1].copy(),
            "ml": self.theta_ml[r0:r1, c0:c1].copy(),
            "contains_midline": contains_midline,
        }

    def graft(self, donor: dict, r0: int, c0: int,
              carries_source: bool | None = None) -> None:
        """Transplant the donor block at (r0, c0): both fields are
        overwritten with the donor's stored values. A midline donor keeps
        its ACTIVE source (the transplanted zero column broadcasts the axis
        into its surroundings during intercalation) unless
        carries_source=False (the disrupted-source ablation analog).
        Native midline pins inside the graft footprint are removed — the
        graft replaces that tissue."""
        bh, bw = donor["ap"].shape
        r1, c1 = min(r0 + bh, self.h), min(c0 + bw, self.w)
        bh2, bw2 = r1 - r0, c1 - c0
        self.theta_ap[r0:r1, c0:c1] = donor["ap"][:bh2, :bw2]
        self.theta_ml[r0:r1, c0:c1] = donor["ml"][:bh2, :bw2]
        # the graft replaces the host tissue incl. any native midline pins
        for j in range(c0, c1):
            for i in range(r0, r1):
                self._ml_pins.pop((i, j), None)
        active = donor["contains_midline"] if carries_source is None \
            else bool(carries_source)
        self._graft_sources = []
        if active:
            self._graft_sources.append(
                (r0, r1, c0, c1, donor["ml"][:bh2, :bw2].copy()))
        self._apply_pins()

    # --------------------------------------------------------- intercalation
    def _apply_graft_sources(self) -> None:
        """A grafted midline MAINTAINS its own stored ML axis: the frozen
        values are re-imposed every step (the organizer property — the
        graft's internal L-R contrast is not absorbed by the host)."""
        for (r0, r1, c0, c1, vals) in self._graft_sources:
            self.theta_ml[r0:r1, c0:c1] = vals

    def intercalate(self, steps: int = 400, diffusion: float = 0.05,
                    drive_gain: float = 0.5,
                    discontinuity_thresh: float = 0.2) -> None:
        """M-L intercalation phase (coupled):
          ML: diffusion (graft-source regions held — the organizer keeps
              its axis; a non-source graft's values blend into the host).
          AP: the intercalation drive fires where horizontally adjacent
              cells present a ZERO-CROSSING DISCONTINUITY — opposing ML
              signs whose contrast EXCEEDS the physiological adjacent
              gradient (the smooth native axis, |dML| ~ 1/w, never fires;
              the midline is homeostatic, not inductive). Both contact
              cells' AP identity is driven toward the pole with strength
              proportional to the EXCESS contrast (Saito's intercalation:
              opposing positional values in contact re-create the A-P
              axis)."""
        for _ in range(steps):
            # ML substep: diffusion + organizer hold + native pins
            lap_ml = self._lap(self.theta_ml)
            self.theta_ml += diffusion * lap_ml
            self._apply_graft_sources()
            # AP substep: intercalation drive on zero-crossing
            # discontinuities above the physiological gradient
            ml = self.theta_ml
            sgn = np.sign(ml)
            opp = (sgn[:, :-1] * sgn[:, 1:]) < 0
            excess = np.abs(ml[:, :-1] - ml[:, 1:]) - discontinuity_thresh
            fire = opp & (excess > 0)
            drive = fire * excess
            dl = np.zeros_like(self.theta_ap)
            dr = np.zeros_like(self.theta_ap)
            dl[:, :-1] += drive
            dr[:, 1:] += drive
            lap_ap = self._lap(self.theta_ap)
            self.theta_ap += diffusion * lap_ap \
                + drive_gain * (dl + dr) * (HEAD_V - self.theta_ap)
            self._apply_pins()

    # --------------------------------------------------------------- readout
    def head_fraction(self, region: tuple[slice, slice]) -> float:
        """Fraction of head-identity cells (theta_ap >= HEAD_THRESH)."""
        seg = self.theta_ap[region[0], region[1]]
        return float(np.mean(seg >= HEAD_THRESH))

    def half_fractions(self, region: tuple[slice, slice]) -> tuple[float, float]:
        """Head fractions of the LEFT and RIGHT halves of a region."""
        rs, cs = region
        mid = (cs.start + cs.stop) // 2
        return (self.head_fraction((rs, slice(cs.start, mid))),
                self.head_fraction((rs, slice(mid, cs.stop))))
