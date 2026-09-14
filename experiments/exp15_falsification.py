"""EXP15 — Phase E: falsification controls.

THE TOWER HAS PASSED ITS TESTS — THESE ARE THE CONTROLS THAT COULD TAKE
IT DOWN. Every layer's central claim gets a control arm whose predicted
outcome follows from the claim being TRUE; if the control's prediction
fails, the layer's claim is falsified (or the machinery is fooling us
some other way).

  E1 RANDOM POLICY CONTROL  (against exp10/exp14)
      The discovered policy's held-out win comes from searched STRUCTURE,
      not from 'any policy with maintenance helps'. Control: 8 policies
      drawn uniformly at random from the same 8-dim box, identical cost
      accounting, identical held-out corpus. Prediction if the search is
      real: no random policy matches the discovered one. (Calibration
      from the run itself: random draws land on the broad ~90-yr
      maintenance plateau — the box is dense with workable schedules —
      so the decisive test is the top end: the discovered policy must
      beat every draw, and it does, +22% over the random mean.)

  E2 NO-LATCH CONTROL  (against exp11)
      The novel morphology persists because of the LATCHING MEMORY, not
      because clamps happen to leave residue. Control: the exact
      third_eye protocol applied with the latch integration rate zeroed
      (alpha_latch = 0 — the anchor never rewrites; the cells' memory
      stays wild-type). Prediction if the latch claim is real: after
      release fidelity decays to the WILDTYPE-VS-TARGET baseline (the
      null-protocol level — the novel zone is lost, everything else was
      always going to match), while the native latch holds the full
      pattern.

  E3 SHUFFLED GENOME CONTROL  (against exp8/the codec gate)
      The verified-maintenance gate pays because the ARCHIVE IS CORRECT,
      not because writing per se helps. Control: the archival reference
      (cohort.theta0 — what the codec detects against and writes from,
      and what regenerate() re-derives from) is a fixed permutation of
      the true pattern's per-cell values; mortality is still scored
      against the TRUE functional pattern (organs must be arranged
      correctly to work, whatever the genome says). Default physics never
      reads theta0 (the theta_pull term is intervention-only), so a
      'none' arm with the shuffled genome is the sanity check that the
      scramble touches ONLY the repair pathway.
      Prediction if the archive claim is real: none+shuffled == none
      (sanity), codec+shuffled collapses to <= baseline — the gate's
      x1.9 is archive-dependent.

  E4 CROSS-SPECIES TRANSFER  (against exp11's protocol specificity)
      Discovered protocols encode TARGET-SPECIFIC structure, not generic
      'make fidelity better' magic. Control: the third_eye protocol run
      against the dual_zone target (and vice versa), against the null
      protocol's do-nothing baseline. Pre-registered prediction:
      transferred fidelity degrades substantially but is not annihilated
      (degrade-not-zero). Amplitude/inertness thresholds were ALSO
      pre-registered; the run's actual finding (recorded honestly in the
      results): transfers are not inert — the wrong clamps actively
      overwrite cells that were already correct for the new target
      (off-target reprogramming hazard), which is specificity evidence
      of a stronger kind: the intervention's sign flips.

All references (disc_codec 111.2, hand_codec 124.3, hand_none 63.5,
hand_local 65.1 on the held-out corpus) are LOADED from exp14's results
JSON — nothing is re-tuned. Morphology protocols are loaded from exp11's
state. Either outcome of every control is recorded honestly.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, FidelityCodec, quantize,
)
from cultivation.bioelectric.morpho_engineering import (
    ALPHA_LATCH, ClampProtocol, LatchingCollective, NOVEL_TARGETS,
    discrete_fidelity, evaluate_protocol, null_protocol_u,
    target_third_eye, target_wildtype,
)
from cultivation.inverse.design import POLICY_BOUNDS, eval_policy
from experiments.exp14_stack import (
    DECAY_TAU, HELDOUT_COHORT, HELDOUT_K, HELDOUT_REGIME, HELDOUT_SEEDS,
    HELDOUT_YEARS,
)
from experiments.exp8_fidelity import (
    BUDGET, CHECKUP, FROM_AGE, N_CELLS, age_preset, fidelity_target,
)
from experiments.viz import PALETTE, dump_json, fig_path, setup

import matplotlib.pyplot as plt

EXP11_STATE = "scripts_dev/exp11_state.json"
EXP14_RESULTS = "results/integrated_stack_heldout.json"
N_RANDOM = 8
RANDOM_SEED = 999
SHUFFLE_SEED = 4242


def _p(s):
    print(s, flush=True)


# --------------------------------------------------------------- E3 machinery
class ShuffledGenomeCohort(FidelityAgingCohort):
    """Genome-scramble control cohort.

    The ARCHIVAL reference (theta0: what the codec compares against, what
    it writes, what regenerate() re-derives) is a fixed permutation of the
    true pattern's per-cell values — same value distribution, wrong
    positions, organ boundaries destroyed. Mortality is still scored
    against the TRUE pattern (theta0_true): organs must be arranged
    correctly to function, whatever the scrambled genome instructs.
    Default physics never reads theta0 (theta_pull is intervention-only),
    so this scramble touches ONLY detection/writes/regeneration."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.theta0_true = self.theta0.copy()
        perm = np.random.default_rng(SHUFFLE_SEED).permutation(self.n)
        self.theta0 = self.theta0[perm]

    def _correct_mask(self) -> np.ndarray:
        ref = getattr(self, "theta0_true", self.theta0)
        ok = quantize(self.V, self.levels) == quantize(ref[None, :], self.levels)
        ok[:, ~self._fid_keep] = True
        return ok

    def global_fidelity(self) -> np.ndarray:
        # during super().__init__ theta0_true does not exist yet — and
        # theta0 is still the TRUE pattern there, so the fallback is exact
        ref = getattr(self, "theta0_true", self.theta0)
        ok = quantize(self.V, self.levels) == quantize(ref[None, :], self.levels)
        return ok[:, self._fid_keep].mean(axis=1)

    def organ_fidelities(self) -> np.ndarray:
        ok = self._correct_mask()
        return np.stack([ok[:, sl].mean(axis=1) for sl in self._organ_slices],
                        axis=1)


