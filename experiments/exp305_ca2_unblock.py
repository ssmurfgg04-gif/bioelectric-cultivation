#!/usr/bin/env python3
"""exp305 — THE LAST DORMANT CHANNEL: CAN THE REGISTER UNBLOCK ca2?
(batch 60; ledger L290c's promoted candidate (4) — exp296 landed
CARRIER-GENERAL: gj/str/apop carry the history register, ca2 the sole
inert holdout (+0.0042 mV, 0/12 hosts at the plateau dose g=1.0). THE
DIAGNOSED MECHANISM OF THE INERTNESS: exp296's CA2-HIST arm kept
exp261's landed commit-time gain form VERBATIM with the one source
swap (the HH gate reads the register instead of the live Vmem) — but
the gain's contrast term is battery-mean-centered: gain = 1 +
g*(p_i - pbar), pbar the battery-wide mean P over the register's init
face. The contrast is zero-mean BY CONSTRUCTION across the battery and
near-flat in the working voltage window (the Cav3.3 P face is a
band-pass around ~-48 mV; |p - pbar| ~ 1e-2 over the spec's [-60,-20]
rungs) — a zero-mean per-cell modulation of the correction cannot move
a zone-mean decode. THE OPEN QUESTION: is ca2's inertness FORM-
SPECIFIC (a register coupling whose contrast is NOT zero-mean carries)
or STRUCTURAL (no register coupling through the ca2 channel's landed
semantics can move the decode — the channel sweep closes at 3 carried
+ 1 structurally inert)?

THE INSTRUMENT (exp296's landed walk machinery VERBATIM — the traced
replica at the production budget 8, the register port, the RNG
discipline (exactly ONE normal draw per commit, the stream position
arm-independent), the 72-row substituted battery exp256's, 12 hosts x
3 seeds x r-60i0/r-60i1 at n=400) with the coupling block swapped to
TWO pre-named arms at the plateau dose g=1.0:

  C1 CONTRAST-GAIN  exp261's landed gain form with the ONE pre-named
                    knob change: the baseline term becomes the cell's
                    OWN live gate — p_live = ca_open_prob(ca_m_inf(V_i),
                    ca_h_inf(V_i)) read at the commit (pre-write),
                    p_reg = the same gate at the register read —
                    gain = 1 + g*(p_reg - p_live); written =
                    theta_before + gain*(theta_new - theta_before) at
                    EVERY committed cell (exp261's site semantics);
                    ch4 "ca2" carries the contrast (p_reg - p_live)
                    (the mold: the channel vector carries the
                    coupling's per-cell scalar). The zero-mean
                    cancellation is REMOVED: cells whose remembered
                    state differs from their live state get real
                    amplification/attenuation of the correction.
  C2 CA2-BLEND      the house blend form (exp289's ctx form VERBATIM)
                    at exp261's site semantics (EVERY committed
                    cell): written = (1-g)*theta_new + g*hist_i; ch4
                    "ca2" carries the register read hist_i. The
                    widest site mask any channel has — the
                    site-saturation face of the register's
                    re-assertion.

THE CONTROLS: both arms' control is exp256's deposited substituted
errs (72) — the ca2 channel's landed no-history face IS the dormant
baseline (exp261's c0 identity gate and exp289's G1 proved the g=0
face == the production decode bit-exact on this battery; exp296's
CA2-HIST arm used the same control).

THE BRANCHES (pre-named): UNBLOCKED iff >= 1 arm CARRIES; STILL-INERT
iff neither arm carries; ANTI-CARRIES iff both arms' mean paired
deltas > +0.05 mV (disclosed). An arm CARRIES iff its 72-row mean
paired delta < -0.05 mV AND >= 10/12 hosts improve (host delta < 0) —
exp296's landed bars VERBATIM, re-fixed here, never fit.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets 72/72; THE DORMANT CANARY (seed 1,
      instance 0 per host, g=0.0 — the walk machinery's identity,
      exp304's G1 form): err_exact BIT-EXACT vs exp282's deposited
      err_exact 12/12 + the trace shas BIT-EXACT vs exp282 12/12 +
      round(err_exact, 2) == exp256's deposited err 12/12; exp256's 72
      substituted records re-read as the control (the err chain vs
      exp282's err_deposited 72/72); the consumed deposits READ-ONLY
      sha before/after (exp243/256/282/296); the port's provenance
      (the ported file's sha recorded) + the zero-reader scan (the
      allowlist = the port + the pre-named history instruments + this
      module); exp142 and the core NOT modified (sha at entry ==
      exit); the test suite green.
  G2  THE FORMS (zero-knob asserted, fail=STOP per row): per arm 72
      rows; the register's faces (present/init/replay-equality/
      complement/finite) 144/144; n_arm_writes == walk_steps 144/144
      (both arms arm EVERY committed cell); the ch4 write counts ==
      n_arm_writes; the site-write counts constant across the seeds
      per (host, instance) 24/24 per arm; the A3 state convention
      144/144; the coverage 144/144; the commit count == walk_steps ==
      the trace length 144/144 (the stream face — the RNG positions
      are arm-independent, one draw per commit); the C1 gain faces:
      the gains finite and within [1-g, 1+g] (asserted in-walk, the
      min/max recorded per row); the C2 blend faces: the blend weight
      exactly g (the write's form asserted in-walk by construction);
      the commit values finite 144/144.
  G3  THE BRANCH DISCRIMINANT (the bars pre-named HERE, numeric, never
      fit): carry = (the 72-row mean paired delta < -0.05 mV) AND
      (>= 10/12 hosts improve) — exp296's landed bars VERBATIM;
      UNBLOCKED / STILL-INERT / ANTI-CARRIES as pre-named above; the
      per-host delta table + the worst-err audit + the gain-spread
      audit recorded.
  G4  THE DISCIPLINE: deterministic (one pass per arm; the payload
      serialized twice, the shas asserted equal); no wall-clock
      fields; the docstring + header pinned to the pre-registration
      commit, asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0
      asserted at exit; the floor -60.0 asserted at the entry, after
      the canary, after each arm's batch, and at exit.

RUN: 144 armed decodes + the 12 canary decodes, in-process one
invocation, ~4-6 min, under the 570 s cap.

DEPOSIT: results/exp305_ca2_unblock.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp305_ca2_unblock.json")


def main() -> dict:
    raise SystemExit("the body is not written yet (pre-registration stub)")
