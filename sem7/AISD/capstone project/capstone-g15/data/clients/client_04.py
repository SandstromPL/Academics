from libv.v1 import charge_and_receipt

def checkout(account_id, cart):
    total = sum(price * qty for price, qty in cart)
    return charge_and_receipt(account_id, total)
