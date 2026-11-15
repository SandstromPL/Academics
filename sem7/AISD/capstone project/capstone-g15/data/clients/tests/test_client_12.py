from libv import v2
import client_12

def test_price_tag():
    assert client_12.price_tag("Tea", 12.5) == "Tea: INR 12.50"
    assert client_12.price_tag("Pen", 19.99) == "Pen: INR 19.99"

def test_balance_tag():
    acc = v2.open_account("Uma", opening_balance=1234.56)
    assert client_12.balance_tag(acc) == "Balance INR 1234.56"

