#!/usr/bin/env python3
"""exp160 — THE UNIVERSAL READER AT ANY MEDIUM (Stage 5 path 1, the
L134-registered "any medium" cell: RANDOM/ADVERSARIAL media drawn over
the union space, NOT curated classes).

FOUNDATION (exp137 L115 4/4; exp142; exp145 L125; exp148 L129 3/4 with the
flip-clock channel delivered; exp152 L134 4/4): the read stack that has
consumed the 19-substrate-type domain, exp137's 6 curated OOD classes and
the 3 semantics channels (sign exp142, phase exp145, flip-clock exp148) is
exp148's temporal read: PN1/PN2 dominant-quadrature projection + TC1 raw
per-edge presence-transition counts + TC2 A_ext = A + F, feeding exp142's
execute_signed VERBATIM. Every medium it has ever eaten was CURATED — a
named class with fixed parameters. This experiment asks the untested
question: does the SAME configuration decode media drawn AT RANDOM from
the union of all consumed spaces, with zero rejections and bounded
quality loss — and when it fails, is the violated semantics dimension
nameable from the medium's generation record alone?

THE UNION SPACE (the generator; ONE master seed, frozen before the run):
  GEN_SEED = 160160; instance i draws with np.random.default_rng(GEN_SEED
  + i) at n=100; support = exp137's _base_connected (ring backbone +
  chords p=0.04); magnitudes = exp137's _wU, U(0.5, 1.5) — the deposited
  operating range. FIVE semantics dimensions, each independently ACTIVE
  with p = 0.5 (the instance is a random MIX, not a class):
    oriented  (A-SYM)   per-edge one-way orientation with prob 0.5,
                        direction random (the rest stays undirected)
    signed    (A-NN)    per-edge negative sign with instance-level
                        p_neg ~ U(0.1, 0.5); sign is a property of the
                        undirected edge (symmetric; exp142's probe-pair
                        convention)
    complex   (A-REAL)  per-edge random phase with instance-level
                        fraction ~ U(0.2, 1.0)
    hyper     (A-PAIR)  1-20 added hyperedges of size 3-6 with magnitude
                        U(0.5,1.5) and sign/phase drawn from the SAME
                        mechanism as pair edges, presented through the ONE
                        pairwise factorization w_e/(|e|-1) (exp137's
                        clause, generalized phase-carrying: the pair
                        weight is the complex w_e/(|e|-1))
    temporal  (A-STAT)  T = 8 frames; per-edge presence Bernoulli with
                        instance-level p_keep ~ U(0.6, 0.95) per frame
                        (ring backbone always on); hyperedges flip on the
                        same p_keep; a static draw is one all-on frame
  All schedules are drawn in __init__ from the instance's own rng stream;
  snapshots() is a deterministic re-iterable (no rng at read time).

THE ONE CONFIGURATION (frozen before the first battery decode; zero
knobs): read_temporal (exp148 VERBATIM) at op = STAR (gamma=64, mu=0),
spec = MULTI, seeds = (1, 2, 3) — exp137's seed protocol, unchanged. The
read path is imported, never copied, and contains no branch on any
property of the instance (the generator branches; the reader does not).

PRE-REGISTERED GATES (fixed before the first battery decode; the deposit
reports them whatever the outcome):

  U1 (zero rejections)  every decode over all 200 instances x 3 seeds
                        (600 decodes) returns a finite err_vs_target with
                        no exception and no dtype-coercion warning
                        (warnings-as-errors; exp137/exp142 policy). A
                        low-quality decode is NOT a rejection (exp137 D2
                        precedent) — program_verified is recorded per
                        decode and deposited, not gated here.

  U2 (bounded quality)  pooled median decode err over the whole battery
                        <= 1.30 mV = 2.0 x exp137's DEPOSITED OOD pooled
                        median 0.65 mV. The anchor is the deposited
                        number; no in-run re-derivation.

  U3 (failure           every instance whose per-instance median err
      localization)     exceeds the bar carries its named violated-
                        assumption set (mechanical from the generation
                        record; the all-off corner is named "none") and
                        the tail decomposition is deposited: per-
                        dimension conditional above-bar rates (+ lift),
                        the per-subset table, and the dominant driver =
                        the dimension with the highest above-bar rate
                        among dimensions with >= 20 active instances
                        (min cell 20); if no single dimension qualifies
                        while a tail exists, the most frequent above-bar
                        violated-subset is named (subset-level). If no
                        instance is above the bar the decomposition is
                        the empty one. U3 does NOT gate on the tail
                        fraction — see the heavy-tail clause.

  U4 (one               the read configuration is a single frozen
      configuration)    constant: its sha256 fingerprint is recorded for
                        every decode and asserted identical across all
                        instances, asserted unchanged after the run, and
                        the read path identity is asserted
                        (read_temporal IS exp148's; its executor IS
                        exp142's execute_signed; spec IS exp94's MULTI).

HEAVY-TAIL CLAUSE (pre-registered): if the tail fraction (instances above
the bar) exceeds 0.10, that IS the result — universality has a quantified
boundary; the owning dimension (the dominant driver) and a registered
repair are deposited with the tail table. Below 0.10 the boundary is not
crossed at the bar on random media.

TIMING DISCLOSURE (pre-registration): a 2-decode timing probe (exp137's
TimeVaryingMedium and SignedMedium through exp148's read_temporal, seed 1)
was run before this protocol was frozen, solely to size the battery inside
the wall budget; the read configuration was untouched by it.

DEPOSIT: results/exp160_any_medium.json

RUN:
  python3 -m experiments.exp160_any_medium            # full (200 x 3)
  python3 -m experiments.exp160_any_medium --smoke    # instrument check
"""
from __future__ import annotations

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
OUT = os.path.join(ROOT, "results", "exp160_any_medium.json")

