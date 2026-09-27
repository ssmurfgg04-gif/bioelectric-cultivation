#!/usr/bin/env python3
"""exp423 — THE PER-BLOCK DECODE BIAS: THE NAMED GAP TESTED (batch
HU-11; ledger L311's named repair — the runs test fired |z| = 17.21,
the residual signs systematically clustered: the model over/under-
predicts in blocks; the decode correction axis carries 4x the data's
own uncertainty). HYPOTHESIS: a per-block bias term (the decode's
correction fitted per corpus block — the arm/protocol family) absorbs
the sign structure and cuts the decoded MAE materially below 0.290
WITHOUT new data.

THE INSTRUMENT (the L74 per-row corpus, 905 scored rows, the
train/test discipline frozen here): the blocks = the corpus's own
group field (cutting / gj_block / ion_channel / morphogen / other_rnai
/ innexin); per block, the median residual (sim - recorded_corrected)
fitted on the TRAIN half (the rows' even indices) and applied to the
TEST half (the odd indices); the corrected-corrected MAE vs 0.290.
PRE-REGISTERED GATES:
  G1  the anchor reproduced (0.3705/0.2900/0.6928 bit-tight); the
      blocks enumerated from the corpus's own field (no invention).
  G2  the holdout discipline asserted (train/test disjoint; the bias
      fitted train-only).
  G3  THE GATE: the test-half MAE after the per-block bias <= 0.290 -
      0.02 (a material cut, pre-named) AND the runs test's |z| on the
      test-half residuals <= 2 (the sign structure absorbed).
  G4  the per-block bias table deposited (the gap's anatomy: WHICH
      blocks over/under-predict, with n each).
  G5  deposit results/exp423_decode_bias_repair.json.
BRANCH: BIAS-CONFIRMED (G3 PASS — the model-side gap is the decode's
block bias, repaired for 0.02+ MAE with zero new data) /
BIAS-PARTIAL (the MAE cut lands, the sign structure persists) /
BIAS-REFUTED (neither — the clustering is not block-structured; the
gap stays open with the block table deposited as the negative).
THE HONEST STAKES: L311 named the gap; THIS experiment either repairs
it with zero new data or kills the block hypothesis — both deposits
sharpen the corpus's next move.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

MAE_TARGET = 0.27      # 0.290 - 0.02
RUNS_Z = 2.0
DEPOSIT = os.path.join(ROOT, "results", "exp423_decode_bias_repair.json")


def main() -> dict:
    raise NotImplementedError(
        "exp423 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
