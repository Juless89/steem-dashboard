# This file contains all vote operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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