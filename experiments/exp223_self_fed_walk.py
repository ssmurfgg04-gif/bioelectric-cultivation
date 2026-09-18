#!/usr/bin/env python3
"""exp223 — THE SELF-FED WALK (L195's registered next).

exp218's X1 + X3 closed the autocatalytic axis on the substrate side:
the cone expands itself (36/36 cones, 12 hosts) and the expansion ADDS
carrying capacity (ADD-CAPACITY on H0 and H4). The remaining edge: the
cone's expansion fed by ITS OWN EMISSIONS as the next round's TARGET —
not just substrate. exp151's walk with the plan re-drawn per round from
the committed pattern itself: the seed patch's own structure propagates
into the frontier's target (the plan for ring k's frontier read from
the committed pattern's own local structure — the propagation rule
pre-named, zero knobs), no external target injection beyond the seed.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp218's walk machinery
verbatim (the window construction, the exp178 production scoped read,
the S* lock, the floor-restore discipline); the PROPAGATION RULE
(pre-named, zero knobs): ring k's frontier plan = the committed
pattern's own values propagated by exp94's spec_target_n on the canon
labeling (the frontier cells' target = the canon value of their
nearest committed ring neighbor — the pattern's own structure carries
forward); the pre-named hosts: H0 and H4 only (the reference and the
worst-margin host — exp218's X3 disclosure reused).

GATES (each evaluated exactly once):
  GATE-Y1 (the self-fed walk) 6 self-fed rings complete with zero
           rejections on H0 and H4 (3 seeds each); ring errs under
           the 6.0 bar throughout — the pattern propagates ITSELF.
  GATE-Y2 (the no-drift clause) the committed values frozen (P6
           verbatim): after each round, the committed prefix equals
           the frozen values bit-exactly (the walk's own discipline,
           asserted — NOT the re-read clause exp218 refuted).
  GATE-Y3 (the self-similarity profile) per-round the frontier's
           emitted-vs-propagated-plan err deposited; the profile
           monotone within the 6.0 bar; the branch named:
           SELF-CARRYING (all 6 rings under the bar) / DEGRADES (any
           ring over).
  GATE-Y4 (hygiene) all finite; the S* lock per write; the -60.0
           floor post-restore asserted; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp223_self_fed_walk.json
RUN: python3 -m experiments.exp223_self_fed_walk [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp223_self_fed_walk.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
