# This file contains all orderbook operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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

