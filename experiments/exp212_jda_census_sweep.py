#!/usr/bin/env python3
"""exp212 — THE JD-A CENSUS SWEEP (L183's registered next).

exp210's membership census disclosed the composition structurally
vacuous at F3 ring-1: the JD-a fence excludes NOBODY there (excl = []
at every ring k=1..6). L183's registered next: the same census, zero
knobs, across ALL 4 families' ring sequences — the fence's exclusions
are unknown everywhere else. Only sites with nonempty excl are
candidates for the boundary-aware composition's second chance; the
census names them or closes the membership face project-wide.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp210's census machinery
verbatim (raw_F - quiet_F per ring via E155's quiet_c_sequence +
frontier_of), swept across the 4 families (F1_zone_tail, F2_*,
F3_canon_boundary, F4_* — the exp200/exp205 family set) x all rings
x the averaged substrates (exp155's averaged_substrate_cs, the
deposited chord seed).

GATES (each evaluated exactly once):
  GATE-C1 (the sweep) every family x ring census deposited (excl
           lists, n_raw, n_quiet per ring); complete, not sampled.
  GATE-C2 (the branch) FENCE-BITES (>= 1 (family, ring) with nonempty
           excl — the sites named and deposited as the composition's
           second-chance candidates) / FENCE-VACUOUS-PROJECT-WIDE
           (excl = [] at every (family, ring) — the membership face
           closes project-wide and the boundary-aware composition is
           closed with it, exp210's reduction generalized).
  GATE-C3 (if FENCE-BITES) at each named site the canon-boundary
           classification of the excluded cells (exp210's convention):
           how many of the fence's exclusions are canon-value boundary
           cells (the composition's admission clause would fire).
  GATE-C4 (hygiene) zero rejections; all finite; the floor pin
           save/restore asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp212_jda_census_sweep.json
RUN: python3 -m experiments.exp212_jda_census_sweep [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp212_jda_census_sweep.json")


def main() -> dict:
    raise NotImplementedError("body written by the run agent; gates fixed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
