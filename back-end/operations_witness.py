# This file contains all witness operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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

