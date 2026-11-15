# P04 / g15: final CAPSTONE.md, EVIDENCE.md, slides and freeze (M2 paritoshl)

Everything here is for you (M2), in your own workspace, after M1's F7. Five scripts and the slides, in this order (changed on 15 Nov: the slides go in the last commit with D5, so slide 4 can show the D4 hash):

| # | What | Files | Commit message |
|---|---|---|---|
| D1 | EVIDENCE.md Runs and Results rows for all 10 runs and 4 compare files, labelled baseline / first guide / fixed guide | EVIDENCE.md | `Day 10: EVIDENCE.md runs and results rows for all runs, with guide labels` |
| D2 | CAPSTONE.md Results (all three sets), One failure diagnosed from a trace (case_02 and case_09, both fixed), Safety control and Harness bounds corrected from the real runs | CAPSTONE.md | `Day 10: CAPSTONE.md results with the fixed guide, failure diagnosis, safety and bounds from the real runs` |
| D3 | CAPSTONE.md Limitations and Use of AI assistants | CAPSTONE.md | `Day 10: CAPSTONE.md limitations and use of AI assistants` |
| D4 | CAPSTONE.md Contributions and EVIDENCE.md Members table (counts every commit up to D3) | CAPSTONE.md, EVIDENCE.md | `Day 10: CAPSTONE.md contributions, EVIDENCE.md members table` |
| S + D5 | slides.pdf (its freeze HEAD is the D4 hash) and the freeze row, in one last commit | slides.pdf, EVIDENCE.md | `Freeze: slides.pdf and EVIDENCE.md freeze commit` |

Every number the scripts write comes from the result files and traces; nothing is typed by hand. D2 also checks
every claim about case_02 and case_09 against the traces before it writes anything. All five ran in this order on a
copy of main (`4936dbd75ce3`), each check printed its OK line, and the working tree was clean at the end.

`P04_g15_preview_CAPSTONE.md` and `P04_g15_preview_EVIDENCE.md` next to this file show what CAPSTONE.md and EVIDENCE.md
look like after D1 to D3 (the real data). Use them for the slides; the Members table and Contributions only appear
after D4, in the real repo.

Freeze: **Sun 15 Nov 2026, 11:59 PM IST**. Aim to push D5 a few hours before.

## Start

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -3
```

The top line must be M1's `Day 10: compare baseline round 2 vs fixed improved round 2`.

```bash
git status --short
```

This must print nothing.

### D1 · EVIDENCE.md Runs and Results rows

It rebuilds the rows of the Runs and Results tables from all result files, oldest first, and labels each run: baseline, Checkpoint 2, improved (first guide), improved (fixed guide), and the two backups. The Results rows use `headline()` from compare.py, so slide 6 can copy them exactly.

Paste it on its own; it must end with `EVIDENCE.md updated: 10 runs, 13 results rows`:

```bash
python3 - <<'PY'
import glob, json, re, sys
sys.path.insert(0, "eval")
from compare import headline
p = "EVIDENCE.md"
s = open(p).read()
def label(d):
    rid, n = d["run_id"], d["summary"]["cases"]
    live = ", ".join(c["case_id"] for c in d["cases"])
    if rid.endswith("-backup2"):
        return "backup (improved, fixed guide, live cases " + live + ")"
    if rid.endswith("-backup"):
        return "backup (improved, first guide, live cases " + live + ")"
    if rid.endswith("-v2"):
        return "improved (fixed guide)"
    if d["variant"] == "improved":
        return "improved (first guide)"
    if n == 1:
        return "baseline (smoke, " + d["cases"][0]["case_id"] + ")"
    if n < 12:
        return f"baseline (Checkpoint 2, {n} cases)"
    return "baseline"
runs = sorted(({**json.load(open(f)), "_file": f} for f in glob.glob("eval/results/p04-*.json")), key=lambda d: d["started_utc"])
run_rows = "".join(f"| {d['run_id']} | {label(d)} | {d['started_utc']} | {d['ended_utc']} | {d['model']} | "
                   f"{d['summary']['calls_total']} | {d['trace']} | {d['_file']} |\n" for d in runs)
res_rows = "".join(f"| {d['_file']} | {label(d)}: {headline(d)} |\n" for d in runs if d["summary"]["cases"] > 1)
by_id = {d["run_id"]: d for d in runs}
for f in sorted(glob.glob("eval/results/compare-*.md")):
    m = re.fullmatch(r"eval/results/compare-(p04-baseline-\d{8}T\d{6}Z)-vs-(p04-improved-[\w-]+)\.md", f)
    b, i = by_id[m.group(1)]["summary"], by_id[m.group(2)]
    res_rows += (f"| {f} | baseline vs {label(i)}: {b['fully_migrated']}/{b['cases']} vs {i['summary']['fully_migrated']}/"
                 f"{i['summary']['cases']} fully migrated; tokens per file {b['tokens_per_file']} vs "
                 f"{i['summary']['tokens_per_file']}; hit rate {i['summary']['retrieval_hit_rate']} |\n")
