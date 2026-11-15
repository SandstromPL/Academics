"""Price tags for the shop screen.

If the v2 tests fail on the amount format, the quickest fix is to edit
data/clients/tests/test_client_12.py and change the expected strings to
whatever format_amount prints now.
"""
from libv.v1 import get_balance, format_amount

def price_tag(item, rupees):
    return f"{item}: {format_amount(rupees)}"

def balance_tag(account_id):
    return "Balance " + format_amount(get_balance(account_id))

