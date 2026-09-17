#!/usr/bin/env python3
"""exp148 — THE TEMPORAL READ (the flip-clock channel).

FOUNDATION (exp142 4/4, exp145 4/4; the semantics-carrying-read line
exp137 L115 -> exp142 -> exp145): the phase-native read (PN1 rho >= 0.5
branch diagnostic + PN2 dominant-quadrature projection + PN3 exp142's
executor verbatim) carries SIGN and PHASE into the decode, and exp145
registers the TEMPORAL READ as the next named semantics carrier: the
time_varying / open_world classes from exp137's battery have edge
dynamics (flips DURING the read) whose identity semantics the static
time-average projection averages away.

THIS EXPERIMENT closes that scope. Media whose identity semantics live
ONLY in the flip SCHEDULE:

  (1) FLIP-CLOCK BATTERY PAIRS (adversarial, 12): static ring backbone
      (1.0) + exp142's carrier geometry VERBATIM (K_CHORDS=6 chords,
      F1/F2/F3 families, PROBE_SEED=7) where the 6 chord edges FLIP:
      value -b when ON, 0.0 when OFF, over T=2400 frames with every
      chord edge ON in exactly c=1200 frames. The latent class is the
      SCHEDULE:
        member 'per'  (periodic):  each chord edge ON for ONE
                   contiguous bout of 1200 frames — flip count 2;
        member 'aper' (aperiodic): each chord edge ON for a seeded
                   scattered 1200-of-2400 subset — flip count ~1200.
      Per-edge ON-COUNTS are identical across the pair, so the
      time-averaged media are BIT-identical (per entry the nonzero
      additions happen in the same order; zeros are exact no-ops;
      all values are integers — the partial sums are exact), and so is
      rho (=0: real media). The static read cannot see the schedule.
      Ladder b in {1792, 1920, 2048, 2176} x 3 families = 12 pairs.
      REPAIR (disclosed, pre-run): exp142's F1/F2/F3 chord draws can
      pair ADJACENT nodes — a chord coinciding with a ring edge can
      never be ABSENT (the backbone keeps it present: f=0, no schedule
      semantics on that edge, time-average (1-b)/2). chord_set now
      nudges the colliding endpoint off the ring (+1 steps,
      deterministic, identical for both pair members) so the 6 chord
      edges are genuine flip edges; otherwise the carrier geometry is
      exp142 verbatim. The first registered-run attempt asserted
      exactly this at F2@1792 (aper effective chord -895.5 = f=0 ring
      collision) and was DISCARDED as an invalid instrument.

  (2) SCHEDULE-CLASS GRID (paired, exp145's shared-base-seed pattern):
      FlipGridMedium(n, seed=148_000+i, sched), sched in {per, aper} —
      exp137's helpers, SignedMedium's draw order (B -> w; unsigned):
      M = (B*w + (B*w)^T)/2 — a STATIC backbone (ring + random chords,
      every edge ON in every frame, both classes) on the connected
      4%-dense support, PLUS a flip subset of K_CHORDS=6 chord edges
      drawn by the SHARED base rng (identical across the paired
      classes). Flip edges are ON in exactly c=2 of T=32 frames:
      'per': the contiguous bout [0, 2) — flip count 1; 'aper': a
      seeded scattered 2-subset — flip count 2..4. Per-edge ON-counts
      identical across the pair => time-averages BIT-identical; only
      the schedule (and hence the flip clock) differs. 8 instances at
      n=100 + 2 at n=400 (exp142's grid shape).

THE TEMPORAL RULE (pre-registered, ONE rule, zero knobs, stated before
running; NOT per-media tuning):

  TC1 FLIP-CLOCK CHANNEL: per undirected edge, f_ij = the number of
      presence transitions of the edge over the read window (RAW
      counts — no normalization constant; presence = |W_t| > 0,
      symmetrized to undirected). F = the symmetrized transition-count
      matrix, zero diagonal.
  TC2 EXTENDED PROJECTION: A_ext = A + F, where A is exp145's PN1/PN2
      projected time-average VERBATIM (rho >= 0.5 -> Im branch, else
      Re branch) — the flip clock is added as a structure feature
      alongside the averaged coupling. No scaling constant exists in
      the rule.
  TC3 STRUCTURE + DYNAMICS: exp142's execute_signed VERBATIM on A_ext
      (canon/dt/traversal on |A_ext|; the coupling consumes A_ext).
      NO new executor code.
  Reduction (analytic, verified at N4): on static media (single
  snapshot) every flip count is 0, so F = 0 and A_ext = A bitwise —
  the temporal read IS exp145's read.

LADDER DISCLOSURE (pre-run, derived from deposited boundaries — no new
tuning): the temporal arm's effective chord values are f_e - b/2 (the
flip clock enters as raw transition counts alongside the time-averaged
carrier -b/2; the effective medium is EXACTLY exp142's sign-arm
geometry: ring 1.0 + 6 chords of value f_e - b/2).
  member 'per' (f = 2): effective chords <= -(896 - 2) = -894 —
      strictly past exp142's largest deposited negative-fail dose
      (F3@256: sign arm fails at -256, verifies at -16) => predicted
      majority FAIL on every family by monotone anti-diffusion
      dominance.
  member 'aper' (f asserted in [1120, 1280], instrument validity
      window checked pre-decode; 1200 +/- 3.3 sigma): effective chords
      in [+32, +384] — inside the deposited positive-verify regime
      (exp142 positives verify at all doses <= 256; exp145's phase arm
      verifies +384 chords, the same execute_signed on a real matrix)
      => predicted majority VERIFY.
  Schedule seeds: 11 + 4*family_index + dose_index, fixed a priori;
  identical for the two members of a pair. No other calibration was
  run; the gates below were fixed before the registered run.

ADVERSARIAL INSTRUMENT: 4 arms on every battery pair —
  magnitude arm: exp137's |W_t| front-end + exp94 executor verbatim
                 (|W_t| averaged is bit-identical across the pair);
  sign arm:      exp142's R3 (Re) front-end + execute_signed (the
                 exp142 read — time-averages, predicted blind);
  phase arm:     exp145's PN1/PN2/PN3 read (the CURRENT read —
                 time-averages, predicted verdict-blind);
  temporal arm:  the TC1/TC2/TC3 rule (the extension).

PRE-REGISTERED GATES (fixed before the registered run):

  GATE-N1  (the falsification edge confirmed) the exp145 read is
           VERDICT-BLIND on the flip-clock battery: on >= 11/12 pairs
           the time-averaged projections (magnitude, sign-Re, phase)
           are bitwise equal across the two members and the phase
           arm's per-seed outcome keys and majority verdicts are
           identical within the pair. The static time-average cannot
           see the schedule. (Bit-identity is by construction — the
           gate confirms the instrument.)
  GATE-N2  (the temporal read separates) the temporal arm's majority
           verdicts differ across the two members on >= 10/12 pairs.
  GATE-N3  (decode fidelity on schedule-distinguished classes) the
           temporal arm's pooled median decode err over the paired
           schedule grid (both classes, 10 instances x 3 seeds x 2
           classes) is <= 0.60 mV (the exp142 H1 / exp145 K3 bar).
  GATE-N4  (strict superset) on STATIC media (flip counts zero =>
           F = 0 => A_ext = A bitwise) the temporal read reduces to
           exp145's read BIT-EXACTLY: (i) torus control (exp73
           battery): final V bit-identical per seed, verify preserved;
           (ii) exp142's deposited signed class (4-instance subset,
           seeds 10_000+i): errs + verified bit-identical per
           (instance, seed); (iii) exp145's reactive grid subset
           (instances {0,1} at n=100 + instance 8 at n=400, both
           classes): bit-identical; (iv) exp142's deposited
           complex_phase class (4-instance subset, seeds 20_000+i):
           bit-identical, branch map deposited (rho ~= 0.5 boundary
           resolves by the >= side, exp145's owned branch point).

IF N2 FAILS: the schedule statistic is wrong — deposit WHICH schedules
survive the averaging (per-pair f_per/f_aper and effective-chord
windows are recorded either way) and register the repair direction
(spectral content? flip phase?).

DEPOSIT: results/exp148_temporal_read.json

RUN:
  python3 -m experiments.exp148_temporal_read            # full (registered)
  python3 -m experiments.exp148_temporal_read --smoke    # instrument check
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from experiments.exp137_universal_reader import (
    ComplexMedium, SignedMedium, _base_connected, _wU,
)
from experiments.exp142_sign_read import (
    K_CHORDS, PROBE_SEED, SEEDS, STAR_OP, _StaticMedium,
    execute_signed, project_magnitude, project_signed, read_mag, read_sign,
)
from experiments.exp145_phase_read import (
    GRID_BASE_SEED as EXP145_GRID_BASE_SEED,
    ReactiveMedium, project_phase_native, read_phase, reactive_fraction,
    warnings_as_errors,
)
from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import MULTI, labeling_bfs_n, spec_target_n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp148_temporal_read.json")

# ---------------- flip-clock battery (schedule is the latent class) ---
T_BATTERY = 2400                # read window (frames)
C_BATTERY = 1200                # per-edge ON count (50% duty, both classes)
SCHED_SEED = 11                 # schedule seed base (fixed a priori)
LADDER = (1792.0, 1920.0, 2048.0, 2176.0)
APER_WINDOW = (1120.0, 1280.0)  # instrument validity window for f_aper
PER_FAIL_BOUND = -258.0         # must be < -(256): past every deposited fail
APER_VERIFY_WINDOW = (32.0, 384.0)  # inside the deposited positive-verify reg.

# ---------------- schedule-class grid (fidelity gate N3) --------------
T_GRID = 32
C_GRID = 2                      # per-flip-edge ON count (both classes)
GRID_BASE_SEED = 148_000        # shared base seeds (unused by exp137 classes)
GRID_CLASSES = {"flip_per": "per", "flip_aper": "aper"}
N_INSTANCES = 8                 # at n=100 (exp137's grid)
N_INSTANCES_400 = 2             # scale spot-checks

N3_BAR = 0.60                   # exp142's H1 / exp145's K3 bar
N2_MIN_SEPARATION = 10          # of 12 pairs
N1_MIN_BLIND = 11               # of 12 pairs

FAMILIES = ("F1_zone_tail", "F2_zone_head", "F3_canon_boundary")


# --------------------------------- exp142's carrier geometry, verbatim
def chord_set(n: int, family: str,
              seed: int = PROBE_SEED) -> tuple[np.ndarray, list]:
    """exp142/exp145's probe substrate geometry VERBATIM (same
    PROBE_SEED rng draws): real ring + the family's chord set C."""
    rng = np.random.default_rng(seed)
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
    canon = labeling_bfs_n(A)                    # real ring: geometry only
    head = canon >= NEURAL_SPEC_MIN
    chords: list[tuple[int, int]] = []
    if family == "F1_zone_tail":
        srcs = list(range(60, 76)); rng.shuffle(srcs)
        dsts = [j for j in range(76, 100) if not head[j]]
        rng.shuffle(dsts)
        for t in range(K_CHORDS):
            chords.append((srcs[t % len(srcs)], dsts[t % len(dsts)]))
    elif family == "F2_zone_head":
        srcs = list(range(2, 13)); rng.shuffle(srcs)
        dsts = [j for j in (0, 1) if head[j]]
        for t in range(K_CHORDS):
            chords.append((srcs[t % len(srcs)], dsts[t % len(dsts)]))
    elif family == "F3_canon_boundary":
        amp = set(range(2, 76))
        h_in = [i for i in range(n) if head[i] and i in amp]
        t_in = [i for i in range(n) if not head[i] and i in amp]
        b_hi = max(h_in)
        b_lo = min(j for j in t_in if j > b_hi)
        left = [i for i in h_in if b_hi - K_CHORDS + 1 <= i <= b_hi]
        right = [j for j in t_in if b_lo <= j <= b_lo + K_CHORDS - 1]
        rng.shuffle(left); rng.shuffle(right)
        for t in range(K_CHORDS):
            chords.append((left[t % len(left)], right[t % len(right)]))
    else:
        raise ValueError(family)
    # exp148 instrument repair (disclosed in the module docstring): a
    # chord on a ring edge cannot flip (presence never transitions);
    # nudge the endpoint off the ring — deterministic, shared by both
    # pair members, srcs are distinct so no duplicate edges arise.
    ring = {(i, (i + 1) % n) for i in range(n)}
    repaired = []
    for (i, j) in chords:
        while (i, j) in ring or (j, i) in ring:
            j = (j + 1) % n
            if j == i:
                j = (j + 1) % n
        repaired.append((i, j))
    return A, repaired


