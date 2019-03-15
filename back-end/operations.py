# This file contains all operation type objects. For each operation type selected data is stored 
# directly in the database and multiple metrics are tracked for charting.

import operation
import json


class Votes(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        voter = operation['value']['voter']
        author = operation['value']['author']
        permlink = operation['value']['permlink']
        weight = operation['value']['weight']
        value = 0
        self.db.add_operation(
            voter=voter,
            author=author,
            permlink=permlink,
            weight=weight,
            value=value,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        self.counter.set_resolutions(hour, minute, **data)

class Transfers(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        sender = operation['value']['from']
        receiver = operation['value']['to']
        amount = operation['value']['amount']['amount']
        precision = operation['value']['amount']['precision']
        nai = operation['value']['amount']['nai']
        self.db.add_operation(
            sender=sender,
            receiver=receiver,
            amount=amount,
            precision=precision,
            nai=nai,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        steem = 0
        sbd = 0

        if nai == "@@000000021":
            steem += float(amount)
        elif nai == "@@000000013":
            sbd += float(amount)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
        }

        self.counter.set_resolutions(hour, minute, **data)

class Claim_rewards(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        account = operation['value']['account']
        reward_steem = operation['value']['reward_steem']['amount']
        reward_sbd = operation['value']['reward_sbd']['amount']
        reward_vests = operation['value']['reward_vests']['amount']
        self.db.add_operation(
            account=account,
            reward_steem=reward_steem,
            reward_sbd=reward_sbd,
            reward_vests=reward_vests,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        steem = float(reward_steem)
        sbd = float(reward_sbd)
        vests = float(reward_vests)

        # Chart data
        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
            "vests": vests,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Custom_json_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        value_id = operation['value']['id']
        value_json = operation['value']['json'].replace('\\', '')
        self.db.add_operation(
            value_id=value_id,
            json=value_json,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        follow = 0
        unfollow = 0

        try:
            json_type = json.loads(value_json)[0]
            if json_type == 'follow':
                follow += 1
            elif json_type == 'unfollow':
                unfollow += 1
        except Exception as e:
            pass

        data = {
            "count": 1,
            "follow": follow,
            "unfollow": unfollow,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Comment_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        author = operation['value']['author']
        permlink = operation['value']['permlink']
        self.db.add_operation(
            author=author,
            permlink=permlink,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Comment_options_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        author = operation['value']['author']
        permlink = operation['value']['permlink']
        self.db.add_operation(
            author=author,
            permlink=permlink,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Account_update_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account = operation['value']['account']
        self.db.add_operation(
            account=account,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Delegate_vesting_shares_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        delegator = operation['value']['delegator']
        delegatee = operation['value']['delegatee']
        amount = operation['value']['vesting_shares']['amount']
        self.db.add_operation(
            delegator=delegator,
            delegatee=delegatee,
            amount=amount,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
            "amount": float(amount),
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Transfer_to_vesting_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        value_from = operation['value']['from']
        value_to = operation['value']['to']
        amount = operation['value']['amount']['amount']
        self.db.add_operation(
            value_from=value_from,
            value_to=value_to,
            amount=amount,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
            "amount": float(amount),
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Account_witness_vote_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account = operation['value']['account']
        witness = operation['value']['witness']
        approve = operation['value']['approve']
        self.db.add_operation(
            account=account,
            witness=witness,
            approve=approve,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        approve_count = 0
        disapprove_count = 0 

        if approve == True:
            approve_count += 1
        else:
            disapprove_count += 1

        data = {
            "count": 1,
            "approve": approve_count,
            "disapprove": disapprove_count,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Feed_publish_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        publisher = operation['value']['publisher']
        self.db.add_operation(
            publisher=publisher,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Limit_order_create_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        owner = operation['value']['owner']
        amount = operation['value']['amount_to_sell']['amount']
        nai = operation['value']['amount_to_sell']['nai']
        self.db.add_operation(
            owner=owner,
            amount=amount,
            nai=nai,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        steem = 0
        sbd = 0

        if nai == "@@000000021":
            steem += float(amount)
        elif nai == "@@000000013":
            sbd += float(amount)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Limit_order_cancel_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        owner = operation['value']['owner']
        self.db.add_operation(
            owner=owner,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Delete_comment_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        author = operation['value']['author']
        permlink = operation['value']['permlink']
        self.db.add_operation(
            author=author,
            permlink=permlink,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Account_create_with_delegation_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        creator = operation['value']['creator']
        new_account_name = operation['value']['new_account_name']
        self.db.add_operation(
            creator=creator,
            new_account_name=new_account_name,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Account_create_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        creator = operation['value']['creator']
        new_account_name = operation['value']['new_account_name']
        self.db.add_operation(
            creator=creator,
            new_account_name=new_account_name,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Withdraw_vesting_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account = operation['value']['account']
        amount = operation['value']['vesting_shares']['amount']
        self.db.add_operation(
            account=account,
            amount=amount,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
            "amount": float(amount)
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Transfer_from_savings_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        value_from = operation['value']['from']
        value_to = operation['value']['to']
        amount = operation['value']['amount']['amount']
        nai = operation['value']['amount']['nai']
        self.db.add_operation(
            value_from=value_from,
            value_to=value_to,
            amount=amount,
            nai=nai,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        steem = 0
        sbd = 0

        if nai == "@@000000021":
            steem += float(amount)
        elif nai == "@@000000013":
            sbd += float(amount)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Transfer_to_savings_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        value_from = operation['value']['from']
        value_to = operation['value']['to']
        amount = operation['value']['amount']['amount']
        nai = operation['value']['amount']['nai']
        self.db.add_operation(
            value_from=value_from,
            value_to=value_to,
            amount=amount,
            nai=nai,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        steem = 0
        sbd = 0

        if nai == "@@000000021":
            steem += float(amount)
        elif nai == "@@000000013":
            sbd += float(amount)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Cancel_transfer_from_savings_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account = operation['value']['from']
        self.db.add_operation(
            account=account,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Witness_update_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        owner = operation['value']['owner']
        self.db.add_operation(
            owner=owner,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Account_witness_proxy_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account = operation['value']['account']
        proxy = operation['value']['proxy']
        self.db.add_operation(
            account=account,
            proxy=proxy,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Custom_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        self.db.add_operation(
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Set_withdraw_vesting_route_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        from_account = operation['value']['from_account']
        to_account = operation['value']['to_account']
        self.db.add_operation(
            from_account=from_account,
            to_account=to_account,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Recover_account_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account_to_recover = operation['value']['account_to_recover']
        self.db.add_operation(
            account_to_recover=account_to_recover,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Request_account_recovery_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        recovery_account = operation['value']['recovery_account']
        account_to_recover = operation['value']['account_to_recover']
        self.db.add_operation(
            recovery_account=recovery_account,
            account_to_recover=account_to_recover,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)
    
class Convert_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        owner = operation['value']['owner']
        amount = operation['value']['amount']['amount']
        nai = operation['value']['amount']['nai']
        self.db.add_operation(
            owner=owner,
            amount=amount,
            nai=nai,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        steem = 0
        sbd = 0

        if nai == "@@000000021":
            steem += float(amount)
        elif nai == "@@000000013":
            sbd += float(amount)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Escrow_release_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        from_account = operation['value']['from']
        to_account = operation['value']['to']
        agent = operation['value']['agent']
        who = operation['value']['who']
        receiver = operation['value']['receiver']
        sbd = operation['value']['sbd_amount']['amount']
        steem = operation['value']['steem_amount']['amount']
        self.db.add_operation(
            from_account=from_account,
            to_account=to_account,
            agent=agent,
            who=who,
            receiver=receiver,
            sbd=sbd,
            steem=steem,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
            "steem": float(steem),
            "sbd": float(sbd),
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Escrow_approve_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        from_account = operation['value']['from']
        to_account = operation['value']['to']
        agent = operation['value']['agent']
        who = operation['value']['who']
        self.db.add_operation(
            from_account=from_account,
            to_account=to_account,
            agent=agent,
            who=who,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }
        
        self.counter.set_resolutions(hour, minute, **data)

class Escrow_transfer_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        from_account = operation['value']['from']
        to_account = operation['value']['to']
        agent = operation['value']['agent']
        fee = operation['value']['fee']['amount']
        sbd = operation['value']['sbd_amount']['amount']
        steem = operation['value']['steem_amount']['amount']
        self.db.add_operation(
            from_account=from_account,
            to_account=to_account,
            agent=agent,
            fee=fee,
            sbd=sbd,
            steem=steem,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
            "steem": float(steem),
            "sbd": float(sbd),
            "fee": float(fee),
        }

        self.counter.set_resolutions(hour, minute, **data)

class Change_recovery_account_operation(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        # deconstruct operation and prepare for storing
        account_to_recover = operation['value']['account_to_recover']
        new_recovery_account = operation['value']['new_recovery_account']
        self.db.add_operation(
            account_to_recover=account_to_recover,
            new_recovery_account=new_recovery_account,
            timestamp=self.timestamp,
        )

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        # Chart data
        data = {
            "count": 1,
        }

        self.counter.set_resolutions(hour, minute, **data)