#!/usr/bin/env python3
"""codegraph — project structure analyzer (AST-based for Python, regex-based
for TS/JS/Rust). Outputs a module dependency graph (JSON + graphviz dot) and
a symbol census. Companion to `scc` (LOC stats) and `code2flow` (call graphs).

    python tools/codegraph.py [path] [--json out.json] [--dot out.dot]
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from collections import defaultdict


def scan_python(path: str) -> dict:
    mods, deps, symbols = {}, defaultdict(set), defaultdict(int)
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in
                   {".git", "__pycache__", "node_modules", ".venv", "results"}]
        for f in files:
            if not f.endswith(".py"):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, path)
            mod = rel[:-3].replace(os.sep, ".")
            mods[mod] = rel
            try:
                tree = ast.parse(open(fp, encoding="utf-8", errors="ignore").read())
            except SyntaxError:
                continue
            local = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols["functions"] += 1
                    local.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    symbols["classes"] += 1
                    local.add(node.name)
                elif isinstance(node, ast.Import):
                    for a in node.names:
                        deps[mod].add(a.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps[mod].add(node.module.split(".")[0])
    return {"modules": mods, "dependencies": {k: sorted(v) for k, v in deps.items()},
            "symbols": dict(symbols)}


TS_IMPORT = re.compile(r"""(?:import\s+[^'"]*?from\s+|require\(\s*)['"]([^'"]+)""")
RUST_USE = re.compile(r"^\s*(?:pub\s+)?use\s+([a-zA-Z0-9_:]+)", re.M)


def scan_other(path: str) -> dict:
    counts = defaultdict(int)
    imports = defaultdict(int)
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in
                   {".git", "__pycache__", "node_modules", ".venv", "results",
                    ".next", "dist"}]
        for f in files:
            fp = os.path.join(root, f)
            ext = f.rsplit(".", 1)[-1] if "." in f else ""
            if ext in {"ts", "tsx", "js", "jsx", "mjs", "cjs"}:
                counts["ts_js_files"] += 1
                try:
                    text = open(fp, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                for m in TS_IMPORT.findall(text):
                    if not m.startswith("."):
                        imports[f"npm:{m.split('/')[0]}"] += 1
                counts["ts_js_lines"] += text.count("\n")
            elif ext == "rs":
                counts["rust_files"] += 1
                try:
                    text = open(fp, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                for m in RUST_USE.findall(text):
                    imports[f"rust:{m.split('::')[0]}"] += 1
                counts["rust_lines"] += text.count("\n")
            elif ext in {"py",}:
                pass  # handled by scan_python
    return {"counts": dict(counts), "external_imports": dict(imports)}


def to_dot(deps: dict) -> str:
    lines = ["digraph codegraph {", "  rankdir=LR;", '  node [shape=box, fontsize=10];']
    for mod, ds in deps.items():
        for d in ds:
            lines.append(f'  "{mod}" -> "{d}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--dot", dest="dot_out", default=None)
    args = ap.parse_args()

    py = scan_python(args.path)
    other = scan_other(args.path)
    report = {"python": py, "other": other}
    js = json.dumps(report, indent=2)
    if args.json_out:
        open(args.json_out, "w").write(js)
    else:
        print(js)
    if args.dot_out:
        open(args.dot_out, "w").write(to_dot(py["dependencies"]))
    n_mod = len(py["modules"])
    print(f"[codegraph] {n_mod} python modules, "
          f"{py['symbols'].get('functions', 0)} functions, "
          f"{py['symbols'].get('classes', 0)} classes, "
          f"{other['counts'].get('ts_js_files', 0)} ts/js files, "
          f"{other['counts'].get('rust_files', 0)} rust files",
          file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
