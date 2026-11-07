"""The production route: the same read-only file server, written with the
official MCP Python SDK (package `mcp`, installed in the lab workspace image).

The SDK writes the JSON-RPC loop, the lifecycle and the inputSchema (from
the type hints and docstring) for you. It does NOT write your guard: the
path check is still yours, so it reuses guard.py.

    python3 sdk_file_server.py --root world/sandbox

Our hand-written client talks to it unchanged:
    python3 -c "from mcp_client import *; c=StdioMCPClient(['python3','sdk_file_server.py']); c.initialize(); print([t['name'] for t in c.list_tools()]); c.close()"
"""
import argparse

try:  # mcp 2.x renamed FastMCP to MCPServer
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

from guard import resolve_in_root

ap = argparse.ArgumentParser()
ap.add_argument("--root", default="world/sandbox")
ROOT = ap.parse_args().root

mcp = FastMCP("csp352-files-sdk")


@mcp.tool()
def list_files(directory: str = ".") -> list[str]:
    """List the files and folders in a sandbox directory."""
    d = resolve_in_root(ROOT, directory)
    return sorted(p.name + ("/" if p.is_dir() else "") for p in d.iterdir())


@mcp.tool()
def read_file(path: str) -> str:
    """Read a text file in the sandbox."""
    return resolve_in_root(ROOT, path).read_text()[:4000]


if __name__ == "__main__":
    mcp.run()  # stdio by default; mcp.run(transport="streamable-http") serves HTTP instead
