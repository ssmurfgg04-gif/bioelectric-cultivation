#!/usr/bin/env python3
"""exp302 — THE COMPOSED STRESS FACE: IS THE ~29x PROTECTION
PRESERVED UNDER COMPOSITION? (batch 56; ledger L286's registered
next (a) — exp293 landed PROTECTED: the ctx register's 2x2
interaction P = +0.73 mV, the write-time stress hurting ~29x LESS
when the history is carried than the register's own rest
improvement would suggest; exp300 landed MONOTONE-TO-1.0: the
composed carrier's optimum IS the saturated face g=1.0 of the union
faces=(ctx, gj, apop) on ONE walk; exp301 landed WRITE-SIDE-CARRIED:
the carrier changes WHAT the program commits, not the structure of
how it commits. THE OPEN QUESTION: does the PROTECTION face survive
composition — is the composed union (the strongest carrier the stack
has) under write-time ionic stress degraded LESS than the schema-only
walk by more than the pre-named margin, and how does the composed
protection compare to the single register's (the audit face — does
protection COMPOSE like the improvement did below saturation)? The
null: the stress degradation is additive under the union too and the
composed interaction == the single register's (P_union == P_ctx).)

THE INSTRUMENT (exp293's landed 2x2 factorial form COMPOSED VERBATIM
with exp300's landed union coupling + exp290's landed stress-pin
schedule; the 72-row substituted battery, exp256's):
  U0-S0  union OFF (the g=0 schema-only form), floor -60.0
         (the anchor — the errs reproduce exp256's deposited errs
         BIT-EXACT 72/72, the walk anchors exp282's 72/72);
  U1-S0  union ON (the faces=(ctx, gj, apop) union at the composed
         optimum g=1.0, exp300's landed arm VERBATIM), floor -60.0
         (the anchor — the errs + the trace shas reproduce exp300's
         deposited union g=1.0 rows BIT-EXACT 72/72);
  U0-S1  union OFF, the WRITE-TIME stress (the walk at the -35.0
         pin, exp290's A1 arm verbatim — the errs reproduce exp290's
         deposited A1 errs BIT-EXACT 72/72);
  U1-S1  union ON (g=1.0), the WRITE-TIME stress (THE NEW CELL).
THE PROTECTION READ (zero knobs): the composed protection delta
  P_union = [mean_err(U0-S1) - mean_err(U1-S1)]
            - [mean_err(U0-S0) - mean_err(U1-S0)]
(the standard 2x2 interaction on the union: P > 0 = the union
PROTECTS under composition; P = 0 = additive independence; P < 0 =
the union AMPLIFIES the stress harm).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: U0-S0 == exp256's deposited errs BIT-EXACT 72/72
      (the verified flags 72/72; exp282's walk_end_rms + trace shas +
      err_exact 72/72 — the SAME walk exp282 deposited; the
      commit-layer digests vs exp287/exp288 recorded AUDIT-ONLY);
      U1-S0 == exp300's deposited union g=1.0 rows BIT-EXACT 72/72
      (the errs + the trace shas; the face write-count + register
      digest faces AUDIT-ONLY); U0-S1 == exp290's deposited A1 errs
      BIT-EXACT 72/72 (the fresh trace shas + floor schedules
      AUDIT-ONLY); the MARKS' VALIDITY: the rebuilt q10/q90 +
      target_part + bands reproduce exp300's deposited arm_inputs
      BIT-EXACT (fail=STOP — the union's armed-site plan is pinned
      to the deposited one); the floor asserts (the -35.0 pin during
      the walk in the S1 cells 144/144, the -60.0 encode in the S0
      cells 144/144, -60.0 at every settle/decode 288/288); 11
      deposits READ-ONLY (exp243/256/272/273/282/287/288/289/290/
      293/300 — sha before/after); the rebuild chain sha-asserted.
  G2  THE NEW CELL'S INTEGRITY (U1-S1, zero-knob asserted, fail=STOP
      per row): finite errs 72/72; the A3 convention 72/72; the
      trace lengths == walk_steps 72/72; the commit counts ==
      walk_steps 72/72; the register's replay equality (exp289's G2
      form) 72/72; the STREAM face (the commit-index digests +
      walk_steps + n_commits identical across ALL FOUR cells) 72/72;
      the PLAN face (the union's armed-site counts n_arm_writes +
      n_sigma_writes + n_blend_writes identical across U1-S0/U1-S1 —
      the plan is (target, A)-determined, stress-independent) 72/72;
      the S* lock reads 288 (4 cells x 72).
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars): P_union vs
      the pre-named bar PROTECT_BAR 0.05 mV (the exp293 margin form):
      PROTECTED-PRESERVED  iff P_union >= 0.05;
      AMPLIFIED             iff P_union <= -0.05;
      ADDITIVE              otherwise (the honest null).
      AUDIT-ONLY, never gating: the composition's protection
      comparison (P_union vs exp293's deposited P_ctx — does
      protection compose?); the ratio face (P_union / the union's
      rest improvement) vs exp293's ~29x; the per-host P (the
      outliers H3/H5 disclosed); the worst-err per cell vs the 6.0
      bar; the commit src censuses per cell (the floor's effect on
      the (e) branch); the gj landed compensation assert re-run per
      U1 row (exp259's conservation identity — exp300's G2 form).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified
      (the composition uses exp300's landed union coupling + exp290's
      landed pin schedule — the module attributes set around the
      calls, disclosed); NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PROTECTED-PRESERVED / AMPLIFIED / ADDITIVE
at the PROTECT_BAR 0.05 mV form.

RUN: 288 decodes ~ 5-8 min — the pre-named form is the CHECKPOINT-
SPLIT EXP302_MODE=pass1 (the S0 cells, 144 decodes) | pass2 (the S1
cells, 144 decodes) | merge; the in-process default for the GitHub
runners. Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp302_composed_stress_face.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 26e15a1; gates G1-G4
    #      evaluated exactly once. THE COMPOSITION: exp300's landed
    #      union coupling (the faces=(ctx, gj, apop) walk, its landed
    #      body's _execute_signed_traced VERBATIM) + exp290's landed
    #      stress-pin schedule (the A1 write-time -35.0 pin around the
    #      calls, its landed body's arm form + exp293's composed
    #      floor_rec boundary reads) — both VERBATIM, the module
    #      attributes set around the calls, disclosed) ================
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
    #      the 26e15a1 pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "acaed8d126d080217581c434375aa949220a0ff24737629061956c8eaa2486c2")
    EXPECTED_HEADER_SHA256 = (
        "1e6102a78336ef2636fdb3656c7eb1835794a72e27a5f8dd6642d63168a0a245")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 26e15a1"
    assert header_ok, "header drifted from 26e15a1"

    # ---- the -60.0 floor (G4: asserted at exit; exp290's disclosed
    #      exp169-import discipline — the whole reader chain imported
    #      FIRST, the floor restored after; the -35.0 reader-line pin
    #      is the S1 cells' write-time stress, disclosed) -----------------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)   # exp169's PIN_MODULES form
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    set_floor_seen: list = []

    def set_floor(v):
        # exp169's disclosed pin form (exp290's landed set_floor
        # VERBATIM): the module attribute set around the calls (exp142
        # and the core NOT modified — the attribute is READ AT STEP
        # TIME by the walk's commit branch (e))
        set_floor_seen.append(float(v))
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
    #      THE 2x2 FACTORIAL + THE BRANCH BAR — pre-named) ---------------
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
    # STEPS_PER_CELL == 8 (the exp287/exp288/exp289/exp290 traced
    # replica form).
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE 2x2 FACTORIAL (pre-named): the carrier state (U0 the union
    # off / U1 the faces=(ctx, gj, apop) union at the composed optimum
    # g=1.0, exp300's landed arm) x the stress state (S0 floor -60.0 /
    # S1 the write-time -35.0 pin during the walk only).
    CELLS = ("U0-S0", "U1-S0", "U0-S1", "U1-S1")
    CELL_G = {"U0-S0": 0.0, "U1-S0": 1.0, "U0-S1": 0.0, "U1-S1": 1.0}
    CELL_ARM = {"U0-S0": "A0", "U1-S0": "A0", "U0-S1": "A1", "U1-S1": "A1"}
    CELL_NAMES = {
        "U0-S0": "union OFF, floor -60.0 (the exp256 anchor)",
        "U1-S0": ("union ON faces=(ctx, gj, apop) at the composed "
                  "optimum g=1.0, floor -60.0 (the exp300 deposited "
                  "union anchor)"),
        "U0-S1": ("union OFF, the write-time -35.0 pin during the "
                  "walk only (exp290's A1 arm verbatim)"),
        "U1-S1": ("union ON g=1.0 + the write-time -35.0 pin during "
                  "the walk only (THE NEW CELL)")}
    G_COMPOSED = 1.0                       # exp300's composed optimum
    FACES_UNION = ("ctx", "gj", "apop")    # exp300's landed union arm
    # THE BRANCH BAR (pre-named at 26e15a1, numeric, never fit)
    PROTECT_BAR = 0.05                     # the exp293 margin form
    # THE FLOOR SCHEDULES (exp290's landed FLOOR_SCHEDULE form — the
    # machinery's own registered constants -60.0 / -35.0):
    ARM_NAMES = {"A0": "anchor (-60.0 everywhere)",
                 "A1": "write-stress (-35.0 during the walk only)"}
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
               "decode_start": PROD_FLOOR}}
    # the commit source tags (the pre-named census; audit-only — the
    # floor's effect on the (e) branch, exp290's disclosed form)
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

    # ---- the composition's own provenance: the two composed files'
    #      bytes (the register's home + the walk's home — NEITHER
    #      modified by this module) --------------------------------------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; the
    #      pre-registration's named list, 11 deposits) ------------------
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
    DEP289 = os.path.join(ROOT, "results",
                          "exp289_history_register.json")
    DEP290 = os.path.join(ROOT, "results", "exp290_stress_timing.json")
    DEP293 = os.path.join(ROOT, "results", "exp293_history_stress.json")
    DEP300 = os.path.join(ROOT, "results",
                          "exp300_composed_optimum.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287, DEP288,
                 DEP289, DEP290, DEP293, DEP300)
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit",
                  DEP288: "exp288_deposit", DEP289: "exp289_deposit",
                  DEP290: "exp290_deposit", DEP293: "exp293_deposit",
                  DEP300: "exp300_deposit"}
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
    with open(DEP288) as fh:
        dep288 = json.load(fh)
    with open(DEP289) as fh:
        dep289 = json.load(fh)
    with open(DEP290) as fh:
        dep290 = json.load(fh)
    with open(DEP293) as fh:
        dep293 = json.load(fh)
    with open(DEP300) as fh:
        dep300 = json.load(fh)

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep287["hosts"] == hosts, "exp287's host frame drifted"
    assert dep288["hosts"] == hosts, "exp288's host frame drifted"
    assert dep289["hosts"] == hosts, "exp289's host frame drifted"
    assert dep290["hosts"] == hosts, "exp290's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    assert dep272["descriptive"]["premium_hosts"] == outliers, \
        "exp272's premium_hosts drifted from the outlier pre-name"
    cluster = [h for h in hosts if h not in outliers]
    assert len(cluster) == 10, "the ten-host cluster drifted"

    rec272 = {r["host"]: r for r in dep272["per_host"]}

    # ---- exp208's classify VERBATIM (the CLEAN masks; used by the
    #      union's class plan (exp300's landed form) and by the
    #      rebuild's boundary-count asserts) ------------------------------
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

    # ---- exp259's compensation instrument (the landed form's own
    #      machinery, re-run per U1 row as the NON-HISTORY path's
    #      assert; the HIST coupling does NOT consume it — exp300's G2
    #      form carried) --------------------------------------------------
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
        """exp259's landed compensation VERBATIM: multipliers on the
        substituted medium's PAIR-JUNCTION cells (m_i = target_part /
        part_i), non-pair cells 1.0, applied as row+column scalings,
        then the GLOBAL conservation renormalization (the landed
        assert's own face). Returns (W, m, residual)."""
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

    # ---- THE COMPOSED TRACED REPLICA: exp300's landed
    #      _execute_signed_traced (the union coupling faces=(ctx, gj,
    #      apop) — the sigma face first, then the blends, the overlap
    #      recorded not doubled) with exp290's landed ARM PIN schedule
    #      slotted at its landed boundaries (the A1 write-stress floor
    #      goes on at the ENCODE WINDOW's start, through the last
    #      commit, restored before the settle; the A0 arm never pins;
    #      the floor reads are PURE — the RNG stream and the dynamics
    #      untouched; the walk loop is exp300's VERBATIM otherwise) --
    def _execute_signed_traced_union_stress(
            spec, adjacency, seed, op, budget,
            g=0.0, a_base=None, mark_mask=None, arm="A0"):
        assert arm in ("A0", "A1"), f"unknown arm {arm}"
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
        # the register's PRESENCE + INIT at the walk's start (fail=STOP
        # per row): the init == the spec's install BIT-EXACT (G2's
        # per-arm init face; runs BEFORE the A1 pin — the history
        # starts as the program's own target at the production floor)
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
                    "reg_init_ok": reg_init_ok, "floor_rec": floor_rec,
                    "n_arm_writes": 0, "n_sigma_writes": 0,
                    "n_blend_writes": 0}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        # ---- exp290's ARM PIN (A1 only): the write-stress floor goes
        #      on at the ENCODE WINDOW's start, through the last commit
        #      (the landed schedule; A0 runs the encode at -60.0) ------
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
        trace: list = []
        order: list = []
        commits: list = []
        n_arm_writes = 0
        n_sigma_writes = 0
        n_blend_writes = 0
        # the union's SITE plan (computed ONLY when the coupling is
        # armed; T and a_base are g- and stress-independent — the row
        # sets match 1:1 across the whole battery)
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
                # the landed band-containment assert (exp264's own)
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
        first_commit_done = False
        for i, src in order:
            for _ in range(budget):                  # the landed
                c.step(dt)                           # parameterization
            canon_src = getattr(c, "phi_spec_canon", None)
            # the verbatim commit branch chain (pure reads; the noise
            # draw ONCE below, at the arm's pre-named sigma); the floor
            # read AT STEP TIME is live (exp290's landed form) — the A1
            # pin (-35.0) re-routes the sub-floor spec cells to the
            # canon fallback; A0 reads -60.0
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
            #      ZERO at g == 0.0; the coupling order fixed: the
            #      sigma face first (the draw's scale), then the blends
            #      (the write's value); at a cell carrying BOTH blend
            #      faces the blend is applied ONCE) ----------------------
            if g > 0.0:
                hist_i = float(c.phi_history[i])
                cell_armed = False
                if "apop" in FACES_UNION:
                    # exp264's landed form: the sigma relaxation at the
                    # marked cell + the channel-write face (the mark is
                    # state, carried in ch6); the draw's SCALE changes,
                    # the stream POSITION does not (one normal/commit)
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
                    # exp289's landed form VERBATIM (the self blend at
                    # the canon-boundary cells)
                    blend = True
                if "gj" in FACES_UNION and bool(J[i]):
                    # the blend at exp259's site; ch2 carries the
                    # register read (the coupling's per-cell scalar)
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
            # the commit value recorded AT THE WRITE (the exp287 face)
            commits.append((int(i), float(written), src_tag))
            # THE PORT'S POPULATION (arm-independent, g-independent):
            # after the write the register holds the committed value
            c.phi_history[i] = written
            # exp290's first-commit floor read (a pure recording)
            if not first_commit_done:
                floor_rec["walk_first_commit"] = read_floor()
                first_commit_done = True
            # the per-step RMS read (a pure read; the walk's
            # full-frame convergence; unchanged)
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        floor_rec["walk_last_commit"] = read_floor()
        # the write-set coverage (the replica's side, the walk order in
        # scope): the commit sequence elementwise == the walked order
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        # ---- exp290's SETTLE BOUNDARY (the pin-restore point): the A1
        #      floor restored to -60.0 before the settle -----------------
        if arm == "A1":
            set_floor(PROD_FLOOR)
        floor_rec["settle_start"] = read_floor()
        c.run(15.0, dt=dt)
        floor_rec["decode_start"] = read_floor()
        # the register AT THE WALK'S END (G2's per-arm faces, fail=STOP)
        reg = getattr(c, "phi_history", None)
        reg_present_ok = bool(reg is not None)
        assert reg_present_ok, "the history register vanished across the walk"
        reg = np.asarray(reg, dtype=float)
        reg_finite_ok = bool(np.all(np.isfinite(reg)))
        assert reg_finite_ok, "non-finite history-register entry"
        replay_idx = [int(rec[0]) for rec in commits]
        replay_val = np.asarray([float(rec[1]) for rec in commits],
                                dtype=float)
        reg_replay_ok = bool(np.array_equal(reg[replay_idx], replay_val))
        assert reg_replay_ok, \
            "the register's write-set face drifted from the commit replay"
        comp = np.ones(n, dtype=bool)
        comp[replay_idx] = False
        reg_complement_ok = bool(np.array_equal(reg[comp], target[comp]))
        assert reg_complement_ok, \
            "the register's non-write-set face drifted from the spec install"
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
               "reg_init_ok": reg_init_ok,
               "reg_present_ok": reg_present_ok,
               "reg_replay_ok": reg_replay_ok,
               "reg_complement_ok": reg_complement_ok,
               "reg_finite_ok": reg_finite_ok,
               "phi_history_sha256": _f_sha(reg),
               "n_arm_writes": int(n_arm_writes),
               "n_sigma_writes": int(n_sigma_writes),
               "n_blend_writes": int(n_blend_writes),
               "floor_rec": floor_rec}
        return out

    # ---- the state-carrying replica read (exp289's form VERBATIM,
    #      with the composed walk + the arm pin schedule) ---------------
    def _scoped_row_read_union_stress(spec, med, seed, fmax, budget,
                                      g=0.0, a_base=None, mark_mask=None,
                                      arm="A0"):
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
            out = _execute_signed_traced_union_stress(
                spec, A_ext, seed, op=STAR_OP, budget=budget, g=g,
                a_base=a_base, mark_mask=mark_mask, arm=arm)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- ONE ARMED-ROW DECODE (the register + the commit bookkeeping
    #      asserted fail=STOP per row; the ANCHOR set per cell per the
    #      pre-named G1 clauses — fail=STOP; the extra cross-deposit
    #      faces recorded AUDIT-ONLY, never gating) -----------------------
    def _decode_cell_row(cell, host, row_key, spec, med, seed, fmax,
                         A_base, mark_mask, dep_rec, rec282, rec287,
                         rec288, rec300u1, rec290a1, target_part):
        assert cell in CELLS, f"unknown cell {cell}"
        g_u = float(CELL_G[cell])
        arm = CELL_ARM[cell]
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_union_stress(
            spec, med, seed, fmax, BUDGET,
            g=g_u, a_base=(A_base if g_u > 0.0 else None),
            mark_mask=(mark_mask if g_u > 0.0 else None),
            arm=arm)
        # ---- THE FLOOR SCHEDULE (G1's facets, asserted per row
        #      fail=STOP, exp290's landed form) ---------------------------
        for k, v in FLOOR_SCHEDULE[arm].items():
            got = out["floor_rec"].get(k)
            assert got == v, \
                (f"{host} {row_key} s{seed} {cell}: the floor at {k} "
                 f"read {got} != the pre-named {v} (fail=STOP)")
        floor_schedule_ok = bool(all(out["floor_rec"].get(k) == v
                                     for k, v in
                                     FLOOR_SCHEDULE[arm].items()))
        err = float(out["err_vs_target"])
        assert np.isfinite(err), \
            f"{host} {row_key} s{seed} {cell}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, \
            f"{host} {row_key} s{seed} {cell}: A3 state-convention drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        trace_len_ok = bool(len(trace) == steps and steps >= 1)
        assert trace_len_ok, \
            (f"{host} {row_key} s{seed} {cell}: trace {len(trace)} != "
             f"walk steps {steps}")
        all_finite = bool(all(np.isfinite(trace)))
        assert all_finite, \
            f"{host} {row_key} s{seed} {cell}: non-finite trace entry"
        final = trace[-1]
        final_positive_ok = bool(final > 0.0)
        assert final_positive_ok, \
            f"{host} {row_key} s{seed} {cell}: final RMS == 0"
        # TA3 — the convergence point (existence; exp282's assert form)
        thresh = 2.0 * final
        conv = None
        for kk, v in enumerate(trace):
            if v < thresh:
                conv = kk
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            (f"{host} {row_key} s{seed} {cell}: the convergence point "
             "does not exist")
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        # ---- THE COMMIT RECORDING bookkeeping (the exp287 form,
        #      fail=STOP) -------------------------------------------------
        commits = out["commits"]
        n_commits = len(commits)
        commits_count_ok = bool(n_commits == steps == len(trace))
        assert commits_count_ok, \
            (f"{host} {row_key} s{seed} {cell}: the commit count "
             f"{n_commits} != walk steps {steps} — the write set is not "
             "fully recorded")
        idxs = [int(rec[0]) for rec in commits]
        commits_unique_ok = bool(len(set(idxs)) == n_commits)
        assert commits_unique_ok, \
            (f"{host} {row_key} s{seed} {cell}: a committed cell "
             "written twice")
        coverage_ok = bool(out["coverage_ok"])
        assert coverage_ok, \
            f"{host} {row_key} s{seed} {cell}: the write-set coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        commits_finite_ok = bool(all(np.isfinite(v) for v in vals))
        assert commits_finite_ok, \
            (f"{host} {row_key} s{seed} {cell}: non-finite commit value")
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        census_ok = bool(sum(census_src.values()) == n_commits
                         and set(tags) <= set(COMMIT_SOURCES))
        assert census_ok, \
            (f"{host} {row_key} s{seed} {cell}: the commit source census "
             "drifted")
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        commit_idx_sha = hashlib.sha256(
            json.dumps(idxs, sort_keys=True).encode()).hexdigest()
        # the union's FACE-WRITE bookkeeping (exp300's G2 form, carried)
        n_arm_writes = int(out["n_arm_writes"])
        n_sigma_writes = int(out["n_sigma_writes"])
        n_blend_writes = int(out["n_blend_writes"])
        if g_u > 0.0:
            # the gj landed compensation assert re-run per U1 row
            # (exp259's conservation identity — exp300's G2 form)
            _W, _m, _resid = compensate(A_base, T, target_part)
            gj_assert_ok = bool(_resid <= 1e-9)
        else:
            gj_assert_ok = None
        # the commit layer's self-consistency read (audit-only, the
        # exp287 replay form)
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        assert np.isfinite(sc_rms), \
            f"{host} {row_key} s{seed} {cell}: non-finite sc_rms"
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed} {cell}: non-finite cvt_rms"
        sc_frac = float(sc_rms / err_exact)

        # ---- THE REGISTER FACE (the replica's own fail=STOP asserts;
        #      the flags + the digest recorded per row) ------------------
        reg = {"present_ok": bool(out["reg_present_ok"]),
               "init_ok": bool(out["reg_init_ok"]),
               "replay_ok": bool(out["reg_replay_ok"]),
               "complement_ok": bool(out["reg_complement_ok"]),
               "finite_ok": bool(out["reg_finite_ok"]),
               "phi_history_sha256": str(out["phi_history_sha256"])}
        assert reg["present_ok"] and reg["init_ok"] and reg["replay_ok"] \
            and reg["complement_ok"] and reg["finite_ok"], \
            f"{host} {row_key} s{seed} {cell}: the register face drifted"

        rec = {"cell": cell, "arm": arm, "g_u": g_u,
               "host": host, "seed": int(seed),
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
               "commit_idx_sha256": commit_idx_sha,
               "src_census": census_src,
               "n_arm_writes": n_arm_writes,
               "n_sigma_writes": n_sigma_writes,
               "n_blend_writes": n_blend_writes,
               "gj_assert_ok": gj_assert_ok,
               "sc_rms": sc_rms, "sc_frac": sc_frac, "cvt_rms": cvt_rms,
               "floor_rec": {k: float(v)
                             for k, v in out["floor_rec"].items()},
               "floor_schedule_ok": floor_schedule_ok,
               "register": reg,
               "final_positive_ok": final_positive_ok,
               "conv_ok": conv_ok}
        # ---- THE ANCHOR ASSERTS (per cell, the pre-named G1 set;
        #      fail=STOP; the extra cross-deposit faces AUDIT-ONLY) -----
        if cell == "U0-S0":
            # THE S0 ANCHOR: exp256's deposited errs BIT-EXACT (the
            # exp289/exp290 S0 discipline: the walk anchors too)
            s0_err_ok = bool(err == dep_rec["err"])
            s0_ver_ok = bool(bool(out["program_verified"])
                             == bool(dep_rec["verified"]))
            assert s0_err_ok, \
                (f"{host} {row_key} s{seed} U0-S0: the fresh err {err} "
                 f"drifted from exp256's deposited {dep_rec['err']} — "
                 "the U0-S0 anchor REFUTED")
            assert s0_ver_ok, \
                f"{host} {row_key} s{seed} U0-S0: the verified flag drifted"
            we_ok = bool(final == float(rec282["walk_end_rms"]))
            assert we_ok, \
                (f"{host} {row_key} s{seed} U0-S0: the fresh "
                 "walk_end_rms drifted from exp282's deposited")
            ts_ok = bool(trace_sha == rec282["trace_sha256"])
            assert ts_ok, \
                (f"{host} {row_key} s{seed} U0-S0: the fresh trace sha "
                 "drifted from exp282's deposited — the walk is not the "
                 "traced one")
            ee_ok = bool(err_exact == float(rec282["err_exact"]))
            assert ee_ok, \
                (f"{host} {row_key} s{seed} U0-S0: the fresh err_exact "
                 "drifted from exp282's deposited")
            rec["s0_err_ok"] = s0_err_ok
            rec["s0_verified_ok"] = s0_ver_ok
            rec["walk_end_282_ok"] = we_ok
            rec["trace_sha_282_ok"] = ts_ok
            rec["err_exact_282_ok"] = ee_ok
            # the commit-layer digests vs the anchored deposits
            # (exp287/exp288 — audit-only, exp290's disclosed form)
            rec["commit_sha_287_ok"] = bool(
                commit_sha == rec287["commit_seq_sha256"])
            rec["commit_sha_288_ok"] = bool(
                commit_sha == rec288["commit_seq_sha256"])
            rec["cvt_287_ok"] = bool(cvt_rms == float(rec287["cvt_rms"]))
        elif cell == "U1-S0":
            # THE exp300 ANCHOR: the deposited union g=1.0 rows' errs +
            # trace shas BIT-EXACT (the pre-named G1 clause)
            u1_err_ok = bool(err == float(rec300u1["err"]))
            assert u1_err_ok, \
                (f"{host} {row_key} s{seed} U1-S0: the fresh err {err} "
                 f"drifted from exp300's deposited union g=1.0 "
                 f"{rec300u1['err']} — the U1-S0 anchor REFUTED")
            u1_ts_ok = bool(trace_sha == rec300u1["trace_sha256"])
            assert u1_ts_ok, \
                (f"{host} {row_key} s{seed} U1-S0: the fresh trace sha "
                 "drifted from exp300's deposited union g=1.0 trace "
                 "sha — the composed walk is not the deposited one")
            rec["u1s0_err_ok"] = u1_err_ok
            rec["u1s0_trace_sha_ok"] = u1_ts_ok
            # audit-only: the rest of the deposited union row face
            rec["u1s0_walk_end_ok"] = bool(
                final == float(rec300u1["walk_end_rms"]))
            rec["u1s0_reg_sha_ok"] = bool(
                reg["phi_history_sha256"]
                == rec300u1["register"]["phi_history_sha256"])
            rec["u1s0_narm_ok"] = bool(
                n_arm_writes == int(rec300u1["n_arm_writes"]))
            rec["u1s0_nsigma_ok"] = bool(
                n_sigma_writes == int(rec300u1["n_sigma_writes"]))
            rec["u1s0_nblend_ok"] = bool(
                n_blend_writes == int(rec300u1["n_blend_writes"]))
            rec["u1s0_ncommits_ok"] = bool(
                n_commits == int(rec300u1["n_commits"]))
            rec["u1s0_cvt_ok"] = bool(
                cvt_rms == float(rec300u1["cvt_rms"]))
        elif cell == "U0-S1":
            # THE exp290 ANCHOR: the deposited A1 errs BIT-EXACT (the
            # pre-named G1 clause)
            ws1_err_ok = bool(err == float(rec290a1["err"]))
            assert ws1_err_ok, \
                (f"{host} {row_key} s{seed} U0-S1: the fresh err {err} "
                 f"drifted from exp290's deposited A1 "
                 f"{rec290a1['err']} — the U0-S1 anchor REFUTED")
            rec["u0s1_err_ok"] = ws1_err_ok
            # audit-only: the walk + the floor schedule vs the deposit
            rec["u0s1_trace_sha_ok"] = bool(
                trace_sha == rec290a1["trace_sha256"])
            rec["u0s1_floor_rec_ok"] = bool(
                rec["floor_rec"] == {k: float(v) for k, v in
                                     rec290a1["floor_rec"].items()})
            rec["u0s1_ncommits_ok"] = bool(
                n_commits == int(rec290a1["n_commits"]))
        else:  # U1-S1 — THE NEW CELL: the G2 integrity face is asserted
            # above (finite err, A3, trace length, commit count, the
            # register's replay equality); no deposit anchor applies.
            rec["new_cell"] = True
        return rec

    # ---- THE REBUILD (exp290's landed form VERBATIM: the sha-asserted
    #      rebuild against exp243's OWN records + the re-reads; shared by
    #      both passes — deterministic; PLUS the exp300 union anchor
    #      re-read + the MARKS' VALIDITY cross-check) ---------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_canon_ok": 0, "h0_echo_h1": False, "n_fmax_ok": 0,
                  "n_nonneg_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
                  "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
                  "n_medium_shas_ok": 0, "n_rows282": 0,
                  "n_282_chain_ok": 0, "n_rows287": 0, "n_rows288": 0,
                  "n_rows289_g1": 0, "n_rows290_a1": 0,
                  "n_rows300_u1": 0, "n_marks_ok": 0, "n_tpart_ok": 0}
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

        # exp256's 72 rows — the substituted records the U0-S0 anchor
        # reads, complete with the instance structure
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
                f"{r['host']} s{r['seed']}: the substituted structure " \
                "drifted"
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

        # THE EXP282 RE-READ (the walk anchor deposit)
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
                 "deposited substituted err")
            n_chain282 += int(ok_chain)
            r282[key] = r
        counts["n_282_chain_ok"] = n_chain282
        assert counts["n_282_chain_ok"] == 72, \
            "exp282's err chain anchor drifted"

        # THE EXP287 + EXP288 RE-READS (the commit-layer anchor
        # deposits; audit-only cross-checks for the U0-S0 cell)
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

        # THE EXP289 CHAIN RE-READ (the deposited best-dose face — the
        # union's own provenance chain; the deposited branch + dose
        # face asserted)
        assert dep289["branch"] == "HISTORY-CARRIED", \
            "exp289's deposited branch drifted from HISTORY-CARRIED"
        assert float(dep289["grid"]["best_grid_point"]) == G_COMPOSED, \
            "exp289's deposited best dose drifted from g=1.0"
        n289g1 = sum(1 for r in dep289["grid_rows"]
                     if float(r["g_ctx"]) == G_COMPOSED)
        counts["n_rows289_g1"] = n289g1
        assert counts["n_rows289_g1"] == 72, \
            "exp289's 72-row g=1.0 grid drifted"

        # THE EXP290 ANCHOR RE-READ (the deposited A1 rows — the U0-S1
        # anchor's source; the deposited branch asserted)
        assert dep290["branch"] == "STORAGE-SIDE", \
            "exp290's deposited branch drifted from STORAGE-SIDE"
        r290a1 = {}
        for r in dep290["rows"]:
            if r["arm"] != "A1":
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r290a1, f"duplicate exp290 A1 row {key}"
            assert all(fld in r for fld in
                       ("err", "trace_sha256", "floor_rec", "n_commits")), \
                f"{key}: exp290's A1 row record is missing anchors"
            r290a1[key] = r
        counts["n_rows290_a1"] = len(r290a1)
        assert counts["n_rows290_a1"] == 72, \
            "exp290's 72-row A1 battery drifted"

        # THE EXP300 ANCHOR RE-READ (the deposited union g=1.0 rows —
        # the U1-S0 anchor's source; the deposited branch + ladder
        # asserted)
        assert dep300["branch"] == "MONOTONE-TO-1.0", \
            "exp300's deposited branch drifted from MONOTONE-TO-1.0"
        r300u1 = {}
        for r in dep300["rows"]:
            if r["arm"] != "ctx|gj|apop" or float(r["g"]) != G_COMPOSED:
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r300u1, \
                f"duplicate exp300 union g=1.0 row {key}"
            assert all(fld in r for fld in
                       ("err", "trace_sha256", "walk_end_rms",
                        "n_arm_writes", "n_sigma_writes",
                        "n_blend_writes", "n_commits", "cvt_rms")) \
                and "phi_history_sha256" in r["register"], \
                f"{key}: exp300's union row record is missing anchors"
            r300u1[key] = r
        counts["n_rows300_u1"] = len(r300u1)
        assert counts["n_rows300_u1"] == 72, \
            "exp300's 72-row union g=1.0 battery drifted"

        # THE MARKS' VALIDITY (fail=STOP): the rebuilt q10/q90 +
        # target_part + bands reproduce exp300's deposited arm_inputs
        # BIT-EXACT — the union's armed-site plan is pinned to the
        # deposited one (the marks drive the apop face + the U1-S0
        # anchor's bit-exactness depends on them)
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
            (f"the rebuilt quantiles ({q10}, {q90}) drifted from exp300's "
             f"deposited arm_inputs ({ai300['q10']}, {ai300['q90']}) — "
             "the marks' validity FAILED")
        assert int(ai300["pooled_n"]) == int(pooled.size) == 9600, \
            "the pooled mark source drifted from exp300's"
        marks = {}
        for h in hosts:
            marks[h] = {}
            for inst in DEEP_INSTANCES:
                f = np.asarray(bases[h]["deep"][inst]["f"], dtype=float)
                lo, hi = bands[(h, inst)]
                mk = (f <= q10) | (f >= q90)
                mk[lo:hi + 1] = True          # the band clause (OR)
                marks[h][inst] = mk
                # the band faces vs exp300's deposited bands (audit
                # tally; the equality asserted per host below via the
                # bands dict)
                dep_band = ai300["bands"][f"{h}|i{inst}"]
                counts["n_marks_ok"] += int(
                    bool([int(lo), int(hi)] == [int(dep_band[0]),
                                                int(dep_band[1])]))
            counts["n_tpart_ok"] += int(
                target_part[h] == float(ai300["target_part"][h]))
        assert all(bool([int(bands[(h, i)][0]), int(bands[(h, i)][1])]
                        == [int(ai300["bands"][f"{h}|i{i}"][0]),
                            int(ai300["bands"][f"{h}|i{i}"][1])]
                        ) for h in hosts for i in DEEP_INSTANCES), \
            "the rebuilt amputation bands drifted from exp300's bands"
        assert counts["n_marks_ok"] == 24 and counts["n_tpart_ok"] == 12, \
            "the marks'/target_part's validity tally drifted"

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
                                       "n_chain_ok":
                                           counts["n_282_chain_ok"]},
                     "exp287_reread": {"n_rows": counts["n_rows287"]},
                     "exp288_reread": {"n_rows": counts["n_rows288"],
                                       "branch": dep288["branch"]},
                     "exp289_reread": {
                         "n_rows_g1": counts["n_rows289_g1"],
                         "branch": dep289["branch"],
                         "best_grid_point":
                             float(dep289["grid"]["best_grid_point"])},
                     "exp290_reread": {
                         "n_rows_a1": counts["n_rows290_a1"],
                         "branch": dep290["branch"]},
                     "exp300_reread": {
                         "n_rows_union_g1": counts["n_rows300_u1"],
                         "branch": dep300["branch"]},
                     "marks_validity": {
                         "q10": q10, "q90": q90,
                         "pooled_n": int(pooled.size),
                         "n_marks_ok": counts["n_marks_ok"],
                         "n_tpart_ok": counts["n_tpart_ok"]}}
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "r288": r288, "r290a1": r290a1,
                "r300u1": r300u1, "marks": marks, "bands": bands,
                "target_part": target_part, "integrity": integrity}

    # ---- ONE PASS (the cells of the pass: 144 decodes each; the
    #      sha-asserted rebuild first (deterministic), then the battery
    #      in the pre-named order, then the per-pass determinism canary
    #      (each cell's first row re-decoded bit-exactly; the canary's
    #      S* re-reads truncated from the log — the exp290 form)) -------
    def _compute_pass(tag):
        cells = PASS_CELLS[tag]
        _LOCK_LOG.clear()
        rb = _rebuild()
        bases = rb["bases"]
        rows_by_cell: dict = {}
        first_args: dict = {}
        for cell in cells:
            rows_out: list = []
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_cell_row(
                            cell, k, rk, ctx["deep"][inst]["spec"],
                            med, s, ctx["fmax"], ctx["A"],
                            rb["marks"][k][inst],
                            rb["dep_sub"][(k, s, rk)],
                            rb["r282"][(k, s, rk)],
                            rb["r287"][(k, s, rk)],
                            rb["r288"][(k, s, rk)],
                            rb["r300u1"][(k, s, rk)],
                            rb["r290a1"][(k, s, rk)],
                            rb["target_part"][k])
                        rows_out.append(rec)
                        if cell not in first_args:
                            first_args[cell] = (
                                k, rk, ctx["deep"][inst]["spec"], med, s,
                                ctx["fmax"], ctx["A"],
                                rb["marks"][k][inst],
                                rb["target_part"][k])
                hs = [r for r in rows_out if r["host"] == k]
                print(f"  [pass{tag} {cell} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | src "
                      f"{ {t: sum(r['src_census'][t] for r in hs) for t in COMMIT_SOURCES} }",
                      flush=True)
            assert len(rows_out) == 72, \
                f"the {cell} battery produced {len(rows_out)} rows != 72"
            rows_by_cell[cell] = rows_out
        assert len(_LOCK_LOG) == 72 * len(cells), \
            (f"the S* lock count {len(_LOCK_LOG)} != "
             f"{72 * len(cells)} reads")

        # ---- THE DETERMINISM CANARY (G4's evaluable determinism: each
        #      cell's first row re-decoded bit-exactly; the canary's S*
        #      re-reads truncated from the log — the counted reads are
        #      the battery's, disclosed) ---------------------------------
        canary = []
        for cell in cells:
            (k, rk, spec_o, med_o, s, fmax_o, abase_o, mk_o,
             tp_o) = first_args[cell]
            r1 = rows_by_cell[cell][0]
            assert (r1["host"], r1["row_key"], int(r1["seed"])) == \
                (k, rk, s), "the canary's first-row args drifted"
            mark = len(_LOCK_LOG)
            r2 = _decode_cell_row(
                cell, k, rk, spec_o, med_o, s, fmax_o, abase_o, mk_o,
                rb["dep_sub"][(k, s, rk)], rb["r282"][(k, s, rk)],
                rb["r287"][(k, s, rk)], rb["r288"][(k, s, rk)],
                rb["r300u1"][(k, s, rk)], rb["r290a1"][(k, s, rk)], tp_o)
            del _LOCK_LOG[mark:]
            same = bool(
                r2["err"] == r1["err"]
                and r2["err_exact"] == r1["err_exact"]
                and r2["trace_sha256"] == r1["trace_sha256"]
                and r2["commit_seq_sha256"] == r1["commit_seq_sha256"]
                and r2["walk_end_rms"] == r1["walk_end_rms"]
                and r2["walk_steps"] == r1["walk_steps"]
                and r2["floor_rec"] == r1["floor_rec"]
                and r2["src_census"] == r1["src_census"]
                and r2["register"] == r1["register"]
                and r2["n_arm_writes"] == r1["n_arm_writes"]
                and r2["n_sigma_writes"] == r1["n_sigma_writes"]
                and r2["n_blend_writes"] == r1["n_blend_writes"])
            assert same, \
                f"the determinism canary failed on {cell} {k} {rk} s{s}"
            canary.append({"cell": cell, "host": k, "seed": int(s),
                           "row_key": rk, "bit_identical": same})
        assert len(_LOCK_LOG) == 72 * len(cells), \
            "the S* lock count drifted after the canary truncation"

        return {"pass": int(tag), "cells": list(cells),
                "rows_by_cell": rows_by_cell,
                "integrity": rb["integrity"],
                "lock_reads": len(_LOCK_LOG), "canary": canary,
                "ro_before": ro_before,
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry}

    # ---- THE ASSEMBLY (a pure function of the two passes' payloads +
    #      the deposits; the merge NEVER re-decodes; the stream face +
    #      the plan face asserted across the cells here — the structural
    #      zero-knob asserts, fail=STOP) ---------------------------------
    def _assemble(p1, p2, run_form):
        assert p1["pass"] == 1 and p2["pass"] == 2, "payload swap"
        assert p1["cells"] == list(PASS_CELLS[1]) \
            and p2["cells"] == list(PASS_CELLS[2]), "the cell split drifted"
        ia = hashlib.sha256(json.dumps(
            p1["integrity"], sort_keys=True, default=float).encode()
        ).hexdigest()
        ib = hashlib.sha256(json.dumps(
            p2["integrity"], sort_keys=True, default=float).encode()
        ).hexdigest()
        assert ia == ib, \
            (f"the two passes' integrity sections diverged: {ia[:16]} vs "
             f"{ib[:16]} — the byte-identity check FAILED")
        assert p1["ro_before"] == p2["ro_before"] == ro_before, \
            "ro_before drifted across passes"
        assert p1["port_sha256"] == p2["port_sha256"] == _sha(PORT_FILE), \
            "the register's home (collective.py) drifted mid-run"
        assert p1["exp142_sha256"] == p2["exp142_sha256"] \
            == _sha(EXP142_FILE), \
            "exp142 was modified — the pre-registered NOT-modified rule"
        rows_by_cell = {}
        for tag, p in ((1, p1), (2, p2)):
            for cell in PASS_CELLS[tag]:
                rows = p["rows_by_cell"][cell]
                assert len(rows) == 72, \
                    f"the {cell} battery drifted in pass {tag}"
                rows_by_cell[cell] = rows
        E = {}
        for cell in CELLS:
            d = {}
            for r in rows_by_cell[cell]:
                key = (r["host"], int(r["seed"]), r["row_key"])
                assert key not in d, f"duplicate {cell} row {key}"
                d[key] = r
            E[cell] = d
        assert len(set(E["U0-S0"])) == 72, "the 72-row paired frame drifted"
        assert set(E["U0-S0"]) == set(E["U1-S0"]) == set(E["U0-S1"]) \
            == set(E["U1-S1"]), "the paired key frame drifted across cells"
        lock_total = int(p1["lock_reads"]) + int(p2["lock_reads"])
        assert lock_total == 288, \
            f"the S* lock count {lock_total} != 288 (4 cells x 72)"
        canary_all = list(p1["canary"]) + list(p2["canary"])
        assert len(canary_all) == 4 and \
            all(c["bit_identical"] for c in canary_all), \
            "the determinism canary drifted"

        # ---- THE STREAM FACE (zero knobs): the walk order + the commit
        #      count are g- and stress-independent — per row the
        #      commit-index digest + walk_steps + n_commits identical
        #      across ALL FOUR cells (the population path is
        #      stress-independent by construction, asserted) -----------
        n_stream_ok = 0
        for key in E["U0-S0"]:
            ok = bool(
                len({E[c][key]["commit_idx_sha256"] for c in CELLS}) == 1
                and len({E[c][key]["walk_steps"] for c in CELLS}) == 1
                and len({E[c][key]["n_commits"] for c in CELLS}) == 1)
            assert ok, \
                (f"{key}: the stream face drifted across the cells — the "
                 "walk order / commit count moved with a factor")
            n_stream_ok += int(ok)
        assert n_stream_ok == 72, "the stream face drifted"
        # ---- THE PLAN FACE: the union's armed-site plan is
        #      (target, A)-determined — the arm/sigma/blend write counts
        #      identical across the two U1 cells per row ---------------
        n_plan_ok = 0
        for key in E["U0-S0"]:
            ok = bool(
                E["U1-S0"][key]["n_arm_writes"]
                == E["U1-S1"][key]["n_arm_writes"]
                and E["U1-S0"][key]["n_sigma_writes"]
                == E["U1-S1"][key]["n_sigma_writes"]
                and E["U1-S0"][key]["n_blend_writes"]
                == E["U1-S1"][key]["n_blend_writes"])
            assert ok, \
                (f"{key}: the plan face drifted — the union's armed-site "
                 "plan moved with the stress")
            n_plan_ok += int(ok)
        assert n_plan_ok == 72, "the plan face drifted"
        # ---- the gj landed compensation asserts (exp300's G2 form,
        #      re-run per U1 row) ----------------------------------------
        n_gj_ok = int(sum(bool(E[c][k]["gj_assert_ok"])
                          for c in ("U1-S0", "U1-S1") for k in E[c]))
        assert n_gj_ok == 144, "the gj landed compensation assert drifted"

        # ---- THE PROTECTION READ (zero knobs, the pre-named 2x2
        #      interaction on the mean errs) -----------------------------
        cell_means = {c: float(np.mean(
            [r["err"] for r in rows_by_cell[c]])) for c in CELLS}
        stress_no_union = float(cell_means["U0-S1"] - cell_means["U0-S0"])
        stress_with_union = float(cell_means["U1-S1"] - cell_means["U1-S0"])
        union_no_stress = float(cell_means["U0-S0"] - cell_means["U1-S0"])
        union_under_stress = float(cell_means["U0-S1"]
                                   - cell_means["U1-S1"])
        P = float(union_under_stress - union_no_stress)
        assert np.isfinite(P), "non-finite composed protection delta"
        if P >= PROTECT_BAR:
            branch = "PROTECTED-PRESERVED"
        elif P <= -PROTECT_BAR:
            branch = "AMPLIFIED"
        else:
            branch = "ADDITIVE"
        per_host_P = {}
        for h in hosts:
            m = {c: float(np.mean([r["err"] for r in rows_by_cell[c]
                                   if r["host"] == h])) for c in CELLS}
            per_host_P[h] = {
                "cell_means": m,
                "P": float((m["U0-S1"] - m["U1-S1"])
                           - (m["U0-S0"] - m["U1-S0"]))}

        # ---- THE COMPOSITION'S PROTECTION COMPARISON (audit-only,
        #      never gating): the composed union's P vs exp293's
        #      deposited single-register P — does protection compose? --
        P_ctx = float(dep293["protection"]["P"])
        imp_ctx = float(dep293["protection"]
                        ["register_improvement_no_stress"])
        ratio_union = (float(P / union_no_stress)
                       if abs(union_no_stress) > 1e-12 else float("nan"))
        ratio_ctx = (float(P_ctx / imp_ctx)
                     if abs(imp_ctx) > 1e-12 else float("nan"))
        composition_comparison = {
            "P_union": P, "P_ctx_deposited": P_ctx,
            "protection_delta_composition": float(P - P_ctx),
            "union_rest_improvement": union_no_stress,
            "ctx_rest_improvement_deposited": imp_ctx,
            "ratio_union": ratio_union, "ratio_ctx_deposited": ratio_ctx,
            "note": ("audit-only, never gating: P_union vs exp293's "
                     "deposited P_ctx (the composition's protection "
                     "comparison) + the ratio face (the protection / "
                     "the rest improvement — exp293's landed ~29x form)")}

        # ---- the per-cell summaries (the zero-knob tallies) ------------
        tallies = {}
        for cell in CELLS:
            rows = rows_by_cell[cell]
            errs = [float(r["err"]) for r in rows]
            tallies[cell] = {
                "cell": cell, "arm": CELL_ARM[cell],
                "g_u": float(CELL_G[cell]), "name": CELL_NAMES[cell],
                "n_rows": 72,
                "n_finite_err": int(sum(np.isfinite(e) for e in errs)),
                "mean_err": float(np.mean(errs)),
                "worst_err": float(max(errs)),
                "err_bar": float(ERR_BAR),
                "n_rows_over_bar": int(sum(e >= ERR_BAR for e in errs)),
                "n_verified": int(sum(bool(r["verified"])
                                      for r in rows)),
                "n_a3_ok": int(sum(r["a3_ok"] for r in rows)),
                "n_trace_len_ok": int(sum(r["trace_len_ok"]
                                          for r in rows)),
                "n_commits_count_ok": int(sum(r["commits_count_ok"]
                                              for r in rows)),
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
                "mean_cvt_rms": float(np.mean(
                    [r["cvt_rms"] for r in rows])),
                "n_register_replay_ok": int(sum(r["register"]["replay_ok"]
                                                for r in rows)),
                "mean_n_arm_writes": float(np.mean(
                    [r["n_arm_writes"] for r in rows])),
                "mean_n_sigma_writes": float(np.mean(
                    [r["n_sigma_writes"] for r in rows])),
                "mean_n_blend_writes": float(np.mean(
                    [r["n_blend_writes"] for r in rows]))}

        # ---- the tallies per gate ---------------------------------------
        n_s0_err = int(sum(bool(E["U0-S0"][k].get("s0_err_ok"))
                           for k in E["U0-S0"]))
        n_s0_ver = int(sum(bool(E["U0-S0"][k].get("s0_verified_ok"))
                           for k in E["U0-S0"]))
        n_we282 = int(sum(bool(E["U0-S0"][k].get("walk_end_282_ok"))
                          for k in E["U0-S0"]))
        n_ts282 = int(sum(bool(E["U0-S0"][k].get("trace_sha_282_ok"))
                          for k in E["U0-S0"]))
        n_ee282 = int(sum(bool(E["U0-S0"][k].get("err_exact_282_ok"))
                          for k in E["U0-S0"]))
        n_u1s0_err = int(sum(bool(E["U1-S0"][k].get("u1s0_err_ok"))
                             for k in E["U1-S0"]))
        n_u1s0_ts = int(sum(bool(E["U1-S0"][k].get("u1s0_trace_sha_ok"))
                            for k in E["U1-S0"]))
        n_u0s1_err = int(sum(bool(E["U0-S1"][k].get("u0s1_err_ok"))
                             for k in E["U0-S1"]))
        # the floor facets (the pre-named G1 counts)
        s1_cells = ("U0-S1", "U1-S1")
        s0_cells = ("U0-S0", "U1-S0")
        n_floor_walk_s1 = int(sum(
            E[c][k]["floor_rec"]["walk_first_commit"] == READER_PIN_FLOOR
            and E[c][k]["floor_rec"]["walk_last_commit"]
            == READER_PIN_FLOOR
            for c in s1_cells for k in E[c]))
        n_floor_encode_s0 = int(sum(
            E[c][k]["floor_rec"]["encode_start"] == PROD_FLOOR
            for c in s0_cells for k in E[c]))
        n_floor_encode_s1 = int(sum(
            E[c][k]["floor_rec"]["encode_start"] == READER_PIN_FLOOR
            for c in s1_cells for k in E[c]))
        n_floor_settle_decode = int(sum(
            E[c][k]["floor_rec"]["settle_start"] == PROD_FLOOR
            and E[c][k]["floor_rec"]["decode_start"] == PROD_FLOOR
            for c in CELLS for k in E[c]))
        # the audit-only cross-deposit faces
        n_a0_sha287 = int(sum(bool(E["U0-S0"][k].get("commit_sha_287_ok"))
                              for k in E["U0-S0"]))
        n_a0_sha288 = int(sum(bool(E["U0-S0"][k].get("commit_sha_288_ok"))
                              for k in E["U0-S0"]))
        n_a0_cvt287 = int(sum(bool(E["U0-S0"][k].get("cvt_287_ok"))
                              for k in E["U0-S0"]))
        n_u0s1_ts = int(sum(bool(E["U0-S1"][k].get("u0s1_trace_sha_ok"))
                            for k in E["U0-S1"]))
        n_u0s1_fr = int(sum(bool(E["U0-S1"][k].get("u0s1_floor_rec_ok"))
                            for k in E["U0-S1"]))
        n_u1s0_we = int(sum(bool(E["U1-S0"][k].get("u1s0_walk_end_ok"))
                            for k in E["U1-S0"]))
        n_u1s0_rg = int(sum(bool(E["U1-S0"][k].get("u1s0_reg_sha_ok"))
                            for k in E["U1-S0"]))
        n_u1s0_narm = int(sum(bool(E["U1-S0"][k].get("u1s0_narm_ok"))
                              for k in E["U1-S0"]))
        n_u1s0_nsigma = int(sum(bool(E["U1-S0"][k].get("u1s0_nsigma_ok"))
                                for k in E["U1-S0"]))
        n_u1s0_nblend = int(sum(bool(E["U1-S0"][k].get("u1s0_nblend_ok"))
                                for k in E["U1-S0"]))
        n_u1s0_cvt = int(sum(bool(E["U1-S0"][k].get("u1s0_cvt_ok"))
                             for k in E["U1-S0"]))
        n_u1s1_replay = int(sum(E["U1-S1"][k]["register"]["replay_ok"]
                                for k in E["U1-S1"]))
        n_u1s1_fin = int(sum(np.isfinite(E["U1-S1"][k]["err"])
                             for k in E["U1-S1"]))
        n_u1s1_a3 = int(sum(E["U1-S1"][k]["a3_ok"] for k in E["U1-S1"]))
        n_u1s1_tl = int(sum(E["U1-S1"][k]["trace_len_ok"]
                            for k in E["U1-S1"]))
        n_u1s1_cc = int(sum(E["U1-S1"][k]["commits_count_ok"]
                            for k in E["U1-S1"]))

        g1 = dict(p1["integrity"]["counts"])
        g1.update({
            "n_u0s0_err_ok": n_s0_err, "n_u0s0_verified_ok": n_s0_ver,
            "n_walk282_ok": n_we282, "n_trace282_ok": n_ts282,
            "n_errexact282_ok": n_ee282,
            "n_u1s0_err_ok": n_u1s0_err, "n_u1s0_trace_sha_ok": n_u1s0_ts,
            "n_u0s1_err_ok": n_u0s1_err,
            "n_floor_walk_s1_ok": n_floor_walk_s1,
            "n_floor_encode_s0_ok": n_floor_encode_s0,
            "n_floor_encode_s1_audit": n_floor_encode_s1,
            "n_floor_settle_decode_ok": n_floor_settle_decode,
            "n_a0_commit_sha_287_audit": n_a0_sha287,
            "n_a0_commit_sha_288_audit": n_a0_sha288,
            "n_a0_cvt_287_audit": n_a0_cvt287,
            "n_u0s1_trace_sha_audit": n_u0s1_ts,
            "n_u0s1_floor_rec_audit": n_u0s1_fr,
            "n_u1s0_walk_end_audit": n_u1s0_we,
            "n_u1s0_reg_sha_audit": n_u1s0_rg,
            "n_u1s0_narm_audit": n_u1s0_narm,
            "n_u1s0_nsigma_audit": n_u1s0_nsigma,
            "n_u1s0_nblend_audit": n_u1s0_nblend,
            "n_u1s0_cvt_audit": n_u1s0_cvt})
        g2 = {"n_rows": 72, "n_finite_err": n_u1s1_fin,
              "n_a3_ok": n_u1s1_a3, "n_trace_len_ok": n_u1s1_tl,
              "n_commits_count_ok": n_u1s1_cc,
              "n_register_replay_ok": n_u1s1_replay,
              "n_stream_ok_rows": n_stream_ok,
              "n_plan_ok": n_plan_ok,
              "n_gj_assert_ok": n_gj_ok,
              "n_lock_reads": lock_total}
        g3 = {"branch": branch, "bar": PROTECT_BAR, "P": P,
              "cell_means": cell_means,
              "stress_degradation_no_union": stress_no_union,
              "stress_degradation_with_union": stress_with_union,
              "union_improvement_no_stress": union_no_stress,
              "union_improvement_under_stress": union_under_stress,
              "composition_comparison": composition_comparison,
              "n_rows": 72,
              "per_host_P_finite": bool(all(
                  np.isfinite(per_host_P[h]["P"]) for h in hosts))}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": p1["integrity"],
                "rows": [r for c in CELLS for r in rows_by_cell[c]],
                "per_cell": tallies,
                "protection": {
                    "form": ("P_union = [mean_err(U0-S1) - mean_err(U1-S1)"
                             "] - [mean_err(U0-S0) - mean_err(U1-S0)]"),
                    "bar": PROTECT_BAR, "P": P,
                    "cell_means": cell_means,
                    "stress_degradation_no_union": stress_no_union,
                    "stress_degradation_with_union": stress_with_union,
                    "union_improvement_no_stress": union_no_stress,
                    "union_improvement_under_stress": union_under_stress,
                    "per_host_P": per_host_P,
                    "outliers_H3_H5": {h: per_host_P[h]
                                       for h in outliers},
                    "composition_comparison": composition_comparison},
                "stream_face": {"n_stream_ok_rows": n_stream_ok,
                                "n_plan_ok": n_plan_ok,
                                "n_gj_assert_ok": n_gj_ok},
                "branch": branch,
                "branch_discriminant": {
                    "bar": PROTECT_BAR,
                    "bar_pre_named_at": ("26e15a1 — fixed at "
                                         "pre-registration, never fit"),
                    "form": ("PROTECTED-PRESERVED iff P_union >= 0.05; "
                             "AMPLIFIED iff P_union <= -0.05; else "
                             "ADDITIVE (the honest null: the two effects "
                             "independent at the machinery's resolution)"),
                    "resolved": branch},
                "g1": g1, "g2": g2, "g3": g3,
                "canary": canary_all,
                "lock_reads": lock_total,
                "run_form": run_form,
                "integrity_shas": {"pass1": ia, "pass2": ib}}

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True, default=float).encode()
        ).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the CHECKPOINT-
    #      SPLIT EXP302_MODE=pass1 (the S0 cells, 144 decodes) | pass2
    #      (the S1 cells, 144 decodes) | merge — each pass a separate
    #      process, the merge assembling + evaluating the gates once and
    #      NEVER re-decoding; the in-process default for the GitHub
    #      runners. Both forms evaluate the SAME gates.) ------------------
    _MODE = os.environ.get("EXP302_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp302_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp302_pass2.checkpoint.json")}
    PASS_CELLS = {1: ("U0-S0", "U1-S0"), 2: ("U0-S1", "U1-S1")}

    def _run_test_suite():
        cmd = [sys.executable, "-m", "tests.run_tests"]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                              text=True, timeout=560)
        tail = "\n".join(proc.stdout.strip().splitlines()[-4:])
        green = bool(proc.returncode == 0)
        return {"green": green, "returncode": int(proc.returncode),
                "tail": tail}

    def _exit_checks():
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
            "the register's home (collective.py) drifted after the work"
        assert _sha(EXP142_FILE) == exp142_sha_entry, \
            "exp142 was modified after the work"

    if _MODE in ("pass1", "pass2"):
        tag = 1 if _MODE == "pass1" else 2
        print(f"=== exp302 pass{tag}: the "
              f"{'S0' if tag == 1 else 'S1'} cells "
              f"({list(PASS_CELLS[tag])}, 144 decodes) ===")
        payload = _compute_pass(tag)
        ck = _CK[tag]
        assert not os.path.exists(ck), \
            (f"{ck} already holds a payload — the split form caches "
             "exactly one payload per pass")
        with open(ck, "w") as fh:
            json.dump(payload, fh, sort_keys=True, default=float)
        print(f"  checkpointed {_MODE} (sha {_payload_sha(payload)[:16]})")
        _exit_checks()
        set_floor(PROD_FLOOR)
        assert read_floor() == PROD_FLOOR, "floor drift at exit"
        return {"mode": _MODE, "payload_sha256": _payload_sha(payload)}

    if _MODE == "merge":
        cached = {}
        for tag in (1, 2):
            with open(_CK[tag]) as fh:
                cached[tag] = json.load(fh)
        core = _assemble(cached[1], cached[2],
                         "checkpoint-split pass1|pass2 + merge")
        run_form = "checkpoint-split pass1|pass2 + merge"
        sa = _payload_sha(cached[1])
        sb = _payload_sha(cached[2])
    else:
        print("=== exp302: THE COMPOSED STRESS FACE (is the ~29x "
              "protection preserved under composition?) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows x 4 cells = 288 decodes "
              f"at the production budget {BUDGET} (== exp142's "
              f"STEPS_PER_CELL)")
        print(f"  the cells: U0-S0 the exp256 anchor | U1-S0 exp300's "
              f"union g=1.0 anchor | U0-S1 exp290's A1 arm verbatim | "
              f"U1-S1 THE NEW CELL | the branch bar: PROTECT_BAR "
              f"{PROTECT_BAR} mV")
        p1 = _compute_pass(1)
        p2 = _compute_pass(2)
        sa = _payload_sha(p1)
        sb = _payload_sha(p2)
        core = _assemble(p1, p2, "in-process default (one invocation)")
        run_form = "in-process default (one invocation)"
    del sa, sb

    # ---- the gate assembly (evaluated exactly once) ---------------------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    tallies = core["per_cell"]
    prot = core["protection"]
    branch = core["branch"]
    P = prot["P"]
    comp_cmp = prot["composition_comparison"]
    canary_bit_identical = bool(
        all(c["bit_identical"] for c in core["canary"]))
    ro_unchanged = bool(
        set(_sha(p) for p in READ_DEPS) == set(ro_before.values())
        and True)
    g1_pass = bool(
        g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
        and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
        and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
        and g1["n_rows256"] == 72 and g1["n_structure_ok"] == 36
        and g1["n_worst_eq_max"] == 36
        and g1["n_deep_targets_ok"] == 72 and g1["n_medium_shas_ok"] == 72
        and g1["n_rows282"] == 72 and g1["n_282_chain_ok"] == 72
        and g1["n_rows287"] == 72 and g1["n_rows288"] == 72
        and g1["n_rows289_g1"] == 72 and g1["n_rows290_a1"] == 72
        and g1["n_rows300_u1"] == 72
        and g1["n_marks_ok"] == 24 and g1["n_tpart_ok"] == 12
        and g1["n_u0s0_err_ok"] == 72 and g1["n_u0s0_verified_ok"] == 72
        and g1["n_walk282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72
        and g1["n_u1s0_err_ok"] == 72 and g1["n_u1s0_trace_sha_ok"] == 72
        and g1["n_u0s1_err_ok"] == 72
        and g1["n_floor_walk_s1_ok"] == 144
        and g1["n_floor_encode_s0_ok"] == 144
        and g1["n_floor_settle_decode_ok"] == 288
        and ro_unchanged)
    g2_pass = bool(
        g2["n_rows"] == 72 and g2["n_finite_err"] == 72
        and g2["n_a3_ok"] == 72 and g2["n_trace_len_ok"] == 72
        and g2["n_commits_count_ok"] == 72
        and g2["n_register_replay_ok"] == 72
        and g2["n_stream_ok_rows"] == 72 and g2["n_plan_ok"] == 72
        and g2["n_gj_assert_ok"] == 144
        and g2["n_lock_reads"] == 288)
    g3_pass = bool(
        g3["branch"] in ("PROTECTED-PRESERVED", "AMPLIFIED", "ADDITIVE")
        and g3["n_rows"] == 72 and np.isfinite(g3["P"])
        and g3["bar"] == PROTECT_BAR
        and g3["per_host_P_finite"])

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

    if branch == "PROTECTED-PRESERVED":
        branch_text = (
            "the composed union PROTECTS — protection is preserved "
            "under composition: the write-time stress hurts less when "
            "the union is carried by the pre-named margin (the "
            "memory-protection face survives the composition with the "
            "strongest carrier the stack has)")
    elif branch == "AMPLIFIED":
        branch_text = (
            "the composed union AMPLIFIES the stress harm — the "
            "write-time degradation is LARGER under the union by the "
            "pre-named margin (the composition is anti-protective)")
    else:
        branch_text = (
            "ADDITIVE — the stress degradation is additive and the "
            "union's improvement independent at the machinery's "
            "resolution (the honest null: P within the pre-named "
            "±0.05 mV bar)")
    verdict_body = (
        f"{branch} — {branch_text} "
        f"(the composed protection read: P_union {P:+.4f} mV vs the "
        f"pre-named PROTECT_BAR {PROTECT_BAR} mV"
        f" | the cell means: U0-S0 {prot['cell_means']['U0-S0']:.4f} / "
        f"U1-S0 {prot['cell_means']['U1-S0']:.4f} / "
        f"U0-S1 {prot['cell_means']['U0-S1']:.4f} / "
        f"U1-S1 {prot['cell_means']['U1-S1']:.4f}"
        f" | the stress deltas: without the union "
        f"{prot['stress_degradation_no_union']:+.4f} mV, with the union "
        f"{prot['stress_degradation_with_union']:+.4f} mV | the union "
        f"improvements: without stress "
        f"{prot['union_improvement_no_stress']:+.4f} mV, under stress "
        f"{prot['union_improvement_under_stress']:+.4f} mV"
        f" | the composition's protection comparison (AUDIT-ONLY): "
        f"P_union {comp_cmp['P_union']:+.4f} vs exp293's deposited "
        f"P_ctx {comp_cmp['P_ctx_deposited']:+.4f} (the delta "
        f"{comp_cmp['protection_delta_composition']:+.4f} mV); the "
        f"ratio face: the union {comp_cmp['ratio_union']:.2f}x vs the "
        f"ctx register's deposited {comp_cmp['ratio_ctx_deposited']:.2f}x"
        f" | the per-host P within "
        f"[{min(v['P'] for v in prot['per_host_P'].values()):.3f}, "
        f"{max(v['P'] for v in prot['per_host_P'].values()):.3f}], the "
        f"outliers H3/H5: P(H3) {prot['outliers_H3_H5']['H3']['P']:+.4f} "
        f"/ P(H5) {prot['outliers_H3_H5']['H5']['P']:+.4f} (audit-only)"
        f" | the worst-err per cell vs the 6.0 bar (audit-only, "
        f"unchanged): U0-S0 {tallies['U0-S0']['worst_err']:.2f} "
        f"({tallies['U0-S0']['n_rows_over_bar']}/72 over) / U1-S0 "
        f"{tallies['U1-S0']['worst_err']:.2f} "
        f"({tallies['U1-S0']['n_rows_over_bar']}/72 over) / U0-S1 "
        f"{tallies['U0-S1']['worst_err']:.2f} "
        f"({tallies['U0-S1']['n_rows_over_bar']}/72 over) / U1-S1 "
        f"{tallies['U1-S1']['worst_err']:.2f} "
        f"({tallies['U1-S1']['n_rows_over_bar']}/72 over)"
        f" | the commit src censuses per cell (audit-only, the floor's "
        f"effect on the (e) branch): U0-S0 spec "
        f"{tallies['U0-S0']['src_census']['spec']} / canon "
        f"{tallies['U0-S0']['src_census']['canon']} / parent "
        f"{tallies['U0-S0']['src_census']['parent']}; U1-S0 spec "
        f"{tallies['U1-S0']['src_census']['spec']} / canon "
        f"{tallies['U1-S0']['src_census']['canon']} / parent "
        f"{tallies['U1-S0']['src_census']['parent']}; U0-S1 spec "
        f"{tallies['U0-S1']['src_census']['spec']} / canon "
        f"{tallies['U0-S1']['src_census']['canon']} / parent "
        f"{tallies['U0-S1']['src_census']['parent']}; U1-S1 spec "
        f"{tallies['U1-S1']['src_census']['spec']} / canon "
        f"{tallies['U1-S1']['src_census']['canon']} / parent "
        f"{tallies['U1-S1']['src_census']['parent']}"
        f" | THE ANCHORS (bit-exact): U0-S0 == exp256's deposited errs "
        f"{g1['n_u0s0_err_ok']}/72 (the verified flags "
        f"{g1['n_u0s0_verified_ok']}/72, exp282's walk anchors "
        f"{g1['n_walk282_ok']}/72 + trace shas {g1['n_trace282_ok']}/72 "
        f"+ err_exact {g1['n_errexact282_ok']}/72; the commit-layer "
        f"digests vs exp287/288 audit-only "
        f"{g1['n_a0_commit_sha_287_audit']}/72 + "
        f"{g1['n_a0_commit_sha_288_audit']}/72); U1-S0 == exp300's "
        f"deposited union g=1.0 errs {g1['n_u1s0_err_ok']}/72 + trace "
        f"shas {g1['n_u1s0_trace_sha_ok']}/72 (the walk-end/"
        f"register-digest/write-count faces audit-only "
        f"{g1['n_u1s0_walk_end_audit']}/72 + "
        f"{g1['n_u1s0_reg_sha_audit']}/72 + "
        f"{g1['n_u1s0_narm_audit']}/72 + "
        f"{g1['n_u1s0_nsigma_audit']}/72 + "
        f"{g1['n_u1s0_nblend_audit']}/72 + "
        f"{g1['n_u1s0_cvt_audit']}/72); U0-S1 == exp290's deposited A1 "
        f"errs {g1['n_u0s1_err_ok']}/72 (the fresh A1 trace shas match "
        f"the deposit {g1['n_u0s1_trace_sha_audit']}/72 and the floor "
        f"schedule {g1['n_u0s1_floor_rec_audit']}/72, audit-only)"
        f" | THE MARKS' VALIDITY: the rebuilt q10/q90 + target_part + "
        f"bands reproduce exp300's deposited arm_inputs (the marks "
        f"{g1['n_marks_ok']}/24, the target parts {g1['n_tpart_ok']}/12)"
        f" | THE FLOOR ASSERTS: the -35.0 pin during the walk in the S1 "
        f"cells {g1['n_floor_walk_s1_ok']}/144, the -60.0 encode in the "
        f"S0 cells {g1['n_floor_encode_s0_ok']}/144 (the S1 encode at "
        f"the pin {g1['n_floor_encode_s1_audit']}/144, exp290's A1 "
        f"schedule), the -60.0 settle/decode everywhere "
        f"{g1['n_floor_settle_decode_ok']}/288"
        f" | THE NEW CELL (U1-S1, G2): finite errs "
        f"{g2['n_finite_err']}/72, the A3 convention "
        f"{g2['n_a3_ok']}/72, the trace lengths {g2['n_trace_len_ok']}"
        f"/72, the commit counts {g2['n_commits_count_ok']}/72, the "
        f"register's replay equality {g2['n_register_replay_ok']}/72 "
        f"(the population path is stress-independent: the stream face "
        f"{g2['n_stream_ok_rows']}/72 + the plan face "
        f"{g2['n_plan_ok']}/72 + the gj landed asserts "
        f"{g2['n_gj_assert_ok']}/144); the S* lock reads "
        f"{g2['n_lock_reads']}/288"
        f" | 12 hosts, the deterministic sha-asserted rebuild "
        f"(graph_path for H0/H1, small_world at the deposited rewire "
        f"seeds), 11 deposits READ-ONLY byte-unchanged, exp142 + the "
        f"core NOT modified ({run_form}), floor -60.0")

    # ---- the discipline scans + the deposit form -------------------------
    no_wall_clock = bool(not _scan_wall_clock_keys(core))
    deposit = {
        "exp": "exp302_composed_stress_face",
        "claim": (
            "THE COMPOSED STRESS FACE (batch 56, pre-registration "
            "commit 26e15a1): IS THE ~29x PROTECTION PRESERVED UNDER "
            "COMPOSITION? exp293 landed PROTECTED (the ctx register's "
            "2x2 interaction P = +0.73 mV, ~29x the rest improvement); "
            "exp300 landed MONOTONE-TO-1.0 (the composed carrier's "
            "optimum IS the saturated face g=1.0 of the union "
            "faces=(ctx, gj, apop)); exp301 landed WRITE-SIDE-CARRIED. "
            "The 2x2 factorial composes exp300's landed union coupling "
            "+ exp290's landed stress-pin schedule VERBATIM over "
            "exp256's 72-row substituted battery: U0-S0 union OFF "
            "floor -60.0 (== exp256's errs bit-exact), U1-S0 union ON "
            "at g=1.0 (== exp300's deposited union rows bit-exact), "
            "U0-S1 the write-time pin (== exp290's A1 errs bit-exact), "
            "U1-S1 union ON + the write-time pin (THE NEW CELL). THE "
            "COMPOSED PROTECTION READ (zero knobs): P_union = "
            "[mean_err(U0-S1) - mean_err(U1-S1)] - [mean_err(U0-S0) - "
            "mean_err(U1-S0)]; PROTECTED-PRESERVED iff P_union >= 0.05, "
            "AMPLIFIED iff P_union <= -0.05, else ADDITIVE (the honest "
            "null). The audit face (never gating): P_union vs exp293's "
            "deposited P_ctx — does protection COMPOSE like the "
            "improvement did? The null: the stress degradation is "
            "additive under the union too and the composed interaction "
            "== the single register's."),
        "method": {
            "battery": ("12 hosts x 3 seeds (1, 2, 3) x 2 deep "
                        "instances (r-60i0, r-60i1) at n=400 — exp256's "
                        "72-row substituted battery"),
            "cells": {c: {"g": CELL_G[c], "arm": CELL_ARM[c],
                          "faces": (list(FACES_UNION)
                                    if CELL_G[c] > 0.0 else []),
                          "name": CELL_NAMES[c]} for c in CELLS},
            "walk": ("exp300's landed union coupling VERBATIM (the "
                     "sigma face first at the marked cells, then the "
                     "ctx/gj blends applied once) + exp290's landed "
                     "A1 write-time -35.0 pin schedule (encode start "
                     "through the last commit, restored before the "
                     "settle); the module attributes set around the "
                     "calls — exp142 + the core NOT modified"),
            "budget": BUDGET, "protection_bar": PROTECT_BAR,
            "run_form": run_form},
        "inputs": {"hosts": hosts, "outliers": outliers,
                   "cluster": cluster,
                   "seeds": list(SEEDS_RUN),
                   "deep_instances": list(DEEP_INSTANCES),
                   "deep_rung": DEEP_RUNG,
                   "faces_union": list(FACES_UNION),
                   "g_composed": G_COMPOSED,
                   "marks_validity": integrity["marks_validity"]},
        "integrity": integrity,
        "rows": core["rows"],
        "per_cell": tallies,
        "protection": prot,
        "stream_face": core["stream_face"],
        "branch": branch,
        "branch_discriminant": core["branch_discriminant"],
        "g1": g1, "g2": g2, "g3": g3,
        "canary": core["canary"],
        "lock_reads": core["lock_reads"],
        "run_form": run_form,
        "integrity_shas": core["integrity_shas"]}
    gates = {
        "G1_the_anchors_floors_and_marks": {
            "pass": g1_pass,
            "counts": g1,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "anchor_definition": (
                "U0-S0's errs reproduce exp256's deposited substituted "
                "errs bit-exact (72/72, the verified flags 72/72) AND "
                "exp282's walk_end_rms bit-exact (walk_end + trace "
                "sha256 + err_exact 72/72 — the SAME walk exp282 "
                "deposited; the commit-layer digests vs exp287/exp288 "
                "recorded audit-only); U1-S0's errs + trace shas "
                "reproduce exp300's deposited union g=1.0 rows "
                "bit-exact (72/72; the walk-end/register-digest/"
                "write-count faces audit-only); U0-S1's errs reproduce "
                "exp290's deposited A1 errs bit-exact (72/72, the "
                "fresh trace shas + floor schedules matching the "
                "deposit audit-only); the MARKS' VALIDITY: the rebuilt "
                "q10/q90 + target_part + bands reproduce exp300's "
                "deposited arm_inputs (fail=STOP at the rebuild); the "
                "floor asserts: the -35.0 pin during the walk in the "
                "S1 cells 144/144, the -60.0 encode in the S0 cells "
                "144/144, the -60.0 settle/decode everywhere 288/288 "
                "— recorded per row, asserted fail=STOP")},
        "G2_new_cell_integrity": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "the U1-S1 cell (the union ON at g=1.0 + the "
                "write-time -35.0 pin during the walk only), 72 rows, "
                "fail=STOP per row: the errs finite; the A3 convention "
                "round(err_exact, 2) == the reported err; the trace "
                "lengths == walk_steps; the commit counts == "
                "walk_steps; the register's replay equality (exp289's "
                "G2 form — the register IS the commit sequence stored "
                "incrementally, under stress too); the population "
                "path's stress-independence asserted (the stream face: "
                "the commit-index digests + walk_steps + n_commits "
                "identical across ALL FOUR cells 72/72; the plan face: "
                "the union's armed-site counts n_arm_writes + "
                "n_sigma_writes + n_blend_writes identical across the "
                "two U1 cells 72/72; the gj landed compensation "
                "asserts 144/144); the S* lock reads 288 (4 cells x "
                "72 — the canary re-reads truncated, disclosed)")},
        "G3_protection_branch": {
            "pass": g3_pass,
            "bars": (
                "P_union = [mean_err(U0-S1) - mean_err(U1-S1)] - "
                "[mean_err(U0-S0) - mean_err(U1-S0)] vs the pre-named "
                "PROTECT_BAR 0.05 mV: PROTECTED-PRESERVED iff "
                "P_union >= 0.05; AMPLIFIED iff P_union <= -0.05; else "
                "ADDITIVE (the honest null). Audit-only, never gating: "
                "the composition's protection comparison (P_union vs "
                "exp293's deposited P_ctx), the ratio face (the "
                "protection / the rest improvement vs exp293's ~29x), "
                "the per-host P (the outliers H3/H5 disclosed), the "
                "worst-err per cell vs the 6.0 bar (unchanged), the "
                "commit src censuses per cell (the floor's effect on "
                "the (e) branch, exp290's disclosed form)"),
            "resolved": {"branch": branch, "P": P,
                         "cell_means": prot["cell_means"],
                         "per_host_P": prot["per_host_P"],
                         "outliers_H3_H5": prot["outliers_H3_H5"],
                         "composition_comparison": comp_cmp}},
        "G4_discipline": {
            "pass": None}}   # filled after the floor-exit assert
    n_pass = 0
    n_refute = 0
    for name in ("G1_the_anchors_floors_and_marks",
                 "G2_new_cell_integrity", "G3_protection_branch"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    # ---- the floor restore + the exit asserts (G4: NEURAL_SPEC_MIN ==
    #      -60.0 asserted at exit; the docstring + header re-checked) ----
    set_floor(PROD_FLOOR)
    floor_exit = read_floor()
    assert floor_exit == PROD_FLOOR, "floor drift at exit"
    _exit_checks()
    suite = _run_test_suite()
    gates["G4_discipline"] = {
        "pass": bool(canary_bit_identical
                     and no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged and floor_exit == PROD_FLOOR
                     and suite["green"]),
        "determinism_canary_bit_identical": canary_bit_identical,
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_26e15a1": docstring_ok,
        "header_byte_unchanged_vs_26e15a1": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "n_source_deposits": len(READ_DEPS),
        "exp142_not_modified": True,
        "core_not_modified": True,
        "exp142_sha256": exp142_sha_entry,
        "core_sha256": port_sha_entry,
        "floor_at_entry": floor_at_entry,
        "floor_at_exit": floor_exit,
        "floor_at_exit_per_module": {
            m.__name__: float(getattr(m, "NEURAL_SPEC_MIN", None))
            for m in PINNED},
        "reader_pin_floor_disclosed": READER_PIN_FLOOR,
        "docstring_sha256": docstring_sha,
        "header_sha256": header_sha,
        "test_suite": suite,
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

    print(f"\n  G1 the anchors + the floor asserts + the marks + the "
          f"deposits: {'PASS' if g1_pass else 'FAIL'} "
          f"(the 12 bases rebuilt sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the canon "
          f"identity {g1['n_canon_ok']}/12 + H0 == H1 + f_max "
          f"{g1['n_fmax_ok']}/12; THE ANCHORS — U0-S0 == exp256's errs "
          f"bit-exact {g1['n_u0s0_err_ok']}/72 (the verified flags "
          f"{g1['n_u0s0_verified_ok']}/72, exp282's walks "
          f"{g1['n_walk282_ok']}/72 + trace shas {g1['n_trace282_ok']}"
          f"/72), U1-S0 == exp300's union errs + trace shas "
          f"{g1['n_u1s0_err_ok']}/72 + {g1['n_u1s0_trace_sha_ok']}/72, "
          f"U0-S1 == exp290's A1 errs {g1['n_u0s1_err_ok']}/72; the "
          f"MARKS {g1['n_marks_ok']}/24 + {g1['n_tpart_ok']}/12; the "
          f"floor: the S1 walk pin {g1['n_floor_walk_s1_ok']}/144, the "
          f"S0 encode -60.0 {g1['n_floor_encode_s0_ok']}/144, the "
          f"settle/decode -60.0 {g1['n_floor_settle_decode_ok']}/288; "
          f"11 deposits READ-ONLY byte-unchanged: {ro_unchanged})")
    print(f"  G2 the new cell's integrity (U1-S1): "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(finite errs {g2['n_finite_err']}/72, A3 {g2['n_a3_ok']}/72, "
          f"trace lengths {g2['n_trace_len_ok']}/72, commit counts "
          f"{g2['n_commits_count_ok']}/72, the register's replay "
          f"equality {g2['n_register_replay_ok']}/72, the stream face "
          f"{g2['n_stream_ok_rows']}/72, the plan face "
          f"{g2['n_plan_ok']}/72, the gj asserts "
          f"{g2['n_gj_assert_ok']}/144; the S* lock reads "
          f"{g2['n_lock_reads']}/288)")
    print("  G3 the composed protection read (P_union = the 2x2 "
          "interaction; the pre-named PROTECT_BAR 0.05 mV):")
    cm = prot["cell_means"]
    print(f"      cell means: U0-S0 {cm['U0-S0']:.4f} | U1-S0 "
          f"{cm['U1-S0']:.4f} | U0-S1 {cm['U0-S1']:.4f} | U1-S1 "
          f"{cm['U1-S1']:.4f}")
    print(f"      P_union {prot['P']:+.4f} mV | stress without the union "
          f"{prot['stress_degradation_no_union']:+.4f} | stress with "
          f"the union {prot['stress_degradation_with_union']:+.4f}"
          f" | union without stress "
          f"{prot['union_improvement_no_stress']:+.4f} | union under "
          f"stress {prot['union_improvement_under_stress']:+.4f}")
    print(f"      AUDIT the composition's comparison: P_union "
          f"{comp_cmp['P_union']:+.4f} vs exp293's P_ctx "
          f"{comp_cmp['P_ctx_deposited']:+.4f} (delta "
          f"{comp_cmp['protection_delta_composition']:+.4f}) | the "
          f"ratio face: {comp_cmp['ratio_union']:.2f}x vs "
          f"{comp_cmp['ratio_ctx_deposited']:.2f}x")
    for h in hosts:
        ph = prot["per_host_P"][h]
        tag = " <== outlier" if h in outliers else ""
        print(f"      {h:4s} P {ph['P']:+.4f}{tag}")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(the determinism canary: "
          f"{gates['G4_discipline']['determinism_canary_bit_identical']}, "
          f"form {run_form}; no wall-clock fields: {no_wall_clock}; "
          f"docstring+header pinned to 26e15a1; exp142 + the core NOT "
          f"modified; the test suite "
          f"{gates['G4_discipline']['test_suite']['green']}; floor at "
          f"exit {gates['G4_discipline']['floor_at_exit']})")
    print(f"\n  BRANCH: {branch} | P_union {P:+.4f} mV | the bar "
          f"{PROTECT_BAR}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    if _MODE == "merge":
        for tag in (1, 2):
            if os.path.exists(_CK[tag]):
                os.remove(_CK[tag])
        print("  the checkpoint caches removed after the merge")
    return deposit


if __name__ == "__main__":
    main()
