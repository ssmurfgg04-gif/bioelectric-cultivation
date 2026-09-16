#!/usr/bin/env python3
"""exp149 — THE MIRROR AUDIT (harness-implementation re-read, workstream O).

L126's registered object. exp147 (M-REFUTED) proved the harness's own
noise channels are 89x too small in squared-error mass to close the
g64@36 break, so the deterministic mirror (exp135.simulate, verified
3e-15 vs the exp143 chain and reproducing the deposited 4.904) must
diverge from the TRUE HARNESS deterministically at late times by an
omitted or mis-ordered step. This experiment re-reads the harness
implementation line-by-line, diffs it against the mirror, repairs the
mirror to harness-verbatim, and re-runs the 8 anchors.

=====================================================================
PRE-REGISTERED GATES (written BEFORE running; nothing below was
executed when this docstring was committed to the file):
=====================================================================

O1  THE DIFF TABLE identifies >= 1 operationally real discrepancy
    (an operation present in the harness and absent/mis-ordered in
    the mirror, or vice versa) with harness file:line citations.
    Deposit order: the diff table is written to
    results/exp149_mirror_audit.json BEFORE any repaired run.

O2  REPAIR SAFETY: the repaired (harness-verbatim, zero-noise,
    stream-preserving) mirror reproduces exp135.simulate()'s four
    deposited scalars (err, err_span, err_intact, th_span_dev) at the
    7 NON-LATE anchors (g4@36, g16@48, g64@0/16/24/28/31/34) within
    1e-6 per scalar, AND the live exp135.simulate(g64@36) err
    reproduces exp147's deposited deterministic scalar 4.9037 within
    5e-4. If the repair breaks the 7 anchors, the discrepancy list
    was wrong: own it, deposit the diff table + ranked residuals, and
    fail O2.

O3  THE FLIP: the repaired mirror scores g64@36 >= 6.0 (break,
    matching the deposited P(break)=1.0) WITHOUT breaking the other
    7 mandate anchors (all stay < 6.0, verdict-identical).

O4  (conditional on O3) exp140's state-space evaluation re-run on the
    repaired states: the 8 exp140 anchors ((1,0),(4,48),(16,52),
    (16,72),(64,36) break; (4,36),(16,48),(64,34) rescue) get fresh
    (x, y) = (RMS th[span]-target, RMS V[intact]-target) at the read
    from the repaired runs; exp140's exact hard-margin separator
    (max_margin) must separate the repaired break hull from the
    repaired rescue hull (not None) — i.e. the deadline arc's
    standing reduction (the joint (x,y) threshold) CLOSES on
    harness-verbatim data, or fails visibly.

If O3 fails after an honest O1+O2 pass, the deposit IS the diff
table: what the mirror omits that does NOT matter, plus the ranked
remaining divergence hypothesis.

=====================================================================
THE DIFF TABLE (static, from the code as read; each entry verified
dynamically where marked):
=====================================================================

D1  LATCH SCOPE (FLIP CANDIDATE #1, operation domain).
    Harness: exp124.run_deadline's `maybe(t0)` (mu -> 0 when
    t0 >= onset) is called ONLY inside the window loop
    (exp124_deadline_curve.py:95-99) and the walk sub-step loop
    (exp124:121-126). The settle is `c.run(SETTLE_H, dt=dt)`
    (exp124:130) -> BioElectricCollective.run (collective.py:679-698)
    which calls step() with NO latch check. So an onset beyond the
    walk-end time NEVER silences mu: the run finishes with
    mu = 0.015 throughout.
    Mirror: exp135.simulate's dyn_step (exp135:246-249) checks
    `t0 >= t_star -> mu = 0` on EVERY step, and the settle loop
    (exp135:295-299) calls dyn_step — so the mirror silences
    mid-settle for any onset < walk-end + settle.
    Active exactly when onset > t0_walk_end = 24 + 73*8*dt:
    g64 (dt = 1.2/68, walk-end ~34.31) at onset 36, and
    g16 (dt = 0.06, walk-end ~59.04) at onset 72 — the two late
    controls, and nothing else in the deposited grid.
    Direction: the mirror REMOVES mu damage the harness keeps, so
    the mirror under-errs at the late controls (4.904 vs deposited
    break). exp135's docstring claim that the harness latches "in
    the settle's final hours" is FALSE of the harness code; exp125
    imports exp124.run_deadline verbatim (exp125:16,94), so the
    deposited P(break)=1.0 at g64@36 is a full-mu run.

D2  INHERITANCE BRANCH CONTENT (clears the "wound/injection state
    details" candidate). Harness commit (exp124:127-134): three
    branches — (a) phi_spec[i] >= NEURAL_SPEC_MIN (-35,
    collective.py:46) -> phi_spec[i] + N(0,0.6); (b) elif
    phi_spec_canon exists -> canon[i] + N(0,0.6); (c) else parent
    theta + N(0,0.6). exp124 calls set_target(canon) (materializes
    phi_spec = canon, collective.py:113-123) then
    write_spec_layer(target) (preserves canon as phi_spec_canon,
    collective.py:145-148). MULTI's zone voltages are all -30.0
    (exp94:174-177) >= -35, and every amputated span cell lies in a
    zone, so branch (a) fires for EVERY commit with base
    phi_spec[i] = target[i] EXACTLY: the mirror's flat injection
    V[i]=th[i]=target[i] (exp135:288-291) is the precise branch-(a)
    mean. Residual = the 0.6 iid draw only (exp147's inheritance
    channel, budget 0.127 mV^2). VERIFIED DYNAMICALLY: the repaired
    run records max|commit_base - target[i]| over all commits.

D3  INIT-V NOISE. Harness V0 = theta + N(0,2) per cell
    (collective.py:93, seed-dependent); mirror V0 = canon exact
    (exp135:232-233). A channel exp147 did NOT carry (it carried
    per-step V-noise + inheritance only). One-time 2 mV kick, V
    relaxes to theta at rate gamma; repaired run zeroes it by
    overwriting V = canon after construction (stream-preserving:
    the draw still happens, its value is discarded).

D4  PER-STEP V-NOISE. Harness noise_std = 0.30 default, not
    overridden by exp124 (collective.py:75; draw at :645); mirror
    omits (exp135 docstring). exp147 budget: 0.007 mV^2. Zeroed via
    noise_std=0.0 (draw still executes — stream-preserving).

D5  COMMITMENT NOISE. Harness +N(0,0.6) per committing cell
    (exp124:128/131/134); mirror omits. exp147 budget 0.127 mV^2.
    Zeroed stream-preservingly (draw executed, value discarded).

D6  dV FLOAT GROUPING. Harness: coupling = G@V - V*deg then
    dV = gamma*(theta-V) + coupling (collective.py:641-643) —
    a + (b - c). Mirror: dV = gamma*(th-V) + G@V - V*degG
    (exp135:252-253) — (a + b) - c. Last-ulp associativity only;
    covered by O2's 1e-6 tolerance.

D7  CLIPS. Harness np.clip(theta, -85, 5) and np.clip(V, -90, 10)
    every step (collective.py:35-36, :667-669); mirror omits
    (docstring: inert). VERIFIED DYNAMICALLY: the repaired run
    tracks min/max state; clip inert iff state inside
    [V_PHYS_MIN, V_PHYS_MAX] / [V_PHYS_MIN-5, V_PHYS_MAX+5].

D8  CLAMP APPLICATION SITE. Harness clamps applied inside step()
    after the theta/V updates (collective.py:671-676); mirror
    applies them after dyn_step in the window loop (exp135:263-266).
    Same effective order (post-update V override + theta pull at
    dt*eps*(val-theta)). NO-OP.

D9  WALK ORDER + SUB-STEP COUNT (clears the "step-count rounding"
    candidate as a walk mechanism). Harness walks its OWN inline BFS
    with parent selection and a HARDCODED 8 sub-steps per cell
    (exp124:107-126) — it never calls regrow/regenerate_region, so
    graph.py's steps_per_cell = round(cell_period/dt) rounding never
    enters this protocol. Mirror: walk_order + WALK_SUB = 8
    (exp135:224-241, 273-281). MATCH. The g64-specific dt (1.2/68)
    does not change the count 8; it changes WHERE the walk ends on
    the t0 axis, which feeds D1.

D10 GAP_SCALE COUPLING (clears that candidate). Harness theta
    diffusion carries mu*gap_scale with gap_scale = 1.0 throughout
    (exp124 never calls block/restore_gap_junctions;
    collective.py:655); the V-coupling matrix G = A*0.20 is never
    rescaled. Mirror: mu direct. Bit-identical at gap_scale = 1.

D11 THETA_DRIVERS. Harness step() loops self.theta_drivers
    (collective.py:658-662); exp124 installs none. NO-OP.

D12 CLAMP THETA PULL (clears that candidate AS a window mechanism).
    Harness theta[idx] += dt*eps*(vals - theta[idx]) for clamped
    cells (collective.py:675-676); mirror identical form
    (exp135:265). Present in both; clamps exist only in the window
    in both (release_clamps at exp124:100 before amputation).
    NO-OP.

REPAIR DEFINITION (harness-verbatim): the repaired mirror IS
exp124.run_deadline's code path executed on the REAL
GraphCollective/BioElectricCollective classes, with exactly three
documented determinism deltas, each stream-preserving (every RNG
draw the harness makes still executes; only its VALUE is zeroed):
 (i)  noise_std = 0.0 constructor kwarg (D4),
 (ii) V overwritten to canon after set_target/write_spec_layer (D3),
 (iii) the commitment draw's value discarded (D5).
Everything else — clamp objects, window/walk latch scope (D1 left
EXACTLY as the harness has it), amputate, 8-sub-step walk, 3-branch
inheritance, settle via c.run, pattern_error read — is the harness's
own code and objects.

RUN: 13 deterministic cells (the 8 mandate anchors + exp140's
g1@0, g4@48, g16@52, g16@72), seconds each. BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.collective import NEURAL_SPEC_MIN
from cultivation.bioelectric.sheet import TRUNK_V, HEAD_V
from cultivation.compiler.anatomy import compile_anatomy
from cultivation.substrate.graph import GraphCollective
from experiments.exp73_active_renormalization import bfs_order
from experiments.exp90_two_source_read import star_dt
from experiments.exp94_multizone_scale import MULTI, ERR_BAR
from experiments.exp112_walk_speed_ladder import build_battery
from experiments.exp124_deadline_curve import (
    run_deadline as _harness_run_deadline,  # source-integrity reference
    WINDOW_H, SETTLE_H,
)
from experiments.exp135_walk_chain import simulate as e135_simulate
from experiments import exp135_walk_chain as e135
from experiments import exp140_state_space as e140

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp149_mirror_audit.json")

# ---- the mandate's 8 anchors (exp147's cells) + exp140's extra 4
LATE_CELL = (64.0, 36.0)
MANDATE_ANCHORS = [(4.0, 36.0), (16.0, 48.0), (64.0, 0.0), (64.0, 16.0),
                   (64.0, 24.0), (64.0, 28.0), (64.0, 31.0), (64.0, 34.0)]
NON_LATE = MANDATE_ANCHORS                      # 7 + late = 8 mandate
EXTRA_CELLS = [(1.0, 0.0), (4.0, 48.0), (16.0, 52.0), (16.0, 72.0)]
ALL_CELLS = sorted(set(MANDATE_ANCHORS + [LATE_CELL] + EXTRA_CELLS))

DEPOSITED_ERR_DET_G64_36 = 4.9037               # exp147's deposited mirror scalar
DEPOSITED_BREAK = {(1.0, 0.0), (4.0, 48.0), (16.0, 52.0), (16.0, 72.0),
                   (64.0, 36.0)}                # exp140 BREAK_CELLS + verdict
O2_TOL = 1e-6
DEPOSIT_TOL = 5e-4


def fmt(c) -> str:
    return f"g{c[0]:g}@{c[1]:g}"


# ---------------------------------------------------------------- diff table
def build_diff_table() -> list[dict]:
    return [
        {"id": "D1", "title": "mu-latch scope: settle never checks maybe()",
         "harness_site": "exp124_deadline_curve.py:95-99 (window), :121-126 "
                         "(walk sub-steps); settle = c.run(SETTLE_H) at "
                         "exp124:130 -> collective.py:679-698 run() has no "
                         "latch",
         "mirror_site": "exp135_walk_chain.py:246-249 dyn_step latches every "
                        "step; settle loop :295-299 calls dyn_step",
         "class": "operation-domain (mis-ordered/over-broad latch)",
         "active_when": "onset > t0_walk_end = 24 + 73*8*dt -> exactly the "
                        "late controls g64@36 (walk-end ~34.31) and g16@72 "
                        "(~59.04)",
         "direction": "mirror silences mid-settle, harness keeps mu=0.015 "
                      "to the read -> mirror under-errs at late controls",
         "flip_candidate": True,
         "verified_dynamically": "mu_at_read + latch_time recorded per run"},
        {"id": "D2", "title": "inheritance branch content",
         "harness_site": "exp124:127-134 (3 branches); NEURAL_SPEC_MIN "
                         "collective.py:46; phi_spec materialization "
                         "collective.py:113-123,145-148",
         "mirror_site": "exp135:288-291 flat target[i] injection",
         "class": "operation-presence (branch structure)",
         "active_when": "never on this protocol: MULTI zones all -30.0 >= "
                        "-35 (exp94:174-177) and every span cell is zoned, "
                        "so branch (a) fires with base phi_spec[i] = "
                        "target[i] exactly; mirror injects the branch mean",
         "direction": "none structurally; residual = the 0.6 iid draw "
                      "(exp147 budget 0.127 mV^2)",
         "flip_candidate": False,
         "verified_dynamically": "max|commit_base - target| recorded "
                                 "(expect 0.0)"},
        {"id": "D3", "title": "init-V noise N(0,2) at construction",
         "harness_site": "collective.py:93",
         "mirror_site": "exp135:232-233 V0 = canon exact",
         "class": "noise channel (one-time, not carried by exp147)",
         "active_when": "always; V relaxes to theta at rate gamma",
         "direction": "zeroed stream-preservingly in the repair",
         "flip_candidate": False, "verified_dynamically": "repair delta (ii)"},
        {"id": "D4", "title": "per-step V-noise sigma=0.30",
         "harness_site": "collective.py:75 (default), :645 (draw)",
         "mirror_site": "exp135 docstring: noise omitted",
         "class": "noise channel (exp147 budget 0.007 mV^2)",
         "active_when": "always", "direction": "zeroed (noise_std=0.0)",
         "flip_candidate": False, "verified_dynamically": "repair delta (i)"},
        {"id": "D5", "title": "commitment noise N(0,0.6) per commit",
         "harness_site": "exp124:128/131/134",
         "mirror_site": "exp135:288-291 (omitted)",
         "class": "noise channel (exp147 budget 0.127 mV^2)",
         "active_when": "always", "direction": "zeroed stream-preservingly",
         "flip_candidate": False, "verified_dynamically": "repair delta (iii)"},
        {"id": "D6", "title": "dV float grouping a+(b-c) vs (a+b)-c",
         "harness_site": "collective.py:641-643",
         "mirror_site": "exp135:252-253",
         "class": "float associativity",
         "active_when": "always, last-ulp",
         "direction": "covered by O2 tolerance 1e-6",
         "flip_candidate": False, "verified_dynamically": "O2 max|diff|"},
        {"id": "D7", "title": "physiological clips every step",
         "harness_site": "collective.py:35-36 (bounds), :667-669 (clip)",
         "mirror_site": "exp135 (omitted, docstring: inert)",
         "class": "operation-presence",
         "active_when": "only if state leaves [-85,5]/[-90,10]",
         "direction": "expected inert; bounds tracked",
         "flip_candidate": False, "verified_dynamically": "min/max state "
                                 "recorded per run"},
        {"id": "D8", "title": "clamp application site",
         "harness_site": "collective.py:671-676 (inside step)",
         "mirror_site": "exp135:263-266 (after dyn_step)",
         "class": "ordering", "active_when": "window only (both)",
         "direction": "same effective order: NO-OP",
         "flip_candidate": False, "verified_dynamically": "n/a"},
        {"id": "D9", "title": "walk order + hardcoded 8 sub-steps",
         "harness_site": "exp124:107-126 (inline BFS, range(8)); the "
                         "protocol never calls regrow, so graph.py's "
                         "round(cell_period/dt) rounding never enters",
         "mirror_site": "exp135:224-241 walk_order, WALK_SUB=8",
         "class": "step-count rounding candidate",
         "active_when": "never (counts match); g64's dt moves the walk-end "
                        "in t0, which feeds D1",
         "direction": "clears the ledger's step-rounding candidate",
         "flip_candidate": False, "verified_dynamically": "walk-end t0 "
                                 "recorded"},
        {"id": "D10", "title": "gap_scale coupling",
         "harness_site": "collective.py:655 (mu*gap_scale*lap), :97 "
                         "(gap_scale=1), G never rescaled on this protocol",
         "mirror_site": "exp135:254 mu*(lap)",
         "class": "coefficient", "active_when": "never (gap_scale == 1.0 "
                  "throughout exp124)",
         "direction": "bit-identical at gap_scale=1: clears the candidate",
         "flip_candidate": False, "verified_dynamically": "n/a"},
        {"id": "D11", "title": "theta_drivers loop",
         "harness_site": "collective.py:658-662",
         "mirror_site": "exp135 (omitted)",
         "class": "operation-presence", "active_when": "never (exp124 "
                  "installs no drivers)",
         "direction": "NO-OP", "flip_candidate": False,
         "verified_dynamically": "n/a"},
        {"id": "D12", "title": "clamp theta pull",
         "harness_site": "collective.py:675-676",
         "mirror_site": "exp135:265",
         "class": "operation-presence", "active_when": "window only (both)",
         "direction": "present in both: clears the candidate",
         "flip_candidate": False, "verified_dynamically": "n/a"},
    ]


# ------------------------------------------------- source-integrity asserts
def assert_harness_source() -> dict:
    """The diff table cites exp124/collective lines; assert the load-bearing
    lines still say what the table claims (guards against drift)."""
    src = open(os.path.join(ROOT, "experiments",
                            "exp124_deadline_curve.py")).read()
    checks = {
        "window_maybe": "t0 += dt\n        maybe(t0)\n        c.step(dt)" in src,
        "walk_8_substeps": "for _ in range(8):" in src,
        "walk_maybe": "t0 += dt\n            maybe(t0)\n            c.step(dt)" in src,
        "settle_via_run": "c.run(SETTLE_H, dt=dt)" in src,
        "branch_a": "if c.phi_spec[i] >= NEURAL_SPEC_MIN:" in src,
        "commit_noise_06": "c.rng.normal(0.0, 0.6)" in src,
    }
    assert all(checks.values()), f"harness source drift: {checks}"
    return checks


# ------------------------------------------------------------ repaired run
def run_repaired(adj: np.ndarray, gamma: float, onset: float) -> dict:
    """exp124.run_deadline VERBATIM on the real harness classes, with the
    three documented stream-preserving determinism deltas (docstring).
    Returns full diagnostics instead of a bare bool."""
    n = adj.shape[0]
    dt = star_dt(gamma, float(adj.sum(axis=1).max()))
    order = bfs_order(adj)
    canon = np.full(n, TRUNK_V)
    canon[order[:n // 4]] = HEAD_V
    target = canon.copy()
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        target[i0:i1] = z.voltage
    # delta (i): noise_std=0.0 (harness default 0.30; draw still executes)
    c = GraphCollective(adjacency=adj, seed=0, gamma=gamma,
                        mu_theta=0.015, noise_std=0.0)
    c.set_target(canon)
    c.write_spec_layer(target)
    # delta (ii): V <- canon (harness init V = theta + N(0,2); draw already
    # executed inside __init__, value discarded here — stream-preserving)
    c.V = canon.astype(float).copy()
    prog = compile_anatomy(MULTI, n=n)               # verbatim exp124:88-96
    if prog.rejected:
        return {"cell": None, "rejected": True, "break": True,
                "err": float("nan")}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])

    def maybe(t):
        if t >= onset:
            c.mu = 0.0

    t0 = 0.0
    latch_time: float | None = None
    vmin, vmax = np.inf, -np.inf
    tmin, tmax = np.inf, -np.inf

    def track():
        nonlocal vmin, vmax, tmin, tmax
        vmin = min(vmin, float(c.V.min())); vmax = max(vmax, float(c.V.max()))
        tmin = min(tmin, float(c.theta.min()))
        tmax = max(tmax, float(c.theta.max()))

    track()
    n_win = int(round(WINDOW_H / dt))
    for _ in range(n_win):                       # window: maybe() ACTIVE
        t0 += dt
        maybe(t0)
        if latch_time is None and c.mu == 0.0:
            latch_time = t0
        c.step(dt)
        track()
    c.release_clamps()
    reg_idx: list[int] = []
    for z in MULTI.zones:
        i0 = int(round(z.f0 * n))
        i1 = max(int(round(z.f1 * n)), i0 + 1)
        reg_idx.extend(range(i0, i1))
    reg_idx = sorted(set(reg_idx))
    reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
    region_set = set(reg_walk)
    c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
    track()
    wound_center = float(np.mean(c.theta[reg_walk]))
    parent_of: dict[int, int] = {}
    frontier: list[int] = []
    for i in reg_walk:
        nbrs = [j for j in np.where(c.A[i] > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(
                nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = reg_idx[:1]
        parent_of[frontier[0]] = frontier[0]
    visited = set(frontier)
    order2 = [(i, parent_of[i]) for i in frontier]
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order2.append((int(j), int(i)))
                queue.append(int(j))
    branch_base_dev = 0.0                        # D2 dynamic verification
    n_commits = 0
    for i, src in order2:                        # walk: maybe() ACTIVE
        for _ in range(8):
            t0 += dt
            maybe(t0)
            if latch_time is None and c.mu == 0.0:
                latch_time = t0
            c.step(dt)
            track()
        canon_src = getattr(c, "phi_spec_canon", None)
        if c.phi_spec[i] >= NEURAL_SPEC_MIN:
            draw = c.rng.normal(0.0, 0.6)        # delta (iii): value discarded
            theta_new = c.phi_spec[i] + 0.0 * draw
        elif canon_src is not None:
            draw = c.rng.normal(0.0, 0.6)
            theta_new = canon_src[i] + 0.0 * draw
        else:
            draw = c.rng.normal(0.0, 0.6)
            theta_new = c.theta[src] + 0.0 * draw
        branch_base_dev = max(branch_base_dev,
                              abs(float(theta_new) - float(target[i])))
        n_commits += 1
        c.theta[i] = theta_new
        c.V[i] = theta_new
        track()
    t_walk_end = t0
    c.run(SETTLE_H, dt=dt)                       # settle: NO maybe() — D1
    track()
    err = float(c.pattern_error(target))
    span = np.array(reg_walk)
    intact = np.array([i for i in range(n) if i < reg_idx[0]
                       or i > reg_idx[-1]], dtype=int)
    return {
        "cell": None, "dt": dt, "err": err,
        "err_span": float(np.sqrt(np.mean((c.V[span] - target[span]) ** 2))),
        "err_intact": float(np.sqrt(np.mean((c.V[intact]
                                             - target[intact]) ** 2))),
        "th_span_dev": float(np.sqrt(np.mean((c.theta[span]
                                              - target[span]) ** 2))),
        "x": float(np.sqrt(np.mean((c.theta[span] - target[span]) ** 2))),
        "y": float(np.sqrt(np.mean((c.V[intact] - target[intact]) ** 2))),
        "t_read": t0, "t_walk_end": t_walk_end,
        "mu_at_read": float(c.mu), "latch_time": latch_time,
        "latch_fired": latch_time is not None,
        "clip_inert_V": bool(vmin >= -90.0 - 1e-9 and vmax <= 10.0 + 1e-9),
        "clip_inert_theta": bool(tmin >= -85.0 - 1e-9 and tmax <= 5.0 + 1e-9),
        "state_min_V": vmin, "state_max_V": vmax,
        "state_min_theta": tmin, "state_max_theta": tmax,
        "commit_branch_max_base_dev": branch_base_dev,
        "n_commits": n_commits,
        "break": bool(err >= ERR_BAR),
    }


def main() -> dict:
    print("=== exp149: the mirror audit (harness re-read) ===\n")
    t_start = time.time()
    out: dict = {"exp": "exp149_mirror_audit",
                 "pre_registered": "gates O1-O4 in docstring, written "
                                   "before any run"}

    # ---- PART 1: the diff table, deposited BEFORE any repaired run
    out["source_integrity"] = assert_harness_source()
    out["diff_table"] = build_diff_table()
    out["stage"] = "diff_table_deposited_pre_run"
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"  O1 diff table: {len(out['diff_table'])} entries deposited "
          f"pre-run; flip candidate D1 (settle latch scope)", flush=True)

    battery = build_battery()
    torus = battery["torus"]
    n = torus.shape[0]
    deg_max = float(torus.sum(axis=1).max())
    out["instrument"] = {
        "n_torus": int(n), "deg_max": deg_max,
        "dt": {fmt(c): star_dt(c[0], deg_max) for c in ALL_CELLS},
        "walk_substeps": 8, "n_walk_cells": 73,
        "note": "walk-end t0 = 24 + 73*8*dt; latch scope D1 active iff "
                "onset > walk-end",
    }

    # ---- mirror-side reference: exp135.simulate live (the deposit's
    #      generator), plus the deposited-scalar reproduction check
    mirror: dict = {}
    for c in ALL_CELLS:
        mirror[c] = e135_simulate(torus, c[0], c[1])
    dep_dev = abs(mirror[LATE_CELL]["err"] - DEPOSITED_ERR_DET_G64_36)
    out["deposit_reproduction"] = {
        "deposited_err_det_g64_36": DEPOSITED_ERR_DET_G64_36,
        "live_exp135_err_g64_36": mirror[LATE_CELL]["err"],
        "abs_dev": dep_dev, "tol": DEPOSIT_TOL,
        "pass": bool(dep_dev <= DEPOSIT_TOL)}

    # ---- PART 2+3: the repaired (harness-verbatim) runs
    rows: list[dict] = []
    for c in ALL_CELLS:
        r = run_repaired(torus, c[0], c[1])
        r["cell"] = fmt(c)
        m = mirror[c]
        r["mirror_err"] = m["err"]
        r["deposited_verdict"] = ("break" if c in DEPOSITED_BREAK
                                  else "rescue")
        r["repaired_verdict"] = "break" if r["break"] else "rescue"
        r["verdict_match"] = r["deposited_verdict"] == r["repaired_verdict"]
        rows.append(r)
        print(f"  {fmt(c):>9}  dt={r['dt']:.6f}  walk_end={r['t_walk_end']:7.3f}"
              f"  latch={'@%.3f' % r['latch_time'] if r['latch_fired'] else 'NEVER':>7}"
              f"  mu_read={r['mu_at_read']:.4f}  err={r['err']:7.4f}"
              f"  (mirror {m['err']:7.4f})  {r['repaired_verdict']}"
              f"{'  MATCH' if r['verdict_match'] else '  MISMATCH'}",
              flush=True)
    out["anchors"] = rows

    # ---- O2: repair safety at the 7 non-late anchors
    fid = []
    for c in NON_LATE:
        r = next(x for x in rows if x["cell"] == fmt(c))
        d = max(abs(r[k] - mirror[c][k])
                for k in ("err", "err_span", "err_intact", "th_span_dev"))
        fid.append({"cell": fmt(c), "max_abs_scalar_diff": float(d)})
    o2 = {"per_anchor": fid,
          "max_abs_diff": max(f["max_abs_scalar_diff"] for f in fid),
          "tol": O2_TOL,
          "deposit_reproduction_pass": out["deposit_reproduction"]["pass"]}
    o2["pass"] = bool(o2["max_abs_diff"] <= O2_TOL
                      and o2["deposit_reproduction_pass"])
    out["o2_fidelity"] = o2

    # ---- O3: the flip
    late = next(x for x in rows if x["cell"] == fmt(LATE_CELL))
    others = [x for x in rows if x["cell"] != fmt(LATE_CELL)
              and x["cell"] in {fmt(c) for c in MANDATE_ANCHORS}]
    o3 = {"g64_36_repaired_err": late["err"],
          "g64_36_repaired_verdict": late["repaired_verdict"],
          "g64_36_latch_fired": late["latch_fired"],
          "g64_36_mu_at_read": late["mu_at_read"],
          "others_all_rescue": bool(all(not x["break"] for x in others)),
          "others_verdicts_match": bool(all(x["verdict_match"]
                                            for x in others))}
    o3["pass"] = bool(late["err"] >= ERR_BAR and o3["others_all_rescue"]
                      and o3["others_verdicts_match"])
    out["o3_flip"] = o3

    # ---- full-cell verdict table vs deposits
    out["verdict_table"] = {
        "n_cells": len(rows),
        "n_verdict_match": sum(r["verdict_match"] for r in rows),
        "mismatches": [r["cell"] for r in rows if not r["verdict_match"]],
    }

    # ---- PART 4 (O4, conditional): exp140's separator on repaired states
    o4: dict = {"run": bool(o3["pass"])}
    if o3["pass"]:
        xy = {fmt(c): (next(x for x in rows if x["cell"] == fmt(c))["x"],
                       next(x for x in rows if x["cell"] == fmt(c))["y"])
              for c in e140.ANCHORS}
        pb = [xy[fmt(c)] for c in e140.BREAK_CELLS]
        pr = [xy[fmt(c)] for c in e140.RESCUE_CELLS]
        sep = e140.max_margin(pb, pr)
        o4["repaired_anchors"] = [
            {"cell": fmt(c), "x": xy[fmt(c)][0], "y": xy[fmt(c)][1],
             "deposited": "break" if c in e140.BREAK_CELLS else "rescue",
             "deposited_x": None, "deposited_y": None}
            for c in e140.ANCHORS]
        # deposited mirror coordinates for movement comparison
        try:
            dep = json.load(open(os.path.join(ROOT, "results",
                                              "exp140_state_space.json")))
            dxy = {a["cell"]: (a["x"], a["y"]) for a in dep["anchors"]}
            for row in o4["repaired_anchors"]:
                # exp140's fmt is g{g}_t{t}; ours is g{g}@{t}
                dx, dy = dxy.get(row["cell"].replace("@", "_t"),
                                 (None, None))
                row["deposited_x"], row["deposited_y"] = dx, dy
                row["delta_x"] = (round(row["x"] - dx, 6)
                                  if dx is not None else None)
        except Exception as e:  # deposited coords are context, not a gate
            o4["deposit_load_error"] = repr(e)
        if sep is not None:
            w, b, dist = sep
            nw = float(np.linalg.norm(w))
            o4["separator"] = {"w": [float(w[0]), float(w[1])],
                               "b": float(b), "margin": float(dist)}
            for row in o4["repaired_anchors"]:
                s = w[0] * row["x"] + w[1] * row["y"] + b
                row["score"] = float(s)
                row["placed"] = "break" if s > 0 else "rescue"
            o4["all_placed_correctly"] = bool(all(
                (row["placed"] == row["deposited"])
                for row in o4["repaired_anchors"]))
        else:
            o4["separator"] = None
            o4["all_placed_correctly"] = False
        o4["pass"] = bool(sep is not None and o4["all_placed_correctly"])
    out["o4_separator"] = o4

    # ---- gates + verdict
    o1_pass = any(d["flip_candidate"] and d["harness_site"] and
                  d["class"] for d in out["diff_table"])
    out["gates"] = {
        "O1_diff_table_real_discrepancy": bool(o1_pass),
        "O2_repair_safety_7_anchors": o2["pass"],
        "O3_g64_36_flip": o3["pass"],
        "O4_separator_on_repaired_states": o4.get("pass", None),
    }
    n_pass = sum(1 for v in out["gates"].values() if v is True)
    if o3["pass"]:
        verdict = ("MIRROR-REPAIRED: the deterministic divergence is REAL "
                   "and identified — the harness's settle phase never "
                   "checks the mu-latch (exp124 c.run(SETTLE_H) has no "
                   "maybe()), so g64@36 is a FULL-MU run in the true "
                   "harness while the mirror silenced mid-settle; the "
                   "repaired mirror flips g64@36 to break and the "
                   "exp140 separator re-test runs on repaired states")
    elif o2["pass"]:
        verdict = ("O3-FAIL after honest O1+O2: the diff table's "
                   "discrepancies are real but none flips g64@36; the "
                   "deposit is the diff table + ranked residuals")
    else:
        verdict = ("O2-FAIL: the repair broke the non-late anchors — the "
                   "discrepancy list was wrong; deposit = diff table + "
                   "owned error")
    out["verdict"] = verdict
    out["gates_passed"] = f"{n_pass}/{len(out['gates'])}"
    out["wall_s"] = round(time.time() - t_start, 1)
    out["stage"] = "complete"
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  GATES: {out['gates']}  [{out['gates_passed']}]")
    print(f"  VERDICT: {verdict}")
    print(f"  wall {out['wall_s']}s -> {OUT}")
    return out


if __name__ == "__main__":
    main()
