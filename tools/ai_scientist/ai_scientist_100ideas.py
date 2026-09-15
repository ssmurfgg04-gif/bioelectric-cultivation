"""AI-Scientist background driver: 100 new ideas, generated + pooled.

Runs SakanaAI/AI-Scientist v1's generate_ideas() in rounds of 12 against
the bioelectric_fidelity template (v2 — the multi-pattern stack surface),
through the local OpenAI-compatible proxy (zai_openai_proxy.mjs, port
8787). After every round:

  * pools the round's ideas (dedupe by normalized Name),
  * computes the Pareto front on (Interestingness, Novelty, Feasibility),
  * rewrites seed_ideas.json as the Pareto front of the whole pool so far
    (capped at 16 — dedup pressure + diversity, context stays lean),
  * checkpoints the pool to pool_checkpoint.json (crash-safe per round).

Stops when >= TARGET new ideas are pooled. No Semantic Scholar novelty
check (rate-limited shared IP — the M17 lesson); novelty vetting happens
offline in the Pareto vetting step against our own corpus.

Usage: nohup python ai_scientist_100ideas.py > ai_scientist.log 2>&1 &
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

TARGET = int(os.environ.get("TARGET_IDEAS", 100))
ROUND_IDEAS = int(os.environ.get("ROUND_IDEAS", 12))
MAX_ROUNDS = int(os.environ.get("MAX_ROUNDS", 16))
TEMPLATE = "/home/z/AI-Scientist/templates/bioelectric_fidelity"
OUT_DIR = "/home/z/AI-Scientist/results/bioelectric_fidelity"
POOL = os.path.join(OUT_DIR, "pool_checkpoint.json")
ROUND_CMD = [sys.executable, "-u",
             "/home/z/AI-Scientist/run_round.py"]

os.makedirs(OUT_DIR, exist_ok=True)


def _norm(name: str) -> str:
    return "".join(c for c in name.lower() if c.isalnum())


def pareto_front(ideas: list[dict]) -> list[dict]:
    """Non-dominated set maximizing (Interestingness, Novelty, Feasibility)."""
    def key(d):
        return (float(d.get("Interestingness", 0)),
                float(d.get("Novelty", 0)),
                float(d.get("Feasibility", 0)))
    front = []
    for i, a in enumerate(ideas):
        ka = key(a)
        dominated = False
        for j, b in enumerate(ideas):
            if i == j:
                continue
            kb = key(b)
            if all(x >= y for x, y in zip(kb, ka)) and any(
                    x > y for x, y in zip(kb, ka)):
                dominated = True
                break
        if not dominated:
            front.append(a)
    return front


def load_pool() -> dict:
    if os.path.exists(POOL):
        with open(POOL) as f:
            return json.load(f)
    return {"ideas": [], "names": [], "rounds_done": 0}


def save_pool(pool: dict) -> None:
    with open(POOL, "w") as f:
        json.dump(pool, f, indent=1)


def main() -> None:
    pool = load_pool()
    t0 = time.time()
    print(f"[driver] pool starts at {len(pool['ideas'])} ideas "
          f"(rounds done: {pool['rounds_done']})", flush=True)

    while len(pool["ideas"]) < TARGET and pool["rounds_done"] < MAX_ROUNDS:
        r = pool["rounds_done"] + 1
        # seed the round with the pool's Pareto front (dedup pressure)
        seeds = pareto_front(pool["ideas"])[-16:]
        if not seeds:
            with open(os.path.join(TEMPLATE, "trial_ideas.json")) as f:
                trial = json.load(f)
            seeds = sorted(
                trial,
                key=lambda d: -(d.get("Interestingness", 0)
                                + d.get("Novelty", 0)
                                + d.get("Feasibility", 0)))[:8]
        with open(os.path.join(TEMPLATE, "seed_ideas.json"), "w") as f:
            json.dump(seeds, f, indent=2)

        print(f"\n[driver] round {r}/{MAX_ROUNDS}: {len(seeds)} seeds, "
              f"{ROUND_IDEAS} ideas to generate "
              f"(pool {len(pool['ideas'])}/{TARGET})", flush=True)
        t_round = time.time()
        try:
            cp = subprocess.run(
                ROUND_CMD + [str(ROUND_IDEAS)], timeout=3600, check=False,
                capture_output=False)
            print(f"[driver] round {r} exit={cp.returncode} "
                  f"({time.time()-t_round:.0f}s)", flush=True)
        except subprocess.TimeoutExpired:
            print(f"[driver] round {r} TIMED OUT (3600s) — skipping",
                  flush=True)

        # harvest whatever the round wrote
        ideas_file = os.path.join(TEMPLATE, "ideas.json")
        if os.path.exists(ideas_file):
            with open(ideas_file) as f:
                round_ideas = json.load(f)
            added = 0
            for d in round_ideas:
                nm = _norm(d.get("Name", ""))
                if nm and nm not in pool["names"]:
                    pool["names"].append(nm)
                    d["round"] = r
                    pool["ideas"].append(d)
                    added += 1
            print(f"[driver] round {r} harvested {added} new ideas "
                  f"(pool {len(pool['ideas'])}/{TARGET})", flush=True)
        pool["rounds_done"] = r
        save_pool(pool)

    front = pareto_front(pool["ideas"])
    summary = {
        "n_ideas": len(pool["ideas"]),
        "n_rounds": pool["rounds_done"],
        "pareto_front_size": len(front),
        "pareto_front": front,
        "elapsed_s": round(time.time() - t0),
    }
    with open(os.path.join(OUT_DIR, "generation_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(f"[driver] DONE: {len(pool['ideas'])} ideas, "
          f"Pareto front {len(front)} "
          f"({time.time()-t0:.0f}s total)", flush=True)


if __name__ == "__main__":
    main()
