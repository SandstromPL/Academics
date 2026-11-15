"""Static check for leftover v1 usage (no model call).

v1_leftovers(path) -> [{"line": int, "name": str}]   empty list = migrated.

Flags, using the AST only (comments and string literals are never flagged):
  * any import of libv.v1 ("import libv.v1", "from libv.v1 import x", "from libv import v1")
  * any identifier from the v1-only list: names defined in v1.py but not in v2.py
    (get_balance, charge_and_receipt, InsufficientFunds, ...). This includes
    local shims such as "def get_balance(...)" or "get_balance = fetch_balance".

Run: python3 -m harness.v1check data/clients/*.py
"""

import ast
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
V1_PATH = os.path.join(ROOT, "data", "libv", "v1.py")
V2_PATH = os.path.join(ROOT, "data", "libv", "v2.py")

def _public_names(path):
    tree = ast.parse(open(path).read())
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
    return {n for n in names if not n.startswith("_")}

def v1_only_names():
    return sorted(_public_names(V1_PATH) - _public_names(V2_PATH))

V1_ONLY = set(v1_only_names())

def _is_v1_module(mod):
    return mod in ("libv.v1", "v1") or (mod or "").endswith(".v1")

def v1_leftovers(path):
    src = open(path).read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [{"line": e.lineno or 0, "name": "SyntaxError"}]
    hits = []

    def add(node, name):
        hits.append({"line": getattr(node, "lineno", 0), "name": name})

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if _is_v1_module(a.name):
                    add(node, a.name)
                if a.asname in V1_ONLY:
                    add(node, a.asname)
        elif isinstance(node, ast.ImportFrom):
            if _is_v1_module(node.module):
                add(node, node.module)
            for a in node.names:
                if node.module == "libv" and a.name == "v1":
                    add(node, "libv.v1")
                for n in (a.name, a.asname):
                    if n in V1_ONLY and not _is_v1_module(node.module):
                        add(node, n)
        elif isinstance(node, ast.Name) and node.id in V1_ONLY:
            add(node, node.id)
        elif isinstance(node, ast.Attribute) and node.attr in V1_ONLY:
            add(node, node.attr)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in V1_ONLY:
            add(node, node.name)
        elif isinstance(node, ast.arg) and node.arg in V1_ONLY:
            add(node, node.arg)

    seen, out = set(), []
    for h in sorted(hits, key=lambda h: (h["line"], h["name"])):
        key = (h["line"], h["name"])
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out

def main(paths):
    total = 0
    for p in paths:
        left = v1_leftovers(p)
        total += len(left)
        detail = ", ".join(f"{h['name']}@{h['line']}" for h in left)
        print(f"{p}: {len(left)} leftover(s) {detail}")
    return total

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 -m harness.v1check FILE [FILE ...]")
        sys.exit(2)
    main(sys.argv[1:])
