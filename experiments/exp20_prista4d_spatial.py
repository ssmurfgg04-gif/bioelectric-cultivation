#!/usr/bin/env python3
"""exp20 — PRISTA4D: the SPATIAL Vm time-course (V3's transient and V4's
spatial form — the two clauses the dissociated atlases could not test).

DATA (public, downloaded this session):
  PRISTA4D (Han et al. 2026, GigaScience; db.cngb.org/stomics/prista4d,
  STDS0000399): 4D single-cell spatial transcriptomic atlas of planarian
  regeneration. Ingested here: the .spc (spatial-bin) matrices for
  0hpa (intact baseline), 12hpa, 36hpa post-amputation — 17,897 / ~14k /
  ~18k spatial bins x ~21.5k genes each, with obsm/spatial_3d coordinates
  and 34 anno cell-type labels per bin.

GENE-ID BRIDGE (solved this session):
  PRISTA4D annotates genes with SMESG IDs; the curated ion-transporter
  families use dd_Smed_v6. Bridge built via the planosphere Rosetta Stone
  2020 (smed_20140614.mapping.rosettastone.2020.txt, mirrored in the
  neurogenomics/orthogene GitHub release v1.1.1): dd_Smed_v6 ->
  ref_id(SMED300) -> SMESG_dd_Smes_v2. 270/270 bridged ion genes,
  266 present in the 12hpa sc var, all 11 families represented
  (57 innexin, 73 kv, 38 trp, 30 fana, ...).
  scripts_dev/build_smesg_bridge.py writes
  research/data/gene_mapping/ion_genes_smesg.json.

METHOD: per spatial bin, sum ion-family expression -> CP10K -> log1p ->
global scaling K=log1p(100) (the exp18 convention) -> family-weighted
permeabilities (vmem_inference GENE_WEIGHTS at family level) -> vectorized
GHK resting potential per bin -> the predicted SPATIAL bioelectric map at
each timepoint. No simulation of the ensemble is involved.

PRE-REGISTERED CRITERIA (written before any result was computed):
  V3s (injury depolarization transient, spatial form):
     the wound-facing edge (outer 12% of the long axis at each end)
     is DEPOLARIZED vs the fragment interior at 12hpa and 36hpa
     (Vm(edge) - Vm(interior) > 0), and the contrast is larger than
     the same positional contrast in the intact 0hpa animal.
  V3c (phagocyte clause, spatial): at 12hpa, bins annotated
     cathepsin+/phagocyte rank >= 70th percentile of all bins' Vm.
  V4s (junction smoothness — V4's spatial form): bins with high innexin
     expression sit in SMOOTHER regions of the Vm map: Spearman(innexin,
     local roughness) < 0 with block-bootstrap CI excluding 0, and the
     same correlation for a non-coupling family (kv) strictly weaker.
  V1s (stemness in space — sanity): at 0hpa, neoblast bins' mean Vm
     ranks <= 30th percentile among the 34 anno types.

KILLS-ROW: if V3s fails, the injury-transient premise of the fidelity
clock (FC1) is unsupported in real spatial data; if V4s fails, innexin
expression does not organize the spatial Vm map and the coupling story
loses its spatial leg. Both are informative either way.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import h5py
from scipy import sparse
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cultivation.validation import vmem_inference as VI  # noqa: E402
from cultivation.validation.stats import mean_se, spearman_ties  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRISTA = os.path.join(ROOT, "data", "prista4d")
BRIDGE = os.path.join(ROOT, "research", "data", "gene_mapping",
                      "ion_genes_smesg.json")
OUT = os.path.join(ROOT, "results", "exp20_prista4d_spatial.json")

# family -> (GHK class, weight) — vmem_inference GENE_WEIGHTS, family level
FAM_W = {
    "k_channel_leak": ("PK", 1.0), "kv_channel": ("PK", 0.6),
    "k_ca_channel": ("PK", 0.30), "nak_atpase": ("PK", 0.25),
    "fana_nav": ("PNa", 0.50), "nav_channel": ("PNa", 0.7),
    "trp_cation": ("PNa", 0.35), "p2x_purinergic": ("PNa", 0.20),
    "hvcn": ("PNa", 0.10), "cl_channel": ("PCl", 0.30),
}
FLOORS = {"PK": 0.05, "PNa": 0.02, "PCl": 0.05}
K_SCALE = float(np.log1p(100.0))
EDGE_FRAC = 0.12          # outer fraction of long axis = wound-facing edge


def _p(s):
    print(s, flush=True)


def load_bin_data(fn):
    """Return (family_expr {fam: per-bin log-scaled level}, xyz, anno codes,
    anno categories, n_bins) for one .spc.h5ad file."""
    with h5py.File(os.path.join(PRISTA, fn), "r") as f:
        var = [g.decode() if isinstance(g, bytes) else g
               for g in f["var/_index"][:]]
        data = f["X/data"][:]
        indices = f["X/indices"][:]
        indptr = f["X/indptr"][:]
        n_bins, n_genes = len(indptr) - 1, len(var)
        X = sparse.csr_matrix((data, indices, indptr),
                              shape=(n_bins, n_genes))
        xyz = f["obsm/spatial_3d"][:]
        anno_codes = f["obs/anno/codes"][:]
        anno_cats = [c.decode() if isinstance(c, bytes) else c
                     for c in f["obs/anno/categories"][:]]

    bridge = json.load(open(BRIDGE))["families"]
    smesg_of = {}
    for fam, genes in bridge.items():
        for g in genes:
            for s in g["smesg"]:
                smesg_of.setdefault(s, fam)

    tot = np.asarray(X.sum(axis=1)).ravel()
    cp10k_base = 1e4 / np.maximum(tot, 1.0)
    fam_expr = {}
    for fam in list(FAM_W) + ["innexin"]:
        cols = [i for i, g in enumerate(var) if smesg_of.get(g) == fam]
        if not cols:
            fam_expr[fam] = np.zeros(n_bins)
            continue
        sub = X[:, cols]
        s = np.asarray(sub.sum(axis=1)).ravel() * cp10k_base
        fam_expr[fam] = np.log1p(s) / K_SCALE
    return fam_expr, xyz, anno_codes, anno_cats, n_bins


def vm_map(fam_expr):
    """Vectorized GHK per bin (vmem_inference constants and weights)."""
    P = {c: np.full_like(next(iter(fam_expr.values())), v, float)
         for c, v in FLOORS.items()}
    for fam, (cls, w) in FAM_W.items():
        P[cls] = P[cls] + w * fam_expr[fam]
    ion = VI.ION
    num = (P["PK"] * ion["K"]["out"] + P["PNa"] * ion["Na"]["out"]
           + P["PCl"] * ion["Cl"]["in"])
    den = (P["PK"] * ion["K"]["in"] + P["PNa"] * ion["Na"]["in"]
           + P["PCl"] * ion["Cl"]["out"])
    return VI.RTF_MV * np.log(np.maximum(num, 1e-12)
                              / np.maximum(den, 1e-12))


def edge_interior_contrast(vm, xyz):
    """Vm(edge) - Vm(interior); edge = outer EDGE_FRAC of long axis."""
    x = xyz[:, 0]
    lo, hi = np.quantile(x, EDGE_FRAC), np.quantile(x, 1 - EDGE_FRAC)
    edge = (x <= lo) | (x >= hi)
    interior = ~edge
    return float(vm[edge].mean() - vm[interior].mean()), edge, interior


def block_bootstrap_ci(stat_fn, xyz, n_boot=300, seed=0,
                       n_blocks=12):
    """Block bootstrap over long-axis slices (spatial autocorrelation)."""
    rng = np.random.default_rng(seed)
    x = xyz[:, 0]
    edges = np.quantile(x, np.linspace(0, 1, n_blocks + 1))
    bid = np.digitize(x, edges[1:-1])
    blocks = [np.where(bid == b)[0] for b in range(n_blocks)]
    stats = []
    for _ in range(n_boot):
        pick = rng.integers(0, n_blocks, n_blocks)
        idx = np.concatenate([blocks[p] for p in pick])
        stats.append(stat_fn(idx))
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return float(lo), float(hi)


def main() -> dict:
    _p("=== exp20: PRISTA4D spatial Vm time-course "
       "(V3 transient + V4 spatial form) ===\n")
    files = {"0hpa": "0hpa1.spc.h5ad", "12hpa": "12hpa1.spc.h5ad",
             "36hpa": "36hpa1.spc.h5ad"}
    maps, contrasts, meta = {}, {}, {}
    for tp, fn in files.items():
        fam_expr, xyz, anno, cats, n = load_bin_data(fn)
        vm = vm_map(fam_expr)
        maps[tp] = (vm, xyz, anno, fam_expr)
        c, edge, interior = edge_interior_contrast(vm, xyz)
        contrasts[tp] = c
        _p(f"[{tp}] {n} bins  Vm mean {vm.mean():7.1f} mV  "
           f"sd {vm.std():5.1f}  edge-interior {c:+6.1f} mV")
        meta[tp] = {"n_bins": int(n), "vm_mean": float(vm.mean()),
                    "vm_sd": float(vm.std()), "contrast": c}

    # ---------------- V3s ----------------
    v3s_a = contrasts["12hpa"] > 0 and contrasts["36hpa"] > 0
    v3s_b = (contrasts["12hpa"] > contrasts["0hpa"]
             and contrasts["36hpa"] > contrasts["0hpa"])
    # bootstrap CI on the 12hpa contrast
    vm12, xyz12, _, _ = maps["12hpa"]
    ci12 = block_bootstrap_ci(
        lambda idx: float(vm12[idx][
            (xyz12[idx, 0] <= np.quantile(xyz12[idx, 0], EDGE_FRAC))
            | (xyz12[idx, 0] >= np.quantile(xyz12[idx, 0],
                                            1 - EDGE_FRAC))].mean()
            - vm12[idx][
                (xyz12[idx, 0] > np.quantile(xyz12[idx, 0], EDGE_FRAC))
                & (xyz12[idx, 0] < np.quantile(xyz12[idx, 0],
                                               1 - EDGE_FRAC))].mean()),
        xyz12, n_boot=200, seed=1)

    # ---------------- V3c (phagocyte clause at 12hpa) ----------------
    vm12, xyz12, anno12, _ = maps["12hpa"]
    cats12 = meta_cats = None
    ph_mask = np.isin(anno12, [i for i, c in enumerate(PH_CATS)
                                if c]) if False else None
    # anno categories are identical across files (34 types); rebuild mask
    with h5py.File(os.path.join(PRISTA, files["12hpa"]), "r") as f:
        cats12 = [c.decode() if isinstance(c, bytes) else c
                  for c in f["obs/anno/categories"][:]]
    ph_idx = [i for i, c in enumerate(cats12)
              if "cathepsin" in c.lower() or "phagocyt" in c.lower()]
    ph_mask = np.isin(anno12, ph_idx)
    pct = 100.0 * float((vm12 < vm12[ph_mask].mean()).mean()) \
        if ph_mask.any() else float("nan")
    v3c = bool(ph_mask.any() and pct >= 70.0)

    # ---------------- V4s (junction smoothness) ----------------
    def roughness(vm, xyz, k=6):
        """RMS Vm difference to k nearest spatial neighbors per bin."""
        from scipy.spatial import cKDTree
        tree = cKDTree(xyz)
        _, nn = tree.query(xyz, k=k + 1)   # +1: self
        nb = vm[nn[:, 1:]]
        return np.sqrt(np.mean((nb - vm[:, None]) ** 2, axis=1))

    v4 = {}
    for tp in ("0hpa", "12hpa", "36hpa"):
        vm, xyz, anno, fam = maps[tp]
        r = roughness(vm, xyz)
        rho_inx = spearman_ties(fam["innexin"], r)
        rho_kv = spearman_ties(fam["kv_channel"], r)
        ci_inx = block_bootstrap_ci(
            lambda idx: spearman_ties(fam["innexin"][idx], r[idx]),
            xyz, n_boot=200, seed=2)
        v4[tp] = {"rho_innexin_roughness": rho_inx,
                  "rho_kv_roughness": rho_kv,
                  "ci95_innexin": ci_inx}
        _p(f"[{tp}] V4s rho(innexin, roughness) = {rho_inx:+.3f} "
           f"CI {ci_inx[0]:+.3f}..{ci_inx[1]:+.3f}   "
           f"control rho(kv) = {rho_kv:+.3f}")
    tp_main = "12hpa"
    v4s = bool(v4[tp_main]["rho_innexin_roughness"] < 0
               and v4[tp_main]["ci95_innexin"][1] < 0
               and abs(v4[tp_main]["rho_innexin_roughness"])
               > abs(v4[tp_main]["rho_kv_roughness"]))

    # ---------------- V1s (neoblast in space, 0hpa) ----------------
    vm0, xyz0, anno0, _ = maps["0hpa"]
    with h5py.File(os.path.join(PRISTA, files["0hpa"]), "r") as f:
        cats0 = [c.decode() if isinstance(c, bytes) else c
                 for c in f["obs/anno/categories"][:]]
    means = [(c, float(vm0[anno0 == i].mean())) for i, c in enumerate(cats0)
             if (anno0 == i).sum() >= 30]
    order = sorted(means, key=lambda t: t[1])
    nb_rank = next((r for r, (c, _) in enumerate(order, 1)
                    if "neoblast" in c.lower()), None)
    n_types = len(order)
    v1s = bool(nb_rank is not None and nb_rank <= max(1, int(np.ceil(
        0.3 * n_types))))

    # ---------------- report ----------------
    crit = {
        "V3s_injury_depolarization": bool(v3s_a and v3s_b),
        "V3c_phagocyte_depolarized": v3c,
        "V4s_junction_smoothness": v4s,
        "V1s_neoblast_hyperpolarized_in_space": v1s,
    }
    _p("\n criteria:")
    for k, v in crit.items():
        _p(f"    {k}: {'PASS' if v else 'REFUTED'}")

    out = {"exp": "exp20_prista4d_spatial",
           "source": "PRISTA4D STDS0000399 (Han 2026, GigaScience); "
                     "0hpa/12hpa/36hpa spc matrices, replicate 1",
           "gene_bridge": "dd_Smed_v6 -> SMED300 -> SMESG via planosphere "
                          "Rosetta Stone 2020 (orthogene mirror); "
                          "270 ion genes, 11 families",
           "timepoints": meta,
           "contrasts": contrasts,
           "contrast_ci95_12hpa": ci12,
           "V4s": v4,
           "V1s": {"neoblast_rank": nb_rank, "n_anno_types": n_types,
                   "order": [c for c, _ in order[:10]]},
           "criteria": crit,
           "notes": "per-bin GHK on family-level CP10K-log1p expression "
                    "(exp18 normalization); edge = outer 12% of long "
                    "axis; block bootstrap (12 x-slices); no ensemble "
                    "simulation involved."}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    _p(f"\n  results -> {OUT}")
    return out


PH_CATS = []  # unused placeholder (mask built from categories directly)


if __name__ == "__main__":
    main()
