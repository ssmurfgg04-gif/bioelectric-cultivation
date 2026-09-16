#!/usr/bin/env python3
"""exp146 — THE SPLICE BAR (family-internal re-derivation; workstream L;
the L124-registered repair: the corpus-defines-threshold rule was applied
to the 72-member library but never to the 48,564-profile splice family
the library itself induces — re-derive the anti-recombination bar from
the SPLICE FAMILY'S OWN internal spread, BEFORE any further gate run).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates are
executed exactly once against these clauses):
======================================================================

MOTIVE (L124's owned diagnosis v3): exp144 re-localized the killer —
NOT the audit (24/24 diagnostic-fill candidates pass the two-channel
audit at the frozen 9-rung ladder, eV/eTheta all << 6.0,
Spearman(NOV_lib, best-rung quad) = -0.607) but the ANTI-RECOMBINATION
SPLICE CLAUSE: 0/96 library-novel candidates clear nov_splice > N*
(best nov_splice 65.37 vs bar 82.29); exp141's audit never even
executed. exp136's wording made the splice check part of C1's novelty
clause, and the bar was calibrated from the LIBRARY's internal spread
(95th-pct NN = 82.288) while the family the library induces blankets
the widened space far more densely. THE REPAIR UNDER TEST: apply the
SAME 95th-percentile nearest-neighbor rule to the splice corpus itself
— symmetric with N*'s derivation, zero knobs.

DESIGN:
  (1) THE SPLICE FAMILY: exp136's build_splices VERBATIM on the frozen
      72-member library: all C(72,2) = 2556 pairs x 19 crossover
      fractions {0.05, ..., 0.95} = 48,564 single-crossover profiles.
      The library N*_lib is re-derived (library_nn_stats verbatim) and
      asserted = 82.288 (exp136/exp144 deposited; CUT_TOL 0.01).
  (2) THE NEW BAR, deposited at stage "bar_deposit" BEFORE the search's
      first candidate is evaluated:
        N*_splice = np.percentile(nn, 95) over all 48,564 family
        members, nn(s) = min over family members s' at a DIFFERENT
        INDEX of dist(s, s') — the library_nn_stats rule applied to S
        verbatim, including its symmetric-storage convention: the pair
        distance is computed ONCE as D[i,j] = dist(S[i], S[j]) for the
        index-ordered pair i < j and stored both ways (d_struct's
        greedy is B1-driven, so the metric is directed; the index rule
        fixes the direction by index order). Same metric
        (dist = 100*d_struct + d_rms, exp136's, imported verbatim).
        Members whose profile appears at >= 2 indices get nn = 0 by
        this rule (a duplicate partner sits at distance exactly 0) —
        the family's own redundancy is part of its spread and is
        DEPOSITED (duplicate-class histogram, nn histogram, percentile
        table). EXACTNESS INSTRUMENT: the verbatim dist is ~40 us/pair
        (all-pairs = 782 min), so an EXACT vectorized re-implementation
        of d_struct's greedy (replicating its argmin-over-all-B2
        nearest, no-fallback-on-used semantics AND its float tolerance
        comparisons via precomputed float tables TOLF[i,j] =
        abs(j/N - i/N) and TOLB = TOLF <= CUT_TOL — adjacent lattice
        cuts are NOT always within tolerance in float64: e.g.
        abs(5/100 - 4/100) = 0.010000000000000002 > 0.01) is verified
        against the verbatim metric BEFORE any bar or selection is
        computed, on: 4,000 random family pairs (index-ordered
        direction); 6 random wide-domain candidate profiles x 4,000
        random family members; 2 candidates vs the FULL family
        (nov_splice end-to-end); and 12 random singletons' full
        index-rule NN recomputed with the VERBATIM metric (both metric
        directions, per the symmetric-storage convention). ANY mismatch
        ABORTS the run before selection (fail-loud, pre-registered).
  (3) THE REPAIRED CLAUSE (stated exactly, before the run): a search
      candidate clears iff
        NOV_lib(f) > N*_lib  AND  nov_splice(f) > N*_splice
      where nov_splice(f) = min over the FULL family S of dist(f, s)
      (exp136 verbatim, direction (candidate, splice)). Everything
      else in exp136's delivery procedure is UNCHANGED: J-order greedy,
      pairwise C4 filter dist(f, d) <= N*_lib skips, cap 10.
  (4) DELIVERED candidates -> the exp144 frozen 9-rung ladder audit
      VERBATIM (rungs, provenance, cost key gamma/4 + (1 if mu>0),
      pass = hypot(eV, eT) < 6.0 at seeds (1,2,3), emitted = argmin
      cost over PASSING rungs) -> decode+hold at the emitted rung ->
      exp136's gates C1-C4 UNCHANGED, evaluated in this same run.
  (5) THE SILENT-FREEBIE CHECK (part of the gate, not an afterthought;
      the L124 warning: the delivered-cell (1.0, 0.0) MU0_SILENCE rung
      carries a SILENT-ONLY freebie risk, the mirror of exp136's
      star-only clause): any delivered invention that verifies ONLY at
      mu = 0 rungs (no rung with mu > 0 and quad < 6.0) is flagged
      silent_only and EXCLUDED from the C2/C3 counts (primary,
      registered reading: removed from both numerator and denominator;
      the secondary reading — excluded from the numerator only — is
      deposited alongside for transparency). The flag list is
      deposited with each flagged invention's full rung table.

GATES (pre-registered):
  GATE-L1  BAR DEPOSIT ORDER (procedural): N*_splice deposited at
           stage bar_deposit BEFORE the search re-runs; the rule is
           the verbatim library_nn_stats semantics (95th pct, same
           metric, index-based self-exclusion, symmetric storage);
           the fast/verbatim verification harness passed. PASS iff all
           three hold.
  GATE-L2  MINIMUM REVIVAL: >= 1 delivered candidate clears the
           repaired clause AND passes the two-channel audit at some
           rung of the frozen ladder AND is NOT silent-only.
  GATE-L3  = C2 UNCHANGED + silent-freebie exclusion: >= 8/10 of the
           delivered (silent-only excluded, primary reading) pass the
           audit at their emitted rung.
  GATE-L4  = C3 UNCHANGED + silent-freebie exclusion: >= 8/10 of the
           delivered (silent-only excluded, primary reading) decode
           under the existing decoder at the emitted rung: post-settle
           error < 6.0 mV AND 100 t.u. hold error < 6.0 mV on >= 2/3
           seeds.
  C1       UNCHANGED except the clause it references: exactly 10
           delivered, each clearing the repaired novelty clause
           (NOV_lib > N*_lib AND nov_splice > N*_splice).
  C4       UNCHANGED: pairwise min D > N*_lib among delivered.

BRANCHES (pre-registered):
  - delivery >= 8: full gate evaluation (all six clauses above).
  - delivery 1-7: deposit as PARTIAL with C1's verdict per its own
    wording (REFUTED unless exactly 10 delivered each clearing the
    repaired clause) and the binding stage identified (splice clause
    vs C4 pairwise filter vs audit).
  - delivery 0: the splice clause REMAINS load-bearing even at its own
    family-internal bar — deposit its ROC: a pre-named bar grid
    (family nn percentiles P50..P100, the old library bar, and the
    max candidate nov_splice + 1) with, per bar: splice-clear count,
    greedy+C4 delivered count, and how many delivered would be
    audited-passing (the top-24 lib-novel-by-J candidates are audited
    once, exp144's fill scope, so the projection uses MEASURED audit
    outcomes, plus the silent-check status of each) — and the
    family-spread diagnosis (duplicate mass, nn distribution) of WHY
    the bar exists at the value it takes.

INSTRUMENT DISCLOSURE: exp136/exp141/exp144 machinery imported verbatim
(profile_of_zones, build_library, dist, library_nn_stats, build_splices,
nov_lib, nov_splice, quad_err, erosion, decode, ERR_BAR, AUDIT_SEEDS,
LAMBDA_NOV, N_DELIVER, CUT_TOL; exp141's wide search functions, seed
141, search shape and score J; exp144's EXTENDED_LADDER, PROVENANCE and
rung cost key). The search re-run is exp141's loop verbatim at its seed
and is CHECKED against exp141's deposited aggregates (as exp144 did).
The ONLY new objects are (a) the bar's derivation corpus (the family
instead of the library) and (b) an exact vectorized evaluator of the
UNCHANGED metric (verified against the verbatim metric pre-selection,
with the delivered candidates' nov_splice values additionally
re-verified with the verbatim metric in full before gates are
evaluated).
RUNTIME BUDGET: family NN ~2 min + verification ~1 min + search ~4 min
+ splice scan + audit <= 10 x 9 rungs x 6 ablation runs + decodes;
wall under ~15 min, serial, BLAS pinned.
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

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, LADDER as POLE_LADDER, SEARCH_CELLS, CELL_SURCHARGE,
    AUDIT_SEEDS, LAMBDA_NOV, N_DELIVER, CUT_TOL, N as LAT_N,
    profile_of_zones, build_library, dist, library_nn_stats,
    build_splices, nov_lib, nov_splice, quad_err, erosion, decode,
)
from experiments import exp141_generator_wide as W  # noqa: E402
from experiments.exp144_audit_operating_points import (  # noqa: E402
    EXTENDED_LADDER, PROVENANCE, rung_cost,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp146_splice_bar.json")
PREV = os.path.join(ROOT, "results", "exp141_generator_wide.json")

BLOCK = 8192                            # fast-path block size


# ==================================================================
# the EXACT vectorized evaluator of the UNCHANGED metric
# (dist = 100*d_struct + d_rms; verified against dist() pre-selection)
# ==================================================================
def make_tol_tables():
    """TOLF[i,j] = abs(j/N - i/N) with the verbatim float64 ops;
    TOLB = TOLF <= CUT_TOL. d_struct's tolerance test is per-pair in
    float — adjacent lattice cuts are NOT always within tolerance."""
    pos = np.arange(100, dtype=float) / LAT_N
    tolf = np.abs(pos[None, :] - pos[:, None])
    return tolf, tolf <= CUT_TOL


TOLF, TOLB = make_tol_tables()


def cut_mask(f: np.ndarray) -> np.ndarray:
    """Boolean lattice mask of cuts (positions 1..99), identical to
    cuts_of's test f[i] != f[i-1]."""
    m = np.zeros(len(f), dtype=bool)
    m[1:] = f[1:] != f[:-1]
    return m


