#!/usr/bin/env python3
"""exp142 — THE SIGN-CARRYING READ (the L115-registered SEMANTICS-CARRYING
READ, sharpest single edge = SIGN).

FOUNDATION (exp137, ledger L115, 4/4): the M33 two-source read + ONE fixed
front-end consumed 6 out-of-domain medium classes with ZERO rejections and
pooled OOD median 0.65 mV (ratio 1.18 vs the 2.0x bound). The boundary
diagnosis: the read consumes coupling MAGNITUDE on a static, symmetric,
pairwise support — orientation/sign/phase are DISCARDED by the projection
(|W_t| -> (B+B^T)/2 -> time-average). Sharpest named gaps: SIGNED media run
degraded (negative conductances fight the read; the traversal filter
`A[i] > 0` silently skips negative edges) and complex-phase media suffer
SILENT dtype coercion. exp137's deposited degraded-class medians: signed
0.685 mV (max 1.69), complex_phase 0.715 mV (max 1.72).

THE MINIMUM SEMANTICS EXTENSION (one projection rule + one traversal rule,
zero knobs — everything else exp94/exp137 VERBATIM):

  THE SIGNED-WEIGHT RULE (pre-registered, stated before running):
  R1 STRUCTURE ON |A|  — a signed edge is a FIRST-CLASS edge: it connects
     exactly as its magnitude. Canon labeling = labeling_bfs_n(|A|); the
     Euler step dt = star_dt(gamma, max_i sum_j |A_ij|) (stability on the
     magnitude; bit-identical to exp94 on positive input); the walk's
     frontier discovery and BFS order run on |A[i,j]| > 0. The exp137-named
     `A[i] > 0` traversal filter is DROPPED.
  R2 SIGN IN THE DYNAMICS — the continuous coupling consumes the SIGNED
     matrix verbatim (GraphCollective on A as-is): a negative conductance
     anti-diffuses (pushes the cell away from its neighbor) — the honest
     signed physics. NO reflection is invented at the commit: the walk is a
     delivery schedule for the spec/canon layers (with_canon=True, the
     commit is a layer lookup at the cell's own index), so the polarity
     channel is the dynamics'. On all-positive input every clause reduces
     to exp94 bit-exactly.
  R3 SIGN-PRESERVING SYMMETRIZE (the projection; the ONLY change from
     exp137's project_medium): R_t = Re(W_t) (for real signed media R = W
     verbatim; for complex-phase media R = |W| cos(phi), the phase-ALIGNED
     component — the sign of cos(phi) is the polarity the read consumes;
     the reactive sin(phi) channel stays discarded, an OWNED scope note:
     exp137's silent coercion becomes an owned real embedding);
     S_t = (R_t + R_t^T)/2 (NO magnitude); A_signed = mean_t S_t; zero
     diagonal. On all-positive real media R3 is BIT-IDENTICAL to
     exp137's project_medium, so the extension is a STRICT SUPERSET.

THE ADVERSARIAL PROBE INSTRUMENT (magnitude-identical, sign-different):
  12 sign-flip pairs = 24 probes. Each pair is ONE substrate (ring
  backbone, weight 1.0) + a carrier chord set C (k=6 chords, weight w_c);
  member P+ carries +w_c on C, member P- carries -w_c on C; |P+| == |P-|
  BITWISE (same magnitudes, same support) and C is the pair's ONLY sign
  difference. The carrier sits where a polarity contrast exists in the
  read's own coordinate system:
    F1 zone-tail      chords z2 cells (60-75) -> trunk-canon tail cells
                      (76-86); contrast -30 zone vs -50 trunk canon.
    F2 zone-head      chords z0 cells (2-12) -> head-canon cells (0-1);
                      contrast -30 zone vs -20 head canon.
    F3 canon-boundary chords spanning the head/trunk canon boundary
                      INSIDE the amputated span (computed from the
                      substrate's own ring canon); contrast -20 vs -50.
  Dose ladder w_c in {4, 16, 64, 256} x 3 families = 12 pairs.
  INSTRUMENT DISCLOSURE: a pre-run calibration (F1 only, 1 seed) bracketed
  the dose response; it showed F1 verdict flips at w_c in {64, 256} and the
  ladder was set to bracket that boundary across all three families BEFORE
  the registered run. The gates below were fixed before the registered run;
  H2's premise (the sign read separates what the magnitude read cannot) is
  tested across ALL families and doses, including the possibility that F2
  or F3 fail to separate.

PRE-REGISTERED GATES (fixed before the registered run):

  GATE-H1  (fidelity improves on the degraded classes) on the exp137
           instance grid (same generators, same seeds 10_000*ci + i:
           8 instances at n=100 + 2 at n=400, seeds 1/2/3), the
           sign-carrying read's median decode err is <= 0.60 mV on
           signed (exp137 deposited 0.685) AND <= 0.63 mV on
           complex_phase (deposited 0.715). Mechanism claim: the magnitude
           projection OVER-COUPLES (every edge attractive — committed
           identity is dragged across inhibitory junctions as if
           excitatory); the sign-carrying read lets inhibition do its work
           in the dynamics so the committed pattern sticks closer to the
           spec/canon values.
  GATE-H2  (verdict separation under sign flips)
           (a) PRECONDITION: the magnitude-only read (exp137's projection
               + verbatim executor) decodes the two members of EVERY pair
               IDENTICALLY — bit-identical projected matrix, identical
               errs and verdicts at every seed. Sign-blindness is
               VERIFIED, not assumed; if it fails, the probe instrument is
               invalid and H2 fails.
           (b) SEPARATION: the sign-carrying read's majority verdict
               (>= 2/3 seeds program_verified) differs within at least
               one pair — the sign rule CHANGES at least one decode
               verdict relative to magnitude-only. If the sign read's
               verdicts are identical within every pair, the extension's
               premise is REFUTED (that is the registered refutation
               outcome, not a harness error).
           Directionality is DEPOSITED per family (which member decodes
           better), not gated.
  GATE-H3  (strict superset / in-domain no-regression) on the in-domain
           control (torus, exp73's battery, seeds 1/2/3) the sign-carrying
           read's final V states are BIT-IDENTICAL to the magnitude-only
           read's (every clause reduces to exp94/exp137 verbatim on
           all-positive input) and the verify rate is preserved. Backstop
           bound: signed control median <= magnitude control median
           + 0.10 mV.
  GATE-H4  (zero rejections) every decode in the run — both arms, OOD
           classes, control, all 24 probes (2 x 30 + 6 + 144 decodes) —
           returns a finite err_vs_target, no exception, no dtype-coercion
           warning (exp137's warnings-as-errors policy). 0 rejections.

DEPOSIT: results/exp142_sign_read.json

RUN:
  python3 -m experiments.exp142_sign_read            # full
  python3 -m experiments.exp142_sign_read --smoke    # instrument check
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.compiler.anatomy import compile_anatomy
from cultivation.substrate.graph import GraphCollective
from experiments.exp73_active_renormalization import make_battery
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import (
    MULTI, execute_two_source_n, labeling_bfs_n, spec_target_n,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp142_sign_read.json")

STAR_OP = {"gamma": 64.0, "mu": 0.0}       # exp99's battery-wide point
SEEDS = (1, 2, 3)
N_INSTANCES = 8                             # at n=100 (exp137's grid)
N_INSTANCES_400 = 2                         # scale spot-checks
WINDOW_H = 24.0                             # exp94's encode window
COMMIT_NOISE = 0.6                          # exp94's commit noise
STEPS_PER_CELL = 8                          # exp94's walk interlude
ERR_BAR = 6.0                               # exp94's verify bar

# exp137's deposited degraded-class medians (the H1 comparison anchors)
EXP137_SIGNED_MEDIAN = 0.685
EXP137_COMPLEX_MEDIAN = 0.715
H1_SIGNED_BAR = 0.60
H1_COMPLEX_BAR = 0.63

# the adversarial dose ladder and carrier geometry
DOSES = (4.0, 16.0, 64.0, 256.0)
K_CHORDS = 6
PROBE_SEED = 7                              # substrate construction seed


# ------------------------------------------------- the medium interface
class _StaticMedium:
    """A fixed adjacency presented through exp137's medium interface."""

    def __init__(self, A: np.ndarray):
        self.A = np.array(A, copy=True)

    def snapshots(self):
        return [self.A.copy()]

    def native_support(self) -> np.ndarray:
        return (np.abs(self.A) > 0).astype(float)