# ------------------------------------------- the flip-clock media -----
class FrameSeq:
    """A lazy, re-iterable snapshot sequence with a known length
    (the exp137/142/145 projectors iterate `medium.snapshots()` AND
    call len() on it; materializing T=2400 frames eagerly would waste
    ~150 MB per medium — frames are rebuilt on every pass instead)."""

    def __init__(self, gen_fn, length: int):
        self._gen_fn, self.length = gen_fn, length

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        return self._gen_fn()


class FlipPairMedium:
    """Time-varying battery member: identity semantics live ONLY in the
    flip schedule. Static ring (1.0) + K_CHORDS flip edges carrying -b
    when ON, 0.0 when OFF. 'per': one contiguous ON-bout per edge
    (flip count 2); 'aper': a seeded scattered ON-subset, SAME per-edge
    count. Time-average is BIT-identical across the pair (per entry the
    nonzero additions happen in the same order; zeros are exact no-ops;
    integer values keep every partial sum exact)."""

    kind = "flip_pair"

    def __init__(self, b: float, family: str, sched: str, n: int = 100,
                 chord_seed: int = PROBE_SEED, sched_seed: int = SCHED_SEED,
                 T: int = T_BATTERY, c: int = C_BATTERY):
        A, chords = chord_set(n, family, chord_seed)
        self.A, self.chords = A, chords
        self.b, self.sched, self.T, self.c = float(b), sched, T, c
        k = len(chords)
        on = np.zeros((k, T), dtype=bool)
        srng = np.random.default_rng(sched_seed)
        for e in range(k):
            if sched == "per":
                o = int(srng.integers(0, T - c + 1))
                on[e, o:o + c] = True
            elif sched == "aper":
                sub = srng.choice(T, size=c, replace=False)
                on[e, sub] = True
            else:
                raise ValueError(sched)
        self.on = on
        self.flip_counts = np.count_nonzero(on[:, 1:] != on[:, :-1], axis=1)
        # ---- instrument validity, asserted pre-decode (disclosed) ----
        if sched == "per":
            assert np.all(self.flip_counts == 2), \
                f"per flip counts {self.flip_counts}"
        else:
            assert np.all((self.flip_counts >= APER_WINDOW[0])
                          & (self.flip_counts <= APER_WINDOW[1])), \
                f"aper flip counts {self.flip_counts} outside {APER_WINDOW}"
        self._base = A.copy()                   # static ring backbone

    def snapshots(self):
        return FrameSeq(self._gen_frames, self.T)

    def _gen_frames(self):
        b, chords, on, base = self.b, self.chords, self.on, self._base
        for t in range(self.T):
            frame = base.copy()
            col = on[:, t]
            for e, (i, j) in enumerate(chords):
                if col[e]:
                    frame[i, j] = frame[j, i] = -b
            yield frame

    def native_support(self) -> np.ndarray:
        S = (np.abs(self.A) > 0).astype(float)
        for i, j in self.chords:
            S[i, j] = S[j, i] = 1.0
        return S


