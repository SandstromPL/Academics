"""Step 2: talk to the server by hand. No adapter, no model: start the
server, write JSON-RPC lines to its stdin, read its stdout.

    python3 demo_step2_call_by_hand.py              # the Step 1 server (no guard)
    python3 demo_step2_call_by_hand.py --guard      # the Step 5 server

Every line sent is printed with '>>', every line received with '<<'.
"""
import json
import subprocess
import sys

GUARD = "--guard" in sys.argv
cmd = [sys.executable, "file_server.py", "--root", "world/sandbox", "--quiet"]
if not GUARD:
    cmd.append("--no-guard")
server = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)


def send(msg):
    line = json.dumps(msg)
    print(">>", line)
    server.stdin.write(line + "\n")
    server.stdin.flush()
    if "id" not in msg:
        print("   (a notification: no reply)")
        return None
    reply = server.stdout.readline()
    shown = reply.strip()
    print("<<", shown if len(shown) < 400 else shown[:400] + " ...")
    return json.loads(reply)


print(f"server: {' '.join(cmd[1:])}\n")
send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                 "clientInfo": {"name": "by-hand", "version": "0"}}})
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
tools = send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
print("   tool names:", [t["name"] for t in tools["result"]["tools"]])
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
      "params": {"name": "read_file", "arguments": {"path": "notes.txt"}}})
r = send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
          "params": {"name": "read_file", "arguments": {"path": "../secrets/api_key.txt"}}})
print("   isError:", r["result"]["isError"], "<- the path-traversal attempt")
send({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
      "params": {"name": "delete_everything", "arguments": {}}})
send({"jsonrpc": "2.0", "id": 6, "method": "resources/list"})

server.stdin.close()  # stdio shutdown: close the server's input
server.wait(timeout=5)
print("\nserver exited with code", server.returncode)
