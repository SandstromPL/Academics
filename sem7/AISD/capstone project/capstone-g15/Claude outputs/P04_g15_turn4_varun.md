# P04 / g15: Turn 4 for M3 varunr (C8 to C12), playbook v3.2

This is Turn 4 of `P04_g15_playbook_v3.md` (v3.2), on its own so it is easy to share. Sections 6 (relay loop)
and 9 (troubleshooting) of the playbook still apply. Fallback zip: `capstone-g15-fallback-C4-C13.zip` (v3.2).

### Turn 4: M3 varunr (C8 to C12)

Varun's turn has 5 aider runs (C8, C9 twice, C10 twice), one smoke run on the gateway (C11) and one script
(C12). Like Rahul's C6 and C7, every prompt gives the code part by part: Qwen copies code reliably but
invents bugs when it has to fill gaps. Each run has its own check, and the checks don't trust Qwen's work.

**Before you start:** copy the newest `capstone-g15-fallback-C4-C13.zip` (v3.2, 9 Nov) to your workspace
home folder. It has every file of this turn, for any run that fails its check twice.

Start of turn:

```bash
git pull --rebase --autostash
git log --oneline -5
git config user.name
```

The top line must be M4's `Day 3: write_file scope guard with gate records`, and the last line must be
`varunr`. If it prints another name, set yours with `git config user.name varunr` before any commit.

**Check that M4's files give your tools what they need.** Paste this block on its own. It makes no
gateway calls.

```bash
python3 - <<'PY'
from harness.v1check import v1_leftovers
from safety.scope import check_write, gate_record
c, h = "data/clients/client_01.py", "eval/hand_migrations/client_01.py"
left = v1_leftovers(c)
assert left and all(set(x) == {"line", "name"} for x in left), left
assert v1_leftovers(h) == [], v1_leftovers(h)
ok, reason = check_write(c, c)
assert ok is True and isinstance(reason, str), (ok, reason)
ok, reason = check_write("data/libv/v2.py", c)
assert ok is False and reason.startswith("denied"), (ok, reason)
rec = gate_record("data/libv/v2.py", c, "case_01")
assert rec["type"] == "gate" and rec["path"] == "data/libv/v2.py" and rec["decision"] == "deny", rec
assert rec["case_id"] == "case_01" and gate_record(c, c, "case_01")["decision"] == "allow", rec
print("M4 interface OK")
PY
```

```bash
python3 -m pytest -q -p no:cacheprovider data/libv/tests harness safety
```

The first block prints `M4 interface OK` and the second `26 passed`. If either fails, stop and post the
error in the group. Your files import M4's, so M4 fixes it first, with an extra commit.

