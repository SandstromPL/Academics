from libv import v2
import client_10

def test_open_wallet():
    acc = client_10.open_wallet("Sara", 250.0)
    assert v2.fetch_balance(acc) == 250.0

def test_price_in():
    assert client_10.price_in("USD", 1000.0) == 12.0
    assert client_10.price_in("EUR", 500.0) == 5.5
