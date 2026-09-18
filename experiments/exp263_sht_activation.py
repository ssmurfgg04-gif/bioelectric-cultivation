#!/usr/bin/env python3
"""exp263 — THE SHT CHANNEL ACTIVATION (batch 24 item 2; L239's
registered next (b) — the FOURTH activation under the exp257 schema,
ch5 "sht", the paper's 5-HT electrophoresis face).

THE OPEN ITEM: the paper's census (exp232) names serotonin transport
(5-HT electrophoresis) as one of the 8 channels — ABSENT from the
stack; the exp257 schema gave it native state (ch5, dormant). BETSE
carries no serotonin machinery (its ion set is Na/K/Cl/Ca — verified
against the reference tree's ion enum), so the grounding is the
paper's OWN spec face: 5-HT transport is a CHARGE-COUPLED flux — the
transporter moves transmitter down the ELECTROCHEMICAL gradient
(SERT-like: the flux follows the Vmem difference the stack already
computes). The stack-native pre-named instrument: the sht channel
carries the theta-gradient's transport face — the per-cell flux
proportional to the sum of the cell's V-differences to its junction
neighbors (the same electrochemical face the GJ network carries, read
through the transporter's sign convention), accumulated over the
settle.

PRE-REGISTERED GATES (the exp258/exp261 mold: identity, readout,
gated coupling):

  H1  THE DORMANT IDENTITY: g_sht = 0 reproduces the production
      decode bit-exactly on the c6 battery (75/75 rows, the exp258
      X1 form verbatim).
  H2  THE READOUT (zero-risk, read-only): on the c6 battery's settled
      states, the sht field S_i (the accumulated electrochemical
      flux face) is computed per cell; the pre-named association:
      Spearman(S_i, the cell's |V_i - theta_i| mismatch) >= 0.5 over
      the pooled battery points.
  H3  THE WRITE COUPLING (only if H2 passes; else SKIPPED-H2-FAIL):
      the transporter's pull — the cell's theta restoration pull
      multiplied by (1 + g_sht * (S_i - S̄)/S̄_scale) at the pre-named
      grid {0, 0.25, 0.5, 1.0} (S̄_scale = the battery-wide mean |S|,
      the zero-knob normalizer); the gates: the best cell reduces the
      worst boundary-row err >= 10% AND the non-boundary rows'
      worst-err change <= +5%.
  H4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded; collective.py untouched sha-recorded (the
      activation lives in the module via the public accessors);
      the -60.0 floor restored and asserted; deterministic re-run;
      no wall-clock fields.

THE BRANCHES (pre-named): SHT-CARRIES / SHT-READOUT-ONLY /
SHT-INERT — deposited honestly.

RUN: the c6 battery x the grid; foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp263_sht_activation.json")


def main() -> dict:
    raise NotImplementedError(
        "exp263 body pending — pre-registration commit only")
