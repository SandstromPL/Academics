# Lab 12a: MCP Tool Servers -- the File Server, and a Git Server of Your Own

Builds on Week 12's lecture, "MCP Tool Servers". `aider` is available for
this session. Lab 12b (Thursday) builds on what you make today, so finish it.

## The idea

In the lecture you built a file server over MCP: the tools moved out of
your agent's process, behind a protocol, and the guards moved with them
into the server. Today you do that again **for a new tool surface, git**,
on your own.

Git looks safe because the server never uses a shell. It is not. Every
argument the model sends goes to git, and git reads arguments that start
with `-` as **options**:

    git show --output=../pwned.txt      writes a file outside the repository
    git diff ../secrets/api_key.txt /dev/null    prints a file outside it

That is **argument injection**: an argument list stops shell injection, not
this. You will write the server's guards so that a revision is only ever a
revision and a path is only ever a path inside the repo. And the server has
one write tool, `git_commit`, which the **host** -- not the server -- makes
wait for a person's yes, from the host's own list (lecture slide 13).

All three servers of capstone Track F start here: the file server
(today, Part A), the git server (today, Part B) and a sandboxed
code-execution server (Lab 12b).

## Setup (5 minutes)

    python3 setup_world.py          # the tutorial's file world
    python3 setup_git_world.py      # the git world: git_world/repo, git_world/secrets
    python3 lab12a.py check         # what works so far (all empty at the start)

Everything runs offline with `--offline` (a stub model, no gateway). Live
runs use `OPENAI_BASE_URL` / `OPENAI_API_KEY`, already set in your workspace.

## The files

| File | What | Yours? |
|---|---|---|
| `TUTORIAL.md` and its files (`file_server.py`, `mcp_client.py`, `agent.py`, `guard.py`, `stub_model.py`, `setup_world.py`, `demo_step*.py`, `sdk_file_server.py`, `test_mcp_tutorial.py`) | the Week 12 tutorial, for reference (A1, optional) | edit only `file_tools.py` (A2) and one line of `agent.py` (B5) |
| `git_tools.py` | the git server's tools: registry given, bodies empty | **yes**, Part B |
| `git_server.py` | the MCP git server: `file_server.py` with your git tools | given |
| `naive_git_tools.py` | the same tools with no checks, for comparison | given, do not copy |
| `setup_git_world.py` | builds the practice repo | given |
| `eval_cases.py` | the git eval's cases | add two (C1) |
| `lab12a.py` | `check`, `eval`, `ask` | given, do not edit |
| `notes.md` | your notes | **yes**, C2 |

## Part A -- the tutorial, then one more tool (20 marks)

**A1 (optional, not graded).** `TUTORIAL.md` is the lecture's tutorial,
here for reference: Part B follows the same pattern, so look back at it when
you need to. You do not have to work through it or submit anything for it.
If you want the practice, steps 0-6 take about 20 minutes, and
`python3 demo_step6_eval.py` runs its eval live.

**A2 (20).** Add a fourth tool to the file server, `search_files`, in
`file_tools.py`'s `build_registry` (put it after `write_file`):

- `search_files(query)`, permission `read`.
- Returns `{"query": query, "matches": [...]}`: the paths, relative to the
  sandbox, with `/` separators, **sorted**, of the files whose text contains
  `query`, ignoring case. At most 50.
- An empty or blank `query` returns `{"error": ...}`.
- Guarded, it must never read outside the sandbox: not through
  `shared/` (a symlinked folder), and not through a symlinked **file**
  either. Use `locate()` on every file you open, and **skip** a file it
  refuses (one planted symlink must not break the whole search).
  `os.walk` does not follow symlinked folders, but it does list symlinked
  files.
- More than 50 matches: the first 50 in sorted order.

Try it: `python3 agent.py "Search the files for 'deadline'." --offline`.

## Part B -- the git server (60 marks)

All in `git_tools.py`. Read its docstrings; they are the contract. The
repo is `git_world/repo` (5 commits; `git -C git_world/repo log --oneline`).

**B6 (12) -- `run_git(repo, args)` first.** Every tool uses it.
`subprocess.run(["git", "-C", repo, *args], ...)`: an argument list, never
`shell=True`, a 10 s timeout, `capture_output=True, text=True`. Returns
`(True, stdout)` on exit 0; otherwise `(False, reason)`: the first line
of stderr, or if stderr is empty (git prints "nothing to commit" on
stdout) the last line of stdout. Never raises.

