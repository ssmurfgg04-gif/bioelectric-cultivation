#!/usr/bin/env python3
"""exp175 — THE M33 SPLIT (one constant, one gate branch, to production).

exp171's registered next (L150): "the SPLIT — M33 needs its OWN
anterior line constant (M33_LINE = -35.0, the literature midpoint)
distinct from the S-REL adoption floor (NEURAL_SPEC_MIN = -60.0)".
exp171 priced the collapse (asymmetry ratio 0.1550 < 0.5 under CF-1's
one-constant widening); this experiment LANDS the repair in the core,
with the same bit-exact-at-old-operating-points discipline exp168 set.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Patch, audits, and gates are fixed now.

THE PATCH (ONE new constant + ONE gate-branch change, cited file:line):
  cultivation/bioelectric/collective.py
    - NEW: M33_LINE = -35.0   (the anterior/posterior literature
      midpoint: WT head -20 vs WT trunk/tail -50; the line M33's
      docstring has always described)
    - the M33 gate branch (collective.py:582) reads
      `float(spec[i]) >= M33_LINE` where it read
      `float(spec[i]) >= NEURAL_SPEC_MIN`.
  NEURAL_SPEC_MIN stays -60.0: the S-REL spec-adoption floor (the
  decode consumer exp136.decode:394) is UNCHANGED — CF-1's widened
  repertoire is untouched by this patch. Exactly one behavioral
  consumer changes (the M33 branch); the M36 misanchor branch
  (collective.py:588+) shares the anterior-eligibility question and
  is INACTIVE at defaults (mis_w = 0) — its floor is NOT changed in
  this patch and that asymmetry is disclosed (M36 keeps reading
  NEURAL_SPEC_MIN; no deposited experiment exercises M36-active).

GATES (each evaluated exactly once):

  GATE-P1 (tests green) `python3 -m tests.run_tests` from the repo
           root POST-patch exits 0 with zero failures (checked
           beforehand: no test references M33_LINE; the -35.0 in
           test_d3_semantics is a theta anchor value, unrelated).

  GATE-P2 (M33 restored to the literature line, bit-exact) exp171's
           four families re-run at neural_w = 0.5, r = 0.05, seeds
           (1, 2, 3): TRUNK/DEEP qualifying-cell counts return to 0
           and the engines' full draw logs are BIT-IDENTICAL to
           exp171's PINNED arm per (family, seed); HEAD/LINE remain
           bit-identical to both of exp171's arms (they never
           diverged); the asymmetry ratio A_patched/A_pinned under
           the SPLIT is 1.0 within float equality (the collapse is
           repaired — branch (a) of exp171's pre-named verdicts,
           now by construction).

  GATE-P3 (adoption untouched — CF-1 stands) the deep band still
           decodes: exp172's frontier rung (-60.0, instance 0,
           seeds (1,2,3)) replayed bit-exactly under the split core
           (exp136.decode reads NEURAL_SPEC_MIN, which did not
           move); exp172's shallow controls bit-exact as well.

  GATE-P4 (hygiene) pin save/restore asserted where used; zero
           non-finite values; the patch diff is exactly the two
           cited lines (git diff --stat asserted in the deposit).

NO post-hoc tuning. A --smoke instrument check (TRUNK family, seed 1)
is permitted before the credited run and discarded. The credited run
uses the committed script unchanged.

DEPOSIT: results/exp175_m33_split.json

RUN:
  python3 -m experiments.exp175_m33_split            # full
  python3 -m experiments.exp175_m33_split --smoke    # check
  python3 -m experiments.exp175_m33_split --job P2   # runner split
  # jobs: P2 | P3
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
OLD_FLOOR_PIN = -35.0          # exp171's pinned floor (the pinned arm)
NEW_FLOOR = -60.0              # CF-1, unchanged by this patch
M33_LINE = -35.0               # the NEW constant the patch introduces
NEURAL_W = 0.5
N_CELLS = 100
SEEDS = (1, 2, 3)
FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}

OUT = os.path.join(ROOT, "results", "exp175_m33_split.json")
DEP171 = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")
DEP172 = os.path.join(ROOT, "results", "exp172_deep_band_sweep.json")


class OldFloorPin:
    """exp168's mechanism, for the pinned-arm replay comparisons."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR_PIN
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


