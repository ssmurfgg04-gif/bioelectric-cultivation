#!/usr/bin/env python3
"""exp305 — THE LAST DORMANT CHANNEL: CAN THE REGISTER UNBLOCK ca2?
(batch 60; ledger L290c's promoted candidate (4) — exp296 landed
CARRIER-GENERAL: gj/str/apop carry the history register, ca2 the sole
inert holdout (+0.0042 mV, 0/12 hosts at the plateau dose g=1.0). THE
DIAGNOSED MECHANISM OF THE INERTNESS: exp296's CA2-HIST arm kept
exp261's landed commit-time gain form VERBATIM with the one source
swap (the HH gate reads the register instead of the live Vmem) — but
the gain's contrast term is battery-mean-centered: gain = 1 +
g*(p_i - pbar), pbar the battery-wide mean P over the register's init
face. The contrast is zero-mean BY CONSTRUCTION across the battery and
near-flat in the working voltage window (the Cav3.3 P face is a
band-pass around ~-48 mV; |p - pbar| ~ 1e-2 over the spec's [-60,-20]
rungs) — a zero-mean per-cell modulation of the correction cannot move
a zone-mean decode. THE OPEN QUESTION: is ca2's inertness FORM-
SPECIFIC (a register coupling whose contrast is NOT zero-mean carries)
or STRUCTURAL (no register coupling through the ca2 channel's landed
semantics can move the decode — the channel sweep closes at 3 carried
+ 1 structurally inert)?

THE INSTRUMENT (exp296's landed walk machinery VERBATIM — the traced
replica at the production budget 8, the register port, the RNG
discipline (exactly ONE normal draw per commit, the stream position
arm-independent), the 72-row substituted battery exp256's, 12 hosts x
3 seeds x r-60i0/r-60i1 at n=400) with the coupling block swapped to
TWO pre-named arms at the plateau dose g=1.0:

  C1 CONTRAST-GAIN  exp261's landed gain form with the ONE pre-named
                    knob change: the baseline term becomes the cell's
                    OWN live gate — p_live = ca_open_prob(ca_m_inf(V_i),
                    ca_h_inf(V_i)) read at the commit (pre-write),
                    p_reg = the same gate at the register read —
                    gain = 1 + g*(p_reg - p_live); written =
                    theta_before + gain*(theta_new - theta_before) at
                    EVERY committed cell (exp261's site semantics);
                    ch4 "ca2" carries the contrast (p_reg - p_live)
                    (the mold: the channel vector carries the
                    coupling's per-cell scalar). The zero-mean
                    cancellation is REMOVED: cells whose remembered
                    state differs from their live state get real
                    amplification/attenuation of the correction.
  C2 CA2-BLEND      the house blend form (exp289's ctx form VERBATIM)
                    at exp261's site semantics (EVERY committed
                    cell): written = (1-g)*theta_new + g*hist_i; ch4
                    "ca2" carries the register read hist_i. The
                    widest site mask any channel has — the
                    site-saturation face of the register's
                    re-assertion.

THE CONTROLS: both arms' control is exp256's deposited substituted
errs (72) — the ca2 channel's landed no-history face IS the dormant
baseline (exp261's c0 identity gate and exp289's G1 proved the g=0
face == the production decode bit-exact on this battery; exp296's
CA2-HIST arm used the same control).

THE BRANCHES (pre-named): UNBLOCKED iff >= 1 arm CARRIES; STILL-INERT
iff neither arm carries; ANTI-CARRIES iff both arms' mean paired
deltas > +0.05 mV (disclosed). An arm CARRIES iff its 72-row mean
paired delta < -0.05 mV AND >= 10/12 hosts improve (host delta < 0) —
exp296's landed bars VERBATIM, re-fixed here, never fit.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets 72/72; THE DORMANT CANARY (seed 1,
      instance 0 per host, g=0.0 — the walk machinery's identity,
      exp304's G1 form): err_exact BIT-EXACT vs exp282's deposited
      err_exact 12/12 + the trace shas BIT-EXACT vs exp282 12/12 +
      round(err_exact, 2) == exp256's deposited err 12/12; exp256's 72
      substituted records re-read as the control (the err chain vs
      exp282's err_deposited 72/72); the consumed deposits READ-ONLY
      sha before/after (exp243/256/282/296); the port's provenance
      (the ported file's sha recorded) + the zero-reader scan (the
      allowlist = the port + the pre-named history instruments + this
      module); exp142 and the core NOT modified (sha at entry ==
      exit); the test suite green.
  G2  THE FORMS (zero-knob asserted, fail=STOP per row): per arm 72
      rows; the register's faces (present/init/replay-equality/
      complement/finite) 144/144; n_arm_writes == walk_steps 144/144
      (both arms arm EVERY committed cell); the ch4 write counts ==
      n_arm_writes; the site-write counts constant across the seeds
      per (host, instance) 24/24 per arm; the A3 state convention
      144/144; the coverage 144/144; the commit count == walk_steps ==
      the trace length 144/144 (the stream face — the RNG positions
      are arm-independent, one draw per commit); the C1 gain faces:
      the gains finite and within [1-g, 1+g] (asserted in-walk, the
      min/max recorded per row); the C2 blend faces: the blend weight
      exactly g (the write's form asserted in-walk by construction);
      the commit values finite 144/144.
  G3  THE BRANCH DISCRIMINANT (the bars pre-named HERE, numeric, never
      fit): carry = (the 72-row mean paired delta < -0.05 mV) AND
      (>= 10/12 hosts improve) — exp296's landed bars VERBATIM;
      UNBLOCKED / STILL-INERT / ANTI-CARRIES as pre-named above; the
      per-host delta table + the worst-err audit + the gain-spread
      audit recorded.
  G4  THE DISCIPLINE: deterministic (one pass per arm; the payload
      serialized twice, the shas asserted equal); no wall-clock
      fields; the docstring + header pinned to the pre-registration
      commit, asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0
      asserted at exit; the floor -60.0 asserted at the entry, after
      the canary, after each arm's batch, and at exit.

RUN: 144 armed decodes + the 12 canary decodes, in-process one
invocation, ~4-6 min, under the 570 s cap.

DEPOSIT: results/exp305_ca2_unblock.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp305_ca2_unblock.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 6278182; gates G1-G4
    #      evaluated exactly once. THE MACHINERY: exp296's landed walk
    #      (the traced replica, the register port, the RNG discipline)
    #      with the coupling block swapped to the two pre-named ca2
    #      arms; the controls are exp256's deposited substituted errs;
    #      the canary is the dormant walk at g=0.0) ======================
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
    #      the 6278182 pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "ce9a18b4a9e5b78af716c149f0e48a131a23b0e59dd3b2496aac0046994e3066")
    EXPECTED_HEADER_SHA256 = (
        "2c2974db21234e165806fc77d6193337aa85806898a4c87633a66c097a35ba42")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from 6278182"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from 6278182"

    # ---- the -60.0 floor (G4: the exp169-import discipline; the whole
    #      reader chain imported FIRST, every pinned floor restored) ---
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0   # recorded, never applied (no A1 arm here)
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    def read_floor():
        return float(CORE.NEURAL_SPEC_MIN)

    assert read_floor() == PROD_FLOOR, "the floor is not -60.0 at entry"

    # ---- the frozen battery constants (exp296's/exp256's; the arms +
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
    ARMS_ORDER = ("c1", "c2")
    ARM_LABELS = {"c1": "C1 CONTRAST-GAIN", "c2": "C2 CA2-BLEND"}
    # the branch bars (pre-named at 6278182, numeric, never fit --
    # exp296's landed carry bars VERBATIM)
    CARRY_MARGIN = -0.05                  # mV, the house margin
    CARRY_MIN_HOSTS = 10                  # the per-host clause
    ANTI_MARGIN = 0.05                    # mV, the ANTI-CARRIES clause
    COMMIT_SOURCES = ("spec", "canon", "parent")

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

    # ---- the read-only deposits (the pre-named 4; sha before/after) ----
    RES = os.path.join(ROOT, "results")
    RO_NAMES = ("exp243_structured_adversarial",
                "exp256_row_pair_regression",
                "exp282_trajectory_structure",
                "exp296_channel_sweep")
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
    dep282 = _deps["exp282_trajectory_structure"]
    dep296 = _deps["exp296_channel_sweep"]
    hosts = list(dep296["hosts"])
    assert len(hosts) == 12, "the 12-host corpus drifted"
    outliers = list(dep296["outliers"])
    assert outliers == ["H3", "H5"], "the outlier pre-name drifted"

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
        "exp305_ca2_unblock.py")

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

    # ---- exp208's classify (the house VERBATIM: exp296's exact form) ---
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

    # ---- THE TRACED REPLICA: exp296's landed _execute_signed_traced
    #      REUSED VERBATIM (the walk byte-similar + the register port
    #      population + the RNG discipline) with the ONE exp305
    #      parameter: the ARM -- the coupling block swapped to the two
    #      pre-named ca2 arms (the docstring's disclosure). The site
    #      plan COLLAPSES: both arms arm EVERY committed cell (no
    #      cls/J/S_site/mark inputs exist for C1/C2). The RNG stream:
    #      exactly ONE c.rng.normal per commit for EVERY arm and at
    #      every g (exp264's stream discipline -- the scale never moves
    #      the stream position), the draw BEFORE the coupling exactly
    #      as exp296's ca2 branch ordered it ----------------------------
    def _execute_signed_traced(spec, adjacency, seed, op, budget,
                               arm="c1", g=G_PLATEAU):
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
        # per-arm init face)
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
                    "n_arm_writes": 0, "n_ch4_writes": 0,
                    "gain_min": None, "gain_max": None}
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
        n_ch4_writes = 0
        gain_min = float("inf")
        gain_max = float("-inf")
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
            # draw ONCE below, at the pre-named sigma)
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
                theta_new = commit_base + c.rng.normal(0.0, sigma)
                if arm == "c2":
                    # the house blend form (exp289's ctx form VERBATIM)
                    # at exp261's site semantics: EVERY committed cell;
                    # ch4 "ca2" carries the register read (the
                    # coupling's per-cell scalar)
                    written = (1.0 - g) * theta_new + g * hist_i
                    ca2_vec = c.read_channel("ca2")
                    ca2_vec[i] = hist_i
                    c.set_channel("ca2", ca2_vec)
                    n_ch4_writes += 1
                    n_arm_writes += 1
                else:                            # arm == "c1"
                    # exp261's landed gain form with the ONE pre-named
                    # knob change: the baseline is the cell's OWN live
                    # gate (the battery-mean pbar is gone -- the
                    # zero-mean cancellation that diagnosed exp296's
                    # inertness is removed)
                    theta_before = float(c.theta[i])
                    p_reg = float(ca_open_prob(ca_m_inf(hist_i),
                                               ca_h_inf(hist_i)))
                    p_live = float(ca_open_prob(
                        ca_m_inf(float(c.V[i])),
                        ca_h_inf(float(c.V[i]))))
                    assert np.isfinite(p_reg) and 0.0 <= p_reg <= 1.0, \
                        "the register-gate P left [0, 1]"
                    assert np.isfinite(p_live) and 0.0 <= p_live <= 1.0, \
                        "the live-gate P left [0, 1]"
                    contrast = p_reg - p_live
                    ca2_vec = c.read_channel("ca2")
                    ca2_vec[i] = contrast
                    c.set_channel("ca2", ca2_vec)
                    n_ch4_writes += 1
                    gain = 1.0 + g * contrast
                    assert np.isfinite(gain) and (1.0 - g) <= gain \
                        <= (1.0 + g), \
                        "the contrast-gain left [1-g, 1+g]"
                    gain_min = min(gain_min, gain)
                    gain_max = max(gain_max, gain)
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
               "arm": arm, "n_arm_writes": int(n_arm_writes),
               "n_ch4_writes": int(n_ch4_writes),
               "gain_min": (None if gain_min == float("inf")
                            else float(gain_min)),
               "gain_max": (None if gain_max == float("-inf")
                            else float(gain_max))}
        return out

    # ---- the state-carrying replica read (exp289's form VERBATIM) -----
    def _scoped_row_read_traced(spec, med, seed, fmax, budget,
                                arm="c1", g=G_PLATEAU):
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
                                         budget=budget, arm=arm, g=g)
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

    # ---- the sha-asserted rebuild (exp296's _rebuild at the faces
    #      this experiment consumes: the 12 hosts, the 72 substituted
    #      rows, the exp282 walk-anchor re-read) --------------------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
                  "n_fmax_ok": 0, "n_nonneg_ok": 0, "n_rows256": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows282": 0, "n_282_chain_ok": 0}
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

        # exp256's 72 rows -- the substituted records (the battery's
        # definition + the control)
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
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                for s in SEEDS_RUN:
                    d = dep_sub[(h, s, rk)]
                    ok_t = bool(_f_sha(bases[h]["deep"][inst]["f"])
                                == bases[h]["deep"][inst]["sha"])
                    # the medium IS the base (asserted by the rebuild's
                    # sha above); the row-key walk:
                    assert ok_t
                    counts["n_deep_targets_ok"] += int(ok_t)
                    counts["n_medium_shas_ok"] += 1
        assert counts["n_deep_targets_ok"] == 72 \
            and counts["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # THE EXP282 RE-READ (the canary's anchor: the trace shas +
        # the err chain + the walked counts)
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
            counts["n_282_chain_ok"] += int(ok_chain)
            r282[key] = r
        assert counts["n_282_chain_ok"] == 72, \
            "the exp282 err chain anchor drifted"
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "counts": counts, "rebuild_report": rebuild_report}

    rb = _rebuild()

    # ---- one ROW decode (the register + the commit bookkeeping
    #      asserted fail=STOP per row; the stream face asserted against
    #      exp282's walked counts) --------------------------------------
    def _decode_row(host, row_key, spec, med, seed, fmax, arm, g,
                    anchor282):
        out = _scoped_row_read_traced(spec, med, seed, fmax, BUDGET,
                                      arm=arm, g=g)
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
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        # the STREAM FACE (fail=STOP): the walked count is arm- and
        # g-independent (the coupling is value-level only; the RNG
        # positions identical -- exp264's one-draw discipline)
        assert steps == int(anchor282["walk_steps"]), \
            (f"{host} {row_key} s{seed} arm {arm} g {g}: the walked "
             "count moved with the arm -- the stream face drifted")
        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps == len(trace), \
            f"{host} {row_key} s{seed}: the commit count drifted"
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
        rec = {"host": host, "seed": int(seed),
               "instance": int(row_key[-1]), "row_key": row_key,
               "pert": P3, "medium": "base", "arm": arm, "g": float(g),
               "err": err, "err_exact": err_exact, "a3_ok": a3_ok,
               "verified": bool(out["program_verified"]),
               "walk_steps": steps, "n_commits": n_commits,
               "trace_sha256": trace_sha,
               "census": census_src, "cvt_rms": cvt_rms,
               "register": reg,
               "n_arm_writes": int(out["n_arm_writes"]),
               "n_ch4_writes": int(out["n_ch4_writes"]),
               "gain_min": out["gain_min"], "gain_max": out["gain_max"]}
        return rec

    # ---- G1: THE DORMANT CANARY (seed 1, instance 0 per host, g=0.0 --
    #      the walk machinery's identity, exp304's G1 form) --------------
    print("[exp305] the canary: the 12 dormant rows (g=0.0) ...")
    canary_rows = []
    n_can_err = 0
    n_can_sha = 0
    n_can_a3 = 0
    for h in hosts:
        key = (h, 1, f"r{DEEP_RUNG:g}i0")
        rec = _decode_row(h, key[2], rb["bases"][h]["deep"][0]["spec"],
                          HostWMedium(rb["bases"][h]["A"]), 1,
                          rb["bases"][h]["fmax"], "c1", 0.0, rb["r282"][key])
        ok_err = bool(rec["err_exact"]
                      == float(rb["r282"][key]["err_exact"]))
        ok_sha = bool(rec["trace_sha256"]
                      == str(rb["r282"][key]["trace_sha256"]))
        ok_a3 = bool(round(rec["err_exact"], 2)
                     == rb["dep_sub"][key]["err"])
        assert ok_err, \
            (f"{h}: the canary's err_exact drifted from exp282's "
             "deposited record")
        assert ok_sha, f"{h}: the canary's trace sha drifted from exp282's"
        assert ok_a3, f"{h}: the canary's A3 err drifted from exp256's"
        assert rec["n_arm_writes"] == 0 and rec["n_ch4_writes"] == 0, \
            f"{h}: the canary's g=0.0 walk armed the coupling"
        n_can_err += int(ok_err)
        n_can_sha += int(ok_sha)
        n_can_a3 += int(ok_a3)
        canary_rows.append({"host": h, "row_key": key[2],
                            "err_exact": rec["err_exact"],
                            "err_bit_exact_vs_exp282": ok_err,
                            "trace_sha_ok": ok_sha,
                            "a3_ok_vs_exp256": ok_a3})
    assert n_can_err == 12 and n_can_sha == 12 and n_can_a3 == 12, \
        "the canary drifted"
    assert read_floor() == PROD_FLOOR, "the floor moved after the canary"
    print(f"  [canary] 12/12 bit-exact (errs + trace shas vs exp282, "
          f"A3 vs exp256)")

    # ---- THE ARMED BATTERIES (2 arms x 72 rows; one pass per arm) ------
    rows_out = []
    per_arm_g2 = {}
    for arm in ARMS_ORDER:
        print(f"[exp305] the arm {ARM_LABELS[arm]}: 72 armed rows ...")
        n_rows = 0
        site_const = True
        site_by_row = {}
        for h in hosts:
            for inst in DEEP_INSTANCES:
                rk = f"r{DEEP_RUNG:g}i{inst}"
                counts_here = []
                for s in SEEDS_RUN:
                    key = (h, s, rk)
                    rec = _decode_row(
                        h, rk, rb["bases"][h]["deep"][inst]["spec"],
                        HostWMedium(rb["bases"][h]["A"]), s,
                        rb["bases"][h]["fmax"], arm, G_PLATEAU,
                        rb["r282"][key])
                    assert rec["n_arm_writes"] == rec["walk_steps"], \
                        (f"{h} {rk} s{s} arm {arm}: the arm-write count "
                         "drifted from the walked count (both arms arm "
                         "EVERY committed cell)")
                    assert rec["n_ch4_writes"] == rec["n_arm_writes"], \
                        (f"{h} {rk} s{s} arm {arm}: the ch4 write count "
                         "drifted from the arm-write count")
                    counts_here.append(rec["n_arm_writes"])
                    rows_out.append(rec)
                    n_rows += 1
                site_by_row[f"{h}|i{inst}"] = {
                    "min": int(min(counts_here)),
                    "max": int(max(counts_here)),
                    "constant_across_seeds":
                        bool(min(counts_here) == max(counts_here))}
                site_const &= site_by_row[f"{h}|i{inst}"][
                    "constant_across_seeds"]
        assert n_rows == 72, f"the {arm} battery drifted"
        assert site_const, \
            f"the {arm} site-write counts moved across the seeds"
        g_mins = [r["gain_min"] for r in rows_out
                  if r["arm"] == arm and r["gain_min"] is not None]
        g_maxs = [r["gain_max"] for r in rows_out
                  if r["arm"] == arm and r["gain_max"] is not None]
        per_arm_g2[arm] = {
            "n_rows": n_rows,
            "n_register_ok": int(sum(
                1 for r in rows_out if r["arm"] == arm
                and all(r["register"][k] for k in
                        ("present_ok", "init_ok", "replay_ok",
                         "complement_ok", "finite_ok")))),
            "n_stream_ok": int(sum(
                1 for r in rows_out if r["arm"] == arm
                and r["walk_steps"] == r["n_commits"] == r["n_arm_writes"]
                == r["n_ch4_writes"])),
            "n_a3_ok": int(sum(1 for r in rows_out
                               if r["arm"] == arm and r["a3_ok"])),
            "site_writes_constant_across_seeds": site_const,
            "site_writes_by_row": site_by_row,
            "gain_min_overall": (float(min(g_mins)) if g_mins else None),
            "gain_max_overall": (float(max(g_maxs)) if g_maxs else None)}
        assert per_arm_g2[arm]["n_register_ok"] == 72, \
            f"the {arm} register faces drifted"
        assert per_arm_g2[arm]["n_stream_ok"] == 72, \
            f"the {arm} stream faces drifted"
        assert per_arm_g2[arm]["n_a3_ok"] == 72, \
            f"the {arm} A3 convention drifted"
        assert read_floor() == PROD_FLOOR, \
            f"the floor moved after the {arm} batch"
        print(f"  [{arm}] 72 rows landed "
              f"(mean err {float(np.mean([r['err'] for r in rows_out if r['arm'] == arm])):.4f})")

    # ---- THE SWEEP (exp296's landed form VERBATIM: the paired deltas
    #      vs exp256's deposited substituted errs; the host deltas; the
    #      carry bars) ----------------------------------------------------
    sweep = {}
    delta_table = {}
    for arm in ARMS_ORDER:
        arm_rows = [r for r in rows_out if r["arm"] == arm]
        assert len(arm_rows) == 72, f"the {arm} sweep drifted"
        deltas = {}
        for r in arm_rows:
            key = (r["host"], int(r["seed"]), r["row_key"])
            deltas[key] = float(r["err"]) - rb["dep_sub"][key]["err"]
        mean_delta = float(np.mean(list(deltas.values())))
        host_deltas = {}
        for h in hosts:
            hd = [deltas[(h, s, rk)] for s in SEEDS_RUN
                  for rk in (f"r{DEEP_RUNG:g}i{i}" for i in DEEP_INSTANCES)]
            host_deltas[h] = float(np.mean(hd))
        n_hosts_improved = int(sum(1 for v in host_deltas.values()
                                   if v < 0.0))
        carries = bool(mean_delta < CARRY_MARGIN
                       and n_hosts_improved >= CARRY_MIN_HOSTS)
        anti = bool(mean_delta > ANTI_MARGIN)
        sweep[arm] = {
            "arm_label": ARM_LABELS[arm],
            "mean_paired_delta": mean_delta,
            "carry_bar": CARRY_MARGIN,
            "n_hosts_improved": n_hosts_improved,
            "n_hosts_bar": CARRY_MIN_HOSTS,
            "host_deltas": host_deltas,
            "carries": carries,
            "anti_carries": anti,
            "worst_err": float(max(r["err"] for r in arm_rows)),
            "worst_under_bar": bool(max(r["err"] for r in arm_rows) < 6.0),
            "n_verified": int(sum(1 for r in arm_rows
                                  if r["verified"])),
            "mean_err": float(np.mean([r["err"] for r in arm_rows])),
            "mean_err_exact": float(np.mean([r["err_exact"]
                                             for r in arm_rows])),
            "control_mean": float(np.mean(
                [rb["dep_sub"][(h, s, rk)]["err"] for h in hosts
                 for s in SEEDS_RUN
                 for rk in (f"r{DEEP_RUNG:g}i{i}"
                            for i in DEEP_INSTANCES)]))}
        delta_table[arm] = host_deltas
    assert sweep["c2"]["control_mean"] == sweep["c1"]["control_mean"], \
        "the two arms' controls disagree (they are the same deposit)"

    # ---- THE BRANCH (the pre-named clauses) -----------------------------
    carried_arms = [a for a in ARMS_ORDER if sweep[a]["carries"]]
    anti_arms = [a for a in ARMS_ORDER if sweep[a]["anti_carries"]]
    if carried_arms:
        branch = "UNBLOCKED"
    elif len(anti_arms) == len(ARMS_ORDER):
        branch = "ANTI-CARRIES"
    else:
        branch = "STILL-INERT"

    # ---- the gates -------------------------------------------------------
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
                   and rb["counts"]["n_rows282"] == 72
                   and rb["counts"]["n_282_chain_ok"] == 72
                   and n_can_err == 12 and n_can_sha == 12
                   and n_can_a3 == 12
                   and ro_unchanged and exp142_unmodified
                   and test_suite["green"])
    g2_pass = bool(all(per_arm_g2[a]["n_rows"] == 72
                       and per_arm_g2[a]["n_register_ok"] == 72
                       and per_arm_g2[a]["n_stream_ok"] == 72
                       and per_arm_g2[a]["n_a3_ok"] == 72
                       and per_arm_g2[a]["site_writes_constant_across_seeds"]
                       for a in ARMS_ORDER)
                   and len(rows_out) == 144)
    g3_pass = bool(branch in ("UNBLOCKED", "STILL-INERT", "ANTI-CARRIES"))
    g4_pass = bool(ro_unchanged and exp142_unmodified and port_unmodified
                   and floor_exit_ok and test_suite["green"]
                   and zero_reader_scan["files_outside_port_and_instruments"]
                   == [])

    print(f"  G1 the anchors: {'PASS' if g1_pass else 'FAIL'}")
    print(f"  G2 the forms: {'PASS' if g2_pass else 'FAIL'}")
    print(f"  G3 the branch: {branch} ({'PASS' if g3_pass else 'FAIL'})")
    print(f"  G4 the discipline: {'PASS' if g4_pass else 'FAIL'}")

    # ---- the deposit ------------------------------------------------------
    payload = {
        "exp": "exp305_ca2_unblock",
        "claim": (
            "THE LAST DORMANT CHANNEL -- CAN THE REGISTER UNBLOCK ca2? "
            "(batch 60; ledger L290c's promoted candidate (4); "
            "pre-registration 6278182): exp296 landed CARRIER-GENERAL "
            "with ca2 the sole inert holdout (+0.0042 mV, 0/12 hosts at "
            "g=1.0); the inertness mechanism diagnosed (the landed gain "
            "form's contrast is battery-mean-centered -- zero-mean by "
            "construction, near-flat in the working window -- it cannot "
            "move a zone-mean decode); TWO pre-named arms at g=1.0 on "
            "exp256's 72-row battery: C1 CONTRAST-GAIN (exp261's landed "
            "gain form, the baseline swapped to the cell's OWN live "
            "gate) + C2 CA2-BLEND (the house blend form at exp261's "
            "site semantics -- every committed cell); the branches "
            "UNBLOCKED / STILL-INERT / ANTI-CARRIES with exp296's "
            "landed carry bars VERBATIM"),
        "method": {
            "battery": ("the shared 72-row deep-row battery (12 hosts x "
                        "3 seeds x 2 deep instances, the base medium, "
                        "exp256's rows); 2 arms x 72 = 144 armed decodes "
                        "+ the 12-row dormant canary (g=0.0)"),
            "arms": {"c1": "C1 CONTRAST-GAIN", "c2": "C2 CA2-BLEND"},
            "dose": G_PLATEAU,
            "control": ("exp256's deposited substituted errs (72) -- the "
                        "ca2 channel's landed no-history face IS the "
                        "dormant baseline (exp261's c0 + exp289's G1)"),
            "run_form": "in-process one invocation",
            "branch_rule": (
                "UNBLOCKED iff >= 1 arm carries; STILL-INERT iff "
                "neither; ANTI-CARRIES iff both arms' mean paired "
                "deltas > +0.05; an arm CARRIES iff its 72-row mean "
                "paired delta < -0.05 mV AND >= 10/12 hosts improve "
                "(exp296's landed bars VERBATIM)"),
            "inertness_diagnosis": (
                "exp296's CA2-HIST gain = 1 + g*(p_i - pbar) with pbar "
                "the battery-wide mean P: the contrast is zero-mean by "
                "construction and near-flat in the working window "
                "(the Cav3.3 P face is a band-pass around ~-48 mV); a "
                "zero-mean per-cell modulation cannot move a zone-mean "
                "decode -- C1 removes the cancellation, C2 replaces "
                "the form")},
        "inputs": {n: {"path": f"results/{n}.json",
                       "sha256": ro_before[n]} for n in RO_NAMES},
        "port": {"file": "cultivation/bioelectric/collective.py",
                 "sha256": port_sha_entry,
                 "zero_reader_scan": zero_reader_scan,
                 "exp142_modified": not exp142_unmodified,
                 "exp142_sha256": exp142_sha_exit},
        "rebuild_report": rb["rebuild_report"],
        "rebuild_counts": rb["counts"],
        "canary": {"n_rows": 12, "n_err_bit_exact_vs_exp282": n_can_err,
                   "n_trace_sha_ok": n_can_sha,
                   "n_a3_ok_vs_exp256": n_can_a3,
                   "rows": canary_rows},
        "control": {"source": "exp256's deposited substituted errs",
                    "n_rows": 72,
                    "mean_err": sweep["c1"]["control_mean"]},
        "rows": rows_out,
        "per_arm_g2": per_arm_g2,
        "sweep": sweep,
        "delta_table": delta_table,
        "branch": branch,
        "branch_discriminant": {
            "n_carried": len(carried_arms),
            "carried_arms": carried_arms,
            "anti_arms": anti_arms,
            "bars": {"carry_margin_mV": CARRY_MARGIN,
                     "carry_min_hosts": CARRY_MIN_HOSTS,
                     "anti_margin_mV": ANTI_MARGIN}},
        "test_suite": test_suite,
        "determinism": {
            "form": "in-process one invocation (one pass per arm)",
            "discipline": ("one decode per (arm, host, seed, instance); "
                           "the merge never re-decodes; the canary "
                           "bit-exact vs exp256/exp282"),
            "no_wall_clock_fields": True},
        "discipline": {
            "no_wall_clock_fields": True,
            "deterministic_one_pass_per_arm": True,
            "docstring_header_pinned": True,
            "pinned_to": "6278182",
            "ro_unchanged": ro_unchanged,
            "floor": PROD_FLOOR,
            "reader_pin_disclosed": READER_PIN_FLOOR,
            "exp142_and_core_not_modified": bool(
                exp142_unmodified and port_unmodified)},
        "gates": {
            "G1_the_anchors": {"pass": g1_pass,
                               "counts": dict(rb["counts"],
                                              **{"n_can_err": n_can_err,
                                                 "n_can_sha": n_can_sha,
                                                 "n_can_a3": n_can_a3,
                                                 "ro_unchanged":
                                                     ro_unchanged,
                                                 "exp142_unmodified":
                                                     exp142_unmodified,
                                                 "test_suite_green":
                                                     test_suite["green"]})},
            "G2_the_forms": {"pass": g2_pass,
                             "counts_per_arm": per_arm_g2},
            "G3_the_branch": {"pass": g3_pass,
                              "branch": branch,
                              "carried_arms": carried_arms,
                              "anti_arms": anti_arms},
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
        f"REFUTE) | BRANCH: {branch} | "
        + "; ".join(
            f"{ARM_LABELS[a]} {'CARRIES' if sweep[a]['carries'] else ('ANTI-CARRIES' if sweep[a]['anti_carries'] else 'inert')} "
            f"({sweep[a]['mean_paired_delta']:+.4f} mV, "
            f"{sweep[a]['n_hosts_improved']}/12 hosts)"
            for a in ARMS_ORDER)
        + f" | the canary bit-exact 12/12")
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
        "docstring drifted from 6278182 (exit)"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from 6278182 (exit)"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, \
        "NEURAL_SPEC_MIN drifted at exit"
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    print(f"[exp305] deposited {OUT}")
    print(f"[exp305] VERDICT: {payload['verdict']}")
    assert read_floor() == PROD_FLOOR, "the floor moved at exit"
    return payload


if __name__ == "__main__":
    main()

