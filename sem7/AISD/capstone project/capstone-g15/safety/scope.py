"""write_file scope guard (code-enforced safety control).

check_write(path, case_client) -> (allowed: bool, reason: str)

A write is allowed only if the resolved path equals the current case's client
file. Writes to data/libv/, the client tests, other clients, or anything
outside the repo are denied. Every decision is returned as a gate record that
the harness writes to the trace.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def _resolve(path):
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    return os.path.realpath(p)

def check_write(path, case_client):
    target = _resolve(path)
    allowed_path = _resolve(case_client)
    if target == allowed_path:
        return True, "allowed: current case client file"
    rel = os.path.relpath(target, ROOT)
    if rel.startswith(".."):
        return False, "denied: outside the repository"
    if rel.startswith(os.path.join("data", "libv")):
        return False, "denied: library files are read-only"
    if rel.startswith(os.path.join("data", "clients", "tests")):
        return False, "denied: client tests are read-only"
    if rel.startswith(os.path.join("data", "clients")):
        return False, "denied: not the current case's client file"
    return False, "denied: path not writable"

def gate_record(path, case_client, case_id):
    ok, reason = check_write(path, case_client)
    return {
        "type": "gate",
        "case_id": case_id,
        "tool": "write_file",
        "path": path,
        "resolved": os.path.relpath(_resolve(path), ROOT),
        "decision": "allow" if ok else "deny",
        "reason": reason,
    }
