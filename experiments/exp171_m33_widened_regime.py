#!/usr/bin/env python3
"""exp171 — M33'S NEW [-60, -35) REGIME (first exercise + audit).

exp168's registered next (L146): "the M33 gate's new [-60, -35) regime
(collective.py:366/584) is unexercised by any deposited experiment —
its first use should carry its own bit-exact-at-old-operating-points
audit". CF-1 widened NEURAL_SPEC_MIN from -35.0 to -60.0 for the
S-REL spec-adoption floor; the SAME constant gates the core's M33
non-junctional neural/muscle polarity readout (neural_readout > 0.0,
junction blockade r < 1.0, spec[i] >= NEURAL_SPEC_MIN). No deposited
experiment has ever set neural_readout > 0 — this is the FIRST.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Arms, weights, and gates are fixed now.

WHAT CHANGED SEMANTICALLY (named before the run): M33's comment fixes
the old line at "the fate-axis midpoint between the WT head identity
(-20 mV) and the WT trunk/tail identity (-50 mV)" — i.e. -35.0 was the
ANTERIOR/POSTERIOR literature line (posterior identities have no local
pole; recorded GJ-blockade phenotypes concentrate at posterior planes,
innexin|tail 0.67 vs innexin|head 0.00). The widened floor RECLASSIFIES
every identity in [-60, -35) — including the -50 trunk/tail identity —
as ANTERIOR-ELIGIBLE for the pole readout. This may be exactly right
(deeper anterior identities exist) or exactly wrong (the trunk plane's
junction-carried phenomenology is the literature asymmetry M33
encodes). The experiment does not presuppose either: it prices the
reclassification and deposits the asymmetry ratio.

INSTRUMENTS (zero new calibration):
  * The core engine VERBATIM: the M33 branch at collective.py:582
    (`neural_w > 0.0 and spec is not None and 0 <= i < n and
    float(spec[i]) >= NEURAL_SPEC_MIN`), the constructor's
    neural_readout / neural_misanchor parameters (line 199), and the
    junction-blockade coupling parameter that drives r < 1.0 (the
    guess branch's precondition; read from the engine's constructor —
    M33 is inert at full coupling r >= 1.0 and at neural_w = 0).
  * Substrates: four identity families, values from the WT/literature
    ladder — HEAD -20.0, LINE -35.0 (the old boundary), TRUNK -50.0,
    DEEP -60.0 — as uniform per-plane spec identities on n=100
    engines, seeds (1, 2, 3) per family.
  * THE TWO ARMS (the audit IS the design):
      PATCHED — the working tree's CF-1 floor NEURAL_SPEC_MIN = -60.0.
      PINNED  — exp168's OLD_FLOOR_PIN mechanism rebinding the ONE
                constant to -35.0 (save/restore asserted) in every
                module that captured it at import time.
    neural_w = 0.5 (pre-registered, the blend midpoint — zero
    fitting), one blockade setting (the engine's default reduced-
    coupling configuration, recorded in the deposit), no other knobs.
  * The sweep ladder over neural_w is FORBIDDEN (one weight only).

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-M1 (bit-exact audit above the old line) HEAD/LINE families
           (identities >= -35.0): patched vs pinned are BIT-IDENTICAL
           per (family, seed) — final V, committed phi_spec, and the
           guess stream at the blocked plane (float equality). The
           patch must be invisible where it was already active.
  GATE-M2 (the new regime is live) TRUNK/DEEP families (identities
           in [-60, -35)): patched differs from pinned under the
           same settings — qualifying-cell count > 0 (cells whose
           spec >= -60 and < -35 that now take the pole branch);
           the FIRST divergent step reproduces the M33 blend exactly:
           guess_patched = (1 - w) * guess_base + w * (spec + draw)
           with guess_base and draw taken from the pinned arm's
           shared stream (the divergence point is the branch itself).
  GATE-M3 (the asymmetry price — the literature clause) the head/tail
           blockade asymmetry under the pole readout:
             A(arm) = | mean_err(TRUNK planes, arm) -
                       mean_err(HEAD planes, arm) |
           where err = |guess - spec| at the blocked plane, pooled
           over seeds. Deposited: A_pinned, A_patched, and the ratio
           A_patched / A_pinned. The gate RECORDS the ratio with two
           pre-named verdict branches (no post-hoc reading):
             (a) ratio >= 0.5 — the asymmetry SURVIVES the widened
                 floor; CF-1 stands as ONE constant (the pole readout
                 is identity-anchored, not line-anchored, at this
                 weight).
             (b) ratio < 0.5 — the asymmetry COLLAPSES toward the
                 patched floor's eligibility; the split is REGISTERED
                 (M33 needs its own anterior line, distinct from the
                 S-REL adoption floor) as the experiment's registered
                 next.
           Either branch is a completed deposit; the gate passes on
           the RECORD being complete, not on which branch fires.
  GATE-M4 (inertia + hygiene) neural_readout = 0.0 runs: patched ==
           pinned bit-identically on ALL four families (the inert-at-
           default clause, whole-sweep); pin save/restore asserted;
           zero non-finite values anywhere.

NO post-hoc knob tuning; exactly ONE neural_w. A --smoke instrument
check (HEAD + TRUNK families, seed 1 only) is permitted before the
credited run and discarded; the credited full run uses the committed
script unchanged.

DEPOSIT: results/exp171_m33_widened_regime.json

RUN:
  python3 -m experiments.exp171_m33_widened_regime           # full
  python3 -m experiments.exp171_m33_widened_regime --smoke   # check
  python3 -m experiments.exp171_m33_widened_regime --family TRUNK
  # jobs: HEAD | LINE | TRUNK | DEEP | inertia
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
FAMILIES = {"HEAD": -20.0, "LINE": -35.0, "TRUNK": -50.0, "DEEP": -60.0}
NEURAL_W = 0.5                 # the ONE weight, pre-registered
N_CELLS = 100
SEEDS = (1, 2, 3)
OLD_FLOOR = -35.0              # exp168's pre-patch value
NEW_FLOOR = -60.0              # exp168's CF-1 value (the working tree)
ASYM_RATIO_SPLIT = 0.5         # the pre-named verdict branch point

OUT = os.path.join(ROOT, "results", "exp171_m33_widened_regime.json")


class OldFloorPin:
    """exp168's OLD_FLOOR_PIN mechanism, verbatim semantics."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


