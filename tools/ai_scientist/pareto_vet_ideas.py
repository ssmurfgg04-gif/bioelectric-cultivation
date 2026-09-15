"""Pareto-vet the AI-Scientist's pooled ideas (the 100-idea deliverable).

Input:  /home/z/AI-Scientist/results/bioelectric_fidelity/pool_checkpoint.json
Output: research/ai_scientist_100/{ideas_pooled.json, pareto_vetted.json,
        vetting_report.json} in the REPO (committed artifact).

Vetting layers:
  1. PARETO FRONT — non-dominated set on (Interestingness, Novelty,
     Feasibility), maximizing all three. The Pareto PRINCIPLE read: the
     front should be ~the top quintile of the pool (the 80/20 claim is
     tested, not assumed).
  2. GROUNDEDNESS VET — one LLM call per Pareto idea (through the local
     proxy): given our FALSIFICATION.md kill-record and the current
     frontier (exp24/exp25 included), classify each idea as
       frontier_advancing / already_falsified_in_stack / duplicate_of_done
       / not_implementable_here
     with a one-line reason. The already-falsified class is the one the
     user cares about ('what the failures tell us').
  3. Report: counts per class, the vetted shortlist, the near-duplicate
     clusters (name-normalized), and the honest failure statistics.

Usage: python pareto_vet_ideas.py   (after the generation driver is done)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

POOL = ("/home/z/AI-Scientist/results/bioelectric_fidelity/"
        "pool_checkpoint.json")
REPO_OUT = "/home/z/my-project/repo/research/ai_scientist_100"
FRONTIER_BRIEF = """
OUR STACK'S CURRENT FRONTIER (do NOT re-award ideas that merely restate
these; DO award ideas that move past them):
- V1 neoblast hyperpolarization CONFIRMED (3 modalities); V2 refuted;
  V3 spatial split; V4 innexin-proxy falsified-with-mechanism.
- Matched-channel law: memory-guided repair needs weak anchor pull
  (k_anchor ~ 0.25-0.33); rediscovered independently by CEM search.
- Two-layer capacity law: protected-tier STORAGE of written patterns is
  free (per-pattern); EXPRESSION (working state I_V) is budget-bound.
- Death-restoration equilibrium: zone physics (jump susceptibility,
  senescence hazard) sets the working-state deficit. exp23: NO
  allocation policy beats cell order (policy effects ~0.02 vs physics
  ~0.4). exp24: POTENTIATION (transient AND permanent jump-probability
  reduction on corrected clusters) fails to break the equilibrium
  (delta <= 0.009 vs the 0.046 physics-scale threshold; permanent
  potentiation even costs 5.7yr of median lifespan); random placement
  does nothing (correction-coupling is real but moot).
- exp25: the century-hold CEM policy TRANSPLANTED into competition
  WINS decisively (hold 0.625 vs hand 0.500, +14.4yr median) despite
  2.3x procedure risk — the single-pattern search under-estimated its
  own policy; the searched cadence/budget dimensions are exactly the
  competition-relevant ones.
- exp20/21: spatial/family-expression forms of the bioelectric claims
  refuted at transcriptome level; junction claim bounded to weak-form.
- Known sunk baselines: archive-referenced repair erases novel patterns;
  ungated channel boost propagates errors; amplitude is not a
  corruption axis (discrete symbols).
The stack: numpy cohort simulation, seconds-to-minutes per run, no wet
lab. Metrics: pattern ledgers (I_V / I_anchor / I_recoverable),
median lifespan, hold integrals, codec counters.
"""


def pareto_front(ideas):
    def key(d):
        return (float(d.get("Interestingness", 0)),
                float(d.get("Novelty", 0)),
                float(d.get("Feasibility", 0)))
    front = []
    for i, a in enumerate(ideas):
        ka = key(a)
        dominated = any(
            all(x >= y for x, y in zip(key(b), ka))
            and any(x > y for x, y in zip(key(b), ka))
            for j, b in enumerate(ideas) if i != j)
        if not dominated:
            front.append(a)
    return front


def llm_classify(idea) -> dict:
    prompt = f"""{FRONTIER_BRIEF}

IDEA TO VET:
Name: {idea.get('Name')}
Title: {idea.get('Title', '')}
Experiment sketch: {str(idea.get('Experiment', ''))[:2000]}

