#!/usr/bin/env python3
"""exp169 — R_T SCOPED (the per-media diagnostic exp167 registered).

exp167's deposit (L147) falsified the BLANKET R_T adoption clause for
the temporal read: the flip-quiet window silences exactly the channel
(TC1's F) that carries exp148's schedule semantics — the corner's
excess and the battery's signal are the SAME channel, so one zero-knob
clause cannot buy both (A2 FAIL 0/12 separated; fidelity +0.005 only).
The deposit registered the scoping: "R_T per-media via a PRE-REGISTERED
diagnostic in the style of PN1's rho (threshold fixed from deposited
boundaries BEFORE decoding, zero per-instance tuning): the flip clock's
CONCENTRATION". THIS EXPERIMENT runs that diagnostic.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Gates, statistic, and threshold are fixed
now; the credited run uses this file unchanged.

THE DIAGNOSTIC (zero knobs, computable from the medium alone):
  f_max(medium) = max over directed edges (i, j) of the per-edge
  presence-transition count across the read window (the TC1 raw
  flip-clock matrix's max entry; FrameSeq/flip_clock_matrix machinery,
  exp148 verbatim). For PAIRED constructions (exp148's FlipPairMedium
  families) the unit of scoping is the PAIR: f_max(pair) = max over the
  two schedule members — a scoped read must use ONE arm per pair or the
  N2 contrast is an instrument artifact, not a schedule readout.
  THE RULE: apply R_T (exp167's adopted read) iff f_max < 32.0;
  otherwise keep exp148's RAW temporal read. One threshold, no
  per-instance tuning, no outcome feedback.

THE THRESHOLD — fixed from the DEPOSITED empty gap before this file
  was written (both bounds recomputed and asserted at run time):
  * diffuse class (R_T side): exp166's corner spot media (cell 7,
    j = 0..9) and clean media (cell 0, j = 0..9) — exp167's deposit
    records raw f_max in [5, 7] (scoping_candidate text).
  * concentrated class (raw side): exp148's 12 battery pairs —
    f_aper per chord edge up to ~1248, minimum member-max across the
    24 deposited members >= 1165 (results/exp167_rt_adopted.json
    battery.pairs f_per/f_aper lists; every f_per entry is 2 but the
    PAIR-JOINT max is the f_aper scale — the pair is the unit).
  * 32.0 sits in the deposited gap (7, 1165): >= 4x above the diffuse
    ceiling, >= 36x below the concentrated floor. The grid instances'
    f_max values are NOT part of the gap derivation — classifying them
    is the diagnostic's prediction work (gate S4).

INSTRUMENTS (zero new calibration):
  * exp148's module verbatim: FAMILIES, LADDER, SCHED_SEED,
    GRID_BASE_SEED, GRID_CLASSES, N_INSTANCES, N_INSTANCES_400,
    FlipPairMedium, FlipGridMedium, FrameSeq, flip_clock_matrix,
    read_temporal, exp148_decode, outcome_key, verdict_blind, and the
    constants N3_BAR 0.60 / N2_MIN_SEPARATION 10 / N1_MIN_BLIND 11;
    seeds (1, 2, 3).
  * exp167's module verbatim: RTMasked (the adopted medium wrapper),
    its decode dispatch, CORNER_CELL 7 / CLEAN_CELL 0 / SPOT_J / 
    SPOT_SEEDS.
  * Deposits read at run time: results/exp148_temporal_read.json,
    results/exp166_leading_edge.json, results/exp167_rt_adopted.json
    (errs at execute_signed's 2-dp precision; replay = exact float
    equality on the records).
  * INSTRUMENT PIN (exp167's mechanism, disclosed pre-run): both
    replay references predate CF-1, so NEURAL_SPEC_MIN is pinned to
    -35.0 in every module whose bound name the read chain consults
    (cultivation.bioelectric.collective, exp142, exp145, exp148,
    exp94) — restored-world semantics, save/restore asserted.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-S1 (threshold validity) recomputed f_max reproduces the
           deposited classes: all 20 corner/clean spot media
           f_max < 32.0; all 12 battery pair-joint f_max >= 32.0;
           the recomputed per-chord counts match the deposit's
           f_per/f_aper lists exactly (instrument replay); the
           corner spot raw projection errs replay exp167's A3
           inputs bit-exactly (the wrapper changes nothing raw).
           PASS = all clauses.
  GATE-S2 (raw where concentrated) the scoped read on the 12
           battery pairs IS exp148's raw temporal read bit-exactly:
           per-pair verdicts and errs identical to the deposited
           temporal records; N2 separation 12/12 and N1 blindness
           12/12 reproduced. (The diagnostic keeps the schedule
           channel wherever it lives.)
  GATE-S3 (R_T where diffuse) the scoped read on the corner spot
           set IS exp167's adopted read bit-exactly: corner
           (cell 7) errs == exp167's A3 errs_adopted (median 0.535,
           20/20 media replay), clean cell (cell 0) bit-identical
           to exp166's clean arm-A (the no-op clause).
  GATE-S4 (the grid prediction + no-regression) the schedule grid
           under the scoped read: per-instance f_max and class
           deposited BEFORE the pooled verdict; zero rejections;
           scoped pooled median <= 0.685 (exp148's deposited
           temporal median — no fidelity regression); the scoped
           cross-class outcome-identity count deposited and
           strictly below exp167's blanket 30/30 whenever at least
           one instance classifies concentrated (the schedule
           channel survives there). No bar on HOW many grid
           instances classify which way — that is the prediction.

NO post-hoc knob tuning; exactly ONE threshold. Whatever the outcome,
it is deposited. A --smoke instrument check (1 pair, 1 grid instance,
corner j=0, clean j=0) is permitted before the credited run and
discarded; the credited full run uses the committed script unchanged.

DEPOSIT: results/exp169_rt_scoping.json

RUN:
  python3 -m experiments.exp169_rt_scoping                 # full
  python3 -m experiments.exp169_rt_scoping --smoke         # check
  python3 -m experiments.exp169_rt_scoping --job battery   # runner split
  # jobs: threshold | battery | corner | grid
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

from experiments.exp148_temporal_read import (  # noqa: E402
    FAMILIES, FlipGridMedium, FlipPairMedium, FrameSeq, GRID_BASE_SEED,
    GRID_CLASSES, LADDER, N1_MIN_BLIND, N2_MIN_SEPARATION, N3_BAR,
    N_INSTANCES, N_INSTANCES_400, SCHED_SEED,
    decode as exp148_decode, flip_clock_matrix, outcome_key,
    read_temporal, verdict_blind,
)
from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE,
)
from experiments.exp167_rt_adopted import (  # noqa: E402
    RTMasked, CORNER_CELL, CLEAN_CELL, SPOT_J, SPOT_SEEDS,
    decode as exp167_decode,
)

# ---- INSTRUMENT PIN (see docstring) --------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP148_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP148_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


# ---- THE DIAGNOSTIC (fixed) ----------------------------------------
THRESHOLD = 32.0            # the deposited gap (7, 1165)

OUT = os.path.join(ROOT, "results", "exp169_rt_scoping.json")
DEP148 = os.path.join(ROOT, "results", "exp148_temporal_read.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")
DEP167 = os.path.join(ROOT, "results", "exp167_rt_adopted.json")


def f_max_frames(frames: list[np.ndarray]) -> float:
    """Max per-edge presence-transition count across the window."""
    trans = np.zeros_like(frames[0], dtype=np.int64)
    for a, b in zip(frames[:-1], frames[1:]):
        trans += ((np.abs(b) > 0).astype(np.int64)
                  - (np.abs(a) > 0).astype(np.int64) != 0)
    return float(trans.max()) if trans.size else 0.0


def scoped_read(medium, seed: int, fmax: float, return_state: bool = False):
    """THE RULE: R_T iff f_max < THRESHOLD, else exp148's raw temporal."""
    if fmax < THRESHOLD:
        return exp167_decode("adopted", medium, seed,
                             return_state=return_state)
    return exp148_decode("temporal", medium, seed,
                         return_state=return_state)


