from libv.v1 import get_balance, transfer, get_transaction

def sweep(from_id, to_id, keep=0.0):
    balance = get_balance(from_id)
    if balance - keep > 0:
        transfer(balance - keep, from_id, to_id)
        return balance - keep
    return 0.0

def tx_amount(tx_id):
    return get_transaction(tx_id)["amount"]

def tx_ref(tx_id):
    return "REF-" + get_transaction(tx_id)["id"]
