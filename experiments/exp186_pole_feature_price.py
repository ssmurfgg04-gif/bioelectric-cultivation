#!/usr/bin/env python3
"""exp186 — THE POLE-FEATURE PRICE (does any substrate WANT the deep
pole readout?).

exp175's registered next (L154): with the M33 split in production
(M33_LINE = -35.0), the disclosed open question stands — "whether any
substrate WANTS pole-eligible deep identities (the -60 pole readout as
a feature)". THIS EXPERIMENT prices it as a counterfactual: substrates
at deep identities under blockade, M33 armed at the DEEP line (the
pre-split CF-1 world) vs the production line (the split world) — does
arming the pole readout at -60 HELP or HURT the substrate's identity
read?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Arms, weights, and gates are fixed now.

THE ARMS (the engine-variant mechanism, exp156's decode_cf discipline
— one constant rebound per arm, save/restore asserted):
  ARM-PROD — the production split core (M33_LINE = -35.0): deep
             identities get NO pole readout.
  ARM-DEEP — M33_LINE rebound to -60.0 in the one module that binds
             it: deep identities GET the pole readout (the CF-1-world
             M33 behavior, exp171's measured collapse world).
  THE SUBSTRATES: exp171's four identity families (HEAD -20, LINE
  -35, TRUNK -50, DEEP -60) at neural_w = 0.5, r = 0.05, seeds
  (1, 2, 3) — exp171's protocol verbatim, now with the SPLIT core.
  THE PRICE: per family, err = |guess - spec| at the blocked plane
  pooled over seeds, arm-PROD vs arm-DEEP; the FEATURE question is
  the SIGN of (err_DEEP - err_PROD) on the TRUNK/DEEP families:
  negative = the deep pole readout HELPS (a feature worth arming);
  positive = it HURTS (the split is not just literature-faithful,
  it is substrate-correct).

GATES (each evaluated exactly once):
  GATE-Z1 (production replay) ARM-PROD reproduces exp175's P2
           records bit-exactly (the four families, seeds (1,2,3):
           TRUNK/DEEP == exp171's pinned arm, HEAD/LINE unchanged).
  GATE-Z2 (the counterfactual is live) ARM-DEEP differs from
           ARM-PROD on TRUNK/DEEP (the pole branch fires; the
           first divergent step reproduces the M33 blend exactly,
           exp171's M2 discipline) and is BIT-IDENTICAL on
           HEAD/LINE (the line only moved below -35).
  GATE-Z3 (the price) per family the signed delta deposited; the
           verdict branch pre-named: HELP iff BOTH TRUNK and DEEP
           deltas < 0; HURT iff BOTH > 0; MIXED otherwise. All
           three branches complete the gate.
  GATE-Z4 (hygiene) rebind save/restore asserted both arms; zero
           non-finite values.

NO post-hoc tuning. --smoke (TRUNK, seed 1, both arms) permitted,
discarded. Deposit: results/exp186_pole_feature_price.json
Jobs: prod | deep
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

import cultivation.bioelectric.collective as core  # noqa: E402

FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}
NEURAL_W = 0.5
N_CELLS = 100
SEEDS = (1, 2, 3)
PROD_LINE = -35.0
DEEP_LINE = -60.0

OUT = os.path.join(ROOT, "results", "exp186_pole_feature_price.json")
DEP171 = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")
DEP175 = os.path.join(ROOT, "results", "exp175_m33_split.json")


def main() -> dict:
    # Thread pins (defensive; the corpus discipline — the credited runs
    # this deposit is compared against ran with BLAS threading at 1).
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    import hashlib  # noqa: F401  (digest helpers below)
    import time

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["prod", "deep", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()  # sys.argv — the pre-registered __main__ CLI
    t0 = time.time()
    print("=== exp186: THE POLE-FEATURE PRICE (does any substrate WANT "
          "the deep pole readout?) ===")

    # ---- working-tree preconditions (the production split core) ----
    assert core.NEURAL_SPEC_MIN == -60.0, \
        "precondition: the S-REL adoption floor is CF-1 (-60.0), untouched"
    assert core.M33_LINE == PROD_LINE, \
        "precondition: the production split core (M33_LINE = -35.0) " \
        "must be in the tree"

    # ---- deposited references --------------------------------------
    with open(DEP175) as fh:
        dep175 = json.load(fh)
    p2 = dep175["runs_replays_p2"]
    with open(DEP171) as fh:
        dep171 = json.load(fh)

    # ---- exp171/exp175's corpus protocol constants (verbatim) ------
    DT = 0.1                       # corpus integration step
    SETTLE_H = 10.0                # make_collective settle window (exp27)
    BLOCK_H = 24.0                 # sustained-blockade window (exp27 innexin)
    BLOCKADE = 0.05                # block_gap_junctions scale -> r = 0.05
    BLOCKED_PLANE = slice(85, 100)  # exp32 TAILP — the posterior blocked plane
    CELL_PERIOD = 0.8              # corpus regen cell period
    REGEN_NOISE = 0.6              # corpus commitment noise
    COMMITMENT_DELAY = 0.0         # M40 off (default)
    WOUND_V = -30.0                # corpus amputation protocol
    BLASTEMA_THETA = -40.0         # corpus amputation protocol
    STEPS_PER_CELL = max(1, int(round(
        CELL_PERIOD * (1.0 + COMMITMENT_DELAY * (1.0 - BLOCKADE)) / DT)))  # = 8
    REGEN_CELLS = len(np.arange(N_CELLS)[BLOCKED_PLANE])   # = 15
    EFF_NOISE = REGEN_NOISE * 1.0  # noise * commitment_noise_scale (default)
    FAMILY_OF = {v: k for k, v in FAMILIES.items()}

    class _RngProxy:
        """Passive recording proxy around the engine's Generator.

        Forwards EVERY call to the real numpy Generator bit-exactly and
        logs (method, args, kwargs, result). Zero behavioral change —
        the engine code path is untouched; this only makes the shared
        stream observable for the Z1/Z2 audits (the guess stream at the
        blocked plane). Copied from exp171's body verbatim."""

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
        per-cell guess stream at the blocked plane (exp171's parser,
        verbatim). Returns (guesses, branch_taken_count,
        first_pole_read_seg_index)."""
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

    def run_engine(spec_val: float, seed: int, deep: bool = False) -> dict:
        """Build the n=100 plane engine, run under blockade, return the
        record. ARM-PROD (deep=False) is the tree's production core
        AS-IS (M33_LINE = -35.0, the exp175 split): deep identities in
        [-60, -35) get NO pole readout — no rebind anywhere, the line
        asserted unchanged pre/post run. ARM-DEEP (deep=True) rebinds
        the ONE constant core.M33_LINE to -60.0 in the one module that
        binds it (exp174's save/rebind/restore mechanism, asserted per
        run): the CF-1-world M33 behavior, exp171's measured collapse
        world. The substrate is a UNIFORM per-plane spec identity
        (set_target captures it as phi_spec — the spec identity
        plumbing); the blocked plane regenerates under sustained
        junction blockade (r = gap_scale = 0.05 < 1.0 — the M25
        guess-branch precondition) with the M33 pole channel armed at
        NEURAL_W. exp171's run_engine protocol verbatim; the engine
        class is used VERBATIM; the guess stream at the blocked plane
        is recorded via the passive _RngProxy."""
        assert core.NEURAL_SPEC_MIN == -60.0, \
            "run_engine precondition: the S-REL floor must be untouched"
        spec_val = float(spec_val)

        def _plane() -> dict:
            c = core.BioElectricCollective(n=N_CELLS, seed=seed)
            proxy = _RngProxy(c.rng)
            c.rng = proxy
            c.set_target(np.full(N_CELLS, spec_val))   # phi_spec: uniform plane
            c.run(SETTLE_H, dt=DT)
            c.block_gap_junctions(BLOCKADE)            # r = 0.05 (the setting)
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
        """ARM-DEEP (p) vs ARM-PROD (q) per (family, seed): the Z2
        audit — GATE-Z2's bit-identity clause above the line, or the
        live-counterfactual clauses with exp171's M2 blend discipline
        (the first divergent step reproduces the M33 blend exactly)."""
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
                f"{p['family']}: the line only moved below -35 — " \
                "HEAD/LINE arms must be bit-identical"
            return chk
        # GATE-Z2: the counterfactual is live — ARM-DEEP must DIFFER,
        # the split must be the pole branch itself, and the blend must
        # reproduce exactly (exp171's M2 discipline).
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

    def _vs_dep175(rec: dict) -> dict:
        """GATE-Z1's bit-identity of an ARM-PROD re-run against
        exp175's DEPOSITED P2 record for (family, seed): float equality
        on every recorded array + the full draw-log sha256 + wound
        center + qualifying count + first pole-read segment index."""
        fam = FAMILY_OF[rec["spec_val"]]
        dep = p2[fam]["runs"][f"patched_s{rec['seed']}"]
        assert dep["spec_val"] == rec["spec_val"] \
            and dep["seed"] == rec["seed"], "deposit lookup mismatch"
        chk = {
            "dep175_record": f"runs_replays_p2.{fam}.runs."
                             f"patched_s{rec['seed']}",
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
        }
        chk["bit_identical"] = bool(all(v for k, v in chk.items()
                                        if k.endswith("_equal")))
        return chk

    def _dep_pair_check(d_rec: dict, deep_regime: bool) -> dict:
        """--job deep's Z2 audit: the FRESH ARM-DEEP run against
        exp175's DEPOSITED production records (the prod reference —
        GATE-Z1 establishes those records bit-exact). HEAD/LINE: the
        deposited record must be reproduced bit-exactly (the line only
        moved below -35). TRUNK/DEEP: the counterfactual must be live
        (differ, qualifying 0 -> >0) with the blend reproduced
        bit-exactly from the deep arm's own shared stream, and the
        deposited prod guess reconstructed exactly from it."""
        fam = FAMILY_OF[d_rec["spec_val"]]
        dep = p2[fam]["runs"][f"patched_s{d_rec['seed']}"]
        assert dep["spec_val"] == d_rec["spec_val"] \
            and dep["seed"] == d_rec["seed"], "deposit lookup mismatch"
        if not deep_regime:
            chk = _vs_dep175(d_rec)
            assert chk["bit_identical"], \
                f"{fam} s{d_rec['seed']}: ARM-DEEP must be bit-identical " \
                "to the deposited production record above the line"
            return chk
        chk = {
            "dep175_record": f"runs_replays_p2.{fam}.runs."
                             f"patched_s{d_rec['seed']}",
            "final_V_differs": not bool(np.array_equal(
                d_rec["final_V"], np.asarray(dep["final_V"], dtype=float))),
            "guess_stream_differs": not bool(np.array_equal(
                d_rec["guess_stream"],
                np.asarray(dep["guess_stream"], dtype=float))),
            "draw_log_sha256_differs": bool(d_rec["draw_log_sha256"]
                                            != dep["draw_log_sha256"]),
            "wound_center_equal": bool(d_rec["wound_center"]
                                       == dep["wound_center"]),
            "qualifying_dep_prod": dep["qualifying_cells"],
            "qualifying_deep": d_rec["qualifying_cells"],
        }
        assert dep["qualifying_cells"] == 0 and d_rec["qualifying_cells"] > 0, \
            "pole-branch take counts do not match the deep-eligibility clause"
        assert chk["final_V_differs"] and chk["guess_stream_differs"] \
            and chk["draw_log_sha256_differs"] and chk["wound_center_equal"], \
            "ARM-DEEP must differ from the deposited production record"
        seg = d_rec["_seg"]
        sd = d_rec["first_pole_read_seg_index"]
        assert sd is not None and seg[sd][0] == "normal" \
            and seg[sd][1] == (0.0, EFF_NOISE), \
            "first pole read is not a pole-read draw"
        assert seg[sd - 1][0] == "normal" \
            and seg[sd - 1][1] == (0.0, d_rec["blastema_readout_noise"]), \
            "the pole-read draw does not sit on the cell's M25 guess draw"
        draw_shared = float(seg[sd - 1][3])
        nread_val = float(seg[sd][3])
        expected = (1.0 - d_rec["neural_w"]) \
            * (d_rec["wound_center"] + draw_shared) \
            + d_rec["neural_w"] * (d_rec["spec_val"] + nread_val)
        dep_prod_guess0 = float(np.asarray(dep["guess_stream"],
                                           dtype=float)[0])
        chk["first_divergent_step"] = {
            "in_regen_segment": True,
            "cell_index": BLOCKED_PLANE.start,
            "shared_guess_draw_from_deep_stream": draw_shared,
            "pole_read_draw": nread_val,
            "expected_guess": expected,
            "deep_guess": float(d_rec["guess_stream"][0]),
            "dep175_prod_guess": dep_prod_guess0,
            "shared_stream_reconstruction_matches_deposit": bool(
                d_rec["wound_center"] + draw_shared == dep_prod_guess0),
            "blend_bit_exact": bool(expected
                                    == float(d_rec["guess_stream"][0])),
        }
        assert chk["first_divergent_step"]["blend_bit_exact"], \
            "first divergent step must reproduce the M33 blend exactly"
        assert chk["first_divergent_step"][
            "shared_stream_reconstruction_matches_deposit"], \
            "the deep arm's shared stream must reconstruct the deposited " \
            "production guess exactly"
        return chk

    def _family_job(family: str, seeds=SEEDS) -> dict:
        """Both arms per seed on one identity family, with in-job Z2
        pair checks (the credited all-run / smoke evaluator)."""
        spec_val = FAMILIES[family]
        deep_regime = bool(NEURAL_W > 0.0 and spec_val < PROD_LINE)
        block: dict = {
            "spec_val": spec_val, "neural_w": NEURAL_W,
            "seeds": list(seeds),
            "regime": ("deep pole eligibility (spec < -35: the CF-1-world "
                       "M33 branch fires under ARM-DEEP only)"
                       if deep_regime else
                       "production line (spec >= -35: both arms fire the "
                       "pole branch identically)"),
            "runs": {}, "pair_checks": {}}
        for arm, deep in (("prod", False), ("deep", True)):
            for s in seeds:
                rec = run_engine(spec_val, s, deep=deep)
                rec["family"] = family
                block["runs"][f"{arm}_s{s}"] = rec
        for s in seeds:
            block["pair_checks"][str(s)] = _pair_check(
                block["runs"][f"deep_s{s}"],
                block["runs"][f"prod_s{s}"], deep_regime)
        _strip(block)
        return block

    def _arm_job(family: str, seeds=SEEDS, deep: bool = False) -> dict:
        """One arm per seed on one identity family (the runner-split
        partial jobs; checks are evaluated by the gate functions).
        Transients are kept until the job's gate checks have run
        (--job deep's Z2 audit reads the deep arm's _seg)."""
        block: dict = {"spec_val": FAMILIES[family], "neural_w": NEURAL_W,
                       "seeds": list(seeds), "runs": {}}
        for s in seeds:
            rec = run_engine(FAMILIES[family], s, deep=deep)
            rec["family"] = family
            block["runs"][f"{'deep' if deep else 'prod'}_s{s}"] = rec
        return block

    def _pool_errs_runs(fam_block: dict, arm: str) -> float:
        errs = []
        for s in SEEDS:
            rec = fam_block["runs"][f"{arm}_s{s}"]
            errs.extend(abs(float(g) - rec["spec_val"])
                        for g in rec["guess_stream"])
        return float(np.mean(errs))

    def _pool_errs_dep(fam: str) -> float:
        errs = []
        for s in SEEDS:
            dep = p2[fam]["runs"][f"patched_s{s}"]
            errs.extend(abs(float(g) - dep["spec_val"])
                        for g in dep["guess_stream"])
        return float(np.mean(errs))

    def _make_price(err_prod: dict, err_deep: dict,
                    prod_source: str) -> dict:
        """GATE-Z3: per family the signed delta deposited; the verdict
        branch pre-named: HELP iff BOTH TRUNK and DEEP deltas < 0; HURT
        iff BOTH > 0; MIXED otherwise. All three branches complete the
        gate."""
        fams = {}
        for fam in FAMILIES:
            ep, ed = err_prod[fam], err_deep[fam]
            fams[fam] = {"err_PROD": ep, "err_DEEP": ed,
                         "delta_err_DEEP_minus_PROD": ed - ep}
        dtk = fams["TRUNK"]["delta_err_DEEP_minus_PROD"]
        ddk = fams["DEEP"]["delta_err_DEEP_minus_PROD"]
        branch = ("HELP" if (dtk < 0.0 and ddk < 0.0)
                  else ("HURT" if (dtk > 0.0 and ddk > 0.0) else "MIXED"))
        return {
            "definition": ("per family: err = |guess - spec| at the "
                           "blocked plane, pooled over seeds and "
                           "committed cells (exp171's pool formula); "
                           "the signed price is delta = err_DEEP - "
                           "err_PROD; HELP iff BOTH TRUNK and DEEP "
                           "deltas < 0 (the deep pole readout is a "
                           "feature worth arming); HURT iff BOTH > 0 "
                           "(the split is substrate-correct); MIXED "
                           "otherwise — all three branches complete "
                           "the gate"),
            "err_PROD_source": prod_source,
            "units": "mV (|guess - spec| at the blocked plane)",
            "families": fams,
            "trunk_delta": dtk, "deep_delta": ddk,
            "verdict_branch": branch,
            "head_line_deltas_exactly_zero": bool(
                fams["HEAD"]["delta_err_DEEP_minus_PROD"] == 0.0
                and fams["LINE"]["delta_err_DEEP_minus_PROD"] == 0.0),
        }

    def _gate_z1(blocks: dict) -> dict:
        comps = {fam: {str(s): _vs_dep175(blocks[fam]["runs"][f"prod_s{s}"])
                       for s in SEEDS} for fam in FAMILIES}
        n_ok = sum(1 for fam in comps for s in comps[fam]
                   if comps[fam][s]["bit_identical"])
        corrob: dict = {}
        corrob_ok = True
        for fam in FAMILIES:
            corrob[fam] = {}
            for s in SEEDS:
                sha = blocks[fam]["runs"][f"prod_s{s}"]["draw_log_sha256"]
                arms = (("pinned",) if fam in ("TRUNK", "DEEP")
                        else ("patched", "pinned"))
                corrob[fam][str(s)] = {
                    a: bool(sha == dep171["runs"][fam]["runs"]
                            [f"{a}_s{s}"]["draw_log_sha256"])
                    for a in arms}
                corrob_ok &= all(corrob[fam][str(s)].values())
        return {
            "source": ("results/exp175_m33_split.json runs_replays_p2 — "
                       "exp175's credited P2 replay records (arm "
                       "'patched' = the production split core, already "
                       "verified there bit-exact vs exp171: TRUNK/DEEP "
                       "== exp171's pinned arm, HEAD/LINE unchanged)"),
            "comparisons": comps,
            "n_bit_identical": n_ok, "n_records": 12,
            "exp171_corroboration": corrob,
            "clauses": {
                "prod_bit_identical_to_dep175_p2": bool(n_ok == 12),
                "exp171_corroboration_shas": bool(corrob_ok),
            },
            "pass": bool(n_ok == 12 and corrob_ok),
        }

    def _gate_z2_all(blocks: dict) -> dict:
        fams = {fam: blocks[fam]["pair_checks"] for fam in FAMILIES}
        head_line_ok = all(fams[f][str(s)]["bit_identical"]
                           for f in ("HEAD", "LINE") for s in SEEDS)
        live_ok = True
        for f in ("TRUNK", "DEEP"):
            for s in SEEDS:
                chk = fams[f][str(s)]
                live_ok &= bool(
                    chk["final_V_differs"]
                    and chk["qualifying_cells_deep"] > 0
                    and chk["qualifying_cells_prod"] == 0
                    and chk["first_divergent_step"]["blend_bit_exact"])
        return {
            "families": fams,
            "reference": ("both arms run fresh in this process; the "
                          "prod side is separately GATE-Z1-verified "
                          "bit-exact vs exp175's deposited P2 records"),
            "clauses": {
                "trunk_deep_counterfactual_live": bool(live_ok),
                "head_line_bit_identical": bool(head_line_ok),
            },
            "pass": bool(live_ok and head_line_ok),
        }

    def _gate_z2_dep(blocks_deep: dict) -> dict:
        fams = {fam: {str(s): _dep_pair_check(
                          blocks_deep[fam]["runs"][f"deep_s{s}"],
                          FAMILIES[fam] < PROD_LINE)
                      for s in SEEDS} for fam in FAMILIES}
        head_line_ok = all(fams[f][str(s)].get("bit_identical", False)
                           for f in ("HEAD", "LINE") for s in SEEDS)
        live_ok = True
        for f in ("TRUNK", "DEEP"):
            for s in SEEDS:
                chk = fams[f][str(s)]
                live_ok &= bool(
                    chk["final_V_differs"] and chk["qualifying_deep"] > 0
                    and chk["qualifying_dep_prod"] == 0
                    and chk["first_divergent_step"]["blend_bit_exact"]
                    and chk["first_divergent_step"]
                    ["shared_stream_reconstruction_matches_deposit"])
        return {
            "families": fams,
            "reference": ("exp175's deposited P2 records "
                          "(runs_replays_p2, arm 'patched') as the prod "
                          "reference — GATE-Z1's source of truth"),
            "clauses": {
                "trunk_deep_counterfactual_live": bool(live_ok),
                "head_line_bit_identical": bool(head_line_ok),
            },
            "pass": bool(live_ok and head_line_ok),
        }

    def _gate_z4(all_recs: list, price: dict) -> dict:
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
        finite_ok &= all(np.isfinite(price["families"][f][k])
                         for f in FAMILIES
                         for k in ("err_PROD", "err_DEEP",
                                   "delta_err_DEEP_minus_PROD"))
        return {
            "deep_rebind_save_rebind_restore_asserted": f"{deep_ok}/12",
            "prod_no_rebind_line_unchanged_asserted": f"{prod_ok}/12",
            "zero_non_finite": bool(finite_ok),
            "pass": bool(deep_ok == 12 and prod_ok == 12 and finite_ok),
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

    # ---- --smoke: instrument check ONLY, permitted and DISCARDED ----
    if args.smoke:
        blk = _family_job("TRUNK", seeds=(1,))
        chk = _vs_dep175(blk["runs"]["prod_s1"])
        pc = blk["pair_checks"]["1"]
        ok = bool(
            chk["bit_identical"]
            and pc["final_V_differs"]
            and pc["qualifying_cells_deep"] == REGEN_CELLS
            and pc["qualifying_cells_prod"] == 0
            and pc["first_divergent_step"]["blend_bit_exact"])
        print(f"  smoke instrument check (TRUNK, seed 1, both arms): "
              f"{'OK' if ok else 'BROKEN'} — discarded (not a deposit)")
        return {"smoke": True, "discarded": True, "instrument_ok": ok}

    # ---- --job prod: ARM-PROD only (runner split; GATE-Z1) ----------
    if args.job == "prod":
        blocks = {fam: _arm_job(fam, deep=False) for fam in FAMILIES}
        z1 = _gate_z1(blocks)
        for blk in blocks.values():
            _strip(blk)
        print(f"  partial job prod: GATE-Z1 production replay "
              f"{z1['n_bit_identical']}/12 bit-exact vs exp175's P2 "
              f"records -> {'PASS' if z1['pass'] else 'REFUTED'}")
        if args.out:
            _dump({"exp": "exp186_pole_feature_price",
                   "partial_job": "prod", "runs": blocks,
                   "gate_Z1": z1}, args.out)
            print(f"  partial job prod -> {args.out} "
                  f"(wall {time.time() - t0:.1f} s)")
        else:
            print("  (no --out: not deposited)")
        return {"partial_job": "prod", "gate_Z1_pass": z1["pass"]}

    # ---- --job deep: ARM-DEEP only (runner split; Z2/Z3 vs deposit) -
    if args.job == "deep":
        blocks = {fam: _arm_job(fam, deep=True) for fam in FAMILIES}
        z2 = _gate_z2_dep(blocks)
        err_prod = {fam: _pool_errs_dep(fam) for fam in FAMILIES}
        err_deep = {fam: _pool_errs_runs(blocks[fam], "deep")
                    for fam in FAMILIES}
        price = _make_price(
            err_prod, err_deep,
            "exp175's deposited P2 records (runs_replays_p2, arm "
            "'patched') — the GATE-Z1 source of truth")
        z3_pass = bool(all(np.isfinite(price["families"][f][k])
                           for f in FAMILIES
                           for k in ("err_PROD", "err_DEEP",
                                     "delta_err_DEEP_minus_PROD"))
                       and price["verdict_branch"]
                       in ("HELP", "HURT", "MIXED"))
        for blk in blocks.values():
            _strip(blk)
        print(f"  partial job deep: GATE-Z2 counterfactual live "
              f"{'PASS' if z2['pass'] else 'REFUTED'}; GATE-Z3 branch "
              f"{price['verdict_branch']} (TRUNK "
              f"{price['trunk_delta']:+.4f}, DEEP "
              f"{price['deep_delta']:+.4f} mV)")
        if args.out:
            _dump({"exp": "exp186_pole_feature_price",
                   "partial_job": "deep", "runs": blocks,
                   "gate_Z2": z2, "gate_Z3": price}, args.out)
            print(f"  partial job deep -> {args.out} "
                  f"(wall {time.time() - t0:.1f} s)")
        else:
            print("  (no --out: not deposited)")
        return {"partial_job": "deep", "gate_Z2_pass": z2["pass"],
                "branch": price["verdict_branch"]}

    # ---- the credited FULL run (both arms, gates Z1-Z4) --------------
    blocks = {fam: _family_job(fam) for fam in FAMILIES}
    all_recs = [rec for fam in FAMILIES
                for rec in blocks[fam]["runs"].values()]

    # GATE-Z1: ARM-PROD reproduces exp175's P2 records bit-exactly
    z1 = _gate_z1(blocks)

    # GATE-Z2: the counterfactual is live (TRUNK/DEEP diverge + blend
    # bit-exact; HEAD/LINE bit-identical — the line only moved below -35)
    z2 = _gate_z2_all(blocks)

    # GATE-Z3: the price (signed deltas + the pre-named branch)
    err_prod = {fam: _pool_errs_runs(blocks[fam], "prod")
                for fam in FAMILIES}
    err_deep = {fam: _pool_errs_runs(blocks[fam], "deep")
                for fam in FAMILIES}
    price = _make_price(
        err_prod, err_deep,
        "this run's ARM-PROD records (GATE-Z1: bit-identical to "
        "exp175's deposited P2 records)")
    z3_pass = bool(all(np.isfinite(price["families"][f][k])
                       for f in FAMILIES
                       for k in ("err_PROD", "err_DEEP",
                                 "delta_err_DEEP_minus_PROD"))
                   and price["verdict_branch"] in ("HELP", "HURT", "MIXED"))

    # GATE-Z4: hygiene (rebind save/restore asserted both arms; zero
    # non-finite values anywhere)
    z4 = _gate_z4(all_recs, price)

    criteria = {
        "Z1_production_replay": z1["pass"],
        "Z2_counterfactual_live": z2["pass"],
        "Z3_price_branch": z3_pass,
        "Z4_hygiene": z4["pass"],
    }
    all_pass = bool(all(criteria.values()))
    branch = price["verdict_branch"]
    dtk, ddk = price["trunk_delta"], price["deep_delta"]
    branch_text = {
        "HELP": ("the deep pole readout is a FEATURE worth arming: both "
                 "deep-eligible families read their identity BETTER "
                 "with the pole readout armed at -60 (deltas < 0) — the "
                 "production split leaves substrate value on the table"),
        "HURT": ("the split is not just literature-faithful, it is "
                 "substrate-correct: both deep-eligible families read "
                 "their identity WORSE with the pole readout armed at "
                 "-60 (deltas > 0)"),
        "MIXED": ("the families disagree: the deep pole readout is a "
                  "feature for one deep-eligible family and a cost for "
                  "the other — the -35 line is doing real work either "
                  "way"),
    }[branch]
    verdict = (
        f"THE POLE-FEATURE PRICE IS IN (branch {branch}): TRUNK delta "
        f"{dtk:+.4f} mV, DEEP delta {ddk:+.4f} mV pooled |guess - spec| "
        "err at the blocked plane (negative = the -60 pole readout "
        f"HELPS the substrate's identity read). {branch_text} "
        f"GATE-Z1 production replay {z1['n_bit_identical']}/12 "
        "bit-exact vs exp175's deposited P2 records (TRUNK/DEEP == "
        "exp171's pinned arm, HEAD/LINE unchanged); GATE-Z2 the "
        "counterfactual is live — ARM-DEEP diverges from ARM-PROD on "
        "TRUNK/DEEP with the first divergent step reproducing the M33 "
        "blend bit-exactly over the prod arm's shared stream, and is "
        "bit-identical on HEAD/LINE (the line only moved below -35); "
        "GATE-Z4 rebind save/restore asserted 12/12 (deep) + 12/12 "
        "(prod line unchanged), zero non-finite values."
        if all_pass else
        "REFUTED: at least one pre-registered gate failed — see "
        "criteria.")

    deposit = {
        "exp": "exp186_pole_feature_price",
        "title": "THE POLE-FEATURE PRICE (does any substrate WANT the "
                 "deep pole readout?)",
        "pre_registered": (
            "docstring gates committed before any run (357faa4, "
            "batch-4 pre-registrations); the --smoke instrument check "
            "(TRUNK, seed 1, both arms) ran first and was discarded; "
            "this credited run used the committed script unchanged"),
        "engine": {
            "class": "cultivation.bioelectric.collective."
                     "BioElectricCollective",
            "m33_branch": ("collective.py:583-587 (the pole blend under "
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
                                       "capture (collective.py:115-123)"),
            "junction_blockade_coupling": {
                "param": ("block_gap_junctions(scale) -> gap_scale, read "
                          "as r = float(gap_scale) at regen onset "
                          "(collective.py:169-173, 405)"),
                "scale": BLOCKADE, "r": BLOCKADE,
                "convention": ("corpus innexin/gjblock sustained "
                               "blockade (exp27 S2P1, exp34 run_arm)"),
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
                      "PROD_LINE": PROD_LINE, "DEEP_LINE": DEEP_LINE},
        "instruments": {
            "guess_stream": (
                "passive _RngProxy around the engine's Generator "
                "(bit-exact forwarding, zero behavioral change; "
                "exp171's instrument verbatim); per-cell draw pattern "
                "structurally asserted; guess composition replicates "
                "the engine's exact float ops"),
            "z1_comparisons": (
                "bit-identity vs exp175's DEPOSITED P2 records: float "
                "equality on final_V / final_theta / phi_spec / "
                "guess_stream + full draw-log sha256 + wound center + "
                "qualifying count + first pole-read segment index"),
            "z2_blend_discipline": (
                "exp171's M2 discipline: the first divergent draw "
                "between the arms is the pole-read draw sitting on the "
                "cell's M25 guess draw, and the blend (1-w)*guess + "
                "w*(spec + N(0,eff)) is reproduced bit-exactly over "
                "the prod arm's shared stream"),
        },
        "runs": blocks,
        "gate_Z1": z1,
        "gate_Z2": z2,
        "gate_Z3": price,
        "gate_Z4": z4,
        "criteria": criteria,
        "verdict": verdict,
        "smoke_disclosure": (
            "a --smoke instrument check (TRUNK family, seed 1, both "
            "arms) ran before the credited run and was discarded (no "
            "file)"),
        "wall_s": round(time.time() - t0, 1),
    }
    out_path = args.out or OUT
    _dump(deposit, out_path)

    print(f"\n  GATE-Z1 production replay (ARM-PROD == exp175's P2, "
          f"12 records): {'PASS' if z1['pass'] else 'REFUTED'} "
          f"({z1['n_bit_identical']}/12 bit-exact)")
    print(f"  GATE-Z2 the counterfactual is live (TRUNK/DEEP diverge + "
          f"blend bit-exact; HEAD/LINE bit-identical): "
          f"{'PASS' if z2['pass'] else 'REFUTED'}")
    print(f"  GATE-Z3 the price -> branch {branch}: TRUNK {dtk:+.4f} mV, "
          f"DEEP {ddk:+.4f} mV: {'PASS' if z3_pass else 'REFUTED'}")
    print(f"  GATE-Z4 hygiene (rebind save/restore asserted both arms, "
          f"all finite): {'PASS' if z4['pass'] else 'REFUTED'}")
    print(f"\n  verdict: {verdict}")
    print(f"\n  results -> {out_path} (wall {deposit['wall_s']} s)")
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["prod", "deep", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
