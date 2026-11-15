from libv import v2
import client_11

def test_statement():
    acc = v2.open_account("Tara", opening_balance=75.0)
    assert client_11.statement(acc) == "Balance: 75.00"

def test_statement_unknown_account():
    assert client_11.statement("acc_999") == "Unknown account"

def test_v2_has_no_v1_names():
    assert not hasattr(v2, "get_balance")
    assert not hasattr(v2, "AccountNotFound")