# ------------------------------------------------------------ harness
def _cell_dims(c: int) -> dict:
    """exp166's cell_dims VERBATIM (pure bit decomposition; the frozen
    import block does not carry the name — replicated bit-for-bit; the
    scoping consumes exactly c=7 (o/h/t active) and c=0 (none))."""
    o, h, t = (c >> 2) & 1, (c >> 1) & 1, c & 1
    return {"oriented": bool(o), "signed": False, "complex": False,
            "hyper": bool(h), "temporal": bool(t)}


def _wall() -> float:
    """Wall-clock seconds (the frozen import block carries no time
    module; os.times()[4] is elapsed wall time)."""
    return os.times()[4]


def _arm(arm: str, medium, seeds: list[int]) -> dict:
    """exp148's run_arm shape VERBATIM (the frozen import block does
    not carry run_arm — identical semantics: errs/verify/keys/majority
    via exp148's decode dispatch, rejections recorded never raised)."""
    errs, vs, keys = [], [], []
    for s in seeds:
        out = exp148_decode(arm, medium, s)
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(outcome_key(out))
    return {"errs": errs, "verify": vs, "keys": keys,
            "majority": bool(np.mean(vs) > 0.5)}


def _scoped_arm(medium, seeds: list[int], fmax: float) -> tuple[dict, int]:
    """THE RULE applied per seed as an arm record; returns the record
    and the rejection count (rejections RECORDED, never raised)."""
    errs, vs, keys, rej = [], [], [], 0
    for s in seeds:
        out = scoped_read(medium, s, fmax)
        if not out["ok"]:
            rej += 1
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(outcome_key(out))
    return ({"errs": errs, "verify": vs, "keys": keys,
             "majority": bool(np.mean(vs) > 0.5)}, rej)


