#!/usr/bin/env python3
"""Merge the b16-hosts and b16-reader runner fleets' artifacts into the
repo's results/ and evaluate the unions (exp241 X1/X2, exp242 N1/N2)."""
import io
import json
import os
import subprocess
import zipfile

import numpy as np

import re as _re


def _token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    remote = subprocess.run(["git", "remote", "get-url", "origin"],
                            capture_output=True, text=True,
                            cwd=ROOT).stdout
    m = _re.search(r":([A-Za-z0-9_]+)@", remote)
    if not m:
        raise SystemExit("no token: set GITHUB_TOKEN")
    return m.group(1)


REPO = "ssmurfgg04-gif/bioelectric-cultivation"
ROOT = "/home/z/my-project/bioelectric-cultivation"
TOKEN = _token()


def get_artifacts(run_id):
    url = f"https://api.github.com/repos/{REPO}/actions/runs/{run_id}/artifacts?per_page=100"
    out = subprocess.run(["curl", "-s", "-H", f"Authorization: token {TOKEN}", url],
                         capture_output=True, text=True)
    return json.loads(out.stdout).get("artifacts", [])


def download(art, want_prefix):
    """Extract ONLY the job's own shard file from the artifact zip: the
    shard number comes from the artifact's job_id suffix (b16-hosts-h7
    -> shard 7; b16-reader-r12 -> shard 12; h0r -> shard 0)."""
    job_id = art["name"].rsplit("-", 1)[-1]
    shard = 0 if job_id == "h0r" else int(job_id.lstrip("hr"))
    want = f"{want_prefix}{shard}.json"
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts/{art['id']}/zip"
    out = subprocess.run(["curl", "-sL", "-H", f"Authorization: token {TOKEN}", url],
                         capture_output=True)
    zf = zipfile.ZipFile(io.BytesIO(out.stdout))
    for name in zf.namelist():
        if os.path.basename(name) == want:
            data = zf.read(name)
            dest = os.path.join(ROOT, "results", want)
            with open(dest, "wb") as f:
                f.write(data)
            return want
    return None


def main():
    landed = []
    for run_id, tag, prefix in (
            (35368769651, "hosts", "exp241_host_shard_"),
            (35368772204, "reader", "exp242_reader_n5000_shard_")):
        for art in get_artifacts(run_id):
            name = download(art, prefix)
            if name:
                landed.append((tag, art["name"], name))
    print(f"landed {len(landed)} artifact files")
    for tag, aname, fname in landed[:6]:
        print(" ", tag, aname, "->", fname)

    # ---- exp241 union ----
    shards = {}
    for i in range(20):
        pth = os.path.join(ROOT, "results", f"exp241_host_shard_{i}.json")
        if os.path.exists(pth):
            shards[i] = json.load(open(pth))
    print(f"\nexp241 shards on disk: {sorted(shards.keys())}")
    all_errs, host_stats = [], []
    x1_all = True
    for i, d in sorted(shards.items()):
        x1_all = x1_all and bool(d["gates"]["X1"]) and bool(d["gates"]["X2"])
        for h in d["hosts"]:
            worst_h = 0.0
            for t in h["targets"]:
                for e in t["errs"]:
                    all_errs.append(float(e))
                    worst_h = max(worst_h, float(e))
            host_stats.append({"shard": i, "host": h["host"],
                               "grid_index": h["grid_index"],
                               "worst_err": worst_h,
                               "carried": worst_h < 6.0,
                               "connected": h["connected"],
                               "rewire_seed": h.get("rewire_seed")})
    worst = max(all_errs) if all_errs else None
    carried = sum(1 for h in host_stats if h["carried"])
    x1 = bool(x1_all and all(np.isfinite(all_errs)) and len(host_stats) == 100)
    x2 = carried == 100
    wtxt = f"{worst:.4f}" if worst is not None else "NA"
    print(f"exp241 union: {len(host_stats)} hosts, carried {carried}, "
          f"worst err {wtxt}, X1 {x1}, X2 {x2}")
    union241 = {
        "exp": "exp241_cross_organism_scale UNION (the b16-hosts fleet merge)",
        "shards_landed": sorted(shards.keys()),
        "n_hosts": len(host_stats),
        "carried_hosts": carried,
        "worst_err": worst,
        "worst_margin": 6.0 - worst if worst is not None else None,
        "exp209_anchor_margin": 5.298,
        "host_stats": host_stats,
        "X1": bool(x1), "X2": bool(x2),
        "note": "the 100 pre-named host draws with exp202's disclosed "
                "connectivity-redraw multiplicity carried verbatim "
                "(rewire_seed recorded per host; ~51 distinct organisms "
                "across 100 draws, not deduplicated)",
    }
    with open(os.path.join(ROOT, "results", "exp241_host_union.json"), "w") as f:
        json.dump(union241, f, indent=1, default=float)

    # ---- exp242 union ----
    rshards = {}
    for i in range(20):
        p = os.path.join(ROOT, "results", f"exp242_reader_n5000_shard_{i}.json")
        if os.path.exists(p):
            rshards[i] = json.load(open(p))
    print(f"\nexp242 shards on disk: {sorted(rshards.keys())}")
    prim, red = {}, {}
    for i, d in sorted(rshards.items()):
        gate = d.get("gates", {}).get("N2_flat_profile", {})
        errs = gate.get("row_errs", [])
        row = d.get("row_index")
        if d.get("redundancy_rerun"):
            red[row] = errs
        else:
            prim[row] = {"class": gate.get("class"), "errs": errs}
    n_rows = len(prim)
    all_e = [e for v in prim.values() for e in v["errs"]]
    worst_r = max(all_e) if all_e else None
    # redundancy bit-checks
    red_ok = []
    for row, errs in red.items():
        if row in prim:
            red_ok.append(errs == prim[row]["errs"])
    n1 = n_rows == 15 and all(np.isfinite(all_e))
    n2 = worst_r is not None and worst_r < 6.0 and worst_r <= 0.81
    wtxt_r = f"{worst_r:.4f}" if worst_r is not None else "NA"
    print(f"exp242 union: {n_rows}/15 primary rows, worst err {wtxt_r}, "
          f"redundancy re-runs {len(red)} bit-identical {all(red_ok) if red_ok else '-'}, "
          f"N1 {n1}, N2 {n2}")
    union242 = {
        "exp": "exp242_reader_n5000 UNION (the b16-reader fleet merge)",
        "shards_landed": sorted(rshards.keys()),
        "primary_rows": {str(k): v for k, v in sorted(prim.items())},
        "n_primary_rows": n_rows,
        "worst_err": worst_r,
        "redundancy_reruns": {str(k): v for k, v in sorted(red.items())},
        "redundancy_bit_identical": bool(all(red_ok)) if red_ok else None,
        "N1": bool(n1), "N2": bool(n2),
        "band_1p5x_n1000": 0.81,
    }
    with open(os.path.join(ROOT, "results", "exp242_reader_n5000_union.json"), "w") as f:
        json.dump(union242, f, indent=1, default=float)
    print("\nunions deposited: exp241_host_union.json, exp242_reader_n5000_union.json")


if __name__ == "__main__":
    main()
