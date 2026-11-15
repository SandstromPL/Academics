"""P04 agent loop: migrate each client file from libv v1 to v2.

  python3 -m harness.agent --variant baseline            # all cases in eval/cases/
  python3 -m harness.agent --variant baseline --only case_01
  python3 -m harness.agent --variant improved --model main

baseline: tools read_file, write_file, run_tests; the prompt has v2.py signatures + the client.
improved: same + search_guide over data/guide.json.

Writes traces/<run_id>.jsonl and eval/results/<run_id>.json and prints the run ID.
Client files are restored to their v1 originals after every case (the agent's
final file is kept in the trace's case_end row).
"""

import argparse
import ast
import glob
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

from harness import model as model_mod
from harness.retrieval import hit_rate
from harness.tools import (BASELINE_TOOLS, IMPROVED_TOOLS, CaseContext, build_tools_desc, dispatch,
                           run_tests, v1_leftovers, validate_arguments)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ---- harness bounds (CAPSTONE.md "Harness bounds") ----
STEP_LIMIT = 8          # model calls per client file
CASE_TIMEOUT = 180      # seconds per client file
PACING = 0.5            # seconds between model calls
MAX_PARSE_ERRORS = 3    # consecutive unparseable replies before giving up on a file
MAX_OBS = 1500          # chars of tool output fed back to the model


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_user():
    try:
        return subprocess.run(["git", "config", "user.name"], cwd=ROOT, capture_output=True,
                              text=True, timeout=5).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def v2_signatures():
    """Public def/class lines of v2.py without bodies or docstrings (what the baseline sees)."""
    tree = ast.parse(open(os.path.join(ROOT, "data", "libv", "v2.py")).read())
    lines = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            node.body = [ast.Expr(ast.Constant(...))]
            lines.append(ast.unparse(node).replace("\n    ...", " ..."))
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            bases = ", ".join(ast.unparse(b) for b in node.bases)
            deco = "".join(f"@{ast.unparse(d)}\n" for d in node.decorator_list)
            fields = [f"    {ast.unparse(s)}" for s in node.body if isinstance(s, ast.AnnAssign)]
            lines.append(f"{deco}class {node.name}({bases}):" + ("\n" + "\n".join(fields) if fields else " ..."))
    return "\n".join(lines)


def load_cases(cases_dir, only=None):
    cases = []
    for p in sorted(glob.glob(os.path.join(cases_dir, "*.json"))):
        c = json.load(open(p))
        case = {
            "case_id": c.get("case_id") or c.get("id"),
            "client": c.get("client") or c.get("client_file"),
            "needed": c.get("needed_sections") or c.get("required_sections") or [],
            "kind": c.get("kind") or ",".join(c.get("tags", [])),
            "expected": c.get("expected", {}),
        }
        if not only or case["case_id"] in only:
            cases.append(case)
    return cases


SYSTEM = """You migrate ONE Python client module from the deprecated libv.v1 API to libv.v2.
Goal: the client's tests pass against libv.v2 and no libv.v1 import or v1-only name is left.
Rules:
- Import only from libv.v2. Do not define wrappers or aliases named like old v1 functions or exceptions.
- Keep the client's own function names, behaviour, comments, docstrings and string literals.
- You may write ONLY the client file. Library and test files are read-only.
{guide_rule}
Reply with exactly ONE JSON object per turn and nothing else, of the form
{{"tool": "<name>", "args": {{...}}}}
For write_file you may leave "text" out of args and instead put the complete new file
in a ```python ... ``` block right after the JSON.
When the tests are green and no v1 names remain, reply {{"tool": "done", "args": {{}}}}.
Tools:
{tools}"""

GUIDE_RULE = ("- First call search_guide with the v1 names used in the client; follow the guide's AFTER code. "
              "Search again if a v1 name is not covered.")