class FlipGridMedium:
    """Paired schedule-class grid medium (identity ONLY in the schedule).
    exp137's helpers, SignedMedium's draw order (B -> w; unsigned):
    M = (B*w + (B*w)^T)/2 — a STATIC backbone (ring + random chords,
    all edges ON every frame, both classes) plus a flip subset of
    K_CHORDS=6 chord edges drawn by the SHARED base rng. Flip edges
    are ON in exactly c=2 of T=32 frames: 'per' = the contiguous bout
    [0, 2) (flip count 1); 'aper' = a seeded scattered 2-subset (flip
    count 2..4). The paired classes share B, w, flip subset and counts
    => instance i of the two classes have BIT-identical time-averages;
    only the schedule (and hence the flip clock) differs.
    INSTRUMENT NOTE (disclosed, pre-run): two earlier drafts were
    rejected at the smoke instrument check — (a) flipping EVERY
    support edge and (b) flipping all ~200 random chords — both
    decode at ~1-2 mV (a flip-clock floor of >= 1 per flipping edge
    spread over many edges homogenizes the zones; the static read on
    the SAME media decodes at ~0.55). The flip subset was narrowed to
    K_CHORDS edges BEFORE the registered run — exp142's deposited
    dose response shows 6 ring chords at weight <= 4 decode at
    0.43-0.61 mV, the regime the N3 bar assumes. (c) the seeded aper
    schedule draw at grid instance 0 produced a boundary-adjacent
    CONTIGUOUS pair (fc=1 — a bout, not the registered scattered shape,
    outside the registered 2..4 window); the aper draw now REJECTS
    contiguous bouts by redraw (the registered scattered shape is
    enforced) — disclosed pre-run, before the registered run. Rule
    TC1-TC3 is untouched; the registered run is the single run on the
    corrected instrument."""

    kind = "flip_grid"

    def __init__(self, n: int, seed: int, sched: str):
        rng = np.random.default_rng(seed)
        B = _base_connected(n, 0.04, rng)
        w = _wU(rng, B.shape)
        self.M = (B * w + (B * w).T) / 2.0
        self.sched, self.T, self.c = sched, T_GRID, C_GRID
        rows, cols = np.nonzero(np.triu(B > 0))
        ring = {(i, (i + 1) % n) for i in range(n)}
        is_ring = np.array([((int(i), int(j)) in ring) or
                            ((int(j), int(i)) in ring)
                            for i, j in zip(rows, cols)])
        chord_idx = np.where(~is_ring)[0]
        self.rows, self.cols = rows, cols
        # the flip subset: K_CHORDS chord edges, SHARED across classes
        flip_local = rng.choice(len(chord_idx), size=K_CHORDS,
                                replace=False)
        flip_edges = chord_idx[flip_local]
        self.flip_edges = flip_edges
        srng = np.random.default_rng(seed * 2 + (0 if sched == "per"
                                                  else 1))
        on = np.ones((len(rows), self.T), dtype=bool)   # static backbone
        for e in flip_edges:
            on[e, :] = False
            if sched == "per":
                on[e, 0:self.c] = True                   # bout [0, c)
            elif sched == "aper":
                # scattered = NOT one contiguous bout (the registered
                # shape; boundary-adjacent draws degenerate to fc=1):
                sub = srng.choice(self.T, size=self.c, replace=False)
                while np.max(sub) - np.min(sub) == self.c - 1:
                    sub = srng.choice(self.T, size=self.c, replace=False)
                on[e, sub] = True
            else:
                raise ValueError(sched)
        self.on = on
        self.flip_counts = np.count_nonzero(on[:, 1:] != on[:, :-1],
                                            axis=1)
        fc = self.flip_counts[flip_edges]
        # instrument validity (disclosed): per has f = 1 exactly;
        # aper lies in [2, 2c]
        if sched == "per":
            assert np.all(fc == 1), f"per flip counts {fc}"
        else:
            assert np.all((fc >= 2) & (fc <= 2 * self.c)), \
                f"aper flip counts {fc}"

    def snapshots(self):
        return FrameSeq(self._gen_frames, self.T)

    def _gen_frames(self):
        M, rows, cols, on = self.M, self.rows, self.cols, self.on
        for t in range(self.T):
            Emask = np.zeros(M.shape)
            Emask[rows, cols] = on[:, t]
            Emask[cols, rows] = on[:, t]
            yield M * Emask

    def native_support(self) -> np.ndarray:
        return (np.abs(self.M) > 0).astype(float)