runs_head = "|---|---|---|---|---|---|---|---|\n"
a = s.index(runs_head, s.index("## Runs")) + len(runs_head)
b = s.index("\n## Results")
s = s[:a] + run_rows + s[b:]
res_head = "| Result file | Headline numbers (exactly as on slide 6) |\n|---|---|\n"
a = s.index(res_head) + len(res_head)
b = a
while s.startswith("| ", b):
    b = s.index("\n", b) + 1
s = s[:a] + res_rows + s[b:]
open(p, "w").write(s)
print(run_rows)
print(res_rows)
print("EVIDENCE.md updated:", len(runs), "runs,", res_rows.count("\n"), "results rows")
PY
```

**Check**, paste it on its own; it must end with `evidence rows OK`:

```bash
python3 - <<'PY'
import glob
ev = open("EVIDENCE.md").read()
runs = ev[ev.index("## Runs"):ev.index("## Results")]
res = ev[ev.index("## Results"):]
for f in glob.glob("eval/results/p04-*.json"):
    assert runs.count(f) == 1, "Runs row for " + f
for f in glob.glob("eval/results/compare-*.md"):
    assert res.count(f) == 1, "Results row for " + f
assert runs.count("improved (fixed guide)") == 2 and runs.count("improved (first guide)") == 2, "Variant labels"
assert "fixed guide, live cases" in runs and "first guide, live cases" in runs, "backup labels"
assert res.count("| eval/results/") == len(glob.glob("eval/results/p04-*.json")) - 1 + len(glob.glob("eval/results/compare-*.md"))
print("evidence rows OK")
PY
```

```bash
git add EVIDENCE.md && git commit -m "Day 10: EVIDENCE.md runs and results rows for all runs, with guide labels" && git push
```


### D2 · CAPSTONE.md Results, One failure, Safety control, Harness bounds

It replaces the Results section with all three sets (B1/B2 baseline, I1/I2 first guide, V1/V2 fixed guide): a table per run, a case-by-case table with the calls used, regressions and fixes against the baseline, a summary table, and the answer to the project question for both guides, including the warning that the fixed-guide numbers are optimistic. It rewrites One failure diagnosed from a trace: case_02 (cause, the first fix that didn't work, the G02 rewrite, verified) and case_09 (the search loop, the G09 rewrite, verified). In Safety control it states the real denied writes and that Qwen never tried the m11/m12 writes; in Harness bounds the real largest prompt (3,303 tokens). It prints everything it writes.

Paste it on its own; it must end with `CAPSTONE.md updated`:

```bash
python3 - <<'PY'
import glob, json, re
p = "CAPSTONE.md"
s = open(p).read()
runs = [json.load(open(f)) for f in sorted(glob.glob("eval/results/p04-*.json"))]
main = sorted((d for d in runs if d["summary"]["cases"] == 12), key=lambda d: d["started_utc"])
B = [d for d in main if d["variant"] == "baseline"]
I = [d for d in main if d["variant"] == "improved" and not d["run_id"].endswith("-v2")]
V = [d for d in main if d["run_id"].endswith("-v2")]
assert len(B) == 2 and len(I) == 2 and len(V) == 2, (len(B), len(I), len(V))
SETS = [("B", "baseline", B), ("I", "improved, first guide", I), ("V", "improved, fixed guide", V)]
cases = {d["run_id"]: {c["case_id"]: c for c in d["cases"]} for d in main}
ids = sorted(cases[B[0]["run_id"]])
def trace(d):
    return [json.loads(line) for line in open(d["trace"])]
def tot(group):
    n = 12 * len(group)
    return (sum(d["summary"]["fully_migrated"] for d in group), n,
            sum(d["summary"]["tokens_total"] for d in group) / n, sum(d["summary"]["calls_total"] for d in group) / n)
mb, n, tb, cb = tot(B)
mi, _, ti, ci = tot(I)
mv, _, tv, cv = tot(V)
pct = lambda x: f"{(x - tb) / tb * 100:+.1f}%"
# ---- Results ----
out = ["Runs on all 12 cases with the gateway model `main` (temperature 0), the same harness and the same bounds.",
       "B = baseline, I = improved with the first guide, V = improved after the guide fix (commits F1 and F2, runs tagged `-v2`).", "",
       "| Run | Set | By | Fully migrated | Tests green | Calls (per file) | Tokens (per file) | Hit rate |",
       "|---|---|---|---|---|---|---|---|"]
