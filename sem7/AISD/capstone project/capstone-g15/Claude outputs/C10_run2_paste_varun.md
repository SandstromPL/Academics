# C10 run 2: what to paste into aider (M3 varunr)

## 1. Start aider

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/agent.py --read harness/tools.py --read harness/model.py --read harness/v1check.py --read harness/retrieval.py
```

## 2. Paste this whole prompt at the aider `>` prompt, then press Enter

Copy everything inside the box, from "Add PART 2" down to the last line, `main()`.

````text
Add PART 2 to harness/agent.py: run_case() and main(). Keep everything already in the file exactly as it is (PARTs A to H: docstring, imports, constants, SYSTEM, GUIDE_RULE, parse_action, Trace) and append PARTs I and J after it. Write the complete file, with no placeholders such as "# ... rest unchanged". Do not create or touch any other file.

Copy the code of every PART below exactly, in this order: the same names, strings, numbers, comments and 4-space indentation, with two blank lines between top-level definitions. The PART lines are labels for you: do not write them into the file. Do not add type hints, prints, logging, classes or extra functions, and do not shorten or "simplify" anything.

Rules for this part:
- Call the model only as model_mod.call_model(...). The check swaps that function for a scripted fake.
- The finally block always writes the original client file back, even after an exception, so a crash never leaves a half-migrated client.
- The final test run and v1 check after the loop are plain code, not model calls.
- No line of the file may start with three backticks (aider would end the file there).

PART I. run_case:
def run_case(case, variant, model_name, trace, expand=False):
    ctx = CaseContext(case["case_id"], case["client"], expand=expand)
    client_path = os.path.join(ROOT, case["client"])
    original = open(client_path).read()
    allowed = IMPROVED_TOOLS if variant == "improved" else BASELINE_TOOLS
    system = SYSTEM.format(guide_rule=GUIDE_RULE if variant == "improved" else "",
                           tools=build_tools_desc(allowed))
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": first_user_message(case, original)}]
    calls = ptok = ctok = errors = parse_errors = 0
    stop_reason = "step_limit"
    t_start = time.time()
    final_text = original
    try:
        for step in range(1, STEP_LIMIT + 1):
            if time.time() - t_start > CASE_TIMEOUT:
                stop_reason = "timeout"
                break
            if step > 1:
                time.sleep(PACING)
            try:
                r = model_mod.call_model(messages, model=model_name)
            except Exception as e:  # gateway down / retries exhausted
                errors += 1
                trace.log(type="error", case_id=case["case_id"], step=step, error=str(e)[:300])
                stop_reason = "model_error"
                break
            calls += 1
            ptok += r["prompt_tokens"]
            ctok += r["completion_tokens"]
            reply = r["text"]
            messages.append({"role": "assistant", "content": reply})
            tool, args, perr = parse_action(reply)
            row = dict(type="step", case_id=case["case_id"], variant=variant, step=step, model=r["model"],
                       prompt_tokens=r["prompt_tokens"], completion_tokens=r["completion_tokens"],
                       latency_ms=r["latency_ms"], response_id=r.get("response_id"),
                       finish_reason=r.get("finish_reason"), tool=tool, args=short_args(args),
                       retrieved_ids=[])
            if perr:
                errors += 1
                parse_errors += 1
                obs = {"error": perr + '. Reply with one JSON object: {"tool": ..., "args": {...}}'}
            elif tool == "done":
                trace.log(**row, observation="done")
                stop_reason = "model_done"
                break
            else:
                parse_errors = 0
                err = validate_arguments(tool, args, allowed)
                if err:
                    errors += 1
                    obs = {"error": err}
                else:
                    before = len(ctx.retrieved_ids)
                    obs = dispatch(ctx, tool, args)
                    if tool == "search_guide":
                        row["retrieved_ids"] = ctx.retrieved_ids[before:]
                    if tool == "write_file":
                        trace.log(**{**ctx.gates[-1], "step": step})
                        if not obs.get("ok"):
                            errors += 1
                        else:
                            obs["v1_leftovers"] = v1_leftovers(client_path)
                    if tool == "run_tests":
                        obs["v1_leftovers"] = v1_leftovers(client_path)
            obs_text = json.dumps(obs)[:MAX_OBS]
            row["observation"] = obs_text[:400]
            trace.log(**row)
            if (not perr and tool == "run_tests" and isinstance(obs, dict)
                    and obs.get("exit_code") == 0 and not obs.get("v1_leftovers")):
                stop_reason = "green"
                break
            if parse_errors >= MAX_PARSE_ERRORS:
                stop_reason = "parse_errors"
                break
            messages.append({"role": "user", "content": f"Result of {tool or 'your reply'}: {obs_text}"})
        # ---- final check: plain code, no model ----
        final_text = open(client_path).read()
        tests = run_tests(ctx)
        left = v1_leftovers(client_path)
    finally:
        with open(client_path, "w") as f:
            f.write(original)
    needed = case["needed"]
    res = {
        "case_id": case["case_id"],
        "client": case["client"],
        "kind": case["kind"],
        "tests_green": tests["exit_code"] == 0,
        "v1_leftovers": len(left),
        "leftover_names": sorted({h["name"] for h in left}),
        "fully_migrated": tests["exit_code"] == 0 and not left,
        "first_failure": tests["first_failure"][:300],
        "calls": calls,
        "prompt_tokens": ptok,
        "completion_tokens": ctok,
        "tokens": ptok + ctok,
        "errors": errors,
        "stop_reason": stop_reason,
        "seconds": round(time.time() - t_start, 1),
        "needed_sections": needed,
        "retrieved_ids": sorted(set(ctx.retrieved_ids)),
        "hit_rate": round(hit_rate(needed, ctx.retrieved_ids), 3) if variant == "improved" else None,
        "gate_denied_paths": [g["path"] for g in ctx.gates if g["decision"] == "deny"],
    }
    trace.log(type="case_end", **res, final_text=final_text)
    return res

PART J. main and the __main__ guard:
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["baseline", "improved"], required=True)
    ap.add_argument("--model", default="main")
    ap.add_argument("--cases", default=os.path.join(ROOT, "eval", "cases"))
    ap.add_argument("--only", default="", help="comma-separated case ids")
    ap.add_argument("--expand", action="store_true", help="synonym expansion in search_guide (stretch)")
    ap.add_argument("--tag", default="", help="suffix for the run id, e.g. backup")
    a = ap.parse_args(argv)

    only = [x.strip() for x in a.only.split(",") if x.strip()]
    cases = load_cases(a.cases, only)
    if not cases:
        sys.exit("no cases found")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"p04-{a.variant}-{stamp}" + (f"-{a.tag}" if a.tag else "")
    trace = Trace(os.path.join(ROOT, "traces", f"{run_id}.jsonl"), run_id)
    started = utc_now()
    trace.log(type="run_start", variant=a.variant, model=a.model, member=git_user(),
              cases=[c["case_id"] for c in cases], step_limit=STEP_LIMIT, expand=a.expand)
    print(f"run_id {run_id}", flush=True)

    results = []
    for c in cases:
        r = run_case(c, a.variant, a.model, trace, expand=a.expand)
        results.append(r)
        print(f"  {r['case_id']}: green={r['tests_green']} leftovers={r['v1_leftovers']} "
              f"calls={r['calls']} tokens={r['tokens']} stop={r['stop_reason']}", flush=True)

    n = len(results)
    hits = [r["hit_rate"] for r in results if r["hit_rate"] is not None]
    needed_total = sum(len(r["needed_sections"]) for r in results)
    needed_hit = sum(len(set(r["needed_sections"]) & set(r["retrieved_ids"])) for r in results)
    summary = {
        "cases": n,
        "fully_migrated": sum(r["fully_migrated"] for r in results),
        "tests_green": sum(r["tests_green"] for r in results),
        "zero_leftovers": sum(r["v1_leftovers"] == 0 for r in results),
        "calls_total": sum(r["calls"] for r in results),
        "tokens_total": sum(r["tokens"] for r in results),
        "calls_per_file": round(sum(r["calls"] for r in results) / n, 2),
        "tokens_per_file": round(sum(r["tokens"] for r in results) / n, 1),
        "retrieval_hit_rate": round(needed_hit / needed_total, 3) if hits and needed_total else None,
    }
    trace.log(type="run_end", **summary)
    out = {"run_id": run_id, "variant": a.variant, "model": a.model, "member": git_user(),
           "started_utc": started, "ended_utc": utc_now(), "trace": f"traces/{run_id}.jsonl",
           "summary": summary, "cases": results}
    os.makedirs(os.path.join(ROOT, "eval", "results"), exist_ok=True)
    with open(os.path.join(ROOT, "eval", "results", f"{run_id}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"fully migrated {summary['fully_migrated']}/{n}  calls {summary['calls_total']}  "
          f"tokens {summary['tokens_total']}  hit_rate {summary['retrieval_hit_rate']}")
    print(f"trace   traces/{run_id}.jsonl\nresult  eval/results/{run_id}.json")
    return run_id


if __name__ == "__main__":
    main()
````

## 3. Before you type /exit

- aider must print **`Applied edit to harness/agent.py`**. Then type `/exit`.
- If it says it hit a **token limit**, or the reply stops midway, or there is no "Applied edit" line: type
  `/exit` and use the fallback in step 5.

## 4. Checks, in this order (paste each block on its own)

The file must now list `def run_case` and `def main` with no indentation, and be about 326 lines:

```bash
grep -nE '^(def|class) |^    def ' harness/agent.py && wc -l harness/agent.py
```

Check, part 2 (must print `agent loop OK`):

```bash
python3 - <<'PY'
import json, os, tempfile
import harness.model
import harness.agent as agent
def run(variant, replies):
    replies = list(replies)
    def fake(messages, model="main", **kw):
        if not replies:
            raise RuntimeError("fake gateway down")
        return {"text": replies.pop(0), "prompt_tokens": 10, "completion_tokens": 5, "latency_ms": 1,
                "model": model, "response_id": "fake-id", "finish_reason": "stop"}
    harness.model.call_model = fake
    if hasattr(agent, "call_model"):
        agent.call_model = fake
    path = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    res = agent.run_case(case, variant, "main", agent.Trace(path, "check"))
    return res, [json.loads(line) for line in open(path)]
