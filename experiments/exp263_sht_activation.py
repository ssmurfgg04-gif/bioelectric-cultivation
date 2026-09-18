#!/usr/bin/env python3
"""exp263 — THE SHT CHANNEL ACTIVATION (batch 24 item 2; L239's
registered next (b) — the FOURTH activation under the exp257 schema,
ch5 "sht", the paper's 5-HT electrophoresis face).

THE OPEN ITEM: the paper's census (exp232) names serotonin transport
(5-HT electrophoresis) as one of the 8 channels — ABSENT from the
stack; the exp257 schema gave it native state (ch5, dormant). BETSE
carries no serotonin machinery (its ion set is Na/K/Cl/Ca — verified
against the reference tree's ion enum), so the grounding is the
paper's OWN spec face: 5-HT transport is a CHARGE-COUPLED flux — the
transporter moves transmitter down the ELECTROCHEMICAL gradient
(SERT-like: the flux follows the Vmem difference the stack already
computes). The stack-native pre-named instrument: the sht channel
carries the theta-gradient's transport face — the per-cell flux
proportional to the sum of the cell's V-differences to its junction
neighbors (the same electrochemical face the GJ network carries, read
through the transporter's sign convention), accumulated over the
settle.

PRE-REGISTERED GATES (the exp258/exp261 mold: identity, readout,
gated coupling):

  H1  THE DORMANT IDENTITY: g_sht = 0 reproduces the production
      decode bit-exactly on the c6 battery (75/75 rows, the exp258
      X1 form verbatim).
  H2  THE READOUT (zero-risk, read-only): on the c6 battery's settled
      states, the sht field S_i (the accumulated electrochemical
      flux face) is computed per cell; the pre-named association:
      Spearman(S_i, the cell's |V_i - theta_i| mismatch) >= 0.5 over
      the pooled battery points.
  H3  THE WRITE COUPLING (only if H2 passes; else SKIPPED-H2-FAIL):
      the transporter's pull — the cell's theta restoration pull
      multiplied by (1 + g_sht * (S_i - S̄)/S̄_scale) at the pre-named
      grid {0, 0.25, 0.5, 1.0} (S̄_scale = the battery-wide mean |S|,
      the zero-knob normalizer); the gates: the best cell reduces the
      worst boundary-row err >= 10% AND the non-boundary rows'
      worst-err change <= +5%.
  H4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded; collective.py untouched sha-recorded (the
      activation lives in the module via the public accessors);
      the -60.0 floor restored and asserted; deterministic re-run;
      no wall-clock fields.

THE BRANCHES (pre-named): SHT-CARRIES / SHT-READOUT-ONLY /
SHT-INERT — deposited honestly.

RUN: the c6 battery x the grid; foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp263_sht_activation.json")

# ==== BODY (written by the run agent under the body-only discipline;
# docstring/imports/constants above byte-unchanged — verified against
# 437ee24 by EXPECTED_HEADER_SHA256 at merge; the gates below are the
# docstring's, each evaluated exactly once) =============================
EXPECTED_HEADER_SHA256 = (
    "cab89fc0d777a6a16b6f32e4592ab6980b33cf2e249a8d89a93ea9284cb6f0cc")
_HEADER_MARKER = (
    'OUT = os.path.join(ROOT, "results", '
    '"exp263_sht_activation.json")\n')
DOCSTRING_SHA256 = (
    "093a7dabe82defb4cc9fab3cafca657e6dbc04b777010fdfe080df4d8f1210a8")


def _docstring_sha() -> str:
    # the pre-registered docstring bytes (the opening '"""' after the
    # shebang through the closing '"""' + newline), sha256'd; asserted
    # BEFORE any work and AGAIN after the deposit is written, in every
    # process (the hard rule: byte-unchanged vs 437ee24)
    import hashlib
    raw = open(os.path.abspath(__file__), "r").read()
    start = raw.index('"""', raw.index("\n") + 1)
    end = raw.index('"""', start + 3)
    return hashlib.sha256(raw[start:end + 4].encode()).hexdigest()


