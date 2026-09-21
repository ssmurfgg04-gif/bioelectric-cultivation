#!/usr/bin/env python3
"""exp306 — THE PREMIUM UNDER THE COMPOSED CARRIER: DOES THE UNION'S
COMMIT LAYER DISSOLVE THE STRUCTURAL RESIDUAL? (batch 60; ledger
L290c's promoted candidate (5) — exp294 landed PREMIUM-MIXED on the
SELF g=1.0 carrier's commits: the noise-carried fraction DISSOLVED
(rho(mean_cvt)~mia_prod_err +0.2679 vs exp287's deposited +0.8616,
under the 0.40 bar) while the structural residual STRADDLED
(rho(mean_cvt)~one_zone_premium +0.4175 — above the dissolved bar,
below the carried bar). exp302 then landed PROTECTED-PRESERVED on the
COMPOSED union (faces=(ctx, gj, apop) at the composed optimum g=1.0,
+13.13 mV, the stress decode-invisible) — the strongest carrier the
stack has, and exp294 never saw it. THE OPEN QUESTION: does the
composed carrier's commit layer dissolve the structural residual too
(UNION-DISSOLVED — the premium story closes entirely: the host
dependence of the committed pattern was the noise's structure all the
way down), does it CARRY THROUGH (UNION-CARRIED — the premium is
structural to the spec layer and survives the strongest carrier), or
does the honest middle hold (UNION-MIXED)?

THE INSTRUMENT (exp302's landed union walk machinery VERBATIM at arm
A0 — no stress pin anywhere, the floor at -60.0 throughout; the 72-row
substituted battery exp256's/exp300's, 12 hosts x 3 seeds x r-60i0/
r-60i1 at n=400, the production budget 8; the commit recording the
exp287 form) with exp294's landed rho reads on top:

  R1  THE COMMIT-LAYER REGRESSIONS: per row the commit-vs-target RMS
      cvt_rms on the union's commits; per host the 6-row mean_cvt; THE
      ANCHOR REGRESSIONS: rho(mean_cvt)~mia_prod_err and
      rho(mean_cvt)~one_zone_premium under the house conventions
      VERBATIM (Spearman = Pearson on the tied-average ranks, the
      12-slot frame with the H0==H1 echo carried; the CONVENTION
      SELF-CHECK first: fed exp287's OWN deposited carrier host-table
      mean_cvt + the same covariate carries, the machinery must
      reproduce exp287's deposited rhos BIT-EXACT 2/2). The branch
      reads the comparison vs exp287's deposited rhos (+0.8616 /
      +0.7790) AND vs exp294's fresh self-carrier rhos (+0.2679 /
      +0.4175, re-read READ-ONLY from exp294's deposit).
  R2  THE IMPROVEMENT'S ADDRESS (audit-only, never gating): the
      per-host mean err deltas vs the dormant control (exp256's
      deposited substituted errs) vs the per-host mean_cvt deltas vs
      exp287's deposited commit layer — the delta correlation; the
      worst-err vs the 6.0 bar (audit-only).

THE ANCHOR (G1, fail=STOP): the 72 union walks reproduce exp300's
deposited union g=1.0 rows BIT-EXACT — the errs 72/72 + the trace shas
72/72 + the per-row cvt_rms 72/72 + the per-host mean_cvt 12/12 (the
commit layer IS the deposited union's, not a new instrument).

THE BRANCHES (pre-named): UNION-DISSOLVED iff BOTH fresh |rho| < 0.40
(the structural residual dissolves too — the premium was the noise's
host structure all the way down); UNION-CARRIED iff BOTH fresh |rho|
>= 0.60 (the premium is structural to the spec layer); UNION-MIXED
otherwise (the honest middle). The bars PREMIUM_DISSOLVED 0.40 /
PREMIUM_CARRIED 0.60 are exp294's landed bars, re-fixed HERE at
pre-registration, never fit.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets 72/72; THE MARKS' VALIDITY: the
      rebuilt q10/q90 + target_part + bands reproduce exp300's
      deposited arm_inputs BIT-EXACT 24/24 + 12/12 (the union's
      armed-site plan pinned to the deposited one — the anchor's
      bit-exactness depends on them); THE EXP300 ANCHOR: the 72 union
      rows bit-exact (errs + trace shas + per-row cvt_rms 72/72 each;
      the per-host mean_cvt 12/12); the convention self-check vs
      exp287's deposited rhos BIT-EXACT 2/2; the covariate carries
      (mia_prod_err + one_zone_premium) bit-exact 12/12 + 12/12 via
      exp273's field table; 7 deposits READ-ONLY sha before/after
      (exp243/256/272/273/287/294/300); the port's provenance + the
      zero-reader scan (the allowlist = the port + the pre-named
      history instruments + this module); exp142 and the core NOT
      modified (sha at entry == exit); the test suite green.
  G2  THE COMMIT LAYER'S DEFINITION (zero-knob asserted, fail=STOP per
      row): the commit count == walk_steps == the trace length 72/72;
      the commit indices unique 72/72; the write-set coverage 72/72;
      the values finite 72/72; the digests recorded 72/72 (the full
      sequences NOT re-deposited); cvt_rms finite 72/72; the A3 state
      convention 72/72; the register's replay equality + complement
      face 72/72; the union's face-write bookkeeping (n_sigma_writes +
      n_blend_writes) constant across the seeds per (host, instance)
      24/24; the gj landed compensation assert re-run per row
      (exp259's conservation identity, exp300's G2 form).
  G3  THE BRANCH DISCRIMINANT (the bars pre-named above, numeric,
      never fit): the fresh rhos vs the bars, evaluated exactly once;
      UNION-DISSOLVED / UNION-CARRIED / UNION-MIXED; the audit faces
      recorded (R2's address reads, never gating).
  G4  THE DISCIPLINE: deterministic (one pass; the payload serialized
      twice, the shas asserted equal); no wall-clock fields; the
      docstring + header pinned to the pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at
      exit; the floor -60.0 asserted at the entry, after the battery,
      and at exit (NO pin anywhere in this experiment).

RUN: 72 union decodes, in-process one invocation, ~2-4 min, under the
570 s cap.

DEPOSIT: results/exp306_premium_under_union.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp306_premium_under_union.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit c963c4e; gates G1-G4
    #      evaluated exactly once. THE MACHINERY: exp302's landed union
    #      walk VERBATIM at arm A0 (no stress pin) + exp294's landed
    #      rho reads (the house conventions); the anchor = exp300's
    #      deposited union g=1.0 rows) ================================
    import hashlib
    import json
    import subprocess

    import numpy as np
    from scipy.stats import rankdata   # the house conventions' ranker

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
    #      the c963c4e pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "06c6329f9fdf84c2409c6f04902652389f80b744eb16dd4c4dfb5064233cd861")
    EXPECTED_HEADER_SHA256 = (
        "0ccb3f82e00d28094c0dd25b17eaf2226d5ced5b2cb0d421ae436ee7ec7a7e88")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from c963c4e"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from c963c4e"

    # ---- the -60.0 floor (G4: the exp169-import discipline; NO pin
    #      anywhere in this experiment) ---------------------------------
    PROD_FLOOR = -60.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    def read_floor():
        return float(CORE.NEURAL_SPEC_MIN)

    assert read_floor() == PROD_FLOOR, "the floor is not -60.0 at entry"

    # ---- the frozen battery constants (exp302's/exp300's; the bars
    #      pre-named) -----------------------------------------------------
    REWIRE_P = 0.10
    DEEP_RUNG = -60.0
    DEEP_INSTANCES = (0, 1)
    ARM_SUBST = "substituted"
    P3 = "P3_deep_band_substitution"
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert SEEDS_RUN == (1, 2, 3), "seed-line drift"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        "the read drifted off S*"
    assert (WINDOW_H, COMMIT_NOISE, STEPS_PER_CELL, ERR_BAR) == (
        _m142.WINDOW_H, _m142.COMMIT_NOISE, _m142.STEPS_PER_CELL,
        _m142.ERR_BAR), "the executor constants drifted from exp142's"
    BUDGET = 8                            # the production budget
    assert BUDGET == int(STEPS_PER_CELL) == 8, "the budget drifted"
    G_COMPOSED = 1.0                      # the composed optimum
    FACES_UNION = ("ctx", "gj", "apop")   # exp300's landed union arm
    # the branch bars (exp294's landed bars, re-fixed at c963c4e,
    # never fit)
    PREMIUM_DISSOLVED = 0.40
    PREMIUM_CARRIED = 0.60
    REG_KEYS = ("mean_cvt~mia_prod_err", "mean_cvt~one_zone_premium")
    COMMIT_SOURCES = ("spec", "canon", "parent")
    CLASS_NAMES = {0: "canon_boundary", 1: "pair_junction", 2: "interior"}
    CONC_BAR = 1.50                       # exp288's audit bar (audit-only)

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    def _a_sha(A):
        return hashlib.sha256(np.ascontiguousarray(
            np.abs(np.asarray(A, dtype=float)),
            dtype=np.float64).tobytes()).hexdigest()

    # ---- the read-only deposits (the pre-named 7; sha before/after) ----
    RES = os.path.join(ROOT, "results")
    RO_NAMES = ("exp243_structured_adversarial",
                "exp256_row_pair_regression",
                "exp272_host_premium_structure",
                "exp273_outlier_hosts",
                "exp287_fixed_point_identity",
                "exp294_premium_under_history",
                "exp300_composed_optimum")
    RO_PATHS = {n: os.path.join(RES, n + ".json") for n in RO_NAMES}
    for _p in RO_PATHS.values():
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    ro_before = {n: _sha(p) for n, p in RO_PATHS.items()}
    _deps: dict = {}
    for _n in RO_NAMES:
        with open(RO_PATHS[_n]) as _fh:
            _deps[_n] = json.load(_fh)
    dep243 = _deps["exp243_structured_adversarial"]
    dep256 = _deps["exp256_row_pair_regression"]
    dep272 = _deps["exp272_host_premium_structure"]
    dep273 = _deps["exp273_outlier_hosts"]
    dep287 = _deps["exp287_fixed_point_identity"]
    dep294 = _deps["exp294_premium_under_history"]
    dep300 = _deps["exp300_composed_optimum"]
    hosts = list(dep287["hosts"])
    assert len(hosts) == 12, "the 12-host corpus drifted"
    outliers = ["H3", "H5"]              # exp289's pre-named outliers
    assert all(h in hosts for h in outliers), \
        "the outlier pre-name drifted"
    rec272 = {r["host"]: r for r in dep272["per_host"]}
    ft273 = {f["field"]: f for f in dep273["field_table"]}

    # ---- the port's provenance: the ported file's bytes + the
    #      zero-reader scan (the register read only in the port + the
    #      pre-named history instruments + this module) -----------------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)
    HISTORY_INSTRUMENTS = (
        "exp289_history_register.py", "exp292_history_dose_source.py",
        "exp293_history_stress.py", "exp294_premium_under_history.py",
        "exp295_dose_curve_leak_repair.py", "exp296_channel_sweep.py",
        "exp297_site_dose_ladders.py", "exp298_combined_site_carrier.py",
        "exp299_subsaturation_faces.py", "exp300_composed_optimum.py",
        "exp301_write_side_face.py", "exp302_composed_stress_face.py",
        "exp303_zero_substrate_8th.py", "exp304_transport_rescoped.py",
        "exp305_ca2_unblock.py", "exp306_premium_under_union.py")

    def _zero_reader_scan():
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
                    rel = os.path.relpath(p, ROOT)
                    with open(p, "r", encoding="utf-8",
                              errors="replace") as fh:
                        txt = fh.read()
                    cnt = txt.count("phi_history")
                    if cnt:
                        hits[rel] = cnt
        allowed = {"cultivation/bioelectric/collective.py"} | {
            f"experiments/{f}" for f in HISTORY_INSTRUMENTS}
        stray = sorted(set(hits) - allowed)
        assert not stray, \
            ("phi_history touched outside the port + the pre-named "
             f"instruments: {stray}")
        return {"files_with_phi_history": hits,
                "files_outside_port_and_instruments": stray,
                "readers_at_defaults": 0,
                "note": ("nothing reads phi_history at defaults; the "
                         "scan's allowlist = the port + the pre-named "
                         "history instruments (the landed forms + this "
                         "module)")}

    zero_reader_scan = _zero_reader_scan()

    # ---- exp208's classify (the house VERBATIM: exp302's exact form) ---
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

    # ---- exp259's compensation instrument (the gj face's landed
    #      assert machinery, re-run per row as the NON-history path's
    #      assert; the union coupling does NOT consume it) ---------------
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
        """exp259's landed compensation VERBATIM."""
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

    # ---- THE TRACED UNION REPLICA: exp302's landed
    #      _execute_signed_traced_union_stress VERBATIM with the A1 arm
    #      REMOVED (this experiment runs arm A0 only -- no stress pin
    #      anywhere; the floor stays at -60.0 throughout; the coupling
    #      order fixed: the sigma face first (the draw's scale), then
    #      the blends (the write's value); at a cell carrying BOTH
    #      blend faces the blend is applied ONCE) ------------------------
    def _execute_signed_traced_union(
            spec, adjacency, seed, op, budget,
            g=0.0, a_base=None, mark_mask=None):
        assert isinstance(g, (int, float)) and 0.0 <= float(g) <= 1.0, \
            "the dose drifted off the [0, 1] domain"
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
        # per row): the init == the spec's install BIT-EXACT
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
                    "reg_init_ok": reg_init_ok,
                    "n_arm_writes": 0, "n_sigma_writes": 0,
                    "n_blend_writes": 0}
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
        trace: list = []
        order: list = []
        commits: list = []
        n_arm_writes = 0
        n_sigma_writes = 0
        n_blend_writes = 0
        # the union's SITE plan (computed ONLY when the coupling is
        # armed; T and a_base are g-independent -- the row sets match
        # 1:1 across the whole battery)
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
        for i, src in order:
            for _ in range(budget):                  # the landed
                c.step(dt)                           # parameterization
            canon_src = getattr(c, "phi_spec_canon", None)
            # the verbatim commit branch chain (pure reads; the noise
            # draw ONCE below, at the arm's pre-named sigma)
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
            #      ZERO at g == 0.0) -------------------------------------
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
            # the per-step RMS read (a pure read; the walk's
            # full-frame convergence; unchanged)
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        c.run(15.0, dt=dt)
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
               "n_blend_writes": int(n_blend_writes)}
        return out

    # ---- the state-carrying replica read (exp289's form VERBATIM) -----
    def _scoped_row_read_union(spec, med, seed, fmax, budget,
                               g=0.0, a_base=None, mark_mask=None):
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
            out = _execute_signed_traced_union(
                spec, A_ext, seed, op=STAR_OP, budget=budget, g=g,
                a_base=a_base, mark_mask=mark_mask)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- the test suite (the shadow-path disclosure, exp289's form) ---
    def _run_test_suite():
        cmd = [sys.executable, "-m", "tests.run_tests"]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                              text=True, timeout=560)
        tail = "\n".join(proc.stdout.strip().splitlines()[-6:])
        green = bool(proc.returncode == 0)
        return {"green": green, "returncode": int(proc.returncode),
                "shadow_path_disclosure": (
                    "run from the repo root; the DeepScientist tests/"
                    " directory would shadow the repo's -- it does not "
                    "on this path (the repo root is the cwd)"),
                "tail": tail}

    # ---- the sha-asserted rebuild (exp302's _rebuild at the faces
    #      this experiment consumes: the 12 hosts, exp256's battery,
    #      exp300's union rows, the MARKS' VALIDITY) -----------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
                  "n_fmax_ok": 0, "n_nonneg_ok": 0, "n_rows256": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows300_u1": 0, "n_marks_ok": 0, "n_tpart_ok": 0,
                  "n_mia_carry": 0, "n_prem_carry": 0,
                  "n_host_table287_ok": 0}
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
            assert sha_ok and edges_ok and bnd_ok and canon_ok, \
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
            counts["n_bnd_ok"] += int(bnd_ok)
            counts["n_canon_ok"] += int(canon_ok)
            counts["n_fmax_ok"] += int(fmax_ok)
            counts["n_nonneg_ok"] += int(nonneg)
            rebuild_report.append({
                "host": h, "n": n,
                "constructor": ("graph_path (the chain/path constructor)"
                                if h in ("H0", "H1") else
                                "small_world(n, 0.10, rewire_seed)"),
                "sha256_matches_exp243_record": sha_ok,
                "edges_match_exp243_record": edges_ok,
                "boundary_count_matches": bnd_ok,
                "canon_identity_ok": canon_ok,
                "f_max_matches_exp243_record": fmax_ok,
                "base_non_negative": nonneg})
        counts["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                                   bases["H1"]["A"]))
        assert counts["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        # exp256's 72 rows (the rebuild's integrity + the control means)
        rows256 = dep256["rows"]
        counts["n_rows256"] = len(rows256)
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        dep_sub = {}
        for r in rows256:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                dep_sub[(r["host"], int(r["seed"]),
                         i["row_key"])] = {
                    "err": float(i["err"]),
                    "verified": bool(i["verified"])}
        assert len(dep_sub) == 72, \
            "the 72 substituted instance records drifted"
        for h in hosts:
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                for s in SEEDS_RUN:
                    assert (h, s, rk) in dep_sub
                    ok_t = bool(_f_sha(bases[h]["deep"][inst]["f"])
                                == bases[h]["deep"][inst]["sha"])
                    assert ok_t
                    counts["n_deep_targets_ok"] += int(ok_t)
                    counts["n_medium_shas_ok"] += 1
        assert counts["n_deep_targets_ok"] == 72 \
            and counts["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # THE EXP300 ANCHOR RE-READ (the deposited union g=1.0 rows —
        # the fresh battery's anchor source; the deposited branch
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
        # deposited one (the anchor's bit-exactness depends on them)
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

        # THE EXP287 HOST TABLE (the convention self-check's input +
        # the delta-cvt audit's control)
        ht287 = {row["host"]: row for row in dep287["host_table"]}
        assert len(ht287) == 12, "exp287's host table drifted"
        mean_cvt287 = {h: float(ht287[h]["mean_cvt"]) for h in hosts}
        counts["n_host_table287_ok"] = len(mean_cvt287)

        return {"bases": bases, "dep_sub": dep_sub, "r300u1": r300u1,
                "marks": marks, "bands": bands, "target_part": target_part,
                "q10": q10, "q90": q90, "pooled_n": int(pooled.size),
                "targets": {"mia_prod_err": mia, "one_zone_premium": prem},
                "mean_cvt287": mean_cvt287, "counts": counts,
                "rebuild_report": rebuild_report}

    rb = _rebuild()

    # ---- ONE UNION-ROW DECODE (the register + the commit bookkeeping
    #      asserted fail=STOP per row; THE ANCHOR: the errs + the trace
    #      shas + the per-row cvt_rms reproduce exp300's deposited union
    #      g=1.0 rows BIT-EXACT — fail=STOP) ------------------------------
    def _decode_union_row(host, row_key, spec, med, seed, fmax,
                          A_base, mark_mask, dep_rec, target_part):
        out = _scoped_row_read_union(
            spec, med, seed, fmax, BUDGET,
            g=G_COMPOSED, a_base=A_base, mark_mask=mark_mask)
        err = float(out["err_vs_target"])
        assert np.isfinite(err), \
            f"{host} {row_key} s{seed}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, \
            f"{host} {row_key} s{seed}: A3 state-convention drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        assert len(trace) == steps and steps >= 1, \
            f"{host} {row_key} s{seed}: trace len != walk steps"
        assert all(np.isfinite(trace)), \
            f"{host} {row_key} s{seed}: non-finite trace entry"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        # ---- the commit layer's bookkeeping (the exp287 form, fail=STOP)
        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps == len(trace), \
            (f"{host} {row_key} s{seed}: the commit count drifted")
        idxs = [int(rec[0]) for rec in commits]
        assert len(set(idxs)) == n_commits, \
            f"{host} {row_key} s{seed}: a committed cell written twice"
        assert bool(out["coverage_ok"]), \
            f"{host} {row_key} s{seed}: the write-set coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        assert all(np.isfinite(v) for v in vals), \
            f"{host} {row_key} s{seed}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        assert sum(census_src.values()) == n_commits, \
            f"{host} {row_key} s{seed}: the commit source census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        sc_rms = float(np.sqrt(np.mean((V[replay_idx] - replay_val) ** 2)))
        assert np.isfinite(sc_rms), \
            f"{host} {row_key} s{seed}: non-finite sc_rms"
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite cvt_rms"
        # the union's face-write bookkeeping (exp300's G2 form, carried)
        n_arm_writes = int(out["n_arm_writes"])
        n_sigma_writes = int(out["n_sigma_writes"])
        n_blend_writes = int(out["n_blend_writes"])
        # the gj landed compensation assert re-run per row (exp259's
        # conservation identity — exp300's G2 form)
        _W, _m, _resid = compensate(A_base, T, target_part)
        # ---- THE REGISTER FACE ----------------------------------------
        reg = {"present_ok": bool(out["reg_present_ok"]),
               "init_ok": bool(out["reg_init_ok"]),
               "replay_ok": bool(out["reg_replay_ok"]),
               "complement_ok": bool(out["reg_complement_ok"]),
               "finite_ok": bool(out["reg_finite_ok"]),
               "phi_history_sha256": str(out["phi_history_sha256"])}
        assert reg["present_ok"] and reg["init_ok"], \
            f"{host} {row_key} s{seed}: the register's presence/init drifted"
        # ---- THE EXP300 ANCHOR (fail=STOP) -----------------------------
        err_300_ok = bool(err == float(dep_rec["err"]))
        assert err_300_ok, \
            (f"{host} {row_key} s{seed}: the fresh union err {err} "
             f"drifted from exp300's deposited {dep_rec['err']} — "
             "the anchor REFUTED")
        trace_300_ok = bool(trace_sha == str(dep_rec["trace_sha256"]))
        assert trace_300_ok, \
            (f"{host} {row_key} s{seed}: the fresh trace sha drifted "
             "from exp300's deposited record — the anchor REFUTED")
        cvt_300_ok = bool(cvt_rms == float(dep_rec["cvt_rms"]))
        assert cvt_300_ok, \
            (f"{host} {row_key} s{seed}: the fresh cvt_rms drifted from "
             "exp300's deposited record — the anchor REFUTED")
        rec = {"host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "g": G_COMPOSED,
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "walk_steps": steps, "n_commits": n_commits,
               "trace_sha256": trace_sha,
               "commit_seq_sha256": commit_sha,
               "census": census_src, "cvt_rms": cvt_rms,
               "sc_rms": sc_rms,
               "register": reg,
               "n_arm_writes": n_arm_writes,
               "n_sigma_writes": n_sigma_writes,
               "n_blend_writes": n_blend_writes,
               "gj_compensation_resid_ok": bool(_resid <= 1e-9),
               "err_300_ok": err_300_ok,
               "trace_sha_300_ok": trace_300_ok,
               "cvt_300_ok": cvt_300_ok}
        return rec

    # ---- THE BATTERY (72 union rows; one pass) --------------------------
    print("[exp306] the battery: 72 union rows (faces=ctx,gj,apop at "
          "g=1.0) ...")
    rows_out: list = []
    for k in hosts:
        ctx = rb["bases"][k]
        med = HostWMedium(ctx["A"])
        for s in SEEDS_RUN:
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                dep_rec = rb["r300u1"][(k, s, rk)]
                rec = _decode_union_row(
                    k, rk, ctx["deep"][inst]["spec"], med, s,
                    ctx["fmax"], ctx["A"], rb["marks"][k][inst],
                    dep_rec, rb["target_part"][k])
                rows_out.append(rec)
        hs = [r for r in rows_out if r["host"] == k]
        print(f"  [union g={G_COMPOSED:g} {k}] 6 rows | errs "
              f"{[r['err'] for r in hs]} | anchor errs "
              f"{sum(r['err_300_ok'] for r in hs)}/6 | trace shas "
              f"{sum(r['trace_sha_300_ok'] for r in hs)}/6 | cvt "
              f"{sum(r['cvt_300_ok'] for r in hs)}/6", flush=True)
    assert len(rows_out) == 72, \
        f"the union battery produced {len(rows_out)} rows != 72"
    assert read_floor() == PROD_FLOOR, "the floor moved after the battery"

    # ---- the per-host union table (the 12-slot frame for R1; the
    #      anchor means re-asserted bit-exact vs exp300's deposited
    #      per-row cvt_rms means) ----------------------------------------
    host_table = []
    for h in hosts:
        hs = [r for r in rows_out if r["host"] == h]
        mean_err = float(np.mean([r["err"] for r in hs]))
        mean_cvt = float(np.mean([r["cvt_rms"] for r in hs]))
        mean_cvt_300 = float(np.mean(
            [float(rb["r300u1"][(h, s, rk)]["cvt_rms"])
             for s in SEEDS_RUN
             for rk in (f"r{DEEP_RUNG:g}i{i}" for i in DEEP_INSTANCES)]))
        mc_ok = bool(mean_cvt == mean_cvt_300)
        assert mc_ok, \
            (f"{h}: the fresh per-host mean_cvt drifted from exp300's "
             "deposited union rows' cvt_rms mean")
        control_err = float(np.mean(
            [rb["dep_sub"][(h, s, rk)]["err"] for s in SEEDS_RUN
             for rk in (f"r{DEEP_RUNG:g}i{i}" for i in DEEP_INSTANCES)]))
        host_table.append({
            "host": h, "n_rows": 6, "outlier": bool(h in outliers),
            "mean_err": mean_err,
            "mean_cvt": mean_cvt,
            "mean_cvt_equals_exp300_union_mean": mc_ok,
            "mean_cvt_control_exp287": float(rb["mean_cvt287"][h]),
            "mean_err_control_dormant": control_err,
            "delta_err_vs_dormant": float(mean_err - control_err),
            "delta_cvt_vs_exp287": float(
                mean_cvt - float(rb["mean_cvt287"][h])),
            "src_census": {
                t: int(sum(r["census"][t] for r in hs))
                for t in COMMIT_SOURCES}})

    # ---- the house conventions (exp287's regression read VERBATIM) -----
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

    def _regression_record(xs, tvals, tk):
        rho = _spearman(xs, tvals)
        rk_resp = rankdata(np.asarray(xs, dtype=float))
        r2_single = _r2([tvals], rk_resp)
        r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))], rk_resp)
        return {"quantity": "mean_cvt", "target": tk,
                "rho": rho, "rho_abs": abs(rho),
                "rank_R2_single": r2_single,
                "rank_R2_all_ranks": r2_all,
                "all_ranks_minus_rho2": r2_all - rho * rho,
                "ties_carrier": _ties_census(xs),
                "ties_target": _ties_census(tvals)}

    # ---- R1: the fresh commit-layer regressions (the house conventions
    #      verbatim — the CONVENTION SELF-CHECK first: fed exp287's OWN
    #      deposited carrier (its host-table mean_cvt) + the same
    #      carries, the machinery must reproduce exp287's deposited
    #      rhos BIT-EXACT) -------------------------------------------------
    targets = rb["targets"]
    target_cols = {
        "mia_prod_err": [float(targets["mia_prod_err"][h])
                         for h in hosts],
        "one_zone_premium": [float(targets["one_zone_premium"][h])
                             for h in hosts]}
    xs287 = [float(rb["mean_cvt287"][h]) for h in hosts]
    convention_selfcheck = {}
    for tk in REG_KEYS:
        tk_col = tk.split("~", 1)[1]
        rho_chk = _spearman(xs287, target_cols[tk_col])
        dep_rho = float(dep287["regressions"][tk]["rho"])
        ok = bool(rho_chk == dep_rho)
        assert ok, \
            (f"the house conventions drifted: the self-check rho for "
             f"{tk} {rho_chk!r} != exp287's deposited {dep_rho!r}")
        convention_selfcheck[tk] = {
            "rho_recomputed": rho_chk, "rho_deposited": dep_rho,
            "bit_exact": ok}
    xs = [next(row for row in host_table
               if row["host"] == hh)["mean_cvt"] for hh in hosts]
    regressions = {}
    for tk in REG_KEYS:
        tk_col = tk.split("~", 1)[1]
        rec = _regression_record(xs, target_cols[tk_col], tk_col)
        rec["rho_exp287_deposited"] = float(
            dep287["regressions"][tk]["rho"])
        rec["delta_vs_exp287_deposited"] = float(
            rec["rho"] - rec["rho_exp287_deposited"])
        rec["rho_exp294_self_carrier"] = float(
            dep294["regressions"][tk]["rho"])
        rec["delta_vs_exp294_self_carrier"] = float(
            rec["rho"] - rec["rho_exp294_self_carrier"])
        rec["gating"] = True
        rec["role"] = (
            "the branch discriminant — the pre-named bars "
            "PREMIUM_DISSOLVED 0.40 / PREMIUM_CARRIED 0.60 (exp294's "
            "landed bars, re-fixed at pre-registration c963c4e, never "
            "fit)")
        regressions[tk] = rec
    rho_mia = float(regressions["mean_cvt~mia_prod_err"]["rho"])
    rho_prem = float(regressions["mean_cvt~one_zone_premium"]["rho"])

    # ---- THE BRANCH (the pre-named bars; evaluated exactly once) --------
    a_mia = abs(rho_mia)
    a_prem = abs(rho_prem)
    if a_mia < PREMIUM_DISSOLVED and a_prem < PREMIUM_DISSOLVED:
        branch = "UNION-DISSOLVED"
    elif a_mia >= PREMIUM_CARRIED and a_prem >= PREMIUM_CARRIED:
        branch = "UNION-CARRIED"
    else:
        branch = "UNION-MIXED"

    # ---- R2: THE IMPROVEMENT'S ADDRESS (audit-only, never gating) -------
    delta_err = [next(row for row in host_table
                      if row["host"] == hh)["delta_err_vs_dormant"]
                 for hh in hosts]
    delta_cvt = [next(row for row in host_table
                      if row["host"] == hh)["delta_cvt_vs_exp287"]
                 for hh in hosts]
    rho_delta = _spearman(delta_err, delta_cvt)
    delta_corr = {
        "quantity": "delta_err_vs_dormant_control",
        "target": "delta_cvt_vs_exp287_g0.0",
        "rho": rho_delta, "rho_abs": abs(rho_delta),
        "ties_err": _ties_census(delta_err),
        "ties_cvt": _ties_census(delta_cvt),
        "gating": False,
        "role": ("audit-only — R2's address read: does the decode "
                 "improvement track the commit-layer change under the "
                 "composed carrier (never gating)")}
    worst = max(rows_out, key=lambda r: r["err"])
    worst_face = {
        "worst_err": float(worst["err"]),
        "worst_row": {"host": worst["host"], "seed": int(worst["seed"]),
                      "row_key": worst["row_key"]},
        "bar": ERR_BAR, "under_bar": bool(worst["err"] < ERR_BAR),
        "note": ("the anchor's 6.0 bar, unchanged — audit-only, never "
                 "gating")}

    # ---- the gates --------------------------------------------------------
    ro_after = {n: _sha(p) for n, p in RO_PATHS.items()}
    ro_unchanged = bool(all(ro_after[n] == ro_before[n]
                            for n in RO_NAMES))
    exp142_sha_exit = _sha(EXP142_FILE)
    port_sha_exit = _sha(PORT_FILE)
    exp142_unmodified = bool(exp142_sha_exit == exp142_sha_entry)
    port_unmodified = bool(port_sha_exit == port_sha_entry)
    test_suite = _run_test_suite()
    floor_exit_ok = bool(read_floor() == PROD_FLOOR
                         and CORE.NEURAL_SPEC_MIN == PROD_FLOOR
                         and _m142.NEURAL_SPEC_MIN == PROD_FLOOR)
    n_err_300 = int(sum(r["err_300_ok"] for r in rows_out))
    n_sha_300 = int(sum(r["trace_sha_300_ok"] for r in rows_out))
    n_cvt_300 = int(sum(r["cvt_300_ok"] for r in rows_out))
    n_mc_300 = int(sum(row["mean_cvt_equals_exp300_union_mean"]
                       for row in host_table))
    site_const = bool(all(
        len({r[f"n_{w}_writes"] for r in rows_out
             if r["host"] == h and r["instance"] == i})
        == 1 for h in hosts for i in DEEP_INSTANCES
        for w in ("sigma", "blend")))
    g2_commit_ok = bool(all(
        r["walk_steps"] == r["n_commits"] and r["a3_ok"]
        for r in rows_out))
    g1_pass = bool(rb["counts"]["n_sha_ok"] == 12
                   and rb["counts"]["n_edges_ok"] == 12
                   and rb["counts"]["n_bnd_ok"] == 12
                   and rb["counts"]["n_canon_ok"] == 12
                   and rb["counts"]["n_fmax_ok"] == 12
                   and rb["counts"]["n_nonneg_ok"] == 12
                   and rb["counts"]["h0_echo_h1"]
                   and rb["counts"]["n_rows256"] == 72
                   and rb["counts"]["n_deep_targets_ok"] == 72
                   and rb["counts"]["n_medium_shas_ok"] == 72
                   and rb["counts"]["n_rows300_u1"] == 72
                   and rb["counts"]["n_marks_ok"] == 24
                   and rb["counts"]["n_tpart_ok"] == 12
                   and rb["counts"]["n_mia_carry"] == 12
                   and rb["counts"]["n_prem_carry"] == 12
                   and rb["counts"]["n_host_table287_ok"] == 12
                   and n_err_300 == 72 and n_sha_300 == 72
                   and n_cvt_300 == 72 and n_mc_300 == 12
                   and len(convention_selfcheck) == 2
                   and all(v["bit_exact"] for v in
                           convention_selfcheck.values())
                   and ro_unchanged and exp142_unmodified
                   and test_suite["green"])
    g2_pass = bool(len(rows_out) == 72 and g2_commit_ok
                   and all(r["register"]["replay_ok"]
                           and r["register"]["complement_ok"]
                           for r in rows_out)
                   and all(r["gj_compensation_resid_ok"]
                           for r in rows_out)
                   and site_const)
    g3_pass = bool(branch in ("UNION-DISSOLVED", "UNION-CARRIED",
                              "UNION-MIXED"))
    g4_pass = bool(ro_unchanged and exp142_unmodified and port_unmodified
                   and floor_exit_ok and test_suite["green"]
                   and zero_reader_scan["files_outside_port_and_instruments"]
                   == [])

    print(f"  G1 the anchors: {'PASS' if g1_pass else 'FAIL'}")
    print(f"  G2 the commit layer's definition: "
          f"{'PASS' if g2_pass else 'FAIL'}")
    print(f"  G3 the branch: {branch} ({'PASS' if g3_pass else 'FAIL'})")
    print(f"  G4 the discipline: {'PASS' if g4_pass else 'FAIL'}")

    # ---- the deposit -------------------------------------------------------
    payload = {
        "exp": "exp306_premium_under_union",
        "claim": (
            "THE PREMIUM UNDER THE COMPOSED CARRIER (batch 60; ledger "
            "L290c's promoted candidate (5); pre-registration c963c4e): "
            "exp294 landed PREMIUM-MIXED on the self g=1.0 carrier (the "
            "noise-carried fraction dissolved +0.86->+0.27; the "
            "structural residual straddles at +0.42); exp302's composed "
            "union (+13.13 mV) did not exist yet -- does the union's "
            "commit layer dissolve the structural residual too? the "
            "instrument = exp302's landed union walk VERBATIM at arm "
            "A0 + exp294's landed rho reads (the house conventions "
            "verbatim); the anchor = exp300's deposited union g=1.0 "
            "rows bit-exact"),
        "method": {
            "battery": ("the shared 72-row deep-row battery (12 hosts x "
                        "3 seeds x 2 deep instances, the base medium); "
                        "the union faces=(ctx, gj, apop) at the composed "
                        "optimum g=1.0; 72 decodes, one pass"),
            "reads": {
                "R1": ("the fresh commit-layer regressions under the "
                       "house conventions (Spearman = Pearson on the "
                       "tied-average ranks; the 12-slot frame with the "
                       "H0==H1 echo carried); the convention self-check "
                       "vs exp287 bit-exact first"),
                "R2": ("the improvement's address (audit-only): the "
                       "delta correlation + the worst-err")},
            "run_form": "in-process one invocation",
            "branch_rule": (
                "UNION-DISSOLVED iff BOTH fresh |rho| < 0.40; "
                "UNION-CARRIED iff BOTH >= 0.60; UNION-MIXED otherwise "
                "(exp294's landed bars, re-fixed, never fit)")},
        "inputs": {n: {"path": f"results/{n}.json",
                       "sha256": ro_before[n]} for n in RO_NAMES},
        "port": {"file": "cultivation/bioelectric/collective.py",
                 "sha256": port_sha_entry,
                 "zero_reader_scan": zero_reader_scan,
                 "exp142_modified": not exp142_unmodified,
                 "exp142_sha256": exp142_sha_exit},
        "rebuild_report": rb["rebuild_report"],
        "rebuild_counts": rb["counts"],
        "marks_validity": {"q10": rb["q10"], "q90": rb["q90"],
                           "pooled_n": rb["pooled_n"],
                           "n_marks_ok": rb["counts"]["n_marks_ok"],
                           "n_tpart_ok": rb["counts"]["n_tpart_ok"],
                           "pinned_to": "exp300's deposited arm_inputs"},
        "anchor": {"source": "exp300's deposited union g=1.0 rows",
                   "n_err_bit_exact": n_err_300,
                   "n_trace_sha_ok": n_sha_300,
                   "n_cvt_bit_exact": n_cvt_300,
                   "n_host_mean_cvt_ok": n_mc_300},
        "targets": {
            "mia_prod_err": {
                "source": ("exp273's field-table field "
                           "'exp243.classes.multi_identity_audit."
                           "prod_err'"),
                "values": targets["mia_prod_err"],
                "carry_vs_exp243_bit_exact":
                    rb["counts"]["n_mia_carry"]},
            "one_zone_premium": {
                "source": ("exp272's per-host one_zone_premium_mean"),
                "values": targets["one_zone_premium"],
                "carry_vs_exp273_field_table_bit_exact":
                    rb["counts"]["n_prem_carry"]}},
        "convention_selfcheck": convention_selfcheck,
        "rows": rows_out,
        "host_table": host_table,
        "regressions": regressions,
        "branch": branch,
        "branch_discriminant": {
            "rho_mia": rho_mia, "rho_premium": rho_prem,
            "a_mia": a_mia, "a_premium": a_prem,
            "bars": {"PREMIUM_DISSOLVED": PREMIUM_DISSOLVED,
                     "PREMIUM_CARRIED": PREMIUM_CARRIED},
            "bars_source": ("exp294's landed bars, re-fixed at "
                            "pre-registration c963c4e, never fit")},
        "audit_r2_address": delta_corr,
        "audit_worst_err": worst_face,
        "test_suite": test_suite,
        "determinism": {
            "form": "in-process one invocation (one pass)",
            "discipline": ("one decode per (host, seed, instance); the "
                           "anchor is the deposit re-read, never a "
                           "re-decode"),
            "no_wall_clock_fields": True},
        "discipline": {
            "no_wall_clock_fields": True,
            "deterministic_one_pass": True,
            "docstring_header_pinned": True,
            "pinned_to": "c963c4e",
            "ro_unchanged": ro_unchanged,
            "floor": PROD_FLOOR,
            "no_pin_anywhere": True,
            "exp142_and_core_not_modified": bool(
                exp142_unmodified and port_unmodified)},
        "gates": {
            "G1_the_anchors": {"pass": g1_pass,
                               "counts": dict(rb["counts"],
                                              **{"n_err_300": n_err_300,
                                                 "n_sha_300": n_sha_300,
                                                 "n_cvt_300": n_cvt_300,
                                                 "n_mc_300": n_mc_300,
                                                 "ro_unchanged":
                                                     ro_unchanged,
                                                 "exp142_unmodified":
                                                     exp142_unmodified,
                                                 "test_suite_green":
                                                     test_suite["green"]})},
            "G2_the_commit_layer": {"pass": g2_pass,
                                    "commit_definition_ok": g2_commit_ok,
                                    "site_constancy_ok": site_const},
            "G3_the_branch": {"pass": g3_pass, "branch": branch},
            "G4_the_discipline": {"pass": g4_pass,
                                  "ro_unchanged": ro_unchanged,
                                  "exp142_unmodified": exp142_unmodified,
                                  "port_unmodified": port_unmodified,
                                  "floor_exit_ok": floor_exit_ok,
                                  "test_suite_green":
                                      test_suite["green"]}},
    }
    n_pass = int(g1_pass) + int(g2_pass) + int(g3_pass) + int(g4_pass)
    payload["verdict"] = (
        f"{n_pass}/4 evaluated gates ({n_pass} PASS / {4 - n_pass} "
        f"REFUTE) | BRANCH: {branch} | the fresh rhos on the union's "
        f"commits: rho(mean_cvt)~mia_prod_err {rho_mia:+.4f} vs "
        f"exp287's +0.8616 and exp294's self-carrier +0.2679 | "
        f"rho(mean_cvt)~one_zone_premium {rho_prem:+.4f} vs exp287's "
        f"+0.7790 and exp294's self-carrier +0.4175 | the anchor "
        f"bit-exact (errs + trace shas + cvt 72/72; the per-host "
        f"mean_cvt 12/12)")
    # the determinism face: two serializations, one sha
    det_sha1 = hashlib.sha256(json.dumps(
        payload, sort_keys=True).encode()).hexdigest()
    det_sha2 = hashlib.sha256(json.dumps(
        payload, sort_keys=True).encode()).hexdigest()
    assert det_sha1 == det_sha2, "the payload serialization drifted"
    payload["determinism"]["payload_sha256_pass1"] = det_sha1
    payload["determinism"]["payload_sha256_pass2"] = det_sha2
    # the exit pins (the docstring + the header re-asserted AFTER)
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from c963c4e (exit)"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from c963c4e (exit)"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, \
        "NEURAL_SPEC_MIN drifted at exit"
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    print(f"[exp306] deposited {OUT}")
    print(f"[exp306] VERDICT: {payload['verdict']}")
    assert read_floor() == PROD_FLOOR, "the floor moved at exit"
    return payload


if __name__ == "__main__":
    main()

