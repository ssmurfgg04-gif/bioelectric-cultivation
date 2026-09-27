#!/usr/bin/env python3
"""exp415 — THE MAE 0.290 RESIDUAL: DATA-SIDE OR MODEL-SIDE? (batch
HU-10; handoff Test 4, the honest-scrutiny face). L73 landed the
corpus decode at decoded MAE 0.290 (raw 0.365 -> 0.371 across the
axis repairs) via exp91's dose-axis + amplitude axis + the exclusion
rules. The honest-scrutiny question: the remaining error is
attributed to data-side limits (missing/unknowable drug
concentrations); is that attribution TRUE, or is a model-side gap
hiding behind it? Two probes, one arithmetic, zero knobs:
  P-DATA  — the missing-concentration band: every corpus row with an
            imputed/unknown dose is resampled WITHIN its pre-named
            plausible range (the corpus's own observed min-max per
            drug class — nothing invented), the decode re-run,
            N = 200 resamples; the MAE band [min, max] and its width
            W_data. W_data is what the data's own uncertainty can
            explain.
  P-MODEL — the ablation ladder: one-at-a-time disable each known
            pipeline mechanism (the decoded axis -> raw; the
            amplitude axis off; the dose-axis/threshold structure
            off; each exclusion rule dropped, one per run), the
            DeltaMAE per ablation; A_max = the largest |DeltaMAE|.
  P-STRUCT— the residual-sign runs test on the per-row residual
            sequence (systematic sign structure = a NAMED model-side
            gap, not noise).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: the loaded pipeline reproduces the deposited
      decoded MAE 0.290 on the committed corpus (+/- 0.005 tolerance
      — float reproducibility, disclosed if the corpus gained rows
      since L73; fail=STOP on a larger gap).
  G2  THE BAND: W_data deposited with the per-drug-class ranges used;
      the 200 resamples' MAE distribution deposited (min/median/max).
  G3  THE LADDER: every ablation's DeltaMAE deposited with its named
      mechanism; A_max = max |DeltaMAE|.
  G4  THE VERDICT ARITHMETIC: DATA-SIDE-DOMINANT iff W_data >= 2 x
      A_max; MODEL-SIDE-DOMINANT iff A_max >= 2 x W_data; else
      MIXED. P-STRUCT separately: if the runs test rejects (z > 2),
      the sign structure is deposited AS a named model-side gap
      regardless of the G4 branch.
  G5  THE DEPOSIT: the band, the ladder, the runs test, gates +
      branch as results/exp415_mae_decomposition.json (fail=STOP).

BRANCH LATTICE (pre-named): DATA-SIDE-DOMINANT (the honest-scrutiny
attribution CONFIRMED — the 29% is the data's own uncertainty);
MODEL-SIDE-DOMINANT (the attribution was a shield — the named gap
becomes the top repair target); MIXED (both stories carry part of the
29%). Any G4 branch + a rejected runs test = the gap is NAMED in the
deposit either way.

THE HONEST STAKES: MAE 0.290 has been quoted as the model's ceiling
with the residue blamed on missing concentrations. This experiment
either pays that claim out in numbers or names what the model is
missing. Both outcomes are deposits; only silence would be a failure.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
N_RESAMPLES = 200
RUNS_TEST_Z = 2.0
ANCHOR_TOL = 0.005
DEPOSIT = os.path.join(ROOT, "results", "exp415_mae_decomposition.json")


def main() -> dict:
    raise NotImplementedError(
        "exp415 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
