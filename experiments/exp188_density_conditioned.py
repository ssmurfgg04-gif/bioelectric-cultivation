#!/usr/bin/env python3
"""exp188 — THE DENSITY-CONDITIONED ENSEMBLE (the grouping read's
production form).

exp183's registered next (from its L160 finding, branch (i)): the
ensemble's sign structure is a DENSITY effect (k = 3 stratum holds,
k = 4 weakens) — the grouping read gains its first structural
covariate. THIS EXPERIMENT conditions the statistic on the covariate
and validates on a THIRD cohort: stat = the signed mean over the
k = 3 stratum ONLY (d_k-conditioned), tested on 36 fresh pairs
(ladder 188001..188036, exp183's protocol verbatim).

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Conditioning, cohort, and gates fixed.

THE CONDITIONED STATISTIC (zero new knobs): per pair, realized k and
d_k recorded; the conditioned stat = the signed mean over the k = 3
stratum ONLY. The unconditioned mean is computed for contrast
(recorded, not gated). Two-phase nulls per stratum (exp183's
protocol): bars frozen on disk before the stratum's real arm.

GATES (each evaluated exactly once):
  GATE-D1 (cohort integrity) 36 fresh pairs, construction asserts
           36/36, realized-k classification 36/36; independence from
           both prior cohorts (no projection bit-equal to any).
  GATE-D2 (null discipline) per-stratum bars frozen before their
           real arms (byte order); finite > 0.
  GATE-D3 (the conditioning claim) on the THIRD cohort: the k = 3
           stratum's conditioned stat > its bar with a majority
           sign (>= 5/6 if 6 pairs exist), AND the conditioned stat
           EXCEEDS the unconditioned stat in magnitude (conditioning
           buys power on independent draws); if the cohort's k = 3
           stratum has < 4 pairs, the gate evaluates on what exists
           (disclosed).
  GATE-D4 (attribution) the k = 4 stratum and the m2 side both
           silent (<= their bars) — the contrast stays attributable.

NO post-hoc tuning. --smoke (ladder pairs 0-1, features only)
permitted, discarded. Deposit: results/exp188_density_conditioned.json
Jobs: build | k3 | k4
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
    build_pair, co_membership, project, connected, T1, T2, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

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


LADDER = list(range(188001, 188037))

OUT = os.path.join(ROOT, "results", "exp188_density_conditioned.json")
DEP183 = os.path.join(ROOT, "results", "exp183_k_controlled_cohort.json")


def main() -> dict:
    import hashlib
    import math
    import time
    t0 = time.time()

    # ---- body-level constants (fixed here, BEFORE any decode) ----------
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["build", "k3", "k4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    smoke = bool(args.smoke)
    job = args.job
    out_path = args.out or (OUT + ".smoke.json" if smoke else OUT)
    name = "exp188_the_density_conditioned_ensemble"
    STRATUM_SIZES = (6, 6)
    DEP174 = os.path.join(ROOT, "results", "exp174_replication_cohort.json")
    DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")

    # The null protocol's seeds: the read core's own deposited seed
    # convention (exp142.SEEDS = (1, 2, 3), asserted at runtime).  The
    # fresh ladder cohort has no prior deposit, so per (pair, own-target)
    # the seed-1 null decode is the baseline -- exp174's translation of
    # exp173's two-phase discipline to a fresh construction, zero new
    # choices; seed 1 contributes exactly 0 and the bar is carried by
    # the protocol's other seeds (pure null-arm seed noise).
    NULL_SEEDS = (1, 2, 3)
    seed_exec = exp159.SEED_EXEC          # the credited decode seed (1)

    # per-stratum byte-order markers (exp168/exp173/exp183's discipline,
    # per stratum as the docstring registers)
    _PHASE_A_WRITE_MARKER = {
        3: "# === STRATUM k=3 PHASE-A DEPOSIT WRITE (byte-order discipline",
        4: "# === STRATUM k=4 PHASE-A DEPOSIT WRITE (byte-order discipline",
    }
    _PHASE_B_DECODE_MARKER = {
        3: "# === FIRST STRATUM k=3 (REAL-ARM) DECODE CALL",
        4: "# === FIRST STRATUM k=4 (REAL-ARM) DECODE CALL",
    }

    def assert_phase_order() -> dict:
        """D2's byte-offset assertion, PER STRATUM (exp173/exp183's
        mechanism): each stratum's phase-A deposit write precedes that
        stratum's first real-arm decode call, by byte offset in this
        file."""
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
        """THE DENSITY-CONDITIONED COHORT (exp183's protocol, verbatim):
        exp159's construction with the ONE changed input disclosed
        pre-run -- exp159.SEED_CONSTRUCT rebound PER PAIR along the
        ladder 188001..188036 (the exp174 rebinding mechanism: save,
        rebind, build, restore asserted -- per pair here); the build
        call is exp159's build_pair on the protocol's own 12 slots in
        exp159's order (ladder index i -> slot i % 12: the 36 fresh
        pairs are 3 independent passes of the 12-slot adversarial
        family with independent draws).  Per pair the exp163/exp173
        construction asserts: A1 == A2 bit-identical, S1 != S2,
        S2 == support(A) (all-size-2 reduction), cancellation layout,
        connectivity; the pair's REALIZED k is recorded from the
        construction (member 1's hyperedge size) and asserted against
        the construction's own k field (exp159.GADGET_SIZE)."""
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
            k_field = int(exp159.GADGET_SIZE[slot])  # the construction's k
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
        """F, computed BEFORE any decode by exp159/exp163/exp183's
        pre-registered rule applied to this cohort: median |A_ij| over
        nonzero entries pooled across the 36 FRESH projections; ONE
        constant shared by both strata."""
        pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in ps])
        return float(np.median(np.abs(pool))), int(pool.size)

    def prior_cohort_digests() -> dict:
        """D1's independence evidence (construction only, ZERO decodes,
        run BEFORE any decode): the two prior cohorts' projections,
        rebuilt bit-exactly from their deposited protocols and digested
        -- exp173's ORIGINAL 12 (build_pair slots 0..11 at the deposited
        SEED_CONSTRUCT 159) and exp174's replication 12 (exp174's own
        mechanism: ONE rebind of SEED_CONSTRUCT to 174174, slots 0..11
        in order, restore asserted); plus exp183's k-controlled 36,
        whose digest_A rows are read straight from its deposit.  Each
        rebuilt projection is cross-checked against its deposit row's
        (p, n, k) before digesting."""
        dep173 = json.load(open(DEP173))
        dep174 = json.load(open(DEP174))
        out = {
            "exp173_original_12": {
                "source": "rebuilt at the deposited SEED_CONSTRUCT 159 "
                          "(exp159's build_pair, slots 0..11 in order; "
                          "the original cohort exp174 itself rebuilt for "
                          "its F1 independence check)",
                "digests": [], "cross_checked_rows": 0},
            "exp174_replication_12": {
                "source": "rebuilt via exp174's own mechanism: ONE "
                          "rebind of exp159.SEED_CONSTRUCT to 174174, "
                          "build_pair slots 0..11 in order, restore "
                          "asserted",
                "digests": [], "cross_checked_rows": 0},
            "exp183_k_controlled_36": {
                "source": "digest_A read from the deposited cohort "
                          "table of results/exp183_k_controlled_cohort"
                          ".json (36 rows)",
                "digests": [], "cross_checked_rows": 0},
        }
        saved = exp159.SEED_CONSTRUCT
        assert saved == 159, "SEED_CONSTRUCT drifted before the rebuild"
        # exp173's originals: seed 159 (the saved value), slots 0..11
        for p in range(12):
            n, m1, _m2 = build_pair(p)
            A = project(m1, n)
            row = dep173["pairs"][p]
            assert int(row["p"]) == p, f"exp173 row order broken at {p}"
            assert int(row["n"]) == int(n), f"exp173 pair {p}: n drift"
            kr = int(sorted({len(nodes) for nodes, _ in m1})[0])
            assert int(row["k"]) == kr, f"exp173 pair {p}: k drift"
            out["exp173_original_12"]["digests"].append(hashlib.sha256(
                np.ascontiguousarray(A).tobytes()).hexdigest())
            out["exp173_original_12"]["cross_checked_rows"] += 1
        # exp174's replication: ONE rebind to 174174, slots 0..11
        exp159.SEED_CONSTRUCT = 174174
        assert exp159.SEED_CONSTRUCT == 174174, "exp174 rebind failed"
        for p in range(12):
            n, m1, _m2 = build_pair(p)
            A = project(m1, n)
            row = dep174["pairs"][p]
            assert int(row["p"]) == p, f"exp174 row order broken at {p}"
            assert int(row["n"]) == int(n), f"exp174 pair {p}: n drift"
            kr = int(sorted({len(nodes) for nodes, _ in m1})[0])
            assert int(row["k"]) == kr, f"exp174 pair {p}: k drift"
            out["exp174_replication_12"]["digests"].append(hashlib.sha256(
                np.ascontiguousarray(A).tobytes()).hexdigest())
            out["exp174_replication_12"]["cross_checked_rows"] += 1
        exp159.SEED_CONSTRUCT = saved               # RESTORE
        assert exp159.SEED_CONSTRUCT == saved == 159, \
            "SEED_CONSTRUCT not restored after the prior-cohort rebuild"
        dep183 = json.load(open(DEP183))
        out["exp183_k_controlled_36"]["digests"] = \
            [r["digest_A"] for r in dep183["cohort"]]
        out["exp183_k_controlled_36"]["cross_checked_rows"] = \
            len(dep183["cohort"])
        return out

    def phase_a_null(stratum: list, k: int) -> tuple:
        """PHASE-A for one stratum (exp173's two-phase null discipline,
        exp174/exp183's fresh-cohort translation, zero new choices):
        the stratum's pooled null distribution from the SHARED arm-1
        null decode of the bit-identical plain projection; per (pair,
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
                            "D3 and D4 for that stratum",
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
            "experiment": name, "task_id": "4-e", "smoke": True,
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
    # D1 independence evidence: prior cohorts' projections, digested;
    # construction-only, BEFORE any decode
    prior = prior_cohort_digests()
    cohort_digests = [q["digest_A"] for q in pairs]
    within_distinct = len(set(cohort_digests)) == len(cohort_digests)
    prior_overlap = {src: sorted(set(v["digests"]) & set(cohort_digests))
                     for src, v in prior.items()}
    independent_of_prior = all(len(v) == 0 for v in prior_overlap.values())
    k3_idx = [q["i"] for q in pairs
              if q["k_realized"] == 3][:STRATUM_SIZES[0]]
    k4_idx = [q["i"] for q in pairs
              if q["k_realized"] == 4][:STRATUM_SIZES[1]]
    k5_idx = [q["i"] for q in pairs if q["k_realized"] == 5]
    kcounts = {str(kk): sum(1 for q in pairs if q["k_realized"] == kk)
               for kk in (3, 4, 5)}

    doc.update({
        "experiment": name,
        "task_id": "4-e",
        "registered_next_of": "exp183 (ledger L160, branch (i) DENSITY "
                              "EFFECT CONFIRMED): the k=3 stratum holds, "
                              "k=4 weakens -- the grouping read's "
                              "registered next conditions the statistic "
                              "on the covariate (the k=3-conditioned "
                              "ensemble)",
        "smoke": smoke,
        "runner": {"job": job, "out": out_path},
        "pre_registered": {
            "source": "module docstring, committed at HEAD (357faa4, "
                      "batch-4 pre-registrations) BEFORE any decode; the "
                      "credited run used this file with only the body "
                      "filled",
            "conditioned_statistic": "zero new knobs: per pair, realized "
                                     "k and d_k recorded; the conditioned "
                                     "stat = the signed mean over the "
                                     "k=3 stratum ONLY; the unconditioned "
                                     "mean (signed mean over all decoded "
                                     "pairs) computed for contrast -- "
                                     "recorded, not gated",
            "stratification": "exp183's protocol verbatim: exp159's "
                              "construction, seed ladder 188001..188036 "
                              "(SEED_CONSTRUCT rebound per pair, the "
                              "exp174 mechanism, restore asserted) -- 36 "
                              "fresh pairs; each pair's REALIZED k "
                              "recorded from the construction; the "
                              "cohort THEN split into the k=3 stratum "
                              "and the k=4 stratum, taking the FIRST 6 "
                              "of each by ladder order",
            "statistic": "exp173/exp174/exp183's, verbatim: dev_signed "
                         "per pair, stat = mean over the stratum's "
                         "pairs, V2 weighting via exp163's "
                         "cancel_mass_matrix, STAR_OP readout, seed "
                         "(1,); m2 side identical",
            "null": "per stratum: the shared arm-1 null, bar = max "
                    "|pooled null stat| over exp142's deposited seeds x "
                    "own-targets, frozen on disk BEFORE the stratum's "
                    "real-arm decode; byte-offset assertion per stratum",
            "gates": "D1 cohort integrity (36 fresh pairs, construction "
                     "asserts 36/36, realized-k classification 36/36, "
                     "independence from both prior cohorts -- no "
                     "projection bit-equal to any); D2 null discipline "
                     "(per-stratum bars frozen before their real arms, "
                     "byte order asserted, finite > 0); D3 the "
                     "conditioning claim (the k=3 stratum's conditioned "
                     "stat > its bar with a majority sign >= 5/6 if 6 "
                     "pairs exist, AND the conditioned stat EXCEEDS the "
                     "unconditioned stat in magnitude; if the k=3 "
                     "stratum has < 4 pairs the gate evaluates on what "
                     "exists -- disclosed); D4 attribution (the k=4 "
                     "stratum and the m2 side both silent <= their "
                     "bars)",
            "seeds": {"exec": seed_exec,
                      "construct_ladder": "188001..188036 (per pair)",
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
                "ladder": "188001..188036 (module LADDER, 36 seeds)",
                "rebinds": len(LADDER), "restores_asserted": "36/36"},
            "F": F,
            "F_rule": "median |A_ij| over nonzero entries pooled across "
                      "the 36 FRESH projections, computed before any "
                      "decode (exp159/exp163/exp183's rule at this "
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
                                        "exp159.GADGET_SIZE per pair)",
            "realized_k_classification": {
                "classified_pairs": int(sum(kcounts.values())),
                "counts": kcounts,
                "note": "every one of the 36 pairs carries a realized k "
                        "recorded from the construction and asserted "
                        "against the construction's own k field"},
            "independence": {
                "prior_cohort_digest_sources": {
                    src: {"source": v["source"],
                          "n_digests": len(v["digests"]),
                          "cross_checked_rows": v["cross_checked_rows"]}
                    for src, v in prior.items()},
                "prior_overlap_pairs": prior_overlap,
                "within_cohort_digests_distinct": bool(within_distinct),
                "no_projection_bit_equal_to_any_prior": bool(
                    independent_of_prior)},
            "realized_k_counts": kcounts,
            "strata": {"k3_ladder_indices": k3_idx,
                       "k4_ladder_indices": k4_idx,
                       "k5_unstratified_ladder_indices": k5_idx,
                       "selection_rule": "first 6 of each realized-k "
                                         "class by ladder order "
                                         "(exp183's pre-registered rule; "
                                         "sizes deposited as-is if a "
                                         "stratum has fewer than 6 among "
                                         "the 36)"},
            "decode_scope": "12 of 36 decoded (6+6); the 12 realized-k=5 "
                            "pairs are built and disclosed, not "
                            "stratified (the pre-registered strata are "
                            "k=3 and k=4)",
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
                # === FIRST STRATUM k=3 (REAL-ARM) DECODE CALL ==========
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
                # === FIRST STRATUM k=4 (REAL-ARM) DECODE CALL ==========
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
                dep183 = json.load(open(DEP183))
                s3, s4 = doc["strata"]["k3"], doc["strata"]["k4"]
                bar3 = float(s3["null_bar"])
                bar4 = float(s4["null_bar"])
                cond = float(s3["stat_m1_signed_mean"])   # CONDITIONED
                stat4 = float(s4["stat_m1_signed_mean"])
                stat2_3 = float(s3["stat_m2_signed_mean"])
                stat2_4 = float(s4["stat_m2_signed_mean"])
                ms3, ms4 = int(s3["majority_sign"]), int(s4["majority_sign"])
                nm3 = int(s3["n_majority_sign"])
                nm4 = int(s4["n_majority_sign"])
                # the UNCONDITIONED contrast: signed mean of dev1 over
                # ALL decoded pairs (k3 + k4 strata) -- recorded, not
                # gated (the docstring's "unconditioned mean")
                all_dev1 = ([p["dev1_signed"] for p in s3["pairs"]]
                            + [p["dev1_signed"] for p in s4["pairs"]])
                uncond = float(np.mean(all_dev1))
                n_dec = len(all_dev1)

                # D1 (cohort integrity)
                con = doc["construction"]
                indep = con["independence"]
                d1_pass = bool(
                    con["pairs_constructed"] == 36
                    and con["asserts_held_pairs"] == 36
                    and con["realized_k_match_pairs"] == 36
                    and con["realized_k_classification"]["classified_pairs"]
                    == 36
                    and indep["within_cohort_digests_distinct"]
                    and indep["no_projection_bit_equal_to_any_prior"]
                    and s3["n_pairs"] >= 1 and s4["n_pairs"] >= 1)

                # D2 (null discipline; both bars frozen before their arms)
                d2_per = {}
                for kk, pkey in (("k3", "phase_a_k3"),
                                 ("k4", "phase_a_k4")):
                    pa = doc[pkey]
                    ev = doc["phase_a_write_evidence"][kk]
                    bb = float(pa["null_bar"])
                    d2_per[kk] = bool(
                        order_ev[kk]["order_held"]
                        and pa["frozen_before_phase_b_decode"]
                        and np.isfinite(bb) and bb > 0
                        and pa["null_bar_finite_positive"]
                        and ev["record_confirmed_on_disk_before_stratum_real_decode"])
                d2_pass = bool(all(d2_per.values()) and not doc["smoke"])

                # D3 (the conditioning claim, exactly as registered)
                n3 = int(s3["n_pairs"])
                # majority clause: >= 5/6 of the stratum's pairs; if the
                # k=3 stratum has < 4 pairs, the gate evaluates on what
                # exists (disclosed) -- bare majority of what exists
                required_majority = (int(math.ceil(5.0 / 6.0 * n3))
                                     if n3 >= 4 else 1)
                shortfall_disclosed = bool(n3 < STRATUM_SIZES[0])
                majority_ok = bool(nm3 >= required_majority)
                signed_bar_ok = bool(cond > bar3)     # registered wording
                abs_bar_ok = bool(abs(cond) > bar3)   # exp183's semantics
                power_ok = bool(abs(cond) > abs(uncond))
                d3_pass = bool(signed_bar_ok and majority_ok and power_ok)

                # D4 (attribution: the k=4 stratum AND the m2 side silent)
                d4_pass = bool(abs(stat4) <= bar4
                               and abs(stat2_3) <= bar3
                               and abs(stat2_4) <= bar4)

                doc["gates"] = {
                    "D1_cohort_integrity": {
                        "pass": d1_pass,
                        "pairs_constructed": con["pairs_constructed"],
                        "construction_asserts_held":
                            con["construction_asserts_held"],
                        "realized_k_matches_field":
                            con["realized_k_matches_field"],
                        "realized_k_classification":
                            con["realized_k_classification"],
                        "independence": {
                            "within_cohort_digests_distinct":
                                indep["within_cohort_digests_distinct"],
                            "no_projection_bit_equal_to_any_prior":
                                indep["no_projection_bit_equal_to_any_prior"],
                            "prior_overlap_pairs":
                                indep["prior_overlap_pairs"]},
                        "stratum_sizes": {"k3": s3["n_pairs"],
                                          "k4": s4["n_pairs"]},
                        "registered_sizes": list(STRATUM_SIZES),
                        "shortfall_disclosed": bool(
                            s3["n_pairs"] < STRATUM_SIZES[0]
                            or s4["n_pairs"] < STRATUM_SIZES[1])},
                    "D2_null_discipline": {
                        "pass": d2_pass,
                        "per_stratum": d2_per,
                        "byte_offset_order_held":
                            {kk: order_ev[kk]["order_held"]
                             for kk in ("k3", "k4")},
                        "bars": {"k3": bar3, "k4": bar4},
                        "bars_finite_positive": bool(
                            np.isfinite(bar3) and bar3 > 0
                            and np.isfinite(bar4) and bar4 > 0),
                        "smoke": bool(doc["smoke"])},
                    "D3_conditioning_claim": {
                        "pass": d3_pass,
                        "conditioned_stat_m1_signed_mean":
                            round(cond, 6),
                        "conditioned_scope":
                            f"the k=3 stratum ONLY ({n3} pairs)",
                        "unconditioned_stat_m1_signed_mean":
                            round(uncond, 6),
                        "unconditioned_scope":
                            f"all {n_dec} decoded pairs (k3 + k4 strata), "
                            f"recorded not gated",
                        "abs_conditioned": round(abs(cond), 6),
                        "abs_unconditioned": round(abs(uncond), 6),
                        "conditioning_buys_power_abs":
                            bool(abs(cond) > abs(uncond)),
                        "null_bar_k3": bar3,
                        "signed_stat_gt_bar": signed_bar_ok,
                        "abs_stat_gt_bar": abs_bar_ok,
                        "majority_sign": ms3,
                        "n_majority_sign": nm3, "of": n3,
                        "required_majority": required_majority,
                        "majority_ok": majority_ok,
                        "majority_matches_deposited_cohorts_sign":
                            bool(ms3 == 1),
                        "stratum_shortfall_disclosed": shortfall_disclosed,
                        "clauses": {"bar": signed_bar_ok,
                                    "majority": majority_ok,
                                    "power": power_ok}},
                    "D4_attribution": {
                        "pass": d4_pass,
                        "k4_stratum": {"stat_m1_signed_mean": stat4,
                                       "null_bar": bar4,
                                       "abs_stat_le_bar":
                                           bool(abs(stat4) <= bar4),
                                       "majority_sign": ms4,
                                       "n_majority_sign": nm4,
                                       "of": s4["n_pairs"]},
                        "m2_side": {"k3": {"stat_m2_signed_mean": stat2_3,
                                           "null_bar": bar3,
                                           "abs_stat_le_bar":
                                               bool(abs(stat2_3) <= bar3)},
                                    "k4": {"stat_m2_signed_mean": stat2_4,
                                           "null_bar": bar4,
                                           "abs_stat_le_bar":
                                               bool(abs(stat2_4) <= bar4)}},
                        "reference_context_recorded_not_gated": {
                            "exp183_k3_stratum": {
                                "stat_m1_signed_mean":
                                    dep183["strata"]["k3"]
                                    ["stat_m1_signed_mean"],
                                "null_bar":
                                    dep183["strata"]["k3"]["null_bar"],
                                "majority_sign":
                                    dep183["strata"]["k3"]["majority_sign"],
                                "n_majority_sign":
                                    dep183["strata"]["k3"]
                                    ["n_majority_sign"]},
                            "exp183_k4_stratum": {
                                "stat_m1_signed_mean":
                                    dep183["strata"]["k4"]
                                    ["stat_m1_signed_mean"],
                                "null_bar":
                                    dep183["strata"]["k4"]["null_bar"]}}},
                }
                doc["conditioned_statistic"] = {
                    "conditioned_stat_m1_signed_mean": round(cond, 6),
                    "unconditioned_stat_m1_signed_mean": round(uncond, 6),
                    "abs_conditioned": round(abs(cond), 6),
                    "abs_unconditioned": round(abs(uncond), 6),
                    "null_bar_k3": bar3,
                    "majority_sign": ms3,
                    "n_majority_sign": nm3, "of": n3,
                    "n_decoded_pairs": n_dec,
                    "definition": "conditioned = signed mean of dev1 over "
                                  "the k=3 stratum ONLY; unconditioned = "
                                  "signed mean of dev1 over all decoded "
                                  "pairs (recorded, not gated)"}
                doc["all_gates_pass"] = all(
                    g["pass"] for g in doc["gates"].values())
                if d3_pass:
                    doc["verdict"] = (
                        "CONDITIONING BUYS POWER (D3 PASS) -- the "
                        "k=3-conditioned stat |%.4f| > its frozen bar "
                        "%.4f (majority sign %d/%d) and EXCEEDS the "
                        "unconditioned mean |%.4f| over the %d decoded "
                        "pairs in magnitude: conditioning on the density "
                        "covariate buys power on independent draws (k=4 "
                        "stratum silent: |%.4f| <= bar %.4f; m2 side "
                        "silent in both strata: |%.4f| vs bar %.4f, "
                        "|%.4f| vs bar %.4f -- attribution clean)"
                        % (abs(cond), bar3, nm3, n3, abs(uncond), n_dec,
                           abs(stat4), bar4, abs(stat2_3), bar3,
                           abs(stat2_4), bar4))
                else:
                    failed = [cname for cname, ok in
                              (("bar", signed_bar_ok),
                               ("majority", majority_ok),
                               ("power", power_ok)) if not ok]
                    doc["verdict"] = (
                        "CONDITIONING CLAIM NOT CONFIRMED (D3 REFUTE; "
                        "failed clause(s): %s) -- conditioned |%.4f| vs "
                        "its bar %.4f (majority sign %d/%d, required "
                        "%d), unconditioned |%.4f| over the %d decoded "
                        "pairs; k=4 stratum |%.4f| vs bar %.4f, m2 side "
                        "|%.4f| vs bar %.4f, |%.4f| vs bar %.4f -- "
                        "tables deposited"
                        % (",".join(failed), abs(cond), bar3, nm3, n3,
                           required_majority, abs(uncond), n_dec,
                           abs(stat4), bar4, abs(stat2_3), bar3,
                           abs(stat2_4), bar4))
        elif job in ("k3", "k4"):
            doc["gates_note"] = ("gates pending: both strata must be on "
                                 "disk; the closing job evaluates D1-D4 "
                                 "exactly once")

        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)
        g = doc.get("gates", {})
        print(json.dumps({
            "smoke": smoke, "job": job,
            "D1": g.get("D1_cohort_integrity", {}).get("pass"),
            "D2": g.get("D2_null_discipline", {}).get("pass"),
            "D3": g.get("D3_conditioning_claim", {}).get("pass"),
            "D4": g.get("D4_attribution", {}).get("pass"),
            "conditioned": doc.get("conditioned_statistic", {}).get(
                "conditioned_stat_m1_signed_mean"),
            "unconditioned": doc.get("conditioned_statistic", {}).get(
                "unconditioned_stat_m1_signed_mean"),
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
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
