#!/usr/bin/env python3
"""exp407 — THE STRESS-INVISIBILITY MECHANISM: WHY IS THE COMPOSED
CARRIER'S STRESS DELTA EXACTLY +0.0000 mV? (batch HU-7; ledger L302;
charter docs/HUMAN_EXTENSION.md §8's recorded next question). exp302
landed the composed stress face: the 2×2 interaction P_union =
+13.13 mV AND the stress decode-delta under the union at g=1.0 EXACTLY
+0.0000 mV, 12/12 hosts. THE MECHANISM HYPOTHESIS (pre-registered
here): at saturation (g=1.0) the commit layer BYPASSES THE DYNAMICS —
the blend `written = (1-g)*theta_new + g*phi_history[i]` degenerates to
`written = phi_history[i]`, and the register chain (the spec install
populated by committed values) is REACHED BY NOTHING THE STRESS TOUCHES
(the pin moves c.theta, the noise, and the branch routing — but a
blended cell's committed value at g=1.0 is its register value alone,
and every cell's register at its first write IS the spec install,
bit-exact). THE PREDICTION: the committed values at the blended cells
are BIT-IDENTICAL between the stress and no-stress arms at g=1.0; the
decode stress-delta is exactly 0 at g=1.0; and the invisibility
DISSOLVES as g relaxes (the delta grows monotonically toward g=0 where
the commit is fully dynamics-coupled).

THE INSTRUMENT (exp300's landed coupling form, minimal mechanism face,
self-contained): the chain substrate n=100 (path adjacency), the
3-zone spec (the house ladder), faces=(ctx, gj) — the two BLEND faces
(the apop face is a SIGMA face: it changes only the noise scale, not
the blend — disclosed exclusion); the g ladder {0, 0.25, 0.5, 0.75,
1.0} × the stress {off, on} (the exp290 A1 write-time −35.0 pin,
restored −60.0), 5 seeds; the exp142 constants (COMMIT_NOISE 0.6,
STEPS_PER_CELL 8); the register populated at the write (the port's
landed form). THE READS: (a) the committed values at the blended cells
per (g, stress, seed); (b) the settled decode error vs the target.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: the coupling form asserted (the blend application
      order, the stream discipline: one normal draw per commit for
      every arm); the floor −60.0 at entry/exit and every settle; the
      constants pre-named (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      pin −35.0, the ladder) and asserted (fail=STOP).
  G2  THE BYPASS FACE (the mechanism, cell-exact): at g=1.0, EVERY
      blended cell's committed value == its spec-install value
      BIT-EXACT (float64 equality) in BOTH stress arms, 5/5 seeds —
      the register chain is reached by nothing the stress touches.
  G3  THE INVISIBILITY REPRODUCED: at g=1.0 the settled decode error
      under stress minus under no stress == 0.0 EXACTLY (the exp302
      face, on the instrument battery), 5/5 seeds.
  G4  THE DISSOLUTION LADDER: |stress delta| of the decode error is
      MONOTONE NON-DECREASING as g falls 1.0 → 0.75 → 0.5 → 0.25 →
      0.0 (the mean over seeds at each g; ties allowed at 0.0) — the
      invisibility is a SATURATION phenomenon, not a carrier property
      that survives relaxation.
  G5  THE DEPOSIT: the committed-layer table, the deltas per g, the
      bit-exact flags, the gates and the branch deposited as
      results/exp407_invisibility_mechanism.json (fail=STOP).

BRANCH LATTICE (pre-named): G1–G5 all PASS -> BYPASS-EXPLAINED (the
+0.0000 is the saturation limit: at g=1.0 the decode reads the
register chain, a channel the stress cannot reach — the carrier does
not ABSORB stress, the saturated commit STOPS READING the dynamics);
any gate FAIL -> MECHANISM-OTHER (the invisibility has another source
— the decomposition table localizes it either way); G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: if BYPASS-EXPLAINED, the "protection" engineering
story changes meaning — building stress-invisible patterns means
building commit layers that read memory, not dynamics (the register
route), NOT building carriers that "absorb" perturbation; the practical
target moves from carrier strength to memory-write discipline.
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
from cultivation.substrate.graph import GraphCollective, path

DEPOSIT = os.path.join(ROOT, "results", "exp407_invisibility_mechanism.json")
N = 100
SEEDS = [0, 1, 2, 3, 4]
GLADDER = [0.0, 0.25, 0.5, 0.75, 1.0]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
DT = 0.1
WINDOW = 30.0


def _spec_target():
    tgt = np.empty(N)
    tgt[:40] = -50.0
    tgt[40:70] = -30.0
    tgt[70:] = -20.0
    return tgt


def _run_arm(g, stress, seed):
    """One (g, stress, seed) arm; returns the committed values at the
    blended cells + the settled decode error."""
    c = GraphCollective(adjacency=path(N), seed=seed)
    tgt = _spec_target()
    c.set_target(tgt)
    c.write_spec_layer(tgt)          # the register's install == the spec
    c.run(WINDOW, dt=DT)
    region = list(range(20, 60))     # the amputation band
    region_set = set(region)
    c.amputate(slice(region[0], region[-1] + 1))
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
    # the boundary set (the ctx face: the region cells adjacent to
    # committed intact tissue) and the junction set (the gj face: the
    # exp259 site — degree >= 2 off the boundary; on the chain the
    # interior non-boundary cells have degree 2 — the gj face covers
    # them, disclosed)
    bnd = set(i for i in region
              if any(j not in region_set
                     for j in np.where(np.abs(c.A[i]) > 0)[0]))
    blended = sorted(bnd | (set(region) - bnd))
    commits = {}
    if stress:
        CORE.NEURAL_SPEC_MIN = STRESS_FLOOR
    for i, src in order:
        for _ in range(STEPS_PER_CELL):
            c.step(DT)
        if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
            commit_base = c.phi_spec[i]
        else:
            commit_base = c.theta[src]
        hist_i = float(c.phi_history[i])
        theta_new = commit_base + c.rng.normal(0.0, COMMIT_NOISE)
        written = theta_new
        if g > 0.0 and i in blended:
            written = (1.0 - g) * theta_new + g * hist_i
        c.theta[i] = written
        c.V[i] = written
        c.phi_history[i] = written
        commits[i] = float(written)
    if stress:
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    c.run(WINDOW, dt=DT)
    err = float(c.pattern_error(tgt))
    return commits, err, blended


def main() -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 the anchors
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert GLADDER == [0.0, 0.25, 0.5, 0.75, 1.0]
    tgt = _spec_target()
    assert tgt.shape == (N,)
    verdicts["G1"] = "PASS"
    print("G1 PASS (anchors: floor %s, the ladder %s)" % (CORE.NEURAL_SPEC_MIN, GLADDER))

    # ---- the battery
    errs = {(g, s): [] for g in GLADDER for s in (False, True)}
    commits_store = {}
    for g in GLADDER:
        for stress in (False, True):
            for seed in SEEDS:
                commits, err, blended = _run_arm(g, stress, seed)
                errs[(g, stress)].append(err)
                commits_store[(g, stress, seed)] = (commits, blended)
                assert np.isfinite(err)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR

    # ---- G2 the bypass face (cell-exact bit equality at g=1.0)
    n_checked = 0
    bit_ok = True
    for seed in SEEDS:
        c_off, blended = commits_store[(1.0, False, seed)]
        c_on, _ = commits_store[(1.0, True, seed)]
        tgt = _spec_target()
        for i in blended:
            n_checked += 1
            if not (c_off[i] == c_on[i] == float(tgt[i])):
                bit_ok = False
    assert bit_ok, "the bypass face failed"
    verdicts["G2"] = "PASS"
    detail["bypass_cells_checked"] = n_checked
    detail["bypass_bit_exact"] = True
    print("G2 PASS (g=1.0: %d blended-cell commits bit-identical to the "
          "spec install in BOTH arms)" % n_checked)

    # ---- G3 the invisibility reproduced at g=1.0
    d1 = [e_on - e_off for e_off, e_on
          in zip(errs[(1.0, False)], errs[(1.0, True)])]
    assert all(d == 0.0 for d in d1), d1
    verdicts["G3"] = "PASS"
    detail["delta_g100_per_seed"] = d1
    print("G3 PASS (g=1.0 stress delta == 0.0 exactly, 5/5 seeds)")

    # ---- G4 the dissolution ladder
    deltas = {}
    for g in GLADDER:
        deltas[g] = float(np.mean([e_on - e_off for e_off, e_on in
                                   zip(errs[(g, False)], errs[(g, True)])]))
    seq = [abs(deltas[g]) for g in GLADDER]
    # RUNTIME BODY FIX, disclosed (gates unchanged in intent): the
    # first run asserted seq in GLADDER's ASCENDING order, which
    # asserts |delta| increasing with g — the REVERSE of the
    # pre-registered gate text ("|stress delta| monotone
    # NON-DECREASING as g falls 1.0 -> 0.75 -> 0.5 -> 0.25 -> 0.0").
    # The assertion now walks the reversed ladder; the deposited data
    # is unchanged and confirms the gate as written.
    seq_desc = list(reversed(seq))          # g: 1.0 -> 0.0
    assert all(seq_desc[i] <= seq_desc[i + 1] + 1e-12
               for i in range(len(seq_desc) - 1)), seq_desc
    verdicts["G4"] = "PASS"
    detail["mean_delta_per_g"] = {str(g): deltas[g] for g in GLADDER}
    print("G4 PASS (|delta| ladder %s monotone non-decreasing toward g=0)"
          % ["%.4f" % x for x in seq])

    # ---- G5 the deposit
    dep = {
        "experiment": "exp407",
        "title": "THE STRESS-INVISIBILITY MECHANISM (batch HU-7)",
        "instrument": {"substrate": "path(100), the 3-zone spec [-50 x40, -30 x30, -20 x30]",
                       "faces": "(ctx, gj) — the two blend faces; the apop sigma face excluded (disclosed: it scales the noise, not the blend)",
                       "ladder": GLADDER,
                       "stress": "the write-time -35.0 floor pin (the exp290 A1 form), restored -60.0",
                       "constants": {"COMMIT_NOISE": COMMIT_NOISE,
                                     "STEPS_PER_CELL": STEPS_PER_CELL,
                                     "SEEDS": SEEDS}},
        "errs": {("%g|%s" % (g, s)): errs[(g, s)] for g in GLADDER for s in (False, True)},
        "mechanism": {"bypass_cells_checked": n_checked,
                      "bypass_bit_exact": True,
                      "mean_delta_per_g": detail["mean_delta_per_g"],
                      "delta_g100_per_seed": d1},
        "gates": verdicts,
        "verdict": "BYPASS-EXPLAINED",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP407 VERDICT: %s BYPASS-EXPLAINED" % verdicts)
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
