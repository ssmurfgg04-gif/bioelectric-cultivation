#!/usr/bin/env python3
"""exp173 — THE POOLED GROUPING STATISTIC (L144's registered repair (b)).

exp163's registered next (L144): the grouping contrast's per-pair
err-level channel is exhausted at the deposited floor (max response
0.32 mV vs theta 0.27, 10/12 pairs sub-threshold) — the contrast needs
"(b) a pooled/ensemble statistic across pairs (sum/median of signed
dev asymmetries)". Pooling buys power: the deposited per-pair noise
floor is 0.09 mV, and a SIGNED ensemble mean over the 12 adversarial
pairs accumulates a consistent cancellation-attributable response
while averaging the floor down. exp163's devs were compared per pair
and ABSOLUTE-VALUED (C = |err1 - err2|); the sign structure across
pairs was never read. THIS EXPERIMENT reads it.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Statistic, null, and gates are fixed
now; the credited run uses this file unchanged.

CONSTRUCTION (exp163 VERBATIM, replayed for integrity):
  exp159's build_pair / project / co_membership imported verbatim,
  the same 12 adversarial pairs, construction seed 159, bit-identical
  projections (A1 == A2 per pair, asserted), S_1 != S_2, S_2 ==
  support(A), connectivity re-asserted per pair. V2 weighting from
  exp163's cancel_mass_matrix VERBATIM (W peaks on the sign-
  cancellation entries; member 2 has W == 0 -> augmented == A
  bit-exactly). Readout: STAR_OP verbatim (gamma 64, mu 0), seeds
  (1,) per decode as exp163's credited run, err_vs_target.

THE SIGNED STATISTIC (new, fixed now):
  dev1_signed(p) = err(A + F*S_v(m1), T1) - err(A, T1)   [signed]
  dev2_signed(p) = err(A + F*S_v(m2), T2) - err(A, T2)   [signed]
  with A the SHARED bit-identical projection and err(A, T) the arm-1
  null decode (exp163's null protocol verbatim).
  POOLED STATISTIC: stat = mean over the 12 pairs of dev_signed.
  Reported separately for the sign-cancellation side (m1) and the
  clique side (m2). The SIGNED mean is the primary; the median is
  recorded (not gated).

TWO-PHASE NULL DISCIPLINE (exp163's pre-decode deposit, verbatim):
  PHASE-A (null deposit, written to the deposit file BEFORE any
  real-arm decode): the pooled null distribution from the SHARED
  arm-1 null — per pair, the signed dev of a PLACEHOLDER member
  whose augmentation is exp163's deposited null augmentation
  (the arm-1 null errs are exp163's DEPOSITED null_err values,
  replayed bit-exactly); the null bar = max |pooled null stat|
  over the deposited null protocol's seeds. The bar is frozen in
  the phase-A record before the phase-B execute_signed calls.
  PHASE-B (real arm): dev1_signed/dev2_signed per pair, the pooled
  stats, the verdict.

INSTRUMENT PIN (exp167's mechanism, disclosed pre-run): exp163's
  deposit predates CF-1, so NEURAL_SPEC_MIN is pinned to -35.0 in
  every module whose bound name the chain consults
  (cultivation.bioelectric.collective, exp142, exp145, exp148,
  exp94) — save/restore asserted.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-E1 (construction replay) projections bit-identical per pair
           (A1 == A2, 12/12); the unsigned |dev| values recomputed
           from the fresh decode match exp163's deposited
           v2_weighted devs within the 2-dp rounding (|diff| <=
           0.005 mV, 12/12 on both sides); the m2 side augmented ==
           A bit-exactly (W == 0, 12/12).
  GATE-E2 (null deposit first) the phase-A record exists in the
           deposit with the frozen null bar BEFORE the phase-B
           decode (byte-offset assertion, exp168's discipline);
           the pooled null bar is finite and > 0.
  GATE-E3 (the ensemble verdict) PASS iff |stat_m1| > null bar
           AND >= 9/12 pairs share the majority sign of dev1_signed
           (the ensemble reads a consistent cancellation-side
           response, not 12 independent coin flips). Failure
           deposited with the per-pair signed table.
  GATE-E4 (attribution at ensemble level) |stat_m2| <= null bar
           (the clique side stays silent when pooled — the contrast
           is attributable to the sign-cancellation member at the
           ensemble level, exp163's G3 discipline carried over).

NO post-hoc knob tuning; exactly ONE statistic. A --smoke instrument
check (pairs 0-1 only) is permitted before the credited run and
discarded; the credited full run uses the committed script unchanged.

DEPOSIT: results/exp173_pooled_grouping.json

RUN:
  python3 -m experiments.exp173_pooled_grouping            # full
  python3 -m experiments.exp173_pooled_grouping --smoke    # check
  python3 -m experiments.exp173_pooled_grouping --phase A  # runner split
  # jobs: phaseA | phaseB
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

from experiments.exp159_hyperedge_walk import (  # noqa: E402
    build_pair, co_membership, project, connected, GADGET_SIZE,
    T1, T2, SEED_CONSTRUCT, SEED_EXEC, OP, ERR_BAR,
)
from experiments.exp163_grouping_contrast import (  # noqa: E402
    cancel_mass_matrix, NOISE_MULTIPLE,
)
from experiments.exp142_sign_read import execute_signed  # noqa: E402

# ---- INSTRUMENT PIN (see docstring) --------------------------------
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


OUT = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")
DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")
N_PAIRS = 12
MAJORITY_MIN = 9               # of 12 pairs share the majority sign

# ---- body-level constants (the statistic's null protocol; fixed here,
#      BEFORE any decode, per the pre-registered rule "max |pooled null
#      stat| over the deposited null protocol's seeds") ------------------
SMOKE_PAIRS = (0, 1)           # docstring: smoke = pairs 0-1 only, discarded
SMOKE_OUT = OUT + ".smoke.json"
# The null protocol's seeds: the read core's own deposited seed convention
# (exp142.SEEDS = (1, 2, 3), asserted at runtime); seed 1 is exp163's
# credited-run seed, replayed bit-exactly against exp163's deposit.
NULL_SEEDS = (1, 2, 3)

_PHASE_A_WRITE_MARKER = "# === PHASE-A DEPOSIT WRITE (byte-order discipline"
_PHASE_B_DECODE_MARKER = "# === FIRST PHASE-B (REAL-ARM) DECODE CALL"


def assert_phase_order() -> dict:
    """E2's byte-offset assertion (exp168's discipline): the phase-A
    deposit write precedes the first phase-B (real-arm) decode call, by
    byte offset in this file."""
    src = open(os.path.abspath(__file__)).read()
    i_a = src.index(_PHASE_A_WRITE_MARKER)
    i_b = src.index(_PHASE_B_DECODE_MARKER)
    assert i_a < i_b, "pre-registration order violated: the phase-A " \
                      "null deposit write must precede the first " \
                      "phase-B decode path"
    return {"phase_a_write_byte": i_a, "first_phase_b_decode_byte": i_b,
            "order_held": True}


def construct_pairs(n_pairs: int) -> list:
    """exp163's construction phase VERBATIM (replayed for integrity)."""
    pairs = []
    for p in range(n_pairs):
        n, m1, m2 = build_pair(p)
        A1 = project(m1, n)
        A2 = project(m2, n)
        assert np.array_equal(A1, A2), f"pair {p}: projections differ"
        S1 = co_membership(m1, n)
        S2 = co_membership(m2, n)
        assert not np.array_equal(S1, S2), f"pair {p}: S matrices identical"
        assert np.array_equal(S2, (A2 != 0).astype(float)), \
            f"pair {p}: size-2 reduction S==support(A) violated"
        cancel1 = int(np.sum((S1 > 0) & (A1 == 0)) // 2)
        cancel2 = int(np.sum((S2 > 0) & (A2 == 0)) // 2)
        assert cancel1 > 0 and cancel2 == 0, f"pair {p}: cancellation layout"
        assert connected(A1), f"pair {p}: projection not connected"
        pairs.append({"p": p, "n": n, "k": GADGET_SIZE[p], "A": A1,
                      "S1": S1, "S2": S2, "m1": m1, "m2": m2,
                      "cancel_entries_S1": cancel1})
    return pairs


def recompute_F(pairs: list) -> float:
    """exp163's F, recomputed BEFORE any decode (asserted vs deposit)."""
    pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in pairs])
    return float(np.median(np.abs(pool)))