agent.PACING = 0
case = agent.load_cases("eval/cases", ["case_01"])[0]
client = case["client"]
orig, v2 = open(client).read(), open("data/libv/v2.py").read()
hand = open("eval/hand_migrations/client_01.py").read()
res, rows = run("baseline", [
    '{"tool": "write_file", "args": {"path": "data/libv/v2.py", "text": "x = 1"}}',
    '```json\n{"tool": "write_file", "args": {"path": "%s"}}\n```\n\n```python\n%s```' % (client, hand),
    '{"tool": "run_tests", "args": {}}'])
assert res["fully_migrated"] and res["stop_reason"] == "green" and res["calls"] == 3, res
assert res["gate_denied_paths"] == ["data/libv/v2.py"] and res["hit_rate"] is None, res
types = [r["type"] for r in rows]
assert types.count("step") == 3 and types.count("gate") == 2 and types[-1] == "case_end", types
assert all(r["response_id"] == "fake-id" for r in rows if r["type"] == "step")
assert rows[-1]["final_text"].strip() == hand.strip(), "case_end must keep the agent's final file"
assert open(client).read() == orig and open("data/libv/v2.py").read() == v2, "client not restored, or v2.py changed"
res, rows = run("improved", ['{"tool": "search_guide", "args": {"query": "get_balance"}}', "not json", '{"tool": "done", "args": {}}'])
assert res["stop_reason"] == "model_done" and res["hit_rate"] == 1.0 and res["errors"] == 1 and not res["fully_migrated"], res
res, rows = run("baseline", [])
assert res["stop_reason"] == "model_error" and res["calls"] == 0 and rows[0]["type"] == "error", res
assert open(client).read() == orig
print("agent loop OK")
PY
```

Check, part 1 again (must print `agent part 1 OK`):

```bash
python3 - <<'PY'
from harness.agent import (parse_action, v2_signatures, load_cases, SYSTEM, GUIDE_RULE, first_user_message,
                           short_args, STEP_LIMIT, CASE_TIMEOUT, PACING, MAX_PARSE_ERRORS, MAX_OBS)
