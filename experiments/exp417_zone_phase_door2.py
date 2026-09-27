#!/usr/bin/env python3
"""exp417 — THE ZONE-PHASE DOOR, DISCRIMINATING ATTEMPT: THE 10TH
FORMALIZATION OF THE ZERO-SUBSTRATE STAR (batch HU-10; handoff Test
6a; exp409's deposited design map EXECUTED). exp409 built the
zone-phase addressing probe and honestly VOIDED it: F2 (the plain
cross-wiring control) passed 20/20 WIDE because the same-family
modular pairs' BFS order correspondence makes plain transport
trivial — the probe could not discriminate the indexation forms. The
deposited design map named the two repairs: the exp304-SCALE battery
(the 130-pair form, not 20 pairs) and WITHIN-ZONE-STRUCTURED programs
(the program's content varies WITHIN each identity zone along the
zone's own walk order — plain transport's order-matched copy fails
by construction, because matching the zone label no longer matches
the content). This experiment rebuilds the probe with both repairs
and re-asks the door. Legality per exp307's precedent, unchanged:
the destination donates its walk order + its own labels; NO spec
install on the wound cells; the zero-substrate protocol otherwise
untouched.

THE INSTRUMENT (exp409's probe form, both repairs applied; the
program-class change disclosed here as pre-registered, not
discovered mid-run):
  the modular graph-pair battery at the exp304 scale (the 130-pair
  form: the same-family and cross-family pairs as exp304's battery
  enumerates them); the WITHIN-ZONE-STRUCTURED program class (the
  content varies along the zone's own walk order — the compiled
  programs remain zone-constant in LABEL, variable in VALUE); the
  commit stream annotated with the identity-zone labels (the nearest
  ladder rung) + the within-zone phase (the walk-order decile per
  (class, rung) group); the destination re-addresses through its OWN
  (class, rung) groups in ITS walk order (the prefix-min rule, the
  pre-named fallback ladder).
FACES (the exp409 pre-named thresholds, re-frozen at the new scale —
the rates are per-pair over 130):
  F1  the same-wiring content control >= 117/130 (0.90 — the probe
      must detect REAL transport);
  F2  the plain cross-wiring control <= 13/130 (0.10 — at the new
      program class a wide pass again VOIDS the probe);
  F3  the class-reindex control <= 13/130 (the exp307 form);
  F4  the zone-phase re-index (THE DOOR) >= 65/130 DOOR-OPENS /
      <= 13/130 DOOR-CLOSES / else DOOR-MIXED.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS + LEGALITY: floor -60.0 discipline; the exp307
      legality asserts (the destination-donated walk order + labels;
      no spec install on wound cells — asserted, fail=STOP); the
      battery enumeration == exp304's form (count asserted 130).
  G2  F1 (the probe's sensitivity).
  G3  F2 + F3 (the probe's validity — either wide-pass FAILs G3 and
      the probe is VOID-2, disclosed; the block then stands at 9
      formalizations + 2 void instruments).
  G4  F4 (the door itself — evaluated only if G3 holds).
  G5  THE DEPOSIT: the per-pair table (130 rows), the four faces,
      gates + branch as results/exp417_zone_phase_door2.json
      (fail=STOP).

BRANCH LATTICE (pre-named): DOOR-OPENS (the 10th formalization
lives: pattern = zone-phase structure; transfer needs a phase-
relational substrate — the minimal-substrate question exp418 runs
gains its lower bound); DOOR-CLOSES (BLOCK-ROBUST-10: the
zero-substrate star stands at 10 formalizations, the block is
honest and final at this instrument class); DOOR-PROBE-VOID-2 (the
probe fails again — the design map's repairs were insufficient; the
next repair, if any, is NOT named here — no infinite probe loop).
G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: the last open door on pure-pattern ascension,
under the fair probe the first attempt taught us to build. Opens,
closes, or voids — all three are honest deposits; the star's count
moves either way.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
N_PAIRS = 130
F1_PASS = 117          # >= 0.90
F2_CEIL = 13           # <= 0.10
F3_CEIL = 13           # <= 0.10
F4_OPEN = 65           # >= 0.50
F4_CLOSE = 13          # <= 0.10
PROD_FLOOR = -60.0
DEPOSIT = os.path.join(ROOT, "results", "exp417_zone_phase_door2.json")


def main() -> dict:
    raise NotImplementedError(
        "exp417 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
