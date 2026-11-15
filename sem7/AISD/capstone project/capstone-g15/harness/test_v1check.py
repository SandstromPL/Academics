import glob
import os

from harness.v1check import ROOT, V1_ONLY, v1_leftovers


def _write(tmp_path, src):
    p = tmp_path / "c.py"
    p.write_text(src)
    return str(p)


def test_v1_only_list():
    assert {"get_balance", "charge_and_receipt", "InsufficientFunds",
            "AccountNotFound", "PaymentError"} <= V1_ONLY
    assert "transfer" not in V1_ONLY and "withdraw" not in V1_ONLY


def test_every_base_client_has_leftovers():
    clients = sorted(glob.glob(os.path.join(ROOT, "data", "clients", "*.py")))
    assert clients
    for c in clients:
        assert v1_leftovers(c), c


def test_every_hand_migration_is_clean():
    for c in sorted(glob.glob(os.path.join(ROOT, "eval", "hand_migrations", "*.py"))):
        assert v1_leftovers(c) == [], c


def test_comments_and_strings_are_not_flagged(tmp_path):
    p = _write(tmp_path, '# get_balance(x) was v1\nX = "InsufficientFunds"\nD = {"get_balance": 1}\n')
    assert v1_leftovers(p) == []


def test_import_forms(tmp_path):
    assert v1_leftovers(_write(tmp_path, "import libv.v1\n"))
    assert v1_leftovers(_write(tmp_path, "from libv import v1\n"))
    assert v1_leftovers(_write(tmp_path, "from libv.v1 import withdraw\n"))


def test_local_shim_is_flagged(tmp_path):
    src = "from libv.v2 import fetch_balance\n\ndef get_balance(a):\n    return fetch_balance(a)\n"
    assert {"line": 3, "name": "get_balance"} in v1_leftovers(_write(tmp_path, src))
    src2 = "from libv.v2 import fetch_balance\nget_balance = fetch_balance\n"
    assert v1_leftovers(_write(tmp_path, src2))


def test_alias_and_attribute(tmp_path):
    assert v1_leftovers(_write(tmp_path, "from libv.v2 import fetch_balance as get_balance\n"))
    assert v1_leftovers(_write(tmp_path, "import libv.v2 as lib\nlib.get_balance('a')\n"))


def test_many_hits_sorted_and_deduplicated(tmp_path):
    src = "from libv.v1 import get_balance\nx = get_balance('a')\ny = (get_balance, get_balance)\n"
    assert v1_leftovers(_write(tmp_path, src)) == [
        {"line": 1, "name": "libv.v1"}, {"line": 2, "name": "get_balance"}, {"line": 3, "name": "get_balance"}]
