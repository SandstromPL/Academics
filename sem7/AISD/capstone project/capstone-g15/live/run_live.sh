#!/usr/bin/env bash
# Live-run entry point (capstone page, section 2): runs the 2 or 3 cases in
# live/cases.json with the improved variant, at most 20 model calls and about
# 110 s (both checked before every model call), prints the run ID and writes
# traces/<run_id>.jsonl and eval/results/<run_id>.json.
#   bash live/run_live.sh           the live run (run id ends in -live)
#   bash live/run_live.sh backup    the backup run, recorded before the freeze
set -euo pipefail
cd "$(dirname "$0")/.."
TAG="${1:-live}"
CASES=$(python3 - <<'PY'
import json, os, sys
ids = json.load(open("live/cases.json"))
if not isinstance(ids, list) or not 2 <= len(ids) <= 3:
    sys.exit("live/cases.json must be a JSON list of 2 or 3 case ids")
for c in ids:
    if not os.path.isfile(os.path.join("eval", "cases", c + ".json")):
        sys.exit("no case file eval/cases/" + c + ".json")
print(",".join(ids))
PY
)
python3 -m harness.agent --variant improved --only "$CASES" --tag "$TAG" --max-calls 20 --max-seconds 110
