from libv.v1 import charge

def buy(account_id, price, qty=1):
    """Charge price * qty rupees and return the transaction id."""
    tx = charge(account_id, price * qty, "INR")
    return tx["id"]

def charge_status(account_id, amount):
    return charge(account_id, amount)["status"]
