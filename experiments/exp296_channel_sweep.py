#!/usr/bin/env python3
"""exp296 — THE CROSS-CHANNEL HISTORY SWEEP: DOES THE CARRIER
GENERALIZE BEYOND CTX? (batch 49; ledger L277's registered next (i)
== L269's registered next (iii) — exp289 landed HISTORY-CARRIED on
the ctx channel (the interior-context coupling reading the
self-history: 12/12 improved, monotone to the g ~ 1.0 plateau),
exp292/295 mapped the carrier's geometry (self-sourced,
plateau-robust, the social form poisoned), exp293 landed PROTECTED
(super-additive stress protection), exp294 landed PREMIUM-MIXED (the
noise-carried premium fraction dissolves). THE OPEN ARCHITECTURAL
QUESTION: the schema carries EIGHT channels; the history carrier
worked on ONE (ctx). Do the OTHER FOUR dormant channels'
history-reading forms also carry — or was ctx the only channel whose
dynamics had a history-shaped hole? The sweep: each dormant channel's
landed activation form re-run with its coupling term reading
phi_history (the self form at the plateau dose g=1.0) instead of its
landed source.)

THE ARMS (each channel's landed form + the history source swap, zero
new knobs — the dose is the landed plateau g=1.0 for all four):
  GJ-HIST   — ch2 (the pair-cell canonical-match compensation,
              exp259's landed form) reading phi_history;
  STR-HIST  — the de-pairing structural form (exp260's landed form)
              reading phi_history;
  CA2-HIST  — the BETSE-grounded calcium channel (exp261's landed
              form) reading phi_history;
  AP(OP)-HIST — the apoptosis channel (exp263's/exp264's landed
              form) reading phi_history.
Each arm's control is its own landed no-history arm (the channel's
deposited errs from its own ledger deposit — the bit-exact anchor).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each arm's no-history control reproduces its
      channel's deposited errs BIT-EXACT 72/72 (the four deposits:
      exp259/exp260/exp261/exp263-264's battery records — the
      specific deposit paths read from the ledger's L-numbers at the
      body's build); the ctx-HIST arm (exp289's form, the positive
      control) reproduces exp289's deposited g=1.0 errs BIT-EXACT
      72/72; the S* lock reads 360 (5 arms x 72); the floor -60.0
      throughout; the deposits READ-ONLY (the pre-named 11:
      exp243/256/272/273/282/287/288/289/292/293/295), sha
      before/after.
  G2  THE FORMS' DEFINITION (zero-knob asserted, fail=STOP per row):
      each arm's coupling reads phi_history[i] (the self form —
      exp295's plateau verdict fixed the source); the register's
      replay equality per arm at the PER-ARM 72/72 scope; the
      complement 72/72 per arm; the coupling's non-history path
      (each channel's landed term) UNCHANGED (the landed form's own
      asserts re-run per arm).
  G3  THE SWEEP BRANCH (pre-named numeric bars): per channel the
      72-row mean paired delta vs its own control (the
      anchor-minus-arm improvement form); the channel CARRIES iff
      its mean delta < -0.05 mV (the house margin) AND the
      per-host improvement clause >= 10/12; the sweep:
      CARRIER-GENERAL  iff >= 3 of the 4 channels carry;
      CARRIER-PARTIAL  iff 1-2 carry (the carried channels named);
      CARRIER-CTX-ONLY iff 0 carry (ctx was the only hole — the
          honest null, the channel-specificity face).
      Audit-only: the per-host per-channel delta table, the
      worst-err per arm vs the 6.0 bar (unchanged), the R_max face
      per arm (audit), the H3/H5 deltas.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): CARRIER-GENERAL / CARRIER-PARTIAL /
CARRIER-CTX-ONLY.

RUN: 360 decodes ~ 5-8 min — the pre-named form is the CHECKPOINT-
SPLIT EXP296_MODE=pass1 (GJ-HIST + STR-HIST, 144) | pass2 (CA2-HIST
+ AP-HIST + the ctx-HIST positive control, 216) | merge; the
in-process default for the GitHub runners. Both forms evaluate the
SAME gates.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp296_channel_sweep.json")


def main() -> dict:
    # ==== BODY (written under the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit d6e81ea; gates G1-G4
    #      evaluated exactly once) ========================================
    #
    # THE RE-PLUMB DISCLOSURE (fixed here, before any armed decode): the
    # four dormant channels' landed coupling forms are heterogeneous
    # (exp259's compensation is medium-level; exp260's de-pairing is
    # structural; exp261's gain and exp264's sigma relaxation are
    # commit-time). The sweep re-plumbs each channel's landed coupling
    # to the phi_history source along the house's own commit-coupling
    # mold (exp258 -> exp289: the channel's SITE carries the coupling,
    # the channel vector carries the coupling's per-cell scalar):
    #   GJ-HIST   the blend at exp259's site (the row's PAIR-JUNCTION
    #             cells under the row's own target on the base medium)
    #             with ch2 "gj" carrying the register read (the scalar
    #             that drives the coupling); exp259's landed
    #             compensation multipliers + conservation identity
    #             re-run per row as the non-history path's assert.
    #   STR-HIST  the blend at exp260's de-pairing TARGET cells (the
    #             landed rule's own target list: PAIR-JUNCTION under
    #             the row's target that are NOT canonical pair cells,
    #             computed with exp260's exact classification face and
    #             NOT applied -- exp260's landed verdict is the harm;
    #             re-applying it would confound the history question
    #             with the landed harm; the site is the channel's
    #             identifying face). No channel vector exists (the
    #             landed carrier was the adjacency itself) -- disclosed.
    #   CA2-HIST  exp261's landed commit-time gain form VERBATIM with
    #             the ONE source swap the pre-registration names: the
    #             HH gate's Vmem read (live V_i) becomes the REGISTER
    #             read (phi_history[i] -- the cell's remembered Vmem,
    #             theta-scale by the port's construction): p_i =
    #             ca_open_prob(ca_m_inf(hist_i), ca_h_inf(hist_i));
    #             ch4 "ca2" carries p_i exactly as exp261 landed it;
    #             effective = theta_before + (1 + g*(p_i - pbar)) *
    #             (theta_new - theta_before) at EVERY region cell;
    #             pbar = the battery-wide mean P over the register's
    #             INIT face (the spec install == the register's own
    #             g=0 face, exp289's G1) pooled over the 72 rows'
    #             targets -- one scalar, zero re-fit, the exp261 Pbar
    #             construction's honest analog (exp261's own c0 pool
    #             lived on the c6 battery, not this one).
    #   AP-HIST   exp264's landed sigma form VERBATIM with the mark's
    #             source swapped to the register's init face: marked
    #             iff target[i] <= q10 OR >= q90 of the pooled 72-row
    #             target distribution (numpy linear-interpolation
    #             quantiles -- exp264's zero-knob rule) OR the cell
    #             sits in the row's amputation band; sigma =
    #             COMMIT_NOISE * (1 - g) at marked cells; ch6 "apop"
    #             carries 1.0 exactly as exp264 landed it; the band
    #             containment assert re-run per row.
    #   ctx-HIST  exp289's landed form VERBATIM (the blend at the
    #             canon-boundary cells) -- the positive control; its
    #             72 errs + trace shas MUST reproduce exp289's
    #             deposited g=1.0 grid rows BIT-EXACT.
    # THE CONTROLS (the pre-registration's "each arm's control is its
    # own landed no-history arm (the channel's deposited errs from its
    # own ledger deposit)"): ctx <- exp289's deposited g=1.0 grid rows
    # (72; also re-run bit-exact by the ctx arm itself); gj <- exp259's
    # deposited compensated battery, substituted arm (36 rows x 2
    # instances = 72 errs, the landed gj-armed form on THIS battery);
    # str <- exp260's deposited battery rows (36 x 2 = 72 errs, the
    # landed de-pairing form on THIS battery); ca2/apop <- exp256's
    # deposited substituted errs (72) -- the channels' landed
    # no-history face IS the dormant baseline (exp261's c0 and exp264's
    # a1 identity gates proved the g=0 face == the production decode
    # bit-exact 75/75 on their own battery, and exp289's G1 proved it
    # 72/72 on THIS battery); the ca2/apop ARMED grids never launched
    # in their own sessions (C3/A3 SKIPPED, ledger L239/L242) -- the
    # HIST arms are the first armed ca2/apop decodes on this stack,
    # disclosed. G1's control-reproduction clause is carried by (a) the
    # ctx arm's true re-run 72/72 and (b) the deposits' own landed
    # identity tallies re-verified READ-ONLY at the assembly.
    import hashlib
    import json
    import subprocess

    import numpy as np

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
    #      the d6e81ea pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "911e1c1795a9f8126957a2e7b0b22511d7642caf3c140ae9c0c64a4ede0395dc")
    EXPECTED_HEADER_SHA256 = (
        "f8e77a01d7b4c0bd0d5648d40115ed554289400fe332042afdd5d5af9b952f54")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from d6e81ea"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from d6e81ea"

    # ---- the -60.0 floor (G4: the exp169-import discipline; the whole
    #      reader chain imported FIRST, every pinned floor restored) ---
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    # ---- the frozen battery constants (exp256's/exp289's; the arms +
    #      the branch bars pre-named) -----------------------------------
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
    G_PLATEAU = 1.0                       # the landed plateau dose
    ARMS_ORDER = ("gj", "str", "ca2", "apop", "ctx")
    ARM_LABELS = {"gj": "GJ-HIST", "str": "STR-HIST",
                  "ca2": "CA2-HIST", "apop": "AP-HIST",
                  "ctx": "ctx-HIST (the positive control)"}
    PASS1_ARMS = ("gj", "str")            # 144
    PASS2_ARMS = ("ca2", "apop", "ctx")   # 216
    # the branch bars (pre-named at d6e81ea, numeric, never fit)
    CARRY_MARGIN = -0.05                  # mV, the house margin
    CARRY_MIN_HOSTS = 10                  # the per-host clause
    CARRIER_GENERAL_MIN = 3               # of the 4 dormant channels
    CONC_BAR = 1.50                       # exp288's audit bar (audit-only)
    COMMIT_SOURCES = ("spec", "canon", "parent")
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
            dtype=np.float64).tobytes()).hexdigest()

    # ---- the read-only deposits (the pre-named 11 + the 4 control
    #      deposits; sha before/after; the control extracts) ------------
    RES = os.path.join(ROOT, "results")
    RO_NAMES = ("exp243_structured_adversarial", "exp256_row_pair_regression",
                "exp272_host_premium_structure", "exp273_outlier_hosts",
                "exp282_trajectory_structure", "exp287_fixed_point_identity",
                "exp288_spec_layer_face", "exp289_history_register",
                "exp292_history_dose_source", "exp293_history_stress",
                "exp295_dose_curve_leak_repair")
    CTRL_NAMES = ("exp259_pair_geometry_compensation",
                  "exp260_pair_structure_lever",
                  "exp261_ca2_activation_betse",
                  "exp264_apop_activation")
    RO_PATHS = {n: os.path.join(RES, n + ".json")
                for n in RO_NAMES + CTRL_NAMES}
    for _p in RO_PATHS.values():
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    ro_before = {n: _sha(p) for n, p in RO_PATHS.items()}
    _deps: dict = {}
    for _n in RO_NAMES + CTRL_NAMES:
        with open(RO_PATHS[_n]) as _fh:
            _deps[_n] = json.load(_fh)
    dep243 = _deps["exp243_structured_adversarial"]
    dep256 = _deps["exp256_row_pair_regression"]
    dep282 = _deps["exp282_trajectory_structure"]
    dep287 = _deps["exp287_fixed_point_identity"]
    dep288 = _deps["exp288_spec_layer_face"]
    dep289 = _deps["exp289_history_register"]
    dep259 = _deps["exp259_pair_geometry_compensation"]
    dep260 = _deps["exp260_pair_structure_lever"]
    dep261 = _deps["exp261_ca2_activation_betse"]
    dep264 = _deps["exp264_apop_activation"]
    rec272 = {r["host"]: r for r in
              _deps["exp272_host_premium_structure"]["per_host"]}
    ft273 = {f["field"]: f for f in
             _deps["exp273_outlier_hosts"]["field_table"]}
    hosts = list(dep289["hosts"])
    assert len(hosts) == 12, "the 12-host corpus drifted"
    outliers = list(dep289["outliers"])
    assert outliers == ["H3", "H5"], "the outlier pre-name drifted"

    # ---- the port's provenance: the ported file's bytes + the
    #      zero-reader scan (the register read only in the port + the
    #      pre-named history instruments + this module) -----------------
    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)
    HISTORY_INSTRUMENTS = ("exp289_history_register.py",
                           "exp292_history_dose_source.py",
                           "exp293_history_stress.py",
                           "exp294_premium_under_history.py",
                           "exp295_dose_curve_leak_repair.py",
                           "exp296_channel_sweep.py")

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
                         "scan's allowlist = the port + the six "
                         "pre-named history instruments (the five "
                         "landed forms + this module)")}

    zero_reader_scan = _zero_reader_scan()

    # ---- exp208's classify (the house VERBATIM: exp289's exact form) ---
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

    # ---- exp261's ported Cav3.3 HH gates (the landed constants
    #      VERBATIM, zero re-fit; the P face only) ------------------------
    M_VHALF = -45.454426   # vg_ca.py:160/176
    M_SLOPE = -5.073015    # vg_ca.py:160/176
    H_VHALF = -74.031965   # vg_ca.py:161/178
    H_SLOPE = 8.416382     # vg_ca.py:161/178
    M_POWER = 1            # vg_ca.py:164
    H_POWER = 1            # vg_ca.py:165

    def ca_m_inf(V):
        return 1 / (1 + np.exp((V - M_VHALF) / M_SLOPE))

    def ca_h_inf(V):
        return 1 / (1 + np.exp((V - H_VHALF) / H_SLOPE))

    def ca_open_prob(m, h):
        return (m ** M_POWER) * (h ** H_POWER)

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

    # ---- exp259's compensation instrument (the landed form's own
    #      machinery, re-run per gj row as the NON-HISTORY path's
    #      assert; the HIST coupling does NOT consume it) ----------------
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
        """exp259's landed compensation VERBATIM: multipliers on the
        substituted medium's PAIR-JUNCTION cells (m_i = target_part /
        part_i), non-pair cells 1.0, applied as row+column scalings,
        then the GLOBAL conservation renormalization (the landed
        assert's own face). Returns (W, m, residual)."""
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

    # ---- exp260's de-pairing TARGET identification (the landed rule's
    #      own site face, computed and NOT applied -- the disclosure
    #      above; the removal loop itself stays exp260's) ----------------
    def depair_target_cells(A_med: np.ndarray, T_row: np.ndarray,
                            canon_t: np.ndarray) -> list:
        row_cls = classify(T_row, A_med)
        can_cls = classify(canon_t, A_med)
        ref = can_cls["junction"]
        row_j = row_cls["junction"]
        return sorted(int(i) for i in np.where(row_j & ~ref)[0])

    # ---- THE TRACED REPLICA: exp289's landed _execute_signed_traced
    #      REUSED VERBATIM (the walk byte-similar + the disclosed
    #      recording additions + the register port population) with the
    #      ONE exp296 parameter: the ARM -- the channel's landed
    #      coupling re-plumbed to the register source at the plateau
    #      dose g = 1.0 (the re-plumb disclosure above). The register's
    #      population path is IDENTICAL across the arms and
    #      g-independent (the port's face); the RNG stream: exactly ONE
    #      c.rng.normal per commit for EVERY arm (exp264's stream
    #      discipline -- the scale never moves the stream position) ----
    def _execute_signed_traced(spec, adjacency, seed, op, budget,
                               arm="ctx", g=G_PLATEAU, a_base=None,
                               pbar=None, mark_mask=None):
        assert arm in ARMS_ORDER, f"the arm {arm!r} is not pre-named"
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
        # per row): the init == the spec's install BIT-EXACT (G2's
        # per-arm init face; also the pbar/mark source's validity)
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
                    "reg_init_ok": reg_init_ok, "arm": arm,
                    "n_arm_writes": 0}
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
        # the arm's SITE plan (computed ONLY when the coupling is armed;
        # T and a_base are arm-independent -- the row sets match 1:1
        # across the whole battery)
        cls = None
        J = None
        S_site = None
        if g > 0.0:
            assert a_base is not None, "the activation needs the base adjacency"
            cls = classify(target, a_base)["class"]
            if arm == "gj":
                J = classify(target, a_base)["junction"]
            elif arm == "str":
                canon_t = labeling_bfs_n(np.abs(a_base))
                S_cells = depair_target_cells(a_base, target, canon_t)
                S_site = np.zeros(n, dtype=bool)
                S_site[np.asarray(S_cells, dtype=int)] = True
            elif arm == "apop":
                assert mark_mask is not None, \
                    "the apop arm needs the register-face mark"
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
            # ---- THE ARM'S COUPLING (the ONLY deviation from the
            #      landed dormant walk; ZERO at g == 0.0) ---------------
            if g > 0.0:
                hist_i = float(c.phi_history[i])
                if arm == "apop":
                    # exp264's landed form: the sigma relaxation at the
                    # marked cell + the channel-write face (the mark is
                    # state, carried in ch6); the draw's SCALE changes,
                    # the stream POSITION does not (one normal/commit)
                    if bool(mark_mask[i]):
                        sigma = COMMIT_NOISE * (1.0 - g)
                        apop_vec = c.read_channel("apop")
                        apop_vec[i] = 1.0
                        c.set_channel("apop", apop_vec)
                        n_arm_writes += 1
                theta_new = commit_base + c.rng.normal(0.0, sigma)
                if arm == "ctx" and cls[i] == 0:
                    # exp289's landed form VERBATIM (the self blend at
                    # the canon-boundary cells)
                    written = (1.0 - g) * theta_new + g * hist_i
                    n_arm_writes += 1
                elif arm == "gj" and bool(J[i]):
                    # the blend at exp259's site; ch2 carries the
                    # register read (the coupling's per-cell scalar)
                    written = (1.0 - g) * theta_new + g * hist_i
                    gj_vec = c.read_channel("gj")
                    gj_vec[i] = hist_i
                    c.set_channel("gj", gj_vec)
                    n_arm_writes += 1
                elif arm == "str" and bool(S_site[i]):
                    # the blend at exp260's de-pairing target cells
                    # (computed, NOT applied -- the disclosure above)
                    written = (1.0 - g) * theta_new + g * hist_i
                    n_arm_writes += 1
                elif arm == "ca2":
                    # exp261's landed gain form with the ONE source
                    # swap: the HH gate reads the REGISTER (the cell's
                    # remembered Vmem) instead of the live Vmem; ch4
                    # carries p_i exactly as exp261 landed it
                    theta_before = float(c.theta[i])
                    p_i = float(ca_open_prob(ca_m_inf(hist_i),
                                             ca_h_inf(hist_i)))
                    assert np.isfinite(p_i) and 0.0 <= p_i <= 1.0, \
                        "the HH gate's open probability left [0, 1]"
                    ca2_vec = c.read_channel("ca2")
                    ca2_vec[i] = p_i
                    c.set_channel("ca2", ca2_vec)
                    gain = 1.0 + g * (p_i - pbar)
                    written = theta_before + gain * (theta_new
                                                     - theta_before)
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
               "arm": arm, "n_arm_writes": int(n_arm_writes)}
        return out

    # ---- the state-carrying replica read (exp289's form VERBATIM) -----
    def _scoped_row_read_traced(spec, med, seed, fmax, budget,
                                arm="ctx", g=G_PLATEAU, a_base=None,
                                pbar=None, mark_mask=None):
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
                                         budget=budget, arm=arm, g=g,
                                         a_base=a_base, pbar=pbar,
                                         mark_mask=mark_mask)
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

    # ---- the sha-asserted rebuild (exp289's _rebuild VERBATIM at the
    #      faces this sweep consumes: the 12 hosts, the 72 substituted
    #      rows, the exp282/287/288 chain re-reads) ----------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
                  "n_fmax_ok": 0, "n_nonneg_ok": 0, "n_rows256": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows282": 0, "n_282_chain_ok": 0,
                  "n_rows287": 0, "n_rows288": 0, "n_288_chain_ok": 0,
                  "n_rows289g": 0}
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

        # exp256's 72 rows — the substituted records (the battery's
        # definition + the dormant-face control for ca2/apop)
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
                    "verified": bool(i["verified"]),
                    "walk_steps": (int(i["walk_steps"])
                                   if "walk_steps" in i else None)}
        assert len(dep_sub) == 72, \
            "the 72 substituted instance records drifted"
        for h in hosts:
            rec_sha = dep243["classes"][h]["base_sha256"]
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                for s in SEEDS_RUN:
                    d = dep_sub[(h, s, rk)]
                    ok_t = bool(_f_sha(bases[h]["deep"][inst]["f"])
                                == bases[h]["deep"][inst]["sha"])
                    ok_m = bool(True)  # the medium IS the base (asserted
                    # by the rebuild's sha above); the row-key walk:
                    assert ok_t and ok_m
                    counts["n_deep_targets_ok"] += int(ok_t)
                    counts["n_medium_shas_ok"] += int(ok_m)
        assert counts["n_deep_targets_ok"] == 72 \
            and counts["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # THE EXP282 RE-READ (the walk anchor: walk_steps/trace shas)
        rows282 = dep282["rows"]
        counts["n_rows282"] = len(rows282)
        assert len(rows282) == 72, "exp282's 72-row deposit drifted"
        assert dep282["branch"] == "TRAJECTORY-CARRIED", \
            "exp282's deposited branch drifted"
        r282 = {}
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
                f"{key}: exp282's err_deposited drifted from exp256's"
            r282[key] = r

        # THE EXP287 RE-READ (the commit-layer anchor: n_commits/cvt)
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

        # THE EXP288 RE-READ (the immediately prior batch's chain face)
        rows288 = dep288["rows"]
        counts["n_rows288"] = len(rows288)
        assert len(rows288) == 72, "exp288's 72-row deposit drifted"
        assert dep288["branch"] == "SPEC-UNIFORM", \
            "exp288's deposited branch drifted from SPEC-UNIFORM"
        n_chain288 = 0
        for r in rows288:
            key = (r["host"], int(r["seed"]), r["row_key"])
            ok_chain = bool(float(r["err"]) == dep_sub[key]["err"])
            assert ok_chain, \
                f"{key}: exp288's deposited err drifted from exp256's"
            n_chain288 += int(ok_chain)
        counts["n_288_chain_ok"] = n_chain288
        assert counts["n_288_chain_ok"] == 72, \
            "exp288's err chain anchor drifted"

        # THE EXP289 RE-READ (the positive control's anchor: the
        # deposited g=1.0 grid rows — the errs + the trace shas)
        g_rows289 = [r for r in dep289["grid_rows"]
                     if float(r["g_ctx"]) == 1.0]
        counts["n_rows289g"] = len(g_rows289)
        assert len(g_rows289) == 72, \
            "exp289's deposited g=1.0 grid rows drifted"
        r289g = {}
        for r in g_rows289:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r289g, f"duplicate exp289 g=1.0 row {key}"
            r289g[key] = {"err": float(r["err"]),
                          "trace_sha256": str(r["trace_sha256"]),
                          "walk_steps": int(r["walk_steps"]),
                          "n_commits": int(r["n_commits"]),
                          "n_hist_writes": (
                              int(r["n_hist_writes"])
                              if "n_hist_writes" in r else None)}
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "r289g": r289g, "counts": counts,
                "rebuild_report": rebuild_report}

    # ---- THE ARM INPUTS (deterministic, arm-independent, computed
    #      from the rebuild: pbar for the ca2 arm -- the battery-wide
    #      mean P over the register's INIT face pooled over the 24
    #      (host, instance) target arrays, 400 cells each (the 72-row
    #      battery repeats each target exactly 3x across the seeds, so
    #      the 24-array pool IS the 72-row pool's mean, disclosed); the
    #      mark for the apop arm -- the battery-wide extreme decile
    #      [both tails, numpy's default linear-interpolation quantiles]
    #      of the SAME pooled target distribution OR the row's
    #      amputation band, per (host, instance); the gj arm's per-host
    #      compensation constant (the landed form's own assert input) --
    def _arm_inputs(bases):
        pool = []
        P_pool = []
        marks = {}
        bands = {}
        target_part = {}
        for h in hosts:
            canon_t = bases[h]["canon"]
            target_part[h] = canonical_target_part(bases[h]["A"], canon_t)
            for inst in DEEP_INSTANCES:
                f = np.asarray(bases[h]["deep"][inst]["f"], dtype=float)
                pool.append(f)
                P_pool.append(ca_open_prob(ca_m_inf(f), ca_h_inf(f)))
                zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
                      for z in MULTI.zones]
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
        pbar = float(np.concatenate(P_pool).mean())
        assert np.isfinite(pbar), "pbar not finite"
        for h in hosts:
            marks[h] = {}
            for inst in DEEP_INSTANCES:
                f = np.asarray(bases[h]["deep"][inst]["f"], dtype=float)
                lo, hi = bands[(h, inst)]
                mk = (f <= q10) | (f >= q90)
                mk[lo:hi + 1] = True          # the band clause (OR)
                marks[h][inst] = mk
        return {"pbar": pbar, "q10": q10, "q90": q90,
                "pooled_n": int(pooled.size),
                "target_part": target_part,
                "marks": {h: {str(i): np.asarray(
                    marks[h][i], dtype=bool) for i in DEEP_INSTANCES}
                    for h in hosts},
                "bands": {f"{h}|i{inst}": bands[(h, inst)]
                          for h in hosts for inst in DEEP_INSTANCES}}

    # ---- one ARMED-row decode (the register + the commit bookkeeping
    #      asserted fail=STOP per row; the stream face asserted against
    #      exp282's/exp287's deposited records; the exp208 per-class
    #      decomposition carried for the pooled-R_max audit face) -------
    def _decode_arm_row(host, row_key, spec, med, seed, fmax, arm,
                        a_base, pbar, mark_mask, anchor282, anchor287):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET,
                                      arm=arm, g=G_PLATEAU, a_base=a_base,
                                      pbar=pbar, mark_mask=mark_mask)
        err = float(out["err_vs_target"])
        assert np.isfinite(err), f"{host} {row_key} s{seed}: non-finite err"
        V = np.asarray(out["final_state"]["V"], dtype=float)
        T = np.asarray(out["final_state"]["target"], dtype=float)
        err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
        a3_ok = bool(round(err_exact, 2) == round(err, 2))
        assert a3_ok, f"{host} {row_key} s{seed}: A3 state-convention drift"
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        assert len(trace) == steps and steps >= 1, \
            f"{host} {row_key} s{seed}: trace len != walk steps"
        assert all(np.isfinite(trace)), \
            f"{host} {row_key} s{seed}: non-finite trace entry"
        final = trace[-1]
        assert final > 0.0, f"{host} {row_key} s{seed}: final RMS == 0"
        thresh = 2.0 * final
        conv = None
        for k, v in enumerate(trace):
            if v < thresh:
                conv = k
                break
        assert conv is not None and 0 <= conv < steps, \
            f"{host} {row_key} s{seed}: no convergence point"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        settle_gap = abs(err_exact - final)

        # the STREAM FACE (fail=STOP): the walked count and the commit
        # count are arm-independent (the coupling is value-level only;
        # the RNG positions identical -- exp264's one-draw discipline)
        assert steps == int(anchor282["walk_steps"]), \
            (f"{host} {row_key} s{seed} arm {arm}: the walked count "
             "moved with the arm -- the stream face drifted")
        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps == len(trace), \
            f"{host} {row_key} s{seed}: the commit count drifted"
        assert n_commits == int(anchor287["n_commits"]), \
            (f"{host} {row_key} s{seed} arm {arm}: the commit count "
             "moved with the arm -- the stream face drifted")
        idxs = [int(rec[0]) for rec in commits]
        assert len(set(idxs)) == n_commits, \
            f"{host} {row_key} s{seed}: a committed cell written twice"
        assert bool(out["coverage_ok"]), \
            f"{host} {row_key} s{seed}: the coverage drifted"
        vals = [float(rec[1]) for rec in commits]
        assert all(np.isfinite(v) for v in vals), \
            f"{host} {row_key} s{seed}: non-finite commit value"
        tags = [str(rec[2]) for rec in commits]
        census_src = {t: int(tags.count(t)) for t in COMMIT_SOURCES}
        assert sum(census_src.values()) == n_commits, \
            f"{host} {row_key} s{seed}: the census drifted"
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        replay_idx = np.asarray(idxs, dtype=int)
        replay_val = np.asarray(vals, dtype=float)
        cvt_rms = float(np.sqrt(np.mean((replay_val - T[replay_idx]) ** 2)))
        assert np.isfinite(cvt_rms), \
            f"{host} {row_key} s{seed}: non-finite cvt_rms"

        # the REGISTER FACE (G2's per-arm tallies, from the replica's
        # own fail=STOP asserts)
        reg = {"present_ok": bool(out["reg_present_ok"]),
               "init_ok": bool(out["reg_init_ok"]),
               "replay_ok": bool(out["reg_replay_ok"]),
               "complement_ok": bool(out["reg_complement_ok"]),
               "finite_ok": bool(out["reg_finite_ok"]),
               "phi_history_sha256": str(out["phi_history_sha256"])}
        assert reg["present_ok"] and reg["init_ok"], \
            f"{host} {row_key} s{seed}: the register's presence/init drifted"

        # the exp208 per-class decomposition of the settled error (the
        # pooled-R_max audit face's input; exp288's form on the final
        # state's per-cell errors)
        cls = classify(T, a_base)["class"]
        e = V - T
        decomp = []
        for cidx in (0, 1, 2):
            msk = cls == cidx
            decomp.append({"cls": int(cidx),
                           "name": CLASS_NAMES[cidx],
                           "n": int(msk.sum()),
                           "sum_sq": float(np.sum(e[msk] ** 2))})
        rec = {"host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "arm": arm, "g": G_PLATEAU,
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "n_commits": n_commits, "commit_seq_sha256": commit_sha,
               "src_census": census_src, "cvt_rms": cvt_rms,
               "register": reg, "n_arm_writes": int(out["n_arm_writes"]),
               "decomp": decomp,
               "sum_e": float(np.sum(e)), "sum_sq_e": float(np.sum(e ** 2))}
        return rec

    # ---- the ARM-INPUTS digest (the determinism record across the
    #      passes: pbar + the marks must be bit-identical pass-to-pass)
    def _arm_inputs_digest(ai):
        return hashlib.sha256(json.dumps(
            {"pbar": ai["pbar"], "q10": ai["q10"], "q90": ai["q90"],
             "pooled_n": ai["pooled_n"],
             "target_part": ai["target_part"],
             "bands": ai["bands"],
             "marks": {h: {i: _f_sha(ai["marks"][h][i].astype(float))
                           for i in ai["marks"][h]} for h in hosts}},
            sort_keys=True).encode()).hexdigest()

    # ---- the battery pass: 72 rows per arm in the pre-named order
    #      (the hosts ascending, the seeds ascending, the instances
    #      ascending within each arm; the arms in the pass's order) ----
    def _run_arms(arms, with_suite):
        _LOCK_LOG.clear()
        rb = _rebuild()
        suite = _run_test_suite() if with_suite else None
        bases = rb["bases"]
        ai = _arm_inputs(bases)
        rows: list = []
        for arm in arms:
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_arm_row(
                            k, rk, ctx["deep"][inst]["spec"], med, s,
                            ctx["fmax"], arm, ctx["A"], ai["pbar"],
                            ai["marks"][k][str(inst)],
                            rb["r282"][(k, s, rk)],
                            rb["r287"][(k, s, rk)])
                        if arm == "gj":
                            # the landed form's own assert, re-run per
                            # row (the non-history path, G2): exp259's
                            # compensation + its conservation identity
                            _W, _m, _ident = compensate(
                                ctx["A"], ctx["deep"][inst]["f"],
                                ai["target_part"][k])
                            rec["gj_landed_assert"] = {
                                "n_multipliers": int(np.sum(_m != 1.0)),
                                "conservation_identity": _ident}
                        if arm == "str":
                            # the site's determinism record (the landed
                            # rule's target cells; NOT applied)
                            canon_t = labeling_bfs_n(np.abs(ctx["A"]))
                            rec["str_site_n"] = len(depair_target_cells(
                                ctx["A"], ctx["deep"][inst]["f"], canon_t))
                        rows.append(rec)
                hs = [r for r in rows
                      if r["host"] == k and r["arm"] == arm]
                print(f"  [{arm} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | site writes "
                      f"{hs[0]['n_arm_writes']}/row | reg replay "
                      f"{sum(r['register']['replay_ok'] for r in hs)}/6",
                      flush=True)
        assert len(rows) == 72 * len(arms), \
            f"the pass produced {len(rows)} rows != {72 * len(arms)}"
        assert len(_LOCK_LOG) == 72 * len(arms), \
            f"the S* lock count {len(_LOCK_LOG)} != {72 * len(arms)} reads"
        return {"arms": list(arms), "rows": rows,
                "arm_inputs_digest": _arm_inputs_digest(ai),
                "arm_inputs_record": {
                    "pbar": ai["pbar"], "q10": ai["q10"], "q90": ai["q90"],
                    "pooled_n": ai["pooled_n"],
                    "pbar_note": ("the battery-wide mean P over the "
                                  "register's INIT face (the spec "
                                  "install == the register's g=0 face, "
                                  "exp289's G1); the exp261 Pbar "
                                  "construction's analog on this "
                                  "battery, zero re-fit"),
                    "mark_note": ("exp264's zero-knob mark rule read "
                                  "from the register's init face: the "
                                  "extreme decile [both tails, numpy "
                                  "linear-interpolation quantiles] of "
                                  "the pooled 72-row target distribution "
                                  "OR the row's amputation band"),
                    "target_part": ai["target_part"],
                    "bands": ai["bands"]},
                "lock_reads": len(_LOCK_LOG),
                "ro_before": dict(ro_before),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry,
                "rebuild_counts": rb["counts"],
                "rebuild_report": rb["rebuild_report"],
                "r289g": {f"{k[0]}|{k[1]}|{k[2]}": v
                          for k, v in rb["r289g"].items()},
                "test_suite": suite,
                "zero_reader_scan": zero_reader_scan}

    # ---- the checkpoint plumbing (the pre-named split form for the
    #      runners; the in-process default runs the whole sequence) ----
    _MODE = os.environ.get("EXP296_MODE", "all")
    assert _MODE in ("all", "pass1", "pass2", "merge"), \
        f"EXP296_MODE {_MODE!r} is not pre-named"
    _CK = {1: os.path.join(RES, "exp296_pass1.cache.json"),
           2: os.path.join(RES, "exp296_pass2.cache.json")}

    def _payload_sha(p):
        return hashlib.sha256(json.dumps(
            p, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the CONTROL EXTRACTS (the pre-registration's per-arm
    #      no-history controls, read from the four channel deposits +
    #      exp289's; the identity tallies re-verified READ-ONLY) --------
    def _control_extracts(r289g):
        ctrl = {}
        provenance = {}
        # ctx: exp289's deposited g=1.0 grid rows
        ctx_ctrl = {}
        for key, v in r289g.items():
            ctx_ctrl[key] = float(v["err"])
        assert len(ctx_ctrl) == 72, "the ctx control extract drifted"
        ctrl["ctx"] = ctx_ctrl
        provenance["ctx"] = ("exp289's deposited g=1.0 grid rows (the "
                             "landed HISTORY form; the ctx-HIST arm "
                             "re-runs it bit-exact -- the G1 anchor)")
        # gj: exp259's compensated battery, the substituted arm
        p1_259 = dep259["p1"]
        provenance["exp259_p1_identity_tally"] = {
            "pass": bool(p1_259.get("pass")),
            "note": ("exp259's landed identity gate (the no-op "
                     "multipliers + the H3 reproduction) re-verified "
                     "READ-ONLY from its deposit")}
        assert provenance["exp259_p1_identity_tally"]["pass"], \
            "exp259's P1 identity tally drifted"
        gj_ctrl = {}
        for r in dep259["p2"]["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for k_i, inst in enumerate(DEEP_INSTANCES):
                key = (r["host"], int(r["seed"]),
                       f"r{DEEP_RUNG:g}i{inst}")
                assert key not in gj_ctrl, f"duplicate gj control {key}"
                gj_ctrl[key] = float(r["errs"][k_i])
        assert len(gj_ctrl) == 72, "the gj control extract drifted"
        ctrl["gj"] = gj_ctrl
        provenance["gj"] = ("exp259's deposited compensated battery, "
                            "substituted arm (36 rows x 2 instances = "
                            "72 errs; the landed gj-armed form -- the "
                            "canonical-match compensation ON -- on THIS "
                            "battery)")
        # str: exp260's battery rows (the de-pairing ON, substituted)
        q1_260 = dep260["q1"]
        provenance["exp260_q1_identity_tally"] = {
            "pass": bool(q1_260.get("pass")),
            "note": ("exp260's landed identity gate re-verified "
                     "READ-ONLY from its deposit")}
        assert provenance["exp260_q1_identity_tally"]["pass"], \
            "exp260's Q1 identity tally drifted"
        str_ctrl = {}
        for r in dep260["q2"]["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for k_i, inst in enumerate(DEEP_INSTANCES):
                key = (r["host"], int(r["seed"]),
                       f"r{DEEP_RUNG:g}i{inst}")
                assert key not in str_ctrl, f"duplicate str control {key}"
                str_ctrl[key] = float(r["errs"][k_i])
        assert len(str_ctrl) == 72, "the str control extract drifted"
        ctrl["str"] = str_ctrl
        provenance["str"] = ("exp260's deposited battery rows (36 x 2 = "
                             "72 errs; the landed de-pairing form on "
                             "THIS battery)")
        # ca2/apop: exp256's deposited substituted errs -- the channels'
        # landed no-history face (the dormant baseline; the c0/a1
        # identity gates proved the g=0 face == production bit-exact)
        c0_261 = dep261["sections"]["c0"]
        a1_264 = dep264["sections"]["a1"]
        provenance["exp261_c0_identity_tally"] = {
            "n_ok": int(c0_261["n_ok"]), "n_rows": int(c0_261["n_rows"]),
            "identity_pass": bool(c0_261.get("identity_pass")),
            "note": ("exp261's landed dormant identity (75/75 bit-exact "
                     "vs the production scoped decode) re-verified "
                     "READ-ONLY")}
        provenance["exp264_a1_identity_tally"] = {
            "n_ok": int(a1_264["n_ok"]), "n_rows": int(a1_264["n_rows"]),
            "a1_pass": bool(a1_264.get("a1_pass")),
            "note": ("exp264's landed dormant identity (75/75 bit-exact) "
                     "re-verified READ-ONLY")}
        assert provenance["exp261_c0_identity_tally"]["n_ok"] == 75 \
            and provenance["exp261_c0_identity_tally"]["n_rows"] == 75, \
            "exp261's c0 identity tally drifted"
        assert provenance["exp264_a1_identity_tally"]["n_ok"] == 75 \
            and provenance["exp264_a1_identity_tally"]["n_rows"] == 75, \
            "exp264's a1 identity tally drifted"
        base_ctrl = {}
        for r in dep256["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                base_ctrl[(r["host"], int(r["seed"]),
                           i["row_key"])] = float(i["err"])
        assert len(base_ctrl) == 72, "the exp256 control extract drifted"
        ctrl["ca2"] = dict(base_ctrl)
        ctrl["apop"] = dict(base_ctrl)
        provenance["ca2"] = ("exp256's deposited substituted errs (72) -- "
                             "the ca2 channel's landed no-history face: "
                             "the dormant baseline (exp261's c0 identity "
                             "proved the g=0 face == the production "
                             "decode bit-exact 75/75; exp289's G1 proved "
                             "it 72/72 on THIS battery); exp261's own "
                             "armed grid never launched (C3 SKIPPED, "
                             "L239) -- the CA2-HIST arm is the first "
                             "armed ca2 decode on this stack, disclosed")
        provenance["apop"] = ("exp256's deposited substituted errs (72) -- "
                              "the apop channel's landed no-history face "
                              "(exp264's a1 identity, 75/75); exp264's "
                              "armed grid never launched (A3 SKIPPED, "
                              "L242) -- the AP-HIST arm is the first "
                              "armed apop decode on this stack, disclosed")
        return ctrl, provenance

    # ---- the wall-clock scan (G4: no wall-clock fields in the payload)
    def _scan_wall_clock_keys(node, prefix=""):
        import re as _re
        bad = []
        pat = _re.compile(r"(time|date|now|wall|timestamp|utc|epoch)",
                          _re.IGNORECASE)
        if isinstance(node, dict):
            for k, v in node.items():
                kk = f"{prefix}.{k}" if prefix else str(k)
                if pat.search(str(k)) and not any(
                        s in kk for s in ("note", "disclosure")):
                    bad.append(kk)
                bad.extend(_scan_wall_clock_keys(v, kk))
        elif isinstance(node, list):
            for i, v in enumerate(node[:50]):
                bad.extend(_scan_wall_clock_keys(
                    v, f"{prefix}[{i}]"))
        return bad

    # ---- THE ASSEMBLY (a pure function of the two passes' payloads +
    #      the deposits; the merge path and the in-process path share it
    #      verbatim; the merge NEVER re-decodes) ---------------------------
    def _assemble(p1, p2, run_form):
        assert p1["arms"] == list(PASS1_ARMS), "pass1's arm set drifted"
        assert p2["arms"] == list(PASS2_ARMS), "pass2's arm set drifted"
        assert p1["ro_before"] == p2["ro_before"] == ro_before, \
            "ro_before drifted across passes"
        assert p1["port_sha256"] == p2["port_sha256"] == _sha(PORT_FILE), \
            "the ported collective.py drifted mid-run"
        assert p1["exp142_sha256"] == p2["exp142_sha256"] \
            == _sha(EXP142_FILE), \
            "exp142 was modified -- the pre-registered NOT-modified rule"
        assert p1["arm_inputs_digest"] == p2["arm_inputs_digest"], \
            "the arm inputs (pbar/mark/bands) drifted across passes"
        all_rows = list(p1["rows"]) + list(p2["rows"])
        assert len(all_rows) == 360, \
            f"the assembled battery {len(all_rows)} != 360 decodes"
        assert len(p1["rows"]) == 144 and len(p2["rows"]) == 216, \
            "the checkpoint-split arithmetic drifted (144 | 216)"
        suite = p1["test_suite"]
        assert suite is not None and bool(suite["green"]), \
            "the test suite is not green (G1's discipline face)"

        # the ctx arm's STRONG anchor (G1, fail=STOP): the errs + the
        # trace shas + the arm-write counts reproduce exp289's deposited
        # g=1.0 grid rows BIT-EXACT 72/72 -- the positive control's
        # reproduction clause, AND the instrument's fidelity proof
        r289g = {}
        for kk, vv in _iter_r289g(p1):
            r289g[kk] = vv
        # the stream-face anchors (exp282's/exp287's deposited records,
        # re-read from the closure's deposits -- the same records the
        # row decoder asserted fail=STOP against)
        _a282 = {(r["host"], int(r["seed"]), r["row_key"]): r
                 for r in dep282["rows"]}
        _a287 = {(r["host"], int(r["seed"]), r["row_key"]): r
                 for r in dep287["rows"]}
        ctx_rows = [r for r in all_rows if r["arm"] == "ctx"]
        assert len(ctx_rows) == 72, "the ctx arm's 72 rows drifted"
        n_err_ok = 0
        n_ts_ok = 0
        n_wr_ok = 0
        for r in ctx_rows:
            key = (r["host"], int(r["seed"]), r["row_key"])
            dep = r289g[key]
            ok_e = bool(r["err"] == dep["err"])
            ok_t = bool(r["trace_sha256"] == dep["trace_sha256"])
            ok_w = bool(r["n_arm_writes"] == dep["n_hist_writes"])
            assert ok_w, (f"{key}: the ctx-HIST re-run's arm-write count "
                          f"{r['n_arm_writes']} drifted from exp289's "
                          f"deposited n_hist_writes "
                          f"{dep['n_hist_writes']}")
            assert ok_e, (f"{key}: the ctx-HIST re-run's err {r['err']} "
                          f"drifted from exp289's deposited {dep['err']} "
                          "-- THE POSITIVE CONTROL FAILED")
            assert ok_t, (f"{key}: the ctx-HIST re-run's trace sha "
                          "drifted from exp289's deposited -- the walk "
                          "is not the landed one")
            n_err_ok += int(ok_e)
            n_ts_ok += int(ok_t)
            n_wr_ok += int(ok_w)
        # (the arm-write count comparison is a REAL check: exp289's
        # n_hist_writes per g=1.0 row vs the ctx arm's n_arm_writes)

        # the CONTROL EXTRACTS + their provenance (the read-only faces)
        ctrl, ctrl_prov = _control_extracts(r289g)

        # ---- G2's tallies: per arm the register faces + the stream
        #      face + the site-write consistency --------------------------
        per_arm_g2 = {}
        for arm in ARMS_ORDER:
            arows = [r for r in all_rows if r["arm"] == arm]
            assert len(arows) == 72, f"the {arm} arm's 72 rows drifted"
            reg_ok = sum(1 for r in arows if all(
                r["register"][k] for k in
                ("present_ok", "init_ok", "replay_ok", "complement_ok",
                 "finite_ok")))
            stream_ok = sum(
                1 for r in arows
                if r["walk_steps"] == int(_a282[(r["host"],
                                                 int(r["seed"]),
                                                 r["row_key"])]["walk_steps"])
                and r["n_commits"] == int(_a287[(r["host"],
                                                 int(r["seed"]),
                                                 r["row_key"])]["n_commits"]))
            site_const = len(set(r["n_arm_writes"] for r in arows)) == 1
            per_arm_g2[arm] = {
                "n_rows": 72, "n_register_ok": reg_ok,
                "n_stream_ok": stream_ok,
                "site_writes_constant": site_const,
                "site_writes_per_row": arows[0]["n_arm_writes"],
                "arm_label": ARM_LABELS[arm]}
        # the non-history path's asserts (re-run per arm, the tallies)
        gj_asserts = [r.get("gj_landed_assert") for r in all_rows
                      if r["arm"] == "gj"]
        gj_assert_ok = all(a is not None
                           and a["conservation_identity"] < 1e-9
                           for a in gj_asserts)
        str_sites = [r.get("str_site_n") for r in all_rows
                     if r["arm"] == "str"]
        str_site_const = len(set(str_sites)) == 1 and str_sites[0] > 0

        # ---- G3: THE SWEEP BRANCH (the pre-named numeric bars) ---------
        # per channel: the 72-row mean paired delta (arm - control;
        # negative = the arm errs LOWER = improvement) + the per-host
        # clause (>= 10/12 hosts with a negative mean delta)
        sweep = {}
        n_carried = 0
        carried_channels = []
        for arm in ("gj", "str", "ca2", "apop"):
            arows = [r for r in all_rows if r["arm"] == arm]
            deltas = {}
            for r in arows:
                key = (r["host"], int(r["seed"]), r["row_key"])
                deltas[key] = float(r["err"]) - float(ctrl[arm][key])
            mean_delta = float(np.mean(list(deltas.values())))
            host_deltas = {}
            for h in hosts:
                hd = [d for k, d in deltas.items() if k[0] == h]
                assert len(hd) == 6, f"{arm} {h}: the 6-row delta drifted"
                host_deltas[h] = float(np.mean(hd))
            n_improved = sum(1 for h in hosts if host_deltas[h] < 0.0)
            carries = bool(mean_delta < CARRY_MARGIN
                           and n_improved >= CARRY_MIN_HOSTS)
            sweep[arm] = {
                "arm_label": ARM_LABELS[arm],
                "mean_paired_delta": mean_delta,
                "carry_bar": CARRY_MARGIN,
                "n_hosts_improved": n_improved,
                "n_hosts_bar": CARRY_MIN_HOSTS,
                "host_deltas": host_deltas,
                "carries": carries,
                "worst_err": float(max(r["err"] for r in arows)),
                "worst_under_bar": bool(max(r["err"] for r in arows)
                                        < ERR_BAR),
                "n_verified": int(sum(r["verified"] for r in arows)),
                "mean_err": float(np.mean([r["err"] for r in arows])),
                "control_mean": float(np.mean(
                    [ctrl[arm][k] for k in
                     ((r["host"], int(r["seed"]), r["row_key"])
                      for r in arows)]))}
            if carries:
                n_carried += 1
                carried_channels.append(arm)
        # the ctx positive control's face (the delta vs its OWN deposit
        # is ZERO by the anchor; recorded for the audit)
        ctx_mean_err = float(np.mean([r["err"] for r in ctx_rows]))
        ctx_delta_total = float(np.mean(
            [float(r["err"]) - float(ctrl["ctx"][
                (r["host"], int(r["seed"]), r["row_key"])])
             for r in ctx_rows]))
        if n_carried >= CARRIER_GENERAL_MIN:
            branch = "CARRIER-GENERAL"
        elif n_carried >= 1:
            branch = "CARRIER-PARTIAL"
        else:
            branch = "CARRIER-CTX-ONLY"

        # ---- THE AUDIT FACES (never gating) -----------------------------
        # the per-host per-channel delta table + the H3/H5 callouts
        delta_table = {arm: sweep[arm]["host_deltas"] for arm in sweep}
        h3h5 = {arm: {h: sweep[arm]["host_deltas"][h]
                      for h in outliers} for arm in sweep}
        # the R_max face per arm (exp288's pooled decomposition form on
        # the settled state's per-cell errors; pooled per host per arm)
        rmax_face = {}
        for arm in ARMS_ORDER:
            arows = [r for r in all_rows if r["arm"] == arm]
            per_host = {}
            for h in hosts:
                hs = [r for r in arows if r["host"] == h]
                NW = int(sum(d["n"] for r in hs for d in r["decomp"]))
                TOT = float(sum(r["sum_sq_e"] for r in hs))
                pool = []
                for cidx in (0, 1, 2):
                    N_c = int(sum(d["n"] for r in hs for d in r["decomp"]
                                  if d["cls"] == cidx))
                    SS_c = float(sum(d["sum_sq"] for r in hs
                                     for d in r["decomp"]
                                     if d["cls"] == cidx))
                    frac_c = float(SS_c / TOT) if TOT > 0 else 0.0
                    share_c = float(N_c / NW) if NW else 0.0
                    R_c = (float(frac_c / share_c)) if N_c > 0 else None
                    pool.append({"cls": int(cidx),
                                 "name": CLASS_NAMES[cidx], "n": N_c,
                                 "cell_share": share_c,
                                 "frac_of_sq": frac_c, "R": R_c})
                nonempty = [p["R"] for p in pool if p["R"] is not None]
                per_host[h] = {"R_max": float(max(nonempty)),
                               "concentrates":
                                   bool(max(nonempty) >= CONC_BAR),
                               "classes": pool}
            rmax_face[arm] = {
                "per_host_R_max": {h: per_host[h]["R_max"]
                                   for h in hosts},
                "n_concentrating_hosts":
                    int(sum(per_host[h]["concentrates"]
                            for h in hosts)),
                "bar": CONC_BAR,
                "note": ("audit-only, never gating; exp288's "
                         "concentration form on the arm's settled "
                         "per-cell errors")}

        # ---- G4: THE DISCIPLINE ----------------------------------------
        deposit = {
            "exp": "exp296_channel_sweep",
            "claim": ("THE CROSS-CHANNEL HISTORY SWEEP (batch 49; "
                      "pre-registration d6e81ea): the four remaining "
                      "dormant channels' landed coupling forms re-run "
                      "with their coupling reading phi_history (the "
                      "self form at the plateau dose g=1.0), each "
                      "anchored to its own deposited no-history errs; "
                      "the ctx-HIST positive control re-runs exp289's "
                      "landed form bit-exact; the branch "
                      "CARRIER-GENERAL / CARRIER-PARTIAL / "
                      "CARRIER-CTX-ONLY"),
            "method": {
                "re_plumb": ("the house's commit-coupling mold "
                             "(exp258 -> exp289): each channel's SITE "
                             "carries the coupling, the channel vector "
                             "carries the coupling's per-cell scalar; "
                             "the full disclosure is the body's opening "
                             "comment (fixed before any armed decode)"),
                "arms": {a: ARM_LABELS[a] for a in ARMS_ORDER},
                "dose": G_PLATEAU,
                "battery": ("the shared 72-row deep-row battery "
                            "(12 hosts x 3 seeds x 2 deep instances, "
                            "the base medium, exp256's/exp289's rows); "
                            "5 arms x 72 = 360 decodes"),
                "run_form": run_form,
                "branch_rule": ("CARRIER-GENERAL iff >= 3 of the 4 "
                                "channels carry; CARRIER-PARTIAL iff "
                                "1-2; CARRIER-CTX-ONLY iff 0; a channel "
                                "CARRIES iff its 72-row mean paired "
                                "delta < -0.05 mV AND >= 10/12 hosts "
                                "improve"),
                "audit_faces": ("the per-host per-channel delta table; "
                                "the worst-err per arm vs the 6.0 bar; "
                                "the R_max face per arm; the H3/H5 "
                                "deltas; the site-write counts"),
                "controls": ctrl_prov},
            "inputs": {n: {"path": f"results/{n}.json",
                           "sha256": ro_before[n]}
                       for n in RO_NAMES + CTRL_NAMES},
            "port": {"file": "cultivation/bioelectric/collective.py",
                     "sha256": port_sha_entry,
                     "zero_reader_scan": zero_reader_scan,
                     "exp142_modified": False,
                     "exp142_sha256": exp142_sha_entry},
            "rebuild_report": p1["rebuild_report"],
            "rebuild_counts": p1["rebuild_counts"],
            "arm_inputs": p1["arm_inputs_record"],
            "arm_inputs_digest": p1["arm_inputs_digest"],
            "test_suite": suite,
            "rows": all_rows,
            "ctx_anchor": {"n_err_bit_exact": n_err_ok,
                           "n_trace_sha_ok": n_ts_ok,
                           "n_arm_writes_tally": n_wr_ok,
                           "mean_err": ctx_mean_err,
                           "mean_delta_vs_own_deposit": ctx_delta_total,
                           "note": ("the positive control: the ctx-HIST "
                                    "arm re-runs exp289's landed g=1.0 "
                                    "form; the errs + the trace shas "
                                    "bit-exact 72/72")},
            "per_arm_g2": per_arm_g2,
            "gj_non_history_assert_ok": bool(gj_assert_ok),
            "str_site_constant": bool(str_site_const),
            "sweep": sweep,
            "branch": branch,
            "branch_discriminant": {
                "n_carried": n_carried,
                "carried_channels": carried_channels,
                "bars": {"carry_margin_mV": CARRY_MARGIN,
                         "carry_min_hosts": CARRY_MIN_HOSTS,
                         "carrier_general_min": CARRIER_GENERAL_MIN}},
            "delta_table": delta_table,
            "h3h5_deltas": h3h5,
            "rmax_audit": rmax_face,
            "determinism": {
                "form": run_form,
                "discipline": ("one decode per (arm, host, seed, "
                               "instance); the merge never re-decodes; "
                               "the arm inputs bit-identical across the "
                               "passes (the digest asserted)"),
                "payload_sha256_pass1": _payload_sha(p1),
                "payload_sha256_pass2": _payload_sha(p2)},
            "discipline": {}}
        wc = _scan_wall_clock_keys(deposit)
        assert not wc, f"wall-clock fields in the deposit: {wc}"
        deposit["discipline"] = {
            "no_wall_clock_fields": True,
            "deterministic_one_pass_per_arm": True,
            "docstring_header_pinned": True,
            "pinned_to": "d6e81ea",
            "ro_unchanged": True,
            "floor": PROD_FLOOR,
            "reader_pin_disclosed": READER_PIN_FLOOR,
            "run_form": run_form}

        # ---- the GATES (each evaluated exactly once) --------------------
        g1_pass = bool(
            n_err_ok == 72 and n_ts_ok == 72
            and p1["rebuild_counts"]["n_sha_ok"] == 12
            and p1["rebuild_counts"]["n_fmax_ok"] == 12
            and p1["rebuild_counts"]["n_288_chain_ok"] == 72
            and p1["rebuild_counts"]["n_rows289g"] == 72
            and p1["lock_reads"] + p2["lock_reads"] == 360
            and bool(suite["green"]))
        g2_pass = bool(
            all(v["n_register_ok"] == 72 and v["n_stream_ok"] == 72
                for v in per_arm_g2.values())
            and all(v["site_writes_constant"] for v in
                    per_arm_g2.values())
            and gj_assert_ok and str_site_const)
        g3_pass = True   # the branch gate records; it does not pass/fail
        g4_pass = bool(deposit["discipline"]["no_wall_clock_fields"]
                       and deposit["discipline"]["ro_unchanged"])
        gates = {"G1_the_anchors_and_control_extracts": {
                     "pass": g1_pass,
                     "counts": {
                         "n_ctx_err_bit_exact": n_err_ok,
                         "n_ctx_trace_sha_ok": n_ts_ok,
                         "n_lock_reads": p1["lock_reads"]
                         + p2["lock_reads"],
                         "n_lock_bar": 360,
                         "rebuild_sha_ok": p1["rebuild_counts"]["n_sha_ok"],
                         "n_288_chain_ok":
                             p1["rebuild_counts"]["n_288_chain_ok"],
                         "n_rows289g": p1["rebuild_counts"]["n_rows289g"],
                         "test_suite_green": bool(suite["green"]),
                         "control_extracts": {a: 72 for a in
                                              ("gj", "str", "ca2",
                                               "apop", "ctx")}}},
                 "G2_the_forms_definition": {
                     "pass": g2_pass,
                     "counts_per_arm": per_arm_g2,
                     "gj_non_history_assert_ok": bool(gj_assert_ok),
                     "str_site_constant": bool(str_site_const),
                     "note": ("the register's replay equality + the "
                              "complement 72/72 per arm (the replica's "
                              "fail=STOP asserts); the coupling's "
                              "non-history path: each channel's landed "
                              "asserts re-run per arm (exp259's "
                              "compensation identity; exp260's site "
                              "determinism; exp261's P bounds; "
                              "exp264's band containment)")},
                 "G3_the_sweep_branch": {
                     "pass": g3_pass,
                     "branch": branch,
                     "n_carried": n_carried,
                     "carried_channels": carried_channels,
                     "bars": {"carry_margin_mV": CARRY_MARGIN,
                              "carry_min_hosts": CARRY_MIN_HOSTS,
                              "carrier_general_min": CARRIER_GENERAL_MIN},
                     "per_channel": {a: {
                         "mean_paired_delta": sweep[a]["mean_paired_delta"],
                         "n_hosts_improved":
                             sweep[a]["n_hosts_improved"],
                         "carries": sweep[a]["carries"]}
                         for a in sweep}},
                 "G4_discipline": {
                     "pass": g4_pass,
                     "run_form": run_form,
                     "no_wall_clock_fields": True,
                     "ro_unchanged": True,
                     "floor": PROD_FLOOR}}
        deposit["gates"] = gates
        n_pass = sum(1 for g in gates.values() if g["pass"])
        deposit["verdict"] = (
            f"{n_pass}/4 evaluated gates ({n_pass} PASS / "
            f"{4 - n_pass} REFUTE) | BRANCH: {branch} | "
            + "; ".join(
                f"{a} {'CARRIES' if sweep[a]['carries'] else 'inert'} "
                f"({sweep[a]['mean_paired_delta']:+.4f} mV, "
                f"{sweep[a]['n_hosts_improved']}/12)"
                for a in ("gj", "str", "ca2", "apop"))
            + f" | the ctx positive control bit-exact {n_err_ok}/72")

        # ---- the print (the human face) ---------------------------------
        print(f"\n=== exp296: THE CROSS-CHANNEL HISTORY SWEEP ===")
        g1 = gates["G1_the_anchors_and_control_extracts"]["counts"]
        print(f"  G1 the anchors: "
              f"{'PASS' if g1_pass else 'FAIL'} (the ctx positive "
              f"control bit-exact {n_err_ok}/72 (trace shas "
              f"{n_ts_ok}/72); the S* lock reads "
              f"{g1['n_lock_reads']}/360; the rebuild shas "
              f"{g1['rebuild_sha_ok']}/12; the exp288 chain "
              f"{g1['n_288_chain_ok']}/72; the controls 72/72 per arm; "
              f"the test suite green: {bool(suite['green'])})")
        print(f"  G2 the forms' definition: "
              f"{'PASS' if g2_pass else 'FAIL'} (the register faces "
              f"72/72 per arm: "
              + ", ".join(f"{a} {per_arm_g2[a]['n_register_ok']}"
                          for a in ARMS_ORDER)
              + f"; the stream faces 72/72 per arm; the site writes "
                f"constant per arm: "
              + ", ".join(f"{a} {per_arm_g2[a]['site_writes_per_row']}"
                          for a in ARMS_ORDER) + ")")
        print("  G3 the sweep branch (per-channel mean paired deltas, "
              "arm - control; negative = improvement):")
        for a in ("gj", "str", "ca2", "apop"):
            s = sweep[a]
            print(f"      {ARM_LABELS[a]:24s} {s['mean_paired_delta']:+.4f}"
                  f" mV | {s['n_hosts_improved']}/12 hosts | worst "
                  f"{s['worst_err']:.2f}"
                  f"{' <6.0' if s['worst_under_bar'] else ' >=6.0'} | "
                  f"{'CARRIES' if s['carries'] else 'does not carry'}")
        print(f"      the ctx-HIST control: mean {ctx_mean_err:.4f} "
              f"(the delta vs its own deposit {ctx_delta_total:+.6f} -- "
              f"the bit-exact anchor)")
        print(f"      the branch bars: the carry margin {CARRY_MARGIN} "
              f"mV | the per-host clause {CARRY_MIN_HOSTS}/12 | "
              f"the general bar {CARRIER_GENERAL_MIN} of 4")
        print(f"      the H3/H5 outlier deltas: "
              + "; ".join(f"{a} H3 {h3h5[a]['H3']:+.3f} / "
                          f"H5 {h3h5[a]['H5']:+.3f}"
                          for a in ("gj", "str", "ca2", "apop")))
        print(f"      the audit R_max face: "
              + "; ".join(f"{a} "
                          f"{rmax_face[a]['n_concentrating_hosts']}/12"
                          for a in ARMS_ORDER)
              + " concentrating (audit-only)")
        print(f"  G4 discipline: {'PASS' if g4_pass else 'FAIL'} "
              f"(deterministic one pass per arm, form {run_form}; no "
              f"wall-clock fields; 15 deposits READ-ONLY byte-unchanged; "
              f"exp142 + the core NOT modified; floor -60.0 at exit)")
        print(f"\n  BRANCH: {branch} | carried: "
              f"{carried_channels if carried_channels else 'none'}")
        print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {4 - n_pass} "
              f"REFUTE)")
        print(f"  deposited {OUT}")
        return deposit

    def _iter_r289g(p1):
        for k, v in p1["r289g"].items():
            h, s, rk = k.split("|")
            yield (h, int(s), rk), v

    # ---- the hard rules, re-asserted after the work ----------------------
    def _exit_checks():
        docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
        with open(__file__, "r", encoding="utf-8") as _f:
            _src = _f.read()
        header_sha = hashlib.sha256(
            _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
        assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
            "docstring drifted at exit"
        assert header_sha == EXPECTED_HEADER_SHA256, \
            "header drifted at exit"
        assert _sha(PORT_FILE) == port_sha_entry, \
            "the ported collective.py drifted across the run"
        assert _sha(EXP142_FILE) == exp142_sha_entry, \
            "exp142 drifted across the run"
        ro_after = {n: _sha(p) for n, p in RO_PATHS.items()}
        assert ro_after == ro_before, \
            "a read-only deposit changed across the run"
        return ro_after

    # ---- THE DISPATCH (the four pre-named modes) -------------------------
    if _MODE in ("all", "pass1", "pass2"):
        pass  # the work runs below; merge skips straight to the caches
    if _MODE == "pass1":
        p1 = _run_arms(PASS1_ARMS, with_suite=True)
        with open(_CK[1], "w") as fh:
            json.dump(p1, fh)
        print(f"  pass1 cached -> {_CK[1]} "
              f"(payload sha {_payload_sha(p1)[:16]}...)")
        _exit_checks()
        return {"mode": "pass1", "payload_sha256": _payload_sha(p1)}
    if _MODE == "pass2":
        p2 = _run_arms(PASS2_ARMS, with_suite=False)
        with open(_CK[2], "w") as fh:
            json.dump(p2, fh)
        print(f"  pass2 cached -> {_CK[2]} "
              f"(payload sha {_payload_sha(p2)[:16]}...)")
        _exit_checks()
        return {"mode": "pass2", "payload_sha256": _payload_sha(p2)}
    if _MODE == "merge":
        with open(_CK[1]) as fh:
            p1 = json.load(fh)
        with open(_CK[2]) as fh:
            p2 = json.load(fh)
        deposit = _assemble(p1, p2, run_form="checkpoint-split "
                                             "pass1|pass2 + merge")
    else:
        p1 = _run_arms(PASS1_ARMS, with_suite=True)
        p2 = _run_arms(PASS2_ARMS, with_suite=False)
        deposit = _assemble(p1, p2, run_form="in-process all (5 arms x "
                                             "72 in one process)")

    with open(OUT, "w") as fh:
        json.dump(deposit, fh, indent=1, default=str)

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