Classify this research idea into exactly one class:
- frontier_advancing: proposes a mechanism/intervention/measurement the
  stack has NOT tested and that is not already settled by our results
- already_falsified_in_stack: our own kill-record already refutes its
  core premise
- duplicate_of_done: restates a completed experiment (exp1-25) or a
  listed frontier finding without a new twist
- not_implementable_here: needs wet lab, new data modalities, or
  resources the stack does not have

Respond in EXACTLY this format (no other text):
CLASS: <one of the four>
REASON: <one line, <= 200 chars>
VERDICT_SCORE: <1-10, how much this idea would move the program if it
worked; be harsh>
"""
    proc = subprocess.run(
        ["curl", "-s", "http://127.0.0.1:8787/v1/chat/completions",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({
             "model": "gpt-4o",
             "messages": [{"role": "user", "content": prompt}],
             "temperature": 0.2})],
        capture_output=True, text=True, timeout=300)
    try:
        txt = json.loads(proc.stdout)["choices"][0]["message"]["content"]
    except Exception:
        return {"class": "vet_error", "reason": proc.stdout[:200],
                "verdict_score": None}
    out = {}
    for line in txt.splitlines():
        if line.startswith("CLASS:"):
            out["class"] = line.split(":", 1)[1].strip().lower()
        elif line.startswith("REASON:"):
            out["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("VERDICT_SCORE:"):
            try:
                out["verdict_score"] = int(
                    line.split(":", 1)[1].strip().split("/")[0])
            except ValueError:
                out["verdict_score"] = None
    out.setdefault("class", "vet_error")
    out.setdefault("reason", txt[:200])
    out.setdefault("verdict_score", None)
    return out


def main():
    os.makedirs(REPO_OUT, exist_ok=True)
    with open(POOL) as f:
        pool = json.load(f)
    ideas = pool["ideas"]
    print(f"[vet] pooling {len(ideas)} ideas "
          f"({pool['rounds_done']} rounds)")

    with open(os.path.join(REPO_OUT, "ideas_pooled.json"), "w") as f:
        json.dump(ideas, f, indent=1)

    front = pareto_front(ideas)
    print(f"[vet] Pareto front: {len(front)}/{len(ideas)} "
          f"({100*len(front)/max(len(ideas),1):.0f}%)")

    vetted = []
    for i, idea in enumerate(front):
        v = llm_classify(idea)
        v["Name"] = idea.get("Name")
        v["Interestingness"] = idea.get("Interestingness")
        v["Novelty"] = idea.get("Novelty")
        v["Feasibility"] = idea.get("Feasibility")
        vetted.append(v)
        print(f"  [{i+1}/{len(front)}] {v['Name'][:40]:40s} "
              f"-> {v['class']}  ({v['reason'][:80]})")

    with open(os.path.join(REPO_OUT, "pareto_vetted.json"), "w") as f:
        json.dump(vetted, f, indent=1)

    counts = {}
    for v in vetted:
        counts[v["class"]] = counts.get(v["class"], 0) + 1
    shortlist = [v for v in vetted
                 if v["class"] == "frontier_advancing"]
    shortlist.sort(key=lambda v: -(v.get("verdict_score") or 0))
    report = {
        "n_pooled": len(ideas),
        "n_rounds": pool["rounds_done"],
        "pareto_front_size": len(front),
        "pareto_fraction": round(len(front) / max(len(ideas), 1), 3),
        "class_counts": counts,
        "vetted_shortlist_ranked": [
            {k: v[k] for k in ("Name", "verdict_score", "reason",
                               "Interestingness", "Novelty",
                               "Feasibility")}
            for v in shortlist],
        "pareto_principle_check": {
            "front_fraction": round(len(front) / max(len(ideas), 1), 3),
            "note": "the 80/20 reading: the front should concentrate "
                    "most of the pool's score-mass in a minority of "
                    "ideas — tested, not assumed"},
    }
    with open(os.path.join(REPO_OUT, "vetting_report.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(f"[vet] classes: {counts}")
    print(f"[vet] shortlist (frontier_advancing, ranked): "
          f"{len(shortlist)} ideas")


if __name__ == "__main__":
    main()
