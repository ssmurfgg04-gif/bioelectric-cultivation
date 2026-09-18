#!/usr/bin/env python3
"""exp252 — THE DEEP-BAND SUBSTITUTION'S COST (exp243's registered
next; the conjunction's price decomposed; ledger L230).

THE OPEN ITEM (L221): exp243's A2 named the conjunction's price — the
deep-band substitution (P3) triples the reader's worst cell (3.68 vs
the structured-only 0.62 and the random 1.45). THE DECOMPOSITION: where
the 3.68 lives — the boundary vs the interior — via exp208's
machinery on the substituted rows (exp243's deposit carries the
argmax's decomposition records; this experiment re-reads them and
EXTENDS with the per-rung split: the substituted deep-band rows' errs
vs the canonical rows' errs, each decomposed into the canon-boundary
and interior shares).

PRE-REGISTERED GATES:

  B1  THE COST'S ADDRESS: the 3.68's decomposition deposited (the
      boundary share vs the interior share of the substituted rows'
      sum-of-squares) — the gate is the record (zero silence).
  B2  THE RUNG SPLIT: the substituted deep-band rows' worst err vs the
      canonical rows' worst err (both from exp243's deposit, re-read)
      — the gate: the deep-band rows' worst exceeds the canonical
      rows' worst (the substitution IS the cost's carrier, pre-named
      expectation).
  B3  THE DISCIPLINE: exp243's deposit READ-ONLY (sha-recorded,
      byte-unchanged), deterministic.

THE BRANCH (pre-named): the cost is boundary-dominant (the boundary
share >= 0.5) -> BOUNDARY-CARRIED (the conjunction's price is the
boundary signature amplified by the substitution — consistent with
exp226/exp229/exp245's boundary frontier); interior-dominant ->
INTERIOR-CARRIED (the deep band's geometry itself costs — the honest
surprise).

RUN: the deposit re-read + the arithmetic; seconds.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp252.json")


def main() -> dict:
    import hashlib
    p243 = os.path.join(ROOT, "results", "exp243_structured_adversarial.json")

    def sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    sha243 = sha(p243)
    with open(p243) as f:
        dep = json.load(f)

    # B1: the argmax's decomposition records (exp208's machinery, run by
    # exp243 on the argmax candidate's decode rows)
    decomps = dep["gates"]["A3_adversary_anatomy"]["decompositions"]
    b_share = []
    for rec in decomps:
        per = {c["class"]: c["frac_of_sq"] for c in rec["decomposition"]["per_class"]}
        b_share.append(per.get("CANON-BOUNDARY", 0.0))
    mean_b = float(np.mean(b_share)) if b_share else None
    interior_share = 1.0 - mean_b if mean_b is not None else None

    # B2: the deep-band rows' worst vs the canonical rows' worst
    cls_worst = {}
    for c in dep["candidates"]:
        pert = c["pert"]
        for e in c.get("errs", []):
            cls_worst[pert] = max(cls_worst.get(pert, 0.0), float(e))
    deep_worst = cls_worst.get("P3_deep_band_substitution")
    canon_worst = max(cls_worst.get("P1_canon_zone_relabelings", 0.0),
                      cls_worst.get("P2_boundary_double_frequency_rewiring", 0.0))

    b1 = mean_b is not None
    b2 = deep_worst is not None and deep_worst > canon_worst
    branch = ("BOUNDARY-CARRIED" if (b1 and mean_b >= 0.5)
              else "INTERIOR-CARRIED")
    criteria = {"B1_cost_addressed": bool(b1), "B2_substitution_carries": bool(b2)}
    print(f"  B1 the argmax's boundary share: mean {mean_b:.4f} "
          f"(interior {interior_share:.4f}) -> recorded")
    print(f"  B2 deep-band worst {deep_worst} vs canonical worst "
          f"{canon_worst} -> {'PASS' if b2 else 'REFUTED'}")
    print(f"  BRANCH: {branch}")

    out = {
        "exp": "exp252_deep_band_cost (exp243's registered next)",
        "boundary_share_mean": mean_b,
        "interior_share_mean": interior_share,
        "per_seed_boundary_shares": b_share,
        "decompositions": decomps,
        "class_worsts": cls_worst,
        "deep_band_worst": deep_worst,
        "canonical_worst": canon_worst,
        "criteria": criteria,
        "branch": branch,
        "consumed_deposits": {"exp243": sha243},
        "notes": (
            "The decomposition records are exp243's own (exp208's "
            "machinery run on the argmax candidate's decode rows); this "
            "re-read aggregates them and splits the conjunction's price "
            "boundary-vs-interior. PAIR-JUNCTION is exp208's "
            "structure-coupled interior class."),
    }
    sha243b = sha(p243)
    out["read_only_verified"] = bool(sha243b == sha243)
    criteria["B3_discipline"] = bool(out["read_only_verified"])
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(criteria.values())
    print(f"  === {npass}/3 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