# ---- BODY (written by the run agent; gates fixed above) -------------
# Fixed BEFORE the credited run, disclosed here and in the deposit:
#   * ENGINE IDENTITY (the pre-registered instruments, read from the
#     source): the physics class is cultivation.bioelectric.collective.
#     BioElectricCollective (constructor collective.py:68 — the
#     junction-blockade coupling is `block_gap_junctions(scale)` ->
#     gap_scale, read as r = float(self.gap_scale) at regen onset,
#     collective.py:169-173/405; the spec identity plumbing is
#     set_target's write-once phi_spec capture, collective.py:115-123;
#     the M33 pole-channel parameters are regrow's neural_readout /
#     neural_misanchor, collective.py:199-200; the M33 branch is
#     collective.py:582-587; the floor is collective.py:46).
#   * BLOCKADE SETTING (the one reduced-coupling configuration, the
#     corpus default, recorded in the deposit): block_gap_junctions(
#     0.05) -> r = 0.05 < 1.0 — the innexin/gjblock arms' sustained
#     blockade of exp27 S2P1 / exp34 run_arm. g_gap keeps its
#     constructor default 0.20.
#   * PROTOCOL (exp27/exp31/exp32/exp34 discipline, zero new
#     calibration): settle 10 h (make_collective), sustained blockade
#     24 h (innexin_sustained), amputate the exp32 TAILP posterior
#     plane slice(85, 100) at wound -30 / blastema -40, regrow
#     cell_period 0.8 dt 0.1 noise 0.6 forward, metrics read
#     immediately after regrow. No post-regen window, no other knobs.
#   * THE GUESS STREAM at the blocked plane is made observable by a
#     PASSIVE recording proxy around the engine's Generator (forwards
#     every call bit-exactly; the engine code path is untouched). The
#     per-cell draw pattern under this protocol is fully determined by
#     the source: [2*steps_per_cell standard_normal(n)] (step noise +
#     drift) + normal(0, eff_noise) (commitment noise) + normal(0,
#     blastema_readout_noise) (the M25 guess draw) + [normal(0,
#     eff_noise)] iff the pole branch is taken (M33 or M36). guess_base
#     = wound_center = mean(theta[idx]) at regen onset (collective.py
#     :414) — the parse replicates the engine's exact float ops.
#   * M2's blend check is executed BIT-EXACTLY through the whole
#     engine by a replay instrument built ONLY from the docstring's
#     declared parameters (neural_readout / neural_misanchor, line
#     199): the M36 mis-anchored pole run (neural_misanchor=1.0) at
#     the PINNED floor. On a uniform plane spec[0] == spec[i], so the
#     M36 composition (1.0 - w*1.0)*guess + w*1.0*(spec[0] + N(0,
#     eff)) is float-identical arithmetic to the M33 blend (1.0 - w)*
#     guess + w*(spec[i] + N(0, eff)) over the same shared stream —
#     replay bit-identity with the patched run proves the first
#     divergent step (and every step) reproduces the M33 blend
#     exactly, with guess_base/draw from the pinned arm's stream.
#   * The pin scope here is cultivation.bioelectric.collective ONLY:
#     the M33 branch reads the module global at call time and this
#     experiment imports no other module that captures the constant
#     (exp136/exp156 are not on this path).
import time

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

