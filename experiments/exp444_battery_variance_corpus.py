#!/usr/bin/env python3
"""exp444 — THE BATTERY-VARIANCE CORPUS (batch HU-14; exp441's
resolution limit). exp441: the register dose-shape and stream-content
families are ZERO-VARIANCE on the form corpus (the battery is
verbatim) — untestable by construction. HYPOTHESIS: a corpus WITH
battery variance — the same forms run under a pre-named battery grid
(the register's g_ctx in {0.25, 0.5, 0.75}; the commit noise in
{0.3, 0.6}) — makes the B/D families testable: the class-fixing
feature may be a battery x wiring INTERACTION invisible at fixed
battery.

THE INSTRUMENT (exp427/431's battery with the two pre-named battery
axes; the representative form set: the 8 census-representative forms
spanning the class split — path3, triangle3, ring4, k23, c5chord,
ring5, c6chord, double_ring4; 5 seeds per (form, battery) cell;
the protection class per cell = the >= 3/5 bar).

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0; the constants EXCEPT the two axes
      asserted; the 8-form x 6-battery count (fail=STOP).
  G2  the full table: face status per (form, battery, seed), no
      pruning.
  G3  THE INTERACTION: the protection class FLIPS for >= 1 form
      across the battery grid (INTERACTION-CARRIES — the class is
      battery-coupled, the B/D families are live) or no form flips
      (BATTERY-ROBUST — the class is battery-invariant at this
      grid; the wiring families stand alone).
  G4  the anatomy: the (form x battery) class matrix + the flip
      cells named.
  G5  deposit results/exp444_battery_variance_corpus.json.

BRANCH LATTICE: INTERACTION-CARRIES / BATTERY-ROBUST /
INSTRUMENT-REFUTED.
"""