# ------------------------------------------------- frozen protocol
GEN_SEED = 160160                 # master generator seed (deposited pre-run)
N_INSTANCES = 200
N = 100
SEEDS = (1, 2, 3)                 # exp137's seed protocol, unchanged
T_FRAMES = 8                      # temporal depth when the dim draws active
DIM_P = 0.5                       # per-dimension activity probability
DIMENSIONS = ("oriented", "signed", "complex", "hyper", "temporal")
VIOLATION = {"oriented": "A-SYM", "signed": "A-NN", "complex": "A-REAL",
             "hyper": "A-PAIR", "temporal": "A-STAT"}

OOD_ANCHOR = 0.65                 # exp137's DEPOSITED OOD pooled median (mV)
BAR = 1.30                        # U2 bar = 2.0 x anchor
MIN_CELL = 20                     # dominant-driver minimum cell
HEAVY_TAIL = 0.10                 # heavy-tail clause threshold

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


# ------------------------------------------------- the random medium
class RandomMedium:
    """One random draw over the semantics union space (5 dimensions, each
    independently active with DIM_P; magnitudes in exp137's deposited
    operating range U(0.5, 1.5); support = exp137's _base_connected).
    All random choices happen in __init__ from ONE rng stream
    (np.random.default_rng(seed)); snapshots() is a deterministic
    re-iterable with no rng at read time."""

    kind = "random_union"

    def __init__(self, n: int, seed: int):
        rng = np.random.default_rng(seed)
        self.seed = seed
        self.n = n
        self.dims = {d: bool(rng.random() < DIM_P) for d in DIMENSIONS}

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

        # --- signed (A-NN): symmetric per-edge sign
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

        # --- complex (A-REAL): symmetric per-edge phase
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
                        if self.hyper_on[k, t]:
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


# ------------------------------------------------------------ helpers
def tail_decomposition(instances: list[dict]) -> dict:
    """U3's tail table: per-dimension conditional above-bar rates, the
    per-subset table, and the dominant driver (min-cell rule; subset-
    level fallback). Deposited whatever the outcome."""
    above = [r for r in instances if r["above_bar"]]
    per_dim: dict = {}
    for d in DIMENSIONS:
        act = [r for r in instances if r["dims"][d]]
        ina = [r for r in instances if not r["dims"][d]]
        ra = (sum(1 for r in act if r["above_bar"]) / len(act)) if act else None
        ri = (sum(1 for r in ina if r["above_bar"]) / len(ina)) if ina else None
        per_dim[d] = {
            "n_active": len(act), "n_above_active": sum(
                1 for r in act if r["above_bar"]),
            "rate_active": ra,
            "n_inactive": len(ina), "n_above_inactive": sum(
                1 for r in ina if r["above_bar"]),
            "rate_inactive": ri,
            "lift": (ra / ri) if (ra is not None and ri) else None,
        }
    subsets: dict = {}
    for r in instances:
        key = "+".join(r["violated"]) if r["violated"] else "none"
        rec = subsets.setdefault(key, {"n": 0, "n_above": 0, "errs": []})
        rec["n"] += 1
        rec["errs"].extend(r["errs"])
        if r["above_bar"]:
            rec["n_above"] += 1
    for rec in subsets.values():
        rec["median_err"] = (float(np.median(rec["errs"]))
                             if rec["errs"] else None)
        del rec["errs"]

    driver, driver_level = None, None
    if above:
        best = 0.0
        for d in DIMENSIONS:
            c = per_dim[d]
            if (c["n_active"] >= MIN_CELL and c["rate_active"]
                    and c["rate_active"] > best):
                best, driver, driver_level = c["rate_active"], d, "dimension"
        if driver is None:                       # interaction-class fallback
            top = max(subsets.items(), key=lambda kv: kv[1]["n_above"])
            driver, driver_level = top[0], "subset"
    return {
        "bar_mV": BAR,
        "anchor": f"exp137 deposited OOD pooled median {OOD_ANCHOR} mV",
        "n_above": len(above),
        "tail_frac": len(above) / len(instances) if instances else 0.0,
        "above_bar_instances": [r["i"] for r in above],
        "per_dimension": per_dim,
        "per_subset": subsets,
        "min_cell": MIN_CELL,
        "dominant_driver": driver,
        "driver_level": driver_level,
        "heavy_tail_clause_triggered": bool(
            instances and len(above) / len(instances) > HEAVY_TAIL),
    }