def _false(n):
    return np.zeros(n, dtype=bool)


def fast_dist_fwd(f1, mask1, len1, F2, M2, L2):
    """dist(f1, f2_r) for a block — B1 = f1's cuts (scalar profile),
    B2 = each row's cuts. EXACTLY replicates d_struct's greedy: for
    each b in B1 ascending, j* = argmin over ALL of B2 of |B2[j]-b|
    (float64 ops, ties -> first index = lowest value); match iff B2[j*]
    unused and |B2[j*]-b| <= tol — NO fallback to the next-nearest when
    the nearest is used. When b is present in B2 it is the strictly
    nearest (distance 0); otherwise only b-1/b+1 can be within
    tolerance, and anything farther is out of tolerance anyway. Used-
    state and counts follow the verbatim formulas."""
    B = F2.shape[0]
    diff = F2 - f1
    rms = np.sqrt(np.einsum("ij,ij->i", diff, diff) / len(f1))
    used = np.zeros((B, 100), dtype=bool)
    hits = np.zeros(B, dtype=np.int64)
    for b in np.flatnonzero(mask1):
        assert b >= 1, "cut at lattice 0 impossible"
        col_b = M2[:, b]
        # b present in B2 -> nearest is b (distance 0, strictly minimal)
        m0 = col_b & ~used[:, b]
        hits += m0
        if m0.any():
            used[np.flatnonzero(m0), b] = True
        nb = ~col_b                       # b absent -> nearest at +-1?
        hasL = (M2[:, b - 1] & nb) if b >= 2 else _false(B)
        hasR = (M2[:, b + 1] & nb) if b <= 98 else _false(B)
        if hasL.any() or hasR.any():
            # argmin tie between b-1 and b+1: strictly smaller float
            # |B2[j]-b| wins; bit-equal -> first index (b-1, lower)
            if b >= 2 and b <= 98:
                pickL = hasL & (~hasR |
                                (TOLF[b - 1, b] <= TOLF[b, b + 1]))
            elif b >= 2:
                pickL = hasL
            else:
                pickL = _false(B)
            pickR = hasR & ~pickL
            if b >= 2 and TOLB[b - 1, b]:
                mL = pickL & ~used[:, b - 1]
                hits += mL
                if mL.any():
                    used[np.flatnonzero(mL), b - 1] = True
            if b <= 98 and TOLB[b, b + 1]:
                mR = pickR & ~used[:, b + 1]
                hits += mR
                if mR.any():
                    used[np.flatnonzero(mR), b + 1] = True
    un1 = len1 - hits
    un2 = L2 - hits
    matched = (len1 + L2 - un1 - un2) // 2
    union = matched * 2 + un1 + un2
    d = np.zeros(B, dtype=float)
    np.divide(un1 + un2, union, out=d, where=union > 0)
    return 100.0 * d + rms


