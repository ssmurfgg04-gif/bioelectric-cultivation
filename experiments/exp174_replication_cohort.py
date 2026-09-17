#!/usr/bin/env python3
"""exp174 — THE REPLICATION COHORT (the ensemble's second 12).

exp173's registered next (L152): the signed-mean signature is a power
claim, and "a power claim is only as good as its second cohort" — 12
FRESH adversarial pairs (same construction protocol, new construction
seed) to test whether stat_m1 > null bar with a >= 9/12 majority sign
REPLICATES; plus the minority-pair anatomy (the 2 minority-sign pairs
of the original cohort) recorded.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Cohort, statistic, and gates are fixed
now; the credited run uses this file unchanged.

THE FRESH COHORT:
  exp159's construction VERBATIM with the ONE changed input disclosed
  here: exp159.SEED_CONSTRUCT rebound 159 -> 174174 for the cohort
  build (the OLD_FLOOR_PIN rebinding mechanism — save, rebind, build
  all 12 pairs via build_pair(p) p = 0..11, restore asserted). The
  construction protocol is otherwise untouched: same GADGET_SIZE,
  same T1/T2 targets, same OP, same adversarial family structure —
  the 12 fresh pairs are the same CLASS of object with independent
  draws, not a re-run of the original 12.

THE STATISTIC (exp173's, verbatim — zero new choices):
  dev_signed(p) = err(A + F*S_v(m1), T1) - err(A, T1)   [signed]
  stat = mean over the 12 pairs; V2 weighting via exp163's
  cancel_mass_matrix VERBATIM; STAR_OP readout, seed (1,); m2 side
  computed identically for attribution.

TWO-PHASE NULL DISCIPLINE (exp173's, verbatim):
  PHASE-A: the fresh cohort's null bar frozen on disk BEFORE any
  real-arm decode — per-pair null = the shared arm-1 null decode of
  the bit-identical projection (exp163/exp173's null protocol); bar =
  max |pooled null stat| over exp142's deposited seeds (1, 2, 3) x
  own-targets. Byte-offset assertion in the deposit.
  PHASE-B: the real arm.

INSTRUMENT PIN: the chain predates CF-1; NEURAL_SPEC_MIN pinned to
  -35.0 (exp167's mechanism, save/restore asserted).

MINORITY ANATOMY (recorded, no bar): exp173's deposit lists the
  per-pair signed devs of the ORIGINAL cohort; the minority-sign
  pairs' structural features (density d_k, cancel_entries_S1,
  gadget size, sw1 mass) are tabulated against the majority pairs'
  — the deposit carries the table; any structural split is the
  registered question, not a gate.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-F1 (fresh construction integrity) per pair: A1 == A2
           bit-identical, S_1 != S_2, S_2 == support(A), connectivity
           holds — 12/12 (exp163's G3/A1 discipline on the new
           cohort); the fresh projections differ from the original
           cohort's (independence check: no pair's projection
           bit-equal to any original pair's).
  GATE-F2 (null discipline) the phase-A record precedes the phase-B
           decode (byte offsets in the deposit); the fresh null bar
           is finite and > 0.
  GATE-F3 (REPLICATION — the gate) |stat_m1_fresh| > fresh null bar
           AND >= 9/12 pairs share the majority sign of dev1_signed.
           PASS = the signature replicates on independent draws.
           Failure = the original cohort's 4/4 was cohort luck —
           deposited honestly and the ensemble claim DOWNGRADED to
           cohort-specific in the ledger.
  GATE-F4 (attribution replicates) |stat_m2_fresh| <= fresh null
           bar (the clique side silent on the fresh cohort too).

NO post-hoc knob tuning. A --smoke check (fresh pairs 0-1) is
permitted before the credited run and discarded.

DEPOSIT: results/exp174_replication_cohort.json

RUN:
  python3 -m experiments.exp174_replication_cohort          # full
  python3 -m experiments.exp174_replication_cohort --smoke  # check
  python3 -m experiments.exp174_replication_cohort --phase A
  # jobs: phaseA | phaseB | anatomy
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


# ---- FIXED CONSTANTS ------------------------------------------------
FRESH_SEED_CONSTRUCT = 174174    # the ONE changed input, disclosed
N_PAIRS = 12
MAJORITY_MIN = 9

OUT = os.path.join(ROOT, "results", "exp174_replication_cohort.json")
DEP173 = os.path.join(ROOT, "results", "exp173_pooled_grouping.json")
DEP163 = os.path.join(ROOT, "results", "exp163_grouping_contrast.json")


# ---- body-level constants (fixed here, BEFORE any decode) --------------
# Null protocol (docstring, pre-registered): per-pair null = the shared
# arm-1 null decode of the bit-identical projection (exp163/exp173's null
# protocol); bar = max |pooled null stat| over exp142's deposited seeds
# (1, 2, 3) x own-targets. The FRESH cohort has no prior deposit, so the
# seed-1 null decode (seed 1 = exp159.SEED_EXEC, the credited decode seed)
# is the per-pair baseline and the pooled null stat at (seed, own-target)
# is the SIGNED mean over pairs of [err(A, target, seed) - err(A, target,
# seed 1)] — exp173's two-phase discipline translated to a fresh
# construction, zero new choices (seed 1 contributes exactly 0; the bar
# is carried by the protocol's other seeds, pure null-arm seed noise).
SMOKE_PAIRS = (0, 1)           # docstring: smoke = fresh pairs 0-1, discarded
SMOKE_OUT = OUT + ".smoke.json"
NULL_SEEDS = (1, 2, 3)         # exp142's deposited seed convention (asserted)

_PHASE_A_WRITE_MARKER = "# === PHASE-A DEPOSIT WRITE (byte-order discipline"
_PHASE_B_DECODE_MARKER = "# === FIRST PHASE-B (REAL-ARM) DECODE CALL"


def assert_phase_order() -> dict:
    """F2's byte-offset assertion (exp168's discipline, exp173's
    mechanism): the phase-A deposit write precedes the first phase-B
    (real-arm) decode call, by byte offset in this file."""
    src = open(os.path.abspath(__file__)).read()
    i_a = src.index(_PHASE_A_WRITE_MARKER)
    i_b = src.index(_PHASE_B_DECODE_MARKER)
    assert i_a < i_b, "pre-registration order violated: the phase-A " \
                      "null deposit write must precede the first " \
                      "phase-B decode path"
    return {"phase_a_write_byte": i_a, "first_phase_b_decode_byte": i_b,
            "order_held": True}


def build_cohort() -> tuple:
    """THE FRESH COHORT (docstring, verbatim protocol): exp159's
    construction with the ONE changed input disclosed pre-run —
    exp159.SEED_CONSTRUCT rebound 159 -> FRESH_SEED_CONSTRUCT (174174)
    for the cohort build; save, rebind, and restore asserted. The
    ORIGINAL cohort's projections are built first (exp159's own seed
    159) for the F1 independence check (construction only, no decode).
    Per fresh pair the exp163/exp173 construction asserts: A1 == A2
    bit-identical, S1 != S2, S2 == support(A) (all-size-2 reduction),
    cancellation layout, connectivity. Returns (fresh_pairs,
    n_original_projections)."""
    saved = exp159.SEED_CONSTRUCT
    assert saved == 159, f"exp159.SEED_CONSTRUCT drifted pre-rebind: {saved}"
    # original cohort's projections (construction only -- F1 independence)
    orig_projs = []
    for p in range(N_PAIRS):
        n_o, m1_o, _ = build_pair(p)
        orig_projs.append(project(m1_o, n_o))
    # THE REBIND — the one changed input, disclosed in the docstring
    exp159.SEED_CONSTRUCT = FRESH_SEED_CONSTRUCT
    assert exp159.SEED_CONSTRUCT == FRESH_SEED_CONSTRUCT, "rebind failed"
    fresh = []
    for p in range(N_PAIRS):
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
        # structural features for the minority anatomy (construction math)
        W1 = cancel_mass_matrix(m1, n)
        Sw1 = S1 * W1
        nz = Sw1[Sw1 > 0]
        cmask = (S1 > 0) & (A1 == 0)
        fresh.append({"p": p, "n": n, "k": GADGET_SIZE[p],
                      "A": A1, "S1": S1, "S2": S2, "m1": m1, "m2": m2,
                      "cancel_entries_S1": cancel1,
                      "density_d_k": float(W1[cmask].sum()),
                      "sw1_stats": {"nnz_entries": int(nz.size // 2),
                                    "min": float(nz.min()),
                                    "max": float(nz.max())}})
    # RESTORE asserted
    exp159.SEED_CONSTRUCT = saved
    assert exp159.SEED_CONSTRUCT == saved == 159, "SEED_CONSTRUCT not restored"
    # F1 independence: no fresh pair's projection bit-equal to any
    # original pair's projection (A1 == A2 per pair on both cohorts)
    for q in fresh:
        q["independent_of_original"] = not any(
            np.array_equal(q["A"], A0) for A0 in orig_projs)
    return fresh, len(orig_projs)


def recompute_F(pairs: list) -> float:
    """F, recomputed BEFORE any decode by exp159/exp163's pre-registered
    rule applied to the FRESH pool: median |A_ij| over nonzero entries
    pooled across the 12 fresh projections."""
    pool = np.concatenate([q["A"][q["A"] != 0].ravel() for q in pairs])
    return float(np.median(np.abs(pool)))


def phase_a_null(pairs: list, out_path: str, order_ev: dict, F: float,
                 smoke: bool) -> tuple:
    """PHASE-A (exp173's two-phase null discipline): the fresh cohort's
    pooled null distribution from the SHARED arm-1 null decode of the
    bit-identical projection, deposited (with the frozen bar) BEFORE any
    real-arm decode. Per pair, the null arm is the plain projection A
    decoded at each protocol seed against each side's own target (T1 =
    the sign-cancellation side's, T2 = the clique side's); the pooled
    null stat at (seed, own-target) = the SIGNED mean over pairs of
    [err(A, target, seed) - err(A, target, seed 1)]. One bar, frozen
    once, gating F3 and F4."""
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
    # pooled null stats: per seed, per own-target side (signed mean vs the
    # seed-1 baseline -- the credited decode seed's own null arm)
    pooled = {}
    for s in NULL_SEEDS:
        for tname, _ in targets:
            devs = [null_errs[(q["p"], tname, s)]
                    - null_errs[(q["p"], tname, 1)] for q in pairs]
            pooled[f"{tname}@seed{s}"] = float(np.mean(devs))
    bar = round(max(abs(v) for v in pooled.values()), 6)   # frozen value
    assert np.isfinite(bar) and bar > 0, \
        f"pooled null bar must be finite and > 0 (got {bar})"
    record = {
        "phase": "A (null deposit; frozen before any real-arm decode)",
        "null_protocol": {
            "augmentation": "exp163/exp173's null augmentation: the "
                            "arm-1 null arm = the shared bit-identical "
                            "plain projection A (no S term)",
            "placeholder": "one placeholder member per pair, decoded on "
                           "the null augmentation at each protocol seed, "
                           "against each side's own target",
            "seeds": list(NULL_SEEDS),
            "seed_source": "exp142's deposited SEEDS (1,2,3) — the read "
                           "core's own seed convention (asserted at "
                           "runtime); seed 1 = the credited decode seed "
                           "(exp159.SEED_EXEC), the fresh cohort's "
                           "baseline — no prior deposit exists for a "
                           "fresh construction",
            "pooled_null_stat": "mean over pairs of [err(A, own_target, "
                                "seed) - err(A, own_target, seed 1)], "
                                "SIGNED",
            "bar_rule": "null bar = max |pooled null stat| over the "
                        "protocol's seeds x own-targets (T1/T2) — one "
                        "bar, frozen once, gating F3 and F4",
        },
        "F_frozen": F,
        "pooled_null_stats": {k: round(v, 6) for k, v in pooled.items()},
        "null_err_seed1": {str(q["p"]): {t: null_errs[(q["p"], t, 1)]
                                         for t, _ in targets}
                           for q in pairs},
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
        json.dump({"experiment": "exp174_the_replication_cohort",
                   "phase_a": record}, f, indent=1)
    return record, bar


def _anatomy_side(rows: dict, devs: dict, dev_source: str) -> dict:
    """One cohort's minority/majority tabulation (recorded, no bar)."""
    npos = sum(1 for d in devs.values() if d > 0)
    nneg = sum(1 for d in devs.values() if d < 0)
    maj = 1 if npos > nneg else (-1 if nneg > npos else 0)

    def grp(minority: bool) -> dict:
        if maj == 0:
            ps = []
        else:
            ps = sorted(p for p, d in devs.items()
                        if d != 0 and ((d > 0) != (maj > 0)) == minority)
        feats = {}
        for f in ("k", "cancel_entries_S1", "density_d_k",
                  "sw1_mass_max", "sw1_nnz_entries"):
            vals = [rows[p][f] for p in ps]
            feats[f] = ({"min": min(vals), "median": float(np.median(vals)),
                         "max": max(vals)} if vals else None)
        return {"n_pairs": len(ps), "pairs": ps, "features": feats}

    return {
        "dev_source": dev_source,
        "majority_sign": maj, "n_pos": npos, "n_neg": nneg,
        "minority_sign_pairs": grp(True),
        "majority_sign_pairs": grp(False),
        "per_pair_signed_devs": {str(p): devs[p] for p in sorted(devs)},
    }


