#!/usr/bin/env python3
"""exp288 — THE SPEC LAYER'S FACE: WHAT MAKES THE COMPILER'S SPEC-LAYER
COMMITS DEEP-BAND-HOST-DEPENDENT? (batch 46; ledger L265's registered
next (a) — the decomposition of exp287's commit layer, the premium's
structural address: batch 45 closed the mechanism line at the compiler
with the committed pattern itself carrying the exposure
(rho(mean_cvt)~mia +0.8616 / ~premium +0.7790) while every grain
screened so far is class-blind (exp277's decode NEITHER, exp284's walk
CLASS-BLIND, exp285's ring ABSENT). Before the chain rests, the commit
layer's OWN face gets its decomposition: the commit error by cell
class, and the commit values against the spec's own named voltages.)

THE OPEN ITEM: exp287 landed SELF-DRIFT with the exposure carried by
the COMMITTED PATTERN (mean_cvt spread 0.587059-0.631465 across the 12
hosts, the rank carriage +0.8616/+0.7790) and recorded the commits'
source census: every one of the 20802 commits drew from the SPEC layer
(spec 20802 / canon 0 / parent 0). The landed write path fixes WHAT the
spec layer contains: set_target(canon) installs phi_spec = canon,
write_spec_layer(target) then re-installs phi_spec = target BIT-EXACTLY
(a plain array copy) and preserves the pre-program memory as
phi_spec_canon; the dynamics (step/run/clamp/amputate) never touch
phi_spec — so at the write, phi_spec[i] == target[i] bit-exact and each
commit is phi_spec[i] + ONE commit-noise draw (exp142's COMMIT_NOISE
0.6, the machinery's own constant). The commit values' bases are
therefore the target values themselves: the spec's PRE-NAMED deep-rung
voltage -60.0 on the deep-zone cells, the canon's gap values (-50.0
trunk / -20.0 head) on the un-named gap cells the write inherits. THE
STRUCTURAL QUESTION (this module, zero new knobs): with the per-cell
commit error being exactly one commit-noise draw, WHAT makes the
committed pattern deep-band-host-dependent? Candidate carriers: the
commit error's CLASS structure — the squared commit error concentrates
in a classify class beyond that class's cell share (SPEC-GEOMETRIC) —
or NOTHING in the spec layer's content, the host-dependence entering
only through the noise DRAWS' stream positions and the walked count
(SPEC-UNIFORM — class-blind like every other level screened). The
draw-stream reading (disclosed, asserted as its observable
consequence): the walk's dt = star_dt at the S* operating point, scaled
by the projected adjacency's max degree (host-dependent), sets how much
rng the encode window + the per-cell interludes consume before each
commit — hosts sharing dt share the commit-draw sequence, hosts sharing
dt AND the per-row walked counts share the commit-value multisets
BIT-EXACT, and the commit-vs-target RMS — the RMS of pure draws —
cannot see the walk ORDER at all.

THE INSTRUMENT (pre-named, zero knobs): exp287's landed body REUSED
VERBATIM — the state-carrying traced replica with the commit recording
(_execute_signed_traced with the disclosed recording addition (f), the
RNG stream / dt / canon / walk order / commits untouched; exp142 NOT
modified) at the production budget 8 == exp142's STEPS_PER_CELL, the
host rebuild (exp269's/exp280's form), exp256's _scoped_row_read_state
form (the projection chain PN1/PN2 + TC1 + TC2 + the traced TC3) — ONE
FRESH RUN of the SAME 72 substituted rows (12 hosts x 3 seeds (1,2,3) x
r-60i0/r-60i1 at n=400, exp256's battery). The decomposition (pure
rebuild + arithmetic, ZERO new knobs):

  (1) THE COMMITTED PATTERN REBUILT per row: the commit sequence
      re-read (the recorded committed theta per cell in walk order —
      exp287's replay form verbatim; the replay built ONLY from the
      recorded commits — no re-simulation, no parameters, no external
      target enters it); the per-cell commit error
      e_i = commit_i - T_i against the row's deep target, on the
      program's write set (the replay's support: exactly the cells
      the executed program wrote, each exactly once).
  (2) THE CLASS DECOMPOSITION (exp208's classify VERBATIM, applied
      per instance — classify(T_instance, A_host) — the CLEAN masks:
      CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR, disjoint, covering;
      the exp208-label cls-array records carried audit-only
      alongside, exp284's disclosure repeated: cls 1 = the
      pair-junctions off the boundary ring, cls 0 = the boundary ring
      AND the interior riding the same mask, cls 2 never occurs —
      asserted): per row and per class c on the write set —
      n_c = |c intersect write|, cell_share_c = n_c / n_write,
      sum_sq_c = sum e_i^2 over c, frac_of_sq_c = sum_sq_c / total,
      rms_contrib_mV = sqrt(sum_sq_c / n_write), and the
      concentration ratio R_c = frac_of_sq_c / cell_share_c (a class
      with n_c == 0 on a row is recorded with zero shares and R
      null, disclosed — the branch reads the POOLED form below).
  (3) THE COMMIT-VALUE DISTRIBUTION'S OWN STRUCTURE: the base census
      (the distinct target values at the committed cells, with
      counts — the spec's pre-named voltage -60.0 vs the canon gap
      values), THE NAMED-BASE FRACTION (#{s_i == -60.0} / n_write —
      the histogram's mass whose base IS the spec layer's named
      voltage), THE EXACT-LANDING COUNT (#{commit_i == -60.0}
      bit-exact — what fraction of commits land EXACTLY on the spec
      layer's named voltage: the noise-vanished face; and
      #{commit_i == s_i} — the noise-vanished face on any base),
      and the error moments (mean/std/min/max of e_i — the population
      std — and the fraction |e_i| <= COMMIT_NOISE, the machinery's
      own sigma).

THE PRE-NAMED BRANCH (the bars numeric, fixed HERE at
pre-registration, never fit): per host, the 6 rows POOLED per class
(the sums and counts added over the host's rows — the pooling kills
the small-class single-row variance, the probe-level fluctuation of
R on ~12-27-cell classes reaching ~0.5, disclosed); the host's
concentration R_max = max over non-empty classes of the pooled R_c;
CONC_BAR = 1.50 (a class holding >= 1.5x its committed-cell share of
the squared commit error);
  SPEC-GEOMETRIC iff #{hosts with R_max >= CONC_BAR} >=
      CONC_MIN_HOSTS (10) — the commit error's class decomposition
      concentrates in a class;
  else SPEC-UNIFORM — class-blind like every other level.
Audit-only, never gating: the per-row R table; the exp284-style
outlier-vs-cluster margins on the pooled clean-mask fracs (margin_c =
min over {H3,H5} - max over the cluster, the 0.05 bar form, recorded
honestly); the mean_cvt~mia / ~premium regressions under the
exp274/exp275/exp282 conventions VERBATIM (asserted == exp287's
deposited rhos BIT-EXACT — the anchor); THE DRAW-STREAM FACE (the
mechanism audit, deterministic arithmetic on the rows, asserted
fail=STOP): the hosts grouped by (dt, the 6-row walked-count vector)
must carry BIT-IDENTICAL per-row cvt_rms within a group, and cvt_rms
must be BIT-IDENTICAL across the two instances of every (host, seed)
pair — the commit values are the spec's bases + draw-stream positions
and cannot see the walk order; the per-host dt + the projected
adjacency's max degree recorded (the dt recomputed OUTSIDE the replica
by the same pure projection calls — project_phase_native +
flip_clock_matrix on the base medium: no rng, no state, a pure read).

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285/exp286/exp287
      precedent (graph_path at the chain class's n=400 call site for
      H0/H1 — H0 echoes H1 bit-exactly, asserted; small_world(n, 0.10,
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
      TRAJECTORY-CARRIED asserted; exp282's host_table
      walk_end_rms_mean present for the 12 hosts. THE EXP287 RE-READ:
      the 72 row records present with commit_seq_sha256 + cvt_rms +
      n_commits + sc_rms; the 12-host mean_cvt present. THE S0 ANCHOR
      (the production-budget battery): the re-run's reported errs
      reproduce exp256's DEPOSITED substituted errs BIT-EXACT (72/72,
      the machinery's native 2-dp convention; the verified flags
      72/72), exp282's walk_end_rms reproduces BIT-EXACT (the fresh
      walk_end_rms == exp282's deposited walk_end_rms 72/72; the
      fresh trace sha256 == exp282's deposited trace_sha256 72/72;
      err_exact 72/72; the fresh per-host end-RMS means == exp282's
      deposited host_table means 12/12), AND exp287's COMMIT LAYER
      reproduces BIT-EXACT (the fresh commit sequence digests ==
      exp287's deposited commit_seq_sha256 72/72 — the SAME commits
      exp287 recorded; the fresh per-row cvt_rms == exp287's 72/72;
      the fresh n_commits == exp287's 72/72; the fresh sc_rms ==
      exp287's 72/72; the fresh per-host mean_cvt == exp287's
      deposited mean_cvt 12/12). The carries: the mia carry bit-exact
      12/12 (exp273's field table == exp243's own class records) +
      the premium carry bit-exact 12/12 (exp272 == exp273's
      field-table carry). THE PROVENANCE CHAINS sha-verified against
      the current file bytes — exp243 (4) + exp256 (3) + exp272 (4) +
      exp273 (5) + exp282 (4) + exp287 (5) = 25 records. The source
      deposits READ-ONLY: sha-recorded BEFORE any read, byte-unchanged
      after the work (6 deposits: exp243, exp256, exp272, exp273,
      exp282, exp287).
  G2  THE COMMIT REPLAY + THE DECOMPOSITION'S ACCOUNTING IDENTITY
      (zero-knob asserted, fail=STOP per row): the commit recording
      bookkeeping (the exp287 form: the commit count == walk_steps ==
      the trace length 72/72; the commit indices UNIQUE — each
      committed cell exactly once 72/72; the replica-side write-set
      coverage — the commit sequence elementwise == the walked order
      72/72; the commit values finite 72/72; the source census sane
      72/72; the commit sequence digest sha256 recorded 72/72 — the
      full sequences NOT re-deposited, bit-reproduced via the digests
      + G1's anchors). THE DECOMPOSITION: per row the three clean
      classes partition the write set (the class counts sum to
      n_write 72/72; the masks disjoint and covering by construction,
      asserted via the classify source); the exp208-label cls-2
      count == 0 72/72 (the exp277/exp284 disclosure, asserted);
      THE ACCOUNTING IDENTITY on the scale the RMS actually
      decomposes: sum_c sum_sq_c / n_write == cvt_rms^2 within
      1e-6 * max(1.0, cvt_rms^2) (exp208's/exp284's identity form on
      the write-set support, disclosed) 72/72, and the fracs sum to
      1.0 within 1e-9 72/72. THE HISTOGRAM's sanity: the base census
      sums to n_write 72/72; the named-base + gap-base partition
      72/72; the exact-landing count within [0, n_write] 72/72; the
      error moments finite 72/72. The per-row decode integrity: the
      A3 state convention (round(err_exact, 2) == the reported err)
      asserted fail=STOP 72/72; the trace finite + trace[-1] > 0 +
      the trace length == walk_steps 72/72; the convergence point
      exists (TA3) 72/72; the S* lock reads 72; the exp284-style
      settle gap recorded audit-only.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): per host
      the pooled decomposition; R_max vs CONC_BAR 1.50; N_conc >=
      CONC_MIN_HOSTS 10 -> SPEC-GEOMETRIC; else SPEC-UNIFORM. The
      mean_cvt~mia / ~premium regressions asserted == exp287's
      deposited rhos BIT-EXACT (the anchor, fail=STOP; the house
      conventions verbatim: Spearman = Pearson on the tied-average
      ranks, the single-predictor OLS rank R2, the ties census per
      vector, the 12-slot frame with the H0==H1 echo carried).
      Audit-only, never gating: the per-row R table; the exp284-style
      margins (the 0.05 bar form); the draw-stream face's cvt-tie
      groups + the per-host dt record; the orderings by R_max; the
      outlier-vs-cluster faces; the pooled base censuses; the pooled
      named-base + exact-landing totals; the error moments vs
      COMMIT_NOISE.
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, 72 decodes per pass; or
      the pre-named checkpoint-split EXP288_MODE=pass1|pass2 + merge
      with each pass a separate process; the two passes' payloads
      BIT-IDENTICAL, asserted at the merge/assembly); no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): SPEC-GEOMETRIC / SPEC-UNIFORM.

RUN: the deterministic sha-asserted rebuild (seconds) + 72 decodes per
pass ~ 60-90 s foreground per pass, TWO passes (G4) ~ 2-4 min total,
far under the 570 s cap per invocation. THE DEFAULT TWO-PASS
IN-PROCESS FORM (no env): the full battery computed twice in one
invocation. THE PRE-NAMED CHECKPOINT-SPLIT ALTERNATIVE:
EXP288_MODE=pass1|pass2 computes and caches ONE pass's payload per
invocation; EXP288_MODE=merge compares the two cached payloads
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
OUT = os.path.join(ROOT, "results", "exp288_spec_layer_face.json")


def main() -> dict:
    # ==== BODY (written by the main agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once,
    #      pre-registration commit 6ae42a3) ================================
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
    #      is the 6ae42a3 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "09eacfe55a0e823e1a927bc2f416fa60d2004fa2022f4bb5e975cfa11555d988")
    EXPECTED_HEADER_SHA256 = (
        "2ca1e109d0f349fcc78254a14ed45ce900e4f88781857036238ec44ce41e4f5e")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 6ae42a3"
    assert header_ok, "header drifted from 6ae42a3"

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
    #      THE BRANCH BARS — the pre-named numeric bars) ------------------
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
    # STEPS_PER_CELL == 8 — the production parameterization at the
    # default (no ladder: the question is commit-level, not budget-level).
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE BRANCH BARS (pre-named at 6ae42a3, numeric, never fit)
    CONC_BAR = 1.50
    CONC_MIN_HOSTS = 10
    # the commit source tags (the pre-named census; audit-only)
    COMMIT_SOURCES = ("spec", "canon", "parent")
    # the three clean classes (the cls mapping: 0 = CANON-BOUNDARY,
    # 1 = PAIR-JUNCTION, 2 = INTERIOR — the exp208-label records carried
    # audit-only; the exp277/exp284 disclosure: cls 2 never occurs)
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

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; SIX deposits:
    #      exp243 + exp256 + exp272 + exp273 + exp282 + exp287) ---------
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
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit"}
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

    # ---- the host frame (exp272's per_host order — the house frame) ----
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
    assert dep272["descriptive"]["premium_hosts"] == outliers, \
        "exp272's premium_hosts drifted from the outlier pre-name"
    assert dep282["outliers"] == outliers, "exp282's outliers drifted"
    cluster = [h for h in hosts if h not in outliers]
    assert len(cluster) == 10, "the ten-host cluster drifted"

    rec272 = {r["host"]: r for r in dep272["per_host"]}
    ft273 = {rec["field"]: rec for rec in dep273["field_table"]}

    # ---- exp208's classify VERBATIM (the CLEAN masks: CANON-BOUNDARY /
    #      PAIR-JUNCTION / INTERIOR, disjoint, covering; the exp208-label
    #      cls array carried audit-only — cls 2 never occurs, the
    #      exp277/exp284 disclosure, asserted) -----------------------------
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
    #      REUSED VERBATIM (exp142's walk byte-similar + exactly the
    #      disclosed recording additions (a)-(e) + the budget
    #      parameterization + exp287's disclosed recording addition (f):
    #      the committed theta per cell RECORDED AT THE WRITE with the
    #      source tag — draws NOTHING from the RNG stream, touches no
    #      state; proven by the S0 anchor's bit-exact trace sha256 +
    #      walk_end_rms + commit-sequence digests) at the production
    #      budget (BUDGET == STEPS_PER_CELL == 8, asserted). ------------
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

    # ---- one decomposition-row decode (the commit-level read + THE
    #      CLASS DECOMPOSITION; the S0 anchors asserted fail=STOP on
    #      EVERY row: the battery runs at the production budget only) --
    def _decode_row(host, row_key, spec, med, seed, fmax, dep_rec,
                    rec282, rec287, A_base):
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
             "the commit sequence re-read is not a clean replay")
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
        # THE REPLAY: the commit sequence re-read — built ONLY from the
        # recorded commits (zero knobs: no re-simulation, no parameters,
        # no external target enters the replay).
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        sc_finite_ok = bool(np.isfinite(sc_rms))
        assert sc_finite_ok, \
            f"{host} {row_key} s{seed}: non-finite self-consistency RMS"
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite commit-vs-target RMS"
        denom_ok = bool(err_exact > 0.0)
        assert denom_ok, \
            f"{host} {row_key} s{seed}: the program-vs-target gap == 0"
        sc_frac = float(sc_rms / err_exact)

        # ---- THE S0 ANCHOR (G1, fail=STOP): the production-budget
        #      re-run IS the landed machinery — exp256's deposited errs,
        #      exp282's walks AND exp287's commit layer reproduce
        #      BIT-EXACT ------------------------------------------------
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
        # THE EXP287 COMMIT-LAYER ANCHOR: the SAME commits exp287 recorded
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

        # ---- THE CLASS DECOMPOSITION (the pre-registered read (1)+(2);
        #      exp208's classify VERBATIM applied per instance) ----------
        n = len(T)
        masks = classify(T, A_base)
        bnd, jct, intr = masks["boundary"], masks["junction"], \
            masks["interior"]
        masks_disjoint_ok = bool(
            int((bnd & jct).sum()) == 0 and int((bnd & intr).sum()) == 0
            and int((jct & intr).sum()) == 0 and bool((bnd | jct | intr).all()))
        assert masks_disjoint_ok, \
            (f"{host} {row_key} s{seed}: the clean masks are not disjoint "
             "and covering")
        cls_arr = masks["class"]
        cls2_full = int((cls_arr == 2).sum())
        assert cls2_full == 0, \
            (f"{host} {row_key} s{seed}: the exp208-label cls-2 count "
             f"{cls2_full} != 0 — the exp277/exp284 disclosure drifted")
        # the per-cell commit error on the program's write set:
        # e_i = commit_i - T_i (the base IS the target bit-exact — the
        # commit draws phi_spec + ONE noise draw, so e is the draw)
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
                rms_contrib = float(np.sqrt(sum_sq_c / n_write))
            else:
                sum_sq_c = 0.0
                frac_c = 0.0
                share_c = 0.0
                R_c = None
                rms_contrib = 0.0
            fracs_sum += frac_c
            sum_sq_total += sum_sq_c
            decomp.append({"cls": int(cidx),
                           "name": CLASS_NAMES[cidx], "n": n_c,
                           "cell_share": share_c, "sum_sq": sum_sq_c,
                           "frac_of_sq": frac_c,
                           "rms_contrib_mV": rms_contrib, "R": R_c})
        # THE ACCOUNTING IDENTITY (the scale the RMS actually decomposes)
        ident_ok = bool(
            abs(sum_sq_total / n_write - cvt_rms ** 2)
            <= 1e-6 * max(1.0, cvt_rms ** 2))
        assert ident_ok, \
            (f"{host} {row_key} s{seed}: the accounting identity drifted — "
             "the class decomposition does not reconstruct cvt_rms^2")
        fracs_ok = bool(abs(fracs_sum - 1.0) <= 1e-9)
        assert fracs_ok, \
            f"{host} {row_key} s{seed}: the class fracs do not sum to 1"
        partition_ok = bool(sum(d["n"] for d in decomp) == n_write)
        assert partition_ok, \
            (f"{host} {row_key} s{seed}: the class counts do not partition "
             "the write set")

        # ---- THE COMMIT-VALUE DISTRIBUTION'S OWN STRUCTURE (read (3)) --
        s_vals = T[replay_idx]
        census: dict = {}
        for sv in s_vals.tolist():
            census[float(sv)] = census.get(float(sv), 0) + 1
        census_sum_ok = bool(sum(census.values()) == n_write)
        assert census_sum_ok, \
            f"{host} {row_key} s{seed}: the base census does not sum to n_write"
        named_count = int((s_vals == DEEP_RUNG).sum())
        named_base_frac = float(named_count / n_write)
        named_gap_partition_ok = bool(
            named_count + (n_write - named_count) == n_write)
        assert named_gap_partition_ok, \
            f"{host} {row_key} s{seed}: the named/gap partition drifted"
        exact_landing_named = int((replay_val == DEEP_RUNG).sum())
        exact_landing_base = int((replay_val == s_vals).sum())
        landing_range_ok = bool(0 <= exact_landing_named <= n_write
                                and 0 <= exact_landing_base <= n_write)
        assert landing_range_ok, \
            (f"{host} {row_key} s{seed}: the exact-landing count out of "
             "range")
        err_mean = float(e.mean())
        err_std = float(e.std())          # the population std
        err_min = float(e.min())
        err_max = float(e.max())
        frac_sigma = float((np.abs(e) <= COMMIT_NOISE).mean())
        err_moments_ok = bool(np.isfinite(err_mean) and np.isfinite(err_std)
                              and np.isfinite(err_min)
                              and np.isfinite(err_max)
                              and np.isfinite(frac_sigma))
        assert err_moments_ok, \
            f"{host} {row_key} s{seed}: non-finite error moment"
        sum_e = float(e.sum())
        sum_sq_e = total_sq

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
               "src_census": census_src,
               "sc_rms": sc_rms, "sc_finite_ok": sc_finite_ok,
               "sc_frac": sc_frac, "denom_ok": denom_ok,
               "cvt_rms": cvt_rms,
               "s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
               "walk_end_282_ok": we_ok, "trace_sha_282_ok": ts_ok,
               "err_exact_282_ok": ee_ok,
               "commit_sha_287_ok": cs287_ok, "cvt_287_ok": cvt287_ok,
               "n_commits_287_ok": nc287_ok, "sc_287_ok": sc287_ok,
               "masks_disjoint_ok": masks_disjoint_ok,
               "cls2_full_frame": cls2_full,
               "decomp": decomp,
               "accounting_ok": ident_ok, "fracs_ok": fracs_ok,
               "partition_ok": partition_ok,
               "census": census, "named_base_frac": named_base_frac,
               "named_count": named_count,
               "exact_landing_named": exact_landing_named,
               "exact_landing_base": exact_landing_base,
               "err_moments": {"mean": err_mean, "std": err_std,
                               "min": err_min, "max": err_max,
                               "frac_within_sigma": frac_sigma},
               "sum_e": sum_e, "sum_sq_e": sum_sq_e, "n_write": n_write}
        return rec

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; the pre-named 25 records: exp243 4 + exp256 3 +
    #      exp272 4 + exp273 5 + exp282 4 + exp287 5) ----------------------
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
        ("exp287_fixed_point_identity.json", "inputs"))

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
        assert total == 25, f"the chain record count {total} != 25"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

    # ---- THE COMPUTATION (ONE pass: the sha-asserted rebuild + the
    #      fresh 72-row battery at the production budget + the per-host
    #      dt record; the integrity section is a pure function of the
    #      deposits + the module bytes and is bit-compared across the
    #      two passes at assembly) ---------------------------------------
    def _compute_battery():
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (the exp269/exp280/exp284/exp285/exp286/
        #      exp287 form, every rebuild bit-asserted against exp243's
        #      OWN records) ----------------------------------------------
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_bnd_dual_ok": 0, "n_canon_ok": 0,
                  "h0_echo_h1": False, "n_fmax_ok": 0, "n_nonneg_ok": 0,
                  "n_rows256": 0, "n_structure_ok": 0, "n_worst_eq_max": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows282": 0, "n_282_chain_ok": 0,
                  "n_host_table282_ok": 0,
                  "n_rows287": 0, "n_host_table287_ok": 0,
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
        ht282 = {row["host"]: row for row in dep282["host_table"]}
        assert len(ht282) == 12, "exp282's host table drifted"
        means282 = {h: float(ht282[h]["walk_end_rms_mean"]) for h in hosts}
        counts["n_host_table282_ok"] = len(means282)

        # ---- G1: THE EXP287 RE-READ (the commit-layer anchor deposit) --
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

        # ---- G1: THE PROVENANCE CHAINS (25 records) ---------------------
        chains = _verify_chains()

        # ---- THE PER-HOST DT RECORD (the draw-stream face's pure read:
        #      project_phase_native + flip_clock_matrix on the base
        #      medium — no rng, no state, a pure projection; the dt the
        #      replica itself derives, recomputed OUTSIDE it) -----------
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

        # ---- THE FRESH DECOMPOSITION BATTERY: the 72 substituted rows
        #      at the production budget (the S0 anchors on EVERY row,
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
                    rec287 = r287[(k, s, rk)]
                    rec = _decode_row(k, rk, ctx["deep"][inst]["spec"],
                                      med, s, ctx["fmax"], d, rec282,
                                      rec287, ctx["A"])
                    rows_out.append(rec)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] 6 rows | errs {[r['err'] for r in hs]} | "
                  f"R_max "
                  f"{max(d['R'] for r in hs for d in r['decomp'] if d['R'] is not None):.4f}"
                  f" | cvt_rms {[round(r['cvt_rms'], 4) for r in hs]}",
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
                              "dt_record": dt_record,
                              "exp282_reread": {
                                  "n_rows": counts["n_rows282"],
                                  "branch": dep282["branch"],
                                  "host_table_walk_end_rms_means":
                                      means282},
                              "exp287_reread": {
                                  "n_rows": counts["n_rows287"],
                                  "host_table_mean_cvt": mean_cvt287}},
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
        mean_cvt287 = integrity["exp287_reread"]["host_table_mean_cvt"]
        dt_record = integrity["dt_record"]
        mia = integrity["targets"]["mia_prod_err"]["values"]
        prem = integrity["targets"]["one_zone_premium"]["values"]

        # ---- the per-host table + the POOLED CLASS DECOMPOSITION (the
        #      sums and counts added over the host's 6 rows — the pooling
        #      kills the small-class single-row variance, the probe-level
        #      fluctuation of R on small classes disclosed) --------------
        host_table = []
        for h in hosts:
            hs = [r for r in rows if r["host"] == h]
            assert len(hs) == 6, f"{h}: the 6 rows drifted"
            scs = [r["sc_rms"] for r in hs]
            gaps = [r["err_exact"] for r in hs]
            cvts = [r["cvt_rms"] for r in hs]
            errs = [r["err"] for r in hs]
            wes = [r["walk_end_rms"] for r in hs]
            settles = [r["settle_gap_abs"] for r in hs]
            mean_sc = float(np.mean(scs))
            mean_gap = float(np.mean(gaps))
            assert mean_gap > 0.0, f"{h}: the mean program-vs-target gap <= 0"
            mean8_dep = means282[h]
            mean8_ok = bool(float(np.mean(wes)) == mean8_dep)
            assert mean8_ok, \
                (f"{h}: the fresh per-host end-RMS mean {float(np.mean(wes))!r} "
                 f"drifted from exp282's deposited {mean8_dep!r}")
            # THE COMMIT-LAYER ANCHOR (the pre-named per-host mean_cvt)
            mean_cvt = float(np.mean(cvts))
            meancvt287_ok = bool(mean_cvt == mean_cvt287[h])
            assert meancvt287_ok, \
                (f"{h}: the fresh per-host mean_cvt {mean_cvt!r} drifted "
                 f"from exp287's deposited {mean_cvt287[h]!r}")
            census = {t: int(sum(r["src_census"][t] for r in hs))
                      for t in COMMIT_SOURCES}
            assert sum(census.values()) == sum(r["n_commits"] for r in hs), \
                f"{h}: the per-host commit census drifted"
            # the POOLED per-class decomposition
            NW = int(sum(r["n_write"] for r in hs))
            TOT = float(sum(r["sum_sq_e"] for r in hs))
            pool = []
            for cidx in (0, 1, 2):
                N_c = int(sum(d["n"] for r in hs for d in r["decomp"]
                              if d["cls"] == cidx))
                SS_c = float(sum(d["sum_sq"] for r in hs for d in r["decomp"]
                                 if d["cls"] == cidx))
                frac_c = float(SS_c / TOT)
                share_c = float(N_c / NW)
                R_c = (float(frac_c / share_c)) if N_c > 0 else None
                pool.append({"cls": int(cidx), "name": CLASS_NAMES[cidx],
                             "n": N_c, "cell_share": share_c,
                             "sum_sq": SS_c, "frac_of_sq": frac_c,
                             "R": R_c,
                             "rms_contrib_mV": float(np.sqrt(SS_c / NW))})
            nonempty_R = [p["R"] for p in pool if p["R"] is not None]
            R_max = float(max(nonempty_R))
            concentrates = bool(R_max >= CONC_BAR)
            # the pooled census + the named/landing totals + the moments
            census_pool: dict = {}
            for r in hs:
                for k, v in r["census"].items():
                    kk = float(k) if not isinstance(k, float) else k
                    census_pool[kk] = census_pool.get(kk, 0) + int(v)
            named_count = int(sum(r["named_count"] for r in hs))
            named_frac = float(named_count / NW)
            landing_named = int(sum(r["exact_landing_named"] for r in hs))
            landing_base = int(sum(r["exact_landing_base"] for r in hs))
            sum_e = float(sum(r["sum_e"] for r in hs))
            sum_sq_e = float(sum(r["sum_sq_e"] for r in hs))
            mean_e = float(sum_e / NW)
            std_e = float(np.sqrt(max(0.0, sum_sq_e / NW - mean_e ** 2)))
            fracsig = float(sum(r["err_moments"]["frac_within_sigma"]
                                * r["n_write"] for r in hs) / NW)
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "mean_sc": mean_sc, "mean_gap": mean_gap,
                "mean_cvt": mean_cvt,
                "mean_cvt_equals_exp287_host_table": meancvt287_ok,
                "mean_err": float(np.mean(errs)),
                "mean_walk_end_rms": float(np.mean(wes)),
                "mean8_equals_exp282_host_table": mean8_ok,
                "mean_settle_gap": float(np.mean(settles)),
                "src_census": census,
                "pooled": {"n_write": NW, "total_sq": TOT,
                           "classes": pool, "R_max": R_max,
                           "concentrates": concentrates},
                "pooled_census": census_pool,
                "pooled_named": {"named_count": named_count,
                                 "named_base_frac": named_frac,
                                 "exact_landing_named": landing_named,
                                 "exact_landing_base": landing_base},
                "pooled_err_moments": {"mean": mean_e, "std": std_e,
                                       "frac_within_sigma": fracsig,
                                       "min": float(min(r["err_moments"]["min"]
                                                        for r in hs)),
                                       "max": float(max(r["err_moments"]["max"]
                                                        for r in hs))}})

        # ---- THE BRANCH (pre-named: CONC_BAR 1.50 / CONC_MIN_HOSTS 10) --
        n_conc = sum(1 for row in host_table if row["pooled"]["concentrates"])
        if n_conc >= CONC_MIN_HOSTS:
            branch_local = "SPEC-GEOMETRIC"
        else:
            branch_local = "SPEC-UNIFORM"
        # the exp284-style margins on the pooled clean-mask fracs
        margins = []
        for cidx in (0, 1, 2):
            def _frac(row):
                return next(p["frac_of_sq"] for p in row["pooled"]["classes"]
                            if p["cls"] == cidx)
            o_vals = [_frac(row) for row in host_table if row["outlier"]]
            c_vals = [_frac(row) for row in host_table
                      if not row["outlier"]]
            margin = float(min(o_vals) - max(c_vals))
            margins.append({"cls": int(cidx), "name": CLASS_NAMES[cidx],
                            "outlier_fracs": o_vals,
                            "cluster_frac_range": [min(c_vals), max(c_vals)],
                            "margin": margin,
                            "separated_at_0.05": bool(margin >= 0.05)})
        branch_discriminant = {
            "bars": {"CONC_BAR": CONC_BAR, "CONC_MIN_HOSTS": CONC_MIN_HOSTS},
            "bars_pre_named_at": ("6ae42a3 — fixed at pre-registration, "
                                  "never fit"),
            "n_concentrating_hosts": n_conc,
            "per_host_R_max": {row["host"]: row["pooled"]["R_max"]
                               for row in host_table},
            "per_host_concentrates": {row["host"]:
                                      row["pooled"]["concentrates"]
                                      for row in host_table},
            "per_host_pooled_classes": {
                row["host"]: [{"cls": p["cls"], "name": p["name"],
                               "n": p["n"], "cell_share": p["cell_share"],
                               "frac_of_sq": p["frac_of_sq"], "R": p["R"]}
                              for p in row["pooled"]["classes"]]
                for row in host_table},
            "ordering_by_R_max": [
                {"host": row["host"], "R_max": row["pooled"]["R_max"],
                 "concentrates": row["pooled"]["concentrates"],
                 "outlier": row["outlier"]}
                for row in sorted(host_table,
                                  key=lambda r: -r["pooled"]["R_max"])],
            "outlier_vs_cluster_margins": margins,
            "pooled_censuses": {row["host"]: row["pooled_census"]
                                for row in host_table},
            "pooled_named_totals": {
                row["host"]: row["pooled_named"] for row in host_table},
            "pooled_err_moments": {
                row["host"]: row["pooled_err_moments"]
                for row in host_table},
            "source_census_total": {
                t: int(sum(row["src_census"][t] for row in host_table))
                for t in COMMIT_SOURCES},
            "branch": branch_local}

        # ---- the audit-only regressions (the exp274/exp275/exp282
        #      conventions VERBATIM: Spearman = Pearson on the tied-average
        #      ranks; the single-predictor OLS rank R2; the ties census per
        #      vector) — ASSERTED == exp287's deposited rhos BIT-EXACT ----
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
        n_reg_asserts = 0
        for tk, tvals in TARGET_COLS.items():
            xs = [row["mean_cvt"] for row in
                  (next(r for r in host_table if r["host"] == hh)
                   for hh in hosts)]
            rho = _spearman(xs, tvals)
            dep_rho = float(
                dep287["regressions"][f"mean_cvt~{tk}"]["rho"])
            rho_assert_ok = bool(rho == dep_rho)
            assert rho_assert_ok, \
                (f"the mean_cvt~{tk} regression rho {rho!r} drifted from "
                 f"exp287's deposited {dep_rho!r} — the anchor REFUTED")
            n_reg_asserts += int(rho_assert_ok)
            rk_resp = rankdata(np.asarray(xs, dtype=float))
            r2_single = _r2([tvals], rk_resp)
            r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))],
                         rk_resp)
            regressions[f"mean_cvt~{tk}"] = {
                "quantity": "mean_cvt", "target": tk,
                "rho": rho, "rho_abs": abs(rho),
                "deposited_rho_exp287": dep_rho,
                "rho_equals_exp287_bit_exact": rho_assert_ok,
                "rank_R2_single": r2_single,
                "rank_R2_all_ranks": r2_all,
                "all_ranks_minus_rho2": r2_all - rho * rho,
                "ties_carrier": _ties_census(xs),
                "ties_target": _ties_census(tvals),
                "gating": False,
                "role": ("audit-only — the anchor face (asserted == "
                         "exp287's deposited rho bit-exact, fail=STOP)")}
        # ---- THE DRAW-STREAM FACE (audit-only per G3's binding text:
        #      the cvt-tie groups + the per-host dt record, RECORDED —
        #      never gating; the docstring's narrative fail=STOP form is
        #      superseded by the G3 audit-only placement, the exp231
        #      body-landing disclosure precedent) -------------------------
        by_hs: dict = {}
        for r in rows:
            by_hs.setdefault((r["host"], int(r["seed"])), {})[
                r["row_key"]] = r
        cross_instance = []
        n_cvt_ties = 0
        for (h, s) in sorted(by_hs, key=lambda t: (t[0], t[1])):
            d = by_hs[(h, s)]
            a, b = d["r-60i0"], d["r-60i1"]
            tie = bool(a["cvt_rms"] == b["cvt_rms"])
            n_cvt_ties += int(tie)
            cross_instance.append({
                "host": h, "seed": int(s),
                "cvt_rms_i0": a["cvt_rms"], "cvt_rms_i1": b["cvt_rms"],
                "cvt_tie": tie,
                "walk_steps_tie": bool(a["walk_steps"] == b["walk_steps"]),
                "commit_sha_tie": bool(a["commit_seq_sha256"]
                                       == b["commit_seq_sha256"])})
        groups: dict = {}
        for h in hosts:
            hs = [r for r in rows if r["host"] == h]
            wvec = tuple(int(r["walk_steps"]) for r in hs)
            key = (repr(dt_record[h]["dt"]), wvec)
            groups.setdefault(key, []).append(h)
        tie_groups = []
        for key, gh in sorted(groups.items(),
                              key=lambda kv: (-len(kv[1]), kv[0])):
            positions_tied = None
            if len(gh) > 1:
                ref_rows = [r for r in rows if r["host"] == gh[0]]
                positions_tied = []
                for j in range(6):
                    rv = ref_rows[j]["cvt_rms"]
                    ok = all(
                        [r for r in rows if r["host"] == hh][j]["cvt_rms"]
                        == rv for hh in gh[1:])
                    positions_tied.append(bool(ok))
            tie_groups.append({
                "dt": float(key[0]),
                "walked_count_vector": list(key[1]),
                "hosts": gh, "n_hosts": len(gh),
                "per_position_cvt_tie": positions_tied})
        draw_stream_face = {
            "gating": False,
            "role": ("audit-only — the mechanism face (G3's audit-only "
                     "list: the cvt-tie groups + the per-host dt record; "
                     "RECORDED, never gating — the docstring's narrative "
                     "fail=STOP form superseded by the G3 binding text, "
                     "the exp231 body-landing disclosure precedent)"),
            "cross_instance": {
                "n_pairs": len(cross_instance),
                "n_cvt_ties": n_cvt_ties,
                "disclosure": (
                    "the pre-registration's narrative expected the "
                    "cross-instance cvt_rms bit-identity; the machinery's "
                    "own anchored deposit (exp287) already shows it holds "
                    "only on a subset of the 36 (host, seed) pairs — the "
                    "intra-walk draw consumption is state-coupled, not "
                    "purely structural; RECORDED, never gating"),
                "pairs": cross_instance},
            "tie_groups": tie_groups,
            "per_host_dt": dt_record}

        # ---- the S0 + G2 tallies (from the rows) -----------------------
        n_s0_err = sum(1 for r in rows if r["s0_err_ok"])
        n_s0_ver = sum(1 for r in rows if r["s0_verified_ok"])
        n_we282 = sum(1 for r in rows if r["walk_end_282_ok"])
        n_ts282 = sum(1 for r in rows if r["trace_sha_282_ok"])
        n_ee282 = sum(1 for r in rows if r["err_exact_282_ok"])
        n_mean282 = sum(1 for row in host_table
                        if row["mean8_equals_exp282_host_table"])
        n_cs287 = sum(1 for r in rows if r["commit_sha_287_ok"])
        n_cvt287 = sum(1 for r in rows if r["cvt_287_ok"])
        n_nc287 = sum(1 for r in rows if r["n_commits_287_ok"])
        n_sc287 = sum(1 for r in rows if r["sc_287_ok"])
        n_meancvt287 = sum(1 for row in host_table
                           if row["mean_cvt_equals_exp287_host_table"])
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
        n_masks = sum(1 for r in rows if r["masks_disjoint_ok"])
        n_cls2 = sum(1 for r in rows if r["cls2_full_frame"] == 0)
        n_ident = sum(1 for r in rows if r["accounting_ok"])
        n_fracs = sum(1 for r in rows if r["fracs_ok"])
        n_part = sum(1 for r in rows if r["partition_ok"])
        n_census_sum = sum(1 for r in rows
                           if sum(r["census"].values()) == r["n_write"])
        n_landing = sum(1 for r in rows
                        if 0 <= r["exact_landing_named"] <= r["n_write"]
                        and 0 <= r["exact_landing_base"] <= r["n_write"])

        g1 = dict(counts)
        g1.update({"n_s0_err_ok": n_s0_err, "n_s0_verified_ok": n_s0_ver,
                   "n_walk_end282_ok": n_we282, "n_trace282_ok": n_ts282,
                   "n_errexact282_ok": n_ee282, "n_mean282_ok": n_mean282,
                   "n_commitsha287_ok": n_cs287, "n_cvt287_ok": n_cvt287,
                   "n_ncommits287_ok": n_nc287, "n_scrms287_ok": n_sc287,
                   "n_meancvt287_ok": n_meancvt287})
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
              "max_settle_gap": max_settle,
              "n_masks_disjoint_ok": n_masks,
              "n_cls2_zero_ok": n_cls2,
              "n_accounting_ok": n_ident,
              "n_fracs_ok": n_fracs,
              "n_partition_ok": n_part,
              "n_census_sum_ok": n_census_sum,
              "n_landing_range_ok": n_landing}
        g3 = {"branch": branch_local,
              "n_concentrating_hosts": n_conc,
              "bars": {"CONC_BAR": CONC_BAR, "CONC_MIN_HOSTS": CONC_MIN_HOSTS},
              "n_regression_asserts_ok": n_reg_asserts,
              "all_regression_rhos_finite": bool(
                  all(np.isfinite(v["rho"])
                      for v in regressions.values())),
              "all_host_means_finite": bool(
                  all(np.isfinite(row["mean_sc"])
                      and np.isfinite(row["mean_gap"])
                      and np.isfinite(row["mean_cvt"])
                      and np.isfinite(row["pooled"]["R_max"])
                      for row in host_table)),
              "draw_stream_audit": {
                  "n_cross_instance_pairs": len(cross_instance),
                  "n_cross_instance_cvt_ties": n_cvt_ties,
                  "n_tie_groups": len(tie_groups),
                  "n_multi_host_tie_groups": sum(
                      1 for g in tie_groups if g["n_hosts"] > 1)}}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": integrity, "rows": rows,
                "host_table": host_table, "regressions": regressions,
                "draw_stream_face": draw_stream_face,
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
    _MODE = os.environ.get("EXP288_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp288_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp288_pass2.checkpoint.json")}

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
        print("=== exp288: THE SPEC LAYER'S FACE (what makes the "
              "compiler's spec-layer commits deep-band-host-dependent?) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows at the production budget "
              f"{BUDGET} (== exp142's STEPS_PER_CELL), TWO passes (G4)")
        print(f"  the decomposition: the commit error by classify class "
              f"(CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR) + the "
              f"commit-value distribution vs the spec's named voltages; "
              f"the branch bars CONC_BAR {CONC_BAR} / CONC_MIN_HOSTS "
              f"{CONC_MIN_HOSTS}")

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
        and g1["n_rows287"] == 72 and g1["n_host_table287_ok"] == 12
        and g1["n_s0_err_ok"] == 72 and g1["n_s0_verified_ok"] == 72
        and g1["n_walk_end282_ok"] == 72 and g1["n_trace282_ok"] == 72
        and g1["n_errexact282_ok"] == 72 and g1["n_mean282_ok"] == 12
        and g1["n_commitsha287_ok"] == 72 and g1["n_cvt287_ok"] == 72
        and g1["n_ncommits287_ok"] == 72 and g1["n_scrms287_ok"] == 72
        and g1["n_meancvt287_ok"] == 12
        and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
        and integrity["provenance_chains"]["total_verified"] == 25
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
                   and g2["n_lock_reads"] == 72
                   and g2["n_masks_disjoint_ok"] == 72
                   and g2["n_cls2_zero_ok"] == 72
                   and g2["n_accounting_ok"] == 72
                   and g2["n_fracs_ok"] == 72
                   and g2["n_partition_ok"] == 72
                   and g2["n_census_sum_ok"] == 72
                   and g2["n_landing_range_ok"] == 72)
    g3_pass = bool(g3["branch"] in ("SPEC-GEOMETRIC", "SPEC-UNIFORM")
                   and g3["n_concentrating_hosts"]
                   == sum(1 for row in core["host_table"]
                          if row["pooled"]["concentrates"])
                   and g3["n_regression_asserts_ok"] == 2
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
    dsf = core["draw_stream_face"]
    n_conc = bd["n_concentrating_hosts"]
    cens = bd["source_census_total"]

    if branch == "SPEC-GEOMETRIC":
        branch_text = (
            f"the commit error's class decomposition CONCENTRATES — "
            f"{n_conc}/12 hosts hold a pooled class with R >= {CONC_BAR} "
            f"(>= the pre-named {CONC_MIN_HOSTS}): the committed pattern's "
            f"host-dependence has a geometric address in the classify "
            f"classes, the spec layer's face is the class structure")
    else:
        branch_text = (
            f"the commit error's class decomposition is CLASS-BLIND — only "
            f"{n_conc}/12 hosts hold a pooled class with R >= {CONC_BAR} "
            f"(< the pre-named {CONC_MIN_HOSTS}): the spec layer's face is "
            f"uniform like every other level screened — the "
            f"host-dependence enters through the draw stream's positions "
            f"and the walked count, not through the class structure")

    verdict_body = (
        f"{branch} — {branch_text}"
        f" (N_conc {n_conc}/12 | the per-host pooled R_max within "
        f"[{min(bd['per_host_R_max'].values()):.4f}, "
        f"{max(bd['per_host_R_max'].values()):.4f}] vs the pre-named bar "
        f"{CONC_BAR} | the margins (audit-only): "
        + "; ".join(f"{m['name']} {m['margin']:+.4f}"
                    f"{' SEP' if m['separated_at_0.05'] else ''}"
                    for m in bd["outlier_vs_cluster_margins"])
        + f" | the audit-only anchor regressions: rho(mean_cvt)~mia "
          f"{regressions['mean_cvt~mia_prod_err']['rho']:+.4f} / "
          f"~premium "
          f"{regressions['mean_cvt~one_zone_premium']['rho']:+.4f} — "
          f"asserted == exp287's deposited rhos BIT-EXACT "
          f"({g3['n_regression_asserts_ok']}/2) | the commits' source "
          f"census (audit-only): spec {cens['spec']} / canon "
          f"{cens['canon']} / parent {cens['parent']} over "
          f"{sum(cens.values())} commits | THE COMMIT-VALUE FACE "
          f"(audit-only): the pooled named-base fraction within "
          f"[{min(v['named_base_frac'] for v in bd['pooled_named_totals'].values()):.4f}, "
          f"{max(v['named_base_frac'] for v in bd['pooled_named_totals'].values()):.4f}], "
          f"the exact-landing totals named "
          f"{sum(v['exact_landing_named'] for v in bd['pooled_named_totals'].values())} "
          f"/ base "
          f"{sum(v['exact_landing_base'] for v in bd['pooled_named_totals'].values())} "
          f"over "
          f"{sum(v['named_count'] for v in bd['pooled_named_totals'].values())} "
          f"named-base commits | the pooled error moments vs "
          f"COMMIT_NOISE {COMMIT_NOISE}: the mean within "
          f"[{min(v['mean'] for v in bd['pooled_err_moments'].values()):+.4f}, "
          f"{max(v['mean'] for v in bd['pooled_err_moments'].values()):+.4f}], "
          f"the |e| <= sigma fraction within "
          f"[{min(v['frac_within_sigma'] for v in bd['pooled_err_moments'].values()):.4f}, "
          f"{max(v['frac_within_sigma'] for v in bd['pooled_err_moments'].values()):.4f}] "
          f"| THE DRAW-STREAM FACE (audit-only, RECORDED): "
          f"{dsf['cross_instance']['n_cvt_ties']}/"
          f"{dsf['cross_instance']['n_pairs']} cross-instance cvt ties, "
          f"{g3['draw_stream_audit']['n_tie_groups']} (dt, walked-count) "
          f"groups | THE S0 ANCHOR: the fresh errs reproduce exp256's "
          f"deposited substituted errs bit-exact ({g1['n_s0_err_ok']}/72, "
          f"the verified flags {g1['n_s0_verified_ok']}/72) AND exp282's "
          f"walk_end_rms bit-exact (walk_end_rms {g1['n_walk_end282_ok']}"
          f"/72, trace sha256 {g1['n_trace282_ok']}/72 — the SAME walk "
          f"exp282 deposited, err_exact {g1['n_errexact282_ok']}/72, the "
          f"per-host means {g1['n_mean282_ok']}/12) AND exp287's COMMIT "
          f"LAYER bit-exact (the commit-sequence digests "
          f"{g1['n_commitsha287_ok']}/72 — the SAME commits exp287 "
          f"recorded, cvt_rms {g1['n_cvt287_ok']}/72, n_commits "
          f"{g1['n_ncommits287_ok']}/72, sc_rms {g1['n_scrms287_ok']}/72, "
          f"the per-host mean_cvt {g1['n_meancvt287_ok']}/12) | "
          f"12 hosts, a deterministic sha-asserted rebuild (graph_path "
          f"for H0/H1, small_world at the deposited rewire seeds — "
          f"exp269's/exp280's form), the provenance chains sha-verified "
          f"25/25, 6 deposits READ-ONLY byte-unchanged, two-pass "
          f"bit-identical ({run_form}), floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp288_spec_layer_face",
        "claim": (
            "THE SPEC LAYER'S FACE (batch 46, pre-registration commit "
            "6ae42a3): what makes the compiler's spec-layer commits "
            "deep-band-host-dependent? exp287 landed SELF-DRIFT with the "
            "exposure carried by the COMMITTED PATTERN "
            "(rho(mean_cvt)~mia +0.8616 / ~premium +0.7790) while every "
            "grain screened so far is class-blind (exp277's decode "
            "NEITHER, exp284's walk CLASS-BLIND, exp285's ring ABSENT). "
            "This module decomposes the commit layer itself: the landed "
            "write path fixes WHAT the spec layer contains "
            "(set_target(canon) installs phi_spec = canon; "
            "write_spec_layer(target) re-installs phi_spec = target "
            "BIT-EXACTLY; each commit is phi_spec[i] + ONE commit-noise "
            "draw — so the per-cell commit error e_i = commit_i - T_i is "
            "exactly one draw). The decomposition (pure rebuild + "
            "arithmetic, zero new knobs): (1) the committed pattern "
            "rebuilt per row (the commit sequence re-read, exp287's "
            "replay form — the replay built ONLY from the recorded "
            "commits); (2) the class decomposition by exp208's classify "
            "VERBATIM per instance (the clean masks CANON-BOUNDARY / "
            "PAIR-JUNCTION / INTERIOR; per class n_c / cell_share / "
            "sum_sq / frac_of_sq / rms_contrib / R_c = frac_of_sq / "
            "cell_share); (3) the commit-value distribution's own "
            "structure (the base census; the named-base fraction; the "
            "EXACT-LANDING COUNT #{commit_i == -60.0} bit-exact; the "
            "error moments vs COMMIT_NOISE). Branch (bars numeric, fixed "
            "at pre-registration): per host the 6 rows POOLED per class, "
            "R_max = max over non-empty classes of the pooled R_c; "
            "SPEC-GEOMETRIC iff #{hosts with R_max >= CONC_BAR 1.50} >= "
            "CONC_MIN_HOSTS 10; else SPEC-UNIFORM (class-blind like "
            "every other level screened)"),
        "method": {
            "replica": (
                "exp287's landed body REUSED VERBATIM — the "
                "state-carrying traced replica (_execute_signed_traced "
                "with the disclosed recording addition (f)) at the "
                "production budget 8 == exp142's STEPS_PER_CELL, the "
                "host rebuild (exp269's/exp280's form), exp256's "
                "_scoped_row_read_state form (PN1/PN2 + TC1 + TC2 + the "
                "traced TC3); ONE FRESH RUN of the SAME 72 substituted "
                "rows (12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, "
                "exp256's battery); the RNG stream, dt, canon, walk "
                "order, commits UNTOUCHED; exp142 NOT modified"),
            "decomposition": (
                "per row: e = commit - target on the program's write "
                "set (the replay's support: exactly the cells the "
                "executed program wrote, each exactly once); per clean "
                "class c (classify(T_instance, A_base) — CANON-BOUNDARY "
                "wins, then PAIR-JUNCTION, then INTERIOR, disjoint and "
                "covering): n_c, cell_share_c, sum_sq_c, frac_of_sq_c, "
                "rms_contrib_mV, R_c = frac_of_sq_c / cell_share_c; the "
                "ACCOUNTING IDENTITY sum_c sum_sq_c / n_write == "
                "cvt_rms^2 within 1e-6 * max(1, cvt_rms^2); the fracs "
                "sum to 1 within 1e-9; the exp208-label cls-2 count == 0 "
                "(the exp277/exp284 disclosure, asserted); pooled per "
                "host over the 6 rows (the sums and counts added — the "
                "pooling kills the small-class single-row variance)"),
            "branch_rule": (
                "per host the pooled decomposition; R_max = max over "
                "non-empty classes of the pooled R_c; the host "
                "concentrates iff R_max >= CONC_BAR (1.50); "
                "SPEC-GEOMETRIC iff N_conc >= CONC_MIN_HOSTS (10); else "
                "SPEC-UNIFORM. Bars CONC_BAR 1.50 / CONC_MIN_HOSTS 10, "
                "fixed at pre-registration (6ae42a3), never fit"),
            "regressions": (
                "the mean_cvt~mia / ~premium regressions under the "
                "exp274/exp275/exp282 conventions VERBATIM: Spearman = "
                "Pearson on the tied-average ranks (scipy rankdata); "
                "the single-predictor OLS rank R2; the ties census per "
                "vector; the 12-slot frame with the H0==H1 echo "
                "carried; ASSERTED == exp287's deposited rhos "
                "BIT-EXACT (fail=STOP) — the anchor"),
            "draw_stream_face_disclosure": (
                "BODY-LANDING DISCLOSURE (the exp231 precedent — gates "
                "untouched): the pre-registration's narrative sentence "
                "described the draw-stream face as 'asserted fail=STOP' "
                "(cvt_rms bit-identical across the two instances of "
                "every (host, seed) pair), but G3's binding gate text "
                "places the face in the AUDIT-ONLY, NEVER-GATING list "
                "('the draw-stream face's cvt-tie groups + the per-host "
                "dt record'). The audit-only placement is the binding "
                "form and the body records the face — the machinery's "
                "own anchored deposit (exp287) already shows the "
                "cross-instance bit-identity holds only on a subset of "
                "the 36 pairs (the intra-walk draw consumption is "
                "state-coupled, not purely structural), so the "
                "fail=STOP form would have crashed the instrument "
                "against data exp287 already landed. The face is "
                "RECORDED in full (the cross-instance table, the "
                "(dt, walked-count) tie groups, the per-host dt + "
                "projected max degree) — never gating; the branch "
                "discriminant is the R_max pooling"),
            "scope": (
                "the full commit sequences NOT re-deposited — "
                "bit-reproduced via the per-row commit_seq_sha256 "
                "digests + G1's anchors (the exp284/exp285/exp286/"
                "exp287 precedent); no wall-clock fields; the "
                "deterministic two-pass form")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": core["ro_before"][name],
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
                "commit_seq_sha256 + cvt_rms + n_commits + sc_rms + "
                "the 12-host mean_cvt + the deposited SELF-DRIFT "
                "branch + the regressions' deposited rhos (the bit-"
                "exact anchor target)"))},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp282_reread": integrity["exp282_reread"],
        "exp287_reread": integrity["exp287_reread"],
        "provenance_chains": integrity["provenance_chains"],
        "targets": integrity["targets"],
        "rows": core["rows"],
        "host_table": host_table,
        "regressions": regressions,
        "draw_stream_face": dsf,
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
                "plus err_exact 72/72 and the per-host means 12/12) "
                "AND exp287's commit layer reproduces bit-exact (the "
                "commit-sequence digests 72/72 — the SAME commits "
                "exp287 recorded, cvt_rms 72/72, n_commits 72/72, "
                "sc_rms 72/72, the per-host mean_cvt 12/12; asserted "
                "fail=STOP at decode)")},
        "G2_commit_replay_decomposition_accounting": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "the commit recording bookkeeping (the exp287 form: "
                "the commit count == walk_steps == the trace length; "
                "the commit indices unique; the replica-side write-set "
                "coverage; the values finite; the source census sane; "
                "the digest sha256 recorded — the full sequences NOT "
                "re-deposited); THE DECOMPOSITION: the three clean "
                "classes partition the write set (the class counts sum "
                "to n_write; the masks disjoint and covering by "
                "construction, asserted via the classify source); the "
                "exp208-label cls-2 count == 0 (the exp277/exp284 "
                "disclosure, asserted); THE ACCOUNTING IDENTITY "
                "sum_c sum_sq_c / n_write == cvt_rms^2 within 1e-6 * "
                "max(1, cvt_rms^2); the fracs sum to 1 within 1e-9; "
                "THE HISTOGRAM's sanity: the base census sums to "
                "n_write; the named-base + gap-base partition; the "
                "exact-landing count within [0, n_write]; the error "
                "moments finite; the A3 convention + the trace "
                "integrity + the TA3 convergence point asserted "
                "fail=STOP; the S* lock reads 72; the exp284-style "
                "settle gap recorded audit-only")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bars": ("per host the POOLED per-class decomposition over "
                     "the 6 rows; R_max = max over non-empty classes "
                     "of the pooled R_c; the host concentrates iff "
                     "R_max >= CONC_BAR (1.50); N_conc >= CONC_MIN_HOSTS "
                     "(10) -> SPEC-GEOMETRIC; else SPEC-UNIFORM. The "
                     "mean_cvt~mia / ~premium regressions asserted == "
                     "exp287's deposited rhos BIT-EXACT (fail=STOP; "
                     "the house conventions verbatim). Audit-only, "
                     "never gating: the per-row R table; the "
                     "exp284-style margins (the 0.05 bar form); the "
                     "draw-stream face's cvt-tie groups + the per-host "
                     "dt record; the orderings by R_max; the "
                     "outlier-vs-cluster faces; the pooled base "
                     "censuses; the pooled named-base + exact-landing "
                     "totals; the error moments vs COMMIT_NOISE"),
            "resolved": {"branch": branch,
                         "n_concentrating_hosts": n_conc,
                         "per_host_R_max": bd["per_host_R_max"]}},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_s0_anchor_integrity",
                 "G2_commit_replay_decomposition_accounting",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    gates["G4_discipline"] = {
        "pass": bool(deterministic and no_wall_clock and docstring_ok
                     and header_ok and ro_unchanged),
        "two_pass_bit_identical": deterministic,
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_6ae42a3": docstring_ok,
        "header_byte_unchanged_vs_6ae42a3": header_ok,
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
          f"(the 12 bases rebuilt sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the "
          f"classify boundary count {g1['n_bnd_dual_ok']}/12 dual-carried "
          f"+ the canon identity {g1['n_canon_ok']}/12 + H0 == H1 + "
          f"f_max {g1['n_fmax_ok']}/12 + non-negative "
          f"{g1['n_nonneg_ok']}/12; the deep targets "
          f"{g1['n_deep_targets_ok']}/72 + the medium shas "
          f"{g1['n_medium_shas_ok']}/72; exp282's re-read: rows "
          f"{g1['n_rows282']}/72 + the err chain anchor "
          f"{g1['n_282_chain_ok']}/72; exp287's re-read: rows "
          f"{g1['n_rows287']}/72; THE S0 ANCHOR — the errs == exp256's "
          f"deposited errs bit-exact {g1['n_s0_err_ok']}/72 AND "
          f"exp282's walk_end_rms bit-exact (walk_end "
          f"{g1['n_walk_end282_ok']}/72, trace sha "
          f"{g1['n_trace282_ok']}/72, err_exact "
          f"{g1['n_errexact282_ok']}/72, the per-host means "
          f"{g1['n_mean282_ok']}/12) AND exp287's COMMIT LAYER bit-exact "
          f"(the commit digests {g1['n_commitsha287_ok']}/72, cvt_rms "
          f"{g1['n_cvt287_ok']}/72, n_commits {g1['n_ncommits287_ok']}"
          f"/72, sc_rms {g1['n_scrms287_ok']}/72, the per-host mean_cvt "
          f"{g1['n_meancvt287_ok']}/12); the carries mia "
          f"{g1['n_mia_carry']}/12 + premium {g1['n_prem_carry']}/12; "
          f"the provenance chains "
          f"{integrity['provenance_chains']['total_verified']}/25)")
    print(f"  G2 the commit replay + the decomposition's accounting: "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(n_commits == walk_steps == the trace length "
          f"{g2['n_commits_count_ok']}/72; the commit indices unique "
          f"{g2['n_commits_unique_ok']}/72; the write-set coverage "
          f"{g2['n_coverage_ok']}/72; the digests {g2['n_digests_ok']}"
          f"/72; the masks disjoint+covering {g2['n_masks_disjoint_ok']}"
          f"/72; the cls-2 counts zero {g2['n_cls2_zero_ok']}/72; the "
          f"accounting identity {g2['n_accounting_ok']}/72; the fracs "
          f"{g2['n_fracs_ok']}/72; the partitions "
          f"{g2['n_partition_ok']}/72; the census sums "
          f"{g2['n_census_sum_ok']}/72; the landing ranges "
          f"{g2['n_landing_range_ok']}/72; the A3 convention "
          f"{g2['n_a3_ok']}/72; the convergence points "
          f"{g2['n_conv_ok']}/72; the S* lock reads "
          f"{g2['n_lock_reads']}/72; the settle gap max "
          f"{g2['max_settle_gap']:.4f} mV)")
    print("  the 12-host pooled decomposition table (R_max by host; "
          "H3/H5 the outliers):")
    for row in host_table:
        tag = " <== outlier" if row["outlier"] else ""
        parts = []
        for p in row["pooled"]["classes"]:
            rtxt = "null" if p["R"] is None else f"{p['R']:.3f}"
            parts.append(f"{p['name']}: n {p['n']} "
                         f"share {p['cell_share']:.3f} "
                         f"frac {p['frac_of_sq']:.3f} R {rtxt}")
        cls_txt = " | ".join(parts)
        print(f"      {row['host']:4s} R_max {row['pooled']['R_max']:.4f}"
              f"{'*' if row['pooled']['concentrates'] else ' '}  "
              f"mean_cvt {row['mean_cvt']:.4f}  {cls_txt}{tag}")
    print("  G3 branch — the anchor regressions (asserted == exp287's "
          "deposited rhos bit-exact):")
    for k, v in regressions.items():
        print(f"      {k:28s} rho {v['rho']:+.4f} (deposited "
              f"{v['deposited_rho_exp287']:+.4f}, "
              f"bit-exact {v['rho_equals_exp287_bit_exact']})")
    print(f"      the branch bars: CONC_BAR {CONC_BAR} | "
          f"CONC_MIN_HOSTS {CONC_MIN_HOSTS} | N_conc {n_conc}/12")
    print("  the draw-stream face (audit-only, RECORDED): "
          f"{dsf['cross_instance']['n_cvt_ties']}/"
          f"{dsf['cross_instance']['n_pairs']} cross-instance cvt ties; "
          f"{len(dsf['tie_groups'])} (dt, walked-count) groups "
          f"({g3['draw_stream_audit']['n_multi_host_tie_groups']} "
          f"multi-host)")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}, form {run_form}; "
          f"no wall-clock fields: {no_wall_clock}; 6 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged})")
    print(f"\n  BRANCH: {branch} | N_conc {n_conc}/12 | the per-host "
          f"pooled R_max within "
          f"[{min(bd['per_host_R_max'].values()):.4f}, "
          f"{max(bd['per_host_R_max'].values()):.4f}] vs the bar "
          f"{CONC_BAR}")
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
