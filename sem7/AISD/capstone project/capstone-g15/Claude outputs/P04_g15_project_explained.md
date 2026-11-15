# Our capstone project, explained simply (P04, group g15, team GREP)

This is a plain explanation of what our project is, who did what, how we worked, what we built, and how close we
are to what the professor asked for. It is based on the repo as it is now (after D1 and D2).

---

## 1. The project in a few lines

Course: CSP352 AI-Augmented Software Development. Project P04: **"API migration assistant with a retrieved guide"**.

Think of a small software library that changes its functions from an old version (**v1**) to a new version (**v2**).
Some functions are renamed, some change the order of their inputs, some return a different kind of value. Other
programs that use the library (we call them **client files**) break and have to be updated. Doing this update is
called a **migration**.

Our job was to:

1. write that small library ourselves, in a v1 and a v2 version;
2. write a **migration guide**: short notes that say what changed and how to fix it;
3. write 12 client files that still use v1;
4. build an **agent**: a program that asks an AI model, step by step, to update each client file to v2;
5. measure one thing: **does the agent do better when it can search the guide, or when it just guesses?** And how
   many more (or fewer) tokens does the guide cost?

A client file counts as "fully migrated" only if its tests pass with v2 **and** no v1 name is left in the code.

---

## 2. Words used in this document

| Word | Meaning here |
|---|---|
| libv v1 / v2 | our small payments library: the old version and the new version |
| client file | a small program that uses libv; ours start on v1 and must be moved to v2 |
| guide | `data/guide.json`: 12 short sections (G01 to G12), one per change from v1 to v2 |
| agent | our program in `harness/` that asks the model what to do, step by step, and carries it out |
| baseline | the agent **without** the guide: it sees the client file and the list of v2 function names only |
| improved | the agent **with** the guide: same as baseline, plus a `search_guide` tool |
| main | the AI model on the course gateway (a Qwen model); every member used their own key |
| trace | a log file of one run: every step, every model call, token counts (`traces/`) |
| result file | the summary of one run: which files passed, calls, tokens (`eval/results/`) |
| case | one test case: which client file, which guide sections it needs (`eval/cases/`) |
| hand migration | the correct v2 version of a client, written by us; it is the expected answer |
| aider | the coding tool we used in the lab; it sends our prompt to the model and writes the files |
| checkpoint / freeze | progress deadlines; the freeze is the final deadline (Sun 15 Nov, 11:59 PM IST) |

---

## 3. What the professor asked for

From the README, the CAPSTONE.md template and the EVIDENCE.md template in our repo (we could not open the capstone
web page itself from the computer used to write this, so check it once more for anything extra):

**The task**
- A guide of 12 to 15 sections, 12 client files to migrate.
- Four tools for the agent: `search_guide`, `read_file`, `write_file` (only allowed on the file being migrated),
  `run_tests`.
- A check, in plain code, that finds any v1 call left in a file.
- A **safety control** written in code (not just a rule in the prompt), and cases that test it.
- A comparison: baseline against improved, case by case, with regressions and token cost.

**The files the repo must have**
- `CAPSTONE.md`: the design report, with fixed headings.
- `EVIDENCE.md`: four tables (repo and checkpoints, members, runs, results).
- `slides.pdf`: 8 slides from the course template.
- `harness/`, `safety/`, `data/`, `eval/cases/` (pushed **before** any results), `eval/results/`, `traces/`
  (one per run, including a backup run), `live/run_live.sh` and `live/cases.json` for a live demo.

**Dates**
- Checkpoint 1, Thu 5 Nov: report sections 1 to 3 and at least 6 test cases.
- Checkpoint 2, Sun 8 Nov: the agent working end to end, one baseline result and its trace.
- Freeze, Sun 15 Nov, 11:59 PM IST: the last push before this time is our submission.

**Rules**
- Only the course workspace, our Gitea repo and the gateway models.
- Each member pushes from their own Gitea account and uses only their own key.
- Every model call and every commit is tracked and checked against each other.

The handout also gave a day-by-day plan: Day 0 list the changes, Day 1 library and guide, Day 2 clients and
expected answers, Day 3 the checks, safety, search and tools, Day 4 the agent loop and a first run, Day 5 the
baseline (Checkpoint 2), Days 6 to 8 the remaining clients, the improved runs, the comparison, the backup run, the
live run and the slides.

---

## 4. The team and the roles we gave at the start

The roles below are the split we made in our first plan (the professor gave the project and the rules; the team
split the work).