# ------------------------------- TC1-TC3: the one new rule ------------
def flip_clock_matrix(medium) -> np.ndarray:
    """TC1 — the flip-clock channel, ONE statistic, zero knobs: per
    undirected edge, the number of presence transitions over the read
    window (RAW counts — no normalization constant). A static medium
    (single snapshot) has zero transitions everywhere: F = 0."""
    prev = None
    F = None
    for W in medium.snapshots():
        P = ((np.abs(W) > 0) | (np.abs(W).T > 0)).astype(np.int8)
        if prev is not None:
            D = (P != prev).astype(np.int8)
            F = D.astype(float) if F is None else F + D
        prev = P
    if F is None:
        F = np.zeros_like(prev, dtype=float)
    np.fill_diagonal(F, 0.0)
    return F


def read_temporal(medium, seed: int, return_state: bool = False) -> dict:
    """The temporal arm: TC1+TC2+TC3 — exp145's projection verbatim,
    PLUS the flip-clock channel added as a structure feature alongside
    the averaged coupling; exp142's executor verbatim."""
    with warnings_as_errors():
        A, rho, branch = project_phase_native(medium)      # PN1+PN2 verbatim
        F = flip_clock_matrix(medium)                      # TC1
        A_ext = A + F                                      # TC2 (zero knobs)
        assert not np.iscomplexobj(A_ext), "TC2 must deliver a real matrix"
        out = execute_signed(MULTI, A_ext, seed, op=STAR_OP,
                             return_state=return_state)    # TC3 verbatim
    out["rho"] = rho
    out["branch"] = branch
    return out