def _spot_media(js: list[int]) -> dict:
    """exp166's/exp167's corner + clean spot media (construction
    verbatim: CornerMedium(100, EXP166_SEED_BASE + 1000*cell + j,
    cell_dims(cell)); cells CORNER_CELL=7, CLEAN_CELL=0)."""
    meds = {}
    for tag, cell in (("corner", CORNER_CELL), ("clean", CLEAN_CELL)):
        for j in js:
            meds[(tag, j)] = CornerMedium(
                100, EXP166_SEED_BASE + 1000 * cell + j, _cell_dims(cell))
    return meds


def _battery_members(fams: tuple, doses: tuple) -> list[dict]:
    """exp148's flip-clock battery pairs, construction VERBATIM
    (sched_seed = SCHED_SEED + 4*family_index + dose_index)."""
    out = []
    for fam in fams:
        fi = FAMILIES.index(fam)
        for b in doses:
            di = LADDER.index(b)
            ss = SCHED_SEED + 4 * fi + di
            out.append({"family": fam, "dose": b, "sched_seed": ss,
                        "per": FlipPairMedium(b, fam, "per", sched_seed=ss),
                        "aper": FlipPairMedium(b, fam, "aper",
                                               sched_seed=ss)})
    return out


def _pair_fmax(m_per, m_aper) -> dict:
    """THE DIAGNOSTIC on a paired construction: f_max(pair) = max over
    the two schedule members (each member's value = the TC1 raw
    flip-clock matrix's max entry via f_max_frames; cross-checked
    against exp148's lazy flip_clock_matrix — the same number on these
    media: symmetric frames, zero diagonal)."""
    f_per = f_max_frames(list(m_per.snapshots()))
    f_aper = f_max_frames(list(m_aper.snapshots()))
    assert f_per == float(flip_clock_matrix(m_per).max()), \
        f"f_max mismatch per: {f_per}"
    assert f_aper == float(flip_clock_matrix(m_aper).max()), \
        f"f_max mismatch aper: {f_aper}"
    return {"f_max_per": f_per, "f_max_aper": f_aper,
            "pair_f_max": max(f_per, f_aper)}


