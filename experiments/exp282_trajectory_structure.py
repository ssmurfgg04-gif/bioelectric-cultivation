#!/usr/bin/env python3
"""exp282 — THE TRAJECTORY INSTRUMENT: THE DEEP-BAND READ'S OWN WALK
STRUCTURE (batch 40; the first genuinely NEW measurement since exp269).

THE OPEN ITEM: the deep-band line closed at mia (exp278's MIA-SCALED,
rho 0.7250) with the premium's origin formally OUTSIDE the deposited
host records (exp281's CHORD-ABSENT) — but every instrument so far read
the deep-band substitution's COST as a single terminal number. The
state-carrying scoped read (execute_signed with return_state=True,
exp243's A3 path via exp256's _scoped_row_read_state) returns the final
state only; the walk's per-step structure inside execute_signed's commit
loop has never been measured. The question this module asks: does the
deep-band read's own walk — the per-step convergence of the RMS-to-target
as the walk commits cell by cell — carry the per-host exposure that the
terminal err carries (mia-scaled, premium-linked), or is the trajectory
structure ABSENT (the terminal err alone is informative, named honestly)?

THE INSTRUMENT (pre-registered, zero-knob): the substituted rows of
exp256's battery — 12 hosts x 3 seeds (1, 2, 3) x the two deep-band
instances (r-60i0/r-60i1, exp214's deep construction at the -60.0 rung)
= 72 rows at n=400 — THE SAME BATTERY, ONE FRESH RUN. Each row runs the
state-carrying scoped read with the walk's per-step convergence trace
recorded, and computes per-row trajectory summaries:

  THE TRACE (pre-named, zero-knob): ONE walk step = ONE cell commit
  (exp142's commit loop `for i, src in order:` — the walk's per-cell
  step; the 8 integration sub-steps inside a commit are NOT separately
  traced — disclosed). After each commit the replica records
  rms_k = sqrt(mean((V_k - T)^2)) over the FULL n=400 cell frame
  (pattern_error's own convention, mV) — the trace is the S-vector
  [rms_0 .. rms_{S-1}], S = the walk's commit count. The settle run
  after the walk (execute_signed's trailing c.run(15.0)) is NOT part of
  the walk — the trace ends at the walk's last commit (disclosed).

  THE THREE PER-ROW SUMMARIES (zero-knob):
    TA1 walk_end_rms  — the per-step RMS-to-target curve's FINAL value
         (rms_{S-1}; the walk-end RMS, pre-settle — disclosed).
    TA2 last10_slope  — the least-squares slope of the curve over the
         LAST 10% OF STEPS: W = max(2, ceil(0.10 * S)) final entries,
         numpy.polyfit(step_index, rms, 1)[0]; mV per walk-step.
    TA3 conv_step     — the CONVERGENCE POINT: the smallest step index k
         (0-based over the walk's commit sequence) where the curve first
         falls below 2x its final value (strict rms_k < 2.0 * rms_{S-1});
         asserted to exist on every row (rms_{S-1} > 0.0 asserted; then
         k = S-1 qualifies at worst).

  THE MACHINERY, DISCLOSED (the pre-named form): the trace hooks the
  walk WITHOUT modifying exp142. exp142's execute_signed records
  NOTHING per-step (read, disclosed pre-body), so the PRE-NAMED
  FALLBACK IS THE FORM: the state-carrying replica pattern — exp142's
  walk copied byte-similar into _execute_signed_traced carrying EXACTLY
  the disclosed additions (the per-step RMS read after each commit — a
  pure numpy read of the live V vs the target; the trace + step-count
  fields attached to the returned dict; the final state always carried),
  the RNG stream / dt / canon / walk order / commits untouched, called
  through exp256's _scoped_row_read_state form (the projection chain
  PN1/PN2 + TC1 + TC2 + the TC3 state-carrying call VERBATIM). The
  replica's inertness is not assumed — it is the S0 anchor below.

  THE 12-HOST TABLE: per-host MEANS of each summary over the host's 6
  substituted rows (3 seeds x 2 instances). THE REGRESSIONS: each
  summary's per-host mean against TWO targets — T_mia = mia_prod_err
  (exp273's field-table field 'exp243.classes.multi_identity_audit.
  prod_err', asserted bit-exact vs exp243's own class records) and
  T_prem = exp272's per-host ONE-ZONE PREMIUM means (asserted bit-exact
  vs exp273's field-table carry 'exp272.per_host.one_zone_premium_mean')
  — Spearman under the exp274/exp275/exp280 conventions (Pearson on
  scipy's tied-average ranks; the 12-slot frame, the H0==H1 echo
  carried; the ties census recorded; the single-predictor rank R2
  audit-only).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY (sha-asserted, READ-ONLY): the 12 base
      adjacencies rebuilt per the exp269/exp280 precedent (graph_path
      at the chain class's n=400 call site for H0/H1 — H0 echoes H1
      bit-exactly, asserted; small_world(n, 0.10, deposited
      rewire_seed) for H2-H11), every rebuild bit-asserted against
      exp243's records: sha256(|A| as float64) == base_sha256 12/12;
      the upper-triangle edge count == edges_base 12/12; the exp208
      classify CANON-BOUNDARY count == n_boundary_cells_base 12/12,
      dual-carried vs exp272's per_host AND exp273's field table; the
      canon identity labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12.
      The two deep-row targets rebuilt per exp256's build_rows deep
      construction (exp214's deep form VERBATIM): row_target_sha256 ==
      exp256's deposited substituted instance records 72/72, and the
      base medium sha == exp243's base_sha256 == the deposited instance
      medium_sha256 72/72; f_max recomputed == f_max_base 12/12. The
      source deposits (exp243, exp256, exp272, exp273) READ-ONLY:
      sha-recorded BEFORE any read, byte-unchanged after the work.
  G2  THE TRACE'S INTEGRITY (completeness + THE S0 ANCHOR): one fresh
      run of the 72 substituted rows through the state-carrying traced
      replica; TRACE COMPLETENESS — every row's trace covers the walk's
      FULL step count (len(trace) == the replica's recorded walk commit
      count, 72/72) with every entry finite; the per-row A3
      state-convention assert (round(err_exact, 2) == round(err, 2),
      exp243's convention) 72/72; THE S0 ANCHOR — every row's final err
      reproduces exp256's DEPOSITED substituted instance err BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags carried 72/72) — the trace form is inert on the deposited
      machine, the recording provably perturbed nothing.
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      TRAJECTORY-CARRIED iff >= 1 of the SIX signed Spearman rhos
      (3 summaries TA1/TA2/TA3 x 2 targets T_mia/T_prem) reaches
      >= 0.5 (the SIGNED house bar — positive); else TRAJECTORY-ABSENT
      (the walk's trajectory structure carries nothing at the bar —
      named honestly). THE ABS VARIANT, pre-named: max |rho| over the
      same six recorded audit-only — a crossing at |rho| >= 0.5 with a
      NEGATIVE sign is the ANTI-ALIGNED face (the summary runs OPPOSITE
      the exposure); it is NAMED in the deposit and the verdict per
      summary x target, NEVER gating. The rank R2s and the outlier
      (H3/H5) vs cluster summary margins audit-only.
  G4  THE DISCIPLINE: deterministic — the fresh run executes TWICE, the
      two passes' row payloads (errs, traces, summaries, table,
      regressions) BIT-IDENTICAL; no wall-clock fields (recursive key
      scan + serialized-blob scan); the docstring + header pinned to
      this pre-registration commit, asserted at entry AND exit; the
      source deposits byte-unchanged; NEURAL_SPEC_MIN == -60.0 asserted
      at exit (the floor restored post-import — exp218's disclosed
      exp169-import discipline, the -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): TRAJECTORY-CARRIED / TRAJECTORY-ABSENT.

RUN: the deterministic sha-asserted rebuild (seconds) + the fresh
72-row traced battery run TWICE (G4's two-pass clause; 72 decodes per
pass), foreground ~3-5 min. If a pass cannot finish inside the 570 s
foreground cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE pass per
invocation (env EXP282_PASS=1|2 caches that pass's row payload) and the
PRE-NAMED MERGE (env EXP282_MERGE=1) compares the two cached payloads
BIT-EXACT and writes the deposit — the merge never recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp282_trajectory_structure.json")


def main() -> dict:
    raise NotImplementedError(
        "the body lands under the body-only discipline; this "
        "pre-registration commit carries the docstring + header + "
        "stub ONLY (gates fixed before any body exists)")


if __name__ == "__main__":
    main()
