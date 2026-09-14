#!/usr/bin/env python3
"""exp18 — THE PSCA INGEST: the first real-data test of the vmem_inference
layer (V1-V4 falsifiable predictions) on two public planarian atlases.

DATA (all public, downloaded this session):
  PSCA   (Plass/Rajewsky 2018): 21,612 cells x 28,066 genes  (raw counts)
  Fincher (Fincher/Reddien 2018, GSE111764): 50,456 cells x 26,561 genes

GENE-ID MAPPING (the missing piece solved this session):
  dd_Smed_v6 -> SMED300 (planosphere Rosetta Stone May2024)
  SMED300 -> functional annotation (planosphere AHRD 2020)
  -> curated ion-transporter families (curated_ion_genes.json; validated
     3/3 vs PMC12421698 Smed-TRPM-a1/a2/c)

PIPELINE:
  1. stream each atlas matrix gene-by-gene
  2. accumulate per-(class, cell-type) counts + per-type totals
  3. aggregate CP10K -> log1p -> global 0..1 scaling
  4. GHK resting potential per cell type (vmem_inference.infer_vmem)
  5. pre-registered checks V1-V4 (+ cross-atlas consistency + weight
     jackknife robustness)

Pre-registered criteria (from vmem_inference.PUBLISHED_PREDICTIONS):
  V1 neoblasts among most hyperpolarized (rank <= 30% percentile of types)
  V2 muscle hyperpolarized (Vm < median) AND pump expression > median
  V3 phagocyte depolarized (rank >= 70%) AND cation-leak (trp/p2x/fana)
     expression in phagocyte top-3
  V4 innexin does NOT predict own-Vm (|Spearman| < 0.35) AND innexin
     top-3 includes a known coupled tissue (muscle / neoblast / pharynx)
"""
from __future__ import annotations

import gzip
import json
import os
import re
import sys
import warnings
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cultivation.validation import vmem_inference as VI   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSCA_DIR = os.path.join(ROOT, "research", "data", "psca")
FIN_DIR = os.path.join(ROOT, "research", "data", "fincher")
GENE_MINING = os.path.join(PSCA_DIR, "gene_mining")
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)

# classes that enter the GHK permeability model (innexin excluded -> V4)
VM_CLASSES = ["k_channel_leak", "kv_channel", "k_ca_channel", "nak_atpase",
              "hk_atpase", "fana_nav", "nav_channel", "trp_cation",
              "p2x_purinergic", "cl_channel", "hvcn"]


# ------------------------------------------------------------- cell groups
def group_psca(ctype: str) -> str:
    c = ctype.lower()
    if "neoblast" in c:
        return "neoblast"
    if "muscle" in c:
        return "muscle"
    if any(k in c for k in ("neuron", "neural", "chat", "gaba", "seroton",
                            "octopam", "glutamat", "dopamin", "photo",
                            "opsin")):
        return "neural"
    if "phagocyt" in c:
        return "phagocyte"
    if "epiderm" in c:
        return "epidermis"
    if any(k in c for k in ("gut", "goblet", "pharynx", "intestin")):
        return "gut/pharynx"
    if any(k in c for k in ("secretory", "gland")):
        return "secretory"
    if "parenchymal" in c:
        return "parenchymal"
    if "pigment" in c:
        return "pigment"
    return "other"


def group_fincher(ctype: str) -> str:
    c = ctype.lower()
    if "neoblast" in c:
        return "neoblast"
    if "muscle" in c:
        return "muscle"
    if any(k in c for k in ("neuron", "neural", "chat", "gaba", "seroton",
                            "octopam", "glutamat", "dopamin", "photo",
                            "opsin")):
        return "neural"
    if any(k in c for k in ("phagocyt", "cathepsin")):   # Cathepsin+ cells =
        return "phagocyte"                                 # macrophage-like
    if "epiderm" in c or "epithelial" in c:
        return "epidermis"
    if any(k in c for k in ("gut", "goblet", "pharynx", "intestin",
                            "parapharyngeal")):
        return "gut/pharynx"
    if any(k in c for k in ("secretory", "gland")):
        return "secretory"
    if "parenchym" in c:
        return "parenchymal"
    if "pigment" in c:
        return "pigment"
    return "other"