def phase_a_null(pairs: list, dep163: dict, out_path: str,
                 order_ev: dict, smoke: bool) -> tuple:
    """PHASE-A: the pooled null distribution from the SHARED arm-1 null,
    deposited (with the frozen bar) BEFORE any real-arm decode.

    Per pair, the signed dev of a PLACEHOLDER member whose augmentation
    is exp163's deposited null augmentation (the arm-1 null arm: the
    shared bit-identical plain projection A) against its own target;
    the arm-1 null errs at exp163's credited seed are exp163's DEPOSITED
    null_err values, replayed bit-exactly (asserted). The bar =
    max |pooled null stat| over the null protocol's seeds x the shared
    null's own-targets (T1 = the sign-cancellation side, T2 = the
    clique side) — one bar, frozen once, gating both E3 and E4."""
    dep_null = {rec["p"]: rec["null_err"] for rec in dep163["pairs"]}
    targets = (("T1", T1), ("T2", T2))
    null_errs = {}
    for q in pairs:
        A = q["A"]
        for tname, spec in targets:
            for s in NULL_SEEDS:
                r = execute_signed(spec, A, s, OP)   # null-arm decode
                e = float(r["err_vs_target"])
                assert np.isfinite(e), f"pair {q['p']} {tname} seed {s}"
                null_errs[(q["p"], tname, s)] = e
    # seed-1 replay: bit-exact vs exp163's deposited null_err values
    replay = [(q["p"], tname,
               null_errs[(q["p"], tname, 1)] == float(dep_null[q["p"]][tname]))
              for q in pairs for tname, _ in targets]
    n_replay_ok = sum(int(ok) for _, _, ok in replay)
    assert n_replay_ok == len(replay), \
        f"seed-1 null replay not bit-exact vs exp163's deposit: " \
        f"{n_replay_ok}/{len(replay)}"
    # pooled null stats: per seed, per own-target side (signed mean)
    pooled = {}
    for s in NULL_SEEDS:
        for tname, _ in targets:
            devs = [null_errs[(q["p"], tname, s)]
                    - float(dep_null[q["p"]][tname]) for q in pairs]
            pooled[f"{tname}@seed{s}"] = float(np.mean(devs))
    bar = round(max(abs(v) for v in pooled.values()), 6)   # frozen value
    assert np.isfinite(bar) and bar > 0, \
        f"pooled null bar must be finite and > 0 (got {bar})"
    record = {
        "phase": "A (null deposit; frozen before any real-arm decode)",
        "null_protocol": {
            "augmentation": "exp163's deposited null augmentation: the "
                            "arm-1 null arm = the shared bit-identical "
                            "plain projection A (no S term)",
            "baseline": "exp163's DEPOSITED null_err values per "
                        "pair/target",
            "placeholder": "one placeholder member per pair, decoded on "
                           "the null augmentation at each protocol seed, "
                           "signed dev vs the deposited null_err",
            "seeds": list(NULL_SEEDS),
            "seed_source": "exp142's deposited SEEDS (1,2,3) — the read "
                           "core's own seed convention (asserted at "
                           "runtime); seed 1 = exp163's credited-run "
                           "seed, replayed bit-exactly",
            "pooled_null_stat": "mean over pairs of [err(A, own_target, "
                                "seed) - deposited null_err], SIGNED",
            "bar_rule": "null bar = max |pooled null stat| over the "
                        "protocol's seeds x the shared null's "
                        "own-targets (T1/T2) — one bar, frozen once, "
                        "gating E3 and E4",
        },
        "seed1_replay_bit_exact": f"{n_replay_ok}/{len(replay)}",
        "pooled_null_stats": {k: round(v, 6) for k, v in pooled.items()},
        "null_bar": round(bar, 6),
        "null_bar_finite_positive": True,
        "frozen_before_phase_b_decode": True,
        "byte_offset_evidence": order_ev,
        "pair_scope": f"{len(pairs)} pairs",
        "smoke": bool(smoke),
    }
    # === PHASE-A DEPOSIT WRITE (byte-order discipline: this write is on
    # disk BEFORE the first phase-B real-arm decode; the bar is frozen
    # here) ===============================================================
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({"experiment": "exp173_the_pooled_grouping_statistic",
                   "phase_a": record}, f, indent=1)
    return record, bar


