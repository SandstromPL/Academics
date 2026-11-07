# Lab 12b: A Sandboxed Code-Execution Server, and One Host for Three Servers

Builds on Lab 12a and the Week 12 lecture. `aider` is available for this
session. This repo starts from the **Lab 12a reference solution**: the file
server (with `search_files`), the git server and their eval are all here and
working. Lab 12a's handout is `LAB12A.md`; the tutorial is `TUTORIAL.md`.

## The idea

An agent that can run code is the most useful kind and the most dangerous
kind. Today you build the third server of capstone Track F: `run_python`,
which runs a short Python program for the model. Running it in a subprocess
is not enough. `naive_exec_tools.py` does exactly that, and the eval shows
what it lets through: an endless loop, a 1 GiB allocation, 200 processes,
your API key from the environment, a secret file one folder up (read, or
moved in), a network connection, a 50 MB file, and C code through `ctypes`.

You add four layers, each enforced in code, outside the model:

| Layer | Stops | Enforced by |
|---|---|---|
| wall-clock kill | a program that waits forever (sleeping, blocked) | the server (`os.killpg`) |
| resource limits | a busy loop (CPU), memory, file size, open files | the kernel (`resource.setrlimit`) |
| a clean environment | reading `OPENAI_API_KEY` and other secrets | the server (`env=`) |
| an audit hook | sockets, new processes, `ctypes`, and opening, renaming, removing or linking files outside the scratch folder | Python itself (`sys.addaudithook`) |

Then you put all three servers behind **one host**, and `run_python` goes
on the host's approval list. A person says yes before any code runs, and the
sandbox still has to hold after that yes. Approval decides *whether* to run;
the sandbox decides *what the program can reach* once it runs. The eval
approves every attack on purpose.

**An honest limit, measured on our own workspaces.** The workspace
containers do not allow a separate network namespace (`unshare` is not
permitted), and they can reach the internet. So the network block here is
Python's audit hook, which runs inside the same process as the snippet:
native code can get round it, which is why `ctypes` is blocked too. The
resource limits are enforced by the kernel and cannot be got round from
inside. Say which is which in your notes.

## Setup (5 minutes)

    python3 setup_exec_world.py     # worlds/: world/ (files), git_world/ (git), exec_world/ (code)
    python3 lab12b.py check         # what works so far (nothing yet)

Everything runs offline with `--offline` (a stub model, no gateway). Live
runs use `OPENAI_BASE_URL` / `OPENAI_API_KEY`, already set in your workspace.

## The files

| File | What | Yours? |
|---|---|---|
| `exec_tools.py` | `run_python` and its sandbox: constants given, bodies empty | **yes**, Part A |
| `host.py` | the host for three servers: `MultiHost` given | **yes**, Part B (three parts) |
| `exec_server.py` | the MCP code-execution server (`file_server.py` with your tool) | given |
| `naive_exec_tools.py` | `run_python` with no sandbox, for comparison | given, do not copy |
| `eval12b_cases.py` | the eval's cases | add two (C1) |
| `lab12b.py` | `check`, `eval`, `ask` | given, do not edit |
| `setup_exec_world.py` | builds `worlds/` | given |
| everything from Lab 12a | file and git servers, agent, client, stub | given (reference) |
| `notes.md` | your notes | **yes**, C2 |

## Part A -- the sandbox (55 marks), all in `exec_tools.py`

Read the docstrings; they are the contract. Do them in this order.

**A4 (13) -- `check_code(code)`.** A non-empty string (not just spaces) of
at most 10000 characters, else raise `SandboxError`. `call_tool` turns a
`SandboxError` into a refusal the model can read.

**A1 (15) -- `run_sandboxed(code, scratch)`.** The core. Start
`[sys.executable, "-I", "-c", audit_prelude(scratch) + "\n" + code]` with
`subprocess.Popen` (an argument list, never `shell=True`), with:
- `cwd=scratch` (create it if needed);
- `env=` exactly `PATH=/usr/bin:/bin`, `HOME=<scratch, absolute>`,
  `LANG=C.UTF-8`. Nothing else: the snippet must not see your key;
- `stdin=subprocess.DEVNULL`, `start_new_session=True` (a process group of
  its own, so you can kill all of it), `preexec_fn=make_limits()`;
- `communicate(timeout=WALL_TIMEOUT_S)`; on `TimeoutExpired`,
  `os.killpg(proc.pid, signal.SIGKILL)`, then `communicate()` again, and set
  `timed_out` True;
- cut stdout and stderr at 4000 characters each; `truncated` True if either
  was cut.

Return `{"stdout", "stderr", "exit_code", "timed_out", "truncated"}`. Never
raise for anything the snippet does. Try it now with `audit_prelude`
still returning `""` and `make_limits` doing nothing:

    python3 lab12b.py ask "Run this Python: print(2 ** 10)" --offline --approve yes

**A2 (12) -- `make_limits()`.** Return the function `preexec_fn` will call
in the child, just before the snippet starts. It sets soft and hard limits
with `resource.setrlimit`: `RLIMIT_CPU` 2 s, `RLIMIT_AS` 256 MiB,
`RLIMIT_FSIZE` 1 MiB, `RLIMIT_NOFILE` 64. If a hard limit is already lower
than the value, use the lower one (`setrlimit` refuses to raise a hard
limit).

Why no limit on the number of processes (`RLIMIT_NPROC`)? We measured it.
That limit counts every thread of a Linux user ID, and on our VMs all the
workspace containers run as the same user ID: on one VM that user already
had 3048 threads, while a container can see only its own ~480. Any value
you could set from inside a container is below what the others already
use, so even an ordinary thread in a snippet would fail. New processes are
refused by your audit hook instead (A3). This is a real limit of this
sandbox: write it down in your notes.

