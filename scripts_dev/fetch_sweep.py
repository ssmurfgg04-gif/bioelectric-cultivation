"""Download the 24 sweep cell artifacts + aggregate from GitHub Actions."""
import json
import os
import urllib.request
import zipfile
import io

TOKEN = os.environ.get("GITHUB_TOKEN", "")  # never hard-commit credentials
REPO = "ssmurfgg04-gif/bioelectric-cultivation"
RUN_ID = 34819736606
OUT = os.path.join(os.path.dirname(__file__), "sweep_artifacts")


def api(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    return json.load(urllib.request.urlopen(req))


def download_artifact(url, dest_dir):
    """Handle the 302 to azure blob storage WITHOUT forwarding the token."""
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    opener = urllib.request.build_opener(NoAuthRedirect())
    data = opener.open(req).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extractall(dest_dir)
    return data


class NoAuthRedirect(urllib.request.HTTPRedirectHandler):
    """Strip the Authorization header when following redirects (azure 401s otherwise)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is not None:
            new_req.headers = {k: v for k, v in new_req.headers.items()
                               if k.lower() != "authorization"}
            del new_req.unverifiable  # not needed; keep simple
        return new_req


def main():
    os.makedirs(os.path.join(OUT, "cells"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "aggregate"), exist_ok=True)
    arts = api(f"https://api.github.com/repos/{REPO}/actions/runs/"
               f"{RUN_ID}/artifacts?per_page=100")["artifacts"]
    n = 0
    for a in arts:
        if a["name"].startswith("fidelity-cell-"):
            idx = a["name"].split("-")[-1]
            download_artifact(a["archive_download_url"],
                              os.path.join(OUT, "cells"))
            # zip contains cell_<idx>.json; ensure naming
            n += 1
        elif a["name"] == "fidelity-sweep-aggregate":
            download_artifact(a["archive_download_url"],
                              os.path.join(OUT, "aggregate"))
    print(f"downloaded {n} cells + aggregate -> {OUT}")
    print(sorted(os.listdir(os.path.join(OUT, "cells")))[:5], "...")
    print(os.listdir(os.path.join(OUT, "aggregate")))


if __name__ == "__main__":
    main()