for tag, name, group in SETS:
    for k, d in enumerate(group, 1):
        t = d["summary"]
        hr = t["retrieval_hit_rate"] if t["retrieval_hit_rate"] is not None else "n/a"
        out.append(f"| `{d['run_id']}` | {tag}{k}, {name} | {d['member']} | {t['fully_migrated']}/12 | {t['tests_green']}/12 | "
                   f"{t['calls_total']} ({t['calls_per_file']}) | {t['tokens_total']} ({t['tokens_per_file']}) | {hr} |")
out += ["", "Case by case: yes or no = fully migrated (tests green and zero v1 leftovers), with the model calls used.", "",
        "| Case | Kind | Needed | B1 | B2 | I1 | I2 | V1 | V2 |", "|---|---|---|---|---|---|---|---|---|"]
for cid in ids:
    c0 = cases[B[0]["run_id"]][cid]
    cells = []
    for _, _, group in SETS:
        for d in group:
            c = cases[d["run_id"]][cid]
            cells.append(f"{'yes' if c['fully_migrated'] else '**no**'} ({c['calls']})")
    out.append(f"| {cid} | {c0['kind']} | {', '.join(c0['needed_sections'])} | " + " | ".join(cells) + " |")
def diff(group):
    reg, fix = {}, {}
    for k, (b, i) in enumerate(zip(B, group), 1):
        for cid in ids:
            bm, im = cases[b["run_id"]][cid]["fully_migrated"], cases[i["run_id"]][cid]["fully_migrated"]
            if bm and not im:
                reg.setdefault(cid, []).append(str(k))
            if im and not bm:
                fix.setdefault(cid, []).append(str(k))
    fmt = lambda d: "; ".join(f"{c} (round{'s' if len(ks) > 1 else ''} {', '.join(ks)})" for c, ks in sorted(d.items())) or "none"
    return fmt(reg), fmt(fix)
def same_rounds(group):
    return all(cases[group[0]["run_id"]][c]["fully_migrated"] == cases[group[1]["run_id"]][c]["fully_migrated"] for c in ids)
ri, fi = diff(I)
rv, fv = diff(V)
notes = sum("no_new_sections" in (r.get("observation") or "") for d in V for r in trace(d) if r["type"] == "step")
vmax = max(c["calls"] for d in V for c in cases[d["run_id"]].values())
b8 = sorted({cid for d in B for cid, c in cases[d["run_id"]].items() if c["calls"] == 8})
b8txt = " and ".join(f"{cid}{' (and still failed)' if not all(cases[d['run_id']][cid]['fully_migrated'] for d in B) else ''}" for cid in b8)
cmps = sorted(glob.glob("eval/results/compare-*.md"))
out += ["",
        f"Against the baseline, same round. First guide: regressions {ri}; fixed {fi}. Fixed guide: regressions {rv}; fixed {fv}.",
        "Run to run: " + ("both runs of each set gave the same outcome on every case." if all(same_rounds(g) for _, _, g in SETS)
                          else "some cases changed outcome between the two runs of a set (see the table)."),
        "Full tables: " + ", ".join(f"`{f}`" for f in cmps) + ".", "",
        f"| Set (2 runs, 24 files) | Fully migrated | Tokens per file | Calls per file |", "|---|---|---|---|",
        f"| Baseline | {mb}/{n} | {tb:.0f} | {cb:.2f} |",
        f"| Improved, first guide | {mi}/{n} | {ti:.0f} ({pct(ti)}) | {ci:.2f} |",
        f"| Improved, fixed guide | {mv}/{n} | {tv:.0f} ({pct(tv)}) | {cv:.2f} |", "",
        f"Answer: with the guide as first written, retrieved sections did {'better than' if mi > mb else ('as well as' if mi == mb else 'worse than')} "
        f"the model's own guesses ({mi} against {mb} of {n} files, {pct(ti)} tokens per file). Two cases failed because of the "
        f"guide text, not the retrieval: search_guide returned the right section, but G02 did not say that the two ids keep "
        f"their order and G09 did not say that the limit lost its default (see One failure diagnosed from a trace). After "
        f"rewriting G02 and G09 (F1) and adding a note for repeated searches (F2), the improved variant fully migrated "
        f"{mv} of {n} files at {tv:.0f} tokens per file ({pct(tv)} against the baseline): every file took at most {vmax} calls, "
        f"where the baseline used all 8 on {b8txt}. "
        + ("The repeat note never fired in the fixed-guide runs, so the gain comes from the guide text. " if notes == 0 else
           f"The repeat note fired {notes} time{'s' if notes != 1 else ''} in the fixed-guide runs. ")
        + f"The guide was rewritten after seeing these results on "
        f"the same 12 cases, so the fixed-guide numbers are optimistic (see Limitations).",
        "The Checkpoint 2 run `p04-baseline-20261109T145606Z` (6 cases) was a harness check and is not part of the comparison."]
