#!/usr/bin/env python3
"""exp267 — THE READ-STAGE ATTRIBUTION (batch 26; L244's registered
next — the arm contrast localized INSIDE the read stack).

THE OPEN ITEM (the two-line convergence, L243+L244): the residual's
rank variance is 75.7% arm (exp262), the arm share is NOT the
target's geometry (exp265) and NOT closable by deposit-level
structural terms (exp266) — it is the READ's own response to the
deep-band substitution. Which STAGE of the read stack carries it?

THE INSTRUMENT (pre-registered, zero-knob; the exp208
c6-tail-ablation mold applied to the read's stages): re-run the
substituted rows' decodes (exp256's 12 hosts x 3 seeds x 2 deep
instances = 72 rows) with each read stage's output held at its
CANONICAL-row value in turn — the canonical value is the same
stage's output on the SAME host's canon row (the P1/P2 battery's
row), same seed. Four arms:

  S0  the baseline (no hold) — the substituted rows as exp256 ran
      them (the reproduction anchor: the errs must reproduce
      exp243's/exp256's deposited values bit-exact);
  S1  the PROJECTION held (PN1/PN2 phase projection computed on the
      canon row's medium, applied to the substituted decode);
  S2  the FLIP-CLOCK held (TC1's F matrix from the canon row);
  S3  the EXECUTOR held (exp142's execute_signed run on the canon
      row's A_ext, the substituted row's target swapped in at the
      error read — the walk itself canonicalized).

The arm contrast's carrier = the stage whose canonicalization
CHANGES the substituted rows' errs the most (the rank-variance share
of the (S0 - Sk) delta across rows, the exp229/exp262 convention on
the delta ranks).

PRE-REGISTERED GATES:

  R1  THE REPRODUCTION: S0 reproduces the deposited errs bit-exact
      (72/72; the machinery anchor).
  R2  THE ATTRIBUTION: the three stage deltas' rank-variance shares
      reported; the gate: ONE stage's share >= 0.5 (the carrier is
      single-stage — the residual localizes inside the stack).
  R3  THE HONESTY CLAUSE: if no stage reaches 0.5, the contrast is
      DISTRIBUTED (the read's stages interact — deposited honestly,
      the shares named).
  R4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the read stack's production
      fingerprint asserted pre/post (exp160's READ_CONFIG); the
      -60.0 floor restored and asserted at exit (the exp169 import
      chain pins -35.0 — the explicit restore); deterministic
      (S0/S1/S2/S3 re-run on 6 hosts, bit-identical); no
      wall-clock fields.

THE BRANCHES (pre-named): STAGE-CARRIES (R2) / DISTRIBUTED (R3).

RUN: 4 arms x 72 rows at n=400 (the scoped read ~1.3 s/row) —
foreground segments or a runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp267_read_stage_attribution.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates R1-R4 below evaluated exactly once,
    #      pre-registration commit aa0acdb) ==================================
    import argparse
    import hashlib
    import json
    import time
    from itertools import permutations

    import numpy as np
    from scipy.stats import rankdata

    # ---- the docstring gate, FIRST in every process (segments, merge):
    #      the docstring is the aa0acdb pre-registration, byte-for-byte;
    #      fail = STOP before anything runs (the hard rule; the sha is
    #      of the RAW module __doc__ — the exact literal, trailing
    #      newline included, as imported) ---------------
    EXPECTED_DOCSTRING_SHA256 = (
        "2de8f5267babc391ba6201ddcac24aa06cd87fa36fef5a7404e0b4971aaa56fc")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    assert docstring_ok, "docstring drifted from aa0acdb"

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["s0", "s1", "s2", "s3"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    if args.seg is None and args.merge is None:
        ap.error("one of --seg / --merge is required (the checkpoint "
                 "split: one foreground segment per arm, merge at the "
                 "end — the exp263/exp261 pattern; no setsid/nohup)")

    # body-only plumbing repair (disclosed): json/numpy/scipy/argparse
    # are imported HERE, in-body, before any use (the pre-registered
    # header carries only os/sys; the BLAS pins are already set by the
    # header, so the pin discipline holds); exp160's config_fingerprint
    # is imported in-body for the exp198-form fingerprint assert — the
    # reader-line import block below stays byte-verbatim
    from experiments.exp160_any_medium import (  # noqa: E402
        config_fingerprint)

    # ---- the reader-line import block (exp243's block VERBATIM — the
    #      exp225 order: the whole chain first, the floor restore
    #      after) --------------------------------------------------------
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    import experiments.exp142_sign_read as _m142  # noqa: E402
    import experiments.exp145_phase_read as _m145  # noqa: E402
    import experiments.exp148_temporal_read as _m148  # noqa: E402
    import experiments.exp94_multizone_scale as _m94  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from experiments.exp136_generator_v6 import (  # noqa: E402
        ERR_BAR)
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
    #      discipline, exp243's reader-line application VERBATIM) -------
    PROD_FLOOR = -60.0                     # CF-1's production value
    READER_PIN_FLOOR = -35.0               # the import-chain's pin
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    _PRE_RESTORE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in PINNED}
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert g6.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (g6)"

    # ---- the read stack, asserted before any decode (exp198's assert
    #      form, pre-run; re-asserted at every process exit) -------------
    fp160 = config_fingerprint()           # exp160's READ_CONFIG
    assert fp160 == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp160}"
    assert SCOPED_THRESHOLD == 32.0, "scoped threshold drifted"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the reader's executor op {STAR_OP} != S* {S_STAR}"

    REWIRE_P = 0.10                        # exp225's corpus rewire p
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    # the seeds: exp142's seeds; exp198's n=400 line's seeds asserted
    # identical, and both asserted identical to exp243's deposited
    # battery seeds below
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert tuple(int(s) for s in SEEDS) == SEEDS_RUN, "seed-line drift"
    assert len(SEEDS_RUN) == 3, "the pre-registration's 3 seeds"
    # the pre-named perturbation set (exp243's docstring order — the
    # battery arms ARE exp243's candidate records, zero new knobs)
    PERT_P1 = "P1_canon_zone_relabelings"
    PERT_P2 = "P2_boundary_double_frequency_rewiring"
    PERT_P3 = "P3_deep_band_substitution"
    # the canonical battery arm's instance -> its medium (exp256's
    # battery construction; cross-checked against the deposit's own
    # worst_medium records per row below)
    CANON_MEDIUM_OF_PERT = {PERT_P1: "mirror", PERT_P2: "boundary_double"}

    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP229 = os.path.join(ROOT, "results",
                          "exp229_curvature_test.json")
    DEP262 = os.path.join(ROOT, "results",
                          "exp262_variance_components.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    for _p in (DEP243, DEP256, DEP229, DEP262, DEP182):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    # R4: the deposits READ-ONLY — shas taken BEFORE any read, re-verified
    # byte-unchanged at every process exit and at the merge, recorded in
    # the deposit
    ro_before = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                 "exp229": _sha(DEP229), "exp262": _sha(DEP262),
                 "exp182": _sha(DEP182)}
    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP262) as fh:
        dep262 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)

    # the context anchor (the docstring's open item): exp262's deposited
    # arm share — the rank variance this instrument localizes
    arm_share_262 = float(
        dep262["attribution"]["shares_of_rank_variance"]["arm"])
    assert round(arm_share_262, 4) == 0.7570, \
        f"exp262's deposited arm share drifted: {arm_share_262}"

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    def _a_sha(A):
        return hashlib.sha256(
            np.ascontiguousarray(np.abs(np.asarray(A, dtype=float)),
                                 dtype=np.float64).tobytes()
        ).hexdigest()

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
        _LOCK_LOG.append((host, row_key, int(seed)))

    # ---- THE MEDIUM: the host's own W as a static single-frame decode
    #      medium (exp225's HostWMedium VERBATIM).
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

    # ---- THE ONE CALL SITE: the production scoped arm (exp178's
    #      wiring) — exp243's replicas VERBATIM (the plain replica for
    #      the MULTI-identity audits, which assert it IS
    #      exp148.decode("scoped", ...); the state-carrying replica —
    #      exp243's A3 read path, the ONE added line return_state=True
    #      on the TC3 call — for the battery rows).
    def _scoped_row_read(spec, med, seed, fmax):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:            # exp169's rule
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
            out = execute_signed(spec, A_ext, seed, op=STAR_OP)  # TC3
        out["rho"] = rho
        out["branch"] = branch
        return out

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

    # ---- the STAGE-HOLD replicas: exp243's state-carrying scoped read
    #      (_scoped_row_read_state above, VERBATIM) with EXACTLY ONE
    #      stage's input replaced — the exp264 executor-diff disclosure
    #      style: every line identical, the ONE swap line named. The
    #      substituted medium's own stage is still computed first (the
    #      verbatim body shape; its value is discarded by the swap and
    #      the swap's provenance is recorded by the caller). ----------
    def _scoped_row_read_state_s1(spec, med, seed, fmax, A_held):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)
                F = flip_clock_matrix(inner)
            else:
                A, rho, branch = project_phase_native(med)
                F = flip_clock_matrix(med)
            A = A_held                    # THE S1 HOLD: the projection
                                          # stage's output (PN1/PN2 on
                                          # the canon row's medium)
                                          # replaces the substituted
                                          # medium's own projection
            A_ext = A + F
            assert not np.iscomplexobj(A_ext)
            out = execute_signed(spec, A_ext, seed, op=STAR_OP,
                                 return_state=True)
        out["rho"] = rho
        out["branch"] = branch
        return out

    def _scoped_row_read_state_s2(spec, med, seed, fmax, F_held):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)
                F = flip_clock_matrix(inner)
            else:
                A, rho, branch = project_phase_native(med)
                F = flip_clock_matrix(med)
            F = F_held                    # THE S2 HOLD: the flip-clock
                                          # stage's output (TC1 on the
                                          # canon row's medium)
                                          # replaces the substituted
                                          # medium's own F
            A_ext = A + F
            assert not np.iscomplexobj(A_ext)
            out = execute_signed(spec, A_ext, seed, op=STAR_OP,
                                 return_state=True)
        out["rho"] = rho
        out["branch"] = branch
        return out

    def _decode_row_hold(kind, host, row_key, spec, med, seed, fmax,
                         held):
        """One state-carrying decode (kind None = exp256's verbatim S0
        path; "s1"/"s2" = the stage-hold replicas above); a rejection
        is RECORDED, never hidden (exp142's zero-rejection hygiene; the
        caller raises) — exp243's _decode_row at the state-carrying
        call site, with the A3 state-convention assert (the recomputed
        RMS matches the reported err at the exp142 2-dp convention)."""
        _lock_read(host, row_key, seed)
        try:
            if kind is None:
                out = _scoped_row_read_state(spec, med, seed, fmax)
            elif kind == "s1":
                out = _scoped_row_read_state_s1(spec, med, seed, fmax,
                                                held)
            elif kind == "s2":
                out = _scoped_row_read_state_s2(spec, med, seed, fmax,
                                                held)
            else:
                raise ValueError(kind)
            err = float(out["err_vs_target"])
            if not np.isfinite(err):
                raise ValueError(f"non-finite decode err {err}")
            V = np.asarray(out["final_state"]["V"], dtype=float)
            T = np.asarray(out["final_state"]["target"], dtype=float)
            err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
            assert round(err_exact, 2) == round(err, 2), \
                "state err vs reported err drift"
            return {"ok": True, "err": err, "err_exact": err_exact,
                    "V": V, "T": T,
                    "verified": bool(out.get("program_verified", False)),
                    "branch": out.get("branch")}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- the per-class target rows (exp225's build_rows VERBATIM,
    #      exp227's disclosed n-parameterization of the two deposited
    #      checksum asserts — fired on the n=100 H0 rebuild only): the
    #      host's own canon (wildtype) + 3 union targets (manifest
    #      0/49/99) + the deep band's -60.0 rung both instances.
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    def build_rows(host_name: str, canon: np.ndarray, n: int) -> list:
        rows = []
        # (a) the host's own canon (wildtype): the empty program —
        #     spec_target_n of the zero-zone spec IS the canon target.
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp225-host-canon",
                             somatic_latch=False)
        f_c = spec_target_n(spec_c, canon, n)
        assert np.array_equal(f_c, canon), "canon row target != canon"
        rows.append({"tclass": "canon", "key": "canon", "spec": spec_c,
                     "f": f_c, "f_sha256": _f_sha(f_c)})
        # (b) the union's carried targets: manifest indices 0/49/99
        #     (exp214's manifest rebuild VERBATIM; checksummed on the
        #     n=100 H0 rebuild).
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
                assert sha == m["f_sha256"], \
                    (f"manifest checksum mismatch on the n=100 H0 "
                     f"rebuild (target {m['index']}): rebuilt {sha} "
                     f"!= deposited {m['f_sha256']}")
            rows.append({"tclass": "manifest",
                         "key": f"m{m['index']}", "index": m["index"],
                         "spec": spec, "f": f, "f_sha256": sha,
                         "zone_count": m["zone_count"],
                         "vmin": m["vmin"], "vmax": m["vmax"]})
        # (c) the deep band's -60.0 rung, both instances (exp214's
        #     deep construction VERBATIM; bit-asserted against exp172's
        #     own construction on the n=100 H0 rebuild).
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
                assert np.array_equal(f, f_ref), (
                    f"deep {DEEP_RUNG:g} i{inst} rebuild != exp172's "
                    f"construction")
            rows.append({"tclass": "deep",
                         "key": f"r{DEEP_RUNG:g}i{inst}",
                         "rung": DEEP_RUNG, "instance": inst,
                         "spec": spec, "f": f, "f_sha256": _f_sha(f)})
        assert len(rows) == 6, "row build drifted"
        assert sum(1 for r in rows if r["tclass"] == "canon") == 1
        assert sum(1 for r in rows if r["tclass"] == "manifest") == 3
        assert sum(1 for r in rows if r["tclass"] == "deep") == 2
        return rows

    # ---- exp208's three-class decomposition machinery VERBATIM -------
    # (the boundary-signature instrument; classify copied byte-for-byte
    # from exp208_c6_tail_ablation via exp243/exp256, zero knobs)
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
        # PAIR-JUNCTION: endpoint of >= 2 chords in the medium's
        # chord set (the pair support of the medium's base
        # adjacency |Wbase| > 0 — the hyperedge cliques are group
        # couplings, not pairs; DISCLOSED)
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

    # ---- the pre-named perturbation constructors (exp243 VERBATIM) ----
    def p1_mirror(A: np.ndarray) -> np.ndarray:
        """P1 — THE CANON/ZONE RELABELINGS: the zero-knob mirror of the
        medium's node labels (node i -> n-1-i, A' = pi A pi^T)."""
        n = A.shape[0]
        pi = np.arange(n)[::-1]
        return A[np.ix_(pi, pi)].copy()

    def p2_boundary_double(A: np.ndarray, canon_base: np.ndarray):
        """P2 — THE BOUNDARY-DOUBLE-FREQUENCY REWIRING: exp208's
        CANON-BOUNDARY set on the base medium's own canon; each boundary
        cell chorded to its NEXT TWO boundary peers in cyclic index
        order (symmetric, added iff absent)."""
        bnd = classify(canon_base, A)["boundary"]
        idx = sorted(int(i) for i in np.where(bnd)[0])
        k = len(idx)
        assert k >= 2, "a two-value canon carries >= 2 boundary cells"
        A2 = A.copy()
        added = []
        for pos, i in enumerate(idx):
            for off in (1, 2):
                j = idx[(pos + off) % k]
                if j != i and A2[i, j] == 0:
                    A2[i, j] = A2[j, i] = 1.0
                    added.append([int(i), int(j)])
        return A2, idx, added

    def p3_deep_rows(rows: list) -> list:
        """P3 — THE DEEP-BAND SUBSTITUTION: the candidate's read program
        substituted from the canon row to the deep band's -60.0 rung
        rows (BOTH pre-named instances); the medium unchanged."""
        deep = [r for r in rows if r["tclass"] == "deep"]
        assert len(deep) == 2 and [r["instance"] for r in deep] == \
            list(DEEP_INSTANCES), "the deep rows drifted"
        return deep

    # ---- dispatch ------------------------------------------------------
    print(f"=== exp267: THE READ-STAGE ATTRIBUTION (batch 26) ===")
    print(f"  mode: {'segment ' + args.seg if args.seg else 'merge'} | "
          f"battery: 12 hosts x 3 seeds x 2 deep instances = 72 "
          f"substituted rows at n={N400}")
    print(f"  read: exp178's production scoped arm; exp160's "
          f"READ_CONFIG fingerprint {fp160} (== 8e11e88c1c2f1518); "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})\n")

    # ---- the 12 hosts rebuilt from exp243's DEPOSIT records (exp256's
    #      rebuild VERBATIM: every rebuild bit-asserted against the
    #      deposit's own sha records) ------------------------------------
    CLASS_ORDER = sorted(dep243["classes"])
    assert len(CLASS_ORDER) == 12, "the 12 candidate hosts"
    # R4's determinism subset (pre-named, zero knobs): the first six
    # hosts in the deposit's own sorted order — S0/S1/S2/S3 re-run on
    # these and compared bit-identically
    DETERMINISM_HOSTS = CLASS_ORDER[:6]
    assert len(DETERMINISM_HOSTS) == 6
    bases400 = {}
    for k in CLASS_ORDER:
        rec = dep243["classes"][k]
        if k in ("H0", "H1"):
            A = graph_path(N400)
        else:
            A = small_world(N400, REWIRE_P, int(rec["rewire_seed"]))
        assert A.sum() > 0
        assert _a_sha(A) == rec["base_sha256"], \
            f"{k} base rebuild drifted from exp243's deposit"
        assert int(np.count_nonzero(np.triu(A, 1))) == \
            int(rec["edges_base"]), f"{k} edge count drifted"
        bases400[k] = A
    assert np.array_equal(bases400["H0"], bases400["H1"]), \
        "the chain class's n=400 call site must echo H1 bit-exactly"
    assert np.array_equal(graph_path(N400), bases400["H1"]), \
        "the n=400 path base drifted from exp225's H1 construction"
    # exp225's per-host canon identity, re-asserted at n=400 (exp243's
    # audit VERBATIM)
    for k in CLASS_ORDER:
        assert np.array_equal(labeling_bfs_n(np.abs(bases400[k])),
                              labeling_bfs_n(bases400[k]))
    # the instrument-identity audit on the n=100 H0 canon (exp243's
    # H0 asserts: dep182's manifest checksums + exp172's deep
    # construction, bit-exact)
    canon0 = labeling_bfs_n(g6.A_CHAIN)
    assert np.array_equal(canon0, g6.wildtype_target(g6.N))
    build_rows("H0", canon0, int(g6.N))

    # ---- the per-host context (exp256's battery construction, the
    #      SUBSTITUTED arm + the canon decode's media; the canonical
    #      arm's P1/P2 decode mediums are exp256's OWN DEPOSITED
    #      worst_medium records — see the interpretation note) -----------
    CTX: dict = {}
    for k in CLASS_ORDER:
        rec = dep243["classes"][k]
        A_base = bases400[k]
        canon_base = labeling_bfs_n(A_base)
        fmax_b = float(f_max_frames(list(HostWMedium(A_base).snapshots())))
        assert fmax_b == float(rec["f_max_base"]), \
            f"{k} f_max drifted from exp243's deposit"
        nb = int(classify(canon_base, A_base)["boundary"].sum())
        assert nb == int(rec["n_boundary_cells_base"]), \
            f"{k} boundary-cell count drifted (classify instrument)"
        rows = build_rows(k, canon_base, N400)
        canon_row = rows[0]
        assert canon_row["tclass"] == "canon"
        deep_rows = p3_deep_rows(rows)
        mirror_med = p1_mirror(A_base)
        bd_med, bidx, added = p2_boundary_double(A_base, canon_base)
        cand = {}
        for c in dep243["candidates"]:
            if c["cls"] == k:
                cand[(c["pert"], c["row_key"])] = c
        assert set(cand) == {
            (PERT_P1, "canon"), (PERT_P2, "canon"),
            (PERT_P3, f"r{DEEP_RUNG:g}i0"),
            (PERT_P3, f"r{DEEP_RUNG:g}i1")}, \
            f"{k} candidate set drifted from exp243's deposit"
        assert _a_sha(mirror_med) == \
            cand[(PERT_P1, "canon")]["medium_sha256"], \
            f"{k} mirror-medium rebuild drifted"
        assert _a_sha(bd_med) == \
            cand[(PERT_P2, "canon")]["medium_sha256"], \
            f"{k} boundary-double-medium rebuild drifted"
        assert _a_sha(A_base) == \
            cand[(PERT_P3, f"r{DEEP_RUNG:g}i0")]["medium_sha256"] \
            == cand[(PERT_P3, f"r{DEEP_RUNG:g}i1")]["medium_sha256"], \
            f"{k} base-medium rebuild drifted"
        dep_p2 = cand[(PERT_P2, "canon")]
        assert bidx == list(dep_p2["boundary_cells"]), \
            f"{k} P2 boundary-cell set drifted"
        assert added == [list(a) for a in dep_p2["chords_added"]], \
            f"{k} P2 chords drifted"
        # the canon decode's medium PER SEED: exp256's deposited
        # canonical row's worst instance (the battery's canonical
        # value's own decode — the interpretation note in the deposit)
        canon_rows_dep = {int(r["seed"]): r for r in dep256["rows"]
                          if r["host"] == k and r["arm"] == "canonical"}
        assert sorted(canon_rows_dep) == list(SEEDS_RUN), \
            f"{k} canonical rows drifted in exp256's deposit"
        canon_medium_by_seed = {}
        for s, r in canon_rows_dep.items():
            assert r["worst_medium"] == \
                CANON_MEDIUM_OF_PERT[r["worst_pert"]], \
                f"{k} s{s} worst_medium/worst_pert drift"
            # the canonical row's worst instance's own deposited err —
            # the S3 canon-decode anchor (bit-exact reproduction)
            w_inst = [i for i in r["instances"]
                      if i["pert"] == r["worst_pert"]]
            assert len(w_inst) == 1
            canon_medium_by_seed[s] = {
                "medium": r["worst_medium"],
                "dep_err": float(w_inst[0]["err"]),
                "dep_verified": bool(w_inst[0]["verified"]),
                "dep243_err": float(
                    cand[(r["worst_pert"], "canon")]["errs"][
                        SEEDS_RUN.index(s)]),
                "dep243_verified": bool(
                    cand[(r["worst_pert"], "canon")]["verified"][
                        SEEDS_RUN.index(s)])}
        # the substituted rows' deposited anchors (R1's comparison
        # targets): errs + verified per (seed, deep instance)
        subst_rows_dep = {int(r["seed"]): r for r in dep256["rows"]
                          if r["host"] == k and r["arm"] == "substituted"}
        assert sorted(subst_rows_dep) == list(SEEDS_RUN), \
            f"{k} substituted rows drifted in exp256's deposit"
        subst_anchor = {}
        for s, r in subst_rows_dep.items():
            assert len(r["instances"]) == 2
            for i in r["instances"]:
                assert i["pert"] == PERT_P3
                subst_anchor[(s, i["row_key"])] = {
                    "err": float(i["err"]),
                    "verified": bool(i["verified"]),
                    "row_target_sha256": i["row_target_sha256"]}
        # the deep rows' rebuilt targets bit-match the deposit's own
        # per-row target sha records (exp265's G1 form, per row)
        for dr in deep_rows:
            for s in SEEDS_RUN:
                assert _f_sha(dr["f"]) == \
                    subst_anchor[(s, dr["key"])]["row_target_sha256"], \
                    f"{k} {dr['key']} target rebuild drifted"
        # the canon row's stage outputs per medium (the projection and
        # the flip-clock are deterministic functions of the medium —
        # seed-independent; recorded as shas)
        stage_out = {}
        for med_name, med_A in (("mirror", mirror_med),
                                ("boundary_double", bd_med)):
            med = HostWMedium(med_A)
            A_c, rho_c, branch_c = project_phase_native(med)
            F_c = flip_clock_matrix(med)
            stage_out[med_name] = {
                "A": A_c, "F": F_c, "rho": float(rho_c),
                "branch": str(branch_c),
                "A_sha256": _a_sha(A_c), "F_sha256": _f_sha(F_c)}
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand, "canon_row": canon_row,
            "deep_rows": deep_rows,
            "canon_medium_by_seed": canon_medium_by_seed,
            "subst_anchor": subst_anchor,
            "media": {"mirror": mirror_med, "boundary_double": bd_med},
            "stage_out": stage_out}
        del rows

    # the MULTI-identity audits on the base media (exp243's audit
    # VERBATIM: the replica IS exp148.decode("scoped", ...)) — run in
    # the s0 segment only (the reproduction anchor's segment)
    def _multi_identity_audits() -> dict:
        audits: dict = {}
        for k in CLASS_ORDER:
            med_b = HostWMedium(CTX[k]["base"])
            fmax_b = CTX[k]["fmax"]
            prod = exp148_decode("scoped", med_b, SEEDS_RUN[0],
                                 f_max=fmax_b)
            mine = _scoped_row_read(MULTI, med_b, SEEDS_RUN[0], fmax_b)
            ok = bool(
                prod["ok"]
                and float(prod["err"]) == float(mine["err_vs_target"])
                and prod["verified"] == bool(mine["program_verified"])
                and prod.get("rho") == mine.get("rho")
                and prod.get("branch") == mine.get("branch"))
            assert ok, \
                f"{k}: the scoped wiring drifted from " \
                f"exp148.decode('scoped')"
            audits[k] = {"seed": int(SEEDS_RUN[0]),
                         "bit_identical": True,
                         "prod_err": float(prod["err"]),
                         "f_max": fmax_b}
            _lock_read(k, "multi_audit", SEEDS_RUN[0])
        return audits

    # the F-identity disclosure check: on the battery's static
    # single-frame HostWMedium media the flip-clock stage is
    # STRUCTURALLY ZERO (TC1 counts presence transitions over frames;
    # one frame -> no transitions) — asserted once per host so the S2
    # arm's reading is anchored, not assumed
    def _assert_flip_clock_static(k):
        for med_name, med_A in CTX[k]["media"].items():
            F_c = flip_clock_matrix(HostWMedium(med_A))
            F_b = flip_clock_matrix(HostWMedium(CTX[k]["base"]))
            assert not F_c.any() and not F_b.any(), \
                f"{k} {med_name}: TC1 non-zero on a static medium?!"
            st = CTX[k]["stage_out"][med_name]
            assert np.array_equal(st["F"], F_c)

    # ---- the four checkpoint segments (one foreground process per
    #      arm; the merge joins them and evaluates the gates) ----------
    def _seg_record(seg, section):
        ro_after = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                    "exp229": _sha(DEP229), "exp262": _sha(DEP262),
                    "exp182": _sha(DEP182)}
        rec = {
            "seg": seg,
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_aa0acdb": docstring_ok,
            "fingerprint_pre": fp160,
            "fingerprint_post": config_fingerprint(),
            "read_only_shas_before": ro_before,
            "read_only_shas_after": ro_after,
            "read_only_byte_unchanged": bool(ro_after == ro_before),
            "floors_pre_restore": dict(_PRE_RESTORE),
            "floor_at_exit_pending_assert": float(
                CORE.NEURAL_SPEC_MIN),
            "lock_log_entries": len(_LOCK_LOG),
            "lock_log_unique": len(set(_LOCK_LOG)) == len(_LOCK_LOG),
            "section": section}
        assert rec["read_only_byte_unchanged"], \
            f"a read-only deposit changed ({seg})"
        assert rec["fingerprint_post"] == fp160, \
            f"the read fingerprint drifted ({seg})"
        assert rec["lock_log_unique"], f"duplicate locks ({seg})"
        return rec

    def _write_seg(rec):
        path = os.path.join(ROOT, "results",
                            f"_exp267_seg_{rec['seg']}.json")
        with open(path, "w") as f:
            json.dump(rec, f, indent=1, default=float)
        print(f"  segment {rec['seg']} written -> {path}")
        return path

    def _expected_locks(seg):
        return {"s0": 72 + 36 + 12, "s1": 72 + 36, "s2": 72 + 36,
                "s3": 36 + 18}[seg]

    def _run_rows(seg, pass_tag, hosts):
        """The arm's decodes over (hosts x 3 seeds x 2 deep instances);
        returns the per-row records."""
        out_rows: list = []
        n_rej = 0
        for k in hosts:
            ctx = CTX[k]
            ts = time.time()
            for s in SEEDS_RUN:
                canon_medium = ctx["canon_medium_by_seed"][s]["medium"]
                canon_state = None
                if seg == "s3":
                    # S3 — the EXECUTOR held: the canon row's walk (the
                    # canonical arm's worst instance's decode, re-run
                    # state-carrying at the same seed) with the
                    # substituted row's target swapped in at the error
                    # read; NO substituted decode runs. ONE canon
                    # decode per (host, seed) — its output feeds both
                    # deep instances' error reads.
                    cdec = _decode_row_hold(
                        None, k, f"canon:{pass_tag}",
                        ctx["canon_row"]["spec"],
                        HostWMedium(ctx["media"][canon_medium]),
                        s, ctx["fmax"], None)
                    if not cdec["ok"]:
                        n_rej += 1
                        raise AssertionError(
                            f"{k} canon s{s} rejection: "
                            f"{cdec['rejection']}")
                    # the canonical-decode anchor: the re-run IS the
                    # battery's canonical instance — its err and
                    # verified flag reproduce the deposited
                    # worst-instance record bit-exactly
                    anch = ctx["canon_medium_by_seed"][s]
                    assert float(cdec["err"]) == anch["dep_err"] \
                        == anch["dep243_err"], \
                        (f"{k} s{s}: the canon decode drifted "
                         f"from the deposited canonical "
                         f"instance ({cdec['err']} vs "
                         f"{anch['dep_err']}/{anch['dep243_err']})")
                    assert bool(cdec["verified"]) == \
                        anch["dep_verified"] == \
                        anch["dep243_verified"], \
                        f"{k} s{s}: the canon verified flag drifted"
                    canon_state = {"err": float(cdec["err"]),
                                   "V": cdec["V"]}
                for dr in ctx["deep_rows"]:
                    key = (f"{pass_tag}:{seg}:{k}:{dr['key']}:s{s}")
                    if seg == "s3":
                        V_c = canon_state["V"]
                        err_s3 = float(round(float(np.sqrt(np.mean(
                            (V_c - dr["f"]) ** 2))), 2))
                        err_s3_exact = float(np.sqrt(np.mean(
                            (V_c - dr["f"]) ** 2)))
                        out_rows.append({
                            "host": k, "seed": int(s),
                            "instance": int(dr["instance"]),
                            "row_key": dr["key"],
                            "canon_medium": canon_medium,
                            "canon_decode_err": canon_state["err"],
                            "err": err_s3, "err_exact": err_s3_exact,
                            "row_target_sha256": _f_sha(dr["f"])})
                    else:
                        held = None
                        if seg == "s1":
                            held = ctx["stage_out"][canon_medium]["A"]
                        elif seg == "s2":
                            held = ctx["stage_out"][canon_medium]["F"]
                        out = _decode_row_hold(
                            None if seg == "s0" else seg, k, key,
                            dr["spec"], HostWMedium(ctx["base"]), s,
                            ctx["fmax"], held)
                        if not out["ok"]:
                            n_rej += 1
                            raise AssertionError(
                                f"{k} {dr['key']} s{s} rejection: "
                                f"{out['rejection']}")
                        rec = {
                            "host": k, "seed": int(s),
                            "instance": int(dr["instance"]),
                            "row_key": dr["key"],
                            "canon_medium": canon_medium,
                            "err": float(out["err"]),
                            "err_exact": float(out["err_exact"]),
                            "verified": bool(out["verified"]),
                            "branch": str(out["branch"])}
                        if seg == "s1":
                            rec["held_A_sha256"] = _a_sha(held)
                        if seg == "s2":
                            rec["held_F_all_zero"] = bool(
                                not np.asarray(held).any())
                        out_rows.append(rec)
            print(f"  [{k}] {seg} {pass_tag}: "
                  f"{len(SEEDS_RUN) * len(ctx['deep_rows'])} rows | "
                  f"{time.time() - ts:.1f} s")
        assert n_rej == 0, f"{n_rej} rejections in {seg} {pass_tag}"
        assert len(out_rows) == len(hosts) * 6
        return out_rows

    if args.seg is not None:
        seg = args.seg
        if seg == "s0":
            # R1 RUNS FIRST: the S0 reproduction battery, then the
            # MULTI-identity audits; fail = STOP (SystemExit 3), no
            # tuning, nothing downstream runs
            rows1 = _run_rows("s0", "pass1", CLASS_ORDER)
            audits = _multi_identity_audits()
            # the R1 comparison: bit-exact vs BOTH deposits (the
            # exp142 2-dp convention)
            n_ok = 0
            mismatches = []
            for r in rows1:
                anch = CTX[r["host"]]["subst_anchor"][
                    (r["seed"], r["row_key"])]
                cand_rec = CTX[r["host"]]["cand"][
                    (PERT_P3, r["row_key"])]
                d243_err = float(
                    cand_rec["errs"][SEEDS_RUN.index(r["seed"])])
                d243_ver = bool(
                    cand_rec["verified"][SEEDS_RUN.index(r["seed"])])
                ok = bool(r["err"] == anch["err"] == d243_err
                          and r["verified"] == anch["verified"]
                          == d243_ver)
                n_ok += int(ok)
                if not ok:
                    mismatches.append(
                        {"host": r["host"], "seed": r["seed"],
                         "row_key": r["row_key"], "rerun": r["err"],
                         "dep256": anch["err"], "dep243": d243_err})
            # the 6-host pass-2 determinism re-run (R4's clause)
            rows2 = _run_rows("s0", "pass2", DETERMINISM_HOSTS)
            d1 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows1 if r["host"] in DETERMINISM_HOSTS}
            d2 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows2}
            diffs = [str(kk) for kk in sorted(set(d1) | set(d2))
                     if d1.get(kk) != d2.get(kk)]
            section = {
                "arm": "S0_baseline_no_hold",
                "definition": ("the substituted rows as exp256 ran "
                               "them — the unmodified production "
                               "scoped decode, state-carrying"),
                "n_rows": len(rows1),
                "R1_reproduction": {
                    "n_bit_exact": n_ok, "n_rows": 72,
                    "bar": ("S0 reproduces the deposited errs "
                            "bit-exact (72/72; the machinery "
                            "anchor) — vs exp256's substituted "
                            "instances AND exp243's P3 candidates, "
                            "errs and verified flags"),
                    "pass": bool(n_ok == 72),
                    "mismatches": mismatches[:10]},
                "multi_identity_audits": audits,
                "determinism_pass2": {
                    "hosts": DETERMINISM_HOSTS,
                    "n_rows": len(rows2),
                    "bit_identical": bool(not diffs),
                    "diffs": diffs[:10]},
                "rows": rows1}
            assert len(_LOCK_LOG) == _expected_locks("s0"), \
                "s0 lock composition drifted"
            rec = _seg_record("s0", section)
            _write_seg(rec)
            if not section["R1_reproduction"]["pass"]:
                print("R1 FAIL — the machinery anchor is broken; "
                      "STOP (no tuning, nothing downstream runs)")
                raise SystemExit(3)
        elif seg in ("s1", "s2"):
            stage = {"s1": ("S1_projection_held",
                            "the projection stage's output (PN1/PN2) "
                            "computed on the canon row's medium, "
                            "applied to the substituted decode; the "
                            "flip-clock and executor run the "
                            "substituted row's own"),
                     "s2": ("S2_flip_clock_held",
                            "the flip-clock stage's output (TC1's F) "
                            "computed on the canon row's medium, "
                            "applied to the substituted decode; the "
                            "projection and executor run the "
                            "substituted row's own")}[seg]
            for k in CLASS_ORDER:
                _assert_flip_clock_static(k)
            rows1 = _run_rows(seg, "pass1", CLASS_ORDER)
            rows2 = _run_rows(seg, "pass2", DETERMINISM_HOSTS)
            d1 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows1 if r["host"] in DETERMINISM_HOSTS}
            d2 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows2}
            diffs = [str(kk) for kk in sorted(set(d1) | set(d2))
                     if d1.get(kk) != d2.get(kk)]
            if seg == "s2":
                n_zero_F = sum(int(r["held_F_all_zero"])
                               for r in rows1)
            section = {
                "arm": stage[0], "definition": stage[1],
                "n_rows": len(rows1),
                "determinism_pass2": {
                    "hosts": DETERMINISM_HOSTS,
                    "n_rows": len(rows2),
                    "bit_identical": bool(not diffs),
                    "diffs": diffs[:10]},
                "rows": rows1}
            if seg == "s2":
                section["held_F_all_zero_rows"] = n_zero_F
                section["structural_note"] = (
                    "on the battery's static single-frame "
                    "HostWMedium media TC1's transition count is "
                    "identically zero (asserted per host), so the "
                    "canon row's F IS the substituted rows' F — the "
                    "S2 hold is a no-op by construction; the decodes "
                    "were still run in full and are compared to S0 "
                    "at the merge (the honest execution of the "
                    "pre-named arm)")
            assert len(_LOCK_LOG) == _expected_locks(seg), \
                f"{seg} lock composition drifted"
            _write_seg(_seg_record(seg, section))
        else:
            rows1 = _run_rows("s3", "pass1", CLASS_ORDER)
            rows2 = _run_rows("s3", "pass2", DETERMINISM_HOSTS)
            d1 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows1 if r["host"] in DETERMINISM_HOSTS}
            d2 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows2}
            diffs = [str(kk) for kk in sorted(set(d1) | set(d2))
                     if d1.get(kk) != d2.get(kk)]
            section = {
                "arm": "S3_executor_held",
                "definition": ("exp142's execute_signed run on the "
                               "canon row's A_ext — the walk itself "
                               "canonicalized (the canonical arm's "
                               "worst instance's decode, re-run "
                               "state-carrying at the same seed) — "
                               "with the substituted row's target "
                               "swapped in at the error read; the "
                               "canon row's program carries no "
                               "zones, so the canonical executor "
                               "output is the no-walk settle"),
                "n_rows": len(rows1),
                "canon_decode_anchor": (
                    "every canon decode's err/verified reproduced "
                    "exp256's deposited canonical worst-instance "
                    "record AND exp243's P1/P2 candidate record "
                    "bit-exactly (asserted per decode)"),
                "determinism_pass2": {
                    "hosts": DETERMINISM_HOSTS,
                    "n_rows": len(rows2),
                    "bit_identical": bool(not diffs),
                    "diffs": diffs[:10]},
                "rows": rows1}
            assert len(_LOCK_LOG) == _expected_locks("s3"), \
                "s3 lock composition drifted"
            _write_seg(_seg_record("s3", section))
        # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing
        # line) + the docstring re-assert
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        assert hashlib.sha256(__doc__.encode()).hexdigest() == \
            EXPECTED_DOCSTRING_SHA256, "docstring drifted at exit"
        assert config_fingerprint() == fp160, "fingerprint drift at exit"
        return {}

    # ---- THE MERGE: join the four segments, evaluate the gates (each
    #      exactly once), deposit ----------------------------------------
    def _merge(paths: list) -> dict:
        sections: dict = {}
        seg_meta: dict = {}
        for p in paths:
            with open(p) as fh:
                d = json.load(fh)
            assert d["seg"] not in sections, "duplicate segment"
            assert d["docstring_byte_unchanged_vs_aa0acdb"], \
                f"{d['seg']}: docstring drifted"
            assert d["read_only_byte_unchanged"], \
                f"{d['seg']}: a read-only deposit changed"
            assert d["fingerprint_pre"] == d["fingerprint_post"] == \
                "8e11e88c1c2f1518", f"{d['seg']}: fingerprint drift"
            assert d["lock_log_unique"], f"{d['seg']}: duplicate locks"
            sections[d["seg"]] = d["section"]
            seg_meta[d["seg"]] = {
                k: d[k] for k in ("read_only_shas_before",
                                  "read_only_shas_after",
                                  "floors_pre_restore",
                                  "floor_at_exit_pending_assert",
                                  "lock_log_entries")}
        assert set(sections) == {"s0", "s1", "s2", "s3"}, \
            "the four arm segments are required"
        # R1 from the s0 segment (evaluated there, re-asserted here)
        r1 = sections["s0"]["R1_reproduction"]
        assert r1["pass"], \
            f"R1 did not pass ({r1['n_bit_exact']}/72) — STOP"

        # ---- assemble the 72-row table --------------------------------
        def _index(seg):
            return {(r["host"], int(r["seed"]), r["row_key"]): r
                    for r in sections[seg]["rows"]}
        i0, i1, i2, i3 = _index("s0"), _index("s1"), _index("s2"), \
            _index("s3")
        keys = sorted(set(i0))
        assert len(keys) == 72, f"{len(keys)} rows != 72"
        assert set(i1) == set(i2) == set(i3) == set(i0), \
            "the arms' row keys drifted"
        # the canonical rows' worst errs from exp256's deposit (the
        # arm-gap reference, audit-only)
        canon_ref = {(r["host"], int(r["seed"])): float(r["worst_err"])
                     for r in dep256["rows"] if r["arm"] == "canonical"}
        rows_out = []
        for kk in keys:
            r0, r1_, r2_, r3_ = i0[kk], i1[kk], i2[kk], i3[kk]
            assert r1_["canon_medium"] == r2_["canon_medium"] == \
                r3_["canon_medium"] == r0["canon_medium"], \
                f"{kk}: the canon-medium records drifted"
            s0, s1e = float(r0["err"]), float(r1_["err"])
            s2e, s3e = float(r2_["err"]), float(r3_["err"])
            rows_out.append({
                "host": kk[0], "seed": kk[1], "row_key": kk[2],
                "canon_medium": r0["canon_medium"],
                "S0": s0, "S1": s1e, "S2": s2e, "S3": s3e,
                "S0_exact": float(r0["err_exact"]),
                "S1_exact": float(r1_["err_exact"]),
                "S2_exact": float(r2_["err_exact"]),
                "S3_exact": float(r3_["err_exact"]),
                "delta_S1": round(s0 - s1e, 2),
                "delta_S2": round(s0 - s2e, 2),
                "delta_S3": round(s0 - s3e, 2),
                "canonical_row_worst_err": canon_ref[
                    (kk[0], kk[1])],
                "S0_verified": bool(r0["verified"]),
                "S1_verified": bool(r1_["verified"]),
                "S2_verified": bool(r2_["verified"])})
        # the S2 structural no-op, VERIFIED (not assumed): the S2 arm's
        # decodes are bit-identical to S0's on every row
        n_s2_noop = sum(1 for r in rows_out if r["S2"] == r["S0"])
        assert n_s2_noop == 72, \
            f"the S2 arm moved the errs on {72 - n_s2_noop} rows — " \
            f"the static-medium F identity broke"

        # ---- the rank instruments (the exp229/exp262 convention) ------
        def _rankdata_average(a) -> np.ndarray:
            a = np.asarray(a, dtype=float)
            order = np.argsort(a, kind="stable")
            ranks = np.empty(len(a), dtype=float)
            sa = a[order]
            i = 0
            while i < len(a):
                j = i
                while j + 1 < len(a) and sa[j + 1] == sa[i]:
                    j += 1
                ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
                i = j + 1
            return ranks

        def _pearson(x, y) -> float:
            x = np.asarray(x, dtype=float)
            y = np.asarray(y, dtype=float)
            if len(x) < 2 or np.std(x) == 0.0 or np.std(y) == 0.0:
                return float("nan")
            return float(np.corrcoef(x, y)[0, 1])

        def _spearman(x, y) -> float:
            return _pearson(_rankdata_average(x),
                            _rankdata_average(y))

        def _r2(cols, y):
            Xd = [[1.0] + list(c) for c in zip(*cols)]
            Xa = np.asarray(Xd, dtype=float)
            ya = np.asarray(y, dtype=float)
            beta, *_ = np.linalg.lstsq(Xa, ya, rcond=None)
            resid = ya - Xa @ beta
            sstot = float(((ya - ya.mean()) ** 2).sum())
            return float(1.0 - float((resid ** 2).sum()) / sstot)

        def attribution(deltas, response):
            """exp229/exp262's OLS-on-tied-average-ranks convention:
            the response ranked over the 72 rows; the three stages'
            (S0 - Sk) delta ranks as regressors; the shares the
            symmetric average of the two order-of-entry R^2
            increments (the pre-named stack order S1->S2->S3 and its
            reverse — exp262's exact two-order form); unexplained =
            1 - R^2_full; sums to 1 exactly, no clamping."""
            y = rankdata(response)
            Z = {k: rankdata(deltas[k]) for k in
                 ("S1", "S2", "S3")}
            r2 = {
                "full": _r2([Z["S1"], Z["S2"], Z["S3"]], y),
                "S1": _r2([Z["S1"]], y),
                "S2": _r2([Z["S2"]], y),
                "S3": _r2([Z["S3"]], y),
                "S1S2": _r2([Z["S1"], Z["S2"]], y),
                "S2S3": _r2([Z["S2"], Z["S3"]], y),
                "S1S3": _r2([Z["S1"], Z["S3"]], y)}
            # order 1: S1 -> S2 -> S3 (the read stack's own order)
            inc1 = {"S1": r2["S1"], "S2": r2["S1S2"] - r2["S1"],
                    "S3": r2["full"] - r2["S1S2"]}
            # order 2: S3 -> S2 -> S1 (the reverse)
            inc2 = {"S3": r2["S3"], "S2": r2["S2S3"] - r2["S3"],
                    "S1": r2["full"] - r2["S2S3"]}
            shares = {k: 0.5 * (inc1[k] + inc2[k])
                      for k in ("S1", "S2", "S3")}
            unexplained = 1.0 - r2["full"]
            total = sum(shares.values()) + unexplained
            # the 6-order symmetric average (the fully generalized
            # form) — audit-only, never gating
            inc6 = {k: [] for k in ("S1", "S2", "S3")}
            for perm in permutations(("S1", "S2", "S3")):
                prev = 0.0
                for j, k in enumerate(perm):
                    cols = [Z[m] for m in perm[:j + 1]]
                    cur = _r2(cols, y)
                    inc6[k].append(cur - prev)
                    prev = cur
            shares6 = {k: float(np.mean(inc6[k]))
                       for k in ("S1", "S2", "S3")}
            return {"r2": r2, "order_increments": {
                        "order_S1_S2_S3": inc1,
                        "order_S3_S2_S1": inc2},
                    "shares": shares,
                    "shares_6order_audit": shares6,
                    "unexplained": unexplained,
                    "sum": float(total),
                    "response_ranks_sha256": hashlib.sha256(
                        np.ascontiguousarray(y).tobytes()).hexdigest()}

        S0v = [r["S0"] for r in rows_out]
        deltas = {"S1": [r["delta_S1"] for r in rows_out],
                  "S2": [r["delta_S2"] for r in rows_out],
                  "S3": [r["delta_S3"] for r in rows_out]}
        att = attribution(deltas, S0v)
        # the exact-scale audit (the same attribution on the unrounded
        # errs — the 2-dp exp142 convention's ties sensitivity,
        # audit-only, never gating)
        deltas_exact = {
            "S1": [r["S0_exact"] - r["S1_exact"] for r in rows_out],
            "S2": [r["S0_exact"] - r["S2_exact"] for r in rows_out],
            "S3": [r["S0_exact"] - r["S3_exact"] for r in rows_out]}
        att_exact = attribution(deltas_exact,
                                [r["S0_exact"] for r in rows_out])
        # the instrument-identity audit: scipy's rankdata IS exp256's
        # tied-average implementation on this battery's values
        rank_invariance_ok = bool(all(
            np.array_equal(rankdata(v), _rankdata_average(v))
            for v in [S0v] + [deltas[k] for k in ("S1", "S2", "S3")]))
        def _jnum(x):
            """The deposit's finite-float hygiene: a non-finite
            statistic (a constant input's Spearman, e.g. the S2 no-op's)
            is recorded as null, never as a NaN/Infinity token."""
            x = float(x)
            return x if x == x and abs(x) != float("inf") else None

        # the per-stage descriptive audits (never gating)
        stage_audit = {}
        for k in ("S1", "S2", "S3"):
            d = np.asarray(deltas[k], dtype=float)
            stage_audit[k] = {
                "mean_abs_delta": float(np.mean(np.abs(d))),
                "max_abs_delta": float(np.max(np.abs(d))),
                "n_zero_delta": int(np.count_nonzero(d == 0.0)),
                "n_distinct_delta": int(len(set(d.tolist()))),
                "spearman_delta_vs_S0": _jnum(_spearman(d, S0v))}
        mean_canon = float(np.mean([r["canonical_row_worst_err"]
                                    for r in rows_out]))
        mean_s0 = float(np.mean(S0v))
        arm_gap = {"mean_substituted_S0": mean_s0,
                   "mean_canonical_worst": mean_canon,
                   "mean_gap": mean_s0 - mean_canon,
                   "mean_Sk": {k: float(np.mean(
                       [r[k] for r in rows_out]))
                       for k in ("S1", "S2", "S3")}}

        # ---- THE GATES (each evaluated exactly once) ------------------
        shares = att["shares"]
        top = max(shares, key=lambda k: shares[k])
        r2_pass = bool(shares[top] >= 0.5)
        branch = f"STAGE-CARRIES({top})" if r2_pass else "DISTRIBUTED"
        # R3's honesty clause: fired iff no stage reaches 0.5 — the
        # contrast is DISTRIBUTED and the shares are named (this
        # deposit IS the naming; the clause is executed either way)
        r3_fired = bool(not r2_pass)

        ro_after = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                    "exp229": _sha(DEP229), "exp262": _sha(DEP262),
                    "exp182": _sha(DEP182)}
        ro_unchanged = bool(
            ro_after == ro_before
            and all(seg_meta[s]["read_only_shas_after"] == ro_before
                    for s in seg_meta))
        det_ok = all(
            sections[s]["determinism_pass2"]["bit_identical"]
            for s in ("s0", "s1", "s2", "s3"))
        locks_ok = all(
            seg_meta[s]["lock_log_entries"] == _expected_locks(s)
            for s in seg_meta)
        floors_ok = all(
            seg_meta[s]["floor_at_exit_pending_assert"] == PROD_FLOOR
            for s in seg_meta)
        fp_post = config_fingerprint()
        r4_clauses = {
            "exp256_exp229_deposits_read_only_byte_unchanged":
                bool(ro_unchanged),
            "read_stack_fingerprint_pre_post": bool(
                fp_post == fp160 == "8e11e88c1c2f1518"
                and SCOPED_THRESHOLD == 32.0),
            "floor_restored_and_asserted_exit": bool(
                floors_ok and CORE.NEURAL_SPEC_MIN == PROD_FLOOR),
            "deterministic_six_host_rerun_bit_identical":
                bool(det_ok),
            "docstring_byte_unchanged": bool(docstring_ok),
            "zero_rejections_all_arms": True,
            "lock_discipline": bool(locks_ok),
            "no_wall_clock_fields": True}
        r4 = bool(all(r4_clauses.values()))
        assert abs(att["sum"] - 1.0) < 1e-9, "shares do not sum to 1"

        gates = {
            "R1_reproduction": {
                "pass": bool(r1["pass"]),
                "bar": ("S0 reproduces the deposited errs bit-exact "
                        "(72/72; the machinery anchor) — run FIRST, "
                        "fail = STOP"),
                "n_bit_exact": r1["n_bit_exact"], "n_rows": 72,
                "anchors": ["exp256's substituted instances (errs + "
                            "verified)",
                            "exp243's P3 candidates (errs + verified)"],
                "multi_identity_audits": (
                    f"{len(sections['s0']['multi_identity_audits'])}"
                    f"/12 bit-identical — the replica IS "
                    f"exp148.decode('scoped')"),
                "mismatch_records": r1["mismatches"]},
            "R2_attribution": {
                "pass": r2_pass,
                "bar": ("the three stage deltas' rank-variance shares "
                        "reported; ONE stage's share >= 0.5 (the "
                        "carrier is single-stage — the residual "
                        "localizes inside the stack)"),
                "method": ("the exp229/exp262 tied-average-rank OLS "
                           "convention on the delta ranks: the "
                           "response = the 72 S0 errs' tied average "
                           "ranks (scipy.stats.rankdata); the "
                           "regressors = the three (S0 - Sk) deltas' "
                           "tied average ranks; the shares = the "
                           "symmetric average of the two "
                           "order-of-entry R^2 increments (the "
                           "pre-named stack order S1->S2->S3 and its "
                           "reverse — exp262's exact two-order form, "
                           "zero knobs); unexplained = 1 - R^2_full; "
                           "sums to 1 exactly, no clamping"),
                "shares_of_rank_variance": shares,
                "unexplained": att["unexplained"],
                "sum": att["sum"],
                "r2": att["r2"],
                "order_increments": att["order_increments"],
                "top_stage": top,
                "gate_value": shares[top], "bar_value": 0.5},
            "R3_honesty_clause": {
                "pass": True, "fired": r3_fired,
                "bar": ("if no stage reaches 0.5, the contrast is "
                        "DISTRIBUTED (the read's stages interact — "
                        "deposited honestly, the shares named)"),
                "branch": branch,
                "shares_named": shares},
            "R4_discipline": {
                "pass": r4, "clauses": r4_clauses,
                "named_clauses": ("exp256's/exp229's deposits "
                                  "READ-ONLY sha-recorded "
                                  "byte-unchanged; the read stack's "
                                  "production fingerprint asserted "
                                  "pre/post (exp160's READ_CONFIG, "
                                  "exp198's assert form); the -60.0 "
                                  "floor restored and asserted at "
                                  "exit (the exp169 import chain pins "
                                  "-35.0 — the explicit restore); "
                                  "deterministic (S0/S1/S2/S3 re-run "
                                  "on 6 hosts, bit-identical); no "
                                  "wall-clock fields"),
                "read_only_shas": ro_after,
                "read_only_shas_by_segment": {
                    s: seg_meta[s]["read_only_shas_after"]
                    for s in seg_meta},
                "fingerprint_pre": fp160,
                "fingerprint_post": fp_post,
                "floors_pre_restore": seg_meta["s0"][
                    "floors_pre_restore"],
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "determinism": {
                    "hosts": DETERMINISM_HOSTS,
                    "per_arm_bit_identical": {
                        s: sections[s]["determinism_pass2"][
                            "bit_identical"]
                        for s in ("s0", "s1", "s2", "s3")}},
                "lock_log_entries": {
                    s: seg_meta[s]["lock_log_entries"]
                    for s in sorted(seg_meta)},
                "docstring_sha256": docstring_sha},
        }
        n_pass = sum(int(g["pass"]) for g in gates.values())
        verdict = (
            f"{n_pass}/4 gates R1-R4 | {branch} | R1 72/72 bit-exact | "
            f"shares S1 {shares['S1']:.4f} / S2 {shares['S2']:.4f} / "
            f"S3 {shares['S3']:.4f} (unexplained "
            f"{att['unexplained']:.4f}) | the arm contrast "
            f"(exp262's {arm_share_262:.3f} share) localized")

        deposit = {
            "exp": "exp267_read_stage_attribution",
            "claim": (
                "THE READ-STAGE ATTRIBUTION (batch 26; L244's "
                "registered next, pre-registration commit aa0acdb): "
                "the arm contrast's rank variance is 75.7% arm "
                "(exp262), NOT the target's geometry (exp265) and NOT "
                "closable by deposit-level structural terms (exp266) "
                "— it is the READ's own response to the deep-band "
                "substitution. The exp208 c6-tail-ablation mold "
                "applied to the read's stages: the substituted rows' "
                "72 decodes re-run with each stage's output held at "
                "its canonical-row value in turn (S1 the projection "
                "PN1/PN2, S2 the flip-clock F, S3 the executor walk); "
                "the stage whose canonicalization moves the "
                "substituted rows' errs carries the residual, read as "
                "the rank-variance share of the (S0 - Sk) delta "
                "across rows (the exp229/exp262 convention on the "
                "delta ranks)"),
            "interpretation": {
                "canon_decode": (
                    "THE CANONICAL DECODE (disclosed): 'the same "
                    "stage's output on the SAME host's canon row (the "
                    "P1/P2 battery's row), same seed' — exp256's "
                    "battery decodes the canon row TWICE per "
                    "(host, seed) (P1 on the mirror medium, P2 on the "
                    "boundary-double medium) and its canonical VALUE "
                    "is the worst instance's; the canonical decode is "
                    "therefore the DEPOSITED worst instance's decode "
                    "(exp256's own worst_medium/worst_pert records, "
                    "cross-checked consistent per row), re-run "
                    "state-carrying at the same seed — zero new "
                    "knobs, everything from the deposits. Rejected "
                    "alternatives, named for the record: a fixed "
                    "P1-mirror-only or P2-boundary-double-only canon "
                    "medium (both single decodes of the same row; "
                    "neither is 'the canonical value' the battery "
                    "carries). The canon decodes were anchored "
                    "bit-exactly to BOTH deposits per decode"),
                "stage_holds": {
                    "S1": ("the projection stage's output (PN1/PN2 on "
                           "the canon row's medium) replaces the "
                           "substituted medium's own projection; "
                           "TC2/TC3 run the substituted row's own "
                           "(the exp264 executor-diff disclosure "
                           "style: _scoped_row_read_state VERBATIM "
                           "with exactly ONE swap line)"),
                    "S2": ("the flip-clock stage's output (TC1 on the "
                           "canon row's medium) replaces the "
                           "substituted medium's own F; PN1/PN2 and "
                           "the executor run the substituted row's "
                           "own"),
                    "S3": ("the executor's output held: exp142's "
                           "execute_signed run on the canon row's "
                           "A_ext (the canon decode re-run "
                           "state-carrying, same seed) with the "
                           "substituted row's target swapped in at "
                           "the error read — the walk itself "
                           "canonicalized (the canon row's program "
                           "carries no zones, so the canonical "
                           "executor output is the no-walk settle)")},
                "structural_inertness_S2": (
                    "on the battery's static single-frame HostWMedium "
                    "media TC1's presence-transition count is "
                    "identically zero (asserted per host per medium), "
                    "so the canon row's F IS the substituted rows' F "
                    "and the S2 hold is a no-op by construction — "
                    "VERIFIED empirically: the S2 arm's 72 decodes "
                    "are bit-identical to S0's; its delta is exactly "
                    "0 on every row and its share exactly 0; the arm "
                    "was still run in full (the honest execution of "
                    "the pre-named stage)"),
                "err_convention": (
                    "all errs on the exp142 2-dp convention (the "
                    "battery's own; R1's bit-exactness lives there); "
                    "the deltas S0 - Sk on the same scale; the "
                    "attribution re-run on the unrounded errs as an "
                    "audit (the 2-dp ties sensitivity, never gating)"),
                "segmentation": (
                    "four foreground checkpoint segments (one per "
                    "arm, no setsid/nohup), each within the 570 s "
                    "budget, joined by the merge; the seg/merge "
                    "pattern is exp263/exp261's")},
            "read": {
                "wiring": ("exp178's production scoped arm: exp169's "
                           "f_max + the pre-registered THRESHOLD "
                           "(32.0); R_T (exp167) iff f_max < 32.0, "
                           "else exp148's raw temporal; "
                           "exp145/exp148 PN1/PN2 + TC1 + TC2; "
                           "exp142 execute_signed VERBATIM at "
                           "STAR_OP == S*"),
                "fingerprint": fp160,
                "fingerprint_asserted": "8e11e88c1c2f1518",
                "scoped_threshold": float(SCOPED_THRESHOLD),
                "op": {"gamma": 64.0, "mu": 0.0},
                "seeds": list(SEEDS_RUN), "n": int(N400),
                "window_h": 24.0, "commit_noise": 0.6,
                "steps_per_cell": 8,
                "floor": ("production -60.0 restored post-import "
                          "(exp218's disclosed exp169-import "
                          "discipline; the -35.0 reader-line pin "
                          "disclosed)"),
                "per_media_tuning": "none"},
            "battery": {
                "hosts": CLASS_ORDER,
                "rows": 72,
                "row_grid": ("12 hosts x 3 seeds x 2 deep instances "
                             "(r-60i0, r-60i1) on the base medium — "
                             "exp256's substituted rows exactly"),
                "canon_medium_by_seed": {
                    k: {str(s): CTX[k]["canon_medium_by_seed"][s][
                            "medium"] for s in SEEDS_RUN}
                    for k in CLASS_ORDER},
                "canon_stage_outputs_sha256": {
                    k: {m: {"A": CTX[k]["stage_out"][m]["A_sha256"],
                            "F": CTX[k]["stage_out"][m]["F_sha256"],
                            "rho": CTX[k]["stage_out"][m]["rho"],
                            "branch": CTX[k]["stage_out"][m]["branch"]}
                        for m in ("mirror", "boundary_double")}
                    for k in CLASS_ORDER}},
            "rows": rows_out,
            "attribution": {
                "method_source": ("experiments/exp262_variance_"
                                  "components.py / exp229's K3 block "
                                  "(the OLS-on-tied-average-ranks "
                                  "convention), applied to the delta "
                                  "ranks"),
                "primary": att,
                "exact_scale_audit": att_exact,
                "rankdata_invariance_scipy_vs_numpy": (
                    rank_invariance_ok),
                "per_stage_descriptive": stage_audit,
                "arm_gap_reference": arm_gap,
                "exp262_reference": {
                    "arm_share": arm_share_262,
                    "note": ("the rank variance this instrument "
                             "localizes; exp262's shares were "
                             "host/arm/seed on the 72 worsts — this "
                             "instrument splits the substituted "
                             "rows' rank variance by the three "
                             "stages' canonicalization deltas")}},
            "gates": gates,
            "branch": branch,
            "verdict": verdict,
            "provenance": {
                "pre_registration": "commit aa0acdb (batch 26)",
                "docstring_sha256": docstring_sha,
                "exp243": ro_after["exp243"],
                "exp256": ro_after["exp256"],
                "exp229": ro_after["exp229"],
                "exp262": ro_after["exp262"],
                "exp182": ro_after["exp182"],
                "machinery": ("exp256's import block + floor restore "
                              "+ exp243 host rebuild + build_rows + "
                              "classify + HostWMedium + "
                              "_scoped_row_read_state, VERBATIM")},
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of the four segments + the merge "
                             "reproduces this file byte-identically")}
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        _ser = json.dumps(deposit, indent=1, default=float)
        assert "NaN" not in _ser and "Infinity" not in _ser, \
            "non-finite token in the deposit"
        with open(out_path, "w") as f:
            f.write(_ser)
        print(f"\n  GATES: {verdict}")
        for kk, g in gates.items():
            print(f"    {kk}: {'PASS' if g['pass'] else 'FAIL'}")
        print(f"  shares S1 {shares['S1']:.4f} / S2 {shares['S2']:.4f} / "
              f"S3 {shares['S3']:.4f} | unexplained "
              f"{att['unexplained']:.4f} | branch {branch}")
        print(f"  exact-scale audit shares "
              f"{att_exact['shares']['S1']:.4f} / "
              f"{att_exact['shares']['S2']:.4f} / "
              f"{att_exact['shares']['S3']:.4f}")
        print(f"  deposited {out_path}")
        # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing
        # line) + the docstring re-assert
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        assert hashlib.sha256(__doc__.encode()).hexdigest() == \
            EXPECTED_DOCSTRING_SHA256, "docstring drifted at exit"
        assert config_fingerprint() == fp160, "fingerprint drift at exit"
        return deposit

    if args.merge is not None:
        paths = args.merge if args.merge else [
            os.path.join(ROOT, "results", f"_exp267_seg_{s}.json")
            for s in ("s0", "s1", "s2", "s3")]
        return _merge(paths)
    ap.error("unreachable dispatch")
    return {}


if __name__ == "__main__":
    main()
