# P04 / g15: fixes after C32 (F1 to F7)

The CP2 and round 1 and 2 results are in (up to C32). This file is the fix and improvement step that the traces call
for. The final CAPSTONE.md / EVIDENCE.md text and the slides are done by M2 afterwards; section 6 lists the facts to
put in them.

Everything below was run end to end on a copy of main (`aa421981de80`) with 3 member clones and a shared origin:
real aider 0.86.1 for F1 and F2 against a fake gateway with the 16,384 / 4,096 limits, and the harness against a
scripted fake model. Every check, run and commit passed in this order. What a real Qwen run gives is not known
until F4 and F6: whatever it is, it gets committed.

## 0. What the traces show, and what changes

| Case | Baseline (calls) | Improved (calls) | Cause in the trace | Fix |
|---|---|---|---|---|
| case_09 | migrated (4) | **failed (8)**, both rounds | Same `TypeError: list_transactions() missing ... 'limit'` as the baseline at step 3. Then 5 `search_guide` calls in a row (steps 4 to 8), each returning G09, which never says that `limit` lost its default (its BEFORE and AFTER are the same line). Out of steps. | **F1**: G09 says the limit must be passed (v1 used 10), with a BEFORE and AFTER that differ. **F2**: a repeat search returns a short note instead of the same text. |
| case_02 | failed (8) | failed (8), both rounds | G02 was retrieved at step 1, but Qwen still wrote `transfer(payer_id, friend_id, share)`: it ordered the ids by their names. The old G02 only listed parameter names. | **F1**: G02 says that only the amount moves and the two ids keep their order, with an example. |
| case_12 | migrated, on the last allowed call (8) | migrated (3) | The guide already helps here (G08, paise). | none |

Not changed: the baseline (it uses neither the guide nor search_guide, and `agent.py` is unchanged, so rounds 1 and 2
of the baseline stay valid), the cases, the tests, the hand migrations, and the first improved runs (they stay in the
repo as "improved, first guide"). The new improved runs get the tag `v2` and the new backup run the tag `backup2`.

Retrieval: of the 19 different search queries Qwen sent in the improved runs, 18 return the same sections with
the new guide; `list_transactions limit argument` now returns G02 as a second hit after G09. No query loses a
section it needs (checked in F1).

**Be honest about it in the report:** the guide was rewritten after seeing results on the same 12 cases, so the `v2`
numbers are optimistic. Say so in Limitations.

## 1. Who does what (relay order)

| # | Member | What | Files | Commit message |
|---|---|---|---|---|
| F1 | M1 agastyan (wrote the guide) | aider: rewrite G02 and G09, regenerate guide.json | `data/make_guide.py`, `data/guide.json` | `Day 9: guide G02 and G09 rewritten after the case_02 and case_09 traces` |
| F2 | M3 varunr (wrote tools.py) | aider: repeat-search note in `search_guide` | `harness/tools.py` | `Day 9: search_guide says when it has no new sections (stops search loops)` |
| F3 | M3 varunr | backup run of the live cases with the fixed guide (your key) | traces/, eval/results/ | `Day 9: backup run $RUN of the live cases (fixed guide)` |
| F4 | M4 yallappagarid | improved run, fixed guide, round 1 (your key) | traces/, eval/results/ | `Day 9: improved run $RUN on 12 cases (fixed guide, round 1)` |
| F5 | M4 yallappagarid | compare with baseline round 1 | eval/results/compare-...md | `Day 9: compare baseline round 1 vs fixed improved round 1` |
| F6 | M1 agastyan | improved run, fixed guide, round 2 (your key) | traces/, eval/results/ | `Day 10: improved run $RUN on 12 cases (fixed guide, round 2)` |
| F7 | M1 agastyan | compare with baseline round 2 | eval/results/compare-...md | `Day 10: compare baseline round 2 vs fixed improved round 2` |
| then | M2 paritoshl | CAPSTONE.md, EVIDENCE.md, slides.pdf, freeze row | | (yours) |

Each run is about 45 to 50 model calls and 2 minutes; the backup about 10 calls and under a minute.

## 2. Rules (same as before)

- Pull first, push after every commit, never force-push, your own login and key.
- One aider session per prompt: start aider with the exact command, type `/clear`, paste the box, wait for
  `Applied edit to ...`, type `/exit`. Answer **N** if aider asks about any other file.
- Commit only after the check prints its OK line. If a file differs, the check prints the line number and the line.
- A run with `ERROR ROW` lines (gateway errors) is not valid: delete it and run again (section 7).

## 3. Turn A: M1 agastyan (F1)