results = "\n".join(out) + "\n\n"
# ---- One failure ----
cp2 = [json.loads(line) for line in open("traces/p04-baseline-20261109T145606Z.jsonl")]
st = {r["step"]: r for r in cp2 if r["type"] == "step" and r["case_id"] == "case_02"}
end = [r for r in cp2 if r["type"] == "case_end" and r["case_id"] == "case_02"][0]
assert [st[k]["tool"] for k in range(1, 9)] == ["write_file", "run_tests", "read_file", "write_file", "run_tests", "write_file", "run_tests", "write_file"]
assert any(r["type"] == "gate" and r["case_id"] == "case_02" and r["step"] == 4 and r["decision"] == "deny" for r in cp2)
assert "assert 240.0 == 360.0" in end["first_failure"] and "transfer(payer_id, friend_id, share)" in end["final_text"]
for d in I:
    c = cases[d["run_id"]]["case_02"]
    first = [r for r in trace(d) if r["type"] == "step" and r["case_id"] == "case_02"][0]
    assert not c["fully_migrated"] and first["tool"] == "search_guide" and "G02" in first["retrieved_ids"], d["run_id"]
i9 = [r for r in trace(I[0]) if r["type"] == "step" and r["case_id"] == "case_09"]
assert "missing 1 required positional argument: 'limit'" in i9[2]["observation"], i9[2]["observation"]
assert [r["tool"] for r in i9[3:8]] == ["search_guide"] * 5 and all(r["retrieved_ids"] == ["G09"] for r in i9[3:8])
assert cases[I[0]["run_id"]]["case_09"]["stop_reason"] == "step_limit"
assert all(cases[d["run_id"]][c]["fully_migrated"] for d in V for c in ("case_02", "case_09"))
def calls_txt(cid):
    cs = [cases[d["run_id"]][cid]["calls"] for d in V]
    return f"{cs[0]} calls in both" if len(set(cs)) == 1 else f"{cs[0]} and {cs[1]} calls in the two"
v02, v09 = calls_txt("case_02"), calls_txt("case_09")
backup2 = [json.load(open(f)) for f in glob.glob("eval/results/p04-improved-*-backup2.json")]
bk = ""
if backup2 and {c["case_id"]: c for c in backup2[0]["cases"]}.get("case_02", {}).get("fully_migrated"):
    bk = f", and in the backup run `{backup2[0]['run_id']}`"
failure = f"""Run `p04-baseline-20261109T145606Z` (baseline, Checkpoint 2), case_02 (`data/clients/client_02.py`, needs G02):
stopped at the step limit after {end['calls']} calls and {end['tokens']} tokens, tests red.
- Steps 1, 6 and 8 (`write_file`): the v1 call `transfer(share, friend_id, payer_id)` (the friend pays the payer)
  became `transfer(payer_id, friend_id, share)`, so the payer paid the friends. Steps 2, 5 and 7 (`run_tests`):
  `test_split_bill` failed with `assert 240.0 == 360.0`. `pay_rent` was migrated correctly.
- Step 3 read the test file; step 4 tried to `write_file` the test itself, and the scope gate denied it
  (`denied: client tests are read-only`).
- Cause: the baseline prompt has the v2 signature `transfer(from_id, to_id, amount)` but not the v1 one, and
  `read_file` cannot open v1.py. The model saw that the amount moved to the end and ordered the two ids by their
  meaning.
- First fix tried, the improved variant with the first guide: search_guide returned G02 at step 1 in both runs
  (`{I[0]['run_id']}`, `{I[1]['run_id']}`), and the model still wrote the same wrong call. The old G02 only
  listed the parameter names (`amount, from_id, to_id` becomes `from_id, to_id, amount`).
- Fix (commit F1): G02 rewritten to say that only the amount moves to the end and that the two ids keep their order,
  with an example (`transfer(25.0, acc_a, acc_b)` becomes `transfer(acc_a, acc_b, 25.0)`). Verified: case_02 was fully
  migrated after {v02} fixed-guide runs (`{V[0]['run_id']}`, `{V[1]['run_id']}`){bk}.

A second failure, fixed the same way: run `{I[0]['run_id']}` (improved, first guide), case_09 (needs G09). Step 3:
`TypeError: list_transactions() missing 1 required positional argument: 'limit'`. Steps 4 to 8: five `search_guide`
calls, each returning only G09, then the step limit. The baseline hit the same error and fixed it with its next write.
Cause: the old G09 never said that `limit` lost its default (its before and after were the same line), and nothing
stopped a repeated search. Fix: G09 rewritten to say that the limit must be passed (v1 used 10), with a before and
after that differ (F1), and a note when a search returns only sections already seen (F2). Verified: case_09 was fully
migrated after {v09} fixed-guide runs, without a repeated search.

"""
# ---- Safety: what the real runs show ----
denials = []
attack_tries = 0
for d in runs:
    for r in trace(d):
        if r["type"] == "gate" and r["decision"] == "deny":
            denials.append((d["run_id"], r["case_id"], r["path"], r["step"]))
            if r["case_id"] in ("case_11", "case_12"):
                attack_tries += 1
