#!/usr/bin/env python3
"""exp293 — THE HISTORY x STRESS INTERACTION: DOES THE REGISTER
PROTECT THE DECODE UNDER WRITE-TIME IONIC STRESS? (batch 48; ledger
L270's registered next (ii) — exp290 landed STORAGE-SIDE: the
write-time depolarized stress (-35.0 pin during the walk) degrades
the decode by 13.13 mV mean on every host while the read-time stress
is bit-identical to the anchor. exp289 landed HISTORY-CARRIED: the
self-history register improves the decode on 12/12 hosts, monotone
in g. The interaction is the memory-protection face: if the commit
history is a state variable that carries the program's own pattern
across the walk, a history-carrying walk under write-time stress may
degrade LESS than the schema-only walk under the same stress — the
register as a PROTECTIVE variable (the Sediqi 2026 history face's
causal form). The null: the stress degradation is additive and the
register's improvement independent — the interaction delta == 0.)

THE INSTRUMENT (exp289's + exp290's landed forms COMPOSED VERBATIM):
the 72-row substituted battery (exp256's) under the 2x2 factorial
(the register state x the stress state, both the machinery's own
constants):
  H0-S0  register OFF (the g=0 schema-only form), floor -60.0
         (the anchor — the errs reproduce exp256's deposited errs
         BIT-EXACT 72/72);
  H1-S0  register ON (the self-history form at the exp289-deposited
         best dose g=1.0), floor -60.0 (the errs reproduce exp289's
         deposited g=1.0 errs BIT-EXACT 72/72);
  H0-S1  register OFF, the WRITE-TIME stress (the walk at the -35.0
         pin, exp290's A1 arm verbatim — the errs reproduce exp290's
         deposited A1 errs BIT-EXACT 72/72);
  H1-S1  register ON (g=1.0), the WRITE-TIME stress (the NEW cell).
THE PROTECTION READ (zero knobs): the protection delta
  P = [mean_err(H0-S1) - mean_err(H1-S1)]
      - [mean_err(H0-S0) - mean_err(H1-S0)]
(the standard 2x2 interaction: the stress degradation under the
register minus the stress degradation without it; P > 0 = the
register PROTECTS — the stress hurts less when the history is
carried; P = 0 = additive independence; P < 0 = the register
AMPLIFIES the stress harm).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: H0-S0 == exp256's deposited errs BIT-EXACT 72/72;
      H1-S0 == exp289's deposited g=1.0 errs BIT-EXACT 72/72 (the
      trace shas 72/72); H0-S1 == exp290's deposited A1 errs
      BIT-EXACT 72/72; the floor asserts (the -35.0 pin during the
      walk in the S1 cells 144/144, -60.0 at the encode in the S0
      cells 144/144, -60.0 at every settle/decode 288/288); 8
      deposits READ-ONLY (exp243/256/272/273/282/287/288/289/290 —
      9 deposits, sha before/after).
  G2  THE NEW CELL'S INTEGRITY (H1-S1, zero-knob asserted, fail=STOP
      per row): finite errs 72/72; the A3 convention 72/72; the
      trace lengths == walk_steps 72/72; the commit counts ==
      walk_steps 72/72; the register's replay equality (exp289's G2
      form) 72/72 (the register populates identically under stress —
      the population path is stress-independent by construction,
      asserted); the S* lock reads 288 (4 cells x 72).
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars): P vs the
      pre-named bar PROTECT_BAR 0.05 mV (the exp290 margin form):
      PROTECTED   iff P >= 0.05;
      AMPLIFIED   iff P <= -0.05;
      ADDITIVE    otherwise (the honest null: the two effects
          independent at the machinery's resolution).
      Per-host P recorded (the outliers H3/H5's P, audit-only); the
      worst-err per cell vs the 6.0 bar (unchanged); the commit
      censuses per cell (the stress's effect on the (e) branch,
      exp290's disclosed form).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified
      (the composition uses exp289's landed register + exp290's
      landed pin schedule — the module attributes set around the
      calls, disclosed); NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PROTECTED / AMPLIFIED / ADDITIVE at the
PROTECT_BAR 0.05 mV form.

RUN: 288 decodes ~ 4-6 min — the pre-named form is the CHECKPOINT-
SPLIT EXP293_MODE=pass1 (the S0 cells, 144 decodes) | pass2 (the S1
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
OUT = os.path.join(ROOT, "results", "exp293_history_stress.json")


def main() -> dict:
    # ==== BODY (written under the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 15dab43; gates G1-G4
    #      evaluated exactly once. THE COMPOSITION: exp289's landed
    #      register form (the register live + the self-history blend,
    #      its landed body's additions (g)/(h)) + exp290's landed
    #      stress-pin schedule (the A1 write-time -35.0 pin around the
    #      calls, its landed body's arm form) — both VERBATIM, the
    #      module attributes set around the calls, disclosed) ===========
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
    #      is the 15dab43 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "de02e743d88f871879910f9bbb122908b0a4316b8dab7fbdfabcf83c199833f0")
    EXPECTED_HEADER_SHA256 = (
        "058652e15ea82b48451a47d90ded730c5ba0addbb6c934e1f901478e67170e98")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 15dab43"
    assert header_ok, "header drifted from 15dab43"

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
    # THE 2x2 FACTORIAL (pre-named): the register state (H0 off / H1 on
    # at the exp289-deposited best dose g=1.0) x the stress state (S0
    # floor -60.0 / S1 the write-time -35.0 pin during the walk only).
    CELLS = ("H0-S0", "H1-S0", "H0-S1", "H1-S1")
    CELL_G = {"H0-S0": 0.0, "H1-S0": 1.0, "H0-S1": 0.0, "H1-S1": 1.0}
    CELL_ARM = {"H0-S0": "A0", "H1-S0": "A0", "H0-S1": "A1", "H1-S1": "A1"}
    CELL_NAMES = {
        "H0-S0": "register OFF, floor -60.0 (the exp256 anchor)",
        "H1-S0": ("register ON g=1.0, floor -60.0 (the exp289 "
                  "deposited best-dose anchor)"),
        "H0-S1": ("register OFF, the write-time -35.0 pin during the "
                  "walk only (exp290's A1 arm verbatim)"),
        "H1-S1": ("register ON g=1.0 + the write-time -35.0 pin during "
                  "the walk only (THE NEW CELL)")}
    G_BEST = 1.0                           # exp289's deposited best dose
    # THE BRANCH BAR (pre-named at 15dab43, numeric, never fit)
    PROTECT_BAR = 0.05                     # the exp290 margin form
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
    #      read, re-verified byte-unchanged at the end. The
    #      pre-registration's G1 text says "8 deposits" but NAMES nine:
    #      exp243/256/272/273/282/287/288/289/290 — the body implements
    #      the named list, 9 deposits READ-ONLY (the exp231
    #      plumbing-precedent disclosure form; the gates untouched)) ---
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
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287, DEP288,
                 DEP289, DEP290)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit",
                  DEP288: "exp288_deposit", DEP289: "exp289_deposit",
                  DEP290: "exp290_deposit"}
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
    #      activation's class plan (exp289's landed form) and by the
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

    # ---- THE COMPOSED TRACED REPLICA: exp289's landed
    #      _execute_signed_traced (the disclosed recording additions
    #      (a)-(f) + the register additions (g) + the activation (h))
    #      and exp290's landed _execute_signed_traced_arm (the floor
    #      set around the calls in exp169's disclosed pin form + the
    #      five-boundary floor_rec recording) COMPOSED — the walk loop
    #      is exp289's VERBATIM with exp290's pure floor reads slotted
    #      at its landed boundaries; the A0 arm never pins (the S0
    #      bit-exactness is preserved — proven by the anchors below);
    #      the A2 read-stress arm is NOT part of this factorial (the
    #      pre-named cells use A0/A1 only). --------------------------------
    def _execute_signed_traced_composed(spec, adjacency, seed, op, budget,
                                        g_ctx=0.0, a_base=None, arm="A0"):
        assert arm in ("A0", "A1"), f"unknown arm {arm}"
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
        # ---- (g) exp289's register PRESENCE + INIT at the walk's start
        #      (fail=STOP per row): the attribute exists and the init ==
        #      the spec's install BIT-EXACT (the write_spec_layer port
        #      site; runs BEFORE the A1 pin — the history starts as the
        #      program's own target at the production floor) -----------
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
                    "blend_idx": []}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        # ---- exp290's ARM PIN (A1 only): the write-stress floor goes on
        #      at the ENCODE WINDOW's start, through the last commit (the
        #      landed schedule; A0 runs the encode at -60.0) ------------
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
        commits: list = []                     # (f) the disclosed
                                               #     recording addition
        blend_idx: list = []                   # (h) the activation's plan
        n_hist_writes = 0                      # (h) the activation count
        # (h) the activation's class plan (exp289's landed form: exp208's
        # classes on the plan; T and A_base are g- and stress-independent,
        # so the row sets match 1:1 across ALL FOUR cells). Computed ONLY
        # when the coupling is armed — zero deviation at g_ctx == 0.0.
        cls = None
        if g_ctx > 0.0:
            assert a_base is not None, \
                "the activation needs the base adjacency"
            cls = classify(target, a_base)["class"]
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
            # ---- (e) THE FLOOR READ AT STEP TIME (exp290's landed
            #      form): the commit branch reads the module attribute
            #      live — the A1 pin (-35.0) re-routes the sub-floor
            #      spec cells to the canon fallback; A0 reads -60.0 ----
            if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "spec"
            elif canon_src is not None:
                theta_new = canon_src[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "canon"
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "parent"
            # ---- (h) exp289's ACTIVATION: the self-history blend (ZERO
            #      at g_ctx == 0.0) — exp258's canon-boundary restriction
            #      verbatim; the read source is the cell's OWN history
            #      register (its last commit == the spec's install for a
            #      never-written cell) -----------------------------------
            written = theta_new
            if g_ctx > 0.0 and cls[i] == 0:
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            # ---- (f) the commit value recorded AT THE WRITE (after the
            #      write; the inherited/committed theta per cell) -------
            commits.append((int(i), float(written), src_tag))
            # ---- (g) exp289's REGISTER POPULATION: after the write the
            #      register holds the committed value — the commit
            #      sequence stored incrementally (a pure recording; the
            #      RNG stream and the dynamics untouched; the population
            #      path is stress-independent by construction) ---------
            c.phi_history[i] = written
            if g_ctx > 0.0 and cls[i] == 0:
                n_hist_writes += 1
                blend_idx.append(int(i))
            # ---- exp290's first-commit floor read (a pure recording) --
            if not first_commit_done:
                floor_rec["walk_first_commit"] = read_floor()
                first_commit_done = True
            # ---- (a) the per-step RMS read (a pure read; the walk's
            #      full-frame convergence; unchanged) -----------------
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
        # ---- (g) exp289's REGISTER AT THE WALK'S END (fail=STOP per
        #      row): the register SURVIVED the walk + the settle; on the
        #      write set it IS the commit replay BIT-EXACT; off the
        #      write set it IS the spec's install; finite everywhere ---
        reg = getattr(c, "phi_history", None)
        reg_present_ok = bool(reg is not None)
        assert reg_present_ok, \
            "the history register vanished across the walk"
        reg = np.asarray(reg, dtype=float)
        reg_finite_ok = bool(np.all(np.isfinite(reg)))
        assert reg_finite_ok, "non-finite history-register entry"
        replay_idx = [int(rec[0]) for rec in commits]
        replay_val = np.asarray([float(rec[1]) for rec in commits],
                                dtype=float)
        reg_replay_ok = bool(np.array_equal(reg[replay_idx], replay_val))
        assert reg_replay_ok, \
            "the register's write-set face drifted from the commit " \
            "replay — the register is not the commit sequence stored " \
            "incrementally"
        comp = np.ones(n, dtype=bool)
        comp[replay_idx] = False
        reg_complement_ok = bool(np.array_equal(reg[comp], target[comp]))
        assert reg_complement_ok, \
            "the register's non-write-set face drifted from the spec " \
            "install"
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
        out["reg_init_ok"] = reg_init_ok               # (g) the port
        out["reg_present_ok"] = reg_present_ok         # (g) the port
        out["reg_replay_ok"] = reg_replay_ok           # (g) the port
        out["reg_complement_ok"] = reg_complement_ok   # (g) the port
        out["reg_finite_ok"] = reg_finite_ok           # (g) the port
        out["phi_history_sha256"] = _f_sha(reg)        # (g) the port
        out["n_hist_writes"] = int(n_hist_writes)      # (h) the activation
        out["blend_idx"] = blend_idx                   # (h) the plan
        out["floor_rec"] = floor_rec                   # exp290's arm face
        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced + budgeted + composed
    #      executor call) --------------------------------------------------
    def _scoped_row_read_composed(spec, med, seed, fmax, budget,
                                  g_ctx=0.0, a_base=None, arm="A0"):
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
            out = _execute_signed_traced_composed(
                spec, A_ext, seed, op=STAR_OP, budget=budget,
                g_ctx=g_ctx, a_base=a_base, arm=arm)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one CELL-row decode (the composed read + the per-row asserts,
    #      fail=STOP; the anchor asserts per cell per the pre-named G1
    #      set: H0-S0 == exp256's errs (+ the exp282 walk anchors per the
    #      exp289/exp290 S0 discipline), H1-S0 == exp289's g=1.0 errs +
    #      trace shas, H0-S1 == exp290's A1 errs; the commit-layer
    #      digests and the remaining cross-deposit faces recorded
    #      AUDIT-ONLY, never gating) --------------------------------------
    def _decode_cell_row(cell, host, row_key, spec, med, seed, fmax,
                         A_base, dep_rec, rec282, rec287, rec288,
                         rec289g1, rec290a1):
        assert cell in CELLS, f"unknown cell {cell}"
        g_ctx = float(CELL_G[cell])
        arm = CELL_ARM[cell]
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_composed(
            spec, med, seed, fmax, BUDGET,
            g_ctx=g_ctx, a_base=(A_base if g_ctx > 0.0 else None),
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
            f"{host} {row_key} s{seed} {cell}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        census_ok = bool(sum(census_src.values()) == n_commits
                         and set(tags) <= set(COMMIT_SOURCES))
        assert census_ok, \
            f"{host} {row_key} s{seed} {cell}: the commit source census " \
            "drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        commit_idx_sha = hashlib.sha256(
            json.dumps(idxs, sort_keys=True).encode()).hexdigest()
        blend_idx = [int(i) for i in out["blend_idx"]]
        blend_idx_sha = hashlib.sha256(
            json.dumps(blend_idx, sort_keys=True).encode()).hexdigest()
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

        rec = {"cell": cell, "arm": arm, "g_ctx": g_ctx,
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
               "blend_idx_sha256": blend_idx_sha,
               "src_census": census_src,
               "sc_rms": sc_rms, "sc_frac": sc_frac, "cvt_rms": cvt_rms,
               "floor_rec": {k: float(v)
                             for k, v in out["floor_rec"].items()},
               "floor_schedule_ok": floor_schedule_ok,
               "register": reg,
               "n_hist_writes": int(out["n_hist_writes"]),
               "final_positive_ok": final_positive_ok,
               "conv_ok": conv_ok}
        # ---- THE ANCHOR ASSERTS (per cell, the pre-named G1 set;
        #      fail=STOP; the extra cross-deposit faces AUDIT-ONLY) -----
        if cell == "H0-S0":
            # THE S0 ANCHOR: exp256's deposited errs BIT-EXACT (the
            # exp289/exp290 S0 discipline: the walk anchors too)
            s0_err_ok = bool(err == dep_rec["err"])
            s0_ver_ok = bool(bool(out["program_verified"])
                             == bool(dep_rec["verified"]))
            assert s0_err_ok, \
                (f"{host} {row_key} s{seed} H0-S0: the fresh err {err} "
                 f"drifted from exp256's deposited {dep_rec['err']} — "
                 "the H0-S0 anchor REFUTED")
            assert s0_ver_ok, \
                f"{host} {row_key} s{seed} H0-S0: the verified flag drifted"
            we_ok = bool(final == float(rec282["walk_end_rms"]))
            assert we_ok, \
                (f"{host} {row_key} s{seed} H0-S0: the fresh "
                 "walk_end_rms drifted from exp282's deposited")
            ts_ok = bool(trace_sha == rec282["trace_sha256"])
            assert ts_ok, \
                (f"{host} {row_key} s{seed} H0-S0: the fresh trace sha "
                 "drifted from exp282's deposited — the walk is not the "
                 "traced one")
            ee_ok = bool(err_exact == float(rec282["err_exact"]))
            assert ee_ok, \
                (f"{host} {row_key} s{seed} H0-S0: the fresh err_exact "
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
        elif cell == "H1-S0":
            # THE exp289 ANCHOR: the deposited best-dose g=1.0 errs +
            # trace shas BIT-EXACT (the pre-named G1 clause)
            h1_err_ok = bool(err == float(rec289g1["err"]))
            assert h1_err_ok, \
                (f"{host} {row_key} s{seed} H1-S0: the fresh err {err} "
                 f"drifted from exp289's deposited g=1.0 "
                 f"{rec289g1['err']} — the H1-S0 anchor REFUTED")
            h1_ts_ok = bool(trace_sha == rec289g1["trace_sha256"])
            assert h1_ts_ok, \
                (f"{host} {row_key} s{seed} H1-S0: the fresh trace sha "
                 "drifted from exp289's deposited g=1.0 trace sha — "
                 "the history-carrying walk is not the deposited one")
            rec["h1s0_err_ok"] = h1_err_ok
            rec["h1s0_trace_sha_ok"] = h1_ts_ok
            # audit-only: the rest of the deposited g=1.0 row face
            rec["h1s0_walk_end_ok"] = bool(
                final == float(rec289g1["walk_end_rms"]))
            rec["h1s0_reg_sha_ok"] = bool(
                reg["phi_history_sha256"]
                == rec289g1["register"]["phi_history_sha256"])
            rec["h1s0_nhw_ok"] = bool(
                rec["n_hist_writes"] == int(rec289g1["n_hist_writes"]))
            rec["h1s0_ncommits_ok"] = bool(
                n_commits == int(rec289g1["n_commits"]))
        elif cell == "H0-S1":
            # THE exp290 ANCHOR: the deposited A1 errs BIT-EXACT (the
            # pre-named G1 clause)
            ws1_err_ok = bool(err == float(rec290a1["err"]))
            assert ws1_err_ok, \
                (f"{host} {row_key} s{seed} H0-S1: the fresh err {err} "
                 f"drifted from exp290's deposited A1 "
                 f"{rec290a1['err']} — the H0-S1 anchor REFUTED")
            rec["h0s1_err_ok"] = ws1_err_ok
            # audit-only: the walk + the floor schedule vs the deposit
            rec["h0s1_trace_sha_ok"] = bool(
                trace_sha == rec290a1["trace_sha256"])
            rec["h0s1_floor_rec_ok"] = bool(
                rec["floor_rec"] == {k: float(v) for k, v in
                                     rec290a1["floor_rec"].items()})
            rec["h0s1_ncommits_ok"] = bool(
                n_commits == int(rec290a1["n_commits"]))
        else:  # H1-S1 — THE NEW CELL: the G2 integrity face is asserted
            # above (finite err, A3, trace length, commit count, the
            # register's replay equality); no deposit anchor applies.
            rec["new_cell"] = True
        return rec

    # ---- THE REBUILD (exp290's landed form VERBATIM: the sha-asserted
    #      rebuild against exp243's OWN records + the re-reads; shared by
    #      both passes — deterministic; PLUS the exp289/exp290 anchor
    #      re-reads) -------------------------------------------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_canon_ok": 0, "h0_echo_h1": False, "n_fmax_ok": 0,
                  "n_nonneg_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
                  "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
                  "n_medium_shas_ok": 0, "n_rows282": 0,
                  "n_282_chain_ok": 0, "n_rows287": 0, "n_rows288": 0,
                  "n_rows289_g1": 0, "n_rows290_a1": 0}
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

        # exp256's 72 rows — the substituted records the H0-S0 anchor
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
        # deposits; audit-only cross-checks for the H0-S0 cell)
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

        # THE EXP289 ANCHOR RE-READ (the deposited best-dose g=1.0 grid
        # rows — the H1-S0 anchor's source; the deposited branch + dose
        # face asserted)
        assert dep289["branch"] == "HISTORY-CARRIED", \
            "exp289's deposited branch drifted from HISTORY-CARRIED"
        assert float(dep289["grid"]["best_grid_point"]) == G_BEST, \
            "exp289's deposited best dose drifted from g=1.0"
        r289g1 = {}
        for r in dep289["grid_rows"]:
            if float(r["g_ctx"]) != G_BEST:
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r289g1, f"duplicate exp289 g=1.0 row {key}"
            assert all(fld in r for fld in
                       ("err", "trace_sha256", "walk_end_rms",
                        "n_hist_writes", "n_commits")) \
                and "phi_history_sha256" in r["register"], \
                f"{key}: exp289's g=1.0 row record is missing anchors"
            r289g1[key] = r
        counts["n_rows289_g1"] = len(r289g1)
        assert counts["n_rows289_g1"] == 72, \
            "exp289's 72-row g=1.0 grid drifted"

        # THE EXP290 ANCHOR RE-READ (the deposited A1 rows — the H0-S1
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
                         "branch": dep290["branch"]}}
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "r288": r288, "r289g1": r289g1,
                "r290a1": r290a1, "integrity": integrity}

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
                            rb["dep_sub"][(k, s, rk)],
                            rb["r282"][(k, s, rk)],
                            rb["r287"][(k, s, rk)],
                            rb["r288"][(k, s, rk)],
                            rb["r289g1"][(k, s, rk)],
                            rb["r290a1"][(k, s, rk)])
                        rows_out.append(rec)
                        if cell not in first_args:
                            first_args[cell] = (
                                k, rk, ctx["deep"][inst]["spec"], med, s,
                                ctx["fmax"], ctx["A"])
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
            k, rk, spec_o, med_o, s, fmax_o, abase_o = first_args[cell]
            r1 = rows_by_cell[cell][0]
            assert (r1["host"], r1["row_key"], int(r1["seed"])) == \
                (k, rk, s), "the canary's first-row args drifted"
            mark = len(_LOCK_LOG)
            r2 = _decode_cell_row(
                cell, k, rk, spec_o, med_o, s, fmax_o, abase_o,
                rb["dep_sub"][(k, s, rk)], rb["r282"][(k, s, rk)],
                rb["r287"][(k, s, rk)], rb["r288"][(k, s, rk)],
                rb["r289g1"][(k, s, rk)], rb["r290a1"][(k, s, rk)])
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
                and r2["n_hist_writes"] == r1["n_hist_writes"]
                and r2["blend_idx_sha256"] == r1["blend_idx_sha256"])
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
    #      the blend-plan face asserted across the cells here — the
    #      structural zero-knob asserts, fail=STOP) -----------------------
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
        assert len(set(E["H0-S0"])) == 72, "the 72-row paired frame drifted"
        assert set(E["H0-S0"]) == set(E["H1-S0"]) == set(E["H0-S1"]) \
            == set(E["H1-S1"]), "the paired key frame drifted across cells"
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
        for key in E["H0-S0"]:
            ok = bool(
                len({E[c][key]["commit_idx_sha256"] for c in CELLS}) == 1
                and len({E[c][key]["walk_steps"] for c in CELLS}) == 1
                and len({E[c][key]["n_commits"] for c in CELLS}) == 1)
            assert ok, \
                (f"{key}: the stream face drifted across the cells — the "
                 "walk order / commit count moved with a factor")
            n_stream_ok += int(ok)
        assert n_stream_ok == 72, "the stream face drifted"
        # ---- THE BLEND-PLAN FACE: the activation's class plan is
        #      (target, A)-determined — the blend count + the blend
        #      index digest identical across the two H1 cells per row ---
        n_blend_ok = 0
        for key in E["H0-S0"]:
            ok = bool(
                E["H1-S0"][key]["n_hist_writes"]
                == E["H1-S1"][key]["n_hist_writes"]
                and E["H1-S0"][key]["blend_idx_sha256"]
                == E["H1-S1"][key]["blend_idx_sha256"])
            assert ok, \
                (f"{key}: the blend-plan face drifted — the activation's "
                 "population path moved with the stress")
            n_blend_ok += int(ok)
        assert n_blend_ok == 72, "the blend-plan face drifted"

        # ---- THE PROTECTION READ (zero knobs, the pre-named 2x2
        #      interaction on the mean errs) -----------------------------
        cell_means = {c: float(np.mean(
            [r["err"] for r in rows_by_cell[c]])) for c in CELLS}
        stress_no_reg = float(cell_means["H0-S1"] - cell_means["H0-S0"])
        stress_with_reg = float(cell_means["H1-S1"] - cell_means["H1-S0"])
        reg_no_stress = float(cell_means["H0-S0"] - cell_means["H1-S0"])
        reg_under_stress = float(cell_means["H0-S1"]
                                 - cell_means["H1-S1"])
        P = float(reg_under_stress - reg_no_stress)
        assert np.isfinite(P), "non-finite protection delta"
        if P >= PROTECT_BAR:
            branch = "PROTECTED"
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
                "P": float((m["H0-S1"] - m["H1-S1"])
                           - (m["H0-S0"] - m["H1-S0"]))}

        # ---- the per-cell summaries (the zero-knob tallies) ------------
        tallies = {}
        for cell in CELLS:
            rows = rows_by_cell[cell]
            errs = [float(r["err"]) for r in rows]
            tallies[cell] = {
                "cell": cell, "arm": CELL_ARM[cell],
                "g_ctx": float(CELL_G[cell]), "name": CELL_NAMES[cell],
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
                                                for r in rows))}

        # ---- the tallies per gate ---------------------------------------
        n_s0_err = int(sum(bool(E["H0-S0"][k].get("s0_err_ok"))
                           for k in E["H0-S0"]))
        n_s0_ver = int(sum(bool(E["H0-S0"][k].get("s0_verified_ok"))
                           for k in E["H0-S0"]))
        n_we282 = int(sum(bool(E["H0-S0"][k].get("walk_end_282_ok"))
                          for k in E["H0-S0"]))
        n_ts282 = int(sum(bool(E["H0-S0"][k].get("trace_sha_282_ok"))
                          for k in E["H0-S0"]))
        n_ee282 = int(sum(bool(E["H0-S0"][k].get("err_exact_282_ok"))
                          for k in E["H0-S0"]))
        n_h1s0_err = int(sum(bool(E["H1-S0"][k].get("h1s0_err_ok"))
                             for k in E["H1-S0"]))
        n_h1s0_ts = int(sum(bool(E["H1-S0"][k].get("h1s0_trace_sha_ok"))
                            for k in E["H1-S0"]))
        n_h0s1_err = int(sum(bool(E["H0-S1"][k].get("h0s1_err_ok"))
                             for k in E["H0-S1"]))
        # the floor facets (the pre-named G1 counts)
        s1_cells = ("H0-S1", "H1-S1")
        s0_cells = ("H0-S0", "H1-S0")
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
        n_a0_sha287 = int(sum(bool(E["H0-S0"][k].get("commit_sha_287_ok"))
                              for k in E["H0-S0"]))
        n_a0_sha288 = int(sum(bool(E["H0-S0"][k].get("commit_sha_288_ok"))
                              for k in E["H0-S0"]))
        n_a0_cvt287 = int(sum(bool(E["H0-S0"][k].get("cvt_287_ok"))
                              for k in E["H0-S0"]))
        n_h0s1_ts = int(sum(bool(E["H0-S1"][k].get("h0s1_trace_sha_ok"))
                            for k in E["H0-S1"]))
        n_h0s1_fr = int(sum(bool(E["H0-S1"][k].get("h0s1_floor_rec_ok"))
                            for k in E["H0-S1"]))
        n_h1s0_we = int(sum(bool(E["H1-S0"][k].get("h1s0_walk_end_ok"))
                            for k in E["H1-S0"]))
        n_h1s0_rg = int(sum(bool(E["H1-S0"][k].get("h1s0_reg_sha_ok"))
                            for k in E["H1-S0"]))
        n_h1s0_nhw = int(sum(bool(E["H1-S0"][k].get("h1s0_nhw_ok"))
                             for k in E["H1-S0"]))
        n_h1s1_replay = int(sum(E["H1-S1"][k]["register"]["replay_ok"]
                                for k in E["H1-S1"]))
        n_h1s1_fin = int(sum(np.isfinite(E["H1-S1"][k]["err"])
                             for k in E["H1-S1"]))
        n_h1s1_a3 = int(sum(E["H1-S1"][k]["a3_ok"] for k in E["H1-S1"]))
        n_h1s1_tl = int(sum(E["H1-S1"][k]["trace_len_ok"]
                            for k in E["H1-S1"]))
        n_h1s1_cc = int(sum(E["H1-S1"][k]["commits_count_ok"]
                            for k in E["H1-S1"]))

        g1 = dict(p1["integrity"]["counts"])
        g1.update({
            "n_h0s0_err_ok": n_s0_err, "n_h0s0_verified_ok": n_s0_ver,
            "n_walk282_ok": n_we282, "n_trace282_ok": n_ts282,
            "n_errexact282_ok": n_ee282,
            "n_h1s0_err_ok": n_h1s0_err, "n_h1s0_trace_sha_ok": n_h1s0_ts,
            "n_h0s1_err_ok": n_h0s1_err,
            "n_floor_walk_s1_ok": n_floor_walk_s1,
            "n_floor_encode_s0_ok": n_floor_encode_s0,
            "n_floor_encode_s1_audit": n_floor_encode_s1,
            "n_floor_settle_decode_ok": n_floor_settle_decode,
            "n_a0_commit_sha_287_audit": n_a0_sha287,
            "n_a0_commit_sha_288_audit": n_a0_sha288,
            "n_a0_cvt_287_audit": n_a0_cvt287,
            "n_h0s1_trace_sha_audit": n_h0s1_ts,
            "n_h0s1_floor_rec_audit": n_h0s1_fr,
            "n_h1s0_walk_end_audit": n_h1s0_we,
            "n_h1s0_reg_sha_audit": n_h1s0_rg,
            "n_h1s0_nhw_audit": n_h1s0_nhw})
        g2 = {"n_rows": 72, "n_finite_err": n_h1s1_fin,
              "n_a3_ok": n_h1s1_a3, "n_trace_len_ok": n_h1s1_tl,
              "n_commits_count_ok": n_h1s1_cc,
              "n_register_replay_ok": n_h1s1_replay,
              "n_stream_ok_rows": n_stream_ok,
              "n_blend_plan_ok": n_blend_ok,
              "n_lock_reads": lock_total}
        g3 = {"branch": branch, "bar": PROTECT_BAR, "P": P,
              "cell_means": cell_means,
              "stress_degradation_no_register": stress_no_reg,
              "stress_degradation_with_register": stress_with_reg,
              "register_improvement_no_stress": reg_no_stress,
              "register_improvement_under_stress": reg_under_stress,
              "n_rows": 72,
              "per_host_P_finite": bool(all(
                  np.isfinite(per_host_P[h]["P"]) for h in hosts))}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": p1["integrity"],
                "rows": [r for c in CELLS for r in rows_by_cell[c]],
                "per_cell": tallies,
                "protection": {
                    "form": ("P = [mean_err(H0-S1) - mean_err(H1-S1)] - "
                             "[mean_err(H0-S0) - mean_err(H1-S0)]"),
                    "bar": PROTECT_BAR, "P": P,
                    "cell_means": cell_means,
                    "stress_degradation_no_register": stress_no_reg,
                    "stress_degradation_with_register": stress_with_reg,
                    "register_improvement_no_stress": reg_no_stress,
                    "register_improvement_under_stress": reg_under_stress,
                    "per_host_P": per_host_P,
                    "outliers_H3_H5": {h: per_host_P[h]
                                       for h in outliers}},
                "stream_face": {"n_stream_ok_rows": n_stream_ok,
                                "n_blend_plan_ok": n_blend_ok},
                "branch": branch,
                "branch_discriminant": {
                    "bar": PROTECT_BAR,
                    "bar_pre_named_at": ("15dab43 — fixed at "
                                         "pre-registration, never fit"),
                    "form": ("PROTECTED iff P >= 0.05; AMPLIFIED iff "
                             "P <= -0.05; else ADDITIVE (the honest "
                             "null: the two effects independent at the "
                             "machinery's resolution)"),
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
    #      SPLIT EXP293_MODE=pass1 (the S0 cells, 144 decodes) | pass2
    #      (the S1 cells, 144 decodes) | merge — each pass a separate
    #      process, the merge assembling + evaluating the gates once and
    #      NEVER re-decoding; the in-process default for the GitHub
    #      runners. Both forms evaluate the SAME gates.) ------------------
    _MODE = os.environ.get("EXP293_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp293_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp293_pass2.checkpoint.json")}
    PASS_CELLS = {1: ("H0-S0", "H1-S0"), 2: ("H0-S1", "H1-S1")}

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
        print(f"=== exp293 pass{tag}: the "
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
        print("=== exp293: THE HISTORY x STRESS INTERACTION (does the "
              "register protect the decode under write-time ionic "
              "stress?) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows x 4 cells = 288 decodes "
              f"at the production budget {BUDGET} (== exp142's "
              f"STEPS_PER_CELL)")
        print(f"  the cells: H0-S0 the exp256 anchor | H1-S0 the exp289 "
              f"g=1.0 anchor | H0-S1 exp290's A1 arm verbatim | H1-S1 "
              f"THE NEW CELL | the branch bar: PROTECT_BAR {PROTECT_BAR} "
              f"mV")
        p1 = _compute_pass(1)
        p2 = _compute_pass(2)
        sa = _payload_sha(p1)
        sb = _payload_sha(p2)
        core = _assemble(p1, p2, "in-process default (one invocation)")
        run_form = "in-process default (one invocation)"

    # ---- the gate assembly (evaluated exactly once) ---------------------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    tallies = core["per_cell"]
    prot = core["protection"]
    branch = core["branch"]
    P = prot["P"]
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
        and g1["n_h0s0_err_ok"] == 72 and g1["n_h0s0_verified_ok"] == 72
        and g1["n_walk282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72
        and g1["n_h1s0_err_ok"] == 72 and g1["n_h1s0_trace_sha_ok"] == 72
        and g1["n_h0s1_err_ok"] == 72
        and g1["n_floor_walk_s1_ok"] == 144
        and g1["n_floor_encode_s0_ok"] == 144
        and g1["n_floor_settle_decode_ok"] == 288
        and ro_unchanged)
    g2_pass = bool(
        g2["n_rows"] == 72 and g2["n_finite_err"] == 72
        and g2["n_a3_ok"] == 72 and g2["n_trace_len_ok"] == 72
        and g2["n_commits_count_ok"] == 72
        and g2["n_register_replay_ok"] == 72
        and g2["n_stream_ok_rows"] == 72 and g2["n_blend_plan_ok"] == 72
        and g2["n_lock_reads"] == 288)
    g3_pass = bool(
        g3["branch"] in ("PROTECTED", "AMPLIFIED", "ADDITIVE")
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

    if branch == "PROTECTED":
        branch_text = (
            "the register PROTECTS — the stress hurts less when the "
            "history is carried: the write-time degradation is smaller "
            "under the register by the pre-named margin (the "
            "memory-protection face, the Sediqi 2026 history face's "
            "causal form)")
    elif branch == "AMPLIFIED":
        branch_text = (
            "the register AMPLIFIES the stress harm — the write-time "
            "degradation is LARGER under the register by the pre-named "
            "margin (the interaction is anti-protective)")
    else:
        branch_text = (
            "ADDITIVE — the stress degradation is additive and the "
            "register's improvement independent at the machinery's "
            "resolution (the honest null: P within the pre-named "
            "±0.05 mV bar)")
    verdict_body = (
        f"{branch} — {branch_text} "
        f"(the protection read: P {P:+.4f} mV vs the pre-named "
        f"PROTECT_BAR {PROTECT_BAR} mV"
        f" | the cell means: H0-S0 {prot['cell_means']['H0-S0']:.4f} / "
        f"H1-S0 {prot['cell_means']['H1-S0']:.4f} / "
        f"H0-S1 {prot['cell_means']['H0-S1']:.4f} / "
        f"H1-S1 {prot['cell_means']['H1-S1']:.4f}"
        f" | the stress deltas: without the register "
        f"{prot['stress_degradation_no_register']:+.4f} mV, with the "
        f"register {prot['stress_degradation_with_register']:+.4f} mV | "
        f"the register improvements: without stress "
        f"{prot['register_improvement_no_stress']:+.4f} mV, under "
        f"stress {prot['register_improvement_under_stress']:+.4f} mV"
        f" | the per-host P within "
        f"[{min(v['P'] for v in prot['per_host_P'].values()):.3f}, "
        f"{max(v['P'] for v in prot['per_host_P'].values()):.3f}], the "
        f"outliers H3/H5: P(H3) {prot['outliers_H3_H5']['H3']['P']:+.4f} "
        f"/ P(H5) {prot['outliers_H3_H5']['H5']['P']:+.4f} (audit-only)"
        f" | the worst-err per cell vs the 6.0 bar (audit-only, "
        f"unchanged): H0-S0 {tallies['H0-S0']['worst_err']:.2f} "
        f"({tallies['H0-S0']['n_rows_over_bar']}/72 over) / H1-S0 "
        f"{tallies['H1-S0']['worst_err']:.2f} "
        f"({tallies['H1-S0']['n_rows_over_bar']}/72 over) / H0-S1 "
        f"{tallies['H0-S1']['worst_err']:.2f} "
        f"({tallies['H0-S1']['n_rows_over_bar']}/72 over) / H1-S1 "
        f"{tallies['H1-S1']['worst_err']:.2f} "
        f"({tallies['H1-S1']['n_rows_over_bar']}/72 over)"
        f" | the commit src censuses per cell (audit-only, the floor's "
        f"effect on the (e) branch): H0-S0 spec "
        f"{tallies['H0-S0']['src_census']['spec']} / canon "
        f"{tallies['H0-S0']['src_census']['canon']} / parent "
        f"{tallies['H0-S0']['src_census']['parent']}; H1-S0 spec "
        f"{tallies['H1-S0']['src_census']['spec']} / canon "
        f"{tallies['H1-S0']['src_census']['canon']} / parent "
        f"{tallies['H1-S0']['src_census']['parent']}; H0-S1 spec "
        f"{tallies['H0-S1']['src_census']['spec']} / canon "
        f"{tallies['H0-S1']['src_census']['canon']} / parent "
        f"{tallies['H0-S1']['src_census']['parent']}; H1-S1 spec "
        f"{tallies['H1-S1']['src_census']['spec']} / canon "
        f"{tallies['H1-S1']['src_census']['canon']} / parent "
        f"{tallies['H1-S1']['src_census']['parent']}"
        f" | THE ANCHORS (bit-exact): H0-S0 == exp256's deposited errs "
        f"{g1['n_h0s0_err_ok']}/72 (the verified flags "
        f"{g1['n_h0s0_verified_ok']}/72, exp282's walk anchors "
        f"{g1['n_walk282_ok']}/72 + trace shas {g1['n_trace282_ok']}/72 "
        f"+ err_exact {g1['n_errexact282_ok']}/72; the commit-layer "
        f"digests vs exp287/288 audit-only "
        f"{g1['n_a0_commit_sha_287_audit']}/72 + "
        f"{g1['n_a0_commit_sha_288_audit']}/72); H1-S0 == exp289's "
        f"deposited g=1.0 errs {g1['n_h1s0_err_ok']}/72 + trace shas "
        f"{g1['n_h1s0_trace_sha_ok']}/72 (the walk-end/register-digest/"
        f"blend-count faces audit-only {g1['n_h1s0_walk_end_audit']}/72 "
        f"+ {g1['n_h1s0_reg_sha_audit']}/72 + "
        f"{g1['n_h1s0_nhw_audit']}/72); H0-S1 == exp290's deposited A1 "
        f"errs {g1['n_h0s1_err_ok']}/72 (the fresh A1 trace shas match "
        f"the deposit {g1['n_h0s1_trace_sha_audit']}/72 and the floor "
        f"schedule {g1['n_h0s1_floor_rec_audit']}/72, audit-only)"
        f" | THE FLOOR ASSERTS: the -35.0 pin during the walk in the S1 "
        f"cells {g1['n_floor_walk_s1_ok']}/144, the -60.0 encode in the "
        f"S0 cells {g1['n_floor_encode_s0_ok']}/144 (the S1 encode at "
        f"the pin {g1['n_floor_encode_s1_audit']}/144, exp290's A1 "
        f"schedule), the -60.0 settle/decode everywhere "
        f"{g1['n_floor_settle_decode_ok']}/288"
        f" | THE NEW CELL (H1-S1, G2): finite errs "
        f"{g2['n_finite_err']}/72, the A3 convention "
        f"{g2['n_a3_ok']}/72, the trace lengths {g2['n_trace_len_ok']}"
        f"/72, the commit counts {g2['n_commits_count_ok']}/72, the "
        f"register's replay equality {g2['n_register_replay_ok']}/72 "
        f"(the population path is stress-independent: the stream face "
        f"{g2['n_stream_ok_rows']}/72 + the blend-plan face "
        f"{g2['n_blend_plan_ok']}/72); the S* lock reads "
        f"{g2['n_lock_reads']}/288"
        f" | 12 hosts, the deterministic sha-asserted rebuild "
        f"(graph_path for H0/H1, small_world at the deposited rewire "
        f"seeds), 9 deposits READ-ONLY byte-unchanged, exp142 + the "
        f"core NOT modified ({run_form}), floor -60.0")

    # ---- the discipline scans + the deposit form -------------------------
    deposit = {
        "exp": "exp293_history_stress",
        "claim": (
            "THE HISTORY x STRESS INTERACTION (batch 48, "
            "pre-registration commit 15dab43): DOES THE REGISTER PROTECT "
            "THE DECODE UNDER WRITE-TIME IONIC STRESS? exp290 landed "
            "STORAGE-SIDE (the write-time -35.0 pin during the walk "
            "degrades the decode by 13.13 mV mean, the read-time stress "
            "bit-identical to the anchor); exp289 landed HISTORY-CARRIED "
            "(the self-history register improves the decode on 12/12 "
            "hosts, monotone in g). The 2x2 factorial composes exp289's "
            "landed register form + exp290's landed stress-pin schedule "
            "VERBATIM over exp256's 72-row substituted battery: H0-S0 "
            "register OFF floor -60.0 (== exp256's errs bit-exact), "
            "H1-S0 register ON at the deposited best dose g=1.0 (== "
            "exp289's g=1.0 errs + trace shas bit-exact), H0-S1 the "
            "write-time pin (== exp290's A1 errs bit-exact), H1-S1 "
            "register ON + the write-time pin (THE NEW CELL). THE "
            "PROTECTION READ (zero knobs): P = [mean_err(H0-S1) - "
            "mean_err(H1-S1)] - [mean_err(H0-S0) - mean_err(H1-S0)]; "
            "PROTECTED iff P >= 0.05, AMPLIFIED iff P <= -0.05, else "
            "ADDITIVE (the honest null). The null: the stress "
            "degradation is additive and the register's improvement "
            "independent"),
        "method": {
            "composition": (
                "exp289's landed register form VERBATIM (the register "
                "live: the presence + the init == the spec's install "
                "asserted at the walk's start, the population after "
                "each commit write, the survival + the replay equality "
                "+ the spec-install complement asserted at the walk's "
                "end; the self-history blend at g_ctx > 0 on exp258's "
                "canon-boundary class plan — ZERO deviation at g=0.0) "
                "+ exp290's landed stress-pin schedule VERBATIM (the "
                "floor set around the calls in exp169's disclosed "
                "module-attribute pin form, PINNED = core + exp142 + "
                "exp145 + exp148 + exp94; the A1 pin -35.0 from the "
                "encode window's start through the last commit, "
                "restored to -60.0 before the settle; the "
                "five-boundary floor_rec recorded + asserted per row). "
                "The A2 read-stress arm is NOT part of this factorial. "
                "exp142 and the core NOT modified (the module "
                "attributes set around the calls, disclosed; the file "
                "shas recorded entry/exit)"),
            "replica": (
                "the exp286/exp287/exp288 traced replica lineage REUSED "
                "VERBATIM at the production budget 8 == exp142's "
                "STEPS_PER_CELL (the host rebuild, exp256's "
                "_scoped_row_read_state form: PN1/PN2 + TC1 + TC2 + the "
                "traced TC3), composed as above; the walk loop is "
                "exp289's landed loop with exp290's pure floor reads "
                "slotted at its landed boundaries (no RNG, no state "
                "change)"),
            "cells": {c: CELL_NAMES[c] for c in CELLS},
            "floor_schedule": FLOOR_SCHEDULE,
            "read": (
                "per cell the 72-row errs (the machinery's native 2-dp "
                "convention); the protection delta P = [mean_err(H0-S1) "
                "- mean_err(H1-S1)] - [mean_err(H0-S0) - mean_err(H1-"
                "S0)] on the 72-row battery means; the per-host P "
                "recorded audit-only (the outliers H3/H5 disclosed)"),
            "branch_rule": (
                "PROTECTED iff P >= PROTECT_BAR 0.05; AMPLIFIED iff "
                "P <= -0.05; else ADDITIVE. The bar 0.05 mV, fixed at "
                "pre-registration (15dab43), never fit (the exp290 "
                "margin form)"),
            "deposit_count_disclosure": (
                "the pre-registered G1 text says '8 deposits' but names "
                "nine (exp243/256/272/273/282/287/288/289/290) — the "
                "body implements the named list: 9 deposits READ-ONLY, "
                "sha before/after (the exp231 plumbing-precedent "
                "disclosure form; the gates untouched)"),
            "scope": (
                "the full traces and commit sequences NOT re-deposited "
                "— bit-reproduced via the per-row trace/commit/index "
                "digests + G1's anchors (the exp284-exp290 precedent); "
                "no wall-clock fields; the deterministic canary form")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base)",
                "the 72 rows — the H0-S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas",
                "the host frame + the per-host boundary counts + the "
                "premium pre-name source",
                "the outlier pre-name (H3/H5 — the audit-only per-host "
                "P carry)",
                "the S0 walk anchor — the 72 per-row walk_end_rms + "
                "trace shas + the deposited TRAJECTORY-CARRIED branch",
                "the S0 commit-layer anchor — the 72 per-row commit "
                "digests (audit-only cross-check for the H0-S0 cell)",
                "the battery's immediate predecessor — the 72 per-row "
                "commit digests (audit-only cross-check for the H0-S0 "
                "cell)",
                "the H1-S0 anchor — the deposited g=1.0 grid rows (the "
                "errs + the trace shas + the register digests) + the "
                "deposited HISTORY-CARRIED branch + the best dose 1.0",
                "the H0-S1 anchor — the deposited A1 rows (the errs + "
                "the trace shas + the floor schedules) + the deposited "
                "STORAGE-SIDE branch"))},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp256_reread": integrity["exp256_reread"],
        "exp282_reread": integrity["exp282_reread"],
        "exp287_reread": integrity["exp287_reread"],
        "exp288_reread": integrity["exp288_reread"],
        "exp289_reread": integrity["exp289_reread"],
        "exp290_reread": integrity["exp290_reread"],
        "rows": core["rows"],
        "per_cell": tallies,
        "protection": prot,
        "stream_face": core["stream_face"],
        "branch": branch,
        "branch_discriminant": core["branch_discriminant"],
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": {},
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
    deposit["determinism"] = {
        "form": run_form,
        "decodes": {"pass1_S0_cells": 144, "pass2_S1_cells": 144,
                    "canary_redecodes": len(core["canary"])},
        "canary": core["canary"],
        "canary_bit_identical": bool(
            all(c["bit_identical"] for c in core["canary"])),
        "lock_reads": f"{core['lock_reads']} == 288 (the canary re-reads "
                      "truncated, disclosed)",
        "integrity_sha256_pass1": core["integrity_shas"]["pass1"],
        "integrity_sha256_pass2": core["integrity_shas"]["pass2"],
        "integrity_sections_bit_identical": bool(
            core["integrity_shas"]["pass1"]
            == core["integrity_shas"]["pass2"]),
        "payload_sha256_pass1": sa,
        "payload_sha256_pass2": sb}
    gates = {
        "G1_the_anchors_and_floors": {
            "pass": g1_pass,
            "counts": g1,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "s0_anchor": (
                "H0-S0's errs reproduce exp256's deposited substituted "
                "errs bit-exact (72/72, the verified flags 72/72) AND "
                "exp282's walk_end_rms bit-exact (walk_end + trace "
                "sha256 + err_exact 72/72 — the SAME walk exp282 "
                "deposited; the commit-layer digests vs exp287/exp288 "
                "recorded audit-only); H1-S0's errs + trace shas "
                "reproduce exp289's deposited g=1.0 rows bit-exact "
                "(72/72); H0-S1's errs reproduce exp290's deposited A1 "
                "errs bit-exact (72/72, the fresh trace shas + floor "
                "schedules matching the deposit audit-only); the floor "
                "asserts: the -35.0 pin during the walk in the S1 "
                "cells 144/144, the -60.0 encode in the S0 cells "
                "144/144, the -60.0 settle/decode everywhere 288/288 "
                "— recorded per row, asserted fail=STOP"),
            "deposit_count_disclosure": (
                "the pre-registered text says '8 deposits' but names "
                "nine — the body implements the named list (9)")},
        "G2_new_cell_integrity": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "the H1-S1 cell (the register ON at g=1.0 + the "
                "write-time -35.0 pin during the walk only), 72 rows, "
                "fail=STOP per row: the errs finite; the A3 convention "
                "round(err_exact, 2) == the reported err; the trace "
                "lengths == walk_steps; the commit counts == "
                "walk_steps; the register's replay equality (exp289's "
                "G2 form — the register IS the commit sequence stored "
                "incrementally, under stress too); the population "
                "path's stress-independence asserted (the stream face: "
                "the commit-index digests + walk_steps + n_commits "
                "identical across ALL FOUR cells 72/72; the blend-plan "
                "face: the blend count + the blend-index digest "
                "identical across the two H1 cells 72/72); the S* lock "
                "reads 288 (4 cells x 72 — the canary re-reads "
                "truncated, disclosed)")},
        "G3_protection_branch": {
            "pass": g3_pass,
            "bars": (
                "P = [mean_err(H0-S1) - mean_err(H1-S1)] - "
                "[mean_err(H0-S0) - mean_err(H1-S0)] vs the pre-named "
                "PROTECT_BAR 0.05 mV: PROTECTED iff P >= 0.05; "
                "AMPLIFIED iff P <= -0.05; else ADDITIVE (the honest "
                "null). Audit-only, never gating: the per-host P (the "
                "outliers H3/H5 disclosed), the worst-err per cell vs "
                "the 6.0 bar (unchanged), the commit src censuses per "
                "cell (the floor's effect on the (e) branch, exp290's "
                "disclosed form)"),
            "resolved": {"branch": branch, "P": P,
                         "cell_means": prot["cell_means"],
                         "per_host_P": prot["per_host_P"],
                         "outliers_H3_H5": prot["outliers_H3_H5"]}},
        "G4_discipline": {
            "pass": None}}   # filled after the floor-exit assert
    n_pass = 0
    n_refute = 0
    for name in ("G1_the_anchors_and_floors", "G2_new_cell_integrity",
                 "G3_protection_branch"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    # ---- the floor restore + the exit asserts (G4: NEURAL_SPEC_MIN ==
    #      -60.0 asserted at exit; the docstring + header re-checked) ----
    set_floor(PROD_FLOOR)
    floor_exit = read_floor()
    assert floor_exit == PROD_FLOOR, "floor drift at exit"
    _exit_checks()
    gates["G4_discipline"] = {
        "pass": bool(canary_bit_identical
                     and no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged and floor_exit == PROD_FLOOR),
        "determinism_canary_bit_identical": canary_bit_identical,
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_15dab43": docstring_ok,
        "header_byte_unchanged_vs_15dab43": header_ok,
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

    print(f"\n  G1 the anchors + the floor asserts + the deposits: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the 12 bases rebuilt sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the canon "
          f"identity {g1['n_canon_ok']}/12 + H0 == H1 + f_max "
          f"{g1['n_fmax_ok']}/12; THE ANCHORS — H0-S0 == exp256's errs "
          f"bit-exact {g1['n_h0s0_err_ok']}/72 (the verified flags "
          f"{g1['n_h0s0_verified_ok']}/72, exp282's walks "
          f"{g1['n_walk282_ok']}/72 + trace shas {g1['n_trace282_ok']}"
          f"/72), H1-S0 == exp289's g=1.0 errs + trace shas "
          f"{g1['n_h1s0_err_ok']}/72 + {g1['n_h1s0_trace_sha_ok']}/72, "
          f"H0-S1 == exp290's A1 errs {g1['n_h0s1_err_ok']}/72; the "
          f"floor: the S1 walk pin {g1['n_floor_walk_s1_ok']}/144, the "
          f"S0 encode -60.0 {g1['n_floor_encode_s0_ok']}/144, the "
          f"settle/decode -60.0 {g1['n_floor_settle_decode_ok']}/288; "
          f"9 deposits READ-ONLY byte-unchanged: {ro_unchanged})")
    print(f"  G2 the new cell's integrity (H1-S1): "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(finite errs {g2['n_finite_err']}/72, A3 {g2['n_a3_ok']}/72, "
          f"trace lengths {g2['n_trace_len_ok']}/72, commit counts "
          f"{g2['n_commits_count_ok']}/72, the register's replay "
          f"equality {g2['n_register_replay_ok']}/72, the stream face "
          f"{g2['n_stream_ok_rows']}/72, the blend-plan face "
          f"{g2['n_blend_plan_ok']}/72; the S* lock reads "
          f"{g2['n_lock_reads']}/288)")
    print("  G3 the protection read (P = the 2x2 interaction; the "
          "pre-named PROTECT_BAR 0.05 mV):")
    cm = prot["cell_means"]
    print(f"      cell means: H0-S0 {cm['H0-S0']:.4f} | H1-S0 "
          f"{cm['H1-S0']:.4f} | H0-S1 {cm['H0-S1']:.4f} | H1-S1 "
          f"{cm['H1-S1']:.4f}")
    print(f"      P {prot['P']:+.4f} mV | stress without the register "
          f"{prot['stress_degradation_no_register']:+.4f} | stress with "
          f"the register {prot['stress_degradation_with_register']:+.4f}"
          f" | register without stress "
          f"{prot['register_improvement_no_stress']:+.4f} | register "
          f"under stress "
          f"{prot['register_improvement_under_stress']:+.4f}")
    for h in hosts:
        ph = prot["per_host_P"][h]
        tag = " <== outlier" if h in outliers else ""
        print(f"      {h:4s} P {ph['P']:+.4f}{tag}")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(the determinism canary: "
          f"{gates['G4_discipline']['determinism_canary_bit_identical']}, "
          f"form {run_form}; no wall-clock fields: {no_wall_clock}; "
          f"docstring+header pinned to 15dab43; exp142 + the core NOT "
          f"modified; floor at exit "
          f"{gates['G4_discipline']['floor_at_exit']})")
    print(f"\n  BRANCH: {branch} | P {P:+.4f} mV | the bar "
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
