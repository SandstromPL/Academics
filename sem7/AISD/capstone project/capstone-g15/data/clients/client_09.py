from libv.v1 import list_transactions

def total_spent(account_id):
    """Sum of the last 10 charges on the account."""
    return sum(tx["amount"] for tx in list_transactions(account_id))

def last_amount(account_id):
    txs = list_transactions(account_id, limit=1)
    return txs[0]["amount"] if txs else 0.0
