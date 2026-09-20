#!/usr/bin/env python3
"""exp298 — THE COMBINED-SITE CARRIER: WHAT DOES THE UNION OF THE
CARRYING FACES DO? (batch 52; ledger L281's registered next (a) —
exp296 landed CARRIER-GENERAL (three carrying sites at g=1.0) and
exp297 fixed the absolute dose faces (gj PEAKED-AT-1.0 at -0.2707,
apop CARRYING-MONOTONE to -0.3550 at saturation, str dose-inert vs
the absolute baseline — the control-dependence decomposition). THE
OPEN ARCHITECTURAL QUESTION: the three carrying faces (the ctx blend
at the canon-boundary cells, the gj blend at the pair-junction cells,
the apop sigma relaxation at the register-face marked cells) were
tested SEPARATELY. The sites are NOT disjoint — the apop mark's band
clause covers the whole walked region (the boundary and junction
cells included), and the extreme-decile clause adds the deep-value
cells. What does the UNION do: super-additive (the faces compound),
additive (the best single dominates), or interfering (the faces
fight over the same commits)?)

THE ARMS (the exp296 landed forms VERBATIM, composed on ONE walk via
the faces parameter — the anchor ladder proves the composition
bit-exact, then the union runs once):
  faces=("ctx",)  — exp289's blend at the canon-boundary cells; MUST
                    reproduce exp296's deposited ctx rows BIT-EXACT
                    72/72 (the anchor ladder, G1);
  faces=("gj",)   — the blend at exp259's pair-junction site, ch2
                    carrying the register read; MUST reproduce exp296's
                    deposited gj rows BIT-EXACT 72/72;
  faces=("apop",) — exp264's landed sigma form with the mark read from
                    the register's init face; MUST reproduce exp296's
                    deposited apop rows BIT-EXACT 72/72;
  faces=all three — THE UNION: the sigma face first (the draw's scale),
                    then the blends (the write's value), the channel
                    writes per face preserved; 72 fresh rows.
4 arms x 72 rows = 288 decodes on the shared deep-row battery at the
plateau dose g=1.0.

THE COUPLING ORDER (fixed here, before any union row): at the commit
of each walked cell — (1) the sigma face: if the cell is marked
(the register-face mark, exp296's), sigma = COMMIT_NOISE * (1 - g)
and ch6 carries 1.0; (2) the draw: theta_new = commit_base +
rng.normal(0, sigma) — ONE draw per commit (the stream discipline);
(3) the blend faces: if the cell is a canon-boundary cell (the ctx
face) or a pair-junction cell (the gj face, exp259's site), written =
(1 - g) * theta_new + g * phi_history[i], ch2 carrying the register
read at the gj cells. At a cell carrying BOTH blend faces the blend
is applied ONCE (the same value — the sites' blend forms are
identical; the overlap is recorded, not doubled). At a marked cell
outside both blend sites the sigma face acts alone; at a blend-site
cell outside the mark the blend acts alone.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each single-face arm reproduces exp296's deposited
      rows BIT-EXACT 72/72 (the errs + the trace shas — the
      composition's fidelity proof: the faces parameter changes
      nothing when a face runs alone); the rebuild chain asserted;
      the S* lock reads 288 (4 arms x 72); the floor -60.0; the
      deposits READ-ONLY (the pre-named 12 + the 4 control deposits),
      sha before/after; the test suite green.
  G2  THE FORMS: the register faces 72/72 per arm (present + init +
      replay + complement + finite); the stream faces 72/72 per arm
      vs exp282's/exp287's deposited walk_steps/n_commits; the
      site-write counts constant across seeds per (host, instance)
      and the per-row overlap audit recorded (the boundary ∩ mark,
      the junction ∩ mark, the blend-site ∩ mark counts); the gj
      landed assert re-run per row.
  G3  THE ADDITIVITY BRANCH (pre-named): the union's mean paired
      delta vs exp256's dormant baseline (the honest absolute
      control, exp297's lesson) compared with the BEST SINGLE's mean
      paired delta (the min of the three singles' deltas):
      SUPER-ADDITIVE  iff delta(union) <= delta(best single) - 0.05
                      (the union beats the best single by >= 0.05 mV);
      ADDITIVE        iff |delta(union) - delta(best single)| < 0.05;
      INTERFERING     iff delta(union) > delta(best single) + 0.05
                      (the faces fight);
      each with the per-host improvement count recorded (the 10/12
      clause as the audit). Audit-only: the per-host delta tables per
      arm, the worst-err per arm vs the 6.0 bar, the H3/H5 deltas,
      the R_max face per arm, the overlap census.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): SUPER-ADDITIVE / ADDITIVE / INTERFERING.

RUN: 288 decodes ~ 3-5 min — the in-process default runs the whole
sequence (the anchor ladder + the union); EXP298_MODE=all is the
pre-named form.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp298_combined_site_carrier.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp298's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
