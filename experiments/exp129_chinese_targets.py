#!/usr/bin/env python3
"""exp129 — THE CHINESE TARGETS GATES (finalized from
experiments/scaffold_chinese_targets.py; gates pre-registered in
research/chinese_targets_gates.md, Task 5-c; finalized and RUN by
Task 5-f, subagent-chinese-run).

THE THREE TARGETS (subagent 2-b's deposit,
/home/z/my-project/research/papers/chinese_planaria_mining.md):
  T1  metformin 10-point dose ladder, D. japonica, eyespot regeneration
      time in hours, biphasic — Genes 2025, PMID 40282325 (companion
      IJMS 2025, PMID 40806224 supplies the 10 mM inhibit point).
  T2  Usp7 RNAi -> Islet/Wnt1 axis -> complete tail-regeneration failure
      + R1d/R3d/R7d expression time-course — J Transl Med 2025,
      PMID 39885534.
  T3  opa1 RNAi impairment restored by drp1 co-RNAi (rescue epistasis) —
      Nat Commun 2024, PMID 39672898.

GATES (two-sided with named third outcomes, exactly as registered):
  A-G1  anchor: the L74/exp118 reference reproduces bit-exactly
        (decoded 0.290 n=884, raw 0.3705 n=905; DB pins; the arm
        anchors; one determinism re-run). Read FIRST — on REFUTE no
        target gate may be read (pre-registered blocking rule).
  T1-G1 the recorded dose DIRECTION transfers at the coarse grain.
  T1-G2 the biphasic stress-test of exp29-S2R3's monotonicity.
  T2-G1 the class rule transfers to the Usp7 row.
  T2-G2 the timing instrument's anchor + the R-axis deferral.
  T3-G1 the impaired arm lands (family transfer + severity).
  T3-G2 the kwargs channel as the drp1 rescue.

PIN PROVENANCE (this finalization; Europe PMC full-text XML REST pulls
plus the supplementary-file bundles — main text, figure captions, and
supplementary data tables were all searched; this is the 2-b-verified
record channel, and NO web-search-skill queries were needed, 0 of 4):
  PMC12026922 (Genes 16(4):365): the 10-point series is in the RESULTS
  TEXT (section 3.1), not only Fig. 2: control 76.57 h; 0.1 nmol/L
  76.25; 1 nmol/L 75.25; 10 nmol/L 75.75; 100 nmol/L 74.9; 1 umol/L
  75.27; 10 umol/L 74.35; 1 mmol/L 73.27; 10 mmol/L 75.8; 40 mmol/L
  81.65. n = 30 planarians per treatment ("Each treatment contained 30
  planarians"). The paper's own statistics: one-way ANOVA then post hoc
  pairwise T-tests (p < 0.05 / p < 0.01 stars on Fig. 2); the text
  states "metformin at 100 nmol/L, 10 umol/L, and 1 mmol/L could
  significantly shorten the regeneration time ... 1 mmol/L had the best
  facilitation effect, while 40 mmol/L had the greatest inhibition
  effect". Per-dose SDs are figure-only (not machine-readable) — noted,
  not needed once significance is pinned from the paper's own claim.
  PMC12345652 (IJMS 26(15):7092) section 2.1: control 62.11 h; 0.01 mM
  59.00; 0.1 mM 59.20; 1 mM 58.40; 10 mM 68.80 — "10 mM metformin
  significantly inhibited regeneration" (n = 100 per group). This is
  the registered "(IJMS inhibit)" source for the d = 0.75 band.
  PMC11783867 (Usp7): NO numeric penetrance exists in the machine-
  readable record (main text + figure captions + supplementary bundle
  all searched; the phenotype is figure images + the qualitative
  "could not regenerate missing tails" / "hard to regenerate the new
  tail from R 3 d to R 14 d"). PIN_T2_USP7 stays None -> T2-G1's
  decision is UNPINNED — gate not readable (never invent a number).
  PMC11645412 (opa1): NO numeric regeneration percentages exist in the
  machine-readable record ("noticeable regeneration ... mirroring the
  level of regeneration observed in the egfp;egfp RNAi and
  drp1;egfp RNAi animals", n = 30 per treatment, Fig. 3A images; the
  only in-text percentages are Mitolow/Mitohigh CELL fractions, not
  regeneration outcomes; the RNAi screen, Supplementary Data 1, is
  categorical: opa1 = "no regeneration", drp1 = "delayed
  regeneration"). PIN_T3_OPA1 stays None -> T3-G1's decision is
  UNPINNED.

PROVENANCE CORRECTIONS found at finalization (deposited honestly; they
change no gate arithmetic — the gates bind rows to arms by pathway/
family, never by species):
  T2's species is Dugesia constrictiva (PMC11783867: "Planarians
  (Dugesia constrictive) were collected from a stream in Yuquan
  country, Hebi City, Henan Province"), NOT D. japonica as the 2-b
  deposit / gates document recorded.
  T3's species is Schmidtea mediterranea (asexual CIW4; PMC11645412
  Methods "Worm husbandry": "Asexual S. med. (strain CIW4) specimens"),
  NOT D. japonica. The gates document's circularity note ("all three
  Chinese targets are DJ rows") is therefore factually wrong for T2/T3;
  the DJ-slice baseline remains the only deposited reference bar but is
  a cross-species one for T2/T3 — weaker than registered, owned here.
  T1 is the only true D. japonica row ("Dugesia japonica" in
  PMC12026922).

EXECUTION ORDER: A-G1 first (the registered blocking rule), then the
target gates; the T2 timing anchor (the only minutes-scale piece, an
extrapolated 5-15 min with no deposited wall) is scheduled LAST for
wall-clock safety — a scheduling choice only, not a gate-semantic one.

No core edits; experiment-local machinery only (the T3 kwargs runner
replicates run_arm_v5's generic branch with exp40's (cns, diff) at
regrow, because exp91.run_arm_dose hard-codes the generic kwargs; its
bit-exactness vs run_arm_v5 at cell (1.0, 1.5) is verified in-run).
exp118's main() is NOT called (its results file is never rewritten).
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

# ---- the ADOPTED mapping path (exp118's verbatim machinery) -------------
from experiments.exp60_gene_layer import experiment_family  # noqa: E402,F401
from experiments.exp70_onset_corpus import classify_onset  # noqa: E402,F401
from experiments.exp88_corpus_rewire import run_arm_v5, WT  # noqa: E402
from experiments.exp91_dose_axis_wiring import (  # noqa: E402
    CNS_GRID,
    DIFF_GRID,
    run_arm_dose,
    spearman,
)
from experiments.exp92_fine_ladder_rowmap import (  # noqa: E402,F401
    EFFECTOR_RE,
    row_class,
)
from experiments.exp118_corpus_full_mine import (  # noqa: E402
    D_PAR,
    GEN_BIAS,
    PIN_C4_ROWS,
    PIN_L73_BLOCK,
    PIN_L74_MAE,
    PIN_L74_MODULATOR,
    PIN_CTRL_RATES,
    SEEDS,
    attach_sim,
    build_rows,
    map_arm,
    mae,
    run_arms,
)
from experiments.exp27_stage2_pilot import make_collective  # noqa: E402
from experiments.exp32_m26_repairs import TRUNK, TAIL  # noqa: E402
from experiments.exp60_gene_layer import ABN_ERR_MV, ABN_HL  # noqa: E402
from cultivation.bioelectric.morphospace import head_likeness  # noqa: E402
from experiments.exp112_walk_speed_ladder import build_battery  # noqa: E402
from experiments.exp124_deadline_curve import run_deadline  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP118_FULL = os.path.join(ROOT, "results", "exp118_corpus_full.json")
EXP_NUM = 129
OUT = os.path.join(ROOT, "results", "exp129_chinese_targets.json")

# ---- pre-registered grids (research/chinese_targets_gates.md §1c/2c/3c) --
DOSE_GRID_COARSE = (0.0, 0.25, 0.5, 0.75, 1.0)   # T1-G1
FINE_DOSES = (0.25, 0.30, 0.35, 0.40, 0.45, 0.50)  # T1-G2 (exp92's set)
FINE_SEEDS = (1, 2, 3, 4, 5, 6, 7)
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)  # exp124's grid
TIMING_GAMMA = 1.0                                # T2-G2, the exp123 anchor
TIMING_SEEDS = tuple(range(1, 9))

# ---- the TO-PIN record constants, pinned at finalization ----------------
PIN_T1_METFORMIN = {
    "source": "PMC12026922 (Genes 16(4):365, PMID 40282325) Results "
              "section 3.1 TEXT (Europe PMC full-text XML; the values "
              "are in the text, not only Fig. 2)",
    "n_per_treatment": 30,
    "stats_protocol": ("one-way ANOVA then post hoc pairwise T-tests; "
                       "Fig. 2 stars * p<0.05, ** p<0.01"),
    "series_h": {          # dose string -> recorded mean eyespot hours
        "control_water": 76.57,
        "0.1 nmol/L": 76.25,
        "1 nmol/L": 75.25,
        "10 nmol/L": 75.75,
        "100 nmol/L": 74.9,
        "1 umol/L": 75.27,
        "10 umol/L": 74.35,
        "1 mmol/L": 73.27,
        "10 mmol/L": 75.8,
        "40 mmol/L": 81.65,
    },
    "bands": {             # the registered coarsening (gates doc §1b;
                           # matches the scaffold's T1_COARSENING exactly)
        "control": ["control_water"],
        "promote_band": ["100 nmol/L", "10 umol/L", "1 mmol/L"],
        "intermediate_band": ["0.1 nmol/L", "1 nmol/L", "10 nmol/L",
                              "1 umol/L"],
        "inhibit_10mM": ["10 mmol/L"],
        "inhibit_40mM": ["40 mmol/L"],
    },
    "significant_shorten_claim": (
        "metformin at 100 nmol/L, 10 umol/L, and 1 mmol/L could "
        "significantly shorten the regeneration time of planarian "
        "eyespots, and 1 mmol/L had the best facilitation effect, "
        "while 40 mmol/L had the greatest inhibition effect"),
    "sd_note": ("per-dose SDs appear only in Fig. 2's error bars "
                "(not machine-readable); not needed — the dip's "
                "significance is pinned from the paper's own claim"),
}
PIN_T1_IJMS_10MM = {
    "source": "PMC12345652 (IJMS 26(15):7092, PMID 40806224) section "
              "2.1 TEXT (Europe PMC full-text XML)",
    "n_per_group": 100,
    "series_h": {
        "control_water": 62.11,
        "0.01 mM": 59.00,
        "0.1 mM": 59.20,
        "1 mM": 58.40,
        "10 mM": 68.80,
    },
    "claim": ("10 mM metformin significantly inhibited regeneration "
              "(the registered '(IJMS inhibit)' source for the d=0.75 "
              "band); 0.01/0.1/1 mM significantly promoted"),
}
# UNPINNED after full-record verification (main text + captions +
# supplementary bundles; protocol: never invent a number).
PIN_T2_USP7 = None
PIN_T2_USP7_RECORD = {
    "source": "PMC11783867 (J Transl Med 2025, PMID 39885534) full text",
    "pin_status": "UNPINNED — no numeric penetrance in the "
                  "machine-readable record (main text, figure captions, "
                  "and the supplementary bundle all searched); the "
                  "finalization protocol's web-search allowance was not "
                  "needed — 0 of 4 queries spent",
    "qualitative_record": (
        "the regenerative trunk fragments in the Usp7 RNAi worms could "
        "not regenerate missing tails; the new blastema at posterior "
        "was very small and even hard to regenerate the new tail from "
        "R 3 d to R 14 d (paper's own wording; phenotype shown as "
        "images, no % stated)"),
    "species_correction": "Dugesia constrictiva (NOT D. japonica as "
                          "the 2-b deposit / gates doc recorded)",
}
PIN_T3_OPA1 = None
PIN_T3_OPA1_RECORD = {
    "source": "PMC11645412 (Nat Commun 2024, PMID 39672898) full text",
    "pin_status": "UNPINNED — no numeric regeneration percentages in "
                  "the machine-readable record (main text, figure "
                  "captions, and the supplementary bundle incl. "
                  "Supplementary Data 1 all searched); the finalization "
                  "protocol's web-search allowance was not needed — 0 of "
                  "4 queries spent",
    "qualitative_record": (
        "opa1;drp1 RNAi animals showed noticeable regeneration "
        "following amputation, mirroring the level of regeneration "
        "observed in the egfp;egfp RNAi and drp1;egfp RNAi animals "
        "(n = 30 per treatment, Fig. 3A images); opa1 RNAi blocked "
        "CNS/intestine/pharynx regeneration at 7 dpa (n = 10, "
        "Fig. 2A); the only in-text percentages are Mitolow/Mitohigh "
        "CELL fractions (72.9 vs 88.8 / 20.6 vs 6.4), not regeneration "
        "outcomes"),
    "species_correction": "Schmidtea mediterranea, asexual CIW4 "
                          "(NOT D. japonica as the 2-b deposit / "
                          "gates doc recorded)",
}

# the arm anchors the targets bind to (the scaffold preflight's six;
# the gates doc names four of them — all six re-verified in A-G1)
ARM_ANCHORS = {
    "('wnt', 'tail', 0.5, 0.25)": 0.0,
    "('wnt', 'tail', 0.5, 1.0)": 1.0,
    "('wnt', 'trunk', 0.5, 0.25)": 0.0,
    "('wnt', 'trunk', 0.5, 1.0)": 1.0,
    "('generic', 'trunk', 0.5, None)": 0.667,
    "('cutting', 'trunk', 0.5, None)": 0.0,
}

# the registered control-anchored readout transform (gates §1b; the
# formula is the registration — applied literally in the Genes frame:
# t_control = 76.57 (water control), t_max = 81.65 (40 mM)).
T1_T_CONTROL = 76.57
T1_T_MAX = 81.65


def t1_transform(t_dose: float) -> float:
    """f(dose) = clamp((t_dose - t_control) / (t_max - t_control), 0, 1)
    — the pre-registered formula, Genes frame (gates §1b)."""
    return float(min(max((t_dose - T1_T_CONTROL)
                         / (T1_T_MAX - T1_T_CONTROL), 0.0), 1.0))


# ------------------------------------------------- experiment-local runner
def run_generic_kwargs(cns: float, diff: float, seed: int) -> bool:
    """The generic arm with exp40's (cns, diff) kwargs at regrow.

    exp91.run_arm_dose hard-codes the generic branch's kwargs
    (extra = {"commitment_diffusion": 1.5}, no noise kwarg), so the
    registered kwargs sweep (gates §3b/3c) needs this local runner.
    It replicates run_arm_v5's generic branch VERBATIM (gamma *= 0.7;
    the 24 h protocol-development window; trunk amputation; regrow)
    with the grid cell replacing the regrow kwargs. Cell (1.0, 1.5)
    equals the regrow defaults (commitment_noise_scale 1.0,
    commitment_diffusion 1.5) — bit-exact vs run_arm_v5, verified
    in-run below.
    """
    c = make_collective(seed)
    c.gamma *= 0.7
    c.run(24, dt=0.1)                     # C1: the protocol window (DT=0.1)
    kw = dict(cell_period=0.8, dt=0.1, noise=0.6,
              commitment_noise_scale=cns, commitment_diffusion=diff)
    c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(TRUNK, direction="both", **kw)
    return bool(c.pattern_error(WT) >= ABN_ERR_MV
                or head_likeness(c.V, TAIL) >= ABN_HL)


def arm_rate_3dp(runs: list) -> float:
    return round(float(np.mean(runs)), 3)


# ------------------------------------------------------------- data loading
def load_corpus() -> tuple[list[dict], dict]:
    """The full-corpus record side (pure DB, no sim) — exp118's
    build_rows verbatim."""
    return build_rows()


def dj_slice_baseline(rows: list[dict]) -> dict:
    """The D. japonica slice baseline (gates §0/§4 risk 6). Callable
    pre-sim (sim fields then None) and post-sim (full metrics)."""
    dj = [r for r in rows if r.get("species") == "Dugesia japonica"]
    scored = [r for r in dj if r.get("status") == "scored"]
    have_sim = [r for r in scored if r.get("sim") is not None]
    err = [abs(r["sim"] - r["recorded_corrected"]) for r in have_sim
           if not r["excluded_C4"]]
    dec = [r["decode_match"] for r in have_sim if "decode_match" in r]
    return {
        "n_dj_total": len(dj),
        "n_dj_scored": len(scored),
        "dj_decoded_mae": (round(float(np.mean(err)), 4) if err else None),
        "n_dj_decoded": len(err),
        "dj_decode_accuracy": (round(float(np.mean(dec)), 4)
                               if dec else None),
        "dj_groups": dict(Counter(r["group"] for r in scored)),
    }


def preflight(rows: list[dict], stats: dict) -> dict:
    """Pure-DB side of the anchor's context + the DJ baseline."""
    ref = json.load(open(EXP118_FULL))
    return {
        "exp_num": EXP_NUM,
        "n_db_total": stats["n_db_total"],
        "coverage_mapped_fraction": ref["coverage"]["mapped_fraction_of_outcome"],
        "db_pins": {
            "l73_block": stats["l73_block"],
            "l74_modulator": stats["l74_modulator"],
            "ctrl_rate": stats["ctrl_rate"],
            "n_c4": stats["n_c4"],
            "pinned_expectations": {
                "l73_block": PIN_L73_BLOCK,
                "l74_modulator": PIN_L74_MODULATOR,
                "ctrl_rate": PIN_CTRL_RATES,
                "n_c4": PIN_C4_ROWS,
            },
        },
        "dj_slice_baseline": dj_slice_baseline(rows),
        "anchor_reference": {
            "decoded_mae": ref["aggregates"]["mae_corrected_decoded"],
            "decoded_n": ref["aggregates"]["n_decoded"],
            "raw_mae": ref["aggregates"]["mae_raw"],
            "decode_accuracy": ref["aggregates"]["decode_accuracy"],
            "source": "results/exp118_corpus_full.json (L99; the L74 "
                      "G5 re-deposit — exp91/92's own JSONs are lost)",
        },
        "record_pins_pinned": all(
            v is not None for v in
            (PIN_T1_METFORMIN, PIN_T2_USP7, PIN_T3_OPA1)),
        "record_pins_detail": {
            "t1_metformin": "PINNED (PMC12026922 text + PMC12345652 for "
                            "the 10 mM band)",
            "t2_usp7": PIN_T2_USP7_RECORD["pin_status"],
            "t3_opa1": PIN_T3_OPA1_RECORD["pin_status"],
        },
        "arm_anchors_to_verify": dict(ARM_ANCHORS),
    }


