#!/usr/bin/env python3
"""exp259 — PAIR-CELL GEOMETRY COMPENSATION (batch 22 item 4; the SECOND
channel activation under the exp257 schema — activates ch2 "gj", the
per-cell gap-junction state).

THE OPEN ITEM (exp254/exp255): the deep-band substitution re-wires the
pair-junction structure and the reader's price follows it (pair share
70.1% -> 83.5%, the substituted medium's pair cells' RMS err 3.706 vs
the rest's 3.520); the cost decouples from the host-level boundary
geometry (rho 0.137) and lives at the ROW level (exp256's test). The
compensation: local junction-weight re-scaling targeted specifically
at the substituted pair cells.

THE MECHANISM (pre-registered, zero free parameters): the per-cell gj
channel (ch2) carries each cell's junction-weight multiplier; the
compensation pass renormalizes each PAIR-JUNCTION cell's multiplier so
the cell's effective pair-participation (sum of working conductances
to its pair-junction neighbors) matches the CANONICAL medium's mean
pair-participation over its own pair cells (the canonical-match rule —
the canonical medium is the target of record, no new constants; the
non-pair cells' multipliers stay 1.0; the total conductance
conservation is asserted: the compensation redistributes, it does not
amplify — sum(G) post == sum(G) pre within 1e-9).

PRE-REGISTERED GATES:

  P1  THE DORMANT IDENTITY: gj at defaults (all multipliers 1.0)
      reproduces the exp257 schema's own battery bit-exactly.
  P2  THE COMPENSATION: applying the canonical-match renormalization
      to the substituted medium's pair cells REDUCES the reader's
      worst err on the substituted rows (exp243's 12 candidate hosts x
      the P3 medium x 3 seeds) — pooled worst-err reduction >= 10%
      (the pre-named bar; all rows reported, zero post-hoc selection).
  P3  THE SPECIFICITY / NON-INTERFERENCE: the SAME compensation
      applied to the canonical media does NOT degrade them (worst-err
      change <= +5% on the P1/P2 rows) — the lever is specific to the
      substitution's pair re-wiring.
  P4  THE DISCIPLINE: exp243's/exp254's deposits READ-ONLY
      sha-recorded byte-unchanged; conductance conservation asserted;
      the -60.0 floor restored and asserted; deterministic re-run.

THE BRANCHES (pre-named): P2 PASS -> PAIR-COMPENSATED (the pair
geometry's causal face lands — the row-level driver is compensated at
its own scale); P2 REFUTE -> COMPENSATION-INERT (the pair re-wiring is
not the row-level driver's lever, deposited honestly).

RUN: 12 hosts x 2 media x 3 seeds x {on, off} (48 scoped reads) + the
dormant identity battery; runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp259_pair_geometry_compensation.json")


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
    #      discipline, exp243's/exp256's reader-line application) -------
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

    # ---- the frozen read configuration (exp243's, exp256's battery-
    #      adapted VERBATIM; the ONE added disclosure: the gj channel
    #      is the carrier of record, the read's medium its projection)
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
        "gj_channel": ("ch2 'gj' carries the per-cell multipliers "
                       "(set_channel); the read's medium is its "
                       "projection onto the adjacency (the weighted "
                       "W); support unchanged (multipliers positive)"),
        "compensation_rule": ("pair cells' multipliers m_i = "
                              "target_part / part_i with part_i = sum "
                              "of working conductances to the "
                              "medium's own PAIR-JUNCTION cells "
                              "(exp208's classify under the row's "
                              "own target); target_part = the HOST "
                              "BASE medium's canon-row mean "
                              "pair-participation (one constant per "
                              "host); non-pair cells 1.0; then the "
                              "global conservation renormalization "
                              "sum(W_post) = sum(W_pre)"),
        "pooled_form": ("P2/P3's pooled worst-err = the MEAN over the "
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

    # ---- exp225's build_rows (exp256's VERBATIM, checksummed) ---------
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

    # ---- exp208's classify (exp256's VERBATIM) ------------------------
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

    # ---- THE COMPENSATION INSTRUMENT (the docstring's zero-knob
    #      canonical-match rule; the one per-host constant is the BASE
    #      medium's canon-row mean pair-participation) ------------------
    def pair_participation(A: np.ndarray, junction: np.ndarray,
                           i: int) -> float:
        """sum of the working conductances from cell i to the
        medium's own PAIR-JUNCTION cells (the pre-named reading)."""
        return float(sum(A[i, j] for j in range(A.shape[0])
                         if j != i and A[i, j] > 0 and junction[j]))

    def canonical_target_part(A_base: np.ndarray,
                              canon_t: np.ndarray) -> float:
        j = classify(canon_t, A_base)["junction"]
        parts = [pair_participation(A_base, j, int(i))
                 for i in np.where(j)[0]]
        assert parts, "the canonical medium carries no pair cells"
        return float(np.mean(parts))

    def compensate(A_med: np.ndarray, T_row: np.ndarray,
                   target_part: float, identity: bool = False):
        """The per-row compensation: multipliers on the substituted
        medium's PAIR-JUNCTION cells (m_i = target_part / part_i),
        non-pair cells 1.0, then the global conservation
        renormalization. identity=True forces all multipliers 1.0
        (the P1 dormant-identity form). Returns (W, multipliers)."""
        n = A_med.shape[0]
        J = classify(T_row, A_med)["junction"]
        m = np.ones(n, dtype=float)
        if not identity:
            for i in np.where(J)[0]:
                p = pair_participation(A_med, J, int(i))
                if p > 0.0:
                    m[int(i)] = target_part / p
        W = A_med.copy().astype(float)
        for i in np.where(J)[0]:
            if not identity:
                W[int(i), :] *= m[int(i)]
                W[:, int(i)] *= m[int(i)]
        s_pre = float(np.asarray(A_med, dtype=float).sum())
        s_w = float(W.sum())
        W *= s_pre / s_w
        assert abs(float(W.sum()) - s_pre) <= 1e-9 * max(1.0, abs(s_pre)), \
            "conductance conservation violated"
        return W, m

    # ---- the 12 hosts rebuilt from exp243's deposit (exp256's
    #      rebuild VERBATIM: shas, edge counts, canon identity) ---------
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
        # the host's ONE compensation constant: the BASE medium's
        # canon-row mean pair-participation
        tp = canonical_target_part(A_base, canon_row["f"])
        CTX[k] = {
            "base": A_base, "canon": canon_base, "fmax": fmax_b,
            "cand": cand, "target_part": tp,
            "arms": {
                ARM_CANON: [
                    {"pert": PERT_ORDER[0], "row": canon_row,
                     "med0": mirror_med},
                    {"pert": PERT_ORDER[1], "row": canon_row,
                     "med0": bd_med}],
                ARM_SUBST: [
                    {"pert": PERT_ORDER[2], "row": deep_rows[0],
                     "med0": A_base},
                    {"pert": PERT_ORDER[2], "row": deep_rows[1],
                     "med0": A_base}]}}

    print(f"=== exp259: PAIR-CELL GEOMETRY COMPENSATION (the second "
          f"channel activation, ch2 'gj') ===")
    print(f"  battery: 12 hosts x 2 arms x 3 seeds x 2 instances at "
          f"n={N400}; read fingerprint {FP}")
    print(f"  compensation: canonical-match multipliers, conservation "
          f"asserted; P1 identity first\n")

    # ---- P1 THE DORMANT IDENTITY: identity multipliers are a no-op
    #      (W == A bit-exact on ALL 12 hosts) + the H3 battery at
    #      identity multipliers reproduces exp243's deposited errs
    #      bit-exact (the machinery anchor) ------------------------------
    p1_identity_ok = True
    for k in CLASS_ORDER:
        ctx = CTX[k]
        W_id, m_id = compensate(ctx["base"], ctx["canon"],
                                ctx["target_part"], identity=True)
        if not (np.array_equal(W_id, ctx["base"].astype(float))
                and np.all(m_id == 1.0)):
            p1_identity_ok = False
    h3 = "H3"
    ctx3 = CTX[h3]
    p1_rows = []
    for s in SEEDS_RUN:
        for arm in ARMS:
            errs = []
            for inst in ctx3["arms"][arm]:
                W_id, _ = compensate(inst["med0"], inst["row"]["f"],
                                     ctx3["target_part"], identity=True)
                assert np.array_equal(W_id, inst["med0"].astype(float))
                out = _decode_row(h3, f"p1:{arm}:{inst['row']['key']}",
                                  inst["row"]["spec"],
                                  HostWMedium(W_id), s, ctx3["fmax"])
                assert out["ok"], f"P1 rejection: {out['rejection']}"
                errs.append(float(out["err"]))
            dep_worst = max(
                float(e) for e in ctx3["cand"][
                    (inst["pert"], inst["row"]["key"])]["errs"])
            # per-seed deposited errs are per (row, seed); the arm's
            # deposited worst at this seed:
            dep_seed_worst = max(
                float(ctx3["cand"][(i["pert"], i["row"]["key"])]
                      ["errs"][SEEDS_RUN.index(s)])
                for i in ctx3["arms"][arm])
            p1_rows.append({"host": h3, "arm": arm, "seed": int(s),
                            "worst": max(errs),
                            "deposited_worst": dep_seed_worst})
    p1_repro_ok = all(
        r["worst"] == r["deposited_worst"] for r in p1_rows)
    P1 = bool(p1_identity_ok and p1_repro_ok)
    print(f"  P1 dormant identity: no-op 12/12 hosts, H3 reproduction "
          f"{sum(1 for r in p1_rows if r['worst'] == r['deposited_worst'])}"
          f"/12 -> {'PASS' if P1 else 'FAIL'}")

    # ---- the compensated battery: both arms, all 12 hosts, 3 seeds
    #      (the gj channel carries the multipliers; the read consumes
    #      the weighted medium) ------------------------------------------
    def run_comp_battery(pass_tag: str, hosts=None) -> list:
        rows_out = []
        n_rej = 0
        for k in (hosts or CLASS_ORDER):
            ctx = CTX[k]
            for s in SEEDS_RUN:
                for arm in ARMS:
                    errs = []
                    for inst in ctx["arms"][arm]:
                        W, m = compensate(inst["med0"],
                                          inst["row"]["f"],
                                          ctx["target_part"])
                        # the gj channel is the carrier of record
                        gc = GraphCollective(adjacency=W, seed=1)
                        gc.set_channel("gj", m)
                        assert np.array_equal(gc.read_channel("gj"), m)
                        out = _decode_row(
                            k, f"{pass_tag}:{arm}:{inst['row']['key']}",
                            inst["row"]["spec"], HostWMedium(W), s,
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

    rows_on = run_comp_battery("on")

    # determinism: the substituted arm re-run, bit-identical (S4/P4)
    rows_on2 = run_comp_battery("on2", hosts=CLASS_ORDER[:6])
    key = lambda r: (r["host"], r["arm"], r["seed"])  # noqa: E731
    d1 = {key(r): r for r in rows_on if r["host"] in
          [h for h in CLASS_ORDER[:6]]}
    d2 = {key(r): r for r in rows_on2}
    deterministic = (set(d1) == set(d2)
                     and all(d1[kk] == d2[kk] for kk in d1))

    # ---- the OFF baselines: exp243's DEPOSITED errs (exp256 verified
    #      the machinery reproduces them bit-exact; the deposit IS the
    #      zero-drift baseline) ------------------------------------------
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
    chg_can = (mean(on_can) - mean(off_can)) / mean(off_can)

    P2 = bool(red_sub >= 0.10)
    P3 = bool(chg_can <= 0.05)

    sha243_after = _sha(DEP243)
    read_only = bool(sha243_after == sha243_before)
    floor_ok = CORE.NEURAL_SPEC_MIN == PROD_FLOOR

    P4 = bool(read_only and floor_ok and deterministic)

    out = {
        "exp": "exp259",
        "read_config": READ_CONFIG,
        "fingerprint": FP,
        "p1": {"identity_noop_12": p1_identity_ok,
               "h3_reproduction_rows": p1_rows, "pass": P1},
        "p2": {"off_worst_mean": mean(off_sub),
               "on_worst_mean": mean(on_sub),
               "reduction_frac": red_sub,
               "rows": [r for r in rows_on if r["arm"] == ARM_SUBST],
               "pass": P2},
        "p3": {"off_worst_mean": mean(off_can),
               "on_worst_mean": mean(on_can),
               "change_frac": chg_can,
               "rows": [r for r in rows_on if r["arm"] == ARM_CANON],
               "pass": P3},
        "p4": {"exp243_sha256": sha243_after, "exp254_sha256": sha254,
               "read_only": read_only, "floor_ok": floor_ok,
               "deterministic_6host_rerun": deterministic, "pass": P4},
        "criteria": {"P1_dormant_identity": P1,
                     "P2_compensation": P2,
                     "P3_non_interference": P3,
                     "P4_discipline": P4},
        "branch": ("PAIR-COMPENSATED" if (P1 and P2 and P3 and P4)
                   else "COMPENSATION-INERT"),
        "notes": [
            "pre-registration 276e41e; docstring byte-unchanged; body "
            "written by the MAIN AGENT (two-death rule: the fleet died "
            "twice pre-body on dispatch)",
            "the compensation multipliers are per (host, row): the "
            "substituted rows' own PAIR-JUNCTION classification (the "
            "row's own target, exp254's precedent); the target "
            "participation is the host BASE medium's canon-row mean — "
            "ONE constant per host, zero knobs",
            "conservation: the global renormalization sum(W_post) == "
            "sum(W_pre) asserted per compensation (the compensation "
            "redistributes, it does not amplify)",
            "the OFF baseline is exp243's deposited errs (exp256 "
            "verified the shared machinery reproduces them bit-exact)",
            "the pooled form (mean over the 36 rows of the arm's worst "
            "err) is fixed in the body's READ_CONFIG, zero selection; "
            "all rows deposited",
            "the gj channel (ch2) is the multipliers' carrier of "
            "record (set_channel/read_channel round-trip asserted per "
            "decode); the read's medium is the channel's projection "
            "onto the adjacency",
            "determinism: the substituted arm re-run on hosts H0-H5 "
            "bit-identical in-process",
        ],
        "deposit_fingerprint": None,
    }
    out["deposit_fingerprint"] = hashlib.sha256(
        json.dumps({k: v for k, v in out.items()
                    if k != "deposit_fingerprint"},
                   sort_keys=True, default=str).encode()).hexdigest()

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\n=== exp259: branch {out['branch']} ===")
    for kk, vv in out["criteria"].items():
        print(f"  {kk}: {'PASS' if vv else 'FAIL'}")
    return out


if __name__ == "__main__":
    main()