#### C8 · Day 3 · keyword retrieval

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/retrieval.py --read data/guide.json
```

Prompt:

````text
Write harness/retrieval.py from scratch (replace anything already in it): keyword retrieval over data/guide.json, the same shape as lab 8b retrieve(). Python 3 standard library only (json, math, os, re). No model calls. Do not create or touch any other file.

data/guide.json (read-only) is a list of 12 sections. Each section is a dict with the keys id, title, text, before, after.

Copy the code of every PART below exactly, in this order: the same names, strings, numbers, comments and 4-space indentation, with two blank lines between top-level definitions. The PART lines are labels for you: do not write them into the file. Do not add type hints, prints, logging, classes or extra functions, and do not shorten or "simplify" anything.

PART A. Module docstring and imports:
"""Keyword retrieval over data/guide.json (same shape as lab-08b retrieve()).

Section text is capped at 600 chars and k at 3 so retrieval cannot fill the context.
"""
import json
import math
import os
import re

PART B. Constants. Copy every value; never shorten STOPWORDS or SYNONYMS, and keep the comment above SYNONYMS:
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUIDE_PATH = os.path.join(ROOT, "data", "guide.json")
MAX_K = 3
MAX_TEXT = 600

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "be",
    "it", "its", "with", "by", "as", "at", "from", "this", "that", "now", "not", "no",
    "use", "how", "do", "does", "what", "v1", "v2", "libv", "import", "call", "calls",
    "function", "migrate", "migration", "python", "code", "new", "old", "instead",
}

# Stretch (lab 8b): synonym expansion. Off by default; harness passes expand=True to use it.
SYNONYMS = {
    "pay": ["charge", "transfer"],
    "payment": ["charge", "pay"],
    "balance": ["fetch_balance", "get_balance"],
    "receipt": ["make_receipt", "charge_and_receipt"],
    "error": ["exception", "payerror"],
    "exception": ["error"],
    "rupees": ["paise", "amount"],
    "currency": ["money"],
}

PART C. The tokenizer. tokens() keeps duplicates, and keeps the whole lower-cased word as well as its parts: tokens("get_balance") == ["get_balance", "get", "balance"] and tokens("InsufficientFunds") == ["insufficientfunds", "insufficient", "funds"]:
def _split_ident(word):
    parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", word).replace("_", " ").split()
    return [p.lower() for p in parts]


def tokens(text):
    out = []
    for word in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text or ""):
        low = word.lower()
        cands = [low] + (_split_ident(word) if ("_" in word or not word.islower()) else [])
        for c in cands:
            if c and c not in STOPWORDS and len(c) > 1:
                out.append(c)
    return out

PART D. Synonym expansion (a stretch feature, used only when expand=True) and loading the guide:
def expand_query(query_tokens):
    out = list(query_tokens)
    for t in query_tokens:
        out.extend(SYNONYMS.get(t, []))
    return out


def load_guide(path=GUIDE_PATH):
    return json.load(open(path))

PART E. The tokens of one section, and the IDF weights. The formula is exactly math.log((n + 1) / (c + 0.5)):
def _section_tokens(s):
    return set(tokens(s["title"])) | set(tokens(s["text"])) | set(tokens(s["before"])) | set(tokens(s["after"]))


def _idf(guide):
    n = len(guide)
    df = {}
    for s in guide:
        for t in _section_tokens(s):
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}

PART F. retrieve(). A query token that is in the title counts double. k is clamped to 1..3. IMPORTANT: Python cannot compare two dicts, so never sort tuples that end in a section dict without a key: two equal scores would make Python compare the dicts and crash with TypeError. Keep the (-score, i, s) tuples and sort with key=lambda x: (x[0], x[1]) exactly as shown: higher score first, guide order breaks ties:
def retrieve(query, guide, k=3, expand=False):
    """Return up to k sections ranked by IDF-weighted keyword overlap (title counts double)."""
    k = max(1, min(int(k), MAX_K))
    q = tokens(query)
    if expand:
        q = expand_query(q)
    q = set(q)
    idf = _idf(guide)
    scored = []
    for i, s in enumerate(guide):
        title = set(tokens(s["title"]))
        body = _section_tokens(s)
        score = sum(idf.get(t, 0) * (2 if t in title else 1) for t in q & body)
        if score > 0:
            scored.append((-score, i, s))
    scored.sort(key=lambda x: (x[0], x[1]))
    return [s for _, _, s in scored[:k]]

PART G. hit_rate():
def hit_rate(needed_ids, retrieved_ids):
    needed = set(needed_ids)
    if not needed:
        return 1.0
    return len(needed & set(retrieved_ids)) / len(needed)
````

Check (paste this block on its own):

```bash
python3 - <<'PY'
import math
from harness.retrieval import tokens, retrieve, load_guide, hit_rate, expand_query, _idf, MAX_K, MAX_TEXT
assert tokens("get_balance") == ["get_balance", "get", "balance"], tokens("get_balance")
assert tokens("InsufficientFunds") == ["insufficientfunds", "insufficient", "funds"], tokens("InsufficientFunds")
assert tokens("the import of libv.v1") == [] and tokens("a b x") == [] and (MAX_K, MAX_TEXT) == (3, 600)
assert tokens("transfer transfer") == ["transfer", "transfer"], tokens("transfer transfer")
g = load_guide()
first = {"get_balance": "G01", "transfer": "G02", "get_transaction": "G03", "charge_and_receipt": "G04",
         "InsufficientFunds": "G05", "AccountNotFound": "G06", "PaymentError": "G12"}
for q, gid in first.items():
    ids = [s["id"] for s in retrieve(q, g)]
    assert ids and ids[0] == gid, (q, ids)
