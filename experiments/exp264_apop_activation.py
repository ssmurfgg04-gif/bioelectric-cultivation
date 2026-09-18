#!/usr/bin/env python3
"""exp264 — THE APOP CHANNEL ACTIVATION (batch 24 item 3; L239's
registered next (c) — the FIFTH activation under the exp257 schema,
ch6 "apop", the paper's apoptosis-as-morphogenetic-signal face).

THE OPEN ITEM: the paper's census names apoptosis as a morphogenetic
signal — ABSENT from the stack; the exp257 schema gave it native
state (ch6, dormant). The stack-native pre-named instrument: the
apop channel MARKS the cells at the extreme band of the theta
distribution (the death-competent state: sustained extreme
depolarization or the wound's blastema state — the pre-named rule:
a cell is marked iff its theta sits in the battery-wide extreme
decile at settle time [both tails, the zero-knob quantile rule] OR
the cell sits in the amputation's blastema band); the mark is
state (carried in ch6), the readout tests whether the marked set
localizes the boundary excess, the coupling (gated on the readout)
lets the mark modulate the cell's identity commitment noise (the
M26b face: the death signal's morphogenetic role is to RELAX the
marked cell's commitment toward the local mean — the pre-named
form: the marked cells' commitment noise multiplied by
(1 - g_apop) at the grid {0, 0.25, 0.5, 1.0}).

PRE-REGISTERED GATES (the exp258/exp261/exp263 mold):

  A1  THE DORMANT IDENTITY: g_apop = 0 reproduces the production
      decode bit-exactly on the c6 battery (75/75, the X1 form
      verbatim).
  A2  THE READOUT (zero-risk, read-only): the marked set's boundary
      enrichment — the marked cells' CANON-BOUNDARY membership rate
      vs the unmarked cells' (the pre-named enrichment ratio >= 2.0
      gates the coupling; Fisher-type count comparison recorded,
      the ratio is the gate).
  A3  THE COUPLING (only if A2 passes; else SKIPPED-A2-FAIL): the
      marked cells' commitment-noise relaxation at the pre-named
      grid; the gates: the best cell reduces the worst boundary-row
      err >= 10% AND the non-boundary rows' worst-err change <= +5%.
  A4  THE DISCIPLINE: exp226's/exp229's deposits READ-ONLY
      sha-recorded; collective.py untouched sha-recorded; the -60.0
      floor restored and asserted; deterministic re-run; no
      wall-clock fields.

THE BRANCHES (pre-named): APOP-CARRIES / APOP-READOUT-ONLY /
APOP-INERT — deposited honestly.

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
OUT = os.path.join(ROOT, "results", "exp264_apop_activation.json")

# ==== BODY (written by the run agent under the body-only discipline;
# docstring/imports/constants above byte-unchanged — verified against
# 437ee24 by EXPECTED_HEADER_SHA256 at merge; the gates below are the
# docstring's, each evaluated exactly once) =============================
EXPECTED_HEADER_SHA256 = (
    "c8c33afdda8053141411c2e9118e012e69a51d0e604d37ab66e0db1f11695573")
_HEADER_MARKER = (
    'OUT = os.path.join(ROOT, "results", '
    '"exp264_apop_activation.json")\n')
DOCSTRING_SHA256 = (
    "ad58c729ad24c98e19248a2bf81ea67818cf7dfd7bac4a15aab517940950ea15")


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
    # ==== imports (the exp258/exp261/exp263 machinery; the BLAS pins
    #      precede the numpy import — the pre-registered header's
    #      discipline) ================================================
    import argparse
    import hashlib
    import json
    from contextlib import contextmanager

    # the docstring gate, FIRST in every process (segments, gates,
    # merge): fail = STOP before anything runs
    assert _docstring_sha() == DOCSTRING_SHA256, \
        "the pre-registered docstring drifted (pre-work assert)"

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["a1", "g025", "g050", "g100"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--pass-b", nargs="*", default=None)
    ap.add_argument("--a2-gate", default=None, metavar="A1_SEG_JSON")
    ap.add_argument("--marks-from", default=None, metavar="A1_SEG_JSON")
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
        # the deterministic deposit fingerprint (no wall-clock fields
        # anywhere in the sections)
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the READ-ONLY reference deposits (A4: sha-recorded before any
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
    #      exp226/exp258/exp261/exp263; the row classes, precedence
    #      intact) ----------------------------------------------------
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
    # sha-recorded). THE MARK RULE (the docstring's pre-named rule,
    # evaluated ONCE on the verified dormant battery at the a1
    # checkpoint and carried from there — DISCLOSED READING,
    # outcome-blind, fixed before any g_apop > 0 run):
    #   a cell is marked iff its SETTLED theta sits in the BATTERY-WIDE
    #   extreme decile [both tails: theta <= q10 OR theta >= q90 of the
    #   pooled settled-theta distribution over EVERY verified g_apop = 0
    #   battery row — 25 instances x 3 seeds x 400 cells; the zero-knob
    #   quantile rule, numpy's default linear-interpolation quantiles]
    #   OR the cell sits in the amputation's blastema band [the row's
    #   amputated region — exactly the slice the executor's
    #   c.amputate(slice(reg_lo, reg_hi + 1)) receives, the band
    #   collective.py sets to the blastema state (theta = -40.0); the
    #   docstring's "the cell SITS IN the amputation's blastema band"
    #   is positional membership in the amputation's own band, not a
    #   derived frontier-adjacency class].
    # WHY THE MARK IS CARRIED FROM THE CHECKPOINT: the docstring
    # defines the mark "at settle time" — a settled-state property —
    # while the coupling acts at commit time DURING the run; the only
    # consistent reading is the mark fixed on the verified dormant
    # battery (the a1 checkpoint's own settled states, bit-exact vs
    # production per A1) and threaded per row into the instrumented
    # runs (the exp261 Pbar form, generalized to a per-row mask). The
    # mark is g-independent: it derives from T-independent settled
    # states and the g-independent zone geometry, so the SAME mark
    # applies across the whole grid (the executor asserts its own
    # amputation band equals the checkpoint's and is fully contained
    # in the mark).
    # THE COUPLING (the docstring's pre-named form): at the commit of a
    # MARKED cell (g_apop > 0 only), the commitment noise is
    # multiplied by (1 - g_apop): sigma = COMMIT_NOISE * (1 - g_apop)
    # — the M26b face: relaxing the marked cell's commitment noise
    # toward the inherited/canon mean. THE RNG STREAM: the commit draw
    # is restructured to exactly ONE c.rng.normal(0.0, sigma) per
    # commit (numpy's Generator.normal consumes the identical
    # underlying stream for any scale — the stream POSITION is
    # preserved for every cell, marked or not, across the whole grid;
    # at g_apop = 0 the else-branch takes the VERBATIM sigma so the
    # dormant path is bit-exact — A1 asserts it per row). The apop
    # channel (ch6) is WRITTEN with the mark (1.0) at the same commit
    # via the public accessors (c.read_channel("apop") /
    # c.set_channel("apop", ...)) — the activation's channel-write
    # face; the docstring's "the mark is state (carried in ch6)".
    # =====================================================================
    def _make_apop_executor(medium, g_apop: float, mark_mask,
                            band, telemetry: dict):

        def _execute_signed_apop(spec, adjacency, seed, op,
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
            n_apop_marks = 0
            if reg_idx:
                if band is not None:
                    # the row's own amputation band must equal the
                    # checkpoint's (g-independent zone geometry) and
                    # be fully contained in the threaded mark
                    assert [int(reg_idx[0]),
                            int(reg_idx[-1])] == list(band), \
                        "the amputation band drifted vs the a1 checkpoint"
                    assert bool(np.all(
                        mark_mask[band[0]:band[1] + 1])), \
                        "the mark does not cover the amputation band"
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
                    canon_src = getattr(c, "phi_spec_canon", None)
                    # the verbatim commit branch chain (pure reads —
                    # the noise draw is made ONCE below, at the
                    # pre-named sigma)
                    if c.phi_spec[i] >= M142.NEURAL_SPEC_MIN:
                        commit_base = c.phi_spec[i]
                    elif canon_src is not None:
                        commit_base = canon_src[i]
                    else:
                        commit_base = c.theta[src]
                    # ---- THE exp264 ACTIVATION (the ONLY deviation;
                    #      ZERO at g_apop = 0.0) ----------------------
                    if g_apop > 0.0 and bool(mark_mask[i]):
                        sigma = M142.COMMIT_NOISE * (1.0 - g_apop)
                        apop_vec = c.read_channel("apop")
                        apop_vec[i] = 1.0
                        c.set_channel("apop", apop_vec)
                        n_apop_marks += 1
                    else:
                        sigma = M142.COMMIT_NOISE
                    theta_new = commit_base + c.rng.normal(0.0, sigma)
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
            telemetry["n_apop_marks"] = n_apop_marks
            telemetry["apop_last_max"] = float(
                np.abs(c.read_channel("apop")).max())
            telemetry["reg_range"] = (
                [int(reg_idx[0]), int(reg_idx[-1])]
                if reg_idx else None)
            # A2's read-only telemetry capture: the settled theta
            # (S[:, 1]) — a COPY; it does not enter the dynamics
            telemetry["theta_final"] = c.theta.tolist()
            return out

        return _execute_signed_apop

    @contextmanager
    def _apop_route(medium, g_apop: float, mark_mask, band,
                    telemetry: dict):
        """Route exp148's executor resolution (read_temporal's global
        name) to the apop instrument for ONE decode; the production
        attribute is restored and asserted. collective.py and every
        experiment module on disk are untouched."""
        saved = M148.execute_signed
        M148.execute_signed = _make_apop_executor(medium, g_apop,
                                                  mark_mask, band,
                                                  telemetry)
        try:
            yield
        finally:
            M148.execute_signed = saved
            assert M148.execute_signed is saved, \
                "executor route not restored"
            assert M148.execute_signed is _PROD_EXECUTOR, \
                "production executor binding drifted"

    def run_instrumented(med, s: int, fmax: float, g_apop: float,
                         mark_mask, band, telemetry: dict) -> dict:
        with _apop_route(med, g_apop, mark_mask, band, telemetry):
            return M148.decode("scoped", med, s, return_state=True,
                               f_max=fmax)

    # ---- the row builder (exp226's battery construction verbatim: the
    #      c6 cell's 25 instances via exp199's gen-seed records, seeds
    #      (1,2,3), the production scoped read — the exp258/261/263
    #      battery verbatim, as the docstring names) ----------------------
    def build_rows(g_apop: float, marks, with_production: bool,
                   a2_readout: bool) -> dict:
        rows: list = []
        n_rej = 0
        rejections: list = []
        theta_rows: list = [] if a2_readout else None
        bnd_rows: list = [] if a2_readout else None
        band_rows: list = [] if a2_readout else None
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
                if g_apop > 0.0:
                    mrec = marks[f"{j}-{s}"]
                    mark_mask = np.zeros(N400, dtype=bool)
                    mark_mask[np.asarray(mrec["marked"], dtype=int)] = True
                    band = [int(mrec["band"][0]), int(mrec["band"][1])]
                else:
                    mark_mask = np.zeros(N400, dtype=bool)
                    band = None
                tel: dict = {"n_apop_marks": 0, "apop_last_max": None,
                             "theta_final": None, "reg_range": None}
                out = run_instrumented(med, s, fmax, g_apop, mark_mask,
                                       band, tel)
                if not out["ok"]:
                    n_rej += 1
                    rejections.append({"j": j, "s": s,
                                       "route": f"g{g_apop}",
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
                       "n_apop_marks": int(tel["n_apop_marks"]),
                       "apop_last_max": tel["apop_last_max"],
                       "n_bnd": int(bnd.sum()),
                       "n_int": int(interior.sum()),
                       "bnd_max": float(dev[bnd].max()) if bnd.any() else None,
                       "int_max": (float(dev[interior].max())
                                   if interior.any() else None),
                       "nonbnd_max": float(dev[~bnd].max()),
                       "nonbnd_mean": float(dev[~bnd].mean()),
                       "bnd_errs": dev[bnd].tolist()}
                # A2's readout fields (the g_apop = 0 rows only): the
                # settled theta + the row's canon-boundary mask + the
                # row's amputation band (the mark rule is evaluated
                # battery-wide AFTER the loop)
                if a2_readout:
                    theta = np.asarray(tel["theta_final"], dtype=float)
                    assert theta is not None and theta.shape == V.shape
                    assert tel["reg_range"] is not None
                    reg_lo, reg_hi = int(tel["reg_range"][0]), \
                        int(tel["reg_range"][1])
                    assert 0 <= reg_lo <= reg_hi < N400
                    theta_rows.append(theta)
                    bnd_rows.append(bnd)
                    band_rows.append((reg_lo, reg_hi))
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
                    # A1's identity: the dormant default (g_apop = 0) vs
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
            print(f"  [c6 j{j:2d}] done (g_apop={g_apop})")
        readout = None
        marks_out = None
        if a2_readout:
            # ---- THE PRE-NAMED MARK RULE, evaluated ONCE, battery-wide
            #      on the verified dormant battery's settled states ----
            Theta_all = np.concatenate(theta_rows)
            B_all = np.concatenate(bnd_rows)
            q10 = float(np.quantile(Theta_all, 0.10))
            q90 = float(np.quantile(Theta_all, 0.90))
            marks_out = {}
            M_all = np.zeros(Theta_all.size, dtype=bool)
            nr_rows = [r for r in rows if not r.get("rejected")]
            assert len(nr_rows) == len(theta_rows)
            for k, theta in enumerate(theta_rows):
                reg_lo, reg_hi = band_rows[k]
                mark = (theta <= q10) | (theta >= q90)
                mark[reg_lo:reg_hi + 1] = True
                idx = np.flatnonzero(mark)
                row = nr_rows[k]
                marks_out[f"{row['j']}-{row['s']}"] = {
                    "marked": idx.tolist(),
                    "band": [reg_lo, reg_hi],
                    "n_decile": int(((theta <= q10)
                                     | (theta >= q90)).sum()),
                    "n_marked": int(mark.sum())}
                M_all[k * N400:(k + 1) * N400] = mark
            n_marked = int(M_all.sum())
            n_marked_bnd = int((M_all & B_all).sum())
            n_unmarked = int((~M_all).sum())
            n_unmarked_bnd = int((~M_all & B_all).sum())
            rate_marked = n_marked_bnd / n_marked
            rate_unmarked = n_unmarked_bnd / n_unmarked
            ratio = float(rate_marked / rate_unmarked)
            assert np.isfinite(ratio) and ratio > 0.0
            # the Fisher-type count comparison (recorded; the RATIO is
            # the gate) — scipy's deterministic exact test
            from scipy.stats import fisher_exact
            odds, p_fisher = fisher_exact(
                [[n_marked_bnd, n_marked - n_marked_bnd],
                 [n_unmarked_bnd, n_unmarked - n_unmarked_bnd]])
            readout = {
                "statistic": (
                    "the marked set's CANON-BOUNDARY enrichment ratio, "
                    "pooled over EVERY verified g_apop=0 battery row "
                    "(25 instances x 3 seeds x 400 cells): "
                    "(marked & canon-boundary / marked) / (unmarked & "
                    "canon-boundary / unmarked); the boundary classes "
                    "are exp208's classify on the row's target "
                    "(precedence intact)"),
                "mark_rule": (
                    "a cell is marked iff its settled theta sits in "
                    "the battery-wide extreme decile [both tails: "
                    "theta <= q10 OR theta >= q90 of the pooled "
                    "settled-theta distribution; the zero-knob "
                    "quantile rule, numpy default linear "
                    "interpolation] OR the cell sits in the "
                    "amputation's blastema band [the row's amputated "
                    "region — the slice c.amputate receives, the band "
                    "collective.py sets to the blastema state]; "
                    "DISCLOSED READING, outcome-blind, fixed before "
                    "any g_apop > 0 run (see pre_registered."
                    "mechanism)"),
                "n_rows": int(sum(1 for r in rows
                                  if not r.get("rejected"))),
                "n_points": int(Theta_all.size),
                "q10": q10, "q90": q90,
                "n_marked": n_marked,
                "n_marked_bnd": n_marked_bnd,
                "n_unmarked": n_unmarked,
                "n_unmarked_bnd": n_unmarked_bnd,
                "rate_marked_bnd": float(rate_marked),
                "rate_unmarked_bnd": float(rate_unmarked),
                "enrichment_ratio": ratio,
                "ratio_bar": 2.0,
                "ratio_pass": bool(ratio >= 2.0),
                "fisher_2x2": [[n_marked_bnd, n_marked - n_marked_bnd],
                               [n_unmarked_bnd,
                                n_unmarked - n_unmarked_bnd]],
                "fisher_oddsratio": float(odds),
                "fisher_two_sided_p": float(p_fisher),
                "settled_theta_sha256": hashlib.sha256(
                    Theta_all.tobytes()).hexdigest()}
        return {"rows": rows, "n_rejections": n_rej,
                "rejections": rejections,
                "a2_readout": readout, "marks": marks_out}

    def worst_over(rows, key_fn, pick):
        vals = [key_fn(r) for r in rows
                if not r.get("rejected") and key_fn(r) is not None]
        return (max(vals) if vals else None,
                sum(1 for r in rows if not r.get("rejected")))

    # ---- the segments -----------------------------------------------------
    G_APOP = {"g025": 0.25, "g050": 0.5, "g100": 1.0}

    def _seg_a1() -> dict:
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(0.0, None, with_production=True,
                               a2_readout=True)
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
        a1_pass = bool(all(checks) and len(checks) == PER_CELL * len(SEEDS)
                       and built["n_rejections"] == 0 and n_ok
                       == PER_CELL * len(SEEDS))
        wb, _ = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, \
            "read-only deposit changed (a1)"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            "collective.py changed (a1)"
        return {"g_apop": 0.0, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_checks_pass": sum(1 for c in checks if c),
                "n_checks": len(checks),
                "a1_pass": a1_pass,
                "a1_disclosure": (
                    "g_apop = 0 vs the production scoped decode: V/T "
                    "states bit-exact, errs + verified equal, "
                    "exp199's deposit replayed at its 2-dp rounding, "
                    "exp208's decomposition rows reproduced bit-exactly "
                    "(exp258's X1 form verbatim) — the dormant identity "
                    "is A3's own migration-gate face, it ran FIRST, and "
                    "the A2 readout (the mark rule) was evaluated on "
                    "those verified settled states"),
                "a2_readout": built["a2_readout"],
                "marks": built["marks"],
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": a1_pass}

    def _seg_grid(seg: str, marks: dict) -> dict:
        g_apop = G_APOP[seg]
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(g_apop, marks, with_production=False,
                               a2_readout=False)
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
        return {"g_apop": g_apop, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_apop_marks_total": sum(r["n_apop_marks"]
                                          for r in rows
                                          if not r.get("rejected")),
                "apop_last_max_over_rows": max(
                    (r["apop_last_max"] for r in rows
                     if not r.get("rejected")), default=None),
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": bool(built["n_rejections"] == 0
                             and n_ok == PER_CELL * len(SEEDS))}

    def _a2_gate(path: str) -> dict:
        with open(path) as f:
            sec = json.load(f)["section"]
        assert sec["g_apop"] == 0.0 and sec["a1_pass"], \
            "the A2 gate needs the verified a1 checkpoint"
        ro = sec["a2_readout"]
        a2_pass = bool(ro["ratio_pass"])
        return {"seg": "a2-gate",
                "a2_pass": a2_pass,
                "enrichment_ratio": ro["enrichment_ratio"],
                "ratio_bar": ro["ratio_bar"],
                "ratio_pass": ro["ratio_pass"],
                "n_marked": ro["n_marked"],
                "source": os.path.abspath(path),
                "note": ("the A2 decision that conditions the grid "
                         "dispatch (the docstring: A3 runs ONLY if A2 "
                         "passes); the merge re-derives the SAME "
                         "decision from the a1 section and asserts "
                         "equality — the deposit's A2 gate record is "
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
        a1 = sections["a1"]
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

        # ---- A1 (the dormant identity, the migration gate; ran FIRST,
        #      fail = STOP) ------------------------------------------------
        a1_ok = bool(a1["a1_pass"])
        assert a1_ok, "A1 (the dormant identity) FAILED — the " \
            "experiment stops before any gate evaluation"

        # ---- row-set integrity across sections (T and Wbase are
        #      g-independent, so the row sets must match 1:1) -----------
        base_rowmap = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                       for r in a1["rows"] if not r.get("rejected")}
        for k, sec in grid_secs.items():
            m = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                 for r in sec["rows"] if not r.get("rejected")}
            assert m == base_rowmap, f"row set drifted ({k})"

        # ---- A2 (the readout; the gate, evaluated exactly once, HERE) ----
        ro = a1["a2_readout"]
        a2_pass = bool(ro["ratio_pass"])

        # ---- A3 (the coupling; ONLY if A2 passes) -------------------------
        base_bnd = a1["worst_bnd_err_mV"]
        base_wn = a1["worst_nonbnd_err_mV"]
        assert base_bnd is not None and base_bnd > 0.0, \
            "degenerate baseline worst boundary-row err"
        a3_record: dict = {"status": None, "pass": None}
        a3_reduction = None
        nonbnd_change = None
        g_star = None
        cells: dict = {}
        if not a2_pass:
            a3_record = {
                "status": "SKIPPED-A2-FAIL", "pass": None,
                "clause": ("the marked cells' commitment-noise "
                           "relaxation at the pre-named grid "
                           "{0.25, 0.5, 1.0} — NOT RUN: the docstring "
                           "gates A3 on A2 (A2 REFUTE -> A3 skipped and "
                           "recorded SKIPPED-A2-FAIL); no g_apop > 0 "
                           "decode was executed anywhere in this "
                           "experiment"),
                "identity_at_g0": a1_ok,
                "n_identity_checks": a1["n_checks"],
                "n_identity_checks_pass": a1["n_checks_pass"]}
        else:
            reds = {}
            for k, sec in sorted(grid_secs.items()):
                gv = float(sec["g_apop"])
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
                    "n_apop_marks_total": sec["n_apop_marks_total"],
                    "apop_last_max_over_rows":
                        sec["apop_last_max_over_rows"],
                    "n_rows": sec["n_rows"], "n_ok": sec["n_ok"]}
            assert len(reds) == 3, "the pre-named grid is incomplete"
            g_star = max(reds, key=lambda k: reds[k])
            a3_reduction = reds[g_star]
            nonbnd_change = cells[str(g_star)]["nonbnd_change_vs_dormant"]
            a3_pass = bool(a1_ok and a3_reduction >= 0.10
                           and nonbnd_change <= 0.05)
            a3_record = {
                "status": "PASS" if a3_pass else "REFUTE",
                "pass": a3_pass,
                "clause": ("the best grid cell reduces the worst "
                           "boundary-row err >= 10% AND the "
                           "non-boundary rows' worst-err change "
                           "<= +5% at that cell (the exp258/exp259/"
                           "exp261 forms verbatim; the gate reads the "
                           "best cell, zero post-hoc selection; all "
                           "three nonzero g values reported; g_apop = 0 "
                           "is the dormant identity — bit-exact per "
                           "A1)"),
                "identity_at_g0": a1_ok,
                "n_identity_checks": a1["n_checks"],
                "n_identity_checks_pass": a1["n_checks_pass"],
                "g_star": float(g_star),
                "reduction_at_best_cell": a3_reduction,
                "nonbnd_change_at_best_cell": nonbnd_change,
                "baseline": {"worst_bnd_err_mV": base_bnd,
                             "worst_nonbnd_err_mV": base_wn,
                             "source": ("a1's g_apop=0 rows (bit-exact "
                                        "vs production per A1)")},
                "all_cells": cells}

        # ---- A4 (the discipline) -----------------------------------------
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
        a4_pass = bool(deposits_unchanged and coll_unchanged
                       and floor_ok and n_rej_total == 0
                       and det["pass_b_byte_identical"]
                       and header_unchanged)

        # ---- branch + verdict --------------------------------------------
        evaluated = [a1_ok, a2_pass, a4_pass]
        if a3_record["pass"] is not None:
            evaluated.append(a3_record["pass"])
        n_pass = sum(1 for v in evaluated if v)
        if not a2_pass:
            branch = "APOP-INERT"
        elif a3_record["pass"]:
            branch = "APOP-CARRIES"
        else:
            branch = "APOP-READOUT-ONLY"
        a3_txt = a3_record["status"]
        a3_detail = ""
        if a3_reduction is not None:
            a3_detail = (f" (reduction {a3_reduction:+.4f} at "
                         f"g_apop={g_star}; non-boundary change "
                         f"{nonbnd_change:+.4f})")
        verdict = (
            f"{n_pass}/{len(evaluated)} evaluated gates | "
            f"A1 {'PASS' if a1_ok else 'FAIL'} "
            f"(dormant identity 75/75 bit-exact, ran FIRST) | "
            f"A2 {'PASS' if a2_pass else 'REFUTE'} "
            f"(marked-set canon-boundary enrichment ratio "
            f"{ro['enrichment_ratio']:.4f} vs bar {ro['ratio_bar']}; "
            f"marked {ro['n_marked']}/{ro['n_points']}, "
            f"marked&bnd {ro['n_marked_bnd']} vs unmarked&bnd "
            f"{ro['n_unmarked_bnd']}) | "
            f"A3 {a3_txt}{a3_detail} | "
            f"A4 {'PASS' if a4_pass else 'FAIL'} | {branch}")

        deposit = {
            "exp": "exp264",
            "claim": (
                "THE APOP CHANNEL ACTIVATION (the FIFTH channel "
                "activation under the exp257 schema): ch6 apop — the "
                "paper's apoptosis-as-morphogenetic-signal face, "
                "stack-native. The pre-named instrument: the "
                "extreme-theta marking rule — a cell is marked iff its "
                "settled theta sits in the battery-wide extreme decile "
                "[both tails] OR the cell sits in the amputation's "
                "blastema band; the mark is state (carried in ch6), "
                "the readout tests whether the marked set localizes "
                "the boundary excess, the coupling (gated on the "
                "readout) relaxes the marked cells' commitment noise "
                "(the M26b face). A1 the dormant identity (75/75 "
                "bit-exact, ran FIRST, fail = STOP); A2 the readout "
                "(the marked set's CANON-BOUNDARY enrichment ratio "
                ">= 2.0; the Fisher-type count comparison recorded, "
                "the ratio is the gate); A3 (ONLY if A2 passes) the "
                "marked cells' commitment-noise relaxation "
                "(1 - g_apop) at the pre-named grid {0, 0.25, 0.5, "
                "1.0}, best cell >= 10% boundary reduction AND "
                "<= +5% non-boundary change (A2 PASS + A3 PASS -> "
                "APOP-CARRIES / A3 REFUTE -> APOP-READOUT-ONLY / "
                "A2 REFUTE -> APOP-INERT)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any body "
                    "(pre-registration 437ee24, batch 24; gates A1-A4 "
                    "fixed there, each evaluated exactly once); the "
                    "pre-registered header (docstring + imports + "
                    "constants) sha256-verified byte-unchanged at "
                    "merge: " + EXPECTED_HEADER_SHA256),
                "docstring_sha256": DOCSTRING_SHA256,
                "mechanism": (
                    "the mark rule evaluated ONCE on the verified "
                    "dormant battery at the a1 checkpoint and carried "
                    "from there: a cell is marked iff its SETTLED "
                    "theta sits in the BATTERY-WIDE extreme decile "
                    "[both tails: theta <= q10 OR theta >= q90 of the "
                    "pooled settled-theta distribution over EVERY "
                    "verified g_apop = 0 battery row — 25 instances x "
                    "3 seeds x 400 cells; the zero-knob quantile "
                    "rule, numpy's default linear-interpolation "
                    "quantiles] OR the cell sits in the amputation's "
                    "blastema band [the row's amputated region — "
                    "exactly the slice the executor's c.amputate "
                    "receives, the band collective.py sets to the "
                    "blastema state theta = -40.0; the docstring's "
                    "'the cell SITS IN the amputation's blastema "
                    "band' is positional membership in the "
                    "amputation's own band, not a derived "
                    "frontier-adjacency class]. WHY CARRIED FROM THE "
                    "CHECKPOINT (DISCLOSED READING, outcome-blind, "
                    "fixed before any g_apop > 0 run): the docstring "
                    "defines the mark 'at settle time' — a "
                    "settled-state property — while the coupling "
                    "acts at commit time DURING the run; the only "
                    "consistent reading is the mark fixed on the "
                    "verified dormant battery (the a1 checkpoint's "
                    "own settled states, bit-exact vs production "
                    "per A1) and threaded per row into the "
                    "instrumented runs (the exp261 Pbar form, "
                    "generalized to a per-row mask); the mark is "
                    "g-independent (it derives from g-independent "
                    "settled states and zone geometry), so the SAME "
                    "mark applies across the whole grid (the "
                    "executor asserts its own amputation band equals "
                    "the checkpoint's and is fully contained in the "
                    "mark). THE COUPLING: at the commit of a MARKED "
                    "cell (g_apop > 0 only), the commitment noise is "
                    "multiplied by (1 - g_apop): sigma = "
                    "COMMIT_NOISE * (1 - g_apop) — the M26b face, "
                    "relaxing the marked cell's commitment toward "
                    "the inherited/canon mean; the verbatim commit "
                    "branch chain (phi_spec / canon_src / theta[src]) "
                    "is kept as pure reads and the noise is drawn "
                    "ONCE per commit at the pre-named sigma — numpy's "
                    "Generator.normal consumes the identical "
                    "underlying stream for any scale, so the stream "
                    "POSITION is preserved for every cell (marked or "
                    "not) across the whole grid, and at g_apop = 0 "
                    "the else-branch takes the VERBATIM sigma so the "
                    "dormant path is bit-exact (A1 asserts it per "
                    "row); the apop channel (ch6) is WRITTEN with "
                    "the mark (1.0) at the same commit via the "
                    "public accessors (c.read_channel('apop') / "
                    "c.set_channel('apop', ...)) — the activation's "
                    "channel-write face, the docstring's 'the mark "
                    "is state (carried in ch6)'; the commit value is "
                    "written to BOTH channels exactly as the "
                    "verbatim commit writes theta_new to both; "
                    "g_apop = 0.0 takes the verbatim path with ZERO "
                    "deviation (no apop write, no sigma change) — "
                    "the bit-exact dormant default, the migration "
                    "gate's own face"),
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
                    "identity at g_apop = 0 is asserted per row against "
                    "the production decode AND exp199's deposit AND "
                    "exp208's decomposition rows (exp226's R1 "
                    "machinery verbatim); T and Wbase are "
                    "g-independent so the row sets match 1:1 across "
                    "the grid (asserted at merge); the A2-gated "
                    "dispatch: the grid segments were launched only "
                    "after --a2-gate read A2 PASS from the a1 "
                    "checkpoint section file")},
            "sections": {k: sections[k] for k in sorted(sections)},
            "readout": ro,
            "grid": {"g_values": [0.0, 0.25, 0.5, 1.0],
                     "g_star": (float(g_star)
                                if g_star is not None else None),
                     "a3_status": a3_record["status"],
                     "cells": cells},
            "gates": {
                "A1": {"pass": a1_ok, "migration_gate": True,
                       "ran_first": True, "fail_stop": True,
                       "n_rows": a1["n_rows"], "n_ok": a1["n_ok"],
                       "n_checks_pass": a1["n_checks_pass"],
                       "n_checks": a1["n_checks"],
                       "clause": ("g_apop = 0 reproduces the "
                                  "production decode bit-exactly on "
                                  "the c6 battery, 75/75 rows (the "
                                  "exp258 X1 form verbatim)"),
                       "disclosure": (
                           "g_apop = 0 vs the production scoped "
                           "decode: V/T states bit-exact, errs + "
                           "verified equal, exp199's deposit "
                           "replayed at its 2-dp rounding, exp208's "
                           "decomposition rows reproduced bit-exactly "
                           "(exp226's R1 verbatim)")},
                "A2": {"pass": a2_pass,
                       "clause": ("the marked set's CANON-BOUNDARY "
                                  "enrichment ratio >= 2.0 (the "
                                  "Fisher-type count comparison "
                                  "recorded, the ratio is the gate), "
                                  "on the settled c6 battery states "
                                  "(zero-risk: read-only)"),
                       "enrichment_ratio": ro["enrichment_ratio"],
                       "ratio_bar": ro["ratio_bar"],
                       "ratio_pass": ro["ratio_pass"],
                       "rate_marked_bnd": ro["rate_marked_bnd"],
                       "rate_unmarked_bnd": ro["rate_unmarked_bnd"],
                       "q10": ro["q10"], "q90": ro["q90"],
                       "n_marked": ro["n_marked"],
                       "n_marked_bnd": ro["n_marked_bnd"],
                       "n_unmarked": ro["n_unmarked"],
                       "n_unmarked_bnd": ro["n_unmarked_bnd"],
                       "fisher_2x2": ro["fisher_2x2"],
                       "fisher_oddsratio": ro["fisher_oddsratio"],
                       "fisher_two_sided_p": ro["fisher_two_sided_p"],
                       "n_points": ro["n_points"]},
                "A3": a3_record,
                "A4": {"pass": a4_pass,
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
                "the MARK-RULE RESOLUTION is disclosed in "
                "pre_registered.mechanism and was fixed outcome-blind "
                "BEFORE any g_apop > 0 run: the extreme decile is the "
                "battery-wide pooled settled-theta quantile rule "
                "[both tails, numpy default linear interpolation]; "
                "the blastema band is the amputation's own region "
                "(the c.amputate slice, the blastema-state band "
                "collective.py sets to theta = -40.0), not a derived "
                "frontier class; the mark is fixed on the verified "
                "dormant battery and threaded per row (g-independent, "
                "band-containment asserted per run); no gate depends "
                "on a post-hoc choice",
                "the A2-gated dispatch (the docstring: A3 runs ONLY "
                "if A2 passes): the a1 segment is the checkpoint; "
                "--a2-gate read the A2 decision from it BEFORE any "
                "g_apop > 0 segment was launched (the grid segments "
                "themselves assert the checkpoint's A2 PASS via "
                "--marks-from before running); on an A2 REFUTE this "
                "merge records A3 as SKIPPED-A2-FAIL and no g_apop > "
                "0 decode exists anywhere in the experiment",
                "the commit restructure (one noise draw per commit at "
                "the pre-named sigma, the branch chain kept as pure "
                "reads) is bit-exact at g_apop = 0 by construction "
                "and A1 asserts the resulting states per row against "
                "the production decode; the battery bring-up ran "
                "inside the a1 segment itself — any instrument "
                "defect would have failed A1 there and stopped the "
                "experiment before the gates; every gate was "
                "evaluated exactly once, at the merge",
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
    elif args.a2_gate is not None:
        result = _a2_gate(args.a2_gate)
    elif args.seg == "a1":
        result = {"seg": "a1", "section": _seg_a1()}
    elif args.seg in G_APOP:
        assert args.marks_from is not None, \
            "grid segments need --marks-from (the a1 checkpoint)"
        with open(args.marks_from) as f:
            _a1sec = json.load(f)["section"]
        assert _a1sec["g_apop"] == 0.0 and _a1sec["a1_pass"], \
            "the a1 checkpoint is not a verified dormant battery"
        assert _a1sec["a2_readout"]["ratio_pass"], \
            "A2 did not pass on the checkpoint — A3 must not run"
        result = {"seg": args.seg,
                  "section": _seg_grid(args.seg, _a1sec["marks"])}
    else:
        raise SystemExit("use --seg {a1,g025,g050,g100} / --a2-gate / "
                         "--merge (runner split is canonical)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, default=str)
    if args.merge:
        print(f"=== exp264 MERGE: branch {result['branch']} ===")
        for k, v in result["gates"].items():
            _st = ("SKIPPED" if v.get("status") == "SKIPPED-A2-FAIL"
                   else ("PASS" if v["pass"] else "REFUTE/FAIL"))
            print(f"  {k}: {_st}")
        print(f"  {result['verdict']}")
    else:
        print(f"=== exp264 seg {result['seg']} written ===")
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
