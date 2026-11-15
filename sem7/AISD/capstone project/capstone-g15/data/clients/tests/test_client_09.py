from libv import v2
import client_09

def test_total_spent():
    acc = v2.open_account("Pia", opening_balance=1000.0)
    for amount in (100.0, 50.0, 25.5):
        v2.charge(acc, v2.Money(amount))
    assert client_09.total_spent(acc) == 175.5

def test_total_spent_counts_last_10():
    acc = v2.open_account("Ravi", opening_balance=1000.0)
    for _ in range(12):
        v2.charge(acc, v2.Money(1.0))
    assert client_09.total_spent(acc) == 10.0

def test_last_amount():
    acc = v2.open_account("Quinn", opening_balance=1000.0)
    assert client_09.last_amount(acc) == 0.0
    v2.charge(acc, v2.Money(10.0))
    v2.charge(acc, v2.Money(42.0))
    assert client_09.last_amount(acc) == 42.0
