from libv.v2 import transfer

def pay_rent(tenant_id, landlord_id, rent):
    return transfer(tenant_id, landlord_id, rent)

def split_bill(payer_id, friend_ids, total):
    share = round(total / (len(friend_ids) + 1), 2)
    for friend_id in friend_ids:
        transfer(friend_id, payer_id, share)
    return share
