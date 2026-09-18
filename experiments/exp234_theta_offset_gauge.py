#!/usr/bin/env python3
"""exp234 — THE THETA-OFFSET GAUGE TEST (exp232's registered next (b);
the Section 12 anti-deferral rule: derived from the ledger, run now;
ledger L210).

THE OPEN QUESTION (L208): exp232's battery exposed the THETA-STATE
breakout — th_offset(threshold delta=20 mV) leaves err 19.98 mV on the
torus, th_noise(10) leaves 9.37 — and the count=2 verdict carried the
honest caveat: a breakout group is a group the WRITE law does not cover,
not necessarily a SIGNALING channel. The gauge hypothesis: the theta
layer encodes pattern RELATIVELY (V chases theta at rate gamma; theta's
own dynamics eps*(V-theta) + mu*lap(theta) conserve a UNIFORM offset —
the offset lies in the kernel of every mechanism in the stack), so a
uniform theta-offset is a GAUGE degree of freedom: it moves the absolute
RMS error err = RMS(V - lbl) by exactly delta while carrying ZERO pattern
information. If the gauge hypothesis holds, exp232's THETA-STATE
breakout is RECLASSIFIED — not a third signaling channel but an
unobservable mode — and the stack's channel inventory returns to 2
signaling channels + 1 gauge mode, which TIGHTENS the exp232 refutation
of the 8-channel mapping. Honesty cuts both ways: this experiment tests
the reclassification against the stack.

THE ZERO MODE (zero-knob derivation, checked numerically in T1): for a
uniform offset c: d(theta+c)/dt = eps*(V - theta - c); dV follows theta+c
at rate gamma; the pair (V, theta+c) satisfies the SAME equations as
(V - c, theta) — the offset is an exact symmetry of the coupled dynamics
at ANY (gamma, mu, kappa), broken ONLY by absolute anchors: the wound
state constants (amputate's wound_voltage=-30, blastema_theta=-40) and
the physiological clamps V_PHYS_MIN/MAX.

PRE-REGISTERED GATES:

  T1  THE CONSERVATION: after the th_offset delta at the star, err(T)
      stays within 0.5 mV of its T=1 value across T in {1, 6, 24, 96}
      (4 windows x 3 arms x 3 seeds) — no decay channel exists; and the
      zero-mode check: the uniform-offset vector is in the numerical
      kernel of the stack's linearized update (|M @ 1| <= 1e-9 for the
      (V,theta) block operator at 3 operating points).
  T2  THE GAUGE (the information test): the zone structure is INVARIANT
      — the head/trunk classification read off (V, theta) at the offset
      substrate matches the offset-free classification on >= 99% of
      cells at every pre-named delta in {5, 10, 20} (the threshold read
      exp142's sign read; the offset shifts both layers equally, every
      relative comparison unchanged); the pattern's mutual information
      with the target's zone map is delta-invariant (MI drop <= 0.01
      bits).
  T3  THE READ'S BLINDNESS: the production scoped read (exp178's
      machinery) decodes the offset substrate to the SAME target (the
      decode's zone assignment invariant, err_read delta-invariant
      within 0.5 mV at delta in {5, 10, 20} x 3 seeds) — the offset is
      invisible to the read: it has NO information capacity.
  T4  THE GAUGE'S EDGE (where the offset is NOT pure): the wound is an
      absolute anchor — after amputate, the offset substrate's regen
      err differs from the offset-free regen err by >= the offset size
      against the blastema constants (the gauge breaks at the wound:
      blastema_theta=-40 is ABSOLUTE, the committed pattern is offset);
      3 arms x 3 seeds, the delta-20 case. The named asymmetry: the
      stack repairs its pattern only through the wound's absolute
      reference — the gauge is global, the repair is local.

THE BRANCH (pre-named): T1+T2+T3 PASS -> GAUGE-MODE (exp232's
THETA-STATE breakout RECLASSIFIED: the stack has 2 signaling channels +
1 gauge mode; the 8-channel refutation TIGHTENS); T4 names the wound as
the gauge's unique breaker either way. Any T1/T2/T3 REFUTE ->
GENUINE-CHANNEL (the theta-state carries real information; exp232's
count=2 stands with THETA-STATE as a third signaling channel).

RUN: 4 windows + 3 deltas x panels; serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp234_theta_offset_gauge.json")


def main() -> dict:
    raise NotImplementedError(
        "exp234 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