Start of turn:

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -3
```

The top line must be `... Day 8: CAPSTONE.md results and one failure diagnosed from a trace` (M4's C32). If it isn't, the previous member hasn't pushed yet: wait.

```bash
git status --short
```

This must print nothing.

#### F1 · rewrite guide sections G02 and G09

Start aider:

```bash
aider --no-auto-commits --edit-format diff --map-tokens 0 data/make_guide.py
```

Type `/clear` and press Enter, then paste this whole box and press Enter:

````text
Task F1. Edit ONLY data/make_guide.py: rewrite two sections of the migration guide, G02 and G09. Make exactly the 2 changes below and nothing else. Do not change any other section, the json.dump at the end, the formatting or the 4-space indentation, and do not create or edit any other file (data/guide.json is regenerated from this script afterwards, by running it).

Why: our improved runs showed two gaps in the guide text.
- case_02: search_guide returned G02 at step 1, but the model still swapped the two account ids, because the old G02 only listed the parameter names. The new G02 says that only the amount moves to the end and that the two ids keep their order, with an example.
- case_09: the old G09 never said that list_transactions lost its default limit, and its BEFORE and AFTER were the same line. The model searched 5 times in a row for "limit" and ran out of steps. The new G09 says that the limit must now be passed (v1 used 10) and that the items are Transaction objects, with a BEFORE and AFTER that differ.

Reply with exactly 2 SEARCH/REPLACE blocks for data/make_guide.py, one per change, in this order. Write the path data/make_guide.py on the line before each block. Each SEARCH part must be copied exactly from the file as it is now (the "Find" text below), and each REPLACE part is the "replace it with" text. Copy the new strings exactly: the backticks, the single quotes inside the strings, and the two characters \n (a backslash and an n, which the script turns into a line break) inside the "before" and "after" of G09. Do not turn \n into a real line break.

CHANGE 1. Find this exact text:
    {
        "id": "G02",
        "title": "Order of arguments in transfer changed",
        "text": "The order of arguments in the `transfer` function was changed from `amount, from_id, to_id` to `from_id, to_id, amount`.",
        "before": "transfer(amount, from_id, to_id)",
        "after": "transfer(from_id, to_id, amount)"
    },
and replace it with:
    {
        "id": "G02",
        "title": "Order of arguments in transfer changed: the amount moves to the end",
        "text": "In v2 the amount is the last argument of `transfer`: v1 `transfer(amount, from_id, to_id)` becomes v2 `transfer(from_id, to_id, amount)`. Only the amount moves. The two account ids keep their order, so the money still goes from the same account to the same account. Do not swap the ids because of what their variable names suggest.",
        "before": "transfer(25.0, acc_a, acc_b)  # acc_a pays acc_b 25.0",
        "after": "transfer(acc_a, acc_b, 25.0)  # still acc_a pays acc_b"
    },

CHANGE 2. Find this exact text:
    {
        "id": "G09",
        "title": "list_transactions returns Transaction objects",
        "text": "The `list_transactions` function now returns a list of `Transaction` objects instead of dictionaries.",
        "before": "transactions = list_transactions(acc, 10)",
        "after": "transactions = list_transactions(acc, 10)"
    },
and replace it with:
    {
        "id": "G09",
        "title": "list_transactions needs a limit and returns Transaction objects",
        "text": "In v2 `limit` has no default any more, so pass it explicitly. v1 used 10 when it was left out, so `list_transactions(acc)` becomes `list_transactions(acc, 10)`. The items are `Transaction` objects instead of dictionaries: read `tx.amount` and `tx.tx_id` instead of `tx['amount']` and `tx['id']`.",
        "before": "recent = list_transactions(acc)\nfirst_id = recent[0]['id']",
        "after": "recent = list_transactions(acc, 10)\nfirst_id = recent[0].tx_id"
    },
````

aider must print **`Applied edit to data/make_guide.py`**. If it asks to edit or create any other file, answer **N**. Then type `/exit`.

Regenerate `data/guide.json` from the script and validate it (must print `12 sections, 0 errors`):

```bash
python3 data/make_guide.py && python3 data/validate_guide.py
```

**Check**, paste it on its own; it must end with `F1 OK`:

```bash
python3 - <<'PY'
import difflib, hashlib, json, os, subprocess, sys
def h8(t):
    return hashlib.sha256(t.encode()).hexdigest()[:8]
def as_asked(p, want):
    if not os.path.isfile(p):
        print("MISSING:", p)
        return False
    mine = [(n, l.rstrip()) for n, l in enumerate(open(p).read().splitlines(), 1) if l.strip()]
    ref = [want[i:i + 8] for i in range(0, len(want), 8)]
    ops = difflib.SequenceMatcher(None, [h8(l) for _, l in mine], ref, autojunk=False).get_opcodes()
    if all(op[0] == "equal" for op in ops):
        return True
    print("DIFFERS FROM WHAT THE PROMPT ASKS FOR:", p)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        for n, l in mine[i1:i2]:
            print(f"  line {n} is not as asked: {l.strip()[:110]}")
        if i1 == i2:
            after = mine[i1 - 1][0] if i1 else 0
            print(f"  {j2 - j1} line(s) asked for are missing after line {after}")
    return False