# ------------------------------------------------------------ ingest core
def load_curated():
    """class -> {4-part dd ids}; also 3-part union lookup."""
    with open(os.path.join(GENE_MINING, "curated_ion_genes.json")) as f:
        cur = json.load(f)
    by_class = {c: [g["dd_id"] for g in genes]
                for c, genes in cur["families"].items()}
    lookup4 = defaultdict(set)     # 4-part id -> classes
    lookup3 = defaultdict(set)     # 3-part id -> classes (union over isoforms)
    for cls, ids in by_class.items():
        for gid in ids:
            lookup4[gid].add(cls)
            base = gid.rsplit("_", 1)[0] if gid.count("_") >= 3 else gid
            lookup3[base].add(cls)
    return by_class, dict(lookup4), dict(lookup3), cur


def stream_atlas(dge_path, types, lookup, n_types):
    """Stream a (genes x cells) raw count matrix; accumulate per-(class,type)
    counts and per-type totals. `types`: np.array type-index per column."""
    class_counts = defaultdict(lambda: np.zeros(n_types))
    type_totals = np.zeros(n_types)
    n_rows = 0
    matched = 0
    with gzip.open(dge_path, "rt") as f:
        header = f.readline()  # cell names (column labels) — order per annot
        for line in f:
            if not line.strip():
                continue
            tab = line.find("\t")
            if tab < 0:
                continue
            gene = line[:tab].strip()
            if gene.startswith("d_Smed") and not gene.startswith("dd_Smed"):
                gene = "d" + gene  # Fincher has a 'd_Smed...' typo row
            rest = line[tab + 1:]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    counts = np.fromstring(rest, dtype=np.float64, sep="\t")
                except Exception:
                    continue
            n_rows += 1
            if counts.size != types.size:
                continue
            type_totals += np.bincount(types, weights=counts,
                                       minlength=n_types)
            classes = lookup.get(gene)
            if classes:
                matched += 1
                for cls in classes:
                    class_counts[cls] += np.bincount(types, weights=counts,
                                                     minlength=n_types)
    return class_counts, type_totals, n_rows, matched


def atlas_expression(class_counts, type_totals, classes):
    """aggregate CP10K -> log1p -> FIXED global scaling.

    Scaling uses the SAME constant for every atlas (K = log1p(100): a family
    at 1% of a type's transcriptome scores 1.0), so permeability ratios and
    predicted Vm are directly comparable across atlases (the v1
    atlas-specific max-normalizer compressed Fincher's map)."""
    K = float(np.log1p(100.0))
    raw = {}
    for cls in classes:
        if cls in class_counts:
            raw[cls] = class_counts[cls] / np.maximum(type_totals, 1.0) * 1e4
    expr = {cls: np.log1p(v) / K for cls, v in raw.items()}
    return expr, K


def build_matrix(expr, classes, group_names):
    """{cell type: {gene class: level 0..1}} for vmem_inference."""
    mat = {}
    for ti, gname in enumerate(group_names):
        mat[gname] = {cls: float(expr[cls][ti])
                      for cls in classes if cls in expr}
    return mat


# ---------------------------------------------------------------- checks
def spearman(a, b):
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def run_checks(vm, expr, groups):
    """V1-V4 pre-registered checks. vm: {group: mV}; expr: {class: array}."""
    order = sorted(vm.items(), key=lambda kv: kv[1])  # hyperpol -> depol
    rank_of = {g: i + 1 for i, (g, _) in enumerate(order)}
    n = len(order)
    res = {}

    # V1 — neoblast among most hyperpolarized
    nb_rank = rank_of.get("neoblast")
    v1_pass = nb_rank is not None and nb_rank <= max(1, int(np.ceil(0.3 * n)))
    res["V1"] = {"rank": nb_rank, "n": n, "pass": bool(v1_pass),
                 "criterion": "neoblast rank <= 30% percentile"}

    # V2 — muscle hyperpolarized + pump-high
    vms = np.array([vm[g] for g in vm])
    med = float(np.median(vms))
    pump = expr.get("nak_atpase", np.zeros(n))
    pump_med = float(np.median(pump))
    mus_idx = groups.index("muscle") if "muscle" in groups else None
    v2a = vm.get("muscle", 1e9) < med
    v2b = mus_idx is not None and pump[mus_idx] > pump_med
    res["V2"] = {"muscle_Vm": vm.get("muscle"), "median_Vm": med,
                 "muscle_pump": float(pump[mus_idx]) if mus_idx is not None else None,
                 "pump_median": pump_med,
                 "hyperpolarized": bool(v2a), "pump_high": bool(v2b),
                 "pass": bool(v2a and v2b),
                 "criterion": "muscle Vm < median AND pump expr > median"}

    # V3 — phagocyte depolarized + cation-leak-high
    ph_rank = rank_of.get("phagocyte")
    v3a = ph_rank is not None and ph_rank >= int(np.floor(0.7 * n))
    cation = (expr.get("trp_cation", np.zeros(n))
              + expr.get("p2x_purinergic", np.zeros(n))
              + expr.get("fana_nav", np.zeros(n)))
    top3 = list(np.argsort(cation)[::-1][:3])
    ph_idx = groups.index("phagocyte") if "phagocyte" in groups else None
    v3b = ph_idx is not None and ph_idx in top3
    res["V3"] = {"rank": ph_rank, "n": n, "depolarized": bool(v3a),
                 "phagocyte_cation_rank": (int(np.argsort(np.argsort(cation))
                                               [ph_idx]) + 1) if ph_idx is not None else None,
                 "top3_cation_types": [groups[i] for i in top3],
                 "pass": bool(v3a and v3b),
                 "criterion": "phagocyte rank >= 70% AND cation-leak top-3"}

    # V4 — innexin does NOT set own Vm + concentrated in coupled tissues
    inx = expr.get("innexin", np.zeros(n))
    vm_arr = np.array([vm[g] for g in sorted(vm)])
    inx_arr = np.array([inx[groups.index(g)] for g in sorted(vm)])
    rho = spearman(inx_arr, vm_arr)
    inx_top3 = [groups[i] for i in np.argsort(inx_arr)[::-1][:3]]
    coupled = {"muscle", "neoblast", "gut/pharynx"}
    v4a = abs(rho) < 0.35
    v4b = bool(set(inx_top3) & coupled)
    res["V4"] = {"spearman_innexin_vm": rho, "innexin_top3": inx_top3,
                 "no_own_vm_effect": bool(v4a), "coupled_tissue_hit": v4b,
                 "pass": bool(v4a and v4b),
                 "criterion": "|rho| < 0.35 AND top-3 in coupled tissues "
                              "(Oviedo 2009 muscle / Nogi 2007 neoblast inx-11)"}
    return res


