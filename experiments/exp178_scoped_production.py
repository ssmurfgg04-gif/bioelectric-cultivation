#!/usr/bin/env python3
"""exp178 — THE SCOPED READ TO PRODUCTION (the adoption, closed).

exp169's registered next (L148 (i)): "the scoped read as the ADOPTION
candidate for exp148's production temporal read (the diagnostic
clause is one function, zero knobs)". exp167 adopted R_T blanket and
was falsified (A2 0/12); exp169 scoped it and reconciled both
channels (4/4). This experiment wires the scoped read into the
PRODUCTION dispatch — exp148's decode gains the arm "scoped" — with
the bit-exact-at-every-old-operating-point audit exp168's CF-1
adoption set as the standard.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Wiring, audits, and gates are fixed now.

THE WIRING (one arm, one function, cited file):
  experiments/exp148_temporal_read.py — the decode dispatch gains
  arm "scoped": f_max from the medium's frames (exp169's
  f_max_frames VERBATIM, PAIR-JOINT max for paired constructions),
  then R_T (exp167's adopted path) iff f_max < 32.0 else the
  existing "temporal" arm's code path UNCHANGED. The existing arms
  ("temporal", "phase", "mag", "sign") are untouched — the scoped
  arm is ADDITIVE. No existing caller changes behavior (the default
  arm is whatever it was; "scoped" must be requested).

GATES (each evaluated exactly once):

  GATE-A1 (T=1 static bit-exactness — the automatic safety) on
           exp148's static N4 controls (the exp73 torus battery,
           exp142's signed/complex_phase 4-instance subsets,
           exp145's reactive subset): f_max == 0 < 32 at T = 1 ->
           the rule selects R_T, and rule_temporal_core at T = 1 is
           the no-op identity (core = the frame's own support), so
           the scoped arm's final V is BIT-IDENTICAL to the temporal
           arm's per seed, verify preserved, errs bit-identical to
           exp148's deposited static records.
  GATE-A2 (concentrated side unchanged) the 12 flip-clock battery
           pairs under the scoped arm: pair-joint f_max >= 32 ->
           the raw temporal path — errs and verdicts BIT-IDENTICAL
           to exp148's deposited temporal records (12/12 separation,
           12/12 blindness).
  GATE-A3 (diffuse side = the adopted read) the corner spot set
           under the scoped arm: BIT-IDENTICAL to exp167's A3
           adopted errs (median 0.535 replayed, 20/20 media; clean
           cell no-op bit-exact vs exp166's arm-A).
  GATE-A4 (grid no-regression + hygiene) the schedule grid under
           the scoped arm: zero rejections, pooled median <= 0.685
           (exp148's deposited temporal median), per-instance
           classification identical to exp169's S4 (all diffuse);
           the tests suite green POST-wiring (`python3 -m
           tests.run_tests` exits 0 — the additive arm touches no
           existing test).

INSTRUMENTS: exp148's module (post-wiring), exp169's f_max_frames +
THRESHOLD imported VERBATIM (one source of truth for the diagnostic),
exp167's adopted path, the -35.0 instrument pin for every replay
against pre-CF-1 deposits (save/restore asserted), seeds (1, 2, 3).

NO post-hoc tuning. A --smoke check (1 torus instance + 1 battery
pair) is permitted before the credited run and discarded.

DEPOSIT: results/exp178_scoped_production.json

RUN:
  python3 -m experiments.exp178_scoped_production            # full
  python3 -m experiments.exp178_scoped_production --smoke    # check
  python3 -m experiments.exp178_scoped_production --job A2   # split
  # jobs: A1 | A2 | A3 | A4
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

from experiments.exp148_temporal_read import (  # noqa: E402
    FAMILIES, FlipGridMedium, FlipPairMedium, GRID_BASE_SEED,
    GRID_CLASSES, LADDER, N1_MIN_BLIND, N2_MIN_SEPARATION, N3_BAR,
    N_INSTANCES, N_INSTANCES_400, SCHED_SEED,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames,
)
from experiments.exp167_rt_adopted import (  # noqa: E402
    RTMasked, CORNER_CELL, CLEAN_CELL, SPOT_J, SPOT_SEEDS,
)

# ---- INSTRUMENT PIN -------------------------------------------------
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


OUT = os.path.join(ROOT, "results", "exp178_scoped_production.json")
DEP148 = os.path.join(ROOT, "results", "exp148_temporal_read.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")
DEP167 = os.path.join(ROOT, "results", "exp167_rt_adopted.json")


# ============================ MODULE BODY (run agent; gates fixed) ====
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")
GATE_NAMES = {"A1": "A1_static_bit_exact",
              "A2": "A2_concentrated_unchanged",
              "A3": "A3_diffuse_adopted",
              "A4": "A4_grid_no_regression_and_hygiene"}


def _wall() -> float:
    return os.times()[4]


def _load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _arm_scoped(medium, seeds: list[int],
                f_max: float | None = None) -> tuple[dict, int]:
    """THE RULE as an arm record THROUGH exp148's PRODUCTION dispatch
    (post-wiring): decode('scoped', ...). Rejections recorded, never
    raised; returns the record and the rejection count. f_max: the
    precomputed diagnostic value (PAIR-JOINT max for paired
    constructions; None => the arm computes it from the medium's own
    frames via exp169's f_max_frames inside the wired read)."""
    errs, vs, keys, rej = [], [], [], 0
    for s in seeds:
        out = _m148.decode("scoped", medium, s, f_max=f_max)
        if not out["ok"]:
            rej += 1
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(_m148.outcome_key(out))
    return ({"errs": errs, "verify": vs, "keys": keys,
             "majority": bool(np.mean(vs) > 0.5)}, rej)


def _arm(arm: str, medium, seeds: list[int]) -> dict:
    """exp148's run_arm shape (untouched arms, via the same dispatch)."""
    return _m148.run_arm(arm, medium, seeds)


def _pair_fmax(m_per, m_aper) -> dict:
    """exp169's diagnostic on a paired construction VERBATIM: f_max
    (pair) = max over the two schedule members (exp169's f_max_frames;
    cross-checked against exp148's lazy flip_clock_matrix — the same
    number on these media)."""
    f_per = f_max_frames(list(m_per.snapshots()))
    f_aper = f_max_frames(list(m_aper.snapshots()))
    assert f_per == float(_m148.flip_clock_matrix(m_per).max()), \
        f"f_max mismatch per: {f_per}"
    assert f_aper == float(_m148.flip_clock_matrix(m_aper).max()), \
        f"f_max mismatch aper: {f_aper}"
    return {"f_max_per": f_per, "f_max_aper": f_aper,
            "pair_f_max": max(f_per, f_aper)}


# ------------------------------------------------------------- gate A1
def _section_static(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-A1: T=1 static bit-exactness (the automatic safety) on
    exp148's static N4 controls: f_max == 0 < 32 at T = 1 -> the rule
    selects R_T; the scoped arm's final V BIT-IDENTICAL to the temporal
    arm's per seed, verify preserved, errs bit-identical to exp148's
    deposited static records."""
    dep148 = _load(DEP148)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    rejections = 0
    # (i) torus control (exp73 battery)
    ctrl: dict = {"substrate": "torus"}
    bit_ok, verify_ok, replay_ok, branch_ok = True, True, True, True
    temporal_errs, scoped_errs = [], []
    dep_torus = {s: dep148["control"]["temporal_errs"][k]
                 for k, s in enumerate(SPOT_SEEDS)}
    for s in seeds:
        m = _m148._StaticMedium(_m148.make_battery()["torus"])
        T = len(m.snapshots())
        fm = f_max_frames(list(m.snapshots()))
        out_t = _m148.decode("temporal", m, s, return_state=True)
        out_s = _m148.decode("scoped", m, s, return_state=True)
        rejections += sum(1 for r in (out_t, out_s) if not r["ok"])
        temporal_errs.append(out_t.get("err"))
        scoped_errs.append(out_s.get("err"))
        same = (out_t["ok"] and out_s["ok"] and np.array_equal(
            np.asarray(out_t["state"]["V"]),
            np.asarray(out_s["state"]["V"])))
        bit_ok &= bool(same)
        verify_ok &= (out_t.get("verified") == out_s.get("verified"))
        replay_ok &= bool(out_s["ok"] and out_s.get("err")
                          == dep_torus.get(s))
        branch_ok &= bool(fm == 0.0 and fm < THRESHOLD and T == 1)
    ctrl.update(T=1, f_max=0.0, rule_branch="R_T",
                temporal_errs=temporal_errs, scoped_errs=scoped_errs,
                bit_identical=bool(bit_ok), verify_preserved=bool(verify_ok),
                replay_vs_deposit=bool(replay_ok))
    print(f"  A1 torus: bit-identical {bit_ok} verify_preserved "
          f"{verify_ok} replay_vs_deposit {replay_ok} "
          f"rule_branch R_T {branch_ok}")

    # (ii) exp142's signed / complex_phase 4-instance subsets
    n4: dict = {}
    dep_n4 = dep148["n4_classes"]
    dep_signed = {(r["i"], r["seed"]): r["temporal_err"]
                  for r in dep_n4["signed"]["instances"]}
    dep_complex = {(r["i"], r["seed"]): r["temporal_err"]
                   for r in dep_n4["complex_phase"]["instances"]}
    for kind, builder, dep_map in (
            ("signed", lambda i: _m148.SignedMedium(100, seed=10_000 + i),
             dep_signed),
            ("complex_phase",
             lambda i: _m148.ComplexMedium(100, seed=20_000 + i),
             dep_complex)):
        recs, bit_identical, replay, n_cmp = [], 0, 0, 0
        for i in range(4):
            med = builder(i)
            T = len(med.snapshots())
            fm = f_max_frames(list(med.snapshots()))
            branch_ok &= bool(fm == 0.0 and fm < THRESHOLD and T == 1)
            for s in seeds:
                out_t = _m148.decode("temporal", med, s)
                out_s = _m148.decode("scoped", med, s)
                rejections += sum(1 for r in (out_t, out_s)
                                  if not r["ok"])
                same = (out_t["ok"] and out_s["ok"]
                        and out_t["err"] == out_s["err"]
                        and out_t["verified"] == out_s["verified"])
                hit = bool(out_s["ok"] and out_s["err"]
                           == dep_map.get((i, s)))
                bit_identical += int(same)
                replay += int(hit)
                n_cmp += 1
                recs.append({"i": i, "seed": s, "f_max": fm,
                             "rule_branch": "R_T",
                             "temporal_err": out_t.get("err"),
                             "scoped_err": out_s.get("err"),
                             "bit_identical": bool(same),
                             "replay_vs_deposit": hit})
        n4[kind] = {"instances": recs, "bit_identical_pairs": bit_identical,
                    "replay_pairs": replay, "n_pairs": n_cmp}
        print(f"  A1 {kind:14s} bit-identical {bit_identical}/{n_cmp} "
              f"replay {replay}/{n_cmp}")

    # (iii) exp145's reactive subset
    dep_react = {(r["n"], r["i"], r["s"], r["seed"]): r["temporal_err"]
                 for r in dep_n4["reactive_grid_subset"]["instances"]}
    reactive_recs, reactive_bit, reactive_replay, reactive_cmp = \
        [], 0, 0, 0
    for (n, i) in ((100, 0), (100, 1), (400, 8)):
        for s_cls in (1, -1):
            med = _m148.ReactiveMedium(n, seed=_m148.EXP145_GRID_BASE_SEED
                                       + i, s=s_cls)
            T = len(med.snapshots())
            fm = f_max_frames(list(med.snapshots()))
            branch_ok &= bool(fm == 0.0 and fm < THRESHOLD and T == 1)
            for s in seeds:
                out_t = _m148.decode("temporal", med, s)
                out_s = _m148.decode("scoped", med, s)
                rejections += sum(1 for r in (out_t, out_s)
                                  if not r["ok"])
                same = (out_t["ok"] and out_s["ok"]
                        and out_t["err"] == out_s["err"]
                        and out_t["verified"] == out_s["verified"])
                hit = bool(out_s["ok"] and out_s["err"]
                           == dep_react.get((n, i, s_cls, s)))
                reactive_bit += int(same)
                reactive_replay += int(hit)
                reactive_cmp += 1
                reactive_recs.append({"n": n, "i": i, "s": s_cls,
                                      "seed": s, "f_max": fm,
                                      "rule_branch": "R_T",
                                      "temporal_err": out_t.get("err"),
                                      "scoped_err": out_s.get("err"),
                                      "bit_identical": bool(same),
                                      "replay_vs_deposit": bool(hit)})
    n4["reactive_grid_subset"] = {
        "instances": reactive_recs, "bit_identical_pairs": reactive_bit,
        "replay_pairs": reactive_replay, "n_pairs": reactive_cmp}
    print(f"  A1 reactive_grid     bit-identical {reactive_bit}/"
          f"{reactive_cmp} replay {reactive_replay}/{reactive_cmp}")

    gate = {"pass": bool(bit_ok and verify_ok and replay_ok and branch_ok
                         and rejections == 0
                         and n4["signed"]["bit_identical_pairs"]
                         == n4["signed"]["n_pairs"]
                         and n4["signed"]["replay_pairs"]
                         == n4["signed"]["n_pairs"]
                         and n4["complex_phase"]["bit_identical_pairs"]
                         == n4["complex_phase"]["n_pairs"]
                         and n4["complex_phase"]["replay_pairs"]
                         == n4["complex_phase"]["n_pairs"]
                         and n4["reactive_grid_subset"]
                         ["bit_identical_pairs"]
                         == n4["reactive_grid_subset"]["n_pairs"]
                         and n4["reactive_grid_subset"]["replay_pairs"]
                         == n4["reactive_grid_subset"]["n_pairs"]),
            "torus_bit_identical": bool(bit_ok),
            "torus_verify_preserved": bool(verify_ok),
            "torus_replay_vs_deposit": bool(replay_ok),
            "rule_selects_rt_all_static": bool(branch_ok),
            "signed": {k: n4["signed"][k]
                       for k in ("bit_identical_pairs", "replay_pairs",
                                 "n_pairs")},
            "complex_phase": {k: n4["complex_phase"][k]
                              for k in ("bit_identical_pairs",
                                        "replay_pairs", "n_pairs")},
            "reactive": {k: n4["reactive_grid_subset"][k]
                         for k in ("bit_identical_pairs", "replay_pairs",
                                   "n_pairs")},
            "rejections": rejections, "smoke": bool(smoke)}
    section = {"control": ctrl, "n4_classes": n4, "runtime_s": 0.0}
    return section, gate, rejections


# ------------------------------------------------------------- gate A2
def _section_battery(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-A2: the 12 flip-clock battery pairs under the scoped arm:
    PAIR-JOINT f_max >= 32 -> the raw temporal path — errs and verdicts
    BIT-IDENTICAL to exp148's deposited temporal records (12/12
    separation, 12/12 blindness). exp169's S2 battery structure."""
    dep148 = _load(DEP148)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    fams = FAMILIES[:1] if smoke else FAMILIES
    doses = LADDER[:1] if smoke else LADDER
    dep_pairs = {(p["family"], p["dose"]): p
                 for p in dep148["probes"]["pairs"]}
    pairs, rejections = [], 0
    n_sep = n_blind = 0
    for fam in fams:
        fi = FAMILIES.index(fam)
        for b in doses:
            di = LADDER.index(b)
            ss = SCHED_SEED + 4 * fi + di
            m_per = FlipPairMedium(b, fam, "per", sched_seed=ss)
            m_aper = FlipPairMedium(b, fam, "aper", sched_seed=ss)
            fm = _pair_fmax(m_per, m_aper)
            scoped_p, rej_p = _arm_scoped(m_per, seeds, f_max=fm["pair_f_max"])
            scoped_a, rej_a = _arm_scoped(m_aper, seeds,
                                          f_max=fm["pair_f_max"])
            rejections += rej_p + rej_a
            phase_p = _arm("phase", m_per, seeds)
            phase_a = _arm("phase", m_aper, seeds)
            dep = dep_pairs[(fam, b)]
            d_per = dep["arms"]["per_temporal"]
            d_aper = dep["arms"]["aper_temporal"]
            replay = (scoped_p["errs"] == d_per["errs"][:len(seeds)]
                      and scoped_p["majority"] == d_per["majority"]
                      and scoped_a["errs"] == d_aper["errs"][:len(seeds)]
                      and scoped_a["majority"] == d_aper["majority"])
            sep = scoped_p["majority"] != scoped_a["majority"]
            blind = bool(_m148.verdict_blind(phase_p, phase_a))
            n_sep += int(sep)
            n_blind += int(blind)
            pairs.append({
                "family": fam, "dose": b, "sched_seed": ss,
                "f_max_per": fm["f_max_per"],
                "f_max_aper": fm["f_max_aper"],
                "pair_f_max": fm["pair_f_max"],
                "scoping_class": "concentrated"
                if fm["pair_f_max"] >= THRESHOLD else "diffuse",
                "rule_branch": "raw_temporal"
                if fm["pair_f_max"] >= THRESHOLD else "R_T",
                "scoped": {"per_errs": scoped_p["errs"],
                           "per_majority": scoped_p["majority"],
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
            print(f"  A2 {fam:17s} b={b:6.1f} pair_f_max="
                  f"{fm['pair_f_max']:.0f} replay={replay} sep={sep} "
                  f"phaseBlind={blind}")
    n_pairs = len(pairs)
    gate = {"pass": bool(
        n_pairs > 0
        and all(p["scoped_replay_bit_exact_vs_deposit"] for p in pairs)
        and all(p["scoping_class"] == "concentrated" for p in pairs)
        and all(p["rule_branch"] == "raw_temporal" for p in pairs)
        and n_sep == n_pairs and n_blind == n_pairs
        and rejections == 0
        and (smoke or (n_sep >= N2_MIN_SEPARATION
                       and n_blind >= N1_MIN_BLIND))),
        "n_pairs": n_pairs,
        "n_separated_scoped": n_sep, "required_n2": N2_MIN_SEPARATION,
        "n_phase_blind_reproduced": n_blind, "required_n1": N1_MIN_BLIND,
        "rejections": rejections, "smoke": bool(smoke)}
    section = {"pairs": pairs, "n_pairs": n_pairs, "runtime_s": 0.0}
    return section, gate, rejections


# ------------------------------------------------------------- gate A3
def _section_corner(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-A3: the corner spot set under the scoped arm IS exp167's
    adopted read bit-exactly (median 0.535 replayed, 20/20 media); the
    clean cell no-op bit-exact vs exp166's arm-A. exp169's S3 corner
    structure."""
    from experiments.exp166_leading_edge import (   # body import (exp167
        CornerMedium, SEED_BASE as EXP166_SEED_BASE, cell_dims)  # carries it
    dep166 = _load(DEP166)
    dep167 = _load(DEP167)
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
                               dims=cell_dims(cell))
            fm = f_max_frames(list(med.snapshots()))
            arm, rej = _arm_scoped(med, seeds, f_max=fm)
            rejections += rej
            rec = {"tag": tag, "cell": cell, "j": j, "gen_seed": med.seed,
                   "T": len(med.snapshots()), "f_max": fm,
                   "scoping_class": "diffuse" if fm < THRESHOLD
                   else "concentrated",
                   "rule_branch": "R_T" if fm < THRESHOLD else "raw_temporal",
                   "errs_scoped": arm["errs"],
                   "verified_scoped": arm["verify"]}
            if tag == "corner":
                ref = spot167[("corner", j)]["errs_adopted"][:len(seeds)]
                rec["ref_source"] = "exp167_A3_errs_adopted"
            else:
                ref = spot166[("clean", j)]["errs_armA"][:len(seeds)]
                rec["ref_source"] = "exp166_clean_errs_armA"
            rec["ref_errs"] = ref
            rec["replay_bit_exact"] = arm["errs"] == ref
            fin = [e for e in arm["errs"] if e is not None]
            rec["median_scoped"] = (float(np.median(fin)) if fin else None)
            replay[tag] += int(rec["replay_bit_exact"])
            n_media[tag] += 1
            if rec["median_scoped"] is not None:
                medians[tag].append(rec["median_scoped"])
            instances.append(rec)
        med_s = (float(np.median(medians[tag])) if medians[tag] else None)
        print(f"  A3 {tag}: replay {replay[tag]}/{n_media[tag]} "
              f"median {med_s}")
    corner_median = (float(np.median(medians["corner"]))
                     if medians["corner"] else None)
    dep_corner_median = dep167["corner_spot"]["corner_median_after"]
    gate = {"pass": bool(replay["corner"] == n_media["corner"]
                         and replay["clean"] == n_media["clean"]
                         and n_media["corner"] + n_media["clean"] == 20
                         and all(r["scoping_class"] == "diffuse"
                                 for r in instances)
                         and all(r["rule_branch"] == "R_T"
                                 for r in instances)
                         and rejections == 0
                         and (smoke
                              or corner_median == dep_corner_median)),
            "corner_replay_bit_exact": [replay["corner"],
                                        n_media["corner"]],
            "clean_replay_bit_exact": [replay["clean"], n_media["clean"]],
            "n_media_replayed": n_media["corner"] + n_media["clean"],
            "corner_median_scoped": corner_median,
            "corner_median_deposited_exp167": dep_corner_median,
            "rejections": rejections, "smoke": bool(smoke)}
    section = {"instances": instances, "runtime_s": 0.0}
    return section, gate, rejections


# ------------------------------------------------------------- gate A4
def _section_grid(smoke: bool) -> tuple[dict, dict, int]:
    """GATE-A4: the schedule grid under the scoped arm — zero
    rejections, pooled median <= 0.685 (exp148's deposited temporal
    median), per-instance classification identical to exp169's S4 (all
    diffuse); plus the tests suite green POST-wiring (`python3 -m
    tests.run_tests` exits 0). exp169's S4 grid structure."""
    dep148 = _load(DEP148)
    dep169 = _load(DEP169)
    seeds = [1] if smoke else list(SPOT_SEEDS)
    inst_range = list(range(1)) if smoke else \
        list(range(N_INSTANCES + N_INSTANCES_400))
    bar = dep148["gates"]["N3_schedule_fidelity"]["pooled_temporal_median"]
    s4 = {(r["cls"], r["i"]): r
          for r in dep169["sections"]["grid"]["instances"]}

    # pass 1 — per-instance f_max and class, recorded BEFORE the pooled
    # verdict (the diagnostic's prediction work)
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

    # pass 2 — the scoped decodes through the production dispatch
    rejections = 0
    errs_all: list[float] = []
    for rec in instances:
        med = FlipGridMedium(rec["n"], seed=rec["gen_seed"],
                             sched=GRID_CLASSES[rec["cls"]])
        arm, rej = _arm_scoped(med, seeds, f_max=rec["f_max"])
        rejections += rej
        rec["errs_scoped"] = arm["errs"]
        rec["verified_scoped"] = arm["verify"]
        errs_all.extend(e for e in arm["errs"] if e is not None)

    pooled = float(np.median(errs_all)) if errs_all else None
    cls_hits = [r for r in instances if (r["cls"], r["i"]) in s4]
    classification_identical = bool(cls_hits) and all(
        r["class"] == s4[(r["cls"], r["i"])]["class"]
        and r["f_max"] == s4[(r["cls"], r["i"])]["f_max"]
        for r in cls_hits)
    all_diffuse = all(r["class"] == "diffuse" for r in instances)

    # the tests suite, POST-wiring (gate A4's hygiene clause)
    proc = subprocess.run([sys.executable, "-m", "tests.run_tests"],
                          cwd=ROOT, capture_output=True, text=True,
                          timeout=1800)
    tests_tail = (proc.stdout or "")[-2000:]
    tests_ok = bool(proc.returncode == 0)

    gate = {"pass": bool(rejections == 0
                         and pooled is not None and pooled <= bar
                         and classification_identical and all_diffuse
                         and tests_ok),
            "pooled_scoped_median": pooled,
            "bar_exp148_deposited_temporal_median": bar,
            "no_regression": bool(pooled is not None and pooled <= bar),
            "classification_identical_to_exp169_S4":
                classification_identical,
            "all_diffuse": bool(all_diffuse),
            "n_instances": len(instances),
            "n_diffuse": sum(1 for r in instances
                             if r["class"] == "diffuse"),
            "n_concentrated": sum(1 for r in instances
                                  if r["class"] == "concentrated"),
            "zero_rejections": bool(rejections == 0),
            "rejections": rejections,
            "tests_post_wiring": {
                "command": "python3 -m tests.run_tests",
                "exit_code": proc.returncode, "green": tests_ok,
                "tail": tests_tail},
            "smoke": bool(smoke)}
    section = {"instances": instances,
               "pooled_scoped_median": pooled,
               "rejections": rejections, "runtime_s": 0.0}
    return section, gate, rejections


SECTIONS = {"A1": _section_static, "A2": _section_battery,
            "A3": _section_corner, "A4": _section_grid}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 torus instance + 1 battery "
                         "pair — discarded, no deposit")
    ap.add_argument("--job", choices=["A1", "A2", "A3", "A4", "all"],
                    default="all",
                    help="runner split; each job evaluates its own gate "
                         "exactly once and merges into the deposit")
    ap.add_argument("--out", default=None,
                    help="deposit path override (default %s)" % OUT)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    t0 = _wall()
    # the registered smoke scope: 1 torus instance (A1) + 1 battery
    # pair (A2); A3/A4 are not part of the permitted smoke check
    jobs = ["A1", "A2", "A3", "A4"] if args.job == "all" else [args.job]
    if args.smoke:
        jobs = [j for j in jobs if j in ("A1", "A2")]
    mode = ("SMOKE instrument check - discarded" if args.smoke
            else "FULL jobs=" + ",".join(jobs))
    print(f"=== exp178: THE SCOPED READ TO PRODUCTION ({mode}) ===\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP148_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP148_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}")
    print(f"  wiring: exp148's decode dispatch post-wiring — arms "
          f"{('mag', 'sign', 'phase', 'temporal', 'scoped')}, the "
          f"scoped arm ADDITIVE (exp169's f_max_frames + THRESHOLD "
          f"{THRESHOLD} verbatim)\n")

    # merged deposit: split runs accumulate sections across invocations
    result: dict = {}
    if not args.smoke and args.job != "all" and os.path.exists(out_path):
        result = _load(out_path)
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
            "exp": "exp178_scoped_production",
            "claim": (
                "THE SCOPED READ TO PRODUCTION (the adoption, closed): "
                "exp148's production decode dispatch gains the ADDITIVE "
                "arm 'scoped' — exp169's f_max diagnostic VERBATIM (one "
                "source of truth) with the pre-registered threshold "
                "32.0, PAIR-JOINT max for paired constructions; R_T "
                "(exp167's adopted path) iff f_max < 32.0 else the "
                "existing raw temporal path UNCHANGED, no existing arm "
                "touched — and every old operating point is audited "
                "bit-exactly: static controls bit-identical to the "
                "temporal arm and to exp148's deposited records (A1), "
                "the concentrated battery side IS exp148's raw temporal "
                "bit-exactly with 12/12 separation and blindness (A2), "
                "the diffuse corner side IS exp167's adopted read "
                "bit-exactly (A3), the grid shows zero rejections and "
                "no fidelity regression with the exp169 S4 "
                "classification replayed (A4), and the tests suite is "
                "green POST-wiring"),
            "pre_registration": {
                "wiring": ("experiments/exp148_temporal_read.py — the "
                           "decode dispatch gains arm 'scoped': f_max "
                           "from the medium's frames (exp169's "
                           "f_max_frames VERBATIM, PAIR-JOINT max for "
                           "paired constructions, passed through the "
                           "arm's optional f_max argument; None => "
                           "computed from the medium's own frames), "
                           "then R_T (exp167's adopted path) iff "
                           "f_max < 32.0 else the existing 'temporal' "
                           "arm's code path UNCHANGED; the existing "
                           "arms ('temporal', 'phase', 'mag', 'sign') "
                           "untouched — the scoped arm is ADDITIVE"),
                "threshold": THRESHOLD,
                "rule": ("apply R_T (exp167's adopted read) iff "
                         "f_max < 32.0, else exp148's raw temporal "
                         "read; one threshold, no outcome feedback"),
                "gates_source": ("module docstring, committed before "
                                 "any run (pre-registration commit "
                                 "fc5f601)")},
            "config": {
                "seeds": list(SPOT_SEEDS),
                "spot_j": list(SPOT_J),
                "corner_cell": CORNER_CELL, "clean_cell": CLEAN_CELL,
                "grid_base_seed": GRID_BASE_SEED,
                "n_instances": N_INSTANCES,
                "n_instances_400": N_INSTANCES_400,
                "families": list(FAMILIES), "ladder": list(LADDER),
                "sched_seed_base": SCHED_SEED,
                "jobs_run": jobs, "smoke": bool(args.smoke),
                "instrument_pin": {
                    "constant": "NEURAL_SPEC_MIN",
                    "pinned_to": DEP148_FLOOR,
                    "saved_values": _PIN_SAVE,
                    "modules": [m.__name__ for m in PIN_MODULES],
                    "note": ("both replay reference worlds "
                             "(exp148/exp166/exp167 deposits) predate "
                             "CF-1; the floor is pinned to -35.0 for "
                             "every replay, save/restore asserted")},
                "wired_module": "experiments/exp148_temporal_read.py"
                " (post-wiring; the scoped arm is the only consumer of "
                "exp167/exp169's lazy imports)"},
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
    ap.add_argument("--job", choices=["A1", "A2", "A3", "A4", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
