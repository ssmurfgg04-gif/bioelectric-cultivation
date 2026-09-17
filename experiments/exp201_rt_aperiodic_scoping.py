#!/usr/bin/env python3
"""exp201 — R_T APERIODIC SCOPING (L147's registered next).

exp167 adopted R_T (flip-quiet core-support windowing) for
time-varying media; exp169 scoped it by the f_max diagnostic
(THRESHOLD 32.0, pair-joint for paired constructions) and exp178
landed the scoped arm in production. The registered open edge: R_T's
scoping on APERIODIC media — presence schedules with no periodic
flip clock, the class the 32.0 threshold has never been asked to
classify.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp169's f_max_frames
VERBATIM with the DEPOSITED THRESHOLD 32.0 (never re-fit); exp148's
temporal battery construction VERBATIM with the flip-clock's
presence intervals replaced by the pre-named APERIODIC schedule
(intervals = ceil(8 * U(0.5, 4.0)^k), drawn per edge from
default_rng(201201) — disclosed, zero fitting); exp160's decode stack
VERBATIM (fingerprint asserted) with exp178's scoped arm; the -35.0
pin asserted.

THE BATTERY (40 aperiodic media, two pre-named subfamilies):
  mild-aperiodic (k mean ~1, schedules near-regular) and
  strong-aperiodic (k mean ~4, schedules bursty) — 20 each,
  generator seeds deposited FIRST (seed = 201200 + i).

GATES (each evaluated exactly once):
  GATE-P1 (census) the f_max census over the 40; the classification
           deposited per medium; the gap structure vs the deposited
           32.0 threshold RECORDED (the threshold stands; a bimodal
           census with an empty gap crossing 32.0 confirms the
           scoping's transfer; an interior census does not refute —
           it prices the aperiodic class's position).
  GATE-P2 (scoped read) every aperiodic medium read under the
           production scoped arm; per-media arm selection and errs
           deposited; zero rejections; all errs finite.
  GATE-P3 (the scoping question) on the f_max < 32 side the scoped
           read IS exp167's adopted path bit-exactly; on the
           >= 32 side it IS exp148's raw temporal bit-exactly; the
           per-subfamily median deltas vs the raw temporal arm
           deposited, with the pre-named branches:
           REPAIR (mild-aperiodic median drops >= 20%),
           PARTIAL (0 < drop < 20%), NEUTRAL-HARM (<= 0).
  GATE-P4 (hygiene) pin save/restore asserted; fingerprints
           asserted; zero rejections.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp201_rt_aperiodic_scoping.json
RUN: python3 -m experiments.exp201_rt_aperiodic_scoping [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp142_sign_read import (  # noqa: E402
    K_CHORDS, PROBE_SEED, execute_signed,
)
from experiments.exp148_temporal_read import (  # noqa: E402
    FAMILIES, FlipPairMedium, LADDER, T_BATTERY,
    decode as exp148_decode, flip_clock_matrix, outcome_key,
)
from experiments.exp167_rt_adopted import (  # noqa: E402
    decode as exp167_decode,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames,
)

# ---- INSTRUMENT PIN (the -35.0 restored world; exp169/exp178 mech) --
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


OUT = os.path.join(ROOT, "results", "exp201_rt_aperiodic_scoping.json")

# ------------------------- THE PRE-NAMED APERIODIC BATTERY -----------
# exp148's temporal battery construction VERBATIM (FlipPairMedium:
# static ring backbone 1.0 + K_CHORDS chord edges carrying -b when ON,
# 0.0 when OFF, over T_BATTERY frames; exp142's carrier geometry via
# chord_set at PROBE_SEED) with the flip-clock's presence intervals
# REPLACED by the pre-named APERIODIC schedule. The schedule
# resolution (disclosed, zero fitting, fixed before any decode):
#   * media i = 0..39; generator seed = 201200 + i (deposited FIRST);
#     subfamily mild_aperiodic for i < 20, strong_aperiodic otherwise;
#     family = FAMILIES[i % 3], dose b = LADDER[i % 4].
#   * per chord edge (chord order), presence is an ALTERNATING
#     ON/OFF interval sequence starting ON at t = 0, truncated at
#     T = 2400. Per interval: k ~ U(0, 2*mean_k) drawn from the
#     medium's own generator stream default_rng(201200 + i)
#     (mean_k = 1.0 mild => E[k] = 1 — "k mean ~1", near-regular
#     jittered-clock schedules; mean_k = 4.0 strong => E[k] = 4 —
#     "k mean ~4", bursty schedules); U ~ U(0.5, 4.0) drawn per edge
#     from THE ONE shared stream default_rng(201201) consumed across
#     the battery in deposit order (draw order per interval: k, then
#     U); interval length = ceil(8 * U**k).
#   * construction is ALWAYS the full 40-medium battery in i order
#     (stream-position invariance across --job splits); jobs filter
#     decodes only.
GEN_SEED_BASE = 201200
SCHEDULE_URN_SEED = 201201
N_MILD = 20
N_MEDIA = 40
SUBFAMILIES = {"mild_aperiodic": 1.0, "strong_aperiodic": 4.0}
SEEDS = (1, 2, 3)               # exp137/exp160's seed protocol

# ------------- exp160's decode stack VERBATIM (fingerprint asserted) -
READ_CONFIG = {
    "projection": (
        "exp178's production scoped arm VERBATIM (exp148's read_temporal"
        " path: PN1/PN2 dominant-quadrature projected time-average + TC1"
        " flip-clock F + TC2 A_ext = A + F; the R_T clause = exp167's"
        " core-support mask iff f_max < 32.0, exp169's f_max_frames +"
        " THRESHOLD verbatim)"),
    "executor": ("exp142 execute_signed VERBATIM (R1 structure on |A|, R2"
                 " signed dynamics, walk frontier on |A|>0)"),
    "op": {"gamma": 64.0, "mu": 0.0},
    "op_source": "exp99 battery-wide STAR point (exp142's STAR_OP)",
    "spec": "MULTI (exp94 3-zone program)",
    "frontier": "walk (inside exp142's executor)",
    "seeds": [1, 2, 3],
    "n": 100,
    "window_h": 24.0,
    "commit_noise": 0.6,
    "steps_per_cell": 8,
    "per_instance_tuning": "none",
}


def config_fingerprint() -> str:
    return hashlib.sha256(
        json.dumps(READ_CONFIG, sort_keys=True).encode()).hexdigest()[:16]


FP_PRE = config_fingerprint()


# ---------------------------- the aperiodic medium -------------------
class AperiodicFlipMedium(FlipPairMedium):
    """exp148's FlipPairMedium VERBATIM (inherited frame generation,
    snapshots(), native_support()) with the presence schedule replaced
    by the pre-named aperiodic interval process (see module header).
    No fixed per-edge ON count: the duty cycle is the process's own
    realization. flip_counts stays exp148's raw per-edge presence-
    transition count (the TC1 quantity)."""

    kind = "aperiodic_flip"

    def __init__(self, b: float, family: str, subfamily: str,
                 gen_seed: int, urng, n: int = 100,
                 chord_seed: int = PROBE_SEED, T: int = T_BATTERY):
        A, chords = chord_set_safe(n, family, chord_seed)
        self.A, self.chords = A, chords
        self.b, self.sched, self.T = float(b), subfamily, T
        self.c = None                       # no fixed ON count
        self.gen_seed, self.subfamily = gen_seed, subfamily
        k = len(chords)
        mean_k = SUBFAMILIES[subfamily]
        krng = np.random.default_rng(gen_seed)
        on = np.zeros((k, T), dtype=bool)
        self.n_intervals: list[int] = []
        self.k_draws: list[list[float]] = []
        for e in range(k):
            t, state, ks = 0, True, []
            while t < T:
                kk = float(krng.uniform(0.0, 2.0 * mean_k))
                U = float(urng.uniform(0.5, 4.0))
                L = int(np.ceil(8.0 * (U ** kk)))
                assert L >= 1, f"non-positive interval {L}"
                L = min(L, T - t)
                on[e, t:t + L] = state
                state = not state
                t += L
                ks.append(kk)
            assert t == T, "interval schedule must cover the window"
            self.n_intervals.append(len(ks))
            self.k_draws.append(ks)
        self.on = on
        self.flip_counts = np.count_nonzero(on[:, 1:] != on[:, :-1],
                                            axis=1)
        self._base = A.copy()               # static ring backbone


def chord_set_safe(n: int, family: str, seed: int):
    """exp148's chord_set VERBATIM (imported module attribute; the
    indirection exists only so the medium reads as one constructor)."""
    return _m148.chord_set(n, family, seed)


# ------------------------------------------------------------ harness
def _wall() -> float:
    return os.times()[4]


def battery_table() -> list[dict]:
    """THE GENERATOR SEEDS, DEPOSITED FIRST: the 40 media identities,
    fixed by arithmetic before any medium is constructed or decoded."""
    rows = []
    for i in range(N_MEDIA):
        sub = "mild_aperiodic" if i < N_MILD else "strong_aperiodic"
        rows.append({"i": i, "gen_seed": GEN_SEED_BASE + i,
                     "subfamily": sub,
                     "family": FAMILIES[i % len(FAMILIES)],
                     "dose": LADDER[i % len(LADDER)]})
    return rows


def build_media(table: list[dict]) -> dict[int, AperiodicFlipMedium]:
    """Construct the FULL battery in i order (the shared U-stream's
    position is part of the instrument); jobs filter decodes only."""
    urng = np.random.default_rng(SCHEDULE_URN_SEED)
    meds = {}
    for rec in table:
        meds[rec["i"]] = AperiodicFlipMedium(
            rec["dose"], rec["family"], rec["subfamily"],
            rec["gen_seed"], urng)
    return meds


def _fmax(med) -> float:
    """exp169's f_max_frames VERBATIM, cross-checked against exp148's
    lazy TC1 matrix (the same number on these symmetric media) — the
    exp169/_pair_fmax instrument identity, per medium."""
    fm = f_max_frames(list(med.snapshots()))
    assert fm == float(flip_clock_matrix(med).max()), \
        f"f_max mismatch: {fm}"
    return fm


def _decode(arm: str, med, s: int, fm: float | None,
            fps: list[str]) -> dict:
    """One decode through the production stack; the fingerprint is
    recorded per decode (exp160's mechanism); rejections are RECORDED,
    never raised (exp148's decode policy)."""
    fps.append(FP_PRE)
    if arm == "scoped":
        return _m148.decode("scoped", med, s, f_max=fm)
    if arm == "temporal":
        return exp148_decode("temporal", med, s)
    if arm == "adopted":
        return exp167_decode("adopted", med, s)
    raise ValueError(arm)


def _seed_arm(arm: str, med, seeds: list[int], fm: float | None,
              fps: list[str]) -> tuple[dict, int]:
    """Arm record over seeds (exp148's run_arm shape); returns the
    record and the rejection count."""
    errs, vs, keys, rej = [], [], [], 0
    for s in seeds:
        out = _decode(arm, med, s, fm, fps)
        if not out["ok"]:
            rej += 1
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(outcome_key(out))
    return ({"errs": errs, "verify": vs, "keys": keys,
             "majority": bool(np.mean(vs) > 0.5)}, rej)


def _branch(drop: float) -> str:
    """THE PRE-NAMED BRANCHES (GATE-P3): REPAIR (drop >= 20%),
    PARTIAL (0 < drop < 20%), NEUTRAL-HARM (<= 0)."""
    if drop >= 0.20:
        return "REPAIR"
    if drop > 0.0:
        return "PARTIAL"
    return "NEUTRAL-HARM"


# ------------------------------------------------------------- sections
def _section_census(smoke: bool, fps: list[str]) -> tuple[dict, dict, int]:
    """GATE-P1: the f_max census over the aperiodic battery; per-medium
    classification; the gap structure vs the DEPOSITED 32.0 threshold
    recorded (the threshold stands; the census position is deposited,
    not gated)."""
    table = battery_table()
    meds = build_media(table)
    seeds = [1] if smoke else list(SEEDS)
    idxs = [0, N_MILD] if smoke else list(range(N_MEDIA))
    rows = []
    for rec in table:
        if rec["i"] not in idxs:
            continue
        med = meds[rec["i"]]
        fm = _fmax(med)
        rows.append({
            **rec, "T": med.T,
            "n_intervals_per_edge": med.n_intervals,
            "flip_counts": [int(x) for x in med.flip_counts],
            "k_mean_realized": round(float(np.mean(
                [k for ks in med.k_draws for k in ks])), 4),
            "f_max": fm,
            "class": "diffuse" if fm < THRESHOLD else "concentrated"})
    below = [r["f_max"] for r in rows if r["class"] == "diffuse"]
    above = [r["f_max"] for r in rows if r["class"] == "concentrated"]
    below_max = max(below) if below else None
    above_min = min(above) if above else None
    sub_ranges = {}
    for sub in SUBFAMILIES:
        vals = [r["f_max"] for r in rows if r["subfamily"] == sub]
        sub_ranges[sub] = {"min": min(vals) if vals else None,
                           "max": max(vals) if vals else None,
                           "n": len(vals),
                           "n_diffuse": sum(
                               1 for r in rows
                               if r["subfamily"] == sub
                               and r["class"] == "diffuse"),
                           "n_concentrated": sum(
                               1 for r in rows
                               if r["subfamily"] == sub
                               and r["class"] == "concentrated")}
    gap = {"threshold": THRESHOLD,
           "largest_below": below_max, "smallest_at_or_above": above_min,
           "gap_interval": ([below_max, above_min]
                            if below_max is not None
                            and above_min is not None else None),
           "empty_gap_crossing_threshold": bool(
               below_max is not None and above_min is not None
               and below_max < THRESHOLD <= above_min),
           "margin_below": (THRESHOLD - below_max
                            if below_max is not None else None),
           "margin_above": (above_min - THRESHOLD
                            if above_min is not None else None),
           "reading": ("bimodal with an empty gap crossing the deposited "
                       "threshold: the scoping's transfer is confirmed"
                       if below_max is not None and above_min is not None
                       and (above_min - below_max) > 2.0
                       else "interior census: the aperiodic class's "
                            "position against 32.0 is priced, not refuted")}
    consistent = all((r["class"] == "diffuse") == (r["f_max"] < THRESHOLD)
                     for r in rows)
    gate = {"pass": bool(rows and consistent
                         and len(rows) == len(idxs)),
            "n_media": len(rows),
            "classification_consistent": bool(consistent),
            "threshold": THRESHOLD, "threshold_source": "exp169 deposit",
            "gap_structure": gap, "subfamily_ranges": sub_ranges,
            "note": ("the threshold stands (never re-fit); bimodality is "
                     "RECORDED, not gated — an interior census prices the "
                     "aperiodic class's position (docstring P1)"),
            "smoke": bool(smoke)}
    section = {"media": rows, "gap_structure": gap,
               "subfamily_ranges": sub_ranges, "runtime_s": 0.0}
    return section, gate, 0


def _section_scoped(smoke: bool, fps: list[str]) -> tuple[dict, dict, int]:
    """GATE-P2: every aperiodic medium read under exp178's production
    scoped arm; per-media arm selection and errs deposited; zero
    rejections; all errs finite."""
    table = battery_table()
    meds = build_media(table)
    seeds = [1] if smoke else list(SEEDS)
    idxs = [0, N_MILD] if smoke else list(range(N_MEDIA))
    rows, rejections = [], 0
    n_decodes = 0
    for rec in table:
        if rec["i"] not in idxs:
            continue
        med = meds[rec["i"]]
        fm = _fmax(med)
        arm_sel = "adopted" if fm < THRESHOLD else "temporal"
        arm, rej = _seed_arm("scoped", med, seeds, fm, fps)
        rejections += rej
        n_decodes += len(seeds)
        fin = all(e is not None and bool(np.isfinite(e))
                  for e in arm["errs"])
        rows.append({**rec, "T": med.T, "f_max": fm,
                     "arm_selected": arm_sel,
                     "errs_scoped": arm["errs"],
                     "verified_scoped": arm["verify"],
                     "majority_scoped": arm["majority"],
                     "all_errs_finite": bool(fin)})
        print(f"  P2 i={rec['i']:2d} {rec['subfamily']:17s} "
              f"{rec['family']:17s} b={rec['dose']:6.1f} "
              f"f_max={fm:7.1f} arm={arm_sel:8s} "
              f"errs={arm['errs']} rej={rej}")
    sel_ok = all((r["arm_selected"] == "adopted")
                 == (r["f_max"] < THRESHOLD) for r in rows)
    gate = {"pass": bool(rejections == 0
                         and n_decodes == len(rows) * len(seeds)
                         and sel_ok
                         and all(r["all_errs_finite"] for r in rows)),
            "n_media": len(rows), "n_decodes": n_decodes,
            "seeds": list(seeds),
            "zero_rejections": bool(rejections == 0),
            "rejections": rejections,
            "arm_selection_consistent": bool(sel_ok),
            "all_errs_finite": bool(all(r["all_errs_finite"]
                                        for r in rows)),
            "n_adopted_side": sum(1 for r in rows
                                  if r["arm_selected"] == "adopted"),
            "n_temporal_side": sum(1 for r in rows
                                   if r["arm_selected"] == "temporal"),
            "fingerprints_distinct": sorted(set(fps)),
            "smoke": bool(smoke)}
    section = {"media": rows, "n_decodes": n_decodes,
               "rejections": rejections, "runtime_s": 0.0}
    return section, gate, rejections


def _section_question(smoke: bool,
                      fps: list[str]) -> tuple[dict, dict, int]:
    """GATE-P3: the scoping question — on the f_max < 32 side the
    scoped read IS exp167's adopted path bit-exactly; on the >= 32
    side it IS exp148's raw temporal bit-exactly; per-subfamily median
    deltas vs the raw temporal arm + the pre-named branches."""
    table = battery_table()
    meds = build_media(table)
    seeds = [1] if smoke else list(SEEDS)
    idxs = [0, N_MILD] if smoke else list(range(N_MEDIA))
    rows, rejections = [], 0
    pools = {sub: {"scoped": [], "raw": []} for sub in SUBFAMILIES}
    for rec in table:
        if rec["i"] not in idxs:
            continue
        med = meds[rec["i"]]
        fm = _fmax(med)
        scoped, rej_s = _seed_arm("scoped", med, seeds, fm, fps)
        raw, rej_r = _seed_arm("temporal", med, seeds, None, fps)
        rejections += rej_s + rej_r
        if fm < THRESHOLD:
            ref, rej_a = _seed_arm("adopted", med, seeds, None, fps)
            rejections += rej_a
            ref_name = "exp167_adopted"
            ref_errs = ref["errs"]
        else:
            ref_name = "exp148_temporal"
            ref_errs = raw["errs"]
        bit_exact = scoped["errs"] == ref_errs
        sub = rec["subfamily"]
        pools[sub]["scoped"].extend(
            e for e in scoped["errs"] if e is not None)
        pools[sub]["raw"].extend(e for e in raw["errs"] if e is not None)
        rows.append({**rec, "T": med.T, "f_max": fm,
                     "side": "f_max<32" if fm < THRESHOLD else "f_max>=32",
                     "reference": ref_name,
                     "errs_scoped": scoped["errs"],
                     "errs_raw_temporal": raw["errs"],
                     "errs_reference": ref_errs,
                     "scoped_is_reference_bit_exact": bool(bit_exact),
                     "delta_scoped_minus_raw_median": None})
        rows[-1]["delta_scoped_minus_raw_median"] = round(
            float(np.median([e for e in scoped["errs"] if e is not None]))
            - float(np.median([e for e in raw["errs"] if e is not None])),
            4) if all(e is not None for e in scoped["errs"]) else None
        print(f"  P3 i={rec['i']:2d} {sub:17s} f_max={fm:7.1f} "
              f"side={rows[-1]['side']} ref={ref_name} "
              f"bit_exact={bit_exact}")
    sub_stats = {}
    for sub, pool in pools.items():
        s_med = (float(np.median(pool["scoped"]))
                 if pool["scoped"] else None)
        r_med = (float(np.median(pool["raw"]))
                 if pool["raw"] else None)
        delta = (s_med - r_med) if (s_med is not None
                                    and r_med is not None) else None
        drop = ((r_med - s_med) / r_med
                if (s_med is not None and r_med is not None and r_med > 0)
                else 0.0)
        sub_stats[sub] = {
            "scoped_pool_median": s_med, "raw_pool_median": r_med,
            "delta_median": (round(delta, 4) if delta is not None
                             else None),
            "drop_fraction": round(drop, 6),
            "branch": _branch(drop),
            "n_errs": len(pool["scoped"])}
        print(f"  P3 {sub}: scoped {s_med} raw {r_med} "
              f"drop {drop:.4f} -> {sub_stats[sub]['branch']}")
    mild_branch = sub_stats["mild_aperiodic"]["branch"]
    gate = {"pass": bool(all(r["scoped_is_reference_bit_exact"]
                             for r in rows)
                         and rejections == 0
                         and all(r["delta_scoped_minus_raw_median"]
                                 is not None for r in rows)),
            "bit_exact_all_sides": bool(
                all(r["scoped_is_reference_bit_exact"] for r in rows)),
            "n_media": len(rows),
            "n_adopted_side": sum(1 for r in rows
                                  if r["side"] == "f_max<32"),
            "n_temporal_side": sum(1 for r in rows
                                   if r["side"] == "f_max>=32"),
            "subfamily_deltas": sub_stats,
            "mild_aperiodic_branch": mild_branch,
            "branch_rule": ("REPAIR (mild-aperiodic median drops >= 20%), "
                            "PARTIAL (0 < drop < 20%), NEUTRAL-HARM "
                            "(<= 0) — pre-named, applied to the realized "
                            "drop, whatever it is"),
            "zero_rejections": bool(rejections == 0),
            "rejections": rejections,
            "fingerprints_distinct": sorted(set(fps)),
            "smoke": bool(smoke)}
    section = {"media": rows, "subfamily_deltas": sub_stats,
               "rejections": rejections, "runtime_s": 0.0}
    return section, gate, rejections


def _read_path_identities() -> dict:
    """exp160's U4 audit, extended to the scoped stack: the read path
    IS exp148's; its executor IS exp142's; spec IS exp94's MULTI; the
    scoped arm IS exp148's production dispatch consuming exp169's
    f_max_frames + THRESHOLD verbatim and exp167's adopted path."""
    import experiments.exp167_rt_adopted as _m167
    import experiments.exp169_rt_scoping as _m169
    return {
        "read_temporal_is_exp148": _m148.read_temporal.__module__
        == "experiments.exp148_temporal_read",
        "executor_is_exp142": execute_signed.__module__
        == "experiments.exp142_sign_read",
        "spec_is_exp94_MULTI": _m94.MULTI.__class__.__name__
        == "AnatomySpec",
        "scoped_arm_is_exp148_dispatch": (
            _m148.read_scoped.__module__
            == "experiments.exp148_temporal_read"
            and '"scoped"' in inspect.getsource(_m148.decode)),
        "f_max_frames_is_exp169": _m169.f_max_frames.__module__
        == "experiments.exp169_rt_scoping",
        "threshold_is_exp169_deposit": (_m169.THRESHOLD == 32.0
                                        and THRESHOLD == 32.0),
        "adopted_path_is_exp167": _m167.read_adopted.__module__
        == "experiments.exp167_rt_adopted",
    }


def _section_hygiene(smoke: bool, result: dict,
                     fps: list[str]) -> tuple[dict, dict, int]:
    """GATE-P4: pin save/restore asserted (live, by main around every
    job); fingerprints asserted (single configuration across every
    decode, unchanged post-run); zero rejections (aggregated over the
    run's decode sections); read-path identity asserted."""
    ident = _read_path_identities()
    fp_post = config_fingerprint()
    sections = result.get("sections", {})
    gates = result.get("gates", {})
    rej = 0
    n_dec = 0
    fp_sets: list[list[str]] = [sorted(set(fps))] if fps else []
    for name, sec in sections.items():
        rej += int(sec.get("rejections", 0) or 0)
        n_dec += int(sec.get("n_decodes", 0) or 0)
    # the fingerprint evidence: this run's live list plus every decode
    # gate's recorded distinct set
    for name in ("scoped", "question"):
        if name in gates:
            fp_sets.append(gates[name].get("fingerprints_distinct", []))
    single = all(len(set(s)) == 1 and s[0] == FP_PRE for s in fp_sets
                 if s)
    gate = {"pass": bool(single and fp_post == FP_PRE
                         and all(ident.values())
                         and rej == 0 and n_dec > 0),
            "pin": {"constant": "NEURAL_SPEC_MIN",
                    "pinned_to": DEP148_FLOOR,
                    "saved_values": _PIN_SAVE,
                    "modules": [m.__name__ for m in PIN_MODULES],
                    "asserted_at_start": True,
                    "restored_at_end_asserted": True},
            "fingerprint": {"pre_run": FP_PRE, "post_run": fp_post,
                            "unchanged": bool(fp_post == FP_PRE),
                            "single_configuration": bool(single),
                            "n_decodes": n_dec},
            "rejections": rej, "zero_rejections": bool(rej == 0),
            "read_path_identities": ident,
            "sections_audited": sorted(sections.keys()),
            "smoke": bool(smoke)}
    section = {"rejections": rej, "n_decodes": n_dec, "runtime_s": 0.0}
    return section, gate, 0


SECTIONS = {"census": _section_census, "scoped": _section_scoped,
            "question": _section_question, "hygiene": _section_hygiene}

GATE_NAMES = {"census": "P1_census",
              "scoped": "P2_scoped_read",
              "question": "P3_scoping_question",
              "hygiene": "P4_hygiene"}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 mild (i=0) + 1 strong "
                         "(i=20) medium, 1 seed — discarded, no deposit")
    ap.add_argument("--job", choices=["census", "scoped", "question",
                                      "hygiene", "all"], default="all",
                    help="runner split; each job evaluates its own gate "
                         "exactly once and merges into the deposit")
    ap.add_argument("--out", default=None,
                    help="deposit path override (default %s)" % OUT)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    t0 = _wall()
    jobs = ["census", "scoped", "question", "hygiene"] \
        if args.job == "all" else [args.job]
    mode = ("SMOKE instrument check - discarded" if args.smoke
            else "FULL jobs=" + ",".join(jobs))
    print(f"=== exp201: R_T APERIODIC SCOPING ({mode}) ===\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP148_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP148_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]} (asserted)")
    print(f"  threshold: exp169's deposited {THRESHOLD} (never re-fit); "
          f"read config fingerprint {FP_PRE}\n")

    # ---- THE GENERATOR SEEDS, DEPOSITED FIRST (before any decode) ---
    table = battery_table()
    assert len(table) == N_MEDIA
    assert [r["gen_seed"] for r in table] \
        == [GEN_SEED_BASE + i for i in range(N_MEDIA)]
    print(f"  battery: {N_MEDIA} aperiodic media, seeds "
          f"{GEN_SEED_BASE}..{GEN_SEED_BASE + N_MEDIA - 1} deposited "
          f"FIRST; subfamilies mild_aperiodic (i<20, E[k]=1) / "
          f"strong_aperiodic (i>=20, E[k]=4); schedule urn seed "
          f"{SCHEDULE_URN_SEED}\n")

    # merged deposit: split runs accumulate sections across invocations
    result: dict = {}
    if not args.smoke and args.job != "all" and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("battery", {})
    result.setdefault("sections", {})
    result.setdefault("gates", {})
    result["battery"] = {
        "seeds_deposited_first": table,
        "n_media": N_MEDIA, "n_mild": N_MILD,
        "T": T_BATTERY, "k_chords": K_CHORDS,
        "schedule": {
            "intervals": "ceil(8 * U(0.5, 4.0)^k), alternating ON/OFF "
                         "starting ON, truncated at T (pre-named)",
            "k_draw": "k ~ U(0, 2*mean_k) per interval from the medium's "
                      "generator stream default_rng(201200 + i); "
                      "mean_k = 1.0 mild / 4.0 strong (E[k] = mean_k: "
                      "the docstring's 'k mean ~1' / 'k mean ~4')",
            "u_draw": "U ~ U(0.5, 4.0) per interval per edge from THE "
                      "ONE shared stream default_rng(201201), consumed "
                      "per edge (chord order) per medium (deposit order)",
            "draw_order_per_interval": "k, then U",
            "geometry": "exp148's chord_set VERBATIM (exp142's carrier "
                        "geometry, PROBE_SEED), family = FAMILIES[i%3], "
                        "dose = LADDER[i%4]",
        },
    }

    fps: list[str] = []
    total_rej = 0
    for name in jobs:
        ts = _wall()
        if name == "hygiene":
            section, gate, rej = SECTIONS[name](args.smoke, result, fps)
        else:
            section, gate, rej = SECTIONS[name](args.smoke, fps)
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
            "exp": "exp201_rt_aperiodic_scoping",
            "claim": (
                "R_T's scoping on APERIODIC media (L147's registered "
                "next): exp148's temporal battery construction with the "
                "flip-clock's presence intervals replaced by the "
                "pre-named aperiodic schedule (intervals = ceil(8 * "
                "U(0.5,4.0)^k); 40 media, mild-aperiodic E[k]=1 "
                "near-regular vs strong-aperiodic E[k]=4 bursty, "
                "generator seeds 201200+i deposited first) — the f_max "
                "census classifies each medium against exp169's "
                "DEPOSITED 32.0 threshold (never re-fit; the gap "
                "structure is recorded whatever its shape), every "
                "medium reads under exp178's production scoped arm "
                "with zero rejections, the scoped read is bit-exactly "
                "exp167's adopted path on the f_max < 32 side and "
                "bit-exactly exp148's raw temporal on the >= 32 side, "
                "and the per-subfamily median deltas vs the raw "
                "temporal arm land in the pre-named REPAIR / PARTIAL / "
                "NEUTRAL-HARM branches"),
            "pre_registration": {
                "instruments": [
                    "exp169's f_max_frames VERBATIM with the DEPOSITED "
                    "THRESHOLD 32.0 (never re-fit)",
                    "exp148's temporal battery construction VERBATIM "
                    "with the flip-clock's presence intervals replaced "
                    "by the pre-named APERIODIC schedule (intervals = "
                    "ceil(8 * U(0.5, 4.0)^k), drawn per edge from "
                    "default_rng(201201) — disclosed, zero fitting)",
                    "exp160's decode stack VERBATIM (fingerprint "
                    "asserted) with exp178's scoped arm",
                    "the -35.0 pin asserted"],
                "battery": ("40 aperiodic media, two pre-named "
                            "subfamilies: mild-aperiodic (k mean ~1, "
                            "schedules near-regular) and "
                            "strong-aperiodic (k mean ~4, schedules "
                            "bursty) — 20 each, generator seeds "
                            "deposited FIRST (seed = 201200 + i)"),
                "branches": ("REPAIR (mild-aperiodic median drops "
                             ">= 20%), PARTIAL (0 < drop < 20%), "
                             "NEUTRAL-HARM (<= 0) — pre-named"),
                "schedule_resolution": (
                    "the pre-named formula's free parameters resolved "
                    "ONCE, disclosed, before any decode: k ~ U(0, "
                    "2*mean_k) per interval (mild mean_k 1.0, strong "
                    "4.0) from the medium's generator stream "
                    "default_rng(201200+i); U(0.5, 4.0) per interval "
                    "per edge from the single shared stream "
                    "default_rng(201201) consumed in deposit order; "
                    "alternating ON/OFF starting ON; truncated at "
                    "T=2400; geometry exp142-verbatim at PROBE_SEED"),
                "gates_source": ("module docstring, committed before "
                                 "any run (pre-registration commit "
                                 "e437f73)")},
            "config": {
                "seeds": list(SEEDS),
                "gen_seed_base": GEN_SEED_BASE,
                "schedule_urn_seed": SCHEDULE_URN_SEED,
                "n_media": N_MEDIA, "n_mild": N_MILD,
                "T": T_BATTERY, "k_chords": K_CHORDS,
                "probe_seed": PROBE_SEED,
                "families": list(FAMILIES), "ladder": list(LADDER),
                "threshold": THRESHOLD,
                "read_config": READ_CONFIG,
                "fingerprint": FP_PRE,
                "jobs_run": jobs, "smoke": bool(args.smoke),
                "instrument_pin": {
                    "constant": "NEURAL_SPEC_MIN",
                    "pinned_to": DEP148_FLOOR,
                    "saved_values": _PIN_SAVE,
                    "modules": [m.__name__ for m in PIN_MODULES],
                    "note": ("exp167's import-time pin has already "
                             "restored the -35.0 world before this "
                             "module's _PIN_SAVE captures it; "
                             "pin/restore asserted around every run "
                             "(the -35.0 pin is load-bearing: the "
                             "battery geometry's head sets depend on "
                             "it)")},
        }})
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
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
