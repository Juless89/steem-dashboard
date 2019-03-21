# This file contains all wallet operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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







