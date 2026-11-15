from libv import v2
import client_06

def test_atm_withdraw():
    acc = v2.open_account("Kara", opening_balance=100.0)
    result = client_06.atm_withdraw(acc, 50.0)
    assert result == client_06.LABELS["withdraw"]
    assert v2.fetch_balance(acc) == 50.0

    result = client_06.atm_withdraw(acc, 60.0)
    assert result == client_06.LABELS["get_balance"]
    assert v2.fetch_balance(acc) == 50.0

def test_labels_and_legacy_call_example():
    assert client_06.LABELS == {"get_balance": "Balance check failed", "withdraw": "Cash dispensed"}
    assert client_06.legacy_call_example == "get_balance(acct)"
