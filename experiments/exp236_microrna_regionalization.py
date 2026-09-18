#!/usr/bin/env python3
"""exp236 — THE microRNA THIRD REGIONALIZATION (Egea-Carro 2026, J. Chem.
Phys. 165(5); the Section 6 item; ledger L212).

THE OPEN QUESTION: the stack's regionalization mechanisms are M33 (the
non-junctional anterior read — exp79/exp128, junction-independent but
ANTERIOR-ONLY above NEURAL_SPEC_MIN) and M35 (the ARZ multi-lineage
convergence — exp59, K lineage reads averaged). The Egea-Carro 2026
proposal: microRNA regionalization — a THIRD mechanism: short-range,
junction-INDEPENDENT diffusing repressor gradients (miRNAs move through
extracellular vesicles, not gap junctions) that carve competence zones
by local decay, not by lineage averaging or anterior polarity. The test:
does a miRNA-like repressor layer regionalize where M33 and M35 both
fail?

THE INSTRUMENT (zero-knob, from the mechanism): a repressor field m_i
with its own dynamics: dm_i/dt = -delta_m * m_i + sigma_m * sum_j A_ij
(m_j - m_i) + s_i (a source term at the pre-named source region — the
mid-body ring, the wound's opposite face), and the competence read:
cell i regen-competent iff m_i < m_line (repression lifts competence).
The miRNA channel is junction-INDEPENDENT: the sigma_m diffusion rides
the CONTACT graph (vesicle exchange needs contact, not cytoplasmic
continuity) — at w=0 (gap junctions cut) the miRNA layer still diffuses.
m_line = the layer's own midpoint (the frozen O-style derivation: the
line that splits the settled field at the source ring's half-max).

PRE-REGISTERED GATES:

  R1  THE M33-DEAD-ZONE CARVE: at w=0, below the M33 line (cells with
      phi_spec < NEURAL_SPEC_MIN — where the anterior read cannot
      reach, exp79 TC-G5's trunk panel), the miRNA layer regionalizes:
      the competence zones carved by m < m_line reproduce the trunk
      target's zone structure (zone-assignment accuracy >= 80% on the
      below-line cells, 3 arms x 3 seeds) — a mechanism where M33
      structurally cannot act.
  R2  THE THREE-MECHANISM DECOMPOSITION: the regen coverage of the
      amputation battery (the head + mid + trunk regions, w=0) under
      each mechanism alone and in pairs: M33-only, M35-only, miRNA-only,
      M33+M35, M33+miRNA, M35+miRNA — the miRNA-only coverage exceeds
      0 on the trunk plane (where M33-only is 0 by the TC-G5 theorem)
      and the pairwise coverages compose (each pair >= max(single) on
      every plane, no interference).
  R3  THE COST (the named price): the miRNA layer's competence zones
      are SLOWER than the junctional mechanisms (the settle time to the
      zone structure at the pre-named parameters is >= 2x the M33
      read's) — vesicle diffusion vs cytoplasmic continuity; and the
      layer is noise-fragile (sigma_m small: the zone boundary wanders
      >= 2 cells under noise_std=0.6 where M33's boundary holds).

THE BRANCH (pre-named): R1 PASS -> THIRD-MECHANISM-CONFIRMED (the stack
carries a regionalization channel beyond M33/M35 — the Egea-Carro
parallel is real in this stack); R1 REFUTE -> NOT-CARVED (the miRNA
layer cannot regionalize the dead zone — the stack's regionalization
stays two-mechanism, deposited honestly).

RUN: the w=0 panels + the decomposition battery; serial, BLAS pinned;
minutes.
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
OUT = os.path.join(ROOT, "results", "exp236_microrna_regionalization.json")


def main() -> dict:
    raise NotImplementedError(
        "exp236 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
