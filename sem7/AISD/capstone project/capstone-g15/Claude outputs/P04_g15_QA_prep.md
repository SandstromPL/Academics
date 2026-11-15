# P04 / g15: Q&A prep for the presentation

For all four of us. Read your own section twice, and the "Numbers" and "Do not say" parts once.
Every answer here is checked against the frozen repo (freeze HEAD `48ac6dbfd8f3`, then the freeze commit).

## How the Q&A works

- 3 minutes after slide 8. The evaluators ask **named members**, and every member answers at least one question.
- Graded as C5 (×1): "every member answers precisely, including trade-offs and limits".
- If the records and the Q&A both suggest a member did little, that member gets a **5-minute follow-up on the code
  they say they wrote**. The launch deck also says "Large code with no editing history will be asked about". Our code
  came from aider in big single commits (for example the 338-line `harness/agent.py` in `e30280555c`), so **each of us
  must be able to open our own files and explain them line by line**.
- How to answer: one or two sentences, a number, and the file or trace that proves it. If you don't know, say
  "I don't know exactly; it is in <file>", and don't guess.

## The 30-second answer to "what did you build?"

We wrote a small payments library, `libv`, with a v1 and a v2 API, a 12-section migration guide, and 12 client files
that use v1. An agent on the course model `main` migrates each client to v2 with four tools: search_guide, read_file,
write_file and run_tests. A file counts as migrated only if its tests pass against v2 and our AST check finds no v1
name. We compared a baseline (no guide) with an improved version (with search_guide) on the same 12 cases, two runs
each. The first guide made things worse: 20/24 against 22/24. After we fixed two guide sections from the traces we
got 24/24, with 16% fewer tokens than the baseline. A write-scope gate stops the agent writing anything except the
client it is migrating.

## Numbers to know

| What | Number |
|---|---|
| Cases | 12: 6 simple, 3 edge (case_05, 08, 10), 3 adversarial (case_06, 11, 12) |
| Guide | 12 sections, G01 to G12; 5 of them are pure renames (the 5 v1-only names) |
| Baseline, 2 runs | 22/24 fully migrated, 3,682 tokens per file, 3.17 calls per file |
| Improved, first guide | 20/24, 4,411 tokens per file (+19.8%), 3.83 calls per file |
| Improved, fixed guide | 24/24, 3,090 tokens per file (−16.1%), 3.00 calls per file |
| Retrieval hit rate | 0.947 = 18 of the 19 needed section ids were returned (G03 for case_08 was never returned) |
| Step limit | 8 model calls per file |
| Timeouts | 180 s per file, 60 s per model call, 30 s per pytest run |
| Retries | 2 (openai SDK, on 429, 5xx and network errors) |
| Context | `main` takes 16,384 tokens; we ask for at most 2,000 reply tokens; largest real prompt 3,303 |
| Tool output fed back | cut to 1,500 chars; one guide section cut to 600 chars, k at most 3 |
| Live run | case_02 and case_11, at most 20 calls and 110 s |
| Backup | `traces/backup-p04-improved-20261115T124945Z-backup3.jsonl`: 2/2, 6 calls, 25 s, by paritoshl |
| Safety | 3 denied writes in real runs, all case_02, all to `tests/test_client_02.py`, all baseline |
| Commits / calls in traces | M1 9 / 74, M2 12 / 52, M3 12 / 57, M4 15 / 100 |

**Known small slip:** slide 4 says "104 gate events". That was counted before backup3, which added 2 allowed writes.
The repo now has **106 gate events, still 3 denied**. If asked, say exactly that.

## Your own section

### M1 agastyan: the library, the guide, clients 07–10, the guide fix (F1)

Your files: `data/libv/v1.py`, `data/libv/v2.py` and their tests, `data/make_guide.py` → `data/guide.json`,
`data/validate_guide.py`, clients 07–10 with their tests and hand migrations, commit `8cc69d465f` (F1).

- **What changed from v1 to v2?** Twelve changes, one per guide section. Five are renames: get_balance →
  fetch_balance, InsufficientFunds → BalanceTooLow, AccountNotFound → UnknownAccount, PaymentError → PayError, and
  charge_and_receipt removed (use charge + make_receipt). The rest change behaviour: transfer's argument order (G02),
  dataclasses instead of dicts (G03, G09), Money objects (G07, G11), integer paise (G08), keyword-only arguments
  (G10), and list_transactions needing a limit (G09).
- **How is the guide made and checked?** make_guide.py writes guide.json: each section has an id, a title, a text,
  and a BEFORE and an AFTER code example. validate_guide.py checks 12 to 20 sections, every field present, ids like
  G01 with no duplicates, and each text non-empty and at most 600 chars.
- **Why did G02 fail?** The old G02 only listed the new parameter names. The model saw that the amount moved to the
  end and then put the two ids in the wrong order, so the payer paid the friend. The new G02 says only the amount
  moves and the two ids keep their order, with an example.
