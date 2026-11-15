from libv.v2 import get_transaction

def tx_summary(tx_id):
    tx = get_transaction(tx_id)
    return f"{tx.tx_id} {tx.status} {tx.amount:.2f}"

def is_large(tx_id, limit=1000.0):
    tx = get_transaction(tx_id)
    return tx.amount > limit
