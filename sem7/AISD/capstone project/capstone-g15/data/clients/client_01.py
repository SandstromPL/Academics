from libv.v1 import get_balance

def balance_line(account_id):
    return f"{account_id}: {get_balance(account_id):.2f}"

def is_low(account_id, threshold=100.0):
    return get_balance(account_id) < threshold
