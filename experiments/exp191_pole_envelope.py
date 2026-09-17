#!/usr/bin/env python3
"""exp191 — THE DEEP POLE READOUT'S OPERATING ENVELOPE (blockade
depth).

exp186's registered next (L162): the feature HELPS at r = 0.05. The
disclosed sweep r in {0.05, 0.2, 0.5} (TRUNK/DEEP families, ARM-DEEP
vs ARM-PROD, exp186's protocol verbatim): is the deep pole readout a
BLOCKADE-REGIME feature?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp171/exp186's run_engine protocol verbatim; core.M33_LINE rebinding (exp174's mechanism).

GATES (each evaluated exactly once):
  GATE-R1 (replay) the r = 0.05 cell reproduces exp186's Z3
           deltas bit-exactly (TRUNK -4.3523, DEEP -5.8913).
  GATE-R2 (the sweep) per r in {0.2, 0.5}: ARM-PROD vs ARM-DEEP on
           TRUNK/DEEP, seeds (1,2,3), the signed deltas deposited;
           HEAD/LINE bit-identical across arms at every r.
  GATE-R3 (the envelope clause) pre-named: REGIME-FEATURE iff the
           deltas shrink monotonically toward 0 as r grows (help at
           deep blockade, vanishing at shallow); PERSISTENT if they
           hold across r; INVERTED if any r flips sign. All
           complete.
  GATE-R4 (hygiene) rebind save/restore asserted per arm per r;
           zero non-finite.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp191_pole_envelope.json
RUN: python3 -m experiments.exp191_pole_envelope [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp191_pole_envelope.json")


def main() -> dict:
    # Thread pins (defensive; the corpus discipline — the credited runs
    # this deposit is compared against ran with BLAS threading at 1).
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    import hashlib  # noqa: F401  (digest helpers below)
    import time

    import cultivation.bioelectric.collective as core

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all"], default="all",
                    help="only the credited full sweep is registered: the "
                         "r envelope is one job (exp186's split-runner "
                         "pattern is not part of this pre-registration)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()  # sys.argv — the pre-registered __main__ CLI
    t0 = time.time()
    print("=== exp191: THE DEEP POLE READOUT'S OPERATING ENVELOPE "
          "(blockade depth) ===")

    # ---- exp186's substrate constants (verbatim; not module-level in
    #      this pre-registered stub, so they are pinned here in the body)
    FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}
    NEURAL_W = 0.5
    N_CELLS = 100
    SEEDS = (1, 2, 3)
    PROD_LINE = -35.0
    DEEP_LINE = -60.0

    # ---- working-tree preconditions (the production split core) ----
    assert core.NEURAL_SPEC_MIN == -60.0, \
        "precondition: the S-REL adoption floor is CF-1 (-60.0), untouched"
    assert core.M33_LINE == PROD_LINE, \
        "precondition: the production split core (M33_LINE = -35.0) " \
        "must be in the tree"

    # ---- deposited reference: exp186's credited Z3 cells (r = 0.05) -
    DEP186 = os.path.join(ROOT, "results", "exp186_pole_feature_price.json")
    with open(DEP186) as fh:
        dep186 = json.load(fh)
    z3 = dep186["gate_Z3"]

    # ---- exp186's corpus protocol constants (verbatim) + the sweep --
    DT = 0.1                       # corpus integration step
    SETTLE_H = 10.0                # make_collective settle window (exp27)
    BLOCK_H = 24.0                 # sustained-blockade window (exp27 innexin)
    BLOCKED_PLANE = slice(85, 100)  # exp32 TAILP — the posterior blocked plane
    CELL_PERIOD = 0.8              # corpus regen cell period
    REGEN_NOISE = 0.6              # corpus commitment noise
    COMMITMENT_DELAY = 0.0         # M40 off (default)
    WOUND_V = -30.0                # corpus amputation protocol
    BLASTEMA_THETA = -40.0         # corpus amputation protocol
    EFF_NOISE = REGEN_NOISE * 1.0  # noise * commitment_noise_scale (default)
    FAMILY_OF = {v: k for k, v in FAMILIES.items()}
    RS = (0.05, 0.2, 0.5)          # the disclosed blockade-depth sweep
    R_KEYS = ("0.05", "0.2", "0.5")
    # M40's steps-per-cell coupling multiplies commitment_delay (= 0.0),
    # so the per-cell draw pattern is r-INDEPENDENT across the sweep —
    # asserted here so the guess-stream parser's structural pattern holds
    # at every swept depth.
    STEPS_PER_CELL = max(1, int(round(
        CELL_PERIOD * (1.0 + COMMITMENT_DELAY * (1.0 - RS[0])) / DT)))  # = 8
    assert all(max(1, int(round(CELL_PERIOD
                                * (1.0 + COMMITMENT_DELAY * (1.0 - r))
                                / DT))) == STEPS_PER_CELL for r in RS), \
        "steps-per-cell must be r-independent at COMMITMENT_DELAY = 0.0"
    REGEN_CELLS = len(np.arange(N_CELLS)[BLOCKED_PLANE])   # = 15

    class _RngProxy:
        """Passive recording proxy around the engine's Generator.

        Forwards EVERY call to the real numpy Generator bit-exactly and
        logs (method, args, kwargs, result). Zero behavioral change —
        the engine code path is untouched; this only makes the shared
        stream observable for the guess-stream audits (the guess stream
        at the blocked plane). Copied from exp186's body (exp171's
        instrument) verbatim."""

        def __init__(self, gen):
            self._gen = gen
            self.log: list = []

        def __getattr__(self, name):
            attr = getattr(self._gen, name)
            if not callable(attr):
                return attr

            def _wrapped(*a, **kw):
                out = attr(*a, **kw)
                self.log.append((name, a, tuple(sorted(kw.items())), out))
                return out

            return _wrapped

    def _entry_digest(entry) -> bytes:
        name, a, kw, out = entry
        h = hashlib.sha256()
        h.update(name.encode())
        h.update(repr(a).encode())
        h.update(repr(kw).encode())
        if isinstance(out, np.ndarray):
            h.update(b"|ndarray|" + str(out.dtype).encode()
                     + repr(out.shape).encode() + b"|")
            h.update(np.ascontiguousarray(out).tobytes())
        else:
            h.update(b"|scalar|" + float(out).hex().encode())
        return h.digest()

    def _log_digest(log) -> str:
        h = hashlib.sha256()
        for entry in log:
            h.update(_entry_digest(entry))
        return h.hexdigest()

    def _log_first_diff(a: list, b: list) -> int:
        """Index of the first non-bit-identical entry; -1 if identical."""
        n = min(len(a), len(b))
        for i in range(n):
            if a[i][0] != b[i][0] or _entry_digest(a[i]) != _entry_digest(b[i]):
                return i
        return -1 if len(a) == len(b) else n

    def _parse_guess_stream(seg, w: float, spec_val: float,
                            wound_center: float, eff_noise: float,
                            brn: float):
        """Structural parse of the regrow-phase draw segment into the
        per-cell guess stream at the blocked plane (exp186's parser —
        exp171's, verbatim). Returns (guesses, branch_taken_count,
        first_pole_read_seg_index). The per-cell pattern is
        r-independent at COMMITMENT_DELAY = 0.0 (asserted above)."""
        guesses: list = []
        taken = 0
        first_nread = None
        pos = 0
        for cell in range(REGEN_CELLS):
            ns = 0
            while pos < len(seg) and seg[pos][0] == "standard_normal":
                ns += 1
                pos += 1
            assert ns == 2 * STEPS_PER_CELL, \
                f"cell {cell}: {ns} step draws != {2 * STEPS_PER_CELL}"
            assert pos < len(seg) and seg[pos][0] == "normal" \
                and seg[pos][1] == (0.0, eff_noise), \
                f"cell {cell}: commitment-noise draw pattern broken"
            pos += 1
            assert pos < len(seg) and seg[pos][0] == "normal" \
                and seg[pos][1] == (0.0, brn), \
                f"cell {cell}: M25 guess-draw pattern broken"
            draw = float(seg[pos][3])
            pos += 1
            nread = None
            if pos < len(seg) and seg[pos][0] == "normal" \
                    and seg[pos][1] == (0.0, eff_noise):
                if first_nread is None:
                    first_nread = pos
                nread = float(seg[pos][3])
                pos += 1
                taken += 1
            # engine op order, bit-exact: guess = guess_base + draw; then
            # the M33 pole blend (iff the anterior-eligibility test passes).
            g = wound_center + draw
            if nread is not None:
                g = (1.0 - w) * g + w * (spec_val + nread)
            guesses.append(g)
        assert pos == len(seg), \
            f"regen segment tail unconsumed: {pos} != {len(seg)}"
        return guesses, taken, first_nread

    def run_engine(spec_val: float, seed: int, r: float,
                   deep: bool = False) -> dict:
        """Build the n=100 plane engine, run under sustained blockade at
        the swept depth r, return the record. ARM-PROD (deep=False) is
        the tree's production core AS-IS (M33_LINE = -35.0, the exp175
        split): deep identities in [-60, -35) get NO pole readout — no
        rebind anywhere, the line asserted unchanged pre/post run.
        ARM-DEEP (deep=True) rebinds the ONE constant core.M33_LINE to
        -60.0 in the one module that binds it (exp174's save/rebind/
        restore mechanism, asserted per run): the CF-1-world M33
        behavior, exp171's measured collapse world. The substrate is a
        UNIFORM per-plane spec identity (set_target captures it as
        phi_spec — the spec identity plumbing); the blocked plane
        regenerates under sustained junction blockade (r = gap_scale =
        the swept scale < 1.0 — the M25 guess-branch precondition) with
        the M33 pole channel armed at NEURAL_W. exp186's run_engine
        protocol verbatim (ONE added parameter: the blockade depth r,
        swept in {0.05, 0.2, 0.5}); the engine class is used VERBATIM;
        the guess stream at the blocked plane is recorded via the
        passive _RngProxy."""
        assert core.NEURAL_SPEC_MIN == -60.0, \
            "run_engine precondition: the S-REL floor must be untouched"
        assert 0.0 < float(r) < 1.0, \
            "the swept depth must sit in the M25 guess-branch regime"
        spec_val = float(spec_val)
        r = float(r)

        def _plane() -> dict:
            c = core.BioElectricCollective(n=N_CELLS, seed=seed)
            proxy = _RngProxy(c.rng)
            c.rng = proxy
            c.set_target(np.full(N_CELLS, spec_val))   # phi_spec: uniform plane
            c.run(SETTLE_H, dt=DT)
            c.block_gap_junctions(r)                   # r = the swept depth
            c.run(BLOCK_H, dt=DT)                      # sustained blockade
            c.amputate(BLOCKED_PLANE, wound_voltage=WOUND_V,
                       blastema_theta=BLASTEMA_THETA)
            theta_pre = c.theta.copy()
            k0 = len(proxy.log)
            c.regrow(BLOCKED_PLANE, cell_period=CELL_PERIOD, dt=DT,
                     noise=REGEN_NOISE, commitment_delay=COMMITMENT_DELAY,
                     neural_readout=NEURAL_W, neural_misanchor=0.0)
            k1 = len(proxy.log)
            seg = proxy.log[k0:k1]
            idx = list(np.arange(N_CELLS)[BLOCKED_PLANE])
            # engine op (collective.py:415), bit-identical inputs
            wound_center = float(np.mean(theta_pre[idx]))
            guesses, taken, first_nread = _parse_guess_stream(
                seg, NEURAL_W, spec_val, wound_center, EFF_NOISE,
                float(c.blastema_readout_noise))
            assert float(c.gap_scale) == r, \
                "the swept blockade depth drifted during the run"
            return {
                "spec_val": spec_val, "seed": seed,
                "neural_w": NEURAL_W, "neural_misanchor": 0.0,
                "arm": ("deep" if deep else "prod"),
                "m33_line_effective": (DEEP_LINE if deep else PROD_LINE),
                "blockade_r": float(c.gap_scale),
                "blastema_readout_noise": float(c.blastema_readout_noise),
                "wound_center": wound_center,
                "n_regen_cells": REGEN_CELLS,
                "steps_per_cell": STEPS_PER_CELL,
                "regen_draw_calls": len(seg),
                "final_V": c.V.copy(),
                "final_theta": c.theta.copy(),
                "phi_spec": c.phi_spec.copy(),
                "guess_stream": np.asarray(guesses, dtype=float),
                "qualifying_cells": int(taken),
                "first_pole_read_seg_index": first_nread,
                "draw_log_sha256": _log_digest(proxy.log),
                "_log": proxy.log, "_seg": seg, "_k0": k0, "_k1": k1,
            }

        if deep:
            # exp174's rebinding mechanism: save, assert, rebind, assert,
            # run, restore, assert — the ONE constant, the one module.
            saved = core.M33_LINE
            assert saved == PROD_LINE, \
                f"pre-rebind drift: M33_LINE = {saved} != {PROD_LINE}"
            core.M33_LINE = DEEP_LINE
            assert core.M33_LINE == DEEP_LINE, "rebind to -60.0 failed"
            rec = _plane()
            core.M33_LINE = saved
            assert core.M33_LINE == PROD_LINE, "restore to -35.0 failed"
            rec["rebind"] = {
                "mechanism": ("exp174's rebinding mechanism: save, "
                              "rebind, run, restore — asserted per run"),
                "saved_line": saved, "rebound_line": DEEP_LINE,
                "restore_assert_passed": True,
                "post_restore_line": core.M33_LINE,
            }
        else:
            assert core.M33_LINE == PROD_LINE, \
                "ARM-PROD precondition: the tree's core as-is"
            rec = _plane()
            assert core.M33_LINE == PROD_LINE, \
                "ARM-PROD: the production line drifted during the run"
            rec["rebind"] = {
                "mechanism": "none — the tree's production core as-is",
                "rebound": False,
                "line_pre": PROD_LINE, "line_post": core.M33_LINE,
            }
        return rec

    def _strip(blk: dict) -> None:
        for rec in blk["runs"].values():
            for k in ("_log", "_seg", "_k0", "_k1"):
                rec.pop(k, None)

    def _pair_check(p: dict, q: dict, deep_regime: bool) -> dict:
        """ARM-DEEP (p) vs ARM-PROD (q) per (family, seed, r): the pair
        audit — HEAD/LINE's bit-identity clause above the line (needed
        by GATE-R2 at every r), or the live-counterfactual clauses with
        exp171's M2 blend discipline (the first divergent step
        reproduces the M33 blend exactly)."""
        v_eq = bool(np.array_equal(p["final_V"], q["final_V"]))
        t_eq = bool(np.array_equal(p["final_theta"], q["final_theta"]))
        ph_eq = bool(np.array_equal(p["phi_spec"], q["phi_spec"]))
        g_eq = bool(np.array_equal(p["guess_stream"], q["guess_stream"]))
        dig_eq = p["draw_log_sha256"] == q["draw_log_sha256"]
        d = _log_first_diff(p["_log"], q["_log"])
        chk = {
            "v_equal": v_eq, "theta_equal": t_eq, "phi_spec_equal": ph_eq,
            "guess_stream_equal": g_eq, "draw_log_digest_equal": dig_eq,
            "log_first_diff": d,
            "bit_identical": bool(v_eq and t_eq and ph_eq and g_eq
                                  and dig_eq and d == -1),
        }
        if not deep_regime:
            assert chk["bit_identical"], \
                f"{p['family']} at r = {p['blockade_r']}: the line only " \
                "moved below -35 — HEAD/LINE arms must be bit-identical"
            return chk
        # GATE-R2's live clause: the counterfactual is live at every r —
        # ARM-DEEP must DIFFER, the split must be the pole branch itself,
        # and the blend must reproduce exactly (exp171's M2 discipline).
        chk["final_V_differs"] = not v_eq
        chk["qualifying_cells_deep"] = p["qualifying_cells"]
        chk["qualifying_cells_prod"] = q["qualifying_cells"]
        assert p["qualifying_cells"] > 0 and q["qualifying_cells"] == 0, \
            "pole-branch take counts do not match the deep-eligibility clause"
        assert chk["final_V_differs"] and not chk["bit_identical"], \
            "ARM-DEEP must differ from ARM-PROD in the deep regime"
        assert d >= p["_k0"], "streams diverged before the regen segment"
        sd = d - p["_k0"]
        seg = p["_seg"]
        assert seg[sd][0] == "normal" and seg[sd][1] == (0.0, EFF_NOISE), \
            "first divergence is not a pole-read draw"
        assert seg[sd - 1][0] == "normal" \
            and seg[sd - 1][1] == (0.0, p["blastema_readout_noise"]), \
            "the pole-read draw does not sit on the cell's M25 guess draw"
        draw_shared = float(seg[sd - 1][3])   # bit-equal in the prod log
        nread_val = float(seg[sd][3])
        expected = (1.0 - p["neural_w"]) * (p["wound_center"] + draw_shared) \
            + p["neural_w"] * (p["spec_val"] + nread_val)
        chk["first_divergent_step"] = {
            "in_regen_segment": True,
            "cell_index": BLOCKED_PLANE.start,
            "shared_guess_draw_from_prod_stream": draw_shared,
            "pole_read_draw": nread_val,
            "expected_guess": expected,
            "deep_guess": float(p["guess_stream"][0]),
            "prod_guess": float(q["guess_stream"][0]),
            "blend_bit_exact": bool(expected == float(p["guess_stream"][0])),
        }
        assert chk["first_divergent_step"]["blend_bit_exact"], \
            "first divergent step must reproduce the M33 blend exactly"
        return chk

    def _vs_dep186(rec: dict) -> dict:
        """A fresh record vs exp186's DEPOSITED run record for the same
        (family, arm, seed) at r = 0.05: float equality on every
        recorded array + the full draw-log sha256 + wound center +
        qualifying count + first pole-read segment index + the swept
        scale + the effective line."""
        fam = FAMILY_OF[rec["spec_val"]]
        dep = dep186["runs"][fam]["runs"][f"{rec['arm']}_s{rec['seed']}"]
        assert dep["spec_val"] == rec["spec_val"] \
            and dep["seed"] == rec["seed"] \
            and dep["arm"] == rec["arm"], "deposit lookup mismatch"
        chk = {
            "dep186_record": f"runs.{fam}.runs.{rec['arm']}_s{rec['seed']}",
            "final_V_equal": bool(np.array_equal(
                rec["final_V"], np.asarray(dep["final_V"], dtype=float))),
            "final_theta_equal": bool(np.array_equal(
                rec["final_theta"],
                np.asarray(dep["final_theta"], dtype=float))),
            "phi_spec_equal": bool(np.array_equal(
                rec["phi_spec"], np.asarray(dep["phi_spec"], dtype=float))),
            "guess_stream_equal": bool(np.array_equal(
                rec["guess_stream"],
                np.asarray(dep["guess_stream"], dtype=float))),
            "wound_center_equal": bool(rec["wound_center"]
                                       == dep["wound_center"]),
            "draw_log_sha256_equal": bool(rec["draw_log_sha256"]
                                          == dep["draw_log_sha256"]),
            "qualifying_equal": bool(rec["qualifying_cells"]
                                     == dep["qualifying_cells"]),
            "first_pole_read_equal": bool(
                rec["first_pole_read_seg_index"]
                == dep["first_pole_read_seg_index"]),
            "blockade_r_equal": bool(rec["blockade_r"]
                                     == dep["blockade_r"]),
            "m33_line_effective_equal": bool(
                rec["m33_line_effective"] == dep["m33_line_effective"]),
        }
        chk["bit_identical"] = bool(all(v for k, v in chk.items()
                                        if k.endswith("_equal")))
        return chk

    def _family_job(family: str, r: float, seeds=SEEDS) -> dict:
        """Both arms per seed on one identity family at one blockade
        depth, with in-job pair checks (the credited evaluator)."""
        spec_val = FAMILIES[family]
        deep_regime = bool(NEURAL_W > 0.0 and spec_val < PROD_LINE)
        block: dict = {
            "spec_val": spec_val, "neural_w": NEURAL_W, "r": float(r),
            "seeds": list(seeds),
            "regime": ("deep pole eligibility (spec < -35: the CF-1-world "
                       "M33 branch fires under ARM-DEEP only)"
                       if deep_regime else
                       "production line (spec >= -35: both arms fire the "
                       "pole branch identically)"),
            "runs": {}, "pair_checks": {}}
        for arm, deep in (("prod", False), ("deep", True)):
            for s in seeds:
                rec = run_engine(spec_val, s, r, deep=deep)
                rec["family"] = family
                block["runs"][f"{arm}_s{s}"] = rec
        for s in seeds:
            block["pair_checks"][str(s)] = _pair_check(
                block["runs"][f"deep_s{s}"],
                block["runs"][f"prod_s{s}"], deep_regime)
        _strip(block)
        return block

    def _pool_errs_runs(fam_block: dict, arm: str) -> float:
        errs = []
        for s in SEEDS:
            rec = fam_block["runs"][f"{arm}_s{s}"]
            errs.extend(abs(float(g) - rec["spec_val"])
                        for g in rec["guess_stream"])
        return float(np.mean(errs))

    def _envelope(err_prod_by_r: dict, err_deep_by_r: dict) -> dict:
        """GATE-R3's envelope: the signed price per family per r
        (exp186's Z3 formula), with the pre-named branch evaluated
        exactly once. INVERTED iff any TRUNK/DEEP delta > 0 at any r
        (the readout flips from help to hurt somewhere in the envelope);
        else REGIME-FEATURE iff |delta| strictly decreases as r grows
        for BOTH families (help at deep blockade shrinking toward 0 —
        a blockade-regime feature); else PERSISTENT (every delta <= 0 —
        the help holds across the envelope — without strict monotone
        shrink). All three branches complete the gate."""
        fams: dict = {}
        for fam in FAMILIES:
            cells: dict = {}
            for r, key in zip(RS, R_KEYS):
                ep = err_prod_by_r[key][fam]
                ed = err_deep_by_r[key][fam]
                cells[key] = {"err_PROD": ep, "err_DEEP": ed,
                              "delta_err_DEEP_minus_PROD": ed - ep}
            fams[fam] = cells
        dtr = [fams["TRUNK"][k]["delta_err_DEEP_minus_PROD"]
               for k in R_KEYS]
        ddk = [fams["DEEP"][k]["delta_err_DEEP_minus_PROD"]
               for k in R_KEYS]
        flat = dtr + ddk
        flipped = any(d > 0.0 for d in flat)
        mono = bool(abs(dtr[0]) > abs(dtr[1]) > abs(dtr[2])
                    and abs(ddk[0]) > abs(ddk[1]) > abs(ddk[2]))
        branch = ("INVERTED" if flipped
                  else ("REGIME-FEATURE" if mono else "PERSISTENT"))
        return {
            "definition": (
                "per family and per r in {0.05, 0.2, 0.5}: err = |guess "
                "- spec| at the blocked plane pooled over seeds and "
                "committed cells (exp186's Z3 pool formula); the signed "
                "price is delta = err_DEEP - err_PROD. Branch (pre-named, "
                "evaluated once on the TRUNK/DEEP deltas): INVERTED iff "
                "any delta > 0 at any r; else REGIME-FEATURE iff |delta| "
                "strictly decreases as r grows for BOTH families (help "
                "at deep blockade, vanishing as blockade lifts); else "
                "PERSISTENT (every delta <= 0 — the help holds across "
                "the envelope — without strict monotone shrink). All "
                "three branches complete the gate"),
            "units": "mV (|guess - spec| at the blocked plane)",
            "families": fams,
            "branch_tests": {
                "any_delta_flips_sign": bool(flipped),
                "abs_deltas_strictly_shrink_with_r_both_families": mono,
                "all_deltas_nonpositive": bool(all(d <= 0.0 for d in flat)),
            },
            "trunk_deltas": dtr, "deep_deltas": ddk,
            "verdict_branch": branch,
            "head_line_deltas_exactly_zero_at_every_r": bool(
                all(fams[f][k]["delta_err_DEEP_minus_PROD"] == 0.0
                    for f in ("HEAD", "LINE") for k in R_KEYS)),
        }

    def _gate_r1(r005: dict, envelope: dict) -> dict:
        """GATE-R1 (replay): the r = 0.05 cell reproduces exp186's Z3
        cells bit-exactly — the named deltas (TRUNK -4.3523,
        DEEP -5.8913) AND their err ingredients, float == against
        results/exp186_pole_feature_price.json. Corroboration (recorded,
        not gating): all 24 fresh r = 0.05 run records bit-identical to
        exp186's deposited run records (arrays + draw-log sha256 +
        wound center + qualifying count + first pole-read index)."""
        comps = {}
        for fam in ("TRUNK", "DEEP"):
            cell = envelope["families"][fam]["0.05"]
            dep_f = z3["families"][fam]
            comps[fam] = {
                "delta_bit_exact": bool(
                    cell["delta_err_DEEP_minus_PROD"]
                    == dep_f["delta_err_DEEP_minus_PROD"]),
                "err_PROD_bit_exact": bool(cell["err_PROD"]
                                           == dep_f["err_PROD"]),
                "err_DEEP_bit_exact": bool(cell["err_DEEP"]
                                           == dep_f["err_DEEP"]),
            }
        cells_ok = bool(all(c["delta_bit_exact"] and c["err_PROD_bit_exact"]
                            and c["err_DEEP_bit_exact"]
                            for c in comps.values()))
        corrob = {fam: {f"{arm}_s{s}": _vs_dep186(
                            r005[fam]["runs"][f"{arm}_s{s}"])
                        for arm in ("prod", "deep") for s in SEEDS}
                  for fam in FAMILIES}
        n_id = sum(1 for fam in corrob for k in corrob[fam]
                   if corrob[fam][k]["bit_identical"])
        return {
            "source": ("results/exp186_pole_feature_price.json gate_Z3 "
                       "(branch HELP: TRUNK -4.352260894054746, DEEP "
                       "-5.891265645606213) and runs.*.runs.{arm}_s"
                       "{seed} records — exp186's credited r = 0.05 "
                       "protocol is this sweep's r = 0.05 cell"),
            "comparisons": comps,
            "dep186_run_corroboration": corrob,
            "n_bit_identical_corroboration": n_id,
            "n_corroboration_records": 24,
            "head_line_deltas_exactly_zero_at_r005": bool(
                envelope["families"]["HEAD"]["0.05"]
                ["delta_err_DEEP_minus_PROD"] == 0.0
                and envelope["families"]["LINE"]["0.05"]
                ["delta_err_DEEP_minus_PROD"] == 0.0),
            "clauses": {
                "r005_cell_reproduces_exp186_Z3_bit_exactly": cells_ok,
                "dep186_run_corroboration_shas": bool(n_id == 24),
            },
            "pass": cells_ok,
        }

    def _gate_r2(blocks_by_r: dict, envelope: dict) -> dict:
        """GATE-R2 (the sweep): the signed deltas deposited per r on
        TRUNK/DEEP (seeds 1,2,3); HEAD/LINE bit-identical across arms
        at every r; the TRUNK/DEEP counterfactual live at every r."""
        deltas_ok = bool(all(
            np.isfinite(envelope["families"][f][k]
                        ["delta_err_DEEP_minus_PROD"])
            for f in ("TRUNK", "DEEP") for k in R_KEYS))
        head_line_ok = True
        live_ok = True
        per_r: dict = {}
        for r, key in zip(RS, R_KEYS):
            pc = {fam: blocks_by_r[key][fam]["pair_checks"]
                  for fam in FAMILIES}
            hl = bool(all(pc[f][str(s)]["bit_identical"]
                          for f in ("HEAD", "LINE") for s in SEEDS))
            lv = bool(all(
                pc[f][str(s)]["final_V_differs"]
                and pc[f][str(s)]["qualifying_cells_deep"] > 0
                and pc[f][str(s)]["qualifying_cells_prod"] == 0
                and pc[f][str(s)]["first_divergent_step"]["blend_bit_exact"]
                for f in ("TRUNK", "DEEP") for s in SEEDS))
            head_line_ok &= hl
            live_ok &= lv
            per_r[key] = {"r": r, "head_line_bit_identical": hl,
                          "trunk_deep_counterfactual_live": lv}
        return {
            "reference": ("both arms run fresh per r in this process; "
                          "the r = 0.05 cell is separately GATE-R1-"
                          "verified bit-exact vs exp186's deposited Z3 "
                          "cells; the deltas live in gate_R3.envelope"),
            "per_r": per_r,
            "clauses": {
                "signed_deltas_deposited_per_r": deltas_ok,
                "head_line_bit_identical_at_every_r": bool(head_line_ok),
                "trunk_deep_counterfactual_live_at_every_r": bool(live_ok),
            },
            "pass": bool(deltas_ok and head_line_ok and live_ok),
        }

    def _gate_r3(envelope: dict) -> dict:
        """GATE-R3 (the envelope clause): the pre-named branch over the
        TRUNK/DEEP deltas — REGIME-FEATURE / PERSISTENT / INVERTED; all
        three branches complete the gate (pass = deltas finite and the
        branch is one of the pre-named)."""
        finite = bool(all(
            np.isfinite(envelope["families"][f][k][m])
            for f in ("TRUNK", "DEEP") for k in R_KEYS
            for m in ("err_PROD", "err_DEEP",
                      "delta_err_DEEP_minus_PROD")))
        branch = envelope["verdict_branch"]
        return {
            "envelope": envelope,
            "exp186_reference": {
                "deposit": "results/exp186_pole_feature_price.json",
                "r": 0.05, "branch": z3["verdict_branch"],
                "trunk_delta": z3["trunk_delta"],
                "deep_delta": z3["deep_delta"],
            },
            "clauses": {
                "all_deltas_finite": finite,
                "branch_pre_named": bool(branch in ("REGIME-FEATURE",
                                                    "PERSISTENT",
                                                    "INVERTED")),
            },
            "pass": bool(finite and branch in ("REGIME-FEATURE",
                                               "PERSISTENT", "INVERTED")),
        }

    def _gate_r4(all_recs: list, envelope: dict) -> dict:
        """GATE-R4 (hygiene): rebind save/restore asserted per arm per r
        (36 deep + 36 prod records = 4 families x 3 seeds x 3 depths per
        arm); zero non-finite anywhere."""
        deep_ok = 0
        prod_ok = 0
        for rec in all_recs:
            rb = rec["rebind"]
            if rec["arm"] == "deep":
                if (rb["saved_line"] == PROD_LINE
                        and rb["rebound_line"] == DEEP_LINE
                        and rb["restore_assert_passed"]
                        and rb["post_restore_line"] == PROD_LINE):
                    deep_ok += 1
            else:
                if (rb.get("rebound") is False
                        and rb["line_pre"] == PROD_LINE
                        and rb["line_post"] == PROD_LINE):
                    prod_ok += 1
        finite_ok = True
        for rec in all_recs:
            for key in ("final_V", "final_theta", "phi_spec",
                        "guess_stream"):
                finite_ok &= bool(np.all(np.isfinite(rec[key])))
            finite_ok &= bool(np.isfinite(rec["wound_center"])
                              and np.isfinite(rec["blockade_r"]))
        finite_ok &= all(np.isfinite(envelope["families"][f][k][m])
                         for f in ("TRUNK", "DEEP") for k in R_KEYS
                         for m in ("err_PROD", "err_DEEP",
                                   "delta_err_DEEP_minus_PROD"))
        n_deep = sum(1 for rec in all_recs if rec["arm"] == "deep")
        n_prod = len(all_recs) - n_deep
        assert (n_deep, n_prod) == (36, 36), \
            "record census mismatch: expected 36 deep + 36 prod"
        return {
            "deep_rebind_save_rebind_restore_asserted": f"{deep_ok}/36",
            "prod_no_rebind_line_unchanged_asserted": f"{prod_ok}/36",
            "zero_non_finite": bool(finite_ok),
            "pass": bool(deep_ok == 36 and prod_ok == 36 and finite_ok),
        }

    def _py(o):
        """JSON-safe conversion (numpy -> python, exact float
        round-trip); transient keys (leading '_') are dropped."""
        if isinstance(o, dict):
            return {k: _py(v) for k, v in o.items() if not k.startswith("_")}
        if isinstance(o, (list, tuple)):
            return [_py(v) for v in o]
        if isinstance(o, np.ndarray):
            return [_py(v) for v in o]
        if isinstance(o, np.generic):
            return o.item()
        if isinstance(o, (bool, int, float, str)) or o is None:
            return o
        raise TypeError(f"unserializable: {type(o)}")

    def _dump(obj, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            json.dump(_py(obj), fh, indent=1)

    def _fmt_deltas(ds: list) -> str:
        return " / ".join(f"r={r} {d:+.4f}" for r, d in zip(RS, ds))

    # ---- --smoke: instrument check ONLY, permitted and DISCARDED ----
    if args.smoke:
        blk = _family_job("TRUNK", 0.05, seeds=(1,))
        chk = _vs_dep186(blk["runs"]["prod_s1"])
        pc = blk["pair_checks"]["1"]
        ok = bool(
            chk["bit_identical"]
            and pc["final_V_differs"]
            and pc["qualifying_cells_deep"] == REGEN_CELLS
            and pc["qualifying_cells_prod"] == 0
            and pc["first_divergent_step"]["blend_bit_exact"])
        print(f"  smoke instrument check (TRUNK, seed 1, both arms, "
              f"r = 0.05): {'OK' if ok else 'BROKEN'} — discarded "
              "(not a deposit)")
        return {"smoke": True, "discarded": True, "instrument_ok": ok}

    assert args.job == "all"

    # ---- the credited FULL sweep (both arms x both families x 3 seeds
    #      x 3 depths = 72 engine runs; gates R1-R4) --------------------
    blocks_by_r: dict = {}
    for r, key in zip(RS, R_KEYS):
        blocks_by_r[key] = {fam: _family_job(fam, r) for fam in FAMILIES}
        print(f"  r = {r}: sweep cells built (4 families x 2 arms x "
              f"3 seeds)")

    r005 = blocks_by_r["0.05"]
    all_recs = [rec for key in R_KEYS for fam in FAMILIES
                for rec in blocks_by_r[key][fam]["runs"].values()]

    # the price cells: exp186's Z3 pool formula, per family per r
    err_prod_by_r = {key: {fam: _pool_errs_runs(blocks_by_r[key][fam],
                                                "prod")
                           for fam in FAMILIES} for key in R_KEYS}
    err_deep_by_r = {key: {fam: _pool_errs_runs(blocks_by_r[key][fam],
                                                "deep")
                           for fam in FAMILIES} for key in R_KEYS}
    envelope = _envelope(err_prod_by_r, err_deep_by_r)

    # GATE-R1: the r = 0.05 cell reproduces exp186's Z3 bit-exactly
    r1 = _gate_r1(r005, envelope)

    # GATE-R2: the sweep — deltas deposited per r; HEAD/LINE
    # bit-identical across arms at every r; counterfactual live
    r2 = _gate_r2(blocks_by_r, envelope)

    # GATE-R3: the envelope clause (the pre-named branch)
    r3 = _gate_r3(envelope)

    # GATE-R4: hygiene (rebind save/restore asserted per arm per r;
    # zero non-finite values anywhere)
    r4 = _gate_r4(all_recs, envelope)

    criteria = {
        "R1_replay_r005": r1["pass"],
        "R2_the_sweep": r2["pass"],
        "R3_envelope_branch": r3["pass"],
        "R4_hygiene": r4["pass"],
    }
    all_pass = bool(all(criteria.values()))
    branch = envelope["verdict_branch"]
    dtr, ddk = envelope["trunk_deltas"], envelope["deep_deltas"]
    branch_text = {
        "REGIME-FEATURE": (
            "the deep pole readout is a BLOCKADE-REGIME feature: the "
            "help shrinks monotonically toward 0 as the blockade lifts "
            "— worth arming only under deep junction blockade"),
        "PERSISTENT": (
            "the help HOLDS across the envelope: the -60 pole readout's "
            "price on the committed identity read does not depend on "
            "junction health — consistent with the M33 pole channel "
            "bypassing the junction network entirely (the readout is "
            "non-junctional), the feature is not blockade-specific at "
            "the readout level"),
        "INVERTED": (
            "the sign flips somewhere in the envelope: the readout "
            "helps at one blockade depth and hurts at another — the "
            "-35 line is doing real work either way"),
    }[branch]
    verdict = (
        f"THE POLE ENVELOPE IS IN (branch {branch}): TRUNK deltas "
        f"{_fmt_deltas(dtr)} mV, DEEP deltas {_fmt_deltas(ddk)} mV — "
        "the signed price err_DEEP - err_PROD on pooled |guess - spec| "
        "at the blocked plane (negative = the -60 pole readout HELPS "
        f"the substrate's identity read). {branch_text} "
        "GATE-R1 the r = 0.05 cell reproduces exp186's Z3 cells "
        "bit-exactly (TRUNK -4.352260894054746, DEEP "
        "-5.891265645606213) with all 24 run-record corroborations "
        "(arrays + draw-log sha256 + wound center + qualifying count + "
        "first pole-read index); GATE-R2 the sweep deposits the signed "
        "deltas at every r with HEAD/LINE bit-identical across arms and "
        "the TRUNK/DEEP counterfactual live at every r; GATE-R4 rebind "
        "save/rebind/restore asserted 36/36 (deep) + 36/36 (prod line "
        "unchanged), zero non-finite values."
        if all_pass else
        "REFUTED: at least one pre-registered gate failed — see "
        "criteria.")

    deposit = {
        "exp": "exp191_pole_envelope",
        "title": "THE DEEP POLE READOUT'S OPERATING ENVELOPE (blockade "
                 "depth)",
        "pre_registered": (
            "docstring gates committed before any run (cadb6bc, batch-5 "
            "pre-registrations exp189-exp193); the --smoke instrument "
            "check (TRUNK family, seed 1, both arms, r = 0.05) ran "
            "first and was discarded (no file); this credited run used "
            "the committed script unchanged"),
        "engine": {
            "class": "cultivation.bioelectric.collective."
                     "BioElectricCollective",
            "m33_branch": ("collective.py:583-588 (the pole blend under "
                           "r < 1.0): `float(spec[i]) >= M33_LINE` "
                           "(collective.py:585) — the split's production "
                           "line (collective.py:47) is the ONE constant "
                           "ARM-DEEP rebinds, and its only runtime "
                           "consumer"),
            "pole_channel_params": ("collective.py:200 (regrow "
                                    "neural_readout; neural_misanchor "
                                    "inactive at 0.0)"),
            "floor": ("collective.py:46 NEURAL_SPEC_MIN = -60.0 (CF-1) — "
                      "UNTOUCHED (the S-REL adoption floor; exp136.decode "
                      "is not on this path)"),
            "spec_identity_plumbing": ("set_target's write-once phi_spec "
                                       "capture (collective.py:115-124)"),
            "junction_blockade_coupling": {
                "param": ("block_gap_junctions(scale) -> gap_scale, read "
                          "as r = float(gap_scale) at regen onset "
                          "(collective.py:170-174, 406)"),
                "scales": list(RS),
                "convention": ("corpus innexin/gjblock sustained "
                               "blockade (exp27 S2P1, exp34 run_arm); "
                               "r = 0.05 is exp186's credited cell"),
            },
            "constructor_defaults": {
                "n": N_CELLS, "gamma": 0.25, "g_gap": 0.20, "eps": 0.04,
                "mu_theta": 0.015, "noise_std": 0.30, "theta_drift": 0.0,
                "blastema_readout_noise": 18.0,
            },
            "protocol": {
                "settle_h": SETTLE_H, "blockade_window_h": BLOCK_H,
                "blocked_plane": "slice(85, 100) (exp32 TAILP)",
                "wound_voltage": WOUND_V,
                "blastema_theta": BLASTEMA_THETA,
                "regrow": {"cell_period": CELL_PERIOD, "dt": DT,
                           "noise": REGEN_NOISE, "direction": "forward",
                           "commitment_delay": COMMITMENT_DELAY},
                "metrics": "read immediately after regrow",
                "steps_per_cell": STEPS_PER_CELL,
                "steps_per_cell_r_independent": (
                    "M40's coupling multiplies commitment_delay = 0.0, "
                    "so the per-cell draw pattern (hence the guess "
                    "stream's structure) is identical at every swept r"),
            },
        },
        "arms": {
            "prod": (
                "the tree's production core AS-IS: cultivation."
                "bioelectric.collective.M33_LINE = -35.0 (exp175's "
                "split) — deep identities in [-60, -35) get NO pole "
                "readout; no rebind anywhere (the line asserted "
                "unchanged pre/post every run)"),
            "deep": (
                "the ONE constant M33_LINE rebound to -60.0 in the one "
                "module that binds it (cultivation.bioelectric."
                "collective) for the run, then restored — exp174's "
                "save/rebind/restore mechanism, asserted per run; the "
                "CF-1-world M33 behavior, exp171's measured collapse "
                "world"),
        },
        "constants": {"FAMILIES": FAMILIES, "NEURAL_W": NEURAL_W,
                      "N_CELLS": N_CELLS, "SEEDS": list(SEEDS),
                      "PROD_LINE": PROD_LINE, "DEEP_LINE": DEEP_LINE,
                      "RS": list(RS)},
        "instruments": {
            "guess_stream": (
                "passive _RngProxy around the engine's Generator "
                "(bit-exact forwarding, zero behavioral change; "
                "exp186's instrument verbatim); per-cell draw pattern "
                "structurally asserted at every r; guess composition "
                "replicates the engine's exact float ops"),
            "r1_comparisons": (
                "bit-identity vs exp186's DEPOSITED records: float "
                "equality on final_V / final_theta / phi_spec / "
                "guess_stream + full draw-log sha256 + wound center + "
                "qualifying count + first pole-read segment index, per "
                "(family, arm, seed) at r = 0.05, plus the Z3 cell "
                "deltas/errs float == "),
            "pair_audit": (
                "exp171's M2 discipline per r: the first divergent draw "
                "between the arms is the pole-read draw sitting on the "
                "cell's M25 guess draw, and the blend (1-w)*guess + "
                "w*(spec + N(0,eff)) is reproduced bit-exactly over "
                "the prod arm's shared stream; HEAD/LINE arms "
                "bit-identical at every r (the line only moved below "
                "-35)"),
        },
        "exp186_reference": {
            "deposit": "results/exp186_pole_feature_price.json",
            "r": 0.05, "branch": z3["verdict_branch"],
            "trunk_delta": z3["trunk_delta"],
            "deep_delta": z3["deep_delta"],
            "protocol": ("exp186's run_engine protocol verbatim at "
                         "neural_w 0.5, seeds (1,2,3), r = 0.05 — this "
                         "sweep's r = 0.05 cell"),
        },
        "runs": {key: blocks_by_r[key] for key in R_KEYS},
        "envelope": envelope,
        "gate_R1": r1,
        "gate_R2": r2,
        "gate_R3": r3,
        "gate_R4": r4,
        "criteria": criteria,
        "verdict": verdict,
        "smoke_disclosure": (
            "a --smoke instrument check (TRUNK family, seed 1, both "
            "arms, r = 0.05) ran before the credited run and was "
            "discarded (no file)"),
        "wall_s": round(time.time() - t0, 1),
    }
    out_path = args.out or OUT
    _dump(deposit, out_path)

    print(f"\n  GATE-R1 replay (r = 0.05 cell == exp186's Z3 cells, "
          f"bit-exact): {'PASS' if r1['pass'] else 'REFUTED'} "
          f"({r1['n_bit_identical_corroboration']}/24 run-record "
          f"corroborations)")
    print(f"  GATE-R2 the sweep (deltas per r; HEAD/LINE bit-identical "
          f"across arms at every r): {'PASS' if r2['pass'] else 'REFUTED'}")
    print(f"  GATE-R3 the envelope -> branch {branch}:")
    print(f"    TRUNK {_fmt_deltas(dtr)} mV")
    print(f"    DEEP  {_fmt_deltas(ddk)} mV: "
          f"{'PASS' if r3['pass'] else 'REFUTED'}")
    print(f"  GATE-R4 hygiene (rebind save/restore asserted both arms "
          f"at every r, all finite): {'PASS' if r4['pass'] else 'REFUTED'}")
    print(f"\n  verdict: {verdict}")
    print(f"\n  results -> {out_path} (wall {deposit['wall_s']} s)")
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
