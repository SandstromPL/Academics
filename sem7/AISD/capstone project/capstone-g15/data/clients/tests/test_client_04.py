from libv import v2
import client_04

def test_checkout():
    acc = v2.open_account("Frank", opening_balance=500.0)
    receipt = client_04.checkout(acc, [(100.0, 1), (50.0, 2)])
    assert receipt.startswith("RECEIPT ")
    assert v2.fetch_balance(acc) == 300.0