def fast_dist_rev(f2, mask2, len2, F1, M1, L1):
    """dist(f1_r, f2) for a block — B1 = each row's cuts (variable),
    B2 = f2's cuts (fixed). The greedy walks each row's B1 in ascending
    order, so a single ascending lattice loop covers every row exactly
    as the verbatim loop would; the B2-side decisions (nearest value,
    tolerance) are scalar per b; only the used-state is per-row."""
    B = F1.shape[0]
    diff = F1 - f2
    rms = np.sqrt(np.einsum("ij,ij->i", diff, diff) / len(f2))
    used = np.zeros((B, 100), dtype=bool)
    hits = np.zeros(B, dtype=np.int64)
    for b in range(1, 100):
        active = M1[:, b]
        if not active.any():
            continue
        if mask2[b]:
            m0 = active & ~used[:, b]
            hits += m0
            if m0.any():
                used[np.flatnonzero(m0), b] = True
            continue
        hasL = bool(mask2[b - 1]) if b >= 2 else False
        hasR = bool(mask2[b + 1]) if b <= 98 else False
        if not hasL and not hasR:
            continue                       # nearest out of tolerance
        if hasL and hasR:
            pickL = TOLF[b - 1, b] <= TOLF[b, b + 1]
        else:
            pickL = hasL
        if pickL and TOLB[b - 1, b]:
            mL = active & ~used[:, b - 1]
            hits += mL
            if mL.any():
                used[np.flatnonzero(mL), b - 1] = True
        elif (not pickL) and TOLB[b, b + 1]:
            mR = active & ~used[:, b + 1]
            hits += mR
            if mR.any():
                used[np.flatnonzero(mR), b + 1] = True
    un1 = L1 - hits
    un2 = len2 - hits
    matched = (L1 + len2 - un1 - un2) // 2
    union = matched * 2 + un1 + un2
    d = np.zeros(B, dtype=float)
    np.divide(un1 + un2, union, out=d, where=union > 0)
    return 100.0 * d + rms


def fast_nov_splice(f: np.ndarray, F2: np.ndarray, M2: np.ndarray,
                    L2: np.ndarray) -> float:
    """min over the family of dist(f, s) — exp136 nov_splice's direction
    (candidate, splice), exact fast evaluator."""
    mask1 = cut_mask(f)
    len1 = int(mask1.sum())
    best = np.inf
    for i in range(0, len(F2), BLOCK):
        d = fast_dist_fwd(f, mask1, len1, F2[i:i + BLOCK],
                          M2[i:i + BLOCK], L2[i:i + BLOCK])
        best = min(best, float(d.min()))
    return best