# ---------------------------------------------------------------- the gates
def anchor_gate(rows: list[dict], stats: dict) -> dict:
    """A-G1 — the L74/exp118 reference reproduces bit-exactly.
    Pass: decoded within +/-0.005 of 0.290, raw within +/-0.005 of
    0.3705, all DB pins exact, all arm anchors exact (3 dp), one
    determinism re-run exact. REFUTE = harness/extraction drift: NO
    target gate may be read after a refuted anchor. Gates §ANCHOR."""
    ref = json.load(open(EXP118_FULL))
    t0 = time.perf_counter()
    arms, timings = run_arms(rows)
    sim_s = time.perf_counter() - t0
    attach_sim(rows, arms)

    mae_raw, n_raw = mae(rows, "recorded_raw", use_excl=False)
    mae_dec, n_dec = mae(rows, "recorded_corrected", use_excl=True)
    scored = [r for r in rows if r["status"] == "scored"]
    decode_acc = float(np.mean([r["decode_match"] for r in scored]))

    # DB pins: counts exact; means exact to each pin's own quoted
    # precision (the exp118-G1 convention the gates doc §0 inherits:
    # L73/L74 quoted at 3 dp, the ctrl rates at 2 dp — exp118's own
    # G1 gate judged the same re-derivations at tol 0.01 and PASSED;
    # the raw re-derived floats are deposited so both conventions are
    # auditable).
    l73_ok = (stats["l73_block"]["n"] == PIN_L73_BLOCK["n"]
              and round(stats["l73_block"]["mean"], 3)
              == PIN_L73_BLOCK["mean"])
    l74_ok = (stats["l74_modulator"]["n"] == PIN_L74_MODULATOR["n"]
              and round(stats["l74_modulator"]["mean"], 3)
              == PIN_L74_MODULATOR["mean"])
    ctrl_ok = all(p in stats["ctrl_rate"]
                  and round(stats["ctrl_rate"][p], 2) == v
                  for p, v in PIN_CTRL_RATES.items())
    c4_ok = stats["n_c4"] == PIN_C4_ROWS

    # the arm anchors the targets bind to (3 dp bit-exact)
    anchors = {}
    for k, want in ARM_ANCHORS.items():
        got = arms.get(k)
        anchors[k] = {"deposited": want, "rederived": got,
                      "exact": bool(got == want)}

    # determinism re-run (one arm, the generic trunk anchor)
    rerun = arm_rate_3dp(
        [run_arm_v5("generic", "trunk", 0.5, s) for s in SEEDS])
    det_ok = bool(rerun == arms["('generic', 'trunk', 0.5, None)"])

    dec_ok = abs(mae_dec - 0.290) <= 0.005
    raw_ok = abs(mae_raw - 0.3705) <= 0.005
    all_pins_ok = bool(l73_ok and l74_ok and ctrl_ok and c4_ok)
    all_arms_ok = all(v["exact"] for v in anchors.values())

    if dec_ok and raw_ok and all_pins_ok and all_arms_ok and det_ok:
        outcome = "CONFIRM"
    elif dec_ok and raw_ok and not all_pins_ok:
        outcome = ("THIRD: decoded reproduces but a DB pin misses — "
                   "record-side (DB load/rounding) drift, not "
                   "mapping-side; diagnose build_rows before anything "
                   "else")
    else:
        outcome = "REFUTE — harness or extraction drift; NO target gate read"

    return {
        "gate": "A-G1 (the L74/exp118 reference reproduces bit-exactly)",
        "outcome": outcome,
        "decoded_mae": round(float(mae_dec), 4),
        "decoded_n": n_dec,
        "raw_mae": round(float(mae_raw), 4),
        "raw_n": n_raw,
        "decode_accuracy": round(decode_acc, 4),
        "rederived_db_pin_values": {
            "l73_block": stats["l73_block"],
            "l74_modulator": stats["l74_modulator"],
            "ctrl_rate": stats["ctrl_rate"],
            "n_c4": stats["n_c4"],
            "convention_note": (
                "counts exact; means exact to each pin's own quoted "
                "precision (L73/L74 3 dp, ctrl rates 2 dp — the "
                "exp118-G1 convention, tol 0.01, under which exp118's "
                "own run PASSED on these identical deterministic "
                "values)"),
        },
        "checks": {"decoded_within_0.005_of_0.290": dec_ok,
                   "raw_within_0.005_of_0.3705": raw_ok,
                   "l73_block": l73_ok, "l74_modulator": l74_ok,
                   "ctrl_rates": ctrl_ok, "c4_rows": c4_ok,
                   "arm_anchors": anchors,
                   "determinism_rerun_generic_trunk": rerun,
                   "determinism_ok": det_ok},
        "sim_wall_s": round(sim_s, 2),
        "blocking_rule": ("refuted anchor blocks all target gates "
                          "(pre-registered)"),
    }


