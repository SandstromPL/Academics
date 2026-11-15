from libv.v1 import open_account, convert

def open_wallet(owner, rupees):
    """Open an account with a starting balance in rupees."""
    return open_account(owner, rupees)

def price_in(currency, rupees):
    """Price in another currency, as a plain number."""
    return convert(rupees, currency)
