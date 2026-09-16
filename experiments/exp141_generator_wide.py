#!/usr/bin/env python3
"""exp141 — GENERATOR V6, WIDENED DOMAIN (the L119-registered repair
run; the 101% Stage-3 generator, second registered run).

======================================================================
PRE-REGISTERED (this docstring was written BEFORE the run; the search
below is executed exactly once against these gates):
======================================================================

CLAIM (wording unchanged from exp136): the compiler can INVENT
anatomies evolution never made — new fate profiles that lie farther
from the repo's frozen reference library (everything the record and
this program have ever produced: WT, two-headed, the exp11 novel set,
exp81's generated registry, exp87's explicit specs, exp94's multi
program) than the library's own internal spread — and the invented
anatomies still decode under the TWO-CHANNEL LAW: writability priced
by the measured quadrature err = sqrt(eV^2 + eTheta^2) (exp84's
adopted channel composition), audited below the map's 6.0 mV operating
bar (ERR_BAR), and restored by the existing decoder (exp90's
two-source read: M33 pole read above the line, canon read below).

======================================================================
THE L119 REPAIR (what changes vs exp136 — the DOMAIN and the N*
re-derivation ONLY; the GATES, the METRIC, the SCORE, the LADDER, the
AUDIT and the DECODE are UNCHANGED):
  exp136 delivered 0/4 with the owned diagnosis: the 72-member frozen
  library's ~260 boundary cuts blanket the pole-read domain [-35,-15]
  mV on 1-4 disjoint zones, and inside that domain novelty is
  ANTI-correlated with two-channel writability (the audit's V-channel
  degrades with distance from library cuts) — a DOMAIN failure, not a
  search failure. L119 registers three repairs, all implemented here:

  (a) DOMAIN WIDENING, justified by exp128's canon-strip re-pricing
      (ledger L112): the canon-stripped knockout IMPROVES zone pricing
      on both substrates (grid2d err_z0 3.21 -> 1.19, err_z2 9.65 ->
      7.00; torus err_z0 6.03/brk 0.50 -> 3.38/0.00, err_z2 7.52 ->
      4.71) — the below-line canon read (phi_spec_canon serving the
      PRE-program canon spec to below-line cells) is a TRADE-OFF
      (gap-fidelity bought with zone-drag): its canon values (trunk
      -50 mV, head -20 mV) DRAG zones during the weak-pinning settle.
      Re-priced with the drag named, the below-line flank of the
      compiler's identity repertoire unlocks: a zone in the
      near-trunk shelf (-56, -44) is CARRIED by the canon read itself
      (the below-line walk branch reads the canon -50 — the drag IS
      the decode there), a mechanism the pole-domain-only pricing
      could not see. The emitted voltage domain therefore widens from
      the pole-read band [-35, -15] to the compiler's FULL identity
      repertoire [-60, -15] (REPERTOIRE_LO/HI, compiler/anatomy.py).
      The deep tail [-60, -56) is admitted as an instruments-priced
      probe: the record's own produced programs live there (exp87's
      -59/-60 entries; exp94's BELOW program at -59) and L112 removes
      the presumption that below-line = unwritable — exp94's MS-G2
      no-backdoor result (the -59 zone failing most substrates at the
      star point) is the competing deposit and the gates own the
      outcome either way.

  (b) THE EXP94-CLASS MULTI ADMISSION: zones may TOUCH or OVERLAP
      (non-disjoint programs; overlap resolved by EMISSION ORDER —
      the compiler's clamp loop applies zones in order, the later
      clamp winning shared cells, exactly the semantics of
      profile_of_zones). exp136's gap >= 0.02 clause forced canon
      tissue between every pair of zones, so non-canon-adjacent
      structure (e.g. a -30/-55 staircase) was UNREACHABLE; the
      multi/exp94-class non-disjoint programs are admitted as the
      novelty-bearing class. The cuts rejection-sampling clause stays
      RETIRED (exp136's in-registered repair): cuts are drawn
      uniform; the novelty pressure lives in the score's penalty
      term, where it was always load-bearing.

  (c) THE N* BAR RE-DERIVED BEFORE THE SEARCH: N* is recomputed on
      the frozen 72-member library with the IDENTICAL metric as
      exp136 (D = 100*d_struct(tol 0.01) + d_rms; d_struct = tolerant
      boundary-set |Delta|/|cup|, match tolerance one cell of the
      n=100 lattice) and DEPOSITED to the results file (stage
      "n_star_deposit") before the search's first candidate is
      evaluated; the gates consume exactly that recomputed value. A
      sensitivity value (the same rule with exp94's produced BELOW
      program added as a 73rd reference member) is deposited
      alongside as a robustness diagnostic; the frozen 72-member bar
      governs, per this pre-registration.

SEARCH (same shape as exp136: stratified seeds -> elite + mutation
generations; J = quad_err + novelty penalty):
  - Space: k in {1..5} zones, per-zone width >= 0.04, voltages on the
    0.1 mV emission grid (exp136's as-built rounding) in [-60, -15]
    (widened), zones may touch/overlap (widened; NO gap requirement),
    total span (zone hull) <= 0.90 (the decoder's regen walk needs
    intact boundary tissue), no both-ends coverage.
  - Score: J = err_quad_search + 5.0 * relu(N_STAR - NOV_lib), where
    err_quad_search = hypot(eV, eT) from 1-seed exp84-style ablation
    runs (V_only: mu=0; theta_only: G_V=0) at the cheaper of the two
    cheapest price-map cells ((1, 0.015), (4, 0) with a +1.0 mV
    surcharge for the more expensive cell), and NOV_lib is the
    distance to the nearest library member.
  - Rounds: 96 stratified seeds (zone count x axis thirds x SIX
    voltage bands — the three pole bands of exp136 plus three
    below-line bands; 1/3 of seeds forced into the non-disjoint
    class), then 5 generations of (select elites -> mutate: shift a
    cut / regrade a voltage / add / drop / move a zone / nest a zone
    inside an existing one — the nest op is the non-disjoint class's
    mutation).
  - The frozen library enters ONLY as the score's reference set; no
    requested spec exists anywhere in the run.

METRIC (identical to exp136, verbatim instruments imported from
exp136's module — the same d_struct, dist, erosion, quad_err, decode
code paths):
  - Representation: the fate profile f in R^100 (canon WT + zone
    overwrites in emission order) and its boundary set B.
  - D(r, s) = 100 * d_struct + d_rms, d_struct the boundary-set
    distance under tolerant greedy matching (tol 0.01), d_rms =
    RMS(f_r - f_s) in mV. Structure dominates voltage.
  - NOV(spec) = min over the reference set of D.
  - N_STAR = the 95th percentile of within-library nearest-neighbor
    distances (the library's own internal spread — the corpus defines
    the threshold, not us).
  - ANTI-RECOMBINATION: distance to every single-crossover splice of
    every reference pair (crossover in {0.05, ..., 0.95}) must also
    exceed N_STAR.

GATES (all evaluated on the 10 delivered inventions; the delivered
set is the greedy diversity-filtered, novelty-filtered top of the
search pool sorted by J; WORDING UNCHANGED from exp136):

  GATE-C1  NOVELTY-CONSTRAINED GENERATION: exactly 10 inventions are
           delivered, and every one satisfies NOV > N_STAR against the
           frozen library INCLUDING the anti-recombination splice
           check.
  GATE-C2  TWO-CHANNEL AUDIT: >= 8/10 inventions pass the measured
           quadrature audit err_quad = hypot(eV, eT) < 6.0 mV (3
           seeds, exp84's ablation semantics) at the program's emitted
           operating point — the cheapest passing cell on the
           pre-registered ladder [(1, 0.015), (4, 0), (16, 0), (64, 0)]
           (the price-map cells; the emitted cell of every invention
           is deposited). Pre-named degradation: if >= 8/10 pass but
           every emitted cell is the star (64, 0), C2 passes and the
           verdict records STAR-ONLY (the claim downgrades to
           "inventions are writable somewhere").
  GATE-C3  DECODE + STABILITY: >= 8/10 inventions decode under the
           existing decoder (R1 spec write + clamp window + amputation
           of the zone span + the exp90 BFS walk with the per-cell M33
           pole read above the line and canon read below it) at their
           emitted operating point: post-settle pattern error < 6.0 mV
           AND the decoded form holds a further 100 t.u. with error
           < 6.0 mV, each on >= 2/3 seeds.
  GATE-C4  ZERO-ANATOMY-IS-SPECIAL: the delivered inventions are
           pairwise novel — min over i != j of D(inv_i, inv_j)
           > N_STAR (the set is not 10 perturbations of one point).

REPORTED DIAGNOSTICS (not gates): (1) the exp136 diagnosis re-tested
on the widened domain — Spearman(NOV_lib, err_quad_search) over the
round-0 pool, over the whole pool, and over the pole-only subpool
(all zones >= -35): exp136 found novelty ANTI-correlated with
writability inside the pole domain; the widening's mechanism claim is
that the anti-correlation breaks once the canon-carried below-line
shelf and the non-disjoint class are admitted; (2) per-class counts
(disjoint vs non-disjoint, pole vs below-line, non-canon-adjacent
boundaries) among the novel pool and the delivered set; (3) the
quadrature composition's own validity on the invented map —
Spearman(err_quad, err_full_measured) across the delivered inventions
at their emitted cells; (4) the per-cell audit ladder table; (5)
search-round summaries.

RUNTIME BUDGET: search 96 + 5x48 = 336 candidates x 2 cells x 2
ablation runs; audit 10 x (4 cells x 6 runs x 3 seeds); decode 10 x 3
runs; splice novelty ~10 x ~49k distances. Serial, BLAS pinned;
minutes, not hours.

HONEST SCOPE (stated, not hidden): one substrate (the canon chain,
n=100 — the compiler's home axis); the widened voltage domain is
still inside the compiler's identity repertoire [-60, -15]; the
below-line class's decode path IS the canon read (L112's trade-off
mechanism), so deep-tail inventions are expected to strain C3 and
the gate count owns that honestly if they do; the audit prices
WRITABILITY (exp84 semantics) while C3 prices RE-DERIVATION (the
two-source walk); no claim beyond what these instruments measure.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.morphospace import wildtype_target  # noqa: E402
from experiments.exp94_multizone_scale import BELOW  # noqa: E402
from experiments.exp136_generator_v6 import (  # noqa: E402
    N, AXIS, ERR_BAR, LADDER, SEARCH_CELLS, CELL_SURCHARGE, AUDIT_SEEDS,
    LAMBDA_NOV, N_DELIVER, CUT_TOL, A_CHAIN, DT_DEG_MAX,
    profile_of_zones, zones_of_spec, build_library, cuts_of, d_struct,
    dist, library_nn_stats, build_splices, nov_lib, nov_splice,
    erosion, quad_err, decode,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp141_generator_wide.json")

# ---- the widened emission domain (L119 repair (a)) ----------------
WIDE_LO = -60.0            # REPERTOIRE_LO (compiler/anatomy.py)
WIDE_HI = -15.0            # REPERTOIRE_HI (compiler/anatomy.py)
NEURAL_LINE = -35.0        # NEURAL_SPEC_MIN: the M33 pole-read line
# six stratification bands: three below-line (new) + exp136's three
# pole bands (unchanged)
VBANDS = ((-60.0, -52.0), (-52.0, -44.0), (-44.0, -35.0),
          (-35.0, -28.0), (-28.0, -21.0), (-21.0, -15.0))
THIRDS = ((0.0, 0.36), (0.32, 0.68), (0.64, 1.0))

# ---- the search shape (exp136's, unchanged) ------------------------
POP0 = 96
ROUNDS = 5
PER_ROUND = 48
N_ELITE = 16
RNG = np.random.default_rng(141)
CANON = wildtype_target(N)


# ==================================================================
# the widened space (L119 repairs (a) + (b))
# ==================================================================
def well_formed_wide(zones) -> bool:
    """The widened well-formedness: k in 1..5, width >= 0.04, voltage
    in the full repertoire [-60, -15], hull span <= 0.90, no both-ends
    coverage; zones MAY touch or overlap (no gap requirement)."""
    if not (1 <= len(zones) <= 5):
        return False
    zs = sorted(zones)
    for (a, b, v) in zs:
        if not (0.0 <= a < b <= 1.0):
            return False
        if (b - a) < 0.04:
            return False
        if not (WIDE_LO <= v <= WIDE_HI):
            return False
    span = zs[-1][1] - zs[0][0]
    if span > 0.90:                           # intact boundary tissue
        return False
    if zs[0][0] <= 0.0 and zs[-1][1] >= 1.0:
        return False
    return True


def to_key(zones) -> tuple:
    return tuple((round(a, 3), round(b, 3), round(v, 1)) for a, b, v in zones)


def random_spec_wide(rng, stratify: bool = True,
                     force_overlap: bool = False):
    """One widened seed. Stratification: zone count x axis third x
    voltage band. force_overlap draws every zone after the first
    overlapping an existing one (the exp94-class non-disjoint
    admission); cuts are drawn uniform (the rejection clause stays
    retired per exp136's in-registered repair)."""
    k = int(rng.integers(1, 6))
    zones: list[tuple] = []
    used_thirds: list[int] = []
    for _ in range(k):
        for _try in range(40):
            if stratify and len(used_thirds) < 3:
                t = int(rng.choice([t for t in range(3)
                                    if t not in used_thirds]))
            else:
                t = int(rng.integers(0, 3))
            lo, hi = THIRDS[t]
            vb = VBANDS[int(rng.integers(0, len(VBANDS)))]
            v = float(np.round(rng.uniform(*vb), 1))
            if force_overlap and zones:
                (a0, b0, _) = zones[int(rng.integers(0, len(zones)))]
                w = float(rng.uniform(0.04, 0.20))
                a_lo = max(0.0, a0 - 0.02)
                a_hi = min(b0 - 0.01, 1.0 - w)
                if a_hi <= a_lo:
                    continue
                a = float(rng.uniform(a_lo, a_hi))
                b = a + w                       # b2 > a0: overlap guaranteed
            else:
                a = float(rng.uniform(lo, hi - 0.05))
                w = float(rng.uniform(0.04, 0.20))
                b = a + w
            if b > 1.0:
                continue
            cand = zones + [(round(a, 3), round(b, 3), v)]
            if well_formed_wide(cand):
                zones = cand
                used_thirds.append(t)
                break
    return zones


def mutate_wide(zones, rng):
    """exp136's op set + the NEST op (the non-disjoint class's
    mutation: a zone drawn overlapping an existing one at a different
    voltage). Regrade clips to the widened repertoire."""
    zs = [list(z) for z in zones]
    ops = ["shift_cut", "regrade", "add", "drop", "move", "nest"]
    if len(zs) >= 5:
        ops.remove("add")
        ops.remove("nest")
    if len(zs) <= 1:
        ops.remove("drop")
    op = ops[int(rng.integers(0, len(ops)))]
    zi = int(rng.integers(0, len(zs)))
    if op == "shift_cut":
        side = int(rng.integers(0, 2))
        zs[zi][side] = round(float(np.clip(
            zs[zi][side] + float(rng.choice([-1, 1]))
            * float(rng.uniform(0.01, 0.05)), 0.0, 1.0)), 3)
    elif op == "regrade":
        zs[zi][2] = round(float(np.clip(
            zs[zi][2] + float(rng.choice([-1, 1])) * float(rng.uniform(1, 3)),
            WIDE_LO, WIDE_HI)), 1)
    elif op == "add":
        a = float(rng.uniform(0.02, 0.94))
        b = round(min(a + float(rng.uniform(0.04, 0.16)), 0.99), 3)
        zs.append([a, b, round(float(rng.uniform(WIDE_LO, WIDE_HI)), 1)])
    elif op == "drop":
        zs.pop(zi)
    elif op == "move":
        a = float(rng.uniform(0.02, 0.94))
        w = zs[zi][1] - zs[zi][0]
        zs[zi][0] = round(a, 3)
        zs[zi][1] = round(min(a + w, 0.99), 3)
    elif op == "nest":
        a0, b0, v0 = zs[zi]
        w = float(rng.uniform(0.04, max(0.05, 0.6 * (b0 - a0))))
        a_lo = max(0.0, a0 - 0.02)
        a_hi = min(b0 - 0.01, 1.0 - w)
        if a_hi <= a_lo:
            return None
        a = float(rng.uniform(a_lo, a_hi))
        v2 = round(float(rng.uniform(WIDE_LO, WIDE_HI)), 1)
        for _try in range(20):
            if abs(v2 - v0) >= 6.0:
                break
            v2 = round(float(rng.uniform(WIDE_LO, WIDE_HI)), 1)
        zs.append([round(a, 3), round(a + w, 3), v2])
    cand = [(z[0], z[1], z[2]) for z in zs]
    return cand if well_formed_wide(cand) else None


def class_tags(zones, f: np.ndarray) -> dict:
    """The widened-domain class diagnostics for one candidate."""
    zs = sorted(zones)
    overlap = any(zs[i + 1][0] < zs[i][1] - 1e-9
                  for i in range(len(zs) - 1))
    touching = any(abs(zs[i + 1][0] - zs[i][1]) <= 1e-9
                   for i in range(len(zs) - 1))
    vs = [v for (_, _, v) in zones]
    below = sum(1 for v in vs if v < NEURAL_LINE)
    # non-canon-adjacent boundaries: adjacent cells BOTH off-canon
    ncab = int(sum(1 for i in range(N - 1)
                   if f[i] != f[i + 1]
                   and f[i] != CANON[i] and f[i + 1] != CANON[i + 1]))
    return {"nondisjoint": bool(overlap or touching), "overlap": overlap,
            "touching": touching, "n_below_line_zones": below,
            "min_v": float(min(vs)), "max_v": float(max(vs)),
            "noncanon_adjacent_boundaries": ncab}


def spearman(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(np.argsort(np.argsort(a)),
                             np.argsort(np.argsort(b)))[0, 1])


# ==================================================================
# main
# ==================================================================
def main() -> dict:
    t_start = time.time()
    print("=== exp141: generator v6, WIDENED DOMAIN (the L119 repair) "
          "===\n")

    # ---- 1. the frozen library and the RE-DERIVED bar --------------
    lib = build_library()
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    n_star, nn = library_nn_stats(lib)
    print(f"  library: {len(lib_names)} reference profiles "
          f"(frozen; identical corpus to exp136)")
    print(f"  within-library NN D: min {nn.min():.1f} "
          f"median {np.median(nn):.1f} p95 {n_star:.2f} max {nn.max():.1f}")
    print(f"  N_STAR recomputed with exp136's IDENTICAL metric "
          f"(100*d_struct(tol {CUT_TOL}) + d_rms): {n_star:.2f} "
          f"(exp136 deposited 82.288)")
    # sensitivity: the produced below-line multi program as a 73rd ref
    aug = dict(lib)
    aug["exp94_below"] = profile_of_zones(zones_of_spec(BELOW))
    n_star_aug, _ = library_nn_stats(aug)
    print(f"  N_STAR sensitivity (73rd member = exp94's BELOW, the "
          f"produced below-line multi): {n_star_aug:.2f} "
          f"(diagnostic only; the frozen 72-member bar governs)")
    dup = [(lib_names[i], lib_names[j])
           for i in range(len(lib_names))
           for j in range(i + 1, len(lib_names))
           if np.array_equal(lib[lib_names[i]], lib[lib_names[j]])]
    if dup:
        print(f"  OWNED corpus defect: identical frozen members {dup}")

    # ---- 2. DEPOSIT the bar BEFORE the search runs ------------------
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump({
            "exp": "exp141_generator_wide (generator v6, widened "
                   "domain — the L119 repair run)",
            "stage": "n_star_deposit (written BEFORE the search runs)",
            "metric": {
                "distance": "100 * d_struct + d_rms; d_struct = "
                            "tolerant boundary-set |Delta|/|cup| "
                            "(match tol 0.01, one cell of the n=100 "
                            "lattice); d_rms = profile RMS (mV) — "
                            "exp136's metric, imported verbatim",
                "N_STAR_rule": "95th percentile of within-library "
                               "nearest-neighbor distances",
                "n_star": round(n_star, 3),
                "n_star_exp136_deposited": 82.288,
                "n_star_aug73_below_sensitivity": round(n_star_aug, 3),
                "library_size": len(lib_names),
                "library": lib_names,
            },
        }, fh, indent=1, default=float)
    print("  N_STAR deposited -> results/exp141_generator_wide.json "
          "(stage n_star_deposit)\n")

    # ---- 3. the search (exp136's shape) -----------------------------
    splices = build_splices(lib)
    print(f"  splice family for the anti-recombination clause: "
          f"{len(splices)} single-crossover profiles")
    cache: dict[tuple, dict] = {}

    def evaluate(zones) -> dict:
        key = to_key(zones)
        if key in cache:
            return cache[key]
        f = profile_of_zones(zones)
        nov = nov_lib(f, lib_arr)
        best = None
        for ci, (g, mu) in enumerate(SEARCH_CELLS):
            eV, eT, q = quad_err(f, g, mu, seeds=(1,))
            cost = q + ci * CELL_SURCHARGE
            if best is None or cost < best["cost"]:
                best = {"cost": cost, "cell": (g, mu), "eV": eV,
                        "eT": eT, "quad": q}
        J = best["cost"] + LAMBDA_NOV * max(0.0, n_star - nov)
        rec = {"zones": zones, "f": f, "nov_lib": nov, "J": J,
               "search_cell": best["cell"], "search_eV": best["eV"],
               "search_eT": best["eT"], "search_quad": best["quad"],
               "novel": bool(nov > n_star),
               "tags": class_tags(zones, f)}
        cache[key] = rec
        return rec

    pop = []
    si = 0
    while len(pop) < POP0:
        zs = random_spec_wide(RNG, stratify=True,
                              force_overlap=(si % 3 == 1))
        si += 1
        if zs and well_formed_wide(zs):
            pop.append(zs)
    pool: dict[tuple, dict] = {}
    round_summaries = []
    round0_recs = None
    for rnd in range(ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[to_key(r["zones"])] = r
        if rnd == 0:
            round0_recs = list(recs)
        recs_sorted = sorted(recs, key=lambda r: r["J"])
        n_novel = sum(int(r["novel"]) for r in recs)
        n_novel_nd = sum(int(r["novel"] and r["tags"]["nondisjoint"])
                         for r in recs)
        n_novel_bl = sum(int(r["novel"]
                             and r["tags"]["n_below_line_zones"] > 0)
                         for r in recs)
        round_summaries.append({
            "round": rnd, "n": len(recs), "n_novel": n_novel,
            "n_novel_nondisjoint": n_novel_nd,
            "n_novel_below_line": n_novel_bl,
            "median_J": float(np.median([r["J"] for r in recs])),
            "best_J": float(recs_sorted[0]["J"]),
        })
        print(f"  search round {rnd}: n={len(recs)} novel={n_novel} "
              f"(nondisjoint {n_novel_nd}, below-line {n_novel_bl}) "
              f"median J {round_summaries[-1]['median_J']:.1f} "
              f"best J {recs_sorted[0]['J']:.2f}")
        if rnd == ROUNDS:
            break
        elites = [r["zones"] for r in recs_sorted[:N_ELITE]]
        pop = list(elites)
        while len(pop) < PER_ROUND:
            parent = elites[int(RNG.integers(0, len(elites)))]
            child = mutate_wide(parent, RNG)
            if child is not None and to_key(child) not in pool:
                pop.append(child)
            else:
                zs = random_spec_wide(RNG, stratify=False)
                if zs:
                    pop.append(zs)

    # ---- 4. the exp136 diagnosis re-tested on the widened pool ------
    pool_recs = list(pool.values())
    rho_round0 = spearman([r["nov_lib"] for r in round0_recs],
                          [r["search_quad"] for r in round0_recs])
    rho_pool = spearman([r["nov_lib"] for r in pool_recs],
                        [r["search_quad"] for r in pool_recs])
    pole_recs = [r for r in pool_recs
                 if r["tags"]["min_v"] >= NEURAL_LINE]
    rho_pole = (spearman([r["nov_lib"] for r in pole_recs],
                         [r["search_quad"] for r in pole_recs])
                if len(pole_recs) >= 3 else None)
    novel_recs = [r for r in pool_recs if r["novel"]]
    print(f"\n  diagnosis re-test (novelty vs writability): "
          f"Spearman(NOV, quad) round0 {rho_round0} | pool {rho_pool} "
          f"| pole-only subpool {rho_pole} "
          f"(exp136: anti-correlated INSIDE the pole domain)")
    print(f"  novel pool: {len(novel_recs)}/{len(pool_recs)} | "
          f"nondisjoint {sum(int(r['tags']['nondisjoint']) for r in novel_recs)}"
          f" | below-line {sum(int(r['tags']['n_below_line_zones'] > 0) for r in novel_recs)}"
          f" | with non-canon-adjacent boundaries "
          f"{sum(int(r['tags']['noncanon_adjacent_boundaries'] > 0) for r in novel_recs)}")

    # ---- 5. delivery: novelty + diversity + anti-recombination ------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    delivered: list[dict] = []
    for r in ordered:
        if len(delivered) >= N_DELIVER:
            break
        if not r["novel"]:
            continue
        f = r["f"]
        if any(dist(f, d["f"]) <= n_star for d in delivered):
            continue                                   # GATE-C4 filter
        ns = nov_splice(f, splices)
        if ns <= n_star:
            continue                                   # anti-recombination
        r = dict(r)
        r["nov_splice"] = ns
        delivered.append(r)
    print(f"  delivered {len(delivered)}/{N_DELIVER} inventions "
          f"({time.time() - t_start:.0f}s)\n")

    # ---- 6. the audit: two-channel quadrature + decode ----------------
    for k, r in enumerate(delivered):
        zones, f = r["zones"], r["f"]
        ladder_tbl = []
        emitted = None
        for (g, mu) in LADDER:
            eV, eT, q = quad_err(f, g, mu, seeds=AUDIT_SEEDS)
            full = float(np.mean([erosion(f, g, mu, "full", s)
                                  for s in AUDIT_SEEDS]))
            ladder_tbl.append({"cell": [g, mu], "eV": round(eV, 3),
                               "eT": round(eT, 3), "quad": round(q, 3),
                               "full": round(full, 3),
                               "pass": bool(q < ERR_BAR)})
            if emitted is None and q < ERR_BAR:
                emitted = (g, mu)
        r["ladder"] = ladder_tbl
        r["emitted_cell"] = list(emitted) if emitted else None
        r["audit_pass"] = emitted is not None
        if emitted is not None:
            g, mu = emitted
            dec = [decode(f, zones, g, mu, s) for s in AUDIT_SEEDS]
            r["decode_errs"] = [round(d["decode_err"], 3) for d in dec]
            r["hold_errs"] = [round(d["hold_err"], 3) for d in dec]
            n_ok = sum(int(d["decode_err"] < ERR_BAR
                           and d["hold_err"] < ERR_BAR) for d in dec)
            r["decode_stable_seeds"] = f"{n_ok}/{len(dec)}"
            r["decode_pass"] = bool(n_ok >= 2)
        else:
            r["decode_errs"] = None
            r["hold_errs"] = None
            r["decode_stable_seeds"] = "0/3"
            r["decode_pass"] = False
        pair_min = min((dist(f, d["f"]) for d in delivered if d is not r),
                       default=float("inf"))
        r["min_pairwise_D"] = round(float(pair_min), 2)
        print(f"  inv-{k + 1:02d} k={len(zones)} "
              f"nd={int(r['tags']['nondisjoint'])} "
              f"bl={r['tags']['n_below_line_zones']} "
              f"NOV {r['nov_lib']:.1f}/splice {r['nov_splice']:.1f} "
              f"emitted {r['emitted_cell']} "
              f"quad@emitted "
              f"{next((t['quad'] for t in ladder_tbl if t['pass']), None)} "
              f"decode {r['decode_stable_seeds']} "
              f"pairD {r['min_pairwise_D']:.1f}")

    # ---- 7. gates (wording unchanged from exp136) ---------------------
    n = len(delivered)
    c1 = bool(n == N_DELIVER
              and all(r["nov_lib"] > n_star and r["nov_splice"] > n_star
                      for r in delivered))
    audit_n = sum(int(r["audit_pass"]) for r in delivered)
    star_only = bool(audit_n >= 8
                     and all(r["emitted_cell"] == [64.0, 0.0]
                             for r in delivered if r["audit_pass"]))
    c2 = bool(audit_n >= 8)
    decode_n = sum(int(r["decode_pass"]) for r in delivered)
    c3 = bool(decode_n >= 8)
    c4 = bool(n == N_DELIVER and n >= 2 and
              all(r["min_pairwise_D"] > n_star for r in delivered))
    gates = {"C1_novelty_generation": c1, "C2_two_channel_audit": c2,
             "C3_decode_stability": c3, "C4_zero_anatomy_special": c4}
    quad_list = [next((t["quad"] for t in r["ladder"] if t["cell"]
                       == r["emitted_cell"]), np.nan)
                 for r in delivered if r["audit_pass"]]
    full_list = [next((t["full"] for t in r["ladder"] if t["cell"]
                       == r["emitted_cell"]), np.nan)
                 for r in delivered if r["audit_pass"]]
    quad_validity = (spearman(quad_list, full_list)
                     if len(quad_list) >= 3 else None)

    print(f"\n  GATE-C1 novelty generation (10 delivered, all beyond "
          f"N_STAR incl. splices): {'PASS' if c1 else 'REFUTED'}")
    print(f"  GATE-C2 two-channel audit ({audit_n}/{n} below the 6.0 bar "
          f"at the emitted cell; star-only={star_only}): "
          f"{'PASS' if c2 else 'REFUTED'}")
    print(f"  GATE-C3 decode+stability ({decode_n}/{n} decode and hold): "
          f"{'PASS' if c3 else 'REFUTED'}")
    print(f"  GATE-C4 zero-anatomy-is-special (min pairwise D "
          f"{min((r['min_pairwise_D'] for r in delivered), default=float('nan')):.1f} "
          f"vs N_STAR {n_star:.1f}): {'PASS' if c4 else 'REFUTED'}")
    npass = sum(int(v) for v in gates.values())
    print(f"\n  === {npass}/4 gates PASS ===")

    out = {
        "exp": "exp141_generator_wide (generator v6, widened domain "
               "— the L119 repair run)",
        "claim": ("the compiler can invent anatomies evolution never "
                  "made (novel beyond the frozen reference library's "
                  "own internal spread) that still decode under the "
                  "two-channel law — the exp136 claim unchanged; the "
                  "L119 repair widens the DOMAIN (full identity "
                  "repertoire [-60, -15] per exp128's canon-strip "
                  "re-pricing; non-disjoint exp94-class multi "
                  "programs) and re-derives N* before the search"),
        "repair_registered": {
            "source": "docs/FALSIFICATION.md L119 (exp136 diagnosis)",
            "a_domain_widening": (
                "voltage domain [-35,-15] -> [-60,-15] (the compiler's "
                "full identity repertoire, REPERTOIRE_LO/HI); justified "
                "by exp128's canon-strip re-pricing (L112): strip "
                "IMPROVES zone pricing (grid2d err_z0 3.21->1.19, "
                "err_z2 9.65->7.00; torus err_z0 6.03/brk 0.50 -> "
                "3.38/0.00, err_z2 7.52->4.71) — the below-line canon "
                "read is a TRADE-OFF (gap-fidelity bought with "
                "zone-drag toward the canon -50), so the near-trunk "
                "below-line shelf (-56,-44) is canon-CARRIED (the drag "
                "IS the decode there); the deep tail [-60,-56) admitted "
                "as an instruments-priced probe (the record's own "
                "exp87 -59/-60 entries and exp94's BELOW program live "
                "there; exp94's MS-G2 no-backdoor failures are the "
                "competing deposit)"),
            "b_multizone_nondisjoint": (
                "zones may touch/overlap (the exp94-class multi "
                "admission, the novelty-bearing class); exp136's "
                "gap>=0.02 clause retired (it forced canon tissue "
                "between zones, making non-canon-adjacent structure "
                "unreachable); overlap resolved by emission order "
                "(compiler clamp loop: later zone wins); cuts drawn "
                "uniform (the rejection clause stays retired)"),
            "c_n_star_rederived": (
                "N* recomputed on the frozen 72-member library with "
                "exp136's IDENTICAL metric and deposited BEFORE the "
                "search (stage n_star_deposit); sensitivity with "
                "exp94's BELOW as a 73rd member deposited alongside; "
                "the frozen 72-member bar governs"),
        },
        "metric": {
            "distance": "100 * d_struct + d_rms; d_struct = tolerant "
                        "boundary-set |Delta|/|cup| (match tol 0.01); "
                        "d_rms = profile RMS (mV) at n=100 — exp136's "
                        "metric, imported verbatim",
            "N_STAR_rule": "95th percentile of within-library "
                           "nearest-neighbor distances",
            "n_star": round(n_star, 3),
            "n_star_exp136_deposited": 82.288,
            "n_star_aug73_below_sensitivity": round(n_star_aug, 3),
            "library_nn": {"min": round(float(nn.min()), 2),
                           "median": round(float(np.median(nn)), 2),
                           "p95": round(float(np.percentile(nn, 95)), 2),
                           "max": round(float(nn.max()), 2)},
            "library": lib_names,
            "library_size": len(lib_names),
            "splice_family": int(len(splices)),
            "anti_recombination": "distance to every single-crossover "
                                  "splice (c in 0.05..0.95) > N_STAR",
        },
        "domain": {
            "voltage_domain": [WIDE_LO, WIDE_HI],
            "exp136_voltage_domain": [-35.0, -15.0],
            "bands": [list(b) for b in VBANDS],
            "disjointness": "retired — zones may touch/overlap "
                            "(emission-order resolution)",
            "width_min": 0.04, "span_max": 0.90,
            "exp128_canon_strip_citations": {
                "grid2d": {"err_z0": "3.21 -> 1.19",
                           "err_z2": "9.65 -> 7.00"},
                "torus": {"err_z0": "6.03 (brk 0.50) -> 3.38 (0.00)",
                          "err_z2": "7.52 -> 4.71"},
                "mechanism": "the canon read is a trade-off "
                             "(gap-fidelity bought with zone-drag); "
                             "its canon values (-50 trunk) drag zones "
                             "during the weak-pinning settle (L112)",
            },
        },
        "search": {
            "space": "1-5 zones (may touch/overlap), width >= 0.04, "
                     "voltages on the 0.1 mV grid in [-60, -15] (the "
                     "widened repertoire), hull span <= 0.90",
            "score": "J = quad_err_search + 5.0 * relu(N_STAR - NOV_lib)",
            "search_cells": [list(c) for c in SEARCH_CELLS],
            "seeding": "96 stratified seeds (zone count x axis thirds "
                       "x 6 voltage bands; 1/3 forced non-disjoint); "
                       "5 generations x 48 (16 elites + mutations incl. "
                       "the nest op)",
            "rounds": round_summaries,
            "pool_size": len(pool),
        },
        "diagnostics": {
            "exp136_diagnosis_retest": {
                "spearman_nov_vs_quad_round0": (round(rho_round0, 4)
                                                if rho_round0 is not None
                                                else None),
                "spearman_nov_vs_quad_pool": (round(rho_pool, 4)
                                              if rho_pool is not None
                                              else None),
                "spearman_nov_vs_quad_pole_only": (
                    round(rho_pole, 4) if rho_pole is not None else None),
                "note": ("exp136 found novelty ANTI-correlated with "
                         "writability inside the pole domain; the "
                         "widening's mechanism claim is that the "
                         "anti-correlation breaks once the "
                         "canon-carried below-line shelf and the "
                         "non-disjoint class are admitted"),
            },
            "novel_pool": {
                "count": len(novel_recs),
                "nondisjoint": sum(int(r["tags"]["nondisjoint"])
                                   for r in novel_recs),
                "with_below_line_zone": sum(
                    int(r["tags"]["n_below_line_zones"] > 0)
                    for r in novel_recs),
                "with_noncanon_adjacent_boundaries": sum(
                    int(r["tags"]["noncanon_adjacent_boundaries"] > 0)
                    for r in novel_recs),
            },
        },
        "inventions": [
            {"name": f"inv-{i + 1:02d}",
             "zones": [list(z) for z in r["zones"]],
             "tags": r["tags"],
             "nov_lib": round(r["nov_lib"], 2),
             "nov_splice": round(r["nov_splice"], 2),
             "min_pairwise_D": r["min_pairwise_D"],
             "emitted_cell": r["emitted_cell"],
             "ladder": r["ladder"],
             "audit_pass": r["audit_pass"],
             "decode_errs": r["decode_errs"],
             "hold_errs": r["hold_errs"],
             "decode_stable_seeds": r["decode_stable_seeds"],
             "decode_pass": r["decode_pass"]}
            for i, r in enumerate(delivered)
        ],
        "quadrature_validity_on_invented_map": {
            "spearman_quad_vs_full": (round(quad_validity, 4)
                                      if quad_validity is not None else None),
            "note": ("exp84's composition law re-tested on the "
                     "invented anatomies at their emitted cells "
                     "(diagnostic, not a gate)")},
        "criteria": gates,
        "star_only_degradation": bool(star_only),
        "delivered_count": n,
        "audit_pass_count": audit_n,
        "decode_pass_count": decode_n,
        "wall_s": round(time.time() - t_start, 1),
        "notes": (
            "The audit prices WRITABILITY (exp84's measured channel "
            "ablations: start at the invented pattern, let each "
            "channel erode for the 24 h window, compose in "
            "quadrature); C3 prices RE-DERIVATION (the exp90 "
            "two-source read after amputation of the zone span, then "
            "a 100 t.u. hold). The operating-point ladder is the "
            "price map's cells; the emitted cell is the cheapest "
            "passing rung and is part of the compiled program. The "
            "below-line class's decode path IS the canon read (L112's "
            "trade-off mechanism): deep-tail inventions are expected "
            "to strain C3 and the gate count owns that honestly."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