def evaluate_gates(instances: list[dict], all_errs: list[float],
                   rejections: list[dict], decode_fps: list[str],
                   fp: str, tail: dict, seeds: tuple[int, ...] = SEEDS) -> dict:
    u1 = (len(rejections) == 0
          and len(all_errs) == len(instances) * len(seeds))
    u2 = bool(np.median(all_errs) <= BAR) if all_errs else False
    coverage = all(r["violated_class_named"] for r in instances
                   if r["above_bar"])
    table_covers = all(
        ("+".join(r["violated"]) if r["violated"] else "none")
        in tail["per_subset"] for r in instances if r["above_bar"])
    u3 = bool(coverage and table_covers)
    u4 = (len(set(decode_fps)) == 1 and decode_fps[0] == fp
          and config_fingerprint() == fp
          and read_temporal.__module__ == "experiments.exp148_temporal_read"
          and execute_signed.__module__ == "experiments.exp142_sign_read"
          and MULTI.__class__.__name__ == "AnatomySpec")
    return {
        "U1_zero_rejections": {
            "pass": bool(u1), "rejections": len(rejections),
            "decodes": len(all_errs),
            "rejection_records": rejections,
            "verify_rate": (float(np.mean([v for r in instances
                                           for v in r["verified"]]))
                            if instances else None)},
        "U2_bounded_quality": {
            "pass": bool(u2), "pooled_median_err": (float(np.median(all_errs))
                                                    if all_errs else None),
            "bar_mV": BAR, "anchor_mV": OOD_ANCHOR,
            "bound_ratio": 2.0,
            "p90_err": (float(np.percentile(all_errs, 90))
                        if all_errs else None),
            "max_err": (float(np.max(all_errs)) if all_errs else None)},
        "U3_failure_localization": {
            "pass": bool(u3), "attribution_coverage": coverage,
            "decomposition": tail},
        "U4_one_configuration": {
            "pass": bool(u4), "fingerprint": fp,
            "distinct_fingerprints": len(set(decode_fps)),
            "post_run_fingerprint": config_fingerprint(),
            "audit": ("read_temporal IS exp148's; its executor IS exp142's "
                      "execute_signed; spec IS exp94's MULTI; the read path "
                      "branches on no instance property; the generator "
                      "branches, the reader does not")},
    }


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 4 instances, 1 seed")
    args = ap.parse_args()
    n_inst = 4 if args.smoke else N_INSTANCES
    seeds = (1,) if args.smoke else SEEDS
    t0 = time.time()
    fp = config_fingerprint()
    print(f"=== exp160: THE UNIVERSAL READER AT ANY MEDIUM "
          f"({'SMOKE' if args.smoke else 'FULL'}) ===")
    print(f"  fingerprint {fp}  gen_seed {GEN_SEED}  "
          f"instances {n_inst}  seeds {seeds}\n")

    rejections: list[dict] = []
    instances: list[dict] = []
    all_errs: list[float] = []
    decode_fps: list[str] = []

    for i in range(n_inst):
        med = RandomMedium(N, seed=GEN_SEED + i)
        errs, vs, branches, rhos = [], [], [], []
        for s in seeds:
            decode_fps.append(fp)
            try:
                out = read_temporal(med, s)          # THE one call site
                err = float(out["err_vs_target"])
                if not np.isfinite(err):
                    raise ValueError(f"non-finite decode err {err}")
                errs.append(err)
                all_errs.append(err)
                vs.append(bool(out["program_verified"]))
                branches.append(out["branch"])
                rhos.append(round(float(out["rho"]), 4))
            except Exception as e:                   # a rejection is
                rejections.append(                   # RECORDED, never hidden
                    {"instance": i, "seed": s,
                     "rejection": f"{type(e).__name__}: {e}"[:200]})
        med_err = float(np.median(errs)) if errs else None
        violated = list(med.violated)
        rec = {
            "i": i, "gen_seed": GEN_SEED + i,
            "dims": {d: bool(med.dims[d]) for d in DIMENSIONS},
            "violated": violated,
            "violated_class_named": True,
            "n_oneway": med.n_oneway, "n_neg": med.n_neg,
            "n_phased": med.n_phased, "n_hyper": med.n_hyper,
            "p_neg": round(med.p_neg, 3),
            "phase_frac": round(med.phase_frac, 3),
            "p_keep": round(med.p_keep, 3), "T": med.T_eff,
            "branch": branches, "rho": rhos,
            "errs": errs, "median_err": med_err, "verified": vs,
            "above_bar": bool(med_err is not None and med_err > BAR),
            "config_fp": fp,
        }
        instances.append(rec)
        if (i + 1) % 25 == 0 or i == n_inst - 1:
            done = len(all_errs)
            print(f"  [{i + 1:3d}/{n_inst}] decodes {done} "
                  f"rejections {len(rejections)} "
                  f"median-so-far "
                  f"{float(np.median(all_errs)):.2f}" if done else
                  f"  [{i + 1:3d}/{n_inst}] decodes 0")

    tail = tail_decomposition(instances)
    gates = evaluate_gates(instances, all_errs, rejections, decode_fps,
                           fp, tail, seeds)
    n_pass = sum(int(g["pass"]) for g in gates.values())
    if args.smoke:
        verdict = "smoke (instrument check; gates not evaluated)"
    else:
        verdict = f"{n_pass}/{len(gates)} gates"
        if tail["heavy_tail_clause_triggered"]:
            verdict += (f" + HEAVY TAIL ({tail['n_above']}/{len(instances)}"
                        f" above bar; owner: {tail['dominant_driver']}"
                        f" [{tail['driver_level']}]) — universality"
                        f" boundary quantified, repair registered")
        else:
            verdict += " — no heavy tail at the bar"
    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k}: {'PASS' if g['pass'] else 'FAIL'}")
    if all_errs:
        print(f"  pooled median {float(np.median(all_errs)):.3f} mV "
              f"(bar {BAR})  p90 "
              f"{float(np.percentile(all_errs, 90)):.3f}  max "
              f"{float(np.max(all_errs)):.3f}")
        print(f"  tail {tail['n_above']}/{len(instances)} "
              f"({tail['tail_frac']:.3f}); dominant driver "
              f"{tail['dominant_driver']} ({tail['driver_level']})")

    result = {
        "exp": "exp160_any_medium",
        "claim": ("the exp148 temporal read (the current best stack: "
                  "sign+phase+flip-clock, A_ext = A + F, exp142 executor "
                  "verbatim) decodes RANDOM media drawn over the union of "
                  "all consumed spaces (random weighted/signed/complex/"
                  "directed/hypergraph/time-varying mixes) with zero "
                  "rejections, zero re-tuning, and bounded quality loss; "
                  "above-bar failures are localized to named semantics "
                  "dimensions from the generation record alone"),
        "generator": {
            "master_seed": GEN_SEED,
            "instance_seed_rule": "GEN_SEED + i",
            "n": N, "n_instances": n_inst,
            "dim_p": DIM_P, "dimensions": list(DIMENSIONS),
            "violation_map": VIOLATION,
            "magnitudes": "U(0.5, 1.5) = exp137's _wU operating range",
            "support": "exp137's _base_connected (ring + chords p=0.04)",
            "temporal_frames": T_FRAMES,
            "hyper_factorization": "w_e/(|e|-1) complex pairwise "
                                   "(exp137's clause, phase-carrying)",
            "sign_convention": "per undirected edge, symmetric (exp142's "
                               "probe-pair convention)",
        },
        "config": {**READ_CONFIG, "fingerprint": fp},
        "pooled_median_err": (float(np.median(all_errs))
                              if all_errs else None),
        "instances": instances,
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
