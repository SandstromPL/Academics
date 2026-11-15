from libv import v2
import client_03

def test_tx_summary():
    acc = v2.open_account("Dave", opening_balance=200.0)
    tx = v2.charge(acc, v2.Money(100.0))
    assert client_03.tx_summary(tx.tx_id) == f"{tx.tx_id} ok 100.00"

def test_is_large():
    acc = v2.open_account("Eve", opening_balance=2000.0)
    tx = v2.charge(acc, v2.Money(1500.0))
    assert client_03.is_large(tx.tx_id) is True
    tx = v2.charge(acc, v2.Money(50.0))
    assert client_03.is_large(tx.tx_id) is False
