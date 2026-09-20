#!/usr/bin/env python3
"""exp294 — THE PREMIUM UNDER THE HISTORY CARRIER: DOES THE SPEC-LAYER
PREMIUM SURVIVE THE REGISTER'S IMPROVEMENT? (batch 48; ledger L269's
registered next (iv) == L273's registered next (iii) — exp289 landed
HISTORY-CARRIED (the self-history coupling improves the decode 12/12,
monotone to g=1.0), exp292 landed DOSE-REVERSAL x SELF-DOMINANT (the
carrier is self-sourced, dose-peaked at g ~ 1.0), exp293 landed
PROTECTED (the register protects under write-time stress,
super-additively, P +0.7285). The chain's standing finding (exp287,
L265): the premium lives in WHAT the program commits —
rho(mean_cvt)~mia +0.8616 / ~premium +0.7790, and exp288 (L267)
showed the commit-error face is class-blind. THE OPEN QUESTION: the
carrier improves the decode by re-coupling the commits to the
cells' own history — does that improvement DISSOLVE the spec-layer
premium (the host-dependence of the committed pattern collapses as
the errs converge — the premium was the noise's host structure) or
CARRY THROUGH it (the committed pattern stays host-dependent — the
premium is structural to the spec layer, not to the un-coupled
noise)?)

THE INSTRUMENT (exp289's landed form REUSED VERBATIM at its landed
best dose): the SELF form at g=1.0 on the 72-row substituted battery
(exp256's, 12 hosts x 3 seeds x r-60i0/r-60i1 at n=400, the traced
replica at the production budget 8) with the commit recording (the
(f) addition) — the SAME walk exp289's g=1.0 arm ran (the errs + the
trace shas reproduce exp289's deposited g=1.0 records BIT-EXACT
72/72 — the anchor, fail=STOP; NO new decodes needed beyond the one
anchor battery re-run that produces them).

THE READS (zero new knobs, all on the fresh carrier-walk commits):

  R1  THE COMMIT LAYER UNDER THE CARRIER: per row the commit-vs-target
      RMS cvt_rms (the exp287 form) on the carrier's commits; per host
      the 6-row mean_cvt; THE ANCHOR REGRESSIONS: rho(mean_cvt)~mia
      and ~premium under the house conventions (exp274/exp275/exp282
      VERBATIM) — the branch reads the comparison vs exp287's
      deposited rhos (+0.8616 / +0.7790):
      PREMIUM-DISSOLVED  iff BOTH fresh |rho| < 0.40 (the carrier's
          improvement flattened the committed pattern's host
          dependence — the premium was the un-coupled noise);
      PREMIUM-CARRIED    iff BOTH fresh |rho| >= 0.60 (the committed
          pattern stays host-dependent under the carrier — the
          premium is structural to the spec layer);
      PREMIUM-MIXED      otherwise (the honest middle).
  R2  THE IMPROVEMENT'S ADDRESS (audit-only): the per-host mean err
      deltas vs the g=0.0 anchor (the exp289 deposited form) vs the
      per-host mean_cvt deltas — does the improvement track the
      commit-layer change (the delta correlation, the house
      conventions, audit-only)? The exp288 pooled-R_max face on the
      carrier's commits (audit-only). The worst-err vs the 6.0 bar
      (unchanged, audit-only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHOR: the carrier battery's errs == exp289's deposited
      g=1.0 errs BIT-EXACT 72/72 (the verified flags 72/72) + the
      trace shas 72/72 (the SAME walk — the commit layer is the
      carrier's, not a new instrument); the 12 bases rebuilt
      sha-asserted vs exp243 (the exp269/exp280 form); the deep
      targets 72/72; the carries mia + premium bit-exact 12/12 +
      12/12; the provenance chains sha-verified (9 deposits:
      exp243/256/272/273/282/287/288/289/292 — the pre-named 29
      records: exp243 4 + exp256 3 + exp272 4 + exp273 5 + exp282 4
      + exp287 5 + exp288 1 + exp289 2 + exp292 1); the source
      deposits READ-ONLY byte-unchanged.
  G2  THE COMMIT LAYER'S DEFINITION (zero-knob asserted, fail=STOP
      per row): the commit count == walk_steps == the trace length
      72/72; the commit indices unique 72/72; the write-set coverage
      72/72; the values finite 72/72; the digests recorded 72/72
      (the full sequences NOT re-deposited); cvt_rms finite 72/72;
      the A3 convention 72/72; the S* lock reads 72; the register's
      replay equality (exp289's G2 form, the PER-ARM scope) 72/72.
  G3  THE BRANCH DISCRIMINANT (pre-named numeric bars above): the
      fresh rhos vs the PREMIUM_DISSOLVED 0.40 / PREMIUM_CARRIED 0.60
      bars (fixed HERE at pre-registration, never fit); the
      regressions under the house conventions verbatim (Spearman =
      Pearson on the tied-average ranks; the 12-slot frame with the
      H0==H1 echo carried); audit-only: R2's address reads.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): PREMIUM-DISSOLVED / PREMIUM-CARRIED /
PREMIUM-MIXED.

RUN: 72 decodes ~ 60-90 s foreground, one pass + the asserts. Under
the 570 s cap in-process.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp294_premium_under_history.json")


def main() -> dict:

    # ==== BODY (written under the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 030536f; gates G1-G4
    #      evaluated exactly once) ========================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata   # the house conventions' ranker

    import cultivation.bioelectric.collective as CORE  # the floor's home; the port CONSUMED as landed — NOT modified
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
    #      is the 030536f pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "a6702324e1a9722d78c2f5d49d4b22e3540683895240c86264f3d5b030086f8d")
    EXPECTED_HEADER_SHA256 = (
        "e1608bce50a75c20b052f8744f87d821d2fc3b046af146de2ed1b2c51fbd1cc8")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 030536f"
    assert header_ok, "header drifted from 030536f"

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
    #      THE CARRIER DOSE + THE BRANCH BARS — pre-named) -----------------
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
    # THE CARRIER DOSE: the SELF form at g=1.0 — exp289's landed best
    # grid point (asserted against the deposit in _read_anchor289; the
    # dose exp292's ladder confirmed as the carrier's peak).
    G_CARRIER = 1.0
    # THE BRANCH BARS (pre-named at 030536f, numeric, never fit):
    # PREMIUM-DISSOLVED iff BOTH fresh |rho| < 0.40;
    # PREMIUM-CARRIED   iff BOTH fresh |rho| >= 0.60;
    # PREMIUM-MIXED     otherwise.
    PREMIUM_DISSOLVED = 0.40
    PREMIUM_CARRIED = 0.60
    REG_KEYS = ("mean_cvt~mia_prod_err", "mean_cvt~one_zone_premium")
    # exp288's pooled-R_max audit bars (the class-blindness re-read —
    # audit-only, never gating)
    CONC_BAR = 1.50
    CONC_MIN_HOSTS = 10
    # the commit source tags (the pre-named census)
    COMMIT_SOURCES = ("spec", "canon", "parent")
    # the three clean classes (exp208's classify labels; cls 2 = INTERIOR
    # never occurs — the exp277/exp284 disclosure, asserted per row)
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

    # ---- the reuse's own provenance: the port's bytes + exp142's bytes
    #      recorded at entry (the core and exp142 NOT modified — the shas
    #      re-asserted at exit AND sha-verified against exp289's deposited
    #      port record in the provenance chains) --------------------------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)

    def _zero_reader_scan():
        """Scan the package + the experiments for phi_history touches:
        every occurrence must live in the ported collective.py (the
        register's init + the commit-write population + their comments)
        or in the history-instrument line's own modules (exp289's landed
        instrument, exp292's/exp293's reuses, THIS instrument — each
        carries the register's recording/coupling forms). exp289's scan
        allowed only the port + itself; the set widens as the instrument
        line grows. No reader anywhere else (the reader-at-defaults
        claim is exp289's landed G1; re-scanned here as a discipline
        carry, audit-only)."""
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
                   "experiments/exp294_premium_under_history.py"}
        unexpected = sorted(set(hits) - allowed)
        assert not unexpected, \
            f"phi_history touched outside the port + the instrument " \
            f"line: {unexpected}"
        return {"files_with_phi_history": hits,
                "files_outside_port_and_instrument_line": unexpected,
                "allowed_set_note": (
                    "the port + the four history-instrument modules "
                    "(exp289 landed, exp292/exp293 reuses, exp294 this "
                    "instrument); exp289's landed scan allowed the port "
                    "+ itself only — the set widens with the line"),
                "readers_at_defaults": 0}

    zero_reader_scan = _zero_reader_scan()

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; NINE deposits:
    #      exp243 + exp256 + exp272 + exp273 + exp282 + exp287 + exp288
    #      + exp289 + exp292) ---------------------------------------------
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
    assert dep289["exp"] == "exp289_history_register", \
        "the exp289 anchor deposit drifted"
    assert dep292["exp"] == "exp292_history_dose_source", \
        "the exp292 chain deposit drifted"

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

    # ---- [exp294 note: the comment and code below are exp289's
    #      landed traced replica — the register (g) and the
    #      self-history activation (h) — REUSED VERBATIM; the
    #      activation runs only at g = 1.0 in this instrument]
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

    # ---- one CARRIER-row decode (the g=1.0 SELF arm; exp289's
    #      _decode_grid_row REUSED VERBATIM with exactly two
    #      disclosed additions: the dep_rec parameter and THE
    #      CARRIER ANCHOR block — exp289's _decode_anchor_row
    #      assert form re-targeted to exp289's own deposited g=1.0
    #      records; the G2 count flags added, the asserts
    #      untouched, fail=STOP on EVERY row) ----------------------
    def _decode_carrier_row(host, row_key, spec, med, seed, fmax, g,
                            A_base, dep_rec):
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
        commits_count_ok = bool(n_commits == steps == len(trace))
        assert commits_count_ok, \
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
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        cvt_fin_ok = bool(np.isfinite(cvt_rms))
        assert cvt_fin_ok, \
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

        # ---- THE CARRIER ANCHOR (G1, fail=STOP): the g=1.0 carrier
        #      row IS exp289's deposited g=1.0 record — the SAME walk, so
        #      the commit layer is the carrier's and not a new instrument
        #      (exp289's _decode_anchor_row assert form, re-targeted from
        #      the exp256/exp282/exp287 deposits to exp289's g=1.0
        #      records) ----------------------------------------------
        err_289_ok = bool(err == dep_rec["err"])
        ver_289_ok = bool(bool(out["program_verified"])
                          == bool(dep_rec["verified"]))
        ts_289_ok = bool(trace_sha == dep_rec["trace_sha256"])
        steps_289_ok = bool(steps == int(dep_rec["walk_steps"]))
        we_289_ok = bool(final == float(dep_rec["walk_end_rms"]))
        ee_289_ok = bool(err_exact == float(dep_rec["err_exact"]))
        nc_289_ok = bool(n_commits == int(dep_rec["n_commits"]))
        cs_289_ok = bool(commit_sha == dep_rec["commit_seq_sha256"])
        cvt_289_ok = bool(cvt_rms == float(dep_rec["cvt_rms"]))
        hw_289_ok = bool(int(out["n_hist_writes"])
                         == int(dep_rec["n_hist_writes"]))
        assert err_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the fresh err drifted from "
             "exp289's deposited g=1.0 err — THE CARRIER IS NOT THE "
             "LANDED WALK")
        assert ver_289_ok, \
            f"{host} {row_key} s{seed} g{g}: the verified flag drifted"
        assert ts_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the fresh trace sha "
             "drifted from exp289's deposited g=1.0 trace sha — the "
             "walk is not the landed carrier walk")
        assert steps_289_ok and nc_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the walked count / commit "
             "count drifted from exp289's deposited g=1.0 records — the "
             "stream face moved")
        assert we_289_ok and ee_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the walk-end / err-exact "
             "faces drifted from exp289's deposited g=1.0 records")
        assert cs_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the fresh commit-sequence "
             "digest drifted from exp289's deposited g=1.0 "
             "commit_seq_sha256 — the commit layer is not the carrier's")
        assert cvt_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the fresh cvt_rms drifted "
             "from exp289's deposited g=1.0 cvt_rms")
        assert hw_289_ok, \
            (f"{host} {row_key} s{seed} g{g}: the blend count drifted "
             "from exp289's deposited g=1.0 n_hist_writes")

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
               "sum_sq_e": total_sq,
               "trace_len_ok": trace_len_ok,
               "commits_count_ok": commits_count_ok,
               "commits_unique_ok": commits_unique_ok,
               "coverage_ok_rec": coverage_ok,
               "commits_finite_ok": commits_finite_ok,
               "census_ok": census_ok,
               "cvt_finite_ok": cvt_fin_ok,
               "digests_ok": bool(len(commit_sha) == 64),
               "err_289_ok": err_289_ok, "verified_289_ok": ver_289_ok,
               "trace_sha_289_ok": ts_289_ok, "steps_289_ok": steps_289_ok,
               "walk_end_289_ok": we_289_ok, "err_exact_289_ok": ee_289_ok,
               "n_commits_289_ok": nc_289_ok,
               "commit_sha_289_ok": cs_289_ok, "cvt_289_ok": cvt_289_ok,
               "hist_writes_289_ok": hw_289_ok}
        return rec

    # ---- THE PROVENANCE CHAINS (sha-verified against the current file
    #      bytes; NINE deposits — exp243/256/272/273/282/287/288/289/292 —
    #      the pre-named 29 records: exp243 4 + exp256 3 + exp272 4 +
    #      exp273 5 + exp282 4 + exp287 5 + exp288 1 + exp289 2 + exp292 1.
    #      The per-source scope: the first six records read whole;
    #      exp288's/exp292's inputs scoped to the NEW chain link each
    #      adds (exp287_deposit / exp289_deposit — the earlier links are
    #      the chain's own earlier sources); exp289's port record read
    #      whole (the ported collective.py + exp142 — the NOT-modified
    #      anchors). The per-source counts asserted = the pre-named. ----
    CHAIN_FILE = {
        "exp182": "results/exp182_substrate_100.json",
        "exp198": "results/exp198_adversarial_reader_n400.json",
        "exp202": "results/exp202_cross_organism_carriage.json",
        "exp225": "results/exp225_structured_media_reader.json",
        "exp243": "results/exp243_structured_adversarial.json",
        "exp255": "results/exp255.json",
        "exp243_deposit": "results/exp243_structured_adversarial.json",
        "exp256_deposit": "results/exp256_row_pair_regression.json",
        "exp270_deposit": "results/exp270_structural_dose.json",
        "exp271_deposit": "results/exp271_one_zone_premium.json",
        "exp272_deposit": "results/exp272_host_premium_structure.json",
        "exp273_deposit": "results/exp273_outlier_hosts.json",
        "exp282_deposit": "results/exp282_trajectory_structure.json",
        "exp287_deposit": "results/exp287_fixed_point_identity.json",
        "exp288_deposit": "results/exp288_spec_layer_face.json",
        "exp289_deposit": "results/exp289_history_register.json",
        "exp182_deposit": "results/exp182_substrate_100.json",
        "exp142_sha256": "experiments/exp142_sign_read.py",
        "sha256": "cultivation/bioelectric/collective.py"}
    CHAIN_SOURCES = (
        ("exp243_structured_adversarial.json", "provenance", None, 4),
        ("exp256_row_pair_regression.json", "provenance", None, 3),
        ("exp272_host_premium_structure.json", "inputs", None, 4),
        ("exp273_outlier_hosts.json", "inputs", None, 5),
        ("exp282_trajectory_structure.json", "inputs", None, 4),
        ("exp287_fixed_point_identity.json", "inputs", None, 5),
        ("exp288_spec_layer_face.json", "inputs",
         ("exp287_deposit",), 1),
        ("exp289_history_register.json", "port", None, 2),
        ("exp292_history_dose_source.json", "inputs",
         ("exp289_deposit",), 1))

    def _verify_chains():
        cur = {}
        report = []
        total = 0
        ok_total = 0
        for fname, rkey, scope, n_expected in CHAIN_SOURCES:
            with open(os.path.join(ROOT, "results", fname)) as fh:
                rec = json.load(fh)[rkey]
            n_rec = 0
            n_ok = 0
            for k, v in rec.items():
                if scope is not None and k not in scope:
                    continue
                if isinstance(v, dict):
                    v = v.get("sha256")
                if not (isinstance(v, str) and len(v) == 64):
                    continue
                n_rec += 1
                target = CHAIN_FILE[k]
                if target not in cur:
                    cur[target] = _sha(os.path.join(ROOT, target))
                good = bool(v == cur[target])
                n_ok += int(good)
                assert good, \
                    f"chain drift: {fname} {rkey}.{k} vs {target}"
            assert n_rec == n_expected, \
                (f"{fname} {rkey}: the chain record count {n_rec} != the "
                 f"pre-named {n_expected}")
            total += n_rec
            ok_total += n_ok
            report.append({"deposit": fname, "record": rkey,
                           "scope": ("all sha-record keys"
                                     if scope is None else
                                     "the pre-named new-link keys "
                                     f"{list(scope)}"),
                           "n_records": n_rec, "n_verified": n_ok})
        assert total == 29, f"the chain record count {total} != 29"
        return {"total_records": total, "total_verified": ok_total,
                "per_source": report}

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

    # ---- THE ANCHOR DEPOSIT READ (exp289's deposit-reading form: the
    #      g=1.0 per-row records + the per-grid faces + the g=0.0
    #      control, keyed and asserted before any use) -------------------
    def _read_anchor289():
        assert dep289["branch"] == "HISTORY-CARRIED", \
            "exp289's deposited branch drifted from HISTORY-CARRIED"
        grid = dep289["grid"]
        assert grid["g_ctx_grid"] == [0.0, 0.25, 0.5, 1.0], \
            "exp289's deposited grid drifted"
        assert float(grid["best_grid_point"]) == float(G_CARRIER), \
            ("exp289's landed best grid point drifted from the carrier's "
             "dose")
        pg1 = grid["per_grid"][str(G_CARRIER)]   # the "1.0" key
        rows = {}
        for r in dep289["grid_rows"]:
            if float(r["g_ctx"]) != float(G_CARRIER):
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in rows, f"duplicate exp289 g=1.0 row {key}"
            assert all(fld in r for fld in
                       ("err", "verified", "trace_sha256", "walk_steps",
                        "walk_end_rms", "err_exact", "n_commits",
                        "commit_seq_sha256", "cvt_rms",
                        "n_hist_writes")), \
                f"{key}: exp289's g=1.0 record is missing anchor fields"
            rows[key] = r
        assert len(rows) == 72, \
            f"exp289's g=1.0 records: {len(rows)} != 72"
        control_means = {row["host"]: float(row["mean_err"])
                         for row in dep289["host_table"]}
        assert len(control_means) == 12, "exp289's control table drifted"
        return {"rows": rows,
                "host_mean_err": {h: float(pg1["host_mean_err"][h])
                                  for h in hosts},
                "mean_cvt": {h: float(pg1["mean_cvt"][h]) for h in hosts},
                "control_means": control_means,
                "worst_err": float(pg1["worst_err"])}

    # ---- the house conventions (exp287's regression read VERBATIM:
    #      Spearman = Pearson on the tied-average ranks (scipy
    #      rankdata); the single-predictor OLS rank R2; the ties census
    #      per vector) ----------------------------------------------------
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

    # ---- R1: THE COMMIT-LAYER REGRESSION READ (the new code — the
    #      exp287 record form on the fresh carrier's per-host mean_cvt;
    #      the 12-slot frame with the H0==H1 echo carried) ---------------
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

    # ---- THE AUDIT FACE: exp288's pooled-R_max class-blindness re-read
    #      on the carrier's commits (exp289's _pooled_face form,
    #      re-nested at top level — indentation only; exp208's classify
    #      VERBATIM pooling; audit-only, never gating) --------------------
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
                                "never gating in exp294")}

    # ---- THE RUN (one pass: the sha-asserted rebuild + the 72-row
    #      carrier battery at the landed best dose + the host table +
    #      the regressions + the branch + the audit faces) ----------------
    def _compute():
        _LOCK_LOG.clear()
        rb = _rebuild()
        bases = rb["bases"]
        anchor = _read_anchor289()
        rows_out: list = []
        for k in hosts:
            ctx = bases[k]
            med = HostWMedium(ctx["A"])
            for s in SEEDS_RUN:
                for inst in DEEP_INSTANCES:
                    rk = f"r{DEEP_RUNG:g}i{inst}"
                    dep_rec = anchor["rows"][(k, s, rk)]
                    rec = _decode_carrier_row(
                        k, rk, ctx["deep"][inst]["spec"], med, s,
                        ctx["fmax"], G_CARRIER, ctx["A"], dep_rec)
                    rows_out.append(rec)
            hs = [r for r in rows_out if r["host"] == k]
            print(f"  [carrier g={G_CARRIER:g} {k}] 6 rows | errs "
                  f"{[r['err'] for r in hs]} | anchor errs "
                  f"{sum(r['err_289_ok'] for r in hs)}/6 | trace shas "
                  f"{sum(r['trace_sha_289_ok'] for r in hs)}/6 | commit "
                  f"digests {sum(r['commit_sha_289_ok'] for r in hs)}/6",
                  flush=True)
        assert len(rows_out) == 72, \
            f"the carrier battery produced {len(rows_out)} rows != 72"
        assert len(_LOCK_LOG) == 72, \
            f"the S* lock count {len(_LOCK_LOG)} != 72 reads"

        # ---- the per-host carrier table (the 12-slot frame for R1/R2;
        #      the anchor means re-asserted bit-exact vs exp289's
        #      deposited g=1.0 per-grid faces) ---------------------------
        host_table = []
        for h in hosts:
            hs = [r for r in rows_out if r["host"] == h]
            mean_err = float(np.mean([r["err"] for r in hs]))
            mean_cvt = float(np.mean([r["cvt_rms"] for r in hs]))
            me_ok = bool(mean_err == anchor["host_mean_err"][h])
            mc_ok = bool(mean_cvt == anchor["mean_cvt"][h])
            assert me_ok, \
                (f"{h}: the fresh per-host mean err drifted from exp289's "
                 "deposited g=1.0 host_mean_err")
            assert mc_ok, \
                (f"{h}: the fresh per-host mean_cvt drifted from exp289's "
                 "deposited g=1.0 mean_cvt")
            host_table.append({
                "host": h, "n_rows": 6, "outlier": bool(h in outliers),
                "mean_err": mean_err,
                "mean_err_equals_exp289_g1_host_mean": me_ok,
                "mean_cvt": mean_cvt,
                "mean_cvt_equals_exp289_g1_mean_cvt": mc_ok,
                "mean_cvt_control_exp287": float(rb["mean_cvt287"][h]),
                "delta_err_vs_control": float(
                    mean_err - anchor["control_means"][h]),
                "delta_cvt_vs_exp287": float(
                    mean_cvt - float(rb["mean_cvt287"][h])),
                "src_census": {
                    t: int(sum(r["src_census"][t] for r in hs))
                    for t in COMMIT_SOURCES}})

        # ---- R1: the fresh commit-layer regressions (the new code;
        #      the house conventions verbatim — the CONVENTION
        #      SELF-CHECK first: fed exp287's OWN deposited carrier (its
        #      host-table mean_cvt) + the same carries, the copied
        #      machinery must reproduce exp287's deposited rhos
        #      BIT-EXACT) --------------------------------------------------
        targets = rb["targets"]
        target_cols = {
            "mia_prod_err": [float(targets["mia_prod_err"]["values"][h])
                             for h in hosts],
            "one_zone_premium": [
                float(targets["one_zone_premium"]["values"][h])
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
            dep_rho = float(dep287["regressions"][tk]["rho"])
            rec["rho_exp287_deposited"] = dep_rho
            rec["delta_vs_exp287_deposited"] = float(
                rec["rho"] - dep_rho)
            rec["gating"] = True
            rec["role"] = (
                "the branch discriminant — the pre-named bars "
                "PREMIUM_DISSOLVED 0.40 / PREMIUM_CARRIED 0.60, fixed at "
                "pre-registration 030536f, never fit")
            regressions[tk] = rec
        rho_mia = float(regressions["mean_cvt~mia_prod_err"]["rho"])
        rho_prem = float(regressions["mean_cvt~one_zone_premium"]["rho"])

        # ---- THE BRANCH (the pre-named bars; evaluated exactly once) ----
        a_mia = abs(rho_mia)
        a_prem = abs(rho_prem)
        if a_mia < PREMIUM_DISSOLVED and a_prem < PREMIUM_DISSOLVED:
            branch_local = "PREMIUM-DISSOLVED"
        elif a_mia >= PREMIUM_CARRIED and a_prem >= PREMIUM_CARRIED:
            branch_local = "PREMIUM-CARRIED"
        else:
            branch_local = "PREMIUM-MIXED"

        # ---- R2: THE IMPROVEMENT'S ADDRESS (audit-only, never gating):
        #      the per-host mean err deltas vs the g=0.0 control (the
        #      exp289 deposited form) vs the per-host mean_cvt deltas vs
        #      exp287's deposited g=0.0 commit layer — the delta
        #      correlation under the house conventions; the exp288
        #      pooled-R_max face on the carrier's commits; the worst-err
        #      vs the 6.0 bar -------------------------------------------
        delta_err = [next(row for row in host_table
                          if row["host"] == hh)["delta_err_vs_control"]
                     for hh in hosts]
        delta_cvt = [next(row for row in host_table
                          if row["host"] == hh)["delta_cvt_vs_exp287"]
                     for hh in hosts]
        rho_delta = _spearman(delta_err, delta_cvt)
        delta_corr = {
            "quantity": "delta_err_vs_g0.0_control",
            "target": "delta_cvt_vs_exp287_g0.0",
            "rho": rho_delta, "rho_abs": abs(rho_delta),
            "ties_err": _ties_census(delta_err),
            "ties_cvt": _ties_census(delta_cvt),
            "gating": False,
            "role": ("audit-only — R2's address read: does the decode "
                     "improvement track the commit-layer change under "
                     "the carrier (never gating)")}
        pooled_face = _pooled_face(rows_out)
        worst = max(rows_out, key=lambda r: r["err"])
        worst_face = {
            "worst_err": float(worst["err"]),
            "worst_row": {"host": worst["host"],
                          "seed": int(worst["seed"]),
                          "row_key": worst["row_key"]},
            "bar": ERR_BAR,
            "under_bar": bool(worst["err"] < ERR_BAR),
            "note": ("the anchor's 6.0 bar, unchanged — audit-only, "
                     "never gating")}
        return {"rows": rows_out, "host_table": host_table,
                "rebuild": rb, "anchor": anchor,
                "regressions": regressions,
                "convention_selfcheck": convention_selfcheck,
                "branch": branch_local,
                "rho_mia": rho_mia, "rho_prem": rho_prem,
                "delta_corr": delta_corr, "pooled_face": pooled_face,
                "worst_face": worst_face,
                "lock_reads": len(_LOCK_LOG)}

    # ---- THE RUN (the pre-named RUN clause: one IN-PROCESS pass — the
    #      72-row carrier battery at the landed best dose + the asserts;
    #      under the 570 s cap) -------------------------------------------
    print("=== exp294: THE PREMIUM UNDER THE HISTORY CARRIER (the SELF "
          "form at g=1.0 — exp289's landed best dose; exp287's deposited "
          "rhos re-measured on the carrier's commits) ===")
    print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
          f"instances at n={N400} = 72 carrier rows at the production "
          f"budget {BUDGET} with the register live and the self-history "
          f"blend armed at g={G_CARRIER:g} (the SAME walk exp289's g=1.0 "
          f"arm ran — the anchor)")
    core = _compute()
    rows = core["rows"]
    host_table = core["host_table"]
    rb = core["rebuild"]
    anchor = core["anchor"]
    counts = rb["counts"]
    chains = rb["chains"]
    regressions = core["regressions"]
    branch = core["branch"]
    rho_mia = core["rho_mia"]
    rho_prem = core["rho_prem"]

    # ---- the tallies ----------------------------------------------------
    n_err_289 = sum(1 for r in rows if r["err_289_ok"])
    n_ver_289 = sum(1 for r in rows if r["verified_289_ok"])
    n_ts_289 = sum(1 for r in rows if r["trace_sha_289_ok"])
    n_steps_289 = sum(1 for r in rows if r["steps_289_ok"])
    n_we_289 = sum(1 for r in rows if r["walk_end_289_ok"])
    n_ee_289 = sum(1 for r in rows if r["err_exact_289_ok"])
    n_nc_289 = sum(1 for r in rows if r["n_commits_289_ok"])
    n_cs_289 = sum(1 for r in rows if r["commit_sha_289_ok"])
    n_cvt_289 = sum(1 for r in rows if r["cvt_289_ok"])
    n_hw_289 = sum(1 for r in rows if r["hist_writes_289_ok"])
    n_mean_err_289 = sum(1 for row in host_table
                         if row["mean_err_equals_exp289_g1_host_mean"])
    n_mean_cvt_289 = sum(1 for row in host_table
                         if row["mean_cvt_equals_exp289_g1_mean_cvt"])
    n_reg_replay = sum(1 for r in rows if r["register"]["replay_ok"])
    n_reg_comp = sum(1 for r in rows if r["register"]["complement_ok"])
    n_reg_fin = sum(1 for r in rows if r["register"]["finite_ok"])
    n_count = sum(1 for r in rows if r["commits_count_ok"])
    n_uniq = sum(1 for r in rows if r["commits_unique_ok"])
    n_cov = sum(1 for r in rows if r["coverage_ok"])
    n_fin = sum(1 for r in rows if r["commits_finite_ok"])
    n_cens = sum(1 for r in rows if r["census_ok"])
    n_digests = sum(1 for r in rows if r["digests_ok"])
    n_cvtfin = sum(1 for r in rows if r["cvt_finite_ok"])
    n_a3 = sum(1 for r in rows if r["a3_ok"])
    n_conv = sum(1 for r in rows if r["conv_step"] >= 0)
    n_tlen = sum(1 for r in rows if r["trace_len_ok"])
    n_stream_ok = sum(1 for r in rows if r["steps_289_ok"]
                      and r["n_commits_289_ok"]
                      and r["hist_writes_289_ok"])
    n_reg_ok = sum(1 for r in rows if all(r["register"][k] for k in
                                          ("present_ok", "init_ok",
                                           "replay_ok", "complement_ok",
                                           "finite_ok")))
    ro_unchanged = bool(set(_sha(p) for p in READ_DEPS)
                        == set(ro_before.values()))
    rhos_finite = bool(all(np.isfinite(regressions[k]["rho"])
                           for k in REG_KEYS))
    selfcheck_ok = bool(all(core["convention_selfcheck"][k]["bit_exact"]
                            for k in REG_KEYS))

    # ---- the gate assembly (evaluated exactly once) ----------------------
    g1 = dict(counts)
    g1.update({"n_err_289_ok": n_err_289, "n_verified_289_ok": n_ver_289,
               "n_trace_289_ok": n_ts_289, "n_steps_289_ok": n_steps_289,
               "n_walk_end_289_ok": n_we_289,
               "n_err_exact_289_ok": n_ee_289,
               "n_ncommits_289_ok": n_nc_289,
               "n_commitsha_289_ok": n_cs_289,
               "n_cvt_289_ok": n_cvt_289, "n_histwrites_289_ok": n_hw_289,
               "n_mean_err_289_ok": n_mean_err_289,
               "n_mean_cvt_289_ok": n_mean_cvt_289,
               "chains_total_verified": chains["total_verified"],
               "source_deposits_read_only_byte_unchanged": ro_unchanged})
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
          "n_cvt_finite_ok": n_cvtfin,
          "n_a3_ok": n_a3, "n_conv_ok": n_conv,
          "n_trace_len_ok": n_tlen,
          "n_lock_reads": int(core["lock_reads"])}
    g3 = {"branch": branch,
          "bars": {"PREMIUM_DISSOLVED": PREMIUM_DISSOLVED,
                   "PREMIUM_CARRIED": PREMIUM_CARRIED},
          "bars_pre_named_at": ("030536f — fixed at pre-registration, "
                                "never fit"),
          "n_rows": len(rows),
          "n_stream_ok_rows": n_stream_ok,
          "n_register_ok_rows": n_reg_ok,
          "n_lock_reads": int(core["lock_reads"]),
          "n_frame_slots": len(host_table),
          "h0_echo_h1_carried": bool(counts["h0_echo_h1"]),
          "fresh_rhos_finite": rhos_finite,
          "convention_selfcheck_bit_exact": selfcheck_ok,
          "resolved": {"branch": branch,
                       "rho_mean_cvt~mia_prod_err": rho_mia,
                       "rho_mean_cvt~one_zone_premium": rho_prem,
                       "abs_rho_mia": abs(rho_mia),
                       "abs_rho_premium": abs(rho_prem)}}
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
        and g1["n_mia_carry"] == 12 and g1["n_prem_carry"] == 12
        and n_err_289 == 72 and n_ver_289 == 72 and n_ts_289 == 72
        and n_steps_289 == 72 and n_we_289 == 72 and n_ee_289 == 72
        and n_nc_289 == 72 and n_cs_289 == 72 and n_cvt_289 == 72
        and n_hw_289 == 72 and n_mean_err_289 == 12
        and n_mean_cvt_289 == 12
        and chains["total_verified"] == 29 and ro_unchanged)
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
                   and g2["n_cvt_finite_ok"] == 72
                   and g2["n_a3_ok"] == 72
                   and g2["n_conv_ok"] == 72
                   and g2["n_trace_len_ok"] == 72
                   and g2["n_lock_reads"] == 72)
    g3_pass = bool(
        g3["branch"] in ("PREMIUM-DISSOLVED", "PREMIUM-CARRIED",
                         "PREMIUM-MIXED")
        and g3["n_rows"] == 72 and g3["n_stream_ok_rows"] == 72
        and g3["n_register_ok_rows"] == 72 and g3["n_lock_reads"] == 72
        and g3["n_frame_slots"] == 12 and g3["h0_echo_h1_carried"]
        and g3["fresh_rhos_finite"]
        and g3["convention_selfcheck_bit_exact"])

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

    # ---- the hard rules (the exit re-assertion: the docstring + the
    #      header byte-pinned to 030536f, the 9 deposits byte-unchanged,
    #      the core + exp142 NOT modified) -------------------------------
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
            ("the core (the ported collective.py) was modified — the "
             "pre-registered NOT-modified rule")
        assert _sha(EXP142_FILE) == exp142_sha_entry, \
            "exp142 was modified after the work"

    if branch == "PREMIUM-DISSOLVED":
        branch_text = (
            "the carrier's improvement DISSOLVED the spec-layer premium — "
            "both fresh |rho| under the 0.40 bar (the committed pattern's "
            "host dependence collapsed as the errs converged under the "
            "self-history coupling): the premium was the un-coupled "
            "noise's host structure")
    elif branch == "PREMIUM-CARRIED":
        branch_text = (
            "the premium is CARRIED THROUGH the carrier — both fresh "
            "|rho| at or above the 0.60 bar (the committed pattern stays "
            "host-dependent under the self-history coupling): the premium "
            "is structural to the spec layer, not to the un-coupled noise")
    else:
        branch_text = (
            "the honest middle — the fresh |rho| straddle the pre-named "
            "bars (one face carried, one dissolved)")

    verdict_body = (
        f"{branch} — {branch_text}"
        f" (THE FRESH RHOS on the carrier's commits: "
        f"rho(mean_cvt)~mia_prod_err {rho_mia:+.4f} vs exp287's deposited "
        f"{float(dep287['regressions']['mean_cvt~mia_prod_err']['rho']):+.4f}"
        f" | rho(mean_cvt)~one_zone_premium {rho_prem:+.4f} vs exp287's "
        f"deposited "
        f"{float(dep287['regressions']['mean_cvt~one_zone_premium']['rho']):+.4f}"
        f"; the bars PREMIUM_DISSOLVED 0.40 / PREMIUM_CARRIED 0.60, fixed "
        f"at pre-registration, never fit; the convention self-check: the "
        f"copied machinery fed exp287's own deposited carrier reproduces "
        f"exp287's deposited rhos BIT-EXACT 2/2"
        f" | THE CARRIER ANCHOR (G1, fail=STOP): the g=1.0 carrier rows "
        f"reproduce exp289's deposited g=1.0 records BIT-EXACT — the errs "
        f"{n_err_289}/72 (the verified flags {n_ver_289}/72, the trace "
        f"shas {n_ts_289}/72, walk_end {n_we_289}/72, err_exact "
        f"{n_ee_289}/72) AND the commit layer (the commit-sequence "
        f"digests {n_cs_289}/72, cvt_rms {n_cvt_289}/72, n_commits "
        f"{n_nc_289}/72, walk_steps {n_steps_289}/72, the blend counts "
        f"{n_hw_289}/72) AND the per-host faces (the mean errs "
        f"{n_mean_err_289}/12, the mean_cvt {n_mean_cvt_289}/12 vs "
        f"exp289's deposited per-grid g=1.0 faces) — the SAME walk: the "
        f"commit layer is the carrier's, not a new instrument"
        f" | THE REGISTER FACE: the presence + the init == the spec "
        f"install asserted at the walk's start; at the walk's end the "
        f"register IS the commit replay {n_reg_replay}/72 with the "
        f"non-write-set face == the spec install {n_reg_comp}/72, finite "
        f"{n_reg_fin}/72"
        f" | R2'S ADDRESS (audit-only, never gating): the delta "
        f"correlation rho(delta_err, delta_cvt) "
        f"{core['delta_corr']['rho']:+.4f}; the exp288 pooled-R_max face "
        f"on the carrier's commits — "
        f"{core['pooled_face']['n_concentrating_hosts']}/12 hosts "
        f"concentrating (vs exp288's deposited SPEC-UNIFORM face, the "
        f"anchor's own R_max within "
        f"[{min(rb['rmax288'].values()):.4f}, "
        f"{max(rb['rmax288'].values()):.4f}]); the worst-err "
        f"{core['worst_face']['worst_err']:.2f} vs the 6.0 bar "
        f"({'under' if core['worst_face']['under_bar'] else 'AT/OVER'})"
        f" | 12 hosts, a deterministic sha-asserted rebuild (graph_path "
        f"for H0/H1, small_world at the deposited rewire seeds), the "
        f"provenance chains sha-verified {chains['total_verified']}/29 "
        f"(9 deposits: exp243 4 + exp256 3 + exp272 4 + exp273 5 + "
        f"exp282 4 + exp287 5 + exp288 1 + exp289 2 + exp292 1 — the "
        f"pre-named split), 9 deposits READ-ONLY byte-unchanged, "
        f"one-pass ({len(rows)} decodes, in-process), floor -60.0")

    # ---- the discipline scans + the deposit form -------------------------
    deposit = {
        "exp": "exp294_premium_under_history",
        "claim": (
            "THE PREMIUM UNDER THE HISTORY CARRIER (batch 48, "
            "pre-registration commit 030536f): exp287's deposited rhos "
            "re-measured on the SELF g=1.0 carrier walks. The chain's "
            "standing finding (exp287): the premium lives in WHAT the "
            "program commits — rho(mean_cvt)~mia +0.8616 / ~premium "
            "+0.7790 on the un-coupled commits. THE OPEN QUESTION: the "
            "carrier (exp289's self-history coupling, landed "
            "HISTORY-CARRIED; exp292: self-sourced, dose-peaked at "
            "g ~ 1.0; exp293: protective under stress) improves the "
            "decode by re-coupling the commits to the cells' own history "
            "— does that improvement DISSOLVE the spec-layer premium "
            "(the committed pattern's host dependence collapses as the "
            "errs converge) or CARRY THROUGH it (the committed pattern "
            "stays host-dependent)? THE INSTRUMENT: exp289's landed body "
            "REUSED VERBATIM at its SELF g=1.0 arm (the register, the "
            "self-history coupling, the decode, the rebuild, the "
            "deposit-reading forms) — the SAME walk exp289's g=1.0 arm "
            "ran, anchored BIT-EXACT vs exp289's deposited g=1.0 records "
            "72/72 (fail=STOP); the only new code is the commit-layer "
            "regression read (exp287's house conventions verbatim) and "
            "the branch bars. Branch: PREMIUM-DISSOLVED iff BOTH fresh "
            "|rho| < 0.40; PREMIUM-CARRIED iff BOTH fresh |rho| >= 0.60; "
            "PREMIUM-MIXED otherwise"),
        "method": {
            "instrument": (
                "exp289's landed body REUSED VERBATIM as the instrument "
                "base at its SELF g=1.0 arm: the traced replica with the "
                "register live (the presence + the init asserted at the "
                "walk's start, the population after each commit write, "
                "the survival + the replay equality + the complement "
                "asserted at the walk's end) and the self-history blend "
                "(the canon-boundary class restriction, "
                "effective = (1 - g) * theta_new + g * phi_history[i]) "
                "armed at g = 1.0 — exp289's landed best grid point "
                "(asserted against the deposit); the decode, the "
                "sha-asserted rebuild and the deposit-reading forms "
                "likewise verbatim"),
            "anchor": (
                "the carrier battery's errs + verified flags + trace "
                "shas reproduce exp289's deposited g=1.0 records "
                "BIT-EXACT 72/72 (fail=STOP per row), extended to the "
                "commit-sequence digests + cvt_rms + n_commits + "
                "walk_steps + walk_end_rms + err_exact + blend counts "
                "72/72 and the per-host mean faces 12/12 — the commit "
                "layer read is the carrier's, not a new instrument; NO "
                "new decodes beyond the one carrier battery"),
            "commit_layer_read": (
                "per row the commit-vs-target RMS cvt_rms (the exp287 "
                "form) on the carrier's commits; per host the 6-row "
                "mean_cvt; the anchor regressions rho(mean_cvt)~"
                "mia_prod_err and ~one_zone_premium under the house "
                "conventions (exp274/exp275/exp282/exp287 VERBATIM: "
                "Spearman = Pearson on the tied-average ranks via scipy "
                "rankdata; the single-predictor OLS rank R2; the ties "
                "census per vector) on the 12-slot frame with the "
                "H0==H1 echo carried; the CONVENTION SELF-CHECK: the "
                "copied machinery fed exp287's own deposited carrier "
                "(its host-table mean_cvt) + the same carries must "
                "reproduce exp287's deposited rhos BIT-EXACT (asserted)"),
            "branch_rule": (
                "PREMIUM-DISSOLVED iff BOTH fresh |rho| < 0.40; "
                "PREMIUM-CARRIED iff BOTH fresh |rho| >= 0.60; "
                "PREMIUM-MIXED otherwise; the bars fixed at "
                "pre-registration 030536f, never fit"),
            "audit_faces": (
                "R2: the per-host mean err deltas vs the g=0.0 control "
                "(exp289's deposited form) vs the per-host mean_cvt "
                "deltas vs exp287's deposited g=0.0 commit layer — the "
                "delta correlation (the house conventions, audit-only); "
                "exp288's pooled-R_max class-blindness face on the "
                "carrier's commits (exp208's classify VERBATIM, exp288's "
                "pooling, exp288's pre-named bars CONC_BAR 1.50 / "
                "CONC_MIN_HOSTS 10 — audit-only, never gating); the "
                "worst-err vs the 6.0 bar (unchanged, audit-only)"),
            "core": (
                "cultivation/bioelectric/collective.py (the exp289 port) "
                "CONSUMED AS LANDED — exp294 adds NOTHING to the core "
                "and modifies no file outside itself; exp142 NOT "
                "modified (both shas recorded at entry, re-asserted at "
                "exit, and sha-verified against exp289's deposited port "
                "record in the provenance chains)"),
            "chain_scope": (
                "the 9-deposit chain reads, per deposit, the pre-named "
                "record with the pre-named record counts (exp243 4 + "
                "exp256 3 + exp272 4 + exp273 5 + exp282 4 + exp287 5 + "
                "exp288 1 + exp289 2 + exp292 1 = 29): the first six "
                "records read whole; exp288's/exp292's inputs scoped to "
                "the NEW chain link each adds (exp287_deposit / "
                "exp289_deposit — the earlier links are the chain's own "
                "earlier sources); exp289's port record read whole (the "
                "ported collective.py + exp142 — the NOT-modified "
                "anchors)"),
            "run_form": (
                "the in-process default, one pass (the pre-named RUN "
                "clause: 72 decodes + the asserts, under the 570 s cap)"),
            "scope": (
                "the full commit sequences, traces, final states and "
                "register arrays NOT re-deposited — bit-reproduced via "
                "the per-row digests (commit_seq_sha256, trace_sha256, "
                "phi_history_sha256) + the carrier anchor (the "
                "exp284/exp285/exp286/exp287/exp288/exp289 precedent); "
                "no wall-clock fields")},
        "inputs": {
            name: {
                "path": f"results/{os.path.basename(p)}",
                "sha256": ro_before[name],
                "role": role}
            for (p, name), role in zip(_dep_names.items(), (
                "the classes records — the rebuild's sha anchors "
                "(base_sha256, edges_base, n_boundary_cells_base, "
                "rewire_seed, n, f_max_base) + the mia audit errs",
                "the 72 rows — the substituted instance structure the "
                "battery keys are read from (the errs' anchor is exp289's "
                "g=1.0 face)",
                "the host frame + the per-host one-zone premium means "
                "+ the boundary counts + the outlier pre-name source",
                "the outlier pre-name + the field-table carries",
                "the S0 walk anchor deposit — the 72 per-row walk faces "
                "the rebuild re-asserts (TRAJECTORY-CARRIED)",
                "the deposited rhos (the comparison targets: "
                "mean_cvt~mia_prod_err +0.8616 / mean_cvt~"
                "one_zone_premium +0.7790) + the g=0.0 commit-layer "
                "host table (R2's delta base) + the S0 commit-layer "
                "anchor the rebuild re-asserts",
                "the deposited SPEC-UNIFORM face — the per-host pooled "
                "R_max anchor + its own fresh errs (the chain face)",
                "THE CARRIER ANCHOR — the deposited g=1.0 per-row "
                "records (errs, verified flags, trace shas, commit "
                "digests, cvt_rms, walk faces, blend counts), the "
                "per-grid g=1.0 host faces, the g=0.0 control means, "
                "the landed best grid point, the port record (the "
                "NOT-modified anchors)",
                "the chain record (the pre-named new link "
                "exp289_deposit) — the immediately prior batch's "
                "dose-source face, READ-ONLY"))},
        "port": {
            "file": "cultivation/bioelectric/collective.py",
            "sha256": port_sha_entry,
            "modified": False,
            "note": ("the exp289 port consumed as landed — exp294 adds "
                     "nothing to the core; the register's presence/init/"
                     "population/survival asserted per row by the "
                     "reused replica"),
            "exp142_modified": False,
            "exp142_sha256": exp142_sha_entry},
        "hosts": hosts,
        "outliers": outliers,
        "cluster": cluster,
        "rebuild_report": rb["rebuild_report"],
        "provenance_chains": chains,
        "targets": rb["targets"],
        "exp287_reread": {
            "n_rows": counts["n_rows287"],
            "branch": dep287["branch"],
            "host_table_mean_cvt": rb["mean_cvt287"],
            "deposited_rhos": {
                k: float(dep287["regressions"][k]["rho"])
                for k in REG_KEYS},
            "convention_selfcheck": core["convention_selfcheck"]},
        "exp289_reread": {
            "branch": dep289["branch"],
            "g_ctx_grid": dep289["grid"]["g_ctx_grid"],
            "best_grid_point": dep289["grid"]["best_grid_point"],
            "g1_records_used": len(anchor["rows"]),
            "control_means_g0": anchor["control_means"],
            "g1_host_mean_err": anchor["host_mean_err"],
            "g1_mean_cvt": anchor["mean_cvt"]},
        "rows": rows,
        "host_table": host_table,
        "regressions": regressions,
        "branch": branch,
        "branch_discriminant": {
            "bars": {"PREMIUM_DISSOLVED": PREMIUM_DISSOLVED,
                     "PREMIUM_CARRIED": PREMIUM_CARRIED},
            "bars_pre_named_at": ("030536f — fixed at pre-registration, "
                                  "never fit"),
            "fresh": {
                "rho_mean_cvt~mia_prod_err": rho_mia,
                "rho_mean_cvt~one_zone_premium": rho_prem,
                "abs_rho_mia": abs(rho_mia),
                "abs_rho_premium": abs(rho_prem)},
            "comparison_rhos_exp287_deposited": {
                k: float(dep287["regressions"][k]["rho"])
                for k in REG_KEYS},
            "resolved": {"branch": branch,
                         "carried": branch == "PREMIUM-CARRIED",
                         "dissolved": branch == "PREMIUM-DISSOLVED",
                         "mixed": branch == "PREMIUM-MIXED"}},
        "audit_r2_address": {
            "delta_correlation": core["delta_corr"],
            "pooled_rmax_at_carrier": core["pooled_face"],
            "pooled_rmax_anchor_exp288": {
                "source": "exp288's deposited face (READ-ONLY)",
                "branch": dep288["branch"],
                "per_host_R_max": rb["rmax288"]},
            "worst_err": core["worst_face"]},
        "gates": None,          # filled below
        "verdict": None,        # assembled after the G4 resolution
        "determinism": {
            "form": "in-process default (one invocation)",
            "discipline": "deterministic one-pass carrier battery",
            "decodes": {"carrier_battery_g_1.0": 72},
            "same_walk_proof": (
                "the carrier battery reproduces exp289's deposited g=1.0 "
                "records bit-exact (the errs + the verified flags + the "
                "trace shas + the commit-sequence digests + cvt_rms + "
                "n_commits + walk_steps + walk_end_rms + err_exact + "
                "the blend counts, 72/72, fail=STOP per row; the "
                "per-host mean faces 12/12) — the commit layer read is "
                "the carrier's"),
            "no_checkpoint_caches": True},
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
    gates = {
        "G1_the_carrier_anchor": {
            "pass": g1_pass,
            "counts": g1,
            "provenance_chains": chains,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "carrier_anchor": (
                "the 72-row carrier battery at the SELF g=1.0 arm "
                "reproduces exp289's deposited g=1.0 records BIT-EXACT "
                "(the errs 72/72, the verified flags 72/72, the trace "
                "shas 72/72 — fail=STOP per row; the commit-sequence "
                "digests + cvt_rms + n_commits + walk_steps + walk_end "
                "+ err_exact + blend counts 72/72; the per-host mean "
                "faces 12/12) — the SAME walk, the commit layer is the "
                "carrier's; the 12 bases rebuilt sha-asserted vs "
                "exp243 (the exp269/exp280 form); the deep targets "
                "72/72; the carries mia + premium bit-exact 12/12 + "
                "12/12; the provenance chains sha-verified 29/29 (9 "
                "deposits, the pre-named split); the source deposits "
                "READ-ONLY byte-unchanged")},
        "G2_the_commit_layer_definition": {
            "pass": g2_pass,
            "counts": g2,
            "zero_knob_definition": (
                "per carrier row (fail=STOP): the commit count == "
                "walk_steps == the trace length; the commit indices "
                "unique; the write-set coverage; the values finite; the "
                "digest recorded (the full sequences NOT re-deposited); "
                "cvt_rms finite; the A3 convention; the trace integrity "
                "+ the TA3 convergence point; the S* lock reads 72; the "
                "register's replay equality (exp289's G2 form, the "
                "PER-ARM scope: phi_history[write_set] == the commit "
                "replay BIT-EXACT, the non-write-set face == the spec "
                "install, finite) 72/72")},
        "G3_the_branch_discriminant": {
            "pass": g3_pass,
            "bars": ("the fresh rhos vs the pre-named PREMIUM_DISSOLVED "
                     "0.40 / PREMIUM_CARRIED 0.60 bars (fixed HERE at "
                     "pre-registration, never fit); the regressions "
                     "under the house conventions verbatim (Spearman = "
                     "Pearson on the tied-average ranks; the 12-slot "
                     "frame with the H0==H1 echo carried); the "
                     "convention self-check bit-exact vs exp287's "
                     "deposited rhos; audit-only: R2's address reads"),
            "resolved": {"branch": branch,
                         "rho_mean_cvt~mia_prod_err": rho_mia,
                         "rho_mean_cvt~one_zone_premium": rho_prem}},
        "G4_discipline": {
            "pass": None}}   # filled after the discipline scans
    n_pass = 0
    n_refute = 0
    for name in ("G1_the_carrier_anchor",
                 "G2_the_commit_layer_definition",
                 "G3_the_branch_discriminant"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    core_not_modified = bool(_sha(PORT_FILE) == port_sha_entry)
    exp142_not_modified = bool(_sha(EXP142_FILE) == exp142_sha_entry)
    gates["G4_discipline"] = {
        "pass": bool(no_wall_clock and docstring_ok and header_ok
                     and ro_unchanged and core_not_modified
                     and exp142_not_modified),
        "run_form": "in-process default (one invocation)",
        "deterministic_one_pass_carrier_battery": True,
        "same_walk_asserted_via_g1": (
            "the bit-exact errs + trace shas + commit digests 72/72"),
        "no_wall_clock_fields": no_wall_clock,
        "docstring_byte_unchanged_vs_030536f": docstring_ok,
        "header_byte_unchanged_vs_030536f": header_ok,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "n_source_deposits": len(READ_DEPS),
        "exp142_not_modified": exp142_not_modified,
        "core_not_modified": core_not_modified,
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

    deposit["discipline"] = {
        "docstring_byte_unchanged_vs_030536f": docstring_ok,
        "header_byte_unchanged_vs_030536f": header_ok,
        "exp142_not_modified": exp142_not_modified,
        "core_not_modified": core_not_modified,
        "source_deposits_read_only_byte_unchanged": ro_unchanged,
        "n_source_deposits": len(READ_DEPS),
        "floor_at_exit": PROD_FLOOR,
        "reader_pin_floor_disclosed": READER_PIN_FLOOR,
        "zero_reader_scan": zero_reader_scan,
        "docstring_sha256": docstring_sha,
        "header_sha256": header_sha}

    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=str).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  G1 the carrier anchor: "
          f"{'PASS' if g1_pass else 'FAIL'} "
          f"(the rebuild sha-asserted {g1['n_sha_ok']}/12 + edges "
          f"{g1['n_edges_ok']}/12 + the boundary counts "
          f"{g1['n_bnd_dual_ok']}/12 + f_max {g1['n_fmax_ok']}/12; the "
          f"CARRIER ANCHOR — the errs == exp289's deposited g=1.0 errs "
          f"bit-exact {n_err_289}/72 (the verified flags {n_ver_289}/72, "
          f"the trace shas {n_ts_289}/72), the commit layer == exp289's "
          f"deposited g=1.0 commit layer {n_cs_289}/72 (cvt "
          f"{n_cvt_289}/72, n_commits {n_nc_289}/72); the deep targets "
          f"{g1['n_deep_targets_ok']}/72; the carries mia "
          f"{g1['n_mia_carry']}/12 + premium {g1['n_prem_carry']}/12; "
          f"the chains {chains['total_verified']}/29)")
    print(f"  G2 the commit layer's definition: "
          f"{'PASS' if g2_pass else 'FAIL'} "
          f"(the commit bookkeeping {n_count}/72 + unique {n_uniq}/72 + "
          f"coverage {n_cov}/72 + finite {n_fin}/72 + digests "
          f"{n_digests}/72; cvt finite {n_cvtfin}/72; the A3 convention "
          f"{n_a3}/72; the S* lock reads {core['lock_reads']}/72; the "
          f"register's replay equality {n_reg_replay}/72)")
    print(f"  G3 the branch discriminant: "
          f"{'PASS' if g3_pass else 'FAIL'} "
          f"(the fresh rhos: mean_cvt~mia_prod_err {rho_mia:+.4f} "
          f"[abs {abs(rho_mia):.4f}] vs exp287's deposited "
          f"{float(dep287['regressions']['mean_cvt~mia_prod_err']['rho']):+.4f}"
          f" | mean_cvt~one_zone_premium {rho_prem:+.4f} "
          f"[abs {abs(rho_prem):.4f}] vs exp287's deposited "
          f"{float(dep287['regressions']['mean_cvt~one_zone_premium']['rho']):+.4f}"
          f"; the bars PREMIUM_DISSOLVED {PREMIUM_DISSOLVED} / "
          f"PREMIUM_CARRIED {PREMIUM_CARRIED}; the convention self-check "
          f"bit-exact 2/2: {selfcheck_ok})")
    print("  R2's address reads (audit-only):")
    print(f"      the delta correlation "
          f"rho(delta_err, delta_cvt) {core['delta_corr']['rho']:+.4f} "
          f"| the per-host deltas: " + "; ".join(
              f"{row['host']} dErr {row['delta_err_vs_control']:+.3f} / "
              f"dCvt {row['delta_cvt_vs_exp287']:+.4f}"
              for row in host_table))
    print(f"      the pooled-R_max face on the carrier's commits: "
          f"{core['pooled_face']['n_concentrating_hosts']}/12 "
          f"concentrating (the exp288 anchor face: SPEC-UNIFORM, never "
          f"gating here) | the worst-err "
          f"{core['worst_face']['worst_err']:.2f} vs the 6.0 bar")
    print(f"  G4 discipline: "
          f"{'PASS' if gates['G4_discipline']['pass'] else 'FAIL'} "
          f"(deterministic one-pass, form in-process; no wall-clock "
          f"fields: {no_wall_clock}; 9 deposits READ-ONLY "
          f"byte-unchanged: {ro_unchanged}; exp142 NOT modified: "
          f"{exp142_not_modified}; the core NOT modified: "
          f"{core_not_modified}; floor -60.0 at exit, the -35.0 reader "
          f"pin disclosed)")
    print(f"\n  BRANCH: {branch} | fresh |rho|: mia "
          f"{abs(rho_mia):.4f}, premium {abs(rho_prem):.4f} vs the bars "
          f"PREMIUM_DISSOLVED {PREMIUM_DISSOLVED} / PREMIUM_CARRIED "
          f"{PREMIUM_CARRIED}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")

    # ---- the hard rules, re-asserted after the work ----------------------
    _exit_checks()
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
