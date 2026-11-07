"""Lab 12b, Part B: one host, three MCP servers -- YOUR WORK GOES HERE (B1, B2, B3).

The host starts the file, git and code-execution servers, offers the model
ALL their tools at once, sends each call to the server that owns it, and asks
a person before any tool on its approval list runs.
"""
import json

from agent import MCPBackend
from mcp_client import mcp_tools_to_openai

SEP = "__"
SERVERS = {  # server name -> (script, granted permissions)
    "files": ("file_server.py", ["read", "write"]),
    "git": ("git_server.py", ["read", "write"]),
    "code": ("exec_server.py", ["execute"]),
}

# ------------------------------------------------------------------ B3
# The host's own policy: which namespaced tools need a person's yes before
# they run. It does not come from any server. Every tool that writes or
# executes, on any server, belongs here.
NEEDS_APPROVAL = set()


# ------------------------------------------------------------------ B1
def namespaced_tools(listings):
    """listings: {server: [MCP tool dicts from that server's tools/list]}.
    Return the tools= list for the model (use mcp_tools_to_openai), with
    each tool named "<server>__<tool>" (SEP between them) and its
    description starting "[<server>] ". Two servers may both offer a tool
    with the same name; after this, no two names are equal."""
    return []


# ------------------------------------------------------------------ B2
def route(name, servers):
    """"git__git_log" -> ("git", "git_log"). Raise KeyError for anything that
    is not a known server name, then SEP, then a non-empty tool name
    (split on the FIRST SEP only)."""
    raise KeyError(f"route not implemented yet (task B2): {name!r}")


class MultiHost:
    """Given. A backend for agent.run_task: native_tools(), call(), close()."""
    name = "multi"

    def __init__(self, roots, guarded_exec=True, stderr=None):
        self.servers = {}
        for server, (script, allow) in SERVERS.items():
            self.servers[server] = MCPBackend(str(roots[server]), allow,
                                              guarded=(guarded_exec or server != "code"),
                                              stderr=stderr, server_script=script)
        self._listings = {s: b.mcp.list_tools() for s, b in self.servers.items()}

    def native_tools(self):
        return namespaced_tools(self._listings)

    def call(self, name, arguments, meta):
        try:
            server, tool = route(name, self.servers)
        except KeyError as e:
            return json.dumps({"error": e.args[0] if e.args else "unknown tool"}), True, None
        return self.servers[server].call(tool, arguments, meta)

    def close(self):
        for b in self.servers.values():
            b.close()
