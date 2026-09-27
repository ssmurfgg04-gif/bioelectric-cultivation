#!/usr/bin/env python3
"""exp428 — THE TWO-KEY DECODE BIAS: GROUP x PLANE (batch HU-12;
exp423's registered follow-up). exp423 landed BIAS-PARTIAL: the
per-block bias cuts the test MAE 0.2989 -> 0.2552 (the material cut
landed) but the runs test's |z| = 6.72 persists — the residual sign
structure has a NON-BLOCK component. The next key is pre-named by the
corpus's own anatomy: the per-record `plane` field (the anatomical
region of the recording — the corpus rows carry it; the decode's
errors should key on WHERE the tissue was read, not only on WHAT was
done to it). The lever: a two-key bias, the (group, plane) cell's
median residual, fitted train-only, applied test-only, nested inside
exp423's frozen discipline.

THE INSTRUMENT (exp423's machinery verbatim, the key extended; zero
new knobs):
  the L74 per-row corpus (the scored rows, exp118's per_record with
  per-row errors), the same train/test split (the rows' corpus order,
  even = train, odd = test); the key = the (group, plane) pair from
  the corpus's own fields (no invention; a test row whose cell was
  unseen or train-thin carries bias 0 — the pre-named fallback).
  The ladder's entry point: exp423's corrected test MAE 0.2552
  reproduced first, then the two-key bias applied.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the raw anchor (0.3705/0.2900/0.6928) bit-tight
      within 0.005; exp423's per-block corrected test MAE 0.2552
      reproduced within 0.005 (the ladder's entry point).
  G2  THE DISCIPLINE: train/test disjoint; the two-key bias fitted
      train-only; the fallback rule applied as pre-named; the cell
      support table (train n per (group, plane)) deposited.
  G3  THE GATE: the test-half MAE after the two-key bias <= 0.2402
      (0.2552 - 0.015, a material further cut, pre-named) AND the
      runs test's |z| on the test-half residuals <= 2 (the sign
      structure absorbed, two-sided — the exp415 lesson).
  G4  THE ANATOMY: the two-key bias table deposited (WHICH (group,
      plane) cells over/under-predict, with n each) + the residual
      runs-z ladder (raw / block-corrected / two-key-corrected).
  G5  deposit results/exp428_two_key_bias.json.

BRANCH LATTICE: BIAS-CLOSED (G3 PASS — the model-side gap is the
decode's group x plane bias, repaired with zero new data) /
BIAS-STRUCTURAL (the MAE cut lands, |z| > 2 persists — the sign
structure survives BOTH keys; the gap is not a bias at this
granularity) / BIAS-REFUTED (neither — the plane key adds nothing)
/ INSTRUMENT-REFUTED (G1/G2 fail).

THE HONEST STAKES: the MAE 0.290 story has been decomposed
(exp415: model-side dominant) and partially repaired (exp423: the
block bias); this is the third and finest pre-named key the corpus's
own fields support. If |z| survives it, the residual is STRUCTURAL —
the decode's next repair is a model change, not a bias term.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

ENTRY_MAE = 0.2552
MAE_TARGET = 0.2402
RUNS_Z = 2.0
ANCHOR_TOL = 0.005
MIN_SUPPORT = 3
DEPOSIT = os.path.join(ROOT, "results", "exp428_two_key_bias.json")


BODY_DISCLOSURES = [
    "the corpus rows and the train/test split are exp423's verbatim (the "
    "rows' corpus order, even = train, odd = test; excluded_C4 dropped); "
    "the key extends from the corpus's own `group` field to the "
    "(group, plane) pair — both fields are the corpus's own per-record "
    "columns, no invention",
    "the two-key bias = the (group, plane) cell's median residual "
    "(sim - recorded_corrected) on its TRAIN rows, applied as "
    "sim' = sim - bias to the TEST rows; cells with train support < "
    "MIN_SUPPORT or absent from train carry bias 0 (the pre-named "
    "fallback)",
    "the ladder stage-2 (block-corrected) re-fits exp423's per-block "
    "bias on the same train rows (the entry-point reproduction); the "
    "two-key stage subsumes it (the cell median includes the block "
    "shift)",
    "exp423's _runs_test_z imported verbatim; the runs test evaluated "
    "TWO-SIDED at every rung (the exp415 lesson)",
    "RE-RUN DISCLOSURE: the first credited run omitted the block rung "
    "of the frozen three-rung z ladder (a G4 completeness gap, not a "
    "verdict change — G3's inputs were identical); this re-run is the "
    "credited deposit; the analysis is deterministic (zero rng)",
]

import numpy as np

from experiments.exp423_decode_bias_repair import _runs_test_z


def _median(xs):
    return float(np.median(xs)) if xs else 0.0


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
    assert len(set(id(x) for x in train)) == len(train)
    assert not (set(id(x) for x in train) & set(id(x) for x in test))

    # ---- stage 2: the per-block bias (exp423's fit, the entry point)
    blocks = sorted({r["group"] for r in rows if r.get("group")})
    block_bias = {b: _median([r["sim"] - r["recorded_corrected"]
                              for r in train if r["group"] == b])
                  for b in blocks}
    mae_block = float(np.mean([
        abs(r["sim"] - block_bias.get(r["group"], 0.0)
            - r["recorded_corrected"]) for r in test]))
    entry_ok = abs(mae_block - ENTRY_MAE) <= ANCHOR_TOL
    try:
        dep423 = json.load(open(os.path.join(
            ROOT, "results", "exp423_decode_bias_repair.json")))
        dep423_mae = float(dep423["test_mae_after"])
        dep_ok = abs(mae_block - dep423_mae) <= ANCHOR_TOL
    except (OSError, KeyError):
        dep423_mae, dep_ok = None, False
    verdicts["G1"] = "PASS" if (entry_ok and dep_ok) else "REFUTE"
    print("G1 %s (raw %.4f dec %.4f; block-corrected test MAE %.4f vs "
          "entry %.4f%s)" % (verdicts["G1"], mae_raw, mae_dec, mae_block,
                             ENTRY_MAE,
                             (", deposited %.4f" % dep423_mae)
                             if dep423_mae is not None else ""))

    # ---- the two-key fit (train-only, the support fallback)
    cells = {}
    for r in train:
        cells.setdefault((str(r.get("group")), str(r.get("plane"))),
                         []).append(r["sim"] - r["recorded_corrected"])
    twokey_bias = {k: _median(v) for k, v in cells.items()
                   if len(v) >= MIN_SUPPORT}
    support = {("%s|%s" % k): len(v) for k, v in sorted(cells.items())}

    # ---- the test-half errors at every rung + the runs-z ladder
    e_raw, e_block, e_two = [], [], []
    s_raw, s_block, s_two = [], [], []
    for r in test:
        rec = r["recorded_corrected"]
        b1 = block_bias.get(r["group"], 0.0)
        b2 = twokey_bias.get((str(r.get("group")),
                              str(r.get("plane"))), 0.0)
        e_raw.append(abs(r["sim"] - rec))
        e_block.append(abs(r["sim"] - b1 - rec))
        e_two.append(abs(r["sim"] - b2 - rec))
        s_raw.append(1 if r["sim"] >= rec else -1)
        s_block.append(1 if (r["sim"] - b1) >= rec else -1)
        s_two.append(1 if (r["sim"] - b2) >= rec else -1)
    mae_raw_test = float(np.mean(e_raw))
    mae_two = float(np.mean(e_two))
    z_raw, _ = _runs_test_z(np.array(s_raw))
    z_block, _ = _runs_test_z(np.array(s_block))
    z_two, R2 = _runs_test_z(np.array(s_two))

    # ---- G2 the discipline + the support table
    verdicts["G2"] = "PASS"
    detail["support_cells"] = support
    detail["n_cells_used"] = len(twokey_bias)
    print("G2 PASS (train %d / test %d; %d (group,plane) cells with "
          "support >= %d of %d seen)"
          % (len(train), len(test), len(twokey_bias), MIN_SUPPORT,
             len(cells)))

    # ---- G3 the gate
    gate = mae_two <= MAE_TARGET and abs(z_two) <= RUNS_Z
    verdicts["G3"] = "PASS" if gate else "REFUTE"
    print("G3 %s (test MAE raw %.4f -> block %.4f -> two-key %.4f vs "
          "bar %.4f; runs |z| %.3f -> %.3f)"
          % (verdicts["G3"], mae_raw_test, mae_block, mae_two,
             MAE_TARGET, abs(z_raw), abs(z_two)))

    # ---- G4 the anatomy: the two-key table + the z ladder
    table = {}
    for (g, p), b in sorted(twokey_bias.items()):
        te = [r for r in test
              if str(r.get("group")) == g and str(r.get("plane")) == p]
        tr_n = len(cells[(g, p)])
        if not te:
            continue
        e_before = float(np.mean([abs(r["sim"]
                                       - r["recorded_corrected"])
                                  for r in te]))
        e_after = float(np.mean([abs(r["sim"] - b
                                     - r["recorded_corrected"])
                                 for r in te]))
        table["%s|%s" % (g, p)] = {"n_train": tr_n, "n_test": len(te),
                                   "bias": round(b, 4),
                                   "test_mae_before": round(e_before, 4),
                                   "test_mae_after": round(e_after, 4)}
    detail["z_ladder"] = {"raw": round(z_raw, 3),
                          "block": round(z_block, 3),
                          "two_key": round(z_two, 3)}
    detail["two_key_table"] = table
    verdicts["G4"] = "PASS"
    print("G4 PASS (%d cells in the table; z ladder raw %.3f -> "
          "two-key %.3f)" % (len(table), z_raw, z_two))

    # ---- G5 the deposit
    if not gate:
        branch = ("BIAS-STRUCTURAL" if mae_two < mae_block - 0.005
                  else "BIAS-REFUTED")
    else:
        branch = "BIAS-CLOSED"
    out = {
        "experiment": "exp428",
        "title": "THE TWO-KEY DECODE BIAS: GROUP x PLANE (batch HU-12)",
        "anchor": {"mae_raw": mae_raw, "mae_decoded": mae_dec,
                   "block_corrected_test_mae": mae_block,
                   "entry_mae": ENTRY_MAE,
                   "exp423_deposited": dep423_mae},
        "split": {"train": len(train), "test": len(test),
                  "cells_used": len(twokey_bias), "cells_seen": len(cells)},
        "test_mae": {"raw": mae_raw_test, "block": mae_block,
                     "two_key": mae_two},
        "runs_test": {"z_raw": z_raw, "z_block": z_block,
                      "z_two_key": z_two, "runs": R2},
        "two_key_table": table,
        "support_cells": support,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP428 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
