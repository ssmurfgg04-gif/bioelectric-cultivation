"""exp166 — THE LEADING EDGE: hyper x oriented x temporal corner pricing.

exp160's registered follow-up (L138, U3/GATE-U3 deposit): the universality
boundary's tail lives in the oriented+hyper+temporal corner — 5/200 above
the 1.30 mV bar, medians 1.31-1.65 mV, all still verifying, dominant driver
hyper at the dimension level, "A-PAIR pairwise factorization meeting one-way
orientation under flipping presence" the NAMED leading edge. THIS experiment
prices that corner with a focused crossed factorial and hands back ONE
pre-registered repair candidate.

========================= PRE-REGISTRATION =========================
Deposited BEFORE any decode (this file is committed before the credited
run; gates, seeds, and the repair-rule mapping below are fixed now).

GENERATOR (exp160 verbatim, corner-pinned):
  * RandomMedium machinery copied verbatim from exp160_any_medium.py:
    n = 100; support = exp137's _base_connected (ring + chords p=0.04);
    magnitudes = exp137's _wU = U(0.5, 1.5) (exp160's deposited range);
    oriented = per-edge one-way prob 0.5; hyper = 1-20 added hyperedges
    size 3-6, phase-carrying factorization w_e/(|e|-1); temporal = T=8
    frames, per-edge presence p_keep ~ U(0.6, 0.95), ring backbone always
    on, per-frame hyper presence schedule; all draws from ONE stream
    np.random.default_rng(seed) in exp160's exact branch order.
  * The five DIM_P coins are REPLACED by the factorial cell spec: the
    focal dims {oriented, hyper, temporal} are set by the cell; signed
    (A-NN) and complex (A-REAL) are PINNED INACTIVE in all 400 instances
    — exp160's U3 decomposition found them neutral-to-protective
    (lift 0.74 / 0.67), so pinning them out isolates the focal factorial;
    the corner cell (o+h+t) remains inside exp160's named tail class
    ("A-SYM+A-PAIR+A-STAT and supersets"). Consequence deposited here:
    all frames and hyperedge weights in this battery are real >= 0.

SEEDS (deposited first):
  * Master seed SEED_BASE = 166166. Cell index c = 4*o + 2*h + t with
    bits (o, h, t) = (oriented, hyper, temporal) in {0, 1}. Instance j of
    cell c draws np.random.default_rng(SEED_BASE + 1000*c + j),
    j = 0..49. 8 cells x 50 instances = 400 media, 400 distinct streams.

READ (exp160's stack VERBATIM, ONE configuration, zero per-instance
tuning): read_temporal(medium, seed) for seeds (1, 2, 3) = 1200 decodes —
  PN1 reactive_fraction + PN2 dominant-quadrature (per-frame symmetrize
  S = (R + R.T)/2, exp145 verbatim) + TC1 flip-clock F + TC2 A_ext = A + F
  -> exp142 execute_signed VERBATIM on exp94's MULTI spec. The READ_CONFIG
  dict below is exp160's dict VERBATIM; its fingerprint is asserted equal
  to exp160's deposited 8e11e88c1c2f1518.

GATES (pre-registered; metrics defined now):
  P1 FACTORIAL DECOMPOSITION: per-cell median = median over the cell's 50
     per-instance median-of-3-seed errs. Effect table from the 8 CELL
     MEDIANS, standard 2^3 Yates contrasts on the (1/4)-scale:
     effect_X = (1/4) * sum_cells (-1)^(1 + parity_X(cell)) * m_cell
     (positive = active side degrades) for the three mains, three pairwise
     interactions, and the triple; dominant = argmax over the mains.
     PASS = all 8 cells populated (n = 50) with finite medians AND the
     dominant main effect named AND the full 7-row table deposited.
  P2 MONOTONE DEGRADATION ALONG THE ACTIVE-COUNT AXIS (REGISTERED
     EXPECTATION): grouped-by-k median (mean of the 8/k cell medians
     within k = number of active focal dims, k = 0..3) strictly
     increasing k0 < k1 < k2 < k3 AND the corner cell (k = 3) is the max
     cell median. IF VIOLATED the ACTUAL ordering is deposited as the
     finding (gate records the miss; the ordering itself is the result).
  P3 ZERO REJECTIONS: 400/400 instances, 1200/1200 decodes finite, zero
     exceptions / coercion warnings (exp160's rejection policy); verify
     rate reported; verify 1.00 OR the above-bar tail (exp160's bar
     1.30 mV) characterized per cell in the deposit.
  P4 PRE-REGISTERED REPAIR CANDIDATE — the rule is CHOSEN by the P1
     dominant effect through this mapping, fixed BEFORE the run:
       dominant = hyper    -> R_H "cancellation-density-weighted S"
            (L142's deposit): S_ij = 1 iff i,j share a hyperedge;
            F = median nonzero |W_ij| pooled over ALL frames of the 20
            spot instances computed BEFORE any arm-B decode (L142's
            zero-knob F = median nonzero |A| recipe, taken at the medium
            level); every frame W_t <- W_t + F*S (constant real
            augmentation — TC2's A_ext = A + F moved to the medium).
       dominant = temporal -> R_T "flip-quiet windowing" (L140's
            discipline at the medium level): every frame masked to the
            across-frame CORE support (edges present in EVERY frame);
            membership frozen, zero presence transitions, zero knobs.
       dominant = oriented -> R_O "one-way support restore (symmetrize)":
            in every frame a pair with exactly one direction present gets
            the surviving value copied to the absent direction. Code
            audit pre-registered: the stack ALREADY symmetrizes per frame
            (PN2 S = (R + R.T)/2), so if oriented is named the honest
            statement is "symmetrize already handles" WITH the R_O spot
            check as evidence.
     Each rule is a NO-OP on the clean cell (o = h = t = 0): R_H S = 0,
     R_T core = full single-frame support, R_O no one-way pairs — so the
     clean-cell no-regression check is BIT-EXACTNESS (registered).
     SPOT BATTERY: 20 instances = corner cell (c = 7, j = 0..9) + clean
     cell (c = 0, j = 0..9), seeds (1, 2, 3); arm A = exp160 stack
     verbatim on the raw medium (MUST reproduce the main battery's stored
     errs BIT-EXACTLY — replay integrity); arm B = same stack on the
     repaired wrapper (read core untouched — the rule lives entirely in
     the frames the wrapper yields).
     P4 PASS = (a) replay bit-exact 20/20, (b) clean cell arm B
     bit-identical to arm A (zero regression by construction), (c) corner
     cell median improves under arm B.
NO post-hoc knob tuning anywhere; exactly ONE rule is adopted (the mapped
one). Whatever the outcome, it is deposited.
=====================================================================

Deposits: results/exp166_leading_edge.json; ledger L143 (next free after
L142); wall budget 12 min.
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp137_universal_reader import _base_connected, _wU
from experiments.exp142_sign_read import execute_signed
from experiments.exp148_temporal_read import read_temporal
from experiments.exp94_multizone_scale import MULTI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp166_leading_edge.json")

# ------------------------------------------------- frozen protocol
SEED_BASE = 166166                # master generator seed (deposited first)
N_CELLS = 8                       # 2^3 crossed factorial
N_PER_CELL = 50                   # 400 instances total
N = 100
SEEDS = (1, 2, 3)                 # exp137/exp160 seed protocol, unchanged
T_FRAMES = 8                      # temporal depth when the dim is active
FOCAL = ("oriented", "hyper", "temporal")
PINNED_OFF = ("signed", "complex")   # exp160 U3: neutral-to-protective
DIMENSIONS = ("oriented", "signed", "complex", "hyper", "temporal")
VIOLATION = {"oriented": "A-SYM", "signed": "A-NN", "complex": "A-REAL",
             "hyper": "A-PAIR", "temporal": "A-STAT"}

BAR = 1.30                        # exp160's deposited bar (mV)
OOD_ANCHOR = 0.65                 # exp137's deposited OOD pooled median
EXP160_FP = "8e11e88c1c2f1518"    # exp160's deposited config fingerprint

SPOT_CORNER_J = list(range(10))   # corner-cell instances for the spot battery
SPOT_CLEAN_J = list(range(10))    # clean-cell instances for the spot battery

READ_CONFIG = {
    "projection": ("exp148 read_temporal VERBATIM (PN1/PN2 dominant-quadrature"
                   " + TC1 flip-clock F + TC2 A_ext = A + F)"),
    "executor": ("exp142 execute_signed VERBATIM (R1 structure on |A|, R2"
                 " signed dynamics, walk frontier on |A|>0)"),
    "op": {"gamma": 64.0, "mu": 0.0},
    "op_source": "exp99 battery-wide STAR point (exp142's STAR_OP)",
    "spec": "MULTI (exp94 3-zone program)",
    "frontier": "walk (inside exp142's executor)",
    "seeds": [1, 2, 3],
    "n": 100,
    "window_h": 24.0,
    "commit_noise": 0.6,
    "steps_per_cell": 8,
    "per_instance_tuning": "none",
}


def config_fingerprint() -> str:
    return hashlib.sha256(
        json.dumps(READ_CONFIG, sort_keys=True).encode()).hexdigest()[:16]


def cell_index(o: int, h: int, t: int) -> int:
    return 4 * o + 2 * h + t


def cell_dims(c: int) -> dict:
    o, h, t = (c >> 2) & 1, (c >> 1) & 1, c & 1
    return {"oriented": bool(o), "signed": False, "complex": False,
            "hyper": bool(h), "temporal": bool(t)}


# ------------------------------------------------- the corner medium
# exp160's RandomMedium verbatim with the five DIM_P coins replaced by the
# cell spec (focal dims set; signed/complex pinned inactive). Branch order
# and draw order are exp160's exactly; only active dims draw.
class CornerMedium:
    """One corner-battery draw: exp160's generator machinery with the
    dimension coins dictated by the crossed factorial cell. All random
    choices happen in __init__ from ONE rng stream
    (np.random.default_rng(seed)); snapshots() is a deterministic
    re-iterable with no rng at read time."""

    kind = "random_corner_union"

    def __init__(self, n: int, seed: int, dims: dict):
        rng = np.random.default_rng(seed)
        self.seed = seed
        self.n = n
        self.dims = {d: bool(dims[d]) for d in DIMENSIONS}

        B = _base_connected(n, 0.04, rng)               # 0/1 support
        w = _wU(rng, B.shape) * B                       # magnitudes
        iu = np.triu_indices(n, 1)
        e_on = B[iu] > 0

        # --- oriented (A-SYM): per-edge one-way with prob 0.5
        self.n_oneway = 0
        W = w.copy()
        if self.dims["oriented"]:
            one_way = e_on & (rng.random(len(iu[0])) < 0.5)
            fwd = rng.random(len(iu[0])) < 0.5
            kill_up = np.zeros(B.shape, bool)
            kill_up[iu] = one_way & fwd                 # keep only (j,i)
            kill_lo = np.zeros(B.shape, bool)
            kill_lo[iu] = one_way & (~fwd)              # keep only (i,j)
            W = W * (~kill_up) * (~kill_lo)
            self.n_oneway = int(one_way.sum())

        # --- signed (A-NN): symmetric per-edge sign (PINNED INACTIVE here)
        self.p_neg = 0.0
        self.n_neg = 0
        sign = np.ones(B.shape)
        if self.dims["signed"]:
            self.p_neg = float(rng.uniform(0.1, 0.5))
            neg = e_on & (rng.random(len(iu[0])) < self.p_neg)
            smask = np.zeros(B.shape)
            smask[iu] = neg
            smask = smask + smask.T
            sign = 1.0 - 2.0 * smask
            self.n_neg = int(neg.sum())

        # --- complex (A-REAL): symmetric per-edge phase (PINNED INACTIVE)
        self.phase_frac = 0.0
        self.n_phased = 0
        phase = np.zeros(B.shape)
        if self.dims["complex"]:
            self.phase_frac = float(rng.uniform(0.2, 1.0))
            ph = e_on & (rng.random(len(iu[0])) < self.phase_frac)
            pmask = np.zeros(B.shape)
            pmask[iu] = ph
            pmask = pmask + pmask.T
            theta = rng.uniform(0.0, 2.0 * np.pi, size=B.shape)
            phase = np.where(pmask > 0, theta, 0.0)
            self.n_phased = int(ph.sum())

        self.Wbase = W * sign * np.exp(1j * phase)

        # --- hyper (A-PAIR): added hyperedges, same sign/phase mechanism
        self.hyperedges: list[tuple[list[int], complex]] = []
        if self.dims["hyper"]:
            for _ in range(int(rng.integers(1, 21))):
                size = int(rng.integers(3, 7))
                members = sorted(rng.choice(n, size=size, replace=False)
                                 .tolist())
                m = _wU(rng, ())
                s = -1.0 if (self.dims["signed"]
                             and rng.random() < self.p_neg) else 1.0
                th = rng.uniform(0.0, 2.0 * np.pi) if self.dims["complex"] \
                    else 0.0
                self.hyperedges.append((members, s * m * np.exp(1j * th)))
        self.n_hyper = len(self.hyperedges)

        # --- temporal (A-STAT): per-frame presence schedules (drawn HERE,
        #     once; snapshots() replays them without rng)
        self.T_eff = T_FRAMES if self.dims["temporal"] else 1
        self.p_keep = float(rng.uniform(0.6, 0.95)) \
            if self.dims["temporal"] else 1.0
        ring = np.zeros(B.shape, bool)
        for i in range(n):
            ring[i, (i + 1) % n] = ring[(i + 1) % n, i] = True
        if self.dims["temporal"]:
            pres = rng.random((T_FRAMES, n, n)) < self.p_keep
            pres[:, ring] = True                        # backbone always on
            self.pres = pres
            self.hyper_on = rng.random((T_FRAMES, len(self.hyperedges))) \
                < self.p_keep
        else:
            self.pres = np.ones((1, n, n), bool)
            self.hyper_on = np.ones((1, len(self.hyperedges)), bool)
        self._frames: list[np.ndarray] | None = None

    # -- the medium interface (exp137's; deterministic re-iteration)
    def snapshots(self) -> list[np.ndarray]:
        if self._frames is None:
            frames = []
            n = self.n
            for t in range(self.T_eff):
                Wt = self.Wbase * self.pres[t]
                if self.hyperedges:
                    Badd = np.zeros((n, n), complex)
                    for k, (members, w_e) in enumerate(self.hyperedges):
                        if self.hyper_on[t, k]:
                            c = w_e / (len(members) - 1)
                            for a in range(len(members)):
                                for b in range(a + 1, len(members)):
                                    i, j = members[a], members[b]
                                    Badd[i, j] += c
                                    Badd[j, i] += c
                    Wt = Wt + Badd
                frames.append(Wt)
            self._frames = frames
        return [Wt.copy() for Wt in self._frames]

    def native_support(self) -> np.ndarray:
        sup = np.abs(self.Wbase) > 0
        for members, _ in self.hyperedges:
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    sup[members[a], members[b]] = True
                    sup[members[b], members[a]] = True
        return sup.astype(float)

    @property
    def violated(self) -> tuple[str, ...]:
        return tuple(VIOLATION[d] for d in DIMENSIONS if self.dims[d])


# ------------------------------------------------- the repair wrapper
class RepairedMedium:
    """Zero-knob pre-read repair wrapper. The read core (read_temporal ->
    project_phase_native / reactive_fraction / flip_clock_matrix ->
    execute_signed) is exp148/145/142's VERBATIM; the ONE rule lives
    entirely in the frames this wrapper yields. snapshots() is cached,
    deterministic, re-iterable."""

    kind = "repaired_corner"

    def __init__(self, inner: CornerMedium, frames: list[np.ndarray],
                 rule: str):
        self._inner = inner
        self._frames = frames
        self.rule = rule
        self.n = inner.n

    def snapshots(self) -> list[np.ndarray]:
        return [Wt.copy() for Wt in self._frames]

    def native_support(self) -> np.ndarray:
        sup = np.zeros((self.n, self.n), bool)
        for Wt in self._frames:
            sup |= np.abs(Wt) > 0
        return sup.astype(float)

    @property
    def violated(self) -> tuple[str, ...]:
        return self._inner.violated


# ------------------------------------------------- the three rules
def rule_hyper_S(med: CornerMedium, frames: list[np.ndarray],
                 F: float) -> list[np.ndarray]:
    """R_H (L142's deposit at the medium level): A += F * S with
    S_ij = 1 iff i,j share a hyperedge and F the pre-decode pooled median
    nonzero |W|. No-op when the medium has no hyperedges (S = 0)."""
    if not med.hyperedges:
        return frames                                   # identity, bit-exact
    n = med.n
    S = np.zeros((n, n))
    for members, _ in med.hyperedges:
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                i, j = members[a], members[b]
                S[i, j] = 1.0
                S[j, i] = 1.0
    return [Wt + F * S for Wt in frames]


def pooled_F(media: list[CornerMedium]) -> float:
    """L142's zero-knob F: median of the NONZERO |W_ij| pooled over ALL
    frames of the spot instances, computed BEFORE any arm-B decode."""
    vals = []
    for med in media:
        for Wt in med.snapshots():
            a = np.abs(Wt)
            vals.append(a[a > 0])
    return float(np.median(np.concatenate(vals)))


def rule_temporal_core(med: CornerMedium,
                       frames: list[np.ndarray]) -> list[np.ndarray]:
    """R_T (L140's flip-quiet discipline at the medium level): mask every
    frame to the across-frame CORE support (present in EVERY frame).
    Membership frozen -> zero presence transitions. No-op when T = 1
    (core = the frame's own support)."""
    core = None
    for Wt in frames:
        sup = np.abs(Wt) > 0
        core = sup if core is None else (core & sup)
    return [np.where(core, Wt, Wt.dtype.type(0)) for Wt in frames]


def rule_oriented_restore(med: CornerMedium,
                          frames: list[np.ndarray]) -> list[np.ndarray]:
    """R_O (support-level symmetrize): a pair with exactly one direction
    present gets the surviving value copied to the absent direction.
    No-op when the support is already symmetric (clean media)."""
    out = []
    for Wt in frames:
        sup = np.abs(Wt) > 0
        miss = sup.T & ~sup                  # (i,j) absent, mirror present
        if not miss.any():
            out.append(Wt)                   # identity, bit-exact
            continue
        Wn = Wt.copy()
        Wn[miss] = Wt.T[miss]
        out.append(Wn)
    return out


RULES = {"hyper": rule_hyper_S, "temporal": rule_temporal_core,
         "oriented": rule_oriented_restore}
RULE_MAP_DOC = {
    "hyper": ("R_H cancellation-density-weighted S (L142): A += F*S, "
              "S = co-hyperedge, F = median nonzero |W| pooled pre-decode"),
    "temporal": ("R_T flip-quiet windowing (L140): every frame masked to "
                 "the across-frame core support (membership frozen)"),
    "oriented": ("R_O one-way support restore (symmetrize); NOTE the stack "
                 "already symmetrizes per frame (PN2 S=(R+R.T)/2)"),
}


# ------------------------------------------------- factorial helpers
def yates_effect(medians: dict, factor_bits: int) -> float:
    """2^3 Yates contrast on cell medians, (1/4)-scale, sign fixed so
    positive = the active side degrades. factor_bits: bit mask over
    (o=4, h=2, t=1) for the effect's factors."""
    tot = 0.0
    for c, v in medians.items():
        parity = bin(c & factor_bits).count("1") & 1
        tot += (1.0 if parity == 0 else -1.0) * v
    return -tot / 4.0


def median_of(xs: list[float]) -> float:
    return float(np.median(xs)) if xs else float("nan")


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 3 instances per cell, 1 seed")
    args = ap.parse_args()
    per_cell = 3 if args.smoke else N_PER_CELL
    seeds = (1,) if args.smoke else SEEDS
    # spot battery re-uses the FIRST instances of the corner + clean cells
    # (deposited j = 0..9 for the full run; clamped in smoke mode only)
    spot_corner_j = list(range(min(10, per_cell)))
    spot_clean_j = list(range(min(10, per_cell)))
    t0 = time.time()
    fp = config_fingerprint()
    assert fp == EXP160_FP, (
        f"config fingerprint {fp} != exp160's deposited {EXP160_FP}")
    print(f"=== exp166: THE LEADING EDGE "
          f"({'SMOKE' if args.smoke else 'FULL'}) ===")
    print(f"  fingerprint {fp} (== exp160's deposit)  seed_base {SEED_BASE}"
          f"  cells {N_CELLS} x {per_cell}  seeds {seeds}\n")

    rejections: list[dict] = []
    instances: list[dict] = []
    all_errs: list[float] = []
    decode_fps: list[str] = []

    for c in range(N_CELLS):
        dims = cell_dims(c)
        for j in range(per_cell):
            seed = SEED_BASE + 1000 * c + j
            med = CornerMedium(N, seed, dims)
            errs, vs, branches, rhos = [], [], [], []
            for s in seeds:
                decode_fps.append(fp)
                try:
                    out = read_temporal(med, s)      # THE one call site
                    err = float(out["err_vs_target"])
                    if not np.isfinite(err):
                        raise ValueError(f"non-finite decode err {err}")
                    errs.append(err)
                    all_errs.append(err)
                    vs.append(bool(out["program_verified"]))
                    branches.append(out["branch"])
                    rhos.append(round(float(out["rho"]), 4))
                except Exception as e:               # RECORDED, never hidden
                    rejections.append(
                        {"cell": c, "j": j, "seed": s,
                         "rejection": f"{type(e).__name__}: {e}"[:200]})
            med_err = median_of(errs) if errs else None
            rec = {
                "cell": c,
                "cell_dims": {d: dims[d] for d in FOCAL},
                "k_active": int(sum(1 for d in FOCAL if dims[d])),
                "j": j, "gen_seed": seed,
                "violated": list(med.violated),
                "n_oneway": med.n_oneway, "n_hyper": med.n_hyper,
                "p_keep": round(med.p_keep, 3), "T": med.T_eff,
                "branch": branches, "rho": rhos,
                "errs": errs, "median_err": med_err, "verified": vs,
                "above_bar": bool(med_err is not None and med_err > BAR),
                "config_fp": fp,
            }
            instances.append(rec)
        print(f"  [cell {c} {'o' if dims['oriented'] else '-'}"
              f"{'h' if dims['hyper'] else '-'}"
              f"{'t' if dims['temporal'] else '-'}] done "
              f"{len(instances)} instances, {len(all_errs)} decodes, "
              f"rejections {len(rejections)}, "
              f"median-so-far {median_of(all_errs):.3f}")

    # ---------------- P1: per-cell medians + factorial effect table
    cell_meds: dict[int, float] = {}
    cell_stats: dict[int, dict] = {}
    for c in range(N_CELLS):
        rs = [r for r in instances if r["cell"] == c]
        ms = [r["median_err"] for r in rs if r["median_err"] is not None]
        cell_meds[c] = median_of(ms)
        cell_stats[c] = {
            "cell": c,
            "dims": {d: cell_dims(c)[d] for d in FOCAL},
            "k_active": int(sum(1 for d in FOCAL if cell_dims(c)[d])),
            "n": len(rs), "n_finite": len(ms),
            "median_err": median_of(ms),
            "mean_err": (float(np.mean(ms)) if ms else None),
            "p90_err": (float(np.percentile(ms, 90)) if ms else None),
            "max_err": (float(np.max(ms)) if ms else None),
            "verify_rate": (float(np.mean([v for r in rs for v in
                                           r["verified"]]))
                            if rs else None),
            "n_above_bar": sum(1 for r in rs if r["above_bar"]),
        }
    effects = {
        "main_oriented": yates_effect(cell_meds, 0b100),
        "main_hyper": yates_effect(cell_meds, 0b010),
        "main_temporal": yates_effect(cell_meds, 0b001),
        "int_oriented_x_hyper": yates_effect(cell_meds, 0b110),
        "int_oriented_x_temporal": yates_effect(cell_meds, 0b101),
        "int_hyper_x_temporal": yates_effect(cell_meds, 0b011),
        "int_oriented_x_hyper_x_temporal": yates_effect(cell_meds, 0b111),
    }
    mains = {k: v for k, v in effects.items() if k.startswith("main_")}
    dominant = max(mains, key=mains.get)
    dominant_dim = dominant[len("main_"):]

    # ---------------- P2: ordering along the active-count axis
    by_k = {}
    for k in range(4):
        cs = [c for c in range(N_CELLS)
              if sum(1 for d in FOCAL if cell_dims(c)[d]) == k]
        by_k[k] = {
            "cells": cs,
            "mean_of_cell_medians": float(np.mean([cell_meds[c]
                                                   for c in cs])),
            "pooled_instance_median": median_of(
                [r["median_err"] for r in instances
                 if r["k_active"] == k and r["median_err"] is not None]),
        }
    m = [by_k[k]["mean_of_cell_medians"] for k in range(4)]
    ordering_held = bool(m[0] < m[1] < m[2] < m[3])
    corner_is_worst = bool(cell_meds[7] == max(cell_meds.values()))
    actual_order_cells = [c for c, _ in
                          sorted(cell_meds.items(), key=lambda kv: kv[1])]

    # ---------------- P4: the mapped spot battery (chosen by P1)
    rule_name = dominant_dim
    spot_corner_media = [CornerMedium(N, SEED_BASE + 1000 * 7 + j,
                                      cell_dims(7)) for j in spot_corner_j]
    spot_clean_media = [CornerMedium(N, SEED_BASE + 1000 * 0 + j,
                                     cell_dims(0)) for j in spot_clean_j]
    spot_media = spot_corner_media + spot_clean_media

    # arm A: exp160 stack verbatim on the raw medium (replay integrity)
    spot_records = []
    for tag, meds, cell in (("corner", spot_corner_media, 7),
                            ("clean", spot_clean_media, 0)):
        for idx, med in enumerate(meds):
            j = (spot_corner_j if tag == "corner" else spot_clean_j)[idx]
            errs_a, vs_a = [], []
            for s in seeds:
                out = read_temporal(med, s)
                errs_a.append(float(out["err_vs_target"]))
                vs_a.append(bool(out["program_verified"]))
            main_rec = next(r for r in instances
                            if r["cell"] == cell and r["j"] == j)
            replay_ok = (len(errs_a) == len(main_rec["errs"])
                         and all(x == y for x, y in
                                 zip(errs_a, main_rec["errs"])))
            spot_records.append({
                "tag": tag, "cell": cell, "j": j,
                "gen_seed": main_rec["gen_seed"],
                "errs_armA": errs_a, "verified_armA": vs_a,
                "median_armA": median_of(errs_a),
                "replay_bit_exact_vs_main_battery": bool(replay_ok),
            })

    # the rule + its (single, pre-decode) statistic
    rule_params: dict = {"rule": rule_name,
                         "description": RULE_MAP_DOC[rule_name]}
    if rule_name == "hyper":
        F = pooled_F(spot_media)
        rule_params["F_pooled_median_nonzero_absW"] = F
        rule_params["pooled_over"] = ("all frames of the 20 spot instances,"
                                      " computed BEFORE any arm-B decode")

    # arm B: same stack on the repaired wrapper
    for rec, med in zip(spot_records, spot_media):
        frames = med.snapshots()
        if rule_name == "hyper":
            fixed = rule_hyper_S(med, frames, F)
        else:
            fixed = RULES[rule_name](med, frames)
        wrapped = RepairedMedium(med, fixed, rule_name)
        errs_b, vs_b = [], []
        for s in seeds:
            out = read_temporal(wrapped, s)
            errs_b.append(float(out["err_vs_target"]))
            vs_b.append(bool(out["program_verified"]))
        rec["errs_armB"] = errs_b
        rec["verified_armB"] = vs_b
        rec["median_armB"] = median_of(errs_b)
        rec["armB_bit_identical_to_armA"] = bool(
            all(x == y for x, y in zip(errs_b, rec["errs_armA"])))

    corner_recs = [r for r in spot_records if r["tag"] == "corner"]
    clean_recs = [r for r in spot_records if r["tag"] == "clean"]
    replay_ok_all = all(r["replay_bit_exact_vs_main_battery"]
                        for r in spot_records)
    clean_noop_all = all(r["armB_bit_identical_to_armA"] for r in clean_recs)
    corner_med_a = median_of([r["median_armA"] for r in corner_recs])
    corner_med_b = median_of([r["median_armB"] for r in corner_recs])
    clean_med_a = median_of([r["median_armA"] for r in clean_recs])
    clean_med_b = median_of([r["median_armB"] for r in clean_recs])
    corner_improved = bool(corner_med_b < corner_med_a)
    n_corner_improved = sum(1 for r in corner_recs
                            if r["median_armB"] < r["median_armA"])

    # ---------------- gates
    cells_finite = all(cell_stats[c]["n_finite"] == per_cell
                       for c in range(N_CELLS))
    p1 = bool(cells_finite and len(effects) == 7 and dominant_dim)
    p2 = bool(ordering_held and corner_is_worst)
    verify_rate = (float(np.mean([v for r in instances for v in
                                  r["verified"]]))
                   if instances else None)
    tail_rows = [
        {"cell": cell_stats[c]["cell"],
         "dims": cell_stats[c]["dims"],
         "n_above_bar": cell_stats[c]["n_above_bar"],
         "median_err": cell_stats[c]["median_err"],
         "max_err": cell_stats[c]["max_err"]}
        for c in range(N_CELLS) if cell_stats[c]["n_above_bar"] > 0]
    p3 = bool(len(rejections) == 0
              and len(all_errs) == len(instances) * len(seeds)
              and all(np.isfinite(all_errs))
              and (verify_rate == 1.00 or tail_rows))
    p4 = bool(replay_ok_all and clean_noop_all and corner_improved)
    n_pass = sum(int(x) for x in (p1, p2, p3, p4))
    verdict = (f"{n_pass}/4 gates" if not args.smoke else "smoke")

    print(f"\n  cell medians (o,h,t -> mV):")
    for c in range(N_CELLS):
        d = cell_dims(c)
        print(f"    {int(d['oriented'])}{int(d['hyper'])}"
              f"{int(d['temporal'])}: {cell_meds[c]:.3f}"
              f"  (n_above {cell_stats[c]['n_above_bar']})")
    print(f"  effects: " + ", ".join(f"{k}={v:+.3f}"
                                     for k, v in effects.items()))
    print(f"  dominant: {dominant_dim}  ordering-by-k: "
          f"{['%.3f' % x for x in m]}  held={ordering_held}"
          f"  corner-worst={corner_is_worst}")
    print(f"  spot rule {rule_name}: corner {corner_med_a:.3f} -> "
          f"{corner_med_b:.3f} (improved {n_corner_improved}/"
          f"{len(corner_recs)}), clean {clean_med_a:.3f} -> "
          f"{clean_med_b:.3f}, replay {replay_ok_all}, "
          f"clean-noop {clean_noop_all}")
    print(f"  GATES: {n_pass}/4  "
          f"P1={p1} P2={p2} P3={p3} P4={p4}")
    print(f"  rejections {len(rejections)}  decodes {len(all_errs)}  "
          f"verify {verify_rate}")

    result = {
        "exp": "exp166_leading_edge",
        "claim": ("exp160's registered follow-up: the universality "
                  "boundary's tail (5/200 above the 1.30 mV bar, all "
                  "verifying) lives in the oriented+hyper+temporal corner; "
                  "a crossed 2^3 factorial x 50 random instances (400 "
                  "media, exp160's generator verbatim with the dimension "
                  "coins dictated by the cell) prices the corner, names "
                  "the dominant main effect + interactions, tests the "
                  "pre-registered monotone-degradation ordering along the "
                  "active-count axis, and hands back ONE zero-knob repair "
                  "candidate chosen by a mapping fixed before the run"),
        "pre_registration": {
            "seed_base": SEED_BASE,
            "seed_rule": "SEED_BASE + 1000*c + j, c = 4o+2h+t, j = 0..49",
            "pinned_off": list(PINNED_OFF),
            "pinned_rationale": ("exp160 U3: signed/complex "
                                 "neutral-to-protective (lift 0.74/0.67)"),
            "bar_mV": BAR, "seeds": list(SEEDS),
            "exp160_fp_asserted": EXP160_FP,
            "rule_map": RULE_MAP_DOC,
        },
        "generator": {
            "kind": "exp160 RandomMedium verbatim, corner-pinned",
            "n": N, "n_instances": len(instances),
            "magnitudes": "U(0.5, 1.5) = exp137's _wU operating range",
            "support": "exp137's _base_connected (ring + chords p=0.04)",
            "temporal_frames": T_FRAMES,
            "hyper_factorization": "w_e/(|e|-1) (exp137's clause)",
            "note": ("signed/complex pinned inactive -> all frames real "
                     "nonneg; hyperedge weights real positive"),
        },
        "config": {**READ_CONFIG, "fingerprint": fp},
        "cells": [cell_stats[c] for c in range(N_CELLS)],
        "cell_medians_mV": {str(c): cell_meds[c] for c in range(N_CELLS)},
        "effect_table": {
            "scale": ("2^3 Yates contrasts on the 8 cell medians, (1/4)-"
                      "scale, positive = active side degrades (mV)"),
            **effects,
            "dominant_main_effect": dominant_dim,
        },
        "ordering_by_k": by_k,
        "ordering": {
            "registered_expectation": ("mean-of-cell-medians strictly "
                                       "increasing k=0..3 AND corner cell "
                                       "is the max cell median"),
            "grouped_medians_k0_to_k3": m,
            "ordering_held": ordering_held,
            "corner_is_worst": corner_is_worst,
            "actual_order_cells_worst_first": actual_order_cells,
        },
        "spot_battery": {
            "instances": spot_records,
            "rule": rule_params,
            "corner_median_armA": corner_med_a,
            "corner_median_armB": corner_med_b,
            "clean_median_armA": clean_med_a,
            "clean_median_armB": clean_med_b,
            "n_corner_improved": n_corner_improved,
            "n_corner": len(corner_recs),
            "replay_bit_exact_all": replay_ok_all,
            "clean_noop_bit_exact_all": clean_noop_all,
            "corner_improved": corner_improved,
        },
        "pooled_median_err": median_of(all_errs) if all_errs else None,
        "gates": {
            "P1_factorial_decomposition": {
                "pass": p1,
                "cells_populated_finite": cells_finite,
                "dominant_main_effect": dominant_dim,
                "effect_rows": len(effects),
            },
            "P2_monotone_active_count": {
                "pass": p2,
                "ordering_held": ordering_held,
                "corner_is_worst": corner_is_worst,
                "actual_order_cells_worst_first": actual_order_cells,
            },
            "P3_zero_rejections": {
                "pass": p3,
                "rejections": len(rejections),
                "rejection_records": rejections,
                "decodes": len(all_errs),
                "instances": len(instances),
                "verify_rate": verify_rate,
                "above_bar_tail": tail_rows,
            },
            "P4_repair_candidate": {
                "pass": p4,
                "rule": rule_params,
                "replay_bit_exact_all": replay_ok_all,
                "clean_noop_bit_exact_all": clean_noop_all,
                "corner_improved": corner_improved,
                "corner_median_mV": [corner_med_a, corner_med_b],
                "clean_median_mV": [clean_med_a, clean_med_b],
            },
        },
        "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
    }
    if not args.smoke:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  deposited {OUT}")
    return result


if __name__ == "__main__":
    main()