BRANCH_TEXTS = {
    "a": ("the asymmetry SURVIVES the widened floor; CF-1 stands as "
          "ONE constant (the pole readout is identity-anchored, not "
          "line-anchored, at this weight)"),
    "b": ("the asymmetry COLLAPSES toward the patched floor's "
          "eligibility; the split is REGISTERED (M33 needs its own "
          "anterior line, distinct from the S-REL adoption floor) as "
          "the experiment's registered next"),
}


class _RngProxy:
    """Passive recording proxy around the engine's Generator.

    Forwards EVERY call to the real numpy Generator bit-exactly and
    logs (method, args, kwargs, result). Zero behavioral change — the
    engine code path is untouched; this only makes the shared stream
    observable for the GATE-M1/M2 audits (the guess stream at the
    blocked plane)."""

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


def _log_first_diff(a: list, b: list) -> int:
    """Index of the first non-bit-identical entry; -1 if identical."""
    n = min(len(a), len(b))
    for i in range(n):
        if a[i][0] != b[i][0] or _entry_digest(a[i]) != _entry_digest(b[i]):
            return i
    return -1 if len(a) == len(b) else n


def _parse_guess_stream(seg, w: float, spec_val: float, wound_center: float,
                        eff_noise: float, brn: float):
    """Structural parse of the regrow-phase draw segment into the
    per-cell guess stream at the blocked plane. Per committed cell the
    engine's draw pattern (this protocol's knobs, all others at
    defaults) is fully determined by the source; the guess composition
    replicates the engine's exact float ops (collective.py:570-596).
    Returns (guesses, branch_taken_count, first_pole_read_seg_index)."""
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
        # the M33 (or, on the uniform-plane replay, M36) blend.
        g = wound_center + draw
        if nread is not None:
            g = (1.0 - w) * g + w * (spec_val + nread)
        guesses.append(g)
    assert pos == len(seg), \
        f"regen segment tail unconsumed: {pos} != {len(seg)}"
    return guesses, taken, first_nread


