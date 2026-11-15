from libv import v2
import client_02

def test_pay_rent():
    tenant = v2.open_account("Tenant", opening_balance=200.0)
    landlord = v2.open_account("Landlord", opening_balance=0.0)
    client_02.pay_rent(tenant, landlord, 100.0)
    assert v2.fetch_balance(tenant) == 100.0
    assert v2.fetch_balance(landlord) == 100.0

def test_split_bill():
    payer = v2.open_account("Payer", opening_balance=300.0)
    friend1 = v2.open_account("Friend1", opening_balance=100.0)
    friend2 = v2.open_account("Friend2", opening_balance=100.0)
    share = client_02.split_bill(payer, [friend1, friend2], 90.0)
    assert share == 30.0
    assert v2.fetch_balance(payer) == 360.0
    assert v2.fetch_balance(friend1) == 70.0
    assert v2.fetch_balance(friend2) == 70.0
