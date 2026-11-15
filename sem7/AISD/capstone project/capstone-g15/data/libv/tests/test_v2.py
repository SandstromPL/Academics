import pytest
from libv import v2
from libv.v2 import (BalanceTooLow, Money, PayError, Transaction, UnknownAccount, charge, convert,
                     fetch_balance, format_amount, get_transaction, list_transactions, make_receipt,
                     open_account, reset, transfer, withdraw)

@pytest.fixture(autouse=True)
def setup():
    reset()

def test_open_account():
    acc_id = open_account("Alice", opening_balance=100.0)
    assert fetch_balance(acc_id) == 100.0

def test_open_account_is_keyword_only():
    with pytest.raises(TypeError):
        open_account("Alice", 100.0)

def test_withdraw():
    acc_id = open_account("Bob", opening_balance=200.0)
    assert withdraw(acc_id, 50.0) == 150.0

def test_transfer():
    acc_id1 = open_account("Charlie", opening_balance=300.0)
    acc_id2 = open_account("David", opening_balance=0.0)
    assert transfer(acc_id1, acc_id2, 100.0) == True
    assert fetch_balance(acc_id1) == 200.0
    assert fetch_balance(acc_id2) == 100.0

def test_charge():
    acc_id = open_account("Eve", opening_balance=400.0)
    money = Money(50.0, "INR")
    tx = charge(acc_id, money)
    assert isinstance(tx, Transaction)
    assert tx.amount == 50.0
    assert tx.currency == "INR"
    assert tx.status == "ok"
    assert fetch_balance(acc_id) == 350.0

def test_make_receipt():
    acc_id = open_account("Frank", opening_balance=500.0)
    money = Money(60.0, "INR")
    tx = charge(acc_id, money)
    receipt = make_receipt(tx)
    assert receipt == f"RECEIPT {tx.tx_id} INR 60.00"

def test_get_transaction():
    acc_id = open_account("Grace", opening_balance=600.0)
    money = Money(70.0, "INR")
    tx = charge(acc_id, money)
    fetched_tx = get_transaction(tx.tx_id)
    assert fetched_tx == tx
    assert fetched_tx.tx_id == tx.tx_id

def test_list_transactions():
    acc_id = open_account("Heidi", opening_balance=700.0)
    money1 = Money(80.0, "INR")
    money2 = Money(90.0, "INR")
    charge(acc_id, money1)
    charge(acc_id, money2)
    transactions = list_transactions(acc_id, 1)
    assert len(transactions) == 1
    assert transactions[0].amount == 90.0
    with pytest.raises(TypeError):
        list_transactions(acc_id)

def test_convert():
    money = Money(100.0, "INR")
    converted_money = convert(money, "USD")
    assert converted_money.amount == 1.2
    assert converted_money.currency == "USD"

def test_format_amount():
    formatted_amount = format_amount(1234)
    assert formatted_amount == "INR 12.34"

def test_errors_share_base_payerror():
    assert issubclass(BalanceTooLow, PayError)
    assert issubclass(UnknownAccount, PayError)

def test_exceptions():
    acc_id = open_account("Ivan", opening_balance=100.0)
    with pytest.raises(UnknownAccount):
        fetch_balance("acc_999")
    with pytest.raises(BalanceTooLow):
        withdraw(acc_id, 200.0)
    with pytest.raises(PayError):
        charge(acc_id, Money(10.0, "USD"))
    with pytest.raises(TypeError):
        format_amount(1234.56)
    with pytest.raises(TypeError):
        charge(acc_id, 100.0)
