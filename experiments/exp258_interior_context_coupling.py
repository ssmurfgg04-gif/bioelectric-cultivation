#!/usr/bin/env python3
"""exp258 — INTERIOR-CONTEXT BOUNDARY WRITE COUPLING (batch 22 item 3;
the FIRST channel activation under the exp257 schema — activates ch3
"ctx", the interior-context channel).

THE OPEN ITEM (exp229/exp245): ~0.686 of the boundary residual's rank
variance is unexplained by step or curvature; the four read-face
repairs (exp213 read-only boundary, exp216/exp219 context shells,
exp221 composed rules) all REFUTED — the boundary excess lives in the
channel truncation, not in the read face. The override's causal
prediction: a native interior-context channel, WRITTEN from the
boundary cell's local interior neighborhood during boundary write
passes, gives the boundary cell's write the context the truncation
destroyed — read-face changes failed because the context was never IN
the state to read.

THE MECHANISM (pre-registered, zero free parameters): during the
boundary write pass, each boundary cell's ctx channel is written with
the local interior context — the distance-weighted mean of the
interior neighbors' (theta - V) mismatch over the cell's junction
neighbors (the exp208 pair-geometry instrument's own neighborhood
definition; weights = the working conductances G_ij, normalized; no
new constants). During the write, the boundary cell's effective target
blends its chain-inherited identity with the ctx channel's read: the
blend is the pre-named ctx-gain dial g_ctx in {0, 0.25, 0.5, 1.0} —
g_ctx = 0 IS the bit-exact dormant default (the migration contract's
own face).

PRE-REGISTERED GATES:

  X1  THE DORMANT IDENTITY: g_ctx = 0 reproduces the exp257 schema's
      own battery bit-exactly (the activation's bit-exact gate — the
      dormant default is the legacy behavior).
  X2  THE COUPLING: at g_ctx > 0 the boundary rows' errs (the
      exp226/exp229 canon-boundary row class) DROP below the dormant
      baseline on the pre-named battery (exp226's c6 battery instances
      x 3 seeds) — worst boundary-row err reduction >= 10% at SOME
      pre-named g_ctx (the grid is the test, not a fit: report all
      four g_ctx values, the gate reads the best cell of the grid,
      zero post-hoc tuning).
  X3  THE SPECIFICITY: the interior rows' errs are NOT degraded at the
      same g_ctx (the coupling targets the boundary; non-interference
      on the interior) — worst interior-row err change <= +5%.
  X4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; the -60.0 floor restored and
      asserted; deterministic re-run.

THE BRANCHES (pre-named): X2 PASS -> CONTEXT-CARRIED (the truncation
diagnosis CONFIRMED causally — the boundary excess was the missing
channel); X2 REFUTE -> CONTEXT-INERT (the interior context in the
state does not close the boundary — the ~70% structure has another
carrier, deposited honestly).

RUN: exp226's c6 battery x 4 g_ctx values x 3 seeds (12 battery runs +
the dormant identity re-runs); runner.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp258_interior_context_coupling.json")


EXPECTED_HEADER_SHA256 = (
    "f6553187ac55cad850b63ba699db5c355afe8fc7a8b9521d8a494098e055e744")
_HEADER_MARKER = (
    'OUT = os.path.join(ROOT, "results", '
    '"exp258_interior_context_coupling.json")\n')


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only
    # discipline; docstring/imports/constants above byte-unchanged —
    # verified against 276e41e by EXPECTED_HEADER_SHA256 at merge; the
    # gates below are the docstring's, each evaluated exactly once)
    # =====================================================================
    import argparse
    import hashlib
    import json
    from contextlib import contextmanager

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["x1", "g025", "g050", "g100"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--pass-b", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import numpy as np

    import cultivation.bioelectric.collective as CORE
    import experiments.exp142_sign_read as M142
    import experiments.exp148_temporal_read as M148
    from cultivation.compiler.anatomy import compile_anatomy
    from cultivation.substrate.graph import GraphCollective
    from experiments.exp142_sign_read import execute_signed as _PROD_EXECUTOR
    from experiments.exp160_any_medium import config_fingerprint
    from experiments.exp166_leading_edge import CornerMedium, cell_dims
    # exp169's import BEFORE exp199's (exp213's import order): the
    # exp169-import sets the -35.0 floor across the pin modules, and
    # exp199's _PIN_SAVE snapshots THAT state so restore_floor() lands
    # exactly at the pre-run floors; the production -60.0 floor is
    # restored EXPLICITLY at the end of every process (asserted)
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp199_ro_n400_tail as M199
    from experiments.exp199_ro_n400_tail import (
        N400, PER_CELL, SEEDS, pin_floor, restore_floor)
    from experiments.exp90_two_source_read import star_dt
    from experiments.exp94_multizone_scale import (
        labeling_bfs_n, spec_target_n)

    def _sha(path: str) -> str:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    def _fingerprint(obj) -> str:
        # exp257's deterministic deposit fingerprint (no wall-clock
        # fields anywhere in the sections)
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the READ-ONLY reference deposits (X4: sha-recorded before any
    #      work in every segment; re-checked byte-unchanged at merge) ----
    DEP226 = os.path.join(ROOT, "results",
                          "exp226_boundary_dynamics_test.json")
    DEP229 = os.path.join(ROOT, "results", "exp229_curvature_test.json")
    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    DEP208 = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")
    READ_ONLY_PATHS = {"exp226": DEP226, "exp229": DEP229,
                       "exp199": DEP199, "exp208": DEP208}
    READ_ONLY_SHAS = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
    COLLECTIVE_SHA = _sha(os.path.join(
        ROOT, "cultivation", "bioelectric", "collective.py"))

    with open(DEP199) as f:
        dep199 = json.load(f)
    with open(DEP208) as f:
        dep208 = json.load(f)
    dep_by_cell = {r["j"]: r for r in dep199["cells"]["c6"]["instances"]}
    dep208_by_j = {r["j"]: r
                   for r in dep208["sections"]["c6_tail"]["instances"]}

    # ---- the read stack, asserted before any decode (exp226 verbatim) ---
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    seeds = list(SEEDS)   # exp199's (1, 2, 3) — the battery's seeds

    # ---- exp208's classification + decomposition VERBATIM (carried by
    #      exp226; the row classes, precedence intact) --------------------
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
        ident = abs(sum(p["sum_sq"] for p in per) / n
                    - err_recomputed ** 2)
        assert ident < 1e-6 * max(1.0, err_recomputed ** 2), \
            f"accounting identity violated: {ident}"
        assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
        return {"per_class": per, "identity_residual": ident}

    # ---- THE ACTIVATION INSTRUMENT (lives ENTIRELY here; collective.py
    #      untouched — sha-recorded) ---------------------------------------
    # _make_ctx_executor returns exp142's execute_signed VERBATIM (every
    # line identical, the commit branches untouched, NEURAL_SPEC_MIN
    # resolved dynamically from exp142's module global exactly as the
    # production executor resolves it) with the ONE pre-registered
    # activation interleaved at boundary cells' commits:
    #
    #   at the commit of a CANON-BOUNDARY cell i (exp208's classify on
    #   the plan, precedence intact), and ONLY at g_ctx > 0:
    #     ctx[i] := the distance-weighted mean of the interior
    #     neighbors' (theta_j - V_j) mismatch over i's junction
    #     neighbors (the exp208 pair-geometry instrument's own
    #     neighborhood: the pair support of |Wbase| > 0, read as the
    #     undirected closure — a pair exists if either directed half is
    #     present, which is how exp208's triu degree counts it for both
    #     endpoints; DISCLOSED). THE INTERIOR-NEIGHBOR READING
    #     (disclosed, outcome-blind — resolved BEFORE any non-vacuous
    #     g_ctx > 0 run was executed): "the interior neighbors" = the
    #     junction neighbors NOT in the canon-boundary class
    #     (cls[j] != 0 — on the c6 battery exactly the PAIR-JUNCTION
    #     class, precedence intact). The strict exp208-INTERIOR-class
    #     reading (cls[j] == 2) was discovered to be STRUCTURALLY EMPTY
    #     on the c6 battery (INTERIOR n_cells = 0 in all 75 of
    #     exp208's own deposited decompositions): under it the
    #     pre-registered ctx write would be a structural no-op — the
    #     instrument could never engage and the causal test would be
    #     vacuous (a single-row engineering probe confirmed the
    #     strict-class run is bit-identical to the dormant baseline);
    #     the boundary-vs-interior dichotomy the docstring uses
    #     ("the interior context", "non-interference on the interior")
    #     is honored by the non-boundary reading. X3's ROW CLASS stays
    #     strictly pre-named (cls == 2) and is reported VACUOUS with
    #     the non-boundary complement deposited as audit-only.
    #     weights = the working conductances c.G[i, j] normalized (the
    #     collective's own G = adjacency * g_gap; the scalar cancels in
    #     the normalization); no interior junction neighbor -> no
    #     context available: the write passes through verbatim
    #     (disclosed pass-through);
    #     effective target := (1 - g_ctx) * chain_inherited + g_ctx *
    #     ctx[i], where chain_inherited is the verbatim commit value
    #     (phi_spec/canon_src/chain + COMMIT_NOISE, the rng stream
    #     untouched — the activation draws NOTHING from c.rng); the
    #     effective target is written to BOTH channels exactly as the
    #     verbatim commit writes theta_new to both.
    #   g_ctx = 0.0 takes the verbatim path with ZERO deviation (no ctx
    #   write, no blend) — the bit-exact dormant default, the migration
    #   contract's own face.
    def _make_ctx_executor(medium, g_ctx: float, telemetry: dict):
        Wbase = np.asarray(medium.Wbase)
        pair_support = (np.abs(Wbase) > 0)
        pair_support = pair_support | pair_support.T   # undirected closure

        def _execute_signed_ctx(spec, adjacency, seed, op,
                                return_state=False):
            n = adjacency.shape[0]
            gamma, mu = op["gamma"], op["mu"]
            absA = np.abs(adjacency)
            dt = star_dt(gamma, float(absA.sum(axis=1).max()))       # R1
            canon = labeling_bfs_n(absA)                              # R1
            target = spec_target_n(spec, canon, n)
            c = GraphCollective(adjacency=adjacency, seed=seed,
                                gamma=gamma, mu_theta=mu)             # R2
            c.set_target(canon)
            c.write_spec_layer(target)
            prog = compile_anatomy(spec, n=n)
            if prog.rejected:
                return {"program_verified": False,
                        "rejected": prog.rejected,
                        "err_vs_target": float("nan")}
            for cl in prog.clamps:
                c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
            c.run(M142.WINDOW_H, dt=dt)
            c.release_clamps()
            reg_idx: list[int] = []
            for z in spec.zones:
                i0 = int(round(z.f0 * n))
                i1 = max(int(round(z.f1 * n)), i0 + 1)
                reg_idx.extend(range(i0, i1))
            reg_idx = sorted(set(reg_idx))
            n_ctx_writes = 0
            if reg_idx:
                reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
                region_set = set(reg_walk)
                c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
                wound_center = float(np.mean(c.theta[reg_walk]))
                parent_of: dict[int, int] = {}
                frontier: list[int] = []
                # exp97's blastema frontier under R1: |A| > 0
                for i in reg_walk:
                    nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                            if j not in region_set]
                    if nbrs:
                        parent_of[i] = int(max(
                            nbrs,
                            key=lambda j: -abs(c.theta[j] - wound_center)))
                        frontier.append(i)
                if not frontier:
                    frontier = reg_idx[:1]
                    parent_of[frontier[0]] = frontier[0]
                visited = set(frontier)
                order = [(i, parent_of[i]) for i in frontier]
                queue = list(frontier)
                while queue:
                    i = queue.pop(0)
                    for j in np.where(np.abs(c.A[i]) > 0)[0]:      # R1
                        if int(j) in region_set and int(j) not in visited:
                            visited.add(int(j))
                            parent_of[int(j)] = int(i)
                            order.append((int(j), int(i)))
                            queue.append(int(j))
                # exp208's classes on the plan (the row classes; T and
                # Wbase are g-independent, so the row sets match 1:1
                # across the whole grid — asserted at merge)
                cls = classify(target, Wbase)["class"]
                for i, src in order:
                    for _ in range(M142.STEPS_PER_CELL):
                        c.step(dt)
                    canon_src = getattr(c, "phi_spec_canon", None)
                    if c.phi_spec[i] >= M142.NEURAL_SPEC_MIN:
                        theta_new = (c.phi_spec[i]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    elif canon_src is not None:
                        theta_new = (canon_src[i]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    else:
                        theta_new = (c.theta[src]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    # ---- THE exp258 ACTIVATION (the ONLY deviation;
                    #      ZERO at g_ctx = 0.0) --------------------------
                    # the interior-neighbor reading (disclosed above,
                    # outcome-blind): junction neighbors NOT in the
                    # canon-boundary class — on c6 exactly the
                    # PAIR-JUNCTION class, precedence intact
                    if g_ctx > 0.0 and cls[i] == 0:
                        interior_j = [int(j)
                                      for j in np.where(pair_support[i])[0]
                                      if cls[j] != 0]
                        if interior_j:
                            Gw = np.array([float(c.G[i, j])
                                           for j in interior_j],
                                          dtype=float)
                            assert np.all(Gw > 0.0), \
                                "zero working conductance on a junction " \
                                "neighbor"
                            w = Gw / Gw.sum()
                            mism = np.array(
                                [float(c.theta[j] - c.V[j])
                                 for j in interior_j], dtype=float)
                            ctx_vec = c.read_channel("ctx")
                            ctx_vec[i] = float((w * mism).sum())
                            c.set_channel("ctx", ctx_vec)
                            effective = (
                                (1.0 - g_ctx) * theta_new
                                + g_ctx * float(c.read_channel("ctx")[i]))
                            c.theta[i] = effective
                            c.V[i] = effective
                            n_ctx_writes += 1
                        else:
                            # disclosed pass-through: no interior
                            # junction neighbor -> no context available
                            c.theta[i] = theta_new
                            c.V[i] = theta_new
                    else:
                        c.theta[i] = theta_new
                        c.V[i] = theta_new
            c.run(15.0, dt=dt)
            per_zone = {}
            ok_all = True
            for z in spec.zones:
                i0 = int(round(z.f0 * n))
                i1 = max(int(round(z.f1 * n)), i0 + 1)
                zmean = float(np.mean(c.V[i0:i1]))
                ok = abs(zmean - z.voltage) <= M142.ERR_BAR
                per_zone[z.name] = {"mean": round(zmean, 1),
                                    "ok": bool(ok)}
                ok_all &= ok
            err = float(c.pattern_error(target))
            ok_all &= err < M142.ERR_BAR
            out = {"program_verified": bool(ok_all), "per_zone": per_zone,
                   "err_vs_target": round(err, 2)}
            if return_state:
                out["final_state"] = {"V": c.V.tolist(),
                                      "target": target.tolist()}
            telemetry["n_ctx_writes"] = n_ctx_writes
            telemetry["ctx_last_max"] = float(
                np.abs(c.read_channel("ctx")).max())
            return out

        return _execute_signed_ctx

    @contextmanager
    def _ctx_route(medium, g_ctx: float, telemetry: dict):
        """Route exp148's executor resolution (read_temporal's global
        name) to the ctx instrument for ONE decode; the production
        attribute is restored and asserted. collective.py and every
        experiment module on disk are untouched."""
        saved = M148.execute_signed
        M148.execute_signed = _make_ctx_executor(medium, g_ctx, telemetry)
        try:
            yield
        finally:
            M148.execute_signed = saved
            assert M148.execute_signed is saved, \
                "executor route not restored"
            assert M148.execute_signed is _PROD_EXECUTOR, \
                "production executor binding drifted"

    def run_instrumented(med, s: int, fmax: float, g_ctx: float,
                         telemetry: dict) -> dict:
        with _ctx_route(med, g_ctx, telemetry):
            return M148.decode("scoped", med, s, return_state=True,
                               f_max=fmax)

    # ---- the row builder (exp226's battery construction verbatim: the
    #      c6 cell's 25 instances via exp199's gen-seed records, seeds
    #      (1,2,3), the production scoped read) ---------------------------
    def build_rows(g_ctx: float, with_production: bool) -> dict:
        rows: list = []
        n_rej = 0
        rejections: list = []
        for j in range(PER_CELL):
            dep_rec = dep_by_cell[j]
            gen_seed = dep_rec["gen_seed"]
            med = CornerMedium(N400, gen_seed, cell_dims(6))
            assert med.n == N400
            fmax = float(f_max_frames(list(med.snapshots())))
            for s_idx, s in enumerate(seeds):
                prod_rec = None
                if with_production:
                    prod = M148.decode("scoped", med, s, return_state=True,
                                       f_max=fmax)
                    if not prod["ok"]:
                        n_rej += 1
                        rejections.append({"j": j, "s": s, "route": "prod",
                                           "rejection": prod["rejection"]})
                    else:
                        prod_V = np.asarray(prod["state"]["V"], dtype=float)
                        prod_T = np.asarray(prod["state"]["target"],
                                            dtype=float)
                        prod_err_exact = float(np.sqrt(
                            np.mean((prod_V - prod_T) ** 2)))
                        assert round(prod_err_exact, 2) == round(
                            prod["err"], 2), \
                            "state err vs reported err drift (prod)"
                        prod_rec = {
                            "err": float(prod["err"]),
                            "verified": bool(prod["verified"]),
                            "err_exact": prod_err_exact,
                            "V": prod_V.tolist(), "T": prod_T.tolist()}
                tel: dict = {"n_ctx_writes": 0, "ctx_last_max": None}
                out = run_instrumented(med, s, fmax, g_ctx, tel)
                if not out["ok"]:
                    n_rej += 1
                    rejections.append({"j": j, "s": s, "route": f"g{g_ctx}",
                                       "rejection": out["rejection"]})
                    rows.append({"j": j, "s": s, "gen_seed": int(gen_seed),
                                 "rejected": True,
                                 "rejection": out["rejection"]})
                    continue
                V = np.asarray(out["state"]["V"], dtype=float)
                T = np.asarray(out["state"]["target"], dtype=float)
                err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
                assert round(err_exact, 2) == round(out["err"], 2), \
                    "state err vs reported err drift"
                cinfo = classify(T, med.Wbase)
                cls = cinfo["class"]
                bnd = cls == 0
                interior = cls == 2
                dev = np.abs(V - T)
                row = {"j": j, "s": s, "gen_seed": int(gen_seed),
                       "rejected": False,
                       "err": float(out["err"]),
                       "err_exact": err_exact,
                       "verified": bool(out["verified"]),
                       "n_ctx_writes": int(tel["n_ctx_writes"]),
                       "ctx_last_max": tel["ctx_last_max"],
                       "n_bnd": int(bnd.sum()),
                       "n_int": int(interior.sum()),
                       "bnd_max": float(dev[bnd].max()) if bnd.any() else None,
                       "int_max": (float(dev[interior].max())
                                   if interior.any() else None),
                       "nonbnd_max": float(dev[~bnd].max()),
                       "nonbnd_mean": float(dev[~bnd].mean()),
                       "bnd_errs": dev[bnd].tolist()}
                # X1's replay anchors (exp226's R1 verbatim): the
                # deposit's 2-dp errs + verified, and exp208's
                # decomposition rows bit-exactly
                dec = decompose(V, T, cls, err_exact)
                ref_dec = dep208_by_j[j]["decompositions"][s_idx]
                row["replay_dep199_err"] = bool(
                    round(out["err"], 2) == float(dep_rec["errs"][s_idx]))
                row["replay_dep199_verified"] = bool(
                    bool(out["verified"])
                    == bool(dep_rec["verified"][s_idx]))
                row["replay_exp208_decomposition"] = bool(all(
                    pc["sum_sq"] == rc["sum_sq"]
                    and pc["n_cells"] == rc["n_cells"]
                    for pc, rc in zip(dec["per_class"],
                                      ref_dec["per_class"])))
                if prod_rec is not None:
                    # X1's identity: the dormant default (g_ctx = 0) vs
                    # the production path — bit-exact state
                    row["prod"] = {
                        "err": prod_rec["err"],
                        "verified": prod_rec["verified"],
                        "err_exact": prod_rec["err_exact"],
                        "V_bit_exact": bool(np.array_equal(
                            V, np.asarray(prod_rec["V"], dtype=float))),
                        "T_bit_exact": bool(np.array_equal(
                            T, np.asarray(prod_rec["T"], dtype=float))),
                        "err_equal": bool(row["err"] == prod_rec["err"]),
                        "verified_equal": bool(
                            row["verified"] == prod_rec["verified"])}
                rows.append(row)
            print(f"  [c6 j{j:2d}] done (g_ctx={g_ctx})")
        return {"rows": rows, "n_rejections": n_rej,
                "rejections": rejections}

    def worst_over(rows, key_fn, pick):
        vals = [key_fn(r) for r in rows
                if not r.get("rejected") and key_fn(r) is not None]
        return (max(vals) if vals else None,
                sum(1 for r in rows if not r.get("rejected")))

    # ---- the segments ----------------------------------------------------
    G_CTX = {"g025": 0.25, "g050": 0.5, "g100": 1.0}

    def _seg_x1() -> dict:
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(0.0, with_production=True)
        finally:
            restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        assert floors_post == floors_pre, "floor restore failed"
        # the exp169-import restore (the standing convention): the
        # production -60.0 floor, restored EXPLICITLY, asserted at exit
        CORE.NEURAL_SPEC_MIN = -60.0
        rows = built["rows"]
        checks = []
        for r in rows:
            if r.get("rejected"):
                checks.append(False)
                continue
            p = r["prod"]
            checks.append(bool(
                p["V_bit_exact"] and p["T_bit_exact"]
                and p["err_equal"] and p["verified_equal"]
                and r["replay_dep199_err"] and r["replay_dep199_verified"]
                and r["replay_exp208_decomposition"]))
        n_ok = sum(1 for r in rows if not r.get("rejected"))
        x1_pass = bool(all(checks) and len(checks) == PER_CELL * len(SEEDS)
                       and built["n_rejections"] == 0 and n_ok
                       == PER_CELL * len(SEEDS))
        wb, _ = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, "read-only deposit changed (x1)"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            "collective.py changed (x1)"
        return {"g_ctx": 0.0, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_checks_pass": sum(1 for c in checks if c),
                "n_checks": len(checks),
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": x1_pass}

    def _seg_grid(seg: str) -> dict:
        g_ctx = G_CTX[seg]
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(g_ctx, with_production=False)
        finally:
            restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        assert floors_post == floors_pre, "floor restore failed"
        CORE.NEURAL_SPEC_MIN = -60.0
        rows = built["rows"]
        wb, n_ok = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, \
            f"read-only deposit changed ({seg})"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            f"collective.py changed ({seg})"
        return {"g_ctx": g_ctx, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_ctx_writes_total": sum(r["n_ctx_writes"] for r in rows
                                          if not r.get("rejected")),
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": bool(built["n_rejections"] == 0
                             and n_ok == PER_CELL * len(SEEDS))}

    # ---- the merge (the gates, each evaluated exactly once) --------------
    def _merge(paths_a: list, paths_b) -> dict:
        # BODY-ONLY PLUMBING REPAIR (disclosed; no gate outcome affected):
        # the merge process's own import chain (exp169 -> exp199) leaves
        # the -35.0 instrument floor across the pin modules; the
        # pre-registered -60.0 restore is applied HERE, before the X4
        # record is built, so the deposit's merge-side floor_at_exit
        # carries the production floor the discipline names (the
        # segment sections already restored and recorded -60.0
        # themselves; the process exit assert below is unchanged).
        CORE.NEURAL_SPEC_MIN = -60.0
        sections: dict = {}
        for p in paths_a:
            with open(p) as f:
                d = json.load(f)
            assert d["seg"] not in sections, "duplicate segment"
            sections[d["seg"]] = d["section"]
        x1 = sections["x1"]
        g025 = sections["g025"]
        g050 = sections["g050"]
        g100 = sections["g100"]
        grid_secs = {"0.25": g025, "0.5": g050, "1.0": g100}

        # the file-integrity gate: the pre-registered header (docstring,
        # imports, constants — 276e41e's bytes through the OUT line)
        raw_self = open(os.path.abspath(__file__), "rb").read()
        mk = raw_self.find(_HEADER_MARKER.encode())
        assert mk != -1, "header marker not found"
        header_sha = hashlib.sha256(
            raw_self[:mk + len(_HEADER_MARKER)]).hexdigest()
        header_unchanged = bool(header_sha == EXPECTED_HEADER_SHA256)
        assert header_unchanged, (
            f"the pre-registered header drifted: {header_sha}")

        # ---- X1 (the dormant identity, the migration gate) --------------
        g_x1 = bool(x1["pass"])

        # ---- X2 (the coupling; the grid is the test, the gate reads the
        #      best cell) --------------------------------------------------
        base_bnd = x1["worst_bnd_err_mV"]
        assert base_bnd is not None and base_bnd > 0.0, \
            "degenerate baseline worst boundary-row err"
        cells = {}
        reds = {}
        for gv, sec in grid_secs.items():
            wb = sec["worst_bnd_err_mV"]
            red = float((base_bnd - wb) / base_bnd)
            reds[gv] = red
            cells[gv] = {"worst_bnd_err_mV": wb,
                         "worst_int_err_mV": sec["worst_int_err_mV"],
                         "worst_nonbnd_err_mV": sec["worst_nonbnd_err_mV"],
                         "reduction_vs_dormant": red,
                         "n_ctx_writes_total": sec["n_ctx_writes_total"],
                         "n_rows": sec["n_rows"],
                         "n_ok": sec["n_ok"]}
        g_star = max(reds, key=lambda k: reds[k])
        x2_reduction = reds[g_star]
        x2_pass = bool(x2_reduction >= 0.10)

        # ---- X3 (the specificity) ----------------------------------------
        n_int_total = sum(r["n_int"] for sec in
                          [x1] + list(grid_secs.values())
                          for r in sec["rows"] if not r.get("rejected"))
        base_int = x1["worst_int_err_mV"]
        star_int = grid_secs[g_star]["worst_int_err_mV"]
        if n_int_total == 0:
            # the exp208 INTERIOR class is EMPTY on the c6 battery
            # (exp208's own deposit carries INTERIOR n_cells = 0 in all
            # 75 decompositions): no interior row exists that the
            # coupling could degrade — the pre-named gate is satisfied
            # vacuously and is NOT evidence of non-interference; the
            # non-boundary (PAIR-JUNCTION-complement) reading is
            # deposited alongside as an audit-only number, never gated
            x3_pass = True
            x3_vacuous = True
            x3_change = None
        else:
            x3_vacuous = False
            x3_change = float((star_int - base_int) / base_int)
            x3_pass = bool(x3_change <= 0.05)
        base_nonbnd = x1["worst_nonbnd_err_mV"]
        star_nonbnd = grid_secs[g_star]["worst_nonbnd_err_mV"]
        nonbnd_change = float((star_nonbnd - base_nonbnd) / base_nonbnd)

        # ---- X4 (the discipline) -----------------------------------------
        shas_ok = True
        for sec in sections.values():
            if sec.get("read_only_shas") != READ_ONLY_SHAS:
                shas_ok = False
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        deposits_unchanged = bool(shas_now == READ_ONLY_SHAS and shas_ok)
        coll_now = _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                     "collective.py"))
        coll_unchanged = bool(coll_now == COLLECTIVE_SHA)
        n_rej_total = sum(sec["n_rejections"] for sec in sections.values())
        det = {"pass_b_byte_identical": None, "segments": {}}
        if paths_b:
            assert len(paths_b) == len(paths_a), \
                "pass B segment count mismatch"
            for pa, pb in zip(paths_a, paths_b):
                sa = hashlib.sha256(open(pa, "rb").read()).hexdigest()
                sb = hashlib.sha256(open(pb, "rb").read()).hexdigest()
                det["segments"][os.path.basename(pb)] = {
                    "pass_a_sha256": sa, "pass_b_sha256": sb,
                    "byte_identical": bool(sa == sb)}
            det["pass_b_byte_identical"] = bool(all(
                v["byte_identical"] for v in det["segments"].values()))
        floor_ok = all(float(sec["floor_at_exit"]) == -60.0
                       for sec in sections.values())
        x4_pass = bool(deposits_unchanged and coll_unchanged
                       and floor_ok and n_rej_total == 0
                       and det["pass_b_byte_identical"]
                       and header_unchanged)

        n_pass = sum(1 for v in (g_x1, x2_pass, x3_pass, x4_pass) if v)
        if not g_x1:
            branch = "MIGRATION-GATE-FAILED"
        elif x2_pass:
            branch = "CONTEXT-CARRIED"
        else:
            branch = "CONTEXT-INERT"
        verdict = (f"{n_pass}/4 gates (X1 X2 X3 X4) | "
                   f"X2 {'PASS' if x2_pass else 'REFUTE'} "
                   f"(worst boundary-row reduction "
                   f"{x2_reduction:.4f} at g_ctx={g_star}) | "
                   f"X3 {'VACUOUS' if x3_vacuous else ('PASS' if x3_pass else 'REFUTE')} "
                   f"(exp208 INTERIOR class empty on c6: {n_int_total} "
                   f"rows; audit-only non-boundary change "
                   f"{nonbnd_change:+.4f}) | {branch}")

        deposit = {
            "exp": "exp258",
            "claim": (
                "INTERIOR-CONTEXT BOUNDARY WRITE COUPLING (the FIRST "
                "channel activation under the exp257 schema): ch3 ctx "
                "written from the interior neighbors' (theta - V) "
                "mismatch during boundary write passes; the boundary "
                "cell's effective target blends its chain-inherited "
                "identity with the ctx read at the pre-named g_ctx grid "
                "{0, 0.25, 0.5, 1.0} — the truncation diagnosis's "
                "causal test (X2 PASS -> CONTEXT-CARRIED / REFUTE -> "
                "CONTEXT-INERT)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any body "
                    "(pre-registration 276e41e, batch 22; gates X1-X4 "
                    "fixed there, each evaluated exactly once); the "
                    "pre-registered header (docstring + imports + "
                    "constants) sha256-verified byte-unchanged at "
                    "merge: " + EXPECTED_HEADER_SHA256),
                "mechanism": (
                    "during the boundary write pass (exp142's "
                    "execute_signed commit loop, routed through the "
                    "experiment's own instrument — collective.py "
                    "untouched), each CANON-BOUNDARY cell's ctx channel "
                    "is written with the distance-weighted mean of the "
                    "interior neighbors' (theta - V) mismatch over the "
                    "cell's junction neighbors (exp208's pair support "
                    "|Wbase| > 0, undirected closure); the "
                    "INTERIOR-NEIGHBOR READING (disclosed, "
                    "outcome-blind — resolved BEFORE any non-vacuous "
                    "g_ctx > 0 run was executed): the junction "
                    "neighbors NOT in the canon-boundary class "
                    "(cls != 0; on c6 exactly the PAIR-JUNCTION class, "
                    "precedence intact) — the strict exp208-INTERIOR "
                    "reading is STRUCTURALLY EMPTY on this battery "
                    "(INTERIOR n_cells = 0 in all 75 of exp208's own "
                    "deposited decompositions), under which the "
                    "pre-registered write would be a structural no-op "
                    "and the causal test vacuous; weights = the working "
                    "conductances c.G[i, j] normalized; no interior "
                    "junction neighbor -> verbatim pass-through, "
                    "disclosed); the effective target = (1 - g_ctx) * "
                    "chain_inherited + g_ctx * ctx_read, written to "
                    "both channels; g_ctx = 0 is the bit-exact dormant "
                    "default (zero deviation, no ctx write); the "
                    "activation draws NOTHING from c.rng"),
                "row_conventions": (
                    "a ROW = one per-cell err |V_i - T_i| (mV) at a "
                    "cell of the exp226/exp229 canon-boundary row "
                    "class (exp208's classify, precedence intact), "
                    "pooled over exp226's c6 battery (25 instances x 3 "
                    "seeds); 'worst boundary-row err' = the max over "
                    "that pooled row set; X3's 'interior rows' = the "
                    "exp208 INTERIOR class (cls == 2) under the same "
                    "convention"),
                "conventions": (
                    "the executor instrument is exp142's "
                    "execute_signed copied line-for-line into this "
                    "module with the ONE activation block; bit-exact "
                    "identity at g_ctx = 0 is asserted per row against "
                    "the production decode AND exp199's deposit AND "
                    "exp208's decomposition rows (exp226's R1 "
                    "machinery verbatim); T and Wbase are "
                    "g-independent so the row sets match 1:1 across "
                    "the grid")},
            "sections": {"x1": x1, "g025": g025, "g050": g050,
                         "g100": g100},
            "grid": {"g_values": [0.0, 0.25, 0.5, 1.0],
                     "baseline_cell": {
                         "g_ctx": 0.0,
                         "worst_bnd_err_mV": base_bnd,
                         "worst_int_err_mV": base_int,
                         "worst_nonbnd_err_mV": base_nonbnd,
                         "source": "x1's g_ctx=0 rows (bit-exact vs "
                                   "production per X1)"},
                     "cells": cells,
                     "g_star": float(g_star),
                     "x2_reduction_at_best_cell": x2_reduction},
            "gates": {
                "X1": {"pass": g_x1, "migration_gate": True,
                       "n_rows": x1["n_rows"], "n_ok": x1["n_ok"],
                       "n_checks_pass": x1["n_checks_pass"],
                       "n_checks": x1["n_checks"],
                       "disclosure": (
                           "g_ctx = 0 vs the production scoped decode: "
                           "V/T states bit-exact, errs + verified "
                           "equal, exp199's deposit replayed at its "
                           "2-dp rounding, exp208's decomposition rows "
                           "reproduced bit-exactly (exp226's R1 "
                           "verbatim)")},
                "X2": {"pass": x2_pass, "clause": (
                            "worst boundary-row err reduction >= 10% "
                            "at SOME pre-named g_ctx (the grid is the "
                            "test; the gate reads the best cell; all "
                            "four g values reported)"),
                       "g_star": float(g_star),
                       "reduction_at_best_cell": x2_reduction,
                       "all_cells": cells},
                "X3": {"pass": x3_pass, "vacuous": x3_vacuous,
                       "n_interior_rows_total": int(n_int_total),
                       "worst_interior_change_at_g_star": x3_change,
                       "clause": ("worst interior-row err change "
                                  "<= +5% at the X2 best cell"),
                       "disclosure": (
                           "X3's row class stays STRICTLY pre-named "
                           "(exp208's classify, precedence intact): the "
                           "exp208 INTERIOR class (cls == 2) is EMPTY on "
                           "the c6 battery (INTERIOR n_cells = 0 in all "
                           "75 of exp208's own deposited decompositions "
                           "— the p=0.04 pair support gives every "
                           "non-boundary cell pair-degree >= 2): no "
                           "interior row exists to degrade; the gate "
                           "is satisfied vacuously and is NOT "
                           "evidence of non-interference. The "
                           "MECHANISM's own interior-neighbor reading "
                           "(disclosed, outcome-blind) uses the "
                           "non-boundary junction neighbors so the "
                           "pre-registered write engages at all; the "
                           "matching non-boundary complement "
                           "(PAIR-JUNCTION + INTERIOR rows) is "
                           "deposited as an audit-only reading, "
                           "never gated"),
                       "audit_only_non_boundary": {
                           "worst_change_at_g_star": nonbnd_change,
                           "baseline": base_nonbnd,
                           "at_g_star": star_nonbnd,
                           "never_gated": True}},
                "X4": {"pass": x4_pass,
                       "deposits_read_only": {
                           k: {"sha256": READ_ONLY_SHAS[k],
                               "unchanged": bool(shas_now[k]
                                                 == READ_ONLY_SHAS[k])}
                           for k in READ_ONLY_SHAS},
                       "collective_py_sha256": coll_now,
                       "collective_py_unchanged": coll_unchanged,
                       "n_rejections_total": n_rej_total,
                       "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                       "floor_ok": bool(
                           float(CORE.NEURAL_SPEC_MIN) == -60.0),
                       "determinism": det,
                       "header_unchanged": header_unchanged}},
            "branch": branch,
            "verdict": verdict,
            "notes": [
                "body written by the run agent under the body-only "
                "discipline; the pre-registered header (docstring, "
                "imports, constants) byte-unchanged, verified against "
                "276e41e by sha256 at merge",
                "the activation instrument routes exp148's executor "
                "name to the experiment's own verbatim copy of "
                "exp142's execute_signed for the instrumented decodes "
                "only; the production binding is restored and asserted "
                "around every decode; no file on disk modified but "
                "this module",
                "X1 is the migration gate: it was run FIRST and the "
                "grid segments only followed its PASS",
                "one body-side engineering probe (a single row's "
                "production-vs-g_ctx=0 bit-exactness, run in a scratch "
                "session before the battery to verify the executor "
                "copy integrates) was performed OUTSIDE the deposited "
                "evaluation; that probe also surfaced the "
                "strict-INTERIOR-class structural emptiness (the "
                "instrument never engaged, bit-identical to the "
                "dormant baseline) — the interior-neighbor reading was "
                "resolved to the non-boundary junction neighbors "
                "BEFORE any non-vacuous g_ctx > 0 run was executed, "
                "outcome-blind, disclosed in pre_registered.mechanism; "
                "no gate was evaluated twice",
                "no wall-clock fields anywhere in this deposit; "
                "deterministic re-run recorded via pass B byte-" 
                "identity"],
            "deposit_fingerprint": None,
        }
        deposit["deposit_fingerprint"] = _fingerprint(
            {k: v for k, v in deposit.items() if k != "deposit_fingerprint"})
        return deposit

    # ---- dispatch ---------------------------------------------------------
    if args.merge is not None:
        result = _merge(args.merge, args.pass_b)
    elif args.seg == "x1":
        result = {"seg": "x1", "section": _seg_x1()}
    elif args.seg in G_CTX:
        result = {"seg": args.seg, "section": _seg_grid(args.seg)}
    else:
        raise SystemExit("use --seg {x1,g025,g050,g100} / --merge "
                         "(runner split is canonical)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, default=str)
    if args.merge:
        print(f"=== exp258 MERGE: branch {result['branch']} ===")
        for k, v in result["gates"].items():
            print(f"  {k}: {'PASS' if v['pass'] else 'REFUTE/FAIL'}")
        print(f"  {result['verdict']}")
    else:
        sec = result["section"]
        print(f"=== exp258 seg {result['seg']}: "
              f"{'PASS' if sec.get('pass') else 'FAIL'} ===")
    # the production floor at exit, asserted (the exp169-import
    # restore convention)
    CORE.NEURAL_SPEC_MIN = -60.0
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == -60.0, \
        "production floor not restored at exit"
    return result


if __name__ == "__main__":
    main()
