from libv import v2
import client_01

def test_balance_line():
    acc = v2.open_account("Alice", opening_balance=150.0)
    assert client_01.balance_line(acc) == f"{acc}: 150.00"

def test_is_low():
    acc = v2.open_account("Bob", opening_balance=50.0)
    assert client_01.is_low(acc) is True
    acc = v2.open_account("Charlie", opening_balance=200.0)
    assert client_01.is_low(acc) is False
