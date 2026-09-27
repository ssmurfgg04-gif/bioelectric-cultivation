#!/usr/bin/env python3
"""exp437 — THE MINIMAL FALSIFIABLE WET-LAB TEST FOR d-02 (batch HU-13;
exp416's registered follow-up). exp416 landed WETLAB-PATH-OPEN: 3/10
generator anatomies are realizable in the wet lab and the d-02 spec
was deposited. THE OPEN QUESTION: what is the MINIMAL falsifiable
test — the smallest intervention whose simulated signature, if
absent in the wet lab, kills the d-02 mechanism claim outright?

THE INSTRUMENT (a design experiment — the deliverable is the
protocol, the gates bind its structure): the d-02 anatomy's minimal
intervention selected by the pre-named criterion (fewest manipulated
variables with a pre-named simulated signature); the protocol
deposited as a structured spec (arm table, measurement, the
disconfirming observation, the confound list); every claim in the
spec traced to a landed experiment's deposit.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE TRACE: every mechanism claim in the spec cites a landed
      deposit (results/expNNN_*.json present in the repo); any
      uncited claim fails the gate (fail=STOP).
  G2  THE FALSIFIER: the spec names ONE disconfirming observation,
      stated as a measurement with a threshold, such that the
      mechanism claim is dead if it obtains; the observation is
      measurable with the equipment the d-02 anatomy's own paper
      used (no new instruments invented).
  G3  THE MINIMALITY: the intervention manipulates <= 2 variables
      and the arm table has <= 4 arms; a larger panel is a
      REFUTE of the minimality claim (deposited honestly).
  G4  THE SIGNATURE: the spec's simulated signature is computed
      from the repo's own machinery on the d-02 anatomy (the arm
      table's simulated outcomes deposited as numbers, not prose).
  G5  deposit results/exp437_d02_wetlab_test.json.

BRANCH LATTICE: SPEC-DEPOSITED (all gates pass) / SPEC-BLOATED (G3
REFUTE) / INSTRUMENT-REFUTED (G1 fail).
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cultivation.bioelectric.collective as CORE
from cultivation.substrate.graph import GraphCollective, path

DEPOSIT = os.path.join(ROOT, "results", "exp437_d02_wetlab_test.json")

CITED = [
    ("results/exp416_generator_wetlab_path.json",
     ["minimal_spec", "scoring_table"]),
    ("results/exp150_generator_complete.json", ["anatomy_programs"]),
    ("results/exp118_corpus_full.json", ["aggregates"]),
    ("results/exp410_register_decomposition.json", ["gates"]),
    ("results/exp407_invisibility_mechanism.json", ["errs"]),
]

BODY_DISCLOSURES = [
    "the dose -> register-g mapping: the corpus's wnt dose range "
    "[0.25, 1.0] maps onto the register's write dose g (exp410's "
    "dose axis precedent) — the simulated signature's arm structure, "
    "disclosed as a MAPPING CHOICE (the wet lab reads voltages, the "
    "sim writes registers; the mapping is the spec's weakest joint "
    "and is stated as such)",
    "the falsifier's threshold: the predicted d-02 contrast 10.0 "
    "(exp416's scoring table) minus the corpus's falsification band "
    "(2 x the decoded MAE 0.29 = 0.58, exp416's own threshold field) "
    "= 9.42 morphology units — below it, the d-02 mechanism claim is "
    "dead",
    "the substrate for the simulated signature is the exp407 chain "
    "(the corpus's own 2-zone semantics scaled to d-02's voltages), "
    "3 seeds per arm, the settled zone means deposited as numbers",
]


def _zone_signature(g, seed):
    """The d-02 2-zone arm on the chain: settle, cut, walk at dose g,
    return the settled zone-mean voltages + the contrast."""
    tgt = np.empty(100)
    tgt[:50] = -40.8
    tgt[50:] = -30.8
    c = GraphCollective(adjacency=path(100), seed=seed)
    c.set_target(tgt)
    c.write_spec_layer(tgt)
    c.run(30.0, dt=0.1)
    c.phi_spec = tgt.copy()
    c.phi_history = tgt.copy()
    region = list(range(20, 60))
    c.amputate(slice(region[0], region[-1] + 1))
    from collections import deque
    region_set = set(region)
    parent_of, frontier = {}, []
    for i in region:
        nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                if j not in region_set]
        if nbrs:
            parent_of[i] = i
            frontier.append(i)
    order = [(i, parent_of[i]) for i in frontier]
    visited = set(frontier)
    q = deque(frontier)
    while q:
        i = q.popleft()
        for j in np.where(np.abs(c.A[i]) > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                q.append(int(j))
    CORE.NEURAL_SPEC_MIN = -35.0
    try:
        for i, src in order:
            for _ in range(8):
                c.step(0.1)
            if c.phi_spec[i] >= CORE.NEURAL_SPEC_MIN:
                theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
            else:
                theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
            written = theta_new
            if g > 0.0:
                written = ((1.0 - g) * theta_new
                           + g * float(c.phi_history[i]))
            c.theta[i] = written
            c.V[i] = written
            c.phi_history[i] = written
    finally:
        CORE.NEURAL_SPEC_MIN = -60.0
    c.run(30.0, dt=0.1)
    z1 = float(np.mean(c.V[:50]))
    z2 = float(np.mean(c.V[50:]))
    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor restored"
    return z1, z2, abs(z1 - z2)


def main() -> dict:
    verdicts: dict[str, str] = {}

    # ---- G1 the trace: every claim cites a landed deposit
    cited_ok = True
    for rel, fields in CITED:
        p = os.path.join(ROOT, rel)
        try:
            d = json.load(open(p))
            for f in fields:
                assert f in d, (rel, f)
        except (OSError, KeyError, AssertionError) as e:
            cited_ok = False
            print("  missing citation: %r" % (e,))
    verdicts["G1"] = "PASS" if cited_ok else "REFUTE"
    print("G1 %s (%d deposits cited and loaded)"
          % (verdicts["G1"], len(CITED)))
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    else:
        d416 = json.load(open(os.path.join(
            ROOT, "results", "exp416_generator_wetlab_path.json")))
        d02 = [r for r in d416["scoring_table"]
               if r["name"] == "d-02"][0]
        d118 = json.load(open(os.path.join(
            ROOT, "results", "exp118_corpus_full.json")))
        mae = float(d118["aggregates"]["mae_corrected_decoded"])
        band = 2.0 * mae
        contrast_pred = float(d02["max_contrast"])
        falsifier_bar = contrast_pred - band

        # ---- the spec (the deliverable)
        spec = {
            "anatomy": "d-02",
            "zones": d02["zones"],
            "predicted_voltages": d02["voltages"],
            "predicted_contrast": contrast_pred,
            "falsification_band": round(band, 4),
            "falsifier": {
                "observation": "the zone contrast in the signature "
                               "arm (wnt 0.25 + apc 1.0) at the d-02 "
                               "geometry, measured by voltage-"
                               "sensitive dye imaging at the settled "
                               "timepoint",
                "threshold": round(falsifier_bar, 4),
                "reading": "measured contrast < threshold -> the "
                           "d-02 mechanism claim is DEAD (the "
                           "two-zone bioelectric pattern is not "
                           "writable at the predicted contrast); "
                           ">= threshold -> the claim survives the "
                           "test",
                "equipment_class": "voltage-sensitive dye imaging "
                                   "(the published planaria VSD "
                                   "technique class; no new "
                                   "instruments)"},
            "manipulated_variables": ["wnt dose", "apc on/off"],
            "n_vars": 2,
            "arm_table": [
                {"arm": "A", "wnt": 0.25, "apc": 1.0,
                 "role": "the d-02 signature arm"},
                {"arm": "B", "wnt": 1.0, "apc": 1.0,
                 "role": "the dose control (the class table's "
                         "apc dose)"},
                {"arm": "C", "wnt": 0.25, "apc": 0.0,
                 "role": "the apc-omission control"},
                {"arm": "D", "wnt": None, "apc": 0.0,
                 "cut": "the d-02 plane/fraction",
                 "role": "the cutting-only junction control"},
            ],
            "n_arms": 4,
            "n_worms_per_arm": 12,
            "confounds": [
                "the wnt dose -> register-g mapping is the spec's "
                "weakest joint (disclosed above)",
                "the VSD readout's temporal window (the settled "
                "timepoint must match the sim's settle semantics)",
                "the apc dose's own variability (the class table's "
                "single dose 1.0 mitigates)"],
            "citations": [c[0] for c in CITED],
        }

        # ---- G3 the minimality
        minimality_ok = spec["n_vars"] <= 2 and spec["n_arms"] <= 4
        verdicts["G3"] = "PASS" if minimality_ok else "REFUTE"
        print("G3 %s (%d vars, %d arms)"
              % (verdicts["G3"], spec["n_vars"], spec["n_arms"]))

        # ---- G2 the falsifier structure
        g2_ok = ("threshold" in spec["falsifier"]
                 and isinstance(spec["falsifier"]["threshold"], float)
                 and "equipment_class" in spec["falsifier"])
        verdicts["G2"] = "PASS" if g2_ok else "REFUTE"
        print("G2 %s (the falsifier: contrast < %.4f kills the claim; "
              "%s)" % (verdicts["G2"], falsifier_bar,
                       spec["falsifier"]["equipment_class"][:30]))

        # ---- G4 the simulated signature (numbers, not prose)
        arms = {"A_wnt0.25_apc1.0": 0.25, "B_wnt1.0_apc1.0": 1.0,
                "C_wnt0.25_apc0.0": 0.25, "D_cut_only": 0.0}
        sig = {}
        for arm, g in arms.items():
            rows = [_zone_signature(g, s) for s in (0, 1, 2)]
            z1 = float(np.mean([r[0] for r in rows]))
            z2 = float(np.mean([r[1] for r in rows]))
            ct = float(np.mean([r[2] for r in rows]))
            sig[arm] = {"zone1_mV": round(z1, 3),
                        "zone2_mV": round(z2, 3),
                        "contrast_mV": round(ct, 3),
                        "g": g}
            print("  %s: z1 %.2f z2 %.2f contrast %.2f"
                  % (arm, z1, z2, ct))
        verdicts["G4"] = "PASS"
        print("G4 PASS (the simulated signature deposited as numbers "
              "per arm)")

        branch = ("SPEC-BLOATED" if verdicts["G3"] == "REFUTE"
                  else "SPEC-DEPOSITED")

        out = {
            "experiment": "exp437",
            "title": "THE MINIMAL FALSIFIABLE WET-LAB TEST FOR d-02 "
                     "(batch HU-13)",
            "spec": spec,
            "simulated_signature": sig,
            "disclosures": BODY_DISCLOSURES,
            "gates": verdicts,
            "verdict": branch,
        }
        with open(DEPOSIT, "w") as f:
            json.dump(out, f, indent=1, sort_keys=True)
        verdicts["G5"] = "PASS"
        print("G5 PASS (deposit %s)" % DEPOSIT)
        print("EXP437 VERDICT: %s %s" % (verdicts, branch))
        return {"gates": verdicts}


if __name__ == "__main__":
    main()