def run_engine(spec_val: float, seed: int, neural_w: float,
               pinned: bool = False, neural_misanchor: float = 0.0):
    """Build the n=100 plane engine, run under blockade, return the
    record. The substrate is a UNIFORM per-plane spec identity
    (set_target captures it as phi_spec — the spec identity plumbing);
    the blocked plane regenerates under sustained junction blockade
    (r = gap_scale = 0.05 < 1.0 — the M25 guess-branch precondition)
    with the M33 pole channel armed at `neural_w`, the corpus innexin
    protocol otherwise. PINNED rebinds the ONE constant via OldFloorPin
    (save/restore asserted); PATCHED runs the working tree's CF-1
    floor. The engine class is used VERBATIM; the guess stream at the
    blocked plane is recorded via the passive _RngProxy."""
    assert core.NEURAL_SPEC_MIN == NEW_FLOOR, \
        "run_engine precondition: working tree must be at the CF-1 floor"
    spec_val = float(spec_val)
    neural_w = float(neural_w)
    mis_w = float(neural_misanchor)
    if mis_w > 0.0:
        assert pinned, "the M36 replay instrument runs at the PINNED floor"

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
                 neural_readout=neural_w, neural_misanchor=mis_w)
        k1 = len(proxy.log)
        seg = proxy.log[k0:k1]
        idx = list(np.arange(N_CELLS)[BLOCKED_PLANE])
        # engine op (collective.py:414), bit-identical inputs
        wound_center = float(np.mean(theta_pre[idx]))
        guesses, taken, first_nread = _parse_guess_stream(
            seg, neural_w, spec_val, wound_center, EFF_NOISE,
            float(c.blastema_readout_noise))
        return {
            "spec_val": spec_val, "seed": seed,
            "neural_w": neural_w, "neural_misanchor": mis_w,
            "arm": ("replay_m36" if mis_w > 0.0 else
                    ("pinned" if pinned else "patched")),
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

    if pinned:
        with OldFloorPin():
            assert core.NEURAL_SPEC_MIN == OLD_FLOOR, "pin enter failed"
            rec = _plane()
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"
        rec["pin"] = {"entered_floor": OLD_FLOOR,
                      "restore_assert_passed": True,
                      "post_restore_floor": NEW_FLOOR}
    else:
        rec = _plane()
        rec["pin"] = None
    return rec


def _pair_check(p: dict, q: dict, new_regime: bool) -> dict:
    """PATCHED vs PINNED per (family, seed): the M1/M4 bit-identity
    audit (old-line + inert pairs) or the M2 live-regime split."""
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
    if not new_regime:
        assert chk["bit_identical"], \
            "old-line/inert pair must be bit-identical (float equality)"
        return chk
    # GATE-M2: the new regime is live — patched must DIFFER, the split
    # must be the branch itself, and the blend must reproduce exactly.
    chk["final_V_differs"] = not v_eq
    chk["qualifying_cells_patched"] = p["qualifying_cells"]
    chk["qualifying_cells_pinned"] = q["qualifying_cells"]
    assert p["qualifying_cells"] > 0 and q["qualifying_cells"] == 0, \
        "pole-branch take counts do not match the [-60, -35) clause"
    assert chk["final_V_differs"] and not chk["bit_identical"], \
        "patched must differ from pinned in the new regime"
    assert d >= p["_k0"], "streams diverged before the regen segment"
    sd = d - p["_k0"]
    seg = p["_seg"]
    assert seg[sd][0] == "normal" and seg[sd][1] == (0.0, EFF_NOISE), \
        "first divergence is not a pole-read draw"
    assert seg[sd - 1][0] == "normal" \
        and seg[sd - 1][1] == (0.0, p["blastema_readout_noise"]), \
        "the pole-read draw does not sit on the cell's M25 guess draw"
    draw_shared = float(seg[sd - 1][3])   # bit-equal in the pinned log
    nread_val = float(seg[sd][3])
    expected = (1.0 - p["neural_w"]) * (p["wound_center"] + draw_shared) \
        + p["neural_w"] * (p["spec_val"] + nread_val)
    chk["first_divergent_step"] = {
        "in_regen_segment": True,
        "cell_index": BLOCKED_PLANE.start,
        "shared_guess_draw_from_pinned_stream": draw_shared,
        "pole_read_draw": nread_val,
        "expected_guess": expected,
        "patched_guess": float(p["guess_stream"][0]),
        "pinned_guess": float(q["guess_stream"][0]),
        "blend_bit_exact": bool(expected == float(p["guess_stream"][0])),
    }
    assert chk["first_divergent_step"]["blend_bit_exact"], \
        "first divergent step must reproduce the M33 blend exactly"
    return chk


def _replay_check(p: dict, rp: dict) -> dict:
    """M2's blend reproduction, bit-exact through the whole engine:
    the pinned-floor M36 mis-anchored pole replay must be bit-identical
    to the patched M33 run (uniform plane => spec[0] == spec[i], so the
    M36 composition is float-identical arithmetic to the M33 blend)."""
    ok = bool(np.array_equal(p["final_V"], rp["final_V"])
              and np.array_equal(p["final_theta"], rp["final_theta"])
              and np.array_equal(p["phi_spec"], rp["phi_spec"])
              and np.array_equal(p["guess_stream"], rp["guess_stream"])
              and p["draw_log_sha256"] == rp["draw_log_sha256"])
    assert ok, "M36-misanchor replay must be bit-identical to the M33 run"
    return {"replay_bit_identical": True,
            "instrument": ("pinned-floor M36 mis-anchored pole run "
                           "(neural_misanchor=1.0); on a uniform plane "
                           "spec[0] == spec[i], so its composition is "
                           "float-identical arithmetic to the M33 blend "
                           "(1-w)*guess + w*(spec + N(0, eff)) over the "
                           "same shared stream")}


def _family_job(family: str, seeds=SEEDS, neural_w: float = NEURAL_W) -> dict:
    """Both arms (plus the M2 replay instrument where the new regime is
    live) on one identity family; in-job bit-level pair checks."""
    spec_val = FAMILIES[family]
    new_regime = bool(neural_w > 0.0 and spec_val < OLD_FLOOR)
    block: dict = {"spec_val": spec_val, "neural_w": float(neural_w),
                   "seeds": list(seeds),
                   "regime": ("new [-60, -35)" if new_regime
                              else "old line (>= -35)"),
                   "runs": {}, "pair_checks": {},
                   "replay_runs": {}, "replay_checks": {}}
    for arm, pinned in (("patched", False), ("pinned", True)):
        for s in seeds:
            rec = run_engine(spec_val, s, neural_w, pinned=pinned)
            rec["family"] = family
            block["runs"][f"{arm}_s{s}"] = rec
    for s in seeds:
        p = block["runs"][f"patched_s{s}"]
        q = block["runs"][f"pinned_s{s}"]
        block["pair_checks"][str(s)] = _pair_check(p, q, new_regime)
    if new_regime:
        for s in seeds:
            rp = run_engine(spec_val, s, neural_w, pinned=True,
                            neural_misanchor=1.0)
            rp["family"] = family
            block["replay_runs"][str(s)] = rp
            block["replay_checks"][str(s)] = _replay_check(
                block["runs"][f"patched_s{s}"], rp)
    for rec in list(block["runs"].values()) \
            + list(block["replay_runs"].values()):
        for k in ("_log", "_seg", "_k0", "_k1"):
            rec.pop(k, None)
    return block


def _inertia_job(seeds=SEEDS) -> dict:
    """GATE-M4's whole-sweep inert clause: neural_w = 0.0 on all four
    families, both arms, bit-identity everywhere."""
    block: dict = {"neural_w": 0.0, "clause": (
        "neural_readout = 0.0 short-circuits the M33 test before the "
        "floor is read — patched == pinned bit-identically on ALL "
        "families"), "families": {}}
    for fam in FAMILIES:
        block["families"][fam] = _family_job(fam, seeds=seeds, neural_w=0.0)
    return block


def _m3_price(head_block: dict, trunk_block: dict) -> dict:
    """GATE-M3: the head/tail blockade asymmetry under the pole
    readout. err = |guess - spec| at the blocked plane, pooled over
    seeds; A(arm) = |mean_err(TRUNK, arm) - mean_err(HEAD, arm)|."""
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
        "pooled over seeds and committed cells")}
    for arm in ("pinned", "patched"):
        eh = pool(head_block, arm)
        et = pool(trunk_block, arm)
        out[f"mean_err_HEAD_{arm}"] = eh
        out[f"mean_err_TRUNK_{arm}"] = et
        out[f"A_{arm}"] = abs(et - eh)
    a_p, a_q = out["A_patched"], out["A_pinned"]
    ratio = (a_p / a_q) if a_q != 0.0 else None
    out["asym_ratio"] = ratio
    branch = "b" if (ratio is None or ratio < ASYM_RATIO_SPLIT) else "a"
    out["verdict_branch"] = branch
    out["branch_text"] = BRANCH_TEXTS[branch]
    out["split"] = ASYM_RATIO_SPLIT
    return out


