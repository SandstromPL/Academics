"""Lab 12b: the NAIVE code-execution tool (given; do not copy this into exec_tools.py).

It runs the snippet in a new process and nothing else: same environment as
the server (your API key included), no resource limits, no audit hook, and
only a 20-second safety timeout so the eval itself cannot hang. Running a
snippet in a subprocess is not a sandbox; this file is what that looks like.

lab12b.py eval runs your exec_tools.py ("guarded") against this ("naive").
"""
import subprocess
import sys
from pathlib import Path

SAFETY_TIMEOUT_S = 20


def build_registry(scratch):
    scratch = Path(scratch)

    def run_python(code):
        scratch.mkdir(parents=True, exist_ok=True)
        try:
            p = subprocess.run([sys.executable, "-c", code], cwd=str(scratch), capture_output=True,
                               text=True, timeout=SAFETY_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": f"killed after {SAFETY_TIMEOUT_S} s", "exit_code": None,
                    "timed_out": True, "truncated": False}
        return {"stdout": p.stdout[:4000], "stderr": p.stderr[:4000], "exit_code": p.returncode,
                "timed_out": False, "truncated": False}

    return {"run_python": {"fn": run_python, "description": "Run a short Python 3 program and return its output.",
                           "parameters": {"type": "object", "properties": {"code": {"type": "string"}},
                                          "required": ["code"]},
                           "permission": "execute"}}