# ==================================================================
# the family-internal bar (library_nn_stats rule applied to S)
# ==================================================================
def splice_family_bar(S: np.ndarray):
    """N*_splice = 95th-pct of index-rule NN distances within S, with
    the library_nn_stats symmetric-storage convention: the pair
    distance is computed once as dist(S[i], S[j]) for i < j. Members
    of duplicate classes (identical profile at >= 2 indices) get
    nn = 0 exactly. Exact via the verified fast evaluator; the index
    convention is honored through per-class min/max original index:
    for a singleton s at index p and another class C (identical
    profile r for every member), dist(r, s) is admissible iff C has a
    member at index < p, and dist(s, r) iff C has a member at
    index > p."""
    n = len(S)
    void = np.ascontiguousarray(S).view(
        np.dtype((np.void, S.dtype.itemsize * S.shape[1]))).ravel()
    _, inv, cnt = np.unique(void, return_inverse=True, return_counts=True)
    n_cls = len(cnt)
    reps = np.zeros((n_cls, S.shape[1]))
    reps[inv] = S                       # class id -> its (unique) profile
    rmask = np.zeros((n_cls, 100), dtype=bool)
    rmask[:, 1:] = reps[:, 1:] != reps[:, :-1]
    rlen = rmask.sum(axis=1)
    idx = np.arange(n)
    min_idx = np.full(n_cls, n)
    max_idx = np.full(n_cls, -1)
    np.minimum.at(min_idx, inv, idx)
    np.maximum.at(max_idx, inv, idx)
    singles = np.flatnonzero(cnt == 1)
    nn = np.zeros(n)                    # duplicates: nn = 0 exactly
    t0 = time.time()
    for k, p in enumerate(singles):
        c = inv[p]
        s = reps[c]
        smask = rmask[c]
        slen = int(rlen[c])
        others = np.concatenate([np.arange(0, c),
                                 np.arange(c + 1, n_cls)])
        R = reps[others]
        RM = rmask[others]
        RL = rlen[others]
        fA = np.empty(len(others))      # dist(s -> r)
        fB = np.empty(len(others))      # dist(r -> s)
        for i in range(0, len(others), BLOCK):
            sl = slice(i, i + BLOCK)
            fA[sl] = fast_dist_fwd(s, smask, slen, R[sl], RM[sl], RL[sl])
            fB[sl] = fast_dist_rev(s, smask, slen, R[sl], RM[sl], RL[sl])
        # index convention per class
        okA = max_idx[others] > p       # dist(s, r) admissible
        okB = min_idx[others] < p       # dist(r, s) admissible
        cands = []
        if okA.any():
            cands.append(float(fA[okA].min()))
        if okB.any():
            cands.append(float(fB[okB].min()))
        nn[p] = min(cands) if cands else 0.0
        if k % 2000 == 0:
            print(f"    nn[{k + 1}/{len(singles)}] "
                  f"({time.time() - t0:.0f}s)")
    n_star_splice = float(np.percentile(nn, 95))
    return n_star_splice, nn, dict(reps=reps, rmask=rmask, rlen=rlen,
                                   inv=inv, cnt=cnt, singles=singles,
                                   min_idx=min_idx, max_idx=max_idx)