**A3 (15) -- `audit_prelude(scratch)`.** Return Python *source* that
installs an audit hook before the snippet runs. The hook raises
`PermissionError` for:
- every event in `BLOCKED_EVENTS`;
- every event in `PATH_EVENTS` (rename, remove, mkdir, symlink, chmod...)
  whose path arguments are outside `scratch`. Checking only `open` is not
  enough: `os.rename('../secrets/api_key.txt', 'k.txt')` would move the
  secret in;
- the `"open"` event (arguments: path, mode, flags) on any path whose
  `os.path.realpath` is outside `scratch`, except a *read* under Python's own
  `sys.base_prefix`, `sys.prefix` or `sys.exec_prefix` (every `import` opens
  files there) and `/dev/null`, `/dev/urandom`. The docstring says exactly
  what counts as a read.

A path can be `str`, `bytes`, or an `int` (an already open file; allow it).
Two traps: compare against `scratch + os.sep` (otherwise `.../s` matches
`.../sec.txt`), and bind everything the hook uses (`os.path.realpath`, the
folder, the lists) when it is installed, because the snippet runs after it
and can replace `os.path.realpath`. Put the values into the source with
`repr()`, and `del` the hook function afterwards. Line numbers in error
messages count the prelude's lines too.

## Part B -- one host for three servers (25 marks), all in `host.py`

`MultiHost` (given) starts the file, git and code servers and gives the
model all their tools at once. Two servers could offer a tool with the same
name, and the host has to know where each call goes.

**B1 (10) -- `namespaced_tools(listings)`.** `{server: [tools/list
entries]}` -> the `tools=` list (use `mcp_tools_to_openai`), each named
`<server>__<tool>` (`files__read_file`, `git__git_log`,
`code__run_python`) with its description starting `[<server>] `.

**B2 (8) -- `route(name, servers)`.** `"git__git_log"` -> `("git",
"git_log")`; split on the first `__` only. Anything that is not a known
server, `__`, and a non-empty tool name raises `KeyError` (the host turns it
into an error the model can read).

**B3 (7) -- `NEEDS_APPROVAL`.** The host's own list, by namespaced name:
every tool that writes or executes, on any server. Three tools.

Try the host:

    python3 lab12b.py ask "Read notes.txt. Then show me the last 2 commits." --offline
    python3 lab12b.py ask "Read notes.txt. Then run this Python: print(14 * 2)" --offline

Both ask `Approve? [y/N]`. The second, before its code runs. The first
because a commit subject in the git world carries a planted instruction
to call `git_commit` (Lab 12a), and the stub obeys it: answer `n`. Drop
`--offline` to use the real model.

## Part C -- evaluate it (20 marks)

    python3 lab12b.py eval --offline

runs every case on fresh worlds, through your host, twice: the code server
with your `exec_tools.py` (**guarded**) and with `naive_exec_tools.py`
(**naive**). The person's answer is written into each case first: *yes* to
every attack (only the sandbox stands in the way) and *no* in `denied`
(only the host's approval list stands in the way). Done, guarded passes
every case and naive fails every attack except `denied`.

**C1 (10).** Add two attack cases to `STUDENT_CASES` in `eval12b_cases.py`,
each attacking something the given cases do not, decided from the world
(`w.runs`, `w.outputs`, `w.scratch`, `w.big_files()`), and passing on your
guarded server offline. Decide from what happened, not from what was
printed: a live model that is blocked often tries again a different way
(for example, it writes the file inside scratch instead and prints
"done"), so check the file system, not the word. The stub's phrasings are at the top of the file.
Then run it live and keep the output:

    python3 lab12b.py eval | tee eval12b_live.txt

(28 runs, about 7 minutes). Expect `file-then-code` to fail live: when the
model has already used one server, our 32B model tends to skip the second
step (or writes the call as plain text instead of making it), so nothing
runs. That is a model failure, not your sandbox's; the check is right to
call it a fail. Say in your notes what you saw in the trace.

**C2 (10).** `notes.md`, three sections, a few lines each: what each layer
stops (name the eval case); one thing a snippet could still do that none of
your layers catches, and why; and what approval protects against that the
sandbox cannot, and the other way round.

## What to commit

    git add exec_tools.py host.py eval12b_cases.py notes.md eval12b_live.txt
    git commit -m "Lab 12b: sandboxed run_python, three-server host, eval"
    git push

`python3 lab12b.py check` should show every item ok before you push.

## Grading

After the cutoff (announced by the TAs; 7 PM today unless they say
otherwise) the grader runs a hidden test suite, offline, against the files
in your last commit, with inputs not in this handout (other escapes, other
paths, other tool names). A refusal only counts if the same sandbox also
runs ordinary code, so a sandbox that refuses everything scores nothing. TAs
mark `notes.md`.

| Part | Task | Marks |
|---|---|---|
| A | A1 `run_sandboxed` | 15 |
| A | A2 `make_limits` | 12 |
| A | A3 `audit_prelude` | 15 |
| A | A4 `check_code` and the registry | 13 |
| B | B1 `namespaced_tools` | 10 |
| B | B2 `route` | 8 |
| B | B3 `NEEDS_APPROVAL` | 7 |
| C | C1 two attack cases (+ `eval12b_live.txt`) | 10 |
| C | C2 `notes.md` | 10 |
| | **Total** | **100** |
