#!/usr/bin/env python3
"""exp290 — THE STRESS-TIMING SPLIT: WRITE-TIME VS READ-TIME IONIC
STRESS ON THE COMMIT MACHINERY (batch 47; ledger L267's registered
next (c) — Tazumi 2026 (APA): salt exposure disrupts memory RETRIEVAL
in D. japonica while leaving storage intact — the timing split. The
stack analog is runnable as-is on the commit-noise machinery: the
ionic exposure IS the depolarized floor (the exp169 pin discipline's
own -35.0 reader-line form), and the machinery has a clean write/
read boundary — the WALK (the commits) is the storage face, the
SETTLE+DECODE is the retrieval face.)

THE ARMS (pre-named, zero new knobs — the floor values are the
machinery's own registered constants): the 72-row substituted battery
(exp256's, 12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, the
exp287/exp288 traced replica form at the production budget 8) run
under three floor states:
  A0  ANCHOR — the floor -60.0 everywhere (the production form; the
      errs reproduce exp256's deposited substituted errs BIT-EXACT
      72/72 — the S0 anchor, fail=STOP);
  A1  WRITE-STRESS — the floor pinned to -35.0 DURING THE WALK ONLY
      (from the encode window's start through the last commit), the
      floor restored to -60.0 before the settle (c.run(15.0)) and the
      decode (the settle and the read run at the production floor);
  A2  READ-STRESS — the walk at the production floor -60.0, the floor
      pinned to -35.0 for the SETTLE ONLY, restored to -60.0 before
      the decode (the read itself runs at the production floor — the
      stress is the consolidation dynamics, the retrieval face).
The pin discipline is exp169's disclosed form (the module attribute
_neural_spec_min read at step time; the restore asserted); exp142 and
the core are NOT modified — the arms set the module attribute around
the calls exactly as the reader-line pin does, disclosed.

THE READ (zero knobs): per arm the 72-row errs (the machinery's
native 2-dp convention) + err_exact; per arm the mean paired delta
vs the A0 anchor over the 72 rows (the same rows — the paired
structure); the branch pre-named:
  RETRIEVAL-SIDE  iff mean_delta(A2) < mean_delta(A1) - 0.05 (the
      read-arm degrades MORE than the write-arm by the pre-named 0.05
      mV margin — Tazumi's direction: the retrieval is the sensitive
      face);
  STORAGE-SIDE    iff mean_delta(A1) < mean_delta(A2) - 0.05;
  SYMMETRIC-INERT otherwise (the two faces indistinguishable at the
      machinery's resolution — an honest null).
Audit-only: the per-row paired delta table per arm, the per-host mean
deltas, the outliers H3/H5's deltas (the exp273 pre-name), the
worst-err per arm vs the 6.0 bar (unchanged), the commit censuses per
arm (the spec/canon/parent tags — the floor's effect on the (e)
branch, disclosed), the trace shas per arm (the walks differ across
arms by construction — the anchor is the A0 arm only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: A0's errs reproduce exp256's deposited substituted
      errs BIT-EXACT 72/72 (the verified flags 72/72) AND exp282's
      walk_end_rms bit-exact (the trace sha256 72/72); the floor
      asserts: the floor reads -60.0 at the encode start per row in
      A0/A2 and -35.0 during the walk in A1 (recorded per row,
      asserted); the source deposits READ-ONLY (exp243/256/272/273/
      282/287/288 — 7 deposits, the sha-recorded before/after form).
  G2  THE ARMS' INTEGRITY (zero-knob asserted, fail=STOP per row):
      every row's errs finite; the A3 convention (round(err_exact, 2)
      == the reported err) 72/72 per arm; the trace lengths ==
      walk_steps 72/72 per arm; the S* lock reads 216 (3 arms x 72);
      the commit counts == walk_steps per arm 72/72; the pin restore
      asserted at the settle boundary per row (the floor reads -60.0
      at the settle start in A1, -35.0 in A2, -60.0 at the decode in
      both — recorded, fail=STOP).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars above):
      the paired deltas over the 72 rows per arm; RETRIEVAL-SIDE /
      STORAGE-SIDE / SYMMETRIC-INERT by the 0.05 mV margin form.
  G4  THE DISCIPLINE: deterministic (the arms are pure floor-state
      schedules over the same seed stream — the in-process form runs
      the 3 arms sequentially, 216 decodes ~ 3-4 min, under the 570 s
      cap; the checkpoint-split EXP290_MODE=pass1|pass2 + merge is
      the pre-named alternative); no wall-clock fields; the docstring
      + header pinned to this pre-registration commit, asserted at
      entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): RETRIEVAL-SIDE / STORAGE-SIDE /
SYMMETRIC-INERT.

RUN: 216 decodes ~ 3-4 min foreground (in-process), or the
checkpoint-split form. Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp290_stress_timing.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp290's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
