"""Lab 12a: the git server (given). Your work is in git_tools.py.

The same server as file_server.py -- same JSON-RPC loop, same lifecycle,
same tools/list and tools/call -- with the git tools in place of the file
tools. Only the registry changes; the protocol code does not. That is the
point of a protocol.

    python3 git_server.py --root git_world/repo                      # guarded, read only
    python3 git_server.py --root git_world/repo --allow read,write   # git_commit offered too
    python3 git_server.py --root git_world/repo --no-guard           # naive_git_tools.py
"""
import argparse
import json
import sys

import naive_git_tools
from file_server import FileServer
from file_tools import visible_tools

SERVER_INFO = {"name": "csp352-git", "version": "0.1.0"}


class GitServer(FileServer):
    def __init__(self, root, granted=("read",), guarded=True, log_path=None, stderr=sys.stderr):
        self.granted = set(granted)
        self.guarded = guarded
        if guarded:
            import git_tools  # your code
            self.registry = git_tools.build_registry(root)
        else:
            self.registry = naive_git_tools.build_registry(root)
        self.tools = visible_tools(self.registry, self.granted, guarded)
        self.initialized = False
        self.ready = False
        self.log_path = log_path
        self.stderr = stderr

    def tools_call(self, msg_id, params):
        # A bug in a tool must not kill the server: report it as a tool error.
        try:
            return super().tools_call(msg_id, params)
        except Exception as e:  # noqa: BLE001 -- the server keeps serving
            self.log({"rpc_id": msg_id, "method": "tools/call", "tool": params.get("name"),
                      "is_error": True, "error": f"server bug: {type(e).__name__}: {e}"})
            text = json.dumps({"error": f"server bug: {type(e).__name__}: {e}"})
            return {"jsonrpc": "2.0", "id": msg_id,
                    "result": {"content": [{"type": "text", "text": text}], "isError": True}}

    def initialize(self, params):
        result = super().initialize(params)
        result["serverInfo"] = SERVER_INFO
        result["instructions"] = ("Git tools over one repository. Revisions are HEAD, HEAD~N, "
                                  "HEAD^ or a commit hash; paths are relative to the repository.")
        return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="The Lab 12a MCP git server over stdio.")
    ap.add_argument("--root", required=True, help="the repository")
    ap.add_argument("--allow", default="read", help="granted permissions, e.g. read or read,write")
    ap.add_argument("--no-guard", action="store_true", help="serve naive_git_tools.py instead")
    ap.add_argument("--log", default=None, help="append one JSON line per request to this file")
    ap.add_argument("--quiet", action="store_true", help="no log lines on stderr")
    args = ap.parse_args(argv)

    server = GitServer(args.root, granted=args.allow.split(","), guarded=not args.no_guard,
                       log_path=args.log, stderr=None if args.quiet else sys.stderr)
    if not args.quiet:
        print(f"[server] ready: repo={args.root} guarded={server.guarded} "
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