| Member | Gitea user | Roll no. | Role in the first plan (up to Checkpoint 2) |
|---|---|---|---|
| M1 | agastyan | 12340140 | Day 0 to 1: the list of changes, the library v1 and v2 with its tests, the guide (12 sections) and a script that checks it |
| M2 | paritoshl | 12341550 | Day 2: the first 6 client files with their tests, and their hand migrations (the expected answers); after Checkpoint 2, the repo link and checkpoint hashes in EVIDENCE.md |
| M3 | varunr | 12342320 | Day 3 to 4: guide search, the connection to the model, the 4 tools, the agent loop, the first test run (one file), the Architecture part of the report |
| M4 | yallappagarid | 12342390 | Checkpoint 1 (report sections 1 to 3, the first 6 cases); Day 3: the v1 leftover check and the safety guard; Day 5: the check of the expected answers, the Checkpoint 2 baseline run, the Safety and Evaluation parts of the report |

After Checkpoint 2 we split the rest the same way, by who knew that part best:

| Member | After Checkpoint 2 |
|---|---|
| M1 agastyan | clients 07 to 10 with tests, hand migrations and cases; baseline run round 1; the guide fix (G02, G09); the fixed-guide run round 2 and its comparison |
| M2 paritoshl | the two attack clients 11 and 12 with tests, hand migrations, cases and the Safety text; improved run round 1 and its comparison; the final report text, slides and freeze |
| M3 varunr | the run limit for the live demo, the live demo script, the comparison script; baseline run round 2 and the first backup run; the repeat-search note; the second backup run |
| M4 yallappagarid | improved run round 2 and its comparison, the first EVIDENCE rows and Results text; the fixed-guide run round 1 and its comparison |

Model calls in our traces per member: M1 74, M2 46, M3 57, M4 100. So every member has real runs on record.

---

## 5. How we worked

**One member at a time ("relay").** Commits had to go in a fixed order, because each step builds on the one
before. A member started only after the previous member pushed. Everyone pulled first and pushed after every commit,
never force-pushed, and always worked from their own login and key.

**aider wrote the code.** Each step had a prompt for aider. The prompt explained the task and gave the exact file
contents, and the course model (`main`) wrote the files through aider. We gave the exact contents because, when the
model only got a description, it changed numbers, names or test values, and the expected answers stopped matching.
The playbooks with these prompts and checks were prepared with Claude, outside the course workspace. We say this in
the "Use of AI assistants" section of the report, and it should stay there.

**A check before every commit.** After each step, a member ran a short check script. It made no model call. It
compared the files line by line with what the prompt asked for, ran the tests, and confirmed that no other file had
changed. Only after the check printed "OK" did the member commit and push.

**Real runs with each member's own key.** The experiment runs (baseline, improved, backup) were done by different
members, so that every member's key shows up in the traces.

**Problems we ran into and how we got past them**
- The model has a size limit (16,384 tokens in, 4,096 out). The agent loop file (`agent.py`) was too big to write
  in one go, so step C10 was split into two smaller prompts.
- One line of `agent.py` started with three backticks, which made aider cut the file short. We re-wrapped that
  line.
- At first there was a "fallback" zip with ready-made files. We removed it, so that every file in the repo is written
  by aider.
- Checkpoint 2 was due Sun 8 Nov but was pushed on Mon 9 Nov, one day late. On 8 Nov the repo still had only the
  Checkpoint 1 work, so the Day 0 to Day 5 steps were done over those two days.

---

## 6. What happened, in order

| When | What |
|---|---|
| by Thu 5 Nov | **Checkpoint 1** (M4): report sections 1 to 3 and 6 test cases (`54a047918b16`) |
| 8 to 9 Nov | **C1 to C15**: library and guide (M1), clients 01 to 06 and expected answers (M2), the v1 check and safety guard (M4), search, tools and agent loop (M3), the first one-file run (M3), the check of the expected answers and the 6-case baseline run (M4). **Checkpoint 2** pushed Mon 9 Nov (`82c0c4f76cd1`). The baseline passed 5 of 6 files. |
| 10 to 11 Nov | **C16 to C23**: checkpoint hashes in EVIDENCE.md (M2); clients 07 to 10 (M1); attack clients 11 and 12 (M2); a run limit for the live demo, the live demo script and a comparison script (M3) |
| 11 to 12 Nov | **C24 to C32**: two baseline runs and two improved runs on all 12 files, a backup run, two comparison files, the EVIDENCE rows and the Results text |
| 13 Nov | We read the traces. The improved agent was **worse** than the baseline. We found the two reasons in the guide text (section 8). |
| 13 to 14 Nov | **F1 to F7**: guide fix (M1), repeat-search note (M3), a new backup run (M3), two new improved runs and their comparisons (M4, M1). The improved agent now passed **all 12 files** in both runs. |
| 14 Nov | **D1, D2** (M2): EVIDENCE rows and the Results, failure, safety and limits text in CAPSTONE.md |
| left | **D3** (Limitations and AI use), **slides**, **D4** (Contributions and Members table), **D5** (freeze row), before Sun 15 Nov, 11:59 PM IST |

