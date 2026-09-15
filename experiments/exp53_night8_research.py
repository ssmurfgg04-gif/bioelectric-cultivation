#!/usr/bin/env python3
"""exp53 (night-eight, phase 0) — RESEARCH WAVE, MULTI-SOURCE.

User directive: "research directive first ... europe pmc is good but theres
more". This wave broadens the source set beyond Europe PMC (exp44) to six
free, key-less scholarly APIs, with per-source backoff and graceful
degradation:

  S1 Europe PMC REST       (proven channel, nights 4-7)
  S2 PubMed E-utilities    (esummary — verifies specific PMIDs, e.g. the
                            3h-window paper the directive names)
  S3 Crossref              (DOI verification, e.g. the M-L intercalation DOI)
  S4 arXiv API             (physics-of-morphogenesis / quantitative models)
  S5 OpenAlex              (broad scholarly index incl. preprints; polite
                            pool with mailto)
  S6 Zenodo REST           (the directive's 2026 grey-literature deposits)

PRE-REGISTERED ITEM -> QUERY MAP (before any fetch; the night-eight queue
plus the user directive's research-grounded build plan):

  V-WIN-3H   the 3-hour critical window: bioelectric state at 3h
             post-amputation decides A/P polarity (nigericin 3h-washout ->
             indistinguishable blastema depolarization at 6h -> double-head)
  V-WIN-6H   the write deadline: wnt1 generic at all wounds by ~6h; notum
             anterior-preferential by ~6h; notum RNAi -> tail; wnt1 RNAi ->
             ectopic heads  (Reddien-lab timing sequence)
  V-ML-INT   mediolateral intercalation / symmetry hypothesis: two
             independent positional fields; midline graft laterally ->
             complete ectopic head (Saito; graft literature)
  V-ARZ      the anterior regenerative zone as a spatial DOMAIN (multi-
             lineage convergence at the wound-proximal region; Mediator8)
  V-UNDM     underdamped recovery: positional-control-gene dynamics
             overshoot/oscillate before settling
  V-GEOM     coupling response geometry: fixed structural form (saturation
             plateau, onset point, finite transition width); late
             perturbations fail regardless of strength
  V-SYM      symbol grounding: meaning sits in the READER not the carrier;
             the decisive test is perturb-the-reader-hold-the-pattern
  V-TAS      tangential action spaces: bioelectric memory as a geometric,
             costed, testable object (hidden-state model to compare M28
             phi-layer semantics against)
  V-NEURO    neurobots / memory in synthetic living constructs (Levin-lab
             2026: designed constructs carrying stimulus-specific memory —
             the wet-lab anchor for M31-A stored-state minting)

Output: results/exp53_night8_research.json + research/NIGHT_EIGHT_RESEARCH.md
(raw hits per query, every hit stamped with its source) — the synthesis and
the build directives are then pieced together in
research/NIGHT_EIGHT_SYNTHESIS.md AFTER reading the raw results.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "results", "exp53_night8_research.json")
OUT_MD = os.path.join(ROOT, "research", "NIGHT_EIGHT_RESEARCH.md")
UA = "bioelectric-cultivation/night8-research (contact: research agent)"


# --------------------------------------------------------------- source APIs
def _get(url: str, timeout: int = 30, retries: int = 3) -> bytes:
    """GET with polite backoff; raises last error after retries."""
    last: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:                          # noqa: BLE001
            last = e
            time.sleep(2.0 * (attempt + 1))             # polite backoff
    assert last is not None
    raise last


def src_europepmc(q: str) -> list[dict]:
    base = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
            "?query={q}&format=json&pageSize=5&resultType=core")
    data = json.loads(_get(base.format(q=urllib.parse.quote(q))))
    hits = []
    for res in data.get("resultList", {}).get("result", []):
        hits.append({
            "id": f"{res.get('source','')}{res.get('id','')}",
            "year": res.get("pubYear"),
            "title": _clean(res.get("title", "")),
            "journal": res.get("journalTitle", "") or res.get("bookOrReportDetails", {}).get("publisher", ""),
            "authors": (res.get("authorString", "") or "")[:160],
            "abstract": _clean(res.get("abstractText", ""))[:2400],
            "doi": res.get("doi", ""),
        })
    return hits


def src_pubmed(pmid: str) -> list[dict]:
    base = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            "?db=pubmed&id={q}&retmode=json")
    data = json.loads(_get(base.format(q=urllib.parse.quote(pmid))))
    res = data.get("result", {})
    out = []
    for uid in res.get("uids", []):
        doc = res.get(uid, {})
        out.append({
            "id": f"PMID:{uid}",
            "year": doc.get("pubdate", "")[:4],
            "title": _clean(doc.get("title", "")),
            "journal": doc.get("source", ""),
            "authors": ", ".join(a.get("name", "") for a in doc.get("authors", [])[:6]),
            "abstract": "(esummary record — no abstract field; title+journal carry the verification)",
            "doi": next((x["value"] for x in doc.get("articleids", [])
                         if x.get("idtype") == "doi"), ""),
        })
    return out


def src_crossref(doi: str) -> list[dict]:
    base = "https://api.crossref.org/works/{q}"
    data = json.loads(_get(base.format(q=urllib.parse.quote(doi))))
    m = data.get("message", {})
    date = (m.get("issued", {}).get("date-parts") or [[None]])[0]
    return [{
        "id": f"DOI:{m.get('DOI', doi)}",
        "year": date[0],
        "title": _clean(" ".join(m.get("title", []) or [])),
        "journal": (m.get("container-title") or [""])[0],
        "authors": ", ".join(
            f"{a.get('given','')} {a.get('family','')}".strip()
            for a in m.get("author", [])[:6]),
        "abstract": _clean(m.get("abstract", "") or
                           "(crossref record — no abstract deposited)"),
        "doi": m.get("DOI", doi),
    }]


def src_arxiv(q: str) -> list[dict]:
    base = ("http://export.arxiv.org/api/query?search_query={q}"
            "&max_results=5&sortBy=relevance")
    xml = _get(base.format(q=urllib.parse.quote(q))).decode("utf-8", "replace")
    hits = []
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        title = _clean(re.search(r"<title>(.*?)</title>", entry, re.S).group(1)) \
            if re.search(r"<title>(.*?)</title>", entry, re.S) else ""
        summary = _clean(re.search(r"<summary>(.*?)</summary>", entry, re.S).group(1)) \
            if re.search(r"<summary>(.*?)</summary>", entry, re.S) else ""
        link = re.search(r"<id>(.*?)</id>", entry, re.S)
        pub = re.search(r"<published>(\d{4})", entry)
        hits.append({
            "id": link.group(1).strip() if link else "arXiv:?",
            "year": pub.group(1) if pub else "",
            "title": title[:300],
            "journal": "arXiv",
            "authors": "",
            "abstract": summary[:2400],
            "doi": "",
        })
    return hits


def src_openalex(q: str) -> list[dict]:
    base = ("https://api.openalex.org/works?search={q}&per-page=5"
            "&mailto=bioelectric-cultivation@example.org")
    data = json.loads(_get(base.format(q=urllib.parse.quote(q))))
    hits = []
    for w in data.get("results", []):
        venue = ""
        prim = w.get("primary_location") or {}
        src = prim.get("source") or {}
        venue = src.get("display_name", "") or ""
        hits.append({
            "id": w.get("id", "").replace("https://openalex.org/", "OA:"),
            "year": w.get("publication_year"),
            "title": _clean(w.get("title") or ""),
            "journal": venue,
            "authors": ", ".join(
                a.get("author", {}).get("display_name", "")
                for a in (w.get("authorships") or [])[:6]),
            "abstract": _abstract_oa(w),
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        })
    return hits


def _abstract_oa(w: dict) -> str:
    """OpenAlex stores abstracts as inverted index — rebuild it."""
    inv = w.get("abstract_inverted_index")
    if not inv:
        return "(no abstract indexed)"
    pos: dict[int, str] = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    text = " ".join(pos[i] for i in sorted(pos))
    return text[:2400]


def src_zenodo(q: str) -> list[dict]:
    base = "https://zenodo.org/api/records?q={q}&size=5&sort=bestmatch"
    data = json.loads(_get(base.format(q=urllib.parse.quote(q))))
    hits = []
    for h in data.get("hits", {}).get("hits", []):
        md = h.get("metadata", {})
        hits.append({
            "id": f"ZENODO:{h.get('id','')}",
            "year": (md.get("publication_date") or "")[:4],
            "title": _clean(md.get("title", "")),
            "journal": md.get("journal", {}).get("title", "") if isinstance(md.get("journal"), dict) else "",
            "authors": ", ".join(
                c.get("name", "") for c in (md.get("creators") or [])[:6]),
            "abstract": _clean(md.get("description", ""))[:2400],
            "doi": h.get("doi", ""),
        })
    return hits


SOURCES = {
    "europepmc": src_europepmc,
    "pubmed": src_pubmed,
    "crossref": src_crossref,
    "arxiv": src_arxiv,
    "openalex": src_openalex,
    "zenodo": src_zenodo,
}


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


# ----------------------------------------------------------------- query map
# each item: (label, [(source, query-or-id), ...])
ITEMS = {
    "V-WIN-3H": ("the 3-hour critical window (nigericin washout protocol)", [
        ("pubmed", "30824103"),
        ("europepmc", 'planarian bioelectric "3 h" post-amputation polarity '
                      'nigericin blastema depolarization'),
        ("openalex", "planarian regeneration bioelectric three hours "
                     "amputation polarity nigericin"),
    ]),
    "V-WIN-6H": ("the 6h write deadline (wnt1 generic / notum anterior timing)", [
        ("europepmc", 'planarian wnt1 expressed all wounds six hours injury'),
        ("europepmc", 'planarian notum anterior wounds expression timing '
                      'regeneration polarity RNAi tail'),
        ("openalex", "planarian wound-induced gene expression kinetics "
                     "wnt notum hours"),
    ]),
    "V-ML-INT": ("mediolateral intercalation / graft representation", [
        ("crossref", "10.1002/dvdy.10246"),
        ("europepmc", 'planarian graft mediolateral intercalation ectopic '
                      'head lateral implantation'),
        ("openalex", "planarian tissue intercalation positional values "
                     "left right axis graft"),
    ]),
    "V-ARZ": ("anterior regenerative zone as a spatial domain", [
        ("europepmc", 'planarian injury-induced anterior regenerative zone '
                      'positional signals lineage'),
        ("europepmc", 'planarian wound-proximal region multi-lineage '
                      'convergence blastema formation regulator'),
        ("openalex", "anterior regenerative zone planarian single-cell "
                     "atlas injury"),
    ]),
    "V-UNDM": ("underdamped positional-control-gene recovery", [
        ("europepmc", 'planarian positional control gene expression '
                      'dynamics recovery oscillation overshoot'),
        ("openalex", "planarian regeneration gene expression time series "
                     "dynamics oscillation wound"),
    ]),
    "V-GEOM": ("coupling response geometry (fixed structural form)", [
        ("europepmc", 'bioelectric perturbation response saturation '
                      'transition width regeneration polarity strength'),
        ("arxiv", 'all:"bioelectric" AND all:"regeneration" AND '
                  'all:"response"'),
        ("openalex", "coupling response geometry regeneration polarity "
                     "perturbation strength exposure"),
        ("zenodo", "bioelectric regeneration coupling response geometry"),
    ]),
    "V-SYM": ("symbol grounding — reader, not carrier", [
        ("zenodo", "developmental bioelectricity syntax semantics "
                   "inspection spaces"),
        ("europepmc", 'bioelectric pattern memory reader semantics '
                      'morphogenesis Levin'),
        ("openalex", "symbol grounding morphogenesis bioelectric code"),
    ]),
    "V-TAS": ("tangential action spaces (geometric memory model)", [
        ("europepmc", 'tangential action spaces bioelectric memory '
                      'geometric model regeneration'),
        ("openalex", "tangential action spaces bioelectric memory"),
        ("zenodo", "tangential action spaces bioelectric memory"),
    ]),
    "V-NEURO": ("neurobots / synthetic-construct memory (wet-lab anchors)", [
        ("europepmc", 'neurobots living robots self-organized nervous '
                      'system frog cells'),
        ("europepmc", 'xenobots memory synthetic living constructs '
                      'stimulus-specific non-neural'),
        ("openalex", "synthetic living constructs memory xenobot "
                     "bioelectric"),
    ]),
    "V-Q8ANOM": ("gjblock|head_tail both-faces anomaly (night-eight queue)", [
        ("europepmc", 'planarian gap junction blockade both anterior '
                      'posterior amputation double phenotype frequency'),
    ]),
}


def main() -> None:
    print("=== exp53: night-eight research wave (6 sources) ===\n")
    out: dict = {"exp": "exp53_night8_research",
                 "sources": list(SOURCES.keys()),
                 "items": {}}
    md: list[str] = [
        "# Night-eight research wave (multi-source: Europe PMC, PubMed, "
        "Crossref, arXiv, OpenAlex, Zenodo)\n",
        "Executed per the standing research directive — broadened past "
        "Europe PMC ('europe pmc is good but theres more'). Every hit "
        "stamped with its source. Fetched "
        f"{time.strftime('%Y-%m-%d %H:%M UTC')}.\n",
    ]
    n_hits = 0
    n_err = 0
    for key, (label, calls) in ITEMS.items():
        print(f"  [{key}] {label}")
        md.append(f"\n## {key} — {label}\n")
        entry: dict = {"label": label, "calls": {}}
        for source, query in calls:
            tag = f"{source}::{query[:60]}"
            print(f"      {tag}")
            try:
                hits = SOURCES[source](query)
            except Exception as e:                      # noqa: BLE001
                entry["calls"][tag] = {"error": str(e)}
                md.append(f"\n### {source} — `{query}`\n\nERROR: {e}\n")
                n_err += 1
                continue
            entry["calls"][tag] = {"hit_count": len(hits), "hits": hits}
            n_hits += len(hits)
            md.append(f"\n### {source} — `{query}` ({len(hits)} hits)\n")
            for h in hits:
                md.append(
                    f"- **{h['year']}** {h['title']} — {h['journal']} "
                    f"[{h['id']}" + (f" | doi:{h['doi']}" if h['doi'] else "")
                    + f"]\n  - {h['abstract'][:900]}\n")
            time.sleep(0.8)                             # politeness gap
        out["items"][key] = entry
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(md))
    print(f"\nWrote {OUT_JSON} and {OUT_MD}")
    print(f"Total hits: {n_hits}; source errors: {n_err} "
          f"(each error retried 3x with backoff)")
    return 0 if n_hits > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
