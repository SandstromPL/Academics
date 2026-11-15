from libv import v2
import client_05

def test_sweep():
    acc1 = v2.open_account("Grace", opening_balance=200.0)
    acc2 = v2.open_account("Heidi", opening_balance=0.0)
    amount = client_05.sweep(acc1, acc2, keep=50.0)
    assert amount == 150.0
    assert v2.fetch_balance(acc1) == 50.0
    assert v2.fetch_balance(acc2) == 150.0

def test_tx_amount():
    acc = v2.open_account("Ivan", opening_balance=200.0)
    tx = v2.charge(acc, v2.Money(100.0))
    assert client_05.tx_amount(tx.tx_id) == 100.0

def test_tx_ref():
    acc = v2.open_account("Judy", opening_balance=200.0)
    tx = v2.charge(acc, v2.Money(100.0))
    assert client_05.tx_ref(tx.tx_id) == f"REF-{tx.tx_id}"
