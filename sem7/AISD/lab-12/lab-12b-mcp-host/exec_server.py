"""Lab 12b: the code-execution MCP server (given). Your work is in exec_tools.py.

The same server as file_server.py and git_server.py -- same JSON-RPC loop,
same lifecycle -- with run_python in place of the file tools.

    python3 exec_server.py --root exec_world/scratch                # guarded (exec_tools.py)
    python3 exec_server.py --root exec_world/scratch --no-guard     # naive_exec_tools.py
"""
import argparse
import json
import sys

import naive_exec_tools
from file_server import FileServer
from file_tools import visible_tools

SERVER_INFO = {"name": "csp352-exec", "version": "0.1.0"}


class ExecServer(FileServer):
    def __init__(self, root, granted=("execute",), guarded=True, log_path=None, stderr=sys.stderr):
        self.granted = set(granted)
        self.guarded = guarded
        if guarded:
            import exec_tools  # your code
            self.registry = exec_tools.build_registry(root)
        else:
            self.registry = naive_exec_tools.build_registry(root)
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
            text = json.dumps({"error": f"server bug: {type(e).__name__}: {e}"})
            return {"jsonrpc": "2.0", "id": msg_id,
                    "result": {"content": [{"type": "text", "text": text}], "isError": True}}

    def initialize(self, params):
        result = super().initialize(params)
        result["serverInfo"] = SERVER_INFO
        result["instructions"] = "Runs short Python programs in a sandbox folder."
        return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="The Lab 12b MCP code-execution server over stdio.")
    ap.add_argument("--root", required=True, help="the scratch directory")
    ap.add_argument("--allow", default="execute")
    ap.add_argument("--no-guard", action="store_true", help="serve naive_exec_tools.py instead")
    ap.add_argument("--log", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    server = ExecServer(args.root, granted=args.allow.split(","), guarded=not args.no_guard,
                        log_path=args.log, stderr=None if args.quiet else sys.stderr)
    for line in sys.stdin:
        if line.strip():
            response = server.handle_line(line)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
