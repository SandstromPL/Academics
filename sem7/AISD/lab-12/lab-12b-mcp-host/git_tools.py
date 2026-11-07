"""Lab 12a, Part B: the git server's tools (Lab 12a reference solution, given in Lab 12b).

Same registry shape as file_tools.py: one entry per tool with fn,
description, parameters (real JSON Schema) and permission. git_server.py
serves it over MCP; call_tool() and visible_tools() from file_tools.py run
it, so the permission check, the argument-type check and GuardError
handling are the same as the file server's.
"""
import re
import subprocess
from pathlib import Path

from guard import GuardError, resolve_in_root

MAX_OUTPUT_CHARS = 4000
GIT_TIMEOUT_S = 10

_HEX = re.compile(r"[0-9a-f]{4,40}")
_HEAD = re.compile(r"HEAD(~[0-9]{1,2}|\^)?")


# ---------------------------------------------------------------- B6
def run_git(repo, args):
    """Run git in repo. Returns (ok, text): stdout if git succeeded, else
    the first line of stderr. Never raises."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                              timeout=GIT_TIMEOUT_S, shell=False)
    except subprocess.TimeoutExpired:
        return False, f"git timed out after {GIT_TIMEOUT_S} s"
    except OSError as e:
        return False, f"could not run git: {e}"
    if proc.returncode != 0:
        lines = proc.stderr.strip().splitlines()
        if lines:
            return False, lines[0]
        out = proc.stdout.strip().splitlines()  # "nothing to commit" goes to stdout
        return False, out[-1] if out else f"git exited with {proc.returncode}"
    return True, proc.stdout


# ---------------------------------------------------------------- B1
def check_rev(rev):
    """Return rev if it is one of the revision forms this server accepts,
    else raise GuardError. An allow-list, not a block-list."""
    if not isinstance(rev, str) or not (_HEX.fullmatch(rev) or _HEAD.fullmatch(rev)):
        raise GuardError(f"not an accepted revision: {rev!r} "
                         "(use HEAD, HEAD~N, HEAD^ or a commit hash)")
    return rev


def _truncate(text):
    return {"text": text[:MAX_OUTPUT_CHARS], "truncated": len(text) > MAX_OUTPUT_CHARS}


def build_registry(repo):
    repo = Path(repo)

    # ------------------------------------------------------------ B2
    def git_log(max_count=10, path=None):
        n = max(1, min(int(max_count), 50))
        args = ["log", f"--max-count={n}", "--format=%h%x1f%an%x1f%ad%x1f%s", "--date=short"]
        if path is not None:
            resolve_in_root(repo, path)
            args += ["--", path]
        ok, out = run_git(repo, args)
        if not ok:
            return {"error": out}
        commits = []
        for line in out.splitlines():
            sha, author, date, subject = line.split("\x1f", 3)
            commits.append({"commit": sha, "author": author, "date": date, "subject": subject})
        return {"commits": commits}

    # ------------------------------------------------------------ B3
    def git_show(rev):
        check_rev(rev)
        ok, out = run_git(repo, ["show", "--stat", "--patch", rev, "--"])
        if not ok:
            return {"error": out}
        return {"rev": rev, **_truncate(out)}

    # ------------------------------------------------------------ B4
    def git_diff(rev_from, rev_to="HEAD"):
        check_rev(rev_from)
        check_rev(rev_to)
        ok, out = run_git(repo, ["diff", rev_from, rev_to, "--"])
        if not ok:
            return {"error": out}
        return {"rev_from": rev_from, "rev_to": rev_to, **_truncate(out)}

    # ------------------------------------------------------------ B5
    def git_commit(message, paths):
        if not isinstance(message, str) or not message.strip():
            return {"error": "message must be a non-empty string"}
        if len(message) > 200 or "\n" in message or "\r" in message:
            return {"error": "message must be one line of at most 200 characters"}
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
            return {"error": "paths must be a non-empty list of strings"}
        for p in paths:
            real = resolve_in_root(repo, p)
            if not real.is_file():
                return {"error": f"no such file in the repo: {p}"}
        ok, out = run_git(repo, ["add", "--", *paths])
        if not ok:
            return {"error": out}
        ok, out = run_git(repo, ["commit", "-q", "-m", message, "--", *paths])
        if not ok:
            return {"error": out}
        ok, sha = run_git(repo, ["rev-parse", "--short", "HEAD"])
        return {"commit": sha.strip(), "files": paths}

    return {
        "git_log": {
            "fn": git_log,
            "description": "List recent commits in the repository, newest first. "
                           "Optionally only the commits that touched one file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_count": {"type": "integer", "description": "How many commits (1-50). Default 10."},
                    "path": {"type": "string", "description": "A file path relative to the repository."},
                },
                "required": [],
            },
            "permission": "read",
        },
        "git_show": {
            "fn": git_show,
            "description": "Show one commit: its message, the files it changed and its diff.",
            "parameters": {
                "type": "object",
                "properties": {"rev": {"type": "string",
                                       "description": "HEAD, HEAD~N, HEAD^ or a commit hash."}},
                "required": ["rev"],
            },
            "permission": "read",
        },
        "git_diff": {
            "fn": git_diff,
            "description": "Show the changes between two commits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rev_from": {"type": "string", "description": "The older commit (HEAD~N or a hash)."},
                    "rev_to": {"type": "string", "description": "The newer commit. Default HEAD."},
                },
                "required": ["rev_from"],
            },
            "permission": "read",
        },
        "git_commit": {
            "fn": git_commit,
            "description": "Commit the current contents of the given files with a one-line message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "One line, at most 200 characters."},
                    "paths": {"type": "array", "items": {"type": "string"},
                              "description": "File paths relative to the repository."},
                },
                "required": ["message", "paths"],
            },
            "permission": "write",
        },
    }
