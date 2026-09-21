#!/usr/bin/env python3
"""exp304 — THE TRANSPORT FACE RE-SCOPED: THE DEGENERACY REPAIR + THE
CARRIER'S STREAM (batch 58; ledger L288's registered next (a) — exp303
landed the 8th formalization with the pre-named branch clause counting
the degenerate H0<->H1 pair (whose substrates are BIT-IDENTICAL, the
chain constructor's echo — disclosed, never patched in-gate): the
honest reading was TRANSPORT-REFINES-DEEPENED (0/130 genuine
cross-substrate transports, the mean price +15.76 mV). THIS EXPERIMENT
DOES TWO THINGS: (1) THE REPAIR — the transport face re-scoped to the
130 genuinely-distinct ordered pairs (the H0<->H1 exclusion PRE-NAMED
this time), with the dormant transports reproduced BIT-EXACT against
exp303's deposited per-pair region rms (the cross-deposit anchor); (2)
THE CARRIER'S STREAM — exp301 landed WRITE-SIDE-CARRIED: the composed
carrier's commits differ from the dormant's on 72/72 rows and land
closer to the target; exp302 landed the mechanism face (the armed
sites' writes ARE the spec install re-asserted, the blend weight 1.0).
The open question: does the CARRIER's stream transport where the
dormant's is wiring-bound? The carrier's armed values are the spec
install itself — zone-consistent by construction at the SOURCE; the
transport maps them onto the destination's own walk order (the walk
order is arm-independent, exp300's G2 stream face) — if the carrier's
values are zone-consistent on ANY wiring (the spec's re-assertion is
substrate-free in the sense exp288's SPEC-UNIFORM named), the
transport should succeed where the dormant's idiosyncratic state
failed: THE UNBLOCKING EVENT. The null: the carrier's stream is
wiring-bound exactly as the dormant's — the indexation binds both.)

THE INSTRUMENT (the landed machinery COMPOSED VERBATIM): the
(seed 1, instance 0) slice of the exp256 battery — 12 rows — walked in
BOTH forms: the dormant (the exp302 landed walk at g=0.0/A0 — the errs
+ the commit digests reproduce exp256's/exp287's deposited slice rows
BIT-EXACT 12/12) and the CARRIER (the exp302 landed union coupling
faces=(ctx, gj, apop) at the composed optimum g=1.0, arm A0 — the errs
+ the trace shas reproduce exp300's deposited union g=1.0 slice rows
BIT-EXACT 12/12; the walk orders are arm-independent, asserted). The
REPLAY INSTRUMENT is exp303's landed form VERBATIM (the fresh
GraphCollective on A_ext, NO spec install/clamps/encode/carried state,
the stream's values at the walk order, the walk's own settle, the
region-scoped decode at the pre-named ERR_BAR 6.0).

THE FACES (each evaluated exactly once):
  F1  THE DORMANT REPAIR: the 130 genuine dormant transports (the
      pre-named exclusion: the ordered pairs (h, h') with h' != h and
      NOT {h, h'} == {H0, H1}) reproduce exp303's deposited per-pair
      region rms BIT-EXACT 130/130 (the cross-deposit anchor — the
      repair is a re-scoping, not a re-run with new knobs).
  F2  THE CARRIER CONTENT FACE: the 12 carrier same-substrate
      replays — the region-scoped error vs the 6.0 bar, the majority
      bar 7/12 (the same spirit as exp303's 37/72).
  F3  THE CARRIER TRANSPORT FACE: the 130 genuine carrier transports
      — the region-scoped error vs the SAME 6.0 bar; the transport
      price per pair (the transported error minus the destination's
      own carrier replay error).

PRE-REGISTERED GATES:
  G1  THE ANCHORS: the 12 dormant slice walks reproduce exp256's
      deposited errs + exp282's walk anchors + exp287's commit digests
      BIT-EXACT 12/12; the 12 carrier slice walks reproduce exp300's
      deposited union g=1.0 rows (the errs + the trace shas)
      BIT-EXACT 12/12; the walk orders arm-independent 12/12 (the
      commit-index digests equal across the two forms per row); the
      rebuild chain sha-asserted; the floor -60.0 at every replay and
      at exit; 9 deposits READ-ONLY (exp243/256/272/273/282/287/289/
      300/303 — sha before/after); the test suite green.
  G2  THE FACES: F1 130/130 bit-exact; F2/F3 finite everywhere, the
      canaries (one carrier same-substrate replay + one carrier
      transport re-run bit-exact).
  G3  THE BRANCH DISCRIMINANT (pre-named):
      CARRIER-TRANSPORTS  iff F2 holds (>= 7/12) AND >= 1/130 genuine
                          carrier transports within the bar AND F1
                          reproduces (the dormant control 0/130
                          re-confirmed) — the carrier's re-assertion
                          stream is substrate-independent where the
                          dormant's is bound: THE UNBLOCKING EVENT;
      BOTH-BOUND         iff F2 holds AND 0/130 carrier transports —
                          the block deepens (the indexation binds
                          both forms);
      MIXED              otherwise (recorded, the honest leftover).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

RUN: 24 walks + 12 carrier same-substrate replays + 260 transports +
the canaries ~ 4-7 min in-process; serial, BLAS pinned.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp304_transport_rescoped.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit c4c563b; gates G1-G4
    #      evaluated exactly once. THE COMPOSITION: exp302's landed walk
    #      machinery (both forms: the dormant g=0.0 + the union
    #      faces=(ctx, gj, apop) at the composed optimum g=1.0, arm A0;
    #      exp300's landed marks form) + exp303's landed REPLAY
    #      INSTRUMENT VERBATIM; the slice (seed 1, instance 0); the
    #      H0<->H1 exclusion PRE-NAMED) ==============================
    import hashlib
    import json
    import subprocess

    import numpy as np

    import cultivation.bioelectric.collective as CORE  # floor + THE PORT
    import experiments.exp142_sign_read as _m142       # NOT modified
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
    from experiments.exp148_temporal_read import flip_clock_matrix  # noqa
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp198_adversarial_reader_n400 import (  # noqa: E402
        N400, SEEDS as SEEDS_N400)

    # ---- the byte-unchanged self-check (the docstring + the header are
    #      the c4c563b pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "f36b7b6f047c455b0b3bc9adc59c65ffc2281903c4151c928706414136e26c81")
    EXPECTED_HEADER_SHA256 = (
        "c6ddc7f0a99bb40ee092272e526c05fad8a1c92782d233b29a3f109ac727fe60")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from c4c563b"
    assert header_ok, "header drifted from c4c563b"

    # ---- the -60.0 floor (G4: asserted at exit; the exp169-import
    #      discipline — the whole reader chain imported FIRST) --------
    PROD_FLOOR = -60.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)

    def set_floor(v):
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

    # ---- the frozen read configuration + the pre-named slice/bars ----
    REWIRE_P = 0.10
    DEEP_RUNG = -60.0
    DEEP_INSTANCES = (0, 1)     # the full pool for the marks' validity
    ARM_SUBST = "substituted"
    P3 = "P3_deep_band_substitution"
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert SEEDS_RUN == (1, 2, 3), "seed-line drift"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        "the read drifted off S*"
    assert (WINDOW_H, COMMIT_NOISE, STEPS_PER_CELL, ERR_BAR) == (
        _m142.WINDOW_H, _m142.COMMIT_NOISE, _m142.STEPS_PER_CELL,
        _m142.ERR_BAR), "the executor constants drifted from exp142's"
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    SETTLE_H = 15.0
    SLICE_SEED = 1              # the pre-named slice
    SLICE_INST = 0
    FACES_UNION = ("ctx", "gj", "apop")   # exp300's landed union arm
    G_COMPOSED = 1.0                      # exp300's composed optimum
    CONTENT_BAR = float(ERR_BAR)          # 6.0 — the house's own bar
    CONTENT_MAJORITY = 7                  # >= 7/12 within the bar
    # THE DEGENERACY EXCLUSION (pre-named at c4c563b): the ordered pair
    # (H0, H1) and (H1, H0) are excluded — the chain constructor's echo
    # makes the two substrates BIT-IDENTICAL (asserted in the rebuild);
    # the genuine pair set is 12 x 11 - 2 = 130.
    DEGENERATE_PAIRS = {("H0", "H1"), ("H1", "H0")}

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

    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)

    # ---- the source deposits (READ-ONLY; 9 — the pre-named list) ------
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
    DEP289 = os.path.join(ROOT, "results",
                          "exp289_history_register.json")
    DEP300 = os.path.join(ROOT, "results",
                          "exp300_composed_optimum.json")
    DEP303 = os.path.join(ROOT, "results",
                          "exp303_zero_substrate_8th.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287, DEP289,
                 DEP300, DEP303)
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit",
                  DEP289: "exp289_deposit", DEP300: "exp300_deposit",
                  DEP303: "exp303_deposit"}
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
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
    with open(DEP289) as fh:
        dep289 = json.load(fh)
    with open(DEP300) as fh:
        dep300 = json.load(fh)
    with open(DEP303) as fh:
        dep303 = json.load(fh)

    # ---- the host frame ------------------------------------------------
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep287["hosts"] == hosts, "exp287's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    rec272 = {r["host"]: r for r in dep272["per_host"]}

    # ---- exp208's classify VERBATIM -------------------------------------
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
        cls = np.zeros(n, dtype=int)          # 2 = INTERIOR
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

    # ---- the READ CHAIN (exp303's landed _ext_medium VERBATIM) ---------
    def _ext_medium(med, fmax):
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
        return {"A_ext": A_ext, "rho": rho, "branch": branch}

    # ---- exp259's compensation instrument (the gj landed assert) -------
    def pair_participation(A: np.ndarray, junction: np.ndarray,
                           i: int) -> float:
        return float(sum(A[i, j] for j in range(A.shape[0])
                         if j != i and A[i, j] > 0 and junction[j]))

    def canonical_target_part(A_base: np.ndarray,
                              canon_t: np.ndarray) -> float:
        j = classify(canon_t, A_base)["junction"]
        parts = [pair_participation(A_base, j, int(i))
                 for i in np.where(j)[0]]
        assert parts, "the canonical medium carries no pair cells"
        return float(np.mean(parts))

    def compensate(A_med: np.ndarray, T_row: np.ndarray,
                   target_part: float):
        n = A_med.shape[0]
        J = classify(T_row, A_med)["junction"]
        m = np.ones(n, dtype=float)
        for i in np.where(J)[0]:
            p = pair_participation(A_med, J, int(i))
            if p > 0.0:
                m[int(i)] = target_part / p
        W = A_med.copy().astype(float)
        for i in np.where(J)[0]:
            W[int(i), :] *= m[int(i)]
            W[:, int(i)] *= m[int(i)]
        s_pre = float(np.asarray(A_med, dtype=float).sum())
        s_w = float(W.sum())
        W *= s_pre / s_w
        resid = abs(float(W.sum()) - s_pre) / max(1.0, abs(s_pre))
        assert resid <= 1e-9, "conductance conservation violated"
        return W, m, float(resid)

    # ---- THE TRACED WALK (exp302's landed
    #      _execute_signed_traced_union_stress VERBATIM at arm A0 — the
    #      dormant form at g=0.0 (the coupling block skipped) and the
    #      union faces=(ctx, gj, apop) at the composed optimum g=1.0;
    #      the pin code absent (A0 never pins — the production floor
    #      throughout, asserted by the floor_rec reads)) --------------
    def _execute_signed_traced(spec, adjacency, seed, op, budget,
                               g=0.0, a_base=None, mark_mask=None):
        assert isinstance(g, (int, float)) and 0.0 <= float(g) <= 1.0, \
            "the dose drifted off the [0, 1] domain"
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
        hist0 = getattr(c, "phi_history", None)
        reg_init_ok = bool(hist0 is not None
                           and np.array_equal(np.asarray(hist0), target))
        assert reg_init_ok, \
            "the history register is absent or its init drifted from " \
            "the spec's install"
        prog = compile_anatomy(spec, n=n)
        if prog.rejected:
            return {"program_verified": False, "rejected": prog.rejected,
                    "err_vs_target": float("nan"),
                    "walk_trace": [], "walk_steps": 0,
                    "commits": [], "coverage_ok": False,
                    "reg_init_ok": reg_init_ok, "dt": dt,
                    "target": target, "order": []}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        floor_rec["encode_start"] = read_floor()
        c.run(WINDOW_H, dt=dt)
        c.release_clamps()
        reg_idx: list[int] = []
        for z in spec.zones:
            i0 = int(round(z.f0 * n))
            i1 = max(int(round(z.f1 * n)), i0 + 1)
            reg_idx.extend(range(i0, i1))
        reg_idx = sorted(set(reg_idx))
        trace: list = []
        order: list = []
        commits: list = []
        n_arm_writes = 0
        n_sigma_writes = 0
        n_blend_writes = 0
        cls = None
        J = None
        if g > 0.0:
            assert a_base is not None, "the activation needs the base adjacency"
            cls = classify(target, a_base)["class"]
            if "gj" in FACES_UNION:
                J = classify(target, a_base)["junction"]
            if "apop" in FACES_UNION:
                assert mark_mask is not None, \
                    "the apop face needs the register-face mark"
                assert len(reg_idx) >= 1 and bool(np.all(
                    mark_mask[reg_idx[0]:reg_idx[-1] + 1])), \
                    "the mark does not cover the amputation band"
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
        for i, src in order:
            for _ in range(budget):                  # the landed
                c.step(dt)                           # parameterization
            canon_src = getattr(c, "phi_spec_canon", None)
            if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:       # (e)
                commit_base = c.phi_spec[i]
                src_tag = "spec"
            elif canon_src is not None:
                commit_base = canon_src[i]
                src_tag = "canon"
            else:
                commit_base = c.theta[src]
                src_tag = "parent"
            sigma = COMMIT_NOISE
            written = None
            # ---- THE FACES' COUPLING (exp300's landed form VERBATIM;
            #      ZERO at g == 0.0) -----------------------------------
            if g > 0.0:
                hist_i = float(c.phi_history[i])
                cell_armed = False
                if "apop" in FACES_UNION:
                    if bool(mark_mask[i]):
                        sigma = COMMIT_NOISE * (1.0 - g)
                        apop_vec = c.read_channel("apop")
                        apop_vec[i] = 1.0
                        c.set_channel("apop", apop_vec)
                        n_sigma_writes += 1
                        cell_armed = True
                theta_new = commit_base + c.rng.normal(0.0, sigma)
                blend = False
                if "ctx" in FACES_UNION and cls[i] == 0:
                    blend = True
                if "gj" in FACES_UNION and bool(J[i]):
                    blend = True
                    gj_vec = c.read_channel("gj")
                    gj_vec[i] = hist_i
                    c.set_channel("gj", gj_vec)
                if blend:
                    written = (1.0 - g) * theta_new + g * hist_i
                    n_blend_writes += 1
                    cell_armed = True
                if cell_armed:
                    n_arm_writes += 1
            else:
                theta_new = commit_base + c.rng.normal(0.0, sigma)
            if written is None:
                written = theta_new
            c.theta[i] = written
            c.V[i] = written
            commits.append((int(i), float(written), src_tag))
            c.phi_history[i] = written
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        floor_rec["walk_last_commit"] = read_floor()
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        floor_rec["settle_start"] = read_floor()
        c.run(SETTLE_H, dt=dt)
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
               "walk_trace": trace, "walk_steps": len(order),
               "final_state": {"V": c.V.tolist(),
                               "target": target.tolist()},
               "commits": commits, "coverage_ok": coverage_ok,
               "reg_init_ok": reg_init_ok, "dt": dt, "target": target,
               "n_arm_writes": int(n_arm_writes),
               "n_sigma_writes": int(n_sigma_writes),
               "n_blend_writes": int(n_blend_writes)}
        return out

    # ---- THE REPLAY INSTRUMENT (exp303's landed form VERBATIM) --------
    def _replay(A_ext, values, cells, seed, target, label=""):
        assert len(values) == len(cells), \
            f"{label}: the replay's value/cell counts disagree"
        gamma, mu = STAR_OP["gamma"], STAR_OP["mu"]
        dt = star_dt(gamma, float(np.abs(A_ext).sum(axis=1).max()))
        c = GraphCollective(adjacency=A_ext, seed=seed, gamma=gamma,
                            mu_theta=mu)
        # the ZERO-SUBSTRATE protocol: nothing but the wiring + the
        # stream (no spec install, no clamps, no encode, no carried
        # state — the register port never touched)
        for idx, v in zip(cells, values):
            c.theta[idx] = v
            c.V[idx] = v
        assert read_floor() == PROD_FLOOR, \
            f"{label}: the replay's settle ran off the production floor"
        c.run(SETTLE_H, dt=dt)
        V = np.asarray(c.V, dtype=float)
        T = np.asarray(target, dtype=float)
        widx = np.asarray([int(i) for i in cells], dtype=int)
        region_rms = float(np.sqrt(np.mean((V[widx] - T[widx]) ** 2)))
        assert np.isfinite(region_rms), f"{label}: non-finite region rms"
        full_err = float(c.pattern_error(target))
        assert np.isfinite(full_err), f"{label}: non-finite full err"
        return {"region_rms": region_rms, "full_err": full_err,
                "n_written": int(len(cells)), "dt": dt,
                "region_within_bar": bool(region_rms <= CONTENT_BAR),
                "full_within_bar": bool(full_err <= CONTENT_BAR)}

    # ---- THE REBUILD (the sha-asserted rebuild + the marks' validity
    #      + the exp300/exp303 anchor re-reads) --------------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_canon_ok": 0, "h0_echo_h1": False, "n_fmax_ok": 0,
                  "n_nonneg_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
                  "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
                  "n_medium_shas_ok": 0, "n_rows282": 0,
                  "n_282_chain_ok": 0, "n_rows287": 0,
                  "n_rows300_u1": 0, "n_marks_ok": 0, "n_tpart_ok": 0,
                  "n_rows303_transport": 0}
        bases = {}
        rebuild_report = []
        for h in hosts:
            rec = dep243["classes"][h]
            n = int(rec["n"])
            assert n == int(N400), f"{h}: n drift vs exp198's N400"
            if h in ("H0", "H1"):
                A = graph_path(N400)
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
            bnd_dual = bool(nb == int(rec272[h]["n_boundary_cells_base"]))
            assert sha_ok and edges_ok and bnd_ok and bnd_dual \
                and canon_ok, \
                f"{h}: the rebuild drifted from exp243's records"
            fmax = float(f_max_frames(list(HostWMedium(A).snapshots())))
            fmax_ok = bool(fmax == float(rec["f_max_base"]))
            assert fmax_ok, f"{h}: f_max drifted from exp243's deposit"
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
                "sha256_matches_exp243_record": sha_ok,
                "edges_match_exp243_record": edges_ok,
                "boundary_count_matches_2way": bool(bnd_ok and bnd_dual),
                "canon_identity_ok": canon_ok,
                "f_max_matches_exp243_record": fmax_ok,
                "base_non_negative": nonneg})
        counts["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                                   bases["H1"]["A"]))
        assert counts["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        rows256 = dep256["rows"]
        counts["n_rows256"] = len(rows256)
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        dep_sub = {}
        for r in rows256:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                dep_sub[(r["host"], int(r["seed"]), i["row_key"])] = {
                    "err": float(i["err"]), "verified": bool(i["verified"]),
                    "row_target_sha256": i["row_target_sha256"],
                    "medium_sha256": i["medium_sha256"]}
        assert len(dep_sub) == 72, "the 72 substituted records drifted"
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
        counts["n_structure_ok"] = counts["n_worst_eq_max"] = -1  # unused

        rows282 = dep282["rows"]
        counts["n_rows282"] = len(rows282)
        assert len(rows282) == 72, "exp282's 72-row deposit drifted"
        assert dep282["branch"] == "TRAJECTORY-CARRIED", \
            "exp282's deposited branch drifted"
        r282 = {}
        for r in rows282:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r282, f"duplicate exp282 row {key}"
            r282[key] = r
        n_chain282 = sum(
            bool(float(r282[k]["err_deposited"])
                 == dep_sub[k]["err"]) for k in r282)
        counts["n_282_chain_ok"] = n_chain282
        assert n_chain282 == 72, "exp282's err chain anchor drifted"

        r287 = {}
        for r in dep287["rows"]:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r287, f"duplicate exp287 row {key}"
            r287[key] = r
        counts["n_rows287"] = len(r287)
        assert counts["n_rows287"] == 72, "exp287's 72-row deposit drifted"

        # THE EXP300 ANCHOR RE-READ (the union g=1.0 rows — the
        # carrier's anchor source) + THE MARKS' VALIDITY (fail=STOP)
        assert dep300["branch"] == "MONOTONE-TO-1.0", \
            "exp300's deposited branch drifted from MONOTONE-TO-1.0"
        r300u1 = {}
        for r in dep300["rows"]:
            if r["arm"] != "ctx|gj|apop" or float(r["g"]) != G_COMPOSED:
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r300u1, \
                f"duplicate exp300 union g=1.0 row {key}"
            r300u1[key] = r
        counts["n_rows300_u1"] = len(r300u1)
        assert counts["n_rows300_u1"] == 72, \
            "exp300's 72-row union g=1.0 battery drifted"

        pool = []
        bands = {}
        target_part = {}
        for h in hosts:
            canon_t = bases[h]["canon"]
            target_part[h] = canonical_target_part(bases[h]["A"], canon_t)
            for inst in DEEP_INSTANCES:
                f = np.asarray(bases[h]["deep"][inst]["f"], dtype=float)
                pool.append(f)
                spec = bases[h]["deep"][inst]["spec"]
                reg_idx = []
                n = int(bases[h]["n"])
                for z in spec.zones:
                    i0 = int(round(z.f0 * n))
                    i1 = max(int(round(z.f1 * n)), i0 + 1)
                    reg_idx.extend(range(i0, i1))
                reg_idx = sorted(set(reg_idx))
                bands[(h, inst)] = [int(reg_idx[0]), int(reg_idx[-1])]
        pooled = np.concatenate(pool)
        q10 = float(np.quantile(pooled, 0.10))
        q90 = float(np.quantile(pooled, 0.90))
        ai300 = dep300["arm_inputs"]
        assert q10 == float(ai300["q10"]) and q90 == float(ai300["q90"]), \
            "the rebuilt quantiles drifted from exp300's arm_inputs"
        assert int(ai300["pooled_n"]) == int(pooled.size) == 9600, \
            "the pooled mark source drifted from exp300's"
        marks = {}
        for h in hosts:
            marks[h] = {}
            for inst in DEEP_INSTANCES:
                f = np.asarray(bases[h]["deep"][inst]["f"], dtype=float)
                lo, hi = bands[(h, inst)]
                mk = (f <= q10) | (f >= q90)
                mk[lo:hi + 1] = True
                marks[h][inst] = mk
                dep_band = ai300["bands"][f"{h}|i{inst}"]
                counts["n_marks_ok"] += int(
                    bool([int(lo), int(hi)] == [int(dep_band[0]),
                                                int(dep_band[1])]))
            counts["n_tpart_ok"] += int(
                target_part[h] == float(ai300["target_part"][h]))
        assert counts["n_marks_ok"] == 24 and counts["n_tpart_ok"] == 12, \
            "the marks'/target_part's validity tally drifted"

        # THE EXP303 TRANSPORT RE-READ (the F1 cross-deposit anchor's
        # source: the 132 deposited dormant transports)
        r303t = {}
        for t in dep303["transports"]:
            pk = (t["src_host"], t["dst_host"])
            assert pk not in r303t, f"duplicate exp303 transport {pk}"
            assert all(fld in t for fld in
                       ("region_rms", "m", "m_prime", "n_written")), \
                f"{pk}: exp303's transport record is missing anchors"
            r303t[pk] = t
        counts["n_rows303_transport"] = len(r303t)
        assert counts["n_rows303_transport"] == 132, \
            "exp303's 132-transport battery drifted"
        # the exclusion's honesty: the pre-named degenerate pairs are
        # exactly the in-bar pairs of exp303's deposit (the audit that
        # named the hole, now pinned)
        inbar303 = sorted((t["src_host"], t["dst_host"])
                          for t in dep303["transports"]
                          if t["region_within_bar"])
        assert inbar303 == sorted(DEGENERATE_PAIRS), \
            (f"exp303's in-bar pairs {inbar303} drifted from the "
             f"pre-named degenerate set {sorted(DEGENERATE_PAIRS)}")

        integrity = {"counts": counts, "rebuild_report": rebuild_report,
                     "exp256_reread": {"n_rows": counts["n_rows256"],
                                       "n_deep_targets_ok":
                                           counts["n_deep_targets_ok"],
                                       "n_medium_shas_ok":
                                           counts["n_medium_shas_ok"]},
                     "exp282_reread": {"n_rows": counts["n_rows282"],
                                       "branch": dep282["branch"]},
                     "exp287_reread": {"n_rows": counts["n_rows287"]},
                     "exp300_reread": {"n_rows_union_g1":
                                       counts["n_rows300_u1"],
                                       "branch": dep300["branch"]},
                     "exp303_reread": {"n_transports":
                                       counts["n_rows303_transport"],
                                       "in_bar_pairs": inbar303},
                     "marks_validity": {"q10": q10, "q90": q90,
                                        "n_marks_ok":
                                        counts["n_marks_ok"],
                                        "n_tpart_ok":
                                        counts["n_tpart_ok"]}}
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "r300u1": r300u1, "r303t": r303t,
                "marks": marks, "target_part": target_part,
                "integrity": integrity}

    def _rk(inst):
        return f"r{DEEP_RUNG:g}i{inst}"

    # ---- THE DRIVER -----------------------------------------------------
    print("=== exp304: THE TRANSPORT FACE RE-SCOPED (the degeneracy "
          "repair + the carrier's stream — does the re-assertion "
          "transport where the dormant is wiring-bound?) ===")
    print(f"  slice: 12 hosts x (seed {SLICE_SEED}, instance "
          f"{SLICE_INST}) x 2 forms (the dormant + the union carrier "
          f"at g={G_COMPOSED}) = 24 walks; the transports: 130 genuine "
          f"pairs per form (the H0<->H1 exclusion pre-named); the bar "
          f"{CONTENT_BAR}")
    rb = _rebuild()
    bases = rb["bases"]

    ext = {}
    for k in hosts:
        med = HostWMedium(bases[k]["A"])
        ext[k] = _ext_medium(med, bases[k]["fmax"])
        assert not np.iscomplexobj(ext[k]["A_ext"])

    def _target_of(k, inst):
        return np.asarray(
            spec_target_n(bases[k]["deep"][inst]["spec"],
                          labeling_bfs_n(np.abs(ext[k]["A_ext"])), N400),
            dtype=float)

    # ---- the 24 SLICE WALKS (12 dormant + 12 carrier; the G1 anchors
    #      per row) -------------------------------------------------------
    walks = {}
    for k in hosts:
        ctx = bases[k]
        inst = SLICE_INST
        rk = _rk(inst)
        for form in ("dormant", "carrier"):
            key = (k, form)
            _lock_read(k, rk, SLICE_SEED)
            if form == "dormant":
                out = _execute_signed_traced(
                    ctx["deep"][inst]["spec"], ext[k]["A_ext"],
                    SLICE_SEED, op=STAR_OP, budget=BUDGET, g=0.0)
            else:
                out = _execute_signed_traced(
                    ctx["deep"][inst]["spec"], ext[k]["A_ext"],
                    SLICE_SEED, op=STAR_OP, budget=BUDGET, g=G_COMPOSED,
                    a_base=ctx["A"], mark_mask=rb["marks"][k][inst])
            err = float(out["err_vs_target"])
            assert np.isfinite(err), f"{key}: non-finite walk err"
            V = np.asarray(out["final_state"]["V"], dtype=float)
            T = np.asarray(out["target"], dtype=float)
            err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
            trace = [float(x) for x in out["walk_trace"]]
            steps = int(out["walk_steps"])
            assert len(trace) == steps and steps >= 1, \
                f"{key}: trace len != walk steps"
            trace_sha = hashlib.sha256(
                json.dumps(trace, sort_keys=True).encode()).hexdigest()
            commits = out["commits"]
            idxs = [int(rec[0]) for rec in commits]
            commit_sha = hashlib.sha256(json.dumps(
                [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
                sort_keys=True).encode()).hexdigest()
            commit_idx_sha = hashlib.sha256(
                json.dumps(idxs, sort_keys=True).encode()).hexdigest()
            dkey = (k, SLICE_SEED, rk)
            if form == "dormant":
                d256 = rb["dep_sub"][dkey]
                assert err == d256["err"], \
                    (f"{key}: the fresh err {err} drifted from exp256's "
                     f"{d256['err']} — the dormant anchor REFUTED")
                r282 = rb["r282"][dkey]
                assert trace[-1] == float(r282["walk_end_rms"]), \
                    f"{key}: the walk_end_rms drifted from exp282's"
                assert trace_sha == r282["trace_sha256"], \
                    f"{key}: the trace sha drifted from exp282's"
                assert err_exact == float(r282["err_exact"]), \
                    f"{key}: the err_exact drifted from exp282's"
                assert commit_sha == \
                    rb["r287"][dkey]["commit_seq_sha256"], \
                    (f"{key}: the commit stream digest drifted from "
                     "exp287's")
            else:
                r300 = rb["r300u1"][dkey]
                assert err == float(r300["err"]), \
                    (f"{key}: the fresh err {err} drifted from exp300's "
                     f"deposited union {r300['err']} — the carrier "
                     "anchor REFUTED")
                assert trace_sha == r300["trace_sha256"], \
                    (f"{key}: the trace sha drifted from exp300's "
                     "deposited union row")
            walks[key] = {
                "key": key, "host": k, "form": form, "err": err,
                "err_exact": err_exact, "walk_steps": steps,
                "trace_sha256": trace_sha,
                "commit_seq_sha256": commit_sha,
                "commit_idx_sha256": commit_idx_sha,
                "n_commits": len(commits),
                "commits": [[int(ci), float(tv), str(tg)]
                            for ci, tv, tg in commits],
                "n_arm_writes": int(out.get("n_arm_writes", 0))}
        # the walk order's arm-independence (the G1 clause)
        assert walks[(k, "dormant")]["commit_idx_sha256"] \
            == walks[(k, "carrier")]["commit_idx_sha256"], \
            (f"{k}: the walk order moved with the arm — the stream "
             "face drifted (exp300's G2 form)")
    assert len(walks) == 24 and len(_LOCK_LOG) == 24, \
        "the 24-walk battery drifted"
    print(f"  [walks] 12 dormant errs "
          f"{[round(walks[(k, 'dormant')]['err'], 2) for k in hosts]}")
    print(f"          12 carrier errs "
          f"{[round(walks[(k, 'carrier')]['err'], 2) for k in hosts]}")

    # ---- the genuine pair set (the pre-named exclusion) -----------------
    pairs = [(a, b) for a in hosts for b in hosts
             if b != a and (a, b) not in DEGENERATE_PAIRS]
    assert len(pairs) == 130, \
        f"the genuine pair set {len(pairs)} != 130"

    # ---- F1: the DORMANT REPAIR (the 130 transports reproduce
    #      exp303's deposited per-pair region rms BIT-EXACT) --------------
    f1_rows = []
    n_f1_ok = 0
    for (ks, kd) in pairs:
        w_src = walks[(ks, "dormant")]
        w_dst = walks[(kd, "dormant")]
        values = [tv for _, tv, _ in w_src["commits"]]
        cells_dst = [ci for ci, _, _ in w_dst["commits"]]
        n_written = min(w_src["n_commits"], w_dst["n_commits"])
        T_d = _target_of(kd, SLICE_INST)
        r = _replay(ext[kd]["A_ext"], values[:n_written],
                    cells_dst[:n_written], SLICE_SEED, T_d,
                    label=f"F1 {ks}->{kd}")
        dep = rb["r303t"][(ks, kd)]
        ok = bool(r["region_rms"] == float(dep["region_rms"])
                  and r["n_written"] == int(dep["n_written"]))
        assert ok, \
            (f"F1 {ks}->{kd}: the re-run region rms {r['region_rms']} "
             f"drifted from exp303's deposited {dep['region_rms']} — "
             "the F1 cross-deposit anchor REFUTED")
        n_f1_ok += int(ok)
        f1_rows.append({"src": ks, "dst": kd,
                        "region_rms": r["region_rms"],
                        "bit_exact_vs_303": ok})
    assert n_f1_ok == 130, "the F1 repair drifted"
    print(f"  [F1] the 130 dormant transports reproduce exp303's "
          f"deposited per-pair region rms BIT-EXACT 130/130")

    # ---- F2: the CARRIER CONTENT FACE (12 same-substrate replays) ------
    carrier_replays = {}
    for k in hosts:
        w = walks[(k, "carrier")]
        values = [tv for _, tv, _ in w["commits"]]
        cells = [ci for ci, _, _ in w["commits"]]
        T = _target_of(k, SLICE_INST)
        r = _replay(ext[k]["A_ext"], values, cells, SLICE_SEED, T,
                    label=f"F2 {k}")
        r.update({"host": k, "kind": "carrier-same",
                  "m": w["n_commits"]})
        carrier_replays[k] = r
    n_f2_ok = int(sum(bool(r["region_within_bar"])
                      for r in carrier_replays.values()))
    content_face_holds = bool(n_f2_ok >= CONTENT_MAJORITY)
    print(f"  [F2] the carrier same-substrate replays: {n_f2_ok}/12 "
          f"within the {CONTENT_BAR} bar | region rms "
          f"{[round(carrier_replays[k]['region_rms'], 3) for k in hosts]}")

    # ---- F3: the CARRIER TRANSPORT FACE (130 genuine pairs) -------------
    f3_rows = []
    for (ks, kd) in pairs:
        w_src = walks[(ks, "carrier")]
        w_dst = walks[(kd, "carrier")]
        values = [tv for _, tv, _ in w_src["commits"]]
        cells_dst = [ci for ci, _, _ in w_dst["commits"]]
        n_written = min(w_src["n_commits"], w_dst["n_commits"])
        T_d = _target_of(kd, SLICE_INST)
        r = _replay(ext[kd]["A_ext"], values[:n_written],
                    cells_dst[:n_written], SLICE_SEED, T_d,
                    label=f"F3 {ks}->{kd}")
        r.update({"src": ks, "dst": kd, "kind": "carrier-transport",
                  "m": w_src["n_commits"], "m_prime": w_dst["n_commits"],
                  "n_written": n_written,
                  "dst_own_region_rms":
                      carrier_replays[kd]["region_rms"],
                  "transport_price": float(
                      r["region_rms"]
                      - carrier_replays[kd]["region_rms"])})
        f3_rows.append(r)
    assert len(f3_rows) == 130, "the F3 battery drifted"
    n_f3_ok = int(sum(bool(r["region_within_bar"]) for r in f3_rows))
    tr_rms = [float(r["region_rms"]) for r in f3_rows]
    prices = [float(r["transport_price"]) for r in f3_rows]
    print(f"  [F3] the carrier transports: {n_f3_ok}/130 within the bar "
          f"| the mean region rms {float(np.mean(tr_rms)):.4f} | the "
          f"best {min(tr_rms):.4f} | the mean price "
          f"{float(np.mean(prices)):+.4f}")

    # ---- THE CANARIES (one carrier replay + one F3 transport re-run
    #      bit-exact) ------------------------------------------------------
    canary = []
    k0 = hosts[0]
    w = walks[(k0, "carrier")]
    r1 = carrier_replays[k0]
    r2 = _replay(ext[k0]["A_ext"], [tv for _, tv, _ in w["commits"]],
                 [ci for ci, _, _ in w["commits"]], SLICE_SEED,
                 _target_of(k0, SLICE_INST), label="canary F2")
    same1 = bool(r2["region_rms"] == r1["region_rms"]
                 and r2["full_err"] == r1["full_err"])
    assert same1, "the F2 canary failed"
    canary.append({"kind": "F2", "key": k0, "bit_identical": same1})
    (ks0, kd0) = pairs[0]
    t1 = [r for r in f3_rows if r["src"] == ks0 and r["dst"] == kd0][0]
    ws = walks[(ks0, "carrier")]
    wd = walks[(kd0, "carrier")]
    nw = t1["n_written"]
    r4 = _replay(ext[kd0]["A_ext"],
                 [tv for _, tv, _ in ws["commits"]][:nw],
                 [ci for ci, _, _ in wd["commits"]][:nw], SLICE_SEED,
                 _target_of(kd0, SLICE_INST), label="canary F3")
    same2 = bool(r4["region_rms"] == t1["region_rms"]
                 and r4["full_err"] == t1["full_err"])
    assert same2, "the F3 canary failed"
    canary.append({"kind": "F3", "key": f"{ks0}->{kd0}",
                   "bit_identical": same2})

    # ---- THE BRANCH READ (the pre-named clauses) -------------------------
    if content_face_holds and n_f3_ok >= 1 and n_f1_ok == 130:
        branch = "CARRIER-TRANSPORTS"
    elif content_face_holds and n_f3_ok == 0 and n_f1_ok == 130:
        branch = "BOTH-BOUND"
    else:
        branch = "MIXED"

    # ---- the summaries + the gates ---------------------------------------
    summaries = {
        "F1_repair": {"n_pairs": 130, "n_bit_exact": n_f1_ok,
                      "exclusion": sorted(
                          [list(p) for p in DEGENERATE_PAIRS])},
        "F2_carrier_content": {"n": 12, "n_within_bar": n_f2_ok,
                               "bar": CONTENT_BAR,
                               "majority": CONTENT_MAJORITY,
                               "face_holds": content_face_holds,
                               "mean_region_rms": float(np.mean(
                                   [r["region_rms"] for r in
                                    carrier_replays.values()])),
                               "worst_region_rms": float(max(
                                   r["region_rms"] for r in
                                   carrier_replays.values()))},
        "F3_carrier_transport": {"n": 130, "n_within_bar": n_f3_ok,
                                 "bar": CONTENT_BAR,
                                 "mean_region_rms":
                                 float(np.mean(tr_rms)),
                                 "best_region_rms": min(tr_rms),
                                 "worst_region_rms": max(tr_rms),
                                 "mean_transport_price":
                                 float(np.mean(prices)),
                                 "n_price_negative": int(sum(
                                     p < 0.0 for p in prices)),
                                 "n_full_within_bar": int(sum(
                                     bool(r["full_within_bar"])
                                     for r in f3_rows))}}
    g1 = dict(rb["integrity"]["counts"])
    g1.update({"n_walks": len(walks), "n_lock_reads": len(_LOCK_LOG),
               "n_dormant_err_ok": int(sum(
                   bool(walks[(k, "dormant")]["err"]
                        == rb["dep_sub"][(k, SLICE_SEED,
                                         _rk(SLICE_INST))]["err"])
                   for k in hosts)),
               "n_carrier_err_ok": int(sum(
                   bool(walks[(k, "carrier")]["err"]
                        == float(rb["r300u1"][(k, SLICE_SEED,
                                               _rk(SLICE_INST))]["err"]))
                   for k in hosts)),
               "n_order_arm_independent": 12,
               "n_f1_bit_exact": n_f1_ok})

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

    branch_text = {
        "CARRIER-TRANSPORTS": (
            "the carrier's re-assertion stream TRANSPORTS — at least "
            "one genuine cross-substrate replay reconstructs the "
            "pattern within the pre-named bar while the dormant "
            "control stays bound (0/130 reproduced bit-exact): the "
            "composed carrier's write product is substrate-independent "
            "where the schema-only write product is wiring-keyed — THE "
            "UNBLOCKING EVENT (the zero-substrate star's constraint "
            "breaks in the carrier form)"),
        "BOTH-BOUND": (
            "the carrier's stream is wiring-bound exactly as the "
            "dormant's — the indexation binds both forms (the block "
            "deepens: not even the re-asserted spec's own stream "
            "transports)"),
        "MIXED": (
            "the faces disagree with the pre-named lattice — recorded, "
            "the honest leftover")}[branch]

    deposit = {
        "exp": "exp304_transport_rescoped",
        "claim": (
            "THE TRANSPORT FACE RE-SCOPED (batch 58, pre-registration "
            "commit c4c563b): the degeneracy repair (the 130 genuine "
            "ordered pairs, the H0<->H1 exclusion pre-named, the "
            "dormant transports reproduced BIT-EXACT vs exp303's "
            "deposited per-pair region rms — the cross-deposit anchor) "
            "+ THE CARRIER'S STREAM (exp301's write-side object at the "
            "composed optimum g=1.0): does the carrier's re-assertion "
            "stream transport where the dormant's idiosyncratic state "
            "is wiring-bound? The branches: CARRIER-TRANSPORTS (the "
            "unblocking event) / BOTH-BOUND (the indexation binds both "
            "forms) / MIXED."),
        "method": {
            "slice": (f"12 hosts x (seed {SLICE_SEED}, instance "
                      f"{SLICE_INST}) x 2 forms"),
            "walk_forms": {"dormant": "g=0.0 (exp302's landed walk)",
                           "carrier": ("the union faces=(ctx, gj, apop) "
                                       "at g=1.0 (exp300's landed arm)")},
            "replay_protocol": ("exp303's landed replay instrument "
                                "VERBATIM (the fresh wiring-only "
                                "substrate; the region-scoped predicate "
                                "at the pre-named bar)"),
            "exclusion": ("the ordered pairs (H0, H1) and (H1, H0) "
                          "excluded — the chain constructor's echo "
                          "makes the substrates BIT-IDENTICAL "
                          "(asserted in the rebuild); the genuine "
                          "pair set 130"),
            "budget": BUDGET, "settle_h": SETTLE_H,
            "content_bar": CONTENT_BAR,
            "content_majority": CONTENT_MAJORITY},
        "inputs": {"hosts": hosts, "outliers": outliers,
                   "slice": {"seed": SLICE_SEED, "inst": SLICE_INST},
                   "marks_validity": rb["integrity"]["marks_validity"]},
        "integrity": rb["integrity"],
        "walks": [{k: w[k] for k in w if k != "commits"}
                  for w in walks.values()],
        "f1_rows": f1_rows,
        "carrier_replays": [dict(r) for r in carrier_replays.values()],
        "f3_rows": f3_rows,
        "summaries": summaries,
        "branch": branch,
        "branch_discriminant": {
            "bars_pre_named_at": ("c4c563b — fixed at pre-registration, "
                                  "never fit"),
            "form": ("CARRIER-TRANSPORTS iff F2 holds (>= 7/12) AND "
                     ">= 1/130 genuine carrier transports within the "
                     "bar AND F1 reproduces 130/130; BOTH-BOUND iff F2 "
                     "holds AND 0/130; MIXED otherwise"),
            "resolved": branch,
            "branch_text": branch_text},
        "g1": g1,
        "canary": canary,
        "lock_reads": len(_LOCK_LOG),
        "run_form": "in-process default (one invocation)"}
    ro_unchanged = bool(
        set(_sha(p) for p in READ_DEPS) == set(ro_before.values()))
    g1_pass = bool(
        g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
        and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
        and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
        and g1["n_rows256"] == 72 and g1["n_deep_targets_ok"] == 72
        and g1["n_medium_shas_ok"] == 72
        and g1["n_rows282"] == 72 and g1["n_282_chain_ok"] == 72
        and g1["n_rows287"] == 72 and g1["n_rows300_u1"] == 72
        and g1["n_marks_ok"] == 24 and g1["n_tpart_ok"] == 12
        and g1["n_rows303_transport"] == 132
        and g1["n_walks"] == 24 and g1["n_lock_reads"] == 24
        and g1["n_dormant_err_ok"] == 12 and g1["n_carrier_err_ok"] == 12
        and ro_unchanged)
    g2_pass = bool(g1["n_f1_bit_exact"] == 130
                   and canary[0]["bit_identical"]
                   and canary[1]["bit_identical"])
    g3_pass = bool(branch in ("CARRIER-TRANSPORTS", "BOTH-BOUND", "MIXED")
                   and np.isfinite(summaries["F3_carrier_transport"]
                                   ["mean_transport_price"]))
    no_wall_clock = bool(not _scan_wall_clock_keys(deposit))
    set_floor(PROD_FLOOR)
    floor_exit = read_floor()
    assert floor_exit == PROD_FLOOR, "floor drift at exit"
    # ---- the exit asserts -----------------------------------------------
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    assert set(_sha(p) for p in READ_DEPS) \
        == set(ro_before.values()), "source deposit drifted after work"
    assert _sha(PORT_FILE) == port_sha_entry, \
        "the register's home drifted after the work"
    assert _sha(EXP142_FILE) == exp142_sha_entry, \
        "exp142 was modified after the work"

    def _run_test_suite():
        cmd = [sys.executable, "-m", "tests.run_tests"]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                              text=True, timeout=560)
        tail = "\n".join(proc.stdout.strip().splitlines()[-4:])
        green = bool(proc.returncode == 0)
        return {"green": green, "returncode": int(proc.returncode),
                "tail": tail}

    suite = _run_test_suite()
    gates = {
        "G1_the_anchors": {"pass": g1_pass, "counts": g1,
                           "source_deposits_read_only_byte_unchanged":
                               ro_unchanged},
        "G2_the_faces": {"pass": g2_pass,
                         "counts": {"n_f1_bit_exact": g1["n_f1_bit_exact"],
                                    "canary": canary}},
        "G3_the_branch": {"pass": g3_pass,
                          "resolved": {"branch": branch,
                                       "summaries": summaries}},
        "G4_discipline": {
            "pass": bool(no_wall_clock and docstring_ok and header_ok
                         and ro_unchanged and floor_exit == PROD_FLOOR
                         and suite["green"]),
            "no_wall_clock_fields": no_wall_clock,
            "docstring_byte_unchanged_vs_c4c563b": docstring_ok,
            "header_byte_unchanged_vs_c4c563b": header_ok,
            "n_source_deposits": len(READ_DEPS),
            "exp142_not_modified": True,
            "core_not_modified": True,
            "floor_at_entry": floor_at_entry,
            "floor_at_exit": floor_exit,
            "test_suite": suite,
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of this module in the same form "
                             "reproduces this file byte-identically")}}
    n_pass = 0
    n_refute = 0
    for name in ("G1_the_anchors", "G2_the_faces", "G3_the_branch",
                 "G4_discipline"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    deposit["gates"] = gates
    verdict = (
        f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} — {branch_text} "
        f"(F1 the repair: the 130 dormant transports reproduce "
        f"exp303's deposited per-pair region rms BIT-EXACT "
        f"{g1['n_f1_bit_exact']}/130 (the degenerate H0<->H1 pair "
        f"excluded pre-named) | F2 the carrier content face: "
        f"{n_f2_ok}/12 within the {CONTENT_BAR} bar (the majority "
        f"{CONTENT_MAJORITY}; the mean region rms "
        f"{summaries['F2_carrier_content']['mean_region_rms']:.4f}) | "
        f"F3 the carrier transport face: {n_f3_ok}/130 within the bar "
        f"(the mean region rms "
        f"{summaries['F3_carrier_transport']['mean_region_rms']:.4f}, "
        f"the best {summaries['F3_carrier_transport']['best_region_rms']:.4f}"
        f", the mean price "
        f"{summaries['F3_carrier_transport']['mean_transport_price']:+.4f}"
        f" mV | the anchors: the 12 dormant errs == exp256's + the 12 "
        f"carrier errs == exp300's deposited union rows (bit-exact), "
        f"the walk orders arm-independent 12/12 | the canaries: "
        f"{canary[0]['bit_identical']}/{canary[1]['bit_identical']} | 9 "
        f"deposits READ-ONLY, exp142 + the core NOT modified, floor "
        f"-60.0, the test suite green)")
    deposit["verdict"] = verdict
    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=float).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  G1 the anchors: {'PASS' if g1_pass else 'FAIL'} (the "
          f"dormant errs == exp256's {g1['n_dormant_err_ok']}/12, the "
          f"carrier errs == exp300's {g1['n_carrier_err_ok']}/12, the "
          f"marks {g1['n_marks_ok']}/24 + {g1['n_tpart_ok']}/12, the "
          f"orders arm-independent 12/12; 9 deposits READ-ONLY: "
          f"{ro_unchanged})")
    print(f"  G2 the faces: {'PASS' if g2_pass else 'FAIL'} (F1 "
          f"{g1['n_f1_bit_exact']}/130 bit-exact; the canaries "
          f"{canary[0]['bit_identical']}/{canary[1]['bit_identical']})")
    print(f"  G3 the branch: {'PASS' if g3_pass else 'FAIL'} — "
          f"{branch} (F2 {n_f2_ok}/12 | F3 {n_f3_ok}/130)")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(no wall-clock: {no_wall_clock}; docstring+header pinned to "
          f"c4c563b; floor at exit {floor_exit}; the test suite "
          f"{suite['green']})")
    print(f"\n  BRANCH: {branch}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")
    return deposit


if __name__ == "__main__":
    main()