# ---- BODY (written by the run agent; gates fixed above) -------------
# Fixed BEFORE the credited run, disclosed here and in the deposit:
#   * THE PATCH (applied first, uncommitted at run time, asserted at
#     P4 straight from `git diff`): collective.py:47 adds
#     M33_LINE = -35.0 directly under NEURAL_SPEC_MIN (collective.py
#     :46, unchanged at -60.0), and the M33 gate branch (pre-patch
#     collective.py:582; 583-585 as patched) reads
#     `float(spec[i]) >= M33_LINE` where it read
#     `>= NEURAL_SPEC_MIN`. `git diff --numstat` on the file is
#     exactly 2 additions / 1 deletion. Nothing else moves; the M36
#     branch keeps its committed form (inactive at defaults,
#     mis_w = 0 — the disclosed asymmetry).
#   * ENGINE IDENTITY: run_engine is exp171_m33_widened_regime.py's
#     credited instrument, copied verbatim for this protocol (same
#     constants, same passive _RngProxy guess-stream observability,
#     same structural draw-pattern parse) so the P2 replay shares one
#     protocol with the deposit it is compared against: settle 10 h,
#     sustained blockade 24 h at r = 0.05, amputate slice(85, 100)
#     (exp32 TAILP) at wound -30 / blastema -40, regrow cell_period
#     0.8 / dt 0.1 / noise 0.6 forward, metrics read immediately.
#   * P2's replay comparisons run against exp171's DEPOSITED records
#     (DEP171): bit-identity = float equality on every recorded array
#     (final_V, final_theta, phi_spec, guess_stream) + the full
#     draw-log sha256 + wound center + qualifying count. TRUNK/DEEP
#     (the widened regime, spec < -35) are compared to the deposited
#     PINNED arm per (family, seed); HEAD/LINE (which never diverged
#     in exp171) to BOTH deposited arms. The core has not moved since
#     exp171's credited run except the two patch lines (last core
#     commit 383bba1 predates f272bef), so any mismatch is a bug.
#   * P3 uses exp172's credited machinery VERBATIM (its run_rung /
#     _record: same target construction, same OldFloorPin + g6
#     import-time-capture pin, same exp136.decode call) so the replay
#     shares one source of truth with the deposit it is compared
#     against; exp136.decode reads its own captured NEURAL_SPEC_MIN,
#     which did not move. Shallow controls first (exp172's own D4
#     execution order), then the frontier rung read from the deposit.
#   * Pin scope: on the exp171 path, cultivation.bioelectric.collective
#     was the only runtime consumer of NEURAL_SPEC_MIN, and after the
#     split it has NONE left (the M33 branch reads M33_LINE) — the
#     pinned arm is retained so the ratio clause is priced by
#     construction (OldFloorPin save/restore asserted).
import hashlib
import time

import experiments.exp172_deep_band_sweep as x172

# ---- exp171's corpus protocol constants (verbatim) ------------------
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

_DEP171 = None
_DEP172 = None


def _dep171() -> dict:
    global _DEP171
    if _DEP171 is None:
        with open(DEP171) as fh:
            _DEP171 = json.load(fh)
    return _DEP171


def _dep172() -> dict:
    global _DEP172
    if _DEP172 is None:
        with open(DEP172) as fh:
            _DEP172 = json.load(fh)
    return _DEP172


class _RngProxy:
    """Passive recording proxy around the engine's Generator.

    Forwards EVERY call to the real numpy Generator bit-exactly and
    logs (method, args, kwargs, result). Zero behavioral change — the
    engine code path is untouched; this only makes the shared stream
    observable for the GATE-P2 draw-log audits (the guess stream at
    the blocked plane). Copied from exp171's body verbatim."""

    def __init__(self, gen):
        self._gen = gen
        self.log: list = []

    def __getattr__(self, name):
        attr = getattr(self._gen, name)
        if not callable(attr):
            return attr

        def _wrapped(*args, **kwargs):
            out = attr(*args, **kwargs)
            self.log.append((name, args, tuple(sorted(kwargs.items())), out))
            return out

        return _wrapped


def _entry_digest(entry) -> bytes:
    name, args, kwargs, out = entry
    h = hashlib.sha256()
    h.update(name.encode())
    h.update(repr(args).encode())
    h.update(repr(kwargs).encode())
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


def _parse_guess_stream(seg, w: float, spec_val: float, wound_center: float,
                        eff_noise: float, brn: float):
    """Structural parse of the regrow-phase draw segment into the
    per-cell guess stream at the blocked plane. Per committed cell the
    engine's draw pattern (this protocol's knobs, all others at
    defaults) is fully determined by the source; the guess composition
    replicates the engine's exact float ops (collective.py:571-597,
    post-patch numbering). Returns (guesses, branch_taken_count,
    first_pole_read_seg_index). Copied from exp171's body verbatim."""
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