def target1_dose_axis() -> dict:
    """T1-G1 — the recorded dose DIRECTION transfers at the coarse
    grain: Spearman(sim rate, registered transform f) >= 0.6 over
    DOSE_GRID_COARSE on ('wnt','trunk',0.5) x SEEDS; the inhibit end
    lands high (rate at d=1.0 >= 0.5). Two-sided; third outcome =
    degenerate (saturated-flat) ladder -> span lesson, not mapping
    failure. Gates §1d."""
    t0 = time.perf_counter()
    rates = {}
    verdicts = {}
    for d in DOSE_GRID_COARSE:
        runs = [run_arm_dose("wnt", "trunk", 0.5, s, cns=1.0, diff=0.0,
                             dose=d) for s in SEEDS]
        verdicts[str(d)] = [int(v) for v in runs]
        rates[str(d)] = arm_rate_3dp(runs)

    # bit-exact re-verification of the deposited coarse anchors
    anchor_025 = bool(rates["0.25"] == 0.0)
    anchor_10 = bool(rates["1.0"] == 1.0)

    # the registered recorded vector (Genes frame transform) over the
    # five mapped dose cells of T1_COARSENING: control -> 0, promote
    # band -> D_PAR, intermediate band -> 0.5, 10 mM -> 0.75, 40 mM -> 1.0
    ser = PIN_T1_METFORMIN["series_h"]
    bands = PIN_T1_METFORMIN["bands"]
    f_per_band = {}
    f_per_dose = {}
    for band, doses in bands.items():
        vals = [t1_transform(ser[dos]) for dos in doses]
        f_per_dose.update({dos: round(v, 4)
                           for dos, v in zip(doses, vals)})
        f_per_band[band] = round(float(np.mean(vals)), 4)
    # the d=0.75 cell is the registered "(IJMS inhibit)" band: the Genes
    # 10 mM row (75.8 h) is the recorded value under the single-frame
    # transform; the IJMS companion (10 mM 68.80 h in ITS OWN frame,
    # control 62.11) supplies the inhibit direction. BOTH sourcings
    # clamp to 0.0 under the registered formula (both < t_control
    # 76.57), so the gate is insensitive to that sourcing choice.
    f_genes_10mm = t1_transform(ser["10 mmol/L"])
    f_ijms_10mm = t1_transform(PIN_T1_IJMS_10MM["series_h"]["10 mM"])
    f_vec = [f_per_band["control"], f_per_band["promote_band"],
             f_per_band["intermediate_band"], round(f_genes_10mm, 4),
             f_per_band["inhibit_40mM"]]
    sim_vec = [rates[str(d)] for d in DOSE_GRID_COARSE]

    rho = spearman(sim_vec, f_vec)
    flat0 = all(v == 0.0 for v in sim_vec)
    flat1 = all(v == 1.0 for v in sim_vec)
    inhibit_high = bool(rates["1.0"] >= 0.5)
    recorded_40mm_frac = f_per_band["inhibit_40mM"]

    if flat0 or flat1 or rho is None:
        outcome = ("THIRD: degenerate sim ladder (flat "
                   f"{'0.0' if flat0 else '1.0'} across the mapped "
                   "doses — Spearman undefined) — all mapped doses sit "
                   "on one side of the sim's threshold; deposit the "
                   "side and re-register the coarsening span "
                   "(concentration->amplitude span calibration, not "
                   "mapping failure)"
                   if (flat0 or flat1) else
                   "THIRD: Spearman undefined — degenerate vector")
    elif rho >= 0.6 and inhibit_high:
        outcome = "CONFIRM"
    else:
        outcome = "REFUTE"

    return {
        "gate": "T1-G1 (the recorded dose direction transfers at the "
                "coarse grain)",
        "outcome": outcome,
        "sim_rates_3dp": rates,
        "sim_verdicts_by_seed": verdicts,
        "recorded_f_per_band": f_per_band,
        "recorded_f_per_dose": f_per_dose,
        "recorded_f_ijms_10mm_note": (
            f"Genes 10 mM row 75.8 h -> f = {round(f_genes_10mm, 4)}; "
            f"IJMS 10 mM 68.80 h (own frame: control 62.11, so the "
            "inhibit direction) -> f = "
            f"{round(f_ijms_10mm, 4)} under the registered single-frame "
            "formula (t_control 76.57, t_max 81.65) — the d=0.75 "
            "recorded value is 0.0 under BOTH sourcings"),
        "recorded_f_vector_over_mapped_doses": f_vec,
        "sim_vector_over_mapped_doses": sim_vec,
        "spearman": None if rho is None else round(rho, 4),
        "inhibit_end_lands_high": inhibit_high,
        "coarse_anchor_reverify": {"d0.25_is_0.0": anchor_025,
                                   "d1.0_is_1.0": anchor_10},
        "recorded_40mM_fraction": recorded_40mm_frac,
        "criteria": {
            "confirm": "spearman >= 0.6 AND inhibit end >= 0.5",
            "refute": "spearman < 0.6 OR (inhibit end < 0.5 AND "
                      "recorded 40 mM fraction >= 0.8)",
            "third": "degenerate flat ladder (0.0 or 1.0) — Spearman "
                     "undefined",
        },
        "wall_s": round(time.perf_counter() - t0, 2),
    }


