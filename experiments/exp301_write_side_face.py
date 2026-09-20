#!/usr/bin/env python3
"""exp301 — THE CARRIER'S WRITE-SIDE FACE: DOES THE COMPOSED CARRIER
CHANGE WHAT THE PROGRAM COMMITS? (batch 55; ledger L284's registered
next (a) — batches 50-54 landed the carrier's complete read-side
picture: the commit-history register's carrier is the spec-install
re-assertion (exp298's ADDITIVE subsumption at saturation), the
improvement monotone in the site coverage (exp300's MONOTONE-TO-1.0
union ladder), the two mechanisms composing super-additively below
saturation (exp299). THE OPEN QUESTION: every read-side verdict so
far measured the decode's ERR. The WRITE-SIDE face asks the program's
own question: what does the carrier do to the COMMIT SEQUENCE itself
— the program's output? exp287's commit-layer face (the per-row
commit_seq_sha256, the cvt_rms = the commit-vs-target RMS, the
n_commits, the sc_rms) is the instrument. THE PRE-NAMED READ:
(1) the dormant face anchor: the fresh dormant walk reproduces
exp287's deposited commit layer BIT-EXACT (the machinery's anchor,
already proven in exp289's/exp296's G1 faces); (2) the carrier's
faces: the union walks at the composed optimum g=1.0 — the commit
digests MUST differ from the dormant face (the carrier re-asserts the
spec install at the armed cells — the write values change) AND the
register's replay equality says the register IS the commit sequence;
(3) the cvt face: the carrier's commit-vs-target RMS DROPS (the
commits land closer to the target — the write-side counterpart of
the read-side improvement); (4) the census face: the spec/canon/
parent source tags' counts are dose- and carrier-INVARIANT (the
carrier changes the VALUES, not the branch chain's structure).)

THE ARMS (72 rows each on the shared deep-row battery):
  DORMANT   — g=0.0 (the carrier's zero face): MUST reproduce
              exp287's deposited commit layer BIT-EXACT 72/72 (the
              commit_seq_sha256 + the cvt_rms + the n_commits + the
              sc_rms) — G1's anchor;
  UNION-1.0 — the composed faces at the composed optimum: the fresh
              72 rows (the write-side face's subject);
  UNION-0.5 — the composed faces at the sub-saturation point: the
              fresh 72 rows (the composition's write-side face below
              saturation — where the blend re-asserts but the sigma
              leaves noise, exp299's face).
3 arms x 72 rows = 216 decodes.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: the DORMANT arm reproduces exp287's deposited
      commit layer BIT-EXACT 72/72 (the commit_seq_sha256 + the
      cvt_rms + the n_commits + the sc_rms + the errs vs exp256's
      deposited substituted errs); the rebuild chain asserted; the
      S* lock reads 216; the floor -60.0; the deposits READ-ONLY
      (the pre-named 12 + the 4 control deposits), sha before/after;
      the test suite green.
  G2  THE FORMS: the register faces 72/72 per arm (present + init +
      replay + complement + finite — the replay equality IS the
      write-side face's core: the register IS the commit sequence);
      the stream faces 72/72 per arm vs exp282's/exp287's deposited
      records (the walked count and the commit count are
      carrier-invariant); the site-write counts constant across
      seeds per (host, instance) for the union arms.
  G3  THE WRITE-SIDE BRANCH (pre-named):
      the digest face: the union arms' commit_seq_sha256 differ from
      the dormant face's on 72/72 rows (the carrier writes different
      values — the WRITE-SIDE-REAL face) or match on any row (the
      carrier is write-side-invisible on that row — the honest
      count recorded);
      the cvt face: the union arms' mean cvt_rms vs the dormant's
      (the pre-named bars: the carrier's commits land closer to the
      target iff the mean cvt drops; the drop's size recorded per
      arm; the branch WRITE-SIDE-CARRIED iff the union-1.0 mean cvt
      drop > 0.05 mV AND 10/12 hosts improve, else
      WRITE-SIDE-MARGINAL/ABSENT recorded);
      the census face (audit-only): the spec/canon/parent tag counts
      per arm (the branch chain's structure is carrier-invariant —
      the census must match the dormant's 72/72).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): WRITE-SIDE-CARRIED / WRITE-SIDE-MARGINAL /
WRITE-SIDE-ABSENT (on the cvt face; the digest face recorded
independently as WRITE-SIDE-REAL vs the honest per-row count).

RUN: 216 decodes ~ 3-4 min — the in-process default
(EXP301_MODE=all).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp301_write_side_face.json")


def main() -> dict:
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it (the body-only discipline: the bytes
    #      after `def main() -> dict:` are the only ones the body
    #      commit may touch) =============================================
    #
    # ==== THE IMPLEMENTATION PLAN (the standing state for the next
    #      session's first dispatch — the exp288/exp296 precedent:
    #      the pre-registration stands, the body lands under it) ======
    #
    # The body = exp300's machinery re-threaded to the write-side
    # battery, with these deltas (each already exercised by the landed
    # predecessors — zero new machinery):
    #   1. THE BATTERY: 3 arms x 72 rows —
    #      ("dormant", g=0.0), (the union faces=("ctx","gj","apop"),
    #      g=1.0), (the union, g=0.5). The row order: the hosts
    #      ascending, the seeds ascending, the instances ascending
    #      within each arm.
    #   2. THE DORMANT ANCHOR (G1): the dormant arm's per-row records
    #      asserted bit-exact vs exp287's deposited rows (the
    #      commit_seq_sha256, the cvt_rms, the n_commits, the sc_rms)
    #      AND exp256's deposited substituted errs — the same asserts
    #      exp289's _decode_anchor_row ran; the machinery: exp296's/
    #      exp300's _rebuild (the r287 extract already reads
    #      commit_seq_sha256/cvt_rms/n_commits/sc_rms per key).
    #   3. THE UNION ARMS: exp300's union coupling (the sigma face
    #      first, then the blends, the blend ONCE at the overlap
    #      cells) at g=1.0 and g=0.5; the row records carry the
    #      commit_seq_sha256, the cvt_rms, the src_census, the
    #      register faces, the site-write counts (all already in the
    #      exp296 lineage's row decoder).
    #   4. G2's tallies: the register faces 72/72 per arm; the stream
    #      faces 72/72 per arm vs exp282/exp287's deposited records;
    #      the site-write constancy for the union arms.
    #   5. G3's faces:
    #      the digest face: per union arm, count the rows whose
    #      commit_seq_sha256 differs from the DORMANT arm's at the
    #      same key (expect 72/72 differ — the carrier writes
    #      different values; record the honest count);
    #      the cvt face: per union arm, the mean cvt_rms vs the
    #      dormant's mean; the per-host cvt drops; the pre-named
    #      branch: WRITE-SIDE-CARRIED iff the union-1.0 mean cvt drop
    #      > 0.05 mV AND >= 10/12 hosts' cvt improves; MARGINAL iff
    #      the drop is in (0, 0.05]; ABSENT iff <= 0;
    #      the census face (audit): the per-arm spec/canon/parent
    #      counts (the branch chain's structure is carrier-invariant).
    #   6. G4: the pins (the docstring/header shas of THIS commit),
    #      the exit checks, the floor, the wall-clock scan — the
    #      exp300 tail's _exit_checks/_scan_wall_clock_keys verbatim.
    #   7. THE DEPOSIT: results/exp301_write_side_face.json; the
    #      fields: the claim/method/inputs/port/rebuild/arm_inputs/
    #      test_suite/rows/anchor_tallies/per_arm_g2/the digest face/
    #      the cvt face/the census/gates/verdict/determinism/
    #      discipline — the exp300 deposit's shape.
    #   8. THE MODES: EXP301_MODE=all (the single battery, 216
    #      decodes, fits one foreground run).
    #
    # ==== BODY placeholder — the pre-registration is this commit; the
    #      body lands under it ===========================================
    raise NotImplementedError(
        "exp301's body lands under the pre-registration commit")


if __name__ == "__main__":
    main()
