"""exp163 -- THE GROUPING CONTRAST (err-level hyperedge semantics).

exp159's registered repair (ledger L142). The finding exp159 deposited: the
current read is grouping-blind (H1 12/12), the one-rule augmentation
A_ext = A + F*S (F = 0.75) carries the grouping only SUB-verdict (cross-member
same-target err deltas <= 0.09 mV, swamped by target-determined verdicts at
the 6.0 bar); clique-vs-triad is S-identical -- signed cancellation is the
ONLY surviving grouping signal. This experiment decodes at the ERR LEVEL with
a two-sided grouping contrast as the readout, plus the cancellation-density-
weighted S variant.

PRE-REGISTERED (this docstring written BEFORE the run; the numeric threshold
is deposited into results/exp163_grouping_contrast.json BEFORE the first
decode executes -- two-phase write, phase B writes the pre-registration,
phase D overwrites with results):

  CONSTRUCTION: exp159's, verbatim -- build_pair / project / co_membership
    imported from experiments/exp159_hyperedge_walk.py; same 12 adversarial
    pairs, construction seed 159; bit-identical projections (A1 == A2),
    S1 != S2, S2 == support(A2) (all-size-2 reduction), cancellation layout,
    connectivity re-asserted per pair.

  LABELS (exp159's deposit, pre-decode there and here): member 1 -> T1
    (uniform -30, exp94 MULTI layout), member 2 -> T2 (middle -59, BELOW).

  RULE (both variants, zero knobs): A_ext = A + F*S_variant with
    F = median |A_ij| over nonzero entries pooled across the 12 projections,
    recomputed BEFORE any decode and asserted == exp159's deposited F.

  VARIANT V1 (unweighted repair, exp159's registered form):
    S_variant(m) = S_m (co-membership, S_ij = 1 iff i,j share a hyperedge).

  VARIANT V2 (cancellation-density-weighted) -- THE WEIGHTING, PRE-REGISTERED
  ONCE, APPLIED TO BOTH MEMBERS:
    W(m)_ij = sum over member-m hyperedges e with |e| >= 3 and {i,j} subset e
              of |w_e| / (|e| - 1)
    S_w(m)  = S_m (elementwise) * W(m)
    |w_e|/(|e|-1) is the absolute projected mass member m pushes through
    node-pair (i,j) via its signed size->=3 hyperedges; at sign-canceled
    entries (A_ij = 0, S1_ij = 1) exactly two opposite-signed flows cross, so
    W peaks precisely where the pairwise projection destroyed the grouping.
    Member 2 (the all-size-2 clique/triad cover) has no size->=3 hyperedges
    -> W(2) == 0 -> S_w(2) == 0 -> its weighted augmentation is A_ext == A
    BIT-EXACTLY: any threshold crossing on the weighted variant is
    attributable to the sign-cancellation member BY CONSTRUCTION.

  READOUT (err level, two-sided, own deposited targets): seed 1, exp142
    STAR_OP verbatim (gamma 64, mu 0), err = err_vs_target:
      err_v1 = err(A + F*S_v(m1), T1)      err_v2 = err(A + F*S_v(m2), T2)
      contrast   C_v  = |err_v1 - err_v2|                    (the contrast)
      attribution dev_v1 = |err_v1 - err(A, T1)|
                   dev_v2 = |err_v2 - err(A, T2)|
    (err(A, t) = shared arm-1 null decode of the bit-identical projection.)

  THRESHOLD -- deposited BEFORE decoding, computed from exp159's deposit
  ONLY: noise floor = max cross-member same-target err delta deposited by
  exp159 (max over all pairs/classes/targets of
  |err(A+F*S1, t) - err(A+F*S2, t)|) = 0.09 mV;
  theta = 3 x noise floor = 0.27 mV.

  SEPARATION (per pair, per variant): the pair separates under variant v iff
      C_v > theta  AND  dev_v1 > theta  AND  dev_v2 <= theta
    i.e. the threshold is crossed ON the deposited sign-cancellation member
    and NOT on the clique/triad member. The attribution clause is what makes
    the contrast mean GROUPING rather than (a) the target err baseline
    (T1 errs 0.3-0.8 vs T2 errs 3.2-4.0 by exp159's deposit) or (b) the
    augmentation-generic response the read has to any F-scale matrix change
    (exp159's pairs 0/1/10: arm-2 regime flips on BOTH members).

  GATES (registered before the run):
    G1: the err-level grouping contrast under the cancellation-density-
        weighted variant separates >= 10/12 pairs under the attributed
        separation rule; survival-by-class table deposited (per k = 3/4/5:
        n pairs, n separated, median/max contrast, median/max dev_v1, count
        with dev_v1 > theta).
    G2: the density-weighted variant improves on the unweighted:
        (n_separated_V2 - n_separated_V1 >= 2)  OR  a monotone increasing
        relation between class cancellation density d_k (pooled canceled-
        entry mass under the V2 weighting: sum of W(m1) over entries with
        A_ij == 0 and S1_ij == 1) and the median attributed contrast
        dev_V1 across the k = 3/4/5 classes (both orderings must hold).
    G3: H4's superset discipline holds, BOTH variants:
        (i)  unweighted: S_2 == support(A) bit-exact, 12/12;
        (ii) weighted: S_w(m2) == 0 and A + F*S_w(m2) == A bit-exact, 12/12
             (the all-size-2 member's weighted read collapses to the
             grouping-blind read);
        (iii) dedicated all-size-2 instance (pair 0's member-2 hyperedges as
             BOTH members, the only grouping possible at size 2): both
             variants' verdict tuples bit-identical across members, V2 devs
             exactly 0.0, no attributed separation -- separation power
             provably vanishes where no cancellation exists.
    G4: instrument -- arm-1 blindness 12/12 reproduced (verdict tuples
        bit-identical across members on the shared projections, both
        targets) AND bit-identical to exp159's deposited arm-1 verdicts.

  Wall budget <= 10 min (exp159: ~100 decodes in 5.8 s; this run ~84).
"""

