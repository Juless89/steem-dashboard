# This file contains all escrow operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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