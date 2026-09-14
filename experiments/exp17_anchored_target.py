"""exp17 — D3b: the anchored target (novel-pattern maintenance).

The D3 answer (exp16) left one gap: the pattern survives death through
distributed redundancy — but the codec's maintenance is ARCHIVE-referenced,
so a NOVEL morphology (a pattern that exists only in the somatic memory,
not in the genomic archive) reads 'wrong' every cycle and gets repaired
back to factory default. Verified maintenance, as built, actively erases
engineered morphologies — the off-target hazard made concrete.

D3b closes the loop with the biological target-morphology semantics: the
REMEMBERED pattern IS the target. FidelityCodec(target_source="anchored")
uses the somatic memory (theta_anchor) as the verification reference and
write source wherever a cluster's memory is internally coherent (spread
<= half a level), falling back to the genomic archive for incoherent
memories. Mortality in this experiment is scored against the CURRENT
(novel) target — an animal is not sick for differing from its birth
pattern.

Arms (novel zone = the middle region written to level 6, an in-archive-nowhere value):
  none               no maintenance (the decay baseline)
  archive            the tower's codec, archive-referenced (the erasure hazard)
  anchored           the D3b codec, memory-referenced, TRACKER memory
                     (the consensus anchor follows slow collective drift)
  anchored_protected the D3b codec + PROTECTED memory tier (on_write marks
                     cells whose anchors then do not track consensus —
                     Pezzulo & Levin 2021 bistable somatic memories)
  anchored_wrong     the protected codec maintaining a COHERENT WRONG memory
                     (zone written to -60 instead of -10) — the memory-
                     correctness control (E3's analog)

Pre-registered:
  P1 (the hazard)     archive-codec erases the novel pattern
                      (I_recoverable@60 < none's).
  P2a (tracker fail)  the tracker-memory codec does NOT hold the pattern
                      (I_recoverable@60 < 0.5) — memory-referenced
                      maintenance of a drifting memory maintains the drift.
  P2 (the fix)        anchored_protected I_recoverable@60 >= 0.75 AND
                      median >= none — the protected tier holds the
                      written pattern and maintenance pays.
  P3 (the control)    anchored_wrong median <= 0.95x anchored_protected
                      AND I_recoverable@60 < 0.25 — memory correctness is
                      load-bearing (a coherent wrong memory is maintained
                      with full conviction).
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec, quantize
from cultivation.bioelectric.senescence_semantics import SemanticsCohort
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp17_anchored_target.json"

K, YEARS, SEEDS = 200, 120.0, (21, 22, 23)
CHECKUP, FROM_AGE, BUDGET = 5.0, 30.0, 6
COHORT_KW = dict(jump_rate=0.006, f_crit=0.655)

NOVEL_VAL = -10.0                    # level 6 — in no region of the archive
WRONG_VAL = -60.0                    # level 1 — the coherent wrong memory
ZONE = np.zeros(N_CELLS, bool)
ZONE[24:36] = True
NOVEL_TARGET = fidelity_target()
NOVEL_TARGET[ZONE] = NOVEL_VAL


def _p(s):
    print(s, flush=True)


class NovelTargetCohort(SemanticsCohort):
    """Mortality scored against the CURRENT (novel) target — an animal is
    not sick for differing from its birth pattern. The theta0 edge guard
    still applies (the zone boundary coincides with region boundaries)."""

    def _correct_mask(self) -> np.ndarray:
        ok = (quantize(self.V, self.levels)
              == quantize(np.broadcast_to(self._tgt, (self.K, self.n)),
                          self.levels))
        ok[:, ~self._fid_keep] = True
        return ok


def build(seed: int, write_val: float, protect: bool = False) -> NovelTargetCohort:
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **REGIME)
    ch = NovelTargetCohort(K=K, params=params, seed=seed,
                           death_semantics="broadcast", latch="v2",
                           protect_written=protect, **COHORT_KW)
    ch._tgt = NOVEL_TARGET
    ch._write_val = write_val
    return ch


def run_arm(arm: str, seed: int) -> dict:
    write_val = WRONG_VAL if arm == "anchored_wrong" else NOVEL_VAL
    protect = arm in ("anchored_protected", "anchored_wrong")
    ch = build(seed, write_val, protect)
    codec = None
    if arm in ("archive", "anchored", "anchored_protected",
               "anchored_wrong"):
        codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=BUDGET,
                              levels=7,
                              target_source=("anchored"
                                             if arm.startswith("anchored")
                                             else "archive"))
    written = {"done": False}
    seen = set()
    LEDGER_AT = np.arange(10.0, YEARS + 1, 10.0)
    series = {k: [] for k in ("t", "I_rec")}

    def maintain(t, cohort):
        if not written["done"] and t >= 5.0:
            written["done"] = True
            do = np.zeros((cohort.K, cohort.n), bool)
            do[:, ZONE] = True
            cohort.theta = np.where(do, write_val, cohort.theta)
            cohort.V = np.where(do, write_val, cohort.V)
            if hasattr(cohort, "on_write"):
                cohort.on_write(do)
        if codec is not None and t >= FROM_AGE - 1e-9 \
                and abs((t - FROM_AGE) % CHECKUP) <= 0.26:
            codec.maintain(cohort, age_preset(t), mode="codec")
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                led = cohort.pattern_ledger(ref=NOVEL_TARGET, zone=ZONE)
                series["t"].append(float(a))
                series["I_rec"].append(led["I_recoverable"])

    s = ch.run(years=YEARS, dt=0.25, intervention=maintain)
    s["I_rec_t"] = series["t"]
    s["I_rec"] = series["I_rec"]
    s["ledger"] = ({"cycles": codec.cycles, "restored": codec.restored}
                   if codec else None)
    return s


def main() -> dict:
    t0 = time.time()
    _p("exp17 — D3b: the anchored target (novel-pattern maintenance)")
    arms = ("none", "archive", "anchored", "anchored_protected",
            "anchored_wrong")
    out = {}
    for arm in arms:
        rows = [run_arm(arm, s) for s in SEEDS]
        med = float(np.mean([r["median_lifespan"] for r in rows]))
        i60 = _at(rows, 60.0)
        i100 = _at(rows, 100.0)
        out[arm] = {
            "median": med,
            "medians_by_seed": [float(r["median_lifespan"]) for r in rows],
            "I_recoverable_at_60": i60,
            "I_recoverable_at_100": i100,
            "I_rec_t": rows[0]["I_rec_t"],
            "I_rec_curve": [float(np.mean(x)) for x in zip(
                *[r["I_rec"] for r in rows])],
            "restored": (float(np.mean([r["ledger"]["restored"]
                                        for r in rows]))
                         if rows[0]["ledger"] else None),
        }
        _p(f"    {arm:14s}: median {med:6.1f} yr  I_rec@60 {i60:5.3f}  "
           f"I_rec@100 {i100:5.3f}  "
           f"restored {out[arm]['restored'] or 0:.0f}")
    crit = {
        "P1_archive_erases": bool(
            out["archive"]["I_recoverable_at_60"]
            < out["none"]["I_recoverable_at_60"] - 0.10),
        "P2a_tracker_fails": bool(
            out["anchored"]["I_recoverable_at_60"] < 0.5),
        "P2_protected_fixes": bool(
            out["anchored_protected"]["I_recoverable_at_60"] >= 0.75
            and out["anchored_protected"]["median"]
            >= out["none"]["median"]),
        "P3_memory_load_bearing": bool(
            out["anchored_wrong"]["median"]
            <= 0.95 * out["anchored_protected"]["median"]
            and out["anchored_wrong"]["I_recoverable_at_60"] < 0.25),
    }
    results = {"exp": "exp17_anchored_target", "arms": out,
               "criteria": crit,
               "zone": "cells 24:36 (the middle region), novel level 6 "
                       "(-10 mV, in-archive-nowhere)",
               "mortality_reference": "the CURRENT (novel) target"}
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
    _figure(results)
    _p(f"exp17 complete in {time.time()-t0:.0f}s")
    return results


def _at(rows, age) -> float:
    vals = []
    for r in rows:
        if r["I_rec_t"]:
            m = np.abs(np.asarray(r["I_rec_t"]) - age) < 0.2
            if m.any():
                vals.append(float(np.mean(np.asarray(r["I_rec"])[m])))
    return float(np.mean(vals)) if vals else float("nan")


def _figure(results: dict) -> None:
    setup()
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2),
                           constrained_layout=True)
    col = {"none": "0.6", "archive": PALETTE["accent"],
           "anchored": "0.35", "anchored_protected": PALETTE["good"],
           "anchored_wrong": PALETTE["warn"]}
    for arm in col:
        d = results["arms"][arm]
        ax[0].plot(d["I_rec_t"], d["I_rec_curve"], color=col[arm], lw=2.2,
                   label=arm)
    ax[0].set(xlabel="age (yr)", ylabel="I_recoverable (novel pattern)",
              ylim=(0, 1.05), title="the novel pattern under maintenance")
    ax[0].legend(fontsize=9)
    names = list(col)
    meds = [results["arms"][a]["median"] for a in names]
    ax[1].bar(range(len(names)), meds, color=[col[a] for a in names])
    ax[1].set_xticks(range(len(names)))
    ax[1].set_xticklabels(names, rotation=20, fontsize=8)
    ax[1].set(ylabel="median lifespan (yr)",
              title="mortality scored vs the current target")
    fig.suptitle("exp17 — D3b: the anchored target", fontsize=12)
    fig.savefig(fig_path("fig18_anchored_target"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig18_anchored_target.png")


if __name__ == "__main__":
    main()