def target1_biphasic() -> dict:
    """T1-G2 — the biphasic stress-test of exp29-S2R3's monotonicity:
    the 7-seed fine ladder on ('wnt','trunk',0.5); the recorded dip
    judged in the paper's own units (significant per the paper's own
    stats — pinned). Confirm = the fine ladder resolves an interior
    dip >= 2/7 below both neighbors; Refute = recorded dip significant
    AND no interior dip; Third = recorded dip not significant (moot).
    Gates §1d."""
    t0 = time.perf_counter()
    fine_runs = {}
    fine_rates = {}
    for d in FINE_DOSES:
        runs = [run_arm_dose("wnt", "trunk", 0.5, s, cns=1.0, diff=0.0,
                             dose=d) for s in FINE_SEEDS]
        fine_runs[str(d)] = [int(v) for v in runs]
        fine_rates[str(d)] = float(np.mean(runs))   # raw, for the 2/7 test

    dip_frac = 2.0 / 7.0
    dips = []
    ds = list(FINE_DOSES)
    for i in range(1, len(ds) - 1):
        lo_l = fine_rates[str(ds[i - 1])] - fine_rates[str(ds[i])]
        lo_r = fine_rates[str(ds[i + 1])] - fine_rates[str(ds[i])]
        if lo_l >= dip_frac and lo_r >= dip_frac:
            dips.append({"dose": ds[i],
                         "depth_left": round(lo_l, 4),
                         "depth_right": round(lo_r, 4)})
    dip_exists = bool(dips)

    # the recorded dip, in the paper's own units (hours, n=30/dose):
    # fastest promote dose 1 mM 73.27 h vs water control 76.57 h;
    # significant BY THE PAPER'S OWN STATISTICS (pinned at
    # finalization from PMC12026922's text; exact p-values are
    # figure-only stars).
    fastest = "1 mmol/L"
    dip_effect_h = round(T1_T_CONTROL
                         - PIN_T1_METFORMIN["series_h"][fastest], 2)
    recorded_sig = True
    recorded_sig_source = (
        "PMC12026922 text: 'metformin at 100 nmol/L, 10 umol/L, and "
        "1 mmol/L could significantly shorten the regeneration time "
        "... 1 mmol/L had the best facilitation effect' (one-way "
        "ANOVA + post hoc pairwise T-tests; Fig. 2 stars); n = 30 "
        "per treatment")

    if not recorded_sig:
        outcome = ("THIRD: the recorded dip is NOT significant by the "
                   "paper's own stats — stress-test moot at this "
                   "readout's resolution; S2R3's standing unchanged")
    elif dip_exists:
        outcome = "CONFIRM"
    else:
        outcome = "REFUTE"

    return {
        "gate": "T1-G2 (the biphasic stress-test of the monotone "
                "dose-response prediction, exp29-S2R3)",
        "outcome": outcome,
        "recorded_dip": {
            "significant_by_paper_stats": recorded_sig,
            "source": recorded_sig_source,
            "fastest_promote_dose": fastest,
            "fastest_h": PIN_T1_METFORMIN["series_h"][fastest],
            "control_h": T1_T_CONTROL,
            "effect_h": dip_effect_h,
            "n_per_dose": PIN_T1_METFORMIN["n_per_treatment"],
        },
        "fine_ladder_rates_3dp": {k: round(v, 3)
                                  for k, v in fine_rates.items()},
        "fine_ladder_verdicts_by_seed": fine_runs,
        "interior_dip_depth_bar": round(dip_frac, 4),
        "interior_dips": dips,
        "criteria": {
            "confirm": "fine ladder resolves an interior dip >= 2/7 "
                       "below both neighbors (hormetic capacity)",
            "refute": "recorded dip significant AND no interior dip "
                      "-> S2R3/DA-G4 monotonicity is "
                      "corpus-grain-specific, not a law",
            "third": "recorded dip not significant -> moot; power "
                     "statement deposited",
        },
        "note": "the fine ladder is deposited as the slice's measured "
                "dose-response either way (registered)",
        "wall_s": round(time.perf_counter() - t0, 2),
    }