assert len(retrieve("get_balance transfer charge format_amount", g, k=10)) <= 3
assert len(retrieve("get_balance", g, k=0)) == 1 and retrieve("zzzz", g) == []
mk = lambda i, title, text: {"id": i, "title": title, "text": text, "before": "", "after": ""}
tg = [mk("B", "other", "refund"), mk("A", "refund rules", "refund"), mk("C", "other", "refund"), mk("D", "zebra", "zebra")]
assert [s["id"] for s in retrieve("refund", tg)] == ["A", "B", "C"], "a title match counts double; ties keep guide order"
tie = [mk("X", "same", "same words"), mk("Y", "same", "same words"), mk("Z", "other", "other")]
assert [s["id"] for s in retrieve("same words", tie)] == ["X", "Y"], "equal scores must keep guide order"
idf = _idf(tg)
assert abs(idf["zebra"] - math.log(5 / 1.5)) < 1e-9 and abs(idf["refund"] - math.log(5 / 3.5)) < 1e-9, idf
assert expand_query(["pay", "zzzz"]) == ["pay", "zzzz", "charge", "transfer"], expand_query(["pay", "zzzz"])
pg = [mk("P", "charge", "charge money")]
assert retrieve("pay", pg) == [] and [s["id"] for s in retrieve("pay", pg, expand=True)] == ["P"]
assert hit_rate(["G01", "G02"], ["G01", "G05"]) == 0.5 and hit_rate([], []) == 1.0 and hit_rate(["G01"], []) == 0.0
print("retrieval OK")
PY
```

```bash
git status --short
```

The check must print `retrieval OK`, and `git status` must list only `?? harness/retrieval.py`. The `tie`
case catches a sort that compares section dicts (a `TypeError` like Rahul's) or puts equal scores in the
wrong order. If the check fails, quote its `AssertionError` line to aider once (section 6). If it fails
again, exit aider and run `unzip -o ~/capstone-g15-fallback-C4-C13.zip harness/retrieval.py`, then run the
check again.

Commit and push:

```bash
git add harness/retrieval.py && git commit -m "Day 3: keyword retrieval over guide.json (k<=3, IDF, hit_rate)" && git push
```

#### C9 · Day 3 · gateway client and tool registry

**Run 1 of 2: the gateway client**

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/model.py
```

Prompt:

````text
Write harness/model.py from scratch (replace anything already in it): the one function every model call of the harness goes through. It uses the openai Python SDK the same way as the labs. Standard library (os, time) plus openai only. Do not create or touch any other file.

Copy the code of every PART below exactly, in this order: the same names, strings, numbers, comments and 4-space indentation, with two blank lines between top-level definitions. The PART lines are labels for you: do not write them into the file. Do not add type hints, prints, logging, classes or extra functions, and do not shorten or "simplify" anything.

PART A. Module docstring, imports and constants:
"""One function for every model call: call_model(messages, model) -> dict.

Same client as the labs (lab-12 agent.py): openai.OpenAI with OPENAI_BASE_URL and
OPENAI_API_KEY from your workspace (your OWN key), gateway model "main" (or "aux").
The SDK retries 429, 5xx and connection errors MAX_RETRIES times with backoff.
Every result carries the gateway's response id, so trace rows can be joined to
gateway rows.
"""
import os
import time

TIMEOUT_S = 60      # per model call
MAX_RETRIES = 2     # SDK retries on 429 / 5xx / network errors
_client = None

PART B. _get_client(). It builds the client the first time it is called, never at import time, and caches it in the global _client. Import OpenAI inside the function. Pass the base URL exactly as it is in the environment: do NOT add "/v1" or anything else to it. Never print or log the key:
def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        base = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
        key = os.environ.get("OPENAI_API_KEY")
        if not base or not key:
            raise RuntimeError("set OPENAI_BASE_URL and OPENAI_API_KEY (your own gateway key)")
        _client = OpenAI(base_url=base, api_key=key, max_retries=MAX_RETRIES, timeout=TIMEOUT_S)
    return _client

PART C. call_model(). No try/except here (the agent loop handles errors), no retry loop of your own (the SDK retries), no streaming, no tools parameter, no print:
def call_model(messages, model="main", max_tokens=2000, temperature=0.0):
    """Returns {"text", "prompt_tokens", "completion_tokens", "latency_ms", "model",
    "response_id", "finish_reason"}."""
    t0 = time.time()
    resp = _get_client().chat.completions.create(model=model, messages=messages,
                                                 max_tokens=max_tokens, temperature=temperature)
    usage = resp.usage
    choice = resp.choices[0]
    return {
        "text": choice.message.content or "",
        "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
        "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
        "latency_ms": int((time.time() - t0) * 1000),
        "model": resp.model or model,
        "response_id": resp.id,
        "finish_reason": choice.finish_reason,
    }
