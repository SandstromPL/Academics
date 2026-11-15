"""Tool registry for P04 (pattern from lab-06a: TOOL_REGISTRY, validate_arguments, build_tools_desc).

Tools: search_guide, read_file, write_file (scoped by safety/scope.py), run_tests.
v1_leftovers is plain code used by the harness and the eval, not a model tool.
"""
import os
import re
import shutil
import subprocess
import sys

from harness.retrieval import MAX_TEXT, load_guide, retrieve
from harness.v1check import v1_leftovers
from safety.scope import check_write, gate_record

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
READABLE = [os.path.join(ROOT, "data", "clients") + os.sep, os.path.join(ROOT, "data", "libv", "v2.py")]
TEST_TIMEOUT = 30


class CaseContext:
    """Per-case state the tools need: which client may be written, and what was logged."""

    def __init__(self, case_id, client_file, expand=False):
        self.case_id = case_id
        self.client_file = client_file
        self.expand = expand
        self.retrieved_ids = []   # every section id returned by search_guide in this case
        self.gates = []           # gate records from write_file
        self._guide = None

    @property
    def guide(self):
        if self._guide is None:
            self._guide = load_guide()
        return self._guide


def search_guide(ctx, query, k=3):
    hits = retrieve(query, ctx.guide, k=k, expand=ctx.expand)
    ids = [s["id"] for s in hits]
    seen_all = bool(ids) and all(i in ctx.retrieved_ids for i in ids)
    ctx.retrieved_ids.extend(ids)
    if seen_all:
        # Nothing new: repeating the same sections only fills the context (case_09 searched 5 times in a row).
        return {"no_new_sections": ids,
                "note": "search_guide already returned these sections in this file; the guide has nothing more on "
                        "this. Fix the client from the test error and the v2 signatures instead of searching again."}
    return [{"id": s["id"], "title": s["title"],
             "text": (s["text"] + "\nBEFORE:\n" + s["before"] + "\nAFTER:\n" + s["after"])[:MAX_TEXT + 200]}
            for s in hits]


def read_file(ctx, path):
    full = os.path.realpath(os.path.join(ROOT, path))
    if not any(full == r or full.startswith(r) for r in READABLE):
        return {"error": "read denied: only data/clients/ and data/libv/v2.py are readable"}
    if not os.path.isfile(full):
        return {"error": f"no such file: {path}"}
    return {"path": path, "text": open(full).read()}


def write_file(ctx, path, text):
    rec = gate_record(path, ctx.client_file, ctx.case_id)
    ctx.gates.append(rec)
    ok, reason = check_write(path, ctx.client_file)
    if not ok:
        return {"ok": False, "error": reason}
    with open(os.path.join(ROOT, ctx.client_file), "w") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    return {"ok": True}


def run_tests(ctx, client=None):
    name = os.path.splitext(os.path.basename(client or ctx.client_file))[0]
    test = os.path.join("data", "clients", "tests", f"test_{name}.py")
    if not os.path.isfile(os.path.join(ROOT, test)):
        return {"exit_code": 4, "failed": 0, "first_failure": f"no test file {test}"}
    # A rewrite of the same size in the same second can leave a stale .pyc that Python
    # still trusts, so clear the client bytecode cache and never write a new one.
    shutil.rmtree(os.path.join(ROOT, "data", "clients", "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test],
                           cwd=ROOT, capture_output=True, text=True, timeout=TEST_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "failed": 0, "first_failure": f"timeout after {TEST_TIMEOUT}s"}
    out = p.stdout + p.stderr
    failed = sum(int(n) for n in re.findall(r"(\d+) (?:failed|errors?)\b", out.splitlines()[-1] if out.strip() else ""))
    first = ""
    if p.returncode != 0:
        lines = [l for l in out.splitlines() if l.startswith("E ") or "Error" in l]
        first = "\n".join(lines[:8]) or out[-800:]
    if p.returncode != 0 and failed == 0:
        failed = 1  # collection/import error
    return {"exit_code": p.returncode, "failed": failed if p.returncode else 0, "first_failure": first[:800]}


TOOL_REGISTRY = {
    "search_guide": {
        "fn": search_guide,
        "args": {"query": str, "k": int},
        "required": ["query"],
        "desc": "search_guide(query: str, k: int = 3) -> list of {id, title, text}. Keyword search over "
                "the v1->v2 migration guide. Put the v1 names you see in the client in the query.",
    },
    "read_file": {
        "fn": read_file,
        "args": {"path": str},
        "required": ["path"],
        "desc": "read_file(path: str) -> {path, text}. Read-only; allowed: data/clients/..., data/libv/v2.py.",
    },
    "write_file": {
        "fn": write_file,
        "args": {"path": str, "text": str},
        "required": ["path", "text"],
        "desc": "write_file(path: str, text: str) -> {ok}. Overwrites the WHOLE file. Only the current "
                "client file may be written; anything else is denied.",
    },
    "run_tests": {
        "fn": run_tests,
        "args": {"client": str},
        "required": [],
        "desc": "run_tests(client: str) -> {exit_code, failed, first_failure}. Runs the client's pytest "
                "file against libv v2 (30 s timeout). exit_code 0 means green.",
    },
}

BASELINE_TOOLS = ["read_file", "write_file", "run_tests"]
IMPROVED_TOOLS = ["search_guide", "read_file", "write_file", "run_tests"]


def validate_arguments(name, args, allowed):
    if name not in allowed:
        return f"unknown or unavailable tool {name!r}; available: {', '.join(allowed)}"
    if not isinstance(args, dict):
        return "args must be a JSON object"
    spec = TOOL_REGISTRY[name]
    for r in spec["required"]:
        if r not in args:
            return f"missing argument {r!r} for {name}"
    for k, v in args.items():
        if k not in spec["args"]:
            return f"unexpected argument {k!r} for {name}"
        if not isinstance(v, spec["args"][k]):
            return f"argument {k!r} must be {spec['args'][k].__name__}"
    return None


def build_tools_desc(allowed):
    return "\n".join(f"- {TOOL_REGISTRY[n]['desc']}" for n in allowed)


def dispatch(ctx, name, args):
    return TOOL_REGISTRY[name]["fn"](ctx, **args)


__all__ = ["CaseContext", "TOOL_REGISTRY", "BASELINE_TOOLS", "IMPROVED_TOOLS", "validate_arguments",
           "build_tools_desc", "dispatch", "v1_leftovers"]