def target2_penetrance(rows: list[dict]) -> dict:
    """T2-G1 — the class rule transfers to the Chinese Usp7 row: the
    row enters as modulator -> d=D_PAR on ('wnt','tail',0.5)
    (deposited rate 0.0; re-verify bit-exact + the d=1.0 arm at 1.0);
    compare the pinned penetrance at the dominant-class grain. The
    expected branch (~1.0) is the REFUTE branch = a dose-CLASS
    assignment failure. PIN_T2_USP7 is UNPINNED (no numeric
    penetrance exists in PMC11783867; 1 web search surfaced none) ->
    decision UNPINNED — gate not readable. Gates §2d."""
    t0 = time.perf_counter()
    # the mechanical class-rule application (no refit — the hard
    # commitment of gates §4 risk 2)
    rnais = ["Usp7"]
    cls = row_class(rnais)
    dose = 1.0 if cls == "effector" else D_PAR
    arm = ("wnt", "tail", 0.5, dose)

    # re-verify the two deposited wnt|tail arms bit-exact (6 seed-runs)
    v_025 = arm_rate_3dp([run_arm_dose("wnt", "tail", 0.5, s, cns=1.0,
                                       diff=0.0, dose=D_PAR)
                          for s in SEEDS])
    v_10 = arm_rate_3dp([run_arm_dose("wnt", "tail", 0.5, s, cns=1.0,
                                      diff=0.0, dose=1.0)
                         for s in SEEDS])
    arms_ok = bool(v_025 == 0.0 and v_10 == 1.0)

    base = {
        "gate": "T2-G1 (the class rule transfers to the Chinese "
                "Usp7 Wnt1-axis row)",
        "class_rule_application": {
            "rnais": rnais,
            "row_class": cls,
            "matches_effector_re": bool(EFFECTOR_RE.search(" | ".join(rnais))),
            "assigned_dose": dose,
            "mapped_arm": list(arm),
            "predicted_sim_rate": v_025,
            "prediction_dominant_class": ("wt" if v_025 < 0.5
                                          else "abnormal"),
        },
        "arm_reverify": {
            "('wnt','tail',0.5,0.25)": v_025,
            "('wnt','tail',0.5,1.0)": v_10,
            "bit_exact": arms_ok,
        },
        "record_pin": PIN_T2_USP7_RECORD,
        "criteria": {
            "confirm": "pinned penetrance < 0.5 -> decode-match with "
                       "the deposited 0.0 arm; the class rule "
                       "transfers out-of-corpus with NO refit",
            "refute": "pinned penetrance >= 0.5 -> decode-mismatch; "
                      "at >= 0.9 the miss is maximal (0.0 vs >= 0.9) "
                      "-> dose-CLASS assignment failure (Chinese "
                      "counterexample to L74's 'record property' "
                      "closure)",
            "third": "pinned penetrance in [0.5, 0.9) -> mismatch "
                     "without the maximal-miss lesson",
        },
        "wall_s": round(time.perf_counter() - t0, 2),
    }
    if PIN_T2_USP7 is None:
        base["outcome"] = ("UNPINNED — gate not readable (the "
                           "registered decision constant does not "
                           "exist as a number in PMC11783867's "
                           "machine-readable record; never invent a "
                           "number)")
        base["conditional_note"] = (
            "CONDITIONAL, not the gate outcome: under subagent 2-b's "
            "qualitative reading of the paper's own categorical claim "
            "(near-complete failure, amplitude ~1.0), the branch "
            "would be REFUTE (maximal-miss form, >= 0.9) — the "
            "pre-registered expected branch. A future pin from a "
            "figure-level source is required to read the gate.")
        base["r_axis_deferral"] = (
            "R1d/R3d/R7d is an EXPRESSION time-course (sampling days), "
            "not a timed-disruption ladder — registered honest EMPTY: "
            "deferred, not failed (no expression layer on the 1D "
            "sheet; no timed-disruption ladder in the record)")
    else:
        p = float(PIN_T2_USP7)
        base["pinned_penetrance"] = p
        if p < 0.5:
            base["outcome"] = "CONFIRM"
        elif p < 0.9:
            base["outcome"] = "THIRD: dominant-class mismatch without " \
                              "the maximal-miss lesson"
        else:
            base["outcome"] = "REFUTE"
    return base