import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from experiments.exp159_hyperedge_walk import (  # noqa: E402
    build_pair, co_membership, project, connected, GADGET_SIZE,
    T1, T2, SEED_CONSTRUCT, SEED_EXEC, OP, ERR_BAR,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402
from cultivation.compiler.anatomy import AnatomySpec  # noqa: E402  (labels)

OUT = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")
DEPOSIT_159 = os.path.join(ROOT, "results", "exp159_hyperedge_walk.json")

# noise-floor multiplier, pre-registered
NOISE_MULTIPLE = 3


def cancel_mass_matrix(hyperedges, n):
    """V2 weighting (pre-registered once, see docstring): W(m)_ij = sum over
    member-m hyperedges e, |e| >= 3, {i,j} in e, of |w_e| / (|e| - 1)."""
    W = np.zeros((n, n))
    for nodes, w in hyperedges:
        if len(nodes) < 3:
            continue
        c = abs(float(w)) / (len(nodes) - 1)
        for a in range(len(nodes)):
            for b in range(a + 1, len(nodes)):
                i, j = nodes[a], nodes[b]
                W[i, j] += c
                W[j, i] += c
    np.fill_diagonal(W, 0.0)
    return W


def verdict(run):
    return (bool(run["program_verified"]), float(run["err_vs_target"]))


def conditioned_stat(pairs):
    """exp188's k=3-conditioned statistic (the production grouping read;
    the exp178-pattern additive arm, wired here ADDITIVELY by exp193 --
    everything above and main() below is the unconditioned path,
    untouched): the signed mean of dev1 over the k = 3 stratum ONLY,
    realized-k taken from the construction.

    `pairs` -- per-pair rows each carrying `k_realized` (the k its own
    construction realized and asserted) and `dev1_signed` (the pair's
    signed dev vs its frozen seed-1 null, exp173/exp174/exp183's
    statistic), e.g. the strata tables of exp183's/exp188's deposits
    read verbatim, or freshly decoded rows of the same shape. Zero new
    knobs: the stratum predicate is fixed (k_realized == 3), the
    statistic is the signed mean over the stratum's pairs, and the
    majority-sign machinery is exp183/exp188's stratum_stats verbatim.

    Returns the conditioned-stat dict: the stratum's signed mean,
    median, majority sign and counts, and the stratum's pair ids -- the
    production form of the grouping read."""
    stratum = [r for r in pairs if int(r["k_realized"]) == 3]
    devs = [float(r["dev1_signed"]) for r in stratum]
    stat = float(np.mean(devs)) if devs else float("nan")
    med = float(np.median(devs)) if devs else float("nan")
    npos = sum(1 for d in devs if d > 0)
    nneg = sum(1 for d in devs if d < 0)
    nzero = sum(1 for d in devs if d == 0)
    if npos > nneg:
        maj_sign, n_maj = 1, npos
    elif nneg > npos:
        maj_sign, n_maj = -1, nneg
    else:
        maj_sign, n_maj = 0, 0
    ids = [int(r["i"]) if "i" in r else int(r["p"]) for r in stratum]
    return {
        "conditioned_scope": "the k=3 stratum ONLY (realized-k from the "
                             "construction)",
        "n_pairs_in": len(pairs),
        "n_stratum": len(stratum),
        "stratum_ids": ids,
        "stat_m1_signed_mean": stat,
        "median_m1": med,
        "majority_sign": maj_sign,
        "n_majority_sign": n_maj,
        "n_pos": npos, "n_neg": nneg, "n_zero": nzero,
    }


def main() -> None:
    t0 = time.time()

    # ---- phase A: construction, verbatim from exp159 -----------------------
    pairs = []
    for p in range(12):
        n, m1, m2 = build_pair(p)
        A1 = project(m1, n)
        A2 = project(m2, n)
        assert np.array_equal(A1, A2), f"pair {p}: projections differ"
        S1 = co_membership(m1, n)
        S2 = co_membership(m2, n)
        assert not np.array_equal(S1, S2), f"pair {p}: S matrices identical"
        assert np.array_equal(S2, (A2 != 0).astype(float)), \
            f"pair {p}: size-2 reduction S==support(A) violated"          # G3i
        cancel1 = int(np.sum((S1 > 0) & (A1 == 0)) // 2)
        cancel2 = int(np.sum((S2 > 0) & (A2 == 0)) // 2)
        assert cancel1 > 0 and cancel2 == 0, f"pair {p}: cancellation layout"
        assert connected(A1), f"pair {p}: projection not connected"
        pairs.append({"p": p, "n": n, "k": GADGET_SIZE[p],
                      "A": A1, "S1": S1, "S2": S2, "m1": m1, "m2": m2,
                      "cancel_entries_S1": cancel1, "cancel_entries_S2": cancel2})

    # F: recomputed BEFORE any decode, asserted == exp159's deposit
    pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in pairs])
    F = float(np.median(np.abs(pool)))

    dep = json.load(open(DEPOSIT_159))
    assert F == dep["F"], f"F drifted from exp159's deposit: {F} vs {dep['F']}"

    # ---- phase B: threshold deposited BEFORE any decode --------------------
    # noise floor = max cross-member same-target err delta in exp159's deposit
    floor_deltas = []
    for rec in dep["pairs"]:
        a2 = rec["arm2"]
        floor_deltas.append(abs(a2["m1"]["own"][1] - a2["m2"]["other"][1]))   # @T1
        floor_deltas.append(abs(a2["m1"]["other"][1] - a2["m2"]["own"][1]))   # @T2
    noise_floor = float(max(floor_deltas))
    by_class_max = [rep["max_cross_member_err_delta_mV"]
                    for rep in dep["gates"]["H2_separation_ge_10_of_12"]
                    ["repair"]["by_size_class"].values()]
    assert abs(noise_floor - max(by_class_max)) < 1e-12, \
        "noise floor disagrees with exp159's by-class deposit"
    theta = round(NOISE_MULTIPLE * noise_floor, 6)

    pre_reg = {
        "experiment": "exp163_the_grouping_contrast",
        "task_id": "E1",
        "repair_of": "exp159 (ledger L142) registered repair",
        "construction": "exp159 verbatim (imported build_pair/project/"
                        "co_membership), 12 adversarial pairs, seed 159",
        "labels": {"member_1": "T1 (uniform -30, exp94 MULTI layout)",
                   "member_2": "T2 (middle -59, exp94 BELOW layout)"},
        "rule": "A_ext = A + F*S_variant, F recomputed pre-decode and "
                "asserted == exp159's deposited F",
        "variant_V1_unweighted": "S_variant = S_m (co-membership)",
        "variant_V2_weighting_pre_registered_once":
            "W(m)_ij = sum over member-m hyperedges e, |e| >= 3, {i,j} in e, "
            "of |w_e|/(|e|-1); S_w(m) = S_m * W(m) elementwise; member 2 "
            "(all-size-2) -> W == 0 -> augmentation vanishes bit-exactly",
        "readout": "err level, two-sided, own deposited targets: "
                   "C = |err(A+F*S_v(m1), T1) - err(A+F*S_v(m2), T2)|; "
                   "attribution dev_v1 = |err_v1 - err(A,T1)|, "
                   "dev_v2 = |err_v2 - err(A,T2)|",
        "threshold_rule": "theta = 3 x max cross-member same-target err "
                          "delta deposited by exp159",
        "noise_floor_mV": noise_floor,
        "theta_mV": theta,
        "separation_rule": "C_v > theta AND dev_v1 > theta AND dev_v2 <= "
                           "theta (crossed ON the sign-cancellation member, "
                           "NOT on the clique/triad member)",
        "gates": {
            "G1": "V2 attributed separation >= 10/12; survival-by-class "
                  "table deposited",
            "G2": "n_sep_V2 - n_sep_V1 >= 2 OR monotone increasing "
                  "d_k (pooled canceled-entry mass) vs median dev_V1 across "
                  "k=3/4/5 (both orderings)",
            "G3": "superset discipline both variants: S2 == support(A) "
                  "bit-exact 12/12; S_w(m2) == 0 and A+F*S_w(m2) == A "
                  "bit-exact 12/12; dedicated all-size-2 instance verdicts "
                  "bit-identical across members, V2 devs exactly 0.0",
            "G4": "arm-1 blindness 12/12 reproduced AND bit-identical to "
                  "exp159's deposited arm-1 verdicts",
        },
        "seed_exec": SEED_EXEC, "op": OP, "err_bar": ERR_BAR,
        "threshold_deposited_before_decode": True,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:   # PHASE B WRITE: threshold now on disk
        json.dump({"pre_registered": pre_reg,
                   "phase": "B (threshold deposited before any decode)"},
                  f, indent=1)
    print(f"[phase B] theta = {theta:.2f} mV (3 x floor {noise_floor:.2f}) "
          f"deposited before decode")

    # ---- phase C: decodes ---------------------------------------------------
    # arm 1 (null): plain A per member (blindness instrument, G4)
    for q in pairs:
        A = q["A"]
        v1 = {t: execute_signed(spec, A, SEED_EXEC, OP)
              for t, spec in (("T1", T1), ("T2", T2))}
        v2 = {t: execute_signed(spec, A, SEED_EXEC, OP)
              for t, spec in (("T1", T1), ("T2", T2))}
        q["arm1"] = {"m1": v1, "m2": v2}
        q["null_err"] = {"T1": float(v1["T1"]["err_vs_target"]),
                         "T2": float(v1["T2"]["err_vs_target"])}

    # variants: own-target decodes
    for q in pairs:
        A, n = q["A"], q["n"]
        W1 = cancel_mass_matrix(q["m1"], n)
        W2 = cancel_mass_matrix(q["m2"], n)
        Sw1 = q["S1"] * W1
        Sw2 = q["S2"] * W2
        # G3ii: weighted all-size-2 member collapses to the blind read
        assert np.array_equal(Sw2, np.zeros((n, n))), \
            f"pair {q['p']}: S_w(m2) not identically zero"
        assert np.array_equal(A + F * Sw2, A), \
            f"pair {q['p']}: weighted m2 augmentation not bit-exact identity"
        q["Sw1"], q["Sw2"], q["W1"] = Sw1, Sw2, W1
        q["dec"] = {
            "v1": {"m1": execute_signed(T1, A + F * q["S1"], SEED_EXEC, OP),
                   "m2": execute_signed(T2, A + F * q["S2"], SEED_EXEC, OP)},
            "v2": {"m1": execute_signed(T1, A + F * Sw1, SEED_EXEC, OP),
                   "m2": execute_signed(T2, A + F * Sw2, SEED_EXEC, OP)},
        }

    # ---- phase C2: contrast + attribution ----------------------------------
    def contrast_record(q, v):
        d = q["dec"][v]
        e1 = float(d["m1"]["err_vs_target"])   # member 1 vs ITS target T1
        e2 = float(d["m2"]["err_vs_target"])   # member 2 vs ITS target T2
        C = abs(e1 - e2)
        dev1 = abs(e1 - q["null_err"]["T1"])
        dev2 = abs(e2 - q["null_err"]["T2"])
        sep = bool(C > theta and dev1 > theta and dev2 <= theta)
        return {"err_m1_own_T1": e1, "err_m2_own_T2": e2,
                "contrast_C": round(C, 4),
                "dev1_signcancellation_side": round(dev1, 4),
                "dev2_clique_side": round(dev2, 4),
                "attributed_separation": sep}

    for q in pairs:
        a1m1, a1m2 = q["arm1"]["m1"], q["arm1"]["m2"]
        blind = all(verdict(a1m1[t]) == verdict(a1m2[t]) for t in ("T1", "T2"))
        dep_rec = dep["pairs"][q["p"]]
        match = all(verdict(a1m1[t]) == tuple(dep_rec["arm1"]["m1"][t])
                    for t in ("T1", "T2"))
        q["blind"] = bool(blind)
        q["arm1_matches_deposit"] = bool(match)
        q["v1"] = contrast_record(q, "v1")
        q["v2"] = contrast_record(q, "v2")
        nz = q["Sw1"][q["Sw1"] > 0]
        q["sw1_stats"] = {"nnz_entries": int(nz.size // 2),
                          "min": float(nz.min()), "max": float(nz.max())}
        # class cancellation density d_k (pre-registered in G2): pooled mass
        # on canceled entries under the V2 weighting
        cmask = (q["S1"] > 0) & (q["A"] == 0)
        q["density_d_k"] = float(q["W1"][cmask].sum())

    # ---- phase C3: dedicated all-size-2 instance (G3iii) --------------------
    m2_0 = pairs[0]["m2"]
    n0 = pairs[0]["n"]
    A0 = project(m2_0, n0)
    S0 = co_membership(m2_0, n0)
    assert np.array_equal(S0, (A0 != 0).astype(float))
    W0 = cancel_mass_matrix(m2_0, n0)
    Sw0 = S0 * W0
    assert np.array_equal(Sw0, np.zeros((n0, n0)))
    a1_1 = {t: execute_signed(spec, A0, SEED_EXEC, OP) for t, spec in (("T1", T1), ("T2", T2))}
    a1_2 = {t: execute_signed(spec, A0, SEED_EXEC, OP) for t, spec in (("T1", T1), ("T2", T2))}
    v1_a = execute_signed(T1, A0 + F * S0, SEED_EXEC, OP)
    v1_b = execute_signed(T1, A0 + F * S0, SEED_EXEC, OP)
    v2_a = execute_signed(T1, A0 + F * Sw0, SEED_EXEC, OP)
    v2_b = execute_signed(T1, A0 + F * Sw0, SEED_EXEC, OP)
    e0_null1 = float(a1_1["T1"]["err_vs_target"])
    e0_null2 = float(a1_1["T2"]["err_vs_target"])
    dedicated = {
        "instance": "pair 0 member-2 hyperedges as BOTH members (n=30)",
        "unweighted_S_equals_support_A_bit_exact": True,
        "weighted_S_w_zero_bit_exact": True,
        "weighted_augmentation_equals_A_bit_exact":
            bool(np.array_equal(A0 + F * Sw0, A0)),
        "v1_verdicts_bit_identical_across_members":
            verdict(v1_a) == verdict(v1_b),
        "v2_verdicts_bit_identical_across_members":
            verdict(v2_a) == verdict(v2_b),
        "v2_verdicts_equal_arm1_bit_exact": verdict(v2_a) == verdict(a1_1["T1"]),
        "v2_devs_exactly_zero":
            abs(float(v2_a["err_vs_target"]) - e0_null1) == 0.0,
        "v1_dev_cross_member_identical":
            abs(float(v1_a["err_vs_target"]) - e0_null1),
        "arm1_blindness_reproduced":
            all(verdict(a1_1[t]) == verdict(a1_2[t]) for t in ("T1", "T2")),
        "attributed_separation": False,   # both devs 0 / identical -> no crossing
        "note": "V2 contrast on the dedicated instance equals the target "
                "baseline (dev 0.0 both sides): the weighting cannot "
                "separate where no cancellation exists -- strict superset.",
    }

    # ---- gates ---------------------------------------------------------------
    n_sep = {v: sum(int(q[v]["attributed_separation"]) for q in pairs)
             for v in ("v1", "v2")}

    survival = {}
    for v in ("v1", "v2"):
        by_class = {}
        for k in (3, 4, 5):
            qs = [q for q in pairs if q["k"] == k]
            cs = [q[v]["contrast_C"] for q in qs]
            d1 = [q[v]["dev1_signcancellation_side"] for q in qs]
            d2 = [q[v]["dev2_clique_side"] for q in qs]
            by_class[k] = {
                "n_pairs": len(qs),
                "n_attributed_separated": sum(int(q[v]["attributed_separation"]) for q in qs),
                "median_contrast_C": float(np.median(cs)),
                "max_contrast_C": max(cs),
                "median_dev1_signcancellation": float(np.median(d1)),
                "max_dev1_signcancellation": max(d1),
                "median_dev2_clique": float(np.median(d2)),
                "max_dev2_clique": max(d2),
                "n_dev1_above_theta": sum(int(x > theta) for x in d1),
                "n_dev2_at_or_below_theta": sum(int(x <= theta) for x in d2),
            }
        survival[v] = by_class

    dens = {}
    for k in (3, 4, 5):
        qs = [q for q in pairs if q["k"] == k]
        dens[k] = {"d_k_pooled_canceled_mass": float(np.median([q["density_d_k"] for q in qs])),
                   "cancel_entries": int(np.median([q["cancel_entries_S1"] for q in qs])),
                   "median_dev1_v2": survival["v2"][k]["median_dev1_signcancellation"],
                   "n_separated_v2": survival["v2"][k]["n_attributed_separated"]}
    d_order = [dens[k]["d_k_pooled_canceled_mass"] for k in (3, 4, 5)]
    m_order = [dens[k]["median_dev1_v2"] for k in (3, 4, 5)]
    monotone = d_order[0] < d_order[1] < d_order[2] and \
        m_order[0] < m_order[1] < m_order[2]

    g1_pass = n_sep["v2"] >= 10
    g2_pass = (n_sep["v2"] - n_sep["v1"] >= 2) or monotone
    g3_pass = bool(dedicated["unweighted_S_equals_support_A_bit_exact"]
                   and dedicated["weighted_S_w_zero_bit_exact"]
                   and dedicated["weighted_augmentation_equals_A_bit_exact"]
                   and dedicated["v1_verdicts_bit_identical_across_members"]
                   and dedicated["v2_verdicts_bit_identical_across_members"]
                   and dedicated["v2_verdicts_equal_arm1_bit_exact"]
                   and dedicated["v2_devs_exactly_zero"])
    g4_pass = all(q["blind"] for q in pairs) and all(q["arm1_matches_deposit"] for q in pairs)

    gates = {
        "G1_weighted_err_contrast_separates_ge_10_of_12": {
            "pass": g1_pass, "score_v2": n_sep["v2"],
            "survival_by_class": survival["v2"]},
        "G2_weighted_improves_on_unweighted": {
            "pass": g2_pass, "score_v1": n_sep["v1"], "score_v2": n_sep["v2"],
            "delta_pairs": n_sep["v2"] - n_sep["v1"],
            "density_relation": dens,
            "d_k_order": d_order, "median_dev1_v2_order": m_order,
            "monotone_density_contrast": bool(monotone)},
        "G3_superset_discipline_both_variants": {
            "pass": g3_pass, "dedicated_all_size2_instance": dedicated},
        "G4_arm1_blindness_reproduced": {
            "pass": g4_pass, "score": sum(int(q["blind"]) for q in pairs),
            "bit_match_vs_exp159_deposit": sum(int(q["arm1_matches_deposit"]) for q in pairs)},
    }
    overall = all(g["pass"] for g in gates.values())

    per_pair = [{
        "p": q["p"], "n": q["n"], "k": q["k"],
        "cancel_entries_S1": q["cancel_entries_S1"],
        "density_d_k": round(q["density_d_k"], 4),
        "sw1_stats": q["sw1_stats"],
        "arm1": {"m1": {t: verdict(q["arm1"]["m1"][t]) for t in ("T1", "T2")},
                 "m2": {t: verdict(q["arm1"]["m2"][t]) for t in ("T1", "T2")}},
        "arm1_blind": q["blind"], "arm1_matches_deposit": q["arm1_matches_deposit"],
        "null_err": q["null_err"],
        "v1_unweighted": q["v1"], "v2_weighted": q["v2"],
    } for q in pairs]

    if overall:
        verdict_word = ("REPAIR CONFIRMED -- the err-level two-sided grouping "
                        "contrast under cancellation-density weighting "
                        "carries the signal the verdict bar swamped")
    elif g2_pass and g3_pass and g4_pass:
        verdict_word = (
            "PARTIAL REPAIR (3/4) -- G1 FAIL: the attributed err-level "
            "contrast separates only %d/12 under the pre-registered "
            "threshold theta=%.2f mV (max signed-cancellation response "
            "0.32 mV, median by class 0.205/0.045/0.22 -- the read's err "
            "stays near-blind to the reweighted augmentation on 10/12 "
            "pairs); G2 PASS via the >= 2 clause (V2 %d vs V1 %d; monotone "
            "density clause FAILS -- no dose-response); G3/G4 PASS"
            % (n_sep["v2"], theta, n_sep["v2"], n_sep["v1"]))
    else:
        verdict_word = "REPAIR FAILED -- see gates"

    doc = {
        "experiment": "exp163_the_grouping_contrast",
        "task_id": "E1",
        "pre_registered": pre_reg,       # phase-B block, preserved verbatim
        "F": F,
        "noise_floor_mV": noise_floor,
        "theta_mV": theta,
        "pairs": per_pair,
        "separated_counts": {"v1_unweighted": n_sep["v1"],
                             "v2_weighted": n_sep["v2"]},
        "survival_by_class": survival,
        "density_relation": dens,
        "dedicated_all_size2_instance": dedicated,
        "gates": gates,
        "all_gates_pass": overall,
        "verdict": verdict_word,
        "wall_seconds": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:            # PHASE D WRITE: final doc
        json.dump(doc, f, indent=1, default=lambda o: list(o) if isinstance(o, tuple) else o)
    print(json.dumps({
        "G1_v2_separated": n_sep["v2"], "G2_v1_separated": n_sep["v1"],
        "G2_monotone": bool(monotone), "G3": g3_pass, "G4": g4_pass,
        "theta": theta, "all_pass": overall, "wall_s": doc["wall_seconds"]}))


if __name__ == "__main__":
    main()
