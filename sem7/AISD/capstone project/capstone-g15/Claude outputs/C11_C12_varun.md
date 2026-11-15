# C11 and C12 (M3 varunr): smoke run, then CAPSTONE.md

C10 is pushed (`e302805`). Two steps left, both without aider.

## Context check (already done, nothing to run)

- **C11 is the harness calling `main` itself**, not aider. Measured with the real harness code on all 6 cases:
  a normal case asks with **640 to 1,309 prompt tokens** per call. The limit is 16,384 tokens, and each call
  reserves up to 2,000 for the reply (`max_tokens` in `harness/model.py`), so a prompt may use 14,384. That
  leaves more than 10 times the room.
- Only in an extreme case (every reply 2,000 tokens long) would calls 7 and 8 of one file pass the limit. Then
  the gateway refuses that call, the harness logs an `error` row, stops that file with `stop=model_error`, and
  goes on. It doesn't crash. The check below prints the real token count of every step, so you'll see it.
- **C12 is a plain Python script** that edits CAPSTONE.md. It makes no model call, so it has no context limit.
- For M4's C13 next: its aider run sends about 7.4k tokens (tested with real aider), under the limit. Tell
  Rahul to type `/clear` right after aider starts anyway.

## C11 · smoke run on case_01 (uses your gateway key)

Check that your last commit is C10:

```bash
git log --oneline -3
```

The top line must be `e302805 Day 4: agent loop with step limit, trace and result writer`.

Run the smoke run. It takes 2 to 8 model calls, at most 3 minutes:

```bash
python3 -m harness.agent --variant baseline --only case_01
```

It prints `run_id p04-baseline-...`, one line for case_01 (`green=... calls=... stop=...`), then the trace and
result paths.

The client must be restored, so this prints nothing:

```bash
git status --short data/clients
```

Then the check (paste it on its own). It prints every step with its real token counts, and must end with
`smoke OK`:

```bash
python3 - <<'PY'
import glob, json, os
f = max(glob.glob("eval/results/p04-*.json"), key=os.path.getmtime)
d = json.load(open(f))
for k in ("run_id", "variant", "model", "member", "started_utc", "ended_utc", "trace", "summary", "cases"):
    assert k in d, k
for k in ("cases", "fully_migrated", "tests_green", "zero_leftovers", "calls_total", "tokens_total",
          "calls_per_file", "tokens_per_file", "retrieval_hit_rate"):
    assert k in d["summary"], k
rows = [json.loads(line) for line in open(d["trace"])]
types = {r["type"] for r in rows}
for r in rows:
    if r["type"] == "error":
        print("ERROR ROW:", r.get("step"), r.get("error"))
assert {"run_start", "step", "case_end", "run_end"} <= types, types
steps = [r for r in rows if r["type"] == "step"]
assert all(r.get("response_id") for r in steps), "a step row has no response_id"
for r in steps:
    print(f"  step {r['step']}: tool={r['tool']} prompt_tokens={r['prompt_tokens']} "
          f"completion_tokens={r['completion_tokens']} finish={r['finish_reason']}")
peak = max(r["prompt_tokens"] for r in steps)
assert peak + 2000 <= 16384, f"prompt {peak} + max_tokens 2000 is over the 16,384 context"
cut = [r["step"] for r in steps if r["finish_reason"] == "length"]
if cut:
    print("WARNING: reply cut at max_tokens in steps", cut)
c = d["cases"][0]
print(d["run_id"], d["member"], "fully migrated", d["summary"]["fully_migrated"], "/", d["summary"]["cases"],
      "calls", d["summary"]["calls_total"], "stop", c["stop_reason"], "peak prompt", peak, "of 14384")
print("smoke OK")
PY
```

What the output means:
- **`fully migrated 1 / 1`, `stop green`:** the expected result.
- **`fully migrated 0 / 1`:** still commit it. The smoke run proves the loop, the trace and the result file work.
  Don't rerun just to get a better number.
- **`ERROR ROW` or an `AssertionError` about `step`:** the model call failed (gateway, key or context). Read the
  error text. For 401/404 or missing variables, see playbook section 9. Then run the smoke run again before you
  commit.
- **`WARNING: reply cut at max_tokens`:** Qwen wrote more than 2,000 tokens in one reply. Commit anyway, and tell
  the group; we can raise `max_tokens` later.

