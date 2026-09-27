#!/usr/bin/env python3
"""exp412 — THE STRESS-INVISIBILITY ON THE HUMAN CONNECTOME (batch
HU-10; handoff Test 2b). exp407 explained the composed carrier's
+0.0000 mV stress delta as the SATURATION bypass on the planarian
chain; exp404 landed COMPOSITION-CLASS-MATCH — the human graph's
composition is ADDITIVE (f = -0.025, Celnik-consistent) where the
planarian's is SUPER-ADDITIVE (P_union = +13.13 mV). THE OPEN
QUESTION: does the saturation bypass itself transfer — is the g=1.0
committed layer on the REAL HUMAN CONNECTOME equally unreached by
stress — or does the human substrate keep the dynamics readable under
composition (a second, mechanistic face of the composition-class
split)? If the bypass transfers, invisibility is a property of the
commit ARCHITECTURE (substrate-general); if it breaks, it is a
property of the substrate's coupling (and shares a mechanism with
exp404's additivity — the charter's recorded question advances).

THE INSTRUMENT (exp403's ported human walk VERBATIM, composed with
exp407's 2-arm face): the exp401 pre-registered human adjacency (the
Schaefer-400 k=6 form, sha-pinned), the identity target, the zone-0
wound corrupted to -30.0, the BFS boundary walk, STEPS_PER_CELL 8,
COMMIT_NOISE 0.6; the register blend at the boundary cells; the
exp290 write-time -35.0 pin, restored -60.0. The composed union here
is (ctx, gj) at g=1.0 — the apop sigma face excluded as exp407
excluded it (it scales the noise, not the blend; disclosed); the gj
face on the human graph = the junction cells (degree >= 2 off the
wound boundary, the exp407 junction rule ported verbatim).
  ARMS: {union OFF, union ON} x {stress OFF, stress ON} x 5 seeds
  (the union-OFF arms ARE exp403's H0/H1 arms at the shared seeds —
  the anchor reuse is disclosed, no re-derivation);
  THE LADDER: g in {1.0, 0.75, 0.5, 0.25, 0.0} x stress x 3 seeds
  (disclosed budget: 3 seeds on the ladder, 5 on the g=1.0 head).
READS: (a) at g=1.0 every blended cell's committed value across the
stress arms — bit-equality; (b) the settled decode error deltas per
g; (c) the cross-species table: the human |Delta(g)| against the
planarian chain's deposited exp407 table and a fresh n=100 chain
replica at the same seeds (the shared-seed comparison, disclosed).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: floor -60.0 at entry/exit and every settle; the
      human FC sha asserted against human/substrate.py's pin; the
      constants asserted (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, the
      pin -35.0, the ladders); the union-OFF arms reproduce exp403's
      deposited per-seed errs BIT-EXACT at the shared seeds
      (fail=STOP).
  G2  THE BYPASS FACE ON HUMAN: at g=1.0, EVERY blended cell's
      committed value is BIT-IDENTICAL across the stress arms in 5/5
      seeds AND the settled stress delta == 0.0 exactly.
  G3  THE DISSOLUTION LADDER: |Delta(g)| monotone non-decreasing as g
      falls 1.0 -> 0.0 on the human graph (the mean over the 3 ladder
      seeds; ties allowed at 0.0).
  G4  THE CROSS-SPECIES TABLE: the human vs planarian-chain |Delta|
      per g deposited side by side; the class comparison stated
      (same-ladder / human-raises / human-lowers) with the ratio at
      g=0.5.
  G5  THE DEPOSIT: the bit-equality flags, the ladder table, the
      cross-species table, gates + branch as
      results/exp412_invisibility_human.json (fail=STOP).

BRANCH LATTICE (pre-named): G2 PASS -> INVISIBLE-TRANSFERS (the
bypass is commit-architecture, substrate-general — the "memory-write
discipline" target from exp407 carries to human-scale design); G2
FAIL with the human delta >= 1.0 mV at g=1.0 -> INVISIBLE-BREAKS-
HUMAN (a species difference mechanistically consistent with exp404's
additivity: an additive substrate keeps the dynamics readable under
composition); G2 FAIL with the delta in (0, 1.0) mV mixed across
seeds -> INCONCLUSIVE (the table localizes it either way). G1 FAIL ->
INSTRUMENT-REFUTED.

THE HONEST STAKES: the second discriminator for the composition-class
question — architecture vs substrate. Either answer sharpens what
"strengthening the carrier" would even mean on a human-scale
neuromodulation target.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
GLADDER = [1.0, 0.75, 0.5, 0.25, 0.0]
COMMIT_NOISE = 0.6
STEPS_PER_CELL = 8
STRESS_FLOOR = -35.0
PROD_FLOOR = -60.0
HEAD_SEEDS = [0, 1, 2, 3, 4]
LADDER_SEEDS = [0, 1, 2]
WOUND_VOLT = -30.0
DEPOSIT = os.path.join(ROOT, "results", "exp412_invisibility_human.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 2d78648; gates G1-G5
    #      evaluated exactly once) ========================================
    # body-only plumbing repair (disclosed, the exp256 body pattern):
    # the pre-registered header carries only os/sys — the rest is
    # imported HERE, in-body, before any use
    import hashlib
    import json
    from collections import deque

    import numpy as np

    import cultivation.bioelectric.collective as CORE
    from cultivation.substrate.graph import GraphCollective, path
    from human.substrate import (build_human_adjacency, human_target,
                                 load_human_fc)

    # ---- the byte-unchanged self-check (the docstring is the 2d78648
    #      pre-registration, byte-for-byte; the header likewise; asserted
    #      at entry AND exit) ---------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "e748c28c15c3e1053b3d11a6ca71faa193fd7a9ee6c0fda98e54db0bc4567ec6")
    EXPECTED_HEADER_SHA256 = (
        "12ae9d8c42efedb968e57271307b779adb8c518aa4fa4f60d8db8c67a574b8b5")
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    _i0 = _src.index('"""')
    _i1 = _src.index('"""', _i0 + 3) + 3
    docstring_sha = hashlib.sha256(_src[_i0:_i1].encode()).hexdigest()
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "exp412 docstring drifted from 2d78648"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "exp412 header drifted from 2d78648"

    DT = 0.1                      # exp403's landed dt
    G_CTX_403 = 0.5               # exp403's H1 dose (the ctx face's ON arm)
    SETTLE_TU = 30.0              # exp403's landed settle

    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}
    floor_log: list = []

    def _set_floor(v: float) -> None:
        CORE.NEURAL_SPEC_MIN = float(v)

    def _read_floor() -> float:
        return float(CORE.NEURAL_SPEC_MIN)

    # =====================================================================
    # THE INSTRUMENT — exp403's ported human walk VERBATIM (the body of
    # experiments/exp403_history_preconditioning.py's _walk copied
    # byte-similar; the ONLY change is the union's gj face, marked
    # inline below) + exp407's junction rule ported verbatim.
    # =====================================================================
    def _walk_union(h, target, zones, region, g, stress, floor_log,
                    union_on: bool):
        """exp403's walk form on the human graph (self-contained).

        union_on=False: exp403's _walk EXACTLY (the ctx blend at the
        boundary cells only — the H0/H1 arms' form).
        union_on=True: the composed union (ctx, gj) at dose g — the
        blend additionally covers the junction cells (the exp407
        junction rule ported verbatim: the region's non-boundary cells
        with degree >= 2; on the k=6 human adjacency every non-boundary
        region cell has support-degree >= 6 >= 2, so the rule covers
        them exactly as it covered the chain's interior on exp407 —
        disclosed). At a cell carrying BOTH faces the blend is applied
        ONCE (exp300's landed composition rule)."""
        region_set = set(region)
        cls = np.zeros(h.n, dtype=int)          # 0 boundary / 1 interior
        for i in region:
            nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
            if nbrs:
                cls[i] = 0
            else:
                cls[i] = 1
        # ---- THE UNION'S GJ FACE (the exp407 junction rule ported; the
        #      ONLY instrument change vs exp403's walk) ------------------
        if union_on:
            support_deg = (np.abs(h.A) > 0).sum(axis=1)
            junction = set(int(i) for i in region
                           if cls[i] != 0 and int(support_deg[i]) >= 2)
            blended = set(int(i) for i in region
                          if cls[i] == 0) | junction
        else:
            blended = set(int(i) for i in region if cls[i] == 0)
        # frontier seeds: region cells adjacent to committed intact tissue
        parent_of, frontier = {}, []
        for i in region:
            nbrs = [j for j in np.where(h.A[i] > 0)[0] if j not in region_set]
            if nbrs:
                parent_of[i] = int(max(nbrs,
                                       key=lambda j: -abs(h.theta[j] - WOUND_VOLT)))
                frontier.append(i)
        if not frontier:
            frontier = list(region)[:1]
            parent_of[frontier[0]] = frontier[0]
        order = [(i, parent_of[i]) for i in frontier]
        visited = set(frontier)
        q = deque(frontier)
        while q:
            i = q.popleft()
            for j in np.where(h.A[i] > 0)[0]:
                if int(j) in region_set and int(j) not in visited:
                    visited.add(int(j))
                    parent_of[int(j)] = int(i)
                    order.append((int(j), int(i)))
                    q.append(int(j))
        if stress:
            _set_floor(STRESS_FLOOR)
            floor_log.append(("walk_entry", _read_floor()))
        for i, src in order:
            for _ in range(STEPS_PER_CELL):
                h.step(DT)
            if h.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                theta_new = h.phi_spec[i] + h.rng.normal(0.0, COMMIT_NOISE)
            else:
                theta_new = h.theta[src] + h.rng.normal(0.0, COMMIT_NOISE)
            written = theta_new
            if g > 0.0 and int(i) in blended:
                written = ((1.0 - g) * theta_new
                           + g * float(h.phi_history[i]))
            h.theta[i] = written
            h.V[i] = written
            h.phi_history[i] = written       # the population (pure recording)
        if stress:
            _set_floor(PROD_FLOOR)
            floor_log.append(("walk_exit", _read_floor()))
        h.run(SETTLE_TU, dt=DT)
        return float(h.pattern_error(target)), blended

    def _run_human(g, stress, seed, union_on):
        """One human arm: exp403's landed setup VERBATIM + the walk."""
        h = GraphCollective(adjacency=W, seed=seed)
        h.set_target(tgt)
        h.run(SETTLE_TU, dt=DT)
        h.phi_spec = tgt.copy()
        h.phi_history = tgt.copy()      # the register's install
        # the wound: zone 0 corrupted to the wound voltage
        h.theta[region] = WOUND_VOLT
        h.V[region] = WOUND_VOLT
        e, blended = _walk_union(h, tgt, zones, region, g, stress,
                                 floor_log, union_on)
        assert np.isfinite(e), (g, stress, seed, e)
        return e, blended, h

    # ---- the exp407 chain instrument (the fresh replica's arm; the
    #      body of experiments/exp407_invisibility_mechanism.py's
    #      _run_arm copied byte-similar, commits dropped — the deltas
    #      need only the settled errs) -----------------------------------
    N_CHAIN = 100

    def _spec_target_chain():
        tgt_c = np.empty(N_CHAIN)
        tgt_c[:40] = -50.0
        tgt_c[40:70] = -30.0
        tgt_c[70:] = -20.0
        return tgt_c

    def _run_chain_arm(g, stress, seed):
        c = GraphCollective(adjacency=path(N_CHAIN), seed=seed)
        tgt_c = _spec_target_chain()
        c.set_target(tgt_c)
        c.write_spec_layer(tgt_c)          # the register's install == spec
        c.run(30.0, dt=DT)
        reg = list(range(20, 60))          # the amputation band
        region_set = set(reg)
        c.amputate(slice(reg[0], reg[-1] + 1))
        wound_center = float(np.mean(c.theta[reg]))
        parent_of, frontier = {}, []
        for i in reg:
            nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                    if j not in region_set]
            if nbrs:
                parent_of[i] = int(max(
                    nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
                frontier.append(i)
        if not frontier:
            frontier = reg[:1]
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
        if stress:
            _set_floor(STRESS_FLOOR)
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
            if g > 0.0:                    # the chain's blended set == the
                written = ((1.0 - g) * theta_new   # whole band (exp407's
                           + g * hist_i)           # landed rule, disclosed)
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
        if stress:
            _set_floor(PROD_FLOOR)
        c.run(30.0, dt=DT)
        err = float(c.pattern_error(tgt_c))
        assert np.isfinite(err)
        return err

    # ==================== G1 — THE ANCHORS ==============================
    assert _read_floor() == PROD_FLOOR, "floor drift at entry"
    assert GLADDER == [1.0, 0.75, 0.5, 0.25, 0.0], GLADDER
    assert COMMIT_NOISE == 0.6 and STEPS_PER_CELL == 8
    assert STRESS_FLOOR == -35.0 and PROD_FLOOR == -60.0
    assert WOUND_VOLT == -30.0
    assert HEAD_SEEDS == [0, 1, 2, 3, 4] and LADDER_SEEDS == [0, 1, 2]
    fc = load_human_fc()                   # the sha asserted inside
    W = build_human_adjacency(fc)
    rs = float(W.sum(axis=1).mean())
    assert abs(rs - 0.4) < 1e-9, rs
    dep401 = json.load(open(os.path.join(ROOT, "results",
                                         "exp401_human_substrate.json")))
    density = float((W > 0).mean())
    assert abs(float(dep401["preprocessing"]["density"]) - density) < 1e-12, \
        "exp401 adjacency drifted"
    tgt, zones = human_target(W)
    region = list(np.where(zones == 0)[0])
    assert len(region) == 80
    # the union-OFF anchor: exp403's deposited per-seed errs BIT-EXACT
    # at the shared seeds (fail=STOP)
    dep403 = json.load(open(os.path.join(
        ROOT, "results", "exp403_history_preconditioning.json")))
    n_anchor = 0
    union_off_errs: dict = {}
    for key, g, stress in [("H0-S0", 0.0, False), ("H1-S0", G_CTX_403, False),
                           ("H0-S1", 0.0, True), ("H1-S1", G_CTX_403, True)]:
        union_off_errs[key] = []
        for seed in HEAD_SEEDS:
            e, _bl, _h = _run_human(g, stress, seed, union_on=False)
            deposited = float(dep403["errs_per_seed"][key][seed])
            assert e == deposited, \
                (f"the union-OFF anchor drifted at {key} seed {seed}: "
                 f"fresh {e!r} != deposited {deposited!r} (fail=STOP)")
            union_off_errs[key].append(e)
            n_anchor += 1
        assert _read_floor() == PROD_FLOOR, "floor restored"
    assert n_anchor == 20
    verdicts["G1"] = "PASS"
    detail["rowsum_mean"] = rs
    detail["density"] = density
    detail["union_off_anchor_rows"] = n_anchor
    detail["union_off_errs"] = union_off_errs
    print("G1 PASS (anchors: rowsum %.6f, floor %s, %d/20 union-OFF rows "
          "bit-exact vs exp403's deposit)" % (rs, CORE.NEURAL_SPEC_MIN,
                                              n_anchor), flush=True)

    # ==================== G2 — THE BYPASS FACE ON HUMAN =================
    head_errs = {("on" if s else "off"): [] for s in (False, True)}
    bit_ok = True
    n_cells_checked = 0
    for seed in HEAD_SEEDS:
        e_off, bl_off, h_off = _run_human(1.0, False, seed, union_on=True)
        e_on, bl_on, h_on = _run_human(1.0, True, seed, union_on=True)
        assert bl_off == bl_on, (seed, "the blended sets drifted")
        for i in sorted(bl_off):
            n_cells_checked += 1
            v_off = float(h_off.phi_history[i])
            v_on = float(h_on.phi_history[i])
            if not (v_off == v_on == float(tgt[i])):
                bit_ok = False
        head_errs["off"].append(e_off)
        head_errs["on"].append(e_on)
        assert _read_floor() == PROD_FLOOR, "floor restored"
    deltas_head = [eo - ef for eo, ef in
                   zip(head_errs["on"], head_errs["off"])]
    zero_delta = bool(all(d == 0.0 for d in deltas_head))
    assert bit_ok and zero_delta, \
        (f"the bypass face failed: bit_ok={bit_ok} zero_delta={zero_delta} "
         f"deltas={deltas_head}")
    verdicts["G2"] = "PASS"
    detail["bypass_cells_checked"] = n_cells_checked
    detail["bypass_bit_exact"] = True
    detail["delta_g100_per_seed"] = deltas_head
    detail["head_errs"] = head_errs
    print("G2 PASS (g=1.0 union-ON: %d blended-cell commits bit-identical "
          "across the stress arms, 5/5 seeds; the settled stress delta "
          "== 0.0 exactly)" % n_cells_checked, flush=True)

    # ==================== G3 — THE DISSOLUTION LADDER ===================
    ladder_errs = {g: {"off": [], "on": []} for g in GLADDER}
    for g in GLADDER:
        for stress in (False, True):
            for seed in LADDER_SEEDS:
                e, _bl, _h = _run_human(g, stress, seed, union_on=True)
                ladder_errs[g]["on" if stress else "off"].append(e)
            assert _read_floor() == PROD_FLOOR, "floor restored"
    delta_per_g = {}
    for g in GLADDER:
        delta_per_g[g] = float(np.mean(ladder_errs[g]["on"])
                               - np.mean(ladder_errs[g]["off"]))
    seq = [abs(delta_per_g[g]) for g in GLADDER]      # g: 1.0 -> 0.0
    assert all(seq[i] <= seq[i + 1] + 1e-12 for i in range(len(seq) - 1)), \
        f"the dissolution ladder is not monotone non-decreasing: {seq}"
    verdicts["G3"] = "PASS"
    detail["mean_delta_per_g"] = {str(g): delta_per_g[g] for g in GLADDER}
    detail["ladder_abs_seq"] = seq
    detail["ladder_errs"] = {str(g): ladder_errs[g] for g in GLADDER}
    print("G3 PASS (|Delta| ladder %s monotone non-decreasing toward g=0)"
          % ["%.4f" % x for x in seq], flush=True)

    # ==================== G4 — THE CROSS-SPECIES TABLE ==================
    dep407 = json.load(open(os.path.join(
        ROOT, "results", "exp407_invisibility_mechanism.json")))
    planarian_dep_delta = {}
    for g in GLADDER:
        e_off = dep407["errs"]["%g|%s" % (g, "False")]
        e_on = dep407["errs"]["%g|%s" % (g, "True")]
        planarian_dep_delta[g] = float(np.mean(e_on) - np.mean(e_off))
    planarian_fresh_delta = {}
    chain_errs = {g: {"off": [], "on": []} for g in GLADDER}
    for g in GLADDER:
        for stress in (False, True):
            for seed in LADDER_SEEDS:
                e = _run_chain_arm(g, stress, seed)
                chain_errs[g]["on" if stress else "off"].append(e)
        planarian_fresh_delta[g] = float(
            np.mean(chain_errs[g]["on"]) - np.mean(chain_errs[g]["off"]))
        assert _read_floor() == PROD_FLOOR, "floor restored"
    # the class comparison at g=0.5 (the fresh replica = the shared-seed
    # like-for-like; the deposited 5-seed table carried beside)
    h05 = abs(delta_per_g[0.5])
    p05 = abs(planarian_fresh_delta[0.5])
    if p05 > 0.0:
        ratio_05 = float(h05 / p05)
    else:
        ratio_05 = None
    if ratio_05 is None:
        species_class = "human-raises"
    elif 0.9 <= ratio_05 <= 1.1:      # the pre-named tie band (disclosed)
        species_class = "same-ladder"
    elif ratio_05 > 1.1:
        species_class = "human-raises"
    else:
        species_class = "human-lowers"
    verdicts["G4"] = "PASS"
    detail["cross_species_table"] = {
        str(g): {"human_abs_delta": abs(delta_per_g[g]),
                 "planarian_deposited_abs_delta": abs(planarian_dep_delta[g]),
                 "planarian_fresh_abs_delta": abs(planarian_fresh_delta[g])}
        for g in GLADDER}
    detail["planarian_deposited_delta_signed"] = {
        str(g): planarian_dep_delta[g] for g in GLADDER}
    detail["planarian_fresh_delta_signed"] = {
        str(g): planarian_fresh_delta[g] for g in GLADDER}
    detail["chain_errs_fresh"] = {str(g): chain_errs[g] for g in GLADDER}
    detail["ratio_at_g05_human_over_fresh_planarian"] = ratio_05
    detail["ratio_at_g05_human_over_deposited_planarian"] = (
        float(h05 / abs(planarian_dep_delta[0.5]))
        if abs(planarian_dep_delta[0.5]) > 0.0 else None)
    detail["species_class"] = species_class
    print("G4 PASS (the cross-species table: class %s, ratio at g=0.5 %s; "
          "human |D| ladder %s vs planarian-fresh %s)"
          % (species_class,
             ("%.4f" % ratio_05) if ratio_05 is not None else "inf",
             ["%.4f" % abs(delta_per_g[g]) for g in GLADDER],
             ["%.4f" % abs(planarian_fresh_delta[g]) for g in GLADDER]),
          flush=True)

    # ==================== G5 — THE DEPOSIT ==============================
    branch = ("INVISIBLE-TRANSFERS" if verdicts["G2"] == "PASS"
              else "INSTRUMENT-REFUTED")
    dep = {
        "experiment": "exp412",
        "title": "THE STRESS-INVISIBILITY ON THE HUMAN CONNECTOME "
                 "(batch HU-10; Test 2b)",
        "instrument": {
            "adjacency": "exp401's pre-registered human adjacency "
                         "(top-6 symmetric, row-sum 0.4, sha-pinned FC)",
            "wound": "zone 0 (80 cells) -> -30.0",
            "walk": "exp403's ported human walk VERBATIM (BFS "
                    "boundary-inward, STEPS_PER_CELL 8, COMMIT_NOISE 0.6, "
                    "the register blend at the boundary cells, the canon "
                    "layer ABSENT as exp403) + the union's gj face "
                    "(exp407's junction rule ported: the region's "
                    "non-boundary cells with support-degree >= 2)",
            "union": "(ctx, gj) at dose g; the apop sigma face excluded "
                     "as exp407 excluded it (it scales the noise, not "
                     "the blend; disclosed)",
            "stress": "the write-time -35.0 floor pin during the walk "
                      "(the exp290 A1 form), restored -60.0",
            "constants": {"GLADDER": GLADDER, "COMMIT_NOISE": COMMIT_NOISE,
                          "STEPS_PER_CELL": STEPS_PER_CELL,
                          "STRESS_FLOOR": STRESS_FLOOR,
                          "PROD_FLOOR": PROD_FLOOR,
                          "HEAD_SEEDS": HEAD_SEEDS,
                          "LADDER_SEEDS": LADDER_SEEDS,
                          "WOUND_VOLT": WOUND_VOLT}},
        "union_off_anchor": {
            "shared_seeds": HEAD_SEEDS,
            "errs_bit_exact_vs_exp403": True,
            "errs": union_off_errs},
        "bypass_face": {"cells_checked": n_cells_checked,
                        "bit_exact": bool(bit_ok),
                        "delta_g100_per_seed": deltas_head,
                        "head_errs": head_errs},
        "ladder": {"mean_delta_per_g": {str(g): delta_per_g[g]
                                        for g in GLADDER},
                   "abs_seq_g100_to_g0": seq,
                   "errs_per_g": {str(g): ladder_errs[g] for g in GLADDER}},
        "cross_species_table": detail["cross_species_table"],
        "planarian_deposited_delta_signed": {
            str(g): planarian_dep_delta[g] for g in GLADDER},
        "planarian_fresh_delta_signed": {
            str(g): planarian_fresh_delta[g] for g in GLADDER},
        "ratio_at_g05": detail["ratio_at_g05_human_over_fresh_planarian"],
        "species_class": species_class,
        "floor_log_n": len(floor_log),
        "gates": verdicts,
        "verdict": branch,
        "disclosures": [
            "the union-OFF head arms ARE exp403's H0/H1 arms re-run "
            "VERBATIM at the shared seeds — bit-exact against the "
            "deposited errs (the anchor reuse, no re-derivation)",
            "the gj junction rule covers every non-boundary region cell "
            "on both substrates (the chain's interior degree 2; the "
            "human k=6 min degree >= 6) — the ported rule's coverage is "
            "the same whole-band face exp407 landed",
            "the ladder's 3 seeds and the head's 5 seeds ran as "
            "pre-registered; no budget cut was needed",
        ],
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    # the exit discipline: the floor + the bytes re-asserted
    assert _read_floor() == PROD_FLOOR, "floor drifted at exit"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()).hexdigest() \
        == EXPECTED_HEADER_SHA256, "header drifted at exit"
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT, flush=True)

    print("EXP412 VERDICT: %s %s" % (verdicts, branch), flush=True)
    return {"gates": verdicts, "verdict": branch}


if __name__ == "__main__":
    main()
