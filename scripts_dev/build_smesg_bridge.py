#!/usr/bin/env python3
"""Build the dd_Smed_v6 -> SMESG gene-ID bridge for PRISTA4D ingestion.

Source: planosphere Rosetta Stone 2020 (smed_20140614.mapping.rosettastone.2020),
mirrored as a GitHub release asset of neurogenomics/orthogene (v1.1.1).
Structure: ref_id (SMED300) <-> seq_id <-> transcriptome_id, where
transcriptome_id in {dd_Smed_v6, SMESG_dd_Smes_v2, ...}.

Bridge: dd_Smed_v6 --(ref_id SMED300)--> SMESG_dd_Smes_v2.
Applied to the curated ion-transporter families from exp18
(research/data/psca/gene_mining/curated_ion_genes.json).

Output: research/data/gene_mapping/ion_genes_smesg.json
"""
import gzip
import json
import os

ROOT = "/home/z/my-project/bioelectric-cultivation"
RS = os.path.join(ROOT, "research/data/gene_mapping/rosettastone_2020.txt.gz")
CUR = os.path.join(ROOT, "research/data/psca/gene_mining/curated_ion_genes.json")
OUT = os.path.join(ROOT, "research/data/gene_mapping/ion_genes_smesg.json")


def main():
    # 1. ref_id -> dd_v6 and ref_id -> SMESG
    ref2v6, ref2smesg = {}, {}
    with gzip.open(RS, "rt") as f:
        header = f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) != 3:
                continue
            ref, seq, tid = p
            if tid == "dd_Smed_v6":
                ref2v6[ref] = seq
            elif tid == "SMESG_dd_Smes_v2":
                ref2smesg[ref] = seq
    print(f"rosetta: {len(ref2v6)} dd_v6, {len(ref2smesg)} SMESG entries")

    # 2. dd_v6 -> SMESG via shared ref
    v6_to_smesg = {}
    for ref, v6 in ref2v6.items():
        if ref in ref2smesg:
            v6_to_smesg.setdefault(v6, set()).add(ref2smesg[ref])
    print(f"dd_v6 -> SMESG: {len(v6_to_smesg)} genes bridged")

    # 3. apply to curated families
    cur = json.load(open(CUR))
    fams = cur["families"]
    out_fams, stats = {}, {}
    for fam, genes in fams.items():
        mapped, unmapped = [], []
        for g in genes:
            sm = v6_to_smesg.get(g["dd_id"])
            if sm:
                mapped.append({"dd_id": g["dd_id"], "smesg": sorted(sm),
                               "smed300": g.get("smed300", []),
                               "desc": g.get("desc", "")})
            else:
                unmapped.append(g["dd_id"])
        out_fams[fam] = mapped
        stats[fam] = {"n": len(genes), "mapped": len(mapped),
                      "unmapped": len(unmapped)}
    print("\nfamily coverage (dd_v6 -> SMESG):")
    for fam, s in sorted(stats.items()):
        pct = 100 * s["mapped"] / max(1, s["n"])
        print(f"  {fam:18s} {s['mapped']:4d}/{s['n']:4d} ({pct:.0f}%)")
    tot = sum(s["n"] for s in stats.values())
    mtot = sum(s["mapped"] for s in stats.values())
    print(f"  {'TOTAL':18s} {mtot}/{tot} ({100*mtot/tot:.0f}%)")

    with open(OUT, "w") as f:
        json.dump({"source": "planosphere rosettastone 2020 via "
                             "neurogenomics/orthogene release v1.1.1",
                   "bridge": "dd_Smed_v6 -> ref_id(SMED300) -> "
                             "SMESG_dd_Smes_v2",
                   "families": out_fams, "stats": stats}, f, indent=1)
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
