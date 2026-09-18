#!/usr/bin/env python3
"""exp261 — THE CA2 CHANNEL ACTIVATION, BETSE-GROUNDED (batch 23
item 2; the THIRD activation under the exp257 schema — ch4 "ca2" —
with the kinetics ported from BETSE, the user's designated reference).

THE OPEN ITEM: the paper's 8-channel census (exp232) found Ca2+
transient signaling ABSENT from the stack; the exp257 schema gave it
native state (ch4, dormant); the activation record so far: ch3 ctx
INERT (exp258), ch2 gj INERT (exp259). Ca2+ is the channel with the
richest external grounding: BETSE (the BioElectric Tissue Simulation
Engine, github.com/betsee/betse — the cell-mesh electrical dynamics,
ionic flux and voltage-gated channel machinery of the Levin-lineage
modeling program) ships voltage-gated calcium channels with
Hodgkin-Huxley kinetics and a Vmem-dependent Ca2+ ATPase pump. This
experiment ports those kinetics VERBATIM (constants + source-line
provenance, zero re-fit) and tests whether the Ca2+ channel carries a
boundary-localized signal the V/theta pair does not.

THE PORT (pre-registered, provenance-recorded in the deposit):

  K1  BETSE's Cav3.3 T-type channel (betse/science/channels/vg_ca.py,
      class Cav3p3, Traboulsie et al. 2007): m_inf(V) =
      1/(1+exp((V+45.454426)/5.073015)); m_tau(V) = 3.394938 +
      54.187616/(1+exp((V+40.040397)/4.110392)); h_inf(V) =
      1/(1+exp((V+74.031965)/8.416382)); h_tau(V) = 109.701136 +
      0.003816*exp(-V/4.781719); open probability P = m^1 * h^1;
      time unit 1e3 (ms); reversal +30 mV (recorded, not used — the
      open-probability face only).
  K2  BETSE's Ca2+ ATPase pump face (betse/science/sim_toolbox.py,
      pumpCa): the equilibrium constant Keq = exp(-(dG_ATP/(RT) -
      2 F Vm/(RT))) — the pump's Vmem dependence is exactly the
      2-charge electrophoresis term; recorded as the pump's
      steady-state reading: the Vmem -> resting-P map is monotone
      through BOTH the channel gates and the pump equilibrium.

PRE-REGISTERED GATES (two stages, the write coupling GATED on the
readout):

  C1  THE PORT: the ported gate functions reproduce BETSE's own
      curves bit-exactly — the deposit records the source sha256 of
      the two BETSE files, the ported constants, and a 401-point
      V-grid (-85..+5 mV, the stack's physiological range) where
      m_inf/h_inf/m_tau/h_tau/P are computed BOTH by the ported
      functions and by a direct import-free recomputation from the
      quoted source lines; equality asserted to 0.0 delta.
  C2  THE READOUT (does the Ca2+ field localize the boundary
      excess?): at the dormant baseline (no coupling), compute the
      per-cell open-probability field P_i = m(V_i) h(V_i) on the c6
      battery's settled states (exp226's battery x 3 seeds, the
      exp258 battery verbatim) and test the pre-named association:
      Spearman(P_i, the cell's |V_i - theta_i| mismatch) >= 0.5 AND
      the boundary cells' mean P exceeds the non-boundary cells' mean
      (the pre-named localization clause). The readout is zero-risk:
      no dynamics touched, the channel is READ only.
  C3  THE WRITE COUPLING (only if C2 passes; if C2 fails, C3 is
      skipped and recorded SKIPPED-C2-FAIL): the HH-gated ca2 pull —
      the cell's theta restoration pull multiplied by (1 + g_ca *
      (P_i - P̄)) with P̄ the battery-wide mean P (the gain form the
      exp258 grid tested; the SAME pre-named grid {0, 0.25, 0.5,
      1.0}); the gates: the best cell reduces the worst boundary-row
      err >= 10% AND the non-boundary rows' worst-err change <= +5%
      (the exp258/exp259 forms verbatim). g_ca = 0 IS the dormant
      identity (bit-exact, the migration gate's own face).
  C4  THE DISCIPLINE: the BETSE reference tree READ-ONLY (sha-record
      the two ported files); exp226's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; collective.py untouched (the
      activation instrument lives in the experiment module via the
      public accessors); the -60.0 floor restored and asserted;
      deterministic re-run, no wall-clock fields.

THE BRANCHES (pre-named): C2 PASS + C3 PASS -> CA2-CARRIES (the
paper's third absent substrate carries a boundary-localized,
externally-grounded signal — the 8-channel correspondence gains its
first NEW active channel); C2 PASS + C3 REFUTE -> CA2-READOUT-ONLY
(the signal localizes but the write face does not close the boundary);
C2 REFUTE -> CA2-INERT (deposited honestly).

RUN: the c6 battery x the pre-named grid (4 values x 3 seeds) + the
port verification; foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp261_ca2_activation_betse.json")

# the BETSE reference tree (the user's directive clone; READ-ONLY)
BETSE_REF = os.path.join(os.path.dirname(ROOT), "betse-reference")
BETSE_VG_CA = os.path.join(BETSE_REF, "betse", "science", "channels",
                           "vg_ca.py")
BETSE_TOOLBOX = os.path.join(BETSE_REF, "betse", "science",
                             "sim_toolbox.py")


def main() -> dict:
    raise NotImplementedError(
        "exp261 body pending — pre-registration commit only")