# ------------------------------------------------- R3: the projections
def project_signed(medium) -> np.ndarray:
    """R3 — the sign-preserving front-end, ONE rule, zero knobs:
    real-aligned component -> sign-preserving symmetrize -> time-average.
    The ONLY difference from exp137's project_medium is the dropped
    magnitude: Re(W_t) instead of |W_t|."""
    snaps = medium.snapshots()
    acc = None
    for W in snaps:
        R = np.real(W)                   # phase-aligned component
        S = (R + R.T) / 2.0              # sign-PRESERVING symmetrize
        acc = S if acc is None else acc + S
    A = acc / len(snaps)
    np.fill_diagonal(A, 0.0)
    return A


def project_magnitude(medium) -> np.ndarray:
    """exp137's front-end verbatim (the magnitude-only arm)."""
    snaps = medium.snapshots()
    acc = None
    for W in snaps:
        B = np.abs(W)
        S = (B + B.T) / 2.0
        acc = S if acc is None else acc + S
    A = acc / len(snaps)
    np.fill_diagonal(A, 0.0)
    return A


# --------------------------- R1+R2: the sign-carrying executor call
def execute_signed(spec: AnatomySpec, adjacency: np.ndarray, seed: int,
                   op: dict, return_state: bool = False) -> dict:
    """exp94's execute_two_source_n with EXACTLY the pre-registered
    signed clauses R1 (structure on |A|: dt, canon, the two traversal
    filters) and R2 (the coupling consumes the signed matrix — which is
    simply what passing the signed adjacency into GraphCollective does).
    Every other line is exp94 verbatim (the commit branches untouched;
    with_canon=True, no anchor, frontier_mode='walk' — exp137's call)."""
    n = adjacency.shape[0]
    gamma, mu = op["gamma"], op["mu"]
    absA = np.abs(adjacency)
    dt = star_dt(gamma, float(absA.sum(axis=1).max()))          # R1
    canon = labeling_bfs_n(absA)                                # R1
    target = spec_target_n(spec, canon, n)
    c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                        mu_theta=mu)                            # R2 (signed)
    c.set_target(canon)
    c.write_spec_layer(target)
    prog = compile_anatomy(spec, n=n)
    if prog.rejected:
        return {"program_verified": False, "rejected": prog.rejected,
                "err_vs_target": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=dt)
    c.release_clamps()
    reg_idx: list[int] = []
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    if reg_idx:
        reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
        region_set = set(reg_walk)
        c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
        wound_center = float(np.mean(c.theta[reg_walk]))
        parent_of: dict[int, int] = {}
        frontier: list[int] = []
        # exp97's blastema frontier under R1: |A| > 0 (the signed-weight
        # traversal rule — the exp137-named `A[i] > 0` filter dropped)
        for i in reg_walk:
            nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                    if j not in region_set]
            if nbrs:
                parent_of[i] = int(max(
                    nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
                frontier.append(i)
        if not frontier:
            frontier = reg_idx[:1]
            parent_of[frontier[0]] = frontier[0]
        visited = set(frontier)
        order = [(i, parent_of[i]) for i in frontier]
        queue = list(frontier)
        while queue:
            i = queue.pop(0)
            for j in np.where(np.abs(c.A[i]) > 0)[0]:           # R1
                if int(j) in region_set and int(j) not in visited:
                    visited.add(int(j))
                    parent_of[int(j)] = int(i)
                    order.append((int(j), int(i)))
                    queue.append(int(j))
        for i, src in order:
            for _ in range(STEPS_PER_CELL):
                c.step(dt)
            canon_src = getattr(c, "phi_spec_canon", None)
            if c.phi_spec[i] >= NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
            elif canon_src is not None:
                theta_new = canon_src[i] + c.rng.normal(0.0, COMMIT_NOISE)
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
            c.theta[i] = theta_new
            c.V[i] = theta_new
    c.run(15.0, dt=dt)
    per_zone = {}
    ok_all = True
    for z in spec.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        zmean = float(np.mean(c.V[i0:i1]))
        ok = abs(zmean - z.voltage) <= ERR_BAR
        per_zone[z.name] = {"mean": round(zmean, 1), "ok": bool(ok)}
        ok_all &= ok
    err = float(c.pattern_error(target))
    ok_all &= err < ERR_BAR
    out = {"program_verified": bool(ok_all), "per_zone": per_zone,
           "err_vs_target": round(err, 2)}
    if return_state:
        out["final_state"] = {"V": c.V.tolist(), "target": target.tolist()}
    return out


# ------------------------------------------------------------ helpers
def read_mag(adjacency: np.ndarray, seed: int,
             return_state: bool = False) -> dict:
    """The magnitude-only arm: exp94's executor VERBATIM (exp137's
    read_one policy: a coerced read is a rejection)."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        out = execute_two_source_n(MULTI, adjacency, seed, op=STAR_OP,
                                   frontier_mode="walk",
                                   return_state=return_state)
    err = float(out["err_vs_target"])
    if not np.isfinite(err):
        raise ValueError(f"non-finite decode err {err}")
    return out


def read_sign(adjacency: np.ndarray, seed: int,
              return_state: bool = False) -> dict:
    """The sign-carrying arm (same rejection policy)."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        out = execute_signed(MULTI, adjacency, seed, op=STAR_OP,
                             return_state=return_state)
    err = float(out["err_vs_target"])
    if not np.isfinite(err):
        raise ValueError(f"non-finite decode err {err}")
    return out


def native_target(medium, n: int) -> np.ndarray:
    return spec_target_n(MULTI, labeling_bfs_n(medium.native_support()), n)


# ------------------------------------------------- the probe substrate
def probe_pair(n: int, family: str, w_c: float,
               seed: int) -> tuple[np.ndarray, np.ndarray, list]:
    """One adversarial sign-flip pair: (A_pos, A_neg) magnitude-identical,
    differing ONLY in the sign of the carrier chord set C."""
    rng = np.random.default_rng(seed)
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
    canon = labeling_bfs_n(A)
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
        b_hi = max(h_in)                       # canon boundary inside span
        b_lo = min(j for j in t_in if j > b_hi)
        left = [i for i in h_in if b_hi - K_CHORDS + 1 <= i <= b_hi]
        right = [j for j in t_in if b_lo <= j <= b_lo + K_CHORDS - 1]
        rng.shuffle(left); rng.shuffle(right)
        for t in range(K_CHORDS):
            chords.append((left[t % len(left)], right[t % len(right)]))
    else:
        raise ValueError(family)
    Ap = A.copy(); An = A.copy()
    for i, j in chords:
        Ap[i, j] = Ap[j, i] = w_c
        An[i, j] = An[j, i] = -w_c
    assert np.array_equal(np.abs(Ap), np.abs(An)), "pairs must be "\
        "magnitude-identical"
    return Ap, An, chords


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 2 instances/class, 1 seed, "
                         "1 dose")
    args = ap.parse_args()
    n_inst = 2 if args.smoke else N_INSTANCES
    n_inst400 = 1 if args.smoke else N_INSTANCES_400
    seeds = (1,) if args.smoke else SEEDS
    doses = DOSES[:1] if args.smoke else DOSES
    t0 = time.time()
    print("=== exp142: THE SIGN-CARRYING READ ===\n")

    rejections = 0
    all_errs: list[float] = []

    # ---- GATE-H3: in-domain control, strict-superset bit-identity
    battery = make_battery()
    ctrl_adj = battery["torus"]
    ctrl = {"substrate": "torus"}
    mag_errs, sign_errs, bit_ok = [], [], True
    mag_v, sign_v = [], []
    for s in seeds:
        out_m = read_mag(ctrl_adj, s, return_state=True)
        out_s = read_sign(project_signed(_StaticMedium(ctrl_adj)), s,
                          return_state=True)
        mag_errs.append(out_m["err_vs_target"])
        sign_errs.append(out_s["err_vs_target"])
        mag_v.append(bool(out_m["program_verified"]))
        sign_v.append(bool(out_s["program_verified"]))
        all_errs.extend([out_m["err_vs_target"], out_s["err_vs_target"]])
        same = np.array_equal(np.asarray(out_m["final_state"]["V"]),
                              np.asarray(out_s["final_state"]["V"]))
        bit_ok &= same
    ctrl["magnitude_errs"] = mag_errs
    ctrl["sign_errs"] = sign_errs
    ctrl["magnitude_verify"] = float(np.mean(mag_v))
    ctrl["sign_verify"] = float(np.mean(sign_v))
    ctrl["bit_identical"] = bool(bit_ok)
    ctrl["mag_median"] = float(np.median(mag_errs))
    ctrl["sign_median"] = float(np.median(sign_errs))
    ctrl["backstop_pass"] = bool(ctrl["sign_median"]
                                 <= ctrl["mag_median"] + 0.10)
    print(f"  H3 control torus: mag {ctrl['mag_median']:.2f} "
          f"sign {ctrl['sign_median']:.2f} bit-identical {bit_ok} "
          f"verify {ctrl['magnitude_verify']:.2f}/"
          f"{ctrl['sign_verify']:.2f}")

    # ---- GATE-H1: the two degraded classes on exp137's grid
    from experiments.exp137_universal_reader import (
        ComplexMedium, SignedMedium,
    )
    ood: dict = {}
    ref_ci = {"signed": 1, "complex_phase": 2}   # exp137's class indices
    ref_median = {"signed": EXP137_SIGNED_MEDIAN,
                  "complex_phase": EXP137_COMPLEX_MEDIAN}
    for kind, cls in (("signed", SignedMedium),
                      ("complex_phase", ComplexMedium)):
        inst_rec, errs, errs_native, oks = [], [], [], []
        for i in range(n_inst + n_inst400):
            n = 400 if i >= n_inst else 100
            med = cls(n, seed=10_000 * ref_ci[kind] + i)   # exp137 seeds
            A = project_signed(med)                         # R3
            assert not np.iscomplexobj(A), "R3 must deliver a real matrix"
            for s in seeds:
                try:
                    out = read_sign(A, s, return_state=True)
                except Exception as e:                       # pragma: no cover
                    rejections += 1
                    inst_rec.append({"n": n, "seed": s,
                                     "rejection":
                                     f"{type(e).__name__}: {e}"[:200]})
                    continue
                err = float(out["err_vs_target"])
                V = np.asarray(out["final_state"]["V"])
                err_nat = float(np.sqrt(np.mean(
                    (V - native_target(med, n)) ** 2)))
                errs.append(err)
                errs_native.append(err_nat)
                oks.append(bool(out["program_verified"]))
                all_errs.append(err)
                inst_rec.append({"n": n, "seed": s, "err": err,
                                 "err_native": round(err_nat, 2),
                                 "verified": bool(out["program_verified"])})
        ood[kind] = {
            "rejections": sum(1 for r in inst_rec if "rejection" in r),
            "err_median": float(np.median(errs)) if errs else None,
            "err_max": float(np.max(errs)) if errs else None,
            "err_native_median": (float(np.median(errs_native))
                                  if errs_native else None),
            "verify_rate": float(np.mean(oks)) if oks else None,
            "instances": inst_rec,
        }
        print(f"  H1 {kind:14s} sign-read median "
              f"{ood[kind]['err_median']:.3f} "
              f"max {ood[kind]['err_max']:.2f} "
              f"verify {ood[kind]['verify_rate']:.2f} "
              f"(exp137 magnitude-read {ref_median[kind]:.3f})")

    # ---- GATE-H2: the adversarial sign-flip probe ladder
    families = ("F1_zone_tail", "F2_zone_head", "F3_canon_boundary")
    pairs: list[dict] = []
    n_bit_identical = 0
    separated, verdict_changed = [], []
    for fam in families:
        for w_c in doses:
            Ap, An, chords = probe_pair(100, fam, w_c, PROBE_SEED)
            rec = {"family": fam, "dose": w_c, "n_chords": len(chords)}
            arms: dict = {}
            for name, W, arm in (("magnitude+", Ap, "mag"),
                                 ("magnitude-", An, "mag"),
                                 ("sign+", Ap, "sign"),
                                 ("sign-", An, "sign")):
                med = _StaticMedium(W)
                errs, vs = [], []
                for s in seeds:
                    try:
                        if arm == "mag":
                            out = read_mag(project_magnitude(med), s)
                        else:
                            out = read_sign(project_signed(med), s)
                    except Exception as e:                   # pragma: no cover
                        rejections += 1
                        errs.append(float("nan")); vs.append(False)
                        rec.setdefault("rejections", []).append(
                            f"{name} s{s}: {type(e).__name__}"[:120])
                        continue
                    errs.append(float(out["err_vs_target"]))
                    vs.append(bool(out["program_verified"]))
                    all_errs.append(float(out["err_vs_target"]))
                arms[name] = {"errs": errs, "verify": vs,
                              "majority": bool(np.mean(vs) > 0.5)
                              if vs else False}
            # (a) the magnitude arm MUST be sign-blind: identical errs
            blind = (arms["magnitude+"]["errs"]
                     == arms["magnitude-"]["errs"])
            rec["magnitude_sign_blind"] = bool(blind)
            n_bit_identical += int(blind)
            # (b) the sign arm separates the pair at the verdict level
            sep = (arms["sign+"]["majority"] != arms["sign-"]["majority"])
            rec["sign_separated"] = bool(sep)
            changed = bool(sep and (
                arms["sign+"]["majority"]
                != arms["magnitude+"]["majority"]
                or arms["sign-"]["majority"]
                != arms["magnitude+"]["majority"]))
            rec["verdict_changed_vs_magnitude"] = changed
            rec["arms"] = arms
            pairs.append(rec)
            if sep:
                separated.append(f"{fam}@{w_c:g}")
            if changed:
                verdict_changed.append(f"{fam}@{w_c:g}")
            print(f"  H2 {fam:17s} w={w_c:6.1f}  blind={blind}  "
                  f"mag {arms['magnitude+']['errs']} "
                  f"V{int(arms['magnitude+']['majority'])} | "
                  f"sign+ {arms['sign+']['errs']} "
                  f"V{int(arms['sign+']['majority'])} | "
                  f"sign- {arms['sign-']['errs']} "
                  f"V{int(arms['sign-']['majority'])}"
                  + ("  <== SEPARATED" if sep else ""))

    # ---- gates
    h1 = bool(ood["signed"]["err_median"] is not None
              and ood["complex_phase"]["err_median"] is not None
              and ood["signed"]["err_median"] <= H1_SIGNED_BAR
              and ood["complex_phase"]["err_median"] <= H1_COMPLEX_BAR)
    h2 = bool(len(pairs) > 0 and n_bit_identical == len(pairs)
              and len(verdict_changed) >= 1)
    h3 = bool(bit_ok and ctrl["sign_verify"] >= ctrl["magnitude_verify"]
              and ctrl["backstop_pass"])
    h4 = bool(rejections == 0 and len(all_errs) > 0)
    gates = {
        "H1_fidelity_improves": {
            "pass": h1,
            "signed_median": ood["signed"]["err_median"],
            "signed_bar": H1_SIGNED_BAR,
            "signed_exp137": EXP137_SIGNED_MEDIAN,
            "complex_median": ood["complex_phase"]["err_median"],
            "complex_bar": H1_COMPLEX_BAR,
            "complex_exp137": EXP137_COMPLEX_MEDIAN},
        "H2_verdict_separation": {
            "pass": h2,
            "n_pairs": len(pairs), "n_probes": 2 * len(pairs),
            "magnitude_sign_blind_pairs": n_bit_identical,
            "separated_pairs": separated,
            "verdict_changed_vs_magnitude": verdict_changed},
        "H3_strict_superset": {
            "pass": h3,
            "bit_identical": bool(bit_ok),
            "mag_median": ctrl["mag_median"],
            "sign_median": ctrl["sign_median"],
            "verify_mag": ctrl["magnitude_verify"],
            "verify_sign": ctrl["sign_verify"],
            "backstop_pass": ctrl["backstop_pass"]},
        "H4_zero_rejections": {
            "pass": h4, "rejections": rejections,
            "n_decodes": len(all_errs)},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = f"{n_pass}/{len(gates)} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in gates.items()))

    result = {
        "exp": "exp142_sign_read",
        "claim": ("the minimum semantics extension of the universal "
                  "reader — sign-preserving symmetrize (R3) + the "
                  "signed-weight rule (R1 structure on |A|, R2 signed "
                  "dynamics) — carries SIGN into the decode: fidelity on "
                  "exp137's two degraded classes, sign-flip adversarial "
                  "separation at the verdict level, and a strict-superset "
                  "in-domain control"),
        "pre_registration": {
            "signed_weight_rule": [
                "R1 structure on |A|: canon labeling labeling_bfs_n(|A|), "
                "dt = star_dt(gamma, max_i sum_j |A_ij|), frontier and BFS "
                "traversal on |A[i,j]| > 0 (the exp137-named A[i]>0 filter "
                "dropped)",
                "R2 sign in the dynamics: the coupling consumes the SIGNED "
                "matrix (GraphCollective on A as-is); no commit-time "
                "reflection is invented",
                "R3 projection: Re(W_t) -> (R+R^T)/2 -> time-average, zero "
                "diagonal (the ONLY change from exp137's |W_t| front-end); "
                "bit-identical to exp137 on all-positive real media"],
            "gates": {k: g for k, g in gates.items()},
            "dose_ladder": list(DOSES),
            "carrier_families": list(families)},
        "config": {"op": STAR_OP, "spec": "MULTI (exp94)",
                   "frontier": "walk", "seeds": list(seeds),
                   "control": "torus (exp73 battery)",
                   "probe_seed": PROBE_SEED, "k_chords": K_CHORDS},
        "control": ctrl,
        "ood": ood,
        "exp137_reference": {"signed_median": EXP137_SIGNED_MEDIAN,
                             "complex_phase_median": EXP137_COMPLEX_MEDIAN},
        "probes": {"pairs": pairs,
                   "n_pairs": len(pairs),
                   "n_probes": 2 * len(pairs),
                   "magnitude_sign_blind_pairs": n_bit_identical,
                   "separated_pairs": separated,
                   "verdict_changed_vs_magnitude": verdict_changed},
        "gates": gates,
        "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print(f"  deposited {OUT}")
    return result


if __name__ == "__main__":
    main()