def _finite_everywhere(*blocks: dict) -> bool:
    """Zero non-finite values anywhere in the recorded state."""
    def recs(block: dict):
        for fam_block in block.values():
            for rec in fam_block["runs"].values():
                yield rec
            for rec in fam_block.get("replay_runs", {}).values():
                yield rec

    for block in blocks:
        for rec in recs(block):
            for key in ("final_V", "final_theta", "phi_spec",
                        "guess_stream"):
                if not np.all(np.isfinite(rec[key])):
                    return False
            if not (np.isfinite(rec["wound_center"])
                    and np.isfinite(rec["blockade_r"])):
                return False
    return True


def _pin_journal_ok(*blocks: dict) -> bool:
    """Every pinned run's save/restore asserts passed."""
    def pinned_recs(block: dict):
        for fam_block in block.values():
            for rec in fam_block["runs"].values():
                if rec["pin"] is not None:
                    yield rec
            for rec in fam_block.get("replay_runs", {}).values():
                if rec["pin"] is not None:
                    yield rec

    n = 0
    for block in blocks:
        for rec in pinned_recs(block):
            pin = rec["pin"]
            if not (pin["entered_floor"] == OLD_FLOOR
                    and pin["restore_assert_passed"]
                    and pin["post_restore_floor"] == NEW_FLOOR):
                return False
            n += 1
    return n > 0


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