# ------------------------------------------------------------- sections
def _section_threshold(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-S1: the recomputed f_max classes + instrument replays."""
    with open(DEP148) as f:
        dep148 = json.load(f)
    with open(DEP166) as f:
        dep166 = json.load(f)
    with open(DEP167) as f:
        dep167 = json.load(f)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    js = SPOT_J[:1] if smoke else SPOT_J
    fams = FAMILIES[:1] if smoke else FAMILIES
    doses = LADDER[:1] if smoke else LADDER
    spot166 = {(r["tag"], r["j"]): r
               for r in dep166["spot_battery"]["instances"]}
    spot167 = {(r["tag"], r["j"]): r
               for r in dep167["corner_spot"]["instances"]}
    dep_pairs167 = {(p["family"], p["dose"]): p
                    for p in dep167["battery"]["pairs"]}
    dep_pairs148 = {(p["family"], p["dose"]): p
                    for p in dep148["probes"]["pairs"]}

    # (1) the diffuse class: f_max over the corner/clean spot media
    meds = _spot_media(js)
    diffuse = []
    for (tag, j), med in meds.items():
        fm = f_max_frames(list(med.snapshots()))
        diffuse.append({"tag": tag, "j": j,
                        "T": len(med.snapshots()), "f_max": fm,
                        "class": "diffuse" if fm < THRESHOLD
                        else "concentrated"})
    corner_vals = [d["f_max"] for d in diffuse if d["tag"] == "corner"]
    corner_range = ([min(corner_vals), max(corner_vals)]
                    if corner_vals else None)
    dep_corner_range = dep167["gates"]["A3_corner_spot_adopted"][
        "corner_raw_fmax_range"]
    diffuse_max = max(d["f_max"] for d in diffuse)

    # (2) the concentrated class: pair-joint f_max over the battery
    concentrated, chord_replay = [], []
    for mem in _battery_members(fams, doses):
        fm = _pair_fmax(mem["per"], mem["aper"])
        concentrated.append({"family": mem["family"], "dose": mem["dose"],
                             "sched_seed": mem["sched_seed"], **fm,
                             "class": "concentrated"
                             if fm["pair_f_max"] >= THRESHOLD
                             else "diffuse"})
        dep = dep_pairs167[(mem["family"], mem["dose"])]
        d148 = dep_pairs148[(mem["family"], mem["dose"])]
        chord_replay.append({
            "family": mem["family"], "dose": mem["dose"],
            "f_per_replay": [int(x) for x in mem["per"].flip_counts]
                            == dep["f_per"],
            "f_aper_replay": [int(x) for x in mem["aper"].flip_counts]
                             == dep["f_aper"],
            "dep148_f_lists_equal_dep167": (
                d148["f_per"] == dep["f_per"]
                and d148["f_aper"] == dep["f_aper"])})
    conc_min = min(c["pair_f_max"] for c in concentrated)

    # the deposited gap bounds, recomputed and ASSERTED at run time
    assert diffuse_max <= 7.0, f"diffuse ceiling drifted: {diffuse_max}"
    assert conc_min >= 1165.0, f"concentrated floor drifted: {conc_min}"
    assert diffuse_max < THRESHOLD < conc_min, \
        f"threshold {THRESHOLD} outside the recomputed gap " \
        f"({diffuse_max}, {conc_min})"

    # (3) raw projection replay on the spot set: exp148's raw temporal
    # read on the RAW media replays exp166's deposited arm-A errs
    # bit-exactly — these are exp167's A3 input records (its clean
    # reference verbatim, its corner 'before' median), and the RTMasked
    # wrapper changes nothing on the raw path (no wrap at T=1; the
    # wrapper never mutates the raw medium or its frames).
    raw_replay, rejections = [], 0
    for (tag, j), med in meds.items():
        errs = []
        for s in seeds:
            out = exp148_decode("temporal", med, s)
            if not out["ok"]:
                rejections += 1
            errs.append(out.get("err"))
        ref = spot166[(tag, j)]["errs_armA"][:len(seeds)]
        raw_replay.append({"tag": tag, "j": j,
                           "replay_bit_exact_vs_exp166_armA":
                               errs == ref, "errs": errs,
                           "ref": ref})
    # (4) deposit consistency of exp167's A3 inputs: its replay refs
    # (errs_exp166) are exp166's armB (corner) / armA (clean) records,
    # and its deposited errs_adopted matched them bit-exactly.
    a3_refs_ok = True
    for (tag, j), r167 in spot167.items():
        dep = spot166[(tag, j)]
        ref = dep["errs_armB"] if tag == "corner" else dep["errs_armA"]
        a3_refs_ok &= (r167["errs_exp166"] == ref
                       and r167["errs_adopted"] == ref)

    c1 = all(d["class"] == "diffuse" for d in diffuse)
    c2 = all(c["class"] == "concentrated" for c in concentrated)
    c3 = all(all(v for k, v in r.items()
                 if k.endswith("_replay") or k.endswith("_dep167"))
             for r in chord_replay)
    c4 = (all(r["replay_bit_exact_vs_exp166_armA"] for r in raw_replay)
          and bool(a3_refs_ok))
    c5 = bool(smoke) or corner_range == dep_corner_range
    gate = {"pass": bool(c1 and c2 and c3 and c4 and c5),
            "clauses": {"diffuse_all_below_threshold": bool(c1),
                        "concentrated_all_at_or_above": bool(c2),
                        "per_chord_counts_replay": bool(c3),
                        "raw_projection_replay_and_a3_refs": bool(c4),
                        "corner_fmax_range_matches_deposit": c5},
            "recomputed_gap": {"diffuse_ceiling": diffuse_max,
                               "concentrated_floor": conc_min,
                               "threshold": THRESHOLD},
            "corner_fmax_range": corner_range,
            "corner_fmax_range_deposited": dep_corner_range,
            "n_diffuse_media": len(diffuse),
            "n_battery_pairs": len(concentrated),
            "smoke": bool(smoke)}
    section = {"diffuse_media": diffuse,
               "concentrated_pairs": concentrated,
               "per_chord_replay": chord_replay,
               "raw_projection_replay": raw_replay,
               "a3_inputs_consistent": bool(a3_refs_ok),
               "runtime_s": 0.0}
    return section, gate, rejections


def _section_battery(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-S2: the scoped read on the battery pairs IS exp148's raw
    temporal read bit-exactly; N2/N1 reproduced."""
    with open(DEP148) as f:
        dep148 = json.load(f)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    fams = FAMILIES[:1] if smoke else FAMILIES
    doses = LADDER[:1] if smoke else LADDER
    dep_pairs = {(p["family"], p["dose"]): p
                 for p in dep148["probes"]["pairs"]}
    pairs, rejections = [], 0
    n_sep = n_blind = 0
    for mem in _battery_members(fams, doses):
        fam, b = mem["family"], mem["dose"]
        fm = _pair_fmax(mem["per"], mem["aper"])
        scoped, rej_p = _scoped_arm(mem["per"], seeds, fm["pair_f_max"])
        scoped_a, rej_a = _scoped_arm(mem["aper"], seeds,
                                      fm["pair_f_max"])
        rejections += rej_p + rej_a
        phase_p = _arm("phase", mem["per"], seeds)
        phase_a = _arm("phase", mem["aper"], seeds)
        dep = dep_pairs[(fam, b)]
        d_per = dep["arms"]["per_temporal"]
        d_aper = dep["arms"]["aper_temporal"]
        replay = (scoped["errs"] == d_per["errs"][:len(seeds)]
                  and scoped["majority"] == d_per["majority"]
                  and scoped_a["errs"] == d_aper["errs"][:len(seeds)]
                  and scoped_a["majority"] == d_aper["majority"])
        sep = scoped["majority"] != scoped_a["majority"]
        blind = bool(verdict_blind(phase_p, phase_a))
        n_sep += int(sep)
        n_blind += int(blind)
        pairs.append({
            "family": fam, "dose": b, "sched_seed": mem["sched_seed"],
            "f_max_per": fm["f_max_per"], "f_max_aper": fm["f_max_aper"],
            "pair_f_max": fm["pair_f_max"],
            "scoping_class": "concentrated"
            if fm["pair_f_max"] >= THRESHOLD else "diffuse",
            "scoped": {"per_errs": scoped["errs"],
                       "per_majority": scoped["majority"],
                       "aper_errs": scoped_a["errs"],
                       "aper_majority": scoped_a["majority"]},
            "deposited_temporal": {
                "per_errs": d_per["errs"],
                "per_majority": d_per["majority"],
                "aper_errs": d_aper["errs"],
                "aper_majority": d_aper["majority"],
                "separated": dep["temporal_separated"]},
            "scoped_replay_bit_exact_vs_deposit": bool(replay),
            "scoped_separated": bool(sep),
            "phase_verdict_blind": blind,
            "phase_errs_replay_vs_deposit": bool(
                phase_p["errs"]
                == dep["arms"]["per_phase"]["errs"][:len(seeds)]
                and phase_a["errs"]
                == dep["arms"]["aper_phase"]["errs"][:len(seeds)]),
        })
        print(f"  S2 {fam:17s} b={b:6.1f} pair_f_max="
              f"{fm['pair_f_max']:.0f} replay={replay} sep={sep} "
              f"phaseBlind={blind}")
    n_pairs = len(pairs)
    gate = {"pass": bool(
        all(p["scoped_replay_bit_exact_vs_deposit"] for p in pairs)
        and all(p["scoping_class"] == "concentrated" for p in pairs)
        and n_sep == n_pairs and n_blind == n_pairs
        and rejections == 0
        and (smoke or (n_sep >= N2_MIN_SEPARATION
                       and n_blind >= N1_MIN_BLIND))),
        "n_pairs": n_pairs,
        "n_separated_scoped": n_sep, "required_n2": N2_MIN_SEPARATION,
        "n_phase_blind_reproduced": n_blind,
        "required_n1": N1_MIN_BLIND,
        "rejections": rejections, "smoke": bool(smoke)}
    section = {"pairs": pairs, "n_pairs": n_pairs, "runtime_s": 0.0}
    return section, gate, rejections


def _section_corner(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-S3: the scoped read on the spot set IS exp167's adopted
    read bit-exactly (corner) / exp166's clean arm-A (clean no-op)."""
    with open(DEP166) as f:
        dep166 = json.load(f)
    with open(DEP167) as f:
        dep167 = json.load(f)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    js = SPOT_J[:1] if smoke else SPOT_J
    spot166 = {(r["tag"], r["j"]): r
               for r in dep166["spot_battery"]["instances"]}
    spot167 = {(r["tag"], r["j"]): r
               for r in dep167["corner_spot"]["instances"]}
    instances, rejections = [], 0
    medians = {"corner": [], "clean": []}
    replay = {"corner": 0, "clean": 0}
    n_media = {"corner": 0, "clean": 0}
    for tag, cell in (("corner", CORNER_CELL), ("clean", CLEAN_CELL)):
        for j in js:
            med = CornerMedium(100,
                               seed=EXP166_SEED_BASE + 1000 * cell + j,
                               dims=_cell_dims(cell))
            fm = f_max_frames(list(med.snapshots()))
            arm, rej = _scoped_arm(med, seeds, fm)
            rejections += rej
            rec = {"tag": tag, "cell": cell, "j": j,
                   "gen_seed": med.seed, "T": len(med.snapshots()),
                   "f_max": fm,
                   "scoping_class": "diffuse" if fm < THRESHOLD
                   else "concentrated",
                   "errs_scoped": arm["errs"],
                   "verified_scoped": arm["verify"]}
            if tag == "corner":
                # exp167's A3 reference: the adopted read on this medium
                ref = spot167[("corner", j)]["errs_adopted"][:len(seeds)]
                rec["ref_source"] = "exp167_A3_errs_adopted"
            else:
                # exp166's clean arm-A (the no-op clause)
                ref = spot166[("clean", j)]["errs_armA"][:len(seeds)]
                rec["ref_source"] = "exp166_clean_errs_armA"
            rec["ref_errs"] = ref
            rec["replay_bit_exact"] = arm["errs"] == ref
            fin = [e for e in arm["errs"] if e is not None]
            rec["median_scoped"] = (float(np.median(fin)) if fin
                                    else None)
            replay[tag] += int(rec["replay_bit_exact"])
            n_media[tag] += 1
            if rec["median_scoped"] is not None:
                medians[tag].append(rec["median_scoped"])
            instances.append(rec)
        med_s = (float(np.median(medians[tag]))
                 if medians[tag] else None)
        print(f"  S3 {tag}: replay {replay[tag]}/{n_media[tag]} "
              f"median {med_s}")
    corner_median = (float(np.median(medians["corner"]))
                     if medians["corner"] else None)
    dep_corner_median = dep167["corner_spot"]["corner_median_after"]
    gate = {"pass": bool(replay["corner"] == n_media["corner"]
                         and replay["clean"] == n_media["clean"]
                         and all(r["scoping_class"] == "diffuse"
                                 for r in instances)
                         and rejections == 0
                         and (smoke
                              or corner_median == dep_corner_median)),
            "corner_replay_bit_exact": [replay["corner"],
                                        n_media["corner"]],
            "clean_replay_bit_exact": [replay["clean"],
                                       n_media["clean"]],
            "corner_median_scoped": corner_median,
            "corner_median_deposited_exp167": dep_corner_median,
            "rejections": rejections, "smoke": bool(smoke)}
    section = {"instances": instances, "runtime_s": 0.0}
    return section, gate, rejections


def _section_grid(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-S4: the schedule grid under the scoped read — per-instance
    f_max/class deposited BEFORE the pooled verdict; zero rejections;
    pooled median <= exp148's deposited temporal median; the
    cross-class outcome-identity clause (conditional)."""
    with open(DEP148) as f:
        dep148 = json.load(f)
    with open(DEP167) as f:
        dep167 = json.load(f)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    inst_range = list(range(1)) if smoke else \
        list(range(N_INSTANCES + N_INSTANCES_400))
    bar = dep148["gates"]["N3_schedule_fidelity"][
        "pooled_temporal_median"]
    blanket = dep167["grid_pooled"][
        "adopted_cross_class_outcome_identical"]

    # pass 1 — the PREDICTION records: per-instance f_max and class,
    # fixed and deposited before any pooled verdict is formed
    instances = []
    for cls_name, sched in GRID_CLASSES.items():
        for i in inst_range:
            n = 400 if i >= N_INSTANCES else 100
            med = FlipGridMedium(n, seed=GRID_BASE_SEED + i, sched=sched)
            fm = f_max_frames(list(med.snapshots()))
            instances.append({"cls": cls_name, "i": i, "n": n,
                              "gen_seed": GRID_BASE_SEED + i,
                              "f_max": fm,
                              "class": "diffuse" if fm < THRESHOLD
                              else "concentrated"})

    # pass 2 — the scoped decodes (the rule applied per instance)
    rejections = 0
    errs_all: list[float] = []
    cross_cache: dict = {}
    identical = compared = 0
    for rec in instances:
        med = FlipGridMedium(rec["n"], seed=rec["gen_seed"],
                             sched=GRID_CLASSES[rec["cls"]])
        arm, rej = _scoped_arm(med, seeds, rec["f_max"])
        rejections += rej
        rec["errs_scoped"] = arm["errs"]
        rec["verified_scoped"] = arm["verify"]
        errs_all.extend(e for e in arm["errs"] if e is not None)
        if rec["cls"] == "flip_per":
            for s, k in zip(seeds, arm["keys"]):
                cross_cache[(rec["n"], rec["i"], s)] = k
        else:
            for s, k in zip(seeds, arm["keys"]):
                twin = cross_cache.get((rec["n"], rec["i"], s))
                if twin is not None:
                    compared += 1
                    identical += int(twin == k)

    pooled = float(np.median(errs_all)) if errs_all else None
    any_conc = any(r["class"] == "concentrated" for r in instances)
    conditional = (not any_conc) or (identical < compared)
    gate = {"pass": bool(rejections == 0
                         and pooled is not None and pooled <= bar
                         and conditional),
            "pooled_scoped_median": pooled,
            "bar_exp148_deposited_temporal_median": bar,
            "no_regression": bool(pooled is not None and pooled <= bar),
            "n_instances": len(instances),
            "n_diffuse": sum(1 for r in instances
                             if r["class"] == "diffuse"),
            "n_concentrated": sum(1 for r in instances
                                  if r["class"] == "concentrated"),
            "zero_rejections": bool(rejections == 0),
            "rejections": rejections,
            "cross_class_outcome_identical": {
                "n_identical": identical, "n_compared": compared,
                "exp167_blanket": {"n_identical": blanket["n_identical"],
                                   "n_compared": blanket["n_compared"]},
                "clause": ("strictly below the blanket whenever >= 1 "
                           "instance classifies concentrated; vacuous "
                           "otherwise"),
                "clause_met": bool(conditional),
                "any_concentrated": bool(any_conc)},
            "smoke": bool(smoke)}
    if gate["n_concentrated"] == 0:
        gate["prediction_note"] = (
            "no grid instance classifies concentrated at T=32 (f_max "
            "at the flip-edge scale, well below 32.0): the scoped read "
            "is exp167's adopted read everywhere on the grid and the "
            "schedule-channel clause is vacuous here — the "
            "concentrated side is carried by the battery (S2)")
    section = {"instances": instances,
               "pooled_scoped_median": pooled,
               "rejections": rejections, "runtime_s": 0.0}
    return section, gate, rejections


SECTIONS = {"threshold": _section_threshold, "battery": _section_battery,
            "corner": _section_corner, "grid": _section_grid}

GATE_NAMES = {"threshold": "S1_threshold_validity",
              "battery": "S2_raw_where_concentrated",
              "corner": "S3_rt_where_diffuse",
              "grid": "S4_grid_prediction"}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 pair, 1 grid instance, "
                         "corner j=0, clean j=0 — discarded, no deposit")
    ap.add_argument("--job", choices=["threshold", "battery", "corner",
                                      "grid", "all"], default="all",
                    help="runner split; each job evaluates its own gate "
                         "exactly once and merges into the deposit")
    ap.add_argument("--out", default=None,
                    help="deposit path override (default %s)" % OUT)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    t0 = _wall()
    jobs = ["threshold", "battery", "corner", "grid"] \
        if args.job == "all" else [args.job]
    mode = ("SMOKE instrument check - discarded" if args.smoke
            else "FULL jobs=" + ",".join(jobs))
    print(f"=== exp169: R_T SCOPING ({mode}) ===\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP148_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP148_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}\n")

    # merged deposit: split runs accumulate sections across invocations
    result: dict = {}
    if not args.smoke and args.job != "all" and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("sections", {})
    result.setdefault("gates", {})

    total_rej = 0
    for name in jobs:
        ts = _wall()
        section, gate, rej = SECTIONS[name](args.smoke)
        section["runtime_s"] = round(_wall() - ts, 1)
        total_rej += rej
        result["sections"][name] = section
        result["gates"][GATE_NAMES[name]] = gate
        print(f"  [{name}] {GATE_NAMES[name]} pass={gate['pass']} "
              f"({section['runtime_s']} s, rejections {rej})")

    n_pass = sum(int(g["pass"]) for g in result["gates"].values())
    verdict = f"{n_pass}/{len(result['gates'])} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in result["gates"].items()))

    if not args.smoke:
        result.update({
            "exp": "exp169_rt_scoping",
            "claim": (
                "exp167's registered scoping run (L147): R_T per-media "
                "via the PRE-REGISTERED f_max concentration diagnostic "
                "(threshold 32.0 fixed from the deposited gap "
                "(7, 1165) before any decode; f_max(pair) = max over "
                "the two schedule members, zero per-instance tuning) — "
                "the scoped read keeps exp148's raw temporal read "
                "wherever the flip clock is concentrated and applies "
                "exp167's adopted R_T read wherever it is diffuse, "
                "with bit-exact replay on both sides; the grid "
                "classification is deposited as the diagnostic's "
                "prediction"),
            "pre_registration": {
                "threshold": THRESHOLD,
                "rule": ("apply R_T (exp167's adopted read) iff "
                         "f_max < 32.0, else exp148's raw temporal "
                         "read; one threshold, no outcome feedback"),
                "diagnostic": ("f_max = max over directed edges of the "
                               "per-edge presence-transition count "
                               "across the read window (the TC1 raw "
                               "flip-clock matrix's max entry); "
                               "f_max(pair) = max over the two "
                               "schedule members"),
                "deposited_gap": {"diffuse_ceiling": 7,
                                  "concentrated_floor": 1165,
                                  "source": ("exp167 corner_raw_fmax_"
                                             "range [5, 7]; exp148/167 "
                                             "battery f_aper lists")},
                "gates_source": ("module docstring, committed before "
                                 "any decode (pre-registration commit "
                                 "9d61e3b)")},
            "config": {
                "seeds": list(SPOT_SEEDS),
                "spot_j": list(SPOT_J),
                "corner_cell": CORNER_CELL, "clean_cell": CLEAN_CELL,
                "grid_base_seed": GRID_BASE_SEED,
                "n_instances": N_INSTANCES,
                "n_instances_400": N_INSTANCES_400,
                "families": list(FAMILIES), "ladder": list(LADDER),
                "sched_seed_base": SCHED_SEED,
                "exp166_seed_base": EXP166_SEED_BASE,
                "jobs_run": jobs,
                "smoke": bool(args.smoke),
                "instrument_pin": {
                    "constant": "NEURAL_SPEC_MIN",
                    "pinned_to": DEP148_FLOOR,
                    "saved_values": _PIN_SAVE,
                    "modules": [m.__name__ for m in PIN_MODULES],
                    "note": ("exp167's import-time pin has already "
                             "restored the -35.0 world before this "
                             "module's _PIN_SAVE captures it; "
                             "pin/restore asserted around every job")}},
        })
        result["verdict"] = verdict
        result["rejections"] = total_rej
        result["runtime_s"] = round(_wall() - t0, 1)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  deposited {out_path} "
              f"(rejections {total_rej}, runtime {result['runtime_s']} s)")
    else:
        print("\n  SMOKE instrument check complete - DISCARDED "
              "(no deposit written)")
        result["verdict"] = "smoke (discarded)"
        result["rejections"] = total_rej

    # ---- save/restore asserted ----
    restore_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None)
               == _PIN_SAVE[m.__name__] for m in PIN_MODULES), \
        "instrument floor restore failed"
    print(f"  floor restored to the saved world (asserted): {_PIN_SAVE}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["threshold", "battery", "corner",
                                      "grid", "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
