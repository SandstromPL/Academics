# P04 / g15: fresh backup run, recount, then the freeze (M2 paritoshl, 15 Nov 2026)

Why: the launch deck says "Commit one backup run in the 48 hours before the freeze: traces/backup-<run_id>.jsonl".
backup2 started at 13 Nov 23:57:51 IST (about a minute before that window opened) and its file name has no
`backup-` prefix. This records a new backup in the window, under the right name, and redoes the counts after it.

Do every step in your own workspace (`~/capstone-g15`, git user `paritoshl`, your own key). Push after each commit.
Tested on a copy of the repo with a fake run (no gateway calls).

## 0 · Start clean

```bash
cd ~/capstone-g15 && git pull && git status --short && git log -1 --format='%h %an %s'
```

`git status` must print nothing, and the last commit must be `95c6dafd6d paritoshl Day 10: CAPSTONE.md contributions, EVIDENCE.md members table`.

## 1 · The backup run (about 15 s, about 6 calls)

```bash
bash live/run_live.sh backup3
```

It prints the run ID, `traces/<run_id>.jsonl` and `eval/results/<run_id>.json`.

## 2 · Rename the trace, add the EVIDENCE rows

It checks the run (inside the 48 hours, every call has a response_id, at most 20 calls, both cases migrated),
renames the trace to `traces/backup-<run_id>.jsonl`, fixes the `trace` field in the result file, adds the Runs and
Results rows to EVIDENCE.md and one line in README.md. If it says not every case migrated, run the `rm` line it
prints and do step 1 again.

Paste it on its own; it must end with `backup files OK`, then run the `git add ... && git push` line it prints:

```bash
python3 - <<'PY'
import glob, json, os, subprocess
from datetime import datetime
res = sorted(glob.glob("eval/results/p04-improved-*-backup3.json"))
if len(res) != 1:
    raise SystemExit(f"expected exactly one backup3 result file, found {res}")
p = res[0]
d = json.load(open(p))
rid, s = d["run_id"], d["summary"]
old, new = f"traces/{rid}.jsonl", f"traces/backup-{rid}.jsonl"
if d["trace"] != old or not os.path.isfile(old):
    raise SystemExit(f"trace file {old} not found")
me = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
secs = round((datetime.fromisoformat(d["ended_utc"].replace("Z", "+00:00"))
             - datetime.fromisoformat(d["started_utc"].replace("Z", "+00:00"))).total_seconds())
print(f"run {rid} by {d['member']}, {d['started_utc']} to {d['ended_utc']} ({secs} s)")
print(f"fully migrated {s['fully_migrated']}/{s['cases']}, calls {s['calls_total']}")
if d["member"] != me:
    raise SystemExit(f"the run says member {d['member']} but git user.name is {me}")
if not "2026-11-13T18:29:00Z" <= d["started_utc"] <= "2026-11-15T18:29:00Z":
    raise SystemExit("the run did not start inside the 48 hours before the freeze")
rows = [json.loads(line) for line in open(old)]
steps = [r for r in rows if r["type"] == "step"]
if not steps or not all(r.get("response_id") for r in steps) or len(steps) != s["calls_total"] or len(steps) > 20:
    raise SystemExit("the trace's step rows do not match the result (or a step has no response_id)")
if s["fully_migrated"] != s["cases"]:
    raise SystemExit(f"not every case migrated. Delete the two new files and run the backup again:\n  rm {old} {p}")
os.rename(old, new)
d["trace"] = new
with open(p, "w") as f:
    json.dump(d, f, indent=2)
cases = ", ".join(c["case_id"] for c in d["cases"])
label = f"backup for the presentation (improved, fixed guide, live cases {cases})"
ev = open("EVIDENCE.md").read()
if rid in ev:
    raise SystemExit("this run is already in EVIDENCE.md")
lines = ev.split("\n")
i = max(k for k, line in enumerate(lines) if line.startswith("| p04-"))
lines.insert(i + 1, f"| {rid} | {label} | {d['started_utc']} | {d['ended_utc']} | {d['model']} | {s['calls_total']} | {new} | {p} |")
i = max(k for k, line in enumerate(lines) if line.startswith("| eval/results/p04-"))
lines.insert(i + 1, f"| {p} | {label}: fully migrated {s['fully_migrated']}/{s['cases']}, calls {s['calls_total']} "
                    f"({s['calls_per_file']}/file), tokens {s['tokens_total']} ({s['tokens_per_file']}/file), "
                    f"retrieval hit rate {s['retrieval_hit_rate']} |")
open("EVIDENCE.md", "w").write("\n".join(lines))
files = [new, p, "EVIDENCE.md"]
rd = open("README.md").read()
a = "<run_id>.jsonl, one per run, incl. the backup run"
if a in rd:
    open("README.md", "w").write(rd.replace(a, "<run_id>.jsonl, one per run; the presentation backup is backup-<run_id>.jsonl", 1))
    files.append("README.md")
ev = open("EVIDENCE.md").read()
assert ev.count(rid) == 4 and json.load(open(p))["trace"] == new and os.path.isfile(new) and not os.path.exists(old)
print(f"FOR THE SLIDES: {rid} | {s['fully_migrated']}/{s['cases']} migrated, {s['calls_total']} calls, {secs} s")
print("Now commit and push it:\n")
print(f'git add {" ".join(files)} && git commit -m "Day 10: backup run {rid} of the live cases (fixed guide), '
      f'saved as traces/backup-{rid}.jsonl" && git push')
print("\nbackup files OK")
PY
```

