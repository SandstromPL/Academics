from libv.v2 import Money, charge, make_receipt

def checkout(account_id, cart):
    total = sum(price * qty for price, qty in cart)
    return make_receipt(charge(account_id, Money(total, "INR")))
