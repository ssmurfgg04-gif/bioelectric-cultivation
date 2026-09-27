#!/usr/bin/env python3
"""exp427 — WHAT WIRING CARRIES THE PROTECTION? THE MOTIF CENSUS
(batch HU-12; exp424's registered follow-up). exp424 corrected exp418:
protection holds at n=3 on protective graphs — the floor is
WIRING-DEPENDENT, not a universal count. The open question is the
shape of that dependence: WHICH wiring feature separates protective
graphs from non-protective ones at small n? Four pre-named candidates,
fixed before the census runs:
  (a) CYCLE      — the graph contains a cycle (cycle rank >= 1);
  (b) DEGREE     — min degree >= 2 (every cell has a second neighbor);
  (c) HUB        — max degree >= 3 (a concentration point exists);
  (d) TWOKCHANNEL— the exp418 two-channel motif structure (a ctx face
                   AND a gj face both present).

THE INSTRUMENT (exp418's battery verbatim at the census scale; zero
new knobs):
  the census forms — every connected simple graph on 3 nodes (path3,
  triangle3) and on 4 nodes (path4, star4, ring4, complete4, paw4,
  diamond4) + the exp418 two-channel motif (motif4): 9 forms total,
  binary unweighted (the census question is WIRING; exp424's
  precedent), each form's adjacency built by the corpus's own
  constructors.
  THE BATTERY per (form, seed): the settled program defines phi_spec
  (the house-ladder zones, exp418's scaled semantics); the wound +
  walk (STEPS_PER_CELL 8, COMMIT_NOISE 0.6); the register blend
  g_ctx in {0, 0.5}; stress {off, on} (the write-time -35.0 pin,
  restored -60.0); 5 seeds per form.
  FACES per (form, seed): T-REGISTER, T-PROTECT (the 2x2 interaction
  P), T-COMPOSE — exp418's definitions verbatim.
  A form is PROTECTIVE iff T-PROTECT holds on >= 3/5 seeds.
  The holdout probes (ring5, path5) are built and held aside; their
  battery runs ONLY after the carrier verdict is fixed from the
  census (the pre-named prediction test).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      constants asserted; the census count asserted (9 forms, no
      pruning); every form's face table complete (fail=STOP).
  G2  THE FULL TABLE: face status per (form, seed) x all three faces
      deposited — no pruning, including the forms that fail
      everywhere.
  G3  THE CARRIER: a candidate is CONSISTENT iff every protective
      form has it AND every non-protective form lacks it (zero
      contradictions across the 9-form census). THE GATE: exactly
      one candidate is consistent.
  G4  THE HOLDOUT: the winning candidate predicts T-PROTECT on
      ring5 (has-cycle) and path5 (no-cycle) — both predictions
      correct (fail of either = REFUTE, deposited honestly).
  G5  deposit results/exp427_protection_motif_census.json.

BRANCH LATTICE: CYCLE-CARRIED / DEGREE-CARRIED / HUB-CARRIED /
MOTIF-CARRIED (the consistent winner) / MULTI-CARRIER (>= 2
consistent — the protection is over-determined) / NO-CARRIER (none —
the protection is not a single-feature property at this scale) /
INSTRUMENT-REFUTED (G1 fail).

THE HONEST STAKES: exp424's correction made the minimal substrate a
WIRING question; the census either names the feature (the S_min
curve becomes predictive — "protection = f(wiring), computable
before the battery runs") or honestly dissolves the single-feature
hypothesis.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

G_CTX_GRID = [0.0, 0.5]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
SEEDS = [0, 1, 2, 3, 4]
CENSUS_FORMS = ["path3", "triangle3", "path4", "star4", "ring4",
                "complete4", "paw4", "diamond4", "motif4"]
HOLDOUT_FORMS = ["ring5", "path5"]
PROTECT_SEED_BAR = 3
DEPOSIT = os.path.join(ROOT, "results",
                       "exp427_protection_motif_census.json")


def main() -> dict:
    raise NotImplementedError(
        "exp427 body pending — gates frozen at the pre-registration commit")


if __name__ == "__main__":
    main()
