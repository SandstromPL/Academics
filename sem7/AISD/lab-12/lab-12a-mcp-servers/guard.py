"""Step 5: the path guard and the permission check, enforced in the server.

Both run in code, outside the model, on every call (Week 11: the model
proposes, code decides). The permission message is Lab 5b's, word for word.
"""
from pathlib import Path


class GuardError(Exception):
    """A call the server refuses. The message goes back to the model."""


def resolve_in_root(root, user_path):
    """Return the real path for user_path, or raise GuardError if it is
    outside root.

    resolve() turns "a/../../b" into a real absolute path and follows
    symlinks, so "..", absolute paths and a symlink that points out of the
    sandbox are all caught by one comparison. Checking the string for ".."
    catches only the first of the three.
    """
    if not isinstance(user_path, str) or not user_path.strip():
        raise GuardError("path must be a non-empty string")
    if "\x00" in user_path:
        raise GuardError("path contains a NUL byte")
    root = Path(root).resolve()
    candidate = (root / user_path).resolve()  # an absolute user_path replaces root here
    if candidate != root and not candidate.is_relative_to(root):
        raise GuardError(f"path outside the sandbox: {user_path}")
    return candidate


def check_permission(name, spec, granted):
    """Lab 5b's check: None if allowed, else the denial message."""
    needed = spec["permission"]
    if needed not in granted:
        return f"permission denied: '{name}' requires '{needed}' permission"
    return None
