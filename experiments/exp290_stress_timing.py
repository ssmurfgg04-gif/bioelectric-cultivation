#!/usr/bin/env python3
"""exp290 — THE STRESS-TIMING SPLIT: WRITE-TIME VS READ-TIME IONIC
STRESS ON THE COMMIT MACHINERY (batch 47; ledger L267's registered
next (c) — Tazumi 2026 (APA): salt exposure disrupts memory RETRIEVAL
in D. japonica while leaving storage intact — the timing split. The
stack analog is runnable as-is on the commit-noise machinery: the
ionic exposure IS the depolarized floor (the exp169 pin discipline's
own -35.0 reader-line form), and the machinery has a clean write/
read boundary — the WALK (the commits) is the storage face, the
SETTLE+DECODE is the retrieval face.)

THE ARMS (pre-named, zero new knobs — the floor values are the
machinery's own registered constants): the 72-row substituted battery
(exp256's, 12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, the
exp287/exp288 traced replica form at the production budget 8) run
under three floor states:
  A0  ANCHOR — the floor -60.0 everywhere (the production form; the
      errs reproduce exp256's deposited substituted errs BIT-EXACT
      72/72 — the S0 anchor, fail=STOP);
  A1  WRITE-STRESS — the floor pinned to -35.0 DURING THE WALK ONLY
      (from the encode window's start through the last commit), the
      floor restored to -60.0 before the settle (c.run(15.0)) and the
      decode (the settle and the read run at the production floor);
  A2  READ-STRESS — the walk at the production floor -60.0, the floor
      pinned to -35.0 for the SETTLE ONLY, restored to -60.0 before
      the decode (the read itself runs at the production floor — the
      stress is the consolidation dynamics, the retrieval face).
The pin discipline is exp169's disclosed form (the module attribute
_neural_spec_min read at step time; the restore asserted); exp142 and
the core are NOT modified — the arms set the module attribute around
the calls exactly as the reader-line pin does, disclosed.

THE READ (zero knobs): per arm the 72-row errs (the machinery's
native 2-dp convention) + err_exact; per arm the mean paired delta
vs the A0 anchor over the 72 rows (the same rows — the paired
structure); the branch pre-named:
  RETRIEVAL-SIDE  iff mean_delta(A2) < mean_delta(A1) - 0.05 (the
      read-arm degrades MORE than the write-arm by the pre-named 0.05
      mV margin — Tazumi's direction: the retrieval is the sensitive
      face);
  STORAGE-SIDE    iff mean_delta(A1) < mean_delta(A2) - 0.05;
  SYMMETRIC-INERT otherwise (the two faces indistinguishable at the
      machinery's resolution — an honest null).
Audit-only: the per-row paired delta table per arm, the per-host mean
deltas, the outliers H3/H5's deltas (the exp273 pre-name), the
worst-err per arm vs the 6.0 bar (unchanged), the commit censuses per
arm (the spec/canon/parent tags — the floor's effect on the (e)
branch, disclosed), the trace shas per arm (the walks differ across
arms by construction — the anchor is the A0 arm only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: A0's errs reproduce exp256's deposited substituted
      errs BIT-EXACT 72/72 (the verified flags 72/72) AND exp282's
      walk_end_rms bit-exact (the trace sha256 72/72); the floor
      asserts: the floor reads -60.0 at the encode start per row in
      A0/A2 and -35.0 during the walk in A1 (recorded per row,
      asserted); the source deposits READ-ONLY (exp243/256/272/273/
      282/287/288 — 7 deposits, the sha-recorded before/after form).
  G2  THE ARMS' INTEGRITY (zero-knob asserted, fail=STOP per row):
      every row's errs finite; the A3 convention (round(err_exact, 2)
      == the reported err) 72/72 per arm; the trace lengths ==
      walk_steps 72/72 per arm; the S* lock reads 216 (3 arms x 72);
      the commit counts == walk_steps per arm 72/72; the pin restore
      asserted at the settle boundary per row (the floor reads -60.0
      at the settle start in A1, -35.0 in A2, -60.0 at the decode in
      both — recorded, fail=STOP).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars above):
      the paired deltas over the 72 rows per arm; RETRIEVAL-SIDE /
      STORAGE-SIDE / SYMMETRIC-INERT by the 0.05 mV margin form.
  G4  THE DISCIPLINE: deterministic (the arms are pure floor-state
      schedules over the same seed stream — the in-process form runs
      the 3 arms sequentially, 216 decodes ~ 3-4 min, under the 570 s
      cap; the checkpoint-split EXP290_MODE=pass1|pass2 + merge is
      the pre-named alternative); no wall-clock fields; the docstring
      + header pinned to this pre-registration commit, asserted at
      entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): RETRIEVAL-SIDE / STORAGE-SIDE /
SYMMETRIC-INERT.

RUN: 216 decodes ~ 3-4 min foreground (in-process), or the
checkpoint-split form. Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp290_stress_timing.json")


def main() -> dict:
    # ==== BODY (written under the body-only discipline; the docstring +
    #      header above byte-unchanged, pinned to pre-registration commit
    #      982cb81; gates G1-G4 evaluated exactly once) ==================
    import hashlib
    import json

    import numpy as np

    import cultivation.bioelectric.collective as CORE  # the floor's home
    import experiments.exp142_sign_read as _m142       # the walk's home —
                                                       # NOT modified
    import experiments.exp145_phase_read as _m145
    import experiments.exp148_temporal_read as _m148
    import experiments.exp94_multizone_scale as _m94
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone, compile_anatomy)
    from cultivation.substrate.graph import GraphCollective  # noqa: E402
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp90_two_source_read import star_dt  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)
    from experiments.exp142_sign_read import (  # noqa: E402
        COMMIT_NOISE, ERR_BAR, STEPS_PER_CELL, STAR_OP, WINDOW_H)
    from experiments.exp145_phase_read import (  # noqa: E402
        project_phase_native, warnings_as_errors)
    from experiments.exp148_temporal_read import flip_clock_matrix  # noqa: E402
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp198_adversarial_reader_n400 import (  # noqa: E402
        N400, SEEDS as SEEDS_N400)

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the 982cb81 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "cdf24a5e1bcc9c7abe3bc1ee19f915ac09272430c31dd6b209ad1394b57af83c")
    EXPECTED_HEADER_SHA256 = (
        "447b2da7596f6d9e319b1cb6fbb44a3d2f5b900e1aecfee3486c50b8fe35c491")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 982cb81"
    assert header_ok, "header drifted from 982cb81"

    # ---- the -60.0 floor (G4: asserted at exit; exp218's disclosed
    #      exp169-import discipline — the whole reader chain imported
    #      FIRST, the floor restored after; exp167's import-time
    #      instrument pin is -35.0, disclosed in floor_at_entry) --------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)   # exp169's PIN_MODULES form
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    _PRE_RESTORE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in PINNED}

    def set_floor(v):
        # exp169's disclosed pin form: the module attribute set around
        # the calls (exp142 and the core NOT modified — the attribute is
        # READ AT STEP TIME by the walk's commit branch (e))
        for _m in PINNED:
            if hasattr(_m, "NEURAL_SPEC_MIN"):
                _m.NEURAL_SPEC_MIN = float(v)

    def read_floor():
        vals = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                for m in PINNED}
        uv = set(float(v) for v in vals.values())
        assert len(uv) == 1, f"the pinned floor set disagrees: {vals}"
        return uv.pop()

    set_floor(PROD_FLOOR)
    assert read_floor() == PROD_FLOOR, "floor restore failed"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (core)"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    # ---- the frozen read configuration (exp256's battery constants;
    #      the replica's executor constants asserted = exp142's own;
    #      THE BRANCH BAR — the pre-named 0.05 mV margin) ----------------
    REWIRE_P = 0.10                        # exp225's corpus rewire p
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    ARM_SUBST = "substituted"
    P3 = "P3_deep_band_substitution"
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert SEEDS_RUN == (1, 2, 3), "seed-line drift"
    assert len(SEEDS_RUN) == 3, "the pre-registration's 3 seeds"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        "the read drifted off S*"
    assert (WINDOW_H, COMMIT_NOISE, STEPS_PER_CELL, ERR_BAR) == (
        _m142.WINDOW_H, _m142.COMMIT_NOISE, _m142.STEPS_PER_CELL,
        _m142.ERR_BAR), "the executor constants drifted from exp142's"
    # THE BUDGET (the production default): the replica runs at exp142's
    # STEPS_PER_CELL == 8 — the exp287/exp288 traced replica form at the
    # production budget (no ladder: the question is the floor's TIMING,
    # not the budget).
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE THREE ARMS (pre-named schedules; the floor values are the
    # machinery's own registered constants -60.0 / -35.0):
    ARMS = ("A0", "A1", "A2")
    ARM_NAMES = {"A0": "anchor (-60.0 everywhere)",
                 "A1": "write-stress (-35.0 during the walk only)",
                 "A2": "read-stress (-35.0 during the settle only)"}
    MARGIN = 0.05                          # the pre-named 0.05 mV bar
    # THE FLOOR SCHEDULE per arm (recorded at five boundaries per row and
    # asserted fail=STOP — G1's encode/walk facets, G2's settle/decode
    # facets):
    FLOOR_SCHEDULE = {
        "A0": {"encode_start": PROD_FLOOR,
               "walk_first_commit": PROD_FLOOR,
               "walk_last_commit": PROD_FLOOR,
               "settle_start": PROD_FLOOR,
               "decode_start": PROD_FLOOR},
        "A1": {"encode_start": READER_PIN_FLOOR,
               "walk_first_commit": READER_PIN_FLOOR,
               "walk_last_commit": READER_PIN_FLOOR,
               "settle_start": PROD_FLOOR,
               "decode_start": PROD_FLOOR},
        "A2": {"encode_start": PROD_FLOOR,
               "walk_first_commit": PROD_FLOOR,
               "walk_last_commit": PROD_FLOOR,
               "settle_start": READER_PIN_FLOOR,
               "decode_start": PROD_FLOOR}}
    # the commit source tags (the pre-named census; audit-only — the
    # floor's effect on the (e) branch, disclosed)
    COMMIT_SOURCES = ("spec", "canon", "parent")

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
        _LOCK_LOG.append((host, row_key, int(seed)))

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    def _a_sha(A):
        return hashlib.sha256(np.ascontiguousarray(
            np.abs(np.asarray(A, dtype=float)),
            dtype=np.float64).tobytes()
        ).hexdigest()

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; SEVEN deposits:
    #      exp243 + exp256 + exp272 + exp273 + exp282 + exp287 + exp288) -
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP282 = os.path.join(ROOT, "results",
                          "exp282_trajectory_structure.json")
    DEP287 = os.path.join(ROOT, "results",
                          "exp287_fixed_point_identity.json")
    DEP288 = os.path.join(ROOT, "results",
                          "exp288_spec_layer_face.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287, DEP288)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit",
                  DEP288: "exp288_deposit"}
    ro_before = {name: _sha(p) for p, name in _dep_names.items()}

    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP272) as fh:
        dep272 = json.load(fh)
    with open(DEP273) as fh:
        dep273 = json.load(fh)
    with open(DEP282) as fh:
        dep282 = json.load(fh)
    with open(DEP287) as fh:
        dep287 = json.load(fh)
    with open(DEP288) as fh:
        dep288 = json.load(fh)

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep287["hosts"] == hosts, "exp287's host frame drifted"
    assert dep288["hosts"] == hosts, "exp288's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    cluster = [h for h in hosts if h not in outliers]
    assert len(cluster) == 10, "the ten-host cluster drifted"

    rec272 = {r["host"]: r for r in dep272["per_host"]}

    # ---- exp208's classify VERBATIM (used only by the rebuild's
    #      boundary-count asserts, the exp288 form) -----------------------
    def classify(T: np.ndarray, W: np.ndarray) -> dict:
        n = len(T)
        Td = np.asarray(T, dtype=float)
        bnd = np.zeros(n, dtype=bool)
        for i in range(n):
            if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                bnd[i] = True
        support = np.abs(W) > 0
        iu = np.triu_indices(n, 1)
        deg = np.zeros(n, dtype=int)
        for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
            deg[a] += 1
            deg[b] += 1
        pj = deg >= 2
        cls = np.zeros(n, dtype=int)
        cls[pj] = 1
        cls[bnd] = 0
        return {"boundary": bnd, "junction": pj & ~bnd,
                "interior": ~(bnd | pj), "class": cls}

    # ---- the MEDIUM (exp256's HostWMedium VERBATIM) ---------------------
    class HostWMedium:
        kind = "host_w_structured"

        def __init__(self, A):
            self.A = np.asarray(A, dtype=float)
            self.n = int(self.A.shape[0])

        def snapshots(self):
            return [self.A.copy()]

        def native_support(self):
            return (np.abs(self.A) > 0).astype(float)

        @property
        def violated(self):
            return ()

    # ---- THE TRACED REPLICA WITH THE ARM SCHEDULE: exp286's landed
    #      _execute_signed_traced REUSED VERBATIM (exp142's walk
    #      byte-similar + exactly the disclosed recording additions
    #      (a)-(f), exp287's commit recording included) at the production
    #      budget, PLUS exactly the pre-named arm schedule: the floor set
    #      around the calls in exp169's disclosed pin form (the module
    #      attribute read AT STEP TIME by the commit branch (e)); the
    #      floor reads are pure recording (no RNG, no state) and the
    #      A0 arm never pins (bit-exactness preserved — proven by the S0
    #      anchors below). ------------------------------------------------
    def _execute_signed_traced_arm(spec, adjacency, seed, op, budget, arm):
        floor_rec: dict = {}
        n = adjacency.shape[0]
        gamma, mu = op["gamma"], op["mu"]
        absA = np.abs(adjacency)
        dt = star_dt(gamma, float(absA.sum(axis=1).max()))           # R1
        canon = labeling_bfs_n(absA)                                 # R1
        target = spec_target_n(spec, canon, n)
        c = GraphCollective(adjacency=adjacency, seed=seed, gamma=gamma,
                            mu_theta=mu)                             # R2 (signed)
        c.set_target(canon)
        c.write_spec_layer(target)
        prog = compile_anatomy(spec, n=n)
        if prog.rejected:
            return {"program_verified": False, "rejected": prog.rejected,
                    "err_vs_target": float("nan"),
                    "walk_trace": [], "walk_steps": 0,
                    "commits": [], "coverage_ok": False,
                    "floor_rec": floor_rec}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        # ---- THE ARM PIN (A1 only): the write-stress floor goes on at
        #      the ENCODE WINDOW's start, through the last commit (the
        #      pre-named schedule; A0/A2 run the encode at -60.0) -------
        if arm == "A1":
            set_floor(READER_PIN_FLOOR)
        floor_rec["encode_start"] = read_floor()
        c.run(WINDOW_H, dt=dt)
        c.release_clamps()
        reg_idx: list[int] = []
        for z in spec.zones:
            i0 = int(round(z.f0 * n))
            i1 = max(int(round(z.f1 * n)), i0 + 1)
            reg_idx.extend(range(i0, i1))
        reg_idx = sorted(set(reg_idx))
        trace: list = []                       # (b) the disclosed addition
        order: list = []                       # (d) the disclosed no-op init
        commits: list = []                     # (f) exp287's disclosed
                                               #     recording addition
        if reg_idx:
            reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
            region_set = set(reg_walk)
            c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
            wound_center = float(np.mean(c.theta[reg_walk]))
            parent_of: dict[int, int] = {}
            frontier: list[int] = []
            # exp97's blastema frontier under R1 (exp142 verbatim)
            for i in reg_walk:
                nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                        if j not in region_set]
                if nbrs:
                    parent_of[i] = int(max(
                        nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
                    frontier.append(i)
            if not frontier:
                frontier = reg_idx[:1]
                parent_of[frontier[0]] = frontier[0]
            visited = set(frontier)
            order = [(i, parent_of[i]) for i in frontier]
            queue = list(frontier)
            while queue:
                i = queue.pop(0)
                for j in np.where(np.abs(c.A[i]) > 0)[0]:        # R1
                    if int(j) in region_set and int(j) not in visited:
                        visited.add(int(j))
                        parent_of[int(j)] = int(i)
                        order.append((int(j), int(i)))
                        queue.append(int(j))
        first_commit_done = False
        for i, src in order:
            for _ in range(budget):                  # the landed
                c.step(dt)                           # parameterization
            canon_src = getattr(c, "phi_spec_canon", None)
            # ---- (e) THE FLOOR READ AT STEP TIME: the commit branch
            #      reads the module attribute live — A1's pin (-35.0)
            #      re-routes the sub-floor spec cells to the canon
            #      fallback; A0/A2 read -60.0 -----------------------------
            if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "spec"
            elif canon_src is not None:
                theta_new = canon_src[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "canon"
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "parent"
            c.theta[i] = theta_new
            c.V[i] = theta_new
            # ---- (f) exp287's disclosed recording addition --------------
            commits.append((int(i), float(theta_new), src_tag))
            if not first_commit_done:
                floor_rec["walk_first_commit"] = read_floor()
                first_commit_done = True
            # ---- (a) the per-step RMS read (a pure read; the walk's
            #      full-frame convergence; unchanged) ---------------------
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        floor_rec["walk_last_commit"] = read_floor()
        # the write-set coverage (the replica's side, the walk order in
        # scope): the commit sequence elementwise == the walked order
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        # ---- THE SETTLE BOUNDARY (G2's pin-restore point): A1 restored
        #      to -60.0 before the settle; A2 pinned to -35.0 for the
        #      settle only -----------------------------------------------
        if arm == "A1":
            set_floor(PROD_FLOOR)
        elif arm == "A2":
            set_floor(READER_PIN_FLOOR)
        floor_rec["settle_start"] = read_floor()
        c.run(15.0, dt=dt)
        # ---- THE DECODE BOUNDARY: A2 restored to -60.0 before the
        #      decode (the read itself runs at the production floor) ----
        if arm == "A2":
            set_floor(PROD_FLOOR)
        floor_rec["decode_start"] = read_floor()
        per_zone = {}
        ok_all = True
        for z in spec.zones:
            i0 = int(round(z.f0 * n))
            i1 = max(int(round(z.f1 * n)), i0 + 1)
            zmean = float(np.mean(c.V[i0:i1]))
            ok = abs(zmean - z.voltage) <= ERR_BAR
            per_zone[z.name] = {"mean": round(zmean, 1), "ok": bool(ok)}
            ok_all &= ok
        err = float(c.pattern_error(target))
        ok_all &= err < ERR_BAR
        out = {"program_verified": bool(ok_all), "per_zone": per_zone,
               "err_vs_target": round(err, 2),
               "walk_trace": trace,                    # (b)
               "walk_steps": len(order)}               # (b)
        out["final_state"] = {"V": c.V.tolist(),       # (c) always carried
                              "target": target.tolist()}
        out["commits"] = commits                       # (f)
        out["coverage_ok"] = coverage_ok               # (f)
        out["floor_rec"] = floor_rec
        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced + budgeted + armed
    #      executor call) --------------------------------------------------
    def _scoped_row_read_traced_arm(spec, med, seed, fmax, budget, arm):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)  # PN1+PN2
                F = flip_clock_matrix(inner)       # TC1
            else:
                A, rho, branch = project_phase_native(med)    # PN1+PN2
                F = flip_clock_matrix(med)         # TC1
            A_ext = A + F                          # TC2 (zero knobs)
            assert not np.iscomplexobj(A_ext), \
                "TC2 must deliver a real matrix"
            out = _execute_signed_traced_arm(spec, A_ext, seed, op=STAR_OP,
                                             budget=budget, arm=arm)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one decode (the arm read + the per-row asserts, fail=STOP) ----
    def _decode_row(arm, host, row_key, spec, med, seed, fmax,
                    dep_rec, rec282, rec287, rec288):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced_arm(spec, med, seed, fmax, BUDGET,
                                          arm)
        floor_rec = out["floor_rec"]
        # ---- THE FLOOR SCHEDULE (G1's encode/walk facets + G2's
        #      settle/decode facets, asserted per row, fail=STOP) --------
        for k, v in FLOOR_SCHEDULE[arm].items():
            got = floor_rec.get(k)
            assert got == v, \
                (f"{host} {row_key} s{seed} {arm}: the floor at {k} read "
                 f"{got} != the pre-named {v} (fail=STOP)")
        floor_schedule_ok = bool(all(floor_rec.get(k) == v
                                     for k, v in FLOOR_SCHEDULE[arm].items()))
        err = float(out["err_vs_target"])
        assert np.isfinite(err), f"{host} {row_key} s{seed}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, f"{host} {row_key} s{seed}: A3 state-convention drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        trace_len_ok = bool(len(trace) == steps and steps >= 1)
        assert trace_len_ok, \
            f"{host} {row_key} s{seed}: trace {len(trace)} != walk steps {steps}"
        all_finite = bool(all(np.isfinite(trace)))
        assert all_finite, \
            f"{host} {row_key} s{seed}: non-finite trace entry"
        final = trace[-1]
        final_positive_ok = bool(final > 0.0)
        assert final_positive_ok, \
            f"{host} {row_key} s{seed}: final RMS == 0"
        # TA3 — the convergence point (existence; exp282's assert form)
        thresh = 2.0 * final
        conv = None
        for kk, v in enumerate(trace):
            if v < thresh:
                conv = kk
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            f"{host} {row_key} s{seed}: the convergence point does not exist"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        # ---- THE COMMIT RECORDING (G2, zero-knob asserted, fail=STOP) --
        commits = out["commits"]
        n_commits = len(commits)
        commits_count_ok = bool(n_commits == steps == len(trace))
        assert commits_count_ok, \
            (f"{host} {row_key} s{seed}: the commit count {n_commits} != "
             f"walk steps {steps} — the write set is not fully recorded")
        idxs = [int(rec[0]) for rec in commits]
        commits_unique_ok = bool(len(set(idxs)) == n_commits)
        assert commits_unique_ok, \
            (f"{host} {row_key} s{seed}: a committed cell written twice — "
             "the commit sequence is not a clean write record")
        coverage_ok = bool(out["coverage_ok"])
        assert coverage_ok, \
            f"{host} {row_key} s{seed}: the write-set coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        commits_finite_ok = bool(all(np.isfinite(v) for v in vals))
        assert commits_finite_ok, \
            f"{host} {row_key} s{seed}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        census_ok = bool(sum(census_src.values()) == n_commits
                         and set(tags) <= set(COMMIT_SOURCES))
        assert census_ok, \
            f"{host} {row_key} s{seed}: the commit source census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        # the commit layer's self-consistency read (audit-only, the
        # exp287 replay form — the floor's effect on the commit layer,
        # disclosed)
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        assert np.isfinite(sc_rms), \
            f"{host} {row_key} s{seed}: non-finite self-consistency RMS"
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite commit-vs-target RMS"
        denom_ok = bool(err_exact > 0.0)
        assert denom_ok, \
            f"{host} {row_key} s{seed}: the program-vs-target gap == 0"
        sc_frac = float(sc_rms / err_exact)

        rec = {"arm": arm, "host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "err": err,
               "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "trace_len_ok": trace_len_ok,
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "n_commits": n_commits,
               "commits_count_ok": commits_count_ok,
               "commits_unique_ok": commits_unique_ok,
               "coverage_ok": coverage_ok,
               "commits_finite_ok": commits_finite_ok,
               "census_ok": census_ok,
               "commit_seq_sha256": commit_sha,
               "src_census": census_src,
               "sc_rms": sc_rms, "sc_finite_ok": True,
               "sc_frac": sc_frac, "denom_ok": denom_ok,
               "cvt_rms": cvt_rms,
               "floor_rec": {k: float(v) for k, v in floor_rec.items()},
               "floor_schedule_ok": floor_schedule_ok}
        if arm == "A0":
            # ---- THE S0 ANCHOR (G1, fail=STOP): the A0 arm IS the
            #      production form — exp256's deposited errs, exp282's
            #      walks reproduce BIT-EXACT -----------------------------
            s0_err_ok = bool(err == dep_rec["err"])
            s0_ver_ok = bool(bool(out["program_verified"])
                             == bool(dep_rec["verified"]))
            assert s0_err_ok, \
                (f"{host} {row_key} s{seed}: the fresh err {err} drifted "
                 f"from exp256's deposited {dep_rec['err']} — S0 REFUTED")
            assert s0_ver_ok, \
                f"{host} {row_key} s{seed}: the verified flag drifted"
            we_ok = bool(final == float(rec282["walk_end_rms"]))
            assert we_ok, \
                (f"{host} {row_key} s{seed}: the fresh walk_end_rms "
                 "drifted from exp282's deposited walk_end_rms")
            ts_ok = bool(trace_sha == rec282["trace_sha256"])
            assert ts_ok, \
                (f"{host} {row_key} s{seed}: the fresh trace sha drifted "
                 "from exp282's deposited trace sha — the walk is not "
                 "the traced one")
            ee_ok = bool(err_exact == float(rec282["err_exact"]))
            assert ee_ok, \
                (f"{host} {row_key} s{seed}: the fresh err_exact drifted "
                 "from exp282's deposited err_exact")
            rec["s0_err_ok"] = s0_err_ok
            rec["s0_verified_ok"] = s0_ver_ok
            rec["walk_end_282_ok"] = we_ok
            rec["trace_sha_282_ok"] = ts_ok
            rec["err_exact_282_ok"] = ee_ok
            # the commit-layer digests vs the anchored deposits
            # (exp287/exp288 — AUDIT-ONLY for exp290: G1's binding text
            # names the errs + the verified flags + the walk anchors)
            rec["commit_sha_287_ok"] = bool(
                commit_sha == rec287["commit_seq_sha256"])
            rec["commit_sha_288_ok"] = bool(
                commit_sha == rec288["commit_seq_sha256"])
            rec["cvt_287_ok"] = bool(cvt_rms == float(rec287["cvt_rms"]))
        return rec

    # ---- THE COMPUTATION (the sha-asserted rebuild + the fresh
    #      3-arm x 72-row battery at the production budget + the
    #      determinism canary; the integrity section is a pure function
    #      of the deposits and is bit-compared across the split passes) -
    def _compute_arms(arms):
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (the exp269/exp280/exp284/exp285/exp286/
        #      exp287/exp288 form, every rebuild bit-asserted against
        #      exp243's OWN records) --------------------------------------
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_canon_ok": 0, "h0_echo_h1": False, "n_fmax_ok": 0,
                  "n_nonneg_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
                  "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
                  "n_medium_shas_ok": 0, "n_rows282": 0,
                  "n_282_chain_ok": 0, "n_rows287": 0, "n_rows288": 0}
        bases = {}
        rebuild_report = []
        for h in hosts:
            rec = dep243["classes"][h]
            n = int(rec["n"])
            assert n == int(N400), f"{h}: n drift vs exp198's N400"
            if h in ("H0", "H1"):
                A = graph_path(N400)     # the chain/path constructor
            else:
                A = small_world(N400, REWIRE_P, int(rec["rewire_seed"]))
            assert A.sum() > 0, f"{h}: the rebuilt base is empty"
            nonneg = bool(float(np.min(A)) >= 0.0)
            assert nonneg, f"{h}: the base carries negative entries"
            sha_ok = bool(_a_sha(A) == rec["base_sha256"])
            edges = int(np.count_nonzero(np.triu(A, 1)))
            edges_ok = bool(edges == int(rec["edges_base"]))
            canon = labeling_bfs_n(np.abs(A))
            canon_ok = bool(np.array_equal(labeling_bfs_n(A), canon))
            nb = int(classify(canon, A)["boundary"].sum())
            bnd_ok = bool(nb == int(rec["n_boundary_cells_base"]))
            bnd_dual = bool(
                nb == int(rec272[h]["n_boundary_cells_base"]))
            assert sha_ok and edges_ok and bnd_ok and bnd_dual \
                and canon_ok, \
                f"{h}: the rebuild drifted from exp243's records"
            fmax = float(f_max_frames(list(HostWMedium(A).snapshots())))
            fmax_ok = bool(fmax == float(rec["f_max_base"]))
            assert fmax_ok, f"{h}: f_max drifted from exp243's deposit"
            # the two deep-row targets (exp256's build_rows deep
            # construction — exp214's deep form VERBATIM)
            deep = {}
            for inst in DEEP_INSTANCES:
                zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
                      for z in MULTI.zones]
                spec = AnatomySpec(
                    zones=[Zone(f0=a, f1=b, voltage=DEEP_RUNG, name=nm)
                           for (a, b, nm) in zs],
                    amputate_plane=MULTI.amputate_plane,
                    spec_name=f"ms-multi-deep-i{inst}",
                    somatic_latch=MULTI.somatic_latch)
                f = spec_target_n(spec, canon, N400)
                deep[inst] = {"spec": spec, "f": f, "sha": _f_sha(f)}
            bases[h] = {"A": A, "n": n, "edges": edges, "canon": canon,
                        "fmax": fmax, "deep": deep}
            counts["n_hosts"] += 1
            counts["n_sha_ok"] += int(sha_ok)
            counts["n_edges_ok"] += int(edges_ok)
            counts["n_canon_ok"] += int(canon_ok)
            counts["n_fmax_ok"] += int(fmax_ok)
            counts["n_nonneg_ok"] += int(nonneg)
            rebuild_report.append({
                "host": h, "n": n,
                "constructor": ("graph_path (the chain/path constructor)"
                                if h in ("H0", "H1") else
                                "small_world(n, 0.10, rewire_seed)"),
                "rewire_seed": (None if rec["rewire_seed"] is None
                                else int(rec["rewire_seed"])),
                "sha256_matches_exp243_record": sha_ok,
                "edges_base": edges,
                "edges_match_exp243_record": edges_ok,
                "n_boundary_cells": nb,
                "boundary_count_matches_2way": bool(bnd_ok and bnd_dual),
                "canon_identity_ok": canon_ok,
                "f_max_matches_exp243_record": fmax_ok,
                "base_non_negative": nonneg})
        counts["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                                   bases["H1"]["A"]))
        assert counts["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        # ---- G1: exp256's 72 rows — the substituted records the S0
        #      anchor reads, complete with the instance structure -----
        rows256 = dep256["rows"]
        counts["n_rows256"] = len(rows256)
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        dep_sub = {}
        for r in rows256:
            if r["arm"] != ARM_SUBST:
                continue
            insts = r["instances"]
            inst_perts = sorted(i["pert"] for i in insts)
            keys = sorted(i["row_key"] for i in insts)
            struct_ok = bool(
                inst_perts == [P3, P3]
                and keys == sorted(f"r{DEEP_RUNG:g}i{i}"
                                   for i in DEEP_INSTANCES)
                and all(i["medium"] == "base" for i in insts))
            werr = float(r["worst_err"])
            wmax = max(float(i["err"]) for i in insts)
            counts["n_structure_ok"] += int(struct_ok)
            counts["n_worst_eq_max"] += int(werr == wmax)
            assert struct_ok, \
                f"{r['host']} s{r['seed']}: the substituted structure drifted"
            for i in insts:
                dep_sub[(r["host"], int(r["seed"]), i["row_key"])] = {
                    "err": float(i["err"]), "verified": bool(i["verified"]),
                    "medium_sha256": i["medium_sha256"],
                    "row_target_sha256": i["row_target_sha256"]}
        assert len(dep_sub) == 72, \
            "the 72 substituted instance records drifted"
        assert counts["n_structure_ok"] == 36 \
            and counts["n_worst_eq_max"] == 36, \
            "the substituted arm split drifted"
        for h in hosts:
            rec_sha = dep243["classes"][h]["base_sha256"]
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                for s in SEEDS_RUN:
                    d = dep_sub[(h, s, rk)]
                    ok_t = bool(d["row_target_sha256"]
                                == bases[h]["deep"][inst]["sha"])
                    ok_m = bool(d["medium_sha256"] == rec_sha)
                    assert ok_t and ok_m, \
                        f"{h} {rk} s{s}: the deep rebuild drifted"
                    counts["n_deep_targets_ok"] += int(ok_t)
                    counts["n_medium_shas_ok"] += int(ok_m)
        assert counts["n_deep_targets_ok"] == 72 \
            and counts["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # ---- G1: THE EXP282 RE-READ (the walk anchor deposit) ---------
        rows282 = dep282["rows"]
        counts["n_rows282"] = len(rows282)
        assert len(rows282) == 72, "exp282's 72-row deposit drifted"
        assert dep282["branch"] == "TRAJECTORY-CARRIED", \
            "exp282's deposited branch drifted from TRAJECTORY-CARRIED"
        r282 = {}
        n_chain282 = 0
        for r in rows282:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r282, f"duplicate exp282 row {key}"
            assert all(fld in r for fld in
                       ("trace_sha256", "walk_end_rms", "err_deposited",
                        "err_exact", "walk_steps")), \
                f"{key}: exp282's row record is missing anchor fields"
            d256 = dep_sub[key]
            ok_chain = bool(float(r["err_deposited"]) == d256["err"])
            assert ok_chain, \
                (f"{key}: exp282's err_deposited drifted from exp256's "
                 "deposited substituted err — the two deposits' chain "
                 "anchor broken")
            n_chain282 += int(ok_chain)
            r282[key] = r
        counts["n_282_chain_ok"] = n_chain282
        assert counts["n_282_chain_ok"] == 72, \
            "exp282's err chain anchor drifted"

        # ---- G1: THE EXP287 + EXP288 RE-READS (the commit-layer
        #      anchor deposits; audit-only for exp290's A0 arm) ---------
        rows287 = dep287["rows"]
        counts["n_rows287"] = len(rows287)
        assert len(rows287) == 72, "exp287's 72-row deposit drifted"
        r287 = {}
        for r in rows287:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r287, f"duplicate exp287 row {key}"
            assert "commit_seq_sha256" in r and "cvt_rms" in r, \
                f"{key}: exp287's row record is missing anchor fields"
            r287[key] = r
        rows288 = dep288["rows"]
        counts["n_rows288"] = len(rows288)
        assert len(rows288) == 72, "exp288's 72-row deposit drifted"
        r288 = {}
        for r in rows288:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r288, f"duplicate exp288 row {key}"
            assert "commit_seq_sha256" in r, \
                f"{key}: exp288's row record is missing the commit digest"
            r288[key] = r

        # ---- THE FRESH THREE-ARM BATTERY: 3 x 72 substituted rows at
        #      the production budget (the S0 anchors on EVERY A0 row,
        #      fail=STOP; the arm order is the pre-named A0 -> A1 -> A2;
        #      the arms are pure floor-state schedules over the same
        #      seed stream — each decode carries its own GraphCollective
        #      seed, the order carries no state) --------------------------
        rows_by_arm: dict = {}
        first_args: dict = {}
        for arm in arms:
            assert arm in ARMS, f"unknown arm {arm}"
            rows_out: list = []
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_row(
                            arm, k, rk, ctx["deep"][inst]["spec"],
                            med, s, ctx["fmax"], dep_sub[(k, s, rk)],
                            r282[(k, s, rk)], r287[(k, s, rk)],
                            r288[(k, s, rk)])
                        rows_out.append(rec)
                        if arm not in first_args:
                            first_args[arm] = (k, rk,
                                               ctx["deep"][inst]["spec"],
                                               med, s, ctx["fmax"])
                hs = [r for r in rows_out if r["host"] == k]
                print(f"  [{arm} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | src "
                      f"{ {t: sum(r['src_census'][t] for r in hs) for t in COMMIT_SOURCES} }",
                      flush=True)
            assert len(rows_out) == 72, \
                f"the {arm} battery produced {len(rows_out)} rows != 72"
            rows_by_arm[arm] = rows_out
        assert len(_LOCK_LOG) == 72 * len(arms), \
            (f"the S* lock count {len(_LOCK_LOG)} != "
             f"{72 * len(arms)} reads")

        # ---- THE DETERMINISM CANARY (G4's evaluable determinism: each
        #      arm's first row re-decoded bit-exactly; the canary's S*
        #      re-read truncated from the log — the 216 battery reads
        #      are the counted ones, disclosed) ---------------------------
        canary = []
        for arm in arms:
            k, rk, spec_o, med_o, s, fmax_o = first_args[arm]
            r1 = rows_by_arm[arm][0]
            assert (r1["host"], r1["row_key"], int(r1["seed"])) == \
                (k, rk, s), "the canary's first-row args drifted"
            mark = len(_LOCK_LOG)
            r2 = _decode_row(arm, k, rk, spec_o, med_o, s, fmax_o,
                             dep_sub[(k, s, rk)], r282[(k, s, rk)],
                             r287[(k, s, rk)], r288[(k, s, rk)])
            del _LOCK_LOG[mark:]
            same = bool(
                r2["err"] == r1["err"]
                and r2["err_exact"] == r1["err_exact"]
                and r2["trace_sha256"] == r1["trace_sha256"]
                and r2["commit_seq_sha256"] == r1["commit_seq_sha256"]
                and r2["walk_end_rms"] == r1["walk_end_rms"]
                and r2["walk_steps"] == r1["walk_steps"]
                and r2["floor_rec"] == r1["floor_rec"]
                and r2["src_census"] == r1["src_census"])
            assert same, \
                f"the determinism canary failed on {arm} {k} {rk} s{s}"
            canary.append({"arm": arm, "host": k, "seed": int(s),
                           "row_key": rk, "bit_identical": same})
        assert len(_LOCK_LOG) == 72 * len(arms), \
            "the S* lock count drifted after the canary truncation"

        integrity = {"counts": counts, "rebuild_report": rebuild_report,
                     "exp256_reread": {
                         "n_rows": counts["n_rows256"],
                         "n_substituted_instance_records": len(dep_sub),
                         "n_structure_ok": counts["n_structure_ok"],
                         "n_worst_eq_max": counts["n_worst_eq_max"],
                         "n_deep_targets_ok": counts["n_deep_targets_ok"],
                         "n_medium_shas_ok": counts["n_medium_shas_ok"]},
                     "exp282_reread": {"n_rows": counts["n_rows282"],
                                       "branch": dep282["branch"],
                                       "n_chain_ok": counts["n_282_chain_ok"]},
                     "exp287_reread": {"n_rows": counts["n_rows287"]},
                     "exp288_reread": {"n_rows": counts["n_rows288"],
                                       "branch": dep288["branch"]}}
        return {"rows_by_arm": rows_by_arm, "integrity": integrity,
                "lock_reads": len(_LOCK_LOG), "canary": canary,
                "ro_before": ro_before}

    # ---- THE ASSEMBLY (the paired-delta read + the branch + the gate
    #      tallies; identical for the in-process and the merge paths) ----
    def _assemble(rows_by_arm, integrity, lock_total, canary,
                  ro_before_pass):
        assert set(rows_by_arm.keys()) == set(ARMS), \
            "the assembled arm frame drifted"
        for arm in ARMS:
            assert len(rows_by_arm[arm]) == 72, \
                f"the {arm} battery produced {len(rows_by_arm[arm])} != 72"
        E = {}
        for arm in ARMS:
            d = {}
            for r in rows_by_arm[arm]:
                key = (r["host"], int(r["seed"]), r["row_key"])
                assert key not in d, f"duplicate {arm} row {key}"
                d[key] = r
            E[arm] = d
        assert set(E["A0"]) == set(E["A1"]) == set(E["A2"]), \
            "the paired key frame drifted across the arms"
        assert len(E["A0"]) == 72, "the 72-row paired frame drifted"
        assert lock_total == 216, \
            f"the S* lock count {lock_total} != 216 (3 arms x 72)"
        assert all(c["bit_identical"] for c in canary), \
            "the determinism canary drifted"

        # ---- the per-arm summaries (the zero-knob tallies, G2) ---------
        tallies = {}
        for arm in ARMS:
            rows = rows_by_arm[arm]
            errs = [float(r["err"]) for r in rows]
            tallies[arm] = {
                "arm": arm, "name": ARM_NAMES[arm], "n_rows": 72,
                "n_finite_err": int(sum(np.isfinite(e) for e in errs)),
                "mean_err": float(np.mean(errs)),
                "worst_err": float(max(errs)),
                "err_bar": float(ERR_BAR),
                "n_rows_over_bar": int(sum(e >= ERR_BAR for e in errs)),
                "n_verified": int(sum(bool(r["verified"]) for r in rows)),
                "n_a3_ok": int(sum(r["a3_ok"] for r in rows)),
                "n_trace_len_ok": int(sum(r["trace_len_ok"]
                                          for r in rows)),
                "n_commits_count_ok": int(sum(r["commits_count_ok"]
                                              for r in rows)),
                "n_commits_unique_ok": int(sum(r["commits_unique_ok"]
                                               for r in rows)),
                "n_coverage_ok": int(sum(r["coverage_ok"] for r in rows)),
                "n_commits_finite_ok": int(sum(r["commits_finite_ok"]
                                               for r in rows)),
                "n_census_ok": int(sum(r["census_ok"] for r in rows)),
                "n_floor_schedule_ok": int(sum(r["floor_schedule_ok"]
                                               for r in rows)),
                "n_commits": int(sum(r["n_commits"] for r in rows)),
                "src_census": {t: int(sum(r["src_census"][t]
                                          for r in rows))
                               for t in COMMIT_SOURCES},
                "n_distinct_trace_shas": len(set(r["trace_sha256"]
                                                 for r in rows)),
                "n_distinct_commit_shas": len(set(r["commit_seq_sha256"]
                                                  for r in rows)),
                "mean_walk_steps": float(np.mean(
                    [r["walk_steps"] for r in rows])),
                "mean_cvt_rms": float(np.mean(
                    [r["cvt_rms"] for r in rows])),
                "mean_sc_rms": float(np.mean([r["sc_rms"] for r in rows]))}

        # ---- THE PAIRED DELTAS (the pre-named read: delta =
        #      err_A0 - err_arm — the anchor-minus-arm form, the
        #      convention that makes the pre-registered numeric form
        #      RETRIEVAL-SIDE iff mean_delta(A2) < mean_delta(A1) - 0.05
        #      equivalent to its own parenthetical "the read-arm degrades
        #      MORE than the write-arm" (L268: RETRIEVAL-SIDE iff A2
        #      degrades more than A1); BOTH signed conventions recorded
        #      per row, disclosed) ---------------------------------------
        delta_rows = []
        per_host_acc = {h: {"A1": [], "A2": []} for h in hosts}
        for key in E["A0"]:
            h, s, rk = key
            e0 = float(E["A0"][key]["err"])
            e1 = float(E["A1"][key]["err"])
            e2 = float(E["A2"][key]["err"])
            d1 = float(e0 - e1)
            d2 = float(e0 - e2)
            assert np.isfinite(d1) and np.isfinite(d2), \
                f"{key}: non-finite paired delta"
            delta_rows.append({
                "host": h, "seed": int(s), "row_key": rk,
                "err_A0": e0, "err_A1": e1, "err_A2": e2,
                "delta_A1_anchor_minus_arm": d1,
                "delta_A2_anchor_minus_arm": d2,
                "delta_A1_arm_minus_anchor": float(e1 - e0),
                "delta_A2_arm_minus_anchor": float(e2 - e0)})
            per_host_acc[h]["A1"].append(d1)
            per_host_acc[h]["A2"].append(d2)
        assert len(delta_rows) == 72, "the paired delta table drifted"
        mean_d1 = float(np.mean([d["delta_A1_anchor_minus_arm"]
                                 for d in delta_rows]))
        mean_d2 = float(np.mean([d["delta_A2_anchor_minus_arm"]
                                 for d in delta_rows]))
        per_host = {h: {"mean_delta_A1": float(np.mean(v["A1"])),
                        "mean_delta_A2": float(np.mean(v["A2"]))}
                    for h, v in per_host_acc.items()}
        # ---- THE BRANCH (the pre-named numeric form, evaluated exactly
        #      once) ------------------------------------------------------
        if mean_d2 < mean_d1 - MARGIN:
            branch = "RETRIEVAL-SIDE"
        elif mean_d1 < mean_d2 - MARGIN:
            branch = "STORAGE-SIDE"
        else:
            branch = "SYMMETRIC-INERT"

        # ---- the audit-only faces --------------------------------------
        # (i) the A2-identity face: the settle/decode never read the
        #     floor, so the read-stress arm's walks/errs are expected
        #     bit-identical to the anchor — RECORDED, never gating
        n_a2_err_id = int(sum(E["A2"][k]["err"] == E["A0"][k]["err"]
                              for k in E["A0"]))
        n_a2_sha_id = int(sum(E["A2"][k]["trace_sha256"]
                              == E["A0"][k]["trace_sha256"]
                              for k in E["A0"]))
        n_a2_cmt_id = int(sum(E["A2"][k]["commit_seq_sha256"]
                              == E["A0"][k]["commit_seq_sha256"]
                              for k in E["A0"]))
        # (ii) the trace-sha families per arm (the walks differ across
        #     the arms by construction — the anchor is the A0 arm only)
        n_a1_sha_neq = int(sum(E["A1"][k]["trace_sha256"]
                               != E["A0"][k]["trace_sha256"]
                               for k in E["A0"]))
        # (iii) the A0 commit-layer digest cross-checks vs exp287/exp288
        n_a0_287 = int(sum(bool(r.get("commit_sha_287_ok"))
                           for r in rows_by_arm["A0"]))
        n_a0_288 = int(sum(bool(r.get("commit_sha_288_ok"))
                           for r in rows_by_arm["A0"]))
        n_a0_cvt287 = int(sum(bool(r.get("cvt_287_ok"))
                              for r in rows_by_arm["A0"]))

        # ---- the S0 + G1/G2/G3 tallies ----------------------------------
        a0_rows = rows_by_arm["A0"]
        counts = integrity["counts"]
        n_s0_err = int(sum(bool(r.get("s0_err_ok")) for r in a0_rows))
        n_s0_ver = int(sum(bool(r.get("s0_verified_ok")) for r in a0_rows))
        n_we282 = int(sum(bool(r.get("walk_end_282_ok")) for r in a0_rows))
        n_ts282 = int(sum(bool(r.get("trace_sha_282_ok")) for r in a0_rows))
        n_ee282 = int(sum(bool(r.get("err_exact_282_ok")) for r in a0_rows))
        n_enc_a0a2 = int(sum(rows_by_arm[a][i]["floor_rec"]["encode_start"]
                             == PROD_FLOOR
                             for a in ("A0", "A2") for i in range(72)))
        n_walk_a1 = int(sum(
            rows_by_arm["A1"][i]["floor_rec"]["walk_first_commit"]
            == READER_PIN_FLOOR
            and rows_by_arm["A1"][i]["floor_rec"]["walk_last_commit"]
            == READER_PIN_FLOOR for i in range(72)))
        n_a1_settle = int(sum(rows_by_arm["A1"][i]["floor_rec"]
                              ["settle_start"] == PROD_FLOOR
                              for i in range(72)))
        n_a2_settle = int(sum(rows_by_arm["A2"][i]["floor_rec"]
                              ["settle_start"] == READER_PIN_FLOOR
                              for i in range(72)))
        n_dec = int(sum(rows_by_arm[a][i]["floor_rec"]["decode_start"]
                        == PROD_FLOOR for a in ("A1", "A2")
                        for i in range(72)))

        g1 = dict(counts)
        g1.update({
            "n_s0_err_ok": n_s0_err, "n_s0_verified_ok": n_s0_ver,
            "n_walk_end282_ok": n_we282, "n_trace282_ok": n_ts282,
            "n_errexact282_ok": n_ee282,
            "n_floor_encode_a0a2_ok": n_enc_a0a2,
            "n_floor_walk_a1_ok": n_walk_a1,
            "n_a0_commit_sha_287_ok": n_a0_287,
            "n_a0_commit_sha_288_ok": n_a0_288,
            "n_a0_cvt_287_ok": n_a0_cvt287})
        g2 = {
            "n_rows": 216, "n_lock_reads": lock_total,
            "per_arm_finite_err": {a: tallies[a]["n_finite_err"]
                                   for a in ARMS},
            "per_arm_a3_ok": {a: tallies[a]["n_a3_ok"] for a in ARMS},
            "per_arm_trace_len_ok": {a: tallies[a]["n_trace_len_ok"]
                                     for a in ARMS},
            "per_arm_commits_count_ok": {
                a: tallies[a]["n_commits_count_ok"] for a in ARMS},
            "per_arm_commits_unique_ok": {
                a: tallies[a]["n_commits_unique_ok"] for a in ARMS},
            "per_arm_coverage_ok": {a: tallies[a]["n_coverage_ok"]
                                    for a in ARMS},
            "per_arm_commits_finite_ok": {
                a: tallies[a]["n_commits_finite_ok"] for a in ARMS},
            "per_arm_census_ok": {a: tallies[a]["n_census_ok"]
                                  for a in ARMS},
            "n_floor_a1_settle_ok": n_a1_settle,
            "n_floor_a2_settle_ok": n_a2_settle,
            "n_floor_decode_ok": n_dec}
        g3 = {"branch": branch, "margin": MARGIN,
              "mean_delta_A1": mean_d1, "mean_delta_A2": mean_d2,
              "delta_convention": "err_A0 - err_arm (anchor minus arm)",
              "n_paired_rows": len(delta_rows),
              "all_deltas_finite": bool(all(
                  np.isfinite(d["delta_A1_anchor_minus_arm"])
                  and np.isfinite(d["delta_A2_anchor_minus_arm"])
                  for d in delta_rows))}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": integrity,
                "rows": [r for a in ARMS for r in rows_by_arm[a]],
                "per_arm": tallies,
                "paired_deltas": {
                    "convention": (
                        "delta = err_A0 - err_arm (the anchor-minus-arm "
                        "form; the arm-minus-anchor negatives are "
                        "recorded per row alongside — the pre-registered "
                        "numeric form RETRIEVAL-SIDE iff mean_delta(A2) < "
                        "mean_delta(A1) - 0.05 is the form that makes the "
                        "pre-registered parenthetical 'the read-arm "
                        "degrades MORE than the write-arm' true, per "
                        "L268's 'RETRIEVAL-SIDE iff A2 degrades more than "
                        "A1 by the 0.05 mV margin')"),
                    "rows": delta_rows, "per_host": per_host,
                    "outliers_H3_H5": {h: per_host[h]
                                       for h in outliers},
                    "mean_delta_A1": mean_d1, "mean_delta_A2": mean_d2},
                "a2_identity_audit": {
                    "gating": False,
                    "role": ("audit-only — the settle c.run(15.0) and the "
                             "decode pattern_error never read the floor, "
                             "so the A2 arm is expected bit-identical to "
                             "the A0 anchor; RECORDED, never gating"),
                    "n_err_identical": n_a2_err_id,
                    "n_trace_sha_identical": n_a2_sha_id,
                    "n_commit_sha_identical": n_a2_cmt_id},
                "trace_sha_families": {
                    "n_A1_trace_shas_differ_from_A0": n_a1_sha_neq,
                    "per_arm_distinct_trace_shas": {
                        a: tallies[a]["n_distinct_trace_shas"]
                        for a in ARMS}},
                "branch": branch,
                "branch_discriminant": {
                    "bar": MARGIN,
                    "bar_pre_named_at": ("982cb81 — fixed at "
                                         "pre-registration, never fit"),
                    "mean_delta_A1": mean_d1, "mean_delta_A2": mean_d2,
                    "form": ("RETRIEVAL-SIDE iff mean_delta(A2) < "
                             "mean_delta(A1) - 0.05; STORAGE-SIDE iff "
                             "mean_delta(A1) < mean_delta(A2) - 0.05; "
                             "else SYMMETRIC-INERT"),
                    "resolved": branch},
                "g1": g1, "g2": g2, "g3": g3,
                "ro_before": ro_before_pass}

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True, default=float).encode()
        ).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the default is
    #      the IN-PROCESS form (the 3 arms sequentially, 216 decodes
    #      ~3-4 min, under the 570 s cap); the pre-named alternative is
    #      the CHECKPOINT-SPLIT pass1|pass2 + merge — pass1 the A0+A1
    #      arms (144 decodes), pass2 the A2 arm (72), the merge
    #      bit-comparing the two passes' integrity sections and never
    #      re-decoding) ---------------------------------------------------
    _MODE = os.environ.get("EXP290_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp290_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp290_pass2.checkpoint.json")}
    PASS_ARMS = {1: ("A0", "A1"), 2: ("A2",)}

    if _MODE in ("pass1", "pass2"):
        tag = 1 if _MODE == "pass1" else 2
        payload = _compute_arms(PASS_ARMS[tag])
        ck = _CK[tag]
        assert not os.path.exists(ck), \
            (f"{ck} already holds a payload — the split form caches "
             "exactly one payload per pass")
        with open(ck, "w") as fh:
            json.dump(payload, fh, sort_keys=True, default=float)
        print(f"  checkpointed {_MODE} (sha {_payload_sha(payload)[:16]})")
        assert docstring_ok and header_ok, \
            "the self-check drifted after the work"
        set_floor(PROD_FLOOR)
        assert read_floor() == PROD_FLOOR, "floor drift at exit"
        return {"mode": _MODE,
                "payload_sha256": _payload_sha(payload)}

    if _MODE == "merge":
        cached = {}
        for tag in (1, 2):
            with open(_CK[tag]) as fh:
                cached[tag] = json.load(fh)
        ia = hashlib.sha256(json.dumps(
            cached[1]["integrity"], sort_keys=True,
            default=float).encode()).hexdigest()
        ib = hashlib.sha256(json.dumps(
            cached[2]["integrity"], sort_keys=True,
            default=float).encode()).hexdigest()
        assert ia == ib, \
            (f"the two passes' integrity sections diverged: {ia[:16]} vs "
             f"{ib[:16]} — the byte-identity check FAILED")
        assert cached[1]["ro_before"] == cached[2]["ro_before"] \
            == ro_before, "ro_before drifted across passes"
        rows_by_arm = {}
        for tag in (1, 2):
            for arm in PASS_ARMS[tag]:
                rows_by_arm[arm] = cached[tag]["rows_by_arm"][arm]
        lock_total = int(cached[1]["lock_reads"]) \
            + int(cached[2]["lock_reads"])
        canary_all = list(cached[1]["canary"]) + list(cached[2]["canary"])
        core = _assemble(rows_by_arm, cached[1]["integrity"], lock_total,
                         canary_all, ro_before)
        run_form = "checkpoint-split pass1|pass2 + merge"
        det = {"form": run_form,
               "pass_arms": {"pass1": list(PASS_ARMS[1]),
                             "pass2": list(PASS_ARMS[2])},
               "integrity_sha256_pass1": ia,
               "integrity_sha256_pass2": ib,
               "integrity_sections_bit_identical": True,
               "lock_reads": f"{int(cached[1]['lock_reads'])} + "
                             f"{int(cached[2]['lock_reads'])} == 216",
               "canary": canary_all,
               "canary_bit_identical": bool(
                   all(c["bit_identical"] for c in canary_all))}
    else:
        print("=== exp290: THE STRESS-TIMING SPLIT (write-time vs "
              "read-time depolarized stress on the commit machinery) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows x 3 arms = 216 decodes at "
              f"the production budget {BUDGET} (== exp142's "
              f"STEPS_PER_CELL)")
        print(f"  the arms: A0 the -60.0 anchor (the S0 bit-exact form) | "
              f"A1 the -35.0 pin during the walk only (the storage face) "
              f"| A2 the -35.0 pin during the settle only (the retrieval "
              f"face) | the branch bar: the 0.05 mV margin")

        payload = _compute_arms(ARMS)
        core = _assemble(payload["rows_by_arm"], payload["integrity"],
                         payload["lock_reads"], payload["canary"],
                         ro_before)
        run_form = "in-process three-arm sequential"
        det = {"form": run_form,
               "decodes_battery": 216,
               "canary_redecodes": len(payload["canary"]),
               "canary": payload["canary"],
               "canary_bit_identical": bool(
                   all(c["bit_identical"] for c in payload["canary"])),
               "payload_sha256": _payload_sha(payload)}

    # ---- the gate assembly (evaluated exactly once) ---------------------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    tallies = core["per_arm"]
    ro_unchanged = bool(
        set(_sha(p) for p in READ_DEPS) == set(ro_before.values())
        and set(core["ro_before"].values()) == set(ro_before.values()))
    g1_pass = bool(
        g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
        and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
        and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
        and g1["n_rows256"] == 72 and g1["n_structure_ok"] == 36
        and g1["n_worst_eq_max"] == 36
        and g1["n_deep_targets_ok"] == 72 and g1["n_medium_shas_ok"] == 72
        and g1["n_rows282"] == 72 and g1["n_282_chain_ok"] == 72
        and g1["n_rows287"] == 72 and g1["n_rows288"] == 72
        and g1["n_s0_err_ok"] == 72 and g1["n_s0_verified_ok"] == 72
        and g1["n_walk_end282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72
        and g1["n_floor_encode_a0a2_ok"] == 144
        and g1["n_floor_walk_a1_ok"] == 72
        and ro_unchanged)
    g2_pass = bool(
        g2["n_rows"] == 216 and g2["n_lock_reads"] == 216
        and all(g2["per_arm_finite_err"][a] == 72 for a in ARMS)
        and all(g2["per_arm_a3_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_trace_len_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_commits_count_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_commits_unique_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_coverage_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_commits_finite_ok"][a] == 72 for a in ARMS)
        and all(g2["per_arm_census_ok"][a] == 72 for a in ARMS)
        and g2["n_floor_a1_settle_ok"] == 72
        and g2["n_floor_a2_settle_ok"] == 72
        and g2["n_floor_decode_ok"] == 144)
    g3_pass = bool(
        g3["branch"] in ("RETRIEVAL-SIDE", "STORAGE-SIDE",
                         "SYMMETRIC-INERT")
        and g3["n_paired_rows"] == 72 and g3["all_deltas_finite"]
        and g3["margin"] == MARGIN)

    def _scan_wall_clock_keys(node, prefix=""):
        bad = []
        if isinstance(node, dict):
            for k, v in node.items():
                kk = f"{prefix}.{k}" if prefix else str(k)
                if any(t in str(k).lower() for t in
                       ("time", "clock", "stamp", "duration", "elapsed",
                        "runtime", "wall")):
                    bad.append(kk)
                bad.extend(_scan_wall_clock_keys(v, kk))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                bad.extend(_scan_wall_clock_keys(v, f"{prefix}[{i}]"))
        return bad

    branch = core["branch"]
    pd = core["paired_deltas"]
    bd = core["branch_discriminant"]
    a2id = core["a2_identity_audit"]

    if branch == "RETRIEVAL-SIDE":
        branch_text = (
            "the read-arm degrades MORE than the write-arm by the "
            "pre-named margin — Tazumi's retrieval-side direction holds "
            "at the machinery: the retrieval face is the sensitive one")
    elif branch == "STORAGE-SIDE":
        branch_text = (
            "the write-arm degrades MORE than the read-arm by the "
            "pre-named margin — the storage face (the walk's commits) "
            "is the sensitive one; Tazumi's retrieval-side direction is "
            "NOT borne out at the machinery")
    else:
        branch_text = (
            "the two faces indistinguishable at the machinery's "
            "resolution — the honest null")
    verdict_body = (
        f"{branch} — {branch_text} "
        f"(the paired deltas over the same 72 rows: mean_delta(A1) "
        f"{pd['mean_delta_A1']:+.4f} mV / mean_delta(A2) "
        f"{pd['mean_delta_A2']:+.4f} mV, delta = err_A0 - err_arm, vs "
        f"the pre-named 0.05 mV margin"
        f" | the per-arm faces: A0 mean err "
        f"{tallies['A0']['mean_err']:.4f} worst "
        f"{tallies['A0']['worst_err']:.4f}; A1 mean err "
        f"{tallies['A1']['mean_err']:.4f} worst "
        f"{tallies['A1']['worst_err']:.4f}; A2 mean err "
        f"{tallies['A2']['mean_err']:.4f} worst "
        f"{tallies['A2']['worst_err']:.4f}"
        f" | the worst-err vs the 6.0 bar: A0 "
        f"{tallies['A0']['n_rows_over_bar']}/72, A1 "
        f"{tallies['A1']['n_rows_over_bar']}/72, A2 "
        f"{tallies['A2']['n_rows_over_bar']}/72 over"
        f" | THE A2-IDENTITY FACE (audit-only): errs bit-identical to "
        f"the anchor {a2id['n_err_identical']}/72, trace shas "
        f"{a2id['n_trace_sha_identical']}/72, commit digests "
        f"{a2id['n_commit_sha_identical']}/72 — the settle+decode never "
        f"reads the floor"
        f" | the commit src census per arm (audit-only, the floor's "
        f"effect on the (e) branch): A0 spec "
        f"{tallies['A0']['src_census']['spec']} / canon "
        f"{tallies['A0']['src_census']['canon']} / parent "
        f"{tallies['A0']['src_census']['parent']}; A1 spec "
        f"{tallies['A1']['src_census']['spec']} / canon "
        f"{tallies['A1']['src_census']['canon']} / parent "
        f"{tallies['A1']['src_census']['parent']}; A2 spec "
        f"{tallies['A2']['src_census']['spec']} / canon "
        f"{tallies['A2']['src_census']['canon']} / parent "
        f"{tallies['A2']['src_census']['parent']}"
        f" | the trace shas per arm (audit-only): A1 differs from A0 on "
        f"{core['trace_sha_families']['n_A1_trace_shas_differ_from_A0']}"
        f"/72 rows — the walks differ across the arms by construction, "
        f"the anchor is the A0 arm only"
        f" | THE S0 ANCHOR: the A0 errs reproduce exp256's deposited "
        f"substituted errs bit-exact ({g1['n_s0_err_ok']}/72, the "
        f"verified flags {g1['n_s0_verified_ok']}/72) AND exp282's "
        f"walk_end_rms bit-exact (walk_end {g1['n_walk_end282_ok']}/72, "
        f"trace sha256 {g1['n_trace282_ok']}/72 — the SAME walk exp282 "
        f"deposited, err_exact {g1['n_errexact282_ok']}/72); the "
        f"commit-layer digests vs exp287/exp288 (audit-only): "
        f"{g1['n_a0_commit_sha_287_ok']}/72 + "
        f"{g1['n_a0_commit_sha_288_ok']}/72"
        f" | 12 hosts, the deterministic sha-asserted rebuild (graph_path "
        f"for H0/H1, small_world at the deposited rewire seeds — "
        f"exp269's/exp280's form), 7 deposits READ-ONLY byte-unchanged "
        f"({run_form}), floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp290_stress_timing",
        "claim": (
            "THE STRESS-TIMING SPLIT (batch 47, pre-registration commit "
            "982cb81): write-time vs read-time ionic stress on the "
            "commit machinery. Tazumi 2026 (APA): salt exposure "
            "disrupts memory RETRIEVAL in D. japonica while leaving "
            "storage intact — the timing split. The stack analog runs "
            "as-is on the commit-noise machinery: the ionic exposure IS "
            "the depolarized floor (exp169's disclosed -35.0 pin form), "
            "and the machinery has a clean write/read boundary — the "
            "WALK (the commits) is the storage face, the SETTLE+DECODE "
            "is the retrieval face. The 72-row substituted battery "
            "(exp256's, 12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, "
            "the exp287/exp288 traced replica form at the production "
            "budget 8) runs under three floor states: A0 the -60.0 "
            "anchor (the S0 bit-exact form), A1 the -35.0 pin during "
            "the walk only (from the encode window's start through the "
            "last commit), A2 the -35.0 pin during the settle only. "
            "Branch (the pre-named 0.05 mV margin form): RETRIEVAL-SIDE "
            "iff mean_delta(A2) < mean_delta(A1) - 0.05 (the read-arm "
            "degrades more — Tazumi's direction) / STORAGE-SIDE iff "
            "mean_delta(A1) < mean_delta(A2) - 0.05 / else "
            "SYMMETRIC-INERT"),
        "method": {
            "replica": (
                "exp288's landed body's traced replica REUSED VERBATIM "
                "(_execute_signed_traced with the disclosed recording "
                "additions (a)-(f), exp287's commit recording included) "
                "at the production budget 8 == exp142's STEPS_PER_CELL, "
                "plus exactly the pre-named arm schedule; the pin form "
                "is exp169's disclosed module-attribute pin (PINNED = "
                "core + exp142 + exp145 + exp148 + exp94; the attribute "
                "read AT STEP TIME by the walk's commit branch (e)); "
                "exp142 and the core NOT modified; the floor reads are "
                "pure recording (no RNG, no state) and the A0 arm never "
                "pins (the S0 bit-exactness proves it)"),
            "arms": {a: ARM_NAMES[a] for a in ARMS},
            "floor_schedule": FLOOR_SCHEDULE,
            "read": (
                "per arm the 72-row errs (the machinery's native 2-dp "
                "convention) + err_exact; the mean paired delta vs the "
                "A0 anchor over the same 72 rows; delta = err_A0 - "
                "err_arm (the anchor-minus-arm form — the convention "
                "that makes the pre-registered numeric form equivalent "
                "to its own parenthetical and to L268's 'RETRIEVAL-SIDE "
                "iff A2 degrades more than A1'; both signed conventions "
                "recorded per row, disclosed)"),
            "branch_rule": (
                "RETRIEVAL-SIDE iff mean_delta(A2) < mean_delta(A1) - "
                "0.05; STORAGE-SIDE iff mean_delta(A1) < mean_delta(A2) "
                "- 0.05; else SYMMETRIC-INERT. The bar 0.05 mV, fixed "
                "at pre-registration (982cb81), never fit"),
            "scope": (
                "the full traces and commit sequences NOT re-deposited "
                "— bit-reproduced via the per-row trace/commit digests "
                "+ G1's anchors (the exp284/exp285/exp286/exp287/"
                "exp288 precedent); no wall-clock fields; the "
                "deterministic canary form")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": core["ro_before"][name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base)",
                "the 72 rows — the S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas",
                "the host frame + the per-host boundary counts",
                "the outlier pre-name (H3/H5 — the audit-only per-host "
                "delta carry)",
                "the S0 walk anchor — the 72 per-row walk_end_rms + "
                "trace shas + the deposited TRAJECTORY-CARRIED branch",
                "the commit-layer anchor deposit — the 72 per-row "
                "commit digests (audit-only cross-check for the A0 arm)",
                "the battery's immediate predecessor — the 72 per-row "
                "commit digests (audit-only cross-check for the A0 "
                "arm) + the traced replica form's provenance"))},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp256_reread": integrity["exp256_reread"],
        "exp282_reread": integrity["exp282_reread"],
        "exp287_reread": integrity["exp287_reread"],
        "exp288_reread": integrity["exp288_reread"],
        "rows": core["rows"],
        "per_arm": tallies,
        "paired_deltas": pd,
        "a2_identity_audit": a2id,
        "trace_sha_families": core["trace_sha_families"],
        "branch": branch,
        "branch_discriminant": bd,
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": det,
        "discipline": {}}

    no_wall_clock = True
    _bad_keys = _scan_wall_clock_keys(deposit)
    if _bad_keys:
        no_wall_clock = False
    assert not _bad_keys, f"wall-clock key detected: {_bad_keys}"
    _blob = json.dumps(deposit, default=float)
    assert not any(pat in _blob for pat in ('"runtime', '"wall_clock',
                                            '"wall_s', '"timestamp',
                                            '"generated_at')), \
        "wall-clock field detected in the deposit"
    gates = {
        "G1_anchor_floor_deposits": {
            "pass": g1_pass,
            "counts": g1,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "s0_anchor": (
                "the A0 arm's errs reproduce exp256's deposited "
                "substituted errs bit-exact (72/72, the machinery's "
                "native 2-dp convention) with the verified flags 72/72, "
                "AND exp282's walk_end_rms reproduces bit-exact "
                "(walk_end_rms + trace sha256 72/72 — the SAME walk "
                "exp282 deposited, plus err_exact 72/72); the floor "
                "asserts: the floor reads -60.0 at the encode start per "
                "row in A0/A2 (144/144) and -35.0 during the walk in A1 "
                "(72/72 first+last commit) — recorded per row, asserted "
                "fail=STOP; the commit-layer digests vs exp287/exp288 "
                "recorded audit-only")},
        "G2_arms_integrity": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "per arm (72 rows each): the errs finite; the A3 "
                "convention round(err_exact, 2) == the reported err; "
                "the trace lengths == walk_steps; the commit counts == "
                "walk_steps; the commit indices unique; the write-set "
                "coverage; the values finite; the source census sane; "
                "the S* lock reads 216 (3 arms x 72 — the canary "
                "re-reads truncated, disclosed); the pin restore "
                "asserted at the settle boundary per row (the floor "
                "reads -60.0 at the settle start in A1 72/72, -35.0 in "
                "A2 72/72, -60.0 at the decode in both 144/144) — "
                "recorded, fail=STOP")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bars": ("the paired deltas over the same 72 rows per arm; "
                     "RETRIEVAL-SIDE iff mean_delta(A2) < mean_delta(A1) "
                     "- 0.05; STORAGE-SIDE iff mean_delta(A1) < "
                     "mean_delta(A2) - 0.05; else SYMMETRIC-INERT. "
                     "Audit-only, never gating: the per-row paired "
                     "delta table (both signed conventions), the "
                     "per-host mean deltas, the outliers H3/H5's "
                     "deltas, the worst-err per arm vs the 6.0 bar, "
                     "the commit censuses per arm, the trace shas per "
                     "arm, the A2-identity face"),
            "resolved": {"branch": branch,
                         "mean_delta_A1": pd["mean_delta_A1"],
                         "mean_delta_A2": pd["mean_delta_A2"],
                         "per_host_mean_deltas": pd["per_host"],
                         "outliers_H3_H5": pd["outliers_H3_H5"]}},
        "G4_discipline": {
            "pass": None}}   # filled after the floor-exit assert
    n_pass = 0
    n_refute = 0
    for name in ("G1_anchor_floor_deposits", "G2_arms_integrity",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    # ---- the floor restore + the exit asserts (G4: NEURAL_SPEC_MIN ==
    #      -60.0 asserted at exit; the docstring + header re-checked) ----
    set_floor(PROD_FLOOR)
    floor_exit = read_floor()
    assert floor_exit == PROD_FLOOR, "floor drift at exit"
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    assert set(_sha(p) for p in READ_DEPS) \
        == set(ro_before.values()), "source deposit drifted after work"
    gates["G4_discipline"] = {
        "pass": bool(det.get("canary_bit_identical", False)
                     and no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged and floor_exit == PROD_FLOOR),
        "determinism_canary_bit_identical": det.get(
            "canary_bit_identical", False),
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_982cb81": docstring_ok,
        "header_byte_unchanged_vs_982cb81": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "floor_at_entry": floor_at_entry,
        "floor_at_exit": floor_exit,
        "floor_at_exit_per_module": {
            m.__name__: float(getattr(m, "NEURAL_SPEC_MIN", None))
            for m in PINNED},
        "reader_pin_floor_disclosed": READER_PIN_FLOOR,
        "docstring_sha256": docstring_sha,
        "header_sha256": header_sha,
        "deposit_form": ("deterministic: no wall-clock fields — a re-run "
                         "of this module in the same form reproduces this "
                         "file byte-identically")}
    n_pass += int(gates["G4_discipline"]["pass"])
    n_refute += int(not gates["G4_discipline"]["pass"])
    deposit["gates"] = gates
    verdict = (f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} "
               f"REFUTE) | " + verdict_body)
    deposit["verdict"] = verdict

    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=float).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  G1 the anchor + the floor asserts + the deposits: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the 12 bases rebuilt sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the canon "
          f"identity {g1['n_canon_ok']}/12 + H0 == H1 + f_max "
          f"{g1['n_fmax_ok']}/12; the deep targets "
          f"{g1['n_deep_targets_ok']}/72 + the medium shas "
          f"{g1['n_medium_shas_ok']}/72; THE S0 ANCHOR — the errs == "
          f"exp256's deposited errs bit-exact {g1['n_s0_err_ok']}/72, the "
          f"verified flags {g1['n_s0_verified_ok']}/72, exp282's "
          f"walk_end_rms {g1['n_walk_end282_ok']}/72 + trace sha "
          f"{g1['n_trace282_ok']}/72 + err_exact "
          f"{g1['n_errexact282_ok']}/72; the floor: A0/A2 encode -60.0 "
          f"{g1['n_floor_encode_a0a2_ok']}/144, A1 walk -35.0 "
          f"{g1['n_floor_walk_a1_ok']}/72; 7 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged})")
    print(f"  G2 the arms' integrity: {'PASS' if g2_pass else 'FAIL'} "
          f"(per arm: finite errs "
          f"{[g2['per_arm_finite_err'][a] for a in ARMS]}/72, A3 "
          f"{[g2['per_arm_a3_ok'][a] for a in ARMS]}/72, trace lengths "
          f"{[g2['per_arm_trace_len_ok'][a] for a in ARMS]}/72, commit "
          f"counts {[g2['per_arm_commits_count_ok'][a] for a in ARMS]}/72; "
          f"the S* lock reads {g2['n_lock_reads']}/216; the settle "
          f"boundary: A1 -60.0 {g2['n_floor_a1_settle_ok']}/72, A2 -35.0 "
          f"{g2['n_floor_a2_settle_ok']}/72, the decode -60.0 "
          f"{g2['n_floor_decode_ok']}/144)")
    print("  G3 the paired deltas (delta = err_A0 - err_arm; the "
          "pre-named 0.05 mV margin):")
    print(f"      mean_delta(A1) {pd['mean_delta_A1']:+.4f} mV | "
          f"mean_delta(A2) {pd['mean_delta_A2']:+.4f} mV")
    for h in hosts:
        ph = pd["per_host"][h]
        tag = " <== outlier" if h in outliers else ""
        print(f"      {h:4s} dA1 {ph['mean_delta_A1']:+.4f} "
              f"dA2 {ph['mean_delta_A2']:+.4f}{tag}")
    print(f"      A2-identity (audit-only): errs "
          f"{a2id['n_err_identical']}/72, trace shas "
          f"{a2id['n_trace_sha_identical']}/72 — the settle+decode "
          f"never reads the floor")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(the determinism canary: "
          f"{gates['G4_discipline']['determinism_canary_bit_identical']}, "
          f"form {run_form}; no wall-clock fields: {no_wall_clock}; "
          f"docstring+header pinned to 982cb81; floor at exit "
          f"{gates['G4_discipline']['floor_at_exit']})")
    print(f"\n  BRANCH: {branch} | mean_delta(A1) "
          f"{pd['mean_delta_A1']:+.4f} | mean_delta(A2) "
          f"{pd['mean_delta_A2']:+.4f} | the margin {MARGIN}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    return deposit

if __name__ == "__main__":
    main()