def run_engine(spec_val: float, seed: int, pinned: bool = False) -> dict:
    """exp171's run_engine protocol, verbatim: build the n=100 plane
    engine, settle, sustain junction blockade (r = gap_scale = 0.05 <
    1.0 — the M25 guess-branch precondition), amputate the exp32
    TAILP posterior plane, regrow with the M33 pole channel armed at
    NEURAL_W = 0.5. PATCHED runs the split core (M33_LINE = -35.0);
    PINNED additionally rebinds the S-REL floor constant via
    OldFloorPin (save/restore asserted) — under the SPLIT that rebind
    is inert on this path, which is exactly the P2 clause. The engine
    class is used VERBATIM; the guess stream at the blocked plane is
    recorded via the passive _RngProxy."""
    assert core.NEURAL_SPEC_MIN == NEW_FLOOR, \
        "run_engine precondition: S-REL adoption floor unchanged (CF-1)"
    assert core.M33_LINE == M33_LINE, \
        "run_engine precondition: the split core must be in the tree"
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
        # engine op (collective.py:415, post-patch), bit-identical inputs
        wound_center = float(np.mean(theta_pre[idx]))
        guesses, taken, first_nread = _parse_guess_stream(
            seg, NEURAL_W, spec_val, wound_center, EFF_NOISE,
            float(c.blastema_readout_noise))
        return {
            "spec_val": spec_val, "seed": seed,
            "neural_w": NEURAL_W, "neural_misanchor": 0.0,
            "arm": ("pinned" if pinned else "patched"),
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
        }

    if pinned:
        with OldFloorPin():
            assert core.NEURAL_SPEC_MIN == OLD_FLOOR_PIN, "pin enter failed"
            rec = _plane()
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"
        rec["pin"] = {"entered_floor": OLD_FLOOR_PIN,
                      "restore_assert_passed": True,
                      "post_restore_floor": NEW_FLOOR}
    else:
        rec = _plane()
        rec["pin"] = None
    return rec


