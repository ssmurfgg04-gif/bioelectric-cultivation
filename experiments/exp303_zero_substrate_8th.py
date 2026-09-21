#!/usr/bin/env python3
"""exp303 — THE ZERO-SUBSTRATE 8TH FORMALIZATION: THE TRANSPORT FORM
(the commit stream as the pattern representation; batch 57; ledger
L287's registered next (c) — the standing frontier sharpened by
exp301/exp302: the carrier's value changes are the program's own spec
re-asserted; the reader's excess IS the un-asserted spec; exp301
landed WRITE-SIDE-CARRIED: the commit stream is the write-side object;
exp288 landed SPEC-UNIFORM: the spec-layer face is class-blind).

THE 8TH FORMALIZATION CLASS: the prior 7 formalizations quantified
over the substrate's structure (the 5 static metrics, the temporal
schedule, the gauge quotient). The 8th states the constraint on the
PROGRAM'S OWN OUTPUT — the commit stream C = [(i_1, v_1), ..., (i_m,
v_m)] (the write-side object exp287 deposited and exp301 carried): the
stream is a substrate-independent pattern representation iff replaying
it into a fresh substrate (the wiring ONLY — no spec install, no
clamps, no encode window, no carried state) reconstructs the pattern
within the pre-named bar. The zero-substrate question in its 8th form:
does the program's write product transport the pattern, or is the
write product as substrate-BOUND as the state it came from?

THE INSTRUMENT (the landed machinery COMPOSED VERBATIM): the 72-row
substituted battery (exp256's) walked in the dormant form (the exp302
landed walk machinery at g=0.0, arm A0 — the errs + the commit-stream
digests MUST reproduce exp256's deposited errs BIT-EXACT 72/72 and
exp287's deposited commit_seq_sha256 BIT-EXACT 72/72 — the streams ARE
the deposited commit sequences), then the REPLAY INSTRUMENT (zero
knobs; every constant inherited): a fresh GraphCollective on the SAME
extended medium A_ext (the read chain's own output), NO spec install /
clamps / encode; the stream's values written into theta AND V at the
walk order's cells IN THE COMMIT ORDER; the walk's own settle (15.0
t.u. at the walk's own dt) at the production floor; the decode.
THE PREDICATE (zero-knob): the REGION-SCOPED reconstruction RMS over
the written cells vs the row's target, vs the pre-named bar ERR_BAR
6.0 mV (the house's registered decode bar — never fit). The scoping is
the machinery's own: the written set IS the commit-index set (the
stream's content claim is exactly the walked cells — the encode's
contribution to the un-walked zones is NOT the stream's to claim; the
full-target decode recorded audit-only).

THE FACES (each evaluated exactly once):
  R2  THE SAME-SUBSTRATE CONTENT FACE: 72 replays (each row's own
      stream on its own substrate, the row's own seed) — the
      region-scoped error vs the 6.0 bar (the stream IS a
      representation of the walked region's pattern, or it is not).
  R3  THE TRANSPORT FACE: the 12 x 11 ordered host-pair slice (the
      pre-named transport slice: the source = the host's (seed 1, i0)
      stream; the destination = each OTHER host's i0 — the
      destination's own walk order computed by the landed frontier
      rule on the destination's own A_ext + the destination's own
      compiled target; the stream's first min(m, m') values written at
      the destination order's first min(m, m') cells; the counts
      recorded) — the region-scoped error vs the SAME 6.0 bar.
  R4  THE BREAK PROBE (the FORALL direction, audit): the transport
      price (the transported error minus the destination's own
      same-substrate replay error — the content vs the destination's
      own program output) per pair.

PRE-REGISTERED GATES:

  R1  THE ANCHORS: the 72 dormant walks reproduce exp256's deposited
      substituted errs BIT-EXACT 72/72 (the verified flags 72/72) +
      exp282's walk anchors (the walk_end_rms + the trace shas +
      err_exact 72/72) + exp287's deposited commit_seq_sha256
      BIT-EXACT 72/72 (the streams ARE the deposited commit
      sequences); the rebuild chain sha-asserted; the floor -60.0
      asserted at the settle/decode of every replay and at exit; 6
      deposits READ-ONLY (exp243/256/272/273/282/287 — sha
      before/after); the test suite green.
  R2  THE CONTENT FACE: the 72 same-substrate replays deterministic
      (the canary re-runs one replay bit-exact); the errors finite
      72/72; the branch clause (below).
  R3  THE TRANSPORT FACE: the 132 transports deterministic; the
      errors finite 132/132; the counts (m, m', n_written) recorded
      per pair; the branch clause (below).
  R4  THE DISCIPLINE: deterministic; no wall-clock fields; the
      docstring + header pinned to this pre-registration commit,
      asserted at entry AND exit; exp142 and the core NOT modified;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named):
  TRANSPORT-BREAKS   iff the R2 content face holds (>= 1 of the 72
                     same-substrate replays within the 6.0 bar... no —
                     PRE-NAMED STRICTLY: the R2 face HOLDS iff the
                     MAJORITY (>= 37/72) of the same-substrate
                     replays land within the 6.0 bar AND >= 1 of the
                     132 transports lands within the 6.0 bar — the
                     zero-substrate representation EXISTS in the 8th
                     form (the honest unblocking event);
  TRANSPORT-REFINES  iff the R2 face holds (>= 37/72 within the bar)
                     and ALL 132 transports fail — the stream is a
                     representation but substrate-BOUND (the block
                     DEEPENS: even the program's own output does not
                     transport — the zero-substrate path stays blocked
                     at 8 formalizations);
  TRANSPORT-ABSENT   otherwise (the stream is not even a same-substrate
                     representation — the constraint holds at its
                     strongest form; the write product is not the
                     pattern).

RUN: 72 walks + 72 same-substrate replays + 132 transports ~ 4-7 min
in-process (the replays skip the encode + the per-commit stepping —
settle-only); serial, BLAS pinned.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp303_zero_substrate_8th.json")


def main() -> dict:
    # ==== BODY (the body-only discipline: the bytes after
    #      `def main() -> dict:` are the only ones the body commit
    #      touches; the docstring/imports/constants above byte-unchanged,
    #      pinned to pre-registration commit 7a968de; gates R1-R4
    #      evaluated exactly once. THE COMPOSITION: exp302's landed walk
    #      machinery (the dormant form: g=0.0, arm A0 — the coupling
    #      block skipped, the pin inert; the errs + the commit streams
    #      reproduce exp256's/exp287's deposits BIT-EXACT) + the REPLAY
    #      INSTRUMENT (zero knobs: a fresh GraphCollective on the read
    #      chain's own A_ext, NO spec install / clamps / encode, the
    #      stream's values at the walk order's cells in the commit
    #      order, the walk's own settle, the decode) =================
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
    #      the 7a968de pre-registration, byte-for-byte; asserted BEFORE
    #      and AFTER the work) ------------------------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "ed18e68aa631cb66b3f760de43bd3faa6c35ddfbd5e87de0aebd39a4014a3f03")
    EXPECTED_HEADER_SHA256 = (
        "e326abeda28ec71c74701cfc176117ae80e1016c6ccd9aa8feb6909b44bc38b9")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 7a968de"
    assert header_ok, "header drifted from 7a968de"

    # ---- the -60.0 floor (G4: asserted at exit; the exp169-import
    #      discipline — the whole reader chain imported FIRST, the floor
    #      restored after) --------------------------------------------
    PROD_FLOOR = -60.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)   # exp169's PIN_MODULES form
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)

    def set_floor(v):
        for _m in PINNED:
            if hasattr(_m, "NEURAL_SPEC_MIN"):
                _m.NEURAL_SPEC_MIN = float(v)

    def read_floor():
        vals = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                for m in PINNED}
        uv = set(float(v) for v in vals.values())
        assert len(uv) == 1, f"the pinned floor set disagrees: {vals}"
        return uv.pop()

    set_floor(PROD_FLOOR)
    assert read_floor() == PROD_FLOOR, "floor restore failed"
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (core)"
    assert _m142.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (m142)"

    # ---- the frozen read configuration (exp256's battery constants;
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
    BUDGET = 8
    assert BUDGET == int(STEPS_PER_CELL) == 8, \
        "the production budget drifted from exp142's STEPS_PER_CELL"
    SETTLE_H = 15.0                        # the walk's own settle
    # THE BRANCH BARS (pre-named at 7a968de, numeric, never fit):
    CONTENT_BAR = float(ERR_BAR)           # 6.0 — the house's own bar
    CONTENT_MAJORITY = 37                  # >= 37/72 within the bar
    TRANSPORT_SLICE_SEED = 1               # the pre-named transport slice
    TRANSPORT_SLICE_INST = 0

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

    PORT_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                             "collective.py")
    EXP142_FILE = os.path.join(ROOT, "experiments", "exp142_sign_read.py")
    port_sha_entry = _sha(PORT_FILE)
    exp142_sha_entry = _sha(EXP142_FILE)

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      read, re-verified byte-unchanged at the end; the
    #      pre-registration's named list, 6 deposits) --------------------
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
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP282, DEP287)
    _dep_names = {DEP243: "exp243_deposit", DEP256: "exp256_deposit",
                  DEP272: "exp272_deposit", DEP273: "exp273_deposit",
                  DEP282: "exp282_deposit", DEP287: "exp287_deposit"}
    for _p in READ_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"
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

    # ---- the host frame (exp272's per_host order — the house frame) ----
    hosts = [r["host"] for r in dep272["per_host"]]
    assert len(hosts) == 12 and len(set(hosts)) == 12, \
        "the 12-host frame drifted"
    assert dep273["hosts"] == hosts, "exp273's host frame drifted"
    assert dep282["hosts"] == hosts, "exp282's host frame drifted"
    assert dep287["hosts"] == hosts, "exp287's host frame drifted"
    assert sorted(dep243["classes"]) == sorted(hosts), \
        "exp243's classes drifted from the host frame"
    outliers = dep273["outliers"]
    assert outliers == ["H3", "H5"], \
        f"exp273's outlier pre-name drifted: {outliers}"
    rec272 = {r["host"]: r for r in dep272["per_host"]}

    # ---- exp208's classify VERBATIM (the rebuild's boundary asserts) ----
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

    # ---- THE READ CHAIN (exp289's/exp302's landed
    #      _scoped_row_read form VERBATIM, factored: the extended medium
    #      A_ext = PN1+PN2 + TC1 + TC2 on the row's medium — the
    #      substrate the walks and the replays share) ------------------
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

    # ---- THE TRACED WALK (exp302's landed
    #      _execute_signed_traced_union_stress VERBATIM — the dormant
    #      form at g=0.0/A0: the coupling block skipped, the pin inert;
    #      the errs + the commit streams reproduce exp256's/exp287's
    #      deposited forms BIT-EXACT) ---------------------------------
    def _execute_signed_traced(spec, adjacency, seed, op, budget):
        floor_rec: dict = {}
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
                    "reg_init_ok": reg_init_ok, "dt": dt, "target": target}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        floor_rec["encode_start"] = read_floor()
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
            # the verbatim commit branch chain (the floor read AT STEP
            # TIME is live — the production floor here)
            if c.phi_spec[i] >= _m142.NEURAL_SPEC_MIN:       # (e)
                commit_base = c.phi_spec[i]
                src_tag = "spec"
            elif canon_src is not None:
                commit_base = canon_src[i]
                src_tag = "canon"
            else:
                commit_base = c.theta[src]
                src_tag = "parent"
            theta_new = commit_base + c.rng.normal(0.0, COMMIT_NOISE)
            written = theta_new
            c.theta[i] = written
            c.V[i] = written
            commits.append((int(i), float(written), src_tag))
            # THE PORT'S POPULATION (the walk's own; the replays never
            # touch the register — the zero-substrate discipline is
            # protocol-level, disclosed)
            c.phi_history[i] = written
            trace.append(float(np.sqrt(np.mean((c.V - target) ** 2))))
        floor_rec["walk_last_commit"] = read_floor()
        coverage_ok = bool([ci for ci, tv, tg in commits]
                           == [oi for oi, osrc in order])
        assert coverage_ok, \
            "the commit sequence drifted from the walked order"
        floor_rec["settle_start"] = read_floor()
        c.run(SETTLE_H, dt=dt)
        floor_rec["decode_start"] = read_floor()
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
               "dt": dt, "target": target}
        return out

    # ---- THE REPLAY INSTRUMENT (zero knobs; the zero-substrate
    #      protocol: a fresh GraphCollective on A_ext — the wiring ONLY;
    #      NO write_spec_layer, NO clamps, NO encode window, NO carried
    #      state (the register port exists on the object and is NEVER
    #      touched — disclosed); the stream's values written into theta
    #      AND V at the given cells IN THE COMMIT ORDER; the walk's own
    #      settle at the production floor; the decode) -----------------
    def _replay(A_ext, values, cells, seed, target, label=""):
        assert len(values) == len(cells), \
            f"{label}: the replay's value/cell counts disagree"
        gamma, mu = STAR_OP["gamma"], STAR_OP["mu"]
        dt = star_dt(gamma, float(np.abs(A_ext).sum(axis=1).max()))
        c = GraphCollective(adjacency=A_ext, seed=seed, gamma=gamma,
                            mu_theta=mu)
        # the ZERO-SUBSTRATE protocol: nothing but the wiring + the
        # stream (the constructor's own seeded init; no spec install)
        for idx, v in zip(cells, values):
            c.theta[idx] = v
            c.V[idx] = v
        floor_before_settle = read_floor()
        assert floor_before_settle == PROD_FLOOR, \
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
                "n_written": int(len(cells)),
                "dt": dt,
                "region_within_bar": bool(region_rms <= CONTENT_BAR),
                "full_within_bar": bool(full_err <= CONTENT_BAR)}

    # ---- THE REBUILD (the sha-asserted rebuild against exp243's OWN
    #      records + the anchor re-reads; deterministic) ---------------
    def _rebuild():
        counts = {"n_hosts": 0, "n_sha_ok": 0, "n_edges_ok": 0,
                  "n_canon_ok": 0, "h0_echo_h1": False, "n_fmax_ok": 0,
                  "n_nonneg_ok": 0, "n_rows256": 0, "n_structure_ok": 0,
                  "n_worst_eq_max": 0, "n_deep_targets_ok": 0,
                  "n_medium_shas_ok": 0, "n_rows282": 0,
                  "n_282_chain_ok": 0, "n_rows287": 0}
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
            bnd_dual = bool(nb == int(rec272[h]["n_boundary_cells_base"]))
            assert sha_ok and edges_ok and bnd_ok and bnd_dual \
                and canon_ok, \
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
                "boundary_count_matches_2way": bool(bnd_ok and bnd_dual),
                "canon_identity_ok": canon_ok,
                "f_max_matches_exp243_record": fmax_ok,
                "base_non_negative": nonneg})
        counts["h0_echo_h1"] = bool(np.array_equal(bases["H0"]["A"],
                                                   bases["H1"]["A"]))
        assert counts["h0_echo_h1"], \
            "the chain class's n=400 call site must echo H1 bit-exactly"

        # exp256's 72 rows — the substituted records the R1 anchor reads
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
                f"{r['host']} s{r['seed']}: the substituted structure " \
                "drifted"
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

        # THE EXP287 RE-READ (the commit-layer anchor deposit — the
        # streams' bit-exactness source)
        rows287 = dep287["rows"]
        counts["n_rows287"] = len(rows287)
        assert len(rows287) == 72, "exp287's 72-row deposit drifted"
        r287 = {}
        for r in rows287:
            key = (r["host"], int(r["seed"]), r["row_key"])
            assert key not in r287, f"duplicate exp287 row {key}"
            assert "commit_seq_sha256" in r and "cvt_rms" in r, \
                f"{key}: exp287's row record is missing anchor fields"
            r287[key] = r

        integrity = {"counts": counts, "rebuild_report": rebuild_report,
                     "exp256_reread": {
                         "n_rows": counts["n_rows256"],
                         "n_substituted_instance_records": len(dep_sub),
                         "n_structure_ok": counts["n_structure_ok"],
                         "n_worst_eq_max": counts["n_worst_eq_max"],
                         "n_deep_targets_ok": counts["n_deep_targets_ok"],
                         "n_medium_shas_ok": counts["n_medium_shas_ok"]},
                     "exp282_reread": {"n_rows": counts["n_rows282"],
                                       "branch": dep282["branch"],
                                       "n_chain_ok":
                                           counts["n_282_chain_ok"]},
                     "exp287_reread": {"n_rows": counts["n_rows287"]}}
        return {"bases": bases, "dep_sub": dep_sub, "r282": r282,
                "r287": r287, "integrity": integrity}

    # ---- the row-key helper ------------------------------------------
    def _rk(inst):
        return f"r{DEEP_RUNG:g}i{inst}"

    # ---- THE DRIVER: the 72 dormant walks (the streams' source), the
    #      72 same-substrate replays (R2), the 132 transports (R3), the
    #      canary (the replay determinism) ------------------------------
    print("=== exp303: THE ZERO-SUBSTRATE 8TH FORMALIZATION (the "
          "transport form — is the commit stream a substrate-bound "
          "object or a pattern representation?) ===")
    print(f"  battery: 12 hosts x 3 seeds {list(SEEDS_RUN)} x 2 deep "
          f"instances at n={N400} = 72 walks (the dormant form; the "
          f"errs + the streams anchored bit-exact vs exp256/exp282/"
          f"exp287) + 72 same-substrate replays (R2) + 132 transports "
          f"(R3, the pre-named slice: seed {TRANSPORT_SLICE_SEED}, "
          f"instance {TRANSPORT_SLICE_INST}) at the bar {CONTENT_BAR}")
    rb = _rebuild()
    bases = rb["bases"]

    # the extended media (one per host — the walks' and the replays'
    # shared substrate; the read chain's own output)
    ext = {}
    for k in hosts:
        med = HostWMedium(bases[k]["A"])
        ext[k] = _ext_medium(med, bases[k]["fmax"])
        assert not np.iscomplexobj(ext[k]["A_ext"])

    # ---- the 72 WALKS (the streams' source; the R1 anchors per row) --
    walks = {}
    for k in hosts:
        ctx = bases[k]
        for s in SEEDS_RUN:
            for inst in DEEP_INSTANCES:
                rk = _rk(inst)
                key = (k, s, rk)
                _lock_read(k, rk, s)
                out = _execute_signed_traced(
                    ctx["deep"][inst]["spec"], ext[k]["A_ext"], s,
                    op=STAR_OP, budget=BUDGET)
                err = float(out["err_vs_target"])
                assert np.isfinite(err), f"{key}: non-finite walk err"
                V = np.asarray(out["final_state"]["V"], dtype=float)
                T = np.asarray(out["target"], dtype=float)
                err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
                a3_ok = bool(round(err_exact, 2) == round(err, 2))
                assert a3_ok, f"{key}: A3 state-convention drift"
                trace = [float(x) for x in out["walk_trace"]]
                steps = int(out["walk_steps"])
                assert len(trace) == steps and steps >= 1, \
                    f"{key}: trace len != walk steps"
                final = trace[-1]
                assert final > 0.0, f"{key}: final RMS == 0"
                trace_sha = hashlib.sha256(
                    json.dumps(trace, sort_keys=True).encode()).hexdigest()
                commits = out["commits"]
                n_commits = len(commits)
                assert n_commits == steps, \
                    f"{key}: the commit count != walk steps"
                idxs = [int(rec[0]) for rec in commits]
                assert len(set(idxs)) == n_commits, \
                    f"{key}: a committed cell written twice"
                assert bool(out["coverage_ok"]), \
                    f"{key}: the write-set coverage drifted"
                commit_sha = hashlib.sha256(json.dumps(
                    [[int(ci), float(tv), str(tg)]
                     for ci, tv, tg in commits],
                    sort_keys=True).encode()).hexdigest()
                # ---- THE R1 ANCHORS (fail=STOP) ----------------------
                d256 = rb["dep_sub"][key]
                assert err == d256["err"], \
                    (f"{key}: the fresh err {err} drifted from exp256's "
                     f"deposited {d256['err']} — the R1 anchor REFUTED")
                assert bool(out["program_verified"]) == d256["verified"], \
                    f"{key}: the verified flag drifted"
                r282 = rb["r282"][key]
                assert final == float(r282["walk_end_rms"]), \
                    f"{key}: the walk_end_rms drifted from exp282's"
                assert trace_sha == r282["trace_sha256"], \
                    (f"{key}: the trace sha drifted from exp282's — the "
                     "walk is not the traced one")
                assert err_exact == float(r282["err_exact"]), \
                    f"{key}: the err_exact drifted from exp282's"
                r287 = rb["r287"][key]
                assert commit_sha == r287["commit_seq_sha256"], \
                    (f"{key}: the commit stream digest drifted from "
                     "exp287's deposited commit_seq_sha256 — the stream "
                     "is not the deposited one")
                walks[key] = {
                    "key": key, "host": k, "seed": int(s),
                    "row_key": rk, "instance": int(inst),
                    "err": err, "err_exact": err_exact,
                    "walk_end_rms": final, "walk_steps": steps,
                    "trace_sha256": trace_sha,
                    "commit_seq_sha256": commit_sha,
                    "commit_idx_sha256": hashlib.sha256(
                        json.dumps(idxs, sort_keys=True).encode()
                    ).hexdigest(),
                    "n_commits": n_commits,
                    "commits": [[int(ci), float(tv), str(tg)]
                                for ci, tv, tg in commits],
                    "cvt_rms": float(np.sqrt(np.mean(
                        (np.asarray([float(tv) for _, tv, _ in commits])
                         - T[np.asarray(idxs, dtype=int)]) ** 2))),
                    "r1_anchor_ok": True}
        print(f"  [walks {k}] 6 rows | errs "
              f"{[walks[(k, s, _rk(i))]['err'] for s in SEEDS_RUN for i in DEEP_INSTANCES]}",
              flush=True)
    assert len(walks) == 72, "the 72-walk battery drifted"
    assert len(_LOCK_LOG) == 72, "the S* lock count drifted"

    # ---- the 72 SAME-SUBSTRATE REPLAYS (R2: the content face) --------
    replays = {}
    for k in hosts:
        ctx = bases[k]
        for s in SEEDS_RUN:
            for inst in DEEP_INSTANCES:
                rk = _rk(inst)
                key = (k, s, rk)
                w = walks[key]
                values = [tv for _, tv, _ in w["commits"]]
                cells = [ci for ci, _, _ in w["commits"]]
                T = np.asarray(
                    spec_target_n(ctx["deep"][inst]["spec"],
                                  labeling_bfs_n(
                                      np.abs(ext[k]["A_ext"])), N400),
                    dtype=float)
                r = _replay(ext[k]["A_ext"], values, cells, s, T,
                            label=f"same {key}")
                r.update({"source": key, "dest": key, "m": w["n_commits"],
                          "m_prime": w["n_commits"], "kind": "same"})
                replays[key] = r
        print(f"  [replays {k}] 6 rows | region rms "
              f"{[round(replays[(k, s, _rk(i))]['region_rms'], 3) for s in SEEDS_RUN for i in DEEP_INSTANCES]}",
              flush=True)
    assert len(replays) == 72, "the 72-replay battery drifted"

    # ---- the 132 TRANSPORTS (R3: the pre-named slice) -----------------
    transports = []
    src_hosts = hosts
    for k in src_hosts:
        src_key = (k, TRANSPORT_SLICE_SEED, _rk(TRANSPORT_SLICE_INST))
        w_src = walks[src_key]
        values = [tv for _, tv, _ in w_src["commits"]]
        m = w_src["n_commits"]
        for kd in hosts:
            if kd == k:
                continue
            dkey = (kd, TRANSPORT_SLICE_SEED, _rk(TRANSPORT_SLICE_INST))
            w_dst = walks[dkey]
            cells_dst = [ci for ci, _, _ in w_dst["commits"]]
            m_prime = w_dst["n_commits"]
            n_written = min(m, m_prime)
            T_d = np.asarray(
                spec_target_n(bases[kd]["deep"][TRANSPORT_SLICE_INST]
                              ["spec"],
                              labeling_bfs_n(
                                  np.abs(ext[kd]["A_ext"])), N400),
                dtype=float)
            r = _replay(ext[kd]["A_ext"], values[:n_written],
                        cells_dst[:n_written], TRANSPORT_SLICE_SEED, T_d,
                        label=f"transport {k}->{kd}")
            r.update({"source": src_key, "dest": dkey,
                      "src_host": k, "dst_host": kd,
                      "m": m, "m_prime": m_prime,
                      "n_written": n_written, "kind": "transport",
                      # R4's transport price: the transported error
                      # minus the destination's own same-substrate
                      # replay error (the content vs the destination's
                      # own program output)
                      "dst_own_region_rms":
                          replays[dkey]["region_rms"],
                      "transport_price": float(
                          r["region_rms"]
                          - replays[dkey]["region_rms"])})
            transports.append(r)
        print(f"  [transports {k}] 11 dests | region rms "
              f"{[round(r['region_rms'], 2) for r in transports[-11:]]}",
              flush=True)
    assert len(transports) == 132, "the 132-transport battery drifted"

    # ---- THE DETERMINISM CANARY (the replay instrument: one same-
    #      substrate replay + one transport re-run bit-exact) ----------
    canary = []
    ck1 = (hosts[0], SEEDS_RUN[0], _rk(DEEP_INSTANCES[0]))
    r1 = replays[ck1]
    w1 = walks[ck1]
    T1 = np.asarray(
        spec_target_n(bases[hosts[0]]["deep"][DEEP_INSTANCES[0]]["spec"],
                      labeling_bfs_n(np.abs(ext[hosts[0]]["A_ext"])), N400),
        dtype=float)
    r2 = _replay(ext[hosts[0]]["A_ext"],
                 [tv for _, tv, _ in w1["commits"]],
                 [ci for ci, _, _ in w1["commits"]],
                 SEEDS_RUN[0], T1, label="canary same")
    same1 = bool(r2["region_rms"] == r1["region_rms"]
                 and r2["full_err"] == r1["full_err"]
                 and r2["dt"] == r1["dt"])
    assert same1, "the same-substrate replay canary failed"
    canary.append({"kind": "same", "key": ck1, "bit_identical": same1})
    k0 = hosts[0]
    kd0 = hosts[1]
    t_src = [t for t in transports
             if t["src_host"] == k0 and t["dst_host"] == kd0][0]
    w_src = walks[(k0, TRANSPORT_SLICE_SEED,
                   _rk(TRANSPORT_SLICE_INST))]
    w_dst = walks[(kd0, TRANSPORT_SLICE_SEED,
                   _rk(TRANSPORT_SLICE_INST))]
    n_w = t_src["n_written"]
    T_d0 = np.asarray(
        spec_target_n(bases[kd0]["deep"][TRANSPORT_SLICE_INST]["spec"],
                      labeling_bfs_n(np.abs(ext[kd0]["A_ext"])), N400),
        dtype=float)
    r4 = _replay(ext[kd0]["A_ext"],
                 [tv for _, tv, _ in w_src["commits"]][:n_w],
                 [ci for ci, _, _ in w_dst["commits"]][:n_w],
                 TRANSPORT_SLICE_SEED, T_d0, label="canary transport")
    same2 = bool(r4["region_rms"] == t_src["region_rms"]
                 and r4["full_err"] == t_src["full_err"]
                 and r4["dt"] == t_src["dt"])
    assert same2, "the transport canary failed"
    canary.append({"kind": "transport",
                   "key": f"{k0}->{kd0}", "bit_identical": same2})

    # ---- THE BRANCH READ (zero knobs, the pre-named clauses) ----------
    n_content_ok = int(sum(bool(r["region_within_bar"])
                           for r in replays.values()))
    content_face_holds = bool(n_content_ok >= CONTENT_MAJORITY)
    n_transport_ok = int(sum(bool(r["region_within_bar"])
                             for r in transports))
    if content_face_holds and n_transport_ok >= 1:
        branch = "TRANSPORT-BREAKS"
    elif content_face_holds and n_transport_ok == 0:
        branch = "TRANSPORT-REFINES"
    else:
        branch = "TRANSPORT-ABSENT"

    # ---- the summaries -------------------------------------------------
    same_rms = [float(r["region_rms"]) for r in replays.values()]
    tr_rms = [float(r["region_rms"]) for r in transports]
    prices = [float(r["transport_price"]) for r in transports]
    summaries = {
        "same_substrate": {
            "n": 72, "n_within_bar": n_content_ok,
            "bar": CONTENT_BAR, "majority_needed": CONTENT_MAJORITY,
            "face_holds": content_face_holds,
            "mean_region_rms": float(np.mean(same_rms)),
            "worst_region_rms": float(max(same_rms)),
            "best_region_rms": float(min(same_rms)),
            "n_full_within_bar": int(sum(bool(r["full_within_bar"])
                                         for r in replays.values())),
            "mean_full_err": float(np.mean(
                [r["full_err"] for r in replays.values()]))},
        "transport": {
            "n": 132, "n_within_bar": n_transport_ok,
            "bar": CONTENT_BAR,
            "mean_region_rms": float(np.mean(tr_rms)),
            "worst_region_rms": float(max(tr_rms)),
            "best_region_rms": float(min(tr_rms)),
            "mean_transport_price": float(np.mean(prices)),
            "n_price_negative": int(sum(p < 0.0 for p in prices)),
            "n_full_within_bar": int(sum(bool(r["full_within_bar"])
                                         for r in transports)),
            "n_written_min": int(min(r["n_written"]
                                     for r in transports)),
            "n_written_max": int(max(r["n_written"]
                                     for r in transports)),
            "n_m_eq_mprime": int(sum(r["m"] == r["m_prime"]
                                     for r in transports))},
        "per_source_host": {
            k: {"mean_region_rms": float(np.mean(
                    [r["region_rms"] for r in transports
                     if r["src_host"] == k])),
                "n_within_bar": int(sum(bool(r["region_within_bar"])
                                        for r in transports
                                        if r["src_host"] == k))}
            for k in hosts}}

    # ---- the gate tallies ----------------------------------------------
    g1 = dict(rb["integrity"]["counts"])
    g1.update({
        "n_walks": len(walks),
        "n_lock_reads": len(_LOCK_LOG),
        "n_streams_bitexact_287": int(sum(
            bool(w["commit_seq_sha256"]
                 == rb["r287"][(w["host"], w["seed"],
                                w["row_key"])]["commit_seq_sha256"])
            for w in walks.values())),
        "n_errs_bitexact_256": int(sum(
            bool(w["err"] == rb["dep_sub"][(w["host"], w["seed"],
                                           w["row_key"])]["err"])
            for w in walks.values())),
        "n_trace_shas_bitexact_282": int(sum(
            bool(w["trace_sha256"]
                 == rb["r282"][(w["host"], w["seed"],
                                w["row_key"])]["trace_sha256"])
            for w in walks.values()))})
    r2_gate = {"n_replays": 72, "n_finite": 72,
               "n_within_bar": n_content_ok,
               "bar": CONTENT_BAR, "majority": CONTENT_MAJORITY,
               "face_holds": content_face_holds,
               "canary": canary[0]}
    r3_gate = {"n_transports": 132, "n_finite": 132,
               "n_within_bar": n_transport_ok,
               "bar": CONTENT_BAR, "slice_seed": TRANSPORT_SLICE_SEED,
               "slice_inst": TRANSPORT_SLICE_INST,
               "canary": canary[1]}

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

    def _run_test_suite():
        cmd = [sys.executable, "-m", "tests.run_tests"]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                              text=True, timeout=560)
        tail = "\n".join(proc.stdout.strip().splitlines()[-4:])
        green = bool(proc.returncode == 0)
        return {"green": green, "returncode": int(proc.returncode),
                "tail": tail}

    ro_unchanged = bool(
        set(_sha(p) for p in READ_DEPS) == set(ro_before.values()))

    branch_text = {
        "TRANSPORT-BREAKS": (
            "the commit stream TRANSPORTS — the program's own output is "
            "a substrate-independent pattern representation in the 8th "
            "form: at least one cross-substrate replay reconstructs the "
            "pattern within the pre-named bar (the honest unblocking "
            "event — the zero-substrate star's constraint BREAKS in "
            "this form)"),
        "TRANSPORT-REFINES": (
            "the commit stream is a representation but substrate-BOUND "
            "— every cross-substrate replay fails while the "
            "same-substrate content face holds (the block DEEPENS: "
            "even the program's own output does not transport — the "
            "zero-substrate path stays blocked at 8 formalizations)"),
        "TRANSPORT-ABSENT": (
            "the commit stream is not even a same-substrate "
            "representation — the write product is not the pattern "
            "(the constraint holds at its strongest form)")}[branch]

    # ---- the deposit form ----------------------------------------------
    deposit = {
        "exp": "exp303_zero_substrate_8th",
        "claim": (
            "THE ZERO-SUBSTRATE 8TH FORMALIZATION: THE TRANSPORT FORM "
            "(batch 57, pre-registration commit 7a968de). The prior 7 "
            "formalizations quantified over the substrate's structure "
            "(the 5 static metrics, the temporal schedule, the gauge "
            "quotient); the 8th states the constraint on the PROGRAM'S "
            "OWN OUTPUT — the commit stream C = [(i, v), ...] (the "
            "write-side object exp287 deposited and exp301 carried): "
            "the stream is a substrate-independent pattern "
            "representation iff replaying it into a fresh substrate "
            "(the wiring ONLY — no spec install, no clamps, no encode, "
            "no carried state) reconstructs the pattern within the "
            "pre-named bar ERR_BAR 6.0. The region-scoped predicate "
            "zero-knob: the written set IS the commit-index set. R2 "
            "the same-substrate content face (72 replays, the "
            "majority bar 37), R3 the transport face (the 12x11 "
            "ordered pairs, the pre-named slice seed 1 / instance 0, "
            "the min(m, m') prefix), R4 the transport price (the "
            "transported error minus the destination's own replay "
            "error). The branches: TRANSPORT-BREAKS (the unblocking "
            "event) / TRANSPORT-REFINES (substrate-bound — blocked at "
            "8) / TRANSPORT-ABSENT (the stream is not the pattern)."),
        "method": {
            "battery": ("12 hosts x 3 seeds (1, 2, 3) x 2 deep "
                        "instances (r-60i0, r-60i1) at n=400 — the 72 "
                        "dormant walks (the exp302 landed walk "
                        "machinery at g=0.0/A0) + 72 same-substrate "
                        "replays + 132 transports"),
            "replay_protocol": ("a fresh GraphCollective on the read "
                                "chain's own A_ext; NO write_spec_layer, "
                                "NO clamps, NO encode window, NO carried "
                                "state (the register port exists on the "
                                "object and is NEVER touched — the "
                                "zero-substrate discipline is "
                                "protocol-level, disclosed); the "
                                "stream's values into theta AND V at "
                                "the walk order's cells in the commit "
                                "order; the walk's own settle 15.0 at "
                                "the production floor; the decode"),
            "region_predicate": ("the RMS over the written cells vs "
                                 "the row's target (the same-substrate) "
                                 "/ the destination's compiled target "
                                 "(the transport) — the scoping is the "
                                 "machinery's own: the written set IS "
                                 "the commit-index set; the full-target "
                                 "decode recorded audit-only (the "
                                 "encode's contribution to the "
                                 "un-walked zones is NOT the stream's "
                                 "to claim)"),
            "transport_order_disclosure": (
                "the destination's walk order IS the destination row's "
                "own recorded commit-index sequence (the landed "
                "frontier rule's output on the destination's own A_ext "
                "+ seed + spec — deterministic); the stream's first "
                "min(m, m') values written at the destination order's "
                "first min(m, m') cells"),
            "budget": BUDGET, "settle_h": SETTLE_H,
            "content_bar": CONTENT_BAR,
            "content_majority": CONTENT_MAJORITY},
        "inputs": {"hosts": hosts, "outliers": outliers,
                   "seeds": list(SEEDS_RUN),
                   "deep_instances": list(DEEP_INSTANCES),
                   "deep_rung": DEEP_RUNG,
                   "transport_slice": {"seed": TRANSPORT_SLICE_SEED,
                                       "inst": TRANSPORT_SLICE_INST}},
        "integrity": rb["integrity"],
        "walks": [{k: w[k] for k in w if k != "commits"}
                  for w in walks.values()],
        "replays": [{k: r[k] for k in r} for r in replays.values()],
        "transports": transports,
        "summaries": summaries,
        "branch": branch,
        "branch_discriminant": {
            "bars_pre_named_at": ("7a968de — fixed at pre-registration, "
                                  "never fit"),
            "form": ("TRANSPORT-BREAKS iff the content face holds "
                     "(>= 37/72 within the 6.0 bar) AND >= 1 of the 132 "
                     "transports within the bar; TRANSPORT-REFINES iff "
                     "the content face holds and ALL transports fail; "
                     "TRANSPORT-ABSENT otherwise"),
            "resolved": branch,
            "branch_text": branch_text},
        "g1": g1, "r2": r2_gate, "r3": r3_gate,
        "canary": canary,
        "lock_reads": len(_LOCK_LOG),
        "run_form": "in-process default (one invocation)"}
    r1_pass = bool(
        g1["n_sha_ok"] == 12 and g1["n_edges_ok"] == 12
        and g1["n_canon_ok"] == 12 and g1["h0_echo_h1"]
        and g1["n_fmax_ok"] == 12 and g1["n_nonneg_ok"] == 12
        and g1["n_rows256"] == 72 and g1["n_structure_ok"] == 36
        and g1["n_worst_eq_max"] == 36
        and g1["n_deep_targets_ok"] == 72 and g1["n_medium_shas_ok"] == 72
        and g1["n_rows282"] == 72 and g1["n_282_chain_ok"] == 72
        and g1["n_rows287"] == 72
        and g1["n_walks"] == 72 and g1["n_lock_reads"] == 72
        and g1["n_streams_bitexact_287"] == 72
        and g1["n_errs_bitexact_256"] == 72
        and g1["n_trace_shas_bitexact_282"] == 72
        and ro_unchanged)
    r2_pass = bool(r2_gate["n_replays"] == 72 and r2_gate["n_finite"] == 72
                   and canary[0]["bit_identical"]
                   and branch in ("TRANSPORT-BREAKS", "TRANSPORT-REFINES",
                                  "TRANSPORT-ABSENT"))
    r3_pass = bool(r3_gate["n_transports"] == 132
                   and r3_gate["n_finite"] == 132
                   and canary[1]["bit_identical"])
    no_wall_clock = bool(
        not _scan_wall_clock_keys(deposit)
        and not _scan_wall_clock_keys(summaries))
    set_floor(PROD_FLOOR)
    floor_exit = read_floor()
    assert floor_exit == PROD_FLOOR, "floor drift at exit"
    # ---- the exit asserts -----------------------------------------------
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
        "the register's home (collective.py) drifted after the work"
    assert _sha(EXP142_FILE) == exp142_sha_entry, \
        "exp142 was modified after the work"
    suite = _run_test_suite()
    gates = {
        "R1_the_anchors": {"pass": r1_pass, "counts": g1,
                           "source_deposits_read_only_byte_unchanged":
                               ro_unchanged,
                           "anchor_definition": (
                               "the 72 dormant walks reproduce "
                               "exp256's deposited substituted errs "
                               "BIT-EXACT 72/72 (the verified flags "
                               "72/72) + exp282's walk anchors (the "
                               "walk_end_rms + the trace shas + "
                               "err_exact 72/72) + exp287's deposited "
                               "commit_seq_sha256 BIT-EXACT 72/72 — "
                               "the streams ARE the deposited commit "
                               "sequences; the rebuild chain "
                               "sha-asserted; the floor -60.0 at "
                               "every replay's settle and at exit")},
        "R2_the_content_face": {"pass": r2_pass, "counts": r2_gate,
                                "definition": (
                                    "the 72 same-substrate replays "
                                    "deterministic (the canary "
                                    "bit-exact); the errors finite "
                                    "72/72; the face at the pre-named "
                                    "majority bar 37/72 within the "
                                    "6.0 mV ERR_BAR")},
        "R3_the_transport_face": {"pass": r3_pass, "counts": r3_gate,
                                  "definition": (
                                      "the 132 transports "
                                      "deterministic (the canary "
                                      "bit-exact); the errors finite "
                                      "132/132; the counts (m, m', "
                                      "n_written) recorded per pair; "
                                      "the face at the SAME 6.0 bar")},
        "R4_discipline": {
            "pass": bool(no_wall_clock and docstring_ok and header_ok
                         and ro_unchanged and floor_exit == PROD_FLOOR
                         and suite["green"]),
            "no_wall_clock_fields": no_wall_clock,
            "docstring_byte_unchanged_vs_7a968de": docstring_ok,
            "header_byte_unchanged_vs_7a968de": header_ok,
            "source_deposits_read_only_byte_unchanged": ro_unchanged,
            "n_source_deposits": len(READ_DEPS),
            "exp142_not_modified": True,
            "core_not_modified": True,
            "exp142_sha256": exp142_sha_entry,
            "core_sha256": port_sha_entry,
            "floor_at_entry": floor_at_entry,
            "floor_at_exit": floor_exit,
            "docstring_sha256": docstring_sha,
            "header_sha256": header_sha,
            "test_suite": suite,
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of this module in the same form "
                             "reproduces this file byte-identically")}}
    n_pass = 0
    n_refute = 0
    for name in ("R1_the_anchors", "R2_the_content_face",
                 "R3_the_transport_face", "R4_discipline"):
        n_pass += int(gates[name]["pass"])
        n_refute += int(not gates[name]["pass"])
    deposit["gates"] = gates
    verdict = (
        f"{n_pass}/4 gates R1-R4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} — {branch_text} "
        f"(the content face: {n_content_ok}/72 within the "
        f"{CONTENT_BAR} bar (the majority bar {CONTENT_MAJORITY}; the "
        f"mean region rms {summaries['same_substrate']['mean_region_rms']:.4f}"
        f", the worst {summaries['same_substrate']['worst_region_rms']:.4f}"
        f"; the full-target decode within the bar "
        f"{summaries['same_substrate']['n_full_within_bar']}/72, "
        f"audit-only — the encode's zones are NOT the stream's to "
        f"claim) | the transport face: {n_transport_ok}/132 within the "
        f"bar (the mean region rms "
        f"{summaries['transport']['mean_region_rms']:.4f}, the best "
        f"{summaries['transport']['best_region_rms']:.4f}, the worst "
        f"{summaries['transport']['worst_region_rms']:.4f}; the mean "
        f"transport price "
        f"{summaries['transport']['mean_transport_price']:+.4f} mV vs "
        f"the destination's own replay, "
        f"{summaries['transport']['n_price_negative']}/132 pairs "
        f"transporting BETTER than the destination's own program "
        f"output, audit-only) | the anchors: the streams ARE exp287's "
        f"deposited commit sequences bit-exact "
        f"{g1['n_streams_bitexact_287']}/72, the errs exp256's "
        f"{g1['n_errs_bitexact_256']}/72, the trace shas exp282's "
        f"{g1['n_trace_shas_bitexact_282']}/72 | the canary: "
        f"same {canary[0]['bit_identical']}, transport "
        f"{canary[1]['bit_identical']} | 6 deposits READ-ONLY "
        f"byte-unchanged, exp142 + the core NOT modified, floor -60.0, "
        f"the test suite green)")
    deposit["verdict"] = verdict
    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=float).encode()).hexdigest()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  R1 the anchors: {'PASS' if r1_pass else 'FAIL'} "
          f"(the 12 bases rebuilt sha-asserted {g1['n_sha_ok']}/12; the "
          f"streams == exp287's deposited commit sequences "
          f"{g1['n_streams_bitexact_287']}/72; the errs == exp256's "
          f"{g1['n_errs_bitexact_256']}/72; the trace shas == exp282's "
          f"{g1['n_trace_shas_bitexact_282']}/72; 6 deposits "
          f"READ-ONLY: {ro_unchanged})")
    print(f"  R2 the content face: {'PASS' if r2_pass else 'FAIL'} "
          f"({n_content_ok}/72 within the {CONTENT_BAR} bar | the mean "
          f"region rms "
          f"{summaries['same_substrate']['mean_region_rms']:.4f} | the "
          f"canary {canary[0]['bit_identical']})")
    print(f"  R3 the transport face: {'PASS' if r3_pass else 'FAIL'} "
          f"({n_transport_ok}/132 within the bar | the mean transport "
          f"price {summaries['transport']['mean_transport_price']:+.4f} "
          f"mV | the canary {canary[1]['bit_identical']})")
    print(f"  R4 discipline: "
          f"{'PASS' if gates['R4_discipline']['pass'] else 'FAIL'} "
          f"(no wall-clock: {no_wall_clock}; docstring+header pinned to "
          f"7a968de; exp142 + the core NOT modified; floor at exit "
          f"{floor_exit}; the test suite {suite['green']})")
    print(f"\n  BRANCH: {branch}")
    print(f"\n  GATES: {n_pass}/4 ({n_pass} PASS / {n_refute} REFUTE)")
    print(f"  deposited {OUT}")
    return deposit


if __name__ == "__main__":
    main()
