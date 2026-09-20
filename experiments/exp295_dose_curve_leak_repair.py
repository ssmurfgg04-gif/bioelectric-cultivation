#!/usr/bin/env python3
"""exp295 — THE DOSE CURVE REFINED AND THE NBOR LEAK REPAIR (batch 48;
ledger L273's registered nexts (i)+(ii) — exp292 landed DOSE-REVERSAL
x SELF-DOMINANT: the self-history carrier peaks at g ~ 1.0 (the
reversal past the peak 12/12) and the neighbor-mean form degrades
12/12 (+1.8385 mV at g=1.0 — the register of the unwound neighbors
holds the SPEC INSTALL, so the naive neighbor mean re-injects the
spec's own values as a false history: THE LEAK). Two pre-named
follow-ups, one battery: (1) THE DOSE CURVE refined around the peak —
the pre-named {0.75, 1.0, 1.25, 1.5} SELF ladder (the reversal's
sharpness: is the peak flat or sharp?); (2) THE LEAK REPAIR — the
WRITE-SET-WEIGHTED neighbor form: the neighbor mean weighted by each
neighbor's write-set membership (nbrs that the program ACTUALLY
wrote contribute their true commit history; unwritten nbrs — whose
register holds the spec install — contribute ZERO weight): the leak
face isolated. The repaired NBOR arm re-runs the source face: does
the social form turn from poison to neutral/protection once the leak
is removed?)

THE INSTRUMENT (exp292's landed form REUSED VERBATIM): the additive
phi_history register, the traced replica, the 72-row substituted
battery. The arms:
  SELF-R  — the self form at g in {0.75, 1.0, 1.25, 1.5} (the
            refined curve; the g=1.0 point anchors bit-exact vs
            exp289's deposited g=1.0 errs 72/72);
  NBW     — the write-set-weighted neighbor form at g in {0.25, 0.5,
            1.0} (exp292's NBOR grid, now leak-repaired; the weight
            w_j = 1 if the neighbor j is in the row's write set (the
            commit sequence's support) else 0; the mean over the
            weighted support; a row with NO written neighbors falls
            back to the self value — disclosed, the fallback count
            recorded).
The g=0.0 control is exp289's/exp288's anchor errs (the deposits,
bit-exact — read, never re-run).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR + THE ARMS' INTEGRITY: the SELF g=1.0 errs ==
      exp289's deposited g=1.0 errs BIT-EXACT 72/72 (the trace shas
      72/72); per arm-cell the finite/A3/trace-length/commit-count
      asserts 72/72; the S* lock reads 504 (7 arm-cells x 72); the
      floor -60.0 throughout (no stress); 9 deposits READ-ONLY
      (exp243/256/272/273/282/287/288/289/292), sha before/after.
  G2  THE FORMS' DEFINITION (zero-knob asserted, fail=STOP per row):
      the NBW weights derived ONLY from the commit sequence's support
      (the write set — no new knobs); the fallback-to-self count
      recorded per row (audit); the register replay equality per arm
      at the PER-ARM scope (exp292's diagnosis honored): 72/72 per
      arm-cell; the complement 72/72 per arm-cell.
  G3  THE TWO BRANCH FACES (pre-named numeric bars):
      THE DOSE FACE (SELF-R): the curve's shape at the refined grid —
      PEAK-FLAT  iff the |delta| differences among {0.75, 1.0, 1.25}
          are all < 0.01 mV on >= 10/12 hosts (a plateau);
      PEAK-SHARP otherwise (a distinct optimum — the reversal's
          sharpness recorded by the argbest host-wise, audit-only).
      THE LEAK FACE (NBW vs exp292's NBOR deposited deltas): the
      repaired form's mean paired delta vs the leaky form's +1.8385
      at g=1.0:
      LEAK-CONFIRMED  iff the NBW delta at g=1.0 improves vs the NBOR
          deposited delta by > 0.05 mV on >= 10/12 hosts (the leak
          WAS the failure mode);
      LEAK-NOT-SUFFICIENT otherwise (the social form's failure is
          deeper than the leak — recorded honestly).
      Audit-only: the per-host per-arm delta table, the fallback
      counts, the worst-err vs the 6.0 bar, the R_max face (audit).
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PEAK-FLAT / PEAK-SHARP x LEAK-CONFIRMED /
LEAK-NOT-SUFFICIENT (the two faces recorded independently).

RUN: 504 decodes ~ 7-10 min — the pre-named form is the CHECKPOINT-
SPLIT EXP295_MODE=pass1 (SELF-R, 288 decodes) | pass2 (NBW, 216
decodes) | merge; the in-process default for the GitHub runners.
Both forms evaluate the SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp295_dose_curve_leak_repair.json")


def main() -> dict:
    # ==== BODY (written under the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit dfd6fb5; gates G1-G4
    #      evaluated exactly once. THE INSTRUMENT BASE IS exp292's LANDED
    #      BODY (commit da45529) REUSED VERBATIM — the register, the two
    #      source forms' plumbing, the decode, the rebuild, the cells/
    #      delta assembly, the deposit-reading; every exp295 delta is
    #      marked `exp295 delta` inline; the ONLY new code is the SELF-R
    #      dose grid {0.75, 1.0, 1.25, 1.5}, the NBW write-set-weighted
    #      neighbor form (the leak repair: w_j = 1 iff the neighbor is in
    #      the row's commit-sequence support, the weighted mean, the
    #      no-written-neighbor fallback to the self value with the
    #      fallback count recorded), and the two branch faces (PEAK-FLAT/
    #      PEAK-SHARP; LEAK-CONFIRMED/LEAK-NOT-SUFFICIENT vs exp292's
    #      deposited NBOR deltas) plus the minimal re-plumbing the
    #      pre-registered checkpoint split dictates) =====================
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
    #      is the dfd6fb5 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "7639137e4b1c437ab0b17e5f74f77914ca491add5a13d16409532b5134c70200")
    EXPECTED_HEADER_SHA256 = (
        "8c4595076736a476419a878670542a401ef337a566dd947e69d6dfa53b7c3a2b")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from dfd6fb5"
    assert header_ok, "header drifted from dfd6fb5"


    # ---- the -60.0 floor (G4: asserted at exit; the exp169-import
    #      discipline — the whole reader chain imported FIRST, every
    #      pinned floor import restored to -60.0 after; exp295: the
    #      -35.0 reader-line pin is N/A — no stress arm here, the
    #      floor -60.0 throughout, asserted) ------------------------------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = None    # the exp290 stress-reader pin — N/A here
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"


    # ---- the frozen read configuration (exp256's battery constants;
    #      the replica's executor constants asserted = exp142's own;
    #      exp295 delta: THE ARMS' LADDERS — the SELF-R refined curve
    #      {0.75, 1.0, 1.25, 1.5} (the g=1.0 point IS exp289's landed
    #      grid point — the anchor) and the NBW leak-repaired grid
    #      {0.25, 0.5, 1.0} (exp292's NBOR grid); the g=0.0 control is
    #      the ANCHOR, read from exp289's deposit, never re-run) --------
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
    # exp295 delta — THE ARMS' LADDERS (the pre-named grids) and THE
    # SOURCES (the coupling's read source: "self" == exp289's landed
    # form, "nbw" == the write-set-weighted neighbor mean — the leak
    # repair). The g=0.0 control is the anchor, READ from exp289's
    # deposit — no re-run (the pre-registered form).
    SELF_LADDER = (0.75, 1.0, 1.25, 1.5)
    NBW_LADDER = (0.25, 0.5, 1.0)
    HISTORY_SOURCES = ("self", "nbw")
    # THE BRANCH BARS (pre-named at dfd6fb5, numeric, never fit)
    DOSE_MIN_HOSTS = 10                    # the ">= 10/12 hosts" clauses
    PLATEAU_EPS = 0.01                     # the PEAK-FLAT plateau bar
    MARGIN = 0.05                          # the 0.05 mV margin form
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
    #      zero-reader scan (exp295 delta: the allowed set carries
    #      exp292's landed module TOO — THE INSTRUMENT BASE this module
    #      reuses verbatim; the scan asserts phi_history appears in no
    #      file outside the port + the instrument modules) ----------------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    EXP289_FILE = os.path.join(ROOT, "experiments",
                               "exp289_history_register.py")
    EXP292_FILE = os.path.join(ROOT, "experiments",
                               "exp292_history_dose_source.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)
    exp289_sha_entry = _sha(EXP289_FILE)
    exp292_sha_entry = _sha(EXP292_FILE)

    def _zero_reader_scan():
        """Scan the package + the walk's home for phi_history touches:
        every occurrence must live in the ported collective.py (the
        register's init + the commit-write population + their comments),
        in exp289's landed instrument (the base's base), in exp292's
        landed instrument (THE BASE this module reuses verbatim), in
        exp293's and exp294's modules (the batch-48 siblings — exp293
        pre-registered alongside this base, exp294's body reusing
        exp289's landed source via programmatic byte-slices; each reads
        the register under its own pre-registered discipline), or in
        THIS module (the instrument). No reader anywhere else."""
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
                   "experiments/exp289_history_register.py",
                   "experiments/exp292_history_dose_source.py",
                   "experiments/exp293_history_stress.py",
                   "experiments/exp294_premium_under_history.py",
                   "experiments/exp295_dose_curve_leak_repair.py"}
        unexpected = sorted(set(hits) - allowed)
        assert not unexpected, \
            f"phi_history touched outside the port + the instruments: " \
            f"{unexpected}"
        return {"files_with_phi_history": hits,
                "files_outside_port_and_instruments": unexpected,
                "readers_at_defaults": 0,
                "allowed_set_disclosure": (
                    "the port + exp289's landed instrument (the base's "
                    "base) + exp292's landed instrument (THE BASE this "
                    "module reuses verbatim) + exp293 + exp294 (the "
                    "batch-48 siblings, each reading the register under "
                    "its own pre-registered gates) + this instrument — "
                    "no other reader anywhere")}

    zero_reader_scan = _zero_reader_scan()


    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; exp295 delta:
    #      NINE deposits — exp243 + exp256 + exp272 + exp273 + exp282 +
    #      exp287 + exp288 + exp289 + exp292, the G1 pre-name) -----------
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
    DEP292 = os.path.join(ROOT, "results",
                          "exp292_history_dose_source.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287, DEP288,
                 DEP289, DEP292)
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit",
                  DEP288: "exp288_deposit", DEP289: "exp289_deposit",
                  DEP292: "exp292_deposit"}
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
    with open(DEP292) as fh:
        dep292 = json.load(fh)


    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep287["hosts"] == hosts, "exp287's host frame drifted"
    assert dep288["hosts"] == hosts, "exp288's host frame drifted"
    assert dep289["hosts"] == hosts, "exp289's host frame drifted"
    assert dep292["hosts"] == hosts, "exp292's host frame drifted"
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


    # ---- exp295 delta: THE EXP292 RE-READ (the LEAK FACE's comparison
    #      deposit — the leaky NBOR form's deposited per-host deltas at
    #      g=1.0, the +1.8385 mean face; read, never re-run; fail=STOP
    #      here on the frame) --------------------------------------------
    assert dep292.get("exp") == "exp292_history_dose_source", \
        "exp292's deposit identity drifted"
    assert dep292.get("branch") == "DOSE-REVERSAL x SELF-DOMINANT", \
        "exp292's deposited branch drifted"
    nbor_dep_cell = dep292["ladder"]["cells"]["nbors|g=1"]
    nbor_dep_rows = nbor_dep_cell["delta_rows"]
    assert len(nbor_dep_rows) == 12, \
        "exp292's deposited NBOR g=1.0 delta rows drifted"
    nbor_dep_delta = {r["host"]: float(r["delta_arm_minus_anchor"])
                      for r in nbor_dep_rows}
    assert set(nbor_dep_delta) == set(hosts), \
        "exp292's deposited NBOR delta hosts drifted from the frame"
    nbor_dep_mean = float(
        nbor_dep_cell["mean_paired_delta_arm_minus_anchor"])
    assert abs(nbor_dep_mean - 1.8385) <= 1e-3, \
        (f"exp292's deposited NBOR g=1.0 mean {nbor_dep_mean} drifted "
         "from the pre-registered +1.8385 leak face")
    assert abs(float(np.mean(list(nbor_dep_delta.values())))
               - nbor_dep_mean) <= 1e-9, \
        "exp292's deposited per-host NBOR deltas disagree with their mean"


    # ---- exp292 delta: THE ANCHOR READ (the g=0.0 control column and
    #      the g=1.0 SELF anchor, both from exp289's landed deposit —
    #      the pre-registered "no re-run" form; the anchor's own
    #      provenance (== exp256's deposited substituted errs) is
    #      re-asserted at the assembly; fail=STOP here on the frame) ----
    assert dep289.get("exp") == "exp289_history_register", \
        "exp289's deposit identity drifted"
    assert dep289.get("branch") == "HISTORY-CARRIED", \
        "exp289's deposited branch drifted from HISTORY-CARRIED"
    anchor_rows289 = dep289["rows"]
    assert len(anchor_rows289) == 72, "exp289's anchor battery drifted"
    control_err = {}
    anchor_steps = {}
    anchor_commits = {}
    for _r in anchor_rows289:
        _key = (_r["host"], int(_r["seed"]), _r["row_key"])
        assert _key not in control_err, f"duplicate exp289 anchor row {_key}"
        control_err[_key] = float(_r["err"])
        anchor_steps[_key] = int(_r["walk_steps"])
        anchor_commits[_key] = int(_r["n_commits"])
    assert len(control_err) == 72, \
        "exp289's deposited anchor errs drifted"
    grid289_g1 = {}
    for _r in dep289["grid_rows"]:
        if float(_r["g_ctx"]) == 1.0:
            _key = (_r["host"], int(_r["seed"]), _r["row_key"])
            assert _key not in grid289_g1, \
                f"duplicate exp289 g=1.0 grid row {_key}"
            grid289_g1[_key] = {"err": float(_r["err"]),
                                "trace_sha256": str(_r["trace_sha256"]),
                                "walk_steps": int(_r["walk_steps"]),
                                "n_commits": int(_r["n_commits"])}
    assert len(grid289_g1) == 72, "exp289's g=1.0 grid rows drifted"

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


    # ---- THE TRACED REPLICA: exp289's landed _execute_signed_traced
    #      REUSED VERBATIM (exp142's walk byte-similar + the disclosed
    #      recording additions (a)-(g) + the exp289 activation (h) + the
    #      exp292 read-source plumbing (h')) with exactly ONE exp295
    #      delta, disclosed, pure:
    #      (h'') THE COUPLING'S READ SOURCE: hist_source — "self" reads
    #          phi_history[i] (exp289's landed form VERBATIM, bit-exact
    #          at the default); "nbw" reads the WRITE-SET-WEIGHTED
    #          neighbor mean of phi_history (the exp295 delta — THE
    #          LEAK REPAIR: the weight w_j = 1 if the neighbor j is in
    #          the row's write set — the commit sequence's support,
    #          derived in-executor from the walk order, no new knobs —
    #          else 0; the mean over the weighted support; a
    #          NO-WRITTEN-NEIGHBOR write falls back to the self value,
    #          the fallback counted). A pure projection: the register
    #          itself UNTOUCHED, the population path identical to
    #          exp289's, the RNG stream and the state untouched (the
    #          walk structure is value-level only — the stream face
    #          asserted vs the anchor at the assembly). --

    def _execute_signed_traced(spec, adjacency, seed, op, budget,
                               g_ctx=0.0, a_base=None, hist_source="self"):
        assert hist_source in HISTORY_SOURCES, \
            f"the coupling source {hist_source!r} is not pre-named"
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
        #      (fail=STOP per row): the attribute exists and the
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
                    "reg_init_ok": reg_init_ok,
                    "hist_source": str(hist_source),
                    "n_nbors_reads": 0,
                    "n_nbw_fallbacks": 0}

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
        n_nbors_reads = 0                      # (h') the exp292 delta
        n_nbw_fallbacks = 0                   # (h'') the exp295 delta

        # (h) the activation's class plan (exp258's form: exp208's
        # classes on the plan; T and A_base are g- and source-
        # independent, so the row sets match 1:1 across the whole
        # battery). Computed ONLY when the coupling is armed — zero
        # deviation at g_ctx == 0.0.
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
        # exp295 delta: THE ROW'S WRITE SET — the commit sequence's
        # support (the set of cells this row's walk commits; the NBW
        # weights derive ONLY from this set — no new knobs)
        write_set = set(int(oi) for oi, _osrc in order)

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
            # ---- (h) THE ACTIVATION: the history blend (ZERO at
            #      g_ctx == 0.0) — exp258's canon-boundary restriction
            #      verbatim; the read source is the register via
            #      hist_source: "self" == the cell's OWN last commit
            #      (exp289's landed form VERBATIM); "nbw" == the
            #      exp295 delta: the WRITE-SET-WEIGHTED neighbor mean
            #      of phi_history (the weights derive ONLY from the
            #      row's write set — the commit sequence's support;
            #      the mean taken at the write time, the walk order's
            #      causal face; the fallback disclosed below) ----------
            written = theta_new
            if g_ctx > 0.0 and cls[i] == 0:
                if hist_source == "nbw":         # exp295 delta
                    nbr_idx = np.where(np.abs(adjacency[i]) > 0)[0]
                    assert nbr_idx.size > 0, \
                        (f"the NBW support is empty at cell {i} — the "
                         "weighted neighbor mean is undefined")
                    written_nbrs = [int(j) for j in nbr_idx
                                    if int(j) in write_set]
                    if written_nbrs:
                        n_nbors_reads += 1
                        # the weighted mean: w_j = 1 for the neighbors
                        # in the row's write set (the commit sequence's
                        # support — their registers hold their TRUE
                        # commit history), 0 otherwise — the mean over
                        # the weighted support
                        src_val = float(
                            sum(float(c.phi_history[j])
                                for j in written_nbrs)
                            / float(len(written_nbrs)))
                    else:
                        # the pre-named fallback: NO written neighbors
                        # — the self value (disclosed; the fallback
                        # count recorded per row)
                        src_val = float(c.phi_history[i])
                        n_nbw_fallbacks += 1

                else:                            # exp289's form VERBATIM
                    src_val = float(c.phi_history[i])
                written = ((1.0 - g_ctx) * theta_new
                           + g_ctx * src_val)
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
        # ---- (g) THE REGISTER AT THE WALK'S END (fail=STOP per row):
        #      the register SURVIVED the walk + the settle; on the
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
        out["hist_source"] = str(hist_source)          # (h') exp292 delta
        out["n_nbors_reads"] = int(n_nbors_reads)      # (h') exp292 delta
        out["n_nbw_fallbacks"] = int(n_nbw_fallbacks)  # (h'') exp295 delta

        return out

    # ---- the state-carrying replica read (exp256's _scoped_row_read_
    #      state form VERBATIM with the traced + budgeted + register-
    #      live executor call; exp292 delta: the hist_source passthrough)
    def _scoped_row_read_traced(spec, med, seed, fmax, budget,
                                g_ctx=0.0, a_base=None, hist_source="self"):
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
                                         a_base=a_base,
                                         hist_source=hist_source)
        out["rho"] = rho
        out["branch"] = branch
        return out

    # ---- one ARM-row decode (the exp289 grid-row decode form VERBATIM;
    #      the register + commit bookkeeping asserted fail=STOP; the
    #      exp288 class decomposition carried for the pooled-R_max audit
    #      face; the g=0.0 anchors DO NOT apply at g > 0 — the blend is
    #      the pre-registered deviation — and the structural stream face
    #      (the walked count, the commit count) is asserted against the
    #      ANCHOR DEPOSIT at the assembly; exp292 delta: the row flags
    #      for the G1 arm-cell counts + the hist_source/n_nbors_reads
    #      passthrough) ----------------------------------------------------
    def _decode_grid_row(host, row_key, spec, med, seed, fmax, g, A_base,
                         hist_source="self"):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET,
                                      g_ctx=g, a_base=A_base,
                                      hist_source=hist_source)
        assert out["hist_source"] == hist_source, \
            "the coupling source tag drifted"
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
        all_finite = bool(all(np.isfinite(trace)))
        assert all_finite, \
            f"{host} {row_key} s{seed} g{g}: non-finite trace entry"
        final = trace[-1]
        assert final > 0.0, f"{host} {row_key} s{seed} g{g}: final RMS == 0"
        thresh = 2.0 * final
        conv = None
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        conv_ok = bool(conv is not None and 0 <= conv < steps)
        assert conv_ok, \
            f"{host} {row_key} s{seed} g{g}: no convergence point"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        commits = out["commits"]
        n_commits = len(commits)
        commit_count_ok = bool(n_commits == steps == len(trace))
        assert commit_count_ok, \
            f"{host} {row_key} s{seed} g{g}: the commit count drifted"
        idxs = [int(rec[0]) for rec in commits]
        commits_unique_ok = bool(len(set(idxs)) == n_commits)
        assert commits_unique_ok, \
            f"{host} {row_key} s{seed} g{g}: a cell written twice"
        coverage_ok = bool(out["coverage_ok"])
        assert coverage_ok, \
            f"{host} {row_key} s{seed} g{g}: the coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        commits_finite_ok = bool(all(np.isfinite(v) for v in vals))
        assert commits_finite_ok, \
            f"{host} {row_key} s{seed} g{g}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        census_ok = bool(sum(census_src.values()) == n_commits
                         and set(tags) <= set(COMMIT_SOURCES))
        assert census_ok, \
            f"{host} {row_key} s{seed} g{g}: the census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        digests_ok = bool(len(commit_sha) == 64)
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed} g{g}: non-finite cvt_rms"

        # ---- the register face at the arm point (the same fail=STOP
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
        #      for the pooled-R_max audit face at the best arm-cell;
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
               "g_ctx": float(g), "hist_source": str(hist_source),
               "pert": P3, "medium": "base",
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "trace_len_ok": trace_len_ok, "finite_ok": all_finite,
               "commit_count_ok": commit_count_ok,
               "commits_unique_ok": commits_unique_ok,
               "commits_finite_ok": commits_finite_ok,
               "census_ok": census_ok, "digests_ok": digests_ok,
               "conv_ok": conv_ok,
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
               "n_nbors_reads": int(out["n_nbors_reads"]),
               "n_nbw_fallbacks": int(out["n_nbw_fallbacks"]),
               "register": reg,
               "masks_disjoint_ok": masks_disjoint_ok,
               "decomp": decomp, "accounting_ok": ident_ok,
               "fracs_ok": fracs_ok, "partition_ok": partition_ok,
               "n_write": n_write, "sum_e": float(e.sum()),
               "sum_sq_e": total_sq}
        return rec

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; exp288's 25 records + exp288's own inputs record
    #      (6 sha records) = 31; exp289's landed form VERBATIM) ----------
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

    # ---- THE SHADOW TEST SUITE (the exp289 form: python3 -m
    #      tests.run_tests from the repo root; THE SHADOW PATH
    #      DISCLOSED: the suite runs in a separate interpreter — a
    #      shadow process importing the ON-DISK ported collective.py —
    #      so the additive port's legacy-call-site proof is made
    #      against the file this commit ships, not against this
    #      process's pinned in-memory state; the subprocess's own floor
    #      state is unpinned by this process; recorded under the
    #      integrity block, never gating in exp292) -----------------------
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
    #      exp288/exp289 form VERBATIM, every rebuild bit-asserted
    #      against exp243's OWN records; shared by both passes —
    #      deterministic) ---------------------------------------------------
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

        # exp256's 72 rows — the substituted records the anchor chain reads
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


    # ---- PASS 1 (the SELF-R ladder — the refined dose face): the
    #      sha-asserted rebuild + the shadow test suite + 4 doses x 72
    #      fresh decodes (288) at the production budget with the
    #      register live and the coupling reading phi_history[i]
    #      (exp289's landed form); the G1 ANCHOR asserted fail=STOP per
    #      row at g=1.0: the errs + the trace shas == exp289's deposited
    #      g=1.0 grid rows BIT-EXACT ------------------------------------
    def _compute_pass1():
        _LOCK_LOG.clear()
        rb = _rebuild()
        suite = _run_test_suite()
        bases = rb["bases"]
        rows_out: list = []
        n_anchor_err = 0
        n_anchor_trace = 0
        for g in SELF_LADDER:
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_grid_row(
                            k, rk, ctx["deep"][inst]["spec"], med, s,
                            ctx["fmax"], g, ctx["A"], hist_source="self")
                        assert rec["hist_source"] == "self", \
                            "the SELF arm's source tag drifted"
                        assert rec["n_nbors_reads"] == 0, \
                            "the SELF arm performed a neighbor read"
                        assert rec["n_nbw_fallbacks"] == 0, \
                            "the SELF arm recorded an NBW fallback"
                        if g == 1.0:
                            # exp295 delta: THE G1 ANCHOR (fail=STOP per
                            # row): the SELF g=1.0 errs + the trace shas
                            # == exp289's deposited g=1.0 rows BIT-EXACT
                            # (the same-walk discipline)
                            a = grid289_g1[(k, s, rk)]
                            err_ok = bool(rec["err"] == a["err"])
                            assert err_ok, \
                                (f"{k} {rk} s{s}: the SELF g=1.0 err "
                                 f"{rec['err']} drifted from exp289's "
                                 f"deposited {a['err']} — the G1 anchor "
                                 "REFUTED")
                            ts_ok = bool(rec["trace_sha256"]
                                         == a["trace_sha256"])
                            assert ts_ok, \
                                (f"{k} {rk} s{s}: the SELF g=1.0 trace "
                                 "sha drifted from exp289's deposited — "
                                 "not the same walk")
                            n_anchor_err += int(err_ok)
                            n_anchor_trace += int(ts_ok)
                        rows_out.append(rec)
                hs = [r for r in rows_out
                      if r["host"] == k and r["g_ctx"] == g]
                print(f"  [pass1 SELF-R g={g} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | hist writes "
                      f"{hs[0]['n_hist_writes']}/row",
                      flush=True)
        assert len(rows_out) == 288, \
            f"pass1 produced {len(rows_out)} rows != 288"
        assert len(_LOCK_LOG) == 288, \
            f"the S* lock count {len(_LOCK_LOG)} != 288 reads"
        assert n_anchor_err == 72 and n_anchor_trace == 72, \
            "the G1 anchor counts drifted"
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
                     "exp142_sha256": exp142_sha_entry,
                     "exp289_module_sha256": exp289_sha_entry,
                     "exp292_module_sha256": exp292_sha_entry}
        return {"pass": 1, "source": "self", "rows": rows_out,
                "anchor_289": {"n_err_ok": int(n_anchor_err),
                               "n_trace_ok": int(n_anchor_trace)},
                "integrity": integrity, "test_suite": suite,
                "ro_before": ro_before, "lock_reads": len(_LOCK_LOG),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry}



    # ---- PASS 2 (the NBW ladder — the leak face): the sha-asserted
    #      rebuild + 3 doses x 72 fresh decodes (216) with the coupling
    #      reading the WRITE-SET-WEIGHTED neighbor mean of phi_history
    #      (the leak repair); the register face + the bookkeeping
    #      asserted fail=STOP per row (the population path identical to
    #      exp289's — the read is a pure projection; the armed-write
    #      partition — the weighted reads + the fallbacks == the blend
    #      count — asserted per row) -------------------------------------
    def _compute_pass2():
        _LOCK_LOG.clear()
        rb = _rebuild()
        bases = rb["bases"]
        rows_out: list = []
        for g in NBW_LADDER:
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_grid_row(
                            k, rk, ctx["deep"][inst]["spec"], med, s,
                            ctx["fmax"], g, ctx["A"], hist_source="nbw")
                        assert rec["hist_source"] == "nbw", \
                            "the NBW arm's source tag drifted"
                        # exp295 delta: the armed-write partition face —
                        # every armed write EITHER performed the
                        # weighted neighbor read OR fell back to the
                        # self value (fail=STOP per row)
                        assert rec["n_nbors_reads"] \
                            + rec["n_nbw_fallbacks"] \
                            == rec["n_hist_writes"], \
                            (f"{k} {rk} s{s} g{g}: the NBW armed-write "
                             "partition drifted — the weighted reads + "
                             "the fallbacks != the blend count")
                        rows_out.append(rec)
                hs = [r for r in rows_out
                      if r["host"] == k and r["g_ctx"] == g]
                print(f"  [pass2 NBW g={g} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | hist writes "
                      f"{hs[0]['n_hist_writes']}/row | fallbacks "
                      f"{hs[0]['n_nbw_fallbacks']}/row",
                      flush=True)
        assert len(rows_out) == 216, \
            f"pass2 produced {len(rows_out)} rows != 216"
        assert len(_LOCK_LOG) == 216, \
            f"the S* lock count {len(_LOCK_LOG)} != 216 reads"
        return {"pass": 2, "source": "nbw", "rows": rows_out,
                "ro_before": ro_before, "lock_reads": len(_LOCK_LOG),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry}



    # ---- THE ASSEMBLY (a pure function of the two passes' payloads +
    #      the deposits; the merge path and the in-process path share it
    #      verbatim; the merge NEVER re-decodes; exp295 deltas: the
    #      control column IS exp289's deposited anchor (read, never
    #      re-run); the cells dict carries delta_rows as this assembly
    #      reads it — exp292's landed lesson; the branch faces are the
    #      PEAK dose face and the LEAK face vs exp292's deposited NBOR
    #      deltas, recorded independently) ---------------------------------
    def _assemble(p1, p2, run_form):
        assert p1["pass"] == 1 and p2["pass"] == 2, "payload swap"
        assert p1["source"] == "self" and p2["source"] == "nbw", \
            "the arms' sources swapped"
        assert p1["ro_before"] == p2["ro_before"] == ro_before, \
            "ro_before drifted across passes"
        assert p1["port_sha256"] == p2["port_sha256"] == _sha(PORT_FILE), \
            "the ported collective.py drifted mid-run"
        assert p1["exp142_sha256"] == p2["exp142_sha256"] \
            == _sha(EXP142_FILE), \
            "exp142 was modified — the pre-registered NOT-modified rule"
        rows_self = p1["rows"]
        rows_nbw = p2["rows"]
        assert len(rows_self) == 288 and len(rows_nbw) == 216, \
            "the arm batteries drifted"
        integrity = p1["integrity"]
        counts = integrity["counts"]
        chains = integrity["provenance_chains"]
        suite = p1["test_suite"]

        # ---- the CONTROL COLUMN's provenance (fail=STOP): exp289's
        #      deposited anchor errs == exp256's deposited substituted
        #      errs 72/72 (the anchor chain: exp256 -> exp289's landed
        #      anchor -> this module's g=0.0 control — READ, never run)
        dep_sub = {}
        for r in dep256["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                dep_sub[(r["host"], int(r["seed"]),
                         i["row_key"])] = float(i["err"])
        n_control_provenance = 0
        for key, err_val in control_err.items():
            ok = bool(err_val == dep_sub[key])
            assert ok, \
                (f"{key}: exp289's deposited anchor err drifted from "
                 "exp256's deposited substituted err — the control "
                 "column's provenance broke")
            n_control_provenance += int(ok)
        assert n_control_provenance == 72, \
            "the control column's provenance drifted"
        control_means = {}
        for h in hosts:
            hs = [v for (hh, _ss, _rr), v in control_err.items()
                  if hh == h]
            assert len(hs) == 6, f"{h}: the control rows drifted"
            control_means[h] = float(np.mean(hs))

        # ---- THE STREAM FACE (the pairing's precondition; the exp289
        #      form carried to BOTH arms): per arm row the walked count +
        #      the commit count == the anchor's (the deposited g=0.0
        #      walk); the blend count constant across the 7 arm-cells ----
        stream_ok_rows = 0
        reg_ok_rows = 0
        hist_const_counter: dict = {}
        for rows, src_name in ((rows_self, "self"), (rows_nbw, "nbw")):
            for r in rows:
                key = (r["host"], int(r["seed"]), r["row_key"])
                st_ok = bool(r["walk_steps"] == anchor_steps[key]
                             and r["n_commits"] == anchor_commits[key])
                assert st_ok, \
                    (f"{key} {src_name} g={r['g_ctx']}: the walked count "
                     "/ commit count moved with the arm — the stream "
                     "face drifted (the pairing is broken)")
                stream_ok_rows += int(st_ok)
                reg_ok_rows += int(all(r["register"][kk] for kk in
                                       ("present_ok", "init_ok",
                                        "replay_ok", "complement_ok",
                                        "finite_ok")))
                hist_const_counter.setdefault(
                    key, set()).add(int(r["n_hist_writes"]))
        hist_const_rows = sum(1 for v in hist_const_counter.values()
                              if len(v) == 1)
        assert hist_const_rows == 72, \
            "the per-row blend count moved across the arms/doses"
        assert stream_ok_rows == 504 and reg_ok_rows == 504, \
            "the arms' stream/register face drifted"

        # ---- the per ARM-CELL tables (4 SELF-R doses + 3 NBW doses):
        #      the 72-row mean errs, the per-host paired deltas (BOTH
        #      signings recorded — the anchor-minus-arm form is the
        #      house improvement form, exp290's disclosed convention),
        #      the worst-err face vs the 6.0 bar, the G1 arm-cell counts
        cells = {}
        cell_g2: dict = {}
        for src_name, rows, arm_ladder in (
                ("self", rows_self, SELF_LADDER),
                ("nbw", rows_nbw, NBW_LADDER)):
            for g in arm_ladder:
                crows = [r for r in rows if r["g_ctx"] == g]
                assert len(crows) == 72, \
                    f"{src_name} g={g}: the 72-row battery drifted"
                host_means = {}
                for h in hosts:
                    hs = [r for r in crows if r["host"] == h]
                    assert len(hs) == 6, \
                        f"{src_name} g={g} {h}: the 6 rows drifted"
                    host_means[h] = float(np.mean(
                        [r["err"] for r in hs]))
                worst = max(crows, key=lambda r: r["err"])
                drows = []
                for h in hosts:
                    impr = float(control_means[h] - host_means[h])
                    drows.append({
                        "host": h, "outlier": bool(h in outliers),
                        "mean_err_cell": host_means[h],
                        "mean_err_control": control_means[h],
                        "delta_anchor_minus_arm": impr,
                        "delta_arm_minus_anchor": float(-impr),
                        "improved_strict": bool(impr > 0.0)})
                mean_paired_impr = float(np.mean(
                    [d["delta_anchor_minus_arm"] for d in drows]))
                tot_err_delta = float(sum(
                    d["delta_arm_minus_anchor"] for d in drows))
                ck = f"{src_name}|g={g:g}"
                cells[ck] = {
                    "source": src_name, "g_ctx": float(g), "n_rows": 72,
                    "host_mean_err": host_means,
                    "mean_err_all_hosts": float(np.mean(
                        [r["err"] for r in crows])),
                    "mean_paired_delta_anchor_minus_arm": mean_paired_impr,
                    "mean_paired_delta_arm_minus_anchor":
                        float(-mean_paired_impr),
                    "total_delta_arm_minus_anchor": tot_err_delta,
                    "n_improved": int(sum(d["improved_strict"]
                                          for d in drows)),
                    "worst_err": float(worst["err"]),
                    "worst_row": {"host": worst["host"],
                                  "seed": int(worst["seed"]),
                                  "row_key": worst["row_key"]},
                    "worst_under_bar": bool(worst["err"] < ERR_BAR),
                    "bar": ERR_BAR,
                    "bar_note": ("the anchor's 6.0 bar, unchanged — "
                                 "audit-only, never gating"),
                    "n_verified": int(sum(r["verified"] for r in crows)),
                    "register_ok_rows": int(sum(
                        all(r["register"][kk] for kk in
                            ("present_ok", "init_ok", "replay_ok",
                             "complement_ok", "finite_ok"))
                        for r in crows)),
                    "mean_cvt": {h: float(np.mean(
                        [r["cvt_rms"] for r in crows if r["host"] == h]))
                        for h in hosts},
                    "counts": {
                        "n_finite": int(sum(r["finite_ok"]
                                            for r in crows)),
                        "n_a3": int(sum(r["a3_ok"] for r in crows)),
                        "n_trace_len": int(sum(r["trace_len_ok"]
                                               for r in crows)),
                        "n_commit_count": int(sum(r["commit_count_ok"]
                                                  for r in crows))},
                    "n_nbw_fallbacks_total": int(sum(
                        r["n_nbw_fallbacks"] for r in crows)),
                    "n_rows_with_fallback": int(sum(
                        bool(r["n_nbw_fallbacks"]) for r in crows)),
                    "outliers_H3_H5": {
                        d["host"]: {
                            "delta_anchor_minus_arm":
                                d["delta_anchor_minus_arm"],
                            "delta_arm_minus_anchor":
                                d["delta_arm_minus_anchor"],
                            "improved_strict": d["improved_strict"]}
                        for d in drows if d["host"] in outliers},
                    "delta_rows": drows}
                # exp295 delta: the PER-ARM-CELL G2 tallies (exp292's
                # landed diagnosis honored — the register-replay scope
                # is the 72-row arm-cell, not a pooled per-arm count)
                cell_g2[ck] = {
                    "n_rows": len(crows),
                    "n_register_replay_ok": int(sum(
                        r["register"]["replay_ok"] for r in crows)),
                    "n_register_complement_ok": int(sum(
                        r["register"]["complement_ok"] for r in crows)),
                    "n_register_finite_ok": int(sum(
                        r["register"]["finite_ok"] for r in crows)),
                    "n_register_ok_rows": cells[ck]["register_ok_rows"]}

        # ---- THE DOSE FACE (the SELF-R refined curve; the pre-named
        #      PEAK-FLAT bar: the |delta| differences among {0.75, 1.0,
        #      1.25} are all < the 0.01 mV plateau bar on >= 10/12 hosts
        #      — a plateau; PEAK-SHARP otherwise — a distinct optimum;
        #      the differences are sign-agnostic (both signings recorded
        #      per row above); the argbest dose recorded host-wise,
        #      audit-only, the smaller-dose tie-break) -------------------
        impr = {g: {d["host"]: d["delta_anchor_minus_arm"]
                    for d in cells[f"self|g={g:g}"]["delta_rows"]}
                for g in SELF_LADDER}
        peak_rows = []
        n_flat = 0
        for h in hosts:
            d075 = impr[0.75][h]
            d100 = impr[1.0][h]
            d125 = impr[1.25][h]
            diffs = (abs(d075 - d100), abs(d100 - d125),
                     abs(d075 - d125))
            flat = bool(all(dd < PLATEAU_EPS for dd in diffs))
            n_flat += int(flat)
            best_g = sorted(SELF_LADDER,
                            key=lambda gg: (-impr[gg][h], gg))[0]
            peak_rows.append({
                "host": h, "outlier": bool(h in outliers),
                "impr_g0.75": d075, "impr_g1.0": d100,
                "impr_g1.25": d125, "impr_g1.5": impr[1.5][h],
                "diff_0.75_1.0": diffs[0],
                "diff_1.0_1.25": diffs[1],
                "diff_0.75_1.25": diffs[2],
                "plateau_clause": flat,
                "argbest_dose": float(best_g),
                "argbest_impr": float(impr[best_g][h])})
        if n_flat >= DOSE_MIN_HOSTS:
            dose_face = "PEAK-FLAT"
        else:
            dose_face = "PEAK-SHARP"

        # ---- THE LEAK FACE (the NBW form at g=1.0 vs exp292's deposited
        #      NBOR deltas — the leaky form's +1.8385 mean face; the
        #      arm-minus-anchor err-delta form, exp292's landed
        #      convention): LEAK-CONFIRMED iff the NBW delta improves vs
        #      the NBOR deposited delta by > the 0.05 mV margin on >=
        #      10/12 hosts (the leak WAS the failure mode);
        #      LEAK-NOT-SUFFICIENT otherwise (recorded honestly) --------
        nbw_delta = {d["host"]: d["delta_arm_minus_anchor"]
                     for d in cells["nbw|g=1"]["delta_rows"]}
        leak_rows = []
        n_leak = 0
        for h in hosts:
            md_nbwh = nbw_delta[h]
            md_nbor = nbor_dep_delta[h]
            improves = bool(md_nbwh < md_nbor - MARGIN)
            n_leak += int(improves)
            leak_rows.append({
                "host": h, "outlier": bool(h in outliers),
                "nbw_delta_arm_minus_anchor": md_nbwh,
                "nbor_deposited_delta_arm_minus_anchor": md_nbor,
                "nbw_improvement_vs_nbor": float(md_nbor - md_nbwh),
                "improves_over_leaky_by_margin": improves})
        if n_leak >= DOSE_MIN_HOSTS:
            leak_face = "LEAK-CONFIRMED"
        else:
            leak_face = "LEAK-NOT-SUFFICIENT"
        md_nbw_g1 = float(
            cells["nbw|g=1"]["mean_paired_delta_arm_minus_anchor"])

        # ---- THE AUDIT FACE: exp288's pooled-R_max class-blindness
        #      re-read at the leak face's arm-cell nbw|g=1 (the battery's
        #      pivotal cell — exp292's best-shared-dose machinery not
        #      pre-named in exp295; never gating) -------------------------
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
                                    "never gating in exp295")}
        best_cell_rows = [r for r in rows_nbw if r["g_ctx"] == 1.0]
        assert len(best_cell_rows) == 72, "the leak arm-cell drifted"
        rmax_face_best = _pooled_face(best_cell_rows)
        rmax_face_anchor = {"source": "exp288's deposited face (READ-ONLY)",
                            "branch": dep288["branch"],
                            "per_host_R_max": integrity["exp288_reread"]
                            ["per_host_R_max"]}

        # ---- the per-arm G2 counts (the register face + the commit
        #      bookkeeping, at the per-arm scope) --------------------------
        def _arm_g2_counts(rows):
            return {
                "n_rows": len(rows),
                "n_register_present_ok": int(sum(
                    r["register"]["present_ok"] for r in rows)),
                "n_register_init_ok": int(sum(
                    r["register"]["init_ok"] for r in rows)),
                "n_register_replay_ok": int(sum(
                    r["register"]["replay_ok"] for r in rows)),
                "n_register_complement_ok": int(sum(
                    r["register"]["complement_ok"] for r in rows)),
                "n_register_finite_ok": int(sum(
                    r["register"]["finite_ok"] for r in rows)),
                "n_commits_count_ok": int(sum(r["commit_count_ok"]
                                              for r in rows)),
                "n_commits_unique_ok": int(sum(r["commits_unique_ok"]
                                               for r in rows)),
                "n_coverage_ok": int(sum(r["coverage_ok"] for r in rows)),
                "n_commits_finite_ok": int(sum(r["commits_finite_ok"]
                                               for r in rows)),
                "n_census_ok": int(sum(r["census_ok"] for r in rows)),
                "n_digests_ok": int(sum(r["digests_ok"] for r in rows)),
                "n_a3_ok": int(sum(r["a3_ok"] for r in rows)),
                "n_conv_ok": int(sum(r["conv_ok"] for r in rows))}
        g2_counts = {"self": _arm_g2_counts(rows_self),
                     "nbw": _arm_g2_counts(rows_nbw)}

        # ---- the tallies -------------------------------------------------
        n_a3_cells = {ck: cells[ck]["counts"]["n_a3"] for ck in cells}

        g1 = dict(counts)
        g1.update({
            "n_anchor289_err_ok": int(p1["anchor_289"]["n_err_ok"]),
            "n_anchor289_trace_ok": int(p1["anchor_289"]["n_trace_ok"]),
            "arm_cell_counts": {ck: cells[ck]["counts"] for ck in cells},
            "n_a3_per_cell": n_a3_cells,
            "lock_reads_pass1": int(p1["lock_reads"]),
            "lock_reads_pass2": int(p2["lock_reads"]),
            "lock_reads_total": int(p1["lock_reads"] + p2["lock_reads"]),
            "floor_asserted_in_process": True,
            "reader_pin_floor": READER_PIN_FLOOR,
            "reader_pin_disclosure": (
                "N/A — no stress arm in exp295; the floor -60.0 "
                "throughout, asserted at setup and re-asserted at exit "
                "(the exp290 -35.0 reader-line pin does not apply)")})

        g3 = {"branch_dose": dose_face, "branch_leak": leak_face,
              "n_rows_total": len(rows_self) + len(rows_nbw),
              "n_stream_ok_rows": stream_ok_rows,
              "n_register_ok_rows": reg_ok_rows,
              "n_hist_const_rows": hist_const_rows,
              "n_control_provenance_ok": n_control_provenance,
              "peak_clause_counts": {
                  "n_plateau_clause": n_flat,
                  "DOSE_MIN_HOSTS": DOSE_MIN_HOSTS,
                  "PLATEAU_EPS": PLATEAU_EPS},
              "leak_clause_counts": {
                  "n_improves_over_leaky": n_leak,
                  "DOSE_MIN_HOSTS": DOSE_MIN_HOSTS,
                  "MARGIN": MARGIN},
              "nbor_deposited_mean_g1": nbor_dep_mean,
              "md_nbw_g1": md_nbw_g1,
              "n_improved_per_cell": {ck: cells[ck]["n_improved"]
                                      for ck in cells},
              "lock_reads_total": int(p1["lock_reads"]
                                      + p2["lock_reads"])}

        return {"hosts": hosts, "outliers": outliers, "cluster": cluster,
                "rows_self": rows_self, "rows_nbw": rows_nbw,
                "cells": cells, "cell_g2": cell_g2,
                "peak_rows": peak_rows, "leak_rows": leak_rows,
                "control_means": control_means,
                "n_control_provenance": n_control_provenance,
                "dose_face": dose_face, "leak_face": leak_face,
                "n_flat": n_flat, "n_leak": n_leak,
                "nbor_dep_mean": nbor_dep_mean, "md_nbw_g1": md_nbw_g1,
                "rmax_face_best": rmax_face_best,
                "rmax_face_anchor": rmax_face_anchor,
                "integrity": integrity, "test_suite": suite,
                "g1": g1, "g2_counts": g2_counts, "g3": g3,
                "run_form": run_form}



    def _payload_sha(p):
        return hashlib.sha256(
            json.dumps(p, sort_keys=True).encode()).hexdigest()

    # ---- the mode dispatch (the pre-named RUN clause: the default is
    #      the IN-PROCESS form (the whole sequence, may exceed the 560 s
    #      cap); the pre-named sandbox form is the CHECKPOINT-SPLIT
    #      EXP295_MODE=pass1 (the SELF-R ladder, 288 decodes) | pass2
    #      (the NBW ladder, 216 decodes) | merge — each pass a separate
    #      process, the merge assembling + evaluating the gates once and
    #      NEVER re-decoding) --------------------------------------------
    _MODE = os.environ.get("EXP295_MODE", "")
    _CK = {1: os.path.join(ROOT, "results",
                           ".exp295_pass1.checkpoint.json"),
           2: os.path.join(ROOT, "results",
                           ".exp295_pass2.checkpoint.json")}

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
        assert _sha(EXP289_FILE) == exp289_sha_entry, \
            "exp289's landed instrument module drifted after the work"
        assert _sha(EXP292_FILE) == exp292_sha_entry, \
            "exp292's landed instrument module (the base) drifted after " \
            "the work"

    if _MODE in ("pass1", "pass2"):
        tag = 1 if _MODE == "pass1" else 2
        if tag == 1:
            print("=== exp295 pass1: THE SELF-R LADDER (the refined dose "
                  "face; the G1 anchor vs exp289's deposited g=1.0 "
                  "rows) ===")
            payload = _compute_pass1()
        else:
            print("=== exp295 pass2: THE NBW LADDER (the leak-repaired "
                  "neighbor form; the write-set-weighted mean over the "
                  "commit sequence's support) ===")
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
        print("=== exp295: THE DOSE CURVE REFINED AND THE NBOR LEAK "
              "REPAIR ===")
        print(f"  battery: 4 SELF-R doses + 3 NBW doses x (12 hosts x 3 "
              f"seeds {list(SEEDS_RUN)} x 2 deep instances at n={N400}) = "
              f"504 decodes at the production budget {BUDGET}; the g=0.0 "
              f"control is exp289's deposited anchor (read, never "
              f"re-run)")
        p1 = _compute_pass1()
        p2 = _compute_pass2()
        sa = _payload_sha(p1)
        sb = _payload_sha(p2)
        core = _assemble(p1, p2, "in-process default (one invocation)")
        run_form = "in-process default (one invocation)"

    # ---- the gate assembly (evaluated exactly once) ---------------------
    g1 = core["g1"]
    g2_counts = core["g2_counts"]
    cell_g2 = core["cell_g2"]
    g3 = core["g3"]
    integrity = core["integrity"]
    chains = integrity["provenance_chains"]
    suite = core["test_suite"]
    cells = core["cells"]
    dose_face = core["dose_face"]
    leak_face = core["leak_face"]
    n_flat = core["n_flat"]
    n_leak = core["n_leak"]
    nbor_dep_mean = core["nbor_dep_mean"]
    md_nbw_g1 = core["md_nbw_g1"]
    control_means = core["control_means"]
    peak_rows = core["peak_rows"]
    leak_rows = core["leak_rows"]
    rmax_best = core["rmax_face_best"]
    rmax_anchor = core["rmax_face_anchor"]
    rows_nbw_all = core["rows_nbw"]
    nbw_fallback_total = int(sum(r["n_nbw_fallbacks"]
                                 for r in rows_nbw_all))
    nbw_armed_total = int(sum(r["n_hist_writes"] for r in rows_nbw_all))
    # (ro_before is the module-level record; both passes asserted it at
    #  _assemble; the exit re-check lands below)
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(ro_before.values()))
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at the gate assembly"

    n_per_cell_ok = bool(len(cells) == 7 and all(
        all(v == 72 for v in cells[ck]["counts"].values())
        for ck in cells))
    g1_pass = bool(
        g1["n_anchor289_err_ok"] == 72
        and g1["n_anchor289_trace_ok"] == 72
        and n_per_cell_ok
        and g1["lock_reads_pass1"] == 288
        and g1["lock_reads_pass2"] == 216
        and g1["lock_reads_total"] == 504
        and ro_unchanged)
    g2_pass = bool(
        all(cell_g2[ck]["n_register_replay_ok"] == 72
            and cell_g2[ck]["n_register_complement_ok"] == 72
            and cell_g2[ck]["n_register_ok_rows"] == 72
            for ck in cells)
        and all(v == 288 for kk, v in g2_counts["self"].items()
                if kk != "n_rows")
        and all(v == 216 for kk, v in g2_counts["nbw"].items()
                if kk != "n_rows")
        and g2_counts["self"]["n_rows"] == 288
        and g2_counts["nbw"]["n_rows"] == 216
        and all("n_nbw_fallbacks" in r for r in rows_nbw_all))
    g3_pass = bool(
        g3["branch_dose"] in ("PEAK-FLAT", "PEAK-SHARP")
        and g3["branch_leak"] in ("LEAK-CONFIRMED",
                                  "LEAK-NOT-SUFFICIENT")
        and g3["n_rows_total"] == 504
        and g3["n_stream_ok_rows"] == 504
        and g3["n_register_ok_rows"] == 504
        and g3["n_hist_const_rows"] == 72
        and g3["n_control_provenance_ok"] == 72
        and g3["lock_reads_total"] == 504)


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


    branch = f"{dose_face} x {leak_face}"
    if dose_face == "PEAK-FLAT":
        dose_text = (
            f"PEAK-FLAT — the |delta| differences among {{0.75, 1.0, "
            f"1.25}} are all < the {PLATEAU_EPS} mV plateau bar on "
            f"{n_flat}/12 hosts (>= the pre-named {DOSE_MIN_HOSTS}): the "
            f"carrier's optimum is a plateau — exp289's grid stopped "
            f"inside it, the reversal past it is gentle")
    else:
        dose_text = (
            f"PEAK-SHARP — the plateau clause met on only {n_flat}/12 "
            f"hosts (< the pre-named {DOSE_MIN_HOSTS}): a distinct "
            f"optimum at the refined grid — the argbest dose is "
            f"recorded host-wise (audit-only)")
    if leak_face == "LEAK-CONFIRMED":
        leak_text = (
            f"LEAK-CONFIRMED — the NBW g=1.0 delta improves vs exp292's "
            f"deposited NBOR delta (the leaky mean {nbor_dep_mean:+.4f}) "
            f"by > the {MARGIN} mV margin on {n_leak}/12 hosts (>= the "
            f"pre-named {DOSE_MIN_HOSTS}): the leak WAS the failure "
            f"mode — the unwritten neighbors' spec-install register "
            f"poisoned the naive social form")
    else:
        leak_text = (
            f"LEAK-NOT-SUFFICIENT — the NBW g=1.0 delta improves vs "
            f"exp292's deposited NBOR delta (the leaky mean "
            f"{nbor_dep_mean:+.4f}) by > the {MARGIN} mV margin on only "
            f"{n_leak}/12 hosts (< the pre-named {DOSE_MIN_HOSTS}): the "
            f"social form's failure is deeper than the leak — recorded "
            f"honestly")

    verdict_body = (
        f"{dose_text}; {leak_text}"
        f" | THE DELTAS vs the g=0.0 anchor (exp289's deposited "
        f"control, READ not re-run; the anchor's provenance == "
        f"exp256's deposited errs re-asserted 72/72): "
        + "; ".join(
            f"{src} g={g}: {cells[f'{src}|g={g:g}']['n_improved']}/12 "
            f"improved, mean paired arm-minus-anchor "
            f"{cells[f'{src}|g={g:g}']['mean_paired_delta_arm_minus_anchor']:+.4f}"
            for src, lad in (("self", SELF_LADDER), ("nbw", NBW_LADDER))
            for g in lad)
        + f" | the per-host mean errs at the leak face's arm-cell "
          f"(nbw g=1.0) within "
          f"[{min(cells['nbw|g=1']['host_mean_err'].values()):.3f}, "
          f"{max(cells['nbw|g=1']['host_mean_err'].values()):.3f}] "
          f"vs the control within "
          f"[{min(control_means.values()):.3f}, "
          f"{max(control_means.values()):.3f}]"
          f" | the worst-err faces vs the 6.0 bar (unchanged, audit-"
          f"only): "
        + "; ".join(
            f"{src} g={g}: {cells[f'{src}|g={g:g}']['worst_err']:.2f}"
            f"{' <bar' if cells[f'{src}|g={g:g}']['worst_under_bar'] else ' >=BAR'}"
            for src, lad in (("self", SELF_LADDER), ("nbw", NBW_LADDER))
            for g in lad)
        + f" | THE G1 ANCHOR: the SELF-R g=1.0 errs reproduce exp289's "
          f"deposited g=1.0 errs BIT-EXACT "
          f"({g1['n_anchor289_err_ok']}/72) with the trace shas "
          f"({g1['n_anchor289_trace_ok']}/72) — the same-walk "
          f"discipline; the arm-cell integrity counts 7 x 4 faces "
          f"72/72; the S* lock reads {g1['lock_reads_total']} "
          f"(7 arm-cells x 72 — 4 SELF-R doses + 3 NBW doses)"
          f" | THE REGISTER FACE (G2, the PER-ARM-CELL scope — exp292's "
          f"landed diagnosis honored): the replay equality 72/72 x 7 "
          f"arm-cells, the spec-install complement 72/72 x 7 arm-cells, "
          f"finite 72/72 per arm-cell — the register survives the walk "
          f"+ the settle on BOTH arms, the population path identical "
          f"(the NBW read a pure projection; the armed-write partition "
          f"216/216; the NBW fallback-to-self counts recorded per row — "
          f"total {nbw_fallback_total} across {nbw_armed_total} armed "
          f"writes)"
          f" | THE AUDIT FACES (never gating): the PEAK argbest faces "
          f"host-wise and the per-host leak rows carried in the deposit; "
          f"exp288's pooled-R_max class-blindness re-read at the leak "
          f"face's arm-cell nbw|g=1 — "
          f"{rmax_best['n_concentrating_hosts']}/12 hosts concentrating "
          f"(vs exp288's deposited SPEC-UNIFORM face, the anchor's own "
          f"R_max within [{min(rmax_anchor['per_host_R_max'].values()):.4f}, "
          f"{max(rmax_anchor['per_host_R_max'].values()):.4f}]); the "
          f"H3/H5 outlier deltas carried per arm-cell; the repo test "
          f"suite green in the shadow subprocess "
          f"({suite['n_pass_lines']} PASS lines, returncode "
          f"{suite['returncode']}); the zero-reader scan: "
          f"{len(integrity['zero_reader_scan']['files_with_phi_history'])} "
          f"files carry phi_history (the port + the instrument modules "
          f"only)"
          f" | 12 hosts, a deterministic sha-asserted rebuild "
          f"(graph_path for H0/H1, small_world at the deposited rewire "
          f"seeds), the provenance chains sha-verified 31/31, 9 "
          f"deposits READ-ONLY byte-unchanged, one pass per arm "
          f"({core['run_form']}), floor -60.0")



    # ---- the discipline scans + the deposit form -------------------------
    deposit = {
        "exp": "exp295_dose_curve_leak_repair",
        "claim": (
            "THE DOSE CURVE REFINED AND THE NBOR LEAK REPAIR (batch 48, "
            "pre-registration commit dfd6fb5; ledger L273's registered "
            "nexts (i)+(ii)): exp292 landed DOSE-REVERSAL x "
            "SELF-DOMINANT — the self-history carrier peaks at g ~ 1.0 "
            "(the reversal past the peak 12/12) and the neighbor-mean "
            "form degrades 12/12 (+1.8385 mV at g=1.0 — the register of "
            "the unwound neighbors holds the SPEC INSTALL, so the naive "
            "neighbor mean re-injects the spec's own values as a false "
            "history: THE LEAK). Two pre-named follow-ups, one battery, "
            "zero new knobs: (1) THE DOSE CURVE refined around the peak "
            "— the pre-named {0.75, 1.0, 1.25, 1.5} SELF ladder (the "
            "reversal's sharpness: is the peak flat or sharp?); (2) THE "
            "LEAK REPAIR — the WRITE-SET-WEIGHTED neighbor form: the "
            "neighbor mean weighted by each neighbor's write-set "
            "membership (nbrs that the program ACTUALLY wrote "
            "contribute their true commit history; unwritten nbrs — "
            "whose register holds the spec install — contribute ZERO "
            "weight); the repaired NBOR arm re-runs the source face at "
            "exp292's NBOR grid {0.25, 0.5, 1.0}. ONE battery: 4 SELF-R "
            "doses x 72 rows + 3 NBW doses x 72 rows = 504 decodes; the "
            "g=0.0 control is exp289's deposited anchor (read, never "
            "re-run). Branches: the dose face PEAK-FLAT (the plateau "
            "bar: the |delta| differences among {0.75, 1.0, 1.25} all "
            "< 0.01 mV on >= 10/12 hosts) / PEAK-SHARP x the leak face "
            "LEAK-CONFIRMED (the NBW g=1.0 delta improves vs exp292's "
            "deposited NBOR delta by > 0.05 mV on >= 10/12 hosts) / "
            "LEAK-NOT-SUFFICIENT — the two faces recorded "
            "independently"),
        "method": {
            "port": (
                "cultivation/bioelectric/collective.py is exp289's "
                "LANDED form, UNCHANGED (sha recorded at entry == exit): "
                "write_spec_layer installs phi_history = the spec map "
                "bit-exactly; the commit-write site populates the "
                "register after the write. exp142 NOT modified (sha "
                "entry == exit, recorded); exp292's landed instrument "
                "module (THE BASE) likewise sha-pinned; the zero-reader "
                "scan asserts phi_history appears in no file outside "
                "the port + the instrument modules"),
            "replica": (
                "the exp286/exp287/exp288/exp289 traced replica REUSED "
                "VERBATIM at the production budget 8 == exp142's "
                "STEPS_PER_CELL (the host rebuild, exp256's "
                "_scoped_row_read_state form: PN1/PN2 + TC1 + TC2 + the "
                "traced TC3), plus the register live (presence + init "
                "asserted at the walk's start; the population after "
                "each write; the survival asserted at the walk's end) "
                "and the activation blend (g_ctx > 0 AND the exp258 "
                "canon-boundary class restriction; ZERO deviation at "
                "g_ctx == 0.0)"),
            "arms": (
                "SELF-R — the coupling reads phi_history[i] (exp289's "
                "landed form verbatim; asserted == the deposited "
                "instrument by G1's bit-exact g=1.0 anchor: the errs + "
                "the trace shas 72/72). NBW — the coupling reads the "
                "WRITE-SET-WEIGHTED neighbor mean of phi_history (the "
                "weight w_j = 1 if the neighbor j is in the row's write "
                "set — the commit sequence's support, derived "
                "in-executor from the walk order, no new knobs — else "
                "0; the mean over the weighted support; a "
                "no-written-neighbor write falls back to the self "
                "value, the fallback count recorded per row; the "
                "register itself UNTOUCHED: the read is a pure "
                "projection, the population path identical, the "
                "armed-write partition reads + fallbacks == the blend "
                "count asserted 216/216). The arms differ ONLY in the "
                "coupling's read source (the executor's hist_source; "
                "default 'self')"),
            "ladder": (
                "the SELF-R doses {0.75, 1.0, 1.25, 1.5} (the refined "
                "curve; the g=1.0 point IS exp289's landed grid point — "
                "the anchor) and the NBW doses {0.25, 0.5, 1.0} "
                "(exp292's NBOR grid, leak-repaired); the g=0.0 control "
                "is exp289's deposited anchor battery (72 errs, "
                "walk_steps, n_commits — read, never re-run; its "
                "provenance == exp256's deposited substituted errs "
                "re-asserted 72/72 at assembly); the walk structure is "
                "value-level only (the stream face: the walked + commit "
                "counts == the anchor's 504/504; the per-row blend "
                "count constant across the 7 arm-cells 72/72)"),
            "branch_rule": (
                "per arm-cell (4 SELF-R + 3 NBW cells) the 72-row mean "
                "err and the mean paired delta vs the g=0.0 anchor. "
                "SIGN CONVENTIONS (exp290's disclosed-convention "
                "precedent, both signings recorded per row): the DOSE "
                "face is evaluated on the anchor-minus-arm improvement "
                "form's MAGNITUDES — the plateau clause is "
                "sign-agnostic: PEAK-FLAT iff the |delta| differences "
                "among {0.75, 1.0, 1.25} are all < 0.01 mV on >= 10/12 "
                "hosts; PEAK-SHARP otherwise (the argbest dose recorded "
                "host-wise, audit-only, the smaller-dose tie-break). "
                "The LEAK face is evaluated in the ARM-MINUS-ANCHOR "
                "err-delta form (exp292's landed convention, the form "
                "of its deposited +1.8385 face): LEAK-CONFIRMED iff the "
                "NBW g=1.0 delta improves vs the deposited per-host "
                "NBOR delta by > 0.05 mV on >= 10/12 hosts; "
                "LEAK-NOT-SUFFICIENT otherwise"),
            "audit_faces": (
                "the worst-err per arm-cell vs the anchor's 6.0 bar "
                "(unchanged); the per-host per-arm delta tables; the "
                "PEAK argbest host-wise table; the NBW fallback counts "
                "per row/cell; exp288's pooled-R_max class-blindness "
                "re-read at the leak face's arm-cell nbw|g=1 (exp208's "
                "classify VERBATIM, exp288's pooling, exp288's "
                "pre-named bars CONC_BAR 1.50 / CONC_MIN_HOSTS 10 — "
                "audit-only, never gating), carried next to exp288's "
                "deposited face; the H3/H5 outlier deltas per "
                "arm-cell; the shadow test suite (green, disclosed "
                "subprocess)"),
            "run_form": (
                "the default in-process form runs the whole sequence "
                "(may exceed the 560 s cap); the pre-named sandbox "
                "form is the checkpoint split EXP295_MODE=pass1 (the "
                "SELF-R ladder, 288 decodes) | pass2 (the NBW ladder, "
                "216 decodes) | merge — each pass a separate process, "
                "the merge assembling and evaluating the gates once, "
                "NEVER re-decoding; both forms evaluate the SAME "
                "gates and assert the same bit-identities"),
            "scope": (
                "the full commit sequences, traces, final states and "
                "register arrays NOT re-deposited — bit-reproduced via "
                "the per-row digests (commit_seq_sha256, "
                "trace_sha256, phi_history_sha256) + G1's anchor (the "
                "exp284..exp289 precedent); no wall-clock fields")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base) + the mia audit errs",
                "the 72 rows — the anchor chain's base (the control "
                "column's provenance target) + the deep-row target/"
                "medium shas",
                "the host frame + the per-host one-zone premium means "
                "+ the boundary counts + the outlier pre-name source",
                "the outlier pre-name + the field-table carries",
                "the S0 walk anchor — the 72 per-row walk_end_rms + "
                "trace shas + the deposited TRAJECTORY-CARRIED branch",
                "the S0 commit-layer anchor — the 72 per-row "
                "commit_seq_sha256 + cvt_rms + n_commits + sc_rms + "
                "the 12-host mean_cvt",
                "the prior batch's face — the deposited SPEC-UNIFORM "
                "branch + the per-host pooled R_max + its own fresh "
                "errs (the chain face) + the 6 inputs sha records "
                "verified in the chains",
                "the landed HISTORY-CARRIED instrument — the g=0.0 "
                "CONTROL column (the 72 anchor errs + walk_steps + "
                "n_commits, read never re-run) + the g=1.0 ANCHOR "
                "rows (the 72 errs + trace shas the SELF-R arm must "
                "reproduce bit-exact) + the deposited branch face",
                "the landed DOSE-REVERSAL x SELF-DOMINANT instrument "
                "— the LEAK FACE's comparison deposit (the per-host "
                "NBOR deltas at g=1.0, the leaky form's +1.8385 mean "
                "face, read never re-run) + the deposited branch "
                "face"))},
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
            "exp142_sha256": integrity["exp142_sha256"],
            "exp289_module_sha256": integrity["exp289_module_sha256"],
            "exp292_module_sha256": integrity["exp292_module_sha256"]},
        "hosts": core["hosts"],
        "outliers": core["outliers"],
        "cluster": core["cluster"],
        "rebuild_report": integrity["rebuild_report"],
        "exp282_reread": integrity["exp282_reread"],
        "exp287_reread": integrity["exp287_reread"],
        "exp288_reread": integrity["exp288_reread"],
        "exp292_reread": {
            "n_rows": nbor_dep_cell["n_rows"],
            "branch": dep292["branch"],
            "nbors_g1_mean_paired_delta_arm_minus_anchor":
                nbor_dep_mean,
            "nbors_g1_delta_rows_arm_minus_anchor": {
                r["host"]: float(r["delta_arm_minus_anchor"])
                for r in nbor_dep_rows}},
        "provenance_chains": chains,
        "targets": integrity["targets"],
        "test_suite": suite,
        "rows_self": core["rows_self"],
        "rows_nbw": core["rows_nbw"],
        "ladder": {
            "self_ladder": list(SELF_LADDER),
            "nbw_ladder": list(NBW_LADDER),
            "sources": list(HISTORY_SOURCES),
            "control_source": (
                "exp289's deposited anchor rows (the g=0.0 face) — "
                "read, never re-run; the anchor's provenance == "
                "exp256's deposited substituted errs re-asserted 72/72 "
                "at assembly"),
            "control_means": control_means,
            "cells": cells,
            "peak_rows": peak_rows,
            "leak_rows": leak_rows,
            "n_improved_per_cell": g3["n_improved_per_cell"]},
        "branch": branch,
        "branch_discriminant": {
            "bars": {"DOSE_MIN_HOSTS": DOSE_MIN_HOSTS,
                     "PLATEAU_EPS": PLATEAU_EPS,
                     "MARGIN": MARGIN},
            "bars_pre_named_at": ("dfd6fb5 — fixed at pre-registration, "
                                  "never fit"),
            "clause_form": (
                "the DOSE face on the anchor-minus-arm improvement "
                "form's magnitudes (the plateau clause is "
                "sign-agnostic; both signings recorded per row): "
                "PEAK-FLAT iff the |delta| differences among {0.75, "
                "1.0, 1.25} are all < 0.01 mV on >= 10/12 hosts; "
                "PEAK-SHARP otherwise. The LEAK face in the "
                "arm-minus-anchor err-delta form (exp292's landed "
                "convention, the form of its deposited +1.8385 face): "
                "LEAK-CONFIRMED iff the NBW g=1.0 delta improves vs "
                "the deposited per-host NBOR delta by > 0.05 mV on "
                ">= 10/12 hosts; LEAK-NOT-SUFFICIENT otherwise"),
            "resolved": {"branch": branch,
                         "dose_face": dose_face,
                         "leak_face": leak_face,
                         "n_plateau_clause": n_flat,
                         "n_improves_over_leaky": n_leak,
                         "nbor_deposited_mean_g1": nbor_dep_mean,
                         "mean_paired_delta_nbw_g1": md_nbw_g1},
            "audit_rmax_face_at_leak_cell": rmax_best,
            "audit_rmax_face_anchor_exp288": rmax_anchor},
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": {
            "form": run_form,
            "discipline": "deterministic one pass per arm",
            "decodes": {"self_g0.75": 72, "self_g1.0": 72,
                        "self_g1.25": 72, "self_g1.5": 72,
                        "nbw_g0.25": 72, "nbw_g0.5": 72,
                        "nbw_g1.0": 72},
            "stream_untouched_proof": (
                "the register is a state variable, not a second RNG "
                "consumer — the population is a pure recording after "
                "the write and the NBW read a pure projection before "
                "it; G1's bit-exact g=1.0 anchor (the errs + the "
                "trace shas vs exp289's deposited rows 72/72) is the "
                "assertion; the arms' walked counts + commit counts "
                "== the anchor's 504/504; the per-row blend count "
                "constant across the 7 arm-cells 72/72"),
            "two_pass_note": (
                "the exp288 two-pass bit-identity discipline does NOT "
                "carry to this module — G4 pre-names the one-pass-per-"
                "arm form (the exp289/exp292 checkpoint-split "
                "precedent); exp292's landed G2 tally-scope diagnosis "
                "IS honored: the register-replay tallies at the "
                "PER-ARM-CELL 72/72 scope"),
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
        "G1_the_anchor_and_the_arms_integrity": {
            "pass": g1_pass,
            "counts": g1,
            "anchor_289": (
                "the SELF-R g=1.0 errs reproduce exp289's deposited "
                "g=1.0 errs BIT-EXACT 72/72 with the trace shas 72/72 "
                "(the same-walk discipline; asserted fail=STOP per row "
                "at decode); the SELF form's coupling thereby asserted "
                "== the deposited instrument"),
            "arm_cell_integrity": (
                "per arm-cell (4 SELF-R + 3 NBW cells) the finite/A3/"
                "trace-length/commit-count asserts 72/72 (fail=STOP at "
                "decode; the counts recorded per cell)"),
            "lock_reads": (
                f"{g1['lock_reads_total']} (7 arm-cells x 72; "
                f"{g1['lock_reads_pass1']} + {g1['lock_reads_pass2']})"),
            "floor_disclosure": (
                "no stress arm; the floor -60.0 throughout, asserted "
                "at setup, at the gate assembly and at exit"),
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "n_source_deposits": len(READ_DEPS)},
        "G2_the_forms_definition": {
            "pass": g2_pass,
            "counts_per_arm": g2_counts,
            "counts_per_arm_cell": cell_g2,
            "zero_knob_definition": (
                "the SELF form's coupling reads phi_history[i] "
                "(exp289's form, asserted == the deposited instrument "
                "by G1's bit-exactness); the NBW form's coupling reads "
                "the WRITE-SET-WEIGHTED neighbor mean of phi_history — "
                "the weights derived ONLY from the commit sequence's "
                "support (the row's write set, derived in-executor "
                "from the walk order; w_j = 1 for the written "
                "neighbors, 0 otherwise; the mean over the weighted "
                "support; a no-written-neighbor write falls back to "
                "the self value, the fallback count recorded per row) "
                "— no new knobs; the register itself UNTOUCHED, the "
                "population path identical to exp289's"),
            "register_replay_per_arm_cell": (
                "the register's replay equality re-asserted at the "
                "PER-ARM-CELL scope (exp292's landed diagnosis "
                "honored): 72/72 per arm-cell x 7 cells; the "
                "spec-install complement 72/72 per arm-cell; finite "
                "72/72 per arm-cell; the commit bookkeeping (the "
                "exp287 form) at the per-arm scope"),
            "nbw_fallback_counts": (
                "recorded per row (audit): the NBW rows carry "
                "n_nbw_fallbacks; the cells carry the per-cell totals "
                "(n_nbw_fallbacks_total, n_rows_with_fallback); the "
                "armed-write partition (the weighted reads + the "
                "fallbacks == the blend count) asserted 216/216 at "
                "decode")},
        "G3_the_dose_and_leak_branch": {
            "pass": g3_pass,
            "bars": (
                "per arm-cell the 72-row mean err and the mean paired "
                "delta vs the g=0.0 anchor. THE DOSE FACE (SELF-R): "
                "PEAK-FLAT iff the |delta| differences among {0.75, "
                "1.0, 1.25} are all < 0.01 mV on >= 10/12 hosts (a "
                "plateau); PEAK-SHARP otherwise (a distinct optimum — "
                "the argbest dose recorded host-wise, audit-only). "
                "THE LEAK FACE (NBW vs exp292's deposited NBOR "
                "deltas): LEAK-CONFIRMED iff the NBW g=1.0 delta "
                "improves vs the deposited per-host NBOR delta by "
                "> 0.05 mV on >= 10/12 hosts (the leak WAS the failure "
                "mode); LEAK-NOT-SUFFICIENT otherwise. Audit-only, "
                "never gating: the per-host per-arm delta tables; the "
                "fallback counts; the worst-err per arm vs the 6.0 "
                "bar; exp288's pooled-R_max face at the leak face's "
                "arm-cell; the H3/H5 outlier deltas"),
            "resolved": {"branch": branch,
                         "dose_face": dose_face,
                         "leak_face": leak_face,
                         "peak_clause_counts": g3["peak_clause_counts"],
                         "leak_clause_counts": g3["leak_clause_counts"],
                         "nbor_deposited_mean_g1": nbor_dep_mean,
                         "mean_paired_delta_nbw_g1": md_nbw_g1},
            "stream_face": (
                "the walked counts + the commit counts == the anchor's "
                "504/504 (the pairing's precondition); the per-row "
                "blend count constant across the 7 arm-cells 72/72; "
                "the control column's provenance (== exp256's "
                "deposited substituted errs via exp289's anchor) 72/72")},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_the_anchor_and_the_arms_integrity",
                 "G2_the_forms_definition",
                 "G3_the_dose_and_leak_branch"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    gates["G4_discipline"] = {
        "pass": bool(no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged),
        "run_form": run_form,
        "deterministic_one_pass_per_arm": True,
        "stream_untouched_asserted_via_g1": (
            "the bit-exact g=1.0 anchor (the errs + the trace shas "
            "72/72) + the stream face 504/504"),
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_dfd6fb5": docstring_ok,
        "header_byte_unchanged_vs_dfd6fb5": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "n_source_deposits": len(READ_DEPS),
        "exp142_not_modified": True,
        "core_not_modified": True,
        "floor_at_exit": PROD_FLOOR,
        "reader_pin_floor": READER_PIN_FLOOR,
        "reader_pin_disclosure": (
            "N/A — no stress arm; the floor -60.0 throughout"),
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

    print(f"\n  G1 the anchor + the arms' integrity: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the SELF-R g=1.0 anchor: the errs == exp289's deposited "
          f"g=1.0 errs bit-exact {g1['n_anchor289_err_ok']}/72 + the "
          f"trace shas {g1['n_anchor289_trace_ok']}/72; the arm-cell "
          f"integrity counts 7 cells x 4 faces 72/72: {n_per_cell_ok}; "
          f"the S* lock reads {g1['lock_reads_total']} (288 + 216); "
          f"9 deposits READ-ONLY byte-unchanged: {ro_unchanged})")
    print(f"  G2 the forms' definition: "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(the SELF form == exp289's landed form (via G1's "
          f"bit-exactness); the NBW form the write-set-weighted "
          f"neighbor mean, the weights derived only from the commit "
          f"sequence's support, the fallback-to-self counts recorded "
          f"per row (total {nbw_fallback_total} across "
          f"{nbw_armed_total} armed writes); the register replay "
          f"equality at the PER-ARM-CELL scope: "
          f"{'/'.join(str(cell_g2[ck]['n_register_replay_ok']) for ck in cells)}"
          f" = 72/72 x 7; the complement "
          f"{'/'.join(str(cell_g2[ck]['n_register_complement_ok']) for ck in cells)}"
          f" = 72/72 x 7)")
    print("  G3 the dose + leak branch (per-host mean paired deltas "
          "vs the g=0.0 anchor, anchor-minus-arm form; H3/H5 the "
          "outliers):")
    for src, lad in (("self", SELF_LADDER), ("nbw", NBW_LADDER)):
        for g in lad:
            parts_g = "; ".join(
                f"{d['host']} {d['delta_anchor_minus_arm']:+.3f}"
                f"{'*' if d['improved_strict'] else ''}"
                for d in cells[f"{src}|g={g:g}"]["delta_rows"])
            print(f"      {src} g={g}: "
                  f"{cells[f'{src}|g={g:g}']['n_improved']}/12 improved "
                  f"(mean paired "
                  f"{cells[f'{src}|g={g:g}']['mean_paired_delta_arm_minus_anchor']:+.4f}"
                  f" err-delta) | {parts_g}")
    print(f"      the PEAK clause (the plateau bar {PLATEAU_EPS} mV "
          f"among {{0.75, 1.0, 1.25}}): {n_flat}/12 hosts flat "
          f"(bar {DOSE_MIN_HOSTS}) -> {dose_face}")
    print("      the argbest host-wise (audit): "
          + "; ".join(f"{r['host']}@g={r['argbest_dose']:g}"
                      for r in peak_rows))
    print(f"      the LEAK clause (the margin {MARGIN} mV vs exp292's "
          f"deposited NBOR g=1.0 deltas, mean {nbor_dep_mean:+.4f}): "
          f"{n_leak}/12 hosts improve -> {leak_face}")
    print("      the per-host leak rows (audit): "
          + "; ".join(f"{r['host']} nbw {r['nbw_delta_arm_minus_anchor']:+.3f} "
                      f"vs nbor {r['nbor_deposited_delta_arm_minus_anchor']:+.3f}"
                      f"{'*' if r['improves_over_leaky_by_margin'] else ''}"
                      for r in leak_rows))
    print(f"      the audit R_max face at the leak face's arm-cell "
          f"(nbw g=1.0): "
          f"{rmax_best['n_concentrating_hosts']}/12 concentrating (the "
          f"exp288 anchor face: SPEC-UNIFORM, never gating here)")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(deterministic one pass per arm, form {run_form}; no "
          f"wall-clock fields: {no_wall_clock}; 9 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged}; exp142 and the core NOT "
          f"modified; floor -60.0 at exit)")
    print(f"\n  BRANCH: {branch} | peak clause {n_flat}/12 | leak "
          f"clause {n_leak}/12 | NBW g=1.0 mean delta {md_nbw_g1:+.4f} "
          f"vs the deposited NBOR {nbor_dep_mean:+.4f}")
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