````

Check, part 1 (paste this block on its own). It puts a fake `openai` module in place of the real one, so
it makes **no gateway call**. It checks the base URL, the retries, the timeout, the exact request and every
key of the result:

```bash
python3 - <<'PY'
import os, sys, types
seen = {"init": [], "create": []}
class _Completions:
    def create(self, **kw):
        seen["create"].append(kw)
        msg = types.SimpleNamespace(content=None if kw.get("max_tokens") == 1 else "ok")
        return types.SimpleNamespace(id="resp-123", model="gw-main",
                                     choices=[types.SimpleNamespace(message=msg, finish_reason="stop")],
                                     usage=types.SimpleNamespace(prompt_tokens=7, completion_tokens=2))
class OpenAI:
    def __init__(self, **kw):
        seen["init"].append(kw)
        self.chat = types.SimpleNamespace(completions=_Completions())
fake = types.ModuleType("openai")
fake.OpenAI = OpenAI
sys.modules["openai"] = fake
import harness.model as m
assert m._client is None, "the client must be built on the first call, not at import time"
assert (m.TIMEOUT_S, m.MAX_RETRIES) == (60, 2)
msgs = [{"role": "user", "content": "hi"}]
r = m.call_model(msgs)
kw = seen["init"][0]
base = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
assert kw.get("base_url") == base, "pass the base URL exactly as it is in the environment (no /v1 added)"
assert kw.get("api_key") == os.environ.get("OPENAI_API_KEY"), "api_key must come from OPENAI_API_KEY"
assert kw.get("max_retries") == 2 and kw.get("timeout") == 60, sorted(k for k in kw if k != "api_key")
assert seen["create"][0] == {"model": "main", "messages": msgs, "max_tokens": 2000, "temperature": 0.0}, seen["create"][0]
assert set(r) == {"text", "prompt_tokens", "completion_tokens", "latency_ms", "model", "response_id", "finish_reason"}, r
assert (r["text"], r["prompt_tokens"], r["completion_tokens"], r["model"], r["response_id"], r["finish_reason"]) == (
    "ok", 7, 2, "gw-main", "resp-123", "stop"), r
assert isinstance(r["latency_ms"], int), r
r2 = m.call_model(msgs, model="aux", max_tokens=1)
assert r2["text"] == "" and seen["create"][1]["model"] == "aux", "empty content must give text ''"
assert len(seen["init"]) == 1, "the client must be built once and reused"
print("model OK")
PY
```

It must print `model OK`. A `RuntimeError: set OPENAI_BASE_URL and OPENAI_API_KEY` here means your terminal
doesn't have the gateway variables: open a new workspace terminal (section 9).

Check, part 2. The first command must print
`RuntimeError: set OPENAI_BASE_URL and OPENAI_API_KEY (your own gateway key)`. The second makes **one real
gateway call** with your key, and prints some text, a response id and two token counts:

```bash
env -u OPENAI_BASE_URL -u OPENAI_API_BASE python3 -c "from harness.model import call_model; call_model([{'role': 'user', 'content': 'hi'}])" 2>&1 | tail -1
python3 -c "from harness.model import call_model; r = call_model([{'role': 'user', 'content': 'Reply with the single word ok'}], max_tokens=50); print(repr(r['text'][:60]), r['response_id'], r['prompt_tokens'], r['completion_tokens'])"
```

If the second command fails, see section 9 (gateway) before going on. Fallback for this run:
`unzip -o ~/capstone-g15-fallback-C4-C13.zip harness/model.py`.