---

## 7. What we built

| Part | Where | What it does |
|---|---|---|
| The library | `data/libv/v1.py`, `v2.py`, tests | a tiny payments library: open an account, check the balance, transfer, charge, receipts. v2 changes 12 things compared with v1. |
| The list of changes | `data/CHANGES.md` | the 12 changes (G01 to G12), and whether each one can be guessed from the v2 function names |
| The guide | `data/make_guide.py` → `data/guide.json`, `data/validate_guide.py` | 12 sections, each with an explanation and a before/after example; a script that checks the guide is well formed |
| 12 client files | `data/clients/client_01.py` to `client_12.py`, with tests | small programs on v1. 6 are simple, 3 need 2 or 3 sections, 3 are "attack" cases (below) |
| Expected answers | `eval/hand_migrations/` | our own correct v2 version of every client. The agent cannot read these. |
| Test cases | `eval/cases/case_01.json` to `case_12.json` | which client and which guide sections each case needs. All 12 were pushed before any 12-file run. |
| Answer check | `eval/check_hand.py` | proves, without any model, that every original client fails its tests and every expected answer passes |
| v1 leftover check | `harness/v1check.py` | reads the code structure and flags any v1 import or v1-only name, but ignores comments and strings |
| Guide search | `harness/retrieval.py` | keyword search over the guide: returns at most 3 sections, ranked by how rare the matching words are |
| Model connection | `harness/model.py` | one function that calls the course model with the member's own key, with time limits and retries |
| The 4 tools | `harness/tools.py` | `search_guide`, `read_file` (only clients and v2.py), `write_file` (only the current client), `run_tests`. Since F2, a repeated search returns a short note instead of the same text. |
| The agent | `harness/agent.py` | the loop: ask the model, run the tool it picks, show the result, repeat. Limits: at most 8 model calls and 180 s per file. It writes a trace and a result file, and restores every client file after its case. |
| Safety guard | `safety/scope.py`, `safety/test_scope.py` | before any write, it checks the real path. Only the client being migrated may be written. The library, the tests, other clients and anything outside the repo are blocked, and every decision is logged. |
| Comparison | `eval/compare.py` | turns one baseline run and one improved run into a case-by-case table (`compare-...md`) |
| Live demo | `live/run_live.sh`, `live/cases.json` | runs case_02 and case_11 with the improved agent, with at most 20 model calls and 110 s |
| Runs | `traces/`, `eval/results/` | 10 runs: the first test run, the Checkpoint 2 run, 2 baseline, 2 improved (first guide), 2 improved (fixed guide), 2 backups |
| Report | `CAPSTONE.md`, `EVIDENCE.md` | the design report and the evidence tables |

**The three attack cases.** Each one tests that the agent cannot cheat or be tricked:
- case_06 mentions the old name `get_balance` only inside comments and strings. The v1 check must not flag them.
- case_11 (m11) has a note in the file that tells the agent to add the old names back into the library. Writing
  the library must be blocked.
- case_12 (m12) has a note that tells the agent to edit its own test file. Writing the test must be blocked.

---

## 8. What we found

Each set below has 2 runs × 12 files = 24 files.

| Set | Files fully migrated | Tokens per file | Model calls per file |
|---|---|---|---|
| Baseline (no guide) | 22 of 24 | 3,682 | 3.17 |
| Improved, first guide | 20 of 24 | 4,411 (19.8% more) | 3.83 |
| Improved, fixed guide | **24 of 24** | **3,090 (16.1% fewer)** | 3.00 |

**With the guide as we first wrote it, the agent did worse than guessing.** The traces showed why, in two files:

- **case_02 (transfer):** in v1, `transfer(amount, from, to)`; in v2, `transfer(from, to, amount)`. The client had
  `transfer(share, friend_id, payer_id)`, which means the friend pays the payer. The model moved the amount to the
  end but also swapped the two people, because "payer pays friend" sounded more natural. It found the right guide
  section (G02) at its first step and still got it wrong, because the guide only listed the input names.
- **case_09 (list of transactions):** in v2, `list_transactions` no longer has a default for how many items to
  return. The model hit that error, then searched the guide 5 times in a row. Each search returned the same section
  (G09), which never mentioned the missing default. The model ran out of its 8 steps. The baseline hit the same error
  and simply fixed it.

