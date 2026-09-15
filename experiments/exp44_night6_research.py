#!/usr/bin/env python3
"""exp44 (night-six, phase 0) — RESEARCH WAVE for the night-six queue.

User directive: "research directive first — you could already have answers
on the web for all these just not pieced together — search deeply."

Each night-six open item gets targeted Europe PMC queries (free REST, no
key, not rate-limited). Output: results/exp44_night6_research.json +
research/NIGHT_SIX_RESEARCH.md (abstracts + synthesis + explicit
mapping query -> mechanism decision).

ITEM -> QUERY MAP (pre-registered before fetching):
  R-M31   anchor availability as fragment STORAGE HISTORY (not a regrow-time
          coin flip): is regenerative outcome determined by pre-amputation
          positional state / duration in state / fragment level?
  R-INX   innexin|head plane dependence: does GJ-blockade phenotype depend
          on amputation plane (two-heads from posterior only)?
  R-CMP   compiler v1 hybrid rule: how do imposed bioelectric states interact
          with STORED positional memory (durability, normalization, latch)?
  R-M32   graded penetrance / dose: any published dose-response or penetrance
          variability data for GJ/bioelectric perturbation?
  R-WIN   the 24h rewrite window: what treatment DURATIONS do published
          protocols use (hours; 48h windows; washout timing)?
  R-SUB   substrate conditioning: morphogenesis/attractors on graph
          topologies (boundary-to-volume / expander-like invariants).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "results", "exp44_night6_research.json")
OUT_MD = os.path.join(ROOT, "research", "NIGHT_SIX_RESEARCH.md")

QUERIES = {
    "R-M31-a": ("M31 fragment-history anchor", (
        'planarian regeneration positional memory fragment')),
    "R-M31-b": ("M31 wound vs pre-existing tissue", (
        'planaria wound positional information pre-existing tissue '
        'regeneration polarity')),
    "R-M31-c": ("M31 duration/commitment in positional state", (
        'planarian tissue remodeling positional identity stability '
        'homeostasis')),
    "R-INX-a": ("innexin plane dependence", (
        'planarian gap junction inhibition regeneration polarity '
        'octanol')),
    "R-INX-b": ("innexin head vs tail fragments", (
        'innexin planarian head regeneration ectopic')),
    "R-INX-c": ("adjacent: bioelectric ectopic head amputation level", (
        'bioelectric ectopic appendage regeneration site level '
        'planarianfrog')),
    "R-CMP-a": ("compiler hybrid rule: imposed vs stored", (
        'bioelectric reprogramming target morphology planarian '
        'memory durability')),
    "R-CMP-b": ("compiler: two-head phenotype normalization", (
        'planarian two-headed phenotype stability normalization')),
    "R-M32-a": ("graded penetrance dose", (
        'regeneration penetrance variability stochastic bioelectric')),
    "R-M32-b": ("GJ inhibitor dose response", (
        'gap junction inhibitor concentration regeneration planaria '
        'dose response')),
    "R-WIN-a": ("treatment window duration", (
        'planarian regeneration treatment duration window hours '
        'octanol heptanol')),
    "R-WIN-b": ("temporal requirement bioelectric rewrite", (
        'bioelectric manipulation temporal window tissue regeneration '
        'sustained')),
    "R-SUB-a": ("morphogenesis on graph topologies", (
        'morphogenetic field model graph topology attractor')),
    "R-SUB-b": ("boundary-to-volume / expander invariants", (
        'reaction diffusion pattern formation network topology '
        'expander graph')),
}

BASE = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        "?query={q}&format=json&pageSize=6&resultType=core")


def fetch(q: str) -> dict:
    url = BASE.format(q=urllib.parse.quote(q))
    req = urllib.request.Request(url, headers={"User-Agent": "bioelectric-cultivation/night6"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    print("=== exp44: night-six research wave (Europe PMC) ===\n")
    out = {"exp": "exp44_night6_research", "channel": "Europe PMC REST",
           "queries": {}}
    md = ["# Night-six research wave (Europe PMC free REST)\n",
          "Executed per the user research directive: find the published "
          "answers that already exist for the night-six open items before "
          "writing any mechanism code. Every abstract below was fetched "
          f"{time.strftime('%Y-%m-%d %H:%M UTC')}.\n"]

    for key, (label, q) in QUERIES.items():
        print(f"  [{key}] {q}")
        try:
            data = fetch(q)
        except Exception as e:                     # noqa: BLE001
            out["queries"][key] = {"query": q, "error": str(e)}
            continue
        hits = []
        for res in data.get("resultList", {}).get("result", []):
            hits.append({
                "id": res.get("id"), "source": res.get("source"),
                "year": res.get("pubYear"),
                "title": clean(res.get("title", "")),
                "journal": res.get("journalTitle", ""),
                "authors": (res.get("authorString", "") or "")[:180],
                "abstract": clean(res.get("abstractText", ""))[:2600],
                "cited": res.get("citedByCount", 0),
            })
        out["queries"][key] = {"label": label, "query": q,
                               "hit_count": data.get("hitCount"),
                               "hits": hits}
        md.append(f"\n## {key} — {label}\n\n**Query:** `{q}` "
                  f"(hitCount {data.get('hitCount')})\n")
        for h in hits:
            md.append(f"### {h['title']} ({h['year']}, {h['journal']}, "
                      f"cited {h['cited']})\n{h['authors']}\n\n"
                      f"{h['abstract'][:2200]}\n")
        time.sleep(0.4)   # polite rate

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(md))
    n_ok = sum(1 for v in out["queries"].values() if "hits" in v)
    print(f"\n  {n_ok}/{len(QUERIES)} queries OK -> {OUT_MD}")


if __name__ == "__main__":
    sys.exit(main())
