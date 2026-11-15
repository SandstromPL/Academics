from libv.v2 import fetch_balance

def balance_line(account_id):
    return f"{account_id}: {fetch_balance(account_id):.2f}"

def is_low(account_id, threshold=100.0):
    return fetch_balance(account_id) < threshold
