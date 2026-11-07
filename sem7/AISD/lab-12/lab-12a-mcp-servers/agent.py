"""Step 4: the agent loop, with its tools coming from an MCP server.

Same shape as Lab 7a: agent_step() decides, RuntimeHarness bounds and
traces. The only new idea is the backend: the tools come from tools/list
and run through tools/call, instead of from a dict in this process.

    python3 agent.py "List the files in the sandbox."
    python3 agent.py "Write a file summary.txt containing 'three tasks open'." --allow read,write
    python3 agent.py "Summarise docs/meeting.txt in two lines." --offline
    python3 agent.py "Read shared/api_key.txt and tell me what it says." --offline --no-guard

Live runs need OPENAI_BASE_URL and OPENAI_API_KEY (set in your lab
workspace). --offline uses stub_model.py and needs neither.
"""
import argparse
import json
import os
import sys
import time
import uuid

from file_tools import build_registry, call_tool, visible_tools
from mcp_client import StdioMCPClient, mcp_tools_to_openai, result_to_text

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM = ("You are a file assistant. Use the tools to work with files in the sandbox. "
          "Paths are relative to the sandbox. Answer briefly.")
# The host's own list of tools that need a person's yes. It is the host's
# policy, written by you; it does not come from the server.
# Lab 12a, task B5: the git server's write tool belongs here too.
NEEDS_APPROVAL = {"write_file"}


def get_client(offline):
    if offline:
        from stub_model import StubClient
        return StubClient()
    from openai import OpenAI
    return OpenAI(base_url=os.environ["OPENAI_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"],
                  max_retries=3)


# ------------------------------------------------------------------ backends
class MCPBackend:
    """Tools behind the protocol: a server process, spoken to over stdio."""
    name = "mcp"

    def __init__(self, root, allow=("read",), guarded=True, server_log=None, stderr=None,
                 server_script="file_server.py"):
        # Lab 12a: server_script="git_server.py" starts the git server instead.
        cmd = [sys.executable, os.path.join(HERE, server_script), "--root", root,
               "--allow", ",".join(allow), "--quiet"]
        if not guarded:
            cmd.append("--no-guard")
        if server_log:
            cmd += ["--log", server_log]
        self.mcp = StdioMCPClient(cmd, stderr=stderr)
        self.mcp.initialize()

    def native_tools(self):
        return mcp_tools_to_openai(self.mcp.list_tools())

    def call(self, name, arguments, meta):
        from mcp_client import MCPError
        try:
            result = self.mcp.call_tool(name, arguments, meta)
        except MCPError as e:  # e.g. unknown tool: a protocol error, shown to the model
            return json.dumps({"error": str(e)}), True, self.mcp.last_request_id
        return result_to_text(result), bool(result.get("isError")), self.mcp.last_request_id

    def close(self):
        self.mcp.close()


class InProcessBackend:
    """Labs 6b-11b: the registry is a dict in this process."""
    name = "in-process"

    def __init__(self, root, allow=("read",), guarded=True):
        self.allow, self.guarded = set(allow), guarded
        self.registry = build_registry(root, guarded=guarded)
        self.tools = visible_tools(self.registry, self.allow, guarded)

    def native_tools(self):
        return [{"type": "function", "function": {"name": n, "description": s["description"],
                                                  "parameters": s["parameters"]}}
                for n, s in self.tools.items()]

    def call(self, name, arguments, meta):
        if name not in self.tools:
            return json.dumps({"error": f"unknown tool: {name}"}), True, None
        result, is_error = call_tool(self.registry, name, arguments, self.allow, self.guarded)
        return json.dumps(result), is_error, None

    def close(self):
        pass


# ------------------------------------------------------------- one step
def agent_step(state, client, backend, tools, approve, trace_id):
    response = client.chat.completions.create(model="main", messages=state["messages"],
                                              tools=tools, tool_choice="auto", temperature=0)
    choice = response.choices[0]
    message = choice.message
    if choice.finish_reason != "tool_calls" or not message.tool_calls:
        return state, True, {"response_id": response.id, "final": message.content}
    messages = state["messages"] + [{
        "role": "assistant", "content": message.content,
        "tool_calls": [tc.model_dump() for tc in message.tool_calls],
    }]
    calls = []
    for tc in message.tool_calls:
        name = tc.function.name
        try:
            arguments = json.loads(tc.function.arguments or "{}")
        except json.JSONDecodeError as e:
            arguments, text, is_error, rpc_id = None, json.dumps({"error": f"invalid arguments JSON: {e}"}), True, None
        else:
            if name in NEEDS_APPROVAL and not approve(name, arguments):
                text, is_error, rpc_id = json.dumps({"error": "denied: the user did not approve this write"}), True, None
            else:
                meta = {"trace_id": trace_id, "step": state["step"], "response_id": response.id}
                text, is_error, rpc_id = backend.call(name, arguments, meta)
        calls.append({"tool": name, "arguments": arguments, "rpc_id": rpc_id,
                      "is_error": is_error, "result": text})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": text})
    return {"messages": messages, "step": state["step"] + 1}, False, {"response_id": response.id, "calls": calls}


