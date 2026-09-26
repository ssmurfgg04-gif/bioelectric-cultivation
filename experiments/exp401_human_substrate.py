#!/usr/bin/env python3
"""exp401 — THE HUMAN SUBSTRATE INGESTION (batch HU-1; the first
experiment of the HUMAN EXTENSION, ledger L295; the charter is
docs/HUMAN_EXTENSION.md). THE PLANARIAN PROJECT IS COMPLETE (L1–L294,
HEAD d089875). THE HYPOTHESIS UNDER TEST (handoff Section 2): the
structural findings of the planarian corpus — the two-channel law, the
history register, the composed carrier, the deadline law — are
universal properties of bioelectric systems, not planarian-specific.
THE FIRST STEP IS INGESTION: extend the model to a REAL human
connectome and show the machinery runs on it.

THE REAL DATA (handoff Section 3: mine what exists, no new
experiments): the HCP group-average functional connectome at the
Schaefer-400 parcellation (400 cortical parcels), the discovery cohort
of Vos de Wael et al. 2018 (PNAS), as distributed with brainspace
(load_group_fc('schaefer', 400)), committed in-repo as
data/human_fc_schaefer400.npy
(sha256 9c8cc9155c2f96e680db9730e25c0c9d56f643949378afb28250a462d9b12243).

THE PRE-REGISTERED PREPROCESSING RULE (human/substrate.py, frozen at
the pre-registration commit; every step deterministic, nothing tuned
to the outcome): negatives -> 0 (2.08% of edges, disclosed — the
model's conductance matrix is non-negative); diagonal -> 0; per-node
symmetric top-6 (the pre-named ladder {6, 8, 10, 12, 16}: the FIRST k
that connects all 400 nodes — k=6 connects 400/400, disclosed); global
scale to mean row-sum 0.4 (the path-regime comparability rule: the
validated 1-D machinery runs at interior degree 2 x g_gap 0.20 = 0.4
total conductance per node). The dynamical parameters keep the
planarian defaults EVERYWHERE — the human mapping enters through the
real connectivity structure only, no parameter fitted on human data.

THE IDENTITY TARGET (data-shaped, deterministic, synthetic semantics
as in the planarian corpus): order the nodes by the leading
eigenvector of the human adjacency, partition into 5 equal zones of
80, assign the house ladder centers [-50, -40, -30, -20, -10] mV.

PRE-REGISTERED GATES (each evaluated exactly once):

  G1  THE DATA INTEGRITY FACE: the committed FC loads against the
      pinned sha256 (9c8cc9155c2f96e680db9730e25c0c9d56f643949378afb
      28250a462d9b12243 — fail=STOP); shape (400, 400); symmetric
      atol 1e-12; the raw diagonal carries 1.0 self-coupling; the
      negative-edge fraction in [0.015, 0.030] (the documented 2.08%
      property — a silent preprocessing drift raises here).
  G2  THE HUMAN DYNAMICS FACE: the GraphCollective runs on the
      pre-registered human adjacency, 5 seeds x 30.0 time units at
      dt 0.1: every V/theta finite at every seed (fail=STOP); the
      settled pattern error vs the identity target < 6.0 (the house
      bar) on 5/5 seeds; the adjacency's mean row-sum == 0.4 within
      1e-9 (the comparability rule asserted, not assumed).
  G3  THE ZERO-DRIFT ANCHOR (the human package adds an ingestion
      layer and NOTHING else): (a) the frozen 100-node path
      instrument — BioElectricCollective(n=100, seed=0), the
      pre-named 20-cell alternating target (-30/-50), run 30.0/0.1 —
      reproduces the pre-registered reference BIT-EXACT: pattern
      error == 4.3562672231 (printed at 10 decimals, compared on the
      float64 bytes) and V[:5] digest sha256[:16] == 25d22aba033b9d9a
      (fail=STOP — the human layer must not perturb the core);
      (b) `git diff --stat HEAD -- cultivation/` reports ZERO changed
      files at run time (the core is byte-untouched by the bridge).
  G4  THE BASELINE DEPOSIT: the per-node error vector (the 400-node
      settled error vs the identity target, seed 0), the summary
      stats (mean/worst/median over the 5 seeds), the adjacency
      provenance (the ladder k, the density, the row-sum stats), and
      the fingerprint chain deposited as
      results/exp401_human_substrate.json (fail=STOP on any missing
      field).

BRANCH LATTICE (pre-named): 4/4 PASS -> HUMAN-SUBSTRATE-LIVE (the
machinery runs on a real human connectome; the validation experiments
exp402-406 are unblocked); any gate FAIL -> INGESTION-REFUTED (the
bridge is not buildable at this scale/regime and the honest answer is
diagnosis before any further human experiment).

THE HONEST LIMITS (handoff Section 5, restated per deposit): this is
a 400-parcel coarse-graining of 86 billion neurons; the FC matrix is
group-average functional connectivity, not structural wiring; the
dynamical parameters are the planarian defaults (the hypothesis under
test is whether the STRUCTURE alone carries the findings — that is
the test, not a confound).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.substrate.graph import GraphCollective
from human.substrate import FC_SHA256, build_human_adjacency, human_target, load_human_fc

DEPOSIT = os.path.join(ROOT, "results", "exp401_human_substrate.json")

NS = [400]
SEEDS = [0, 1, 2, 3, 4]
DURATION = 30.0
DT = 0.1
BAR = 6.0
REF_ERR = 4.3562672231
REF_HEAD_SHA = "25d22aba033b9d9a"


def _sha16(arr: np.ndarray) -> str:
    return hashlib.sha256(np.asarray(arr, dtype=np.float64).tobytes()).hexdigest()[:16]


def main() -> dict:
    verdicts: dict[str, str] = {}
    detail: dict[str, object] = {}

    # ---- G1 the data integrity face
    fc = load_human_fc()          # raises on sha mismatch (fail=STOP)
    neg_frac = float((fc < 0).mean())
    diag_mean = float(fc.diagonal().mean())
    assert fc.shape == (400, 400)
    assert np.allclose(fc, fc.T, atol=1e-12)
    assert 0.015 <= neg_frac <= 0.030, neg_frac
    assert abs(diag_mean - 1.0) < 1e-9
    verdicts["G1"] = "PASS"
    detail["neg_frac"] = neg_frac
    detail["diag_mean"] = diag_mean
    print("G1 PASS (neg_frac %.4f, diag %.2f)" % (neg_frac, diag_mean))

    # ---- G2 the human dynamics face
    W = build_human_adjacency(fc)
    rs = float(W.sum(axis=1).mean())
    assert abs(rs - 0.4) < 1e-9, rs
    tgt, zones = human_target(W)
    assert np.bincount(zones).tolist() == [80] * 5
    per_seed = []
    per_node_seed0 = None
    for seed in SEEDS:
        h = GraphCollective(adjacency=W, seed=seed)
        h.set_target(tgt)
        h.run(DURATION, dt=DT)
        assert np.isfinite(h.V).all() and np.isfinite(h.theta).all()
        err = float(h.pattern_error(tgt))
        assert np.isfinite(err)
        per_seed.append(err)
        if seed == 0:
            per_node_seed0 = np.abs(h.theta - tgt).copy()
    assert max(per_seed) < BAR, per_seed
    verdicts["G2"] = "PASS"
    detail["per_seed_errs"] = per_seed
    detail["mean_err"] = float(np.mean(per_seed))
    detail["worst_err"] = float(np.max(per_seed))
    detail["mean_rowsum"] = rs
    print("G2 PASS (errs %s, worst %.4f < %.1f)"
          % (["%.4f" % e for e in per_seed], max(per_seed), BAR))

    # ---- G3 the zero-drift anchor
    c = BioElectricCollective(n=100, seed=0)
    tgt100 = np.where((np.arange(100) % 20) < 10, -30.0, -50.0)
    c.set_target(tgt100)
    c.run(30.0, dt=0.1)
    err100 = float(c.pattern_error(tgt100))
    sha100 = _sha16(np.concatenate([[err100], c.V[:5].copy()]))
    assert err100 == REF_ERR, repr((err100, REF_ERR))
    assert sha100 == REF_HEAD_SHA, repr((sha100, REF_HEAD_SHA))
    diff = subprocess.run(
        ["git", "diff", "--stat", "HEAD", "--", "cultivation/"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert diff == "", diff
    verdicts["G3"] = "PASS"
    detail["ref_err"] = err100
    detail["ref_head_sha"] = sha100
    detail["core_diff_empty"] = True
    print("G3 PASS (anchor bit-exact: err %.10f, sha %s; core diff empty)"
          % (err100, sha100))

    # ---- G4 the baseline deposit
    dep = {
        "experiment": "exp401",
        "title": "THE HUMAN SUBSTRATE INGESTION (the human bridge, batch HU-1)",
        "data": {
            "fc_file": "data/human_fc_schaefer400.npy",
            "fc_sha256": FC_SHA256,
            "source": "HCP group-average FC, Schaefer-400, Vos de Wael et al. 2018 PNAS discovery cohort, via brainspace load_group_fc('schaefer', 400)",
        },
        "preprocessing": {
            "rule": "negatives->0; diag->0; per-node symmetric top-6 (ladder {6,8,10,12,16}, first k connecting 400/400); scale to mean row-sum 0.4 (path-regime comparability)",
            "ladder_k": 6,
            "density": float((W > 0).mean()),
            "rowsum_mean": rs,
            "rowsum_std": float(W.sum(axis=1).std()),
        },
        "target": "leading-eigenvector ordering, 5 zones x 80, centers [-50,-40,-30,-20,-10]",
        "gates": verdicts,
        "per_seed_errs": per_seed,
        "mean_err": float(np.mean(per_seed)),
        "worst_err": float(np.max(per_seed)),
        "per_node_err_seed0": [float(x) for x in per_node_seed0],
        "anchor": {"ref_err": REF_ERR, "ref_head_sha": REF_HEAD_SHA,
                   "core_diff_empty": True},
        "verdict": "HUMAN-SUBSTRATE-LIVE",
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(dep, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G4"] = "PASS"
    print("G4 PASS (deposit %s)" % DEPOSIT)

    print("EXP401 VERDICT: %s %s" % (verdicts, "HUMAN-SUBSTRATE-LIVE"))
    return {"gates": verdicts, "detail": detail}


if __name__ == "__main__":
    main()