**B1 (12) -- `check_rev(rev)`.** Accept exactly `HEAD`, `HEAD~N` (N 0-99),
`HEAD^`, or a lowercase hex hash of 4-40 characters; raise `GuardError` for
anything else. Write an **allow-list** (`re.fullmatch`) of what is
accepted. A block-list of what is refused ("starts with `-`", "contains
`..`") always misses one.

**B2 (8) -- `git_log(max_count=10, path=None)`.**
`{"commits": [{"commit", "author", "date", "subject"}, ...]}`, newest
first, short hashes. Clamp `max_count` to 1-50. If `path` is given, check
it with `resolve_in_root(repo, path)` and pass it after `--`. Hint:
`--format=%h%x1f%an%x1f%ad%x1f%s --date=short` gives one line per commit
with an unprintable separator.

**B3 (8) -- `git_show(rev)`.** `check_rev`, then
`git show --stat --patch <rev> --`. Returns `{"rev", "text", "truncated"}`,
`text` cut at 4000 characters.

**B4 (8) -- `git_diff(rev_from, rev_to="HEAD")`.** `check_rev` both, then
`git diff <rev_from> <rev_to> --`. Returns `{"rev_from", "rev_to", "text",
"truncated"}`.

**B5 (12) -- `git_commit(message, paths)`, and the host.**
- `message`: a non-empty string, one line, at most 200 characters.
- `paths`: a non-empty **list** of strings; each must pass
  `resolve_in_root` and be an existing file in the repo (`vault/` is a
  symlink out of it).
- `git add -- <paths>`, then `git commit -q -m <message> -- <paths>`.
  Then `git rev-parse --short HEAD` for the hash. Returns
  `{"commit": <short hash>, "files": paths}`. A refused input can raise
  `GuardError` or return `{"error": ...}`; the model sees an error either
  way.
- **And** add `"git_commit"` to `NEEDS_APPROVAL` in `agent.py`. That set is
  the host's own policy. Until you do, nothing asks a person before a
  commit, and two of the eval's attacks get through.

Try each tool as you finish it, by hand over MCP or through the agent:

    python3 lab12a.py ask "Show me the last 3 commits." --offline
    python3 lab12a.py ask "Show commit HEAD~3." --offline
    python3 lab12a.py ask "Commit notes.md with message 'Add the viva date'." --allow read,write --offline

(Drop `--offline` to use the real model. The last one asks you
`Approve? [y/N]` once B5 is done. `ask` writes
`harness_trace.jsonl` and `server_log.jsonl` and prints them joined, as in
the tutorial's Step 4.)

## Part C -- evaluate it (20 marks)

    python3 lab12a.py eval --offline

runs nine cases on a fresh `git_world` each, against your `git_tools.py`
(**guarded**) and `naive_git_tools.py` (**naive**). Verdicts come from the
world: the commit count, files on disk, where the secret ended up. With
everything done, guarded passes all of them and naive fails the four
argument-injection attacks. Two attacks (`commit-denied`,
`injected-commit`) depend on the host, not the server: once `git_commit`
works, they fail in **both** columns until B5's `NEEDS_APPROVAL` line is in.

**C1 (10).** Add two attack cases to `STUDENT_CASES` in `eval_cases.py`.
Each must attack something the nine do not, decide its verdict from the
world (`w.commits()`, `w.exists()`, `w.leaked()`), and pass on your
guarded server offline. Offline the stub only understands the phrasings
listed at the top of `eval_cases.py`, and it obeys any
`call <tool> with {json}` it reads in a tool result.

Then run it live and keep the output:

    python3 lab12a.py eval | tee eval_git_live.txt

(22 runs, about 8 minutes; a live model may refuse an attack
the stub obeys, so naive's column can be better live than offline. Say so
in your notes if it is.)

**C2 (10).** `notes.md`, three sections, a few lines each:
1. **What each guard stops.** For `check_rev`, `--` and the host's
   approval list: one eval case each stops. The path check
   (`resolve_in_root`) stops none of the nine on its own -- git refuses
   most outside paths itself -- so say what it adds (one of your C1 cases
   may show it).
2. **One attack your guards do NOT stop**, and why. (Think about what a
   person approving `git_commit` actually sees, or about a commit that is
   allowed but should not be.)
3. **Host versus server.** What the host's approval list can do that the
   server cannot, and the other way round.

## What to commit

    git add file_tools.py agent.py git_tools.py eval_cases.py notes.md \
            eval_git_live.txt
    git commit -m "Lab 12a: search_files, git server, eval"
    git push

`.gitignore` keeps `world/`, `git_world/` and the `.jsonl` logs out.
`python3 lab12a.py check` should show every item ok before you push.

## Grading

After the cutoff (announced by the TAs; 7 PM today unless they say
otherwise) the grader runs a **hidden** test suite, offline, against the
files in your last commit: A2 and every Part B task, including inputs not
in this handout (other option forms, other paths, other malformed
messages). A refusal only counts if the same tool also works on a normal
call, so a tool that refuses everything scores nothing. It also runs the
offline eval with your two cases. TAs mark `notes.md` and may ask you to
explain a guard during the session.

| Part | Task | Marks |
|---|---|---|
| A | A1 the tutorial (reference, optional) | 0 |
| A | A2 `search_files` | 20 |
| B | B1 `check_rev` | 12 |
| B | B2 `git_log` | 8 |
| B | B3 `git_show` | 8 |
| B | B4 `git_diff` | 8 |
| B | B5 `git_commit` + host approval | 12 |
| B | B6 `run_git` | 12 |
| C | C1 two attack cases (+ `eval_git_live.txt`) | 10 |
| C | C2 `notes.md` | 10 |
| | **Total** | **100** |