def minority_anatomy(fresh_per_pair: list = None) -> dict:
    """MINORITY ANATOMY (docstring: recorded, no gate): exp173's deposit
    lists the per-pair signed devs of the ORIGINAL cohort; the
    minority-sign pairs' structural features (density d_k,
    cancel_entries_S1, gadget size, sw1 mass) are tabulated against the
    majority pairs'. Original-cohort features come from exp163's
    deposit; fresh-cohort features (when supplied) from this run."""
    dep173 = json.load(open(DEP173))
    dep163 = json.load(open(DEP163))
    feat163 = {rec["p"]: rec for rec in dep163["pairs"]}
    devs = {rec["p"]: float(rec["dev1_signed"]) for rec in dep173["pairs"]}
    rows = {p: {"k": feat163[p]["k"],
                "cancel_entries_S1": feat163[p]["cancel_entries_S1"],
                "density_d_k": feat163[p]["density_d_k"],
                "sw1_mass_max": feat163[p]["sw1_stats"]["max"],
                "sw1_nnz_entries": feat163[p]["sw1_stats"]["nnz_entries"]}
            for p in devs}
    table = {"original_cohort": _anatomy_side(
        rows, devs, "exp173's deposited dev1_signed (the original cohort)")}
    if fresh_per_pair is not None:
        fdevs = {r["p"]: float(r["dev1_signed"]) for r in fresh_per_pair}
        frows = {r["p"]: {"k": r["k"],
                          "cancel_entries_S1": r["cancel_entries_S1"],
                          "density_d_k": r["density_d_k"],
                          "sw1_mass_max": r["sw1_stats"]["max"],
                          "sw1_nnz_entries": r["sw1_stats"]["nnz_entries"]}
                 for r in fresh_per_pair}
        table["fresh_cohort"] = _anatomy_side(
            frows, fdevs, "this run's dev1_signed (the fresh cohort)")
    return table


