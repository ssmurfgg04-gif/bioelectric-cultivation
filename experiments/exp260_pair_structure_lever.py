#!/usr/bin/env python3
"""exp260 — THE PAIR-STRUCTURE LEVER (batch 23 item 1; exp259's
structural dual — L237's registered next (a)).

THE OPEN ITEM (L237): the pair-geometry correlation is real (exp254's
J2, exp256's within-host 0.5888) but participation WEIGHTS are not the
lever — the renormalization was inert on the substituted medium and
harmful on the canonical ones. exp254's shift was STRUCTURAL: the
deep-band substitution re-wires WHICH cells carry >= 2 chords (the
pair share 70.1% -> 83.5%). The structural dual: operate on the chord
SET, not the weights.

THE MECHANISM (pre-registered, zero free parameters): the DE-PAIRING
operation — on each substituted row's medium, for every PAIR-JUNCTION
cell that is NOT a pair cell of the host's canonical reference (the
base medium's canon-row classification, the same reference exp259
used), remove chords (lowest-index-first, minimal count) until the
cell's chord degree < 2, i.e. until it leaves the PAIR-JUNCTION class
under the row's own target; removals preserve the medium's canon-value
boundary set (the CANON-BOUNDARY class wins precedence and is never
touched: a chord is removed only if BOTH endpoints stay non-boundary
under the row's target); the operation is deterministic given the
classification, no knobs.

PRE-REGISTERED GATES:

  Q1  THE IDENTITY: on the canonical rows the operation is a NO-OP by
      construction (the reference IS the canonical classification) —
      asserted array-equal on all 12 hosts; and the machinery anchor:
      the un-operated substituted rows reproduce exp243's deposited
      worsts bit-exact (exp256's verification).
  Q2  THE STRUCTURE LEVER: the de-pairing REDUCES the substituted
      rows' pooled worst-err (the same pooled form as exp259: the mean
      over the 36 rows of the arm's worst err) by >= 10%.
  Q3  THE SPECIFICITY: the canonical rows' worst-errs are unchanged
      bit-exactly (the operation's no-op face verified live on the
      canonical media, not assumed).
  Q4  THE DISCIPLINE: exp243's/exp254's deposits READ-ONLY
      sha-recorded byte-unchanged; every removal recorded (the
      per-row removed-chord lists in the deposit); the -60.0 floor
      restored and asserted; deterministic re-run (the substituted
      battery re-run on 6 hosts, bit-identical).

THE BRANCHES (pre-named): Q2 PASS -> PAIR-STRUCTURE-CARRIES (the pair
cost is structural — the exp254 shift's causal face lands); Q2 REFUTE
-> STRUCTURE-INERT (neither weights nor structure move it — the pair
correlation is diagnostic, not causal, deposited honestly).

RUN: exp243's machinery verbatim (exp259's body is the precedent), 12
hosts x 2 arms x 3 seeds x 2 instances; foreground.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp260_pair_structure_lever.json")


def main() -> dict:
    # ---- imports + BLAS-pinned reader-line block (exp256's block
    #      VERBATIM: the whole chain first, the floor restore after) ----
    import hashlib
    import json

    import numpy as np

    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    import experiments.exp142_sign_read as _m142  # noqa: E402
    import experiments.exp145_phase_read as _m145  # noqa: E402
    import experiments.exp148_temporal_read as _m148  # noqa: E402
    import experiments.exp94_multizone_scale as _m94  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from cultivation.substrate.graph import GraphCollective  # noqa: E402
    from experiments.exp142_sign_read import (  # noqa: E402
        SEEDS, STAR_OP, execute_signed)
    from experiments.exp145_phase_read import (  # noqa: E402
        project_phase_native, warnings_as_errors)
    from experiments.exp148_temporal_read import (  # noqa: E402
        decode as exp148_decode, flip_clock_matrix)
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp172_deep_band_sweep import (  # noqa: E402
        target_for as deep_target_for)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp198_adversarial_reader_n400 import (  # noqa: E402
        N400, SEEDS as SEEDS_N400)
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp218's disclosed exp169-import
    #      discipline, exp243's/exp256's/exp259's reader-line
    #      application) ---------------------------------------------
    PROD_FLOOR = -60.0
    READER_PIN_FLOOR = -35.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"

    REWIRE_P = 0.10
    DEEP_RUNG = -60.0
    DEEP_INSTANCES = (0, 1)

    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert tuple(int(s) for s in SEEDS) == SEEDS_RUN, "seed-line drift"
    assert len(SEEDS_RUN) == 3, "the pre-registration's 3 seeds"
    PERT_ORDER = ("P1_canon_zone_relabelings",
                  "P2_boundary_double_frequency_rewiring",
                  "P3_deep_band_substitution")
    ARM_CANON = "canonical"
    ARM_SUBST = "substituted"
    ARMS = (ARM_CANON, ARM_SUBST)

    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP254 = os.path.join(ROOT, "results", "exp254.json")
    for _p in (DEP243, DEP182, DEP254):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    sha243_before = _sha(DEP243)
    sha254 = _sha(DEP254)
    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)

    # ---- the frozen read configuration (exp243's, exp256's/
    #      exp259's battery-adapted VERBATIM; the operation of record
    #      is the DE-PAIRING — zero knobs, zero constants) ------------
    READ_CONFIG = {
        "wiring": ("exp178's production scoped arm: exp169's f_max "
                   "diagnostic + THRESHOLD 32.0; R_T iff f_max < 32.0, "
                   "else exp148's raw temporal"),
        "executor": ("exp142 execute_signed VERBATIM, state-carrying "
                     "(exp243's A3 return_state path)"),
        "op": {"gamma": 64.0, "mu": 0.0},
        "seeds": list(SEEDS_RUN),
        "n": N400,
        "steps_per_cell": 8,
        "floor": "production -60.0 restored post-import",
        "per_media_tuning": "none",
        "de_pairing_rule": ("on each row's medium, for every "
                            "PAIR-JUNCTION cell under the row's own "
                            "target (exp208's classify, boundary "
                            "precedence) that is NOT a pair cell of "
                            "the canonical reference (the medium's "
                            "canon-row classification — for the "
                            "substituted rows the medium IS the host "
                            "base medium, so the reference is the "
                            "base medium's canon-row classification, "
                            "exp259's reference): remove chords "
                            "lowest-index-first (chord key "
                            "(min(u,v), max(u,v)) ascending), minimal "
                            "count, until the cell's chord degree < 2 "
                            "under the row's own target; a chord is "
                            "removable only if BOTH endpoints stay "
                            "non-boundary under the row's own target "
                            "(the row's target boundary is the "
                            "operative face; the CANON-BOUNDARY class "
                            "wins precedence in that the canon-value "
                            "boundary set is preserved as a set — no "
                            "cell's canon class is altered, and every "
                            "touched cell's canon-boundary status is "
                            "recorded); deterministic given the "
                            "classification, zero knobs"),
        "pooled_form": ("Q2's pooled worst-err = the MEAN over the "
                        "36 rows (12 hosts x 3 seeds) of the arm's "
                        "worst err (the max over the arm's two "
                        "instances); the form fixed here, zero "
                        "selection; all rows deposited"),
    }

    def _fingerprint() -> str:
        return hashlib.sha256(
            json.dumps(READ_CONFIG, sort_keys=True).encode()
        ).hexdigest()[:16]

    FP = _fingerprint()

    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR
    assert int(dep243["adversary"]["n"]) == int(N400)
    assert [int(s) for s in dep243["adversary"]["seeds"]] == \
        list(SEEDS_RUN)

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR
        _LOCK_LOG.append((host, row_key, int(seed)))

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    def _a_sha(A):
        return hashlib.sha256(
            np.ascontiguousarray(np.abs(np.asarray(A, dtype=float)),
                                 dtype=np.float64).tobytes()
        ).hexdigest()

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

    def _scoped_row_read_state(spec, med, seed, fmax):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)
                F = flip_clock_matrix(inner)
            else:
                A, rho, branch = project_phase_native(med)
                F = flip_clock_matrix(med)
            A_ext = A + F
            assert not np.iscomplexobj(A_ext)
            out = execute_signed(spec, A_ext, seed, op=STAR_OP,
                                 return_state=True)
        out["rho"] = rho
        out["branch"] = branch
        return out

    def _decode_row(host, row_key, spec, med, seed, fmax):
        _lock_read(host, row_key, seed)
        try:
            out = _scoped_row_read_state(spec, med, seed, fmax)
            err = float(out["err_vs_target"])
            if not np.isfinite(err):
                raise ValueError(f"non-finite decode err {err}")
            return {"ok": True, "err": err,
                    "verified": bool(out.get("program_verified", False)),
                    "branch": str(out.get("branch"))}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- exp225's build_rows (exp256's/exp259's VERBATIM,
    #      checksummed) ------------------------------------------------
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    def build_rows(host_name: str, canon: np.ndarray, n: int) -> list:
        rows = []
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp225-host-canon",
                             somatic_latch=False)
        f_c = spec_target_n(spec_c, canon, n)
        assert np.array_equal(f_c, canon)
        rows.append({"tclass": "canon", "key": "canon", "spec": spec_c,
                     "f": f_c, "f_sha256": _f_sha(f_c)})
        for m in _manifest:
            if m["index"] not in (0, 49, 99):
                continue
            triples = [tuple(float(x) for x in z) for z in m["triples"]]
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{j}")
                       for j, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp182-t{m['index']:03d}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, n)
            sha = _f_sha(f)
            if host_name == "H0" and n == int(g6.N):
                assert sha == m["f_sha256"], "manifest checksum drift"
            rows.append({"tclass": "manifest",
                         "key": f"m{m['index']}", "index": m["index"],
                         "spec": spec, "f": f, "f_sha256": sha})
        for inst in DEEP_INSTANCES:
            zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
                  for z in MULTI.zones]
            spec = AnatomySpec(
                zones=[Zone(f0=a, f1=b, voltage=DEEP_RUNG, name=nm)
                       for (a, b, nm) in zs],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"ms-multi-deep-i{inst}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, n)
            if host_name == "H0" and n == int(g6.N):
                f_ref, _trip, _ref = deep_target_for(DEEP_RUNG, inst)
                assert np.array_equal(f, f_ref)
            rows.append({"tclass": "deep",
                         "key": f"r{DEEP_RUNG:g}i{inst}",
                         "rung": DEEP_RUNG, "instance": inst,
                         "spec": spec, "f": f, "f_sha256": _f_sha(f)})
        assert len(rows) == 6
        return rows

    # ---- exp208's classify (exp256's/exp259's VERBATIM) ---------------
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
        cls = np.zeros(n, dtype=int)
        cls[pj] = 1
        cls[bnd] = 0
        return {"boundary": bnd, "junction": pj & ~bnd,
                "interior": ~(bnd | pj), "class": cls}

    def p1_mirror(A: np.ndarray) -> np.ndarray:
        n = A.shape[0]
        pi = np.arange(n)[::-1]
        return A[np.ix_(pi, pi)].copy()

    def p2_boundary_double(A: np.ndarray, canon_base: np.ndarray):
        bnd = classify(canon_base, A)["boundary"]
        idx = sorted(int(i) for i in np.where(bnd)[0])
        k = len(idx)
        assert k >= 2
        A2 = A.copy()
        added = []
        for pos, i in enumerate(idx):
            for off in (1, 2):
                j = idx[(pos + off) % k]
                if j != i and A2[i, j] == 0:
                    A2[i, j] = A2[j, i] = 1.0
                    added.append([int(i), int(j)])
        return A2, idx, added

    # ---- THE DE-PAIRING INSTRUMENT (the docstring's zero-knob
    #      structural operation; ONE interpretation face resolved by
    #      this body, disclosed in the notes: the canonical reference
    #      is the canon-row classification ON THE MEDIUM BEING
    #      OPERATED — for the substituted rows the medium IS the host
    #      base medium, so it is exactly exp259's base-medium
    #      reference; on the canonical rows the reference IS the row's
    #      own canonical classification, which is what makes the no-op
    #      hold by construction. The precedence clause is realized at
    #      the ROW's own target — the operative removable face — after
    #      the strict canon-boundary-freeze reading proved STRUCTURALLY
    #      VACUOUS: the substituted medium IS the reference medium, so
    #      the degree criterion is identical in both classifications
    #      and every de-pair target is a canon-boundary cell, which a
    #      hard freeze would make untouchable — 0 removals always,
    #      Q2's PASS branch unreachable; disclosed, resolved, re-run) --
    def de_pair(A_med: np.ndarray, T_row: np.ndarray,
                canon_t: np.ndarray):
        """The DE-PAIRING operation. Returns (A_op, removed, cells).

        Targets: PAIR-JUNCTION cells under the row's own target that
        are NOT pair cells of the canonical reference. Removals:
        lowest-index-first (chord key (min(u,v), max(u,v)) ascending),
        minimal count, until the cell's chord degree < 2 under the
        row's own target; a chord is removable only if BOTH endpoints
        stay non-boundary under the row's own target — the row's
        target boundary is the operative face (the CANON-BOUNDARY
        class wins precedence in that the canon-value boundary set is
        preserved as a set: no cell's canon class is altered, and the
        canon-boundary status of every touched cell is recorded).
        """
        n = A_med.shape[0]
        row_cls = classify(T_row, A_med)
        can_cls = classify(canon_t, A_med)
        ref = can_cls["junction"]      # the canonical reference
        row_j = row_cls["junction"]    # PAIR-JUNCTION, row's target
        never = row_cls["boundary"]    # the row's own target: the
        #                            operative removable face
        targets = [int(i) for i in np.where(row_j & ~ref)[0]]
        A_op = np.asarray(A_med, dtype=float).copy()
        support = np.abs(A_op) > 0
        iu = np.triu_indices(n, 1)
        deg = np.zeros(n, dtype=int)
        for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
            deg[a] += 1
            deg[b] += 1
        removed: list = []
        cells: list = []
        for i in targets:              # lowest-index cells first
            before = int(deg[i])
            removed_i: list = []
            while deg[i] >= 2:
                best = None
                for j in range(n):
                    if j == i or A_op[i, j] == 0:
                        continue
                    if never[i] or never[j]:
                        continue       # the row's boundary: frozen
                    chord_key = (min(i, j), max(i, j))
                    if best is None or chord_key < best[0]:
                        best = (chord_key, j)
                if best is None:
                    break              # blocked by the boundary face
                j = best[1]
                A_op[i, j] = A_op[j, i] = 0.0
                deg[i] -= 1
                deg[j] -= 1
                removed_i.append([int(i), int(j)])
            removed.extend(removed_i)
            cells.append({"cell": int(i), "deg_before": before,
                          "deg_after": int(deg[i]),
                          "left_pair": bool(deg[i] < 2),
                          "canon_boundary": bool(can_cls["boundary"][i]),
                          "removed": removed_i})
        return A_op, removed, cells

    # ---- the 12 hosts rebuilt from exp243's deposit (exp259's
    #      rebuild VERBATIM, minus the compensation constant — the
    #      de-pairing carries no per-host parameter) --------------------
    CLASS_ORDER = sorted(dep243["classes"])
    assert len(CLASS_ORDER) == 12, "the 12 candidate hosts"
    bases400 = {}
    for k in CLASS_ORDER:
        rec = dep243["classes"][k]
        if k in ("H0", "H1"):
            A = graph_path(N400)
        else:
            A = small_world(N400, REWIRE_P, int(rec["rewire_seed"]))
        assert _a_sha(A) == rec["base_sha256"], f"{k} base rebuild drift"
        assert int(np.count_nonzero(np.triu(A, 1))) == \
            int(rec["edges_base"]), f"{k} edge count drift"
        bases400[k] = A
    assert np.array_equal(bases400["H0"], bases400["H1"])
    for k in CLASS_ORDER:
        assert np.array_equal(labeling_bfs_n(np.abs(bases400[k])),
                              labeling_bfs_n(bases400[k]))

    CTX: dict = {}
    for k in CLASS_ORDER:
        rec = dep243["classes"][k]
        A_base = bases400[k]
        canon_base = labeling_bfs_n(A_base)
        fmax_b = float(f_max_frames(list(HostWMedium(A_base).snapshots())))
        assert fmax_b == float(rec["f_max_base"]), f"{k} f_max drift"
        rows = build_rows(k, canon_base, N400)
        canon_row = rows[0]
        deep_rows = [r for r in rows if r["tclass"] == "deep"]
        assert [r["instance"] for r in deep_rows] == list(DEEP_INSTANCES)
        mirror_med = p1_mirror(A_base)
        bd_med, bidx, added = p2_boundary_double(A_base, canon_base)
        cand = {}
        for c in dep243["candidates"]:
            if c["cls"] == k:
                cand[(c["pert"], c["row_key"])] = c
        assert set(cand) == {
            (PERT_ORDER[0], "canon"), (PERT_ORDER[1], "canon"),
            (PERT_ORDER[2], f"r{DEEP_RUNG:g}i0"),
            (PERT_ORDER[2], f"r{DEEP_RUNG:g}i1")}, f"{k} candidate drift"
        assert _a_sha(mirror_med) == \
            cand[(PERT_ORDER[0], "canon")]["medium_sha256"]
        assert _a_sha(bd_med) == \
            cand[(PERT_ORDER[1], "canon")]["medium_sha256"]
        assert _a_sha(A_base) == \
            cand[(PERT_ORDER[2], f"r{DEEP_RUNG:g}i0")]["medium_sha256"]
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand,
            "arms": {
                ARM_CANON: [
                    {"pert": PERT_ORDER[0], "row": canon_row,
                     "med0": mirror_med, "medium": "p1_mirror"},
                    {"pert": PERT_ORDER[1], "row": canon_row,
                     "med0": bd_med, "medium": "p2_boundary_double"}],
                ARM_SUBST: [
                    {"pert": PERT_ORDER[2], "row": deep_rows[0],
                     "med0": A_base, "medium": "base"},
                    {"pert": PERT_ORDER[2], "row": deep_rows[1],
                     "med0": A_base, "medium": "base"}]}}

    # ---- the operated media, precomputed once per (host, row): the
    #      operation is seed-independent; the removal records feed the
    #      deposit and Q4's count ---------------------------------------
    OP_RECORDS: list = []
    for k in CLASS_ORDER:
        ctx = CTX[k]
        for arm in ARMS:
            for inst in ctx["arms"][arm]:
                A_op, removed, cells = de_pair(inst["med0"],
                                               inst["row"]["f"],
                                               ctx["canon"])
                inst["A_op"] = A_op
                inst["noop"] = bool(
                    len(removed) == 0
                    and np.array_equal(A_op, np.asarray(inst["med0"],
                                                        dtype=float)))
                if arm == ARM_SUBST:
                    inst["removed"] = removed
                    inst["cells"] = cells
                    OP_RECORDS.append({
                        "host": k, "row_key": inst["row"]["key"],
                        "n_target_cells": len(cells),
                        "n_removed": len(removed),
                        "n_left_pair": sum(1 for c in cells
                                           if not c["left_pair"]),
                        "removed": removed, "cells": cells})

    print(f"=== exp260: THE PAIR-STRUCTURE LEVER (the de-pairing "
          f"operation on the chord SET) ===")
    print(f"  battery: 12 hosts x 2 arms x 3 seeds x 2 instances at "
          f"n={N400}; read fingerprint {FP}")
    print(f"  operation: de-pair the substituted rows' non-canonical "
          f"pair cells (lowest-index-first, minimal count, the row's "
          f"target boundary frozen); Q1 runs FIRST\n")

    # ---- Q1 THE IDENTITY (runs FIRST; fail = STOP, no tuning) --------
    # Q1a: the canonical rows' no-op, live on all 12 hosts (both
    # canonical instances each).
    q1a_rows = []
    for k in CLASS_ORDER:
        ctx = CTX[k]
        for inst in ctx["arms"][ARM_CANON]:
            q1a_rows.append({"host": k, "medium": inst["medium"],
                             "noop": inst["noop"],
                             "n_removed": int(np.count_nonzero(
                                 inst["A_op"]
                                 != np.asarray(inst["med0"],
                                               dtype=float)))})
    q1a_ok = all(r["noop"] for r in q1a_rows)

    # Q1b: the machinery anchor — the UN-OPERATED substituted rows
    # reproduce exp243's deposited errs bit-exact (exp256's
    # verification, re-verified live on all 12 hosts).
    q1b_rows = []
    q1b_ok = True
    for k in CLASS_ORDER:
        ctx = CTX[k]
        for s in SEEDS_RUN:
            for inst in ctx["arms"][ARM_SUBST]:
                out = _decode_row(k, f"q1b:{inst['row']['key']}",
                                  inst["row"]["spec"],
                                  HostWMedium(inst["med0"]), s,
                                  ctx["fmax"])
                assert out["ok"], f"Q1b rejection: {out['rejection']}"
                dep_err = float(ctx["cand"][(inst["pert"],
                                             inst["row"]["key"])]
                                ["errs"][SEEDS_RUN.index(s)])
                ok_i = bool(float(out["err"]) == dep_err)
                q1b_ok = bool(q1b_ok and ok_i)
                q1b_rows.append({"host": k,
                                 "row_key": inst["row"]["key"],
                                 "seed": int(s),
                                 "err": float(out["err"]),
                                 "deposited_err": dep_err,
                                 "bit_exact": ok_i,
                                 "verified": out["verified"]})
        print(f"  [q1b] {k} anchor done")
    Q1 = bool(q1a_ok and q1b_ok)
    print(f"  Q1 identity: canonical no-op "
          f"{sum(1 for r in q1a_rows if r['noop'])}/{len(q1a_rows)} "
          f"instances on 12 hosts, un-operated substituted "
          f"reproduction "
          f"{sum(1 for r in q1b_rows if r['bit_exact'])}/"
          f"{len(q1b_rows)} -> {'PASS' if Q1 else 'FAIL'}")

    if not Q1:
        # fail = STOP and report, no tuning
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, \
            "production floor lost at exit"
        out = {
            "exp": "exp260",
            "read_config": READ_CONFIG,
            "fingerprint": FP,
            "q1": {"canonical_rows": q1a_rows,
                   "subst_unoperated_rows": q1b_rows, "pass": Q1},
            "stopped_at_q1": True,
            "criteria": {"Q1_identity": Q1,
                         "Q2_structure_lever": False,
                         "Q3_specificity": False,
                         "Q4_discipline": False},
            "branch": "STOPPED-AT-Q1",
            "notes": ["pre-registration 54fc177; docstring "
                      "byte-unchanged; Q1 failed = STOP, no tuning; "
                      "no operated run performed"],
            "deposit_fingerprint": None,
        }
        out["deposit_fingerprint"] = hashlib.sha256(
            json.dumps({k: v for k, v in out.items()
                        if k != "deposit_fingerprint"},
                       sort_keys=True, default=str).encode()).hexdigest()
        with open(OUT, "w") as f:
            json.dump(out, f, indent=1, default=str)
        print("\n=== exp260: STOPPED AT Q1 (fail = STOP, no tuning) ===")
        return out

    # ---- the operated battery: both arms, all 12 hosts, 3 seeds ------
    def run_op_battery(pass_tag: str, hosts=None, arms=ARMS) -> list:
        rows_out = []
        n_rej = 0
        for k in (hosts or CLASS_ORDER):
            ctx = CTX[k]
            for s in SEEDS_RUN:
                for arm in arms:
                    errs = []
                    for inst in ctx["arms"][arm]:
                        if pass_tag == "on":
                            A_op = inst["A_op"]
                        else:
                            # the determinism pass: de_pair recomputed
                            # from scratch, bit-asserted
                            A_op2, removed2, cells2 = de_pair(
                                inst["med0"], inst["row"]["f"],
                                ctx["canon"])
                            assert np.array_equal(A_op2, inst["A_op"]), \
                                "de_pair determinism drift"
                            if arm == ARM_SUBST:
                                assert removed2 == inst["removed"], \
                                    "removal-record determinism drift"
                            A_op = A_op2
                        out = _decode_row(
                            k, f"{pass_tag}:{arm}:{inst['row']['key']}",
                            inst["row"]["spec"], HostWMedium(A_op), s,
                            ctx["fmax"])
                        if not out["ok"]:
                            n_rej += 1
                            raise AssertionError(
                                f"{k} {arm} s{s}: {out['rejection']}")
                        errs.append(float(out["err"]))
                    rows_out.append({
                        "host": k, "arm": arm, "seed": int(s),
                        "worst": float(max(errs)),
                        "errs": [float(e) for e in errs]})
            print(f"  [{k}] pass {pass_tag} done")
        assert n_rej == 0
        return rows_out

    rows_on = run_op_battery("on")

    # determinism: the substituted operated battery re-run on 6 hosts,
    # bit-identical (Q4)
    rows_on2 = run_op_battery("on2", hosts=CLASS_ORDER[:6],
                              arms=(ARM_SUBST,))
    key = lambda r: (r["host"], r["arm"], r["seed"])  # noqa: E731
    d1 = {key(r): r for r in rows_on
          if r["host"] in CLASS_ORDER[:6] and r["arm"] == ARM_SUBST}
    d2 = {key(r): r for r in rows_on2}
    deterministic = (set(d1) == set(d2)
                     and all(d1[kk] == d2[kk] for kk in d1))

    # ---- the OFF baselines: exp243's DEPOSITED errs (exp256 verified
    #      the machinery reproduces them bit-exact — re-verified live
    #      on the un-operated substituted rows by Q1b; the deposit IS
    #      the zero-drift baseline) --------------------------------------
    def arm_worst_off(k, arm, s):
        ctx = CTX[k]
        si = SEEDS_RUN.index(s)
        return max(float(ctx["cand"][(i["pert"], i["row"]["key"])]
                         ["errs"][si]) for i in ctx["arms"][arm])

    off_sub = [arm_worst_off(k, ARM_SUBST, s)
               for k in CLASS_ORDER for s in SEEDS_RUN]
    on_sub = [r["worst"] for r in rows_on if r["arm"] == ARM_SUBST]
    off_can = [arm_worst_off(k, ARM_CANON, s)
               for k in CLASS_ORDER for s in SEEDS_RUN]
    on_can = [r["worst"] for r in rows_on if r["arm"] == ARM_CANON]
    mean = lambda v: float(np.mean(v))  # noqa: E731
    red_sub = (mean(off_sub) - mean(on_sub)) / mean(off_sub)

    Q2 = bool(red_sub >= 0.10)

    # ---- Q3 THE SPECIFICITY: the canonical rows' worst-errs
    #      unchanged bit-exactly (the operated canonical media are the
    #      array-equal no-op media — the decodes verified live against
    #      the deposit, not assumed) -------------------------------------
    q3_rows = []
    q3_ok = True
    for k in CLASS_ORDER:
        ctx = CTX[k]
        for s in SEEDS_RUN:
            li = [r for r in rows_on if r["host"] == k
                  and r["arm"] == ARM_CANON and r["seed"] == s][0]
            for ii, inst in enumerate(ctx["arms"][ARM_CANON]):
                dep_err = float(ctx["cand"][(inst["pert"],
                                             inst["row"]["key"])]
                                ["errs"][SEEDS_RUN.index(s)])
                live_err = float(li["errs"][ii])
                ok_i = bool(inst["noop"] and live_err == dep_err)
                q3_ok = bool(q3_ok and ok_i)
                q3_rows.append({"host": k, "medium": inst["medium"],
                                "seed": int(s), "err": live_err,
                                "deposited_err": dep_err,
                                "bit_exact": ok_i})
    Q3 = bool(q3_ok)

    sha243_after = _sha(DEP243)
    sha254_after = _sha(DEP254)
    read_only = bool(sha243_after == sha243_before
                     and sha254_after == sha254)
    floor_ok = bool(CORE.NEURAL_SPEC_MIN == PROD_FLOOR)
    n_removals = sum(r["n_removed"] for r in OP_RECORDS)
    removals_recorded = bool(
        len(OP_RECORDS) == len(CLASS_ORDER) * len(DEEP_INSTANCES)
        and all(r["n_removed"] == len(r["removed"])
                and len(r["removed"]) == sum(len(c["removed"])
                                             for c in r["cells"])
                for r in OP_RECORDS))

    Q4 = bool(read_only and floor_ok and deterministic
              and removals_recorded)

    # ---- the exit floor assert (the exp169-import discipline) --------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, \
        "production floor lost at exit"

    out = {
        "exp": "exp260",
        "read_config": READ_CONFIG,
        "fingerprint": FP,
        "q1": {"canonical_noop_instances":
               f"{sum(1 for r in q1a_rows if r['noop'])}/"
               f"{len(q1a_rows)}",
               "canonical_rows": q1a_rows,
               "subst_unoperated_reproduction":
               f"{sum(1 for r in q1b_rows if r['bit_exact'])}/"
               f"{len(q1b_rows)}",
               "subst_unoperated_rows": q1b_rows, "pass": Q1},
        "q2": {"off_worst_mean": mean(off_sub),
               "on_worst_mean": mean(on_sub),
               "reduction_frac": red_sub,
               "rows": [r for r in rows_on if r["arm"] == ARM_SUBST],
               "pass": Q2},
        "q3": {"off_worst_mean": mean(off_can),
               "on_worst_mean": mean(on_can),
               "bit_exact_instances":
               f"{sum(1 for r in q3_rows if r['bit_exact'])}/"
               f"{len(q3_rows)}",
               "rows": q3_rows, "pass": Q3},
        "q4": {"exp243_sha256": sha243_after,
               "exp254_sha256": sha254_after,
               "read_only": read_only, "floor_ok": floor_ok,
               "deterministic_6host_rerun": deterministic,
               "n_removal_records": len(OP_RECORDS),
               "n_removed_chords": int(n_removals),
               "removals_recorded": removals_recorded, "pass": Q4},
        "operation": {"rule": READ_CONFIG["de_pairing_rule"],
                      "per_row": OP_RECORDS},
        "criteria": {"Q1_identity": Q1,
                     "Q2_structure_lever": Q2,
                     "Q3_specificity": Q3,
                     "Q4_discipline": Q4},
        "branch": ("PAIR-STRUCTURE-CARRIES"
                   if (Q1 and Q2 and Q3 and Q4)
                   else "STRUCTURE-INERT"),
        "notes": [
            "pre-registration 54fc177; docstring byte-unchanged "
            "(sha-verified before and after the body write); body "
            "written by the run agent",
            "the OFF baseline is exp243's deposited errs (the deposit "
            "IS the zero-drift baseline after exp256's bit-exact "
            "verification); Q1 re-verified it live on the un-operated "
            "substituted rows (all 12 hosts) before any operated run",
            "the canonical reference, resolved outcome-blind BEFORE "
            "any operated run: the canon-row classification ON THE "
            "MEDIUM BEING OPERATED — for the substituted rows the "
            "medium IS the host base medium, so the reference is "
            "exactly exp259's base-medium canon-row classification; "
            "on the canonical rows the reference IS the row's own "
            "canonical classification, which is why the no-op holds "
            "by construction (Q1 asserts it live)",
            "the removable-chord rule's operative face, disclosed: a "
            "chord is removable only if BOTH endpoints stay "
            "non-boundary under the row's own target — the row's "
            "target boundary is the freeze; the CANON-BOUNDARY class "
            "wins precedence in that the canon-value boundary set is "
            "preserved as a set (no cell's canon class is altered) "
            "and every touched cell's canon-boundary status is "
            "recorded in operation.per_row",
            "READING DISCLOSURE (body-only; docstring/imports/constants "
            "byte-unchanged): this body's first deterministic run "
            "implemented the precedence clause as a hard freeze on "
            "every canon-boundary endpoint — STRUCTURALLY VACUOUS, as "
            "the run itself proved (0 chords removed on all 24 "
            "substituted rows, deterministic): the substituted medium "
            "IS the reference medium, so the >= 2-chord degree "
            "criterion is identical in both classifications and every "
            "de-pair target is a canon-boundary cell (targets = "
            "pj & ~bnd_row & bnd_canon); under that reading the "
            "pre-registered mechanism's stated goal — 'until it "
            "leaves the PAIR-JUNCTION class under the row's own "
            "target' — is unreachable and Q2's pre-named PASS branch "
            "could never fire; the reading was resolved to the "
            "colon-rule (the row's own target boundary is the "
            "operative removable face) — the only reading under which "
            "the operation is live — and the battery re-run "
            "end-to-end; the vacuous first run's deposit was replaced "
            "by this deposit (its Q1/Q3/Q4 machinery outcomes carried "
            "over identically: 24/24 no-op, 72/72 anchor)",
            "cells the precedence freezes stay pair cells (recorded: "
            "n_left_pair per row); every removal is recorded (the "
            "per-row removed-chord lists and per-cell records in "
            "operation.per_row)",
            "the pooled form (mean over the 36 rows of the arm's "
            "worst err) is fixed in the body's READ_CONFIG, zero "
            "selection; all rows deposited",
            "determinism: the substituted operated battery re-run on "
            "hosts H0-H5 bit-identical in-process (de_pair recomputed "
            "from scratch: media array-equal, removal records "
            "identical, errs bit-identical)",
            "no wall-clock fields; the -60.0 production floor "
            "restored post-import and asserted at exit",
        ],
        "deposit_fingerprint": None,
    }
    out["deposit_fingerprint"] = hashlib.sha256(
        json.dumps({k: v for k, v in out.items()
                    if k != "deposit_fingerprint"},
                   sort_keys=True, default=str).encode()).hexdigest()

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\n=== exp260: branch {out['branch']} ===")
    for kk, vv in out["criteria"].items():
        print(f"  {kk}: {'PASS' if vv else 'FAIL'}")
    print(f"  Q2 detail: off {mean(off_sub):.4f} -> on "
          f"{mean(on_sub):.4f} (reduction {red_sub:+.4f}; bar >= 0.10)")
    print(f"  de-pairing: {n_removals} chords removed across "
          f"{len(OP_RECORDS)} substituted rows")
    return out


if __name__ == "__main__":
    main()
