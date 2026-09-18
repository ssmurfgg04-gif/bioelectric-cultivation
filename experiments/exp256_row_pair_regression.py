#!/usr/bin/env python3
"""exp256 — THE ROW-LEVEL PAIR REGRESSION (exp255's registered next, L233;
batch 22 item 1).

THE OPEN ITEM (L233): the boundary geometry drives the CANONICAL rows'
cost across hosts (rho 0.8574) but the deep-band substitution BREAKS
that dependence (rho 0.1374) — exp254's pair-structure mechanism
operating at the ROW level, not the host level. The per-host records
carry only the argmax decompositions; the row-level regression needs
per-seed rows for MANY hosts.

THE INSTRUMENT (exp243's machinery verbatim, zero new knobs): run the
per-seed decomposition battery — the 12 candidate hosts x the two media
(the canonical P1/P2 battery medium vs the P3 deep-band substituted
medium) x 3 seeds (exp142's seeds) — recording each row's per-class
decomposition (exp208's classify: CANON-BOUNDARY / PAIR-JUNCTION /
INTERIOR, precedence intact) and the row's worst err. 72 rows.

PRE-REGISTERED GATES:

  R1  THE ROW-LEVEL REGRESSION: Spearman(per-row PAIR-JUNCTION count,
      per-row worst err) across the 72 rows >= 0.5 (the pair structure
      carries the cost AT THE ROW LEVEL, where exp255 located it).
  R2  THE SPECIFICITY: the row-level pair count predicts the
      substituted (P3-medium) rows' errs BETTER than the canonical
      rows' (rho_P3 > rho_canon on the same 36-row halves) — the
      row-level mirror of exp255's host-level inversion.
  R3  THE HOST-LEVEL NULL SHARPENED: within-host rank correlation
      (Spearman computed per host over its own 6 rows, pooled via the
      tied average-rank OLS on within-host ranks) — the row-level
      driver must survive CONTROLLING for host identity (the null:
      the host-level boundary count alone explains the rows).
  R4  THE DISCIPLINE: exp243's deposit READ-ONLY sha-recorded
      byte-unchanged; deterministic (re-run bit-identical); the
      -60.0 floor restored and asserted at exit after any exp169
      import.

THE BRANCHES (pre-named): R1 PASS -> ROW-PAIR-CARRIES (the pair
geometry is the row-level driver — exp254's mechanism measured at its
own scale); R1 REFUTE -> ROW-DRIVER-ABSENT (the row-level cost has a
different structure than pair counts — deposited honestly).

RUN: 72 scoped reads + decompositions (exp243's battery ran 138.5 s for
48 candidates; this is comparable), foreground or runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp256_row_pair_regression.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline; gates R1-R4 below evaluated exactly once,
    # pre-registration commit 276e41e) ==================================
    # body-only plumbing repair (disclosed): the pre-registered header
    # carries only os/sys — json and numpy are imported HERE, in-body,
    # before any use and before the reader-line chain (the BLAS pins
    # are already set by the header, so the pin discipline holds)
    import hashlib
    import json
    import time

    import numpy as np

    t0 = time.time()
    out_path = OUT

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

    REWIRE_P = 0.10                        # exp225's corpus rewire p
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    # the seeds: exp142's seeds (the docstring's "3 seeds (exp142's
    # seeds)"); exp198's n=400 line's seeds asserted identical, and both
    # asserted identical to exp243's deposited battery seeds below
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert tuple(int(s) for s in SEEDS) == SEEDS_RUN, "seed-line drift"
    assert len(SEEDS_RUN) == 3, "the pre-registration's 3 seeds"
    # the pre-named perturbation set (exp243's docstring order — the
    # battery arms ARE exp243's candidate records, zero new knobs)
    PERT_ORDER = ("P1_canon_zone_relabelings",
                  "P2_boundary_double_frequency_rewiring",
                  "P3_deep_band_substitution")
    PERT_NAME = {
        "P1_canon_zone_relabelings": "the canon/zone relabelings",
        "P2_boundary_double_frequency_rewiring":
            "the boundary-double-frequency rewiring",
        "P3_deep_band_substitution": "the deep-band substitution"}

    # ---- THE TWO BATTERY ARMS (the docstring's "two media"; both are
    #      exp243's own candidate records — exp255's per-host worsts,
    #      taken per-seed): the canonical arm = exp243's P1+P2
    #      candidates (the canon row read on the mirror /
    #      boundary-double media), the row's worst err = the arm's max
    #      at that seed (exp255's worst_canon, per-seed); the substituted
    #      arm = exp243's P3 candidates (the deep band's -60.0 rung
    #      rows, BOTH pre-named instances, on the base medium), the
    #      row's worst err = the arm's max at that seed (exp255's
    #      worst_p3, per-seed). The within-arm tie-break is the
    #      pre-named instance order (P1 before P2; deep i0 before i1):
    #      the FIRST strict max wins (exp243's argmax rule).
    ARM_CANON = "canonical"
    ARM_SUBST = "substituted"
    ARMS = (ARM_CANON, ARM_SUBST)

    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP255 = os.path.join(ROOT, "results", "exp255.json")
    for _p in (DEP243, DEP182, DEP255):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    # R4: exp243's deposit READ-ONLY — sha taken BEFORE any read,
    # re-verified byte-unchanged after the battery, recorded in the
    # deposit
    sha243_before = _sha(DEP243)
    sha182 = _sha(DEP182)
    sha255 = _sha(DEP255)
    with open(DEP243) as fh:
        dep243 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)
    with open(DEP255) as fh:
        dep255 = json.load(fh)

    # the host-level anchors being sharpened (the docstring's open
    # item): exp255's deposited inversion, asserted un-drifted
    rho_canon_host = float(dep255["spearman_canon"])
    rho_p3_host = float(dep255["spearman_p3"])
    assert round(rho_canon_host, 4) == 0.8574, \
        f"exp255's deposited rho_canon drifted: {rho_canon_host}"
    assert round(rho_p3_host, 4) == 0.1374, \
        f"exp255's deposited rho_P3 drifted: {rho_p3_host}"
    assert list(dep255["consumed_deposits"].values()) == [sha243_before], \
        "exp255's recorded exp243 sha != the live exp243 sha"

    # ---- the one frozen read configuration (exp243's READ_CONFIG,
    #      battery-adapted; fingerprinted, asserted identical pre/post)
    READ_CONFIG = {
        "wiring": ("exp178's production scoped arm: exp169's f_max "
                   "diagnostic + the pre-registered THRESHOLD (32.0); "
                   "R_T (exp167's adopted read) iff f_max < 32.0, else "
                   "exp148's raw temporal — one arm, one function, zero "
                   "knobs"),
        "projection": ("exp145/exp148 TC1-TC3: PN1/PN2 dominant-quadrature "
                       "projection + TC1 flip-clock F + TC2 A_ext = A + F"),
        "executor": ("exp142 execute_signed VERBATIM (R1 structure on "
                     "|A|, R2 signed dynamics, walk frontier on |A|>0), "
                     "state-carrying (exp243's A3 return_state path)"),
        "op": {"gamma": 64.0, "mu": 0.0},
        "op_source": ("exp99's battery-wide STAR point (exp142's "
                      "STAR_OP); STAR_OP IS S* = (64.0, 0.0), asserted"),
        "spec_input": ("per-row target spec — the read stack's target "
                       "parameter (exp148's MULTI default asserted "
                       "bit-identical per class by the MULTI-identity "
                       "audit)"),
        "seeds": list(SEEDS_RUN),
        "n": N400,
        "window_h": 24.0,
        "commit_noise": 0.6,
        "steps_per_cell": 8,
        "floor": ("production -60.0 restored post-import (exp218's "
                  "disclosed exp169-import discipline; the -35.0 "
                  "reader-line pin disclosed)"),
        "per_media_tuning": "none",
        "battery": ("the per-seed decomposition battery: exp243's 12 "
                    "candidate hosts x the two battery arms (canonical "
                    "P1/P2 vs substituted P3) x 3 seeds = 72 rows; each "
                    "row carries exp208's classify decomposition "
                    "(CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR, "
                    "precedence intact) and the row's worst err"),
    }

    def _fingerprint() -> str:
        return hashlib.sha256(
            json.dumps(READ_CONFIG, sort_keys=True).encode()
        ).hexdigest()[:16]

    FP = _fingerprint()

    # ---- the S* identity of the reader's executor (exp243 VERBATIM) ---
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the reader's executor op {STAR_OP} != S* {S_STAR}"
    assert int(dep243["adversary"]["n"]) == int(N400), "n drift vs dep243"
    assert [int(s) for s in dep243["adversary"]["seeds"]] == \
        list(SEEDS_RUN), "seed drift vs dep243"

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
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

    def _decode_row_state(host, row_key, spec, med, seed, fmax):
        """One state-carrying decode; a rejection is RECORDED, never
        hidden (exp142's zero-rejection hygiene; the caller raises) —
        exp243's _decode_row at the state-carrying call site, with the
        A3 state-convention assert (the recomputed RMS matches the
        reported err at the exp142 2-dp convention)."""
        _lock_read(host, row_key, seed)
        try:
            out = _scoped_row_read_state(spec, med, seed, fmax)
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
    # (the boundary-signature instrument; classify + decompose copied
    # byte-for-byte from exp208_c6_tail_ablation via exp243, zero knobs)
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

    def decompose(V: np.ndarray, T: np.ndarray, cls: np.ndarray,
                  err_recomputed: float) -> dict:
        e2 = (np.asarray(V, dtype=float)
              - np.asarray(T, dtype=float)) ** 2
        total = float(e2.sum())
        n = len(e2)
        per = []
        for name, mask in (("CANON-BOUNDARY", cls == 0),
                           ("PAIR-JUNCTION", cls == 1),
                           ("INTERIOR", cls == 2)):
            ss = float(e2[mask].sum())
            per.append({"class": name, "n_cells": int(mask.sum()),
                        "sum_sq": ss,
                        "frac_of_sq": ss / total if total > 0 else 0.0,
                        "rms_contrib_mV":
                            float(np.sqrt(ss / n)) if n else 0.0})
        # THE ACCOUNTING IDENTITY (the RMS convention, disclosed):
        # the shares are mean-squared contributions in mV^2 and
        # sum to err^2 — the identity on the scale the RMS actually
        # decomposes (an mV-linear split would be a fake identity)
        ident = abs(sum(p["sum_sq"] for p in per) / n
                    - err_recomputed ** 2)
        assert ident < 1e-6 * max(1.0, err_recomputed ** 2), \
            f"accounting identity violated: {ident}"
        assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
        return {"per_class": per, "identity_residual": ident}

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
    print(f"=== exp256: THE ROW-LEVEL PAIR REGRESSION (L233's "
          f"registered next) ===")
    print(f"  battery: {len(dep243['classes'])} candidate hosts x 2 "
          f"battery arms (canonical P1/P2 vs substituted P3) x "
          f"{len(SEEDS_RUN)} seeds {list(SEEDS_RUN)} = 72 rows, at "
          f"n={N400}")
    print(f"  read: exp178's production scoped arm, fingerprint {FP}; "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})\n")

    # ---- the 12 hosts rebuilt from exp243's DEPOSIT records (the
    #      task's zero-knob rule: hosts/seeds/arms from exp243's
    #      deposit; every rebuild bit-asserted against the deposit's
    #      own sha records) ----------------------------------------------
    CLASS_ORDER = sorted(dep243["classes"])
    assert len(CLASS_ORDER) == 12, "the 12 candidate hosts"
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

    # ---- the per-class media, rows and reproduction anchors -----------
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
            (PERT_ORDER[0], "canon"), (PERT_ORDER[1], "canon"),
            (PERT_ORDER[2], f"r{DEEP_RUNG:g}i0"),
            (PERT_ORDER[2], f"r{DEEP_RUNG:g}i1")}, \
            f"{k} candidate set drifted from exp243's deposit"
        assert _a_sha(mirror_med) == \
            cand[(PERT_ORDER[0], "canon")]["medium_sha256"], \
            f"{k} mirror-medium rebuild drifted"
        assert _a_sha(bd_med) == \
            cand[(PERT_ORDER[1], "canon")]["medium_sha256"], \
            f"{k} boundary-double-medium rebuild drifted"
        assert _a_sha(A_base) == \
            cand[(PERT_ORDER[2], f"r{DEEP_RUNG:g}i0")]["medium_sha256"] \
            == cand[(PERT_ORDER[2],
                     f"r{DEEP_RUNG:g}i1")]["medium_sha256"], \
            f"{k} base-medium rebuild drifted"
        dep_p2 = cand[(PERT_ORDER[1], "canon")]
        assert bidx == list(dep_p2["boundary_cells"]), \
            f"{k} P2 boundary-cell set drifted"
        assert added == [list(a) for a in dep_p2["chords_added"]], \
            f"{k} P2 chords drifted"
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand,
            "arms": {
                ARM_CANON: [
                    {"pert": PERT_ORDER[0], "row": canon_row,
                     "med": HostWMedium(mirror_med), "medium": "mirror"},
                    {"pert": PERT_ORDER[1], "row": canon_row,
                     "med": HostWMedium(bd_med),
                     "medium": "boundary_double"}],
                ARM_SUBST: [
                    {"pert": PERT_ORDER[2], "row": deep_rows[0],
                     "med": HostWMedium(A_base), "medium": "base"},
                    {"pert": PERT_ORDER[2], "row": deep_rows[1],
                     "med": HostWMedium(A_base), "medium": "base"}]}}
    # the MULTI-identity audits on the base media (exp243's audit
    # VERBATIM: the replica IS exp148.decode("scoped", ...))
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
            f"{k}: the scoped wiring drifted from exp148.decode('scoped')"
        audits[k] = {"seed": int(SEEDS_RUN[0]), "bit_identical": True,
                     "prod_err": float(prod["err"]), "f_max": fmax_b}
        _lock_read(k, "multi_audit", SEEDS_RUN[0])

    # ---- THE PER-SEED DECOMPOSITION BATTERY (one pass = 72 rows;
    #      every decode state-carrying, so each row's decomposition is
    #      exp208's classify + decompose on the worst instance's own
    #      state) ----------------------------------------------------------
    def run_battery(pass_tag: str) -> list:
        rows_out: list = []
        repro: dict = {}
        n_rej = 0
        for k in CLASS_ORDER:
            ctx = CTX[k]
            ts = time.time()
            for s in SEEDS_RUN:
                for arm in ARMS:
                    inst_recs, errs = [], []
                    for inst in ctx["arms"][arm]:
                        out = _decode_row_state(
                            k, f"{pass_tag}:{arm}:{inst['pert']}:"
                               f"{inst['row']['key']}",
                            inst["row"]["spec"], inst["med"], s,
                            ctx["fmax"])
                        if not out["ok"]:
                            n_rej += 1
                            raise AssertionError(
                                f"{k} {arm} {inst['pert']} s{s} "
                                f"rejection: {out['rejection']}")
                        inst_recs.append({
                            "pert": inst["pert"], "row_key":
                                inst["row"]["key"],
                            "medium": inst["medium"],
                            "medium_sha256":
                                _a_sha(inst["med"].A),
                            "row_target_sha256":
                                _f_sha(inst["row"]["f"]),
                            "err": float(out["err"]),
                            "verified": bool(out["verified"]),
                            "branch": str(out["branch"])})
                        errs.append(float(out["err"]))
                        repro.setdefault(
                            (k, inst["pert"], inst["row"]["key"]),
                            {})[int(s)] = (float(out["err"]),
                                           bool(out["verified"]))
                    worst = max(errs)
                    # the pre-named tie-break: FIRST strict max in the
                    # arm's instance order (exp243's argmax rule)
                    w_idx = errs.index(worst)
                    w_inst = ctx["arms"][arm][w_idx]
                    w_rec = inst_recs[w_idx]
                    # the worst instance's own state -> the row's
                    # decomposition (exp208's classify precedence
                    # intact; W = the read's own medium)
                    out = _decode_row_state(
                        k, f"{pass_tag}:dec:{arm}:{w_inst['pert']}:"
                           f"{w_inst['row']['key']}",
                        w_inst["row"]["spec"], w_inst["med"], s,
                        ctx["fmax"])
                    assert out["ok"] and \
                        abs(float(out["err"]) - worst) < 1e-12, \
                        (f"{k} {arm} s{s}: the decomposition re-read "
                         f"drifted from the battery read")
                    V, T = out["V"], out["T"]
                    cinfo = classify(T, w_inst["med"].A)
                    decomp = decompose(V, T, cinfo["class"],
                                       float(out["err_exact"]))
                    rows_out.append({
                        "host": k, "arm": arm, "seed": int(s),
                        "instances": inst_recs,
                        "worst_err": float(worst),
                        "worst_pert": w_rec["pert"],
                        "worst_row_key": w_rec["row_key"],
                        "worst_medium": w_rec["medium"],
                        "worst_medium_sha256": w_rec["medium_sha256"],
                        "row_target_sha256":
                            w_rec["row_target_sha256"],
                        "f_max": ctx["fmax"],
                        "pair_junction_count":
                            int(cinfo["junction"].sum()),
                        "class_counts": {
                            "CANON-BOUNDARY":
                                int(cinfo["boundary"].sum()),
                            "PAIR-JUNCTION":
                                int(cinfo["junction"].sum()),
                            "INTERIOR":
                                int(cinfo["interior"].sum())},
                        "decomposition": decomp})
            wc = max(r["worst_err"] for r in rows_out
                     if r["host"] == k and r["arm"] == ARM_CANON)
            ws = max(r["worst_err"] for r in rows_out
                     if r["host"] == k and r["arm"] == ARM_SUBST)
            print(f"  [{k}] pass {pass_tag}: 12 rows | worst canon "
                  f"{wc:.2f} worst subst {ws:.2f} | "
                  f"{time.time() - ts:.1f} s")
        # the exp243 battery reproduction anchor: the pass's errs and
        # verified flags must reproduce exp243's deposited candidate
        # records EXACTLY (the exp142 2-dp err convention — the
        # machinery IS exp243's machine, bit-verified)
        for (k, pert, rk), by_seed in repro.items():
            dep_rec = CTX[k]["cand"][(pert, rk)]
            assert [by_seed[s][0] for s in SEEDS_RUN] == \
                [float(e) for e in dep_rec["errs"]], \
                f"{k} {pert} {rk}: errs drifted from exp243's deposit"
            assert [by_seed[s][1] for s in SEEDS_RUN] == \
                [bool(v) for v in dep_rec["verified"]], \
                f"{k} {pert} {rk}: verified flags drifted"
        assert n_rej == 0, f"{n_rej} rejections in pass {pass_tag}"
        assert len(rows_out) == 72, \
            f"pass {pass_tag}: {len(rows_out)} rows != 72"
        return rows_out

    print()
    rows1 = run_battery("pass1")
    rows2 = run_battery("pass2")

    # ---- determinism: the full battery re-run, bit-identical
    #      (exp250's discipline) ------------------------------------------
    key = lambda r: (r["host"], r["arm"], r["seed"])  # noqa: E731
    d1 = {key(r): r for r in rows1}
    d2 = {key(r): r for r in rows2}
    diffs = []
    if set(d1) != set(d2):
        diffs.append("row-key sets differ")
    for kk in sorted(set(d1) & set(d2)):
        if d1[kk] != d2[kk]:
            diffs.append(str(kk))
    deterministic = not diffs

    # the worst-instance tie census (disclosure, non-gating): rows
    # where the arm's two instances tie at the worst err — the
    # pre-named first-instance tie-break decided the decomposition
    n_tied = sum(1 for r in rows1 if len(
        {i["err"] for i in r["instances"]
         if i["err"] == r["worst_err"]}) == 1
        and len([i for i in r["instances"]
                 if i["err"] == r["worst_err"]]) > 1)

    # ---- the rank instruments (tied average ranks; zero scipy) --------
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
        return _pearson(_rankdata_average(x), _rankdata_average(y))

    # ================= THE GATES (each evaluated exactly once) =========
    xs = np.array([r["pair_junction_count"] for r in rows1], dtype=float)
    ys = np.array([r["worst_err"] for r in rows1], dtype=float)
    m_sub = np.array([r["arm"] == ARM_SUBST for r in rows1])
    m_can = ~m_sub
    assert int(m_sub.sum()) == 36 and int(m_can.sum()) == 36, \
        "the 36-row halves drifted"

    rho_all = _spearman(xs, ys)
    rho_sub = _spearman(xs[m_sub], ys[m_sub])
    rho_can = _spearman(xs[m_can], ys[m_can])
    r1 = bool(rho_all == rho_all and rho_all >= 0.5)
    r2 = bool(rho_sub == rho_sub and rho_can == rho_can
              and rho_sub > rho_can)

    # R3 — the host-level null sharpened: within-host rank correlation
    # (Spearman per host over its own 6 rows; pooled via the tied
    # average-rank OLS on the within-host ranks — controlling for host
    # identity removes every host-level term, the host-boundary-count
    # null included)
    per_host = []
    rx_pool, ry_pool = [], []
    for k in CLASS_ORDER:
        idx = [i for i, r in enumerate(rows1) if r["host"] == k]
        assert len(idx) == 6, f"{k}: {len(idx)} rows != 6"
        rho_h = _spearman(xs[idx], ys[idx])
        per_host.append({"host": k, "n_rows": 6,
                         "spearman": (rho_h if rho_h == rho_h
                                      else None)})
        rx_pool.extend(_rankdata_average(xs[idx]).tolist())
        ry_pool.extend(_rankdata_average(ys[idx]).tolist())
    rx_pool = np.array(rx_pool, dtype=float)
    ry_pool = np.array(ry_pool, dtype=float)
    pooled_r = _pearson(rx_pool, ry_pool)
    cx = rx_pool - rx_pool.mean()
    cy = ry_pool - ry_pool.mean()
    denom = float((cx * cx).sum())
    ols_slope = (float((cx * cy).sum()) / denom) if denom > 0 else \
        float("nan")
    ols_intercept = (float(ry_pool.mean() - ols_slope * rx_pool.mean())
                     if denom > 0 else float("nan"))
    r3 = bool(pooled_r == pooled_r and pooled_r >= 0.5)

    sha243_after = _sha(DEP243)
    read_only = bool(sha243_after == sha243_before)

    fp_post = _fingerprint()
    audits_ok = all(a["bit_identical"] for a in audits.values())
    n_decodes_total = len(_LOCK_LOG)
    # the composition: 2 passes x (144 arm-instance decodes + 72
    # worst-instance decomposition re-reads) + 12 audits = 444
    expected_locks = 2 * (144 + 72) + 12
    lock_ok = (len(set(_LOCK_LOG)) == len(_LOCK_LOG)
               and n_decodes_total == expected_locks)
    floors_live_ok = all(
        getattr(m, "NEURAL_SPEC_MIN", None)
        in (PROD_FLOOR, READER_PIN_FLOOR) for m in PINNED)
    all_errs = [i["err"] for r in rows1 for i in r["instances"]]
    all_finite = bool(all_errs) and bool(np.all(np.isfinite(all_errs)))
    repro_ok = True          # asserted hard inside run_battery
    r4_clauses = {
        "exp243_deposit_read_only_byte_unchanged": read_only,
        "deterministic_rerun_bit_identical": bool(deterministic),
        "floor_restored_exit_pending_assert": bool(floors_live_ok),
        "zero_rejections": True,
        "all_finite": all_finite,
        "battery_complete_72_rows_x2_passes": bool(
            len(rows1) == 72 and len(rows2) == 72 and not diffs),
        "multi_identity_audits": bool(audits_ok),
        "fingerprint_stable": bool(fp_post == FP),
        "exp243_battery_reproduction": repro_ok,
        "lock_discipline": bool(lock_ok)}
    r4 = bool(all(r4_clauses.values()))

    branch = "ROW-PAIR-CARRIES" if r1 else "ROW-DRIVER-ABSENT"

    gates = {
        "R1_row_level_regression": {
            "pass": r1,
            "bar": ("Spearman(per-row PAIR-JUNCTION count, per-row "
                    "worst err) across the 72 rows >= 0.5"),
            "rho_all_72": rho_all, "bar_value": 0.5, "n_rows": 72,
            "n_decodes": 144, "seeds": list(SEEDS_RUN)},
        "R2_specificity": {
            "pass": r2,
            "bar": ("the row-level pair count predicts the substituted "
                    "(P3-medium) rows' errs BETTER than the canonical "
                    "rows' (rho_P3 > rho_canon on the same 36-row "
                    "halves) — the row-level mirror of exp255's "
                    "host-level inversion"),
            "rho_substituted_36": rho_sub,
            "rho_canonical_36": rho_can,
            "host_level_reference": {"rho_canon_exp255":
                                     rho_canon_host,
                                     "rho_p3_exp255": rho_p3_host}},
        "R3_host_null_sharpened": {
            "pass": r3,
            "bar": ("the pooled within-host rank correlation >= 0.5 — "
                    "the row-level driver must survive CONTROLLING for "
                    "host identity (the null: the host-level boundary "
                    "count alone explains the rows)"),
            "method": ("Spearman computed per host over its own 6 "
                       "rows; pooled via the tied average-rank OLS on "
                       "within-host ranks (Pearson on the pooled "
                       "average ranks)"),
            "pooled_within_host_rank_pearson": pooled_r,
            "ols_slope": ols_slope, "ols_intercept": ols_intercept,
            "per_host_spearman": per_host, "n_hosts": 12},
        "R4_discipline": {
            "pass": r4, "clauses": r4_clauses,
            "named_clauses": ("exp243's deposit READ-ONLY sha-recorded "
                              "byte-unchanged; deterministic (re-run "
                              "bit-identical); the -60.0 floor restored "
                              "and asserted at exit after any exp169 "
                              "import"),
            "hygiene_note": ("the remaining clauses are exp243's A4 "
                             "hygiene carried verbatim (zero "
                             "rejections, all finite, complete, "
                             "audits, fingerprint, reproduction, "
                             "locks)"),
            "floor_discipline": (
                f"production {PROD_FLOOR} restored post-import on all "
                f"pinned modules (save disclosed: {_PRE_RESTORE}); the "
                f"{READER_PIN_FLOOR} reader-line pin disclosed "
                f"(exp218's discipline); the exit assert runs after "
                f"the deposit write"),
            "floors_pre_restore": dict(_PRE_RESTORE),
            "floors_midrun_live": {m.__name__: getattr(
                m, "NEURAL_SPEC_MIN", None) for m in PINNED},
            "exp243_deposit_sha256": sha243_after,
            "determinism": {"passes": 2, "rows_per_pass": 72,
                            "decodes_per_pass": 144,
                            "bit_identical": bool(deterministic),
                            "diffs": diffs[:10],
                            "rows_sha256_pass1": hashlib.sha256(
                                json.dumps(rows1,
                                           sort_keys=True).encode()
                            ).hexdigest(),
                            "rows_sha256_pass2": hashlib.sha256(
                                json.dumps(rows2,
                                           sort_keys=True).encode()
                            ).hexdigest()},
            "lock_log_entries": n_decodes_total,
            "decode_locks_expected": expected_locks,
            "lock_composition": ("2 battery passes x (144 arm-instance "
                                 "decodes + 72 worst-instance "
                                 "decomposition re-reads) + 12 "
                                 "MULTI-identity audit locks = 444 — "
                                 "all unique, no duplicates"),
            "worst_instance_ties_first_instance_rule": n_tied,
            "fingerprint_pre": FP, "fingerprint_post": fp_post,
            "per_media_tuning": "none"},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = (f"{n_pass}/4 gates R1-R4 | {branch} | "
               f"rho_all {rho_all:.4f} (bar 0.5) | rho_subst "
               f"{rho_sub:.4f} vs rho_canon {rho_can:.4f} | pooled "
               f"within-host {pooled_r:.4f} | 12 hosts x 2 arms x 3 "
               f"seeds = 72 rows")

    deposit = {
        "exp": "exp256_row_pair_regression",
        "claim": (
            "THE ROW-LEVEL PAIR REGRESSION (L233's registered next; "
            "batch 22 item 1): exp255 located the pair-structure "
            "mechanism at the ROW level (the boundary geometry drives "
            "the CANONICAL rows' cost across hosts at rho 0.8574 but "
            "the deep-band substitution BREAKS that dependence at rho "
            "0.1374 — the host level cannot see it). The per-seed "
            "decomposition battery runs exp243's machinery verbatim "
            "over the 12 candidate hosts x the two battery arms (the "
            "canonical P1/P2 medium arm vs the P3 deep-band "
            "substituted arm) x 3 seeds = 72 rows, recording each "
            "row's per-class decomposition (exp208's classify: "
            "CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR, precedence "
            "intact) and the row's worst err, then regresses the "
            "per-row PAIR-JUNCTION count on the per-row worst err"),
        "read": {**READ_CONFIG, "fingerprint": FP,
                 "wiring_id": ("exp148.decode('scoped') wiring | "
                               "exp169 f_max/THRESHOLD | exp167 R_T | "
                               "exp145/148 PN+TC | exp142 "
                               "execute_signed@STAR_OP==S*")},
        "battery": {
            "hosts": CLASS_ORDER,
            "host_source": ("exp243's deposit records ONLY: the 12 "
                            "classes' base media rebuilt at exp243's "
                            "own deposited rewire seeds and bit-asserted "
                            "against exp243's base_sha256 / edges_base "
                            "records (H0/H1 the chain/path constructor "
                            "-> path(400), the H0 slot echoing H1 "
                            "bit-exactly); zero new knobs"),
            "arms": {
                ARM_CANON: ("exp243's canonical P1/P2 candidates: the "
                            "canon row read on the mirror medium (P1) "
                            "and on the boundary-double medium (P2); "
                            "the row's worst err = the arm's max at "
                            "that seed (exp255's worst_canon, "
                            "per-seed)"),
                ARM_SUBST: ("exp243's P3 deep-band substitution "
                            "candidates: the deep band's -60.0 rung "
                            "rows, BOTH pre-named instances, on the "
                            "base medium; the row's worst err = the "
                            "arm's max at that seed (exp255's "
                            "worst_p3, per-seed)")},
            "tie_break": ("within-arm worst-instance ties resolved to "
                          "the FIRST instance in the pre-named order "
                          "(P1 before P2; deep i0 before i1) — "
                          "exp243's argmax rule; ties censused in R4"),
            "decomposition_rule": ("each row's decomposition = exp208's "
                                   "classify(T_row, W_row) + decompose "
                                   "on the row's WORST instance's own "
                                   "state-carrying read (exp243's A3 "
                                   "path)"),
            "seeds": list(SEEDS_RUN), "n": int(N400),
            "rows_per_pass": 72, "decodes_per_pass": 144,
            "classes": {k: {
                "base_sha256": dep243["classes"][k]["base_sha256"],
                "edges_base": int(dep243["classes"][k]["edges_base"]),
                "rewire_seed": dep243["classes"][k]["rewire_seed"],
                "f_max_base": float(dep243["classes"][k]["f_max_base"]),
                "n_boundary_cells_base":
                    int(dep243["classes"][k]["n_boundary_cells_base"]),
                "media_sha256": {
                    "mirror": _a_sha(p1_mirror(bases400[k])),
                    "boundary_double": _a_sha(
                        p2_boundary_double(
                            bases400[k],
                            labeling_bfs_n(bases400[k]))[0]),
                    "base": _a_sha(bases400[k])}}
                for k in CLASS_ORDER}},
        "provenance": {
            "exp243": sha243_after,
            "exp182": sha182,
            "exp255": sha255,
            "pre_registration": "commit 276e41e (batch 22)",
            "exp255_host_level_reference": {
                "rho_canon": rho_canon_host, "rho_p3": rho_p3_host,
                "branch": dep255["branch"]}},
        "instrument_identity": {
            "multi_identity_audits":
                (f"{len(audits)}/{len(audits)} bit-identical"
                 if audits_ok else "DRIFT"),
            "audit_records": audits,
            "build_rows_H0_n100_checksums": True,
            "media_rebuild_sha_asserts": True,
            "boundary_count_reasserts": True,
            "exp243_battery_reproduction": (
                "all 48 candidate records' errs and verified flags "
                "reproduced EXACTLY per seed (the exp142 2-dp "
                "convention) — the battery IS exp243's machine")},
        "rows": rows1,
        "determinism": gates["R4_discipline"]["determinism"],
        "regressions": {
            "regressor": "per-row PAIR-JUNCTION count (exp208's "
                         "classify on the row's own target and medium)",
            "response": "per-row worst err (the arm's max at that "
                        "seed)",
            "rho_all_72": rho_all,
            "rho_substituted_36": rho_sub,
            "rho_canonical_36": rho_can,
            "within_host": {
                "method": gates["R3_host_null_sharpened"]["method"],
                "pooled_within_host_rank_pearson": pooled_r,
                "ols_slope": ols_slope,
                "ols_intercept": ols_intercept,
                "per_host_spearman": per_host}},
        "gates": gates,
        "branch": branch,
        "verdict": verdict,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically (verified by the run agent "
                         "across processes)")}
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(deposit, f, indent=1, default=float)
    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k}: {'PASS' if g['pass'] else 'FAIL'}")
    print(f"  rho_all {rho_all:.4f} | rho_subst {rho_sub:.4f} vs "
          f"rho_canon {rho_can:.4f} | pooled within-host {pooled_r:.4f}")
    print(f"  determinism: {'bit-identical' if deterministic else 'DRIFT'} "
          f"(2 passes x 72 rows); worst-instance ties {n_tied}")
    print(f"  deposited {out_path}")
    # THE FLOOR ASSERT AT EXIT (the pre-registration's R4; exp243's
    # closing line VERBATIM)
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