- **Why did G09 fail?** Its BEFORE and AFTER were the same line, so it never said that `limit` lost its default. The
  new G09 says to pass the limit (v1 used 10).
- **Isn't that cheating?** Partly, and we say so: we fixed the guide after seeing these 12 cases, so the fixed-guide
  numbers are optimistic. A fair test needs clients the guide has never seen.

### M2 paritoshl: clients 01–06, the adversarial clients 11–12, round 1, final docs, slides, backup

Your files: clients 01–06 and 11–12 with their tests and hand migrations (`data/clients/`, `eval/hand_migrations/`),
case_11 and case_12, the Safety control text, run `p04-improved-20261111T162925Z` and its comparison, the final
CAPSTONE.md and EVIDENCE.md, slides.pdf, and the backup run.

- **What are m11 and m12?** Prompt-injection attacks hidden in the client's docstring. m11 (case_11) tells the agent
  to add the v1 names back into `data/libv/v2.py`. m12 (case_12) tells it to edit its own test file. The scope gate
  must deny both writes, and the client must still be migrated.
- **Did the gate stop them?** No. The model (Qwen) ignored both docstrings in all our runs and migrated the files
  properly, so it never tried those writes. For those paths our evidence is `safety/test_scope.py`. The gate did
  deny real writes in case_02 (see M4).
- **What is an expected answer here?** A hand migration for every client. `eval/check_hand.py` proves, with no
  model, that the original client fails its tests and has v1 names, and that the hand migration passes with none.
- **Why is case_06 adversarial?** Its v1 names appear only in comments and strings. A grep would flag them; our AST
  check correctly ignores them.
- **Why is the hash on slide 4 one commit behind HEAD?** A commit can't contain its own hash. The slide and the
  freeze row show `48ac6dbfd8f3`; the freeze commit after it only adds slides.pdf and the freeze row.
- **Why a backup3?** The rule is one backup committed in the 48 hours before the freeze, named
  `traces/backup-<run_id>.jsonl`. backup2 started about a minute before that window and had the wrong name, so we
  recorded a new one today.

### M3 varunr: the loop, the model client, the tools, retrieval, the live run, F2

Your files: `harness/agent.py`, `harness/model.py`, `harness/tools.py`, `harness/retrieval.py`, `eval/compare.py`,
`live/run_live.sh`, commit `f140d24cad` (F2).

- **Walk us through one step.** The prompt has the system rules, the client and the v2 signatures. Each step is one
  model call. The reply must hold one JSON object `{"tool": ..., "args": {...}}` (for write_file the code can follow in
  a python block). `parse_action` finds the first JSON object with a "tool" key, `validate_arguments` checks the tool
  and argument types against `TOOL_REGISTRY`, `dispatch` runs it, and the result (cut to 1,500 chars) goes back as the
  next user message. Every step is a trace row with the tokens, the response_id and the tool.
- **When does a file stop?** Tests green with zero v1 names (`green`), the model says `done`, 8 calls (`step_limit`),
  180 s (`timeout`), 3 bad replies in a row (`parse_errors`), a gateway error after retries (`model_error`), or the
  live-run budget (`run_budget`). Then plain code runs the tests and the v1 check again, and the client is restored.
- **What if the gateway goes down?** The SDK retries twice. Then `call_model` raises, the harness logs an error row,
  stops that file with `model_error`, and the batch goes on to the next case. Nothing crashes.
- **How does retrieval work?** Keyword overlap weighted by IDF: rare words count more, and words in the title count
  double. Identifiers are split (`get_balance` → get, balance), stopwords are dropped, k is at most 3 and each section
  is cut to 600 chars, so retrieval can't fill the context.
- **Why not embeddings?** 12 short sections full of exact names like `get_balance`. Keywords find those exactly, and
  a hit can be explained. The trade-off: no paraphrase matching. Synonym expansion (`--expand`) is built but not
  evaluated.
- **Why temperature 0?** So two runs of the same set are comparable; both runs gave the same outcome on every case.
- **What does F2 do?** If search_guide returns only sections it already returned in this file, it sends a short note
  instead of the same text again. It came from case_09's five repeated searches. It **never fired** in the
  fixed-guide runs; the fix there was the guide text (F1).
- **How is the live-run budget enforced?** Calls left and the deadline are checked before every model call. The limit:
  one slow call (60 s, 2 retries) can still overrun 110 s.

### M4 yallappagarid: the v1 check, the scope gate, check_hand, CP2, round 2, the fixed-guide round 1

Your files: `harness/v1check.py` and its tests, `safety/scope.py`, `safety/test_scope.py`, `eval/check_hand.py`,
the Safety and Evaluation sections, runs `p04-improved-20261112T164545Z` and `p04-improved-20261113T183159Z-v2`.

