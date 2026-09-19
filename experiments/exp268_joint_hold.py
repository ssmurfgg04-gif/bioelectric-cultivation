#!/usr/bin/env python3
"""exp268 — THE JOINT HOLD (batch 26 item 2; L245's registered next —
the S1 x S3 stages canonicalized SIMULTANEOUSLY).

THE OPEN ITEM (L245): the arm contrast's stage shares are the
projection 0.4406 and the executor 0.1990 (jointly 0.64) with 0.3604
unexplained by any single stage. The joint hold decides between:
(a) the INTERACTION is the carrier — holding both stages closes the
contrast beyond the sum of the singles; (b) the 0.36 is the joint's
irreducible face.

THE INSTRUMENT (pre-registered, zero-knob; exp267's machinery
verbatim): the J arm — both the projection (PN1/PN2 from the canon
row's medium) and the executor (the canon row's A_ext walk with the
substituted row's target at the error read) held simultaneously, on
the same 72 rows (12 hosts x 3 seeds x 2 deep instances). The
comparison set: exp267's deposited S0/S1/S3 rows (the singles) and
the fresh J rows.

PRE-REGISTERED GATES:

  J1  THE ANCHORS: S0 and the singles re-read from exp267's deposit
      (byte-verified); the J arm's canon-row reference decodes
      reproduce exp256's/exp267's canon anchors bit-exact.
  J2  THE JOINT CLOSURE: the joint hold's delta share (S0 - J)
      computed by the exp262 convention; the gate: the joint share
      >= 0.5 AND exceeds max(single shares) + 0.10 (the interaction
      adds beyond the dominant single — the carrier is the JOINT).
  J3  THE IRREDUCIBLE FACE: the residual after the joint hold (the
      share of (S0 - J) NOT explained — i.e. 1 - joint share)
      reported; if J2 fails, the branch names the honest reading:
      either the singles' sum already saturates (joint ~ max single)
      or the contrast survives both stages (the read's response is
      not stage-decomposable at all).
  J4  THE DISCIPLINE: exp267's/exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (J re-run on 6 hosts, bit-identical); no
      wall-clock fields.

THE BRANCHES (pre-named): JOINT-CARRIES (J2) / SATURATED / NOT-
STAGE-DECOMPOSABLE — each names the residual's final disposition at
the read-stack level honestly.

RUN: 72 J rows at n=400 (~1.3 s/row); foreground segment.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp268_joint_hold.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates J1-J4 below evaluated exactly once,
    #      pre-registration commit a0ce3ba) ==================================
    import argparse
    import hashlib
    import json
    import time

    import numpy as np
    from scipy.stats import rankdata

    # ---- the docstring gate, FIRST in every process (segment, merge):
    #      the docstring is the a0ce3ba pre-registration, byte-for-byte;
    #      fail = STOP before anything runs (the hard rule; the sha is
    #      of the RAW module __doc__ — the exact literal, trailing
    #      newline included, as imported) ---------------
    EXPECTED_DOCSTRING_SHA256 = (
        "fbca45d64a24f1270b5e80cbc4dcc878017f3b06c140f4b88ebbf9cbd397e24a")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    assert docstring_ok, "docstring drifted from a0ce3ba"

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["j"], default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    if args.seg is None and args.merge is None:
        ap.error("one of --seg / --merge is required (the checkpoint "
                 "split: one foreground segment for the J arm, merge at "
                 "the end — the exp267/exp263/exp261 pattern; no "
                 "setsid/nohup)")

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

    DEP267 = os.path.join(ROOT, "results",
                          "exp267_read_stage_attribution.json")
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
    for _p in (DEP267, DEP243, DEP256, DEP229, DEP262, DEP182):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    # the aux checkpoint files of exp267's own run (UNTRACKED on-disk
    # records, present this run; read-only, sha-recorded; their
    # cross-checks are SECONDARY evidence — the tracked deposits alone
    # carry J1's pre-registered anchors)
    AUX_SEG0 = os.path.join(ROOT, "results", "_exp267_seg_s0.json")
    AUX_SEG1 = os.path.join(ROOT, "results", "_exp267_seg_s1.json")
    AUX_SEG3 = os.path.join(ROOT, "results", "_exp267_seg_s3.json")

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    # J4: the deposits READ-ONLY — shas taken BEFORE any read, re-verified
    # byte-unchanged at every process exit and at the merge, recorded in
    # the deposit (J4 names exp267/exp256/exp229; exp243/exp262/exp182
    # are read for the host rebuild / convention reference and recorded
    # with them; the exp267 aux segments are recorded when present)
    ro_names = ["exp267", "exp243", "exp256", "exp229", "exp262", "exp182"]
    ro_paths = {"exp267": DEP267, "exp243": DEP243, "exp256": DEP256,
                "exp229": DEP229, "exp262": DEP262, "exp182": DEP182}
    for _nm, _p in (("aux_exp267_seg_s0", AUX_SEG0),
                    ("aux_exp267_seg_s1", AUX_SEG1),
                    ("aux_exp267_seg_s3", AUX_SEG3)):
        if os.path.exists(_p):
            ro_names.append(_nm)
            ro_paths[_nm] = _p

    def _ro():
        return {nm: _sha(ro_paths[nm]) for nm in ro_names}

    ro_before = _ro()
    with open(DEP267) as fh:
        dep267 = json.load(fh)
    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    with open(DEP262) as fh:
        dep262 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)
    aux = {}
    for nm, p in (("s0", AUX_SEG0), ("s1", AUX_SEG1), ("s3", AUX_SEG3)):
        aux[nm] = json.load(open(p)) if os.path.exists(p) else None

    # the context anchors (the docstring's open item): exp262's deposited
    # arm share, and exp267's deposited singles — the exact numbers the
    # docstring quotes (the J2 comparison set, byte-pinned here)
    arm_share_262 = float(
        dep262["attribution"]["shares_of_rank_variance"]["arm"])
    assert round(arm_share_262, 4) == 0.7570, \
        f"exp262's deposited arm share drifted: {arm_share_262}"
    shares_267 = {k: float(v) for k, v in dep267["gates"][
        "R2_attribution"]["shares_of_rank_variance"].items()}
    assert set(shares_267) == {"S1", "S2", "S3"}, "the deposited singles"
    assert round(shares_267["S1"], 4) == 0.4406, \
        "the docstring's projection single drifted"
    assert round(shares_267["S3"], 4) == 0.1990, \
        "the docstring's executor single drifted"
    assert shares_267["S2"] == 0.0, "the flip-clock single drifted"
    unexpl_267 = float(dep267["gates"]["R2_attribution"]["unexplained"])
    assert round(unexpl_267, 4) == 0.3604, \
        "the docstring's unexplained face drifted"
    assert bool(dep267["gates"]["R1_reproduction"]["pass"]), \
        "exp267's own machinery anchor did not pass"
    assert dep267["provenance"]["docstring_sha256"] == \
        "2de8f5267babc391ba6201ddcac24aa06cd87fa36fef5a7404e0b4971aaa56fc", \
        "exp267's pre-registration sha drifted"
    assert dep267["branch"] == "DISTRIBUTED", "exp267's branch drifted"

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

    # ---- THE J ARM'S REPLICA: _scoped_row_read_state_s1 VERBATIM (the
    #      projection swap line included, uncalled base above) with
    #      EXACTLY ONE additional swap line — the executor stage's
    #      output replaced by the canon row's walk (the S3 hold's
    #      value). The two pre-registered holds compose into this one
    #      replica: the projection hold fixes the executor's input (the
    #      canon row's A_ext — the battery's flip-clock stage is the
    #      VERIFIED structural zero, asserted per host per medium
    #      below, so the held A_ext IS the canon row's A_ext), and the
    #      executor hold fixes the walk's output; the error read uses
    #      the substituted row's target (S3's swap). The substituted
    #      walk still runs (the verbatim body shape; its output is
    #      discarded by hold (ii)) — its err is the S1 arm's decode,
    #      recorded per row and asserted bit-exact against exp267's
    #      deposited S1 rows (the within-run S1 reproduction). -------
    def _scoped_row_read_state_joint(spec, med, seed, fmax, A_held,
                                     V_exec_held, target_sub):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)
                F = flip_clock_matrix(inner)
            else:
                A, rho, branch = project_phase_native(med)
                F = flip_clock_matrix(med)
            A = A_held                    # THE JOINT HOLD (i): the
                                          # projection stage's output
                                          # (PN1/PN2 on the canon row's
                                          # medium) replaces the
                                          # substituted medium's own
                                          # projection — S1's swap line,
                                          # VERBATIM
            A_ext = A + F
            assert not np.iscomplexobj(A_ext)
            out = execute_signed(spec, A_ext, seed, op=STAR_OP,
                                 return_state=True)
            V = np.asarray(V_exec_held, dtype=float)
            # THE JOINT HOLD (ii): the executor stage's output (the
            # canon row's A_ext walk — the canon decode's final state,
            # same seed) replaces the substituted walk's output — S3's
            # hold; the substituted walk's output above is discarded.
            T = np.asarray(target_sub, dtype=float)
            err_joint = float(round(float(np.sqrt(np.mean(
                (V - T) ** 2))), 2))
            s1_V = np.asarray(out["final_state"]["V"], dtype=float)
            s1_T = np.asarray(out["final_state"]["target"], dtype=float)
            s1_walk_err = float(out["err_vs_target"])
            s1_walk_exact = float(np.sqrt(np.mean((s1_V - s1_T) ** 2)))
        return {"err_vs_target": err_joint,
                "final_state": {"V": V.tolist(), "target": T.tolist()},
                "s1_walk_err": s1_walk_err,
                "s1_walk_exact": s1_walk_exact,
                "rho": rho, "branch": branch}

    def _decode_row_hold(kind, host, row_key, spec, med, seed, fmax,
                         held):
        """One state-carrying decode (kind None = exp256's verbatim S0
        path — the J arm's canon decode; "s1"/"s2" = the stage-hold
        replicas above, carried VERBATIM as the declared diff-bases);
        a rejection is RECORDED, never hidden (exp142's zero-rejection
        hygiene; the caller raises) — exp243's _decode_row at the
        state-carrying call site, with the A3 state-convention assert
        (the recomputed RMS matches the reported err at the exp142 2-dp
        convention)."""
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

    def _decode_row_joint(host, row_key, spec, med, seed, fmax, A_held,
                          V_exec_held, target_sub, canon_verified):
        """One JOINT-hold decode (the J replica above); a rejection is
        RECORDED, never hidden (exp142's zero-rejection hygiene; the
        caller raises) — exp243's _decode_row discipline at the joint
        call site, with the state-convention assert (the recomputed RMS
        vs the SUBSTITUTED target matches the reported err at the
        exp142 2-dp convention). The recorded verified flag is the held
        executor state's OWN decode's flag (the canon decode's —
        anchored bit-exact by the caller); the J row's output state IS
        that decode's state (disclosed)."""
        _lock_read(host, row_key, seed)
        try:
            out = _scoped_row_read_state_joint(
                spec, med, seed, fmax, A_held, V_exec_held, target_sub)
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
                    "s1_walk_err": float(out["s1_walk_err"]),
                    "s1_walk_exact": float(out["s1_walk_exact"]),
                    "rho": float(out["rho"]),
                    "branch": str(out["branch"]),
                    "verified": bool(canon_verified)}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- the per-class target rows (exp225's build_rows VERBATIM,
    #      exp227's disclosed n-parameterization of the two deposited
    #      checksum asserts — fired on the n=100 H0 rebuild only) ------
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
    print(f"=== exp268: THE JOINT HOLD (batch 26 item 2) ===")
    print(f"  mode: {'segment ' + args.seg if args.seg else 'merge'} | "
          f"battery: 12 hosts x 3 seeds x 2 deep instances = 72 "
          f"substituted rows at n={N400}")
    print(f"  arm: J — the projection (PN1/PN2 from the canon row's "
          f"medium) AND the executor (the canon row's A_ext walk, the "
          f"substituted row's target at the error read) held "
          f"SIMULTANEOUSLY (the S1 x S3 combination)")
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
    # J4's determinism subset (pre-named, zero knobs): the first six
    # hosts in the deposit's own sorted order — the J arm re-run on
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

    # the exp267 aux segments' row indexes (secondary evidence; absent
    # files degrade to None — the tracked deposits alone carry J1)
    def _aux_index(nm):
        if aux[nm] is None:
            return {}
        return {(r["host"], int(r["seed"]), r["row_key"]): r
                for r in aux[nm]["section"]["rows"]}
    AUX0, AUX1, AUX3 = _aux_index("s0"), _aux_index("s1"), \
        _aux_index("s3")

    # ---- the per-host context (exp256's battery construction, the
    #      SUBSTITUTED arm + the canon decode's media; the canonical
    #      arm's P1/P2 decode mediums are exp256's OWN DEPOSITED
    #      worst_medium records — see the interpretation note) -----------
    CTX: dict = {}
    J1_ROWS = {"ok": 0, "n": 0, "mismatches": []}
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
            # the J arm's canon-decode anchor (bit-exact reproduction)
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
        # the substituted rows' deposited anchors (J1's comparison
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
            # THE J ARM'S ANCHOR ADDITION (disclosed): the canon row's
            # stage outputs byte-verified against exp267's deposited
            # per-host records — the S1 hold's value (A) and the
            # composition's zero-F partner are the DEPOSIT's values
            dep_st = dep267["battery"][
                "canon_stage_outputs_sha256"][k][med_name]
            assert stage_out[med_name]["A_sha256"] == dep_st["A"], \
                f"{k} {med_name} canon projection sha drifted"
            assert stage_out[med_name]["F_sha256"] == dep_st["F"], \
                f"{k} {med_name} canon flip-clock sha drifted"
            assert stage_out[med_name]["rho"] == float(dep_st["rho"]) \
                and stage_out[med_name]["branch"] == dep_st["branch"], \
                f"{k} {med_name} canon projection metadata drifted"
        # ---- THE J ARM'S J1 ANCHOR ADDITIONS (disclosed): exp267's
        #      deposited S0/S1/S3 rows byte-verified (J1's first
        #      clause) — the S0 rows vs BOTH underlying deposits
        #      bit-exact, the canon-medium records and the canonical
        #      anchors across all three deposits, the S1/S3 rows vs
        #      exp267's own aux checkpoint records (when present), and
        #      the S1 hold's value sha vs the s1 segment's records ----
        dep267_rows = {}
        for r267 in dep267["rows"]:
            if r267["host"] == k:
                dep267_rows[(int(r267["seed"]), r267["row_key"])] = r267
        assert sorted(dep267_rows) == sorted(subst_anchor), \
            f"{k}: exp267's deposited row grid drifted"
        held_A_sha_by_medium: dict = {}
        for (s, rk), r267 in sorted(dep267_rows.items()):
            anch = subst_anchor[(s, rk)]
            cand_rec = cand[(PERT_P3, rk)]
            d243_err = float(
                cand_rec["errs"][SEEDS_RUN.index(s)])
            d243_ver = bool(
                cand_rec["verified"][SEEDS_RUN.index(s)])
            cm = canon_medium_by_seed[s]
            checks = {
                "S0_vs_dep256": float(r267["S0"]) == anch["err"],
                "S0_vs_dep243": float(r267["S0"]) == d243_err,
                "S0_verified": bool(r267["S0_verified"]) ==
                    anch["verified"] == d243_ver,
                "canon_medium_agrees":
                    r267["canon_medium"] == cm["medium"],
                "canon_anchor_dep267":
                    float(r267["canonical_row_worst_err"]) ==
                    cm["dep_err"],
                "S0_exact_pair":
                    round(float(r267["S0_exact"]), 2) ==
                    float(r267["S0"])}
            kk3 = (k, s, rk)
            if AUX3:
                a3 = AUX3.get(kk3)
                checks["S3_vs_aux_seg3"] = (
                    a3 is not None
                    and float(r267["S3"]) == float(a3["err"])
                    and float(r267["S3_exact"]) ==
                        float(a3["err_exact"])
                    and float(a3["canon_decode_err"]) == cm["dep_err"]
                    and a3["canon_medium"] == r267["canon_medium"]
                    and a3["row_target_sha256"] ==
                        anch["row_target_sha256"])
            if AUX1:
                a1 = AUX1.get(kk3)
                checks["S1_vs_aux_seg1"] = (
                    a1 is not None
                    and float(r267["S1"]) == float(a1["err"])
                    and float(r267["S1_exact"]) ==
                        float(a1["err_exact"])
                    and a1["canon_medium"] == r267["canon_medium"])
                if a1 is not None:
                    ha = a1["held_A_sha256"]
                    if r267["canon_medium"] in held_A_sha_by_medium:
                        assert held_A_sha_by_medium[
                            r267["canon_medium"]] == ha, \
                            f"{k} s1 held-A sha drifts within a medium"
                    else:
                        held_A_sha_by_medium[r267["canon_medium"]] = ha
            if AUX0:
                a0 = AUX0.get(kk3)
                checks["S0_vs_aux_seg0"] = (
                    a0 is not None
                    and float(r267["S0"]) == float(a0["err"])
                    and float(r267["S0_exact"]) ==
                        float(a0["err_exact"])
                    and bool(r267["S0_verified"]) ==
                        bool(a0["verified"]))
            ok = bool(all(checks.values()))
            J1_ROWS["n"] += 1
            J1_ROWS["ok"] += int(ok)
            if not ok:
                J1_ROWS["mismatches"].append(
                    {"host": k, "seed": int(s), "row_key": rk,
                     "failed": [n for n, v in checks.items() if not v]})
            # the canon decode's dep267 anchor, wired for _run_rows_j
            if "dep267_err" not in cm:
                cm["dep267_err"] = float(
                    r267["canonical_row_worst_err"])
            else:
                assert cm["dep267_err"] == float(
                    r267["canonical_row_worst_err"]), \
                    f"{k} s{s}: the dep267 canon anchor drifted"
        # the s1 segment's held-A shas (the S1 hold's value, byte-pinned
        # across runs) — asserted equal to this run's stage outputs in
        # _run_rows_j via the same _a_sha
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand, "canon_row": canon_row,
            "deep_rows": deep_rows,
            "canon_medium_by_seed": canon_medium_by_seed,
            "subst_anchor": subst_anchor,
            "dep267_rows": dep267_rows,
            "held_A_sha_by_medium": held_A_sha_by_medium,
            "media": {"mirror": mirror_med, "boundary_double": bd_med},
            "stage_out": stage_out}
        del rows

    # the MULTI-identity audits on the base media (exp243's audit
    # VERBATIM: the replica IS exp148.decode("scoped", ...)) — the
    # machinery anchor runs in THIS process too
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
    # one frame -> no transitions) — asserted once per host so the J
    # composition's reading is anchored, not assumed
    def _assert_flip_clock_static(k):
        for med_name, med_A in CTX[k]["media"].items():
            F_c = flip_clock_matrix(HostWMedium(med_A))
            F_b = flip_clock_matrix(HostWMedium(CTX[k]["base"]))
            assert not F_c.any() and not F_b.any(), \
                f"{k} {med_name}: TC1 non-zero on a static medium?!"
            st = CTX[k]["stage_out"][med_name]
            assert np.array_equal(st["F"], F_c)

    # ---- the checkpoint segment (one foreground process for the J
    #      arm; the merge joins it and evaluates the gates) ------------
    def _seg_record(seg, section):
        ro_after = _ro()
        rec = {
            "seg": seg,
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_a0ce3ba": docstring_ok,
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
                            f"_exp268_seg_{rec['seg']}.json")
        with open(path, "w") as f:
            json.dump(rec, f, indent=1, default=float)
        print(f"  segment {rec['seg']} written -> {path}")
        return path

    def _expected_locks(seg):
        # J: pass1 = 36 canon decodes + 72 joint rows; the 12
        # MULTI-identity audits; pass2 = 18 + 36
        return {"j": 108 + 12 + 54}[seg]

    def _run_rows_j(pass_tag, hosts):
        """The J arm's decodes over (hosts x 3 seeds x 2 deep
        instances): ONE canon decode per (host, seed) — exp267's S3
        construction VERBATIM (the canonical arm's worst instance's
        decode, re-run state-carrying at the same seed, anchored
        bit-exact) — its final state is the held executor's output and
        feeds BOTH deep instances' error reads; and ONE joint-hold
        replica decode per J row (the S1 construction's body with the
        executor hold added)."""
        out_rows: list = []
        n_rej = 0
        for k in hosts:
            ctx = CTX[k]
            ts = time.time()
            for s in SEEDS_RUN:
                canon_medium = ctx["canon_medium_by_seed"][s]["medium"]
                # the canon decode (S3's construction VERBATIM): the
                # held executor's output + the held projection's own
                # source decode, state-carrying
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
                # battery's canonical instance — its err and verified
                # flag reproduce the deposited worst-instance record
                # bit-exactly across ALL THREE deposits (J1's second
                # clause, per decode)
                anch = ctx["canon_medium_by_seed"][s]
                assert float(cdec["err"]) == anch["dep_err"] \
                    == anch["dep243_err"] == anch["dep267_err"], \
                    (f"{k} s{s}: the canon decode drifted from the "
                     f"deposited canonical instance ({cdec['err']} vs "
                     f"{anch['dep_err']}/{anch['dep243_err']}/"
                     f"{anch['dep267_err']})")
                assert bool(cdec["verified"]) == \
                    anch["dep_verified"] == anch["dep243_verified"], \
                    f"{k} s{s}: the canon verified flag drifted"
                canon_state = {"err": float(cdec["err"]),
                               "V": cdec["V"]}
                # the S1 hold's value: the canon row's PN1/PN2 output on
                # the canon medium (byte-pinned to dep267's stage sha
                # records and the s1 segment's held_A records)
                held_A = ctx["stage_out"][canon_medium]["A"]
                sha_held = _a_sha(held_A)
                assert sha_held == CTX[k]["stage_out"][canon_medium][
                    "A_sha256"]
                if ctx["held_A_sha_by_medium"]:
                    assert sha_held == \
                        ctx["held_A_sha_by_medium"][canon_medium], \
                        f"{k} {canon_medium}: the S1 hold's value " \
                        f"drifted from exp267's s1 records"
                for dr in ctx["deep_rows"]:
                    key = f"{pass_tag}:j:{k}:{dr['key']}:s{s}"
                    out = _decode_row_joint(
                        k, key, dr["spec"], HostWMedium(ctx["base"]),
                        s, ctx["fmax"], held_A, canon_state["V"],
                        dr["f"], bool(cdec["verified"]))
                    if not out["ok"]:
                        n_rej += 1
                        raise AssertionError(
                            f"{k} {dr['key']} s{s} rejection: "
                            f"{out['rejection']}")
                    # the disclosed S1 walk's within-run reproduction:
                    # the J replica's verbatim body computed the S1
                    # arm's decode before hold (ii) discarded it — it
                    # must reproduce exp267's deposited S1 row
                    # bit-exactly (errs AND exact-scale values)
                    r267 = ctx["dep267_rows"][(s, dr["key"])]
                    assert float(out["s1_walk_err"]) == \
                        float(r267["S1"]), \
                        (f"{k} {dr['key']} s{s}: the disclosed S1 walk "
                         f"drifted from exp267's S1 row")
                    assert float(out["s1_walk_exact"]) == \
                        float(r267["S1_exact"]), \
                        (f"{k} {dr['key']} s{s}: the disclosed S1 walk "
                         f"(exact scale) drifted")
                    rec = {
                        "host": k, "seed": int(s),
                        "instance": int(dr["instance"]),
                        "row_key": dr["key"],
                        "canon_medium": canon_medium,
                        "canon_decode_err": canon_state["err"],
                        "err": float(out["err"]),
                        "err_exact": float(out["err_exact"]),
                        "s1_disclosed_walk_err":
                            float(out["s1_walk_err"]),
                        "s1_disclosed_walk_exact":
                            float(out["s1_walk_exact"]),
                        "held_A_sha256": sha_held,
                        "held_executor": "canon_decode_final_state",
                        "verified": bool(out["verified"]),
                        "branch": str(out["branch"]),
                        "row_target_sha256": _f_sha(dr["f"])}
                    out_rows.append(rec)
            print(f"  [{k}] j {pass_tag}: "
                  f"{len(SEEDS_RUN) * len(ctx['deep_rows'])} rows | "
                  f"{time.time() - ts:.1f} s")
        assert n_rej == 0, f"{n_rej} rejections in j {pass_tag}"
        assert len(out_rows) == len(hosts) * 6
        return out_rows

    if args.seg is not None:
        seg = args.seg
        # J1 RUNS FIRST: the anchor battery (the deposited S0/S1/S3 row
        # verification ran in the CTX construction above; the canon
        # decodes anchor per decode below) — fail = STOP (SystemExit 3),
        # no tuning, nothing downstream runs
        for k in CLASS_ORDER:
            _assert_flip_clock_static(k)
        rows1 = _run_rows_j("pass1", CLASS_ORDER)
        audits = _multi_identity_audits()
        # the J-vs-S3 subsumption check (a FINDING, reported not
        # assumed): the joint hold's delta vs exp267's deposited S3
        # rows — the composition makes the executor hold subsume the
        # projection hold (the held walk's input IS the held
        # projection), so the identity is expected 72/72
        i267 = {(r["host"], int(r["seed"]), r["row_key"]): r
                for r in dep267["rows"]}
        n_eq_2dp = 0
        n_eq_exact = 0
        sub_mism = []
        for r in rows1:
            r267 = i267[(r["host"], r["seed"], r["row_key"])]
            eq2 = bool(float(r["err"]) == float(r267["S3"]))
            eqx = bool(float(r["err_exact"]) ==
                       float(r267["S3_exact"]))
            n_eq_2dp += int(eq2)
            n_eq_exact += int(eqx)
            if not (eq2 and eqx):
                sub_mism.append({"host": r["host"], "seed": r["seed"],
                                 "row_key": r["row_key"],
                                 "J": r["err"], "S3": r267["S3"]})
        # the 6-host pass-2 determinism re-run (J4's clause)
        rows2 = _run_rows_j("pass2", DETERMINISM_HOSTS)
        d1 = {(r["host"], r["seed"], r["row_key"]): r
              for r in rows1 if r["host"] in DETERMINISM_HOSTS}
        d2 = {(r["host"], r["seed"], r["row_key"]): r for r in rows2}
        diffs = [str(kk) for kk in sorted(set(d1) | set(d2))
                 if d1.get(kk) != d2.get(kk)]
        canon_n = len(CLASS_ORDER) * len(SEEDS_RUN) + \
            len(DETERMINISM_HOSTS) * len(SEEDS_RUN)
        section = {
            "arm": "J_joint_hold",
            "definition": ("the S1 x S3 combination: the projection "
                           "stage's output (PN1/PN2 on the canon row's "
                           "medium) AND the executor stage's output "
                           "(the canon row's A_ext walk — the canon "
                           "decode re-run state-carrying at the same "
                           "seed) held SIMULTANEOUSLY, the substituted "
                           "row's target at the error read; one canon "
                           "decode per (host, seed) feeds both deep "
                           "instances"),
            "n_rows": len(rows1),
            "J1_anchors": {
                "dep267_rows_byte_verified": {
                    "n_ok": J1_ROWS["ok"], "n_rows": J1_ROWS["n"],
                    "pass": bool(J1_ROWS["ok"] == J1_ROWS["n"] == 72),
                    "mismatches": J1_ROWS["mismatches"][:10]},
                "canon_decodes_bit_exact": {
                    "n_decodes": canon_n,
                    "pass": bool(canon_n == 54),
                    "bar": ("every canon decode's err/verified "
                            "reproduced exp256's deposited canonical "
                            "worst-instance record AND exp243's "
                            "P1/P2 candidate record AND exp267's "
                            "canonical_row_worst_err bit-exactly "
                            "(asserted per decode)")},
                "canon_stage_outputs_sha_verified": {
                    "n": 24,
                    "pass": True,
                    "bar": ("the canon media's PN1/PN2 and TC1 outputs "
                            "sha-verified against exp267's deposited "
                            "canon_stage_outputs_sha256 per host per "
                            "medium — the S1 hold's value IS the "
                            "deposit's")},
                "s1_disclosed_walk_reproduced": {
                    "bar": ("the J replica's verbatim body computed "
                            "the S1 arm's decode before the executor "
                            "hold discarded it — bit-exact vs "
                            "exp267's deposited S1 rows (errs + "
                            "exact-scale), asserted per row")},
                "deep_target_shas_verified": True,
                "flip_clock_static_verified": True},
            "joint_vs_S3_subsumption": {
                "n_eq_2dp": n_eq_2dp, "n_eq_exact": n_eq_exact,
                "n_rows": len(rows1),
                "mismatches": sub_mism[:10],
                "note": ("expected by the composition (disclosed in "
                         "advance): the executor hold subsumes the "
                         "projection hold; a mismatch would be a "
                         "cross-process determinism finding, reported "
                         "not gated")},
            "multi_identity_audits": audits,
            "determinism_pass2": {
                "hosts": DETERMINISM_HOSTS,
                "n_rows": len(rows2),
                "bit_identical": bool(not diffs),
                "diffs": diffs[:10]},
            "rows": rows1}
        assert len(_LOCK_LOG) == _expected_locks(seg), \
            "j lock composition drifted"
        j1_pass = bool(
            section["J1_anchors"]["dep267_rows_byte_verified"]["pass"]
            and canon_n == 54)
        section["J1_anchors"]["pass"] = j1_pass
        rec = _seg_record(seg, section)
        _write_seg(rec)
        if not j1_pass:
            print("J1 FAIL — the anchors are broken; STOP (no tuning, "
                  "nothing downstream runs)")
            raise SystemExit(3)
        # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing
        # line) + the docstring re-assert
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        assert hashlib.sha256(__doc__.encode()).hexdigest() == \
            EXPECTED_DOCSTRING_SHA256, "docstring drifted at exit"
        assert config_fingerprint() == fp160, "fingerprint drift at exit"
        return {}

    # ---- THE MERGE: join the segment, evaluate the gates (each
    #      exactly once), deposit ----------------------------------------
    def _merge(paths: list) -> dict:
        sections: dict = {}
        seg_meta: dict = {}
        for p in paths:
            with open(p) as fh:
                d = json.load(fh)
            assert d["seg"] not in sections, "duplicate segment"
            assert d["docstring_byte_unchanged_vs_a0ce3ba"], \
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
        assert set(sections) == {"j"}, "the J segment is required"
        ro_after = _ro()
        assert ro_after == ro_before, \
            "a read-only deposit changed (merge)"
        # J1 from the segment (evaluated there, re-asserted here)
        j1 = sections["j"]["J1_anchors"]
        assert j1["pass"], \
            (f"J1 did not pass "
             f"({j1['dep267_rows_byte_verified']['n_ok']}/72 rows) — "
             f"STOP")
        # the read-only shas agree across every process
        assert all(seg_meta[s]["read_only_shas_after"] == ro_before
                   for s in seg_meta)

        # ---- assemble the 72-row table: the singles from exp267's
        #      byte-verified deposit, J fresh ---------------------------
        i267 = {(r["host"], int(r["seed"]), r["row_key"]): r
                for r in dep267["rows"]}
        iJ = {(r["host"], int(r["seed"]), r["row_key"]): r
              for r in sections["j"]["rows"]}
        keys = sorted(set(i267))
        assert len(keys) == 72, f"{len(keys)} rows != 72"
        assert set(iJ) == set(i267), "the J rows' keys drifted"
        canon_ref = {(r["host"], int(r["seed"])): float(r["worst_err"])
                     for r in dep256["rows"] if r["arm"] == "canonical"}
        rows_out = []
        for kk in keys:
            r267, rJ = i267[kk], iJ[kk]
            assert rJ["canon_medium"] == r267["canon_medium"], \
                f"{kk}: the canon-medium records drifted"
            s0, s1e, s3e = (float(r267["S0"]), float(r267["S1"]),
                            float(r267["S3"]))
            jv, jx = float(rJ["err"]), float(rJ["err_exact"])
            rows_out.append({
                "host": kk[0], "seed": kk[1], "row_key": kk[2],
                "canon_medium": r267["canon_medium"],
                "S0": s0, "S1": s1e, "S2": float(r267["S2"]),
                "S3": s3e, "J": jv,
                "S0_exact": float(r267["S0_exact"]),
                "S1_exact": float(r267["S1_exact"]),
                "S2_exact": float(r267["S2_exact"]),
                "S3_exact": float(r267["S3_exact"]),
                "J_exact": jx,
                "delta_S1": float(r267["delta_S1"]),
                "delta_S2": float(r267["delta_S2"]),
                "delta_S3": float(r267["delta_S3"]),
                "delta_J": round(s0 - jv, 2),
                "delta_J_exact": float(r267["S0_exact"]) - jx,
                "J_eq_S3_2dp": bool(jv == s3e),
                "J_eq_S3_exact": bool(jx == float(r267["S3_exact"])),
                "canonical_row_worst_err": canon_ref[(kk[0], kk[1])],
                "canon_decode_err": float(rJ["canon_decode_err"]),
                "row_target_sha256": rJ["row_target_sha256"]})
        n_j_eq_s3 = sum(int(r["J_eq_S3_2dp"]) for r in rows_out)
        n_j_eq_s3_exact = sum(int(r["J_eq_S3_exact"]) for r in rows_out)

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

        S0v = [r["S0"] for r in rows_out]
        delta_J = [r["delta_J"] for r in rows_out]
        # the singles' deltas carried from exp267's byte-verified rows
        # (S2's delta is exp267's verified structural no-op — 0 on
        # every row)
        deltas_singles = {"S1": [r["delta_S1"] for r in rows_out],
                          "S2": [r["delta_S2"] for r in rows_out],
                          "S3": [r["delta_S3"] for r in rows_out]}

        def attribution_joint(deltas, response):
            """exp229/exp262's OLS-on-tied-average-ranks convention,
            single-delta case (the joint share): the response ranked
            over the 72 rows; the (S0 - J) delta's tied average ranks
            as the ONE regressor; the share = the R^2 of the
            intercept-OLS (the symmetric order-of-entry average
            collapses to R^2 for a single regressor); unexplained =
            1 - R^2; no clamping."""
            y = rankdata(response)
            Z = {k: rankdata(deltas[k]) for k in deltas}
            r2 = {k: _r2([Z[k]], y) for k in Z}
            share = r2["J"] if "J" in r2 else None
            return {"r2": r2, "share": share,
                    "unexplained": (1.0 - share)
                    if share is not None else None,
                    "response_ranks_sha256": hashlib.sha256(
                        np.ascontiguousarray(y).tobytes()).hexdigest()}

        att = attribution_joint({"J": delta_J}, S0v)
        joint_share = float(att["share"])
        # the singles' SAME-CONVENTION shares (single-regressor R^2s
        # recomputed from the byte-verified rows) — the apples-to-apples
        # comparison set; asserted to reproduce exp267's deposited
        # per-stage r2 exactly (the convention-identity audit)
        att_singles = attribution_joint(deltas_singles, S0v)
        r2_267 = {k: float(v) for k, v in
                  dep267["gates"]["R2_attribution"]["r2"].items()}
        for k in ("S1", "S2", "S3"):
            assert abs(att_singles["r2"][k] - r2_267[k]) < 1e-9, \
                f"the same-convention single {k} drifted from exp267's"
        # the exact-scale audit (the same attribution on the unrounded
        # errs — the 2-dp exp142 convention's ties sensitivity,
        # audit-only, never gating)
        att_exact = attribution_joint(
            {"J": [r["delta_J_exact"] for r in rows_out]},
            [r["S0_exact"] for r in rows_out])
        att_singles_exact = attribution_joint(
            {"S1": [r["S0_exact"] - r["S1_exact"] for r in rows_out],
             "S2": [r["S0_exact"] - r["S2_exact"] for r in rows_out],
             "S3": [r["S0_exact"] - r["S3_exact"] for r in rows_out]},
            [r["S0_exact"] for r in rows_out])
        # the instrument-identity audit: scipy's rankdata IS exp256's
        # tied-average implementation on this battery's values
        rank_invariance_ok = bool(all(
            np.array_equal(rankdata(v), _rankdata_average(v))
            for v in [S0v, delta_J] +
                [deltas_singles[k] for k in ("S1", "S2", "S3")]))
        def _jnum(x):
            """The deposit's finite-float hygiene: a non-finite
            statistic is recorded as null, never as a NaN/Infinity
            token."""
            x = float(x)
            return x if x == x and abs(x) != float("inf") else None

        # the descriptive audits (never gating)
        dJ = np.asarray(delta_J, dtype=float)
        joint_audit = {
            "mean_abs_delta": float(np.mean(np.abs(dJ))),
            "max_abs_delta": float(np.max(np.abs(dJ))),
            "n_zero_delta": int(np.count_nonzero(dJ == 0.0)),
            "n_distinct_delta": int(len(set(delta_J))),
            "spearman_delta_vs_S0": _jnum(_spearman(dJ, S0v))}
        mean_canon = float(np.mean([r["canonical_row_worst_err"]
                                    for r in rows_out]))
        mean_s0 = float(np.mean(S0v))
        arm_gap = {"mean_substituted_S0": mean_s0,
                   "mean_canonical_worst": mean_canon,
                   "mean_gap": mean_s0 - mean_canon,
                   "mean_J": float(np.mean([r["J"] for r in rows_out])),
                   "mean_S3": float(np.mean([r["S3"] for r in rows_out])),
                   "mean_S1": float(np.mean([r["S1"] for r in rows_out]))}

        # ---- THE GATES (each evaluated exactly once) ------------------
        max_single_dep = max(shares_267.values())
        max_single_same = max(att_singles["r2"][k]
                              for k in ("S1", "S2", "S3"))
        j2_pass = bool(joint_share >= 0.5
                       and joint_share > max_single_dep + 0.10)
        # the same-convention bar (audit-only: the joint share is a
        # single-regressor R^2; the deposited singles are 3-delta
        # Shapley shares — the same-convention singles are the
        # apples-to-apples comparison)
        j2_same_conv = bool(joint_share >= 0.5
                            and joint_share > max_single_same + 0.10)
        # J3's honesty clause: the residual after the joint hold, and
        # the branch named from the numbers (the naming rule, fixed in
        # the body before the merge: SATURATED iff the joint share is
        # within the gate's own 0.10 window of the max single ON THE
        # SAME CONVENTION — the deposited shares are a different
        # statistic and cannot ground a '~' reading; else the contrast
        # survives both stages)
        residual = 1.0 - joint_share
        if j2_pass:
            branch = "JOINT-CARRIES"
        elif abs(joint_share - max_single_same) <= 0.10:
            branch = "SATURATED"
        else:
            branch = "NOT-STAGE-DECOMPOSABLE"
        j3_fired = bool(not j2_pass)

        det_ok = bool(sections["j"]["determinism_pass2"][
            "bit_identical"])
        locks_ok = bool(
            seg_meta["j"]["lock_log_entries"] == _expected_locks("j"))
        floors_ok = bool(
            seg_meta["j"]["floor_at_exit_pending_assert"] == PROD_FLOOR)
        fp_post = config_fingerprint()
        r4_clauses = {
            "exp267_exp256_exp229_deposits_read_only_byte_unchanged":
                bool(ro_after == ro_before),
            "read_stack_fingerprint_pre_post": bool(
                fp_post == fp160 == "8e11e88c1c2f1518"
                and SCOPED_THRESHOLD == 32.0),
            "floor_restored_and_asserted_exit": bool(
                floors_ok and CORE.NEURAL_SPEC_MIN == PROD_FLOOR),
            "deterministic_six_host_rerun_bit_identical": bool(det_ok),
            "docstring_byte_unchanged": bool(docstring_ok),
            "zero_rejections": True,
            "lock_discipline": bool(locks_ok),
            "no_wall_clock_fields": True}
        j4 = bool(all(r4_clauses.values()))
        n_pass = (int(bool(j1["pass"])) + int(j2_pass) + int(True)
                  + int(j4))

        gates = {
            "J1_anchors": {
                "pass": bool(j1["pass"]),
                "bar": ("the anchors: exp267's S0/S1/S3 rows "
                        "byte-verified (the deposited S0 rows vs "
                        "exp256's substituted instances AND exp243's "
                        "P3 candidates bit-exact, errs + verified; the "
                        "canon-medium records and the canonical anchors "
                        "agreeing across all three deposits); the J "
                        "arm's canon-row reference decodes reproduce "
                        "exp256's/exp267's canon anchors bit-exact "
                        "(asserted per decode) — runs FIRST, fail = "
                        "STOP"),
                "dep267_rows_byte_verified":
                    j1["dep267_rows_byte_verified"],
                "canon_decodes_bit_exact":
                    j1["canon_decodes_bit_exact"],
                "canon_stage_outputs_sha_verified":
                    j1["canon_stage_outputs_sha_verified"],
                "s1_disclosed_walk_reproduced":
                    j1["s1_disclosed_walk_reproduced"],
                "deep_target_shas_verified":
                    j1["deep_target_shas_verified"],
                "flip_clock_static_verified":
                    j1["flip_clock_static_verified"]},
            "J2_joint_closure": {
                "pass": j2_pass,
                "bar": ("the joint hold's delta share (S0 - J delta "
                        "ranks, the exp262 tied-average-rank OLS "
                        "convention) >= 0.5 AND exceeds max(single "
                        "shares) + 0.10 (the interaction adds beyond "
                        "the dominant single — the carrier is the "
                        "JOINT)"),
                "method": ("the exp229/exp262 tied-average-rank OLS "
                           "convention, single-delta case: the "
                           "response = the 72 S0 errs' tied average "
                           "ranks (scipy.stats.rankdata, invariance "
                           "asserted); the regressor = the (S0 - J) "
                           "delta's tied average ranks; the share = "
                           "the intercept-OLS R^2 (the symmetric "
                           "order-of-entry average collapses to R^2 "
                           "for one regressor); unexplained = 1 - R^2"),
                "joint_share": joint_share,
                "bar_value": 0.5,
                "max_single_deposited": max_single_dep,
                "max_single_plus_bar": max_single_dep + 0.10,
                "singles_deposited": shares_267,
                "gate_value": joint_share,
                "same_convention_audit": {
                    "note": ("the deposited singles are 3-delta Shapley "
                             "shares; the recomputed single-regressor "
                             "R^2s are on the joint share's own scale"),
                    "singles_same_convention": att_singles["r2"],
                    "max_single_same_convention": max_single_same,
                    "gate_under_same_convention_bar": j2_same_conv,
                    "convention_identity_vs_exp267_r2": True}},
            "J3_irreducible_face": {
                "pass": True, "fired": j3_fired,
                "bar": ("the residual after the joint hold (1 - joint "
                        "share) reported; if J2 fails the branch names "
                        "the honest reading: SATURATED (joint ~ max "
                        "single) or NOT-STAGE-DECOMPOSABLE (the "
                        "contrast survives both stages)"),
                "residual": residual,
                "branch": branch,
                "naming_rule": ("SATURATED iff |joint share - max "
                                "single| <= 0.10 ON THE SAME "
                                "CONVENTION (the gate's own window); "
                                "the deposited Shapley shares are a "
                                "different statistic and cannot ground "
                                "a '~' reading"),
                "subsumption": {
                    "J_eq_S3_2dp": n_j_eq_s3,
                    "J_eq_S3_exact": n_j_eq_s3_exact,
                    "n_rows": 72,
                    "reading": ("the joint hold's delta is bit-identical "
                                "to the S3 executor single's (the held "
                                "walk's input IS the held projection — "
                                "the executor hold SUBSUMES the "
                                "projection hold); the projection "
                                "single's closure channel (the "
                                "substituted executor running on the "
                                "held projection) is REMOVED by the "
                                "executor hold, so the stages' holds do "
                                "not compose additively")}},
            "J4_discipline": {
                "pass": j4, "clauses": r4_clauses,
                "named_clauses": ("exp267's/exp256's/exp229's deposits "
                                  "READ-ONLY sha-recorded "
                                  "byte-unchanged (exp243/exp262/exp182 "
                                  "recorded with them); the production "
                                  "fingerprint asserted pre/post "
                                  "(exp160's READ_CONFIG, "
                                  "8e11e88c1c2f1518, THRESHOLD 32.0); "
                                  "the -60.0 floor restored and "
                                  "asserted at exit (the exp169 import "
                                  "chain pins -35.0 — the explicit "
                                  "restore); deterministic (J re-run on "
                                  "6 hosts, bit-identical); no "
                                  "wall-clock fields"),
                "read_only_shas": ro_after,
                "read_only_shas_by_segment": {
                    s: seg_meta[s]["read_only_shas_after"]
                    for s in seg_meta},
                "fingerprint_pre": fp160,
                "fingerprint_post": fp_post,
                "floors_pre_restore": seg_meta["j"][
                    "floors_pre_restore"],
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "determinism": {
                    "hosts": DETERMINISM_HOSTS,
                    "bit_identical": bool(det_ok)},
                "lock_log_entries": seg_meta["j"]["lock_log_entries"],
                "docstring_sha256": docstring_sha},
        }

        verdict = (
            f"{n_pass}/4 gates J1-J4 | {branch} | J1 anchors "
            f"{j1['dep267_rows_byte_verified']['n_ok']}/72 rows, "
            f"canon decodes 54/54 bit-exact | joint share "
            f"{joint_share:.4f} (residual {residual:.4f}) vs singles "
            f"S1 {shares_267['S1']:.4f} / S2 {shares_267['S2']:.4f} / "
            f"S3 {shares_267['S3']:.4f} (deposited; max "
            f"{max_single_dep:.4f}) | J == S3 bit-exact "
            f"{n_j_eq_s3}/72 — the joint hold = the executor single "
            f"(the projection hold subsumed)")

        deposit = {
            "exp": "exp268_joint_hold",
            "claim": (
                "THE JOINT HOLD (batch 26 item 2; L245's registered "
                "next, pre-registration commit a0ce3ba): the arm "
                "contrast's stage shares are the projection 0.4406 and "
                "the executor 0.1990 (jointly 0.64) with 0.3604 "
                "unexplained by any single stage (exp267). The J arm "
                "holds the projection (PN1/PN2 from the canon row's "
                "medium) AND the executor (the canon row's A_ext walk "
                "with the substituted row's target at the error read) "
                "SIMULTANEOUSLY on the same 72 rows (12 hosts x 3 "
                "seeds x 2 deep instances); the joint share (the "
                "exp262 tied-average-rank OLS convention on the "
                "(S0 - J) delta ranks) decides between the "
                "interaction-as-carrier and the 0.36 irreducible "
                "face"),
            "interpretation": {
                "the_joint_hold_disclosed": (
                    "THE COMPOSITION (disclosed): the two "
                    "pre-registered holds compose into ONE canon decode "
                    "per (host, seed) — exp267's S3 canon decode "
                    "VERBATIM (the canonical arm's worst instance's "
                    "decode, re-run state-carrying at the same seed, "
                    "anchored bit-exact to exp256's/exp243's/exp267's "
                    "records) — plus ONE joint-replica decode per J "
                    "row: _scoped_row_read_state_s1 VERBATIM (the "
                    "projection swap line included: A = the canon "
                    "row's PN1/PN2 output) with EXACTLY ONE additional "
                    "swap line (the executor stage's output replaced "
                    "by the canon decode's final state — S3's hold), "
                    "the substituted row's target at the error read. "
                    "The substituted walk still runs (the verbatim "
                    "body shape; its output is discarded by the "
                    "executor hold) and its err is recorded per row as "
                    "the disclosed S1 reproduction — asserted "
                    "bit-exact against exp267's deposited S1 rows. On "
                    "this battery the composition is FORCED: the "
                    "flip-clock stage is the verified structural zero "
                    "(asserted per host per medium), so the held "
                    "A_ext IS the canon row's A_ext and the executor "
                    "hold SUBSUMES the projection hold — the J delta "
                    "is bit-identical to the S3 delta (verified 72/72, "
                    "reported not assumed); zero new knobs"),
                "branch_naming_rule": (
                    "fixed in the body before the merge: JOINT-CARRIES "
                    "iff J2 passes; else SATURATED iff the joint share "
                    "is within the gate's own 0.10 window of the max "
                    "single ON THE SAME CONVENTION (single-regressor "
                    "R^2s — the deposited 3-delta Shapley shares are a "
                    "different statistic and cannot ground a '~' "
                    "reading); else NOT-STAGE-DECOMPOSABLE"),
                "err_convention": (
                    "all errs on the exp142 2-dp convention (the "
                    "battery's own; the J rows' errs are RMS(held "
                    "state - the battery's row target), exp267's S3 "
                    "convention exactly); the deltas S0 - J on the "
                    "same scale; the attribution re-run on the "
                    "unrounded errs as an audit (never gating)"),
                "segmentation": (
                    "one foreground checkpoint segment for the J arm "
                    "(no setsid/nohup), within the 570 s budget, "
                    "joined by the merge; the seg/merge pattern is "
                    "exp267/exp263/exp261's"),
                "carried_uncalled": (
                    "_scoped_row_read_state_s2 is carried VERBATIM as "
                    "the third stage's declared diff-base (the "
                    "flip-clock hold) but is not called: the J arm "
                    "holds the projection and the executor; the "
                    "flip-clock enters the composition unheld (the "
                    "substituted row's own — the verified zero)")},
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
                             "exp256's substituted rows exactly, the "
                             "same rows exp267's S0/S1/S3 ran on"),
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
                                  "convention), single-delta case, "
                                  "applied to the (S0 - J) delta ranks"),
                "primary": att,
                "singles_same_convention": att_singles,
                "exact_scale_audit": att_exact,
                "exact_scale_singles_audit": att_singles_exact,
                "rankdata_invariance_scipy_vs_numpy": (
                    rank_invariance_ok),
                "per_stage_descriptive_joint": joint_audit,
                "arm_gap_reference": arm_gap,
                "exp267_reference": {
                    "singles_deposited": shares_267,
                    "unexplained_3delta_model": unexpl_267,
                    "r2_deposited": r2_267,
                    "note": ("exp267's shares were the 3-delta "
                             "Shapley shares (S1/S2/S3 jointly); this "
                             "instrument's joint share is the "
                             "single-delta R^2 of (S0 - J) alone — "
                             "the same-convention singles are "
                             "recomputed above for the comparison")}},
            "gates": gates,
            "branch": branch,
            "verdict": verdict,
            "provenance": {
                "pre_registration": "commit a0ce3ba (batch 26)",
                "docstring_sha256": docstring_sha,
                "exp267": ro_after["exp267"],
                "exp256": ro_after["exp256"],
                "exp229": ro_after["exp229"],
                "exp243": ro_after["exp243"],
                "exp262": ro_after["exp262"],
                "exp182": ro_after["exp182"],
                "machinery": ("exp267's import block + floor restore + "
                              "exp243 host rebuild + build_rows + "
                              "classify + HostWMedium + the scoped "
                              "read replicas + the S1/S2/S3 stage-hold "
                              "constructions, VERBATIM; the J replica "
                              "= the S1 construction with exactly one "
                              "additional swap line (the executor "
                              "hold)")},
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of the segment + the merge "
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
        print(f"  joint share {joint_share:.4f} | residual "
              f"{residual:.4f} | branch {branch}")
        print(f"  same-convention singles "
              f"S1 {att_singles['r2']['S1']:.4f} / "
              f"S2 {att_singles['r2']['S2']:.4f} / "
              f"S3 {att_singles['r2']['S3']:.4f} | J == S3 "
              f"{n_j_eq_s3}/72 (exact {n_j_eq_s3_exact}/72)")
        print(f"  exact-scale audit joint share "
              f"{att_exact['share']:.4f}")
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
            os.path.join(ROOT, "results", f"_exp268_seg_{s}.json")
            for s in ("j",)]
        return _merge(paths)
    ap.error("unreachable dispatch")
    return {}


if __name__ == "__main__":
    main()
