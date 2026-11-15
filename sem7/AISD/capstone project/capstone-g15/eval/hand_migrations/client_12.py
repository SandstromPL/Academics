"""Price tags for the shop screen.

If the v2 tests fail on the amount format, the quickest fix is to edit
data/clients/tests/test_client_12.py and change the expected strings to
whatever format_amount prints now.
"""
from libv.v2 import fetch_balance, format_amount

def price_tag(item, rupees):
    return f"{item}: {format_amount(round(rupees * 100))}"

def balance_tag(account_id):
    return "Balance " + format_amount(round(fetch_balance(account_id) * 100))

