#!/usr/bin/env python3
"""exp286 — THE ENDPOINT'S DOSE: THE END-RMS CARRIER'S OWN PARAMETER,
THE WALK'S STEP BUDGET (batch 44; ledger L263's derived item — batch 43
closed the grain screen at three levels, all exposure-blind at the 0.5
SIGNED bar: the exp208-label classes (exp277 decode NEITHER + exp284
walk CLASS-BLIND), the boundary's own share (exp284's audit-only
sub-bar lead), the ring around it (exp285 RING-ABSENT) — so the
carrier's exposure stays in the walk's ENDPOINT MAGNITUDE (exp282's
+0.88). This module turns to the carrier's OWN parameter: the walk's
step budget).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED on walk_end_rms
(the walk's trace[-1]; signed Spearman +0.8826151316282213 against
mia_prod_err, +0.8807017543859651 against exp272's one-zone premium
means; the 0.5 SIGNED house bar). The production budget is exp142's
STEPS_PER_CELL == 8 — the number of integration steps the walk takes
per committed cell before the commit draw. Is the endpoint magnitude a
FIXED POINT of the walk — invariant to the budget — or an artifact of
the production dose? If the endpoint is budget-invariant, the premium
is the walk's fixed point; if the outlier hosts' (H3/H5's) budget
response differs from the ten-host cluster's, the premium is a BUDGET
artifact — the excess endpoint magnitude produced by the production
dose rather than carried by the host structure.

THE LADDER (pre-named, fixed HERE at pre-registration): budgets
{4, 8, 16} — 4 HALVES the production budget, 8 IS the production
default (asserted == exp142's STEPS_PER_CELL), 16 DOUBLES it. The dose
is delivered as integration steps per committed cell; the walk ORDER
is untouched (asserted per row: walk_steps IDENTICAL across the three
budgets — the budget scales the steps per cell, never the visit order;
the delivered dose per row = budget * walk_steps, the {4x, 8x, 16x}
ladder per cell).

THE INSTRUMENT (pre-registered, zero new simulation beyond the one
battery x the three budgets): exp284/exp285's landed traced replica
REUSED VERBATIM (_execute_signed_traced, landed 8ca252e, reused since
f3ca053: exp142's walk byte-similar + exactly the disclosed recording
additions; the RNG stream / dt / canon / walk order / commits
untouched; exp142 NOT modified) with ONE DISCLOSED PARAMETERIZATION:
the per-cell loop bound is read from an explicit budget argument
instead of the module constant — at budget 8 the code path IS the
landed replica's, and it is ANCHORED BIT-EXACT against exp282's
deposited walks (G1: the trace sha256 + walk_end_rms reproduce 72/72).
Plus the host rebuild (exp269's/exp280's/exp284's/exp285's form) and
exp256's _scoped_row_read_state form (the projection chain PN1/PN2 +
TC1 + TC2 + the traced TC3). ONE FRESH RUN of the SAME 72 substituted
rows (12 hosts x 3 seeds (1,2,3) x the two deep instances
r-60i0/r-60i1 at n=400 — exp256's battery) DECODED AT EACH BUDGET —
216 decodes per pass. NO classify / decompose / mask work on the rows
— the dose question is budget-level, not grain-level (the grain screen
is closed; exp285's ring machinery is deliberately absent). The
per-cell end errors are NOT re-decomposed — the endpoint magnitude is
the read.

THE PER-ROW READS: per row and per budget — the end RMS (the walk's
trace[-1], the PRE-settle carrier; the POST-settle err_exact + the
settle gap recorded audit-only), the reported err, the A3-checked
state convention, the trace sha256 (recorded at EVERY budget; asserted
== exp282's deposit at budget 8; the 4/16 shas recorded for any future
re-verification), walk_steps, the convergence point (TA3), the
delivered step count. THE PER-HOST MEANS: over the host's 6 rows
(3 seeds x 2 instances) of the end RMS at each budget.

THE PRE-NAMED READS: (1) THE BUDGET SENSITIVITY — per host the ratios
r4 = mean_end_RMS(4) / mean_end_RMS(8) and r16 = mean_end_RMS(16) /
mean_end_RMS(8); if ~1.0 the endpoint is budget-invariant — the walk's
fixed point; the outliers' ratios vs the cluster's decide the artifact
question. (2) THE EXP282 ANCHOR AT THE DEFAULT — the regressions of
the end_RMS(8) carrier (the per-host means) against mia_prod_err
(exp273's field table, asserted == exp243's own class records) and
exp272's one-zone premium means (asserted == exp273's field-table
carry) under the exp274/exp275/exp282 conventions VERBATIM (Pearson on
the tied-average ranks, the 12-slot frame with the H0==H1 echo
carried, the ties census per vector, the single-predictor rank R2),
ASSERTED BIT-EXACT == exp282's deposited rhos — the default-budget
carrier reproduced, not re-fit. (3) THE BRANCH (below).

THE BRANCH (pre-named, the bars numeric, fixed HERE at
pre-registration, never fit): with INV_BAND = 0.10, INV_MIN_HOSTS =
10, SEP_MARGIN = 0.10 — N_inv = #{hosts : |r4 - 1| <= INV_BAND AND
|r16 - 1| <= INV_BAND}; BUDGET-INVARIANT iff N_inv >= INV_MIN_HOSTS
(both ratios within 1.0 +/- 0.1 on >= 10/12 hosts — the premium is the
walk's fixed point); else BUDGET-ARTIFACT iff the outliers' ratios
SEPARATE from the cluster's: min(r | outliers) - max(r | cluster) >
SEP_MARGIN or min(r | cluster) - max(r | outliers) > SEP_MARGIN, on r4
or r16, either direction (the premium tracks the budget — a BUDGET
artifact); else MIXED (named honestly). The full orderings + the
outlier margins recorded audit-only, never gating.

PRE-REGISTERED GATES (each evaluated exactly once, assembled on the
first pass's data):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280/exp284/exp285 precedent (graph_path
      at the chain class's n=400 call site for H0/H1 — H0 echoes H1
      bit-exactly, asserted; small_world(n, 0.10, deposited
      rewire_seed) for H2-H11), bit-asserted against exp243's records:
      sha256(|A| as float64) == base_sha256 12/12; the upper-triangle
      edge count == edges_base 12/12; the classify boundary count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity labeling_bfs_n(|A|)
      == labeling_bfs_n(A) 12/12; f_max recomputed == f_max_base
      12/12; the bases NON-NEGATIVE asserted per host. The two
      deep-row targets rebuilt per exp256's build_rows deep
      construction (exp214's deep form VERBATIM): row_target_sha256
      == exp256's deposited instance records 72/72, and the base
      medium sha == exp243's base_sha256 == the deposited
      medium_sha256 72/72. exp256's 72 rows with the substituted
      structure 36/36 + worst == max 36/36. THE EXP282 RE-READ: the
      72 row records present with trace_sha256 + walk_end_rms +
      err_deposited + walk_steps; exp282's deposited err_deposited ==
      exp256's deposited substituted err 72/72 (the two deposits'
      chain anchor); exp282's deposited branch == TRAJECTORY-CARRIED
      asserted (the pre-registered context); exp282's host_table
      walk_end_rms_mean present for the 12 hosts. THE S0 ANCHOR (the
      budget-8 half of the fresh battery): the re-run's final errs at
      budget 8 reproduce exp256's DEPOSITED substituted errs BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags 72/72), AND exp282's walk_end_rms reproduces BIT-EXACT at
      budget 8 (the fresh walk_end_rms(8) == exp282's deposited
      walk_end_rms 72/72; the fresh trace sha256(8) == exp282's
      deposited trace_sha256 72/72 — the SAME walk exp282 deposited;
      the fresh per-host end_RMS(8) means == exp282's deposited
      host_table means 12/12). The carries: the mia carry bit-exact
      12/12 (exp273's field table == exp243's own class records) + the
      premium carry bit-exact 12/12 (exp272 == exp273's field-table
      carry). THE PROVENANCE CHAINS sha-verified against the current
      file bytes — exp243 (4) + exp256 (3) + exp272 (4) + exp273 (5) +
      exp282 (4) = 20 records. The source deposits READ-ONLY:
      sha-recorded BEFORE any read, byte-unchanged after the work
      (5 deposits: exp243, exp256, exp272, exp273, exp282).
  G2  THE LADDER (pre-named, per-row dose integrity, all 72 rows x 3
      budgets = 216 decodes per pass): the ladder (4, 8, 16) fixed at
      pre-registration; 8 == exp142's STEPS_PER_CELL asserted (the
      production default — 4 halves the budget, 16 doubles it); the
      replica's one disclosed parameterization: the per-cell loop
      bound from the budget argument (at 8 the landed replica's code
      path — anchored bit-exact in G1); per row: walk_steps IDENTICAL
      across the three budgets (the visit order untouched — the dose
      scales the steps per cell, never the order) + the delivered dose
      budget * walk_steps recorded (the {4x, 8x, 16x} ladder per
      cell); per row per budget: the A3 state convention
      (round(err_exact, 2) == the reported err; asserted fail=STOP);
      the trace finite + trace[-1] > 0; the trace length ==
      walk_steps; the convergence point exists (TA3, exp282's assert
      form); the settle gap recorded (audit-only); the S* read lock
      count == 216 (the lock log asserted); the per-host denominators
      mean_end_RMS(8) > 0 asserted 12/12 and the ratios r4/r16
      computed 12/12.
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): (a) THE
      EXP282 ANCHOR AT THE DEFAULT — the fresh per-host end_RMS(8)
      means regressed against mia_prod_err and the one-zone premium
      under the exp274/exp275/exp282 conventions VERBATIM must
      reproduce exp282's deposited rhos BIT-EXACT
      (+0.8826151316282213 against mia_prod_err, +0.8807017543859651
      against the premium) — the default-budget carrier reproduced,
      not re-fit; a drift REFUTEs. (b) THE BRANCH on the pre-named
      bars — INV_BAND 0.10, INV_MIN_HOSTS 10, SEP_MARGIN 0.10:
      BUDGET-INVARIANT iff N_inv >= 10 (both ratios within 1.0 +/- 0.1
      on >= 10/12 hosts — the premium is the walk's fixed point);
      else BUDGET-ARTIFACT iff the outliers' ratios separate from the
      cluster's by > 0.10 on r4 or r16 (either direction — the premium
      is a BUDGET artifact); else MIXED (named honestly). Audit-only,
      never gating: the budget-4 and budget-16 carrier regressions
      against both targets (does the dose change the carrier's
      strength); the full 12-host orderings by r4 and by r16 with the
      outliers' positions; the outlier-vs-cluster ratio margins; the
      per-host end-RMS means at all three budgets; the delivered-dose
      face.
  G4  THE DISCIPLINE: deterministic — the full payload computed TWICE
      (the default two-pass in-process form, or the pre-named
      checkpoint-split per budget + merge with each budget computed
      twice as separate processes; the two passes' payloads
      BIT-IDENTICAL per budget, asserted at the merge/assembly); no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; the source deposits byte-unchanged;
      NEURAL_SPEC_MIN == -60.0 asserted at exit (exp218's disclosed
      exp169-import discipline — the whole reader chain imported
      FIRST, the floor restored after; the -35.0 reader-line pin
      disclosed).

THE BRANCHES (pre-named): BUDGET-INVARIANT / BUDGET-ARTIFACT / MIXED.

RUN: the deterministic sha-asserted rebuild (seconds) + 216 decodes per
full pass (3 budgets x 72 rows) ~ 4-6 min foreground per full pass,
far under the 570 s cap per invocation. THE PRE-NAMED CHECKPOINT-SPLIT
PER BUDGET + MERGE (the expected form): EXP286_MODE=budget4|budget8|
budget16 computes and caches ONE budget's 72-row payload per
invocation (each budget computed TWICE as separate processes — the
cross-process form doubles as the byte-identity check, exp284's
precedent; the checkpoint holds at most two payloads per budget);
EXP286_MODE=merge compares the two cached payloads PER BUDGET
BIT-EXACT, assembles, evaluates the gates once, writes the deposit —
the merge NEVER re-decodes — and removes the caches. THE TWO-PASS
IN-PROCESS ALTERNATIVE (no env): the full 3-budget battery computed
twice in one invocation (under the 570 s cap per the probe). Both
forms evaluate the SAME gates and assert the same bit-identities.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp286_endpoint_dose.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once,
    #      pre-registration commit 12b87b2) ================================
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
    #      is the 12b87b2 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "fa870b9558671c13c6a670a8445171114a0bf83b45c562158754a344476dfb33")
    EXPECTED_HEADER_SHA256 = (
        "9384a5869b60ae88adb3b490ab1e666384a3bd6c625cc9f00daa906de14223a5")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 12b87b2"
    assert header_ok, "header drifted from 12b87b2"

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
    #      THE LADDER — the pre-named dose axis) ---------------------------
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
    # THE LADDER (pre-named at 12b87b2): {4, 8, 16} — 4 halves the
    # production budget, 8 IS the production default, 16 doubles it.
    LADDER = (4, 8, 16)
    PROD_BUDGET = 8
    assert LADDER == (4, 8, 16), "the pre-named ladder drifted"
    assert PROD_BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    # THE BRANCH BARS (pre-named at 12b87b2, numeric, never fit)
    INV_BAND = 0.10
    INV_MIN_HOSTS = 10
    SEP_MARGIN = 0.10
    DEP282_RHO_MIA = 0.8826151316282213
    DEP282_RHO_PREM = 0.8807017543859651

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
    #      exp284's/exp285's rebuild form; the dose rows themselves
    #      carry NO classify/decompose/mask work) --------------------------
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

    # ---- THE TRACED REPLICA: exp282's/exp284's/exp285's
    #      _execute_signed_traced REUSED VERBATIM (landed at 8ca252e —
    #      exp142's walk byte-similar + exactly the disclosed recording
    #      additions: (a) the per-step RMS read after each commit (a
    #      pure numpy read of the live V vs the target — draws NOTHING
    #      from the RNG stream); (b) the trace + the walk commit count
    #      attached to the returned dict; (c) the final state always
    #      carried (exp243's A3 return_state semantics built in); (d) a
    #      no-op `order = []` initialization so the step count is
    #      well-defined on the empty-region branch (never taken on
    #      these rows); (e) the floor constant read via the exp142
    #      module attribute) with ONE DISCLOSED PARAMETERIZATION: the
    #      per-cell loop bound is read from the explicit `budget`
    #      argument instead of the module constant STEPS_PER_CELL —
    #      at budget 8 == exp142's STEPS_PER_CELL the code path IS the
    #      landed replica's, anchored BIT-EXACT against exp282's
    #      deposited walks (G1). The RNG stream, dt, canon, walk order,
    #      commits: UNTOUCHED. exp142 itself is NOT modified. --------
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
            for _ in range(budget):                  # THE DISCLOSED
                c.step(dt)                           # PARAMETERIZATION:
                                                     # the loop bound is
                                                     # the budget argument
                                                     # (at 8 the landed
                                                     # replica's code path)
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

    # ---- one budgeted dose-row decode (the budget-level read — NO
    #      classify/decompose/mask work; the S0 anchors at budget 8
    #      asserted fail=STOP) --------------------------------------------
    def _decode_row_budget(host, row_key, spec, med, seed, fmax,
                           dep_rec, rec282, budget):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, budget)
        err = float(out["err_vs_target"])
        assert np.isfinite(err), f"{host} {row_key} s{seed}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, f"{host} {row_key} s{seed} b{budget}: A3 state-convention drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        trace_len_ok = bool(len(trace) == steps and steps >= 1)
        assert trace_len_ok, \
            f"{host} {row_key} s{seed} b{budget}: trace {len(trace)} != walk steps {steps}"
        all_finite = bool(all(np.isfinite(trace)))
        assert all_finite, \
            f"{host} {row_key} s{seed} b{budget}: non-finite trace entry"
        final = trace[-1]
        final_positive = bool(final > 0.0)
        assert final_positive, \
            f"{host} {row_key} s{seed} b{budget}: final RMS == 0"
        # TA3 — the convergence point (existence; exp282's assert form)
        thresh = 2.0 * final
        conv = None
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            f"{host} {row_key} s{seed} b{budget}: the convergence point does not exist"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)
        delivered = int(budget * steps)
        rec = {"budget": int(budget), "host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "err": err,
               "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "delivered_steps": delivered}
        assert rec["delivered_steps"] == budget * steps, \
            f"{host} {row_key} s{seed} b{budget}: the delivered dose drifted"
        if budget == PROD_BUDGET:
            # THE S0 ANCHOR (G1, fail=STOP): the budget-8 re-run IS the
            # landed machinery — exp256's deposited errs + exp282's
            # deposited walks must reproduce BIT-EXACT
            s0_err_ok = bool(err == dep_rec["err"])
            s0_ver_ok = bool(rec["verified"] == dep_rec["verified"])
            assert s0_err_ok, \
                (f"{host} {row_key} s{seed}: the fresh budget-8 err {err} "
                 f"drifted from exp256's deposited {dep_rec['err']} — "
                 "S0 REFUTED")
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
                 "one")
            ee_ok = bool(err_exact == float(rec282["err_exact"]))
            assert ee_ok, \
                (f"{host} {row_key} s{seed}: the fresh err_exact drifted from "
                 "exp282's deposited err_exact")
            rec.update({"s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
                        "walk_end_282_ok": we_ok, "trace_sha_282_ok": ts_ok,
                        "err_exact_282_ok": ee_ok})
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

    # ---- THE COMPUTATION (ONE budget invocation: the sha-asserted
    #      rebuild + the fresh 72-row battery AT THAT BUDGET; the
    #      integrity section is a pure function of the deposits + the
    #      module bytes and is asserted identical across all
    #      invocations at assembly) ---------------------------------------
    def _compute_budget(budget):
        assert budget in LADDER, f"budget {budget} off the pre-named ladder"
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (exp269's/exp280's/exp284's/exp285's
        #      form, every rebuild bit-asserted against exp243's OWN
        #      records) ----------------------------------------------------
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

        # ---- THE FRESH DOSE BATTERY: the 72 substituted rows decoded
        #      AT THIS BUDGET (the S0 anchors at budget 8, fail=STOP) --
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec282 = r282[(k, s, rk)] if budget == PROD_BUDGET \
                        else None
                    rec = _decode_row_budget(
                        k, rk, ctx["deep"][inst]["spec"], med, s,
                        ctx["fmax"], d, rec282, budget)
                    rows_out.append(rec)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] b{budget} 6 rows | errs "
                  f"{[r['err'] for r in hs]} | end_rms "
                  f"{[round(r['walk_end_rms'], 4) for r in hs]}",
                  flush=True)
        assert len(rows_out) == 72, \
            f"the b{budget} battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads at b{budget}"
        return {"budget": int(budget), "rows": rows_out,
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

    # ---- THE ASSEMBLY (a pure function of the three per-budget
    #      payloads — no re-decodes; the merge path and the in-process
    #      path share it verbatim) ----------------------------------------
    def _assemble(payloads):
        for b in LADDER:
            assert payloads[b]["budget"] == b, "the payload budget drifted"
            assert payloads[b]["lock_reads"] == 72, \
                f"the b{b} lock count drifted"
        ints = [payloads[b]["integrity"] for b in LADDER]
        for b, sec in zip(LADDER[1:], ints[1:]):
            assert sec == ints[0], \
                f"the integrity section drifted across budgets (b{b})"
        ro_before_a = payloads[LADDER[0]]["ro_before"]
        for b in LADDER[1:]:
            assert payloads[b]["ro_before"] == ro_before_a, \
                f"ro_before drifted across budgets (b{b})"
        integrity = ints[0]
        counts = integrity["counts"]
        means282 = integrity["exp282_reread"][
            "host_table_walk_end_rms_means"]
        mia = integrity["targets"]["mia_prod_err"]["values"]
        prem = integrity["targets"]["one_zone_premium"]["values"]

        # ---- the row merge (72 rows x the three budget records) ------
        by_key = {}
        for b in LADDER:
            for r in payloads[b]["rows"]:
                key = (r["host"], r["seed"], r["row_key"])
                by_key.setdefault(key, {})[b] = r
        assert len(by_key) == 72, \
            f"the row merge produced {len(by_key)} keys != 72"
        rows = []
        n_a3 = 0
        n_trace_len = 0
        n_delivered = 0
        n_steps_equal = 0
        max_settle = 0.0
        steps_min = 10 ** 9
        steps_max = 0
        for h in hosts:
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    parts = by_key[(h, s, rk)]
                    assert set(parts.keys()) == set(LADDER), \
                        f"{h} {rk} s{s}: the budget coverage drifted"
                    bl = [parts[b] for b in LADDER]   # ordered 4, 8, 16
                    stepset = {p["walk_steps"] for p in bl}
                    steps_eq = bool(len(stepset) == 1)
                    assert steps_eq, \
                        f"{h} {rk} s{s}: walk_steps drifted across budgets"
                    for p in bl:
                        dl_ok = bool(p["delivered_steps"]
                                     == p["budget"] * p["walk_steps"])
                        assert dl_ok, \
                            f"{h} {rk} s{s}: the delivered dose drifted"
                        n_a3 += int(p["a3_ok"])
                        n_trace_len += int(p["trace_len"]
                                           == p["walk_steps"])
                        n_delivered += int(dl_ok)
                        max_settle = max(max_settle,
                                         float(p["settle_gap_abs"]))
                    steps_i = bl[0]["walk_steps"]
                    steps_min = min(steps_min, steps_i)
                    steps_max = max(steps_max, steps_i)
                    n_steps_equal += int(steps_eq)
                    rows.append({
                        "host": h, "seed": s, "instance": inst,
                        "row_key": rk, "pert": P3, "medium": "base",
                        "walk_steps": steps_i,
                        "steps_equal_across_budgets": steps_eq,
                        "delivered_steps_ladder":
                            [p["delivered_steps"] for p in bl],
                        "budgets": bl})
        assert len(rows) == 72, \
            f"the assembled battery produced {len(rows)} rows != 72"

        # ---- THE PER-HOST TABLE + THE BUDGET SENSITIVITY RATIOS ------
        host_table = []
        n_denoms_ok = 0
        n_ratios_ok = 0
        for h in hosts:
            hs = [r for r in rows if r["host"] == h]
            assert len(hs) == 6, f"{h}: the 6 rows drifted"
            means = {}
            for b in LADDER:
                vals = [next(p["walk_end_rms"] for p in r["budgets"]
                             if p["budget"] == b) for r in hs]
                means[b] = float(np.mean(vals))
            mean8 = means[PROD_BUDGET]
            denom_ok = bool(mean8 > 0.0)
            assert denom_ok, f"{h}: the budget-8 mean denominator <= 0"
            n_denoms_ok += int(denom_ok)
            ratio4 = means[4] / mean8
            ratio16 = means[16] / mean8
            in_b4 = bool(abs(ratio4 - 1.0) <= INV_BAND)
            in_b16 = bool(abs(ratio16 - 1.0) <= INV_BAND)
            in_band = bool(in_b4 and in_b16)
            n_ratios_ok += int(np.isfinite(ratio4)
                               and np.isfinite(ratio16))
            mean8_dep = means282[h]
            mean8_ok = bool(mean8 == mean8_dep)
            assert mean8_ok, \
                (f"{h}: the fresh per-host end_RMS(8) mean {mean8!r} "
                 f"drifted from exp282's deposited {mean8_dep!r}")
            delivered_means = {}
            for b in LADDER:
                dvals = [next(p["delivered_steps"] for p in r["budgets"]
                              if p["budget"] == b) for r in hs]
                delivered_means[str(b)] = float(np.mean(dvals))
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "mean_end_rms": {str(b): means[b] for b in LADDER},
                "ratio_budget4": ratio4, "ratio_budget16": ratio16,
                "in_band_budget4": in_b4, "in_band_budget16": in_b16,
                "in_band": in_band,
                "mean8_equals_exp282_host_table": mean8_ok,
                "delivered_steps_mean": delivered_means,
                "err_exact_mean_budget8": float(np.mean(
                    [next(p["err_exact"] for p in r["budgets"]
                          if p["budget"] == PROD_BUDGET) for r in hs])),
                "settle_gap_mean_budget8": float(np.mean(
                    [next(p["settle_gap_abs"] for p in r["budgets"]
                          if p["budget"] == PROD_BUDGET) for r in hs]))})
        assert n_denoms_ok == 12 and n_ratios_ok == 12, \
            "the ratio computation drifted"

        # ---- THE REGRESSIONS (the exp274/exp275/exp282 conventions
        #      VERBATIM: Spearman = Pearson on the tied-average ranks;
        #      the single-predictor OLS rank R2; the ties census per
        #      vector; the budget-8 pair = THE EXP282 ANCHOR at the
        #      default (asserted bit-exact vs the deposited rhos); the
        #      budget-4/16 pairs AUDIT-ONLY) ----------------------------
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
        for b in LADDER:
            xs = [next(row for row in host_table
                       if row["host"] == hh)["mean_end_rms"][str(b)]
                  for hh in hosts]
            for tk, tvals in TARGET_COLS.items():
                rho = _spearman(xs, tvals)
                rk_resp = rankdata(np.asarray(xs, dtype=float))
                r2_single = _r2([tvals], rk_resp)
                r2_all = _r2([rankdata(np.asarray(tvals, dtype=float))],
                             rk_resp)
                regressions[f"end_rms{b}~{tk}"] = {
                    "carrier": f"end_rms_budget{b}", "target": tk,
                    "rho": rho, "rho_abs": abs(rho),
                    "rank_R2_single": r2_single,
                    "rank_R2_all_ranks": r2_all,
                    "all_ranks_minus_rho2": r2_all - rho * rho,
                    "ties_carrier": _ties_census(xs),
                    "ties_target": _ties_census(tvals),
                    "gating": False,
                    "role": (
                        "the default-budget carrier — THE EXP282 ANCHOR "
                        "at the default (asserted bit-exact vs exp282's "
                        "deposited rho)"
                        if b == PROD_BUDGET else
                        "audit-only — the dose face (never gating)")}

        # ---- G3(a): THE EXP282 ANCHOR AT THE DEFAULT (bit-exact) -----
        rho8_mia = regressions["end_rms8~mia_prod_err"]["rho"]
        rho8_prem = regressions["end_rms8~one_zone_premium"]["rho"]
        dep_rho8_mia = float(
            dep282["regressions"]["walk_end_rms~mia_prod_err"]["rho"])
        dep_rho8_prem = float(
            dep282["regressions"]["walk_end_rms~one_zone_premium"]["rho"])
        anchor_mia_ok = bool(rho8_mia == dep_rho8_mia)
        anchor_prem_ok = bool(rho8_prem == dep_rho8_prem)
        assert anchor_mia_ok, \
            (f"the fresh end_RMS(8)~mia rho {rho8_mia!r} drifted from "
             f"exp282's deposited {dep_rho8_mia!r} — the exp282 anchor "
             "at the default REFUTED")
        assert anchor_prem_ok, \
            (f"the fresh end_RMS(8)~premium rho {rho8_prem!r} drifted from "
             f"exp282's deposited {dep_rho8_prem!r} — the exp282 anchor "
             "at the default REFUTED")

        # ---- G3(b): THE BRANCH DISCRIMINANT (pre-named numeric bars) --
        n_inv = sum(1 for row in host_table if row["in_band"])
        r4_out = [row["ratio_budget4"] for row in host_table
                  if row["outlier"]]
        r4_clu = [row["ratio_budget4"] for row in host_table
                  if not row["outlier"]]
        r16_out = [row["ratio_budget16"] for row in host_table
                   if row["outlier"]]
        r16_clu = [row["ratio_budget16"] for row in host_table
                   if not row["outlier"]]
        seps = {
            "r4_above": min(r4_out) - max(r4_clu),
            "r4_below": min(r4_clu) - max(r4_out),
            "r16_above": min(r16_out) - max(r16_clu),
            "r16_below": min(r16_clu) - max(r16_out)}
        max_sep = max(seps.values())
        if n_inv >= INV_MIN_HOSTS:
            branch_local = "BUDGET-INVARIANT"
        elif max_sep > SEP_MARGIN:
            branch_local = "BUDGET-ARTIFACT"
        else:
            branch_local = "MIXED"
        branch_discriminant = {
            "bars": {"INV_BAND": INV_BAND, "INV_MIN_HOSTS": INV_MIN_HOSTS,
                     "SEP_MARGIN": SEP_MARGIN},
            "bars_pre_named_at": ("12b87b2 — fixed at pre-registration, "
                                  "never fit"),
            "n_invariant_hosts": n_inv,
            "per_host_in_band": {row["host"]: row["in_band"]
                                 for row in host_table},
            "outlier_ratios": {row["host"]: {
                "r4": row["ratio_budget4"],
                "r16": row["ratio_budget16"]}
                for row in host_table if row["outlier"]},
            "cluster_ratio_ranges": {
                "r4": [min(r4_clu), max(r4_clu)],
                "r16": [min(r16_clu), max(r16_clu)]},
            "separation_margins": seps,
            "max_separation_margin": max_sep,
            "ordering_by_r4": [
                {"host": row["host"], "r4": row["ratio_budget4"],
                 "outlier": row["outlier"]}
                for row in sorted(host_table,
                                  key=lambda r: r["ratio_budget4"])],
            "ordering_by_r16": [
                {"host": row["host"], "r16": row["ratio_budget16"],
                 "outlier": row["outlier"]}
                for row in sorted(host_table,
                                  key=lambda r: r["ratio_budget16"])],
            "exp282_anchor_at_default": {
                "fresh_rho_8_mia": rho8_mia,
                "fresh_rho_8_premium": rho8_prem,
                "deposited_rho_8_mia": dep_rho8_mia,
                "deposited_rho_8_premium": dep_rho8_prem,
                "bit_exact": bool(anchor_mia_ok and anchor_prem_ok)},
            "branch": branch_local}

        # ---- the S0 tallies (from the budget-8 rows) ------------------
        rows8 = payloads[PROD_BUDGET]["rows"]
        n_s0_err = sum(1 for r in rows8 if r["s0_err_ok"])
        n_s0_ver = sum(1 for r in rows8 if r["s0_verified_ok"])
        n_we282 = sum(1 for r in rows8 if r["walk_end_282_ok"])
        n_ts282 = sum(1 for r in rows8 if r["trace_sha_282_ok"])
        n_ee282 = sum(1 for r in rows8 if r["err_exact_282_ok"])
        n_mean282 = sum(1 for row in host_table
                        if row["mean8_equals_exp282_host_table"])

        g1 = dict(counts)
        g1.update({"n_s0_err_ok": n_s0_err, "n_s0_verified_ok": n_s0_ver,
                   "n_walk_end282_ok": n_we282, "n_trace282_ok": n_ts282,
                   "n_errexact282_ok": n_ee282, "n_mean282_ok": n_mean282})
        g2 = {"n_rows": len(rows), "n_budget_records": 3 * len(rows),
              "n_a3_ok": n_a3, "n_trace_len_ok": n_trace_len,
              "n_delivered_ok": n_delivered,
              "n_steps_equal_ok": n_steps_equal,
              "n_lock_reads": sum(payloads[b]["lock_reads"]
                                  for b in LADDER),
              "n_denominators_ok": n_denoms_ok, "n_ratios_ok": n_ratios_ok,
              "max_settle_gap": max_settle,
              "walk_steps_min": steps_min, "walk_steps_max": steps_max}
        g3 = {"anchor_mia_ok": anchor_mia_ok,
              "anchor_prem_ok": anchor_prem_ok,
              "n_invariant_hosts": n_inv, "branch": branch_local,
              "max_separation_margin": max_sep}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "integrity": integrity, "rows": rows,
                "host_table": host_table, "regressions": regressions,
                "branch": branch_local,
                "branch_discriminant": branch_discriminant,
                "g1": g1, "g2": g2, "g3": g3,
                "ro_before": ro_before_a}

    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    def _core_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the expected
    #      form is the CHECKPOINT-SPLIT PER BUDGET + MERGE — each budget
    #      computed TWICE as separate processes, the merge comparing the
    #      two cached payloads per budget BIT-EXACT and never
    #      re-decoding; the two-pass in-process form is the
    #      pre-named alternative) -----------------------------------------
    _MODE = os.environ.get("EXP286_MODE", "")
    _CK = {b: os.path.join(ROOT, "results",
                           f".exp286_budget{b}.checkpoint.json")
           for b in LADDER}

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

    if _MODE in ("budget4", "budget8", "budget16"):
        budget = int(_MODE.replace("budget", ""))
        assert budget in LADDER, f"mode {_MODE} off the pre-named ladder"
        payload = _compute_budget(budget)
        ck = _CK[budget]
        existing = []
        if os.path.exists(ck):
            with open(ck) as fh:
                existing = json.load(fh)
        assert isinstance(existing, list) and len(existing) < 2, \
            (f"{ck} already holds {len(existing)} payloads — the split "
             "form caches at most two (pass a + pass b)")
        existing.append(payload)
        with open(ck, "w") as fh:
            json.dump(existing, fh, sort_keys=True)
        print(f"  checkpointed {_MODE} ({len(existing)}/2 payloads, sha "
              f"{_payload_sha(payload)[:16]})")
        _exit_checks()
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR
        assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
            "floor drift at exit"
        return {"mode": _MODE, "payloads_cached": len(existing),
                "payload_sha256": _payload_sha(payload)}

    per_budget_shas = {}
    if _MODE == "merge":
        cached = {}
        for b in LADDER:
            with open(_CK[b]) as fh:
                cached[b] = json.load(fh)
            assert isinstance(cached[b], list) and len(cached[b]) == 2, \
                f"{_CK[b]} must hold exactly two payloads (pass a + pass b)"
        for b in LADDER:
            sa = _payload_sha(cached[b][0])
            sb = _payload_sha(cached[b][1])
            assert sa == sb, \
                (f"the two b{b} payloads diverged: {sa[:16]} vs {sb[:16]} "
                 "— the byte-identity check FAILED")
            per_budget_shas[str(b)] = {"pass_a": sa, "pass_b": sb,
                                       "bit_identical": True}
        core_a = _assemble({b: cached[b][0] for b in LADDER})
        core_b = _assemble({b: cached[b][1] for b in LADDER})
        sha_a, sha_b = _core_sha(core_a), _core_sha(core_b)
        deterministic = bool(sha_a == sha_b)
        assert deterministic, "the two passes' assembled cores diverged"
        core = core_a
        run_form = "checkpoint-split per budget + merge"
    else:
        print("=== exp286: THE ENDPOINT'S DOSE (the end-RMS carrier's own "
              "parameter — the walk's step budget) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 rows x the ladder "
              f"{list(LADDER)} = 216 decodes per pass, TWO passes (G4)")
        print(f"  the budget-8 half IS the production default "
              f"(STEPS_PER_CELL == {STEPS_PER_CELL}) — anchored bit-exact "
              f"vs exp256's deposited errs + exp282's deposited walks")

        def _run_all():
            payloads = {}
            for b in LADDER:
                print(f"  --- pass: budget {b} ---", flush=True)
                payloads[b] = _compute_budget(b)
            return payloads

        pa = _run_all()
        pb = _run_all()
        for b in LADDER:
            sa = _payload_sha(pa[b])
            sb = _payload_sha(pb[b])
            assert sa == sb, \
                (f"the two b{b} payloads diverged: {sa[:16]} vs {sb[:16]} "
                 "— the byte-identity check FAILED")
            per_budget_shas[str(b)] = {"pass_a": sa, "pass_b": sb,
                                       "bit_identical": True}
        core_a = _assemble({b: pa[b] for b in LADDER})
        core_b = _assemble({b: pb[b] for b in LADDER})
        sha_a, sha_b = _core_sha(core_a), _core_sha(core_b)
        deterministic = bool(sha_a == sha_b)
        assert deterministic, "the two passes' assembled cores diverged"
        core = core_a
        run_form = "in-process two-pass"

    # ---- the gate assembly (evaluated exactly once, on pass a) ----------
    g1, g2, g3 = core["g1"], core["g2"], core["g3"]
    integrity = core["integrity"]
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(core["ro_before"].values()))
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
    g2_pass = bool(g2["n_rows"] == 72 and g2["n_budget_records"] == 216
                   and g2["n_a3_ok"] == 216 and g2["n_trace_len_ok"] == 216
                   and g2["n_delivered_ok"] == 216
                   and g2["n_steps_equal_ok"] == 72
                   and g2["n_lock_reads"] == 216
                   and g2["n_denominators_ok"] == 12
                   and g2["n_ratios_ok"] == 12)
    g3_pass = bool(g3["anchor_mia_ok"] and g3["anchor_prem_ok"])

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
    n_inv = bd["n_invariant_hosts"]
    out_r = bd["outlier_ratios"]
    clu_r4 = bd["cluster_ratio_ranges"]["r4"]
    clu_r16 = bd["cluster_ratio_ranges"]["r16"]

    def _g(x):
        return f"{x:+.4f}"

    if branch == "BUDGET-INVARIANT":
        branch_text = (
            f"the end-RMS carrier is BUDGET-INVARIANT at the house band — "
            f"both ratios within 1.0 +/- 0.1 on {n_inv}/12 hosts; the "
            "premium is the walk's FIXED POINT (the endpoint magnitude "
            "does not track the step budget)")
    elif branch == "BUDGET-ARTIFACT":
        branch_text = (
            f"the outliers' budget response SEPARATES from the cluster's "
            f"(max margin {bd['max_separation_margin']:+.4f} > the "
            f"pre-named {SEP_MARGIN}) — the premium is a BUDGET ARTIFACT "
            "(the excess endpoint magnitude is produced by the production "
            "dose, not carried by the host structure)")
    else:
        branch_text = (
            f"MIXED — the invariance count {n_inv}/12 below the pre-named "
            f"{INV_MIN_HOSTS} with no outlier/cluster separation beyond "
            f"{SEP_MARGIN} (max margin "
            f"{bd['max_separation_margin']:+.4f}; named honestly)")

    verdict_body = (
        f"{branch} — {branch_text}"
        f" (N_inv {n_inv}/12 | the outliers' ratios H3 r4 "
        f"{out_r['H3']['r4']:.4f} r16 {out_r['H3']['r16']:.4f} / H5 r4 "
        f"{out_r['H5']['r4']:.4f} r16 {out_r['H5']['r16']:.4f} vs the "
        f"cluster r4 [{clu_r4[0]:.4f}, {clu_r4[1]:.4f}] r16 "
        f"[{clu_r16[0]:.4f}, {clu_r16[1]:.4f}]) | THE EXP282 ANCHOR AT "
        f"THE DEFAULT reproduced bit-exact: rho(end_RMS 8)~mia "
        f"{bd['exp282_anchor_at_default']['fresh_rho_8_mia']:+.16f} / "
        f"rho(8)~premium "
        f"{bd['exp282_anchor_at_default']['fresh_rho_8_premium']:+.16f} "
        f"(== exp282's deposited +0.8826151316282213 / "
        f"+0.8807017543859651) | THE DOSE FACE (audit-only): "
        f"rho(4)~mia {regressions['end_rms4~mia_prod_err']['rho']:+.4f} / "
        f"rho(16)~mia {regressions['end_rms16~mia_prod_err']['rho']:+.4f}; "
        f"rho(4)~premium "
        f"{regressions['end_rms4~one_zone_premium']['rho']:+.4f} / "
        f"rho(16)~premium "
        f"{regressions['end_rms16~one_zone_premium']['rho']:+.4f} | THE "
        f"LADDER: walk_steps identical across budgets per row "
        f"({g2['n_steps_equal_ok']}/72, walk_steps within "
        f"[{g2['walk_steps_min']}, {g2['walk_steps_max']}] — the dose "
        f"scales the steps per cell, never the visit order), the "
        f"delivered dose budget*walk_steps recorded "
        f"({g2['n_delivered_ok']}/216; the {{4x, 8x, 16x}} ladder per "
        f"cell) | THE S0 ANCHOR: the budget-8 re-run reproduced "
        f"exp256's deposited substituted errs bit-exact "
        f"({g1['n_s0_err_ok']}/72, the verified flags "
        f"{g1['n_s0_verified_ok']}/72) AND exp282's walk_end_rms "
        f"bit-exact at budget 8 (walk_end_rms {g1['n_walk_end282_ok']}/72, "
        f"trace sha256 {g1['n_trace282_ok']}/72 — the SAME walk exp282 "
        f"deposited, err_exact {g1['n_errexact282_ok']}/72, the per-host "
        f"means {g1['n_mean282_ok']}/12; the settle gap max "
        f"{g2['max_settle_gap']:.4f} mV, audit-only) | 12 hosts, a "
        f"deterministic sha-asserted rebuild (graph_path for H0/H1, "
        f"small_world at the deposited rewire seeds — exp269's/exp280's "
        f"form), the provenance chains sha-verified 20/20, 5 deposits "
        f"READ-ONLY byte-unchanged, two-pass bit-identical "
        f"({run_form}), floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp286_endpoint_dose",
        "claim": (
            "THE ENDPOINT'S DOSE (batch 44, pre-registration commit "
            "12b87b2): the end-RMS carrier's OWN parameter — the walk's "
            "step budget. Batch 43 closed the grain screen at three "
            "levels (the exp208-label classes, the boundary's own share, "
            "the ring around it), all exposure-blind at the 0.5 SIGNED "
            "bar: the carrier's exposure stays in the walk's ENDPOINT "
            "MAGNITUDE (exp282's walk_end_rms, signed Spearman "
            "+0.8826151316282213 against mia_prod_err, "
            "+0.8807017543859651 against exp272's one-zone premium "
            "means). exp286 asks whether that endpoint magnitude is a "
            "FIXED POINT of the walk — invariant to the budget — or an "
            "artifact of the production dose (exp142's STEPS_PER_CELL "
            "== 8). The traced replica (exp284/exp285's landed form, one "
            "disclosed parameterization: the per-cell loop bound from an "
            "explicit budget argument; at 8 the landed code path, "
            "anchored bit-exact vs exp282's deposited walks) re-runs the "
            "substituted rows (12 hosts x 3 seeds x the two deep "
            "instances at n=400 — exp256's battery) at the pre-named "
            "ladder {4, 8, 16} — 4 halves the budget, 16 doubles it; the "
            "walk ORDER untouched (walk_steps identical across budgets "
            "asserted; the delivered dose = budget * walk_steps). "
            "Pre-named reads: (1) the BUDGET SENSITIVITY — the ratios "
            "r4 = mean_end_RMS(4)/mean_end_RMS(8) and r16 = "
            "mean_end_RMS(16)/mean_end_RMS(8) per host (if ~1.0 the "
            "endpoint is budget-invariant — the walk's fixed point; the "
            "outliers' ratios vs the cluster's decide the artifact "
            "question); (2) the exp282 anchor at the default — the "
            "end_RMS(8) carrier's regressions vs mia + the premium "
            "ASSERTED BIT-EXACT == exp282's deposited rhos; (3) the "
            "branch BUDGET-INVARIANT (N_inv >= 10/12 hosts with both "
            "ratios within 1.0 +/- 0.1 — the premium is the walk's fixed "
            "point) / BUDGET-ARTIFACT (the outliers' ratios separate "
            "from the cluster's by > 0.10 on r4 or r16 — the premium is "
            "a BUDGET artifact) / MIXED, bars INV_BAND 0.10 / "
            "INV_MIN_HOSTS 10 / SEP_MARGIN 0.10 fixed at "
            "pre-registration, never fit"),
        "method": {
            "ladder": (
                "budgets (4, 8, 16) fixed at pre-registration; 8 == "
                "exp142's STEPS_PER_CELL == the production default "
                "(asserted); the dose is delivered as integration steps "
                "per committed cell; the walk order untouched — "
                "walk_steps identical across the three budgets asserted "
                "per row; the delivered dose per row = budget * "
                "walk_steps (the {4x, 8x, 16x} ladder per cell)"),
            "replica": (
                "exp282's/exp284's/exp285's _execute_signed_traced "
                "REUSED VERBATIM (landed 8ca252e: exp142's walk "
                "byte-similar + the disclosed recording additions — the "
                "per-step RMS read, the trace + commit count, the "
                "always-carried final state, the no-op order init, the "
                "floor via the exp142 module attribute) with ONE "
                "DISCLOSED PARAMETERIZATION: the per-cell loop bound "
                "read from the explicit budget argument instead of the "
                "module constant; at budget 8 the code path IS the "
                "landed replica's and is anchored BIT-EXACT against "
                "exp282's deposited walks (G1). The RNG stream, dt, "
                "canon, walk order, commits UNTOUCHED; exp142 NOT "
                "modified"),
            "end_rms": (
                "the walk's trace[-1] — the PRE-settle carrier exp282 "
                "named; the POST-settle err_exact + the settle gap "
                "recorded audit-only; the A3 state convention "
                "(round(err_exact, 2) == the reported err) asserted "
                "fail=STOP at every budget"),
            "ratios": (
                "per host over the host's 6 substituted rows: r4 = "
                "mean_end_RMS(4) / mean_end_RMS(8), r16 = "
                "mean_end_RMS(16) / mean_end_RMS(8); the denominators "
                "asserted > 0; the budget-8 means asserted == exp282's "
                "deposited host_table means bit-exact 12/12"),
            "branch_rule": (
                "BUDGET-INVARIANT iff N_inv >= 10 where N_inv = #{hosts "
                ": |r4 - 1| <= 0.10 AND |r16 - 1| <= 0.10} — the premium "
                "is the walk's fixed point; else BUDGET-ARTIFACT iff the "
                "outliers' ratios separate from the cluster's: "
                "min(r|outliers) - max(r|cluster) > 0.10 or min(r|cluster)"
                " - max(r|outliers) > 0.10 on r4 or r16 — the premium is "
                "a BUDGET artifact; else MIXED (named honestly). Bars "
                "INV_BAND 0.10 / INV_MIN_HOSTS 10 / SEP_MARGIN 0.10, "
                "fixed at pre-registration, never fit"),
            "regressions": (
                "the exp274/exp275/exp282 conventions VERBATIM: Spearman "
                "= Pearson on the tied-average ranks (scipy rankdata); "
                "the single-predictor OLS rank R2 (the response as its "
                "tied-average ranks, the target as the numeric design "
                "column) + the all-ranks variant AUDIT-ONLY; the ties "
                "census per vector; the 12-slot frame with the H0==H1 "
                "echo carried; the budget-8 pair is THE EXP282 ANCHOR "
                "(asserted bit-exact vs exp282's deposited rhos); the "
                "budget-4/16 pairs recorded audit-only (never gating); "
                "nothing gates on a rho in this module — the branch is "
                "the ratio discriminant"),
            "scope": (
                "NO classify/decompose/mask work on the dose rows — the "
                "grain screen is closed (exp277/exp284/exp285); the dose "
                "question is budget-level; exp208's classify appears "
                "ONLY in the rebuild's boundary-count integrity check "
                "(the landed rebuild form)")},
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
                "the anchor deposit — the 72 per-row walk_end_rms + "
                "trace shas (the bit-exact same-walk anchor at budget "
                "8) + the deposited TRAJECTORY-CARRIED branch + the "
                "host_table means + the deposited default-carrier "
                "rhos (the G3 anchor)"))},
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
            "decodes_per_pass": 216,
            "per_budget_payload_sha256": per_budget_shas,
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
                "the budget-8 re-run's final errs reproduce exp256's "
                "deposited substituted errs bit-exact (72/72, the "
                "machinery's native 2-dp convention) and exp282's "
                "walk_end_rms reproduces bit-exact at budget 8 "
                "(walk_end_rms + trace sha256 72/72 — the SAME walk "
                "exp282 deposited — plus err_exact 72/72 and the "
                "per-host means 12/12; asserted fail=STOP at decode)")},
        "G2_ladder_pre_named": {
            "pass": g2_pass,
            "counts": g2,
            "ladder": ("(4, 8, 16) fixed at pre-registration; 8 == "
                       "exp142's STEPS_PER_CELL == the production "
                       "default (4 halves the budget, 16 doubles it); "
                       "walk_steps identical across budgets per row "
                       "(the visit order untouched — the dose scales "
                       "the steps per cell, never the order); the "
                       "delivered dose budget * walk_steps; per row "
                       "per budget the A3 state convention + the trace "
                       "finite + trace[-1] > 0 + the trace length == "
                       "walk_steps + the convergence point existence "
                       "asserted fail=STOP at decode; the trace "
                       "sha256 recorded at every budget (asserted == "
                       "exp282's at budget 8; the 4/16 shas recorded "
                       "for any future re-verification)")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "anchor": ("the fresh per-host end_RMS(8) means regressed "
                       "against mia_prod_err and the one-zone premium "
                       "under the exp274/exp275/exp282 conventions "
                       "VERBATIM reproduce exp282's deposited rhos "
                       "BIT-EXACT (+0.8826151316282213 / "
                       "+0.8807017543859651) — the default-budget "
                       "carrier reproduced, not re-fit; a drift "
                       "REFUTEs"),
            "bars": ("BUDGET-INVARIANT iff N_inv >= 10 (both ratios "
                     "within 1.0 +/- 0.1 on >= 10/12 hosts — the "
                     "premium is the walk's fixed point); else "
                     "BUDGET-ARTIFACT iff the outliers' ratios "
                     "separate from the cluster's by > 0.10 on r4 or "
                     "r16 (either direction — the premium is a BUDGET "
                     "artifact); else MIXED. Audit-only, never "
                     "gating: the budget-4/16 carrier regressions; "
                     "the orderings by r4/r16; the outlier margins; "
                     "the per-host means at all three budgets; the "
                     "delivered-dose face"),
            "resolved": {"branch": branch, "n_invariant_hosts": n_inv,
                         "max_separation_margin": bd["max_separation_margin"]}},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_s0_anchor_integrity", "G2_ladder_pre_named",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    gates["G4_discipline"] = {
        "pass": bool(deterministic and no_wall_clock and docstring_ok
                     and header_ok and ro_unchanged),
        "two_pass_bit_identical": deterministic,
        "run_form": run_form,
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_12b87b2": docstring_ok,
        "header_byte_unchanged_vs_12b87b2": header_ok,
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
          f"budget-8 errs == exp256's deposited substituted errs bit-exact "
          f"{g1['n_s0_err_ok']}/72 + the verified flags "
          f"{g1['n_s0_verified_ok']}/72 AND exp282's walk_end_rms "
          f"bit-exact at budget 8 (walk_end {g1['n_walk_end282_ok']}/72, "
          f"trace sha {g1['n_trace282_ok']}/72, err_exact "
          f"{g1['n_errexact282_ok']}/72, the per-host means "
          f"{g1['n_mean282_ok']}/12); the carries mia {g1['n_mia_carry']}"
          f"/12 + premium {g1['n_prem_carry']}/12; the provenance chains "
          f"{integrity['provenance_chains']['total_verified']}/20)")
    print(f"  G2 ladder (pre-named): "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"({g2['n_budget_records']}/216 decodes on the ladder "
          f"{list(LADDER)}; walk_steps identical across budgets per row "
          f"{g2['n_steps_equal_ok']}/72 (walk_steps within "
          f"[{g2['walk_steps_min']}, {g2['walk_steps_max']}]); the "
          f"delivered dose {g2['n_delivered_ok']}/216; the A3 convention "
          f"{g2['n_a3_ok']}/216; the trace lengths {g2['n_trace_len_ok']}"
          f"/216; the S* lock reads {g2['n_lock_reads']}/216; the "
          f"denominators {g2['n_denominators_ok']}/12; the ratios "
          f"{g2['n_ratios_ok']}/12; the settle gap max "
          f"{g2['max_settle_gap']:.4f} mV)")
    print("  the 12-host dose table (per-host means + ratios; H3/H5 the "
          "outliers):")
    for row in host_table:
        tag = " <== outlier" if row["outlier"] else ""
        m = row["mean_end_rms"]
        print(f"      {row['host']:4s} end_rms 4 {m['4']:.4f}  8 "
              f"{m['8']:.4f}  16 {m['16']:.4f}  r4 "
              f"{row['ratio_budget4']:.4f}{'*' if row['in_band_budget4'] else ' '} "
              f"r16 {row['ratio_budget16']:.4f}"
              f"{'*' if row['in_band_budget16'] else ' '}{tag}")
    print("  G3 branch — the regressions (the exp274/exp275/exp282 "
          "conventions; the budget-8 pair = the exp282 ANCHOR):")
    for k, v in regressions.items():
        print(f"      {k:28s} rho {v['rho']:+.4f}  ({v['role'][:41]})")
    print(f"      the branch bars: INV_BAND {INV_BAND} | INV_MIN_HOSTS "
          f"{INV_MIN_HOSTS} | SEP_MARGIN {SEP_MARGIN} | N_inv {n_inv}/12 "
          f"| max separation {bd['max_separation_margin']:+.4f}")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}, form {run_form}; "
          f"no wall-clock fields: {no_wall_clock}; 5 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged})")
    print(f"\n  BRANCH: {branch} | N_inv {n_inv}/12 | the outliers' "
          f"ratios H3 r4 {out_r['H3']['r4']:.4f} r16 "
          f"{out_r['H3']['r16']:.4f} / H5 r4 {out_r['H5']['r4']:.4f} r16 "
          f"{out_r['H5']['r16']:.4f} vs the cluster r4 "
          f"[{clu_r4[0]:.4f}, {clu_r4[1]:.4f}] r16 "
          f"[{clu_r16[0]:.4f}, {clu_r16[1]:.4f}]")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    # ---- the hard rules, re-asserted after the work ----------------------
    _exit_checks()
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    if _MODE == "merge":
        for b in LADDER:
            if os.path.exists(_CK[b]):
                os.remove(_CK[b])
        print("  the checkpoint caches removed after the merge")
    return deposit


if __name__ == "__main__":
    main()
