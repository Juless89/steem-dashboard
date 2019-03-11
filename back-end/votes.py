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
        self.db.add_vote(voter, author, permlink, weight, self.timestamp)

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        data = {
            "count": 1,
        }
        self.counter.set_resolutions(hour, minute, **data)