Commit and push. The run id is filled in for you, from the newest result file:

```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && git add traces/ eval/results/ && git commit -m "Day 4: baseline smoke run on case_01 (run $RUN)" && git push
```

## C12 · CAPSTONE.md: Architecture and Harness bounds

This script replaces the two placeholder lines in CAPSTONE.md (`Harness loop, tools, models used and why.` and
`Step limit, timeout, retries, pacing.`). It now also writes the context bound into the Harness bounds table.
Paste it on its own:

```bash
python3 - <<'PY'
p = "CAPSTONE.md"
s = open(p).read()
blocks = {
"Harness loop, tools, models used and why.\n": """One loop per client file (`harness/agent.py`, run as `python3 -m harness.agent --variant baseline|improved`).
Each step is one model call to the gateway model `main` (`harness/model.py`, the `openai` SDK as in the labs,
`OPENAI_BASE_URL` + the member's own key, temperature 0). The model answers with one JSON action
`{"tool": ..., "args": {...}}`; for `write_file` the new file may follow in a ```python block.
`harness/tools.py` holds the registry (pattern from lab 6a: `TOOL_REGISTRY`, `validate_arguments`,
`build_tools_desc`) for `search_guide`, `read_file`, `write_file` and `run_tests`.
`search_guide` is keyword retrieval over `data/guide.json` (`harness/retrieval.py`, from lab 8b:
`tokens`, `STOPWORDS`, `retrieve`, `hit_rate`, plus IDF weighting, k capped at 3, section text capped at 600 chars).
Everything that is not a judgement is plain code (lab 4b pattern): the v1 check (`harness/v1check.py`),
the scope gate (`safety/scope.py`), the final test run and the per-file report.
Baseline: tools read_file, write_file, run_tests; the prompt holds the client and the v2.py signatures
(no docstrings). Improved: the same plus `search_guide`.
After each case the client file is restored to its v1 original; the agent's final file is kept in the
trace's `case_end` row. Trace: `traces/<run_id>.jsonl` (run_start, step, gate, case_end, run_end rows;
step rows log the tool, arguments, token counts, the gateway `response_id` and the retrieved section IDs).
Result: `eval/results/<run_id>.json`.
""",
"Step limit, timeout, retries, pacing.\n": """| Bound | Value | Where |
|---|---|---|
| Step limit | 8 model calls per client file | `STEP_LIMIT`, harness/agent.py |
| Case timeout | 180 s wall clock per file | `CASE_TIMEOUT` |
| Model call timeout / retries | 60 s per call, openai SDK `max_retries=2` with backoff (429, 5xx, network) | `TIMEOUT_S`, `MAX_RETRIES`, harness/model.py |
| Test timeout | 30 s pytest subprocess | `TEST_TIMEOUT`, harness/tools.py |
| Pacing | 0.5 s between calls | `PACING` |
| Bad replies | stop after 3 unparseable replies in a row | `MAX_PARSE_ERRORS` |
| Observation size | tool output cut to 1500 chars | `MAX_OBS` |
| Context and reply size | the gateway model `main` takes 16,384 tokens; each call asks for at most 2,000 reply tokens (`max_tokens`), so a prompt may use 14,384. In a scripted run of all 6 cases the largest prompt was about 1,300 tokens. A request that is too long fails as a model error and stops that file | `call_model`, harness/model.py |
| Early stop | run_tests exit 0 and zero v1 leftovers, or the model replies `done` | agent.py |
""",
}
for old, new in blocks.items():
    if old not in s:
        raise SystemExit("placeholder not found, edit CAPSTONE.md by hand: " + old.strip())
    s = s.replace(old, new, 1)
open(p, "w").write(s)
print("CAPSTONE.md updated")
PY
```

It must print `CAPSTONE.md updated`. Then check that only CAPSTONE.md changed:

```bash
git --no-pager diff --stat
```

```bash
git add CAPSTONE.md && git commit -m "Day 4: CAPSTONE.md architecture and harness bounds" && git push
```

## End of turn

```bash
git log -1 --format=%h
```

Post "C12 pushed, <hash>" in the group. **M4 (Rahul) goes next with C13**; he should type `/clear` first in aider.
