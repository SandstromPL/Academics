"""Step 3: the client side, and the adapter from MCP tools to native tools.

StdioMCPClient starts a server as a subprocess and speaks JSON-RPC to it
over its stdin/stdout: initialize, notifications/initialized, tools/list,
tools/call. mcp_tools_to_openai() turns the tools/list answer into the
tools= list that client.chat.completions.create() takes (Lab 6b's
build_native_tools, with the registry now on the far side of a pipe).
"""
import hashlib
import json
import subprocess
import sys

PROTOCOL_VERSION = "2025-11-25"
CLIENT_INFO = {"name": "csp352-agent", "version": "0.1.0"}


class MCPError(Exception):
    def __init__(self, error):
        super().__init__(f"{error.get('code')}: {error.get('message')}")
        self.code = error.get("code")


class StdioMCPClient:
    def __init__(self, command, stderr=None, timeout=10):
        # stderr=None lets the server's log lines show in your terminal.
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=stderr, text=True, bufsize=1)
        self.next_id = 1
        self.last_request_id = None
        self.server_info = None
        self.timeout = timeout

    # --------------------------------------------------------- transport
    def _send(self, msg):
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def _read(self):
        line = self.proc.stdout.readline()
        if not line:
            raise ConnectionError("server closed its stdout (did it crash? read its stderr)")
        return json.loads(line)

    def request(self, method, params=None):
        msg_id = self.next_id
        self.next_id += 1
        msg = {"jsonrpc": "2.0", "id": msg_id, "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)
        self.last_request_id = msg_id
        while True:
            reply = self._read()
            if "method" in reply:
                # A request or notification from the server. This client
                # offers no client features, so it declines any request.
                if "id" in reply:
                    self._send({"jsonrpc": "2.0", "id": reply["id"],
                                "error": {"code": -32601, "message": "not supported"}})
                continue
            if reply.get("id") != msg_id:
                continue
            if "error" in reply:
                raise MCPError(reply["error"])
            return reply["result"]

    def notify(self, method, params=None):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)

    # --------------------------------------------------------- lifecycle
    def initialize(self):
        result = self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": CLIENT_INFO,
        })
        if result["protocolVersion"] != PROTOCOL_VERSION:
            # A real client checks this against its own supported list.
            print(f"[client] server answered protocol {result['protocolVersion']}", file=sys.stderr)
        self.server_info = result.get("serverInfo")
        self.notify("notifications/initialized")
        return result

    def list_tools(self):
        tools, cursor = [], None
        while True:
            result = self.request("tools/list", {"cursor": cursor} if cursor else None)
            tools.extend(result["tools"])
            cursor = result.get("nextCursor")
            if not cursor:
                return tools

    def call_tool(self, name, arguments, meta=None):
        params = {"name": name, "arguments": arguments}
        if meta:
            params["_meta"] = meta
        return self.request("tools/call", params)

    def close(self):
        # stdio shutdown: close the server's input, then wait for it to exit.
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, *exc):
        self.close()


# ------------------------------------------------------------- the adapter
def mcp_tools_to_openai(mcp_tools):
    """tools/list -> tools=. inputSchema is already JSON Schema, so it is
    copied straight into "parameters", as in Lab 6b."""
    return [
        {"type": "function", "function": {
            "name": t["name"],
            "description": t.get("description", ""),
            "parameters": t.get("inputSchema") or {"type": "object", "properties": {}},
        }}
        for t in mcp_tools
    ]


def result_to_text(result):
    """tools/call result -> the string for the {"role": "tool"} message."""
    parts = []
    for item in result.get("content", []):
        if item.get("type") == "text":
            parts.append(item["text"])
        else:
            parts.append(f"[{item.get('type')} content not shown to the model]")
    return "\n".join(parts)


def tools_fingerprint(mcp_tools):
    """A hash of the tool definitions. Pin it when you review a server; if it
    changes later (a "rug pull"), stop and review again."""
    canonical = json.dumps(sorted(mcp_tools, key=lambda t: t["name"]), sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


if __name__ == "__main__":
    # python3 mcp_client.py world/sandbox : show tools/list and the adapter's output
    root = sys.argv[1] if len(sys.argv) > 1 else "world/sandbox"
    with StdioMCPClient([sys.executable, "file_server.py", "--root", root, "--quiet"]) as mcp:
        tools = mcp.list_tools()
        print("server:", mcp.server_info)
        print("tools/list ->", [t["name"] for t in tools])
        print("fingerprint:", tools_fingerprint(tools))
        print(json.dumps(mcp_tools_to_openai(tools)[1], indent=2))
