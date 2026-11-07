"""Offline mode: a stub with the same shape as the openai client, so every
step runs without the gateway (pass --offline).

It is not a language model. It reads the task, picks tool calls by simple
rules, and, like a careless model, OBEYS any line in a tool result of the
form 'call <tool> with {json}'. That makes the injection case behave the
same way on every run, so the guard's effect is easy to see. Its final
answer just repeats what the tools returned.
"""
import json
import re
from types import SimpleNamespace

INJECTED_CALL = re.compile(r"call (\w+) with (\{[^}]*\})")


class _ToolCall:
    def __init__(self, call_id, name, arguments):
        self.id = call_id
        self.type = "function"
        self.function = SimpleNamespace(name=name, arguments=json.dumps(arguments))

    def model_dump(self):
        return {"id": self.id, "type": "function",
                "function": {"name": self.function.name, "arguments": self.function.arguments}}


def plan_for_git(task):
    """Lab 12a: the git server's tasks. Phrasings the stub understands:
      show me the last N commits             -> git_log {max_count: N}
      show the history of <path>             -> git_log {path}
      show commit <rev>                      -> git_show {rev}
      compare <a> with <b>                   -> git_diff {rev_from, rev_to}
      commit <path> with message '<msg>'     -> git_commit {message, paths: [path]}
    """
    m = re.search(r"commit (\S+) with message '([^']*)'", task, re.IGNORECASE)
    if m:
        return [("git_commit", {"message": m.group(2), "paths": [m.group(1)]})]
    m = re.search(r"last (\d+) commits", task, re.IGNORECASE)
    if m:
        return [("git_log", {"max_count": int(m.group(1))})]
    m = re.search(r"history of (\S+?)[.]?(?:\s|$)", task, re.IGNORECASE)
    if m:
        return [("git_log", {"path": m.group(1)})]
    m = re.search(r"show commit (\S+?)[.]?(?:\s|$)", task, re.IGNORECASE)
    if m:
        return [("git_show", {"rev": m.group(1)})]
    m = re.search(r"compare (\S+) with (\S+?)[.]?(?:\s|$)", task, re.IGNORECASE)
    if m:
        return [("git_diff", {"rev_from": m.group(1), "rev_to": m.group(2)})]
    return []


def plan_for_all(task):
    """Lab 12b: "<step>. Then <step>. Then run this Python: <code>" -> the
    calls of every step, in order. "Run this Python:" takes the rest of the
    task as the code, so put it last."""
    calls = []
    # code in backticks may come anywhere: "Run this Python: `print(1)`. Then read notes.txt."
    for part in re.split(r"\bthen\b(?=[^`]*(?:`[^`]*`[^`]*)*$)", task, flags=re.IGNORECASE):
        part = part.strip(" .,")
        m = re.search(r"run this python:\s*`([^`]+)`", part, re.IGNORECASE)
        if m:
            calls.append(("run_python", {"code": m.group(1)}))
            continue
        m = re.search(r"run this python:\s*(.+)$", part, re.IGNORECASE | re.DOTALL)
        if m:  # unquoted code: the rest of the task is the code
            rest = task[task.lower().index(part.lower()[:20]):] if part else part
            mm = re.search(r"run this python:\s*(.+)$", rest, re.IGNORECASE | re.DOTALL)
            calls.append(("run_python", {"code": mm.group(1).strip()}))
            break
        if part:
            calls += plan_for(part)
    return calls


def resolve_name(name, offered):
    """Lab 12b: a host may prefix tool names with their server ("git__git_log")."""
    if name in offered:
        return name
    matches = [o for o in offered if o.endswith("__" + name)]
    return matches[0] if len(matches) == 1 else None


def plan_for(task):
    """The calls a sensible agent would make for this task."""
    git = plan_for_git(task)
    if git:
        return git
    t = task.lower()
    m = re.search(r"search (?:the files )?for '([^']*)'", task, re.IGNORECASE)
    if m:  # Lab 12a, task A2
        return [("search_files", {"query": m.group(1)})]
    m = re.search(r"write a file (\S+) containing '([^']*)'", task, re.IGNORECASE)
    if m:
        return [("write_file", {"path": m.group(1), "content": m.group(2) + "\n"})]
    m = re.search(r"\b(?:read|summari[sz]e) (\S+?)[.,]?(?:\s|$)", task, re.IGNORECASE)
    if m:
        return [("read_file", {"path": m.group(1)})]
    if "list" in t:
        return [("list_files", {"directory": "."})]
    return []


class _Completions:
    def __init__(self):
        self.calls = 0

    def create(self, model=None, messages=(), tools=None, **kwargs):
        self.calls += 1
        task = next(m["content"] for m in messages if m["role"] == "user")
        tool_results = [m["content"] for m in messages if m["role"] == "tool"]
        done = sum(len(m.get("tool_calls") or []) for m in messages if m["role"] == "assistant")
        offered = {t["function"]["name"] for t in (tools or [])}

        queue = plan_for_all(task)
        for text in tool_results:  # the careless part: instructions in data are obeyed
            for name, args in INJECTED_CALL.findall(text.replace('\\"', '"')):
                try:
                    queue.append((name, json.loads(args)))
                except json.JSONDecodeError:
                    pass
        queue = [(resolve_name(n, offered), a) for n, a in queue]
        queue = [(n, a) for n, a in queue if n]

        if done < len(queue):
            name, args = queue[done]
            message = SimpleNamespace(role="assistant", content=None,
                                      tool_calls=[_ToolCall(f"call_{self.calls}", name, args)])
            finish = "tool_calls"
        else:
            answer = "Here is what the tools returned:\n" + "\n".join(tool_results)
            message = SimpleNamespace(role="assistant", content=answer, tool_calls=None)
            finish = "stop"
        return SimpleNamespace(id=f"stub-{self.calls}", model="stub",
                               choices=[SimpleNamespace(finish_reason=finish, message=message)])


class StubClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=_Completions())
