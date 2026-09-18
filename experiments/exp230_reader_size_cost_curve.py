#!/usr/bin/env python3
"""exp230 — THE READER SIZE-COST CURVE (L204's registered next).

The reader's worst-err profile is graded in n: 1.45 (random, n=100),
0.62 (structured, n=400), 3.42 (structured, n=1000). The registered
measurement: the size-cost curve as ONE deposited line — the worst-err
vs n profile at n = 100/200/400/700/1000 on the path constructor (the
A_CHAIN family), 5 target classes x 3 seeds per n, the 6.0 bar
unchanged; PLUS the E1 checker repair (the completeness predicate
rebuilt from the deposited grid definition, re-run as a hygiene-only
pass — no gate rewrite).

========================= pre-registration =========================
Committed BEFORE any run. Instruments: exp225/exp227's sweep machinery
verbatim (the production scoped read, the target classes, the 3
seeds); the ns (pre-named): 100, 200, 400, 700, 1000; the target
classes per exp225's pre-named list; the floor discipline per
exp218's exp169-import restore VERBATIM (disclosed).

GATES (each evaluated exactly once):
  GATE-N1 (the curve) 5 ns x 5 target classes x 3 seeds decode with
           zero rejections, every err finite; the curve (worst-err
           and mean-err vs n) deposited as one line.
  GATE-N2 (the bar) every err < 6.0 at every n (the reader holds
           across the whole measured size axis).
  GATE-N3 (the fit) the log-log slope of worst-err vs n deposited
           (the scaling exponent, zero fitting — one OLS line, the
           value disclosed); the branch named: SUB-LINEAR (slope
           < 1) / LINEAR (1 <= slope < 2) / SUPER-LINEAR (>= 2).
  GATE-N4 (hygiene) zero rejections; all finite; the floor
           discipline asserted and disclosed; the completeness
           predicate built from the grid definition (the exp227 E1
           repair — hygiene only).
NO post-hoc tuning. --smoke permitted (n=200, 1 target), discarded.
DEPOSIT: results/exp230_reader_size_cost_curve.json
RUN: python3 -m experiments.exp230_reader_size_cost_curve [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results",
                   "exp230_reader_size_cost_curve.json")


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
    ap.add_argument("--job", choices=["all", "n100", "n200", "n400",
                                      "n700", "n1000"], default="all")
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
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp218's disclosed exp169-import
    #      discipline, VERBATIM from exp225/exp227's reader-line
    #      application): the reader-line imports (exp167 -> exp169)
    #      carry an import-time instrument pin that flips the
    #      reader-world floor -35.0 onto (collective, exp142, exp145,
    #      exp148, exp94). The read-chain modules captured CF-1's
    #      production -60.0 at their own import (the pins are
    #      attribute-only); restored here so the reader's commit branch
    #      runs at the CF-1 production floor the pre-registration
    #      asserts — the deep band's -60.0 rung is decodable ONLY at
    #      the production floor.
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
    assert BAR == 6.0, "the 6.0 bar drifted"
    # the pre-named size axis (the registered grid)
    NS = (100, 200, 400, 700, 1000)
    N_ROWS = 6                # 5 target classes; the deep rung carries
    #                         # BOTH pre-named instances (2 decode rows)
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    MANIFEST_INDICES = (0, 49, 99)         # the union's carried targets
    #                                     #   (pre-named)
    SEEDS_RUN = tuple(SEEDS)               # exp142's 3 seeds, verbatim
    # THE GRID DEFINITION (the one object the completeness predicate is
    # built from — the exp227 E1 repair: no hand-counted constants)
    GRID = {f"n{n}": {"n": int(n), "rows": N_ROWS,
                      "seeds": len(SEEDS_RUN),
                      "decodes": N_ROWS * len(SEEDS_RUN)} for n in NS}
    EXPECTED_TOTAL = sum(g["decodes"] for g in GRID.values())  # 90
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP225 = os.path.join(ROOT, "results",
                          "exp225_structured_media_reader.json")
    DEP227 = os.path.join(ROOT, "results",
                          "exp227_reader_n1000.json")
    for _p in (DEP182, DEP225, DEP227):
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
                       "bit-identical per rung by the MULTI-identity "
                       "audit)"),
        "seeds": list(SEEDS_RUN),
        "n": "the rung's own (100/200/400/700/1000 — the pre-named ns)",
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
    with open(DEP227) as fh:
        dep227 = json.load(fh)

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
        _LOCK_LOG.append((host, row_key, int(seed)))

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
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
    #      wiring) — exp225/exp227's replica VERBATIM (its
    #      MULTI-identity audit asserts the replica IS
    #      exp148.decode("scoped", ...)).
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

    # ---- the per-rung target rows (exp225/exp227's build_rows
    #      VERBATIM, parameterized on the rung's n): the rung's own
    #      canon (wildtype) + 3 union targets (manifest indices 0, 49,
    #      99) + the deep band's -60.0 rung both instances. 5 target
    #      classes; 6 decode rows per rung (the deep rung carries BOTH
    #      pre-named instances). The dep182 manifest checksums live at
    #      n=100 — the checksum assert fires on the n=100 rebuild only
    #      (the instrument-identity audit; at the larger ns the same
    #      construction is re-run parameterized — disclosed, per
    #      exp227's discipline; no deposited larger-n checksum exists).
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    def build_rows(canon: np.ndarray, n: int) -> list:
        rows = []
        # (a) the rung's own canon (wildtype): the empty program —
        #     spec_target_n of the zero-zone spec IS the canon target.
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp230-host-canon",
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
        assert len(rows) == N_ROWS, "row build drifted"
        # the pre-registration's 5 targets = 1 canon + 3 manifest
        # + the -60.0 rung (both pre-named instances = 2 deep rows)
        assert sum(1 for r in rows if r["tclass"] == "canon") == 1
        assert sum(1 for r in rows if r["tclass"] == "manifest") == 3
        assert sum(1 for r in rows if r["tclass"] == "deep") == 2
        return rows

    # ---- the instrument-identity audit at n=100 (exp227's audit
    #      VERBATIM): the row-build machinery on exp136's own canon
    #      reproduces dep182's manifest checksums exactly.
    build_rows(labeling_bfs_n(g6.A_CHAIN), int(g6.N))

    # ---- THE SIZE AXIS: path(n) at every pre-named rung — exp198's
    #      scale constructor (the SAME graph_path that builds exp136's
    #      A_CHAIN and exp225's H1 / exp227's path1000) — the host's
    #      own W as a static single-frame decode medium.
    def build_path_host(n: int) -> dict:
        A = graph_path(n)
        canon = labeling_bfs_n(A)
        assert np.array_equal(canon, g6.wildtype_target(n)), \
            f"path({n}) canon != wildtype_target({n})"
        if n == int(g6.N):
            assert np.array_equal(A, g6.A_CHAIN), \
                "path(100) != exp136's A_CHAIN (the constructor anchor)"
        return {"name": f"path{n}", "n": int(n), "A": A, "canon": canon}

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
        # the per-rung MULTI-identity audit (credited runs only): the
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
                         "the pre-named size-axis rung"),
                "edges": int(np.count_nonzero(np.triu(A, 1))),
                "f_max": fmax, "dispatch_class": cls,
                "seeds": [int(s) for s in seeds],
                "n_rows": len(per_row),
                "n_decodes": len(all_errs) + n_rej,
                "n_rejections": n_rej,
                "worst_err": (float(max(all_errs)) if all_errs else None),
                "mean_err": (float(np.mean(all_errs))
                             if all_errs else None),
                "median_err": (float(np.median(all_errs))
                               if all_errs else None),
                "per_row": per_row,
                "multi_identity_audit": {"seed": int(seeds[0]),
                                         "bit_identical": audit_ok,
                                         "prod_err": prod_err}}

    # ---- THE E1 CHECKER REPAIR (hygiene only; NO gate rewrite) -------
    # exp227's deposited E1 recorded complete_not_sampled=false while
    # its own deposited counts prove 33/33 complete (the checker
    # contradiction, disclosed in the ledger). The repair: the
    # completeness predicate is DERIVED from the grid-definition object
    # (no hand-counted constants) — here re-run (a) as exp230's own
    # gate predicate over GRID and (b) against exp227's DEPOSITED grid
    # definition, read from its own cohort fields. exp227's deposit is
    # read-only here; its gate verdicts are NOT rewritten.
    def completeness_from_grid(grid: dict, sections: dict) -> dict:
        per = {}
        for key, g in sorted(grid.items()):
            sec = sections.get(key)
            if sec is None:
                per[key] = {"present": False, "complete": False}
                continue
            errs = [e for r in sec["per_row"] for e in r["errs"]]
            ok = (sec["n_decodes"] == g["decodes"]
                  and len(sec["per_row"]) == g["rows"]
                  and all(r["seeds"] == list(SEEDS_RUN)
                          for r in sec["per_row"])
                  and sec["n_rejections"] == 0
                  and len(errs) == g["decodes"]
                  and bool(np.all(np.isfinite(errs))))
            per[key] = {"present": True, "complete": bool(ok),
                        "decodes": sec["n_decodes"],
                        "expected": g["decodes"],
                        "rejections": sec["n_rejections"]}
        return {"per_n": per,
                "complete": all(v["complete"] for v in per.values()),
                "definition": ("derived from GRID (5 ns x 6 rows x 3 "
                               "seeds = 90), not hand-counted — the "
                               "exp227 E1 repair, hygiene only")}

    def exp227_e1_repair(dep: dict) -> dict:
        p = dep["sections"]["path1000"]
        c = dep["sections"]["corner_n1000"]
        # the grid definition, rebuilt from the deposit's OWN fields
        grid227 = {"path1000": {"units": p["n_rows"],
                                "seeds": len(p["seeds"])},
                   "corner_n1000": {"units": c["n_instances"],
                                    "seeds": len(c["seeds"])}}
        checks = {
            "path_decodes": (p["n_decodes"] ==
                             grid227["path1000"]["units"]
                             * grid227["path1000"]["seeds"]),
            "corner_decodes": (c["n_decodes"] ==
                               grid227["corner_n1000"]["units"]
                               * grid227["corner_n1000"]["seeds"]),
            "path_rows": p["n_rows"] == 6,
            "corner_instances": c["n_instances"] == 5,
            "path_seeds": all(r["seeds"] == p["seeds"]
                              for r in p["per_row"]),
            "corner_seeds": c["seeds"] == p["seeds"],
            "corner_gen_seed_rule": all(i["gen_seed"]
                                        == 166000 + i["j"]
                                        for i in c["instances"]),
            "zero_rejections":
                p["n_rejections"] + c["n_rejections"] == 0,
            "all_finite":
                bool(np.all(np.isfinite(
                    [e for r in p["per_row"] for e in r["errs"]]
                    + [e for i in c["instances"]
                       for e in i["errs"]]))),
        }
        total = p["n_decodes"] + c["n_decodes"]
        return {
            "predicate_value": bool(all(checks.values())),
            "deposited_counts": {
                "decodes": total, "expected": total,
                "rejections": p["n_rejections"] + c["n_rejections"]},
            "checks": checks,
            "deposited_gate_state_read_at_runtime": {
                "E1_pass": dep["gates"]["E1_n1000_sweep"]["pass"],
                "E1_complete_not_sampled":
                    dep["gates"]["E1_n1000_sweep"]
                    ["complete_not_sampled"],
                "verdict": dep["verdict"]},
            "disclosure": ("exp227's deposited E1 recorded "
                           "complete_not_sampled=false while its own "
                           "counts prove 33/33 complete (the checker "
                           "contradiction, disclosed in the ledger); "
                           "the predicate is rebuilt here from the "
                           "deposit's own grid definition and re-run — "
                           "hygiene only; exp227's deposit untouched "
                           "(NO gate rewrite)")}

    # ---- dispatch ------------------------------------------------------
    job_to_n = {"n100": 100, "n200": 200, "n400": 400,
                "n700": 700, "n1000": 1000}
    jobs = (list(sorted(job_to_n)) if args.job == "all"
            else [args.job])
    seeds_run = (1,) if args.smoke else SEEDS_RUN
    mode = ("SMOKE n=200, 1 target - discarded" if args.smoke else
            f"FULL jobs={jobs} seeds={list(seeds_run)}")
    print(f"=== exp230: THE READER SIZE-COST CURVE ({mode}) ===")
    print(f"  read: exp178's production scoped arm, fingerprint {FP}; "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})")
    print(f"  grid: {len(NS)} ns x {N_ROWS} rows x "
          f"{len(SEEDS_RUN)} seeds = {EXPECTED_TOTAL} decodes\n")

    result: dict = {}
    if not args.smoke and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("sections", {})

    if args.smoke:
        h = build_path_host(200)
        # 1 target = the canon row only (the pre-registered smoke scope)
        sec = run_path_host(h, seeds_run,
                            rows_override=build_rows(h["canon"],
                                                     h["n"])[:1])
        print(f"\n  SMOKE (n=200, 1 target) decodes "
              f"{sec['n_decodes']} rejections {sec['n_rejections']} "
              f"worst {sec['worst_err']} - DISCARDED (no deposit, "
              f"gates not evaluated)")
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        return {"exp": "exp230_reader_size_cost_curve", "smoke": True,
                "verdict": "smoke (discarded)"}

    for j in jobs:
        ts = time.time()
        n = job_to_n[j]
        h = build_path_host(n)
        sec = run_path_host(h, seeds_run)
        sec["runtime_s"] = round(time.time() - ts, 1)
        sec["m4_evidence"] = {
            "floors_pre_restore": dict(_PRE_RESTORE),
            "floor_post_restore": PROD_FLOOR,
            "fingerprint": FP,
            "threshold": SCOPED_THRESHOLD,
            "multi_identity_bit_identical":
                sec["multi_identity_audit"]["bit_identical"]}
        result["sections"][j] = sec
        print(f"\n  [{j}] path({n}) edges={sec['edges']} "
              f"f_max={sec['f_max']} ({sec['dispatch_class']}) "
              f"worst {sec['worst_err']} mean "
              f"{round(sec['mean_err'], 3)} rejections "
              f"{sec['n_rejections']} ({sec['runtime_s']} s)\n")
        # incremental partial deposit (the runner-split discipline)
        result["verdict"] = (
            f"partial - sections {sorted(result['sections'])} merged; "
            f"gates pending the complete 5-n grid")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)

    # merge discipline: gates close only on the complete cohort
    want = list(sorted(GRID.keys()))
    got = sorted(result["sections"].keys())
    if got != want:
        print(f"  partial deposit written ({out_path}); rerun the "
              f"remaining job(s) to close the gates")
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        return result

    sections = result["sections"]

    # ---- THE CURVE (one deposited line): worst-err and mean-err vs n --
    CURVE = []
    for key in want:
        sec = sections[key]
        errs_n = [e for r in sec["per_row"] for e in r["errs"]]
        CURVE.append({"n": int(sec["n"]),
                      "worst_err": sec["worst_err"],
                      "mean_err": float(np.mean(errs_n)),
                      "median_err": float(np.median(errs_n)),
                      "decodes": sec["n_decodes"],
                      "rejections": sec["n_rejections"]})
        print(f"  [curve] n={sec['n']}: worst "
              f"{round(sec['worst_err'], 3)} mean "
              f"{round(float(np.mean(errs_n)), 3)}")
    worst_row = max(CURVE, key=lambda c: c["worst_err"])
    worst = float(worst_row["worst_err"])
    worst_n = int(worst_row["n"])
    all_errs = [e for key in want for r in sections[key]["per_row"]
                for e in r["errs"]]
    n_rej = sum(sections[k]["n_rejections"] for k in want)
    n_decodes = sum(sections[k]["n_decodes"] for k in want)
    all_finite = bool(all_errs) and bool(np.all(np.isfinite(all_errs)))

    # ---- N3: the log-log fit (one OLS line, zero fitting) -------------
    xs = np.log(np.array([c["n"] for c in CURVE], dtype=float))
    ys = np.log(np.array([c["worst_err"] for c in CURVE], dtype=float))
    slope, intercept = (float(b) for b in np.polyfit(xs, ys, 1))
    pred = slope * xs + intercept
    ss_res = float(np.sum((ys - pred) ** 2))
    ss_tot = float(np.sum((ys - float(ys.mean())) ** 2))
    r2 = (1.0 - ss_res / ss_tot) if ss_tot > 0 else None
    # the mean-err slope (disclosed, non-gating)
    ys_mean = np.log(np.array([c["mean_err"] for c in CURVE],
                              dtype=float))
    slope_mean, intercept_mean = (float(b) for b in
                                  np.polyfit(xs, ys_mean, 1))
    branch = ("SUB-LINEAR" if slope < 1
              else "LINEAR" if slope < 2 else "SUPER-LINEAR")

    # ---- the n=1000 provenance cross-check (disclosed, non-gating) ----
    # exp227's path1000 IS the same instrument at the same rung (same
    # constructor, rows, seeds, read): the errs are expected
    # bit-identical (exp228's provenance-identity discipline)
    ref_rows = {r["key"]: r["errs"]
                for r in dep227["sections"]["path1000"]["per_row"]}
    mine_rows = {r["key"]: r["errs"]
                 for r in sections["n1000"]["per_row"]}
    n1000_bit_identical = bool(
        set(ref_rows) == set(mine_rows)
        and all(ref_rows[k] == mine_rows[k] for k in ref_rows))
    _sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
    prov227_sha = _sha(DEP227)
    n1000_crosscheck = {
        "bit_identical": n1000_bit_identical,
        "rows_compared": len(ref_rows),
        "source": ("exp227's deposit sections/path1000 (the same "
                   "instrument at the same rung), sha256 "
                   f"{prov227_sha[:16]} — re-read at run time; "
                   "disclosed, non-gating")}

    # ---- the E1 repair re-run against exp227's deposited grid --------
    repair227 = exp227_e1_repair(dep227)

    # ================= THE GATES (each evaluated exactly once) =========
    complete_grid = completeness_from_grid(GRID, sections)
    audits_ok = all(sections[k]["multi_identity_audit"]["bit_identical"]
                    for k in want)
    floors_ok = bool(
        all(sections[k]["m4_evidence"]["floor_post_restore"]
            == PROD_FLOOR for k in want)
        and all(v == READER_PIN_FLOOR
                for k in want
                for v in sections[k]["m4_evidence"]
                ["floors_pre_restore"].values()))
    thresholds_ok = bool(all(sections[k]["m4_evidence"]["threshold"]
                             == 32.0 for k in want))
    lock_ok = len(_LOCK_LOG) == n_decodes
    fp_post = _fingerprint()
    seeds_ok = all(r["seeds"] == list(SEEDS_RUN)
                   for k in want for r in sections[k]["per_row"])
    n1 = bool(n_rej == 0 and all_finite
              and n_decodes == EXPECTED_TOTAL
              and complete_grid["complete"] and seeds_ok
              and len(CURVE) == len(NS))
    n2 = bool(all_finite and all(e < BAR for e in all_errs))
    n3 = bool(len(CURVE) == len(NS) and np.isfinite(slope)
              and branch in ("SUB-LINEAR", "LINEAR", "SUPER-LINEAR"))
    e4 = bool(n_rej == 0 and all_finite and floors_ok and thresholds_ok
              and audits_ok and lock_ok and fp_post == FP
              and complete_grid["complete"]
              and repair227["predicate_value"])

    # the context reading (recorded, not gated): the docstring's
    # profile numbers, re-read from the deposits at run time
    with open(DEP225) as f:
        dep225 = json.load(f)
    d198 = json.load(open(os.path.join(
        ROOT, "results", "exp198_adversarial_reader_n400.json")))
    d199 = json.load(open(os.path.join(
        ROOT, "results", "exp199_ro_n400_tail.json")))
    worst198 = max(e for sec_ in d198["cells"].values()
                   for r in sec_["instances"] for e in r["errs"])
    worst199 = max(e for sec_ in d199["cells"].values()
                   for r in sec_["instances"] for e in r["errs"])
    context = {
        "random_worst_pooled_n400": float(max(worst198, worst199)),
        "random_worst_source": (
            f"exp198 pooled max {worst198} + exp199 pooled max "
            f"{worst199}, re-read at run time"),
        "structured_worst_n400": float(dep225["structured_worst_err"]),
        "structured_worst_n400_source":
            "exp225's deposit, re-read at run time",
        "structured_worst_n1000_exp227":
            float(max(e for r in dep227["sections"]["path1000"]
                      ["per_row"] for e in r["errs"])),
        "structured_worst_n1000_source":
            "exp227's deposit path1000, re-read at run time",
        "reading": (f"the curve's n=1000 worst {worst} vs exp227's "
                    f"deposited {float(max(e for r in dep227['sections']['path1000']['per_row'] for e in r['errs']))} "
                    f"(bit-identical: {n1000_bit_identical})")}

    gates = {
        "N1_size_curve": {
            "pass": n1,
            "decodes": n_decodes, "expected": EXPECTED_TOTAL,
            "rejections": n_rej,
            "complete_from_grid": complete_grid,
            "ns": list(NS), "n_target_classes": 5,
            "n_rows_per_n": N_ROWS, "seeds": list(SEEDS_RUN),
            "curve": CURVE,
            "note": ("the pre-registration's '5 target classes' = the "
                     "5 pre-named target classes; the deep band's "
                     "-60.0 rung carries BOTH pre-named instances "
                     "(2 decode rows), per exp225's pre-named target "
                     "list — 6 decode rows x 3 seeds per n")},
        "N2_reader_bar": {
            "pass": n2,
            "bar_mV": BAR, "n_finite": int(np.sum(np.isfinite(all_errs))),
            "worst_err": worst, "worst_at_n": worst_n,
            "per_n_worst": {c["n"]: c["worst_err"] for c in CURVE},
            "context": context},
        "N3_loglog_slope": {
            "pass": n3,
            "branch": branch,
            "slope_worst": slope, "intercept_worst": intercept,
            "r2_worst": r2,
            "slope_mean_disclosed": slope_mean,
            "intercept_mean_disclosed": intercept_mean,
            "points_loglog": [[float(x), float(y)]
                              for x, y in zip(xs, ys)],
            "thresholds": ("SUB-LINEAR (slope < 1) / LINEAR "
                           "(1 <= slope < 2) / SUPER-LINEAR (>= 2)"),
            "fit": ("one OLS line on (log n, log worst-err) over the "
                    "5 deposited curve points; zero fitting — the "
                    "value disclosed")},
        "N4_hygiene": {
            "pass": e4,
            "rejections": n_rej, "all_finite": all_finite,
            "floor_discipline": (
                f"production {PROD_FLOOR} restored post-import on all "
                f"pinned modules; the {READER_PIN_FLOOR} reader-line "
                f"pin disclosed (exp218's discipline, VERBATIM)"),
            "floors_pre_restore": dict(_PRE_RESTORE),
            "threshold_asserted": 32.0,
            "multi_identity_audit": ("all 5 rungs bit-identical"
                                     if audits_ok else "DRIFT"),
            "s_star_identity": (f"STAR_OP == S* == {S_STAR}, asserted"),
            "lock_log_entries": len(_LOCK_LOG),
            "fingerprint_pre": FP, "fingerprint_post": fp_post,
            "completeness_predicate":
                complete_grid["definition"],
            "e1_repair_exp227": {
                "predicate_value": repair227["predicate_value"],
                "deposited_counts": repair227["deposited_counts"],
                "no_gate_rewrite": True,
                "deposited_gate_state_read_at_runtime":
                    repair227["deposited_gate_state_read_at_runtime"],
                "disclosure": repair227["disclosure"]},
            "n1000_provenance_crosscheck": n1000_crosscheck,
            "per_media_tuning": "none"},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = (f"{n_pass}/{len(gates)} gates - N3 {branch} (log-log "
               f"slope {round(slope, 4)}, r2 {None if r2 is None else round(r2, 4)}); "
               f"worst {worst} at n={worst_n} under the {BAR} bar")

    deposit = {
        "exp": "exp230_reader_size_cost_curve",
        "claim": ("THE READER SIZE-COST CURVE (L204's registered "
                  "next): the reader's worst-err profile graded in n "
                  "as ONE deposited line — worst-err and mean-err vs n "
                  "at n = 100/200/400/700/1000 on the path constructor "
                  "(exp198's graph_path, the A_CHAIN family), 5 target "
                  "classes x 3 seeds per n (exp225/exp227's sweep "
                  "machinery verbatim: the production scoped read, "
                  "exp225's target classes, exp142's 3 seeds), the 6.0 "
                  "bar unchanged; PLUS the exp227 E1 checker repair — "
                  "the completeness predicate rebuilt from the "
                  "deposited grid definition and re-run as a "
                  "hygiene-only pass (no gate rewrite)"),
        "read": {**READ_CONFIG, "fingerprint": FP,
                 "wiring_id": ("exp148.decode('scoped') wiring | "
                               "exp169 f_max/THRESHOLD | exp167 R_T | "
                               "exp145/148 PN+TC | exp142 "
                               "execute_signed@STAR_OP==S*")},
        "cohort": {
            "hosts": [f"path{n}" for n in NS],
            "ns": list(NS),
            "constructor": ("exp198's scale constructor "
                            "(cultivation.substrate.graph.path) — the "
                            "SAME constructor that builds exp136's "
                            "A_CHAIN (path(100) bit-asserted) and "
                            "exp225's H1 / exp227's path1000"),
            "seeds": list(SEEDS_RUN),
            "target_list": ("the host's own canon (wildtype) + manifest "
                            "indices 0, 49, 99 + the deep band's -60.0 "
                            "rung both instances (pre-named; exp225's "
                            "target classes)"),
            "n_target_classes": 5, "n_decode_rows_per_n": N_ROWS,
            "grid": GRID,
            "expected_decodes": EXPECTED_TOTAL},
        "provenance": {"exp182": _sha(DEP182), "exp225": _sha(DEP225),
                       "exp227": prov227_sha},
        "sections": sections,
        "curve": CURVE,
        "log_log_fit": {"slope_worst": slope,
                        "intercept_worst": intercept, "r2_worst": r2,
                        "slope_mean": slope_mean,
                        "branch": branch},
        "n1000_provenance_crosscheck": n1000_crosscheck,
        "e1_repair_exp227": repair227,
        "worst_err": worst, "worst_at_n": worst_n,
        "pooled_median_err": (float(np.median(all_errs))
                              if all_errs else None),
        "context": context,
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
    print(f"  curve (worst/mean mV vs n): "
          + " | ".join(f"n{c['n']}: {round(c['worst_err'], 3)}/"
                       f"{round(c['mean_err'], 3)}" for c in CURVE))
    print(f"  N3: {branch} — log-log slope {slope:.4f} (r2 "
          f"{r2 if r2 is not None else float('nan'):.4f}); the exp227 "
          f"E1 repair predicate: "
          f"{repair227['predicate_value']} (hygiene, no gate rewrite)")
    print(f"  n=1000 cross-check bit-identical vs exp227's path1000: "
          f"{n1000_bit_identical}")
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
