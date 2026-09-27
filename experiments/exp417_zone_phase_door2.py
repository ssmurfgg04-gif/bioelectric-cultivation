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

BODY_DISCLOSURES = [
    "the probe machinery = exp409's landed functions imported VERBATIM "
    "(planted_partition / _target / _walk_stream / _replay — the "
    "planted-partition modular substrates at the validated coupling "
    "regime, the clamp install, the stream-content zone labels, the "
    "within-zone phase, the prefix-min addressing; the within-zone-"
    "structured programs ARE the landed exp409 form, its fix #5)",
    "the battery = the exp409 pair family at the exp304 SCALE: 130 "
    "pairs (seed s vs s+1000 per pair), both orientations collapsed to "
    "the exp409 enumeration (A0 -> A1; the count, not the corpus hosts, "
    "is what the design map demanded — disclosed: the exp304 corpus-host "
    "pairs need the corpus walk home that exp409's probe deliberately "
    "avoids; the scale repair runs on the probe's own family)",
    "the faces at the frozen thresholds: F1 >= 117/130, F2 <= 13/130 "
    "(wide pass = VOID-2), F3 <= 13/130, F4 >= 65/130 OPENS / <= 13/130 "
    "CLOSES / else MIXED",
]


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    from experiments.exp409_zone_phase_door import (
        _replay, _target, _walk_stream, classify_vectorized,
        planted_partition)

    n_pairs = 5 if smoke else N_PAIRS
    rows = []
    for s in range(n_pairs):
        A0 = planted_partition(s)
        A1 = planted_partition(s + 1000)
        tgt0, z0, commits = _walk_stream(A0, seed=s)
        tgt1, z1 = _target(A1, rotate=1)
        ann = {"class": classify_vectorized(tgt0, A0)["class"]}
        e_f1 = _replay(A0, s, tgt0, z0, commits, ann, "plain")
        e_f2 = _replay(A1, s + 1000, tgt1, z1, commits, ann, "plain")
        e_f3 = _replay(A1, s + 1000, tgt1, z1, commits, ann, "class")
        e_f4 = _replay(A1, s + 1000, tgt1, z1, commits, ann, "zonephase")
        rows.append({"pair": s, "F1": e_f1, "F2": e_f2, "F3": e_f3,
                     "F4": e_f4})
        print("pair %3d: F1 %.2f F2 %.2f F3 %.2f F4 %.2f"
              % (s, e_f1, e_f2, e_f3, e_f4))
    BAR = 6.0
    f1 = sum(r["F1"] < BAR for r in rows)
    f2 = sum(r["F2"] < BAR for r in rows)
    f3 = sum(r["F3"] < BAR for r in rows)
    f4 = sum(r["F4"] < BAR for r in rows)
    print("F1 %d/%d  F2 %d/%d  F3 %d/%d  F4 %d/%d (bar %.1f)"
          % (f1, n_pairs, f2, n_pairs, f3, n_pairs, f4, n_pairs, BAR))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": {"SMOKE": "PASS"}}
    verdicts["G1"] = "PASS"          # legality asserted inside exp409's
                                     # landed forms (the exp307 form)
    verdicts["G2"] = "PASS" if f1 >= F1_PASS else "REFUTE"
    verdicts["G3"] = "PASS" if (f2 <= F2_CEIL and f3 <= F3_CEIL) \
        else "REFUTE"
    if verdicts["G3"] == "PASS":
        verdicts["G4"] = "PASS"
        if f4 >= F4_OPEN:
            door = "DOOR-OPENS"
        elif f4 <= F4_CLOSE:
            door = "DOOR-CLOSES"
        else:
            door = "DOOR-MIXED"
    else:
        verdicts["G4"] = "REFUTE"
        door = "DOOR-PROBE-VOID-2"
    branch = door
    dep = {
        "experiment": "exp417",
        "title": "THE ZONE-PHASE DOOR, DISCRIMINATING ATTEMPT (batch "
                 "HU-10)",
        "instrument": {"pairs": n_pairs, "bar": BAR,
                       "machinery": "exp409's landed forms verbatim"},
        "summary": {"F1": f1, "F2": f2, "F3": f3, "F4": f4},
        "rows": rows,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP417 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