def _vs_dep171(rec: dict, arm: str) -> dict:
    """Bit-identity of a split-core re-run against exp171's DEPOSITED
    record for (family, arm, seed): float equality on every recorded
    array + the full draw-log sha256 + wound center + qualifying
    count + first pole-read segment index."""
    fam = FAMILY_OF[rec["spec_val"]]
    dep = _dep171()["runs"][fam]["runs"][f"{arm}_s{rec['seed']}"]
    assert dep["spec_val"] == rec["spec_val"] and dep["seed"] == rec["seed"], \
        "deposit lookup mismatch"
    chk = {
        "dep171_arm": arm,
        "final_V_equal": bool(np.array_equal(
            rec["final_V"], np.asarray(dep["final_V"], dtype=float))),
        "final_theta_equal": bool(np.array_equal(
            rec["final_theta"], np.asarray(dep["final_theta"], dtype=float))),
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


def _family_job(family: str, seeds=SEEDS) -> dict:
    """P2's family replay: both arms (patched = the split core,
    pinned = OldFloorPin) per seed, with in-job bit checks — the two
    arms against EACH OTHER (the split must make the pin a no-op on
    this path) and the patched arm against exp171's deposited records
    (both arms for HEAD/LINE; the pinned arm for TRUNK/DEEP)."""
    spec_val = FAMILIES[family]
    old_regime = bool(spec_val >= OLD_FLOOR_PIN)   # HEAD/LINE
    block: dict = {"spec_val": spec_val, "neural_w": NEURAL_W,
                   "seeds": list(seeds),
                   "regime": ("old line (>= -35)" if old_regime
                              else "widened [-60, -35)"),
                   "dep171_refs": (["patched", "pinned"] if old_regime
                                   else ["pinned"]),
                   "runs": {}, "split_arm_checks": {}, "vs_dep171": {}}
    for pinned in (False, True):
        arm = "pinned" if pinned else "patched"
        for s in seeds:
            rec = run_engine(spec_val, s, pinned=pinned)
            rec["family"] = family
            block["runs"][f"{arm}_s{s}"] = rec
    for s in seeds:
        p = block["runs"][f"patched_s{s}"]
        q = block["runs"][f"pinned_s{s}"]
        eq = {
            "final_V_equal": bool(np.array_equal(p["final_V"],
                                                 q["final_V"])),
            "final_theta_equal": bool(np.array_equal(p["final_theta"],
                                                     q["final_theta"])),
            "phi_spec_equal": bool(np.array_equal(p["phi_spec"],
                                                  q["phi_spec"])),
            "guess_stream_equal": bool(np.array_equal(p["guess_stream"],
                                                      q["guess_stream"])),
            "draw_log_sha256_equal": bool(p["draw_log_sha256"]
                                          == q["draw_log_sha256"]),
            "qualifying_equal": bool(p["qualifying_cells"]
                                     == q["qualifying_cells"]),
        }
        eq["bit_identical"] = bool(all(eq.values()))
        assert eq["bit_identical"], \
            f"{family} s{s}: the split must make the pin a no-op " \
            "on the M33 path (branch (a) by construction)"
        block["split_arm_checks"][str(s)] = eq
        block["vs_dep171"][str(s)] = {
            arm: _vs_dep171(p, arm) for arm in block["dep171_refs"]}
    return block


def _m3_price(head_block: dict, trunk_block: dict) -> dict:
    """exp171's GATE-M3 formula, recomputed under the SPLIT for both
    arms: err = |guess - spec| at the blocked plane, pooled over seeds
    and committed cells; A(arm) = |mean_err(TRUNK, arm) -
    mean_err(HEAD, arm)|."""
    def pool(block: dict, arm: str) -> float:
        errs = []
        for s in SEEDS:
            rec = block["runs"][f"{arm}_s{s}"]
            errs.extend(abs(float(g) - rec["spec_val"])
                        for g in rec["guess_stream"])
        return float(np.mean(errs))

    out: dict = {"definition": (
        "A(arm) = | mean_err(TRUNK planes, arm) - mean_err(HEAD "
        "planes, arm) |, err = |guess - spec| at the blocked plane, "
        "pooled over seeds and committed cells (exp171's formula)")}
    for arm in ("patched", "pinned"):
        eh = pool(head_block, arm)
        et = pool(trunk_block, arm)
        out[f"mean_err_HEAD_{arm}"] = eh
        out[f"mean_err_TRUNK_{arm}"] = et
        out[f"A_{arm}"] = abs(et - eh)
    a_p, a_q = out["A_patched"], out["A_pinned"]
    out["asym_ratio"] = (a_p / a_q) if a_q != 0.0 else None
    dep_m3 = _dep171()["m3"]
    out["exp171_deposited"] = {k: dep_m3[k] for k in
                               ("A_pinned", "A_patched", "asym_ratio",
                                "verdict_branch")}
    return out


def _p2_job() -> tuple:
    """GATE-P2: M33 restored to the literature line, bit-exact."""
    blocks = {fam: _family_job(fam)
              for fam in ("HEAD", "LINE", "TRUNK", "DEEP")}
    m3 = _m3_price(blocks["HEAD"], blocks["TRUNK"])
    ratio = m3["asym_ratio"]

    # clause (i): the split arms are bit-identical per (family, seed)
    a_ok = all(blk["split_arm_checks"][str(s)]["bit_identical"]
               for blk in blocks.values() for s in SEEDS)

    # clause (ii): TRUNK/DEEP qualifying-cell counts return to 0 and
    # the re-run is bit-identical to exp171's deposited PINNED arm
    q0 = True
    b_ok = True
    for fam in ("TRUNK", "DEEP"):
        for s in SEEDS:
            rec = blocks[fam]["runs"][f"patched_s{s}"]
            chk = blocks[fam]["vs_dep171"][str(s)]["pinned"]
            q0 &= (rec["qualifying_cells"] == 0)
            b_ok &= bool(chk["bit_identical"])

    # clause (iii): HEAD/LINE remain bit-identical to BOTH of
    # exp171's arms (they never diverged)
    c_ok = True
    for fam in ("HEAD", "LINE"):
        for s in SEEDS:
            for arm in ("patched", "pinned"):
                c_ok &= bool(
                    blocks[fam]["vs_dep171"][str(s)][arm]["bit_identical"])

    # clause (iv): the asymmetry ratio under the SPLIT is 1.0 within
    # float equality (exp171's branch (a), now by construction)
    d_ok = bool(ratio == 1.0)

    p2 = {
        "families": {f: {"spec_val": blocks[f]["spec_val"],
                         "regime": blocks[f]["regime"],
                         "dep171_refs": blocks[f]["dep171_refs"],
                         "split_arm_checks": blocks[f]["split_arm_checks"],
                         "vs_dep171": blocks[f]["vs_dep171"],
                         "qualifying_cells": {
                             f"{arm}_s{s}":
                                 blocks[f]["runs"][f"{arm}_s{s}"]
                                 ["qualifying_cells"]
                             for arm in ("patched", "pinned")
                             for s in SEEDS}}
                     for f in blocks},
        "m3": m3,
        "clauses": {
            "split_arms_bit_identical": bool(a_ok),
            "trunk_deep_qualifying_zero": bool(q0),
            "trunk_deep_bit_identical_to_dep171_pinned": bool(b_ok),
            "head_line_bit_identical_to_both_dep171_arms": bool(c_ok),
            "asym_ratio_is_1_0": d_ok,
        },
        "pass": bool(a_ok and q0 and b_ok and c_ok and d_ok),
    }
    return blocks, p2


def _p3_job() -> dict:
    """GATE-P3: adoption untouched — the deep band still decodes.
    exp172's frontier rung (-60.0, instance 0, seeds (1, 2, 3)) and
    its shallow controls (3 rungs x 10 instances x 3 seeds) replayed
    through exp172's own credited machinery under the split core;
    every exact err must equal the deposited exact err (float
    equality) on BOTH arms, and each record's patched-vs-pinned
    relation must match the deposit's (exp136.decode reads its
    captured NEURAL_SPEC_MIN, which did not move)."""
    dep = _dep172()
    frontier = dep["gates"]["D3"]["frontier_rung"]
    assert frontier == -60.0, "unexpected deposited frontier rung"
    by_key = {(r["rung"], r["instance"], r["seed"]): r
              for r in dep["records"]}
    plan = ([(r, i) for r in x172.SHALLOW_RUNGS for i in range(x172.N_INST)]
            + [(frontier, 0)])
    rows = []
    for rung, inst in plan:            # shallow controls FIRST (exp172 D4)
        for seed in SEEDS:
            rec = x172._record(rung, inst, seed)
            dep_r = by_key[(rung, inst, seed)]
            # "replayed bit-exactly under the split core": BOTH arms
            # must reproduce the deposited exact errs (float equality)
            # AND the record's patched-vs-pinned relation must match
            # the deposit's (shallow: bit-exact equal; the deep
            # frontier rung: patched adopts while pinned refuses at
            # the canon scale — exp172's deposited D2 relation).
            vs = {
                "patched_decode": bool(
                    rec["patched"]["decode_err_exact"]
                    == dep_r["patched"]["decode_err_exact"]),
                "patched_hold": bool(
                    rec["patched"]["hold_err_exact"]
                    == dep_r["patched"]["hold_err_exact"]),
                "pinned_decode": bool(
                    rec["pinned"]["decode_err_exact"]
                    == dep_r["pinned"]["decode_err_exact"]),
                "pinned_hold": bool(
                    rec["pinned"]["hold_err_exact"]
                    == dep_r["pinned"]["hold_err_exact"]),
                "relation_matches_deposit": bool(
                    rec["bit_exact"] == dep_r["bit_exact"]),
            }
            vs["bit_exact_replay"] = bool(all(vs.values()))
            assert vs["bit_exact_replay"], \
                f"rung {rung} i{inst} s{seed}: replay != exp172 deposit"
            rows.append({
                "rung": rung, "instance": inst, "seed": seed,
                "patched": rec["patched"], "pinned": rec["pinned"],
                "vs_exp172_deposit": vs,
                "rejections": len(rec["rejected"]),
                "finite": bool(rec["finite"]),
            })
        print(f"  p3: rung {rung:6.1f} instance {inst:2d} done "
              f"({time.time() - _T0:.0f}s)", flush=True)
    shallow = [r for r in rows if r["rung"] in x172.SHALLOW_RUNGS]
    deep = [r for r in rows if r["rung"] == frontier]
    return {
        "frontier_rung": frontier,
        "plan": {"shallow_controls": [list(x172.SHALLOW_RUNGS),
                                      list(range(x172.N_INST))],
                 "frontier": [frontier, 0], "seeds": list(SEEDS),
                 "machinery": "exp172_deep_band_sweep._record/run_rung "
                              "VERBATIM (patched + pinned arms, its own "
                              "OldFloorPin + g6 pin, exp136.decode)"},
        "n_records": len(rows),
        "n_shallow": len(shallow),
        "n_frontier": len(deep),
        "all_bit_exact_vs_deposit": bool(all(
            r["vs_exp172_deposit"]["bit_exact_replay"] for r in rows)),
        "record_relation_matches_deposit": True,   # asserted above (raises)
        "zero_rejections": bool(all(r["rejections"] == 0 for r in rows)),
        "all_finite": bool(all(r["finite"] for r in rows)),
        "rows": rows,
        "pass": bool(len(shallow) == 90 and len(deep) == 3
                     and len(rows) == 93
                     and all(r["vs_exp172_deposit"]["bit_exact_replay"]
                             for r in rows)
                     and all(r["rejections"] == 0 and r["finite"]
                             for r in rows)),
    }


def _p1_job() -> dict:
    """GATE-P1: `python3 -m tests.run_tests` from the repo root,
    POST-patch, must exit 0 with zero failures."""
    pr = subprocess.run([sys.executable, "-m", "tests.run_tests"],
                        cwd=ROOT, capture_output=True, text=True)
    out = (pr.stdout or "").strip().splitlines()
    err = (pr.stderr or "").strip()
    return {"cmd": f"{sys.executable} -m tests.run_tests (cwd=repo root)",
            "exit": pr.returncode,
            "stdout_tail": "\n".join(out[-12:]),
            "stderr_tail": err[-800:],
            "pass": bool(pr.returncode == 0)}


def _p4_diff() -> dict:
    """GATE-P4's diff clause: the UNCOMMITTED patch diff must be
    exactly the two cited lines (2 additions / 1 deletion in
    cultivation/bioelectric/collective.py)."""
    numstat = subprocess.run(
        ["git", "diff", "--numstat", "--",
         "cultivation/bioelectric/collective.py"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip()
    diff = subprocess.run(
        ["git", "diff", "--", "cultivation/bioelectric/collective.py"],
        cwd=ROOT, capture_output=True, text=True).stdout
    added = [ln[1:].strip() for ln in diff.splitlines()
             if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:].strip() for ln in diff.splitlines()
               if ln.startswith("-") and not ln.startswith("---")]
    worktree = subprocess.run(
        ["git", "diff", "--numstat"], cwd=ROOT,
        capture_output=True, text=True).stdout.strip()
    two = bool(
        numstat == "2\t1\tcultivation/bioelectric/collective.py"
        and added == ["M33_LINE = -35.0",
                      "and float(spec[i]) >= M33_LINE:"]
        and removed == ["and float(spec[i]) >= NEURAL_SPEC_MIN:"])
    return {"patch_file": "cultivation/bioelectric/collective.py",
            "numstat": numstat,
            "added_lines": added,
            "removed_lines": removed,
            "two_lines_asserted": two,
            "worktree_numstat_disclosure": worktree}


def _finite_everywhere(blocks: dict, p3: dict) -> bool:
    """Zero non-finite values anywhere in the recorded state."""
    for blk in blocks.values():
        for rec in blk["runs"].values():
            for key in ("final_V", "final_theta", "phi_spec",
                        "guess_stream"):
                if not np.all(np.isfinite(rec[key])):
                    return False
            if not (np.isfinite(rec["wound_center"])
                    and np.isfinite(rec["blockade_r"])):
                return False
    return all(r["finite"] for r in p3["rows"])


def _pin_journal(blocks: dict) -> tuple:
    """Every pinned run's save/restore asserts passed; returns
    (n_pinned_runs, all_ok)."""
    n = 0
    for blk in blocks.values():
        for rec in blk["runs"].values():
            if rec["pin"] is None:
                continue
            pin = rec["pin"]
            if not (pin["entered_floor"] == OLD_FLOOR_PIN
                    and pin["restore_assert_passed"]
                    and pin["post_restore_floor"] == NEW_FLOOR):
                return n, False
            n += 1
    return n, True


def _py(o):
    """JSON-safe conversion (numpy -> python, exact float round-trip);
    transient keys (leading '_') are dropped."""
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


_T0 = 0.0


def main(args=None) -> dict:
    global _T0
    if args is None:
        args = argparse.ArgumentParser().parse_args([])
    print("=== exp175: THE M33 SPLIT (one constant, one gate branch, "
          "to production) ===")
    _T0 = time.time()
    t0 = _T0

    assert core.M33_LINE == M33_LINE and core.NEURAL_SPEC_MIN == NEW_FLOOR, \
        "working tree must carry the split (M33_LINE = -35.0, floor -60.0)"

    if args.smoke:
        # --smoke instrument check ONLY (TRUNK family, seed 1) —
        # permitted before the credited run and DISCARDED.
        blk = _family_job("TRUNK", seeds=(1,))
        dep_q = _dep171()["runs"]["TRUNK"]["runs"]["pinned_s1"][
            "qualifying_cells"]
        ok = bool(
            core.M33_LINE == M33_LINE
            and core.NEURAL_SPEC_MIN == NEW_FLOOR
            and blk["runs"]["patched_s1"]["qualifying_cells"] == 0
            and blk["runs"]["pinned_s1"]["qualifying_cells"] == 0
            and dep_q == 0
            and blk["split_arm_checks"]["1"]["bit_identical"]
            and blk["vs_dep171"]["1"]["pinned"]["bit_identical"])
        print(f"  smoke instrument check (TRUNK, seed 1): "
              f"{'OK' if ok else 'BROKEN'} — discarded (not a deposit)")
        return {"smoke": True, "discarded": True, "instrument_ok": ok}

    if args.job == "P2":
        blocks, p2 = _p2_job()
        if args.out:
            _dump({"exp": "exp175_m33_split", "partial_job": "P2",
                   "runs": blocks, "gate_P2": p2}, args.out)
            print(f"  partial job P2 -> {args.out} "
                  f"(wall {time.time() - t0:.1f} s)")
        else:
            print(f"  partial job P2: gate "
                  f"{'PASS' if p2['pass'] else 'REFUTED'} "
                  f"(no --out: not deposited)")
        return {"partial_job": "P2", "pass": p2["pass"]}

    if args.job == "P3":
        p3 = _p3_job()
        if args.out:
            _dump({"exp": "exp175_m33_split", "partial_job": "P3",
                   "gate_P3": p3}, args.out)
            print(f"  partial job P3 -> {args.out} "
                  f"(wall {time.time() - t0:.1f} s)")
        else:
            print(f"  partial job P3: gate "
                  f"{'PASS' if p3['pass'] else 'REFUTED'} "
                  f"(no --out: not deposited)")
        return {"partial_job": "P3", "pass": p3["pass"]}

    # ---- the credited FULL run --------------------------------------
    # P1 first: tests green POST-patch (the patch is in the tree).
    p1 = _p1_job()
    print(f"  p1: tests.run_tests exit {p1['exit']}")

    # P2: the four families replayed under the split core.
    blocks, p2 = _p2_job()
    print(f"  p2: ratio {p2['m3']['asym_ratio']!r} "
          f"(exp171 deposited {p2['m3']['exp171_deposited']['asym_ratio']:.4f})")

    # P3: exp172's frontier rung + shallow controls replayed bit-exact.
    p3 = _p3_job()

    # P4: hygiene — diff exactly the two cited lines, pin journal,
    # zero non-finite values.
    p4 = _p4_diff()
    n_pinned, pin_ok = _pin_journal(blocks)
    fin = _finite_everywhere(blocks, p3)
    p4["pin"] = {"pinned_runs_exp175_arm": n_pinned,
                 "pinned_runs_exp172_arm": len(p3["rows"]),
                 "save_restore_asserted": bool(pin_ok and n_pinned > 0),
                 "mechanism": ("OldFloorPin save/restore asserts (the "
                               "exp175 P2 pinned arm) + exp172's own pin "
                               "asserts inside run_rung (the P3 arm); "
                               "any violation raises")}
    p4_pass = bool(p4["two_lines_asserted"]
                   and p4["pin"]["save_restore_asserted"] and fin)

    verdict = (
        "THE M33 SPLIT LANDS IN PRODUCTION: one new constant "
        "(collective.py:47 M33_LINE = -35.0, the literature midpoint) "
        "+ one gate branch (collective.py:582, pre-patch numbering, "
        "now reads M33_LINE instead of NEURAL_SPEC_MIN) — P1 tests "
        "green POST-patch; P2 M33 is bit-exactly restored to the "
        "literature line (TRUNK/DEEP qualifying cells return to 0 and "
        "every re-run is bit-identical to exp171's deposited pinned "
        "arm; HEAD/LINE identical to both arms; the asymmetry ratio "
        f"A_patched/A_pinned = {p2['m3']['asym_ratio']!r} exactly — "
        "exp171's branch (a), now by construction); P3 "
        "adoption untouched (exp136.decode's floor did not move: "
        f"exp172's frontier rung {p3['frontier_rung']} + all 90 "
        "shallow controls replay bit-exactly with zero rejections); "
        "P4 the uncommitted diff is exactly the two cited lines with "
        "pin save/restore asserted and zero non-finite values."
        if (p1["pass"] and p2["pass"] and p3["pass"] and p4_pass) else
        "REFUTED: at least one pre-registered gate failed — see "
        "criteria.")

    deposit = {
        "exp": "exp175_m33_split",
        "title": "THE M33 SPLIT (one constant, one gate branch, "
                 "to production)",
        "pre_registered": ("docstring gates committed before any run "
                           "(006ccc9); the patch was applied first "
                           "(exactly the two cited lines, asserted from "
                           "git diff at P4) and tests run green before "
                           "the replays; the --smoke instrument check "
                           "(TRUNK, seed 1) ran first and was discarded; "
                           "this credited run used the committed gates "
                           "unchanged"),
        "patch": {
            "file": "cultivation/bioelectric/collective.py",
            "new_constant": "collective.py:47 M33_LINE = -35.0 (the "
                            "anterior/posterior literature midpoint, "
                            "directly under NEURAL_SPEC_MIN)",
            "branch": "the M33 gate branch (pre-patch collective.py:582; "
                      "583-585 as patched) reads float(spec[i]) >= "
                      "M33_LINE (was >= NEURAL_SPEC_MIN)",
            "unchanged": "NEURAL_SPEC_MIN stays -60.0 (the S-REL "
                         "spec-adoption floor; exp136.decode:394's "
                         "consumer untouched — CF-1's widened repertoire "
                         "stands); the M36 misanchor branch keeps its "
                         "committed form (INACTIVE at defaults, "
                         "mis_w = 0) — the disclosed asymmetry",
            "p4_assertion": p4,
        },
        "engine": {
            "class": "cultivation.bioelectric.collective."
                     "BioElectricCollective",
            "m33_branch": "collective.py:583-588 (post-patch; the pole "
                          "blend under r < 1.0, gated by M33_LINE)",
            "pole_channel_params": "collective.py:200-201 (regrow "
                                   "neural_readout / neural_misanchor; "
                                   "post-patch numbering)",
            "floor": "collective.py:46 NEURAL_SPEC_MIN = -60.0 (CF-1, "
                     "UNCHANGED; no runtime consumer left in "
                     "collective.py after the split)",
            "spec_identity_plumbing": "set_target's write-once phi_spec "
                                      "capture",
            "junction_blockade_coupling": {
                "param": "block_gap_junctions(scale) -> gap_scale, read "
                         "as r = float(gap_scale) at regen onset",
                "scale": BLOCKADE, "r": BLOCKADE,
                "convention": "corpus innexin/gjblock sustained "
                              "blockade (exp27 S2P1, exp34 run_arm; "
                              "exp171's deposited setting)",
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
            "patched": "the split core (M33_LINE = -35.0 gates the M33 "
                       "branch; NEURAL_SPEC_MIN = -60.0 untouched)",
            "pinned": "OldFloorPin (exp168 OLD_FLOOR_PIN semantics, "
                      "verbatim class) rebinds NEURAL_SPEC_MIN to -35.0 "
                      "with save/restore asserted — under the split "
                      "this rebind is INERT on the M33 path (the whole "
                      "point); scope = cultivation.bioelectric."
                      "collective (the only module on this path)",
            "exp172_pinned": "exp172's own run_rung pin (core + its "
                             "g6 import-time capture) used verbatim "
                             "for the P3 replay",
        },
        "constants": {"OLD_FLOOR_PIN": OLD_FLOOR_PIN, "NEW_FLOOR": NEW_FLOOR,
                      "M33_LINE": M33_LINE, "NEURAL_W": NEURAL_W,
                      "N_CELLS": N_CELLS, "SEEDS": list(SEEDS),
                      "FAMILIES": FAMILIES},
        "instruments": {
            "guess_stream": ("passive _RngProxy around the engine's "
                             "Generator (bit-exact forwarding, zero "
                             "behavioral change; exp171's instrument "
                             "verbatim); per-cell draw pattern "
                             "structurally asserted; guess composition "
                             "replicates the engine's exact float ops"),
            "p2_comparisons": ("bit-identity vs exp171's DEPOSITED "
                               "records: float equality on final_V / "
                               "final_theta / phi_spec / guess_stream + "
                               "full draw-log sha256 + wound center + "
                               "qualifying count"),
            "p3_machinery": ("exp172_deep_band_sweep._record / run_rung "
                             "VERBATIM — one source of truth with the "
                             "deposit the replay is compared against"),
        },
        "runs_replays_p2": blocks,
        "gate_P1": p1,
        "gate_P2": p2,
        "gate_P3": p3,
        "gate_P4": p4,
        "criteria": {
            "P1_tests_green_post_patch": bool(p1["pass"]),
            "P2_m33_restored_bit_exact": bool(p2["pass"]),
            "P3_adoption_untouched": bool(p3["pass"]),
            "P4_hygiene_two_line_diff": bool(p4_pass),
        },
        "verdict": verdict,
        "smoke_disclosure": "a --smoke instrument check (TRUNK family, "
                            "seed 1) ran before the credited run and "
                            "was discarded (no file)",
        "wall_s": round(time.time() - t0, 1),
    }
    out_path = args.out or OUT
    _dump(deposit, out_path)

    print(f"\n  GATE-P1 tests green POST-patch "
          f"(python3 -m tests.run_tests): "
          f"{'PASS' if p1['pass'] else 'REFUTED'}")
    print(f"  GATE-P2 M33 restored bit-exact (TRUNK/DEEP qualifying -> 0, "
          f"draw logs == exp171's pinned arm, ratio "
          f"{p2['m3']['asym_ratio']:.1f}): "
          f"{'PASS' if p2['pass'] else 'REFUTED'}")
    print(f"  GATE-P3 adoption untouched (frontier rung "
          f"{p3['frontier_rung']} + 90 shallow controls replay "
          f"bit-exact, 0 rejections): "
          f"{'PASS' if p3['pass'] else 'REFUTED'}")
    print(f"  GATE-P4 hygiene (two-line diff, pin save/restore "
          f"asserted, all finite): {'PASS' if p4_pass else 'REFUTED'}")
    print(f"\n  verdict: {verdict}")
    print(f"\n  results -> {out_path} (wall {deposit['wall_s']} s)")
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["P2", "P3", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main(args)  # noqa: F841  (body honors --smoke/--job/--out)