assert as_asked("data/make_guide.py", "ff3e4d4dffcd426b0d3d2f5afc970c2ab9cba67ea1cc855ebba0c04e623bf32758636dd90d3d2f5a6eb1b71e8b349e80563e58c92cfa7e08b406f65658636dd90d3d2f5ad7f3e6f0f8534b2af95dfed20a101a419a739cf058636dd90d3d2f5ae13f69daa03b4b6d4d032375148f85c1bb625c3358636dd90d3d2f5af9928c72a6cc90e30583dfb896aca9537706dbb658636dd90d3d2f5a11698706fb3843d4ab07670587b190b9775f8dfb58636dd90d3d2f5a1e088a25ebc496aa96efef54950b305f57e47da458636dd90d3d2f5ad8818cdfcde40d98ed8fd174b9453b9af9d0bfc858636dd90d3d2f5ada1358f18a9f69011a48e68967bcbc3315f956af58636dd90d3d2f5abdd25dd0a142450f9f837d36148d08a89fdf90b758636dd90d3d2f5adf6bccde9458bdc39fbedd4aa75c38dfc9bc30ed58636dd90d3d2f5a50945d05fc7f7389099e3ba6c6e126c85395f56e28d86778cfae0d4228dea7dfb89e6861"), "fix data/make_guide.py (playbook: If something goes wrong)"
guide = json.load(open("data/guide.json"))
SECTIONS = {"G01": "041fa0ac", "G02": "956796af", "G03": "99413a5d", "G04": "327eccd1", "G05": "5f1b1d03", "G06": "05ea1074", "G07": "e1fcbd8c", "G08": "62612eff", "G09": "73c5b90a", "G10": "bf6d6b2b", "G11": "62ba7f96", "G12": "906638f0"}
got = {s["id"]: h8(json.dumps(s, sort_keys=True)) for s in guide}
bad = sorted(k for k in set(got) | set(SECTIONS) if got.get(k) != SECTIONS.get(k))
assert not bad, "data/guide.json sections differ: " + ", ".join(bad) + " (did you run python3 data/make_guide.py?)"
r = subprocess.run([sys.executable, "data/validate_guide.py"], capture_output=True, text=True)
print(r.stdout.strip())
assert r.returncode == 0 and "0 errors" in r.stdout
sys.path.insert(0, os.getcwd())
from harness.retrieval import retrieve
for q, want in [["get_balance", ["G01", "G03", "G05"]], ["transfer", ["G02"]], ["transfer behavior", ["G02"]], ["get_transaction", ["G03", "G01", "G09"]], ["charge_and_receipt", ["G04", "G07"]], ["get_balance, transfer, get_transaction", ["G03", "G01", "G02"]], ["withdraw, InsufficientFunds", ["G05"]], ["withdraw, AccountNotFound, PaymentError", ["G12", "G06", "G10"]], ["charge", ["G04", "G07"]], ["list_transactions", ["G09"]], ["list_transactions default limit", ["G09"]], ["list_transactions limit", ["G09"]], ["list_transactions limit argument", ["G09", "G02"]], ["list_transactions limit default", ["G09"]], ["list_transactions limit parameter", ["G09"]], ["list_transactions limit parameter v2", ["G09"]], ["open_account, convert", ["G10", "G11", "G06"]], ["get_balance, AccountNotFound", ["G01", "G06", "G10"]], ["get_balance, format_amount", ["G08", "G01", "G03"]]]:
    ids = [s["id"] for s in retrieve(q, guide, k=3)]
    assert ids == want, (q, ids, want)
print("retrieval: all", 19, "queries from our improved traces return the expected sections")
st = sorted(subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.splitlines())
assert st == [" M data/guide.json", " M data/make_guide.py"], "git status must list exactly the two guide files, but lists: " + repr(st)
print("F1 OK")
PY
```
It checks the script line by line, every section of guide.json, the validator, that the 19 real search queries return the expected sections, and that only the two guide files changed.

```bash
git add data/make_guide.py data/guide.json && git commit -m "Day 9: guide G02 and G09 rewritten after the case_02 and case_09 traces" && git push
```

Post "F1 pushed, <hash>" (`git log -1 --format=%h`). **M3 goes next.**

## 4. Turn B: M3 varunr (F2, F3)

Start of turn:

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -3
```

The top line must be M1's `... Day 9: guide G02 and G09 rewritten after the case_02 and case_09 traces`. If it isn't, the previous member hasn't pushed yet: wait.

```bash
git status --short
```

This must print nothing.

#### F2 · repeat-search note in search_guide

Start aider:

```bash
aider --no-auto-commits --edit-format diff --map-tokens 0 harness/tools.py
```

Type `/clear` and press Enter, then paste this whole box and press Enter:

````text
Task F2. Edit ONLY harness/tools.py, and only inside the function search_guide(). Make exactly the 1 change below and nothing else: do not change any other function, line, name, comment or the formatting, and do not create or edit any other file.

Why: in our improved runs on case_09 the model called search_guide 5 times in a row, got the same section (G09) back every time and ran out of its 8 steps. After the change, when every section a search returns was already returned earlier in the same file, search_guide does not repeat their text. It returns a short dict instead: "no_new_sections" (the ids) and a "note" that tells the model to fix the client from the test error and the v2 signatures. A search that finds at least one new section, or none at all, works exactly as before. ctx.retrieved_ids is still extended in every case, so the hit rate is computed as before.

Reply with exactly 1 SEARCH/REPLACE block for harness/tools.py. Write the path harness/tools.py on the line before the block. The SEARCH part must be copied exactly from the file as it is now (the "Find" text below), and the REPLACE part is the "replace it with" text, with the same 4-space indentation.

