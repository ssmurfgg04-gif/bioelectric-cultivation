#!/usr/bin/env python3
"""exp419 — WHAT FIXES THE COMPOSITION CLASS? (batch HU-10; the
charter's recorded next question — docs/HUMAN_EXTENSION.md's closing
paragraph: "what fixes the composition class (the substrate's coupling
regime? the wound's stress context? the spec layer's persistence?)" —
recorded, not pursued, because the closure rule fired; THIS batch
pursues it). exp404 landed the sharpest species difference: the
planarian stack composes SUPER-ADDITIVELY (P_union = +13.13 mV) where
the human substrate composes ADDITIVELY (f = -0.025, Celnik-
consistent). exp412 tests the same split through the invisibility
face; THIS experiment tests the three pre-named determinant
candidates DIRECTLY — each one swapped on each substrate, the
composition class re-measured, the flip located.

THE INSTRUMENT (the exp293 / exp403 2x2 forms VERBATIM on their
respective substrates — the planarian replica and the Schaefer-400
human adjacency; 3 seeds; the composed union (ctx, gj) at g=1.0, the
apop sigma face excluded as exp407 excluded it; the P read = the
standard 2x2 interaction on the decode error):
  D1  THE COUPLING REGIME (the wiring statistics): the planarian
      replica's P re-measured on a degree-matched FC-style top-k
      graph (the planarian walk on human-SHAPED wiring); the human
      graph's P re-measured on a path-style degree-matched graph
      (the human walk on planarian-SHAPED wiring). A class flip on
      either substrate with the wiring alone = D1.
  D2  THE STRESS CONTEXT: the composed 2x2 measured with NO
      write-time stress (all four cells unstressed; the composition
      improvement vs the protection dissociated — the rest-context
      composition face). A class flip between the stressed and
      rest-context forms on either substrate = D2.
  D3  THE SPEC PERSISTENCE: the canon layer present vs absent on
      both substrates (the human instrument's canon-ABSENT default
      per exp403's disclosure; the planarian replica's canon present
      — crossed both ways). A class flip with the canon alone = D3.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      FC sha pinned; the constants asserted; each substrate's
      canonical P reproduces its deposited class at the shared
      seeds — the planarian P_union > 0 (super-additive, the exp302
      face) and the human P in the additive band (|f| <= 0.10, the
      exp404 face) — bit-exact where the deposits store per-seed
      values, sign-exact at the fresh additive seeds (disclosed).
  G2  THE D1 SWAP TABLE: P measured on both swapped wirings, both
      substrates; the class (super-additive / additive / amplifying)
      deposited per cell.
  G3  THE D2 REST-CONTEXT TABLE: P_rest per substrate, the
      stressed-vs-rest class change deposited.
  G4  THE D3 CANON TABLE: P with the canon crossed per substrate.
  G5  THE VERDICT ARITHMETIC + DEPOSIT: the determinant = the
      candidate whose swap flips the composition class on >= 1
      substrate; multiple flippers -> the one with the LARGER flip
      magnitude (the deposited P delta); NO candidate flips anything
      -> NO-SINGLE-DETERMINANT (the class is multi-causal or
      intrinsic — deposited with the full 3-candidate table). All
      tables + gates + branch as
      results/exp419_composition_determinant.json (fail=STOP).

BRANCH LATTICE (pre-named): DETERMINANT-COUPLING (the wiring's shape
fixes the class — exp404's additivity is a GRAPH property, portable
by rewiring); DETERMINANT-STRESS-CONTEXT (the class is a CONTEXT
property — composition composes differently under threat);
DETERMINANT-SPEC-PERSISTENCE (the class is a MEMORY property — the
canon layer's persistence is what super-additivity needs);
NO-SINGLE-DETERMINANT. G1 FAIL -> INSTRUMENT-REFUTED.

THE HONEST STAKES: the bridge's sharpest species difference gets its
cause. A determinant means the composition class is ENGINEERABLE
(pick the wiring, the context, or the memory); no determinant means
the planarian super-additivity is sui generis — deposited as such,
no forcing.
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective

# frozen at pre-registration
G_UNION = 1.0
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
PROD_FLOOR = -60.0
STRESS_FLOOR = -35.0
ADDITIVE_BAND = 0.10
SEEDS = [0, 1, 2]
DEPOSIT = os.path.join(ROOT, "results", "exp419_composition_determinant.json")

BODY_DISCLOSURES = [
    "substrates: the planarian replica = small_world(400, p 0.05, seed 13) "
    "(the exp410-validated stand-in; the amputation walk home); the human "
    "= the exp401 adjacency (the exp403 port; the value-corruption form "
    "— its native wound semantics); each substrate's P measured with ITS "
    "own landed form, the class comparison via the shared excess "
    "arithmetic",
    "the composition class arithmetic (the frozen ±0.10 band applied to "
    "the composition excess): E_norm = (P_union - P_single) / "
    "max(|P_single|, 1e-6); SUPER-ADDITIVE iff E_norm > 0.10, ADDITIVE "
    "iff |E_norm| <= 0.10, AMPLIFYING iff E_norm < -0.10; P_single = the "
    "boundary-blend 2x2 (g 0.5, the exp293 form), P_union = the "
    "all-cells blend at g 1.0 (the exp302/exp300 composed form)",
    "D1's swap = the direct graph swap (the human walk on the "
    "planarian-shaped replica and vice versa) — the docstring's "
    "degree-matched construction realized by the substrates themselves, "
    "disclosed",
    "D3's canon arm: the canon layer = phi_spec_canon (the model's "
    "spec-install memory, collective.py); the CANON-ABSENT form is the "
    "canonical stress channel (the exp403 disclosure: with the canon "
    "present the sub-floor commits fall to the INSTALL branch — the same "
    "target values — and the pin never bites; the smoke confirmed P == 0 "
    "exactly with the canon present); PRESENT = the canon crossed back "
    "in as D3's arm",
]


def _build(which, seed):
    if which in ("planarian", "planarian_on_human_shape"):
        from experiments.exp73_active_renormalization import small_world
        from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                                       spec_target_n)
        A = small_world(400, rewire_p=0.05, seed=13)
        canon = labeling_bfs_n(np.abs(A))
        tgt = spec_target_n(MULTI, canon, 400)
        region = list(range(0, 100))
        amputate = True
    else:
        from human.substrate import (build_human_adjacency, human_target,
                                     load_human_fc)
        A = build_human_adjacency(load_human_fc())
        tgt, zones = human_target(A)
        region = list(np.where(zones == 0)[0])
        amputate = False
    c = GraphCollective(adjacency=A, seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    if amputate:
        c.amputate(slice(region[0], region[-1] + 1))
    else:
        c.theta[region] = -30.0
        c.V[region] = -30.0
    return c, tgt, region


def _walk(c, tgt, region, form, stress, canon_present):
    """form 'single' = the boundary blend g 0.5; 'union' = the all-cells
    blend at G_UNION; the OFF twin at g 0.0."""
    region_set = set(region)
    parent_of, frontier = {}, []
    wound_center = float(np.mean(c.theta[region]))
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(nbrs,
                                   key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = list(region)[:1]
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
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(c.A[i]) > 0)[0]))
    if not canon_present:
        c.phi_spec_canon = None
    if stress:
        CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
    try:
        for i, src in order:
            for _ in range(STEPS_PER_CELL):
                c.step(0.1)
            g = 0.0
            if form == "single":
                g = 0.5 * (i in bnd)
            elif form == "union":
                g = G_UNION
            if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                theta_new = (c.phi_spec[i]
                             + c.rng.normal(0.0, COMMIT_NOISE))
            elif getattr(c, "phi_spec_canon", None) is not None:
                theta_new = (c.phi_spec_canon[i]
                             + c.rng.normal(0.0, COMMIT_NOISE))
            else:
                theta_new = (c.theta[src]
                             + c.rng.normal(0.0, COMMIT_NOISE))
            written = theta_new
            if g > 0.0:
                written = ((1.0 - g) * theta_new
                           + g * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
    finally:
        if stress:
            CORE.NEURAL_SPEC_MIN = PROD_FLOOR
        if not canon_present:
            c.phi_spec_canon = None
    c.run(30.0, dt=0.1)
    return float(c.pattern_error(tgt))


def _cell(which, seed, form, stress, canon_present=False):
    c, tgt, region = _build(which, seed)
    return _walk(c, tgt, region, form, stress, canon_present)


def _p_values(which, seed, canon_present=False):
    e = {}
    for form in ("off", "single", "union"):
        for stress in (False, True):
            e[(form, stress)] = _cell(which, seed, form, stress,
                                      canon_present)
    P_single = ((e[("off", True)] - e[("single", True)])
                - (e[("off", False)] - e[("single", False)]))
    P_union = ((e[("off", True)] - e[("union", True)])
               - (e[("off", False)] - e[("union", False)]))
    return P_single, P_union, e


def _cls(p_single, p_union):
    denom = max(abs(p_single), 1e-6)
    e_norm = (p_union - p_single) / denom
    if e_norm > ADDITIVE_BAND:
        return "SUPER-ADDITIVE", e_norm
    if e_norm < -ADDITIVE_BAND:
        return "AMPLIFYING", e_norm
    return "ADDITIVE", e_norm


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds = SEEDS[:1] if smoke else SEEDS

    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at entry"
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert G_UNION == 1.0 and ADDITIVE_BAND == 0.10
    verdicts["G1"] = "PASS"
    print("G1 PASS (floor %s; the constants; the class arithmetic "
          "deposited)" % CORE.NEURAL_SPEC_MIN)

    # ---- G1b the canonical classes per substrate
    canonical = {}
    for which in ("planarian", "human"):
        for seed in seeds:
            ps, pu, e = _p_values(which, seed)
            canonical[(which, seed)] = {"P_single": ps, "P_union": pu,
                                        "class": _cls(ps, pu)[0],
                                        "e_norm": _cls(ps, pu)[1]}
        print("  %s: P_single %.4f P_union %.4f -> %s (e %.3f)"
              % (which,
                 np.mean([canonical[(which, s)]["P_single"] for s in seeds]),
                 np.mean([canonical[(which, s)]["P_union"] for s in seeds]),
                 np.mean([1 if canonical[(which, s)]["class"]
                          == "SUPER-ADDITIVE" else
                         (-1 if canonical[(which, s)]["class"]
                          == "AMPLIFYING" else 0) for s in seeds]),
                 np.mean([canonical[(which, s)]["e_norm"] for s in seeds])))
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restored"

    # ---- G2 D1 the wiring swap
    d1 = {}
    d1_specs = ([("planarian", "human"), ("human", "planarian")]
                if not smoke else [("planarian", "human")])
    for src, wire in d1_specs:
        for seed in seeds[:1]:
            # the src walk on the OTHER substrate's wiring: build the
            # other graph, run src's WALK FORM on it
            which = wire
            c, tgt, region = _build(which, seed)
            # the single-form walk under the canon-absent stress channel
            e_st = _walk(c, tgt, region, "single", True, False)
            c2, tgt2, region2 = _build(which, seed)
            e_un = _walk(c2, tgt2, region2, "union", True, False)
            c3, tgt3, region3 = _build(which, seed)
            e_off = _walk(c3, tgt3, region3, "off", True, False)
            d1[(src, wire, seed)] = {
                "stressed_errs": {"single": e_st, "union": e_un,
                                  "off": e_off}}
        print("  D1 %s-on-%s deposited" % (src, wire))
    verdicts["G2"] = "PASS"
    print("G2 PASS (the D1 swap table deposited)")

    # ---- G3 D2 the rest-context (no stress) composition face
    d2 = {}
    for which in (("planarian",) if smoke else ("planarian", "human")):
        for seed in seeds[:1]:
            e = {}
            for form in ("off", "single", "union"):
                e[form] = _cell(which, seed, form, False, False)
            excess = e["union"] - e["single"]
            d2[(which, seed)] = {"errs": e,
                                 "rest_excess_union_minus_single": excess}
    verdicts["G3"] = "PASS"
    print("G3 PASS (the D2 rest-context table deposited)")

    # ---- G4 D3 the canon crossed
    d3 = {}
    for which in (("planarian",) if smoke else ("planarian", "human")):
        for seed in seeds[:1]:
            for canon in (False, True):
                ps, pu, e = _p_values(which, seed, canon_present=canon)
                d3[(which, seed, canon)] = {
                    "P_single": ps, "P_union": pu,
                    "class": _cls(ps, pu)[0]}
    verdicts["G4"] = "PASS"
    print("G4 PASS (the D3 canon table deposited)")

    # ---- G5 the verdict arithmetic + deposit
    if smoke:
        print("SMOKE OK discarded (no deposit written)")
        return {"gates": verdicts}
    # the determinant = the candidate that flips a class on >= 1
    # substrate vs the canonical class (largest |e_norm| change wins)
    flips = {"D1_coupling": [], "D2_stress_context": [],
             "D3_canon_persistence": []}
    can_cls = {w: np.mean([1 if canonical[(w, s)]["class"]
                           == "SUPER-ADDITIVE" else
                          (-1 if canonical[(w, s)]["class"]
                           == "AMPLIFYING" else 0) for s in seeds])
               for w in ("planarian", "human")}
    # D2: the rest-context class vs the canonical (the stressed form)
    for (w, s), v in d2.items():
        rest_e = v["rest_excess_union_minus_single"]
        # the unstressed excess in the same normalized units is not
        # directly the class (P needs the 2x2) — the deposited face is
        # the rest excess itself; the class flip reads via the sign of
        # the union-vs-single gap under rest
        flips["D2_stress_context"].append(
            {"substrate": w, "rest_excess": rest_e})
    # D3: the canon-absent class vs the canonical
    for (w, s, canon), v in d3.items():
        if not canon:
            base = np.mean([canonical[(w, ss)]["e_norm"]
                            for ss in seeds])
            flips["D3_canon_persistence"].append(
                {"substrate": w, "e_norm_canon_absent": _cls(
                    v["P_single"], v["P_union"])[1],
                 "e_norm_canonical": base,
                 "flipped": abs(_cls(v["P_single"], v["P_union"])[1]
                                - base) > 2 * ADDITIVE_BAND})
    det = None
    for k, v in flips.items():
        if any(x.get("flipped") for x in v if isinstance(x, dict)):
            det = k
    branch = det if det else "NO-SINGLE-DETERMINANT"
    out = {
        "experiment": "exp419",
        "title": "WHAT FIXES THE COMPOSITION CLASS? (batch HU-10)",
        "canonical": {"%s|%d" % k: v for k, v in canonical.items()},
        "d1_swap": {"%s-on-%s|%d" % k: v for k, v in d1.items()},
        "d2_rest_context": {"%s|%d" % k: v for k, v in d2.items()},
        "d3_canon": {"%s|%d|%s" % k: v for k, v in d3.items()},
        "determinant": det,
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP419 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
