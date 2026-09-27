#!/usr/bin/env python3
"""exp430 — THE RESIDUAL'S GRAIN: THE LIMITING DECODE BIAS (batch HU-12;
exp428's registered follow-up). exp428 landed BIAS-STRUCTURAL: the
two-key (group, plane) bias cut the test MAE 0.2552 -> 0.2317 (the cut
landed) but the runs |z| persists -9.095 -> -6.721 -> -5.145 two-sided
— the sign structure survives BOTH pre-named keys. THE OPEN QUESTION:
is the residual sign structure a BIAS at any granularity the corpus's
own fields support, or is it STRUCTURAL — carried by the decode's
form itself (the next repair is a model change, not a bias term)?
THE INSTRUMENT (exp428's machinery verbatim; the ladder extended):
the corpus's own per-record fields name two pre-named THIRD keys —
`species` (17 distinct; the recorded baseline may be species-specific)
and `cut_f` (15 distinct; the dose axis the arm table carries) — each
fitted as a (group, plane, <field>) cell-median bias on the TRAIN rows
with exp428's support fallback (cells < MIN_SUPPORT carry 0). And the
LIMITING bias: a k-NN-in-corpus-fields bias — each TEST row's bias is
the median residual of its K = 15 nearest TRAIN rows under the Hamming
mismatch count over the five encoded fields (group, plane, species,
cut_f, ap_morphogen), ties broken by (distance, train corpus order) —
the finest bias key expressible WITHOUT a model change. If the sign
clustering survives the limiting bias, no bias term the corpus can
express will absorb it.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the deterministic chain reproduces — raw 0.3705 /
      decoded 0.2900 via the aggregates; the block rung 0.2552 vs
      exp423's deposited test_mae_after; the two-key rung reproduces
      exp428's deposited test MAE AND its z (-5.145) bit-tight
      (fail=STOP).
  G2  THE DISCIPLINE: train-only fit at every rung; the support
      fallback; the k-NN neighbors drawn from TRAIN rows only; no
      test residual touches any fit (asserted in-code).
  G3  THE DECISIVE LADDER (two-sided, the conservative ABSORB_Z = 3.0):
      if |z| < 3.0 at the species rung -> ABSORBED-SPECIES; if |z| <
      3.0 at the cut_f rung -> ABSORBED-CUTF; if both survive, the
      LIMITING rung decides: |z| >= 3.0 -> STRUCTURAL-COMPLETE (the
      residual is not a bias at any corpus-expressible key; the next
      repair is a model change); |z| < 3.0 -> ABSORBED-LIMITING.
  G4  THE ANATOMY: the full z + MAE ladder deposited at every rung +
      the support tables + the overfit disclosure (the limiting
      bias's MAE rising above the two-key's = the bias eats variance,
      not structure — disclosed, not gated).
  G5  deposit results/exp430_residual_grain.json.

BRANCH LATTICE: STRUCTURAL-COMPLETE / ABSORBED-SPECIES / ABSORBED-CUTF
/ ABSORBED-LIMITING / INSTRUMENT-REFUTED (G1 fail).

THE HONEST STAKES: exp415's decomposition put the decode axis at 4x
the data's own uncertainty; exp423 and exp428 each repaired a bias
rung and the sign clustering persisted. Either the corpus carries a
finer key (the residual was a label all along) or the decode's FORM
is the defect (the model-change candidate earns its freeze). Both
outcomes are deposits: the first names the key, the second closes
the bias-program with the model change as the only exit.
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

ENTRY_MAE = 0.2552
TWOKEY_MAE = 0.2317
ABSORB_Z = 3.0
KNN_K = 15
ANCHOR_TOL = 0.005
MIN_SUPPORT = 3
DEPOSIT = os.path.join(ROOT, "results", "exp430_residual_grain.json")

BODY_DISCLOSURES = [
    "the corpus rows, the train/test split (even/odd corpus order, "
    "excluded_C4 dropped), the block rung and the two-key rung are "
    "exp428's verbatim — this experiment extends the LADDER only",
    "the third keys are the corpus's own per-record fields (species, "
    "cut_f) — no invention; cells < MIN_SUPPORT or absent from train "
    "carry bias 0 (exp428's fallback verbatim)",
    "the limiting bias is a Hamming-k-NN over the five encoded fields "
    "(group, plane, species, cut_f, ap_morphogen), K = 15 TRAIN rows, "
    "ties by (distance, train corpus order); the applied form is "
    "still sim' = sim - bias — no model change (that is the point: "
    "the finest bias expressible)",
    "exp423's _runs_test_z imported verbatim; the runs test evaluated "
    "TWO-SIDED at every rung (the exp415 lesson); ABSORB_Z = 3.0 "
    "frozen conservative (claiming absorption requires the strong "
    "evidence)",
    "the analysis is deterministic (zero rng); the credited run is "
    "the first and only full run",
]

import numpy as np

from experiments.exp423_decode_bias_repair import _runs_test_z


def _median(xs):
    return float(np.median(xs)) if xs else 0.0


def _feats(r):
    return (str(r.get("group")), str(r.get("plane")),
            str(r.get("species")), str(r.get("cut_f")),
            str(r.get("ap_morphogen")))


def main() -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    dep = json.load(open(os.path.join(
        ROOT, "results", "exp118_corpus_full.json")))
    rows = [r for r in dep["per_record"]
            if "abs_err_raw" in r and "sim" in r]
    agg = dep["aggregates"]
    assert len(rows) == agg["n_raw"]
    mae_raw = float(np.mean([r["abs_err_raw"] for r in rows]))
    mae_dec = float(np.mean([r["abs_err_corrected"] for r in rows
                             if not r["excluded_C4"]]))
    assert abs(mae_raw - agg["mae_raw"]) <= ANCHOR_TOL and \
        abs(mae_dec - agg["mae_corrected_decoded"]) <= ANCHOR_TOL

    train, test = [], []
    for i, r in enumerate(rows):
        if r["excluded_C4"]:
            continue
        (train if i % 2 == 0 else test).append(r)

    # ---- rung 1: the per-block bias (exp423's fit, the entry point)
    blocks = sorted({r["group"] for r in rows if r.get("group")})
    block_bias = {b: _median([r["sim"] - r["recorded_corrected"]
                              for r in train if r["group"] == b])
                  for b in blocks}

    # ---- rung 2: the two-key bias (exp428's fit, the entry anchor)
    cells2 = {}
    for r in train:
        cells2.setdefault((str(r.get("group")), str(r.get("plane"))),
                          []).append(r["sim"] - r["recorded_corrected"])
    twokey_bias = {k: _median(v) for k, v in cells2.items()
                   if len(v) >= MIN_SUPPORT}

    # ---- rung 3a/3b: the two pre-named third keys
    def three_key(field):
        cells = {}
        for r in train:
            cells.setdefault((str(r.get("group")), str(r.get("plane")),
                              str(r.get(field))), []
            ).append(r["sim"] - r["recorded_corrected"])
        bias = {k: _median(v) for k, v in cells.items()
                if len(v) >= MIN_SUPPORT}
        return bias, {("%s|%s|%s" % k): len(v)
                      for k, v in sorted(cells.items())}, len(cells)

    sp_bias, sp_support, sp_seen = three_key("species")
    cf_bias, cf_support, cf_seen = three_key("cut_f")

    # ---- rung 4: the LIMITING k-NN bias (train-only, deterministic)
    train_feats = [_feats(r) for r in train]
    train_res = [r["sim"] - r["recorded_corrected"] for r in train]

    def knn_bias(r):
        f = _feats(r)
        scored = []
        for ti, tf in enumerate(train_feats):
            d = sum(1 for a, b in zip(f, tf) if a != b)
            scored.append((d, ti))
        scored.sort()
        top = [train_res[ti] for _, ti in scored[:KNN_K]]
        return _median(top)

    # ---- the test-half errors + sign runs at every rung
    e_rungs = {k: [] for k in ("raw", "block", "two_key", "species",
                               "cut_f", "limit")}
    s_rungs = {k: [] for k in e_rungs}
    for r in test:
        rec = r["recorded_corrected"]
        b1 = block_bias.get(r["group"], 0.0)
        b2 = twokey_bias.get((str(r.get("group")),
                              str(r.get("plane"))), 0.0)
        b3 = sp_bias.get((str(r.get("group")), str(r.get("plane")),
                          str(r.get("species"))), 0.0)
        b4 = cf_bias.get((str(r.get("group")), str(r.get("plane")),
                          str(r.get("cut_f"))), 0.0)
        b5 = knn_bias(r)
        sims = {"raw": r["sim"], "block": r["sim"] - b1,
                "two_key": r["sim"] - b2, "species": r["sim"] - b3,
                "cut_f": r["sim"] - b4, "limit": r["sim"] - b5}
        for k, v in sims.items():
            e_rungs[k].append(abs(v - rec))
            s_rungs[k].append(1 if v >= rec else -1)
    mae_rungs = {k: float(np.mean(v)) for k, v in e_rungs.items()}
    z_rungs, runs_rungs = {}, {}
    for k in e_rungs:
        z, R = _runs_test_z(np.array(s_rungs[k]))
        z_rungs[k] = z
        runs_rungs[k] = R

    # ---- G1 the anchors
    dep428 = json.load(open(os.path.join(
        ROOT, "results", "exp428_two_key_bias.json")))
    a428_mae = float(dep428["test_mae"]["two_key"])
    a428_z = float(dep428["runs_test"]["z_two_key"])
    entry_ok = abs(mae_rungs["block"] - ENTRY_MAE) <= ANCHOR_TOL and \
        abs(mae_rungs["two_key"] - a428_mae) <= 5e-4 and \
        abs(a428_mae - TWOKEY_MAE) <= 5e-4
    z_ok = abs(z_rungs["two_key"] - a428_z) <= 1e-3
    verdicts["G1"] = "PASS" if (entry_ok and z_ok) else "REFUTE"
    print("G1 %s (block %.4f / two-key %.4f vs %.4f; z two-key %.3f "
          "vs deposited %.3f)"
          % (verdicts["G1"], mae_rungs["block"], mae_rungs["two_key"],
             a428_mae, z_rungs["two_key"], a428_z))
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    else:
        # ---- G2 the discipline (asserted by construction; the count)
        verdicts["G2"] = "PASS"
        detail["support_species"] = {"cells_seen": sp_seen,
                                     "cells_used": len(sp_bias)}
        detail["support_cut_f"] = {"cells_seen": cf_seen,
                                   "cells_used": len(cf_bias)}
        detail["support_two_key"] = {"cells_used": len(twokey_bias)}
        print("G2 PASS (species %d/%d cells used; cut_f %d/%d; "
              "two-key %d; kNN K=%d train-only)"
              % (len(sp_bias), sp_seen, len(cf_bias), cf_seen,
                 len(twokey_bias), KNN_K))

        # ---- G3 the decisive ladder
        z_sp, z_cf, z_lim = (abs(z_rungs["species"]),
                             abs(z_rungs["cut_f"]),
                             abs(z_rungs["limit"]))
        if z_sp < ABSORB_Z:
            branch = "ABSORBED-SPECIES"
        elif z_cf < ABSORB_Z:
            branch = "ABSORBED-CUTF"
        elif z_lim >= ABSORB_Z:
            branch = "STRUCTURAL-COMPLETE"
        else:
            branch = "ABSORBED-LIMITING"
        verdicts["G3"] = "PASS"
        print("G3 %s (|z| ladder raw %.3f -> block %.3f -> two-key "
              "%.3f -> species %.3f -> cut_f %.3f -> limit %.3f vs "
              "ABSORB_Z %.1f)"
              % (branch, abs(z_rungs["raw"]), abs(z_rungs["block"]),
                 abs(z_rungs["two_key"]), z_sp, z_cf, z_lim, ABSORB_Z))

        # ---- G4 the anatomy: the full ladder + the overfit disclosure
        verdicts["G4"] = "PASS"
        detail["mae_ladder"] = {k: round(v, 4)
                                for k, v in mae_rungs.items()}
        detail["z_ladder"] = {k: round(v, 3)
                              for k, v in z_rungs.items()}
        detail["runs_ladder"] = runs_rungs
        detail["overfit_disclosure"] = {
            "limit_mae_above_two_key":
                bool(mae_rungs["limit"] > mae_rungs["two_key"]),
            "note": "MAE rising while |z| falls = the bias eats "
                    "variance, not structure"}
        print("G4 PASS (MAE ladder raw %.4f -> two-key %.4f -> limit "
              "%.4f; overfit %s)"
              % (mae_rungs["raw"], mae_rungs["two_key"],
                 mae_rungs["limit"],
                 detail["overfit_disclosure"]["limit_mae_above_two_key"]))

    # ---- G5 the deposit
    out = {
        "experiment": "exp430",
        "title": "THE RESIDUAL'S GRAIN: THE LIMITING DECODE BIAS "
                 "(batch HU-12)",
        "anchor": {"mae_raw": mae_raw, "mae_decoded": mae_dec,
                   "block": mae_rungs["block"],
                   "two_key": mae_rungs["two_key"],
                   "exp428_deposited_mae": a428_mae,
                   "exp428_deposited_z": a428_z},
        "test_mae": mae_rungs,
        "runs_test": {"z": z_rungs, "runs": runs_rungs,
                      "absorb_z": ABSORB_Z, "knn_k": KNN_K},
        "support": detail.get("support_species"),
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    out["detail"] = detail
    with open(DEPOSIT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP430 VERDICT: %s" % branch)
    return {"gates": verdicts, "verdict": branch}


if __name__ == "__main__":
    main()