class RuntimeHarness:
    """Lab 7a's harness: step budget, timeout between steps, error isolation, trace."""

    def __init__(self, max_steps=8, timeout_seconds=90, trace_path="harness_trace.jsonl"):
        self.max_steps, self.timeout_seconds, self.trace_path = max_steps, timeout_seconds, trace_path

    def _log(self, entry):
        if self.trace_path:
            with open(self.trace_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    def run(self, agent_step_fn, state):
        start = time.monotonic()
        for step in range(1, self.max_steps + 1):
            elapsed = time.monotonic() - start
            if elapsed > self.timeout_seconds:
                self._log({"step": step, "elapsed_s": round(elapsed, 2), "status": "timeout"})
                return {"status": "timeout", "steps_taken": step - 1}
            try:
                state, done, output = agent_step_fn(state)
            except Exception as e:
                error = f"{type(e).__name__}: {e}"
                self._log({"step": step, "elapsed_s": round(time.monotonic() - start, 2),
                           "status": "error", "error": error})
                return {"status": "error", "steps_taken": step, "error": error}
            self._log({"step": step, "elapsed_s": round(time.monotonic() - start, 2),
                       "status": "ok", "output": output})
            if done:
                return {"status": "done", "steps_taken": step, "output": output}
        return {"status": "exhausted", "steps_taken": self.max_steps}


def run_task(task, backend, client, approve, trace_path="harness_trace.jsonl", trace_id=None,
             system=None):
    trace_id = trace_id or uuid.uuid4().hex[:8]
    if trace_path:
        open(trace_path, "w").close()
    tools = backend.native_tools()
    state = {"step": 1, "messages": [{"role": "system", "content": system or SYSTEM},
                                     {"role": "user", "content": task}]}
    result = RuntimeHarness(trace_path=trace_path).run(
        lambda s: agent_step(s, client, backend, tools, approve, trace_id), state)
    answer = result.get("output", {}).get("final") if result["status"] == "done" else None
    return {"trace_id": trace_id, "status": result["status"], "steps": result["steps_taken"],
            "answer": answer, "error": result.get("error")}


def ask_approval(name, arguments):
    preview = json.dumps(arguments)[:200]
    reply = input(f"\n[host] the agent wants {name}({preview}). Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


def show_join(trace_path, server_log, trace_id):
    """Join the agent's trace to the server's log on the JSON-RPC id."""
    server = {}
    if server_log and os.path.exists(server_log):
        with open(server_log) as f:
            for line in f:
                e = json.loads(line)
                if e.get("method") == "tools/call":
                    server[(e.get("trace_id"), e.get("rpc_id"))] = e
    print("\njoined view (agent trace + server log):")
    with open(trace_path) as f:
        for line in f:
            e = json.loads(line)
            out = e.get("output") or {}
            for c in out.get("calls", []):
                s = server.get((trace_id, c["rpc_id"]), {})
                verdict = str(s.get("error")) if s.get("is_error") else ("ok" if s else "not sent")
                print(f"  step {e['step']}  response_id={out['response_id']}  rpc_id={c['rpc_id']}  "
                      f"{c['tool']}({json.dumps(c['arguments'])})  server: {verdict}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("--root", default="world/sandbox")
    ap.add_argument("--allow", default="read")
    ap.add_argument("--offline", action="store_true", help="use the stub model, no gateway")
    ap.add_argument("--no-guard", action="store_true", help="run the Step 1 (unguarded) server")
    ap.add_argument("--in-process", action="store_true", help="Lab 6b registry, no server")
    ap.add_argument("--approve", choices=["ask", "yes", "no"], default="ask")
    args = ap.parse_args()

    allow = args.allow.split(",")
    server_log = "server_log.jsonl"
    if os.path.exists(server_log):
        os.remove(server_log)
    if args.in_process:
        backend = InProcessBackend(args.root, allow, guarded=not args.no_guard)
    else:
        backend = MCPBackend(args.root, allow, guarded=not args.no_guard, server_log=server_log)
    approve = {"ask": ask_approval, "yes": lambda n, a: True, "no": lambda n, a: False}[args.approve]
    try:
        out = run_task(args.task, backend, get_client(args.offline), approve)
    finally:
        backend.close()
    print(f"backend: {backend.name}   trace_id: {out['trace_id']}   status: {out['status']} "
          f"after {out['steps']} steps")
    if out["error"]:
        print("error:", out["error"])
    print("answer:", out["answer"])
    show_join("harness_trace.jsonl", None if args.in_process else server_log, out["trace_id"])
