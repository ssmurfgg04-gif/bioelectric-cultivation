#!/usr/bin/env python3
"""exp289 — THE HISTORY-REGISTER PORT: GIVING THE DORMANT CHANNELS A
STATE VARIABLE THAT SURVIVES THE WALK (batch 47; ledger L267's
registered next (b) — Sediqi 2026 (bioRxiv 2026-06-23.733978: ionic-
exposure HISTORY shapes voltage/chromatin responses) converges with
Blattner-TAS 2026 (bioRxiv 2026-04-03.715890, github.com/marcelbtec/
tasmorpho: regeneration = a HIDDEN bioelectric state invisible in the
current anatomy) on one architectural move: the programs' writes need
a persistent register. exp288 landed SPEC-UNIFORM — the spec layer's
face is class-blind like every other level — so the frontier is NOT
geometric; L267's (a): the five dormant channels (ctx / pair /
structure / ca2 / apop, exp258/259/260/261/263/264) are inert under
SCHEMA-ONLY activation — the schema carries them, no evolution rule
acts on them. THE MISSING VARIABLE this module ports: the commit
HISTORY — what the program wrote LAST time, carried across walks as
a state variable the dynamics can read.)

THE PORT (additive, zero-knob at defaults): a new per-cell register
`phi_history` on the collective (the 8-channel named array's history
face — the channel values as of the LAST write), populated AT EACH
commit write (the traced replica's disclosed addition (f) site: after
c.theta[i] = theta_new, phi_history[i] = theta_new), initialized to
the spec layer's own values at write_spec_layer time (the history
starts as the program's own target — the never-written cells' history
IS the spec's install). NOTHING reads phi_history at defaults — the
register is recorded, never consumed — so EVERY legacy call site is
bit-exact by construction. G1 PROVES it on the machinery's own anchor:
the full 72-row substituted battery (12 hosts x 3 seeds x r-60i0/r-60i1
at n=400, exp256's battery, the exp287/exp288 traced replica form at
the production budget 8) re-run with the port live reproduces exp256's
deposited substituted errs BIT-EXACT 72/72 (the verified flags 72/72)
— the same S0 anchor discipline as exp287/exp288, now proving the
PORT side-effect-free (plus the repo test suite green from the repo
root).

THE FIRST HISTORY-CARRYING ACTIVATION (ch3 ctx, exp258's registered
channel, its landed form's registered next): the ctx coupling term
re-run reading the HISTORY register — the cell pulled toward its OWN
last commit (the self-history face) instead of the interior context.
The grid is exp258's VERBATIM {0, 0.25, 0.5, 1.0} (g_ctx), zero new
knobs, on the same 72-row battery shape (the grid multiplies the
battery: 4 grid points x 72 rows = 288 decodes per arm-set; the
g=0.0 point IS the schema-only arm — the within-run control, asserted
bit-exact vs the G1 anchor's errs).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE PORT'S ZERO-DELTA AT DEFAULTS: the 72-row battery with the
      register live reproduces exp256's deposited substituted errs
      BIT-EXACT 72/72 (the verified flags 72/72) AND exp282's
      walk_end_rms bit-exact 72/72 (the trace sha256 72/72 — the same
      walk discipline); the register's PRESENCE asserted (the
      attribute exists, the values finite, the init == the spec's
      install bit-exact at the walk's start — asserted per row);
      the repo test suite green (python3 -m tests.run_tests from the
      repo root, the shadow path disclosed); exp142 NOT modified.
  G2  THE HISTORY POPULATED (zero-knob asserted, fail=STOP per row):
      at the walk's end phi_history[write_set] == the commit replay's
      values BIT-EXACT per row (the register IS the commit sequence
      stored incrementally — the same replay exp287/exp288 anchored,
      now read from the register); the register's non-write-set cells
      == the spec install (the never-written cells' history is the
      spec layer); the register finite 72/72.
  G3  THE ACTIVATION BRANCH (pre-named numeric bars): per grid point
      g in {0.25, 0.5, 1.0} the 72-row battery re-run with the ctx
      coupling reading phi_history; per host the 6-row mean err; the
      branch HISTORY-CARRIED iff EXISTS a grid point g > 0 with the
      mean err IMPROVED vs the g=0.0 within-run control on >= 10/12
      hosts (the improvement bar: the per-host mean delta < 0.0 —
      strict, disclosed); else HISTORY-INERT (the exp258 verdict's
      form: degradation or no improvement). Audit-only: the per-host
      per-grid delta table, the worst-err per grid point vs the 6.0
      bar (unchanged), the exp288 pooled-R_max face re-computed at
      the best grid point (the class-blindness re-read under the
      history — audit-only, never gating).
  G4  THE DISCIPLINE: deterministic one-pass per grid point (the
      port is a state register, not a second RNG consumer — the
      stream UNTOUCHED, asserted via G1's bit-exact errs); no
      wall-clock fields; the docstring + header pinned to this
      pre-registration commit, asserted at entry AND exit; the
      source deposits READ-ONLY (exp243/256/272/273/282/287/288);
      NEURAL_SPEC_MIN == -60.0 asserted at exit (the exp169-import
      discipline; the -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): HISTORY-CARRIED / HISTORY-INERT.

RUN: the G1 anchor pass (72 decodes ~ 60-90 s) + the G2 asserts
(free) + the G3 grid (3 x 72 decodes ~ 3-5 min) — one invocation,
~4-7 min, UNDER the 570 s cap only in the checkpoint-split form
EXP289_MODE=pass1 (G1+G2) | pass2 (G3) | merge; the default
in-process form runs the whole sequence and may exceed the cap —
the pre-named form for the sandbox is the checkpoint split; the
pre-named form for the GitHub runners (30-min) is the in-process
default. Both forms evaluate the SAME gates and assert the same
bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp289_history_register.json")


def main() -> dict:
    # ==== BODY (written under the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 982cb81; gates G1-G4
    #      evaluated exactly once) ========================================
    import hashlib
    import json
    import subprocess

    import numpy as np

    import cultivation.bioelectric.collective as CORE  # the floor's home + THE PORT
    import experiments.exp142_sign_read as _m142       # the walk's home — NOT modified
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
        "a9946b0bae54333a59779bc33a84476a2ac491aff4d93758d2a2eb33210df69b")
    EXPECTED_HEADER_SHA256 = (
        "04afe95ac0a247831fa0ca40c1c77e31e875bf399995c72d63a70a6bce83c23d")
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

    # ---- the -60.0 floor (G4: asserted at exit; the exp169-import
    #      discipline — the whole reader chain imported FIRST, every
    #      pinned floor import restored to -60.0 after; the -35.0
    #      reader-line pin disclosed) -------------------------------------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    # ---- the frozen read configuration (exp256's battery constants;
    #      the replica's executor constants asserted = exp142's own;
    #      THE GRID + THE BRANCH BARS — pre-named) -------------------------
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
    # STEPS_PER_CELL == 8 (the exp287/exp288 traced replica form).
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE GRID (exp258's VERBATIM g_ctx dial; g = 0.0 IS the schema-only
    # arm — the within-run control)
    G_CTX_GRID = (0.0, 0.25, 0.5, 1.0)
    G_ACTIVE = (0.25, 0.5, 1.0)
    # THE BRANCH BARS (pre-named at 982cb81, numeric, never fit)
    HISTORY_MIN_HOSTS = 10
    # exp288's pooled-R_max audit bars (the class-blindness re-read —
    # audit-only, never gating)
    CONC_BAR = 1.50
    CONC_MIN_HOSTS = 10
    # the commit source tags (the pre-named census)
    COMMIT_SOURCES = ("spec", "canon", "parent")
    # the three clean classes (exp208's classify labels; cls 2 = INTERIOR
    # never occurs — the exp277/exp284 disclosure, asserted on the grid)
    CLASS_NAMES = {0: "canon_boundary", 1: "pair_junction", 2: "interior"}

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

    # ---- the port's own provenance: the ported file's bytes + the
    #      zero-reader scan (NOTHING reads phi_history at defaults —
    #      the code-level face complementing G1's bit-exact proof) ------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)

    def _zero_reader_scan():
        """Scan the package + the walk's home for phi_history touches:
        every occurrence must live in the ported collective.py (the
        register's init + the commit-write population + their comments)
        or in THIS module (the instrument). No reader anywhere else."""
        hits = {}
        for base in ("cultivation", "experiments"):
            root = os.path.join(ROOT, base)
            for dirpath, _dirs, files in os.walk(root):
                if "__pycache__" in dirpath:
                    continue
                for fn in files:
                    if not fn.endswith(".py"):
                        continue
                    p = os.path.join(dirpath, fn)
                    with open(p, "r", encoding="utf-8") as fh:
                        txt = fh.read()
                    cnt = txt.count("phi_history")
                    if cnt:
                        hits[os.path.relpath(p, ROOT)] = cnt
        allowed = {"cultivation/bioelectric/collective.py",
                   "experiments/exp289_history_register.py"}
        unexpected = sorted(set(hits) - allowed)
        assert not unexpected, \
            f"phi_history touched outside the port + the instrument: " \
            f"{unexpected}"
        return {"files_with_phi_history": hits,
                "files_outside_port_and_instrument": unexpected,
                "readers_at_defaults": 0}

    zero_reader_scan = _zero_reader_scan()

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
    assert dep272["descriptive"]["premium_hosts"] == outliers, \
        "exp272's premium_hosts drifted from the outlier pre-name"
    assert dep282["outliers"] == outliers, "exp282's outliers drifted"
    cluster = [h for h in hosts if h not in outliers]
    assert len(cluster) == 10, "the ten-host cluster drifted"

    rec272 = {r["host"]: r for r in dep272["per_host"]}
    ft273 = {rec["field"]: rec for rec in dep273["field_table"]}

    # ---- exp208's classify VERBATIM (the CLEAN masks; used by the
    #      activation's class plan (exp258's form) and by the grid's
    #      pooled-R_max audit face) ---------------------------------------
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

    # ---- THE TRACED REPLICA: exp286's/exp287's/exp288's landed
    #      _execute_signed_traced REUSED VERBATIM (exp142's walk
    #      byte-similar + the disclosed recording additions (a)-(f)) with
    #      exactly TWO exp289 additions, both disclosed, both pure:
    #      (g) THE PORT'S REGISTER, LIVE: the presence + the init
    #          asserted at the walk's start (write_spec_layer installed
    #          it — collective.py's additive site), and the register
    #          POPULATED AT EACH COMMIT WRITE (after the write,
    #          phi_history[i] = the written value — the (f)-site analog;
    #          a pure recording of already-computed values — the RNG
    #          stream and the state untouched, proven by G1's bit-exact
    #          anchors), and the register's SURVIVAL asserted at the
    #          walk's end (the replay equality + the spec-install
    #          complement — G2's face, read from the register);
    #      (h) THE ACTIVATION (the ONLY deviation; ZERO at g_ctx == 0.0):
    #          exp258's ctx coupling term re-run reading the HISTORY
    #          register — the cell pulled toward its OWN last commit
    #          (the self-history face) instead of the interior context;
    #          exp258's VERBATIM structure (the canon-boundary class
    #          restriction, the blend site, the pre-named g_ctx grid),
    #          the read source swapped to the register. At g_ctx == 0.0
    #          the replica takes the verbatim path with ZERO deviation. --
    def _execute_signed_traced(spec, adjacency, seed, op, budget,
                               g_ctx=0.0, a_base=None):
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
        # ---- (g) the register's PRESENCE + INIT at the walk's start
        #      (G1, fail=STOP per row): the attribute exists and the
        #      init == the spec's install BIT-EXACT ------------------------
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
                    "reg_init_ok": reg_init_ok}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
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
        n_hist_writes = 0                      # (h) the activation count
        # (h) the activation's class plan (exp258's form: exp208's
        # classes on the plan; T and A_base are g-independent, so the
        # row sets match 1:1 across the whole grid). Computed ONLY when
        # the coupling is armed — zero deviation at g_ctx == 0.0.
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
        for i, src in order:
            for _ in range(budget):                  # the landed
                c.step(dt)                           # parameterization
            canon_src = getattr(c, "phi_spec_canon", None)
            if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:       # (e)
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "spec"
            elif canon_src is not None:
                theta_new = canon_src[i] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "canon"
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
                src_tag = "parent"
            # ---- (h) THE ACTIVATION: the self-history blend (ZERO at
            #      g_ctx == 0.0) — exp258's canon-boundary restriction
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
            #      write; the inherited/committed theta per cell; a pure
            #      recording of already-computed values) -----------------
            commits.append((int(i), float(written), src_tag))
            # ---- (g) THE PORT'S POPULATION: after the write the
            #      register holds the committed value — the commit
            #      sequence stored incrementally (a pure recording; the
            #      RNG stream and the dynamics untouched) ----------------
            c.phi_history[i] = written
            if g_ctx > 0.0 and cls[i] == 0:
                n_hist_writes += 1
            # ---- (a) the per-step RMS read (a pure read; the walk's
            #      full-frame convergence; unchanged) -----------------
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        # the write-set coverage (the replica's side, the walk order in
        # scope): the commit sequence elementwise == the walked order
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        c.run(15.0, dt=dt)
        # ---- (g) THE REGISTER AT THE WALK'S END (G2, fail=STOP per
        #      row): the register SURVIVED the walk + the settle; on the
        #      write set it IS the commit replay BIT-EXACT; off the
        #      write set it IS the spec's install (the never-written
        #      cells' history); finite everywhere -------------------------
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
        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced + budgeted + register-
    #      live executor call) -------------------------------------------
    def _scoped_row_read_traced(spec, med, seed, fmax, budget,
                                g_ctx=0.0, a_base=None):
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
            out = _execute_signed_traced(spec, A_ext, seed, op=STAR_OP,
                                         budget=budget, g_ctx=g_ctx,
                                         a_base=a_base)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one ANCHOR-row decode (pass 1: the S0 anchors + the register
    #      face, asserted fail=STOP on EVERY row; the battery runs at
    #      the production budget with the register live, g_ctx == 0.0) --
    def _decode_anchor_row(host, row_key, spec, med, seed, fmax, dep_rec,
                           rec282, rec287):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET)
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
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            f"{host} {row_key} s{seed}: the convergence point does not exist"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        # ---- THE COMMIT RECORDING bookkeeping (the exp287 form) --------
        commits = out["commits"]
        n_commits = len(commits)
        commits_count_ok = bool(n_commits == steps == len(trace))
        assert commits_count_ok, \
            (f"{host} {row_key} s{seed}: the commit count {n_commits} != "
             f"walk steps {steps} — the write set is not fully recorded")
        idxs = [int(rec[0]) for rec in commits]
        commits_unique_ok = bool(len(set(idxs)) == n_commits)
        assert commits_unique_ok, \
            (f"{host} {row_key} s{seed}: a committed cell written twice")
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
        # the exp287 replay reads (the anchor's cvt/sc faces)
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        assert np.isfinite(sc_rms), \
            f"{host} {row_key} s{seed}: non-finite self-consistency RMS"
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite commit-vs-target RMS"
        sc_frac = float(sc_rms / err_exact)

        # ---- THE REGISTER FACE (G1's presence + G2's replay, from the
        #      replica's own fail=STOP asserts; the flags + the digest
        #      recorded per row) ------------------------------------------
        reg = {"present_ok": bool(out["reg_present_ok"]),
               "init_ok": bool(out["reg_init_ok"]),
               "replay_ok": bool(out["reg_replay_ok"]),
               "complement_ok": bool(out["reg_complement_ok"]),
               "finite_ok": bool(out["reg_finite_ok"]),
               "phi_history_sha256": str(out["phi_history_sha256"])}
        assert reg["present_ok"] and reg["init_ok"], \
            f"{host} {row_key} s{seed}: the register's presence/init drifted"

        # ---- THE S0 ANCHOR (G1, fail=STOP): the production-budget
        #      re-run WITH THE REGISTER LIVE reproduces exp256's
        #      deposited errs, exp282's walks AND exp287's commit layer
        #      BIT-EXACT — the port is side-effect-free -------------------
        s0_err_ok = bool(err == dep_rec["err"])
        s0_ver_ok = bool(bool(out["program_verified"])
                         == bool(dep_rec["verified"]))
        assert s0_err_ok, \
            (f"{host} {row_key} s{seed}: the fresh err {err} drifted from "
             f"exp256's deposited {dep_rec['err']} — S0 REFUTED under the "
             f"port")
        assert s0_ver_ok, \
            f"{host} {row_key} s{seed}: the verified flag drifted"
        we_ok = bool(final == float(rec282["walk_end_rms"]))
        assert we_ok, \
            (f"{host} {row_key} s{seed}: the fresh walk_end_rms drifted "
             "from exp282's deposited walk_end_rms")
        ts_ok = bool(trace_sha == rec282["trace_sha256"])
        assert ts_ok, \
            (f"{host} {row_key} s{seed}: the fresh trace sha drifted from "
             "exp282's deposited trace sha — the walk is not the traced "
             "one (the register population was NOT side-effect-free)")
        ee_ok = bool(err_exact == float(rec282["err_exact"]))
        assert ee_ok, \
            (f"{host} {row_key} s{seed}: the fresh err_exact drifted from "
             "exp282's deposited err_exact")
        cs287_ok = bool(commit_sha == rec287["commit_seq_sha256"])
        assert cs287_ok, \
            (f"{host} {row_key} s{seed}: the fresh commit-sequence digest "
             "drifted from exp287's deposited commit_seq_sha256 — the "
             "commit layer is not the recorded one")
        cvt287_ok = bool(cvt_rms == float(rec287["cvt_rms"]))
        assert cvt287_ok, \
            (f"{host} {row_key} s{seed}: the fresh cvt_rms drifted from "
             "exp287's deposited cvt_rms")
        nc287_ok = bool(n_commits == int(rec287["n_commits"]))
        assert nc287_ok, \
            (f"{host} {row_key} s{seed}: the fresh n_commits drifted from "
             "exp287's deposited n_commits")
        sc287_ok = bool(sc_rms == float(rec287["sc_rms"]))
        assert sc287_ok, \
            (f"{host} {row_key} s{seed}: the fresh sc_rms drifted from "
             "exp287's deposited sc_rms")

        rec = {"host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "err": err,
               "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "n_commits": n_commits,
               "coverage_ok": coverage_ok,
               "commits_count_ok": commits_count_ok,
               "commits_unique_ok": commits_unique_ok,
               "commits_finite_ok": commits_finite_ok,
               "census_ok": census_ok,
               "commit_seq_sha256": commit_sha,
               "src_census": census_src,
               "sc_rms": sc_rms, "sc_frac": sc_frac, "cvt_rms": cvt_rms,
               "s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
               "walk_end_282_ok": we_ok, "trace_sha_282_ok": ts_ok,
               "err_exact_282_ok": ee_ok,
               "commit_sha_287_ok": cs287_ok, "cvt_287_ok": cvt287_ok,
               "n_commits_287_ok": nc287_ok, "sc_287_ok": sc287_ok,
               "register": reg,
               "n_hist_writes": int(out["n_hist_writes"])}
        return rec

    # ---- one GRID-row decode (pass 2: the activation at g_ctx > 0;
    #      the register + commit bookkeeping asserted fail=STOP; the
    #      exp288 class decomposition carried for the pooled-R_max audit
    #      face; the S0 anchors DO NOT apply at g > 0 — the blend is the
    #      pre-named deviation — and the structural stream face (the
    #      walked count, the commit count, the draw positions) is
    #      asserted against the anchor at the merge) ----------------------
    def _decode_grid_row(host, row_key, spec, med, seed, fmax, g, A_base):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET,
                                      g_ctx=g, a_base=A_base)
        err = float(out["err_vs_target"])
        assert np.isfinite(err), \
            f"{host} {row_key} s{seed} g{g}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, f"{host} {row_key} s{seed} g{g}: A3 drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        trace_len_ok = bool(len(trace) == steps and steps >= 1)
        assert trace_len_ok, \
            f"{host} {row_key} s{seed} g{g}: trace len != walk steps"
        assert all(np.isfinite(trace)), \
            f"{host} {row_key} s{seed} g{g}: non-finite trace entry"
        final = trace[-1]
        assert final > 0.0, f"{host} {row_key} s{seed} g{g}: final RMS == 0"
        thresh = 2.0 * final
        conv = None
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        assert conv is not None and 0 <= conv < steps, \
            f"{host} {row_key} s{seed} g{g}: no convergence point"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps == len(trace), \
            f"{host} {row_key} s{seed} g{g}: the commit count drifted"
        idxs = [int(rec[0]) for rec in commits]
        assert len(set(idxs)) == n_commits, \
            f"{host} {row_key} s{seed} g{g}: a cell written twice"
        assert bool(out["coverage_ok"]), \
            f"{host} {row_key} s{seed} g{g}: the coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        assert all(np.isfinite(v) for v in vals), \
            f"{host} {row_key} s{seed} g{g}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        assert sum(census_src.values()) == n_commits, \
            f"{host} {row_key} s{seed} g{g}: the census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed} g{g}: non-finite cvt_rms"

        # ---- the register face at the grid point (the same fail=STOP
        #      asserts inside the replica; the flags recorded) -----------
        reg = {"present_ok": bool(out["reg_present_ok"]),
               "init_ok": bool(out["reg_init_ok"]),
               "replay_ok": bool(out["reg_replay_ok"]),
               "complement_ok": bool(out["reg_complement_ok"]),
               "finite_ok": bool(out["reg_finite_ok"]),
               "phi_history_sha256": str(out["phi_history_sha256"])}
        assert all(reg[k] for k in
                   ("present_ok", "init_ok", "replay_ok",
                    "complement_ok", "finite_ok")), \
            f"{host} {row_key} s{seed} g{g}: the register face drifted"

        # ---- THE CLASS DECOMPOSITION (exp288's read (2) form, carried
        #      for the pooled-R_max audit face at the best grid point;
        #      exp208's classify VERBATIM applied per instance) ----------
        masks = classify(T, A_base)
        bnd, jct, intr = masks["boundary"], masks["junction"], \
            masks["interior"]
        masks_disjoint_ok = bool(
            int((bnd & jct).sum()) == 0 and int((bnd & intr).sum()) == 0
            and int((jct & intr).sum()) == 0 and bool((bnd | jct | intr).all()))
        assert masks_disjoint_ok, \
            f"{host} {row_key} s{seed} g{g}: the clean masks drifted"
        cls_arr = masks["class"]
        assert int((cls_arr == 2).sum()) == 0, \
            f"{host} {row_key} s{seed} g{g}: the cls-2 disclosure drifted"
        e = replay_val - T[replay_idx]
        n_write = int(len(e))
        total_sq = float((e ** 2).sum())
        cls_of_write = cls_arr[replay_idx]
        decomp = []
        fracs_sum = 0.0
        sum_sq_total = 0.0
        for cidx in (0, 1, 2):
            sel = cls_of_write == cidx
            n_c = int(sel.sum())
            if n_c > 0:
                sum_sq_c = float((e[sel] ** 2).sum())
                frac_c = float(sum_sq_c / total_sq)
                share_c = float(n_c / n_write)
                R_c = float(frac_c / share_c)
            else:
                sum_sq_c = 0.0
                frac_c = 0.0
                share_c = 0.0
                R_c = None
            fracs_sum += frac_c
            sum_sq_total += sum_sq_c
            decomp.append({"cls": int(cidx),
                           "name": CLASS_NAMES[cidx], "n": n_c,
                           "cell_share": share_c, "sum_sq": sum_sq_c,
                           "frac_of_sq": frac_c, "R": R_c})
        ident_ok = bool(
            abs(sum_sq_total / n_write - cvt_rms ** 2)
            <= 1e-6 * max(1.0, cvt_rms ** 2))
        assert ident_ok, \
            f"{host} {row_key} s{seed} g{g}: the accounting identity drifted"
        fracs_ok = bool(abs(fracs_sum - 1.0) <= 1e-9)
        assert fracs_ok, \
            f"{host} {row_key} s{seed} g{g}: the class fracs drifted"
        partition_ok = bool(sum(d["n"] for d in decomp) == n_write)
        assert partition_ok, \
            f"{host} {row_key} s{seed} g{g}: the partition drifted"

        rec = {"host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "g_ctx": float(g), "pert": P3, "medium": "base",
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "n_commits": n_commits,
               "coverage_ok": bool(out["coverage_ok"]),
               "commit_seq_sha256": commit_sha,
               "src_census": census_src,
               "cvt_rms": cvt_rms,
               "n_hist_writes": int(out["n_hist_writes"]),
               "register": reg,
               "masks_disjoint_ok": masks_disjoint_ok,
               "decomp": decomp, "accounting_ok": ident_ok,
               "fracs_ok": fracs_ok, "partition_ok": partition_ok,
               "n_write": n_write, "sum_e": float(e.sum()),
               "sum_sq_e": total_sq}
        return rec

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; exp288's 25 records + exp288's own inputs record
    #      (6 sha records) = 31) -------------------------------------------
    CHAIN_FILE = {
        "exp202": "exp202_cross_organism_carriage.json",
        "exp198": "exp198_adversarial_reader_n400.json",
        "exp225": "exp225_structured_media_reader.json",
        "exp255": "exp255.json",
        "exp243": "exp243_structured_adversarial.json",
        "exp182": "exp182_substrate_100.json",
        "exp243_deposit": "exp243_structured_adversarial.json",
        "exp256_deposit": "exp256_row_pair_regression.json",
        "exp272_deposit": "exp272_host_premium_structure.json",
        "exp273_deposit": "exp273_outlier_hosts.json",
        "exp282_deposit": "exp282_trajectory_structure.json",
        "exp287_deposit": "exp287_fixed_point_identity.json",
        "exp288_deposit": "exp288_spec_layer_face.json",
        "exp277_deposit": "exp277_deep_band_break_face.json",
        "exp271_deposit": "exp271_one_zone_premium.json",
        "exp182_deposit": "exp182_substrate_100.json",
        "exp274_deposit": "exp274_premium_mechanism.json",
        "exp275_deposit": "exp275_audit_direction.json",
        "exp270_deposit": "exp270_structural_dose.json"}
    CHAIN_SOURCES = (
        ("exp243_structured_adversarial.json", "provenance"),
        ("exp256_row_pair_regression.json", "provenance"),
        ("exp272_host_premium_structure.json", "inputs"),
        ("exp273_outlier_hosts.json", "inputs"),
        ("exp282_trajectory_structure.json", "inputs"),
        ("exp287_fixed_point_identity.json", "inputs"),
        ("exp288_spec_layer_face.json", "inputs"))

    def _verify_chains():
        cur = {}
        report = []
        total = 0
        ok_total = 0
        for fname, rkey in CHAIN_SOURCES:
            with open(os.path.join(ROOT, "results", fname)) as fh:
                rec = json.load(fh)[rkey]
            n_rec = 0
            n_ok = 0
            for k, v in rec.items():
                if isinstance(v, dict):
                    v = v.get("sha256")
                if not (isinstance(v, str) and len(v) == 64):
                    continue
                n_rec += 1
                target = CHAIN_FILE[k]
                if target not in cur:
                    cur[target] = _sha(os.path.join(ROOT, "results",
                                                    target))
                good = bool(v == cur[target])
                n_ok += int(good)
                assert good, \
                    f"chain drift: {fname} {rkey}.{k} vs {target}"
            total += n_rec
            ok_total += n_ok
            report.append({"deposit": fname, "record": rkey,
                           "n_records": n_rec, "n_verified": n_ok})
        assert total == 31, f"the chain record count {total} != 31"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

    # ---- THE SHADOW TEST SUITE (G1: python3 -m tests.run_tests from
    #      the repo root; THE SHADOW PATH DISCLOSED: the suite runs in a
    #      separate interpreter — a shadow process importing the ON-DISK
    #      ported collective.py — so the additive port's legacy-call-site
    #      proof is made against the file this commit ships, not against
    #     this process's pinned in-memory state; the subprocess's own
    #      floor state is unpinned by this process) -----------------------
    def _run_test_suite():
        proc = subprocess.run(
            [sys.executable, "-m", "tests.run_tests"],
            cwd=ROOT, capture_output=True, text=True, timeout=300)
        n_pass = int(proc.stdout.count("PASS "))
        tail = [ln for ln in proc.stdout.splitlines() if ln.strip()][-3:]
        ok = bool(proc.returncode == 0)
        assert ok, (f"the repo test suite is not green under the port "
                    f"(returncode {proc.returncode}):\n{proc.stdout}\n"
                    f"{proc.stderr}")
        return {"returncode": int(proc.returncode), "n_pass_lines": n_pass,
                "tail": tail,
                "shadow_path_disclosure": (
                    "the suite ran in a shadow subprocess (a separate "
                    "interpreter launched from the repo root, importing "
                    "the on-disk ported collective.py), so the additive "
                    "port is proven against the shipped file, not this "
                    "process's pinned state; this process's floor pins "
                    "do not reach the subprocess"),
                "green": ok}

    # ---- THE REBUILD (the exp269/exp280/exp284/exp285/exp286/exp287/
    #      exp288 form VERBATIM, every rebuild bit-asserted against
    #      exp243's OWN records; shared by both passes — deterministic) --
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_bnd_dual_ok": 0, "n_canon_ok": 0,
                  "h0_echo_h1": False, "n_fmax_ok": 0, "n_nonneg_ok": 0,
                  "n_rows256": 0, "n_structure_ok": 0, "n_worst_eq_max": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows282": 0, "n_282_chain_ok": 0,
                  "n_host_table282_ok": 0,
                  "n_rows287": 0, "n_host_table287_ok": 0,
                  "n_rows288": 0, "n_288_chain_ok": 0,
                  "n_mia_carry": 0, "n_prem_carry": 0}
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
                nb == int(rec272[h]["n_boundary_cells_base"])
                and nb == int(ft273["exp243.classes.n_boundary_cells_base"]
                              ["values"][h]))
            assert sha_ok and edges_ok and bnd_ok and bnd_dual \
                and canon_ok, f"{h}: the rebuild drifted from exp243's records"
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
            counts["n_bnd_ok"] += int(bnd_ok)
            counts["n_bnd_dual_ok"] += int(bnd_dual)
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
                "boundary_count_matches_3way": bool(bnd_ok and bnd_dual),
                "canon_identity_ok": canon_ok,
                "f_max_matches_exp243_record": fmax_ok,
                "base_non_negative": nonneg})
        counts["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                                   bases["H1"]["A"]))
        assert counts["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        # exp256's 72 rows — the substituted records the S0 anchor reads
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
        ht282 = {row["host"]: row for row in dep282["host_table"]}
        assert len(ht282) == 12, "exp282's host table drifted"
        means282 = {h: float(ht282[h]["walk_end_rms_mean"]) for h in hosts}
        counts["n_host_table282_ok"] = len(means282)

        # THE EXP287 RE-READ (the commit-layer anchor deposit)
        rows287 = dep287["rows"]
        counts["n_rows287"] = len(rows287)
        assert len(rows287) == 72, "exp287's 72-row deposit drifted"
        r287 = {}
        for r in rows287:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r287, f"duplicate exp287 row {key}"
            assert all(fld in r for fld in
                       ("commit_seq_sha256", "cvt_rms", "n_commits",
                        "sc_rms")), \
                f"{key}: exp287's row record is missing anchor fields"
            r287[key] = r
        ht287 = {row["host"]: row for row in dep287["host_table"]}
        assert len(ht287) == 12, "exp287's host table drifted"
        mean_cvt287 = {h: float(ht287[h]["mean_cvt"]) for h in hosts}
        counts["n_host_table287_ok"] = len(mean_cvt287)

        # THE EXP288 RE-READ (the SPEC-UNIFORM face deposit: the branch,
        # the per-host pooled R_max, and its own fresh errs == exp256's
        # — the deposited chain face of the immediately prior batch)
        rows288 = dep288["rows"]
        counts["n_rows288"] = len(rows288)
        assert len(rows288) == 72, "exp288's 72-row deposit drifted"
        assert dep288["branch"] == "SPEC-UNIFORM", \
            "exp288's deposited branch drifted from SPEC-UNIFORM"
        n_chain288 = 0
        for r in rows288:
            key = (r["host"], int(r["seed"]), r["row_key"])
            d256 = dep_sub[key]
            ok_chain = bool(float(r["err"]) == d256["err"])
            assert ok_chain, \
                (f"{key}: exp288's deposited err drifted from exp256's "
                 "deposited substituted err")
            n_chain288 += int(ok_chain)
        counts["n_288_chain_ok"] = n_chain288
        assert counts["n_288_chain_ok"] == 72, \
            "exp288's err chain anchor drifted"
        rmax288 = {h: float(dep288["branch_discriminant"]
                            ["per_host_R_max"][h]) for h in hosts}
        pooled288 = {h: [{"cls": p["cls"], "name": p["name"],
                          "n": p["n"], "cell_share": p["cell_share"],
                          "frac_of_sq": p["frac_of_sq"], "R": p["R"]}
                         for p in dep288["branch_discriminant"]
                         ["per_host_pooled_classes"][h]]
                     for h in hosts}

        # THE TARGETS (the pre-named carries, asserted bit-exact)
        mia = dict(ft273["exp243.classes.multi_identity_audit.prod_err"]
                   ["values"])
        assert set(mia) == set(hosts), "the mia field table drifted"
        for h in hosts:
            ok = bool(mia[h] == float(
                dep243["classes"][h]["multi_identity_audit"]["prod_err"]))
            assert ok, f"{h}: the mia carry drifted from exp243's records"
            counts["n_mia_carry"] += int(ok)
        prem = {h: float(rec272[h]["one_zone_premium_mean"])
                for h in hosts}
        prem_dep = dict(ft273["exp272.per_host.one_zone_premium_mean"]
                        ["values"])
        for h in hosts:
            ok = bool(prem[h] == float(prem_dep[h]))
            assert ok, f"{h}: the premium carry drifted from exp273's"
            counts["n_prem_carry"] += int(ok)
        assert counts["n_mia_carry"] == 12 and counts["n_prem_carry"] == 12, \
            "the target carries drifted"
        targets = {
            "mia_prod_err": {
                "source": ("exp273's field-table field "
                           "'exp243.classes.multi_identity_audit.prod_err'"),
                "values": mia, "carry_vs_exp243_bit_exact":
                    counts["n_mia_carry"]},
            "one_zone_premium": {
                "source": ("exp272's per-host one_zone_premium_mean "
                           "(the one-zone premium means)"),
                "values": prem,
                "carry_vs_exp273_field_table_bit_exact":
                    counts["n_prem_carry"]}}

        chains = _verify_chains()

        # THE PER-HOST DT RECORD (the battery's operating point, recomputed
        # OUTSIDE the replica by the same pure projection calls)
        dt_record = {}
        for h in hosts:
            med_h = HostWMedium(bases[h]["A"])
            with warnings_as_errors():
                A_proj, rho_p, br_p = project_phase_native(med_h)
                F_h = flip_clock_matrix(med_h)
            A_ext_h = A_proj + F_h
            max_deg = float(np.abs(A_ext_h).sum(axis=1).max())
            dt_h = float(star_dt(STAR_OP["gamma"], max_deg))
            dt_record[h] = {"dt": dt_h, "projected_max_degree": max_deg,
                            "proj_branch": str(br_p), "rho": float(rho_p)}

        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "counts": counts,
                "rebuild_report": rebuild_report, "targets": targets,
                "chains": chains, "dt_record": dt_record,
                "means282": means282, "mean_cvt287": mean_cvt287,
                "rmax288": rmax288, "pooled288": pooled288}

    # ---- PASS 1 (G1 + G2): the sha-asserted rebuild + the shadow test
    #      suite + the fresh 72-row battery at the production budget
    #      WITH THE REGISTER LIVE (g_ctx == 0.0) + the per-host dt record
    def _compute_pass1():
        _LOCK_LOG.clear()
        rb = _rebuild()
        suite = _run_test_suite()
        bases, dep_sub = rb["bases"], rb["dep_sub"]
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec282 = rb["r282"][(k, s, rk)]
                    rec287 = rb["r287"][(k, s, rk)]
                    rec = _decode_anchor_row(k, rk, ctx["deep"][inst]["spec"],
                                             med, s, ctx["fmax"], d,
                                             rec282, rec287)
                    rows_out.append(rec)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [pass1 {k}] 6 rows | errs {[r['err'] for r in hs]} | "
                  f"reg replay {sum(r['register']['replay_ok'] for r in hs)}"
                  f"/6 | commit digests "
                  f"{sum(r['commit_sha_287_ok'] for r in hs)}/6",
                  flush=True)
        assert len(rows_out) == 72, \
            f"pass1 produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"
        # the per-host anchor table (the control column's source)
        host_table = []
        for h in hosts:
            hs = [r for r in rows_out if r["host"] == h]
            mean_err = float(np.mean([r["err"] for r in hs]))
            mean_we = float(np.mean([r["walk_end_rms"] for r in hs]))
            mean_cvt = float(np.mean([r["cvt_rms"] for r in hs]))
            mean8_ok = bool(mean_we == rb["means282"][h])
            assert mean8_ok, \
                (f"{h}: the fresh per-host end-RMS mean drifted from "
                 "exp282's deposited")
            meancvt_ok = bool(mean_cvt == rb["mean_cvt287"][h])
            assert meancvt_ok, \
                (f"{h}: the fresh per-host mean_cvt drifted from exp287's "
                 "deposited")
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "mean_err": mean_err, "mean_walk_end_rms": mean_we,
                "mean8_equals_exp282_host_table": mean8_ok,
                "mean_cvt": mean_cvt,
                "mean_cvt_equals_exp287_host_table": meancvt_ok,
                "mean_sc": float(np.mean([r["sc_rms"] for r in hs])),
                "mean_settle_gap": float(np.mean(
                    [r["settle_gap_abs"] for r in hs])),
                "src_census": {t: int(sum(r["src_census"][t] for r in hs))
                               for t in COMMIT_SOURCES}})
        integrity = {"counts": rb["counts"],
                     "rebuild_report": rb["rebuild_report"],
                     "targets": rb["targets"],
                     "provenance_chains": rb["chains"],
                     "dt_record": rb["dt_record"],
                     "exp282_reread": {
                         "n_rows": rb["counts"]["n_rows282"],
                         "branch": dep282["branch"],
                         "host_table_walk_end_rms_means": rb["means282"]},
                     "exp287_reread": {
                         "n_rows": rb["counts"]["n_rows287"],
                         "host_table_mean_cvt": rb["mean_cvt287"]},
                     "exp288_reread": {
                         "n_rows": rb["counts"]["n_rows288"],
                         "branch": dep288["branch"],
                         "per_host_R_max": rb["rmax288"]},
                     "zero_reader_scan": zero_reader_scan,
                     "port_sha256": port_sha_entry,
                     "exp142_sha256": exp142_sha_entry}
        return {"pass": 1, "rows": rows_out, "host_table": host_table,
                "integrity": integrity, "test_suite": suite,
                "ro_before": ro_before, "lock_reads": len(_LOCK_LOG),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry}

    # ---- PASS 2 (G3): the activation grid — 3 x 72 fresh decodes (the
    #     g > 0 points of exp258's VERBATIM grid; the g = 0.0 point IS
    #      the schema-only arm — pass 1's G1 anchor, asserted bit-exact
    #      vs exp256's deposits — serves as the within-run control) -----
    def _compute_pass2():
        _LOCK_LOG.clear()
        rb = _rebuild()
        bases = rb["bases"]
        grid_rows: list = []
        for g in G_ACTIVE:
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_grid_row(
                            k, rk, ctx["deep"][inst]["spec"], med, s,
                            ctx["fmax"], g, ctx["A"])
                        grid_rows.append(rec)
                hs = [r for r in grid_rows
                      if r["host"] == k and r["g_ctx"] == g]
                print(f"  [pass2 g={g} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | hist writes "
                      f"{hs[0]['n_hist_writes']}/row",
                      flush=True)
        assert len(grid_rows) == 216, \
            f"pass2 produced {len(grid_rows)} rows != 216"
        assert len(_LOCK_LOG) == 216, \
            f"the S* lock count {len(_LOCK_LOG)} != 216 reads"
        return {"pass": 2, "grid_rows": grid_rows, "ro_before": ro_before,
                "lock_reads": len(_LOCK_LOG),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry}

    # ---- THE ASSEMBLY (a pure function of the two passes' payloads +
    #      the deposits; the merge path and the in-process path share it
    #      verbatim; the merge NEVER re-decodes) ---------------------------
    def _assemble(p1, p2, run_form):
        assert p1["pass"] == 1 and p2["pass"] == 2, "payload swap"
        assert p1["ro_before"] == p2["ro_before"] == ro_before, \
            "ro_before drifted across passes"
        assert p1["port_sha256"] == p2["port_sha256"] == _sha(PORT_FILE), \
            "the ported collective.py drifted mid-run"
        assert p1["exp142_sha256"] == p2["exp142_sha256"] \
            == _sha(EXP142_FILE), \
            "exp142 was modified — the pre-registered NOT-modified rule"
        rows = p1["rows"]
        assert len(rows) == 72, "the anchor battery drifted"
        grid_rows = p2["grid_rows"]
        assert len(grid_rows) == 216, "the grid battery drifted"
        integrity = p1["integrity"]
        counts = integrity["counts"]
        chains = integrity["provenance_chains"]
        suite = p1["test_suite"]

        # ---- the control column IS the G1 anchor: re-asserted bit-exact
        #      vs exp256's deposits at assembly (fail=STOP) ---------------
        dep_sub = {}
        for r in dep256["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                dep_sub[(r["host"], int(r["seed"]),
                         i["row_key"])] = float(i["err"])
        control_err = {}
        for r in rows:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert r["err"] == dep_sub[key], \
                (f"{key}: the control column drifted from exp256's "
                 "deposited err")
            control_err[key] = r["err"]
        anchor_by_key = {(r["host"], int(r["seed"]), r["row_key"]): r
                         for r in rows}

        # ---- THE GRID FACE: per grid point the per-host mean errs, the
        #      deltas vs the control, the strict-improvement flags; the
        #      structural stream face (the walked count + the commit
        #      count + the blend count are g-independent) ----------------
        per_grid = {}
        stream_ok_rows = 0
        hist_const_rows = 0
        reg_ok_rows = 0
        for g in G_ACTIVE:
            grows = [r for r in grid_rows if r["g_ctx"] == g]
            assert len(grows) == 72, f"g={g}: the 72-row battery drifted"
            n_st = 0
            n_hc = 0
            n_rg = 0
            for r in grows:
                key = (r["host"], int(r["seed"]), r["row_key"])
                a = anchor_by_key[key]
                st_ok = bool(r["walk_steps"] == a["walk_steps"]
                             and r["n_commits"] == a["n_commits"])
                assert st_ok, \
                    (f"{key} g={g}: the walked count / commit count moved "
                     "with the grid — the stream face drifted")
                n_st += int(st_ok)
                n_hc += int(r["n_hist_writes"] > 0)
                n_rg += int(all(r["register"][k] for k in
                                ("present_ok", "init_ok", "replay_ok",
                                 "complement_ok", "finite_ok")))
            stream_ok_rows += n_st
            reg_ok_rows += n_rg
            host_means = {}
            for h in hosts:
                hs = [r for r in grows if r["host"] == h]
                assert len(hs) == 6, f"g={g} {h}: the 6 rows drifted"
                host_means[h] = float(np.mean([r["err"] for r in hs]))
            worst = max(grows, key=lambda r: r["err"])
            per_grid[g] = {
                "g_ctx": float(g),
                "host_mean_err": host_means,
                "worst_err": float(worst["err"]),
                "worst_row": {"host": worst["host"],
                              "seed": int(worst["seed"]),
                              "row_key": worst["row_key"]},
                "worst_under_bar": bool(worst["err"] < ERR_BAR),
                "bar": ERR_BAR,
                "bar_note": ("the anchor's 6.0 bar, unchanged — audit-"
                             "only, never gating"),
                "n_verified": int(sum(r["verified"] for r in grows)),
                "n_rows_with_hist_writes": n_hc,
                "register_ok_rows": n_rg,
                "mean_cvt": {h: float(np.mean(
                    [r["cvt_rms"] for r in grows if r["host"] == h]))
                    for h in hosts}}
        for rk_full in {(r["host"], int(r["seed"]), r["row_key"],)
                        for r in grid_rows}:
            hw = tuple(r["n_hist_writes"] for r in grid_rows
                       if (r["host"], int(r["seed"]), r["row_key"])
                       == rk_full)
            hist_const_rows += int(len(set(hw)) == 1)
        assert hist_const_rows == 72, \
            "the per-row blend count moved with the grid"
        assert stream_ok_rows == 216 and reg_ok_rows == 216, \
            "the grid's stream/register face drifted"

        # ---- THE DELTA TABLE + THE BRANCH (pre-named bars) --------------
        control_means = {row["host"]: float(row["mean_err"])
                         for row in p1["host_table"]}
        delta_table = {}
        n_improved = {}
        total_delta = {}
        for g in G_ACTIVE:
            drow = {}
            n_imp = 0
            tot = 0.0
            for h in hosts:
                delta = float(per_grid[g]["host_mean_err"][h]
                              - control_means[h])
                drow[h] = {"mean_err_g": float(
                    per_grid[g]["host_mean_err"][h]),
                    "mean_err_control": control_means[h],
                    "delta": delta, "improved_strict": bool(delta < 0.0)}
                n_imp += int(delta < 0.0)
                tot += delta
            delta_table[g] = drow
            n_improved[g] = int(n_imp)
            total_delta[g] = float(tot)
        # the best grid point (pre-named tie-break: most improving hosts,
        # then the more-negative total delta, then the smaller g)
        best_g = sorted(G_ACTIVE,
                        key=lambda g: (-n_improved[g], total_delta[g], g))[0]
        if max(n_improved[g] for g in G_ACTIVE) >= HISTORY_MIN_HOSTS:
            branch_local = "HISTORY-CARRIED"
        else:
            branch_local = "HISTORY-INERT"

        # ---- THE AUDIT FACE: exp288's pooled-R_max class-blindness
        #     re-read at the best grid point (never gating) ---------------
        def _pooled_face(grows):
            ht = []
            for h in hosts:
                hs = [r for r in grows if r["host"] == h]
                NW = int(sum(r["n_write"] for r in hs))
                TOT = float(sum(r["sum_sq_e"] for r in hs))
                pool = []
                for cidx in (0, 1, 2):
                    N_c = int(sum(d["n"] for r in hs for d in r["decomp"]
                                  if d["cls"] == cidx))
                    SS_c = float(sum(d["sum_sq"] for r in hs
                                     for d in r["decomp"]
                                     if d["cls"] == cidx))
                    frac_c = float(SS_c / TOT)
                    share_c = float(N_c / NW)
                    pool.append({
                        "cls": cidx, "name": CLASS_NAMES[cidx], "n": N_c,
                        "cell_share": share_c, "frac_of_sq": frac_c,
                        "R": (float(frac_c / share_c)) if N_c > 0 else None})
                nonempty = [p["R"] for p in pool if p["R"] is not None]
                ht.append({"host": h, "n_write": NW, "classes": pool,
                           "R_max": float(max(nonempty)),
                           "concentrates": bool(max(nonempty) >= CONC_BAR)})
            n_conc = sum(1 for row in ht if row["concentrates"])
            return {"per_host": ht, "n_concentrating_hosts": n_conc,
                    "bars": {"CONC_BAR": CONC_BAR,
                             "CONC_MIN_HOSTS": CONC_MIN_HOSTS},
                    "bars_source": ("exp288's pre-named audit bars, "
                                    "reused for the re-read — audit-only, "
                                    "never gating in exp289")}
        best_grows = [r for r in grid_rows if r["g_ctx"] == best_g]
        rmax_face_best = _pooled_face(best_grows)
        rmax_face_anchor = {"source": "exp288's deposited face (READ-ONLY)",
                            "branch": dep288["branch"],
                            "per_host_R_max": integrity["exp288_reread"]
                            ["per_host_R_max"]}

        # ---- the tallies ------------------------------------------------
        n_s0_err = sum(1 for r in rows if r["s0_err_ok"])
        n_s0_ver = sum(1 for r in rows if r["s0_verified_ok"])
        n_we282 = sum(1 for r in rows if r["walk_end_282_ok"])
        n_ts282 = sum(1 for r in rows if r["trace_sha_282_ok"])
        n_ee282 = sum(1 for r in rows if r["err_exact_282_ok"])
        n_cs287 = sum(1 for r in rows if r["commit_sha_287_ok"])
        n_cvt287 = sum(1 for r in rows if r["cvt_287_ok"])
        n_nc287 = sum(1 for r in rows if r["n_commits_287_ok"])
        n_sc287 = sum(1 for r in rows if r["sc_287_ok"])
        n_reg_present = sum(1 for r in rows if r["register"]["present_ok"])
        n_reg_init = sum(1 for r in rows if r["register"]["init_ok"])
        n_reg_replay = sum(1 for r in rows if r["register"]["replay_ok"])
        n_reg_comp = sum(1 for r in rows
                         if r["register"]["complement_ok"])
        n_reg_fin = sum(1 for r in rows if r["register"]["finite_ok"])
        n_count = sum(1 for r in rows if r["commits_count_ok"])
        n_uniq = sum(1 for r in rows if r["commits_unique_ok"])
        n_cov = sum(1 for r in rows if r["coverage_ok"])
        n_fin = sum(1 for r in rows if r["commits_finite_ok"])
        n_cens = sum(1 for r in rows if r["census_ok"])
        n_a3 = sum(1 for r in rows if r["a3_ok"])
        n_conv = sum(1 for r in rows if r["conv_step"] >= 0)
        n_digests = sum(1 for r in rows
                        if len(r["commit_seq_sha256"]) == 64)

        g1 = dict(counts)
        g1.update({"n_s0_err_ok": n_s0_err, "n_s0_verified_ok": n_s0_ver,
                   "n_walk_end282_ok": n_we282, "n_trace282_ok": n_ts282,
                   "n_errexact282_ok": n_ee282,
                   "n_commitsha287_ok": n_cs287, "n_cvt287_ok": n_cvt287,
                   "n_ncommits287_ok": n_nc287, "n_scrms287_ok": n_sc287,
                   "n_mean282_ok": sum(1 for row in p1["host_table"]
                                       if row[
                                           "mean8_equals_exp282_host_table"]),
                   "n_meancvt287_ok": sum(
                       1 for row in p1["host_table"]
                       if row["mean_cvt_equals_exp287_host_table"]),
                   "n_register_present_ok": n_reg_present,
                   "n_register_init_ok": n_reg_init,
                   "test_suite_green": bool(suite["green"]),
                   "test_suite_returncode": suite["returncode"],
                   "test_suite_n_pass_lines": suite["n_pass_lines"]})
        g2 = {"n_rows": len(rows),
              "n_register_replay_ok": n_reg_replay,
              "n_register_complement_ok": n_reg_comp,
              "n_register_finite_ok": n_reg_fin,
              "n_commits_count_ok": n_count,
              "n_commits_unique_ok": n_uniq,
              "n_coverage_ok": n_cov,
              "n_commits_finite_ok": n_fin,
              "n_census_ok": n_cens,
              "n_digests_ok": n_digests,
              "n_a3_ok": n_a3, "n_conv_ok": n_conv,
              "n_lock_reads": int(p1["lock_reads"])}
        g3 = {"branch": branch_local,
              "n_grid_rows": len(grid_rows),
              "n_stream_ok_rows": stream_ok_rows,
              "n_register_ok_rows": reg_ok_rows,
              "n_hist_const_rows": hist_const_rows,
              "n_improved_per_grid": {str(g): n_improved[g]
                                      for g in G_ACTIVE},
              "total_delta_per_grid": {str(g): total_delta[g]
                                       for g in G_ACTIVE},
              "control_is_g1_anchor_bit_exact": len(control_err) == 72,
              "worst_err_per_grid": {str(g): per_grid[g]["worst_err"]
                                     for g in G_ACTIVE},
              "worst_under_bar_per_grid": {
                  str(g): per_grid[g]["worst_under_bar"] for g in G_ACTIVE},
              "n_verified_per_grid": {str(g): per_grid[g]["n_verified"]
                                      for g in G_ACTIVE},
              "lock_reads_pass2": int(p2["lock_reads"])}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "rows": rows, "host_table": p1["host_table"],
                "grid_rows": grid_rows, "per_grid": per_grid,
                "delta_table": delta_table, "n_improved": n_improved,
                "total_delta": total_delta, "best_g": float(best_g),
                "control_means": control_means,
                "rmax_face_best": rmax_face_best,
                "rmax_face_anchor": rmax_face_anchor,
                "integrity": integrity, "test_suite": suite,
                "g1": g1, "g2": g2, "g3": g3,
                "branch": branch_local, "run_form": run_form}

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the default is
    #      the IN-PROCESS form (the whole sequence, may exceed the 570 s
    #      cap); the pre-named sandbox form is the CHECKPOINT-SPLIT
    #      EXP289_MODE=pass1 (G1+G2) | pass2 (G3) | merge — each pass a
    #      separate process, the merge assembling + evaluating the gates
    #      once and NEVER re-decoding) ------------------------------------
    _MODE = os.environ.get("EXP289_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp289_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp289_pass2.checkpoint.json")}

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
            "the ported collective.py drifted after the work"
        assert _sha(EXP142_FILE) == exp142_sha_entry, \
            "exp142 was modified after the work"

    if _MODE in ("pass1", "pass2"):
        tag = 1 if _MODE == "pass1" else 2
        if tag == 1:
            print("=== exp289 pass1: THE PORT (G1 anchor + G2 register) "
                  "===")
            payload = _compute_pass1()
        else:
            print("=== exp289 pass2: THE ACTIVATION GRID (G3) ===")
            payload = _compute_pass2()
        ck = _CK[tag]
        assert not os.path.exists(ck), \
            (f"{ck} already holds a payload — the split form caches "
             "exactly one payload per pass")
        with open(ck, "w") as fh:
            json.dump(payload, fh, sort_keys=True)
        print(f"  checkpointed {_MODE} (sha {_payload_sha(payload)[:16]})")
        _exit_checks()
        for _m in PINNED:
            if hasattr(_m, "NEURAL_SPEC_MIN"):
                _m.NEURAL_SPEC_MIN = PROD_FLOOR
        assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
            "floor drift at exit"
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
        print("=== exp289: THE HISTORY-REGISTER PORT (giving the dormant "
              "channels a state variable that survives the walk) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 anchor rows at the production "
              f"budget {BUDGET} with the register live (G1+G2), then the "
              f"activation grid {list(G_ACTIVE)} x 72 rows (G3; the "
              f"g=0.0 point IS the anchor — the within-run control)")
        p1 = _compute_pass1()
        p2 = _compute_pass2()
        sa = _payload_sha(p1)
        sb = _payload_sha(p2)
        core = _assemble(p1, p2, "in-process default (one invocation)")
        run_form = "in-process default (one invocation)"

    # ---- the gate assembly (evaluated exactly once) ---------------------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    chains = integrity["provenance_chains"]
    suite = core["test_suite"]
    # (ro_before is the module-level record; both passes asserted it at
    #  _assemble; the exit re-check lands below)
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(ro_before.values()))
    g1_pass = bool(
        g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
        and g1["n_bnd_ok"] == 12 and g1["n_bnd_dual_ok"] == 12
        and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
        and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
        and g1["n_rows256"] == 72 and g1["n_structure_ok"] == 36
        and g1["n_worst_eq_max"] == 36
        and g1["n_deep_targets_ok"] == 72 and g1["n_medium_shas_ok"] == 72
        and g1["n_rows282"] == 72 and g1["n_282_chain_ok"] == 72
        and g1["n_host_table282_ok"] == 12
        and g1["n_rows287"] == 72 and g1["n_host_table287_ok"] == 12
        and g1["n_rows288"] == 72 and g1["n_288_chain_ok"] == 72
        and g1["n_s0_err_ok"] == 72 and g1["n_s0_verified_ok"] == 72
        and g1["n_walk_end282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72 and g1["n_mean282_ok"] == 12
        and g1["n_commitsha287_ok"] == 72 and g1["n_cvt287_ok"] == 72
        and g1["n_ncommits287_ok"] == 72 and g1["n_scrms287_ok"] == 72
        and g1["n_meancvt287_ok"] == 12
        and g1["n_register_present_ok"] == 72
        and g1["n_register_init_ok"] == 72
        and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
        and g1["test_suite_green"]
        and chains["total_verified"] == 31
        and ro_unchanged)
    g2_pass = bool(g2["n_rows"] == 72
                   and g2["n_register_replay_ok"] == 72
                   and g2["n_register_complement_ok"] == 72
                   and g2["n_register_finite_ok"] == 72
                   and g2["n_commits_count_ok"] == 72
                   and g2["n_commits_unique_ok"] == 72
                   and g2["n_coverage_ok"] == 72
                   and g2["n_commits_finite_ok"] == 72
                   and g2["n_census_ok"] == 72
                   and g2["n_digests_ok"] == 72
                   and g2["n_a3_ok"] == 72
                   and g2["n_conv_ok"] == 72
                   and g2["n_lock_reads"] == 72)
    g3_pass = bool(
        g3["branch"] in ("HISTORY-CARRIED", "HISTORY-INERT")
        and g3["n_grid_rows"] == 216
        and g3["n_stream_ok_rows"] == 216
        and g3["n_register_ok_rows"] == 216
        and g3["n_hist_const_rows"] == 72
        and g3["control_is_g1_anchor_bit_exact"]
        and len(g3["n_improved_per_grid"]) == 3
        and all(v >= 0 and v <= 12 for v in g3["n_improved_per_grid"].values())
        and g3["lock_reads_pass2"] == 216)

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
    n_improved = core["n_improved"]
    total_delta = core["total_delta"]
    best_g = core["best_g"]
    per_grid = core["per_grid"]
    delta_table = core["delta_table"]
    control_means = core["control_means"]
    rmax_best = core["rmax_face_best"]
    rmax_anchor = core["rmax_face_anchor"]

    if branch == "HISTORY-CARRIED":
        g_star = max(G_ACTIVE, key=lambda g: (n_improved[g],
                                              -total_delta[g]))
        branch_text = (
            f"the register is READ AND IT MATTERS — the self-history "
            f"blend IMPROVED the mean err on "
            f"{max(n_improved.values())}/12 hosts at some g_ctx > 0 "
            f"(>= the pre-named {HISTORY_MIN_HOSTS}); the five dormant "
            f"channels now have a state variable that survives the walk, "
            f"and its first activation is carried")
    else:
        g_star = max(G_ACTIVE, key=lambda g: (n_improved[g],
                                              -total_delta[g]))
        branch_text = (
            f"the register is read and INERT — no g_ctx > 0 improved the "
            f"mean err on >= {HISTORY_MIN_HOSTS}/12 hosts (the best grid "
            f"point improved {max(n_improved.values())}/12); the "
            f"self-history face does not carry the battery, deposited "
            f"honestly (the exp258 verdict's form)")

    verdict_body = (
        f"{branch} — {branch_text}"
        f" (the deltas vs the g=0.0 within-run control: "
        + "; ".join(
            f"g={g}: {n_improved[g]}/12 improved, total delta "
            f"{total_delta[g]:+.4f}" for g in G_ACTIVE)
        + f" | the per-host mean errs at the best grid point g={best_g} "
          f"within [{min(core['delta_table'][best_g][h]['mean_err_g'] for h in hosts):.3f}, "
          f"{max(core['delta_table'][best_g][h]['mean_err_g'] for h in hosts):.3f}] "
          f"vs the control within "
          f"[{min(control_means.values()):.3f}, "
          f"{max(control_means.values()):.3f}]"
          f" | the worst-err faces vs the 6.0 bar (unchanged, audit-only): "
        + "; ".join(f"g={g}: {per_grid[g]['worst_err']:.2f}"
                    f"{' <bar' if per_grid[g]['worst_under_bar'] else ' >=BAR'}"
                    for g in G_ACTIVE)
        + f" | THE REGISTER FACE: the presence "
          f"{g1['n_register_present_ok']}/72 + the init == the spec "
          f"install {g1['n_register_init_ok']}/72 at the walk's start; "
          f"at the walk's end the register IS the commit replay "
          f"{g2['n_register_replay_ok']}/72 with the non-write-set face "
          f"== the spec install {g2['n_register_complement_ok']}/72, "
          f"finite {g2['n_register_finite_ok']}/72 — and 216/216 on the "
          f"grid (the register survives the walk + the settle)"
          f" | THE S0 ANCHOR (the port side-effect-free): the errs "
          f"reproduce exp256's deposited substituted errs bit-exact "
          f"({g1['n_s0_err_ok']}/72, the verified flags "
          f"{g1['n_s0_verified_ok']}/72) AND exp282's walk_end_rms "
          f"bit-exact (walk_end {g1['n_walk_end282_ok']}/72, trace sha "
          f"{g1['n_trace282_ok']}/72, err_exact {g1['n_errexact282_ok']}"
          f"/72, the per-host means {g1['n_mean282_ok']}/12) AND exp287's "
          f"COMMIT LAYER bit-exact (the commit-sequence digests "
          f"{g1['n_commitsha287_ok']}/72, cvt_rms {g1['n_cvt287_ok']}/72, "
          f"n_commits {g1['n_ncommits287_ok']}/72, sc_rms "
          f"{g1['n_scrms287_ok']}/72, the per-host mean_cvt "
          f"{g1['n_meancvt287_ok']}/12)"
          f" | THE AUDIT FACES (never gating): exp288's pooled-R_max "
          f"class-blindness re-read at the best grid point — "
          f"{rmax_best['n_concentrating_hosts']}/12 hosts concentrating "
          f"(vs exp288's deposited SPEC-UNIFORM face, the anchor's own "
          f"R_max within [{min(rmax_anchor['per_host_R_max'].values()):.4f}, "
          f"{max(rmax_anchor['per_host_R_max'].values()):.4f}]); the "
          f"repo test suite green in the shadow subprocess "
          f"({suite['n_pass_lines']} PASS lines, returncode "
          f"{suite['returncode']}); the zero-reader scan: "
          f"{len(integrity['zero_reader_scan']['files_with_phi_history'])} "
          f"files carry phi_history (the port + this instrument only)"
          f" | 12 hosts, a deterministic sha-asserted rebuild (graph_path "
          f"for H0/H1, small_world at the deposited rewire seeds), the "
          f"provenance chains sha-verified 31/31, 7 deposits READ-ONLY "
          f"byte-unchanged, one-pass per grid point ({core['run_form']}), "
          f"floor -60.0")

    # ---- the discipline scans + the deposit form -------------------------
    deposit = {
        "exp": "exp289_history_register",
        "claim": (
            "THE HISTORY-REGISTER PORT (batch 47, pre-registration commit "
            "982cb81): the commit HISTORY as a persistent register — what "
            "the program wrote LAST time, carried across walks as a state "
            "variable the dynamics can read. THE PORT (additive, zero-knob "
            "at defaults): a per-cell register phi_history on the "
            "collective, populated AT EACH commit write (after the write, "
            "phi_history[i] = the written value), initialized to the spec "
            "layer's own values at write_spec_layer time (the never-written "
            "cells' history IS the spec's install); NOTHING reads it at "
            "defaults — G1's bit-exact anchor (exp256's deposited "
            "substituted errs 72/72) is the side-effect-free proof. THE "
            "FIRST HISTORY-CARRYING ACTIVATION: exp258's ctx coupling term "
            "re-run reading the HISTORY register — the cell pulled toward "
            "its OWN last commit (the self-history face) instead of the "
            "interior context — on exp258's VERBATIM g_ctx grid {0, 0.25, "
            "0.5, 1.0} over the same 72-row battery shape (the g=0.0 point "
            "IS the schema-only arm — the within-run control). Branch: "
            "HISTORY-CARRIED iff EXISTS g > 0 improving the per-host mean "
            "err vs the control on >= 10/12 hosts (strict delta < 0.0); "
            "else HISTORY-INERT"),
        "method": {
            "port": (
                "cultivation/bioelectric/collective.py touched ADDITIVELY "
                "only: (1) write_spec_layer installs phi_history = the "
                "spec map bit-exactly (the history starts as the program's "
                "own target); (2) regrow's chain-walk commit site "
                "populates the register after the write (guarded — absent "
                "when no spec layer was ever written, the pre-spec legacy "
                "paths untouched); (3) the traced replica populates the "
                "same register at its own commit site (the disclosed (f)-"
                "site analog). exp142 NOT modified (sha entry == exit, "
                "recorded); the zero-reader scan asserts phi_history "
                "appears in no file outside the port + this instrument"),
            "replica": (
                "the exp286/exp287/exp288 traced replica REUSED VERBATIM "
                "at the production budget 8 == exp142's STEPS_PER_CELL "
                "(the host rebuild, exp256's _scoped_row_read_state form: "
                "PN1/PN2 + TC1 + TC2 + the traced TC3), plus the two "
                "disclosed additions: the register live (presence + init "
                "asserted at the walk's start; the population after each "
                "write; the survival asserted at the walk's end) and the "
                "activation blend (g_ctx > 0 AND the exp258 canon-boundary "
                "class restriction; ZERO deviation at g_ctx == 0.0)"),
            "activation": (
                "effective = (1 - g_ctx) * theta_new + g_ctx * "
                "phi_history[i] at the canon-boundary write cells (exp258's "
                "restriction verbatim; the read source swapped from the "
                "interior-context channel to the cell's own history "
                "register — the self-history face). The walk order, the "
                "interludes, the draw positions are g-independent (the "
                "blend is value-level only), asserted per row across the "
                "grid (walk_steps + n_commits == the anchor's 216/216)"),
            "branch_rule": (
                "per grid point g in {0.25, 0.5, 1.0}: per host the 6-row "
                "mean err; the host improves iff the mean delta vs the "
                "g=0.0 within-run control is < 0.0 (strict, disclosed); "
                "HISTORY-CARRIED iff EXISTS g with #{improved} >= 10 "
                "(the pre-named bar); else HISTORY-INERT. The best grid "
                "point (for the audit faces): most improving hosts, then "
                "the more-negative total delta, then the smaller g"),
            "audit_faces": (
                "the worst-err per grid point vs the anchor's 6.0 bar "
                "(unchanged); exp288's pooled-R_max class-blindness "
                "re-read at the best grid point (exp208's classify "
                "VERBATIM, exp288's pooling, exp288's pre-named bars "
                "CONC_BAR 1.50 / CONC_MIN_HOSTS 10 — audit-only, never "
                "gating), carried next to exp288's deposited face"),
            "run_form": (
                "the default in-process form runs the whole sequence (may "
                "exceed the 570 s cap); the pre-named sandbox form is the "
                "checkpoint split EXP289_MODE=pass1 (G1+G2) | pass2 (G3) "
                "| merge — each pass a separate process, the merge "
                "assembling and evaluating the gates once, NEVER "
                "re-decoding; both forms evaluate the SAME gates and "
                "assert the same bit-identities"),
            "scope": (
                "the full commit sequences, traces, final states and "
                "register arrays NOT re-deposited — bit-reproduced via "
                "the per-row digests (commit_seq_sha256, trace_sha256, "
                "phi_history_sha256) + G1's anchors (the exp284/exp285/"
                "exp286/exp287/exp288 precedent); no wall-clock fields")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base) + the mia audit errs",
                "the 72 rows — the S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas",
                "the host frame + the per-host one-zone premium means "
                "+ the boundary counts + the outlier pre-name source",
                "the outlier pre-name + the field-table carries",
                "the S0 walk anchor — the 72 per-row walk_end_rms + "
                "trace shas + the deposited TRAJECTORY-CARRIED branch",
                "the S0 commit-layer anchor — the 72 per-row "
                "commit_seq_sha256 + cvt_rms + n_commits + sc_rms + the "
                "12-host mean_cvt",
                "the immediately prior batch's face — the deposited "
                "SPEC-UNIFORM branch + the per-host pooled R_max + its "
                "own fresh errs (the chain face) + the 6 inputs sha "
                "records verified in the chains"))},
        "port": {
            "file": "cultivation/bioelectric/collective.py",
            "sha256": integrity["port_sha256"],
            "additive_sites": [
                "write_spec_layer: phi_history initialized to the spec "
                "map (the history starts as the program's own target)",
                "regrow walk: the commit-write population (guarded; "
                "the (f)-site analog)",
                "the traced replica: the population at its own commit "
                "site + the survival asserts (this module)"],
            "zero_reader_scan": integrity["zero_reader_scan"],
            "exp142_modified": False,
            "exp142_sha256": integrity["exp142_sha256"]},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp282_reread": integrity["exp282_reread"],
        "exp287_reread": integrity["exp287_reread"],
        "exp288_reread": integrity["exp288_reread"],
        "provenance_chains": chains,
        "targets": integrity["targets"],
        "test_suite": suite,
        "rows": core["rows"],
        "host_table": core["host_table"],
        "grid_rows": core["grid_rows"],
        "grid": {
            "g_ctx_grid": list(G_CTX_GRID),
            "g_active": list(G_ACTIVE),
            "grid_source": "exp258's VERBATIM g_ctx dial",
            "per_grid": {str(g): per_grid[g] for g in G_ACTIVE},
            "delta_table": {str(g): delta_table[g] for g in G_ACTIVE},
            "control_means": control_means,
            "control_source": ("pass 1's G1 anchor rows — asserted "
                               "bit-exact vs exp256's deposited "
                               "substituted errs 72/72 at assembly"),
            "n_improved_per_grid": {str(g): n_improved[g]
                                    for g in G_ACTIVE},
            "total_delta_per_grid": {str(g): total_delta[g]
                                     for g in G_ACTIVE},
            "best_grid_point": best_g,
            "best_grid_point_rule": ("most improving hosts, then the "
                                     "more-negative total delta, then "
                                     "the smaller g")},
        "branch": branch,
        "branch_discriminant": {
            "bars": {"HISTORY_MIN_HOSTS": HISTORY_MIN_HOSTS},
            "bars_pre_named_at": ("982cb81 — fixed at pre-registration, "
                                  "never fit"),
            "improvement_bar": ("the per-host mean delta < 0.0 — strict, "
                                "disclosed"),
            "n_improved_per_grid": {str(g): n_improved[g]
                                    for g in G_ACTIVE},
            "resolved": {"branch": branch,
                         "best_grid_point": best_g,
                         "n_improved_at_best": n_improved[best_g]},
            "audit_rmax_face_at_best_g": rmax_best,
            "audit_rmax_face_anchor_exp288": rmax_anchor},
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": {
            "form": run_form,
            "discipline": "deterministic one-pass per grid point",
            "decodes": {"anchor_battery_g0": 72,
                        "grid_g_0.25": 72, "grid_g_0.5": 72,
                        "grid_g_1.0": 72},
            "stream_untouched_proof": (
                "the register is a state variable, not a second RNG "
                "consumer — the population is a pure recording after the "
                "write; G1's bit-exact errs + trace shas + commit "
                "digests 72/72 are the assertion; the grid's walked "
                "counts + commit counts == the anchor's 216/216"),
            "two_pass_note": (
                "the exp288 two-pass bit-identity discipline does NOT "
                "carry to this module — G4 pre-names the one-pass-per-"
                "grid-point form"),
            "payload_sha256_pass1": sa,
            "payload_sha256_pass2": sb},
        "discipline": {}}

    no_wall_clock = True
    _bad_keys = _scan_wall_clock_keys(deposit)
    if _bad_keys:
        no_wall_clock = False
    assert not _bad_keys, f"wall-clock key detected: {_bad_keys}"
    _blob = json.dumps(deposit)
    assert not any(pat in _blob for pat in ('"runtime', '"wall_clock',
                                            '"wall_s', '"timestamp',
                                            '"generated_at')), \
        "wall-clock field detected in the deposit"
    gates = {
        "G1_port_zero_delta_at_defaults": {
            "pass": g1_pass,
            "counts": g1,
            "provenance_chains": chains,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "s0_anchor": (
                "the 72-row battery with the register live reproduces "
                "exp256's deposited substituted errs bit-exact (72/72, "
                "the verified flags 72/72) AND exp282's walk_end_rms "
                "bit-exact (walk_end_rms + trace sha256 72/72 — the same "
                "walk discipline, plus err_exact 72/72 and the per-host "
                "means 12/12) AND exp287's commit layer bit-exact (the "
                "commit-sequence digests 72/72, cvt_rms 72/72, n_commits "
                "72/72, sc_rms 72/72, the per-host mean_cvt 12/12; "
                "asserted fail=STOP at decode) — the PORT is "
                "side-effect-free; the register's presence + init "
                "asserted per row; the repo test suite green from the "
                "repo root in the disclosed shadow subprocess; exp142 "
                "NOT modified")},
        "G2_the_register_is_the_commit_sequence": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "at the walk's end phi_history[write_set] == the commit "
                "replay's values BIT-EXACT per row (the register IS the "
                "commit sequence stored incrementally — the same replay "
                "exp287/exp288 anchored, now read from the register); "
                "the register's non-write-set cells == the spec install "
                "(the never-written cells' history is the spec layer); "
                "the register finite 72/72; the commit bookkeeping (the "
                "exp287 form: the count == walk_steps == the trace "
                "length, the indices unique, the coverage, the values "
                "finite, the census sane, the digest recorded); the A3 "
                "convention + the trace integrity + the TA3 convergence "
                "point asserted fail=STOP; the S* lock reads 72")},
        "G3_activation_branch": {
            "pass": g3_pass,
            "bars": ("per grid point g in {0.25, 0.5, 1.0} the 72-row "
                     "battery re-run with the ctx coupling reading "
                     "phi_history; per host the 6-row mean err; "
                     "HISTORY-CARRIED iff EXISTS g > 0 with the mean err "
                     "improved vs the g=0.0 within-run control on >= "
                     "10/12 hosts (the per-host mean delta < 0.0 — "
                     "strict, disclosed); else HISTORY-INERT. "
                     "Audit-only, never gating: the per-host per-grid "
                     "delta table; the worst-err per grid point vs the "
                     "6.0 bar (unchanged); exp288's pooled-R_max face "
                     "re-computed at the best grid point"),
            "resolved": {"branch": branch,
                         "n_improved_per_grid": {str(g): n_improved[g]
                                                 for g in G_ACTIVE},
                         "best_grid_point": best_g}},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_port_zero_delta_at_defaults",
                 "G2_the_register_is_the_commit_sequence",
                 "G3_activation_branch"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    gates["G4_discipline"] = {
        "pass": bool(no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged),
        "run_form": run_form,
        "deterministic_one_pass_per_grid_point": True,
        "stream_untouched_asserted_via_g1": (
            "the bit-exact errs + trace shas + commit digests 72/72"),
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_982cb81": docstring_ok,
        "header_byte_unchanged_vs_982cb81": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "n_source_deposits": len(READ_DEPS),
        "exp142_not_modified": True,
        "floor_at_exit": PROD_FLOOR,
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
        sort_keys=True, default=str).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  G1 the port's zero-delta at defaults: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the rebuild sha-asserted {g1['n_sha_ok']}/12 + edges "
          f"{g1['n_edges_ok']}/12 + the boundary counts "
          f"{g1['n_bnd_dual_ok']}/12 + f_max {g1['n_fmax_ok']}/12; the "
          f"S0 ANCHOR — the errs == exp256's deposited errs bit-exact "
          f"{g1['n_s0_err_ok']}/72 (the verified flags "
          f"{g1['n_s0_verified_ok']}/72), exp282's walk_end_rms "
          f"{g1['n_walk_end282_ok']}/72 (trace sha "
          f"{g1['n_trace282_ok']}/72), exp287's commit layer "
          f"{g1['n_commitsha287_ok']}/72 (cvt {g1['n_cvt287_ok']}/72, "
          f"n_commits {g1['n_ncommits287_ok']}/72, sc_rms "
          f"{g1['n_scrms287_ok']}/72); the register presence "
          f"{g1['n_register_present_ok']}/72 + init "
          f"{g1['n_register_init_ok']}/72; the test suite green: "
          f"{g1['test_suite_green']} ({g1['test_suite_n_pass_lines']} "
          f"PASS lines); the chains {chains['total_verified']}/31)")
    print(f"  G2 the register IS the commit sequence: "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(the replay equality {g2['n_register_replay_ok']}/72; the "
          f"spec-install complement {g2['n_register_complement_ok']}/72; "
          f"finite {g2['n_register_finite_ok']}/72; the commit "
          f"bookkeeping {g2['n_commits_count_ok']}/72 + unique "
          f"{g2['n_commits_unique_ok']}/72 + coverage "
          f"{g2['n_coverage_ok']}/72; the S* lock reads "
          f"{g2['n_lock_reads']}/72)")
    print("  G3 the activation grid (per-host mean deltas vs the g=0.0 "
          "control; H3/H5 the outliers):")
    for g in G_ACTIVE:
        drow = delta_table[g]
        parts = "; ".join(
            f"{h} {drow[h]['delta']:+.3f}"
            f"{'*' if drow[h]['improved_strict'] else ''}"
            for h in hosts)
        print(f"      g={g}: {n_improved[g]}/12 improved "
              f"(total {total_delta[g]:+.4f}) | {parts}")
    print(f"      the branch bars: HISTORY_MIN_HOSTS "
          f"{HISTORY_MIN_HOSTS} | best grid point g={best_g} | worst-err "
          f"faces: " + "; ".join(
              f"g={g} {per_grid[g]['worst_err']:.2f}"
              f"{' <6.0' if per_grid[g]['worst_under_bar'] else ' >=6.0'}"
              for g in G_ACTIVE))
    print(f"      the audit R_max face at the best grid point: "
          f"{rmax_best['n_concentrating_hosts']}/12 concentrating (the "
          f"exp288 anchor face: SPEC-UNIFORM, never gating here)")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(deterministic one-pass per grid point, form {run_form}; "
          f"no wall-clock fields: {no_wall_clock}; 7 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged}; exp142 NOT modified; floor "
          f"-60.0 at exit, the -35.0 reader pin disclosed)")
    print(f"\n  BRANCH: {branch} | n_improved per grid "
          f"{ {g: n_improved[g] for g in G_ACTIVE} } | best g={best_g}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    # ---- the hard rules, re-asserted after the work ----------------------
    _exit_checks()
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    if _MODE == "merge":
        for tag in (1, 2):
            if os.path.exists(_CK[tag]):
                os.remove(_CK[tag])
        print("  the checkpoint caches removed after the merge")
    return deposit


if __name__ == "__main__":
    main()
