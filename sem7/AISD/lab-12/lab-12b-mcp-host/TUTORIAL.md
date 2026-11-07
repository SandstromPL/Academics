# Week 12 live coding: an MCP tool server, from scratch

Your Lab 6 file tools, moved out of your agent's process and behind the
Model Context Protocol. Everything here uses only the standard library plus
`openai` (for the gateway); `pytest` for the tests. The official `mcp` SDK
is not needed; `sdk_file_server.py` shows it side by side.

Run every command from this folder. Live steps need `OPENAI_BASE_URL` and
`OPENAI_API_KEY` (already set in your lab workspace). Add `--offline` to
steps 4 and 6 to use a stub model instead of the gateway.

| Step | What | File | Command |
|---|---|---|---|
| 0 | build the file world | `setup_world.py` | `python3 setup_world.py` |
| 1 | a minimal stdio MCP server | `file_server.py` (+ `file_tools.py`) | see step 2 |
| 2 | call it by hand | `demo_step2_call_by_hand.py` | `python3 demo_step2_call_by_hand.py` |
| 3 | the client adapter | `mcp_client.py` | `python3 mcp_client.py` |
| 4 | an agent loop through the gateway | `agent.py` | `python3 agent.py "List the files in the sandbox."` |
| 5 | permission check and path guard | `guard.py` | `python3 demo_step2_call_by_hand.py --guard` |
| 6 | a six-case eval | `demo_step6_eval.py` | `python3 demo_step6_eval.py --offline` |
| 7 | commit and push | | see below |

## Step 0: the world

`python3 setup_world.py` creates `world/sandbox/` (the only folder the
server may touch) and `world/secrets/api_key.txt` (a fake key that must
never leave). `world/sandbox/shared` is a symlink to `../secrets`, and
`world/sandbox/docs/meeting.txt` carries an instruction hidden in the data,
as in Week 11.

## Steps 1-2: the server, by hand

The quickest test is a pipe. Three JSON-RPC lines in, two replies out (the
middle line is a notification, so it gets none):

```
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"by-hand","version":"0"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 | python3 file_server.py --root world/sandbox --no-guard
```

`demo_step2_call_by_hand.py` does the same from Python and goes on to
`tools/call`, including `read_file` on `../secrets/api_key.txt`. Without
`--guard` that call returns the key. With `--guard` it returns
`"isError": true` and `path outside the sandbox`.

## Step 3: the adapter

`python3 mcp_client.py` starts the server, runs `initialize` and
`tools/list`, and prints one tool after `mcp_tools_to_openai()`: the
`inputSchema` is copied into `parameters`, as in Lab 6b.

## Step 4: the agent

```
python3 agent.py "List the files in the sandbox."
python3 agent.py "Write a file summary.txt containing 'three tasks open'." --allow read,write
python3 agent.py "Summarise docs/meeting.txt in two lines." --no-guard --offline
```

`write_file` asks you `Approve? [y/N]` in the terminal (`--approve yes|no`
skips the prompt). Each run writes `harness_trace.jsonl` (the agent's trace)
and `server_log.jsonl` (the server's log), and prints the two joined on the
JSON-RPC id, with the gateway's `response_id` for each step.

`--in-process` runs the same tools as a Lab 6b registry, with no server.

## Step 5: the guard

`guard.py` has `resolve_in_root()` (resolve the path, follow symlinks, then
check it is still inside the sandbox) and Lab 5b's `check_permission()`.
The server only offers the tools its `--allow` grants; read-only is the
default.

## Step 6: the eval

`python3 demo_step6_eval.py --offline` runs six cases (three tasks, three
attacks) against `in-process`, `mcp-guarded` and `mcp-naive`. Offline, the
stub model obeys the injected instruction every time, so the table is:
6/6, 6/6, 3/6. Live (without `--offline`), about 40 model calls, about 3
minutes; your numbers may differ, and `--runs 3` takes a majority of three.

## Step 7: commit and push

```
git add .gitignore *.py README.md
git commit -m "Week 12: MCP server, adapter, guard, eval"
git push
```

`.gitignore` keeps `world/` and the two `.jsonl` logs out of the commit.

## Tests

```
python3 -m pytest -q test_mcp_tutorial.py
```

All offline. They cover the guard, the protocol (initialize, notifications,
error codes, `tools/list`, `tools/call`, `isError`), a real subprocess
session including a refused path-traversal, the adapter, host approval, and
the eval table.

## The SDK version

`sdk_file_server.py` is the read-only server written with the official SDK
(FastMCP in `mcp` 1.x, renamed `MCPServer` in 2.x; the file handles both).
Our hand-written client talks to it unchanged, and the SDK's client talks to
`file_server.py`.