paths = sorted({x[2] for x in denials})
cases_d = sorted({x[1] for x in denials})
old_seen = """Seen in a real run: in `p04-baseline-20261109T145606Z`, case_02 step 4, the model tried to rewrite
`data/clients/tests/test_client_02.py`; the gate denied it (gate row in the trace, `gate_denied_paths` in the result).
"""
new_seen = (f"Seen in the real runs: the gate denied {len(denials)} write{'s' if len(denials) != 1 else ''}, all in "
            f"{', '.join(cases_d)}, all to {', '.join('`' + x + '`' for x in paths)}, in "
            f"{', '.join('`' + x + '`' for x in sorted({x[0] for x in denials}))} (gate rows in the traces, "
            f"`gate_denied_paths` in the results). "
            + ("Qwen never tried the m11 or m12 writes in any of our " + str(len(runs)) + " runs, so for those paths "
               "the evidence is `safety/test_scope.py`." if attack_tries == 0 else
               f"In case_11 and case_12 it tried {attack_tries} denied write(s).") + "\n")
# ---- Harness bounds: the real largest prompt ----
peak = max(((r["prompt_tokens"], d["run_id"], r["case_id"]) for d in runs for r in trace(d) if r["type"] == "step"))
old_b = "In a scripted run of all 6 cases the largest prompt was about 1,300 tokens."
new_b = f"In the real runs the largest prompt was {peak[0]:,} tokens (`{peak[1]}`, {peak[2]})."
def body(name):
    a = s.index(f"## {name}\n") + len(f"## {name}\n")
    return a, s.index("\n## ", a) + 1
for old, new in ((old_seen, new_seen), (old_b, new_b)):
    if s.count(old) != 1:
        raise SystemExit("text not found, CAPSTONE.md was changed by hand: " + old[:60])
    s = s.replace(old, new)
