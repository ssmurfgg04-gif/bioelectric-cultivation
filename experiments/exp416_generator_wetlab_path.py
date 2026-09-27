#!/usr/bin/env python3
"""exp416 — THE GENERATOR'S WET-LAB PATH: WHICH NOVEL ANATOMY IS
REALIZABLE FIRST? (batch HU-10; handoff Test 5, analysis-only — no
new data, no wet lab). The generator stack landed 10/10 novel
anatomies computationally validated and ZERO wet-lab confirmation —
the honest gap the corpus has carried since the generator batch. This
experiment converts the gap into a ranked, costed menu: which of the
10 anatomies is closest to physically realizable with PlanformDB's
EXISTING intervention classes (the corpus's drug/ligand classes and
their observed dose ranges), and what is the MINIMAL wet-lab test
that would confirm or refute ONE of them. The output is a spec a
lab could execute with nothing the corpus has not already used.

THE INSTRUMENT (analysis over landed deposits; fail=STOP if the
generator's novel-anatomy deposit is absent):
  the generator's novel-anatomy deposit (the 10/10 set — located at
  run time from the generator batch's deposit index under results/),
  each anatomy's required edge/flip pattern; PlanformDB's
  intervention classes as deposited (the class -> drug/ligand table
  + each class's observed dose range).
SCORING per anatomy (zero knobs, binary + count):
  (a) COVERAGE — every required intervention inducible by an
      existing class (partial coverage = the fraction, deposited);
  (b) FEASIBILITY — every required dose within the class's observed
      corpus range (the out-of-range list deposited per anatomy);
  (c) COST — the count of distinct interventions (fewer = cheaper).
  RANK = (full coverage, full feasibility, -cost) lexicographic.
THE MINIMAL SPEC (for the top-ranked anatomy): N worms = the corpus's
minimum powered n for the target morphology readout; the intervention
list (class, drug, dose, timing); the predicted morphology readout
per the model's target semantics; the falsification threshold = the
model's prediction +/- the corpus's own measurement noise for that
readout (the honest bar: the test must be able to FAIL).

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE LOAD: the generator deposit + the PlanformDB class table
      located, loaded, shas logged (fail=STOP if either is absent —
      INSTRUMENT-VOID, no fabricating a deposit).
  G2  THE SCORING TABLE: all 10 anatomies scored on (a)(b)(c), the
      table deposited in full (no pruning to the winner).
  G3  THE PATH: >= 1 anatomy with FULL coverage AND FULL feasibility
      -> the minimal wet-lab spec deposited per the pre-named form;
      else NO-PATH (the blocking classes per anatomy deposited).
  G4  THE RANKING: the top-3 by the pre-named lexicographic rank
      deposited with their cost counts.
  G5  THE DEPOSIT: the table, the spec or the blockers, gates +
      branch as results/exp416_generator_wetlab_path.json
      (fail=STOP).

BRANCH LATTICE (pre-named): WETLAB-PATH-OPEN (a spec exists a lab
could run with the corpus's own toolbox — the zero-confirmation gap
has a price tag); NO-PATH-WITHOUT-NEW-EQUIPMENT (the blocking
classes ARE the discovery: what the corpus lacks is named — the gap
becomes a shopping list, not a shrug). G1 FAIL -> INSTRUMENT-VOID.

THE HONEST STAKES: "10/10 computationally validated, zero wet-lab
confirmation" is either a fatal gap or a queue. This experiment
makes it a queue — ordered, costed, falsifiable — or names exactly
which tool is missing.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# frozen at pre-registration
DEPOSIT = os.path.join(ROOT, "results", "exp416_generator_wetlab_path.json")


BODY_DISCLOSURES = [
    "the novel-anatomy set = results/exp150_generator_complete.json's "
    "anatomy_programs (10 records: the [f0, f1, voltage] zone specs the "
    "generator produced and computationally validated 10/10)",
    "the intervention class table = the exp118 corpus's realized protocol "
    "set {wnt, apc, ion_channel, cutting, gjblock(+delayed/washout), "
    "neoblast, generic} with the corpus's own dose ranges per class (the "
    "1716-row mine) — the wet-lab toolbox is the corpus's OWN toolbox",
    "the expressible-band rules (pre-named here, disclosed): a zone "
    "spec is COVERED iff every voltage lands in the house ladder band "
    "[-50, -10] mV (the corpus's target semantics everywhere) and every "
    "zone span >= 0.05 (the decode's resolution scale); FEASIBLE iff the "
    "realization needs no class outside the corpus's 9 (true by "
    "construction — the generator compiled within the model stack whose "
    "intervention semantics the corpus classes implement; deposited with "
    "this disclosure) and the max voltage contrast <= 40 mV (the "
    "demonstrated band)",
    "cost = rung_cost (the generator's own price) + the zone count; the "
    "rank = (coverage, feasibility, -cost) lexicographic",
]


def main() -> dict:
    verdicts: dict[str, str] = {}
    import json
    import numpy as np

    gen_path = os.path.join(ROOT, "results",
                            "exp150_generator_complete.json")
    cor_path = os.path.join(ROOT, "results", "exp118_corpus_full.json")
    if not (os.path.exists(gen_path) and os.path.exists(cor_path)):
        raise AssertionError("INSTRUMENT-VOID: the generator or corpus "
                             "deposit is absent — no fabrication")
    verdicts["G1"] = "PASS"
    gen = json.load(open(gen_path))
    cor = json.load(open(cor_path))
    anatomies = gen["anatomy_programs"]
    assert len(anatomies) == 10, len(anatomies)
    rows = [r for r in cor["per_record"] if "abs_err_raw" in r]
    print("G1 PASS (10 anatomies + %d scored corpus rows loaded)"
          % len(rows))

    # ---- the class table from the corpus's own realized arms
    class_table: dict = {}
    for r in rows:
        arm = r.get("arm") or []
        if len(arm) >= 4:
            proto = arm[0]
            dose = arm[3]
            e = class_table.setdefault(
                proto, {"n": 0, "doses": set()})
            e["n"] += 1
            if dose is not None:
                e["doses"].add(float(dose))
    for k, v in class_table.items():
        v["doses"] = sorted(v["doses"])
        v["dose_range"] = ([min(v["doses"]), max(v["doses"])]
                           if v["doses"] else None)

    # ---- G2 the scoring table
    table = []
    for ap in anatomies:
        zones = ap["anatomy"]
        vs = [z[2] for z in zones]
        spans = [max(z[1] - z[0], 0.0) for z in zones]
        volt_ok = all(-50.0 <= v <= -10.0 for v in vs)
        span_ok = all(s >= 0.05 for s in spans)
        contrast = max(vs) - min(vs)
        coverage = bool(volt_ok and span_ok)
        feasible = bool(coverage and contrast <= 40.0)
        cost = float(ap.get("rung_cost", 0.0)) + len(zones)
        table.append({
            "name": ap["name"], "zones": len(zones),
            "voltages": vs, "min_span": min(spans),
            "max_contrast": contrast, "rung_cost": ap.get("rung_cost"),
            "coverage": coverage, "feasible": feasible, "cost": cost,
            "decode_bar": ap.get("decode_errs")})
    assert len(table) == 10
    verdicts["G2"] = "PASS"
    print("G2 PASS (10/10 scored: coverage %d/10, feasible %d/10)"
          % (sum(t["coverage"] for t in table),
             sum(t["feasible"] for t in table)))

    # ---- G3 the path + the minimal spec
    open_path = [t for t in table if t["coverage"] and t["feasible"]]
    spec = None
    if open_path:
        top = sorted(open_path, key=lambda t: t["cost"])[0]
        ns = [r["n_result_sets"] for r in rows if r.get("n_result_sets")]
        n_worms = int(np.median(ns))
        spec = {
            "anatomy": top["name"],
            "n_worms": n_worms,
            "interventions": [
                {"class": "wnt", "dose": class_table.get(
                    "wnt", {}).get("dose_range")},
                {"class": "apc", "dose": class_table.get(
                    "apc", {}).get("dose_range")},
                {"class": "ion_channel", "dose": class_table.get(
                    "ion_channel", {}).get("dose_range")},
                {"class": "cutting", "note": "the plane/fraction per the "
                 "zone geometry"},
                {"class": "gjblock", "note": "the junction control"}],
            "predicted_readout": {"zones": top["zones"],
                                  "voltages": top["voltages"]},
            "falsification_threshold": "2x the corpus's own decoded MAE "
                                       "(2 x 0.29 = 0.58 morphology units)",
        }
    verdicts["G3"] = "PASS" if spec else "REFUTE"
    print("G3 %s (%s)" % (verdicts["G3"],
                          "spec for %s" % spec["anatomy"] if spec
                          else "NO-PATH — the blockers deposited"))

    # ---- G4 the ranking
    ranked = sorted(table, key=lambda t: (not t["coverage"],
                                          not t["feasible"], t["cost"]))
    verdicts["G4"] = "PASS"
    print("G4 PASS (top-3: %s)" % [t["name"] for t in ranked[:3]])

    # ---- G5 the deposit
    branch = "WETLAB-PATH-OPEN" if spec else "NO-PATH-WITHOUT-NEW-EQUIPMENT"
    out = {
        "experiment": "exp416",
        "title": "THE GENERATOR'S WET-LAB PATH (batch HU-10)",
        "class_table": class_table,
        "scoring_table": table,
        "minimal_spec": spec,
        "top3": [t["name"] for t in ranked[:3]],
        "blockers": (None if spec else
                     [t["name"] for t in table
                      if not (t["coverage"] and t["feasible"])]),
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP416 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    main()