def first_user_message(case, client_text):
    return (f"Client file: {case['client']}\n```python\n{client_text}```\n\n"
            f"libv.v2 public signatures:\n```python\n{v2_signatures()}\n```\n"
            f"Migrate {case['client']} now.")


THINK_RE = re.compile(r"<think>.*?(</think>|$)", re.S)
FENCE_RE = re.compile(r"```([\w+-]*)[ \t]*\n(.*?)```", re.S)


def parse_action(text):
    """First JSON object in the reply -> (tool, args). write_file text may come from a code block.

    <think>...</think> reasoning is dropped first. Fences are matched as open/close pairs,
    so a ```json fence around the action is skipped and the ```python block is used.
    """
    text = THINK_RE.sub("", text or "")
    dec = json.JSONDecoder()
    obj = None
    for m in re.finditer(r"\{", text):
        try:
            cand, _ = dec.raw_decode(text[m.start():])
        except ValueError:
            continue
        if isinstance(cand, dict) and "tool" in cand:
            obj = cand
            break
    if obj is None:
        return None, None, "no JSON object with a \"tool\" key found"
    tool, args = obj.get("tool"), obj.get("args") or {}
    if tool == "write_file" and isinstance(args, dict) and "text" not in args:
        blocks = [body for lang, body in FENCE_RE.findall(text)
                  if lang.lower() != "json" and not body.lstrip().startswith("{")]
        if blocks:
            args["text"] = max(blocks, key=len)
    return tool, args, None


def short_args(args):
    if not isinstance(args, dict):
        return args
    return {k: (f"<{len(v)} chars>" if k == "text" and isinstance(v, str) else v) for k, v in args.items()}


class Trace:
    def __init__(self, path, run_id):
        self.path, self.run_id = path, run_id
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.f = open(path, "a")

    def log(self, **row):
        row = {"run_id": self.run_id, "ts": utc_now(), **row}
        self.f.write(json.dumps(row) + "\n")
        self.f.flush()

def run_case(case, variant, model_name, trace, expand=False, budget=None):
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
            if budget is not None and (budget["calls_left"] <= 0 or time.time() > budget["deadline"]):
                stop_reason = "run_budget"
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
            if budget is not None:
                budget["calls_left"] -= 1
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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["baseline", "improved"], required=True)
    ap.add_argument("--model", default="main")
    ap.add_argument("--cases", default=os.path.join(ROOT, "eval", "cases"))
    ap.add_argument("--only", default="", help="comma-separated case ids")
    ap.add_argument("--expand", action="store_true", help="synonym expansion in search_guide (stretch)")
    ap.add_argument("--tag", default="", help="suffix for the run id, e.g. backup")
    ap.add_argument("--max-calls", type=int, default=0, help="run-level cap on model calls (live run), 0 = none")
    ap.add_argument("--max-seconds", type=float, default=0, help="run-level time cap in seconds (live run), 0 = none")
    a = ap.parse_args(argv)

    only = [x.strip() for x in a.only.split(",") if x.strip()]
    cases = load_cases(a.cases, only)
    if not cases:
        sys.exit("no cases found")
    budget = None
    if a.max_calls > 0 or a.max_seconds > 0:
        budget = {"calls_left": a.max_calls if a.max_calls > 0 else 10 ** 9,
                  "deadline": time.time() + (a.max_seconds if a.max_seconds > 0 else 10 ** 9)}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"p04-{a.variant}-{stamp}" + (f"-{a.tag}" if a.tag else "")
    trace = Trace(os.path.join(ROOT, "traces", f"{run_id}.jsonl"), run_id)
    started = utc_now()
    trace.log(type="run_start", variant=a.variant, model=a.model, member=git_user(),
              cases=[c["case_id"] for c in cases], step_limit=STEP_LIMIT, expand=a.expand,
              max_calls=a.max_calls, max_seconds=a.max_seconds)
    print(f"run_id {run_id}", flush=True)

    results = []
    for c in cases:
        r = run_case(c, a.variant, a.model, trace, expand=a.expand, budget=budget)
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
