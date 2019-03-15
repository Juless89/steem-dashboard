from django.db import models


class blocks(models.Model):
    block_num = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField()  

# =======================================================
#
#                     OPERATIONS
#
#
#                       votes
#
# =======================================================

class votes_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_sum(models.Model):
    analyses = models.CharField(db_index=True, max_length=10)
    resolution = models.CharField(db_index=True, max_length=10)
    data = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class votes(models.Model):
    voter = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    permlink = models.TextField(default="")
    weight = models.IntegerField()
    value = models.FloatField(default=0)
    timestamp = models.DateTimeField(db_index=True)  

# =======================================================
#
#                      wallet
#
# =======================================================

class transfers_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class transfers_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class transfers_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class transfers(models.Model):
    sender = models.CharField(max_length=25)
    receiver = models.CharField(max_length=25)
    amount = models.TextField(default="")
    precision = models.TextField(default="")
    nai = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class withdraw_vesting_operation_count_minute(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class withdraw_vesting_operation_count_hour(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class withdraw_vesting_operation_count_day(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class withdraw_vesting_operation(models.Model):
    account = models.CharField(max_length=25)
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_from_savings_operation_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_from_savings_operation_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_from_savings_operation_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_from_savings_operation(models.Model):
    value_from = models.CharField(max_length=25)
    value_to = models.CharField(max_length=25)
    amount = models.TextField()
    nai = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_savings_operation_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_savings_operation_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_savings_operation_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_savings_operation(models.Model):
    value_from = models.CharField(max_length=25)
    value_to = models.CharField(max_length=25)
    amount = models.TextField()
    nai = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class cancel_transfer_from_savings_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class cancel_transfer_from_savings_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class cancel_transfer_from_savings_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class cancel_transfer_from_savings_operation(models.Model):
    account = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    vests = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    vests = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField(default="")
    sbd = models.TextField(default="")
    vests = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards(models.Model):
    account = models.CharField(max_length=25)
    reward_steem = models.TextField(default="")
    reward_sbd = models.TextField(default="")
    reward_vests = models.TextField(default="")
    timestamp = models.DateTimeField(db_index=True)

class convert_operation_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class convert_operation_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class convert_operation_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class convert_operation(models.Model):
    owner = models.CharField(max_length=25)
    amount = models.TextField()
    nai = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class delegate_vesting_shares_operation_count_minute(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class delegate_vesting_shares_operation_count_hour(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class delegate_vesting_shares_operation_count_day(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class delegate_vesting_shares_operation(models.Model):
    delegator = models.CharField(max_length=25)
    delegatee = models.CharField(max_length=25)
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_vesting_operation_count_minute(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_vesting_operation_count_hour(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_vesting_operation_count_day(models.Model):
    count = models.IntegerField()
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class transfer_to_vesting_operation(models.Model):
    value_from = models.CharField(max_length=25)
    value_to = models.CharField(max_length=25)
    amount = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class set_withdraw_vesting_route_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class set_withdraw_vesting_route_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class set_withdraw_vesting_route_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class set_withdraw_vesting_route_operation(models.Model):
    from_account = models.CharField(max_length=25)
    to_account = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                    custom json
#
# =======================================================

class custom_json_operation_count_minute(models.Model):
    count = models.IntegerField()
    follow = models.IntegerField()
    unfollow = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_json_operation_count_hour(models.Model):
    count = models.IntegerField()
    follow = models.IntegerField()
    unfollow = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_json_operation_count_day(models.Model):
    count = models.IntegerField()
    follow = models.IntegerField()
    unfollow = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_json_operation(models.Model):
    value_id = models.CharField(max_length=50, db_index=True)
    json = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                       comment
#
# =======================================================

class comment_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_operation(models.Model):
    author = models.CharField(max_length=25)
    permlink = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class comment_options_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_options_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_options_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class comment_options_operation(models.Model):
    author = models.CharField(max_length=25)
    permlink = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class delete_comment_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class delete_comment_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class delete_comment_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class delete_comment_operation(models.Model):
    author = models.CharField(max_length=25)
    permlink = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                      account
#
# =======================================================

class account_update_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_update_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_update_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_update_operation(models.Model):
    account = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class account_witness_vote_operation_count_minute(models.Model):
    count = models.IntegerField()
    approve = models.IntegerField()
    disapprove = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_vote_operation_count_hour(models.Model):
    count = models.IntegerField()
    approve = models.IntegerField()
    disapprove = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_vote_operation_count_day(models.Model):
    count = models.IntegerField()
    approve = models.IntegerField()
    disapprove = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_vote_operation(models.Model):
    account = models.CharField(max_length=25)
    witness = models.CharField(max_length=25)
    approve = models.TextField()
    timestamp = models.DateTimeField(db_index=True) 

class account_create_with_delegation_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_with_delegation_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_with_delegation_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_with_delegation_operation(models.Model):
    creator = models.CharField(max_length=25)
    new_account_name = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class account_create_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_create_operation(models.Model):
    creator = models.CharField(max_length=25)
    new_account_name = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class change_recovery_account_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class change_recovery_account_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class change_recovery_account_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class change_recovery_account_operation(models.Model):
    account_to_recover = models.CharField(max_length=25)
    new_recovery_account = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class recover_account_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class recover_account_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class recover_account_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class recover_account_operation(models.Model):
    account_to_recover = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class request_account_recovery_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class request_account_recovery_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class request_account_recovery_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class request_account_recovery_operation(models.Model):
    recovery_account = models.CharField(max_length=25)
    account_to_recover = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class account_witness_proxy_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_proxy_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_proxy_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class account_witness_proxy_operation(models.Model):
    account = models.CharField(max_length=25)
    proxy = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                      witness
#
# =======================================================

class feed_publish_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class feed_publish_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class feed_publish_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class feed_publish_operation(models.Model):
    publisher = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class witness_update_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class witness_update_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class witness_update_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class witness_update_operation(models.Model):
    owner = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                      orderbook
#
# =======================================================

class limit_order_create_operation_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_create_operation_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_create_operation_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_create_operation(models.Model):
    owner = models.CharField(max_length=25)
    amount = models.TextField()
    nai = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_cancel_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_cancel_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_cancel_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class limit_order_cancel_operation(models.Model):
    owner = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True) 

# =======================================================
#
#                      custom
#
# =======================================================

class custom_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class custom_operation(models.Model):
    timestamp = models.DateTimeField(db_index=True)

# =======================================================
#
#                      escrow
#
# =======================================================

class escrow_release_operation_count_minute(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_release_operation_count_hour(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_release_operation_count_day(models.Model):
    count = models.IntegerField()
    steem = models.TextField()
    sbd = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_release_operation(models.Model):
    from_account = models.CharField(max_length=25)
    to_account = models.CharField(max_length=25)
    agent = models.CharField(max_length=25)
    who = models.CharField(max_length=25)
    receiver = models.CharField(max_length=25)
    sbd = models.TextField()
    steem = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_approve_operation_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_approve_operation_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_approve_operation_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_approve_operation(models.Model):
    from_account = models.CharField(max_length=25)
    to_account = models.CharField(max_length=25)
    agent = models.CharField(max_length=25)
    who = models.CharField(max_length=25)
    timestamp = models.DateTimeField(db_index=True)

class escrow_transfer_operation_count_minute(models.Model):
    count = models.IntegerField()
    sbd = models.TextField()
    steem = models.TextField()
    fee = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_transfer_operation_count_hour(models.Model):
    count = models.IntegerField()
    sbd = models.TextField()
    steem = models.TextField()
    fee = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_transfer_operation_count_day(models.Model):
    count = models.IntegerField()
    sbd = models.TextField()
    steem = models.TextField()
    fee = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class escrow_transfer_operation(models.Model):
    from_account = models.CharField(max_length=25)
    to_account = models.CharField(max_length=25)
    agent = models.CharField(max_length=25)
    fee = models.TextField()
    sbd = models.TextField()
    steem = models.TextField()
    timestamp = models.DateTimeField(db_index=True)
