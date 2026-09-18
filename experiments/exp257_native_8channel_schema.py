#!/usr/bin/env python3
"""exp257 — THE NATIVE MULTI-CHANNEL WRITE-PATH SCHEMA (THE
ARCHITECTURAL OVERRIDE; batch 22 item 2 — the priority experiment).

THE OPEN ITEM (exp232's S3b STACK-2CH + the user's override directive):
the underlying state is a 2-tuple (V, theta). It cannot represent the
paper's 8 channels because there is nowhere to put them — three of the
paper's 8 channels (Ca2+ transients, 5-HT electrophoresis, apoptosis)
have NO lower-level substrate at all, and the boundary excess lives in
the channel truncation, not in the read face (exp213/216/219/221's four
refutations, exp245's 0.686 unexplained share).

THE SCHEMA (pre-registered here, before any body):

  The state becomes a named 8-channel array `S` of shape (n, 8) on
  BioElectricCollective (and every state-carrying subclass). Channels,
  named per exp232's census — the paper's own 8-channel spec:

    ch0 "vmem"  Vmem bistability            — ACTIVE (the legacy self.V)
    ch1 "theta" homeostatic target / the
                epigenetic-proliferation
                memory face                 — ACTIVE (the legacy self.theta)
    ch2 "gj"    per-cell gap-junction state — DORMANT (init 1.0; today a
                global scalar gap_scale; per-cell state, zero dynamics
                at defaults)                — activation queued (exp259)
    ch3 "ctx"   interior-context channel    — DORMANT (init 0.0; NO stack
                substrate today)            — activation queued (exp258)
    ch4 "ca2"   Ca2+ transient layer        — DORMANT (init 0.0; ABSENT
                today — now it has state)
    ch5 "sht"   serotonin/5-HT electrophoresis — DORMANT (init 0.0;
                ABSENT today — now it has state)
    ch6 "apop"  apoptosis morphogenetic signal — DORMANT (init 0.0;
                ABSENT today — now it has state)
    ch7 "ichan" per-cell ion-channel expression — DORMANT (init gamma;
                today a scalar dial; zero dynamics at defaults)

  Dormancy contract: at defaults every dormant channel (ch2..ch7) has
  ZERO dynamics, ZERO feedback into ch0/ch1, and is only CARRIED
  (initialized, cloned, restored, read). The ch0/ch1 dynamics, the RNG
  draw order, and every legacy code path are byte-identical — the
  refactor is ADDITIVE ONLY.

  Compatibility shims (the migration path): self.V / self.theta become
  properties backed by S[:, 0] / S[:, 1]; set_state, set_target,
  clone_state, restore_state keep their exact legacy signatures and
  semantics (the 2-tuple is channels 0/1; restore writes 0/1 and leaves
  2..7 untouched). New accessors: set_channel / read_channel /
  clone_state_full / restore_state_full (the 8-channel form) and
  CHANNEL_NAMES / ACTIVE_CHANNELS / DORMANT_CHANNELS module constants.

PRE-REGISTERED GATES:

  S1  THE SCHEMA: BioElectricCollective carries S (n, 8) with the 8
      census names above; every legacy accessor is a bit-exact shim;
      the new full-state accessors exist and round-trip (write ch4,
      clone_state, restore_state — ch4 unchanged; clone_state_full /
      restore_state_full — ch4 preserved through the round trip).
  S2  THE BIT-EXACT GATE (zero delta on the deposits):
      B1  exp79's 45-point grid errs re-run bit-exact vs
          results/exp79_two_channel_law.json (the two-channel law's
          own surface — the core deposit);
      B2  exp32's M26 chain record re-run bit-exact (the regrow walk —
          the write path);
      B3  GraphCollective settle+read fingerprint matches
          exp198's n=400 cohort anchor (the subclass carries state
          through the schema);
      B4  the full test suite green from the repo root (hygiene,
          non-gating).
  S3  THE MIGRATION: no experiment module changes (imports unchanged);
      only the core state plumbing (collective.py + the two subclasses'
      state plumbing) is touched; the dormancy contract is asserted in
      code (a dormant channel cannot alter ch0/ch1 trajectories: a
      seeded settle run with ch4 arbitrarily perturbed mid-run
      reproduces the unperturbed run's ch0/ch1 bit-exactly).
  S4  THE DISCIPLINE: deterministic (re-run bit-identical across
      processes); the -60.0 floor restored and asserted at exit after
      any exp169 import; every step pre-registered, nothing tuned.

THE BRANCHES (pre-named): S1-S4 PASS -> SCHEMA-8-NATIVE (the override
lands; channel activation queued one at a time, exp258 first); ANY S2
failure -> the schema does NOT land — diagnose, repair, re-run, the
delta is named in the deposit.

RUN: the anchor batteries (exp79's grid the long pole; serial, BLAS
pinned) + the suite; runner or foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp257_native_8channel_schema.json")


def main() -> dict:
    raise NotImplementedError(
        "exp257 body pending — pre-registration commit only")
