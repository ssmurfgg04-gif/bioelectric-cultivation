#!/usr/bin/env python3
"""exp269 — THE RESPONSE-SURFACE SAMPLE (batch 27; L246's registered
next (a) — the read's err surface sampled over the substitution's own
parameter: the deep rung's voltage ladder).

THE OPEN ITEM (L246): the boundary residual is deterministic-per-
instance, arm-carried, and irreducible at every decomposition level
(substrate, target, law, stages, channels). The one measurement never
taken: the read's response SHAPE — how the err moves as the
substitution's own parameter (the deep rung's voltage) sweeps. The
battery sampled the rung at -60.0 only; the dose-response curve is
the direct measurement of the response surface the stage ablations
proved non-decomposable.

THE INSTRUMENT (pre-registered, zero-knob): the pre-named rung
ladder {-30, -40, -50, -55, -60, -65, -70} mV x the 12 hosts x 3
seeds x 2 instances (the exp172/exp214 deep construction at each
rung; the -60.0 rung is the battery's own anchor and must reproduce
exp256's deposited errs bit-exact). The per-host curve: worst err vs
rung; the pre-named shape reads:

  D1  the curve's monotonicity per host (Spearman |rung| vs err);
  D2  the curve's inflection (the rung where the err crosses the
      battery's own worst-canonical mean — the "the substitution
      starts to cost here" point);
  D3  the curve's end-behavior (does the err saturate at the
      extreme rungs or diverge — the response surface's face at the
      physiological boundary).

PRE-REGISTERED GATES:

  U1  THE ANCHOR: the -60.0 rung reproduces exp256's deposited
      substituted-row errs bit-exact (72 values; the machinery
      anchor; fail = STOP, no tuning).
  U2  THE SURFACE: all 7 rungs x 72 rows complete, finite, zero
      rejections; the per-host curves deposited.
  U3  THE SHAPE: the monotonicity/inflection/saturation reads
      reported per host and pooled; the gate: the pooled
      monotonicity Spearman >= 0.5 (the response has a directed
      shape — the surface is a curve, not a scatter) AND the
      extreme-rung behavior named (saturating or diverging).
  U4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (the -60.0 rung re-run IS the anchor; the
      -65.0 rung re-run on 6 hosts bit-identical); no wall-clock
      fields.

THE BRANCHES (pre-named): CURVE (U3 passes — the response surface
has a directed, nameable shape) / SCATTER (it does not).

RUN: 7 rungs x 72 rows at n=400 (~1.3 s/row ≈ 11 min) — checkpoint
segments per rung pair.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp269_response_surface.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates U1-U4 below evaluated exactly once,
    #      pre-registration commit dc92b37) ==================================
    import argparse
    import hashlib
    import json
    import time

    import numpy as np

    # body-only plumbing (disclosed): json/numpy/argparse imported HERE,
    # before any use; exp160's config_fingerprint for the exp198-form
    # fingerprint assert; the reader-line import block below stays
    # byte-verbatim
    from experiments.exp160_any_medium import (  # noqa: E402
        config_fingerprint)
    # the compiler's own entry point + the identity-repertoire band
    # constants — READ for the refusal classification only, never rebound
    # (the production system's own safety refusal IS the boundary's face;
    # disclosed in-body plumbing, the reader block above untouched)
    from cultivation.compiler.anatomy import (  # noqa: E402
        REPERTOIRE_HI, REPERTOIRE_LO, compile_anatomy)

    # ---- the docstring gate, FIRST in every process (segments, merge):
    #      the docstring is the dc92b37 pre-registration, byte-for-byte;
    #      fail = STOP before anything runs (the hard rule; the sha is
    #      of the RAW module __doc__ — the exact literal, trailing
    #      newline included, as imported) ---------------
    EXPECTED_DOCSTRING_SHA256 = (
        "3075d46a3f41e2a0ef155d4c89d960e52e04c547dd896b846c65b0073edb8cc4")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    assert docstring_ok, "docstring drifted from dc92b37"

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg",
                    choices=["s60", "s30_40", "s50_55", "s65_70"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    if args.seg is None and args.merge is None:
        ap.error("one of --seg / --merge is required (the checkpoint "
                 "split: one foreground segment per pre-named rung pair, "
                 "the -60.0 anchor segment FIRST, merge at the end — the "
                 "exp267/exp263 pattern; no setsid/nohup)")

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
    # the identity-repertoire band is the production compiler's own —
    # asserted unchanged (the -60.0 floor and the repertoire floor
    # COINCIDE at production: exp168's CF-1 semantics; the rungs below
    # -60.0 are outside the band the production system accepts)
    assert (REPERTOIRE_LO, REPERTOIRE_HI) == (-60.0, -15.0), \
        "the identity repertoire drifted"

    REWIRE_P = 0.10                        # exp225's corpus rewire p
    # THE PRE-NAMED LADDER (the docstring's own order; zero knobs)
    RUNG_LADDER = (-30.0, -40.0, -50.0, -55.0, -60.0, -65.0, -70.0)
    ANCHOR_RUNG = -60.0                    # the battery's own anchor rung
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

    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP229 = os.path.join(ROOT, "results",
                          "exp229_curvature_test.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP267 = os.path.join(ROOT, "results",
                          "exp267_read_stage_attribution.json")
    for _p in (DEP243, DEP256, DEP229, DEP182, DEP267):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    # U4: the deposits READ-ONLY — shas taken BEFORE any read, re-verified
    # byte-unchanged at every process exit and at the merge, recorded in
    # the deposit
    ro_before = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                 "exp229": _sha(DEP229), "exp182": _sha(DEP182),
                 "exp267": _sha(DEP267)}
    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)
    with open(DEP267) as fh:
        dep267 = json.load(fh)

    # the context anchor (the docstring's open item): exp267's deposited
    # arm-gap reference — the battery's worst-canonical mean (the U3
    # inflection level), recomputed from exp256's canonical rows in
    # exp267's exact key order and cross-asserted bit-exact below (at
    # the merge, where the 72-key order exists)
    _dep267_mean_canon = float(
        dep267["attribution"]["arm_gap_reference"]
        ["mean_canonical_worst"])
    canon_ref = {(r["host"], int(r["seed"])): float(r["worst_err"])
                 for r in dep256["rows"] if r["arm"] == "canonical"}

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

    # ---- the production scoped arm (exp178's wiring) — exp243's
    #      replicas VERBATIM (the state-carrying replica — exp243's A3
    #      read path, the ONE added line return_state=True on the TC3
    #      call — is the battery's read; the plain replica is carried
    #      with it, uncalled: exp269 runs no MULTI-identity audits, the
    #      -60.0 anchor's bit-exactness IS the wiring-identity evidence)
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

    # ---- the state-carrying decode (exp243's _decode_row at the
    #      state-carrying call site VERBATIM, exp267's kind-dispatch
    #      form carried; only kind=None is called in exp269 — the s1/s2
    #      stage-hold replicas are exp267's machinery, uncalled here);
    #      a rejection is RECORDED, never hidden (exp142's zero-
    #      rejection hygiene; the CALLER decides: in-repertoire rejections
    #      are instrument trouble and raise, the below-repertoire rungs'
    #      refusals are the boundary's own face and are recorded) --------
    def _decode_row_hold(kind, host, row_key, spec, med, seed, fmax,
                         held):
        _lock_read(host, row_key, seed)
        try:
            if kind is None:
                out = _scoped_row_read_state(spec, med, seed, fmax)
            elif kind == "s1":
                out = _scoped_row_read_state(spec, med, seed, fmax)
                out["held"] = held        # unused in exp269 (no holds)
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

    # ---- the refusal recorder: the production compiler's OWN safety
    #      refusal, cited per refused row (a RECORD of the refusal
    #      class, never a behavior change — the repertoire constants are
    #      read, never rebound; zero knobs). The below-repertoire rungs
    #      {-65.0, -70.0} sit outside the identity band the production
    #      system accepts: execute_signed's compile_anatomy call refuses
    #      the spec BEFORE the walk, the decode returns no finite err —
    #      the response surface's face at the physiological boundary.
    def _repertoire_refusal(spec):
        prog = compile_anatomy(spec, n=int(N400))
        rej = [str(m) for m in (prog.rejected or [])]
        assert rej, "expected the identity-repertoire refusal; none"
        assert all("identity repertoire" in m for m in rej), \
            f"unexpected refusal class: {rej[:2]}"
        return rej

    # ---- the per-class target rows (exp225's build_rows VERBATIM,
    #      exp227's disclosed n-parameterization of the two deposited
    #      checksum asserts — fired on the n=100 H0 rebuild only), with
    #      THE PRE-REGISTERED LADDER PARAMETERIZATION (disclosed): the
    #      deep section (c) loops the pre-named rung ladder x both
    #      instances — the construction's OWN form at each rung (the
    #      zones carry the rung voltage; exp172's deep_target_for is the
    #      bit-asserted reference at EVERY rung on the n=100 H0 rebuild;
    #      zero knobs). The -60.0 rows are bit-identical to exp256's/
    #      exp267's deep construction by the same assert.
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
        # (c) the deep band's ladder, both instances (exp214's deep
        #     construction VERBATIM at each pre-named rung; bit-asserted
        #     against exp172's own construction on the n=100 H0 rebuild
        #     at EVERY rung).
        for rung in RUNG_LADDER:
            for inst in DEEP_INSTANCES:
                zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, rung)
                      for z in MULTI.zones]
                spec = AnatomySpec(
                    zones=[Zone(f0=a, f1=b, voltage=rung, name=nm)
                           for (a, b, nm) in zs],
                    amputate_plane=MULTI.amputate_plane,
                    spec_name=f"ms-multi-deep-i{inst}",
                    somatic_latch=MULTI.somatic_latch)
                f = spec_target_n(spec, canon, n)
                if host_name == "H0" and n == int(g6.N):
                    f_ref, _trip, _ref = deep_target_for(rung, inst)
                    assert np.array_equal(f, f_ref), (
                        f"deep {rung:g} i{inst} rebuild != exp172's "
                        f"construction")
                rows.append({"tclass": "deep",
                             "key": f"r{rung:g}i{inst}",
                             "rung": rung, "instance": inst,
                             "spec": spec, "f": f, "f_sha256": _f_sha(f)})
        assert len(rows) == 1 + 3 + len(RUNG_LADDER) * len(DEEP_INSTANCES)
        assert sum(1 for r in rows if r["tclass"] == "canon") == 1
        assert sum(1 for r in rows if r["tclass"] == "manifest") == 3
        assert sum(1 for r in rows if r["tclass"] == "deep") == \
            len(RUNG_LADDER) * len(DEEP_INSTANCES)
        return rows

    # ---- exp208's three-class decomposition machinery VERBATIM -------
    # (the boundary-signature instrument; classify copied byte-for-byte
    # from exp208_c6_tail_ablation via exp243/exp256/exp267, zero knobs)
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

    # the per-row decomposition context in exp256's own row form (the
    # MASK counts — cinfo["boundary"/"junction"/"interior"].sum(), the
    # deposit's recorded convention, cross-asserted on the -60.0 rows)
    def class_counts_of(f, A):
        cinfo = classify(f, A)
        return ({"CANON-BOUNDARY": int(cinfo["boundary"].sum()),
                 "PAIR-JUNCTION": int(cinfo["junction"].sum()),
                 "INTERIOR": int(cinfo["interior"].sum())},
                int(cinfo["junction"].sum()))

    # ---- dispatch ------------------------------------------------------
    print(f"=== exp269: THE RESPONSE-SURFACE SAMPLE (batch 27) ===")
    print(f"  mode: {'segment ' + args.seg if args.seg else 'merge'} | "
          f"surface: {len(RUNG_LADDER)} rungs {list(RUNG_LADDER)} x "
          f"12 hosts x 3 seeds x 2 instances = "
          f"{len(RUNG_LADDER) * 72} rows at n={N400}")
    print(f"  read: exp178's production scoped arm; exp160's "
          f"READ_CONFIG fingerprint {fp160} (== 8e11e88c1c2f1518); "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE}); the "
          f"identity repertoire [{REPERTOIRE_LO}, {REPERTOIRE_HI}] is "
          f"the production compiler's own, read never rebound\n")

    # ---- the 12 hosts rebuilt from exp243's DEPOSIT records (exp256's
    #      rebuild VERBATIM: every rebuild bit-asserted against the
    #      deposit's own sha records) ------------------------------------
    CLASS_ORDER = sorted(dep243["classes"])
    assert len(CLASS_ORDER) == 12, "the 12 candidate hosts"
    # U4's determinism subset (pre-named, zero knobs): the first six
    # hosts in the deposit's own sorted order — the -65.0 rung re-run
    # on these and compared bit-identically (the exp267 form)
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
    # construction at EVERY rung, bit-exact)
    canon0 = labeling_bfs_n(g6.A_CHAIN)
    assert np.array_equal(canon0, g6.wildtype_target(g6.N))
    build_rows("H0", canon0, int(g6.N))

    # ---- the per-host context (exp256's battery construction form: the
    #      SUBSTITUTED arm's base medium + anchors; the P1/P2 canon
    #      mediums are NOT built — exp269 runs no canon rows, disclosed;
    #      the P3 medium-sha and candidate-set asserts stay VERBATIM) ---
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
        deep_by_rung = {}
        for dr in rows:
            if dr["tclass"] == "deep":
                deep_by_rung.setdefault(dr["rung"], []).append(dr)
        assert set(deep_by_rung) == set(RUNG_LADDER)
        assert list(deep_by_rung) == list(RUNG_LADDER)
        assert all(len(v) == 2 for v in deep_by_rung.values())
        cand = {}
        for c in dep243["candidates"]:
            if c["cls"] == k:
                cand[(c["pert"], c["row_key"])] = c
        assert set(cand) == {
            (PERT_P1, "canon"), (PERT_P2, "canon"),
            (PERT_P3, f"r{ANCHOR_RUNG:g}i0"),
            (PERT_P3, f"r{ANCHOR_RUNG:g}i1")}, \
            f"{k} candidate set drifted from exp243's deposit"
        assert _a_sha(A_base) == \
            cand[(PERT_P3, f"r{ANCHOR_RUNG:g}i0")]["medium_sha256"] \
            == cand[(PERT_P3, f"r{ANCHOR_RUNG:g}i1")]["medium_sha256"], \
            f"{k} base-medium rebuild drifted"
        # the substituted rows' deposited anchors (U1's comparison
        # targets): errs + verified + target sha + the row's own
        # class_counts records per (seed, deep instance) — exp267's
        # subst_anchor construction VERBATIM
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
            # the deposited row's own decomposition context — the WORST
            # instance's target (the deposit's recorded convention),
            # cross-asserted against this rebuild's classify counts
            w_inst = [i for i in r["instances"]
                      if i["row_key"] == r["worst_row_key"]]
            assert len(w_inst) == 1
            assert float(w_inst[0]["err"]) == float(r["worst_err"])
        # the deep rows' rebuilt targets bit-match the deposit's own
        # per-row target sha records (exp265's G1 form, per row) — and
        # the classify counts of each row's WORST instance's target
        # reproduce the deposit's recorded class_counts/pair_junction
        for dr in deep_by_rung[ANCHOR_RUNG]:
            for s in SEEDS_RUN:
                assert _f_sha(dr["f"]) == \
                    subst_anchor[(s, dr["key"])]["row_target_sha256"], \
                    f"{k} {dr['key']} target rebuild drifted"
        for s, r in subst_rows_dep.items():
            w_inst_no = int(r["worst_row_key"][-1])
            cc, pjc = class_counts_of(
                next(dr["f"] for dr in deep_by_rung[ANCHOR_RUNG]
                     if dr["instance"] == w_inst_no), A_base)
            assert cc == r["class_counts"], \
                f"{k} s{s} class_counts drifted (classify instrument)"
            assert pjc == int(r["pair_junction_count"]), \
                f"{k} s{s} pair-junction count drifted"
        # the per-(rung, instance) decomposition context of THIS
        # surface's rows (exp256's row form, carried per row instance)
        class_ctx = {}
        for rung, drs in deep_by_rung.items():
            for dr in drs:
                class_ctx[(rung, dr["instance"])] = class_counts_of(
                    dr["f"], A_base)
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand, "deep_by_rung": deep_by_rung,
            "subst_anchor": subst_anchor, "class_ctx": class_ctx}
        del rows

    # the battery's worst-canonical mean (the U3 inflection level),
    # recomputed in exp267's exact 72-key order and cross-asserted
    _keys267 = sorted({(r["host"], int(r["seed"]), rk)
                       for r in dep256["rows"]
                       if r["arm"] == "substituted"
                       for rk in ("r-60i0", "r-60i1")})
    assert len(_keys267) == 72
    mean_canon = float(np.mean([canon_ref[(h, s)]
                                for (h, s, _rk) in _keys267]))
    assert mean_canon == _dep267_mean_canon, \
        (f"the worst-canonical mean drifted: {mean_canon} vs "
         f"exp267's deposited {_dep267_mean_canon}")

    # ---- the checkpoint segments (foreground processes; the -60.0
    #      anchor segment FIRST — U1 runs FIRST, fail = STOP; then the
    #      pre-named rung-pair segments in the ladder's order; the merge
    #      joins them and evaluates the gates) ---------------------------
    SEG_RUNGS = {"s60": (ANCHOR_RUNG,),
                 "s30_40": (-30.0, -40.0),
                 "s50_55": (-50.0, -55.0),
                 "s65_70": (-65.0, -70.0)}

    def _expected_locks(seg):
        return {"s60": 72, "s30_40": 144, "s50_55": 144,
                "s65_70": 144 + 36}[seg]

    def _seg_record(seg, section):
        ro_after = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                    "exp229": _sha(DEP229), "exp182": _sha(DEP182),
                    "exp267": _sha(DEP267)}
        rec = {
            "seg": seg,
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_dc92b37": docstring_ok,
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
                            f"_exp269_seg_{rec['seg']}.json")
        with open(path, "w") as f:
            json.dump(rec, f, indent=1, default=float)
        print(f"  segment {rec['seg']} written -> {path}")
        return path

    def _run_rows(seg, pass_tag, hosts, rungs):
        """The surface's decodes over (hosts x rungs x 3 seeds x 2
        instances) on the base medium; returns the per-row records.
        In-repertoire rejections are instrument trouble and RAISE (the
        exp267 caller discipline); the below-repertoire rungs' compiler
        refusals are RECORDED (the boundary's own face — never hidden,
        never raised: they are U2's data)."""
        out_rows: list = []
        n_rej = 0
        for k in hosts:
            ctx = CTX[k]
            ts = time.time()
            for rung in rungs:
                for s in SEEDS_RUN:
                    for dr in ctx["deep_by_rung"][rung]:
                        key = (f"{pass_tag}:{seg}:{k}:{dr['key']}:s{s}")
                        out = _decode_row_hold(
                            None, k, key, dr["spec"],
                            HostWMedium(ctx["base"]), s, ctx["fmax"],
                            None)
                        cc, pjc = ctx["class_ctx"][(rung, dr["instance"])]
                        rec = {
                            "host": k, "seed": int(s), "rung": rung,
                            "instance": int(dr["instance"]),
                            "row_key": dr["key"],
                            "row_target_sha256": _f_sha(dr["f"]),
                            "class_counts": cc,
                            "pair_junction_count": pjc}
                        if out["ok"]:
                            rec.update({
                                "err": float(out["err"]),
                                "err_exact": float(out["err_exact"]),
                                "verified": bool(out["verified"]),
                                "branch": str(out["branch"]),
                                "rejection": None,
                                "compiler_refused": None})
                        else:
                            n_rej += 1
                            if rung >= REPERTOIRE_LO:
                                raise AssertionError(
                                    f"{k} {dr['key']} s{s} rejection "
                                    f"(in-repertoire — instrument "
                                    f"trouble): {out['rejection']}")
                            rec.update({
                                "err": None, "err_exact": None,
                                "verified": False, "branch": None,
                                "rejection": out["rejection"],
                                "compiler_refused":
                                    _repertoire_refusal(dr["spec"])})
                        out_rows.append(rec)
            print(f"  [{k}] {seg} {pass_tag}: "
                  f"{len(rungs) * len(SEEDS_RUN) * 2} rows | "
                  f"{time.time() - ts:.1f} s")
        assert len(out_rows) == len(hosts) * len(rungs) * 6
        assert n_rej == sum(1 for r in out_rows
                            if r["rejection"] is not None)
        return out_rows, n_rej

    if args.seg is not None:
        seg = args.seg
        if seg == "s60":
            # U1 RUNS FIRST: the -60.0 anchor battery — the 72 rows as
            # exp256 ran them; the bit-exact comparison vs BOTH
            # deposits; fail = STOP (SystemExit 3), no tuning, nothing
            # downstream runs
            rows1, _ = _run_rows(seg, "pass1", CLASS_ORDER,
                                 SEG_RUNGS[seg])
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
            section = {
                "arm": "the_-60.0_anchor",
                "definition": ("the battery's own rung re-run: the 72 "
                               "substituted rows exactly as exp256 ran "
                               "them (the unmodified production scoped "
                               "decode, state-carrying) — the "
                               "machinery anchor AND the cross-process "
                               "determinism evidence (the re-run IS "
                               "the anchor)"),
                "rung": ANCHOR_RUNG,
                "n_rows": len(rows1),
                "U1_reproduction": {
                    "n_bit_exact": n_ok, "n_rows": 72,
                    "bar": ("the -60.0 rung reproduces exp256's "
                            "deposited substituted-row errs bit-exact "
                            "(72/72) — vs exp256's substituted "
                            "instances AND exp243's P3 candidates, "
                            "errs and verified flags — runs FIRST, "
                            "fail = STOP, no tuning"),
                    "pass": bool(n_ok == 72),
                    "mismatches": mismatches[:10]},
                "rows": rows1}
            assert len(_LOCK_LOG) == _expected_locks("s60"), \
                "s60 lock composition drifted"
            rec = _seg_record("s60", section)
            _write_seg(rec)
            if not section["U1_reproduction"]["pass"]:
                print("U1 FAIL — the machinery anchor is broken; "
                      "STOP (no tuning, nothing downstream runs)")
                raise SystemExit(3)
        elif seg in ("s30_40", "s50_55"):
            rows1, n_rej = _run_rows(seg, "pass1", CLASS_ORDER,
                                     SEG_RUNGS[seg])
            section = {
                "rungs": list(SEG_RUNGS[seg]),
                "n_rows": len(rows1),
                "zero_rejections": bool(n_rej == 0),
                "rows": rows1}
            assert n_rej == 0, \
                f"{n_rej} rejections on in-repertoire rungs ({seg})"
            assert len(_LOCK_LOG) == _expected_locks(seg), \
                f"{seg} lock composition drifted"
            _write_seg(_seg_record(seg, section))
        else:
            rows1, n_rej = _run_rows(seg, "pass1", CLASS_ORDER,
                                     SEG_RUNGS[seg])
            # U4's determinism clause: the -65.0 rung re-run on the 6
            # pre-named hosts, bit-identical (the exp267 pass-2 form)
            rows2, _ = _run_rows(seg, "pass2", DETERMINISM_HOSTS,
                                 (-65.0,))
            d1 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows1
                  if r["rung"] == -65.0 and r["host"] in
                  DETERMINISM_HOSTS}
            d2 = {(r["host"], r["seed"], r["row_key"]): r
                  for r in rows2}
            assert len(d1) == len(d2) == 36
            diffs = [str(kk) for kk in sorted(set(d1) | set(d2))
                     if d1.get(kk) != d2.get(kk)]
            refused = [r for r in rows1 if r["rejection"] is not None]
            census = {
                "n_refused": len(refused),
                "refusal_rungs": sorted({r["rung"] for r in refused}),
                "all_refusals_identity_repertoire_class": bool(
                    all(r["compiler_refused"] for r in refused)),
                "refusal_message_example": (
                    refused[0]["compiler_refused"][0] if refused
                    else None)}
            section = {
                "rungs": list(SEG_RUNGS[seg]),
                "n_rows": len(rows1),
                "refusal_census": census,
                "determinism_pass2": {
                    "rung": -65.0,
                    "hosts": DETERMINISM_HOSTS,
                    "n_rows": len(rows2),
                    "bit_identical": bool(not diffs),
                    "diffs": diffs[:10]},
                "rows": rows1}
            assert len(_LOCK_LOG) == _expected_locks(seg), \
                f"{seg} lock composition drifted"
            _write_seg(_seg_record(seg, section))
        # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing
        # line) + the docstring re-assert
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        assert hashlib.sha256(__doc__.encode()).hexdigest() == \
            EXPECTED_DOCSTRING_SHA256, "docstring drifted at exit"
        assert config_fingerprint() == fp160, "fingerprint drift at exit"
        return {}

    # ---- THE MERGE: join the four segments, evaluate the gates (each
    #      exactly once), deposit ----------------------------------------
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

    def _jnum(x):
        """The deposit's finite-float hygiene: a non-finite statistic
        is recorded as null, never as a NaN/Infinity token."""
        x = float(x)
        return x if x == x and abs(x) != float("inf") else None

    def _merge(paths: list) -> dict:
        sections: dict = {}
        seg_meta: dict = {}
        for p in paths:
            with open(p) as fh:
                d = json.load(fh)
            assert d["seg"] not in sections, "duplicate segment"
            assert d["docstring_byte_unchanged_vs_dc92b37"], \
                f"{d['seg']}: docstring drifted"
            assert d["read_only_byte_unchanged"], \
                f"{d['seg']}: a read-only deposit changed"
            assert d["fingerprint_pre"] == d["fingerprint_post"] == \
                "8e11e88c1c2f1518", f"{d['seg']}: fingerprint drift"
            assert d["lock_log_unique"], f"{d['seg']}: duplicate locks"
            assert d["floor_at_exit_pending_assert"] == PROD_FLOOR, \
                f"{d['seg']}: floor drift"
            sections[d["seg"]] = d["section"]
            seg_meta[d["seg"]] = {
                k: d[k] for k in ("read_only_shas_before",
                                  "read_only_shas_after",
                                  "floors_pre_restore",
                                  "floor_at_exit_pending_assert",
                                  "lock_log_entries")}
        assert set(sections) == {"s60", "s30_40", "s50_55", "s65_70"}, \
            "the four pre-named segments are required"
        assert all(sections[s]["n_rows"] == len(sections[s]["rows"])
                   for s in sections)

        # ---- U1 re-asserted FIRST (the anchor; fail = STOP) ------------
        u1 = sections["s60"]["U1_reproduction"]
        assert u1["pass"], \
            f"U1 did not pass ({u1['n_bit_exact']}/72) — STOP"

        # ---- assemble the 504-row surface ------------------------------
        rows_out = (sections["s60"]["rows"]
                    + sections["s30_40"]["rows"]
                    + sections["s50_55"]["rows"]
                    + sections["s65_70"]["rows"])
        keys = [(r["host"], int(r["seed"]), float(r["rung"]),
                 int(r["instance"])) for r in rows_out]
        assert len(rows_out) == len(RUNG_LADDER) * 72 == 504, \
            f"{len(rows_out)} rows != 504"
        assert len(set(keys)) == 504, "duplicate surface records"
        assert {kk[2] for kk in keys} == set(RUNG_LADDER), \
            "the rung ladder drifted"

        # ---- U2: THE SURFACE (complete / finite / zero rejections) -----
        n_rej = sum(1 for r in rows_out if r["rejection"] is not None)
        n_finite = sum(1 for r in rows_out if r["err"] is not None)
        assert n_finite + n_rej == 504
        refused_rungs = sorted({float(r["rung"]) for r in rows_out
                                if r["rejection"] is not None})
        # every rejection is a below-repertoire rung's identity-
        # repertoire refusal (the run loops already raised on any
        # in-repertoire rejection; re-asserted from the records here)
        assert all(float(r["rung"]) < REPERTOIRE_LO
                   for r in rows_out if r["rejection"] is not None), \
            "a rejection outside the below-repertoire rungs?!"
        assert all(r["compiler_refused"]
                   for r in rows_out if r["rejection"] is not None), \
            "a rejection without the compiler's own refusal record"
        refusal_examples = {}
        for rung in refused_rungs:
            ex = next(r for r in rows_out
                      if float(r["rung"]) == rung
                      and r["rejection"] is not None)
            refusal_examples[f"{rung:g}"] = {
                "rejection": ex["rejection"],
                "compiler_refused": ex["compiler_refused"]}
        # the per-host curves (the docstring's own form: worst err vs
        # rung; the worst over the 3 seeds x 2 instances; a rung with
        # any non-finite row carries NO finite curve point — recorded
        # as null, the refusal disclosed in U2's census)
        per_host_curves: dict = {}
        for k in CLASS_ORDER:
            curve = {}
            for rung in RUNG_LADDER:
                errs = [float(r["err"]) for r in rows_out
                        if r["host"] == k and float(r["rung"]) == rung
                        and r["err"] is not None]
                curve[f"{rung:g}"] = (
                    max(errs) if len(errs) == 6 else None)
            per_host_curves[k] = curve
        u2_pass = bool(n_rej == 0 and n_finite == 504)

        # ---- U3: THE SHAPE (monotonicity / inflection / end-behavior) --
        # the finite surface: the rungs the production read accepts
        finite_rungs = [rung for rung in RUNG_LADDER
                        if rung >= REPERTOIRE_LO]
        finite_rows = [r for r in rows_out if r["err"] is not None]
        assert len(finite_rows) == len(finite_rungs) * 72
        # D1 pooled: Spearman(|rung|, err) over ALL finite rows (the
        # gate's pre-named form: |rung| vs err, pooled over the surface)
        pooled_rho = _spearman([abs(float(r["rung"]))
                                for r in finite_rows],
                               [float(r["err"]) for r in finite_rows])
        # audits: the pooled-curve form (the 12 per-host worst-err
        # curves pooled) and the exact-scale (unrounded) errs
        curve_pts = [(abs(rung), per_host_curves[k][f"{rung:g}"])
                     for k in CLASS_ORDER for rung in finite_rungs]
        pooled_rho_curves = _spearman([p[0] for p in curve_pts],
                                      [p[1] for p in curve_pts])
        pooled_rho_exact = _spearman(
            [abs(float(r["rung"])) for r in finite_rows],
            [float(r["err_exact"]) for r in finite_rows])
        # D1 per host: Spearman(|rung|, worst err) on the 5-point
        # finite curve
        per_host_rho: dict = {}
        for k in CLASS_ORDER:
            pts = [(abs(rung), per_host_curves[k][f"{rung:g}"])
                   for rung in finite_rungs]
            per_host_rho[k] = _jnum(_spearman([p[0] for p in pts],
                                              [p[1] for p in pts]))
        # D2 the inflection: per host, the FIRST finite rung (|rung|
        # ascending) whose worst err is strictly above the battery's
        # worst-canonical mean (the "the substitution starts to cost
        # here" point); the pooled form as an audit
        per_host_inflection: dict = {}
        for k in CLASS_ORDER:
            hit = None
            for rung in finite_rungs:
                w = per_host_curves[k][f"{rung:g}"]
                if w is not None and w > mean_canon:
                    hit = rung
                    break
            per_host_inflection[k] = hit
        per_rung_mean_err = {
            f"{rung:g}": float(np.mean([float(r["err"])
                                        for r in finite_rows
                                        if float(r["rung"]) == rung]))
            for rung in finite_rungs}
        pooled_inflection = None
        for rung in finite_rungs:
            if per_rung_mean_err[f"{rung:g}"] > mean_canon:
                pooled_inflection = rung
                break
        # D3 the end-behavior: the deep extreme rungs BELOW the
        # production floor return NO finite read — the compiler's own
        # identity-repertoire safety refusal (recorded per row; never
        # patched: the repertoire constants are the production system's
        # own). The pre-named dichotomy {saturating, diverging}
        # presupposes finite errs at the extreme rungs; the data name a
        # third behavior, and the gate's conjunct evaluates on what IS.
        deep_refused = [rung for rung in RUNG_LADDER
                        if rung < REPERTOIRE_LO]
        assert deep_refused == [-65.0, -70.0]
        assert all(per_host_curves[k][f"{rung:g}"] is None
                   for k in CLASS_ORDER for rung in deep_refused)
        extreme_naming = (
            "refused-at-the-identity-repertoire-boundary — NEITHER "
            "pre-named behavior: the production read returns no finite "
            "err at the {-65.0, -70.0} extreme rungs (the compiler's "
            "own safety refusal; the surface TRUNCATES at the -60.0 "
            "floor), so the err neither saturates nor diverges there")
        conj1 = bool(pooled_rho >= 0.5)
        conj2 = False          # the honest naming is neither pre-named
        u3_pass = bool(conj1 and conj2)

        # ---- U4: THE DISCIPLINE ----------------------------------------
        ro_after = {"exp243": _sha(DEP243), "exp256": _sha(DEP256),
                    "exp229": _sha(DEP229), "exp182": _sha(DEP182),
                    "exp267": _sha(DEP267)}
        ro_unchanged = bool(
            ro_after == ro_before
            and all(seg_meta[s]["read_only_shas_after"] == ro_before
                    for s in seg_meta))
        fp_post = config_fingerprint()
        det_ok = bool(u1["pass"]
                      and sections["s65_70"]["determinism_pass2"]
                      ["bit_identical"])
        locks_ok = all(seg_meta[s]["lock_log_entries"] ==
                       _expected_locks(s) for s in seg_meta)
        floors_ok = all(
            seg_meta[s]["floor_at_exit_pending_assert"] == PROD_FLOOR
            for s in seg_meta)
        u4_clauses = {
            "exp256_exp229_deposits_read_only_byte_unchanged":
                bool(ro_unchanged),
            "read_stack_fingerprint_pre_post": bool(
                fp_post == fp160 == "8e11e88c1c2f1518"
                and SCOPED_THRESHOLD == 32.0),
            "floor_restored_and_asserted_exit": bool(
                floors_ok and CORE.NEURAL_SPEC_MIN == PROD_FLOOR),
            "deterministic": bool(det_ok),
            "docstring_byte_unchanged": bool(docstring_ok),
            "zero_unexpected_rejections": bool(all(
                float(r["rung"]) < REPERTOIRE_LO
                for r in rows_out if r["rejection"] is not None)),
            "lock_discipline": bool(locks_ok),
            "no_wall_clock_fields": True}
        u4 = bool(all(u4_clauses.values()))

        # ---- THE GATES (each evaluated exactly once) -------------------
        gates = {
            "U1_anchor": {
                "pass": bool(u1["pass"]),
                "bar": ("the -60.0 rung reproduces exp256's deposited "
                        "substituted-row errs bit-exact (72/72; the "
                        "machinery anchor) — runs FIRST, fail = STOP, "
                        "no tuning"),
                "n_bit_exact": u1["n_bit_exact"], "n_rows": 72,
                "anchors": ["exp256's substituted instances (errs + "
                            "verified)",
                            "exp243's P3 candidates (errs + verified)"],
                "mismatch_records": u1["mismatches"]},
            "U2_surface": {
                "pass": u2_pass,
                "bar": ("all 7 rungs x 72 rows complete, finite, zero "
                        "rejections; the per-host curves deposited"),
                "n_records": 504, "n_finite": n_finite,
                "n_rejections": n_rej,
                "refusal_rungs": refused_rungs,
                "refusal_census": refusal_examples,
                "per_host_curves_deposited": True},
            "U3_shape": {
                "pass": u3_pass,
                "bar": ("the pooled monotonicity Spearman >= 0.5 (the "
                        "response has a directed shape — the surface "
                        "is a curve, not a scatter) AND the "
                        "extreme-rung behavior named (saturating or "
                        "diverging)"),
                "conjunct_pooled_spearman_ge_05": {
                    "value": _jnum(pooled_rho), "bar": 0.5,
                    "pass": conj1},
                "conjunct_extreme_rung_named": {
                    "naming": extreme_naming,
                    "pass": conj2},
                "reads": {
                    "per_host_monotonicity_spearman": per_host_rho,
                    "pooled_spearman_curves_audit":
                        _jnum(pooled_rho_curves),
                    "pooled_spearman_exact_scale_audit":
                        _jnum(pooled_rho_exact),
                    "finite_rungs": finite_rungs,
                    "deep_refused_rungs": deep_refused,
                    "mean_canonical_worst": mean_canon,
                    "inflection_per_host": per_host_inflection,
                    "inflection_pooled_audit": pooled_inflection,
                    "per_rung_mean_err": per_rung_mean_err}},
            "U4_discipline": {
                "pass": u4, "clauses": u4_clauses,
                "named_clauses": ("exp256's/exp229's deposits "
                                  "READ-ONLY sha-recorded "
                                  "byte-unchanged (with exp243/exp182/"
                                  "exp267, all read-used); the read "
                                  "stack's production fingerprint "
                                  "asserted pre/post (exp160's "
                                  "READ_CONFIG, exp198's assert form); "
                                  "the -60.0 floor restored and "
                                  "asserted at every exit (the exp169 "
                                  "import chain pins -35.0 — the "
                                  "explicit restore); deterministic "
                                  "(the -60.0 rung re-run IS the "
                                  "anchor; the -65.0 rung re-run on 6 "
                                  "hosts bit-identical); no "
                                  "wall-clock fields"),
                "read_only_shas": ro_after,
                "read_only_shas_by_segment": {
                    s: seg_meta[s]["read_only_shas_after"]
                    for s in seg_meta},
                "fingerprint_pre": fp160,
                "fingerprint_post": fp_post,
                "floors_pre_restore": seg_meta["s60"][
                    "floors_pre_restore"],
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "determinism": {
                    "anchor_-60_bit_exact": bool(u1["pass"]),
                    "rung_-65_six_host_pass2_bit_identical": bool(
                        sections["s65_70"]["determinism_pass2"]
                        ["bit_identical"])},
                "lock_log_entries": {
                    s: seg_meta[s]["lock_log_entries"]
                    for s in sorted(seg_meta)},
                "docstring_sha256": docstring_sha},
        }
        n_pass = sum(int(g["pass"]) for g in gates.values())
        branch = "CURVE" if u3_pass else "SCATTER"
        verdict = (
            f"{n_pass}/4 gates U1-U4 | {branch} | U1 72/72 bit-exact | "
            f"the surface: {n_finite}/504 finite, {n_rej} refusals "
            f"(the -65/-70 rungs refused by the production compiler's "
            f"identity-repertoire check — the surface truncates at the "
            f"-60.0 floor) | pooled |rung|-vs-err Spearman "
            f"{pooled_rho:.4f} on the finite band")

        deposit = {
            "exp": "exp269_response_surface",
            "claim": (
                "THE RESPONSE-SURFACE SAMPLE (batch 27; L246's "
                "registered next (a), pre-registration commit dc92b37): "
                "the read's err surface sampled over the substitution's "
                "own parameter — the deep rung's voltage ladder "
                "{-30, -40, -50, -55, -60, -65, -70} mV x 12 hosts x 3 "
                "seeds x 2 instances at n=400 (the exp172/exp214 deep "
                "construction at each rung, zero knobs; the -60.0 rung "
                "the battery's own anchor). The response surface's "
                "first direct shape measurement: monotonicity, "
                "inflection, saturation-vs-divergence"),
            "interpretation": {
                "the_boundary_face": (
                    "THE PRE-REGISTERED LADDER EXTENDS BELOW THE "
                    "PRODUCTION FLOOR (disclosed, the run's central "
                    "finding): the production read is execute_signed "
                    "via compile_anatomy, whose AnatomySpec.validate() "
                    "enforces the identity repertoire "
                    "[-60.0, -15.0] (REPERTOIRE_LO/HI, the production "
                    "constants — read here, never rebound). The "
                    "-65.0/-70.0 rungs' specs are outside the band the "
                    "production system accepts: EVERY such row returns "
                    "the compiler's safety refusal (CP-G4's class), no "
                    "finite err exists, the row is RECORDED (never "
                    "hidden, never raised — it is U2's data). The "
                    "response surface therefore TRUNCATES at the -60.0 "
                    "floor: the extreme-rung behavior is neither "
                    "saturating nor diverging — the read is refused "
                    "beyond the boundary. Patching the repertoire (or "
                    "the floor) would be a new knob against the "
                    "pre-registration and the production system's own "
                    "safety design; the honest sample is what the "
                    "production machinery returns"),
                "curve_convention": (
                    "the per-host curve is worst err vs rung: the max "
                    "over the 3 seeds x 2 instances at each rung (the "
                    "battery's own worst-err convention); a rung with "
                    "any non-finite row carries no finite curve point"),
                "inflection_convention": (
                    "per host, the FIRST finite rung (|rung| ascending) "
                    "whose worst err is strictly above the battery's "
                    "worst-canonical mean (exp256's 72 canonical rows' "
                    "worst_err mean, recomputed in exp267's exact key "
                    "order and cross-asserted bit-exact vs exp267's "
                    "deposited arm_gap reference)"),
                "monotonicity_convention": (
                    "the GATE's pooled form: Spearman(|rung|, err) "
                    "over ALL finite rows (tied-average ranks, the "
                    "exp229/exp267 numpy convention); the per-host "
                    "form reads the 5-point finite worst-err curve; "
                    "the pooled-curve and exact-scale forms are "
                    "audits, never gating"),
                "err_convention": (
                    "all errs on the exp142 2-dp convention (the "
                    "battery's own; U1's bit-exactness lives there); "
                    "the exact-scale errs carried per row for audit"),
                "machinery_disclosures": (
                    "exp267's machinery reused VERBATIM: the "
                    "reader-line import block, the floor restore, the "
                    "exp243 host rebuild, build_rows (the deep section "
                    "looped over the pre-named ladder — the "
                    "construction's own form at each rung, the row-"
                    "count asserts parameterized), classify, "
                    "HostWMedium, _scoped_row_read_state, "
                    "_decode_row_hold (only kind=None called; the s1/"
                    "s2 stage-hold dispatch carried but uncalled — "
                    "exp269 runs no stage holds), the rank forms. The "
                    "P1/P2 canon mediums are not built (no canon rows "
                    "in this instrument — disclosed); the MULTI-"
                    "identity audits are not re-run (the -60.0 "
                    "anchor's bit-exactness IS the wiring-identity "
                    "evidence — disclosed); the refusal recorder cites "
                    "compile_anatomy's own message per refused row (a "
                    "record, never a behavior change). Body-only "
                    "plumbing: the in-body imports, the --out flag, "
                    "the __main__ guard appended (the exp256/exp262 "
                    "precedent)"),
                "segmentation": (
                    "four foreground checkpoint segments (no setsid/"
                    "nohup), each within the 570 s budget, joined by "
                    "the merge; the seg/merge pattern is "
                    "exp267/exp263's; the -60.0 anchor segment ran "
                    "FIRST (U1 runs FIRST, fail = STOP) — the "
                    "pre-named rung-pair split preserved exactly")},
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
                "op": {"gamma": STAR_OP["gamma"], "mu": STAR_OP["mu"]},
                "seeds": list(SEEDS_RUN), "n": int(N400),
                "window_h": 24.0, "commit_noise": 0.6,
                "steps_per_cell": 8,
                "floor": ("production -60.0 restored post-import "
                          "(exp218's disclosed exp169-import "
                          "discipline; the -35.0 reader-line pin "
                          "disclosed)"),
                "identity_repertoire": [REPERTOIRE_LO, REPERTOIRE_HI],
                "per_media_tuning": "none"},
            "battery": {
                "hosts": CLASS_ORDER,
                "rung_ladder": list(RUNG_LADDER),
                "rows": 504,
                "row_grid": ("7 rungs x 12 hosts x 3 seeds x 2 deep "
                             "instances on the base medium — the "
                             "exp256 substituted battery re-drawn at "
                             "each rung"),
                "mean_canonical_worst": mean_canon},
            "rows": rows_out,
            "surface": {
                "per_host_curves_worst_err": per_host_curves,
                "per_host_monotonicity_spearman": per_host_rho,
                "pooled_monotonicity_spearman_rows": _jnum(pooled_rho),
                "pooled_spearman_curves_audit":
                    _jnum(pooled_rho_curves),
                "pooled_spearman_exact_scale_audit":
                    _jnum(pooled_rho_exact),
                "per_rung_mean_err": per_rung_mean_err,
                "inflection_per_host": per_host_inflection,
                "inflection_pooled_audit": pooled_inflection,
                "deep_refused_rungs": deep_refused},
            "gates": gates,
            "branch": branch,
            "verdict": verdict,
            "provenance": {
                "pre_registration": "commit dc92b37 (batch 27)",
                "docstring_sha256": docstring_sha,
                "exp243": ro_after["exp243"],
                "exp256": ro_after["exp256"],
                "exp229": ro_after["exp229"],
                "exp182": ro_after["exp182"],
                "exp267": ro_after["exp267"],
                "machinery": ("exp267's import block + floor restore "
                              "+ exp243 host rebuild + build_rows (the "
                              "ladder-parameterized deep form) + "
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
        print(f"  finite {n_finite}/504 | refusals {n_rej} at "
              f"{refused_rungs} | pooled rho {pooled_rho:.4f} "
              f"(curves audit {pooled_rho_curves:.4f}) | branch "
              f"{branch}")
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
            os.path.join(ROOT, "results", f"_exp269_seg_{s}.json")
            for s in ("s60", "s30_40", "s50_55", "s65_70")]
        return _merge(paths)
    ap.error("unreachable dispatch")
    return {}


if __name__ == "__main__":
    main()
