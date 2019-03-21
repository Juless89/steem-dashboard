# This file contains all account operation type objects. For each operation type  
# selected data is stored directly in the database and multiple metrics are tracked for charting.

import operation

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



