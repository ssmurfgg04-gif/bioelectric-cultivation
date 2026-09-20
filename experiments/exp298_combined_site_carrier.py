#!/usr/bin/env python3
"""exp298 — THE COMBINED-SITE CARRIER: WHAT DOES THE UNION OF THE
CARRYING FACES DO? (batch 52; ledger L281's registered next (a) —
exp296 landed CARRIER-GENERAL (three carrying sites at g=1.0) and
exp297 fixed the absolute dose faces (gj PEAKED-AT-1.0 at -0.2707,
apop CARRYING-MONOTONE to -0.3550 at saturation, str dose-inert vs
the absolute baseline — the control-dependence decomposition). THE
OPEN ARCHITECTURAL QUESTION: the three carrying faces (the ctx blend
at the canon-boundary cells, the gj blend at the pair-junction cells,
the apop sigma relaxation at the register-face marked cells) were
tested SEPARATELY. The sites are NOT disjoint — the apop mark's band
clause covers the whole walked region (the boundary and junction
cells included), and the extreme-decile clause adds the deep-value
cells. What does the UNION do: super-additive (the faces compound),
additive (the best single dominates), or interfering (the faces
fight over the same commits)?)

THE ARMS (the exp296 landed forms VERBATIM, composed on ONE walk via
the faces parameter — the anchor ladder proves the composition
bit-exact, then the union runs once):
  faces=("ctx",)  — exp289's blend at the canon-boundary cells; MUST
                    reproduce exp296's deposited ctx rows BIT-EXACT
                    72/72 (the anchor ladder, G1);
  faces=("gj",)   — the blend at exp259's pair-junction site, ch2
                    carrying the register read; MUST reproduce exp296's
                    deposited gj rows BIT-EXACT 72/72;
  faces=("apop",) — exp264's landed sigma form with the mark read from
                    the register's init face; MUST reproduce exp296's
                    deposited apop rows BIT-EXACT 72/72;
  faces=all three — THE UNION: the sigma face first (the draw's scale),
                    then the blends (the write's value), the channel
                    writes per face preserved; 72 fresh rows.
4 arms x 72 rows = 288 decodes on the shared deep-row battery at the
plateau dose g=1.0.

THE COUPLING ORDER (fixed here, before any union row): at the commit
of each walked cell — (1) the sigma face: if the cell is marked
(the register-face mark, exp296's), sigma = COMMIT_NOISE * (1 - g)
and ch6 carries 1.0; (2) the draw: theta_new = commit_base +
rng.normal(0, sigma) — ONE draw per commit (the stream discipline);
(3) the blend faces: if the cell is a canon-boundary cell (the ctx
face) or a pair-junction cell (the gj face, exp259's site), written =
(1 - g) * theta_new + g * phi_history[i], ch2 carrying the register
read at the gj cells. At a cell carrying BOTH blend faces the blend
is applied ONCE (the same value — the sites' blend forms are
identical; the overlap is recorded, not doubled). At a marked cell
outside both blend sites the sigma face acts alone; at a blend-site
cell outside the mark the blend acts alone.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS: each single-face arm reproduces exp296's deposited
      rows BIT-EXACT 72/72 (the errs + the trace shas — the
      composition's fidelity proof: the faces parameter changes
      nothing when a face runs alone); the rebuild chain asserted;
      the S* lock reads 288 (4 arms x 72); the floor -60.0; the
      deposits READ-ONLY (the pre-named 12 + the 4 control deposits),
      sha before/after; the test suite green.
  G2  THE FORMS: the register faces 72/72 per arm (present + init +
      replay + complement + finite); the stream faces 72/72 per arm
      vs exp282's/exp287's deposited walk_steps/n_commits; the
      site-write counts constant across seeds per (host, instance)
      and the per-row overlap audit recorded (the boundary ∩ mark,
      the junction ∩ mark, the blend-site ∩ mark counts); the gj
      landed assert re-run per row.
  G3  THE ADDITIVITY BRANCH (pre-named): the union's mean paired
      delta vs exp256's dormant baseline (the honest absolute
      control, exp297's lesson) compared with the BEST SINGLE's mean
      paired delta (the min of the three singles' deltas):
      SUPER-ADDITIVE  iff delta(union) <= delta(best single) - 0.05
                      (the union beats the best single by >= 0.05 mV);
      ADDITIVE        iff |delta(union) - delta(best single)| < 0.05;
      INTERFERING     iff delta(union) > delta(best single) + 0.05
                      (the faces fight);
      each with the per-host improvement count recorded (the 10/12
      clause as the audit). Audit-only: the per-host delta tables per
      arm, the worst-err per arm vs the 6.0 bar, the H3/H5 deltas,
      the R_max face per arm, the overlap census.
  G4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): SUPER-ADDITIVE / ADDITIVE / INTERFERING.

RUN: 288 decodes ~ 3-5 min — the in-process default runs the whole
sequence (the anchor ladder + the union); EXP298_MODE=all is the
pre-named form.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp298_combined_site_carrier.json")


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
        "4b6045088e0671b10dfe51de8ef394a573d0aaf446e8b591cee34753c36766f4")
    EXPECTED_HEADER_SHA256 = (
        "5c793332c4741800f30baddbe3863fbc111a6bbd1b929d710e6a5b8cc3cfc1aa")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from the exp298 pre-registration"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from the exp298 pre-registration"

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
    FACES_BATTERY = (("ctx",), ("gj",), ("apop",),
                     ("ctx", "gj", "apop"))
    ARM_NAMES = ("ctx-single", "gj-single", "apop-single", "UNION")
    G_PLATEAU = 1.0                       # the landed plateau dose
    # the additivity bars (pre-named at the exp298 pre-registration)
    ADDITIVITY_BAND = 0.05                # mV around the best single
    # THE DOMAIN DISCLOSURE (fixed here, disclosed in the ledger; the
    # run caught it before any apop row ran): the pre-registration's
    # ladder named 1.5 for ALL THREE sites, but the apop site's landed
    # form (exp264's sigma relaxation, sigma = COMMIT_NOISE * (1 - g))
    # has domain g in [0, 1] BY CONSTRUCTION -- sigma < 0 at g = 1.5
    # (the rng raised scale < 0). The honest fix: the apop ladder is
    # DOMAIN-RESTRICTED to {0.25, 0.5, 1.0}; the branch face for apop
    # reads on the available doses (the saturation at g=1.0 is the
    # form's own maximum BY CONSTRUCTION -- the pre-named apop
    # branches: DOSE-INERT / CARRYING-MONOTONE / MIXED). The docstring
    # pin stands (the pre-registration's bytes unchanged); this body
    # disclosure + the ledger entry carry the deviation.
    N_DECODES = len(FACES_BATTERY) * 72   # 288
    # the dose-branch bars are not used here (the single-dose battery)
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
                "exp295_dose_curve_leak_repair",
                "exp296_channel_sweep")
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
    dep296 = _deps["exp296_channel_sweep"]
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
                           "exp296_channel_sweep.py",
                           "exp297_site_dose_ladders.py",
                           "exp298_combined_site_carrier.py")

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
                               faces=("ctx",), g=1.0, a_base=None,
                               pbar=None, mark_mask=None):
        assert isinstance(faces, tuple) and len(faces) >= 1 \
            and all(f in ("ctx", "gj", "apop") for f in faces) \
            and len(set(faces)) == len(faces), \
            f"the face set {faces!r} is not pre-named"
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
                    "reg_init_ok": reg_init_ok, "faces": list(faces),
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
        # the arm's SITE plan (computed ONLY when the coupling is armed;
        # T and a_base are arm-independent -- the row sets match 1:1
        # across the whole battery)
        cls = None
        J = None
        if g > 0.0:
            assert a_base is not None, "the activation needs the base adjacency"
            cls = classify(target, a_base)["class"]
            if "gj" in faces:
                J = classify(target, a_base)["junction"]
            if "apop" in faces:
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
            # ---- THE FACES' COUPLING (the ONLY deviation from the
            #      landed dormant walk; ZERO at g == 0.0; the coupling
            #      order fixed in the pre-registration: the sigma face
            #      first (the draw's scale), then the blends (the
            #      write's value); at a cell carrying BOTH blend faces
            #      the blend is applied ONCE -- the sites' blend forms
            #      are identical, the overlap recorded not doubled) --
            if g > 0.0:
                hist_i = float(c.phi_history[i])
                cell_armed = False
                if "apop" in faces:
                    assert 0.0 <= g <= 1.0, \
                        "the apop sigma form's domain is g in [0, 1]"
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
                if "ctx" in faces and cls[i] == 0:
                    # exp289's landed form VERBATIM (the self blend at
                    # the canon-boundary cells)
                    blend = True
                if "gj" in faces and bool(J[i]):
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
               "faces": list(faces), "n_arm_writes": int(n_arm_writes),
               "n_sigma_writes": int(n_sigma_writes),
               "n_blend_writes": int(n_blend_writes)}
        return out

    # ---- the state-carrying replica read (exp289's form VERBATIM) -----
    def _scoped_row_read_traced(spec, med, seed, fmax, budget,
                                faces=("ctx",), g=1.0, a_base=None,
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
                                         budget=budget, faces=faces, g=g,
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
    def _decode_arm_row(host, row_key, spec, med, seed, fmax, faces,
                        a_base, pbar, mark_mask, anchor282, anchor287,
                        g=1.0):
        _lock_read(host, row_key, seed)
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET,
                                      faces=faces, g=g, a_base=a_base,
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
            (f"{host} {row_key} s{seed} faces {faces}: the walked "
             "moved with the arm -- the stream face drifted")
        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps == len(trace), \
            f"{host} {row_key} s{seed}: the commit count drifted"
        assert n_commits == int(anchor287["n_commits"]), \
            (f"{host} {row_key} s{seed} faces {faces}: the commit "
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
               "pert": P3, "medium": "base", "faces": list(faces),
               "arm": "|".join(faces), "g": float(g),
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "branch": str(out["branch"]), "rho": float(out["rho"]),
               "walk_steps": steps, "trace_len": len(trace),
               "walk_end_rms": final, "trace_sha256": trace_sha,
               "conv_step": int(conv), "settle_gap_abs": float(settle_gap),
               "n_commits": n_commits, "commit_seq_sha256": commit_sha,
               "src_census": census_src, "cvt_rms": cvt_rms,
               "register": reg, "n_arm_writes": int(out["n_arm_writes"]),
               "n_sigma_writes": int(out["n_sigma_writes"]),
               "n_blend_writes": int(out["n_blend_writes"]),
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

    # ---- the battery pass: the 4 faces batteries (72 rows each =
    #      288 decodes; the hosts ascending, the seeds ascending, the
    #      instances ascending within each arm; the arms in the
    #      pre-named battery order) --------------------------------------
    def _run_faces(with_suite):
        _LOCK_LOG.clear()
        rb = _rebuild()
        suite = _run_test_suite() if with_suite else None
        bases = rb["bases"]
        ai = _arm_inputs(bases)
        rows: list = []
        for faces in FACES_BATTERY:
            for k in hosts:
                ctx = bases[k]
                med = HostWMedium(ctx["A"])
                for s in SEEDS_RUN:
                    for inst in DEEP_INSTANCES:
                        rk = f"r{DEEP_RUNG:g}i{inst}"
                        rec = _decode_arm_row(
                            k, rk, ctx["deep"][inst]["spec"], med, s,
                            ctx["fmax"], faces, ctx["A"], ai["pbar"],
                            ai["marks"][k][str(inst)],
                            rb["r282"][(k, s, rk)],
                            rb["r287"][(k, s, rk)], g=G_PLATEAU)
                        if "gj" in faces:
                            _W, _m, _resid = compensate(
                                ctx["A"], ctx["deep"][inst]["f"],
                                ai["target_part"][k])
                            rec["gj_landed_assert"] = {
                                "n_multipliers": int(np.sum(_m != 1.0)),
                                "conservation_residual": _resid}
                        rows.append(rec)
                hs = [r for r in rows
                      if r["host"] == k and r["faces"] == list(faces)]
                print(f"  [{'|'.join(faces)} {k}] 6 rows | errs "
                      f"{[r['err'] for r in hs]} | armed "
                      f"{hs[0]['n_arm_writes']}/row (sigma "
                      f"{hs[0]['n_sigma_writes']}, blend "
                      f"{hs[0]['n_blend_writes']}) | reg replay "
                      f"{sum(r['register']['replay_ok'] for r in hs)}/6",
                      flush=True)
        assert len(rows) == N_DECODES, \
            f"the battery produced {len(rows)} rows != {N_DECODES}"
        assert len(_LOCK_LOG) == N_DECODES, \
            f"the S* lock count {len(_LOCK_LOG)} != {N_DECODES} reads"
        return {"rows": rows,
                "arm_inputs_digest": _arm_inputs_digest(ai),
                "arm_inputs_record": {
                    "pbar": ai["pbar"], "q10": ai["q10"], "q90": ai["q90"],
                    "pooled_n": ai["pooled_n"],
                    "target_part": ai["target_part"],
                    "bands": ai["bands"]},
                "lock_reads": len(_LOCK_LOG),
                "ro_before": dict(ro_before),
                "port_sha256": port_sha_entry,
                "exp142_sha256": exp142_sha_entry,
                "rebuild_counts": rb["counts"],
                "rebuild_report": rb["rebuild_report"],
                "test_suite": suite,
                "zero_reader_scan": zero_reader_scan}

    _MODE = os.environ.get("EXP298_MODE", "all")
    assert _MODE == "all", \
        f"EXP298_MODE {_MODE!r} is not pre-named (the single-dose " \
        "battery fits one foreground run)"

    def _payload_sha(p):
        return hashlib.sha256(json.dumps(
            p, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the ANCHOR EXTRACT (exp296's deposited single-face rows at
    #      g=1.0) + the CONTROL (exp256's dormant baseline) --------------
    def _exp296_anchor():
        anch = {}
        for arm, faces in zip(ARM_NAMES[:3], FACES_BATTERY[:3]):
            key0 = faces[0]
            arows = [r for r in dep296["rows"]
                     if r["arm"] == key0 and float(r["g"]) == 1.0]
            assert len(arows) == 72, \
                f"exp296's deposited {key0} rows drifted"
            m = {}
            for r in arows:
                k = (r["host"], int(r["seed"]), r["row_key"])
                assert k not in m, f"duplicate exp296 {key0} row {k}"
                m[k] = {"err": float(r["err"]),
                        "trace_sha256": str(r["trace_sha256"])}
            anch[key0] = m
        base_ctrl = {}
        for r in dep256["rows"]:
            if r["arm"] != ARM_SUBST:
                continue
            for i in r["instances"]:
                base_ctrl[(r["host"], int(r["seed"]),
                           i["row_key"])] = float(i["err"])
        assert len(base_ctrl) == 72, "the exp256 control extract drifted"
        return anch, base_ctrl

    # ---- the wall-clock scan (G4) ------------------------------------
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
                bad.extend(_scan_wall_clock_keys(v, f"{prefix}[{i}]"))
        return bad

    # ---- THE ASSEMBLY --------------------------------------------------
    def _assemble(p, run_form):
        assert p["ro_before"] == ro_before, "ro_before drifted"
        assert p["port_sha256"] == _sha(PORT_FILE), \
            "the ported collective.py drifted mid-run"
        assert p["exp142_sha256"] == _sha(EXP142_FILE), \
            "exp142 was modified -- the pre-registered NOT-modified rule"
        rows = p["rows"]
        assert len(rows) == N_DECODES, \
            f"the assembled battery {len(rows)} != {N_DECODES}"
        suite = p["test_suite"]
        assert suite is not None and bool(suite["green"]), \
            "the test suite is not green (G1's discipline face)"
        _a282 = {(r["host"], int(r["seed"]), r["row_key"]): r
                 for r in dep282["rows"]}
        _a287 = {(r["host"], int(r["seed"]), r["row_key"]): r
                 for r in dep287["rows"]}

        # G1: the single-face anchors vs exp296's deposit (bit-exact)
        anch, base_ctrl = _exp296_anchor()
        anchor_tallies = {}
        for faces in FACES_BATTERY[:3]:
            key0 = faces[0]
            arows = [r for r in rows if r["faces"] == list(faces)]
            assert len(arows) == 72, f"the {key0} arm's 72 rows drifted"
            n_e = n_t = 0
            for r in arows:
                k = (r["host"], int(r["seed"]), r["row_key"])
                dep = anch[key0][k]
                ok_e = bool(r["err"] == dep["err"])
                ok_t = bool(r["trace_sha256"] == dep["trace_sha256"])
                assert ok_e, (f"{k} {key0}: the single-face re-run's "
                              f"err {r['err']} drifted from exp296's "
                              f"deposited {dep['err']}")
                assert ok_t, (f"{k} {key0}: the trace sha drifted")
                n_e += int(ok_e)
                n_t += int(ok_t)
            anchor_tallies[key0] = {"n_err_bit_exact": n_e,
                                    "n_trace_sha_ok": n_t}

        # G2: the register + stream faces per arm + the overlap census
        per_arm_g2 = {}
        overlap_census = {}
        for faces in FACES_BATTERY:
            arows = [r for r in rows if r["faces"] == list(faces)]
            assert len(arows) == 72, "the arm's 72 rows drifted"
            reg_ok = sum(1 for r in arows if all(
                r["register"][k] for k in
                ("present_ok", "init_ok", "replay_ok", "complement_ok",
                 "finite_ok")))
            stream_ok = sum(
                1 for r in arows
                if r["walk_steps"] == int(
                    _a282[(r["host"], int(r["seed"]),
                           r["row_key"])]["walk_steps"])
                and r["n_commits"] == int(
                    _a287[(r["host"], int(r["seed"]),
                           r["row_key"])]["n_commits"]))
            const_ok = all(
                len(set(r["n_arm_writes"] for r in arows
                        if r["host"] == h and r["instance"] == i)) == 1
                for h in hosts for i in DEEP_INSTANCES)
            per_arm_g2["|".join(faces)] = {
                "n_register_ok": reg_ok, "n_stream_ok": stream_ok,
                "site_writes_constant_across_seeds": const_ok,
                "sigma_first_row": arows[0]["n_sigma_writes"],
                "blend_first_row": arows[0]["n_blend_writes"],
                "armed_first_row": arows[0]["n_arm_writes"]}
            if len(faces) == 3:
                # the overlap census (pooled over the 72 rows): the
                # cells where the sigma face and the blend face act on
                # the SAME commit
                both = sum(r["n_sigma_writes"] and r["n_blend_writes"]
                           and 1 or 0 for r in arows)
                overlap_census = {
                    "note": ("per-row the sigma and blend write counts; "
                             "the union's per-row armed count <= the "
                             "sum of the singles' (the overlap face)"),
                    "union_sigma_first_row":
                        arows[0]["n_sigma_writes"],
                    "union_blend_first_row":
                        arows[0]["n_blend_writes"],
                    "union_armed_first_row":
                        arows[0]["n_arm_writes"]}
        gj_asserts = [r.get("gj_landed_assert") for r in rows
                      if "gj" in r["faces"]]
        gj_assert_ok = all(a is not None
                           and a["conservation_residual"] < 1e-9
                           for a in gj_asserts)

        # G3: THE ADDITIVITY BRANCH (the pre-named bars)
        deltas = {}
        host_deltas = {}
        for faces in FACES_BATTERY:
            arm_name = ("UNION" if len(faces) == 3
                        else "|".join(faces))
            arows = [r for r in rows if r["faces"] == list(faces)]
            d = {}
            for r in arows:
                k = (r["host"], int(r["seed"]), r["row_key"])
                d[k] = float(r["err"]) - float(base_ctrl[k])
            deltas[arm_name] = d
            hd = {}
            for h in hosts:
                hds = [v for k, v in d.items() if k[0] == h]
                hd[h] = float(np.mean(hds))
            host_deltas[arm_name] = hd
        mean_d = {a: float(np.mean(list(d.values())))
                  for a, d in deltas.items()}
        n_imp = {a: sum(1 for h in hosts if host_deltas[a][h] < 0.0)
                 for a in mean_d}
        singles = {a: v for a, v in mean_d.items() if a != "UNION"}
        assert len(singles) == 3, "the singles drifted"
        best_single = min(singles, key=singles.get)
        d_union = mean_d["UNION"]
        d_best = singles[best_single]
        if d_union <= d_best - ADDITIVITY_BAND:
            branch = "SUPER-ADDITIVE"
        elif abs(d_union - d_best) < ADDITIVITY_BAND:
            branch = "ADDITIVE"
        else:
            branch = "INTERFERING"

        # the audit faces
        worst = {"|".join(f): float(max(
            r["err"] for r in rows if r["faces"] == list(f)))
            for f in FACES_BATTERY}
        h3h5 = {a: {h: host_deltas[a][h] for h in outliers}
                for a in mean_d}
        # the R_max face (exp288's form on the settled per-cell errors)
        rmax_face = {}
        for faces in FACES_BATTERY:
            arows = [r for r in rows if r["faces"] == list(faces)]
            per_host = {}
            for h in hosts:
                hs = [r for r in arows if r["host"] == h]
                NW = int(sum(d["n"] for r in hs for d in r["decomp"]))
                TOT = float(sum(r["sum_sq_e"] for r in hs))
                pool = []
                for cidx in (0, 1, 2):
                    N_c = int(sum(d["n"] for r in hs
                                  for d in r["decomp"]
                                  if d["cls"] == cidx))
                    SS_c = float(sum(d["sum_sq"] for r in hs
                                     for d in r["decomp"]
                                     if d["cls"] == cidx))
                    frac_c = float(SS_c / TOT) if TOT > 0 else 0.0
                    share_c = float(N_c / NW) if NW else 0.0
                    R_c = (float(frac_c / share_c)) if N_c > 0 else None
                    pool.append({"cls": int(cidx), "n": N_c,
                                 "cell_share": share_c,
                                 "frac_of_sq": frac_c, "R": R_c})
                nonempty = [q["R"] for q in pool if q["R"] is not None]
                per_host[h] = float(max(nonempty))
            rmax_face["|".join(faces)] = {
                "per_host_R_max": per_host,
                "n_concentrating_hosts": int(sum(
                    1 for h in hosts if per_host[h] >= 1.50)),
                "bar": 1.50}

        deposit = {
            "exp": "exp298_combined_site_carrier",
            "claim": ("THE COMBINED-SITE CARRIER (batch 52; the exp298 "
                      "pre-registration): the three carrying faces "
                      "composed on ONE walk via the faces parameter -- "
                      "the anchor ladder proves the composition "
                      "bit-exact per single face, the union runs once; "
                      "the additivity branch vs the best single"),
            "method": {
                "battery": ("the shared 72-row deep-row battery at "
                            "g=1.0; 4 arms x 72 = 288 decodes"),
                "faces_order": [list(f) for f in FACES_BATTERY],
                "coupling_order": ("the sigma face first (the draw's "
                                   "scale), then the blends (the "
                                   "write's value); at a cell carrying "
                                   "both blend faces the blend is "
                                   "applied ONCE"),
                "branch_rule": ("SUPER-ADDITIVE iff the union's mean "
                                "paired delta beats the best single's "
                                "by >= 0.05 mV; ADDITIVE iff within "
                                "0.05 mV; INTERFERING iff worse by "
                                ">= 0.05 mV"),
                "controls": ("exp256's dormant baseline per row (the "
                             "honest absolute control, exp297's "
                             "lesson); the anchors = exp296's "
                             "deposited single-face rows"),
                "audit_faces": ("the per-host delta tables, the "
                                "overlap census, the worst-err vs the "
                                "6.0 bar, the H3/H5 deltas, the "
                                "R_max face")},
            "inputs": {n: {"path": f"results/{n}.json",
                           "sha256": ro_before[n]}
                       for n in RO_NAMES + CTRL_NAMES},
            "port": {"file": "cultivation/bioelectric/collective.py",
                     "sha256": port_sha_entry,
                     "zero_reader_scan": zero_reader_scan,
                     "exp142_modified": False,
                     "exp142_sha256": exp142_sha_entry},
            "rebuild_report": p["rebuild_report"],
            "rebuild_counts": p["rebuild_counts"],
            "arm_inputs": p["arm_inputs_record"],
            "test_suite": suite,
            "rows": rows,
            "anchor_tallies": anchor_tallies,
            "per_arm_g2": per_arm_g2,
            "overlap_census": overlap_census,
            "gj_non_history_assert_ok": bool(gj_assert_ok),
            "mean_deltas": mean_d,
            "n_hosts_improved": n_imp,
            "host_deltas": host_deltas,
            "best_single": best_single,
            "branch": branch,
            "branch_discriminant": {
                "d_union": d_union, "d_best_single": d_best,
                "band_mV": ADDITIVITY_BAND},
            "worst_errs": worst,
            "h3h5_deltas": h3h5,
            "rmax_audit": rmax_face,
            "determinism": {
                "form": run_form,
                "discipline": ("one decode per (arm, host, seed, "
                               "instance)"),
                "payload_sha256": _payload_sha(p)},
            "discipline": {}}
        wc = _scan_wall_clock_keys(deposit)
        assert not wc, f"wall-clock fields in the deposit: {wc}"
        deposit["discipline"] = {
            "no_wall_clock_fields": True,
            "deterministic_one_pass_per_arm": True,
            "docstring_header_pinned": True,
            "pinned_to": "the exp298 pre-registration commit",
            "ro_unchanged": True,
            "floor": PROD_FLOOR,
            "reader_pin_disclosed": READER_PIN_FLOOR,
            "run_form": run_form}

        lock_ok = p["lock_reads"] == N_DECODES
        g1_pass = bool(
            all(v["n_err_bit_exact"] == 72 and v["n_trace_sha_ok"] == 72
                for v in anchor_tallies.values())
            and p["rebuild_counts"]["n_sha_ok"] == 12
            and p["rebuild_counts"]["n_288_chain_ok"] == 72
            and lock_ok and bool(suite["green"]))
        g2_pass = bool(
            all(v["n_register_ok"] == 72 and v["n_stream_ok"] == 72
                for v in per_arm_g2.values())
            and all(v["site_writes_constant_across_seeds"]
                    for v in per_arm_g2.values())
            and gj_assert_ok)
        g3_pass = True   # the branch gate records; it does not pass/fail
        g4_pass = bool(deposit["discipline"]["no_wall_clock_fields"]
                       and deposit["discipline"]["ro_unchanged"])
        deposit["gates"] = {
            "G1_the_anchor_ladder": {
                "pass": g1_pass, "anchor_tallies": anchor_tallies,
                "n_lock_reads": p["lock_reads"],
                "n_lock_bar": N_DECODES,
                "test_suite_green": bool(suite["green"])},
            "G2_the_forms": {"pass": g2_pass,
                             "per_arm": per_arm_g2,
                             "gj_assert_ok": bool(gj_assert_ok)},
            "G3_the_additivity_branch": {
                "pass": g3_pass, "branch": branch,
                "mean_deltas": mean_d, "best_single": best_single,
                "d_union": d_union, "d_best_single": d_best,
                "band_mV": ADDITIVITY_BAND,
                "n_hosts_improved": n_imp},
            "G4_discipline": {"pass": g4_pass, "run_form": run_form,
                              "no_wall_clock_fields": True,
                              "ro_unchanged": True,
                              "floor": PROD_FLOOR}}
        n_pass = sum(1 for g in deposit["gates"].values() if g["pass"])
        deposit["verdict"] = (
            f"{n_pass}/4 evaluated gates ({n_pass} PASS / "
            f"{4 - n_pass} REFUTE) | BRANCH: {branch} | the union "
            f"{d_union:+.4f} mV vs the best single ({best_single}) "
            f"{d_best:+.4f} mV")

        print(f"\n=== exp298: THE COMBINED-SITE CARRIER ===")
        print(f"  G1 the anchor ladder: "
              f"{'PASS' if g1_pass else 'FAIL'} (exp296's single-face "
              f"rows reproduced bit-exact: "
              + ", ".join(f"{s} {anchor_tallies[s]['n_err_bit_exact']}"
                          f"/72" for s in anchor_tallies)
              + f"; the S* lock reads {p['lock_reads']}/{N_DECODES}; "
                f"the test suite green: {bool(suite['green'])})")
        print(f"  G2 the forms: {'PASS' if g2_pass else 'FAIL'} "
              f"(the register + stream faces 72/72 per arm; the site "
              f"writes seed-invariant per (host, instance); the gj "
              f"landed assert: {gj_assert_ok})")
        print("  G3 the additivity branch (the mean paired deltas vs "
              "exp256's dormant baseline):")
        for a in mean_d:
            star = " <- the best single" if a == best_single else ""
            uni = " <- THE UNION" if a == "UNION" else ""
            print(f"      {a:12s} {mean_d[a]:+.4f} mV "
                  f"({n_imp[a]}/12 hosts){star}{uni}")
        print(f"      the band {ADDITIVITY_BAND} mV -> BRANCH: "
              f"{branch}")
        print(f"      the H3/H5 deltas: "
              + "; ".join(f"{a} H3 {h3h5[a]['H3']:+.3f} / "
                          f"H5 {h3h5[a]['H5']:+.3f}" for a in mean_d))
        print(f"      the worst-errs vs the 6.0 bar: "
              + "; ".join(f"{a} {worst[a]:.2f}" for a in worst))
        print(f"  G4 discipline: {'PASS' if g4_pass else 'FAIL'} "
              f"(deterministic, form {run_form}; no wall-clock fields; "
              f"16 deposits READ-ONLY byte-unchanged; exp142 + the core "
              f"NOT modified; floor -60.0 at exit)")
        print(f"\n  BRANCH: {branch}")
        print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {4 - n_pass} "
              f"REFUTE)")
        print(f"  deposited {OUT}")
        return deposit

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

    # ---- THE DISPATCH -----------------------------------------------------
    p = _run_faces(with_suite=True)
    deposit = _assemble(p, run_form="in-process all (4 arms x 72 in one "
                                    "process)")

    with open(OUT, "w") as fh:
        json.dump(deposit, fh, indent=1, default=str)

    _exit_checks()
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
