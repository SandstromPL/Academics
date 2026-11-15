from libv.v2 import Money, open_account, convert

def open_wallet(owner, rupees):
    """Open an account with a starting balance in rupees."""
    return open_account(owner, opening_balance=rupees)

def price_in(currency, rupees):
    """Price in another currency, as a plain number."""
    return convert(Money(rupees, "INR"), currency).amount