**Run 2 of 2: the tools**

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/tools.py --read harness/retrieval.py --read harness/v1check.py --read safety/scope.py
```

Prompt:

````text
Write harness/tools.py from scratch (replace anything already in it): the agent's tool registry, the pattern from lab 6a (TOOL_REGISTRY, validate_arguments, build_tools_desc). The 3 read-only files are finished: import from them, and never copy or change their code. Do not create or touch any other file.

What the imported functions do:
- retrieve(query, guide, k=3, expand=False) returns up to 3 section dicts (keys id, title, text, before, after). MAX_TEXT is 600. load_guide() returns the guide list.
- v1_leftovers(path) returns a list of {"line": int, "name": str}; an empty list means migrated.
- check_write(path, case_client) returns (allowed: bool, reason: str).
- gate_record(path, case_client, case_id) returns a dict with the keys type, case_id, tool, path, resolved, decision ("allow" or "deny") and reason.

Copy the code of every PART below exactly, in this order: the same names, strings, numbers, comments and 4-space indentation, with two blank lines between top-level definitions. The PART lines are labels for you: do not write them into the file. Do not add type hints, prints, logging, classes or extra functions, and do not shorten or "simplify" anything.

PART A. Module docstring, imports and constants. READABLE ends the clients folder with os.sep, so a folder such as data/clients_old/ is not readable:
"""Tool registry for P04 (pattern from lab-06a: TOOL_REGISTRY, validate_arguments, build_tools_desc).

Tools: search_guide, read_file, write_file (scoped by safety/scope.py), run_tests.
v1_leftovers is plain code used by the harness and the eval, not a model tool.
"""
import os
import re
import shutil
import subprocess
import sys

from harness.retrieval import MAX_TEXT, load_guide, retrieve
from harness.v1check import v1_leftovers
from safety.scope import check_write, gate_record

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
READABLE = [os.path.join(ROOT, "data", "clients") + os.sep, os.path.join(ROOT, "data", "libv", "v2.py")]
TEST_TIMEOUT = 30

PART B. CaseContext, the per-case state. guide is a property that loads the guide once:
class CaseContext:
    """Per-case state the tools need: which client may be written, and what was logged."""

    def __init__(self, case_id, client_file, expand=False):
        self.case_id = case_id
        self.client_file = client_file
        self.expand = expand
        self.retrieved_ids = []   # every section id returned by search_guide in this case
        self.gates = []           # gate records from write_file
        self._guide = None

    @property
    def guide(self):
        if self._guide is None:
            self._guide = load_guide()
        return self._guide

PART C. search_guide and read_file. read_file resolves the path with os.path.realpath before the check, so "data/clients/../libv/v1.py" is denied:
def search_guide(ctx, query, k=3):
    hits = retrieve(query, ctx.guide, k=k, expand=ctx.expand)
    ids = [s["id"] for s in hits]
    ctx.retrieved_ids.extend(ids)
    return [{"id": s["id"], "title": s["title"],
             "text": (s["text"] + "\nBEFORE:\n" + s["before"] + "\nAFTER:\n" + s["after"])[:MAX_TEXT + 200]}
            for s in hits]


def read_file(ctx, path):
    full = os.path.realpath(os.path.join(ROOT, path))
    if not any(full == r or full.startswith(r) for r in READABLE):
        return {"error": "read denied: only data/clients/ and data/libv/v2.py are readable"}
    if not os.path.isfile(full):
        return {"error": f"no such file: {path}"}
    return {"path": path, "text": open(full).read()}

PART D. write_file. Keep this order: build the gate record and append it to ctx.gates FIRST (every attempt is logged, allowed or denied), then call check_write. When denied, write NOTHING and return the reason. When allowed, write to ctx.client_file, adding a final newline if the text has none:
def write_file(ctx, path, text):
    rec = gate_record(path, ctx.client_file, ctx.case_id)
    ctx.gates.append(rec)
    ok, reason = check_write(path, ctx.client_file)
    if not ok:
        return {"ok": False, "error": reason}
    with open(os.path.join(ROOT, ctx.client_file), "w") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    return {"ok": True}

PART E. run_tests. Keep the __pycache__ removal and its comment, PYTHONDONTWRITEBYTECODE, "-p", "no:cacheprovider", the 30 s timeout and the failed-count parsing exactly as shown:
def run_tests(ctx, client=None):
    name = os.path.splitext(os.path.basename(client or ctx.client_file))[0]
    test = os.path.join("data", "clients", "tests", f"test_{name}.py")
    if not os.path.isfile(os.path.join(ROOT, test)):
        return {"exit_code": 4, "failed": 0, "first_failure": f"no test file {test}"}
    # A rewrite of the same size in the same second can leave a stale .pyc that Python
    # still trusts, so clear the client bytecode cache and never write a new one.
    shutil.rmtree(os.path.join(ROOT, "data", "clients", "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test],
                           cwd=ROOT, capture_output=True, text=True, timeout=TEST_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "failed": 0, "first_failure": f"timeout after {TEST_TIMEOUT}s"}
    out = p.stdout + p.stderr
    failed = sum(int(n) for n in re.findall(r"(\d+) (?:failed|errors?)\b", out.splitlines()[-1] if out.strip() else ""))
    first = ""
    if p.returncode != 0:
        lines = [l for l in out.splitlines() if l.startswith("E ") or "Error" in l]
        first = "\n".join(lines[:8]) or out[-800:]
    if p.returncode != 0 and failed == 0:
        failed = 1  # collection/import error
    return {"exit_code": p.returncode, "failed": failed if p.returncode else 0, "first_failure": first[:800]}

PART F. The registry and the two tool lists. Keep the 4 desc strings word for word (the model reads them):
TOOL_REGISTRY = {
    "search_guide": {
        "fn": search_guide,
        "args": {"query": str, "k": int},
        "required": ["query"],
        "desc": "search_guide(query: str, k: int = 3) -> list of {id, title, text}. Keyword search over "
                "the v1->v2 migration guide. Put the v1 names you see in the client in the query.",
    },
    "read_file": {
        "fn": read_file,
        "args": {"path": str},
        "required": ["path"],
        "desc": "read_file(path: str) -> {path, text}. Read-only; allowed: data/clients/..., data/libv/v2.py.",
    },
    "write_file": {
        "fn": write_file,
        "args": {"path": str, "text": str},
        "required": ["path", "text"],
        "desc": "write_file(path: str, text: str) -> {ok}. Overwrites the WHOLE file. Only the current "
                "client file may be written; anything else is denied.",
    },
    "run_tests": {
        "fn": run_tests,
        "args": {"client": str},
        "required": [],
        "desc": "run_tests(client: str) -> {exit_code, failed, first_failure}. Runs the client's pytest "
                "file against libv v2 (30 s timeout). exit_code 0 means green.",
    },
}

BASELINE_TOOLS = ["read_file", "write_file", "run_tests"]
IMPROVED_TOOLS = ["search_guide", "read_file", "write_file", "run_tests"]

PART G. validate_arguments (the checks in exactly this order: tool allowed, args is a dict, required args present, no unexpected arg, types), build_tools_desc, dispatch and __all__:
def validate_arguments(name, args, allowed):
    if name not in allowed:
        return f"unknown or unavailable tool {name!r}; available: {', '.join(allowed)}"
    if not isinstance(args, dict):
        return "args must be a JSON object"
    spec = TOOL_REGISTRY[name]
    for r in spec["required"]:
        if r not in args:
            return f"missing argument {r!r} for {name}"
    for k, v in args.items():
        if k not in spec["args"]:
            return f"unexpected argument {k!r} for {name}"
        if not isinstance(v, spec["args"][k]):
            return f"argument {k!r} must be {spec['args'][k].__name__}"
    return None


def build_tools_desc(allowed):
    return "\n".join(f"- {TOOL_REGISTRY[n]['desc']}" for n in allowed)


def dispatch(ctx, name, args):
    return TOOL_REGISTRY[name]["fn"](ctx, **args)


__all__ = ["CaseContext", "TOOL_REGISTRY", "BASELINE_TOOLS", "IMPROVED_TOOLS", "validate_arguments",
           "build_tools_desc", "dispatch", "v1_leftovers"]
````

Check (paste this block on its own). It makes no gateway calls, and it restores `client_01.py` itself:

```bash
python3 - <<'PY'
import os
from harness.tools import (ROOT, CaseContext, TOOL_REGISTRY, BASELINE_TOOLS, IMPROVED_TOOLS,
                           validate_arguments, build_tools_desc, dispatch)
