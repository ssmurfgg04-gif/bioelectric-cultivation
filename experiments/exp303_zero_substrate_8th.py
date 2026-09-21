#!/usr/bin/env python3
"""exp303 — THE ZERO-SUBSTRATE 8TH FORMALIZATION: THE TRANSPORT FORM
(the commit stream as the pattern representation; batch 57; ledger
L287's registered next (c) — the standing frontier sharpened by
exp301/exp302: the carrier's value changes are the program's own spec
re-asserted; the reader's excess IS the un-asserted spec; exp301
landed WRITE-SIDE-CARRIED: the commit stream is the write-side object;
exp288 landed SPEC-UNIFORM: the spec-layer face is class-blind).

THE 8TH FORMALIZATION CLASS: the prior 7 formalizations quantified
over the substrate's structure (the 5 static metrics, the temporal
schedule, the gauge quotient). The 8th states the constraint on the
PROGRAM'S OWN OUTPUT — the commit stream C = [(i_1, v_1), ..., (i_m,
v_m)] (the write-side object exp287 deposited and exp301 carried): the
stream is a substrate-independent pattern representation iff replaying
it into a fresh substrate (the wiring ONLY — no spec install, no
clamps, no encode window, no carried state) reconstructs the pattern
within the pre-named bar. The zero-substrate question in its 8th form:
does the program's write product transport the pattern, or is the
write product as substrate-BOUND as the state it came from?

THE INSTRUMENT (the landed machinery COMPOSED VERBATIM): the 72-row
substituted battery (exp256's) walked in the dormant form (the exp302
landed walk machinery at g=0.0, arm A0 — the errs + the commit-stream
digests MUST reproduce exp256's deposited errs BIT-EXACT 72/72 and
exp287's deposited commit_seq_sha256 BIT-EXACT 72/72 — the streams ARE
the deposited commit sequences), then the REPLAY INSTRUMENT (zero
knobs; every constant inherited): a fresh GraphCollective on the SAME
extended medium A_ext (the read chain's own output), NO spec install /
clamps / encode; the stream's values written into theta AND V at the
walk order's cells IN THE COMMIT ORDER; the walk's own settle (15.0
t.u. at the walk's own dt) at the production floor; the decode.
THE PREDICATE (zero-knob): the REGION-SCOPED reconstruction RMS over
the written cells vs the row's target, vs the pre-named bar ERR_BAR
6.0 mV (the house's registered decode bar — never fit). The scoping is
the machinery's own: the written set IS the commit-index set (the
stream's content claim is exactly the walked cells — the encode's
contribution to the un-walked zones is NOT the stream's to claim; the
full-target decode recorded audit-only).

THE FACES (each evaluated exactly once):
  R2  THE SAME-SUBSTRATE CONTENT FACE: 72 replays (each row's own
      stream on its own substrate, the row's own seed) — the
      region-scoped error vs the 6.0 bar (the stream IS a
      representation of the walked region's pattern, or it is not).
  R3  THE TRANSPORT FACE: the 12 x 11 ordered host-pair slice (the
      pre-named transport slice: the source = the host's (seed 1, i0)
      stream; the destination = each OTHER host's i0 — the
      destination's own walk order computed by the landed frontier
      rule on the destination's own A_ext + the destination's own
      compiled target; the stream's first min(m, m') values written at
      the destination order's first min(m, m') cells; the counts
      recorded) — the region-scoped error vs the SAME 6.0 bar.
  R4  THE BREAK PROBE (the FORALL direction, audit): the transport
      price (the transported error minus the destination's own
      same-substrate replay error — the content vs the destination's
      own program output) per pair.

PRE-REGISTERED GATES:

  R1  THE ANCHORS: the 72 dormant walks reproduce exp256's deposited
      substituted errs BIT-EXACT 72/72 (the verified flags 72/72) +
      exp282's walk anchors (the walk_end_rms + the trace shas +
      err_exact 72/72) + exp287's deposited commit_seq_sha256
      BIT-EXACT 72/72 (the streams ARE the deposited commit
      sequences); the rebuild chain sha-asserted; the floor -60.0
      asserted at the settle/decode of every replay and at exit; 6
      deposits READ-ONLY (exp243/256/272/273/282/287 — sha
      before/after); the test suite green.
  R2  THE CONTENT FACE: the 72 same-substrate replays deterministic
      (the canary re-runs one replay bit-exact); the errors finite
      72/72; the branch clause (below).
  R3  THE TRANSPORT FACE: the 132 transports deterministic; the
      errors finite 132/132; the counts (m, m', n_written) recorded
      per pair; the branch clause (below).
  R4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named):
  TRANSPORT-BREAKS   iff the R2 content face holds (>= 1 of the 72
                     same-substrate replays within the 6.0 bar... no —
                     PRE-NAMED STRICTLY: the R2 face HOLDS iff the
                     MAJORITY (>= 37/72) of the same-substrate
                     replays land within the 6.0 bar AND >= 1 of the
                     132 transports lands within the 6.0 bar — the
                     zero-substrate representation EXISTS in the 8th
                     form (the honest unblocking event);
  TRANSPORT-REFINES  iff the R2 face holds (>= 37/72 within the bar)
                     and ALL 132 transports fail — the stream is a
                     representation but substrate-BOUND (the block
                     DEEPENS: even the program's own output does not
                     transport — the zero-substrate path stays blocked
                     at 8 formalizations);
  TRANSPORT-ABSENT   otherwise (the stream is not even a same-substrate
                     representation — the constraint holds at its
                     strongest form; the write product is not the
                     pattern).

RUN: 72 walks + 72 same-substrate replays + 132 transports ~ 4-7 min
in-process (the replays skip the encode + the per-commit stepping —
settle-only); serial, BLAS pinned.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp303_zero_substrate_8th.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to this file's pre-registration commit; gates R1-R4
    #      evaluated exactly once) ========================================
    raise NotImplementedError(
        "exp303's body lands per the pre-registration (the stub holds "
        "the plan; the body is the next commit)")
