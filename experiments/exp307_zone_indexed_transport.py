#!/usr/bin/env python3
"""exp307 — THE ZONE-INDEXED TRANSPORT FORM: THE 9TH FORMALIZATION OF
THE ZERO-SUBSTRATE STAR (batch 60; ledger L290c's promoted candidate
(6) — the handoff's "does the composed carrier transport" WITH THE
PREMISE REPAIR DISCLOSED: exp304's carrier arm IS the composed union,
so the literal question is already answered (F3: 0/130, BOTH-BOUND);
the genuinely open transport question is the one the project's final
form pre-named three times (L289's final form, PROJECT_COMPLETE's
next-researcher #1, SYNTHESIS_FINAL §5): the binding is the
INDEXATION, and the one untried door is a WIRING-INDEPENDENT
ZONE-ADDRESSING scheme).

THE 9TH FORMALIZATION: the pattern representation = the commit stream
ANNOTATED WITH THE SOURCE'S PER-POSITION STRUCTURAL CLASS LABELS (the
exp208 classes: 0 canon_boundary, 1 pair_junction, 2 interior — the
same classify call the walk machinery itself runs on its own target
and base adjacency; the annotation travels with the stream as part of
the representation). The destination re-addresses the stream through
its OWN structural classes: each source position's value is written to
the destination's next cell OF THE SAME CLASS in the destination's own
walk order (per-class prefix rule n_c = min(src count, dst count)).
THE LEGALITY (disclosed): the destination donates its own walk order
(exp303/304's precedent — the 8th formalization's transport face used
the destination's own walk as the order donor) AND its own class
labels (a coarser object than the walk order, computed the same way
the walk computes them); the zero-substrate protocol is otherwise
UNTOUCHED — no spec install, no clamps, no encode, no carried state,
the register port never touched. The stream + the source's class
annotation is the representation under test.

THE INSTRUMENT (exp304's landed machinery VERBATIM: the sha-asserted
rebuild, the union walk at the composed optimum g=1.0 arm A0, the
_replay instrument, the canaries; the slice = 12 hosts x (seed 1,
instance 0)) with the ONE new face:

  Z1  THE ANCHORS: the 12 carrier slice walks reproduce exp300's
      deposited union g=1.0 slice rows BIT-EXACT (the errs + the trace
      shas 12/12 — exp304's G1 form); THE CROSS-DEPOSIT ANCHOR: the
      12 plain same-substrate replays reproduce exp304's deposited F2
      region_rms + full_err BIT-EXACT 12/12 (the re-run is a re-run,
      not a re-knob); the marks' validity pinned to exp300's deposited
      arm_inputs.
  Z2  THE RE-INDEX IDENTITY FACE (the new-machinery anchor): the
      class-reindexed SAME-SUBSTRATE replays == the plain F2 replays
      BIT-EXACT 12/12 — on own substrate the class order IS the walk
      order, so the re-index must be a no-op; any transport-face
      difference is thereby attributable to the re-indexation alone.
  Z3  THE ZONE-INDEXED TRANSPORT FACE: the 130 genuine pairs (the
      H0<->H1 exclusion PRE-NAMED, exp304's form), class-reindexed:
      does the annotated stream transport where the bare streams (the
      dormant's AND the carrier's) transported nowhere?

THE BRANCHES (pre-named): TRANSPORT-UNBLOCKED iff >= 1/130 genuine
pairs within the 6.0 bar (THE ZERO-SUBSTRATE BLOCK WEAKENS AT THE 9TH
FORMALIZATION — the representation transports when indexed by
structural role; the headline changes fundamentally); ZONE-BOUND iff
0/130 (THE BLOCK SHARPENS AT 9: the binding is FINER than the
structural classes — the zone-addressing door is tried and closed;
the block's final form gains its 9th and strongest formalization).
The price faces recorded either way (the mean/best region rms; the
per-pair price delta vs exp304's deposited F3 prices — audit-only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets; THE MARKS' VALIDITY: the rebuilt
      q10/q90 + target_part + bands reproduce exp300's deposited
      arm_inputs BIT-EXACT 24/24 + 12/12; THE EXP300 ANCHOR: the 12
      carrier slice walks bit-exact (the errs + the trace shas 12/12);
      THE EXP304 ANCHOR: the 12 plain F2 replays bit-exact (the
      region_rms + the full_err 12/12); the H0<->H1 exclusion
      re-asserted (the pair set == 130 genuine); 4 deposits READ-ONLY
      sha before/after (exp243/256/300/304); the port's provenance +
      the zero-reader scan (the allowlist = the port + the pre-named
      history instruments + this module); exp142 and the core NOT
      modified (sha at entry == exit); the test suite green.
  G2  THE FACES' DEFINITION (zero-knob asserted, fail=STOP per face):
      the streams' bookkeeping (the commit count == walk_steps == the
      trace length 12/12; the digests recorded); the class vectors
      deterministic (the classify re-run identity 12/12); the per-class
      counts recorded per host; Z2's identity 12/12 (the re-index
      no-op on own substrate); every Z3 transport's writes finite and
      n_written > 0; the canaries bit-exact (one Z2 + one Z3 re-run).
  G3  THE BRANCH DISCRIMINANT (pre-named above, evaluated exactly
      once): the 6.0 bar is the house's own ERR_BAR (exp303/304's
      content bar, unchanged); TRANSPORT-UNBLOCKED / ZONE-BOUND; the
      price faces + the F3-delta audit recorded.
  G4  THE DISCIPLINE: deterministic (one pass; the payload serialized
      twice, the shas asserted equal); no wall-clock fields; the
      docstring + header pinned to the pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at
      exit; the floor -60.0 asserted at the entry, at every replay's
      settle (the _replay assert), and at exit.

RUN: 12 carrier walks + 12 plain replays + 12 re-indexed own replays +
130 re-indexed transports + the canaries, in-process one invocation,
~5-6 min, under the 570 s cap.

DEPOSIT: results/exp307_zone_indexed_transport.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp307_zone_indexed_transport.json")


def main() -> dict:
    raise SystemExit("the body is not written yet (pre-registration stub)")
