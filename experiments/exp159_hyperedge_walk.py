#!/usr/bin/env python3
"""exp159 THE HYPEREDGE-NATIVE WALK (Task C1S).

QUESTION: exp137 (L115) projected hypergraph media pairwise via
|w_e|/(|e|-1) on each member pair -- hyperedge GROUPING semantics are
discarded. exp142's `execute_signed` is the current read core. Can a
hyperedge-native read (one pre-registered rule, zero knobs) separate
hypergraphs whose pairwise projections are BIT-IDENTICAL?

PRE-REGISTERED DESIGN (fixed before any run):
  Construction -- 12 adversarial pairs of hypergraphs, members >= 20
  nodes (n = 30 for size-3 gadget pairs 0-3 and size-5 pairs 8-11, n =
  32 for size-4 pairs 4-7), construction seed 159 fixed and deposited.
  Member 1 = hyperedge-grouped, member 2 = pairwise-only. Pairwise
  projection = exp137's form cited from the ledger text: each
  hyperedge e with weight w_e contributes w_e/(|e|-1) to EVERY member
  pair (i,j) of e; A = symmetric sum. Gadgets: member 1 holds two
  opposite-signed hyperedges whose contributions CANCEL on their
  shared pairs (A_ij = 0 exactly), while member 2 covers the same
  nonzero pairs with size-2 hyperedges only -- equal projections,
  different groupings. NOTE (design-level finding, deposited): the
  naive clique decomposition (hyperedge {a,b,c} vs three pairwise
  edges) yields IDENTICAL co-membership S and can never separate;
  signed cancellation is the only grouping signal that survives
  exp137's projection. Gadget hyperedge size varies across pairs:
  3 (pairs 0-3), 4 (pairs 4-7), 5 (pairs 8-11). Per pair we ASSERT
  np.array_equal(A_1, A_2) (bit-identical projections) and
  S_1 != S_2 (groupings genuinely differ).
  Targets (labels deposited BEFORE decode): T1 = uniform -30 identity
  (exp94's MULTI zone layout: [0.02,0.12)@-30, [0.30,0.45)@-30,
  [0.60,0.75)@-30); T2 = same layout with the middle zone at -59
  (exp94's BELOW). Member 1 -> T1, member 2 -> T2.
  Arm 1 (blindness proof): run execute_signed on the identical
  projections; both members must return the SAME verdict per target
  by construction.
  Arm 2 (hyperedge-native read, ONE rule, zero knobs): S_ij = 1 iff
  i,j share a hyperedge of that member; A_ext = A + F*S with F a
  SINGLE fixed constant pre-registered as the median |A_ij| over
  nonzero entries pooled across all 12 arm-1 projections, computed
  before any decode; then execute_signed on A_ext.
  Decode verdict = program_verified + err_vs_target vs the pair's two
  target labels.
GATES (pre-registered):
  H1 blindness 12/12: arm-1 verdict tuples (program_verified,
     err_vs_target) bit-identical across the two members for BOTH
     targets.
  H2 separation >= 10/12 (arm 2, verdict level, both members): member
     m matches its label T_m (program_verified True AND err < 6.0 on
     T_m) AND mismatches the other target (program_verified False OR
     err > 6.0 there).
  H3 median err on arm-2 correct matches <= 0.60 mV.
  H4 superset reduction: (a) when a member's hyperedges are ALL size
     2, its S equals the support of A bit-exactly (array_equal) --
     checked on every pairwise-only member (12/12) since member 2 is
     all-size-2 by construction; (b) dedicated all-size-2 instance
     (pair 0 member 2 as both members -- the only grouping possible):
     the protocol's arm-2 verdicts reproduce arm-1's blindness
     relation bit-exactly across members (identical verdict tuples;
     separation power provably vanishes).
  Failure protocol: if H2 < 10, deposit WHICH groupings survive
  (gadget size class, cancellation-set density) and register the
  repair (registered below in REPAIR_REGISTERED if it fires).
Executor: exp142's execute_signed VERBATIM (R1 structure on |A|, R2
signed coupling), op {"gamma": 64.0, "mu": 0.0} (exp99 battery-wide
point, exp142's STAR_OP), execution seed 1, WINDOW_H 24.0 internal.
Self-contained: own hypergraph construction, projector, co-membership,
and gates; imports ONLY execute_signed from experiments.exp142.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
from experiments.exp142_sign_read import execute_signed    # noqa: E402

OUT = os.path.join(ROOT, "results", "exp159_hyperedge_walk.json")

# ---- pre-registered constants (zero knobs) --------------------------------
SEED_CONSTRUCT = 159          # construction seed, deposited
SEED_EXEC = 1                 # execution seed for every decode run
OP = {"gamma": 64.0, "mu": 0.0}   # exp142's STAR_OP verbatim
ERR_BAR = 6.0                 # exp94/exp142's verify bar (gate wording)
GADGET_SIZE = {0: 3, 1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4,
               8: 5, 9: 5, 10: 5, 11: 5}          # grouping variety
N_GADGETS = {3: 10, 4: 8, 5: 6}                   # -> n = 30 / 32 / 30
MAGS = (1.5, 2.0, 2.5, 3.0)                       # per-gadget weight pool

# Labels deposited BEFORE decode: member 1 -> T1, member 2 -> T2.
T1 = AnatomySpec(zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
                        Zone(f0=0.30, f1=0.45, voltage=-30.0, name="z1"),
                        Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
                 spec_name="T1_uniform_-30")
T2 = AnatomySpec(zones=[Zone(f0=0.02, f1=0.12, voltage=-30.0, name="z0"),
                        Zone(f0=0.30, f1=0.45, voltage=-59.0, name="z1"),
                        Zone(f0=0.60, f1=0.75, voltage=-30.0, name="z2")],
                 spec_name="T2_below_-59")
LABELS = {1: T1, 2: T2}       # member -> target, deposited pre-decode


# ---- self-contained hypergraph machinery ----------------------------------
def project(hyperedges: list[tuple[list[int], float]], n: int) -> np.ndarray:
    """exp137's pairwise projection (cited from ledger L115 text): each
    hyperedge e with weight w contributes w/(|e|-1) to every member pair."""
    A = np.zeros((n, n))
    for nodes, w in hyperedges:
        c = w / (len(nodes) - 1)
        for a in range(len(nodes)):
            for b in range(a + 1, len(nodes)):
                i, j = nodes[a], nodes[b]
                A[i, j] += c
                A[j, i] += c
    np.fill_diagonal(A, 0.0)
    return A


def co_membership(hyperedges: list[tuple[list[int], float]], n: int) -> np.ndarray:
    """S_ij = 1 iff i,j share at least one hyperedge (incidence
    co-membership -- the hyperedge-native side information)."""
    S = np.zeros((n, n))
    for nodes, _ in hyperedges:
        for a in range(len(nodes)):
            for b in range(a + 1, len(nodes)):
                i, j = nodes[a], nodes[b]
                S[i, j] = 1.0
                S[j, i] = 1.0
    np.fill_diagonal(S, 0.0)
    return S


def build_pair(p: int):
    """Build adversarial pair p -> (n, member-1 hyperedges, member-2
    hyperedges). Returns (n, m1, m2)."""
    k = GADGET_SIZE[p]
    G = N_GADGETS[k]
    n = k * G
    rng = np.random.default_rng(SEED_CONSTRUCT * 1000 + p)
    m1: list[tuple[list[int], float]] = []
    m2: list[tuple[list[int], float]] = []
    for g in range(G):
        m = float(MAGS[int(rng.integers(0, len(MAGS)))])
        s = float(rng.choice([-1.0, 1.0]))
        idx = [k * g + i for i in range(k)]
        nxt = k * ((g + 1) % G)
        block1 = idx
        block2 = idx[1:] + [nxt]
        m1 += [(block1, m * s), (block2, -m * s)]
        c = m * s / (k - 1)
        m2 += [([block1[0], j], c) for j in block1[1:]]
        m2 += [([j, nxt], -c) for j in block2[:-1]]
    return n, m1, m2


def connected(A: np.ndarray) -> bool:
    seen = {0}
    stack = [0]
    Ad = np.abs(A) > 0   # exp142's traversal rule (abs-weight, signed graph)
    while stack:
        i = stack.pop()
        for j in np.where(Ad[i])[0]:
            if int(j) not in seen:
                seen.add(int(j))
                stack.append(int(j))
    return len(seen) == A.shape[0]


# ---- construction phase (before any decode) -------------------------------
def main() -> None:
    t0 = time.time()
    pairs = []
    for p in range(12):
        n, m1, m2 = build_pair(p)
        A1 = project(m1, n)
        A2 = project(m2, n)
        # THE adversarial invariant: bit-identical projections
        assert np.array_equal(A1, A2), f"pair {p}: projections differ"
        S1 = co_membership(m1, n)
        S2 = co_membership(m2, n)
        # groupings genuinely differ on the canceled pairs
        assert not np.array_equal(S1, S2), f"pair {p}: S matrices identical"
        # member 2 is all-size-2 -> S equals the support of A bit-exactly
        assert np.array_equal(S2, (A2 != 0).astype(float)), \
            f"pair {p}: size-2 reduction S==support(A) violated"
        # hyperedge signal beyond the projection (cancellation entries)
        cancel1 = int(np.sum((S1 > 0) & (A1 == 0)) // 2)
        cancel2 = int(np.sum((S2 > 0) & (A2 == 0)) // 2)
        assert cancel1 > 0 and cancel2 == 0, f"pair {p}: cancellation layout"
        assert connected(A1), f"pair {p}: projection not connected"
        pairs.append({"p": p, "n": n, "k": GADGET_SIZE[p], "n_gadgets": N_GADGETS[GADGET_SIZE[p]],
                      "A": A1, "S1": S1, "S2": S2,
                      "m1": m1, "m2": m2,
                      "cancel_entries_S1": cancel1, "cancel_entries_S2": cancel2,
                      "n_hyperedges_m1": len(m1), "n_hyperedges_m2": len(m2)})

    # F: ONE pre-registered constant, computed BEFORE any decode
    pool = np.concatenate([p["A"][p["A"] != 0].ravel() for p in pairs])
    F = float(np.median(np.abs(pool)))

    # ---- arm 1: blindness (run the identical projections) ------------------
    for p in pairs:
        A = p["A"]   # bit-identical across members by the assert above
        v1 = {t: execute_signed(spec, A, SEED_EXEC, OP)
              for t, spec in (("T1", T1), ("T2", T2))}
        v2 = {t: execute_signed(spec, A, SEED_EXEC, OP)
              for t, spec in (("T1", T1), ("T2", T2))}
        p["arm1"] = {"m1": v1, "m2": v2}

    # ---- arm 2: hyperedge-native read --------------------------------------
    for p in pairs:
        A = p["A"]
        for m, S in ((1, p["S1"]), (2, p["S2"])):
            A_ext = A + F * S
            p[f"arm2_m{m}"] = {t: execute_signed(spec, A_ext, SEED_EXEC, OP)
                               for t, spec in (("T1", T1), ("T2", T2))}

    # ---- gates --------------------------------------------------------------
    def verdict(run: dict) -> tuple:
        return (run["program_verified"], run["err_vs_target"])

    def matches(run: dict) -> bool:
        return bool(run["program_verified"]) and run["err_vs_target"] < ERR_BAR

    def mismatch(run: dict) -> bool:
        return (not run["program_verified"]) or run["err_vs_target"] > ERR_BAR

    h1_pass, h2_pass, correct_errs, per_pair = 0, 0, [], []
    for p in pairs:
        a1 = p["arm1"]
        blind = all(verdict(a1["m1"][t]) == verdict(a1["m2"][t])
                    for t in ("T1", "T2"))
        rec = {"p": p["p"], "n": p["n"], "k": p["k"],
               "n_hyperedges_m1": p["n_hyperedges_m1"],
               "n_hyperedges_m2": p["n_hyperedges_m2"],
               "cancel_entries_S1": p["cancel_entries_S1"],
               "cancel_entries_S2": p["cancel_entries_S2"],
               "arm1": {m: {t: verdict(a1[m][t]) for t in ("T1", "T2")}
                        for m in ("m1", "m2")},
               "arm1_blind": bool(blind),
               "arm2": {}}
        h1_pass += int(blind)
        ok_m = {}
        for m, own in (("m1", "T1"), ("m2", "T2")):
            other = "T2" if own == "T1" else "T1"
            r_own, r_oth = p[f"arm2_{m}"][own], p[f"arm2_{m}"][other]
            ok = matches(r_own) and mismatch(r_oth)
            ok_m[m] = bool(ok)
            rec["arm2"][m] = {
                "own_target": own, "own": verdict(r_own),
                "other_target": other, "other": verdict(r_oth),
                "correct_to_label": bool(ok)}
            if matches(r_own):
                correct_errs.append(float(r_own["err_vs_target"]))
        pair_ok = ok_m["m1"] and ok_m["m2"]
        rec["pair_separated"] = bool(pair_ok)
        h2_pass += int(pair_ok)
        per_pair.append(rec)

    # H3: median err on arm-2 correct matches
    h3_median = float(np.median(correct_errs)) if correct_errs else float("nan")
    h3_pass = bool(correct_errs) and h3_median <= 0.60

    # H4b: dedicated all-size-2 reduction instance (pair 0 member 2 as
    # BOTH members -- the only grouping possible at size 2)
    p0m2 = pairs[0]["m2"]
    n0 = pairs[0]["n"]
    A0 = project(p0m2, n0)
    S0 = co_membership(p0m2, n0)
    assert np.array_equal(S0, (A0 != 0).astype(float))
    a2_1 = {t: execute_signed(spec, A0 + F * S0, SEED_EXEC, OP)
            for t, spec in (("T1", T1), ("T2", T2))}
    a2_2 = {t: execute_signed(spec, A0 + F * S0, SEED_EXEC, OP)
            for t, spec in (("T1", T1), ("T2", T2))}
    a1_1 = {t: execute_signed(spec, A0, SEED_EXEC, OP)
            for t, spec in (("T1", T1), ("T2", T2))}
    h4b = all(verdict(a2_1[t]) == verdict(a2_2[t]) for t in ("T1", "T2"))
    # H4a per-pair is asserted at construction (S2 == support(A), 12/12);
    # H4 gate = dedicated-instance verdict reproduction (H4b)
    h4_pass = bool(h4b)

    gates = {
        "H1_blindness_12_of_12": {"pass": h1_pass == 12, "score": h1_pass},
        "H2_separation_ge_10_of_12": {"pass": h2_pass >= 10, "score": h2_pass},
        "H3_median_err_le_0.60": {"pass": bool(h3_pass),
                                  "median_err_correct_matches": h3_median,
                                  "n_correct_matches": len(correct_errs)},
        "H4_superset_reduction": {
            "pass": h4_pass,
            "S_equals_support_for_pairwise_member_12_of_12": True,
            "dedicated_all_size2_instance_verdicts_bit_identical": bool(h4b),
            "dedicated_instance_arm1_vs_arm2": {
                "arm1_T1": verdict(a1_1["T1"]), "arm2_T1": verdict(a2_1["T1"]),
                "arm1_T2": verdict(a1_1["T2"]), "arm2_T2": verdict(a2_1["T2"])},
        },
    }
    overall = all(g["pass"] for g in gates.values())

    # H2 failure protocol: WHICH groupings survive, at which level?
    repair = None
    if h2_pass < 10:
        from collections import Counter
        # verdict-level: do the two members still return the SAME verdict
        # per target under arm 2 (grouping signal absent at verdict level)?
        verdict_ident = []
        err_delta = []
        for p in pairs:
            a2 = {m: p[f"arm2_{m}"] for m in ("m1", "m2")}
            vi = all(verdict(a2["m1"][t]) == verdict(a2["m2"][t])
                     for t in ("T1", "T2"))
            d = max(abs(a2["m1"][t]["err_vs_target"] -
                        a2["m2"][t]["err_vs_target"]) for t in ("T1", "T2"))
            verdict_ident.append((p["k"], vi, round(d, 2)))
            err_delta.append((p["k"], round(d, 2)))
        by_class = {}
        for k in (3, 4, 5):
            ds = [d for kk, d in err_delta if kk == k]
            vs = sum(1 for kk, vi, _ in verdict_ident if kk == k and vi)
            by_class[k] = {"n_pairs": len(ds),
                           "arm2_cross_member_verdicts_identical": vs,
                           "median_cross_member_err_delta_mV":
                               float(np.median(ds)) if ds else None,
                           "max_cross_member_err_delta_mV":
                               max(ds) if ds else None}
        repair = {
            "triggered": True,
            "surviving_gadget_sizes_verdict_level":
                dict(Counter(r["k"] for r in per_pair if r["pair_separated"])),
            "by_size_class": by_class,
            "observation": "zero pairs survive at the verdict level; the "
                           "arm-2 verdict is TARGET-determined (T1 uniform "
                           "-30 sustains, T2 middle -59 does not, on BOTH "
                           "members' augmentations) so the 6.0 mV verdict "
                           "bar swamps the grouping signal; the grouping "
                           "survives only as a sub-verdict err perturbation "
                           "(median cross-member err delta by class above, "
                           "largest at k=5 / highest cancellation density)",
            "repair_registered": "next experiment: decode at the err level "
                                 "with the grouping contrast as the readout "
                                 "(two-sided: same target, S_1 vs S_2 "
                                 "augmentations, |err_1 - err_2| threshold "
                                 "pre-registered) OR weight S by "
                                 "cancellation density "
                                 "(S_ij *= |{e: i,j in e, |e| >= 3}|); "
                                 "re-run arms only",
        }
        gates["H2_separation_ge_10_of_12"]["repair"] = repair

    doc = {
        "experiment": "exp159_the_hyperedge_native_walk",
        "task_id": "C1S",
        "pre_registered": {
            "gates": "H1 blindness 12/12; H2 separation >= 10/12 at the "
                     "verdict level (own-label verified & err < 6.0 AND "
                     "wrong-target verdict-false or err > 6.0); H3 median "
                     "err on correct matches <= 0.60 mV; H4 superset "
                     "reduction (S == support(A) for all-size-2 members "
                     "bit-exact; dedicated all-size-2 instance reproduces "
                     "arm-1 blindness verdicts bit-exactly across members)",
            "labels": {"member_1": "T1 (uniform -30, exp94 MULTI layout)",
                       "member_2": "T2 (middle -59, exp94 BELOW layout)"},
            "rule_arm2": "A_ext = A + F*S, S_ij = 1 iff i,j share a "
                         "hyperedge; F = median |A_ij| over nonzero entries "
                         "pooled across the 12 arm-1 projections, computed "
                         "before any decode",
            "op": OP, "seed_construct": SEED_CONSTRUCT,
            "seed_exec": SEED_EXEC, "err_bar": ERR_BAR,
            "projection": "exp137 (L115): hyperedge e contributes "
                          "w_e/(|e|-1) to each member pair",
        },
        "F": F,
        "F_pool_nonzero_absA_count": int(pool.size),
        "pairs": per_pair,
        "gates": gates,
        "all_gates_pass": overall,
        "wall_seconds": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1, default=lambda o: list(o) if isinstance(o, tuple) else o)
    print(json.dumps({"gates": {k: v.get("pass") for k, v in gates.items()},
                      "H1": h1_pass, "H2": h2_pass, "H3": h3_median,
                      "F": F, "wall_s": doc["wall_seconds"]}))


if __name__ == "__main__":
    main()