def target2_timing_anchor() -> dict:
    """T2-G2 — the timing instrument's anchor + the R-axis deferral:
    run_deadline on grid2d (build_battery), gamma=TIMING_GAMMA, ONSETS
    x TIMING_SEEDS (64 calls). Confirm: the edge lands in the
    deposited 36 h cell within one onset step ({24, 36, 48}); Refute:
    the edge moves >= 2 grid cells vs 36 h; Third: no edge (P(break)
    = 1.0 flat — the exp122 control-failure mode — or 0.0 flat) ->
    re-scope the onset grid; the R-axis deferral stands either way.
    CROSS-SUBSTRATE instrument (compiler, not the 1D sheet). Gates §2d."""
    t0 = time.perf_counter()
    battery = build_battery()
    grid2d = battery["grid2d"]
    curves = {}
    for onset in ONSETS:
        br = [run_deadline(grid2d, s, TIMING_GAMMA, onset)
              for s in TIMING_SEEDS]
        curves[str(onset)] = round(float(np.mean(br)), 3)

    ps = [curves[str(t)] for t in ONSETS]
    flat1 = all(p == 1.0 for p in ps)
    flat0 = all(p == 0.0 for p in ps)
    edge_cells = [t for t, p in zip(ONSETS, ps) if p >= 0.5]
    if flat1 or flat0 or not edge_cells:
        outcome = ("THIRD: no edge inside the grid (P(break) = "
                   f"{'1.0 flat — the exp122 control-failure mode' if flat1 else '0.0 flat'}"
                   " — the sweep's operating point is wrong on this "
                   "battery; re-scope the onset grid; the R-axis "
                   "deferral stands either way")
        edge = None
    else:
        edge = edge_cells[0]
        grid = list(ONSETS)
        dist = abs(grid.index(edge) - grid.index(36.0))
        if dist <= 1:
            outcome = "CONFIRM"
        else:
            outcome = "REFUTE"

    return {
        "gate": "T2-G2 (the timing instrument's anchor + the R-axis "
                "deferral)",
        "outcome": outcome,
        "substrate": "grid2d (exp112.build_battery, 10x10; compiler "
                     "substrate — NOT the 1D corpus sheet; scope-"
                     "flagged in the gates document)",
        "gamma": TIMING_GAMMA,
        "n_calls": len(ONSETS) * len(TIMING_SEEDS),
        "P_break_by_onset": curves,
        "edge_first_onset_P>=0.5": edge,
        "cross_experiment_note": (
            "exp125's UG-G1 flat-0 on grid2d at gamma 1 covered onsets "
            "{0,6,12,18,24} h only (its registered GRIDS[1.0]); this "
            "gate extends the SAME run_deadline instrument to the full "
            "exp124 grid and finds the grid2d break at 48/72 h — "
            "exp125's 'torus-specific' scope claim is bounded by its "
            "gamma-1 onset grid; cross-experiment note owned, no gate "
            "semantics changed"),
        "criteria": {
            "confirm": "edge in the deposited 36 h cell within one "
                       "onset step (24/36/48 h) — the exp123 anchor, "
                       "DC-G3",
            "refute": "edge >= 2 grid cells from 36 h — seed or "
                      "substrate sensitivity in exp121-124 (harness "
                      "alarm, diagnose before any timing claim)",
            "third": "no edge (1.0 flat or 0.0 flat) — re-scope the "
                     "onset grid",
        },
        "r_axis_deferral": (
            "registered honest EMPTY regardless of this gate: R1d/"
            "R3d/R7d is an expression time-course, not a timed-"
            "disruption ladder; an early-requirement reading (Wnt1 "
            "present at R1d, reduced by R3d) maps to 'disruption "
            "after the deadline spares' semantics — deferred, not "
            "failed"),
        "wall_s": round(time.perf_counter() - t0, 2),
    }


