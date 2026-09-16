#!/usr/bin/env python3
"""exp145 — THE PHASE-NATIVE READ (the reactive sin(phi) channel).

FOUNDATION (exp142, 4/4 gates, deposited results/exp142_sign_read.json; the
semantics-carrying-read line exp137 L115 -> exp142): the sign-carrying read
(sign-preserving symmetrize R3, structure-on-|A| traversal R1, signed
dynamics R2) carries SIGN into the decode — signed median 0.575 (was 0.685),
complex_phase 0.525 (was 0.715), 5/12 adversarial sign-flip pairs separated
at the verdict level, torus control bit-identical (strict superset).
exp142's R3 consumes Re(W_t) = |W| cos(phi) — the phase-ALIGNED component —
and DISCARDS the reactive sin(phi) channel; that discard is an OWNED scope
note in exp142's R3, and exp142's REGISTERED NEXT (a) names exactly this:
the phase-native read. Sharpened falsification edge carried from L115: a
medium whose identity semantics live ONLY in the reactive channel should
still break the current (sign-carrying) read.

THIS EXPERIMENT closes that scope. Two medium constructions in which the
identity semantics live ONLY in the reactive (imaginary) channel:

  (1) REACTIVE BATTERY MEDIA (adversarial pairs): substrate = PURELY
      IMAGINARY ring backbone (W[i,i+1] = 1j, |W| = 1, phi = +pi/2 — a
      reactive-only substrate) + a carrier chord set C (k=6, exp142's
      F1/F2/F3 geometries verbatim) carrying W_c = a +/- i*b with
        a = 4.0  — the REAL component, BITWISE IDENTICAL across the two
                   pair members: semantically empty (class-independent),
        +/- i*b  — the REACTIVE component, whose SIGN is the latent class.
      Member P+ (class up) and P- (class down) are magnitude-identical
      (|W| bitwise equal) and real-component-identical (Re(W) bitwise
      equal); ONLY the sign of the imaginary part differs. Dose ladder
      b in {64, 128, 256, 384} x 3 families = 12 pairs.
      INSTRUMENT DISCLOSURE (pre-run): the ladder is derived from
      exp142's DEPOSITED dose response (sign-arm verdict flips at
      F1@{64,256}, F2@{64,256}, F3@{256}; no flips at 4/16 or F3@64).
      The ladder brackets upward from that deposited flip boundary and
      the b=64/256 points DOUBLE as bit-exact anchors: at those doses
      the phase-native arm's projected matrix equals exp142's sign-arm
      matrix (ring 1.0 +/- w_c) BITWISE, same executor, same seeds —
      so the deposited errs must be reproduced exactly (instrument
      validity precondition). No other calibration was run; the gates
      below were fixed before the registered run.

  (2) REACTIVE GRID CLASSES (paired conjugate media, exp137-analog soft
      media): ReactiveMedium(n, seed, s), s = +/-1 the latent class,
      built from exp137's exact helpers in SignedMedium's draw order
      (B = _base_connected(n, 0.04, rng); sigma = rng.choice(+/-1);
      w = _wU(rng, shape)):
        W = 0.5*B*w  +  i * s * B*w*sigma
      Re(W) = 0.5*B*w is the class-INDEPENDENT real component (same rng
      stream => bitwise identical across the paired classes); Im(W) =
      s*B*w*sigma carries the identity. Instance i of class up and
      class down share the SAME base seed (80_000+i, unused by exp137's
      class indices 0..5; the class index labels, it does not seed) =>
      W_down = conj(W_up) BITWISE (|W| and Re(W) identical, Im(W)
      sign-flipped): a paired-conjugate grid, 8 instances at n=100 +
      2 at n=400 (exp142's grid shape). Reactive energy fraction
      rho = ||Im W||^2/||W||^2 = 0.8 exactly (well above the branch
      threshold).

THE PHASE-NATIVE RULE (pre-registered, ONE rule, zero knobs, stated
before running; NOT per-media tuning):

  PN1 DIAGNOSTIC (fixed threshold): pool over snapshots;
      rho = sum_t ||Im W_t||_F^2 / sum_t ||W_t||_F^2.
      The medium is REACTIVE-DOMINANT iff rho >= 0.5.
  PN2 PROJECTION: if reactive-dominant, project onto the imaginary-
      phase-aligned component A_t = Im(W_t) (|W| sin(phi) carries the
      polarity); else A_t = Re(W_t) (exp142's R3 verbatim). Symmetrize
      S_t = (A_t + A_t^T)/2, time-average, zero diagonal.
  PN3 STRUCTURE + DYNAMICS: exp142's R1+R2 VERBATIM via execute_signed
      (canon/dt/traversal on |A| of the projected matrix; the coupling
      consumes the projected signed matrix). NO new executor code —
      the phase-native read is exp142's sign-read with the projection
      channel switched by PN1/PN2.
  Reduction (analytic, verified at K4): on real media (rho = 0) the
  rule takes the Re branch and is BIT-IDENTICAL to exp142's sign-read
  clause-for-clause.

ADVERSARIAL INSTRUMENT: 3 arms on every medium —
  magnitude arm: exp137's |W_t| front-end + exp94 executor verbatim
                 (the precondition read: |W| is blind by construction);
  sign arm:      exp142's R3 (Re) front-end + execute_signed (the
                 CURRENT read — predicted verdict-blind on reactive
                 media: it phase-aligns to the semantically-empty real
                 component);
  phase arm:     the PN1/PN2/PN3 rule (the extension).

PRE-REGISTERED GATES (fixed before the registered run):

  GATE-K1  (the falsification edge confirmed) the sign arm is
           VERDICT-BLIND on the reactive battery: for all 12 pairs the
           Re projections are bitwise equal across the two members and
           the sign arm's per-seed outcomes (finite errs or shared
           rejections) and majority verdicts are identical within every
           pair. The current read cannot see the latent classes.
           Supporting diagnostic (deposited, not gated): on the paired
           conjugate grid the sign arm decodes the semantically-empty
           real component (0.5*B*w, connected, healthy) and its errs
           are bitwise identical across conjugate classes at every
           seed — CONFIDENT blindness: the read reports success while
           the identity is invisible. If the sign arm DOES distinguish
           the classes (K1 fails), that is a genuine surprise — deposit
           it and re-scope.
  GATE-K2  (the phase-native rule separates) preconditions: (a) the
           magnitude arm is verdict-blind on 12/12 pairs (the pairs are
           genuinely adversarial — only the reactive channel differs);
           (b) PN1 selects the Im branch on all 24 battery members;
           (c) the exp142 anchor: phase-arm errs at b=64 and b=256
           reproduce exp142's deposited sign-arm errs BIT-EXACTLY on
           all anchored pairs. Gate: the phase arm's majority verdicts
           differ across the two members on >= 10/12 pairs.
  GATE-K3  (decode fidelity on the reactive classes) the phase arm's
           pooled median decode err over the paired conjugate grid
           (both classes, 10 instances x 3 seeds x 2 classes) is
           <= 0.60 mV (exp142's H1 bar).
  GATE-K4  (strict superset) (i) torus control (exp73 battery): the
           phase arm's final V states are BIT-IDENTICAL to the sign
           arm's at every seed and verify is preserved (rho = 0 => Re
           branch analytic); (ii) exp142's deposited signed class
           (4-instance subset, seeds 10_000+i): phase-arm errs
           BIT-IDENTICAL to the sign-arm errs at every (instance,
           seed); (iii) exp142's deposited complex_phase class
           (4-instance subset, seeds 20_000+i): uniform phases put
           rho ~= 0.5 BY CONSTRUCTION, so the branch map is deposited
           per instance; Re-branch instances must be bit-identical to
           the sign arm; the pooled phase-arm median on the subset
           must stay <= 0.63 mV (exp142's deposited complex bar). If
           the reduction is not exact on the complex class, the delta
           is OWNED and the branch point is NAMED: PN1's threshold at
           rho = 0.5 — a uniform-phase medium sits ON the boundary and
           the rule resolves it by the >= side (that boundary is the
           one knob the rule contains, fixed a priori, not tuned).

DEPOSIT: results/exp145_phase_read.json

RUN:
  python3 -m experiments.exp145_phase_read            # full (registered)
  python3 -m experiments.exp145_phase_read --smoke    # instrument check
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
from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import MULTI, labeling_bfs_n, spec_target_n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp145_phase_read.json")
EXP142 = os.path.join(ROOT, "results", "exp142_sign_read.json")

# the adversarial dose ladder (disclosure in docstring: derived from
# exp142's deposited dose response; 64/256 double as bit-exact anchors)
DOSES = (64.0, 128.0, 256.0, 384.0)
A_REAL = 4.0                    # class-independent real carrier part
A_BACKBONE = 1.0                # reactive ring magnitude (W = 1j)

# the paired conjugate grid: SHARED base seeds (80_000+i, unused by
# exp137's classes 0..5); the latent class enters ONLY through s in
# Im(W) — instance i of the two classes are bitwise conjugates
GRID_BASE_SEED = 80_000
GRID_CLASSES = {"reactive_up": 1, "reactive_down": -1}
N_INSTANCES = 8                 # at n=100
N_INSTANCES_400 = 2             # scale spot-checks

RHO_THRESHOLD = 0.5             # PN1, fixed a priori
K3_BAR = 0.60                   # exp142's H1 bar
K4_COMPLEX_BAR = 0.63           # exp142's deposited complex bar
K2_MIN_SEPARATION = 10          # of 12 pairs

FAMILIES = ("F1_zone_tail", "F2_zone_head", "F3_canon_boundary")

# conjugate-pair cache for the confident-blindness diagnostic
conj_cache: dict = {}


# ------------------------------------------- the reactive grid medium
class ReactiveMedium:
    """Paired-conjugate reactive medium: identity ONLY in Im(W).

    W = 0.5*B*w + i * s * B*w*sigma  (exp137 helpers, SignedMedium's
    draw order B -> sigma -> w). Re(W) is class-independent; instance i
    of class up/down with the same base seed are bitwise conjugates."""

    kind = "reactive"

    def __init__(self, n: int, seed: int, s: int):
        rng = np.random.default_rng(seed)
        B = _base_connected(n, 0.04, rng)
        sigma = rng.choice((-1.0, 1.0), size=B.shape)
        w = _wU(rng, B.shape)
        self.s = int(s)
        self.W = 0.5 * B * w + 1j * (s * B * w * sigma)

    def snapshots(self):
        return [self.W]

    def native_support(self) -> np.ndarray:
        return (np.abs(self.W) > 0).astype(float)


# --------------------------------------- PN1 + PN2: the one new rule
def reactive_fraction(medium) -> float:
    """PN1 — pooled reactive energy fraction (fixed threshold 0.5)."""
    num = den = 0.0
    for W in medium.snapshots():
        num += float(np.sum(np.imag(W) ** 2))
        den += float(np.sum(np.abs(W) ** 2))
    return num / den if den > 0 else 0.0


def project_phase_native(medium) -> tuple[np.ndarray, float, str]:
    """PN1 + PN2 — ONE rule: the dominant-quadrature projection.
    rho >= 0.5 -> Im branch; else Re branch (exp142's R3 verbatim)."""
    rho = reactive_fraction(medium)
    branch = "imag" if rho >= RHO_THRESHOLD else "real"
    snaps = medium.snapshots()
    acc = None
    for W in snaps:
        R = np.imag(W) if branch == "imag" else np.real(W)
        S = (R + R.T) / 2.0
        acc = S if acc is None else acc + S
    A = acc / len(snaps)
    np.fill_diagonal(A, 0.0)
    return A, rho, branch


def read_phase(medium, seed: int, return_state: bool = False) -> dict:
    """The phase-native arm: PN1/PN2 projection + exp142's executor
    verbatim (same rejection policy as read_sign)."""
    with warnings_as_errors():
        A, rho, branch = project_phase_native(medium)
        assert not np.iscomplexobj(A), "PN2 must deliver a real matrix"
        out = execute_signed(MULTI, A, seed, op=STAR_OP,
                             return_state=return_state)
    out["rho"] = rho
    out["branch"] = branch
    return out


class warnings_as_errors:
    """exp142's warnings-as-errors policy (context manager)."""

    def __enter__(self):
        import warnings
        self._cm = warnings.catch_warnings()
        self._cm.__enter__()
        warnings.simplefilter("error")
        return self

    def __exit__(self, *exc):
        return self._cm.__exit__(*exc)


# ------------------------------------- the reactive battery pair
def probe_pair_reactive(n: int, family: str, b: float,
                        seed: int) -> tuple[np.ndarray, np.ndarray, list]:
    """One adversarial reactive pair: (W_up, W_down) magnitude-identical
    and real-component-identical, differing ONLY in the sign of the
    imaginary carrier on the chord set C. Geometry = exp142's
    probe_pair verbatim (computed on the REAL ring's canon — labeling
    is phase-blind by construction); the substrate ring itself is
    purely imaginary (W = 1j), so the whole medium is reactive-only."""
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
    Wp = 1j * A.copy()
    Wm = 1j * A.copy()
    for i, j in chords:
        Wp[i, j] = Wp[j, i] = A_REAL + 1j * b      # class up:  +pi/2
        Wm[i, j] = Wm[j, i] = A_REAL - 1j * b      # class down: -pi/2
    assert np.array_equal(np.abs(Wp), np.abs(Wm)), \
        "pair members must be magnitude-identical"
    assert np.array_equal(np.real(Wp), np.real(Wm)), \
        "pair members must be real-component-identical"
    return Wp, Wm, chords


# ------------------------------------------------------------ helpers
def decode(arm: str, medium, seed: int,
           return_state: bool = False) -> dict:
    """Dispatch one decode; a rejection is RECORDED, never raised
    (exp142's zero-rejection hygiene; the caller counts)."""
    if arm == "mag":
        fn = lambda med, s, st: read_mag(project_magnitude(med), s, st)
    elif arm == "sign":
        fn = lambda med, s, st: read_sign(project_signed(med), s, st)
    elif arm == "phase":
        fn = read_phase
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


def load_exp142_anchors() -> dict | None:
    if not os.path.exists(EXP142):
        return None
    with open(EXP142) as f:
        d = json.load(f)
    anchors = {}
    for rec in d.get("probes", {}).get("pairs", []):
        anchors[(rec["family"], rec["dose"])] = {
            "+": rec["arms"]["sign+"].get("errs"),
            "-": rec["arms"]["sign-"].get("errs"),
        }
    return anchors


def native_target(medium, n: int) -> np.ndarray:
    return spec_target_n(MULTI, labeling_bfs_n(medium.native_support()), n)


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 instance/class, 1 seed, "
                         "F1 only at one dose")
    args = ap.parse_args()
    n_inst = 1 if args.smoke else N_INSTANCES
    n_inst400 = 1 if args.smoke else N_INSTANCES_400
    seeds = (1,) if args.smoke else SEEDS
    fams = FAMILIES[:1] if args.smoke else FAMILIES
    doses = DOSES[:1] if args.smoke else DOSES
    t0 = time.time()
    print("=== exp145: THE PHASE-NATIVE READ (reactive channel) ===\n")

    rejections = 0
    conj_cache.clear()
    anchors = None if args.smoke else load_exp142_anchors()
    gates = {}

    # ---- GATE-K4(i): torus control — bit-exact reduction to exp142
    ctrl: dict = {"substrate": "torus"}
    bit_ok, verify_ok = True, True
    sign_errs, phase_errs, mag_errs = [], [], []
    for s in seeds:
        m = _StaticMedium(make_battery()["torus"])
        out_s = decode("sign", m, s, return_state=True)
        out_p = decode("phase", m, s, return_state=True)
        out_m = decode("mag", m, s)
        rejections += sum(1 for r in (out_s, out_p, out_m) if not r["ok"])
        sign_errs.append(out_s.get("err"))
        phase_errs.append(out_p.get("err"))
        mag_errs.append(out_m.get("err"))
        same = (out_s["ok"] and out_p["ok"] and np.array_equal(
            np.asarray(out_s["state"]["V"]),
            np.asarray(out_p["state"]["V"])))
        bit_ok &= bool(same)
        verify_ok &= (out_s.get("verified") == out_p.get("verified"))
    ctrl.update(sign_errs=sign_errs, phase_errs=phase_errs,
                mag_errs=mag_errs, bit_identical=bool(bit_ok),
                verify_preserved=bool(verify_ok),
                rho=reactive_fraction(
                    _StaticMedium(make_battery()["torus"])))
    print(f"  K4 torus: bit-identical {bit_ok} verify_preserved "
          f"{verify_ok} errs sign {sign_errs} phase {phase_errs}")

    # ---- GATE-K4(ii)/(iii): exp142's deposited classes, subset
    k4_classes: dict = {}
    for kind, cls, ref_ci in (("signed", SignedMedium, 1),
                              ("complex_phase", ComplexMedium, 2)):
        recs, branches = [], []
        bit_identical = 0
        n_cmp = 0
        errs_phase = []
        for i in range(4):                    # n=100 subset
            med = cls(100, seed=10_000 * ref_ci + i)
            rho = reactive_fraction(med)
            branches.append(rho >= RHO_THRESHOLD)
            for s in seeds:
                out_s = decode("sign", med, s)
                out_p = decode("phase", med, s)
                rejections += sum(1 for r in (out_s, out_p) if not r["ok"])
                same = (out_s["ok"] and out_p["ok"]
                        and out_s["err"] == out_p["err"]
                        and out_s["verified"] == out_p["verified"])
                bit_identical += int(same)
                n_cmp += 1
                if out_p["ok"]:
                    errs_phase.append(out_p["err"])
                recs.append({"i": i, "seed": s, "rho": round(rho, 4),
                             "branch": "imag" if rho >= RHO_THRESHOLD
                             else "real",
                             "sign_err": out_s.get("err"),
                             "phase_err": out_p.get("err"),
                             "bit_identical": bool(same)})
        med = float(np.median(errs_phase)) if errs_phase else None
        re_branch_all_bit = all(
            r["bit_identical"] for r in recs if r["branch"] == "real")
        k4_classes[kind] = {
            "instances": recs,
            "branch_map_imag": [i for i, b in enumerate(branches) if b],
            "bit_identical_pairs": bit_identical,
            "n_pairs": n_cmp,
            "re_branch_all_bit_identical": bool(re_branch_all_bit),
            "phase_median": med,
            "bar": K4_COMPLEX_BAR if kind == "complex_phase" else None,
        }
        print(f"  K4 {kind:14s} bit-identical {bit_identical}/{n_cmp} "
              f"imag-branch instances {k4_classes[kind]['branch_map_imag']} "
              f"phase median {med}")

    # ---- GATE-K3: the paired conjugate reactive grid
    grid: dict = {}
    grid_errs: list[float] = []
    conj_blind = 0
    conj_cmp = 0
    for cls_name, s_cls in GRID_CLASSES.items():
        inst_rec, errs, errs_native, oks = [], [], [], []
        for i in range(n_inst + n_inst400):
            n = 400 if i >= n_inst else 100
            med = ReactiveMedium(n, seed=GRID_BASE_SEED + i, s=s_cls)
            A_nat = native_target(med, n)
            for s in seeds:
                out_p = decode("phase", med, s, return_state=True)
                out_s = decode("sign", med, s)
                rejections += sum(1 for r in (out_p, out_s) if not r["ok"])
                rec = {"n": n, "seed": s,
                       "rho": round(out_p.get("rho", float("nan")), 4),
                       "branch": out_p.get("branch")}
                if out_p["ok"]:
                    V = np.asarray(out_p["state"]["V"])
                    err_nat = float(np.sqrt(np.mean((V - A_nat) ** 2)))
                    errs.append(out_p["err"])
                    errs_native.append(err_nat)
                    oks.append(out_p["verified"])
                    grid_errs.append(out_p["err"])
                    rec.update(err=out_p["err"],
                               err_native=round(err_nat, 2),
                               verified=out_p["verified"])
                else:
                    rec["rejection"] = out_p["rejection"]
                # the confident-blindness diagnostic: sign arm identical
                # across conjugate classes (paired base seeds)
                if cls_name == "reactive_up":
                    conj_cache[(n, i, s)] = out_s
                else:
                    twin = conj_cache.get((n, i, s))
                    if twin is not None:
                        conj_cmp += 1
                        conj_blind += int(outcome_key(twin)
                                          == outcome_key(out_s))
                inst_rec.append(rec)
        grid[cls_name] = {
            "instances": inst_rec,
            "phase_median": float(np.median(errs)) if errs else None,
            "phase_max": float(np.max(errs)) if errs else None,
            "err_native_median": (float(np.median(errs_native))
                                  if errs_native else None),
            "verify_rate": float(np.mean(oks)) if oks else None,
        }
        print(f"  K3 {cls_name:14s} phase median "
              f"{grid[cls_name]['phase_median']} "
              f"verify {grid[cls_name]['verify_rate']}")

    # ---- GATE-K1 / GATE-K2: the reactive adversarial battery
    pairs: list[dict] = []
    n_blind_sign = n_blind_mag = 0
    separated, anchored, anchor_ok = [], 0, True
    for fam in fams:
        for b in doses:
            Wp, Wm, chords = probe_pair_reactive(100, fam, b, PROBE_SEED)
            rec = {"family": fam, "dose": b, "n_chords": len(chords)}
            arms: dict = {}
            for name, W in (("up", Wp), ("down", Wm)):
                med = _StaticMedium(W)
                for arm in ("mag", "sign", "phase"):
                    errs, vs, keys = [], [], []
                    for s in seeds:
                        out = decode(arm, med, s)
                        rejections += 0 if out["ok"] else 1
                        errs.append(out.get("err"))
                        vs.append(bool(out.get("verified", False)))
                        keys.append(outcome_key(out))
                    arms[(name, arm)] = {"errs": errs, "verify": vs,
                                         "keys": keys,
                                         "majority": bool(np.mean(vs) > 0.5)}
            rec["arms"] = {
                f"{name}_{arm}": {"errs": v["errs"],
                                  "verify": [int(x) for x in v["verify"]],
                                  "majority": v["majority"]}
                for (name, arm), v in arms.items()}
            # (a) magnitude arm must be sign-blind (adversarial validity)
            blind_mag = (arms[("up", "mag")]["keys"]
                         == arms[("down", "mag")]["keys"])
            rec["magnitude_blind"] = bool(blind_mag)
            n_blind_mag += int(blind_mag)
            # (b) K1: the sign arm (exp142's read) must be verdict-blind
            proj_same = np.array_equal(project_signed(_StaticMedium(Wp)),
                                       project_signed(_StaticMedium(Wm)))
            blind_sign = bool(proj_same and
                              arms[("up", "sign")]["keys"]
                              == arms[("down", "sign")]["keys"] and
                              arms[("up", "sign")]["majority"]
                              == arms[("down", "sign")]["majority"])
            rec["re_projection_bit_identical"] = bool(proj_same)
            rec["sign_verdict_blind"] = blind_sign
            n_blind_sign += int(blind_sign)
            # (c) K2: the phase arm separates the latent classes
            sep = (arms[("up", "phase")]["majority"]
                   != arms[("down", "phase")]["majority"])
            rec["phase_separated"] = bool(sep)
            rec["rho_up"] = round(reactive_fraction(_StaticMedium(Wp)), 4)
            if sep:
                separated.append(f"{fam}@{b:g}")
            # (d) the exp142 bit-exact anchor at deposited doses
            if anchors is not None and (fam, b) in anchors:
                anch = anchors[(fam, b)]
                got_p = arms[("up", "phase")]["errs"]
                got_m = arms[("down", "phase")]["errs"]
                ok = (anch["+"] is not None and anch["-"] is not None
                      and got_p == anch["+"] and got_m == anch["-"])
                rec["exp142_anchor"] = {"expected+": anch["+"],
                                        "expected-": anch["-"],
                                        "match": bool(ok)}
                anchored += 1
                anchor_ok &= bool(ok)
            pairs.append(rec)
            print(f"  K1/K2 {fam:17s} b={b:6.1f} magBlind={blind_mag} "
                  f"signBlind={blind_sign} "
                  f"phase up{arms[('up', 'phase')]['errs']}"
                  f"V{int(arms[('up', 'phase')]['majority'])} "
                  f"down{arms[('down', 'phase')]['errs']}"
                  f"V{int(arms[('down', 'phase')]['majority'])}"
                  + ("  <== SEPARATED" if sep else ""))

    # ---- gates
    n_pairs = len(pairs)
    gates["K1_sign_read_fails_reactive"] = {
        "pass": bool(n_pairs > 0 and n_blind_sign == n_pairs),
        "n_pairs": n_pairs,
        "sign_verdict_blind_pairs": n_blind_sign,
        "grid_confident_blind": {"conjugate_outcome_identical":
                                 conj_blind, "n_compared": conj_cmp},
    }
    precond = bool(n_blind_mag == n_pairs and anchor_ok
                   and anchored > 0)
    n_sep = len(separated)
    gates["K2_phase_native_separates"] = {
        "pass": bool(precond and n_sep >= K2_MIN_SEPARATION),
        "preconditions": {"magnitude_blind_pairs": n_blind_mag,
                          "exp142_anchor_pairs": anchored,
                          "anchor_bit_exact": bool(anchor_ok)},
        "separated_pairs": separated,
        "n_separated": n_sep,
        "required": K2_MIN_SEPARATION,
    }
    g3 = float(np.median(grid_errs)) if grid_errs else None
    gates["K3_reactive_fidelity"] = {
        "pass": bool(g3 is not None and g3 <= K3_BAR),
        "pooled_phase_median": g3, "bar": K3_BAR,
        "n_decodes": len(grid_errs),
    }
    k4 = bool(bit_ok and verify_ok
              and k4_classes["signed"]["bit_identical_pairs"]
              == k4_classes["signed"]["n_pairs"]
              and k4_classes["complex_phase"]["re_branch_all_bit_identical"]
              and k4_classes["complex_phase"]["phase_median"] is not None
              and k4_classes["complex_phase"]["phase_median"]
              <= K4_COMPLEX_BAR)
    gates["K4_strict_superset"] = {
        "pass": bool(k4),
        "torus_bit_identical": bool(bit_ok),
        "torus_verify_preserved": bool(verify_ok),
        "signed_bit_identical": k4_classes["signed"]["bit_identical_pairs"],
        "signed_pairs": k4_classes["signed"]["n_pairs"],
        "complex_re_branch_bit_identical":
            k4_classes["complex_phase"]["re_branch_all_bit_identical"],
        "complex_phase_median":
            k4_classes["complex_phase"]["phase_median"],
        "complex_bar": K4_COMPLEX_BAR,
        "complex_branch_map_imag":
            k4_classes["complex_phase"]["branch_map_imag"],
        "branch_point": ("PN1 threshold rho >= 0.5: uniform-phase media "
                         "sit on the boundary; the rule resolves by the "
                         ">= side (fixed a priori, not tuned)"),
    }

    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = f"{n_pass}/{len(gates)} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in gates.items()))
    print(f"  rejections: {rejections}")

    result = {
        "exp": "exp145_phase_read",
        "claim": (
            "the phase-native read — PN1 (pooled reactive energy "
            "fraction rho >= 0.5) + PN2 (imaginary-phase-aligned "
            "projection for reactive-dominant media, exp142's R3 "
            "otherwise) + PN3 (exp142's R1+R2 executor verbatim) — "
            "consumes the reactive sin(phi) channel exp142's sign-read "
            "discards: verdict-blind adversarial separation where the "
            "current read is blind, verdict-level separation of purely "
            "reactive latent classes, exp142-bar fidelity on paired "
            "conjugate reactive classes, and a bit-exact reduction to "
            "the sign-read wherever the medium is not reactive-dominant"),
        "pre_registration": {
            "phase_native_rule": [
                "PN1 diagnostic: rho = sum_t ||Im W_t||_F^2 / "
                "sum_t ||W_t||_F^2 pooled over snapshots; "
                "reactive-dominant iff rho >= 0.5 (fixed a priori)",
                "PN2 projection: Im branch A_t = Im(W_t) if "
                "reactive-dominant else Re branch A_t = Re(W_t) "
                "(exp142 R3 verbatim); symmetrize, time-average, "
                "zero diagonal",
                "PN3 structure+dynamics: exp142's R1+R2 via "
                "execute_signed VERBATIM — no new executor code"],
            "media": {
                "battery": ("purely imaginary ring (W = 1j) + carrier "
                            "a +/- i*b with a = 4.0 class-independent "
                            "(semantically empty), class = sign of the "
                            "imaginary carrier"),
                "grid": ("paired conjugates W = 0.5*B*w + i*s*B*w*sigma "
                         "(exp137 helpers, SignedMedium draw order); "
                         "SHARED base seeds 80_000+i — the class enters "
                         "only through s in Im(W), so instance i of the "
                         "two classes are bitwise conjugates"),
            },
            "dose_ladder": list(DOSES),
            "ladder_disclosure": (
                "derived from exp142's deposited dose response "
                "(flips at F1@{64,256}, F2@{64,256}, F3@{256}; none at "
                "4/16/F3@64); b=64/256 double as bit-exact anchors"),
            "gates": gates,
        },
        "config": {"op": STAR_OP, "spec": "MULTI (exp94)",
                   "frontier": "walk", "seeds": list(seeds),
                   "control": "torus (exp73 battery)",
                   "probe_seed": PROBE_SEED, "k_chords": K_CHORDS,
                   "rho_threshold": RHO_THRESHOLD,
                   "a_real": A_REAL},
        "control": ctrl,
        "k4_classes": k4_classes,
        "grid": grid,
        "probes": {"pairs": pairs, "n_pairs": n_pairs,
                   "magnitude_blind_pairs": n_blind_mag,
                   "sign_verdict_blind_pairs": n_blind_sign,
                   "separated_pairs": separated,
                   "n_separated": n_sep},
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
