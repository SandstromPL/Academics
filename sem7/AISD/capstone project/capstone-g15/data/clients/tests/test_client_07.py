from libv import v2
import client_07

def test_safe_withdraw_ok():
    acc = v2.open_account("Liam", opening_balance=100.0)
    assert client_07.safe_withdraw(acc, 40.0) == "ok"
    assert v2.fetch_balance(acc) == 60.0

def test_safe_withdraw_unknown_account():
    assert client_07.safe_withdraw("acc_999", 10.0) == "no such account"

def test_safe_withdraw_too_much():
    acc = v2.open_account("Mia", opening_balance=20.0)
    assert client_07.safe_withdraw(acc, 50.0) == "payment failed"
    assert v2.fetch_balance(acc) == 20.0