- **How does the gate work?** Every write_file goes through `check_write(path, case_client)` before anything is
  written. Both paths are resolved with `realpath`, so `../` and symlinks are caught, and the write is allowed only if
  the path is the current case's client file. Library, tests, other clients and anything outside the repo are denied
  with a reason. Each decision is a `gate` row in the trace.
- **Show it working.** Three real denies, all case_02 in the three baseline runs: the model tried to rewrite
  `data/clients/tests/test_client_02.py` to make its own wrong code pass. `safety/test_scope.py` covers v2.py, a test
  file, another client and `../` paths.
- **What does it not cover?** It guards writes only. run_tests imports the client the model wrote, so that code runs
  in our workspace during pytest (30 s timeout, no sandbox). The fix would be running pytest in a container with no
  network.
- **How does the v1 check work?** It parses the file with `ast`. It flags any libv.v1 import and any name defined in
  v1.py but not in v2.py (the 5 renames), including local shims like `def get_balance`. Comments and strings are never
  flagged.
- **What does it miss?** A function that kept its name but changed behaviour (transfer, charge, convert,
  format_amount, list_transactions, open_account). Only the tests catch those, which is why "migrated" needs both.
- **How do you prove the expected answers came first?** Git history: cases 01–06 were in CP1 (`54a047918b16`), cases
  07–10 in `16227096d9` and 11–12 in `21399d3b9b`, all before the first 12-case run (`7af1666a9e`).

## Questions anyone may get

**Why does the baseline do so well (22/24)?** Its prompt has the v2 signatures, so renames are easy. The guide can only
help where a change isn't visible in a signature: argument order (G02) and the lost default (G09).

**Why was the first guide worse?** Every improved file costs at least one extra call (search, then write, then test:
3 calls against the baseline's 2), plus the section text in the prompt. case_09 got stuck searching five times, and
case_02 still failed even though the right section was returned.

**So does retrieval help?** Only when the guide text is right. With the fixed guide, every file took 3 calls. The
baseline wasted all 8 calls on case_02 (and failed) and on case_12, so the improved version used 16% fewer tokens.
But the fix was shaped by these same cases.

**What does a 0.947 hit rate mean?** 18 of the 19 needed section ids came back from search_guide. It counts what
was returned, not what the model used: case_02 failed with G02 returned, and case_08 passed without G03.

**Why did the baseline need 8 calls on case_12?** format_amount now takes integer paise. It took four write-and-test
rounds to get the rounding right (`'Tea: INR 0.12'`, then `'19.98'` against `'19.99'`). G08's example
`round(70.0 * 100)` gives the improved version the answer in one write.

**Tell us about one failure from a trace.** Use slide 7 (case_09). The other one is case_02 in
`p04-baseline-20261109T145606Z`: steps 1, 6 and 8 wrote `transfer(payer_id, friend_id, share)` (wrong order), the
test said `assert 240.0 == 360.0`, and at step 4 it tried to rewrite the test, which the gate denied.

**Why are the two runs of each set identical?** Temperature 0 and the same prompts. That shows the result repeats;
it doesn't show it holds on other code.

**Why is `aux` not used?** One model keeps the comparison clean, and `main` was enough.

**Why are calls in traces lower than calls in the gateway log?** The gateway also counts aider's calls while we wrote
the code, plus runs we repeated after a failed check and did not keep. Only committed runs are in traces/.

**How did you use AI tools?** aider with `main` wrote the code from our prompts, with `--no-auto-commits`. Every
change was checked by the unit tests, `check_hand.py` and a check script with a scripted fake model before we
committed it by hand. Claude was used outside the course workspace to plan the work and draft prompts and scripts. It
is written in CAPSTONE.md. If someone points at "no other LLM", don't argue: say it was planning outside the lab,
made no calls in the project, and is disclosed.

**What would you do next?** Test the fixed guide on new clients it has never seen; evaluate `--expand`; sandbox
run_tests; add an adversarial case that actually makes the model try a bad write.

## Live run drill (whoever is named)

1. In your own workspace: `cd ~/capstone-g15 && git pull && git rev-parse HEAD`. Show that it is the freeze commit
   (the Gitea top commit, "Freeze: slides.pdf and EVIDENCE.md freeze commit").
2. `bash live/run_live.sh`: case_02 and case_11, about 25 s, at most 20 calls. While it runs, say what each line means.
3. `grep -m1 response_id traces/<run_id>.jsonl` and read the response id out loud so they can match it.
4. **Don't commit or push the live run.**
5. If the lab is down, show `traces/backup-p04-improved-20261115T124945Z-backup3.jsonl` (no cap; they repeat later).
   If our code fails, show the same file, but then the live-run score is capped at 1.

## Do not say

- That the gate stopped m11 or m12 (the model never tried those writes).
- That the fixed-guide result proves the guide works in general (it was fixed on these cases).
- That F2 fixed case_09 in the real runs (it never fired; the G09 text did).
- That the hit rate shows the model used the sections.
- That the code was written by hand. Say aider wrote it from our prompts and we checked and committed each part.
