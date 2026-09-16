#!/usr/bin/env python3
"""exp133 — THE WOUND-DOMAIN READOUT TEST (the M35 inherited gate; ledger
L112's exp133 registration: "whether the ARZ multi-lineage readout
(arz_readout/neural_readout, M35-A) carries the anterior-restricted role
the canon read lacks, on the chain planes"). H-P2's graph-level refutation
(exp128/HP2-G1, L112) handed its FAIL note to M35: the M35 wound-domain
mapping inherits the gate. THIS experiment runs that inherited gate.

BACKGROUND CHAIN: exp86 measured the chain inverse pair (no-M33 head
0.70 / M33 head 0.00, coin off — the read-side anterior fragility) and
exp128 refuted the graph-level anterior-restricted phenocopy for the
CANON read (the stripped arm IMPROVES both zones: the canon read is a
gap-fidelity/zone-drag trade-off, not an anterior necessity), handing
the gate to M35. exp126 (L107) fixed the coin vocabulary this batch
inherits (None = the coin MECHANISM ABSENT = the exp86 coin-off default
inheritance path; the saturated rung 0.8 is the record-matched NB_P).

=======================================================================
STEP 1 — THE MACHINERY, STATED EXACTLY (read before any arm was run)
=======================================================================
Both readouts live ONLY inside the M25 blind-guess branch of the chain
regen walk (BioElectricCollective.regrow -> walk; collective.py L557-603).
The walk commits cells one at a time outward from the wound face; each
commit is theta_new = chain_base + N(0, eff_noise) + wander (chain_base =
the last committed cell's theta, optionally spec-blended). When
r = gap_scale < 1.0 (junction blockade) the M25 fallback replaces the
commit with guess = wound_center + draw and theta_new = r*theta_new +
(1-r)*guess, where wound_center = mean(theta[wound region]) — after
exp60's amputate this is the blastema_theta flat -40.0 — and
draw ~ N(0, blastema_readout_noise) (spread 18.0 mV: a blind cell can
land anywhere on the head-trunk fate axis). At r >= 1.0 the whole guess
branch is SKIPPED (zero RNG contact): both readouts are structurally
inert at full coupling.

ARZ_READOUT (M35-A, collective.py L557-578 + constants L47-52):
arz_readout = w in (0,1] blends the SINGLE guess draw with the mean of
ARZ_LINEAGES = 3 independent N(0, blastema_readout_noise) draws — the
epidermal/neural/muscle lineage reads (K from the published lineage
count, MED42172041, not fitted): draw <- (1-w)*draw + w*mean(3 draws).
The content is pure VARIANCE REDUCTION of the blind guess (at w=1.0 the
sd falls 18.0 -> 18/sqrt(3) ~= 10.39 mV); the guess CENTER is untouched
(the first-registered base blend toward wound_center was found redundant
— the M35 redundancy discovery, L558-563). It fires at EVERY committing
cell under blockade regardless of position or identity — the
wound-proximal domain, wound-domain-wide BY CONSTRUCTION.
arz_readout = 0.0 consumes no RNG draws (bit-exact, single-draw stream
unchanged — L568). ARZ_WIDTH = 2 is the registered wound-domain width
constant (L52, regrow kwarg default L202) but is NOT consumed in the
deposited walk body: the width is realized by the wound region slice
itself (the amputated segment defines the guess base). exp133 carries
it at its deposited default verbatim; it is not a free knob here.

NEURAL_READOUT (M33, collective.py L579-595): fires inside the same
guess branch AFTER the arz blend: if neural_readout = w > 0 AND phi_spec
exists AND the committing cell's spec identity is ANTERIOR
(spec[i] >= NEURAL_SPEC_MIN = -35 mV), the guess is blended with a
direct NON-JUNCTIONAL spec read:
guess <- (1-w)*guess + w*(spec[i] + N(0, eff_noise)),
eff_noise = noise * commitment_noise_scale. Posterior identities do NOT
qualify, and the pole draw is consumed only when the branch fires — so
on WT spec (phi_spec = wildtype_target: -20 for cells 0..24, -50 beyond)
the tail/trunk trajectories are BIT-IDENTICAL with the read off (the
draw never fires below the line; a construction-level certainty,
pre-registered as such in WD-G2). exp86 verified the pole read's
anterior role at full coupling (head 0.70 -> 0.00) and at gap 0.2
(Panel B: no_read 1.0 -> blend_plus_pole 0.0 with the phi blend + pole
read — the deposit attributes the repair to the guess-path pole read,
the phi blend being (1-r)-diluted).

PLANE TAXONOMY (the exp66 mis-map domain): exp66/SG-G1 corrected the
corpus plane map (e421 "head plus PRE-pharyngeal crop" is ONE contiguous
anterior removal -> head-plane semantics; only POST-pharyngeal is
two-ended) and exp128's construction note showed the mis-map axis has
zero bite without an actual mis-map. exp133 therefore runs on the
CORRECTED taxonomy only (regrow60 verbatim: head = anterior removal,
backward walk; tail = posterior removal, forward; trunk = mid-body,
direction="both"). No mis-map arm is registered.

=======================================================================
PRE-REGISTRATION (fixed BEFORE any run; thresholds never tuned after)
=======================================================================
OPERATING POINT: run_arm86 VERBATIM (exp86's arm; exp128's chain
re-anchor instrument), protocol="neoblast", coin off (coin_p=None =
the coin mechanism absent, L107's vocabulary), gap_scale=0.2 — exp86
Panel B's deposited damaged-junction operating point, the only
deposited point where the M25 guess path (and hence BOTH channels) is
active. Planes {head, tail, trunk} x 12 FRESH seeds 11..22 (the exp86
FRESH_SEEDS convention starting at 11).

ARMS (the minimal 2x2 — read_kw extras on run_arm86):
  A blind   {}                                (arz off, neural off)
  B arz     {"arz_readout": 1.0}              (the M35-A readout alone)
  C neural  {"neural_readout": 0.75}          (the M33 pole read alone;
            0.75 = exp86 Panel B's deposited weight)
  D comp    {"arz_readout": 1.0, "neural_readout": 0.75}  (recomposed)
arz weight 1.0 because the M35-A registration IS the K=3 convergence
(the full lineage-averaged guess); no registered dose axis exists.

ANCHORS:
  WD-A1 (blocking) exp86's deposited inverse pair — results/
      exp86_regen_read.json baseline_coin_off.head = 0.70 /
      m33_read_coin_off.head = 0.00 — reproduces within +/-0.1 at
      seeds 1..10, head plane, full coupling (exp128's chain re-anchor
      convention, which re-landed 0.70/0.00 in L112). FAIL -> batch
      void, no gate may be read.
  WD-A2 (instrument identities, bit-exact, non-statistical)
      (i) arz_readout=0.0 stream-neutrality: arm A vs
          {"arz_readout": 0.0} bit-identical per seed on all three
          planes at gap 0.2 AND gap 1.0 (the L568 claim);
      (ii) full-coupling inertness: arm B vs arm A bit-identical per
          seed at gap 1.0 (the guess branch is skipped at r >= 1.0).
      FAIL on any pair -> harness defect, batch void.

GATES (two-sided; third outcomes named; bars fixed from the n=12
binomial scale BEFORE any run: 0.25 = 3/12 seeds >= 1.7 x
SE(0.5/sqrt(12)) = 1.7 x 0.144, materially above binomial noise; 0.10 =
the sub-noise floor, matching exp86's +/-0.10/0.15 and exp128's +/-0.1
conventions):
  WD-G1 (THE INHERITED M35 GATE — core) the ARZ contrast
      S_p = rate(B,p) - rate(A,p), p in {head, tail, trunk}.
      CONFIRM  anterior-restricted: |S_head| >= 0.25 AND
               |S_head| >= 2 * max(|S_tail|, |S_trunk|).
      REFUTE   wound-domain-general (the exp128-inherited outcome):
               min(|S_tail|, |S_trunk|) >= 0.10 AND
               max(|S_tail|, |S_trunk|) >= 0.5 * |S_head|.
      THIRD    named "RATE-INERT" if max_p |S_p| < 0.10 (the guess
               CENTER, not its spread, decides these rates — the
               variance reduction never crosses the 6 mV bar); else
               "PARTIAL" (shifts present, neither branch fires).
      Signs deposited descriptively: variance reduction predicts
      S <= 0 (fewer threshold crossings); a shift with positive sign
      >= 0.25 is deposited with the sign paradox flagged, not hidden.
  WD-G2 (the pole-read reference — the M33 chain analog at r < 1)
      T_p = rate(C,p) - rate(A,p).
      CONFIRM: |T_head| >= 0.25 AND T_tail = T_trunk = 0 bit-exactly
               (construction: the spec-gated draw never fires on WT
               below-line spec).
      REFUTE:  any posterior T_p != 0 (gating leak — instrumentation
               event) OR |T_head| < 0.10 (the pole repair fails off
               the deposited seed band).
      THIRD    named "PARTIAL-REPAIR": posterior pair bit-zero but
               0.10 <= |T_head| < 0.25.
  WD-G3 (composition invariance) U_p = rate(D,p) - rate(C,p),
      classified by WD-G1's rules. Outcome "INVARIANT" (same class as
      WD-G1) vs "CONTEXT-DEPENDENT" (class flip). Pre-stated
      interpretation: WD-G1 RATE-INERT + WD-G3 ANTERIOR-RESTRICTED =
      "the ARZ averaging's rate content is visible only once the pole
      read re-centers the guess — wound-domain variance reduction,
      anterior-expressed effect" (a wound-domain-general mechanism
      wearing an anterior readout mask).

READING MAP (pre-registered):
  WD-G1 CONFIRM -> the M35-A ARZ readout carries an anterior-restricted
      regulatory role the canon read lacks on graph substrates — the
      M35 wound-domain mapping survives its inherited gate.
  WD-G1 REFUTE -> the ARZ readout is wound-domain-general like the
      canon read — the exp128-inherited outcome fires at the chain
      level; M35-A's regulatory content is NOT anterior-restricted.
  WD-G1 RATE-INERT/PARTIAL -> the discrimination is carried to WD-G3's
      composition column; the measured profile is deposited as owned.

RUN: ~308 chain runs (main grid 4x3x12 + anchors), serial, BLAS
pinned. Runtime: seconds.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp86_regen_read import run_arm86, M33_KW  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp133_wound_domain_readout.json")

PLANES = ("head", "tail", "trunk")
SEEDS12 = tuple(range(11, 23))          # 12 fresh seeds, exp86 convention
GAP = 0.2                               # exp86 Panel B operating point
NEURAL_W = 0.75                         # exp86 Panel B's deposited weight

# thresholds — fixed BEFORE any run (see pre-registration above)
BAR_CONFIRM = 0.25
BAR_FLOOR = 0.10
ANCHOR_TOL = 0.1

ARMS = {
    "A_blind": {},
    "B_arz": {"arz_readout": 1.0},
    "C_neural": {"neural_readout": NEURAL_W},
    "D_comp": {"arz_readout": 1.0, "neural_readout": NEURAL_W},
}


def run_grid(arms: dict, planes, seeds, gap: float) -> dict:
    """run_arm86 verbatim; per-seed binary outcomes + pooled rate."""
    grid = {}
    for name, kw in arms.items():
        rows = {}
        for plane in planes:
            outs = [run_arm86(plane, s, None, read_kw=kw or None,
                              gap_scale=gap) for s in seeds]
            rows[plane] = {"seeds": list(seeds), "outcomes": outs,
                           "rate": round(float(np.mean(outs)), 4)}
        grid[name] = rows
    return grid


def classify(shifts: dict) -> str:
    """WD-G1's pre-registered three-way classification (shared with
    WD-G3). shifts: plane -> signed rate shift."""
    h = abs(shifts["head"])
    t = abs(shifts["tail"])
    k = abs(shifts["trunk"])
    m, M = min(t, k), max(t, k)
    if h >= BAR_CONFIRM and h >= 2.0 * M:
        return "ANTERIOR-RESTRICTED"
    if m >= BAR_FLOOR and M >= 0.5 * h:
        return "WOUND-DOMAIN-GENERAL"
    if max(h, t, k) < BAR_FLOOR:
        return "RATE-INERT"
    return "PARTIAL"


def main() -> dict:
    print("=== exp133: the wound-domain readout test (M35 inherited gate) ===\n")
    t0 = time.time()
    result: dict = {"exp": "exp133_wound_domain_readout"}

    # ---- WD-A1: the exp86 inverse pair (blocking anchor) -------------------
    base = [run_arm86("head", s, None) for s in range(1, 11)]
    m33 = [run_arm86("head", s, None, read_kw=M33_KW) for s in range(1, 11)]
    rb, rm = float(np.mean(base)), float(np.mean(m33))
    a1_ok = abs(rb - 0.70) <= ANCHOR_TOL and abs(rm - 0.00) <= ANCHOR_TOL
    result["wd_a1_anchor"] = {
        "no_m33_head": round(rb, 3), "m33_head": round(rm, 3),
        "deposited": {"no_m33": 0.7, "m33": 0.0},
        "source": "results/exp86_regen_read.json (re-landed in exp128, L112)",
        "pass": bool(a1_ok),
    }
    print(f"  WD-A1 anchor: no-M33 {rb:.2f} (want 0.70) | "
          f"M33 {rm:.2f} (want 0.00) -> "
          f"{'MATCH' if a1_ok else 'DRIFT — BATCH VOID'}", flush=True)

    # ---- WD-A2: instrument identities (bit-exact, void batch on fail) ------
    probes = run_grid({"A_blind": {}, "A_zero": {"arz_readout": 0.0},
                       "B_arz": ARMS["B_arz"]}, PLANES, SEEDS12, gap=1.0)
    neutral_gap1 = all(
        probes["A_blind"][p]["outcomes"] == probes["A_zero"][p]["outcomes"]
        for p in PLANES)
    inert_gap1 = all(
        probes["A_blind"][p]["outcomes"] == probes["B_arz"][p]["outcomes"]
        for p in PLANES)
    probes02 = run_grid({"A_blind": {}, "A_zero": {"arz_readout": 0.0}},
                        PLANES, SEEDS12, gap=GAP)
    neutral_gap02 = all(
        probes02["A_blind"][p]["outcomes"] == probes02["A_zero"][p]["outcomes"]
        for p in PLANES)
    a2_ok = neutral_gap1 and inert_gap1 and neutral_gap02
    result["wd_a2_identities"] = {
        "arz0_stream_neutral_gap1.0": bool(neutral_gap1),
        "arz_inert_full_coupling_gap1.0": bool(inert_gap1),
        "arz0_stream_neutral_gap0.2": bool(neutral_gap02),
        "pass": bool(a2_ok),
    }
    print(f"  WD-A2 identities: neutral@r1 {neutral_gap1} | "
          f"inert@r1 {inert_gap1} | neutral@r0.2 {neutral_gap02} -> "
          f"{'PASS' if a2_ok else 'HARNESS DEFECT — BATCH VOID'}", flush=True)

    if not (a1_ok and a2_ok):
        result["criteria"] = {"batch": "VOID — anchor failure"}
        with open(OUT, "w") as f:
            json.dump(result, f, indent=1, default=float)
        print(f"\n  results -> {OUT}")
        return result

    # ---- main grid: the 2x2 at the damaged-junction operating point --------
    print(f"\n  main grid (4 arms x 3 planes x {len(SEEDS12)} seeds, "
          f"gap_scale={GAP}, coin off):", flush=True)
    grid = run_grid(ARMS, PLANES, SEEDS12, gap=GAP)
    for name in ARMS:
        prof = {p: grid[name][p]["rate"] for p in PLANES}
        print(f"    {name:9s} {prof}", flush=True)
    result["grid"] = {n: {p: grid[n][p] for p in PLANES} for n in ARMS}

    # ---- WD-G1: the ARZ contrast (the inherited M35 gate) -------------------
    S = {p: round(grid["B_arz"][p]["rate"] - grid["A_blind"][p]["rate"], 4)
         for p in PLANES}
    g1_class = classify(S)
    result["wd_g1_arz_contrast"] = {
        "shifts": S, "class": g1_class,
        "rule": ("CONFIRM anterior-restricted: |S_head|>=0.25 and "
                 "|S_head|>=2*max(|S_tail|,|S_trunk|); REFUTE wound-domain-"
                 "general: min(|S_tail|,|S_trunk|)>=0.10 and "
                 "max>=0.5*|S_head|; third: RATE-INERT if max<0.10 else "
                 "PARTIAL"),
    }
    print(f"\n  WD-G1 ARZ shifts {S} -> {g1_class}", flush=True)

    # ---- WD-G2: the pole-read reference ------------------------------------
    T = {p: round(grid["C_neural"][p]["rate"] - grid["A_blind"][p]["rate"], 4)
         for p in PLANES}
    post_zero = (grid["C_neural"]["tail"]["outcomes"]
                 == grid["A_blind"]["tail"]["outcomes"]) and \
                (grid["C_neural"]["trunk"]["outcomes"]
                 == grid["A_blind"]["trunk"]["outcomes"])
    if not post_zero or abs(T["head"]) < BAR_FLOOR:
        g2 = "REFUTE"
        g2_why = ("gating leak (posterior T != 0)" if not post_zero else
                  f"pole repair fails off the deposited band (|T_head| "
                  f"{abs(T['head']):.2f} < {BAR_FLOOR})")
    elif abs(T["head"]) >= BAR_CONFIRM:
        g2 = "CONFIRM"
        g2_why = (f"|T_head| {abs(T['head']):.2f} >= {BAR_CONFIRM} with the "
                  f"posterior pair bit-zero (construction verified)")
    else:
        g2 = "PARTIAL-REPAIR"
        g2_why = (f"posterior pair bit-zero but |T_head| "
                  f"{abs(T['head']):.2f} in [{BAR_FLOOR}, {BAR_CONFIRM})")
    result["wd_g2_pole_reference"] = {
        "shifts": T, "posterior_pair_bit_zero": bool(post_zero),
        "outcome": g2, "why": g2_why,
    }
    print(f"  WD-G2 pole shifts {T} (posterior bit-zero: {post_zero}) "
          f"-> {g2}: {g2_why}", flush=True)

    # ---- WD-G3: composition invariance --------------------------------------
    U = {p: round(grid["D_comp"][p]["rate"] - grid["C_neural"][p]["rate"], 4)
         for p in PLANES}
    g3_class = classify(U)
    g3 = "INVARIANT" if g3_class == g1_class else "CONTEXT-DEPENDENT"
    result["wd_g3_composition"] = {
        "shifts": U, "class": g3_class, "outcome": g3,
        "g1_class": g1_class,
        "pre_stated_reading": (
            "WD-G1 RATE-INERT + WD-G3 ANTERIOR-RESTRICTED = the ARZ "
            "averaging's rate content is visible only once the pole read "
            "re-centers the guess — wound-domain variance reduction, "
            "anterior-expressed effect"),
    }
    print(f"  WD-G3 composition shifts {U} -> {g3_class} "
          f"({g3} vs WD-G1 {g1_class})", flush=True)

    # ---- gates summary -------------------------------------------------------
    criteria = {
        "WD_A1_anchor_inverse_pair": bool(a1_ok),
        "WD_A2_instrument_identities": bool(a2_ok),
        "WD_G1_arz_domain_gate": g1_class,       # the class IS the outcome
        "WD_G2_pole_reference": g2,
        "WD_G3_composition_invariance": g3,
    }
    result["criteria"] = criteria
    result["notes"] = (
        "The M35 inherited gate (L112): the ARZ multi-lineage wound-domain "
        "readout (arz_readout, K=3 lineage draws averaged, ARZ_WIDTH=2 "
        "carried unused — width realized by the wound slice) vs the M33 "
        "pole read (neural_readout) on the chain planes at exp86 Panel B's "
        "damaged-junction operating point (gap 0.2, coin off, seeds "
        "11..22). run_arm86 verbatim; arz weight 1.0 = the registered K=3 "
        "convergence; neural weight 0.75 = the deposited Panel B weight. "
        "Thresholds fixed pre-run from the n=12 binomial scale; never "
        "tuned after seeing data.")
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    n_hard = sum(1 for v in criteria.values() if v is True)
    print(f"  === anchors {n_hard}/2 PASS | WD-G1 -> {g1_class} | "
          f"WD-G2 -> {g2} | WD-G3 -> {g3} "
          f"({time.time() - t0:.0f}s) ===")
    return result


if __name__ == "__main__":
    main()
