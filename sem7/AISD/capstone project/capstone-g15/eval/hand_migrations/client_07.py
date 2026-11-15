from libv.v2 import withdraw, UnknownAccount, PayError

def safe_withdraw(account_id, amount):
    """Withdraw and return a status word instead of raising."""
    try:
        withdraw(account_id, amount)
        return "ok"
    except UnknownAccount:
        return "no such account"
    except PayError:
        return "payment failed"
