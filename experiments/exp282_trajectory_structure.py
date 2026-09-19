#!/usr/bin/env python3
"""exp282 — THE TRAJECTORY INSTRUMENT: THE DEEP-BAND READ'S OWN WALK
STRUCTURE (batch 40; the first genuinely NEW measurement since exp269).

THE OPEN ITEM: the deep-band line closed at mia (exp278's MIA-SCALED,
rho 0.7250) with the premium's origin formally OUTSIDE the deposited
host records (exp281's CHORD-ABSENT) — but every instrument so far read
the deep-band substitution's COST as a single terminal number. The
state-carrying scoped read (execute_signed with return_state=True,
exp243's A3 path via exp256's _scoped_row_read_state) returns the final
state only; the walk's per-step structure inside execute_signed's commit
loop has never been measured. The question this module asks: does the
deep-band read's own walk — the per-step convergence of the RMS-to-target
as the walk commits cell by cell — carry the per-host exposure that the
terminal err carries (mia-scaled, premium-linked), or is the trajectory
structure ABSENT (the terminal err alone is informative, named honestly)?

THE INSTRUMENT (pre-registered, zero-knob): the substituted rows of
exp256's battery — 12 hosts x 3 seeds (1, 2, 3) x the two deep-band
instances (r-60i0/r-60i1, exp214's deep construction at the -60.0 rung)
= 72 rows at n=400 — THE SAME BATTERY, ONE FRESH RUN. Each row runs the
state-carrying scoped read with the walk's per-step convergence trace
recorded, and computes per-row trajectory summaries:

  THE TRACE (pre-named, zero-knob): ONE walk step = ONE cell commit
  (exp142's commit loop `for i, src in order:` — the walk's per-cell
  step; the 8 integration sub-steps inside a commit are NOT separately
  traced — disclosed). After each commit the replica records
  rms_k = sqrt(mean((V_k - T)^2)) over the FULL n=400 cell frame
  (pattern_error's own convention, mV) — the trace is the S-vector
  [rms_0 .. rms_{S-1}], S = the walk's commit count. The settle run
  after the walk (execute_signed's trailing c.run(15.0)) is NOT part of
  the walk — the trace ends at the walk's last commit (disclosed).

  THE THREE PER-ROW SUMMARIES (zero-knob):
    TA1 walk_end_rms  — the per-step RMS-to-target curve's FINAL value
         (rms_{S-1}; the walk-end RMS, pre-settle — disclosed).
    TA2 last10_slope  — the least-squares slope of the curve over the
         LAST 10% OF STEPS: W = max(2, ceil(0.10 * S)) final entries,
         numpy.polyfit(step_index, rms, 1)[0]; mV per walk-step.
    TA3 conv_step     — the CONVERGENCE POINT: the smallest step index k
         (0-based over the walk's commit sequence) where the curve first
         falls below 2x its final value (strict rms_k < 2.0 * rms_{S-1});
         asserted to exist on every row (rms_{S-1} > 0.0 asserted; then
         k = S-1 qualifies at worst).

  THE MACHINERY, DISCLOSED (the pre-named form): the trace hooks the
  walk WITHOUT modifying exp142. exp142's execute_signed records
  NOTHING per-step (read, disclosed pre-body), so the PRE-NAMED
  FALLBACK IS THE FORM: the state-carrying replica pattern — exp142's
  walk copied byte-similar into _execute_signed_traced carrying EXACTLY
  the disclosed additions (the per-step RMS read after each commit — a
  pure numpy read of the live V vs the target; the trace + step-count
  fields attached to the returned dict; the final state always carried),
  the RNG stream / dt / canon / walk order / commits untouched, called
  through exp256's _scoped_row_read_state form (the projection chain
  PN1/PN2 + TC1 + TC2 + the TC3 state-carrying call VERBATIM). The
  replica's inertness is not assumed — it is the S0 anchor below.

  THE 12-HOST TABLE: per-host MEANS of each summary over the host's 6
  substituted rows (3 seeds x 2 instances). THE REGRESSIONS: each
  summary's per-host mean against TWO targets — T_mia = mia_prod_err
  (exp273's field-table field 'exp243.classes.multi_identity_audit.
  prod_err', asserted bit-exact vs exp243's own class records) and
  T_prem = exp272's per-host ONE-ZONE PREMIUM means (asserted bit-exact
  vs exp273's field-table carry 'exp272.per_host.one_zone_premium_mean')
  — Spearman under the exp274/exp275/exp280 conventions (Pearson on
  scipy's tied-average ranks; the 12-slot frame, the H0==H1 echo
  carried; the ties census recorded; the single-predictor rank R2
  audit-only).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY (sha-asserted, READ-ONLY): the 12 base
      adjacencies rebuilt per the exp269/exp280 precedent (graph_path
      at the chain class's n=400 call site for H0/H1 — H0 echoes H1
      bit-exactly, asserted; small_world(n, 0.10, deposited
      rewire_seed) for H2-H11), every rebuild bit-asserted against
      exp243's records: sha256(|A| as float64) == base_sha256 12/12;
      the upper-triangle edge count == edges_base 12/12; the exp208
      classify CANON-BOUNDARY count == n_boundary_cells_base 12/12,
      dual-carried vs exp272's per_host AND exp273's field table; the
      canon identity labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12.
      The two deep-row targets rebuilt per exp256's build_rows deep
      construction (exp214's deep form VERBATIM): row_target_sha256 ==
      exp256's deposited substituted instance records 72/72, and the
      base medium sha == exp243's base_sha256 == the deposited instance
      medium_sha256 72/72; f_max recomputed == f_max_base 12/12. The
      source deposits (exp243, exp256, exp272, exp273) READ-ONLY:
      sha-recorded BEFORE any read, byte-unchanged after the work.
  G2  THE TRACE'S INTEGRITY (completeness + THE S0 ANCHOR): one fresh
      run of the 72 substituted rows through the state-carrying traced
      replica; TRACE COMPLETENESS — every row's trace covers the walk's
      FULL step count (len(trace) == the replica's recorded walk commit
      count, 72/72) with every entry finite; the per-row A3
      state-convention assert (round(err_exact, 2) == round(err, 2),
      exp243's convention) 72/72; THE S0 ANCHOR — every row's final err
      reproduces exp256's DEPOSITED substituted instance err BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags carried 72/72) — the trace form is inert on the deposited
      machine, the recording provably perturbed nothing.
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      TRAJECTORY-CARRIED iff >= 1 of the SIX signed Spearman rhos
      (3 summaries TA1/TA2/TA3 x 2 targets T_mia/T_prem) reaches
      >= 0.5 (the SIGNED house bar — positive); else TRAJECTORY-ABSENT
      (the walk's trajectory structure carries nothing at the bar —
      named honestly). THE ABS VARIANT, pre-named: max |rho| over the
      same six recorded audit-only — a crossing at |rho| >= 0.5 with a
      NEGATIVE sign is the ANTI-ALIGNED face (the summary runs OPPOSITE
      the exposure); it is NAMED in the deposit and the verdict per
      summary x target, NEVER gating. The rank R2s and the outlier
      (H3/H5) vs cluster summary margins audit-only.
  G4  THE DISCIPLINE: deterministic — the fresh run executes TWICE, the
      two passes' row payloads (errs, traces, summaries, table,
      regressions) BIT-IDENTICAL; no wall-clock fields (recursive key
      scan + serialized-blob scan); the docstring + header pinned to
      this pre-registration commit, asserted at entry AND exit; the
      source deposits byte-unchanged; NEURAL_SPEC_MIN == -60.0 asserted
      at exit (the floor restored post-import — exp218's disclosed
      exp169-import discipline, the -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): TRAJECTORY-CARRIED / TRAJECTORY-ABSENT.

RUN: the deterministic sha-asserted rebuild (seconds) + the fresh
72-row traced battery run TWICE (G4's two-pass clause; 72 decodes per
pass), foreground ~3-5 min. If a pass cannot finish inside the 570 s
foreground cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE pass per
invocation (env EXP282_PASS=1|2 caches that pass's row payload) and the
PRE-NAMED MERGE (env EXP282_MERGE=1) compares the two cached payloads
BIT-EXACT and writes the deposit — the merge never recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp282_trajectory_structure.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit 3c354c2) ==========================
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
        COMMIT_NOISE, ERR_BAR, STAR_OP, STEPS_PER_CELL, WINDOW_H)
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
    #      is the 3c354c2 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "fb6fae3c91b30c124ff8e12b61bd3b50c8b52a41e171b347dec5cd7c1d527c76")
    EXPECTED_HEADER_SHA256 = (
        "3886a8bc3176cd4e3b35fcbeed21cb3c4cfe047d0f6d6661f7f7dc2ed3d8d55d")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 3c354c2"
    assert header_ok, "header drifted from 3c354c2"

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
    #      the replica's executor constants asserted = exp142's own) ------
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
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit"}
    ro_before = {name: _sha(p) for p, name in _dep_names.items()}

    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP272) as fh:
        dep272 = json.load(fh)
    with open(DEP273) as fh:
        dep273 = json.load(fh)

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
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
    ft273 = {rec["field"]: rec for rec in dep273["field_table"]}

    # exp208's classify CANON-BOUNDARY mask (the T-ring-backbone half),
    # copied byte-for-byte from exp243's/exp269's/exp280's classify
    def _classify_boundary(T):
        n = len(T)
        Td = np.asarray(T, dtype=float)
        bnd = np.zeros(n, dtype=bool)
        for i in range(n):
            if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                bnd[i] = True
        return bnd

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

    # ---- THE TRACED REPLICA (the pre-named fallback IS the form:
    #      exp142's execute_signed records nothing per-step — read and
    #      disclosed pre-body — so exp142's walk is copied byte-similar
    #      here with EXACTLY the pre-registered disclosed additions:
    #      (a) the per-step RMS read after each commit (a pure numpy
    #      read of the live V vs the target — draws NOTHING from the
    #      RNG stream); (b) the trace + the walk commit count attached
    #      to the returned dict; (c) the final state always carried
    #      (exp243's A3 return_state semantics built in); (d) a no-op
    #      `order = []` initialization so the step count is well-defined
    #      on the empty-region branch (never taken on these rows);
    #      (e) the floor constant read via the exp142 module attribute
    #      (the same object exp142's own global resolves to).
    #      The RNG stream, dt, canon, walk order, commits: UNTOUCHED.
    #      exp142 itself is NOT modified.) ---------------------------------
    def _execute_signed_traced(spec, adjacency, seed, op):
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
                    "walk_trace": [], "walk_steps": 0}
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
                for _ in range(STEPS_PER_CELL):
                    c.step(dt)
                canon_src = getattr(c, "phi_spec_canon", None)
                if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:       # (e)
                    theta_new = c.phi_spec[i] + c.rng.normal(0.0, COMMIT_NOISE)
                elif canon_src is not None:
                    theta_new = canon_src[i] + c.rng.normal(0.0, COMMIT_NOISE)
                else:
                    theta_new = c.theta[src] + c.rng.normal(0.0, COMMIT_NOISE)
                c.theta[i] = theta_new
                c.V[i] = theta_new
                # ---- (a) THE DISCLOSED ADDITION: the per-step RMS read
                #      (a pure read; the walk's full-frame convergence) ---
                trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
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
        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced executor call) -------------
    def _scoped_row_read_traced(spec, med, seed, fmax):
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
            out = _execute_signed_traced(spec, A_ext, seed, op=STAR_OP)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one traced row decode (exp256's _decode_row_state form with
    #      the A3 state-convention assert + the S0 anchor) ----------------
    def _decode_row_traced(host, row_key, spec, med, seed, fmax, dep_rec):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax)
        err = float(out["err_vs_target"])
        assert np.isfinite(err), f"{host} {row_key} s{seed}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, f"{host} {row_key} s{seed}: state err vs reported err drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        trace_len_ok = bool(len(trace) == steps and steps >= 1)
        assert trace_len_ok, \
            f"{host} {row_key} s{seed}: trace {len(trace)} != walk steps {steps}"
        all_finite = bool(all(np.isfinite(trace)))
        assert all_finite, f"{host} {row_key} s{seed}: non-finite trace entry"
        final = trace[-1]
        final_positive = bool(final > 0.0)
        assert final_positive, f"{host} {row_key} s{seed}: final RMS == 0"
        # TA2 — the last-10%-of-steps least-squares slope (zero-knob)
        w = max(2, int(np.ceil(0.10 * steps)))
        w = min(w, steps)
        idx = np.arange(steps - w, steps, dtype=float)
        slope = float(np.polyfit(idx, np.asarray(trace[-w:], dtype=float),
                                 1)[0])
        # TA3 — the convergence point: the first index below 2x final
        thresh = 2.0 * final
        conv = None
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            f"{host} {row_key} s{seed}: the convergence point does not exist"
        # THE S0 ANCHOR: the fresh run reproduces exp256's deposited
        # substituted err BIT-EXACT (the machinery's native 2-dp form)
        s0_err_ok = bool(err == dep_rec["err"])
        s0_ver_ok = bool(bool(out["program_verified"]) == dep_rec["verified"])
        assert s0_err_ok, \
            (f"{host} {row_key} s{seed}: the fresh err {err} drifted from "
             f"exp256's deposited {dep_rec['err']} — S0 REFUTED")
        assert s0_ver_ok, f"{host} {row_key} s{seed}: the verified flag drifted"
        return {
            "host": host, "seed": int(seed), "instance": int(row_key[-1]),
            "row_key": row_key, "pert": P3, "medium": "base",
            "err": err, "err_deposited": float(dep_rec["err"]),
            "err_exact": err_exact, "a3_ok": a3_ok,
            "verified": bool(out["program_verified"]),
            "branch": str(out["branch"]), "rho": float(out["rho"]),
            "walk_steps": steps, "trace_len": len(trace),
            "walk_end_rms": final, "last10_slope": slope,
            "conv_step": int(conv),
            "trace": trace,
            "trace_sha256": hashlib.sha256(
                json.dumps(trace, sort_keys=True).encode()).hexdigest()}

    # ---- THE COMPUTATION (one full pass: the sha-asserted rebuild +
    #      the fresh 72-row traced battery + the summaries + the table +
    #      the regressions; run twice — G4's two-pass clause) --------------
    def compute():
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (exp269's/exp280's form, every rebuild
        #      bit-asserted against exp243's OWN records) ------------------
        g1 = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0, "n_bnd_ok": 0,
              "n_bnd_dual_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
              "n_fmax_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
              "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
              "n_medium_shas_ok": 0}
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
            sha_ok = bool(_a_sha(A) == rec["base_sha256"])
            edges = int(np.count_nonzero(np.triu(A, 1)))
            edges_ok = bool(edges == int(rec["edges_base"]))
            canon = labeling_bfs_n(np.abs(A))
            canon_ok = bool(np.array_equal(labeling_bfs_n(A), canon))
            bnd = _classify_boundary(canon)
            nb = int(bnd.sum())
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
            g1["n_hosts"] += 1
            g1["n_sha_ok"] += int(sha_ok)
            g1["n_edges_ok"] += int(edges_ok)
            g1["n_bnd_ok"] += int(bnd_ok)
            g1["n_bnd_dual_ok"] += int(bnd_dual)
            g1["n_canon_ok"] += int(canon_ok)
            g1["n_fmax_ok"] += int(fmax_ok)
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
                "f_max_matches_exp243_record": fmax_ok})
        g1["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                               bases["H1"]["A"]))
        assert g1["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        # ---- G1: exp256's 72 rows — the substituted records the S0
        #      anchor reads, complete with the instance structure -------
        rows256 = dep256["rows"]
        g1["n_rows256"] = len(rows256)
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
            g1["n_structure_ok"] += int(struct_ok)
            g1["n_worst_eq_max"] += int(werr == wmax)
            assert struct_ok, \
                f"{r['host']} s{r['seed']}: the substituted structure drifted"
            for i in insts:
                dep_sub[(r["host"], int(r["seed"]), i["row_key"])] = {
                    "err": float(i["err"]), "verified": bool(i["verified"]),
                    "medium_sha256": i["medium_sha256"],
                    "row_target_sha256": i["row_target_sha256"]}
        assert len(dep_sub) == 72, \
            "the 72 substituted instance records drifted"
        assert g1["n_structure_ok"] == 36 and g1["n_worst_eq_max"] == 36, \
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
                    g1["n_deep_targets_ok"] += int(ok_t)
                    g1["n_medium_shas_ok"] += int(ok_m)
        assert g1["n_deep_targets_ok"] == 72 \
            and g1["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # ---- THE FRESH TRACED BATTERY (12 hosts x 3 seeds x 2 deep
        #      instances = 72 rows; every decode state-carrying + traced;
        #      G2's trace completeness + the S0 anchor counted per row) --
        g2 = {"n_rows": 0, "n_trace_len_ok": 0, "n_a3_ok": 0,
              "n_s0_err_ok": 0, "n_s0_verified_ok": 0, "n_conv_ok": 0,
              "all_finite": True, "final_positive": True}
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec = _decode_row_traced(
                        k, rk, ctx["deep"][inst]["spec"], med, s,
                        ctx["fmax"], d)
                    rows_out.append(rec)
                    g2["n_rows"] += 1
                    g2["n_trace_len_ok"] += int(
                        rec["walk_steps"] == rec["trace_len"]
                        and rec["walk_steps"] >= 1)
                    g2["n_a3_ok"] += int(rec["a3_ok"])
                    g2["n_s0_err_ok"] += int(rec["err"] == d["err"])
                    g2["n_s0_verified_ok"] += int(
                        rec["verified"] == d["verified"])
                    g2["n_conv_ok"] += int(
                        0 <= rec["conv_step"] < rec["walk_steps"])
                    g2["all_finite"] = bool(
                        g2["all_finite"]
                        and all(np.isfinite(rec["trace"])))
                    g2["final_positive"] = bool(
                        g2["final_positive"] and rec["walk_end_rms"] > 0.0)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] traced 6 rows | errs "
                  f"{[r['err'] for r in hs]} | walk_steps "
                  f"{hs[0]['walk_steps']} | conv "
                  f"{[r['conv_step'] for r in hs]}")
        assert len(rows_out) == 72, \
            f"the traced battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"

        # ---- THE 12-HOST TABLE (per-host means of the three summaries
        #      over the host's 6 substituted rows) --------------------------
        SUMMARY_KEYS = ("walk_end_rms", "last10_slope", "conv_step")
        host_table = []
        for h in hosts:
            hs = [r for r in rows_out if r["host"] == h]
            assert len(hs) == 6, f"{h}: the 6 substituted rows drifted"
            host_table.append({
                "host": h,
                "walk_end_rms_mean":
                    float(np.mean([r["walk_end_rms"] for r in hs])),
                "last10_slope_mean":
                    float(np.mean([r["last10_slope"] for r in hs])),
                "conv_step_mean":
                    float(np.mean([r["conv_step"] for r in hs])),
                "n_rows": 6, "outlier": bool(h in outliers)})

        # ---- THE TARGETS (the pre-named carries, asserted bit-exact) ---
        mia = dict(ft273["exp243.classes.multi_identity_audit.prod_err"]
                   ["values"])
        assert set(mia) == set(hosts), "the mia field table drifted"
        n_mia_carry = 0
        for h in hosts:
            ok = bool(mia[h] == float(
                dep243["classes"][h]["multi_identity_audit"]["prod_err"]))
            assert ok, f"{h}: the mia carry drifted from exp243's records"
            n_mia_carry += int(ok)
        prem = {h: float(rec272[h]["one_zone_premium_mean"])
                for h in hosts}
        prem_dep = dict(ft273["exp272.per_host.one_zone_premium_mean"]
                        ["values"])
        n_prem_carry = 0
        for h in hosts:
            ok = bool(prem[h] == float(prem_dep[h]))
            assert ok, f"{h}: the premium carry drifted from exp273's"
            n_prem_carry += int(ok)
        targets = {
            "mia_prod_err": {
                "source": ("exp273's field-table field "
                           "'exp243.classes.multi_identity_audit.prod_err'"),
                "values": mia, "carry_vs_exp243_bit_exact": n_mia_carry},
            "one_zone_premium": {
                "source": ("exp272's per-host one_zone_premium_mean "
                           "(the one-zone premium means)"),
                "values": prem,
                "carry_vs_exp273_field_table_bit_exact": n_prem_carry}}

        # ---- THE REGRESSIONS (the exp274/exp275/exp280 conventions
        #      VERBATIM: Spearman = Pearson on the tied-average ranks;
        #      the single-predictor OLS rank R2 audit-only; the ties
        #      census per vector) -----------------------------------------
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
        for tk, tvals in TARGET_COLS.items():
            for sk in SUMMARY_KEYS:
                x = [row[sk + "_mean"] for row in host_table]
                rho = _spearman(x, tvals)
                rk_resp = rankdata(np.asarray(x, dtype=float))
                r2_single = _r2([tvals], rk_resp)
                r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))],
                             rk_resp)
                regressions[f"{sk}~{tk}"] = {
                    "summary": sk, "target": tk, "rho": rho,
                    "rho_abs": abs(rho), "rank_R2_single": r2_single,
                    "rank_R2_all_ranks": r2_all,
                    "all_ranks_minus_rho2": r2_all - rho * rho,
                    "ties_summary": _ties_census(x),
                    "ties_target": _ties_census(tvals)}

        # ---- G3: THE BRANCH DISCRIMINANT (pre-named numeric bar) --------
        rhos = {k: v["rho"] for k, v in regressions.items()}
        max_signed = max(rhos.values())
        signed_leader = max(rhos, key=lambda k: rhos[k])
        carried = bool(max_signed >= 0.5)
        branch_local = ("TRAJECTORY-CARRIED" if carried
                        else "TRAJECTORY-ABSENT")
        abs_leader = max(regressions,
                         key=lambda k: regressions[k]["rho_abs"])
        anti_face = {k: {"rho": v["rho"], "rho_abs": v["rho_abs"]}
                     for k, v in regressions.items()
                     if v["rho_abs"] >= 0.5 and v["rho"] < 0}
        margins = {}
        for sk in SUMMARY_KEYS:
            ov = {row["host"]: row[sk + "_mean"] for row in host_table
                  if row["outlier"]}
            cv = [row[sk + "_mean"] for row in host_table
                  if not row["outlier"]]
            margins[sk] = {"outliers": ov, "cluster_min": min(cv),
                           "cluster_max": max(cv)}
        g3 = {"rhos": rhos, "max_signed_rho": max_signed,
              "signed_leader": signed_leader,
              "abs_leader": abs_leader,
              "max_abs_rho": regressions[abs_leader]["rho_abs"],
              "anti_aligned_face_audit_only": anti_face,
              "outlier_margins_audit_only": margins,
              "branch": branch_local}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "rebuild_report": rebuild_report, "g1": g1, "g2": g2,
                "g3": g3, "rows": rows_out, "host_table": host_table,
                "targets": targets, "regressions": regressions,
                "ro_before": ro_before, "lock_reads": len(_LOCK_LOG)}

    # ---- the mode dispatch (the pre-named RUN clause: the default
    #      two-pass in-process form; EXP282_PASS=pass1|pass2 checkpoints
    #      ONE pass; EXP282_MERGE=1 compares the two cached payloads
    #      bit-exact and writes the deposit — the merge never recomputes)
    _MODE = os.environ.get("EXP282_MODE", "")
    _CK1 = os.path.join(ROOT, "results",
                        ".exp282_pass1.checkpoint.json")
    _CK2 = os.path.join(ROOT, "results",
                        ".exp282_pass2.checkpoint.json")

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

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
        payload = compute()
        _ck = _CK1 if _MODE == "pass1" else _CK2
        with open(_ck, "w") as f:
            json.dump(payload, f, sort_keys=True)
        print(f"  checkpointed {_MODE} -> {_ck} "
              f"(payload sha {_payload_sha(payload)[:16]})")
        _exit_checks()
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
        assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
            "floor drift at exit"
        return payload

    if _MODE == "merge":
        with open(_CK1) as fh:
            pa = json.load(fh)
        with open(_CK2) as fh:
            pb = json.load(fh)
    else:
        print("=== exp282: THE TRAJECTORY INSTRUMENT (the deep-band "
              "read's own walk structure — the first genuinely new "
              "measurement since exp269) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 traced rows, ONE FRESH RUN, "
              f"two passes (G4)")
        pa = compute()
        pb = compute()

    ro_before = pa["ro_before"]
    sha_a, sha_b = _payload_sha(pa), _payload_sha(pb)
    deterministic = bool(sha_a == sha_b)
    if not deterministic:
        ra = {(r["host"], r["seed"], r["row_key"]): r for r in pa["rows"]}
        rb = {(r["host"], r["seed"], r["row_key"]): r for r in pb["rows"]}
        diffs = [str(kk) for kk in sorted(set(ra) & set(rb))
                 if ra[kk] != rb[kk]]
        raise AssertionError(f"the two passes diverged: {diffs[:8]}")

    # ---- the gate assembly (each evaluated exactly once, on pass a;
    #      exp280's form) ---------------------------------------------------
    g1, g2, g3 = pa["g1"], pa["g2"], pa["g3"]
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(ro_before.values()))
    g1_pass = bool(g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
                   and g1["n_bnd_ok"] == 12 and g1["n_bnd_dual_ok"] == 12
                   and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
                   and g1["n_fmax_ok"] == 12 and g1["n_rows256"] == 72
                   and g1["n_structure_ok"] == 36
                   and g1["n_worst_eq_max"] == 36
                   and g1["n_deep_targets_ok"] == 72
                   and g1["n_medium_shas_ok"] == 72)
    g2_pass = bool(g2["n_rows"] == 72 and g2["n_trace_len_ok"] == 72
                   and g2["n_a3_ok"] == 72 and g2["n_s0_err_ok"] == 72
                   and g2["n_s0_verified_ok"] == 72 and g2["n_conv_ok"] == 72
                   and g2["all_finite"] and g2["final_positive"])
    g3_pass = True   # the discriminant evaluated exactly as pre-named

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

    gates = {
        "G1_rebuild_integrity": {
            "pass": g1_pass,
            "counts": g1,
            "source_deposits_read_only_byte_unchanged": ro_unchanged},
        "G2_trace_integrity_s0_anchor": {
            "pass": g2_pass,
            "counts": g2,
            "s0_anchor": ("every row's final err reproduces exp256's "
                          "deposited substituted instance err bit-exact "
                          "(72/72, the machinery's native 2-dp convention) "
                          "— the trace form is inert on the deposited "
                          "machine")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bar": ("TRAJECTORY-CARRIED iff >= 1 of the six signed "
                    "Spearman rhos (3 summaries x 2 targets) reaches "
                    ">= 0.5 (the SIGNED house bar, positive); else "
                    "TRAJECTORY-ABSENT; the abs variant audit-only")},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_integrity", "G2_trace_integrity_s0_anchor",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    max_signed = g3["max_signed_rho"]
    signed_leader = g3["signed_leader"]
    branch = g3["branch"]
    abs_leader = g3["abs_leader"]
    max_abs = g3["max_abs_rho"]
    anti = g3["anti_aligned_face_audit_only"]

    def _g(x):
        return f"{x:+.4f}"

    verdict_body = (
        f"{branch} — "
        + ("a trajectory summary reaches the 0.5 SIGNED house bar"
           if branch == "TRAJECTORY-CARRIED" else
           "no trajectory summary of the deep-band walk reaches the 0.5 "
           "SIGNED house bar against mia or the premium")
        + f" (max signed rho {_g(max_signed)} on {signed_leader}; by "
        + "summary~target: "
        + ", ".join(f"{k} {_g(v)}" for k, v in g3["rhos"].items())
        + f") — the walk's per-step convergence structure "
        + ("IS" if branch == "TRAJECTORY-CARRIED" else "is NOT")
        + " a carrier of the deep-band exposure at the bar | THE ABS "
        f"VARIANT (audit-only): max |rho| {_g(max_abs)} on {abs_leader}"
        + (f"; the ANTI-ALIGNED face crossed on {sorted(anti)} "
           "(named, never gating)" if anti else " — not crossed")
        + f" | the trace: one walk step = one cell commit, the full-frame "
        f"RMS per commit, the settle excluded (the disclosed form — "
        f"exp142's executor records nothing per-step; the state-carrying "
        f"replica pattern) | THE S0 ANCHOR: the fresh run reproduced "
        f"exp256's deposited substituted errs bit-exact "
        f"({g2['n_s0_err_ok']}/72, the verified flags "
        f"{g2['n_s0_verified_ok']}/72) | 12 hosts, a deterministic "
        f"sha-asserted rebuild (graph_path for H0/H1, small_world at the "
        f"deposited rewire seeds — exp269's/exp280's form), READ-ONLY "
        f"byte-unchanged, two-pass bit-identical, floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp282_trajectory_structure",
        "claim": (
            "THE TRAJECTORY INSTRUMENT (batch 40, pre-registration commit "
            "3c354c2; the first genuinely new measurement since exp269): "
            "the deep-band read's OWN WALK STRUCTURE. The state-carrying "
            "scoped read (execute_signed with return_state=True) returns "
            "only the final state; this module records the walk's "
            "per-step convergence trace on the substituted rows (12 "
            "hosts x 3 seeds x the two deep instances at n=400 — "
            "exp256's battery, ONE FRESH RUN) and computes per-row "
            "trajectory summaries (TA1 the per-step RMS-to-target "
            "curve's final value, TA2 its last-10%-of-steps slope, TA3 "
            "the step index where the curve first falls below 2x its "
            "final value); the 12-host table of per-host means "
            "regressed against mia_prod_err (exp273's field table) and "
            "exp272's one-zone premium means; the branch "
            "TRAJECTORY-CARRIED (>= 1 of the six signed rhos >= 0.5 — "
            "the SIGNED house bar) / TRAJECTORY-ABSENT (named "
            "honestly); the abs variant audit-only"),
        "method": {
            "trace": ("ONE walk step = ONE cell commit (exp142's commit "
                      "loop `for i, src in order:`; the 8 integration "
                      "sub-steps inside a commit NOT separately traced "
                      "— disclosed); after each commit the replica "
                      "records rms_k = sqrt(mean((V_k - T)^2)) over the "
                      "FULL n=400 cell frame (pattern_error's own "
                      "convention, mV); the trace is the S-vector over "
                      "the walk's commit sequence; the post-walk settle "
                      "run (execute_signed's trailing 15.0 run) is NOT "
                      "part of the walk — the trace ends at the walk's "
                      "last commit (disclosed)"),
            "trace_form": {
                "executor_per_step_records": (
                    "NONE — exp142's execute_signed records nothing "
                    "per-step (read, disclosed pre-body)"),
                "form": ("the pre-named fallback IS the form: the "
                         "state-carrying replica pattern — exp142's "
                         "walk copied byte-similar into "
                         "_execute_signed_traced with exactly the "
                         "disclosed additions (the per-step RMS read "
                         "after each commit — a pure numpy read, the "
                         "RNG stream untouched; the trace + step-count "
                         "fields; the final state always carried; a "
                         "no-op order init; the floor constant read "
                         "via the exp142 module attribute), called "
                         "through exp256's _scoped_row_read_state "
                         "form; exp142 itself NOT modified"),
                "inertness": ("NOT assumed — the S0 anchor: the fresh "
                              "run's 72 final errs reproduce exp256's "
                              "deposited substituted errs bit-exact")},
            "summaries": {
                "TA1 walk_end_rms": ("the per-step RMS curve's final "
                                     "value (rms_{S-1}; the walk-end "
                                     "RMS, pre-settle — disclosed)"),
                "TA2 last10_slope": ("the least-squares slope over the "
                                     "last W = max(2, ceil(0.10*S)) "
                                     "entries (numpy.polyfit degree 1); "
                                     "mV per walk-step"),
                "TA3 conv_step": ("the smallest 0-based step index k "
                                  "with rms_k < 2.0 * rms_{S-1} "
                                  "(strict); asserted to exist per row "
                                  "(rms_{S-1} > 0.0 asserted)")},
            "table": ("per-host means of the three summaries over the "
                      "host's 6 substituted rows (3 seeds x 2 "
                      "instances)"),
            "targets": {
                "T_mia": ("exp273's field-table field "
                          "'exp243.classes.multi_identity_audit."
                          "prod_err', asserted bit-exact vs exp243's "
                          "own class records 12/12"),
                "T_prem": ("exp272's per-host one_zone_premium_mean, "
                           "asserted bit-exact vs exp273's field-table "
                           "carry 12/12")},
            "regressions": ("the exp274/exp275 conventions VERBATIM: "
                            "Spearman = Pearson on the tied-average "
                            "ranks (scipy rankdata); the "
                            "single-predictor OLS rank R2 (the response "
                            "as its tied-average ranks, the target as "
                            "the numeric design column) + the "
                            "all-ranks variant AUDIT-ONLY; the ties "
                            "census per vector; the 12-slot frame with "
                            "the H0==H1 echo carried"),
            "branch_rule": ("TRAJECTORY-CARRIED iff >= 1 of the six "
                            "signed rhos reaches >= 0.5 (the SIGNED "
                            "house bar, positive); else "
                            "TRAJECTORY-ABSENT; the abs variant audit-"
                            "only (a NEGATIVE |rho| >= 0.5 crossing = "
                            "the ANTI-ALIGNED face, named per "
                            "summary~target, never gating)")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n) + the mia audit errs (T_mia's direct "
                "carry)",
                "the 72 rows — the S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas",
                "the host frame + the per-host one-zone premium means "
                "(T_prem) + the boundary counts + the outlier "
                "pre-name source",
                "the outlier pre-name + the field-table carries (the "
                "mia field + the premium carry, bit-exact)"))},
        "hosts": pa["hosts"],
        "outliers": pa["outliers"],
        "cluster": pa["cluster"],
        "rebuild_report": pa["rebuild_report"],
        "trace_form": {
            "step_unit": "one cell commit (the walk's per-cell step)",
            "rms_convention": ("sqrt(mean((V - T)^2)) over the FULL n=400 "
                               "frame — pattern_error's own convention, "
                               "mV"),
            "settle_excluded": True,
            "executor_per_step_records":
                "none (the pre-named fallback form)",
            "form": ("the state-carrying replica pattern: "
                     "_execute_signed_traced (exp142's walk byte-similar "
                     "+ the disclosed recording additions) through "
                     "exp256's _scoped_row_read_state form; exp142 NOT "
                     "modified")},
        "rows": pa["rows"],
        "host_table": pa["host_table"],
        "targets": pa["targets"],
        "regressions": pa["regressions"],
        "gates": gates,
        "branch": branch,
        "branch_discriminant": {
            "rhos": g3["rhos"],
            "max_signed_rho": max_signed,
            "signed_leader": signed_leader,
            "bar": 0.5,
            "abs_variant_audit_only": {
                "max_abs_rho": max_abs,
                "abs_leader": abs_leader,
                "anti_aligned_face": anti},
            "outlier_margins_audit_only":
                g3["outlier_margins_audit_only"]},
        "verdict": None,   # assembled after the G4 resolution, below
        "determinism": {
            "computation_passes": 2,
            "rows_per_pass": 72,
            "decodes_per_pass": 72,
            "payload_sha256_pass_a": sha_a,
            "payload_sha256_pass_b": sha_b,
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
    gates["G4_discipline"] = {
        "pass": bool(deterministic and no_wall_clock and docstring_ok
                     and header_ok and ro_unchanged),
        "two_pass_bit_identical": deterministic,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_3c354c2": docstring_ok,
        "header_byte_unchanged_vs_3c354c2": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "floor_at_entry": float(CORE.NEURAL_SPEC_MIN),
        "floor_at_exit": PROD_FLOOR,
        "docstring_sha256": docstring_sha,
        "header_sha256": header_sha,
        "deposit_form": ("deterministic: no wall-clock fields — a re-run "
                         "of this module reproduces this file "
                         "byte-identically")}
    n_pass += int(gates["G4_discipline"]["pass"])
    n_refute += int(not gates["G4_discipline"]["pass"])
    verdict = (f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} "
               f"REFUTE) | " + verdict_body)
    deposit["verdict"] = verdict

    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=str).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  G1 rebuild integrity: "
          f"{'PASS' if gates['G1_rebuild_integrity']['pass'] else 'FAIL'} "
          f"(the 12 bases rebuilt — graph_path for H0/H1, small_world at "
          f"the deposited seeds — sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the "
          f"classify boundary count {g1['n_bnd_dual_ok']}/12 dual-carried "
          f"vs exp272+exp273 + the canon identity {g1['n_canon_ok']}/12 + "
          f"H0 == H1; the deep targets {g1['n_deep_targets_ok']}/72 + the "
          f"medium shas {g1['n_medium_shas_ok']}/72 + f_max "
          f"{g1['n_fmax_ok']}/12; exp256's 72 rows with the substituted "
          f"structure {g1['n_structure_ok']}/36 + worst == max "
          f"{g1['n_worst_eq_max']}/36)")
    print(f"  G2 trace integrity + S0: "
          f"{'PASS' if gates['G2_trace_integrity_s0_anchor']['pass'] else 'FAIL'} "
          f"(72/72 traces cover the walk's full step count; the A3 "
          f"convention 72/72; THE S0 ANCHOR — the fresh errs == exp256's "
          f"deposited substituted errs bit-exact {g2['n_s0_err_ok']}/72, "
          f"the verified flags {g2['n_s0_verified_ok']}/72)")
    print("  the 12-host trajectory table (per-host means; H3/H5 the "
          "outliers):")
    for row in pa["host_table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} end_rms "
              f"{row['walk_end_rms_mean']:.4f}  slope10 "
              f"{row['last10_slope_mean']:+.6f}  conv_step "
              f"{row['conv_step_mean']:.2f}{tag}")
    print("  G3 branch — the six signed Spearman rhos:")
    for k, v in pa["regressions"].items():
        print(f"      {k:34s} rho {v['rho']:+.4f}  (abs "
              f"{v['rho_abs']:.4f})")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock}; 4 deposits READ-ONLY byte-unchanged: "
          f"{ro_unchanged})")
    print(f"\n  BRANCH: {branch} | max signed rho {_g(max_signed)} "
          f"({signed_leader}) vs the 0.5 bar | the abs variant: "
          f"{abs_leader} at {_g(max_abs)} "
          f"({'the ANTI-ALIGNED face crossed — named, never gating'
              if anti else 'not crossed'})")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    # ---- the hard rules, re-asserted after the work ----------------------
    _exit_checks()
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