def main() -> dict:
    t0 = time.time()
    print("=== exp146: the splice bar (family-internal re-derivation) ===\n")

    # ---- 0. frozen library, deposited bar N*_lib --------------------
    lib = build_library()
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    n_star, nn_lib = library_nn_stats(lib)
    print(f"  library {len(lib_names)} members | N*_lib {n_star:.3f} "
          f"(deposited 82.288)")
    assert abs(n_star - 82.288) < 0.01, "N*_lib re-derivation drift"

    # ---- 1. the splice family + VERIFICATION HARNESS ----------------
    S = build_splices(lib)
    print(f"  splice family: {len(S)} single-crossover profiles "
          f"(C(72,2) x 19); t={time.time() - t0:.0f}s")
    rng = np.random.default_rng(146)
    harness = {}
    pair_idx = rng.integers(0, len(S), size=(4000, 2))
    worst = 0.0
    for a, b in pair_idx:
        if a == b:
            continue
        i, j = min(a, b), max(a, b)
        m1, m2 = cut_mask(S[i]), cut_mask(S[j])
        fast = float(fast_dist_fwd(S[i], m1, int(m1.sum()),
                                   S[j][None], m2[None],
                                   np.array([int(m2.sum())]))[0])
        worst = max(worst, abs(fast - dist(S[i], S[j])))
    harness["family_pairs_4000_max_abs_diff"] = worst
    print(f"  harness: 4000 family pairs (i<j direction), "
          f"max|fast-verbatim| {worst:.2e}")
    assert worst < 1e-9, "fast evaluator diverged from verbatim dist"
    # reverse direction too (used by the index rule)
    worst = 0.0
    for a, b in pair_idx[:2000]:
        if a == b:
            continue
        i, j = min(a, b), max(a, b)
        m1, m2 = cut_mask(S[i]), cut_mask(S[j])
        fast = float(fast_dist_rev(S[j], m2, int(m2.sum()),
                                   S[i][None], m1[None],
                                   np.array([int(m1.sum())]))[0])
        worst = max(worst, abs(fast - dist(S[i], S[j])))
    harness["family_pairs_reverse_2000_max_abs_diff"] = worst
    print(f"  harness: 2000 family pairs (reverse direction), "
          f"max|fast-verbatim| {worst:.2e}")
    assert worst < 1e-9, "fast reverse evaluator diverged"

    # random wide candidates (independent rng; search rng untouched)
    wcand = []
    while len(wcand) < 6:
        zs = W.random_spec_wide(rng, stratify=(len(wcand) % 2 == 0))
        if zs and W.well_formed_wide(zs):
            wcand.append(profile_of_zones(zs))
    fm = np.zeros((len(S), 100), dtype=bool)
    fm[:, 1:] = S[:, 1:] != S[:, :-1]
    fl = fm.sum(axis=1)
    worst = 0.0
    for f in wcand:
        pick = rng.integers(0, len(S), 4000)
        m1 = cut_mask(f)
        dfast = fast_dist_fwd(f, m1, int(m1.sum()), S[pick], fm[pick],
                              fl[pick])
        dverb = np.array([dist(f, S[q]) for q in pick])
        worst = max(worst, float(np.max(np.abs(dfast - dverb))))
    harness["candidate_x_family_6x4000_max_abs_diff"] = worst
    print(f"  harness: 6 candidates x 4000 members, "
          f"max|fast-verbatim| {worst:.2e}")
    assert worst < 1e-9, "fast evaluator diverged on candidate profiles"
    for f in wcand[:2]:
        v = nov_splice(f, S)
        q = fast_nov_splice(f, S, fm, fl)
        harness.setdefault("nov_splice_full_family", []).append(
            {"fast": round(q, 9), "verbatim": round(v, 9)})
        assert abs(q - v) < 1e-9, "nov_splice end-to-end divergence"
    print("  harness: 2 candidates vs FULL family (nov_splice "
          "end-to-end): exact")

    # ---- 2. THE BAR (deposited BEFORE the search) --------------------
    n_star_splice, nn_arr, aux = splice_family_bar(S)
    pcts = {f"P{p}": round(float(np.percentile(nn_arr, p)), 3)
            for p in (50, 60, 70, 80, 90, 95, 99, 100)}
    print(f"  N*_splice {n_star_splice:.3f} (old library bar "
          f"{n_star:.3f}) | percentiles {pcts}")
    # 12 singletons: full index-rule NN re-verified with the VERBATIM metric
    sng = aux["singles"]
    inv, cnt = aux["inv"], aux["cnt"]
    reps, rmask, rlen = aux["reps"], aux["rmask"], aux["rlen"]
    min_idx, max_idx = aux["min_idx"], aux["max_idx"]
    n_cls = len(cnt)
    pick = np.sort(rng.choice(sng, 12, replace=False))
    worst = 0.0
    for p in pick:
        c = inv[p]
        others = np.concatenate([np.arange(0, c),
                                 np.arange(c + 1, n_cls)])
        vals = []
        for r in others:
            if min_idx[r] < p:
                vals.append(dist(reps[r], S[p]))
            if max_idx[r] > p:
                vals.append(dist(S[p], reps[r]))
        worst = max(worst, abs(min(vals) - nn_arr[p]))
    harness["singleton_nn_12_verbatim_max_abs_diff"] = worst
    print(f"  harness: 12 singletons' full index-rule NN vs verbatim: "
          f"max diff {worst:.2e}")
    assert worst < 1e-9, "index-rule NN diverged from verbatim metric"
    dup = int((cnt >= 2).sum())
    stage_order = ["bar_deposit"]
    with open(OUT, "w") as fh:
        json.dump({
            "exp": "exp146_splice_bar (workstream L)",
            "stage": "bar_deposit (written BEFORE the search runs)",
            "stage_order": stage_order,
            "pre_registered_clause": (
                "clear iff NOV_lib > N*_lib AND nov_splice > N*_splice; "
                "N*_splice = 95th-pct index-rule NN within the 48,564-"
                "profile splice family, library_nn_stats semantics "
                "(same metric, symmetric storage, i<j computed once)"),
            "n_star_lib": round(n_star, 3),
            "n_star_splice": round(n_star_splice, 3),
            "bar_ratio": round(n_star_splice / n_star, 4),
            "family": {"size": int(len(S)),
                       "distinct_profiles": int(n_cls),
                       "duplicate_classes": dup,
                       "singletons": int(len(sng)),
                       "max_class_size": int(cnt.max()),
                       "members_in_duplicate_classes":
                           int(cnt[cnt >= 2].sum())},
            "nn_percentiles": pcts,
            "nn_histogram": {"bin_edges":
                             [round(x, 2) for x in
                              np.histogram_bin_edges(nn_arr, bins=20)],
                             "counts": [int(x) for x in
                                        np.histogram(nn_arr, bins=20)[0]]},
            "verification_harness": harness,
        }, fh, indent=1, default=float)
    print("  BAR DEPOSITED (stage bar_deposit) BEFORE the search\n")

    # ---- 3. the search re-run (exp141's loop VERBATIM, seed 141) ----
    rng = np.random.default_rng(141)
    cache: dict[tuple, dict] = {}

    def evaluate(zones) -> dict:
        key = W.to_key(zones)
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
               "tags": W.class_tags(zones, f)}
        cache[key] = rec
        return rec

    pop = []
    si = 0
    while len(pop) < W.POP0:
        zs = W.random_spec_wide(rng, stratify=True,
                                force_overlap=(si % 3 == 1))
        si += 1
        if zs and W.well_formed_wide(zs):
            pop.append(zs)
    pool: dict[tuple, dict] = {}
    round_summaries = []
    for rnd in range(W.ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[W.to_key(r["zones"])] = r
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
              f"best J {recs_sorted[0]['J']:.2f}")
        if rnd == W.ROUNDS:
            break
        elites = [r["zones"] for r in recs_sorted[:W.N_ELITE]]
        pop = list(elites)
        while len(pop) < W.PER_ROUND:
            parent = elites[int(rng.integers(0, len(elites)))]
            child = W.mutate_wide(parent, rng)
            if child is not None and W.to_key(child) not in pool:
                pop.append(child)
            else:
                zs = W.random_spec_wide(rng, stratify=False)
                if zs:
                    pop.append(zs)

    prev = json.load(open(PREV))
    rep_rounds = []
    for a, b in zip(round_summaries, prev["search"]["rounds"]):
        ok = (a["round"] == b["round"] and a["n"] == b["n"]
              and a["n_novel"] == b["n_novel"]
              and a["n_novel_nondisjoint"] == b["n_novel_nondisjoint"]
              and a["n_novel_below_line"] == b["n_novel_below_line"]
              and abs(a["best_J"] - b["best_J"]) < 1e-9)
        rep_rounds.append({"round": a["round"], "match": bool(ok)})
    rep = {"rounds_match": all(r["match"] for r in rep_rounds),
           "pool_size_match": len(pool) == prev["search"]["pool_size"],
           "rounds": rep_rounds,
           "pool_size": len(pool),
           "exp141_pool_size": prev["search"]["pool_size"]}
    print(f"  replication vs exp141 deposit: rounds "
          f"{rep['rounds_match']} | pool {len(pool)} vs "
          f"{prev['search']['pool_size']} -> "
          f"{'IDENTICAL' if rep['rounds_match'] and rep['pool_size_match'] else 'DIVERGED'}")
    assert rep["rounds_match"] and rep["pool_size_match"], \
        "search re-run diverged from the exp141 deposit"

    # ---- 4. the funnel under the REPAIRED clause ---------------------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    eligible = [r for r in ordered if r["novel"]]
    print(f"\n  lib-novel pool: {len(eligible)}/{len(pool)}")
    for r in eligible:
        r["nov_splice"] = fast_nov_splice(r["f"], S, fm, fl)
    splice_clear = [r for r in eligible if r["nov_splice"] > n_star_splice]
    print(f"  splice-clear under N*_splice {n_star_splice:.3f}: "
          f"{len(splice_clear)}/{len(eligible)} "
          f"(old bar {n_star:.3f} cleared "
          f"{sum(int(r['nov_splice'] > n_star) for r in eligible)})"
          f" | best nov_splice {max(r['nov_splice'] for r in eligible):.2f}")

    # delivered: exp136's greedy VERBATIM, repaired clause spliced in
    delivered: list[dict] = []
    for r in eligible:
        if len(delivered) >= N_DELIVER:
            break
        f = r["f"]
        if any(dist(f, d["f"]) <= n_star for d in delivered):
            continue                                   # GATE-C4 filter
        if r["nov_splice"] <= n_star_splice:
            continue                                   # repaired clause
        delivered.append(r)
    n_del = len(delivered)
    print(f"  delivered {n_del}/{N_DELIVER} (exp136 procedure, "
          f"repaired clause)")

    if n_del == 0:
        # ---- REFUTATION BRANCH: the clause is still load-bearing ----
        roc = []
        audited = eligible[:24]   # exp144's fill scope, pre-registered
        for r in audited:
            tbl = []
            for (g, mu) in EXTENDED_LADDER:
                eV, eT, q = quad_err(r["f"], g, mu, seeds=AUDIT_SEEDS)
                tbl.append({"cell": [g, mu], "quad": round(q, 3),
                            "pass": bool(q < ERR_BAR),
                            "silent": bool(mu == 0.0)})
            r["roc_ladder"] = tbl
            r["roc_pass"] = any(t["pass"] for t in tbl)
            r["roc_nonsilent_pass"] = any(t["pass"] and not t["silent"]
                                          for t in tbl)
        grid = sorted(set([n_star_splice, n_star] +
                          [float(np.percentile(nn_arr, p))
                           for p in (50, 60, 70, 80, 90, 95, 99, 100)] +
                          [max(r["nov_splice"] for r in eligible) + 1.0]))
        for bar in grid:
            clr = [r for r in eligible if r["nov_splice"] > bar]
            dset: list[dict] = []
            for r in clr:
                if len(dset) >= N_DELIVER:
                    break
                if any(dist(r["f"], d["f"]) <= n_star for d in dset):
                    continue
                dset.append(r)
            roc.append({"bar": round(bar, 3),
                        "splice_clear": len(clr),
                        "delivered": len(dset),
                        "delivered_audit_pass_projected": sum(
                            int(a["roc_pass"]) for a in audited
                            if any(a is r for r in dset)),
                        "delivered_nonsilent_pass_projected": sum(
                            int(a["roc_nonsilent_pass"]) for a in audited
                            if any(a is r for r in dset))})
        out = {
            "exp": "exp146_splice_bar (workstream L)",
            "branch": "REFUTATION (delivery 0): the splice clause is "
                      "still load-bearing at its own family-internal bar",
            "stage_order": stage_order + ["search", "funnel",
                                          "roc_deposit"],
            "pre_registered_clause": (
                "clear iff NOV_lib > N*_lib AND nov_splice > N*_splice"),
            "n_star_lib": round(n_star, 3),
            "n_star_splice": round(n_star_splice, 3),
            "verification_harness": harness,
            "replication_of_exp141": rep,
            "funnel": {"pool": len(pool), "lib_novel": len(eligible),
                       "splice_clear_new_bar": len(splice_clear),
                       "splice_clear_old_bar":
                           sum(int(r["nov_splice"] > n_star)
                               for r in eligible),
                       "best_nov_splice":
                           round(max(r["nov_splice"] for r in eligible), 2),
                       "delivered": 0},
            "nov_splice_all_lib_novel": [
                {"J": round(r["J"], 4),
                 "nov_lib": round(r["nov_lib"], 2),
                 "nov_splice": round(r["nov_splice"], 3)}
                for r in eligible],
            "roc": roc,
            "roc_audited_top24": [
                {"J": round(r["J"], 4),
                 "nov_splice": round(r["nov_splice"], 3),
                 "audit_pass": r["roc_pass"],
                 "nonsilent_pass": r["roc_nonsilent_pass"],
                 "ladder": r["roc_ladder"]}
                for r in audited],
            "family_spread_diagnosis": {
                "nn_percentiles": pcts,
                "members_in_duplicate_classes":
                    int(cnt[cnt >= 2].sum()),
                "max_class_size": int(cnt.max()),
                "note": "the corpus-defines-threshold rule applied to "
                        "the corpus the library itself induces"},
            "gates": {"L1_bar_deposit_order": True,
                      "L2_minimum_revival": False,
                      "L3_C2_audit": False, "L4_C3_decode": False,
                      "C1_novelty_generation": False,
                      "C4_zero_anatomy_special": False},
            "wall_s": round(time.time() - t0, 1),
        }
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1, default=float)
        print(f"\n  REFUTATION BRANCH deposited -> {OUT}")
        return out

    # ---- 5. the audit at exp144's frozen ladder (VERBATIM) ----------
    for k, r in enumerate(delivered):
        zones, f = r["zones"], r["f"]
        tbl = []
        for (g, mu) in EXTENDED_LADDER:
            eV, eT, q = quad_err(f, g, mu, seeds=AUDIT_SEEDS)
            tbl.append({"cell": [g, mu], "cost": rung_cost(g, mu),
                        "eV": round(eV, 3), "eT": round(eT, 3),
                        "quad": round(q, 3),
                        "pass": bool(q < ERR_BAR),
                        "silent": bool(mu == 0.0)})
        passing = [t for t in tbl if t["pass"]]
        nonsilent_pass = [t for t in passing if not t["silent"]]
        if passing:
            emitted_t = min(passing, key=lambda t: t["cost"])
            g, mu = emitted_t["cell"]
            full = float(np.mean([erosion(f, g, mu, "full", s)
                                  for s in AUDIT_SEEDS]))
            emitted_t["full"] = round(full, 3)
            dec = [decode(f, zones, g, mu, s) for s in AUDIT_SEEDS]
            r["decode_errs"] = [round(d["decode_err"], 3) for d in dec]
            r["hold_errs"] = [round(d["hold_err"], 3) for d in dec]
            n_ok = sum(int(d["decode_err"] < ERR_BAR
                           and d["hold_err"] < ERR_BAR) for d in dec)
            r["decode_stable_seeds"] = f"{n_ok}/{len(dec)}"
            r["decode_pass"] = bool(n_ok >= 2)
            r["emitted_cell"] = [g, mu]
        else:
            g, mu = min(tbl, key=lambda t: t["quad"])["cell"]
            full = float(np.mean([erosion(f, g, mu, "full", s)
                                  for s in AUDIT_SEEDS]))
            tbl[[t["cell"] for t in tbl].index([g, mu])]["full"] = \
                round(full, 3)
            r["emitted_cell"] = None
            r["decode_errs"] = r["hold_errs"] = None
            r["decode_stable_seeds"] = "0/3"
            r["decode_pass"] = False
        r["audit_pass"] = bool(passing)
        # THE SILENT-FREEBIE CHECK (part of the gate)
        r["nonsilent_pass"] = bool(nonsilent_pass)
        r["silent_only"] = bool(passing and not nonsilent_pass)
        r["ladder"] = tbl
        print(f"  audit[{k + 1}/{n_del}] J={r['J']:.2f} "
              f"nov_splice={r['nov_splice']:.2f} "
              f"audit_pass={r['audit_pass']} "
              f"emitted={r['emitted_cell']} "
              f"nonsilent_pass={r['nonsilent_pass']} "
              f"silent_only={r['silent_only']} "
              f"decode={r['decode_stable_seeds']}")

    # ---- 6. the gates -----------------------------------------------
    recheck = {}
    for i, r in enumerate(delivered):
        v = nov_splice(r["f"], S)
        recheck[str(i)] = {"fast": round(r["nov_splice"], 6),
                           "verbatim": round(v, 6)}
        assert abs(v - r["nov_splice"]) < 1e-9, \
            f"delivered nov_splice verbatim recheck failed (d-{i + 1})"
    print("  verbatim recheck of delivered nov_splice: exact")
    c1 = bool(n_del == N_DELIVER
              and all(r["nov_lib"] > n_star
                      and r["nov_splice"] > n_star_splice
                      for r in delivered))
    for r in delivered:
        r["min_pairwise_D"] = round(float(min(
            (dist(r["f"], d["f"]) for d in delivered
             if r is not d), default=float("inf"))), 2)
    c4 = bool(n_del == N_DELIVER and n_del >= 2 and
              all(r["min_pairwise_D"] > n_star for r in delivered))
    eff = [r for r in delivered if not r["silent_only"]]   # primary
    audit_n_eff = sum(int(r["audit_pass"]) for r in eff)
    decode_n_eff = sum(int(r["decode_pass"]) for r in eff)
    audit_n_all = sum(int(r["audit_pass"]) for r in delivered)
    decode_n_all = sum(int(r["decode_pass"]) for r in delivered)
    l3 = bool(len(eff) >= 8 and audit_n_eff >= 8)          # primary
    l4 = bool(len(eff) >= 8 and decode_n_eff >= 8)
    l3_sec = bool(n_del >= 8 and audit_n_all >= 8)         # secondary
    l4_sec = bool(n_del >= 8 and decode_n_all >= 8)
    l2 = bool(any(r["audit_pass"] and not r["silent_only"]
                  for r in delivered))
    partial = 1 <= n_del <= 7
    gates = {"L1_bar_deposit_order": True,
             "L2_minimum_revival": l2,
             "L3_C2_audit": l3, "L4_C3_decode": l4,
             "C1_novelty_generation": c1,
             "C4_zero_anatomy_special": c4}
    npass = sum(int(v) for v in gates.values())
    print(f"\n  GATE-L2 revival: {'PASS' if l2 else 'REFUTED'}")
    print(f"  GATE-L3/C2 audit (primary {audit_n_eff}/{len(eff)}; "
          f"secondary {audit_n_all}/{n_del}): "
          f"{'PASS' if l3 else 'REFUTED'}")
    print(f"  GATE-L4/C3 decode (primary {decode_n_eff}/{len(eff)}; "
          f"secondary {decode_n_all}/{n_del}): "
          f"{'PASS' if l4 else 'REFUTED'}")
    print(f"  C1: {'PASS' if c1 else 'REFUTED'} | "
          f"C4: {'PASS' if c4 else 'REFUTED'} | "
          f"silent-only flagged: "
          f"{sum(int(r['silent_only']) for r in delivered)}")
    print(f"  === {npass}/6 gate clauses PASS ==="
          f"{' (PARTIAL: delivery %d)' % n_del if partial else ''}")

    out = {
        "exp": "exp146_splice_bar (workstream L)",
        "claim": ("re-deriving the anti-recombination bar from the "
                  "splice family's OWN internal spread (the "
                  "corpus-defines-threshold rule applied to the corpus "
                  "the library induces) repairs the L124-localized "
                  "killer and revives the exp136 generator claim"),
        "branch": ("full gates" if n_del >= 8 else
                   f"PARTIAL (delivery {n_del}): C1 verdict per its own "
                   f"wording; binding stage identified"),
        "stage_order": stage_order + ["search", "funnel", "audit",
                                      "gates"],
        "pre_registered_clause": (
            "clear iff NOV_lib > N*_lib AND nov_splice > N*_splice"),
        "n_star_lib": round(n_star, 3),
        "n_star_splice": round(n_star_splice, 3),
        "bar_ratio": round(n_star_splice / n_star, 4),
        "family": {"size": int(len(S)),
                   "distinct_profiles": int(n_cls),
                   "duplicate_classes": dup,
                   "singletons": int(len(sng)),
                   "max_class_size": int(cnt.max()),
                   "members_in_duplicate_classes": int(cnt[cnt >= 2].sum())},
        "nn_percentiles": pcts,
        "verification_harness": harness,
        "delivered_nov_splice_verbatim_recheck": recheck,
        "replication_of_exp141": rep,
        "funnel": {"pool": len(pool), "lib_novel": len(eligible),
                   "splice_clear_new_bar": len(splice_clear),
                   "splice_clear_old_bar":
                       sum(int(r["nov_splice"] > n_star)
                           for r in eligible),
                   "delivered": n_del,
                   "audit_pass_delivered": audit_n_all,
                   "nonsilent_pass_delivered":
                       sum(int(r["nonsilent_pass"]) for r in delivered),
                   "decode_pass_delivered": decode_n_all,
                   "silent_only_flagged":
                       [i for i, r in enumerate(delivered)
                        if r["silent_only"]]},
        "delivered": [
            {"name": f"d-{i + 1:02d}",
             "zones": [list(z) for z in r["zones"]],
             "tags": r["tags"], "J": round(r["J"], 4),
             "nov_lib": round(r["nov_lib"], 2),
             "nov_splice": round(r["nov_splice"], 3),
             "min_pairwise_D": r["min_pairwise_D"],
             "ladder": r["ladder"],
             "audit_pass": r["audit_pass"],
             "nonsilent_pass": r["nonsilent_pass"],
             "silent_only": r["silent_only"],
             "emitted_cell": r["emitted_cell"],
             "decode_errs": r["decode_errs"],
             "hold_errs": r["hold_errs"],
             "decode_stable_seeds": r["decode_stable_seeds"],
             "decode_pass": r["decode_pass"]}
            for i, r in enumerate(delivered)],
        "silent_freebie_check": {
            "rule": "a delivered invention verifying ONLY at mu=0 rungs "
                    "is flagged silent_only and excluded from the C2/C3 "
                    "counts (primary reading: numerator AND "
                    "denominator; secondary: numerator only)",
            "flagged": [i for i, r in enumerate(delivered)
                        if r["silent_only"]],
            "c2_primary": l3, "c3_primary": l4,
            "c2_secondary": l3_sec, "c3_secondary": l4_sec},
        "gates": gates,
        "gate_clauses_passed": npass,
        "partial_deposit": ({"delivery": n_del,
                             "c1_verdict_per_wording": c1,
                             "binding_stage": (
                                 "splice clause" if len(splice_clear) < 8
                                 else "C4 pairwise filter or audit")}
                            if partial else None),
        "wall_s": round(time.time() - t0, 1),
        "notes": ("Instruments are exp136/exp141/exp144's imported "
                  "verbatim; the ONLY changes are (a) the splice bar's "
                  "derivation corpus (the family itself, same 95th-pct "
                  "NN rule and metric, verified exactly against the "
                  "verbatim metric before any selection) and (b) the "
                  "silent-freebie check, which is part of gates L2/L3/"
                  "L4 by pre-registration. The delivered candidates' "
                  "nov_splice values are re-verified with the verbatim "
                  "metric before the gates are evaluated."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