a, b = body("Results")
s = s[:a] + results + s[b:]
a, b = body("One failure diagnosed from a trace")
s = s[:a] + failure + s[b:]
open(p, "w").write(s)
print(results)
print(failure)
print(new_seen)
print(new_b)
print("CAPSTONE.md updated")
PY
```

**Check**, paste it on its own; it must end with `capstone results OK`:

```bash
python3 - <<'PY'
s = open("CAPSTONE.md").read()
r = s[s.index("## Results"):s.index("## One failure")]
f = s[s.index("## One failure"):s.index("## Limitations")]
assert r.count("| case_") == 12 and r.count("-v2`") >= 2 and "Answer: with the guide as first written" in r
assert "Improved, fixed guide" in r and "Improved, first guide" in r
assert "still not migrated" not in f and "First fix tried" in f and "Fix (commit F1)" in f and "case_09" in f
assert "Seen in the real runs:" in s and "about 1,300 tokens" not in s and "In the real runs the largest prompt was" in s
assert s.count("## Results") == 1 and s.count("## One failure diagnosed from a trace") == 1 and s.count("## Limitations") == 1
print("capstone results OK")
PY
```

```bash
git add CAPSTONE.md && git commit -m "Day 10: CAPSTONE.md results with the fixed guide, failure diagnosis, safety and bounds from the real runs" && git push
```


Read the new sections once: `sed -n '/^## Results/,/^## Limitations/p' CAPSTONE.md`.

### D3 · CAPSTONE.md Limitations and Use of AI assistants

Limitations: the guide was rewritten after seeing results on the same 12 cases (so the fixed-guide numbers are optimistic), the small synthetic set, keyword retrieval and what the hit rate does not show, the repeat note never fired, the m11/m12 writes were never tried, what the tests and the v1 check can and cannot catch, the unsandboxed test run, the run budget, token counts. Use of AI assistants: what aider wrote, how each output was checked, and one line on what Claude was used for.

Paste it on its own; it must end with `CAPSTONE.md updated`:

```bash
python3 - <<'PY'
p = "CAPSTONE.md"
s = open(p).read()
limits = """- The guide was rewritten (G02, G09) after we saw the results on the same 12 cases, so the fixed-guide numbers are
  optimistic: the fix was shaped by these cases. A fair test of the fixed guide needs clients it has not seen.
- Small, synthetic set: one small payments library and 12 clients that we wrote ourselves. Both runs of each set
  gave the same outcome on every case (temperature 0), so the second run shows the result repeats, not that it holds
  on other code.
- One model (`main`) and keyword retrieval only (IDF-weighted overlap, k at most 3): no embeddings, no reranking.
  The hit rate counts section ids that search_guide returned, not whether the model used them: case_02 failed with
  the right section retrieved, and case_08 passed although G03 was never retrieved.
- The repeat-search note (F2) never fired in the fixed-guide runs, so it is tested only by our scripted check, not by
  Qwen.
- Qwen never tried the m11 or m12 writes, so for those paths the scope gate is tested only by `safety/test_scope.py`.
  The only denied writes in real runs are the baseline's attempts to rewrite the case_02 test file.
- The tests define "migrated". The v1 check flags libv.v1 imports and v1-only names only; a changed function that
  kept its name (charge, convert, format_amount, list_transactions, open_account) is caught only if a test calls it.
- The baseline sees the v2 signatures, so the renames (G01, G05, G06, G12) are easy for both variants; the guide can
  only help where a change is not visible in a signature.
- run_tests imports the client that the model wrote, so that code runs in our workspace during pytest (30 s timeout,
  no sandbox).
- The run budget is checked before each model call, so one slow call (60 s timeout, 2 retries) can overrun
  `--max-seconds`.
- Token counts are the gateway's usage numbers. The aider calls we made while writing the code are not in traces/.
"""
ai = """- aider 0.86.1 with the gateway model `main` wrote the code and data files from our prompts, with
  `--no-auto-commits`: every commit was made by hand, by the member who ran aider, after the checks below.
- Every aider output was checked by plain code before its commit: the unit tests (data/libv/tests, harness, safety),
  `python3 eval/check_hand.py` (every base client fails, every hand migration passes), and a check script per commit
  that runs the new code with a scripted fake model and makes no gateway call.
- The agent's own model calls (`main`) are in traces/, one step row per call with the gateway response id.
- Claude (Anthropic) was used outside the course workspace to plan the work and draft the aider prompts, the check scripts and the scripts that fill in this report.
"""
old_l = "## Limitations\n\n## Contributions"
old_a = "What aider or the gateway models wrote, and how it was checked.\n"
for old in (old_l, old_a):
    if old not in s:
        raise SystemExit("placeholder not found, edit CAPSTONE.md by hand: " + old.splitlines()[0])
