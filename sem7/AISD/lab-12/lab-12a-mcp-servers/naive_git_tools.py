"""Lab 12a: the NAIVE git tools (given; do not copy this into git_tools.py).

The git server's "Step 1": every argument goes to git as it came from the
model. No check_rev, no path guard, no "--" before paths. It still uses an
argument list (no shell), so this is not shell injection; it is ARGUMENT
injection, which a list does not stop:

    rev = "--output=../pwned.txt"        git show writes a file outside the repo
    rev_from = "../secrets/api_key.txt"  git diff reads a file outside the repo

lab12a.py eval runs your git_tools.py ("guarded") against this ("naive").
"""
import subprocess
from pathlib import Path


def _git(repo, args):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=10)
    if proc.returncode != 0 and not proc.stdout:  # git diff of files outside a repo exits 1 when they differ
        return {"error": (proc.stderr.strip().splitlines() or ["git failed"])[0]}
    return {"text": proc.stdout[:4000]}


def build_registry(repo):
    repo = Path(repo)

    def git_log(max_count=10, path=None):
        args = ["log", "-n", str(max_count), "--format=%h %ad %s", "--date=short"]
        if path is not None:
            args.append(path)
        return _git(repo, args)

    def git_show(rev):
        return _git(repo, ["show", "--stat", "--patch", rev])

    def git_diff(rev_from, rev_to="HEAD"):
        return _git(repo, ["diff", rev_from, rev_to])

    def git_commit(message, paths):
        result = _git(repo, ["add", *paths])
        if "error" in result:
            return result
        return _git(repo, ["commit", "-q", "-m", message, *paths])

    def spec(fn, description, properties, required, permission):
        return {"fn": fn, "description": description, "permission": permission,
                "parameters": {"type": "object", "properties": properties, "required": required}}

    return {
        "git_log": spec(git_log, "List recent commits in the repository, newest first.",
                        {"max_count": {"type": "integer"}, "path": {"type": "string"}}, [], "read"),
        "git_show": spec(git_show, "Show one commit.", {"rev": {"type": "string"}}, ["rev"], "read"),
        "git_diff": spec(git_diff, "Show the changes between two commits.",
                         {"rev_from": {"type": "string"}, "rev_to": {"type": "string"}},
                         ["rev_from"], "read"),
        "git_commit": spec(git_commit, "Commit the given files with a message.",
                           {"message": {"type": "string"},
                            "paths": {"type": "array", "items": {"type": "string"}}},
                           ["message", "paths"], "write"),
    }