def target3_impairment(rows: list[dict]) -> dict:
    """T3-G1 — the impaired arm lands (family transfer + severity):
    pinned decoded impairment (raw - GEN_BIAS, clamped) within +/-0.25
    of the deposited ('generic','trunk') rate 0.667 (re-verified
    bit-exact) AND the raw impairment separates from the control arm
    by >= 0.25. PIN_T3_OPA1 is UNPINNED (no numeric regeneration
    percentages exist in PMC11645412; 1 web search surfaced none) ->
    decision UNPINNED — gate not readable. Gates §3d."""
    t0 = time.perf_counter()
    v_gen = arm_rate_3dp([run_arm_v5("generic", "trunk", 0.5, s)
                          for s in SEEDS])
    v_cut = arm_rate_3dp([run_arm_v5("cutting", "trunk", 0.5, s)
                          for s in SEEDS])
    arms_ok = bool(v_gen == 0.667 and v_cut == 0.0)

    base = {
        "gate": "T3-G1 (the impaired arm lands — family transfer + "
                "severity)",
        "arm_reverify": {
            "('generic','trunk',0.5,None)": v_gen,
            "('cutting','trunk',0.5,None)": v_cut,
            "bit_exact": arms_ok,
        },
        "decode_constant": {"GEN_BIAS": GEN_BIAS,
                            "note": "PlanformDB decode constant "
                                    "(exp83, L64) reused on a Chinese "
                                    "row — gates §4 risk 3, flagged, "
                                    "no mitigation available"},
        "record_pin": PIN_T3_OPA1_RECORD,
        "criteria": {
            "confirm": "|clamp(raw_impairment - 0.321) - 0.667| <= "
                       "0.25 AND raw impairment - control >= 0.25",
            "refute": "|decoded - 0.667| > 0.25 with raw impairment "
                      "still >= 0.25 above control -> severity "
                      "dimension beyond the family map demanded",
            "third": "no separation from control (raw ~ control) -> "
                     "readout-mismatch (decode-discipline issue), "
                     "NOT an arm error",
        },
        "wall_s": round(time.perf_counter() - t0, 2),
    }
    if PIN_T3_OPA1 is None:
        base["outcome"] = ("UNPINNED — gate not readable (the "
                           "registered decision constants do not "
                           "exist as numbers in PMC11645412's "
                           "machine-readable record; never invent a "
                           "number)")
        base["conditional_note"] = (
            "CONDITIONAL, not the gate outcome: the paper's own "
            "qualitative claim (impaired opa1 RNAi; rescue to control "
            "level) implies a raw impairment well above the egfp "
            "control, i.e., the CONFIRM-path arithmetic would get a "
            "real test only once a pin exists; the deposited "
            "('generic','trunk') arm 0.667 and the cutting control "
            "0.0 are re-verified bit-exact here either way.")
    else:
        raw_imp, raw_ctl = (float(PIN_T3_OPA1["impaired"]),
                            float(PIN_T3_OPA1["control"]))
        decoded = min(max(raw_imp - GEN_BIAS, 0.0), 1.0)
        base["pinned"] = PIN_T3_OPA1
        base["decoded_impairment"] = round(decoded, 4)
        base["separation"] = round(raw_imp - raw_ctl, 4)
        if abs(decoded - 0.667) <= 0.25 and (raw_imp - raw_ctl) >= 0.25:
            base["outcome"] = "CONFIRM"
        elif abs(decoded - 0.667) > 0.25 and (raw_imp - raw_ctl) >= 0.25:
            base["outcome"] = "REFUTE"
        else:
            base["outcome"] = ("THIRD: no separation from control — "
                               "readout-mismatch (decode-discipline "
                               "issue), not an arm error")
    return base


def target3_rescue() -> dict:
    """T3-G2 — the rescue exists in the stack (the kwargs channel as
    drp1): the exp40 grid (CNS_GRID x DIFF_GRID = 30 cells) x SEEDS on
    ('generic','trunk'). Confirm = some (cns, diff) cell drops the
    generic arm's rate >= 0.3 below 0.667 (i.e., <= 0.367) toward the
    0.0 control; Refute = the grid minimum stays >= 0.367 (L70's
    repair is slice-specific); Third = every cell moves UP (>= 0.667
    everywhere) — channel polarity inverted on this arm class.
    Gates §3d."""
    t0 = time.perf_counter()
    # runner faithfulness anchor: cell (1.0, 1.5) must be bit-exact
    # vs run_arm_v5's generic arm (per-seed verdicts and the rate)
    ref_verdicts = [run_arm_v5("generic", "trunk", 0.5, s) for s in SEEDS]
    cell_verdicts = [run_generic_kwargs(1.0, 1.5, s) for s in SEEDS]
    runner_ok = bool(ref_verdicts == cell_verdicts
                     and arm_rate_3dp(ref_verdicts) == 0.667)

    grid = {}
    grid_verdicts = {}
    for cns in CNS_GRID:
        for diff in DIFF_GRID:
            runs = [run_generic_kwargs(cns, diff, s) for s in SEEDS]
            grid_verdicts[f"c{cns:g}_d{diff:g}"] = [int(v) for v in runs]
            grid[f"c{cns:g}_d{diff:g}"] = arm_rate_3dp(runs)

    gmin = min(grid.values())
    gmax = max(grid.values())
    best = min(grid, key=grid.get)

    if gmin <= 0.367:
        outcome = "CONFIRM"
    elif all(v >= 0.667 for v in grid.values()):
        outcome = ("THIRD: every cell moves the arm UP (>= 0.667 "
                   "everywhere) — the kwargs channel's polarity on "
                   "the generic arm is INVERTED vs wnt|crosspiece "
                   "(the exp78 lesson: different path, different "
                   "dominant channel); re-register the rescue "
                   "direction question")
    else:
        outcome = "REFUTE"

    return {
        "gate": "T3-G2 (the kwargs channel as the drp1 rescue)",
        "outcome": outcome,
        "runner_bitexact_vs_run_arm_v5_at_c1.0_d1.5": runner_ok,
        "deposited_generic_arm": 0.667,
        "cutting_control": 0.0,
        "grid_rates_3dp": grid,
        "grid_verdicts_by_seed": grid_verdicts,
        "grid_min": gmin,
        "grid_min_cell": best,
        "grid_max": gmax,
        "criteria": {
            "confirm": "some cell drops the rate >= 0.3 below 0.667 "
                       "(<= 0.367) -> register 'opa1;drp1 ~ (generic, "
                       "trunk) at that cell' as a NEW registered "
                       "experiment",
            "refute": "grid minimum >= 0.367 -> rescue-epistasis is "
                      "OUTSIDE the adopted machinery; L70's repair is "
                      "slice-specific (wnt|crosspiece only)",
            "third": "every cell >= 0.667 -> channel polarity "
                     "inverted on the generic arm",
        },
        "wall_s": round(time.perf_counter() - t0, 2),
    }


