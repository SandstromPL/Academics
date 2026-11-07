"""The three file tools, as a Lab 6b-shaped registry: one entry per tool
with fn, description, parameters (real JSON Schema) and permission.

The same registry is used two ways:
  - in process, exactly as in Labs 6b-11b (InProcessBackend in agent.py);
  - behind the MCP server (file_server.py), where "parameters" is sent to
    the client as the tool's "inputSchema".

guarded=False is the Step 1 server: it joins paths naively and has no
permission check. guarded=True is the Step 5 server.
"""
import os
from pathlib import Path

from guard import GuardError, check_permission, resolve_in_root

MAX_READ_CHARS = 4000
MAX_MATCHES = 50

_TYPE_MAP = {"integer": int, "string": str, "boolean": bool, "number": (int, float)}


def validate_arguments(schema, arguments):
    """Given, unchanged from Lab 6a."""
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    for field in required:
        if field not in arguments:
            return False, f"missing required field: {field}"
    for field, value in arguments.items():
        if field in properties:
            expected_type = properties[field].get("type")
            py_type = _TYPE_MAP.get(expected_type)
            if py_type and not isinstance(value, py_type):
                return False, f"field '{field}' expected {expected_type}, got {type(value).__name__}"
    return True, None


def build_registry(root, guarded=True):
    root = Path(root)

    def locate(path):
        if guarded:
            return resolve_in_root(root, path)
        return Path(os.path.join(root, path))  # Step 1: "..", "/etc/..." and symlinks all escape

    def list_files(directory="."):
        d = locate(directory)
        if not d.is_dir():
            return {"error": f"not a directory: {directory}"}
        names = sorted(p.name + ("/" if p.is_dir() else "") for p in d.iterdir())
        return {"directory": directory, "entries": names}

    def read_file(path):
        p = locate(path)
        if not p.is_file():
            return {"error": f"no such file: {path}"}
        text = p.read_text(errors="replace")
        return {"path": path, "text": text[:MAX_READ_CHARS], "truncated": len(text) > MAX_READ_CHARS}

    def write_file(path, content):
        p = locate(path)
        if not p.parent.is_dir():
            return {"error": f"no such directory for: {path}"}
        p.write_text(content)
        return {"written": path, "chars": len(content)}

    def search_files(query):
        # Lab 12a, task A2 (reference).
        if not isinstance(query, str) or not query.strip():
            return {"error": "query must be a non-empty string"}
        top = locate(".")
        needle = query.lower()
        matches = []
        for dirpath, dirs, files in os.walk(top):  # does not descend into symlinked dirs
            dirs.sort()
            for name in sorted(files):
                rel = os.path.relpath(os.path.join(dirpath, name), top)
                try:
                    p = locate(rel)  # guarded: a symlinked FILE pointing out is refused here
                    text = p.read_text(errors="ignore")
                except (GuardError, OSError):
                    continue
                if needle in text.lower():
                    matches.append(Path(rel).as_posix())
                    if len(matches) >= MAX_MATCHES:
                        return {"query": query, "matches": sorted(matches)}
        return {"query": query, "matches": sorted(matches)}

    return {
        "list_files": {
            "fn": list_files,
            "description": "List the files and folders in a sandbox directory.",
            "parameters": {
                "type": "object",
                "properties": {"directory": {"type": "string",
                                             "description": "Path relative to the sandbox, e.g. '.' or 'docs'."}},
                "required": [],
            },
            "permission": "read",
        },
        "read_file": {
            "fn": read_file,
            "description": "Read a text file in the sandbox.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string",
                                        "description": "File path relative to the sandbox."}},
                "required": ["path"],
            },
            "permission": "read",
        },
        "write_file": {
            "fn": write_file,
            "description": "Create or overwrite a text file in the sandbox.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                "required": ["path", "content"],
            },
            "permission": "write",
        },
        "search_files": {
            "fn": search_files,
            "description": "Find the text files in the sandbox that contain a word or phrase "
                           "(case-insensitive). Returns their paths.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The text to look for."}},
                "required": ["query"],
            },
            "permission": "read",
        },
    }


def visible_tools(registry, granted, guarded=True):
    """Least privilege: a guarded server only offers the tools it is
    allowed to run. A tool that is never offered cannot be misused."""
    if not guarded:
        return dict(registry)
    return {name: spec for name, spec in registry.items() if spec["permission"] in granted}


def call_tool(registry, name, arguments, granted, guarded=True):
    """Run one tool call. Returns (result_dict, is_error). Never raises for
    a bad call: the model gets an error it can read, as in Lab 6b.
    The caller has already checked that name is a known tool."""
    spec = registry[name]
    if guarded:
        denied = check_permission(name, spec, granted)
        if denied:
            return {"error": denied}, True
    if not isinstance(arguments, dict):
        return {"error": "invalid arguments: expected an object"}, True
    valid, reason = validate_arguments(spec["parameters"], arguments)
    if not valid:
        return {"error": f"invalid arguments: {reason}"}, True
    try:
        result = spec["fn"](**arguments)
    except GuardError as e:
        return {"error": f"refused: {e}"}, True
    except TypeError as e:
        return {"error": f"dispatch failed: {e}"}, True
    except OSError as e:
        return {"error": f"{type(e).__name__}: {e.strerror or e}"}, True
    return result, "error" in result
