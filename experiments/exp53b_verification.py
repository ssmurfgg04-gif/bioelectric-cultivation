#!/usr/bin/env python3
"""exp53b — targeted verification pass (night-eight research wave, part 2).

Findings from exp53 that need resolution before any build:
  F1  PMID 30824103 is a coconut-cellulose materials paper — the directive's
      3h-window citation is WRONG. Find the real 3h-window paper.
  F2  The directive's Zenodo deposits (symbol-grounding, coupling-response-
      geometry) did not surface via search — fetch the given IDs DIRECTLY.
  F3  Full abstracts needed for the verified anchors: 4D atlas (MED42172041),
      TAS (PPRPPR1216581), neurobots (MED41717829), synthetic-construct
      memory (PPRPPR1219439), microtubule/injury genes (MED41099309),
      GJ-blockade anomaly context (MED26610482, MED27499881, MED39372228),
      top-down models (MED27807271), Mind Everywhere (MED42183019).
  F4  notum/wnt1 6h timing: query the primary literature (Reddien lab).
  F5  arXiv syntax retry (simpler query), OpenAlex retry w/ different pool.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "results", "exp53b_verification.json")
OUT_MD = os.path.join(ROOT, "research", "NIGHT_EIGHT_VERIFICATION.md")
UA = "bioelectric-cultivation/night8-verify (contact: research agent)"


def _get(url: str, timeout: int = 30, retries: int = 3) -> bytes:
    last: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:                          # noqa: BLE001
            last = e
            time.sleep(2.0 * (attempt + 1))
    assert last is not None
    raise last


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def epmc(q: str, fmt: str = "core", size: int = 5) -> list[dict]:
    base = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
            f"?query={{q}}&format=json&pageSize={size}&resultType={fmt}")
    data = json.loads(_get(base.format(q=urllib.parse.quote(q))))
    hits = []
    for res in data.get("resultList", {}).get("result", []):
        hits.append({
            "id": f"{res.get('source','')}{res.get('id','')}",
            "year": res.get("pubYear"),
            "title": _clean(res.get("title", "")),
            "journal": res.get("journalTitle", ""),
            "authors": (res.get("authorString", "") or "")[:160],
            "abstract": _clean(res.get("abstractText", ""))[:3200],
            "doi": res.get("doi", ""),
        })
    return hits


def epmc_by_id(rid: str) -> list[dict]:
    return epmc(f'"{rid}"', fmt="core", size=1)


def zenodo_record(zid: str) -> list[dict]:
    data = json.loads(_get(f"https://zenodo.org/api/records/{zid}"))
    md = data.get("metadata", {})
    return [{
        "id": f"ZENODO:{data.get('id','')}",
        "year": (md.get("publication_date") or "")[:4],
        "title": _clean(md.get("title", "")),
        "journal": (md.get("journal") or {}).get("title", "")
        if isinstance(md.get("journal"), dict) else "",
        "authors": ", ".join(c.get("name", "")
                             for c in (md.get("creators") or [])[:6]),
        "abstract": _clean(md.get("description", ""))[:4200],
        "doi": data.get("doi", ""),
    }]


TASKS = {
    # F1: the REAL 3h-window paper
    "F1-nigericin": ("epmc", 'planarian nigericin regeneration polarity'),
    "F1-durant": ("epmc", 'Durant planarian bioelectric gradient editing'),
    "F1-3h": ("epmc", 'planarian amputation "hours" bioelectric anterior '
                      'posterior blastema potential double-headed'),
    "F1-bj2019": ("epmc", 'SRC:MED AND planarian AND "Biophysical Journal" '
                          'AND bioelectric'),
    # F2: directive's Zenodo deposits, fetched by ID
    "F2-sym-21459264": ("zenodo_id", "21459264"),
    "F2-geom-18358611": ("zenodo_id", "18358611"),
    # F3: full abstracts for verified anchors
    "F3-atlas-4D": ("epmc_id", "MED42172041"),
    "F3-TAS": ("epmc_id", "PPRPPR1216581"),
    "F3-neurobots": ("epmc_id", "MED41717829"),
    "F3-mem-synth": ("epmc_id", "PPRPPR1219439"),
    "F3-mtubules": ("epmc_id", "MED41099309"),
    "F3-gjb-2015": ("epmc_id", "MED26610482"),
    "F3-pietak2016": ("epmc_id", "MED27499881"),
    "F3-comp2022": ("epmc_id", "MED39372228"),
    "F3-topdown": ("epmc_id", "MED27807271"),
    "F3-mideas": ("epmc_id", "MED42183019"),
    # F4: notum/wnt1 primary timing
    "F4-notum": ("epmc", 'notum planarian head regeneration anterior '
                         'wound RNAi tails'),
    "F4-wnt1": ("epmc", 'wnt1 planarian wound expression posterior '
                        'regeneration RNAi ectopic heads'),
    # F5: arXiv retry (simpler), OpenAlex retry
    "F5-arxiv": ("arxiv", 'bioelectric regeneration morphogenesis'),
}


def arxiv(q: str) -> list[dict]:
    base = ("http://export.arxiv.org/api/query?search_query={q}"
            "&max_results=5&sortBy=relevance")
    xml = _get(base.format(q=urllib.parse.quote(q))).decode("utf-8", "replace")
    hits = []
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        tm = re.search(r"<title>(.*?)</title>", entry, re.S)
        sm = re.search(r"<summary>(.*?)</summary>", entry, re.S)
        im = re.search(r"<id>(.*?)</id>", entry, re.S)
        pm = re.search(r"<published>(\d{4})", entry)
        hits.append({
            "id": im.group(1).strip() if im else "arXiv:?",
            "year": pm.group(1) if pm else "",
            "title": _clean(tm.group(1))[:300] if tm else "",
            "journal": "arXiv", "authors": "", "doi": "",
            "abstract": _clean(sm.group(1))[:2400] if sm else "",
        })
    return hits


def run(task: str, spec: tuple[str, str]) -> list[dict]:
    kind, arg = spec
    if kind == "epmc":
        return epmc(arg)
    if kind == "epmc_id":
        return epmc_by_id(arg)
    if kind == "zenodo_id":
        return zenodo_record(arg)
    if kind == "arxiv":
        return arxiv(arg)
    raise ValueError(kind)


def main() -> None:
    print("=== exp53b: targeted verification pass ===\n")
    out: dict = {"exp": "exp53b_verification", "tasks": {}}
    md: list[str] = [
        "# Night-eight verification pass (targeted; part 2 of the wave)\n",
        f"Fetched {time.strftime('%Y-%m-%d %H:%M UTC')}.\n"]
    for key, spec in TASKS.items():
        print(f"  [{key}] {spec}")
        try:
            hits = run(key, spec)
        except Exception as e:                          # noqa: BLE001
            out["tasks"][key] = {"error": str(e)}
            md.append(f"\n## {key}\n\nERROR: {e}\n")
            continue
        out["tasks"][key] = {"hit_count": len(hits), "hits": hits}
        md.append(f"\n## {key} ({len(hits)} hits)\n")
        for h in hits:
            md.append(
                f"- **{h['year']}** {h['title']} — {h['journal']} "
                f"[{h['id']}" + (f" | doi:{h['doi']}" if h['doi'] else "")
                + f"]\n  - {h['abstract'][:1500]}\n")
        time.sleep(0.8)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(md))
    print(f"\nWrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
