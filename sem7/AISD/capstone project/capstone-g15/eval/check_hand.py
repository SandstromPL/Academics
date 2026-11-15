"""Confirms each case before any agent run (plain code, no model):
  base client:   tests FAIL and v1check finds leftovers
  hand migration (eval/hand_migrations/, outside the model's read scope):
                 tests PASS and v1check finds none
Client files are restored afterwards.   Run: python3 eval/check_hand.py
"""


import os
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from harness.agent import load_cases  # noqa: E402
from harness.tools import CaseContext, run_tests  # noqa: E402
from harness.v1check import v1_leftovers  # noqa: E402


def main():
    ok_all = True
    for c in load_cases(os.path.join(ROOT, "eval", "cases")):
        client = os.path.join(ROOT, c["client"])
        hand = os.path.join(ROOT, "eval", "hand_migrations", os.path.basename(c["client"]))
        ctx = CaseContext(c["case_id"], c["client"])
        base_t, base_l = run_tests(ctx)["exit_code"], len(v1_leftovers(client))
        backup = open(client).read()
        try:
            shutil.copy(hand, client)
            hand_t, hand_l = run_tests(ctx)["exit_code"], len(v1_leftovers(client))
        finally:
            open(client, "w").write(backup)
        ok = base_t != 0 and base_l > 0 and hand_t == 0 and hand_l == 0
        ok_all &= ok
        print(f"{c['case_id']} {c['client']}: base tests_exit={base_t} leftovers={base_l} | "
              f"hand tests_exit={hand_t} leftovers={hand_l} | needed={c['needed']} -> {'OK' if ok else 'PROBLEM'}")
    print("ALL OK" if ok_all else "SOME CASES HAVE PROBLEMS")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
