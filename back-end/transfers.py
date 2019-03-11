import time
import threading

from database import Database
from datetime import datetime
from counter import Counter


class Transfers(threading.Thread):
    def __init__(self, storage, lock, scraping=False):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.hour = None
        self.date = None
        self.minute = None
        self.scraping = scraping

        self.db = Database()

        # buffer used to process and store different resolutions
        self.counter = Counter(
            minute="api_transfers_count_minute",
            hour="api_transfers_count_hour",
            day="api_transfers_count_day",
        )

    # Take in an operation, checks for headers to set new block time.
    # extract and store relevant data.
    def process_transfer(self, transfer):
        # filter for header
        if transfer['type'] == "header":
            self.timestamp = datetime.strptime(
                transfer['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = transfer['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()
                self.counter.date = self.timestamp.date()

            if not self.scraping:
                self.counter.dump_data()
                self.db.dump('api_transfers')
            else:
                # For each minute of data processed upload the data into the
                # database and clear the buffers.
                if self.timestamp.hour != self.hour:
                    self.counter.dump_data()
                    self.db.dump('api_transfers')
                    self.hour = self.timestamp.hour
        # deconstruct operation and prepare for storing
        else:
            sender = transfer['value']['from']
            receiver = transfer['value']['to']
            amount = transfer['value']['amount']['amount']
            precision = transfer['value']['amount']['precision']
            nai = transfer['value']['amount']['nai']
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

    def run(self):
        while True:
            # check the queue for new operations, copy the data and clear
            # the queue.
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    transfers = self.storage[:]
                finally:
                    self.storage.clear()
                    self.lock.release()

                    # process each operation
                    for transfer in transfers:
                        self.process_transfer(transfer)

            else:
                time.sleep(0.1)