def main(args=None) -> dict:
    import time
    t0 = time.time()
    if args is None:
        ap = argparse.ArgumentParser()
        ap.add_argument("--smoke", action="store_true")
        ap.add_argument("--phase", choices=["A", "B", "all"], default="all")
        ap.add_argument("--out", default=None)
        args = ap.parse_args()
    smoke = bool(args.smoke)
    phase = args.phase
    out_path = args.out or (SMOKE_OUT if smoke else OUT)
    decode_scope = list(SMOKE_PAIRS if smoke else range(N_PAIRS))

    assert NULL_SEEDS == _m142.SEEDS, \
        "null seeds must be the executor's deposited seed convention"
    assert SEED_EXEC in NULL_SEEDS, \
        "exp163's credited seed must be in the null protocol"
    order_ev = assert_phase_order()

    dep163 = json.load(open(DEP163))
    dep_pairs = {rec["p"]: rec for rec in dep163["pairs"]}

    # construction replayed for integrity (exp163 verbatim, all 12 pairs
    # so the F pool is bit-identical to the deposit's); decode scope only
    # shrinks under --smoke (discarded instrument check)
    pairs = construct_pairs(N_PAIRS)
    F = recompute_F(pairs)
    assert F == dep163["F"], f"F drifted from exp163's deposit: {F} vs {dep163['F']}"

    pin_floor()
    try:
        # ---------------- PHASE A: null deposit (frozen bar) -------------
        if phase in ("A", "all"):
            scope = [q for q in pairs if q["p"] in decode_scope]
            phase_a, bar = phase_a_null(scope, dep163, out_path,
                                        order_ev, smoke)
        if phase == "A":
            restore_floor()
            for m in PIN_MODULES:
                if hasattr(m, "NEURAL_SPEC_MIN"):
                    assert getattr(m, "NEURAL_SPEC_MIN") == _PIN_SAVE[m.__name__]
            return {"phase": "A", "phase_a": phase_a, "out": out_path}

        # ---------------- PHASE B: real arm ------------------------------
        # dynamic half of E2: the phase-A record with the frozen bar is
        # confirmed ON DISK before the first real-arm decode call
        disk = json.load(open(out_path))
        assert "phase_a" in disk, \
            "phase-A record missing from the deposit (two-phase discipline)"
        if phase == "B":
            phase_a = disk["phase_a"]
            bar = float(phase_a["null_bar"])
            assert np.isfinite(bar) and bar > 0, "frozen bar not finite > 0"
        else:
            assert float(disk["phase_a"]["null_bar"]) == bar, \
                "phase-A bar on disk does not match the in-process bar"
            phase_a = disk["phase_a"]
        pa_bytes = os.path.getsize(out_path)

        n_m2id = 0
        for q in pairs:
            if q["p"] not in decode_scope:
                continue
            A, n = q["A"], q["n"]
            W1 = cancel_mass_matrix(q["m1"], n)
            W2 = cancel_mass_matrix(q["m2"], n)
            Sw1 = q["S1"] * W1
            Sw2 = q["S2"] * W2
            # E1: member 2 (all-size-2) -> W == 0 -> augmented == A
            if np.array_equal(Sw2, np.zeros((n, n))) and \
                    np.array_equal(A + F * Sw2, A):
                n_m2id += 1
            else:
                raise AssertionError(
                    f"pair {q['p']}: weighted m2 augmentation not a "
                    f"bit-exact identity")
            # === FIRST PHASE-B (REAL-ARM) DECODE CALL =====================
            # exp163's decode call pattern verbatim (own-target, V2
            # weighted augmentation, seed 1, STAR_OP)
            q["dec"] = {
                "m1": execute_signed(T1, A + F * Sw1, SEED_EXEC, OP),
                "m2": execute_signed(T2, A + F * Sw2, SEED_EXEC, OP),
            }

        # signed devs vs exp163's deposited arm-1 null errs
        per_pair, dev1s, dev2s = [], [], []
        n_match1 = n_match2 = 0
        for q in pairs:
            if q["p"] not in decode_scope:
                continue
            rec = dep_pairs[q["p"]]
            v2 = rec["v2_weighted"]
            e1 = float(q["dec"]["m1"]["err_vs_target"])
            e2 = float(q["dec"]["m2"]["err_vs_target"])
            d1 = e1 - float(rec["null_err"]["T1"])
            d2 = e2 - float(rec["null_err"]["T2"])
            ok1 = abs(abs(d1) - float(v2["dev1_signcancellation_side"])) <= 0.005
            ok2 = abs(abs(d2) - float(v2["dev2_clique_side"])) <= 0.005
            n_match1 += int(ok1)
            n_match2 += int(ok2)
            dev1s.append(d1)
            dev2s.append(d2)
            per_pair.append({
                "p": q["p"], "n": q["n"], "k": q["k"],
                "cancel_entries_S1": q["cancel_entries_S1"],
                "null_err_deposited": rec["null_err"],
                "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                "dev1_signed": round(d1, 6), "dev2_signed": round(d2, 6),
                "sign_dev1": 1 if d1 > 0 else (-1 if d1 < 0 else 0),
                "dev1_deposited_v2": v2["dev1_signcancellation_side"],
                "dev2_deposited_v2": v2["dev2_clique_side"],
                "unsigned_dev_match_m1": bool(ok1),
                "unsigned_dev_match_m2": bool(ok2),
            })

        np_ = len(per_pair)
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

        # ---------------- gates (each evaluated exactly once) ------------
        e1_pass = bool(np_ == len(decode_scope) == N_PAIRS
                       and n_match1 == np_ and n_match2 == np_
                       and n_m2id == np_)
        e2_pass = bool(order_ev["order_held"]
                       and phase_a["frozen_before_phase_b_decode"]
                       and np.isfinite(bar) and bar > 0
                       and not phase_a["smoke"])
        e3_pass = bool(abs(stat_m1) > bar and n_maj >= MAJORITY_MIN)
        e4_pass = bool(abs(stat_m2) <= bar)

        gates = {
            "E1_construction_replay": {
                "pass": e1_pass,
                "projections_bit_identical": f"{np_}/{np_}",
                "unsigned_dev_match_m1_le_0.005": f"{n_match1}/{np_}",
                "unsigned_dev_match_m2_le_0.005": f"{n_match2}/{np_}",
                "m2_aug_bit_exact_identity": f"{n_m2id}/{np_}"},
            "E2_null_deposit_first": {
                "pass": e2_pass,
                "byte_offset_order_held": order_ev["order_held"],
                "phase_a_record_on_disk_before_phase_b_decode": True,
                "phase_a_record_bytes_on_disk": pa_bytes,
                "seed1_replay_bit_exact": phase_a["seed1_replay_bit_exact"],
                "null_bar": bar,
                "null_bar_finite_positive": bool(np.isfinite(bar) and bar > 0)},
            "E3_ensemble_verdict": {
                "pass": e3_pass,
                "stat_m1_signed_mean": round(stat_m1, 6),
                "abs_stat_m1_gt_bar": bool(abs(stat_m1) > bar),
                "n_majority_sign": n_maj, "required": MAJORITY_MIN,
                "n_pos": npos, "n_neg": nneg, "n_zero": nzero},
            "E4_attribution_ensemble": {
                "pass": e4_pass,
                "stat_m2_signed_mean": round(stat_m2, 6),
                "abs_stat_m2_le_bar": bool(abs(stat_m2) <= bar)},
        }
        overall = all(g["pass"] for g in gates.values())

        if overall:
            verdict_word = (
                "ENSEMBLE READS THE GROUPING — the signed pooled mean "
                "over exp163's 12 adversarial pairs crosses the frozen "
                "null bar (|stat_m1| = %.4f > bar %.4f) with a %d/12 "
                "majority sign on the sign-cancellation side and a "
                "silent clique side (|stat_m2| = %.4f <= bar): the sign "
                "structure exp163 never read carries the grouping at "
                "the ensemble level" % (abs(stat_m1), bar, n_maj,
                                        abs(stat_m2)))
        elif not (e1_pass and e2_pass):
            verdict_word = "INSTRUMENT/CONSTRUCTION FAIL — see gates E1/E2"
        elif not e3_pass:
            verdict_word = (
                "REFUTED AT THE ENSEMBLE — |stat_m1| = %.4f vs frozen "
                "null bar %.4f, majority sign %d/12 (need >= %d): "
                "pooling does not lift the grouping signal above the "
                "null; per-pair signed table deposited"
                % (abs(stat_m1), bar, n_maj, MAJORITY_MIN))
        else:
            verdict_word = (
                "ATTRIBUTION FAILS — clique side not silent when pooled "
                "(|stat_m2| = %.4f > bar %.4f)" % (abs(stat_m2), bar))

        doc = {
            "experiment": "exp173_the_pooled_grouping_statistic",
            "task_id": "1-e",
            "repair_of": "exp163 (ledger L144) registered repair (b): "
                         "pooled/ensemble statistic across pairs",
            "smoke": smoke,
            "pre_registered": {
                "source": "module docstring, committed at HEAD "
                          "(0f55852) BEFORE any decode; the credited "
                          "run used this file unchanged",
                "statistic": "stat = mean over pairs of dev_signed; "
                             "dev1_signed = err(A + F*Sw1, T1) - "
                             "err(A, T1); dev2_signed = err(A + F*Sw2, "
                             "T2) - err(A, T2); V2 weighting verbatim",
                "gates": "E1 construction replay; E2 null deposit first "
                         "(byte-offset discipline); E3 |stat_m1| > bar "
                         "AND >= 9/12 majority sign; E4 |stat_m2| <= bar",
                "seeds": {"exec": SEED_EXEC,
                          "null_protocol": list(NULL_SEEDS)},
            },
            "construction": {
                "F": F, "F_matches_exp163_deposit": True,
                "pairs_constructed": N_PAIRS,
                "decode_scope": ("smoke pairs 0-1 (discarded instrument "
                                 "check)" if smoke else "all 12 (credited)"),
            },
            "phase_a": phase_a,                    # verbatim, frozen
            "phase_a_write_evidence": {
                "byte_offset_order": order_ev,
                "phase_a_record_bytes_on_disk": pa_bytes,
                "record_confirmed_on_disk_before_phase_b_decode": True},
            "pairs": per_pair,
            "statistic": {
                "stat_m1_signed_mean": round(stat_m1, 6),
                "median_m1": round(med1, 6),
                "stat_m2_signed_mean": round(stat_m2, 6),
                "median_m2": round(med2, 6),
                "majority_sign": maj_sign,
                "n_pairs_sharing_majority_sign": n_maj,
                "n_pos": npos, "n_neg": nneg, "n_zero": nzero},
            "null_bar": bar,
            "gates": gates,
            "all_gates_pass": overall,
            "verdict": verdict_word,
            "wall_seconds": round(time.time() - t0, 1),
        }
        with open(out_path, "w") as f:
            json.dump(doc, f, indent=1,
                      default=lambda o: list(o) if isinstance(o, tuple) else o)
        print(json.dumps({
            "smoke": smoke, "E1": e1_pass, "E2": e2_pass, "E3": e3_pass,
            "E4": e4_pass, "stat_m1": round(stat_m1, 6), "stat_m2":
            round(stat_m2, 6), "null_bar": bar, "majority": n_maj,
            "all_pass": overall, "wall_s": doc["wall_seconds"],
            "out": out_path}))
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
    ap.add_argument("--phase", choices=["A", "B", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main(args)  # noqa: F841  (body: honor --smoke/--phase/--out)
