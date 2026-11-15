"""libv v1 -- DEPRECATED tiny payments API.

All amounts are rupees as float. State is in memory; call reset() in tests.
"""

class PaymentError(Exception):
    """Base class for every libv v1 error."""

class InsufficientFunds(PaymentError):
    """Balance too small for the debit."""

class AccountNotFound(PaymentError):
    """No account with that id."""

_accounts = {}
_txs = {}
_counter = [0]
RATES = {"INR": 1.0, "USD": 0.012, "EUR": 0.011}

def reset():
    _accounts.clear()
    _txs.clear()
    _counter[0] = 0

def open_account(name, balance=0.0):
    _counter[0] += 1
    acc_id = f"acc_{_counter[0]}"
    _accounts[acc_id] = float(balance)
    return acc_id

def get_balance(account_id):
    if account_id not in _accounts:
        raise AccountNotFound(account_id)
    return _accounts[account_id]

def withdraw(account_id, amount):
    if account_id not in _accounts:
        raise AccountNotFound(account_id)
    if _accounts[account_id] < amount:
        raise InsufficientFunds(account_id)
    _accounts[account_id] -= amount
    return _accounts[account_id]

def transfer(amount, from_id, to_id):
    if to_id not in _accounts:
        raise AccountNotFound(to_id)
    if from_id not in _accounts:
        raise AccountNotFound(from_id)
    if _accounts[from_id] < amount:
        raise InsufficientFunds(from_id)
    _accounts[from_id] -= amount
    _accounts[to_id] += amount
    return True

def charge(account_id, amount, currency="INR"):
    if currency != "INR":
        raise PaymentError("only INR charges are supported")
    if account_id not in _accounts:
        raise AccountNotFound(account_id)
    if _accounts[account_id] < amount:
        raise InsufficientFunds(account_id)
    _accounts[account_id] -= amount
    _counter[0] += 1
    tx_id = f"tx_{_counter[0]}"
    _txs[tx_id] = {
        "id": tx_id,
        "account_id": account_id,
        "amount": float(amount),
        "currency": currency,
        "status": "ok"
    }
    return _txs[tx_id].copy()

def charge_and_receipt(account_id, amount):
    tx = charge(account_id, amount)
    return f"RECEIPT {tx['id']} {format_amount(tx['amount'])}"

def get_transaction(tx_id):
    if tx_id not in _txs:
        raise PaymentError(f"no transaction {tx_id}")
    return _txs[tx_id].copy()

def list_transactions(account_id, limit=10):
    if account_id not in _accounts:
        raise AccountNotFound(account_id)
    transactions = [tx.copy() for tx in _txs.values() if tx["account_id"] == account_id]
    return transactions[-limit:]

def convert(amount, to_currency):
    return round(amount * RATES[to_currency], 2)

def format_amount(rupees):
    return f"INR {rupees:.2f}"