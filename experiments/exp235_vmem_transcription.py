#!/usr/bin/env python3
"""exp235 — THE VMEM->TRANSCRIPTION GROUNDING (Cervera, Levin & Mafe 2026,
Scientific Reports 16(1996); the Section 6 item; ledger L211).

THE OPEN QUESTION: the stack's gene layer (M37, exp60/exp64) responds to
the voltage pattern, but the RESPONSE LAW was never grounded in the
biophysical mechanism. The Cervera 2026 mechanism: Vmem gates
transcription through voltage-sensitive membrane processes (voltage-gated
enzymes / Ca2+ entry alternating with the Nernst potential) — the
transcription factor activation is a THRESHOLD-RESTORED read of Vmem,
not a linear one: activation follows the fraction of time the local Vmem
spends beyond a gate voltage, with the Nernst alternation setting the
gate scale. The grounding test: does the M37 gene layer's response
follow the voltage-gated threshold law, and does the threshold restore
robustness the linear read lacks?

THE INSTRUMENT (zero-knob, from the mechanism): the activation of gene
g at cell i under the Cervera law: a_i,g = sigmoid((|V_i| - gate_g)/w_g)
evaluated on the time-averaged |V| over the write window (the
transcription integrates), with gate_g = the gene's Nernst-scale gate
(the gene layer's own frozen weight table from exp64's candidates — the
gates DERIVED from the layer's existing weights, no new fitting:
gate_g = the |theta| midpoint of the gene's recorded activation range,
w_g = the recorded range's quarter-width). The linear comparator: the
M37 layer's existing linear response (the frozen production read).

PRE-REGISTERED GATES:

  G1  THE THRESHOLD LAW: the Cervera-gated activation tracks the gene
      layer's measured response across the battery (the 3 arms x 5
      target classes x 3 seeds of exp225's target-class sweep machinery)
      with Spearman >= 0.85 — the biophysical mechanism reproduces the
      layer's response WITHOUT fitting.
  G2  THE THRESHOLD RESTORES ROBUSTNESS: under V-noise sigma in
      {2, 5, 10}, the gated read's zone-assignment accuracy degrades
      LESS than the linear read's at every sigma (the threshold's
      robustness margin; matched read: same layer, same genes, the only
      difference the gate).
  G3  THE NERNST ALTERNATION: the gate's dose-response follows the
      alternating pattern the mechanism predicts — activation vs |Vmem|
      is monotone WITHIN a gene but the gates ORDER the genes by their
      recorded ranges (Spearman(gate_g, range_g) >= 0.8 across the
      layer's genes): the layer's own structure carries the Nernst
      scale ordering.

THE BRANCH (pre-named): all three PASS -> GROUNDED (the gene layer's
response is the Cervera mechanism — the M37 layer gains its biophysical
reading); G1 REFUTE -> NOT-GROUNDED (the layer's response is NOT
voltage-gated-threshold — the linear read is the layer's true law and
the Cervera grounding is a scope mismatch, deposited honestly).

RUN: the sweep battery + the noise panel; serial, BLAS pinned; minutes.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp235_vmem_transcription.json")


def main() -> dict:
    raise NotImplementedError(
        "exp235 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
