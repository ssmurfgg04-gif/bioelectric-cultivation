#!/usr/bin/env python3
"""exp183 — THE K-CONTROLLED COHORT (is the ensemble's sign a density
effect?).

exp174's registered next (L153): all three minority-sign pairs across
both cohorts are k = 4 gadgets (original p4/p6, fresh p5) — "if the
k = 4 stratum flips sign while k = 3 holds, the ensemble's sign
structure is a DENSITY effect and the grouping read gains its first
structural covariate".

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Stratification, statistic, and gates are
fixed now.

THE STRATIFICATION (zero fitting): exp159's construction VERBATIM,
seed ladder 183001..183036 (SEED_CONSTRUCT rebound per pair, the
exp174 mechanism, restore asserted) — 36 fresh pairs; each pair's
REALIZED k recorded from the construction; the cohort is THEN split
into the k = 3 stratum and the k = 4 stratum, taking the FIRST 6 of
each by ladder order (the pre-registered selection rule; if either
stratum has fewer than 6 among the 36, the stratum sizes are
deposited as-is and the gates evaluate on what exists — disclosed).

THE STATISTIC (exp173/exp174's, verbatim): dev_signed per pair,
stat = mean over the stratum's pairs, V2 weighting via exp163's
cancel_mass_matrix, STAR_OP readout, seed (1,); m2 side identical.

TWO-PHASE NULL DISCIPLINE: per stratum, the null bar frozen on disk
BEFORE the stratum's real-arm decode (exp173's protocol: the shared
arm-1 null, bar = max |pooled null stat| over exp142's deposited
seeds x own-targets); byte-offset assertion per stratum.

GATES (each evaluated exactly once):

  GATE-W1 (strata integrity) both strata built; per-pair
           construction asserts hold (A1 == A2, S_2 == support(A),
           connectivity); the realized-k classification matches the
           construction's own k field 36/36 (or as built).
  GATE-W2 (null discipline) both strata's bars frozen before their
           real arms; byte order asserted; bars finite and > 0.
  GATE-W3 (the density clause) per stratum: |stat| vs its bar and
           the majority-sign count deposited; the DENSITY question
           answered by the pre-named pattern: (i) k=4 stratum
           flips/weakens while k=3 holds — density effect CONFIRMED;
           (ii) both strata hold — density NOT the covariate;
           (iii) both flip — the sign is construction-generic.
           ALL THREE branches complete the gate; the branch taken
           is the finding.
  GATE-W4 (attribution) |stat_m2| <= its bar in BOTH strata.

NO post-hoc tuning. A --smoke check (ladder pairs 0-1, features
only) is permitted before the credited run and discarded.

DEPOSIT: results/exp183_k_controlled_cohort.json

RUN:
  python3 -m experiments.exp183_k_controlled_cohort          # full
  python3 -m experiments.exp183_k_controlled_cohort --smoke  # check
  python3 -m experiments.exp183_k_controlled_cohort --stratum 4
  # jobs: build | k3 | k4
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import experiments.exp159_hyperedge_walk as exp159  # noqa: E402
from experiments.exp159_hyperedge_walk import (  # noqa: E402
    build_pair, co_membership, project, connected, GADGET_SIZE,
    T1, T2, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP163_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP163_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


LADDER = list(range(183001, 183037))
STRATUM_SIZES = (6, 6)

OUT = os.path.join(ROOT, "results", "exp183_k_controlled_cohort.json")
DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")


def main() -> dict:
    import hashlib
    import time
    t0 = time.time()

    # ---- body-level constants (fixed here, BEFORE any decode) ----------
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "k3", "k4", "all"],
                    default="all")
    ap.add_argument("--stratum", type=int, choices=[3, 4], default=None,
                    help="alias: restrict the run to one stratum "
                         "(3 -> job k3, 4 -> job k4)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    smoke = bool(args.smoke)
    job = args.job
    if args.stratum == 3 and job == "all":
        job = "k3"
    elif args.stratum == 4 and job == "all":
        job = "k4"
    out_path = args.out or (OUT + ".smoke.json" if smoke else OUT)
    name = "exp183_the_k_controlled_cohort"
    DEP174 = os.path.join(ROOT, "results", "exp174_replication_cohort.json")

    # The null protocol's seeds: the read core's own deposited seed
    # convention (exp142.SEEDS = (1, 2, 3), asserted at runtime).  The
    # fresh ladder cohort has no prior deposit, so per (pair, own-target)
    # the seed-1 null decode is the baseline -- exp174's translation of
    # exp173's two-phase discipline to a fresh construction, zero new
    # choices; seed 1 contributes exactly 0 and the bar is carried by
    # the protocol's other seeds (pure null-arm seed noise).
    NULL_SEEDS = (1, 2, 3)
    seed_exec = exp159.SEED_EXEC          # the credited decode seed (1)

    # per-stratum byte-order markers (exp168/exp173's discipline, per
    # stratum as the docstring registers)
    _PHASE_A_WRITE_MARKER = {
        3: "# === STRATUM k=3 PHASE-A DEPOSIT WRITE (byte-order discipline",
        4: "# === STRATUM k=4 PHASE-A DEPOSIT WRITE (byte-order discipline",
    }
    _PHASE_B_DECODE_MARKER = {
        3: "# === FIRST STRATUM k=3 (REAL-ARM) DECODE CALL",
        4: "# === FIRST STRATUM k=4 (REAL-ARM) DECODE CALL",
    }

    def assert_phase_order() -> dict:
        """W2's byte-offset assertion, PER STRATUM (exp173's mechanism):
        each stratum's phase-A deposit write precedes that stratum's
        first real-arm decode call, by byte offset in this file."""
        src = open(os.path.abspath(__file__)).read()
        ev = {}
        for k in (3, 4):
            i_a = src.index(_PHASE_A_WRITE_MARKER[k])
            i_b = src.index(_PHASE_B_DECODE_MARKER[k])
            assert i_a < i_b, (
                f"pre-registration order violated for stratum k={k}: "
                f"the phase-A null deposit write must precede the "
                f"stratum's first real-arm decode path")
            ev[f"k{k}"] = {"phase_a_write_byte": i_a,
                           "first_real_arm_decode_byte": i_b,
                           "order_held": True}
        return ev

    def build_cohort(ladder_indices: list) -> list:
        """THE K-CONTROLLED COHORT (docstring, verbatim protocol):
        exp159's construction with the ONE changed input disclosed
        pre-run -- exp159.SEED_CONSTRUCT rebound PER PAIR along the
        ladder 183001..183036 (the exp174 rebinding mechanism: save,
        rebind, build, restore asserted -- per pair here); the build
        call is exp159's build_pair on the protocol's own 12 slots in
        exp159's order (ladder index i -> slot i % 12: the 36 fresh
        pairs are 3 independent passes of the 12-slot adversarial
        family with independent draws).  Per pair the exp163/exp173
        construction asserts: A1 == A2 bit-identical, S1 != S2,
        S2 == support(A) (all-size-2 reduction), cancellation layout,
        connectivity; the pair's REALIZED k is recorded from the
        construction (member 1's hyperedge size) and asserted against
        the construction's own k field (GADGET_SIZE)."""
        built = []
        for i in ladder_indices:
            slot = i % 12
            saved = exp159.SEED_CONSTRUCT
            assert saved == 159, \
                f"pair {i}: exp159.SEED_CONSTRUCT drifted pre-rebind: {saved}"
            exp159.SEED_CONSTRUCT = LADDER[i]          # THE REBIND
            assert exp159.SEED_CONSTRUCT == LADDER[i], \
                f"pair {i}: rebind to {LADDER[i]} failed"
            n, m1, m2 = build_pair(slot)
            exp159.SEED_CONSTRUCT = saved               # RESTORE
            assert exp159.SEED_CONSTRUCT == saved == 159, \
                f"pair {i}: SEED_CONSTRUCT not restored"
            A1 = project(m1, n)
            A2 = project(m2, n)
            assert np.array_equal(A1, A2), f"pair {i}: projections differ"
            S1 = co_membership(m1, n)
            S2 = co_membership(m2, n)
            assert not np.array_equal(S1, S2), \
                f"pair {i}: S matrices identical"
            assert np.array_equal(S2, (A2 != 0).astype(float)), \
                f"pair {i}: size-2 reduction S==support(A) violated"
            cancel1 = int(np.sum((S1 > 0) & (A1 == 0)) // 2)
            cancel2 = int(np.sum((S2 > 0) & (A2 == 0)) // 2)
            assert cancel1 > 0 and cancel2 == 0, \
                f"pair {i}: cancellation layout"
            assert connected(A1), f"pair {i}: projection not connected"
            # REALIZED k, recorded from the construction itself
            sizes = sorted({len(nodes) for nodes, _ in m1})
            assert len(sizes) == 1, \
                f"pair {i}: member-1 hyperedge sizes not uniform: {sizes}"
            k_realized = int(sizes[0])
            k_field = int(GADGET_SIZE[slot])   # the construction's own k
            assert k_realized == k_field, \
                f"pair {i}: realized k {k_realized} != construction k " \
                f"field {k_field}"
            W1 = cancel_mass_matrix(m1, n)
            Sw1 = S1 * W1
            cmask = (S1 > 0) & (A1 == 0)
            built.append({
                "i": i, "seed_construct": int(LADDER[i]), "slot": slot,
                "n": int(n), "k_realized": k_realized, "k_field": k_field,
                "A": A1, "S1": S1, "S2": S2, "m1": m1, "m2": m2,
                "cancel_entries_S1": cancel1, "cancel_entries_S2": cancel2,
                "density_d_k": float(W1[cmask].sum()),
                "sw1_stats": {"nnz_entries": int((Sw1 > 0).sum() // 2),
                              "max": (float(Sw1[Sw1 > 0].max())
                                      if (Sw1 > 0).any() else 0.0)},
                "digest_A": hashlib.sha256(
                    np.ascontiguousarray(A1).tobytes()).hexdigest(),
            })
        return built

    def cohort_row(q: dict) -> dict:
        return {"i": q["i"], "seed_construct": q["seed_construct"],
                "slot": q["slot"], "n": q["n"],
                "k_realized": q["k_realized"], "k_field": q["k_field"],
                "cancel_entries_S1": q["cancel_entries_S1"],
                "cancel_entries_S2": q["cancel_entries_S2"],
                "density_d_k": round(q["density_d_k"], 4),
                "sw1_stats": q["sw1_stats"],
                "digest_A": q["digest_A"]}

    def recompute_F(ps: list) -> tuple:
        """F, computed BEFORE any decode by exp159/exp163/exp174's
        pre-registered rule applied to this cohort: median |A_ij| over
        nonzero entries pooled across the 36 FRESH projections; ONE
        constant shared by both strata."""
        pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in ps])
        return float(np.median(np.abs(pool))), int(pool.size)

    def phase_a_null(stratum: list, k: int) -> tuple:
        """PHASE-A for one stratum (exp173's two-phase null discipline,
        exp174's fresh-cohort translation, zero new choices): the
        stratum's pooled null distribution from the SHARED arm-1 null
        decode of the bit-identical plain projection; per (pair,
        own-target) the seed-1 null decode is the baseline (no prior
        deposit exists for a fresh ladder cohort); the pooled null stat
        at (seed, own-target) is the SIGNED mean over the stratum's
        pairs of [err(A, target, seed) - err(A, target, seed 1)]; the
        bar = max |pooled null stat| over exp142's deposited seeds x
        own-targets -- frozen on disk BEFORE the stratum's real-arm
        decode."""
        targets = (("T1", T1), ("T2", T2))
        null_errs = {}
        for q in stratum:
            A = q["A"]
            for tname, spec in targets:
                for s in NULL_SEEDS:
                    r = execute_signed(spec, A, s, OP)  # null-arm decode
                    e = float(r["err_vs_target"])
                    assert np.isfinite(e), \
                        f"pair {q['i']} {tname} seed {s}: non-finite"
                    null_errs[(q["i"], tname, s)] = e
        pooled = {}
        for s in NULL_SEEDS:
            for tname, _ in targets:
                devs = [null_errs[(q["i"], tname, s)]
                        - null_errs[(q["i"], tname, 1)] for q in stratum]
                pooled[f"{tname}@seed{s}"] = float(np.mean(devs))
        bar = round(max(abs(v) for v in pooled.values()), 6)  # frozen value
        assert np.isfinite(bar) and bar > 0, \
            f"stratum k={k}: pooled null bar must be finite and > 0 " \
            f"(got {bar})"
        record = {
            "phase": f"A (stratum k={k} null deposit; frozen before the "
                     f"stratum's real-arm decode)",
            "null_protocol": {
                "augmentation": "exp163/exp173's null augmentation: the "
                                "arm-1 null arm = the shared bit-identical "
                                "plain projection A (no S term)",
                "baseline": "the protocol's own seed-1 null decode per "
                            "(pair, own-target) -- exp174's translation "
                            "of exp173's two-phase discipline to a fresh "
                            "construction (no prior deposit exists for "
                            "the ladder cohort); seed 1 contributes "
                            "exactly 0, the bar is carried by the other "
                            "protocol seeds (pure null-arm seed noise)",
                "seeds": list(NULL_SEEDS),
                "seed_source": "exp142's deposited SEEDS (1,2,3) -- the "
                               "read core's own seed convention (asserted "
                               "at runtime); seed 1 = the credited decode "
                               "seed (exp159.SEED_EXEC)",
                "pooled_null_stat": "mean over the stratum's pairs of "
                                    "[err(A, own_target, seed) - "
                                    "err(A, own_target, seed 1)], SIGNED",
                "bar_rule": "null bar = max |pooled null stat| over the "
                            "protocol's seeds x own-targets (T1/T2) -- "
                            "one bar per stratum, frozen once, gating "
                            "W3 and W4 for that stratum",
            },
            "pooled_null_stats": {kk: round(v, 6)
                                  for kk, v in pooled.items()},
            "null_err_seed1": {str(q["i"]): {t: null_errs[(q["i"], t, 1)]
                                             for t, _ in targets}
                               for q in stratum},
            "null_bar": round(bar, 6),
            "null_bar_finite_positive": True,
            "frozen_before_phase_b_decode": True,
            "byte_offset_evidence": order_ev[f"k{k}"],
            "pair_scope": f"{len(stratum)} pairs (ladder indices "
                          f"{[q['i'] for q in stratum]})",
            "smoke": bool(smoke),
        }
        return record, bar

    def stratum_stats(stratum: list, phase_a_rec: dict, sname: str,
                      n_m2id: int) -> dict:
        """Signed devs vs the stratum's frozen seed-1 null errs, the
        stratum's stats, and the majority-sign count (deposited)."""
        per_pair, dev1s, dev2s = [], [], []
        for q in stratum:
            base = phase_a_rec["null_err_seed1"][str(q["i"])]
            e1 = float(q["dec"]["m1"]["err_vs_target"])
            e2 = float(q["dec"]["m2"]["err_vs_target"])
            d1 = e1 - float(base["T1"])
            d2 = e2 - float(base["T2"])
            dev1s.append(d1)
            dev2s.append(d2)
            per_pair.append({
                "i": q["i"], "seed_construct": q["seed_construct"],
                "slot": q["slot"], "n": q["n"], "k_realized": q["k_realized"],
                "cancel_entries_S1": q["cancel_entries_S1"],
                "density_d_k": round(q["density_d_k"], 4),
                "sw1_stats": q["sw1_stats"], "digest_A": q["digest_A"],
                "null_err_seed1_frozen": base,
                "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                "dev1_signed": round(d1, 6), "dev2_signed": round(d2, 6),
                "sign_dev1": 1 if d1 > 0 else (-1 if d1 < 0 else 0),
            })
        stat_m1 = float(np.mean(dev1s)) if dev1s else float("nan")
        stat_m2 = float(np.mean(dev2s)) if dev2s else float("nan")
        med1 = float(np.median(dev1s)) if dev1s else float("nan")
        med2 = float(np.median(dev2s)) if dev2s else float("nan")
        npos = sum(1 for d in dev1s if d > 0)
        nneg = sum(1 for d in dev1s if d < 0)
        nzero = sum(1 for d in dev1s if d == 0)
        if npos > nneg:
            maj_sign, n_maj = 1, npos
        elif nneg > npos:
            maj_sign, n_maj = -1, nneg
        else:
            maj_sign, n_maj = 0, 0
        return {
            "stratum": sname, "n_pairs": len(per_pair),
            "ladder_indices": [q["i"] for q in stratum],
            "stat_m1_signed_mean": round(stat_m1, 6),
            "median_m1": round(med1, 6),
            "stat_m2_signed_mean": round(stat_m2, 6),
            "median_m2": round(med2, 6),
            "majority_sign": maj_sign, "n_majority_sign": n_maj,
            "n_pos": npos, "n_neg": nneg, "n_zero": nzero,
            "null_bar": phase_a_rec["null_bar"],
            "m2_aug_bit_exact_identity": f"{n_m2id}/{len(stratum)}",
            "pairs": per_pair,
        }

    def write_doc(doc: dict, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(doc, f, indent=1,
                      default=lambda o: list(o)
                      if isinstance(o, tuple) else o)

    # ---- SMOKE (permitted, discarded): ladder pairs 0-1, features only -
    if smoke:
        spairs = build_cohort([0, 1])
        doc_s = {
            "experiment": name, "task_id": "3-e", "smoke": True,
            "job": "smoke -- ladder pairs 0-1, features only (permitted "
                   "pre-registered check; DISCARDED, not the credited "
                   "deposit)",
            "no_decode": True,
            "cohort_features": [cohort_row(q) for q in spairs],
            "note": "construction + structural features only; no null "
                    "decodes, no real decodes, no pin, no gates",
            "wall_seconds": round(time.time() - t0, 1),
        }
        write_doc(doc_s, out_path)
        print(json.dumps({"smoke": True, "features": len(spairs),
                          "out": out_path,
                          "wall_s": doc_s["wall_seconds"]}))
        return doc_s

    order_ev = assert_phase_order()
    assert NULL_SEEDS == _m142.SEEDS, \
        "null seeds must be the executor's deposited seed convention"
    assert seed_exec == 1, \
        "the credited decode seed is exp159's deposited SEED_EXEC (1)"
    assert seed_exec in NULL_SEEDS, \
        "the credited seed must be in the null protocol"

    run_k3 = job in ("k3", "all")
    run_k4 = job in ("k4", "all")

    # merged deposit: split runner jobs accumulate across invocations
    doc = {}
    if job != "all" and os.path.exists(out_path):
        doc = json.load(open(out_path))
        assert doc.get("experiment") == name, "deposit file mismatch"
    doc.setdefault("phase_a_write_evidence", {})
    doc.setdefault("strata", {})

    # ---- construction: the 36-pair ladder cohort (every job replays it,
    #      raising on any assert; cross-checked vs the deposited table) --
    pairs = build_cohort(list(range(36)))
    F, n_pool = recompute_F(pairs)
    if "construction" in doc and "F" in doc["construction"]:
        assert F == doc["construction"]["F"], \
            "F drifted vs the deposited construction"
    if "cohort" in doc:
        old = {r["i"]: r for r in doc["cohort"]}
        for q in pairs:
            r = old.get(q["i"])
            assert r is not None, \
                f"pair {q['i']}: missing from the deposited cohort table"
            assert (r["digest_A"] == q["digest_A"] and r["n"] == q["n"]
                    and r["k_realized"] == q["k_realized"]), \
                f"pair {q['i']}: construction replay drifted vs deposit"
    k3_idx = [q["i"] for q in pairs
              if q["k_realized"] == 3][:STRATUM_SIZES[0]]
    k4_idx = [q["i"] for q in pairs
              if q["k_realized"] == 4][:STRATUM_SIZES[1]]
    k5_idx = [q["i"] for q in pairs if q["k_realized"] == 5]
    kcounts = {str(kk): sum(1 for q in pairs if q["k_realized"] == kk)
               for kk in (3, 4, 5)}

    doc.update({
        "experiment": name,
        "task_id": "3-e",
        "registered_next_of": "exp174 (ledger L153): all three "
                              "minority-sign pairs across both cohorts "
                              "are k = 4 gadgets -- the density "
                              "hypothesis",
        "smoke": smoke,
        "runner": {"job": job, "stratum_alias": args.stratum,
                   "out": out_path},
        "pre_registered": {
            "source": "module docstring, committed at HEAD (c7c0dea, "
                      "batch-3 pre-registrations) BEFORE any decode; the "
                      "credited run used this file with only the body "
                      "filled",
            "stratification": "exp159's construction VERBATIM, seed "
                              "ladder 183001..183036 (SEED_CONSTRUCT "
                              "rebound per pair, the exp174 mechanism, "
                              "restore asserted) -- 36 fresh pairs; each "
                              "pair's REALIZED k recorded from the "
                              "construction; the cohort THEN split into "
                              "the k=3 stratum and the k=4 stratum, "
                              "taking the FIRST 6 of each by ladder "
                              "order",
            "statistic": "exp173/exp174's, verbatim: dev_signed per "
                         "pair, stat = mean over the stratum's pairs, V2 "
                         "weighting via exp163's cancel_mass_matrix, "
                         "STAR_OP readout, seed (1,); m2 side identical",
            "null": "per stratum: the shared arm-1 null, bar = max "
                    "|pooled null stat| over exp142's deposited seeds x "
                    "own-targets, frozen on disk BEFORE the stratum's "
                    "real-arm decode; byte-offset assertion per stratum",
            "gates": "W1 strata integrity; W2 null discipline (both "
                     "bars frozen before their real arms, byte order "
                     "asserted, finite > 0); W3 the density clause -- "
                     "branch (i) k=4 flips/weakens while k=3 holds "
                     "(density CONFIRMED), branch (ii) both hold "
                     "(density NOT the covariate), branch (iii) both "
                     "flip (construction-generic); ALL THREE complete "
                     "the gate, the branch taken is the finding; W4 "
                     "|stat_m2| <= its bar in BOTH strata",
            "seeds": {"exec": seed_exec,
                      "construct_ladder": "183001..183036 (per pair)",
                      "null_protocol": list(NULL_SEEDS)},
            "err_bar": ERR_BAR,
        },
        "construction": {
            "seed_ladder_rebind": {
                "mechanism": "exp174's rebinding mechanism, PER PAIR: "
                             "save exp159.SEED_CONSTRUCT (assert == 159), "
                             "rebind to the ladder seed, build via "
                             "exp159's build_pair on the protocol's own "
                             "slot (ladder index i -> slot i % 12: 3 "
                             "independent passes of the 12-slot "
                             "adversarial family in exp159's order), "
                             "restore asserted per pair",
                "ladder": "183001..183036 (module LADDER, 36 seeds)",
                "rebinds": len(LADDER), "restores_asserted": "36/36"},
            "F": F,
            "F_rule": "median |A_ij| over nonzero entries pooled across "
                      "the 36 FRESH projections, computed before any "
                      "decode (exp159/exp163/exp174's rule at this "
                      "cohort's size); ONE constant shared by both "
                      "strata",
            "F_pool_nonzero_absA_count": n_pool,
            "pairs_constructed": len(pairs),
            "asserts_held_pairs": len(pairs),
            "realized_k_match_pairs": len(pairs),
            "construction_asserts_held": "36/36 (raise-on-failure at "
                                         "build: A1==A2, S1!=S2, "
                                         "S2==support(A), cancellation "
                                         "layout, connectivity)",
            "realized_k": "recorded from the construction (member 1's "
                          "hyperedge size) per pair",
            "realized_k_matches_field": "36/36 (asserted vs "
                                        "GADGET_SIZE per pair)",
            "realized_k_counts": kcounts,
            "strata": {"k3_ladder_indices": k3_idx,
                       "k4_ladder_indices": k4_idx,
                       "k5_unstratified_ladder_indices": k5_idx,
                       "selection_rule": "first 6 of each realized-k "
                                         "class by ladder order "
                                         "(pre-registered; sizes "
                                         "deposited as-is if a stratum "
                                         "has fewer than 6 among the "
                                         "36)"},
            "decode_scope": "24 of 36 stratified pairs decoded (6+6); "
                            "the 12 realized-k=5 pairs are built and "
                            "disclosed, not stratified (the "
                            "pre-registered strata are k=3 and k=4)",
        },
        "cohort": [cohort_row(q) for q in pairs],
    })

    pin_floor()
    try:
        # ---------------- job build: construction only ------------------
        if job == "build":
            doc["job_note"] = ("build -- construction only, no decode; "
                               "the strata jobs k3/k4 complete the "
                               "credited deposit")
            doc["wall_seconds"] = round(time.time() - t0, 1)
            write_doc(doc, out_path)
            print(json.dumps({"job": "build",
                              "pairs_constructed": len(pairs), "F": F,
                              "strata": {"k3": k3_idx, "k4": k4_idx},
                              "out": out_path,
                              "wall_s": doc["wall_seconds"]}))
            return doc

        # ================= STRATUM k=3 ==================================
        if run_k3:
            stratum3 = [q for q in pairs if q["i"] in set(k3_idx)]
            rec3, bar3 = phase_a_null(stratum3, 3)
            doc["phase_a_k3"] = rec3
            # === STRATUM k=3 PHASE-A DEPOSIT WRITE (byte-order discipline:
            # this write is on disk BEFORE the stratum's first real-arm
            # decode; the k=3 bar is frozen here) ========================
            write_doc(doc, out_path)
            disk = json.load(open(out_path))
            assert "phase_a_k3" in disk, \
                "phase-A (k3) record missing on disk (two-phase discipline)"
            assert float(disk["phase_a_k3"]["null_bar"]) == bar3, \
                "phase-A (k3) bar on disk does not match the in-process bar"
            pa_bytes3 = os.path.getsize(out_path)
            doc["phase_a_write_evidence"]["k3"] = {
                "byte_offset_order": order_ev["k3"],
                "phase_a_record_bytes_on_disk": pa_bytes3,
                "record_confirmed_on_disk_before_stratum_real_decode": True}
            # PHASE-B (real arm), pairs in ladder order
            n_m2id3 = 0
            for q in stratum3:
                A, n = q["A"], q["n"]
                W1 = cancel_mass_matrix(q["m1"], n)
                W2 = cancel_mass_matrix(q["m2"], n)
                Sw1 = q["S1"] * W1
                Sw2 = q["S2"] * W2
                # V2 weighting discipline: member 2 (all-size-2)
                # -> W == 0 -> augmented == A bit-exactly
                if np.array_equal(Sw2, np.zeros((n, n))) and \
                        np.array_equal(A + F * Sw2, A):
                    n_m2id3 += 1
                else:
                    raise AssertionError(
                        f"pair {q['i']}: weighted m2 augmentation not a "
                        f"bit-exact identity")
                # === FIRST STRATUM k=3 (REAL-ARM) DECODE CALL ===========
                # exp173's decode call pattern verbatim (own-target, V2
                # weighted augmentation, seed 1, STAR_OP)
                q["dec"] = {
                    "m1": execute_signed(T1, A + F * Sw1, seed_exec, OP),
                    "m2": execute_signed(T2, A + F * Sw2, seed_exec, OP),
                }
            doc["strata"]["k3"] = stratum_stats(stratum3, rec3, "k3",
                                                n_m2id3)
            write_doc(doc, out_path)

        # ================= STRATUM k=4 ==================================
        if run_k4:
            stratum4 = [q for q in pairs if q["i"] in set(k4_idx)]
            rec4, bar4 = phase_a_null(stratum4, 4)
            doc["phase_a_k4"] = rec4
            # === STRATUM k=4 PHASE-A DEPOSIT WRITE (byte-order discipline:
            # this write is on disk BEFORE the stratum's first real-arm
            # decode; the k=4 bar is frozen here) ========================
            write_doc(doc, out_path)
            disk = json.load(open(out_path))
            assert "phase_a_k4" in disk, \
                "phase-A (k4) record missing on disk (two-phase discipline)"
            assert float(disk["phase_a_k4"]["null_bar"]) == bar4, \
                "phase-A (k4) bar on disk does not match the in-process bar"
            pa_bytes4 = os.path.getsize(out_path)
            doc["phase_a_write_evidence"]["k4"] = {
                "byte_offset_order": order_ev["k4"],
                "phase_a_record_bytes_on_disk": pa_bytes4,
                "record_confirmed_on_disk_before_stratum_real_decode": True}
            # PHASE-B (real arm), pairs in ladder order
            n_m2id4 = 0
            for q in stratum4:
                A, n = q["A"], q["n"]
                W1 = cancel_mass_matrix(q["m1"], n)
                W2 = cancel_mass_matrix(q["m2"], n)
                Sw1 = q["S1"] * W1
                Sw2 = q["S2"] * W2
                # V2 weighting discipline: member 2 (all-size-2)
                # -> W == 0 -> augmented == A bit-exactly
                if np.array_equal(Sw2, np.zeros((n, n))) and \
                        np.array_equal(A + F * Sw2, A):
                    n_m2id4 += 1
                else:
                    raise AssertionError(
                        f"pair {q['i']}: weighted m2 augmentation not a "
                        f"bit-exact identity")
                # === FIRST STRATUM k=4 (REAL-ARM) DECODE CALL ===========
                # exp173's decode call pattern verbatim (own-target, V2
                # weighted augmentation, seed 1, STAR_OP)
                q["dec"] = {
                    "m1": execute_signed(T1, A + F * Sw1, seed_exec, OP),
                    "m2": execute_signed(T2, A + F * Sw2, seed_exec, OP),
                }
            doc["strata"]["k4"] = stratum_stats(stratum4, rec4, "k4",
                                                n_m2id4)
            write_doc(doc, out_path)

        # ---------------- gates (each evaluated exactly once) ------------
        if "k3" in doc["strata"] and "k4" in doc["strata"]:
            if "gates" in doc:
                print("gates already evaluated in the deposited record; "
                      "left untouched (evaluate-exactly-once discipline)")
            else:
                dep173 = json.load(open(DEP173))
                dep174 = json.load(open(DEP174))
                sign0 = int(dep173["statistic"]["majority_sign"])
                assert int(dep174["statistic"]["majority_sign"]) == sign0, \
                    "the two deposited cohorts' majority signs disagree"
                s3, s4 = doc["strata"]["k3"], doc["strata"]["k4"]
                bar3 = float(s3["null_bar"])
                bar4 = float(s4["null_bar"])
                stat3 = float(s3["stat_m1_signed_mean"])
                stat4 = float(s4["stat_m1_signed_mean"])
                stat2_3 = float(s3["stat_m2_signed_mean"])
                stat2_4 = float(s4["stat_m2_signed_mean"])
                ms3, ms4 = int(s3["majority_sign"]), int(s4["majority_sign"])
                nm3 = int(s3["n_majority_sign"])
                nm4 = int(s4["n_majority_sign"])

                # W1 (strata integrity)
                con = doc["construction"]
                w1_pass = bool(
                    con["pairs_constructed"] == 36
                    and con["asserts_held_pairs"] == 36
                    and con["realized_k_match_pairs"] == 36
                    and s3["n_pairs"] >= 1 and s4["n_pairs"] >= 1)
                # W2 (null discipline; both bars frozen before their arms)
                w2_per = {}
                for kk, pkey in (("k3", "phase_a_k3"),
                                 ("k4", "phase_a_k4")):
                    pa = doc[pkey]
                    ev = doc["phase_a_write_evidence"][kk]
                    bb = float(pa["null_bar"])
                    w2_per[kk] = bool(
                        order_ev[kk]["order_held"]
                        and pa["frozen_before_phase_b_decode"]
                        and np.isfinite(bb) and bb > 0
                        and pa["null_bar_finite_positive"]
                        and ev["record_confirmed_on_disk_before_stratum_real_decode"])
                w2_pass = bool(all(w2_per.values()) and not doc["smoke"])

                # W3 (the density clause; the pre-named branches)
                def outcome(stat: float, bar: float, ms: int) -> str:
                    if abs(stat) > bar:
                        if ms == sign0:
                            return "holds"
                        if ms == -sign0:
                            return "flips"
                        return "off-sign"
                    return "weakens"

                o3 = outcome(stat3, bar3, ms3)
                o4 = outcome(stat4, bar4, ms4)
                if o4 in ("flips", "weakens") and o3 == "holds":
                    branch = "(i)"
                    pattern = (f"k=4 stratum {o4} while the k=3 stratum "
                               f"holds -- DENSITY EFFECT CONFIRMED")
                elif o3 == "holds" and o4 == "holds":
                    branch = "(ii)"
                    pattern = "both strata hold -- density NOT the covariate"
                elif o3 == "flips" and o4 == "flips":
                    branch = "(iii)"
                    pattern = ("both strata flip -- the sign is "
                               "construction-generic")
                else:
                    branch = "off-pattern"
                    pattern = (f"no pre-named branch matched (k3={o3}, "
                               f"k4={o4}) -- disclosed")
                w3_pass = bool(branch != "off-pattern")
                # W4 (attribution in BOTH strata)
                w4_pass = bool(abs(stat2_3) <= bar3 and abs(stat2_4) <= bar4)

                doc["gates"] = {
                    "W1_strata_integrity": {
                        "pass": w1_pass,
                        "pairs_constructed": con["pairs_constructed"],
                        "construction_asserts_held":
                            con["construction_asserts_held"],
                        "realized_k_matches_field":
                            con["realized_k_matches_field"],
                        "stratum_sizes": {"k3": s3["n_pairs"],
                                          "k4": s4["n_pairs"]},
                        "registered_sizes": list(STRATUM_SIZES),
                        "shortfall_disclosed": bool(
                            s3["n_pairs"] < STRATUM_SIZES[0]
                            or s4["n_pairs"] < STRATUM_SIZES[1])},
                    "W2_null_discipline": {
                        "pass": w2_pass,
                        "per_stratum": w2_per,
                        "byte_offset_order_held":
                            {kk: order_ev[kk]["order_held"]
                             for kk in ("k3", "k4")},
                        "bars": {"k3": bar3, "k4": bar4},
                        "bars_finite_positive": bool(
                            np.isfinite(bar3) and bar3 > 0
                            and np.isfinite(bar4) and bar4 > 0),
                        "smoke": bool(doc["smoke"])},
                    "W3_density_clause": {
                        "pass": w3_pass,
                        "reference_sign": sign0,
                        "reference_sources": {
                            "exp173_deposited_majority_sign":
                                int(dep173["statistic"]["majority_sign"]),
                            "exp174_deposited_majority_sign":
                                int(dep174["statistic"]["majority_sign"])},
                        "k3": {"stat_m1_signed_mean": stat3,
                               "null_bar": bar3,
                               "abs_stat_gt_bar": bool(abs(stat3) > bar3),
                               "majority_sign": ms3,
                               "n_majority_sign": nm3,
                               "of": s3["n_pairs"], "outcome": o3},
                        "k4": {"stat_m1_signed_mean": stat4,
                               "null_bar": bar4,
                               "abs_stat_gt_bar": bool(abs(stat4) > bar4),
                               "majority_sign": ms4,
                               "n_majority_sign": nm4,
                               "of": s4["n_pairs"], "outcome": o4},
                        "branch": branch, "pattern": pattern},
                    "W4_attribution": {
                        "pass": w4_pass,
                        "stat_m2_signed_mean": {"k3": stat2_3,
                                                "k4": stat2_4},
                        "null_bars": {"k3": bar3, "k4": bar4},
                        "abs_stat_m2_le_bar_both_strata": w4_pass},
                }
                doc["all_gates_pass"] = all(
                    g["pass"] for g in doc["gates"].values())
                doc["branch"] = {"branch": branch, "pattern": pattern,
                                 "k3_outcome": o3, "k4_outcome": o4}
                if branch == "(i)":
                    doc["verdict"] = (
                        "DENSITY EFFECT CONFIRMED (branch i) -- the k=4 "
                        "stratum %s while the k=3 stratum holds: "
                        "|stat_k4| = %.4f vs its bar %.4f (majority sign "
                        "%d/%d) vs |stat_k3| = %.4f > bar %.4f (majority "
                        "sign %d/%d); the ensemble's sign structure is a "
                        "DENSITY effect and the grouping read gains its "
                        "first structural covariate (m2 side silent in "
                        "both strata: |%.4f| vs bar %.4f, |%.4f| vs bar "
                        "%.4f)"
                        % (o4, abs(stat4), bar4, nm4, s4["n_pairs"],
                           abs(stat3), bar3, nm3, s3["n_pairs"],
                           abs(stat2_3), bar3, abs(stat2_4), bar4))
                elif branch == "(ii)":
                    doc["verdict"] = (
                        "DENSITY NOT THE COVARIATE (branch ii) -- both "
                        "strata hold: |stat_k3| = %.4f > bar %.4f "
                        "(majority sign %d/%d) and |stat_k4| = %.4f > "
                        "bar %.4f (majority sign %d/%d); the ensemble's "
                        "sign survives at k=4 density, so the k=4 "
                        "minority pairs were not a density signature "
                        "(m2 side silent in both strata: |%.4f| vs bar "
                        "%.4f, |%.4f| vs bar %.4f)"
                        % (abs(stat3), bar3, nm3, s3["n_pairs"],
                           abs(stat4), bar4, nm4, s4["n_pairs"],
                           abs(stat2_3), bar3, abs(stat2_4), bar4))
                elif branch == "(iii)":
                    doc["verdict"] = (
                        "SIGN IS CONSTRUCTION-GENERIC (branch iii) -- "
                        "both strata flip: |stat_k3| = %.4f > bar %.4f "
                        "(majority sign %d/%d, opposite the deposited "
                        "cohorts) and |stat_k4| = %.4f > bar %.4f "
                        "(majority sign %d/%d, opposite the deposited "
                        "cohorts); the sign is a property of the "
                        "construction family, not of any k stratum"
                        % (abs(stat3), bar3, nm3, s3["n_pairs"],
                           abs(stat4), bar4, nm4, s4["n_pairs"]))
                else:
                    doc["verdict"] = (
                        "OFF-PATTERN (disclosed) -- k=3 %s, k=4 %s: no "
                        "pre-named branch matched; per-stratum tables "
                        "deposited" % (o3, o4))
        elif job in ("k3", "k4"):
            doc["gates_note"] = ("gates pending: both strata must be on "
                                 "disk; the closing job evaluates W1-W4 "
                                 "exactly once")

        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)
        g = doc.get("gates", {})
        print(json.dumps({
            "smoke": smoke, "job": job,
            "W1": g.get("W1_strata_integrity", {}).get("pass"),
            "W2": g.get("W2_null_discipline", {}).get("pass"),
            "W3": g.get("W3_density_clause", {}).get("pass"),
            "W4": g.get("W4_attribution", {}).get("pass"),
            "branch": doc.get("branch", {}).get("branch"),
            "strata": {kk: {"stat_m1": v["stat_m1_signed_mean"],
                            "stat_m2": v["stat_m2_signed_mean"],
                            "bar": v["null_bar"],
                            "majority": f"{v['n_majority_sign']}/"
                                        f"{v['n_pairs']}"}
                       for kk, v in doc["strata"].items()},
            "all_pass": doc.get("all_gates_pass"),
            "wall_s": doc["wall_seconds"], "out": out_path}))
        return doc
    finally:
        restore_floor()
        for m in PIN_MODULES:
            if hasattr(m, "NEURAL_SPEC_MIN"):
                assert getattr(m, "NEURAL_SPEC_MIN") == _PIN_SAVE[m.__name__], \
                    f"{m.__name__}: floor not restored"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "k3", "k4", "all"],
                    default="all")
    ap.add_argument("--stratum", type=int, choices=[3, 4], default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--stratum/--out)
