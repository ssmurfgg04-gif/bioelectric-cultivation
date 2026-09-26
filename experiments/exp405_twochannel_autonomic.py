#!/usr/bin/env python3
"""exp405 — THE TWO-CHANNEL LAW ↔ THE AUTONOMIC SUBSTRATE (batch HU-5;
ledger L299; charter docs/HUMAN_EXTENSION.md). exp404 landed
COMPOSITION-CLASS-MATCH. THE OPEN QUESTION (handoff Section 7): does
the TWO-CHANNEL LAW — the model's claim that an intervention's effect
is gated by (i) the VOLTAGE STATE (the V-ratio: the depolarization
gate) and (ii) the θ-HOMOGENEIZATION (the pattern-field coupling) —
transfer to human data, in (a) the real autonomic substrate (HRV's
two-branch balance: the sympathovagal ratio LF/HF, day vs night) and
(b) the literature's responder-fraction band (tDCS individual-difference
studies: the responder fraction ~0.40–0.60 at standard settings, and
the response is baseline-state dependent)?

THE REAL DATA: NSRDB record 16420 (PhysioNet; 24 h Holter ECG, 128 Hz,
2 channels, ~102k annotated beats; committed under data/physionet/).
THE REAL FEATURES (pre-registered, deterministic): the RR intervals
from the beat annotations (kept in [0.3, 2.0] s); per 1-h segment with
>= 300 kept beats: the RR series resampled to a 4 Hz grid, the Welch
PSD (nperseg 1024), LF = 0.04–0.15 Hz, HF = 0.15–0.40 Hz, LF/HF; DAY =
the median over 8:00–20:00, NIGHT = the median over 23:00–06:00.
THE LITERATURE ANCHOR (encoded, disclosed as a band not a point): the
tDCS responder fraction ~[0.40, 0.60] at standard settings, and the
response is baseline-state dependent (the responder-variability
reviews; the state-dependency of stimulation effects).

THE MODEL INSTRUMENT (the collective's own two-channel machinery, on
the human graph, self-contained): the settled human program (30 tu);
the intervention = a depolarizing theta driver (target −25.0 mV, rate
0.5, ALL 400 nodes — the collective's voltage-gated driver form: the
pull is ACTIVE only where V > vgate, the FIRST channel); 20 tu; the
response magnitude = |Δtheta| per node; a responder = |Δtheta| > 2.0
mV (the pre-named threshold). THE VGATE LADDER (pre-named):
[−45, −40, −35, −30]. THE SECOND CHANNEL: the neighborhood θ
homogeneity — per node the theta std over its closed neighborhood
(self + the top-6 neighbors); the prediction: the response magnitude
rises with homogeneity (the pattern-field coupling carries the
response — the rank correlation with −local_std is positive).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE REAL-ECG INTEGRITY: the record loads, fs == 128.0, duration
      >= 23.5 h; the annotations parse; >= 80,000 beats; the RR keep
      fraction >= 0.95 (fail=STOP).
  G2  THE REAL AUTONOMIC TWO-CHANNEL SHIFT: LF/HF DAY > LF/HF NIGHT
      (the canonical sympathovagal day-night direction, on the REAL
      record) and both medians finite and > 0 (fail=STOP).
  G3  THE MODEL'S FIRST-CHANNEL DIRECTION: the responder fraction over
      the vgate ladder is MONOTONE NON-INCREASING (raising the
      depolarization gate shrinks the responder pool — the voltage
      state gates the intervention; the direction the literature's
      baseline-state dependency claims).
  G4  THE RESPONDER-RANGE MATCH (the gate): there EXISTS a vgate on
      the pre-named ladder with the responder fraction inside the
      literature band [0.40, 0.60].
  G5  THE MODEL'S SECOND-CHANNEL DIRECTION: at vgate = −35.0, the
      Spearman rank correlation between the response magnitude and
      (−local theta std) is > 0 (the homogenization channel carries
      the response).
  G6  THE DEPOSIT: the LF/HF table, the responder sweep, the
      correlation, the gates and the branch deposited as
      results/exp405_twochannel_autonomic.json (fail=STOP).

BRANCH LATTICE (pre-named): G1–G6 all PASS -> TWO-CHANNEL-MAPS (the
two-channel law transfers in direction and range to the human
autonomic + responder data); G1/G2 PASS but any of G3–G5 FAIL ->
TWO-CHANNEL-WEAK (disclosed; Outcome B/D territory); G1/G2 FAIL ->
DATA-INSUFFICIENT.

THE HONEST LIMITS (in the deposit): LF/HF is a PROXY of the two-branch
autonomic balance (the literature debates its purity); the model's
"nodes" are cortical parcels, not ganglia; the responder band is a
literature convention, not a constant of nature; the map is
directional, not clinical.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.signal import welch
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cultivation.substrate.graph import GraphCollective
from human.substrate import build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp405_twochannel_autonomic.json")
ECG = os.path.join(ROOT, "data", "physionet", "16420")
VGATES = [-45, -40, -35, -30]
DRIVER_TARGET = -25.0
DRIVER_RATE = 0.5
DRIVER_TU = 20.0
RESP_THR = 2.0
LIT_BAND = (0.40, 0.60)


def _hrv_segments():
    import wfdb
    rec = wfdb.rdrecord(ECG)
    fs = float(rec.fs)
    ann = wfdb.rdann(ECG, "atr")
    beats = ann.sample[np.isin(ann.symbol, list("NLRAaJSVrFej"))]
    rr_all = np.diff(beats) / fs
    keep = (rr_all >= 0.3) & (rr_all <= 2.0)
    rr = rr_all[keep]
    tb = beats[1:][keep] / fs
    return fs, beats, rr, tb


def _lf_hf(tb, rr, t0, t1):
    m = (tb >= t0) & (tb < t1)
    if m.sum() < 300:
        return None
    grid = np.arange(t0, t1, 0.25)
    xi = np.interp(grid, tb[m], rr[m])
    xi -= xi.mean()
    f, P = welch(xi, fs=4.0, nperseg=1024)
    lf = P[(f >= 0.04) & (f < 0.15)].sum()
    hf = P[(f >= 0.15) & (f < 0.4)].sum()
    return lf / hf if hf > 0 else None


def main() -> dict:
    """THE BODY IS WRITTEN AT THE BODY COMMIT (pre-registration)."""
    raise NotImplementedError("exp405 body lands at the body commit")


    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 the real-ECG integrity
    fs, beats, rr, tb = _hrv_segments()
    dur_h = float(tb.max() - tb.min()) / 3600.0
    assert fs == 128.0, fs
    assert dur_h >= 23.5, dur_h
    assert len(beats) >= 80_000, len(beats)
    keep_frac = len(rr) / max(len(np.diff(beats)), 1)
    assert keep_frac >= 0.95, keep_frac
    verdicts["G1"] = "PASS"
    detail["ecg"] = {"fs": fs, "dur_h": dur_h, "n_beats": int(len(beats)),
                     "rr_keep_frac": float(keep_frac),
                     "source": "NSRDB record 16420, PhysioNet (24 h Holter)"}
    print("G1 PASS (%.1f h, %d beats, keep %.3f)" % (dur_h, len(beats), keep_frac))

    # ---- G2 the real autonomic two-channel shift
    day = [v for h0 in range(8, 20)
           if (v := _lf_hf(tb, rr, h0 * 3600, (h0 + 1) * 3600)) is not None]
    night = [v for h0 in [0, 1, 2, 3, 4, 5, 23]
             if (v := _lf_hf(tb, rr, h0 * 3600, (h0 + 1) * 3600)) is not None]
    day_med, night_med = float(np.median(day)), float(np.median(night))
    assert day_med > 0 and night_med > 0
    assert day_med > night_med, (day_med, night_med)
    verdicts["G2"] = "PASS"
    detail["lf_hf"] = {"day_median": day_med, "night_median": night_med,
                       "day_n": len(day), "night_n": len(night),
                       "day_values": day, "night_values": night}
    print("G2 PASS (LF/HF day %.3f > night %.3f)" % (day_med, night_med))

    # ---- G3/G4 the model's two-channel faces
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    tgt, _ = human_target(W)
    A = (W > 0).astype(float)
    An = A + np.eye(W.shape[0])
    nbr_lists = [np.where(An[i] > 0)[0] for i in range(W.shape[0])]
    sweep = {}
    mags_at = {}
    for vg in VGATES:
        h = GraphCollective(adjacency=W, seed=0)
        h.set_target(tgt)
        h.run(30.0, dt=0.1)
        th0 = h.theta.copy()
        h.theta_drivers.append((np.arange(W.shape[0]), DRIVER_TARGET,
                                DRIVER_RATE, float(vg)))
        h.run(DRIVER_TU, dt=0.1)
        mag = np.abs(h.theta - th0)
        mags_at[vg] = mag
        sweep[vg] = float((mag > RESP_THR).mean())
    vals = [sweep[v] for v in VGATES]
    assert all(vals[i] >= vals[i + 1] - 1e-12 for i in range(len(vals) - 1)), vals
    verdicts["G3"] = "PASS"
    detail["responder_sweep"] = {str(k): v for k, v in sweep.items()}
    print("G3 PASS (sweep %s monotone non-increasing)"
          % ["%.3f" % v for v in vals])

    in_band = [vg for vg in VGATES if LIT_BAND[0] <= sweep[vg] <= LIT_BAND[1]]
    assert in_band, sweep
    verdicts["G4"] = "PASS"
    detail["in_band_vgates"] = in_band
    detail["literature_band"] = list(LIT_BAND)
    detail["literature_source"] = ("the tDCS responder-variability reviews: "
                                   "the responder fraction ~0.40-0.60 at "
                                   "standard settings, baseline-state dependent")
    print("G4 PASS (vgates %s land inside the literature band [0.40, 0.60])"
          % in_band)

    # ---- G5 the second channel (the homogenization face)
    h = GraphCollective(adjacency=W, seed=0)
    h.set_target(tgt)
    h.run(30.0, dt=0.1)
    th0 = h.theta.copy()
    h.theta_drivers.append((np.arange(W.shape[0]), DRIVER_TARGET,
                            DRIVER_RATE, -35.0))
    h.run(DRIVER_TU, dt=0.1)
    mag = np.abs(h.theta - th0)
    mags_at[-35] = mag
    local_std = np.array([h.theta[nbr_lists[i]].std() for i in range(W.shape[0])])
    rho, p = spearmanr(-local_std, mag)
    assert rho > 0, (rho, p)
    verdicts["G5"] = "PASS"
    detail["spearman_rho_homog"] = float(rho)
    detail["spearman_p"] = float(p)
    print("G5 PASS (Spearman(mag, -local theta std) = %.3f, p %.2e)"
          % (rho, p))

    # ---- G6 the deposit
    dep = {
        "experiment": "exp405",
        "title": "THE TWO-CHANNEL LAW <-> THE AUTONOMIC SUBSTRATE (batch HU-5)",
        "real_data": detail["ecg"],
        "lf_hf": detail["lf_hf"],
        "model": {"vgate_ladder": VGATES,
                  "responder_sweep": detail["responder_sweep"],
                  "in_band_vgates": in_band,
                  "spearman_rho_homog": float(rho),
                  "driver": {"target": DRIVER_TARGET, "rate": DRIVER_RATE,
                             "tu": DRIVER_TU, "resp_thr": RESP_THR}},
        "literature_band": list(LIT_BAND),
        "gates": verdicts,
        "verdict": "TWO-CHANNEL-MAPS",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G6"] = "PASS"
    print("G6 PASS (deposit %s)" % DEPOSIT)

    print("EXP405 VERDICT: %s TWO-CHANNEL-MAPS" % verdicts)
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
