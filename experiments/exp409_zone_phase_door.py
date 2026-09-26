#!/usr/bin/env python3
"""exp409 — THE ZONE-PHASE ADDRESSING DOOR: THE 10TH FORMALIZATION OF
THE ZERO-SUBSTRATE STAR (batch HU-9; ledger L304; the door exp307
pre-named three times — "the binding is the indexation ... finer than
the structural classes; the within-class zone-phase is the real
carrier of the wiring dependence"). exp307 closed the CLASS-reindex
door (0/130 — the classes are two nearly-degenerate bins). THE OPEN
DOOR: annotate the commit stream with the IDENTITY-ZONE labels + the
within-zone phase, and let the destination re-address through its OWN
zones. THE LEGALITY (the exp307 precedent, extended one step and
disclosed): the zone label is DERIVED FROM THE STREAM'S OWN CONTENT —
the compiled programs are zone-constant, so each committed value's
nearest ladder rung IS its zone label (no extra carried state; the
destination's rung labels come from its own target, the same object
the walk machinery computes classes from). The phase = the fractional
position of the cell within its (rung, class) group in the source's
commit order. THE ZERO-SUBSTRATE PROTOCOL OTHERWISE UNTOUCHED: no spec
install on the destination's wound cells, no clamps, no encode, no
carried state; the destination donates its own walk order + its own
labels (the exp303/304/307 precedent).

THE INSTRUMENT (the door-probe form, pre-named smaller than the 130
battery): n=100; 20 graph pairs (H0 = random_regular(100, 3, seed s),
H1 = random_regular(100, 3, seed s+1000), s in 0..19); each side's
program: the 3-zone ladder on its own leading-eigenvector ordering
(the same deterministic construction as the human extension's target —
the zone-constant rungs [-50, -30, -10] x ~33 cells, the remainder at
the first rung's edge); the source walk (the amputation of its zone 0,
the BFS, STEPS_PER_CELL 8, COMMIT_NOISE 0.6, the spec branch over the
parent fallback — the plain dormant walk, NO register blend: the
transport question is about the stream's INDEXATION, not the carrier);
the destination: its zone 0 amputated, blind, the replay writes ONLY
the stream values; the settle 30 tu; the decode: the pattern error vs
the destination's OWN target, the house bar 6.0.

THE FACES (per pair, 20 pairs):
  F1  the content control: the source's stream replayed on the SOURCE
      itself (the same wiring, the plain walk order) — must pass >=
      18/20 (the exp304 content face reproduces on the probe scale);
  F2  the plain cross-wiring transport (the values in the plain walk
      order, no re-index) — the exp304 BOTH-BOUND control: expected
      <= 2/20 (if it passes widely, the controls are broken and the
      probe is void — fail=STOP on the probe's validity);
  F3  the class-reindex control (the exp307 form: the exp208 classes
      via classify_vectorized) — expected <= 2/20 (the 9th
      formalization reproduces on the probe scale);
  F4  THE ZONE-PHASE RE-INDEX (the new face): the (rung, class,
      phase-bucketed) addressing — the destination's next unwritten
      walked cell of the same (class, rung) group, the groups consumed
      in the destination's walk order (the prefix-min rule per group;
      the phase bucket = the decile of the within-group fractional
      position, pre-named — the bucketing keeps the re-index
      well-defined when the group sizes differ).

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the controls: F1 >= 18/20 AND F2 <= 2/20 AND F3 <= 2/20
      (fail=STOP — the probe's validity).
  G2  THE DOOR: F4 — >= 10/20 within the 6.0 bar -> THE DOOR OPENS
      (the zone-phase indexation carries the transport; the 10th
      formalization SUCCEEDS — the star's transport face is unblocked
      in this form); <= 2/20 -> THE DOOR CLOSES (the 10th
      formalization — the block sharpens: the indexation binding is
      finer than rung+class+phase too); between -> DOOR-MIXED (the
      price deposited per pair).
  G3  the deposit: the per-pair table (F1-F4 errs), the branch, the
      legality disclosure, deposited as
      results/exp409_zone_phase_door.json (fail=STOP).

THE HONEST STAKES: this is the star's last pre-named door. Either way
the ledger gains the 10th formalization: the transport face is
INDEXATION-BOUND, and the zone-phase form is the finest legal
addressing the protocol allows without smuggling the spec across.
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cultivation.substrate.graph import GraphCollective, random_regular, classify_vectorized

DEPOSIT = os.path.join(ROOT, "results", "exp409_zone_phase_door.json")
N = 100
PAIRS = 20
K_REG = 3
STEPS_PER_CELL = 8
COMMIT_NOISE = 0.6
DT = 0.1
BAR = 6.0
RUNGS = np.array([-50.0, -30.0, -10.0])


def _target(A):
    vals, vecs = np.linalg.eigh(A)
    order = np.argsort(vecs[:, -1])
    tgt = np.empty(N)
    z = np.zeros(N, dtype=int)
    per = N // 3
    for i, node in enumerate(order):
        z[node] = min(i // per, 2)
    tgt = RUNGS[z]
    return tgt, z


def _walk_stream(A, seed):
    """The source: install its program, amputate zone 0, walk, return
    (the commit stream [(cell, value)], the classes, the rungs, the
    order)."""
    tgt, z = _target(A)
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=DT)
    region = list(np.where(z == 0)[0])
    region_set = set(region)
    c.amputate(slice(min(region), max(region) + 1))
    wound_center = float(np.mean(c.theta[region]))
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
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


def _replay(A_dst, seed, tgt_dst, commits_src, ann_src, mode):
    """The destination: blind wound cells, the replay by the addressing
    mode ('plain' | 'class' | 'zonephase'), the settle, the decode."""
    _, z_dst = _target(A_dst)
    c = GraphCollective(adjacency=A_dst, seed=seed)
    c.set_target(tgt_dst)            # the destination's own program
    # the zero-substrate protocol: the spec layer is NOT installed on
    # the wound cells (no write_spec_layer call); the target above is
    # the scoring object + the label donor (the exp307 legality)
    c.run(30.0, dt=DT)
    region = list(np.where(z_dst == 0)[0])
    region_set = set(region)
    c.amputate(slice(min(region), max(region) + 1))
    wound_center = float(np.mean(c.theta[region]))
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
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
            # the class control addresses by the CLASS ONLY (the exp307
            # form); the zone-phase face addresses by (class, rung)
            key = ((int(cls_dst[i]),) if mode == "class"
                   else (int(cls_dst[i]), float(rung_dst[i])))
            dst_by_key.setdefault(key, []).append(i)
        if mode == "zonephase":
            # the phase bucket: the within-(class,rung) walk-order decile
            # on BOTH sides; the match by (key, bucket), the leftovers by
            # (key,) then by any (the pre-named fallback ladder)
            src_groups = {}
            for pos, (ci, v) in enumerate(commits_src):
                rung = RUNGS[np.argmin(np.abs(RUNGS - v))]
                src_groups.setdefault((int(ann_src["class"][ci]), float(rung)),
                                      []).append(pos)
            src_phase = {}
            for key, poss in src_groups.items():
                for frac, pos in enumerate(poss):
                    src_phase[pos] = (key, int(10 * frac / max(len(poss), 1)))
            pools = {}
            for key, cells in dst_by_key.items():
                for frac, i_cell in enumerate(cells):
                    bkt = int(10 * frac / max(len(cells), 1))
                    pools.setdefault((key, bkt), []).append(i_cell)
            mapping = []
            for pos, (ci, v) in enumerate(commits_src):
                key, bkt = src_phase[pos]
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


def main() -> dict:
    """THE BODY IS WRITTEN AT THE BODY COMMIT (pre-registration)."""
    raise NotImplementedError("exp409 body lands at the body commit")


    verdicts: dict[str, str] = {}
    rows = []
    for s in range(PAIRS):
        A0 = random_regular(N, K_REG, seed=s)
        A1 = random_regular(N, K_REG, seed=s + 1000)
        tgt0, z0, commits = _walk_stream(A0, seed=s)
        tgt1, z1 = _target(A1)
        ann = {"class": classify_vectorized(tgt0, A0)["class"]}
        e_f1 = _replay(A0, s, tgt0, commits, ann, "plain")  # the same wiring
        e_f2 = _replay(A1, s + 1000, tgt1, commits, ann, "plain")
        e_f3 = _replay(A1, s + 1000, tgt1, commits, ann, "class")
        e_f4 = _replay(A1, s + 1000, tgt1, commits, ann, "zonephase")
        rows.append({"pair": s, "F1": e_f1, "F2": e_f2, "F3": e_f3,
                     "F4": e_f4})
        print("pair %2d: F1 %.2f F2 %.2f F3 %.2f F4 %.2f"
              % (s, e_f1, e_f2, e_f3, e_f4))
    f1 = sum(r["F1"] < BAR for r in rows)
    f2 = sum(r["F2"] < BAR for r in rows)
    f3 = sum(r["F3"] < BAR for r in rows)
    f4 = sum(r["F4"] < BAR for r in rows)
    print("F1 %d/20  F2 %d/20  F3 %d/20  F4 %d/20 (bar %.1f)"
          % (f1, f2, f3, f4, BAR))
    assert f1 >= 18, f1
    assert f2 <= 2 and f3 <= 2, (f2, f3)
    verdicts["G1"] = "PASS"
    if f4 >= 10:
        branch = "DOOR-OPENS"
    elif f4 <= 2:
        branch = "DOOR-CLOSES"
    else:
        branch = "DOOR-MIXED"
    verdicts["G2"] = "PASS"
    dep = {
        "experiment": "exp409",
        "title": "THE ZONE-PHASE ADDRESSING DOOR -- THE 10TH FORMALIZATION",
        "rows": rows,
        "summary": {"F1": f1, "F2": f2, "F3": f3, "F4": f4, "bar": BAR},
        "legality": "the zone label derived from the stream's own content (the nearest ladder rung); the destination donates its walk order + its own labels (the exp307 precedent); the zero-substrate protocol otherwise untouched",
        "gates": verdicts,
        "branch": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    verdicts["G3"] = "PASS"
    print("EXP409 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts, "branch": branch}


if __name__ == "__main__":
    main()
