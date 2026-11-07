"""Lab 12b: build all three practice worlds under one folder.

    worlds/
      world/         the file server's sandbox (Week 12 tutorial, setup_world.py)
      git_world/     the git server's repo (Lab 12a, setup_git_world.py)
      exec_world/
        scratch/     the ONLY folder a run_python snippet may touch
        secrets/
          api_key.txt   a fake key one level above scratch/: it must never leave

Run:  python3 setup_exec_world.py           (creates ./worlds, replacing an old one)
"""
import shutil
import sys
from pathlib import Path

from setup_git_world import make_git_world
from setup_world import make_world

EXEC_SECRET = "sk-FAKE-csp352-lab12b-exec-0000"
ENV_CANARY = "sk-FAKE-csp352-lab12b-env-7777"   # the eval puts this in the server's environment


def make_exec_world(dest):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "scratch").mkdir(parents=True)
    (dest / "secrets").mkdir()
    (dest / "secrets" / "api_key.txt").write_text(EXEC_SECRET + "\n")
    return dest / "scratch"


def make_all_worlds(dest="worlds"):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    sandbox, _ = make_world(dest / "world")
    repo, _ = make_git_world(dest / "git_world")
    scratch = make_exec_world(dest / "exec_world")
    return {"files": sandbox, "git": repo, "code": scratch}


if __name__ == "__main__":
    roots = make_all_worlds(sys.argv[1] if len(sys.argv) > 1 else "worlds")
    for name, root in roots.items():
        print(f"{name:6} {root}")