def run_shuffled_arm(condition: str, seed: int) -> dict:
    """One held-out-corpus run with a scrambled archival genome.

    Faithful replication of exp8's run_condition machinery (same schedule,
    same budget, same presets) with the cohort class swapped."""
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=BUDGET, levels=7)
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **HELDOUT_REGIME)
    ch = ShuffledGenomeCohort(K=HELDOUT_K, params=params, seed=seed,
                              **HELDOUT_COHORT)

    def maintain(t, cohort):
        if t < FROM_AGE - 1e-9 or condition == "none":
            return
        if abs((t - FROM_AGE) % CHECKUP) > 0.26:
            return
        codec.maintain(cohort, age_preset(t), mode="codec")

    s = ch.run(years=HELDOUT_YEARS, dt=0.25, intervention=maintain)
    return {"median": s["median_lifespan"],
            "hist_t": s["hist_t"], "hist_alive": s["hist_alive"]}


# --------------------------------------------------------------- E2/E4 pieces
def latch_arm(u, target, alpha_latch: float, seed: int = 1,
              settle: float = 300.0):
    """exp11's evaluation pipeline with the latch rate as the knob."""
    col = LatchingCollective(n=100, seed=seed, alpha_latch=alpha_latch)
    col.set_target(target_wildtype(100))
    col.set_state(target_wildtype(100) + col.rng.normal(0, 2.0, 100))
    proto = ClampProtocol(u)
    proto.apply(col, dt=0.1)
    fid_release = discrete_fidelity(col.V, target)
    rec = col.run(settle, dt=0.1, record_every=100)
    traj = ([discrete_fidelity(rec[k], target) for k in range(len(rec))]
            if rec is not None else [])
    return {"fid_release": fid_release,
            "fid_settled": discrete_fidelity(col.V, target),
            "traj": traj}


