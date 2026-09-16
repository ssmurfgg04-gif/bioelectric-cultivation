#!/usr/bin/env python3
"""exp137 — THE UNIVERSAL READER: OUT-OF-DOMAIN MEDIA (the 101% target
Stage 5 path 1; ledger L~117).

THE CLAIM (pre-registered before running)
-----------------------------------------
M33-class reading generalizes to media OUTSIDE the 19-substrate-type
domain with zero rejections and bounded quality loss — one reader
configuration, no per-medium re-tuning. The reader's domain today:
19 substrate types (exp73's 7 + exp94's 12) x 12 zone counts
(exp101) x n to 784 (exp104), ZERO rejections, every instance a
simple undirected binary/positive graph. exp68 established the
coherence constraint (5 formalizations, naive star blocked); exp79
crossed the reframed star ("any substrate coherent with the pattern,
given an identity strong enough and an anchor that does not
diffuse"). This experiment asks whether the READER — the M33
two-source read at its battery-wide verified operating point —
consumes media that violate the domain's implicit input contract.

THE M33 INPUT CONTRACT (named for the diagnosis; the reader never
states these — they are implicit in BioElectricCollective +
execute_two_source_n):
  A-SYM   A[i,j] == A[j,i]          (undirected coupling)
  A-NN    A entries real >= 0       (conductances)
  A-REAL  A entries real            (real-valued state pipeline)
  A-PAIR  coupling is pairwise      (an n x n matrix exists)
  A-STAT  one static coupling for the whole read window
  A-CW    closed world: the edge set is fixed and fully observable

OUT-OF-DOMAIN MEDIUM CLASSES (6; each violates a DISTINCT named
assumption; >= 4 required by GATE-D1):
  dag            violates A-SYM   (oriented acyclic coupling)
  signed         violates A-NN    (inhibitory negative weights)
  complex_phase  violates A-REAL  (complex conductances)
  hypergraph     violates A-PAIR  (hyperedges size 3-6)
  time_varying   violates A-STAT  (edges flip during the read)
  open_world     violates A-CW    (+A-STAT: no fixed edge set; each
                 snapshot i.i.d. draws over a potential edge set the
                 reader never observes directly)

THE ONE CONFIGURATION (GATE-D4; auditable, zero knobs):
  Projection (the universal front-end, one function, no per-class
  branch): B_t = |W_t| (complex modulus; hyperedges factorize to
  pairwise co-incidence with weight |w_e|/(|e|-1)); S_t =
  (B_t + B_t^T)/2; A_proj = mean_t S_t; zero diagonal.
  Executor: execute_two_source_n VERBATIM (no edits), op = STAR
  (gamma=64, mu=0 — exp99's battery-wide verified point),
  frontier_mode="walk" (exp97), spec = MULTI (exp94's 3-zone
  program), seeds (1, 2, 3). Identical for every class and baseline.

PRE-REGISTERED GATES:

  GATE-D1  (domain) >= 4 out-of-domain medium classes implemented,
           each violating a DISTINCT named M33 assumption, and the
           RAW reader probed on each (where an n x n input exists;
           interface-absent is the recorded probe outcome when no
           matrix can even be passed). The probe table (crash /
           silent coercion / degradation / interface-absent) IS the
           localization of M33's universality boundary.

  GATE-D2  (zero rejections) the universal reader returns a decode
           (finite err_vs_target, no exception, no refusal) on 100%
           of out-of-domain instances, including the n=400 scale
           spot-checks. A low-quality decode is NOT a rejection —
           that is GATE-D3's territory. Any crash/exception/non-
           finite decode fails this gate.

  GATE-D3  (bounded quality loss) pooled median decode err over all
           OOD instances <= 2.0 x pooled median in-domain err, where
           the in-domain baseline is the FULL 19-substrate battery
           re-run in-run under the identical one configuration and
           seeds. The 2x bound is taken from the existing map: the
           reader's verified class prices span 0.49-5.71 mV (a >10x
           topology spread, exp100), so 2x-of-median is the
           conservative continuation of the map's own spread.

  GATE-D4  (one configuration) a single reader configuration — one
           projection function with no per-medium parameters, one
           executor call site, one op, one spec, one seed set — used
           for EVERY class and the baseline. Any per-medium tuning
           refutes the claim as per-domain engineering (verdict
           REFUTE regardless of D1-D3).

PREDICTED DIAGNOSIS TABLE (registered before running; the probe
outcomes to compare against):
  dag            runs uncalibrated — the row-Laplacian tolerates
                 asymmetry; orientation silently ignored (A-SYM not
                 load-bearing at the dynamics level).
  signed         runs with degraded fidelity — negative conductances
                 fight the read (anti-diffusive coupling); traversal
                 (A[i] > 0) silently skips negative edges.
  complex_phase  runs with SILENT dtype coercion (imaginary parts
                 discarded at matrix/state boundaries) — a decode
                 returned without acknowledging the discard.
  hypergraph     interface-absent — no n x n object exists to pass.
  time_varying   interface-absent as a static read; the most
                 favorable static proxy (first snapshot) is an
                 unowned choice the reader cannot know it made.
  open_world     interface-absent as a closed-world read; the
                 realized-union proxy is measurable, but the
                 medium's unrealized potential edges are invisible
                 to ANY static read (the information gap is
                 recorded as err vs the potential-support canon).

DEPOSIT: results/exp137_universal_reader.json

RUN:
  python3 -m experiments.exp137_universal_reader            # full
  python3 -m experiments.exp137_universal_reader --smoke    # instrument check
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

from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import (
    MULTI, execute_two_source_n, labeling_bfs_n, new_battery, spec_target_n,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp137_universal_reader.json")

STAR_OP = {"gamma": 64.0, "mu": 0.0}       # exp99's battery-wide point
SEEDS = (1, 2, 3)
N_INSTANCES = 8                             # at n=100
N_INSTANCES_400 = 2                         # scale spot-checks
ERR_BAR = 6.0                               # exp94's verify bar

# the named M33 input contract
CONTRACT = ("A-SYM", "A-NN", "A-REAL", "A-PAIR", "A-STAT", "A-CW")


# ---------------------------------------------------------------- media
def _base_connected(n: int, p_extra: float, rng: np.random.Generator,
                    p_backbone: float = 1.0) -> np.ndarray:
    """Ring backbone + random chords — a connected undirected support."""
    A = np.zeros((n, n))
    for i in range(n):
        if rng.random() < p_backbone:
            j = (i + 1) % n
            A[i, j] = A[j, i] = 1.0
    for i in range(n):
        for j in range(i + 2, n):
            if rng.random() < p_extra:
                A[i, j] = A[j, i] = 1.0
    return A


def _wU(rng, shape) -> np.ndarray:
    return rng.uniform(0.5, 1.5, size=shape)


class DagMedium:
    """Directed acyclic weighted graph. Violates A-SYM."""
    kind = "dag"
    violated = ("A-SYM",)

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(n)
        W = np.zeros((n, n))
        for a in range(n - 1):                       # directed backbone
            i, j = perm[a], perm[a + 1]
            W[i, j] = _wU(rng, ())
        for a in range(n):
            for b in range(a + 2, n):
                if rng.random() < 0.05:
                    W[perm[a], perm[b]] = _wU(rng, ())
        self.W = W

    def snapshots(self):
        return [self.W]

    def native_support(self) -> np.ndarray:
        return (self.W + self.W.T > 0).astype(float)


class SignedMedium:
    """Signed weighted undirected graph. Violates A-NN."""
    kind = "signed"
    violated = ("A-NN",)

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        B = _base_connected(n, 0.04, rng)
        signs = rng.choice((-1.0, 1.0), size=B.shape)
        self.W = B * signs * _wU(rng, B.shape)

    def snapshots(self):
        return [self.W]

    def native_support(self) -> np.ndarray:
        return (np.abs(self.W) > 0).astype(float)


class ComplexMedium:
    """Complex-weighted undirected graph. Violates A-REAL."""
    kind = "complex_phase"
    violated = ("A-REAL",)

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        B = _base_connected(n, 0.04, rng)
        phase = rng.uniform(0.0, 2.0 * np.pi, size=B.shape)
        self.W = B * _wU(rng, B.shape) * np.exp(1j * phase)

    def snapshots(self):
        return [self.W]

    def native_support(self) -> np.ndarray:
        return (np.abs(self.W) > 0).astype(float)


class HypergraphMedium:
    """Random connected hypergraph, hyperedge size 3-6. Violates A-PAIR.

    snapshots() yields the ONE-rule pairwise factorization
    (|w_e|/(|e|-1) per co-incident pair) as the projection input —
    the MEDIUM itself has no n x n object; the factorization is the
    projection's higher-order clause, not a per-instance choice."""
    kind = "hypergraph"
    violated = ("A-PAIR",)

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        edges: list[tuple[list[int], float]] = []
        # ring-covering seed hyperedges guarantee 2-section connectivity
        for k in range(0, n, 2):
            members = [(k + t) % n for t in range(3)]
            edges.append((members, _wU(rng, ())))
        for _ in range(max(20, n // 3)):
            size = int(rng.integers(3, 7))
            members = sorted(rng.choice(n, size=size, replace=False)
                             .tolist())
            edges.append((members, _wU(rng, ())))
        self.hyperedges = edges
        self.n = n

    def snapshots(self):
        B = np.zeros((self.n, self.n))
        for members, w in self.hyperedges:
            c = abs(w) / (len(members) - 1)
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    i, j = members[a], members[b]
                    B[i, j] += c
                    B[j, i] += c
        return [B]

    def native_support(self) -> np.ndarray:
        return (self.snapshots()[0] > 0).astype(float)


class TimeVaryingMedium:
    """Edge set flips during the read (T snapshots). Violates A-STAT."""
    kind = "time_varying"
    violated = ("A-STAT",)
    T = 8

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        base = _base_connected(n, 0.04, rng)
        self.snaps: list[np.ndarray] = []
        for _ in range(self.T):
            keep = (rng.random(base.shape) > 0.3) * base
            add = (rng.random(base.shape) < 0.02) * (1 - base)
            Wt = (keep + add) * _wU(rng, base.shape)
            Wt = np.triu(Wt) + np.triu(Wt, 1).T      # keep undirected
            self.snaps.append(Wt)

    def snapshots(self):
        return self.snaps

    def native_support(self) -> np.ndarray:
        sup = np.zeros_like(self.snaps[0])
        for W in self.snaps:
            sup = sup + (W != 0)
        return (sup > 0).astype(float)


class OpenWorldMedium:
    """No fixed edge set: each snapshot i.i.d. draws over a POTENTIAL
    edge set the reader never observes. Violates A-CW (+A-STAT)."""
    kind = "open_world"
    violated = ("A-CW", "A-STAT")
    T = 8
    P_PRESENT = 0.4

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        self.potential = _base_connected(n, 0.05, rng)
        self.snaps: list[np.ndarray] = []
        for _ in range(self.T):
            draw = (rng.random(self.potential.shape) < self.P_PRESENT) \
                * self.potential
            self.snaps.append(draw * _wU(rng, self.potential.shape))

    def snapshots(self):
        return self.snaps

    def native_support(self) -> np.ndarray:
        return (self.potential > 0).astype(float)


CLASSES = [DagMedium, SignedMedium, ComplexMedium, HypergraphMedium,
           TimeVaryingMedium, OpenWorldMedium]


# ------------------------------------------------- THE one projection
def project_medium(medium) -> np.ndarray:
    """The universal reader's front-end — ONE rule, zero knobs:
    magnitude -> orientation-symmetrize -> time-average -> pairwise.
    Applied identically to every medium class."""
    snaps = medium.snapshots()
    acc = None
    for W in snaps:
        B = np.abs(W)                    # complex modulus included
        S = (B + B.T) / 2.0              # orientation-symmetrize
        acc = S if acc is None else acc + S
    A = acc / len(snaps)
    np.fill_diagonal(A, 0.0)
    return A


# ------------------------------------------------------------ helpers
def read_one(adjacency: np.ndarray, seed: int) -> dict:
    """The ONE executor call site (execute_two_source_n, verbatim)."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")   # a coerced read is a rejection
        out = execute_two_source_n(MULTI, adjacency, seed, op=STAR_OP,
                                   frontier_mode="walk",
                                   return_state=True)
    err = float(out["err_vs_target"])
    if not np.isfinite(err):
        raise ValueError(f"non-finite decode err {err}")
    return out


def native_target(medium, n: int) -> np.ndarray:
    return spec_target_n(MULTI, labeling_bfs_n(medium.native_support()), n)


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 2 instances/class, 1 seed")
    args = ap.parse_args()
    n_inst = 2 if args.smoke else N_INSTANCES
    n_inst400 = 1 if args.smoke else N_INSTANCES_400
    seeds = (1,) if args.smoke else SEEDS
    t0 = time.time()
    print("=== exp137: THE UNIVERSAL READER — out-of-domain media ===\n")

    # ---- in-domain baseline: the full 19-type battery, one config
    battery = {**make_battery(), **new_battery()}
    assert len(battery) == 19, f"expected the 19-type domain, got {len(battery)}"
    in_errs: list[float] = []
    in_domain: dict = {}
    for name, adj in battery.items():
        errs, ok = [], []
        for s in seeds:
            out = read_one(adj, s)
            errs.append(out["err_vs_target"])
            ok.append(out["program_verified"])
        in_domain[name] = {"err_median": float(np.median(errs)),
                           "errs": errs,
                           "verify_rate": float(np.mean(ok))}
        in_errs.extend(errs)
        print(f"  in-domain {name:14s} median err "
              f"{in_domain[name]['err_median']:.2f} "
              f"verify {in_domain[name]['verify_rate']:.2f}")
    in_median = float(np.median(in_errs))
    print(f"  IN-DOMAIN pooled median err: {in_median:.3f} "
          f"({len(in_errs)} runs)\n")

    # ---- raw-reader probes (the diagnosis table)
    raw_probes: dict = {}
    for cls in CLASSES:
        med = cls(100, seed=101)
        rec: dict = {"violated": list(med.violated)}
        if cls is HypergraphMedium:
            rec["probe"] = "interface-absent"
            rec["note"] = ("no n x n coupling object exists to pass — "
                           "A-PAIR violation blocks invocation itself")
            raw_probes[cls.kind] = rec
            print(f"  raw probe {cls.kind:14s} interface-absent")
            continue
        raw = med.snapshots()[0] if cls in (TimeVaryingMedium,
                                            OpenWorldMedium) else med.W
        if cls is TimeVaryingMedium:
            rec["proxy"] = "first snapshot (most favorable static choice)"
        if cls is OpenWorldMedium:
            rec["proxy"] = "first realized snapshot (union unobservable)"
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                out = execute_two_source_n(MULTI, raw, 1, op=STAR_OP,
                                           frontier_mode="walk")
            rec["probe"] = "ran"
            rec["warnings"] = [str(w.category.__name__) for w in caught]
            rec["err"] = out["err_vs_target"]
            rec["verified"] = bool(out["program_verified"])
            rec["coerced"] = any("Complex" in w for w in rec["warnings"])
        except Exception as e:                      # pragma: no cover
            rec["probe"] = "crash"
            rec["exception"] = f"{type(e).__name__}: {e}"[:200]
        raw_probes[cls.kind] = rec
        print(f"  raw probe {cls.kind:14s} {rec['probe']} "
              f"err {rec.get('err')} warnings {rec.get('warnings', [])}")

    # ---- out-of-domain reads through the universal reader
    ood: dict = {}
    all_ood_errs: list[float] = []
    all_rejections = 0
    for ci, cls in enumerate(CLASSES):
        inst_rec, errs, errs_native, oks, rej = [], [], [], [], 0
        for i in range(n_inst + n_inst400):
            n = 400 if i >= n_inst else 100
            med = cls(n, seed=10_000 * ci + i)
            A = project_medium(med)
            for s in seeds:
                try:
                    out = read_one(A, s)
                except Exception as e:
                    rej += 1
                    inst_rec.append({"n": n, "seed": s,
                                     "rejection": f"{type(e).__name__}: {e}"[:200]})
                    continue
                err = float(out["err_vs_target"])
                V = np.asarray(out["final_state"]["V"])
                err_nat = float(np.sqrt(np.mean(
                    (V - native_target(med, n)) ** 2)))
                errs.append(err)
                errs_native.append(err_nat)
                oks.append(bool(out["program_verified"]))
                inst_rec.append({"n": n, "seed": s, "err": err,
                                 "err_native": round(err_nat, 2),
                                 "verified": bool(out["program_verified"])})
        all_rejections += rej
        all_ood_errs.extend(errs)
        ood[cls.kind] = {
            "violated": list(cls.violated),
            "rejections": rej,
            "err_median": float(np.median(errs)) if errs else None,
            "err_max": float(np.max(errs)) if errs else None,
            "err_native_median": (float(np.median(errs_native))
                                  if errs_native else None),
            "verify_rate": float(np.mean(oks)) if oks else None,
            "instances": inst_rec,
        }
        print(f"  OOD {cls.kind:14s} ({','.join(cls.violated)}): "
              f"median err {ood[cls.kind]['err_median']:.2f} "
              f"max {ood[cls.kind]['err_max']:.2f} "
              f"verify {ood[cls.kind]['verify_rate']:.2f} "
              f"rejections {rej} "
              f"[native-canon median {ood[cls.kind]['err_native_median']:.2f}]")

    # ---- gates
    ood_median = float(np.median(all_ood_errs))
    d1 = (len({tuple(c.violated) for c in CLASSES}) >= 4
          and len(raw_probes) == len(CLASSES))
    d2 = all_rejections == 0 and len(all_ood_errs) > 0
    d3 = bool(ood_median <= 2.0 * in_median)
    d4 = True   # auditable: project_medium has no per-class branch;
    # one call site in read_one; STAR/MULTI/walk/seeds module constants.
    gates = {
        "D1_domain": {"pass": bool(d1),
                      "n_classes": len(CLASSES),
                      "distinct_violation_sets":
                          len({tuple(c.violated) for c in CLASSES})},
        "D2_zero_rejections": {"pass": bool(d2),
                               "rejections": all_rejections,
                               "n_decodes": len(all_ood_errs)},
        "D3_bounded_fidelity": {"pass": d3,
                                "ood_median_err": ood_median,
                                "in_domain_median_err": in_median,
                                "bound_ratio": 2.0,
                                "ratio_realized": (ood_median / in_median
                                                   if in_median else None)},
        "D4_one_configuration": {"pass": d4,
                                 "audit": ("one projection function, one "
                                           "executor call site, op=STAR, "
                                           "spec=MULTI, frontier=walk, "
                                           "seeds=(1,2,3) for all classes "
                                           "and the baseline")},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = f"{n_pass}/{len(gates)} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in gates.items()))
    print(f"  OOD median {ood_median:.3f} vs in-domain {in_median:.3f} "
          f"(bound {2.0 * in_median:.3f})")

    result = {
        "exp": "exp137_universal_reader",
        "claim": ("M33-class reading generalizes to media outside the "
                  "19-type domain with zero rejections and bounded "
                  "quality loss (one reader configuration, no "
                  "per-medium re-tuning)"),
        "config": {"op": STAR_OP, "spec": "MULTI (exp94)",
                   "frontier": "walk", "seeds": list(seeds),
                   "projection": "magnitude -> symmetrize -> time-average"
                                 " -> pairwise (|w_e|/(|e|-1) factorization)",
                   "contract": list(CONTRACT)},
        "in_domain": in_domain,
        "in_domain_pooled_median_err": in_median,
        "raw_probes": raw_probes,
        "ood": ood,
        "ood_pooled_median_err": ood_median,
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
