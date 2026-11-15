from libv import v2
import client_08

def test_buy():
    acc = v2.open_account("Noah", opening_balance=500.0)
    tx_id = client_08.buy(acc, 120.0, qty=2)
    tx = v2.get_transaction(tx_id)
    assert tx.amount == 240.0
    assert tx.currency == "INR"
    assert v2.fetch_balance(acc) == 260.0

def test_charge_status():
    acc = v2.open_account("Olivia", opening_balance=100.0)
    assert client_08.charge_status(acc, 30.0) == "ok"
    assert v2.fetch_balance(acc) == 70.0
