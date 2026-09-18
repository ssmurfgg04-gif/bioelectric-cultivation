#!/usr/bin/env python3
"""exp225 — THE STRUCTURED-MEDIA ADVERSARIAL READER (L189/L194's
Stage 5 path-1 push).

The universal reader closed on random media (200 random media, zero
rejections; the corner battery at n=400) — the registered Stage 5
extension: STRUCTURED adversarial media, the hardest class the stack
can name. The 12 union hosts' own graph structures (small-world
corpus rewires + the n=400 path) used AS decode media — the reader
decoding each host's own W under the production scoped arm against
the host's own canon target and against the union's carried targets:
if the reader holds on the media the WRITER itself built from, the
"any medium" claim extends from random to structured.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp214's build_hosts verbatim
(the 12 hosts, checksummed from exp202's deposit); the production
scoped read (exp178's wiring — exp148.decode("scoped", ...) with
exp169's f_max); exp169's THRESHOLD asserted; the floors asserted
post-restore (exp218's disclosed exp169-import discipline: restore
CORE.NEURAL_SPEC_MIN = -60.0 after the import chain); the targets
per host: the host's own canon (wildtype) + 3 union targets
(manifest indices 0, 49, 99 — pre-named) + the deep band's -60.0
rung both instances (pre-named).

GATES (each evaluated exactly once):
  GATE-M1 (the structured sweep) all 12 hosts x 5 targets x 3 seeds
           decode with ZERO rejections under the production scoped
           arm (structured media, complete, not sampled).
  GATE-M2 (the reader bar) every decode's err under the 6.0 bar
           (exp151/155's verify bar); the per-host worst-case
           deposited; zero non-finite.
  GATE-M3 (the structured-vs-random contrast) the structured media's
           worst err vs the corner battery's deposited worst (exp198/
           exp199's n=400 line): the branch named — HELD (structured
           worst <= the random worst + 0.5 mV) / DEGRADES (beyond).
  GATE-M4 (hygiene) the -60.0/-35.0 floor discipline asserted
           (exp218's restore, disclosed); zero rejections; all
           finite; no per-media tuning.
NO post-hoc tuning. --smoke permitted (H0 only), discarded.
DEPOSIT: results/exp225_structured_media_reader.json
RUN: python3 -m experiments.exp225_structured_media_reader [--smoke] [--job ...] [--out ...]
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
                   "exp225_structured_media_reader.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline; gates below evaluated exactly once) =======
    import hashlib
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "corpus",
                                      "gates"], default="all")
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
    from experiments.exp172_deep_band_sweep import (  # noqa: E402
        target_for as deep_target_for)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp218's disclosed exp169-import
    #      discipline, applied to every module the import chain pinned,
    #      disclosed): the reader-line imports (exp167 -> exp169) carry
    #      an import-time instrument pin that flips the reader-world
    #      floor -35.0 onto (collective, exp142, exp145, exp148, exp94).
    #      The read-chain modules captured CF-1's production -60.0 at
    #      their own import (the pins are attribute-only); restored here
    #      so the reader's commit branch runs at the CF-1 production
    #      floor the pre-registration asserts — the deep band's -60.0
    #      rung is decodable ONLY at the production floor.
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
    N400 = 400
    REWIRE_P = 0.10
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    MANIFEST_INDICES = (0, 49, 99)         # the union's carried targets
    #                                     #   (pre-named)
    M3_BAR = 0.5            # mV, the structured-vs-random contrast bar
    DEP202 = os.path.join(ROOT, "results",
                          "exp202_cross_organism_carriage.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP198 = os.path.join(ROOT, "results",
                          "exp198_adversarial_reader_n400.json")
    DEP199 = os.path.join(ROOT, "results",
                          "exp199_ro_n400_tail.json")
    DEP214 = os.path.join(ROOT, "results",
                          "exp214_union_carriage.json")
    for _p in (DEP202, DEP182, DEP198, DEP199, DEP214):
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
                       "bit-identical per host by the MULTI-identity "
                       "audit)"),
        "seeds": list(SEEDS),
        "n": "the host's own (100 or 400)",
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
    # the scoped arm ends in exp142's execute_signed at op=STAR_OP;
    # STAR_OP IS S* = (64.0, 0.0) — asserted once here and per read.
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the reader's executor op {STAR_OP} != S* {S_STAR}"

    with open(DEP202) as fh:
        dep202 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)

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
    #      medium (the exp137/exp160 medium contract: snapshots() +
    #      native_support(); deterministic re-iteration, no rng at read
    #      time). The STRUCTURED adversarial class: the media the
    #      WRITER itself built from — no semantics dimension is
    #      violated (the all-off corner, exp160's "none" naming); the
    #      structure IS the host's own.
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
    #      wiring) with the read stack's target input = the row's spec.
    #      Every stage is the imported production machinery: exp169's
    #      f_max diagnostic + THRESHOLD; exp167's R_T adoption at T>1
    #      (T=1 passthrough); exp145/exp148's PN1/PN2 projection + TC1
    #      flip-clock + TC2 A_ext; exp142's execute_signed at
    #      op=STAR_OP (== S*). The production arm's own target input
    #      (exp148's MULTI default) is asserted bit-identical per host
    #      by the MULTI-identity audit.
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

    # ---- the per-host target rows (the pre-registration's list,
    #      verbatim): the host's own canon (wildtype) + 3 union targets
    #      (manifest indices 0, 49, 99) + the deep band's -60.0 rung
    #      both instances. 5 target classes; 6 decode rows per host
    #      (the deep rung carries BOTH pre-named instances).
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
        #     (exp214's manifest rebuild VERBATIM; checksummed on H0).
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
            if host_name == "H0":
                assert sha == m["f_sha256"], \
                    (f"manifest checksum mismatch on H0 target "
                     f"{m['index']}: rebuilt {sha} != deposited "
                     f"{m['f_sha256']}")
            rows.append({"tclass": "manifest",
                         "key": f"m{m['index']}", "index": m["index"],
                         "spec": spec, "f": f, "f_sha256": sha,
                         "zone_count": m["zone_count"],
                         "vmin": m["vmin"], "vmax": m["vmax"]})
        # (c) the deep band's -60.0 rung, both instances (exp214's
        #     deep construction VERBATIM; H0 bit-asserted against
        #     exp172's own construction).
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
            if host_name == "H0":
                f_ref, _trip, _ref = deep_target_for(DEEP_RUNG, inst)
                assert np.array_equal(f, f_ref), (
                    f"deep {DEEP_RUNG:g} i{inst} rebuild != exp172's "
                    f"construction")
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

    # ---- the hosts (exp202's build records reused checksummed;
    #      exp214's build_hosts VERBATIM) --------------------------------
    def build_hosts() -> dict:
        hosts = {}
        canon0 = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon0, g6.wildtype_target(g6.N))
        hosts["H0"] = {"name": "H0", "n": int(g6.N), "A": g6.A_CHAIN,
                       "canon": canon0}
        A400 = graph_path(N400)
        canon400 = labeling_bfs_n(A400)
        assert np.array_equal(canon400, g6.wildtype_target(N400))
        hosts["H1"] = {"name": "H1", "n": N400, "A": A400,
                       "canon": canon400}
        redraw = {r["host"]: r["seed"] for r in
                  dep202["sections"]["corpus"]["scan"]["redraw_log"]}
        dep_hosts = dep202["sections"]["corpus"]["hosts"]
        for k in sorted(dep_hosts):
            if not k.startswith("H") or int(k[1:]) < 2:
                continue
            seed = int(redraw[k])
            A = small_world(100, REWIRE_P, seed)
            assert A.sum() > 0
            dep_edges = dep_hosts[k].get("edges")
            got_edges = int(np.count_nonzero(
                np.triu(A, 1) if not np.iscomplexobj(A) else np.abs(
                    np.triu(A, 1)) > 0))
            if dep_edges is not None and isinstance(dep_edges, int):
                assert got_edges == dep_edges, \
                    (f"{k} rebuild drift: edges {got_edges} != "
                     f"deposit {dep_edges}")
            hosts[k] = {"name": k, "n": 100, "A": A,
                        "canon": labeling_bfs_n(A),
                        "rewire_seed": seed,
                        "record": dep_hosts[k].get("record")}
        return hosts

    def run_host(h: dict, seeds) -> dict:
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
        rows = build_rows(h["name"], canon, n)
        # the per-host MULTI-identity audit: the parameterized scoped
        # wiring IS exp148.decode("scoped", ...) at the production
        # default target input (bit-exact on err/verified/rho/branch)
        prod = exp148_decode("scoped", med, seeds[0], f_max=fmax)
        mine = _scoped_row_read(MULTI, med, seeds[0], fmax)
        audit_ok = bool(
            prod["ok"]
            and float(prod["err"]) == float(mine["err_vs_target"])
            and prod["verified"] == bool(mine["program_verified"])
            and prod.get("rho") == mine.get("rho")
            and prod.get("branch") == mine.get("branch"))
        if not audit_ok:
            raise AssertionError(
                f"{h['name']}: the parameterized scoped wiring drifted "
                f"from exp148.decode('scoped')")
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
                "kind": ("reference (exp182's own host)"
                         if h["name"] == "H0" else
                         "size-law organism (exp198's scale)"
                         if h["name"] == "H1" else
                         "corpus-rewired organism"),
                "edges": int(np.count_nonzero(np.triu(A, 1))),
                "rewire_seed": h.get("rewire_seed"),
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
                                         "prod_err": (float(prod["err"])
                                                      if prod["ok"]
                                                      else None)}}

    # ---- dispatch (exp214's sharding pattern) -------------------------
    jobs = (["H0", "H1", "corpus"] if args.job == "all"
            else [args.job] if args.job in ("H0", "H1", "corpus")
            else [])
    hosts = build_hosts() if (args.smoke or jobs) else None
    seeds_run = (1,) if args.smoke else tuple(SEEDS)
    mode = ("SMOKE H0 only - discarded" if args.smoke else
            f"FULL jobs={jobs} seeds={seeds_run}")
    print(f"=== exp225: THE STRUCTURED-MEDIA ADVERSARIAL READER "
          f"({mode}) ===")
    print(f"  read: exp178's production scoped arm, fingerprint {FP}; "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})\n")

    result: dict = {}
    if not args.smoke and (jobs or args.job == "gates") \
            and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("hosts", {})

    if args.smoke:
        h = hosts["H0"]
        sec = run_host(h, seeds_run)
        print(f"\n  SMOKE (H0 only) decodes {sec['n_decodes']} "
              f"rejections {sec['n_rejections']} worst "
              f"{sec['worst_err']} - DISCARDED (no deposit, gates not "
              f"evaluated)")
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
        return {"exp": "exp225_structured_media_reader", "smoke": True,
                "verdict": "smoke (discarded)"}

    def _job_hosts(j: str) -> list:
        if j == "H0":
            return [hosts["H0"]]
        if j == "H1":
            return [hosts["H1"]]
        return [hosts[k] for k in sorted(hosts) if k.startswith("H")
                and int(k[1:]) >= 2]

    for j in jobs:
        for h in _job_hosts(j):
            ts = time.time()
            sec = run_host(h, seeds_run)
            sec["runtime_s"] = round(time.time() - ts, 1)
            sec["m4_evidence"] = {
                "floors_pre_restore": dict(_PRE_RESTORE),
                "floor_post_restore": PROD_FLOOR,
                "fingerprint": FP,
                "threshold": SCOPED_THRESHOLD,
                "multi_identity_bit_identical":
                    sec["multi_identity_audit"]["bit_identical"]}
            result["hosts"][h["name"]] = sec
            print(f"\n  [{h['name']}] n={h['n']} edges={sec['edges']} "
                  f"f_max={sec['f_max']} ({sec['dispatch_class']}) "
                  f"worst {sec['worst_err']} median "
                  f"{sec['median_err']} rejections "
                  f"{sec['n_rejections']} ({sec['runtime_s']} s)")

    # merge discipline: gates close only on the complete 12-host cohort
    want_hosts = sorted(["H0", "H1"] + [f"H{i}" for i in range(2, 12)])
    got_hosts = sorted(result["hosts"].keys())
    if jobs and got_hosts != want_hosts:
        result["verdict"] = (f"partial - hosts {got_hosts} merged; "
                             f"gates pending all 12")
        result["hosts_run"] = got_hosts
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  partial deposit written ({out_path}); rerun the "
              f"remaining jobs to close the gates")
        return result
    if not jobs and args.job == "gates" and got_hosts != want_hosts:
        raise AssertionError(f"gates job on incomplete cohort: "
                             f"{got_hosts}")

    # ================= THE GATES (each evaluated exactly once) =========
    all_errs = [e for k in want_hosts
                for r in result["hosts"][k]["per_row"] for e in r["errs"]]
    n_rej = sum(result["hosts"][k]["n_rejections"] for k in want_hosts)
    n_decodes = sum(result["hosts"][k]["n_decodes"] for k in want_hosts)
    expected = 12 * 6 * len(seeds_run)
    rows_ok = all(result["hosts"][k]["n_rows"] == 6 for k in want_hosts)
    seeds_ok = all(r["seeds"] == list(seeds_run)
                   for k in want_hosts
                   for r in result["hosts"][k]["per_row"])
    complete = (rows_ok and seeds_ok
                and all(result["hosts"][k]["n_decodes"]
                        == 6 * len(seeds_run) for k in want_hosts))
    per_host_worst = {k: result["hosts"][k]["worst_err"]
                      for k in want_hosts}

    # M3's reference: the corner battery's deposited worst (exp198/
    # exp199's n=400 line), re-read from the deposits at run time
    with open(DEP198) as f:
        d198 = json.load(f)
    with open(DEP199) as f:
        d199 = json.load(f)
    worst198 = max(e for sec in d198["cells"].values()
                   for r in sec["instances"] for e in r["errs"])
    worst199 = max(e for sec in d199["cells"].values()
                   for r in sec["instances"] for e in r["errs"])
    random_worst = float(max(worst198, worst199))
    structured_worst = float(max(all_errs))
    m3_branch = ("HELD" if structured_worst <= random_worst + M3_BAR
                 else "DEGRADES")

    fp_post = _fingerprint()
    audits_ok = all(result["hosts"][k]["multi_identity_audit"]
                    ["bit_identical"] for k in want_hosts)
    floors_ok = all(
        sec["m4_evidence"]["floor_post_restore"] == PROD_FLOOR
        and all(v == READER_PIN_FLOOR
                for v in sec["m4_evidence"]["floors_pre_restore"].values())
        for sec in (result["hosts"][k] for k in want_hosts))
    thresholds_ok = all(result["hosts"][k]["m4_evidence"]["threshold"]
                        == 32.0 for k in want_hosts)
    lock_ok = (len(_LOCK_LOG) == n_decodes) if jobs else True
    m4 = bool(floors_ok and thresholds_ok and audits_ok and lock_ok
              and fp_post == FP)

    gates = {
        "M1_structured_sweep": {
            "pass": bool(n_rej == 0 and n_decodes == expected
                         and complete),
            "decodes": n_decodes, "expected": expected,
            "rejections": n_rej, "complete_not_sampled": complete,
            "hosts": len(want_hosts),
            "n_target_classes": 5, "n_rows_per_host": 6,
            "note": ("the pre-registration's '5 targets' = the 5 "
                     "pre-named target classes; the deep band's -60.0 "
                     "rung carries BOTH pre-named instances (2 decode "
                     "rows), per the pre-named target list")},
        "M2_reader_bar": {
            "pass": bool(all(np.isfinite(all_errs))
                         and all(e < BAR for e in all_errs)),
            "bar_mV": BAR, "n_finite": int(np.sum(np.isfinite(all_errs))),
            "worst_err": structured_worst,
            "per_host_worst_case": per_host_worst},
        "M3_structured_vs_random": {
            "pass": bool(m3_branch == "HELD"), "branch": m3_branch,
            "structured_worst": structured_worst,
            "random_worst_deposited": random_worst,
            "random_worst_source": (f"exp198 pooled max {worst198} + "
                                    f"exp199 pooled max {worst199} "
                                    f"(the n=400 corner battery line)"),
            "bar_mV": M3_BAR},
        "M4_hygiene": {
            "pass": m4,
            "floor_discipline": (f"production {PROD_FLOOR} restored "
                                 f"post-import on all pinned modules; "
                                 f"the {READER_PIN_FLOOR} reader-line "
                                 f"pin disclosed (exp218's discipline)"),
            "floors_pre_restore": dict(_PRE_RESTORE),
            "threshold_asserted": 32.0,
            "multi_identity_audits": "12/12 bit-identical" if audits_ok
                                     else "DRIFT",
            "lock_log_entries": len(_LOCK_LOG),
            "fingerprint_pre": FP, "fingerprint_post": fp_post,
            "per_media_tuning": "none"},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = (f"{n_pass}/{len(gates)} gates - "
               f"M3 {m3_branch} (structured worst "
               f"{structured_worst} vs random worst {random_worst} "
               f"+{M3_BAR:g} bar)")

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    deposit = {
        "exp": "exp225_structured_media_reader",
        "claim": ("the production scoped reader holds on STRUCTURED "
                  "adversarial media — the 12 union hosts' own graph "
                  "structures (small-world corpus rewires + the n=400 "
                  "path) used AS decode media, each host's own W read "
                  "under exp178's production scoped arm against the "
                  "host's own canon (wildtype), the union's carried "
                  "targets (manifest 0/49/99) and the deep band's "
                  "-60.0 rung both instances — extending the 'any "
                  "medium' claim from random to structured media"),
        "read": {**READ_CONFIG, "fingerprint": FP,
                 "wiring_id": ("exp148.decode('scoped') wiring | "
                               "exp169 f_max/THRESHOLD | exp167 R_T | "
                               "exp145/148 PN+TC | exp142 "
                               "execute_signed@STAR_OP==S*")},
        "cohort": {
            "hosts": want_hosts,
            "build": "exp214's build_hosts VERBATIM (checksummed from "
                     "exp202's deposit)",
            "seeds": list(seeds_run),
            "target_list": ("the host's own canon (wildtype) + manifest "
                            "indices 0, 49, 99 + the deep band's -60.0 "
                            "rung both instances (pre-named)"),
            "n_target_classes": 5, "n_decode_rows_per_host": 6},
        "provenance": {
            "exp202": _sha(DEP202), "exp182": _sha(DEP182),
            "exp198": _sha(DEP198), "exp199": _sha(DEP199),
            "exp214": _sha(DEP214)},
        "hosts": {k: result["hosts"][k] for k in want_hosts},
        "pooled_median_err": (float(np.median(all_errs))
                              if all_errs else None),
        "structured_worst_err": structured_worst,
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
          f"structured worst {structured_worst} vs random worst "
          f"{random_worst} (bar +{M3_BAR:g})")
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