C, H = "data/clients/client_01.py", "eval/hand_migrations/client_01.py"
rd = lambda p: open(os.path.join(ROOT, p)).read()
ctx = CaseContext("case_01", C)
hits = dispatch(ctx, "search_guide", {"query": "get_balance"})
assert hits[0]["id"] == "G01" and "BEFORE:" in hits[0]["text"] and "AFTER:" in hits[0]["text"], hits
assert ctx.retrieved_ids[0] == "G01" and set(hits[0]) == {"id", "title", "text"} and all(len(x["text"]) <= 800 for x in hits)
assert len(dispatch(ctx, "search_guide", {"query": "get_balance transfer charge_and_receipt", "k": 10})) <= 3
big = CaseContext("case_x", C)
big._guide = [{"id": "L1", "title": "long", "text": "long " * 400, "before": "b", "after": "a"}]
assert len(dispatch(big, "search_guide", {"query": "long"})[0]["text"]) == 800, "search_guide must cut text to MAX_TEXT + 200"
assert "text" in dispatch(ctx, "read_file", {"path": C}) and "text" in dispatch(ctx, "read_file", {"path": "data/libv/v2.py"})
for bad in ("data/libv/v1.py", "data/clients/../libv/v1.py", "eval/hand_migrations/client_01.py",
            "../../etc/passwd", os.path.join(ROOT, "data", "libv", "v1.py"), "data/clients/nope.py"):
    assert "error" in dispatch(ctx, "read_file", {"path": bad}), bad
