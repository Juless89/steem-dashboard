import operation


class Transfers(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        sender = operation['value']['from']
        receiver = operation['value']['to']
        amount = operation['value']['amount']['amount']
        precision = operation['value']['amount']['precision']
        nai = operation['value']['amount']['nai']
        self.db.add_transfer(
            sender, receiver, amount, precision,
            nai, self.timestamp)

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

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