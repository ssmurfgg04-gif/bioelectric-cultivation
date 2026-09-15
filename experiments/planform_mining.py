#!/usr/bin/env python3
"""PlanformDB mining for per-experiment Stage 2 validation (night two).

Shares the exp21 experiment loader and adds:
  * per-experiment amputation PLANE parsed from the curated Manipulation
    name (Lobo et al. 2013 curated naming is the ground truth; the drawn
    RemoveAction/CropAction polygons vary their image frame per
    publication and are kept for audit only);
  * drug-class enrichment: ExperimentDrug joins map GJ-blocker drugs
    (octanol/heptanol/hexanol) onto the innexin protocol and Ca/ATPase
    drugs onto the ion_channel protocol, widening the bioelectric slices
    beyond the 9 RNAi-only innexin experiments (exp21's power caveat).

PLANE TAXONOMY (pre-registered 2026-09-15, BEFORE any per-plane outcome
query; name-keyword rules applied verbatim, first match wins):
  head        anterior tissue removed (head crop/amputation, pre-pharyngeal,
              pre-eye/post-eye remove, headless anterior removes, 'Anterior
              k/N remove'); optional cut fraction f recorded
  tail        posterior tissue removed (tail crop/amputation,
              post-pharyngeal*, 'Small posterior*', 'Two tails, one *-cut')
  head_tail   both ends removed (head plus *-pharyngeal crops, headless
              anterior+posterior remove, 'Head amputation, postpharyngeal')
  trunk       mid-body removed (pharyngeal crop/amputation, trunk crop,
              center remove, fragments, trunk slices, triangles)
  crosspiece  'Anterior k/N crosspiece' — piece kept from behind the head
              to cut position f = k/N; posterior cut face at f regenerates
              the tail ('exclude head' variant also removes the head tip)
  graft/join  transplant manipulations (no sim mapping tonight)
  irr         irradiation without cutting (no neoblast layer in model)
  lateral     2D cuts (notch/slit/eye/wedge/lateral/side/midline/T-cut)
  generic     bare 'Amputation' family — mapped to tail protocol but
              flagged generic_amputation for robustness re-runs
  none        no cutting ('Wild type', 'Growth', 'Degrowth')

DRUG -> PROTOCOL CLASS (pre-registered, alphabetical):
  gj_block     Hexanol, Heptanol, Octanol           -> innexin protocol
  ion_channel  EGTA, Nicardipine, Potassium,
               PZQ, SCH-28080, Sodium azide? (unmapped: record-only)
  record_only  everything else (Ivermectin et al.)
Experiment class = priority(rnai classes) if any, else drug class if any
mapped, else cutting.
"""
from __future__ import annotations

