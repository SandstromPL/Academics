"""Lab 12a, Part B: the git server's tools. YOUR WORK GOES HERE.

Same registry shape as file_tools.py: one entry per tool with fn,
description, parameters (real JSON Schema) and permission. git_server.py
serves it over MCP. call_tool() and visible_tools() from file_tools.py run
it, so the permission check, the argument-type check and the handling of
GuardError are already done for you: raise GuardError from a tool and the
model gets {"error": "refused: <your message>"} with isError true.

The descriptions and schemas below are given (the model reads them). The
bodies are yours. Read README.md, Part B, for each task's exact contract.
Check your progress with:  python3 lab12a.py check
"""
import re  # noqa: F401  -- you will want it for check_rev
import subprocess  # noqa: F401
from pathlib import Path

from guard import GuardError, resolve_in_root  # noqa: F401

MAX_OUTPUT_CHARS = 4000
GIT_TIMEOUT_S = 10


# ---------------------------------------------------------------- B6
def run_git(repo, args):
    """Run `git -C <repo> <args...>` and return (ok, text).

    ok True:  text is git's stdout (exit code 0).
    ok False: any non-zero exit. text is the first line of git's stderr; if
              stderr is empty (e.g. "nothing to commit" prints to stdout),
              the last line of stdout; else "git exited with <code>".
    Rules: subprocess.run with an argument LIST, never shell=True; timeout GIT_TIMEOUT_S;
    never raises (a timeout or a missing git binary is (False, reason)).
    """
    return False, "run_git not implemented yet (task B6)"


# ---------------------------------------------------------------- B1
def check_rev(rev):
    """Return rev unchanged if it is one of the forms this server accepts:
        HEAD     HEAD~N (N = 0-99)     HEAD^     a hex commit hash, 4-40 chars (lowercase)
    and raise GuardError for anything else. Write an ALLOW-list (what is
    accepted), not a block-list (what is refused): "--output=x", "-p",
    "../secrets/api_key.txt", "HEAD:notes.md", "main..HEAD", "" and a
    non-string must all be refused.
    """
    raise GuardError("check_rev not implemented yet (task B1)")


def build_registry(repo):
    repo = Path(repo)

    # ------------------------------------------------------------ B2
    def git_log(max_count=10, path=None):
        """{"commits": [{"commit", "author", "date", "subject"}, ...]}, newest first.
        max_count clamped to 1-50. If path is given: resolve_in_root(repo, path)
        first, then pass it to git AFTER a "--"."""
        return {"error": "git_log not implemented yet (task B2)"}

    # ------------------------------------------------------------ B3
    def git_show(rev):
        """check_rev(rev); git show --stat --patch <rev> --
        -> {"rev", "text", "truncated"} (text cut at MAX_OUTPUT_CHARS)."""
        return {"error": "git_show not implemented yet (task B3)"}

    # ------------------------------------------------------------ B4
    def git_diff(rev_from, rev_to="HEAD"):
        """check_rev both; git diff <rev_from> <rev_to> --
        -> {"rev_from", "rev_to", "text", "truncated"}."""
        return {"error": "git_diff not implemented yet (task B4)"}

    # ------------------------------------------------------------ B5
    def git_commit(message, paths):
        """message: non-empty, one line, <= 200 chars. paths: non-empty list of
        strings, each resolve_in_root inside the repo and an existing file.
        git add -- <paths>; git commit -q -m <message> -- <paths>;
        then git rev-parse --short HEAD for the hash
        -> {"commit": short sha, "files": paths}.
        (A message such as "--amend" is safe: -m takes the next argument as
        the message, whatever it looks like.)
        This is the only write tool. ALSO add it to the host's NEEDS_APPROVAL
        in agent.py: the host, not this server, decides what needs a person."""
        return {"error": "git_commit not implemented yet (task B5)"}

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
