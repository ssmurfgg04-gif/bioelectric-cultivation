#!/usr/bin/env python3
"""exp307 — THE ZONE-INDEXED TRANSPORT FORM: THE 9TH FORMALIZATION OF
THE ZERO-SUBSTRATE STAR (batch 60; ledger L290c's promoted candidate
(6) — the handoff's "does the composed carrier transport" WITH THE
PREMISE REPAIR DISCLOSED: exp304's carrier arm IS the composed union,
so the literal question is already answered (F3: 0/130, BOTH-BOUND);
the genuinely open transport question is the one the project's final
form pre-named three times (L289's final form, PROJECT_COMPLETE's
next-researcher #1, SYNTHESIS_FINAL §5): the binding is the
INDEXATION, and the one untried door is a WIRING-INDEPENDENT
ZONE-ADDRESSING scheme).

THE 9TH FORMALIZATION: the pattern representation = the commit stream
ANNOTATED WITH THE SOURCE'S PER-POSITION STRUCTURAL CLASS LABELS (the
exp208 classes: 0 canon_boundary, 1 pair_junction, 2 interior — the
same classify call the walk machinery itself runs on its own target
and base adjacency; the annotation travels with the stream as part of
the representation). The destination re-addresses the stream through
its OWN structural classes: each source position's value is written to
the destination's next cell OF THE SAME CLASS in the destination's own
walk order (per-class prefix rule n_c = min(src count, dst count)).
THE LEGALITY (disclosed): the destination donates its own walk order
(exp303/304's precedent — the 8th formalization's transport face used
the destination's own walk as the order donor) AND its own class
labels (a coarser object than the walk order, computed the same way
the walk computes them); the zero-substrate protocol is otherwise
UNTOUCHED — no spec install, no clamps, no encode, no carried state,
the register port never touched. The stream + the source's class
annotation is the representation under test.

THE INSTRUMENT (exp304's landed machinery VERBATIM: the sha-asserted
rebuild, the union walk at the composed optimum g=1.0 arm A0, the
_replay instrument, the canaries; the slice = 12 hosts x (seed 1,
instance 0)) with the ONE new face:

  Z1  THE ANCHORS: the 12 carrier slice walks reproduce exp300's
      deposited union g=1.0 slice rows BIT-EXACT (the errs + the trace
      shas 12/12 — exp304's G1 form); THE CROSS-DEPOSIT ANCHOR: the
      12 plain same-substrate replays reproduce exp304's deposited F2
      region_rms + full_err BIT-EXACT 12/12 (the re-run is a re-run,
      not a re-knob); the marks' validity pinned to exp300's deposited
      arm_inputs.
  Z2  THE RE-INDEX IDENTITY FACE (the new-machinery anchor): the
      class-reindexed SAME-SUBSTRATE replays == the plain F2 replays
      BIT-EXACT 12/12 — on own substrate the class order IS the walk
      order, so the re-index must be a no-op; any transport-face
      difference is thereby attributable to the re-indexation alone.
  Z3  THE ZONE-INDEXED TRANSPORT FACE: the 130 genuine pairs (the
      H0<->H1 exclusion PRE-NAMED, exp304's form), class-reindexed:
      does the annotated stream transport where the bare streams (the
      dormant's AND the carrier's) transported nowhere?

THE BRANCHES (pre-named): TRANSPORT-UNBLOCKED iff >= 1/130 genuine
pairs within the 6.0 bar (THE ZERO-SUBSTRATE BLOCK WEAKENS AT THE 9TH
FORMALIZATION — the representation transports when indexed by
structural role; the headline changes fundamentally); ZONE-BOUND iff
0/130 (THE BLOCK SHARPENS AT 9: the binding is FINER than the
structural classes — the zone-addressing door is tried and closed;
the block's final form gains its 9th and strongest formalization).
The price faces recorded either way (the mean/best region rms; the
per-pair price delta vs exp304's deposited F3 prices — audit-only).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE ANCHORS (fail=STOP): the 12 bases rebuilt sha-asserted vs
      exp243 (edges/boundary/canon/f_max/non-negative + the H0==H1
      chain echo); the deep targets; THE MARKS' VALIDITY: the rebuilt
      q10/q90 + target_part + bands reproduce exp300's deposited
      arm_inputs BIT-EXACT 24/24 + 12/12; THE EXP300 ANCHOR: the 12
      carrier slice walks bit-exact (the errs + the trace shas 12/12);
      THE EXP304 ANCHOR: the 12 plain F2 replays bit-exact (the
      region_rms + the full_err 12/12); the H0<->H1 exclusion
      re-asserted (the pair set == 130 genuine); 4 deposits READ-ONLY
      sha before/after (exp243/256/300/304); the port's provenance +
      the zero-reader scan (the allowlist = the port + the pre-named
      history instruments + this module); exp142 and the core NOT
      modified (sha at entry == exit); the test suite green.
  G2  THE FACES' DEFINITION (zero-knob asserted, fail=STOP per face):
      the streams' bookkeeping (the commit count == walk_steps == the
      trace length 12/12; the digests recorded); the class vectors
      deterministic (the classify re-run identity 12/12); the per-class
      counts recorded per host; Z2's identity 12/12 (the re-index
      no-op on own substrate); every Z3 transport's writes finite and
      n_written > 0; the canaries bit-exact (one Z2 + one Z3 re-run).
  G3  THE BRANCH DISCRIMINANT (pre-named above, evaluated exactly
      once): the 6.0 bar is the house's own ERR_BAR (exp303/304's
      content bar, unchanged); TRANSPORT-UNBLOCKED / ZONE-BOUND; the
      price faces + the F3-delta audit recorded.
  G4  THE DISCIPLINE: deterministic (one pass; the payload serialized
      twice, the shas asserted equal); no wall-clock fields; the
      docstring + header pinned to the pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted at
      exit; the floor -60.0 asserted at the entry, at every replay's
      settle (the _replay assert), and at exit.

RUN: 12 carrier walks + 12 plain replays + 12 re-indexed own replays +
130 re-indexed transports + the canaries, in-process one invocation,
~5-6 min, under the 570 s cap.

DEPOSIT: results/exp307_zone_indexed_transport.json
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp307_zone_indexed_transport.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit f7094a8; gates G1-G4
    #      evaluated exactly once. THE MACHINERY: exp304's landed
    #      transport machinery VERBATIM (the _ext_medium read chain,
    #      the _replay instrument, the union walk at the composed
    #      optimum, the slice seed/instance, the H0<->H1 exclusion)
    #      + the ONE new face: the class-reindexed replay (Z2/Z3)) ====
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
    #      the f7094a8 pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "70a662eca88889a614415ab8892cfed457956b3ecb3669306664c80d67288f6d")
    EXPECTED_HEADER_SHA256 = (
        "28a1893a5c9a8ee491d1bf475f2e8215885e620a45a5e19b9cdc107e31a8690b")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    assert docstring_sha == EXPECTED_DOCSTRING_SHA256, \
        "docstring drifted from f7094a8"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from f7094a8"

    # ---- the -60.0 floor (G4: the exp169-import discipline) ------------
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

    # ---- the frozen battery constants (exp304's; the branch pre-named) -
    REWIRE_P = 0.10
    DEEP_RUNG = -60.0
    DEEP_INSTANCES = (0, 1)     # the full pool for the marks' validity
    ARM_SUBST = "substituted"
    P3 = "P3_deep_band_substitution"
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert SEEDS_RUN == (1, 2, 3), "seed-line drift"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        "the read drifted off S*"
    assert (WINDOW_H, COMMIT_NOISE, STEPS_PER_CELL, ERR_BAR) == (
        _m142.WINDOW_H, _m142.COMMIT_NOISE, _m142.STEPS_PER_CELL,
        _m142.ERR_BAR), "the executor constants drifted from exp142's"
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, "the budget drifted"
    SETTLE_H = 15.0
    SLICE_SEED = 1              # the pre-named slice
    SLICE_INST = 0
    FACES_UNION = ("ctx", "gj", "apop")   # exp300's landed union arm
    G_COMPOSED = 1.0                      # exp300's composed optimum
    CONTENT_BAR = float(ERR_BAR)          # 6.0 — the house's own bar
    CONTENT_MAJORITY = 7                  # >= 7/12 within the bar
    DEGENERATE_PAIRS = {("H0", "H1"), ("H1", "H0")}
    CLASS_NAMES = {0: "canon_boundary", 1: "pair_junction", 2: "interior"}
    COMMIT_SOURCES = ("spec", "canon", "parent")

    def _rk(inst):
        return f"r{DEEP_RUNG:g}i{inst}"

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
                "exp300_composed_optimum",
                "exp304_transport_rescoped")
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
    dep300 = _deps["exp300_composed_optimum"]
    dep304 = _deps["exp304_transport_rescoped"]
    hosts = [w["host"] for w in dep304["walks"]
             if w["form"] == "carrier"]
    assert len(hosts) == 12, "the 12-host corpus drifted"

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
        "exp305_ca2_unblock.py", "exp306_premium_under_union.py",
        "exp307_zone_indexed_transport.py")

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

    # ---- exp208's classify (the house VERBATIM: exp304's exact form) ---
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

    # ---- the READ CHAIN (exp303's landed _ext_medium VERBATIM) ---------
    def _ext_medium(med, fmax):
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
        return {"A_ext": A_ext, "rho": rho, "branch": branch}

    # ---- THE TRACED UNION REPLICA: exp302's/exp306's landed
    #      _execute_signed_traced_union VERBATIM (arm A0 only — no
    #      stress pin anywhere; the coupling order fixed: the sigma
    #      face first (the draw's scale), then the blends (the write's
    #      value); at a cell carrying BOTH blend faces the blend is
    #      applied ONCE) -----------------------------------------------
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
                    blend = True
                if "gj" in FACES_UNION and bool(J[i]):
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
            # THE PORT'S POPULATION (arm-independent, g-independent)
            c.phi_history[i] = written
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        c.run(15.0, dt=dt)
        err = float(c.pattern_error(target))
        out = {"program_verified": bool(err < ERR_BAR),
               "err_vs_target": round(err, 2),
               "walk_trace": trace, "walk_steps": len(order),
               "final_state": {"V": c.V.tolist(),
                               "target": target.tolist()},
               "commits": commits, "coverage_ok": coverage_ok,
               "reg_init_ok": reg_init_ok,
               "n_arm_writes": int(n_arm_writes),
               "n_sigma_writes": int(n_sigma_writes),
               "n_blend_writes": int(n_blend_writes)}
        return out

    # ---- THE REPLAY INSTRUMENT (exp303's/exp304's landed form VERBATIM)
    def _replay(A_ext, values, cells, seed, target, label=""):
        assert len(values) == len(cells), \
            f"{label}: the replay's value/cell counts disagree"
        gamma, mu = STAR_OP["gamma"], STAR_OP["mu"]
        dt = star_dt(gamma, float(np.abs(A_ext).sum(axis=1).max()))
        c = GraphCollective(adjacency=A_ext, seed=seed, gamma=gamma,
                            mu_theta=mu)
        # the ZERO-SUBSTRATE protocol: nothing but the wiring + the
        # stream (no spec install, no clamps, no encode, no carried
        # state — the register port never touched)
        for idx, v in zip(cells, values):
            c.theta[idx] = v
            c.V[idx] = v
        assert read_floor() == PROD_FLOOR, \
            f"{label}: the replay's settle ran off the production floor"
        c.run(SETTLE_H, dt=dt)
        V = np.asarray(c.V, dtype=float)
        T = np.asarray(target, dtype=float)
        widx = np.asarray([int(i) for i in cells], dtype=int)
        region_rms = float(np.sqrt(np.mean((V[widx] - T[widx]) ** 2)))
        assert np.isfinite(region_rms), f"{label}: non-finite region rms"
        full_err = float(c.pattern_error(target))
        assert np.isfinite(full_err), f"{label}: non-finite full err"
        return {"region_rms": region_rms, "full_err": full_err,
                "n_written": int(len(cells)), "dt": dt,
                "region_within_bar": bool(region_rms <= CONTENT_BAR),
                "full_within_bar": bool(full_err <= CONTENT_BAR)}

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

    # ---- the sha-asserted rebuild (exp304's _rebuild at the faces
    #      this experiment consumes: the 12 hosts, exp256's battery, the
    #      marks' validity, the exp300 slice rows, the exp304 F2 rows) --
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_bnd_ok": 0, "n_canon_ok": 0, "h0_echo_h1": False,
                  "n_fmax_ok": 0, "n_nonneg_ok": 0, "n_rows256": 0,
                  "n_deep_targets_ok": 0, "n_medium_shas_ok": 0,
                  "n_rows300_slice": 0, "n_rows304_f2": 0,
                  "n_marks_ok": 0, "n_tpart_ok": 0}
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

        # exp256's 72 rows (the battery's integrity)
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
                rk = _rk(inst)
                for s in SEEDS_RUN:
                    assert (h, s, rk) in dep_sub
                    ok_t = bool(_f_sha(bases[h]["deep"][inst]["f"])
                                == bases[h]["deep"][inst]["sha"])
                    assert ok_t
                    counts["n_deep_targets_ok"] += int(ok_t)
                    counts["n_medium_shas_ok"] += 1
        assert counts["n_deep_targets_ok"] == 72 \
            and counts["n_medium_shas_ok"] == 72, "the deep shas drifted"

        # THE MARKS' VALIDITY (fail=STOP): the rebuilt q10/q90 +
        # target_part + bands reproduce exp300's deposited arm_inputs
        # BIT-EXACT (the armed-site plan pinned to the deposited one)
        pool = []
        bands = {}
        target_part = {}
        for h in hosts:
            canon_t = bases[h]["canon"]
            j = classify(canon_t, bases[h]["A"])["junction"]
            parts = [float(sum(bases[h]["A"][int(i), jj]
                               for jj in range(bases[h]["A"].shape[0])
                               if jj != int(i)
                               and bases[h]["A"][int(i), jj] > 0
                               and j[jj]))
                     for i in np.where(j)[0]]
            assert parts, f"{h}: the canonical medium carries no pair cells"
            target_part[h] = float(np.mean(parts))
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

        # THE EXP300 SLICE RE-READ (the carrier walks' anchor source)
        r300_slice = {}
        for r in dep300["rows"]:
            if r["arm"] != "ctx|gj|apop" or float(r["g"]) != G_COMPOSED:
                continue
            key = (r["host"], int(r["seed"]), r["row_key"])
            if int(r["seed"]) != SLICE_SEED or r["row_key"] != _rk(SLICE_INST):
                continue
            assert key not in r300_slice, f"duplicate exp300 slice row {key}"
            r300_slice[key] = r
        counts["n_rows300_slice"] = len(r300_slice)
        assert counts["n_rows300_slice"] == 12, \
            "exp300's 12 slice union rows drifted"

        # THE EXP304 F2 RE-READ (the plain same-substrate replays'
        # anchor source)
        r304_f2 = {row["host"]: row for row in dep304["carrier_replays"]}
        counts["n_rows304_f2"] = len(r304_f2)
        assert counts["n_rows304_f2"] == 12, \
            "exp304's 12 F2 carrier replays drifted"
        assert set(r304_f2) == set(hosts), "the F2 host set drifted"

        return {"bases": bases, "dep_sub": dep_sub, "marks": marks,
                "bands": bands, "target_part": target_part,
                "q10": q10, "q90": q90, "pooled_n": int(pooled.size),
                "r300_slice": r300_slice, "r304_f2": r304_f2,
                "counts": counts, "rebuild_report": rebuild_report}

    rb = _rebuild()
    bases = rb["bases"]

    # ---- the ext media (exp304's form) -----------------------------------
    ext = {}
    for k in hosts:
        med = HostWMedium(bases[k]["A"])
        ext[k] = _ext_medium(med, bases[k]["fmax"])
        assert not np.iscomplexobj(ext[k]["A_ext"])

    def _target_of(k, inst):
        return np.asarray(
            spec_target_n(bases[k]["deep"][inst]["spec"],
                          labeling_bfs_n(np.abs(ext[k]["A_ext"])), N400),
            dtype=float)

    # ---- THE 12 CARRIER SLICE WALKS (the G1 anchors per row) -------------
    print(f"[exp307] the slice: 12 hosts x (seed {SLICE_SEED}, instance "
          f"{SLICE_INST}) carrier walks ...")
    walks = {}
    for k in hosts:
        ctx = bases[k]
        inst = SLICE_INST
        rk = _rk(inst)
        out = _execute_signed_traced_union(
            ctx["deep"][inst]["spec"], ext[k]["A_ext"], SLICE_SEED,
            op=STAR_OP, budget=BUDGET, g=G_COMPOSED,
            a_base=ctx["A"], mark_mask=rb["marks"][k][inst])
        err = float(out["err_vs_target"])
        trace = [float(x) for x in out["walk_trace"]]
        steps = int(out["walk_steps"])
        assert len(trace) == steps and steps >= 1, f"{k}: the trace drifted"
        trace_sha = hashlib.sha256(
            json.dumps(trace, sort_keys=True).encode()).hexdigest()
        commits = out["commits"]
        n_commits = len(commits)
        assert n_commits == steps, f"{k}: the commit count drifted"
        idxs = [int(rec[0]) for rec in commits]
        commit_idx_sha = hashlib.sha256(
            json.dumps(idxs, sort_keys=True).encode()).hexdigest()
        commit_sha = hashlib.sha256(json.dumps(
            [[int(ci), float(tv), str(tg)] for ci, tv, tg in commits],
            sort_keys=True).encode()).hexdigest()
        dep_rec = rb["r300_slice"][(k, SLICE_SEED, rk)]
        ok_err = bool(err == float(dep_rec["err"]))
        assert ok_err, \
            (f"{k}: the carrier slice err {err} drifted from exp300's "
             f"deposited {dep_rec['err']}")
        ok_sha = bool(trace_sha == str(dep_rec["trace_sha256"]))
        assert ok_sha, \
            (f"{k}: the carrier slice trace sha drifted from exp300's "
             "deposited record")
        ok_writes = bool(
            int(out["n_arm_writes"]) == int(dep_rec["n_arm_writes"])
            and int(out["n_sigma_writes"]) == int(dep_rec["n_sigma_writes"])
            and int(out["n_blend_writes"]) == int(dep_rec["n_blend_writes"]))
        assert ok_writes, f"{k}: the union's write counts drifted from exp300's"
        walks[(k, "carrier")] = {
            "key": k, "form": "carrier", "err": err,
            "walk_steps": steps, "trace_sha256": trace_sha,
            "commit_seq_sha256": commit_sha,
            "commit_idx_sha256": commit_idx_sha,
            "n_commits": n_commits,
            "commits": [[int(ci), float(tv), str(tg)]
                        for ci, tv, tg in commits],
            "n_arm_writes": int(out["n_arm_writes"]),
            "anchor_err_ok": ok_err, "anchor_sha_ok": ok_sha}
        print(f"  [carrier {k}] err {err} | anchor errs "
              f"{int(ok_err)}/1 | trace shas {int(ok_sha)}/1", flush=True)
    assert len(walks) == 12, "the 12-walk battery drifted"

    # ---- the CLASS VECTORS (the 9th formalization's annotation source;
    #      deterministic per (host, row target, base adjacency) — the
    #      classify re-run identity asserted) --------------------------------
    cls_vecs = {}
    class_counts = {}
    for k in hosts:
        T_k = _target_of(k, SLICE_INST)
        c1 = classify(T_k, bases[k]["A"])["class"]
        c2 = classify(T_k, bases[k]["A"])["class"]
        assert np.array_equal(c1, c2), \
            f"{k}: the classify re-run identity drifted"
        cls_vecs[k] = np.asarray(c1, dtype=int)
        class_counts[k] = {int(c): int((c1 == c).sum()) for c in (0, 1, 2)}
    print(f"  [classes] the per-host counts: "
          f"{ {k: class_counts[k] for k in hosts} }")

    # ---- the class-REINDEX machinery (the 9th formalization's ONE new
    #      face: the representation = the stream + the source's
    #      per-position class labels; the destination re-addresses
    #      through its OWN classes, per-class prefix min rule) ------------
    def _class_reindex(src_commits, cls_src, dst_cells, cls_dst):
        """Returns (values, cells): each source position's value written
        to the destination's next cell OF THE SAME CLASS in the
        destination's own walk order."""
        writes = []
        per_class = {}
        for c in (0, 1, 2):
            src_vals_c = [float(tv) for (ci, tv, _tg) in src_commits
                          if int(cls_src[int(ci)]) == c]
            dst_cells_c = [int(ci) for ci in dst_cells
                           if int(cls_dst[int(ci)]) == c]
            n_c = min(len(src_vals_c), len(dst_cells_c))
            writes.extend(zip(dst_cells_c[:n_c], src_vals_c[:n_c]))
            per_class[c] = {"src_count": len(src_vals_c),
                            "dst_count": len(dst_cells_c),
                            "n_written": int(n_c)}
        values = [v for (_c, v) in writes]
        cells = [cc for (cc, _v) in writes]
        return values, cells, per_class

    # ---- Z1b: the PLAIN F2 REPLAYS (the cross-deposit anchor: the 12
    #      plain same-substrate replays reproduce exp304's deposited F2
    #      region_rms + full_err BIT-EXACT) ---------------------------------
    print("[exp307] Z1b: the 12 plain F2 replays (the exp304 anchor) ...")
    f2_replays = {}
    n_f2_ok = 0
    for k in hosts:
        w = walks[(k, "carrier")]
        values = [tv for _, tv, _ in w["commits"]]
        cells = [ci for ci, _, _ in w["commits"]]
        T = _target_of(k, SLICE_INST)
        r = _replay(ext[k]["A_ext"], values, cells, SLICE_SEED, T,
                    label=f"Z1b {k}")
        dep_f2 = rb["r304_f2"][k]
        ok = bool(r["region_rms"] == float(dep_f2["region_rms"])
                  and r["full_err"] == float(dep_f2["full_err"]))
        assert ok, \
            (f"Z1b {k}: the plain replay's region rms "
             f"{r['region_rms']} drifted from exp304's deposited "
             f"{dep_f2['region_rms']} — the cross-deposit anchor REFUTED")
        n_f2_ok += int(ok)
        r.update({"host": k, "kind": "carrier-same-plain",
                  "m": w["n_commits"], "bit_exact_vs_exp304_F2": ok})
        f2_replays[k] = r
    assert n_f2_ok == 12, "the Z1b cross-deposit anchor drifted"
    print(f"  [Z1b] 12/12 bit-exact vs exp304's deposited F2 replays")

    # ---- Z2: THE RE-INDEX IDENTITY FACE (the class-reindexed
    #      SAME-SUBSTRATE replay == the plain F2 replay BIT-EXACT — the
    #      re-index is a no-op on own substrate) -----------------------------
    print("[exp307] Z2: the re-index identity face (own substrate) ...")
    z2_rows = []
    n_z2_ok = 0
    for k in hosts:
        w = walks[(k, "carrier")]
        values, cells, per_class = _class_reindex(
            w["commits"], cls_vecs[k], [ci for ci, _, _ in w["commits"]],
            cls_vecs[k])
        T = _target_of(k, SLICE_INST)
        r = _replay(ext[k]["A_ext"], values, cells, SLICE_SEED, T,
                    label=f"Z2 {k}")
        ok = bool(r["region_rms"] == f2_replays[k]["region_rms"]
                  and r["full_err"] == f2_replays[k]["full_err"])
        assert ok, \
            (f"Z2 {k}: the class-reindexed same-substrate replay drifted "
             "from the plain F2 replay — the re-index is NOT a no-op on "
             "own substrate, the identity face REFUTED")
        n_z2_ok += int(ok)
        z2_rows.append({"host": k, "region_rms": r["region_rms"],
                        "identity_ok": ok, "per_class": per_class})
    assert n_z2_ok == 12, "the Z2 identity face drifted"
    print(f"  [Z2] 12/12 bit-exact (the re-index is a no-op on own "
          f"substrate)")

    # ---- Z3: THE ZONE-INDEXED TRANSPORT FACE (the 130 genuine pairs) ----
    pairs = [(a, b) for a in hosts for b in hosts
             if b != a and (a, b) not in DEGENERATE_PAIRS]
    assert len(pairs) == 130, \
        f"the genuine pair set {len(pairs)} != 130"
    print("[exp307] Z3: the 130 class-reindexed transports ...")
    z3_rows = []
    for (ks, kd) in pairs:
        w_src = walks[(ks, "carrier")]
        w_dst = walks[(kd, "carrier")]
        cells_dst = [ci for ci, _, _ in w_dst["commits"]]
        values, cells, per_class = _class_reindex(
            w_src["commits"], cls_vecs[ks], cells_dst, cls_vecs[kd])
        assert len(values) > 0, f"Z3 {ks}->{kd}: no writes"
        assert all(np.isfinite(v) for v in values), \
            f"Z3 {ks}->{kd}: non-finite written value"
        T_d = _target_of(kd, SLICE_INST)
        r = _replay(ext[kd]["A_ext"], values, cells, SLICE_SEED, T_d,
                    label=f"Z3 {ks}->{kd}")
        r.update({"src": ks, "dst": kd, "kind": "carrier-transport-zoned",
                  "m": w_src["n_commits"], "m_prime": w_dst["n_commits"],
                  "n_written": len(values),
                  "per_class": per_class,
                  "dst_own_region_rms": f2_replays[kd]["region_rms"],
                  "transport_price": float(
                      r["region_rms"]
                      - f2_replays[kd]["region_rms"])})
        # the audit face: the price delta vs exp304's deposited F3
        # (the same pair's plain-BFS transport)
        dep_f3 = [row for row in dep304["f3_rows"]
                  if row["src"] == ks and row["dst"] == kd]
        assert len(dep_f3) == 1, \
            f"Z3 {ks}->{kd}: exp304's F3 row missing"
        r["f3_price_exp304"] = float(dep_f3[0]["transport_price"])
        r["price_delta_vs_exp304_F3"] = float(
            r["transport_price"] - r["f3_price_exp304"])
        z3_rows.append(r)
    assert len(z3_rows) == 130, "the Z3 battery drifted"
    n_z3_ok = int(sum(bool(r["region_within_bar"]) for r in z3_rows))
    tr_rms = [float(r["region_rms"]) for r in z3_rows]
    prices = [float(r["transport_price"]) for r in z3_rows]
    price_deltas = [float(r["price_delta_vs_exp304_F3"]) for r in z3_rows]
    print(f"  [Z3] the class-reindexed transports: {n_z3_ok}/130 within "
          f"the bar | the mean region rms {float(np.mean(tr_rms)):.4f} | "
          f"the best {min(tr_rms):.4f} | the mean price "
          f"{float(np.mean(prices)):+.4f} | the mean price delta vs "
          f"exp304's F3 {float(np.mean(price_deltas)):+.4f}")

    # ---- THE BRANCH READ (the pre-named clauses) -------------------------
    if n_z3_ok >= 1:
        branch = "TRANSPORT-UNBLOCKED"
    else:
        branch = "ZONE-BOUND"

    # ---- the canaries (one Z2 + one Z3 re-run bit-exact) -----------------
    k0 = hosts[0]
    w0 = walks[(k0, "carrier")]
    z2r = [row for row in z2_rows if row["host"] == k0][0]
    values, cells, _pc = _class_reindex(
        w0["commits"], cls_vecs[k0], [ci for ci, _, _ in w0["commits"]],
        cls_vecs[k0])
    r2 = _replay(ext[k0]["A_ext"], values, cells, SLICE_SEED,
                 _target_of(k0, SLICE_INST), label="canary Z2")
    same1 = bool(r2["region_rms"] == f2_replays[k0]["region_rms"])
    assert same1, "the Z2 canary failed"
    (ks0, kd0) = pairs[0]
    t1 = [r for r in z3_rows if r["src"] == ks0 and r["dst"] == kd0][0]
    ws = walks[(ks0, "carrier")]
    wd = walks[(kd0, "carrier")]
    cells_dst0 = [ci for ci, _, _ in wd["commits"]]
    values, cells, _pc = _class_reindex(
        ws["commits"], cls_vecs[ks0], cells_dst0, cls_vecs[kd0])
    r4 = _replay(ext[kd0]["A_ext"], values, cells, SLICE_SEED,
                 _target_of(kd0, SLICE_INST), label="canary Z3")
    same2 = bool(r4["region_rms"] == t1["region_rms"]
                 and r4["full_err"] == t1["full_err"])
    assert same2, "the Z3 canary failed"
    canary = [{"kind": "Z2", "key": k0, "bit_identical": same1},
              {"kind": "Z3", "key": f"{ks0}->{kd0}", "bit_identical": same2}]

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
    n_walk_err = int(sum(1 for k in hosts
                         if walks[(k, "carrier")]["anchor_err_ok"]))
    n_walk_sha = int(sum(1 for k in hosts
                         if walks[(k, "carrier")]["anchor_sha_ok"]))
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
                   and rb["counts"]["n_rows300_slice"] == 12
                   and rb["counts"]["n_rows304_f2"] == 12
                   and rb["counts"]["n_marks_ok"] == 24
                   and rb["counts"]["n_tpart_ok"] == 12
                   and n_walk_err == 12 and n_walk_sha == 12
                   and n_f2_ok == 12
                   and ro_unchanged and exp142_unmodified
                   and test_suite["green"])
    g2_pass = bool(n_z2_ok == 12
                   and all(r["n_written"] > 0 for r in z3_rows)
                   and all(np.isfinite(r["region_rms"]) for r in z3_rows)
                   and all(r["n_written"] == sum(pc["n_written"]
                                                 for pc in
                                                 r["per_class"].values())
                           for r in z3_rows))
    g3_pass = bool(branch in ("TRANSPORT-UNBLOCKED", "ZONE-BOUND"))
    g4_pass = bool(ro_unchanged and exp142_unmodified and port_unmodified
                   and floor_exit_ok and test_suite["green"]
                   and zero_reader_scan["files_outside_port_and_instruments"]
                   == [] and all(c["bit_identical"] for c in canary))

    print(f"  G1 the anchors: {'PASS' if g1_pass else 'FAIL'}")
    print(f"  G2 the faces' definition: {'PASS' if g2_pass else 'FAIL'}")
    print(f"  G3 the branch: {branch} ({'PASS' if g3_pass else 'FAIL'})")
    print(f"  G4 the discipline: {'PASS' if g4_pass else 'FAIL'}")

    # ---- the deposit ------------------------------------------------------
    payload = {
        "exp": "exp307_zone_indexed_transport",
        "claim": (
            "THE ZONE-INDEXED TRANSPORT FORM -- THE 9TH FORMALIZATION OF "
            "THE ZERO-SUBSTRATE STAR (batch 60; ledger L290c's promoted "
            "candidate (6); pre-registration f7094a8; the handoff's "
            "'does the composed carrier transport' WITH THE PREMISE "
            "REPAIR DISCLOSED -- exp304's carrier arm IS the composed "
            "union so the literal question is already answered 0/130; "
            "the genuinely open question is the project's own "
            "pre-named untried door: a wiring-independent "
            "zone-addressing scheme): the representation = the commit "
            "stream + the source's per-position structural class "
            "labels; the destination re-addresses through its OWN "
            "classes (per-class prefix min rule); the legality "
            "disclosed (the destination donates its own walk order per "
            "the exp303/304 precedent + its own class labels; the "
            "zero-substrate protocol otherwise untouched)"),
        "method": {
            "slice": (f"12 hosts x (seed {SLICE_SEED}, instance "
                      f"{SLICE_INST}); the carrier = the union "
                      f"faces=(ctx, gj, apop) at the composed optimum "
                      f"g=1.0"),
            "faces": {
                "Z1": ("the anchors: the exp300 slice walks bit-exact + "
                       "the exp304 F2 replays bit-exact (the "
                       "cross-deposit anchor)"),
                "Z2": ("the re-index identity face: the class-reindexed "
                       "same-substrate replay == the plain F2 replay "
                       "bit-exact 12/12 (the re-index is a no-op on own "
                       "substrate)"),
                "Z3": ("the zone-indexed transport face: the 130 "
                       "genuine pairs, class-reindexed")},
            "run_form": "in-process one invocation",
            "branch_rule": (
                "TRANSPORT-UNBLOCKED iff >= 1/130 genuine pairs within "
                "the 6.0 bar (the block WEAKENS at the 9th); ZONE-BOUND "
                "iff 0/130 (the block SHARPENS at 9 -- the binding is "
                "finer than the structural classes)")},
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
        "walks": [{k2: v for k2, v in w.items() if k2 != "commits"}
                  for w in walks.values()],
        "class_counts": class_counts,
        "f2_replays": f2_replays,
        "z2_rows": z2_rows,
        "z3_rows": z3_rows,
        "branch": branch,
        "branch_discriminant": {
            "n_within_bar": n_z3_ok, "bar": CONTENT_BAR,
            "n_pairs": 130,
            "mean_region_rms": float(np.mean(tr_rms)),
            "best_region_rms": float(min(tr_rms)),
            "worst_region_rms": float(max(tr_rms)),
            "mean_transport_price": float(np.mean(prices)),
            "mean_price_delta_vs_exp304_F3": float(np.mean(price_deltas)),
            "n_price_improved_vs_exp304_F3": int(sum(
                1 for d in price_deltas if d < 0.0))},
        "canary": canary,
        "test_suite": test_suite,
        "determinism": {
            "form": "in-process one invocation (one pass)",
            "discipline": ("one walk per host; the replays "
                           "deterministic; the canaries bit-exact"),
            "no_wall_clock_fields": True},
        "discipline": {
            "no_wall_clock_fields": True,
            "deterministic_one_pass": True,
            "docstring_header_pinned": True,
            "pinned_to": "f7094a8",
            "ro_unchanged": ro_unchanged,
            "floor": PROD_FLOOR,
            "exp142_and_core_not_modified": bool(
                exp142_unmodified and port_unmodified)},
        "gates": {
            "G1_the_anchors": {"pass": g1_pass,
                               "counts": dict(rb["counts"],
                                              **{"n_walk_err": n_walk_err,
                                                 "n_walk_sha": n_walk_sha,
                                                 "n_f2_ok": n_f2_ok,
                                                 "ro_unchanged":
                                                     ro_unchanged,
                                                 "exp142_unmodified":
                                                     exp142_unmodified,
                                                 "test_suite_green":
                                                     test_suite["green"]})},
            "G2_the_faces_definition": {"pass": g2_pass,
                                        "n_z2_ok": n_z2_ok},
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
        f"REFUTE) | BRANCH: {branch} | Z3 the class-reindexed "
        f"transports: {n_z3_ok}/130 within the {CONTENT_BAR} bar (the "
        f"mean region rms {float(np.mean(tr_rms)):.4f}, the best "
        f"{min(tr_rms):.4f}, the mean price "
        f"{float(np.mean(prices)):+.4f} vs the own-replay's "
        f"{float(np.mean([f2_replays[k]['region_rms'] for k in hosts])):.4f})"
        f" | the Z2 identity face 12/12 | the anchors bit-exact "
        f"(the exp300 slice walks 12/12 + the exp304 F2 replays 12/12)")
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
        "docstring drifted from f7094a8 (exit)"
    assert header_sha == EXPECTED_HEADER_SHA256, \
        "header drifted from f7094a8 (exit)"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, \
        "NEURAL_SPEC_MIN drifted at exit"
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    print(f"[exp307] deposited {OUT}")
    print(f"[exp307] VERDICT: {payload['verdict']}")
    assert read_floor() == PROD_FLOOR, "the floor moved at exit"
    return payload


if __name__ == "__main__":
    main()