keep = {p: rd(p) for p in ("data/libv/v2.py", "data/clients/client_02.py", "data/clients/tests/test_client_01.py")}
for bad in keep:
    n = len(ctx.gates)
    r = dispatch(ctx, "write_file", {"path": bad, "text": "x = 1\n"})
    assert r["ok"] is False and r.get("error") and len(ctx.gates) == n + 1, (bad, r)
    assert ctx.gates[-1]["decision"] == "deny" and ctx.gates[-1]["path"] == bad, ctx.gates[-1]
assert all(rd(p) == s for p, s in keep.items()), "a denied write changed a file"
orig = rd(C)
try:
    assert dispatch(ctx, "write_file", {"path": C, "text": "x = 1"})["ok"] is True and ctx.gates[-1]["decision"] == "allow"
    assert rd(C) == "x = 1\n", "write_file must write the client file and add a final newline"
    open(os.path.join(ROOT, C), "w").write(rd(H))
    t = dispatch(ctx, "run_tests", {})
    assert t == {"exit_code": 0, "failed": 0, "first_failure": ""}, t
finally:
    open(os.path.join(ROOT, C), "w").write(orig)
pc = os.path.join(ROOT, "data", "clients", "__pycache__")
os.makedirs(pc, exist_ok=True)
open(os.path.join(pc, "stale.pyc"), "w").close()
t = dispatch(ctx, "run_tests", {})
assert t["exit_code"] != 0 and t["failed"] >= 1 and t["first_failure"], t
assert not os.path.exists(pc), "run_tests must delete data/clients/__pycache__ first and never write a new one"
assert dispatch(ctx, "run_tests", {"client": "data/clients/nope.py"})["exit_code"] == 4
assert validate_arguments("search_guide", {"query": "x"}, BASELINE_TOOLS)
assert validate_arguments("search_guide", {"query": "x"}, IMPROVED_TOOLS) is None
assert validate_arguments("search_guide", {"query": "x", "k": "3"}, IMPROVED_TOOLS)
assert validate_arguments("read_file", [], BASELINE_TOOLS) and validate_arguments("read_file", {}, BASELINE_TOOLS)
assert validate_arguments("read_file", {"path": 1}, BASELINE_TOOLS) and validate_arguments("read_file", {"path": "a", "x": 1}, BASELINE_TOOLS)
assert validate_arguments("read_file", {"path": "a"}, BASELINE_TOOLS) is None and validate_arguments("run_tests", {}, BASELINE_TOOLS) is None
assert sorted(TOOL_REGISTRY) == ["read_file", "run_tests", "search_guide", "write_file"]
assert build_tools_desc(IMPROVED_TOOLS).count("\n- ") == 3 and build_tools_desc(BASELINE_TOOLS).startswith("- read_file")
print("tools OK")
PY
```

```bash
git status --short
```

The check must print `tools OK`, and `git status` must list only `?? harness/model.py` and
`?? harness/tools.py`. Fallback for this run: `unzip -o ~/capstone-g15-fallback-C4-C13.zip harness/tools.py`.

Commit and push:

```bash
git add harness/model.py harness/tools.py && git commit -m "Day 3: gateway client and tool registry (search_guide, read_file, scoped write_file, run_tests)" && git push
```

#### C10 · Day 4 · agent loop

`harness/agent.py` is long, so Qwen writes it in two runs. Run 2 keeps run 1's code and adds the loop.

**Run 1 of 2: helpers, prompt text and the reply parser**

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/agent.py --read harness/tools.py --read harness/model.py --read harness/retrieval.py --read data/libv/v2.py --read eval/cases/case_01.json
```

Prompt:

````text
Write harness/agent.py, PART 1 of 2 (replace anything already in it): the module docstring, imports, constants and helpers. run_case() and main() come in my next prompt, so do NOT write them yet. The read-only files are finished. Do not create or touch any other file.

