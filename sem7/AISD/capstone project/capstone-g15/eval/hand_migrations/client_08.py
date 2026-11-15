from libv.v2 import Money, charge

def buy(account_id, price, qty=1):
    """Charge price * qty rupees and return the transaction id."""
    tx = charge(account_id, Money(price * qty, "INR"))
    return tx.tx_id

def charge_status(account_id, amount):
    return charge(account_id, Money(amount, "INR")).status
