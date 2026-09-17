#!/usr/bin/env python3
"""exp167 — R_T ADOPTED (the temporal read at T > 1 media).

exp166's registered next (L145): "R_T as a zero-knob ADOPTION candidate
into exp148's read_temporal for temporal media (one clause: mask frames
to the core support when T > 1 — the bit-exact clean-cell no-op property
is the adoption-safety proof)". exp166's deposit (P4) priced the corner
cell and attributed its excess to "the TC1 flip-clock channel's own
response to presence transitions", repaired at the medium level by R_T
(corner median 1.015 -> 0.535 mV, clean cell bit-identical no-op).
THIS EXPERIMENT runs the adoption: exp148's read with the ONE clause,
on exp148's OWN deposited batteries (its 12 adversarial flip-clock
pairs + schedule-class grid + static N4 controls, re-run from exp148's
module VERBATIM via imports) plus exp166's corner spot set.

========================= PRE-REGISTRATION =========================
Deposited BEFORE any decode (this file is committed before the credited
run; gates, instruments, and the composed rule below are fixed now).

THE ADOPTED READ — the composed rule, stated exactly ONCE (zero knobs):
  In exp148's TC1-TC3 temporal read, ONE clause is added: when the
  medium's read window has T > 1 frames, EVERY frame is first masked to
  the across-frame CORE support (present in EVERY frame; exp166's
  rule_temporal_core applied verbatim per frame — membership frozen,
  zero presence transitions). TC1-TC3 then run VERBATIM on the masked
  frames: A = exp145's PN1/PN2 projected time-average of the MASKED
  frames (rho >= 0.5 -> Im branch, else Re), F = TC1 raw per-edge
  presence-transition counts of the MASKED frames, A_ext = A + F, and
  exp142's execute_signed VERBATIM on A_ext. At T = 1 no mask applies.
  ANALYTIC CONSEQUENCE (part of the rule, not an outcome): frozen
  membership makes every TC1 transition count zero, so F == 0 and
  A_ext = A_masked — the adopted read IS the flip-quiet window's phase
  read; on static media (T = 1) it is bitwise exp148's temporal read,
  which is bitwise exp145's read (exp148's N4 reduction, untouched).
  REGISTERED TENSION (named before the run): exp148's schedule semantics
  live ONLY on non-core flip edges, which the core mask removes; the
  gate A2 below tests whether exp166's repair (silence the flip clock)
  and exp148's channel (hear the flip clock) can co-exist under ONE
  zero-knob clause. Whatever the outcome, it is deposited.

INSTRUMENTS (zero new calibration; everything from the deposits):
  * exp148's module imported verbatim: FlipPairMedium (12 pairs =
    FAMILIES x LADDER, sched seeds 11 + 4*fi + di), FlipGridMedium
    (GRID_BASE_SEED 148_000 + i, 8 instances n=100 + 2 at n=400, both
    schedule classes), the static N4 controls (exp73 torus, exp142
    signed/complex_phase 4-instance subsets, exp145 reactive subset),
    its decode/dispatch for the phase arm, its constants (N3_BAR 0.60,
    N2_MIN_SEPARATION 10, N1_MIN_BLIND 11), seeds = exp142's SEEDS
    (1, 2, 3).
  * exp166's corner spot set verbatim: CornerMedium(n=100,
    seed = 166166 + 1000*c + j) with cell c = 7 (corner o+h+t,
    j = 0..9) and c = 0 (clean, j = 0..9), seeds (1, 2, 3) — 120
    adopted decodes; replay-compared bit-exactly against exp166's
    deposited arm-A / arm-B errs (the adoption-safety proof).
  * INSTRUMENT PIN (disclosed, pre-run; exp168's OLD_FLOOR_PIN
    mechanism): BOTH replay references (exp148's and exp166's
    deposits) were produced at the pre-CF-1 production floor
    NEURAL_SPEC_MIN = -35.0, while the working tree now carries
    exp168's CF-1 patch (-60.0, pre-registration 2f9f785). The smoke
    instrument check caught the consequence BEFORE this
    pre-registration commit: at -60.0 exp148's chord_set is an
    INVALID instrument (F1/F3 chord destination lists empty ->
    ZeroDivisionError) and every decode target shifts (grid replay
    errs move). The floor is therefore PINNED to the deposited
    -35.0 in every module whose bound name this read chain consults
    (cultivation.bioelectric.collective, exp142, exp145, exp148,
    exp94) — the one constant, nothing else, restored-world
    semantics exactly as exp148/exp166 ran. Recorded in the deposit.
  * Deposits read at run time for replay comparisons:
    results/exp148_temporal_read.json, results/exp166_leading_edge.json
    (errs are recorded at execute_signed's 2-dp precision; replay
    comparisons are exact float equality on those records).

PRE-REGISTERED GATES (fixed before the registered run):

  GATE-A1 (adoption safety on STATIC media, at the deposited
           batteries) exp148's N1-N4 static facts hold under the
           adopted read BIT-EXACTLY:
           (i) N4 machinery: torus control — adopted final V
           bit-identical to the phase arm's per seed, verify preserved;
           exp142's signed and complex_phase 4-instance subsets and
           exp145's reactive subset — adopted errs + verified
           bit-identical to the phase arm per (instance, seed) AND to
           exp148's DEPOSITED temporal-arm errs;
           (ii) N1 instrument replay: on all 12 battery pairs the raw
           phase projections are bitwise equal across members and the
           phase arm is verdict-blind (replaying exp148's deposited
           12/12), the mag/sign arms being untouched code paths.
           PASS = every comparison bit-exact.
  GATE-A2 (registered expectation: separation survives AND fidelity
           improves) on the 12 flip-clock pairs the adopted read's
           majority verdicts differ across members on >= 10/12 (as
           exp148's N2), AND on the paired schedule grid the adopted
           pooled median err improves on exp148's deposited temporal
           median (0.685 mV) toward N3's 0.60 bar (deposit median
           before/after; bar-crossing recorded).
           IF A2 FAILS: deposit WHICH pairs/schedules regressed
           (per-member verdict changes vs exp148's deposited temporal
           verdicts — R_T may discard real flip information on
           aperiodic media) and REGISTER THE SCOPING (R_T per-media?
           a pre-registered diagnostic in the style of PN1's rho?);
           the scoping is registered, NOT run here.
  GATE-A3 (exp166's corner spot set under the adopted read) the corner
           cell (c=7, j=0..9) median improves on exp166's deposited
           arm-A median (1.015 mV) and lands <= 0.60 mV; the clean cell
           (c=0, j=0..9) is BIT-EXACT vs exp166's deposited clean arm-A
           errs (the no-op clause under the adoption); the corner
           adopted errs replay exp166's deposited arm-B errs bit-exactly
           (the adoption-safety proof carries over).
           PASS = all three clauses.
  GATE-A4 (zero rejections) zero rejections and all errs finite across
           the whole run (exp142's hygiene, recorded never raised).

NO post-hoc knob tuning anywhere; exactly ONE composed rule is run.
Whatever the outcome, it is deposited. A --smoke instrument check (1
family x 1 dose, 1 grid instance/class, torus, corner j=0 only) is
permitted before the credited run and discarded; the credited full run
uses the committed script unchanged.

DEPOSIT: results/exp167_rt_adopted.json

RUN:
  python3 -m experiments.exp167_rt_adopted            # full (registered)
  python3 -m experiments.exp167_rt_adopted --smoke    # instrument check
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp137_universal_reader import ComplexMedium, SignedMedium
from experiments.exp142_sign_read import (
    SEEDS, _StaticMedium,
)
from experiments.exp145_phase_read import (
    GRID_BASE_SEED as EXP145_GRID_BASE_SEED,
    ReactiveMedium, project_phase_native,
)
from experiments.exp148_temporal_read import (
    FAMILIES, FlipGridMedium, FlipPairMedium, FrameSeq, GRID_BASE_SEED,
    GRID_CLASSES, LADDER, N1_MIN_BLIND, N2_MIN_SEPARATION, N3_BAR,
    N_INSTANCES, N_INSTANCES_400, SCHED_SEED, T_GRID,
    decode as exp148_decode, flip_clock_matrix, outcome_key, read_temporal,
    verdict_blind,
)
from experiments.exp166_leading_edge import (
    SEED_BASE as EXP166_SEED_BASE, CornerMedium, cell_dims,
)
from experiments.exp73_active_renormalization import make_battery
from experiments.exp94_multizone_scale import MULTI, labeling_bfs_n, spec_target_n

# ---- INSTRUMENT PIN (see docstring; exp168's OLD_FLOOR_PIN mechanism)
import cultivation.bioelectric.collective as _core_mod
import experiments.exp142_sign_read as _m142
import experiments.exp145_phase_read as _m145
import experiments.exp148_temporal_read as _m148
import experiments.exp94_multizone_scale as _m94

EXP148_FLOOR = -35.0             # the floor BOTH deposits ran at
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
PIN_RECORD = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
              for m in PIN_MODULES}
for _m in PIN_MODULES:
    if hasattr(_m, "NEURAL_SPEC_MIN"):
        _m.NEURAL_SPEC_MIN = EXP148_FLOOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp167_rt_adopted.json")
DEP148 = os.path.join(ROOT, "results", "exp148_temporal_read.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")

CORNER_CELL = 7                  # exp166's corner cell (o=h=t=1)
CLEAN_CELL = 0                   # exp166's clean cell
SPOT_J = list(range(10))         # exp166's spot instances per cell
SPOT_SEEDS = (1, 2, 3)           # exp166's seed protocol

cross_cache: dict = {}           # adopted cross-class outcome keys


# --------------------------- the ONE clause as a medium wrapper --------
class RTMasked:
    """The adoption clause: frames masked to the across-frame CORE
    support (exp166's rule_temporal_core applied per frame; the core is
    computed in ONE raw pass and frozen). snapshots() is a lazy,
    re-iterable FrameSeq — no eager materialization of long windows."""

    kind = "rt_masked"

    def __init__(self, inner):
        core = None
        T = 0
        for Wt in inner.snapshots():
            sup = np.abs(Wt) > 0
            core = sup if core is None else (core & sup)
            T += 1
        self._inner, self._core, self.T = inner, core, T
        self.n = core.shape[0]

    @property
    def violated(self):
        return getattr(self._inner, "violated", ())

    def snapshots(self):
        return FrameSeq(self._gen, self.T)

    def _gen(self):
        core = self._core
        for Wt in self._inner.snapshots():
            yield np.where(core, Wt, Wt.dtype.type(0))

    def native_support(self) -> np.ndarray:
        return self._core.astype(float)


def read_adopted(medium, seed: int, return_state: bool = False) -> dict:
    """The ADOPTED TEMPORAL READ (the composed rule, one clause): at
    T > 1 mask the frames to the across-frame core support, then run
    exp148's TC1-TC3 VERBATIM on the masked frames. At T = 1 the raw
    medium passes through (bitwise exp148's temporal read)."""
    if getattr(medium, "kind", "") != "rt_masked":
        if len(medium.snapshots()) > 1:
            medium = RTMasked(medium)          # the ONE clause (T > 1)
    return read_temporal(medium, seed, return_state)   # TC1-TC3 verbatim


# ------------------------------------------------------------ harness
def decode(arm: str, medium, seed: int,
           return_state: bool = False) -> dict:
    """exp148's decode policy with the adopted arm added; a rejection is
    RECORDED, never raised (exp142's zero-rejection hygiene)."""
    if arm != "adopted":
        return exp148_decode(arm, medium, seed, return_state)
    try:
        out = read_adopted(medium, seed, return_state)
        err = float(out["err_vs_target"])
        if not np.isfinite(err):
            raise ValueError(f"non-finite decode err {err}")
        return {"ok": True, "err": err,
                "verified": bool(out.get("program_verified", False)),
                "state": out.get("final_state"),
                "rho": out.get("rho"), "branch": out.get("branch")}
    except Exception as e:                                   # pragma: no cover
        return {"ok": False, "rejection": f"{type(e).__name__}: {e}"[:200]}


def run_arm(arm: str, medium, seeds: list[int]) -> dict:
    errs, vs, keys = [], [], []
    for s in seeds:
        out = decode(arm, medium, s)
        errs.append(out.get("err"))
        vs.append(bool(out.get("verified", False)))
        keys.append(outcome_key(out))
    return {"errs": errs, "verify": vs, "keys": keys,
            "majority": bool(np.mean(vs) > 0.5)}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="instrument check: 1 family x 1 dose, "
                         "1 grid instance/class, torus, corner j=0")
    args = ap.parse_args()
    seeds = list((1,) if args.smoke else SEEDS)
    fams = FAMILIES[:1] if args.smoke else FAMILIES
    doses = LADDER[:1] if args.smoke else LADDER
    n_inst = 1 if args.smoke else N_INSTANCES
    n_inst400 = 1 if args.smoke else N_INSTANCES_400
    spot_j = SPOT_J[:1] if args.smoke else SPOT_J
    t0 = time.time()
    print("=== exp167: R_T ADOPTED (the temporal read at T>1 media) ===\n")

    with open(DEP148) as f:
        dep148 = json.load(f)
    with open(DEP166) as f:
        dep166 = json.load(f)
    dep_pairs = {(p["family"], p["dose"]): p
                 for p in dep148["probes"]["pairs"]}

    rejections = 0
    gates: dict = {}

    # ---- GATE-A1(i): exp148's N4 static machinery under the adopted read
    ctrl: dict = {"substrate": "torus"}
    bit_ok, verify_ok, replay_ok = True, True, True
    phase_errs, adopted_errs = [], []
    dep_torus = {s: dep148["control"]["temporal_errs"][k]
                 for k, s in enumerate(SEEDS)}
    for si, s in enumerate(seeds):
        m = _StaticMedium(make_battery()["torus"])
        out_p = decode("phase", m, s, return_state=True)
        out_a = decode("adopted", m, s, return_state=True)
        rejections += sum(1 for r in (out_p, out_a) if not r["ok"])
        phase_errs.append(out_p.get("err"))
        adopted_errs.append(out_a.get("err"))
        same = (out_p["ok"] and out_a["ok"] and np.array_equal(
            np.asarray(out_p["state"]["V"]),
            np.asarray(out_a["state"]["V"])))
        bit_ok &= bool(same)
        verify_ok &= (out_p.get("verified") == out_a.get("verified"))
        replay_ok &= bool(out_a["ok"] and out_a.get("err")
                          == dep_torus.get(s))
    ctrl.update(phase_errs=phase_errs, adopted_errs=adopted_errs,
                bit_identical=bool(bit_ok), verify_preserved=bool(verify_ok),
                replay_vs_deposit_temporal=bool(replay_ok))
    print(f"  A1 torus: bit-identical {bit_ok} verify_preserved "
          f"{verify_ok} replay_vs_deposit {replay_ok}")

    n4_classes: dict = {}
    dep_n4 = dep148["n4_classes"]
    dep_signed = {(r["i"], r["seed"]): r["temporal_err"]
                  for r in dep_n4["signed"]["instances"]}
    dep_complex = {(r["i"], r["seed"]): r["temporal_err"]
                   for r in dep_n4["complex_phase"]["instances"]}
    for kind, builder, dep_map in (
            ("signed", lambda i: SignedMedium(100, seed=10_000 + i),
             dep_signed),
            ("complex_phase", lambda i: ComplexMedium(100, seed=20_000 + i),
             dep_complex)):
        recs, bit_identical, replay, n_cmp = [], 0, 0, 0
        for i in range(4):
            med = builder(i)
            for si, s in enumerate(seeds):
                out_p = decode("phase", med, s)
                out_a = decode("adopted", med, s)
                rejections += sum(1 for r in (out_p, out_a) if not r["ok"])
                same = (out_p["ok"] and out_a["ok"]
                        and out_p["err"] == out_a["err"]
                        and out_p["verified"] == out_a["verified"])
                dep_err = dep_map.get((i, s))
                hit = bool(out_a["ok"] and out_a["err"] == dep_err)
                bit_identical += int(same)
                replay += int(hit)
                n_cmp += 1
                recs.append({"i": i, "seed": s, "phase_err": out_p.get("err"),
                             "adopted_err": out_a.get("err"),
                             "bit_identical": bool(same),
                             "replay_vs_deposit": hit})
        n4_classes[kind] = {"instances": recs,
                            "bit_identical_pairs": bit_identical,
                            "replay_pairs": replay, "n_pairs": n_cmp}
        print(f"  A1 {kind:14s} bit-identical {bit_identical}/{n_cmp} "
              f"replay {replay}/{n_cmp}")

    reactive_recs, reactive_bit, reactive_replay, reactive_cmp = [], 0, 0, 0
    dep_react = {(r["n"], r["i"], r["s"], r["seed"]): r["temporal_err"]
                 for r in dep_n4["reactive_grid_subset"]["instances"]}
    for (n, i) in ((100, 0), (100, 1), (400, 8)):
        for s_cls in (1, -1):
            med = ReactiveMedium(n, seed=EXP145_GRID_BASE_SEED + i, s=s_cls)
            for s in seeds:
                out_p = decode("phase", med, s)
                out_a = decode("adopted", med, s)
                rejections += sum(1 for r in (out_p, out_a) if not r["ok"])
                same = (out_p["ok"] and out_a["ok"]
                        and out_p["err"] == out_a["err"]
                        and out_p["verified"] == out_a["verified"])
                hit = bool(out_a["ok"] and out_a["err"]
                           == dep_react.get((n, i, s_cls, s)))
                reactive_bit += int(same)
                reactive_replay += int(hit)
                reactive_cmp += 1
                reactive_recs.append({"n": n, "i": i, "s": s_cls, "seed": s,
                                      "phase_err": out_p.get("err"),
                                      "adopted_err": out_a.get("err"),
                                      "bit_identical": bool(same),
                                      "replay_vs_deposit": bool(hit)})
    n4_classes["reactive_grid_subset"] = {
        "instances": reactive_recs, "bit_identical_pairs": reactive_bit,
        "replay_pairs": reactive_replay, "n_pairs": reactive_cmp}
    print(f"  A1 reactive_grid     bit-identical {reactive_bit}/"
          f"{reactive_cmp} replay {reactive_replay}/{reactive_cmp}")

    # ---- GATE-A2: the paired schedule-class grid (fidelity before/after)
    dep_grid_lists: dict = {}
    dep_grid_ptr: dict = {}
    for cls2 in GRID_CLASSES:
        L: dict = {}
        for r in dep148["grid"][cls2]["instances"]:
            L.setdefault((r["n"], r["seed"]), []).append(r["err"])
        dep_grid_lists[cls2] = L
        dep_grid_ptr[cls2] = {}
    grid: dict = {}
    adopted_errs_all: list[float] = []
    replay_errs_all: list[float] = []
    adopted_blind_cross = 0
    cross_cmp = 0
    grid_replay_hits = 0
    grid_replay_cmp = 0
    for cls_name, sched in GRID_CLASSES.items():
        inst_rec, errs_a, errs_r, oks = [], [], [], []
        for i in range(n_inst + n_inst400):
            n = 400 if i >= n_inst else 100
            med = FlipGridMedium(n, seed=GRID_BASE_SEED + i, sched=sched)
            wrapped = RTMasked(med)
            A_nat = spec_target_n(MULTI, labeling_bfs_n(med.native_support()),
                                  n)
            A_nat_core = spec_target_n(MULTI,
                                       labeling_bfs_n(wrapped.native_support()),
                                       n)
            for si, s in enumerate(seeds):
                out_r = decode("temporal", med, s, return_state=True)
                out_a = decode("adopted", wrapped, s, return_state=True)
                rejections += sum(1 for r in (out_r, out_a) if not r["ok"])
                rec = {"n": n, "seed": s}
                if out_r["ok"]:
                    V = np.asarray(out_r["state"]["V"])
                    errs_r.append(out_r["err"])
                    replay_errs_all.append(out_r["err"])
                    rec["before_temporal_err"] = out_r["err"]
                    rec["err_native"] = round(
                        float(np.sqrt(np.mean((V - A_nat) ** 2))), 2)
                    k = (n, s)
                    L = dep_grid_lists[cls_name].get(k, [])
                    p = dep_grid_ptr[cls_name].get(k, 0)
                    hit = p < len(L) and out_r["err"] == L[p]
                    dep_grid_ptr[cls_name][k] = p + 1
                    grid_replay_hits += int(hit)
                    grid_replay_cmp += 1
                    rec["before_replay_vs_deposit"] = bool(hit)
                else:
                    rec["before_rejection"] = out_r["rejection"]
                if out_a["ok"]:
                    V = np.asarray(out_a["state"]["V"])
                    errs_a.append(out_a["err"])
                    adopted_errs_all.append(out_a["err"])
                    oks.append(out_a["verified"])
                    rec["after_adopted_err"] = out_a["err"]
                    rec["err_native_core"] = round(
                        float(np.sqrt(np.mean((V - A_nat_core) ** 2))), 2)
                    rec["verified_adopted"] = out_a["verified"]
                else:
                    rec["after_rejection"] = out_a["rejection"]
                # adopted cross-class blindness (the analytic consequence)
                if cls_name == "flip_per":
                    cross_cache[(n, i, s)] = outcome_key(out_a)
                else:
                    twin = cross_cache.get((n, i, s))
                    if twin is not None:
                        cross_cmp += 1
                        adopted_blind_cross += int(
                            twin == outcome_key(out_a))
                inst_rec.append(rec)
        grid[cls_name] = {
            "instances": inst_rec,
            "adopted_median": float(np.median(errs_a)) if errs_a else None,
            "before_replay_median": (float(np.median(errs_r))
                                     if errs_r else None),
            "verify_rate_adopted": (float(np.mean(oks)) if oks else None),
        }
        print(f"  A2 {cls_name:10s} before(replay) "
              f"{grid[cls_name]['before_replay_median']} "
              f"after(adopted) {grid[cls_name]['adopted_median']} "
              f"verify {grid[cls_name]['verify_rate_adopted']}")
    before_dep = dep148["gates"]["N3_schedule_fidelity"][
        "pooled_temporal_median"]
    after_med = (float(np.median(adopted_errs_all))
                 if adopted_errs_all else None)
    grid_pooled = {
        "before_deposited": before_dep,
        "before_replayed": (float(np.median(replay_errs_all))
                            if replay_errs_all else None),
        "after_adopted": after_med,
        "bar": N3_BAR,
        "improved": bool(after_med is not None and after_med < before_dep),
        "bar_crossed": bool(after_med is not None and after_med <= N3_BAR),
        "adopted_cross_class_outcome_identical": {
            "n_identical": adopted_blind_cross, "n_compared": cross_cmp},
        "before_replay_bit_exact_vs_deposit": [grid_replay_hits,
                                               grid_replay_cmp],
    }
    print(f"  A2 pooled: before {before_dep} (replayed "
          f"{grid_pooled['before_replayed']}) after {after_med} "
          f"bar {N3_BAR} blind-cross {adopted_blind_cross}/{cross_cmp}")

    # ---- GATE-A1(ii) + GATE-A2: the 12 flip-clock adversarial pairs
    pairs: list[dict] = []
    n_blind_phase = 0
    separated: list[str] = []
    regressed: list[dict] = []
    for fam in fams:
        fi = FAMILIES.index(fam)
        for b in doses:
            di_ = LADDER.index(b)
            sched_seed = SCHED_SEED + 4 * fi + di_
            m_per = FlipPairMedium(b, fam, "per", sched_seed=sched_seed)
            m_aper = FlipPairMedium(b, fam, "aper", sched_seed=sched_seed)
            w_per, w_aper = RTMasked(m_per), RTMasked(m_aper)
            rec = {"family": fam, "dose": b, "sched_seed": sched_seed,
                   "f_per": [int(x) for x in m_per.flip_counts],
                   "f_aper": [int(x) for x in m_aper.flip_counts]}
            # (a) N1 instrument replay: raw phase projections bit-identical
            A_per = project_phase_native(m_per)[0]
            A_aper = project_phase_native(m_aper)[0]
            proj_same = bool(np.array_equal(A_per, A_aper))
            # (b) the adopted read's blindness mechanism: masked frames
            #     are bit-identical across members; the flip edges are not
            #     in the core, so the adopted A_ext is 0 at every chord
            Am_per = project_phase_native(w_per)[0]
            Am_aper = project_phase_native(w_aper)[0]
            masked_same = bool(np.array_equal(Am_per, Am_aper))
            eff_adopted = [float(Am_per[i, j]) for i, j in m_per.chords]
            rec["masked_projection_bit_identical"] = masked_same
            rec["adopted_chord_entries_all_zero"] = bool(
                all(v == 0.0 for v in eff_adopted))
            # (c) the two arms on both members
            arms: dict = {}
            for name, med in (("per", m_per), ("aper", m_aper)):
                wl = w_per if name == "per" else w_aper
                for arm, mm in (("phase", med), ("adopted", wl)):
                    arms[(name, arm)] = run_arm(arm, mm, seeds)
                    rejections += sum(
                        1 for k in arms[(name, arm)]["keys"]
                        if k[0] == "rej")
            # (d) A1(ii): the phase arm is verdict-blind (replay)
            blind_phase = bool(proj_same and
                               verdict_blind(arms[("per", "phase")],
                                             arms[("aper", "phase")]))
            rec["phase_projection_bit_identical"] = proj_same
            rec["phase_verdict_blind"] = blind_phase
            n_blind_phase += int(blind_phase)
            # (e) A2: adopted separation + regression vs the deposit
            sep = (arms[("per", "adopted")]["majority"]
                   != arms[("aper", "adopted")]["majority"])
            rec["adopted_separated"] = bool(sep)
            if sep:
                separated.append(f"{fam}@{b:g}")
            dep = dep_pairs[(fam, b)]
            rec["deposited_temporal"] = {
                "per_majority": dep["arms"]["per_temporal"]["majority"],
                "aper_majority": dep["arms"]["aper_temporal"]["majority"],
                "separated": dep["temporal_separated"]}
            rec["adopted"] = {
                "per_errs": arms[("per", "adopted")]["errs"],
                "per_majority": arms[("per", "adopted")]["majority"],
                "aper_errs": arms[("aper", "adopted")]["errs"],
                "aper_majority": arms[("aper", "adopted")]["majority"]}
            if dep["temporal_separated"] and not sep:
                regressed.append({
                    "pair": f"{fam}@{b:g}",
                    "deposited": rec["deposited_temporal"],
                    "adopted": rec["adopted"]})
            pairs.append(rec)
            print(f"  A1/A2 {fam:17s} b={b:6.1f} phaseBlind={blind_phase} "
                  f"maskedSame={masked_same} adopted "
                  f"per{arms[('per', 'adopted')]['errs']}"
                  f"V{int(arms[('per', 'adopted')]['majority'])} "
                  f"aper{arms[('aper', 'adopted')]['errs']}"
                  f"V{int(arms[('aper', 'adopted')]['majority'])}"
                  + ("  <== SEPARATED" if sep else "  (lost)"))

    n_pairs = len(pairs)
    gates["A1_adopted_safe_static"] = {
        "pass": bool(bit_ok and verify_ok and replay_ok
                     and n4_classes["signed"]["bit_identical_pairs"]
                     == n4_classes["signed"]["n_pairs"]
                     and n4_classes["signed"]["replay_pairs"]
                     == n4_classes["signed"]["n_pairs"]
                     and n4_classes["complex_phase"]["bit_identical_pairs"]
                     == n4_classes["complex_phase"]["n_pairs"]
                     and n4_classes["complex_phase"]["replay_pairs"]
                     == n4_classes["complex_phase"]["n_pairs"]
                     and n4_classes["reactive_grid_subset"]
                     ["bit_identical_pairs"]
                     == n4_classes["reactive_grid_subset"]["n_pairs"]
                     and n4_classes["reactive_grid_subset"]["replay_pairs"]
                     == n4_classes["reactive_grid_subset"]["n_pairs"]
                     and n_pairs > 0
                     and n_blind_phase >= N1_MIN_BLIND),
        "torus_bit_identical": bool(bit_ok),
        "torus_verify_preserved": bool(verify_ok),
        "torus_replay_vs_deposit": bool(replay_ok),
        "signed": {k: n4_classes["signed"][k]
                   for k in ("bit_identical_pairs", "replay_pairs",
                             "n_pairs")},
        "complex_phase": {k: n4_classes["complex_phase"][k]
                          for k in ("bit_identical_pairs", "replay_pairs",
                                    "n_pairs")},
        "reactive": {k: n4_classes["reactive_grid_subset"][k]
                     for k in ("bit_identical_pairs", "replay_pairs",
                               "n_pairs")},
        "phase_blind_pairs": n_blind_phase,
        "n_pairs": n_pairs, "required": N1_MIN_BLIND,
        "static_arm_note": ("mag/sign arms are untouched code paths "
                            "(the adoption wraps only the temporal "
                            "arm's input); their deposited verdicts "
                            "stand"),
    }
    gates["A2_separation_and_fidelity"] = {
        "pass": bool(len(separated) >= N2_MIN_SEPARATION
                     and grid_pooled["improved"]),
        "n_separated_adopted": len(separated),
        "separated_pairs": separated,
        "required": N2_MIN_SEPARATION,
        "deposited_separated": 12,
        "regressed_pairs": regressed,
        "grid_pooled": grid_pooled,
    }

    # ---- GATE-A3: exp166's corner spot set under the adopted read
    dep_spot = {(r["tag"], r["j"]): r
                for r in dep166["spot_battery"]["instances"]}
    spot_records: list[dict] = []
    corner_medians_after: list[float] = []
    clean_replay = 0
    corner_replay = 0
    n_clean = n_corner = 0
    corner_fmax: list[int] = []
    for tag, c in (("corner", CORNER_CELL), ("clean", CLEAN_CELL)):
        for j in spot_j:
            med = CornerMedium(100,
                               seed=EXP166_SEED_BASE + 1000 * c + j,
                               dims=cell_dims(c))
            T_eff = len(med.snapshots())
            rec = {"tag": tag, "cell": c, "j": j, "gen_seed": med.seed,
                   "T": T_eff}
            if tag == "corner":
                F_raw = flip_clock_matrix(med)
                fu = np.maximum(F_raw, F_raw.T)
                corner_fmax.append(int(fu.max()))
            errs_a, vs_a = [], []
            wl = RTMasked(med) if T_eff > 1 else med
            for s in SPOT_SEEDS:
                out = decode("adopted", wl, s)
                rejections += 0 if out["ok"] else 1
                if out["ok"]:
                    errs_a.append(out["err"])
                    vs_a.append(bool(out["verified"]))
                else:
                    errs_a.append(None)
                    vs_a.append(False)
                    rec["rejection"] = out["rejection"]
            rec["errs_adopted"] = errs_a
            rec["verified_adopted"] = vs_a
            fin = [e for e in errs_a if e is not None]
            rec["median_adopted"] = float(np.median(fin)) if fin else None
            dep = dep_spot[(tag, j)]
            ref = dep["errs_armB"] if tag == "corner" else dep["errs_armA"]
            hit = all(e == r for e, r in zip(errs_a, ref))
            rec["replay_bit_exact_vs_exp166"] = bool(hit)
            rec["errs_exp166"] = ref
            if tag == "corner":
                corner_replay += int(hit)
                n_corner += 1
                if rec["median_adopted"] is not None:
                    corner_medians_after.append(rec["median_adopted"])
            else:
                clean_replay += int(hit)
                n_clean += 1
            spot_records.append(rec)
    corner_before = dep166["spot_battery"]["corner_median_armA"]
    corner_after = (float(np.median(corner_medians_after))
                    if corner_medians_after else None)
    gates["A3_corner_spot_adopted"] = {
        "pass": bool(corner_after is not None and corner_after <= N3_BAR
                     and corner_after < corner_before
                     and clean_replay == n_clean
                     and corner_replay == n_corner),
        "corner_median_before": corner_before,
        "corner_median_after": corner_after,
        "bar": N3_BAR,
        "clean_replay_bit_exact": [clean_replay, n_clean],
        "corner_replay_bit_exact_vs_armB": [corner_replay, n_corner],
        "corner_raw_fmax_range": ([min(corner_fmax), max(corner_fmax)]
                                  if corner_fmax else None),
    }
    print(f"  A3 corner {corner_before} -> {corner_after} (bar {N3_BAR}) "
          f"replay clean {clean_replay}/{n_clean} corner "
          f"{corner_replay}/{n_corner} raw f_max "
          f"{gates['A3_corner_spot_adopted']['corner_raw_fmax_range']}")

    # ---- GATE-A4: zero rejections across the whole run
    gates["A4_zero_rejections"] = {"pass": bool(rejections == 0),
                                   "rejections": rejections}

    n_pass = sum(int(g["pass"]) for g in gates.values())
    verdict = f"{n_pass}/{len(gates)} gates"
    print(f"\n  GATES: {verdict}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in gates.items()))
    print(f"  rejections: {rejections}")

    a2 = gates["A2_separation_and_fidelity"]
    scoping = None
    if not a2["pass"]:
        scoping = {
            "registered": True,
            "finding": (
                "the blanket R_T adoption clause is FALSIFIED for the "
                "temporal read: the flip-quiet window silences exactly "
                "the channel (TC1's F) that carries exp148's schedule "
                "semantics — the corner's excess and the battery's "
                "signal are the SAME channel, so one zero-knob clause "
                "cannot buy both"),
            "regressed_schedules": [r["pair"] for r in regressed],
            "mechanism": ("masked frames are bit-identical across pair "
                          "members (membership frozen) => the adopted "
                          "read is verdict-blind wherever the schedule "
                          "lives only on non-core flip edges"),
            "scoping_candidate": (
                "R_T per-media via a PRE-REGISTERED diagnostic in the "
                "style of PN1's rho (threshold fixed from deposited "
                "boundaries BEFORE decoding, zero per-instance "
                "tuning): the flip clock's CONCENTRATION — corner-like "
                "media spread transitions diffusely over the support "
                "(raw f_max = %s here) while the flip-clock battery "
                "concentrates them on K_CHORDS=6 edges (f_aper up to "
                "%d, exp148's deposit); candidate rule: apply R_T only "
                "when f_max is at the diffuse scale, keep raw TC1 "
                "otherwise" % (gates["A3_corner_spot_adopted"]
                               ["corner_raw_fmax_range"],
                               max(max(p["f_aper"]) for p in pairs))),
            "status": ("registered for the NEXT experiment, NOT run "
                       "here"),
        }

    result = {
        "exp": "exp167_rt_adopted",
        "claim": (
            "exp166's registered adoption run: R_T flip-quiet "
            "core-support windowing (ONE zero-knob clause: mask frames "
            "to the across-frame core support when T > 1) adopted into "
            "exp148's TC1-TC3 temporal read and run on exp148's OWN "
            "deposited batteries (12 flip-clock adversarial pairs + "
            "paired schedule grid + static N4 controls, module "
            "verbatim) plus exp166's corner spot set — the adoption is "
            "safe on static media (bit-exact) and repairs temporal "
            "fidelity, and the run prices whether the schedule channel "
            "survives"),
        "pre_registration": {
            "registered_next_source": "L145 (exp166 P4)",
            "adopted_rule_stated_once": [
                "ONE clause: when the read window has T > 1 frames, "
                "every frame is masked to the across-frame CORE support "
                "(exp166's rule_temporal_core verbatim; membership "
                "frozen, zero presence transitions)",
                "then exp148's TC1-TC3 run VERBATIM on the masked "
                "frames: A = PN1/PN2 projected time-average of the "
                "masked frames, F = TC1 raw transition counts of the "
                "masked frames, A_ext = A + F, exp142's executor "
                "verbatim; at T = 1 no mask applies",
                "analytic consequence (part of the rule): F == 0 on the "
                "masked window => A_ext = A_masked — the adopted read "
                "IS the flip-quiet window's phase read; on static media "
                "it is bitwise exp145's read"],
            "registered_tension": (
                "exp148's schedule semantics live only on non-core "
                "flip edges, which the core mask removes; A2 tests "
                "whether exp166's repair and exp148's channel "
                "co-exist under one zero-knob clause"),
            "instruments": ("exp148's module imported verbatim (media, "
                            "constants, phase-arm dispatch); exp166's "
                            "corner spot set verbatim; deposits read "
                            "for replay comparisons at the 2-dp "
                            "executor precision"),
            "gates": {k: g for k, g in gates.items()},
        },
        "config": {"spec": "MULTI (exp94)", "seeds": list(seeds),
                   "spot_seeds": list(SPOT_SEEDS),
                   "families": list(FAMILIES), "ladder": list(LADDER),
                   "sched_seed_base": SCHED_SEED,
                   "grid_base_seed": GRID_BASE_SEED, "T_grid": T_GRID,
                   "n3_bar": N3_BAR,
                   "n2_min_separation": N2_MIN_SEPARATION,
                   "corner_cell": CORNER_CELL, "clean_cell": CLEAN_CELL,
                   "exp166_seed_base": EXP166_SEED_BASE,
                   "instrument_pin": {
                       "constant": "NEURAL_SPEC_MIN",
                       "pinned_to": EXP148_FLOOR,
                       "working_tree_values_seen": PIN_RECORD,
                       "modules": [m.__name__ for m in PIN_MODULES],
                       "reason": ("exp148's and exp166's deposits were "
                                  "produced at the pre-CF-1 floor "
                                  "-35.0; the working tree carries "
                                  "exp168's CF-1 -60.0 (2f9f785) under "
                                  "which exp148's chord_set is an "
                                  "invalid instrument (smoke-caught "
                                  "ZeroDivisionError) and every "
                                  "decode target shifts — the pin "
                                  "restores the deposited world for "
                                  "this run only, exp168's "
                                  "OLD_FLOOR_PIN mechanism")}},
        "control": ctrl,
        "n4_adopted": n4_classes,
        "grid": grid,
        "grid_pooled": grid_pooled,
        "battery": {"pairs": pairs, "n_pairs": n_pairs,
                    "phase_blind_pairs": n_blind_phase,
                    "n_separated_adopted": len(separated),
                    "separated_pairs": separated,
                    "regressed_pairs": regressed},
        "corner_spot": {"instances": spot_records,
                        "corner_median_before": corner_before,
                        "corner_median_after": corner_after},
        "scoping_registered": scoping,
        "gates": gates,
        "verdict": verdict,
        "rejections": rejections,
        "runtime_s": round(time.time() - t0, 1),
    }
    if not args.smoke:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  deposited {OUT}")
    return result


if __name__ == "__main__":
    main()