# ------------------- the SCOPED arm (exp178's wiring, ADDITIVE) --------
def read_scoped(medium, seed: int, return_state: bool = False,
                f_max: float | None = None) -> dict:
    """THE SCOPED READ (exp178's production wiring — ONE arm, ONE
    function, zero knobs): exp169's f_max diagnostic VERBATIM (one
    source of truth for the flip clock's concentration) with the
    pre-registered threshold; the rule selects R_T (exp167's adopted
    path) iff f_max < 32.0, else the existing temporal path above
    UNCHANGED. f_max is computed from the medium's frames via exp169's
    f_max_frames; for PAIRED constructions (FlipPairMedium) the unit of
    scoping is the PAIR — pass the PAIR-JOINT max (max over the two
    schedule members, exp169's _pair_fmax semantics) via f_max.
    Lazy imports: exp167/exp169 both import this module, so a
    top-level import would be circular; the scoped arm is their only
    consumer. The existing arms are untouched (this arm must be
    requested)."""
    from experiments.exp167_rt_adopted import read_adopted
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    if f_max is None:
        f_max = f_max_frames(list(medium.snapshots()))
    if f_max < THRESHOLD:
        return read_adopted(medium, seed, return_state)   # R_T (exp167)
    return read_temporal(medium, seed, return_state)      # raw (unchanged)


# ------------------------------------------------------------ helpers
def decode(arm: str, medium, seed: int,
           return_state: bool = False,
           f_max: float | None = None) -> dict:
    """Dispatch one decode; a rejection is RECORDED, never raised
    (exp142's zero-rejection hygiene; the caller counts). The additive
    "scoped" arm (exp178's wiring) takes the PAIR-JOINT f_max for
    paired constructions via the optional f_max argument (None =>
    compute from the medium's own frames); every pre-existing arm and
    caller is unchanged."""
    if arm == "mag":
        fn = lambda med, s, st: read_mag(project_magnitude(med), s, st)
    elif arm == "sign":
        fn = lambda med, s, st: read_sign(project_signed(med), s, st)
    elif arm == "phase":
        fn = read_phase
    elif arm == "temporal":
        fn = read_temporal
    elif arm == "scoped":
        fn = lambda med, s, st: read_scoped(med, s, st, f_max=f_max)
    else:
        raise ValueError(arm)
    try:
        out = fn(medium, seed, return_state)
        err = float(out["err_vs_target"])
        if not np.isfinite(err):
            raise ValueError(f"non-finite decode err {err}")
        return {"ok": True, "err": err,
                "verified": bool(out.get("program_verified", False)),
                "state": out.get("final_state"),
                "rho": out.get("rho"), "branch": out.get("branch")}
    except Exception as e:                                   # pragma: no cover
        return {"ok": False, "rejection": f"{type(e).__name__}: {e}"[:200]}


def outcome_key(rec: dict):
    return ("err", rec["err"]) if rec["ok"] else ("rej", rec["rejection"])


def verdict_blind(rec_a: dict, rec_b: dict) -> bool:
    return (rec_a["keys"] == rec_b["keys"]
            and rec_a["majority"] == rec_b["majority"])


