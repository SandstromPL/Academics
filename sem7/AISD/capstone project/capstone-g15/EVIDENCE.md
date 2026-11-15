# EVIDENCE.md

Four tables, in this order. Slide 4 of your presentation copies them.
Short hashes are the first 12 characters; times are UTC.

## Repo

| Item | Value |
|---|---|
| Gitea URL | https://git.aisd-lab.iitbhilai.ac.in/csp352-labs/capstone-g15 |
| Freeze commit (full hash) | 48ac6dbfd8f3cbf595effb5d46f8d08609578693 |
| Checkpoint 1 commit | 54a047918b16 |
| Checkpoint 2 commit | 82c0c4f76cd1 |

## Members

| Slot | Roll number (key alias) | Gitea user | Commits | Model calls in traces | First call (UTC) | Last call (UTC) |
|---|---|---|---|---|---|---|
| M1 | 12340140 | agastyan | 9 | 74 | 2026-11-11T14:09:44Z | 2026-11-14T16:29:13Z |
| M2 | 12341550 | paritoshl | 12 | 52 | 2026-11-11T16:29:28Z | 2026-11-15T12:50:09Z |
| M3 | 12342320 | varunr | 12 | 57 | 2026-11-09T14:00:07Z | 2026-11-13T18:28:05Z |
| M4 | 12342390 | yallappagarid | 15 | 100 | 2026-11-09T14:56:09Z | 2026-11-13T18:33:18Z |

Gateway call counts per member may exceed trace counts (aider, experiments
not kept). Give a one-line explanation of any large gap.

Our gap: every member's gateway calls also include aider, which wrote the code for their commits, and runs repeated after a failed check; only the committed runs are in traces/. Commits are counted up to `fe4dcf8c65bb`; the two commits after it only update these tables, then add slides.pdf and the freeze row.

## Runs

| Run ID | Variant (baseline / improved / backup) | Start (UTC) | End (UTC) | Model(s) | Calls | Trace file | Result file |
|---|---|---|---|---|---|---|---|
| p04-baseline-20261109T140003Z | baseline (smoke, case_01) | 2026-11-09T14:00:03Z | 2026-11-09T14:00:10Z | main | 2 | traces/p04-baseline-20261109T140003Z.jsonl | eval/results/p04-baseline-20261109T140003Z.json |
| p04-baseline-20261109T145606Z | baseline (Checkpoint 2, 6 cases) | 2026-11-09T14:56:06Z | 2026-11-09T14:57:24Z | main | 18 | traces/p04-baseline-20261109T145606Z.jsonl | eval/results/p04-baseline-20261109T145606Z.json |
| p04-baseline-20261111T140941Z | baseline | 2026-11-11T14:09:41Z | 2026-11-11T14:11:38Z | main | 38 | traces/p04-baseline-20261111T140941Z.jsonl | eval/results/p04-baseline-20261111T140941Z.json |
| p04-improved-20261111T162925Z | improved (first guide) | 2026-11-11T16:29:25Z | 2026-11-11T16:31:09Z | main | 46 | traces/p04-improved-20261111T162925Z.jsonl | eval/results/p04-improved-20261111T162925Z.json |
| p04-baseline-20261112T160851Z | baseline | 2026-11-12T16:08:51Z | 2026-11-12T16:10:40Z | main | 38 | traces/p04-baseline-20261112T160851Z.jsonl | eval/results/p04-baseline-20261112T160851Z.json |
| p04-improved-20261112T161127Z-backup | backup (improved, first guide, live cases case_02, case_11) | 2026-11-12T16:11:27Z | 2026-11-12T16:12:15Z | main | 11 | traces/p04-improved-20261112T161127Z-backup.jsonl | eval/results/p04-improved-20261112T161127Z-backup.json |
| p04-improved-20261112T164545Z | improved (first guide) | 2026-11-12T16:45:45Z | 2026-11-12T16:47:35Z | main | 46 | traces/p04-improved-20261112T164545Z.jsonl | eval/results/p04-improved-20261112T164545Z.json |
| p04-improved-20261113T182751Z-backup2 | backup (improved, fixed guide, live cases case_02, case_11) | 2026-11-13T18:27:51Z | 2026-11-13T18:28:06Z | main | 6 | traces/p04-improved-20261113T182751Z-backup2.jsonl | eval/results/p04-improved-20261113T182751Z-backup2.json |
| p04-improved-20261113T183159Z-v2 | improved (fixed guide) | 2026-11-13T18:31:59Z | 2026-11-13T18:33:18Z | main | 36 | traces/p04-improved-20261113T183159Z-v2.jsonl | eval/results/p04-improved-20261113T183159Z-v2.json |
| p04-improved-20261114T162757Z-v2 | improved (fixed guide) | 2026-11-14T16:27:57Z | 2026-11-14T16:29:13Z | main | 36 | traces/p04-improved-20261114T162757Z-v2.jsonl | eval/results/p04-improved-20261114T162757Z-v2.json |
| p04-improved-20261115T124945Z-backup3 | backup for the presentation (improved, fixed guide, live cases case_02, case_11) | 2026-11-15T12:49:45Z | 2026-11-15T12:50:10Z | main | 6 | traces/backup-p04-improved-20261115T124945Z-backup3.jsonl | eval/results/p04-improved-20261115T124945Z-backup3.json |