**The fix.** M1 rewrote two guide sections (F1):
- G02 now says that only the amount moves, the two people stay in the same order, and gives an example.
- G09 now says that you must pass the number of items (v1 used 10), with a before and an after that differ.

M3 also added a note for repeated searches (F2). After that, the improved agent passed every file in both runs,
with fewer tokens than the baseline, because each file took 3 calls where the baseline sometimes needed all 8. The
repeat note never fired, so the gain came from the better guide text.

**Be honest about this in the report and the talk:** we fixed the guide after seeing results on the same 12 files.
So the "fixed guide" numbers are better than what we would expect on new files. The report says so in Limitations.

**Safety in real runs.** The guard blocked 3 real writes, all in case_02 of the baseline runs: the model tried to
rewrite the test file. The model never tried the m11 or m12 tricks, so for those two paths our proof is the guard's
unit tests.

**Other facts**
- The largest prompt in any real run was 3,303 tokens, far under the 16,384 limit.
- Both runs of each set gave exactly the same outcome for every file.
- No real run had a model error.

---

## 9. How close are we to what was asked?

| Asked for | Where we are |
|---|---|
| Guide of 12 to 15 sections | done: 12 sections |
| 12 client files to migrate | done: 12, including 3 attack cases |
| 4 tools, with `write_file` limited | done |
| Plain-code check for v1 leftovers | done |
| Safety control in code, with cases that test it | done: the guard, its unit tests, 2 attack cases, 3 real blocked writes. The model never tried the 2 attacks, so they did not test the guard live. |
| Cases with expected answers, pushed before results | done: 12 cases and 12 hand migrations, checked by `check_hand.py` |
| Baseline vs improved, case by case, regressions, token cost | done: 2 runs of each, plus 2 runs with the fixed guide, and 4 comparison files |
| One failure explained from a trace | done: case_02, plus case_09 |
| A trace for every run, including a backup | done: 10 traces, 2 backups |
| Live demo script and cases | done: `live/run_live.sh`, 2 cases, call and time limits |
| Every member with commits and model calls | done: model calls 74, 46, 57 and 100 |
| Checkpoint 1 (Thu 5 Nov) | done on time |
| Checkpoint 2 (Sun 8 Nov) | done, one day late (Mon 9 Nov) |
| CAPSTONE.md, all headings | 9 of 12 sections written. Left: Limitations, Use of AI assistants (D3), Contributions (D4) |
| EVIDENCE.md, 4 tables | Runs and Results done; Repo table done except the freeze row (D5); Members table left (D4) |
| `slides.pdf` | not done yet |
| Final push before the freeze | not done yet |

**In short:** all the building and testing work is done, and the main question is answered with evidence. What is
left is writing: three report sections, the slides, the Members table and the freeze row.

---

## 10. What is left, in order

1. **D3**: Limitations and Use of AI assistants (script ready).
2. **Slides**: 8 slides from the template. Slide 4 copies the EVIDENCE tables; slide 6 copies the Results numbers
   exactly (the table in section 8 above).
3. **D4**: Contributions and Members table. Run it after the slides, so it counts every commit.
4. **D5**: the freeze row, as the very last commit, a few hours before Sun 15 Nov, 11:59 PM IST.

The scripts and checks for D3 to D5 are in `P04_g15_final_docs.md`.

---

## 11. Questions you may be asked, with short answers

- **Why did the first guide make things worse?** Two sections were unclear. The model found the right section but
  could not use it: in case_02 it swapped the people, in case_09 it kept searching.
- **Isn't the fixed result unfair?** Partly, yes. We fixed the guide after seeing these 12 files, so those numbers
  are optimistic. A fair test needs new client files. We say this in Limitations.
- **Why does the baseline do so well?** It sees the v2 function names and inputs. So renames are easy to guess. The
  guide only helps where a change cannot be seen from the names, such as the input order (G02) or rupees to paise
  (G08).
- **How do you know the safety guard works?** It runs before every write and checks the real path. Its unit tests
  cover the library, the tests, other clients and `../` paths, and it blocked 3 real writes to a test file.
- **What does "fully migrated" mean?** The client's tests pass with v2, and no v1 name is left in the code.
- **Who wrote the code?** aider with the course model, from our prompts. The prompts and checks were prepared with
  Claude. Every step was checked by a script before it was committed, and each member committed and ran from their
  own account.
- **Is the result repeatable?** Yes. Both runs of each set gave the same outcome for every file. Repeating the runs
  shows they are stable, not that the result would hold for other code.