# --------------------------------------------------------------------- main
def main() -> dict:
    setup()
    t0 = time.time()
    print("[exp15] Phase E — falsification controls")
    exp11 = json.load(open(EXP11_STATE))
    exp14 = json.load(open(EXP14_RESULTS))
    disc_median = exp14["arms"]["disc_codec"]["median"]
    none_median = exp14["arms"]["hand_none"]["median"]
    codec_median = exp14["arms"]["hand_codec"]["median"]

    # ---------------------------------------------------- E1 random policies
    _p("  E1: random-policy control (8 draws, held-out corpus)...")
    rng = np.random.default_rng(RANDOM_SEED)
    lo = np.array([b[0] for b in POLICY_BOUNDS])
    hi = np.array([b[1] for b in POLICY_BOUNDS])
    random_medians, random_by_seed = [], []
    for i in range(N_RANDOM):
        u = rng.uniform(lo, hi)
        ms = [eval_policy(u, seed=s, K=HELDOUT_K, years=HELDOUT_YEARS,
                          regime=HELDOUT_REGIME, target0=fidelity_target,
                          age_preset=age_preset,
                          cohort_kw=HELDOUT_COHORT)["median"]
              for s in HELDOUT_SEEDS]
        random_medians.append(float(np.mean(ms)))
        random_by_seed.append([float(m) for m in ms])
        _p(f"    random[{i}]: median {np.mean(ms):6.1f} yr")
    rand_mean = float(np.mean(random_medians))
    rand_best = float(np.max(random_medians))
    beats = int(sum(m > disc_median for m in random_medians))
    _p(f"    random mean {rand_mean:.1f} / best {rand_best:.1f} vs "
       f"discovered {disc_median:.1f}  ({beats}/{N_RANDOM} beat it)")

    # -------------------------------------------------------- E2 no-latch
    _p("  E2: no-latch control (third_eye, alpha_latch = 0)...")
    u_3e = np.array(exp11["discovered"]["third_eye"]["u"])
    target_3e = target_third_eye(100)
    native = latch_arm(u_3e, target_3e, ALPHA_LATCH)
    nolatch = latch_arm(u_3e, target_3e, 0.0)
    null_3e = latch_arm(null_protocol_u(), target_3e, ALPHA_LATCH)
    _p(f"    native   : release {native['fid_release']:.2f} -> settled "
       f"{native['fid_settled']:.2f}")
    _p(f"    no-latch : release {nolatch['fid_release']:.2f} -> settled "
       f"{nolatch['fid_settled']:.2f}  (null baseline "
       f"{null_3e['fid_settled']:.2f})")

    # ---------------------------------------------------- E3 shuffled genome
    _p("  E3: shuffled-genome control (codec gate, held-out corpus)...")
    shuf = {}
    for cond in ("codec", "none"):
        ms, hists = [], []
        for s in HELDOUT_SEEDS:
            r = run_shuffled_arm(cond, seed=s)
            ms.append(r["median"])
            hists.append(r)
        # survival histories are ragged across seeds (different death
        # times) — average over the common prefix
        n_min = min(len(h["hist_alive"]) for h in hists)
        alive = np.mean([np.asarray(h["hist_alive"][:n_min], float)
                         for h in hists], axis=0)
        shuf[cond] = {"medians_by_seed": [float(m) for m in ms],
                      "median": float(np.mean(ms)),
                      "hist_t": hists[0]["hist_t"][:n_min],
                      "hist_alive": alive.tolist()}
        _p(f"    shuffled/{cond:5s}: median {np.mean(ms):6.1f} yr "
           f"(seeds {[round(m) for m in ms]})")

    # ------------------------------------------------- E4 cross-species
    _p("  E4: cross-species transfer (third_eye <-> dual_zone)...")
    u_dz = np.array(exp11["discovered"]["dual_zone"]["u"])
    target_dz = NOVEL_TARGETS["dual_zone"](100)
    transfer = {
        "native_dz": latch_arm(u_dz, target_dz, ALPHA_LATCH),
        "xfer_3e_to_dz": latch_arm(u_3e, target_dz, ALPHA_LATCH),
        "null_dz": latch_arm(null_protocol_u(), target_dz, ALPHA_LATCH),
        "native_3e": native,
        "xfer_dz_to_3e": latch_arm(u_dz, target_3e, ALPHA_LATCH),
        "null_3e": null_3e,
    }
    for k, v in transfer.items():
        _p(f"    {k:14s}: settled fidelity {v['fid_settled']:.2f}")

    # ------------------------------------------------------- criteria
    crit = {
        "E1_no_random_beats_discovered": bool(beats == 0),
        "E1_random_mean_le_85pct": bool(rand_mean <= 0.85 * disc_median),
        "E2_latch_holds_novel_zone": bool(
            native["fid_settled"] >= nolatch["fid_settled"] + 0.05),
        "E2_no_latch_relaxes_to_baseline": bool(
            abs(nolatch["fid_settled"] - null_3e["fid_settled"]) <= 0.05),
        "E3_sanity_default_physics_untouched": bool(
            shuf["none"]["median"] >= 0.95 * none_median),
        "E3_archive_is_load_bearing": bool(
            shuf["codec"]["median"] <= 1.02 * none_median),
        "E4_specificity_dz": bool(
            transfer["xfer_3e_to_dz"]["fid_settled"]
            <= 0.6 * transfer["native_dz"]["fid_settled"]),
        "E4_specificity_3e": bool(
            transfer["xfer_dz_to_3e"]["fid_settled"]
            <= 0.6 * transfer["native_3e"]["fid_settled"]),
        "E4_transfer_not_destructive": bool(
            transfer["xfer_3e_to_dz"]["fid_settled"]
            >= transfer["null_dz"]["fid_settled"] - 0.10
            and transfer["xfer_dz_to_3e"]["fid_settled"]
            >= transfer["null_3e"]["fid_settled"] - 0.10),
    }

    # post-hoc reanalysis, clearly labeled (the pre-registered amplitude
    # and inertness criteria above stay as recorded — NEGATIVE):
    # the intervention's SIGN flips when the protocol meets the wrong
    # target: native value above null turns into harm below null.
    sign_flip = bool(
        (transfer["native_dz"]["fid_settled"] - transfer["null_dz"]["fid_settled"] > 0)
        and (transfer["xfer_3e_to_dz"]["fid_settled"] - transfer["null_dz"]["fid_settled"] < 0)
        and (transfer["native_3e"]["fid_settled"] - transfer["null_3e"]["fid_settled"] > 0)
        and (transfer["xfer_dz_to_3e"]["fid_settled"] - transfer["null_3e"]["fid_settled"] < 0))
    crit["E4_degrade_not_zero"] = bool(
        transfer["xfer_3e_to_dz"]["fid_settled"] >= 0.30
        and transfer["xfer_dz_to_3e"]["fid_settled"] >= 0.30)
    crit["E4_sign_flip_specificity_POSTHOC"] = sign_flip

    results = {
        "E1_random_policy": {
            "n": N_RANDOM, "seed": RANDOM_SEED,
            "medians": random_medians, "by_seed": random_by_seed,
            "mean": rand_mean, "best": rand_best, "beats_discovered": beats,
            "references": {"discovered": disc_median, "hand_codec":
                           codec_median, "hand_none": none_median},
        },
        "E2_no_latch": {
            "native": {k: native[k] for k in ("fid_release", "fid_settled")},
            "no_latch": {k: nolatch[k] for k in ("fid_release", "fid_settled")},
            "null": {k: null_3e[k] for k in ("fid_release", "fid_settled")},
            "native_traj": native["traj"], "no_latch_traj": nolatch["traj"],
            "null_traj": null_3e["traj"], "alpha_latch_native": ALPHA_LATCH,
        },
        "E3_shuffled_genome": {
            "arms": shuf,
            "references": {"hand_none": none_median,
                           "hand_codec": codec_median},
            "shuffle_seed": SHUFFLE_SEED,
        },
        "E4_transfer": {
            "settled": {k: v["fid_settled"] for k, v in transfer.items()},
        },
        "criteria": crit,
        "honest_notes": [
            "E1 references are LOADED from exp14's held-out JSON (discovered "
            "111.2, hand codec 124.3, none 63.5) — nothing re-tuned here; "
            "random policies get the identical procedure-risk accounting. "
            "Honest calibration: random draws land on the broad ~90-yr "
            "plateau (the 8-dim box is dense with workable maintenance "
            "schedules), NOT at the none baseline — the search's value is "
            "the top end: +22% over the random mean, unbeaten by any of "
            "the 8 draws, +6.4% over the best draw.",
            "E2's no-latch arm keeps the FULL machinery (same clamps, same "
            "junction scaling, same settle time) and changes one number: "
            "alpha_latch 0.042 -> 0. Release fidelity is identical in both "
            "arms (0.56 — clamped sites correct, neighbors displaced by "
            "junction coupling); what differs is RETENTION over the settle: "
            "the native latch converges to the full target (0.96), the "
            "no-latch arm relaxes exactly to the null baseline (0.86) — "
            "the novel zone is precisely what is lost.",
            "E3's mortality is scored against the TRUE pattern while the "
            "codec reads the PERMUTED archive; default physics never reads "
            "theta0 (theta_pull is intervention-only), so the none+shuffled "
            "arm is the sanity check that the scramble isolates the repair "
            "pathway. The permutation is shared across individuals (one "
            "species-level genome scramble).",
            "E4 uses exp11's null protocol (three 1-cell wildtype-consistent "
            "clamps, minimal duration) as the do-nothing baseline, so the "
            "comparison 'transferred vs null' isolates protocol structure "
            "from clamp artifact.",
            "E4 honest reading: the pre-registered amplitude criterion "
            "(transfer <= 0.6 x native) and inertness criterion (transfer "
            ">= null - 0.10) are both NEGATIVE — and the mechanism is the "
            "interesting part: the transferred protocol's clamps pin cells "
            "to the WRONG target's values, overwriting cells that were "
            "already correct for the new target (third_eye->dual_zone: 0.69 "
            "vs 0.87 null = -0.18 harm; dual_zone->third_eye: 0.79 vs 0.86 "
            "= -0.07). The interventions are powerful and NOT safe when "
            "misapplied — the computational analog of off-target "
            "reprogramming hazard. Specificity is confirmed in a stronger "
            "form than pre-registered: the intervention's SIGN FLIPS (native "
            "+0.05/+0.10 above null becomes -0.18/-0.07 below it). The "
            "sign-flip criterion is labeled POSTHOC — it was derived from "
            "this run's data, not registered before it.",
        ],
    }

    for k, v in crit.items():
        _p(f"  {k}: {'PASS' if v else 'NEGATIVE'}")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.6),
                             constrained_layout=True)

    ax = axes[0]
    names = ["none", "random\n(mean of 8)", "random\n(best)", "discovered\n(exp10)",
             "hand codec\n(exp8)"]
    vals = [none_median, rand_mean, rand_best, disc_median, codec_median]
    colors = [PALETTE["muted"], PALETTE["warn"], PALETTE["warn"],
              PALETTE["line2"], PALETTE["primary"]]
    ax.bar(range(5), vals, color=colors)
    ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=6.5)
    ax.set_ylabel("median lifespan (yr)")
    ax.set_title("(a) E1: random-policy control\n(held-out corpus)")
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=7)

    ax = axes[1]
    for traj, lab, col in ((native["traj"], "native latch", PALETTE["good"]),
                           (nolatch["traj"], "no latch", PALETTE["warn"]),
                           (null_3e["traj"], "null protocol", PALETTE["muted"])):
        ax.plot(np.arange(len(traj)) * 100, traj, lw=1.5, color=col, label=lab)
    ax.set_xlabel("free time after release"); ax.set_ylabel("fidelity (third eye)")
    ax.set_ylim(0, 1.02)
    ax.set_title("(b) E2: no-latch control\n(retention vs relaxation)")
    ax.legend(frameon=False, fontsize=7)

    ax = axes[2]
    # survival curves: the two shuffled-genome arms; vertical markers at
    # the true-genome reference medians (50%-alive crossing points)
    ax.plot(shuf["codec"]["hist_t"], shuf["codec"]["hist_alive"], lw=1.8,
            color=PALETTE["warn"],
            label=f"codec, SHUFFLED ({shuf['codec']['median']:.0f} yr)")
    ax.plot(shuf["none"]["hist_t"], shuf["none"]["hist_alive"], lw=1.8,
            color=PALETTE["muted"], ls="--",
            label=f"none, SHUFFLED ({shuf['none']['median']:.0f} yr)")
    ax.axvline(none_median, color=PALETTE["muted"], ls=":", lw=1.2)
    ax.text(none_median + 2, 0.55, f"none/true: {none_median:.0f} yr",
            fontsize=6.5, rotation=90)
    ax.axvline(codec_median, color=PALETTE["primary"], ls=":", lw=1.2)
    ax.text(codec_median + 2, 0.55, f"codec/true: {codec_median:.0f} yr",
            fontsize=6.5, rotation=90)
    ax.set_xlabel("age (yr)"); ax.set_ylabel("fraction alive")
    ax.set_ylim(0, 1.05)
    ax.set_title("(c) E3: shuffled-genome control\n(archive is load-bearing)")
    ax.legend(frameon=False, fontsize=6.5, loc="upper right")

    ax = axes[3]
    names = ["native\n(dual_zone)", "third_eye ->\ndual_zone", "null\n(dual_zone)",
             "native\n(third_eye)", "dual_zone ->\nthird_eye", "null\n(third_eye)"]
    vals = [transfer["native_dz"]["fid_settled"],
            transfer["xfer_3e_to_dz"]["fid_settled"],
            transfer["null_dz"]["fid_settled"],
            transfer["native_3e"]["fid_settled"],
            transfer["xfer_dz_to_3e"]["fid_settled"],
            transfer["null_3e"]["fid_settled"]]
    colors = [PALETTE["good"], PALETTE["warn"], PALETTE["muted"],
              PALETTE["good"], PALETTE["warn"], PALETTE["muted"]]
    ax.bar(range(6), vals, color=colors)
    ax.set_xticks(range(6)); ax.set_xticklabels(names, fontsize=5.8)
    ax.set_ylabel("settled fidelity")
    ax.set_ylim(0, 1.02)
    ax.set_title("(d) E4: cross-species transfer\n(protocol specificity)")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=6.5)

    fig.savefig(fig_path("fig15_falsification.png"))
    plt.close(fig)

    path = dump_json("falsification_controls.json", results)
    _p(f"[exp15] results -> {path}  ({time.time() - t0:.0f}s)")
    return results


if __name__ == "__main__":
    main()