def main():
    print("=== exp18: PSCA + Fincher ingest -> V1-V4 real-data checks ===\n")
    by_class, lookup4, lookup3, cur = load_curated()
    print(f"curated families: " +
          ", ".join(f"{c}={len(v)}" for c, v in sorted(by_class.items())))

    # ---------------- PSCA ----------------
    print("\n[PSCA] loading cell annotations...")
    with open(os.path.join(PSCA_DIR, "R_annotation.txt")) as f:
        psca_types_raw = [ln.strip() for ln in f if ln.strip()]
    psca_groups_raw = [group_psca(t) for t in psca_types_raw]
    group_names = sorted(set(psca_groups_raw))
    gidx = {g: i for i, g in enumerate(group_names)}
    psca_tidx = np.array([gidx[g] for g in psca_groups_raw])
    print(f"  {len(psca_types_raw)} cells -> {len(group_names)} groups: "
          f"{group_names}")
    comp = defaultdict(int)
    for g in psca_groups_raw:
        comp[g] += 1
    print(f"  group sizes: {dict(comp)}")

    print("[PSCA] streaming dge matrix (28,066 genes x 21,612 cells)...")
    cc_psca, tot_psca, rows, matched = stream_atlas(
        os.path.join(PSCA_DIR, "dge.txt.gz"), psca_tidx, lookup3,
        len(group_names))
    print(f"  rows={rows} curated-gene rows matched={matched}")
    expr_psca, L_psca = atlas_expression(cc_psca, tot_psca,
                                         VM_CLASSES + ["innexin"])
    mat_psca = build_matrix(expr_psca, VM_CLASSES, group_names)
    vm_psca = {g: d["Vm_mV"] for g, d in VI.infer_vmem(mat_psca).items()}

    # ---------------- Fincher ----------------
    print("\n[Fincher] loading cell annotations...")
    fin_types_raw = []
    with open(os.path.join(FIN_DIR, "fincher_annotation.txt")) as f:
        next(f)
        for ln in f:
            p = ln.rstrip("\n").split("\t")
            if len(p) >= 4:
                ct = p[2]                       # Celltype: C{N}_{Name}
                fin_types_raw.append(re.sub(r"^C\d+_", "", ct))
    fin_groups_raw = [group_fincher(t) for t in fin_types_raw]
    fin_group_names = sorted(set(fin_groups_raw))
    fgidx = {g: i for i, g in enumerate(fin_group_names)}
    fin_tidx = np.array([fgidx[g] for g in fin_groups_raw])
    print(f"  {len(fin_types_raw)} cells -> {len(fin_group_names)} groups: "
          f"{fin_group_names}")
    comp = defaultdict(int)
    for g in fin_groups_raw:
        comp[g] += 1
    print(f"  group sizes: {dict(comp)}")

    print("[Fincher] streaming dge matrix (26,561 genes x 50,456 cells)...")
    cc_fin, tot_fin, rows, matched = stream_atlas(
        os.path.join(FIN_DIR, "fincher_dge.txt.gz"), fin_tidx, lookup4,
        len(fin_group_names))
    print(f"  rows={rows} curated-gene rows matched={matched}")
    expr_fin, L_fin = atlas_expression(cc_fin, tot_fin,
                                       VM_CLASSES + ["innexin"])
    mat_fin = build_matrix(expr_fin, VM_CLASSES, fin_group_names)
    vm_fin = {g: d["Vm_mV"] for g, d in VI.infer_vmem(mat_fin).items()}

    # ---------------- report ----------------
    print("\n=== predicted Vmem map (PSCA, real data) ===")
    for g, v in sorted(vm_psca.items(), key=lambda kv: kv[1]):
        print(f"  {g:14s} {v:7.1f} mV")
    print("\n=== predicted Vmem map (Fincher, real data) ===")
    for g, v in sorted(vm_fin.items(), key=lambda kv: kv[1]):
        print(f"  {g:14s} {v:7.1f} mV")

    # cross-atlas consistency
    common = sorted(set(vm_psca) & set(vm_fin))
    x = np.array([vm_psca[g] for g in common])
    y = np.array([vm_fin[g] for g in common])
    cross = spearman(x, y)
    pearson = float(np.corrcoef(x, y)[0, 1])
    print(f"\ncross-atlas (PSCA vs Fincher) on {len(common)} common types: "
          f"Spearman rho={cross:.3f}, Pearson r={pearson:.3f}")

    # V1-V4 per atlas
    checks_psca = run_checks(vm_psca, expr_psca, group_names)
    checks_fin = run_checks(vm_fin, expr_fin, fin_group_names)
    for name, checks in (("PSCA", checks_psca), ("Fincher", checks_fin)):
        print(f"\n--- {name} V1-V4 ---")
        for vid, r in checks.items():
            extra = {k: v for k, v in r.items()
                     if k not in ("pass", "criterion")}
            print(f"  {vid}: {'PASS' if r['pass'] else 'FAIL'}  {extra}")

    # weight jackknife: +-30% random multiplicative perturbations
    print("\n[robustness] weight jackknife (20 draws, +-30%)...")
    rng = np.random.default_rng(18)
    base_w = dict(VI.GENE_WEIGHTS)
    stab = {"PSCA": defaultdict(int), "Fincher": defaultdict(int)}
    for draw in range(20):
        pert = {k: (c, w * float(rng.uniform(0.7, 1.3)))
                for k, (c, w) in base_w.items()}
        VI.GENE_WEIGHTS = pert
        for name, mat in (("PSCA", mat_psca), ("Fincher", mat_fin)):
            vm = {g: d["Vm_mV"] for g, d in VI.infer_vmem(mat).items()}
            if name == "PSCA":
                ch = run_checks(vm, expr_psca, group_names)
            else:
                ch = run_checks(vm, expr_fin, fin_group_names)
            for vid, r in ch.items():
                stab[name][vid] += int(r["pass"])
    VI.GENE_WEIGHTS = base_w
    for name in stab:
        print(f"  {name}: " + ", ".join(f"{v}={stab[name][v]}/20"
                                       for v in ("V1", "V2", "V3", "V4")))

    # ---------------- save ----------------
    out = {
        "experiment": "exp18_psca_ingest",
        "data": {
            "PSCA": {"cells": int(psca_tidx.size), "genes": 28066,
                     "source": "shiny.mdc-berlin.de/psca dge.txt.gz "
                               "(Plass/Rajewsky 2018)"},
            "Fincher": {"cells": int(fin_tidx.size), "genes": 26561,
                        "source": "bis.zju.edu.cn GSE111764 mirror "
                                  "(Fincher/Reddien 2018 Science)"},
            "gene_mapping": "planosphere rosettastone_May2024 + AHRD 2020; "
                            "TRPM validation 3/3 vs PMC12421698",
        },
        "curated_gene_counts": {c: len(v) for c, v in by_class.items()},
        "vm_map_mV": {"PSCA": vm_psca, "Fincher": vm_fin},
        "class_expression": {
            "PSCA": {c: [float(x) for x in v] for c, v in expr_psca.items()},
            "Fincher": {c: [float(x) for x in v] for c, v in expr_fin.items()},
        },
        "groups": {"PSCA": group_names, "Fincher": fin_group_names},
        "checks": {"PSCA": checks_psca, "Fincher": checks_fin},
        "cross_atlas": {"common_types": common, "spearman": cross,
                        "pearson": pearson},
        "jackknife_stability": {n: dict(v) for n, v in stab.items()},
    }
    path = os.path.join(RESULTS, "exp18_psca_ingest.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nsaved {path}")

    # figure
    try:
        make_figure(out, expr_psca, expr_fin, group_names, fin_group_names,
                    vm_psca, vm_fin)
    except Exception as e:  # noqa: BLE001
        print(f"figure failed (non-fatal): {e}")


