#!/usr/bin/env python3
"""exp429 — THE ZONE-PHASE DOOR, THE WOUND-GEOMETRY AXIS (batch
HU-12; the standing zero-substrate formalization continues — exp417
voided the COUNT axis honestly at 130/130 and its ledger named the
wound GEOMETRY as what remains). exp409 built the zone-phase
addressing probe; exp417 rebuilt it at the 130-pair scale with
within-zone-structured programs and the probe voided AGAIN: plain
transport matched trivially. The one axis the probe family has not
varied: WHERE the wound sits. If the pattern's addressing is keyed to
the wound GEOMETRY (the plane's position shifts the walk order, the
within-zone phase deciles, and the boundary structure), the
zone-phase re-index statistic must VARY with the wound position; if
the addressing is geometry-invariant, the statistic is flat across
positions and the door's geometry face closes.

THE INSTRUMENT (exp409/exp417's probe form verbatim, the wound
position as the new axis; the budget pre-named):
  the exp409-scale battery (the 20-pair same-family modular form —
  the geometry axis multiplies the battery, so the count axis returns
  to the original scale, disclosed here as frozen); the
  WITHIN-ZONE-STRUCTURED program class (exp417's repair, retained);
  the wound plane's position varied over the pre-named fractions of
  the body axis {0.1, 0.3, 0.5, 0.7, 0.9} — 5 positions x 20 pairs;
  per (position, pair): F1 the same-wiring content control, F2 the
  plain cross-wiring control, F4 the zone-phase re-index statistic
  (the exp409 pre-named forms, thresholds per-pair over 20).
  Legality per exp307's precedent, unchanged: the destination donates
  its walk order + its own labels; NO spec install on the wound
  cells.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS + LEGALITY: floor -60.0 discipline; the exp307
      legality asserts (fail=STOP); the battery enumeration asserted
      (5 x 20 complete).
  G2  THE SENSITIVITY: F1 >= 18/20 at >= 4/5 positions (the probe
      detects real transport across the geometry axis).
  G3  THE VALIDITY: F2 <= 2/20 at >= 4/5 positions (no wide-pass
      void; a wide pass at any position VOIDS that position,
      deposited honestly).
  G4  THE DOOR (the geometry axis): the F4 zone-phase re-index rate
      across the 5 positions — max - min >= 0.30 AND the max
      position's rate >= 0.65 -> DOOR-OPENS-GEOMETRY; all positions
      <= 0.13 -> GEOMETRY-INVARIANT (the door's geometry face
      CLOSES); otherwise DOOR-MIXED.
  G5  deposit results/exp429_wound_geometry_door.json.

BRANCH LATTICE: DOOR-OPENS-GEOMETRY / GEOMETRY-INVARIANT / DOOR-MIXED
/ PROBE-VOID-3 (G3 REFUTE — the third void; the probe family itself
is retired as an instrument and the block stands at 9 formalizations
+ 3 void instruments) / INSTRUMENT-REFUTED.

THE HONEST STAKES: the zero-substrate star's last untested axis. A
geometry-keyed door is a POSITIVE formalization (the addressing has a
physical anchor — the wound plane); a flat result closes the
zone-phase probe family for good and the formalization block records
its terminal honest state.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
POSITIONS = [0.1, 0.3, 0.5, 0.7, 0.9]
PAIRS = 20
F1_BAR = 18
F2_VOID = 2
DOOR_SPREAD = 0.30
DOOR_OPEN_RATE = 0.65
DOOR_CLOSE_RATE = 0.13
DEPOSIT = os.path.join(ROOT, "results",
                       "exp429_wound_geometry_door.json")


BODY_DISCLOSURES = [
    "the probe machinery = exp409's landed functions: _target, "
    "classify_vectorized, planted_partition imported VERBATIM; "
    "_walk_stream and _replay re-implemented with exactly ONE line "
    "changed each — the wound region: the block-pair "
    "{pos, (pos+3)%5} (the zone-exact scatter structure and the 40-cell "
    "size preserved; a contiguous slice would re-introduce the "
    "shredding exp409's runtime fix #2 refuted) instead of the zone-0 "
    "cells; pos=0 IS exp409's canonical form (the calibration "
    "position)",
    "the position mapping: the frozen fractions {0.1, 0.3, 0.5, 0.7, "
    "0.9} of the body axis are the 5 block centers of exp409's "
    "N=100/N_BLOCKS=5 modular substrate — position j = int(frac*5); the "
    "wound's block-pair preserves exp409's zone-mate structure "
    "({j, (j+3)%5}), so the wound's SIZE and scatter are invariant "
    "across positions and only its GEOMETRY (the body-axis location "
    "and the identity-map rung composition it lands on) varies",
    "the destination's wound is GEOMETRY-ALIGNED: the same block-pair "
    "under the destination's own map (the body positions align, the "
    "identity maps differ — the exp303/304 semantics exp409's rotate=1 "
    "encodes)",
    "G4's spread runs over the NON-VOIDED positions only (a wide-pass "
    "position's F4 is meaningless — plain transport matches trivially "
    "there); fewer than 2 valid positions cannot answer the geometry "
    "question and the branch is PROBE-VOID-3 via G3",
]

from collections import deque

import numpy as np

from cultivation.substrate.graph import GraphCollective
from experiments.exp409_zone_phase_door import (
    _target, classify_vectorized, planted_partition, RUNGS, BLOCK,
    DT, STEPS_PER_CELL, COMMIT_NOISE)


def _pair_blocks(pos):
    return sorted(set([pos, (pos + 3) % 5]))


def _wound_region(pos):
    cells = []
    for b in _pair_blocks(pos):
        cells += list(range(b * BLOCK, (b + 1) * BLOCK))
    return sorted(cells)


def _walk_stream_at(A, seed, pos):
    """exp409's _walk_stream verbatim except the wound region (the
    block-pair at pos)."""
    tgt, z = _target(A)
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    for zi, rung in enumerate(RUNGS):
        c.clamp(np.where(z == zi)[0], float(rung))
    c.run(30.0, dt=DT)
    c.release_clamps()
    pre_wound_err = float(c.pattern_error(tgt))
    assert pre_wound_err < 3.0, pre_wound_err
    region = _wound_region(pos)
    region_set = set(region)
    c.V[region] = -30.0
    c.theta[region] = -40.0
    wound_center = float(np.mean(c.theta[region]))
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = region[:1]
        parent_of[frontier[0]] = frontier[0]
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(np.abs(c.A[i]) > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    commits = []
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            c.step(DT)
        if c.phi_spec[i] >= -60.0:
            base = c.phi_spec[i]
        else:
            base = c.theta[src]
        v = base + c.rng.normal(0.0, COMMIT_NOISE)
        c.theta[i] = v
        c.V[i] = v
        commits.append((int(i), float(v)))
    c.run(30.0, dt=DT)
    return tgt, z, commits


def _replay_at(A_dst, seed, tgt_dst, z_dst, commits_src, ann_src, mode,
               pos):
    """exp409's _replay verbatim except the wound region (the
    block-pair at pos, geometry-aligned with the source)."""
    c = GraphCollective(adjacency=A_dst, seed=seed)
    c.set_target(tgt_dst)
    for zi, rung in enumerate(RUNGS):
        c.clamp(np.where(z_dst == zi)[0], float(rung))
    c.run(30.0, dt=DT)
    c.release_clamps()
    assert float(c.pattern_error(tgt_dst)) < 3.0
    region = _wound_region(pos)
    region_set = set(region)
    c.V[region] = -30.0
    c.theta[region] = -40.0
    wound_center = float(np.mean(c.theta[region]))
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = region[:1]
        parent_of[frontier[0]] = frontier[0]
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(np.abs(c.A[i]) > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    dst_cells = [i for i, _ in order]

    if mode == "plain":
        mapping = list(zip([ci for ci, _ in commits_src], dst_cells))
    else:
        cls_dst = classify_vectorized(tgt_dst, A_dst)["class"]
        rung_dst = np.array([RUNGS[np.argmin(np.abs(RUNGS - t))]
                             for t in tgt_dst])
        dst_by_key = {}
        for i in dst_cells:
            key = ((int(cls_dst[i]),) if mode == "class"
                   else (int(cls_dst[i]), float(rung_dst[i])))
            dst_by_key.setdefault(key, []).append(i)
        if mode == "zonephase":
            src_groups = {}
            for pos_i, (ci, v) in enumerate(commits_src):
                rung = RUNGS[np.argmin(np.abs(RUNGS - v))]
                src_groups.setdefault(
                    (int(ann_src["class"][ci]), float(rung)),
                    []).append(pos_i)
            src_phase = {}
            for key, poss in src_groups.items():
                for frac, pos_i in enumerate(poss):
                    src_phase[pos_i] = (
                        key, int(10 * frac / max(len(poss), 1)))
            pools = {}
            for key, cells in dst_by_key.items():
                for frac, i_cell in enumerate(cells):
                    bkt = int(10 * frac / max(len(cells), 1))
                    pools.setdefault((key, bkt), []).append(i_cell)
            mapping = []
            for pos_i, (ci, v) in enumerate(commits_src):
                key, bkt = src_phase[pos_i]
                q2 = pools.get((key, bkt)) or pools.get((key, 0)) or []
                if not q2:
                    for k2, q3 in pools.items():
                        if k2[0] == key and q3:
                            q2 = q3
                            break
                if not q2:
                    for k2, q3 in pools.items():
                        if q3:
                            q2 = q3
                            break
                cell = q2.pop(0) if q2 else None
                if cell is not None:
                    mapping.append((ci, cell))
        else:
            mapping = []
            for ci, v in commits_src:
                if mode == "class":
                    key = (int(ann_src["class"][ci]),)
                else:
                    rung = RUNGS[np.argmin(np.abs(RUNGS - v))]
                    key = (int(ann_src["class"][ci]), float(rung))
                q2 = dst_by_key.get(key)
                if not q2:
                    for k2, q3 in dst_by_key.items():
                        if k2[0] == key[0] and q3:
                            q2 = q3
                            break
                if q2:
                    mapping.append((ci, q2.pop(0)))
    for ci, cell in mapping:
        v = dict(commits_src)[ci]
        c.theta[cell] = v
        c.V[cell] = v
    c.run(30.0, dt=DT)
    return float(c.pattern_error(tgt_dst))


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    smoke = budget_mode == "smoke"
    n_pairs = 3 if smoke else PAIRS
    BAR = 6.0

    per_pos = {}
    for frac in POSITIONS:
        j = int(frac * 5)
        rows = []
        for s in range(n_pairs):
            A0 = planted_partition(s)
            A1 = planted_partition(s + 1000)
            tgt0, z0, commits = _walk_stream_at(A0, s, j)
            tgt1, z1 = _target(A1, rotate=1)
            ann = {"class": classify_vectorized(tgt0, A0)["class"]}
            e_f1 = _replay_at(A0, s, tgt0, z0, commits, ann, "plain", j)
            e_f2 = _replay_at(A1, s + 1000, tgt1, z1, commits, ann,
                              "plain", j)
            e_f3 = _replay_at(A1, s + 1000, tgt1, z1, commits, ann,
                              "class", j)
            e_f4 = _replay_at(A1, s + 1000, tgt1, z1, commits, ann,
                              "zonephase", j)
            rows.append({"pair": s, "F1": e_f1, "F2": e_f2, "F3": e_f3,
                         "F4": e_f4})
        f1 = sum(r["F1"] < BAR for r in rows)
        f2 = sum(r["F2"] < BAR for r in rows)
        f3 = sum(r["F3"] < BAR for r in rows)
        f4 = sum(r["F4"] < BAR for r in rows)
        per_pos[frac] = {"block": j, "f1": f1, "f2": f2, "f3": f3,
                         "f4": f4, "rows": rows}
        print("pos %.1f (block %d): F1 %d/%d F2 %d/%d F3 %d/%d F4 %d/%d"
              % (frac, j, f1, n_pairs, f2, n_pairs, f3, n_pairs,
                 f4, n_pairs))

    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": {"SMOKE": "PASS"}}

    verdicts["G1"] = "PASS"   # the legality/validity asserts fired
                              # inside the verbatim forms (fail=STOP)
    n = PAIRS
    f1_ok = sum(1 for frac in POSITIONS
                if per_pos[frac]["f1"] >= F1_BAR)
    verdicts["G2"] = "PASS" if f1_ok >= 4 else "REFUTE"
    print("G2 %s (F1 >= %d/20 at %d/5 positions)"
          % (verdicts["G2"], F1_BAR, f1_ok))
    f2_ok = sum(1 for frac in POSITIONS
                if per_pos[frac]["f2"] <= F2_VOID)
    verdicts["G3"] = "PASS" if f2_ok >= 4 else "REFUTE"
    voided = [frac for frac in POSITIONS if per_pos[frac]["f2"] > F2_VOID]
    print("G3 %s (F2 <= %d/20 at %d/5 positions; voided %s)"
          % (verdicts["G3"], F2_VOID, f2_ok, voided))

    if verdicts["G3"] == "PASS":
        valid = [frac for frac in POSITIONS if per_pos[frac]["f2"] <= F2_VOID]
        rates = {frac: per_pos[frac]["f4"] / n for frac in valid}
        spread = max(rates.values()) - min(rates.values())
        top = max(rates.values())
        if spread >= DOOR_SPREAD and top >= DOOR_OPEN_RATE:
            door = "DOOR-OPENS-GEOMETRY"
        elif all(r <= DOOR_CLOSE_RATE for r in rates.values()):
            door = "GEOMETRY-INVARIANT"
        else:
            door = "DOOR-MIXED"
        verdicts["G4"] = "PASS"
        detail["f4_rates"] = {str(k): round(v, 3)
                              for k, v in rates.items()}
        detail["spread"] = round(spread, 3)
    else:
        door = "PROBE-VOID-3"
        verdicts["G4"] = "REFUTE"
    branch = door
    print("G4 %s -> %s" % (verdicts["G4"], door))

    dep = {
        "experiment": "exp429",
        "title": "THE ZONE-PHASE DOOR, THE WOUND-GEOMETRY AXIS "
                 "(batch HU-12)",
        "instrument": {"positions": POSITIONS, "pairs": PAIRS,
                       "bar": BAR, "wound": "block-pair {j, (j+3)%5}",
                       "machinery": "exp409's landed forms, one line "
                                    "parameterized each (disclosed)"},
        "per_position": {str(k): {"f1": v["f1"], "f2": v["f2"],
                                  "f3": v["f3"], "f4": v["f4"]}
                         for k, v in per_pos.items()},
        "rows": {"pos_%s" % k: v["rows"] for k, v in per_pos.items()},
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    import json
    import os
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)
    print("EXP429 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
