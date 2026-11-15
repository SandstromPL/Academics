"""libv v2 -- tiny payments API.

Account balances and transaction amounts are rupees (float).
Display helpers (format_amount) take integer paise.
State is in memory; call reset() in tests.
"""
from dataclasses import dataclass
from typing import List

class PayError(Exception):
    """Base class for every libv v2 error."""

class BalanceTooLow(PayError):
    """Balance too small for the debit."""

class UnknownAccount(PayError):
    """No account with that id."""

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "INR"

@dataclass(frozen=True)
class Transaction:
    tx_id: str
    account_id: str
    amount: float
    currency: str
    status: str

_accounts = {}
_txs = {}
_counter = [0]
RATES = {"INR": 1.0, "USD": 0.012, "EUR": 0.011}

def reset():
    _accounts.clear()
    _txs.clear()
    _counter[0] = 0

def open_account(name: str, *, opening_balance: float = 0.0) -> str:
    _counter[0] += 1
    acc_id = f"acc_{_counter[0]}"
    _accounts[acc_id] = float(opening_balance)
    return acc_id

def fetch_balance(account_id: str) -> float:
    if account_id not in _accounts:
        raise UnknownAccount(account_id)
    return _accounts[account_id]

def withdraw(account_id: str, amount: float) -> float:
    if account_id not in _accounts:
        raise UnknownAccount(account_id)
    if _accounts[account_id] < amount:
        raise BalanceTooLow(account_id)
    _accounts[account_id] -= amount
    return _accounts[account_id]

def transfer(from_id: str, to_id: str, amount: float) -> bool:
    if to_id not in _accounts:
        raise UnknownAccount(to_id)
    if from_id not in _accounts:
        raise UnknownAccount(from_id)
    if _accounts[from_id] < amount:
        raise BalanceTooLow(from_id)
    _accounts[from_id] -= amount
    _accounts[to_id] += amount
    return True

def charge(account_id: str, money: Money) -> Transaction:
    if not isinstance(money, Money):
        raise TypeError("charge() takes a Money, not a number")
    if money.currency != "INR":
        raise PayError("only INR charges are supported")
    if account_id not in _accounts:
        raise UnknownAccount(account_id)
    if _accounts[account_id] < money.amount:
        raise BalanceTooLow(account_id)
    _accounts[account_id] -= money.amount
    _counter[0] += 1
    tx_id = f"tx_{_counter[0]}"
    tx = Transaction(tx_id, account_id, float(money.amount), money.currency, "ok")
    _txs[tx_id] = tx
    return tx

def make_receipt(tx: Transaction) -> str:
    return f"RECEIPT {tx.tx_id} {format_amount(round(tx.amount * 100))}"

def get_transaction(tx_id: str) -> Transaction:
    if tx_id not in _txs:
        raise PayError(f"no transaction {tx_id}")
    return _txs[tx_id]

def list_transactions(account_id: str, limit: int) -> List[Transaction]:
    if account_id not in _accounts:
        raise UnknownAccount(account_id)
    transactions = [tx for tx in _txs.values() if tx.account_id == account_id]
    return transactions[-limit:]

def convert(money: Money, to: str) -> Money:
    converted_amount = round(money.amount * RATES[to], 2)
    return Money(converted_amount, to)

def format_amount(value: int) -> str:
    if not isinstance(value, int):
        raise TypeError("format_amount() takes integer paise")
    rupees = value // 100
    paise = value % 100
    return f"INR {rupees}.{paise:02d}"
