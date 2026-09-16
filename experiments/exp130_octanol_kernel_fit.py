#!/usr/bin/env python3
"""exp130 — THE OCTANOL KERNEL FIT (Task 5-g / T1 of the Levin-series
ranked targets, research/levin_voltage_series.md §4 T1).

THE RECORD (research/levin_voltage_series.json, eids 434-444, Oviedo
2010 PMID 20026026, D. japonica post-pharyngeal fragments, n=10 each):

  Fig 2A (the octanol delayed-onset kernel; eid 434 control = 0.00):
    DH 0.85 / 0.90 / 0.58 / 0.10 / 0.10 / 0.10 at DB rungs
    0.13 / 0.25 / 0.5 / 1 / 2 / 3.
  Fig 2B (the VNC-disruption kernel on the sustained-octanol bath):
    DH 0.18 / 0.75 / 0.20 / 0.00 at VNC-cut t = 0 / 0.125 / 0.5 / 1
    (DB panel labels "days").

UNITS RESOLUTION (the md's T1 gate (a), resolved AGAINST THE PAPER
BEFORE RUNNING — Europe PMC / PMC2823934 full text, fetched this
session): "Regenerating tissue without head (post-pharyngeal fragment)
was treated with GJ inhibitor at different time-points after amputation
(Figure 2A) ... the most significant effect results from starting GJ
blockade within the first 3-6 hours post-amputation. The effect on A/P
patterning dropped significantly (<60%) for treatments beginning >12
hours of regeneration ... the primary role of GJ-mediated information
occurs within 12 hours of amputation."
  -> The paper's own verbal timeline (strong at 3-6 h, <60% at >12 h,
     insignificant at >= 24 h) matches the rungs ONLY under the DAYS
     reading (onset = 24 x rung hours: 3.12/6/12/24/48/72 h — 0.85/0.90
     land in the 3-6 h window, 0.58 IS the paper's "<60%" at 12 h,
     0.10 at 24 h+ IS "insignificant"). The HOURS reading would put the
     kernel's drop at 1 h, contradicting the paper's 3-6 h window.
     Corroboration: the Fig 2B DB panels are labelled "0.125days".
  -> ADOPTED: the days reading, onset_hours = 24 x rung. The paper also
     names the protocol: treatment BEGAN at the recorded time
     post-amputation — the DB StartTime semantics (exp70's delayed
     class), NOT a pre-soak; "pre-treatment" is the md's shorthand.
     The hours reading is still RUN and deposited below as the decisive
     alternative (not gated).

THE MAPPING (ledger L103-L104): the record's GJ-blocker drug (octanol)
IS the theta-diffusion cut in the stack's semantics — run_deadline's
mu-silence at `onset` under fixed pinning (exp124's harness, verbatim).
The DH outcome at posterior-facing wounds is the stack's BREAK mode
(exp39-V4: blockade -> blastema blind-guess -> head-like; eid 418:
sustained octanol -> DH 1.00). The stack's deposited deadline curve at
the adopted (gamma 4, mu 0) torus cell is evaluated at the mapped
onsets by STEP-HOLD on the harness grid (the arm at onset t behaves as
the last grid onset <= t) — ZERO FREE PARAMETERS: no amplitude, sign,
or edge refit; the one fit is the axis map itself. (The md T1's
analytic-rate variant was PRE-REFUTED by exp125's AN-G1, ledger L106 —
the axis-map fit is the registered remaining zero-free-parameter form.)

PRE-REGISTERED GATES (thresholds stated BEFORE running):

  OK-A1  (ANCHOR — harness continuity) the freshly-run gamma-4 torus
         deadline curve (run_deadline verbatim, 8 onsets x 8 seeds)
         reproduces results/exp124_deadline_curve.json curves["4.0"]
         within 0.125 at every onset (exp125's AX-G0 anchor discipline).
  OK-G1  (DIRECTION gate — the Fig 2A fit, two-sided)
         Spearman(fresh gamma-4 P(break) at the mapped rung onsets
         [3.12, 6, 12, 24, 48, 72] h, published DH
         [0.85, 0.90, 0.58, 0.10, 0.10, 0.10]) >= 0.6 -> PASS;
         <= -0.3 -> REFUTED (anti-ordered: the deadline and the record's
         kernel run opposite along the onset axis);
         (-0.3, 0.6) -> PARTIAL (measured concordance, owned honestly);
         Spearman undefined (degenerate constant prediction) -> PARTIAL
         with the degeneracy owned (audit fix: an earlier draft routed
         the undefined case to PASS — never scorable as a confirm).
  OK-G2  (FIT QUALITY gate — the Fig 2B prediction, two-sided; the md's
         registered bar) the same zero-free-parameter curve at the VNC
         onsets [0, 3, 12, 24] h must predict the deposited VNC kernel
         [0.18, 0.75, 0.20, 0.00] with Spearman >= 0.8 AND pointwise
         MAE <= 0.25. If the prediction is CONSTANT across the onsets,
         Spearman is undefined and the gate is scored on MAE alone (a
         flat prediction against a peaked kernel is the shape miss
         itself, not an untestable gate). REFUTED iff (rho defined and
         rho < 0.8) or MAE > 0.25.

RUN: 4 gammas x 8 onsets x 8 seeds = 256 run_deadline calls (the ladder
re-run deposits the edge table for the notes; the gates use gamma 4).
Serial, BLAS pinned.

AUDIT TRAIL (owned in the deposit): the workspace held an uncommitted
draft finalization of this same target (script + result JSON, no
worklog entry). This run audited it against the record JSON, the md,
and the harness; independently re-verified ALL quoted Oviedo-2010
passages verbatim from the paper's PMC2823934 full text (NCBI
E-utilities efetch db=pmc id=2823934 — the Europe PMC fullTextXML
endpoint returned HTTP 500 this session); re-derived the units
resolution from those passages plus the DB's own '0.125days' Fig 2B
panel labels and exp70's registered delayed-onset class; fixed the
OK-G1 undefined-Spearman zone (degenerate -> PARTIAL, was PASS);
added the polarity-robustness mirror MAE and Pearson as non-gated
descriptive deposits. Gate thresholds unchanged from the registered
form (stated above, before running).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from scipy.stats import spearmanr  # noqa: E402

from experiments.exp112_walk_speed_ladder import build_battery  # noqa: E402
from experiments.exp124_deadline_curve import GAMMAS, ONSETS, run_deadline  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp130_octanol_kernel_fit.json")
DEP = os.path.join(ROOT, "results", "exp124_deadline_curve.json")

# the record (research/levin_voltage_series.json, eids 434-444)
FIG2A_RUNGS = (0.13, 0.25, 0.5, 1.0, 2.0, 3.0)      # DB StartTime units
FIG2A_DH = (0.85, 0.90, 0.58, 0.10, 0.10, 0.10)     # eid 435-440
FIG2A_CONTROL_DH = 0.00                              # eid 434 (no octanol)
FIG2B_VNC_DAYS = (0.0, 0.125, 0.5, 1.0)             # VNC cut t (days)
FIG2B_DH = (0.18, 0.75, 0.20, 0.00)                 # eid 441-444
ANCHOR_GAMMA = 4.0
ANCHOR_TOL = 0.125
G1_PASS, G1_REFUTE = 0.6, -0.3      # OK-G1 two-sided zones (pre-registered)
G2_RHO, G2_MAE = 0.8, 0.25          # OK-G2 thresholds (pre-registered)


def step_hold(curve, t: float) -> float:
    """The arm at onset t behaves as the last harness grid onset <= t."""
    v = curve[0]
    for onset, p in zip(ONSETS, curve):
        if onset <= t + 1e-9:
            v = p
    return v


def evaluate(curve, onsets_h):
    return [step_hold(curve, t) for t in onsets_h]


def rho_or_none(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(spearmanr(a, b)[0])


def pearson_or_none(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def main() -> dict:
    print("=== exp130: the octanol kernel fit (mu-silence deadline) ===\n")

    dep = json.load(open(DEP))
    dep_g4 = dep["curves"][str(ANCHOR_GAMMA)]

    battery = build_battery()
    torus = battery["torus"]

    # ---- the fresh deadline ladder (the exp124 harness, verbatim) --------
    curves: dict = {}
    for g in GAMMAS:
        ps = []
        for onset in ONSETS:
            br = [run_deadline(torus, s, g, onset) for s in range(1, 9)]
            ps.append(round(float(np.mean(br)), 3))
        curves[str(g)] = ps
        print(f"    gamma {g:5.1f}  P(break): {ps}")

    def edge(ps):
        for t, p in zip(ONSETS, ps):
            if p >= 0.5:
                return t
        return None

    edges = {g: edge(curves[str(g)]) for g in GAMMAS}
    print(f"  fresh edges: {edges}  (deposited: {dep['edges']})")

    # ---- OK-A1: the anchor -----------------------------------------------
    deltas = [abs(a - b) for a, b in zip(curves[str(ANCHOR_GAMMA)], dep_g4)]
    ok_a1 = bool(max(deltas) <= ANCHOR_TOL)
    print(f"\n  OK-A1 anchor (gamma-4 curve, max|delta| "
          f"{max(deltas):.3f} <= {ANCHOR_TOL}): "
          f"{'PASS' if ok_a1 else 'REFUTED'}")

    fresh_g4 = curves[str(ANCHOR_GAMMA)]

    # ---- OK-G1: the direction gate (Fig 2A, days reading) ----------------
    onsets_days = [24.0 * r for r in FIG2A_RUNGS]
    pred_days = evaluate(fresh_g4, onsets_days)
    rho_2a = rho_or_none(pred_days, FIG2A_DH)
    pear_2a = pearson_or_none(pred_days, FIG2A_DH)
    if rho_2a is None:
        g1 = "PARTIAL"   # degenerate prediction: not scorable as a confirm
    elif rho_2a >= G1_PASS:
        g1 = "PASS"
    elif rho_2a <= G1_REFUTE:
        g1 = "REFUTED"
    else:
        g1 = "PARTIAL"
    print(f"  Fig 2A (days): onsets {onsets_days}")
    print(f"    stack P(break) {pred_days} vs DH {list(FIG2A_DH)}")
    print(f"  OK-G1 direction (Spearman {rho_2a}): {g1}")

    # the hours reading — the decisive alternative (deposited, not gated)
    pred_hours = evaluate(fresh_g4, list(FIG2A_RUNGS))
    rho_2a_hours = rho_or_none(pred_hours, FIG2A_DH)
    mae_2a_hours = float(np.mean(np.abs(
        np.array(pred_hours) - np.array(FIG2A_DH))))
    print(f"  [alt] hours reading: prediction {pred_hours} "
          f"(constant, Spearman {rho_2a_hours}), MAE {mae_2a_hours:.3f}")

    # the mirror observation (NOTE, not a gated rescue: the DH<->(1-P)
    # flip would be a free sign parameter, forbidden by the registration)
    rho_mirror = rho_or_none([1.0 - p for p in pred_days], FIG2A_DH)
    print(f"  [note] mirror flip (1-P vs DH): Spearman {rho_mirror} "
          f"— the record's kernel polarity matches the CHAIN corpus's "
          f"delayed-cooler-than-sustained ordering (exp70 ON-G3), "
          f"not the torus deadline; deposited as a note only.")
    mae_2a_mirror = float(np.mean(np.abs(
        np.array([1.0 - p for p in pred_days]) - np.array(FIG2A_DH))))
    print(f"  [note] mirror MAE (2A): {mae_2a_mirror:.4f} "
          f"vs registered-reading MAE "
          f"{float(np.mean(np.abs(np.array(pred_days) - np.array(FIG2A_DH)))):.4f}")

    # ---- OK-G2: the fit-quality gate (Fig 2B prediction) ------------------
    onsets_vnc = [24.0 * t for t in FIG2B_VNC_DAYS]
    pred_vnc = evaluate(fresh_g4, onsets_vnc)
    rho_2b = rho_or_none(pred_vnc, FIG2B_DH)
    pear_2b = pearson_or_none(pred_vnc, FIG2B_DH)
    mae_2b = float(np.mean(np.abs(
        np.array(pred_vnc) - np.array(FIG2B_DH))))
    # polarity robustness of the OK-G2 scoring: even the mirror reading
    # (1-P) is flat across the VNC onsets — its MAE is deposited so the
    # refutation is on record as polarity-invariant on this grid.
    mae_2b_mirror = float(np.mean(np.abs(
        np.array([1.0 - p for p in pred_vnc]) - np.array(FIG2B_DH))))
    if rho_2b is not None and rho_2b < G2_RHO:
        g2 = "REFUTED"
    elif mae_2b > G2_MAE:
        g2 = "REFUTED"
    else:
        g2 = "PASS"
    print(f"\n  Fig 2B (VNC): onsets {onsets_vnc}")
    print(f"    stack P(break) {pred_vnc} vs VNC DH {list(FIG2B_DH)}")
    print(f"    Spearman {rho_2b} (bar {G2_RHO}), MAE {mae_2b:.4f} "
          f"(bar {G2_MAE})")
    print(f"  OK-G2 fit quality: {g2}")

    npass = sum([ok_a1, g1 == "PASS", g2 == "PASS"])
    print(f"\n  === {npass}/3 gates PASS "
          f"(anchor {'PASS' if ok_a1 else 'REFUTED'}, "
          f"direction {g1}, fit-quality {g2}) ===")

    result = {
        "exp": "exp130_octanol_kernel_fit",
        "task": ("T1 of the Levin-series ranked targets "
                 "(research/levin_voltage_series.md): fit the Oviedo-2010 "
                 "octanol kernel with the exp124 mu-silence deadline "
                 "machinery, one zero-free-parameter axis-map fit, predict "
                 "the Fig 2B VNC kernel."),
        "units_resolution": {
            "adopted": "days reading: onset_hours = 24 x DB rung",
            "evidence": (
                "PMC2823934 full text (re-fetched and verified VERBATIM "
                "this session via NCBI E-utilities efetch db=pmc "
                "id=2823934; the Europe PMC fullTextXML endpoint returned "
                "HTTP 500 this session): 'Regenerating tissue without "
                "head (post-pharyngeal fragment) was treated with GJ "
                "inhibitor at different time-points after amputation "
                "(Figure 2A) ... the most significant effect results from "
                "starting GJ blockade within the first 3-6 hours "
                "post-amputation. The effect on A/P patterning dropped "
                "significantly (<60%) for treatments beginning >12 hours "
                "of regeneration ... the primary role of GJ-mediated "
                "information occurs within 12 hours of amputation'; the "
                "rungs match ONLY as 0.125d=3h ... 3d=72h (0.85/0.90 in "
                "the 3-6 h window, 0.58 = the paper's '<60%' at 12 h, "
                "0.10 at 24 h+ = 'insignificant'); Fig 2B DB panels are "
                "labelled '0.125days' (research/levin_voltage_series.json "
                "db_figure_panel fields, eids 441-444), and exp70's "
                "registered delayed-onset class (start>0, end=0) is the "
                "DB semantics these rows carry."),
            "protocol_note": (
                "The paper's protocol is a DELAYED-ONSET bath (treatment "
                "began at the recorded time post-amputation) — the DB "
                "StartTime semantics (exp70 delayed class); 'pre-treat-"
                "ment' is the md's shorthand. Under ledger L103-L104 the "
                "octanol IS the theta-diffusion cut; DH at posterior "
                "wounds is the stack's BREAK mode (eid 418 sustained -> "
                "DH 1.00)."),
        },
        "fresh_curves": curves,
        "fresh_edges": {str(k): v for k, v in edges.items()},
        "deposited_edges": dep["edges"],
        "anchor": {
            "gate": "OK-A1 (gamma-4 curve within 0.125 of exp124)",
            "fresh": curves[str(ANCHOR_GAMMA)],
            "deposited": dep_g4,
            "max_abs_delta": round(max(deltas), 4),
            "verdict": "PASS" if ok_a1 else "REFUTED",
        },
        "fig2a_fit": {
            "reading": "days (adopted)",
            "onsets_h": onsets_days,
            "stack_prediction": pred_days,
            "published_dh": list(FIG2A_DH),
            "spearman": rho_2a,
            "pearson": pear_2a,
            "mae": round(float(np.mean(np.abs(
                np.array(pred_days) - np.array(FIG2A_DH)))), 4),
            "mirror_mae": round(mae_2a_mirror, 4),
            "verdict": g1,
            "hours_alternative": {
                "onsets_h": list(FIG2A_RUNGS),
                "stack_prediction": pred_hours,
                "spearman": rho_2a_hours,
                "mae": round(mae_2a_hours, 4),
            },
            "mirror_note_spearman": rho_mirror,
            "control_note": (
                "eid 434 (no octanol) DH 0.00 vs the stack's torus "
                "control P(break)=1.0 (exp100's refusal): the torus's "
                "baseline polarity is inverted relative to the record — "
                "the deadline curve is a rescue curve, the record's "
                "kernel is a damage kernel."),
        },
        "fig2b_prediction": {
            "onsets_h": onsets_vnc,
            "stack_prediction": pred_vnc,
            "published_vnc_dh": list(FIG2B_DH),
            "spearman": rho_2b,
            "pearson": pear_2b,
            "mae": round(mae_2b, 4),
            "mirror_mae": round(mae_2b_mirror, 4),
            "verdict": g2,
            "paper_check": (
                "PMC2823934 (verified verbatim this session): 'Significant "
                "A/P duplications were observed when VNC contiguity was "
                "disrupted prior to 12 hours after amputation' and "
                "'dramatic decrease (4-fold) in the incidence of A/P "
                "defects if the VNC was disrupted after the first 3 hours "
                "post-amputation' — the 3 h peak (0.75 vs 0.18 at t=0, "
                "~4-fold) is the paper's own reading; the flat stack "
                "curve misses it."),
        },
        "criteria": {
            "OK_A1_anchor_gamma4_curve": ok_a1,
            "OK_G1_direction_fig2a": g1,
            "OK_G2_fit_quality_fig2b": g2,
        },
        "verdict": (
            f"{npass}/3 gates PASS (direction {g1}, fit-quality {g2}; "
            f"anchor {'PASS' if ok_a1 else 'REFUTED'})"),
        "notes": (
            "Zero-free-parameter test: the deposited/anchor-verified "
            "gamma-4 torus deadline curve evaluated at the paper-resolved "
            "onsets; no amplitude, sign, or edge refit. The md T1's "
            "analytic-rate variant was pre-refuted by exp125 AN-G1 "
            "(ledger L106); the axis-map fit is the registered remaining "
            "form. The mirror observation (rho_mirror) is deposited as a "
            "NOTE, not a gated rescue — a sign flip would be a free "
            "parameter; the OK-G2 refutation is polarity-invariant on "
            "this grid (mirror MAE deposited). Next-object named by the "
            "data: the record's kernel polarity matches the chain "
            "corpus's delayed-vs-sustained ordering (exp70 ON-G3), not "
            "the torus rescue curve; the Fig 2B 3 h peak is a "
            "write-window object (exp54), not a deadline object. "
            "AUDIT TRAIL: an uncommitted draft finalization of this "
            "target existed in the workspace (no worklog entry); this "
            "run audited it, re-verified every quoted paper passage "
            "verbatim (NCBI efetch PMC2823934), fixed the OK-G1 "
            "degenerate-prediction zone (was routed to PASS; now "
            "PARTIAL — outcome unchanged, rho defined), and deposited "
            "Pearson/mirror-MAE as non-gated descriptives."),
        "sources": {
            "record": "research/levin_voltage_series.json eids 434-444 "
                      "(Oviedo 2010, PMID 20026026)",
            "paper_full_text": "PMC2823934 (Oviedo 2010, PMID 20026026) "
                               "full text; quotes verified verbatim this "
                               "session via NCBI E-utilities efetch "
                               "db=pmc id=2823934 (Europe PMC "
                               "fullTextXML endpoint: HTTP 500 this "
                               "session)",
            "harness": "experiments/exp124_deadline_curve.py run_deadline "
                       "(verbatim); results/exp124_deadline_curve.json "
                       "(anchor); ledger L103-L106",
        },
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