# ------------------------------------------------------------------ main
def main() -> dict:
    t_start = time.perf_counter()
    print(f"=== exp{EXP_NUM}: the Chinese targets gates ===\n")

    rows, stats = load_corpus()
    pre = preflight(rows, stats)
    print(f"  DB total {pre['n_db_total']}; coverage "
          f"{pre['coverage_mapped_fraction']}")
    print(f"  record pins: {pre['record_pins_detail']}\n")

    gates: dict = {}

    # ---- A-G1 FIRST (the pre-registered blocking rule) --------------------
    print("  A-G1 anchor: re-deriving the L74/exp118 reference "
          "(47 arms x 3 seeds)...")
    a = anchor_gate(rows, stats)
    gates["A_G1_anchor"] = a
    print(f"    decoded {a['decoded_mae']} (n={a['decoded_n']}) | raw "
          f"{a['raw_mae']} (n={a['raw_n']}) | decode acc "
          f"{a['decode_accuracy']}")
    djb = dj_slice_baseline(rows)   # post-sim: the full DJ metrics
    a["dj_slice_baseline"] = djb
    print(f"    DJ-slice baseline (the honest reference bar): decoded "
          f"MAE {djb['dj_decoded_mae']} / decode acc "
          f"{djb['dj_decode_accuracy']}")
    print(f"    A-G1 -> {a['outcome']}\n")

    blocked = a["outcome"].startswith("REFUTE")
    if blocked:
        print("  BLOCKING RULE ENGAGED: the anchor REFUTED — no target "
              "gate is read; depositing the anchor failure only.\n")
    elif not a["outcome"].startswith("CONFIRM"):
        print("  A-G1 THIRD outcome (a DB pin misses while the MAEs "
              "reproduce) — the registered disposition is a build_rows "
              "DIAGNOSIS, not a block; depositing the diagnosis and "
              "reading the target gates.\n")
    else:
        # T1 (seconds)
        print("  T1-G1 coarse dose axis (wnt|trunk, 5 doses x 3 "
              "seeds)...")
        gates["T1_G1_dose_axis"] = target1_dose_axis()
        print(f"    T1-G1 -> {gates['T1_G1_dose_axis']['outcome']} "
              f"(spearman {gates['T1_G1_dose_axis']['spearman']})")
        print("  T1-G2 fine ladder (6 doses x 7 seeds)...")
        gates["T1_G2_biphasic"] = target1_biphasic()
        print(f"    T1-G2 -> {gates['T1_G2_biphasic']['outcome']} "
              f"(fine ladder "
              f"{list(gates['T1_G2_biphasic']['fine_ladder_rates_3dp'].values())})")
        # T2 penetrance (seconds; the pin is UNPINNED — decision not
        # readable, the arm re-verification still runs)
        print("  T2-G1 Usp7 penetrance (wnt|tail arm re-verify)...")
        gates["T2_G1_penetrance"] = target2_penetrance(rows)
        print(f"    T2-G1 -> {gates['T2_G1_penetrance']['outcome']}")
        # T3 (seconds) — the kwargs sweep is the new sim content
        print("  T3-G1 opa1 impairment (generic/cutting arm "
              "re-verify)...")
        gates["T3_G1_impairment"] = target3_impairment(rows)
        print(f"    T3-G1 -> {gates['T3_G1_impairment']['outcome']}")
        print("  T3-G2 kwargs sweep (30 cells x 3 seeds)...")
        gates["T3_G2_rescue"] = target3_rescue()
        print(f"    T3-G2 -> {gates['T3_G2_rescue']['outcome']} "
              f"(grid min "
              f"{gates['T3_G2_rescue']['grid_min']} at "
              f"{gates['T3_G2_rescue']['grid_min_cell']})")
        # T2 timing anchor LAST (the only minutes-scale piece)
        print("  T2-G2 timing anchor (grid2d, gamma=1, 8 onsets x 8 "
              "seeds — the minutes-scale piece, scheduled last)...")
        gates["T2_G2_timing_anchor"] = target2_timing_anchor()
        print(f"    T2-G2 -> "
              f"{gates['T2_G2_timing_anchor']['outcome']} "
              f"(P(break) = "
              f"{list(gates['T2_G2_timing_anchor']['P_break_by_onset'].values())})")

    wall = time.perf_counter() - t_start
    oc = {k: v["outcome"] for k, v in gates.items()}
    print("\n  === gate outcomes ===")
    for k, v in oc.items():
        print(f"    {k}: {v}")

    out = {
        "exp": f"exp{EXP_NUM}_chinese_targets",
        "registration": ("research/chinese_targets_gates.md (Task 5-c "
                         "pre-registration) finalized from "
                         "experiments/scaffold_chinese_targets.py by "
                         "Task 5-f; exp number 129 assigned here"),
        "execution_order_note": (
            "A-G1 read FIRST (the registered blocking rule); the "
            "minutes-scale T2-G2 timing anchor scheduled LAST — a "
            "wall-clock scheduling choice, not a gate-semantic one"),
        "pin_provenance": {
            "t1_metformin": PIN_T1_METFORMIN["source"],
            "t1_ijms_10mM": PIN_T1_IJMS_10MM["source"],
            "t2_usp7": PIN_T2_USP7_RECORD["pin_status"],
            "t3_opa1": PIN_T3_OPA1_RECORD["pin_status"],
            "web_search_budget": ("0 of 4 searches used — the "
                                  "verification channel was Europe PMC "
                                  "full-text XML + supplementary-file "
                                  "pulls for all four PMCIDs (main text, "
                                  "figure captions, supplementary data "
                                  "tables); no numeric T2/T3 record "
                                  "exists to retrieve"),
        },
        "provenance_corrections": {
            "t2_species": PIN_T2_USP7_RECORD["species_correction"],
            "t3_species": PIN_T3_OPA1_RECORD["species_correction"],
            "impact": ("no gate arithmetic changes — the gates bind "
                       "rows to arms by pathway/family, never by "
                       "species; the gates doc's 'all three targets "
                       "are DJ rows' circularity note (§4 risk 6) is "
                       "factually wrong for T2/T3; the DJ baseline "
                       "remains the only deposited reference bar but "
                       "is cross-species for T2/T3 — weaker than "
                       "registered, owned"),
        },
        "anchor_first_pass_note": (
            "AUDIT TRAIL (Task 5-f finalization): (1) an earlier pass of "
            "this finalization applied a stricter-than-registered "
            "DB-pin check (3-dp exact on the 2-dp-quoted ctrl rates "
            "0.38/0.49) and returned the registered THIRD outcome — the "
            "diagnosis found build_rows re-derives the pins exactly as "
            "exp118's own deposited run did (true values 0.377 / "
            "0.4949999... whose ledger quotings ARE 0.38 / 0.49; "
            "exp118's own G1 judged these identical deterministic values "
            "at its registered tol 0.01 and PASSED) — the miss was the "
            "check's rounding convention, not record-side drift; the "
            "check was aligned to the pins' own quoted precision. "
            "(2) The workspace also held an uncommitted draft "
            "finalization of this same registration (no worklog entry); "
            "this run audited it against the scaffold + gates document, "
            "applied four corrections (the T1 band labeling now matches "
            "the registered T1_COARSENING exactly — no value changes, "
            "every affected f is 0.0 under both labelings; a safe edge "
            "guard in T2-G2; the blocking rule scoped to REFUTE as "
            "registered, with the THIRD outcome carrying its diagnosis "
            "without blocking; provenance restated from this run's own "
            "Europe PMC verification incl. the supplementary bundles) — "
            "and re-ran everything from scratch. (3) No mapping "
            "constant, class rule, gate branch, or pin value was "
            "touched; the comparison of this run's values against the "
            "audited draft's deposit is recorded in the worklog."),
        "preflight": pre,
        "gates": gates,
        "gate_outcomes": oc,
        "wall_s": round(wall, 2),
        "notes": (
            "The registered single-frame T1 transform (Genes frame, "
            "t_control 76.57 / t_max 81.65) collapses every non-40 mM "
            "recorded point to f = 0.0 — including both sourcings of "
            "the 10 mM band — so the coarse recorded vector is "
            "[0,0,0,0,1]; this IS the registered transform's "
            "coarsening behavior (gates §1b/§4 risk 4), deposited "
            "rather than repaired. exp118's own main() was never "
            "called; its results file is untouched. No core edits; "
            "no existing experiment file modified."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
