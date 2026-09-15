#!/usr/bin/env python3
"""exp53c — final verification pass (part 3): corrected EXT_ID syntax +
the classic notum/wnt1 timing papers + the 3h paper's full abstract."""
from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "results", "exp53c_final.json")
OUT_MD = os.path.join(ROOT, "research", "NIGHT_EIGHT_FINAL.md")
UA = "bioelectric-cultivation/night8-final"


def _get(url: str, timeout: int = 30, retries: int = 3) -> bytes:
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:                          # noqa: BLE001
            last = e
            time.sleep(2.0 * (attempt + 1))
    raise last


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def epmc(q: str, size: int = 4) -> list[dict]:
    base = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
            "?query={q}&format=json&pageSize=%d&resultType=core" % size)
    data = json.loads(_get(base.format(q=urllib.parse.quote(q))))
    hits = []
    for res in data.get("resultList", {}).get("result", []):
        hits.append({
            "id": f"{res.get('source','')}{res.get('id','')}",
            "year": res.get("pubYear"),
            "title": _clean(res.get("title", "")),
            "journal": res.get("journalTitle", ""),
            "authors": (res.get("authorString", "") or "")[:200],
            "abstract": _clean(res.get("abstractText", ""))[:4200],
            "doi": res.get("doi", ""),
        })
    return hits


TASKS = {
    # THE 3h-window paper (full abstract — exp54's pre-registration basis)
    "P-3H-2019": ('EXT_ID:30799071', 1),
    # The directive-corrected anchors (full abstracts)
    "P-ATLAS4D": ('EXT_ID:42172041', 1),
    "P-TAS": ('EXT_ID:PPR1216581 AND SRC:PPR', 1),
    "P-NEUROBOTS": ('EXT_ID:41717829', 1),
    "P-MEMSYN": ('EXT_ID:PPR1219439 AND SRC:PPR', 1),
    "P-MTUB": ('EXT_ID:41099308', 1),
    # classic notum / wnt1 timing papers
    "P-NOTUM-CLASSIC": ('notum planarian anterior wound', 5),
    "P-WNT1-CLASSIC": ('wnt1 planarian wound regeneration polarity RNAi', 5),
    # GJ-blockade anomaly context (night-eight queue item 2)
    "P-GJB": ('EXT_ID:26610482', 1),
    "P-PIETAK": ('EXT_ID:27499881', 1),
    "P-COMP22": ('EXT_ID:39372228', 1),
}


def main() -> None:
    print("=== exp53c: final verification pass ===")
    out: dict = {"exp": "exp53c_final", "tasks": {}}
    md: list[str] = [
        "# Night-eight final verification (part 3)\n",
        f"Fetched {time.strftime('%Y-%m-%d %H:%M UTC')}.\n"]
    for key, (q, size) in TASKS.items():
        print(f"  [{key}] {q}")
        try:
            hits = epmc(q, size=size)
        except Exception as e:                          # noqa: BLE001
            out["tasks"][key] = {"error": str(e)}
            md.append(f"\n## {key}\n\nERROR: {e}\n")
            continue
        out["tasks"][key] = {"query": q, "hit_count": len(hits), "hits": hits}
        md.append(f"\n## {key} — `{q}` ({len(hits)} hits)\n")
        for h in hits:
            md.append(
                f"- **{h['year']}** {h['title']} — {h['journal']} "
                f"[{h['id']}" + (f" | doi:{h['doi']}" if h['doi'] else "")
                + f"]\n  - {h['abstract'][:2000]}\n")
        time.sleep(0.8)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(md))
    print(f"Wrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
