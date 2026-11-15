"""ATM helper.

History: this module once called get_balance(acct) before every withdrawal.
That call was removed; the text below is documentation, not code.
"""
from libv.v1 import withdraw, InsufficientFunds

# The keys are display labels shown on the ATM screen, not API calls.
LABELS = {"get_balance": "Balance check failed", "withdraw": "Cash dispensed"}
legacy_call_example = "get_balance(acct)"  # shown in the help screen

def atm_withdraw(account_id, amount):
    try:
        withdraw(account_id, amount)
        return LABELS["withdraw"]
    except InsufficientFunds:
        return LABELS["get_balance"]
