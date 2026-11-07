"""Step 1 (and Step 5): a minimal MCP server over stdio, written from
scratch with the standard library only.

Transport: one JSON-RPC 2.0 message per line on stdin, one per line on
stdout. stdout carries protocol messages and nothing else; human-readable
logs go to stderr, and an optional JSONL log goes to --log.

Methods handled: initialize, notifications/initialized, ping, tools/list,
tools/call. Anything else gets JSON-RPC error -32601.

    python3 file_server.py --root world/sandbox --no-guard     # Step 1: naive paths
    python3 file_server.py --root world/sandbox                # Step 5: guarded, read only
    python3 file_server.py --root world/sandbox --allow read,write --log server_log.jsonl
"""
import argparse
import json
import sys
import time

from file_tools import build_registry, call_tool, visible_tools

SERVER_INFO = {"name": "csp352-files", "version": "0.1.0"}
# Protocol versions are dates. The first one is our latest.
SUPPORTED_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]

PARSE_ERROR, INVALID_REQUEST, METHOD_NOT_FOUND, INVALID_PARAMS = -32700, -32600, -32601, -32602


def ok(msg_id, result):
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def err(msg_id, code, message):
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


class FileServer:
    def __init__(self, root, granted=("read",), guarded=True, log_path=None, stderr=sys.stderr):
        self.granted = set(granted)
        self.guarded = guarded
        self.registry = build_registry(root, guarded=guarded)
        self.tools = visible_tools(self.registry, self.granted, guarded)
        self.initialized = False  # set by the initialize request
        self.ready = False        # set by notifications/initialized
        self.log_path = log_path
        self.stderr = stderr

    # ------------------------------------------------------------ logging
    def log(self, entry):
        entry = {"ts": round(time.time(), 3), **entry}
        if self.stderr:
            print(f"[server] {json.dumps(entry)}", file=self.stderr, flush=True)
        if self.log_path:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    # ----------------------------------------------------------- dispatch
    def handle_line(self, line):
        """One line in, at most one response out (None for a notification)."""
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as e:
            return err(None, PARSE_ERROR, f"parse error: {e}")
        if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or "method" not in msg:
            return err(msg.get("id") if isinstance(msg, dict) else None, INVALID_REQUEST,
                       "invalid request")
        return self.handle(msg)

    def handle(self, msg):
        method = msg["method"]
        params = msg.get("params") or {}
        if "id" not in msg:  # a notification: never answered
            if method == "notifications/initialized":
                self.ready = True
            return None
        msg_id = msg["id"]

        if method == "initialize":
            return ok(msg_id, self.initialize(params))
        if method == "ping":
            return ok(msg_id, {})
        if not self.initialized:
            return err(msg_id, INVALID_REQUEST, "server not initialized")
        if method == "tools/list":
            return ok(msg_id, {"tools": [self.describe(n, s) for n, s in self.tools.items()]})
        if method == "tools/call":
            return self.tools_call(msg_id, params)
        return err(msg_id, METHOD_NOT_FOUND, f"method not found: {method}")

    def initialize(self, params):
        self.initialized = True
        asked = params.get("protocolVersion")
        # Same version if we support it, else our latest; the client decides
        # whether it can live with the answer.
        version = asked if asked in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]
        self.log({"method": "initialize", "client": params.get("clientInfo"), "version": version})
        return {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER_INFO,
            "instructions": "File tools over one sandbox directory. Paths are relative to it.",
        }

    @staticmethod
    def describe(name, spec):
        # The registry's "parameters" IS the MCP "inputSchema": same JSON Schema.
        return {"name": name, "description": spec["description"], "inputSchema": spec["parameters"]}

    def tools_call(self, msg_id, params):
        name = params.get("name")
        arguments = params.get("arguments") or {}
        meta = params.get("_meta") or {}
        if name not in self.tools:
            # A tool this server does not offer (including one it holds back
            # for lack of permission) is a protocol error, not a tool result.
            self.log({"rpc_id": msg_id, "method": "tools/call", "tool": name, "outcome": "unknown tool",
                      "trace_id": meta.get("trace_id"), "response_id": meta.get("response_id")})
            return err(msg_id, INVALID_PARAMS, f"unknown tool: {name}")
        result, is_error = call_tool(self.registry, name, arguments, self.granted, self.guarded)
        self.log({"rpc_id": msg_id, "method": "tools/call", "tool": name, "arguments": arguments,
                  "is_error": is_error, "error": result.get("error"),
                  "trace_id": meta.get("trace_id"), "step": meta.get("step"),
                  "response_id": meta.get("response_id")})
        return ok(msg_id, {"content": [{"type": "text", "text": json.dumps(result)}],
                           "isError": is_error})


def main(argv=None):
    ap = argparse.ArgumentParser(description="A minimal MCP file server over stdio.")
    ap.add_argument("--root", required=True, help="the sandbox directory")
    ap.add_argument("--allow", default="read", help="granted permissions, e.g. read or read,write")
    ap.add_argument("--no-guard", action="store_true", help="Step 1 behaviour: naive paths, no checks")
    ap.add_argument("--log", default=None, help="append one JSON line per request to this file")
    ap.add_argument("--quiet", action="store_true", help="no log lines on stderr")
    args = ap.parse_args(argv)

    server = FileServer(args.root, granted=args.allow.split(","), guarded=not args.no_guard,
                        log_path=args.log, stderr=None if args.quiet else sys.stderr)
    if not args.quiet:
        print(f"[server] ready: root={args.root} guarded={server.guarded} "
              f"tools={list(server.tools)}", file=sys.stderr, flush=True)
    for line in sys.stdin:
        if not line.strip():
            continue
        response = server.handle_line(line)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