CHANGE 1. Find this exact text:
    hits = retrieve(query, ctx.guide, k=k, expand=ctx.expand)
    ids = [s["id"] for s in hits]
    ctx.retrieved_ids.extend(ids)
    return [{"id": s["id"], "title": s["title"],
and replace it with:
    hits = retrieve(query, ctx.guide, k=k, expand=ctx.expand)
    ids = [s["id"] for s in hits]
    seen_all = bool(ids) and all(i in ctx.retrieved_ids for i in ids)
    ctx.retrieved_ids.extend(ids)
    if seen_all:
        # Nothing new: repeating the same sections only fills the context (case_09 searched 5 times in a row).
        return {"no_new_sections": ids,
                "note": "search_guide already returned these sections in this file; the guide has nothing more on "
                        "this. Fix the client from the test error and the v2 signatures instead of searching again."}
    return [{"id": s["id"], "title": s["title"],
````

aider must print **`Applied edit to harness/tools.py`**. If it asks to edit or create any other file, answer **N**. Then type `/exit`.

**Check**, paste it on its own; it must end with `F2 OK`:

```bash
python3 - <<'PY'
import difflib, hashlib, json, os, subprocess, sys
def h8(t):
    return hashlib.sha256(t.encode()).hexdigest()[:8]
def as_asked(p, want):
    if not os.path.isfile(p):
        print("MISSING:", p)
        return False
    mine = [(n, l.rstrip()) for n, l in enumerate(open(p).read().splitlines(), 1) if l.strip()]
    ref = [want[i:i + 8] for i in range(0, len(want), 8)]
    ops = difflib.SequenceMatcher(None, [h8(l) for _, l in mine], ref, autojunk=False).get_opcodes()
    if all(op[0] == "equal" for op in ops):
        return True
    print("DIFFERS FROM WHAT THE PROMPT ASKS FOR:", p)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        for n, l in mine[i1:i2]:
            print(f"  line {n} is not as asked: {l.strip()[:110]}")
        if i1 == i2:
            after = mine[i1 - 1][0] if i1 else 0
            print(f"  {j2 - j1} line(s) asked for are missing after line {after}")
    return False
assert as_asked("harness/tools.py", "c2c9e0b3fa915915a75995feb6d267efde2abade66ec0182582f9ff77d8752c49e77b374fcadc20dd54318a533dcd1a4a3291e3dc482a224f3b8cc1b4ba326aefe3159062183d73a56cdb4d1555d1ae81cee0ee18d9c19c575b495f740011dc950150bde39708d844f5be4f80c1c75627f0d74b186094f97b79dca5f0e0c4f58a1220e20767a379ae89e47519c246f4a29f9ddcb046d562184a210a7b1da992c77ea857b68b38b7a64ab7c23cc7822ffa9c89ecd0f8851101a9ac11840d7e6cf1b2e78fa8d8abc7812cd858ce1198394a5aca8ee9804e0cd4168b03a2b1a375cba95f293f77b7b866cc4221d3d29bf817b5e21c32d2a6f32055fea36ebb3decf35bc93da32750d7684462ae1c94f2f6f01c3180be965b0dc7035f759ee926624b56a47cbfdce5f3c1bdb67e5c75c3fe70c9ebdf38132e857200973edac3f1cb26d917959374818e8311a9e37a23f34a40caced675c26f9414ae591ef1a6a2e4c58636dd9d718bf74a0e36dab86a6403ad90dfeab318c63e458636dd930ac9e0e50920ed62a0d71d2413a5922cc047305401d40e858636dd95bc714976beb3e6d18786a6ef32d115d33d8afeff748666358636dd9d10b36aaad6fb201b26c1c03a03b3a04c213610bd4d01641a9da00bf1742218e230ef3a4b104e87e8f2f045dd479f5a6dd0d4b627b346ae7a9f4572145efad6f0fd50637ad4a411359e7e8a21b3acd145c0c63d617a3167eaeabe8145b541220"), "fix harness/tools.py (playbook: If something goes wrong)"
from harness.tools import CaseContext, search_guide
ctx = CaseContext("case_09", "data/clients/client_09.py")
a = search_guide(ctx, "list_transactions")
assert isinstance(a, list) and [s["id"] for s in a] == ["G09"], a
b = search_guide(ctx, "list_transactions limit")
assert isinstance(b, dict) and b["no_new_sections"] == ["G09"] and "instead of searching again" in b["note"], b
c = search_guide(ctx, "get_balance")
assert isinstance(c, list) and [s["id"] for s in c] == ["G01", "G03", "G05"], c
assert search_guide(ctx, "zzz qqq") == []
assert ctx.retrieved_ids == ["G09", "G09", "G01", "G03", "G05"], ctx.retrieved_ids
print("search_guide: new sections as before, repeats -> note, retrieved ids still counted")
import harness.model
import harness.agent as agent
hand = open("eval/hand_migrations/client_09.py").read()
orig = open("data/clients/client_09.py").read()
plan = ['{"tool": "search_guide", "args": {"query": "list_transactions"}}',
        '{"tool": "search_guide", "args": {"query": "list_transactions limit"}}',
        '```json\n{"tool": "write_file", "args": {"path": "data/clients/client_09.py"}}\n```\n\n```python\n%s```' % hand,
        '{"tool": "run_tests", "args": {}}']
def fake(messages, model="main", **kw):
    n = sum(1 for m in messages if m["role"] == "assistant")
    return {"text": plan[min(n, 3)], "prompt_tokens": 10, "completion_tokens": 5, "latency_ms": 1, "model": model,
            "response_id": "fake-id", "finish_reason": "stop"}
harness.model.call_model = fake
agent.PACING = 0
rid = agent.main(["--variant", "improved", "--only", "case_09", "--tag", "selfcheck"])
made = [os.path.join("traces", rid + ".jsonl"), os.path.join("eval", "results", rid + ".json")]
try:
    rows = [json.loads(line) for line in open(made[0])]
    steps = [r for r in rows if r["type"] == "step"]
    assert "no_new_sections" in steps[1]["observation"], steps[1]["observation"]
    d = json.load(open(made[1]))
    assert d["cases"][0]["fully_migrated"] and d["cases"][0]["hit_rate"] == 1.0, d["cases"][0]
    assert open("data/clients/client_09.py").read() == orig, "client_09 not restored"
finally:
    for p in made:
        if os.path.exists(p):
            os.remove(p)
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "data/libv/tests", "harness", "safety"],
                   capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
print("unit tests:", r.stdout.strip().splitlines()[-1])
assert r.returncode == 0
st = sorted(subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.splitlines())
assert st == [" M harness/tools.py"], "git status must list only harness/tools.py, but lists: " + repr(st)
print("F2 OK")
PY
```
It calls search_guide directly (new section, repeat, new again, nothing found), runs the agent once on case_09 with a scripted fake model (no gateway call) to see the note in the trace, then runs the 26 unit tests.

```bash
git add harness/tools.py && git commit -m "Day 9: search_guide says when it has no new sections (stops search loops)" && git push
```

#### F3 · new backup run (your key)

The live run now uses the fixed guide, so the backup has to be recorded again:

```bash
bash live/run_live.sh backup2
```

**Check**, paste it on its own; it must end with `backup OK`:

```bash
python3 - <<'PY'
import glob, json, os, subprocess
CASES, TAG = 2, "backup2"
user = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
assert user in ("agastyan", "paritoshl", "varunr", "yallappagarid"), "git config user.name is " + repr(user)
g09 = [s for s in json.load(open("data/guide.json")) if s["id"] == "G09"][0]
assert g09["title"].startswith("list_transactions needs a limit"), "data/guide.json is the old guide: pull F1 first"
assert "no_new_sections" in open("harness/tools.py").read(), "harness/tools.py is the old version: pull F2 first"
f = max(glob.glob(f"eval/results/p04-improved-*-{TAG}.json"), key=os.path.getmtime)
d = json.load(open(f))
assert d["member"] == user, (d["member"], user)
assert d["summary"]["cases"] == CASES, d["summary"]
rows = [json.loads(line) for line in open(d["trace"])]
errs = [r for r in rows if r["type"] == "error"]
for r in errs:
    print("ERROR ROW:", r["case_id"], "step", r["step"], r["error"])
steps = [r for r in rows if r["type"] == "step"]
assert steps and all(r.get("response_id") for r in steps), "a step row has no response_id"
for c in d["cases"]:
    notes = sum(1 for r in steps if r["case_id"] == c["case_id"] and "no_new_sections" in (r.get("observation") or ""))
    print(f"  {c['case_id']}: migrated={c['fully_migrated']} stop={c['stop_reason']} calls={c['calls']} "
          f"tokens={c['tokens']} retrieved={','.join(c['retrieved_ids']) or '-'} repeat_notes={notes} "
          f"denied={','.join(c['gate_denied_paths']) or '-'}")
peak = max(r["prompt_tokens"] for r in steps)
assert peak + 2000 <= 16384, f"prompt {peak} + 2000 reply tokens is over the 16,384 context"
changed = subprocess.run(["git", "status", "--short", "data", "eval/cases", "eval/hand_migrations", "harness", "safety", "live"],
                         capture_output=True, text=True).stdout
assert not changed.strip(), "files outside traces/ and eval/results/ changed:\n" + changed
assert not errs, "model errors in this run: delete its two files and run it again (playbook: If something goes wrong)"
s = d["summary"]
print(d["run_id"], d["member"], "fully migrated", s["fully_migrated"], "/", s["cases"], "calls", s["calls_total"],
      "tokens", s["tokens_total"], "hit_rate", s["retrieval_hit_rate"], "peak prompt", peak)
from datetime import datetime
secs = (datetime.fromisoformat(d["ended_utc"].rstrip("Z")) - datetime.fromisoformat(d["started_utc"].rstrip("Z"))).total_seconds()
assert s["calls_total"] <= 20 and rows[0]["max_calls"] == 20, (s["calls_total"], rows[0].get("max_calls"))
assert [c["case_id"] for c in d["cases"]] == json.load(open("live/cases.json"))
print("backup run took", secs, "s (live limit 150 s)")
assert secs <= 150, "the backup run took too long for the live slot"
print("backup OK")
PY
```
It also checks that your copy has F1 and F2, the 20-call budget, and the 150 s live limit.

```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && git add traces/ eval/results/ && git commit -m "Day 9: backup run $RUN of the live cases (fixed guide)" && git push
```

Post "F2, F3 pushed, <hash>". **M4 goes next.**

## 5. Turn C: M4 yallappagarid (F4, F5), then Turn D: M1 agastyan (F6, F7)

Start of turn:

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -3
```

The top line must be M3's `... Day 9: backup run p04-improved-...-backup2 of the live cases (fixed guide)`. If it isn't, the previous member hasn't pushed yet: wait.

```bash
git status --short
```

This must print nothing.

#### F4 · improved run with the fixed guide, round 1 (your key)

```bash
python3 -m harness.agent --variant improved --tag v2
```

```bash
git status --short
```

Only the new files in `traces/` and `eval/results/` may be listed.

**Check**, paste it on its own; it must end with `run OK`:

```bash
python3 - <<'PY'
import glob, json, os, subprocess
CASES, TAG = 12, "v2"
user = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
assert user in ("agastyan", "paritoshl", "varunr", "yallappagarid"), "git config user.name is " + repr(user)
g09 = [s for s in json.load(open("data/guide.json")) if s["id"] == "G09"][0]
assert g09["title"].startswith("list_transactions needs a limit"), "data/guide.json is the old guide: pull F1 first"
assert "no_new_sections" in open("harness/tools.py").read(), "harness/tools.py is the old version: pull F2 first"
f = max(glob.glob(f"eval/results/p04-improved-*-{TAG}.json"), key=os.path.getmtime)
d = json.load(open(f))
assert d["member"] == user, (d["member"], user)
assert d["summary"]["cases"] == CASES, d["summary"]
rows = [json.loads(line) for line in open(d["trace"])]
errs = [r for r in rows if r["type"] == "error"]
for r in errs:
    print("ERROR ROW:", r["case_id"], "step", r["step"], r["error"])
steps = [r for r in rows if r["type"] == "step"]
assert steps and all(r.get("response_id") for r in steps), "a step row has no response_id"
for c in d["cases"]:
    notes = sum(1 for r in steps if r["case_id"] == c["case_id"] and "no_new_sections" in (r.get("observation") or ""))
    print(f"  {c['case_id']}: migrated={c['fully_migrated']} stop={c['stop_reason']} calls={c['calls']} "
          f"tokens={c['tokens']} retrieved={','.join(c['retrieved_ids']) or '-'} repeat_notes={notes} "
          f"denied={','.join(c['gate_denied_paths']) or '-'}")
peak = max(r["prompt_tokens"] for r in steps)
assert peak + 2000 <= 16384, f"prompt {peak} + 2000 reply tokens is over the 16,384 context"
changed = subprocess.run(["git", "status", "--short", "data", "eval/cases", "eval/hand_migrations", "harness", "safety", "live"],
                         capture_output=True, text=True).stdout
assert not changed.strip(), "files outside traces/ and eval/results/ changed:\n" + changed
assert not errs, "model errors in this run: delete its two files and run it again (playbook: If something goes wrong)"
s = d["summary"]
print(d["run_id"], d["member"], "fully migrated", s["fully_migrated"], "/", s["cases"], "calls", s["calls_total"],
      "tokens", s["tokens_total"], "hit_rate", s["retrieval_hit_rate"], "peak prompt", peak)
print("run OK")
PY
```
One line per case. `repeat_notes=1` means the new note stopped a repeated search. `migrated=False` is a real result: commit it anyway and don't rerun for a better number.

```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && git add traces/ eval/results/ && git commit -m "Day 9: improved run $RUN on 12 cases (fixed guide, round 1)" && git push
```

#### F5 · compare with baseline round 1

This pairs baseline round 1 (`p04-baseline-20261111T140941Z`) with the first `-v2` run, and writes
`eval/results/compare-...-vs-...-v2.md`:

```bash
python3 - <<'PY'
import glob, json, sys
sys.path.insert(0, "eval")
import compare
ROUND = 1
base = [f for f in sorted(glob.glob("eval/results/p04-baseline-*Z.json")) if json.load(open(f))["summary"]["cases"] == 12]
fixed = [f for f in sorted(glob.glob("eval/results/p04-improved-*-v2.json")) if json.load(open(f))["summary"]["cases"] == 12]
assert len(base) >= ROUND and len(fixed) >= ROUND, (base, fixed)
compare.main([base[ROUND - 1], fixed[ROUND - 1]])
PY
```

**Check**, paste it on its own; it must end with `compare OK`:

```bash
python3 - <<'PY'
import glob, json, os
ROUND = 1
base = [f for f in sorted(glob.glob("eval/results/p04-baseline-*Z.json")) if json.load(open(f))["summary"]["cases"] == 12]
fixed = [f for f in sorted(glob.glob("eval/results/p04-improved-*-v2.json")) if json.load(open(f))["summary"]["cases"] == 12]
b, i = os.path.basename(base[ROUND - 1])[:-5], os.path.basename(fixed[ROUND - 1])[:-5]
f = f"eval/results/compare-{b}-vs-{i}.md"
text = open(f).read()
table = text[text.index("## Case by case"):text.index("## Regressions")]
assert table.count("| case_") == 12, table.count("| case_")
print(f)
for line in text.splitlines():
    if line.startswith(("| Files fully migrated", "| Tokens per file", "| Retrieval hit rate", "Fixed by the guide", "- case_", "None:")):
        print(" ", line)
print("compare OK")
PY
```


```bash
git add eval/results && git commit -m "Day 9: compare baseline round 1 vs fixed improved round 1" && git push
```

Post "F4, F5 pushed, <hash>". **M1 goes next** (Turn D).

**Turn D, M1 agastyan.** Start of turn:

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -3
```

The top line must be M4's `... Day 9: compare baseline round 1 vs fixed improved round 1`. If it isn't, the previous member hasn't pushed yet: wait.

```bash
git status --short
```

This must print nothing.

#### F6 · improved run with the fixed guide, round 2 (your key)

```bash
python3 -m harness.agent --variant improved --tag v2
```

```bash
git status --short
```

**Check**, paste it on its own; it must end with `run OK`:

```bash
python3 - <<'PY'
import glob, json, os, subprocess
CASES, TAG = 12, "v2"
user = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
assert user in ("agastyan", "paritoshl", "varunr", "yallappagarid"), "git config user.name is " + repr(user)
g09 = [s for s in json.load(open("data/guide.json")) if s["id"] == "G09"][0]
assert g09["title"].startswith("list_transactions needs a limit"), "data/guide.json is the old guide: pull F1 first"
assert "no_new_sections" in open("harness/tools.py").read(), "harness/tools.py is the old version: pull F2 first"
f = max(glob.glob(f"eval/results/p04-improved-*-{TAG}.json"), key=os.path.getmtime)
d = json.load(open(f))
assert d["member"] == user, (d["member"], user)
assert d["summary"]["cases"] == CASES, d["summary"]
rows = [json.loads(line) for line in open(d["trace"])]
errs = [r for r in rows if r["type"] == "error"]
for r in errs:
    print("ERROR ROW:", r["case_id"], "step", r["step"], r["error"])
steps = [r for r in rows if r["type"] == "step"]
assert steps and all(r.get("response_id") for r in steps), "a step row has no response_id"
for c in d["cases"]:
    notes = sum(1 for r in steps if r["case_id"] == c["case_id"] and "no_new_sections" in (r.get("observation") or ""))
    print(f"  {c['case_id']}: migrated={c['fully_migrated']} stop={c['stop_reason']} calls={c['calls']} "
          f"tokens={c['tokens']} retrieved={','.join(c['retrieved_ids']) or '-'} repeat_notes={notes} "
          f"denied={','.join(c['gate_denied_paths']) or '-'}")
peak = max(r["prompt_tokens"] for r in steps)
assert peak + 2000 <= 16384, f"prompt {peak} + 2000 reply tokens is over the 16,384 context"
changed = subprocess.run(["git", "status", "--short", "data", "eval/cases", "eval/hand_migrations", "harness", "safety", "live"],
                         capture_output=True, text=True).stdout
assert not changed.strip(), "files outside traces/ and eval/results/ changed:\n" + changed
assert not errs, "model errors in this run: delete its two files and run it again (playbook: If something goes wrong)"
s = d["summary"]
print(d["run_id"], d["member"], "fully migrated", s["fully_migrated"], "/", s["cases"], "calls", s["calls_total"],
      "tokens", s["tokens_total"], "hit_rate", s["retrieval_hit_rate"], "peak prompt", peak)
print("run OK")
PY
```


```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && git add traces/ eval/results/ && git commit -m "Day 10: improved run $RUN on 12 cases (fixed guide, round 2)" && git push
```

#### F7 · compare with baseline round 2

```bash
python3 - <<'PY'
import glob, json, sys
sys.path.insert(0, "eval")
import compare
ROUND = 2
base = [f for f in sorted(glob.glob("eval/results/p04-baseline-*Z.json")) if json.load(open(f))["summary"]["cases"] == 12]
fixed = [f for f in sorted(glob.glob("eval/results/p04-improved-*-v2.json")) if json.load(open(f))["summary"]["cases"] == 12]
assert len(base) >= ROUND and len(fixed) >= ROUND, (base, fixed)
compare.main([base[ROUND - 1], fixed[ROUND - 1]])
PY
```

**Check**, paste it on its own; it must end with `compare OK`:

```bash
python3 - <<'PY'
import glob, json, os
ROUND = 2
base = [f for f in sorted(glob.glob("eval/results/p04-baseline-*Z.json")) if json.load(open(f))["summary"]["cases"] == 12]
fixed = [f for f in sorted(glob.glob("eval/results/p04-improved-*-v2.json")) if json.load(open(f))["summary"]["cases"] == 12]
b, i = os.path.basename(base[ROUND - 1])[:-5], os.path.basename(fixed[ROUND - 1])[:-5]
f = f"eval/results/compare-{b}-vs-{i}.md"
text = open(f).read()
table = text[text.index("## Case by case"):text.index("## Regressions")]
assert table.count("| case_") == 12, table.count("| case_")
print(f)
for line in text.splitlines():
    if line.startswith(("| Files fully migrated", "| Tokens per file", "| Retrieval hit rate", "Fixed by the guide", "- case_", "None:")):
        print(" ", line)
print("compare OK")
PY
```


```bash
git add eval/results && git commit -m "Day 10: compare baseline round 2 vs fixed improved round 2" && git push
```

Post "F6, F7 pushed, <hash>". **M2 takes over** for the docs and slides.

## 6. For M2: facts for CAPSTONE.md, EVIDENCE.md and the slides

- **Results:** three sets now: baseline (rounds 1 and 2, 22/24), improved with the first guide (20/24), improved with
  the fixed guide (the two `-v2` runs). Take the numbers from the two new compare files (F5, F7), not by hand.
  Answer the question for both guides: the first guide did worse; say what the fixed one did.
- **One failure diagnosed from a trace:** case_09 is now the cleanest example. Run `p04-improved-20261111T162925Z`,
  case_09: step 3 `TypeError: list_transactions() missing ... 'limit'`; steps 4 to 8 five `search_guide` calls all
  returning G09; stop at the step limit. Cause: G09 didn't mention the removed default, and nothing stopped a repeated
  search. Fix: F1 (G09 text) and F2 (repeat note); verified (or not) in the two `-v2` runs. You can keep case_02 too:
  retrieval found G02 but Qwen still ordered the ids by their names; say what the `-v2` runs did on it.
- **Safety control:** Qwen never tried the m11 or m12 attacks in any run. The only real denied writes are the
  baseline's attempts to rewrite `data/clients/tests/test_client_02.py` (CP2 run and both baseline rounds).
- **Harness bounds:** the largest real prompt was 3,303 tokens (CP2 run, case_02), not "about 1,300".
- **Limitations:** the guide was revised after seeing results on the same 12 cases, so the `-v2` numbers are
  optimistic; G03 was never retrieved for case_08 (it passed anyway).
- **EVIDENCE.md:** Runs and Results rows for the 3 new runs (`-backup2`, two `-v2`) and the 2 new compare files.
  The part 2 C31 script can be pasted again: it only adds the rows that are missing. Change the Variant cell of the
  `-v2` runs to "improved (fixed guide)" and of `-backup2` to "backup (fixed guide, live cases case_02, case_11)" by hand.
- **Live run:** it now uses the fixed guide; the current backup is the `-backup2` run.

## 7. If something goes wrong

- **`DIFFERS FROM WHAT THE PROMPT ASKS FOR`** followed by `line N is not as asked: ...`: in the same aider session,
  paste one follow-up that names the file and line and copies the correct text from the prompt box, then run the
  check again. If it's still wrong: `/exit`, then `git checkout -- data/make_guide.py data/guide.json` (F1) or
  `git checkout -- harness/tools.py` (F2), start aider again, `/clear`, and paste the same box.
- **F1: `SyntaxError: unterminated string literal`** when running make_guide.py: Qwen turned `\n` into a real line
  break in G09's "before" or "after". Use the follow-up above for that line.
- **F1: `data/guide.json sections differ ... (did you run python3 data/make_guide.py?)`**: run
  `python3 data/make_guide.py` again, then the check.
- **`SearchReplaceNoExactMatch`**: aider retries by itself; if it still fails, use the `git checkout` line above and
  start again.
- **Runs: `ERROR ROW` / `model errors in this run`**: delete the run and run it again later:
```bash
RUN=$(basename "$(ls -t eval/results/p04-*.json | head -1)" .json) && rm "traces/$RUN.jsonl" "eval/results/$RUN.json" && git status --short
```

- **`data/guide.json is the old guide: pull F1 first`** or **`harness/tools.py is the old version`**: you ran before
  pulling. Delete the run (command above), `git pull --rebase --autostash`, and run again.

## 8. Reference: the exact changes

**F1, `data/make_guide.py`** (the rest of the file is unchanged):

````diff
--- a/data/make_guide.py
+++ b/data/make_guide.py
@@ -10,10 +10,10 @@
     },
     {
         "id": "G02",
-        "title": "Order of arguments in transfer changed",
-        "text": "The order of arguments in the `transfer` function was changed from `amount, from_id, to_id` to `from_id, to_id, amount`.",
-        "before": "transfer(amount, from_id, to_id)",
-        "after": "transfer(from_id, to_id, amount)"
+        "title": "Order of arguments in transfer changed: the amount moves to the end",
+        "text": "In v2 the amount is the last argument of `transfer`: v1 `transfer(amount, from_id, to_id)` becomes v2 `transfer(from_id, to_id, amount)`. Only the amount moves. The two account ids keep their order, so the money still goes from the same account to the same account. Do not swap the ids because of what their variable names suggest.",
+        "before": "transfer(25.0, acc_a, acc_b)  # acc_a pays acc_b 25.0",
+        "after": "transfer(acc_a, acc_b, 25.0)  # still acc_a pays acc_b"
     },
     {
         "id": "G03",
@@ -59,10 +59,10 @@
     },
     {
         "id": "G09",
-        "title": "list_transactions returns Transaction objects",
-        "text": "The `list_transactions` function now returns a list of `Transaction` objects instead of dictionaries.",
-        "before": "transactions = list_transactions(acc, 10)",
-        "after": "transactions = list_transactions(acc, 10)"
+        "title": "list_transactions needs a limit and returns Transaction objects",
+        "text": "In v2 `limit` has no default any more, so pass it explicitly. v1 used 10 when it was left out, so `list_transactions(acc)` becomes `list_transactions(acc, 10)`. The items are `Transaction` objects instead of dictionaries: read `tx.amount` and `tx.tx_id` instead of `tx['amount']` and `tx['id']`.",
+        "before": "recent = list_transactions(acc)\nfirst_id = recent[0]['id']",
+        "after": "recent = list_transactions(acc, 10)\nfirst_id = recent[0].tx_id"
     },
     {
         "id": "G10",
````

**F2, `harness/tools.py`** (the rest of the file is unchanged):

````diff
--- a/harness/tools.py
+++ b/harness/tools.py
@@ -39,7 +39,13 @@
 def search_guide(ctx, query, k=3):
     hits = retrieve(query, ctx.guide, k=k, expand=ctx.expand)
     ids = [s["id"] for s in hits]
+    seen_all = bool(ids) and all(i in ctx.retrieved_ids for i in ids)
     ctx.retrieved_ids.extend(ids)
+    if seen_all:
+        # Nothing new: repeating the same sections only fills the context (case_09 searched 5 times in a row).
+        return {"no_new_sections": ids,
+                "note": "search_guide already returned these sections in this file; the guide has nothing more on "
+                        "this. Fix the client from the test error and the v2 signatures instead of searching again."}
     return [{"id": s["id"], "title": s["title"],
              "text": (s["text"] + "\nBEFORE:\n" + s["before"] + "\nAFTER:\n" + s["after"])[:MAX_TEXT + 200]}
             for s in hits]
````

**New G02 and G09 in `data/guide.json`** (what search_guide returns):

````json
[
    {
        "id": "G02",
        "title": "Order of arguments in transfer changed: the amount moves to the end",
        "text": "In v2 the amount is the last argument of `transfer`: v1 `transfer(amount, from_id, to_id)` becomes v2 `transfer(from_id, to_id, amount)`. Only the amount moves. The two account ids keep their order, so the money still goes from the same account to the same account. Do not swap the ids because of what their variable names suggest.",
        "before": "transfer(25.0, acc_a, acc_b)  # acc_a pays acc_b 25.0",
        "after": "transfer(acc_a, acc_b, 25.0)  # still acc_a pays acc_b"
    },
    {
        "id": "G09",
        "title": "list_transactions needs a limit and returns Transaction objects",
        "text": "In v2 `limit` has no default any more, so pass it explicitly. v1 used 10 when it was left out, so `list_transactions(acc)` becomes `list_transactions(acc, 10)`. The items are `Transaction` objects instead of dictionaries: read `tx.amount` and `tx.tx_id` instead of `tx['amount']` and `tx['id']`.",
        "before": "recent = list_transactions(acc)\nfirst_id = recent[0]['id']",
        "after": "recent = list_transactions(acc, 10)\nfirst_id = recent[0].tx_id"
    }
]
````
