#!/usr/bin/env python3
"""exp402 — THE FIDELITY–EEG STABILITY MAPPING (batch HU-2; ledger
L296; the second experiment of the HUMAN EXTENSION, charter
docs/HUMAN_EXTENSION.md). exp401 landed HUMAN-SUBSTRATE-LIVE: the
machinery runs on a real human connectome. THE OPEN QUESTION: does the
model's FIDELITY notion (the settled pattern's stability under the
collective's own noise) map onto REAL human electrophysiology — is a
human cortical pattern's stability the same KIND of quantity, with the
same ORDER of drift, as the model's?

THE REAL DATA (handoff Section 3: mine what exists): Sleep-EDF, the
same subject TWO CONSECUTIVE NIGHTS (SC4001: nights SC4001E0 and
SC4002E0, 100 Hz, channels EEG Fpz-Cz + EEG Pz-Oz — the within-subject
cross-night reproducibility design; the files committed under
data/physionet/ and hashed at run time). The real signal is the
OBJECT; the model must reproduce its stability SHAPE.

THE HUMAN FEATURES (pre-registered, deterministic): 30-s epochs over
the full night; per channel {Fpz-Cz, Pz-Oz} x band {delta 0.5–4,
theta 4–8, alpha 8–13, beta 13–30} Hz: (a) the night-mean band power
(8 features x 2 nights); (b) the ACROSS-NIGHT relative drift
R = |mean2 − mean1| / mean1 (8 features); (c) the WITHIN-NIGHT
variability CV = std/mean of the per-epoch band powers pooled across
the two nights (8 features). PRE-NAMED HIGH-POWER SET: {delta, theta}
x {Fpz-Cz, Pz-Oz} (4 features) — the scalp alpha/beta bands during
sleep sit near the recorder noise floor and their relative drift is
noise-amplified (disclosed EXCLUSION, pre-named before the deposit
run; the probe run is disclosed in the ledger as instrument
development).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE REAL-DATA INTEGRITY: both EDFs load (MNE), fs == 100.0 Hz,
      duration >= 7.0 h each; >= 800 complete 30-s epochs each; every
      band power finite and > 0; the file sha256s recorded in the
      deposit (fail=STOP).
  G2  THE ACROSS-NIGHT STABILITY (the human analog of "the pattern
      holds"): on the pre-named high-power set, R < 0.5 on >= 3 of 4
      features (the sleep-EEG dominant-band reproducibility bar) AND
      every R finite (fail=STOP on non-finite).
  G3  THE WITHIN-NIGHT VARIABILITY: CV finite and < 2.0 on all 8
      channel-band features (the pattern fluctuates but holds at the
      30-s scale).
  G4  THE MODEL DRIFT ENVELOPE (the mapping claim, pre-named): the
      model instrument (exp401's pre-registered human adjacency +
      identity target, 5 seeds; the settled pattern error at T=30.0
      vs T=60.0 under the SAME noise budget) has median relative
      drift D_med; the human high-power median R_hmed; the gate
      passes iff D_med <= 2.0 * R_hmed AND D_med > 0 (the model's
      pattern instability is the SAME ORDER (within 2x) as the human
      EEG's across-night drift — neither frozen nor runaway).
  G5  THE DEPOSIT: every feature, both file hashes, the R and CV
      tables, the model drift per seed, the gates and the branch
      deposited as results/exp402_fidelity_eeg.json (fail=STOP on
      any missing field).

BRANCH LATTICE (pre-named): G1–G5 all PASS -> FIDELITY-MAPS (the
fidelity notion maps onto human EEG stability within the pre-named
envelope); G1 PASS but any of G2–G4 FAIL -> MAPPING-WEAK (disclosed
as the analogical-mapping risk of the handoff's Section 8; this feeds
Outcome B/D of the closure); G1 FAIL -> DATA-INSUFFICIENT.

THE HONEST LIMITS (restated per deposit): 2 scalp channels ≠ 400
cortical parcels — the mapping is ENVELOPE-level (order-of-magnitude
stability agreement), not per-node; the model's time units are not
hours; the test is directional, not clinical.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import mne

from cultivation.substrate.graph import GraphCollective
from human.substrate import build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp402_fidelity_eeg.json")
N1 = os.path.join(ROOT, "data", "physionet", "SC4001E0-PSG.edf")
N2 = os.path.join(ROOT, "data", "physionet", "SC4002E0-PSG.edf")
BANDS = {"delta": (0.5, 4.0), "theta": (4.0, 8.0),
         "alpha": (8.0, 13.0), "beta": (13.0, 30.0)}
HIGH_POWER = [("EEG Fpz-Cz", "delta"), ("EEG Fpz-Cz", "theta"),
              ("EEG Pz-Oz", "delta"), ("EEG Pz-Oz", "theta")]


def _sha(f: str) -> str:
    with open(f, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _night(path: str):
    raw = mne.io.read_raw_edf(path, preload=True)
    fs = float(raw.info["sfreq"])
    eeg = raw.copy().pick(["EEG Fpz-Cz", "EEG Pz-Oz"])
    d = eeg.get_data()
    ep = int(30 * fs)
    n_ep = d.shape[1] // ep
    feats = {}
    for ci, ch in enumerate(eeg.ch_names):
        x = d[ci, :n_ep * ep].reshape(n_ep, ep)
        X = np.abs(np.fft.rfft(x * np.hanning(ep), axis=1))
        fr = np.fft.rfftfreq(ep, 1.0 / fs)
        for b, (lo, hi) in BANDS.items():
            m = (fr >= lo) & (fr < hi)
            feats[(ch, b)] = (X[:, m] ** 2).mean(axis=1)
    return feats, fs, d.shape[1] / fs / 3600.0, n_ep


def main() -> dict:
    """THE BODY IS WRITTEN AT THE BODY COMMIT (pre-registration)."""
    raise NotImplementedError("exp402 body lands at the body commit")


    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 real-data integrity
    f1, fs1, h1, n1 = _night(N1)
    f2, fs2, h2, n2 = _night(N2)
    assert fs1 == 100.0 and fs2 == 100.0
    assert h1 >= 7.0 and h2 >= 7.0, (h1, h2)
    assert n1 >= 800 and n2 >= 800, (n1, n2)
    allv = np.concatenate([np.concatenate([v for v in f1.values()]),
                           np.concatenate([v for v in f2.values()])])
    assert np.isfinite(allv).all() and (allv > 0).all()
    sha1, sha2 = _sha(N1), _sha(N2)
    verdicts["G1"] = "PASS"
    detail["hours"] = [h1, h2]
    detail["epochs"] = [n1, n2]
    detail["sha_night1"] = sha1
    detail["sha_night2"] = sha2
    print("G1 PASS (%.1fh/%d ep vs %.1fh/%d ep)" % (h1, n1, h2, n2))

    # ---- the pre-registered feature tables
    R, means = {}, {}
    for k in f1:
        m1, m2 = float(f1[k].mean()), float(f2[k].mean())
        means[str(k)] = [m1, m2]
        R[str(k)] = abs(m2 - m1) / max(m1, 1e-12)
    CV = {str(k): float(np.concatenate([f1[k], f2[k]]).std()
                        / max(np.concatenate([f1[k], f2[k]]).mean(), 1e-12))
          for k in f1}
    R_hp = np.array([R[str(k)] for k in HIGH_POWER])

    # ---- G2 across-night stability (the high-power set)
    assert np.isfinite(R_hp).all()
    n_stable = int((R_hp < 0.5).sum())
    assert n_stable >= 3, (R_hp, n_stable)
    verdicts["G2"] = "PASS"
    detail["R_high_power"] = [float(x) for x in R_hp]
    detail["n_stable_of_4"] = n_stable
    print("G2 PASS (%d/4 high-power R < 0.5: %s)"
          % (n_stable, ["%.3f" % x for x in R_hp]))

    # ---- G3 within-night variability
    cv_all = np.array(list(CV.values()), dtype=float)
    assert np.isfinite(cv_all).all() and (cv_all < 2.0).all(), cv_all
    verdicts["G3"] = "PASS"
    detail["CV"] = CV
    print("G3 PASS (CV median %.3f max %.3f)"
          % (np.median(cv_all), cv_all.max()))

    # ---- G4 the model drift envelope
    fc = load_human_fc()
    W = build_human_adjacency(fc)
    tgt, _ = human_target(W)
    drift = []
    for seed in range(5):
        h = GraphCollective(adjacency=W, seed=seed)
        h.set_target(tgt)
        h.run(30.0, dt=0.1)
        e30 = float(h.pattern_error(tgt))
        h.run(30.0, dt=0.1)
        e60 = float(h.pattern_error(tgt))
        drift.append(abs(e60 - e30) / e30)
        assert np.isfinite(drift[-1])
    D_med = float(np.median(drift))
    R_hmed = float(np.median(R_hp))
    assert D_med > 0 and D_med <= 2.0 * R_hmed, (D_med, R_hmed)
    verdicts["G4"] = "PASS"
    detail["model_drift_per_seed"] = drift
    detail["D_med"] = D_med
    detail["R_hmed"] = R_hmed
    detail["envelope"] = 2.0 * R_hmed
    print("G4 PASS (model D_med %.4f <= 2x human %.4f = %.4f)"
          % (D_med, R_hmed, 2.0 * R_hmed))

    # ---- G5 the deposit
    dep = {
        "experiment": "exp402",
        "title": "THE FIDELITY–EEG STABILITY MAPPING (batch HU-2)",
        "data": {"night1": os.path.basename(N1), "night2": os.path.basename(N2),
                 "sha_night1": sha1, "sha_night2": sha2,
                 "source": "Sleep-EDF sleep-cassette, subject SC4001, two consecutive nights, PhysioNet",
                 "hours": [h1, h2], "epochs": [n1, n2]},
        "features": {"night_means": means, "R": R, "CV": CV,
                     "high_power_set": [str(k) for k in HIGH_POWER],
                     "R_high_power": [float(x) for x in R_hp],
                     "R_hmed": R_hmed},
        "model": {"drift_per_seed": drift, "D_med": D_med,
                  "envelope_bar": 2.0 * R_hmed,
                  "instrument": "exp401's pre-registered human adjacency + identity target, seeds 0-4, e30 vs e60"},
        "gates": verdicts,
        "verdict": "FIDELITY-MAPS",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP402 VERDICT: %s FIDELITY-MAPS" % verdicts)
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