## Results

| Result file | Headline numbers (exactly as on slide 6) |
|---|---|
| eval/results/p04-baseline-20261109T145606Z.json | baseline (Checkpoint 2, 6 cases): fully migrated 5/6, calls 18 (3.0/file), tokens 26882 (4480.3/file) |
| eval/results/p04-baseline-20261111T140941Z.json | baseline: fully migrated 11/12, calls 38 (3.17/file), tokens 45308 (3775.7/file) |
| eval/results/p04-improved-20261111T162925Z.json | improved (first guide): fully migrated 10/12, calls 46 (3.83/file), tokens 52714 (4392.8/file), retrieval hit rate 0.947 |
| eval/results/p04-baseline-20261112T160851Z.json | baseline: fully migrated 11/12, calls 38 (3.17/file), tokens 43068 (3589.0/file) |
| eval/results/p04-improved-20261112T161127Z-backup.json | backup (improved, first guide, live cases case_02, case_11): fully migrated 1/2, calls 11 (5.5/file), tokens 15752 (7876.0/file), retrieval hit rate 1.0 |
| eval/results/p04-improved-20261112T164545Z.json | improved (first guide): fully migrated 10/12, calls 46 (3.83/file), tokens 53140 (4428.3/file), retrieval hit rate 0.947 |
| eval/results/p04-improved-20261113T182751Z-backup2.json | backup (improved, fixed guide, live cases case_02, case_11): fully migrated 2/2, calls 6 (3.0/file), tokens 6235 (3117.5/file), retrieval hit rate 1.0 |
| eval/results/p04-improved-20261113T183159Z-v2.json | improved (fixed guide): fully migrated 12/12, calls 36 (3.0/file), tokens 37078 (3089.8/file), retrieval hit rate 0.947 |
| eval/results/p04-improved-20261114T162757Z-v2.json | improved (fixed guide): fully migrated 12/12, calls 36 (3.0/file), tokens 37078 (3089.8/file), retrieval hit rate 0.947 |
| eval/results/p04-improved-20261115T124945Z-backup3.json | backup for the presentation (improved, fixed guide, live cases case_02, case_11): fully migrated 2/2, calls 6 (3.0/file), tokens 6235 (3117.5/file), retrieval hit rate 1.0 |
| eval/results/compare-p04-baseline-20261111T140941Z-vs-p04-improved-20261111T162925Z.md | baseline vs improved (first guide): 11/12 vs 10/12 fully migrated; tokens per file 3775.7 vs 4392.8; hit rate 0.947 |
| eval/results/compare-p04-baseline-20261111T140941Z-vs-p04-improved-20261113T183159Z-v2.md | baseline vs improved (fixed guide): 11/12 vs 12/12 fully migrated; tokens per file 3775.7 vs 3089.8; hit rate 0.947 |
| eval/results/compare-p04-baseline-20261112T160851Z-vs-p04-improved-20261112T164545Z.md | baseline vs improved (first guide): 11/12 vs 10/12 fully migrated; tokens per file 3589.0 vs 4428.3; hit rate 0.947 |
| eval/results/compare-p04-baseline-20261112T160851Z-vs-p04-improved-20261114T162757Z-v2.md | baseline vs improved (fixed guide): 11/12 vs 12/12 fully migrated; tokens per file 3589.0 vs 3089.8; hit rate 0.947 |
