#!/usr/bin/env python3
"""Probe for exp288's body: verify the pre-registered assertions hold
against the deposits BEFORE the body is written (fail-fast probe, not
part of the experiment)."""
import json
import os
import sys

import numpy as np

ROOT = "/home/z/my-project/bioelectric-cultivation"
sys.path.insert(0, ROOT)

dep287 = json.load(open(os.path.join(ROOT, "results",
                                     "exp287_fixed_point_identity.json")))
rows = dep287["rows"]

# 1. fields present
need = {"commit_seq_sha256", "cvt_rms", "n_commits", "sc_rms",
        "walk_steps", "host", "seed", "row_key", "err_exact"}
print("1. fields ok:", all(need <= set(r) for r in rows),
      "| n_rows:", len(rows))

# 2. cross-instance identity per (host, seed)
byhs = {}
for r in rows:
    byhs.setdefault((r["host"], int(r["seed"])), {})[r["row_key"]] = r
n_ws_eq = n_cvt_eq = n_nc_eq = 0
pairs = 0
for (h, s), d in byhs.items():
    a, b = d.get("r-60i0"), d.get("r-60i1")
    if a is None or b is None:
        print("   MISSING instance for", h, s, sorted(d))
        continue
    pairs += 1
    n_ws_eq += int(a["walk_steps"] == b["walk_steps"])
    n_cvt_eq += int(a["cvt_rms"] == b["cvt_rms"])
    n_nc_eq += int(a["n_commits"] == b["n_commits"])
print(f"2. pairs {pairs}: walk_steps eq {n_ws_eq}, cvt eq {n_cvt_eq}, "
      f"n_commits eq {n_nc_eq}")

# 3. dep287 regressions + inputs keys + host_table mean_cvt
reg = dep287["regressions"]
print("3. regression keys:", sorted(reg))
print("   rho cvt~mia:",
      repr(reg["mean_cvt~mia_prod_err"]["rho"]),
      "| rho cvt~prem:",
      repr(reg["mean_cvt~one_zone_premium"]["rho"]))
print("   inputs keys:", sorted(dep287["inputs"]))
ht = {r["host"]: r for r in dep287["host_table"]}
print("   host_table mean_cvt sample H0/H3:",
      repr(ht["H0"]["mean_cvt"]), repr(ht["H3"]["mean_cvt"]))
print("   hosts order:", dep287["hosts"])

# 4. dep287 host_table vs rows mean_cvt consistency
hosts = dep287["hosts"]
for h in hosts:
    cvts = [r["cvt_rms"] for r in rows if r["host"] == h]
    assert float(np.mean(cvts)) == ht[h]["mean_cvt"], h
print("4. host mean_cvt consistent with rows: True")

# 5. walk_steps range + n_commits range
ws = [r["walk_steps"] for r in rows]
nc = [r["n_commits"] for r in rows]
print("5. walk_steps range:", min(ws), max(ws),
      "| n_commits range:", min(nc), max(nc))

# 6. cls-2 probe: rebuild two hosts (path + small_world), classify the
#    deep instance targets, count cls 2 over the full frame + the write set
from cultivation.substrate.graph import path as graph_path
from experiments.exp73_active_renormalization import small_world
from experiments.exp94_multizone_scale import (MULTI, labeling_bfs_n,
                                               spec_target_n)
from cultivation.compiler.anatomy import AnatomySpec, Zone


def classify(T, W):
    n = len(T)
    Td = np.asarray(T, dtype=float)
    bnd = np.zeros(n, dtype=bool)
    for i in range(n):
        if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
            bnd[i] = True
    support = np.abs(W) > 0
    iu = np.triu_indices(n, 1)
    deg = np.zeros(n, dtype=int)
    for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
        deg[a] += 1
        deg[b] += 1
    pj = deg >= 2
    cls = np.zeros(n, dtype=int)
    cls[pj] = 1
    cls[bnd] = 0
    return {"boundary": bnd, "junction": pj & ~bnd,
            "interior": ~(bnd | pj), "class": cls}


for hname, A in (("H0-path", graph_path(400)),
                 ("H2-sw", small_world(400, 0.10, 101))):
    canon = labeling_bfs_n(np.abs(A))
    for inst in (0, 1):
        zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, -60.0)
              for z in MULTI.zones]
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=-60.0, name=nm)
                   for (a, b, nm) in zs],
            amputate_plane=MULTI.amputate_plane,
            spec_name=f"probe-i{inst}",
            somatic_latch=MULTI.somatic_latch)
        T = spec_target_n(spec, canon, 400)
        m = classify(T, A)
        c = m["class"]
        full2 = int((c == 2).sum())
        # write set ~ reg_walk span from the zones
        reg_idx = []
        for z in spec.zones:
            i0 = int(round(z.f0 * 400))
            i1 = max(int(round(z.f1 * 400)), i0 + 1)
            reg_idx.extend(range(i0, i1))
        span = list(range(min(reg_idx), max(reg_idx) + 1))
        ws2 = int((c[span] == 2).sum())
        print(f"6. {hname} i{inst}: cls2 full-frame {full2}, "
              f"write-span {ws2}, boundary {int(m['boundary'].sum())}, "
              f"junction {int(m['junction'].sum())}, "
              f"interior {int(m['interior'].sum())}, span {len(span)}")

# 7. exp288 docstring + header shas
src = open(os.path.join(ROOT, "experiments",
                        "exp288_spec_layer_face.py")).read()
import hashlib
doc = src[src.index('"""') + 3:src.index('"""', src.index('"""') + 3)]
marker = "def main() -> dict:\n"
header = src[:src.index(marker) + len(marker)]
print("7. docstring sha:", hashlib.sha256(doc.encode()).hexdigest())
print("   header sha:", hashlib.sha256(header.encode()).hexdigest())