def _anatomy_job(out_path: str, t0: float) -> dict:
    """--phase anatomy (runner split): the minority-pair anatomy recorded,
    no gate, no decode. Merges the fresh-cohort side into a full exp174
    deposit when one is on disk at out_path; otherwise writes a
    standalone anatomy record."""
    fresh_side = None
    if os.path.exists(out_path):
        try:
            disk = json.load(open(out_path))
        except json.JSONDecodeError:
            disk = None
        if isinstance(disk, dict) \
                and disk.get("experiment") == "exp174_the_replication_cohort" \
                and "pairs" in disk and "gates" in disk:
            fresh_side = disk["pairs"]
    an = minority_anatomy(fresh_per_pair=fresh_side)
    if fresh_side is not None:
        disk["minority_anatomy"] = an
        doc = disk
    else:
        doc = {"experiment": "exp174_the_replication_cohort",
               "job": "anatomy (recorded, no bar; no decode; the credited "
                      "deposit is written by the phase-B/full run)",
               "minority_anatomy": an}
    doc["wall_seconds"] = round(time.time() - t0, 1)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(doc, f, indent=1,
                  default=lambda o: list(o) if isinstance(o, tuple) else o)
    print(json.dumps({"anatomy": True, "out": out_path,
                      "original_minority_pairs":
                          an["original_cohort"]["minority_sign_pairs"]["pairs"]}))
    return doc


