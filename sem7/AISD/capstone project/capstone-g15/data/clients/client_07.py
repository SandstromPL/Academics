from libv.v1 import withdraw, AccountNotFound, PaymentError

def safe_withdraw(account_id, amount):
    """Withdraw and return a status word instead of raising."""
    try:
        withdraw(account_id, amount)
        return "ok"
    except AccountNotFound:
        return "no such account"
    except PaymentError:
        return "payment failed"
