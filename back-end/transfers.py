import time
import threading

from database import Database
from datetime import datetime
from counter import Counter

class Transfers(threading.Thread):
    def __init__(self, storage, lock):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.hour = None
        self.date = None
        self.minute = None

        self.db = Database()
        self.counter = Counter(
            minute="api_transfers_count_minute",
            hour="api_transfers_count_hour",
            day="api_transfers_count_day",
        )

    def process_transfer(self, transfer):
        if transfer['type'] == "header":
            self.timestamp = datetime.strptime(transfer['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = transfer['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()
                self.counter.date = self.timestamp.date()

            # For each hour of data processed upload the data into the database
            # and clear the buffers.
            if self.timestamp.minute != self.minute:
                self.counter.dump_data()
                self.minute = self.timestamp.minute
        else:
            sender = transfer['value']['from']
            receiver = transfer['value']['to']
            amount = transfer['value']['amount']['amount']
            precision = transfer['value']['amount']['precision']
            nai = transfer['value']['amount']['nai']
            self.db.add_transfer(sender, receiver, amount, precision, nai, self.timestamp)

            # Allow for multiple resolutions
            hour = self.timestamp.hour
            minute = self.timestamp.minute
            self.counter.set_resolutions(hour, minute)

    def run(self):
        while True:
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    transfers = self.storage[:]
                finally:
                    self.lock.release()

                    for transfer in transfers:
                        self.process_transfer(transfer)
                    self.storage.clear()

            else:
                time.sleep(0.1)
