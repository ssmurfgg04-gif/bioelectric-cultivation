#!/usr/bin/env python3
"""Dispatch a workstream batch to the Experiment Batch runner fleet.

Usage: python3 scripts/dispatch_batch.py <batch_id> <workstream> <matrix.json>
  matrix.json: {"include":[{"module":"exp135_walk_chain","args":"--gamma 1","job_id":"B-g1"}, ...]}
Module must exist on origin/main. Artifacts land as "<batch_id>-<job_id>".
Token is read from $GITHUB_TOKEN or extracted from the origin remote URL.
"""
import json, os, re, subprocess, sys

URL = "https://api.github.com/repos/ssmurfgg04-gif/bioelectric-cultivation/actions/workflows/experiments.yml/dispatches"

def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    remote = subprocess.run(["git", "remote", "get-url", "origin"],
                            capture_output=True, text=True).stdout
    m = re.search(r":([A-Za-z0-9_]+)@", remote)
    if not m:
        sys.exit("no token: set GITHUB_TOKEN")
    return m.group(1)

def main():
    batch_id, workstream, matrix_path = sys.argv[1], sys.argv[2], sys.argv[3]
    matrix = json.load(open(matrix_path))
    body = json.dumps({"ref": "main", "inputs": {
        "batch_id": batch_id, "workstream": workstream,
        "job_matrix": json.dumps(matrix)}}).encode()
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Authorization": f"token {token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"})
    r = urllib.request.urlopen(req)
    print("DISPATCHED", r.status, batch_id, workstream, len(matrix["include"]), "jobs")

if __name__ == "__main__":
    import urllib.request
    main()
