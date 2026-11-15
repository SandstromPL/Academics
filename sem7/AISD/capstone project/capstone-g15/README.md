# capstone-g15 -- P04 API migration assistant with a retrieved guide

CSP352 AI-Augmented Software Development, capstone. Group **g15**
(GREP).

Members (Gitea users; each pushes from their own account and uses only their own gateway key):
- M1: `agastyan`
- M2: `paritoshl`
- M3: `varunr`
- M4: `yallappagarid`

- Your project's full handout and all rules: the capstone page, https://lab.aisd-lab.iitbhilai.ac.in/capstone/ (the lab homepage, section Capstone Project)
  (direct link: https://lab.aisd-lab.iitbhilai.ac.in/capstone/#P04).
- Freeze: **Sunday 15 November 2026, 11:59 PM IST.** The last push before
  the freeze, read from the Gitea push log, is your submission.
- Checkpoint 1 (Thu 5 Nov): CAPSTONE.md sections 1-3 and 6+ eval cases in
  `eval/cases/`. Checkpoint 2 (Sun 8 Nov): harness end to end, one baseline
  result and its trace.

Keep this layout (the evaluators and the evidence script look here):

    CAPSTONE.md     design report, fixed headings
    EVIDENCE.md     evidence tables, fixed format
    slides.pdf      8 slides from the presentation template (add before the freeze)
    harness/        runtime harness, tools, trace logger
    safety/         the code-enforced control(s)
    eval/cases/     cases with expected answers -- push BEFORE any results
    eval/results/   <run_id>.json per run, compare-<base>-vs-<improved>.md
    traces/         <run_id>.jsonl, one per run; the presentation backup is backup-<run_id>.jsonl
    data/           synthetic data and the script that made it
    live/run_live.sh  live-run entry point (run it as: bash live/run_live.sh)
    live/cases.json   the 2 or 3 cases the live run uses

Lab only: your course workspace, this Gitea repo, and the gateway models
`main` and `aux`. Every model call and every commit is tracked and checked
against each other.