def main(args=None) -> dict:
    if args is None:
        ap = argparse.ArgumentParser()
        ap.add_argument("--smoke", action="store_true")
        ap.add_argument("--job", choices=["HEAD", "LINE", "TRUNK", "DEEP",
                                          "inertia", "all"], default="all")
        ap.add_argument("--out", default=None)
        args = ap.parse_args()

    print("=== exp171: M33's new [-60, -35) regime "
          "(first exercise + audit) ===")
    t0 = time.time()

    if args.smoke:
        # --smoke instrument check ONLY (HEAD + TRUNK, seed 1) —
        # permitted before the credited run and DISCARDED.
        head = _family_job("HEAD", seeds=(1,))
        trunk = _family_job("TRUNK", seeds=(1,))
        ok = bool(head["pair_checks"]["1"]["bit_identical"]
                  and trunk["pair_checks"]["1"]["bit_identical"] is False
                  and trunk["pair_checks"]["1"]["final_V_differs"]
                  and trunk["pair_checks"]["1"]["qualifying_cells_patched"]
                  == REGEN_CELLS
                  and trunk["replay_checks"]["1"]["replay_bit_identical"])
        print(f"  smoke instrument check (HEAD+TRUNK, seed 1): "
              f"{'OK' if ok else 'BROKEN'} — discarded (not a deposit)")
        return {"smoke": True, "discarded": True, "instrument_ok": ok}

    if args.job in FAMILIES:
        blk = _family_job(args.job)
        out_path = args.out or os.path.join(
            ROOT, "results", f"exp171_m33_widened_regime_{args.job}.json")
        _dump({"exp": "exp171_m33_widened_regime",
               "partial_job": args.job, "block": blk}, out_path)
        print(f"  partial job {args.job} -> {out_path} "
              f"(wall {time.time() - t0:.1f} s)")
        return {"partial_job": args.job, "path": out_path, "block": blk}

    if args.job == "inertia":
        blk = _inertia_job()
        out_path = args.out or os.path.join(
            ROOT, "results", "exp171_m33_widened_regime_inertia.json")
        _dump({"exp": "exp171_m33_widened_regime",
               "partial_job": "inertia", "block": blk}, out_path)
        print(f"  partial job inertia -> {out_path} "
              f"(wall {time.time() - t0:.1f} s)")
        return {"partial_job": "inertia", "path": out_path, "block": blk}

    # ---- the credited FULL run --------------------------------------
    blocks = {fam: _family_job(fam)
              for fam in ("HEAD", "LINE", "TRUNK", "DEEP")}
    inertia = _inertia_job()

    # GATE-M1: bit-exact audit above the old line (HEAD/LINE)
    m1 = bool(all(blocks[f]["pair_checks"][str(s)]["bit_identical"]
                  for f in ("HEAD", "LINE") for s in SEEDS))

    # GATE-M2: the new regime is live (TRUNK/DEEP)
    m2_clauses = []
    for f in ("TRUNK", "DEEP"):
        for s in SEEDS:
            chk = blocks[f]["pair_checks"][str(s)]
            m2_clauses.append(
                chk["qualifying_cells_patched"] > 0
                and chk["qualifying_cells_pinned"] == 0
                and chk["final_V_differs"]
                and chk["first_divergent_step"]["blend_bit_exact"]
                and blocks[f]["replay_checks"][str(s)]
                ["replay_bit_identical"])
    m2 = bool(all(m2_clauses))

    # GATE-M3: the asymmetry price (record completeness + branch)
    m3 = _m3_price(blocks["HEAD"], blocks["TRUNK"])
    ratio = m3["asym_ratio"]
    m3_ok = bool(np.isfinite(m3["A_pinned"]) and np.isfinite(m3["A_patched"])
                 and (ratio is None or np.isfinite(ratio))
                 and m3["verdict_branch"] in BRANCH_TEXTS)

    # GATE-M4: inertia + hygiene
    m4 = bool(all(inertia["families"][f]["pair_checks"][str(s)]
                  ["bit_identical"] for f in FAMILIES for s in SEEDS)
              and _pin_journal_ok(blocks, inertia["families"])
              and _finite_everywhere(blocks, inertia["families"]))

    verdict = (
        "M33's new [-60, -35) regime is EXERCISED and PRICED: the CF-1 "
        "floor is bit-invisible above the old line (M1), live below it "
        "with the first divergent step reproducing the M33 blend "
        "bit-exactly over the pinned arm's shared stream (M2), the "
        "head/tail blockade asymmetry under the pole readout is priced "
        f"A_pinned={m3['A_pinned']:.4f}, A_patched={m3['A_patched']:.4f}, "
        f"ratio={m3['asym_ratio']:.4f} -> pre-named branch "
        f"({m3['verdict_branch']}): {m3['branch_text']} (M3), and the "
        "channel is inert at neural_readout=0 across the whole sweep "
        "with the pin save/restore asserted and zero non-finite values "
        "anywhere (M4)." if (m1 and m2 and m3_ok and m4) else
        "REFUTED: at least one pre-registered gate failed — see "
        "criteria.")

    deposit = {
        "exp": "exp171_m33_widened_regime",
        "title": "M33's new [-60, -35) regime (first exercise + audit)",
        "pre_registered": ("docstring gates committed before any run; "
                           "the --smoke instrument check (HEAD+TRUNK, "
                           "seed 1) ran first and was discarded; this "
                           "credited run used the committed script "
                           "unchanged"),
        "engine": {
            "class": "cultivation.bioelectric.collective."
                     "BioElectricCollective",
            "m33_branch": "collective.py:582-587 (walk: the pole blend "
                          "under r < 1.0)",
            "pole_channel_params": "collective.py:199-200 (regrow "
                                   "neural_readout / neural_misanchor)",
            "floor": "collective.py:46 NEURAL_SPEC_MIN = -60.0 (CF-1)",
            "spec_identity_plumbing": "set_target's write-once phi_spec "
                                      "capture (collective.py:115-123)",
            "junction_blockade_coupling": {
                "param": "block_gap_junctions(scale) -> gap_scale, read "
                         "as r = float(gap_scale) at regen onset "
                         "(collective.py:169-173, 405)",
                "scale": BLOCKADE, "r": BLOCKADE,
                "convention": "corpus innexin/gjblock sustained "
                              "blockade (exp27 S2P1, exp34 run_arm)",
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
            "patched": "working tree CF-1 floor NEURAL_SPEC_MIN = -60.0",
            "pinned": "OldFloorPin (exp168 OLD_FLOOR_PIN semantics) "
                      "rebinds the ONE constant to -35.0; save/restore "
                      "asserted; scope = cultivation.bioelectric."
                      "collective (the only runtime consumer on this "
                      "path)",
        },
        "constants": {"FAMILIES": FAMILIES, "NEURAL_W": NEURAL_W,
                      "N_CELLS": N_CELLS, "SEEDS": list(SEEDS),
                      "OLD_FLOOR": OLD_FLOOR, "NEW_FLOOR": NEW_FLOOR,
                      "ASYM_RATIO_SPLIT": ASYM_RATIO_SPLIT},
        "instruments": {
            "guess_stream": ("passive _RngProxy around the engine's "
                             "Generator (bit-exact forwarding, zero "
                             "behavioral change); per-cell draw pattern "
                             "structurally asserted; guess composition "
                             "replicates the engine's exact float ops"),
            "m2_blend_replay": ("pinned-floor M36 mis-anchored pole run "
                                "(neural_misanchor=1.0, a docstring-"
                                "declared parameter); uniform plane => "
                                "spec[0] == spec[i] => float-identical "
                                "arithmetic to the M33 blend"),
        },
        "runs": blocks,
        "inertia": inertia,
        "m3": m3,
        "criteria": {
            "M1_bit_exact_above_old_line": m1,
            "M2_new_regime_live": m2,
            "M3_asymmetry_price_recorded": m3_ok,
            "M4_inertia_hygiene": m4,
        },
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1),
    }
    out_path = args.out or OUT
    _dump(deposit, out_path)

    print(f"\n  GATE-M1 bit-exact above the old line (HEAD/LINE):    "
          f"{'PASS' if m1 else 'REFUTED'}")
    print(f"  GATE-M2 the new regime is live (TRUNK/DEEP, branch-split "
          f"+ replay): {'PASS' if m2 else 'REFUTED'}")
    print(f"  GATE-M3 asymmetry price: A_pinned {m3['A_pinned']:.4f}, "
          f"A_patched {m3['A_patched']:.4f}, ratio "
          f"{m3['asym_ratio']:.4f} -> branch ({m3['verdict_branch']}): "
          f"{'PASS' if m3_ok else 'REFUTED'}")
    print(f"  GATE-M4 inertia + hygiene (w=0 whole sweep, pin "
          f"asserted, all finite): {'PASS' if m4 else 'REFUTED'}")
    print(f"\n  verdict: {verdict}")
    print(f"\n  results -> {out_path} (wall {deposit['wall_s']} s)")
    return deposit


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["HEAD", "LINE", "TRUNK", "DEEP",
                                      "inertia", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main(args)  # body honors --smoke/--job/--out