Copy the code of every PART below exactly, in this order: the same names, strings, numbers, comments and 4-space indentation, with two blank lines between top-level definitions. The PART lines are labels for you: do not write them into the file. Do not add type hints, prints, logging, classes or extra functions, and do not shorten or "simplify" anything.

Two places need special care:
1. SYSTEM is filled in with str.format, so the doubled braces {{ and }} stay doubled, and {guide_rule} and {tools} stay single. Keep its line breaks exactly as shown. No line of the file may start with three backticks, because aider would end the file at that line. That is why ```python ... ``` sits in the middle of the line that starts with "in a".
2. parse_action uses FENCE_RE, which matches fences as open/close pairs. Never split the reply on ``` by hand: a ```json fence around the action must be skipped and the ```python block used.

PART A. Module docstring:
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

PART B. Imports, ROOT and the harness bounds (keep the comments):
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

PART C. utc_now and git_user:
def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_user():
    try:
        return subprocess.run(["git", "config", "user.name"], cwd=ROOT, capture_output=True,
                              text=True, timeout=5).stdout.strip() or "unknown"
    except Exception:
        return "unknown"

PART D. v2_signatures: the public def/class lines of v2.py without bodies or docstrings, which is what the baseline sees:
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

PART E. load_cases:
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

PART F. SYSTEM, GUIDE_RULE and first_user_message:
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

PART G. THINK_RE, FENCE_RE and parse_action:
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

PART H. short_args and Trace:
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
````

Check, part 1 (paste this block on its own):

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

It must print `agent part 1 OK`. The `r1` line is the json-fence bug from the first version. Fallback for
both runs of C10: `unzip -o ~/capstone-g15-fallback-C4-C13.zip harness/agent.py` (it has PARTs A to J).

**Run 2 of 2: the loop, the trace and the result file**

```bash
aider --no-auto-commits --edit-format whole --map-tokens 0 harness/agent.py --read harness/tools.py --read harness/model.py --read harness/v1check.py --read harness/retrieval.py
```

Prompt:

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

Check, part 2. It runs the loop 3 times with a **scripted fake model**: no gateway calls, and nothing is
written to `traces/` or `eval/results/`. Paste this block on its own:

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

```bash
python3 -m pytest -q -p no:cacheprovider data/libv/tests harness safety
git status --short
```

It must print `agent loop OK`, then `26 passed`, and `git status` must list only `?? harness/agent.py`.
Run the part 1 check again too, because run 2 rewrote the whole file.

Commit and push:

```bash
git add harness/agent.py && git commit -m "Day 4: agent loop with step limit, trace and result writer" && git push
```

#### C11 · Day 4 · smoke run: one file migrated, with a trace (your key)

The commit block finds the run id by itself (the newest file in `eval/results/`), so a new terminal is fine.

```bash
python3 -m harness.agent --variant baseline --only case_01
```

It prints `run_id p04-baseline-...`, one line for case_01, then the trace and result paths. It makes 2 to 8
model calls.

Check:

```bash
git status --short data/clients
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
assert {"run_start", "step", "case_end", "run_end"} <= types, types
assert all(r.get("response_id") for r in rows if r["type"] == "step"), "a step row has no response_id"
print(d["run_id"], d["member"], d["summary"]["fully_migrated"], "/", d["summary"]["cases"], "calls", d["summary"]["calls_total"])
PY
```

`git status` must print nothing, because the client is restored after the case. The script prints the run
id, **your** Gitea user, the score and the number of calls. An `AssertionError` mentioning `step` means
the model call failed; read the `error` row in the trace and see section 9.

```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && git add traces/ eval/results/ && git commit -m "Day 4: baseline smoke run on case_01 (run $RUN)" && git push
```

#### C12 · Day 4 · CAPSTONE.md: Architecture and Harness bounds

This script replaces the two placeholder lines in CAPSTONE.md with the text:

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
git --no-pager diff --stat
```

It prints `CAPSTONE.md updated`, and the diff shows only `CAPSTONE.md` changed.

Commit and push:

```bash
git add CAPSTONE.md && git commit -m "Day 4: CAPSTONE.md architecture and harness bounds" && git push
```

End of turn:

```bash
git log -1 --format=%h
```

Post "C12 pushed, <hash>". **M4 goes next.**