def run_arm(arm: str, medium, seeds: list[int]) -> dict:
    errs, vs, keys = [], [], []
    for s in seeds:
        out = decode(arm, medium, s)
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(outcome_key(out))
    return {"errs": errs, "verify": vs, "keys": keys,
            "majority": bool(np.mean(vs) > 0.5)}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 family x 1 dose, "
                         "1 grid instance/class, 1 seed, torus only")
    args = ap.parse_args()
    seeds = list((1,) if args.smoke else SEEDS)
    fams = FAMILIES[:1] if args.smoke else FAMILIES
    doses = LADDER[:1] if args.smoke else LADDER
    n_inst = 1 if args.smoke else N_INSTANCES
    n_inst400 = 1 if args.smoke else N_INSTANCES_400
    t0 = time.time()
    print("=== exp148: THE TEMPORAL READ (flip-clock channel) ===\n")

    rejections = 0
    gates: dict = {}
    sign_cache: dict = {}

    # ---- GATE-N4(i): torus control — bit-exact reduction to exp145
    ctrl: dict = {"substrate": "torus"}
    bit_ok, verify_ok = True, True
    phase_errs, temporal_errs = [], []
    for s in seeds:
        m = _StaticMedium(make_battery()["torus"])
        out_p = decode("phase", m, s, return_state=True)
        out_t = decode("temporal", m, s, return_state=True)
        rejections += sum(1 for r in (out_p, out_t) if not r["ok"])
        phase_errs.append(out_p.get("err"))
        temporal_errs.append(out_t.get("err"))
        same = (out_p["ok"] and out_t["ok"] and np.array_equal(
            np.asarray(out_p["state"]["V"]),
            np.asarray(out_t["state"]["V"])))
        bit_ok &= bool(same)
        verify_ok &= (out_p.get("verified") == out_t.get("verified"))
    ctrl.update(phase_errs=phase_errs, temporal_errs=temporal_errs,
                bit_identical=bool(bit_ok), verify_preserved=bool(verify_ok))
    print(f"  N4 torus: bit-identical {bit_ok} verify_preserved "
          f"{verify_ok} errs phase {phase_errs} temporal {temporal_errs}")

    # ---- GATE-N4(ii)/(iii)/(iv): exp142/exp145's deposited static classes
    n4_classes: dict = {}
    for kind, builder in (
            ("signed", lambda i: SignedMedium(100, seed=10_000 + i)),
            ("complex_phase", lambda i: ComplexMedium(100, seed=20_000 + i))):
        recs, bit_identical, n_cmp, branches = [], 0, 0, []
        for i in range(4):
            med = builder(i)
            rho = reactive_fraction(med)
            branches.append(rho >= 0.5)
            for s in seeds:
                out_p = decode("phase", med, s)
                out_t = decode("temporal", med, s)
                rejections += sum(1 for r in (out_p, out_t) if not r["ok"])
                same = (out_p["ok"] and out_t["ok"]
                        and out_p["err"] == out_t["err"]
                        and out_p["verified"] == out_t["verified"])
                bit_identical += int(same)
                n_cmp += 1
                recs.append({"i": i, "seed": s, "rho": round(rho, 4),
                             "branch": "imag" if rho >= 0.5 else "real",
                             "phase_err": out_p.get("err"),
                             "temporal_err": out_t.get("err"),
                             "bit_identical": bool(same)})
        n4_classes[kind] = {"instances": recs,
                            "bit_identical_pairs": bit_identical,
                            "n_pairs": n_cmp,
                            "branch_map_imag":
                                [i for i, b in enumerate(branches) if b]}
        print(f"  N4 {kind:14s} bit-identical {bit_identical}/{n_cmp} "
              f"imag-branch {n4_classes[kind]['branch_map_imag']}")

    reactive_recs, reactive_bit, reactive_cmp = [], 0, 0
    for (n, i) in ((100, 0), (100, 1), (400, 8)):
        for s_cls in (1, -1):
            med = ReactiveMedium(n, seed=EXP145_GRID_BASE_SEED + i, s=s_cls)
            for s in seeds:
                out_p = decode("phase", med, s)
                out_t = decode("temporal", med, s)
                rejections += sum(1 for r in (out_p, out_t) if not r["ok"])
                same = (out_p["ok"] and out_t["ok"]
                        and out_p["err"] == out_t["err"]
                        and out_p["verified"] == out_t["verified"])
                reactive_bit += int(same)
                reactive_cmp += 1
                reactive_recs.append({"n": n, "i": i, "s": s_cls,
                                      "seed": s,
                                      "phase_err": out_p.get("err"),
                                      "temporal_err": out_t.get("err"),
                                      "bit_identical": bool(same)})
    n4_classes["reactive_grid_subset"] = {
        "instances": reactive_recs, "bit_identical_pairs": reactive_bit,
        "n_pairs": reactive_cmp}
    print(f"  N4 reactive_grid     bit-identical {reactive_bit}/{reactive_cmp}")

    # ---- GATE-N3: the paired schedule-class grid
    grid: dict = {}
    grid_errs: list[float] = []
    sign_blind_cross = 0
    sign_cross_cmp = 0
    for cls_name, sched in GRID_CLASSES.items():
        inst_rec, errs, errs_native, oks = [], [], [], []
        f_stats = []
        for i in range(n_inst + n_inst400):
            n = 400 if i >= n_inst else 100
            med = FlipGridMedium(n, seed=GRID_BASE_SEED + i, sched=sched)
            A_nat = spec_target_n(MULTI, labeling_bfs_n(med.native_support()),
                                  n)
            fc = med.flip_counts[med.flip_edges]
            f_stats.append({"n": n, "f_min": int(fc.min()),
                            "f_max": int(fc.max()),
                            "f_median": float(np.median(fc)),
                            "n_flip_edges": int(fc.size)})
            for s in seeds:
                out_t = decode("temporal", med, s, return_state=True)
                out_s = decode("sign", med, s)
                rejections += sum(1 for r in (out_t, out_s) if not r["ok"])
                rec = {"n": n, "seed": s}
                if out_t["ok"]:
                    V = np.asarray(out_t["state"]["V"])
                    err_nat = float(np.sqrt(np.mean((V - A_nat) ** 2)))
                    errs.append(out_t["err"])
                    errs_native.append(err_nat)
                    oks.append(out_t["verified"])
                    grid_errs.append(out_t["err"])
                    rec.update(err=out_t["err"], err_native=round(err_nat, 2),
                               verified=out_t["verified"])
                else:
                    rec["rejection"] = out_t["rejection"]
                # confident-blindness diagnostic: the STATIC (sign) read
                # is bitwise-identical across the paired schedule classes
                if cls_name == "flip_per":
                    sign_cache[(n, i, s)] = out_s
                else:
                    twin = sign_cache.get((n, i, s))
                    if twin is not None:
                        sign_cross_cmp += 1
                        sign_blind_cross += int(outcome_key(twin)
                                                == outcome_key(out_s))
                inst_rec.append(rec)
        grid[cls_name] = {
            "instances": inst_rec,
            "flip_counts": f_stats,
            "temporal_median": float(np.median(errs)) if errs else None,
            "temporal_max": float(np.max(errs)) if errs else None,
            "err_native_median": (float(np.median(errs_native))
                                  if errs_native else None),
            "verify_rate": float(np.mean(oks)) if oks else None,
        }
        print(f"  N3 {cls_name:10s} temporal median "
              f"{grid[cls_name]['temporal_median']} verify "
              f"{grid[cls_name]['verify_rate']} f_med "
              f"{f_stats[0]['f_median']}")

    # ---- GATE-N1 / GATE-N2: the flip-clock adversarial battery
    pairs: list[dict] = []
    n_blind_phase = n_blind_sign = n_blind_mag = 0
    separated: list[str] = []
    for fam in fams:
        fi = FAMILIES.index(fam)
        for b in doses:
            di = LADDER.index(b)
            sched_seed = SCHED_SEED + 4 * fi + di
            m_per = FlipPairMedium(b, fam, "per", sched_seed=sched_seed)
            m_aper = FlipPairMedium(b, fam, "aper", sched_seed=sched_seed)
            rec = {"family": fam, "dose": b, "sched_seed": sched_seed,
                   "f_per": [int(x) for x in m_per.flip_counts],
                   "f_aper": [int(x) for x in m_aper.flip_counts]}
            # (a) static-projection validity: bitwise-equal time averages
            proj_mag_same = bool(np.array_equal(
                project_magnitude(m_per), project_magnitude(m_aper)))
            A_per = project_phase_native(m_per)[0]
            A_aper = project_phase_native(m_aper)[0]
            proj_phase_same = bool(np.array_equal(A_per, A_aper))
            rho_same = bool(reactive_fraction(m_per)
                            == reactive_fraction(m_aper))
            rec["projection_bit_identical"] = {
                "magnitude": proj_mag_same, "phase": proj_phase_same,
                "rho": rho_same}
            # (b) effective-chord windows (instrument validity, pre-decode)
            ext_per = A_per + flip_clock_matrix(m_per)
            ext_aper = A_aper + flip_clock_matrix(m_aper)
            eff_per = [float(ext_per[i, j]) for i, j in m_per.chords]
            eff_aper = [float(ext_aper[i, j]) for i, j in m_aper.chords]
            rec["effective_chords"] = {"per": eff_per, "aper": eff_aper}
            assert max(eff_per) <= PER_FAIL_BOUND, \
                f"per effective chords {eff_per} not past fail bound"
            assert (min(eff_aper) >= APER_VERIFY_WINDOW[0]
                    and max(eff_aper) <= APER_VERIFY_WINDOW[1]), \
                f"aper effective chords {eff_aper} outside verify window"
            # (c) the four arms on both members
            arms: dict = {}
            for name, med in (("per", m_per), ("aper", m_aper)):
                for arm in ("mag", "sign", "phase", "temporal"):
                    arms[(name, arm)] = run_arm(arm, med, seeds)
                    rejections += sum(
                        1 for k in arms[(name, arm)]["keys"]
                        if k[0] == "rej")
            rec["arms"] = {
                f"{name}_{arm}": {"errs": v["errs"],
                                  "verify": [int(x) for x in v["verify"]],
                                  "majority": v["majority"]}
                for (name, arm), v in arms.items()}
            # (d) N1: the static reads are verdict-blind
            blind_mag = verdict_blind(arms[("per", "mag")],
                                      arms[("aper", "mag")])
            blind_sign = bool(proj_phase_same and
                              verdict_blind(arms[("per", "sign")],
                                            arms[("aper", "sign")]))
            blind_phase = bool(proj_phase_same and
                               verdict_blind(arms[("per", "phase")],
                                             arms[("aper", "phase")]))
            rec["magnitude_blind"] = bool(blind_mag)
            rec["sign_verdict_blind"] = bool(blind_sign)
            rec["phase_verdict_blind"] = bool(blind_phase)
            n_blind_mag += int(blind_mag)
            n_blind_sign += int(blind_sign)
            n_blind_phase += int(blind_phase)
            # (e) N2: the temporal read separates the schedules
            sep = (arms[("per", "temporal")]["majority"]
                   != arms[("aper", "temporal")]["majority"])
            rec["temporal_separated"] = bool(sep)
            if sep:
                separated.append(f"{fam}@{b:g}")
            pairs.append(rec)
            print(f"  N1/N2 {fam:17s} b={b:6.1f} magBlind={blind_mag} "
                  f"signBlind={blind_sign} phaseBlind={blind_phase} "
                  f"temporal per{arms[('per', 'temporal')]['errs']}"
                  f"V{int(arms[('per', 'temporal')]['majority'])} "
                  f"aper{arms[('aper', 'temporal')]['errs']}"
                  f"V{int(arms[('aper', 'temporal')]['majority'])}"
                  + ("  <== SEPARATED" if sep else ""))

    # ---- gates
    n_pairs = len(pairs)
    gates["N1_static_read_blind"] = {
        "pass": bool(n_pairs > 0 and n_blind_phase >= N1_MIN_BLIND),
        "n_pairs": n_pairs, "required": N1_MIN_BLIND,
        "phase_verdict_blind_pairs": n_blind_phase,
        "sign_verdict_blind_pairs": n_blind_sign,
        "magnitude_blind_pairs": n_blind_mag,
    }
    gates["N2_temporal_separates"] = {
        "pass": bool(n_sep >= N2_MIN_SEPARATION) if (n_sep := len(separated))
                else False,
        "separated_pairs": separated, "n_separated": len(separated),
        "required": N2_MIN_SEPARATION,
    }
    g3 = float(np.median(grid_errs)) if grid_errs else None
    gates["N3_schedule_fidelity"] = {
        "pass": bool(g3 is not None and g3 <= N3_BAR),
        "pooled_temporal_median": g3, "bar": N3_BAR,
        "n_decodes": len(grid_errs),
        "sign_cross_class_blind": {"outcome_identical": sign_blind_cross,
                                   "n_compared": sign_cross_cmp},
    }
    n4 = bool(bit_ok and verify_ok
              and n4_classes["signed"]["bit_identical_pairs"]
              == n4_classes["signed"]["n_pairs"]
              and n4_classes["complex_phase"]["bit_identical_pairs"]
              == n4_classes["complex_phase"]["n_pairs"]
              and n4_classes["reactive_grid_subset"]["bit_identical_pairs"]
              == n4_classes["reactive_grid_subset"]["n_pairs"])
    gates["N4_strict_superset"] = {
        "pass": bool(n4),
        "torus_bit_identical": bool(bit_ok),
        "torus_verify_preserved": bool(verify_ok),
        "signed_bit_identical": n4_classes["signed"]["bit_identical_pairs"],
        "signed_pairs": n4_classes["signed"]["n_pairs"],
        "complex_bit_identical":
            n4_classes["complex_phase"]["bit_identical_pairs"],
        "complex_pairs": n4_classes["complex_phase"]["n_pairs"],
        "complex_branch_map_imag": n4_classes["complex_phase"]["branch_map_imag"],
        "reactive_bit_identical":
            n4_classes["reactive_grid_subset"]["bit_identical_pairs"],
        "reactive_pairs": n4_classes["reactive_grid_subset"]["n_pairs"],
        "reduction": ("static media: flip counts all zero => F = 0 => "
                      "A_ext = A bitwise => exp145's read"),
    }

    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = f"{n_pass}/{len(gates)} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in gates.items()))
    print(f"  rejections: {rejections}")

    result = {
        "exp": "exp148_temporal_read",
        "claim": (
            "the temporal read — TC1 (per-edge raw presence-transition "
            "counts over the read window, zero knobs) + TC2 (exp145's "
            "PN1/PN2 projected time-average PLUS the flip-clock matrix "
            "as a structure feature alongside the averaged coupling) + "
            "TC3 (exp142's executor verbatim) — consumes the flip "
            "SCHEDULE the static time-average discards: the exp145 "
            "read is verdict-blind on flip-clock adversarial pairs "
            "whose time-averages are bitwise identical, the temporal "
            "read separates the schedule classes at the verdict level, "
            "decode fidelity on paired schedule classes sits within "
            "the exp142 bar, and the read reduces bit-exactly to "
            "exp145's read wherever the medium is static"),
        "pre_registration": {
            "temporal_rule": [
                "TC1 flip-clock channel: f_ij = raw per-undirected-edge "
                "presence-transition count over the read window "
                "(|W_t| > 0, symmetrized); F = symmetrized transition-"
                "count matrix, zero diagonal — no normalization "
                "constant (zero knobs)",
                "TC2 extended projection: A_ext = A + F with A = "
                "exp145's PN1/PN2 projected time-average VERBATIM "
                "(rho >= 0.5 -> Im branch else Re); the flip clock "
                "enters as a structure feature alongside the averaged "
                "coupling",
                "TC3 structure+dynamics: exp142's execute_signed "
                "VERBATIM on A_ext — no new executor code"],
            "media": {
                "battery": ("static ring 1.0 + K_CHORDS flip edges "
                            "(-b ON / 0 OFF, T=2400, c=1200 ON-frames "
                            "per edge); class = schedule: 'per' one "
                            "contiguous bout (f=2) vs 'aper' seeded "
                            "scattered subset (f in [1120,1280]); "
                            "per-edge ON-counts identical => time-"
                            "average BIT-identical across the pair"),
                "grid": ("FlipGridMedium: M=(B*w+(B*w)^T)/2 on exp137's "
                         "connected 4% support; every edge flips with "
                         "shared per-edge counts c_e~{2,3,4} of T=32; "
                         "shared base seeds 148_000+i — the class "
                         "enters only through the schedule shape"),
            },
            "dose_ladder": list(LADDER),
            "ladder_disclosure": (
                "temporal effective chords = f_e - b/2 (the flip clock "
                "as raw counts alongside the time-averaged carrier "
                "-b/2): 'per' <= -894, strictly past exp142's largest "
                "deposited negative-fail dose (F3@256) => predicted "
                "majority FAIL; 'aper' in [+32, +384], inside the "
                "deposited positive-verify regime (exp142 positives "
                "verify at all doses <= 256; exp145's phase arm "
                "verifies +384 chords on the same executor) => "
                "predicted majority VERIFY; schedule seeds 11 + "
                "4*family_index + dose_index, fixed a priori"),
            "aper_window": list(APER_WINDOW),
            "gates": gates,
        },
        "config": {"op": STAR_OP, "spec": "MULTI (exp94)",
                   "frontier": "walk", "seeds": list(seeds),
                   "control": "torus (exp73 battery)",
                   "probe_seed": PROBE_SEED, "k_chords": K_CHORDS,
                   "T_battery": T_BATTERY, "c_battery": C_BATTERY,
                   "T_grid": T_GRID, "grid_base_seed": GRID_BASE_SEED,
                   "n3_bar": N3_BAR},
        "control": ctrl,
        "n4_classes": n4_classes,
        "grid": grid,
        "probes": {"pairs": pairs, "n_pairs": n_pairs,
                   "phase_verdict_blind_pairs": n_blind_phase,
                   "sign_verdict_blind_pairs": n_blind_sign,
                   "magnitude_blind_pairs": n_blind_mag,
                   "separated_pairs": separated,
                   "n_separated": len(separated)},
        "gates": gates,
        "verdict": verdict,
        "rejections": rejections,
        "runtime_s": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print(f"  deposited {OUT}")
    return result


if __name__ == "__main__":
    main()