src = open("harness/agent.py").read()
assert not [l for l in src.splitlines() if l.startswith("```")], "a line starts with ``` (aider cuts the file there)"
r1 = '```json\n{"tool": "write_file", "args": {"path": "x"}}\n```\n\n```python\nimport a\n```'
assert parse_action(r1) == ("write_file", {"path": "x", "text": "import a\n"}, None), parse_action(r1)
assert parse_action('<think>{"tool": "bad"}</think>{"tool": "run_tests", "args": {}}') == ("run_tests", {}, None)
assert parse_action('Sure: {"tool": "read_file", "args": {"path": "p"}} ok') == ("read_file", {"path": "p"}, None)
assert parse_action("no json here")[2] and parse_action('{"tool": "write_file", "args": {"path": "x", "text": "t"}}')[1]["text"] == "t"
sig = v2_signatures()
assert "def fetch_balance(account_id: str) -> float: ..." in sig and "class Money(" in sig and "    amount: float" in sig, sig
assert "get_balance" not in sig and '"""' not in sig, sig
cases = load_cases("eval/cases")
assert len(cases) == 6 and cases[0]["case_id"] == "case_01" and cases[0]["client"] == "data/clients/client_01.py" and cases[0]["needed"] == ["G01"], cases[0]
s = SYSTEM.format(guide_rule=GUIDE_RULE, tools="- t")
assert '{"tool": "<name>", "args": {...}}' in s and "```python ... ```" in s and s.endswith("Tools:\n- t"), s
assert short_args({"path": "p", "text": "abc"}) == {"path": "p", "text": "<3 chars>"}
assert first_user_message(cases[0], "x = 1\n").startswith("Client file: data/clients/client_01.py\n```python\nx = 1\n```")
assert (STEP_LIMIT, CASE_TIMEOUT, PACING, MAX_PARSE_ERRORS, MAX_OBS) == (8, 180, 0.5, 3, 1500)
print("agent part 1 OK")
PY
```

Unit tests (must print `26 passed`):

```bash
python3 -m pytest -q -p no:cacheprovider data/libv/tests harness safety
```

Only `?? harness/agent.py` may be listed:

```bash
git status --short
```

Commit and push:

```bash
git add harness/agent.py && git commit -m "Day 4: agent loop with step limit, trace and result writer" && git push
```

## 5. Fallback, only if a check fails twice

```bash
unzip -o ~/capstone-g15-fallback-C4-C13.zip harness/agent.py
```

Then run the checks in step 4 again.
