#!/usr/bin/env python3
"""exp31 — STAGE 2 WIDENING (night two): ion_channel + morphogen classes,
per-experiment amputation planes, drug-enriched junction slice.

Quest (docs/QUEST_STAGE2_VALIDATION.md tasks 3-4): convert the class-level
pilot (exp27, repaired in exp29) into per-experiment validation. Zero new
mechanisms tonight EXCEPT one additive, bit-exact-at-default regrow
parameter (`direction='backward'` for head-face regeneration — a head
amputation's blastema reads the trunk boundary BEHIND it; forward default
is bit-exact, full suite green, exp29 controls re-verified bit-exact this
session: cutting 3.16 vs 3.16).

DATA: PlanformDB 2.5.0, 1,462 experiments with post-regeneration outcomes
(exp21 metric unchanged: Num-weighted mean of 1 - freq(WT) over
RegenPeriod>0 result sets). Mining in experiments/planform_mining.py —
plane taxonomy + drug->protocol map PRE-REGISTERED there before any
per-plane outcome query (pooled per-plane means seen during development
are recorded in the notes; no class-x-plane cell was queried before this
file was written).

SIM ARMS (31 arms x 3 seeds, seeds (1,2,3) as registered in exp27;
window 24h dt=0.1; thresholds UNCHANGED: abnormal iff pattern_error >=
6.0 mV OR head_likeness(tail) >= 0.7):
  cutting_{plane}      amputation only; plane in {head, tail, trunk,
                       head_tail, cross_a..d (tail-face cut position from
                       the experiment's recorded k/N fraction), none=intact
                       baseline}
  innexin_{plane}      sustained gap_scale=0.05 through window+regen
                       (exp29 protocol) for plane in {head, tail, trunk,
                       none}
  gjblock_{plane}      same protocol — octanol/heptanol/hexanol drug
                       experiments (planform_mining DRUG_CLASS)
  ion_channel_{plane}  gamma x0.5 + noise_std x3 through window+regen
                       (channel dysfunction: impaired homeostatic
                       relaxation, noisier Vmem — the ion-channel
                       transcription target in the theta dynamics)
  wnt_{plane}          beta-catenin/wnt RNAi: posterior-quarter target
                       identity re-specified to HEAD (-20 mV) at window
                       start (tail identity loss), then plane protocol
  apc_{plane}          apc/axin RNAi: anterior-quarter identity -> TAIL
                       (-50 mV), then plane protocol
  other_rnai_{plane}   NULL MAPPING (cutting protocol) — the model has no
                       mechanism for non-AP genes; this arm EXPECTS to
                       refute (recorded RNAi outcomes run hot) and the
                       gap is the repair list, not a hidden failure
  restored_tail        block -> 24h -> restore -> 20h -> tail amputation
                       (exp27 S2C replication control)

PRE-REGISTERED CRITERIA (fixed before the class-x-plane outcome query;
sim gates use pooled seed rates, recorded gates use experiment means):
  S2W1 TAIL-PLANE BIOELECTRIC ORDERING
       pooled sim pred-abn{innexin_tail, gjblock_tail, ion_channel_tail}
       > sim pred-abn(cutting_tail); AND recorded mean abnormal
       (tail-plane innexin+gj_block+ion_channel) > recorded cutting tail.
  S2W2 CUTTING BASELINE
       every cutting arm pred-abn < 0.5 (incl. intact baseline and all
       cross bins); recorded cutting mean < 0.5.
  S2W3 MORPHOGEN POLARITY SPECIFICITY
       sim wnt_tail > cutting_tail (ectopic head fires); sim apc_head >
       cutting_head (ectopic tail fires); sim wnt_head == cutting_head
       (identity-flip specificity — no collateral); recorded AP-morphogen
       mean > recorded cutting mean.
  S2W4 ION-CHANNEL MAPPING
       sim pred-abn{ion_channel_tail, ion_channel_head} pooled >= sim
       innexin_tail (bioelectric disruption >= junction loss, the sim-side
       PB2 analogue); recorded ion_channel mean > recorded cutting mean.
  S2W5 CONTROLS
       restored_tail == 0; each intact arm (cutting/innexin/ion_channel
       _none) == 0 — no spurious abnormality without cutting.
  S2W6 COVERAGE
       fraction of the 1,462-outcome corpus covered by a sim-mappable
       protocol >= 0.60 (excludes graft/irr/lateral planes only).
  S2W7 CROSSPIECE GRADIENT (exploratory, no gate)
       Spearman(cut position f, recorded abnormal) across cutting
       crosspieces; sim cross-bin pred-abn per bin reported alongside.

EXPECTED-LIMITATION PROBES (recorded, ungated — the M26+ repair list):
  trunk-face blindness: forward-only regrow cannot regenerate the
    POSTERIOR face of mid-body removals (wnt_trunk, apc_trunk expected to
    miss the recorded two-tailed/two-headed trunk phenotypes);
  anterior-face organizer: exclude-head crosspieces regenerate heads from
    the anterior face in the record; the model's backward readout extends
    trunk identity (no head-organizer field);
  intact-animal RNAi (none-plane): phenotype formation without amputation
    is outside the sheet's abnormality channels;
  non-AP morphogen genes (notch/bmp/fgf): DV/eye/brain axes, not
    representable on the 1D AP sheet.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from cultivation.validation.stats import mean_se  # noqa: E402
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL,
    make_collective, amputate_regrow,
)
from experiments.planform_mining import (  # noqa: E402
    DB, load_widened,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp31_stage2_widened.json")

HEAD = slice(0, 15)
TAILP = slice(85, 100)
TRUNK = slice(45, 60)
POST_Q = slice(75, 100)   # wnt re-specification zone
ANT_Q = slice(0, 25)      # apc re-specification zone
WT_HEAD_V = -20.0
WT_TAIL_V = -50.0

CROSS_BINS = {"a": (0.0, 0.25), "b": (0.25, 0.5), "c": (0.5, 0.75),
              "d": (0.75, 1.0)}


def plane_protocol(c: "BioElectricCollective", plane: str, cut_f: float) -> None:
    """Amputation + regrowth for one plane (exp27 tail protocol inside)."""
    if plane == "none":
        return
    if plane == "head":
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD, cell_period=0.8, dt=DT, noise=0.6, direction="backward")
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, cell_period=0.8, dt=DT, noise=0.6)
    elif plane == "head_tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
        c.regrow(HEAD, cell_period=0.8, dt=DT, noise=0.6, direction="backward")
    elif plane == "crosspiece":
        ci = int(round(cut_f * N))
        ci = min(max(ci, 5), N - 1)
        c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(slice(ci, N), cell_period=0.8, dt=DT, noise=0.6)
    else:
        raise ValueError(plane)


def window(c: "BioElectricCollective", hours: float = 24.0) -> None:
    c.run(hours, dt=DT)


def run_arm(arm: str, seed: int, cut_f: float = 0.5) -> dict:
    c = make_collective(seed)
    if arm == "restored_tail":
        c.block_gap_junctions(0.05)
        window(c)
        c.restore_gap_junctions(1.0)
        c.run(20, dt=DT)
        m = amputate_regrow(c)
    elif arm.startswith("cutting_"):
        plane = arm[len("cutting_"):]
        if plane.startswith("cross_"):
            plane = "crosspiece"
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    elif arm.startswith("innexin_") or arm.startswith("gjblock_"):
        plane = arm.split("_", 1)[1]
        if plane.startswith("cross_"):
            plane = "crosspiece"
        c.block_gap_junctions(0.05)
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    elif arm.startswith("ion_channel_"):
        plane = arm[len("ion_channel_"):]
        c.gamma *= 0.5
        c.noise_std *= 3.0
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    elif arm.startswith("wnt_"):
        plane = arm[len("wnt_"):]
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    elif arm.startswith("apc_"):
        plane = arm[len("apc_"):]
        c.corrupt_region(ANT_Q, theta_value=WT_TAIL_V)
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    elif arm.startswith("other_rnai_"):
        plane = arm[len("other_rnai_"):]
        window(c)
        plane_protocol(c, plane, cut_f)
        m = _finish(c, plane)
    else:
        raise ValueError(arm)
    m["seed"] = seed
    m["predicted_abnormal"] = bool(
        m["wt_pattern_error"] >= ABN_ERR_MV
        or m["head_likeness_tail"] >= ABN_HL)
    return m


def _finish(c, plane: str) -> dict:
    # readout identical for every plane (exp27 rule): pattern error vs the
    # full WT axis + ectopic-head score at the tail region
    del plane
    return {
        "wt_pattern_error": c.pattern_error(wildtype_target(N)),
        "head_likeness_tail": head_likeness(c.V, TAIL),
        "head_likeness_head": head_likeness(c.V, slice(0, N // 4)),
    }


def sim_arm(arm: str, cut_f: float = 0.5) -> dict:
    runs = [run_arm(arm, s, cut_f) for s in SEEDS]
    errs = [r["wt_pattern_error"] for r in runs]
    ms_e = mean_se(errs)
    return {
        "err_mean": ms_e["mean"], "err_se": ms_e["se"],
        "err_per_seed": errs,
        "pred_abn_rate": float(np.mean([r["predicted_abnormal"]
                                        for r in runs])),
    }


def main() -> dict:
    print("=== exp31: Stage 2 widening — ion_channel + morphogen classes, "
          "per-experiment amputation planes ===\n")

    con = sqlite3.connect(DB)
    exps = load_widened(con)
    print(f"  corpus: {len(exps)} experiments with outcomes")

    # crosspiece bin cut positions (metadata only, no outcomes touched)
    cross_f = {b: [] for b in CROSS_BINS}
    for e in exps.values():
        if e["plane"] == "crosspiece" and e["cut_f"] is not None:
            for b, (lo, hi) in CROSS_BINS.items():
                if lo < e["cut_f"] <= hi or (b == "a" and e["cut_f"] == 0.25):
                    cross_f[b].append(e["cut_f"])
                    break
    cut_f_of_bin = {b: (float(np.median(v)) if v else 0.5)
                    for b, v in cross_f.items()}
    print(f"  crosspiece bins (median cut f): "
          f"{ {b: round(f, 3) for b, f in cut_f_of_bin.items()} }")

    # ---- sim arms ----------------------------------------------------------
    arm_defs: list[tuple[str, float]] = []
    for p in ("head", "tail", "trunk", "head_tail"):
        arm_defs.append((f"cutting_{p}", 0.5))
    for b in CROSS_BINS:
        arm_defs.append((f"cutting_cross_{b}", cut_f_of_bin[b]))
    arm_defs.append(("cutting_none", 0.5))
    for p in ("head", "tail", "trunk", "none"):
        arm_defs.append((f"innexin_{p}", 0.5))
        arm_defs.append((f"ion_channel_{p}", 0.5))
    for p in ("head", "tail", "trunk", "head_tail"):
        arm_defs.append((f"gjblock_{p}", 0.5))
    for p in ("head", "tail", "trunk"):
        arm_defs.append((f"wnt_{p}", 0.5))
        arm_defs.append((f"apc_{p}", 0.5))
        arm_defs.append((f"other_rnai_{p}", 0.5))
    arm_defs.append(("restored_tail", 0.5))

    sim: dict[str, dict] = {}
    for arm, cf in arm_defs:
        sim[arm] = sim_arm(arm, cf)
        s = sim[arm]
        print(f"  {arm:22s} err {s['err_mean']:5.2f} ± {s['err_se']:4.2f} mV"
              f"   pred-abn {s['pred_abn_rate']:.2f}")

    # ---- recorded class x plane cells --------------------------------------
    cells: dict[tuple[str, str], dict] = {}
    for eid, e in exps.items():
        key = (e["group"], e["plane"])
        c = cells.setdefault(key, {"n": 0, "vals": [], "detail": []})
        c["n"] += 1
        c["vals"].append(e["abnormal"])
        c["detail"].append({
            "exp": eid, "abnormal": round(e["abnormal"], 3),
            "rnais": e["rnais"], "drugs": e["drugs"],
            "manipulation": e["manipulation"], "cut_f": e["cut_f"],
            "ap_morphogen": e["ap_morphogen"],
        })
    for c in cells.values():
        c["mean"] = float(np.mean(c["vals"]))
        del c["vals"]

    raw: dict[tuple[str, str], list[float]] = {}
    for e in exps.values():
        raw.setdefault((e["group"], e["plane"]), []).append(e["abnormal"])

    rec_cut_tail = raw.get(("cutting", "tail"), [])
    rec_bio_tail = (raw.get(("innexin", "tail"), [])
                    + raw.get(("gj_block", "tail"), [])
                    + raw.get(("ion_channel", "tail"), []))
    rec_cut_all = [v for (g, p), vs in raw.items()
                   if g == "cutting" for v in vs]
    rec_ap = [v for e in exps.values()
              if e["group"] == "morphogen" and e["ap_morphogen"]
              for v in [e["abnormal"]]]
    rec_ion = [v for (g, p), vs in raw.items() if g == "ion_channel"
               for v in vs]

    # ---- pre-registered criteria ------------------------------------------
    bio_tail_arms = ["innexin_tail", "gjblock_tail", "ion_channel_tail"]
    sim_bio_tail = float(np.mean([sim[a]["pred_abn_rate"]
                                  for a in bio_tail_arms]))
    s2w1 = bool(sim_bio_tail > sim["cutting_tail"]["pred_abn_rate"]
                and rec_bio_tail and rec_cut_tail
                and np.mean(rec_bio_tail) > np.mean(rec_cut_tail))
    cutting_arms = ([f"cutting_{p}" for p in
                     ("head", "tail", "trunk", "head_tail")]
                    + [f"cutting_cross_{b}" for b in CROSS_BINS]
                    + ["cutting_none"])
    s2w2 = bool(max(sim[a]["pred_abn_rate"] for a in cutting_arms) < 0.5
                and rec_cut_all and np.mean(rec_cut_all) < 0.5)
    s2w3 = bool(sim["wnt_tail"]["pred_abn_rate"]
                > sim["cutting_tail"]["pred_abn_rate"]
                and sim["apc_head"]["pred_abn_rate"]
                > sim["cutting_head"]["pred_abn_rate"]
                and sim["wnt_head"]["pred_abn_rate"]
                == sim["cutting_head"]["pred_abn_rate"]
                and rec_ap and rec_cut_all
                and np.mean(rec_ap) > np.mean(rec_cut_all))
    sim_ion_pooled = float(np.mean([sim["ion_channel_tail"]["pred_abn_rate"],
                                    sim["ion_channel_head"]["pred_abn_rate"]]))
    s2w4 = bool(sim_ion_pooled >= sim["innexin_tail"]["pred_abn_rate"]
                and rec_ion and rec_cut_all
                and np.mean(rec_ion) > np.mean(rec_cut_all))
    s2w5 = bool(sim["restored_tail"]["pred_abn_rate"] == 0.0
                and all(sim[a]["pred_abn_rate"] == 0.0 for a in
                        ("cutting_none", "innexin_none", "ion_channel_none")))

    # coverage
    mappable = {"head", "tail", "trunk", "head_tail", "crosspiece", "none"}
    n_mappable = sum(1 for e in exps.values() if e["plane"] in mappable)
    coverage = n_mappable / len(exps)
    s2w6 = bool(coverage >= 0.60)

    # crosspiece gradient (exploratory)
    from scipy.stats import spearmanr
    cp = [(e["cut_f"], e["abnormal"]) for e in exps.values()
          if e["plane"] == "crosspiece" and e["cut_f"] is not None
          and e["group"] == "cutting"]
    rho = spearmanr([x for x, _ in cp], [y for _, y in cp]) if len(cp) > 5 \
        else None

    print(f"\n  S2W1 tail-plane bioelectric ordering (sim "
          f"{sim_bio_tail:.2f} vs cutting {sim['cutting_tail']['pred_abn_rate']:.2f};"
          f" rec bio {np.mean(rec_bio_tail):.3f} vs cut {np.mean(rec_cut_tail):.3f}): "
          f"{'PASS' if s2w1 else 'REFUTED'}")
    print(f"  S2W2 cutting baseline:                     "
          f"{'PASS' if s2w2 else 'REFUTED'}")
    print(f"  S2W3 morphogen polarity specificity:       "
          f"{'PASS' if s2w3 else 'REFUTED'}")
    print(f"  S2W4 ion-channel mapping (sim pooled "
          f"{sim_ion_pooled:.2f} vs innexin "
          f"{sim['innexin_tail']['pred_abn_rate']:.2f}):       "
          f"{'PASS' if s2w4 else 'REFUTED'}")
    print(f"  S2W5 controls:                             "
          f"{'PASS' if s2w5 else 'REFUTED'}")
    print(f"  S2W6 coverage ({coverage:.2f}):                      "
          f"{'PASS' if s2w6 else 'REFUTED'}")
    print(f"  S2W7 crosspiece gradient (exploratory): rho="
          f"{rho.statistic if rho else float('nan'):.3f} "
          f"(p={rho.pvalue if rho else float('nan'):.4f}, n={len(cp)})")

    out = {
        "exp": "exp31_stage2_widened",
        "source": "PlanformDB 2.5.0 (Lobo 2013), in-repo .edb",
        "n_corpus": len(exps),
        "n_mappable": n_mappable,
        "coverage": coverage,
        "cross_bins_median_f": cut_f_of_bin,
        "sim_arms": sim,
        "recorded_cells": {f"{g}|{p}": c for (g, p), c in
                           sorted(cells.items())},
        "criteria": {
            "S2W1_tail_bioelectric_ordering": bool(s2w1),
            "S2W2_cutting_baseline": bool(s2w2),
            "S2W3_morphogen_polarity": bool(s2w3),
            "S2W4_ion_channel_mapping": bool(s2w4),
            "S2W5_controls": bool(s2w5),
            "S2W6_coverage": bool(s2w6),
            "S2W7_crosspiece_gradient_exploratory":
                None if rho is None else float(rho.pvalue),
        },
        "crosspiece_gradient": {
            "spearman_rho": None if rho is None else float(rho.statistic),
            "p": None if rho is None else float(rho.pvalue),
            "n": len(cp),
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "regrow_direction_patch": (
            "additive direction='backward' param (head-face readout); "
            "forward default bit-exact, suite green, exp29 controls "
            "re-verified this session"),
        "notes": (
            "Night-two widening per QUEST tasks 3-4. Null-mapping "
            "other_rnai arms and expected-limitation probes (trunk "
            "posterior face, anterior organizer, intact-animal RNAi, "
            "non-AP genes) are the honest repair list, recorded not "
            "gated."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
