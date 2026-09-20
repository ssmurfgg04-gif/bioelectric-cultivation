#!/usr/bin/env python3
"""exp299 — THE CARRIER AT THE SUB-SATURATION FACES: DO THE TWO FORMS
DIFFER WHERE THE SIGMA LEAVES NOISE? (batch 53; ledger L282's
registered next (a) — exp298 landed ADDITIVE: at g=1.0 the union of
the three carrying faces equals the best single (apop) BIT-EXACT,
because at saturation (sigma = 0) the sigma form and the blend form
both land the commit on the spec install — the faces are one
mechanism at nested site granularities. THE OPEN QUESTION: at g < 1
the two forms genuinely DIFFER — the blend re-asserts the register
value (written = (1-g)*theta_new + g*hist_i, the full pull at any g),
while the sigma form only SHRINKS the noise (sigma = (1-g)*NOISE, the
draw still scattered around commit_base). At g=0.5: does the blend
face add value on top of the sigma face (the union beats the best
single — the mechanisms differ), or does the spec-install
re-assertion still subsume (ADDITIVE at every dose — the mechanism is
one at all doses)?)

THE ARMS (the exp298 landed composition VERBATIM, the dose moved to
the pre-named sub-saturation point):
  faces=("ctx",)  — MUST reproduce exp289's deposited g_ctx=0.5 grid
                    rows BIT-EXACT 72/72 (the ctx form's own dose
                    ladder landed there — the anchor);
  faces=("gj",)   — MUST reproduce exp297's deposited gj ladder rows
                    at g=0.5 BIT-EXACT 72/72;
  faces=("apop",) — MUST reproduce exp297's deposited apop ladder
                    rows at g=0.5 BIT-EXACT 72/72;
  faces=all three — THE UNION AT 0.5: 72 fresh rows.
4 arms x 72 rows = 288 decodes on the shared deep-row battery at
g=0.5.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the three single-face arms reproduce their
      deposited g=0.5 rows BIT-EXACT 72/72 each (the errs + the trace
      shas; the sources: exp289's grid rows for ctx, exp297's ladder
      rows for gj/apop); the rebuild chain asserted; the S* lock
      reads 288; the floor -60.0; the deposits READ-ONLY (the
      pre-named 12 + the 4 control deposits), sha before/after; the
      test suite green.
  G2  THE FORMS: the register faces 72/72 per arm; the stream faces
      72/72 per arm vs exp282's/exp287's deposited records; the
      site-write counts constant across seeds per (host, instance);
      the gj landed assert re-run per row.
  G3  THE DECOMPOSITION BRANCH (pre-named): the union's mean paired
      delta vs exp256's dormant baseline compared with the BEST
      SINGLE's at g=0.5:
      SUPER-ADDITIVE  iff delta(union) <= delta(best single) - 0.05
                      (the blend adds value where the sigma leaves
                      noise — the mechanisms genuinely differ);
      ADDITIVE        iff |delta(union) - delta(best single)| < 0.05
                      (the re-assertion subsumes at every dose);
      INTERFERING     iff delta(union) > delta(best single) + 0.05.
      Audit-only: the per-host delta tables, the worst-err vs the
      6.0 bar, the H3/H5 deltas, the R_max face.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): SUPER-ADDITIVE / ADDITIVE / INTERFERING.

RUN: 288 decodes ~ 3-5 min — the in-process default (EXP298_MODE's
single-battery form).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp299_subsaturation_faces.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp299's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
