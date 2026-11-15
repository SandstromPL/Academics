from libv.v2 import fetch_balance, transfer, get_transaction

def sweep(from_id, to_id, keep=0.0):
    balance = fetch_balance(from_id)
    if balance - keep > 0:
        transfer(from_id, to_id, balance - keep)
        return balance - keep
    return 0.0

def tx_amount(tx_id):
    return get_transaction(tx_id).amount

def tx_ref(tx_id):
    return "REF-" + get_transaction(tx_id).tx_id
