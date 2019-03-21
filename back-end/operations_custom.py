# This file contains all custom operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation
import json

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