def main() -> dict:
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--phase", choices=["A", "B", "anatomy", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    smoke = bool(args.smoke)
    phase = args.phase
    out_path = args.out or (SMOKE_OUT if smoke else OUT)

    if phase == "anatomy":
        return _anatomy_job(out_path, t0)

    decode_scope = list(SMOKE_PAIRS if smoke else range(N_PAIRS))
    seed_exec = exp159.SEED_EXEC          # the credited decode seed (1)

    assert NULL_SEEDS == _m142.SEEDS, \
        "null seeds must be the executor's deposited seed convention"
    assert seed_exec == 1, \
        "the credited decode seed is exp159's deposited SEED_EXEC (1)"
    assert seed_exec in NULL_SEEDS, \
        "the credited seed must be in the null protocol"
    order_ev = assert_phase_order()

    # ---- construction: the FRESH cohort (the ONE changed input disclosed)
    pairs, n_orig = build_cohort()
    F = recompute_F(pairs)                # computed BEFORE any decode
    rebind_evidence = {
        "mechanism": "exp159's OLD_FLOOR_PIN rebinding mechanism: save, "
                     "rebind, build all 12 pairs via build_pair(p) "
                     "p = 0..11, restore asserted",
        "saved": 159, "rebound_to": FRESH_SEED_CONSTRUCT,
        "restored_to": exp159.SEED_CONSTRUCT,
        "restore_asserted": exp159.SEED_CONSTRUCT == 159,
        "original_cohort_projections_built_seed_159_for_F1_independence":
            n_orig,
    }
    n_indep = sum(int(q["independent_of_original"]) for q in pairs)

    pin_floor()
    try:
        # ---------------- PHASE A: null deposit (frozen bar) -------------
        if phase in ("A", "all"):
            scope = [q for q in pairs if q["p"] in decode_scope]
            phase_a, bar = phase_a_null(scope, out_path, order_ev, F,
                                        smoke)
        if phase == "A":
            restore_floor()
            for m in PIN_MODULES:
                if hasattr(m, "NEURAL_SPEC_MIN"):
                    assert getattr(m, "NEURAL_SPEC_MIN") == _PIN_SAVE[m.__name__]
            return {"phase": "A", "phase_a": phase_a, "out": out_path}

        # ---------------- PHASE B: real arm ------------------------------
        # dynamic half of F2: the phase-A record with the frozen bar is
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

        dep163 = json.load(open(DEP163))
        n_m2id = 0
        for q in pairs:
            if q["p"] not in decode_scope:
                continue
            A, n = q["A"], q["n"]
            W1 = cancel_mass_matrix(q["m1"], n)
            W2 = cancel_mass_matrix(q["m2"], n)
            Sw1 = q["S1"] * W1
            Sw2 = q["S2"] * W2
            # V2 weighting discipline: member 2 (all-size-2) -> W == 0
            # -> augmented == A bit-exactly
            if np.array_equal(Sw2, np.zeros((n, n))) and \
                    np.array_equal(A + F * Sw2, A):
                n_m2id += 1
            else:
                raise AssertionError(
                    f"pair {q['p']}: weighted m2 augmentation not a "
                    f"bit-exact identity")
            # === FIRST PHASE-B (REAL-ARM) DECODE CALL =====================
            # exp173's decode call pattern verbatim (own-target, V2
            # weighted augmentation, seed 1, STAR_OP)
            q["dec"] = {
                "m1": execute_signed(T1, A + F * Sw1, seed_exec, OP),
                "m2": execute_signed(T2, A + F * Sw2, seed_exec, OP),
            }

        # signed devs vs the phase-A frozen seed-1 null errs
        per_pair, dev1s, dev2s = [], [], []
        for q in pairs:
            if q["p"] not in decode_scope:
                continue
            base = phase_a["null_err_seed1"][str(q["p"])]
            e1 = float(q["dec"]["m1"]["err_vs_target"])
            e2 = float(q["dec"]["m2"]["err_vs_target"])
            d1 = e1 - float(base["T1"])
            d2 = e2 - float(base["T2"])
            dev1s.append(d1)
            dev2s.append(d2)
            per_pair.append({
                "p": q["p"], "n": q["n"], "k": q["k"],
                "cancel_entries_S1": q["cancel_entries_S1"],
                "density_d_k": round(q["density_d_k"], 4),
                "sw1_stats": q["sw1_stats"],
                "independent_of_original": q["independent_of_original"],
                "null_err_seed1_frozen": base,
                "err_m1_own_T1": e1, "err_m2_own_T2": e2,
                "dev1_signed": round(d1, 6), "dev2_signed": round(d2, 6),
                "sign_dev1": 1 if d1 > 0 else (-1 if d1 < 0 else 0),
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
        f1_pass = bool(n_indep == N_PAIRS and n_m2id == np_
                       and np_ == len(decode_scope))
        f2_pass = bool(order_ev["order_held"]
                       and phase_a["frozen_before_phase_b_decode"]
                       and np.isfinite(bar) and bar > 0
                       and not phase_a["smoke"])
        f3_pass = bool(abs(stat_m1) > bar and n_maj >= MAJORITY_MIN)
        f4_pass = bool(abs(stat_m2) <= bar)

        gates = {
            "F1_fresh_construction_integrity": {
                "pass": f1_pass,
                "construction_asserts_12_of_12":
                    f"{N_PAIRS}/{N_PAIRS} (asserted at build: A1==A2, "
                    f"S1!=S2, S2==support(A), cancellation layout, "
                    f"connectivity)",
                "independence_vs_original_cohort": f"{n_indep}/{N_PAIRS}",
                "m2_aug_bit_exact_identity": f"{n_m2id}/{np_}"},
            "F2_null_deposit_first": {
                "pass": f2_pass,
                "byte_offset_order_held": order_ev["order_held"],
                "phase_a_record_on_disk_before_phase_b_decode": True,
                "phase_a_record_bytes_on_disk": pa_bytes,
                "null_bar": bar,
                "null_bar_finite_positive": bool(np.isfinite(bar) and bar > 0),
                "smoke_scope": bool(phase_a["smoke"])},
            "F3_replication": {
                "pass": f3_pass,
                "stat_m1_fresh_signed_mean": round(stat_m1, 6),
                "abs_stat_m1_gt_bar": bool(abs(stat_m1) > bar),
                "n_majority_sign": n_maj, "required": MAJORITY_MIN,
                "n_pos": npos, "n_neg": nneg, "n_zero": nzero},
            "F4_attribution_replicates": {
                "pass": f4_pass,
                "stat_m2_fresh_signed_mean": round(stat_m2, 6),
                "abs_stat_m2_le_bar": bool(abs(stat_m2) <= bar)},
        }
        overall = all(g["pass"] for g in gates.values())

        # minority anatomy (recorded, no bar) -- original + fresh cohorts
        anatomy = minority_anatomy(fresh_per_pair=per_pair)

        if overall:
            verdict_word = (
                "REPLICATED — the signed-mean signature carries on "
                "independent draws: |stat_m1_fresh| = %.4f > fresh null "
                "bar %.4f with a %d/12 majority sign (need >= %d) and a "
                "silent clique side (|stat_m2_fresh| = %.4f <= bar); the "
                "ensemble claim survives its second cohort"
                % (abs(stat_m1), bar, n_maj, MAJORITY_MIN, abs(stat_m2)))
        elif not (f1_pass and f2_pass):
            verdict_word = "INSTRUMENT/CONSTRUCTION FAIL — see gates F1/F2"
        elif not f3_pass:
            verdict_word = (
                "REFUTED AT REPLICATION — |stat_m1_fresh| = %.4f vs fresh "
                "null bar %.4f, majority sign %d/12 (need >= %d): the "
                "original cohort's majority was cohort luck; the "
                "ensemble claim is DOWNGRADED to cohort-specific in the "
                "ledger" % (abs(stat_m1), bar, n_maj, MAJORITY_MIN))
        else:
            verdict_word = (
                "ATTRIBUTION FAILS TO REPLICATE — clique side not silent "
                "on the fresh cohort (|stat_m2_fresh| = %.4f > bar %.4f)"
                % (abs(stat_m2), bar))

        doc = {
            "experiment": "exp174_the_replication_cohort",
            "task_id": "2-a",
            "registered_next_of": "exp173 (ledger L152): the signed-mean "
                                  "signature is a power claim — a power "
                                  "claim is only as good as its second "
                                  "cohort",
            "smoke": smoke,
            "pre_registered": {
                "source": "module docstring, committed at HEAD (f75075f) "
                          "BEFORE any decode; the credited run used this "
                          "file unchanged",
                "cohort": "exp159's construction VERBATIM with the ONE "
                          "changed input disclosed: exp159.SEED_CONSTRUCT "
                          "rebound 159 -> 174174 for the cohort build "
                          "(save/rebind/restore asserted)",
                "statistic": "stat = mean over pairs of dev_signed; "
                             "dev1_signed = err(A + F*Sw1, T1) - err(A, "
                             "T1) SIGNED; m2 side computed identically "
                             "for attribution; V2 weighting via exp163's "
                             "cancel_mass_matrix VERBATIM; STAR_OP, "
                             "seed (1,)",
                "gates": "F1 fresh construction integrity 12/12 + "
                         "independence vs the original cohort; F2 "
                         "phase-A null deposit precedes phase-B decode "
                         "(byte-offset discipline) + bar finite > 0; "
                         "F3 |stat_m1_fresh| > fresh null bar AND >= 9/12 "
                         "majority sign; F4 |stat_m2_fresh| <= bar",
                "seeds": {"exec": seed_exec,
                          "null_protocol": list(NULL_SEEDS)},
                "seed_construct": {"original": 159,
                                   "fresh": FRESH_SEED_CONSTRUCT},
            },
            "construction": {
                "seed_rebind": rebind_evidence,
                "F": F,
                "F_rule": "median |A_ij| over nonzero entries pooled "
                          "across the 12 FRESH projections, computed "
                          "before any decode (exp159/exp163's rule)",
                "F_original_cohort_exp163_deposit": dep163["F"],
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
                "stat_m1_fresh_signed_mean": round(stat_m1, 6),
                "median_m1": round(med1, 6),
                "stat_m2_fresh_signed_mean": round(stat_m2, 6),
                "median_m2": round(med2, 6),
                "majority_sign": maj_sign,
                "n_pairs_sharing_majority_sign": n_maj,
                "n_pos": npos, "n_neg": nneg, "n_zero": nzero},
            "null_bar": bar,
            "minority_anatomy": anatomy,
            "gates": gates,
            "all_gates_pass": overall,
            "verdict": verdict_word,
            "wall_seconds": round(time.time() - t0, 1),
        }
        with open(out_path, "w") as f:
            json.dump(doc, f, indent=1,
                      default=lambda o: list(o) if isinstance(o, tuple) else o)
        print(json.dumps({
            "smoke": smoke, "F1": f1_pass, "F2": f2_pass, "F3": f3_pass,
            "F4": f4_pass, "stat_m1_fresh": round(stat_m1, 6),
            "stat_m2_fresh": round(stat_m2, 6), "null_bar": bar,
            "majority": n_maj, "all_pass": overall,
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
    ap.add_argument("--phase", choices=["A", "B", "anatomy", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--phase/--out)
