#!/usr/bin/env python3
"""exp284 — THE ENDPOINT COMPOSITION: THE END-RMS CARRIER DECOMPOSED BY
CELL CLASS AT THE WALK LEVEL (batch 42; batch-41's derived item, ledger
L261 — exp283's verdict put the exposure in WHERE THE WALK ENDS, not in
where it settles; this module opens that endpoint).

THE OPEN ITEM: exp282 landed TRAJECTORY-CARRIED — the walk's end RMS
(TA1 walk_end_rms, the per-step RMS-to-target curve's final value) is
the strongest carrier yet named (signed Spearman +0.8826 against
mia_prod_err, +0.8807 against exp272's one-zone premium means; the 0.5
SIGNED house bar). exp277 asked the same WHERE question at the DECODE
level — exp256's deposited per-row decompositions through exp208's
cell-class machinery — and found the decode-level break CLASS-BLIND
(branch NEITHER: the outliers' cb shares 0.1513/0.2265 vs the cluster
max 0.1767, both margins NEGATIVE). THE NEW SURFACE: the WALK level —
the end-RMS carrier's own per-cell composition. The question: does the
outlier hosts' end-RMS mass concentrate in CANON-BOUNDARY cells at the
walk level, in PAIR-JUNCTION cells, or is the walk-level break ALSO
class-blind (matching exp277)?

THE INSTRUMENT (pre-registered, zero-knob): the pure re-reads where
possible + THE MINIMAL FRESH STATE-CARRYING RE-RUN where the per-cell
end state is needed.

  THE PURE RE-READS (no new simulation): exp282's trajectory deposit —
  the 72 per-row traces + the three summaries + the 12-host means
  table; the carrier (walk_end_rms per row) carried BIT-EXACT.
  exp256's 72-row battery — the deposited substituted instance errs
  (the S0 anchor's targets), the row/instance shas, the row-level
  class_counts. exp272's per-host one-zone premium means + exp273's
  field table (the mia field + the premium carry). exp277's per-host
  decode-level shares (the walk-vs-decode face, audit-only).

  THE FRESH RE-RUN (the minimal form): exp282's _execute_signed_traced
  replica REUSED VERBATIM (landed at 8ca252e — exp142's walk
  byte-similar + exactly the disclosed recording additions: the
  per-step RMS read after each commit, the trace + step-count fields,
  the final state always carried; the RNG stream / dt / canon / walk
  order / commits untouched; exp142 NOT modified), called through
  exp256's _scoped_row_read_state form (the projection chain PN1/PN2 +
  TC1 + TC2 + the traced TC3), on the SAME 72 substituted rows
  (12 hosts x 3 seeds (1,2,3) x the two deep instances r-60i0/r-60i1
  at n=400 — exp256's battery, ONE FRESH RUN).

  THE PER-CELL END ERRORS: from the state-carrying read's final_state
  (the replica's disclosed addition (c)): e_i = V_i - T_i over the
  n=400 frame. THE END-RMS (the decomposition's object):
  err_exact = sqrt(mean(e^2)) — the A3-checked state convention.
  DISCLOSED (pre-body): exp282's walk_end_rms carrier is the PRE-settle
  trace[-1]; the final_state end state is POST-settle (exp142's fixed
  15.0 settle tail runs between the walk's last commit and the state
  return — a fixed part of the executor, not a knob); the trace stores
  scalars, not the frame, so the end state is the ONLY per-cell end
  record the landed machinery provides. The per-row settle gap
  |err_exact - walk_end_rms_carried| is recorded per row (audit-only;
  exp282's deposited rows put it at ~1e-3 mV — e.g. H3 s1 i0: 3.6759
  vs 3.6748).

  THE CLASSIFICATION (exp208's classify VERBATIM on the row target +
  medium): CANON-BOUNDARY (the cell sits on a canon-value boundary in
  the target — a ring neighbor's target value differs), PAIR-JUNCTION
  (endpoint of >= 2 chords in the medium's pair support |A_base| > 0),
  INTERIOR (neither); precedence the registered listing order (the
  boundary wins, then the junction). Applied per INSTANCE
  (classify(T_instance, A_host) — the two deep targets differ by the
  instance shift). THE MASK SEMANTICS (exp277's disclosure, carried):
  exp208's decompose reads the cls array — cls 1 = PAIR-JUNCTION (the
  junctions off the boundary ring), cls 0 = otherwise (the boundary
  ring + the interior ride the same mask; cls is never 2) — so the
  per-class CANON-BOUNDARY record is the NON-PAIR-JUNCTION complement
  of the squared error and the INTERIOR record is empty; the branch
  reads the labels at face value (exp277's convention) for
  walk-vs-decode comparability, and THE PURE-MASK SPLIT (the boundary
  ring's own share vs the interior's own share, computed directly from
  the masks — recoverable in the fresh run, unlike exp277's deposit
  re-read) is recorded alongside, audit-only.

  THE DECOMPOSITION (exp208's decompose conventions VERBATIM): per
  class c — sum_sq_c = sum_{i in c} e_i^2; frac_of_sq = sum_sq_c /
  total; rms_contrib_mV = sqrt(sum_sq_c / n). THE ACCOUNTING IDENTITY
  (G2): sum_c sum_sq_c / n == err_exact^2 — the mean-squared scale the
  RMS actually decomposes (an mV-linear split would be a fake
  identity) — and the fracs sum to 1.0.

  THE PER-HOST TABLE: per-host means over the host's 6 rows (3 seeds x
  2 instances) of frac_cb / frac_pj / frac_int (the exp208-label
  shares), the pure-mask shares, the rms_contrib means, the mean class
  counts, the err_exact and walk_end_rms_carried means.

  THE BRANCH (the discriminant pre-named, the bars numeric, the
  exp277 form): the outliers = exp273's deposited outliers (asserted
  == exp272's descriptive.premium_hosts == ['H3', 'H5']); the cluster
  = the other ten. margin_cb = min(frac_cb_mean over {H3, H5}) -
  max(frac_cb_mean over the cluster); margin_pj likewise.
  WALK-BOUNDARY iff margin_cb >= 0.05 AND margin_cb >= margin_pj;
  WALK-PAIR iff margin_pj >= 0.05 AND margin_pj > margin_cb;
  WALK-CLASS-BLIND otherwise — the exhaustive residual, INCLUDING the
  weak-ordering face (an ordering that holds below the 0.05 bar is
  recorded honestly; the branch stays class-blind). The 0.05
  CONCENTRATION BAR = 5 percentage points of the squared-error share
  (fixed HERE at pre-registration, never fit; exp277's decode-level
  margins were NEGATIVE — -0.0255 cb / -0.1792 pj — so any positive
  walk-level ordering is already new information, recorded in full).
  The both-exceed case: the LARGER margin names the branch; exact
  float equality of the margins (never expected) resolves
  WALK-BOUNDARY (the pre-named order).

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD + S0 ANCHOR INTEGRITY: the 12 base adjacencies
      rebuilt per the exp269/exp280 precedent (graph_path at the chain
      class's n=400 call site for H0/H1 — H0 echoes H1 bit-exactly,
      asserted; small_world(n, 0.10, deposited rewire_seed) for
      H2-H11), bit-asserted against exp243's records: sha256(|A| as
      float64) == base_sha256 12/12; the upper-triangle edge count ==
      edges_base 12/12; the classify boundary-ring count ==
      n_boundary_cells_base 12/12, dual-carried vs exp272's per_host
      AND exp273's field table; the canon identity
      labeling_bfs_n(|A|) == labeling_bfs_n(A) 12/12; f_max recomputed
      == f_max_base 12/12. The two deep-row targets rebuilt per
      exp256's build_rows deep construction (exp214's deep form
      VERBATIM): row_target_sha256 == exp256's deposited instance
      records 72/72, and the base medium sha == exp243's base_sha256
      == the deposited instance medium_sha256 72/72. exp256's 72 rows
      with the substituted structure 36/36 + worst == max 36/36. THE
      RE-READS: exp282's 72 traces complete per row (len ==
      walk_steps >= 1, all finite, final > 0, the convergence point
      existing, trace_sha256 recomputed 72/72) + the three summaries
      re-derived from the deposited traces BIT-EXACT 72/72 x 3 + the
      per-host means bit-exact vs exp282's host_table 12/12 x 3; the
      mia carry bit-exact 12/12 (exp273's field table == exp243's own
      class records) + the premium carry bit-exact 12/12 (exp272 ==
      exp273's field-table carry). THE PROVENANCE CHAINS sha-verified
      against the current file bytes — exp243 (4) + exp256 (3) +
      exp272 (4) + exp273 (5) + exp282 (4) + exp277 (8) = 28 records.
      The source deposits READ-ONLY: sha-recorded BEFORE any read,
      byte-unchanged after the work.
  G2  THE RE-RUN'S ANCHORS + THE ACCOUNTING IDENTITY: the fresh
      state-carrying re-run of the 72 rows through exp282's traced
      replica REUSED VERBATIM — THE S0 ANCHOR: every row's final err
      reproduces exp256's DEPOSITED substituted instance err BIT-EXACT
      (72/72, the machinery's native 2-dp convention; the verified
      flags 72/72) and exp282's deposited walk reproduced BIT-EXACTLY
      (the re-run's per-row trace_sha256 == exp282's deposited
      trace_sha256 72/72 — the decomposition is of the SAME walk
      exp282 traced; the fresh walk_end_rms == exp282's deposited
      walk_end_rms 72/72, float-identical). THE A3 STATE-CONVENTION
      ASSERT 72/72 (round(err_exact, 2) == the reported err — the end
      state's own RMS is the reported err's exact form). THE
      CLASSIFICATION ANCHOR: the fresh classify's pure mask counts on
      each row's WORST instance == exp256's deposited row-level
      class_counts 36/36 (the classification machinery reproduces
      exp256's deposited classify). THE ACCOUNTING IDENTITY per row
      (all 72): sum_c sum_sq_c / n == err_exact^2 within 1e-6 *
      max(1.0, err_exact^2) (exp208's identity form, asserted
      fail=STOP); the fracs sum to 1.0 within 1e-9; the pure masks
      partition n=400 (the counts sum to 400, the masks pairwise
      disjoint, 72/72); the per-row identity residual + the settle gap
      recorded (the max of each, audit-only).
  G3  THE BRANCH DISCRIMINANT (pre-named, the numeric bars): the
      branch resolved on the pre-named margins (the exp277 min-vs-max
      form + the 0.05 concentration bar + the pre-named precedence):
      WALK-BOUNDARY / WALK-PAIR / WALK-CLASS-BLIND. Audit-only, never
      gating: the full 12-host ordering by frac_cb_mean and
      frac_pj_mean; exp277's decode-level margins re-read from its
      deposit and recomputed from its per-host table (asserted equal)
      beside the walk-level margins (the walk-vs-decode face); the
      pure-mask split (the boundary ring's own share vs the
      interior's own share) per host; the per-host shares' Spearman
      against mia_prod_err and the one-zone premium (the
      exp274/exp275/exp282 conventions VERBATIM — Spearman = Pearson
      on scipy's tied-average ranks, the 12-slot frame with the
      H0==H1 echo carried, the ties census per vector, the
      single-predictor rank R2; the interior share's degeneracy —
      identically 0.0 on the exp208-label reading — excluded from the
      regressions, disclosed, exp280's F4 precedent).
  G4  THE DISCIPLINE: deterministic — the fresh re-run executes TWICE,
      the two passes' row payloads (errs, decompositions, tables,
      margins) BIT-IDENTICAL; no wall-clock fields (recursive key scan
      + serialized-blob scan); the docstring + header pinned to this
      pre-registration commit, asserted at entry AND exit; the source
      deposits byte-unchanged; NEURAL_SPEC_MIN == -60.0 asserted at
      exit (exp218's disclosed exp169-import discipline — the whole
      reader chain imported FIRST, the floor restored after; the
      -35.0 reader-line pin disclosed).

THE BRANCHES (pre-named): WALK-BOUNDARY / WALK-PAIR / WALK-CLASS-BLIND.

RUN: the deterministic sha-asserted rebuild (seconds) + the pure
re-reads + the fresh 72-row state-carrying battery run TWICE (72
decodes per pass), foreground ~2-3 min. If a pass cannot finish inside
the 570 s foreground cap, the PRE-NAMED CHECKPOINT-SPLIT runs ONE pass
per invocation (env EXP284_PASS=pass1|pass2 caches that pass's row
payload) and the PRE-NAMED MERGE (env EXP284_MERGE=1) compares the two
cached payloads BIT-EXACT and writes the deposit — the merge never
recomputes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp284_endpoint_composition.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit e70ae65) ==========================
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
    #      is the e70ae65 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "5b695b9525ca75a24e0999c6c72766f4ba50b9c8ee807a68fcfd8bfeb14483c7")
    EXPECTED_HEADER_SHA256 = (
        "96524ddbff40a13671e20d29c86444c272fdd5fdb579e66ea0bc35367eee3392")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from e70ae65"
    assert header_ok, "header drifted from e70ae65"

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
    CONCENTRATION_BAR = 0.05               # the pre-named 0.05 bar (G3)

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
    DEP277 = os.path.join(ROOT, "results",
                          "exp277_deep_band_break_face.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP277)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP277: "exp277_deposit"}
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
    with open(DEP277) as fh:
        dep277 = json.load(fh)

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep277["hosts"] == hosts, "exp277's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    assert dep272["descriptive"]["premium_hosts"] == outliers, \
        "exp272's premium_hosts drifted from the outlier pre-name"
    assert dep282["outliers"] == outliers, "exp282's outliers drifted"
    assert dep277["outliers"] == outliers, "exp277's outliers drifted"
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

    # ---- the pure-mask shares from classify's own masks (audit-only)
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

    # ---- one traced + decomposed row decode (exp282's
    #      _decode_row_traced form + the composition additions: the
    #      per-cell end errors from final_state, exp208's classify on
    #      the row target + medium, the decomposition, the exp282
    #      trace/walk_end_rms bit-match, the S0 anchor) -------------------
    def _decode_row_composition(host, row_key, spec, med, seed, fmax,
                                dep_rec, rec282, med_A):
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
        # THE CARRIER REPRODUCED BIT-EXACTLY: the re-run's walk IS
        # exp282's deposited walk (the trace sha + the walk_end_rms)
        trace_match = bool(trace_sha == rec282["trace_sha256"])
        assert trace_match, \
            (f"{host} {row_key} s{seed}: the fresh trace sha drifted from "
             f"exp282's deposited trace sha — the walk is not the traced one")
        walk_end_match = bool(final == float(rec282["walk_end_rms"]))
        assert walk_end_match, \
            (f"{host} {row_key} s{seed}: the fresh walk_end_rms drifted from "
             "exp282's deposited walk_end_rms")
        # THE S0 ANCHOR: the fresh run reproduces exp256's deposited
        # substituted err BIT-EXACT (the machinery's native 2-dp form)
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
        return {
            "host": host, "seed": int(seed), "instance": int(row_key[-1]),
            "row_key": row_key, "pert": P3, "medium": "base",
            "err": err, "err_deposited": float(dep_rec["err"]),
            "err_exact": err_exact, "a3_ok": a3_ok,
            "verified": bool(out["program_verified"]),
            "branch": str(out["branch"]), "rho": float(out["rho"]),
            "walk_steps": steps, "trace_len": len(trace),
            "walk_end_rms": final,
            "walk_end_rms_carried_exp282": float(rec282["walk_end_rms"]),
            "settle_gap_abs": float(settle_gap),
            "trace_sha256": trace_sha,
            "trace_sha256_matches_exp282": trace_match,
            "s0_err_ok": s0_err_ok, "s0_verified_ok": s0_ver_ok,
            "conv_step": int(conv),
            "class_counts": counts,
            "per_class": decomp["per_class"],
            "identity_residual": decomp["identity_residual"],
            "pure_shares": _pure_shares(e2, cinfo),
            "partition_ok": partition_ok,
            "interior_label_empty": interior_label_empty}

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; the pre-named 28 records: exp243 4 + exp256 3 +
    #      exp272 4 + exp273 5 + exp282 4 + exp277 8) ----------------------
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
        ("exp277_deep_band_break_face.json", "inputs"))

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
        assert total == 28, f"the chain record count {total} != 28"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

    # ---- THE COMPUTATION (one full pass: the sha-asserted rebuild +
    #      the pure re-reads + the fresh 72-row state-carrying battery
    #      + the decomposition + the table + the branch; run twice —
    #      G4's two-pass clause) -------------------------------------------
    def compute():
        _LOCK_LOG.clear()
        # ---- G1: THE REBUILD (exp269's/exp280's form, every rebuild
        #      bit-asserted against exp243's OWN records) ------------------
        g1 = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0, "n_bnd_ok": 0,
              "n_bnd_dual_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
              "n_fmax_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
              "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
              "n_medium_shas_ok": 0, "n_traces282_complete": 0,
              "n_trace_sha282_ok": 0, "n_summaries282_bit_exact": 0,
              "n_host_means282_ok": 0, "n_mia_carry": 0,
              "n_prem_carry": 0}
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

        # ---- G1: THE PURE RE-READ of exp282's trajectory deposit — the
        #      carrier (walk_end_rms per row) carried BIT-EXACT ---------
        rows282 = dep282["rows"]
        assert len(rows282) == 72, "exp282's 72-row deposit drifted"
        r282 = {}
        for r in rows282:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r282, f"duplicate exp282 row {key}"
            tr = [float(x) for x in r["trace"]]
            steps = int(r["walk_steps"])
            complete = bool(len(tr) == steps and steps >= 1
                            and all(np.isfinite(tr)) and tr[-1] > 0.0)
            assert complete, f"{key}: exp282's trace incomplete"
            final = tr[-1]
            thresh = 2.0 * final
            conv = None
            for k, v in enumerate(tr):
                if v < thresh:
                    conv = k
                    break
            assert conv is not None, f"{key}: exp282's conv point missing"
            # the three summaries re-derived from the deposited trace
            w = max(2, int(np.ceil(0.10 * steps)))
            w = min(w, steps)
            idx = np.arange(steps - w, steps, dtype=float)
            slope = float(np.polyfit(idx, np.asarray(tr[-w:], dtype=float),
                                     1)[0])
            sums_ok = bool(final == float(r["walk_end_rms"])
                           and slope == float(r["last10_slope"])
                           and int(conv) == int(r["conv_step"]))
            assert sums_ok, f"{key}: exp282's summaries re-derive drifted"
            tsha = hashlib.sha256(
                json.dumps(tr, sort_keys=True).encode()).hexdigest()
            assert tsha == r["trace_sha256"], \
                f"{key}: exp282's trace_sha256 recompute drifted"
            g1["n_traces282_complete"] += int(complete)
            g1["n_trace_sha282_ok"] += 1
            g1["n_summaries282_bit_exact"] += int(sums_ok)
            r282[key] = {"trace": tr, "walk_steps": steps,
                         "walk_end_rms": final, "trace_sha256": tsha}
        rows282_by_key = {(r["host"], int(r["seed"]), r["row_key"]): r
                          for r in rows282}
        ht282 = {row["host"]: row for row in dep282["host_table"]}
        for h in hosts:
            vals = {"walk_end_rms": [], "last10_slope": [], "conv_step": []}
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    rr = rows282_by_key[(h, s, rk)]
                    vals["walk_end_rms"].append(float(rr["walk_end_rms"]))
                    vals["last10_slope"].append(float(rr["last10_slope"]))
                    vals["conv_step"].append(float(rr["conv_step"]))
            means_ok = bool(
                float(np.mean(vals["walk_end_rms"]))
                == float(ht282[h]["walk_end_rms_mean"])
                and float(np.mean(vals["last10_slope"]))
                == float(ht282[h]["last10_slope_mean"])
                and float(np.mean(vals["conv_step"]))
                == float(ht282[h]["conv_step_mean"]))
            assert means_ok, f"{h}: exp282's host means drifted"
            g1["n_host_means282_ok"] += int(means_ok)
        assert g1["n_traces282_complete"] == 72 \
            and g1["n_trace_sha282_ok"] == 72 \
            and g1["n_summaries282_bit_exact"] == 72 \
            and g1["n_host_means282_ok"] == 12, \
            "exp282's re-read integrity drifted"

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

        # ---- G1: THE PROVENANCE CHAINS (28 records) ---------------------
        chains = _verify_chains()

        # ---- G2: THE FRESH STATE-CARRYING RE-RUN (72 rows; the S0
        #      anchor + exp282's walk reproduced bit-exactly + the
        #      per-cell decomposition) ------------------------------------
        g2 = {"n_rows": 0, "n_s0_err_ok": 0, "n_s0_verified_ok": 0,
              "n_trace_match": 0, "n_walk_end_match": 0, "n_a3_ok": 0,
              "n_partition_ok": 0, "n_interior_label_empty": 0,
              "n_identity_ok": 0, "n_frac_sum_ok": 0,
              "n_class_anchor_ok": 0, "max_identity_residual": 0.0,
              "max_settle_gap": 0.0}
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    d = dep_sub[(k, s, rk)]
                    rec = _decode_row_composition(
                        k, rk, ctx["deep"][inst]["spec"], med, s,
                        ctx["fmax"], d, r282[(k, s, rk)], med.A)
                    rows_out.append(rec)
                    g2["n_rows"] += 1
                    g2["n_s0_err_ok"] += int(rec["s0_err_ok"])
                    g2["n_s0_verified_ok"] += int(rec["s0_verified_ok"])
                    g2["n_trace_match"] += int(
                        rec["trace_sha256_matches_exp282"])
                    g2["n_walk_end_match"] += int(
                        rec["walk_end_rms"]
                        == rec["walk_end_rms_carried_exp282"])
                    g2["n_a3_ok"] += int(rec["a3_ok"])
                    g2["n_partition_ok"] += int(rec["partition_ok"])
                    g2["n_interior_label_empty"] += int(
                        rec["interior_label_empty"])
                    g2["n_identity_ok"] += int(
                        rec["identity_residual"]
                        < 1e-6 * max(1.0, rec["err_exact"] ** 2))
                    g2["n_frac_sum_ok"] += int(
                        abs(sum(p["frac_of_sq"]
                                for p in rec["per_class"]) - 1.0) < 1e-9)
                    g2["max_identity_residual"] = max(
                        g2["max_identity_residual"],
                        float(rec["identity_residual"]))
                    g2["max_settle_gap"] = max(
                        g2["max_settle_gap"], float(rec["settle_gap_abs"]))
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [{k}] composed 6 rows | errs "
                  f"{[r['err'] for r in hs]} | cb_frac "
                  f"{[round(r['per_class'][0]['frac_of_sq'], 4) for r in hs]}")
        assert len(rows_out) == 72, \
            f"the composed battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"

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
            assert len(hs) == 6, f"{h}: the 6 composed rows drifted"
            cb = [r["per_class"][0] for r in hs]
            pj = [r["per_class"][1] for r in hs]
            it = [r["per_class"][2] for r in hs]
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "frac_cb_mean": float(np.mean(
                    [p["frac_of_sq"] for p in cb])),
                "frac_pj_mean": float(np.mean(
                    [p["frac_of_sq"] for p in pj])),
                "frac_int_mean": float(np.mean(
                    [p["frac_of_sq"] for p in it])),
                "pure_boundary_ring_share_mean": float(np.mean(
                    [r["pure_shares"]["boundary_ring"] for r in hs])),
                "pure_pair_junction_only_share_mean": float(np.mean(
                    [r["pure_shares"]["pair_junction_only"] for r in hs])),
                "pure_interior_share_mean": float(np.mean(
                    [r["pure_shares"]["interior_only"] for r in hs])),
                "cb_rms_contrib_mean": float(np.mean(
                    [p["rms_contrib_mV"] for p in cb])),
                "pj_rms_contrib_mean": float(np.mean(
                    [p["rms_contrib_mV"] for p in pj])),
                "mean_class_counts": {
                    kk: float(np.mean([r["class_counts"][kk] for r in hs]))
                    for kk in ("CANON-BOUNDARY", "PAIR-JUNCTION",
                               "INTERIOR")},
                "err_exact_mean": float(np.mean(
                    [r["err_exact"] for r in hs])),
                "walk_end_rms_carried_mean": float(np.mean(
                    [r["walk_end_rms_carried_exp282"] for r in hs])),
                "settle_gap_mean": float(np.mean(
                    [r["settle_gap_abs"] for r in hs]))})

        # ---- AUDIT-ONLY: the exp277 decode-level re-read (the
        #      walk-vs-decode face; the margins recomputed and
        #      asserted == the deposited discriminant) ---------------------
        ht277 = {row["host"]: row for row in dep277["per_host_table"]}
        assert dep277["branch"] == "NEITHER", \
            "exp277's deposited branch drifted from NEITHER"
        dec_cb_out = {h: float(ht277[h]["cb_frac_mean"])
                      for h in outliers}
        dec_pj_out = {h: float(ht277[h]["pj_frac_mean"])
                      for h in outliers}
        dec_cb_clu = [float(ht277[h]["cb_frac_mean"]) for h in cluster]
        dec_pj_clu = [float(ht277[h]["pj_frac_mean"]) for h in cluster]
        dec_margin_cb = min(dec_cb_out.values()) - max(dec_cb_clu)
        dec_margin_pj = min(dec_pj_out.values()) - max(dec_pj_clu)
        bd = dep277["branch_discriminant"]
        assert dec_margin_cb == float(bd["cb_outlier_margin"]), \
            "exp277's cb margin recompute drifted"
        assert dec_margin_pj == float(bd["pj_outlier_margin"]), \
            "exp277's pj margin recompute drifted"
        decode_level = {
            "branch_deposited": dep277["branch"],
            "per_host_cb_frac_mean": {h: float(ht277[h]["cb_frac_mean"])
                                      for h in hosts},
            "per_host_pj_frac_mean": {h: float(ht277[h]["pj_frac_mean"])
                                      for h in hosts},
            "cb_outlier_margin": dec_margin_cb,
            "pj_outlier_margin": dec_margin_pj,
            "margins_recomputed_equal_deposited": True}

        # ---- THE REGRESSIONS (audit-only; the exp274/exp275/exp282
        #      conventions VERBATIM: Spearman = Pearson on the
        #      tied-average ranks; the single-predictor OLS rank R2;
        #      the ties census per vector; the interior label share's
        #      degeneracy — identically 0.0 — excluded, disclosed) ------
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

        assert all(row["frac_int_mean"] == 0.0 for row in host_table), \
            "the exp208-label interior share is not identically 0.0"
        SHARE_COLS = {"frac_cb": [row["frac_cb_mean"] for row in host_table],
                      "frac_pj": [row["frac_pj_mean"] for row in host_table]}
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
                    "ties_target": _ties_census(tvals)}

        # ---- G3: THE BRANCH DISCRIMINANT (pre-named numeric bars) -------
        cb_out = {row["host"]: row["frac_cb_mean"] for row in host_table
                  if row["outlier"]}
        pj_out = {row["host"]: row["frac_pj_mean"] for row in host_table
                  if row["outlier"]}
        cb_clu = [row["frac_cb_mean"] for row in host_table
                  if not row["outlier"]]
        pj_clu = [row["frac_pj_mean"] for row in host_table
                  if not row["outlier"]]
        margin_cb = min(cb_out.values()) - max(cb_clu)
        margin_pj = min(pj_out.values()) - max(pj_clu)
        cb_orders = bool(min(cb_out.values()) > max(cb_clu))
        pj_orders = bool(min(pj_out.values()) > max(pj_clu))
        if margin_cb >= CONCENTRATION_BAR and margin_cb >= margin_pj:
            branch_local = "WALK-BOUNDARY"
        elif margin_pj >= CONCENTRATION_BAR and margin_pj > margin_cb:
            branch_local = "WALK-PAIR"
        else:
            branch_local = "WALK-CLASS-BLIND"
        g3 = {
            "margin_cb": margin_cb, "margin_pj": margin_pj,
            "concentration_bar": CONCENTRATION_BAR,
            "cb_outlier_shares": cb_out, "pj_outlier_shares": pj_out,
            "cb_cluster_max": max(cb_clu), "cb_cluster_min": min(cb_clu),
            "pj_cluster_max": max(pj_clu), "pj_cluster_min": min(pj_clu),
            "cb_orders_over_cluster": cb_orders,
            "pj_orders_over_cluster": pj_orders,
            "ordering_by_frac_cb": [
                {"host": row["host"], "frac_cb_mean": row["frac_cb_mean"]}
                for row in sorted(host_table,
                                  key=lambda r: r["frac_cb_mean"])],
            "ordering_by_frac_pj": [
                {"host": row["host"], "frac_pj_mean": row["frac_pj_mean"]}
                for row in sorted(host_table,
                                  key=lambda r: r["frac_pj_mean"])],
            "decode_level_exp277": decode_level,
            "branch": branch_local}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "rebuild_report": rebuild_report, "g1": g1, "g2": g2,
                "g3": g3, "rows": rows_out, "host_table": host_table,
                "targets": targets, "regressions": regressions,
                "provenance_chains": chains, "ro_before": ro_before,
                "lock_reads": len(_LOCK_LOG)}

    # ---- the mode dispatch (the pre-named RUN clause: the default
    #      two-pass in-process form; EXP284_MODE=pass1|pass2 checkpoints
    #      ONE pass; EXP284_MODE=merge compares the two cached payloads
    #      bit-exact and writes the deposit — the merge never recomputes)
    _MODE = os.environ.get("EXP284_MODE", "")
    _CK1 = os.path.join(ROOT, "results",
                        ".exp284_pass1.checkpoint.json")
    _CK2 = os.path.join(ROOT, "results",
                        ".exp284_pass2.checkpoint.json")

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
        print("=== exp284: THE ENDPOINT COMPOSITION (the end-RMS carrier "
              "decomposed by cell class at the walk level) ===")
        print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
              f"instances at n={N400} = 72 composed rows, ONE FRESH RUN, "
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
                   and g1["n_medium_shas_ok"] == 72
                   and g1["n_traces282_complete"] == 72
                   and g1["n_trace_sha282_ok"] == 72
                   and g1["n_summaries282_bit_exact"] == 72
                   and g1["n_host_means282_ok"] == 12
                   and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
                   and pa["provenance_chains"]["total_verified"] == 28
                   and ro_unchanged)
    g2_pass = bool(g2["n_rows"] == 72 and g2["n_s0_err_ok"] == 72
                   and g2["n_s0_verified_ok"] == 72
                   and g2["n_trace_match"] == 72
                   and g2["n_walk_end_match"] == 72
                   and g2["n_a3_ok"] == 72 and g2["n_partition_ok"] == 72
                   and g2["n_interior_label_empty"] == 72
                   and g2["n_identity_ok"] == 72
                   and g2["n_frac_sum_ok"] == 72
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
                          "exp282's deposited walk reproduced bit-exactly "
                          "(trace_sha256 72/72 + walk_end_rms "
                          "float-identical 72/72)")},
        "G2_reanchor_accounting_identity": {
            "pass": g2_pass,
            "counts": g2,
            "identity_form": ("sum_c sum_sq_c / n == err_exact^2 within "
                              "1e-6 * max(1.0, err_exact^2) — the "
                              "mean-squared scale the RMS actually "
                              "decomposes (exp208's identity form); the "
                              "fracs sum to 1.0 within 1e-9; the class "
                              "masks partition n=400")},
        "G3_branch_discriminant": {
            "pass": g3_pass,
            "bar": ("WALK-BOUNDARY iff margin_cb >= 0.05 AND margin_cb >= "
                    "margin_pj; WALK-PAIR iff margin_pj >= 0.05 AND "
                    "margin_pj > margin_cb; WALK-CLASS-BLIND otherwise "
                    "(the exhaustive residual incl. the weak-ordering "
                    "face); the margins in the exp277 min-vs-max form")},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_rebuild_s0_anchor_integrity",
                 "G2_reanchor_accounting_identity",
                 "G3_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])

    branch = g3["branch"]
    margin_cb = g3["margin_cb"]
    margin_pj = g3["margin_pj"]

    def _g(x):
        return f"{x:+.4f}"

    cb_out = g3["cb_outlier_shares"]
    cb_clu_max = g3["cb_cluster_max"]
    pj_out = g3["pj_outlier_shares"]
    pj_clu_max = g3["pj_cluster_max"]
    dec = g3["decode_level_exp277"]

    verdict_body = (
        f"{branch} — "
        + ("the outlier hosts' end-RMS mass concentrates in "
           "CANON-BOUNDARY cells at the walk level"
           if branch == "WALK-BOUNDARY" else
           "the outlier hosts' end-RMS mass concentrates in "
           "PAIR-JUNCTION cells at the walk level"
           if branch == "WALK-PAIR" else
           "the walk-level break is ALSO class-blind — the outlier "
           "hosts' end-RMS class composition is class-typical of the "
           "cluster (matching exp277's decode-level NEITHER)")
        + f" (margin_cb {_g(margin_cb)} [outliers {cb_out['H3']:.4f}/"
        f"{cb_out['H5']:.4f} vs cluster max {cb_clu_max:.4f}], margin_pj "
        f"{_g(margin_pj)} [outliers {pj_out['H3']:.4f}/{pj_out['H5']:.4f} "
        f"vs cluster max {pj_clu_max:.4f}]; the 0.05 concentration bar "
        + ("CROSSED" if branch != "WALK-CLASS-BLIND"
           else "NOT crossed")
        + f") | exp277's decode-level NEITHER beside it (its margins "
        f"{_g(dec['cb_outlier_margin'])} cb / "
        f"{_g(dec['pj_outlier_margin'])} pj) | the pure-mask split "
        f"(audit-only): boundary-ring share H3 "
        f"{[r for r in pa['host_table'] if r['host'] == 'H3'][0]['pure_boundary_ring_share_mean']:.4f} "
        f"/ H5 "
        f"{[r for r in pa['host_table'] if r['host'] == 'H5'][0]['pure_boundary_ring_share_mean']:.4f} "
        f"vs interior share H3 "
        f"{[r for r in pa['host_table'] if r['host'] == 'H3'][0]['pure_interior_share_mean']:.4f} "
        f"/ H5 "
        f"{[r for r in pa['host_table'] if r['host'] == 'H5'][0]['pure_interior_share_mean']:.4f} "
        f"| the end-RMS decomposition: err_exact from the state-carrying "
        f"read's final_state (the A3-checked convention; the PRE-settle "
        f"trace[-1] carrier carried bit-exact from exp282; the settle "
        f"gap max {g2['max_settle_gap']:.4f} mV, audit-only) | THE S0 "
        f"ANCHOR: the fresh re-run reproduced exp256's deposited "
        f"substituted errs bit-exact ({g2['n_s0_err_ok']}/72, the "
        f"verified flags {g2['n_s0_verified_ok']}/72) AND exp282's "
        f"deposited walk bit-exactly (trace_sha256 "
        f"{g2['n_trace_match']}/72, walk_end_rms "
        f"{g2['n_walk_end_match']}/72) — the decomposition is of the "
        f"SAME walk exp282 traced | the accounting identity: per-class "
        f"sums reconstruct the end RMS 72/72 (max residual "
        f"{g2['max_identity_residual']:.2e}); the classification anchor "
        f"36/36 (the fresh worst-instance mask counts == exp256's "
        f"deposited row class_counts) | 12 hosts, a deterministic "
        f"sha-asserted rebuild (graph_path for H0/H1, small_world at the "
        f"deposited rewire seeds — exp269's/exp280's form), the "
        f"provenance chains sha-verified 28/28, 6 deposits READ-ONLY "
        f"byte-unchanged, two-pass bit-identical, floor -60.0")

    # ---- the discipline scans (no wall-clock fields; the deposit form) --
    deposit = {
        "exp": "exp284_endpoint_composition",
        "claim": (
            "THE ENDPOINT COMPOSITION (batch 42, pre-registration commit "
            "e70ae65): the end-RMS carrier (exp282's walk_end_rms, the "
            "strongest premium carrier at +0.88) decomposed by cell "
            "class at the WALK level — the new surface (exp277 found "
            "the decode-level break class-blind). The pure re-reads "
            "where possible + the minimal fresh state-carrying re-run "
            "where the per-cell end state is needed: exp282's "
            "_execute_signed_traced replica REUSED VERBATIM on the "
            "SAME 72 substituted rows (12 hosts x 3 seeds x the two "
            "deep instances at n=400 — exp256's battery, ONE FRESH "
            "RUN); the per-cell end errors from the state-carrying "
            "read's final_state (e_i = V_i - T_i), the END-RMS = "
            "err_exact (the A3-checked state convention; the "
            "PRE-settle trace[-1] carrier vs the POST-settle end state "
            "disclosed pre-body — the trace stores scalars, not the "
            "frame; the settle gap recorded, ~1e-3 mV); the cells "
            "classified per instance by exp208's classify VERBATIM on "
            "the row target + medium (CANON-BOUNDARY / PAIR-JUNCTION / "
            "INTERIOR, the registered precedence; exp277's "
            "mask-semantics disclosure carried — the exp208-label "
            "CANON-BOUNDARY record is the NON-PAIR-JUNCTION "
            "complement, the branch reads the labels at face value "
            "for walk-vs-decode comparability, the PURE-MASK SPLIT "
            "recorded audit-only); the decomposition exp208's "
            "conventions VERBATIM (sum_sq / frac_of_sq / "
            "rms_contrib_mV; the identity on the mean-squared scale); "
            "the branch WALK-BOUNDARY / WALK-PAIR / WALK-CLASS-BLIND "
            "(the exp277 min-vs-max margins + the 0.05 concentration "
            "bar fixed at pre-registration, never fit; the precedence "
            "boundary-then-pair on the both-exceed case)"),
        "method": {
            "end_rms": ("err_exact = sqrt(mean((V - T)^2)) from the "
                        "state-carrying read's final_state — the "
                        "A3-checked state convention (round(err_exact, "
                        "2) == the reported err; the S0 anchor pins the "
                        "reported err to exp256's deposited substituted "
                        "errs bit-exact)"),
            "carrier_vs_end_state": (
                "exp282's walk_end_rms carrier is the PRE-settle "
                "trace[-1]; the final_state end state is POST-settle "
                "(exp142's fixed 15.0 settle tail — a fixed part of "
                "the executor, not a knob); the trace stores scalars, "
                "not the frame, so the end state is the ONLY per-cell "
                "end record the landed machinery provides; the per-row "
                "settle gap |err_exact - walk_end_rms_carried| "
                "recorded (audit-only)"),
            "classification": (
                "exp208's classify VERBATIM per instance: "
                "classify(T_instance, A_host) — CANON-BOUNDARY (a ring "
                "neighbor's target value differs), PAIR-JUNCTION "
                "(endpoint of >= 2 chords in |A_base| > 0), INTERIOR "
                "(neither); precedence the registered listing order; "
                "the exp208-label CANON-BOUNDARY record is the "
                "NON-PAIR-JUNCTION complement (exp277's disclosure, "
                "carried) — the branch reads the labels at face value "
                "for walk-vs-decode comparability; the pure-mask split "
                "(the boundary ring's own share vs the interior's own "
                "share) recorded audit-only"),
            "decomposition": ("exp208's conventions VERBATIM: per class "
                              "sum_sq_c = sum e_i^2; frac_of_sq = "
                              "sum_sq_c / total; rms_contrib_mV = "
                              "sqrt(sum_sq_c / n); the identity on the "
                              "mean-squared scale"),
            "table": ("per-host means over the host's 6 substituted "
                      "rows (3 seeds x 2 instances)"),
            "branch_rule": ("margin_cb = min(frac_cb_mean over {H3, H5}) "
                            "- max(frac_cb_mean over the cluster); "
                            "margin_pj likewise; WALK-BOUNDARY iff "
                            "margin_cb >= 0.05 AND margin_cb >= "
                            "margin_pj; WALK-PAIR iff margin_pj >= 0.05 "
                            "AND margin_pj > margin_cb; WALK-CLASS-BLIND "
                            "otherwise (the exhaustive residual incl. "
                            "the weak-ordering face); the 0.05 bar = 5 "
                            "percentage points of the squared-error "
                            "share, fixed at pre-registration"),
            "regressions": ("audit-only, the exp274/exp275/exp282 "
                            "conventions VERBATIM: Spearman = Pearson "
                            "on the tied-average ranks (scipy rankdata); "
                            "the single-predictor OLS rank R2 (the "
                            "response as its tied-average ranks, the "
                            "target as the numeric design column) + the "
                            "all-ranks variant AUDIT-ONLY; the ties "
                            "census per vector; the 12-slot frame with "
                            "the H0==H1 echo carried; the interior "
                            "label share's degeneracy (identically 0.0 "
                            "on the exp208-label reading) excluded from "
                            "the regressions, disclosed — exp280's F4 "
                            "precedent")},
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
                "the trajectory deposit — the carrier (walk_end_rms "
                "per row) + the 72 traces + the trace shas (the "
                "re-run's bit-exact walk reproduction) + the host "
                "means table",
                "the decode-level break face — the per-host decode "
                "shares + the deposited NEITHER branch + the margins "
                "(the walk-vs-decode comparison, audit-only)"))},
        "hosts": pa["hosts"],
        "outliers": pa["outliers"],
        "cluster": pa["cluster"],
        "rebuild_report": pa["rebuild_report"],
        "provenance_chains": pa["provenance_chains"],
        "rows": pa["rows"],
        "host_table": pa["host_table"],
        "targets": pa["targets"],
        "regressions": pa["regressions"],
        "decode_level_exp277": pa["g3"]["decode_level_exp277"],
        "gates": gates,
        "branch": branch,
        "branch_discriminant": {
            "margin_cb": margin_cb, "margin_pj": margin_pj,
            "concentration_bar": CONCENTRATION_BAR,
            "cb_outlier_shares": g3["cb_outlier_shares"],
            "pj_outlier_shares": g3["pj_outlier_shares"],
            "cb_cluster_max": g3["cb_cluster_max"],
            "cb_cluster_min": g3["cb_cluster_min"],
            "pj_cluster_max": g3["pj_cluster_max"],
            "pj_cluster_min": g3["pj_cluster_min"],
            "cb_orders_over_cluster": g3["cb_orders_over_cluster"],
            "pj_orders_over_cluster": g3["pj_orders_over_cluster"],
            "ordering_by_frac_cb": g3["ordering_by_frac_cb"],
            "ordering_by_frac_pj": g3["ordering_by_frac_pj"],
            "precedence": ("the larger margin names the branch on the "
                           "both-exceed case; exact float equality "
                           "resolves WALK-BOUNDARY (the pre-named "
                           "order)")},
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
        "docstring_byte_unchanged_vs_e70ae65": docstring_ok,
        "header_byte_unchanged_vs_e70ae65": header_ok,
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
          f"H0 == H1; the deep targets {g1['n_deep_targets_ok']}/72 + the "
          f"medium shas {g1['n_medium_shas_ok']}/72 + f_max "
          f"{g1['n_fmax_ok']}/12; exp282's re-read: traces complete "
          f"{g1['n_traces282_complete']}/72 + trace shas "
          f"{g1['n_trace_sha282_ok']}/72 + summaries bit-exact "
          f"{g1['n_summaries282_bit_exact']}/72 + host means "
          f"{g1['n_host_means282_ok']}/12; the carries mia "
          f"{g1['n_mia_carry']}/12 + premium {g1['n_prem_carry']}/12; the "
          f"provenance chains "
          f"{pa['provenance_chains']['total_verified']}/28)")
    print(f"  G2 re-run anchors + accounting identity: "
          f"{'PASS' if gates['G2_reanchor_accounting_identity']['pass'] else 'FAIL'} "
          f"(THE S0 ANCHOR — the fresh errs == exp256's deposited "
          f"substituted errs bit-exact {g2['n_s0_err_ok']}/72, the "
          f"verified flags {g2['n_s0_verified_ok']}/72; exp282's walk "
          f"reproduced bit-exactly: trace_sha256 {g2['n_trace_match']}/72 "
          f"+ walk_end_rms {g2['n_walk_end_match']}/72; the A3 convention "
          f"{g2['n_a3_ok']}/72; the classification anchor "
          f"{g2['n_class_anchor_ok']}/36; the accounting identity "
          f"{g2['n_identity_ok']}/72 (max residual "
          f"{g2['max_identity_residual']:.2e}); the fracs sum to 1 "
          f"{g2['n_frac_sum_ok']}/72; the masks partition "
          f"{g2['n_partition_ok']}/72; the settle gap max "
          f"{g2['max_settle_gap']:.4f} mV)")
    print("  the 12-host composition table (per-host means; H3/H5 the "
          "outliers):")
    for row in pa["host_table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} cb_frac {row['frac_cb_mean']:.4f}  "
              f"pj_frac {row['frac_pj_mean']:.4f}  pure_bnd "
              f"{row['pure_boundary_ring_share_mean']:.4f}  pure_int "
              f"{row['pure_interior_share_mean']:.4f}  err_exact "
              f"{row['err_exact_mean']:.3f}{tag}")
    print("  G3 branch — the audit-only share regressions (the "
          "exp274/exp275/exp282 conventions):")
    for k, v in pa["regressions"].items():
        print(f"      {k:28s} rho {v['rho']:+.4f}  (abs "
              f"{v['rho_abs']:.4f})")
    print(f"      decode-level exp277: branch {dec['branch_deposited']} | "
          f"its margins cb {_g(dec['cb_outlier_margin'])} / pj "
          f"{_g(dec['pj_outlier_margin'])}")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock}; 6 deposits READ-ONLY byte-unchanged: "
          f"{ro_unchanged})")
    print(f"\n  BRANCH: {branch} | margin_cb {_g(margin_cb)} | margin_pj "
          f"{_g(margin_pj)} | the 0.05 concentration bar "
          f"{'CROSSED' if branch != 'WALK-CLASS-BLIND' else 'NOT crossed'}")
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
