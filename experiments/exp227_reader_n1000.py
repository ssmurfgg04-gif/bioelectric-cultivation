#!/usr/bin/env python3
"""exp227 — THE READER AT n=1000 (L199's registered next).

The structured-media adversarial reader held at 0.62 mV worst (L199)
— under the random baseline. The size axis's terminal point for the
reader line: the same structured-media sweep at n=1000 — path(1000)
as host + the corner battery at n=1000, 5 target classes x 3 seeds,
the 6.0 bar unchanged. If the reader holds at n=1000, the media-
independence claim carries to the scale where the n=400 corner
battery's boundary phenomenon (exp208) can be re-examined at a second
large n.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp225's sweep machinery
verbatim (the production scoped read, the target classes, the 3
seeds); the hosts: path(1000) (exp198's scale constructor — the SAME
constructor that builds A_CHAIN and H1) + the n=1000 corner battery
(exp166's CornerMedium at n=1000, 5 instances, gen-seed rule
166000 + j); the floors asserted post-restore (exp218's exp169-import
discipline VERBATIM — the body MUST restore CORE.NEURAL_SPEC_MIN =
-60.0 after the import chain and disclose it).

GATES (each evaluated exactly once):
  GATE-E1 (the n=1000 sweep) path(1000): 5 target classes x 3 seeds
           decode with zero rejections under the 6.0 bar; the corner
           battery at n=1000: 5 instances x 3 seeds decode with zero
           rejections; complete, not sampled.
  GATE-E2 (the reader bar) every err finite and < 6.0; the per-host
           worst-case deposited; the n=1000 worst vs the n=400
           structured worst (0.62, L199) and the random worst (1.45)
           deposited as the contrast reading.
  GATE-E3 (the boundary signature at n=1000) the corner battery's
           decomposition at n=1000 (exp208's three-class machinery
           verbatim): the CANON-BOUNDARY excess vs the interior
           (the interior-0.000 identity exp208 named, re-tested at
           the second large n) — the branch named: REPRODUCED
           (interior excess 0.000 exactly at 2-dp) / DRIFTED.
  GATE-E4 (hygiene) zero rejections; all finite; the floor
           discipline asserted and disclosed.
NO post-hoc tuning. --smoke permitted (path(1000), 1 target), discarded.
DEPOSIT: results/exp227_reader_n1000.json
RUN: python3 -m experiments.exp227_reader_n1000 [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp227_reader_n1000.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline; gates below evaluated exactly once) =======
    import hashlib
    import time

    # exp166's thread discipline (single-threaded BLAS — determinism
    # hygiene for the n=1000 decodes; set BEFORE numpy's first import)
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "path", "corner"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

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
    from experiments.exp166_leading_edge import (  # noqa: E402
        CornerMedium, cell_dims)
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp218's disclosed exp169-import
    #      discipline, VERBATIM from exp225's reader-line application):
    #      the reader-line imports (exp167 -> exp169) carry an
    #      import-time instrument pin that flips the reader-world floor
    #      -35.0 onto (collective, exp142, exp145, exp148, exp94). The
    #      read-chain modules captured CF-1's production -60.0 at their
    #      own import (the pins are attribute-only); restored here so
    #      the reader's commit branch runs at the CF-1 production floor
    #      the pre-registration asserts — the deep band's -60.0 rung is
    #      decodable ONLY at the production floor.
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

    BAR = ERR_BAR                          # 6.0 — exp151/155's verify bar
    N1000 = 1000                           # the size axis's terminal rung
    # the n=1000 corner battery (the pre-registration's fresh cohort —
    # NO replay target): exp166's CornerMedium at the c6 cell (o+h —
    # the tail class whose CANON-BOUNDARY excess exp208 named; the
    # boundary-signature battery exp213/216/221 re-used), 5 instances,
    # the pre-registered gen-seed rule 166000 + j (j = 0..4). Disclosed
    # here as the pre-named cell mapping behind "the corner battery".
    CORNER_CELL = 6
    CORNER_INSTANCES = 5
    CORNER_SEED_BASE = 166000
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    MANIFEST_INDICES = (0, 49, 99)         # the union's carried targets
    #                                     #   (pre-named)
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP198 = os.path.join(ROOT, "results",
                          "exp198_adversarial_reader_n400.json")
    DEP199 = os.path.join(ROOT, "results",
                          "exp199_ro_n400_tail.json")
    DEP225 = os.path.join(ROOT, "results",
                          "exp225_structured_media_reader.json")
    for _p in (DEP182, DEP198, DEP199, DEP225):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    # ---- the one frozen read configuration (exp160's discipline;
    #      fingerprinted, asserted identical pre/post run) ------------
    READ_CONFIG = {
        "wiring": ("exp178's production scoped arm: exp169's f_max "
                   "diagnostic + the pre-registered THRESHOLD (32.0); "
                   "R_T (exp167's adopted read) iff f_max < 32.0, else "
                   "exp148's raw temporal — one arm, one function, zero "
                   "knobs"),
        "projection": ("exp145/exp148 TC1-TC3: PN1/PN2 dominant-quadrature "
                       "projection + TC1 flip-clock F + TC2 A_ext = A + F"),
        "executor": ("exp142 execute_signed VERBATIM (R1 structure on "
                     "|A|, R2 signed dynamics, walk frontier on |A|>0)"),
        "op": {"gamma": 64.0, "mu": 0.0},
        "op_source": ("exp99's battery-wide STAR point (exp142's "
                      "STAR_OP); STAR_OP IS S* = (64.0, 0.0), asserted"),
        "spec_input": ("per-row target spec — the read stack's target "
                       "parameter (exp148's MULTI default asserted "
                       "bit-identical on path(1000) by the "
                       "MULTI-identity audit)"),
        "seeds": list(SEEDS),
        "n": N1000,
        "window_h": 24.0,
        "commit_noise": 0.6,
        "steps_per_cell": 8,
        "floor": ("production -60.0 restored post-import (exp218's "
                  "disclosed exp169-import discipline; the -35.0 "
                  "reader-line pin disclosed)"),
        "per_media_tuning": "none",
    }

    def _fingerprint() -> str:
        return hashlib.sha256(
            json.dumps(READ_CONFIG, sort_keys=True).encode()
        ).hexdigest()[:16]

    FP = _fingerprint()

    # ---- the S* identity of the reader's executor ---------------------
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the reader's executor op {STAR_OP} != S* {S_STAR}"

    with open(DEP182) as fh:
        dep182 = json.load(fh)
    with open(DEP225) as fh:
        dep225 = json.load(fh)

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
        _LOCK_LOG.append((host, row_key, int(seed)))

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    # ---- THE MEDIUM 1: path(1000) — exp198's scale constructor (the
    #      SAME graph_path that builds exp136's A_CHAIN and exp198/
    #      exp225's H1) — the host's own W as a static single-frame
    #      decode medium (exp225's HostWMedium VERBATIM).
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
    #      wiring) — exp225's replica VERBATIM (its MULTI-identity
    #      audit asserts the replica IS exp148.decode("scoped", ...)).
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

    def _decode_row(host, row_key, spec, med, seed, fmax):
        """One decode; a rejection is RECORDED, never hidden (exp142's
        zero-rejection hygiene; the caller counts)."""
        _lock_read(host, row_key, seed)
        try:
            out = _scoped_row_read(spec, med, seed, fmax)
            err = float(out["err_vs_target"])
            if not np.isfinite(err):
                raise ValueError(f"non-finite decode err {err}")
            return {"ok": True, "err": err,
                    "verified": bool(out.get("program_verified", False)),
                    "rho": out.get("rho"), "branch": out.get("branch")}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- the per-host target rows (exp225's build_rows VERBATIM, at
    #      the host's own n): the host's own canon (wildtype) + 3 union
    #      targets (manifest indices 0, 49, 99) + the deep band's -60.0
    #      rung both instances. 5 target classes; 6 decode rows (the
    #      deep rung carries BOTH pre-named instances). The dep182
    #      manifest checksums live at n=100 — the checksum assert fires
    #      on the n=100 rebuild only (the instrument-identity audit);
    #      at n=1000 the same construction is re-run parameterized
    #      (disclosed — no deposited n=1000 checksum exists).
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    def build_rows(canon: np.ndarray, n: int) -> list:
        rows = []
        # (a) the host's own canon (wildtype): the empty program —
        #     spec_target_n of the zero-zone spec IS the canon target.
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp227-host-canon",
                             somatic_latch=False)
        f_c = spec_target_n(spec_c, canon, n)
        assert np.array_equal(f_c, canon), "canon row target != canon"
        rows.append({"tclass": "canon", "key": "canon", "spec": spec_c,
                     "f": f_c, "f_sha256": _f_sha(f_c)})
        # (b) the union's carried targets: manifest indices 0/49/99
        #     (exp214's manifest rebuild VERBATIM; checksummed at n=100).
        for m in _manifest:
            if m["index"] not in MANIFEST_INDICES:
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
            if n == int(g6.N):
                assert sha == m["f_sha256"], \
                    (f"manifest checksum mismatch at the n=100 rebuild "
                     f"(target {m['index']}): rebuilt {sha} != "
                     f"deposited {m['f_sha256']}")
            rows.append({"tclass": "manifest",
                         "key": f"m{m['index']}", "index": m["index"],
                         "spec": spec, "f": f, "f_sha256": sha,
                         "zone_count": m["zone_count"],
                         "vmin": m["vmin"], "vmax": m["vmax"]})
        # (c) the deep band's -60.0 rung, both instances (exp214's
        #     deep construction VERBATIM).
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
            rows.append({"tclass": "deep",
                         "key": f"r{DEEP_RUNG:g}i{inst}",
                         "rung": DEEP_RUNG, "instance": inst,
                         "spec": spec, "f": f, "f_sha256": _f_sha(f)})
        assert len(rows) == 6, "row build drifted"
        # the pre-registration's 5 targets = 1 canon + 3 manifest
        # + the -60.0 rung (both pre-named instances = 2 deep rows)
        assert sum(1 for r in rows if r["tclass"] == "canon") == 1
        assert sum(1 for r in rows if r["tclass"] == "manifest") == 3
        assert sum(1 for r in rows if r["tclass"] == "deep") == 2
        return rows

    # ---- HOST 1: path(1000) — exp198's scale constructor VERBATIM ----
    def build_path_host() -> dict:
        A = graph_path(N1000)
        canon = labeling_bfs_n(A)
        assert np.array_equal(canon, g6.wildtype_target(N1000)), \
            "path(1000) canon != wildtype_target(1000)"
        # the instrument-identity audit: the row-build machinery on the
        # n=100 canon reproduces dep182's manifest checksums exactly
        # (exp225's H0 assert, kept as the same-instrument proof)
        build_rows(labeling_bfs_n(g6.A_CHAIN), int(g6.N))
        return {"name": "path1000", "n": N1000, "A": A, "canon": canon}

    def run_path_host(h: dict, seeds, rows_override=None) -> dict:
        A, canon, n = h["A"], h["canon"], h["n"]
        med = HostWMedium(A)
        # the medium's own canon IS the host's canon (the "host's own
        # W" property — asserted, not assumed)
        assert np.array_equal(labeling_bfs_n(np.abs(med.A)), canon), \
            f"{h['name']}: the medium's own canon != the host's canon"
        fmax = float(f_max_frames(list(med.snapshots())))
        cls = ("diffuse" if fmax < SCOPED_THRESHOLD
               else "concentrated")
        assert SCOPED_THRESHOLD == 32.0, "scoped threshold drifted"
        rows = build_rows(canon, n)
        if rows_override is not None:
            rows = rows_override
        # the per-host MULTI-identity audit (credited run only): the
        # parameterized scoped wiring IS exp148.decode("scoped", ...)
        # at the production default target input (bit-exact on
        # err/verified/rho/branch)
        audit_ok = None
        prod_err = None
        if rows_override is None:
            prod = exp148_decode("scoped", med, seeds[0], f_max=fmax)
            mine = _scoped_row_read(MULTI, med, seeds[0], fmax)
            audit_ok = bool(
                prod["ok"]
                and float(prod["err"]) == float(mine["err_vs_target"])
                and prod["verified"]
                == bool(mine["program_verified"])
                and prod.get("rho") == mine.get("rho")
                and prod.get("branch") == mine.get("branch"))
            if not audit_ok:
                raise AssertionError(
                    f"{h['name']}: the parameterized scoped wiring "
                    f"drifted from exp148.decode('scoped')")
            prod_err = (float(prod["err"]) if prod["ok"] else None)
        per_row = []
        for r in rows:
            recs = []
            for s in seeds:
                out = _decode_row(h["name"], r["key"], r["spec"],
                                  med, s, fmax)
                rec = {"seed": int(s)}
                if out["ok"]:
                    rec.update(err=out["err"], verified=out["verified"],
                               rho=out.get("rho"),
                               branch=out.get("branch"))
                else:
                    rec.update(rejection=out["rejection"])
                recs.append(rec)
            errs = [x["err"] for x in recs if "err" in x]
            per_row.append({
                "tclass": r["tclass"], "key": r["key"],
                "index": r.get("index"), "rung": r.get("rung"),
                "instance": r.get("instance"),
                "f_sha256": r["f_sha256"],
                "errs": errs,
                "verified": [x.get("verified") for x in recs
                             if "err" in x],
                "median_err": (float(np.median(errs)) if errs else None),
                "seeds": [int(s) for s in seeds], "records": recs})
            print(f"  [{h['name']} {r['tclass']} {r['key']}] errs "
                  f"{[round(e, 2) for e in errs]}")
        all_errs = [e for r in per_row for e in r["errs"]]
        n_rej = sum(1 for r in per_row for x in r["records"]
                    if "rejection" in x)
        return {"host": h["name"], "n": int(n),
                "kind": ("exp198's scale constructor (graph_path) at "
                         "the size axis's terminal rung"),
                "edges": int(np.count_nonzero(np.triu(A, 1))),
                "f_max": fmax, "dispatch_class": cls,
                "seeds": [int(s) for s in seeds],
                "n_rows": len(per_row),
                "n_decodes": len(all_errs) + n_rej,
                "n_rejections": n_rej,
                "worst_err": (float(max(all_errs)) if all_errs else None),
                "median_err": (float(np.median(all_errs))
                               if all_errs else None),
                "per_row": per_row,
                "multi_identity_audit": {"seed": int(seeds[0]),
                                         "bit_identical": audit_ok,
                                         "prod_err": prod_err}}

    # ---- exp208's three-class decomposition machinery VERBATIM -------
    # (the boundary-signature instrument; classify + decompose copied
    # byte-for-byte from exp208_c6_tail_ablation, zero knobs)
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

    # ---- HOST 2: the n=1000 corner battery (exp198's decode call
    #      site + exp208's state-carrying decode, VERBATIM) ------------
    def run_corner(seeds) -> dict:
        insts: list = []
        errs_all: list = []
        n_rej = 0
        rej_records: list = []
        for j in range(CORNER_INSTANCES):
            gen_seed = CORNER_SEED_BASE + j   # the pre-registered rule
            # THE n=1000 construction: exp166's CornerMedium VERBATIM —
            # n is the constructor's FIRST PARAMETER (exp181 called it
            # with 100; exp198/199 with 400; this battery at 1000),
            # asserted at build time below.
            med = CornerMedium(N1000, gen_seed, cell_dims(CORNER_CELL))
            assert med.n == N1000, \
                f"CornerMedium built off n={N1000}: got n={med.n}"
            fmax = float(f_max_frames(list(med.snapshots())))
            cls = ("diffuse" if fmax < SCOPED_THRESHOLD
                   else "concentrated")
            rec = {"j": j, "gen_seed": gen_seed, "cell": CORNER_CELL,
                   "n": int(med.n),
                   "violated": list(med.violated), "T": int(med.T_eff),
                   "p_keep": round(float(med.p_keep), 3),
                   "n_hyper": int(med.n_hyper),
                   "n_oneway": int(med.n_oneway),
                   "f_max": fmax, "class": cls,
                   "errs": [], "verified": [], "branch": [], "rho": [],
                   "decompositions": []}
            for s in seeds:
                # THE one call site — exp208's production decode,
                # VERBATIM (the scoped arm, state carried for E3)
                out = exp148_decode("scoped", med, s, return_state=True,
                                    f_max=fmax)
                _lock_read(f"corner_j{j}", f"gen{gen_seed}", s)
                if not out["ok"]:
                    n_rej += 1                # RECORDED, never hidden
                    rej_records.append({"j": j, "seed": int(s),
                                        "f_max": fmax,
                                        "rejection": out["rejection"]})
                    continue
                err = float(out["err"])
                assert np.isfinite(err), \
                    f"non-finite decode err at j{j} s{s}"
                rec["errs"].append(err)
                rec["verified"].append(bool(out["verified"]))
                rec["branch"].append(out.get("branch"))
                rec["rho"].append(float(out["rho"])
                                  if out.get("rho") is not None else None)
                errs_all.append(err)
                # E3's input: the decomposition from the returned state
                V = np.asarray(out["state"]["V"], dtype=float)
                T = np.asarray(out["state"]["target"], dtype=float)
                cinfo = classify(T, med.Wbase)
                err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
                assert round(err_exact, 2) == round(err, 2), \
                    "state err vs reported err drift"
                rec["decompositions"].append(
                    decompose(V, T, cinfo["class"], err_exact))
            rec["median_err"] = (float(np.median(rec["errs"]))
                                 if rec["errs"] else None)
            rec["worst_err"] = (float(max(rec["errs"]))
                                if rec["errs"] else None)
            insts.append(rec)
            print(f"  [corner j{j}] cell c{CORNER_CELL} "
                  f"gen_seed {gen_seed} errs "
                  f"{[round(e, 2) for e in rec['errs']]} "
                  f"({cls}, f_max {fmax})")
        meds = [r["median_err"] for r in insts if r["median_err"]
                is not None]
        return {"battery": ("exp166's CornerMedium at n=1000, the c6 "
                            "cell (o+h — exp208's boundary-signature "
                            "battery class), 5 instances, gen-seed rule "
                            "166000 + j (pre-registered, fresh cohort)"),
                "n_instances": len(insts),
                "n_build": int(N1000),
                "seeds": [int(s) for s in seeds],
                "n_decodes": len(errs_all) + n_rej,
                "n_rejections": n_rej,
                "rejection_records": rej_records,
                "median_err": (float(np.median(errs_all)) if errs_all
                               else None),
                "median_of_instance_medians": (float(np.median(meds))
                                               if meds else None),
                "worst_err": (float(max(errs_all)) if errs_all
                              else None),
                "n_diffuse": sum(1 for r in insts
                                 if r["class"] == "diffuse"),
                "n_concentrated": sum(1 for r in insts
                                      if r["class"] == "concentrated"),
                "instances": insts}

    # ---- dispatch ------------------------------------------------------
    jobs = (["path", "corner"] if args.job == "all"
            else [args.job])
    hosts = build_path_host() if (args.smoke or "path" in jobs) else None
    seeds_run = (1,) if args.smoke else tuple(SEEDS)
    mode = ("SMOKE path(1000) 1 target - discarded" if args.smoke else
            f"FULL jobs={jobs} seeds={seeds_run}")
    print(f"=== exp227: THE READER AT n=1000 ({mode}) ===")
    print(f"  read: exp178's production scoped arm, fingerprint {FP}; "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})\n")

    result: dict = {}
    if not args.smoke and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("sections", {})

    if args.smoke:
        h = hosts
        # 1 target = the canon row only (the pre-registered smoke scope)
        sec = run_path_host(h, seeds_run,
                            rows_override=build_rows(h["canon"],
                                                     h["n"])[:1])
        print(f"\n  SMOKE (path(1000), 1 target) decodes "
              f"{sec['n_decodes']} rejections {sec['n_rejections']} "
              f"worst {sec['worst_err']} - DISCARDED (no deposit, "
              f"gates not evaluated)")
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        return {"exp": "exp227_reader_n1000", "smoke": True,
                "verdict": "smoke (discarded)"}

    for j in jobs:
        ts = time.time()
        if j == "path":
            sec = run_path_host(hosts, seeds_run)
            sec["runtime_s"] = round(time.time() - ts, 1)
            sec["m4_evidence"] = {
                "floors_pre_restore": dict(_PRE_RESTORE),
                "floor_post_restore": PROD_FLOOR,
                "fingerprint": FP,
                "threshold": SCOPED_THRESHOLD,
                "multi_identity_bit_identical":
                    sec["multi_identity_audit"]["bit_identical"]}
            result["sections"]["path1000"] = sec
            print(f"\n  [path1000] n={hosts['n']} "
                  f"edges={sec['edges']} f_max={sec['f_max']} "
                  f"({sec['dispatch_class']}) worst {sec['worst_err']} "
                  f"median {sec['median_err']} rejections "
                  f"{sec['n_rejections']} ({sec['runtime_s']} s)\n")
        else:
            sec = run_corner(seeds_run)
            sec["runtime_s"] = round(time.time() - ts, 1)
            sec["m4_evidence"] = {
                "floors_pre_restore": dict(_PRE_RESTORE),
                "floor_post_restore": PROD_FLOOR,
                "fingerprint": FP,
                "threshold": SCOPED_THRESHOLD}
            result["sections"]["corner_n1000"] = sec
            print(f"\n  [corner_n1000] {sec['n_instances']} instances "
                  f"worst {sec['worst_err']} median "
                  f"{sec['median_err']} rejections "
                  f"{sec['n_rejections']} ({sec['runtime_s']} s)\n")
        # incremental partial deposit (the runner-split discipline)
        result["verdict"] = (f"partial - sections "
                             f"{sorted(result['sections'])} merged; "
                             f"gates pending path1000 + corner_n1000")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)

    # merge discipline: gates close only on the complete cohort
    want = ["corner_n1000", "path1000"]
    got = sorted(result["sections"].keys())
    if got != want:
        print(f"  partial deposit written ({out_path}); rerun the "
              f"remaining job to close the gates")
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        return result

    path_sec = result["sections"]["path1000"]
    corner_sec = result["sections"]["corner_n1000"]

    # ================= THE GATES (each evaluated exactly once) =========
    path_errs = [e for r in path_sec["per_row"] for e in r["errs"]]
    corner_errs = [e for r in corner_sec["instances"] for e in r["errs"]]
    all_errs = path_errs + corner_errs
    n_rej = path_sec["n_rejections"] + corner_sec["n_rejections"]
    n_decodes = path_sec["n_decodes"] + corner_sec["n_decodes"]
    expected = 6 * len(seeds_run) + CORNER_INSTANCES * len(seeds_run)
    seeds_ok = (all(r["seeds"] == list(seeds_run)
                    for r in path_sec["per_row"])
                and corner_sec["seeds"] == list(seeds_run)
                and all(i["gen_seed"] == CORNER_SEED_BASE + i["j"]
                        for i in corner_sec["instances"]))
    complete = bool(seeds_ok
                    and path_sec["n_decodes"] == 6 * len(seeds_run)
                    and corner_sec["n_decodes"]
                    == CORNER_INSTANCES * len(seeds_run)
                    and len(path_sec["per_row"]) == 6
                    and len(corner_sec["instances"])
                    == CORNER_INSTANCES
                    and not args.smoke)
    per_host_worst = {"path1000": path_sec["worst_err"]}
    per_host_worst.update({f"corner_j{i['j']}": i["worst_err"]
                           for i in corner_sec["instances"]})
    all_finite = bool(all_errs) and all(np.isfinite(all_errs))

    # E2's contrast reading (recorded, not gated on a bar): the n=1000
    # worst vs the n=400 structured worst (exp225's deposited 0.62,
    # L199) and the random worst (exp198/199's pooled 1.45) — re-read
    # from the deposits at run time
    with open(DEP198) as f:
        d198 = json.load(f)
    with open(DEP199) as f:
        d199 = json.load(f)
    worst198 = max(e for sec_ in d198["cells"].values()
                   for r in sec_["instances"] for e in r["errs"])
    worst199 = max(e for sec_ in d199["cells"].values()
                   for r in sec_["instances"] for e in r["errs"])
    random_worst = float(max(worst198, worst199))
    structured_worst_400 = float(dep225["structured_worst_err"])
    worst_1000 = float(max(all_errs))

    # E3: the boundary signature at n=1000 — exp208's machinery applied
    # to the corner battery's decompositions (5 instances x 3 seeds)
    def class_means(decomps) -> dict:
        rows_ = {k: [] for k in ("CANON-BOUNDARY", "PAIR-JUNCTION",
                                 "INTERIOR")}
        for d in decomps:
            for p in d["per_class"]:
                rows_[p["class"]].append(p["rms_contrib_mV"])
        return {k: (float(np.mean(v)) if v else None)
                for k, v in rows_.items()}

    decomp_all = [d for i in corner_sec["instances"]
                  for d in i["decompositions"]]
    means_n1000 = class_means(decomp_all)
    interior_mean = means_n1000["INTERIOR"]
    # the interior-0.000 identity (exp208's deposit: INTERIOR mean rms
    # 0.000 EXACTLY — the interior carries zero excess): the branch is
    # REPRODUCED iff the interior mean is 0.000 exactly at 2-dp
    branch_e3 = ("REPRODUCED"
                 if interior_mean is not None
                 and round(interior_mean, 2) == 0.0 else "DRIFTED")
    excess_e3 = {k: ((means_n1000[k] - interior_mean)
                     if (means_n1000[k] is not None
                         and interior_mean is not None) else None)
                 for k in means_n1000}
    boundary_share = float(np.mean(
        [p["frac_of_sq"] for d in decomp_all
         for p in d["per_class"] if p["class"] == "CANON-BOUNDARY"])) \
        if decomp_all else None

    fp_post = _fingerprint()
    audits_ok = bool(path_sec["multi_identity_audit"]["bit_identical"])
    floors_ok = bool(
        path_sec["m4_evidence"]["floor_post_restore"] == PROD_FLOOR
        and all(v == READER_PIN_FLOOR for v in
                path_sec["m4_evidence"]["floors_pre_restore"].values())
        and corner_sec["m4_evidence"]["floor_post_restore"]
        == PROD_FLOOR
        and all(v == READER_PIN_FLOOR for v in
                corner_sec["m4_evidence"]["floors_pre_restore"]
                .values()))
    thresholds_ok = bool(
        path_sec["m4_evidence"]["threshold"] == 32.0
        and corner_sec["m4_evidence"]["threshold"] == 32.0)
    lock_ok = len(_LOCK_LOG) == n_decodes
    e4 = bool(n_rej == 0 and all_finite and floors_ok and thresholds_ok
              and audits_ok and lock_ok and fp_post == FP)

    gates = {
        "E1_n1000_sweep": {
            "pass": bool(n_rej == 0 and n_decodes == expected
                         and complete),
            "decodes": n_decodes, "expected": expected,
            "rejections": n_rej, "complete_not_sampled": complete,
            "path1000": {"rows": path_sec["n_rows"],
                         "decodes": path_sec["n_decodes"],
                         "rejections": path_sec["n_rejections"]},
            "corner_battery": {"instances": corner_sec["n_instances"],
                               "decodes": corner_sec["n_decodes"],
                               "rejections": corner_sec["n_rejections"]},
            "n_target_classes": 5,
            "note": ("the pre-registration's '5 targets' = the 5 "
                     "pre-named target classes; the deep band's -60.0 "
                     "rung carries BOTH pre-named instances (2 decode "
                     "rows), per exp225's pre-named target list")},
        "E2_reader_bar": {
            "pass": bool(all_finite
                         and all(e < BAR for e in all_errs)),
            "bar_mV": BAR, "n_finite": int(np.sum(np.isfinite(all_errs))),
            "worst_err_n1000": worst_1000,
            "per_host_worst_case": per_host_worst,
            "contrast": {
                "structured_worst_n400": structured_worst_400,
                "structured_worst_source":
                    "exp225's deposit (L199), re-read at run time",
                "random_worst": random_worst,
                "random_worst_source":
                    (f"exp198 pooled max {worst198} + exp199 pooled "
                     f"max {worst199}, re-read at run time"),
                "reading": (f"n=1000 worst {worst_1000} vs n=400 "
                            f"structured worst {structured_worst_400} "
                            f"vs random worst {random_worst}")}},
        "E3_boundary_signature": {
            "pass": bool(branch_e3 == "REPRODUCED"),
            "branch": branch_e3,
            "n_decompositions": len(decomp_all),
            "mean_rms_contrib_mV": means_n1000,
            "excess_vs_interior_mV": excess_e3,
            "interior_identity": (f"INTERIOR mean {interior_mean} — "
                                  f"{'0.000 exactly at 2-dp' if branch_e3 == 'REPRODUCED' else 'DRIFTED'}"
                                  f" (exp208's deposited identity, "
                                  f"re-tested at the second large n)"),
            "boundary_frac_of_sq_mean": boundary_share,
            "conventions": ("CANON-BOUNDARY: a lattice neighbor's "
                            "target value differs (the ring backbone); "
                            "PAIR-JUNCTION: endpoint of >= 2 chords in "
                            "the medium's pair support |Wbase| > 0; "
                            "precedence = the registered listing "
                            "order; the accounting identity on the "
                            "mean-squared (mV^2) scale — exp208's "
                            "machinery verbatim")},
        "E4_hygiene": {
            "pass": e4,
            "rejections": n_rej, "all_finite": all_finite,
            "floor_discipline": (f"production {PROD_FLOOR} restored "
                                 f"post-import on all pinned modules; "
                                 f"the {READER_PIN_FLOOR} reader-line "
                                 f"pin disclosed (exp218's discipline)"),
            "floors_pre_restore": dict(_PRE_RESTORE),
            "threshold_asserted": 32.0,
            "multi_identity_audit": ("path1000 bit-identical" if audits_ok
                                     else "DRIFT"),
            "s_star_identity": (f"STAR_OP == S* == {S_STAR}, asserted"),
            "lock_log_entries": len(_LOCK_LOG),
            "fingerprint_pre": FP, "fingerprint_post": fp_post,
            "per_media_tuning": "none"},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = (f"{n_pass}/{len(gates)} gates - E3 {branch_e3} (interior "
               f"{interior_mean}); worst {worst_1000} vs n=400 "
               f"structured {structured_worst_400} / random "
               f"{random_worst}")

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    deposit = {
        "exp": "exp227_reader_n1000",
        "claim": ("THE READER AT n=1000 (L199's registered next): the "
                  "structured-media adversarial reader held at 0.62 mV "
                  "worst at n=400 — the size axis's terminal point for "
                  "the reader line: the same structured-media sweep at "
                  "n=1000 — path(1000) as host (exp198's scale "
                  "constructor, the SAME constructor that builds "
                  "A_CHAIN and H1) + the n=1000 corner battery "
                  "(exp166's CornerMedium at n=1000, 5 instances, "
                  "gen-seed rule 166000 + j), 5 target classes x 3 "
                  "seeds, the 6.0 bar unchanged — and the corner "
                  "battery's boundary decomposition (exp208's "
                  "three-class machinery verbatim) re-testing the "
                  "interior-0.000 identity at the second large n"),
        "read": {**READ_CONFIG, "fingerprint": FP,
                 "wiring_id": ("exp148.decode('scoped') wiring | "
                               "exp169 f_max/THRESHOLD | exp167 R_T | "
                               "exp145/148 PN+TC | exp142 "
                               "execute_signed@STAR_OP==S*")},
        "cohort": {
            "hosts": ["path1000", "corner_n1000"],
            "seeds": list(seeds_run),
            "target_list": ("the host's own canon (wildtype) + manifest "
                            "indices 0, 49, 99 + the deep band's -60.0 "
                            "rung both instances (pre-named; exp225's "
                            "target classes)"),
            "n_target_classes": 5, "n_decode_rows_path1000": 6,
            "corner_cell_mapping": ("the pre-registered 'corner "
                                    "battery' = exp166's CornerMedium "
                                    f"at the c{CORNER_CELL} cell (o+h), "
                                    "the battery class exp208's "
                                    "boundary phenomenon was named on; "
                                    "disclosed as the pre-named cell "
                                    "mapping")},
        "provenance": {
            "exp182": _sha(DEP182), "exp198": _sha(DEP198),
            "exp199": _sha(DEP199), "exp225": _sha(DEP225)},
        "sections": result["sections"],
        "pooled_median_err": (float(np.median(all_errs))
                              if all_errs else None),
        "worst_err_n1000": worst_1000,
        "boundary_signature": {
            "mean_rms_contrib_mV": means_n1000,
            "excess_vs_interior_mV": excess_e3,
            "branch": branch_e3,
            "boundary_frac_of_sq_mean": boundary_share},
        "contrast": {
            "structured_worst_n400": structured_worst_400,
            "random_worst": random_worst,
            "worst_err_n1000": worst_1000},
        "gates": gates,
        "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(deposit, f, indent=1)
    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k}: {'PASS' if g['pass'] else 'FAIL'}")
    print(f"  pooled median {float(np.median(all_errs)):.3f} mV | "
          f"n=1000 worst {worst_1000} vs n=400 structured "
          f"{structured_worst_400} / random {random_worst}")
    print(f"  E3: {branch_e3} — interior {interior_mean} (the exp208 "
          f"identity at the second large n)")
    print(f"  deposited {out_path}")
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
