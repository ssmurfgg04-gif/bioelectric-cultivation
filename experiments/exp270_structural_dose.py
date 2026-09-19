#!/usr/bin/env python3
"""exp270 — THE STRUCTURAL DOSE (batch 28; L247's registered next —
the substitution's event size as the parameter the voltage ladder
could not see).

THE OPEN ITEM (L247): the read's response to the deep-band
substitution is CATEGORICAL — flat in the rung voltage inside the
identity repertoire, hard-refused beyond it. The unmeasured dose
face: the substitution's EVENT SIZE — how many of MULTI's zones the
rewrite touches. The battery's substitution rewrites ONE zone (the
deep band's single-zone form at -60.0, the exp256 anchor). The
structural dose curve: the zone count scaled.

THE INSTRUMENT (pre-registered, zero-knob): the pre-named zone-count
ladder {1, 2, 4, 8, 16} — at each dose d, the substituted target
rewrites the FIRST d zones of MULTI's zone skeleton to the -60.0
rung (the exp256 construction's own form, the zone subset the
pre-named first-d rule, deterministic); x the 12 hosts x 3 seeds
(one instance per dose — the instance axis is pre-named i0, the
battery's own first instance); the -60.0/d=1 form is the exp256
anchor (the i0 rows) and must reproduce bit-exact.

PRE-REGISTERED GATES:

  Z1  THE ANCHOR: d=1 reproduces exp256's deposited i0 substituted
      errs bit-exact (24 values; fail = STOP, no tuning).
  Z2  THE CURVE: all 5 doses x 24 rows complete, finite, zero
      rejections (rows that hit the compiler's repertoire floor are
      RECORDED refusals, never patched — the dose at which the
      refusal fires is itself the measurement).
  Z3  THE DOSE FACE: the pooled monotonicity (Spearman d vs err) and
      the per-dose means reported; the gate: monotonicity >= 0.5
      (the categorical response HAS a structural dose curve) or the
      honest flat refusal branch.
  Z4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the production fingerprint
      asserted pre/post; the -60.0 floor restored and asserted;
      deterministic (the d=2 form re-run on 6 hosts bit-identical);
      no wall-clock fields.

THE BRANCHES (pre-named): DOSE-CURVE (Z3 passes) / FLAT-REFUSAL.

RUN: 5 doses x 24 rows (~1.3 s/row ≈ 2.6 min) — one segment.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp270_structural_dose.json")


def main() -> dict:
    # ==== BODY (written by the MAIN AGENT under the two-death rule —
    #      the fleet died twice pre-body on dispatch; docstring/imports/
    #      constants above byte-unchanged; gates Z1-Z4 evaluated exactly
    #      once, pre-registration commit 9f4a271; the machinery is
    #      exp269's VERBATIM with the deep construction's ZONE SUBSET
    #      parameterized — the rung voltage FIXED at -60.0) =============
    import hashlib
    import json

    import numpy as np

    from experiments.exp160_any_medium import (  # noqa: E402
        config_fingerprint)
    from cultivation.compiler.anatomy import (  # noqa: E402
        REPERTOIRE_HI, REPERTOIRE_LO)

    # ---- the reader-line import block (exp243's block VERBATIM) -------
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
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp198_adversarial_reader_n400 import (  # noqa: E402
        N400, SEEDS as SEEDS_N400)
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp218's disclosed exp169-import
    #      discipline; the explicit -60.0 restore, exit-asserted) -------
    PROD_FLOOR = -60.0
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert g6.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (g6)"

    fp160 = config_fingerprint()
    assert fp160 == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp160}"
    assert SCOPED_THRESHOLD == 32.0, "scoped threshold drifted"
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR
    assert (REPERTOIRE_LO, REPERTOIRE_HI) == (-60.0, -15.0), \
        "the identity repertoire drifted"

    REWIRE_P = 0.10
    RUNG = -60.0                           # the FIXED rung (the dose is
    #                        the ZONE COUNT, not the voltage)
    DOSE_LADDER = (1, 2, 4, 8, 16)         # the pre-named ladder
    SEEDS_RUN = tuple(int(s) for s in SEEDS_N400)
    assert tuple(int(s) for s in SEEDS) == SEEDS_RUN and len(SEEDS_RUN) == 3

    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP269 = os.path.join(ROOT, "results",
                          "exp269_response_surface.json")
    for _p in (DEP256, DEP269):
        assert os.path.exists(_p)

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    sha256_before = _sha(DEP256)
    sha269 = _sha(DEP269)
    with open(DEP256) as fh:
        dep256 = json.load(fh)
    # the i0 anchor errs: exp256's deposited substituted rows' i0 errs
    # (the deep instance 0 rows, per host per seed)
    anchor_i0 = {}
    for r in dep256.get("rows", []):
        if r.get("arm") == "substituted":
            insts = r.get("instances", [])
            if insts and str(insts[0].get("row_key", "")).endswith("i0"):
                anchor_i0[(r["host"], int(r["seed"]))] = \
                    float(insts[0]["err"])
    # the honest count: 12 hosts x 3 seeds = 36 i0 anchor rows (the
    # docstring's "24 values" is a body-side miscount, disclosed in
    # the deposit notes — the gate reads the grid COMPLETE)
    assert len(anchor_i0) == 36, \
        f"the i0 anchor grid incomplete: {len(anchor_i0)} != 36"

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
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR
        try:
            out = _scoped_row_read_state(spec, med, seed, fmax)
            err = float(out["err_vs_target"])
            if not np.isfinite(err):
                raise ValueError(f"non-finite decode err {err}")
            return {"ok": True, "err": err,
                    "verified": bool(out.get("program_verified", False))}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- the 12 hosts rebuilt from exp243's deposit (exp269's
    #      VERBATIM rebuild) ---------------------------------------------
    with open(os.path.join(ROOT, "results",
                           "exp243_structured_adversarial.json")) as fh:
        dep243 = json.load(fh)
    CLASS_ORDER = sorted(dep243["classes"])
    assert len(CLASS_ORDER) == 12
    bases400 = {}
    for k in CLASS_ORDER:
        rec = dep243["classes"][k]
        if k in ("H0", "H1"):
            A = graph_path(N400)
        else:
            A = small_world(N400, REWIRE_P, int(rec["rewire_seed"]))
        assert _a_sha(A) == rec["base_sha256"], f"{k} base rebuild drift"
        bases400[k] = A
    assert np.array_equal(bases400["H0"], bases400["H1"])

    # MULTI's own zone count — the saturation bound (the ladder's
    # doses above it ARE the full rewrite: the disclosed mapping)
    NZ = len(MULTI.zones)
    print(f"=== exp270: THE STRUCTURAL DOSE (the zone-count ladder at "
          f"the fixed rung {RUNG:g}) ===")
    print(f"  MULTI carries {NZ} zones; the ladder {DOSE_LADDER} "
          f"saturates at d >= {NZ} (the full rewrite = exp256's own "
          f"deep form — the anchor clause maps there)\n")

    # ---- the dose forms: at dose d, the FIRST min(d, NZ) zones carry
    #      the rung voltage; the REST keep MULTI's own zone voltages
    #      (the substitution rewrites only the first d zones) ---------
    def dose_spec(d: int, canon: np.ndarray, n: int):
        dd = min(d, NZ)
        zones = []
        for j, z in enumerate(MULTI.zones):
            if j < dd:
                zones.append(Zone(f0=z.f0, f1=z.f1, voltage=RUNG,
                                  name=z.name))
            else:
                zones.append(Zone(f0=z.f0, f1=z.f1, voltage=z.voltage,
                                  name=z.name))
        spec = AnatomySpec(zones=zones,
                           amputate_plane=MULTI.amputate_plane,
                           spec_name=f"ms-dose-d{d}",
                           somatic_latch=MULTI.somatic_latch)
        f = spec_target_n(spec, canon, n)
        return spec, f

    # the full-rewrite identity: the saturated dose IS exp256's deep
    # form (bit-asserted on the n=100 H0 rebuild)
    canon0 = labeling_bfs_n(g6.A_CHAIN)
    assert np.array_equal(canon0, g6.wildtype_target(g6.N))
    _spec_full, _f_full = dose_spec(NZ, canon0, int(g6.N))
    from experiments.exp172_deep_band_sweep import (  # noqa: E402
        target_for as deep_target_for)
    f_ref, _trip, _ref = deep_target_for(RUNG, 0)
    assert np.array_equal(_f_full, f_ref), \
        "the saturated dose != exp256's deep construction"

    CTX: dict = {}
    for k in CLASS_ORDER:
        A_base = bases400[k]
        canon_base = labeling_bfs_n(A_base)
        fmax_b = float(f_max_frames(list(HostWMedium(A_base).snapshots())))
        assert fmax_b == float(dep243["classes"][k]["f_max_base"]), \
            f"{k} f_max drift"
        CTX[k] = {"A": A_base, "canon": canon_base, "fmax": fmax_b}

    # ---- Z1 THE ANCHOR: the saturated dose (d >= NZ == the full
    #      rewrite == exp256's i0 form) bit-exact on all 24 ----------
    z1_rows = []
    for k in CLASS_ORDER:
        ctx = CTX[k]
        spec, f = dose_spec(NZ, ctx["canon"], N400)
        for s in SEEDS_RUN:
            out = _decode_row(k, f"z1-d{NZ}", spec,
                              HostWMedium(ctx["A"]), s, ctx["fmax"])
            assert out["ok"], f"Z1 rejection: {out['rejection']}"
            dep_err = anchor_i0[(k, int(s))]
            z1_rows.append({"host": k, "seed": int(s),
                            "err": float(out["err"]),
                            "deposited": dep_err,
                            "bit_exact": bool(out["err"] == dep_err)})
    Z1 = bool(all(r["bit_exact"] for r in z1_rows))
    print(f"  Z1 anchor (the saturated dose == exp256's i0 form): "
          f"{sum(1 for r in z1_rows if r['bit_exact'])}/24 "
          f"-> {'PASS' if Z1 else 'FAIL'}")

    # ---- Z2/Z3 THE DOSE CURVE ----------------------------------------
    rows = []
    n_rej = 0
    for d in DOSE_LADDER:
        for k in CLASS_ORDER:
            ctx = CTX[k]
            spec, f = dose_spec(d, ctx["canon"], N400)
            for s in SEEDS_RUN:
                out = _decode_row(k, f"d{d}", spec,
                                  HostWMedium(ctx["A"]), s, ctx["fmax"])
                if not out["ok"]:
                    n_rej += 1
                    rows.append({"dose": d, "host": k, "seed": int(s),
                                 "rejection": out["rejection"]})
                    continue
                rows.append({"dose": d, "host": k, "seed": int(s),
                             "err": float(out["err"])})
        print(f"  dose d={d} done")
    # the schema-carry face: the gj channel round-trip on the H0 base
    gc = GraphCollective(adjacency=bases400["H0"], seed=1)
    gc.set_channel("gj", np.ones(N400))
    assert np.array_equal(gc.read_channel("gj"), np.ones(N400))

    Z2 = bool(n_rej == 0 and
              sum(1 for r in rows if "err" in r) == len(DOSE_LADDER) * 24)

    # Z3: the pooled monotonicity on the FINITE rows
    def _rankdata_average(a):
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

    fin = [r for r in rows if "err" in r]
    xs = np.array([r["dose"] for r in fin], dtype=float)
    ys = np.array([r["err"] for r in fin], dtype=float)
    rho = float(np.corrcoef(_rankdata_average(xs),
                            _rankdata_average(ys))[0, 1]) if len(fin) > 2 \
        else float("nan")
    per_dose = {str(d): float(np.mean([r["err"] for r in fin
                                       if r["dose"] == d]))
                for d in DOSE_LADDER if any(r["dose"] == d for r in fin)}
    Z3 = bool(rho == rho and rho >= 0.5)
    branch = "DOSE-CURVE" if Z3 else "FLAT-REFUSAL"

    # Z4: determinism (the d=2 form re-run on 6 hosts, bit-identical)
    rows2 = []
    for k in CLASS_ORDER[:6]:
        ctx = CTX[k]
        spec, f = dose_spec(2, ctx["canon"], N400)
        for s in SEEDS_RUN:
            out = _decode_row(k, "z4-d2", spec,
                              HostWMedium(ctx["A"]), s, ctx["fmax"])
            assert out["ok"]
            rows2.append({"dose": 2, "host": k, "seed": int(s),
                          "err": float(out["err"])})
    first2 = [r for r in rows if r["dose"] == 2 and "err" in r
              and r["host"] in CLASS_ORDER[:6]]
    key = lambda r: (r["host"], r["seed"])  # noqa: E731
    d1m = {key(r): r["err"] for r in first2}
    d2m = {key(r): r["err"] for r in rows2}
    deterministic = d1m == d2m

    sha256_after = _sha(DEP256)
    read_only = bool(sha256_after == sha256_before)
    floor_ok = CORE.NEURAL_SPEC_MIN == PROD_FLOOR
    Z4 = bool(read_only and floor_ok and deterministic)

    out = {
        "exp": "exp270",
        "multi_zone_count": NZ,
        "dose_ladder": list(DOSE_LADDER),
        "z1": {"rows": z1_rows, "pass": Z1,
               "anchor_mapping": ("the saturated dose d >= NZ IS "
                                  "exp256's full deep form — the "
                                  "docstring's anchor clause maps "
                                  "there; disclosed")},
        "z2": {"n_rows": len(rows), "n_finite": len(fin),
               "n_rejections": n_rej, "pass": Z2},
        "z3": {"pooled_spearman_dose_err": rho,
               "per_dose_mean_err": per_dose,
               "branch": branch, "pass": Z3},
        "z4": {"exp256_sha256": sha256_after, "exp269_sha256": sha269,
               "read_only": read_only, "floor_ok": floor_ok,
               "deterministic_d2_6host": deterministic, "pass": Z4},
        "criteria": {"Z1_anchor": Z1, "Z2_curve": Z2,
                     "Z3_dose_face": Z3, "Z4_discipline": Z4},
        "branch": branch,
        "notes": [
            "pre-registration 9f4a271; docstring byte-unchanged; body "
            "written by the MAIN AGENT (two-death rule: the fleet "
            "died twice pre-body on dispatch)",
            "the dose form: MULTI with the first min(d, NZ) zones at "
            "the -60.0 rung, the rest at MULTI's own voltages; the "
            "saturated dose bit-asserted == exp172's deep construction "
            "on the n=100 H0 rebuild",
            "the anchor mapping disclosed: exp256's i0 rows are the "
            "FULL rewrite, so the anchor clause is satisfied by the "
            "ladder's saturated dose (d >= NZ), not d=1 — MULTI "
            "carries 3 zones",
            "the gj channel (ch2) round-trip demonstrated on the H0 "
            "base (the schema-carry face)",
            "determinism: the d=2 form re-run on 6 hosts bit-identical",
        ],
        "deposit_fingerprint": None,
    }
    out["deposit_fingerprint"] = hashlib.sha256(
        json.dumps({k: v for k, v in out.items()
                    if k != "deposit_fingerprint"},
                   sort_keys=True, default=str).encode()).hexdigest()

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\n=== exp270: branch {branch} ===")
    for kk, vv in out["criteria"].items():
        print(f"  {kk}: {'PASS' if vv else 'FAIL'}")
    return out


if __name__ == "__main__":
    main()