s = s.replace(old_l, "## Limitations\n" + limits + "\n## Contributions", 1).replace(old_a, ai, 1)
open(p, "w").write(s)
print("CAPSTONE.md updated")
PY
```

**Check**, paste it on its own; it must end with `capstone limitations OK`:

```bash
python3 - <<'PY'
s = open("CAPSTONE.md").read()
lim = s[s.index("## Limitations"):s.index("## Contributions")]
ai = s[s.index("## Use of AI assistants"):]
assert lim.count("\n- ") >= 8 and "fixed-guide numbers are" in lim
assert "What aider or the gateway models wrote" not in ai and "aider 0.86.1" in ai
print("capstone limitations OK")
PY
```

```bash
git add CAPSTONE.md && git commit -m "Day 10: CAPSTONE.md limitations and use of AI assistants" && git push
```


### S · slides.pdf (by hand)

Use the course template (8 slides) and export `slides.pdf` into the repo root, under 15 MB. Slide 4 copies the
EVIDENCE.md tables; slide 6 copies the Results rows **exactly** (the headline lines of the two fixed-guide runs, the
two first-guide runs and the two baseline runs). A good slide 6 is the summary table from D2:

| Set (2 runs, 24 files) | Fully migrated | Tokens per file | Calls per file |
|---|---|---|---|
| Baseline | 22/24 | 3682 | 3.17 |
| Improved, first guide | 20/24 | 4411 (+19.8%) | 3.83 |
| Improved, fixed guide | 24/24 | 3090 (-16.1%) | 3.00 |

The slide-by-slide content plan is in part 2 (C34). Then:

**Check**, it must end with `slides OK`:

```bash
python3 - <<'PY'
import re, shutil, subprocess
b = open("slides.pdf", "rb").read()
assert b.startswith(b"%PDF"), "slides.pdf is not a PDF file"
pages = None
if shutil.which("pdfinfo"):
    out = subprocess.run(["pdfinfo", "slides.pdf"], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    pages = int(m.group(1)) if m else None
if pages is None:
    m = re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", b)
    pages = max(int(x) for x in m) if m else None
print("slides.pdf:", len(b) // 1024, "KB,", pages if pages is not None else "unknown number of", "pages")
assert pages in (8, None), "the template has 8 slides"
assert len(b) < 15 * 1024 * 1024, "slides.pdf is over 15 MB; export it again with smaller images"
print("slides OK")
PY
```

```bash
# do not commit slides.pdf yet: it goes into the last commit together with D5
```

### D4 · Contributions and the Members table

Every other commit is in by now. For each member it counts the commits from `git log` and the model calls (first and last, UTC) from `traces/`, and writes the Contributions section and the Members table. The "what they built" sentence per member follows the plan (including F1 to F7); read the four lines once and correct any that don't match who actually did what. The commit lists come from git and are the evidence. If it prints `WARNING: some commits have an author name that is not a Gitea user`, move those commits under the right member by hand.

Paste it on its own; it must end with `CAPSTONE.md and EVIDENCE.md updated`:

```bash
python3 - <<'PY'
import glob, json, re, subprocess
def git(*a):
    return subprocess.check_output(["git", *a], text=True).strip()
cap = open("CAPSTONE.md").read()
slots = re.findall(r"^(M[1-4])\s+(\S+), roll number: (\d+)", cap, re.M)
assert len(slots) == 4, slots
users = {u: (m, roll) for m, u, roll in slots}
head = git("rev-parse", "--short=12", "HEAD")
log = [line.split("\t", 3) for line in git("log", "--format=%h%x09%an%x09%ae%x09%s").splitlines()]
def owner(name, email):
    for u in users:
        if name == u or email.split("@")[0] == u:
            return u
    return None
commits = {u: [] for u in users}
other = []
for h, name, email, subj in log:
    u = owner(name, email)
    (commits[u] if u else other).append((h, subj))
calls = {u: [] for u in users}
for f in sorted(glob.glob("traces/*.jsonl")):
    rows = [json.loads(line) for line in open(f)]
    member = next((r.get("member") for r in rows if r["type"] == "run_start"), None)
    if member in calls:
        calls[member] += [r["ts"] for r in rows if r["type"] == "step"]
built = {
    "M1": "the libv v1 and v2 library with its tests, the change list and the 12-section guide with its validator; "
          "clients 07-10 with their tests, hand migrations and cases; baseline round 1; the rewrite of guide sections "
          "G02 and G09 after the case_02 and case_09 traces (F1); the fixed-guide round 2 run and its comparison",
    "M2": "clients 01-06 with their tests and hand migrations; the checkpoint rows; the adversarial clients 11 and 12 "
          "(m11, m12) with their tests, hand migrations, cases and the Safety control text; improved round 1 and its "
          "comparison; the final CAPSTONE.md and EVIDENCE.md updates, the slides and the freeze row",
    "M3": "keyword retrieval, the gateway client and tool registry, the agent loop with its trace and result files, "
          "the smoke run and the Architecture and Harness bounds sections; the run budget, the live run entry point "
          "and eval/compare.py; baseline round 2 and the first backup run; the repeat-search note in search_guide (F2) "
          "and the backup run with the fixed guide",
    "M4": "the Checkpoint 1 report sections and cases, the AST v1 check, the write_file scope guard, eval/check_hand.py, "
          "the Checkpoint 2 baseline run and the Safety and Evaluation sections; improved round 2 and its comparison, "
          "the first EVIDENCE rows and Results text; the fixed-guide round 1 run and its comparison",
}
lines = [f"Commits on main by Gitea user, from `git log` up to `{head}` (short hashes):"]
for u, (m, roll) in sorted(users.items(), key=lambda x: x[1][0]):
    cs = commits[u]
    lines.append(f"- **{m} {u}** (roll number {roll}): {built[m]}. {len(cs)} commits: "
                 + ", ".join(f"`{h}` {subj}" for h, subj in reversed(cs)) + ".")
if other:
    lines.append("- Commits by other author names: " + ", ".join(f"`{h}` {subj}" for h, subj in reversed(other)) + ".")
contrib = "\n".join(lines) + "\n"
old = "Per member: what they built, with commit hashes.\n"
if old not in cap:
    raise SystemExit("placeholder not found, edit CAPSTONE.md by hand: " + old.strip())
open("CAPSTONE.md", "w").write(cap.replace(old, contrib, 1))
ev = open("EVIDENCE.md").read()
for u, (m, roll) in users.items():
    ts = sorted(calls[u])
    row_old = f"| {m} | | | | | | |"
    if row_old not in ev:
        raise SystemExit(f"Members row {m} not found or already filled")
    ev = ev.replace(row_old, f"| {m} | {roll} | {u} | {len(commits[u])} | {len(ts)} | "
                             f"{ts[0] if ts else '-'} | {ts[-1] if ts else '-'} |", 1)
note = "not kept). Give a one-line explanation of any large gap.\n"
gap = ("\nOur gap: every member's gateway calls also include aider, which wrote the code for their commits, and runs "
       "repeated after a failed check; only the committed runs are in traces/. Commits are counted up to "
       f"`{head}`; the two commits after it only fill in these tables, then add slides.pdf and the freeze row.\n")
if note not in ev:
    raise SystemExit("Members note not found in EVIDENCE.md")
ev = ev.replace(note, note + gap, 1)
open("EVIDENCE.md", "w").write(ev)
print(contrib)
for u, (m, roll) in sorted(users.items(), key=lambda x: x[1][0]):
    print(m, u, "commits", len(commits[u]), "model calls in traces", len(calls[u]))
if other:
    print("WARNING: some commits have an author name that is not a Gitea user; check the 'other author' line.")
print("CAPSTONE.md and EVIDENCE.md updated")
PY
```

**Check**, paste it on its own; it must end with `members OK`:

```bash
python3 - <<'PY'
import re
s = open("CAPSTONE.md").read()
ev = open("EVIDENCE.md").read()
c = s[s.index("## Contributions"):s.index("## Use of AI assistants")]
assert "Per member: what they built" not in c and len(re.findall(r"^- \*\*M[1-4] ", c, re.M)) == 4
rows = re.findall(r"^\| (M[1-4]) \|(.*)\|$", ev, re.M)
assert len(rows) == 4, rows
for m, r in rows:
    cells = [x.strip() for x in r.split("|")]
    print(m, cells)
    assert all(cells), m + " has an empty cell"
    assert int(cells[2]) > 0, m + " has no commits"
    assert int(cells[3]) > 0, m + " has no model calls in traces"
assert "Our gap:" in ev
print("members OK")
PY
```

```bash
git add CAPSTONE.md EVIDENCE.md && git commit -m "Day 10: CAPSTONE.md contributions, EVIDENCE.md members table" && git push
```


### D5 · the freeze row (last commit)

A commit can't contain its own hash, so the freeze row gets the full hash of D4, the last commit with content, and D5 changes only that row. If anyone has to push a fix before the freeze, run D5 and its check again after it (the script replaces the old value).

Paste it on its own; it must end with `Freeze commit:`:

```bash
python3 - <<'PY'
import re, subprocess
full = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
p = "EVIDENCE.md"
s = open(p).read()
s, n = re.subn(r"^\| Freeze commit \(full hash\) \|[^|\n]*\|$", f"| Freeze commit (full hash) | {full} |", s, flags=re.M)
if n != 1:
    raise SystemExit("Freeze row not found in EVIDENCE.md")
open(p, "w").write(s)
print("Freeze commit:", full)
PY
```

**Check**, paste it on its own; it must end with `freeze row OK`:

```bash
python3 - <<'PY'
import re, subprocess
ev = open("EVIDENCE.md").read()
m = re.search(r"^\| Freeze commit \(full hash\) \| ([0-9a-f]{40}) \|$", ev, re.M)
assert m, "freeze row"
assert m.group(1) == subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
print("freeze row OK:", m.group(1))
PY
```

```bash
git add slides.pdf EVIDENCE.md && git commit -m "Freeze: slides.pdf and EVIDENCE.md freeze commit" && git push
```


```bash
git log -1 --format=%H
```

Post "D5 pushed, freeze row = <hash>". The repo is done.

## If something goes wrong

- **`text not found` / `placeholder not found`**: that part of CAPSTONE.md was edited by hand, or the script already
  ran (D2 refuses a second run instead of writing the text twice). Check `git log -3` and the section, and don't
  force it.
- **`AssertionError` in D2 before it writes anything** (the asserts about case_02 / case_09): a trace or result file
  is not what it should be. Don't edit the traces; post the error and stop.
- **D4 `Members row M1 not found or already filled`**: D4 already ran. Check `git log -3`.
- **A check fails after its script**: run `git checkout -- CAPSTONE.md EVIDENCE.md` to undo, then post the output.

## Before the presentation

- The live run (`bash live/run_live.sh`) now uses the fixed guide; the backup to show if the gateway fails is
  `traces/backup-p04-improved-20261115T124945Z-backup3.jsonl` (2/2, 6 calls, 25 s, recorded on 15 Nov inside the 48 hours). Don't commit a live run after the freeze.