def main() -> dict:
    # ==== imports (the exp258/exp261 machinery; the BLAS pins precede
    #      the numpy import — the pre-registered header's discipline) ===
    import argparse
    import hashlib
    import json
    from contextlib import contextmanager

    # the docstring gate, FIRST in every process (segments, gates,
    # merge): fail = STOP before anything runs
    assert _docstring_sha() == DOCSTRING_SHA256, \
        "the pre-registered docstring drifted (pre-work assert)"

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["h1", "g025", "g050", "g100"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--pass-b", nargs="*", default=None)
    ap.add_argument("--h2-gate", default=None, metavar="H1_SEG_JSON")
    ap.add_argument("--sbar-from", default=None, metavar="H1_SEG_JSON")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import numpy as np

    import cultivation.bioelectric.collective as CORE
    import experiments.exp142_sign_read as M142
    import experiments.exp148_temporal_read as M148
    from cultivation.compiler.anatomy import compile_anatomy
    from cultivation.substrate.graph import GraphCollective
    from cultivation.validation.stats import spearman_ties
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
        # the deterministic deposit fingerprint (no wall-clock fields
        # anywhere in the sections)
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the READ-ONLY reference deposits (H4: sha-recorded before any
    #      work in every process; re-checked byte-unchanged at merge) ----
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

    # ---- the read stack, asserted before any decode (exp226 verbatim) --
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    seeds = list(SEEDS)   # exp199's (1, 2, 3) — the battery's seeds

    # ---- exp208's classification + decomposition VERBATIM (carried by
    #      exp226/exp258/exp261; the row classes, precedence intact) -----
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

    # =====================================================================
    # THE INSTRUMENT (lives ENTIRELY here; collective.py untouched —
    # sha-recorded). THE FIELD (disclosed, outcome-blind — fixed BEFORE
    # any run was executed, from the docstring's own words + the stack's
    # own coupling form):
    #   S_i(t) = sum over the cell's junction neighbors j of
    #            (V_j(t) - V_i(t)),
    #   S_i    = S_i(t) accumulated (summed) over EVERY step of the
    #            settle — the clamped encode window, the walk's
    #            STEPS_PER_CELL interludes, and the final 15.0 settle.
    # THE SIGN RESOLUTION: the docstring names "the same electrochemical
    # face the GJ network carries, read through the transporter's sign
    # convention". collective.py's step() carries INTO cell i exactly
    # the inward-directed difference sum_j G_ij (V_j - V_i) (its
    # coupling term); the transporter's sign convention (SERT-like
    # uptake) is inward-positive current. The pre-named field is
    # therefore the UNWEIGHTED inward sum sum_j (V_j - V_i) over the
    # cell's junction neighbors (the docstring's "sum of the cell's
    # V-differences to its junction neighbors", unweighted — the task
    # names the V-difference face, not a conductance face). Fixed before
    # the H2 readout ran; no gate depends on a post-hoc choice.
    # THE JUNCTION-NEIGHBOR SET: exp208's pair support |Wbase| > 0 read
    # as the undirected closure (the exp258 instrument's own
    # neighborhood definition).
    # THE ACCUMULATION IS TELEMETRY ONLY: it writes no state, draws
    # NOTHING from c.rng, and is interleaved with c.step() calls by
    # unrolling collective.py's run(duration, dt) — which with
    # record_every=0 is EXACTLY int(round(duration/dt)) step() calls —
    # so the instrumented dynamics are bit-identical to the production
    # executor's (H1 asserts it per row).
    # =====================================================================
    def _make_sht_executor(medium, g_sht: float, sbar: float,
                           sbarscale: float, telemetry: dict):
        Wbase = np.asarray(medium.Wbase)
        pair_support = (np.abs(Wbase) > 0)
        pair_support = pair_support | pair_support.T   # undirected closure
        PS = pair_support.astype(float)
        deg_pair = PS.sum(axis=1)

        def _flux(V: np.ndarray) -> np.ndarray:
            # S_i(t) = sum_j (V_j - V_i) over the junction neighbors
            return PS @ V - deg_pair * V

        def _run_acc(c, duration: float, dt: float,
                     S_acc: np.ndarray) -> None:
            # collective.py run(duration, dt, record_every=0) unrolled
            # bit-identically, with the read-only flux accumulation
            # interleaved (telemetry only)
            for _ in range(int(round(duration / dt))):
                c.step(dt)
                S_acc += _flux(c.V)

        def _execute_signed_sht(spec, adjacency, seed, op,
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
            S_acc = np.zeros(n)
            _run_acc(c, M142.WINDOW_H, dt, S_acc)
            c.release_clamps()
            reg_idx: list[int] = []
            for z in spec.zones:
                i0 = int(round(z.f0 * n))
                i1 = max(int(round(z.f1 * n)), i0 + 1)
                reg_idx.extend(range(i0, i1))
            reg_idx = sorted(set(reg_idx))
            n_sht_writes = 0
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
                for i, src in order:
                    for _ in range(M142.STEPS_PER_CELL):
                        c.step(dt)
                        S_acc += _flux(c.V)
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
                    # ---- THE exp263 ACTIVATION (the ONLY deviation;
                    #      ZERO at g_sht = 0.0) --------------------------
                    # the transporter's pull: the cell's theta
                    # restoration pull (the commit displacement
                    # theta_new - theta_before) multiplied by
                    # (1 + g_sht * (S_i - Sbar)/Sbar_scale); S_i is the
                    # RUNNING accumulated flux face at the commit (the
                    # accumulation "over the settle" read live, the
                    # causal face — the same live-read form exp261 used
                    # for P_i); Sbar/Sbar_scale are the battery-wide
                    # mean S / mean |S| over the settled g_sht=0 c6
                    # battery rows (the h1 checkpoint's own verified
                    # fields — two scalars, zero re-fit). The sht
                    # channel (ch5) is WRITTEN with the cell's running
                    # S_i at the same commit via the public accessors
                    # (c.read_channel("sht") / c.set_channel("sht",
                    # ...)) — the activation's channel-write face. The
                    # rng stream is untouched (the gain multiplies the
                    # displacement AFTER theta_new is drawn — identical
                    # draws across the whole grid); the effective
                    # target is written to BOTH channels exactly as the
                    # verbatim commit writes theta_new to both.
                    if g_sht > 0.0:
                        theta_before = float(c.theta[i])
                        s_i = float(S_acc[i])
                        sht_vec = c.read_channel("sht")
                        sht_vec[i] = s_i
                        c.set_channel("sht", sht_vec)
                        gain = 1.0 + g_sht * (s_i - sbar) / sbarscale
                        effective = (theta_before
                                     + gain * (theta_new - theta_before))
                        c.theta[i] = effective
                        c.V[i] = effective
                        n_sht_writes += 1
                    else:
                        c.theta[i] = theta_new
                        c.V[i] = theta_new
            _run_acc(c, 15.0, dt, S_acc)
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
            telemetry["n_sht_writes"] = n_sht_writes
            telemetry["sht_last_max"] = float(
                np.abs(c.read_channel("sht")).max())
            telemetry["S_final"] = S_acc.copy()
            # H2's read-only telemetry capture: the settled theta
            # (S[:, 1]) — a COPY; it does not enter the dynamics
            telemetry["theta_final"] = c.theta.tolist()
            return out

        return _execute_signed_sht

    @contextmanager
    def _sht_route(medium, g_sht: float, sbar: float, sbarscale: float,
                   telemetry: dict):
        """Route exp148's executor resolution (read_temporal's global
        name) to the sht instrument for ONE decode; the production
        attribute is restored and asserted. collective.py and every
        experiment module on disk are untouched."""
        saved = M148.execute_signed
        M148.execute_signed = _make_sht_executor(medium, g_sht, sbar,
                                                 sbarscale, telemetry)
        try:
            yield
        finally:
            M148.execute_signed = saved
            assert M148.execute_signed is saved, \
                "executor route not restored"
            assert M148.execute_signed is _PROD_EXECUTOR, \
                "production executor binding drifted"

    def run_instrumented(med, s: int, fmax: float, g_sht: float,
                         sbar: float, sbarscale: float,
                         telemetry: dict) -> dict:
        with _sht_route(med, g_sht, sbar, sbarscale, telemetry):
            return M148.decode("scoped", med, s, return_state=True,
                               f_max=fmax)

    # ---- the row builder (exp226's battery construction verbatim: the
    #      c6 cell's 25 instances via exp199's gen-seed records, seeds
    #      (1,2,3), the production scoped read — the exp258/exp261
    #      battery verbatim, as the docstring names) ----------------------
    def build_rows(g_sht: float, sbar, sbarscale, with_production: bool,
                   h2_readout: bool) -> dict:
        rows: list = []
        n_rej = 0
        rejections: list = []
        pooled_S: list = [] if h2_readout else None
        pooled_mism: list = [] if h2_readout else None
        pooled_bnd: list = [] if h2_readout else None
        seed_S: dict = {s: [] for s in seeds} if h2_readout else None
        seed_mism: dict = {s: [] for s in seeds} if h2_readout else None
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
                tel: dict = {"n_sht_writes": 0, "sht_last_max": None,
                             "S_final": None, "theta_final": None}
                out = run_instrumented(med, s, fmax, g_sht, sbar,
                                       sbarscale, tel)
                if not out["ok"]:
                    n_rej += 1
                    rejections.append({"j": j, "s": s,
                                       "route": f"g{g_sht}",
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
                       "n_sht_writes": int(tel["n_sht_writes"]),
                       "sht_last_max": tel["sht_last_max"],
                       "n_bnd": int(bnd.sum()),
                       "n_int": int(interior.sum()),
                       "bnd_max": float(dev[bnd].max()) if bnd.any() else None,
                       "int_max": (float(dev[interior].max())
                                   if interior.any() else None),
                       "nonbnd_max": float(dev[~bnd].max()),
                       "nonbnd_mean": float(dev[~bnd].mean()),
                       "bnd_errs": dev[bnd].tolist()}
                # H2's readout fields (the g_sht = 0 rows only): the
                # settled accumulated-flux field S_i vs the |V - theta|
                # mismatch (theta from the read-only telemetry capture)
                if h2_readout:
                    theta = np.asarray(tel["theta_final"], dtype=float)
                    assert theta is not None and theta.shape == V.shape
                    mism = np.abs(V - theta)
                    S_row = np.asarray(tel["S_final"], dtype=float)
                    assert S_row is not None and S_row.shape == V.shape
                    assert np.all(np.isfinite(S_row))
                    row["h2"] = {
                        "rho_row": float(spearman_ties(S_row, mism)),
                        "mean_S": float(S_row.mean()),
                        "mean_abs_S": float(np.abs(S_row).mean()),
                        "mism_max": float(mism.max()),
                        "mism_mean": float(mism.mean())}
                    row["S_sha256"] = hashlib.sha256(
                        S_row.tobytes()).hexdigest()
                    pooled_S.append(S_row)
                    pooled_mism.append(mism)
                    pooled_bnd.append(bnd)
                    seed_S[s].append(S_row)
                    seed_mism[s].append(mism)
                # the replay anchors (exp258's X1 verbatim): the
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
                    # H1's identity: the dormant default (g_sht = 0) vs
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
            print(f"  [c6 j{j:2d}] done (g_sht={g_sht})")
        readout = None
        sbar_out = None
        sbarscale_out = None
        if h2_readout:
            S_all = np.concatenate(pooled_S)
            M_all = np.concatenate(pooled_mism)
            B_all = np.concatenate(pooled_bnd)
            rho = float(spearman_ties(S_all, M_all))
            assert np.isfinite(rho), "pooled Spearman not finite"
            sbar_out = float(S_all.mean())
            sbarscale_out = float(np.abs(S_all).mean())
            assert sbarscale_out > 0.0, \
                "degenerate Sbar_scale (the battery-wide mean |S|)"
            per_seed_rho = {}
            for s in seeds:
                Ss = np.concatenate(seed_S[s])
                Ms = np.concatenate(seed_mism[s])
                per_seed_rho[str(s)] = float(spearman_ties(Ss, Ms))
            per_row_rho = [float(r["h2"]["rho_row"]) for r in rows
                           if not r.get("rejected")]
            readout = {
                "statistic": (
                    "Spearman(S_i, |V_i - theta_i|) pooled over EVERY "
                    "cell of EVERY verified g_sht=0 battery row (the "
                    "settled c6 battery states, 25 instances x 3 "
                    "seeds x 400 cells); per-row and per-seed rho "
                    "deposited as audit"),
                "S_field": (
                    "S_i = sum over the cell's junction neighbors j of "
                    "(V_j - V_i), accumulated (summed) over EVERY step "
                    "of the settle — the pre-named electrochemical flux "
                    "face (the SIGN RESOLUTION, disclosed, fixed before "
                    "the readout ran: the GJ network's own coupling "
                    "term carries the inward-directed difference into "
                    "the cell and the transporter's sign convention is "
                    "inward-positive uptake; junction neighbors = "
                    "exp208's pair support |Wbase| > 0, undirected "
                    "closure, the exp258 instrument's neighborhood)"),
                "mismatch": (
                    "|V_i - theta_i| at the settled state; theta is "
                    "the instrumented executor's read-only telemetry "
                    "capture of S[:, 1] (a copy; it does not enter "
                    "the dynamics); the row's V/T are bit-exact vs "
                    "the production decode per the identity check"),
                "n_rows": int(sum(1 for r in rows
                                  if not r.get("rejected"))),
                "n_points": int(S_all.size),
                "rho_pooled": rho,
                "rho_bar": 0.5,
                "rho_pass": bool(rho >= 0.5),
                "sbar": sbar_out,
                "sbar_definition": (
                    "the battery-wide mean accumulated S over the same "
                    "settled g_sht=0 states (S_all.mean(); one scalar, "
                    "zero re-fit; the H3 gain's centering)"),
                "sbarscale": sbarscale_out,
                "sbarscale_definition": (
                    "the battery-wide mean |S| over the same settled "
                    "g_sht=0 states (the docstring's zero-knob "
                    "normalizer)"),
                "pooled_S_sha256": hashlib.sha256(
                    S_all.tobytes()).hexdigest(),
                "pooled_mismatch_sha256": hashlib.sha256(
                    M_all.tobytes()).hexdigest(),
                "per_seed_rho": per_seed_rho,
                "per_row_rho": per_row_rho,
                "per_row": [{"j": r["j"], "s": r["s"],
                             "rho_row": r["h2"]["rho_row"],
                             "mean_S": r["h2"]["mean_S"],
                             "mean_abs_S": r["h2"]["mean_abs_S"],
                             "S_sha256": r["S_sha256"]}
                            for r in rows if not r.get("rejected")],
            }
        return {"rows": rows, "n_rejections": n_rej,
                "rejections": rejections,
                "h2_readout": readout, "sbar": sbar_out,
                "sbarscale": sbarscale_out}

    def worst_over(rows, key_fn, pick):
        vals = [key_fn(r) for r in rows
                if not r.get("rejected") and key_fn(r) is not None]
        return (max(vals) if vals else None,
                sum(1 for r in rows if not r.get("rejected")))

    # ---- the segments -----------------------------------------------------
    G_SHT = {"g025": 0.25, "g050": 0.5, "g100": 1.0}

    def _seg_h1() -> dict:
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(0.0, None, None, with_production=True,
                               h2_readout=True)
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
        h1_pass = bool(all(checks) and len(checks) == PER_CELL * len(SEEDS)
                       and built["n_rejections"] == 0 and n_ok
                       == PER_CELL * len(SEEDS))
        wb, _ = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, \
            "read-only deposit changed (h1)"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            "collective.py changed (h1)"
        return {"g_sht": 0.0, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_checks_pass": sum(1 for c in checks if c),
                "n_checks": len(checks),
                "h1_pass": h1_pass,
                "h1_disclosure": (
                    "g_sht = 0 vs the production scoped decode: V/T "
                    "states bit-exact, errs + verified equal, "
                    "exp199's deposit replayed at its 2-dp rounding, "
                    "exp208's decomposition rows reproduced bit-exactly "
                    "(exp258's X1 form verbatim) — the dormant identity "
                    "is H3's own migration-gate face, it ran FIRST, and "
                    "the H2 readout was taken on those verified states"),
                "h2_readout": built["h2_readout"],
                "sbar": built["sbar"],
                "sbarscale": built["sbarscale"],
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": h1_pass}

    def _seg_grid(seg: str, sbar: float, sbarscale: float) -> dict:
        g_sht = G_SHT[seg]
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(g_sht, sbar, sbarscale,
                               with_production=False, h2_readout=False)
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
        return {"g_sht": g_sht, "sbar_used": sbar,
                "sbarscale_used": sbarscale, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_sht_writes_total": sum(r["n_sht_writes"]
                                          for r in rows
                                          if not r.get("rejected")),
                "sht_last_max_over_rows": max(
                    (r["sht_last_max"] for r in rows
                     if not r.get("rejected")), default=None),
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": bool(built["n_rejections"] == 0
                             and n_ok == PER_CELL * len(SEEDS))}

    def _h2_gate(path: str) -> dict:
        with open(path) as f:
            sec = json.load(f)["section"]
        assert sec["g_sht"] == 0.0 and sec["h1_pass"], \
            "the H2 gate needs the verified h1 checkpoint"
        ro = sec["h2_readout"]
        h2_pass = bool(ro["rho_pass"])
        return {"seg": "h2-gate",
                "h2_pass": h2_pass,
                "rho_pooled": ro["rho_pooled"],
                "rho_bar": ro["rho_bar"],
                "rho_pass": ro["rho_pass"],
                "sbar": sec["sbar"],
                "sbarscale": sec["sbarscale"],
                "source": os.path.abspath(path),
                "note": ("the H2 decision that conditions the grid "
                         "dispatch (the docstring: H3 runs ONLY if H2 "
                         "passes); the merge re-derives the SAME "
                         "decision from the h1 section and asserts "
                         "equality — the deposit's H2 gate record is "
                         "the merge's evaluation, exactly once")}

    # ---- the merge (the gates, each evaluated exactly once) --------------
    def _merge(paths_a: list, paths_b) -> dict:
        # the exp169-import restore applied BEFORE the record is built
        # (exp258's disclosed repair, standing practice here): the
        # merge process's own import chain leaves the -35.0 instrument
        # floor; the production -60.0 floor is restored here so the
        # deposit's merge-side floor_at_exit carries the floor the
        # discipline names (the segment sections restored -60.0
        # themselves)
        CORE.NEURAL_SPEC_MIN = -60.0
        sections: dict = {}
        for p in paths_a:
            with open(p) as f:
                d = json.load(f)
            assert d["seg"] not in sections, "duplicate segment"
            sections[d["seg"]] = d["section"]
        h1 = sections["h1"]
        grid_secs = {k: sections[k] for k in ("g025", "g050", "g100")
                     if k in sections}

        # the file-integrity gate: the pre-registered header (docstring,
        # imports, constants — 437ee24's bytes through the OUT line)
        raw_self = open(os.path.abspath(__file__), "rb").read()
        mk = raw_self.find(_HEADER_MARKER.encode())
        assert mk != -1, "header marker not found"
        header_sha = hashlib.sha256(
            raw_self[:mk + len(_HEADER_MARKER)]).hexdigest()
        header_unchanged = bool(header_sha == EXPECTED_HEADER_SHA256)
        assert header_unchanged, (
            f"the pre-registered header drifted: {header_sha}")

        # ---- H1 (the dormant identity, the migration gate; ran FIRST,
        #      fail = STOP) ------------------------------------------------
        h1_ok = bool(h1["h1_pass"])
        assert h1_ok, "H1 (the dormant identity) FAILED — the " \
            "experiment stops before any gate evaluation"

        # ---- row-set integrity across sections (T and Wbase are
        #      g-independent, so the row sets must match 1:1) -----------
        base_rowmap = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                       for r in h1["rows"] if not r.get("rejected")}
        for k, sec in grid_secs.items():
            m = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                 for r in sec["rows"] if not r.get("rejected")}
            assert m == base_rowmap, f"row set drifted ({k})"

        # ---- H2 (the readout; the gate, evaluated exactly once, HERE) ----
        ro = h1["h2_readout"]
        h2_pass = bool(ro["rho_pass"])

        # ---- H3 (the write coupling; ONLY if H2 passes) -------------------
        base_bnd = h1["worst_bnd_err_mV"]
        base_wn = h1["worst_nonbnd_err_mV"]
        assert base_bnd is not None and base_bnd > 0.0, \
            "degenerate baseline worst boundary-row err"
        h3_record: dict = {"status": None, "pass": None}
        h3_reduction = None
        nonbnd_change = None
        g_star = None
        cells: dict = {}
        if not h2_pass:
            h3_record = {
                "status": "SKIPPED-H2-FAIL", "pass": None,
                "clause": ("the transporter's pull at the pre-named "
                           "grid {0.25, 0.5, 1.0} — NOT RUN: the "
                           "docstring gates H3 on H2 (H2 REFUTE -> H3 "
                           "skipped and recorded SKIPPED-H2-FAIL); no "
                           "g_sht > 0 decode was executed anywhere in "
                           "this experiment"),
                "identity_at_g0": h1_ok,
                "n_identity_checks": h1["n_checks"],
                "n_identity_checks_pass": h1["n_checks_pass"]}
        else:
            reds = {}
            for k, sec in sorted(grid_secs.items()):
                gv = float(sec["g_sht"])
                wb = sec["worst_bnd_err_mV"]
                wn = sec["worst_nonbnd_err_mV"]
                red = float((base_bnd - wb) / base_bnd)
                reds[gv] = red
                cells[str(gv)] = {
                    "worst_bnd_err_mV": wb,
                    "worst_int_err_mV": sec["worst_int_err_mV"],
                    "worst_nonbnd_err_mV": wn,
                    "reduction_vs_dormant": red,
                    "nonbnd_change_vs_dormant":
                        float((wn - base_wn) / base_wn),
                    "n_sht_writes_total": sec["n_sht_writes_total"],
                    "sht_last_max_over_rows":
                        sec["sht_last_max_over_rows"],
                    "n_rows": sec["n_rows"], "n_ok": sec["n_ok"]}
            assert len(reds) == 3, "the pre-named grid is incomplete"
            g_star = max(reds, key=lambda k: reds[k])
            h3_reduction = reds[g_star]
            nonbnd_change = cells[str(g_star)]["nonbnd_change_vs_dormant"]
            h3_pass = bool(h1_ok and h3_reduction >= 0.10
                           and nonbnd_change <= 0.05)
            h3_record = {
                "status": "PASS" if h3_pass else "REFUTE",
                "pass": h3_pass,
                "clause": ("the best grid cell reduces the worst "
                           "boundary-row err >= 10% AND the "
                           "non-boundary rows' worst-err change "
                           "<= +5% at that cell (the exp258/exp259/"
                           "exp261 forms verbatim; the gate reads the "
                           "best cell, zero post-hoc selection; all "
                           "three nonzero g values reported; g_sht = 0 "
                           "is the dormant identity — bit-exact per "
                           "H1)"),
                "identity_at_g0": h1_ok,
                "n_identity_checks": h1["n_checks"],
                "n_identity_checks_pass": h1["n_checks_pass"],
                "g_star": float(g_star),
                "reduction_at_best_cell": h3_reduction,
                "nonbnd_change_at_best_cell": nonbnd_change,
                "baseline": {"worst_bnd_err_mV": base_bnd,
                             "worst_nonbnd_err_mV": base_wn,
                             "source": ("h1's g_sht=0 rows (bit-exact "
                                        "vs production per H1)")},
                "all_cells": cells}

        # ---- H4 (the discipline) -----------------------------------------
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
        h4_pass = bool(deposits_unchanged and coll_unchanged
                       and floor_ok and n_rej_total == 0
                       and det["pass_b_byte_identical"]
                       and header_unchanged)

        # ---- branch + verdict --------------------------------------------
        evaluated = [h1_ok, h2_pass, h4_pass]
        if h3_record["pass"] is not None:
            evaluated.append(h3_record["pass"])
        n_pass = sum(1 for v in evaluated if v)
        if not h2_pass:
            branch = "SHT-INERT"
        elif h3_record["pass"]:
            branch = "SHT-CARRIES"
        else:
            branch = "SHT-READOUT-ONLY"
        h3_txt = h3_record["status"]
        h3_detail = ""
        if h3_reduction is not None:
            h3_detail = (f" (reduction {h3_reduction:+.4f} at "
                         f"g_sht={g_star}; non-boundary change "
                         f"{nonbnd_change:+.4f})")
        verdict = (
            f"{n_pass}/{len(evaluated)} evaluated gates | "
            f"H1 {'PASS' if h1_ok else 'FAIL'} "
            f"(dormant identity 75/75 bit-exact, ran FIRST) | "
            f"H2 {'PASS' if h2_pass else 'REFUTE'} "
            f"(pooled rho {ro['rho_pooled']:.4f} vs bar "
            f"{ro['rho_bar']}, n={ro['n_points']} points) | "
            f"H3 {h3_txt}{h3_detail} | "
            f"H4 {'PASS' if h4_pass else 'FAIL'} | {branch}")

        deposit = {
            "exp": "exp263",
            "claim": (
                "THE SHT CHANNEL ACTIVATION (the FOURTH channel "
                "activation under the exp257 schema): ch5 sht — the "
                "paper's 5-HT electrophoresis face, stack-native (BETSE "
                "carries no serotonin machinery; the grounding is the "
                "paper's OWN spec face: 5-HT transport is a "
                "charge-coupled flux following the electrochemical "
                "gradient the stack already computes). The pre-named "
                "instrument: the accumulated flux field S_i = the "
                "per-cell sum of V-differences to junction neighbors, "
                "accumulated over the settle. H1 the dormant identity "
                "(75/75 bit-exact, ran FIRST, fail = STOP); H2 the "
                "readout (Spearman(S_i, |V_i - theta_i|) >= 0.5 "
                "pooled); H3 (ONLY if H2 passes) the transporter's "
                "pull — the theta restoration pull multiplied by "
                "(1 + g_sht * (S_i - Sbar)/Sbar_scale) at the "
                "pre-named grid {0, 0.25, 0.5, 1.0}, best cell >= 10% "
                "boundary reduction AND <= +5% non-boundary change "
                "(H2 PASS + H3 PASS -> SHT-CARRIES / H3 REFUTE -> "
                "SHT-READOUT-ONLY / H2 REFUTE -> SHT-INERT)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any body "
                    "(pre-registration 437ee24, batch 24; gates H1-H4 "
                    "fixed there, each evaluated exactly once); the "
                    "pre-registered header (docstring + imports + "
                    "constants) sha256-verified byte-unchanged at "
                    "merge: " + EXPECTED_HEADER_SHA256),
                "docstring_sha256": DOCSTRING_SHA256,
                "mechanism": (
                    "the transporter's pull: at EVERY commit of the "
                    "regenerated region's walk (exp142's "
                    "execute_signed commit loop, routed through the "
                    "experiment's own instrument — collective.py "
                    "untouched), the cell's theta restoration pull "
                    "(the commit displacement theta_new - "
                    "theta_before) is multiplied by (1 + g_sht * "
                    "(S_i - Sbar)/Sbar_scale); S_i is the RUNNING "
                    "accumulated flux face at the commit (the "
                    "accumulation-over-the-settle read live, the "
                    "causal face — the same live-read form exp261 "
                    "used for P_i; DISCLOSED READING, outcome-blind, "
                    "fixed before any g_sht > 0 run: the docstring's "
                    "coupling formula names S_i without a time index "
                    "and the settle is still running at commit time, "
                    "so the only S_i that exists at the commit is the "
                    "accumulation so far); Sbar = the battery-wide "
                    "mean S and Sbar_scale = the battery-wide mean "
                    "|S| over the settled g_sht=0 c6 battery rows "
                    "(the h1 checkpoint's own verified fields; two "
                    "scalars, zero re-fit); the sht channel (ch5) is "
                    "WRITTEN with the cell's running S_i at the same "
                    "commit via the public accessors "
                    "(c.read_channel('sht') / c.set_channel('sht', "
                    "...)) — the activation's channel-write face; the "
                    "FIELD (disclosed, outcome-blind, fixed before "
                    "the H2 readout ran): S_i(t) = sum over the "
                    "cell's junction neighbors j of (V_j(t) - V_i(t)) "
                    "— the SAME inward-directed V-difference "
                    "collective.py's own coupling term carries into "
                    "the cell (coupling = G @ V - V * deg), read "
                    "through the transporter's sign convention "
                    "(SERT-like uptake = inward-positive); "
                    "UNWEIGHTED per the docstring's 'sum of the "
                    "cell's V-differences to its junction "
                    "neighbors'; junction neighbors = exp208's pair "
                    "support |Wbase| > 0, undirected closure (the "
                    "exp258 instrument's neighborhood); the "
                    "accumulation spans EVERY step of the settle "
                    "(clamped encode window + the walk's "
                    "STEPS_PER_CELL interludes + the final 15.0) and "
                    "is TELEMETRY ONLY (no state write, no rng draw); "
                    "it is interleaved by unrolling collective.py's "
                    "run(duration, dt) — which with record_every=0 "
                    "is EXACTLY int(round(duration/dt)) step() calls "
                    "— so the instrumented dynamics are bit-identical "
                    "to the production executor's (H1 asserts it per "
                    "row); the rng stream is untouched (the gain "
                    "multiplies the displacement AFTER theta_new is "
                    "drawn — identical draws across the whole grid); "
                    "the effective commit is written to BOTH channels "
                    "exactly as the verbatim commit writes theta_new "
                    "to both; g_sht = 0.0 takes the verbatim path "
                    "with ZERO deviation (no sht write, no gain) — "
                    "the bit-exact dormant default, the migration "
                    "gate's own face; the settled theta for H2's "
                    "mismatch is the instrumented executor's "
                    "read-only telemetry capture of S[:, 1] (a copy; "
                    "it does not enter the dynamics)"),
                "row_conventions": (
                    "a ROW = one per-cell err |V_i - T_i| (mV) at a "
                    "cell of the exp226/exp229 canon-boundary row "
                    "class (exp208's classify, precedence intact), "
                    "pooled over exp226's c6 battery (25 instances x "
                    "3 seeds); 'worst boundary-row err' = the max "
                    "over that pooled row set; 'non-boundary rows' = "
                    "the complement under the same convention"),
                "conventions": (
                    "the executor instrument is exp142's "
                    "execute_signed copied line-for-line into this "
                    "module with the ONE activation block; bit-exact "
                    "identity at g_sht = 0 is asserted per row against "
                    "the production decode AND exp199's deposit AND "
                    "exp208's decomposition rows (exp226's R1 "
                    "machinery verbatim); T and Wbase are "
                    "g-independent so the row sets match 1:1 across "
                    "the grid (asserted at merge); the H2-gated "
                    "dispatch: the grid segments were launched only "
                    "after --h2-gate read H2 PASS from the h1 "
                    "checkpoint section file")},
            "sections": {k: sections[k] for k in sorted(sections)},
            "readout": ro,
            "grid": {"g_values": [0.0, 0.25, 0.5, 1.0],
                     "g_star": (float(g_star)
                                if g_star is not None else None),
                     "h3_status": h3_record["status"],
                     "cells": cells},
            "gates": {
                "H1": {"pass": h1_ok, "migration_gate": True,
                       "ran_first": True, "fail_stop": True,
                       "n_rows": h1["n_rows"], "n_ok": h1["n_ok"],
                       "n_checks_pass": h1["n_checks_pass"],
                       "n_checks": h1["n_checks"],
                       "clause": ("g_sht = 0 reproduces the production "
                                  "decode bit-exactly on the c6 "
                                  "battery, 75/75 rows (the exp258 X1 "
                                  "form verbatim)"),
                       "disclosure": (
                           "g_sht = 0 vs the production scoped decode: "
                           "V/T states bit-exact, errs + verified "
                           "equal, exp199's deposit replayed at its "
                           "2-dp rounding, exp208's decomposition rows "
                           "reproduced bit-exactly (exp226's R1 "
                           "verbatim)")},
                "H2": {"pass": h2_pass,
                       "clause": ("Spearman(S_i, |V_i - theta_i|) "
                                  ">= 0.5 over the pooled battery "
                                  "points, on the settled c6 battery "
                                  "states (zero-risk: read-only)"),
                       "rho_pooled": ro["rho_pooled"],
                       "rho_bar": ro["rho_bar"],
                       "rho_pass": ro["rho_pass"],
                       "n_points": ro["n_points"],
                       "sbar": ro["sbar"],
                       "sbarscale": ro["sbarscale"],
                       "per_seed_rho": ro["per_seed_rho"],
                       "per_row_rho": ro["per_row_rho"]},
                "H3": h3_record,
                "H4": {"pass": h4_pass,
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
                       "header_unchanged": header_unchanged,
                       "docstring_sha_at_exit": _docstring_sha()}},
            "branch": branch,
            "verdict": verdict,
            "notes": [
                "body written by the run agent under the body-only "
                "discipline; the pre-registered header (docstring, "
                "imports, constants) byte-unchanged, verified against "
                "437ee24 by sha256 at merge; the docstring sha is "
                "asserted BEFORE any work and AGAIN after the deposit "
                "is written, in every process",
                "the SIGN RESOLUTION of the pre-named field is "
                "disclosed in pre_registered.mechanism and was fixed "
                "outcome-blind BEFORE the H2 readout ran: the "
                "inward-directed sum sum_j (V_j - V_i) — the GJ "
                "network's own coupling face (collective.py: coupling "
                "= G @ V - V * deg) read through the transporter's "
                "inward-positive uptake convention; no gate depends "
                "on a post-hoc choice",
                "the H2-gated dispatch (the docstring: H3 runs ONLY "
                "if H2 passes): the h1 segment is the checkpoint; "
                "--h2-gate read the H2 decision from it BEFORE any "
                "g_sht > 0 segment was launched (the grid segments "
                "themselves assert the checkpoint's H2 PASS via "
                "--sbar-from before running); on an H2 REFUTE this "
                "merge records H3 as SKIPPED-H2-FAIL and no g_sht > 0 "
                "decode exists anywhere in the experiment",
                "the accumulation's run() unroll is bit-exact by "
                "construction (collective.py's run with "
                "record_every=0 is exactly int(round(duration/dt)) "
                "step() calls) and H1 asserts the resulting states "
                "per row against the production decode; the battery "
                "bring-up ran inside the h1 segment itself — any "
                "instrument defect would have failed H1 there and "
                "stopped the experiment before the gates; every gate "
                "was evaluated exactly once, at the merge",
                "the activation instrument routes exp148's executor "
                "name to the experiment's own verbatim copy of "
                "exp142's execute_signed for the instrumented decodes "
                "only; the production binding is restored and "
                "asserted around every decode; no file on disk "
                "modified but this module",
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
    elif args.h2_gate is not None:
        result = _h2_gate(args.h2_gate)
    elif args.seg == "h1":
        result = {"seg": "h1", "section": _seg_h1()}
    elif args.seg in G_SHT:
        assert args.sbar_from is not None, \
            "grid segments need --sbar-from (the h1 checkpoint)"
        with open(args.sbar_from) as f:
            _h1sec = json.load(f)["section"]
        assert _h1sec["g_sht"] == 0.0 and _h1sec["h1_pass"], \
            "the h1 checkpoint is not a verified dormant battery"
        assert _h1sec["h2_readout"]["rho_pass"], \
            "H2 did not pass on the checkpoint — H3 must not run"
        result = {"seg": args.seg,
                  "section": _seg_grid(args.seg,
                                       float(_h1sec["sbar"]),
                                       float(_h1sec["sbarscale"]))}
    else:
        raise SystemExit("use --seg {h1,g025,g050,g100} / --h2-gate / "
                         "--merge (runner split is canonical)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, default=str)
    if args.merge:
        print(f"=== exp263 MERGE: branch {result['branch']} ===")
        for k, v in result["gates"].items():
            _st = ("SKIPPED" if v.get("status") == "SKIPPED-H2-FAIL"
                   else ("PASS" if v["pass"] else "REFUTE/FAIL"))
            print(f"  {k}: {_st}")
        print(f"  {result['verdict']}")
    else:
        print(f"=== exp263 seg {result['seg']} written ===")
    # the production floor at exit, asserted (the exp169-import
    # restore convention) — and the docstring gate AGAIN (after the
    # deposit is written; the hard rule's before-and-after assert)
    CORE.NEURAL_SPEC_MIN = -60.0
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == -60.0, \
        "production floor not restored at exit"
    assert _docstring_sha() == DOCSTRING_SHA256, \
        "the pre-registered docstring drifted (post-write assert)"
    return result


if __name__ == "__main__":
    main()
