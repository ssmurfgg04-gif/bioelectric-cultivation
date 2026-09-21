#!/usr/bin/env python3
"""exp304 — THE TRANSPORT FACE RE-SCOPED: THE DEGENERACY REPAIR + THE
CARRIER'S STREAM (batch 58; ledger L288's registered next (a) — exp303
landed the 8th formalization with the pre-named branch clause counting
the degenerate H0<->H1 pair (whose substrates are BIT-IDENTICAL, the
chain constructor's echo — disclosed, never patched in-gate): the
honest reading was TRANSPORT-REFINES-DEEPENED (0/130 genuine
cross-substrate transports, the mean price +15.76 mV). THIS EXPERIMENT
DOES TWO THINGS: (1) THE REPAIR — the transport face re-scoped to the
130 genuinely-distinct ordered pairs (the H0<->H1 exclusion PRE-NAMED
this time), with the dormant transports reproduced BIT-EXACT against
exp303's deposited per-pair region rms (the cross-deposit anchor); (2)
THE CARRIER'S STREAM — exp301 landed WRITE-SIDE-CARRIED: the composed
carrier's commits differ from the dormant's on 72/72 rows and land
closer to the target; exp302 landed the mechanism face (the armed
sites' writes ARE the spec install re-asserted, the blend weight 1.0).
The open question: does the CARRIER's stream transport where the
dormant's is wiring-bound? The carrier's armed values are the spec
install itself — zone-consistent by construction at the SOURCE; the
transport maps them onto the destination's own walk order (the walk
order is arm-independent, exp300's G2 stream face) — if the carrier's
values are zone-consistent on ANY wiring (the spec's re-assertion is
substrate-free in the sense exp288's SPEC-UNIFORM named), the
transport should succeed where the dormant's idiosyncratic state
failed: THE UNBLOCKING EVENT. The null: the carrier's stream is
wiring-bound exactly as the dormant's — the indexation binds both.)

THE INSTRUMENT (the landed machinery COMPOSED VERBATIM): the
(seed 1, instance 0) slice of the exp256 battery — 12 rows — walked in
BOTH forms: the dormant (the exp302 landed walk at g=0.0/A0 — the errs
+ the commit digests reproduce exp256's/exp287's deposited slice rows
BIT-EXACT 12/12) and the CARRIER (the exp302 landed union coupling
faces=(ctx, gj, apop) at the composed optimum g=1.0, arm A0 — the errs
+ the trace shas reproduce exp300's deposited union g=1.0 slice rows
BIT-EXACT 12/12; the walk orders are arm-independent, asserted). The
REPLAY INSTRUMENT is exp303's landed form VERBATIM (the fresh
GraphCollective on A_ext, NO spec install/clamps/encode/carried state,
the stream's values at the walk order, the walk's own settle, the
region-scoped decode at the pre-named ERR_BAR 6.0).

THE FACES (each evaluated exactly once):
  F1  THE DORMANT REPAIR: the 130 genuine dormant transports (the
      pre-named exclusion: the ordered pairs (h, h') with h' != h and
      NOT {h, h'} == {H0, H1}) reproduce exp303's deposited per-pair
      region rms BIT-EXACT 130/130 (the cross-deposit anchor — the
      repair is a re-scoping, not a re-run with new knobs).
  F2  THE CARRIER CONTENT FACE: the 12 carrier same-substrate
      replays — the region-scoped error vs the 6.0 bar, the majority
      bar 7/12 (the same spirit as exp303's 37/72).
  F3  THE CARRIER TRANSPORT FACE: the 130 genuine carrier transports
      — the region-scoped error vs the SAME 6.0 bar; the transport
      price per pair (the transported error minus the destination's
      own carrier replay error).

PRE-REGISTERED GATES:
  G1  THE ANCHORS: the 12 dormant slice walks reproduce exp256's
      deposited errs + exp282's walk anchors + exp287's commit digests
      BIT-EXACT 12/12; the 12 carrier slice walks reproduce exp300's
      deposited union g=1.0 rows (the errs + the trace shas)
      BIT-EXACT 12/12; the walk orders arm-independent 12/12 (the
      commit-index digests equal across the two forms per row); the
      rebuild chain sha-asserted; the floor -60.0 at every replay and
      at exit; 9 deposits READ-ONLY (exp243/256/272/273/282/287/289/
      300/303 — sha before/after); the test suite green.
  G2  THE FACES: F1 130/130 bit-exact; F2/F3 finite everywhere, the
      canaries (one carrier same-substrate replay + one carrier
      transport re-run bit-exact).
  G3  THE BRANCH DISCRIMINANT (pre-named):
      CARRIER-TRANSPORTS  iff F2 holds (>= 7/12) AND >= 1/130 genuine
                          carrier transports within the bar AND F1
                          reproduces (the dormant control 0/130
                          re-confirmed) — the carrier's re-assertion
                          stream is substrate-independent where the
                          dormant's is bound: THE UNBLOCKING EVENT;
      BOTH-BOUND         iff F2 holds AND 0/130 carrier transports —
                          the block deepens (the indexation binds
                          both forms);
      MIXED              otherwise (recorded, the honest leftover).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

RUN: 24 walks + 12 carrier same-substrate replays + 260 transports +
the canaries ~ 4-7 min in-process; serial, BLAS pinned.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp304_transport_rescoped.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to this file's pre-registration commit; gates G1-G4
    #      evaluated exactly once) ========================================
    raise NotImplementedError(
        "exp304's body lands per the pre-registration (the stub holds "
        "the plan; the body is the next commit)")
