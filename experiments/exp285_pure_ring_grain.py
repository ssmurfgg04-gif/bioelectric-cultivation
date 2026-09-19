#!/usr/bin/env python3
"""exp285 — THE PURE RING GRAIN: THE END-RMS CARRIER'S MASS IN THE RING
AROUND THE CLASSIFY BOUNDARY SET (batch 43; exp284's audit-only sub-bar
live lead — on the boundary's own share the outliers H3/H5 hold the two
highest values (0.1501/0.1601 vs the ten-host cluster's [0.0489,
0.1094], margin +0.0406) but the pre-named 0.05 bar was not crossed and
exp284's branch stayed WALK-CLASS-BLIND; this module widens the grain
by one hop: the ring of cells IMMEDIATELY AROUND the classify boundary
set).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED — the walk's end RMS
(TA1 walk_end_rms) is the strongest carrier yet named (signed Spearman
+0.8826 against mia_prod_err, +0.8807 against exp272's one-zone premium
means; the 0.5 SIGNED house bar). exp284 decomposed the carrier's
endpoint by cell class at the walk level and found it CLASS-BLIND on
the exp208-label reading (the margins NEGATIVE), while its audit-only
PURE-MASK SPLIT showed the boundary ring's OWN share carrying a clean
but sub-bar ordering — the one live lead. exp285 asks the grain
question that lead points at: does the end-RMS mass in the RING AROUND
the classify boundary set — the immediate non-boundary neighbors —
carry the exposure at the 0.5 signed bar?

THE RING (the zero-knob definition, fixed HERE at pre-registration):
per row, exp208's classify VERBATIM on the row target + medium
(classify(T_instance, A_host)) yields the boundary set B; the
RING = {j not in B : exists i in B with A[i,j] > 0} — the immediate
non-boundary neighbors of the classify boundary set on the medium's
pair support. The rebuilt bases are non-negative (asserted per host in
the rebuild), so the read A[i,j] > 0 IS the |A| > 0 support convention
exp208's classify itself uses. No thresholds, no weights, no degree
bars, no distance bands — zero knobs.

THE INSTRUMENT (pre-registered, zero new simulation beyond the one
battery): exp284's landed body REUSED VERBATIM — the traced replica
(_execute_signed_traced, landed at 8ca252e, reused verbatim since
f3ca053: exp142's walk byte-similar + exactly the disclosed recording
additions; the RNG stream / dt / canon / walk order / commits
untouched; exp142 NOT modified), the host rebuild (exp269's/exp280's
form), exp256's _scoped_row_read_state form (the projection chain
PN1/PN2 + TC1 + TC2 + the traced TC3), and the end-state decomposition
(exp208's classify + decompose conventions VERBATIM) — ONE FRESH RUN
of the SAME 72 substituted rows (12 hosts x 3 seeds (1,2,3) x the two
deep instances r-60i0/r-60i1 at n=400 — exp256's battery). THE ONLY
ADDITION: the ring mask + the per-row THREE-WAY end-RMS split boundary
/ RING / rest (exp208's decompose conventions VERBATIM on the
mean-squared scale: sum_sq / frac_of_sq / rms_contrib_mV; the identity
asserted fail=STOP). The per-cell end errors from the state-carrying
read's final_state (e_i = V_i - T_i over the n=400 frame); the
END-RMS = err_exact (the A3-checked state convention; the PRE-settle
trace[-1] carrier vs the POST-settle end state disclosed pre-body in
exp284 — carried; the settle gap recorded audit-only).

THE PER-HOST TABLE: per-host means over the host's 6 rows (3 seeds x 2
instances) of the ring share (frac_ring), the boundary's own share
(frac_boundary — exp284's pure boundary-ring share), the rest share
(frac_rest), the mean ring count, the mean boundary count, the
err_exact and walk_end_rms_carried means, the settle-gap mean.

THE REGRESSIONS: the per-host ring-share means against mia_prod_err
(exp273's field table, asserted == exp243's own class records) and
exp272's one-zone premium means (asserted == exp273's field-table
carry), Spearman under the exp274/exp275/exp282 conventions VERBATIM
(Pearson on the tied-average ranks, the 12-slot frame with the H0==H1
echo carried, the ties census per vector, the single-predictor rank
R2). Audit-only, never gating: the boundary-share and rest-share
regressions; the full 12-host ordering by the ring share; exp284's
audit-only face recomputed beside (the fresh per-host boundary shares
asserted == exp284's deposited pure_boundary_ring_share means
BIT-EXACT 12/12, and the outliers-vs-cluster pure-share margin
recomputed from the fresh means == the margin from exp284's deposited
means bit-exact).

THE BRANCH (pre-named, the bar numeric, fixed HERE at
pre-registration, never fit): RING-CARRIED iff the ring share's signed
Spearman reaches >= 0.5 — the SIGNED house bar, positive — against
>= 1 of the two targets; RING-ABSENT otherwise (named honestly). The
abs variant pre-named: a NEGATIVE rho <= -0.5 crossing = the
ANTI-ALIGNED face, named per target in the deposit + verdict, never
gating (exp280/exp281's precedent).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284 precedent (graph_path at the
      chain class's n=400 call site for H0/H1 — H0 echoes H1 bit-
      exactly, asserted; small_world(n, 0.10, deposited rewire_seed)
      for H2-H11), bit-asserted against exp243's records: sha256(|A| as
      float64) == base_sha256 12/12; the upper-triangle edge count ==
      edges_base 12/12; the classify boundary-ring count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity labeling_bfs_n(|A|)
      == labeling_bfs_n(A) 12/12; f_max recomputed == f_max_base 12/12;
      the bases NON-NEGATIVE asserted per host (the 0/1 support form —
      the ring's read A[i,j] > 0 is then literally the |A| > 0 pair
      support exp208's classify uses). The two deep-row targets rebuilt
      per exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited medium_sha256 72/72. exp256's 72 rows with the
      substituted structure 36/36 + worst == max 36/36. THE EXP284
      RE-READ: the 72 row records present with the per_class records +
      trace_sha256 + err_exact + err_deposited + pure_shares;
      exp284's deposited err_deposited == exp256's deposited
      substituted err 72/72 (the two deposits' chain anchor);
      exp284's deposited branch == WALK-CLASS-BLIND asserted (the
      pre-registered context). THE S0 ANCHOR (both halves, from the
      fresh battery): the re-run's final errs reproduce exp256's
      DEPOSITED substituted errs BIT-EXACT (72/72, the machinery's
      native 2-dp convention; the verified flags 72/72), AND exp284's
      deposited per-class shares reproduce BIT-EXACT (the fresh
      per_class frac_of_sq x 3 == exp284's deposited x 3, 72/72 x 3 —
      with sum_sq and n_cells asserted beside; the fresh err_exact ==
      exp284's err_exact 72/72; the fresh trace_sha256 == exp284's
      trace_sha256 72/72 — the decomposition is of the SAME walk
      exp284 deposited; the fresh boundary's own share == exp284's
      deposited pure boundary-ring share 72/72). The carries: the mia
      carry bit-exact 12/12 (exp273's field table == exp243's own
      class records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS sha-verified
      against the current file bytes — exp243 (4) + exp256 (3) +
      exp272 (4) + exp273 (5) + exp284 (6) = 22 records. The source
      deposits READ-ONLY: sha-recorded BEFORE any read, byte-unchanged
      after the work (5 deposits).
  G2  THE RING DEFINITION (zero knobs, asserted per row, all 72): the
      ring = {j not in boundary : exists i in boundary with
      A[i,j] > 0} on exp208's classify boundary set
      (classify(T_instance, A_host) VERBATIM) + the medium's pair
      support; asserted (a) DISJOINT from the boundary set — the
      constructed ring index set shares no element with the boundary
      index set, and (b) COVERING NO boundary cells — the boolean
      ring & boundary masks all-False; the three-way partition
      boundary / ring / rest covers n=400 (the counts sum to 400, the
      masks pairwise disjoint, 72/72); the ring NONEMPTY 72/72 (a
      degenerate empty ring STOPs honestly — fail=STOP); the per-row
      THREE-WAY identity sum_{parts} sum_sq / n == err_exact^2 within
      1e-6 * max(1.0, err_exact^2) (exp208's identity form, asserted
      fail=STOP) + the ring-split fracs sum to 1.0 within 1e-9; the
      A3 state-convention assert 72/72; the ring split's BOUNDARY part
      == exp284's deposited pure boundary-ring share BIT-EXACT 72/72
      (the new instrument tied to exp284's lead by construction, then
      asserted); the classification anchor — the fresh worst-instance
      mask counts == exp256's deposited row class_counts 36/36; the
      per-row ring count + the identity residual + the settle gap
      recorded (the maxima, audit-only).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): the
      branch resolved on the pre-named 0.5 SIGNED house bar —
      RING-CARRIED iff max(rho_ring~mia, rho_ring~premium) >= 0.5
      (positive), RING-ABSENT otherwise. Audit-only, never gating: the
      full 12-host ordering by frac_ring_mean; the boundary-share +
      rest-share regressions; the ANTI-ALIGNED variant named per
      target (rho <= -0.5); exp284's audit-only face recomputed beside
      (the fresh per-host boundary shares == exp284's deposited
      pure_boundary_ring_share means BIT-EXACT 12/12; the
      outliers-vs-cluster pure-share margin recomputed from the fresh
      means == the margin from exp284's deposited means bit-exact; the
      fresh ordering by the boundary share beside exp284's); exp284's
      WALK-CLASS-BLIND label margins re-read beside (the exp208-label
      shares stay the registered face — the ring is the NEW grain,
      additive, never a replacement).
  G4  THE DISCIPLINE: deterministic — the fresh re-run executes TWICE,
      the two passes' row payloads (errs, ring splits,
      decompositions, tables, rhos) BIT-IDENTICAL; no wall-clock
      fields (recursive key scan + serialized-blob scan); the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): RING-CARRIED / RING-ABSENT.

RUN: the deterministic sha-asserted rebuild (seconds) + the fresh
72-row state-carrying battery run TWICE (72 decodes per pass),
foreground ~2 min total, far under the 570 s cap. If a pass cannot
finish inside the 570 s cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE
pass per invocation (env EXP285_MODE=pass1|pass2 caches that pass's
row payload) and the PRE-NAMED MERGE (env EXP285_MODE=merge) compares
the two cached payloads BIT-EXACT and writes the deposit — the merge
never recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp285_pure_ring_grain.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit dffdc37) ==========================
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
    #      is the dffdc37 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "99fc7f81072b2a9187bbc48e871b56939c05e3fcb464ab9b83d38944ce82a7cb")
    EXPECTED_HEADER_SHA256 = (
        "60905793aef69dc5c2b03e942fe0a47ba9656ec8bfdd530af3ad6ddbcf520895")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from dffdc37"
    assert header_ok, "header drifted from dffdc37"

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
    RING_RHO_BAR = 0.5                     # the pre-named 0.5 SIGNED bar (G3)

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
    DEP284 = os.path.join(ROOT, "results",
                          "exp284_endpoint_composition.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP284)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP284: "exp284_deposit"}
    ro_before = {name: _sha(p) for p, name in _dep_names.items()}

    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP272) as fh:
        dep272 = json.load(fh)
    with open(DEP273) as fh:
        dep273 = json.load(fh)
    with open(DEP284) as fh:
        dep284 = json.load(fh)

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep284["hosts"] == hosts, "exp284's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    assert dep272["descriptive"]["premium_hosts"] == outliers, \
        "exp272's premium_hosts drifted from the outlier pre-name"
    assert dep284["outliers"] == outliers, "exp284's outliers drifted"
    cluster = [h for h in hosts if h not in outliers]
    assert len(cluster) == 10, "the ten-host cluster drifted"

    rec272 = {r["host"]: r for r in dep272["per_host"]}
    ft273 = {rec["field"]: rec for rec in dep273["field_table"]}

    # ---- exp208's classify VERBATIM (the T + W masks; the boundary
    #      ring wins precedence, then the junction; the interior rides
    #      the cls-0 complement — exp277's disclosed mask semantics) ----
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

    # ---- exp208's decompose conventions VERBATIM (the mean-squared
    #      scale the RMS actually decomposes; the identity asserted
    #      fail=STOP) -------------------------------------------------------
    def _decompose_end_state(V, T, cls, err_exact):
        e2 = (np.asarray(V, dtype=float)
              - np.asarray(T, dtype=float)) ** 2
        total = float(e2.sum())
        n = len(e2)
        per = []
        for name, mask in (("CANON-BOUNDARY", cls == 0),
                           ("PAIR-JUNCTION", cls == 1),
                           ("INTERIOR", cls == 2)):
            ss = float(e2[mask].sum())
            per.append({"class": name, "n_cells": int(mask.sum()),
                        "sum_sq": ss,
                        "frac_of_sq": ss / total if total > 0 else 0.0,
                        "rms_contrib_mV":
                            float(np.sqrt(ss / n)) if n else 0.0})
        # THE ACCOUNTING IDENTITY (the RMS convention, disclosed):
        # the shares are mean-squared contributions in mV^2 and sum to
        # err^2 — the identity on the scale the RMS actually decomposes
        ident = abs(sum(p["sum_sq"] for p in per) / n
                    - err_exact ** 2)
        assert ident < 1e-6 * max(1.0, err_exact ** 2), \
            f"accounting identity violated: {ident}"
        assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
        return {"per_class": per, "identity_residual": ident, "e2": e2}

    # ---- the pure-mask shares from classify's own masks (exp284's
    #      audit-only face; the boundary cell's own share) ----------------
    def _pure_shares(e2, cinfo):
        total = float(e2.sum())
        if total <= 0:
            return {"boundary_ring": 0.0, "pair_junction_only": 0.0,
                    "interior_only": 0.0}
        return {
            "boundary_ring": float(e2[cinfo["boundary"]].sum() / total),
            "pair_junction_only":
                float(e2[cinfo["junction"]].sum() / total),
            "interior_only": float(e2[cinfo["interior"]].sum() / total)}

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

    # ---- THE TRACED REPLICA: exp282's _execute_signed_traced REUSED
    #      VERBATIM (landed at 8ca252e — exp142's walk byte-similar +
    #      exactly the disclosed recording additions: (a) the per-step
    #      RMS read after each commit (a pure numpy read of the live V
    #      vs the target — draws NOTHING from the RNG stream); (b) the
    #      trace + the walk commit count attached to the returned dict;
    #      (c) the final state always carried (exp243's A3
    #      return_state semantics built in); (d) a no-op `order = []`
    #      initialization so the step count is well-defined on the
    #      empty-region branch (never taken on these rows); (e) the
    #      floor constant read via the exp142 module attribute (the
    #      same object exp142's own global resolves to). The RNG
    #      stream, dt, canon, walk order, commits: UNTOUCHED. exp142
    #      itself is NOT modified.) ---------------------------------------
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

    # ---- one traced + ring-split row decode (exp284's
    #      _decode_row_composition form with the exp284 anchor replacing
    #      the exp282 anchor + THE RING — the only substantive addition:
    #      the per-cell end errors from final_state, exp208's classify
    #      on the row target + medium, the exp208-label decomposition,
    #      the exp284 bit-exact reproduction, the S0 anchor, and the
    #      pre-registered zero-knob ring + the three-way
    #      boundary/RING/rest end-RMS split) ------------------------------
    def _decode_row_ring(host, row_key, spec, med, seed, fmax,
                         dep_rec, rec284, med_A):
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
        # THE SAME WALK exp284 DEPOSITED: the re-run's trace sha ==
        # exp284's deposited trace_sha256 (exp282's walk carried through
        # exp284's deposit bit-exactly)
        trace_match = bool(trace_sha == rec284["trace_sha256"])
        assert trace_match, \
            (f"{host} {row_key} s{seed}: the fresh trace sha drifted from "
             f"exp284's deposited trace sha — the walk is not the traced one")
        walk_end_match = bool(final == float(rec284["walk_end_rms"]))
        assert walk_end_match, \
            (f"{host} {row_key} s{seed}: the fresh walk_end_rms drifted from "
             "exp284's deposited walk_end_rms")
        # THE S0 ANCHOR (G1's first half): the fresh run reproduces
        # exp256's deposited substituted err BIT-EXACT (the machinery's
        # native 2-dp form)
        s0_err_ok = bool(err == dep_rec["err"])
        s0_ver_ok = bool(bool(out["program_verified"]) == dep_rec["verified"])
        assert s0_err_ok, \
            (f"{host} {row_key} s{seed}: the fresh err {err} drifted from "
             f"exp256's deposited {dep_rec['err']} — S0 REFUTED")
        assert s0_ver_ok, f"{host} {row_key} s{seed}: the verified flag drifted"
        # THE COMPOSITION: the per-cell end errors + exp208's classify
        # on the row target + medium + exp208's decompose conventions
        settle_gap = abs(err_exact - final)
        cinfo = classify(T, med_A)
        decomp = _decompose_end_state(V, T, cinfo["class"], err_exact)
        e2 = decomp.pop("e2")
        counts = {"CANON-BOUNDARY": int(cinfo["boundary"].sum()),
                  "PAIR-JUNCTION": int(cinfo["junction"].sum()),
                  "INTERIOR": int(cinfo["interior"].sum())}
        partition_ok = bool(sum(counts.values()) == len(V)
                            and not np.any(cinfo["boundary"]
                                           & cinfo["junction"])
                            and not np.any(cinfo["boundary"]
                                           & cinfo["interior"])
                            and not np.any(cinfo["junction"]
                                           & cinfo["interior"]))
        assert partition_ok, \
            f"{host} {row_key} s{seed}: the class masks do not partition n"
        interior_label_empty = bool(decomp["per_class"][2]["n_cells"] == 0)
        assert interior_label_empty, \
            (f"{host} {row_key} s{seed}: the INTERIOR label record is not "
             "empty — the exp277 mask semantics drifted")
        # THE EXP284 ANCHOR (G1's second half): exp284's deposited
        # per-class shares reproduce BIT-EXACT
        pc_frac_ok = bool(all(
            decomp["per_class"][i]["frac_of_sq"]
            == float(rec284["per_class"][i]["frac_of_sq"])
            for i in range(3)))
        pc_sumsq_ok = bool(all(
            decomp["per_class"][i]["sum_sq"]
            == float(rec284["per_class"][i]["sum_sq"])
            for i in range(3)))
        pc_ncells_ok = bool(all(
            decomp["per_class"][i]["n_cells"]
            == int(rec284["per_class"][i]["n_cells"])
            for i in range(3)))
        assert pc_frac_ok and pc_sumsq_ok and pc_ncells_ok, \
            (f"{host} {row_key} s{seed}: the fresh per-class shares "
             "drifted from exp284's deposited per-class shares")
        errexact284_ok = bool(err_exact == float(rec284["err_exact"]))
        assert errexact284_ok, \
            (f"{host} {row_key} s{seed}: the fresh err_exact drifted from "
             "exp284's deposited err_exact")
        psh = _pure_shares(e2, cinfo)
        bndshare284_ok = bool(
            psh["boundary_ring"]
            == float(rec284["pure_shares"]["boundary_ring"])
            and psh["pair_junction_only"]
            == float(rec284["pure_shares"]["pair_junction_only"])
            and psh["interior_only"]
            == float(rec284["pure_shares"]["interior_only"]))
        assert bndshare284_ok, \
            (f"{host} {row_key} s{seed}: the fresh pure boundary-ring "
             "share drifted from exp284's deposited pure share")
        # ==== THE RING (the pre-registered zero-knob addition): the
        #      ring = {j not in boundary : exists i in boundary with
        #      A[i,j] > 0} — the immediate non-boundary neighbors of the
        #      classify boundary set on the medium's pair support (the
        #      base is non-negative, asserted per host in the rebuild,
        #      so the read A[i,j] > 0 IS the |A| > 0 support exp208's
        #      classify uses) ============================================
        bnd = cinfo["boundary"]
        support = med_A > 0
        touches_bnd = support[bnd].any(axis=0)
        ring = (~bnd) & touches_bnd
        rest = ~(bnd | ring)
        bnd_idx = set(np.flatnonzero(bnd).tolist())
        ring_idx = set(np.flatnonzero(ring).tolist())
        # (a) DISJOINT from the boundary set — the constructed ring
        #     index set shares no element with the boundary index set
        ring_disjoint_index = bool(not (bnd_idx & ring_idx))
        assert ring_disjoint_index, \
            (f"{host} {row_key} s{seed}: the ring index set is not "
             "disjoint from the boundary index set")
        # (b) COVERING NO boundary cells — the boolean masks all-False
        ring_disjoint_mask = bool(not np.any(ring & bnd))
        assert ring_disjoint_mask, \
            (f"{host} {row_key} s{seed}: the ring mask covers boundary "
             "cells")
        ring_nonempty = bool(ring_idx)
        assert ring_nonempty, \
            (f"{host} {row_key} s{seed}: the ring is empty — the grain "
             "is degenerate on this row (fail=STOP)")
        counts3 = {"BOUNDARY": int(bnd.sum()), "RING": int(ring.sum()),
                   "REST": int(rest.sum())}
        ring_partition_ok = bool(
            sum(counts3.values()) == len(V)
            and not np.any(bnd & ring) and not np.any(bnd & rest)
            and not np.any(ring & rest))
        assert ring_partition_ok, \
            (f"{host} {row_key} s{seed}: the ring three-way split does "
             "not partition n")
        total = float(e2.sum())
        n_frm = len(e2)
        ring_split = []
        for name, mask in (("BOUNDARY", bnd), ("RING", ring),
                           ("REST", rest)):
            ss = float(e2[mask].sum())
            ring_split.append({"part": name, "n_cells": int(mask.sum()),
                               "sum_sq": ss,
                               "frac_of_sq": ss / total if total > 0 else 0.0,
                               "rms_contrib_mV":
                                   float(np.sqrt(ss / n_frm)) if n_frm else 0.0})
        ring_ident = abs(sum(p["sum_sq"] for p in ring_split) / n_frm
                         - err_exact ** 2)
        assert ring_ident < 1e-6 * max(1.0, err_exact ** 2), \
            (f"{host} {row_key} s{seed}: the ring three-way identity "
             f"violated: {ring_ident}")
        ring_fracsum_ok = bool(abs(
            sum(p["frac_of_sq"] for p in ring_split) - 1.0) < 1e-9)
        assert ring_fracsum_ok, \
            f"{host} {row_key} s{seed}: the ring fracs do not sum to 1"
        # the tie: the ring split's BOUNDARY part IS exp284's pure
        # boundary-ring share (the boundary cells' own squared-error
        # share) — the new grain tied to the lead by construction
        frac_b = ring_split[0]["frac_of_sq"]
        frac_r = ring_split[1]["frac_of_sq"]
        frac_t = ring_split[2]["frac_of_sq"]
        bnd_tie = bool(frac_b == float(rec284["pure_shares"]["boundary_ring"]))
        assert bnd_tie, \
            (f"{host} {row_key} s{seed}: the ring split's BOUNDARY part "
             "drifted from exp284's deposited pure boundary-ring share")
        return {
            "host": host, "seed": int(seed), "instance": int(row_key[-1]),
            "row_key": row_key, "pert": P3, "medium": "base",
            "err": err, "err_deposited": float(dep_rec["err"]),
            "err_exact": err_exact, "a3_ok": a3_ok,
            "verified": bool(out["program_verified"]),
            "branch": str(out["branch"]), "rho": float(out["rho"]),
            "walk_steps": steps, "trace_len": len(trace),
            "walk_end_rms": final,
            "walk_end_rms_deposited_exp284": float(rec284["walk_end_rms"]),
            "settle_gap_abs": float(settle_gap),
            "trace_sha256": trace_sha,
            "trace_sha256_matches_exp284": trace_match,
            "s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
            "conv_step": int(conv),
            "class_counts": counts,
            "per_class": decomp["per_class"],
            "identity_residual": decomp["identity_residual"],
            "pure_shares": psh,
            "partition_ok": partition_ok,
            "interior_label_empty": interior_label_empty,
            # the exp284 anchors (G1's second half)
            "errexact284_ok": errexact284_ok,
            "perclass284_frac_ok": pc_frac_ok,
            "perclass284_sumsq_ok": pc_sumsq_ok,
            "perclass284_ncells_ok": pc_ncells_ok,
            "bndshare284_ok": bndshare284_ok,
            # the ring (G2)
            "ring_counts": counts3,
            "ring_split": ring_split,
            "ring_identity_residual": float(ring_ident),
            "ring_fracsum_ok": ring_fracsum_ok,
            "ring_partition_ok": ring_partition_ok,
            "ring_disjoint_index_ok": ring_disjoint_index,
            "ring_disjoint_mask_ok": ring_disjoint_mask,
            "ring_nonempty_ok": ring_nonempty,
            "frac_boundary": frac_b, "frac_ring": frac_r,
            "frac_rest": frac_t,
            "bnd_part_tie284": bnd_tie}

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; the pre-named 22 records: exp243 4 + exp256 3 +
    #      exp272 4 + exp273 5 + exp284 6) --------------------------------
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
        ("exp284_endpoint_composition.json", "inputs"))

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
        assert total == 22, f"the chain record count {total} != 22"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

    # ---- THE COMPUTATION (one full pass: the sha-asserted rebuild +
    #      the fresh 72-row state-carrying battery + the ring split +
    #      the table + the branch; run twice — G4's two-pass clause) ----
    def compute():
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (exp269's/exp280's/exp284's form, every
        #      rebuild bit-asserted against exp243's OWN records) --------
        g1 = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0, "n_bnd_ok": 0,
              "n_bnd_dual_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
              "n_fmax_ok": 0, "n_nonneg_ok": 0, "n_rows256": 0,
              "n_structure_ok": 0, "n_worst_eq_max": 0,
              "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
              "n_rows284": 0, "n_284_chain_ok": 0,
              "n_s0_err_ok": 0, "n_s0_verified_ok": 0,
              "n_trace284_ok": 0, "n_walk_end284_ok": 0,
              "n_errexact284_ok": 0, "n_perclass284_frac_ok": 0,
              "n_perclass284_sumsq_ok": 0, "n_perclass284_ncells_ok": 0,
              "n_bndshare284_ok": 0, "n_mia_carry": 0, "n_prem_carry": 0}
        g2 = {"n_rows": 0, "n_a3_ok": 0,
              "n_ring_disjoint_index_ok": 0, "n_ring_disjoint_mask_ok": 0,
              "n_ring_partition_ok": 0, "n_ring_nonempty_ok": 0,
              "n_ring_identity_ok": 0, "n_ring_fracsum_ok": 0,
              "n_bnd_part_tie284_ok": 0, "n_class_anchor_ok": 0,
              "max_ring_identity_residual": 0.0, "max_settle_gap": 0.0,
              "min_ring_count": 10 ** 9, "max_ring_count": 0}
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
            assert nonneg, \
                (f"{h}: the base carries negative entries — the ring's "
                 "read A[i,j] > 0 would not be the |A| > 0 support")
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
            g1["n_hosts"] += 1
            g1["n_sha_ok"] += int(sha_ok)
            g1["n_edges_ok"] += int(edges_ok)
            g1["n_bnd_ok"] += int(bnd_ok)
            g1["n_bnd_dual_ok"] += int(bnd_dual)
            g1["n_canon_ok"] += int(canon_ok)
            g1["n_fmax_ok"] += int(fmax_ok)
            g1["n_nonneg_ok"] += int(nonneg)
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
        dep_rows256 = {}
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
            dep_rows256[(r["host"], int(r["seed"]))] = {
                "worst_row_key": r["worst_row_key"],
                "class_counts": r["class_counts"]}
        assert len(dep_sub) == 72, \
            "the 72 substituted instance records drifted"
        assert len(dep_rows256) == 36, \
            "the 36 substituted row records drifted"
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

        # ---- G1: THE EXP284 RE-READ (the anchor deposit) — the 72 row
        #      records with the per-class shares + the walk shas + the
        #      err chain anchor + the deposited branch -------------------
        rows284 = dep284["rows"]
        g1["n_rows284"] = len(rows284)
        assert len(rows284) == 72, "exp284's 72-row deposit drifted"
        assert dep284["branch"] == "WALK-CLASS-BLIND", \
            "exp284's deposited branch drifted from WALK-CLASS-BLIND"
        r284 = {}
        n_chain284 = 0
        for r in rows284:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r284, f"duplicate exp284 row {key}"
            assert len(r["per_class"]) == 3, \
                f"{key}: exp284's per_class drifted"
            assert all(fld in r for fld in
                       ("trace_sha256", "err_exact", "err_deposited",
                        "pure_shares", "walk_end_rms")), \
                f"{key}: exp284's row record is missing anchor fields"
            d256 = dep_sub[key]
            ok_chain = bool(float(r["err_deposited"]) == d256["err"])
            assert ok_chain, \
                (f"{key}: exp284's err_deposited drifted from exp256's "
                 "deposited substituted err — the two deposits' chain "
                 "anchor broken")
            n_chain284 += int(ok_chain)
            r284[key] = r
        g1["n_284_chain_ok"] = n_chain284
        assert g1["n_284_chain_ok"] == 72, \
            "exp284's err chain anchor drifted"
        ht284 = {row["host"]: row for row in dep284["host_table"]}
        assert len(ht284) == 12, "exp284's host table drifted"
        pb284 = {h: float(ht284[h]["pure_boundary_ring_share_mean"])
                 for h in hosts}

        # ---- G1: THE TARGETS (the pre-named carries, asserted bit-exact)
        mia = dict(ft273["exp243.classes.multi_identity_audit.prod_err"]
                   ["values"])
        assert set(mia) == set(hosts), "the mia field table drifted"
        for h in hosts:
            ok = bool(mia[h] == float(
                dep243["classes"][h]["multi_identity_audit"]["prod_err"]))
            assert ok, f"{h}: the mia carry drifted from exp243's records"
            g1["n_mia_carry"] += int(ok)
        prem = {h: float(rec272[h]["one_zone_premium_mean"])
                for h in hosts}
        prem_dep = dict(ft273["exp272.per_host.one_zone_premium_mean"]
                        ["values"])
        for h in hosts:
            ok = bool(prem[h] == float(prem_dep[h]))
            assert ok, f"{h}: the premium carry drifted from exp273's"
            g1["n_prem_carry"] += int(ok)
        assert g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12, \
            "the target carries drifted"
        targets = {
            "mia_prod_err": {
                "source": ("exp273's field-table field "
                           "'exp243.classes.multi_identity_audit.prod_err'"),
                "values": mia, "carry_vs_exp243_bit_exact": g1["n_mia_carry"]},
            "one_zone_premium": {
                "source": ("exp272's per-host one_zone_premium_mean "
                           "(the one-zone premium means)"),
                "values": prem,
                "carry_vs_exp273_field_table_bit_exact":
                    g1["n_prem_carry"]}}

        # ---- G1: THE PROVENANCE CHAINS (22 records) ---------------------
        chains = _verify_chains()

        # ---- G1 + G2: THE FRESH STATE-CARRYING RE-RUN (72 rows; the
        #      S0 anchor + exp284's shares reproduced bit-exactly + the
        #      ring split) ------------------------------------------------
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec = _decode_row_ring(
                        k, rk, ctx["deep"][inst]["spec"], med, s,
                        ctx["fmax"], d, r284[(k, s, rk)], med.A)
                    rows_out.append(rec)
                    g1["n_s0_err_ok"] += int(rec["s0_err_ok"])
                    g1["n_s0_verified_ok"] += int(rec["s0_verified_ok"])
                    g1["n_trace284_ok"] += int(
                        rec["trace_sha256_matches_exp284"])
                    g1["n_walk_end284_ok"] += int(
                        rec["walk_end_rms"]
                        == rec["walk_end_rms_deposited_exp284"])
                    g1["n_errexact284_ok"] += int(rec["errexact284_ok"])
                    g1["n_perclass284_frac_ok"] += int(
                        rec["perclass284_frac_ok"])
                    g1["n_perclass284_sumsq_ok"] += int(
                        rec["perclass284_sumsq_ok"])
                    g1["n_perclass284_ncells_ok"] += int(
                        rec["perclass284_ncells_ok"])
                    g1["n_bndshare284_ok"] += int(rec["bndshare284_ok"])
                    g2["n_rows"] += 1
                    g2["n_a3_ok"] += int(rec["a3_ok"])
                    g2["n_ring_disjoint_index_ok"] += int(
                        rec["ring_disjoint_index_ok"])
                    g2["n_ring_disjoint_mask_ok"] += int(
                        rec["ring_disjoint_mask_ok"])
                    g2["n_ring_partition_ok"] += int(
                        rec["ring_partition_ok"])
                    g2["n_ring_nonempty_ok"] += int(
                        rec["ring_nonempty_ok"])
                    g2["n_ring_identity_ok"] += int(
                        rec["ring_identity_residual"]
                        < 1e-6 * max(1.0, rec["err_exact"] ** 2))
                    g2["n_ring_fracsum_ok"] += int(rec["ring_fracsum_ok"])
                    g2["n_bnd_part_tie284_ok"] += int(
                        rec["bnd_part_tie284"])
                    g2["max_ring_identity_residual"] = max(
                        g2["max_ring_identity_residual"],
                        float(rec["ring_identity_residual"]))
                    g2["max_settle_gap"] = max(
                        g2["max_settle_gap"], float(rec["settle_gap_abs"]))
                    g2["min_ring_count"] = min(
                        g2["min_ring_count"],
                        int(rec["ring_counts"]["RING"]))
                    g2["max_ring_count"] = max(
                        g2["max_ring_count"],
                        int(rec["ring_counts"]["RING"]))
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] ring-split 6 rows | errs "
                  f"{[r['err'] for r in hs]} | ring_frac "
                  f"{[round(r['frac_ring'], 4) for r in hs]}")
        assert len(rows_out) == 72, \
            f"the ring battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"
        assert g2["min_ring_count"] <= g2["max_ring_count"], \
            "the ring count summary drifted"

        # ---- G2: THE CLASSIFICATION ANCHOR — the fresh worst-instance
        #      mask counts reproduce exp256's deposited row class_counts
        for (h, s), drow in dep_rows256.items():
            wrk = drow["worst_row_key"]
            fresh = next(r for r in rows_out
                         if r["host"] == h and r["seed"] == s
                         and r["row_key"] == wrk)
            ok = bool(fresh["class_counts"] == drow["class_counts"])
            assert ok, \
                (f"{h} s{s} {wrk}: the fresh classify mask counts "
                 f"{fresh['class_counts']} drifted from exp256's deposited "
                 f"{drow['class_counts']}")
            fresh["worst_instance"] = True
            fresh["class_counts_match_exp256"] = ok
            g2["n_class_anchor_ok"] += int(ok)
        for r in rows_out:
            r.setdefault("worst_instance", False)
            r.setdefault("class_counts_match_exp256", None)
        assert g2["n_class_anchor_ok"] == 36, \
            "the classification anchor drifted"

        # ---- THE PER-HOST TABLE (per-host means over the 6 rows) --------
        host_table = []
        for h in hosts:
            hs = [r for r in rows_out if r["host"] == h]
            assert len(hs) == 6, f"{h}: the 6 ring rows drifted"
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "frac_ring_mean": float(np.mean(
                    [r["frac_ring"] for r in hs])),
                "frac_boundary_mean": float(np.mean(
                    [r["frac_boundary"] for r in hs])),
                "frac_rest_mean": float(np.mean(
                    [r["frac_rest"] for r in hs])),
                "mean_ring_counts": {
                    kk: float(np.mean([r["ring_counts"][kk] for r in hs]))
                    for kk in ("BOUNDARY", "RING", "REST")},
                "mean_label_counts": {
                    kk: float(np.mean([r["class_counts"][kk] for r in hs]))
                    for kk in ("CANON-BOUNDARY", "PAIR-JUNCTION",
                               "INTERIOR")},
                "err_exact_mean": float(np.mean(
                    [r["err_exact"] for r in hs])),
                "walk_end_rms_deposited_exp284_mean": float(np.mean(
                    [r["walk_end_rms_deposited_exp284"] for r in hs])),
                "settle_gap_mean": float(np.mean(
                    [r["settle_gap_abs"] for r in hs]))})

        # ---- G3: exp284's audit-only face recomputed beside (the fresh
        #      boundary shares bit-exact vs exp284's deposited means; the
        #      pure-share margin recomputed == the deposited-derived) ----
        n_bndmean_ok = 0
        for row in host_table:
            ok = bool(row["frac_boundary_mean"] == pb284[row["host"]])
            assert ok, \
                (f"{row['host']}: the fresh boundary-share mean drifted "
                 "from exp284's deposited pure_boundary_ring_share_mean")
            n_bndmean_ok += int(ok)
        assert n_bndmean_ok == 12, \
            "the exp284 boundary-share means drifted"
        fb_out = {row["host"]: row["frac_boundary_mean"]
                  for row in host_table if row["outlier"]}
        fb_clu = [row["frac_boundary_mean"] for row in host_table
                  if not row["outlier"]]
        face_margin_fresh = min(fb_out.values()) - max(fb_clu)
        face_margin_dep = (min(pb284[h] for h in outliers)
                           - max(pb284[h] for h in cluster))
        assert face_margin_fresh == face_margin_dep, \
            "the exp284 pure-share margin recomputation drifted"
        exp284_face = {
            "branch_deposited": dep284["branch"],
            "deposited_label_margins": {
                "margin_cb": float(
                    dep284["branch_discriminant"]["margin_cb"]),
                "margin_pj": float(
                    dep284["branch_discriminant"]["margin_pj"])},
            "deposited_pure_boundary_share_means": pb284,
            "n_boundary_mean_bit_exact": n_bndmean_ok,
            "fresh_boundary_share_means_equal_deposited": True,
            "pure_share_outlier_margin_fresh": face_margin_fresh,
            "pure_share_outlier_margin_from_deposited": face_margin_dep,
            "margin_recomputed_equal": True,
            "ordering_by_frac_boundary": [
                {"host": row["host"],
                 "frac_boundary_mean": row["frac_boundary_mean"]}
                for row in sorted(host_table,
                                  key=lambda r: r["frac_boundary_mean"])]}

        # ---- THE REGRESSIONS (the exp274/exp275/exp282 conventions
        #      VERBATIM: Spearman = Pearson on the tied-average ranks;
        #      the single-predictor OLS rank R2; the ties census per
        #      vector; the GATING PAIR = the ring share's two rhos; the
        #      boundary-share + rest-share regressions AUDIT-ONLY) -------
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

        SHARE_COLS = {"frac_ring": [row["frac_ring_mean"]
                                    for row in host_table],
                      "frac_boundary": [row["frac_boundary_mean"]
                                        for row in host_table],
                      "frac_rest": [row["frac_rest_mean"]
                                    for row in host_table]}
        TARGET_COLS = {"mia_prod_err": [mia[h] for h in hosts],
                       "one_zone_premium": [prem[h] for h in hosts]}
        regressions = {}
        for tk, tvals in TARGET_COLS.items():
            for sk, x in SHARE_COLS.items():
                rho = _spearman(x, tvals)
                rk_resp = rankdata(np.asarray(x, dtype=float))
                r2_single = _r2([tvals], rk_resp)
                r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))],
                             rk_resp)
                regressions[f"{sk}~{tk}"] = {
                    "share": sk, "target": tk, "rho": rho,
                    "rho_abs": abs(rho), "rank_R2_single": r2_single,
                    "rank_R2_all_ranks": r2_all,
                    "all_ranks_minus_rho2": r2_all - rho * rho,
                    "ties_share": _ties_census(x),
                    "ties_target": _ties_census(tvals),
                    "gating": sk == "frac_ring"}

        # ---- G3: THE BRANCH DISCRIMINANT (pre-named numeric bars) -------
        rho_ring_mia = regressions["frac_ring~mia_prod_err"]["rho"]
        rho_ring_prem = regressions["frac_ring~one_zone_premium"]["rho"]
        if max(rho_ring_mia, rho_ring_prem) >= RING_RHO_BAR:
            branch_local = "RING-CARRIED"
        else:
            branch_local = "RING-ABSENT"
        anti_aligned = [
            {"target": tk, "rho": rho}
            for tk, rho in (("mia_prod_err", rho_ring_mia),
                            ("one_zone_premium", rho_ring_prem))
            if rho <= -RING_RHO_BAR]
        g3 = {
            "ring_rho_mia": rho_ring_mia,
            "ring_rho_premium": rho_ring_prem,
            "signed_bar": RING_RHO_BAR,
            "anti_aligned_targets": anti_aligned,
            "ordering_by_frac_ring": [
                {"host": row["host"], "frac_ring_mean": row["frac_ring_mean"]}
                for row in sorted(host_table,
                                  key=lambda r: r["frac_ring_mean"])],
            "ring_outlier_shares": {
                row["host"]: row["frac_ring_mean"] for row in host_table
                if row["outlier"]},
            "ring_cluster_max": max(row["frac_ring_mean"]
                                    for row in host_table
                                    if not row["outlier"]),
            "ring_cluster_min": min(row["frac_ring_mean"]
                                    for row in host_table
                                    if not row["outlier"]),
            "exp284_face": exp284_face,
            "branch": branch_local}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "rebuild_report": rebuild_report, "g1": g1, "g2": g2,
                "g3": g3, "rows": rows_out, "host_table": host_table,
                "targets": targets, "regressions": regressions,
                "provenance_chains": chains, "ro_before": ro_before,
                "lock_reads": len(_LOCK_LOG)}

    # ---- the mode dispatch (the pre-named RUN clause: the default
    #      two-pass in-process form; EXP285_MODE=pass1|pass2 checkpoints
    #      ONE pass; EXP285_MODE=merge compares the two cached payloads
    #      bit-exact and writes the deposit — the merge never recomputes)
    _MODE = os.environ.get("EXP285_MODE", "")
    _CK1 = os.path.join(ROOT, "results",
                        ".exp285_pass1.checkpoint.json")
    _CK2 = os.path.join(ROOT, "results",
                        ".exp285_pass2.checkpoint.json")

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
        print("=== exp285: THE PURE RING GRAIN (the end-RMS mass in the "
              "ring around the classify boundary set) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 ring rows, ONE FRESH RUN, "
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
                   and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
                   and g1["n_rows256"] == 72
                   and g1["n_structure_ok"] == 36
                   and g1["n_worst_eq_max"] == 36
                   and g1["n_deep_targets_ok"] == 72
                   and g1["n_medium_shas_ok"] == 72
                   and g1["n_rows284"] == 72
                   and g1["n_284_chain_ok"] == 72
                   and g1["n_s0_err_ok"] == 72
                   and g1["n_s0_verified_ok"] == 72
                   and g1["n_trace284_ok"] == 72
                   and g1["n_walk_end284_ok"] == 72
                   and g1["n_errexact284_ok"] == 72
                   and g1["n_perclass284_frac_ok"] == 72
                   and g1["n_perclass284_sumsq_ok"] == 72
                   and g1["n_perclass284_ncells_ok"] == 72
                   and g1["n_bndshare284_ok"] == 72
                   and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
                   and pa["provenance_chains"]["total_verified"] == 22
                   and ro_unchanged)
    g2_pass = bool(g2["n_rows"] == 72 and g2["n_a3_ok"] == 72
                   and g2["n_ring_disjoint_index_ok"] == 72
                   and g2["n_ring_disjoint_mask_ok"] == 72
                   and g2["n_ring_partition_ok"] == 72
                   and g2["n_ring_nonempty_ok"] == 72
                   and g2["n_ring_identity_ok"] == 72
                   and g2["n_ring_fracsum_ok"] == 72
                   and g2["n_bnd_part_tie284_ok"] == 72
                   and g2["n_class_anchor_ok"] == 36)
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
        "G1_rebuild_s0_anchor_integrity": {
            "pass": g1_pass,
            "counts": g1,
            "provenance_chains": pa["provenance_chains"],
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "s0_anchor": ("the re-run's final errs reproduce exp256's "
                          "deposited substituted errs bit-exact (72/72, "
                          "the machinery's native 2-dp convention) and "
                          "exp284's deposited per-class shares reproduce "
                          "bit-exact (frac_of_sq x3 72/72 x3 + sum_sq + "
                          "n_cells + err_exact + trace_sha256 — the SAME "
                          "walk exp284 deposited)")},
        "G2_ring_definition_zero_knobs": {
            "pass": g2_pass,
            "counts": g2,
            "ring_form": ("ring = {j not in boundary : exists i in "
                          "boundary with A[i,j] > 0} — exp208's classify "
                          "boundary set on the row target + medium, the "
                          "medium's pair support; asserted per row: "
                          "disjoint from the boundary set (index-set "
                          "form) + covering no boundary cells (mask "
                          "form) + the three-way partition "
                          "boundary/ring/rest covers n=400 + the ring "
                          "nonempty (fail=STOP) + the identity "
                          "sum_parts sum_sq / n == err_exact^2 within "
                          "1e-6 * max(1.0, err_exact^2) (exp208's "
                          "identity form) + the fracs sum to 1.0 within "
                          "1e-9; the ring split's BOUNDARY part == "
                          "exp284's deposited pure boundary-ring share "
                          "bit-exact")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bar": ("RING-CARRIED iff max(rho_ring~mia, "
                    "rho_ring~premium) >= 0.5 — the SIGNED house bar, "
                    "positive; RING-ABSENT otherwise (named honestly); "
                    "the ANTI-ALIGNED variant (rho <= -0.5) named per "
                    "target, never gating")},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_s0_anchor_integrity",
                 "G2_ring_definition_zero_knobs",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    branch = g3["branch"]
    rho_ring_mia = g3["ring_rho_mia"]
    rho_ring_prem = g3["ring_rho_premium"]
    anti = g3["anti_aligned_targets"]
    face = g3["exp284_face"]
    ring_out = g3["ring_outlier_shares"]
    ring_clu_max = g3["ring_cluster_max"]
    ring_clu_min = g3["ring_cluster_min"]

    def _g(x):
        return f"{x:+.4f}"

    verdict_body = (
        f"{branch} — "
        + ("the end-RMS mass in the ring around the classify boundary "
           "set reaches the 0.5 SIGNED house bar"
           if branch == "RING-CARRIED" else
           "the ring around the classify boundary set carries NOTHING "
           "at the 0.5 SIGNED house bar — the ring grain joins the "
           "exp208-label classes as exposure-blind; the carrier's "
           "exposure lives in neither the boundary cells, their "
           "immediate non-boundary neighbors, nor the label "
           "decomposition")
        + f" (rho_ring~mia {rho_ring_mia:+.4f} / rho_ring~premium "
        f"{rho_ring_prem:+.4f} vs the pre-named >= 0.5 SIGNED bar; the "
        f"outliers' mean ring shares H3 {ring_out['H3']:.4f} / H5 "
        f"{ring_out['H5']:.4f} vs the cluster max {ring_clu_max:.4f}"
        + ("; THE ANTI-ALIGNED FACE crossed: "
           + ", ".join(f"{a['target']} {a['rho']:+.4f}" for a in anti)
           if anti else "")
        + f") | exp284's audit-only face beside (the pure boundary-share "
        f"margin {_g(face['pure_share_outlier_margin_fresh'])} recomputed "
        f"bit-exact vs the deposited means; exp284's branch "
        f"{face['branch_deposited']} with label margins "
        f"{_g(face['deposited_label_margins']['margin_cb'])} cb / "
        f"{_g(face['deposited_label_margins']['margin_pj'])} pj) | the "
        f"ring: mean ring count per row within [{g2['min_ring_count']}, "
        f"{g2['max_ring_count']}] of n=400, disjoint from the boundary "
        f"set and covering no boundary cells 72/72 (index-set + mask "
        f"forms), the three-way identity max residual "
        f"{g2['max_ring_identity_residual']:.2e} | THE S0 ANCHOR: the "
        f"fresh re-run reproduced exp256's deposited substituted errs "
        f"bit-exact ({g1['n_s0_err_ok']}/72, the verified flags "
        f"{g1['n_s0_verified_ok']}/72) AND exp284's deposited per-class "
        f"shares bit-exactly (frac_of_sq x3 {g1['n_perclass284_frac_ok']}"
        f"/72, sum_sq {g1['n_perclass284_sumsq_ok']}/72, n_cells "
        f"{g1['n_perclass284_ncells_ok']}/72, err_exact "
        f"{g1['n_errexact284_ok']}/72, trace_sha256 "
        f"{g1['n_trace284_ok']}/72 — the decomposition is of the SAME "
        f"walk exp284 deposited; the settle gap max "
        f"{g2['max_settle_gap']:.4f} mV, audit-only) | the "
        f"classification anchor {g2['n_class_anchor_ok']}/36 (the fresh "
        f"worst-instance mask counts == exp256's deposited row "
        f"class_counts) | 12 hosts, a deterministic sha-asserted rebuild "
        f"(graph_path for H0/H1, small_world at the deposited rewire "
        f"seeds — exp269's/exp280's form; the bases non-negative "
        f"asserted — the ring's read A[i,j] > 0 IS the |A| > 0 support), "
        f"the provenance chains sha-verified 22/22, 5 deposits READ-ONLY "
        f"byte-unchanged, two-pass bit-identical, floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp285_pure_ring_grain",
        "claim": (
            "THE PURE RING GRAIN (batch 43, pre-registration commit "
            "dffdc37): exp284's audit-only sub-bar live lead promoted "
            "to the instrument — on the boundary's own share the "
            "outliers H3/H5 hold the two highest values (0.1501/0.1601 "
            "vs the ten-host cluster's [0.0489, 0.1094], margin "
            "+0.0406), below the 0.05 bar; exp285 widens the grain by "
            "one hop and asks whether the end-RMS mass in the RING "
            "AROUND the classify boundary set carries the exposure at "
            "the 0.5 SIGNED house bar. The zero-knob ring definition: "
            "the ring = {j not in boundary : exists i in boundary with "
            "A[i,j] > 0} — exp208's classify VERBATIM on the row "
            "target + medium yields the boundary set B; the ring is "
            "the immediate non-boundary neighbors of B on the medium's "
            "pair support (the rebuilt bases non-negative asserted per "
            "host — the read A[i,j] > 0 IS the |A| > 0 support "
            "convention exp208's classify uses). exp284's landed body "
            "REUSED VERBATIM (the traced replica + the host rebuild + "
            "the end-state decomposition) — ONE FRESH RUN of the SAME "
            "72 substituted rows (12 hosts x 3 seeds x the two deep "
            "instances at n=400 — exp256's battery), zero new "
            "simulation beyond the one battery; the ONLY addition the "
            "ring mask + the per-row THREE-WAY end-RMS split boundary/"
            "RING/rest (exp208's decompose conventions VERBATIM on the "
            "mean-squared scale); the per-host ring/boundary/rest "
            "share means regressed against mia_prod_err (exp273's "
            "field table) and exp272's one-zone premium means under "
            "the exp274/exp275/exp282 conventions; the branch "
            "RING-CARRIED (the ring share's signed Spearman >= 0.5 "
            "against >= 1 target) / RING-ABSENT, pre-named, never fit"),
        "method": {
            "ring_definition": (
                "per row: bnd = classify(T_instance, A_host)"
                "[\"boundary\"] (exp208's classify VERBATIM); support "
                "= A > 0 (the base non-negative, asserted per host in "
                "the rebuild — the |A| > 0 pair-support convention); "
                "ring = (~bnd) & support[bnd].any(axis=0); rest = "
                "~(bnd | ring); zero knobs — no thresholds, no "
                "weights, no degree bars, no distance bands"),
            "ring_split": (
                "exp208's decompose conventions VERBATIM on the "
                "three-way split: per part sum_sq = sum e_i^2; "
                "frac_of_sq = sum_sq / total; rms_contrib_mV = "
                "sqrt(sum_sq / n); the identity sum_parts sum_sq / n "
                "== err_exact^2 within 1e-6 * max(1.0, err_exact^2) "
                "asserted fail=STOP; the fracs sum to 1.0 within 1e-9; "
                "the ring split's BOUNDARY part == exp284's deposited "
                "pure boundary-ring share bit-exact (the tie to the "
                "lead)"),
            "end_rms": (
                "err_exact = sqrt(mean((V - T)^2)) from the "
                "state-carrying read's final_state — the A3-checked "
                "state convention (round(err_exact, 2) == the reported "
                "err; the S0 anchor pins the reported err to exp256's "
                "deposited substituted errs bit-exact); the PRE-settle "
                "trace[-1] carrier vs the POST-settle end state "
                "disclosed pre-body in exp284 — carried; the settle "
                "gap recorded (audit-only)"),
            "classification": (
                "exp208's classify VERBATIM per instance: "
                "classify(T_instance, A_host); the exp208-label "
                "decomposition carried for the exp284 anchor + the "
                "walk-vs-decode comparability (the exp208-label "
                "CANON-BOUNDARY record is the NON-PAIR-JUNCTION "
                "complement, exp277's disclosure); the classification "
                "anchor — the fresh worst-instance mask counts == "
                "exp256's deposited row class_counts"),
            "table": ("per-host means over the host's 6 substituted "
                      "rows (3 seeds x 2 instances)"),
            "branch_rule": (
                "RING-CARRIED iff max(rho_ring~mia, rho_ring~premium) "
                ">= 0.5 — the SIGNED house bar, positive, fixed at "
                "pre-registration, never fit; RING-ABSENT otherwise "
                "(named honestly); the ANTI-ALIGNED variant (rho <= "
                "-0.5) named per target in the deposit + verdict, "
                "never gating (exp280/exp281's precedent)"),
            "regressions": (
                "the exp274/exp275/exp282 conventions VERBATIM: "
                "Spearman = Pearson on the tied-average ranks (scipy "
                "rankdata); the single-predictor OLS rank R2 (the "
                "response as its tied-average ranks, the target as "
                "the numeric design column) + the all-ranks variant "
                "AUDIT-ONLY; the ties census per vector; the 12-slot "
                "frame with the H0==H1 echo carried; the GATING PAIR "
                "= frac_ring~mia_prod_err and frac_ring~"
                "one_zone_premium; the frac_boundary and frac_rest "
                "regressions recorded audit-only")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base) + the mia audit errs "
                "(T_mia's direct carry)",
                "the 72 rows — the S0 anchor's deposited substituted "
                "instance errs + the deep-row target/medium shas + the "
                "row-level class_counts (the classification anchor)",
                "the host frame + the per-host one-zone premium means "
                "(T_prem) + the boundary counts + the outlier "
                "pre-name source",
                "the outlier pre-name + the field-table carries (the "
                "mia field + the premium carry, bit-exact)",
                "the anchor deposit — the 72 per-row per-class shares "
                "+ the walk trace shas (the bit-exact same-walk "
                "anchor) + the pure boundary-ring shares (the "
                "audit-only face) + the deposited WALK-CLASS-BLIND "
                "branch + the label margins"))},
        "hosts": pa["hosts"],
        "outliers": pa["outliers"],
        "cluster": pa["cluster"],
        "rebuild_report": pa["rebuild_report"],
        "provenance_chains": pa["provenance_chains"],
        "rows": pa["rows"],
        "host_table": pa["host_table"],
        "targets": pa["targets"],
        "regressions": pa["regressions"],
        "exp284_face": pa["g3"]["exp284_face"],
        "gates": gates,
        "branch": branch,
        "branch_discriminant": {
            "ring_rho_mia": rho_ring_mia,
            "ring_rho_premium": rho_ring_prem,
            "signed_bar": RING_RHO_BAR,
            "anti_aligned_targets": anti,
            "ring_outlier_shares": g3["ring_outlier_shares"],
            "ring_cluster_max": g3["ring_cluster_max"],
            "ring_cluster_min": g3["ring_cluster_min"],
            "ordering_by_frac_ring": g3["ordering_by_frac_ring"],
            "bar_pre_named_at": ("dffdc37 — the 0.5 SIGNED house bar, "
                                 "positive, fixed at pre-registration, "
                                 "never fit")},
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
        "docstring_byte_unchanged_vs_dffdc37": docstring_ok,
        "header_byte_unchanged_vs_dffdc37": header_ok,
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

    print(f"\n  G1 rebuild + S0 anchor integrity: "
          f"{'PASS' if gates['G1_rebuild_s0_anchor_integrity']['pass'] else 'FAIL'} "
          f"(the 12 bases rebuilt — graph_path for H0/H1, small_world at "
          f"the deposited seeds — sha-asserted vs exp243's records "
          f"{g1['n_sha_ok']}/12 + edges {g1['n_edges_ok']}/12 + the "
          f"classify boundary count {g1['n_bnd_dual_ok']}/12 dual-carried "
          f"vs exp272+exp273 + the canon identity {g1['n_canon_ok']}/12 + "
          f"H0 == H1 + f_max {g1['n_fmax_ok']}/12 + non-negative "
          f"{g1['n_nonneg_ok']}/12; the deep targets "
          f"{g1['n_deep_targets_ok']}/72 + the medium shas "
          f"{g1['n_medium_shas_ok']}/72; exp284's re-read: rows "
          f"{g1['n_rows284']}/72 + the err chain anchor "
          f"{g1['n_284_chain_ok']}/72; THE S0 ANCHOR — the fresh errs == "
          f"exp256's deposited substituted errs bit-exact "
          f"{g1['n_s0_err_ok']}/72 + the verified flags "
          f"{g1['n_s0_verified_ok']}/72 AND exp284's per-class shares "
          f"bit-exact (frac {g1['n_perclass284_frac_ok']}/72, sum_sq "
          f"{g1['n_perclass284_sumsq_ok']}/72, n_cells "
          f"{g1['n_perclass284_ncells_ok']}/72, err_exact "
          f"{g1['n_errexact284_ok']}/72, trace sha "
          f"{g1['n_trace284_ok']}/72, walk_end "
          f"{g1['n_walk_end284_ok']}/72, the boundary's own share "
          f"{g1['n_bndshare284_ok']}/72); the carries mia "
          f"{g1['n_mia_carry']}/12 + premium {g1['n_prem_carry']}/12; the "
          f"provenance chains "
          f"{pa['provenance_chains']['total_verified']}/22)")
    print(f"  G2 ring definition (zero knobs): "
          f"{'PASS' if gates['G2_ring_definition_zero_knobs']['pass'] else 'FAIL'} "
          f"(disjoint from the boundary set — index-form "
          f"{g2['n_ring_disjoint_index_ok']}/72, mask-form "
          f"{g2['n_ring_disjoint_mask_ok']}/72; the three-way partition "
          f"{g2['n_ring_partition_ok']}/72; the ring nonempty "
          f"{g2['n_ring_nonempty_ok']}/72 (ring count per row within "
          f"[{g2['min_ring_count']}, {g2['max_ring_count']}]); the "
          f"identity {g2['n_ring_identity_ok']}/72 (max residual "
          f"{g2['max_ring_identity_residual']:.2e}); the fracs sum to 1 "
          f"{g2['n_ring_fracsum_ok']}/72; the A3 convention "
          f"{g2['n_a3_ok']}/72; the BOUNDARY-part tie vs exp284 "
          f"{g2['n_bnd_part_tie284_ok']}/72; the classification anchor "
          f"{g2['n_class_anchor_ok']}/36; the settle gap max "
          f"{g2['max_settle_gap']:.4f} mV)")
    print("  the 12-host ring table (per-host means; H3/H5 the "
          "outliers):")
    for row in pa["host_table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} ring {row['frac_ring_mean']:.4f}  "
              f"bnd {row['frac_boundary_mean']:.4f}  rest "
              f"{row['frac_rest_mean']:.4f}  ring_n "
              f"{row['mean_ring_counts']['RING']:.1f}  err_exact "
              f"{row['err_exact_mean']:.3f}{tag}")
    print("  G3 branch — the regressions (the exp274/exp275/exp282 "
          "conventions; the ring pair GATING):")
    for k, v in pa["regressions"].items():
        print(f"      {k:32s} rho {v['rho']:+.4f}  (abs "
              f"{v['rho_abs']:.4f}){'  <== GATING' if v['gating'] else ''}")
    print(f"      exp284's face: branch {face['branch_deposited']} | its "
          f"label margins cb "
          f"{_g(face['deposited_label_margins']['margin_cb'])} / pj "
          f"{_g(face['deposited_label_margins']['margin_pj'])} | the "
          f"pure boundary-share margin "
          f"{_g(face['pure_share_outlier_margin_fresh'])} (recomputed "
          f"bit-exact vs the deposited means)")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock}; 5 deposits READ-ONLY byte-unchanged: "
          f"{ro_unchanged})")
    print(f"\n  BRANCH: {branch} | rho_ring~mia {rho_ring_mia:+.4f} | "
          f"rho_ring~premium {rho_ring_prem:+.4f} | the pre-named 0.5 "
          f"SIGNED bar "
          f"{'REACHED' if branch == 'RING-CARRIED' else 'NOT reached'}")
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
