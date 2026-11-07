"""Lab 12b, Part A: the code-execution server's tool. YOUR WORK GOES HERE.

run_python runs a snippet of Python in its own process, in a scratch
directory, with four kinds of limit:
  - time:        a wall-clock limit, after which the whole process group is killed
  - resources:   CPU, memory, file size and open files (the resource module)
  - environment: only PATH, HOME and LANG reach the snippet (no API keys)
  - an audit hook, installed before the snippet runs, that refuses sockets,
    new processes, loading C libraries, and files outside the scratch directory

Registry shape as file_tools.py and git_tools.py. exec_server.py serves it.
Read README.md, Part A, for each task's contract. Check progress with:
    python3 lab12b.py check
"""
import os
import signal  # noqa: F401  -- for killing the process group (A1)
import subprocess  # noqa: F401
import sys  # noqa: F401
from pathlib import Path

from guard import GuardError

WALL_TIMEOUT_S = 5
CPU_SECONDS = 2
MEMORY_BYTES = 256 * 1024 * 1024
FILE_BYTES = 1 * 1024 * 1024
OPEN_FILES = 64
MAX_CODE_CHARS = 10000
MAX_OUTPUT_CHARS = 4000

# The audit events your hook must refuse (A3). Each is raised by Python just
# before the action happens, with the action's arguments.
BLOCKED_EVENTS = (
    "socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg",
    "subprocess.Popen", "os.system", "os.fork", "os.forkpty", "os.posix_spawn",
    "os.exec", "os.spawn", "ctypes.dlopen", "ctypes.dlsym",
)
# Audit events that change the file system, and which of their arguments are
# paths: every such path must be inside the scratch folder.
PATH_EVENTS = {
    "os.rename": (0, 1), "os.link": (0, 1), "os.symlink": (1,), "os.remove": (0,),
    "os.rmdir": (0,), "os.mkdir": (0,), "os.chmod": (0,), "os.chown": (0,),
    "os.truncate": (0,), "os.utime": (0,),
}



class SandboxError(GuardError):
    """Input the server refuses. The message goes back to the model."""


# --------------------------------------------------------------------- A4
def check_code(code):
    """Return code if it is a string that is not empty or only whitespace,
    has no NUL character ("\\x00": subprocess cannot pass one) and is at
    most MAX_CODE_CHARS characters; else raise SandboxError."""
    raise SandboxError("check_code not implemented yet (task A4)")


# --------------------------------------------------------------------- A3
def audit_prelude(scratch):
    """Return Python SOURCE (a string) that, run before the snippet in the
    same process, installs an audit hook (sys.addaudithook) which raises
    PermissionError for:
      - every event in BLOCKED_EVENTS;
      - every event in PATH_EVENTS whose path arguments (the listed indexes)
        are not inside `scratch` (rename, remove, mkdir, symlink, chmod...:
        without this, os.rename('../secrets/x', 'x') moves a secret in);
        resolve the FOLDER with os.path.realpath and keep the last name as
        it is (it may be a link you are allowed to remove);
      - the "open" event (args: path, mode, flags) for any path whose
        os.path.realpath is outside `scratch`, EXCEPT a read-only open under
        Python's own sys.base_prefix / sys.prefix / sys.exec_prefix
        (imports need those), and /dev/null, /dev/urandom. Read-only means:
        mode (a str, or None for os.open) has none of "w", "a", "x", "+",
        and flags (an int) has none of O_WRONLY, O_RDWR, O_CREAT.
      A path can be str, bytes, or an int (an already open file: allow).
    Two traps, both real escapes:
      - compare with `scratch + os.sep`, not just `scratch`: ".../s" is a
        string prefix of ".../sec.txt";
      - the snippet runs AFTER your hook and can replace os.path.realpath
        or any global your hook reads. Bind everything the hook uses when
        it is installed (default arguments do this), never look it up later.
    Use repr() to put `scratch` and the event lists into the source, and
    del the hook function afterwards so the snippet cannot reach it.
    Error line numbers count the prelude's lines too.
    """
    return ""


# --------------------------------------------------------------------- A2
def make_limits():
    """Return a function for subprocess's preexec_fn (it runs in the child,
    just before the snippet starts) that sets, with resource.setrlimit,
    soft and hard limits:
        RLIMIT_CPU    = CPU_SECONDS
        RLIMIT_AS     = MEMORY_BYTES
        RLIMIT_FSIZE  = FILE_BYTES
        RLIMIT_NOFILE = OPEN_FILES
    If a limit already has a lower hard value, setrlimit refuses a higher
    one: use min(value, current hard) unless hard is RLIM_INFINITY.
    (Why not RLIMIT_NPROC: see README, A2.)"""
    def set_limits():
        pass
    return set_limits


# --------------------------------------------------------------------- A1
def run_sandboxed(code, scratch):
    """Run `code` under every limit and return
        {"stdout", "stderr", "exit_code", "timed_out", "truncated"}.
    - check_code(code) first (its SandboxError may propagate: call_tool
      turns it into a refusal);
    - create scratch if needed; run [sys.executable, "-I", "-c",
      audit_prelude(scratch) + "\\n" + code] with cwd=scratch, an
      environment of ONLY PATH=/usr/bin:/bin, HOME=<scratch, absolute>,
      LANG=C.UTF-8, stdin from /dev/null, start_new_session=True,
      preexec_fn=make_limits();
    - wait at most WALL_TIMEOUT_S; on timeout kill the whole process group
      (os.killpg(pid, signal.SIGKILL)) and set timed_out True;
    - cut stdout and stderr at MAX_OUTPUT_CHARS each (truncated True if cut);
    - never raise for anything the snippet does.
    """
    return {"stdout": "", "stderr": "run_sandboxed not implemented yet (task A1)",
            "exit_code": None, "timed_out": False, "truncated": False}


def build_registry(scratch):
    scratch = Path(scratch)

    def run_python(code):
        return run_sandboxed(code, scratch)

    return {
        "run_python": {
            "fn": run_python,
            "description": ("Run a short Python 3 program in a sandbox and return its stdout, "
                            "stderr and exit code. No network, no other processes, files only in "
                            "the sandbox's own folder, at most 5 seconds."),
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string", "description": "The Python source to run."}},
                "required": ["code"],
            },
            "permission": "execute",
        },
    }