# ------------------------------------------------------------------ figure
def make_figure(out, expr_p, expr_f, groups_p, groups_f, vm_p, vm_f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.font_manager as fm
    for fp in ("/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(fp):
            fm.fontManager.addfont(fp)
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5), constrained_layout=True)

    # (a) Vm maps
    ax = axes[0, 0]
    gp = sorted(vm_p.items(), key=lambda kv: kv[1])
    names = [g for g, _ in gp] + ["--"] + \
        [g for g, _ in sorted(vm_f.items(), key=lambda kv: kv[1])]
    vals = [v for _, v in gp] + [np.nan] + \
        [v for _, v in sorted(vm_f.items(), key=lambda kv: kv[1])]
    colors = ["#2c7fb8"] * len(gp) + ["k"] + ["#41b6c4"] * len(vm_f)
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(names, rotation=60, ha="right", fontsize=7)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel("predicted Vmem (mV)")
    ax.set_title("(a) Predicted bioelectric map — PSCA (dark) vs Fincher "
                 "(light)", fontsize=10)

    # (b) class expression heatmap PSCA
    ax = axes[0, 1]
    cls_order = [c for c in VM_CLASSES if c in expr_p] + ["innexin"]
    M = np.array([[expr_p[c][i] for c in cls_order] for i in
                  range(len(groups_p))])
    im = ax.imshow(M.T, aspect="auto", cmap="viridis")
    ax.set_yticks(range(len(cls_order)))
    ax.set_yticklabels(cls_order, fontsize=8)
    ax.set_xticks(range(len(groups_p)))
    ax.set_xticklabels(groups_p, rotation=60, ha="right", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8, label="expression (scaled 0-1)")
    ax.set_title("(b) Ion-transporter expression by cell type (PSCA)",
                 fontsize=10)

    # (c) V4: innexin vs Vm
    ax = axes[1, 0]
    vm_arr = np.array([vm_p[g] for g in groups_p])
    inx_arr = np.array([expr_p["innexin"][i] for i in range(len(groups_p))])
    ax.scatter(inx_arr, vm_arr, s=60, c="#2c7fb8", edgecolor="k", lw=0.5)
    for i, g in enumerate(groups_p):
        ax.annotate(g, (inx_arr[i], vm_arr[i]), fontsize=7,
                    xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("innexin family expression (scaled)")
    ax.set_ylabel("predicted Vmem (mV)")
    ax.set_title(f"(c) V4: innexin does not set own Vm "
                 f"(rho={out['checks']['PSCA']['V4']['spearman_innexin_vm']:.2f})",
                 fontsize=10)

    # (d) check summary
    ax = axes[1, 1]
    rows = []
    for atlas in ("PSCA", "Fincher"):
        for vid in ("V1", "V2", "V3", "V4"):
            r = out["checks"][atlas][vid]
            rows.append((atlas, vid, r["pass"],
                         out["jackknife_stability"][atlas][vid]))
    ax.axis("off")
    y = 0.95
    ax.text(0.0, y, "V1-V4 pre-registered checks (real data)",
            fontsize=11, weight="bold", transform=ax.transAxes)
    y -= 0.09
    for atlas, vid, ok, jk in rows:
        mark = "PASS" if ok else "FAIL"
        col = "#1a9641" if ok else "#d7191c"
        ax.text(0.02, y, f"{atlas:8s} {vid}: {mark}", fontsize=10,
                color=col, family="DejaVu Sans", transform=ax.transAxes)
        ax.text(0.45, y, f"jackknife {jk}/20", fontsize=9, color="#555",
                transform=ax.transAxes)
        y -= 0.075
    ax.text(0.02, y - 0.02,
            f"cross-atlas Spearman rho = {out['cross_atlas']['spearman']:.2f}",
            fontsize=10, transform=ax.transAxes)
    ax.set_title("(d) Check summary", fontsize=10)

    path = os.path.join(RESULTS, "fig17_psca_vm_map.png")
    fig.savefig(path, dpi=160)
    print(f"saved {path}")


if __name__ == "__main__":
    main()
