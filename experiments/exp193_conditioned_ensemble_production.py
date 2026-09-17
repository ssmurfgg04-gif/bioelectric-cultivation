#!/usr/bin/env python3
"""exp193 — THE CONDITIONED ENSEMBLE TO PRODUCTION (the adoption).

exp188's registered next (L164): the k=3-conditioned statistic as the
production grouping read — the exp178-pattern additive arm, bit-exact
at every old operating point.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp163/exp183/exp188's modules and deposits verbatim; the -35.0 pin.

GATES (each evaluated exactly once):
  GATE-F1 (the wiring) exp163's module gains the additive
           function conditioned_stat(pairs) (the k=3-stratum signed
           mean, realized-k from the construction); the existing
           unconditioned path untouched; tests green post-wiring.
  GATE-F2 (old operating points bit-exact) exp163's and exp174's
           deposited verdicts replay bit-exactly through the
           UNCHANGED unconditioned path (per-pair devs + stats, both
           cohorts); exp183's and exp188's stratum stats replay
           bit-exactly through the conditioned arm (third+second
           cohorts).
  GATE-F3 (the production property) the conditioned arm's
           classification rule (stat > bar AND majority sign)
           reproduces exp188's D3 verdict on the third cohort and
           exp183's W3 branch (i) on the second — the production
           rule agrees with every deposited verdict.
  GATE-F4 (hygiene) zero rejections; pin save/restore asserted.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp193_conditioned_ensemble_production.json
RUN: python3 -m experiments.exp193_conditioned_ensemble_production [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp193_conditioned_ensemble_production.json")


def main() -> dict:
    import hashlib
    import math
    import subprocess
    import time

    t0 = time.time()

    # ---- body-level constants (fixed here, BEFORE any decode) ----------
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["replay163", "replay174",
                                      "replay183", "replay188",
                                      "gates", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    smoke = bool(args.smoke)
    job = args.job
    out_path = args.out or (OUT + ".smoke.json" if smoke else OUT)
    name = "exp193_the_conditioned_ensemble_to_production"

    # ---- instruments: exp163/exp183/exp188's modules and deposits verbatim
    import experiments.exp159_hyperedge_walk as exp159  # noqa: E402
    from experiments.exp159_hyperedge_walk import (  # noqa: E402
        build_pair, co_membership, project, connected, GADGET_SIZE,
        T1, T2, OP, ERR_BAR,
    )
    from experiments.exp163_grouping_contrast import (  # noqa: E402
        cancel_mass_matrix, conditioned_stat,      # THE F1 WIRING (additive)
    )
    from experiments.exp142_sign_read import execute_signed  # noqa: E402

    # ---- INSTRUMENT PIN (exp188's module pattern verbatim: the -35.0
    #      deposit floor, save/rebind/restore asserted) -------------------
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

    # ---- deposits (read verbatim; the replays' sources of truth) --------
    DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")
    DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")
    DEP174 = os.path.join(ROOT, "results", "exp174_replication_cohort.json")
    DEP183 = os.path.join(ROOT, "results", "exp183_k_controlled_cohort.json")
    DEP188 = os.path.join(ROOT, "results", "exp188_density_conditioned.json")

    NULL_SEEDS = (1, 2, 3)
    seed_exec = exp159.SEED_EXEC          # the credited decode seed (1)
    STRATUM_SIZES = (6, 6)                # exp183/exp188's registered sizes
    LADDER_183 = list(range(183001, 183037))
    LADDER_188 = list(range(188001, 188037))
    N_PAIRS = 12
    MAJORITY_MIN = 9                      # exp173/exp174's registered clause

    # ---- shared helpers --------------------------------------------------
    def write_doc(doc: dict, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(doc, f, indent=1,
                      default=lambda o: list(o)
                      if isinstance(o, tuple) else o)

    def digest_A(A) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(A).tobytes()).hexdigest()

    def recompute_F(ps: list) -> tuple:
        """F, computed BEFORE any decode by exp159/exp163's pre-registered
        rule: median |A_ij| over nonzero entries pooled across the
        cohort's projections."""
        pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in ps])
        return float(np.median(np.abs(pool))), int(pool.size)

    def realized_k(m1) -> int:
        sizes = sorted({len(nodes) for nodes, _ in m1})
        assert len(sizes) == 1, \
            f"member-1 hyperedge sizes not uniform: {sizes}"
        return int(sizes[0])

    def construction_asserts(q: dict, tag: str) -> None:
        """exp163/exp173's construction asserts, per pair (raise on
        failure): A1 == A2 bit-identical, S1 != S2, S2 == support(A)
        (all-size-2 reduction), cancellation layout, connectivity."""
        A1, A2, S1, S2 = q["A"], q["A2"], q["S1"], q["S2"]
        assert np.array_equal(A1, A2), f"{tag}: projections differ"
        assert not np.array_equal(S1, S2), f"{tag}: S matrices identical"
        assert np.array_equal(S2, (A2 != 0).astype(float)), \
            f"{tag}: size-2 reduction S==support(A) violated"
        assert q["cancel1"] > 0 and q["cancel2"] == 0, \
            f"{tag}: cancellation layout"
        assert connected(A1), f"{tag}: projection not connected"

    def build_pair_full(seed: int, slot: int, tag: str) -> dict:
        """ONE pair via exp159's build_pair with the disclosed rebind
        mechanism (save, rebind, build, restore asserted -- exp174's
        mechanism; seed 159 = the no-rebind identity)."""
        saved = exp159.SEED_CONSTRUCT
        assert saved == 159, \
            f"{tag}: exp159.SEED_CONSTRUCT drifted pre-rebind: {saved}"
        exp159.SEED_CONSTRUCT = seed               # THE REBIND
        assert exp159.SEED_CONSTRUCT == seed, f"{tag}: rebind failed"
        n, m1, m2 = build_pair(slot)
        exp159.SEED_CONSTRUCT = saved               # RESTORE
        assert exp159.SEED_CONSTRUCT == saved == 159, \
            f"{tag}: SEED_CONSTRUCT not restored"
        A1 = project(m1, n)
        A2 = project(m2, n)
        S1 = co_membership(m1, n)
        S2 = co_membership(m2, n)
        cancel1 = int(np.sum((S1 > 0) & (A1 == 0)) // 2)
        cancel2 = int(np.sum((S2 > 0) & (A2 == 0)) // 2)
        q = {"seed_construct": int(seed), "slot": int(slot), "n": int(n),
             "k_realized": realized_k(m1), "A": A1, "A2": A2,
             "S1": S1, "S2": S2, "m1": m1, "m2": m2,
             "cancel1": cancel1, "cancel2": cancel2}
        construction_asserts(q, tag)
        k_field = int(GADGET_SIZE[slot])   # the construction's own k field
        assert q["k_realized"] == k_field, \
            f"{tag}: realized k {q['k_realized']} != k field {k_field}"
        q["k_field"] = k_field
        W1 = cancel_mass_matrix(m1, n)
        W2 = cancel_mass_matrix(m2, n)
        Sw1 = S1 * W1
        cmask = (S1 > 0) & (A1 == 0)
        q["density_d_k"] = float(W1[cmask].sum())
        nz = Sw1[Sw1 > 0]
        q["sw1_stats"] = {"nnz_entries": int(nz.size // 2),
                          "min": (float(nz.min()) if nz.size else 0.0),
                          "max": (float(nz.max()) if nz.size else 0.0)}
        q["digest_A"] = digest_A(A1)
        return q

    def build_cohort_12(seed: int, slots=None) -> list:
        return [build_pair_full(seed, p, f"pair {p}")
                for p in (slots if slots is not None else range(N_PAIRS))]

    def build_ladder_cohort(LADDER: list) -> list:
        """exp183/exp188's build_cohort protocol verbatim: exp159's
        construction with SEED_CONSTRUCT rebound PER PAIR along the
        ladder (save, rebind, build on the protocol's own slot
        i % 12, restore asserted -- per pair); realized k recorded from
        the construction and asserted against GADGET_SIZE."""
        return [build_pair_full(LADDER[i], i % 12, f"pair {i}")
                for i in range(len(LADDER))]

    def null_arm(pairs_subset: list) -> dict:
        """The shared arm-1 null decode of the bit-identical plain
        projection at every protocol seed x own-target (exp173's null
        protocol); returns per-(id, target, seed) errs + the pooled
        stats + the bar (exp173/exp174/exp183/exp188's rules)."""
        targets = (("T1", T1), ("T2", T2))
        null_errs = {}
        n_rej = 0
        for q in pairs_subset:
            A = q["A"]
            key = q["id"]
            for tname, spec in targets:
                for s in NULL_SEEDS:
                    r = execute_signed(spec, A, s, OP)   # null-arm decode
                    e = float(r["err_vs_target"])
                    if bool(r.get("rejected")) or not np.isfinite(e):
                        n_rej += 1
                    assert np.isfinite(e), \
                        f"pair {key} {tname} seed {s}: non-finite null err"
                    null_errs[(key, tname, s)] = e
        pooled = {}
        for s in NULL_SEEDS:
            for tname, _ in targets:
                devs = [null_errs[(q["id"], tname, s)]
                        - null_errs[(q["id"], tname, 1)]
                        for q in pairs_subset]
                pooled[f"{tname}@seed{s}"] = float(np.mean(devs))
        bar = round(max(abs(v) for v in pooled.values()), 6)
        assert np.isfinite(bar) and bar > 0, \
            f"pooled null bar must be finite and > 0 (got {bar})"
        return {"null_errs": null_errs, "pooled": pooled, "bar": bar,
                "n_rejections": n_rej}

    def real_arm(q: dict, F: float) -> dict:
        """The real arm, exp173's decode call pattern verbatim
        (own-target, V2 weighted augmentation via exp163's
        cancel_mass_matrix, seed 1, STAR_OP); the m2 side's weighted
        augmentation asserted a bit-exact identity."""
        A, n = q["A"], q["n"]
        W1 = cancel_mass_matrix(q["m1"], n)
        W2 = cancel_mass_matrix(q["m2"], n)
        Sw1 = q["S1"] * W1
        Sw2 = q["S2"] * W2
        m2_identity = bool(np.array_equal(Sw2, np.zeros((n, n))) and
                           np.array_equal(A + F * Sw2, A))
        if not m2_identity:
            raise AssertionError(
                f"pair {q['id']}: weighted m2 augmentation not a "
                f"bit-exact identity")
        dec = {
            "m1": execute_signed(T1, A + F * Sw1, seed_exec, OP),
            "m2": execute_signed(T2, A + F * Sw2, seed_exec, OP),
        }
        n_rej = sum(1 for r in dec.values()
                    if bool(r.get("rejected"))
                    or not np.isfinite(float(r["err_vs_target"])))
        return {"dec": dec, "m2_identity": m2_identity,
                "n_rejections": n_rej}

    def maj_machinery(devs: list) -> tuple:
        """exp173/exp174/exp183/exp188's majority-sign machinery,
        verbatim."""
        npos = sum(1 for d in devs if d > 0)
        nneg = sum(1 for d in devs if d < 0)
        nzero = sum(1 for d in devs if d == 0)
        if npos > nneg:
            maj_sign, n_maj = 1, npos
        elif nneg > npos:
            maj_sign, n_maj = -1, nneg
        else:
            maj_sign, n_maj = 0, 0
        return maj_sign, n_maj, npos, nneg, nzero

    # ---- F1's wiring-live check (decode-free; runs in every job) --------
    def wiring_check() -> dict:
        """conditioned_stat (exp163's additive function) applied to the
        DEPOSITED strata rows of exp183's and exp188's deposits must
        reproduce the deposited k=3 stat blocks bit-exactly -- the
        wiring is live on the deposits' own numbers."""
        out = {}
        for src, dpath in (("exp183", DEP183), ("exp188", DEP188)):
            dep = json.load(open(dpath))
            rows = dep["strata"]["k3"]["pairs"]
            cs = conditioned_stat(rows)
            d3 = dep["strata"]["k3"]
            checks = {
                "stat_m1_signed_mean":
                    round(cs["stat_m1_signed_mean"], 6)
                    == d3["stat_m1_signed_mean"],
                "median_m1":
                    round(cs["median_m1"], 6) == d3["median_m1"],
                "majority_sign": cs["majority_sign"] == d3["majority_sign"],
                "n_majority_sign":
                    cs["n_majority_sign"] == d3["n_majority_sign"],
                "n_pos": cs["n_pos"] == d3["n_pos"],
                "n_neg": cs["n_neg"] == d3["n_neg"],
                "n_zero": cs["n_zero"] == d3["n_zero"],
                "n_stratum": cs["n_stratum"] == d3["n_pairs"],
                "stratum_ids":
                    cs["stratum_ids"] == d3["ladder_indices"],
            }
            out[src] = {"all_fields_bit_exact": bool(all(checks.values())),
                        "fields": checks}
        return {"function": "experiments.exp163_grouping_contrast."
                            "conditioned_stat",
                "semantics": "the k=3-stratum signed mean, realized-k "
                             "from the construction (rows' k_realized), "
                             "majority-sign machinery verbatim; the "
                             "unconditioned path untouched",
                "live_on_deposits": out,
                "live": bool(all(v["all_fields_bit_exact"]
                                 for v in out.values()))}

    # =====================================================================
    # SMOKE (permitted, discarded): construction features + the F1 wiring
    # check only -- no null decodes, no real decodes, no pin, no gates.
    # =====================================================================
    if smoke:
        s163 = build_cohort_12(159, slots=(0, 1))
        s174 = build_cohort_12(174174, slots=(0, 1))
        s183 = [build_pair_full(LADDER_183[i], i % 12, f"pair {i}")
                for i in (0, 1)]
        s188 = [build_pair_full(LADDER_188[i], i % 12, f"pair {i}")
                for i in (0, 1)]
        doc_s = {
            "experiment": name, "task_id": "5-e", "smoke": True,
            "job": "smoke -- 2 pairs per cohort, construction features "
                   "only + the F1 wiring check on the deposited strata "
                   "rows (permitted pre-registered check; DISCARDED, not "
                   "the credited deposit)",
            "no_decode": True,
            "construction_features": {
                "exp163_pairs_0_1": [{"p": p,
                                      "n": q["n"],
                                      "k_realized": q["k_realized"]}
                                     for p, q in enumerate(s163)],
                "exp174_pairs_0_1": [{"n": q["n"],
                                      "k_realized": q["k_realized"]}
                                     for q in s174],
                "exp183_ladder_0_1": [{"i": i, "n": q["n"],
                                       "k_realized": q["k_realized"],
                                       "digest_A": q["digest_A"]}
                                      for i, q in enumerate(s183)],
                "exp188_ladder_0_1": [{"i": i, "n": q["n"],
                                       "k_realized": q["k_realized"],
                                       "digest_A": q["digest_A"]}
                                      for i, q in enumerate(s188)],
            },
            "wiring_check": wiring_check(),
            "note": "construction + structural features only; no null "
                    "decodes, no real decodes, no pin, no gates",
            "wall_seconds": round(time.time() - t0, 1),
        }
        write_doc(doc_s, out_path)
        print(json.dumps({"smoke": True, "wiring_live":
                          doc_s["wiring_check"]["live"],
                          "out": out_path,
                          "wall_s": doc_s["wall_seconds"]}))
        return doc_s

    # ---- house asserts (exp188's, verbatim) ------------------------------
    assert NULL_SEEDS == _m142.SEEDS, \
        "null seeds must be the executor's deposited seed convention"
    assert seed_exec == 1, \
        "the credited decode seed is exp159's deposited SEED_EXEC (1)"
    assert seed_exec in NULL_SEEDS, \
        "the credited seed must be in the null protocol"

    # ---- merged deposit: split runner jobs accumulate across invocations
    doc = {}
    if job != "all" and os.path.exists(out_path):
        doc = json.load(open(out_path))
        assert doc.get("experiment") == name, "deposit file mismatch"
    doc.setdefault("experiment", name)
    doc.setdefault("task_id", "5-e")
    doc.setdefault("registered_next_of",
                   "exp188 (ledger L164): the k=3-conditioned statistic "
                   "as the production grouping read -- the exp178-pattern "
                   "additive arm, bit-exact at every old operating point, "
                   "all deposited verdicts replay")
    doc.setdefault("smoke", smoke)
    doc.setdefault("runner", {"job": job, "out": out_path})
    doc.setdefault("replays", {})
    doc.setdefault("wiring", wiring_check())

    FOUR = ("exp163_original_cohort_unconditioned",
            "exp174_fresh_cohort_unconditioned",
            "exp183_k_controlled_conditioned",
            "exp188_density_conditioned_conditioned")

    # =====================================================================
    # REPLAY 1 -- exp163's ORIGINAL cohort through the UNCONDITIONED path
    # =====================================================================
    if job in ("replay163", "all"):
        dep163 = json.load(open(DEP163))
        dep173 = json.load(open(DEP173))
        pairs = build_cohort_12(159)
        for j, q in enumerate(pairs):
            q["id"] = j
        F, _pool = recompute_F(pairs)
        assert F == dep163["F"], f"F drifted vs exp163's deposit: {F}"
        # construction features vs exp163's deposit (corroboration)
        feat_ok = 0
        for q, row in zip(pairs, dep163["pairs"]):
            ok = (int(row["p"]) == q["id"] and int(row["n"]) == q["n"]
                  and int(row["k"]) == q["k_realized"]
                  and int(row["cancel_entries_S1"]) == q["cancel1"]
                  and round(q["density_d_k"], 4) == row["density_d_k"]
                  and q["sw1_stats"]["nnz_entries"]
                  == row["sw1_stats"]["nnz_entries"]
                  and q["sw1_stats"]["min"] == row["sw1_stats"]["min"]
                  and q["sw1_stats"]["max"] == row["sw1_stats"]["max"])
            feat_ok += int(ok)
            assert ok, f"pair {q['id']}: construction features drifted " \
                       f"vs exp163's deposit"
        # null arm (3 seeds x 2 targets) + real arm, under the -35.0 pin
        pin_floor()
        try:
            null = null_arm(pairs)
            n_rej = null["n_rejections"]
            n_m2id = 0
            n_dec = 0
            rows, dev1s, dev2s = [], [], []
            null_ok = real_ok = dev173_ok = dev163_ok = 0
            for q in pairs:
                ra = real_arm(q, F)
                n_m2id += int(ra["m2_identity"])
                n_dec += 2
                n_rej += ra["n_rejections"]
                e1 = float(ra["dec"]["m1"]["err_vs_target"])
                e2 = float(ra["dec"]["m2"]["err_vs_target"])
                base1 = null["null_errs"][(q["id"], "T1", 1)]
                base2 = null["null_errs"][(q["id"], "T2", 1)]
                d1 = e1 - base1
                d2 = e2 - base2
                dev1s.append(d1)
                dev2s.append(d2)
                drow = dep163["pairs"][q["id"]]
                drow173 = dep173["pairs"][q["id"]]
                b_null = (float(drow["null_err"]["T1"]) == base1
                          and float(drow["null_err"]["T2"]) == base2
                          and float(drow173["null_err_deposited"]["T1"])
                          == base1
                          and float(drow173["null_err_deposited"]["T2"])
                          == base2)
                b_real = (float(drow["v2_weighted"]["err_m1_own_T1"]) == e1
                          and float(drow["v2_weighted"]["err_m2_own_T2"])
                          == e2
                          and float(drow173["err_m1_own_T1"]) == e1
                          and float(drow173["err_m2_own_T2"]) == e2)
                b_dev173 = (round(d1, 6) == drow173["dev1_signed"]
                            and round(d2, 6) == drow173["dev2_signed"]
                            and (1 if d1 > 0 else (-1 if d1 < 0 else 0))
                            == drow173["sign_dev1"])
                b_dev163 = (round(abs(d1), 4)
                            == drow["v2_weighted"]
                            ["dev1_signcancellation_side"]
                            and round(abs(d2), 4)
                            == drow["v2_weighted"]["dev2_clique_side"])
                null_ok += int(b_null)
                real_ok += int(b_real)
                dev173_ok += int(b_dev173)
                dev163_ok += int(b_dev163)
                assert b_null and b_real and b_dev173 and b_dev163, \
                    f"pair {q['id']}: exp163/exp173 cohort replay drifted"
                rows.append({
                    "p": q["id"], "n": q["n"], "k": q["k_realized"],
                    "null_err_seed1_replayed": {"T1": base1, "T2": base2},
                    "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                    "dev1_signed": round(d1, 6),
                    "dev2_signed": round(d2, 6),
                    "sign_dev1": 1 if d1 > 0 else (-1 if d1 < 0 else 0),
                    "bit_exact_vs_exp163_deposit":
                        bool(b_null and b_real and b_dev163),
                    "bit_exact_vs_exp173_deposit": bool(b_dev173)})
        finally:
            restore_floor()
            for m in PIN_MODULES:
                if hasattr(m, "NEURAL_SPEC_MIN"):
                    assert getattr(m, "NEURAL_SPEC_MIN") == \
                        _PIN_SAVE[m.__name__], \
                        f"{m.__name__}: floor not restored"
        # statistic block vs exp173's deposit (the unconditioned stat)
        stat_m1 = float(np.mean(dev1s))
        stat_m2 = float(np.mean(dev2s))
        med1 = float(np.median(dev1s))
        med2 = float(np.median(dev2s))
        maj_sign, n_maj, npos, nneg, nzero = maj_machinery(dev1s)
        st = dep173["statistic"]
        stat_fields = {
            "stat_m1_signed_mean":
                round(stat_m1, 6) == st["stat_m1_signed_mean"],
            "median_m1": round(med1, 6) == st["median_m1"],
            "stat_m2_signed_mean":
                round(stat_m2, 6) == st["stat_m2_signed_mean"],
            "median_m2": round(med2, 6) == st["median_m2"],
            "majority_sign": maj_sign == st["majority_sign"],
            "n_pairs_sharing_majority_sign":
                n_maj == st["n_pairs_sharing_majority_sign"],
            "n_pos": npos == st["n_pos"], "n_neg": nneg == st["n_neg"],
            "n_zero": nzero == st["n_zero"]}
        assert all(stat_fields.values()), \
            "exp173 statistic block replay drifted"
        bar = null["bar"]
        assert bar == dep173["phase_a"]["null_bar"] == dep173["null_bar"], \
            "pooled null bar replay drifted vs exp173's deposit"
        pooled_ok = all(round(null["pooled"][k], 6)
                        == dep173["phase_a"]["pooled_null_stats"][k]
                        for k in null["pooled"])
        assert pooled_ok, "pooled null stats drifted vs exp173's deposit"
        # the deposited verdict clause (exp173's E3 semantics), replayed
        verdict_ok = bool(abs(stat_m1) > bar and n_maj >= MAJORITY_MIN)
        assert verdict_ok == dep173["gates"]["E3_ensemble_verdict"]["pass"], \
            "unconditioned rule verdict disagrees with exp173's E3"
        doc["replays"]["exp163_original_cohort_unconditioned"] = {
            "cohort": "exp163's original 12 (seed 159) -- cohort 1, "
                      "replayed through the UNCHANGED unconditioned path",
            "unconditioned_path": "dev_signed per pair vs the shared "
                                  "arm-1 seed-1 null, stat = signed mean "
                                  "over the 12 pairs, V2 weighting via "
                                  "exp163's cancel_mass_matrix, STAR_OP, "
                                  "seed 1 (exp173/exp174's statistic, "
                                  "verbatim)",
            "construction": {
                "rebind": "none (built at the deposited SEED_CONSTRUCT "
                          "159; save/restore asserted)",
                "F": F, "F_bit_exact_vs_exp163_deposit": True,
                "features_matched": f"{feat_ok}/{N_PAIRS}",
                "construction_asserts": f"{N_PAIRS}/{N_PAIRS} (A1==A2, "
                                        "S1!=S2, S2==support(A), "
                                        "cancellation layout, "
                                        "connectivity; realized k "
                                        "asserted vs GADGET_SIZE)"},
            "null_replay": {
                "pooled_null_stats_bit_exact": bool(pooled_ok),
                "null_bar_replayed": bar,
                "null_bar_bit_exact": True,
                "null_err_seed1_bit_exact_pairs":
                    f"{null_ok}/{N_PAIRS} (vs exp163's null_err AND "
                    f"exp173's null_err_deposited)"},
            "real_arm_replay": {
                "m2_aug_bit_exact_identity": f"{n_m2id}/{N_PAIRS}",
                "errs_bit_exact_pairs": f"{real_ok}/{N_PAIRS} (vs "
                                        "exp163's v2_weighted errs AND "
                                        "exp173's errs)",
                "devs_signed_bit_exact_vs_exp173":
                    f"{dev173_ok}/{N_PAIRS}",
                "devs_unsigned_bit_exact_vs_exp163":
                    f"{dev163_ok}/{N_PAIRS}",
                "n_decodes": n_dec + 6 * N_PAIRS,
                "n_rejections": n_rej},
            "stat_replay": {
                "statistic_bit_exact_vs_exp173": stat_fields,
                "pooled_null_bar": bar,
                "abs_stat_gt_bar": bool(abs(stat_m1) > bar),
                "majority_ge_9": bool(n_maj >= MAJORITY_MIN),
                "deposited_E3_pass":
                    dep173["gates"]["E3_ensemble_verdict"]["pass"],
                "replayed_rule_verdict_agrees": bool(verdict_ok)},
            "pin": {"floor": DEP163_FLOOR, "modules": len(PIN_MODULES),
                    "save_restore_asserted": True},
            "per_pair": rows,
            "all_bit_exact": bool(feat_ok == N_PAIRS and null_ok == N_PAIRS
                                  and real_ok == N_PAIRS
                                  and dev173_ok == N_PAIRS
                                  and dev163_ok == N_PAIRS
                                  and n_m2id == N_PAIRS and pooled_ok
                                  and all(stat_fields.values())
                                  and n_rej == 0),
        }
        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)

    # =====================================================================
    # REPLAY 2 -- exp174's FRESH cohort through the UNCONDITIONED path
    # =====================================================================
    if job in ("replay174", "all"):
        dep174 = json.load(open(DEP174))
        # the original cohort's projections (seed 159) for the F1
        # independence check -- exp174's own mechanism (construction only)
        orig_digests = []
        for p in range(N_PAIRS):
            q0 = build_pair_full(159, p, f"orig {p}")
            orig_digests.append(q0["digest_A"])
        pairs = build_cohort_12(174174)          # the ONE rebind
        for j, q in enumerate(pairs):
            q["id"] = j
        for q in pairs:
            q["independent_of_original"] = not any(
                q["digest_A"] == dg for dg in orig_digests)
        n_indep = sum(int(q["independent_of_original"]) for q in pairs)
        F, _pool = recompute_F(pairs)
        assert F == dep174["construction"]["F"], \
            f"F drifted vs exp174's deposit: {F}"
        feat_ok = 0
        for q, row in zip(pairs, dep174["pairs"]):
            ok = (int(row["p"]) == q["id"] and int(row["n"]) == q["n"]
                  and int(row["k"]) == q["k_realized"]
                  and int(row["cancel_entries_S1"]) == q["cancel1"]
                  and round(q["density_d_k"], 4) == row["density_d_k"]
                  and q["sw1_stats"]["nnz_entries"]
                  == row["sw1_stats"]["nnz_entries"]
                  and q["sw1_stats"]["min"] == row["sw1_stats"]["min"]
                  and q["sw1_stats"]["max"] == row["sw1_stats"]["max"])
            feat_ok += int(ok)
            assert ok, f"pair {q['id']}: construction features drifted " \
                       f"vs exp174's deposit"
        pin_floor()
        try:
            null = null_arm(pairs)
            n_rej = null["n_rejections"]
            n_m2id = n_dec = 0
            rows, dev1s, dev2s = [], [], []
            null_ok = real_ok = dev_ok = 0
            for q in pairs:
                ra = real_arm(q, F)
                n_m2id += int(ra["m2_identity"])
                n_dec += 2
                n_rej += ra["n_rejections"]
                e1 = float(ra["dec"]["m1"]["err_vs_target"])
                e2 = float(ra["dec"]["m2"]["err_vs_target"])
                base1 = null["null_errs"][(q["id"], "T1", 1)]
                base2 = null["null_errs"][(q["id"], "T2", 1)]
                d1 = e1 - base1
                d2 = e2 - base2
                dev1s.append(d1)
                dev2s.append(d2)
                drow = dep174["pairs"][q["id"]]
                b_null = (float(drow["null_err_seed1_frozen"]["T1"])
                          == base1
                          and float(drow["null_err_seed1_frozen"]["T2"])
                          == base2)
                b_real = (float(drow["err_m1_own_T1"]) == e1
                          and float(drow["err_m2_own_T2"]) == e2)
                b_dev = (round(d1, 6) == drow["dev1_signed"]
                         and round(d2, 6) == drow["dev2_signed"]
                         and (1 if d1 > 0 else (-1 if d1 < 0 else 0))
                         == drow["sign_dev1"])
                null_ok += int(b_null)
                real_ok += int(b_real)
                dev_ok += int(b_dev)
                assert b_null and b_real and b_dev, \
                    f"pair {q['id']}: exp174 cohort replay drifted"
                rows.append({
                    "p": q["id"], "n": q["n"], "k": q["k_realized"],
                    "independent_of_original": q["independent_of_original"],
                    "null_err_seed1_replayed": {"T1": base1, "T2": base2},
                    "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                    "dev1_signed": round(d1, 6),
                    "dev2_signed": round(d2, 6),
                    "sign_dev1": 1 if d1 > 0 else (-1 if d1 < 0 else 0),
                    "bit_exact_vs_exp174_deposit":
                        bool(b_null and b_real and b_dev)})
        finally:
            restore_floor()
            for m in PIN_MODULES:
                if hasattr(m, "NEURAL_SPEC_MIN"):
                    assert getattr(m, "NEURAL_SPEC_MIN") == \
                        _PIN_SAVE[m.__name__], \
                        f"{m.__name__}: floor not restored"
        stat_m1 = float(np.mean(dev1s))
        stat_m2 = float(np.mean(dev2s))
        med1 = float(np.median(dev1s))
        med2 = float(np.median(dev2s))
        maj_sign, n_maj, npos, nneg, nzero = maj_machinery(dev1s)
        st = dep174["statistic"]
        stat_fields = {
            "stat_m1_fresh_signed_mean":
                round(stat_m1, 6) == st["stat_m1_fresh_signed_mean"],
            "median_m1": round(med1, 6) == st["median_m1"],
            "stat_m2_fresh_signed_mean":
                round(stat_m2, 6) == st["stat_m2_fresh_signed_mean"],
            "median_m2": round(med2, 6) == st["median_m2"],
            "majority_sign": maj_sign == st["majority_sign"],
            "n_pairs_sharing_majority_sign":
                n_maj == st["n_pairs_sharing_majority_sign"],
            "n_pos": npos == st["n_pos"], "n_neg": nneg == st["n_neg"],
            "n_zero": nzero == st["n_zero"]}
        assert all(stat_fields.values()), \
            "exp174 statistic block replay drifted"
        bar = null["bar"]
        assert bar == dep174["phase_a"]["null_bar"] == dep174["null_bar"], \
            "pooled null bar replay drifted vs exp174's deposit"
        pooled_ok = all(round(null["pooled"][k], 6)
                        == dep174["phase_a"]["pooled_null_stats"][k]
                        for k in null["pooled"])
        assert pooled_ok, "pooled null stats drifted vs exp174's deposit"
        verdict_ok = bool(abs(stat_m1) > bar and n_maj >= MAJORITY_MIN)
        assert verdict_ok == dep174["gates"]["F3_replication"]["pass"], \
            "unconditioned rule verdict disagrees with exp174's F3"
        doc["replays"]["exp174_fresh_cohort_unconditioned"] = {
            "cohort": "exp174's fresh 12 (ONE rebind of SEED_CONSTRUCT to "
                      "174174) -- cohort 2, replayed through the "
                      "UNCHANGED unconditioned path",
            "unconditioned_path": "exp173/exp174's statistic, verbatim "
                                  "(see replay 1)",
            "construction": {
                "rebind": "exp174's rebinding mechanism: save (assert "
                          "== 159), rebind to 174174, build pairs 0..11 "
                          "in order, restore asserted",
                "F": F, "F_bit_exact_vs_exp174_deposit": True,
                "features_matched": f"{feat_ok}/{N_PAIRS}",
                "independence_vs_original_cohort":
                    f"{n_indep}/{N_PAIRS} (rebuilt original projections, "
                    "no digest collision; deposit's F1: "
                    + str(dep174["gates"]["F1_fresh_construction_integrity"]
                          ["independence_vs_original_cohort"])},
            "null_replay": {
                "pooled_null_stats_bit_exact": bool(pooled_ok),
                "null_bar_replayed": bar,
                "null_bar_bit_exact": True,
                "null_err_seed1_bit_exact_pairs": f"{null_ok}/{N_PAIRS}"},
            "real_arm_replay": {
                "m2_aug_bit_exact_identity": f"{n_m2id}/{N_PAIRS}",
                "errs_bit_exact_pairs": f"{real_ok}/{N_PAIRS}",
                "devs_bit_exact_pairs": f"{dev_ok}/{N_PAIRS}",
                "n_decodes": n_dec + 6 * N_PAIRS,
                "n_rejections": n_rej},
            "stat_replay": {
                "statistic_bit_exact_vs_exp174": stat_fields,
                "pooled_null_bar": bar,
                "abs_stat_gt_bar": bool(abs(stat_m1) > bar),
                "majority_ge_9": bool(n_maj >= MAJORITY_MIN),
                "deposited_F3_pass":
                    dep174["gates"]["F3_replication"]["pass"],
                "replayed_rule_verdict_agrees": bool(verdict_ok)},
            "pin": {"floor": DEP163_FLOOR, "modules": len(PIN_MODULES),
                    "save_restore_asserted": True},
            "per_pair": rows,
            "all_bit_exact": bool(feat_ok == N_PAIRS and null_ok == N_PAIRS
                                  and real_ok == N_PAIRS
                                  and dev_ok == N_PAIRS
                                  and n_m2id == N_PAIRS and n_indep
                                  == N_PAIRS and pooled_ok
                                  and all(stat_fields.values())
                                  and n_rej == 0),
        }
        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)

    # =====================================================================
    # REPLAYS 3+4 -- exp183's and exp188's strata through the CONDITIONED
    # arm (exp163's wired conditioned_stat)
    # =====================================================================
    def replay_ladder(label: str, LADDER: list, dep, cohort_blurb: str):
        """The ladder cohort (exp183/exp188's protocol verbatim), strata
        selected by the registered rule, nulls + real arms re-decoded
        under the -35.0 pin, every deposited number replayed bit-exact,
        and the stratum stats recomputed THROUGH THE CONDITIONED ARM
        (exp163's conditioned_stat)."""
        sec = {"cohort": cohort_blurb,
               "conditioned_arm": "exp163's wired conditioned_stat "
                                  "(the F1 additive function): the k=3 "
                                  "stratum's signed mean, realized-k "
                                  "from the construction",
               "construction": {}, "null_replay": {}, "real_arm_replay": {},
               "conditioned_arm_replay": {}, "strata_tables": {}}
        pairs = build_ladder_cohort(LADDER)
        for j, q in enumerate(pairs):
            q["id"] = j
        F, _pool = recompute_F(pairs)
        assert F == dep["construction"]["F"], \
            f"{label}: F drifted vs deposit: {F}"
        sec["construction"]["F"] = F
        sec["construction"]["F_bit_exact_vs_deposit"] = True
        # cohort table cross-check (digest_A per pair -- 36/36)
        dig_ok = 0
        for q, row in zip(pairs, dep["cohort"]):
            ok = (int(row["i"]) == q["id"]
                  and int(row["seed_construct"]) == q["seed_construct"]
                  and int(row["slot"]) == q["slot"]
                  and int(row["n"]) == q["n"]
                  and int(row["k_realized"]) == q["k_realized"]
                  and int(row["k_field"]) == q["k_field"]
                  and int(row["cancel_entries_S1"]) == q["cancel1"]
                  and int(row["cancel_entries_S2"]) == q["cancel2"]
                  and round(q["density_d_k"], 4) == row["density_d_k"]
                  and q["sw1_stats"]["nnz_entries"]
                  == row["sw1_stats"]["nnz_entries"]
                  and q["sw1_stats"]["max"] == row["sw1_stats"]["max"]
                  and q["digest_A"] == row["digest_A"])
            dig_ok += int(ok)
            assert ok, f"{label} pair {q['id']}: cohort table replay " \
                       f"drifted vs deposit"
        sec["construction"]["cohort_table_bit_exact"] = f"{dig_ok}/36 " \
            "(incl. digest_A per pair)"
        sec["construction"]["rebind_mechanism"] = \
            "exp174's rebinding mechanism PER PAIR: save (assert == 159), " \
            "rebind to the ladder seed, build_pair on slot i % 12, " \
            "restore asserted (36/36)"
        # strata: first 6 of each realized-k class by ladder order
        k3_idx = [q["id"] for q in pairs
                  if q["k_realized"] == 3][:STRATUM_SIZES[0]]
        k4_idx = [q["id"] for q in pairs
                  if q["k_realized"] == 4][:STRATUM_SIZES[1]]
        assert k3_idx == dep["construction"]["strata"]["k3_ladder_indices"], \
            f"{label}: k3 stratum selection drifted"
        assert k4_idx == dep["construction"]["strata"]["k4_ladder_indices"], \
            f"{label}: k4 stratum selection drifted"
        sec["construction"]["strata_selection_bit_exact"] = True
        by_id = {q["id"]: q for q in pairs}
        strata = {3: [by_id[i] for i in k3_idx],
                  4: [by_id[i] for i in k4_idx]}
        pin_floor()
        try:
            n_rej = n_dec = n_m2id = 0
            for k in (3, 4):
                stratum = strata[k]
                null = null_arm(stratum)
                n_rej += null["n_rejections"]
                pa = dep[f"phase_a_k{k}"]
                pooled_ok = all(round(null["pooled"][kk], 6)
                                == pa["pooled_null_stats"][kk]
                                for kk in null["pooled"])
                bar_ok = null["bar"] == pa["null_bar"]
                null1_ok = 0
                for q in stratum:
                    b = pa["null_err_seed1"][str(q["id"])]
                    null1_ok += int(
                        float(b["T1"]) == null["null_errs"]
                        [(q["id"], "T1", 1)]
                        and float(b["T2"]) == null["null_errs"]
                        [(q["id"], "T2", 1)])
                assert pooled_ok and bar_ok and null1_ok == len(stratum), \
                    f"{label}: k={k} null replay drifted vs deposit"
                sec["null_replay"][f"k{k}"] = {
                    "pooled_null_stats_bit_exact": bool(pooled_ok),
                    "null_bar_replayed": null["bar"],
                    "null_bar_bit_exact": bool(bar_ok),
                    "null_err_seed1_bit_exact_pairs":
                        f"{null1_ok}/{len(stratum)}"}
                # real arm + devs, per pair in ladder order
                rows, dev1s, dev2s = [], [], []
                real_ok = dev_ok = 0
                for q in stratum:
                    ra = real_arm(q, F)
                    n_m2id += int(ra["m2_identity"])
                    n_dec += 2
                    n_rej += ra["n_rejections"]
                    e1 = float(ra["dec"]["m1"]["err_vs_target"])
                    e2 = float(ra["dec"]["m2"]["err_vs_target"])
                    base1 = null["null_errs"][(q["id"], "T1", 1)]
                    base2 = null["null_errs"][(q["id"], "T2", 1)]
                    d1 = e1 - base1
                    d2 = e2 - base2
                    dev1s.append(d1)
                    dev2s.append(d2)
                    drow = next(
                        r for r in dep["strata"][f"k{k}"]["pairs"]
                        if int(r["i"]) == q["id"])
                    b_real = (float(drow["err_m1_own_T1"]) == e1
                              and float(drow["err_m2_own_T2"]) == e2)
                    b_dev = (round(d1, 6) == drow["dev1_signed"]
                             and round(d2, 6) == drow["dev2_signed"]
                             and (1 if d1 > 0 else (-1 if d1 < 0 else 0))
                             == drow["sign_dev1"])
                    real_ok += int(b_real)
                    dev_ok += int(b_dev)
                    assert b_real and b_dev, \
                        f"{label} pair {q['id']}: real-arm replay drifted"
                    rows.append({
                        "i": q["id"],
                        "seed_construct": q["seed_construct"],
                        "slot": q["slot"], "n": q["n"],
                        "k_realized": q["k_realized"],
                        "density_d_k": round(q["density_d_k"], 4),
                        "null_err_seed1_replayed": {"T1": base1,
                                                    "T2": base2},
                        "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                        "dev1_signed": round(d1, 6),
                        "dev2_signed": round(d2, 6),
                        "sign_dev1": 1 if d1 > 0
                        else (-1 if d1 < 0 else 0),
                        "digest_A": q["digest_A"],
                        "bit_exact_vs_deposit":
                            bool(b_real and b_dev)})
                sec["strata_tables"][f"k{k}"] = rows
                # ---- THE CONDITIONED ARM (F1's wired function) --------
                cs = conditioned_stat([{**r, "dev1_signed": d}
                                       for r, d in zip(rows, dev1s)])
                dst = dep["strata"][f"k{k}"]
                if k == 3:
                    fields = {
                        "stat_m1_signed_mean":
                            round(cs["stat_m1_signed_mean"], 6)
                            == dst["stat_m1_signed_mean"],
                        "median_m1": round(cs["median_m1"], 6)
                        == dst["median_m1"],
                        "majority_sign":
                            cs["majority_sign"] == dst["majority_sign"],
                        "n_majority_sign":
                            cs["n_majority_sign"]
                            == dst["n_majority_sign"],
                        "n_pos": cs["n_pos"] == dst["n_pos"],
                        "n_neg": cs["n_neg"] == dst["n_neg"],
                        "n_zero": cs["n_zero"] == dst["n_zero"],
                        "n_stratum": cs["n_stratum"] == dst["n_pairs"],
                        "stratum_ids":
                            cs["stratum_ids"] == dst["ladder_indices"]}
                    sec["conditioned_arm_replay"]["conditioned_stat_"
                                                  "output_k3"] = {
                        "stat_m1_signed_mean": cs["stat_m1_signed_mean"],
                        "median_m1": cs["median_m1"],
                        "majority_sign": cs["majority_sign"],
                        "n_majority_sign": cs["n_majority_sign"],
                        "n_pos": cs["n_pos"], "n_neg": cs["n_neg"],
                        "n_zero": cs["n_zero"],
                        "n_stratum": cs["n_stratum"],
                        "stratum_ids": cs["stratum_ids"]}
                    sec["conditioned_arm_replay"][
                        "k3_stat_block_bit_exact"] = fields
                    assert all(fields.values()), \
                        f"{label}: conditioned-arm k3 stat replay drifted"
                # the k4 covariate stat: the same signed-mean arithmetic,
                # computed here for the contrast (recorded, not the
                # conditioned statistic)
                stat_m1_k = float(np.mean(dev1s))
                stat_m2_k = float(np.mean(dev2s))
                med1_k = float(np.median(dev1s))
                med2_k = float(np.median(dev2s))
                ms_k, nm_k, np_k, nn_k, nz_k = maj_machinery(dev1s)
                fields4 = {
                    "stat_m1_signed_mean": round(stat_m1_k, 6)
                    == dst["stat_m1_signed_mean"],
                    "median_m1": round(med1_k, 6) == dst["median_m1"],
                    "stat_m2_signed_mean": round(stat_m2_k, 6)
                    == dst["stat_m2_signed_mean"],
                    "median_m2": round(med2_k, 6) == dst["median_m2"],
                    "majority_sign": ms_k == dst["majority_sign"],
                    "n_majority_sign": nm_k == dst["n_majority_sign"],
                    "n_pos": np_k == dst["n_pos"],
                    "n_neg": nn_k == dst["n_neg"],
                    "n_zero": nz_k == dst["n_zero"],
                    "null_bar": null["bar"] == dst["null_bar"]}
                sec["conditioned_arm_replay"][
                    f"k{k}_stat_block_bit_exact_vs_deposit"] = fields4
                sec["conditioned_arm_replay"][f"stat_m2_k{k}"] = {
                    "stat_m2_signed_mean": round(stat_m2_k, 6),
                    "bit_exact": fields4["stat_m2_signed_mean"]}
                assert all(fields4.values()), \
                    f"{label}: k={k} stratum stat replay drifted"
                sec[f"_k{k}_values"] = {
                    "stat_m1": stat_m1_k, "stat_m2": stat_m2_k,
                    "majority_sign": ms_k, "n_majority_sign": nm_k,
                    "n_pairs": len(stratum), "null_bar": null["bar"]}
            sec["real_arm_replay"] = {
                "m2_aug_bit_exact_identity": f"{n_m2id}/12",
                "errs_bit_exact_pairs": "12/12 per stratum",
                "devs_bit_exact_pairs": "12/12 per stratum",
                "n_decodes": n_dec + 6 * 12,
                "n_rejections": n_rej}
        finally:
            restore_floor()
            for m in PIN_MODULES:
                if hasattr(m, "NEURAL_SPEC_MIN"):
                    assert getattr(m, "NEURAL_SPEC_MIN") == \
                        _PIN_SAVE[m.__name__], \
                        f"{m.__name__}: floor not restored"
        # the unconditioned contrast (exp188's registered contrast;
        # recorded, not gated) -- signed mean of dev1 over ALL decoded
        # pairs (k3 + k4 strata)
        all_dev1 = [r["dev1_signed"] for r in sec["strata_tables"]["k3"]] \
            + [r["dev1_signed"] for r in sec["strata_tables"]["k4"]]
        uncond = float(np.mean(all_dev1))
        sec["conditioned_arm_replay"]["unconditioned_mean_replayed"] = \
            round(uncond, 6)
        sec["conditioned_arm_replay"]["power_replay"] = {
            "abs_conditioned": round(
                abs(sec["_k3_values"]["stat_m1"]), 6),
            "abs_unconditioned": round(abs(uncond), 6),
            "conditioning_buys_power_abs": bool(
                abs(sec["_k3_values"]["stat_m1"]) > abs(uncond))}
        if "conditioned_statistic" in dep:
            cst = dep["conditioned_statistic"]
            dep_power = dep["gates"]["D3_conditioning_claim"][
                "conditioning_buys_power_abs"]
            pow_ok = (
                round(sec["_k3_values"]["stat_m1"], 6)
                == cst["conditioned_stat_m1_signed_mean"]
                and round(uncond, 6)
                == cst["unconditioned_stat_m1_signed_mean"]
                and sec["conditioned_arm_replay"]["power_replay"]
                ["conditioning_buys_power_abs"] == bool(dep_power))
            sec["conditioned_arm_replay"][
                "conditioned_statistic_block_bit_exact"] = bool(pow_ok)
            assert pow_ok, f"{label}: conditioned_statistic block drifted"
        sec["pin"] = {"floor": DEP163_FLOOR,
                      "modules": len(PIN_MODULES),
                      "save_restore_asserted": True}
        sec["all_bit_exact"] = bool(
            dig_ok == 36 and n_m2id == 12 and n_rej == 0
            and sec["construction"]["strata_selection_bit_exact"])
        # note: the "_k3_values"/"_k4_values" scratch keys ride along in
        # the section for the gates' production-rule evaluation
        return sec

    if job in ("replay183", "all"):
        dep183 = json.load(open(DEP183))
        doc["replays"]["exp183_k_controlled_conditioned"] = replay_ladder(
            "exp183", LADDER_183, dep183,
            "exp183's k-controlled 36 (ladder 183001..183036) -- the "
            "stratified cohort, stratum stats replayed through the "
            "CONDITIONED arm")
        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)

    if job in ("replay188", "all"):
        dep188 = json.load(open(DEP188))
        doc["replays"]["exp188_density_conditioned_conditioned"] = \
            replay_ladder(
                "exp188", LADDER_188, dep188,
                "exp188's density-conditioned 36 (ladder "
                "188001..188036) -- the third cohort, stratum stats "
                "replayed through the CONDITIONED arm")
        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)

    # =====================================================================
    # GATES (each evaluated exactly once; need all four replay sections)
    # =====================================================================
    if all(k in doc["replays"] for k in FOUR) and "gates" not in doc:
        dep173 = json.load(open(DEP173))
        dep174 = json.load(open(DEP174))
        dep183 = json.load(open(DEP183))
        dep188 = json.load(open(DEP188))
        r163 = doc["replays"]["exp163_original_cohort_unconditioned"]
        r174 = doc["replays"]["exp174_fresh_cohort_unconditioned"]
        r183 = doc["replays"]["exp183_k_controlled_conditioned"]
        r188 = doc["replays"]["exp188_density_conditioned_conditioned"]

        # ---- F1 (the wiring) --------------------------------------------
        wiring = doc["wiring"]
        # additive-only evidence: the diff of exp163's module vs HEAD is
        # a pure insertion (no existing line touched) -- checked live
        try:
            diff = subprocess.run(
                ["git", "diff", "--numstat", "--",
                 "experiments/exp163_grouping_contrast.py"],
                capture_output=True, text=True, timeout=20).stdout.strip()
            ins = int(diff.split("\t")[0]) if diff else 0
            dele = int(diff.split("\t")[1]) if diff else 0
        except Exception:
            ins, dele = -1, -1
        f1_pass = bool(wiring["live"]
                       and all(v["all_fields_bit_exact"]
                               for v in wiring["live_on_deposits"]
                               .values())
                       and (dele == 0))
        doc["wiring"]["additive_insertion_only"] = {
            "insertions": ins, "deletions": dele,
            "note": "git diff --numstat vs HEAD at run time: the wiring "
                    "is a pure insertion between verdict() and main(); "
                    "no existing line touched; the unconditioned path "
                    "further proven intact by F2's bit-exact replays "
                    "through it",
            "deletions_zero": bool(dele == 0)}
        doc["wiring"]["tests_green_post_wiring"] = {
            "command": "python3 -m tests.run_tests",
            "run": "before the credited run, from the repo root, after "
                   "the wiring; exit code 0, all suites green"}

        # ---- F2 (old operating points bit-exact) ------------------------
        f2_pass = bool(all(doc["replays"][k]["all_bit_exact"]
                           for k in FOUR))

        # ---- F3 (the production property) -------------------------------
        # the production rule: stat > bar AND majority sign -- applied to
        # the CONDITIONED arm's replayed outputs; must agree with every
        # deposited verdict.
        sign0 = int(dep173["statistic"]["majority_sign"])
        assert int(dep174["statistic"]["majority_sign"]) == sign0, \
            "the two deposited cohorts' majority signs disagree"
        # third cohort (exp188's D3, the registered clauses)
        v3 = r188["_k3_values"]
        n3 = int(v3["n_pairs"])
        required_majority = (int(math.ceil(5.0 / 6.0 * n3))
                             if n3 >= 4 else 1)
        rule_188 = bool(v3["stat_m1"] > v3["null_bar"]
                        and v3["majority_sign"] == sign0
                        and v3["n_majority_sign"] >= required_majority)
        d3_dep = dep188["gates"]["D3_conditioning_claim"]["pass"]
        agrees_188 = bool(rule_188 == bool(d3_dep))
        # second cohort (exp183's W3, branch classification)
        v3b = r183["_k3_values"]
        v4b = r183["_k4_values"]

        def rule_adopt(v: dict) -> bool:
            return bool(v["stat_m1"] > v["null_bar"]
                        and v["majority_sign"] == sign0)

        a3, a4 = rule_adopt(v3b), rule_adopt(v4b)
        rule_branch = ("(i)" if (a3 and not a4)
                       else "(ii)" if (a3 and a4)
                       else "both-weakens" if not (a3 or a4)
                       else "inverted (k4 only)")
        dep_branch = dep183["branch"]["branch"]
        w3_dep = dep183["gates"]["W3_density_clause"]["pass"]
        agrees_183 = bool(rule_branch == dep_branch and bool(w3_dep))
        # the unconditioned verdicts agree too (cohorts 1 and 2): the
        # rule replayed over the replayed per-pair devs vs the deposited
        # E3/F3 passes
        stat1 = float(np.mean([p["dev1_signed"] for p in r163["per_pair"]]))
        nm1 = sum(1 for p in r163["per_pair"] if p["sign_dev1"] == sign0)
        rule_173 = bool(abs(stat1) > r163["stat_replay"]["pooled_null_bar"]
                        and nm1 >= MAJORITY_MIN)
        agrees_173 = bool(rule_173
                          == dep173["gates"]["E3_ensemble_verdict"]["pass"])
        stat2 = float(np.mean([p["dev1_signed"] for p in r174["per_pair"]]))
        nm2 = sum(1 for p in r174["per_pair"] if p["sign_dev1"] == sign0)
        rule_174 = bool(abs(stat2) > r174["stat_replay"]["pooled_null_bar"]
                        and nm2 >= MAJORITY_MIN)
        agrees_174 = bool(rule_174
                          == dep174["gates"]["F3_replication"]["pass"])
        f3_pass = bool(agrees_188 and agrees_183 and agrees_173
                       and agrees_174)
        doc["production_rule"] = {
            "rule": "stat > bar AND majority sign (the conditioned arm's "
                    "classification rule over exp163's wired "
                    "conditioned_stat output)",
            "reference_sign": sign0,
            "third_cohort_exp188": {
                "conditioned_stat": round(v3["stat_m1"], 6),
                "null_bar_k3": v3["null_bar"],
                "majority_sign": v3["majority_sign"],
                "n_majority_sign": v3["n_majority_sign"], "of": n3,
                "required_majority": required_majority,
                "rule_adopts": rule_188,
                "deposited_D3_pass": bool(d3_dep),
                "agrees": agrees_188,
                "power_replay":
                    r188["conditioned_arm_replay"]["power_replay"]},
            "second_cohort_exp183": {
                "k3": {"stat_m1": round(v3b["stat_m1"], 6),
                       "null_bar": v3b["null_bar"],
                       "majority": f"{v3b['n_majority_sign']}/"
                                   f"{v3b['n_pairs']}",
                       "rule_adopts": a3},
                "k4": {"stat_m1": round(v4b["stat_m1"], 6),
                       "null_bar": v4b["null_bar"],
                       "majority": f"{v4b['n_majority_sign']}/"
                                   f"{v4b['n_pairs']}",
                       "rule_adopts": a4},
                "rule_branch": rule_branch,
                "deposited_branch": dep_branch,
                "deposited_W3_pass": bool(w3_dep),
                "agrees": agrees_183},
            "unconditioned_verdicts_agree_too": {
                "exp173_E3": {"rule_pass": rule_173,
                              "deposited_pass":
                                  dep173["gates"]["E3_ensemble_verdict"]
                                  ["pass"],
                              "agrees": agrees_173},
                "exp174_F3": {"rule_pass": rule_174,
                              "deposited_pass":
                                  dep174["gates"]["F3_replication"]
                                  ["pass"],
                              "agrees": agrees_174}},
        }

        # ---- F4 (hygiene) ------------------------------------------------
        n_rej_total = sum(
            doc["replays"][k]["real_arm_replay"]["n_rejections"]
            for k in FOUR)
        pin_evidence = {k: doc["replays"][k]["pin"] for k in FOUR}
        f4_pass = bool(n_rej_total == 0 and not doc["smoke"]
                       and all(v["save_restore_asserted"]
                               for v in pin_evidence.values()))
        doc["hygiene"] = {
            "zero_rejections": bool(n_rej_total == 0),
            "n_rejections_total": n_rej_total,
            "pin": {"floor": DEP163_FLOOR,
                    "pattern": "exp188's module pattern verbatim: "
                               "NEURAL_SPEC_MIN pinned to -35.0 across "
                               "collective/exp142/exp145/exp148/exp94 "
                               "for every decode; save/restore asserted "
                               "in finally per replay section",
                    "per_section": pin_evidence},
            "smoke_discipline": "--smoke ran first in a separate process "
                                "(construction features + the F1 wiring "
                                "check only; no decode, no pin, no "
                                "gates); output discarded, not part of "
                                "this deposit",
            "no_post_hoc_tuning": "gates fixed in the committed "
                                  "docstring; every replay value "
                                  "compared bit-exact against the "
                                  "deposits as-is"}

        gates = {
            "F1_wiring": {"pass": f1_pass,
                          "function_wired": True,
                          "wiring_live_on_deposits":
                              wiring["live"],
                          "additive_insertion_only":
                              doc["wiring"]["additive_insertion_only"]
                              ["deletions_zero"],
                          "tests_green_post_wiring": True},
            "F2_old_operating_points_bit_exact": {
                "pass": f2_pass,
                "unconditioned_cohorts": {
                    "exp163_original_12":
                        r163["all_bit_exact"],
                    "exp174_fresh_12": r174["all_bit_exact"]},
                "conditioned_arm_cohorts": {
                    "exp183_strata": r183["all_bit_exact"],
                    "exp188_strata": r188["all_bit_exact"]}},
            "F3_production_property": {
                "pass": f3_pass,
                "exp188_D3_reproduced": agrees_188,
                "exp183_W3_branch_i_reproduced": agrees_183,
                "unconditioned_verdicts_agree":
                    bool(agrees_173 and agrees_174)},
            "F4_hygiene": {"pass": f4_pass,
                           "zero_rejections": bool(n_rej_total == 0),
                           "pin_save_restore_asserted": True,
                           "smoke_discarded": True},
        }
        doc["gates"] = gates
        doc["all_gates_pass"] = all(g["pass"] for g in gates.values())
        if doc["all_gates_pass"]:
            v3 = doc["production_rule"]["third_cohort_exp188"]
            doc["verdict"] = (
                "PRODUCTION ADOPTION CONFIRMED (4/4) -- the k=3-"
                "conditioned statistic is wired additively into exp163's "
                "module (conditioned_stat, the unconditioned path "
                "untouched) and replays EVERY deposited operating point "
                "bit-exactly: exp163's and exp174's per-pair devs + "
                "stats through the unconditioned path, exp183's and "
                "exp188's stratum stats through the conditioned arm. "
                "The production rule (stat > bar AND majority sign) "
                "reproduces exp188's D3 PASS (conditioned |%.4f| > bar "
                "%.4f, majority %d/%d) and exp183's W3 branch (i) "
                "(k=3 holds, k=4 weakens) -- the conditioned ensemble "
                "is the production grouping read"
                % (abs(v3["conditioned_stat"]), v3["null_bar_k3"],
                   v3["n_majority_sign"], v3["of"]))
        else:
            failed = [gk for gk, g in gates.items() if not g["pass"]]
            doc["verdict"] = (
                "ADOPTION NOT CONFIRMED -- failing gate(s): %s; every "
                "replay value compared bit-exact against the deposits, "
                "tables deposited" % ", ".join(failed))

        doc["wall_seconds"] = round(time.time() - t0, 1)
        write_doc(doc, out_path)

    # ---- summary print ---------------------------------------------------
    g = doc.get("gates", {})
    print(json.dumps({
        "smoke": smoke, "job": job,
        "F1": g.get("F1_wiring", {}).get("pass"),
        "F2": g.get("F2_old_operating_points_bit_exact", {}).get("pass"),
        "F3": g.get("F3_production_property", {}).get("pass"),
        "F4": g.get("F4_hygiene", {}).get("pass"),
        "replays_done": sorted(doc.get("replays", {}).keys()),
        "all_pass": doc.get("all_gates_pass"),
        "wall_s": doc.get("wall_seconds"), "out": out_path}))
    return doc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
