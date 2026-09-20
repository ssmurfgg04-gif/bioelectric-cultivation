#!/usr/bin/env python3
"""exp297 — THE CARRIER'S DOSE-RESPONSE ON THE NEW SITES: DO THE THREE
NEW CARRIERS PLATEAU LIKE CTX? (batch 51; ledger L280's registered
next (a) — exp296 landed CARRIER-GENERAL: three of the four dormant
channels' history forms carry at the plateau dose g=1.0 (GJ-HIST
-0.2722 mV 12/12, STR-HIST -5.0706 mV 10/12, AP-HIST -0.3550 mV
12/12; CA2-HIST honestly inert). exp292/exp295 mapped the ctx site's
dose face: dose-peaked at g ~ 1.0, PEAK-FLAT (a plateau across
{0.75, 1.0, 1.25}, easing by 1.5, reversing past 1.25 on the exp292
ladder). THE OPEN QUESTION: does each NEW site's improvement hold the
same dose geometry — a plateau around 1.0, monotone-rising through
1.5, or a sharper peak? The str site's mean is outlier-carried (H3/H5
-3.84/-3.65) — its dose face is the most informative: if the outliers'
improvement is monotone in g, the site's structure is a genuine dose
axis; if it peaks sharply, the str site rides the same self-sourced
optimum as ctx.)

THE ARMS (the three carrying sites' landed exp296 forms re-run on the
pre-named dose ladder; ZERO new knobs — the forms are exp296's landed
bodies bit-identical, the dose is the only moved dial):
  GJ-HIST   — the blend at exp259's pair-junction site, ch2 carrying
              the register read (exp296's landed form VERBATIM);
  STR-HIST  — the blend at exp260's de-pairing target cells (computed,
              NOT applied), no channel vector (exp296's disclosure);
  AP-HIST   — exp264's landed sigma form with the mark read from the
              register's init face (exp296's landed form VERBATIM).
THE LADDER (pre-named): {0.25, 0.5, 1.0, 1.5} — 4 doses x 3 sites x
72 rows = 864 decodes on the shared deep-row battery (12 hosts x 3
seeds x 2 deep instances, the base medium).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each site's g=1.0 ladder rows reproduce exp296's
      deposited arm rows BIT-EXACT 72/72 (the errs + the trace shas —
      the instrument-reuse proof: the same executor, the same sites,
      the same battery); the rebuild chain asserted (exp243's shas,
      exp282's/exp287's/exp288's chain re-reads); the S* lock reads
      864 (3 sites x 4 doses x 72); the floor -60.0 throughout; the
      deposits READ-ONLY (the pre-named 12: exp243/256/272/273/282/
      287/288/289/292/293/295/296 + the 4 control deposits), sha
      before/after; the test suite green.
  G2  THE FORMS (zero-knob asserted, fail=STOP per row): the register
      faces 72/72 per (site, dose) — present + init + replay +
      complement + finite; the stream faces 72/72 per (site, dose) vs
      exp282's/exp287's deposited walk_steps/n_commits (the coupling
      is value-level only, one draw per commit at every dose); the
      site-write counts constant ACROSS SEEDS AND DOSES per
      (host, instance) — the site is a (host, instance) property, the
      dose must not move it (exp289's hist_const face, generalized);
      the gj arm's landed assert re-run per row (exp259's compensate
      VERBATIM + the conservation renorm).
  G3  THE DOSE BRANCH (pre-named, per site, evaluated in this order):
      per site the mean paired delta vs exp256's deposited substituted
      errs (arm - control; negative = improvement) at each dose;
      DOSE-INERT   iff |delta| < 0.05 mV at EVERY dose;
      PEAKED-AT-1.0 iff delta(1.0) < delta(0.5) AND delta(1.5) >
                    delta(1.0) (the reversal face — exp292's);
      PLATEAU      iff the |delta| spread among {0.5, 1.0, 1.5} <=
                    0.01 mV (exp295's PEAK-FLAT form);
      MONOTONE-RISING iff otherwise, the improvement monotone
                    increasing through 1.5 (delta(1.5) < delta(1.0) <
                    delta(0.5) — no reversal by 1.5);
      else MIXED (recorded, the honest leftover).
      Audit-only: the per-host per-dose delta tables; the per-host
      improvement counts per dose vs the 10/12 clause; the H3/H5
      deltas per site per dose; the worst-err per (site, dose) vs the
      6.0 bar; the R_max face per site at g=1.0.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named, per site): DOSE-INERT / PEAKED-AT-1.0 /
PLATEAU / MONOTONE-RISING / MIXED.

RUN: 864 decodes ~ 8-12 min — the pre-named form is the CHECKPOINT-
SPLIT EXP297_MODE=pass1 (GJ-HIST ladder, 288) | pass2 (STR-HIST
ladder, 288) | pass3 (AP-HIST ladder, 288) | merge; the in-process
default runs the whole sequence. Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp297_site_dose_ladders.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    raise NotImplementedError(
        "exp297's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
