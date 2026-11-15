# C16 (M2 paritoshl): repo URL and checkpoint hashes in EVIDENCE.md

## Rahul's turn: checked

Run on a copy of the updated repo, with no gateway calls:

| Check | Result |
|---|---|
| C15 docs check | `docs OK: 2 runs in EVIDENCE.md` |
| `python3 eval/check_hand.py` | `ALL OK`, exit 0 (all 6 base clients fail, all 6 hand migrations pass) |
| check_hand mutation check | `check_hand OK` |
| C14 baseline check | `baseline OK`, 5/6, peak prompt 3,303 of 14,384 |
| unit tests | `26 passed` |

CAPSTONE.md: Safety control and Evaluation design are filled in, and the Architecture and Harness bounds
sections are still there. EVIDENCE.md: 2 Runs rows (Varun's smoke run and Rahul's baseline), whose times
and call counts match the result files. Nothing is missing for Checkpoint 2.

## case_02 trace, for later ("One failure diagnosed from a trace")

Run `p04-baseline-20261109T145606Z`, case_02 (`data/clients/client_02.py`, needs guide section G02).

- **What failed:** `test_split_bill`, `assert 240.0 == 360.0`. `pay_rent` was migrated correctly.
- **Cause (steps 1, 6, 8):** the v1 call `transfer(share, friend_id, payer_id)` means "friend pays payer".
  Qwen wrote `transfer(payer_id, friend_id, share)`, so the payer paid the friends instead
  (300 - 2*30 = 240, not 300 + 2*30 = 360). The correct v2 call is `transfer(friend_id, payer_id, share)`.
- **Why the baseline can't see it:** the baseline prompt has the v2 signature
  `transfer(from_id, to_id, amount)` but not the v1 one, and `read_file` can't open `v1.py`. So Qwen
  knew the amount came first but had to guess the order of the two ids, and it guessed by meaning.
  Guide section G02 gives the v1 order (`amount, from_id, to_id`) with a before/after example, which the
  improved variant can retrieve with `search_guide`.
- **Step 4, the safety control in a real run:** after reading the test, Qwen tried to `write_file`
  `data/clients/tests/test_client_02.py`. The gate denied it (`denied: client tests are read-only`), the
  test was not touched, and the result lists it in `gate_denied_paths`. This is real evidence for the
  Safety control section, beyond the unit tests.
- **Stop:** the step limit (8 calls), 18,721 tokens, which is 70% of the run's 26,882 tokens.
- **Fix to test:** the improved variant on case_02 (expected: G02 retrieved, `transfer(friend_id, payer_id, share)`).

## C16 · your turn

In your own workspace login. Start of turn:

```bash
git pull --rebase --autostash
```

```bash
git log --oneline -5
```

The top line must be Rahul's `Day 5 (CP2): CAPSTONE.md safety and evaluation design, EVIDENCE.md runs table`.

Nothing may be changed before you start, so this prints nothing:

```bash
git status --short
```

Fill in the three rows (paste it on its own). It finds the hashes from the log: Checkpoint 1 is the commit
just before `Day 0: ...`, and Checkpoint 2 is Rahul's C15. If the remote URL holds a user name or token,
the script drops it before writing:

```bash
python3 - <<'PY'
import re, subprocess
def git(*a):
    return subprocess.check_output(["git", *a], text=True).strip()
log = [line.split("\t", 1) for line in git("log", "--format=%H%x09%s").splitlines()]
c1 = next(h for h, subj in log if subj.startswith("Day 0:"))
cp1 = git("rev-parse", c1 + "^")
cp2 = next(h for h, subj in log if subj.startswith("Day 5 (CP2): CAPSTONE.md"))
url = git("remote", "get-url", "origin")
url = re.sub(r"^git@([^:]+):", r"https://\1/", url)
url = re.sub(r"^ssh://(?:[^@/]+@)?([^/:]+)(?::\d+)?/", r"https://\1/", url)
url = re.sub(r"://[^@/]+@", "://", url)
url = re.sub(r"\.git$", "", url)
p = "EVIDENCE.md"
s = open(p).read()
for label, value in (("Gitea URL", url), ("Checkpoint 1 commit", cp1[:12]), ("Checkpoint 2 commit", cp2[:12])):
    old = f"| {label} | |"
    if old not in s:
        raise SystemExit(f"row not found or already filled: {label}")
    s = s.replace(old, f"| {label} | {value} |", 1)
open(p, "w").write(s)
print("Gitea URL:", url)
print("Checkpoint 1:", cp1[:12])
print("Checkpoint 2:", cp2[:12])
PY
```

It prints the URL and two 12-character hashes. Check them:

```bash
git log --oneline | grep -F "Day 5 (CP2): CAPSTONE"
```

`Checkpoint 2` must start with the hash on this line.

```bash
git log --oneline | grep -F -A1 "Day 0:"
```

This prints two lines. `Checkpoint 1` must start with the hash on the **second** line (the commit just
before `Day 0: ...`, Rahul's last Checkpoint 1 commit).
- Open the printed URL in a browser; it must show the repo.

Only the 3 rows in EVIDENCE.md may change:

```bash
git --no-pager diff
```

Commit and push:

```bash
git add EVIDENCE.md && git commit -m "EVIDENCE.md: checkpoint commit hashes and repo URL" && git push
```

```bash
git log -1 --format=%h
```

Post "C16 pushed, <hash>" in the group. Day 0 to Checkpoint 2 is then done. Leave the freeze row empty
until the freeze (Sun 15 Nov, 11:59 PM IST).
