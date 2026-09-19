#!/usr/bin/env python3
"""exp287 — THE FIXED POINT'S IDENTITY: IS THE WALK'S ERROR THE EXECUTED
PROGRAM'S OWN SELF-CONSISTENCY LIMIT? (batch 45; ledger L264's derived
item — batch 44 closed the budget question: the end-RMS carrier is the
walk's FIXED POINT, BUDGET-INVARIANT on 12/12 hosts with no
outlier/cluster separation, so the last structural question the
walk-level surface could ask is WHAT the fixed point IS. This module
asks for its identity: re-read the executed program's OWN writes as
the target.)

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED on walk_end_rms (the
PRE-settle trace[-1]; signed Spearman +0.8826151316282213 against
mia_prod_err, +0.8807017543859651 against exp272's one-zone premium
means) and exp286 landed the endpoint BUDGET-INVARIANT — the premium
is the walk's fixed point, carried by the host structure at every
step budget. But a fixed point is not yet an IDENTITY: is the walk's
final error vs the deep target the executed program's OWN
self-consistency limit — the walk lands exactly where it commits and
the error is IN the commit values (the program's imperfect
self-knowledge: the committed pattern differs from the deep target —
the chain closes at the compiler's program) — or does the walk's
final state differ from its own commits (the between-commit dynamics
and the settle MOVE it — SELF-DRIFT, the exp284 disclosed settle
gap's amplified form: exp284's |err_exact - trace[-1]| is an
RMS-DIFFERENCE that cancels drift orthogonal to the residual; the
per-cell committed read below is the drift's proper norm)?

THE TEST (pre-named): re-read the executed program's OWN writes as
the target. The state-carrying traced replica (exp286's landed form
REUSED VERBATIM — _execute_signed_traced with the budget
parameterization at the production budget 8 == exp142's
STEPS_PER_CELL, the host rebuild, exp256's _scoped_row_read_state
form: the projection chain PN1/PN2 + TC1 + TC2 + the traced TC3) runs
the substituted rows (12 hosts x 3 seeds (1,2,3) x the two deep
instances r-60i0/r-60i1 at n=400 — exp256's battery; budget 8). ONE
DISCLOSED RECORDING ADDITION (zero knobs): the replica already walks
cell-by-cell with the commit values in hand — the inherited/
committed theta per cell (theta_new, whatever its source: the spec
layer, the canon, or the parent) is RECORDED AT THE WRITE, after the
write, with the source tag; the recording draws NOTHING from the RNG
stream and touches no state — proven by the S0 anchor's bit-exact
trace sha256 + walk_end_rms (the SAME walk exp282 deposited). At the
walk's end the target for the self-consistency read is the COMMITTED
PATTERN itself (the final theta/V the walk wrote — the program's own
output read as its target).

THE PRE-NAMED QUANTITIES (fixed HERE at pre-registration):
  (1) THE SELF-CONSISTENCY ERROR — sc_rms = the RMS over the
      committed cells (the replay's support: exactly the cells the
      executed program wrote, each exactly once) between the walk's
      final state (the post-settle final_state read) and a REPLAY of
      its own commits (the commit sequence re-read: the recorded
      committed theta per cell, re-read in walk order). ZERO KNOBS:
      the replay is built ONLY from the recorded commits — no
      re-simulation, no parameters, no external target enters the
      replay; the definition has no free parameters.
  (2) THE PROGRAM-VS-TARGET GAP — the production err vs the deep
      target: err_exact (the A3-checked full-frame RMS between the
      final state and the deep target), ANCHORED by the S0 anchor
      (the reported errs reproduce exp256's deposited substituted
      errs BIT-EXACT 72/72; err_exact reproduces exp282's 72/72).
      (The supports differ by construction — the replay lives on the
      program's write set, the gap on the full frame; the ratio below
      is the pre-named read, the supports disclosed.)
  (3) THE BRANCH (the bars numeric, fixed HERE, never fit):
      SC_FRAC_BAR = 0.01, SC_MIN_HOSTS = 10 — per host the mean
      sc_rms over its 6 rows vs the mean err_exact over its 6 rows;
      the host is self-consistent iff mean_sc < SC_FRAC_BAR *
      mean_gap; N_sc = #{hosts self-consistent}:
        SELF-CONSISTENT iff N_sc >= SC_MIN_HOSTS (the walk lands
        exactly where it commits — the premium is the program's
        imperfect self-knowledge: the committed pattern differs from
        the deep target, the error is IN the commit values, the
        chain closes at the compiler's program);
        else SELF-DRIFT (the walk's final state differs from its own
        commits — the between-commit dynamics + the settle move it;
        the exp284 disclosed settle gap's amplified form).

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285/exp286 precedent
      (graph_path at the chain class's n=400 call site for H0/H1 —
      H0 echoes H1 bit-exactly, asserted; small_world(n, 0.10,
      deposited rewire_seed) for H2-H11), bit-asserted against
      exp243's records: sha256(|A| as float64) == base_sha256 12/12;
      the upper-triangle edge count == edges_base 12/12; the classify
      boundary count == n_boundary_cells_base 12/12, dual-carried vs
      exp272's per_host AND exp273's field table; the canon identity
      labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12; f_max
      recomputed == f_max_base 12/12; the bases NON-NEGATIVE
      asserted per host. The two deep-row targets rebuilt per
      exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited medium_sha256 72/72. exp256's 72 rows with
      the substituted structure 36/36 + worst == max 36/36. THE
      EXP282 RE-READ: the 72 row records present with trace_sha256 +
      walk_end_rms + err_deposited + walk_steps; exp282's deposited
      err_deposited == exp256's deposited substituted err 72/72 (the
      two deposits' chain anchor); exp282's deposited branch ==
      TRAJECTORY-CARRIED asserted (the pre-registered context);
      exp282's host_table walk_end_rms_mean present for the 12
      hosts. THE S0 ANCHOR (the production-budget battery): the
      re-run's reported errs reproduce exp256's DEPOSITED substituted
      errs BIT-EXACT (72/72, the machinery's native 2-dp convention;
      the verified flags 72/72), AND exp282's walk_end_rms reproduces
      BIT-EXACT (the fresh walk_end_rms == exp282's deposited
      walk_end_rms 72/72; the fresh trace sha256 == exp282's
      deposited trace_sha256 72/72 — the SAME walk exp282 deposited,
      which also proves the commit recording side-effect-free;
      err_exact 72/72; the fresh per-host end-RMS means == exp282's
      deposited host_table means 12/12). The carries: the mia carry
      bit-exact 12/12 (exp273's field table == exp243's own class
      records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS
      sha-verified against the current file bytes — exp243 (4) +
      exp256 (3) + exp272 (4) + exp273 (5) + exp282 (4) = 20 records.
      The source deposits READ-ONLY: sha-recorded BEFORE any read,
      byte-unchanged after the work (5 deposits: exp243, exp256,
      exp272, exp273, exp282).
  G2  THE COMMIT RECORDING + THE SELF-CONSISTENCY QUANTITY'S
      DEFINITION (zero-knob asserted, fail=STOP per row): the
      disclosed recording addition — the committed theta per cell
      recorded AT THE WRITE (after the write; the inherited/
      committed value whatever its source, with the source tag
      spec/canon/parent recorded audit-only) — draws nothing from
      the RNG stream and touches no state (proven by G1's bit-exact
      trace shas). Per row: the commit count == walk_steps == the
      trace length 72/72 (the write set fully recorded); the commit
      indices UNIQUE — each committed cell exactly once (the commit
      sequence re-read is a clean replay) 72/72; the replica-side
      write-set coverage: the commit sequence elementwise == the
      walked order (asserted inside the replica where the region is
      in scope) 72/72; the commit values finite 72/72; the commit
      sequence digest sha256 recorded per row (the full commit
      sequences NOT re-deposited — bit-reproduced via the digest +
      G1's trace shas, the exp284/exp285/exp286 precedent); THE
      REPLAY built ONLY from the recorded commits (the construction
      reads the commit list + the final state and nothing else — no
      re-simulation, no parameters, no external target enters the
      replay); sc_rms finite 72/72; the denominators err_exact > 0
      72/72. The per-row decode integrity: the A3 state convention
      (round(err_exact, 2) == the reported err) asserted fail=STOP
      72/72; the trace finite + trace[-1] > 0 + the trace length ==
      walk_steps 72/72; the convergence point exists (TA3, exp282's
      assert form) 72/72; the S* lock reads 72 (the lock log
      asserted); the exp284-style settle gap |err_exact -
      walk_end_rms| recorded audit-only.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): per host
      mean_sc (the 6-row mean of sc_rms) vs mean_gap (the 6-row mean
      of err_exact); the host self-consistent iff mean_sc <
      SC_FRAC_BAR * mean_gap (SC_FRAC_BAR 0.01); N_sc >= SC_MIN_HOSTS
      (10) -> SELF-CONSISTENT; else SELF-DRIFT. Audit-only, never
      gating: the per-row sc fractions sc_rms/err_exact; the
      commit-vs-target RMS on the committed cells (cvt_rms — where
      the error lives: the committed pattern vs the deep target on
      the program's own write set); the per-row + per-host source
      censuses (how many commits drew from the spec layer vs the
      canon vs the parent — the program's self-knowledge face); the
      exp284-style settle gaps; the max/min per-row sc per host; the
      audit-only regressions of mean_sc and mean_cvt against
      mia_prod_err (exp273's field table, asserted == exp243's own
      class records) and exp272's one-zone premium means (asserted
      == exp273's field-table carry) under the exp274/exp275/exp282
      conventions VERBATIM (Pearson on the tied-average ranks, the
      12-slot frame with the H0==H1 echo carried, the ties census
      per vector, the single-predictor rank R2) — does the
      self-consistency drift track the exposure (named honestly,
      never gating).
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, 72 decodes per pass; or
      the pre-named checkpoint-split EXP287_MODE=pass1|pass2 + merge
      with each pass a separate process; the two passes' payloads
      BIT-IDENTICAL, asserted at the merge/assembly); no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): SELF-CONSISTENT / SELF-DRIFT.

RUN: the deterministic sha-asserted rebuild (seconds) + 72 decodes per
pass ~ 60-90 s foreground per pass, TWO passes (G4) ~ 2-4 min total,
far under the 570 s cap per invocation. THE DEFAULT TWO-PASS
IN-PROCESS FORM (no env): the full battery computed twice in one
invocation. THE PRE-NAMED CHECKPOINT-SPLIT ALTERNATIVE:
EXP287_MODE=pass1|pass2 computes and caches ONE pass's payload per
invocation; EXP287_MODE=merge compares the two cached payloads
BIT-EXACT, assembles, evaluates the gates once, writes the deposit —
the merge NEVER re-decodes — and removes the caches. Both forms
evaluate the SAME gates and assert the same bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp287_fixed_point_identity.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once,
    #      pre-registration commit 1f6f07f) ================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home
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
    #      is the 1f6f07f pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "0c8db6705c55691f3da255ea5e42f706e02e749600885363ceb45f518fa73a00")
    EXPECTED_HEADER_SHA256 = (
        "920ac514d5c762f32a3ef056d45802577b56d7085a4f6edf9798e0b4281563ae")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 1f6f07f"
    assert header_ok, "header drifted from 1f6f07f"

    # ---- the -60.0 floor (G4: asserted at exit; exp218's disclosed
    #      exp169-import discipline — the whole reader chain imported
    #      FIRST, the floor restored after; the -35.0 reader-line pin
    #      disclosed) ------------------------------------------------------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    _PRE_RESTORE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in PINNED}
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    # ---- the frozen read configuration (exp256's battery constants;
    #      the replica's executor constants asserted = exp142's own;
    #      THE BUDGET + THE BRANCH BARS — the pre-named numeric bars) ---
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
    # STEPS_PER_CELL == 8 — exp286's landed parameterization AT the
    # default (no ladder here: exp286 closed the dose axis; the
    # identity question is commit-level, not budget-level).
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE BRANCH BARS (pre-named at 1f6f07f, numeric, never fit)
    SC_FRAC_BAR = 0.01
    SC_MIN_HOSTS = 10
    # the commit source tags (the pre-named census; audit-only)
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
    #      read, re-verified byte-unchanged at the end) -------------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP282 = os.path.join(ROOT, "results",
                          "exp282_trajectory_structure.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit"}
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

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
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

    # ---- exp208's classify VERBATIM (used ONLY in the rebuild's
    #      boundary-count integrity check — exp269's/exp280's/
    #      exp284's/exp285's/exp286's rebuild form; the identity rows
    #      themselves carry NO classify/decompose/mask work) -------------
    def classify(T: np.ndarray, W: np.ndarray) -> dict:
        n = len(T)
        Td = np.asarray(T, dtype=float)
        # CANON-BOUNDARY: the cell sits on a canon-value boundary
        # in the target (a lattice neighbor's target value differs;
        # the n-cell ring backbone i +/- 1)
        bnd = np.zeros(n, dtype=bool)
        for i in range(n):
            if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                bnd[i] = True
        # PAIR-JUNCTION: endpoint of >= 2 chords in the medium's chord
        # set (the pair support of the medium's base adjacency
        # |Wbase| > 0 — the hyperedge cliques are group couplings, not
        # pairs; DISCLOSED)
        support = np.abs(W) > 0
        iu = np.triu_indices(n, 1)
        deg = np.zeros(n, dtype=int)
        for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
            deg[a] += 1
            deg[b] += 1
        pj = deg >= 2
        # precedence: the registered listing order — CANON-BOUNDARY
        # wins, then PAIR-JUNCTION, then INTERIOR (disclosed)
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

    # ---- THE TRACED REPLICA: exp286's landed _execute_signed_traced
    #      REUSED VERBATIM (landed 4e504de — exp142's walk byte-similar
    #      + exactly the disclosed recording additions (a)-(e) + the
    #      budget parameterization; the RNG stream / dt / canon / walk
    #      order / commits untouched; exp142 NOT modified) with ONE
    #      DISCLOSED RECORDING ADDITION for exp287: (f) the inherited/
    #      committed theta per cell (theta_new, whatever its source:
    #      the spec layer, the canon, or the parent) RECORDED AT THE
    #      WRITE — after the write, with the source tag — drawing
    #      NOTHING from the RNG stream and touching no state; proven
    #      by the S0 anchor's bit-exact trace sha256 + walk_end_rms
    #      (the SAME walk exp282 deposited). The budget parameterization
    #      is exp286's landed form; exp287 runs it AT the production
    #      budget (BUDGET == STEPS_PER_CELL == 8, asserted). -----------
    def _execute_signed_traced(spec, adjacency, seed, op, budget):
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
                    "commits": [], "coverage_ok": False}
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
            c.theta[i] = theta_new
            c.V[i] = theta_new
            # ---- (f) THE DISCLOSED RECORDING ADDITION: the commit
            #      value recorded AT THE WRITE (after the write; the
            #      inherited/committed theta per cell; a pure recording
            #      of already-computed values — the RNG stream and the
            #      state untouched) -----------------------------------
            commits.append((int(i), float(theta_new), src_tag))
            # ---- (a) the per-step RMS read (a pure read; the walk's
            #      full-frame convergence; unchanged) -----------------
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        # the write-set coverage (the replica's side, the walk order in
        # scope): the commit sequence elementwise == the walked order —
        # every write recorded, nothing recorded unwritten
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        c.run(15.0, dt=dt)
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
        out["commits"] = commits                       # (f) exp287's
        out["coverage_ok"] = coverage_ok               # (f) exp287's
        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced + budgeted executor call)
    def _scoped_row_read_traced(spec, med, seed, fmax, budget):
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
                                         budget=budget)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one identity-row decode (the commit-level read — NO
    #      classify/decompose/mask work; the S0 anchors asserted
    #      fail=STOP on EVERY row: the battery runs at the production
    #      budget only) ----------------------------------------------------
    def _decode_row(host, row_key, spec, med, seed, fmax, dep_rec, rec282):
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

        # ---- THE COMMIT RECORDING + THE SELF-CONSISTENCY QUANTITY
        #      (G2, zero-knob asserted, fail=STOP) ------------------------
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
             "the commit sequence re-read is not a clean replay")
        coverage_ok = bool(out["coverage_ok"])
        assert coverage_ok, \
            f"{host} {row_key} s{seed}: the write-set coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        commits_finite_ok = bool(all(np.isfinite(v) for v in vals))
        assert commits_finite_ok, \
            f"{host} {row_key} s{seed}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        census_ok = bool(sum(census.values()) == n_commits
                         and set(tags) <= set(COMMIT_SOURCES))
        assert census_ok, \
            f"{host} {row_key} s{seed}: the commit source census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        # THE REPLAY: the commit sequence re-read — built ONLY from the
        # recorded commits (zero knobs: no re-simulation, no parameters,
        # no external target enters the replay). THE SELF-CONSISTENCY
        # ERROR: the RMS over the committed cells (the replay's support)
        # between the walk's final state and the replay.
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        sc_finite_ok = bool(np.isfinite(sc_rms))
        assert sc_finite_ok, \
            f"{host} {row_key} s{seed}: non-finite self-consistency RMS"
        # audit-only: where the error lives — the committed pattern vs
        # the deep target on the program's own write set
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite commit-vs-target RMS"
        # the program-vs-target gap's denominator (the branch ratio)
        denom_ok = bool(err_exact > 0.0)
        assert denom_ok, \
            f"{host} {row_key} s{seed}: the program-vs-target gap == 0"
        sc_frac = float(sc_rms / err_exact)

        # ---- THE S0 ANCHOR (G1, fail=STOP): the production-budget
        #      re-run IS the landed machinery — exp256's deposited errs
        #      + exp282's deposited walks must reproduce BIT-EXACT ----
        s0_err_ok = bool(err == dep_rec["err"])
        s0_ver_ok = bool(bool(out["program_verified"])
                         == bool(dep_rec["verified"]))
        assert s0_err_ok, \
            (f"{host} {row_key} s{seed}: the fresh err {err} drifted from "
             f"exp256's deposited {dep_rec['err']} — S0 REFUTED")
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
             "one (the commit recording was NOT side-effect-free)")
        ee_ok = bool(err_exact == float(rec282["err_exact"]))
        assert ee_ok, \
            (f"{host} {row_key} s{seed}: the fresh err_exact drifted from "
             "exp282's deposited err_exact")
        rec = {"host": host, "seed": int(seed),
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
               "src_census": census,
               "sc_rms": sc_rms, "sc_finite_ok": sc_finite_ok,
               "sc_frac": sc_frac, "denom_ok": denom_ok,
               "cvt_rms": cvt_rms,
               "s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
               "walk_end_282_ok": we_ok, "trace_sha_282_ok": ts_ok,
               "err_exact_282_ok": ee_ok}
        return rec

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; the pre-named 20 records: exp243 4 + exp256 3 +
    #      exp272 4 + exp273 5 + exp282 4) --------------------------------
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
        ("exp282_trajectory_structure.json", "inputs"))

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
        assert total == 20, f"the chain record count {total} != 20"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

    # ---- THE COMPUTATION (ONE pass: the sha-asserted rebuild + the
    #      fresh 72-row battery at the production budget; the integrity
    #      section is a pure function of the deposits + the module bytes
    #      and is bit-compared across the two passes at assembly) -------
    def _compute_battery():
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (exp269's/exp280's/exp284's/exp285's/
        #      exp286's form, every rebuild bit-asserted against
        #      exp243's OWN records) -------------------------------------
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_bnd_dual_ok": 0, "n_canon_ok": 0,
                  "h0_echo_h1": False, "n_fmax_ok": 0, "n_nonneg_ok": 0,
                  "n_rows256": 0, "n_structure_ok": 0, "n_worst_eq_max": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows282": 0, "n_282_chain_ok": 0,
                  "n_host_table282_ok": 0,
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

        # ---- G1: THE EXP282 RE-READ (the anchor deposit) — the 72 row
        #      records with the walk shas + the err chain anchor + the
        #      deposited TRAJECTORY-CARRIED branch + the host means ---
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
        ht282 = {row["host"]: row for row in dep282["host_table"]}
        assert len(ht282) == 12, "exp282's host table drifted"
        means282 = {h: float(ht282[h]["walk_end_rms_mean"]) for h in hosts}
        counts["n_host_table282_ok"] = len(means282)

        # ---- G1: THE TARGETS (the pre-named carries, asserted
        #      bit-exact) --------------------------------------------------
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

        # ---- G1: THE PROVENANCE CHAINS (20 records) ---------------------
        chains = _verify_chains()

        # ---- THE FRESH IDENTITY BATTERY: the 72 substituted rows at
        #      the production budget (the S0 anchors on EVERY row,
        #      fail=STOP) --------------------------------------------------
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec282 = r282[(k, s, rk)]
                    rec = _decode_row(k, rk, ctx["deep"][inst]["spec"],
                                      med, s, ctx["fmax"], d, rec282)
                    rows_out.append(rec)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] 6 rows | errs {[r['err'] for r in hs]} | "
                  f"end_rms {[round(r['walk_end_rms'], 4) for r in hs]} | "
                  f"sc_rms {[round(r['sc_rms'], 5) for r in hs]} | "
                  f"sc_frac {[round(r['sc_frac'], 5) for r in hs]}",
                  flush=True)
        assert len(rows_out) == 72, \
            f"the battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"
        return {"rows": rows_out,
                "integrity": {"counts": counts,
                              "rebuild_report": rebuild_report,
                              "targets": targets,
                              "provenance_chains": chains,
                              "exp282_reread": {
                                  "n_rows": counts["n_rows282"],
                                  "branch": dep282["branch"],
                                  "host_table_walk_end_rms_means":
                                      means282}},
                "ro_before": ro_before,
                "lock_reads": len(_LOCK_LOG)}

    # ---- THE ASSEMBLY (a pure function of ONE pass's payload — the
    #      merge path and the in-process path share it verbatim; the two
    #      passes' assembled cores are bit-compared) ----------------------
    def _assemble(rows, integrity, lock_reads, ro_before_pass):
        assert len(rows) == 72, \
            f"the assembled battery produced {len(rows)} rows != 72"
        assert lock_reads == 72, "the S* lock count drifted"
        assert set(ro_before_pass.values()) == set(ro_before.values()), \
            "the payload's ro_before drifted from the entry record"
        seen = set()
        for r in rows:
            key = (r["host"], r["seed"], r["row_key"])
            assert key not in seen, f"duplicate row {key}"
            seen.add(key)
        assert len(seen) == 72, "the 72-row frame drifted"
        counts = integrity["counts"]
        means282 = integrity["exp282_reread"][
            "host_table_walk_end_rms_means"]
        mia = integrity["targets"]["mia_prod_err"]["values"]
        prem = integrity["targets"]["one_zone_premium"]["values"]

        # ---- the per-host table + THE BRANCH DISCRIMINANT (pre-named
        #      numeric bars: SC_FRAC_BAR 0.01 / SC_MIN_HOSTS 10) --------
        host_table = []
        for h in hosts:
            hs = [r for r in rows if r["host"] == h]
            assert len(hs) == 6, f"{h}: the 6 rows drifted"
            scs = [r["sc_rms"] for r in hs]
            gaps = [r["err_exact"] for r in hs]
            cvts = [r["cvt_rms"] for r in hs]
            fracs = [r["sc_frac"] for r in hs]
            settles = [r["settle_gap_abs"] for r in hs]
            errs = [r["err"] for r in hs]
            wes = [r["walk_end_rms"] for r in hs]
            mean_sc = float(np.mean(scs))
            mean_gap = float(np.mean(gaps))
            gap_ok = bool(mean_gap > 0.0)
            assert gap_ok, f"{h}: the mean program-vs-target gap <= 0"
            host_sc_ok = bool(mean_sc < SC_FRAC_BAR * mean_gap)
            mean8_dep = means282[h]
            mean8_ok = bool(float(np.mean(wes)) == mean8_dep)
            assert mean8_ok, \
                (f"{h}: the fresh per-host end-RMS mean {float(np.mean(wes))!r} "
                 f"drifted from exp282's deposited {mean8_dep!r}")
            census = {t: int(sum(r["src_census"][t] for r in hs))
                      for t in COMMIT_SOURCES}
            assert sum(census.values()) == sum(r["n_commits"] for r in hs), \
                f"{h}: the per-host commit census drifted"
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "mean_sc": mean_sc, "mean_gap": mean_gap,
                "mean_cvt": float(np.mean(cvts)),
                "sc_frac_of_means": float(mean_sc / mean_gap),
                "mean_sc_frac_rowwise": float(np.mean(fracs)),
                "host_self_consistent": host_sc_ok,
                "max_sc_row": float(max(scs)),
                "min_sc_row": float(min(scs)),
                "mean_err": float(np.mean(errs)),
                "mean_walk_end_rms": float(np.mean(wes)),
                "mean8_equals_exp282_host_table": mean8_ok,
                "mean_settle_gap": float(np.mean(settles)),
                "src_census": census})

        # ---- THE BRANCH (pre-named) ------------------------------------
        n_sc_hosts = sum(1 for row in host_table
                         if row["host_self_consistent"])
        if n_sc_hosts >= SC_MIN_HOSTS:
            branch_local = "SELF-CONSISTENT"
        else:
            branch_local = "SELF-DRIFT"
        o_cvt = [row["mean_cvt"] for row in host_table if row["outlier"]]
        c_cvt = [row["mean_cvt"] for row in host_table
                 if not row["outlier"]]
        o_sc = [row["mean_sc"] for row in host_table if row["outlier"]]
        c_sc = [row["mean_sc"] for row in host_table
                if not row["outlier"]]
        branch_discriminant = {
            "bars": {"SC_FRAC_BAR": SC_FRAC_BAR,
                     "SC_MIN_HOSTS": SC_MIN_HOSTS},
            "bars_pre_named_at": ("1f6f07f — fixed at pre-registration, "
                                  "never fit"),
            "n_self_consistent_hosts": n_sc_hosts,
            "per_host_self_consistent": {row["host"]:
                                         row["host_self_consistent"]
                                         for row in host_table},
            "per_host_mean_sc": {row["host"]: row["mean_sc"]
                                 for row in host_table},
            "per_host_mean_gap": {row["host"]: row["mean_gap"]
                                  for row in host_table},
            "per_host_sc_frac_of_means": {row["host"]:
                                          row["sc_frac_of_means"]
                                          for row in host_table},
            "sc_frac_range_of_means": [
                min(row["sc_frac_of_means"] for row in host_table),
                max(row["sc_frac_of_means"] for row in host_table)],
            "outlier_vs_cluster_sc": {
                "outlier_mean_sc": o_sc,
                "cluster_mean_sc_range": [min(c_sc), max(c_sc)]},
            "outlier_vs_cluster_cvt": {
                "outlier_mean_cvt": o_cvt,
                "cluster_mean_cvt_range": [min(c_cvt), max(c_cvt)]},
            "ordering_by_sc_frac_of_means": [
                {"host": row["host"],
                 "sc_frac_of_means": row["sc_frac_of_means"],
                 "self_consistent": row["host_self_consistent"],
                 "outlier": row["outlier"]}
                for row in sorted(host_table,
                                  key=lambda r: r["sc_frac_of_means"])],
            "source_census_total": {
                t: int(sum(row["src_census"][t] for row in host_table))
                for t in COMMIT_SOURCES},
            "branch": branch_local}

        # ---- the audit-only drift regressions (the exp274/exp275/
        #      exp282 conventions VERBATIM: Spearman = Pearson on the
        #      tied-average ranks; the single-predictor OLS rank R2;
        #      the ties census per vector; NEVER gating) ---------------
        def _pearson(xs, ys):
            xa = np.asarray(xs, dtype=float)
            ya = np.asarray(ys, dtype=float)
            return float(np.corrcoef(xa, ya)[0, 1])

        def _spearman(xs, ys):
            rx = rankdata(np.asarray(xs, dtype=float))
            ry = rankdata(np.asarray(ys, dtype=float))
            return _pearson(rx, ry)

        def _r2(cols, rk):
            Xd = np.asarray([[1.0] + list(row) for row in zip(*cols)],
                            dtype=float)
            ya = np.asarray(rk, dtype=float)
            beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
            resid = ya - Xd @ beta
            sstot = float(((ya - ya.mean()) ** 2).sum())
            return float(1.0 - float((resid ** 2).sum()) / sstot)

        def _ties_census(vals):
            vs = sorted(float(v) for v in vals)
            levels = sorted(set(vs))
            mults = [vs.count(v) for v in levels]
            return {"n_distinct": len(levels),
                    "n_tied_values": sum(1 for m in mults if m > 1),
                    "max_multiplicity": int(max(mults))}

        TARGET_COLS = {"mia_prod_err": [mia[h] for h in hosts],
                       "one_zone_premium": [prem[h] for h in hosts]}
        regressions = {}
        for qk in ("mean_sc", "mean_cvt"):
            xs = [next(row for row in host_table if row["host"] == hh)[qk]
                  for hh in hosts]
            for tk, tvals in TARGET_COLS.items():
                rho = _spearman(xs, tvals)
                rk_resp = rankdata(np.asarray(xs, dtype=float))
                r2_single = _r2([tvals], rk_resp)
                r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))],
                             rk_resp)
                regressions[f"{qk}~{tk}"] = {
                    "quantity": qk, "target": tk,
                    "rho": rho, "rho_abs": abs(rho),
                    "rank_R2_single": r2_single,
                    "rank_R2_all_ranks": r2_all,
                    "all_ranks_minus_rho2": r2_all - rho * rho,
                    "ties_carrier": _ties_census(xs),
                    "ties_target": _ties_census(tvals),
                    "gating": False,
                    "role": ("audit-only — the drift face (never gating; "
                             "the branch is the sc fraction "
                             "discriminant)")}

        # ---- the S0 + G2 tallies (from the rows) -----------------------
        n_s0_err = sum(1 for r in rows if r["s0_err_ok"])
        n_s0_ver = sum(1 for r in rows if r["s0_verified_ok"])
        n_we282 = sum(1 for r in rows if r["walk_end_282_ok"])
        n_ts282 = sum(1 for r in rows if r["trace_sha_282_ok"])
        n_ee282 = sum(1 for r in rows if r["err_exact_282_ok"])
        n_mean282 = sum(1 for row in host_table
                        if row["mean8_equals_exp282_host_table"])
        n_count = sum(1 for r in rows if r["commits_count_ok"])
        n_uniq = sum(1 for r in rows if r["commits_unique_ok"])
        n_cov = sum(1 for r in rows if r["coverage_ok"])
        n_fin = sum(1 for r in rows if r["commits_finite_ok"])
        n_cens = sum(1 for r in rows if r["census_ok"])
        n_scfin = sum(1 for r in rows if r["sc_finite_ok"])
        n_denom = sum(1 for r in rows if r["denom_ok"])
        n_a3 = sum(1 for r in rows if r["a3_ok"])
        n_tlen = sum(1 for r in rows if r["trace_len_ok"])
        n_fpos = sum(1 for r in rows if r["walk_end_rms"] > 0.0)
        n_conv = sum(1 for r in rows if r["conv_step"] >= 0)
        max_settle = max(float(r["settle_gap_abs"]) for r in rows)
        n_digests = sum(1 for r in rows
                        if len(r["commit_seq_sha256"]) == 64)

        g1 = dict(counts)
        g1.update({"n_s0_err_ok": n_s0_err, "n_s0_verified_ok": n_s0_ver,
                   "n_walk_end282_ok": n_we282, "n_trace282_ok": n_ts282,
                   "n_errexact282_ok": n_ee282, "n_mean282_ok": n_mean282})
        g2 = {"n_rows": len(rows),
              "n_commits_count_ok": n_count,
              "n_commits_unique_ok": n_uniq,
              "n_coverage_ok": n_cov,
              "n_commits_finite_ok": n_fin,
              "n_census_ok": n_cens,
              "n_digests_ok": n_digests,
              "n_sc_finite_ok": n_scfin,
              "n_denominators_ok": n_denom,
              "n_a3_ok": n_a3, "n_trace_len_ok": n_tlen,
              "n_final_positive_ok": n_fpos, "n_conv_ok": n_conv,
              "n_lock_reads": lock_reads,
              "max_settle_gap": max_settle}
        g3 = {"branch": branch_local,
              "n_self_consistent_hosts": n_sc_hosts,
              "bars": {"SC_FRAC_BAR": SC_FRAC_BAR,
                       "SC_MIN_HOSTS": SC_MIN_HOSTS},
              "n_audit_regressions": len(regressions),
              "all_regression_rhos_finite": bool(
                  all(np.isfinite(v["rho"])
                      for v in regressions.values())),
              "all_host_means_finite": bool(
                  all(np.isfinite(row["mean_sc"])
                      and np.isfinite(row["mean_gap"])
                      and np.isfinite(row["mean_cvt"])
                      for row in host_table))}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": integrity, "rows": rows,
                "host_table": host_table, "regressions": regressions,
                "branch": branch_local,
                "branch_discriminant": branch_discriminant,
                "g1": g1, "g2": g2, "g3": g3,
                "ro_before": ro_before_pass}

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    def _core_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the default is
    #      the TWO-PASS IN-PROCESS form (72 decodes per pass, ~2-4 min
    #      total, far under the 570 s cap); the pre-named alternative is
    #      the CHECKPOINT-SPLIT pass1|pass2 + merge — each pass a
    #      separate process, the merge comparing the two cached payloads
    #      BIT-EXACT and never re-decoding) ------------------------------
    _MODE = os.environ.get("EXP287_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp287_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp287_pass2.checkpoint.json")}

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

    if _MODE in ("pass1", "pass2"):
        tag = 1 if _MODE == "pass1" else 2
        payload = _compute_battery()
        ck = _CK[tag]
        assert not os.path.exists(ck), \
            (f"{ck} already holds a payload — the split form caches "
             "exactly one payload per pass")
        with open(ck, "w") as fh:
            json.dump(payload, fh, sort_keys=True)
        print(f"  checkpointed {_MODE} (sha {_payload_sha(payload)[:16]})")
        _exit_checks()
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
        assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
            "floor drift at exit"
        return {"mode": _MODE, "payload_sha256": _payload_sha(payload)}

    if _MODE == "merge":
        cached = {}
        for tag in (1, 2):
            with open(_CK[tag]) as fh:
                cached[tag] = json.load(fh)
        sa = _payload_sha(cached[1])
        sb = _payload_sha(cached[2])
        assert sa == sb, \
            (f"the two pass payloads diverged: {sa[:16]} vs {sb[:16]} "
             "— the byte-identity check FAILED")
        core_a = _assemble(cached[1]["rows"], cached[1]["integrity"],
                           int(cached[1]["lock_reads"]),
                           cached[1]["ro_before"])
        core_b = _assemble(cached[2]["rows"], cached[2]["integrity"],
                           int(cached[2]["lock_reads"]),
                           cached[2]["ro_before"])
        sha_a, sha_b = _core_sha(core_a), _core_sha(core_b)
        deterministic = bool(sha_a == sha_b)
        assert deterministic, "the two passes' assembled cores diverged"
        core = core_a
        ro_before_a = cached[1]["ro_before"]
        for tag in (2,):
            assert cached[tag]["ro_before"] == ro_before_a, \
                f"ro_before drifted across passes (pass{tag})"
        run_form = "checkpoint-split pass1|pass2 + merge"
    else:
        print("=== exp287: THE FIXED POINT'S IDENTITY (is the walk's "
              "error the executed program's own self-consistency "
              "limit?) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows at the production budget "
              f"{BUDGET} (== exp142's STEPS_PER_CELL), TWO passes (G4)")
        print(f"  the read: the walk's OWN writes re-read as the target — "
              f"sc_rms = the RMS(final state, the commit replay) over the "
              f"committed cells; the branch bars SC_FRAC_BAR {SC_FRAC_BAR} "
              f"/ SC_MIN_HOSTS {SC_MIN_HOSTS}")

        pa = _compute_battery()
        pb = _compute_battery()
        sa = _payload_sha(pa)
        sb = _payload_sha(pb)
        assert sa == sb, \
            (f"the two pass payloads diverged: {sa[:16]} vs {sb[:16]} "
             "— the byte-identity check FAILED")
        core_a = _assemble(pa["rows"], pa["integrity"], pa["lock_reads"],
                           pa["ro_before"])
        core_b = _assemble(pb["rows"], pb["integrity"], pb["lock_reads"],
                           pb["ro_before"])
        sha_a, sha_b = _core_sha(core_a), _core_sha(core_b)
        deterministic = bool(sha_a == sha_b)
        assert deterministic, "the two passes' assembled cores diverged"
        core = core_a
        ro_before_a = pa["ro_before"]
        assert pb["ro_before"] == ro_before_a, \
            "ro_before drifted across passes (pass2)"
        run_form = "in-process two-pass"

    # ---- the gate assembly (evaluated exactly once, on pass a) ----------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(core["ro_before"].values())
                        and set(core["ro_before"].values())
                        == set(ro_before_a.values()))
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
        and g1["n_s0_err_ok"] == 72 and g1["n_s0_verified_ok"] == 72
        and g1["n_walk_end282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72 and g1["n_mean282_ok"] == 12
        and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
        and integrity["provenance_chains"]["total_verified"] == 20
        and ro_unchanged)
    g2_pass = bool(g2["n_rows"] == 72
                   and g2["n_commits_count_ok"] == 72
                   and g2["n_commits_unique_ok"] == 72
                   and g2["n_coverage_ok"] == 72
                   and g2["n_commits_finite_ok"] == 72
                   and g2["n_census_ok"] == 72
                   and g2["n_digests_ok"] == 72
                   and g2["n_sc_finite_ok"] == 72
                   and g2["n_denominators_ok"] == 72
                   and g2["n_a3_ok"] == 72
                   and g2["n_trace_len_ok"] == 72
                   and g2["n_final_positive_ok"] == 72
                   and g2["n_conv_ok"] == 72
                   and g2["n_lock_reads"] == 72)
    g3_pass = bool(g3["branch"] in ("SELF-CONSISTENT", "SELF-DRIFT")
                   and g3["n_self_consistent_hosts"]
                   == sum(1 for row in core["host_table"]
                          if row["host_self_consistent"])
                   and g3["n_audit_regressions"] == 4
                   and g3["all_regression_rhos_finite"]
                   and g3["all_host_means_finite"])

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
    bd = core["branch_discriminant"]
    host_table = core["host_table"]
    regressions = core["regressions"]
    n_sc = bd["n_self_consistent_hosts"]
    sc_frac_range = bd["sc_frac_range_of_means"]
    o_cvt = bd["outlier_vs_cluster_cvt"]["outlier_mean_cvt"]
    c_cvt = bd["outlier_vs_cluster_cvt"]["cluster_mean_cvt_range"]
    cens = bd["source_census_total"]

    if branch == "SELF-CONSISTENT":
        branch_text = (
            f"the walk lands exactly where it commits — the self-"
            f"consistency error is below {SC_FRAC_BAR} of the "
            f"program-vs-target gap on {n_sc}/12 hosts (>= the pre-named "
            f"{SC_MIN_HOSTS}): the premium is the program's imperfect "
            "self-knowledge — the committed pattern differs from the deep "
            "target, the error is IN the commit values, the chain closes "
            "at the compiler's program")
    else:
        branch_text = (
            f"the walk's final state differs from its own commits — the "
            f"between-commit dynamics + the settle move it (the exp284 "
            f"disclosed settle gap's amplified form): the self-consistency "
            f"error reaches >= {SC_FRAC_BAR} of the program-vs-target gap "
            f"beyond the bar on {12 - n_sc}/12 hosts (N_sc {n_sc}/12 < the "
            f"pre-named {SC_MIN_HOSTS})")

    verdict_body = (
        f"{branch} — {branch_text}"
        f" (N_sc {n_sc}/12 | the per-host sc fraction of means within "
        f"[{sc_frac_range[0]:.6f}, {sc_frac_range[1]:.6f}] vs the "
        f"pre-named bar {SC_FRAC_BAR} | WHERE THE ERROR LIVES "
        f"(audit-only): the commit-vs-target RMS mean_cvt — the "
        f"outliers H3/H5 {o_cvt[0]:.4f}/{o_cvt[1]:.4f} vs the cluster "
        f"[{c_cvt[0]:.4f}, {c_cvt[1]:.4f}] | the commits' source census "
        f"(audit-only): spec {cens['spec']} / canon {cens['canon']} / "
        f"parent {cens['parent']} over {sum(cens.values())} commits | "
        f"the audit-only drift regressions: rho(mean_sc)~mia "
        f"{regressions['mean_sc~mia_prod_err']['rho']:+.4f} / ~premium "
        f"{regressions['mean_sc~one_zone_premium']['rho']:+.4f}; "
        f"rho(mean_cvt)~mia "
        f"{regressions['mean_cvt~mia_prod_err']['rho']:+.4f} / ~premium "
        f"{regressions['mean_cvt~one_zone_premium']['rho']:+.4f} | THE "
        f"COMMIT RECORDING: n_commits == walk_steps == the trace length "
        f"{g2['n_commits_count_ok']}/72, the commit indices unique "
        f"{g2['n_commits_unique_ok']}/72, the write-set coverage "
        f"{g2['n_coverage_ok']}/72, the commit digests recorded "
        f"{g2['n_digests_ok']}/72; the settle gap max "
        f"{g2['max_settle_gap']:.4f} mV, audit-only | THE S0 ANCHOR: the "
        f"fresh errs reproduce exp256's deposited substituted errs "
        f"bit-exact ({g1['n_s0_err_ok']}/72, the verified flags "
        f"{g1['n_s0_verified_ok']}/72) AND exp282's walk_end_rms "
        f"bit-exact (walk_end_rms {g1['n_walk_end282_ok']}/72, trace "
        f"sha256 {g1['n_trace282_ok']}/72 — the SAME walk exp282 "
        f"deposited, err_exact {g1['n_errexact282_ok']}/72, the "
        f"per-host means {g1['n_mean282_ok']}/12; the recording "
        f"side-effect-free) | 12 hosts, a deterministic sha-asserted "
        f"rebuild (graph_path for H0/H1, small_world at the deposited "
        f"rewire seeds — exp269's/exp280's form), the provenance chains "
        f"sha-verified 20/20, 5 deposits READ-ONLY byte-unchanged, "
        f"two-pass bit-identical ({run_form}), floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp287_fixed_point_identity",
        "claim": (
            "THE FIXED POINT'S IDENTITY (batch 45, pre-registration "
            "commit 1f6f07f): is the walk's error the executed program's "
            "own self-consistency limit? exp282 landed TRAJECTORY-CARRIED "
            "on walk_end_rms (the PRE-settle trace[-1]; +0.8826151316282213 "
            "~ mia / +0.8807017543859651 ~ the premium) and exp286 landed "
            "the endpoint BUDGET-INVARIANT — the premium is the walk's "
            "fixed point at every step budget. This module asks WHAT the "
            "fixed point is: the state-carrying traced replica (exp286's "
            "landed form reused verbatim at the production budget 8 == "
            "exp142's STEPS_PER_CELL) re-runs the substituted rows (12 "
            "hosts x 3 seeds x the two deep instances at n=400 — "
            "exp256's battery) with ONE disclosed recording addition: "
            "the inherited/committed theta per cell recorded AT THE "
            "WRITE with the source tag (draws nothing from the RNG "
            "stream, touches no state — proven by the S0 anchor's "
            "bit-exact trace shas). At the walk's end the target for "
            "the self-consistency read is the COMMITTED pattern itself "
            "(the program's own output read as its target). Pre-named "
            "reads: (1) the self-consistency error sc_rms = the RMS "
            "over the committed cells between the walk's final state "
            "and a REPLAY of its own commits (the commit sequence "
            "re-read — zero knobs: built ONLY from the recorded "
            "commits, no re-simulation, no parameters, no external "
            "target); (2) the program-vs-target gap = err_exact (the "
            "production err vs the deep target, exp256's deposited "
            "errs the anchor; the support difference disclosed); "
            "(3) the branch SELF-CONSISTENT (mean_sc < 1% of mean_gap "
            "on >= 10/12 hosts — the walk lands exactly where it "
            "commits: the premium is the program's imperfect "
            "self-knowledge, the error IN the commit values, the chain "
            "closing at the compiler's program) / SELF-DRIFT (the "
            "final state differs from its own commits — the "
            "between-commit dynamics + the settle move it, the exp284 "
            "disclosed settle gap's amplified form), bars SC_FRAC_BAR "
            "0.01 / SC_MIN_HOSTS 10 fixed at pre-registration, never "
            "fit"),
        "method": {
            "replica": (
                "exp286's landed _execute_signed_traced REUSED VERBATIM "
                "(landed 4e504de: exp142's walk byte-similar + the "
                "disclosed recording additions (a)-(e) + the budget "
                "parameterization) at the production budget 8 == "
                "exp142's STEPS_PER_CELL (asserted; exp286 closed the "
                "dose axis — no ladder here) with ONE DISCLOSED "
                "RECORDING ADDITION: (f) the inherited/committed theta "
                "per cell (theta_new, whatever its source) recorded AT "
                "THE WRITE, after the write, with the source tag "
                "spec/canon/parent; the recording draws NOTHING from "
                "the RNG stream and touches no state — proven by the "
                "S0 anchor's bit-exact trace sha256 + walk_end_rms "
                "(the SAME walk exp282 deposited). The RNG stream, dt, "
                "canon, walk order, commits UNTOUCHED; exp142 NOT "
                "modified"),
            "self_consistency": (
                "sc_rms = the RMS over the committed cells (the "
                "replay's support: exactly the cells the executed "
                "program wrote, each exactly once) between the walk's "
                "final state (the post-settle final_state read) and "
                "the REPLAY of its own commits (the commit sequence "
                "re-read: the recorded committed theta per cell, "
                "re-read in walk order); ZERO KNOBS — the replay is "
                "built ONLY from the recorded commits (no "
                "re-simulation, no parameters, no external target "
                "enters the replay); the replay covers the write set "
                "exactly (the commit count == walk_steps == the trace "
                "length; the commit indices unique; the replica-side "
                "elementwise coverage vs the walked order)"),
            "gap": (
                "err_exact — the A3-checked full-frame RMS between the "
                "final state and the deep target (the production err), "
                "ANCHORED: the reported errs reproduce exp256's "
                "deposited substituted errs BIT-EXACT 72/72 and "
                "err_exact reproduces exp282's 72/72; the supports "
                "differ by construction (the replay on the write set, "
                "the gap on the full frame) — the ratio is the "
                "pre-named read, the supports disclosed"),
            "branch_rule": (
                "per host mean_sc (the 6-row mean of sc_rms) vs "
                "mean_gap (the 6-row mean of err_exact); the host "
                "self-consistent iff mean_sc < SC_FRAC_BAR * mean_gap; "
                "SELF-CONSISTENT iff N_sc >= SC_MIN_HOSTS (10); else "
                "SELF-DRIFT. Bars SC_FRAC_BAR 0.01 / SC_MIN_HOSTS 10, "
                "fixed at pre-registration, never fit"),
            "regressions": (
                "the exp274/exp275/exp282 conventions VERBATIM: "
                "Spearman = Pearson on the tied-average ranks (scipy "
                "rankdata); the single-predictor OLS rank R2 (the "
                "response as its tied-average ranks, the target as the "
                "numeric design column) + the all-ranks variant "
                "AUDIT-ONLY; the ties census per vector; the 12-slot "
                "frame with the H0==H1 echo carried; the audit-only "
                "quantities mean_sc and mean_cvt against mia_prod_err "
                "(exp273's field table) and exp272's one-zone premium "
                "means; NOTHING gates on a rho in this module — the "
                "branch is the sc fraction discriminant"),
            "scope": (
                "NO classify/decompose/mask work on the identity rows "
                "— the question is commit-level; exp208's classify "
                "appears ONLY in the rebuild's boundary-count "
                "integrity check (the landed rebuild form); the full "
                "commit sequences NOT re-deposited — bit-reproduced "
                "via the per-row commit_seq_sha256 digests + G1's "
                "trace shas (the exp284/exp285/exp286 precedent)")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": core["ro_before"][name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base) + the mia audit errs "
                "(T_mia's direct carry)",
                "the 72 rows — the S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas",
                "the host frame + the per-host one-zone premium means "
                "(T_prem) + the boundary counts + the outlier "
                "pre-name source",
                "the outlier pre-name + the field-table carries (the "
                "mia field + the premium carry, bit-exact)",
                "the S0 walk anchor — the 72 per-row walk_end_rms + "
                "trace shas (the bit-exact same-walk anchor that also "
                "proves the commit recording side-effect-free) + the "
                "deposited TRAJECTORY-CARRIED branch + the host_table "
                "means + the err chain anchor vs exp256"))},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp282_reread": integrity["exp282_reread"],
        "provenance_chains": integrity["provenance_chains"],
        "targets": integrity["targets"],
        "rows": core["rows"],
        "host_table": host_table,
        "regressions": regressions,
        "branch": branch,
        "branch_discriminant": bd,
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": {
            "form": run_form,
            "computation_passes": 2,
            "decodes_per_pass": 72,
            "payload_sha256_pass_a": sa,
            "payload_sha256_pass_b": sb,
            "payloads_bit_identical": True,
            "core_sha256_pass_a": sha_a,
            "core_sha256_pass_b": sha_b,
            "two_pass_bit_identical": deterministic},
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
        "G1_rebuild_s0_anchor_integrity": {
            "pass": g1_pass,
            "counts": g1,
            "provenance_chains": integrity["provenance_chains"],
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "s0_anchor": (
                "the production-budget re-run's reported errs reproduce "
                "exp256's deposited substituted errs bit-exact (72/72, "
                "the machinery's native 2-dp convention) and exp282's "
                "walk_end_rms reproduces bit-exact (walk_end_rms + "
                "trace sha256 72/72 — the SAME walk exp282 deposited, "
                "which also proves the commit recording "
                "side-effect-free — plus err_exact 72/72 and the "
                "per-host means 12/12; asserted fail=STOP at decode)")},
        "G2_commit_recording_self_consistency_definition": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "the disclosed recording addition: the committed theta "
                "per cell recorded AT THE WRITE (after the write; the "
                "inherited/committed value whatever its source, with "
                "the source tag spec/canon/parent recorded audit-only) "
                "— draws nothing from the RNG stream, touches no state "
                "(proven by G1's bit-exact trace shas); per row: the "
                "commit count == walk_steps == the trace length; the "
                "commit indices unique (each committed cell exactly "
                "once — the commit sequence re-read is a clean "
                "replay); the replica-side write-set coverage (the "
                "commit sequence elementwise == the walked order); the "
                "commit values finite; the commit sequence digest "
                "sha256 recorded (the full sequences NOT re-deposited "
                "— bit-reproduced via the digest + G1's trace shas); "
                "THE REPLAY built ONLY from the recorded commits (no "
                "re-simulation, no parameters, no external target "
                "enters the replay); sc_rms finite; the denominators "
                "err_exact > 0; the A3 convention + the trace "
                "integrity + the TA3 convergence point asserted "
                "fail=STOP; the S* lock reads 72; the exp284-style "
                "settle gap recorded audit-only")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bars": ("per host mean_sc (the 6-row mean of sc_rms) vs "
                     "mean_gap (the 6-row mean of err_exact); the host "
                     "self-consistent iff mean_sc < SC_FRAC_BAR * "
                     "mean_gap (SC_FRAC_BAR 0.01); N_sc >= SC_MIN_HOSTS "
                     "(10) -> SELF-CONSISTENT; else SELF-DRIFT. "
                     "Audit-only, never gating: the per-row sc "
                     "fractions; the commit-vs-target RMS cvt_rms "
                     "(where the error lives); the per-row + per-host "
                     "source censuses; the exp284-style settle gaps; "
                     "the max/min per-row sc per host; the mean_sc / "
                     "mean_cvt regressions vs mia + the premium under "
                     "the house conventions"),
            "resolved": {"branch": branch,
                         "n_self_consistent_hosts": n_sc,
                         "sc_frac_range_of_means": sc_frac_range}},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_s0_anchor_integrity",
                 "G2_commit_recording_self_consistency_definition",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    gates["G4_discipline"] = {
        "pass": bool(deterministic and no_wall_clock and docstring_ok
                     and header_ok and ro_unchanged),
        "two_pass_bit_identical": deterministic,
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_1f6f07f": docstring_ok,
        "header_byte_unchanged_vs_1f6f07f": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "floor_at_entry": float(CORE.NEURAL_SPEC_MIN),
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

    print(f"\n  G1 rebuild + S0 anchor integrity: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the 12 bases rebuilt — graph_path for H0/H1, small_world at "
          f"the deposited seeds — sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the "
          f"classify boundary count {g1['n_bnd_dual_ok']}/12 dual-carried "
          f"vs exp272+exp273 + the canon identity {g1['n_canon_ok']}/12 + "
          f"H0 == H1 + f_max {g1['n_fmax_ok']}/12 + non-negative "
          f"{g1['n_nonneg_ok']}/12; the deep targets "
          f"{g1['n_deep_targets_ok']}/72 + the medium shas "
          f"{g1['n_medium_shas_ok']}/72; exp282's re-read: rows "
          f"{g1['n_rows282']}/72 + the err chain anchor "
          f"{g1['n_282_chain_ok']}/72 + branch "
          f"{integrity['exp282_reread']['branch']}; THE S0 ANCHOR — the "
          f"errs == exp256's deposited substituted errs bit-exact "
          f"{g1['n_s0_err_ok']}/72 + the verified flags "
          f"{g1['n_s0_verified_ok']}/72 AND exp282's walk_end_rms "
          f"bit-exact (walk_end {g1['n_walk_end282_ok']}/72, trace sha "
          f"{g1['n_trace282_ok']}/72, err_exact "
          f"{g1['n_errexact282_ok']}/72, the per-host means "
          f"{g1['n_mean282_ok']}/12); the carries mia {g1['n_mia_carry']}"
          f"/12 + premium {g1['n_prem_carry']}/12; the provenance chains "
          f"{integrity['provenance_chains']['total_verified']}/20)")
    print(f"  G2 commit recording + the self-consistency definition: "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(n_commits == walk_steps == the trace length "
          f"{g2['n_commits_count_ok']}/72; the commit indices unique "
          f"{g2['n_commits_unique_ok']}/72; the write-set coverage "
          f"{g2['n_coverage_ok']}/72; the values finite "
          f"{g2['n_commits_finite_ok']}/72; the censuses "
          f"{g2['n_census_ok']}/72; the digests {g2['n_digests_ok']}/72; "
          f"sc_rms finite {g2['n_sc_finite_ok']}/72; the denominators "
          f"{g2['n_denominators_ok']}/72; the A3 convention "
          f"{g2['n_a3_ok']}/72; the trace lengths {g2['n_trace_len_ok']}"
          f"/72; trace[-1] > 0 {g2['n_final_positive_ok']}/72; the "
          f"convergence points {g2['n_conv_ok']}/72; the S* lock reads "
          f"{g2['n_lock_reads']}/72; the settle gap max "
          f"{g2['max_settle_gap']:.4f} mV)")
    print("  the 12-host identity table (per-host means; H3/H5 the "
          "outliers):")
    for row in host_table:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} mean_sc {row['mean_sc']:.5f}  "
              f"mean_gap {row['mean_gap']:.4f}  sc/gap "
              f"{row['sc_frac_of_means']:.5f}"
              f"{'*' if row['host_self_consistent'] else ' '}  "
              f"mean_cvt {row['mean_cvt']:.4f}  "
              f"census {row['src_census']}{tag}")
    print("  G3 branch — the audit-only drift regressions (the "
          "exp274/exp275/exp282 conventions; NEVER gating):")
    for k, v in regressions.items():
        print(f"      {k:28s} rho {v['rho']:+.4f}")
    print(f"      the branch bars: SC_FRAC_BAR {SC_FRAC_BAR} | "
          f"SC_MIN_HOSTS {SC_MIN_HOSTS} | N_sc {n_sc}/12")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}, form {run_form}; "
          f"no wall-clock fields: {no_wall_clock}; 5 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged})")
    print(f"\n  BRANCH: {branch} | N_sc {n_sc}/12 | the per-host sc "
          f"fraction of means within [{sc_frac_range[0]:.6f}, "
          f"{sc_frac_range[1]:.6f}] vs the bar {SC_FRAC_BAR}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    # ---- the hard rules, re-asserted after the work ----------------------
    _exit_checks()
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
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