## 3 · Recount the Members table and Contributions

D4 counted up to D3. This redoes the counts up to the backup commit (your commits and calls change), adds "the backup
run for the presentation" to your line in Contributions and updates the "Our gap" note. It keeps any edits you made
to the "what they built" sentences.

Paste it on its own; it must end with `recount OK`, then run the `git add ... && git push` line it prints:

```bash
python3 - <<'PY'
import glob, json, re, subprocess
def git(*a):
    return subprocess.check_output(["git", *a], text=True).strip()
if "backup run" not in git("log", "-1", "--format=%s"):
    raise SystemExit("HEAD should be the backup run commit; commit and push it first")
cap = open("CAPSTONE.md").read()
ev = open("EVIDENCE.md").read()
slots = re.findall(r"^(M[1-4])\s+(\S+), roll number: (\d+)", cap, re.M)
assert len(slots) == 4, slots
users = {u: (m, roll) for m, u, roll in slots}
head = git("rev-parse", "--short=12", "HEAD")
log = [line.split("\t", 3) for line in git("log", "--format=%h%x09%an%x09%ae%x09%s").splitlines()]
commits = {u: [] for u in users}
for h, name, email, subj in log:
    for u in users:
        if name == u or email.split("@")[0] == u:
            commits[u].append((h, subj))
            break
calls = {u: [] for u in users}
for f in sorted(glob.glob("traces/*.jsonl")):
    rows = [json.loads(line) for line in open(f)]
    member = next((r.get("member") for r in rows if r["type"] == "run_start"), None)
    if member in calls:
        calls[member] += [r["ts"] for r in rows if r["type"] == "step"]
bk = glob.glob("traces/backup-*.jsonl")
assert len(bk) == 1, bk
runner = next(json.loads(line)["member"] for line in open(bk[0]))
for u, (m, roll) in users.items():
    ts = sorted(calls[u])
    row = f"| {m} | {roll} | {u} | {len(commits[u])} | {len(ts)} | {ts[0] if ts else '-'} | {ts[-1] if ts else '-'} |"
    ev, n = re.subn(rf"^\| {m} \| {roll} \| {re.escape(u)} \|.*\|$", lambda _: row, ev, flags=re.M)
    if n != 1:
        raise SystemExit(f"Members row {m} not found in EVIDENCE.md")
    print(row)
ev, n = re.subn(r"Commits are counted up to `[0-9a-f]+`; the two commits after it only fill in these tables",
                lambda _: f"Commits are counted up to `{head}`; the two commits after it only update these tables", ev)
if n != 1:
    raise SystemExit("the 'Our gap' note in EVIDENCE.md was not found")
cap, n = re.subn(r"(Commits on main by Gitea user, from `git log` up to )`[0-9a-f]+`",
                 lambda mo: mo.group(1) + f"`{head}`", cap)
if n != 1:
    raise SystemExit("the Contributions header in CAPSTONE.md was not found")
for u, (m, roll) in users.items():
    lst = ", ".join(f"`{h}` {subj}" for h, subj in reversed(commits[u]))
    def fix(mo):
        built = mo.group(1)
        if u == runner and "backup run for the presentation" not in built:
            built = built[:-2] + "; the backup run for the presentation. "
        return built + f"{len(commits[u])} commits: {lst}."
    pat = rf"^(- \*\*{m} {re.escape(u)}\*\* \(roll number {roll}\): .*?\. )\d+ commits: .*$"
    cap, n = re.subn(pat, fix, cap, flags=re.M)
    if n != 1:
        raise SystemExit(f"Contributions line for {m} not found in CAPSTONE.md")
open("CAPSTONE.md", "w").write(cap)
open("EVIDENCE.md", "w").write(ev)
cap, ev = open("CAPSTONE.md").read(), open("EVIDENCE.md").read()
for u, (m, roll) in users.items():
    assert f"| {m} | {roll} | {u} | {len(commits[u])} |" in ev
    assert re.search(rf"^- \*\*{m} {re.escape(u)}\*\* .*\. {len(commits[u])} commits: ", cap, re.M)
assert f"counted up to `{head}`" in ev and f"up to `{head}` (short hashes)" in cap
print(f"\nCounted up to {head}. Now commit and push it:\n")
print('git add CAPSTONE.md EVIDENCE.md && git commit -m "Day 10: CAPSTONE.md contributions and EVIDENCE.md members '
      'table recounted after the backup run" && git push')
print("\nrecount OK")
PY
```

## 4 · Send Claude the numbers for the slides

```bash
git rev-parse --short=12 HEAD && grep "^| M[1-4] |" EVIDENCE.md && grep -o "counted up to \`[0-9a-f]*\`" EVIDENCE.md && ls traces/backup-*
```

Paste that output, plus the `FOR THE SLIDES:` line from step 2. Claude rebuilds slides.pdf with the new freeze HEAD
(the step 3 commit), the new M2 row, and the new backup on slides 4 and 5.

## 5 · Freeze (last commit)

1. Put the new `slides.pdf` in the repo root (`~/capstone-g15/slides.pdf`).
2. Run the slides check (section S of `P04_g15_final_docs.md`), then D5 and its check (section D5).
3. Commit both together:

```bash
git add slides.pdf EVIDENCE.md && git commit -m "Freeze: slides.pdf and EVIDENCE.md freeze commit" && git push
```

After this nobody pushes anything. Freeze: Sun 15 Nov 2026, 11:59 PM IST.
