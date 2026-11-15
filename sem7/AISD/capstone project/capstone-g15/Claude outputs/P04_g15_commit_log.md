# P04 / g15 commit log (copied from the Gitea commit page, 15 Nov 2026)

The local copy of the repo has no `.git`, so this is the record I work from. Hashes are the 10-character ones Gitea
shows. 12-character ones known from EVIDENCE.md or the zip: CP1 `54a047918b16`, CP2 `82c0c4f76cd1`,
`4936dbd75ce3` (the zip of main before D1).

Members: M1 agastyan (12340140), M2 paritoshl (12341550), M3 varunr (12342320), M4 yallappagarid (12342390).

## Oldest first

| # | Hash | Author | Message | Note |
|---|---|---|---|---|
| 1 | 15ca0d5422 | yallappagarid | feat: add 6 eval case files with expected answers (message has more lines) | |
| 2 | 54a047918b | yallappagarid | check_point | **CP1** |
| 3 | 4e9be9a3bf | agastyan | Day 0: v1->v2 breaking change list (G01-G12) | |
| 4 | abf255edaf | agastyan | Day 1: libv v1 and v2 APIs with v2 unit tests | |
| 5 | 7418dcd0cc | agastyan | Day 1: migration guide (12 sections) + validator | |
| 6 | 31c9057025 | paritoshl | Day 2: 6 v1 client modules with v2 tests (cases 01-06) | |
| 7 | 8d5236647c | paritoshl | Day 2: hand migrations for clients 01-06 (expected answers) | |
| 8 | d5437f8bea | yallappagarid | Day 3: AST v1 leftover check (flags v1 imports and v1-only names incl. shims) | |
| 9 | f88e0826b4 | yallappagarid | Day 3: write_file scope guard with gate records | safety control |
| 10 | 852d016ea9 | varunr | Day 3: keyword retrieval over guide.json (k<=3, IDF, hit_rate) | |
| 11 | 252300db43 | varunr | Day 3: gateway client and tool registry (search_guide, read_file, scoped write_file, run_tests) | |
| 12 | e30280555c | varunr | Day 4: agent loop with step limit, trace and result writer | |
| 13 | 6ca6fd6c6e | varunr | Day 4: baseline smoke run on case_01 (run p04-baseline-20261109T140003Z) | |
| 14 | d873cd4677 | varunr | Day 4: CAPSTONE.md architecture and harness bounds | |
| 15 | df98b01be8 | yallappagarid | Day 5: check expected answers (base fails, hand migration passes) before runs | |
| 16 | 497e1c3fcd | yallappagarid | Day 5 (CP2): baseline run p04-baseline-20261109T145606Z on 6 cases, result and trace | |
| 17 | 82c0c4f76c | yallappagarid | Day 5 (CP2): CAPSTONE.md safety and evaluation design, EVIDENCE.md runs table | **CP2** |
| 18 | 555b2e0bcc | paritoshl | EVIDENCE.md: checkpoint commit hashes and repo URL | |
| 19 | 9a0669e835 | agastyan | Day 6: clients 07-10 with v2 tests (G03, G06-G12) | |
| 20 | 16227096d9 | agastyan | Day 6: hand migrations and cases 07-10 (expected answers) | **cases 07-10** |
| 21 | c7c5f0dd91 | paritoshl | Day 6: adversarial clients 11-12 (m11 edit v2.py, m12 edit the test) with v2 tests | |
| 22 | 21399d3b9b | paritoshl | Day 6: hand migrations and cases 11-12; CAPSTONE.md adversarial cases | **cases 11-12** |
| 23 | 64c6b36371 | varunr | Day 7: run budget for the live run (--max-calls, --max-seconds) | |
| 24 | 2fe5da72a7 | varunr | Day 7: live run entry point (live/run_live.sh, live/cases.json) | |
| 25 | 3fa19a0713 | varunr | Day 7: eval/compare.py, baseline vs improved case by case | |
| 26 | 7af1666a9e | agastyan | Day 7: baseline run p04-baseline-20261111T140941Z on 12 cases | first run on 12 cases |
| 27 | 6326e21c85 | paritoshl | Day 7: improved run p04-improved-20261111T162925Z on 12 cases | |
| 28 | 9544806655 | paritoshl | Day 7: compare baseline vs improved, round 1 | |
| 29 | b5813f8990 | varunr | Day 8: baseline run p04-baseline-20261112T160851Z on 12 cases (round 2) | |
| 30 | adff968bcf | varunr | Day 8: backup run p04-improved-20261112T161127Z-backup of the live cases | first backup |
| 31 | 023006c3a4 | yallappagarid | Day 8: improved run p04-improved-20261112T164545Z on 12 cases (round 2) | |
| 32 | e4080b6807 | yallappagarid | Day 8: compare baseline vs improved, round 2 | |
| 33 | 2e4c4bbb0b | yallappagarid | Day 8: EVIDENCE.md runs and results rows | |
| 34 | ce224b70fa | yallappagarid | Day 8: CAPSTONE.md results and one failure diagnosed from a trace | |
| 35 | 3e178a5e0b | yallappagarid | Day 9: CAPSTONE.md limitations and use of AI assistants | reverted by #36 |
| 36 | aa421981de | yallappagarid | Revert "Day 9: CAPSTONE.md limitations and use of AI assistants" | |
| 37 | 8cc69d465f | agastyan | Day 9: guide G02 and G09 rewritten after the case_02 and case_09 traces | **F1** |
| 38 | f140d24cad | varunr | Day 9: search_guide says when it has no new sections (stops search loops) | **F2** |
| 39 | 2709969a60 | varunr | Day 9: backup run p04-improved-20261113T182751Z-backup2 of the live cases (fixed guide) | backup2 |
| 40 | 04281db1a0 | yallappagarid | Day 9: improved run p04-improved-20261113T183159Z-v2 on 12 cases (fixed guide, round 1) | |
| 41 | 1b570d1b90 | yallappagarid | Day 9: compare baseline round 1 vs fixed improved round 1 | |
| 42 | f6a07374c8 | agastyan | Day 10: improved run p04-improved-20261114T162757Z-v2 on 12 cases (fixed guide, round 2) | |
| 43 | 4936dbd75c | agastyan | Day 10: compare baseline round 2 vs fixed improved round 2 | zip I verified |
| 44 | 548a4e7dce | paritoshl | Day 10: EVIDENCE.md runs and results rows for all runs, with guide labels | D1 |
| 45 | be9b83b09e | paritoshl | Day 10: CAPSTONE.md results with the fixed guide, failure diagnosis, safety and bounds from the real runs | D2 |
| 46 | 4838484632 | paritoshl | Day 10: CAPSTONE.md limitations and use of AI assistants | D3, HEAD on 15 Nov |

## Counts up to D3 (`4838484632`)

| Slot | Gitea user | Commits |
|---|---|---|
| M1 | agastyan | 9 |
| M2 | paritoshl | 10 |
| M3 | varunr | 12 |
| M4 | yallappagarid | 15 |
| | total | 46 |

These assume `15ca0d5422` is the oldest commit (the screenshots end there). D4's Members table counts from the real
`git log` and is the one to trust; if it gives different numbers, the slide must be changed to match.

## After the screenshots

| 47 | 95c6dafd6d | paritoshl | Day 10: CAPSTONE.md contributions, EVIDENCE.md members table | D4 (counts 9 / 10 / 12 / 15 up to D3) |

Gitea says 60 commits: the 47 above plus 13 "Capstone starter" commits from the course.

## Still to come (old plan, replaced by P04_g15_backup_and_freeze.md)

- D4 (paritoshl): Contributions and Members table. It counts commits up to the HEAD it runs on (D3), so 9 / 10 / 12 / 15.
- Last commit (paritoshl): slides.pdf and the D5 freeze row together. The freeze row and slide 4 both carry the D4 hash.