import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.exp21_planform_benchmark import (  # noqa: E402,F401
    DB, WT_MORPH_ID, classify_rnai, load_experiments,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- drug -> protocol class (pre-registered) --------------------------
DRUG_CLASS = {
    "hexanol": "gj_block", "heptanol": "gj_block", "octanol": "gj_block",
    "egta": "ion_channel", "nicardipine": "ion_channel",
    "potassium": "ion_channel", "pzq": "ion_channel",
    "sch-28080": "ion_channel",
}

_CLASS_RANK = {"innexin": 0, "ion_channel": 1, "morphogen": 2,
               "other_rnai": 3, "gj_block": 0, "drug_only": 3}

# AP-polarity morphogen subclass: the only morphogen genes the 1D sheet
# can speak to (beta-catenin/wnt set posterior identity; apc/axin are its
# antagonists). notch/bmp/fgf act on DV/eye/brain axes -> record-only.
AP_MORPHOGEN_RE = re.compile(
    r"catenin|wnt|apc|axin|beta|b-catenin", re.I)


def plane_of_manipulation(name: str) -> dict:
    """Parse the curated manipulation name into a plane record.

    Returns {'plane': str, 'cut_f': float|None, 'exclude_head': bool,
             'generic': bool}.
    """
    l = (name or "").lower()
    rec = {"plane": "none", "cut_f": None, "exclude_head": False,
           "generic": False}
    if not l or l in ("wild type", "growth", "degrowth"):
        return rec
    # graft / transplant family
    if ("graft" in l or "transplant" in l or "join" in l
            or "parabiosis" in l):
        rec["plane"] = "graft"
        return rec
    # crosspiece: anterior k/N piece kept, posterior cut face at f=k/N
    m = re.search(r"anterior (\d+)(?:-(\d+))?/(\d+) crosspiece", l)
    if m:
        k1 = int(m.group(1))
        k2 = int(m.group(2)) if m.group(2) else k1
        denom = int(m.group(3))
        rec["plane"] = "crosspiece"
        rec["cut_f"] = ((k1 + k2) / 2.0) / denom
        rec["exclude_head"] = "exclude head" in l
        return rec
    # 'Anterior k/N remove' = anterior tip piece removed
    m = re.search(r"anterior (\d+)/(\d+) remove", l)
    if m:
        rec["plane"] = "head"
        rec["cut_f"] = int(m.group(1)) / int(m.group(2))
        return rec
    if "irradiation" in l and "amputation" not in l and "crop" not in l:
        rec["plane"] = "irr"
        return rec
    # both ends
    if (("head" in l and ("post-pharyngeal" in l or "postpharyngeal" in l
                          or "pre-pharyngeal" in l or "prepharyngeal" in l))
            or "anterior remove, posterior remove" in l
            or ("head" in l and "tail" in l)):
        rec["plane"] = "head_tail"
        return rec
    # posterior family (before head checks: 'post-pharyngeal' has no 'head')
    if ("tail" in l or "post-pharyngeal" in l or "postpharyngeal" in l
            or "small posterior" in l or "split posterior" in l):
        rec["plane"] = "tail"
        if "amputation" in l and not re.search(r"head|tail|pharyn", l):
            rec["generic"] = True
        return rec
    # anterior family
    if ("head" in l or "pre-pharyngeal" in l or "prepharyngeal" in l
            or "pre-eye" in l or "post-eye" in l or "decapitat" in l
            or "anterior" in l):
        rec["plane"] = "head"
        return rec
    # mid-body family
    if ("pharyn" in l or "trunk" in l or "center" in l or "fragment" in l
            or "crosspiece" in l):
        rec["plane"] = "trunk"
        return rec
    # 2D cuts and everything else
    rec["plane"] = "lateral"
    return rec


def load_widened(con: sqlite3.Connection) -> dict:
    """experiment id -> class, plane, outcome abnormal, provenance.

    Extends exp21.load_experiments with plane + drug enrichment.
    Outcome metric unchanged (pre-registered in exp21): Num-weighted mean
    over post-regeneration result sets of 1 - freq(Wild type).
    """
    exps = load_experiments(con)  # class + abnormal + rnais (exp21)
    cur = con.cursor()

    # manipulation name per experiment
    name_of_manip = dict(cur.execute("SELECT Id, Name FROM Manipulation"))
    manip_of_exp = dict(cur.execute(
        "SELECT Id, Manipulation FROM Experiment"))

    # drugs per experiment
    drug_name = dict(cur.execute("SELECT Id, Name FROM Drug"))
    drugs_of_exp: dict[int, list[str]] = {}
    for eid, did in cur.execute("SELECT Experiment, Drug FROM ExperimentDrug"):
        if did in drug_name:
            drugs_of_exp.setdefault(eid, []).append(drug_name[did])

    for eid, e in exps.items():
        name = name_of_manip.get(manip_of_exp.get(eid), "") or ""
        e["manipulation"] = name
        e.update(plane_of_manipulation(name))
        e["drugs"] = drugs_of_exp.get(eid, [])
        e["drug_classes"] = sorted({DRUG_CLASS[d.lower()] for d in e["drugs"]
                                    if d.lower() in DRUG_CLASS})
        # class enrichment: RNAi class wins by exp21 rank; a mapped drug
        # class lifts otherwise-cutting experiments into a bioelectric
        # slice (octanol/heptanol = the classic GJ-block paradigm)
        if e["group"] == "cutting" and e["drug_classes"]:
            e["group"] = e["drug_classes"][0]
        e["ap_morphogen"] = bool(
            e["group"] == "morphogen"
            and any(AP_MORPHOGEN_RE.search(r) for r in e["rnais"]))
    return exps


def slice_counts(exps: dict) -> dict:
    """(class, plane) -> n, for the sim-mappable planes."""
    out: dict[tuple[str, str], int] = {}
    for e in exps.values():
        out.setdefault((e["group"], e["plane"]), 0)
        out[(e["group"], e["plane"])] += 1
    return dict(sorted(out.items()))


if __name__ == "__main__":
    con = sqlite3.connect(DB)
    exps = load_widened(con)
    print(f"n_experiments with outcomes: {len(exps)}")
    print("\n(class, plane) counts:")
    for (g, p), n in slice_counts(exps).items():
        print(f"  {g:12s} {p:11s} {n:4d}")
    planes = {}
    for e in exps.values():
        planes.setdefault(e["plane"], []).append(e["abnormal"])
    print("\nrecorded abnormal by plane (all classes pooled):")
    import numpy as np
    for p, vals in sorted(planes.items()):
        print(f"  {p:11s} n={len(vals):4d}  mean {np.mean(vals):.3f}")
